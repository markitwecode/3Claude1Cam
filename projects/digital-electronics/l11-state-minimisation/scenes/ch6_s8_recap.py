"""Chapter 6, scene 8: recap in six panels, the lecture's road, and Lecture 12's potential divider. Clips c6.recap.1 – c6.recap.3.

Grid: "Recap" T 44 at the top, six faint DIM slot frames (3 x 2), each panel the chapter's own object
(load_scene, scaled down), its short line under it.
 r1 s2's Loop + LoopElectrons (jittering, drifting) and its train; r2 s2's loop with s3's GOLD clockwise
 arrows and BLUE electron arrow, s3's i_eq_qt() and "1 A = 1 C/s"; r3 s4's handover_shot() (lit lamp,
 V_B / V_L); r4 s5's two substitutions collapsing into the boxed P = IV; r5 s2's resistor beside a
 straight I-V line through the origin, V = IR; r6 s7's kcl_junction() and kvl_loop() with their equations.
{lecture}: the grid clears; ch1 s7's seven_diagram(), ch4 s6's sync_gal() (labels dropped)
with the synchroniser's coloured AND gates, and s4's lit loop, joined by arrows, tagged.
End card (Lecture 12 opens on it): end_card() = "Next lecture", the heading, p. 170's last bullet and a
DIM potential-divider silhouette with a YELLOW "?" between the resistors; handover_shot() returns it.
"""
# style: 2
# handover: next
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

S2 = load_scene("ch6_s2_electrons")
S3 = load_scene("ch6_s3_current")
S4 = load_scene("ch6_s4_volts")
S5 = load_scene("ch6_s5_power")
S7 = load_scene("ch6_s7_kirchhoff")
L7 = load_scene("ch1_s7_left")
SY = load_scene("ch4_s6_sync")


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the grid ---------------------------------------------------------------------------------
XS = (-4.5, 0.0, 4.5)
YS = (1.35, -1.7)
SW, SH = 4.2, 2.9
CAP = 30


XS2 = (-4.65, -0.45, 4.2)      # bottom row: r6 wider, so the KVL equation reads at full size
WS2 = (3.9, 3.9, 4.8)


