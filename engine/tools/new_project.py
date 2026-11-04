"""Scaffold a project, its course (if new) and its material, and list it in projects/INDEX.md.

    vk new projects/digital-electronics/l04-flip-flops "Flip-flops" \\
           "Digital Electronics · Lecture 4" --lang verilog --source lecture4.pdf

- <folder> is relative to the studio (3Claude1Cam). projects/<course>/<lecture>/ makes a course
  lecture; projects/<slug>/ makes a one-off.
- A course folder that doesn't exist yet gets source/ and a COURSE.md stub.
- --source files go to the course's source/ (one-offs: the project's source/). Files inside the
  studio, e.g. dropped in its root, are MOVED; files from elsewhere are COPIED. They're recorded
  in project.json "sources" (pages and notes are left for the planner).
- Refuses to touch an existing project.json.
"""
import argparse
import json
import shutil
from datetime import date
from pathlib import Path

STUDIO = Path(__file__).resolve().parent.parent.parent
PROJECTS = STUDIO / "projects"


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("folder")
    ap.add_argument("title", help="big word on the title card, e.g. 'Flip-flops'")
    ap.add_argument("course_line", help="line under it, e.g. 'Digital Electronics · Lecture 4'")
    ap.add_argument("--lang", default="", help="Pygments lexer for on-screen code (empty: no code)")
    ap.add_argument("--source", nargs="*", default=[], help="material files to move/copy in")
    ap.add_argument("--style", choices=["auto", "deep", "classic"], default="auto",
                    help="teaching style (docs/DEEP_STYLE.md §0): auto = the lecture, enhanced (default); "
                         "deep = rebuilt from first principles; classic = the pre-2026-11-04 style at 1080p")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser()
    folder = (folder if folder.is_absolute() else STUDIO / folder).resolve()
    if PROJECTS not in folder.parents:
        raise SystemExit(f"{folder} is not inside {PROJECTS}")
    if (folder / "project.json").exists():
        raise SystemExit(f"{folder}/project.json already exists")
    course = folder.parent if folder.parent != PROJECTS else None
    today = date.today().isoformat()

    if course and not (course / "COURSE.md").exists():
        (course / "source").mkdir(parents=True, exist_ok=True)
        (course / "COURSE.md").write_text(
            f"# {course.name}\n\nMaterial: `source/`. Each lecture is its own project folder here.\n\n"
            "| # | Lecture | Project | State |\n|---|---|---|---|\n")
        print(f"new course: {course.relative_to(STUDIO)}/ (COURSE.md, source/)")

    for sub in ("script", "audio", "music", "scenes", "source"):
        (folder / sub).mkdir(parents=True, exist_ok=True)

    dest = course / "source" if course else folder / "source"
    sources = []
    for s in args.source:
        src = Path(s).expanduser().resolve()
        if not src.exists():
            raise SystemExit(f"no such file: {s}")
        target = dest / src.name
        if target.exists() and target != src:
            print(f"  {target.relative_to(STUDIO)} already exists: using it")
        elif STUDIO in src.parents and target != src:
            shutil.move(str(src), target)
            print(f"  moved {src.relative_to(STUDIO)} -> {target.relative_to(STUDIO)}")
        elif target != src:
            shutil.copy2(src, target)
            print(f"  copied {src} -> {target.relative_to(STUDIO)}")
        sources.append({"path": str(Path("..", "source", target.name) if course
                                    else Path("source", target.name)), "pages": "", "note": ""})

    cfg = {
        "title": args.title,
        "course_line": args.course_line,
        "code_language": args.lang,     # Pygments lexer for Code(...); "" = no code on screen
        "toolchain": "",                # how to run code examples to verify them (planner fills in)
        "sources": sources,             # planner adds pages and notes
        "created": today,
    }
    if args.style != "classic":         # auto / deep: the 1440p board and the shared teaching rules
        cfg["style"] = args.style
        cfg["resolution"] = "1440p"
        # varied pauses at 1.5x, not the house 2x (the user, 2026-11-04): with the load equalizer and
        # 3b1b-style "pause and ponder" prompts, density isn't left to silence (docs/DEEP_STYLE.md §13)
        cfg["pacing"] = {"scale": 1.5}
    (folder / "project.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    (folder / "PLAN.md").write_text(f"# {args.title}: plan\n\n(The series-planner writes this.)\n")
    (folder / "STATUS.md").write_text(f"# {args.title}: status\n\n{today}: project created; planning.\n")

    rel = folder.relative_to(PROJECTS)
    if course and f"`{folder.name}/`" not in (course / "COURSE.md").read_text():
        # Fill the lecture's existing "not started" row if the table has one; otherwise add a
        # row at the end of the table (not the end of the file, which is below the notes).
        lines = (course / "COURSE.md").read_text().splitlines()
        rows = [i for i, l in enumerate(lines) if l.startswith("|") and not l.startswith("|---")]
        hit = next((i for i in rows if [c.strip() for c in lines[i].split("|")][2:3]
                    == [args.title] and "—" in lines[i]), None)
        if hit is not None:
            num = lines[hit].split("|")[1].strip()
            lines[hit] = f"| {num} | {args.title} | `{folder.name}/` | planning ({today}) |"
        else:
            # end of the lecture table (header "| # |"), not of the file's last table: a course
            # can have other tables below it, e.g. DE's slide sections
            head = next((i for i, l in enumerate(lines) if l.startswith("| # |")), None)
            if head is not None:
                at = head + 1
                while at < len(lines) and lines[at].startswith("|"):
                    at += 1
            else:
                at = rows[-1] + 1 if rows else len(lines)
            lines.insert(at, f"| | {args.title} | `{folder.name}/` | planning ({today}) |")
        (course / "COURSE.md").write_text("\n".join(lines) + "\n")
    index = PROJECTS / "INDEX.md"
    if index.exists() and f"`{rel}`" not in index.read_text():
        lines = index.read_text().splitlines()
        rows = [i for i, l in enumerate(lines) if l.startswith("| `")]
        at = rows[-1] + 1 if rows else len(lines)
        lines.insert(at, f"| `{rel}` | {args.title} ({args.course_line}) | planning ({today}) |")
        course_md = f"{course.name}/COURSE.md" if course else None
        for i, l in enumerate(lines):
            if course_md and l.startswith("Courses:") and course_md not in l:
                lines[i] = l.rstrip(".") + f"; `{course_md}`."
        index.write_text("\n".join(lines) + "\n")
    print(f"created {folder.relative_to(STUDIO)}/  (project.json, PLAN.md, STATUS.md, "
          f"script/ audio/ music/ scenes/ source/; listed in projects/INDEX.md)")


if __name__ == "__main__":
    main()
