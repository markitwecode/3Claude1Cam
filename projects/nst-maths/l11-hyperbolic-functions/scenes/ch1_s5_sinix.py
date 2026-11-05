"""Chapter 1, scene 5: sin(ix) = i sinh x and tan(ix) = i tanh x. Clips c1.sinix.1 – c1.sinix.5.

Opens on ch1_s4_cosix's handover shot (dictionary card, header + row 1, small, top-right) and
grows it to three rows. Ends on `handover_shot()`: dictionary_card(rows=3); ch1_s6_dictionary
opens on it.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S4 = load_scene("ch1_s4_cosix")
ctex, at_glyph, grp, dictionary_card = S4.ctex, S4.at_glyph, S4.grp, S4.dictionary_card
CARD_ROWS = S4.CARD_ROWS


def handover_shot():
    """Last frame of this scene / first of ch1_s6_dictionary: the full card, small, top-right."""
    return dictionary_card(rows=3)


# ---------------------------------------------------------------- derivation lines
SRC_SINZ = (r"\sin z = \frac{e^{iz} - e^{-iz}}{2i}", "BBBFF GPGF UUPU FFP")
SRC_B = (r"\sin(ix) = \frac{e^{-x} - e^{x}}{2i}", "BBBFPFFF UUU F GG FFP")
SRC_C = (r"= -\frac{e^{x} - e^{-x}}{2i}", "FY GG F UUU FFP")
SRC_C2 = (r"= -\frac{1}{2i}\left(e^{x} - e^{-x}\right)", "FY FFFP F GG F UUU F")
SRC_D = (r"= \frac{i}{2}\left(e^{x} - e^{-x}\right)", "F PFF F GG F UUU F")
SRC_E = (r"= i \cdot \frac{1}{2}\left(e^{x} - e^{-x}\right)", "F P F FFF F GG F UUU F")
SRC_F = (r"= i \sinh x", "F P TTTTF")
SRC_P1 = (r"\frac{1}{i}", "FFP")
SRC_P2 = (r"= \frac{1 \cdot i}{i \cdot i}", "F FFP F PFP")
SRC_P3 = (r"= \frac{i}{i^2}", "F P F PF")
SRC_P4 = (r"= \frac{i}{-1}", "F P F FF")
SRC_P5 = (r"= -i", "F FP")
SRC_SLIP = r"\sin(ix) = -i \sinh x"
SRC_T0 = (r"\tan(ix) = \frac{\sin(ix)}{\cos(ix)}", "BBBFPFFF BBBFPFF F BBBFPFF")
SRC_T1 = (r"= \frac{i \sinh x}{\cosh x}", "F PTTTTF F TTTTF")
SRC_T2 = (r"= i \tanh x", "F P TTTTF")

XEQ = -3.6                     # x of the column's "=" signs
ROW_Y = [2.3, 0.5, -1.3]       # rows of the derivation column
SZ = 52
PX, PY = 2.9, [-0.3, -1.45, -2.6]   # 1/i panel: "=" column and rows
XEQ5, ROW5 = -1.2, [1.9, 0.0, -1.8]  # tan column


class SinIx(NarratedScene):
    def born(self, src, dst, si=0, di=0):
        """A copy of src fades in on dst's row (dropping a little), then is edited into dst."""
        cp = src.copy().shift((dst[0][di].get_y() - src[0][si].get_y()) * UP)
        self.play(FadeIn(cp, shift=0.4 * DOWN), run_time=0.8)
        self.play(*edit(cp, dst), run_time=1.4)

    def construct(self):
        card = handover_shot_s4 = S4.handover_shot()
        self.add(handover_shot_s4)
        row2, row3 = card.all_rows[1], card.all_rows[2]

        # ---------------------------------------------------------------- 1: sin z, z = ix
        with self.say("c1.sinix.1") as c:
            sinz = at_glyph(ctex(*SRC_SINZ, size=SZ), 4, XEQ, ROW_Y[0])
            self.play(*appear(sinz), run_time=1.0)
            c.wait_until("E to the eye zed")
            self.play(FlashAround(grp(sinz, 5, 8), color=GOLD, run_time=1.3, time_width=1.5))
            c.wait_until("minus E to the minus eye zed")
            self.play(FlashAround(grp(sinz, 9, 13), color=PURPLE, run_time=1.3, time_width=1.5))
            tag = ctex(r"z = ix", "YYPY", size=48).move_to([0.9, ROW_Y[0] + 0.1, 0])
            c.wait_until("sub")
            self.play(*appear(tag), run_time=1.0)
            b = at_glyph(ctex(*SRC_B, size=SZ), 7, XEQ, ROW_Y[1])
            c.wait_until("the two exponentials")
            self.born(sinz, b, si=4, di=7)
            order = T("order matters", size=34, color=YELLOW).move_to([0.75, ROW_Y[1], 0])
            c.wait_until("backwards")
            self.play(FlashAround(b[0][11], run_time=1.3, time_width=1.5),
                      *during(appear(order), 0.3, 1), run_time=1.3)
            c.wait_until("E to the minus ex")
            self.play(FlashAround(grp(b, 8, 11), color=PURPLE, run_time=1.2, time_width=1.5))
            c.wait_until("minus E to the ex")
            self.play(FlashAround(grp(b, 12, 14), color=GOLD, run_time=1.2, time_width=1.5))

        # ---------------------------------------------------------------- 2: pull out a minus
        with self.say("c1.sinix.2") as c:
            cc = at_glyph(ctex(*SRC_C, size=SZ), 0, XEQ, ROW_Y[2])
            self.born(b, cc, si=7)
            c2 = at_glyph(ctex(*SRC_C2, size=SZ), 0, XEQ, ROW_Y[2])
            c.wait_until("the bracket reads")
            self.play(*edit(cc, c2), run_time=1.5)
            c.wait_until("in front sits")
            self.play(FlashAround(grp(c2, 1, 6), run_time=1.4, time_width=1.5))
            c.wait_until("slow")
            self.play(*set_alpha([sinz, b, tag, card], DIMMED), *disappear(order), run_time=1.0)

        # ---------------------------------------------------------------- 3: 1/i = -i
        with self.say("c1.sinix.3") as c:
            frame = RoundedRectangle(corner_radius=0.2, width=5.2, height=3.9)
            frame.set_stroke(DIM, 2).move_to([3.9, -1.45, 0])
            p1 = ctex(*SRC_P1, size=48).move_to([PX - 0.6, PY[0], 0])
            self.play(*appear(frame, p1, shift=0.6 * LEFT, lag=0.2), run_time=1.2)
            p2 = at_glyph(ctex(*SRC_P2, size=48), 0, PX, PY[0])
            c.wait_until("mult")
            self.play(*appear(p2), run_time=1.0)
            p3 = at_glyph(ctex(*SRC_P3, size=48), 0, PX, PY[1])
            top3, bot3 = VGroup(*p3[0][0:3]), VGroup(*p3[0][3:5])
            c.wait_until("The top becomes eye")
            self.play(*appear(top3), run_time=0.9)
            c.wait_until("The bottom becomes")
            self.play(*appear(bot3), run_time=0.9)
            self.remove(top3, bot3)
            self.add(p3)
            p4 = ctex(*SRC_P4, size=48)
            at_glyph(p4, 0, p3.get_right()[0] + 0.55, PY[1])
            c.wait_until("which is minus one")
            self.play(*appear(p4), run_time=0.9)
            p5 = at_glyph(ctex(*SRC_P5, size=48), 0, PX, PY[2])
            box5 = SurroundingRectangle(grp(p5, 1, 3), color=GREEN, buff=0.15, stroke_width=4)
            c.wait_until("result")
            self.play(*appear(p5), run_time=0.9)
            self.play(GrowFromCenter(box5), run_time=0.8)
            c.wait_until("cancel")
            self.play(*flash([c2[0][1], p5[0][1]]), run_time=1.2)
            d = at_glyph(ctex(*SRC_D, size=SZ), 0, XEQ, ROW_Y[2])
            self.play(*edit(c2, d), run_time=1.5)
            c.wait_until("The two minus signs")
            self.play(FlashAround(grp(d, 1, 4), run_time=1.3, time_width=1.5))

        # ---------------------------------------------------------------- 4: = i sinh x
        with self.say("c1.sinix.4") as c:
            e = at_glyph(ctex(*SRC_E, size=SZ), 0, XEQ, ROW_Y[2])
            self.play(*edit(d, e), run_time=1.5)
            c.wait_until("half the difference")
            self.play(*recolor(list(e[0][3:14]), TEAL), FlashAround(grp(e, 3, 14), color=TEAL),
                      run_time=1.3)
            f = at_glyph(ctex(*SRC_F, size=SZ), 0, XEQ, ROW_Y[2])
            c.wait_until("And half their difference")
            self.play(*edit(e, f), run_time=1.5)
            res = ctex(*CARD_ROWS[1][:2], size=64).move_to([-3.2, 0.9, 0])
            box = SurroundingRectangle(res, color=YELLOW, buff=0.3, stroke_width=4)
            n91 = T("(91)", size=34, color=DIM).next_to(box, RIGHT, buff=0.3)
            c.wait_until("boxed")
            self.play(*during(disappear(sinz, b, tag), 0, 0.4), *during(edit(f, res), 0.3, 0.85),
                      *during([GrowFromCenter(box), FadeIn(n91)], 0.8, 1), run_time=2.2)
            self.play(*set_alpha([card], 1), *appear(row2.tex, row2.num, shift=None, lag=0.2), run_time=1.4)
            c.wait_until("extra")
            self.play(FlashAround(res[0][8], color=PINK, run_time=1.4, time_width=1.5),
                      FlashAround(card.rows[0].tex, color=BLUE, run_time=1.4, time_width=1.5))
            slip = MathTex(SRC_SLIP, font_size=52, color=RED).move_to([-3.2, -1.6, 0])
            c.wait_until("slip")
            self.play(*appear(slip), run_time=1.0)
            x_out = Cross(slip, stroke_color=RED, stroke_width=6)
            back = Arrow(slip.get_right() + 0.2 * RIGHT, box5.get_left(), buff=0.15,
                         color=YELLOW, stroke_width=5)
            c.wait_until("go back")
            self.play(Create(x_out), GrowArrow(back), run_time=1.0)

        # ---------------------------------------------------------------- 5: tan(ix) = i tanh x
        with self.say("c1.sinix.5") as c:
            t0 = at_glyph(ctex(*SRC_T0, size=56), 7, XEQ5, ROW5[0])
            sweep_clear(self, *appear(t0), keep=[card, row2], run_time=1.6)
            t1 = at_glyph(ctex(*SRC_T1, size=56), 0, XEQ5, ROW5[1])
            eqbar = VGroup(t1[0][0], t1[0][7])
            num, den = VGroup(*t1[0][1:7]), VGroup(*t1[0][8:13])
            c.wait_until("ratio")
            self.play(FlashAround(grp(row2.tex, 8, 14), run_time=1.4, time_width=1.5),
                      *during(appear(eqbar, num, shift=None), 0.3, 1), run_time=1.4)
            self.play(FlashAround(grp(card.rows[0].tex, 8, 13), run_time=1.3, time_width=1.5),
                      *during(appear(den, shift=None), 0.3, 1), run_time=1.3)
            self.remove(num, den, eqbar)
            self.add(t1)
            t2 = at_glyph(ctex(*SRC_T2, size=56), 0, XEQ5, ROW5[2])
            c.wait_until("tanh")
            self.born(t1, t2)
            res2 = ctex(*CARD_ROWS[2][:2], size=64).move_to([-0.8, -0.3, 0])
            box2 = SurroundingRectangle(res2, color=YELLOW, buff=0.3, stroke_width=4)
            n92 = T("(92)", size=34, color=DIM).next_to(box2, RIGHT, buff=0.3)
            c.wait_until("boxed2")
            self.play(*during(disappear(t0, t1), 0, 0.4), *during(edit(t2, res2), 0.3, 0.85),
                      *during([GrowFromCenter(box2), FadeIn(n92)], 0.8, 1), run_time=2.2)
            self.play(*appear(row3.tex, row3.num, shift=None, lag=0.2), run_time=1.2)

        keep = set(card.get_family()) | set(row2.get_family()) | set(row3.get_family())
        rest = [m for m in self.mobjects if m not in keep]
        self.play(*disappear(*rest), run_time=1.0)
        self.wait(1.0)
