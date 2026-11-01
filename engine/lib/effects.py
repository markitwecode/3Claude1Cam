"""3b1b's emphasis and transform helpers, ported to Manim CE 0.22.

Promoted from reference/3b1b/ce_ports.py (each one tested there: run
`.venv/bin/python reference/3b1b/ce_ports.py`; see GL_TO_CE.md for the evidence).
Defaults use our palette (lib.style) instead of GL's black/yellow.

    FlashAround(mob, run_time=2, time_width=1.5)   # his signature emphasis (PATTERNS P6)
    FlashUnder(tok, color=TEAL)                     # flash along an underline (P7)
    set_backstroke(label)                           # halo so labels read over arrows (P10)
    TransformMatchingStrings(a, b)                  # glyph-matching rewrite, no {{ }} needed (P11)
    time_span(anim, 0.5, 1.5)                       # run an animation in part of a play()
    select(text_or_tex, "x")                        # every occurrence of a substring
"""
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from manim import *

from lib import style as _style
from manim.animation.animation import prepare_animation
from manim.mobject.mobject import _AnimationBuilder

__all__ = [
    "time_span", "select", "TransformMatchingStrings", "set_backstroke",
    "VShowPassingFlash", "FlashAround", "FlashUnder", "one_glyph",
]


# ── timing ──────────────────────────────────────────────────────────────────────


def time_span(anim: Animation | _AnimationBuilder, start: float, end: float) -> Animation:
    """GL ``Anim(..., time_span=(start, end))``: run only during [start, end] seconds of
    the ``play()`` call (manimlib/animation/animation.py, ``time_spanned_alpha``).

    The animation begins at t=0 (so a FadeIn stays invisible until ``start``), finishes
    at ``end`` and holds its end state if the play() lasts longer. ``rate_func`` and
    ``lag_ratio`` apply inside the span. Works with ``self.play(..., run_time=T)``
    because the span is in absolute seconds.
    """
    if not 0 <= start < end:
        raise ValueError("need 0 <= start < end")
    anim = prepare_animation(anim)  # accepts mob.animate... too
    inner = anim.interpolate
    anim.run_time = end

    def spanned(alpha: float) -> None:
        inner(float(np.clip((alpha * anim.run_time - start) / (end - start), 0, 1)))

    anim.interpolate = spanned  # instance attribute shadows the method
    anim.abs_span = (start, end)   # read by kit.sweep_clear and vk check (seconds into the play)
    return anim


# ── string selection ───────────────────────────────────────────────────────────


def select(mob: VMobject, key: str) -> VGroup:
    """GL ``mob["key"]`` (StringMobject.select_parts): every occurrence of ``key``,
    as a VGroup with one VGroup per occurrence, so ``select(t, "x")[0]`` is the first.

    * MathTex / Tex: ``key`` must be isolated when the mobject is built, i.e. listed in
      ``substrings_to_isolate`` or ``tex_to_color_map``, or be a whole ``{{ }}`` part / arg.
      (CE's own ``get_part_by_tex`` only returns the first occurrence.)
    * Text: plain substring search (not MarkupText: its markup shifts the indices).
      Build the Text with ``disable_ligatures=True`` if it has ligature pairs (fi, fl...).

    Animating a selection makes CE split the parent in ``self.mobjects`` into its
    remaining pieces plus the selection (GL leaves the list alone). Rendering is
    unchanged and ``FadeOut(parent)`` still clears every piece, but a bare
    ``self.remove(parent)`` no longer does: use ``self.remove(*parent.get_family())``.
    """
    if hasattr(mob, "matched_strings_and_ids"):  # MathTex / Tex
        groups, seen = [], set()
        for s, i in mob.matched_strings_and_ids:
            if (s == key or s.strip() == key) and i in mob.id_to_vgroup_dict:
                g = mob.id_to_vgroup_dict[i]
                ids = tuple(id(m) for m in g.family_members_with_points())
                if ids and ids not in seen:
                    seen.add(ids)
                    groups.append(VGroup(*g.family_members_with_points()))
        if not groups:
            raise KeyError(f"{key!r} not isolated: build with substrings_to_isolate=[{key!r}]")
        return VGroup(*groups)
    if hasattr(mob, "original_text"):  # Text
        text = mob.original_text
        per_char = getattr(mob, "disable_ligatures", False)  # then spaces are (invisible) submobjects too
        index, n = [], 0
        for ch in text:
            index.append(n)
            n += per_char or ch not in " \n"
        if n != len(mob.submobjects):
            raise ValueError("glyph count != character count (ligatures?); "
                             "build the Text with disable_ligatures=True")
        groups, pos = [], text.find(key)
        while pos != -1:
            span = range(pos, pos + len(key))
            idx = [index[j] for j in span if per_char or text[j] not in " \n"]
            groups.append(VGroup(*(mob.submobjects[j] for j in idx)))
            pos = text.find(key, pos + len(key))
        if not groups:
            raise KeyError(f"{key!r} not found in {text!r}")
        return VGroup(*groups)
    raise TypeError(f"select() needs MathTex/Tex/Text, got {type(mob).__name__}")


