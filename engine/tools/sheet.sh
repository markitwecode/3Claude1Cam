#!/bin/sh
# Contact sheet of a rendered scene, for quick visual review.
#   tools/sheet.sh media/videos/s2_cons/480p15/ConsCells.mp4 [seconds_between_frames]
# Each tile is the first frame at/after a multiple of the interval, and its label is
# that frame's real timestamp.
in="$1"; every="${2:-3}"
out="${in%.mp4}_sheet.png"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
n=$(python3 -c "import math; print(math.ceil($dur/$every))")
cols=4; rows=$(( (n + cols - 1) / cols ))
ffmpeg -v error -y -i "$in" -fps_mode vfr -vf "select='isnan(prev_selected_t)+gte(t-prev_selected_t\,$every-0.001)',scale=427:-1,drawtext=text='%{pts\:hms}':x=6:y=h-22:fontcolor=white:fontsize=14:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=4:color=white" -frames:v 1 "$out"
echo "$out ($n frames, ${dur}s)"
