"""Append-only event logs for the studio's shared resources (engine/logs/*.jsonl), for measuring
where time goes: slot waits and run times (slots.py -> jobs.jsonl) and Gemini calls (gemini.py ->
gemini.jsonl). Standard library only: slots.py is imported from every venv.

One JSON object per line, written with a single O_APPEND write, so lines from concurrent processes
don't interleave. Logging must never break a job: every error here is swallowed.
Started 2026-11-01 to decide how many chapter-directors to run at once and whether the scheduler
needs priorities (see docs/LESSONS.md).
"""
import json
import os
import time
from pathlib import Path

LOGS = Path(__file__).resolve().parent.parent / "logs"
OFF = os.environ.get("VK_JOBLOG", "1") == "0"


def write(name, **rec):
    """Append `rec` (plus ts, pid, cwd) as one line to engine/logs/<name>.jsonl."""
    if OFF:
        return
    try:
        rec = {"ts": round(time.time(), 2), "pid": os.getpid(), "cwd": os.getcwd(), **rec}
        line = (json.dumps(rec, default=str, ensure_ascii=False) + "\n").encode()
        LOGS.mkdir(exist_ok=True)
        fd = os.open(LOGS / f"{name}.jsonl", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        try:
            os.write(fd, line)
        finally:
            os.close(fd)
    except Exception:  # noqa: BLE001  (a log line is never worth a failed render)
        pass
