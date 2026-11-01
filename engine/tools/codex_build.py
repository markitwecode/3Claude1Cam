"""Build or fix one scene with Codex (OpenAI's agent, GPT-6.1 Sol), off the Claude quota.

    vk build <stem> [--context "…"] [--notes "1) … 2) …"] [--model gpt-6.1-sol] [--effort medium]

Runs `codex exec` in the project with the scene-builder's own instructions
(.claude/agents/scene-builder.md, everything below its frontmatter), so a Codex build follows the
same workflow, checks and report format as a Claude scene-builder. `--notes` makes it a fix pass
(a fresh session, like a fresh Claude fix builder). Prints the builder's report, its time and tokens.
Gotchas (LESSONS, 2026-10-28): stdin must be closed or codex waits for it; the sandbox needs
engine/.locks writable for the memory budget.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import project  # noqa: E402

STUDIO = ENGINE.parent
ROOT = project()


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("stem")
    ap.add_argument("--notes", help="review notes: makes this a fix pass")
    ap.add_argument("--context", help="continuity for a build: shared shots, which scene files to match")
    ap.add_argument("--model", default="gpt-6.1-sol")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--instructions", type=Path,
                    default=STUDIO / ".claude/agents/scene-builder.md",
                    help="role instruction file (default preserves the Claude workflow)")
    a = ap.parse_args()
    instructions = a.instructions.expanduser().resolve()
    if not instructions.is_file():
        ap.error(f"instruction file does not exist: {instructions}")
    vk = f"{STUDIO}/engine/vk -C {ROOT}"
    task = (f"Fix pass on {a.stem}: {a.notes}\nApply exactly these notes, re-check, and report."
            if a.notes else f"Build scene {a.stem}." + (f" Continuity: {a.context}" if a.context else ""))
    prompt = (f"First read {instructions}: everything below any frontmatter is "
              f"your instruction set; you are the scene-builder it describes. Project folder: {ROOT}. {task} "
              f"Run every vk command as `{vk} <command>`, exactly as the instructions say. Write only "
              f"{ROOT}/scenes/{a.stem}.py (plus temp files under {ROOT}/media or /tmp). To look at the beats "
              f"image, open the PNG with your image viewing tool. Finish with the report described at the end "
              f"of the instructions.")
    out = ROOT / "media" / "codex"
    out.mkdir(parents=True, exist_ok=True)
    tag = f"{a.stem}{'_fix' if a.notes else ''}_{time.strftime('%H%M%S')}"
    last = out / f"{tag}.md"
    t0 = time.time()
    with open(out / f"{tag}.jsonl", "w") as log:
        rc = subprocess.run(["codex", "exec", "-m", a.model, "-c", f'model_reasoning_effort="{a.effort}"',
                             "-s", "workspace-write", "-C", str(ROOT), "--add-dir", str(ENGINE / ".locks"),
                             "--skip-git-repo-check", "--json", "-o", str(last), prompt],
                            stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT).returncode
    usage = {}
    for line in open(out / f"{tag}.jsonl"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "turn.completed":
            usage = e.get("usage", {})
    print(last.read_text().strip() if last.exists() else f"(no report; codex exit {rc}, log {out / tag}.jsonl)")
    print(f"[codex {a.model}/{a.effort}: {(time.time() - t0) / 60:.1f} min, exit {rc}, "
          f"in {usage.get('input_tokens', 0) / 1e3:.0f}k (cached {usage.get('cached_input_tokens', 0) / 1e3:.0f}k), "
          f"out {usage.get('output_tokens', 0) / 1e3:.1f}k; no Claude tokens]")
    sys.exit(rc)


if __name__ == "__main__":
    main()
