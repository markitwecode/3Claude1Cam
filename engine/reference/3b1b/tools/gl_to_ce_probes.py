"""Behaviour probes for ../GL_TO_CE.md: each P## checks one claim against installed CE 0.22.

Run:  .venv/bin/python reference/3b1b/tools/gl_to_ce_probes.py
Each line prints PASS (the claim, as written in the guide, holds) or FAIL with details.
Nothing is rendered; Tex/Text caches go to reference/3b1b/_scratch_media.
"""
import inspect
import warnings
from pathlib import Path

import numpy as np

warnings.simplefilter("ignore")
from manim import *  # noqa: E402

config.media_dir = str(Path(__file__).resolve().parents[1] / "_scratch_media")
RESULTS = []


def probe(pid, claim):
    def deco(fn):
        try:
            ok, info = fn()
        except Exception as e:  # a probe that crashes is a failed claim
            ok, info = False, f"probe crashed: {type(e).__name__}: {e}"
        RESULTS.append((pid, ok, claim, info))
        return fn
    return deco


def raises(fn, exc=Exception):
    try:
        fn()
    except exc as e:
        return True, f"{type(e).__name__}: {str(e)[:90]}"
    return False, "no exception"


sq = lambda: Square(side_length=1)  # noqa: E731


@probe("P01", "CE FadeIn(m, scale=s) starts at s x size (GL starts at size / s)")
def _():
    m = sq(); a = FadeIn(m, scale=2); a.begin()       # begin() puts m in its start state
    return np.isclose(m.width, 2.0), f"start width {m.width:.2f} for a 1.0 square"


@probe("P02", "FadeIn(m, shift=v) starts at -v, like GL")
def _():
    m = sq(); FadeIn(m, shift=UP).begin()
    return np.allclose(m.get_center(), DOWN), f"start center {m.get_center().round(2)}"


@probe("P03", "FadeOut(m, shift=v, scale=s) ends shifted by v and scaled by s, like GL")
def _():
    m = sq(); a = FadeOut(m, shift=RIGHT, scale=0.5); a.begin(); a.interpolate(1)
    return np.isclose(m.width, 0.5) and np.allclose(m.get_center(), RIGHT), f"{m.width:.2f} {m.get_center().round(2)}"


@probe("P04", "FadeIn(m, target_position=p, scale=0) starts at p as a point (GL FadeInFromPoint)")
def _():
    m = sq().shift(3 * RIGHT); FadeIn(m, target_position=2 * LEFT, scale=0).begin()
    return np.allclose(m.get_center(), 2 * LEFT) and m.width < 1e-6, f"{m.get_center().round(2)} w={m.width}"


@probe("P05", "CE animations reject time_span=")
def _():
    return raises(lambda: FadeIn(sq(), time_span=(0.5, 1)), TypeError)


@probe("P06", "CE animations suspend the mobject's updaters by default (GL default: False)")
def _():
    vals = [FadeIn(sq()).suspend_mobject_updating, Transform(sq(), Circle()).suspend_mobject_updating,
            Create(sq()).suspend_mobject_updating]
    return all(vals), str(vals)


@probe("P07", "play(..., lag_ratio=x) does not re-time an already-built LaggedStart/AnimationGroup")
def _():
    g = LaggedStart(FadeIn(sq()), FadeIn(Circle()), lag_ratio=0.5)
    g.lag_ratio = 0.0  # exactly what Scene.play(g, lag_ratio=0) does (setattr)
    g.begin()
    starts = list(g.anims_with_timings["start"])
    return np.isclose(starts[1], 0.5), f"starts {starts}"


@probe("P08", "Write defaults: run_time 1 (<15 glyph paths) else 2; lag_ratio min(4/n, 0.2)")
def _():
    a, b = Write(Text("hi")), Write(Text("a long sentence with many glyphs"))
    return a.run_time == 1 and b.run_time == 2, f"{a.run_time}/{a.lag_ratio:.3f}, {b.run_time}/{b.lag_ratio:.3f}"


