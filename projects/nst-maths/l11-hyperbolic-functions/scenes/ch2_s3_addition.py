"""Chapter 2, scene 3: cosh(A + B) through the complex door. Clips c2.add.1 – c2.add.4.

Opens with ch2_s1's docked dictionary card (rows only, rounded box, width 3.2, UR corner).
(94) is rewritten in place, step by step, into cosh(A + B) = cosh A cosh B + sinh A sinh B.
Ends on `handover_shot()`: the boxed result alone (ch2_s4 opens on it).
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
ctex, at_glyph = S4.ctex, S4.at_glyph

SZ = 50
XEQ = -1.9          # x of the line's "≡"
Y_LINE = 0.4        # the working line
Y_RES = -0.6        # the boxed result, final (handover) position
LHS = {
    "94": (r"\cos(A + B)", "BBBFYFYF"),
    "1": (r"\cos(iA + iB)", "BBBFPYFPYF"),
    "2": (r"\cos(i(A + B))", "BBBFPFYFYFF"),
    "3": (r"\cosh(A + B)", "TTTTFYFYF"),
    "8": (r"\cosh(A + B)", "TTTTFFFFF"),
}


def line(lhs, rhs, rpat, y=Y_LINE):
    src, pat = LHS[lhs]
    m = ctex(src + r" \equiv " + rhs, pat + "F" + rpat, size=SZ)
    return at_glyph(m, len(pat.replace(" ", "")), XEQ, y)


def docked_card():
    """ch2_s1's docked dictionary card: three rows, rounded box, width 3.2, top-right."""
    rows = VGroup()
    for i, (src, pat, _) in enumerate(S4.CARD_ROWS):
        rows.add(at_glyph(ctex(src, pat, size=40), 7, 0, -i * 0.74))
    frame = RoundedRectangle(corner_radius=0.2, width=rows.width + 0.6, height=rows.height + 0.5,
                             stroke_color=DIM, stroke_width=2).move_to(rows)
    card = VGroup(frame, rows)
    card.scale_to_fit_width(3.2).to_corner(UR, buff=0.25)
    card.frame, card.rows = frame, rows
    return card


def result_line(y=Y_RES):
    return line("8", r"\cosh A \cosh B + \sinh A \sinh B", "TTTTF TTTTF Y TTTTF TTTTF", y=y)


def result_box(m):
    return SurroundingRectangle(m, color=YELLOW, buff=0.3, stroke_width=3)


def handover_shot():
    """Last frame: cosh(A + B) ≡ cosh A cosh B + sinh A sinh B, boxed, at y = Y_RES."""
    m = result_line()
    return VGroup(m, result_box(m))


