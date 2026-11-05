"""Chapter 3, scene 6: recap of M7, M8, M9, the facts, next time. Clips c3.recap.1 – c3.recap.2.

Reused drawings (never redrawn): s2's plane3 (scaled about each panel's origin) and its GOLD arrow
look (ak.arrow_between), s3's GOLD brace |A| and YELLOW arg A arc (local copies of s3's in-scene
builders, scaled: s3 exports none), s4's tip_to_tail, s5's fan3, ch1 s8's recap_card, ch4 s2's
spring_at / push_arrow for the {next} picture.
Motion: every model-time tracker either runs on a frame-exact clock (reads self.time) or is moved
inside play() (exact landings).
Reversed join: the last frame is exactly load_scene("ch4_s1_hook").opening_card() (chapter 4's
first frame), reached by a morph during the end hold (table → ceiling, coil → hanging coil,
block → weight). No handover mark: this scene ends the chapter.
"""
# style: 2
import cmath
import math
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

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
r8 = load_scene("ch1_s8_recap")
s2 = load_scene("ch3_s2_freeze")
s4 = load_scene("ch3_s4_add")
s5 = load_scene("ch3_s5_velocity")
c4s2 = load_scene("ch4_s2_start")
ch4 = load_scene("ch4_s1_hook")

CM, A3, PHI3, OMEGA3, CLOCK, P3 = s2.CM, s2.A3, s2.PHI3, s2.OMEGA3, s2.CLOCK, s2.PERIOD3
HEAD_Y = 3.36
REC_TOP = 3.0
PIC_BOTTOM = -1.85
LINE_TOP = -2.0
LINE_SIZE = 24
FACTS_Y = -3.4

# {next}
O_N = np.array([-2.6, 0.0, 0.0])
U_N = c4s2.U
LINE_X = 0.55


def _vec(z):
    return np.array([z.real, z.imag, 0.0])


def plane_small(o, k, rot=0.0):
    """s2's plane (grid, axes, circle of radius 5) at origin o, scaled by k."""
    return s2.plane3(rot, 1.0, origin=o).scale(k, about_point=o)


def gold7(o, k, tv, rv, op=1.0):
    z = A3 * cmath.exp(1j * (OMEGA3 * tv + rv))
    a = ak.arrow_between(o, o + k * CM * _vec(z), GOLD, 5, s2.Z_GOLD)
    return s2._fade(a, op)


def brace7(o, k):
    """s3's GOLD brace |A| along the frozen arrow (its look, panel size)."""
    tip = o + k * CM * _vec(A3)
    u = (tip - o) / np.linalg.norm(tip - o)
    n = np.array([u[1], -u[0], 0.0])
    b = BraceBetweenPoints(o, tip, direction=n, buff=0.18, color=GOLD)
    lab = set_backstroke(MathTex("|A|", font_size=28, color=GOLD))
    lab.move_to(b.get_tip() + n * 0.3)
    return b, lab


def arc7(o):
    arc = Arc(radius=0.55, start_angle=0, angle=PHI3, arc_center=o).set_stroke(YELLOW, 4)
    arc.set_z_index(s2.Z_MARK)
    lab = set_backstroke(MathTex(r"\arg A", font_size=28, color=YELLOW))
    lab.move_to(o + np.array([0.95, -0.33, 0]))
    return arc, lab


def rows(*items, x=0.0, top=LINE_TOP):
    g = VGroup(*items).arrange(DOWN, buff=0.12)
    g.move_to([x, top, 0], aligned_edge=UP)
    return g


def line_text(text, t2c=None):
    return T(text, size=LINE_SIZE, color=FG, t2c=t2c or {})


def facts_row():
    m = MathTex(r"\text{remember: }", "A", "=", "a", "-", "ib", r"\ \cdot\ ", "|A|",
                r"=\text{amplitude}", r"\ \cdot\ ", r"\arg A", r"=\text{phase}", font_size=28)
    m.set_color(DIM).move_to([0, FACTS_Y, 0])
    return m


def f19_card():
    t = T("F19 · Examples Sheet I", size=26, color=DIM)
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.34)
    box.set_stroke(DIM, 2).set_fill(kit.CARD_FILL, 1).move_to(t)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