@probe("P09", "LaggedStartMap(FadeIn, g, shift=UP, lag_ratio=r) passes shift to each FadeIn; run_time 2")
def _():
    a = LaggedStartMap(FadeIn, VGroup(sq(), sq()), shift=UP, lag_ratio=0.3)
    return np.allclose(a.animations[0].shift_vector, UP) and a.run_time == 2, f"lag {a.lag_ratio}"


@probe("P10", "Rotate(m, TAU) really turns (half-way = rotated by PI)")
def _():
    m = sq(); a = Rotate(m, TAU); a.begin(); a.interpolate(0.5)
    return np.allclose(m.get_vertices()[0], [-0.5, -0.5, 0], atol=1e-6), str(m.get_vertices()[0].round(2))


@probe("P11", "MathTex/Tex reject t2c= and isolate= (TypeError); tex_to_color_map works")
def _():
    a, b = raises(lambda: MathTex("x+y", t2c={"x": RED})), raises(lambda: MathTex("x+y", isolate=["x"]))
    MathTex("x+y", tex_to_color_map={"x": RED})
    return a[0] and b[0], f"{a[1]} | {b[1]}"


@probe("P12", "substrings_to_isolate does not split MathTex into separate submobjects (0.22)")
def _():
    t = MathTex("a + b = c", substrings_to_isolate=["a", "b", "c"])
    return len(t.submobjects) == 1, f"{len(t.submobjects)} submobject(s)"


@probe("P13", "get_part_by_tex returns only the FIRST occurrence; tex_to_color_map colours all")
def _():
    t = MathTex("x + x + x", substrings_to_isolate=["x"])
    first = len(t.get_part_by_tex("x").family_members_with_points())
    c = MathTex("x + x", tex_to_color_map={"x": RED})
    cols = [g.get_fill_color().to_hex() for g in c.family_members_with_points()]
    return first == 1 and cols[0] == cols[2] != cols[1], f"first-part glyphs={first}, colours={cols}"


@probe("P14", "{{ b }} keeps its spaces: set_color_by_tex('b') is a no-op there, works with {{b}}")
def _():
    cols = lambda m: [g.get_fill_color().to_hex() for g in m.family_members_with_points()]  # noqa: E731
    spaced = cols(MathTex("{{ a }} + {{ b }}").set_color_by_tex("b", TEAL))
    tight = cols(MathTex("{{a}} + {{b}}").set_color_by_tex("b", TEAL))
    return len(set(spaced)) == 1 and len(set(tight)) == 2, f"{spaced} vs {tight}"


@probe("P15", "No string indexing: MathTex(...)['x'] and Text(...)['x'] raise TypeError")
def _():
    a, b = raises(lambda: MathTex("x+y")["x"], TypeError), raises(lambda: Text("ab cd")["cd"], TypeError)
    return a[0] and b[0], b[1]


@probe("P16", "Text(alignment=) raises; Paragraph(..., alignment='left') works")
def _():
    r = raises(lambda: Text("a\nb", alignment="LEFT"), TypeError)
    Paragraph("a", "bbb", alignment="left")
    return r[0], r[1]


@probe("P17", "CE TransformMatchingTex: unsplit strings match nothing; no matched_keys; asserts on Text")
def _():
    an = TransformMatchingTex(MathTex("a + b = c"), MathTex("c = a + b"))
    nothing = len(an.animations[0].mobject.submobjects) == 0
    parts = TransformMatchingTex(MathTex("a", "+", "b"), MathTex("b", "+", "a"))
    n_parts = len(parts.animations[0].mobject.submobjects)
    mk = raises(lambda: TransformMatchingTex(MathTex("{{a}}"), MathTex("{{a}}"), matched_keys=["a"]), TypeError)
    txt = raises(lambda: TransformMatchingTex(Text("ab"), Text("ba")), AssertionError)
    return nothing and n_parts == 3 and mk[0] and txt[0], f"split-args matched {n_parts} parts"


