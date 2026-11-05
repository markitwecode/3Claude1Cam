"""Chapter 3, scene 1: hook: graphs and inverses. Clips c3.hook.1 – c3.hook.3.

Title card; ch2's sign-flip callback (cos/cosh(A + B)); the three definitions (ch1 colours) beside
empty axes with a "?"; x -> sinh x and the reverse arrow to "?", which becomes ln. Ends empty.
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
from lib.titles import title_card  # noqa: E402

S12 = load_scene("ch1_s2_define")
S13 = load_scene("ch1_s3_family")
ctex = S12.ctex

DEF_SZ = 56
DEF_X = -3.2
AX_C = np.array([3.7, 0.95, 0])
ROW1_Y, ROW2_Y = -2.2, -3.05


def tanh_def(size=DEF_SZ):
    # glyphs: 0-3 tanh, 4 x, 5 =, 6-11 numerator, 12 bar, 13-18 denominator
    return S13.mt(r"\tanh x = \dfrac{e^{x} - e^{-x}}{e^{x} + e^{-x}}", size,
                  cmap={(0, 4): TEAL, (6, 8): GOLD, (9, 12): PURPLE, (13, 15): GOLD, (16, 19): PURPLE})


def definitions():
    rows = [S13.cosh_def(DEF_SZ), S13.sinh_def(DEF_SZ), tanh_def()]
    for r, y in zip(rows, (2.0, 0.35, -1.75)):
        S13.at_glyph(r, 5, DEF_X - 1.2, y)   # '=' signs aligned
    return rows


def pulse(mobs, color, scale=1.2):
    """Scale-and-colour pulse that returns to rest: one anim per glyph (no wrapper, no stray strokes)."""
    glyphs = [g for m in mobs for g in m.family_members_with_points()]
    c = VGroup(*[g.copy() for g in glyphs]).get_center()
    return [g.animate(rate_func=there_and_back).scale(scale, about_point=c).set_color(color) for g in glyphs]


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        card = title_card("Part 3 · Graphs and inverses")
        card.title.scale_to_fit_width(min(card.title.width, 12.4))
        with self.say("c3.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.2)  # early: title card
            self.play(*appear(card.course, shift=None), run_time=1.0)  # early: title card
            c.wait_until("part three")
            self.play(*appear(card.part, shift=None), run_time=1.0)
            c.wait_until("last")
            cos = ctex(r"\cos(A + B) = \cos A \cos B - \sin A \sin B",
                       "BBBBBBBBF BBBBBBBB B BBBBBBBB", size=50)
            cosh = ctex(r"\cosh(A + B) = \cosh A \cosh B + \sinh A \sinh B",
                        "TTTTTTTTTF TTTTTTTTTT Y TTTTTTTTTT", size=50)
            S13.at_glyph(cos, 8, 0, 0.75)
            S13.at_glyph(cosh, 9, 0, -0.75)
            # centre the pair horizontally as a whole
            dx = -VGroup(cos, cosh).get_center()[0]
            cos.shift(dx * RIGHT)
            cosh.shift(dx * RIGHT)
            self.play(*during(disappear(card.title, card.rule, card.course, card.part), 0, 0.4),
                      *during(appear(cos, cosh, shift=None, lag=0.5), 0.4, 1), run_time=2.0)
            c.wait_until("sign flip")
            plus = cosh[0][20]
            self.play(*pulse([plus], "#FFF2A0", 1.4), *pulse([cos[0][17]], "#BFEFFF", 1.4), run_time=1.5)
            self.cos, self.cosh = cos, cosh

    def clip2(self):
        with self.say("c3.hook.2") as c:
            rows = definitions()
            self.play(*disappear(self.cos, self.cosh), run_time=0.8)
            for r in rows:
                self.play(*appear(r, shift=None), run_time=0.9)  # early: the three shown together
            c.wait_until("gold")
            cosh, sinh, tanh = rows
            golds = [S13.G(cosh, 10, 12), S13.G(sinh, 10, 12), S13.G(tanh, 6, 8), S13.G(tanh, 13, 15)]
            purples = [S13.G(cosh, 13, 16), S13.G(sinh, 13, 16), S13.G(tanh, 9, 12), S13.G(tanh, 16, 19)]
            self.play(*[a for g in golds for a in pulse([g], "#FFD9A8", 1.25)],   # ends before {purple}
                      run_time=max(0.5, min(1.0, c.until("purple") - 0.1)))
            c.wait_until("purple")
            self.play(*[a for p in purples for a in pulse([p], "#E2C4F5", 1.22)], run_time=1.4)
            c.wait_until("shape")
            ax = S12.graph_axes(x_length=5.6, y_length=4.6).move_to(AX_C)
            q = MathTex("?", font_size=110, color=YELLOW).move_to(ax.c2p(1.1, 2.6))
            self.play(Create(ax), run_time=1.5)
            self.play(*appear(q), run_time=0.8)
            c.wait_until("back")
            fwd = MathTex("x", r"\longrightarrow", r"\sinh x", font_size=50)
            fwd[0].set_color(FG)
            fwd[1].set_color(DIM)
            fwd[2].set_color(TEAL)
            fwd.move_to([AX_C[0], ROW1_Y, 0])
            self.play(*appear(fwd, shift=None), run_time=1.0)
            c.wait_until("find the")
            arr = MathTex(r"\longleftarrow", font_size=50, color=YELLOW)
            arr.move_to([fwd[1].get_x(), ROW2_Y, 0])
            ask = MathTex("?", font_size=56, color=YELLOW)
            ask.move_to([fwd[0].get_x(), ROW2_Y, 0])
            src = fwd[2].copy().set_color(TEAL)
            src.move_to([fwd[2].get_x(), ROW2_Y, 0])
            self.play(*fly(fwd[2], src), run_time=min(1.3, 0.35 * c.until()))
            self.play(GrowFromEdge(arr, RIGHT), *appear(ask, shift=None), run_time=min(1.0, 0.35 * c.until()))
            self.rows, self.ax, self.q, self.fwd = rows, ax, q, fwd
            self.arr, self.ask, self.src = arr, ask, src

    def clip3(self):
        with self.say("c3.hook.3") as c:
            self.play(self.ax.animate(rate_func=there_and_back).set_color(TEAL), run_time=1.5)
            c.wait_until("undo")
            self.play(*pulse([self.arr, self.src], "#FFF2A0", 1.08), run_time=1.5)
            c.wait_until("teaser")
            ln = MathTex(r"\ln", font_size=56, color=YELLOW).move_to(self.ask)
            ln.align_to(self.ask, DOWN).align_to(self.ask, RIGHT)
            self.play(*swap(self.ask, ln), run_time=1.2)
            self.play(*pulse([ln], "#FFF2A0", 1.3), run_time=1.5)
