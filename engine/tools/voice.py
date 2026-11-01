"""Generate narration for every [id] line in script/*.md, with word timings.

Run with the MLX venv:
    vk voice [CHAPTER] [--only ID ...] [--force] [--retime] [--qa-only]

Writes audio/<id>.wav and audio/manifest.json:
    {id: {"file", "duration", "marks": {name: s}, "words": [[word, s], ...], "text", ...}}

Pacing: each sentence is voiced on its own and joined with a short breath
(SENTENCE_GAP), which reads far better than the model's run-on delivery. A
`{pause}` / `{pause=1.5}` in the script inserts a longer deliberate hold.

QA: every clip is transcribed with Whisper base, which gives the word timings
scenes cue on and per-sentence error counts (garbled, or a repeated phrase).
Whisper small and medium (MLX, GPU) transcribe it too, and a sentence that at
least two of the three models mishear the same way is flagged as well
(tools/voiceqa.py). A flagged sentence is re-voiced with a new seed (only that
sentence), keeping the best take; what is still flagged after TRIES takes is
stored in manifest[id]["qa"] and listed by `vk qa`. `--qa-only` runs that QA on
the cached clips without re-voicing or touching the timings. Clips are cached by
text + voice settings; editing one line only re-voices that line.
"""
import argparse
import difflib
import fcntl
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import project  # noqa: E402
import voiceqa  # noqa: E402  (tools/, next to this file)
import slots  # noqa: E402

BULK_LINES = 25   # more lines than this to voice = a bulk run, at low CPU priority (2026-11-01)


def yield_to_short_revoices(max_wait=900):
    """A bulk run pauses between sentences while a short re-voice (a director's fix, which a whole
    chapter waits on) holds the other GPU slot, so the fix gets the whole GPU. The bulk run keeps
    its own slot and memory; it waits at most `max_wait` s per sentence (2026-11-01)."""
    t0, said = time.time(), False
    while time.time() - t0 < max_wait:
        short = [lab for pid, lab in slots.holders("gpu")
                 if pid != os.getpid() and lab.startswith("vk voice") and "(bulk)" not in lab]
        if not short:
            return
        if not said:
            print(f"  pausing for a short re-voice: {short[0]}", flush=True)
            said = True
        time.sleep(3)

try:
    ROOT = project()       # the project: script/ in, audio/ out
except SystemExit:         # tools/audition.py runs outside any project
    ROOT = Path.cwd()
SCRIPTS = ROOT / "script"
AUDIO = ROOT / "audio"
MANIFEST = AUDIO / "manifest.json"

VOICE = {
    "model": "mlx-community/chatterbox-turbo-fp16",
    "ref": "assets/voice/refs/ref_c.wav",   # relative to engine/; only its content is in the cache key
    "temperature": 0.8,
    "sentence_gap": 0.55,   # breath between sentences (user-chosen pacing "B")
    "pause": 1.0,           # default length of a {pause}
}
MAX_WER = 0.12      # per sentence, once it has >= 3 errors
MAX_STUTTER = 3     # this many extra words in one place = a repeated/garbled phrase
TRIES = 4
CONSENSUS_RETAKES = 1   # retakes for a sentence only the consensus flags: if a new seed doesn't fix it,
                        # the text needs changing (LESSONS: "fix the text, not the seed")

# where a run's time goes (printed at the end of vk voice)
STATS = {"tts": 0.0, "base": 0.0, "takes": 0, "retakes": 0, "retakes_consensus_only": 0}

