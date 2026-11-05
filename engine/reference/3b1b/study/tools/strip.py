"""Validation strip: for each detected reset, the 2-fps sample 1 s before and at the reset.
usage: python -I strip.py <key> <video> <out.png> [max]"""
import subprocess, sys, io
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
STUDY = Path(__file__).resolve().parent.parent
key, video, out = sys.argv[1:4]
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 16
a = np.load(STUDY / f"data/{key}.visual.npz")
rs = a["resets"]
if len(rs) > mx:
    rs = rs[np.linspace(0, len(rs) - 1, mx).astype(int)]
def grab(t):
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                          "-vf", "scale=240:135", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGB")
cols = 4
rows = (len(rs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 490, rows * 150), (40, 40, 40))
d = ImageDraw.Draw(sheet)
for i, r in enumerate(rs):
    x, y = (i % cols) * 490, (i // cols) * 150
    sheet.paste(grab(max(0, r / 2 - 1)), (x, y + 14)); sheet.paste(grab(r / 2), (x + 245, y + 14))
    d.text((x + 2, y), f"{int(r/2)//60}:{int(r/2)%60:02d}  lost={a['lost'][r]:.2f}", fill=(255, 255, 0))
sheet.save(out)
print(out, len(rs))
