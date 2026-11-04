"""The load gate (DEEP_STYLE §13, §0): how fast new material arrives, and how much explanation
each idea gets, from an independent coding of the script.

    vk load N… [--wpm W] [--timing auto|video|voice|script] [--codes FILE…] [--out DIR] [--rail]
    vk load N --list          the chapter's lines, sentence by sentence (s1, s2, …): what a coder keys on
    vk load N --check         validate script/chN_load.json against the script, without the numbers

Input: script/chN_load.json, the load-auditor's coding of chapter N (format and rubric:
docs/load-rubric.md): per narration line (clip), its holds (new formulas and new terms) and
questions to the viewer, each with `s`, its sentence number within the line, plus counts of ideas
and motive sentences. `--codes` reads other codings instead; several are averaged (two coders).

Timing, best first (`auto`):
  video   every scene rendered with the current narration (media/cues/): the finished video's
          clip starts, as the calibration measured them (docs/load-calibration.md)
  voice   every line voiced (audio/manifest.json): each line's length and its gap after, plus
          SCENE_EXTRA s per scene for the visuals around the narration
  script  before voicing: the voice's speech rate (SPEECH_WPM), the project's own pacing
          (regap.pacing(): sentence gaps, {pause}s and the gap after each line, scaled as `vk voice`
          will scale them), plus SCENE_EXTRA per scene. With --wpm W instead: words at W per minute
          of finished video plus {pause}s × the pacing scale (§13's rule of thumb, 130 at house pacing)
A line not voiced yet (or changed since) is timed from the script even when the others are voiced.

Checks, per chapter (thresholds below, from DEEP_STYLE §13 and §0):
  load       mean H (holds/min) ≤ 1.9 and H − Q ≤ 1.4 (targets 1.3–1.8 and 0.7–1.2); at most 8 holds
             in any 2-minute window (holds sharing a `pattern` count once there)
  questions  ≥ 1 question in every 2-minute window: listed as advice, not a fail (QUESTION_GAPS_BLOCK)
  substance  ≥ 45 words per idea and ≥ 0.25 motive sentences per idea: below either is "thin explanation"
Writes media/review/chN_load.md (verdict, numbers, every flagged window with its clips and holds,
the per-line table, and the holds in order as rail candidates, §15) and prints one line per
chapter. Exit 1 if any chapter is "over", 2 if a coding is missing or doesn't match the script.
"""
import argparse
import json
import os
import re
import statistics as st
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice  # noqa: E402  (parse_scripts, split_line, clip_key, speech_only, VOICE, ROOT, MANIFEST)
import regap  # noqa: E402  (pacing, sentence_gap, line_gap, DEFAULT_GAP)

ROOT = voice.ROOT

# ── thresholds (DEEP_STYLE §13 and §0; measured in docs/load-calibration.md, 2026-11-04) ─────────
H_BAND, H_MAX = (1.3, 1.8), 1.9          # holds per minute, chapter mean
HQ_BAND, HQ_MAX = (0.7, 1.2), 1.4        # holds minus questions per minute
H_FLOOR = 1.2                            # unmeasured floor: don't pad below it (advice)
PEAK_MAX = 9                             # holds in any 2-minute window (hard; 8 is the target: DE ch2, rated comfortable, sits at 8, and the pre-voice estimate is ±0.5)
PEAK_TARGET = 8                          # advice above this
Q_PER_WINDOW = 1                         # questions in every 2-minute window
QUESTION_GAPS_BLOCK = False              # the 4 comfortable calibration chapters all have gaps (2.4–5.3 min)
WPI_MIN = 32                             # words per idea, chapter mean (§0). Producer, 2026-11-04: Sonnet codes ~1.3x the ideas
                                         # the 3b1b study did, so 3b1b's 58 reads ~45 here and the loved pilot ~18-26; 32 asks
                                         # for ~+30% explanation over the pilot. Provisional: recalibrate on the first auto lecture
