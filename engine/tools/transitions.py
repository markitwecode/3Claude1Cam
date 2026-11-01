"""vk check's transition audit (glitch study 2026-10-28, docs/glitch-study-2026-10-28.md).

Gemini reviews showed that most visible glitches are brief jumbles *between* settled frames, which the
layout lint (settled moments only) can't see. This audit watches every play() of the dry run:

  morph    a Transform-family animation turns one text into a different one (glyph outlines are
           interpolated into each other: letter salad)  -> swap / edit / fly
  partial  text revealed in pieces: Write/Create/DrawBorderThenFill/AddTextLetterByLetter on text,
           or lag_ratio across one text's letters (half-words on screen)  -> appear
  overlap  sampled every 10% of the play, with moving glyphs interpolated between samples (a copy
           crossing a table partway along its path, DE L6 ch3 s3): two different texts drawn over
           each other (doubled copies, old text ghosting under new, glyphs crossing) that overlap
           neither before nor after the play  -> fly / derive / swap / during, or another path
  tilde    a CMU Serif text with ASCII "~" (a raised accent in that font; T() converts it)
  early    a prose label that starts to appear more than EARLY_S before its own word is spoken
           -> c.wait_until(own_word=label); opt out with a "# early: <reason>" comment on the line
  flashbox (advice only, any scene) a flash or drawn box hugging a single letter or digit: its top
           edge reads as an overbar (NOT in a logic course)  -> FlashAround (it rings one glyph)

Scenes marked "# style: 2" (the builder template's line) get these as blocking flags; other scenes
get them as advice, so a fix pass on an older scene doesn't turn into a rewrite. The overlap rule
blocks only when OVERLAP_BLOCKS is set (calibration notes below).
"""
import re
import sys
from contextlib import contextmanager

import numpy as np

STYLE_RE = re.compile(r"^#\s*style:\s*2\b", re.M)
SAMPLES = tuple(round(0.1 * k, 1) for k in range(1, 10))   # each play inspected every 10% (overlap)
SUBSTEPS = (1 / 3, 2 / 3)     # moving glyphs' boxes interpolated between samples, so no crossing slips by
ADVICE_ONLY = {"flashbox"}    # never blocking, in any scene
MIN_OP = 0.3                  # a glyph fainter than this doesn't count as drawn over another
OVERLAP = 0.35                # share of the smaller glyph box (the layout lint's threshold)
EARLY_S = 2.0                 # a label up this long before its word is flagged
MAX_LABEL_WORDS = 6           # longer texts (sentences, quotes) are read over time: not checked
OVERLAP_BLOCKS = True         # set by the 2026-10-28 calibration (see LESSONS.md)
FIX = {"morph": "use swap() or edit() (fly() for a copy)", "partial": "use appear()",
       "flashbox": "use FlashAround (it rings a one-glyph target) or a colour pulse",
       "tilde": "build it with T()", "early": "cue it with c.wait_until(own_word=label)"}


def new_style(src):
    return bool(STYLE_RE.search(src))


def _short(t, n=34):
    t = " ".join(str(t).split())
    return t if len(t) <= n else t[:n - 1] + "…"


