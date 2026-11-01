"""Gemini watches a video (with sound) through the Antigravity CLI `agy`. Shared by
tools/lecture.py (vk lecture) and tools/review.py (vk review).

    from gemini import cut, watch, ffprobe_duration
    cut(src, dst, start=600, duration=600)        # 720p30 H.264/AAC piece of a video
    r = watch(dst, "List …", schema={...})          # r.data (parsed JSON), r.usage, r.seconds

How agy is called (verified 2026-10-28, agy 1.4.7): from a scratch directory holding only the
clip, in plan mode (read-only), JSON output, with `--json-schema` for structured output. The prompt
must tell it to open the clip with its file viewing tool and run no shell commands; otherwise it
tries a shell command, plan mode denies it, and the response comes back empty.

Costs measured: ~15k input tokens per minute of video plus ~50k fixed per call (agy's own
prompt, sent on each of its turns); a 25 s clip took ~110 s, a 90 s clip ~95 s. Its findings are
claims (a mid-transition frame can read as a "glitch"), so callers keep them as such.
Standard library only (imported from both venvs).
"""
import json
import os
import random
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

try:
    import joblog          # tools/: one line per call in engine/logs/gemini.jsonl
except Exception:  # noqa: BLE001
    joblog = None

AGY = Path(os.environ.get("VK_AGY") or shutil.which("agy") or Path.home() / ".local" / "bin" / "agy")
DEFAULT_MODEL = "gemini-3.8-flash-medium"
# a failed call waits before retrying (instant retries hammer a tight quota); quota or rate errors
# wait longer and get up to two extra attempts (2026-11-01). VK_GEMINI_BACKOFF scales the waits.
QUOTA = re.compile(r"429|RESOURCE.?EXHAUSTED|quota|rate.?limit|too many requests|usage limit|limit reached", re.I)
# circuit breaker: once a call fails on quota after its retries, logs/gemini-off is written and every
# later call (any session) fails at once instead of waiting through retries (2026-11-01: the user's
# weekly quota ran out). It expires after VK_GEMINI_OFF_HOURS (24); the next call is then a probe:
# one attempt, no retries, so a quota that's still out costs ~20 s and re-arms the switch, and a quota
# that has come back just works. Deleting the file turns Gemini on at once; VK_GEMINI=0 turns it off.
OFF_FILE = Path(__file__).resolve().parent.parent / "logs" / "gemini-off"


STREAK, STREAK_SPAN, STREAK_HOURS = 6, 120, 1.0   # failures in a row (any session) that also trip it


def off_reason():
    """Why Gemini is off right now ('' when it is on). The file's first line may say "hours: N"
    (a failure-streak trip lasts 1 h; a quota trip VK_GEMINI_OFF_HOURS, default 24)."""
    if os.environ.get("VK_GEMINI", "1") == "0":
        return "VK_GEMINI=0"
    try:
        text = OFF_FILE.read_text()
        hours = float(os.environ.get("VK_GEMINI_OFF_HOURS", "24"))
        first, _, rest = text.partition("\n")
        if first.startswith("hours:"):
            hours, text = float(first.split(":", 1)[1]), rest
        if time.time() - OFF_FILE.stat().st_mtime < hours * 3600:
            return text.strip() or "quota exhausted"
    except (OSError, ValueError):
        pass
    return ""


def _trip(why, hours=None):
    m = re.search(r"Resets in (\d+)h(\d+)m", why)   # Antigravity says when the quota comes back
    if m:
        hours = int(m.group(1)) + int(m.group(2)) / 60 + 0.1
    try:
        OFF_FILE.parent.mkdir(exist_ok=True)
        head = f"hours: {hours}\n" if hours else ""
        OFF_FILE.write_text(f"{head}off at {time.strftime('%Y-%m-%d %H:%M')}: {why[:200]}\n")
    except OSError:
        pass