def slot(i):
    return (XS if i < 3 else XS2)[i % 3], YS[i // 3]


def slot_w(i):
    return SW if i < 3 else WS2[i % 3]


def pic_c(i):
    x, y = slot(i)
    return _p(x, y + 0.3)


def cap_c(i):
    x, y = slot(i)
    return _p(x, y - 1.15)


def frame(i):
    x, y = slot(i)
    return RoundedRectangle(corner_radius=0.15, width=slot_w(i), height=SH).set_stroke(DIM, 2, opacity=0.5).move_to(_p(x, y))


def fit(m, w, h):
    m.scale(min(w / m.width, h / m.height))
    return m


def _no_signs(b):
    b.remove(b.plus_sign, b.minus_sign)


# ---- panels -----------------------------------------------------------------------------------
K = 0.37  # loop panels' scale


def panel_r1():
    shot = S2.handover_shot()
    loop, els = shot
    _no_signs(loop.battery)
    shot.scale(K).move_to(_p(slot(0)[0], slot(0)[1] + 0.12))
    els.place_all()
    train = S2._train(n=6).scale(K)
    train.move_to(_p(loop.get_x() + 0.3, loop.bounds()[3] + 0.22))
    cap = T("slow drift, all at once", CAP).move_to(cap_c(0))
    return shot, loop, els, train, cap


def panel_r2():
    loop = S2.Loop()
    _no_signs(loop.battery)
    L, R, B, Tp = loop.bounds()
    cy = (B + Tp) / 2
    o = 0.45
    Lo, Ro, Bo, To = L - o, R + o, B - o, Tp + o
    A = S2.current_arrow
    gold = VGroup(A([Lo, cy + 0.6, 0], [Lo, Tp - 0.3, 0]).arrow,
                  A([-1.4, To, 0], [1.4, To, 0]).arrow,
                  A([Ro, cy + 0.9, 0], [Ro, cy - 0.9, 0]).arrow,
                  A([Lo, B + 0.4, 0], [Lo, cy - 0.65, 0]).arrow)
    blue = Arrow([R - 0.6, cy - 1.0, 0], [R - 0.6, cy + 1.0, 0], buff=0, stroke_width=5,
                 color=BLUE, max_tip_length_to_length_ratio=0.3, tip_length=0.24)
    pic = VGroup(loop, gold, blue).scale(K).move_to(pic_c(1))
    for a in (*gold, blue):
        a.set_stroke(width=4)
    eq = S3.i_eq_qt(48).move_to(loop.get_center() + LEFT * 0.15)
    amp = T("1 A = 1 C/s", CAP, t2c={"1 A": GOLD}).move_to(cap_c(1))
    return pic, loop, gold, blue, eq, amp


def panel_r3():
    g = S4.handover_shot()
    g.scale(0.32).move_to(pic_c(2))
    for lab, arr, side in ((g.vb.label, g.vb.arrow, LEFT), (g.vl.label, g.vl.arrow, RIGHT)):
        lab.scale(2.1).next_to(arr, side, buff=0.08)
    b = g.loop.battery
    b.remove(b.plus_sign, b.minus_sign)
    cap = T("1 V = 1 J/C", CAP, t2c={"1 V": TEAL}).move_to(cap_c(2))
    return g, cap


def panel_r4():
    c = pic_c(3)
    s1 = S5.mt("E", "=", "Q", "V_L", size=36)
    s2 = S5.mt("Q", "=", "I", "t", size=36)
    S5.at_eq(s1, 1, c[1] + 0.45, x=c[0] - 1.2)
    S5.at_eq(s2, 1, c[1] - 0.45, x=c[0] - 1.2)
    res = S5.mt("P", "=", "I", "V", size=50)
    res.move_to(c + RIGHT * 0.85)
    box = SurroundingRectangle(res, color=YELLOW, buff=0.18, corner_radius=0.1)
    cap = T("power, in watts", CAP).move_to(cap_c(3))
    return s1, s2, res, box, cap


def panel_r5():
    c = pic_c(4)
    res = S2.resistor().move_to(c + LEFT * 1.3)
    ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=1.6, y_length=1.6, tips=True,
              axis_config={"color": DIM, "stroke_width": 3, "include_ticks": False,
                           "tip_width": 0.16, "tip_height": 0.16})
    ax.shift(c + _p(-0.3, -0.85) - ax.c2p(0, 0))
    xl = MathTex("V", font_size=38, color=TEAL).next_to(ax.x_axis.get_right(), RIGHT, buff=0.12)
    yl = MathTex("I", font_size=38, color=GOLD).next_to(ax.y_axis.get_top(), RIGHT, buff=0.15)
    line = Line(ax.c2p(0, 0), ax.c2p(3.6, 3.4)).set_stroke(FG, 5)
    o = Dot(ax.c2p(0, 0), radius=0.08, color=YELLOW).set_z_index(2)
    graph = VGroup(ax, xl, yl, line, o)
    eq = MathTex("V", "=", "I", "R", font_size=48)
    eq[0].set_color(TEAL)
    eq[2].set_color(GOLD)
    eq.move_to(cap_c(4))
    return res, graph, eq


def panel_r6():
    x, y = slot(5)
    kcl = S7.kcl_junction()
    kcl.remove(kcl.labels)
    fit(kcl, 1.8, 1.05).move_to(_p(x - 1.2, y + 0.85))
    kvl = S7.kvl_loop()
    kvl.remove(kvl.vlabels, kvl.names)
    for b in kvl.bats:
        _no_signs(b)
    fit(kvl, 1.9, 1.1).move_to(_p(x + 1.15, y + 0.85))
    e1 = MathTex("I_1", "+", "I_2", "=", "I_3", font_size=40, color=GOLD).move_to(_p(x - 1.2, y - 0.05))
    e1[1].set_color(FG)
    e1[3].set_color(FG)
    e2 = MathTex("V_1{-}V_2{-}V_3{-}V_4{-}V_5{+}V_6=0", font_size=40, color=TEAL).move_to(_p(x, y - 0.85))
    if e2.width > slot_w(5) - 0.2:
        e2.scale((slot_w(5) - 0.2) / e2.width)
    return kcl, kvl, e1, e2


# ---- the lecture's road -----------------------------------------------------------------------
RX = (-4.6, 0.0, 4.6)
RY = 0.2
RW, RH = 3.4, 2.7