@probe("P18", "mob.set_backstroke: no/2 args -> TypeError, 1 arg -> SILENT no-op; set_stroke(background=True) works")
def _():
    m = sq()
    a = raises(lambda: m.set_backstroke(), TypeError)[0]
    b = raises(lambda: m.set_backstroke(BLACK, 3), TypeError)[0]
    m.set_backstroke(BLACK)  # silently stores an attribute
    silent = m.background_stroke_width == 0
    m.set_stroke(BLACK, 6, background=True)
    return a and b and silent and m.background_stroke_width == 6, "auto-setter from Mobject.__getattr__"


@probe("P19", "set_height(h) works (deprecated auto-setter) but any kwarg (stretch/about_edge) raises")
def _():
    m = sq(); m.set_height(2)
    r = raises(lambda: sq().set_height(2, stretch=True), TypeError)
    m2 = sq(); m2.scale_to_fit_height(2, about_edge=DOWN); m3 = sq(); m3.stretch_to_fit_width(3)
    ok = np.isclose(m.height, 2) and r[0] and np.isclose(m2.get_bottom()[1], -0.5) and np.isclose(m3.height, 1)
    return ok, r[1]


@probe("P20", "set_max_width(w) is a SILENT no-op in CE")
def _():
    r = Rectangle(width=8, height=1); r.set_max_width(3)
    return np.isclose(r.width, 8), f"width still {r.width}"


@probe("P21", "set_color(c, 0.3): the 2nd positional does not set opacity in CE")
def _():
    m = sq().set_color(RED, 0.3)
    return m.get_stroke_opacity() == 1.0, f"stroke opacity {m.get_stroke_opacity()}"


@probe("P22", "set_stroke(behind=) and set_fill(border_width=) raise TypeError")
def _():
    a, b = raises(lambda: sq().set_stroke(BLACK, 3, behind=True)), raises(lambda: sq().set_fill(RED, 1, border_width=1))
    return a[0] and b[0], f"{a[1]} | {b[1]}"


@probe("P23", "add_updater does not call the updater at once unless call_updater=True (GL: calls)")
def _():
    calls = []
    sq().add_updater(lambda m: calls.append(1))
    n0 = len(calls)
    sq().add_updater(lambda m: calls.append(1), call_updater=True)
    return n0 == 0 and len(calls) == 1, f"{n0} then {len(calls)}"


@probe("P24", "mob.always.f(...) works; mob.f_always missing; f_always(mob.f, func) works; always_redraw zero-arg only")
def _():
    a, b = Dot(), Dot().shift(LEFT)
    b.always.next_to(a, UP); a.shift(2 * RIGHT); b.update()
    follows = np.isclose(b.get_x(), 2)
    no_prop = raises(lambda: Dot().f_always, AttributeError)[0]
    t, d = ValueTracker(1), Dot()
    f_always(d.move_to, lambda: t.get_value() * RIGHT); t.set_value(3); d.update()
    ar = raises(lambda: always_redraw(lambda x: Dot(x), RIGHT), TypeError)[0]
    return follows and no_prop and np.isclose(d.get_x(), 3) and ar, ""


@probe("P25", "get_grid -> TypeError; replicate, pfp, fix_in_frame -> AttributeError")
def _():
    m = sq()
    res = [raises(lambda: m.get_grid(2, 3), TypeError)[0]] + [
        raises(lambda n=n: getattr(m, n), AttributeError)[0] for n in ("replicate", "pfp", "fix_in_frame")]
    return all(res), str(res)


@probe("P26", "arrange_in_grid(n_rows=, n_cols=, h_buff=, ...) GL kwargs are SILENTLY ignored")
def _():
    g = VGroup(*[sq() for _ in range(6)]).arrange_in_grid(n_rows=1, n_cols=6, h_buff=0)
    return not np.isclose(g.width, 6), f"asked for 1x6 touching, got {g.width:.2f} x {g.height:.2f}"


@probe("P27", "Arrow(thickness=) raises; stroke_width/max_tip_length_to_length_ratio/path_arc accepted")
def _():
    r = raises(lambda: Arrow(LEFT, RIGHT, thickness=3), TypeError)
    Arrow(LEFT, RIGHT, stroke_width=3, max_tip_length_to_length_ratio=0.2, path_arc=PI / 3)
    return r[0], r[1]