# ── matching transform ─────────────────────────────────────────────────────────


def _shape_key(m: VMobject) -> bytes:
    """Glyph identity independent of position and size (like GL's has_same_shape_as)."""
    pts = m.points
    size = max(m.width, m.height, 1e-6)
    norm = np.round((pts - m.get_center()) / size, 2) + 0.0  # + 0.0 turns -0.0 into 0.0
    return len(pts).to_bytes(4, "little") + norm.tobytes()


class TransformMatchingStrings(AnimationGroup):
    """GL TransformMatchingStrings (== GL TransformMatchingTex), from
    manimlib/animation/transform_matching_parts.py.

    Glyphs are paired by finding the longest common runs of identical glyph shapes
    (difflib, as in GL); matched glyphs move, unmatched source glyphs fade out toward
    the target's center and unmatched target glyphs fade in from the source's center.
    ``matched_keys`` / ``key_map`` force pairs first (keys are resolved with select(),
    so isolate them in MathTex). Works on MathTex, Tex and Text alike; no ``{{ }}``
    splitting needed, unlike CE's TransformMatchingTex. GL default run_time=2 kept.
    """

    def __init__(self, source: VMobject, target: VMobject, matched_keys=(), key_map=None,
                 run_time: float = 2, lag_ratio: float = 0, **kwargs):
        src = source.family_members_with_points()
        trg = target.family_members_with_points()
        used_s, used_t, anims = set(), set(), []

        def pair(s_group, t_group):
            s_new = [m for m in s_group.family_members_with_points() if id(m) not in used_s]
            t_new = [m for m in t_group.family_members_with_points() if id(m) not in used_t]
            if s_new and t_new:
                used_s.update(map(id, s_new))
                used_t.update(map(id, t_new))
                anims.append(Transform(VGroup(*s_new), VGroup(*t_new), **kwargs))

        for k1, k2 in (key_map or {}).items():
            pair(select(source, k1), select(target, k2))
        for k in matched_keys:
            pair(select(source, k), select(target, k))

        keys1 = [object() if id(m) in used_s else _shape_key(m) for m in src]
        keys2 = [object() if id(m) in used_t else _shape_key(m) for m in trg]
        while True:
            match = SequenceMatcher(None, keys1, keys2, autojunk=False).find_longest_match(
                0, len(keys1), 0, len(keys2))
            if match.size == 0:
                break
            for k in range(match.size):
                i, j = match.a + k, match.b + k
                anims.append(Transform(src[i], trg[j], **kwargs))
                used_s.add(id(src[i]))
                used_t.add(id(trg[j]))
                keys1[i], keys2[j] = object(), object()

        fade_kw = {k: v for k, v in kwargs.items() if k != "path_arc"}
        for m in src:
            if id(m) not in used_s:
                anims.append(FadeOut(m, target_position=target.get_center(), scale=0, **fade_kw))
        self.fade_in_copies = []
        for m in trg:
            if id(m) not in used_t:
                c = m.copy()
                self.fade_in_copies.append(c)
                anims.append(FadeIn(c, target_position=source.get_center(), scale=0, **fade_kw))
        self.source, self.target = source, target
        super().__init__(*anims, run_time=run_time, lag_ratio=lag_ratio)

    def clean_up_from_scene(self, scene: Scene) -> None:
        # Same end-state handling as CE's TransformMatchingAbstractBase: put the source
        # back as it was, take it and the helpers off screen, show the target.
        for anim in self.animations:
            anim.interpolate(0)
        scene.remove(self.mobject, self.source, *self.fade_in_copies)
        scene.add(self.target)


# ── style ──────────────────────────────────────────────────────────────────────


def set_backstroke(mob: VMobject, color=None, width: float = 6) -> VMobject:
    """GL ``mob.set_backstroke(color=BLACK, width=3)``: an outline drawn *behind* the
    fill, so labels stay legible over lines. In CE it's ``set_stroke(..., background=True)``.

    Do NOT call ``mob.set_backstroke(...)`` on a CE mobject: CE's ``Mobject.__getattr__``
    turns unknown ``set_x(v)`` into a silent attribute write (no error, no outline).
    In our renders widths of ~5-8 give a clearly visible halo at 1080p.
    """
    return mob.set_stroke(color or _style.BG, width, background=True)


# ── flashes ────────────────────────────────────────────────────────────────────


