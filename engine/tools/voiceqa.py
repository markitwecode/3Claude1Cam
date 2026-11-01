"""Consensus voice QA: three Whisper models vote on every narration sentence.

    vk qa [N] [-v]       list the flagged sentences of chapter N (or all), from audio/manifest.json
    vk voice [N] --qa-only   (re)run this QA on the cached clips: no re-voicing, timings untouched

Whisper base (faster-whisper, CPU) still produces the word timings, and its transcript is the
first vote. Whisper small and medium (MLX, on the GPU) transcribe the same audio. A sentence is
flagged when at least MIN_AGREE of the three models mishear the same script word(s), after
normalising what Whisper writes differently from the script: numbers, spelled letters ("ex",
"see-ess"), merged or split words ("phone book", "A, B, C" -> "ABC", "O(n)"), contractions, a
plural s swallowed by a following s, and near misses on jargon (a word missing from the system
dictionary, e.g. OCaml, conses, add-len). Common words are strict: "nil" -> "no",
"halve" -> "have", "type error" -> "tie bearer" all count.

voice.py retries a flagged sentence with new seeds (within its TRIES budget) and stores what is
still flagged in manifest[id]["qa"]:
    {"v": QA_VERSION, "models": [...],
     "flags": [{"s": sentence no. (1-based), "text": sentence, "why": "consensus" | "base-only",
                "sites": [{"expected": script words, "heard": {model: words}, "by": [models]}]}]}
"flags": [] means checked and clean. Lines without "qa" were voiced before this QA existed.
This module imports only the standard library at the top (status.py uses it from the manim venv).
"""
import difflib
import json
import re
import sys
from functools import cache
from pathlib import Path

QA_VERSION = 1
QA_MODELS = {   # extra voters (mlx-audio's Whisper port). base comes from voice.py's faster-whisper.
    "small": "mlx-community/whisper-small-asr-fp16",
    "medium": "mlx-community/whisper-medium-asr-fp16",
}
MIN_AGREE = 2           # models that must mishear the same script word(s)
JARGON_RATIO = 0.5      # a jargon word heard with at least this character similarity is fine

# ── normalisation ─────────────────────────────────────────────────────────────
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen \
fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
# letter names as the script spells them -> the letter Whisper writes. voice.py uses this map too.
LETTERS = {"ex": "x", "ell": "l", "why": "y", "exes": "xs", "whys": "ys", "en": "n", "eyedee": "id",
           "ay": "a", "bee": "b", "see": "c", "eye": "i", "jay": "j", "kay": "k",
           "ess": "s", "aitch": "h", "gee": "g", "eff": "f", "dee": "d", "em": "m", "pee": "p",
           "tee": "t", "vee": "v", "zed": "z", "zee": "z", "ells": "ls",
           "cue": "q", "queue": "q", "cues": "qs", "ar": "r", "ee": "e"}
# words that sound the same: Whisper's choice of spelling says nothing about the audio. The first
# word of a group is what the others become ("to" first, so "onto" still matches "on to").
_HOMOPHONES = ["to two too", "for four fore", "one won", "eight ate", "no know", "right write",
               "by buy bye", "their there theyre", "your youre", "whose whos", "here hear", "new knew",
               "tail tale", "tails tales", "some sum", "pair pear pare", "pairs pears", "whole hole",
               "piece peace", "weight wait", "week weak", "plain plane", "nil nill", "ok okay",
               "allright alright", "sell cell", "sells cells", "sent cent scent", "ys wise",
               "sight site cite", "sync sink"]