MPI_MIN = 0.20                           # motive sentences per idea, chapter mean (§0): 3b1b's 0.25 at Sonnet's idea count (~0.19)
WIN, STEP = 120.0, 5.0                   # sliding windows, as calibrated

# ── timing model before voicing (measured on the 9 calibration chapters, 2026-11-04) ─────────────
SPEECH_WPM = 190      # the voice's words per minute of pure speech (182–201 per chapter)
SCENE_EXTRA = 3.7     # s per scene of visuals around the narration (video − lines − gaps: 2.9–4.9)

SENT_END = re.compile(r"[.?!][\"'”’)\]]*$")      # a sentence, as the calibration's transcripts split them
WORD = re.compile(r"[A-Za-z0-9']+")              # words, as the 3b1b study counted them
SCENE_RE = re.compile(r"^## Scene \d+ · (.+?) \((ch\d+_s\d+_\w+)\)\s*$")
RES = ("1440p60", "1080p60", "480p15")


class _Mean:
    """regap's random gaps at their expected value (a triangular draw's mean)."""
    @staticmethod
    def triangular(low, high, mode):
        return (low + high + mode) / 3


def fmt(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def sentences(timed):
    """[(word, t)] -> [(t of its first word, text)], split at . ? ! (not at colons)."""
    out, cur, t0 = [], [], None
    for w, t in timed:
        t0 = t if t0 is None else t0
        cur.append(w)
        if SENT_END.search(w):
            out.append((t0, " ".join(cur)))
            cur, t0 = [], None
    if cur:
        out.append((t0, " ".join(cur)))
    return out


# ── the chapter: lines, scenes, timing ─────────────────────────────────────────────────────────────
def chapter_lines(n):
    """-> ([(id, raw, scene stem)] in script order, script files)."""
    files = sorted((ROOT / "script").glob(f"ch{n}_*.md"))
    if not files:
        raise SystemExit(f"vk load: no script/ch{n}_*.md")
    raws = voice.parse_scripts(n)
    scene_of, cur = {}, None
    for path in files:
        for line in path.read_text().splitlines():
            if m := SCENE_RE.match(line.strip()):
                cur = m.group(2)
            elif m := voice.LINE_RE.match(line.strip()):
                scene_of[m.group(1)] = cur
    return [(cid, raw, scene_of.get(cid) or f"ch{n}") for cid, raw in raws.items()], files


def script_clip(raw, pace, wpm=None):
    """A line not voiced yet -> (length incl. the gap after it, [(word, t)])."""
    words, _, chunks = voice.split_line(raw)
    sent = voice.VOICE["sentence_gap"]
    scale = pace["scale"] if pace else 1.0
    vary = bool(pace and pace.get("vary", True))
    speed = pace.get("speed", 1.0) if pace else 1.0
    per = 60.0 / wpm if wpm else 60.0 / SPEECH_WPM / speed
    timed, t = [], 0.0
    for a, b, g in chunks:
        for j in range(a, b):
            timed.append((words[j], round(t, 3)))
            t += per
        pause = g > 0 and abs(g - sent) > 1e-6          # regap: a gap that isn't the breath is a {pause}
        if pause:
            t += scale * g if pace else g
        elif g > 0 and not wpm:                          # with --wpm, breaths are inside W
            t += scale * regap.sentence_gap(_Mean, b - a, words[b - 1]) if vary else scale * g
    if not wpm:
        text = " ".join(words)
        t += (scale * regap.line_gap(_Mean, text) if vary else scale * regap.DEFAULT_GAP) if pace \
            else regap.DEFAULT_GAP
    return t, timed


def timeline(n, lines, mode, wpm):
    """-> (clips [{id, scene, t0, dur, sents: [(t, text)], words}], total s, timing note)."""
    manifest = json.loads(voice.MANIFEST.read_text()) if voice.MANIFEST.exists() else {}
    pace = regap.pacing()
    current = {cid: (e := manifest.get(cid)) is not None and e.get("key") == voice.clip_key(voice.speech_only(raw))
               for cid, raw, _ in lines}
    stems = list(dict.fromkeys(sc for _, _, sc in lines))
    cues = None
    if mode in ("auto", "video") and all(current.values()):
        for res in RES:
            files = [ROOT / "media" / "cues" / f"{s}_{res}.json" for s in stems]
            if all(f.exists() for f in files):
                data = [json.loads(f.read_text()) for f in files]
                if [c["id"] for d in data for c in d["clips"]] == [cid for cid, _, _ in lines]:
                    cues = (res, dict(zip(stems, data)))
                    break
    if mode == "video" and cues is None:
        raise SystemExit(f"vk load {n}: --timing video needs every scene rendered with the current narration")
    if mode == "voice" and not all(current.values()):
        raise SystemExit(f"vk load {n}: --timing voice needs every line voiced (vk voice {n})")
    use_voice = mode in ("auto", "voice", "video")

    clips, t, n_voiced = [], 0.0, 0
    if cues:
        res, data = cues
        start = {}
        for s in stems:
            for c in data[s]["clips"]:
                start[c["id"]] = t + c["start"]
            t += data[s]["duration"]
    prev_scene = None
    for i, (cid, raw, sc) in enumerate(lines):
        if not cues and prev_scene is not None and sc != prev_scene:
            t += SCENE_EXTRA
        prev_scene = sc
        if use_voice and current[cid]:
            e = manifest[cid]
            dur, timed = e["duration"] + e.get("gap_after", regap.DEFAULT_GAP), [(w, s) for w, s in e["words"]]
            n_voiced += 1
        else:
            dur, timed = script_clip(raw, pace, wpm)
        t0 = start[cid] if cues else t
        words = [w for w, _ in timed]
        clips.append(dict(id=cid, scene=sc, t0=t0, dur=dur,
                          sents=[(t0 + s, txt) for s, txt in sentences(timed)],
                          words=len(WORD.findall(" ".join(words)))))
        if not cues:
            t += dur
    if not cues and lines:
        t += SCENE_EXTRA
    scale = f"pacing scale {pace['scale']:g}" if pace else "fixed pacing"
    if cues:
        note = f"video ({cues[0]} cues)"
    elif n_voiced == len(lines):
        note = f"voice (manifest, + {SCENE_EXTRA:g} s per scene)"
    else:
        how = f"{wpm:g} wpm of video + {{pause}}s × {pace['scale'] if pace else 1:g}" if wpm else \
            f"{SPEECH_WPM} wpm speech, {scale}, + {SCENE_EXTRA:g} s per scene"
        note = f"script ({how})" + (f"; {n_voiced}/{len(lines)} lines from the manifest" if n_voiced else "")
    return clips, t, note


# ── codings ────────────────────────────────────────────────────────────────────────────────────────
def read_coding(path, clips):
    """-> per-coder rows: holds, questions [(t, clip, s, item)], ideas/motive per clip, warnings."""
    d = json.loads(Path(path).read_text())
    entries = d["clips"] if isinstance(d.get("clips"), list) else [dict(id=k, **v) for k, v in d["clips"].items()]
    by = {e["id"]: e for e in entries}
    ids = [c["id"] for c in clips]
    missing, extra = [i for i in ids if i not in by], [i for i in by if i not in ids]
    if missing or extra:
        raise ValueError(f"{path}: the coding doesn't match the script"
                         + (f"; missing {', '.join(missing)}" if missing else "")
                         + (f"; not in the script {', '.join(extra)}" if extra else "") + " (re-audit)")
    warn, holds, qs, ideas, motive = [], [], [], {}, {}

    def at(c, item, what):
        s = item.get("s")
        if not isinstance(s, int) or not 1 <= s <= len(c["sents"]):
            warn.append(f"{c['id']}: {what} {item.get('text', '')[:40]!r} has s={s!r} "
                        f"(1–{len(c['sents'])}); placed at the line's start")
            return c["t0"]
        return c["sents"][s - 1][0]

    for c in clips:
        e = by[c["id"]]
        for h in e.get("holds", []):
            if h.get("kind") not in ("F", "D"):
                warn.append(f"{c['id']}: hold {h.get('text', '')[:40]!r} has kind {h.get('kind')!r} (F or D)")
            holds.append((at(c, h, "hold"), c["id"], h))
        for q in e.get("questions", []):
            qs.append((at(c, q, "question"), c["id"], q))
        ideas[c["id"]] = float(e.get("ideas", 0))
        motive[c["id"]] = float(e.get("motive", 0))
        if ideas[c["id"]] < len(e.get("holds", [])):
            warn.append(f"{c['id']}: {ideas[c['id']]:g} ideas but {len(e['holds'])} holds (holds are ideas)")
    return dict(meta={k: v for k, v in d.items() if k != "clips"}, holds=holds, qs=qs,
                ideas=ideas, motive=motive, warn=warn)


def window_count(holds, a):
    """Holds in [a, a + WIN); holds sharing a pattern count once."""
    inside = [h for t, _, h in holds if a <= t < a + WIN]
    return sum(1 for h in inside if not h.get("pattern")) + len({h["pattern"] for h in inside if h.get("pattern")})


def stretches(flags, starts):
    """Flagged window starts -> [(first start, last start)], merging flagged windows that start
    within half a window of each other (one burst, not a flicker around the limit)."""
    out = []
    for a, f in zip(starts, flags):
        if f and out and a - out[-1][1] <= WIN / 2 + 1e-6:
            out[-1][1] = a
        elif f:
            out.append([a, a])
    return out


# ── one chapter ────────────────────────────────────────────────────────────────────────────────────
def analyse(n, codes, mode, wpm):
    lines, files = chapter_lines(n)
    clips, T, timing = timeline(n, lines, mode, wpm)
    coders = [read_coding(p, clips) for p in codes]
    mins = T / 60
    words = sum(c["words"] for c in clips)
    mean = lambda f: st.mean(f(k) for k in coders)
    holds = mean(lambda k: len(k["holds"]))
    qs = mean(lambda k: len(k["qs"]))
    ideas = mean(lambda k: sum(k["ideas"].values()))
    motive = mean(lambda k: sum(k["motive"].values()))
    starts = [i * STEP for i in range(int(max(0.0, T - WIN) / STEP) + 1)]
    win_h = [mean(lambda k: window_count(k["holds"], a)) for a in starts]
    win_q = [mean(lambda k: sum(1 for t, _, _ in k["qs"] if a <= t < a + WIN)) for a in starts]
    pk = max(range(len(starts)), key=lambda i: win_h[i])
    r = dict(n=n, T=T, mins=mins, timing=timing, words=words, holds=holds, qs=qs, ideas=ideas, motive=motive,
             H=holds / mins, Q=qs / mins, HQ=(holds - qs) / mins, peak=win_h[pk], peak_at=starts[pk],
             wpi=words / ideas if ideas else float("inf"), mpi=motive / ideas if ideas else 0.0,
             clips=clips, coders=coders, codes=codes, files=files, starts=starts, win_h=win_h, win_q=win_q)
    r["over_peak"] = stretches([h > PEAK_MAX + 1e-9 for h in win_h], starts)
    r["no_q"] = stretches([q < Q_PER_WINDOW - 0.5 for q in win_q], starts)
    load, subst, advice = [], [], []
    if r["H"] > H_MAX:
        load.append(f"H {r['H']:.2f}/min > {H_MAX}")
    if r["HQ"] > HQ_MAX:
        load.append(f"H − Q {r['HQ']:.2f}/min > {HQ_MAX}")
    if r["over_peak"]:
        load.append(f"{len(r['over_peak'])} stretch(es) over {PEAK_MAX} holds in 2 min (peak {r['peak']:g})")
    if r["wpi"] < WPI_MIN:
        subst.append(f"{r['wpi']:.0f} words per idea < {WPI_MIN}")
    if r["mpi"] < MPI_MIN:
        subst.append(f"{r['mpi']:.2f} motive sentences per idea < {MPI_MIN}")
    if not H_BAND[0] <= r["H"] <= H_BAND[1] and r["H"] <= H_MAX:
        advice.append(f"H {r['H']:.2f} outside the target {H_BAND[0]}–{H_BAND[1]}"
                      + (f" (below the {H_FLOOR} floor: don't pad, but check the chapter isn't thin)" if r["H"] < H_FLOOR else ""))
    if not HQ_BAND[0] <= r["HQ"] <= HQ_BAND[1] and r["HQ"] <= HQ_MAX:
        advice.append(f"H − Q {r['HQ']:.2f} outside the target {HQ_BAND[0]}–{HQ_BAND[1]}")
    if r["no_q"]:
        gaps = f"{len(r['no_q'])} stretch(es) with no question in 2 min"
        (load if QUESTION_GAPS_BLOCK else advice).append(gaps)
    stale = [p for p in codes if any(f.stat().st_mtime > Path(p).stat().st_mtime for f in files)]
    if stale:
        advice.append("the script changed after the coding: re-audit before trusting these numbers")
    if PEAK_TARGET < r['peak'] <= PEAK_MAX:
        advice.append(f"densest 2 min holds {r['peak']:g}, above the target {PEAK_TARGET}: spread them if you can")
    r.update(load=load, subst=subst, advice=advice,
             verdict="over" if load or subst else "pass")
    return r


# ── report ─────────────────────────────────────────────────────────────────────────────────────────
def short(text, n=70):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1] + "…"


