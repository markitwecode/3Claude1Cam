"""Chapter 2, scene 4: implied pairs: the test turned around, the decision fork, promises that can break.
Clips c2.pairs.1 - c2.pairs.4.

Opens on an empty frame (s3 ends empty); ends on an empty frame (s5 is a topic change).

Shared drawing (import with load_scene("ch2_s4_implied")), at this scene's home positions:
- `decision_fork()`: "compare p and q, same input x" at the top, two arms down; left: "outputs differ",
  a RED-crossed square, "p ≢ q", "settled"; right: "outputs same" (GREEN), "p ≡ q if p′ ≡ q′".
  `.top .arms [2] .lab_l .box .cross .neq .settled .lab_r .cond`.
- `promise_card(text, size=36, width=None)`: a dashed rounded card round the text (p/q YELLOW, ≡ GOLD),
  centred on ORIGIN. `.frame .text`.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch2_s3_onestep")
S5 = load_scene("ch2_s5_layout")
S6 = load_scene("ch2_s6_outputs")
M1 = load_scene("ch1_s3_mealy")


def _p(x, y):
    return np.array([x, y, 0.0])


RULES = [(r"(?<!\w)[pq][′″]?(?!\w)", YELLOW), (r"(?<!\w)x(?!\w)", BLUE), (r"≡", GOLD)]


def rich(s, size=36):
    return S3._rich(s, size, RULES)


# ------------------------------------------------------------------ shared drawings
def promise_card(text, size=36, width=None):
    t = rich(text, size)
    w = width or (t.width + 0.8)
    frame = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=w, height=t.height + 0.6),
                           num_dashes=44, dashed_ratio=0.6).set_stroke(FG, 2.5)
    frame.move_to(t)
    g = VGroup(frame, t)
    g.frame, g.text = frame, t
    return g


def decision_fork():
    top = rich("compare p and q, same input x", 40).move_to(_p(0, 1.35))
    arms = [Arrow(_p(-0.9, 1.0), _p(-3.2, 0.25), buff=0, stroke_width=4, color=DIM, tip_length=0.22),
            Arrow(_p(0.9, 1.0), _p(3.2, 0.25), buff=0, stroke_width=4, color=DIM, tip_length=0.22)]
    lab_l = T("outputs differ", 36).move_to(_p(-3.4, -0.1))
    box = Square(0.7).set_stroke(DIM, 3).move_to(_p(-3.4, -1.0))
    cross = S6.cell_cross(box)
    neq = MathTex("p", r"\not\equiv", "q", font_size=48)
    neq[0].set_color(YELLOW), neq[1].set_color(RED), neq[2].set_color(YELLOW)
    neq.move_to(_p(-3.85, -1.85))
    settled = T("settled", 30, DIM, slant=ITALIC).next_to(neq, RIGHT, buff=0.4)
    lab_r = T("outputs same", 36, GREEN).move_to(_p(3.4, -0.1))
    cond = rich("p ≡ q if p′ ≡ q′", 44).move_to(_p(3.4, -1.0))
    g = VGroup(top, *arms, lab_l, box, cross, neq, settled, lab_r, cond)
    g.top, g.arms, g.lab_l, g.box, g.cross = top, arms, lab_l, box, cross
    g.neq, g.settled, g.lab_r, g.cond = neq, settled, lab_r, cond
    return g


def crack(card):
    f = card.frame
    x, t, b = f.get_right()[0] - 0.45, f.get_top()[1], f.get_bottom()[1]
    h = t - b
    pts = [_p(x + 0.1, t + 0.12), _p(x - 0.16, t - 0.22 * h), _p(x + 0.18, t - 0.42 * h),
           _p(x - 0.14, t - 0.62 * h), _p(x + 0.16, t - 0.82 * h), _p(x - 0.04, b - 0.12)]
    return VMobject().set_points_as_corners(pts).set_stroke(RED, 4)


CARD_W = 6.0
QUOTE2 = ["Just because a particular pairwise comparison implies that",
          "some pairs of next states are equivalent, it does not mean",
          "they definitely are."]


class Implied(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------------- c2.pairs.1
    def clip1(self):
        with self.say("c2.pairs.1") as c:
            title = T("State Equivalence", 44).move_to(_p(0, 3.35))
            d = S3.pq_diagram(marks=True)
            d.scale(1.2).move_to(_p(0, -0.35))
            d.remove(d.eq_pq, d.eq_next)
            self.title, self.d = title, d
            self.play(*appear(title), FadeIn(d), run_time=1.2)  # early: the slide's title, shown whole
            c.wait_until("If two states")
            self.play(FadeIn(d.eq_pq, scale=1.3), FlashAround(d.eq_pq, color=GOLD, run_time=1.4, time_width=1.5),
                      run_time=1.4)
            c.wait_until("outputs must match")
            self.play(*[FlashAround(lab.out, color=GREEN, time_width=1.5) for lab in d.labels], run_time=1.4)
            c.wait_until("next states must")
            self.play(FadeIn(d.eq_next, scale=1.3), FlashAround(d.eq_next, color=GOLD, time_width=1.5),
                      run_time=1.4)
            settle(self, d, add=[d.eq_pq, d.eq_next])

            c.wait_until("method")
            bullet = VGroup(T("What we need is a method to identify equivalent", 30),
                            T("and not just identical next states.", 30)).arrange(DOWN, buff=0.16)
            bullet.move_to(_p(0.5, 2.4))
            self.bullet = bullet
            self.play(*during([d.animate.scale(0.78).move_to(_p(0, -0.85))], 0, 0.55),  # early: the slide's bullet, read whole
                      *during(appear(bullet, shift=None), 0.45, 1), run_time=1.6)

            fork = decision_fork()
            self.fork = fork
            c.wait_until("Compare the states")
            self.play(*during(disappear(d), 0, 0.5), *during(appear(fork.top), 0.45, 1), run_time=1.6)
            c.wait_until("same input")
            self.play(*[GrowArrow(a) for a in fork.arms], run_time=1.2)

            c.wait_until("differ")
            self.play(*appear(fork.lab_l), *set_alpha([bullet], 0.4), run_time=1.0)
            c.wait_until("tell them apart")
            self.play(FadeIn(fork.box), *[Create(l) for l in fork.cross], run_time=1.0)
            c.wait_until("not equivalent")
            self.play(*appear(fork.neq), run_time=1.0)
            c.wait_until("settled")
            quote = VGroup(T("Note that if the outputs are different,", 28), T("then the checked states", 28),
                           T("cannot be equivalent.", 28)).arrange(DOWN, buff=0.12)
            quote.move_to(_p(-3.2, -2.95))
            self.quote1 = quote
            self.play(*appear(fork.settled), run_time=0.8)
            self.play(*appear(quote, shift=None), run_time=1.0)  # early: the slide's note, shown whole

    # -------------------------------------------------------------- c2.pairs.2
    def clip2(self):
        fork = self.fork
        with self.say("c2.pairs.2") as c:
            self.play(*appear(fork.lab_r), run_time=1.0)
            c.wait_until("equivalent only if")
            self.play(*appear(fork.cond), run_time=1.2)

            c.wait_until("implied")
            src = VGroup(*fork.cond.submobjects[-7:])   # "p′ ≡ q′"
            pair = T("p′-q′", 40).move_to(_p(src.get_x(), -2.3))
            lab = T("implied pair", 30, YELLOW).move_to(_p(pair.get_x(), -3.2))
            self.lab = lab
            self.play(FlashAround(src, color=YELLOW, time_width=1.5, run_time=1.2),
                      *during(appear(pair, shift=0.6 * DOWN), 0.3, 1), run_time=1.5)
            c.wait_until(own_word=lab)
            self.play(*appear(lab), run_time=1.0)

            # the condition line itself becomes the promise card; the pair and its label stay under it
            c.wait_until("promise")
            frame = promise_card("p ≡ q if p′ ≡ q′", 44).frame.move_to(fork.cond)
            card = VGroup(frame, fork.cond)
            card.frame, card.text = frame, fork.cond
            self.card = card
            self.play(Create(frame), run_time=1.4)
            settle(self, card)
            c.wait_until("State pee")
            self.play(FlashAround(card, color=YELLOW, time_width=1.5), run_time=1.6)

    # -------------------------------------------------------------- c2.pairs.3
    def clip3(self):
        card = self.card
        with self.say("c2.pairs.3") as c:
            quote = VGroup(*[T(s, 30) for s in QUOTE2]).arrange(DOWN, buff=0.16)
            quote.move_to(_p(0, 2.25))
            wide = promise_card("p ≡ q if p′ ≡ q′", 38, width=CARD_W).move_to(_p(0, 0.75))
            sweep_clear(self, card.text.animate.scale(38 / 44).move_to(wide.text), Transform(card.frame, wide.frame),  # early: the slide's line, read whole
                        time_span(FadeIn(quote), 0.9, 1.6), keep=[card], run_time=1.6)

            c.wait_until("broken")
            card2 = promise_card("p′ ≡ q′ if p″ ≡ q″", 38, width=CARD_W).move_to(_p(0, -1.0))
            card3 = promise_card("p″, q″: outputs differ", 38, width=CARD_W).move_to(_p(0, -2.75))
            a1 = Arrow(card.get_bottom(), card2.get_top(), buff=0.08, stroke_width=4, color=FG, tip_length=0.2)
            a2 = Arrow(card2.get_bottom(), card3.get_top(), buff=0.08, stroke_width=4, color=FG, tip_length=0.2)
            self.play(GrowArrow(a1), *during([Create(card2.frame)], 0.3, 1),
                      *during(appear(card2.text, shift=None), 0.4, 1), run_time=1.4)
            c.wait_until("may show")
            self.play(GrowArrow(a2), *during([Create(card3.frame)], 0.3, 1),  # early: the failing pair
                      *during(appear(card3.text, shift=None), 0.4, 1), run_time=1.4)
            c.wait_until("after all")
            sq = Square(0.62).set_stroke(DIM, 3).next_to(card3, RIGHT, buff=0.35)
            x3 = S6.cell_cross(sq)
            self.play(FadeIn(sq), *[Create(l) for l in x3], card3.frame.animate.set_stroke(RED), run_time=1.0)

            c.wait_until("every promise")
            back2 = Line(a2.get_end(), a2.get_start()).set_stroke(RED, 7)
            back1 = Line(a1.get_end(), a1.get_start()).set_stroke(RED, 7)
            k2, k1 = crack(card2), crack(card)
            self.play(time_span(VShowPassingFlash(back2, time_width=0.8), 0, 0.6),
                      time_span(a2.animate.set_color(RED), 0, 0.6),
                      time_span(card2.frame.animate.set_stroke(RED), 0.5, 1.0),
                      time_span(Create(k2), 0.5, 1.0),
                      time_span(card2.text.animate.set_opacity(0.45), 0.5, 1.0),
                      time_span(VShowPassingFlash(back1, time_width=0.8), 1.0, 1.6),
                      time_span(a1.animate.set_color(RED), 1.0, 1.6),
                      time_span(card.frame.animate.set_stroke(RED), 1.5, 2.0),
                      time_span(Create(k1), 1.5, 2.0),
                      time_span(card.text.animate.set_opacity(0.45), 1.5, 2.0),
                      run_time=2.0)

    # -------------------------------------------------------------- c2.pairs.4
    def clip4(self):
        with self.say("c2.pairs.4") as c:
            lt = S5.p150_table(size=30, pitch=0.6, top=0.1, x0=-5.6)
            row = lt.rows[0]
            bot = 0.1 - 0.3
            seps = VGroup(*[Line(_p(s.get_x(), s.get_top()[1]), _p(s.get_x(), bot)).set_stroke(DIM, 2)
                            for s in lt.seps])
            left = VGroup(lt.head, lt.rules, seps, row)
            sweep_clear(self, *appear(left, shift=None), keep=[self.title], run_time=1.4)  # early: p. 150's header, shown whole

            c.wait_until("one output")
            mbox = (Rectangle(width=lt.h_out.width + 0.36, height=lt.h_out.get_top()[1] + 0.12 - bot)
                    .move_to(_p(lt.h_out.get_x(), (lt.h_out.get_top()[1] + 0.12 + bot) / 2))
                    .set_stroke(GREEN, 2).set_fill(GREEN, 0.15).set_z_index(-1))
            mlab = VGroup(T("one output per state,", 30), T("like a Moore machine", 30)).arrange(DOWN, buff=0.14)
            mlab.move_to(_p(left.get_x(), -1.5))
            self.play(FadeIn(mbox), *appear(mlab), run_time=1.2)
            c.wait_until("compare the two")
            self.play(FlashAround(mbox, color=GREEN, time_width=1.5), run_time=1.4)

            c.wait_until("mealy")
            mt = M1.state_table(rows=[M1.MACHINE[0]], size=30, pitch=0.6, top=0.1, x0=0.85, rules_after=())
            self.play(*appear(mt, shift=None), run_time=1.0)  # early: ch1's header, shown whole
            elab = VGroup(T("Mealy: compare the output", 30), T("for each input value", 30)).arrange(DOWN, buff=0.14)
            elab.move_to(_p(mt.get_x(), -1.5))
            self.play(*appear(elab), run_time=1.0)
            c.wait_until("output depends")
            box = mt.col_box([3], GREEN)
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("column by column")
            self.play(Transform(box, mt.col_box([4], GREEN)), run_time=1.0)