class VShowPassingFlash(Animation):
    """GL VShowPassingFlash (manimlib/animation/indication.py): a gaussian bump of stroke
    width (sigma = time_width / 6) travels along the path, ends tapered by taper_width.

    CE's Cairo renderer has one stroke width per VMobject, so the path is cut into
    ``n_segments`` pieces per subpath and each piece gets its own width every frame.
    Pass a copy if the path is already on screen: the flash pieces are removed at the end.

    whole: the whole shape fades in and out instead (no travelling bump). Default: when the path
    is shorter than SHORT_PATH. A bump on a short path is a short stroke, and next to a glyph it
    reads as a mark: a comma or prime beside a digit (DE L6 ch3, a ring round "0"), a minus or
    underscore under it. FlashAround passes whole=True for one-glyph targets.
    """

    def __init__(self, vmobject: VMobject, time_width: float = 0.3, taper_width: float = 0.05,
                 n_segments: int = 80, whole: bool | None = None, **kwargs):
        self.time_width = time_width
        if whole is None:
            whole = sum(sm.get_arc_length() for sm in vmobject.family_members_with_points()) < SHORT_PATH
        self.whole = whole
        pieces = VGroup()
        for sm in vmobject.family_members_with_points():
            width, color = sm.get_stroke_width(), sm.get_stroke_color()
            opacity = sm.get_stroke_opacity()
            for i in range(n_segments):
                a, b = i / n_segments, (i + 1) / n_segments
                piece = VMobject().pointwise_become_partial(sm, a, b)
                piece.set_stroke(color, width, opacity).set_fill(opacity=0)
                piece.set_cap_style(CapStyleType.ROUND)
                x = (a + b) / 2
                taper = min(x, 1 - x) / taper_width if taper_width > 0 else 1
                piece.flash_x, piece.flash_w = x, width * min(taper, 1)
                piece.flash_op = opacity
                pieces.add(piece)
        self.source_kind = type(vmobject).__name__   # read by vk check's flash-box advice
        super().__init__(pieces, remover=True, introducer=True, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        if self.whole:   # the whole shape, full width, fading in then out: never a partial stroke
            k = there_and_back(alpha)
            for p in self.mobject.submobjects:
                p.set_stroke(width=p.flash_w, opacity=p.flash_op * k)
            return
        tw = self.time_width
        sigma = tw / 6
        mu = interpolate(-tw / 2, 1 + tw / 2, self.rate_func(alpha))
        for p in self.mobject.submobjects:
            d = p.flash_x - mu
            g = np.exp(-0.5 * (d / sigma) ** 2) if abs(d) <= 3 * sigma else 0.0
            p.set_stroke(width=p.flash_w * g)


class FlashAround(VShowPassingFlash):
    """GL FlashAround: a yellow flash running once around the mobject's bounding box.
    GL defaults: time_width=1.0, taper_width=0, stroke_width=4, buff=SMALL_BUFF, run_time 1.
    He typically writes ``FlashAround(mob, run_time=2, time_width=1.5)``.
    """

    def __init__(self, mobject: Mobject, time_width: float = 1.0, taper_width: float = 0.0,
                 stroke_width: float = 4.0, color=None, buff: float = SMALL_BUFF, **kwargs):
        color = color or _style.YELLOW
        path = self.get_path(mobject, buff).set_stroke(color, stroke_width).set_fill(opacity=0)
        if one_glyph(mobject):   # a ring round one letter or digit fades whole: a travelling arc
            kwargs.setdefault("whole", True)   # beside a digit reads as a comma or prime
        super().__init__(path, time_width=time_width, taper_width=taper_width, **kwargs)

    def get_path(self, mobject: Mobject, buff: float) -> VMobject:
        if one_glyph(mobject):
            # A box hugging one letter or digit flashes its top edge first, which reads as an
            # overbar (NOT, in the digital-electronics course; 3 times in DE L6). Ring it instead,
            # with clearance all round: a circle has no horizontal edge.
            r = 0.5 * float(np.hypot(mobject.width, mobject.height)) + max(buff, GLYPH_RING_BUFF)
            return Circle(radius=r).move_to(mobject.get_center())
        return SurroundingRectangle(mobject, buff=buff)


GLYPH_RING_BUFF = 0.12   # clearance between a one-glyph target and FlashAround's ring
SHORT_PATH = 1.0         # VShowPassingFlash on a path shorter than this fades whole (see its docstring)


def one_glyph(mob: Mobject) -> bool:
    """True when `mob` is a single letter or digit: at most two pieces, all glyph outlines (or a
    thin rule such as a MathTex overline), with no box, line or dot of its own."""
    from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
    parts = mob.family_members_with_points()
    return 0 < len(parts) <= 2 and all(
        isinstance(p, VMobjectFromSVGPath) or (isinstance(p, Rectangle) and min(p.width, p.height) < 0.06)
        for p in parts)


class FlashUnder(FlashAround):
    """GL FlashUnder: the same flash along an underline (GL Underline, stretch_factor=1)."""

    def get_path(self, mobject: Mobject, buff: float) -> VMobject:
        return Line(mobject.get_corner(DL), mobject.get_corner(DR)).shift(buff * DOWN)

