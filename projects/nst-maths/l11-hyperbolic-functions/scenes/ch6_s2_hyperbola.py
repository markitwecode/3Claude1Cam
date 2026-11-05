"""Chapter 6, scene 2: flip one sign, x² − y² = s², the hyperbola. Clips c6.flip.1 – c6.flip.5.

Axes −4..4 (window half-size H world units, centred at C). Left column: (102), s = 1, the root,
the band, then the quarter-pieces one per mark (lecturer's labels), joined into two TEAL branches
with YELLOW vertices; general s (|x| ≥ |s|, vertices s / −s, GOLD 2s brace); asymptotes y = ±x with
a marker riding the right branch while the window zooms out to ±16 and back.

Shared with ch6 s3, s4, s6 and the recap (all at the un-zoomed framing unless R is given):
  to_world(x, y, R=4)         maths point -> scene point (window ±R)
  make_axes(R=4)              the two DIM axis lines
  make_branches(s=1, R=4)     VGroup(.right, .left), both TEAL (s3 recolours .left PURPLE)
  quarter_piece(sx, sy, s, R) one quarter of the curve, drawn outward from the vertex
  make_asymptotes(R=4)        dashed dim-white y = x, y = −x (.up, .down)
  quarter_labels()            the four labels (.tr .tl .br .bl), signs YELLOW
  handover_shot()             axes + s = 1 branches + asymptotes: this scene's last frame
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

C = np.array([0.7, -0.05, 0.0])      # centre of the axes
H = 2.9                              # half-size of the window in scene units
LX0 = -6.4                           # left edge of the text column
LCOL_R = -2.5                        # right edge of the text column
RCOL_L = 3.85                        # left edge of the right column
EQ_Y, ROOT_Y, CAP_Y, ROW1_Y, ROW2_Y, ROW3_Y = 3.4, 2.55, 1.65, 0.75, -0.1, -0.75


def to_world(x, y, R=4):
    return C + (H / R) * np.array([x, y, 0.0])


def make_axes(R=4):
    return VGroup(Line(C + H * LEFT, C + H * RIGHT),
                  Line(C + H * DOWN, C + H * UP)).set_stroke(DIM, 2)


def quarter_piece(sx, sy, s=1, R=4, color=TEAL, width=4):
    tm = float(np.arccosh(R / s))
    return ParametricFunction(lambda t: to_world(sx * s * np.cosh(t), sy * s * np.sinh(t), R),
                              t_range=[0, tm, 0.02]).set_stroke(color, width)


def _branch(sign, s=1, R=4, color=TEAL, width=4):
    tm = float(np.arccosh(R / s))
    return ParametricFunction(lambda t: to_world(sign * s * np.cosh(t), s * np.sinh(t), R),
                              t_range=[-tm, tm, 0.02]).set_stroke(color, width)


def make_branches(s=1, R=4, color=TEAL):
    g = VGroup()
    g.right = _branch(1, s, R, color)
    g.left = _branch(-1, s, R, color)
    g.add(g.right, g.left)
    return g


def make_asymptotes(R=4):
    g = VGroup()
    g.up = DashedLine(C + H * (DL), C + H * (UR), dash_length=0.14, dashed_ratio=0.55)
    g.down = DashedLine(C + H * (UL), C + H * (DR), dash_length=0.14, dashed_ratio=0.55)
    g.add(g.up, g.down)
    g.set_stroke(FG, 2.5, opacity=0.55)
    return g


def _qlabel(sign, cond):
    m = MathTex(sign, r"\sqrt{x^2 - 1},\ " + cond, font_size=32)
    m[0].set_color(YELLOW)
    return m


def quarter_labels():
    g = VGroup()
    g.tr = _qlabel("+", "x > 1")
    g.tr.move_to([RCOL_L, C[1] + 1.0, 0], aligned_edge=LEFT)
    g.br = _qlabel("-", "x > 1")
    g.br.move_to([RCOL_L, C[1] - 1.0, 0], aligned_edge=LEFT)
    g.tl = _qlabel("+", "x < -1")
    g.tl.move_to([LCOL_R, C[1] + 1.0, 0], aligned_edge=RIGHT)
    g.bl = _qlabel("-", "x < -1")
    g.bl.move_to([LCOL_R, C[1] - 1.0, 0], aligned_edge=RIGHT)
    g.add(g.tr, g.tl, g.br, g.bl)
    return g


def handover_shot():
    return VGroup(make_axes(), make_branches(), make_asymptotes())


def _left(m, y):
    return m.move_to([LX0, y, 0], aligned_edge=LEFT)


def _eq(rhs, color=FG):
    m = MathTex(r"x^2 - y^2 =", rhs, font_size=48)
    m[1].set_color(color)
    return _left(m, EQ_Y)


def _root(rad, gold_last=False):
    m = MathTex(r"y =", r"\pm", r"\sqrt{x^2 - " + rad + "}", font_size=44)
    m[1].set_color(YELLOW)
    if gold_last:
        m[2][-1].set_color(GOLD)
    return _left(m, ROOT_Y)


class FlipSign(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        keep = handover_shot()
        self.remove(*self.mobjects)
        self.add(keep)
        self.wait(1.0)

    # ------------------------------------------------------------ the equation, s = 1, the root
    def clip1(self):
        with self.say("c6.flip.1") as c:
            self.axes = make_axes()
            self.eq = _eq("s^2")
            self.tag102 = T("(102)", 30, color=DIM).next_to(self.eq, RIGHT, buff=0.45)
            self.play(FadeIn(self.axes), *appear(self.eq, self.tag102, lag=0.3), run_time=1.2)
            c.wait_until("where S is")
            self.cap = _left(T("s: a non-zero\nreal constant", 28, color=DIM, line_spacing=0.8), CAP_Y)
            self.play(*appear(self.cap), run_time=1.0)
            c.wait_until("one")
            eq1 = _eq("1", GOLD)
            self.play(*edit(self.eq, eq1), run_time=min(1.5, 0.6 * c.until("solve")))
            self.eq = eq1
            c.wait_until("solve")
            self.play(FlashAround(self.eq, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("root")
            self.root = _root("1", gold_last=True)
            self.play(FlashUnder(self.eq, color=YELLOW, time_width=1.5),
                      *during(appear(self.root, shift=0.4 * DOWN), 0.3, 1), run_time=min(1.6, c.until(floor=1.0)))

    # ------------------------------------------------------------ real only for |x| >= 1
    def clip2(self):
        with self.say("c6.flip.2") as c:
            self.cond = _left(MathTex(r"x^2 \ge 1", font_size=44), ROW1_Y)
            self.play(FlashUnder(self.root, color=YELLOW, time_width=1.5), *appear(self.cond), run_time=1.5)
            c.wait_until("band")
            cond2 = _left(MathTex(r"x \ge 1\ \ \text{or}\ \ x \le -1", font_size=44), ROW2_Y)
            self.band = Rectangle(width=2 * H / 4, height=2 * H).move_to(C).set_stroke(width=0)
            self.band.set_fill(RED, 0.16).set_z_index(-2)
            self.band_lbl = T("no real y", 30, color=RED).next_to(to_world(0, 4), UP, buff=0.25)
            self.play(*appear(cond2), FadeIn(self.band), run_time=1.4)
            self.cond2 = cond2
            c.wait_until("In the band")
            self.play(*appear(self.band_lbl), run_time=1.0)

    # ------------------------------------------------------------ four quarter-pieces -> hyperbola
    def clip3(self):
        with self.say("c6.flip.3") as c:
            self.play(*disappear(self.cond, self.cond2), run_time=0.8)
            L = quarter_labels()
            P = {k: quarter_piece(sx, sy) for k, sx, sy in
                 (("tr", 1, 1), ("tl", -1, 1), ("br", 1, -1), ("bl", -1, -1))}
            c.wait_until("tr")
            self.play(*appear(L.tr), run_time=1.0)
            c.wait_until("That's this piece")
            self.play(Create(P["tr"]), run_time=2.0)
            c.wait_until("tl")
            self.play(*appear(L.tl), run_time=1.0)
            self.play(Create(P["tl"]), run_time=1.5)
            c.wait_until("bottom")
            self.play(*appear(L.br, L.bl, lag=0.2), Create(P["br"]), Create(P["bl"]),  # early: both bottom labels named together
                      run_time=min(1.8, c.until("join")))
            c.wait_until("join")
            self.branches = make_branches()
            self.remove(*P.values())
            self.add(self.branches)
            self.vdots = VGroup(Dot(to_world(1, 0), radius=0.1, color=YELLOW),
                                Dot(to_world(-1, 0), radius=0.1, color=YELLOW)).set_z_index(2)
            self.vlab = self._vlabels("1", "-1")
            self.play(VShowPassingFlash(self.branches.right.copy().set_stroke(YELLOW, 7), time_width=0.5),
                      VShowPassingFlash(self.branches.left.copy().set_stroke(YELLOW, 7), time_width=0.5),
                      GrowFromCenter(self.vdots[0]), GrowFromCenter(self.vdots[1]), run_time=1.8)
            self.play(*appear(self.vlab, lag=0.2), run_time=1.0)  # early: the vertex values, read with the join
            c.wait_until("name")
            self.hname = T("hyperbola", 44, color=TEAL).move_to([5.25, 2.3, 0])
            self.fig = T("Figure 27: Simple hyperbola given by x² − y² = 1.", 28, color=DIM)
            self.fig.move_to([C[0], -3.38, 0])
            self.play(*during(disappear(L.tr, L.tl, L.br, L.bl), 0, 0.4),
                      *during(appear(self.hname, self.fig, lag=0.4), 0.45, 1),
                      run_time=min(2.0, c.until(floor=1.0)))

    def _vlabels(self, a, b):
        return VGroup(MathTex(a, font_size=36).move_to(to_world(0.55, 0.45)),
                      MathTex(b, font_size=36).move_to(to_world(-0.6, 0.45)))

    # ------------------------------------------------------------ general s
    def clip4(self):
        with self.say("c6.flip.4") as c:
            eqs = _eq("s^2")
            roots = _root("s^2")
            self.play(*edit(self.eq, eqs), *edit(self.root, roots), run_time=1.5)
            self.eq, self.root = eqs, roots
            c.wait_until("cond")
            self.cond = _left(MathTex(r"|x| \ge |s|", font_size=44), ROW1_Y)
            self.play(*appear(self.cond), run_time=1.0)
            c.wait_until("pos")
            self.spos = MathTex(r"s > 0", font_size=44, color=GOLD).next_to(self.cond, RIGHT, buff=0.6)
            self.play(*appear(self.spos), *disappear(self.fig), run_time=1.0)
            c.wait_until("vertices")
            vl2 = self._vlabels("s", "-s")
            self.play(*swap(self.vlab[0], vl2[0]), *swap(self.vlab[1], vl2[1]),
                      *flash(list(self.vdots), color=YELLOW), run_time=1.5)
            self.vlab = vl2
            c.wait_until("gap")
            self.brace = span_brace(to_world(-1, 0), to_world(1, 0), DOWN, color=GOLD)
            self.gap2s = set_backstroke(MathTex("2s", font_size=40, color=GOLD).next_to(self.brace, DOWN, buff=0.12))
            self.play(GrowFromCenter(self.brace), *appear(self.gap2s), run_time=1.4)

    # ------------------------------------------------------------ asymptotes, zoom out and back
    def clip5(self):
        with self.say("c6.flip.5") as c:
            c.wait_until("far")
            self.play(*disappear(self.band, self.band_lbl, self.brace, self.gap2s, self.vlab, self.vdots,
                                 self.spos, self.hname), run_time=1.0)
            ap1 = _left(MathTex(r"x^2 - s^2 \approx x^2", font_size=44), ROW2_Y)
            note = _left(T("not in the notes", 28, color=DIM, slant=ITALIC), ROW3_Y)
            self.play(*appear(ap1, note, lag=0.4), run_time=1.2)
            c.wait_until("close")
            ap2 = _left(MathTex(r"\sqrt{x^2 - s^2} \approx |x|", font_size=44), ROW2_Y)
            self.play(*edit(ap1, ap2), run_time=min(1.5, 0.6 * c.until("lines")))
            c.wait_until("lines")
            asym = make_asymptotes()
            self.play(FadeIn(asym), run_time=1.2)

            R = ValueTracker(4.0)
            xm = ValueTracker(1.6)
            dyn = always_redraw(lambda: make_branches(1, R.get_value()))
            self.remove(self.branches)
            self.add(dyn)
            dot = always_redraw(lambda: Dot(to_world(xm.get_value(), np.sqrt(xm.get_value() ** 2 - 1),
                                                     R.get_value()), radius=0.11, color=YELLOW).set_z_index(3))
            gapl = always_redraw(lambda: Line(to_world(xm.get_value(), np.sqrt(xm.get_value() ** 2 - 1),
                                                       R.get_value()),
                                              to_world(xm.get_value(), xm.get_value(), R.get_value()))
                                 .set_stroke(GOLD, 5))
            self.play(FadeIn(dot), FadeIn(gapl), run_time=0.6)
            self.play(R.animate.set_value(16.0), xm.animate.set_value(14.0),
                      run_time=max(1.0, c.until("name2") - 0.2), rate_func=smooth)
            c.wait_until("name2")
            lbl = T("asymptotes", 36).move_to([5.3, 2.4, 0])
            self.play(*appear(lbl), run_time=1.0)
            for m in (dot, gapl):
                m.clear_updaters()
            self.play(FadeOut(dot), FadeOut(gapl), run_time=0.8)
            self.remove(dot, gapl)
            back = max(1.0, min(2.5, c.until(floor=1.0) - 0.1))
            hold = c.until(floor=0.3) - back
            if hold > 0.3:
                self.wait(hold)
            self.play(R.animate.set_value(4.0), run_time=back)
        dyn.clear_updaters()
        self.remove(dyn)
        self.add(self.branches)
        self.play(*disappear(self.eq, self.tag102, self.cap, self.root, self.cond, ap2, note, lbl), run_time=1.0)
