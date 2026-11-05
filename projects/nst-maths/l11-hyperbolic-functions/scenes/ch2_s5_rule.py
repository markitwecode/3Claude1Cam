"""Chapter 2, scene 5: the sign-flip rule (Osborn's rule). Clips c2.rule.1 – c2.rule.4.

Module-level builders for reuse (s6, recap):
  tan_formula(h, plus)  tan(A+B) / tanh(A+B) as a VGroup(lhs, VGroup(num, bar, den)).
  prediction_shot()     the predicted tanh(A+B) formula (TEAL, YELLOW + underneath) with its
                        YELLOW "prediction?" tag: VGroup(formula, tag), formula centred at (0, 0.3).
  row5()                scene 4's list row 5: BLUE parent -> TEAL child, YELLOW changed sign.
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
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- builders
def mtex(*parts, size=56, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def frac_of(n, d, color, gap=0.14):
    """A fraction from two MathTex pieces: VGroup(num, bar, den)."""
    w = max(n.width, d.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3.5, color=color)
    n.next_to(bar, UP, buff=gap)
    d.next_to(bar, DOWN, buff=gap)
    return VGroup(n, bar, d)


def tan_formula(h=False, plus=False, size=56):
    f = r"\tanh" if h else r"\tan"
    col = TEAL if h else BLUE
    lhs = mtex(f + r"(A+B)", "=", size=size, color=col)
    n = mtex(f + r" A + " + f + r" B", size=size, color=col)
    d = mtex("1", "+" if plus else "-", f + r" A\, " + f + r" B", size=size, color=col)
    if plus:
        d[1].set_color(YELLOW)
    fr = frac_of(n, d, col)
    fr.next_to(lhs, RIGHT, buff=0.3)
    fr.shift(UP * (lhs[1].get_y() - fr[1].get_y()))
    return VGroup(lhs, fr)


PRED_CENTER = np.array([0, 0.3, 0])


def prediction_shot():
    g = tan_formula(h=True, plus=True).move_to(PRED_CENTER)
    tag = T("prediction?", 36, YELLOW).next_to(g, UP, buff=0.45).align_to(g, RIGHT)
    return VGroup(g, tag)


def row5(size=44):
    parent = mtex("1", "+", r"\tan^2 z", r"\equiv", r"\sec^2 z", size=size, color=BLUE)
    arrow = MathTex(r"\longrightarrow", font_size=size, color=DIM)
    child = mtex("1", "-", r"\tanh^2 z", r"\equiv", r"\operatorname{sech}^2 z", size=size, color=TEAL)
    child[1].set_color(YELLOW)
    return VGroup(parent, arrow, child).arrange(RIGHT, buff=0.45)


RULE_LINES = [
    "The basic pattern is that to get the hyperbolic",
    "identity you simply take the corresponding circular",
    "trigonometric identity, replace 'cos' by 'cosh',",
    "'sin' by 'sinh' etc., and then wherever there is",
    "a product of two 'sinh' functions (also implied,",
    "as in tanh²), change the sign.",
]


def rule_box():
    lines = VGroup(*[T(s, 34) for s in RULE_LINES]).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    box = SurroundingRectangle(lines, color=DIM, buff=0.4).set_stroke(DIM, 2)
    return VGroup(box, lines).move_to(UP * 0.35)


def strip():
    s1 = VGroup(T("1 · rename", 30),
                MathTex(r"\cos", r"\to", r"\cosh", font_size=34))
    s1[1][0].set_color(BLUE)
    s1[1][1].set_color(DIM)
    s1[1][2].set_color(TEAL)
    s1[1].next_to(s1[0], RIGHT, buff=0.3)
    s2 = T("2 · flip the sign of every sinh × sinh", 30, YELLOW)
    steps = VGroup(s1, s2).arrange(RIGHT, buff=1.0)
    box = Rectangle(width=12.8, height=0.85).set_stroke(DIM, 2).move_to(UP * 3.3)
    steps.move_to(box)
    return box, s1, s2


def outline(m, buff=0.12):
    return SurroundingRectangle(m, color=YELLOW, buff=buff).set_stroke(YELLOW, 3)


class RuleScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ the boxed rule
    def clip1(self):
        rb = rule_box()
        box, lines = rb
        self.rb = rb
        with self.say("c2.rule.1") as c:
            self.play(Create(box), *appear(*lines, lag=0.15, shift=None),  # early: the notes' boxed rule, shown whole then walked
                      run_time=min(2.0, c.until("take")))
            c.wait_until("take")
            take = [select(lines[1], "take the corresponding circular")[0],
                    select(lines[2], "trigonometric identity")[0]]
            self.play(*[a for g in take for a in recolor(g, BLUE)], run_time=1.0)
            c.wait_until("rename")
            ren = [select(lines[2], "replace 'cos' by 'cosh'")[0],
                   select(lines[3], "'sin' by 'sinh' etc.")[0]]
            self.play(*[a for g in ren for a in recolor(g, TEAL)],
                      *[FlashUnder(g, color=TEAL, time_width=1.5) for g in ren], run_time=1.5)
            c.wait_until("flip")
            fl = [select(lines[3], "wherever there is")[0],
                  select(lines[4], "a product of two 'sinh' functions")[0],
                  select(lines[5], "change the sign")[0]]
            self.play(*[a for g in fl for a in recolor(g, YELLOW)],
                      *[FlashUnder(g, color=YELLOW, time_width=1.5) for g in fl], run_time=1.6)
            c.wait_until("name")
            cap = T("usually called Osborn's rule (the name is not in the notes)", 30, DIM,
                    t2c={"Osborn's rule": YELLOW})
            cap.next_to(box, DOWN, buff=0.4)
            self.cap = cap
            self.play(*appear(cap), run_time=1.0)

    # ------------------------------------------------------------ test 1: the circle
    def clip2(self):
        sbox, s1, s2 = strip()
        self.s1, self.s2, self.sbox = s1, s2, sbox
        box, lines = self.rb
        eq = mtex(r"\cos^2 x", "+", r"\sin^2 x", r"\equiv 1", size=60, color=BLUE).move_to(UP * 0.9)
        with self.say("c2.rule.2") as c:
            cap_to = self.cap.copy().move_to(UP * 2.45)
            self.play(*during(disappear(lines), 0, 0.45),
                      *during([ReplacementTransform(box, sbox),
                               self.cap.animate.move_to(cap_to)], 0.3, 1.0), run_time=1.3)
            self.play(*appear(s1, s2, lag=0.3, shift=None), *during(appear(eq), 0.3, 1.0),
                      run_time=min(1.5, c.until("cos2")))
            c.wait_until("cos2")
            eq_b = mtex(r"\cosh^2 x", "+", r"\sin^2 x", r"\equiv 1", size=60, color=BLUE).move_to(eq)
            eq_b[0].set_color(TEAL)
            self.play(*edit(eq, eq_b), *flash([s1]), run_time=1.5)
            c.wait_until("sin2")
            eq_c = mtex(r"\cosh^2 x", "+", r"\sinh^2 x", r"\equiv 1", size=60, color=TEAL).move_to(eq)
            self.play(*edit(eq_b, eq_c), run_time=1.5)
            c.wait_until("which is shine times shine")
            br = Brace(eq_c[2], DOWN, buff=0.15, color=DIM)
            prod = mtex(r"\sinh x \cdot \sinh x", size=48, color=TEAL).next_to(br, DOWN, buff=0.25)
            pbox = outline(prod)
            self.play(GrowFromCenter(br), *during(appear(prod), 0.3, 1.0),
                      *during([FadeIn(pbox)], 0.7, 1.0), *during(disappear(self.cap), 0, 0.5),
                      run_time=1.6)
            unf = VGroup(br, prod, pbox)
            settle(self, unf)
            c.wait_until("flipped")
            eq_d = mtex(r"\cosh^2 x", "-", r"\sinh^2 x", r"\equiv 1", size=60, color=TEAL).move_to(eq)
            eq_d[1].set_color(YELLOW)
            self.play(*edit(eq_c, eq_d), *flash([s2]), run_time=1.5)
            self.play(FlashAround(eq_d[1], color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("check")
            b93 = mtex(r"\cosh^2 x - \sinh^2 x \equiv 1", size=52, color=TEAL)
            r93 = SurroundingRectangle(b93, color=YELLOW, buff=0.3).set_stroke(YELLOW, 3)
            n93 = T("(93)", 30, DIM).next_to(r93, LEFT, buff=0.4)
            g93 = VGroup(r93, b93, n93).move_to(DOWN * 1.5)
            g93.shift(RIGHT * 12)
            self.add(g93)
            self.play(*during(disappear(unf), 0, 0.4),
                      *during([g93.animate.shift(LEFT * 12)], 0.3, 1.0), run_time=1.6)
            tick = check_mark().next_to(r93, RIGHT, buff=0.4)
            self.play(*appear(tick, shift=None), run_time=0.8)

    # ------------------------------------------------------------ test 2: the hidden product
    def clip3(self):
        sbox_keep = [self.sbox, self.s1, self.s2]
        with self.say("c2.rule.3") as c:
            c.wait_until("product")
            sweep_clear(self, keep=sbox_keep, run_time=1.2)
            c.wait_until("tan2")
            eq = mtex("1", "+", r"\tan^2 z", r"\equiv", r"\sec^2 z", size=60, color=BLUE).move_to(UP * 1.3)
            self.play(*appear(eq), run_time=1.0)
            c.wait_until("unfold")
            eq_b = mtex("1", "+", r"\tanh^2 z", r"\equiv", r"\operatorname{sech}^2 z",
                        size=60, color=TEAL).move_to(eq)
            self.play(*edit(eq, eq_b), *flash([self.s1]), run_time=1.1)
            fr = frac_of(mtex(r"\sinh^2 z", size=48, color=TEAL), mtex(r"\cosh^2 z", size=48, color=TEAL), TEAL)
            br = Brace(eq_b[2], DOWN, buff=0.15, color=DIM)
            fr.next_to(br, DOWN, buff=0.25)
            self.play(GrowFromCenter(br), *during(appear(fr), 0.3, 1.0), run_time=1.5)
            c.wait_until("a shine times shine")
            nbox = outline(fr[0], buff=0.1)
            self.play(FadeIn(nbox), run_time=0.9)
            unf = VGroup(br, fr, nbox)
            settle(self, unf)
            c.wait_until("flips")
            eq_c = mtex("1", "-", r"\tanh^2 z", r"\equiv", r"\operatorname{sech}^2 z",
                        size=60, color=TEAL).move_to(eq)
            eq_c[1].set_color(YELLOW)
            self.play(*edit(eq_b, eq_c), *flash([self.s2]), run_time=min(1.2, c.until("result")))
            c.wait_until("result")
            row = row5().move_to(DOWN * 2.6)
            row.shift(RIGHT * 12)
            self.add(row)
            self.play(row.animate.shift(LEFT * 12), run_time=1.6)
            c.wait_until("the line from the family list")
            tick = check_mark().next_to(row, RIGHT, buff=0.35)
            self.play(*appear(tick, shift=None), FlashAround(row[2], color=GREEN, run_time=1.2), run_time=1.2)
            c.wait_until("secant")
            sec = VGroup(mtex(r"\sec^2 z =", size=48, color=BLUE),
                         frac_of(mtex("1", size=48, color=BLUE), mtex(r"\cos^2 z", size=48, color=BLUE), BLUE))
            sec[1].next_to(sec[0], RIGHT, buff=0.2)
            sec[1].shift(UP * (sec[0].get_y() - sec[1][1].get_y()))
            sec.next_to(eq_c[4], DOWN, buff=0.7).set_x(eq_c[4].get_x() + 0.3)
            self.play(*during(disappear(unf), 0, 0.45), *during(appear(sec), 0.5, 1.0), run_time=1.3)
            c.wait_until("no sine in it")
            nos = T("no sin", 32, GREEN).next_to(sec, RIGHT, buff=0.4)
            self.play(*appear(nos), FlashAround(eq_c[4], color=GREEN, run_time=1.2), run_time=1.2)

    # ------------------------------------------------------------ prediction: tan(A + B)
    def clip4(self):
        keep = [self.sbox, self.s1, self.s2]
        with self.say("c2.rule.4") as c:
            c.wait_until("something new")
            sweep_clear(self, keep=keep, run_time=1.2)
            c.wait_until("the tangent of the sum")
            f = tan_formula().move_to(UP * 1.0)
            self.play(*appear(f), run_time=1.0)
            c.wait_until("top")
            num, bar, den = f[1]
            hb = SurroundingRectangle(num, color=YELLOW, buff=0.15).set_stroke(YELLOW, 2) \
                .set_fill(YELLOW, 0.15).set_z_index(-1)
            self.play(FadeIn(hb), run_time=0.9)
            c.wait_until("bottom")
            hb2 = SurroundingRectangle(den, color=YELLOW, buff=0.15).set_stroke(YELLOW, 2) \
                .set_fill(YELLOW, 0.15).set_z_index(-1)
            self.play(Transform(hb, hb2), run_time=1.2)
            c.wait_until("hide")
            g = tan_formula(h=True).move_to(f)
            self.play(FadeOut(hb), *edit(f[0], g[0]), *edit(num, g[1][0]), *edit(den, g[1][2]),
                      ReplacementTransform(bar, g[1][1]), *flash([self.s1]), run_time=1.3)
            settle(self, g)
            gden = g[1][2]
            unf = frac_of(mtex(r"\sinh A\, \sinh B", size=44, color=TEAL),
                          mtex(r"\cosh A\, \cosh B", size=44, color=TEAL), TEAL)
            br = Brace(gden[2], DOWN, buff=0.15, color=DIM)
            unf.next_to(br, DOWN, buff=0.25)
            ubox = outline(unf[0], buff=0.1)
            self.play(GrowFromCenter(br), *during(appear(unf), 0.3, 0.9), *during([FadeIn(ubox)], 0.7, 1.0),
                      run_time=min(1.6, c.until("flipdown")))
            uu = VGroup(br, unf, ubox)
            settle(self, uu)
            c.wait_until("flipdown")
            pred = prediction_shot()
            h = tan_formula(h=True, plus=True).move_to(g)
            self.play(*edit(gden, h[1][2]), *flash([self.s2]), run_time=1.3)
            self.play(FlashAround(h[1][2][1], color=YELLOW, run_time=1.2, time_width=1.5))
            g[1].remove(gden)
            g[1].add(h[1][2])
            settle(self, g)
            c.wait_until("guess")
            self.play(*during(disappear(uu), 0, 0.45),
                      *during([g.animate.move_to(pred[0])], 0.3, 0.75),
                      *during(appear(pred[1]), 0.7, 1.0), run_time=2.2)
            c.wait_until("same top")
            self.play(FlashAround(g[1][0], color=TEAL, run_time=1.2, time_width=1.5))
            c.wait_until("plus underneath")
            self.play(FlashAround(g[1][2][1], color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("aid")
            cap = T("memory aid, not a proof", 36, DIM).move_to(DOWN * 2.3)
            self.play(*appear(cap), run_time=1.0)
