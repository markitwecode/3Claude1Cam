"""Small Manim CE 0.22 ports of ManimGL constructs Grant uses often but CE lacks.

Picked by use count in his 2022-2026 videos (tools/api_frequency.py; counts below).
Each port follows the GL source in manimgl/manimlib (cited per item) as closely as
CE allows. Nothing here is in lib/; copy what you need into a scene, or promote it.

    time_span(anim, a, b)         GL  Animation(time_span=(a, b))          555 kwarg uses
    select(mob, "x")              GL  mob["x"]  (all occurrences)         ~1140 uses
    TransformMatchingStrings      GL  TransformMatchingStrings / -Tex      250 uses
    set_backstroke(mob, ...)      GL  VMobject.set_backstroke               293 uses
    VShowPassingFlash             GL  VShowPassingFlash (tapered flash)      64 uses
    FlashAround / FlashUnder      GL  FlashAround / FlashUnder           162 + 26 uses
    VFadeIn / VFadeOut / ...      GL  VFadeIn / VFadeOut / VFadeInThenOut   260 uses
    replicate / get_grid          GL  Mobject.replicate / get_grid     259 + 135 uses
    fix_in_frame(mob, frame)      GL  Mobject.fix_in_frame (2D frame only)  222 uses
    GlowDot                       GL  GlowDot (shader dot)                  219 uses

Self-tests (no rendering):   .venv/bin/python reference/3b1b/ce_ports.py
Demo (last frame):           .venv/bin/manim -ql -s --media_dir reference/3b1b/_scratch_media \
                                 reference/3b1b/ce_ports.py PortsDemo
"""
from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from manim import *
from manim.animation.animation import prepare_animation
from manim.mobject.mobject import _AnimationBuilder

