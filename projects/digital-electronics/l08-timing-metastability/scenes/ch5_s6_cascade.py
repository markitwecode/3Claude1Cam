"""Chapter 5, scene 6: more flip-flops: the K + 1 cascade and its MTBF. Clips c5.cascade.1 – c5.cascade.4.

Shots: s5's answer box `T_c >= 3.04 ns` (upper left, kept all scene) + RED "too long?" -> ch4 s5's
synchroniser (button, D0 BLUE, FF0, D1 TEAL, FF1, Q GREEN, YELLOW CLK) slides left; FF2 slides in,
a faded FF3 with "...", Q moves to the end, CLK stretches; braces "input flip-flop" / "K additional
flip-flops" -> GOLD P_fail tags over FF1..FF3 merge into P_fail_K = (P_fail)^K; trim to K = 1 and
grow back; per-second and MTBF lines -> board clears to the three lines at the top, YELLOW
"P_fail << 1", RED (0.5)^k example left, GREEN (10^-7)^2 right -> panel "by the slide's formula
(ours)": K = 2, 7 million years at 3.04 ns, 1.6 ns for one year (DIM 3.03 ns for K = 1).
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
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# answer_box(): s5's result, small at the upper left (s5 matches this style)
# =============================================================================================
def answer_box():
    tex = MathTex(r"T_c \geq 3.04\text{ ns}", font_size=40, color=FG)
    box = SurroundingRectangle(tex, color=GOLD, buff=0.18, corner_radius=0.08).set_stroke(GOLD, 3)
    g = VGroup(box, tex)
    g.box, g.tex = box, tex
    g.to_corner(UL, buff=0.5)
    return g
# =============================================================================================


# =============================================================================================
# push_button() + make_ff(): copied from ch4_s5_synchroniser.py (from ch4_s1_hook.py)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
PUSH = 0.18


def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.d_w, g.q_w, g.clk_w = d_l, q_l, d_w, q_w, clk_w
    g.shift(center)
    clk_w.shift(center)
    return g


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)
    g.stem, g.cap, g.body = stem, cap, body
    g.shift(center)
    g.out = lambda: body.get_right()
    return g
# =============================================================================================


# =============================================================================================
# sync_circuit(): copied from ch4_s5_synchroniser.py (the two-flip-flop synchroniser, p. 112)
# =============================================================================================
SK = 0.62                    # flip-flop scale
SFF_X = (-1.7, 2.1)          # FF0, FF1 centres
SFF_Y = 2.244                # box centre (top 3.05)
SBTN_X = -4.3                # button housing centre
SHX = (BOX_W / 2 + WIRE) * SK


def sync_circuit():
    C = VGroup()
    ffs = []
    for x in SFF_X:
        f = make_ff()
        f.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        f.clk_w.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.45, about_point=lb.get_center())
        ffs.append(f)
    C.ff0, C.ff1 = ffs
    py = SFF_Y + PIN_Y * SK
    C.py = py
    C.ff0.q_w.set_stroke(TEAL)
    C.ff0.q_l.set_color(TEAL)
    C.ff1.d_w.set_stroke(TEAL)
    C.ff1.d_l.set_color(TEAL)
    C.names = [T(f"FF{i}", 30, FG).move_to(f.box.get_center() + 0.3 * DOWN) for i, f in enumerate(ffs)]
    C.btn = push_button(_p(SBTN_X, py))
    C.d0_w = Line(C.btn.out(), C.ff0.d_w.get_start()).set_stroke(BLUE, 5)
    C.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(
        (C.btn.out() + C.ff0.d_w.get_start()) / 2, UP, buff=0.14)
    C.link = Line(C.ff0.q_w.get_end(), C.ff1.d_w.get_start()).set_stroke(TEAL, 5)
    C.d1_l = MathTex("D_1", font_size=40, color=TEAL).next_to(C.link, UP, buff=0.12)
    C.q_l = MathTex("Q", font_size=40, color=GREEN).next_to(C.ff1.q_w.get_end(), RIGHT, buff=0.15)
    by = SFF_Y - (BOX_H / 2 + EN_WIRE) * SK
    C.by = by
    C.bus = Line(_p(-3.2, by), _p(SFF_X[1], by)).set_stroke(YELLOW, 5)
    C.jdot = Dot(_p(SFF_X[0], by), radius=0.08, color=YELLOW)
    C.clk_ws = [f.clk_w for f in ffs]
    C.clk_l = T("CLK", 30, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.15)
    C.all = [C.ff0, C.ff1, *C.names, C.btn, C.d0_w, C.d0_l, C.link, C.d1_l, C.q_l,
             C.bus, C.jdot, *C.clk_ws, C.clk_l]
    C.add(*C.all)
    return C
# =============================================================================================


# =============================================================================================
# cascade_chain(): the K + 1 synchroniser (slide p. 115) in sync_circuit()'s styling: button,
# D0 BLUE, FF0 .. FF{n-1} (intermediate wires TEAL), Q GREEN, one YELLOW CLK bus. Nothing is
# added to the scene: pick the parts. Positions are the full chain's; the last FF (if fade_last)
# is drawn faded with a "..." after it. bus_to(k) / q_at(k) give the bus and Q label for a chain
# of the first k flip-flops. The recap copies this block.
# =============================================================================================
CK_X0, CK_PITCH, CK_Y = -3.6, 2.6, 1.2
CK_FADE = 0.4


def cascade_chain(n=4, x0=CK_X0, pitch=CK_PITCH, y=CK_Y, fade_last=True):
    C = VGroup()
    xs = [x0 + i * pitch for i in range(n)]
    C.xs = xs
    C.ffs = []
    for x in xs:
        f = make_ff()
        f.scale(SK, about_point=ORIGIN).shift(_p(x, y))
        f.clk_w.scale(SK, about_point=ORIGIN).shift(_p(x, y))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.45, about_point=lb.get_center())
        C.ffs.append(f)
    py = y + PIN_Y * SK
    C.py = py
    for f in C.ffs[1:]:                         # every input after FF0 is an intermediate signal
        f.d_w.set_stroke(TEAL)
        f.d_l.set_color(TEAL)
    C.ffs[0].q_w.set_stroke(TEAL)
    C.ffs[0].q_l.set_color(TEAL)
    C.names = [T(f"FF{i}", 30, FG).move_to(f.box.get_center() + 0.3 * DOWN) for i, f in enumerate(C.ffs)]
    C.btn = push_button(_p(x0 - 2.0, py))
    C.d0_w = Line(C.btn.out(), C.ffs[0].d_w.get_start()).set_stroke(BLUE, 5)
    C.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(
        (C.btn.out() + C.ffs[0].d_w.get_start()) / 2, UP, buff=0.14)
    C.links = [Line(C.ffs[i].q_w.get_end(), C.ffs[i + 1].d_w.get_start()).set_stroke(TEAL, 5)
               for i in range(n - 1)]
    C.d1_l = MathTex("D_1", font_size=40, color=TEAL).next_to(C.links[0], UP, buff=0.12)
    by = y - (BOX_H / 2 + EN_WIRE) * SK
    C.by = by
    C.bx0 = x0 - 1.3
    C.jdots = [Dot(_p(x, by), radius=0.08, color=YELLOW) for x in xs[:-1]]
    C.clk_ws = [f.clk_w for f in C.ffs]
    C.clk_l = T("CLK", 30, YELLOW).next_to(_p(C.bx0, by), LEFT, buff=0.15)
    end = C.ffs[-1].q_w.get_end()
    C.dots = MathTex(r"\cdots", font_size=44, color=FG).next_to(end, RIGHT, buff=0.15)
    if fade_last:
        last = [C.ffs[-1], C.names[-1], C.clk_ws[-1], C.links[-1], C.dots]
        for m in last:
            fade_ghost(m)

    def bus_to(k):
        return Line(_p(C.bx0, by), _p(xs[k - 1], by)).set_stroke(YELLOW, 5)

    def q_at(k):
        anchor = C.dots if (fade_last and k == n) else C.ffs[k - 1].q_w
        return MathTex("Q", font_size=40, color=GREEN).next_to(anchor.get_right(), RIGHT, buff=0.15)

    C.bus_to, C.q_at = bus_to, q_at
    C.bus = bus_to(2)
    C.q_l = q_at(2)
    return C


def fade_ghost(m, op=CK_FADE):
    """Fade outlines and glyphs to op; unfilled shapes stay unfilled, the clock triangle stays opaque."""
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=op)
        if sm.get_fill_opacity() > 0 and not (isinstance(sm, Polygon) and len(sm.get_vertices()) == 3):
            sm.set_fill(opacity=op)
    return m


def stage(C, i):
    """The pieces that add flip-flop i (i >= 2) to the chain: link in, FF, name, clock stub."""
    return [C.links[i - 1], C.ffs[i], C.names[i], C.clk_ws[i]]
# =============================================================================================


def q_wire(C):
    """One GREEN wire from FF1's Q stub to the Q label (no updater: slide_q moves both)."""
    w = Line(C.ffs[1].q_w.get_end(), C.q_l.get_left() + 0.05 * LEFT).set_stroke(GREEN, 5)
    return w