@probe("P28", "Rectangle(5, 2) raises (CE positional: color, height, width); Arc(0, PI) silently has radius 0")
def _():
    r = raises(lambda: Rectangle(5.25, 1.5))
    return r[0] and Arc(0, PI).radius == 0, r[1]


@probe("P29", "Underline(stretch_factor=) raises; Underline(m, buff=) works")
def _():
    r = raises(lambda: Underline(sq(), stretch_factor=1.2), TypeError)
    Underline(sq(), buff=0.1)
    return r[0], r[1]


@probe("P30", "brace.get_tex('x', font_size=) raises; get_text returns Tex; BraceLabel(font_size=) ok; no tex_string")
def _():
    b = Brace(sq(), DOWN)
    r = raises(lambda: b.get_tex("x", font_size=30), TypeError)
    t = type(b.get_text("w")).__name__
    BraceLabel(sq(), "x", font_size=30)
    r2 = raises(lambda: Brace(sq(), DOWN, tex_string=r"\underbrace{\qquad}"), TypeError)
    return r[0] and t == "Tex" and r2[0], f"get_text -> {t}"


@probe("P31", "DecimalNumber(min_total_width=) raises; set_value keeps the left edge (edge_to_fix=LEFT)")
def _():
    r = raises(lambda: DecimalNumber(5, min_total_width=4), TypeError)
    d = DecimalNumber(9.99).to_edge(LEFT); x0 = d.get_left()[0]; d.set_value(1234.5)
    return r[0] and np.isclose(d.get_left()[0], x0), r[1]


@probe("P32", "Axes(width=) raises; axes.get_graph raises; add_coordinate_labels missing; plot/add_coordinates ok")
def _():
    a = raises(lambda: Axes(width=6), TypeError)[0]
    b = raises(lambda: Axes().get_graph(np.sin), TypeError)[0]
    c = raises(lambda: Axes().add_coordinate_labels(), AttributeError)[0]
    ax = Axes(x_range=(-3, 3, 1), y_range=(-2, 2, 1), x_length=6, y_length=4)
    w = ax.x_axis.width  # measured before labels are added
    ax.plot(np.sin, x_range=(-2, 2)); ax.add_coordinates()
    return a and b and c and np.isclose(w, 6, atol=0.01), f"x axis width {w:.2f}"


@probe("P33", "NumberLine(width=)/big_tick_spacing raise; length=, add_numbers(font_size, num_decimal_places) ok")
def _():
    a = raises(lambda: NumberLine(x_range=(0, 10), width=8), TypeError)[0]
    b = raises(lambda: NumberLine(x_range=(0, 10, 1), length=8, big_tick_spacing=5), TypeError)[0]
    n = NumberLine(x_range=(0, 2, 0.5), length=8); n.add_numbers(font_size=24, num_decimal_places=1)
    return a and b, f"{len(n.numbers)} labels"


@probe("P34", "ImageMobject(height=) raises; use .set(height=h)")
def _():
    arr = np.zeros((10, 10, 3), dtype=np.uint8)
    r = raises(lambda: ImageMobject(arr, height=2), TypeError)
    im = ImageMobject(arr).set(height=2)
    return r[0] and np.isclose(im.height, 2), r[1]


@probe("P35", "become(match_updaters=) raises")
def _():
    return raises(lambda: sq().become(Circle(), match_updaters=True), TypeError)


@probe("P36", "Missing in CE: DEG, FRAME_WIDTH/HEIGHT, get_norm, cross, interp_by_hsl; config.frame_width = 14.22")
def _():
    import manim
    miss = [n for n in ("DEG", "FRAME_WIDTH", "FRAME_HEIGHT", "get_norm", "cross") if hasattr(manim, n)]
    hsl = "interp_by_hsl" in str(inspect.signature(color_gradient))
    return not miss and not hsl and np.isclose(config.frame_width, 128 / 9), f"present anyway: {miss}"