def _streak_failed():
    """True when the last STREAK Gemini calls studio-wide (engine/logs/gemini.jsonl) all failed and
    span at least STREAK_SPAN s: an outage or a quota message the QUOTA pattern doesn't know
    (2026-11-01: "invalid model selection", 11 in a row, as the weekly quota ran out)."""
    try:
        lines = (OFF_FILE.parent / "gemini.jsonl").read_text().splitlines()[-STREAK:]
        recs = [json.loads(x) for x in lines]
    except (OSError, ValueError):
        return False
    return (len(recs) == STREAK and not any(r.get("ok") for r in recs)
            and recs[-1]["ts"] - recs[0]["ts"] >= STREAK_SPAN)
# agy in plan mode sometimes tries a shell command instead of opening the file and is denied: a
# flake, not a bad prompt; give it extra attempts after a short pause (2026-11-01: 5 of 9 digest calls)
DENIED = re.compile(r"agy denied", re.I)
BACKOFF = float(os.environ.get("VK_GEMINI_BACKOFF", "1"))
OPEN = ("Open the file {name} in the current directory with your file viewing/reading tool (it "
        "attaches media so you can watch and hear it). Do not run any shell commands, do not create "
        "or edit files, and do not open any other file.\n\n")
USAGE_KEYS = ("input_tokens", "output_tokens", "thinking_tokens", "cache_read_tokens", "total_tokens")


class GeminiError(RuntimeError):
    pass


@dataclass
class Result:
    data: object                 # the parsed JSON (structured output), or the raw text without a schema
    usage: dict = field(default_factory=dict)
    seconds: float = 0.0
    attempts: int = 1
    conversation: str = ""


def ffprobe_duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).strip())


