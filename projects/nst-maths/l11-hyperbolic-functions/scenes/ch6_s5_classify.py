"""Chapter 6, scene 5: one equation, many shapes (the classification table). Clips c6.class.1 – c6.class.5.

The general equation ax^2 + bx + cy^2 + dy + e = 0 with today's three curves (the tilted ellipse
set aside: it has an xy term); completing the squares gives a(x - x0)^2 + c(y - y0)^2 = f (a, c
YELLOW, "coefficients, not the semi-axes"); dividing by f != 0 leads to the lecturer's table, filled
row by row in her order; then two tests: Example 36 lights the ellipse row, s4's y^2 - x^2 = s^2
lights the hyperbola row. Ends on the bare table (handover to ch6_s6_odd_cases).

Shared (import with load_scene("ch6_s5_classify")):
  classify_table(lit=None)   VGroup of 4 rows (circle, ellipse, hyperbola, no solution) in the
                             lecturer's order; .rows[i] has .name .cond .icon; lit=i adds that
                             row's GREEN light (name GREEN + box) as .light
  row_light(table, i)        the GREEN highlight box behind row i (z -1)
  handover_shot()            classify_table() where this scene leaves it (centre-left of frame)
  circle_icon(s) ellipse_icon(s) hyperbola_icon(s) updown_hyperbola_icon(s) empty_icon(s)
  tilted_ellipse_icon(s) ex36_ellipse_icon(s)   small icons at ORIGIN (s = 1: table size, ~1.3 wide)
"""
# style: 2
# handover: next
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

ROW_Y = [1.45, 0.45, -0.55, -1.55]
NAME_X = -6.3          # left edge of the row names
COND_X = -2.75         # left edge of the conditions
ICON_X = 4.3           # icon centres
BESIDE_X = 6.0         # the tested curve, beside its row
Y_TOP = 3.0            # the equation above the table
Y_KEY = -2.75


# ---------------------------------------------------------------- icons
def _faint(mob, op):
    """Dim a mix of stroked curves and filled glyphs without filling the curves."""
    for m in mob.family_members_with_points():
        if m.get_fill_opacity() > 0:
            m.set_fill(opacity=op)
        m.set_stroke(opacity=op * m.get_stroke_opacity())
    return mob


def _axes(s=1.0, w=1.4, h=0.9):
    return VGroup(Line(LEFT * w / 2 * s, RIGHT * w / 2 * s), Line(DOWN * h / 2 * s, UP * h / 2 * s)).set_stroke(DIM, 1.5)


def circle_icon(s=1.0):
    return VGroup(_axes(s), Circle(radius=0.36 * s).set_stroke(BLUE, 4))


def ellipse_icon(s=1.0):
    return VGroup(_axes(s), Ellipse(width=1.1 * s, height=0.6 * s).set_stroke(BLUE, 4))


def _hyp(s, updown=False):
    u = 0.3 * s
    T_ = math.asinh(1.5)
    branches = VGroup()
    for sg in (1, -1):
        if updown:
            f = (lambda t, sg=sg: np.array([u * math.sinh(t), sg * u * math.cosh(t), 0]))
        else:
            f = (lambda t, sg=sg: np.array([sg * u * math.cosh(t), u * math.sinh(t), 0]))
        branches.add(ParametricFunction(f, t_range=[-T_, T_]).set_stroke(TEAL, 4))
    L = 1.8 * u
    asym = VGroup(DashedLine([-L, -L, 0], [L, L, 0], dash_length=0.06),
                  DashedLine([-L, L, 0], [L, -L, 0], dash_length=0.06)).set_stroke(FG, 1.5, opacity=0.5)
    return VGroup(_axes(s, 1.2, 1.2), asym, branches)


def hyperbola_icon(s=1.0):
    """s2's x^2 - y^2 = s^2 (s = 1): TEAL branches left and right, dashed dim-white asymptotes."""
    return _hyp(s)


def updown_hyperbola_icon(s=1.0):
    """s4's y^2 - x^2 = s^2 (s = 1): the branches open up and down."""
    return _hyp(s, updown=True)


def empty_icon(s=1.0):
    return MathTex(r"\emptyset", font_size=52 * s, color=RED)


