"""Speech timing for the 3b1b study (run with engine/.venv/bin/python -I).

Method: decode mono 16 kHz, band-pass to the voice band (150-4000 Hz), 20 ms RMS in dB.
A frame is "voiced" if it is above (the file's 95th-percentile frame level - REL dB), i.e. a
silencedetect with a per-file noise floor. Inactive runs shorter than CLOSE s are filled (stops
between words are not silences), active blips shorter than 0.1 s are dropped. Frames outside the
narration spans (3b1b: human caption cues +-PAD; ours: the voiced clips' placement from
media/cues + audio/manifest.json) are forced silent, so music-only stretches don't count as speech.
"""
import json, re, subprocess, sys
import numpy as np

SR = 16000
HOP = 0.02            # 20 ms frames
CLOSE = 0.30          # gaps shorter than this are inside speech
PAD = 0.30            # caption-span padding
WORD = r"[A-Za-z0-9π]+(?:['’][A-Za-z]+)?"   # one spoken word (same regex both sides)


def envelope(path, start=None, dur=None):
    cmd = ["nice", "-n", "10", "ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if dur is not None:
        cmd += ["-t", str(dur)]
    cmd += ["-i", str(path), "-vn", "-ac", "1", "-ar", str(SR),
            "-af", "highpass=f=150,lowpass=f=4000", "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, np.float32)
    n = int(len(x) / (SR * HOP))
    fr = x[: n * int(SR * HOP)].reshape(n, -1)
    rms = np.sqrt((fr.astype(np.float64) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(rms + 1e-9)


def ref_level(db):
    v = db[db > -70]
    return float(np.percentile(v, 95)) if len(v) else -20.0


def runs(mask):
    """(start, end) frame index pairs of True runs."""
    m = np.concatenate([[False], mask, [False]]).astype(np.int8)
    d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def clean(active):
    a = active.copy()
    for s, e in runs(~a):                     # fill short gaps
        if (e - s) * HOP < CLOSE and s > 0 and e < len(a):
            a[s:e] = True
    for s, e in runs(a):                      # drop blips
        if (e - s) * HOP < 0.1:
            a[s:e] = False
    return a


def span_mask(n, spans):
    m = np.zeros(n, bool)
    for s, e in spans:
        m[max(0, int(s / HOP)): min(n, int(e / HOP) + 1)] = True
    return m


def metrics(active, words, total_s):
    """active: cleaned voiced mask over the whole file."""
    idx = np.where(active)[0]
    first, last = idx[0] * HOP, (idx[-1] + 1) * HOP
    span = last - first
    a = active[idx[0]: idx[-1] + 1]
    speech = a.sum() * HOP
    gaps = [(e - s) * HOP for s, e in runs(~a)]
    out = dict(runtime_min=total_s / 60, narrated_min=span / 60, speech_min=speech / 60, words=words,
               wpm_speech=words / (speech / 60), wpm_runtime=words / (total_s / 60),
               nospeech_share=1 - speech / span)
    for t in (1, 2, 4):
        out[f"gaps_ge{t}_per_min"] = sum(g >= t for g in gaps) / (span / 60)
    out["gap_median_s"] = float(np.median(gaps)) if gaps else 0
    out["gaps_ge0.3"] = len(gaps)
    return out


def caption_spans(json3):
    d = json.load(open(json3))
    spans, words = [], 0
    for e in d["events"]:
        if "segs" not in e:
            continue
        t = "".join(s.get("utf8", "") for s in e["segs"])
        if re.search(r"criblate|^\s*\[.*\]\s*$|♪", t) or not t.strip():
            continue
        s = e["tStartMs"] / 1000
        spans.append((s - PAD, s + e.get("dDurationMs", 0) / 1000 + PAD))
        words += len(re.findall(WORD, t))
    return spans, words


if __name__ == "__main__":
    print(__doc__)