class Audit:
    def __init__(self, scene_file, src):
        self.file = str(scene_file)
        self.lines = src.splitlines()
        self.items, self._keys = [], set()
        self.cur, self.cid = None, None
        self.clips, self.labels, self._label_ids = [], [], set()

    # ── install / remove the hooks ──────────────────────────────────────────────
    def install(self):
        from manim import Scene
        from lib import narration
        self._orig = (Scene.play, Scene.get_time_progression, Scene.update_to_time,
                      narration.NarratedScene.say)
        orig_play, orig_gtp, orig_utt, orig_say = self._orig
        audit = self

        def play(scene, *args, **kwargs):
            return audit._play(orig_play, scene, *args, **kwargs)

        def gtp(scene, run_time, description, n_iterations=None, override_skip_animations=False):
            if audit.cur is not None and scene.renderer.skip_animations and not override_skip_animations:
                return [f * run_time for f in SAMPLES] + [run_time]
            return orig_gtp(scene, run_time, description, n_iterations, override_skip_animations)

        def utt(scene, t):
            orig_utt(scene, t)
            cur = audit.cur
            if cur is not None and scene.duration and t < scene.duration - 1e-9:
                frac = t / scene.duration      # the dry run steps every frame: sample the first past each mark
                due = [f for f in SAMPLES if f <= frac + 1e-9 and f not in cur["done"]]
                if due:
                    cur["done"].update(due)
                    audit._sample(scene, frac)

        @contextmanager
        def say(scene, cid, gap=None):
            audit.clips.append((cid, scene.time))
            audit.cid = cid
            with orig_say(scene, cid, gap) as c:
                yield c

        Scene.play, Scene.get_time_progression, Scene.update_to_time = play, gtp, utt
        narration.NarratedScene.say = say

    def uninstall(self):
        from manim import Scene
        from lib import narration
        Scene.play, Scene.get_time_progression, Scene.update_to_time, narration.NarratedScene.say = self._orig

    # ── helpers ─────────────────────────────────────────────────────────────────
    def _add(self, rule, line, msg, key=None):
        k = (rule, line, key)
        if k in self._keys:
            return
        self._keys.add(k)
        where = f"{self.cid or 'before the first clip'} line {line}" if line else (self.cid or "?")
        self.items.append({"rule": rule, "line": line, "msg": f"{rule}: {where}: {msg}"})

    def _caller(self):
        f, helper = sys._getframe(2), None
        while f is not None:
            if f.f_code.co_filename == self.file:
                return f.f_lineno, helper
            if "/engine/lib/" in f.f_code.co_filename and helper is None:
                helper = f.f_code.co_name
            f = f.f_back
        return None, helper

    @staticmethod
    def _glyphs(mob):
        from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
        if mob is None:
            return []
        return [m for m in mob.family_members_with_points() if isinstance(m, VMobjectFromSVGPath)]

    @staticmethod
    def _textlike(m):
        from manim import MathTex, SingleStringMathTex, Tex, Text
        return isinstance(m, (Text, MathTex, SingleStringMathTex, Tex)) or type(m).__name__ == "Code"

    def _name(self, mob):
        import dwell
        for attr in ("original_text", "src", "tex_string"):
            v = getattr(mob, attr, None)
            if isinstance(v, str):
                return _short(v)
        for g in self._glyphs(mob):
            if id(g) in dwell.OWNER:
                return "part of " + _short(dwell.OWNER[id(g)], 28)
        return type(mob).__name__

    @staticmethod
    def _walk(a):
        from manim import AnimationGroup
        yield a
        if isinstance(a, AnimationGroup):
            for s in a.animations:
                yield from Audit._walk(s)

    # ── play() ──────────────────────────────────────────────────────────────────
    def _play(self, orig_play, scene, *args, **kwargs):
        from manim import Wait
        from manim.animation.animation import prepare_animation
        if self.cur is not None or not args:
            return orig_play(scene, *args, **kwargs)
        anims = [prepare_animation(a) for a in args if not isinstance(a, dict)]
        if all(isinstance(a, Wait) for a in anims):
            return orig_play(scene, *anims, **kwargs)
        line, helper = self._caller()
        self._static(anims, line, helper, scene)
        before = self._texts_on(scene)
        start, start_boxes = self._pairs(scene)
        self.cur = {"line": line, "helper": helper, "mid": {}, "done": set(), "start": start,
                    "start_boxes": start_boxes}
        t0 = scene.time
        try:
            r = orig_play(scene, *anims, **kwargs)
            end, _ = self._pairs(scene)
            for pair, (frac, desc) in self.cur["mid"].items():
                if pair not in self.cur["start"] and pair not in end:
                    a, b = desc
                    hint = ("a copy drawn over its source (doubled text): fly()/derive()" if a == b
                            else "old and new overlap mid-move: clear first (swap/during) or move another way")
                    self._add("overlap", line, f"@ {int(frac * 100)}%: {a!r} runs over {b!r} ({hint})",
                              key=pair)
                    break
            self._new_labels(scene, before, anims, t0, scene.time - t0, line)
        finally:
            self.cur = None
        return r

    def _static(self, anims, line, helper, scene=None):
        """morph, partial and flashbox: read off the animation objects (exact)."""
        import dwell
        from manim import AnimationGroup, FadeTransform, Transform, TransformFromCopy
        from manim.animation.creation import DrawBorderThenFill, ShowIncreasingSubsets, ShowPartial
        from manim.animation.fading import _Fade
        from lib.moves import glyph_classes
        via = f" (via {helper})" if helper else ""
        for top in anims:
            for a in self._walk(top):
                name = type(a).__name__
                if isinstance(a, Transform) and not isinstance(a, (_Fade, FadeTransform)):
                    tgt = getattr(a, "target_mobject", None)
                    if name == "MoveToTarget":           # its target is the generated .target
                        tgt = getattr(a.mobject, "target", None)
                    # .animate / ApplyMethod / Restore build their target at begin(): until then it is
                    # an empty placeholder (and they keep the glyphs anyway)
                    if tgt is None or not tgt.family_members_with_points():
                        continue
                    g1, g2 = self._glyphs(a.mobject), self._glyphs(tgt)
                    if not g1 and not g2:
                        continue
                    k1, k2 = glyph_classes(g1, g2)
                    if len(g1) != len(g2) or k1 != k2:
                        src, dst = (tgt, a.mobject) if isinstance(a, TransformFromCopy) or name == "_FlyCopy" \
                            else (a.mobject, tgt)
                        a_, b_ = self._name(src), self._name(dst)
                        why = "same text in another font: the outlines morph" if a_ == b_ else "letters scramble"
                        self._add("morph", line, f"{name} morphs {a_!r} into {b_!r} ({why}){via}: {FIX['morph']}",
                                  key=(id(src), id(dst)))
                elif isinstance(a, (DrawBorderThenFill, ShowPartial, ShowIncreasingSubsets)) and "Flash" not in name:
                    if self._glyphs(a.mobject):
                        self._add("partial", line, f"{name} draws {self._name(a.mobject)!r} stroke by stroke "
                                  f"(half-drawn glyphs){via}: {FIX['partial']}", key=id(a.mobject))
                elif isinstance(a, _Fade) and a.lag_ratio > 0:
                    texts = [m for m in a.mobject.get_family() if self._textlike(m) and len(self._glyphs(m)) >= 2]
                    if texts:
                        self._add("partial", line, f"{name} with lag_ratio={a.lag_ratio:g} reveals "
                                  f"{self._name(texts[0])!r} letter by letter{via}: {FIX['partial']}",
                                  key=id(a.mobject))
                elif isinstance(a, AnimationGroup) and a.lag_ratio > 0:
                    owners = {}
                    for s in a.animations:
                        if not isinstance(s, (_Fade, DrawBorderThenFill, ShowPartial)):
                            continue
                        gs = self._glyphs(s.mobject)
                        if gs and len(gs) == len(s.mobject.family_members_with_points()) and len(gs) <= 3:
                            o = dwell.OWNER.get(id(gs[0]))
                            if o:
                                owners[o] = owners.get(o, 0) + 1
                    hit = [o for o, n in owners.items() if n >= 2 and len(o.replace(" ", "")) > 3]
                    if hit:
                        self._add("partial", line, f"{name} over single letters of {_short(hit[0])!r} "
                                  f"(letter by letter){via}: {FIX['partial']}", key=(id(a), hit[0]))
                if scene is not None:
                    self._flashbox(a, name, scene, line, via)

    def _flashbox(self, a, name, scene, line, via):
        """A travelling flash or a drawn box round one letter or digit shows its top edge first,
        right above the glyph: it reads as an overbar (3 times in DE L6). FlashAround now rings
        such targets; this catches boxes built by hand."""
        from manim import Rectangle
        from manim.animation.creation import ShowPartial
        box = None
        if getattr(a, "source_kind", "") in ("Rectangle", "SurroundingRectangle", "RoundedRectangle", "Square"):
            box = a.mobject                                    # FlashAround / VShowPassingFlash on a box path
        elif isinstance(a, ShowPartial) and isinstance(a.mobject, Rectangle) \
                and float(a.mobject.get_fill_opacity()) < 0.5:
            box = a.mobject                                    # Create / ShowPassingFlash / Circumscribe's frame
        if box is None or not box.family_members_with_points():
            return
        x0, x1, y0, y1 = box.get_left()[0], box.get_right()[0], box.get_bottom()[1], box.get_top()[1]
        g = self._glyph_list(scene)
        if not g:
            return
        B, ok = self._boxes(g)
        V = self._vis(g)
        cx, cy = (B[:, 0] + B[:, 2]) / 2, (B[:, 1] + B[:, 3]) / 2
        inside = ok & (V >= MIN_OP) & (cx > x0) & (cx < x1) & (cy > y0) & (cy < y1)
        idx = np.nonzero(inside)[0]
        units = {g[i][1] for i in idx}
        if 0 < len(idx) <= 2 and len(units) == 1 and y1 - B[idx, 3].max() < 0.35:
            # a glyph inside its own frame (a table cell, a node): the flash runs outside that frame,
            # so it reads as a box, not as a bar on the glyph
            from manim import VMobject
            from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
            gx0, gy0, gx1, gy1 = B[idx, 0].min(), B[idx, 1].min(), B[idx, 2].max(), B[idx, 3].max()
            garea, own = max((gx1 - gx0) * (gy1 - gy0), 1e-4), {id(m) for m in box.get_family()}
            for top in scene.mobjects:
                for m in top.family_members_with_points():
                    # non-vector members (a ValueTracker keeps its value as a point) have no stroke
                    if (not isinstance(m, VMobject) or isinstance(m, VMobjectFromSVGPath) or id(m) in own
                            or m.get_stroke_width() <= 0):
                        continue
                    if float(m.get_stroke_opacity()) < MIN_OP:
                        continue
                    mx0, mx1, my0, my1 = m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]
                    if (mx0 > x0 - 0.05 and mx1 < x1 + 0.05 and my0 > y0 - 0.05 and my1 < y1 + 0.05
                            and mx0 <= gx0 and mx1 >= gx1 and my0 <= gy0 and my1 >= gy1
                            and (mx1 - mx0) * (my1 - my0) >= 2 * garea):
                        return
            self._add("flashbox", line, f"{name} draws a box hugging the single glyph {g[idx[0]][2]!r} "
                      f"(its top edge reads as an overbar){via}: {FIX['flashbox']}", key=id(box))

    # ── overlap sampling ────────────────────────────────────────────────────────
    def _glyph_list(self, scene):
        """[(glyph, unit key, name)] for every glyph with points on screen, visible or not, in draw
        order. The unit is the text it belongs to: overlaps within one text don't count."""
        import dwell
        from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
        out, done = [], set()

        def walk(m, unit, name):
            if id(m) in done:
                return
            done.add(id(m))
            if self._textlike(m):
                unit, name = id(m), self._name(m)
            if isinstance(m, VMobjectFromSVGPath) and len(m.points):
                u, nm = unit, name
                if u is None:
                    o = dwell.OWNER.get(id(m))
                    u, nm = (("owner", o), _short(o)) if o else (id(m), "a glyph")
                out.append((m, u, nm))
            for s in m.submobjects:
                walk(s, unit, name)

        for top in scene.mobjects:
            walk(top, None, None)
        return out

    @staticmethod
    def _boxes(g):
        """(n x 4 boxes x0 y0 x1 y1, mask of glyphs that have points), vectorised."""
        pts = [m.points for m, _, _ in g]
        n = np.array([len(p) for p in pts])
        B, ok = np.zeros((len(pts), 4)), n > 0
        if ok.any():
            P = np.concatenate([p[:, :2] for p in pts if len(p)])
            st = np.concatenate([[0], np.cumsum(n[ok])[:-1]])
            B[ok, 0], B[ok, 1] = np.minimum.reduceat(P[:, 0], st), np.minimum.reduceat(P[:, 1], st)
            B[ok, 2], B[ok, 3] = np.maximum.reduceat(P[:, 0], st), np.maximum.reduceat(P[:, 1], st)
        return B, ok

    @staticmethod
    def _vis(g):
        out = np.empty(len(g))
        for i, (m, _, _) in enumerate(g):
            try:
                s = m.get_stroke_opacity() if m.get_stroke_width() > 0 else 0.0
                out[i] = max(float(m.get_fill_opacity()), float(s))
            except Exception:
                out[i] = 1.0
        return out

    @staticmethod
    def _hits(B, U, rows, cols):
        """Index pairs (row glyph, col glyph) of different units whose boxes overlap > OVERLAP."""
        if not len(rows) or not len(cols):
            return []
        R, C = B[rows], B[cols]
        ix = np.minimum(R[:, None, 2], C[None, :, 2]) - np.maximum(R[:, None, 0], C[None, :, 0])
        iy = np.minimum(R[:, None, 3], C[None, :, 3]) - np.maximum(R[:, None, 1], C[None, :, 1])
        inter = np.clip(ix, 0, None) * np.clip(iy, 0, None)
        ar = np.maximum((R[:, 2] - R[:, 0]) * (R[:, 3] - R[:, 1]), 1e-4)
        ac = np.maximum((C[:, 2] - C[:, 0]) * (C[:, 3] - C[:, 1]), 1e-4)
        frac = inter / np.minimum(ar[:, None], ac[None, :])
        hit = (frac > OVERLAP) & (U[rows][:, None] != U[cols][None, :])
        return [(rows[i], cols[j]) for i, j in zip(*np.nonzero(hit))]

    def _pairs(self, scene):
        """({frozenset(unit a, unit b): (a name, b name)} for texts overlapping now,
        {glyph id: box} of the visible glyphs)."""
        g = self._glyph_list(scene)
        if not g:
            return {}, {}
        B, ok = self._boxes(g)
        vis = np.nonzero(ok & (self._vis(g) >= MIN_OP))[0]
        U = np.array([hash(u) for _, u, _ in g])
        out = {}
        for i, j in self._hits(B, U, vis, vis):
            out.setdefault(frozenset((g[i][1], g[j][1])), (g[i][2], g[j][2]))
        return out, {id(g[i][0]): B[i].copy() for i in vis}

    def _sample(self, scene, frac):
        """Overlaps of the glyphs that moved or appeared since the play began (the rest can't
        newly overlap), at this frame and at SUBSTEPS between it and the previous sample."""
        cur = self.cur
        if "glyphs" not in cur:      # the play's objects are all on screen from its first frame
            cur["glyphs"] = self._glyph_list(scene)
            cur["U"] = np.array([hash(u) for _, u, _ in cur["glyphs"]])
        g, U = cur["glyphs"], cur["U"]
        if not g:
            return
        B, ok = self._boxes(g)
        vis = ok & (self._vis(g) >= MIN_OP)
        sb = cur["start_boxes"]
        moved = np.array([id(m) not in sb or np.abs(B[i] - sb[id(m)]).max() > 0.01 for i, (m, _, _) in enumerate(g)])
        rows, cols = np.nonzero(vis & moved)[0], np.nonzero(vis)[0]
        steps = [(frac, B)]
        prev = cur.get("prev")
        if prev is not None:
            pf, PB = prev
            steps += [(pf + (frac - pf) * f, PB + (B - PB) * f) for f in SUBSTEPS]
        for at, Bf in steps:
            for i, j in self._hits(Bf, U, rows, cols):
                cur["mid"].setdefault(frozenset((g[i][1], g[j][1])), (at, (g[i][2], g[j][2])))
        cur["prev"] = (frac, B)

    # ── labels: tilde and early ─────────────────────────────────────────────────
    def _texts_on(self, scene):
        from manim import Text
        out = {}
        for top in scene.mobjects:
            for m in top.get_family():
                if isinstance(m, Text) and getattr(m, "font", "") == "CMU Serif" and m.original_text.strip():
                    g = m.family_members_with_points()
                    if g and max(float(x.get_fill_opacity()) for x in g) > MIN_OP:
                        out[id(m)] = m
        return out

    def _new_labels(self, scene, before, anims, t0, dur, line):
        spans = {}
        for top in anims:
            for a in self._walk(top):
                st = None
                if getattr(a, "abs_span", None):
                    st = a.abs_span[0]
                elif getattr(a, "rel_span", None):
                    st = a.rel_span[0] * dur
                if st and getattr(a, "mobject", None) is not None:
                    for m in a.mobject.get_family():
                        spans.setdefault(id(m), st)
        for i, m in self._texts_on(scene).items():
            if i in before or i in self._label_ids:
                continue
            self._label_ids.add(i)
            if "~" in m.original_text:
                self._add("tilde", line, f"{_short(m.original_text)!r} has an ASCII '~' in CMU Serif (a raised "
                          f"accent): {FIX['tilde']}", key=i)
            st = next((spans[id(x)] for x in [m, *m.get_family()] if id(x) in spans), 0.0)
            self.labels.append((m, t0 + st, self.cid, line))

    def results(self, manifest):
        """All items, with the early-label rule applied (needs the whole run's clip times)."""
        from lib.narration import _norm, label_words
        spoken = []
        for cid, start in self.clips:
            for w, t in manifest.get(cid, {}).get("words", []):
                spoken.append((start + t, _norm(w)))
        for m, t, cid, line in self.labels:
            words = set(label_words(m))
            if not words or len(m.original_text.split()) > MAX_LABEL_WORDS:
                continue
            near = [ts for ts, w in spoken if w in words and abs(ts - t) <= 20]
            if not near or any(ts <= t + 0.3 for ts in near):
                continue
            lead = min(near) - t
            src = " ".join(self.lines[max(0, line - 2):line]) if line else ""
            if lead > EARLY_S and "# early" not in src:
                self.cid = cid
                self._add("early", line, f"{_short(m.original_text)!r} appears {lead:.1f} s before its word "
                          f"is spoken: {FIX['early']}", key=id(m))
        return self.items