def clips_between(r, a, b):
    return [c["id"] for c in r["clips"] if c["t0"] < b and c["t0"] + c["dur"] > a]


def report(r):
    n, k0 = r["n"], r["coders"][0]
    rel = lambda p: str(Path(p).resolve().relative_to(ROOT)) if Path(p).resolve().is_relative_to(ROOT) else str(p)
    who = k0["meta"].get("coder", "?")
    L = [f"# Chapter {n} load: {r['verdict']}", "",
         f"{', '.join(f.name for f in r['files'])} · coding {', '.join(rel(p) for p in r['codes'])} ({who}"
         + (f", mean of {len(r['coders'])}" if len(r["coders"]) > 1 else "") + f") · timing {r['timing']} · "
         f"{r['mins']:.1f} min, {r['words']} words · {time.strftime('%Y-%m-%d %H:%M')}", ""]
    if r["verdict"] == "over":
        if r["load"]:
            L.append("**Over on load** (too much to hold, too fast): " + "; ".join(r["load"]) + ".")
        if r["subst"]:
            L.append("**Thin explanation** (too few words and motives per idea): " + "; ".join(r["subst"]) + ".")
        L.append("")
    ok = lambda bad: "OVER" if bad else "ok"
    L += ["## Load (DEEP_STYLE §13)", "",
          "| measure | value | target | limit | |", "|---|---|---|---|---|",
          f"| holds H per min | {r['H']:.2f} ({r['holds']:g} holds) | {H_BAND[0]}–{H_BAND[1]} | ≤ {H_MAX} | {ok(r['H'] > H_MAX)} |",
          f"| H − Q per min | {r['HQ']:.2f} | {HQ_BAND[0]}–{HQ_BAND[1]} | ≤ {HQ_MAX} | {ok(r['HQ'] > HQ_MAX)} |",
          f"| densest 2 min | {r['peak']:g} holds at {fmt(r['peak_at'])}–{fmt(r['peak_at'] + WIN)} | | ≤ {PEAK_MAX} | {ok(bool(r['over_peak']))} |",
          f"| questions Q per min | {r['Q']:.2f} ({r['qs']:g}) | ≥ 1 in every 2 min | | "
          + (f"{len(r['no_q'])} gap(s)" if r["no_q"] else "ok") + " |", ""]
    if r["over_peak"]:
        L += [f"### Stretches over {PEAK_MAX} holds in 2 minutes", ""]
        for a, b in r["over_peak"]:
            i = max((j for j, s in enumerate(r["starts"]) if a <= s <= b), key=lambda j: r["win_h"][j])
            s0 = r["starts"][i]
            L.append(f"- **{fmt(a)}–{fmt(b + WIN)}**, densest {fmt(s0)}–{fmt(s0 + WIN)} with {r['win_h'][i]:g} holds; "
                     f"lines {', '.join(clips_between(r, s0, s0 + WIN))}:")
            for t, cid, h in sorted(k0["holds"], key=lambda x: x[0]):
                if s0 <= t < s0 + WIN:
                    L.append(f"  - {fmt(t)} {cid} s{h.get('s')} {h.get('kind')} {short(h.get('text', ''))}"
                             + (f" (pattern {h['pattern']})" if h.get("pattern") else ""))
        L.append("")
    if r["no_q"]:
        L += ["### Stretches with no question for 2 minutes" + ("" if QUESTION_GAPS_BLOCK else " (advice)"), ""]
        for a, b in r["no_q"]:
            L.append(f"- {fmt(a)}–{fmt(b + WIN)} ({(b + WIN - a) / 60:.1f} min): lines {', '.join(clips_between(r, a, b + WIN))}")
        L.append("")
    if r["load"] or r["no_q"]:
        L += ["Fix load in this order (docs/load-calibration.md §4): turn a step into a question (predict, then "
              "show); swap a new symbol for a recall or a picture the viewer already has; move routine lines to "
              "the reference tier; split the scene. Never fix it by adding silence.", ""]
    L += ["## Explanation per idea (DEEP_STYLE §0)", "",
          "| measure | value | limit | |", "|---|---|---|---|",
          f"| words per idea | {r['wpi']:.0f} ({r['words']} words, {r['ideas']:g} ideas) | ≥ {WPI_MIN} | {'THIN' if r['wpi'] < WPI_MIN else 'ok'} |",
          f"| motive sentences per idea | {r['mpi']:.2f} ({r['motive']:g}) | ≥ {MPI_MIN} | {'THIN' if r['mpi'] < MPI_MIN else 'ok'} |", ""]
    if r["subst"]:
        L += ["Fix thin explanation by giving each hold its motive before it, a read-back in plain words or the "
              "picture's language, and a restatement when it's used again (DEEP_STYLE §0), never padding; or "
              "justify the chapter's numbers in the script report.", ""]
    if r["advice"]:
        L += ["## Advice", ""] + [f"- {a}" for a in r["advice"]] + [""]
    warns = [w for k in r["coders"] for w in k["warn"]]
    if warns:
        L += ["## Coding warnings", ""] + [f"- {w}" for w in warns] + [""]
    per = lambda f, cid: st.mean(f(k, cid) for k in r["coders"])
    L += ["## Per line", "", "| line | at | words | holds | Q | ideas | motive |", "|---|---|---|---|---|---|---|"]
    for c in r["clips"]:
        cid = c["id"]
        h = per(lambda k, i: sum(1 for _, x, _ in k["holds"] if x == i), cid)
        q = per(lambda k, i: sum(1 for _, x, _ in k["qs"] if x == i), cid)
        L.append(f"| {cid} | {fmt(c['t0'])} | {c['words']} | {h:g} | {q:g} | {per(lambda k, i: k['ideas'][i], cid):g} "
                 f"| {per(lambda k, i: k['motive'][i], cid):g} |")
    L += ["", "## Rail candidates (DEEP_STYLE §15): the holds in order", ""] + rail(r) + [""]
    return "\n".join(L)


