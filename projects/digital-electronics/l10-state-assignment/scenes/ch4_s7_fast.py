"""Chapter 4, scene 7: as fast as it gets: no logic in the ring's loop, so T_c >= t_pc + t_su.
Clips c4.fast.1 – c4.fast.5.

Reuses L8's path_diagram() (ch1_s4_path) and budget_bar() (ch1_s6_setup), loaded by file path;
s3's ring4, s4's onehot_circuit / dashed_box, s5's l9_circuit.
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _load_l8(stem):
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_l8_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8P = _load_l8("ch1_s4_path")
L8B = _load_l8("ch1_s6_setup")
S3 = load_scene("ch4_s3_ring4")
S4 = load_scene("ch4_s4_outputs")
budget_bar = L8B.budget_bar


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- layout ----------------------------------------------------------------------------------------
BS = 1.3                                      # the ring's bar: L8's proportions x 1.3
SEG_L = [w * BS for (_, _, w) in L8B.SEGS]    # 1.56, 6.63, 0.91
BAR_X0, BAR_Y = -4.4, -1.35                   # clip 1
BAR_Y2, INEQ_Y2, INEQ_X3 = -2.45, -3.2, 2.2   # clip 2: bar lower, the inequality under it, then beside it
INEQ_Y = -2.9
RING_S, RING_TOP = 0.65, 3.55
P_S1, P_TOP1 = 0.85, 3.5                      # path diagram, clip 1
P_S2, P_TOP2 = 0.72, 1.35                     # clip 2 (ring above)
BAR_UP = 0.5                                  # clip 3: the ring's bar rises to this y
EX_Y = -2.5                                   # clip 3: L8's worked bar
C_S = 0.6                                     # clip 4: one-hot circuit scale
C_SHIFT = 2.65                                # ... and how far it moves left at {l9}
MIN_SIZE = 27


def legible(group, k, min_size=MIN_SIZE):
    """Before `group` is scaled by k: grow each text in it (about its own centre) so it ends >= min_size."""
    seen = set()
    for m in group.get_family():
        if id(m) in seen:
            continue
        if isinstance(m, (Text, SingleStringMathTex)):
            fs = m.font_size * k
            if fs < min_size:
                m.scale(min_size / fs)
            seen.update(id(s) for s in m.get_family())
    return group


def strip_pins(ffs):
    """Drop the D / Q / Q-bar letters inside small flip-flop boxes."""
    for f in ffs:
        for name in ("d_l", "q_l", "qb_l"):
            m = getattr(f, name, None)
            if m is not None and m in f.submobjects:
                f.remove(m)


def hide_heads(ring):
    """Drop the tiny traffic-light heads beside the r / ra / g / a labels (they read as boxes this small)."""
    ring.remove(*ring.heads)
    ring.heads = []


def ineq_tex(*parts, size=52):
    m = MathTex(*parts, font_size=size)
    cols = {"T_c": YELLOW, "t_{pc}": PINK, "t_{pd}": PURPLE, "t_{su}": GOLD}
    for i, p in enumerate(parts):
        if p in cols:
            m[i].set_color(cols[p])
        elif p[0].isdigit():
            m[i].set_color(GOLD)
    return m


class Fast(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(4.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------ c4.fast.1
    def clip1(self):
        P = L8P.path_diagram()
        legible(P, P_S2)
        P.scale(P_S1)
        P.shift((P_TOP1 - P.get_top()[1]) * UP)
        self.P = P
        bar = budget_bar([(t, c, w) for (t, c, _), w in zip(L8B.SEGS, SEG_L)], sum(SEG_L),
                         x0=BAR_X0, y=BAR_Y)
        self.bar = bar
        ineq = ineq_tex("T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}").move_to(_p(0, INEQ_Y))
        self.ineq = ineq
        with self.say("c4.fast.1") as c:
            # {limit}: L8's path returns
            self.play(*appear(P, shift=None), run_time=1.5)  # early: L8's diagram returns whole, then is walked
            c.wait_until("clock speed")
            self.play(*[VShowPassingFlash(p, time_width=0.6) for p in P.clk_paths()], run_time=1.4)
            # {path}: a pulse FF0 -> CL -> FF1
            c.wait_until("path")
            y = P.q0_w.get_y()
            run = Line(_p(P.ff0.box.get_x(), y), _p(P.ff1.box.get_x(), y)).set_stroke(YELLOW, 10)
            self.play(VShowPassingFlash(run, time_width=0.5), run_time=min(2.4, c.until("bar")))
            # {bar}: the outline, then each segment on its words
            c.wait_until("bar")
            self.play(GrowFromEdge(bar.outline, LEFT), *appear(bar.tc, shift=None), run_time=1.0)
            for k, cue in enumerate(("clock-to-output", "logic's delay", "set-up")):
                c.wait_until(cue)
                extra = during(appear(ineq, shift=None), 0.4, 1.0) if k == 2 else []
                self.play(GrowFromEdge(bar.segs[k], LEFT), *appear(bar.syms[k]), *extra,
                          run_time=0.9 if k < 2 else min(1.6, c.until(floor=0.8)))
            settle(self, bar)

    # ------------------------------------------------------------------------------------ c4.fast.2
    def clip2(self):
        P, bar = self.P, self.bar
        R = S3.ring4("1000")
        strip_pins(R.ffs)
        hide_heads(R)
        legible(R, RING_S).scale(RING_S)
        R.shift((RING_TOP - R.get_top()[1]) * UP)
        self.R = R
        P.generate_target()
        P.target.scale(P_S2 / P_S1)
        P.target.shift((P_TOP2 - P.target.get_top()[1]) * UP)
        with self.say("c4.fast.2") as c:
            # {ring}: the ring comes in above the path
            self.play(*during([MoveToTarget(P), bar.animate.shift((BAR_Y2 - BAR_Y) * UP),
                               self.ineq.animate.set_y(INEQ_Y2)], 0, 0.6),
                      *during(appear(R), 0.4, 1.0), run_time=1.8)
            c.wait_until("each output")
            # one link Q_r -> D_ra lights; r and ra fly onto FF0 / FF1
            wl, tip = R.wires[0]
            path = R.wire_paths[0].copy().scale(RING_S).move_to(R.wires[0]).set_stroke(GOLD, 8)
            lab_r = T("r", 36, GREEN).move_to(P.names[0])
            lab_ra = T("ra", 36, GREEN).move_to(P.names[1])
            hl = [f.box.copy().set_stroke(YELLOW, 6).set_fill(opacity=0) for f in (P.ff0, P.ff1)]
            self.play(VShowPassingFlash(path, time_width=0.7), wl.animate.set_stroke(YELLOW, 5),
                      tip.animate.set_fill(YELLOW, 1), run_time=0.9)
            self.play(*fly(R.cells[0], hl[0]), *fly(R.cells[1], hl[1]), run_time=1.2)
            self.play(*swap(P.names[0], lab_r), *swap(P.names[1], lab_ra), run_time=0.9)
            # {zero}: the CL box collapses to a bare wire; the PURPLE segment shrinks to nothing
            c.wait_until("zero")
            y = P.q0_w.get_y()
            bare = Line(_p(P.cl.get_left()[0], y), _p(P.cl.get_right()[0], y)).set_stroke(FG, 5)
            self.play(*during(disappear(P.cl_l), 0, 0.4),
                      *during([ReplacementTransform(P.cl, bare)], 0.3, 1.0), run_time=1.3)
            settle(self, P, add=[lab_r, lab_ra, bare, *hl], drop=[*P.names, P.cl, P.cl_l])
            P.names, P.cl = [lab_r, lab_ra], bare
            c.wait_until("logic's delay")
            pink, purple, gold = bar.segs
            sym_pd, sym_su = bar.syms[1], bar.syms[2]
            dx = purple.width
            flat = purple.copy().stretch_to_fit_width(0.01).align_to(purple, LEFT)
            out2 = bar.outline.copy().stretch_to_fit_width(bar.outline.width - dx).align_to(bar.outline, LEFT)
            tpd0 = MathTex("t_{pd}", "=", "0", font_size=44, color=PURPLE).move_to(_p(bare.get_x(), y - 0.6))
            self.play(*during(disappear(sym_pd), 0, 0.3),
                      *during([Transform(purple, flat), Transform(bar.outline, out2),
                               gold.animate.shift(dx * LEFT), sym_su.animate.shift(dx * LEFT)], 0.15, 0.8),
                      *during(appear(tpd0, shift=None), 0.7, 1.0),
                      run_time=min(2.2, c.until("shrink", floor=1.2)))
            self.remove(purple)
            settle(self, bar, drop=[purple, sym_pd])
            bar.segs, bar.syms = [pink, gold], [bar.syms[0], sym_su]
            self.tpd0 = tpd0
            # {shrink}: the inequality loses its middle term
            c.wait_until("shrink")
            ineq2 = ineq_tex("T_c", r"\ge", "t_{pc}", "+", "t_{su}").move_to(_p(INEQ_X3, BAR_Y2))
            old = self.ineq          # T_c ≥ t_pc + t_pd + t_su: "t_pd +" fades out, then the rest closes up
            keep = {0: 0, 1: 1, 2: 2, 3: 3, 6: 4}
            gap = ineq2[4].get_left()[0] - ineq2[3].get_right()[0]
            self.play(*during([FadeOut(old[4], old[5], shift=0.3 * UP)], 0, 0.5),  # "t_pd +" leave as one
                      *during([old[6].animate.shift((old[3].get_right()[0] + gap - old[6].get_left()[0]) * RIGHT)],
                              0.5, 1.0), run_time=1.2)
            self.play(*[old[i].animate.move_to(ineq2[j]) for i, j in keep.items()], run_time=0.9)
            self.remove(*old.get_family())
            self.add(ineq2)
            self.ineq = ineq2
            # {nums}: L8's flip-flop numbers, then the sum
            n02 = T("0.2 ns", 30, GOLD).next_to(pink, DOWN, buff=0.2).align_to(pink, RIGHT).shift(0.25 * LEFT)
            n01 = T("0.1 ns", 30, GOLD).next_to(gold, DOWN, buff=0.2).align_to(gold, LEFT).shift(0.25 * RIGHT)
            c.wait_until("zero point two")
            self.play(*appear(n02), run_time=0.9)
            c.wait_until("zero point one")
            self.play(*appear(n01), run_time=0.9)
            settle(self, bar, add=[n02, n01])
            bar.nums = [n02, n01]
            c.wait_until("zero point three")
            add2 = ineq_tex("T_c", r"\ge", "0.2", "+", "0.1", "=", r"0.3\ \text{ns}").move_to(_p(INEQ_X3, BAR_Y2))
            self.play(*edit(ineq2, add2), run_time=min(1.6, c.until(floor=1.0)))
            self.ineq = add2

    # ------------------------------------------------------------------------------------ c4.fast.3
    def clip3(self):
        bar, R = self.bar, self.R
        add2 = self.ineq
        fq = MathTex("f_c", r"\le", r"\frac{1}{0.3\ \text{ns}}", r"\approx", r"3.3\ \text{GHz}", font_size=44)
        fq[0].set_color(YELLOW)
        fq[4].set_color(GOLD)
        fq.move_to(_p(2.7, BAR_UP - 1.2))
        tick = check_mark(GREEN).next_to(fq, RIGHT, buff=0.35)
        ex = budget_bar([(t, c, w * 0.6) for (t, c, w) in L8B.SEGS], L8B.TC_LEN * 0.6, x0=-4.4, y=EX_Y,
                        sym_size=32)
        ex.tc.scale(0.8).next_to(ex.outline, LEFT, buff=0.2)
        ex_nums = [T(v, 30, col).next_to(s, DOWN, buff=0.18)
                   for v, col, s in zip(("0.2", "4.7", "0.1"), (PINK, PURPLE, GOLD), ex.segs)]
        ex_cap = VGroup(MathTex(r"T_c \ge 5.0\ \text{ns}", font_size=40),
                        MathTex(r"f_c \le 200\ \text{MHz}", font_size=40)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ex_cap[0][0][3:].set_color(GOLD)
        ex_cap[1][0][3:].set_color(GOLD)
        ex_cap.move_to(_p(2.7, EX_Y + 0.1))
        alone = T("flip-flops alone", 32, GREEN)
        with self.say("c4.fast.3") as c:
            # {freq}: the path leaves; the ring's bar rises, its sum moves beside it
            dy = BAR_UP - BAR_Y2
            add2.generate_target()
            add2.target.scale(44 / 52).move_to(_p(2.7, BAR_UP + 0.1))
            self.play(*during(disappear(self.P, self.tpd0), 0, 0.4),
                      *during([bar.animate.shift(dy * UP), MoveToTarget(add2)], 0.35, 1.0), run_time=1.8)
            c.wait_until("three point three")
            self.play(*appear(fq, shift=None), run_time=1.1)
            c.wait_until("as fast")
            self.play(*appear(tick, shift=None), run_time=0.7)
            # {example}: L8's worked bar, small underneath
            c.wait_until("example")
            self.play(*appear(ex, *ex_nums, shift=None, lag=0.1), run_time=1.2)
            self.play(*appear(*ex_cap, lag=0.3), run_time=1.1)
            # {alone}: the ring's bar glows
            c.wait_until("alone")
            alone.next_to(bar.nums[0], DOWN, buff=0.35).set_x(bar.outline.get_x() + 0.3)
            self.play(FlashAround(VGroup(*bar.segs, bar.outline), color=GREEN, time_width=1.5, buff=0.15),
                      *during(appear(alone), 0.3, 1.0), run_time=1.5)
        self.ex = [ex, *ex_nums, *ex_cap]
        self.fq, self.tick, self.alone = fq, tick, alone

    # ------------------------------------------------------------------------------------ c4.fast.4
    def clip4(self):
        R = self.R
        C = S4.onehot_circuit()
        strip_pins(C.ring.ffs)
        hide_heads(C.ring)
        legible(C, C_S)
        box = S4.dashed_box(-7.0, 5.85, -0.38, 3.15, YELLOW)
        VGroup(C, box).scale(C_S, about_point=ORIGIN).shift(0.4 * UP)
        loop_tag = T("the loop", 32, YELLOW).next_to(box, UP, buff=0.15).align_to(box, LEFT).shift(0.2 * RIGHT)
        after = VGroup(T("after the loop:", 30, FG),
                       T("delays the lamps, not the clock", 30, FG)).arrange(DOWN, buff=0.12)
        after.next_to(C, DOWN, buff=0.35)
        others = [m for m in C.submobjects if m is not C.ring]
        S5 = load_scene("ch4_s5_compare")
        L9 = S5.l9_circuit()
        strip_pins(L9.ffs)
        L9.remove(*[m for pair in L9.in_labels for m in pair])
        for g in L9.gates:                     # the XOR and AND read as blobs at this scale: grow them about their output
            g.scale(1.5, about_edge=DOWN)
        k = 5.0 / L9.width
        legible(L9, k)
        L9.scale(5.0 / L9.width).move_to(_p(3.75, 1.35))
        l9_box = DashedVMobject(SurroundingRectangle(L9, buff=0.2).set_stroke(YELLOW, 3),
                                num_dashes=50, dashed_ratio=0.55)
        l9_bar = budget_bar([("t_{pc}", PINK, 0.9), ("t_{pd}", PURPLE, 2.0), ("t_{su}", GOLD, 0.6)], 3.5,
                            x0=2.35, y=-1.0, sym_size=34)
        l9_bar.tc.scale(0.85).next_to(l9_bar.outline, LEFT, buff=0.2)
        l9_tag = T("slower of ⊕ and AND", 30, PURPLE).next_to(l9_bar.segs[1], DOWN, buff=0.3)
        with self.say("c4.fast.4") as c:
            # {outside}: the board clears; the ring moves into the circuit; the OR gates hang below it
            c.wait_until("sit after")
            sweep_clear(self, *appear(C.ring, shift=None), run_time=1.6)
            self.play(*appear(*others, shift=None, lag=0.05), run_time=1.0)
            self.remove(C.ring, *others)
            self.add(C)
            self.play(FadeIn(box), *appear(loop_tag), run_time=0.9)
            c.wait_until("delay the lamps")
            self.play(*[FlashAround(g, color=BLUE, time_width=1.5) for g in C.gates],
                      *during(appear(after, shift=None), 0.3, 1.0), run_time=1.4)
            # {l9}: Lecture 9's circuit beside it, with its own loop and a bar with t_pd back
            c.wait_until("l9")
            self.play(*[m.animate.shift(C_SHIFT * LEFT) for m in (C, box, loop_tag, after)], run_time=1.3)
            self.play(*appear(L9, shift=None), FadeIn(l9_box), run_time=1.2)
            c.wait_until("so its")
            self.play(*appear(l9_bar, shift=None), run_time=1.1)
            self.play(FlashAround(l9_bar.segs[1], color=PURPLE, time_width=1.5),  # early: the tag sums up the sentence
                      *during(appear(l9_tag), 0.2, 1.0), run_time=1.2)

    # ------------------------------------------------------------------------------------ c4.fast.5
    def clip5(self):
        xe = -0.9                               # the clock edge
        bar = budget_bar([("t_{pc}", PINK, 2.4), ("t_{su}", GOLD, 1.4)], 3.8, x0=xe, y=-1.3)
        clk = VMobject().set_points_as_corners([_p(xe - 1.6, 2.2), _p(xe, 2.2), _p(xe, 2.95),
                                                _p(xe + 3.2, 2.95)]).set_stroke(YELLOW, 5)
        clk_l = T("CLK", 32, YELLOW).next_to(_p(xe - 1.6, 2.2), LEFT, buff=0.2)
        edge = DashedLine(_p(xe, 2.2), _p(xe, -1.55), dash_length=0.12).set_stroke(DIM, 2)
        a_y, h_y = 1.2, 0.25
        tpc = Arrow(_p(xe, a_y), _p(xe + 2.4, a_y), buff=0, stroke_width=5, color=PINK,
                    max_tip_length_to_length_ratio=0.12)
        tpc_l = MathTex("t_{pc}", font_size=40, color=PINK).next_to(tpc, UP, buff=0.12)
        win = Rectangle(width=1.5, height=0.42).set_stroke(GOLD, 3).set_fill(GOLD, 0.3)
        win.move_to(_p(xe + 0.75, h_y))
        win_l = MathTex("t_{hold}", font_size=40, color=GOLD).next_to(win, RIGHT, buff=0.2)
        tick = check_mark(GREEN).next_to(tpc, RIGHT, buff=0.3)
        tag = T("shift-register case (Lecture 8, Part 2)", 30, DIM).move_to(_p(0.5, -2.75))
        # verdict
        fast = T("fast", 52, GREEN)
        fast_tick = check_mark(GREEN)
        mini = budget_bar([("t_{pc}", PINK, 1.2), ("t_{su}", GOLD, 0.7)], 1.9, syms=False, y=0)
        mini.tc.scale(0.8).next_to(mini.outline, LEFT, buff=0.2)
        mini_n = T("0.3 ns", 34, GOLD)
        burn = T("burns flip-flops", 52, FG)
        v8, vs, v3 = T("8", 64, GOLD), T("vs", 36, DIM), T("3", 64, GOLD)
        nums = VGroup(v8, vs, v3).arrange(RIGHT, buff=0.45)
        c8 = T("one-hot", 28, DIM).next_to(v8, DOWN, buff=0.2)
        c3 = T("sequential", 28, DIM).next_to(v3, DOWN, buff=0.2)
        left = VGroup(VGroup(fast, fast_tick).arrange(RIGHT, buff=0.35),
                      VGroup(mini, mini_n).arrange(DOWN, buff=0.3)).arrange(DOWN, buff=0.8)
        left.move_to(_p(-3.5, 0.2))
        mini_n.set_x(mini.outline.get_x())
        right = VGroup(burn, VGroup(nums, c8, c3)).arrange(DOWN, buff=0.7)
        right.move_to(_p(3.4, 0.2))
        right[1].align_to(right[0], ORIGIN)
        with self.say("c4.fast.5") as c:
            # {hold}: back on the ring's bar, with L8's hold check
            c.wait_until("between flip-flops")
            sweep_clear(self, *during(appear(clk, clk_l, edge, bar, shift=None, lag=0.1), 0.5, 1.0), run_time=1.8)
            c.wait_until("reaches")
            self.play(GrowArrow(tpc), *during(appear(tpc_l), 0.4, 1.0), run_time=1.6)
            self.play(*appear(tag), run_time=1.0)  # early: names the case the voice names below
            c.wait_until("hold-time worry")
            self.play(GrowFromEdge(win, LEFT), *during(appear(win_l, shift=None), 0.4, 1.0), run_time=1.4)
            c.wait_until("designed")
            self.play(*appear(tick, shift=None), run_time=0.8)
            # {verdict}: two halves
            c.wait_until("one-hot machines")
            sweep_clear(self, run_time=1.0)
            c.wait_until("fast")
            self.play(*appear(fast, fast_tick, lag=0.3), *during(appear(mini, mini_n, shift=None), 0.4, 1.0),
                      run_time=1.4)
            c.wait_until("burning")
            self.play(*appear(burn), *during(appear(nums, c8, c3, shift=None), 0.4, 1.0), run_time=1.4)
