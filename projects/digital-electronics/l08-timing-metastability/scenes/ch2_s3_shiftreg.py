"""Chapter 2, scene 3: two flip-flops, no logic: the shift register. Clips c2.shift.1 – c2.shift.4.

Circuit: L6 ch6_s8's shift-register sketch (make_ff copied from ch1_s4_path, Q-bar dropped), at
K = 0.6. Timing rows: ch1_s5's data-sheet style (sloped edges, WAVE_W 4, thin DIM guides), copied,
single-line traces revealed left to right. PRE / CLR pins: L6 ch3_s6's RED async pins.
Last shot (opens s4): `pair_shot` state, FF0 + FF1 with the bare Q_0 wire, the rule and the
"reliable flip-flop" line.
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


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- L6's make_ff (via ch1_s4_path), Q-bar dropped, clock wire kept separate ----------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def make_ff():
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri, g.d_w, g.q_w, g.d_l, g.q_l, g.clk_w = box, tri, d_w, q_w, d_l, q_l, clk_w
    return g


# ---- the three-flip-flop chain (L6 ch6_s8 shift_register, full size) -----------------------------
K = 0.6
FF_X = (-3.6, -0.2, 3.2)
FF_Y = 1.15
HX = (BOX_W / 2 + WIRE) * K          # box centre to the end of a pin wire (0.96)


def build_chain(fy=FF_Y, clk_right=False):
    C = VGroup()
    C.ffs = []
    for x in FF_X:
        f = make_ff()
        f.scale(K, about_point=ORIGIN).shift(_p(x, fy))
        f.clk_w.scale(K, about_point=ORIGIN).shift(_p(x, fy))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.3, about_point=lb.get_center())
        C.ffs.append(f)
    qy = fy + PIN_Y * K
    C.qy = qy
    C.links = [Line(_p(FF_X[i] + HX, qy), _p(FF_X[i + 1] - HX, qy)).set_stroke(GREEN, 5) for i in range(2)]
    C.tail = Line(_p(FF_X[2] + HX, qy), _p(FF_X[2] + HX + 0.45, qy)).set_stroke(GREEN, 5)
    rx = [(FF_X[0] + FF_X[1]) / 2, (FF_X[1] + FF_X[2]) / 2, FF_X[2] + HX + 0.45]
    top = fy + BOX_H / 2 * K + 0.22
    C.risers = [Line(_p(x, qy), _p(x, top)).set_stroke(GREEN, 5) for x in rx]
    C.dots = [Dot(_p(x, qy), radius=0.07, color=GREEN) for x in rx[:2]]
    C.qls = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x, top), UP, buff=0.1)
             for i, x in enumerate(rx)]
    C.names = [T(f"FF{i}", 32).next_to(f.box, UP, buff=0.15) for i, f in enumerate(C.ffs)]
    C.din = MathTex("D_{in}", font_size=40, color=BLUE).next_to(C.ffs[0].d_w.get_start(), LEFT, buff=0.12)
    by = fy - (BOX_H / 2 + EN_WIRE) * K
    C.by = by
    C.bus = Line(_p(FF_X[0] - 1.2, by), _p(FF_X[2], by)).set_stroke(YELLOW, 5)
    C.jdots = [Dot(_p(x, by), radius=0.07, color=YELLOW) for x in FF_X[:2]]
    C.clk_ws = [f.clk_w for f in C.ffs]
    if clk_right:   # clips 1-3: the label sits at the bus's right end, clear of the timing rows
        C.clk_l = T("CLK", 32, YELLOW).next_to(C.bus.get_end(), RIGHT, buff=0.2)
    else:
        C.clk_l = T("CLK", 32, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.15)
    C.all = [*C.ffs, *C.names, *C.links, C.tail, *C.risers, *C.dots, *C.qls, C.din,
             C.bus, *C.jdots, *C.clk_ws, C.clk_l]
    return C


def digit_pos(ff):
    b = ff.box
    return b.get_center() + DOWN * 0.19 * b.height


def digit(s, ff, color=GOLD):
    return T(s, 40, color).move_to(digit_pos(ff))


# ---- ch1_s5's data-sheet traces (copied), single-line rows revealed left to right ----------------
WAVE_W = 4
GUIDE_W = 1.5
ROW_H = 0.32
SLOPE = 0.25
X0, X1 = -4.6, 6.3
RISES = [-3.8, -1.8, 0.2, 2.2, 4.2]
FALLS = [r + 1.0 for r in RISES]
LAB_X = -5.7
ROWS = {"CLK": -1.15, "D_in": -1.67, "Q_0": -2.19, "Q_1": -2.71, "Q_2": -3.23}


def wave(y, edges, color, h=ROW_H, slope=SLOPE):
    lo, hi = y - h / 2, y + h / 2
    level = lo
    pts = [_p(X0, level)]
    for xc in edges:
        other = hi if level == lo else lo
        pts += [_p(xc - slope / 2, level), _p(xc + slope / 2, other)]
        level = other
    pts.append(_p(X1, level))
    m = VMobject().set_points_as_corners(pts).set_stroke(color, WAVE_W)
    m.corners = pts
    return m


def cut(m, X):
    pts = m.corners
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        if b[0] <= X:
            out.append(b)
        else:
            if X > a[0]:
                t = (X - a[0]) / (b[0] - a[0])
                out.append(a + t * (b - a))
            break
    if len(out) < 2:
        out.append(out[0] + 0.001 * RIGHT)
    m.set_points_as_corners(out)
    return m


def reveal(m, xa, xb):
    return UpdateFromAlphaFunc(m, lambda mob, a: cut(mob, xa + (xb - xa) * a), rate_func=linear)


def guide(x, y_top, y_bot):
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


# ---- L6 ch3_s6's async pins ----------------------------------------------------------------------
def pin(ff, kind, length=0.35):
    c, hb = ff.box.get_center(), ff.box.height / 2
    if kind == "PRE":
        a = c + hb * UP
        b = a + length * UP
        w = Line(a, b).set_stroke(RED, 5)
        lab = T("PRE", 28, RED).next_to(b, UP, buff=0.08)
    else:
        a = c + 0.33 * RIGHT + hb * DOWN
        b = a + length * DOWN
        w = Line(a, b).set_stroke(RED, 5)
        lab = T("CLR", 28, RED).next_to(b, RIGHT, buff=0.08)
    return w, lab


# ---- the two-box view (last shot, opens s4) ------------------------------------------------------
PAIR_S = 1.4
PAIR_A = _p((FF_X[0] + FF_X[1]) / 2, FF_Y)
PAIR_B = _p(0, 1.05)


def to_pair(p):
    return (p - PAIR_A) * PAIR_S + PAIR_B


RULE_Y = -1.95
REL_Y = -3.0
COLS = {"t_{pc}": PINK, "t_{pd}": PURPLE, "t_{hold}": GOLD}


class ShiftRegister(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.shift.1
    def clip1(self):
        C = build_chain(clk_right=True)
        self.C = C
        with self.say("c2.shift.1") as c:
            # {chain}: three bare flip-flops, no logic between them
            self.play(*appear(*C.ffs, shift=None, lag=0.3), run_time=min(1.6, c.until("shiftreg")))
            c.wait_until("shiftreg")
            # {shiftreg}
            self.play(*appear(*C.names, lag=0.25), run_time=1.2)  # early: the three names, read as one
            c.wait_until("wires")
            # {wires}: Q straight into the next D, taps up to the outputs
            self.play(*[Create(m) for m in (*C.links, C.tail, *C.risers)],
                      *appear(*C.dots, shift=None), run_time=1.4)
            self.play(*appear(*C.qls, lag=0.2), run_time=1.0)  # early: output labels, shown together
            c.wait_until("clk")
            # {clk}: one clock line into all three triangles
            self.play(*during([Create(C.bus)], 0, 0.55),
                      *during([Create(w) for w in C.clk_ws], 0.5, 1.0),
                      *during(appear(*C.jdots, C.clk_l, shift=None), 0.5, 1.0), run_time=1.8)
            c.wait_until("din")
            # {din}
            fl = C.ffs[0].d_w.copy().set_stroke(YELLOW, 8)
            self.play(*appear(C.din), VShowPassingFlash(fl, time_width=0.6), run_time=1.2)
            c.wait_until("move")
            # {move}: the clock row of the diagram, then the data's direction
            self.clk_w = wave(ROWS["CLK"], sorted(RISES + FALLS), YELLOW)
            cut(self.clk_w, X0)
            self.row_labs = [T("CLK", 32, YELLOW).move_to(_p(LAB_X, ROWS["CLK"]))] + [
                MathTex({"D_in": "D_{in}"}.get(k, k), font_size=36,
                        color=BLUE if k == "D_in" else GREEN).move_to(_p(LAB_X, ROWS[k]))
                for k in ("D_in", "Q_0", "Q_1", "Q_2")]
            self.guides = [guide(x, ROWS["CLK"] + 0.24, ROWS["Q_2"] - 0.26) for x in RISES]
            self.play(*appear(*self.row_labs, shift=None, lag=0.1), reveal(self.clk_w, X0, X1),  # early: the diagram's rows, laid out whole
                      *during([Create(g) for g in self.guides], 0.3, 1.0), run_time=2.4)
            c.wait_until("so the data")
            ay = -0.62
            self.mv_arrow = Arrow(_p(-2.6, ay), _p(-1.2, ay), buff=0, stroke_width=5, color=BLUE,
                                  tip_length=0.22)
            self.mv_lab = T("one place per edge", 30, BLUE).next_to(self.mv_arrow, RIGHT, buff=0.2)
            self.play(GrowArrow(self.mv_arrow), *during(appear(self.mv_lab, shift=None), 0.3, 1.0),
                      run_time=1.4)

    # ------------------------------------------------------------------ c2.shift.2
    def clip2(self):
        C = self.C
        din_w = wave(ROWS["D_in"], [-2.5, -1.1], BLUE)
        qw = [wave(ROWS["Q_0"], [-1.8, 0.2], GREEN), wave(ROWS["Q_1"], [0.2, 2.2], GREEN),
              wave(ROWS["Q_2"], [2.2, 4.2], GREEN)]
        for m in (din_w, *qw):
            cut(m, X0)
        self.din_w, self.qw = din_w, qw
        with self.say("c2.shift.2") as c:
            # {one}: a single pulse on D_in, around edge 2
            f = (-2.3 - X0) / (X1 - X0)
            self.play(reveal(din_w, X0, X1), *during([reveal(m, X0, -2.3) for m in qw], 0, f),
                      run_time=min(2.0, c.until("catch")))
            c.wait_until("catch")
            # {catch}: edge 2, Q_0 steps up, a 1 in FF0
            one = digit("1", C.ffs[0])
            self.play(*[reveal(m, -2.3, -1.0) for m in qw],
                      *during(appear(one, shift=0.3 * RIGHT), 0.35, 0.9), run_time=1.8)
            c.wait_until("move1")
            # {move1}: edge 3, the 1 hops to FF1
            self.play(*[reveal(m, -1.0, 1.0) for m in qw],
                      *during([one.animate.move_to(digit_pos(C.ffs[1]))], 0.4, 1.0), run_time=1.4)
            c.wait_until("move2")
            # {move2}: edge 4, to FF2; then edge 5 sends it out
            self.play(*[reveal(m, 1.0, 3.0) for m in qw],
                      *during([one.animate.move_to(digit_pos(C.ffs[2]))], 0.4, 1.0), run_time=1.1)
            self.play(*[reveal(m, 3.0, X1) for m in qw],
                      *during([FadeOut(one, shift=1.5 * RIGHT)], 0.25, 0.75), run_time=1.0)
            c.wait_until("sipo")
            # {sipo}: brace over the outputs
            self.brace = Brace(VGroup(*C.qls), UP, buff=0.08, color=DIM)
            self.sipo = T("serial in, parallel out", 34).next_to(self.brace, UP, buff=0.08)
            self.play(GrowFromCenter(self.brace), *flash([self.row_labs[1]], color=BLUE), run_time=1.2)
            c.wait_until(own_word=self.sipo)
            self.play(*appear(self.sipo))

    # ------------------------------------------------------------------ c2.shift.3
    def clip3(self):
        C = self.C
        with self.say("c2.shift.3") as c:
            # {piso}: the diagram clears, the circuit drops to the centre
            keep = [p for p in C.all if p not in C.names] + [self.brace, self.sipo]
            clk_home = C.clk_l.copy().next_to(C.bus.get_start() + DOWN, LEFT, buff=0.15)
            sweep_clear(self, *[m.animate.shift(DOWN) for m in keep if m is not C.clk_l],
                        C.clk_l.animate.move_to(clk_home), keep=keep,
                        run_time=min(1.6, c.until("load") - 0.7))
            pins = [pin(f, k) for f in C.ffs for k in ("PRE", "CLR")]
            self.play(*[GrowFromEdge(w, DOWN if w.get_start()[1] < w.get_end()[1] else UP) for w, _ in pins],
                      *during(appear(*[lab for _, lab in pins], shift=None), 0.3, 1.0),  # early: the async pins, named before the voice
                      run_time=min(1.0, c.until("load", floor=0.5)))
            c.wait_until("load")
            # {load}: 1 0 1 at once
            digs = [digit(s, f) for s, f in zip("101", C.ffs)]
            self.play(*flash([w for w, _ in pins], color=YELLOW), *appear(*digs, shift=None, lag=0), run_time=1.2)
            c.wait_until("preset")
            self.play(*flash([pins[0][0], pins[4][0]]), *recolor([pins[0][1], pins[4][1]], YELLOW), run_time=1.0)
            c.wait_until("clear inputs")
            self.play(*flash([pins[3][0]]), *recolor([pins[3][1]], YELLOW),
                      *recolor([pins[0][1], pins[4][1]], RED), run_time=1.0)
            self.play(*recolor([pins[3][1]], RED), run_time=0.5)
            c.wait_until("out")
            # {out}: D_in held at 0, three edges shift the bits out of FF2
            din0 = MathTex(r"D_{in} = 0", font_size=40, color=BLUE)
            din0.align_to(C.din, RIGHT).set_y(C.din.get_y())
            qslot = [_p(C.tail.get_end()[0] + 0.5 + 0.45 * i, C.tail.get_end()[1]) for i in range(3)]
            self.play(*edit(C.din, din0), *set_alpha([C.ffs[0].d_w], 0.4), run_time=0.9)
            C.din = din0
            queue = []
            for i, rt in enumerate((1.4, 1.0, 0.9)):
                pulse = C.bus.copy().set_stroke(YELLOW, 9)
                d0, d1, d2 = digs
                new0 = digit("0", C.ffs[0])
                self.play(VShowPassingFlash(pulse, time_width=0.7),
                          *during([d2.animate.move_to(qslot[0]), *[q.animate.shift(0.45 * RIGHT) for q in queue], d1.animate.move_to(digit_pos(C.ffs[2])),
                                   d0.animate.move_to(digit_pos(C.ffs[1]))], 0.15, 0.6),
                          *during(appear(new0, shift=0.25 * RIGHT), 0.65, 1.0), run_time=rt)
                queue.append(d2)
                digs = [new0, d0, d1]
            c.wait_until("that's parallel in")
            self.piso = T("parallel in, serial out", 40).move_to(_p(0, -2.4))
            self.play(*appear(self.piso))
            c.wait_until("link")
            # {link}: the serial data link
            L = self.link_parts()
            self.clear_all(*during(appear(*L["core"], shift=None, lag=0.1), 0.5, 1.0),  # early: the link drawn whole as the voice names it
                           run_time=min(2.0, c.until("fewer", floor=1.0)))
            c.wait_until("fewer")
            # {fewer}: the parallel ghost above, and the count
            self.play(*appear(*L["ghost"], shift=None, lag=0.15), *during(appear(L["count"]), 0.4, 1.0),  # early: the count sums up the sentence
                      run_time=1.4)

    def clear_all(self, *incoming, run_time):
        """The whole picture fades as one, all pieces together, before incoming arrives."""
        self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45), *incoming, run_time=run_time)

    def link_parts(self):
        by, bw, bh = -0.7, 3.2, 1.5
        lx, rx = -3.6, 3.6
        boxes, labs = [], []
        for x, a, b in ((lx, "Parallel in,", "serial out"), (rx, "Serial in,", "parallel out")):
            boxes.append(Rectangle(width=bw, height=bh).set_stroke(FG, 4).move_to(_p(x, by)))
            labs.append(VGroup(T(a, 32), T(b, 32)).arrange(DOWN, buff=0.1).move_to(_p(x, by)))
        top = by + bh / 2
        ins = [Line(_p(lx + dx, top), _p(lx + dx, top + 0.85)).set_stroke(BLUE, 5) for dx in (-0.8, 0, 0.8)]
        outs = [Line(_p(rx + dx, top), _p(rx + dx, top + 0.85)).set_stroke(GREEN, 5) for dx in (-0.8, 0, 0.8)]
        in_l = T("Parallel Data Input", 30, BLUE).next_to(_p(lx, top + 0.85), UP, buff=0.15)
        out_l = T("Parallel Data Output", 30, GREEN).next_to(_p(rx, top + 0.85), UP, buff=0.15)
        ser = Line(_p(lx + bw / 2, by), _p(rx - bw / 2, by)).set_stroke(GREEN, 5)
        ser_l = T("Serial Data", 30, GREEN).next_to(ser, UP, buff=0.15)
        cy = by - bh / 2 - 0.7
        clk = Line(_p(lx - 2.0, cy), _p(rx, cy)).set_stroke(YELLOW, 5)
        brs = [Line(_p(x, cy), _p(x, by - bh / 2)).set_stroke(YELLOW, 5) for x in (lx, rx)]
        jd = Dot(_p(lx, cy), radius=0.07, color=YELLOW)
        clk_l = T("CLK", 32, YELLOW).next_to(clk.get_start(), LEFT, buff=0.15)
        gy = 2.25
        ghost = [Line(_p(-1.4, gy + dy), _p(1.4, gy + dy)).set_stroke(DIM, 4) for dy in (-0.25, 0, 0.25)]
        count = T("3 wires → 1", 36, t2c={"3": GOLD, "1": GOLD}).move_to(_p(0, 3.05))
        return {"core": [boxes[0], labs[0], *ins, in_l, ser, ser_l, boxes[1], labs[1], *outs, out_l,
                         clk, *brs, jd, clk_l],
                "ghost": ghost, "count": count}

    # ------------------------------------------------------------------ c2.shift.4
    def clip4(self):
        with self.say("c2.shift.4") as c:
            # {hold}: back to the chain
            C = build_chain()
            self.C = C
            parts = [p for p in C.all]
            self.clear_all(*during(appear(*parts, shift=None, lag=0.02), 0.5, 1.0), run_time=1.4)  # early: the chain returns whole
            c.wait_until("two flip-flops")
            # the view narrows to FF0 and FF1
            short_bus = Line(C.bus.get_start(), _p(FF_X[1], C.by)).set_stroke(YELLOW, 5)
            gone = [C.ffs[2], C.names[2], C.links[1], C.tail, *C.risers, *C.dots, C.qls[1], C.qls[2],
                    C.din, C.jdots[1], C.clk_ws[2]]
            self.play(*disappear(*gone), Transform(C.bus, short_bus), run_time=1.0)
            pair = [C.ffs[0], C.ffs[1], C.names[0], C.names[1], C.links[0], C.clk_ws[0], C.clk_ws[1],
                    C.bus, C.jdots[0], C.clk_l]
            pin_y = to_pair(_p(0, C.qy))[1]
            q0_target = _p(-1.3, pin_y + 0.42)
            self.play(*[m.animate.scale(PAIR_S, about_point=PAIR_A).shift(PAIR_B - PAIR_A) for m in pair],
                      C.qls[0].animate.scale(1.15).move_to(q0_target), run_time=1.6)
            wire = C.links[0]
            ff0, ff1 = C.ffs[0], C.ffs[1]
            c.wait_until("zero")
            # {zero}: s2's CL box, as a ghost, squeezes to nothing
            cl = Rectangle(width=1.4, height=1.0).set_stroke(BLUE, 3, opacity=0.5).set_fill(BG, 1)
            cl.move_to(_p(0.15, pin_y))
            cl_l = T("CL", 32, BLUE).set_opacity(0.5).move_to(cl)
            self.play(*appear(cl, cl_l, shift=None, lag=0.2), run_time=1.0)
            c.wait_until("the logic's delay")
            self.play(*during(disappear(cl_l), 0, 0.35),
                      cl.animate.stretch(0.02, 0).set_stroke(opacity=0), run_time=1.4)
            self.remove(cl)
            tpd0 = MathTex(r"t_{pd} = 0", font_size=44, color=PURPLE).move_to(_p(0.15, pin_y - 0.6))
            long = MathTex("(", "t_{pc}", "+", "t_{pd}", r")_{\min} \geq", "t_{hold}", font_size=56)
            short = MathTex("(", "t_{pc}", r")_{\min} \geq", "t_{hold}", font_size=56)
            for m in (long, short):
                for part in m:
                    part.set_color(COLS.get(part.tex_string, FG))
                m.move_to(_p(0, RULE_Y))
            c.wait_until("is zero")
            self.play(*appear(tpd0), *during(appear(long, shift=None), 0.35, 1.0), run_time=1.4)  # early: s2's rule returns with the zero
            c.wait_until("rule")
            # {rule}: the hold rule shrinks
            c.wait_until("shrinks")
            assert len(long) == 6 and len(short) == 4
            self.play(*during([FadeOut(long[2]), FadeOut(long[3])], 0, 0.35),
                      *during([long[i].animate.move_to(short[j]) for i, j in ((0, 0), (1, 1), (4, 2), (5, 3))],
                              0.05, 1.0),
                      *flash([tpd0], color=PURPLE), run_time=min(1.4, c.until("the shortest")))
            self.remove(*long.get_family())
            self.add(short)
            c.wait_until("the shortest")
            self.play(FlashAround(short.get_part_by_tex("t_{pc}"), color=PINK), run_time=1.2)
            c.wait_until("hold time")
            self.play(FlashAround(short.get_part_by_tex("t_{hold}"), color=GOLD), run_time=1.2)
            c.wait_until("same")
            # {same}: one clock edge reaches both boxes at once; Q_0 flickers as FF1 reads it
            s = C.bus.get_start()
            paths = [VMobject().set_points_as_corners([s, w.get_start(), w.get_end()]).set_stroke(YELLOW, 10)
                     for w in (C.clk_ws[0], C.clk_ws[1])]

            def flicker(m, a):
                m.set_stroke(interpolate_color(ManimColor(GREEN), ManimColor(YELLOW),
                                               abs(np.sin(3 * PI * a))))

            self.play(*[VShowPassingFlash(p, time_width=0.5) for p in paths],
                      *during([UpdateFromAlphaFunc(wire, flicker)], 0.55, 1.0), run_time=2.2)
            wire.set_stroke(GREEN)
            c.wait_until("skip")
            # {skip}: a DIM what-if: a longer hold window, and a 1 that jumps two places
            dx0, dx1 = ff1.d_w.get_start()[0], ff1.box.get_left()[0]
            win = Rectangle(width=dx1 - dx0, height=0.6).set_stroke(GOLD, 2).set_fill(GOLD, 0.25)
            win.move_to(_p((dx0 + dx1) / 2, pin_y)).set_z_index(-1)
            wide = Rectangle(width=dx1 - (-0.45), height=0.6).set_stroke(GOLD, 2).set_fill(GOLD, 0.25)
            wide.move_to(_p((dx1 - 0.45) / 2, pin_y)).set_z_index(-1)
            self.play(FadeIn(win), run_time=0.7)
            self.play(Transform(win, wide), run_time=1.0)
            src = T("1", 40, DIM).next_to(ff0.d_w.get_start(), LEFT, buff=0.15)
            ghost1 = T("1", 40, DIM).move_to(digit_pos(ff1))
            jump = ArcBetweenPoints(src.get_top() + 0.1 * UP, _p(ff1.box.get_left()[0] + 0.3, ff1.box.get_top()[1] + 0.05),
                                    angle=-1.8).set_stroke(DIM, 4)
            tip = Arrow(jump.point_from_proportion(0.97), jump.get_end(), buff=0, stroke_width=4,
                        color=DIM, tip_length=0.2, max_tip_length_to_length_ratio=1.0)
            self.play(*appear(src, shift=None), Create(jump), *during([GrowArrow(tip)], 0.7, 1.0),
                      *during(appear(ghost1, shift=None), 0.6, 1.0), run_time=1.3)
            x = cross_mark(RED).scale(1.2).move_to(jump.point_from_proportion(0.8))   # on the landing in FF1
            self.play(GrowFromCenter(x), run_time=0.6)
            c.wait_until("reliable")
            # {reliable}: the conclusion under the rule
            rel = VGroup(T("a reliable flip-flop:", 36),
                         MathTex(r"t_{hold}", font_size=44, color=GOLD),
                         T("shorter than its own", 36),
                         MathTex(r"(t_{pc})_{\min}", font_size=44, tex_to_color_map={"t_{pc}": PINK}))
            rel.arrange(RIGHT, buff=0.2).move_to(_p(0, REL_Y))
            self.play(*disappear(win, src, ghost1, jump, tip, x, tpd0), run_time=0.8)
            self.play(*appear(rel), run_time=1.0)
