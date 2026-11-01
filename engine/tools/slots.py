"""Studio-wide memory budget for heavy jobs, shared by every session and agent on this machine.

The Mac has 32 GB shared by CPU and GPU. Measured 2026-10-28: macOS wired ~4.5 GB, apps + Claude
sessions + agy ~8 GB, so ~19 GB is left for studio jobs. Each heavy job declares its measured size:
  voice run (Chatterbox + 3 Whisper models)  7.0 GB  (MLX peak 6.4 + CPU Whisper)
  lecture transcript (Whisper medium)        3.0 GB  (estimate)
  Manim 1080p final render                   1.2 GB  (bench 2026-10-24: 8 at once = 9.1 GB)
  Manim 480p preview                         0.75 GB (measured 0.71)
  dry-run audit                              0.6 GB  (measured 0.58)
A job starts only when the jobs already running plus itself fit in VK_JOB_GB (default 19); a job
always starts when nothing else is running. Count caps stay as upper bounds (GPU 2, Manim 10:
8 renders already saturate the CPU). History: one fixed GPU slot made a 2-minute re-voice wait
20–30 min behind a bulk run; no limit at all filled RAM + 18 GB swap (both 2026-10-28).
The budget can't see other apps, so a job also waits while macOS reports memory pressure at
warning or worse (kern.memorystatus_vm_pressure_level >= 2) and studio jobs are running; it still
starts when nothing else is. Codex's DE L6 run held new work at warning by hand, and pressure stayed
normal through a whole lecture (2026-10-30). VK_PRESSURE_GATE=0 turns this off.
A slot is an flock on engine/.locks/<kind>-<i>.lock (freed when the holder exits, even on a crash);
the file holds "<pid> <GB> <label>". A job that has to wait says so once.
Every job logs a start (with its wait) and an end to engine/logs/jobs.jsonl (joblog.py, 2026-11-01).
"""
import atexit
import fcntl
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

try:
    import joblog          # tools/, next to this file
except Exception:  # noqa: BLE001
    joblog = None

LOCKS = Path(__file__).resolve().parent.parent / ".locks"
BUDGET_GB = float(os.environ.get("VK_JOB_GB", "19"))
GPU_SLOTS = int(os.environ.get("VK_GPU_SLOTS", "2"))
MANIM_SLOTS = int(os.environ.get("VK_MANIM_SLOTS", "10"))
PRESSURE_GATE = os.environ.get("VK_PRESSURE_GATE", "1") != "0"


def _pressure():
    """macOS memory pressure: 1 normal, 2 warning, 4 critical (1 when unknown or gated off)."""
    if not PRESSURE_GATE:
        return 1
    try:
        out = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
                             capture_output=True, text=True, timeout=5).stdout
        return int(out)
    except (OSError, ValueError, subprocess.SubprocessError):
        return 1


def _in_use():
    """GB declared by the slots currently held (any kind)."""
    total = 0.0
    for p in LOCKS.glob("*-*.lock"):
        try:
            fh = open(p, "a+")
        except OSError:
            continue
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)      # free: nobody holds it
            fcntl.flock(fh, fcntl.LOCK_UN)
        except BlockingIOError:                                 # held: count its declared size
            parts = p.read_text().split()
            try:
                total += float(parts[1])
            except (IndexError, ValueError):
                total += 1.0
        finally:
            fh.close()
    return total


_ACTIVE = {}      # id(lock file) -> start record, for the matching "end" log line


def _held():
    """{kind: number of held slots} (for the job log)."""
    out = {}
    for p in LOCKS.glob("*-*.lock"):
        try:
            with open(p, "a+") as fh:
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fcntl.flock(fh, fcntl.LOCK_UN)
                except BlockingIOError:
                    k = p.stem.rsplit("-", 1)[0]
                    out[k] = out.get(k, 0) + 1
        except OSError:
            pass
    return out


def _log_start(fh, kind, label, gb, t_req, first_why, used, pressure):
    if joblog is None:
        return
    try:
        t_start = time.time()
        rec = {"kind": kind, "label": label, "gb": gb, "t_req": round(t_req, 2),
               "wait_s": round(t_start - t_req, 2), "waited_for": first_why,
               "used_gb": round(used, 2), "pressure": pressure, "held": _held()}
        _ACTIVE[id(fh)] = (rec, t_start)
        joblog.write("jobs", ev="start", **rec)
    except Exception:  # noqa: BLE001
        pass