__all__ = [
    "time_span", "select", "TransformMatchingStrings", "set_backstroke",
    "VShowPassingFlash", "FlashAround", "FlashUnder", "VFadeIn", "VFadeOut",
    "VFadeInThenOut", "replicate", "get_grid", "fix_in_frame", "GlowDot",
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


def set_backstroke(mob: VMobject, color=BLACK, width: float = 3) -> VMobject:
    """GL ``mob.set_backstroke(color=BLACK, width=3)``: an outline drawn *behind* the
    fill, so labels stay legible over lines. In CE it's ``set_stroke(..., background=True)``.

    Do NOT call ``mob.set_backstroke(...)`` on a CE mobject: CE's ``Mobject.__getattr__``
    turns unknown ``set_x(v)`` into a silent attribute write (no error, no outline).
    In our renders widths of ~5-8 give a clearly visible halo at 1080p.
    """
    return mob.set_stroke(color, width, background=True)


# ── flashes ────────────────────────────────────────────────────────────────────


class VShowPassingFlash(Animation):
    """GL VShowPassingFlash (manimlib/animation/indication.py): a gaussian bump of stroke
    width (sigma = time_width / 6) travels along the path, ends tapered by taper_width.

    CE's Cairo renderer has one stroke width per VMobject, so the path is cut into
    ``n_segments`` pieces per subpath and each piece gets its own width every frame.
    Pass a copy if the path is already on screen: the flash pieces are removed at the end.
    """

    def __init__(self, vmobject: VMobject, time_width: float = 0.3, taper_width: float = 0.05,
                 n_segments: int = 80, **kwargs):
        self.time_width = time_width
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
                pieces.add(piece)
        super().__init__(pieces, remover=True, introducer=True, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
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
                 stroke_width: float = 4.0, color=YELLOW, buff: float = SMALL_BUFF, **kwargs):
        path = self.get_path(mobject, buff).set_stroke(color, stroke_width).set_fill(opacity=0)
        super().__init__(path, time_width=time_width, taper_width=taper_width, **kwargs)

    def get_path(self, mobject: Mobject, buff: float) -> VMobject:
        return SurroundingRectangle(mobject, buff=buff)


class FlashUnder(FlashAround):
    """GL FlashUnder: the same flash along an underline (GL Underline, stretch_factor=1)."""

    def get_path(self, mobject: Mobject, buff: float) -> VMobject:
        return Line(mobject.get_corner(DL), mobject.get_corner(DR)).shift(buff * DOWN)


# ── opacity-only fades ─────────────────────────────────────────────────────────


class VFadeIn(Animation):
    """GL VFadeIn: fades stroke and fill opacity from 0 to their current values, with no
    shift/scale and WITHOUT suspending updaters, so always_redraw / updater-driven
    mobjects keep moving while they fade (CE's FadeIn suspends them by default).
    """

    def __init__(self, vmobject: VMobject, suspend_mobject_updating: bool = False, **kwargs):
        kwargs.setdefault("introducer", True)
        super().__init__(vmobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs)

    def interpolate_submobject(self, submob: VMobject, start: VMobject, alpha: float) -> None:
        submob.set_stroke(opacity=interpolate(0, start.get_stroke_opacity(), alpha), family=False)
        submob.set_fill(opacity=interpolate(0, start.get_fill_opacity(), alpha), family=False)


class VFadeOut(VFadeIn):
    """GL VFadeOut: opacity-only fade out; removes the mobject, then restores its opacity
    (GL final_alpha_value=0), so re-adding it later shows it normally."""

    def __init__(self, vmobject: VMobject, **kwargs):
        super().__init__(vmobject, remover=True, introducer=False, **kwargs)

    def interpolate_submobject(self, submob, start, alpha):
        super().interpolate_submobject(submob, start, 1 - alpha)

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        self.interpolate(0)


class VFadeInThenOut(VFadeIn):
    """GL VFadeInThenOut: fade in and back out (rate_func=there_and_back), then remove."""

    def __init__(self, vmobject: VMobject, rate_func=there_and_back, **kwargs):
        super().__init__(vmobject, rate_func=rate_func, remover=True, **kwargs)

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        for sm, start in self.get_all_families_zipped():
            VFadeIn.interpolate_submobject(self, sm, start, 1)


# ── grids ──────────────────────────────────────────────────────────────────────


def replicate(mob: Mobject, n: int) -> Group:
    """GL ``mob.replicate(n)``: a group of n copies (VGroup for VMobjects)."""
    group = VGroup if isinstance(mob, VMobject) else Group
    return group(*(mob.copy() for _ in range(n)))


def get_grid(mob: Mobject, n_rows: int, n_cols: int, height: float | None = None,
             width: float | None = None, buff: float | None = None, h_buff: float | None = None,
             v_buff: float | None = None, buff_ratio: float | None = None,
             fill_rows_first: bool = True, group_by_rows: bool = False) -> Group:
    """GL ``mob.get_grid(n_rows, n_cols, ...)``: copies laid out in a grid, centred at
    ORIGIN. GL spacing defaults: gaps of 0.5 x the cell's width / height unless buff,
    h_buff, v_buff or buff_ratio is given. ``group_by_rows`` returns a group of rows.
    """
    grid = replicate(mob, n_rows * n_cols)
    if buff is not None:
        h_buff = v_buff = buff
    ratio = 0.5 if buff_ratio is None else buff_ratio
    h_buff = ratio * mob.width if h_buff is None else h_buff
    v_buff = ratio * mob.height if v_buff is None else v_buff
    grid.arrange_in_grid(n_rows, n_cols, buff=(h_buff, v_buff),
                         flow_order="rd" if fill_rows_first else "dr")
    grid.move_to(ORIGIN)
    if height is not None:
        grid.scale_to_fit_height(height)
    if width is not None:
        grid.scale_to_fit_width(width)
    if group_by_rows:
        return type(grid)(*(type(grid)(*grid[r * n_cols:(r + 1) * n_cols]) for r in range(n_rows)))
    return grid


# ── camera ─────────────────────────────────────────────────────────────────────


def fix_in_frame(mob: Mobject, frame: Mobject) -> Mobject:
    """GL ``mob.fix_in_frame()`` for a CE MovingCameraScene (``frame = self.camera.frame``):
    an updater keeps ``mob`` at the same spot and size on screen however the frame
    pans or zooms. Call it after positioning ``mob`` for the current frame.

    In a ThreeDScene use CE's ``self.add_fixed_in_frame_mobjects(mob)`` instead.
    Caveat: CE suspends a mobject's updaters while it is itself being animated
    (FadeIn etc.), so don't animate ``mob`` and the frame in the same play().
    Undo with ``mob.clear_updaters()``.
    """
    w0, c0 = frame.width, frame.get_center().copy()
    rel = mob.get_center() - c0
    state = {"w": w0}

    def follow(m: Mobject) -> None:
        w = frame.width
        m.scale(w / state["w"])
        state["w"] = w
        m.move_to(frame.get_center() + rel * (w / w0))

    mob.add_updater(follow, call_updater=True)
    return mob


# ── glow ───────────────────────────────────────────────────────────────────────


class GlowDot(VGroup):
    """GL GlowDot (manimlib/mobject/types/dot_cloud.py + shaders/true_dot.wgsl): a disc of
    radius 0.2 whose alpha falls off as (1 - r/radius)**glow_factor. CE's Cairo renderer
    has no radial gradients, so this stacks ``n_layers`` concentric discs whose opacities
    composite to that profile. Recolour with ``set_color``; don't ``set_opacity`` it
    (that flattens the profile), fade it with FadeIn/FadeOut instead.
    (GL TrueDot is just a plain dot: use CE ``Dot``.)
    """

    def __init__(self, center=ORIGIN, radius: float = 0.2, glow_factor: float = 2.0,
                 color=YELLOW, opacity: float = 1.0, n_layers: int = 16, **kwargs):
        super().__init__(**kwargs)
        rs = radius * np.arange(1, n_layers + 1) / n_layers
        mids = rs - radius / (2 * n_layers)
        target = opacity * (1 - mids / radius) ** glow_factor  # alpha wanted in each ring
        for k in range(n_layers - 1, -1, -1):  # outermost disc first
            outer = target[k + 1] if k + 1 < n_layers else 0.0
            op = 1 - (1 - target[k]) / (1 - outer) if outer < 1 else 1.0
            self.add(Circle(radius=rs[k], stroke_width=0, fill_color=color,
                            fill_opacity=float(np.clip(op, 0, 1))))
        self.move_to(center)


# ── demo + tests ───────────────────────────────────────────────────────────────


class PortsDemo(MovingCameraScene):
    """Exercises every port. Render with -s for the last frame, or as a video."""

    def construct(self):
        frame = self.camera.frame
        title = Text("ce_ports demo", font_size=36).to_edge(UP)
        fix_in_frame(title, frame)
        self.add(title)

        eq1 = MathTex(r"a^2 + b^2 = c^2", substrings_to_isolate=["a", "b", "c"]).shift(UP * 1.5)
        eq2 = MathTex(r"c^2 = a^2 + b^2", substrings_to_isolate=["a", "b", "c"]).shift(UP * 1.5)
        set_backstroke(eq1, BLACK, 6)
        for key, col in [("a", BLUE), ("b", TEAL), ("c", YELLOW)]:
            select(eq1, key).set_color(col)
            select(eq2, key).set_color(col)
        self.play(VFadeIn(eq1))
        self.play(TransformMatchingStrings(eq1, eq2, path_arc=PI / 2))
        self.play(FlashAround(eq2, run_time=1.5, time_width=1.5))

        words = Text("the fine print, the fine print", font_size=30, disable_ligatures=True)
        self.play(FadeIn(words))
        self.play(FlashUnder(select(words, "fine")[1], color=RED))
        self.play(*(select(words, "fine")[k].animate.set_color(RED) for k in range(2)))

        cells = get_grid(Square(0.4).set_stroke(GREY_B, 2), 2, 6).shift(1.4 * DOWN)
        glow = GlowDot(cells[0].get_center())
        t = ValueTracker(0)
        glow.add_updater(lambda g: g.move_to(cells[int(t.get_value()) % 12].get_center()))
        self.play(LaggedStartMap(FadeIn, cells, lag_ratio=0.05), VFadeIn(glow))
        self.play(time_span(t.animate.set_value(11), 0.5, 2.0),
                  time_span(VShowPassingFlash(cells[6:].copy().set_stroke(YELLOW, 6), time_width=0.6), 0, 1))
        self.play(frame.animate.scale(0.8).shift(0.5 * DOWN))   # title stays put on screen
        self.play(VFadeInThenOut(SurroundingRectangle(cells, color=PINK)))
        self.play(VFadeOut(glow), FadeOut(words))
        self.wait(0.2)


def _self_test() -> None:
    config.media_dir = str(Path(__file__).resolve().parent / "_scratch_media")
    # time_span: nothing before start, linear inside, held after end
    seen = []
    a = Animation(Square(), rate_func=linear)
    a.interpolate = seen.append  # stand-in for the real interpolate
    time_span(a, 1.0, 3.0)
    for t in (0.0, 1.0, 2.0, 3.0):
        a.interpolate(t / a.run_time)
    assert a.run_time == 3.0 and np.allclose(seen, [0, 0, 0.5, 1]), seen
    a.run_time = 6.0  # what play(run_time=6) does
    seen.clear(); a.interpolate(2.0 / 6.0)
    assert np.isclose(seen[0], 0.5), seen

    # select: all occurrences, on MathTex and Text
    tex = MathTex("x + x^2 = y", substrings_to_isolate=["x"])
    assert len(select(tex, "x")) == 2 and len(select(tex, "x")[0]) == 1
    parts = MathTex("{{ a }} + {{ b }}")
    assert len(select(parts, "b")) == 1
    txt = Text("ab cd ab")
    assert [len(g) for g in select(txt, "ab")] == [2, 2]
    assert select(txt, "cd")[0][0] is txt.submobjects[2]
    lig = Text("the fine print", disable_ligatures=True)
    assert select(lig, "fine")[0][0] is lig.submobjects[4]

    # TransformMatchingStrings: shared glyphs move, the rest fade
    s, t = MathTex("a + b"), MathTex("b + a + c")
    anim = TransformMatchingStrings(s, t)
    kinds = [type(x).__name__ for x in anim.animations]
    assert kinds.count("Transform") == 3 and kinds.count("FadeIn") == 2, kinds

    # grids
    g = get_grid(Square(1), 2, 3)
    assert len(g) == 6 and np.isclose(g.width, 3 + 2 * 0.5) and np.isclose(g.height, 2 + 0.5)
    assert len(get_grid(Square(1), 2, 3, group_by_rows=True)) == 2
    assert len(replicate(Dot(), 4)) == 4

    # fix_in_frame follows a moving / zooming frame
    frame = ScreenRectangle(height=config.frame_height)
    m = Dot().move_to(3 * RIGHT + 2 * UP)
    fix_in_frame(m, frame)
    frame.scale(0.5).shift(LEFT)
    m.update()
    assert np.allclose(m.get_center(), LEFT + 0.5 * (3 * RIGHT + 2 * UP)), m.get_center()

    # VFadeIn halfway halves opacity; VFadeOut restores it after clean-up
    sq = Square().set_fill(RED, 0.8)
    v = VFadeIn(sq, rate_func=linear); v.begin(); v.interpolate(0.5)
    assert np.isclose(sq.get_fill_opacity(), 0.4)

    # backstroke really sets CE's background stroke
    assert set_backstroke(Square(), BLACK, 5).background_stroke_width == 5

    # GlowDot composite alpha follows (1 - r)^2
    gd = GlowDot(radius=1, n_layers=20)
    ops = [c.get_fill_opacity() for c in gd]
    center_alpha = 1 - np.prod([1 - o for o in ops])
    assert center_alpha > 0.85 and ops[0] < 0.05, (center_alpha, ops[0])
    print("ce_ports self-test: all OK")


if __name__ == "__main__":
    _self_test()
