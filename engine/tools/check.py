"""One command to check scenes: a dry-run audit (sync, screen time, layout), a 480p15
render, and one "beats" image to look at. Replaces render → sheet → ffmpeg grabs → dwell.

    vk check ch2_s4_why [ch2_s5_poly …]    # audit + render + beats image
    vk check --chapter 2                    # every scene of a chapter
    vk check ch2_s4_why --no-render         # audit only (seconds)
    vk check ch2_s4_why --frames 12.5 40    # + full-size frames (scene time, s)
    vk check ch2_s4_why --render-anyway     # render even though the audit has flags

A scene renders (and gets its beats image and frames) only once its audit is clean: any
overrun, sync or layout flag skips the render, since those need fixing first anyway. Dwell
flags don't block it: they're often accepted, and the beats image is how to judge them.
--render-anyway overrides that, for flags the brief accepts or to look at a flagged moment.

Per scene it reports (compact on purpose, agents read it):
  error     a Python exception, as a short traceback, from the dry run (before any rendering)
  overrun   a `say` block whose animations outlast its clip (the next clip starts late)
  dwell     text removed before it could be read twice (tools/dwell.py's rule)
  layout    checked at every settled moment ("beat"): text or shapes cut off by the frame
            edge, text within 0.3 of the edge, text overlapping other text, stacked
            duplicate glyphs (a leftover copy), text smaller than 26, the scene not ending
            on an empty frame (a scene marked "# handover: next" must instead end on the
            shot the next scene opens on)
  sync      hard-coded clip times (`c.start + 4.2`) in the source
  transition  (tools/transitions.py) every play() as it runs: a text morphed into a different
            text, text revealed in pieces (Write, lag_ratio), two texts drawn over each other
            mid-transition (sampled at 25/50/75%), "~" in CMU Serif, a label up > 2 s before its
            word. Blocking in scenes marked "# style: 2" (the builder template); advice elsewhere.
            Advice in every scene: a flash/drawn box hugging one glyph (reads as an overbar).
            Advice in projects with a "style": a MathTex rewritten in place with the original no
            longer on screen (DEEP_STYLE §14: use lib.teach.derive_step).
  handover  (tools/handover.py) a scene marked "# handover: next", or the one after it: the
            marked scene's last frame against the next scene's first, from their 480p renders
            once both exist. A difference (with where it is) or an empty shared frame needs fixing.
  beats     media/check/<stem>_beats.png: one tile per settled moment (a wait of ≥ 0.6 s,
            and each clip's end), labelled "clip > next cue". That's what the viewer studies.
Exit status 1 when anything other than the image needs attention.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(ENGINE / "tools"))
from lib.paths import config, ffmpeg_text, project, rel, subprocess_env  # noqa: E402

ROOT = project()   # the project whose scenes are checked
PY = ENGINE / ".venv" / "bin" / "python"
OUT = ROOT / "media" / "check"

MARGIN = 0.3      # text closer than this to the frame edge is flagged (STYLE.md asks 0.5)
# STYLE.md: nothing smaller than 28 (auto/deep styles, docs/DEEP_STYLE.md §6: 22 at 1440p); 2 below is tolerated
MIN_FONT = 20 if config().get("style") in ("deep", "auto") else 26
OVERLAP = 0.35    # two glyphs of different texts sharing this much area (of the smaller one)
MIN_BEAT = 0.6    # a wait at least this long is a settled moment worth a tile
MAX_TILES = 28
ADVICE_MAX = 6    # advice lines printed per scene (older scenes can carry dozens); the rest as counts


def scene_class(stem):
    m = re.search(r"^class (\w+)\(NarratedScene\)", (ROOT / "scenes" / f"{stem}.py").read_text(), re.M)
    if not m:
        sys.exit(f"scenes/{stem}.py: no NarratedScene subclass")
    return m.group(1)


# ── dry-run audit (runs in a child process: it monkeypatches manim) ─────────────────────
def audit(stem):
    import numpy as np
    from contextlib import contextmanager

    import dwell
    from lib import narration
    from manim import Brace, MathTex, Tex, Text, VMobject, config
    from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath

    import handover

    src = (ROOT / "scenes" / f"{stem}.py").read_text()
    res = {"stem": stem, "cls": scene_class(stem), "error": None, "overruns": [], "dwell": [],
           "layout": [], "sync": [], "beats": [], "duration": 0.0, "narration": 0.0,
           "handover": bool(handover.MARK_RE.search(src))}
    lines = src.splitlines()
    for i, line in enumerate(code_only(src).splitlines(), 1):
        if re.search(r"\bc\.(start|end)\s*[-+]\s*[\d.(]", line):
            res["sync"].append(f"line {i}: hard-coded clip time: {lines[i - 1].strip()[:80]}")

    hw, hh = config.frame_width / 2, config.frame_height / 2
    seen_issue = {}

    def vis(m):
        try:
            s = m.get_stroke_opacity() if m.get_stroke_width() > 0 else 0.0
            return max(float(m.get_fill_opacity()), float(s))
        except Exception:
            return 1.0

    def short(t):
        t = " ".join(str(t).split())
        return t if len(t) <= 42 else t[:40] + "…"

    def issue(kind, key, where, msg):
        k = (kind, key)
        if k in seen_issue:
            seen_issue[k]["at"].add(where)
            seen_issue[k]["n"] = len(seen_issue[k]["at"])
            return
        seen_issue[k] = {"kind": kind, "where": where, "msg": msg, "n": 1, "at": {where}}

    def snapshot(scene, where):
        """Lint what is on screen right now (a settled moment)."""
        glyphs, units, done = [], {}, set()

        def walk(m, unit):
            if id(m) in done:
                return
            done.add(id(m))
            t = getattr(m, "original_text", None) or dwell.text_of(m)
            if t and isinstance(m, (Text, MathTex, Tex)):
                unit = id(m)
                units[unit] = {"desc": t, "box": None, "size": None}
                try:
                    units[unit]["size"] = float(m.font_size)
                except Exception:
                    pass
            if isinstance(m, VMobject) and len(m.points) and vis(m) >= 0.15:
                p = m.points
                b = (p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max())
                if isinstance(m, VMobjectFromSVGPath) and not isinstance(m, Brace):
                    u = unit if unit is not None else ("loose", dwell.OWNER.get(id(m), "?"), id(m))
                    if unit is None:
                        units.setdefault(u, {"desc": f"[part of] {dwell.OWNER.get(id(m), '?')}",
                                             "box": None, "size": None})
                    glyphs.append((b, u))
                    ub = units[u]["box"]
                    units[u]["box"] = b if ub is None else (min(ub[0], b[0]), min(ub[1], b[1]),
                                                           max(ub[2], b[2]), max(ub[3], b[3]))
                else:
                    covers = (b[2] - b[0]) > 1.8 * hw and (b[3] - b[1]) > 1.8 * hh
                    inside = b[2] > -hw and b[0] < hw and b[3] > -hh and b[1] < hh
                    out = max(b[2] - hw, -hw - b[0], b[3] - hh, -hh - b[1])
                    if inside and not covers and out > 0.05:
                        issue("cut off", ("shape", type(m).__name__, round(b[0], 1), round(b[1], 1)), where,
                              f"a {type(m).__name__} sticks {out:.2f} past the frame edge "
                              f"(x {b[0]:.1f}..{b[2]:.1f}, y {b[1]:.1f}..{b[3]:.1f})")
            for s in m.submobjects:
                walk(s, unit)

        for top in scene.mobjects:
            walk(top, None)

        for u, info in units.items():
            b = info["box"]
            if b is None:
                continue
            desc = short(info["desc"])
            out = max(b[2] - hw, -hw - b[0], b[3] - hh, -hh - b[1])
            inside = b[2] > -hw and b[0] < hw and b[3] > -hh and b[1] < hh
            if inside and out > 0.02:
                issue("cut off", ("text", desc), where, f"{desc!r} runs {out:.2f} past the frame edge")
            elif inside and out > -MARGIN:
                side = ["right", "left", "top", "bottom"][int(np.argmax(
                    [b[2] - hw, -hw - b[0], b[3] - hh, -hh - b[1]]))]
                issue("margin", ("text", desc), where,
                      f"{desc!r} is {-out:.2f} from the {side} edge (keep ≥ 0.5)")
            if info["size"] is not None and info["size"] < MIN_FONT:
                issue("small text", ("text", desc), where, f"{desc!r} at size {info['size']:.0f}")

        if len(glyphs) > 1:
            B = np.array([g[0] for g in glyphs], dtype=float)
            ids = {u: i for i, u in enumerate(dict.fromkeys(g[1] for g in glyphs))}
            U = np.array([ids[g[1]] for g in glyphs])
            names = {i: units[u]["desc"] for u, i in ids.items()}
            ix = np.minimum(B[:, None, 2], B[None, :, 2]) - np.maximum(B[:, None, 0], B[None, :, 0])
            iy = np.minimum(B[:, None, 3], B[None, :, 3]) - np.maximum(B[:, None, 1], B[None, :, 1])
            inter = np.clip(ix, 0, None) * np.clip(iy, 0, None)
            area = np.maximum((B[:, 2] - B[:, 0]) * (B[:, 3] - B[:, 1]), 1e-4)
            frac = inter / np.minimum(area[:, None], area[None, :])
            same = np.all(np.abs(B[:, None, :] - B[None, :, :]) < 0.01, axis=2)
            upper = np.triu(np.ones_like(same), 1)
            for i, j in zip(*np.nonzero(same & upper)):
                a, b2 = short(names[U[i]]), short(names[U[j]])
                issue("ghost", (a, b2), where, f"duplicate glyphs stacked: {a!r} / {b2!r} "
                      "(a copy left on screen, or the same object added twice)")
            hit = (frac > OVERLAP) & (U[:, None] != U[None, :]) & ~same & upper.astype(bool)
            for i, j in zip(*np.nonzero(hit)):
                a, b2 = short(names[U[i]]), short(names[U[j]])
                issue("overlap", tuple(sorted((a, b2))), where, f"{a!r} overlaps {b2!r}")

    # hooks: say() for overruns, Clip.wait_until() for settled moments
    orig_say, orig_wait = narration.NarratedScene.say, narration.Clip.wait_until
    holder = {}

    @contextmanager
    def say(self, cid, gap=None):
        holder["scene"] = self
        with orig_say(self, cid, gap) as c:
            yield c
            over = self.time - c.end
            if over > 0.05:
                res["overruns"].append((cid, over))
        res["narration"] += c.duration

    def wait_until(self, cue=None, nth=0, own_word=None):
        t0 = self.scene.time
        orig_wait(self, cue, nth, own_word)
        idle = self.scene.time - t0
        ended = cue is None and own_word is None
        if ended or idle >= MIN_BEAT:
            label = "end" if ended else (str(cue) if cue is not None
                                         else "own word of " + short(narration.label_text(own_word)))
            where = f"{self.id} > {label}"
            res["beats"].append({"cid": self.id, "label": label,
                                 "t": round(self.scene.time - self.start, 3), "idle": round(idle, 2)})
            snapshot(self.scene, where)

    narration.NarratedScene.say, narration.Clip.wait_until = say, wait_until
    # private text/LaTeX caches, the same ones tools/render.py gives this scene: parallel
    # manim processes race on the shared ones (LESSONS.md)
    config.text_dir = str(ROOT / "media" / "cache" / stem / "texts")
    config.tex_dir = str(ROOT / "media" / "cache" / stem / "Tex")
    import transitions
    res["style2"] = transitions.new_style(src)
    trans = transitions.Audit(ROOT / "scenes" / f"{stem}.py", src)
    trans.install()
    try:
        _, total, flags = dwell.audit(stem, narration.manifest())
        res["transition"] = trans.results(narration.manifest())
        res["duration"] = total
        last = res["beats"][-1]["cid"] if res["beats"] else None
        res["overruns"] = [f"{cid}: the block runs {over:.1f} s past its clip (the next clip starts "
                           "late: shorten run_times or cue earlier)"
                           for cid, over in res["overruns"] if not (cid == last and over <= 2.0)]
        for t, life, need, kind, text, clip in flags:
            res["dwell"].append(f"t={t:5.1f} {short(text)!r} shown {life:.1f}s (needs {need:.1f}) "
                                f"{kind} during {clip}")
        scene = holder.get("scene")
        if scene is not None:
            left = [m for top in scene.mobjects for m in top.family_members_with_points()
                    if isinstance(m, VMobject) and vis(m) >= 0.05]
            if left and not res["handover"]:
                issue("end", "end", "scene end", f"{len(left)} visible piece(s) left on screen "
                      "(a scene must end fully faded out, unless the next scene opens on this "
                      "shot: then mark it '# handover: next')")
            elif not left and res["handover"]:
                issue("end", "end", "scene end", "marked '# handover: next' but nothing is left on "
                      "screen: end on the shot the next scene opens on, without fading it")
    except Exception as e:
        tb = [f for f in traceback.extract_tb(e.__traceback__)
              if (str(ROOT) in f.filename or str(ENGINE / "lib") in f.filename)
              and "/tools/" not in f.filename][-3:]
        res["error"] = "".join(f"  {rel(f.filename)}:{f.lineno}  {f.line}\n"
                               for f in tb) + f"  {type(e).__name__}: {e}"[:600]
    finally:
        trans.uninstall()
        narration.NarratedScene.say, narration.Clip.wait_until = orig_say, orig_wait
    res["layout"] = [{k: v for k, v in it.items() if k != "at"} for it in seen_issue.values()]
    return res


def run_audit(stem):
    import slots
    with slots.manim(f"audit {stem}", gb=0.6):
        p = subprocess.run([str(PY), str(Path(__file__)), "--_audit", stem], cwd=ROOT,
                           env=subprocess_env(), capture_output=True, text=True)
    m = re.search(r"@@JSON@@(.*)$", p.stdout, re.S)
    if not m:
        tail = (p.stderr or p.stdout).strip().splitlines()[-8:]
        return {"stem": stem, "error": "audit crashed:\n  " + "\n  ".join(tail)}
    return json.loads(m.group(1))


# ── render + images ──────────────────────────────────────────────────────────────────────
def log_tail(log):
    lines = [re.sub(r"[│╭╮╰╯─┃━]+", " ", l).rstrip() for l in Path(log).read_text().splitlines()]
    lines = [l.strip() for l in lines if l.strip()]
    return "\n  ".join(lines[-8:])


def grab(video, t, out, width, label=None):
    vf, ff = f"scale={width}:-1", "ffmpeg"
    if label:
        ff, dt = ffmpeg_text()   # an ffmpeg with drawtext (lib/paths.py)
        safe = re.sub(r"[^A-Za-z0-9 ._>=-]", " ", label)[:44]
        vf += (f",{dt}text='{safe}':x=6:y=h-22:fontcolor=white:fontsize=14:"
               "box=1:boxcolor=black@0.65")
    subprocess.run([ff, "-v", "error", "-y", "-ss", f"{max(0.0, t):.3f}", "-i", str(video),
                    "-frames:v", "1", "-vf", vf, str(out)], check=True)


def tile(pngs, out, cols):
    rows = (len(pngs) + cols - 1) // cols
    with tempfile.TemporaryDirectory() as tmp:
        for i, p in enumerate(pngs):
            os.link(p, Path(tmp) / f"{i:03d}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", f"{tmp}/%03d.png",
                        "-vf", f"tile={cols}x{rows}:padding=4:color=white", "-frames:v", "1",
                        str(out)], check=True)


def beats_image(res, video, cues):
    starts = {c["id"]: c["start"] for c in cues["clips"]}
    beats = [b for b in res["beats"] if b["cid"] in starts]
    if len(beats) > MAX_TILES:   # keep every clip end, then the longest holds
        ends = [b for b in beats if b["label"] == "end"]
        rest = sorted((b for b in beats if b["label"] != "end"), key=lambda b: -b["idle"])
        keep = {id(b) for b in ends + rest[:max(0, MAX_TILES - len(ends))]}
        beats = [b for b in beats if id(b) in keep]
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        pngs = []
        for i, b in enumerate(beats):
            t = starts[b["cid"]] + b["t"] - 0.1
            short_id = b["cid"].split(".", 1)[-1]
            p = Path(tmp) / f"{i:03d}.png"
            grab(video, t, p, 427, f"{short_id} > {b['label']}  {t:.1f}s")
            pngs.append(p)
        out = OUT / f"{res['stem']}_beats.png"
        tile(pngs, out, 4)
    return out, len(beats)


def frames_image(stem, video, times):
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        pngs = []
        for i, t in enumerate(times):
            p = Path(tmp) / f"{i:03d}.png"
            grab(video, t, p, 854, f"t={t:.1f}s")
            pngs.append(p)
        out = OUT / f"{stem}_frames.png"
        tile(pngs, out, 2 if len(times) > 1 else 1)
    return out


# ── report ───────────────────────────────────────────────────────────────────────────────
def code_only(src):
    """src with string literals and comments blanked (line numbers kept), so the sync lint doesn't
    flag on-screen text like "c.start + 4.2" (studio-tour ch1_s7)."""
    import io
    import tokenize
    rows = [list(line) for line in src.splitlines(True)]
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type not in (tokenize.STRING, tokenize.COMMENT) and \
                    tok.type != getattr(tokenize, "FSTRING_MIDDLE", -1):
                continue
            (sr, sc), (er, ec) = tok.start, tok.end
            for r in range(sr, er + 1):
                row = rows[r - 1]
                for k in range(sc if r == sr else 0, min(ec if r == er else len(row), len(row))):
                    if row[k] != "\n":
                        row[k] = " "
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return src
    return "".join("".join(r) for r in rows)


def joins(stem):
    """Handover checks for a freshly rendered scene: the join into the next scene when this one is
    marked "# handover: next", and the join from the previous scene when that one is. A list of
    (ok, message)."""
    import handover
    m = re.match(r"ch(\d+)_", stem)
    if not m:
        return []
    order = [p.stem for p in sorted((ROOT / "scenes").glob(f"ch{m.group(1)}_*.py"))]
    i = order.index(stem)
    out, pairs = [], []
    if i > 0 and handover.marked(ROOT / "scenes" / f"{order[i - 1]}.py"):
        pairs.append((order[i - 1], stem))
    if handover.marked(ROOT / "scenes" / f"{stem}.py"):
        if i + 1 < len(order):
            pairs.append((stem, order[i + 1]))
        else:
            out.append((False, f"{stem} is marked '# handover: next' but is the chapter's last scene"))
    for a, b in pairs:
        other = b if a == stem else a
        va, vb = (ROOT / "media" / "videos" / s / "480p15" / f"{scene_class(s)}.mp4" for s in (a, b))
        if not (va.exists() and vb.exists()):
            out.append((True, f"{a} → {b}: not compared yet, {other} has no 480p render "
                              f"(vk check {other})"))
            continue
        ok, msg = handover.check_join(a, va, b, vb)
        if handover.stale(other, va if other == a else vb, ROOT):
            msg += f" ({other}'s render is older than its file: vk check {other} again)"
        out.append((ok, msg))
    return out


def blocking_transitions(res):
    """The transition items that block: all of them in a "# style: 2" scene (the overlap rule only
    while transitions.OVERLAP_BLOCKS), none in older scenes, where they are advice."""
    import transitions
    if not res.get("style2"):
        return []
    return [it for it in res.get("transition", []) if it["rule"] not in transitions.ADVICE_ONLY
            and (it["rule"] != "overlap" or transitions.OVERLAP_BLOCKS)]


def flagged(res):
    """True when the audit found a must-fix flag. Dwell is left out: it is often accepted on
    purpose (6 of 7 finished l04 ch1 scenes carry one), and the beats image is how to judge it."""
    return any(res.get(k) for k in ("overruns", "sync", "layout")) or bool(blocking_transitions(res))


def report(res, rendered, args, skipped=False):
    stem = res["stem"]
    bad = 0
    head = f"{stem} ({res.get('cls', '?')})"
    if res.get("error"):
        print(f"{head}: ERROR in the dry run\n{res['error']}")
        return 1
    print(f"{head}: {res['duration']:.1f} s (narration {res['narration']:.1f} s, "
          f"{len({b['cid'] for b in res['beats']})} clips)")
    if rendered is not None:
        ok, took, log = rendered[:3]
        if not ok:
            print(f"  render FAILED ({log.relative_to(ROOT)}):\n  {log_tail(log)}")
            bad += 1
    for key, title in (("overruns", "overrun"), ("dwell", "dwell"), ("sync", "sync")):
        for line in res[key]:
            print(f"  {title}: {line}")
            bad += 1
    for it in res["layout"]:
        more = f" (and {it['n'] - 1} later beat(s))" if it["n"] > 1 else ""
        print(f"  {it['kind']}: [{it['where']}] {it['msg']}{more}")
        bad += 1
    block = blocking_transitions(res)
    for it in block:
        print(f"  transition {it['msg']}")
        bad += 1
    advice = [it for it in res.get("transition", []) if it not in block]
    for it in advice[:ADVICE_MAX]:
        print(f"  advice ({'not blocking: no # style: 2' if not res.get('style2') else 'not blocking'}): "
              f"{it['msg']}")
    if len(advice) > ADVICE_MAX:
        from collections import Counter
        more = Counter(it["rule"] for it in advice[ADVICE_MAX:])
        print(f"  advice: … and {len(advice) - ADVICE_MAX} more ("
              + ", ".join(f"{n} {r}" for r, n in more.most_common()) + ")")
    for ok, msg in res.get("joins", []):
        print(f"  handover: {msg}")
        bad += 0 if ok else 1
    if not bad:
        print("  clean: no overruns, dwell flags, layout or transition issues"
              + (f" ({len(advice)} advice)" if advice else ""))
    if skipped:
        what = "render, beats image and frames" if args.frames else "render and beats image"
        print(f"  {what} skipped until the audit is clean (--render-anyway to render with these flags)")
    for line in rendered[3:] if rendered and len(rendered) > 3 else ():
        print(f"  {line}")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stems", nargs="*")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--frames", nargs="*", type=float, default=[])
    ap.add_argument("--render-anyway", action="store_true",
                    help="render scenes whose audit has flags (skipped by default)")
    ap.add_argument("--_audit")
    args = ap.parse_args()

    if args._audit:
        res = audit(args._audit)
        print("@@JSON@@" + json.dumps(res, default=float))
        return

    stems = list(args.stems)
    if args.chapter:
        stems += [p.stem for p in sorted((ROOT / "scenes").glob(f"ch{args.chapter}_*.py"))]
    if not stems:
        ap.error("give scene stems or --chapter N")
    for s in stems:
        if not (ROOT / "scenes" / f"{s}.py").exists():
            sys.exit(f"no scenes/{s}.py")

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        audits = list(pool.map(run_audit, stems))
    rendered = {}
    todo, skipped = [], set()
    if not args.no_render:
        for r in audits:
            if r.get("error"):
                continue   # a Python error: nothing to render
            if flagged(r) and not args.render_anyway:
                skipped.add(r["stem"])   # fix the audit first; the image would be redone anyway
            else:
                todo.append(r)
    if todo:
        os.environ["COLUMNS"] = "400"   # manim's rich logs wrap otherwise
        import render as R
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
            for stem, rc, took, log in pool.map(lambda r: R.render(r["stem"], r["cls"], "-ql"), todo):
                rendered[stem] = [rc == 0, took, log]
        for r in todo:
            ok, took, log = rendered[r["stem"]]
            if not ok:
                continue
            video = ROOT / "media" / "videos" / r["stem"] / "480p15" / f"{r['cls']}.mp4"
            cues = json.loads((ROOT / "media" / "cues" / f"{r['stem']}_480p15.json").read_text())
            img, n = beats_image(r, video, cues)
            rendered[r["stem"]].append(f"beats: {img.relative_to(ROOT)} ({n} tiles, "
                                       f"video {cues['duration']:.1f} s, rendered in {took:.0f} s)")
            if args.frames:
                f = frames_image(r["stem"], video, args.frames)
                rendered[r["stem"]].append(f"frames: {f.relative_to(ROOT)}")
        for r in todo:
            if rendered[r["stem"]][0]:
                r["joins"] = joins(r["stem"])
    status = 0
    for r in audits:
        status |= report(r, rendered.get(r["stem"]), args, r["stem"] in skipped)
    print(f"({time.time() - t0:.0f} s)")
    sys.exit(status)


if __name__ == "__main__":
    main()
