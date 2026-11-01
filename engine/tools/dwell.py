"""Screen-time audit: flag text that is faded out before it could be read.

Runs each scene of a chapter in manim's dry-run mode (nothing is rendered, takes seconds),
records when every piece of text first appears, and when a FadeOut/Uncreate/Unwrite
removes it. Anything removed sooner than MIN_BASE + chars/CHARS_PER_S seconds after it
appeared is flagged, with the narration words being spoken at that moment.

    vk dwell --chapter 1 [--only ch1_s2_what]

Not every flag is a bug: a wrong guess crossed out on purpose may be brief. But anything
that is a *result* or a *fact* the viewer should absorb should stay (LESSONS.md, STYLE.md).
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import project  # noqa: E402

ROOT = project()   # the project folder (script/, audio/, scenes/, media/, …)

MIN_BASE = 4.0      # seconds every piece of text gets at least
CHARS_PER_S = 12.0  # plus reading time (read twice at a relaxed pace)
CLEARING = {"FadeOut", "Uncreate", "Unwrite", "ShrinkToCenter", "FadeOutAndShift"}


def text_of(m):
    for attr in ("text", "tex_string", "src"):
        v = getattr(m, attr, None)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


OWNER = {}  # glyph id -> text of the Text/Code it came from (filled as mobjects appear)


def is_glyph(m):
    from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
    return isinstance(m, VMobjectFromSVGPath)


def text_pieces(mob):
    """(description, members) for the text in a family. Whole text objects are reported
    by their string; loose glyphs (e.g. code.find(...) slices) by the text they came from."""
    out, seen = [], set()
    for m in mob.get_family():
        t = text_of(m)
        if t and id(m) not in seen:
            fam = m.get_family()
            out.append((t, fam))
            seen.update(id(x) for x in fam)
    loose = {}
    for m in mob.get_family():
        if id(m) not in seen and is_glyph(m):
            loose.setdefault(OWNER.get(id(m), "?"), []).append(m)
    for owner, glyphs in loose.items():
        out.append((f"[part of] {owner}", glyphs))
    return out


def clearing_targets(anims):
    from manim import Animation, AnimationGroup
    found = []
    for a in anims:
        if getattr(a, "dwell_exempt", False):   # lib.moves.derive's in-between copy: read on its source line
            continue
        if isinstance(a, AnimationGroup):
            found += clearing_targets(a.animations)
        elif isinstance(a, Animation) and type(a).__name__ in CLEARING:
            found.append((type(a).__name__, a.mobject))
    return found


def audit(stem, manifest):
    from manim import Scene, tempconfig
    path = ROOT / "scenes" / f"{stem}.py"
    cls_name = re.search(r"^class (\w+)\(NarratedScene\)", path.read_text(), re.M).group(1)
    first_seen, flags = {}, []

    def remember(scene):
        for top in scene.mobjects:
            for m in top.get_family():
                first_seen.setdefault(id(m), scene.time)
                t = text_of(m)
                if t:
                    for g in m.get_family():
                        OWNER.setdefault(id(g), t)

    orig_add, orig_play = Scene.add, Scene.play
    in_play = [False]

    def add(self, *mobs):
        r = orig_add(self, *mobs)
        if not in_play[0]:      # inside a play(), text counts from when the play ends
            remember(self)
        return r

    def play(self, *args, **kwargs):
        from manim.animation.animation import prepare_animation
        anims = [prepare_animation(a) for a in args if not isinstance(a, dict)]
        for kind, mob in clearing_targets(anims):
            for desc, members in text_pieces(mob):
                born = min((first_seen.get(id(m), self.time) for m in members), default=self.time)
                life = self.time - born
                shown = len(desc) if not desc.startswith("[part of]") else len(members)
                need = MIN_BASE + shown / CHARS_PER_S   # reading time for what's on screen
                if life < need:
                    flags.append((self.time, life, need, kind, desc, self._clip_now()))
        in_play[0] = True
        try:
            r = orig_play(self, *args, **kwargs)
        finally:
            in_play[0] = False
        remember(self)   # newly shown text is "settled" (readable) from here
        return r

    # remember which text every glyph belongs to, even if only slices reach the screen
    from manim import MathTex, Tex, Text
    originals = {}
    for klass in (Text, MathTex, Tex):
        originals[klass] = klass.__init__

        def init(self, *a, __orig=klass.__init__, **k):
            __orig(self, *a, **k)
            t = text_of(self)
            if t:
                for g in self.get_family():
                    OWNER.setdefault(id(g), t)
        klass.__init__ = init

    spec = importlib.util.spec_from_file_location(stem, path)
    module = importlib.util.module_from_spec(spec)
    Scene.add, Scene.play = add, play
    try:
        with tempconfig({"dry_run": True, "disable_caching": True, "quality": "low_quality",
                         "media_dir": str(ROOT / "media"), "verbosity": "ERROR",
                         "progress_bar": "none"}):
            spec.loader.exec_module(module)
            cls = getattr(module, cls_name)
            state = {"cid": None, "start": 0.0}
            base_say = cls.say

            from contextlib import contextmanager

            @contextmanager
            def say(self, cid, gap=None):
                state.update(cid=cid, start=self.time)
                with base_say(self, cid, gap) as c:
                    yield c

            def clip_now(self):
                cid = state["cid"]
                if not cid:
                    return ""
                t = self.time - state["start"]
                words = [w for w, s in manifest[cid]["words"] if s <= t][-4:]
                return f'{cid} @{t:4.1f}s "…{" ".join(words)}"'

            cls.say, cls._clip_now = say, clip_now
            scene = cls()
            scene.render()
            total = scene.time
    finally:
        Scene.add, Scene.play = orig_add, orig_play
        for klass, init in originals.items():
            klass.__init__ = init
    return cls_name, total, flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    n = 0
    for path in sorted((ROOT / "scenes").glob(f"ch{args.chapter}_*.py")):
        if args.only and path.stem not in args.only:
            continue
        cls, total, flags = audit(path.stem, manifest)
        print(f"\n{path.stem} ({cls}, {total:.0f}s): {len(flags)} flagged")
        for t, life, need, kind, text, clip in flags:
            short = " ".join(text.split())[:48]
            print(f"  t={t:6.1f}  on screen {life:4.1f}s (needs {need:3.1f})  {kind:<8} {short!r:<52} {clip}")
        n += len(flags)
    print(f"\n{n} piece(s) of text removed before they could be read twice")


if __name__ == "__main__":
    main()
