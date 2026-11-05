"""Measure every track of "The Music of 3Blue1Brown" for use as narration beds.

    python -I measure_album.py ALBUM_DIR OUT.json

Per track: duration (ffprobe); EBU R128 integrated loudness, loudness range and true
peak (ffmpeg ebur128); the short-term loudness curve (3 s window, 0.1 s step) summarised
as how fast the track builds, how it ends, its quietest steady minute and its loudest
30 s; and from librosa: tempo, onset rate (busyness), spectral centroid (brightness)
and the share of energy in the speech band (300-3400 Hz), which is what masks a voice.

Needs ffmpeg/ffprobe on PATH, numpy and librosa in a throwaway Python 3.12 venv
(librosa's beat tracker segfaulted in numba under Python 3.13, Oct 2026).
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

SR = 22050


def ebur128(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    err = p.stderr
    t, s = [], []
    for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET.*?S:\s*(-?[\d.]+)", err):
        t.append(float(m.group(1)))
        s.append(float(m.group(2)))
    summ = err[err.rfind("Summary:"):]
    get = lambda k: float(re.search(k + r":\s*(-?[\d.]+|-inf)", summ).group(1).replace("-inf", "-200"))
    return np.array(t), np.array(s), {"I": get("I"), "LRA": get("LRA"), "TP": get("Peak")}


def window_mean(t, s, width):
    """Mean short-term loudness of each `width`-second window (1 s hop)."""
    out = []
    for a in np.arange(0, max(t[-1] - width, 0) + 1e-9, 1.0):
        m = (t >= a) & (t < a + width)
        out.append((a, float(np.mean(s[m])), float(np.std(s[m]))))
    return out


def librosa_feats(path):
    import librosa
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True).stdout
    y = np.frombuffer(raw, dtype=np.float32).copy()
    tempo, _ = librosa.beat.beat_track(y=y, sr=SR)
    onsets = librosa.onset.onset_detect(y=y, sr=SR, units="time")
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=1024)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=2048)
    band = S[(f >= 300) & (f <= 3400)].sum() / max(S.sum(), 1e-12)
    cent = librosa.feature.spectral_centroid(S=np.sqrt(S), sr=SR)[0]
    dur = len(y) / SR
    return {"tempo_bpm": float(np.atleast_1d(tempo)[0]), "onsets_per_s": len(onsets) / dur,
            "centroid_hz": float(np.median(cent)), "speech_band_share": float(band)}


def measure(path):
    path = Path(path)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout)
    t, s, summ = ebur128(path)
    valid = s > -70
    sv = s[valid]
    p10, p50, p90 = (float(np.percentile(sv, q)) for q in (10, 50, 90))
    # build-up: first time the short-term loudness reaches the track's median - 3 dB
    reach = t[valid & (s >= p50 - 3)]
    ramp = float(reach[0]) if len(reach) else None
    # ending: last time it is at median - 6 dB, and the level of the final 10 s
    loud_idx = np.where(s >= p50 - 6)[0]
    tail = float(dur - t[loud_idx[-1]]) if len(loud_idx) else None
    last10 = float(np.mean(s[t >= dur - 10])) if (t >= dur - 10).any() else None
    first15 = float(np.mean(s[(t >= 3) & (t < 15)]))
    w60 = [w for w in window_mean(t, s, 60) if w[0] >= 3]
    calm = min(w60, key=lambda w: (w[2] + 0.3 * abs(w[1] - p50))) if w60 else None
    w30 = window_mean(t, s, 30)
    swell = max(w30, key=lambda w: w[1]) if w30 else None
    rec = {
        "file": path.name, "name": re.sub(r"^.* - \d\d ", "", path.stem),
        "track": int(re.search(r" - (\d\d) ", path.name).group(1)),
        "duration_s": round(dur, 1), **{k: round(v, 1) for k, v in summ.items()},
        "S_p10": round(p10, 1), "S_p50": round(p50, 1), "S_p90": round(p90, 1),
        "build_up_s": None if ramp is None else round(ramp, 1),
        "first_15s_rel_db": round(first15 - p50, 1),
        "last_10s_rel_db": None if last10 is None else round(last10 - p50, 1),
        "fade_tail_s": None if tail is None else round(tail, 1),
        "steadiest_minute_at_s": None if calm is None else calm[0],
        "steadiest_minute_std_db": None if calm is None else round(calm[2], 1),
        "loudest_30s_at_s": None if swell is None else swell[0],
        "loudest_30s_rel_db": None if swell is None else round(swell[1] - p50, 1),
        # shape of the track: mean short-term loudness of each 15 s block, relative to S_p50
        "profile_15s_rel_db": [round(float(np.mean(s[(t >= a) & (t < a + 15)])) - p50, 1)
                               for a in np.arange(0, t[-1], 15.0) if ((t >= a) & (t < a + 15)).any()],
    }
    rec.update({k: round(v, 3) for k, v in librosa_feats(path).items()})
    return rec


if __name__ == "__main__":
    album, out = Path(sys.argv[1]), Path(sys.argv[2])
    files = sorted(p for p in album.iterdir() if p.suffix.lower() in (".ogg", ".mp3", ".flac", ".wav"))
    with ProcessPoolExecutor(8) as ex:
        rows = list(ex.map(measure, files))
    rows.sort(key=lambda r: r["track"])
    out.write_text(json.dumps(rows, indent=1))
    cols = ["track", "name", "duration_s", "I", "LRA", "TP", "build_up_s", "first_15s_rel_db",
            "fade_tail_s", "tempo_bpm", "onsets_per_s", "centroid_hz", "speech_band_share",
            "steadiest_minute_at_s", "loudest_30s_at_s"]
    print("\t".join(cols))
    for r in rows:
        print("\t".join(str(r[c]) for c in cols))
    bars = " .:-=+*#%@"
    print("\nshape (15 s blocks, loudness relative to the track median; ' '=-12 dB or less, '@'=+6 dB)")
    for r in rows:
        line = "".join(bars[max(0, min(9, int((v + 12) / 2)))] for v in r["profile_15s_rel_db"])
        print(f"{r['track']:2} {r['name'][:22]:22} |{line}|")
