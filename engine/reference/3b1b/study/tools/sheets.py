"""Contact sheets: one frame every 10 s, 320x180 tiles, 6 x 5 per sheet (5 min), timestamped.
usage: python -I sheets.py <key> <video>  -> sheets/<key>_NN.png"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
STUDY = Path(__file__).resolve().parent.parent
key, video = sys.argv[1:3]
TW, TH, COLS, ROWS, STEP = 320, 180, 6, 5, 10
raw = subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-threads", "2", "-i", video, "-an",
                      "-vf", f"fps=1/{STEP}:start_time=5,scale={TW}:{TH}:flags=area", "-f", "rawvideo",
                      "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, TH, TW, 3)
per = COLS * ROWS
for s in range(0, len(fr), per):
    sheet = Image.new("RGB", (COLS * (TW + 4), ROWS * (TH + 16)), (60, 60, 60))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(fr[s:s + per]):
        t = 5 + (s + i) * STEP
        x, y = (i % COLS) * (TW + 4), (i // COLS) * (TH + 16)
        sheet.paste(Image.fromarray(f), (x, y + 16))
        d.text((x + 2, y + 2), f"{t // 60}:{t % 60:02d}", fill=(255, 255, 0))
    sheet.save(STUDY / f"sheets/{key}_{s // per + 1:02d}.png")
print(key, len(fr), "frames", (len(fr) + per - 1) // per, "sheets")