class Recap(NarratedScene):
    def construct(self):
        self.t7, self.r7 = self.clock(), self.clock()
        self.t8, self.t9 = self.clock(), self.clock()
        self.op7 = ValueTracker(0.0)
        self.add(self.op7)
        self.clip1()
        self.clip2()
        self.end_hold()

    # ── frame-exact clocks ─────────────────────────────────────────────────────
    def clock(self, v=0.0):
        tr = ValueTracker(v)
        tr.clk_fn = None
        tr.add_updater(lambda m: m.set_value(m.clk_fn(self.time)) if m.clk_fn else None)
        self.add(tr)
        return tr

    def run(self, tr, rate=CLOCK):
        v0, t0 = tr.get_value(), self.time
        tr.clk_fn = lambda tau: v0 + rate * (tau - t0)

    def stop(self, tr):
        tr.clk_fn = None

    # ── {recap}: three moves, each picture moving ──────────────────────────────
    def clip1(self):
        head = T("Recap", size=28, color=DIM).move_to([0, HEAD_Y, 0])
        cards = [r8.recap_card(s2.MOVE_M7), r8.recap_card(s4.MOVE_M8), r8.recap_card(s5.MOVE_M9)]
        row = VGroup(*cards).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        if row.width > 13.2:
            row.scale_to_fit_width(13.2)
        row.move_to([0, REC_TOP, 0], aligned_edge=UP)
        xs = [cd.get_center()[0] for cd in cards]
        pic_top = min(cd.get_bottom()[1] for cd in cards) - 0.2
        cy = (pic_top + PIC_BOTTOM) / 2
        k = min(0.7, (pic_top - PIC_BOTTOM) / 2 / s2.RA)
        self.k = k
        o7, o8, o9 = (np.array([x, cy, 0.0]) for x in xs)
        o8 = o8 + 0.25 * LEFT                  # the L reaches right of its origin
        self.o = (o7, o8, o9)

        # M7: s2's arrow, then the counter-rotating plane; s3's brace and arc
        t7, r7, op7 = self.t7, self.r7, self.op7
        plane7 = always_redraw(lambda: plane_small(o7, k, r7.get_value()))
        arrow7 = always_redraw(lambda: gold7(o7, k, t7.get_value(), r7.get_value(), op7.get_value()))
        a_lab = MathTex("A", font_size=34, color=GOLD).next_to(o7 + k * CM * _vec(A3), RIGHT, buff=0.12)
        br, br_lab = brace7(o7, k)
        arc, arc_lab = arc7(o7)
        l7 = [line_text("ride along: A holds still", {"A": GOLD}),
              line_text("length = amplitude", {"length": GOLD, "amplitude": GOLD}),
              line_text("angle = phase", {"angle": YELLOW, "phase": YELLOW})]
        rows(*l7, x=xs[0])

        # M8: s4's tip-to-tail L
        u8 = k * CM
        t8 = self.t8
        plane8 = plane_small(o8, k)
        ttt8 = s4.tip_to_tail(t8, origin=o8, unit=u8, width=5)
        l8 = MathTex("A", "=", "a", "-", "i", "b", font_size=34)
        for i, col in ((0, GOLD), (2, BLUE), (3, PINK), (4, PINK), (5, PINK)):
            l8[i].set_color(col)
        rows(l8, x=xs[1], top=LINE_TOP - 0.05)

        # M9: s5's fan
        t9 = self.t9
        plane9 = plane_small(o9, k)
        fan9 = s5.fan3(t9, origin=o9, scale=k, labels=False)
        l9 = [MathTex(r"d/dt:\ \times\, i\omega", font_size=30),
              line_text("a quarter turn ahead")]
        l9[0][0][5:].set_color(GREEN)
        rows(*l9, x=xs[2])

        facts = facts_row()

        with self.say("c3.recap.1") as c:
            self.play(*appear(head, shift=None), run_time=1.0)

            c.wait_until("m7")
            self.add(arrow7)
            rt = max(2.4, min(3.6, c.until("holds still")))
            self.play(*during(appear(cards[0], plane7, shift=None, lag=0.2), 0, 0.4),  # early: the move card names the move as it is said
                      *during([op7.animate.set_value(1.0)], 0, 0.3),
                      t7.animate.set_value(P3), rate_func=linear, run_time=rt)
            # ride along: the plane turns back as fast as the arrow turns on
            c.wait_until("holds still")
            self.play(t7.animate.set_value(2 * P3), r7.animate.set_value(-TAU),
                      rate_func=linear, run_time=P3 / CLOCK)
            t7.set_value(0.0)
            r7.set_value(0.0)
            c.wait_until("complex amplitude")
            self.play(*appear(a_lab, l7[0], lag=0.3), run_time=1.2)

            c.wait_until("length")
            self.play(GrowFromCenter(br), *during(appear(br_lab, l7[1], lag=0.3), 0.3, 1.0), run_time=1.4)
            c.wait_until("angle")
            self.play(Create(arc), *during(appear(arc_lab, l7[2], lag=0.3), 0.3, 1.0), run_time=1.4)

            # M8
            c.wait_until("m8")
            self.play(*appear(cards[1], plane8, ttt8, shift=None, lag=0.2), run_time=1.2)  # early: the move card names the move as it is said
            self.play(t8.animate.set_value(P3), rate_func=linear,
                      run_time=max(2.0, min(4.0, c.until("lies flat") - 0.1)))
            c.wait_until("lies flat")
            st = s4.tip_to_tail(P3, origin=o8, unit=u8, width=5)
            self.play(FlashAround(st.blue, color=BLUE, time_width=1.5, buff=0.1), run_time=1.3)
            c.wait_until("points down")
            self.play(FlashAround(st.pink, color=PINK, time_width=1.5, buff=0.1), run_time=1.3)
            c.wait_until("together")
            self.play(FlashAround(st.gold, color=GOLD, time_width=1.5, buff=0.1),
                      *during(appear(l8, shift=None), 0.35, 1.0), run_time=1.5)

            # {facts}: the minus sign, read off the picture
            c.wait_until("facts")
            self.play(FlashAround(st.pink, color=PINK, time_width=1.5, buff=0.1),
                      FlashAround(l8[3], color=PINK, time_width=1.5), run_time=1.5)
            c.wait_until("picture puts")
            self.play(t8.animate.set_value(1.25 * P3), run_time=1.4)
            st2 = s4.tip_to_tail(1.25 * P3, origin=o8, unit=u8, width=5)
            self.play(FlashAround(st2.pink, color=PINK, time_width=1.5, buff=0.1), run_time=1.3)

            # M9
            c.wait_until("m9")
            self.play(*appear(cards[2], plane9, fan9, shift=None, lag=0.2), run_time=1.2)  # early: the move card names the move as it is said
            self.run(t8)
            self.run(t9)
            c.wait_until("eye omega")
            self.play(*appear(l9[0], shift=None), run_time=1.0)
            c.wait_until("quarter turn")
            self.play(*appear(l9[1], shift=None), run_time=1.0)
            c.wait_until("take the shadow")
            self.play(*appear(facts, shift=None), run_time=1.2)
        self.panel = [head, *cards, plane7, arrow7, a_lab, br, br_lab, arc, arc_lab, *l7,
                      plane8, ttt8, l8, plane9, fan9, *l9]
        self.facts = facts

    # ── {next}: from the start to A; F19 ───────────────────────────────────────
    def clip2(self):
        sp = c4s2.spring_at(3.0, O_N, U_N)
        tick = sp.tick
        zero = T("0", size=24, color=DIM).next_to(tick, DOWN, buff=0.1)
        push = c4s2.push_arrow(3.0, 12.0, O_N, U_N)
        blk = sp.block
        x_lab = MathTex(r"x(0) = 3\ \text{cm}", font_size=30, color=BLUE)
        x_lab.next_to(blk, DOWN, buff=0.32).shift(0.35 * RIGHT)
        v_lab = MathTex(r"\dot{x}(0) = 12\ \text{cm/s}", font_size=30, color=GREEN)
        v_lab.next_to(push, UP, buff=0.15).align_to(push, LEFT)
        q = MathTex(r"x(0),", r"\ \dot{x}(0)", r"\ \longrightarrow\ ", "A", r"\ ?", font_size=50)
        for i, col in ((0, BLUE), (1, GREEN), (3, GOLD), (4, YELLOW)):
            q[i].set_color(col)
        q.move_to([LINE_X, 0.5, 0], aligned_edge=LEFT)
        card = f19_card().move_to([LINE_X, -0.95, 0], aligned_edge=LEFT)
        self.nxt = T("Next: putting it to work", size=30, color=DIM).move_to([LINE_X, -2.25, 0], aligned_edge=LEFT)

        with self.say("c3.recap.2") as c:
            for tr in (self.t7, self.r7, self.t8, self.t9):
                self.stop(tr)
            for m in self.panel:
                for sm in m.get_family():
                    sm.clear_updaters()
            shrink = [m.animate.scale(0.05).set_opacity(0) for m in self.panel]
            self.play(*during(shrink, 0, 0.5),
                      *during(appear(sp, zero, shift=None, lag=0.1), 0.5, 1.0), run_time=2.0)
            self.remove(*[sm for m in self.panel for sm in m.get_family()])
            self.play(GrowArrow(push), *during(appear(x_lab, v_lab, shift=None, lag=0.3), 0.2, 1.0),
                      run_time=1.4)
            c.wait_until("complex amplitude")
            self.play(*appear(q, shift=None), run_time=1.2)
            c.wait_until("sheet")
            self.play(FadeIn(card, shift=0.6 * LEFT), run_time=1.2)  # early: the brief's {sheet} card, named in this sentence
        self.next_parts = dict(sp=sp, tick=tick, zero=zero, push=push, x_lab=x_lab, v_lab=v_lab,
                               q=q, card=card)

    # ── end card, then the morph into chapter 4's first frame ──────────────────
    def end_hold(self):
        P = self.next_parts
        self.play(*appear(self.nxt, shift=None), run_time=1.0)  # early: the end card's next-chapter line, after the last word
        self.wait(5.8)
        sp = P["sp"]
        card = ch4.opening_card()
        texts = [P["x_lab"], P["v_lab"], P["q"], P["card"], self.nxt, self.facts, P["zero"]]
        self.play(*during(disappear(*texts), 0, 0.4),
                  *during([FadeOut(P["push"]), FadeOut(sp.wall), FadeOut(sp.tick)], 0, 0.4),
                  *during([ReplacementTransform(sp.table, card.ceiling),
                           ReplacementTransform(sp.hatch, card.hatch),
                           ReplacementTransform(sp.coil, card.coil),
                           ReplacementTransform(sp.block, card.weight)], 0.35, 1.0),
                  run_time=2.6)
        keep = (self.t7, self.r7, self.t8, self.t9, self.op7)
        self.remove(*[m for m in list(self.mobjects) if m not in keep])
        self.add(ch4.opening_card())
        self.wait(1.2)