LINE_RE = re.compile(r"^\[([\w.]+)\]\s*(.*)$")
TOKEN_RE = re.compile(r"\{(\w+)(?:=([\d.]+))?\}")
SENTENCE_END = re.compile(r"[.!?:]$")
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen \
fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
# Whisper writes spoken numbers as digits; map 0-99 to the (hyphen-free) words the script uses
NUM_WORDS = {str(n): _ONES[n] if n < 20 else _TENS[n // 10] + ("" if n % 10 == 0 else _ONES[n % 10])
             for n in range(100)}


# ── script parsing ────────────────────────────────────────────────────────────
def parse_scripts(chapter=None):
    """Return {id: raw_text} in script order, from script/ch*.md (one chapter or all)."""
    files = sorted(SCRIPTS.glob(f"ch{chapter}_*.md" if chapter else "ch*.md"))
    lines = {}
    for path in files:
        cur = None
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if m := LINE_RE.match(line):
                cur = m.group(1)
                if cur in lines:
                    sys.exit(f"duplicate id [{cur}] in {path.name}")
                lines[cur] = m.group(2)
            elif cur and line and not line.startswith(("#", ">", "---")):
                lines[cur] += " " + line
            else:
                cur = None
    return lines


def split_line(raw):
    """-> (words, marks {name: word index}, chunks [(first, last+1, gap_after)])."""
    words, marks, breaks, held = [], {}, {}, {}
    for tok in re.split(r"(\{\w+(?:=[\d.]+)?\})", raw):
        if m := TOKEN_RE.fullmatch(tok):
            name, val = m.groups()
            if name == "pause":
                held[len(words)] = float(val) if val else VOICE["pause"]
                breaks[len(words)] = max(breaks.get(len(words), 0), held[len(words)])
            else:
                marks[name] = len(words)
        else:
            for w in tok.split():
                words.append(w)
                if SENTENCE_END.search(w):
                    n = len(words)
                    breaks[n] = max(breaks.get(n, 0), VOICE["sentence_gap"])
    chunks, start = [], 0
    for end in sorted(b for b in breaks if 0 < b <= len(words)) + [len(words)]:
        if end > start:
            chunks.append((start, end, breaks.get(end, 0.0)))
            start = end
    if chunks:  # no breath after the last sentence (scenes add a gap), but keep a final {pause}
        chunks[-1] = (*chunks[-1][:2], held.get(len(words), 0.0))
    return words, marks, chunks


# ── alignment / QA ─────────────────────────────────────────────────────────────
# letters spelled phonetically in the script (see LESSONS.md) come back from Whisper as letters
# letter names as scripts spell them -> the letter Whisper writes; one list, kept in voiceqa.py
# (two hand-kept copies drifted: "ee", "eff", "vee"... were missing here, 2026-10-31)
SPELLED = dict(voiceqa.LETTERS)


def norm(word):
    w = re.sub(r"[^a-z0-9]", "", word.lower())
    return SPELLED.get(w, NUM_WORDS.get(w, w))


def align(script_words, heard):
    """Whisper words -> (start time per script word or None, opcodes)."""
    S = [norm(w) for w in script_words]
    Ht = heard_tokens(heard)
    H = [t for t, _ in Ht]
    ops = difflib.SequenceMatcher(None, S, H, autojunk=False).get_opcodes()
    times = [None] * len(S)
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                times[i1 + k] = Ht[j1 + k][1]
    return times, ops


def heard_tokens(heard):
    """Whisper words as normalised tokens with their start times. A letter+number token ("Q0",
    "x12", Whisper's way of writing a subscript) is split the way the script says it ("cue zero"),
    both parts at the word's start, as voiceqa's vote already does (Digital Electronics, 2026-10-28)."""
    out = []
    for w in heard:
        n = norm(w.word)
        m = re.fullmatch(r"([a-z])(\d{1,2})", n)
        if m:
            out += [(SPELLED.get(m.group(1), m.group(1)), w.start), (NUM_WORDS.get(m.group(2), m.group(2)), w.start)]
        else:
            out.append((n, w.start))
    return out


def chunk_scores(ops, chunks):
    """Per chunk: (errors, stutter). An insertion counts against the chunk it follows."""
    scores = [[0, 0] for _ in chunks]

    def owner(i):
        for k, (a, b, _) in enumerate(chunks):
            if a <= i < b:
                return k
        return len(chunks) - 1

    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        k = owner(i1 if i2 > i1 else max(0, i1 - 1))
        scores[k][0] += max(i2 - i1, j2 - j1)
        scores[k][1] = max(scores[k][1], (j2 - j1) - (i2 - i1))
    return scores


def is_bad(errors, stutter, n_words):
    return stutter >= MAX_STUTTER or (errors >= 3 and errors / max(1, n_words) > MAX_WER)


def fill_times(times, duration):
    known = [(k, t) for k, t in enumerate(times) if t is not None]
    if not known:
        return [duration * k / max(1, len(times)) for k in range(len(times))]
    out = []
    for idx, t in enumerate(times):
        if t is None:
            before = next(((k, v) for k, v in reversed(known) if k < idx), None)
            after = next(((k, v) for k, v in known if k > idx), None)
            if before and after:
                t = before[1] + (idx - before[0]) / (after[0] - before[0]) * (after[1] - before[1])
            else:
                t = (after or before)[1]
        out.append(t)
    return out


# ── synthesis ─────────────────────────────────────────────────────────────────
def clip_key(raw_without_marks):
    ref_hash = hashlib.sha1((ENGINE / VOICE["ref"]).read_bytes()).hexdigest()[:10]
    blob = json.dumps({**VOICE, "ref": ref_hash, "text": raw_without_marks}, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def speech_only(raw):
    """The line with marks removed but pauses kept: what the audio depends on."""
    return " ".join(TOKEN_RE.sub(lambda m: m.group(0) if m.group(1) == "pause" else " ", raw).split())


def synth(model, text, seed):
    t0 = time.time()
    mx.random.seed(seed)
    parts = [np.array(r.audio, dtype=np.float32)
             for r in model.generate(text=text, ref_audio=str(ENGINE / VOICE["ref"]),
                                     temperature=VOICE["temperature"])]
    STATS["tts"] += time.time() - t0
    STATS["takes"] += 1
    return np.concatenate(parts)


def assemble(takes, chunks, sr):
    out = []
    for audio, (_, _, gap) in zip(takes, chunks):
        out += [audio, np.zeros(int(gap * sr), dtype=np.float32)]
    return np.concatenate(out)


def transcribe(whisper, audio, sr):
    # hand Whisper 16 kHz samples directly (its file decoder trips over newer PyAV)
    t0 = time.time()
    segs, _ = whisper.transcribe(resample_poly(audio, 16000, sr).astype(np.float32),
                                 language="en", word_timestamps=True)
    words = [w for s in segs for w in s.words]
    STATS["base"] += time.time() - t0
    return words


def voice_line(model, whisper, cid, words, chunks, voters=None):
    """Voice one line -> (audio, sr). tools/audition.py calls this (base-only QA)."""
    return voice_line_qa(model, whisper, voters, cid, words, chunks)[:2]


def voice_line_qa(model, whisper, voters, cid, words, chunks):
    """Voice one line sentence by sentence; re-voice only the sentences that fail QA.

    A sentence fails on Whisper base's own counts (is_bad) or, given `voters` (voiceqa.Voters),
    when base + small + medium agree on a mishearing. Takes are ranked by (fails, consensus
    sites, base errors). -> (audio, sr, the voters' transcripts of exactly that audio or None)."""
    sr = model.sample_rate
    best = [None] * len(chunks)          # (score tuple, audio)
    takes = [None] * len(chunks)
    pending = list(range(len(chunks)))
    heard = {}                           # voters' transcripts per assembly (ids of its takes)
    retakes = [0] * len(chunks)
    for attempt in range(TRIES):
        for k in pending:
            a, b, _ = chunks[k]
            seed = int(hashlib.sha1(f"{cid}:{k}:{attempt}".encode()).hexdigest()[:8], 16)
            takes[k] = synth(model, " ".join(words[a:b]), seed)
        line = assemble(takes, chunks, sr)
        base = transcribe(whisper, line, sr)
        _, ops = align(words, base)
        votes = {}
        said = voters.try_hear(line, sr) if voters else None
        if said is not None:
            heard[tuple(map(id, takes))] = said
            votes = voiceqa.serious(voiceqa.consensus(words, chunks, {"base": [w.word for w in base], **said}))
        for k, (err, stut) in enumerate(chunk_scores(ops, chunks)):
            agreed = len(votes.get(k, ()))
            base_bad = is_bad(err, stut, chunks[k][1] - chunks[k][0])
            score = (base_bad or agreed > 0, agreed, err + 2 * stut)
            if best[k] is None or score < best[k][0]:
                best[k] = (score, takes[k], base_bad)
        # base's own failures keep the full budget; a consensus-only flag gets CONSENSUS_RETAKES
        pending = [k for k in range(len(chunks)) if best[k][0][0]
                   and (best[k][2] or retakes[k] < CONSENSUS_RETAKES)]
        if not pending:
            break
        if attempt + 1 < TRIES:
            STATS["retakes"] += len(pending)
            STATS["retakes_consensus_only"] += sum(not best[k][2] for k in pending)
            for k in pending:
                retakes[k] += 1
            print(f"  {cid}: re-voicing sentence(s) {[k + 1 for k in pending]}", flush=True)
        takes = [b[1] for b in best]
    final = [b[1] for b in best]
    return assemble(final, chunks, sr), sr, heard.get(tuple(map(id, final)))


def line_qa(words, chunks, base, heard):
    """The manifest's "qa" record for one line: base's Whisper words (with timings) plus the
    voters' transcripts {model: [words]}; None when the voters couldn't run."""
    if heard is None:
        return None
    _, ops = align(words, base)
    base_bad = {k for k, (e, st) in enumerate(chunk_scores(ops, chunks))
                if is_bad(e, st, chunks[k][1] - chunks[k][0])}
    base_words = [w.word for w in base]
    votes = voiceqa.consensus(words, chunks, {"base": base_words, **heard})
    return voiceqa.record(words, chunks, votes, base_bad, base_words)


def print_flags(cid, flags):
    for f in flags:
        print(f"       ! {voiceqa.format_flag(cid, f)}", flush=True)


# ── manifest (shared by concurrent voice runs) ─────────────────────────────────
def update_manifest(changes=None, prune_to=None, merge=None):
    """Merge `changes` {id: entry} into audio/manifest.json under a file lock.
    `merge` {id: (key, fields)} adds fields to an existing entry, only while its cache key is
    still `key` (the QA of a clip another run has since re-voiced would be wrong).

    Re-reads the file inside the lock, so two voice runs (e.g. different chapters) never
    overwrite each other's entries. Writing a whole in-memory copy did exactly that once,
    leaving new audio with stale timings (LESSONS.md)."""
    AUDIO.mkdir(exist_ok=True)
    with open(AUDIO / ".manifest.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        current = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
        current.update(changes or {})
        for cid, (key, fields) in (merge or {}).items():
            if current.get(cid, {}).get("key") == key:
                current[cid].update(fields)
        if prune_to is not None:
            current = {k: v for k, v in current.items() if k in prune_to}
        order = {k: i for i, k in enumerate(parse_scripts())}
        tmp = MANIFEST.with_suffix(".tmp")
        tmp.write_text(json.dumps(dict(sorted(current.items(),
                                              key=lambda kv: order.get(kv[0], len(order)))), indent=1))
        os.replace(tmp, MANIFEST)
        return current


# ── main ──────────────────────────────────────────────────────────────────────
def qa_only(script, manifest, only):
    """Consensus QA on cached clips: adds manifest[id]["qa"], never touches audio or timings."""
    from faster_whisper import WhisperModel
    _gpu = slots.gpu(f"vk voice --qa-only {ROOT.name}", gb=4.0)  # noqa: F841  (no Chatterbox: ~2.8 GB less)
    whisper = WhisperModel("base", device="cpu", compute_type="int8")
    voters = voiceqa.Voters()
    t0, n_lines, n_flagged, skipped = time.time(), 0, 0, []
    todo = [c for c in script if only is None or c in only]
    for n, cid in enumerate(todo, 1):
        raw = script[cid]
        key = clip_key(speech_only(raw))
        wav_path = AUDIO / f"{cid}.wav"
        if manifest.get(cid, {}).get("key") != key or not wav_path.exists():
            skipped.append(cid)          # not voiced yet, or the text changed: vk voice first
            continue
        words, _, chunks = split_line(raw)
        audio, sr = sf.read(wav_path, dtype="float32")
        qa = line_qa(words, chunks, transcribe(whisper, audio, sr), voters.try_hear(audio, sr))
        if qa is None:
            sys.exit("consensus QA needs the MLX Whisper models (see the message above)")
        update_manifest(merge={cid: (key, {"qa": qa})})
        n_lines += 1
        consensus = [f for f in qa["flags"] if f["why"] == "consensus"]
        n_flagged += bool(consensus)
        print(f"[{n}/{len(todo)}] {cid:<14} {len(audio) / sr:5.1f}s"
              + (f"  <-- {len(consensus)} sentence(s) flagged" if consensus else ""), flush=True)
        print_flags(cid, consensus)
    print(f"QA: {n_lines} lines checked in {time.time() - t0:.0f} s, {n_flagged} flagged (vk qa)")
    if skipped:
        print(f"skipped {len(skipped)} line(s) that need voicing first: {', '.join(skipped[:6])}"
              f"{', …' if len(skipped) > 6 else ''}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, help="only this chapter's script")
    ap.add_argument("--only", nargs="*", help="ids to (re)generate")
    ap.add_argument("--force", action="store_true", help="ignore the cache")
    ap.add_argument("--retime", action="store_true",
                    help="re-run the Whisper timing/QA pass on cached clips, without re-voicing")
    ap.add_argument("--qa-only", action="store_true",
                    help="run the consensus QA (Whisper base + small + medium) on cached clips: "
                         "no re-voicing, timings untouched")
    args = ap.parse_args()

    AUDIO.mkdir(exist_ok=True)
    script = parse_scripts(args.chapter)
    if not script:
        sys.exit("no script lines found")
    if args.qa_only:
        return qa_only(script, update_manifest(), args.only)
    # drop deleted lines (only on a full run, which sees every chapter's script)
    manifest = update_manifest(prune_to=set(parse_scripts()) if args.chapter is None else None)

    todo = []
    for cid, raw in script.items():
        if args.only is not None and cid not in args.only:
            continue
        cached = manifest.get(cid, {})
        fresh = cached.get("key") == clip_key(speech_only(raw)) and (AUDIO / f"{cid}.wav").exists()
        if args.force or not fresh or args.retime or cached.get("raw") != raw:
            todo.append(cid)
    unchecked = [c for c in script if c not in todo and voiceqa.line_state(manifest.get(c)) == "unchecked"]
    if not todo:
        print("narration up to date")
        if unchecked:
            print(f"{len(unchecked)} line(s) have no consensus QA yet: vk voice --qa-only")
        return

    from faster_whisper import WhisperModel
    from mlx_audio.tts.utils import load_model

    bulk = len(todo) > BULK_LINES
    _gpu = slots.gpu(f"vk voice {ROOT.name}" + (" (bulk)" if bulk else ""))  # noqa: F841  held until this run exits
    if bulk:   # a bulk run nobody waits on: builders' previews get the CPU first
        os.nice(10)
    t0 = time.time()
    whisper = WhisperModel("base", device="cpu", compute_type="int8")
    voters = voiceqa.Voters()
    model = None
    for n, cid in enumerate(todo, 1):
        if bulk:
            yield_to_short_revoices()
        t_line = time.time()
        raw = script[cid]
        words, marks, chunks = split_line(raw)
        key = clip_key(speech_only(raw))
        wav_path = AUDIO / f"{cid}.wav"
        reuse = not args.force and manifest.get(cid, {}).get("key") == key and wav_path.exists()
        voter_heard = None
        if reuse:   # only marks moved, or --retime: keep the audio, redo the timings
            audio, sr = sf.read(wav_path, dtype="float32")
        else:
            model = model or load_model(VOICE["model"])
            audio, sr, voter_heard = voice_line_qa(model, whisper, voters, cid, words, chunks)
            sf.write(wav_path, audio, sr)

        heard = transcribe(whisper, audio, sr)
        times, ops = align(words, heard)
        duration = len(audio) / sr
        filled = fill_times(times, duration)
        errors = sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in ops if t != "equal")
        stutter = max([(j2 - j1) - (i2 - i1) for t, i1, i2, j1, j2 in ops if t != "equal"] + [0])
        old_qa = manifest.get(cid, {}).get("qa")
        if reuse and old_qa and old_qa.get("v") == voiceqa.QA_VERSION:
            qa = old_qa      # same audio, same words: the consensus can't have changed
        else:
            qa = line_qa(words, chunks, heard, voter_heard or voters.try_hear(audio, sr))
        if qa is not None:
            unresolved = len(voiceqa.reported(qa))
        else:            # voters unavailable: Whisper base's own counts, as before
            unresolved = sum(is_bad(e, st, b - a) for (e, st), (a, b, _) in
                             zip(chunk_scores(ops, chunks), chunks))
        manifest[cid] = {
            "file": f"audio/{cid}.wav",
            "duration": round(duration, 3),
            # marks land a hair before their word
            "marks": {m: round(max(0.0, (filled[i] if i < len(filled) else duration) - 0.05), 3)
                      for m, i in marks.items()},
            "words": [[w, round(t, 3)] for w, t in zip(words, filled)],
            "text": " ".join(words),
            "raw": raw,
            "key": key,
            "wer": round(errors / max(1, len(words)), 3),
            "stutter": stutter,
            **({"qa": qa} if qa is not None else {}),
        }
        flag = f"  <-- {unresolved} sentence(s) still flagged, listen to this one" if unresolved else ""
        print(f"[{n}/{len(todo)}] {cid:<14} {duration:5.1f}s  {len(words) / duration * 60:3.0f} wpm"
              f"  WER {errors / max(1, len(words)):4.0%}  ({time.time() - t_line:.0f} s){flag}", flush=True)
        print_flags(cid, voiceqa.reported(qa))
        update_manifest({cid: manifest[cid]})
        getattr(mx, "clear_cache", lambda: None)()   # keep MLX's buffer cache from growing over a long run

    mine = [manifest[k]["duration"] for k in script if k in manifest]
    print(f"narration: {sum(mine) / 60:.1f} min over {len(mine)} lines ({len(todo)} processed in "
          f"{time.time() - t0:.0f} s); flagged sentences are listed by vk qa")
    print(f"time: TTS {STATS['tts']:.0f} s ({STATS['takes']} sentence takes, {STATS['retakes']} of them "
          f"retakes, {STATS['retakes_consensus_only']} for consensus alone), Whisper base {STATS['base']:.0f} s, "
          + ", ".join(f"{m} {s:.0f} s" for m, s in voters.seconds.items())
          + f"; MLX peak memory {getattr(mx, 'get_peak_memory', lambda: 0)() / 2 ** 30:.1f} GB")
    if unchecked:
        print(f"{len(unchecked)} other line(s) have no consensus QA yet: vk voice --qa-only")


if __name__ == "__main__":
    sys.exit(main())
