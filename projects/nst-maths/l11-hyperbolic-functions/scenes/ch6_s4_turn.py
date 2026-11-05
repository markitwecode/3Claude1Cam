"""Chapter 6, scene 4: a quarter turn, y² − x² = s². Clips c6.turn.1 – c6.turn.2.

Left half: s2's picture (make_axes / make_branches / make_asymptotes, scaled by K), minus branch
PURPLE as in s3, labelled x = ±s cosh θ, y = s sinh θ and x² − y² = s². Centre top: (102) edited to
x² − y² = −s², then the terms cross to y² − x² = s². Right half: a copy of the left reflects in the
mirror y = x; a ghost turns a quarter turn onto it; vertices s / −s; asymptotes shared;
x = s sinh θ, y = ±s cosh θ. Caption: Figure 28.

Shared with the recap:
  two_orientation_shot()   the final two-picture frame (both halves, labels, caption)
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch6_s2_hyperbola")

K = 0.76                                  # shrink of s2's picture
LC = np.array([-3.55, 0.6, 0.0])          # left picture centre (maths origin)
RC = np.array([3.55, 0.6, 0.0])           # right picture centre
U = S2.H / 4 * K                          # world units per maths unit
TOP_Y, PAR_Y, EQ_Y, CAP_Y = 3.35, -2.05, -2.7, -3.3


# ---------------------------------------------------------------- builders
def left_picture():
    """s2's s = 1 picture, scaled into the left half: .axes .asym .branches (.right TEAL, .left PURPLE)."""
    g = VGroup()
    g.axes = S2.make_axes()
    g.asym = S2.make_asymptotes()
    g.branches = S2.make_branches()
    g.branches.left.set_stroke(PURPLE)
    g.add(g.axes, g.asym, g.branches)
    g.scale(K, about_point=S2.C).shift(LC - S2.C)
    return g


def full_picture():
    """The same picture at s2's own size and place (where this scene picks it up)."""
    g = left_picture()
    g.shift(S2.C - LC).scale(1 / K, about_point=S2.C)
    return g


def right_picture():
    """y² − x² = s²: the left picture reflected in y = x: .axes .asym .branches (top TEAL, bottom PURPLE)."""
    g = VGroup()
    g.axes = S2.make_axes()
    g.asym = S2.make_asymptotes()
    g.branches = S2.make_branches()
    g.branches.left.set_stroke(PURPLE)
    g.add(g.axes, g.asym, g.branches)
    g.scale(K, about_point=S2.C).shift(RC - S2.C)
    g.branches.rotate(PI / 2, about_point=RC)
    return g


def vertex_marks():
    dots = VGroup(Dot(RC + U * UP, radius=0.09, color=YELLOW), Dot(RC + U * DOWN, radius=0.09, color=YELLOW))
    labs = VGroup(set_backstroke(MathTex("s", font_size=36, color=YELLOW).move_to(RC + U * np.array([-0.4, 1.5, 0]))),
                  set_backstroke(MathTex("-s", font_size=36, color=YELLOW)
                                 .move_to(RC + U * np.array([-0.2, -1.9, 0]), aligned_edge=RIGHT)))
    return dots, labs


def left_param():
    m = MathTex(r"x = ", r"\pm", r"s", r"\cosh", r"\theta,\quad y = s", r"\sinh", r"\theta", font_size=36)
    m[1].set_color(YELLOW)
    return m.move_to([LC[0], PAR_Y, 0])


def right_param():
    m = MathTex(r"x = s", r"\sinh", r"\theta,", r"\quad y =", r"\pm", r"s", r"\cosh", r"\theta", font_size=36)
    m[4].set_color(YELLOW)
    return m.move_to([RC[0], PAR_Y, 0])


def eq_parts(first, second, size):
    return MathTex(first, "-", second, "=", "s^2", font_size=size)


def left_eq():
    return eq_parts("x^2", "y^2", 36).move_to([LC[0], EQ_Y, 0])


def right_eq():
    return eq_parts("y^2", "x^2", 36).move_to([RC[0], EQ_Y, 0])


def caption():
    return T("Figure 28: Hyperbolae at different orientations.", 28, color=DIM).move_to([0, CAP_Y, 0])


def two_orientation_shot():
    """The final frame: x² − y² = s² (left) beside y² − x² = s² (right), labels, caption."""
    dots, labs = vertex_marks()
    return VGroup(left_picture(), left_param(), left_eq(),
                  right_picture(), dots, labs, right_param(), right_eq(), caption())


