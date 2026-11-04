"""Pace voiced narration without re-voicing: varied pauses (house default since 2026-11-03).

    vk regap N [--seed S] [--scale X] [--speed V] [--fixed] [--only ID ...] [--revert]

voice.py joins a line's separately voiced sentences with exact digital silence (the fixed
SENTENCE_GAP, or a {pause}), which sounds metronomic. This finds those silences, stretches each
sentence gap to a seeded random length (a longer beat after a question or a long sentence),
multiplies everything by `scale` ({pause}s too), optionally slows the speech itself (`speed`,
Rubber Band), shifts the line's word timings and marks to match, and gives the line a varied
"gap_after" that NarratedScene.say uses instead of its fixed 0.35 s (a scene's own `gap=` wins).

HOUSE pacing (the user's choice, 2026-11-03): varied pauses, twice as long, speech at normal
speed. `vk voice` applies it to every line it voices or re-times (apply(), below), so new
projects get it without asking; project.json "pacing": "fixed" opts a project out, or a dict
overrides the knobs ({"scale": 1.5}). Already-finished projects: `vk regap N` per chapter, then
`vk finalize N --no-review`.

Originals: an entry without the "regap" marker is un-paced audio straight from `vk voice`; it is
copied to audio/.pre-regap/ and every run starts from there, so re-running with other values is
safe and --revert restores it. The voice cache key is untouched, so `vk voice` never re-voices a
line just because it was paced.
"""
import argparse
import fcntl
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice  # noqa: E402  (split_line, VOICE, update_manifest, AUDIO, MANIFEST)

BACKUP = voice.AUDIO / ".pre-regap"
SENT = voice.VOICE["sentence_gap"]
CLOSERS = "\"'”’)]"
DEFAULT_GAP = 0.35   # NarratedScene.gap: the fixed silence after a line
HOUSE = {"seed": "1", "scale": 2.0, "speed": 1.0, "vary": True}   # user's choice, 2026-11-03


def pacing():
    """The project's pacing: HOUSE, overridden by project.json "pacing" (a dict of knobs), or
    None when it says "fixed" (no re-pacing)."""
    cfg = json.loads((voice.ROOT / "project.json").read_text()) if (voice.ROOT / "project.json").exists() else {}
    p = cfg.get("pacing")
    if p in ("fixed", False):
        return None
    return {**HOUSE, **(p if isinstance(p, dict) else {})}


def sentence_gap(rng, n_words, last_word):
    """A breath between sentences: mostly 0.45–0.8 s, now and then up to ~1 s."""
    g = rng.triangular(0.40, 1.05, 0.60)
    if last_word.rstrip(CLOSERS).endswith("?"):
        g += 0.25                      # let a question land
    if n_words >= 18:
        g += 0.12                      # a long sentence earns a breath
    return round(g, 3)


def line_gap(rng, text):
    """Silence after the line (before the next one starts), replacing the fixed 0.35 s."""
    g = rng.triangular(0.30, 0.85, 0.45)
    if text.rstrip().rstrip(CLOSERS).endswith("?"):
        g += 0.30
    return round(g, 3)


def zero_runs(a, sr, min_s):
    z = (a == 0).astype(np.int8)
    d = np.diff(np.r_[0, z, 0])
    starts, ends = np.where(d == 1)[0], np.where(d == -1)[0]
    return [(int(s), int(e)) for s, e in zip(starts, ends) if e - s >= min_s * sr]


def original(cid, cur, backups):
    """The un-paced entry and wav for `cid`. An entry without the "regap" marker is an original
    (fresh from `vk voice`) and becomes the backup; a marked one is rebuilt from its backup."""
    if "regap" not in cur:
        BACKUP.mkdir(parents=True, exist_ok=True)
        shutil.copy2(voice.ROOT / cur["file"], BACKUP / f"{cid}.wav")
        backups[cid] = cur
        return cur, BACKUP / f"{cid}.wav"
    bk = backups.get(cid)
    if bk is None or bk["key"] != cur["key"] or not (BACKUP / f"{cid}.wav").exists():
        raise RuntimeError(f"{cid}: paced, but its original in audio/.pre-regap is missing or stale; "
                           f"re-voice it: vk voice --only {cid} --force")
    return bk, BACKUP / f"{cid}.wav"


def stretch(seg, sr, ratio):
    """Time-stretch int16 speech by `ratio` (1.33 = a third longer) with Rubber Band's R3 engine,
    pitch and formants kept, so it sounds like slower speech, not a slowed tape."""
    if abs(ratio - 1.0) < 1e-9 or len(seg) == 0:
        return seg
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d, "in.wav"), Path(d, "out.wav")
        sf.write(src, seg, sr, subtype="PCM_16")
        subprocess.run(["rubberband", "-q", "-3", "--formant", "-t", f"{ratio:.6f}", str(src), str(dst)],
                       check=True, capture_output=True)
        out, _ = sf.read(dst, dtype="int16")
    return out