def tilted_ellipse_icon(s=1.0):
    """ch5 s4's tilted ellipse: GOLD semi-major and GREEN semi-minor tilting with it."""
    ang = 30 * DEGREES
    e = Ellipse(width=1.3 * s, height=0.7 * s).set_stroke(BLUE, 4)
    major = Line(ORIGIN, RIGHT * 0.65 * s).set_stroke(GOLD, 3)
    minor = Line(ORIGIN, UP * 0.35 * s).set_stroke(GREEN, 3)
    g = VGroup(e, major, minor).rotate(ang, about_point=ORIGIN)
    return VGroup(_axes(s, 1.6, 1.1), g)


def ex36_ellipse_icon(s=1.0):
    """Example 36's tall ellipse: centre (-1, 3) YELLOW, semi-major 2 (GOLD, along y), semi-minor
    sqrt 2 (GREEN, along x)."""
    u = 0.22 * s
    a, b = math.sqrt(2) * u, 2 * u
    e = Ellipse(width=2 * a, height=2 * b).set_stroke(BLUE, 4)
    major = Line(ORIGIN, UP * b).set_stroke(GOLD, 3)
    minor = Line(ORIGIN, RIGHT * a).set_stroke(GREEN, 3)
    dot = Dot(ORIGIN, radius=0.05 * s, color=YELLOW)
    return VGroup(e, major, minor, dot)


# ---------------------------------------------------------------- the table
ROWS = [
    ("circle", r"a = c\ \ \text{and}\ \ f/a > 0", circle_icon),
    ("ellipse", r"a\cdot c > 0\ \ \text{and}\ \ a\cdot f > 0,\ \ a \neq c", ellipse_icon),
    ("hyperbola", r"a\cdot c < 0\,,\ \ f \neq 0", hyperbola_icon),
    ("no solution", r"a\cdot c > 0\ \ \text{and}\ \ a\cdot f < 0", empty_icon),
]


def row_light(table, i):
    r = table.rows[i]
    box = RoundedRectangle(corner_radius=0.12, width=ICON_X + 0.85 - (NAME_X - 0.25), height=0.9)
    box.set_stroke(GREEN, 2.5).set_fill(GREEN, 0.12)
    box.move_to([(ICON_X + 0.85 + NAME_X - 0.25) / 2, r.name.get_y(), 0]).set_z_index(-1)
    return box


def classify_table(lit=None):
    rows = []
    for (name, cond, icon_f), y in zip(ROWS, ROW_Y):
        n = T(name, size=38)
        n.move_to([0, y, 0]).align_to([NAME_X, 0, 0], LEFT)
        c = MathTex(cond, font_size=42)
        c.move_to([0, y, 0]).align_to([COND_X, 0, 0], LEFT)
        ic = icon_f(1.0).move_to([ICON_X, y, 0])
        r = VGroup(n, c, ic)
        r.name, r.cond, r.icon = n, c, ic
        rows.append(r)
    t = VGroup(*rows)
    t.rows = rows
    if lit is not None:
        rows[lit].name.set_color(GREEN)
        t.light = row_light(t, lit)
        t.add(t.light)
    return t


def handover_shot():
    return classify_table()


