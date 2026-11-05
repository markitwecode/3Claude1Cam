"""Visual change at 2 fps, the same method both sides.

Frames: ffmpeg fps=2, scaled to 256x144 grey (area filter), so 480p and 1080p compare alike.
Per sample t (0.5 s apart):
  content  = |pixel - frame median| > 40 (the median is the background)
  change1  = share of ALL pixels that moved > 25 grey levels since t-0.5 s
  R        = share of CONTENT pixels (content at t-1 s or t) that changed > 25 levels since t-1 s
  occ      = content share in each 24x24-px cell (a 10x6 grid), tolerant to motion within a cell
  lost     = share of the occupancy at t-1 s that is gone at t: sum(max(occ[t-2]-occ[t], 0))/sum(occ[t-2])
A board reset = lost >= 0.6 (most of what was on screen 1 s ago is gone, not merely moved or
transformed in place) AND still gone 2 s later (lost(t-1 s -> t+2 s) >= 0.6), ink at t-1 s >= 0.5%
of the frame, peaks >= 3 s apart. Variants (16/48-px cells, no persistence) were tried on la3. (The
pixel-level R alone also fires on grid deformations and camera moves: checked by eye on la3.)
Still      = change1 < STILL (0.2% of the frame, ~74 px: a blink or a dot, not a new line).
usage: python -I visual.py <key> <video>   -> data/<key>.visual.npz, prints a summary
"""
import subprocess, sys
from pathlib import Path
import numpy as np

STUDY = Path(__file__).resolve().parent.parent
W, H = 256, 144
STILL = 0.002


def frames(video):
    cmd = ["nice", "-n", "10", "ffmpeg", "-v", "error", "-threads", "2", "-i", str(video), "-an",
           "-vf", f"fps=2,scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)


def analyse(F):
    n = len(F)
    bg = np.median(F.reshape(n, -1), axis=1).astype(np.int16)
    C = np.abs(F - bg[:, None, None]) > 40
    ink = C.mean((1, 2))
    ch1 = np.zeros(n)
    ch1[1:] = (np.abs(F[1:] - F[:-1]) > 25).mean((1, 2))
    R = np.zeros(n)
    big = np.zeros(n)
    for t in range(2, n):
        d = np.abs(F[t] - F[t - 2]) > 25
        u = C[t] | C[t - 2]
        big[t] = d.mean()
        R[t] = (d & u).sum() / max(u.sum(), 1)
    occ = C[:, :, :240].reshape(n, 6, 24, 10, 24).mean((2, 4))
    lost = np.zeros(n)
    later = np.zeros(n)
    for t in range(2, n):
        tot = occ[t - 2].sum()
        if ink[t - 2] >= 0.005:
            lost[t] = np.clip(occ[t - 2] - occ[t], 0, None).sum() / tot
            later[t] = np.clip(occ[t - 2] - occ[min(t + 4, n - 1)], 0, None).sum() / tot
    cand = np.where((lost >= 0.6) & (later >= 0.6))[0]
    resets = []
    for t in cand:                       # keep local peaks, >= 3 s apart
        if resets and t - resets[-1] < 6:
            if lost[t] > lost[resets[-1]]:
                resets[-1] = t
            continue
        resets.append(t)
    return dict(ink=ink, ch1=ch1, R=R, big=big, lost=lost, later=later, resets=np.array(resets, int))


if __name__ == "__main__":
    key, video = sys.argv[1], sys.argv[2]
    F = frames(video)
    a = analyse(F)
    np.savez_compressed(STUDY / f"data/{key}.visual.npz", **a)
    mins = len(F) / 2 / 60
    r = a["resets"]
    print(key, f"{mins:.1f} min, resets {len(r)} ({len(r)/mins:.2f}/min), mean gap "
          f"{np.diff(r).mean()/2 if len(r) > 1 else float('nan'):.1f} s, still {np.mean(a['ch1'] < STILL):.2f}, "
          f"ink {a['ink'].mean():.3f}")
