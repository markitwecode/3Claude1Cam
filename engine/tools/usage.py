"""Token usage of Claude Code sessions on this project, per agent, from the transcripts.

    python3 tools/usage.py            # the most recent session
    python3 tools/usage.py <session-id-prefix> [--all]   # --all: also list every agent

Context is re-read on every turn, so cost ≈ turns × average context: the columns to watch are
`turns`, `peak ctx` and `ctx read`. ("ctx read" = cache reads + writes + uncached input; output
tokens aren't reliable in transcripts, so they're left out.) Background: LESSONS.md, "Token budget".
"""
import glob
import json
import os
import sys

# transcripts of sessions started in the studio folder (3Claude1Cam), where every session should start
STUDIO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.expanduser("~/.claude/projects/" + STUDIO.replace("/", "-") + "/")


def stats(path):
    seen, turns, read, write, peak, first, t0, t1 = set(), 0, 0, 0, 0, None, None, None
    for line in open(path):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get("message") or {}
        ts = d.get("timestamp")
        if ts:
            t0, t1 = t0 or ts, ts
        if d.get("type") == "user" and first is None:
            c = m.get("content")
            first = c if isinstance(c, str) else next(
                (x.get("text", "") for x in c or [] if isinstance(x, dict) and x.get("type") == "text"), "")
        if d.get("type") == "assistant" and m.get("id") not in seen:
            seen.add(m.get("id"))
            u = m.get("usage") or {}
            turns += 1
            r, w = u.get("cache_read_input_tokens", 0) or 0, u.get("cache_creation_input_tokens", 0) or 0
            i = u.get("input_tokens", 0) or 0
            read += r + i
            write += w
            peak = max(peak, r + w + i)
    return turns, read, write, peak, (first or "").replace("\n", " "), t0, t1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sessions = sorted(glob.glob(BASE + "*.jsonl"), key=os.path.getmtime)
    if args:
        sessions = [s for s in sessions if os.path.basename(s).startswith(args[0])]
    if not sessions:
        sys.exit("no matching session")
    main_path = sessions[-1]
    sid = os.path.basename(main_path)[:-6]
    agents = sorted(glob.glob(f"{BASE}{sid}/subagents/*.jsonl"), key=os.path.getmtime)
    rows = [("main", stats(main_path))] + [(os.path.basename(a)[6:15], stats(a)) for a in agents]
    tot_r = sum(r[1][1] for r in rows)
    tot_w = sum(r[1][2] for r in rows)
    print(f"session {sid}: {len(agents)} agents, ctx read {tot_r / 1e6:.1f}M, cache writes {tot_w / 1e6:.1f}M")
    print(f"{'who':10} {'turns':>5} {'ctx read':>9} {'writes':>7} {'peak ctx':>8}  task")
    for who, (turns, r, w, peak, first, t0, t1) in rows:
        if who != "main" and "--all" not in sys.argv and r < 2e5:
            continue
        print(f"{who:10} {turns:5} {r / 1e6:8.2f}M {w / 1e6:6.2f}M {peak / 1e3:7.0f}k  {first[:70]}")


if __name__ == "__main__":
    main()