def slide_q(C, w, target):
    """Q slides to target; in the same frame the wire's right end follows it."""
    start = C.ffs[1].q_w.get_end()
    p0, p1 = C.q_l.get_center().copy(), target.get_center()

    def upd(q, a):
        q.move_to(p0 + a * (p1 - p0))
        x = max(q.get_left()[0] - 0.05, start[0] + 0.05)
        w.put_start_and_end_on(start, np.array([x, start[1], 0.0]))
    return UpdateFromAlphaFunc(C.q_l, upd)


SHIFT0 = 3.0          # the two-FF circuit enters centred, then slides left by this


class Cascade(NarratedScene):
    def construct(self):
        A = answer_box()
        C = cascade_chain()
        base = [C.btn, C.d0_w, C.d0_l, C.ffs[0], C.names[0], C.links[0], C.d1_l, C.ffs[1], C.names[1],
                C.q_l, C.bus, C.jdots[0], C.clk_ws[0], C.clk_ws[1], C.clk_l]

        # ---------------------------------------------------------------- clip 1
        with self.say("c5.cascade.1") as c:
            self.play(FadeIn(A), run_time=0.6)
            long_tag = T("too long?", 34, RED).next_to(A, RIGHT, buff=0.35)
            c.wait_until("too long")
            self.play(*appear(long_tag), run_time=1.0)

            c.wait_until("cascade")
            for m in base:
                m.shift(SHIFT0 * RIGHT)
            self.play(*appear(*base, shift=None, lag=0.06), run_time=min(1.6, c.until("cascade more")))
            c.wait_until("more flip-flops")
            self.play(*[m.animate.shift(SHIFT0 * LEFT) for m in base], run_time=1.2)

            c.wait_until("input flip-flop")
            yb = C.by - 0.12
            br0 = span_brace(_p(C.ffs[0].d_w.get_start()[0], yb), _p(C.ffs[0].q_w.get_end()[0], yb),
                             DOWN, color=DIM, buff=0.12)
            bl0 = T("input flip-flop", 30, FG).next_to(br0, DOWN, buff=0.12)
            self.play(GrowFromCenter(br0), *appear(bl0), run_time=0.9)

            c.wait_until("third")
            q3 = C.q_at(3)
            self.play(*during([C.q_l.animate.move_to(q3), *recolor([C.ffs[1].q_w, C.ffs[1].q_l], TEAL),
                               Transform(C.bus, C.bus_to(3))], 0, 0.5),
                      *during([FadeIn(m, shift=0.4 * LEFT) for m in stage(C, 2)] + [FadeIn(C.jdots[1])], 0.5, 1),
                      run_time=min(1.4, c.until("or a fourth")))
            c.wait_until("fourth")
            q4 = C.q_at(4)
            self.play(*during([C.q_l.animate.move_to(q4), *recolor([C.ffs[2].q_w, C.ffs[2].q_l], TEAL),
                               Transform(C.bus, C.bus_to(4))], 0, 0.5),
                      *during([FadeIn(m, shift=0.4 * LEFT) for m in stage(C, 3)]
                              + [FadeIn(C.dots), FadeIn(C.jdots[2])], 0.5, 1),
                      run_time=min(1.3, c.until("in a chain")))
            c.wait_until("longer")
            brK = span_brace(_p(C.ffs[1].d_w.get_start()[0], yb), _p(C.q_l.get_right()[0], yb),
                             DOWN, color=DIM, buff=0.12)
            blK = T("K additional flip-flops", 30, FG).next_to(brK, DOWN, buff=0.12)
            self.play(GrowFromCenter(brK), *appear(blK), run_time=min(1.0, c.until(None)))

        # ---------------------------------------------------------------- clip 2
        with self.say("c5.cascade.2") as c:
            tags = [MathTex(r"P_{\text{fail}}", font_size=40, color=GOLD)
                    .next_to(C.ffs[i].box, UP, buff=0.2) for i in (1, 2, 3)]
            tags[2].set_opacity(0.55)
            self.play(*appear(*tags, lag=0.45), run_time=min(1.8, c.until("kfold")))

            c.wait_until("so with k additional")
            f1 = MathTex(r"P_{\text{fail}_K} = (P_{\text{fail}})^K", font_size=48, color=FG)
            f1.move_to(_p(0.6, -1.75))
            mid = tags[1].get_center()
            self.play(*during([t.animate.move_to(mid).set_opacity(0) for t in (tags[0], tags[2])]
                              + [tags[1].animate.set_opacity(0)], 0, 0.45),
                      *during(appear(f1), 0.45, 1), run_time=1.6)
            self.remove(*tags)
            c.wait_until("power")
            self.play(FlashAround(f1[0][-1], run_time=1.2, time_width=1.5),
                      FlashAround(blK[0], run_time=1.2, time_width=1.5))

            # K = 1: trim back to FF0 + FF1
            c.wait_until("kone")
            # boxes, glyphs, stubs and triangles go first while the bus retracts with them; the pin-row
            # wires hold Q until one GREEN wire from FF1 takes over, then Q slides in with the wire's end.
            wires = [C.links[1], C.links[2]] + [w for i in (2, 3) for w in (C.ffs[i].d_w, C.ffs[i].q_w)]
            body = [p for i in (2, 3) for p in (C.ffs[i].box, C.ffs[i].tri, C.ffs[i].d_l, C.ffs[i].q_l,
                                                 C.names[i], C.clk_ws[i])] + [C.dots, C.jdots[1], C.jdots[2]]
            qw = q_wire(C)
            self.play(*during([FadeOut(m) for m in body] + [FadeOut(br0), FadeOut(bl0), FadeOut(brK),
                                                            FadeOut(blK), Transform(C.bus, C.bus_to(2))], 0, 0.3),
                      *during([FadeIn(qw), *recolor([C.ffs[1].q_w, C.ffs[1].q_l], GREEN)], 0.2, 0.4),
                      *during([FadeOut(m) for m in wires], 0.3, 0.45),
                      *during([slide_q(C, qw, C.q_at(2))], 0.45, 0.85),
                      *during([f1.animate.move_to(_p(0.6, -1.0))], 0.45, 1),
                      run_time=1.8)
            self.remove(qw)
            k1 = T("K = 1: Part 4's synchroniser", 34, YELLOW).move_to(_p(3.3, 0.6))
            self.play(*appear(k1), run_time=0.9)

            f2 = MathTex(r"\text{Hence, }P_{\text{fail}_K}/\text{s} = N\,P_{\text{fail}_K} = N(P_{\text{fail}})^K",
                         font_size=44, color=FG).move_to(_p(0.6, -1.85))
            c.wait_until("multiply")
            self.play(*appear(f2), run_time=1.0)

            c.wait_until("mtbfk")
            for m in (C.ffs[2].q_w, C.ffs[2].q_l):
                m.set_color(TEAL)
            for m in (stage(C, 3) + [C.dots]):
                fade_ghost(m)
            qw = q_wire(C)
            self.add(qw)
            self.play(*during(disappear(k1), 0, 0.3),
                      *during([slide_q(C, qw, C.q_at(4))], 0.2, 0.55),
                      *during([FadeIn(m) for m in wires], 0.55, 0.7),
                      *during([UpdateFromAlphaFunc(qw, lambda m, a: m.set_stroke(opacity=1 - a)),
                               *recolor([C.ffs[1].q_w, C.ffs[1].q_l], TEAL)], 0.6, 0.8),
                      *during([FadeIn(m) for m in body] + [Transform(C.bus, C.bus_to(4))], 0.75, 1),
                      run_time=1.8)
            self.remove(qw)
            f3 = MathTex(r"\text{MTBF} = 1/(N(P_{\text{fail}})^K)", font_size=48, color=YELLOW)
            f3.move_to(_p(0.6, -2.75))
            self.play(*appear(f3), run_time=1.2)

        # ---------------------------------------------------------------- clip 3
        with self.say("c5.cascade.3") as c:
            F = VGroup(f1, f2, f3)
            dy = 2.65 - f1.get_y()
            sweep_clear(self, *[m.animate.shift(dy * UP).set_x(0) for m in (f1, f2, f3)],
                        keep=[A, f1, f2, f3], run_time=min(1.4, c.until("low")))
            cond = MathTex(r"P_{\text{fail}} \ll 1", font_size=56, color=YELLOW).move_to(_p(0, -0.05))
            c.wait_until("much lower")
            self.play(*appear(cond), run_time=1.0)

            c.wait_until("half")
            h2 = MathTex(r"(0.5)^2 = 0.25", font_size=48, color=RED).move_to(_p(-3.6, -1.25))
            self.play(*appear(h2), run_time=1.0)
            c.wait_until("each extra")
            h3 = MathTex(r"(0.5)^3 = 0.125", font_size=48, color=RED).next_to(h2, DOWN, buff=0.3)
            h3.align_to(h2, LEFT)
            hcap = T("each flip-flop only halves it", 30, RED).next_to(h3, DOWN, buff=0.35).set_x(-3.6)
            self.play(*appear(h3), run_time=1.0)
            c.wait_until("only cut")
            self.play(*appear(hcap), run_time=1.0)

            c.wait_until("tiny")
            t2 = MathTex(r"(10^{-7})^2 = 10^{-14}", font_size=48, color=GREEN).move_to(_p(3.6, -1.25))
            self.play(*appear(t2), run_time=1.2)
            tcap = T("10 million times smaller", 30, GREEN).next_to(t2, DOWN, buff=0.4)
            c.wait_until("fourteen")
            self.play(*appear(tcap), run_time=1.0)

        # ---------------------------------------------------------------- clip 4
        with self.say("c5.cascade.4") as c:
            head = T("by the slide's formula (ours)", 32, DIM, slant=ITALIC).move_to(_p(0, 1.15))
            panel = RoundedRectangle(corner_radius=0.15, width=11.4, height=3.9).set_stroke(DIM, 2)
            panel.move_to(_p(0, -0.35))
            c.wait_until("our example")
            sweep_clear(self, f3.animate.move_to(_p(0, 2.35)), keep=[A, f3], run_time=1.4)
            self.play(FadeIn(panel), *appear(head), run_time=min(1.0, c.until("two")))
            k2 = MathTex(r"K = 2", font_size=48, color=FG).move_to(_p(0, 0.25))
            c.wait_until("two")
            self.play(*appear(k2), run_time=1.0)

            c.wait_until("keep")
            r1 = MathTex(r"T_c = 3.04\text{ ns} \;\rightarrow\; \text{MTBF} \approx 7\text{ million years}",
                         font_size=44, color=FG).move_to(_p(0, -0.8))
            r1[0][-13:].set_color(GREEN)
            self.play(FlashAround(A, run_time=1.4, time_width=1.5), *appear(r1), run_time=1.4)

            c.wait_until("shrink")
            r2 = MathTex(r"\text{MTBF} = 1\text{ year} \;\rightarrow\; T_c \approx 1.6\text{ ns}",
                         font_size=44, color=FG).move_to(_p(-1.4, -1.9))
            r2[0][-5:].set_color(GREEN)
            self.play(*appear(r2), run_time=1.2)
            aside = MathTex(r"(K = 1:\ 3.03\text{ ns})", font_size=36, color=DIM)
            aside.next_to(r2, RIGHT, buff=0.6)
            c.wait_until("from about")
            self.play(*appear(aside), run_time=1.0)

        self.wait(2.8)                                                    # let the results sit
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
