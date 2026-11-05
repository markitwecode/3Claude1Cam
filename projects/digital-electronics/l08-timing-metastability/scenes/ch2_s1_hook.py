"""Chapter 2, scene 1: title card, the set-up budget bar (late data, a slower clock fixes it), then the
path with its set-up/hold window and the race of a new value towards the old one. Clips c2.hook.1 – c2.hook.2.

Copied (not imported): ch1_s4_path's make_ff + path_diagram (verbatim geometry). The budget bar is ch1_s6_setup's
budget_bar + SEGS (copied verbatim, x0 -3.3, y 0.5), plus a label-free YELLOW T_c dimension arrow
(ch1_s6's dim_arrow geometry) under it. The window follows ch1 s3's GOLD band.

End layout (s6 recap tile 1 copies it): path_diagram() at scale 1, shifted 0.4 DOWN (pin row y = 0.7,
CLK bus y = -2.2, FF boxes centred (+-4.2, 0.1)); here the Q0 / D1 labels sit as in ch1_s4 (above the
wires). Window: GOLD band (no stroke, as ch1_s3's band) 2.8 x 0.55 centred (2.1, 1.75), split at x = 2.1 by a
YELLOW edge line; left half fill 0.1 with "set-up" at opacity 0.4, right half fill 0.85 ("hold"), labels
T 32 GOLD at y 2.3. Tokens: BLUE dots r 0.13 on the D1 wire, "old" at (3.1, 0.7), "new" at (2.15, 0.7),
tags T 30 BLUE just below.
"too soon?" T 36 YELLOW centred (2.3, -0.65). Budget bar (stretched form) scaled 0.3, top-right corner.
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# L6's make_ff (D flip-flop), copied from ch1_s4_path.py
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.1))
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.2)).set_stroke(YELLOW, 5)
    else:
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# =============================================================================================
# THE path, copied from ch1_s4_path.py
# =============================================================================================
P_FF_X = (-4.2, 4.2)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y                       # D / Q pin row (1.1)
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE         # the CLK line (-1.8)
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.0, 1.6


def path_diagram():
    P = VGroup()
    ffs = []
    for x in P_FF_X:
        f = make_ff(_p(x, P_FF_Y))
        f.remove(f.clk_w)
        ffs.append(f)
    P.ff0, P.ff1 = ffs
    P.names = [T(f"FF{i}", 36, FG).next_to(f.box, UP, buff=0.2) for i, f in enumerate(ffs)]
    x_q0 = P_FF_X[0] + BOX_W / 2 + WIRE
    x_d1 = P_FF_X[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=P_CL_W, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.cl_l = VGroup(T("Combinational", 32, BLUE), T("Logic (CL)", 32, BLUE)).arrange(DOWN, buff=0.12).move_to(P.cl)
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-P_CL_W / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(P_CL_W / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    P.q0_l = MathTex("Q_0", font_size=40, color=GREEN).next_to(_p(x_q0, P_PIN), UP, buff=0.15)
    P.d1_l = MathTex("D_1", font_size=40, color=BLUE).next_to(_p(x_d1, P_PIN), UP, buff=0.15)
    P.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(P.ff0.d_w, LEFT, buff=0.12)
    P.q1_l = MathTex("Q_1", font_size=40, color=GREEN).next_to(P.ff1.q_w, RIGHT, buff=0.12)
    P.clk_bus = Line(_p(P_BUS_X0, P_BUS), _p(P_FF_X[1], P_BUS)).set_stroke(YELLOW, 5)
    P.clk_dot = Dot(_p(P_FF_X[0], P_BUS), radius=0.08, color=YELLOW)
    P.clk_l = T("CLK", 34, YELLOW).next_to(_p(P_BUS_X0, P_BUS), LEFT, buff=0.15)
    P.clk_br0, P.clk_br1 = ffs[0].clk_w, ffs[1].clk_w
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1]
    P.add(*P.all)

    def clk_paths(width=10):
        s = P.clk_bus.get_start()
        out = []
        for br in (P.clk_br0, P.clk_br1):
            a, b = br.get_start(), br.get_end()
            out.append(VMobject().set_points_as_corners([s, a, b]).set_stroke(YELLOW, width))
        return out
    P.clk_paths = clk_paths
    return P


# ============================================================================
# THE lecture's budget bar, copied verbatim from ch1_s6_setup.py (which owns it)
# ============================================================================
BAR_H = 0.5          # segment / outline height
BAR_FILL = 0.85      # segment fill opacity (no stroke)
BAR_OUT_W = 3        # YELLOW outline stroke


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
    """One clock period as a budget (ch1_s6's helper, unchanged)."""
    g = VGroup()
    g.segs, g.syms, g.nums = [], [], []
    x = x0
    for tex, col, w in segs:
        r = Rectangle(width=w, height=BAR_H).set_stroke(width=0).set_fill(col, BAR_FILL)
        r.move_to([x + w / 2, y, 0])
        g.segs.append(r)
        x += w
    g.outline = Rectangle(width=total, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    g.outline.move_to([x0 + total / 2, y, 0]).set_z_index(1)
    if syms:
        for (tex, col, _), r in zip(segs, g.segs):
            g.syms.append(MathTex(tex, font_size=sym_size, color=col).next_to(r, UP, buff=0.15))
    g.tc = MathTex(tc_tex, font_size=44, color=YELLOW).next_to(g.outline, LEFT, buff=0.25)
    for txt, r in zip(nums or [], g.segs):
        if txt is not None:
            g.nums.append(T(txt, num_size, GOLD).next_to(r, DOWN, buff=0.2))
    g.add(*g.segs, g.outline, *g.syms, g.tc, *g.nums)
    return g


DIM_W = 3           # ch1_s6's dimension arrows


def tc_arrow(xa, xb, y):
    """ch1_s6's YELLOW T_c dimension arrow (its dim_arrow geometry), label-free: the bar's T_c names it."""
    return DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=YELLOW)


# ch1_s6's proportions: t_pc 1.2, t_pd 5.1, t_su 0.7; T_c 7.0, from x0 = -3.3
W_PC, W_PD, W_SU = 1.2, 5.1, 0.7
TC_LEN = W_PC + W_PD + W_SU
SEGS = [("t_{pc}", PINK, W_PC), ("t_{pd}", PURPLE, W_PD), ("t_{su}", GOLD, W_SU)]
BAR_X0 = -3.3
BAR_Y = 0.5
ARROW_Y = BAR_Y - BAR_H / 2 - 0.35
PD_GROW = 0.6        # {late}: t_pd grows; t_su now ends 0.5 past the period
GAP = 0.6            # {slower}: the slack before t_su


# =============================================================================================
# Window and tokens
# =============================================================================================
WIN_X, WIN_W, WIN_H = 2.1, 2.8, 0.55


def window(pin_y):
    W = VGroup()
    y = pin_y + 1.05
    W.left = (Rectangle(width=WIN_W / 2, height=WIN_H).set_stroke(width=0).set_fill(GOLD, 0.25)
              .move_to(_p(WIN_X - WIN_W / 4, y)))
    W.right = (Rectangle(width=WIN_W / 2, height=WIN_H).set_stroke(width=0).set_fill(GOLD, 0.25)
               .move_to(_p(WIN_X + WIN_W / 4, y)))
    W.edge = Line(_p(WIN_X, y - WIN_H / 2 - 0.12), _p(WIN_X, y + WIN_H / 2 + 0.12)).set_stroke(YELLOW, 4)
    W.l_lab = T("set-up", 32, GOLD).move_to(_p(WIN_X - WIN_W / 4, y + 0.55))
    W.r_lab = T("hold", 32, GOLD).move_to(_p(WIN_X + WIN_W / 4, y + 0.55))
    W.r_lab.align_to(W.l_lab, DOWN)
    W.add(W.left, W.right, W.edge, W.l_lab, W.r_lab)
    return W


def token(text, color, at):
    g = VGroup()
    g.dot = Dot(at, radius=0.13, color=color)
    g.tag = T(text, 30, color).next_to(g.dot, DOWN, buff=0.18)
    g.add(g.dot, g.tag)
    return g


class HoldHook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(1.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c2.hook.1: title, the set-up budget, late data, a slower clock -----------------------------
    def clip1(self):
        # the card is up whole before the voice starts, so all three lines hold ~3 s before {bar}
        card = title_card("Part 2 · Hold time")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole
        self.wait(0.6)
        with self.say("c2.hook.1") as c:
            B = budget_bar(SEGS, TC_LEN, x0=BAR_X0, y=BAR_Y)
            B.arrow = tc_arrow(BAR_X0, BAR_X0 + TC_LEN, ARROW_Y)
            B.add(B.arrow)
            self.B = B
            c.wait_until("bar")
            sweep_clear(self, time_span(GrowFromEdge(B.outline, LEFT), 0.7, 1.6),
                        time_span(GrowFromCenter(B.arrow), 0.7, 1.6),
                        *during(appear(B.tc, shift=None), 0.75, 1.0), run_time=1.6)  # early: the bar's period label
            rt = min(2.2, c.until("set-up time"))
            anims = []
            for i, (s_, y_) in enumerate(zip(B.segs, B.syms)):
                a0, a1 = 0.3 * i * rt, (0.3 * i + 0.4) * rt
                anims += [time_span(GrowFromEdge(s_, LEFT), a0, a1), time_span(FadeIn(y_), a0, a1)]
            self.play(*anims, run_time=rt)  # early: the budget shown whole
            ineq = MathTex("T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=52)
            for i, col in ((0, YELLOW), (2, PINK), (4, PURPLE), (6, GOLD)):
                ineq[i].set_color(col)
            ineq.move_to(_p(0.2, -1.4))
            self.ineq = ineq
            c.wait_until("set-up time")
            self.play(FlashAround(B.segs[2], color=GOLD, time_width=1.5, buff=0.08), run_time=1.2)
            c.wait_until("before the next edge")
            self.play(*appear(ineq, shift=None), run_time=1.2)  # early: the constraint just stated

            # {late}: t_pd grows, t_su pushed past the end, the overhang RED
            c.wait_until("late")
            pd, su = B.segs[1], B.segs[2]
            new_pd = (Rectangle(width=W_PD + PD_GROW, height=BAR_H).set_stroke(width=0).set_fill(PURPLE, BAR_FILL)
                      .move_to(_p(BAR_X0 + W_PC + (W_PD + PD_GROW) / 2, BAR_Y)))
            self.play(Transform(pd, new_pd), B.syms[1].animate.shift(PD_GROW / 2 * RIGHT),
                      su.animate.shift(PD_GROW * RIGHT), B.syms[2].animate.shift(PD_GROW * RIGHT),
                      run_time=min(1.8, c.until("arrives late")))
            bar_r = B.outline.get_right()[0]
            su_r = su.get_right()[0]
            over = (Rectangle(width=su_r - bar_r, height=BAR_H).set_stroke(width=0).set_fill(RED, BAR_FILL)
                    .move_to(_p((bar_r + su_r) / 2, BAR_Y)).set_z_index(0.5))
            self.over = over
            c.wait_until("arrives late")
            self.play(FadeIn(over), B.syms[2].animate.set_color(RED),
                      FlashAround(over, color=RED, time_width=1.5, buff=0.08), run_time=1.2)

            # {slower}: stretch the period until t_su fits, a GREEN gap before it
            c.wait_until("slower")
            W2 = W_PC + W_PD + PD_GROW + GAP + W_SU
            new_out = (Rectangle(width=W2, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
                       .move_to(_p(BAR_X0 + W2 / 2, BAR_Y)).set_z_index(1))
            new_arrow = tc_arrow(BAR_X0, BAR_X0 + W2, ARROW_Y)
            gx0 = BAR_X0 + W_PC + W_PD + PD_GROW
            gap = (Rectangle(width=GAP, height=BAR_H).set_stroke(width=0).set_fill(GREEN, 0.45)
                   .move_to(_p(gx0 + GAP / 2, BAR_Y)))
            self.play(Transform(B.outline, new_out), Transform(B.arrow, new_arrow),
                      su.animate.shift(GAP * RIGHT), B.syms[2].animate.shift(GAP * RIGHT).set_color(GOLD),
                      over.animate.shift(GAP * RIGHT).set_opacity(0),
                      *during([FadeIn(gap)], 0.5, 1.0),
                      run_time=min(2.0, c.until("room again")))
            self.remove(over)
            B.gap = gap
            settle(self, B, add=[gap])
            c.wait_until("so when")
            tick = check_mark(GREEN).next_to(ineq, RIGHT, buff=0.4)
            self.tick = tick
            self.play(*appear(tick, shift=None), FlashAround(gap, color=GREEN, time_width=1.5, buff=0.08),
                      run_time=1.2)

    # ---- c2.hook.2: the path, the window's two sides, the race --------------------------------------
    def clip2(self):
        B = self.B
        P = path_diagram()
        P.shift(0.4 * DOWN)
        pin = P.q0_w.get_start()[1]
        Wd = window(pin)
        with self.say("c2.hook.2") as c:
            words = [*B.syms, B.tc]
            shapes = VGroup(*B.segs, B.gap, B.outline, B.arrow).copy().scale(0.3)
            shapes.to_corner(UR, buff=0.5)
            corner = B.copy().scale(0.3)
            corner.shift(shapes.get_center() - VGroup(*corner.segs, corner.gap, corner.outline,
                                                      corner.arrow).get_center())
            self.play(*during(disappear(self.ineq, self.tick, *words), 0, 0.4),
                      *during([B.animate.scale(0.3).move_to(corner)], 0.3, 0.8),
                      *during(appear(*P.all, shift=None, lag=0.04), 0.4, 1.0),
                      run_time=1.8)
            self.remove(*words)
            for w in words:
                B.remove(w)
            settle(self, P)
            self.play(*appear(Wd.left, Wd.right, Wd.edge, Wd.l_lab, Wd.r_lab, shift=None, lag=0.15), run_time=min(1.0, c.until("sides")))  # early: the window drawn whole, then walked

            c.wait_until("sides")
            self.play(Wd.right.animate.set_fill(opacity=0.6), Wd.left.animate.set_fill(opacity=0.1),
                      Wd.l_lab.animate.set_opacity(0.4), run_time=1.2)
            c.wait_until("hold time")
            self.play(FlashUnder(Wd.r_lab, color=GOLD, time_width=1.5), run_time=1.2)

            # {edge}: one pulse along CLK into both triangles at once
            c.wait_until("edge")
            self.play(*[VShowPassingFlash(p, time_width=0.5) for p in P.clk_paths()], run_time=1.5, rate_func=linear)
            self.play(*flash([P.ff0.tri, P.ff1.tri]), FlashAround(Wd.edge, color=YELLOW), run_time=0.9)

            # {capture}: the old value on D1, held while the hold half glows
            old = token("old", BLUE, _p(3.1, pin))
            c.wait_until("capture")
            self.play(*appear(old), run_time=1.0)
            c.wait_until("old value")
            self.play(FlashAround(old.dot, color=BLUE, time_width=1.5),
                      Wd.right.animate.set_fill(opacity=0.85), run_time=1.2)
            self.play(Wd.right.animate.set_fill(opacity=0.6), run_time=0.8)

            # {launch}: a new value leaves FF0's Q
            q0x0 = P.q0_w.get_start()[0]
            new = token("new", GREEN, _p(q0x0 + 0.2, pin))
            c.wait_until("launch")
            self.play(*appear(new, shift=None), FlashAround(P.ff0.box, color=YELLOW, time_width=1.5),
                      run_time=1.0)
            cl_x0 = P.cl.get_left()[0]
            self.play(new.animate.shift((cl_x0 - 0.25 - new.dot.get_x()) * RIGHT),
                      run_time=min(1.8, c.until("race")), rate_func=linear)

            # {race}: through CL, out on D1, towards the old value
            c.wait_until("race")
            self.play(*disappear(new), run_time=0.5)
            flick = UpdateFromAlphaFunc(P.cl, lambda m, a: m.set_fill(YELLOW, 0.22 * abs(np.sin(2 * PI * a))))
            self.play(flick, run_time=0.9)
            P.cl.set_fill(BG, 1)
            out = token("new", BLUE, _p(P.cl.get_right()[0] + 0.25, pin))
            self.play(FadeIn(out), Wd.right.animate.set_fill(opacity=0.85), run_time=0.5)
            self.play(out.animate.shift((2.15 - out.dot.get_x()) * RIGHT),
                      run_time=min(1.5, c.until("question")), rate_func=rate_functions.ease_out_sine)

            # {question}
            q = T("too soon?", 36, YELLOW).move_to(_p(2.3, pin - 1.35))
            c.wait_until("question")
            self.play(*appear(q), run_time=1.0)