# ---------------------------------------------------------------- scene
class QuarterTurn(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        with self.say("c6.turn.1") as c:
            pic = full_picture()
            eq = MathTex("x^2", "-", "y^2", "=", "s^2", font_size=56).move_to([0, TOP_Y, 0])
            self.play(FadeIn(pic), run_time=1.0)
            self.play(*appear(eq), run_time=1.0)
            c.wait_until("What if")
            self.play(pic.animate.shift(LC - S2.C).scale(K, about_point=LC), run_time=1.4)
            self.pic = pic
            self.lpar, self.leq = left_param(), left_eq()
            self.play(*appear(self.lpar, self.leq, lag=0.4), run_time=min(1.2, c.until("neg")))

            c.wait_until("neg")
            eq2 = MathTex("x^2", "-", "y^2", "=", "-", "s^2", font_size=56).move_to([0, TOP_Y, 0])
            eq2[4].set_color(YELLOW)
            eq2[5].set_color(YELLOW)
            self.play(*edit(eq, eq2), run_time=1.5)
            c.wait_until("across")

            eq3 = MathTex("y^2", "-", "x^2", "=", "s^2", font_size=56).move_to([0, TOP_Y, 0])
            self.play(eq2[0].animate(path_arc=-0.9 * PI).move_to(eq3[2]),
                      eq2[2].animate(path_arc=-0.9 * PI).move_to(eq3[0]),
                      eq2[1].animate.move_to(eq3[1]), eq2[3].animate.move_to(eq3[3]),
                      *during([FadeOut(eq2[4])], 0, 0.45),
                      eq2[5].animate.move_to(eq3[4]).set_color(FG),
                      run_time=2.0)
            self.remove(*eq2.get_family())
            self.add(eq3)
            self.eq = eq3
            c.wait_until("swap")
            xs = [eq3[2][0], eq3[0][0], self.leq[0][0], self.leq[2][0]]
            self.play(*recolor(xs, YELLOW), *flash(xs, run_time=1.5, time_width=1.5), run_time=1.5)

    def clip2(self):
        with self.say("c6.turn.2", gap=1.0) as c:
            L = self.pic
            raxes = L.axes.copy().shift(RC - LC)
            img = VGroup(L.asym.copy(), L.branches.copy())
            self.play(FadeIn(raxes), img.animate.shift(RC - LC), run_time=1.4)
            mirror = Line(RC + 2.0 * U * DL * 1.35, RC + 2.0 * U * UR * 1.35).set_stroke(YELLOW, 6, opacity=0.45)
            mirror.set_z_index(-1)
            mtag = set_backstroke(MathTex("y = x", font_size=32, color=YELLOW)).next_to(mirror.get_end(), UP, buff=0.1)
            c.wait_until("line")
            self.play(FadeIn(mirror), *appear(mtag), run_time=0.8)
            self.play(Rotate(img, angle=PI, axis=np.array([1.0, 1.0, 0.0]), about_point=RC),
                      run_time=min(1.8, max(0.8, c.until("quarter") - 0.1)))

            c.wait_until("quarter")
            ghost = L.branches.copy().shift(RC - LC).set_stroke(FG, opacity=0.35)
            self.play(FadeIn(ghost), run_time=0.6)
            self.play(Rotate(ghost, angle=PI / 2, about_point=RC), run_time=1.8)
            self.play(FadeOut(ghost), *disappear(mtag), FadeOut(mirror), run_time=min(0.8, c.until("updown")))

            c.wait_until("updown")
            rasym, rbr = img[0], img[1]
            req = right_eq()
            self.play(*[VShowPassingFlash(b.copy().set_stroke(YELLOW, 8), time_width=0.5) for b in rbr],
                      *fly(self.eq, req), run_time=1.5)

            c.wait_until("vertices")
            dots, labs = vertex_marks()
            self.play(*[GrowFromCenter(d) for d in dots], run_time=0.8)
            c.wait_until("at S")
            self.play(*appear(*labs, lag=0.4), run_time=1.0)

            c.wait_until("asym")
            lines = [L.asym.up, L.asym.down, rasym[0], rasym[1]]
            cap = caption()
            self.play(*[VShowPassingFlash(Line(m.get_start(), m.get_end()).set_stroke(YELLOW, 7), time_width=0.6)
                        for m in lines],
                      *[m.animate.set_stroke(YELLOW, opacity=0.9) for m in lines], run_time=1.5)
            self.play(*appear(cap, shift=None), run_time=0.8)  # early: the notes' caption, under both pictures

            c.wait_until("param2")
            lp = self.lpar
            trade = [lp[3], lp[5]]
            self.play(*recolor(trade, YELLOW), *flash(trade, run_time=1.2, time_width=1.5),
                      *[m.animate.set_stroke(FG, opacity=0.55) for m in lines], run_time=1.2)
            rp = right_param()
            rp[1].set_color(YELLOW)
            rp[6].set_color(YELLOW)
            c.wait_until("Ex equals S")
            self.play(*appear(rp[0], rp[2], shift=None, lag=0), *fly(lp[5], rp[1], arc=-0.5),
                      run_time=1.5)
            c.wait_until("and why equals")
            self.play(*appear(rp[3], rp[4], rp[5], rp[7], shift=None, lag=0), *fly(lp[3], rp[6], arc=-0.4),
                      run_time=1.5)
            c.wait_until()