def cut(src, dst, start=0.0, duration=None, height=720, fps=30):
    """A piece of `src` as a small H.264/AAC file for upload: `height`p, at most `fps` fps.
    Re-encoded (not stream-copied), so the piece starts exactly at `start`."""
    vf = f"scale=-2:'min({height},ih)',fps='min({fps},source_fps)'"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}"]
    if duration:
        cmd += ["-t", f"{duration:.3f}"]
    cmd += ["-i", str(src), "-map", "0:v:0", "-map", "0:a:0?", "-vf", vf, "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-ac", "2", "-movflags", "+faststart", str(dst)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        cmd[cmd.index("-vf") + 1] = f"scale=-2:'min({height},ih)'"   # ffmpeg without source_fps
        subprocess.run(cmd, check=True)
    return Path(dst)


def add_usage(total, usage):
    for k in USAGE_KEYS:
        total[k] = total.get(k, 0) + int((usage or {}).get(k) or 0)
    return total


def fmt_usage(u):
    return (f"{u.get('input_tokens', 0) / 1000:.0f}k in, {u.get('output_tokens', 0) / 1000:.1f}k out "
            f"(thinking {u.get('thinking_tokens', 0) / 1000:.1f}k)")


def _parse(out, schema):
    """agy's JSON -> (data, why it's unusable or '')."""
    try:
        j = json.loads(out)
    except json.JSONDecodeError:
        return None, f"output is not JSON: {out[:200]!r}"
    if j.get("denied_actions"):
        return j, f"agy denied {j['denied_actions']}"
    if j.get("status") not in (None, "SUCCESS"):
        return j, f"status {j.get('status')}"
    if schema is None:
        text = (j.get("response") or "").strip()
        return j, "" if text else "empty response"
    data = j.get("structured_output")
    if data is None:
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", (j.get("response") or "").strip())
        try:
            data = json.loads(text) if text else None
        except json.JSONDecodeError:
            return j, f"response is not JSON: {text[:200]!r}"
    if not data:
        return j, "empty response"
    j["structured_output"] = data
    return j, ""


def watch(media, task, schema=None, model=DEFAULT_MODEL, timeout=None, retries=1, log=print):
    """Gemini watches (and hears) `media` and does `task`. With `schema` (a JSON schema dict), the
    answer is enforced and parsed. Retries `retries` time(s) on an empty, denied or unparsable
    answer, or a timeout. -> Result; raises GeminiError when every attempt fails."""
    media = Path(media)
    off = off_reason()
    if off:
        raise GeminiError(f"Gemini is off ({off}); skipped")
    probe = OFF_FILE.exists()          # the switch expired: one attempt decides whether it's back
    if not AGY.exists():
        raise GeminiError(f"agy not found at {AGY} (set VK_AGY)")
    dur = ffprobe_duration(media)
    timeout = timeout or max(300, int(2 * dur) + 240)      # measured ~1x real time + overhead
    total, why = {}, ""
    t0 = time.time()
    attempt, max_attempts = 0, (1 if probe else retries + 1)
    while attempt < max_attempts:
        attempt += 1
        pause = 0.0
        t_att = time.time()
        scratch = Path(tempfile.mkdtemp(prefix="vk-gemini-"))
        try:
            clip = scratch / f"clip{media.suffix}"
            try:
                os.link(media, clip)          # same volume: no copy
            except OSError:
                shutil.copy2(media, clip)
            cmd = [str(AGY), "--model", model, "--mode", "plan", "--print-timeout", f"{timeout}s",
                   "--output-format", "json", "--disable-slash-commands"]
            if schema is not None:
                cmd += ["--json-schema", json.dumps(schema)]
            cmd += ["-p", OPEN.format(name=clip.name) + task]
            try:
                p = subprocess.run(cmd, cwd=scratch, capture_output=True, text=True, timeout=timeout + 60)
                j, why = _parse(p.stdout, schema)
                if p.returncode and not why:
                    why = f"agy exit {p.returncode}"
                if p.returncode and p.stderr.strip():
                    why += f": {p.stderr.strip()[-300:]}"
            except subprocess.TimeoutExpired:
                j, why = None, f"timed out after {timeout + 60}s"
            add_usage(total, (j or {}).get("usage"))
            if joblog is not None:
                joblog.write("gemini", media=media.name, media_s=round(dur, 1), model=model,
                             attempt=attempt, call_s=round(time.time() - t_att, 1), ok=not why,
                             why=why[:300], usage=(j or {}).get("usage"))
            if not why:
                data = j["structured_output"] if schema is not None else j["response"].strip()
                if probe:
                    try:
                        OFF_FILE.unlink()      # the quota is back
                    except OSError:
                        pass
                return Result(data, total, time.time() - t0, attempt, j.get("conversation_id", ""))
            if QUOTA.search(why) and not probe:
                max_attempts = min(max(max_attempts, attempt + 1), retries + 3)
                pause = random.uniform(120, 240) * BACKOFF
            elif DENIED.search(why):
                max_attempts = min(max(max_attempts, attempt + 1), retries + 3)
                pause = random.uniform(5, 15) * BACKOFF
            else:
                pause = random.uniform(10, 30) * BACKOFF
            if attempt < max_attempts:
                log(f"  gemini: {media.name}: {why}; retrying in {pause:.0f}s")
            else:
                pause = 0.0
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
        if pause:
            time.sleep(pause)
    if QUOTA.search(why):
        _trip(why)
    elif _streak_failed():
        _trip(f"{STREAK} failed calls in a row, last: {why}", hours=STREAK_HOURS)
    raise GeminiError(f"{media.name}: {why} (after {attempt} attempts, {time.time() - t0:.0f}s)")


def parse_time(s):
    """'mm:ss.s', 'm:ss', 'hh:mm:ss(.s)' or '93.5' -> seconds (None if unreadable)."""
    s = str(s).strip().strip("[]()")
    m = re.match(r"^(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)", s)
    if m:
        h, mi, sec = m.groups()
        return int(h or 0) * 3600 + int(mi) * 60 + float(sec)
    m = re.match(r"^(\d+(?:\.\d+)?)\s*s?$", s)
    return float(m.group(1)) if m else None


def hms(t, frac=False):
    """Seconds -> 'hh:mm:ss' (or 'hh:mm:ss.s')."""
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:" + (f"{s:04.1f}" if frac else f"{int(s):02d}")


def mss(t):
    """Seconds -> 'mm:ss.s'."""
    m, s = divmod(max(0.0, t), 60)
    return f"{int(m):02d}:{s:04.1f}"