def seven_thumb():
    d = L7.seven_diagram()
    for m in list(d.labels.values()) + list(d.ret_labels.values()):
        d.remove(m)
    for s in d.states.values():
        s.remove(s.letter)
        s.circle.set_stroke(BLUE, 4)
    return fit(d, RW, RH).move_to(_p(RX[0], RY))


def _strip_text(m):
    for sub in list(m.submobjects):
        if isinstance(sub, (Text, MathTex, SingleStringMathTex)):
            m.remove(sub)
        else:
            _strip_text(sub)


def gal_thumb():
    """ch4 s6's synchroniser GAL, its coloured AND gates and kept dots; the labels are dropped (too small)."""
    g = SY.sync_gal()
    g.remove(*g.in_labels, *g.rail_labels, *g.out_labels, *g.terms)
    _strip_text(g)
    return fit(g, RW, RH).move_to(_p(RX[1], RY))


def lamp_thumb():
    g = S4.handover_shot()
    g.vb.remove(g.vb.label)
    g.vl.remove(g.vl.label)
    b = g.loop.battery
    b.remove(b.plus_sign, b.minus_sign)
    return fit(g, RW, RH * 0.9).move_to(_p(RX[2], RY))


# ---- end card ---------------------------------------------------------------------------------
def divider_silhouette():
    L, R, Tp, B = -1.8, 1.8, 0.35, -3.35
    yb, y1, y2 = (Tp + B) / 2, -0.55, -2.45
    node_y = (y1 + y2) / 2
    h, rs = S2.BAT_H / 2, S2.SLOT_H / 2
    wire = VGroup(
        VMobject().set_points_as_corners([_p(L, yb + h), _p(L, Tp), _p(R, Tp), _p(R, y1 + rs)]),
        Line(_p(R, y1 - rs), _p(R, y2 + rs)),
        VMobject().set_points_as_corners([_p(R, y2 - rs), _p(R, B), _p(L, B), _p(L, yb - h)]),
    ).set_stroke(DIM, S2.WIRE_W)
    bat = S2.battery()
    bat.remove(bat.plus_sign, bat.minus_sign)
    bat.set_color(DIM).move_to(_p(L, yb))
    r1 = S2.resistor().move_to(_p(R, y1))
    r2 = S2.resistor().move_to(_p(R, y2))
    for r in (r1, r2):
        r.set_stroke(DIM)
    dot = Dot(_p(R, node_y), radius=0.11, color=DIM)
    q = T("?", 72, YELLOW).next_to(dot, RIGHT, buff=0.4)
    g = VGroup(wire, bat, r1, r2, dot)
    g.q = q
    return g


def headings():
    nxt = T("Next lecture", 30, DIM).move_to(_p(0, 3.3))
    h1 = T("Electronics, Devices and Circuits", 44).move_to(_p(0, 2.7))
    quote = T("“We will now analyse a simple 2 resistor circuit\nknown as a potential divider”", 34,
              DIM, slant=ITALIC, t2c={"potential divider": YELLOW}).move_to(_p(0, 1.6))
    g = VGroup(nxt, h1, quote)
    g.nxt, g.h1, g.quote = nxt, h1, quote
    return g


def end_card():
    h = headings()
    sil = divider_silhouette()
    g = VGroup(h, sil, sil.q)
    g.heads, g.sil, g.q = h, sil, sil.q
    return g


def handover_shot():
    return end_card()