def regap(cid, entry, wav, seed, scale=1.0, speed=1.0, vary=True):
    """-> new manifest entry, new audio, report line; or (None, None, reason).
    `vary`: random sentence gaps and gap after the line (else the originals). `scale` multiplies
    every pause. `speed` < 1 slows the speech itself (the silences stay exact)."""
    words, _, chunks = voice.split_line(entry["raw"])
    audio, sr = sf.read(wav, dtype="int16")
    expected = [(k, g) for k, (_, _, g) in enumerate(chunks) if g > 0]
    runs = zero_runs(audio, sr, min((g for _, g in expected), default=SENT) - 0.02)
    if len(runs) != len(expected):
        return None, None, f"{len(runs)} silences for {len(expected)} expected gaps; left as is"
    rng = random.Random(f"{seed}:{cid}")
    ratio = 1.0 / speed
    pieces, tmap, gaps, prev, pos = [], [], [], 0, 0      # tmap: (kind, old a, old b, new a, new b)

    def put(kind, old_a, old_b, samples):
        nonlocal pos
        tmap.append((kind, old_a, old_b, pos, pos + len(samples)))
        pieces.append(samples)
        pos += len(samples)

    for (s, e), (k, g) in zip(runs, expected):
        a, b, _ = chunks[k]
        if abs(g - SENT) < 1e-6:
            new = scale * (sentence_gap(rng, b - a, words[b - 1]) if vary else g)
        else:
            new = scale * g                                   # a {pause}: as written, times scale
        put("speech", prev, s, stretch(audio[prev:s], sr, ratio))
        put("gap", s, e, np.zeros(max(1, (e - s) + int(round((new - g) * sr))), np.int16))
        prev = e
        gaps.append(new)
    put("speech", prev, len(audio), stretch(audio[prev:], sr, ratio))
    out = np.concatenate(pieces)

    def moved(t):
        """Old time -> new: linear inside speech; inside a gap, kept relative to the gap's END,
        so a mark 0.05 s before the next word stays 0.05 s before it."""
        x = t * sr
        for kind, oa, ob, na, nb in tmap:
            if oa <= x < ob:
                if kind == "speech":
                    return round((na + (x - oa) * (nb - na) / (ob - oa)) / sr, 3)
                return round(max(na, nb - (ob - x)) / sr, 3)
        return round(pos / sr - max(0.0, len(audio) / sr - t), 3)

    new_entry = dict(entry)
    new_entry["duration"] = round(len(out) / sr, 3)
    new_entry["words"] = [[w, moved(t)] for w, t in entry["words"]]
    new_entry["marks"] = {m: moved(t) for m, t in entry["marks"].items()}
    if vary or scale != 1.0:
        new_entry["gap_after"] = round(scale * (line_gap(rng, entry["text"]) if vary else DEFAULT_GAP), 3)
    else:
        new_entry.pop("gap_after", None)
    new_entry["regap"] = {"seed": seed, "scale": scale, "speed": speed, "vary": vary,
                          "gaps": [round(g, 3) for g in gaps]}
    after = new_entry.get("gap_after", DEFAULT_GAP)
    note = (f"{len(gaps)} gaps {' '.join(f'{g:.2f}' for g in gaps) or '-'} · after {after:.2f}"
            f" · {entry['duration']:.1f} → {new_entry['duration']:.1f} s")
    return new_entry, (out, sr), note


def apply(ids, seed=HOUSE["seed"], scale=HOUSE["scale"], speed=HOUSE["speed"], vary=HOUSE["vary"],
          revert=False, say=print):
    """Pace (or --revert) the voiced lines `ids`; -> (lines changed, minutes before, minutes after)."""
    manifest = json.loads(voice.MANIFEST.read_text())
    bfile = BACKUP / "manifest.json"
    backups = json.loads(bfile.read_text()) if bfile.exists() else {}
    changes, before, after = {}, 0.0, 0.0
    for cid in ids:
        cur = manifest.get(cid)
        if cur is None:
            continue
        if revert:
            bk = backups.get(cid)
            if bk is not None and bk["key"] == cur["key"] and "regap" in cur:
                shutil.copy2(BACKUP / f"{cid}.wav", voice.ROOT / bk["file"])
                changes[cid] = bk
                say(f"{cid:<16} reverted")
            continue
        entry, wav = original(cid, cur, backups)
        new_entry, sound, note = regap(cid, entry, wav, seed, scale, speed, vary)
        before += entry["duration"]
        if new_entry is None:
            say(f"{cid:<16} {note}")
            after += entry["duration"]
            continue
        sf.write(voice.ROOT / entry["file"], sound[0], sound[1], subtype="PCM_16")
        changes[cid] = new_entry
        after += new_entry["duration"]
        say(f"{cid:<16} {note}")
    BACKUP.mkdir(parents=True, exist_ok=True)
    with open(voice.AUDIO / ".manifest.lock", "w") as lock:      # same lock as update_manifest
        fcntl.flock(lock, fcntl.LOCK_EX)
        on_disk = json.loads(bfile.read_text()) if bfile.exists() else {}
        on_disk.update({c: backups[c] for c in ids if c in backups})
        bfile.write_text(json.dumps(on_disk, indent=1))
    voice.update_manifest(changes)
    return len(changes), before / 60, after / 60


def main():
    p = pacing() or HOUSE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapter", type=int)
    ap.add_argument("--seed", default=p["seed"])
    ap.add_argument("--scale", type=float, default=p["scale"],
                    help=f"multiply every pause (varied gaps, {{pause}}s, gap after the line); default {p['scale']}")
    ap.add_argument("--speed", type=float, default=p["speed"],
                    help="slow (or speed up) the speech itself, e.g. 0.9; the pauses stay exact")
    ap.add_argument("--fixed", action="store_true",
                    help="keep the original fixed pauses (only --speed / --scale apply)")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--revert", action="store_true")
    args = ap.parse_args()

    manifest = json.loads(voice.MANIFEST.read_text())
    prefix = f"c{args.chapter}."
    ids = [c for c in manifest if c.startswith(prefix) and (args.only is None or c in args.only)]
    if not ids:
        raise SystemExit(f"no voiced lines for chapter {args.chapter}")
    n, before, after = apply(ids, args.seed, args.scale, args.speed, not args.fixed and p["vary"], args.revert)
    if not args.revert:
        print(f"narration {before:.2f} → {after:.2f} min (plus the varied gaps after lines)")
    print(f"{n} line(s) updated. Re-render: vk finalize {args.chapter} --no-review")


if __name__ == "__main__":
    main()
