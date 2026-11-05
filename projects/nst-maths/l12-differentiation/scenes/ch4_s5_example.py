"""Chapter 4, scene 5: when most terms vanish (x^2 e^{-x}, tenth derivative). Clips c4.example.1 – c4.example.4.

Plan: c1 the hook's question (ch4_s1_hook.question()) at the top, f / g labels under its factors;
f's chain and g's chain as two stacked rows below (f: zeros DIM; g: minus signs flash YELLOW).
c2 board clears to s4's leibniz_card() at the top, the sum written out for general n under it;
the first term and the dots are dimmed and struck, the last three flash; row n of Pascal's
triangle under the sum, its last three entries (aligned under the surviving terms) YELLOW, their
values under them on "they are / then n / then one". c3 the general form built piece by piece,
a token box walking the polynomial, then n = 1 and the product rule with a GREEN tick.
c4 the general form shrinks to the top; s3's pascal_row(10), all but the last three dimmed; the
three feed 45·2, 10·2x·(−1), 1·x²; answer_box() under them; s1's counter_1024() small in the top
right on "thousand"; a DIM "Part 5" tag; fade to empty.

Exported for the recap: answer_box() = VGroup(eq, box); row_last3() = row ten, last three lit.
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


# --------------------------------------------------------------------------- sibling helpers
def _question():
    return load_scene("ch4_s1_hook").question()


def _counter():
    return load_scene("ch4_s1_hook").counter_1024()


def _card():
    return load_scene("ch4_s4_formula").leibniz_card()


def _pascal_row10():
    return load_scene("ch4_s3_pattern").pascal_row(10, size=42, pitch=1.0).move_to(ORIGIN)


# --------------------------------------------------------------------------- exported helpers
def answer_box():
    """The tenth derivative, boxed YELLOW. VGroup(eq, box); eq is a MathTex with parts
    [0] d^10/dx^10, [1] "(", [2] x^2 BLUE, [3] e^{-x} PURPLE, [4] ")", [5] "=",
    [6] e^{-x} PURPLE, [7] (x^2 - 20x + 90) BLUE. Built at ORIGIN, font 52."""
    eq = MathTex(r"\frac{d^{10}}{dx^{10}}", "(", "x^2", "e^{-x}", ")", "=",
                 "e^{-x}", r"\left(x^2 - 20x + 90\right)", font_size=52, color=FG)
    eq[2].set_color(BLUE)
    eq[3].set_color(PURPLE)
    eq[6].set_color(PURPLE)
    eq[7].set_color(BLUE)
    box = SurroundingRectangle(eq, color=YELLOW, buff=0.25, stroke_width=4)
    return VGroup(eq, box)


def row_last3():
    """Row ten of Pascal's triangle (s3's pascal_row(10)): 11 entries, [0..7] DIM, [8..10]
    (45, 10, 1) YELLOW. Built at ORIGIN."""
    row = _pascal_row10()
    entries = list(row)
    for e in entries[:-3]:
        e.set_color(DIM)
    for e in entries[-3:]:
        e.set_color(YELLOW)
    return row


# --------------------------------------------------------------------------- local pieces
def _factor_parts(q):
    """The x^2 and e^{-x} parts of s1's question (for the f / g labels)."""
    return q[2], q[3]