def rail(r):
    out = []
    for t, cid, h in sorted(r["coders"][0]["holds"], key=lambda x: x[0]):
        until = f" → until {h['until']}" if h.get("until") else ""
        pat = f" (pattern {h['pattern']})" if h.get("pattern") else ""
        out.append(f"- {fmt(t)} {cid} {h.get('kind')} {short(h.get('text', ''), 90)}{pat}{until}")
    return out or ["- (no holds)"]


def summary(r):
    why = (["load: " + "; ".join(r["load"])] if r["load"] else []) + \
          (["thin explanation: " + "; ".join(r["subst"])] if r["subst"] else [])
    return (f"ch{r['n']} {r['verdict'].upper()}" + (f" ({' | '.join(why)})" if why else "") +
            f"\n     H {r['H']:.2f} · H−Q {r['HQ']:.2f} · peak {r['peak']:g}/2 min · Q {r['Q']:.2f}/min"
            + (f" ({len(r['no_q'])} gap(s) > 2 min)" if r["no_q"] else "") +
            f" · {r['wpi']:.0f} words/idea · {r['mpi']:.2f} motive/idea · {r['mins']:.1f} min, {r['timing']}")


def list_lines(n):
    lines, _ = chapter_lines(n)
    sc = None
    for cid, raw, scene in lines:
        if scene != sc:
            print(f"\n## {scene}")
            sc = scene
        words, _, _ = voice.split_line(raw)
        print(f"[{cid}]")
        for i, (_, s) in enumerate(sentences([(w, 0) for w in words]), 1):
            print(f"  s{i} {s}")
    print(f"\n{len(lines)} lines")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapters", type=int, nargs="+")
    ap.add_argument("--wpm", type=float, default=None,
                    help="before voicing, time words at W per minute of finished video (+ {pause}s × the pacing "
                         "scale) instead of the speech-rate model; DEEP_STYLE §13 says 130 at house pacing")
    ap.add_argument("--timing", choices=("auto", "video", "voice", "script"), default="auto")
    ap.add_argument("--codes", nargs="+", help="coding file(s) instead of script/chN_load.json; several are averaged")
    ap.add_argument("--out", type=Path, help="folder for chN_load.md (default media/review/)")
    ap.add_argument("--list", action="store_true", help="print the chapter's lines sentence by sentence and stop")
    ap.add_argument("--rail", action="store_true", help="also print the holds in order (rail candidates)")
    ap.add_argument("--check", action="store_true",
                    help="only validate the coding against the script (ids, sentence numbers, kinds); no verdict")
    args = ap.parse_args()
    if args.list:
        for n in args.chapters:
            list_lines(n)
        return
    if args.codes and len(args.chapters) > 1:
        raise SystemExit("vk load: --codes takes one chapter")
    caller = Path(os.environ.get("VK_CALLER_PWD", "."))     # vk cd's to the project: paths given are the caller's
    out = caller / args.out if args.out else ROOT / "media" / "review"
    out.mkdir(parents=True, exist_ok=True)
    worst = 0
    for n in args.chapters:
        codes = [caller / c for c in args.codes] if args.codes else [ROOT / "script" / f"ch{n}_load.json"]
        if not all(Path(p).exists() for p in codes):
            print(f"ch{n} NO CODING: {', '.join(str(p) for p in codes if not Path(p).exists())} "
                  f"(run a load-auditor on chapter {n})")
            worst = 2
            continue
        if args.check:
            lines, _ = chapter_lines(n)
            clips, _, _ = timeline(n, lines, "script", None)
            for p in codes:
                try:
                    k = read_coding(p, clips)
                except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
                    print(f"ch{n} BAD CODING: {e}")
                    worst = 2
                    continue
                state = f"has {len(k['warn'])} warning(s)" if k["warn"] else "ok"
                print(f"ch{n} coding {state}: {len(clips)} lines, {len(k['holds'])} holds, {len(k['qs'])} questions, "
                      f"{sum(k['ideas'].values()):g} ideas, {sum(k['motive'].values()):g} motive")
                for w in k["warn"]:
                    print(f"     warning: {w}")
                worst = max(worst, 2 if k["warn"] else 0)
            continue
        try:
            r = analyse(n, codes, args.timing, args.wpm)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            print(f"ch{n} BAD CODING: {e}")
            worst = 2
            continue
        (out / f"ch{n}_load.md").write_text(report(r) + "\n")
        print(summary(r) + f"\n     → {(out / f'ch{n}_load.md')}")
        if args.rail:
            print("     rail candidates:\n" + "\n".join("     " + x for x in rail(r)))
        if r["verdict"] == "over":
            worst = max(worst, 1)
    sys.exit(worst)


if __name__ == "__main__":
    main()