# ---------------------------------------------------------------- scene
class Ch6S5Classify(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.ending()

    # general equation + today's curves; the tilted one set aside
    def clip1(self):
        with self.say("c6.class.1") as c:
            icons = [circle_icon(1.7), ellipse_icon(1.7), hyperbola_icon(1.7)]
            for ic, x in zip(icons, (-4.6, -1.9, 0.8)):
                ic.move_to([x, -1.1, 0])
            self.play(*appear(*icons, lag=0.35), run_time=min(1.8, c.until("fits one")))
            c.wait_until("fits one")
            eq = MathTex("a", "x^2", "+", "b", "x", "+", "c", "y^2", "+", "d", "y", "+", "e", "=", "0",
                         font_size=64).move_to([0, 1.7, 0])
            self.play(*appear(eq), run_time=1.2)
            c.wait_until("terms")

            def bx(parts):
                g = VGroup(*parts)
                r = Rectangle(width=g.width + 0.3, height=eq.height + 0.4)
                r.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).move_to([g.get_x(), eq.get_y(), 0]).set_z_index(-1)
                return r
            box = bx(eq[0:2])
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("plus some number times ex")
            self.play(Transform(box, bx(eq[3:5])), run_time=0.8)
            c.wait_until("the same two kinds")
            self.play(Transform(box, bx(eq[6:11])), run_time=0.9)
            c.wait_until("plus a constant")
            self.play(Transform(box, bx(eq[12:13])), run_time=0.8)
            c.wait_until("all equal")
            self.play(Transform(box, bx(eq[13:15])), run_time=0.8)
            c.wait_until("noxy")
            tilt = tilted_ellipse_icon(1.7).move_to([4.3, -1.1, 0])
            _faint(tilt, 0.5)
            note = T("has an xy term: not here", size=30, color=DIM).next_to(tilt, DOWN, buff=0.35)
            self.play(FadeOut(box), *appear(tilt), run_time=1.0)
            c.wait_until("ex times why")
            self.play(*appear(note), run_time=1.0)
        self.eq, self.icons, self.tilt, self.note = eq, icons, tilt, note

    # complete the squares: a(x - x0)^2 + c(y - y0)^2 = f
    def clip2(self):
        eq = self.eq
        with self.say("c6.class.2") as c:
            c.wait_until("just as in")
            sweep_clear(self, eq.animate.scale(0.75).move_to([0, 3.1, 0]), keep=[eq],
                        run_time=min(1.6, c.until("form")))
            full = MathTex("a", "(x - x_0)^2", "+", "c", "(y - y_0)^2", "=", "f", font_size=64).move_to([0, 1.2, 0])
            fx, fp, fy, fe = VGroup(full[0], full[1]), full[2], VGroup(full[3], full[4]), VGroup(full[5], full[6])
            bx_ = Brace(eq[0:5], DOWN, buff=0.12, color=BLUE)
            by_ = Brace(eq[6:11], DOWN, buff=0.12, color=BLUE)
            c.wait_until("form")
            self.play(GrowFromCenter(bx_), run_time=0.8)
            self.play(*appear(fx, shift=0.4 * DOWN), run_time=1.2)
            c.wait_until("plus a multiple")
            self.play(GrowFromCenter(by_), run_time=0.8)
            self.play(*appear(fp, fy, shift=0.4 * DOWN), run_time=1.2)
            c.wait_until("equal to a constant")
            self.play(*appear(fe, shift=0.4 * DOWN), run_time=1.1)
            c.wait_until("names")
            self.play(*recolor(full[0], YELLOW), *recolor(full[3], YELLOW), run_time=1.0)
            self.play(*flash([full[0], full[3]]), run_time=1.2)
            c.wait_until("careful")
            tag = T("a, c: coefficients, not the semi-axes", size=36, color=RED).move_to([0, -0.2, 0])
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("these letters are coefficients")
            ell = Ellipse(width=2.6, height=1.4).set_stroke(BLUE, 3)
            amaj = Line(ORIGIN, RIGHT * 1.3).set_stroke(GOLD, 3)
            bmin = Line(ORIGIN, UP * 0.7).set_stroke(GREEN, 3)
            pic = VGroup(ell, amaj, bmin).move_to([-2.2, -2.3, 0])
            la = MathTex(r"a", font_size=36, color=GOLD).next_to(amaj, DOWN, buff=0.1)
            lb = MathTex(r"b", font_size=36, color=GREEN).next_to(bmin, RIGHT, buff=0.1)
            t1 = T("semi-major axis", size=30, color=GOLD)
            t2 = T("semi-minor axis", size=30, color=GREEN)
            words = VGroup(t1, t2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([1.6, -2.3, 0])
            ghost = _faint(VGroup(pic, la, lb, words), 0.5)
            self.play(*appear(ghost, shift=None), run_time=1.0)  # early: ch5's labels, a ghost to be crossed out
            c.wait_until("not the semi-major")
            cross = Cross(ghost, stroke_color=RED, stroke_width=6)
            self.play(Create(cross), run_time=1.0)
        self.form = VGroup(fx, fp, fy, fe)
        self.full = full

    # divide by f: the table's shape, then the ellipse and circle rows
    def clip3(self):
        with self.say("c6.class.3") as c:
            keep = list(self.form)
            sweep_clear(self, keep=keep, run_time=1.0)
            div = MathTex(r"\frac{a}{f}", r"(x - x_0)^2", "+", r"\frac{c}{f}", r"(y - y_0)^2", "=", "1",
                          font_size=52)
            div[0][0].set_color(YELLOW)
            div[3][0].set_color(YELLOW)
            fnz = MathTex(r"f \neq 0", font_size=44, color=GOLD)
            VGroup(div, fnz).arrange(RIGHT, buff=1.0).move_to([0, Y_TOP, 0])
            self.play(*appear(fnz), run_time=0.9)
            c.wait_until("and divide")
            self.play(*swap(self.form, div), run_time=1.4)
            table = classify_table()
            for r in table.rows:
                r.name.set_color(DIM)
            c.wait_until("decide")
            self.play(*appear(*[r.name for r in table.rows], lag=0.25), run_time=1.4)  # early: the table's shape first, walked next
            c.wait_until("same")
            e = table.rows[1]
            self.play(*appear(e.cond), *recolor(e.name, FG), run_time=1.4)
            c.wait_until("that's an ellipse")
            self.play(*appear(e.icon, shift=None), run_time=1.0)
            c.wait_until("circle")
            ci = table.rows[0]
            self.play(*appear(ci.cond), *recolor(ci.name, FG), run_time=1.3)
            self.play(*appear(ci.icon, shift=None), run_time=1.0)
        self.table, self.div, self.fnz = table, div, fnz

    # hyperbola and no-solution rows, then the key
    def clip4(self):
        t = self.table
        with self.say("c6.class.4") as c:
            h = t.rows[2]
            self.play(*appear(h.cond), *recolor(h.name, FG), run_time=1.4)
            c.wait_until("that's a hyperbola")
            self.play(*appear(h.icon, shift=None), run_time=1.0)
            c.wait_until("neg")
            n = t.rows[3]
            self.play(*appear(n.cond), *recolor(n.name, FG), run_time=1.5)
            c.wait_until("no solution at all")
            self.play(*appear(n.icon, shift=None), run_time=1.0)
            c.wait_until("sheet")
            k1 = MathTex(r"a\cdot c > 0\text{:\ same sign}", font_size=38)
            k2 = MathTex(r"a\cdot c < 0\text{:\ opposite signs}", font_size=38)
            key = VGroup(k1, k2).arrange(RIGHT, buff=1.4).move_to([0, Y_KEY, 0])
            c.wait_until("same sign")
            self.play(*appear(k1), run_time=1.0)
            c.wait_until("opposite signs")
            self.play(*appear(k2), run_time=1.0)
        self.key = key

    # two tests
    def clip5(self):
        t = self.table
        with self.say("c6.class.5") as c:
            self.play(*disappear(self.div, self.fnz), run_time=1.0)
            c.wait_until("ex36")
            l1 = MathTex(r"2x^2 + 4x + y^2 - 6y + 7 = 0", font_size=42).move_to([0, 3.4, 0])
            l2 = MathTex(r"2(x + 1)^2 + (y - 3)^2 = 4", font_size=46).move_to([0, 2.55, 0])
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("two times a square")
            derive(self, l1, l2, run_time=2.0)
            c.wait_until("read")
            rd = MathTex(r"a = 2,\quad c = 1,\quad f = 4", font_size=46, color=GOLD).move_to([0, Y_KEY, 0])
            self.play(*swap(self.key, rd), run_time=1.3)
            c.wait_until("verdict")
            e = t.rows[1]
            light = row_light(t, 1)
            self.play(FadeIn(light), *recolor(e.name, GREEN), run_time=1.2)
            c.wait_until("so it's an ellipse")
            tall = ex36_ellipse_icon(1.0).move_to([BESIDE_X, ROW_Y[1], 0])
            self.play(*appear(tall, shift=None), run_time=1.0)
            c.wait_until("turned")
            turned = MathTex(r"y^2 - x^2 = s^2", font_size=56).move_to([0, Y_TOP, 0])
            self.play(*swap(VGroup(l1, l2), turned), *disappear(light, tall), *recolor(e.name, FG),
                      run_time=1.4)
            c.wait_until("verdict2")
            rd2 = MathTex(r"a = -1,\quad c = 1", font_size=46, color=GOLD).move_to([0, Y_KEY, 0])
            self.play(*swap(rd, rd2), run_time=1.3)
            c.wait_until("with opposite signs")
            h = t.rows[2]
            light2 = row_light(t, 2)
            self.play(FadeIn(light2), *recolor(h.name, GREEN), run_time=1.1)
            c.wait_until("so it's a hyperbola")
            ud = updown_hyperbola_icon(1.0).move_to([BESIDE_X, ROW_Y[2], 0])
            self.play(*appear(ud, shift=None), run_time=1.0)
        self.leftover = (turned, rd2, light2, ud)

    def ending(self):
        turned, rd2, light2, ud = self.leftover
        h = self.table.rows[2]
        self.wait(1.2)
        self.play(*disappear(turned, rd2, light2, ud), *recolor(h.name, FG), run_time=1.0)
        self.wait(1.0)