class Example(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c1: f runs out, g flips
    def clip1(self):
        with self.say("c4.example.1") as c:
            q = _question()
            q.scale_to_fit_width(min(q.width, 7.0)).move_to(UP * 2.2)
            self.play(*appear(q), run_time=1.2)  # early: the question returns as a whole
            fx, gx = _factor_parts(q)
            fl = MathTex("f", "=", "x^2", font_size=44, color=BLUE)
            gl = MathTex("g", "=", "e^{-x}", font_size=44, color=PURPLE)
            fl.move_to([fx.get_x() - 1.0, 0.75, 0])
            gl.move_to([gx.get_x() + 1.0, 0.75, 0])
            c.wait_until("The first factor")
            self.play(*appear(fl), run_time=1.0)
            c.wait_until("The second")
            self.play(*appear(gl), run_time=1.0)

            # the two chains, stacked rows, left-aligned
            fc = MathTex("x^2", r"\to", "2x", r"\to", "2", r"\to", "0", r"\to", "0", font_size=56, color=BLUE)
            gc = MathTex("e^{-x}", r"\to", "-", "e^{-x}", r"\to", "e^{-x}", r"\to", "-", "e^{-x}",
                         font_size=56, color=PURPLE)
            for i in (1, 3, 5, 7):
                fc[i].set_color(FG)
                gc[i].set_color(FG)
            fc[6].set_color(DIM)
            fc[8].set_color(DIM)
            fc.scale_to_fit_width(min(fc.width, 5.4)).move_to([-3.75, -1.2, 0])
            gc.scale_to_fit_width(min(gc.width, 6.6)).move_to([3.35, -1.2, 0])
            rows = VGroup(fc, gc)
            c.wait_until("runs")
            self.play(*fly(fl[2], fc[0]), run_time=1.5)
            c.wait_until("two ex")
            self.play(*appear(fc[1], fc[2], shift=None), run_time=0.9)
            c.wait_until("then two")
            self.play(*appear(fc[3], fc[4], shift=None), run_time=0.8)
            c.wait_until("then zero")
            self.play(*appear(fc[5], fc[6], fc[7], fc[8], shift=None, lag=0.3), run_time=1.3)
            c.wait_until("alt")
            self.play(*fly(gl[2], gc[0]), run_time=1.4)
            c.wait_until("flips")
            rt = max(0.8, c.until())
            self.play(*during(appear(*gc[1:], shift=None, lag=0.45), 0, 0.75),
                      *[x for i, a in ((2, 0.1), (7, 0.62))
                        for x in during(FlashAround(gc[i], color=YELLOW, time_width=1.5), a, a + 0.3)],
                      run_time=rt)
            settle(self, fc)
            settle(self, gc)
        self.q, self.fl, self.gl, self.rows = q, fl, gl, rows

    # ------------------------------------------------------------------ c2: only the last three
    def clip2(self):
        with self.say("c4.example.2") as c:
            card = _card()
            card.scale_to_fit_height(min(card.height, 1.5)).move_to(UP * 2.85)
            P = [r"\binom{n}{0}", r"f^{(n)}", "g", "+", r"\dots", "+",
                 r"\binom{n}{n-2}", "f''", r"g^{(n-2)}", "+",
                 r"\binom{n}{n-1}", "f'", r"g^{(n-1)}", "+",
                 r"\binom{n}{n}", r"f\,", r"g^{(n)}"]
            s = MathTex(*P, font_size=48, color=FG)
            for i in (1, 7, 11, 15):
                s[i].set_color(BLUE)
            for i in (2, 8, 12, 16):
                s[i].set_color(PURPLE)
            s.scale_to_fit_width(min(s.width, 12.6)).move_to(UP * 1.2)
            self.play(*disappear(self.fl, self.gl), *swap(self.q, card), run_time=1.4)
            c.wait_until("N minus M")
            self.play(FlashAround(card.fpart, color=YELLOW, time_width=1.5),
                      run_time=min(1.2, c.until("of the derivatives", floor=0.5)))
            c.wait_until("of the derivatives")
            self.play(*during(disappear(self.rows), 0, 0.4),
                      *during(appear(*[VGroup(*s[a:b]) for a, b in ((0, 3), (3, 6), (6, 10), (10, 14), (14, 17))],
                                     shift=None, lag=0.3), 0.35, 1.0),
                      run_time=max(1.0, min(2.2, c.until("zero") - 0.1)))
            # the appear() above put each term group on screen; gather them back into s
            settle(self, s)

            c.wait_until("zero")
            dead = [s[i] for i in range(0, 6)]
            strikes = [Line(VGroup(*s[0:3]).get_left() + LEFT * 0.08, VGroup(*s[0:3]).get_right() + RIGHT * 0.08,
                            color=RED, stroke_width=5)]
            self.play(*[m.animate.set_color(DIM) for m in dead],
                      *[Create(l) for l in strikes], run_time=1.5)
            c.wait_until("only the last three")
            live = VGroup(*s[6:17])
            self.play(FlashAround(live, color=YELLOW, time_width=1.5, buff=0.2),
                      *recolor([s[6], s[10], s[14]], YELLOW), run_time=2.0)

            # row n of Pascal's triangle, last three entries under the surviving binomials
            y_row = -0.5
            last = [MathTex(t, font_size=48, color=YELLOW) for t in
                    (r"\binom{n}{n-2}", r"\binom{n}{n-1}", r"\binom{n}{n}")]
            for m, k in zip(last, (6, 10, 14)):
                m.move_to([s[k].get_x(), y_row, 0])
            first = [MathTex(t, font_size=48, color=DIM) for t in (r"\binom{n}{0}", r"\binom{n}{1}", r"\cdots")]
            x0 = s[0].get_x()
            for m, x in zip(first, (x0, x0 + 1.25, x0 + 2.4)):
                m.move_to([x, y_row, 0])
            c.wait_until("row")
            self.play(*appear(*first, *last, shift=0.2 * DOWN, lag=0.15), run_time=1.6)

            vals = [MathTex(t, font_size=48, color=YELLOW) for t in (r"\frac{n(n-1)}{2}", "n", "1")]
            eqs = [MathTex("=", font_size=48, color=DIM).rotate(PI / 2) for _ in vals]
            for v, e, m in zip(vals, eqs, last):
                e.next_to(m, DOWN, buff=0.22)
                v.next_to(e, DOWN, buff=0.22)
            for (v, e), cue in zip(zip(vals, eqs), ("They are", "then N", "then one")):
                c.wait_until(cue)
                self.play(*appear(e, v, lag=0.2), run_time=min(0.9, c.until(floor=0.5)))

    # ------------------------------------------------------------------ c3: the general form, n = 1
    def clip3(self):
        with self.say("c4.example.3") as c:
            G = [r"\frac{d^n}{dx^n}", "(", "x^2", "e^{-x}", ")", "=", "(-1)^n", "e^{-x}",
                 r"\big(", "x^2", "-", "2nx", "+", "n(n-1)", r"\big)"]
            g = MathTex(*G, font_size=56, color=FG)
            g[2].set_color(BLUE)
            g[3].set_color(PURPLE)
            g[7].set_color(PURPLE)
            for i in range(8, 15):
                g[i].set_color(BLUE)
            g.scale_to_fit_width(min(g.width, 12.0)).move_to(UP * 1.3)
            lhs, sign, ex, poly = g[0:6], g[6], g[7], g[8:15]
            c.wait_until("You get")
            sweep_clear(self, time_span(FadeIn(VGroup(*lhs)), 0.6, 1.4),
                        time_span(FadeIn(sign), 1.3, 2.0), run_time=2.0)
            c.wait_until("times E to the minus ex")
            self.play(*appear(ex, shift=None), run_time=1.0)
            c.wait_until("short polynomial")
            self.play(*appear(*poly, shift=None, lag=0.05), run_time=1.2)
            settle(self, g)

            c.wait_until("It's ex squared")
            box = token_box(g[9], g, height=0.85)
            box.set_y(g[9].get_y())
            self.play(FadeIn(box), run_time=0.6)
            for k, cue in ((11, "minus two N ex"), (13, "plus N times")):
                c.wait_until(cue)
                nb = token_box(g[k], g, height=0.85).set_y(g[k].get_y())
                self.play(Transform(box, nb), run_time=0.8)

            # n = 1
            n1 = MathTex(r"n = 1:\;\;", "e^{-x}", r"\left(2x - x^2\right)", font_size=48, color=FG)
            n1[1].set_color(PURPLE)
            n1[2].set_color(BLUE)
            pr = MathTex("=", r"2x\,e^{-x} - x^2 e^{-x}", font_size=48, color=FG)
            tick = check_mark(GREEN)
            line = VGroup(n1, pr, tick).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.2)
            tag = T("product rule, part 2", size=30, color=DIM).next_to(pr[1], DOWN, buff=0.35)
            c.wait_until("n1")
            self.play(FadeOut(box), *appear(n1, shift=None), run_time=1.2)
            c.wait_until("which is the product rule")
            self.play(*during(appear(pr, tag, lag=0.3), 0, 0.75), *during(GrowFromCenter(tick), 0.7, 1.0),
                      run_time=max(1.0, min(1.8, c.until())))
        self.g, self.n1grp = g, VGroup(n1, pr, tick, tag)

    # ------------------------------------------------------------------ c4: n = 10, the answer
    def clip4(self):
        with self.say("c4.example.4") as c:
            g = self.g
            row = _pascal_row10()
            row.scale_to_fit_width(min(row.width, 10.5)).move_to(UP * 1.55)
            self.play(g.animate.scale(0.62).move_to(UP * 3.15),
                      time_span(FadeIn(row, shift=0.2 * DOWN), 0.7, 1.6), run_time=1.6)
            entries = list(row)
            c.wait_until("the last three numbers")
            self.play(*[e.animate.set_color(DIM) for e in entries[:-3]], run_time=1.0)

            sz = 48
            feeds = [MathTex(a, b, font_size=sz, color=FG) for a, b in
                     (("45", r"\cdot 2"), ("10", r"\cdot 2x \cdot (-1)"), ("1", r"\cdot x^2"))]
            for f in feeds:
                f[0].set_color(YELLOW)
            rests = [f[1] for f in feeds]
            fr = VGroup(*feeds).arrange(RIGHT, buff=0.8)
            fr.move_to([0, 0.15, 0]).align_to(row, RIGHT)
            # the numbers are the row's own glyphs, enlarged, where the feeds' numbers sit
            nums = [entries[k].copy().scale(f[0].height / entries[k].height).move_to(f[0])
                    for k, f in zip((-3, -2, -1), feeds)]
            c.wait_until("forty-five")
            self.play(*fly(entries[-3], nums[0]), *disappear(self.n1grp), run_time=1.0)
            self.play(*fly(entries[-2], nums[1]), run_time=0.8)
            self.play(*fly(entries[-1], nums[2]), run_time=0.8)
            self.play(*appear(*rests, shift=None, lag=0.2), run_time=min(1.0, c.until("answer", floor=0.5)))

            ab = answer_box()
            ab.scale_to_fit_width(min(ab.width, 10.0)).move_to(DOWN * 1.75)
            eq, box = ab
            c.wait_until("answer")
            self.play(*appear(eq, shift=0.2 * DOWN), run_time=1.4)
            c.wait_until("ninety")
            self.play(GrowFromCenter(box), run_time=1.0)

            cnt = _counter()
            cnt.scale(0.95).to_corner(UR, buff=0.4)
            c.wait_until("thousand")
            self.play(FadeIn(cnt, scale=0.8), run_time=1.0)
            tag = T("Part 5", size=32, color=DIM).to_corner(DR, buff=0.55)
            c.wait_until("later")
            self.play(*appear(tag), run_time=1.0)