SAME = {w: group.split()[0] for group in _HOMOPHONES for w in group.split()[1:]}
_C = [SAME.get(w, w) for w in _ONES]          # number words as compared ("two" -> "to")
NUM_WORDS = {n: _C[n] if n < 20 else _TENS[n // 10] + ("" if n % 10 == 0 else _C[n % 10])
             for n in range(100)}
_NUMBER_WORDS = set(_ONES) | set(_TENS[2:]) | {"hundred", "thousand", "million", "billion"}
SPOKEN_MARKS = {"comma", "colon", "semicolon"}   # read out in code ("ex comma why"); Whisper writes "x, y"
# short words that run into a neighbouring jargon word ("consed onto" -> "consent to", "ex consed" ->
# "X's concessed"); content words next to jargon stay strict
FUNCTION = {"a", "an", "the", "of", "to", "in", "on", "onto", "into", "at", "it", "and", "for", "with",
            "from", "by", "as"}
ABSORBABLE = FUNCTION | {"is", "its"} | set(LETTERS.values())


def _digits(run):
    """A digit run as one token: < 100 -> words; bigger -> '<run>' (expanded per op, see _variants)."""
    n = int(run)
    return NUM_WORDS[n] if n < 100 and not (len(run) > 1 and run[0] == "0") else f"<{run}>"


def qa_token(raw):
    """One script or Whisper word -> the string the QA compares."""
    w = raw.lower().replace("’", "'").strip()
    w = re.sub(r"(?<=\d),(?=\d{3})", "", w)                 # 4,366
    w = re.sub(r"^\W*o\(", "bigoof", w)                      # O(n): "big O of en"
    w = w.replace("(", " of ").replace("²", " squared").replace("^2", " squared")
    w = w.replace("%", " percent").replace("&", " and ")
    w = re.sub(r"(\d*)\.(\d+)", lambda m: f"{m.group(1)} point {' '.join(m.group(2))}", w)  # 1.44, .44
    w = re.sub(r"(?<=[a-z0-9])-(?=\d)", " minus ", w)        # xn-1
    w = re.sub(r"(?<=[a-z0-9])\+(?=[a-z0-9])", " plus ", w)
    out = []
    for piece in re.split(r"[\s\-–—/]+", w):                 # hyphen parts: see-ess -> c + s
        piece = re.sub(r"[^a-z0-9]", "", piece)
        if piece in LETTERS or piece in SAME:
            out.append(LETTERS.get(piece) or SAME[piece])
            continue
        if piece.endswith("s") and piece[:-1] in SAME:          # two's ~ 2's
            out.append(SAME[piece[:-1]] + "s")
            continue
        for run in re.findall(r"[a-z]+|\d+", piece):         # a1 -> a + one
            out.append(_digits(run) if run.isdigit() else run)
    return "".join(out)


def _cardinal(n, use_and):
    if n < 100:
        return NUM_WORDS[n]
    if n < 1000:
        h, r = divmod(n, 100)
        return NUM_WORDS[h] + "hundred" + (("and" if use_and else "") + _cardinal(r, use_and) if r else "")
    for div, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= div:
            q, r = divmod(n, div)
            rest = ("and" if use_and and r < 100 else "") + _cardinal(r, use_and) if r else ""
            return _cardinal(q, use_and) + name + rest


def _spoken(run):
    forms = {"".join(NUM_WORDS[int(d)] for d in run), "".join("oh" if d == "0" else NUM_WORDS[int(d)]
                                                               for d in run)}
    if run[0] != "0" and len(run) <= 12:
        n = int(run)
        forms |= {_cardinal(n, True), _cardinal(n, False)}
        forms |= {"a" + f[3:] for f in forms if re.match(r"one(hundred|thousand|million|billion)", f)}
        if len(run) == 4 and run[2] != "0":                  # 1984: nineteen eighty-four
            forms.add(NUM_WORDS[int(run[:2])] + NUM_WORDS[int(run[2:])])
    return forms


def _variants(tokens):
    """Concatenations of tokens, with each '<digits>' expanded to its spoken forms."""
    out = {""}
    for part in re.split(r"(<\d+>)", "".join(tokens)):
        if part.startswith("<"):
            out = {o + f for o in out for f in _spoken(part[1:-1])}
        else:
            out = {o + part for o in out}
    return out


# ── jargon: words the system dictionary doesn't know ───────────────────────────
@cache
def _dictionary():
    for path in ("/usr/share/dict/words", "/usr/dict/words"):
        try:
            # lowercase entries only: capitalised ones are names ("Len", "Cleo"), which Whisper spells freely
            return frozenset(w for w in (x.strip() for x in open(path, encoding="utf-8", errors="ignore"))
                             if w == w.lower())
        except OSError:
            pass
    return frozenset()      # no dictionary: every word counts as common (strict)


_SUFFIXES = (("ies", "y"), ("es", ""), ("s", ""), ("ed", ""), ("ed", "e"), ("d", ""), ("ing", ""),
             ("ing", "e"), ("er", ""), ("ers", ""), ("ly", ""))


def _known(word, inflected=True):
    words = _dictionary()
    if not words or word in words or word in LETTERS or word in _NUMBER_WORDS:
        return True
    for suf, rep in _SUFFIXES if inflected else ():
        stem = word[:-len(suf)]
        if word.endswith(suf) and len(stem) >= 2:
            if stem + rep in words or (len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in words):
                return True
    return False


def is_identifier(raw):
    """A code name as the script spells it: hyphenated (in-sort, N-length) or mixed case (OCaml).
    Whisper renders these freely, so models only agree when they hear the same thing."""
    w = re.sub(r"[^A-Za-z\-]", "", raw)
    parts = [p for p in w.lower().split("-") if p]
    if len(parts) > 1 and all(p in _NUMBER_WORDS for p in parts):
        return False                    # twenty-one
    return len(parts) > 1 or bool(re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]", w))


def is_jargon(raw):
    """A word the dictionary doesn't know (OCaml, conses, Cleo). Each part of a hyphenated word
    must be a plain dictionary word, and none a letter name: the scripts spell code identifiers
    that way (add-len, rev-app, all-see), while English compounds (catch-all, run-time) stay strict."""
    w = re.sub(r"[^a-z'\-]", "", raw.lower().replace("’", "'"))
    w = re.sub(r"(n't|'s|'ll|'re|'ve|'d|'m|s')$", "", w).replace("'", "")
    parts = [p for p in w.split("-") if p]
    if len(parts) > 1 and any(p in LETTERS for p in parts):
        return True                     # a spelled identifier: all-see, en-sum, ex-why
    return any(not _known(p, inflected=len(parts) == 1) for p in parts)


# ── per-model errors and the consensus ─────────────────────────────────────────
def _plural_slip(S, i, h):
    """'solutions so far' heard as 'solution so far': the s runs into the next s sound."""
    s = S[i]
    nxt = S[i + 1] if i + 1 < len(S) else ""
    return (s == h + "s" or h == s + "s" or s == h + "es" or h == s + "es") and \
        nxt.startswith(("s", "z", "ce", "ci", "cy"))


def _ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def _undouble(w):
    return re.sub(r"(.)\1+", r"\1", w)


def _equivalent(S, jargon, H, i1, i2, j1, j2, nonword):
    """Is a replace op only a difference in how Whisper writes the same speech?"""
    heard = H[j1:j2]
    script = "".join(S[i1:i2])
    variants = _variants(heard)
    bare = "".join(t for t in S[i1:i2] if t not in SPOKEN_MARKS)
    if script in variants or bare in variants or _undouble(script) in {_undouble(v) for v in variants}:
        return True                    # merged/split words, numbers, "all together" / "altogether"
    if i2 - i1 == 1 == j2 - j1:
        if _plural_slip(S, i1, H[j1]):
            return True
        # Whisper invents a spelling ("reconciders") only for sounds it heard; a real mishearing
        # comes back as a real word ("have", "no", "pendant")
        if nonword[j1] and not jargon[i1] and _ratio(script, H[j1]) >= 0.85:
            return True
    if any(jargon[i1:i2]):
        common = [S[i] for i in range(i1, i2) if not jargon[i]]
        if all(c in heard for c in common):
            left = list(heard)
            for c in common:
                left.remove(c)
            target = "".join(S[i] for i in range(i1, i2) if jargon[i])
            if _ratio(target, min(_variants(left), key=len)) >= JARGON_RATIO:
                return True
        if set(common) <= ABSORBABLE and _ratio(script, min(variants, key=len)) >= 0.6:
            return True
    return False


def model_sites(S, jargon, H, nonword=None):
    """-> (opcodes, [(i1, i2) script spans this model got wrong]); i1 == i2 is an insertion.
    nonword[j]: heard word j isn't in the dictionary."""
    nonword = nonword or [False] * len(H)
    ops = difflib.SequenceMatcher(None, S, H, autojunk=False).get_opcodes()
    sites = [(i1, i2) for tag, i1, i2, j1, j2 in ops if tag != "equal"
             and not (tag == "replace" and _equivalent(S, jargon, H, i1, i2, j1, j2, nonword))
             and not (tag == "delete" and set(S[i1:i2]) <= SPOKEN_MARKS)]
    return ops, sites


def _touch(a, b):
    (a1, a2), (b1, b2) = a, b
    if a1 == a2 and b1 == b2:
        return abs(a1 - b1) <= 1
    if a1 == a2:
        return b1 <= a1 <= b2
    if b1 == b2:
        return a1 <= b1 <= a2
    return a1 < b2 and b1 < a2


def _heard_span(ops, a, b, n):
    """Heard-word index range for the script span [a, b)."""
    js = []
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            lo, hi = max(a, i1), min(b, i2)
            if lo < hi:
                js += [j1 + lo - i1, j1 + hi - i1]
        elif i1 == i2:
            if a < i1 < b or (i1 == a == 0) or (i1 == b == n):
                js += [j1, j2]
        elif i1 < b and a < i2:
            js += [j1, j2]
    return (min(js), max(js)) if js else (0, 0)


class _Line:
    """A line's script words prepared for comparison (tokens that normalise to nothing, like a
    lone dash, are left out and don't vote)."""

    def __init__(self, script_words):
        self.words = script_words
        tokens = [qa_token(w) for w in script_words]
        self.keep = [k for k, t in enumerate(tokens) if t]
        self.S = [tokens[k] for k in self.keep]
        self.jargon = [is_jargon(script_words[k]) for k in self.keep]
        self.ident = [is_identifier(script_words[k]) for k in self.keep]

    def span(self, lo, hi):
        """Compared-token span -> script word span (an insertion stays empty)."""
        start = self.keep[lo] if lo < len(self.keep) else len(self.words)
        return start, (self.keep[hi - 1] + 1 if hi > lo else start)

    def sites(self, heard):
        """One model's errors -> (heard, kept heard indices, opcodes, sites)."""
        merged = []
        for w in heard:                  # base writes 118,458 as "118" ",458": one number again
            if merged and re.match(r"\s*,\d{3}", w) and re.search(r"\d\W*$", merged[-1]):
                merged[-1] = merged[-1].rstrip() + w.strip()
            else:
                merged.append(w)
        heard = merged
        hk = [j for j, w in enumerate(heard) if qa_token(w)]
        H = [qa_token(heard[j]) for j in hk]
        nonword = [not re.search(r"\d", heard[j]) and is_jargon(heard[j]) for j in hk]
        ops, sites = model_sites(self.S, self.jargon, H, nonword)
        return heard, hk, ops, sites

    def core_heard(self, lo, hi, model):
        """The compared tokens one model heard for the error span [lo, hi)."""
        heard, hk, ops, _ = model
        got = []
        for tag, i1, i2, j1, j2 in ops:
            if tag != "equal" and ((i1 < hi and lo < i2) or (i1 == i2 and lo <= i1 <= hi)):
                got += [qa_token(heard[hk[j]]) for j in range(j1, j2)]
        return got

    def show(self, lo, hi, per):
        """Expected vs heard text for the span [lo, hi), with one word of context each side."""
        n = len(self.S)
        a, b = max(0, lo - 1), min(n, hi + 1)
        s0, s1 = self.span(a, b)
        heard = {}
        for m, (words, hk, ops, _) in per.items():
            j1, j2 = _heard_span(ops, a, b, n)
            heard[m] = " ".join(w.strip() for w in words[hk[j1]:hk[j2 - 1] + 1]) if j2 > j1 else ""
        return " ".join(self.words[s0:s1]), heard


def _owners(start, end, chunks):
    """Sentences a script word span belongs to; an insertion counts against the one it follows."""
    if start == end:
        start, end = max(0, start - 1), max(1, start)
    return [k for k, (a, b, _) in enumerate(chunks) if a < end and start < b] or [len(chunks) - 1]


def consensus(script_words, chunks, heard):
    """script_words: the line's words; chunks: voice.split_line's [(first, last+1, gap)];
    heard: {model: [Whisper word strings]}. -> {sentence index: [site dict, ...]}."""
    line = _Line(script_words)
    per = {m: line.sites(words) for m, words in heard.items()}
    items = [(m, s) for m in per for s in per[m][3]]
    parent = list(range(len(items)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for x in range(len(items)):
        for y in range(x + 1, len(items)):
            if items[x][0] != items[y][0] and _touch(items[x][1], items[y][1]):
                parent[find(x)] = find(y)
    groups = {}
    for x, it in enumerate(items):
        groups.setdefault(find(x), []).append(it)

    out = {}
    for group in groups.values():
        by = sorted({m for m, _ in group}, key=list(per).index)
        if len(by) < MIN_AGREE:
            continue
        lo, hi = min(s[0] for _, s in group), max(s[1] for _, s in group)
        if any(line.ident[lo:hi]):      # an identifier: only the same mishearing counts as agreement
            forms = {}
            for m in by:
                forms.setdefault("".join(line.core_heard(lo, hi, per[m])), []).append(m)
            by = max(forms.values(), key=len)
            if len(by) < MIN_AGREE:
                continue
        expected, said = line.show(lo, hi, per)
        site = {"expected": expected, "heard": said, "by": by}
        core = set(line.S[lo:hi])
        for m in by:
            core |= set(line.core_heard(lo, hi, per[m]))
        if core <= FUNCTION:            # only "a"/"the", "in"/"on"…: kept, but no retry or count
            site["minor"] = True
        for k in _owners(*line.span(lo, hi), chunks):
            out.setdefault(k, []).append(site)
    return out


def serious(votes):
    """consensus() without the minor sites: what triggers a retry and counts as flagged."""
    out = {k: [s for s in sites if not s.get("minor")] for k, sites in votes.items()}
    return {k: v for k, v in out.items() if v}


def base_sites(script_words, chunks, k, heard_base):
    """Base's own errors inside sentence k (the detail for a base-only WER/stutter flag)."""
    line = _Line(script_words)
    per = {"base": line.sites(heard_base)}
    out = []
    for lo, hi in per["base"][3]:
        if k in _owners(*line.span(lo, hi), chunks):
            expected, said = line.show(lo, hi, per)
            out.append({"expected": expected, "heard": said, "by": ["base"]})
    return out


def reported(qa):
    """The flags a voice run reports and counts: consensus and base-only (minor ones are listed
    by vk qa --all only)."""
    return [f for f in (qa or {}).get("flags", []) if f["why"] != "minor"]


def record(script_words, chunks, votes, base_bad=(), heard_base=None, models=None):
    """The manifest's "qa" entry for one line. votes = consensus(); base_bad = sentence indices
    voice.is_bad() still flags from base alone."""
    flags = []
    for k, (a, b, _) in enumerate(chunks):
        text = " ".join(script_words[a:b])
        if k in votes:
            minor = all(site.get("minor") for site in votes[k])
            flags.append({"s": k + 1, "text": text, "why": "minor" if minor else "consensus",
                          "sites": votes[k]})
        elif k in base_bad:
            sites = base_sites(script_words, chunks, k, heard_base) if heard_base is not None else []
            if sites:   # none left after normalising (numbers, letters, jargon): not a real flag
                flags.append({"s": k + 1, "text": text, "why": "base-only", "sites": sites})
    return {"v": QA_VERSION, "models": models or ["base", *QA_MODELS], "flags": flags}


# ── the extra voters (MLX) ─────────────────────────────────────────────────────
def windows(x, sr=16000, limit=29.5):
    """Split a line into stretches of at most `limit` s (Whisper's window is 30 s), cutting in
    the middle of the breaths voice.py inserts between sentences (runs of exact silence)."""
    import numpy as np
    n, cap = len(x), int(limit * sr)
    if n <= cap:
        return [(0, n)]
    quiet = np.abs(x) < 1e-4
    edges = np.flatnonzero(np.diff(np.concatenate(([0], quiet.astype(np.int8), [0]))))
    gaps = [(a + b) // 2 for a, b in zip(edges[::2], edges[1::2]) if b - a >= 0.25 * sr]
    out, start = [], 0
    while n - start > cap:
        inside = [g for g in gaps if start < g <= start + cap]
        if inside:
            cut = inside[-1]
        else:                     # one sentence longer than a window: cut at its quietest 20 ms
            lo, f = start + int(0.8 * cap), sr // 50
            seg = np.abs(x[lo:start + cap])
            cut = lo + int(np.argmin(seg[:len(seg) // f * f].reshape(-1, f).mean(axis=1))) * f
        out.append((start, cut))
        start = cut
    return out + [(start, n)]


class _StopAtSpeechEnd:
    """Decoder logit filter: force end-of-text once a timestamp reaches the end of a window's
    speech. Whisper otherwise fills the zero-padded rest of its 30 s window with invented or
    repeated sentences ("Thanks for watching! Bye! Bye!"), on most of our clips."""

    def __init__(self, tok, sample_begin, limits):
        self.tok, self.begin = tok, sample_begin
        self.limits = [tok.timestamp_begin + max(1, round(t / 0.02)) for t in limits]

    def apply(self, logits, tokens):
        import mlx.core as mx
        done = [any(t >= lim for t in row[self.begin:]) for row, lim in zip(tokens.tolist(), self.limits)]
        if not any(done):
            return logits
        # EOT gets a finite logit: the timestamp rules may have masked it along with all text
        forced = mx.where(mx.arange(logits.shape[-1]) == self.tok.eot, 0.0, -mx.inf).astype(logits.dtype)
        return mx.where(mx.array(done)[:, None], forced[None, :], logits)


class _NoLoops:
    """Decoder logit filter: forbid continuing a unit of 1-4 tokens repeated REPEATS times in a
    row. Greedy Whisper can lock into "2, 2, 2, 2, …" (the script said "two, two, two") until its
    token limit; the usual escape, sampling at higher temperatures, wrote gibberish here."""
    REPEATS = 5

    def __init__(self, sample_begin):
        self.begin = sample_begin

    def apply(self, logits, tokens):
        import mlx.core as mx
        ban = []
        for k, row in enumerate(tokens.tolist()):
            seq = row[self.begin:]
            for n in range(1, 5):
                unit = seq[-n:]
                if len(seq) >= n * self.REPEATS and seq[-n * self.REPEATS:] == unit * self.REPEATS:
                    ban.append((k, unit[0]))
                    break
        if not ban:
            return logits
        mask = [[0.0] * logits.shape[-1] for _ in range(logits.shape[0])]
        for k, t in ban:
            mask[k][t] = -float("inf")
        return logits + mx.array(mask, dtype=logits.dtype)


def _speech_words(tokens, tok, limit):
    """Text of a timestamped decode, minus empty (start == end) segments and any segment that
    starts at or after `limit` (the end of the speech)."""
    words, start, text = [], 0.0, []
    for t in list(tokens) + [None]:
        if t is None or t >= tok.timestamp_begin:
            at = None if t is None else (t - tok.timestamp_begin) * 0.02
            if text and start < limit and at != start:
                words += tok.decode(text).split()
            text = []
            if at is not None:
                start = at
        elif t < tok.eot:
            text.append(t)
    return words


class Voters:
    """Whisper small + medium on the GPU (mlx-audio), loaded on first use.

    Each window of speech (<= 29.5 s, cut at breaths) is decoded once, greedily (temperature 0),
    with no prompt, and stopped where its speech ends. mlx-audio's own generate() loop failed
    here three ways: its temperature fallback sampled gibberish on clean speech ("гарparum");
    without timestamps the decoder never stops; and with them it re-decodes the last fraction
    of a second, prompted with the text so far, and invents sentences."""

    def __init__(self, names=None):
        self.names = list(names or QA_MODELS)
        self.models = {}
        self.broken = False      # set by try_hear() when the models can't run
        self.seconds = {name: 0.0 for name in self.names}   # decode time per model (vk voice summary)

    def try_hear(self, audio, sr):
        """hear(), or None (warning once) if the models can't load or run: base-only QA then."""
        if self.broken:
            return None
        try:
            return self.hear(audio, sr)
        except Exception as e:  # noqa: BLE001  (a missing download must not kill a voice run)
            self.broken = True
            print(f"  consensus QA unavailable ({type(e).__name__}: {e}); Whisper base only for the "
                  f"rest of this run", flush=True)
            return None

    def _model(self, name):
        if name not in self.models:
            import warnings
            from mlx_audio.stt import load
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = load(QA_MODELS[name])
            self.models[name] = (model, model.get_tokenizer(language="en", task="transcribe"))
        return self.models[name]

    def hear(self, audio, sr):
        """-> {model: [word strings]} for one line (any sample rate)."""
        import mlx.core as mx
        import numpy as np
        from mlx_audio.stt.models.whisper.audio import N_FRAMES, N_SAMPLES, log_mel_spectrogram, pad_or_trim
        from mlx_audio.stt.models.whisper.decoding import DecodingOptions, DecodingTask
        from scipy.signal import resample_poly
        x = np.asarray(audio if sr == 16000 else resample_poly(audio, 16000, sr), dtype=np.float32)
        spans = windows(x)
        rms = np.sqrt(np.mean(x[:len(x) // 160 * 160].reshape(-1, 160) ** 2, axis=1))  # 10 ms frames
        floor = max(1e-3, 0.01 * float(rms.max(initial=0)))       # 40 dB under the line's peak
        ends = []                       # per window: where its speech ends (s from its start)
        for a, b in spans:
            voiced = np.flatnonzero(rms[a // 160:b // 160] > floor)
            ends.append((voiced[-1] + 1) / 100 if len(voiced) else (b - a) / 16000)
        out = {}
        import time
        for name in self.names:
            model, tok = self._model(name)
            t0 = time.time()
            mels = []
            for (a, b), end in zip(spans, ends):  # as generate() does: content frames, zero-padded
                cut = min(b, a + int((end + 0.25) * 16000))   # drop trailing silence ({pause})
                mel = log_mel_spectrogram(mx.array(x[a:cut]), n_mels=model.dims.n_mels, padding=N_SAMPLES)
                mels.append(pad_or_trim(mel[:mel.shape[-2] - N_FRAMES], N_FRAMES, axis=-2).astype(model.dtype))
            task = DecodingTask(model, DecodingOptions(language="en", task="transcribe", temperature=0.0,
                                                       without_timestamps=False))
            # a segment starting in the last 0.2 s of speech is Whisper inventing more (its end
            # timestamps run up to ~0.15 s early); a real one starts well before that
            limits = [max(0.3, e - 0.2) for e in ends]
            task.logit_filters += [_NoLoops(task.sample_begin), _StopAtSpeechEnd(tok, task.sample_begin, limits)]
            words = []
            for r, limit in zip(task.run(mx.stack(mels)), limits):
                words += _speech_words(r.tokens, tok, limit)
            out[name] = words
            self.seconds[name] += time.time() - t0
        return out


# ── reporting (vk qa, vk status) ───────────────────────────────────────────────
def line_state(entry):
    """'unchecked' (no consensus QA yet), 'flagged' (consensus flags), or 'clean' (none, or only
    base-only / minor ones)."""
    qa = (entry or {}).get("qa")
    if not qa:
        return "unchecked"
    whys = {f["why"] for f in qa.get("flags", [])}
    return "flagged" if "consensus" in whys else "clean"


def _norm_heard(s):
    return " ".join(qa_token(w) for w in s.split())


def _short(text, keep=6):
    w = text.split()
    return text if len(w) <= 2 * keep + 1 else " ".join(w[:keep] + ["…"] + w[-keep:])


def format_flag(cid, flag):
    parts = []
    for site in flag["sites"]:
        groups = {}
        for m in site["by"]:
            groups.setdefault(_norm_heard(site["heard"].get(m, "")), []).append(m)
        heard = " / ".join(f"\"{_short(site['heard'][ms[0]])}\" ({', '.join(ms)})" for ms in groups.values())
        parts.append(f"\"{_short(site['expected'])}\" → {heard}")
    tag = {"base-only": "  [base only]", "minor": "  [minor: function words]"}.get(flag["why"], "")
    return f"{cid}:{flag['s']}  " + (" · ".join(parts) or "(no word-level detail)") + tag


def main():
    import argparse
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from lib.paths import project
    from status import script_lines

    ap = argparse.ArgumentParser(description="List the sentences the consensus voice QA flagged.")
    ap.add_argument("chapter", nargs="?", type=int, help="only this chapter")
    ap.add_argument("-v", "--verbose", action="store_true", help="also print each sentence's text")
    ap.add_argument("--all", action="store_true",
                    help="also list minor flags (function words only) and base-only ones (Whisper base alone)")
    args = ap.parse_args()

    root = project()
    mpath = root / "audio" / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    files = sorted((root / "script").glob(f"ch{args.chapter}_*.md" if args.chapter else "ch*_*.md"))
    if not files:
        sys.exit("no script found")
    n_flag = n_lines = n_base = 0
    unchecked, stale = [], []
    for path in files:
        for cid, raw in script_lines(path).items():
            entry = manifest.get(cid)
            if not entry:
                unchecked.append(cid)
                continue
            if entry.get("raw") != raw:
                stale.append(cid)
            state = line_state(entry)
            if state == "unchecked":
                unchecked.append(cid)
                continue
            shown = [f for f in entry["qa"]["flags"] if f["why"] == "consensus" or args.all]
            n_base += sum(f["why"] != "consensus" for f in entry["qa"]["flags"])
            n_lines += bool([f for f in shown if f["why"] == "consensus"])
            for f in shown:
                n_flag += f["why"] == "consensus"
                print(format_flag(cid, f))
                if args.verbose:
                    print(f"      {f['text']}")
    where = f"chapter {args.chapter}" if args.chapter else "all chapters"
    print(f"{n_flag} sentence(s) flagged by consensus in {n_lines} line(s), {where}"
          + (f"; {n_base} minor/base-only flag(s) hidden (--all)" if n_base and not args.all else ""))
    if unchecked:
        print(f"{len(unchecked)} line(s) without consensus QA: run vk voice"
              f"{f' {args.chapter}' if args.chapter else ''} --qa-only ({', '.join(unchecked[:4])}"
              f"{', …' if len(unchecked) > 4 else ''})")
    if stale:
        print(f"{len(stale)} line(s) changed since voicing (vk voice): {', '.join(stale[:4])}"
              f"{', …' if len(stale) > 4 else ''}")


if __name__ == "__main__":
    main()
