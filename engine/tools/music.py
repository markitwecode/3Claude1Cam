"""Music for a chapter: tracks placed relative to narration lines, ducked under the voice.

Used by tools/render.py when stitching (if music/chN.json exists). Cue sheet format:

    {"cues": [
      {"track": "assets/music/album/Some Track.ogg",     # relative to engine/
       "from": "START" | "c1.hook.1" | "c1.hook.1:end",   # chapter start, line start, line end
       "until": "c1.hook.2" | "END",
       "from_offset": 0, "until_offset": 0,               # seconds, may be negative
       "track_start": 0,                                  # where in the track to begin
       "fade_in": 2, "fade_out": 3,
       "level_db": -14,                                   # music loudness relative to the voice
       "swell_after": "c1.recap.1:end", "swell_db": 6}    # optional: rise for the end card
    ],
     "duck": {"threshold": 0.02, "ratio": 6, "attack": 20, "release": 600}}

Times come from media/cues/<scene>_<res>.json (written by NarratedScene during the real render)
plus each scene's offset in the stitched video, so music follows narration lines exactly even
after a line is re-voiced. Never hard-code seconds here either.

Levels: the narration is normalised to -16 LUFS; each music track is measured once
(engine/assets/music/.loudness.json) and gained so its integrated loudness sits level_db below the voice.
A sidechain compressor keyed by the voice then ducks it further while someone is speaking.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import project  # noqa: E402

ROOT = project()   # the project: music/chN.json cue sheets, audio/, media/cues/
VOICE_LUFS = -16.0
DUCK_DEFAULT = {"threshold": 0.03, "ratio": 2, "attack": 50, "release": 2000}  # MUSIC.md §4: no pumping


def probe_duration(path, stream="v"):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", f"{stream}:0", "-show_entries",
         "stream=duration", "-of", "csv=p=0", str(path)]).strip())


def track_loudness(track):
    """Integrated loudness (LUFS) of a track, cached in engine/assets/music/.loudness.json."""
    cache_path = ENGINE / "assets" / "music" / ".loudness.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    key = str(track)
    if key not in cache:
        out = subprocess.run(["ffmpeg", "-nostats", "-i", str(ENGINE / track), "-af", "ebur128",
                              "-f", "null", "-"], capture_output=True, text=True).stderr
        cache[key] = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])
        cache_path.write_text(json.dumps(cache, indent=1))
    return cache[key]


def line_times(scenes, res, manifest):
    """{line id: (abs start, abs end)} and total length, for the stitched chapter."""
    times, offset = {}, 0.0
    for stem, video in scenes:
        cue_file = ROOT / "media" / "cues" / f"{stem}_{res}.json"
        if not cue_file.exists():
            raise FileNotFoundError(f"{cue_file.name} missing: re-render {stem} at {res}")
        for clip in json.loads(cue_file.read_text())["clips"]:
            start = offset + clip["start"]
            times[clip["id"]] = (start, start + manifest[clip["id"]]["duration"])
        offset += probe_duration(video)
    return times, offset


def resolve(ref, times, total):
    if ref == "START":
        return 0.0
    if ref == "END":
        return total
    cid, _, which = ref.partition(":")
    if cid not in times:
        raise KeyError(f"music cue refers to unknown line {cid!r}")
    return times[cid][1 if which == "end" else 0]


def swell(cue, start, times, total):
    """Optional rise once narration is over, so the music carries the end card (3b1b style).
    "swell_after": a line ref (e.g. "c1.recap.1:end"), "swell_db": how much louder, ramped over
    "swell_ramp" seconds. Returns an ffmpeg volume filter (with a trailing comma) or ""."""
    if "swell_after" not in cue:
        return ""
    t0 = resolve(cue["swell_after"], times, total) - start   # in the cue's own timeline
    g = 10 ** (cue.get("swell_db", 6) / 20)
    ramp = cue.get("swell_ramp", 1.5)
    return (f"volume='if(lt(t,{t0:.3f}),1,min(1+(t-{t0:.3f})/{ramp}*({g:.4f}-1),{g:.4f}))'"
            f":eval=frame,")


def build(chapter, scenes, res):
    """-> (extra ffmpeg input args, filter_complex string, output label) or None if no music."""
    sheet_path = ROOT / "music" / f"ch{chapter}.json"
    if not sheet_path.exists():
        return None
    sheet = json.loads(sheet_path.read_text())
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    times, total = line_times(scenes, res, manifest)
    duck = {**DUCK_DEFAULT, **sheet.get("duck", {})}

    inputs, chains, labels = [], [], []
    for i, cue in enumerate(sheet["cues"]):
        a = max(0.0, resolve(cue["from"], times, total) + cue.get("from_offset", 0))
        b = min(total, resolve(cue["until"], times, total) + cue.get("until_offset", 0))
        if b - a < 0.5:
            continue
        dur = b - a
        fi, fo = cue.get("fade_in", 2), min(cue.get("fade_out", 3), dur / 2)
        gain = (VOICE_LUFS + cue.get("level_db", -14)) - track_loudness(cue["track"])
        inputs += ["-i", str(ENGINE / cue["track"])]
        idx = len(labels) + 1          # input 0 is the concatenated video+narration
        chains.append(
            f"[{idx}:a]atrim=start={cue.get('track_start', 0)}:duration={dur:.3f},asetpts=PTS-STARTPTS,"
            f"aformat=sample_rates=48000:channel_layouts=stereo,"
            f"afade=t=in:st=0:d={fi},afade=t=out:st={dur - fo:.3f}:d={fo},volume={gain:.2f}dB,"
            f"{swell(cue, a, times, total)}adelay={int(a * 1000)}:all=1[m{idx}]")
        labels.append(f"[m{idx}]")
    if not labels:
        return None

    music = (f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,"
             if len(labels) > 1 else f"{labels[0]}anull,")
    graph = ";".join([
        f"[0:a]aresample=async=1:first_pts=0,aresample=48000,aformat=channel_layouts=stereo,"
        f"loudnorm=I={VOICE_LUFS}:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={total:.3f}[vfull]",
        "[vfull]asplit=2[voice][key]",
        *chains,
        f"{music}apad=whole_dur={total:.3f}[mus]",
        f"[mus][key]sidechaincompress=threshold={duck['threshold']}:ratio={duck['ratio']}:"
        f"attack={duck['attack']}:release={duck['release']}[ducked]",
        "[voice][ducked]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[aout]",
    ])
    return inputs, graph, "[aout]"