# =============================================================================================
class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)          # end card, the music carries it; Lecture 12 opens on this frame

    def show(self, c, cue, *anims, rt=1.2, nxt=None):
        c.wait_until(cue)
        self.play(*anims, run_time=min(rt, c.until(nxt)) if nxt else rt)

    # -- c6.recap.1 ---------------------------------------------------------------------------------
    def clip1(self):
        head = T("Recap", 44).move_to(_p(0, 3.2))
        frames = [frame(i) for i in range(6)]
        shot, loop, els, train, cap1 = panel_r1()
        pic2, loop2, gold, blue, eq2, amp2 = panel_r2()
        g3, cap3 = panel_r3()
        self.head, self.frames = head, frames
        with self.say("c6.recap.1") as c:
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames], run_time=min(1.2, c.until("r1")))
            # r1: the loop, electrons jittering and drifting together, the train
            c.wait_until("r1")
            els.start()
            self.play(FadeIn(shot), FadeIn(train), *els.motion(drift=0.16, jitter=0.45),
                      run_time=1.2)
            c.wait_until("slowly")
            self.play(*appear(cap1), train.animate(rate_func=linear).shift(LEFT * 0.35), run_time=2.0)  # early: the line sums up the sentence
            # r2: conventional current, then the amp
            c.wait_until("r2")
            self.play(FadeIn(loop2), *[GrowArrow(a) for a in gold], run_time=1.5)
            c.wait_until("against the electrons")
            self.play(GrowArrow(blue), run_time=1.0)
            c.wait_until("one amp")
            self.play(*appear(eq2, amp2, shift=None, lag=0.3), run_time=1.2)  # early: the formula is read as the amp
            # r3: the volt
            c.wait_until("r3")
            self.play(FadeIn(g3), run_time=1.2)
            c.wait_until("one joule")
            self.play(*appear(cap3), run_time=1.0)  # early: "one joule per coulomb" is the J/C
        self.r1 = (shot, train, cap1, els)

    # -- c6.recap.2 ---------------------------------------------------------------------------------
    def clip2(self):
        s1, s2, res, box, cap4 = panel_r4()
        rres, graph, eq5 = panel_r5()
        kcl, kvl, e1, e2 = panel_r6()
        with self.say("c6.recap.2") as c:
            # r4: the two substitutions collapse into P = IV
            self.play(*appear(s1, s2, shift=None, lag=0.3), run_time=0.8)
            self.play(*during(set_alpha([s1, s2], 0.4), 0, 0.5),
                      *during([*appear(res, shift=0.3 * RIGHT), FadeIn(box)], 0.3, 1), run_time=1.2)
            # r5: resistor and its straight line
            c.wait_until("r5")
            self.play(FadeIn(rres), FadeIn(graph), *appear(cap4), run_time=1.2)  # early: r4's line lands as r5 starts
            c.wait_until("voltage is current")
            self.play(*appear(eq5), run_time=1.0)
            # r6: Kirchhoff
            c.wait_until("r6")
            self.play(FadeIn(kcl), *appear(e1, shift=None), run_time=1.2)  # early: the law for the junction
            c.wait_until("around every loop")
            self.play(FadeIn(kvl), *appear(e2, shift=None), run_time=1.2)  # early: the law for the loop
            # lecture: the grid clears, three pictures in a row
            c.wait_until("lecture")
            shot, train, cap1, els = self.r1
            new_head = T("This lecture", 44).move_to(_p(0, 3.2))
            self.play(*during([FadeOut(m, scale=0.6) for m in self.mobjects if m is not self.head], 0, 0.6),
                      *swap(self.head, new_head), run_time=1.2)
            els.stop()
            self.remove(*self.mobjects)
            self.add(new_head)
            pics = [seven_thumb(), gal_thumb(), lamp_thumb()]
            tags = [T(t, 34, YELLOW).move_to(_p(x, -2.0)) for t, x in
                    zip(("shrink it", "put it on a chip", "what it runs on"), RX)]
            arrs = [Arrow(_p(RX[k] + RW / 2 - 0.05, RY), _p(RX[k + 1] - RW / 2 + 0.05, RY), buff=0.1,
                          stroke_width=4, color=DIM, max_tip_length_to_length_ratio=0.35) for k in (0, 1)]
            c.wait_until("shrank")
            self.play(FadeIn(pics[0]), *appear(tags[0]), run_time=1.0)  # early: tag of the verb
            c.wait_until("put it on a chip")
            self.play(GrowArrow(arrs[0]), FadeIn(pics[1]), *appear(tags[1]), run_time=1.0)
            c.wait_until("asked")
            self.play(GrowArrow(arrs[1]), FadeIn(pics[2]), *appear(tags[2]), run_time=min(1.0, c.until(floor=0.6)))  # early: tag of the question

    # -- c6.recap.3: next lecture -------------------------------------------------------------------
    def clip3(self):
        card = end_card()
        h, sil, q = card.heads, card.sil, card.q
        with self.say("c6.recap.3") as c:
            sweep_clear(self, *appear(h.nxt, h.h1, shift=None, lag=0.3),
                        run_time=min(1.6, c.until("ohm")))  # early: the next lecture's heading
            c.wait_until("simple circuit")
            self.play(FadeIn(sil), run_time=1.2)
            c.wait_until("potential divider")
            self.play(*appear(h.quote, shift=None), FadeIn(q, scale=0.6), run_time=1.2)  # early: p. 170's bullet
