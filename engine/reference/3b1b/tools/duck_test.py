"""How deep does tools/music.py's sidechain duck really go? Measure it, don't guess.

    python -I duck_test.py TRACK OUT_DIR [voice clip ids...]

Builds a voice track from narration clips (audio/<id>.wav, joined with 1.5 s of silence
like a scene hold), normalises it to -16 LUFS exactly as the stitch step does, gains the
music to level_db below the voice, runs the same `sidechaincompress` with several
parameter sets, and reports the gain reduction (dB) per 50 ms frame, split into
  speech  - voice active
  breath  - silent runs of 0.3-0.9 s (the 0.55 s gap between sentences)
  pause   - silent runs >= 1.2 s ({pause} holds, line gaps), measured over their 2nd half
Needs ffmpeg and numpy.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
SR = 48000
FR = int(0.05 * SR)
LEVEL_DB = -14.0  # tools/music.py default
PARAMS = {
    "default (thr .02, r6, a20, rel600)": dict(threshold=0.02, ratio=6, attack=20, release=600),
    "thr .02, r3, a20, rel1500": dict(threshold=0.02, ratio=3, attack=20, release=1500),
    "thr .05, r4, a50, rel1500": dict(threshold=0.05, ratio=4, attack=50, release=1500),
    "thr .03, r2, a50, rel2000": dict(threshold=0.03, ratio=2, attack=50, release=2000),
    "thr .015, r10, a20, rel2000": dict(threshold=0.015, ratio=10, attack=20, release=2000),
    "thr .03, r2, a50, rel3000": dict(threshold=0.03, ratio=2, attack=50, release=3000),
    "thr .03, r2.5, a50, rel2500": dict(threshold=0.03, ratio=2.5, attack=50, release=2500),
    "thr .04, r2, a80, rel2500": dict(threshold=0.04, ratio=2, attack=80, release=2500),
    "thr .02, r2, a50, rel2500": dict(threshold=0.02, ratio=2, attack=50, release=2500),
}


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def read(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def lufs(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    import re
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def frames_db(x):
    n = len(x) // FR
    r = np.sqrt(np.mean(x[: n * FR].reshape(n, FR) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(r)


def main():
    track, out = Path(sys.argv[1]), Path(sys.argv[2])
    ids = sys.argv[3:] or ["c1.hook.1", "c1.hook.2", "c1.hook.3"]
    out.mkdir(parents=True, exist_ok=True)
    # voice: clips + 1.5 s holds, normalised like the stitch step
    parts = []
    for cid in ids:
        parts += ["-i", str(ROOT / "audio" / f"{cid}.wav")]
    n = len(ids)
    chain = "".join(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,apad=pad_dur=1.5[v{i}];" for i in range(n))
    ff(*parts, "-filter_complex", chain + "".join(f"[v{i}]" for i in range(n)) +
       f"concat=n={n}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,aresample={SR}[v]", "-map", "[v]",
       str(out / "voice.wav"))
    vdur = len(read(out / "voice.wav")) / SR
    gain = (-16 + LEVEL_DB) - lufs(track)
    ff("-i", str(track), "-t", f"{vdur:.3f}", "-af",
       f"aresample={SR},aformat=channel_layouts=stereo,volume={gain:.2f}dB", str(out / "music.wav"))
    v = frames_db(read(out / "voice.wav"))
    plain = frames_db(read(out / "music.wav"))
    # voice activity and silent-run classes
    active = v > -45
    cls = np.where(active, "speech", "")
    i = 0
    while i < len(active):
        if active[i]:
            i += 1
            continue
        j = i
        while j < len(active) and not active[j]:
            j += 1
        run = (j - i) * 0.05
        if 0.3 <= run <= 0.9:
            cls[i:j] = "breath"
        elif run >= 1.2:
            cls[i + (j - i) // 2: j] = "pause"
        i = j
    res = {}
    print(f"track {track.name}, level_db {LEVEL_DB}, voice {vdur:.1f} s "
          f"({(cls == 'speech').mean():.0%} speech frames, {(cls == 'breath').mean():.0%} breath, "
          f"{(cls == 'pause').mean():.0%} pause)")
    print(f"{'params':36} {'speech':>8} {'breath':>8} {'pause':>8}   (median gain reduction, dB)")
    for name, p in PARAMS.items():
        f = out / "ducked.wav"
        ff("-i", str(out / "music.wav"), "-i", str(out / "voice.wav"), "-filter_complex",
           f"[0:a][1:a]sidechaincompress=threshold={p['threshold']}:ratio={p['ratio']}:"
           f"attack={p['attack']}:release={p['release']}[d]", "-map", "[d]", str(f))
        gr = frames_db(read(f))[: len(plain)] - plain[: len(frames_db(read(f)))]
        row = {c: float(np.median(gr[(cls == c)[: len(gr)] & (plain[: len(gr)] > -70)])) for c in ("speech", "breath", "pause")}
        res[name] = row
        print(f"{name:36} {row['speech']:8.1f} {row['breath']:8.1f} {row['pause']:8.1f}")
    (out / "duck_results.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