@probe("P37", "Not in CE at all (selection of GL names)")
def _():
    import manim
    names = ["ShowCreation", "VFadeIn", "VFadeOut", "VFadeInThenOut", "FlashAround", "FlashUnder",
             "VShowPassingFlash", "CountInFrom", "FadeInFromPoint", "FadeOutToPoint",
             "TransformMatchingStrings", "ShowCreationThenFadeOut", "GlowDot", "TexText", "OldTex",
             "SurfaceMesh", "ParametricSurface", "ParametricCurve", "Checkmark", "Exmark",
             "SpeechBubble", "InteractiveScene"]
    present = [n for n in names if hasattr(manim, n)]
    return not present, f"present: {present}"


@probe("P38", "CE TrueDot/DotCloud live in manim.mobject.opengl (OpenGL renderer only)")
def _():
    import manim
    from manim.mobject.opengl.dot_cloud import TrueDot
    return (not hasattr(manim, "TrueDot")) or "opengl" in TrueDot.__module__, TrueDot.__module__


@probe("P39", "At equal font_size CE Text is ~1.3x taller than MathTex")
def _():
    t, m = Text("0", font_size=48).height, MathTex("0", font_size=48).height
    return 1.2 < t / m < 1.45, f"Text {t:.3f} / MathTex {m:.3f}"


@probe("P40", "VGroup accepts a generator or a list")
def _():
    return len(VGroup(sq() for _ in range(3))) == 3 and len(VGroup([sq(), sq()])) == 2, ""


@probe("P41", "CE Point is a point-cloud PMobject; VectorizedPoint is the VMobject anchor")
def _():
    return isinstance(Point(RIGHT), PMobject) and isinstance(VectorizedPoint(), VMobject), ""


@probe("P42", "mob.animate(run_time=, path_arc=) passes animation args")
def _():
    a = sq().animate(run_time=2, path_arc=PI).shift(RIGHT).build()
    return a.run_time == 2 and np.isclose(a.path_arc, PI), type(a).__name__


@probe("P43", "Flash default flash_radius is 0.1 in CE (GL 0.3); Indicate defaults 1.2 / YELLOW")
def _():
    f, i = Flash(ORIGIN), Indicate(sq())
    return f.flash_radius == 0.1 and i.scale_factor == 1.2, ""


@probe("P44", "GL reorient(theta, phi, gamma) == CE theta-90deg, phi, -gamma (rotation matrices equal)")
def _():
    from scipy.spatial.transform import Rotation
    worst = 0.0
    for th, ph, ga in [(-30, 70, 0), (20, 80, 0), (135, 30, 10), (10, 60, -15)]:
        gl = Rotation.from_euler("zxz", [ga * DEGREES, ph * DEGREES, th * DEGREES]).as_matrix().T
        cam = ThreeDCamera()
        cam.set_theta((th - 90) * DEGREES); cam.set_phi(ph * DEGREES); cam.set_gamma(-ga * DEGREES)
        worst = max(worst, float(np.abs(gl - cam.generate_rotation_matrix()).max()))
    return worst < 1e-12, f"max |diff| {worst:.1e}"


@probe("P45", "CE has mob.always but uses call_updater=True (runs once immediately)")
def _():
    a, b = Dot(), Dot()
    a.shift(UP)
    b.always.move_to(a)
    return np.allclose(b.get_center(), UP), ""


@probe("P46", "Adding a piece of an on-screen mobject splits the parent; then self.remove(parent) leaves the pieces")
def _():
    s = Scene()
    t = MathTex("x + y + x", substrings_to_isolate=["x"])
    s.add(t)
    s.add(VGroup(*t.get_part_by_tex("x").family_members_with_points()))  # what animating a selection does
    split = t not in s.mobjects
    s.remove(t)
    left = len(s.get_mobject_family_members())
    s.remove(*t.get_family())
    return split and left > 0 and not s.mobjects, f"{left} family members left after remove(t)"


if __name__ == "__main__":
    for pid, ok, claim, info in RESULTS:
        print(f"{pid} {'PASS' if ok else 'FAIL'}  {claim}" + (f"   [{info}]" if info else ""))
    print(f"{sum(r[1] for r in RESULTS)}/{len(RESULTS)} claims hold")
