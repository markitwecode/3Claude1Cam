"""Chapter 3, scene 6: asynchronous inputs (PRE / CLR), why they exist, and CLR at work on a T
flip-flop. Clips c3.async.1 – c3.async.5.

The flip-flop box is ch2_s6_symbols.make_ff (copied, with ch2_s7_recap's `ins=`); PRE / CLR pins are
RED, CLR 0.55 right of the clock pin as in ch2_s7_recap. The timing sketch is the module-level
`async_sketch()` (the chapter recap reuses it). Unknown Q is drawn at both levels (ch2_s5_slave).
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


BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6          # D and Q pins sit 0.6 above the box centre
WIRE = 0.85          # D / Q wire length
EN_WIRE = 1.0        # clock wire length below the box
CLR_DX = 0.55        # CLR pin 0.55 right of the clock pin (ch2_s7_recap)


def _p(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=4):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- the flip-flop symbol (ch2_s6_symbols.make_ff, ch2_s7_recap's ins=) -----------------------
def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), scale=1.0, lab_k=1.0):
    """Box 1.5 x 2.6 (FG stroke 4), BLUE inputs left, Q / Q-bar (GREEN) right, YELLOW clock wire
    up to the triangle. Scaled by `scale` about the box centre, then labels grown by lab_k."""
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(*in_w, q_w, qb_w, clk_w, box, tri, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, clk_w, q_w, qb_w, in_w
    g.labels = [*in_l, q_l, qb_l]
    g.scale(scale, about_point=ORIGIN)
    for lab in g.labels:
        lab.scale(lab_k, about_point=lab.get_center())
    g.shift(_p(*center[:2]) if len(center) else ORIGIN)
    return g


def pin(ff, kind, size=30, length=None):
    """A RED async pin growing out of the box: PRE on top (centre), CLR underneath (0.55 right of
    the clock pin). Returns (wire, label); the wire runs from the box edge outwards."""
    s = ff.box.width / BOX_W
    c, hb = ff.box.get_center(), ff.box.height / 2
    L = (length if length is not None else EN_WIRE) * s
    if kind == "PRE":
        a = c + hb * UP
        b = a + L * UP
        w = Line(a, b).set_stroke(RED, 5)
        lab = T("PRE", size, RED).next_to(b, UP, buff=0.12)
    else:
        a = c + CLR_DX * s * RIGHT + hb * DOWN
        b = a + L * DOWN
        w = Line(a, b).set_stroke(RED, 5)
        lab = T("CLR", size, RED).next_to(b, DOWN, buff=0.12)
    return w, lab


# ---- switch and LED (ch2_s6_symbols; its toggle reads as off before it flips) -----------------
def toggle(v, color=BLUE):
    g = VGroup()
    track = RoundedRectangle(corner_radius=0.19, width=0.78, height=0.38).set_stroke(color, 3).set_fill(BG, 1)
    knob = Circle(radius=0.13).set_stroke(width=0)
    g.add(track, knob)
    g.track, g.knob, g.v, g.sw_color = track, knob, v, color

    def knob_pos(val):
        return g.track.get_center() + (0.2 if val else -0.2) * g.track.width / 0.78 * RIGHT
    g.knob_pos = knob_pos
    knob.move_to(knob_pos(v)).set_fill(color if v else DIM, 1)
    return g


def flip(sw, v):
    sw.v = v
    return sw.knob.animate.move_to(sw.knob_pos(v)).set_fill(sw.sw_color if v else DIM, 1)


def led(on):
    c = Circle(radius=0.21).set_stroke(GREEN, 3).set_fill(GREEN, 0.9 if on else 0.0)
    c.on = on
    return c


def set_led(l, on):
    l.on = on
    return l.animate.set_fill(GREEN, 0.9 if on else 0.0)


def flicker(l, seq):
    """The LED blinks through `seq` (0/1 states) and ends on seq[-1]."""
    def f(m, a):
        k = min(int(a * len(seq)), len(seq) - 1)
        m.set_fill(GREEN, 0.9 if seq[k] else 0.0)
    l.on = seq[-1]
    return UpdateFromAlphaFunc(l, f)


# ---- the timing sketch: T flip-flop, T = 1, CLR pulse between edges 1 and 2 -------------------
SK_X0, SK_X1 = -2.0, 6.5
SK_P = 1.6
SK_RISES = [SK_X0 + 0.5 + k * SK_P for k in range(5)]          # -1.5, 0.1, 1.7, 3.3, 4.9
SK_ROWS = {"CLK": 1.9, "CLR": 0.3, "Q": -1.4}
SK_AMP = 0.3
SK_A = SK_RISES[0] + 0.3 * SK_P                                  # CLR rises (Q drops) here
SK_B = SK_RISES[0] + 0.55 * SK_P                                 # CLR back low, well before edge 2


def async_sketch():
    """CLK / CLR / Q rows (labels at x < -2.2). Parts:
    .labels .clk .guides .ups (one YELLOW ▲ per rising edge) .clr_low .clr (with the pulse) .pulse
    .q_unk0 (both levels, power-on to edge 1) .q_unk1 (edge 1 to the drop) .q_drop (to 0 at once,
    then low to edge 2) .q_known (edges 2..5) .values (1, 0, 1 above Q) .mark (RED dashed line +
    "no clock edge"). The finished sketch: everything but .clr_low."""
    g = VGroup()
    y = lambda row, v: SK_ROWS[row] + (SK_AMP if v else -SK_AMP)  # noqa: E731
    r = SK_RISES
    g.labels = VGroup(*[T(n, 30, c).move_to(_p(0, SK_ROWS[n])).align_to(_p(SK_X0 - 0.25, 0), RIGHT)
                        for n, c in (("CLK", YELLOW), ("CLR", RED), ("Q", GREEN))])
    pts = [(SK_X0, y("CLK", 0))]
    for x in r:
        pts += [(x, y("CLK", 0)), (x, y("CLK", 1)), (x + SK_P / 2, y("CLK", 1)), (x + SK_P / 2, y("CLK", 0))]
    pts.append((SK_X1, y("CLK", 0)))
    g.clk = poly(pts, YELLOW)
    top, bot = y("CLK", 1) + 0.15, y("Q", 0) - 0.15
    g.guides = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 1.5).set_z_index(-2) for x in r])
    g.ups = VGroup(*[Triangle().scale(0.11).set_stroke(width=0).set_fill(YELLOW, 1)
                     .move_to(_p(x, SK_ROWS["CLK"])) for x in r])
    lo, hi = y("CLR", 0), y("CLR", 1)
    g.clr_low = poly([(SK_X0, lo), (SK_X1, lo)], RED)
    g.clr = poly([(SK_X0, lo), (SK_A, lo), (SK_A, hi), (SK_B, hi), (SK_B, lo), (SK_X1, lo)], RED)
    g.pulse = poly([(SK_A, lo), (SK_A, hi), (SK_B, hi), (SK_B, lo)], RED, 10)
    qh, ql = y("Q", 1), y("Q", 0)
    g.q_unk0 = VGroup(poly([(SK_X0, qh), (r[0], qh)], GREEN), poly([(SK_X0, ql), (r[0], ql)], GREEN))
    g.q_unk1 = VGroup(poly([(r[0], qh), (SK_A, qh)], GREEN), poly([(r[0], ql), (SK_A, ql)], GREEN))
    g.q_drop = poly([(SK_A, qh), (SK_A, ql), (r[1], ql)], GREEN)
    g.q_known = poly([(r[1], ql), (r[1], qh), (r[2], qh), (r[2], ql), (r[3], ql), (r[3], qh),
                      (r[4], qh), (r[4], ql), (SK_X1, ql)], GREEN)
    g.values = VGroup(*[T(v, 32, GREEN).move_to(_p((r[k] + r[k + 1]) / 2, qh + 0.32))
                        for k, v in ((1, "1"), (2, "0"), (3, "1"))])
    dash = DashedLine(_p(SK_A, lo - 0.1), _p(SK_A, qh + 0.1), dash_length=0.1).set_stroke(RED, 3)
    txt = T("no clock edge", 28, RED).next_to(_p(SK_A, ql), DOWN, buff=0.3)
    g.mark = VGroup(dash, txt)
    g.add(g.guides, g.labels, g.clk, g.ups, g.clr, g.q_unk0, g.q_unk1, g.q_drop, g.q_known,
          g.values, g.mark)
    return g


# ---- layouts ----------------------------------------------------------------------------------
TITLE_Y = 3.22
C1_FF = (0.0, -0.3)          # clip 1 hero, scale 1.1
C1_S = 1.25
C3_FF = (-1.6, 0.0)          # clip 3 hero, scale 1.2
C3_S = 1.2
ALL_X, ALL_Y, ALL_S = (-4.4, 0.0, 4.4), 0.15, 0.75
TF_C, TF_S = (-5.0, 0.35), 0.8   # clip 4 T flip-flop
ROW3_X, ROW3_Y, ROW3_S = (-2.6, 0.6, 3.8), 0.2, 0.7   # clip 2 power-on row
ROW5_X = (-4.0, -1.1, 1.8, 4.7)                        # clip 5 preview: 3 flip-flops, a 4th on {count}


class Async(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c3.async.1
    def clip1(self):
        with self.say("c3.async.1") as c:
            self.title = T("Asynchronous Inputs", 50).move_to(_p(0, TITLE_Y))
            line1 = T("It is common for the FF types we have mentioned to also\n"
                      "have additional so called ‘asynchronous’ inputs", 30,
                      line_spacing=0.9).move_to(_p(0, 2.38))
            ff = make_ff(C1_FF, scale=C1_S)
            qv = value_label("0", 42, GREEN).next_to(ff.q_w, RIGHT, buff=0.18)
            self.play(*appear(self.title, shift=None), run_time=1.0)  # early: slide heading
            self.play(*appear(ff, qv, shift=None, lag=0.2), *during(appear(line1), 0.3, 1.0),
                      run_time=min(1.8, c.until("independent")))
            c.wait_until("independent")
            # a RED input straight into the box from the side, past the clock
            ay = ff.box.get_center()[1] - 0.45 * C1_S
            bx = ff.box.get_left()[0]
            stub = Line(_p(bx - WIRE * C1_S, ay), _p(bx, ay)).set_stroke(RED, 5)   # a pin, like D's wire
            arr = Arrow(_p(-5.4, ay), _p(bx - WIRE * C1_S, ay), buff=0, stroke_width=6,
                        tip_length=0.3, max_tip_length_to_length_ratio=0.3).set_color(RED)
            cap = T("take effect independently of any clock or enable inputs", 30).move_to(_p(0, -3.45))
            self.play(GrowFromPoint(stub, stub.get_end()), run_time=0.8)
            self.play(GrowArrow(arr), run_time=1.2)
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("apply one")
            qv1 = value_label("1", 42, GREEN).move_to(qv)
            path = Line(_p(-5.4, ay), _p(bx, ay)).set_stroke(YELLOW, 10)
            self.play(VShowPassingFlash(path, time_width=0.6),
                      *during(swap(qv, qv1), 0.45, 1.0), run_time=1.4)
            self.play(FlashAround(qv1, color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until("pointless")
            qm = T("?", 72, YELLOW).next_to(ff.clk_w, RIGHT, buff=0.35)
            self.play(*appear(qm), run_time=1.0)
            c.wait_until("we spent")
            self.play(FlashAround(ff.tri, color=YELLOW, time_width=1.5, buff=0.08),
                      FlashAround(ff.clk_w, color=YELLOW, time_width=1.5, buff=0.08), run_time=2.0)

    # ------------------------------------------------------------------ c3.async.2
    def clip2(self):
        with self.say("c3.async.2") as c:
            sw = toggle(0, BLUE).scale(1.6).move_to(_p(-5.5, ROW3_Y)).set_z_index(2)
            sw_l = T("power", 30).next_to(sw, DOWN, buff=0.25)
            ffs, leds = [], []
            for x in ROW3_X:
                f = make_ff((x, ROW3_Y), scale=ROW3_S, lab_k=0.85 / ROW3_S)
                l_ = led(False).next_to(f.q_w, RIGHT, buff=0)
                ffs.append(f)
                leds.append(l_)
            sweep_clear(self, *appear(*ffs, shift=None, lag=0.15), *appear(sw, sw_l, shift=None),
                        *appear(*leds, shift=None), keep=[self.title], run_time=1.6)
            c.wait_until("what happens")
            self.play(flip(sw, 1), run_time=0.8)
            c.wait_until("power")
            seqs = [[1, 0, 1, 1, 0, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0, 1, 1, 0], [1, 1, 0, 1, 0, 0, 1, 0, 1]]
            self.play(*[flicker(l_, s) for l_, s in zip(leds, seqs)], run_time=2.2, rate_func=linear)
            c.wait_until("could be one")
            self.digits = []
            for l_, v in zip(leds, (1, 0, 1)):
                d = T(str(v), 36, GREEN).next_to(l_, UP, buff=0.18)
                q = T("?", 34, YELLOW).next_to(d, RIGHT, buff=0.08)
                self.digits += [d, q]
            self.play(*appear(*self.digits, lag=0.12), run_time=1.4)
            c.wait_until("machine")
            cap = T("a state nobody planned", 44, RED).move_to(_p(0, -2.75))
            self.play(*appear(cap), run_time=1.0)

    # ------------------------------------------------------------------ c3.async.3
    def clip3(self):
        with self.say("c3.async.3") as c:
            ff = make_ff(C3_FF, scale=C3_S)
            qv = value_label("?", 42, GREEN).next_to(ff.q_w, RIGHT, buff=0.18)
            sweep_clear(self, *appear(ff, qv, shift=None, lag=0.2), run_time=1.6)
            pre_w, pre_l = pin(ff, "PRE", 32)
            clr_w, clr_l = pin(ff, "CLR", 32)
            c.wait_until("top")
            self.play(GrowFromPoint(pre_w, pre_w.get_start()), *during(appear(pre_l), 0.4, 1.0),
                      run_time=1.0)
            c.wait_until("bottom")
            self.play(GrowFromPoint(clr_w, clr_w.get_start()), *during(appear(clr_l), 0.4, 1.0),
                      run_time=1.0)
            c.wait_until("clear")
            t_clr = T("Reset/Clear – force Q to 0", 34, t2c={"Q": GREEN}).next_to(clr_l, RIGHT, buff=0.4)
            self.play(*appear(t_clr), run_time=1.0)
            q0 = value_label("0", 42, GREEN).move_to(qv)
            self.play(VShowPassingFlash(Line(clr_w.get_end(), clr_w.get_start()).set_stroke(YELLOW, 10),
                                        time_width=0.8),
                      *during(swap(qv, q0), 0.4, 1.0), run_time=1.4)
            c.wait_until("preset")
            t_pre = T("Preset/Set – force Q to 1", 34, t2c={"Q": GREEN}).next_to(pre_l, RIGHT, buff=0.4)
            self.play(*appear(t_pre), run_time=1.0)
            q1 = value_label("1", 42, GREEN).move_to(qv)
            self.play(VShowPassingFlash(Line(pre_w.get_end(), pre_w.get_start()).set_stroke(YELLOW, 10),
                                        time_width=0.8),
                      *during(swap(q0, q1), 0.4, 1.0), run_time=1.4)
            c.wait_until("all")
            # D, J-K and T side by side, each with PRE on top and CLR underneath
            self.syms = []
            parts = []
            for x, ins, name in zip(ALL_X, ((("D", PIN_Y),), (("J", PIN_Y), ("K", -PIN_Y)), (("T", PIN_Y),)),
                                    ("D", "J-K", "T")):
                f = make_ff((x, ALL_Y), ins=ins, scale=ALL_S, lab_k=30 / (36 * ALL_S))
                pw, pl = pin(f, "PRE", 30)
                cw, cl = pin(f, "CLR", 30)
                self.syms.append(dict(ff=f, pre_w=pw, pre_l=pl, clr_w=cw, clr_l=cl))
                parts.append(VGroup(f, pw, pl, cw, cl))
            self.sym_groups = parts
            sweep_clear(self, *appear(*parts, shift=None, lag=0.2), run_time=1.6)

    # ------------------------------------------------------------------ c3.async.4
    def clip4(self):
        with self.say("c3.async.4") as c:
            # keep the T symbol: it moves left, loses PRE; T tied to 1; the sketch builds beside it
            D, JK, TT = self.syms
            parts = self.sym_groups
            # the parts went on screen as groups; split T's group into its pieces
            self.remove(parts[2])
            tf, clr_w, clr_l = TT["ff"], TT["clr_w"], TT["clr_l"]
            self.add(tf, clr_w, clr_l, TT["pre_w"], TT["pre_l"])
            k = TF_S / ALL_S
            P0 = tf.box.get_center()
            d = _p(*TF_C) - P0
            moves = [m.animate.scale(k, about_point=P0).shift(d) for m in (tf, clr_w, clr_l)]
            self.play(*disappear(parts[0], parts[1], TT["pre_w"], TT["pre_l"]),
                      *during(moves, 0.3, 1.0), run_time=2.0)
            one = T("1", 40, BLUE).next_to(tf.in_w[0], LEFT, buff=0.15)
            sk = self.sk = async_sketch()
            self.play(*appear(one, shift=None),
                      *appear(sk.guides, sk.labels, sk.clk, sk.ups, sk.clr_low, shift=None, lag=0.15),  # early: the sketch's rows are shown whole, then walked
                      run_time=min(1.8, c.until("unknown")))
            c.wait_until("unknown")
            self.play(*[Create(m) for m in sk.q_unk0], rate_func=linear, run_time=1.8)
            c.wait_until("edge1")
            self.play(FlashAround(sk.ups[0], color=YELLOW, time_width=1.5, buff=0.12),
                      *[Create(m) for m in sk.q_unk1], rate_func=linear, run_time=1.5)
            c.wait_until("pulse")
            self.play(ReplacementTransform(sk.clr_low, sk.clr),
                      VShowPassingFlash(sk.pulse.copy(), time_width=1.0, taper_width=0.1), run_time=1.6)
            c.wait_until("drop")
            self.play(Create(sk.q_drop), run_time=1.5)
            self.play(Create(sk.mark[0]), *during(appear(sk.mark[1]), 0.3, 1.0), run_time=1.2)  # early: names what the voice says at "no clock edge"
            c.wait_until("known")
            rt = min(4.5, c.until())
            r, x1 = SK_RISES, SK_X1
            frac = [(((r[k] + r[k + 1]) / 2) - r[1]) / (x1 - r[1]) for k in (1, 2, 3)]
            self.play(Create(sk.q_known, rate_func=linear),
                      *[time_span(FadeIn(v, shift=0.15 * DOWN), f * rt, min(rt, f * rt + 0.7))
                        for v, f in zip(sk.values, frac)],
                      run_time=rt)

    # ------------------------------------------------------------------ c3.async.5
    def clip5(self):
        with self.say("c3.async.5", gap=3.2) as c:   # hold the Part 4 tags before the final clear
            line = T("Often used to force a synchronous circuit\ninto a known state, say at start-up.", 38,
                     line_spacing=0.9).move_to(_p(0, 2.6))
            sweep_clear(self, *appear(line, shift=None), run_time=1.6)
            c.wait_until("zero")
            ffs, leds, clrs, digs = [], [], [], []
            for x, v in zip(ROW5_X, (1, 0, 1, 0)):
                f = make_ff((x, ROW3_Y - 0.3), ins=(("T", PIN_Y),), scale=ROW3_S, lab_k=0.85 / ROW3_S)
                l_ = led(v).next_to(f.q_w, RIGHT, buff=0)
                cw, _ = pin(f, "CLR", 30, length=1.25)
                dg = T(str(v), 34, GREEN).next_to(l_, UP, buff=0.18)
                ffs.append(f)
                leds.append(l_)
                clrs.append(cw)
                digs.append(dg)
            bus_y = clrs[0].get_end()[1]
            x_l = -5.05
            ff4, led4, clr4, dig4 = ffs.pop(), leds.pop(), clrs.pop(), digs.pop()   # slides in on {count}
            bus = Line(_p(x_l, bus_y), _p(clrs[-1].get_end()[0], bus_y)).set_stroke(RED, 5)
            bus4 = Line(_p(x_l, bus_y), _p(clr4.get_end()[0], bus_y)).set_stroke(RED, 5)
            bus_l = T("CLR", 30, RED).next_to(bus.get_start(), LEFT, buff=0.15)
            self.play(*appear(*ffs, shift=None, lag=0.15), *appear(*leds, *digs, shift=None),
                      run_time=1.5)
            self.play(*[GrowFromPoint(w, w.get_start()) for w in clrs], GrowFromPoint(bus, bus.get_end()),
                      *during(appear(bus_l), 0.4, 1.0), run_time=1.2)
            c.wait_until("cleared")
            flash_path = VMobject().set_points_as_corners(
                [bus.get_start(), bus.get_end()]).set_stroke(YELLOW, 10)
            news = [T("0", 34, GREEN).move_to(d) for d in digs]
            self.play(VShowPassingFlash(flash_path, time_width=0.7),
                      *[set_led(l_, 0) for l_ in leds],
                      *during(swap(digs[0], news[0]), 0.4, 1.0), *during(swap(digs[2], news[2]), 0.4, 1.0),
                      run_time=1.5)
            tag1 = T("Part 4: clear, then count", 30, YELLOW).move_to(_p(-3.2, -3.35))
            self.play(*appear(tag1), run_time=1.0)
            c.wait_until("count")
            tag2 = T("Part 4: back to 0 after 9", 30, YELLOW).move_to(_p(3.2, -3.35))
            # a decade counter needs four flip-flops: the fourth slides onto the row, on the same CLR line
            self.play(*[FadeIn(m, shift=1.2 * LEFT) for m in (ff4, led4, dig4)],
                      *during([ReplacementTransform(bus, bus4)], 0.4, 1.0),
                      *during([GrowFromPoint(clr4, clr4.get_start())], 0.4, 1.0), run_time=1.5)
            self.play(*appear(tag2), run_time=1.0)