def _log_end(fh):
    item = _ACTIVE.pop(id(fh), None)
    if joblog is None or item is None:
        return
    rec, t_start = item
    try:
        joblog.write("jobs", ev="end", kind=rec["kind"], label=rec["label"], gb=rec["gb"],
                     wait_s=rec["wait_s"], run_s=round(time.time() - t_start, 2))
    except Exception:  # noqa: BLE001
        pass


@atexit.register
def _log_open_ends():
    """GPU slots are held until the process exits: log their ends here."""
    for key in list(_ACTIVE):
        item = _ACTIVE.pop(key, None)
        if joblog is not None and item is not None:
            rec, t_start = item
            try:
                joblog.write("jobs", ev="end", kind=rec["kind"], label=rec["label"], gb=rec["gb"],
                             wait_s=rec["wait_s"], run_s=round(time.time() - t_start, 2), at_exit=True)
            except Exception:  # noqa: BLE001
                pass


def acquire(kind, slots, label="", gb=1.0):
    """Block until a `kind` slot is free and `gb` fits the budget; return the held lock file."""
    LOCKS.mkdir(exist_ok=True)
    said = False
    t_req, first_why = time.time(), ""
    while True:
        with open(LOCKS / "admit.lock", "a+") as admit:          # one admission decision at a time
            fcntl.flock(admit, fcntl.LOCK_EX)
            used = _in_use()
            pressure = _pressure() if used else 1
            # one bulk voice run at a time: the other GPU slot stays free for short re-voices
            # (2026-11-01; two bulk runs would make a director's 2-minute fix wait an hour)
            bulk_busy = "(bulk)" in label and any("(bulk)" in lab for _, lab in holders(kind))
            if bulk_busy:
                why = "another bulk voice run holds a GPU slot (one at a time)"
            elif used == 0 or (used + gb <= BUDGET_GB and pressure < 2):
                for i in range(slots):
                    fh = open(LOCKS / f"{kind}-{i}.lock", "a+")
                    try:
                        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except BlockingIOError:
                        fh.close()
                        continue
                    fh.seek(0)
                    fh.truncate()
                    fh.write(f"{os.getpid()} {gb} {label}\n")
                    fh.flush()
                    _log_start(fh, kind, label, gb, t_req, first_why, used, pressure)
                    return fh
                why = f"all {slots} {kind} slots busy"
            elif pressure >= 2:
                why = f"macOS memory pressure {'critical' if pressure >= 4 else 'warning'}, {used:.1f} GB of studio jobs running"
            else:
                why = f"{used:.1f} of {BUDGET_GB:.0f} GB in use, needs {gb:.1f}"
        first_why = first_why or why
        if not said:
            print(f"waiting for memory ({why}){': ' + label if label else ''}", file=sys.stderr, flush=True)
            said = True
        time.sleep(1.5)


@contextmanager
def slot(kind, slots, label="", gb=1.0):
    fh = acquire(kind, slots, label, gb)
    try:
        yield
    finally:
        _log_end(fh)
        fh.close()


def holders(kind):
    """[(pid, label)] for the `kind` slots held right now, by any process (this one included)."""
    out = []
    for p in sorted(LOCKS.glob(f"{kind}-*.lock")):
        try:
            with open(p, "a+") as fh:
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fcntl.flock(fh, fcntl.LOCK_UN)
                except BlockingIOError:
                    parts = p.read_text().split(maxsplit=2)
                    pid = int(parts[0]) if parts and parts[0].isdigit() else 0
                    out.append((pid, parts[2].strip() if len(parts) > 2 else ""))
        except OSError:
            pass
    return out


def gpu(label, gb=7.0):
    """Hold a GPU slot for the rest of this process (released when it exits)."""
    return acquire("gpu", GPU_SLOTS, label, gb)


def manim(label="", gb=0.75):
    return slot("manim", MANIM_SLOTS, label, gb)