class Addition(NarratedScene):
    def construct(self):
        self.card = docked_card()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(2.5)
        self.play(*disappear(self.card, self.f94b, self.quote), run_time=1.0)
        self.wait(1.0)

    def pointer(self, row, target):
        f = self.card.frame
        start = np.array([f.get_left()[0] - 0.08, self.card.rows[row].get_y(), 0])
        end = target.get_top() + 0.15 * UP
        return CurvedArrow(start, end, angle=PI / 4, color=TEAL, stroke_width=4)

    # ------------------------------------------------------------ c2.add.1
    def clip1(self):
        card = self.card
        with self.say("c2.add.1") as c:
            self.play(FadeIn(card), run_time=1.0)
            f94 = line("94", r"\cos A \cos B - \sin A \sin B", "BBBY BBBY F BBBY BBBY")
            c.wait_until("start")
            self.play(*appear(f94, shift=None), run_time=1.2)
            g = f94[0]
            c.wait_until("formula")
            box = token_box(g[0:8], f94)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("equals cosine of A")
            self.play(Transform(box, token_box(g[9:17], f94)), run_time=1.0)
            c.wait_until("minus sine of A")
            self.play(Transform(box, token_box(g[17:26], f94)), run_time=1.0)
            cap = T("true for all complex A and B", size=32, color=DIM,
                    t2c={"A": YELLOW, "B": YELLOW}, t2s={"A": ITALIC, "B": ITALIC})
            cap.move_to([f94.get_x(), Y_LINE - 0.85, 0])
            c.wait_until("any complex")
            self.play(FadeOut(box), *appear(cap), run_time=1.0)
            a1 = MathTex(r"\cos z = \tfrac{1}{2}\left(e^{iz} + e^{-iz}\right)", font_size=40)
            a1[0][0:3].set_color(BLUE)
            a2 = MathTex(r"e^{a+b} = e^a e^b", font_size=40)
            note = T("for complex numbers too", size=30, color=DIM)
            a1.move_to([-1.0, -1.75, 0])
            a2.next_to(a1, DOWN, buff=0.45).align_to(a1, LEFT)
            note.next_to(a2, RIGHT, buff=0.5)
            c.wait_until("exponential forms")
            self.play(*appear(a1, shift=None), run_time=1.0)
            c.wait_until("rules for exponents")
            self.play(*appear(a2, shift=None), run_time=1.0)
            c.wait_until(own_word=note)
            self.play(*appear(note), run_time=1.0)
        self.f94, self.aside = f94, VGroup(cap, a1, a2, note)

    # ------------------------------------------------------------ c2.add.2
    def clip2(self):
        with self.say("c2.add.2") as c:
            l1 = line("1", r"\cos iA \cos iB - \sin iA \sin iB", "BBBPY BBBPY F BBBPY BBBPY")
            self.play(*edit(self.f94, l1), run_time=min(2.0, c.until("left")))
            c.wait_until("left")
            l2 = line("2", r"\cos iA \cos iB - \sin iA \sin iB", "BBBPY BBBPY F BBBPY BBBPY")
            c.wait_until("common factor")
            self.play(*during(disappear(*self.aside), 0, 0.5), *during(edit(l1, l2), 0.2, 1),
                      run_time=1.8)
            c.wait_until("dictleft")
            arrow = self.pointer(0, l2[0][0:11])
            self.play(Create(arrow), FlashAround(self.card.rows[0], color=TEAL, time_width=1.5),
                      run_time=1.2)
            l3 = line("3", r"\cos iA \cos iB - \sin iA \sin iB", "BBBPY BBBPY F BBBPY BBBPY")
            c.wait_until("is the cosh of the sum")
            self.play(*edit(l2, l3), run_time=1.5)
            c.wait_until("cos")
            self.play(Transform(arrow, self.pointer(0, l3[0][10:20])),
                      FlashAround(self.card.rows[0], color=TEAL, time_width=1.5), run_time=1.2)
            l4a = line("3", r"\cosh A \cos iB - \sin iA \sin iB", "TTTTY BBBPY F BBBPY BBBPY")
            c.wait_until("turns into cosh of A")
            self.play(*edit(l3, l4a), run_time=1.2)
            l4 = line("3", r"\cosh A \cosh B - \sin iA \sin iB", "TTTTY TTTTY F BBBPY BBBPY")
            c.wait_until("into cosh of B")
            self.play(*edit(l4a, l4), run_time=min(1.2, c.until(floor=0.6)))
        self.arrow, self.cur = arrow, l4

    # ------------------------------------------------------------ c2.add.3
    def clip3(self):
        arrow, l4 = self.arrow, self.cur
        with self.say("c2.add.3") as c:
            self.play(Transform(arrow, self.pointer(1, l4[0][21:31])),
                      FlashAround(VGroup(*l4[0][21:31]), time_width=1.5), run_time=1.2)
            l5a = line("3", r"\cosh A \cosh B - i \sinh A \sin iB", "TTTTY TTTTY F P TTTTY BBBPY")
            c.wait_until("turns into eye")
            self.play(FlashAround(self.card.rows[1], color=TEAL, time_width=1.5),
                      *edit(l4, l5a), run_time=1.5)
            l5 = line("3", r"\cosh A \cosh B - i \sinh A \, i \sinh B", "TTTTY TTTTY F P TTTTY P TTTTY")
            c.wait_until("and the sine of eye B")
            self.play(*edit(l5a, l5), run_time=1.5)
            l6 = line("3", r"\cosh A \cosh B - i^2 \sinh A \sinh B", "TTTTY TTTTY F PP TTTTY TTTTY")
            c.wait_until("product")
            self.play(*disappear(arrow), run_time=0.8)
            c.wait_until("two eyes")
            self.play(*edit(l5, l6), run_time=1.5)
            isq = ctex(r"i^2 = -1", "PP YYY", size=40)
            isq.next_to(l6[0][21:23], DOWN, buff=0.7).shift(0.3 * RIGHT)
            c.wait_until("isq")
            self.play(*appear(isq), run_time=1.0)
        self.cur, self.isq = l6, isq

    # ------------------------------------------------------------ c2.add.4
    def clip4(self):
        l6, isq = self.cur, self.isq
        with self.say("c2.add.4") as c:
            # {sign}: ring the minus alone; {minus}: it turns YELLOW (no second ring)
            self.play(FlashAround(l6[0][20], time_width=1.5), run_time=1.5)
            c.wait_until("minus")
            self.play(*recolor([l6[0][20]], YELLOW), run_time=1.0)
            c.wait_until("so minus")
            l7 = line("3", r"\cosh A \cosh B - (-1) \sinh A \sinh B", "TTTTY TTTTY Y FYFF TTTTY TTTTY")
            self.play(*edit(l6, l7), run_time=1.5)
            c.wait_until("plus")
            l8 = result_line(y=Y_LINE)
            self.play(*during(disappear(isq), 0, 0.4), *during(edit(l7, l8), 0.2, 1),
                      run_time=min(1.8, c.until("result")))
            rbox = result_box(l8)
            c.wait_until("result")
            self.play(GrowFromCenter(rbox), run_time=1.2)
            self.play(FlashAround(l8[0][20], time_width=1.5), run_time=1.2)
            c.wait_until("compare")
            f94b = line("94", r"\cos A \cos B - \sin A \sin B", "BBBF BBBF Y BBBF BBBF",
                        y=Y_RES + 1.35)
            f94b[0][4].set_color(FG)
            f94b[0][6].set_color(FG)
            self.play(*during([VGroup(l8, rbox).animate.shift((Y_RES - Y_LINE) * UP)], 0, 0.6),
                      *during([FadeIn(f94b, shift=0.4 * DOWN)], 0.5, 1),
                      run_time=min(2.0, c.until("lecturer")))
            quote = T("“minus sign is replaced with a plus sign”", size=34, color=FG,
                      t2c={"minus": YELLOW, "plus": YELLOW})
            quote.move_to([0, Y_RES - 1.45, 0])
            c.wait_until(own_word=quote)
            self.play(*appear(quote), run_time=1.0)
            self.play(FlashAround(f94b[0][17], time_width=1.5),
                      FlashAround(l8[0][20], time_width=1.5), run_time=1.5)
        self.f94b, self.quote = f94b, quote
