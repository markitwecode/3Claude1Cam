"""Chapter 2, scene 6: the serial data link (PISO -> wire -> SIPO). Clips c2.link.1 – c2.link.4.

Both chains are L8 ch2_s3's build_chain()/pin()/digit_pos(), scaled to S = 0.56 so the two sit side
by side (left: transmitter with bare RED PRE/CLR pins, D_in a DIM 0; right: receiver, DIM "?" digits).
The parallel ghost and the wire count follow L8 ch2_s3's {fewer} beat. Opens and ends empty.
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _load_l8():
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch2_s3_shiftreg.py"
    spec = importlib.util.spec_from_file_location("_l08_ch2_s3_shiftreg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8 = _load_l8()


def _p(x, y):
    return np.array([x, y, 0.0])


# ── layout ────────────────────────────────────────────────────────────────────────
S = 0.56
TX_SHIFT, RX_SHIFT = _p(-3.284, 0), _p(3.516, 0)
QY = L8.PIN_Y * L8.K * S
BOX_TOP, BOX_BOT = 0.95, -0.98
STUB_TOP = 1.55
BUS_Y = -1.2
NAME_Y = -1.75
WIRE_POS = _p(0.0, 0.0)          # y set from digit_pos below
DIG = 42


def rx_dpos(ff):
    """Digit spot inside a flip-flop box: above the clock triangle, as big as the box allows."""
    return ff.box.get_center() + 0.03 * DOWN


def dig(s, ff, color=GOLD):
    return T(s, DIG, color, weight=BOLD).move_to(rx_dpos(ff))


def side(shift, tx):
    C = L8.build_chain(fy=0)
    for f in C.ffs:
        f.remove(f.d_l, f.q_l)
    geo = [*C.ffs, *C.links]
    pins = []
    if tx:
        for f in C.ffs:
            for kind in ("PRE", "CLR"):
                w, _ = L8.pin(f, kind, length=0.6)
                pins.append((kind, w))
                geo.append(w)
    else:
        geo += [C.tail, *C.dots, *C.risers]
    VGroup(*geo).scale(S, about_point=ORIGIN).shift(shift)
    for d in C.dots:
        d.scale(1.5)
    return C, pins


def usb_icon():
    body = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.4).set_stroke(FG, 3)
    tip = Rectangle(width=0.4, height=0.28).set_stroke(FG, 3).next_to(body, LEFT, buff=0)
    holes = VGroup(*[Square(0.07).set_stroke(FG, 2) for _ in range(2)]).arrange(RIGHT, buff=0.1).move_to(tip)
    cord = Line(body.get_right(), body.get_right() + 0.4 * RIGHT).set_stroke(FG, 4)
    return VGroup(tip, holes, body, cord)


class SerialLink(NarratedScene):
    def construct(self):
        self.build()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ geometry
    def build(self):
        TX, pins = side(TX_SHIFT, True)
        RX, _ = side(RX_SHIFT, False)
        self.TX, self.RX = TX, RX
        self.tx_pos = [rx_dpos(f) for f in TX.ffs]
        self.rx_pos = [rx_dpos(f) for f in RX.ffs]
        self.wire_pos = _p(0, QY + 0.36)

        self.boxL = Rectangle(width=4.68, height=BOX_TOP - BOX_BOT).set_stroke(FG, 3).move_to(
            _p(-3.38, (BOX_TOP + BOX_BOT) / 2))
        self.boxR = Rectangle(width=5.15, height=BOX_TOP - BOX_BOT).set_stroke(FG, 3).move_to(
            _p(3.725, (BOX_TOP + BOX_BOT) / 2))

        # transmitter: pins, inner/outer D stubs, D labels
        self.pin_ws = []
        pre_tops = []
        for kind, w in pins:
            self.pin_ws.append(w)
            if kind == "PRE":
                pre_tops.append(w.get_end())
        self.d_in = [Line(p, _p(p[0], BOX_TOP)).set_stroke(BLUE, 5) for p in pre_tops]
        self.d_out = [Line(_p(p[0], BOX_TOP), _p(p[0], STUB_TOP)).set_stroke(BLUE, 5) for p in pre_tops]
        self.d_labs = [MathTex(f"D_{i}", font_size=36, color=BLUE).next_to(l.get_end(), UP, buff=0.1)
                       for i, l in enumerate(self.d_out)]
        self.in_l = T("Parallel Data Input", 30, BLUE).move_to(_p(self.boxL.get_x(), 2.45))
        self.d0 = T("0", DIG, DIM, weight=BOLD).next_to(TX.ffs[0].d_w.get_start(), LEFT, buff=0.12)

        # receiver: risers inner/outer, Q labels
        rxs = [r.get_start()[0] for r in RX.risers]
        self.q_in = [Line(_p(x, QY), _p(x, BOX_TOP)).set_stroke(GREEN, 5) for x in rxs]
        self.q_out = [Line(_p(x, BOX_TOP), _p(x, STUB_TOP)).set_stroke(GREEN, 5) for x in rxs]
        self.q_labs = [MathTex(f"Q_{i}", font_size=36, color=GREEN).next_to(l.get_end(), UP, buff=0.1)
                       for i, l in enumerate(self.q_out)]
        self.out_l = T("Parallel Data Output", 30, GREEN).move_to(_p(self.boxR.get_x(), 2.45))

        # serial wire
        self.serial = Line(TX.ffs[2].q_w.get_end(), RX.ffs[0].d_w.get_start()).set_stroke(GREEN, 5)
        self.ser_l = T("Serial\nData", 28, GREEN, line_spacing=0.8).next_to(self.serial, DOWN, buff=0.3).set_x(
            self.serial.get_x())

        # clock
        ffx = [f.box.get_x() for f in TX.ffs] + [f.box.get_x() for f in RX.ffs]
        self.bus = Line(_p(-5.6, BUS_Y), _p(ffx[-1], BUS_Y)).set_stroke(YELLOW, 5)
        self.stubs = [Line(_p(x, BUS_Y), f.box.get_bottom()).set_stroke(YELLOW, 4)
                      for x, f in zip(ffx, [*TX.ffs, *RX.ffs])]
        self.jdots = [Dot(_p(x, BUS_Y), radius=0.06, color=YELLOW) for x in ffx[:-1]]
        self.clk_l = T("CLK", 30, YELLOW).next_to(self.bus.get_start(), LEFT, buff=0.15)

        self.nameL = T("parallel in, serial out", 32).move_to(_p(self.boxL.get_x(), NAME_Y))
        self.nameR = T("serial in, parallel out", 32).move_to(_p(self.boxR.get_x(), NAME_Y))

        # small CLK trace (bottom left)
        lo, hi = -3.15, -2.65
        self.tr_l = T("CLK", 30, YELLOW).move_to(_p(-6.05, (lo + hi) / 2))
        self.tr_base = Line(_p(-5.55, lo), _p(-5.0, lo)).set_stroke(YELLOW, 4)
        self.segs = []
        for i in range(3):
            x = -5.0 + 1.25 * i
            seg = VMobject().set_points_as_corners([_p(x, lo), _p(x, hi), _p(x + 0.55, hi),
                                                    _p(x + 0.55, lo), _p(x + 1.25, lo)])
            self.segs.append(seg.set_stroke(YELLOW, 4))

    # ------------------------------------------------------------------ c2.link.1
    def clip1(self):
        TX, RX = self.TX, self.RX
        with self.say("c2.link.1") as c:
            # {link}: the slide's two boxes, parallel wires in and out
            self.play(*appear(self.boxL, self.boxR, *self.d_out, *self.d_labs, self.in_l,  # early: the slide's diagram drawn whole
                              *self.q_out, *self.q_labs, self.out_l, shift=None, lag=0.06),
                      run_time=min(2.0, c.until("tx")))
            c.wait_until("tx")
            # {tx}: the left box is the loaded PISO chain
            tx_parts = [*TX.ffs, *TX.links, *self.pin_ws, *self.d_in, self.d0]
            self.play(*appear(*tx_parts, shift=None, lag=0.03), FlashAround(self.boxL, time_width=1.5),
                      *during(appear(self.nameL), 0.4, 1.0), run_time=1.8)
            c.wait_until("wire")
            # {wire}: one serial wire
            self.play(Create(self.serial), *during(appear(self.ser_l), 0.4, 1.0), run_time=1.4)
            c.wait_until("rx")
            # {rx}: the receiver, SIPO, contents unknown
            self.rxd = [dig("?", f, DIM) for f in RX.ffs]
            self.rxv = ["?", "?", "?"]
            rx_parts = [*RX.ffs, *RX.links, RX.tail, *RX.dots, *self.q_in, *self.rxd]
            self.play(*appear(*rx_parts, shift=None, lag=0.03), FlashAround(self.boxR, time_width=1.5),
                      *during(appear(self.nameR), 0.4, 1.0), run_time=1.8)
            c.wait_until("clk")
            # {clk}: one clock into both
            self.play(Create(self.bus), *[Create(s) for s in self.stubs],
                      *during(appear(*self.jdots, self.clk_l, shift=None), 0.5, 1.0),  # early: CLK names the line drawn on "clock"
                      run_time=min(1.6, c.until(floor=0.8)))

    # ------------------------------------------------------------------ c2.link.2
    def clip2(self):
        TX, RX = self.TX, self.RX
        with self.say("c2.link.2") as c:
            # {load}: 1 1 0 enter through D_0 D_1 D_2
            flashes = [VShowPassingFlash(Line(o.get_end(), i.get_start()).set_stroke(GOLD, 8), time_width=0.8)
                       for o, i in zip(self.d_out, self.d_in)]
            self.txv = ["1", "1", "0"]
            self.txd = [dig(v, f) for v, f in zip(self.txv, TX.ffs)]
            self.play(*flashes, *during(appear(*self.txd, lag=0.2), 0.4, 1.0), run_time=1.8)
            c.wait_until("the wire already")
            # the wire carries the last flip-flop's bit
            self.wd = T("0", DIG, GOLD, weight=BOLD).move_to(self.wire_pos)
            self.play(*self.to_wire(self.wd), *appear(self.tr_l, self.tr_base, shift=None),  # early: the trace label set up for the edges
                      run_time=1.5)
            c.wait_until("e1")
            self.edge(0, 1.7)
            self.refresh(1.1)
            c.wait_until("e2")
            self.edge(1, 1.4)
            self.refresh(0.9)
            c.wait_until("e3")
            self.edge(2, 1.2)
            c.wait_until("match")
            # {match}: Q = D
            self.Dline = MathTex(r"D_0\,D_1\,D_2", "=", r"1\,1\,0", font_size=42)
            self.Dline[0].set_color(BLUE)
            self.Dline[2].set_color(GOLD)
            self.Qline = MathTex(r"Q_0\,Q_1\,Q_2", "=", r"1\,1\,0", font_size=42)
            self.Qline[0].set_color(GREEN)
            self.Qline[2].set_color(GOLD)
            self.Dline.move_to(_p(3.5, -2.6))
            self.Qline.next_to(self.Dline, DOWN, buff=0.3).align_to(self.Dline, LEFT)
            self.tick = check_mark().next_to(self.Qline, RIGHT, buff=0.35)
            self.play(*appear(self.Dline, self.Qline, lag=0.5), run_time=1.6)
            self.play(*appear(self.tick, shift=None), run_time=0.8)
            c.wait_until("far")
            # {far}: the first bit out travels furthest
            self.trail = Arrow(_p(TX.ffs[2].box.get_x(), QY), _p(RX.ffs[2].box.get_x(), QY), buff=0,
                               stroke_width=7, color=GOLD, max_tip_length_to_length_ratio=0.05).set_z_index(3)
            self.play(GrowArrow(self.trail), FlashAround(self.rxd[2], color=GOLD, time_width=1.5),
                      run_time=min(2.2, c.until(floor=1.0)))

    def edge(self, i, rt):
        r, d, w = self.rxd, self.txd, self.wd
        new0 = dig("0", self.TX.ffs[0])
        pulse = self.bus.copy().set_stroke(YELLOW, 9)
        self.play(Create(self.segs[i]), VShowPassingFlash(pulse, time_width=0.7),
                  *during([FadeOut(r[2]), FadeOut(d[2])], 0, 0.4),
                  *during([r[1].animate.move_to(self.rx_pos[2]), r[0].animate.move_to(self.rx_pos[1]),
                           w.animate.move_to(self.rx_pos[0]),
                           d[1].animate.move_to(self.tx_pos[2]), d[0].animate.move_to(self.tx_pos[1])], 0.3, 0.9),
                  *during(appear(new0, shift=0.25 * RIGHT), 0.6, 1.0), run_time=rt)
        self.rxd = [w, r[0], r[1]]
        self.rxv = [self.wv if hasattr(self, "wv") else "0", self.rxv[0], self.rxv[1]]
        self.txd = [new0, d[0], d[1]]
        self.txv = ["0", self.txv[0], self.txv[1]]
        self.wd = None

    def refresh(self, rt):
        self.wv = self.txv[2]
        self.wd = T(self.wv, DIG, GOLD, weight=BOLD).move_to(self.wire_pos)
        self.play(*self.to_wire(self.wd), run_time=rt)

    def to_wire(self, wd):
        """The last flip-flop's bit shows on the wire: a GOLD flash runs out along Q, the digit appears."""
        path = Line(self.TX.ffs[2].box.get_center() * RIGHT + QY * UP, self.serial.get_center()).set_stroke(GOLD, 8)
        return [VShowPassingFlash(path, time_width=0.8), *during(appear(wd, shift=0.2 * RIGHT), 0.45, 1.0)]

    # ------------------------------------------------------------------ c2.link.3
    def clip3(self):
        TX, RX = self.TX, self.RX
        with self.say("c2.link.3") as c:
            # {half}: rewind to after edge 2: the receiver holds 1 0 ?
            r1 = dig("0", RX.ffs[1], RED)
            r2 = dig("?", RX.ffs[2], RED)
            t2 = dig("1", TX.ffs[2])
            self.wd = T("1", DIG, GOLD, weight=BOLD).move_to(self.wire_pos)
            self.play(*during(disappear(self.trail, self.Dline, self.Qline, self.tick, self.segs[2]), 0, 0.45),
                      *recolor([self.rxd[0]], RED), *swap(self.rxd[1], r1), *swap(self.rxd[2], r2),
                      *swap(self.txd[2], t2), *during(appear(self.wd, shift=None), 0.5, 1.0), run_time=1.5)
            self.rxd = [self.rxd[0], r1, r2]
            self.txd[2] = t2
            tag1 = T("part of a word", 32, RED).move_to(_p(3.7, -2.6))
            tag2 = T("which edge completes a word?", 32).move_to(_p(3.7, -3.25))
            c.wait_until(own_word=tag1)
            self.play(*appear(tag1, tag2, lag=0.6), run_time=1.6)  # early: the question follows its premise
            c.wait_until("old")
            # {old}: the third edge completes the word again (receiver 1 1 0); the trace leaves
            r, d, w = self.rxd, self.txd, self.wd
            new0 = dig("0", TX.ffs[0])
            trace = [self.tr_l, self.tr_base, self.segs[0], self.segs[1]]
            self.play(VShowPassingFlash(self.bus.copy().set_stroke(YELLOW, 9), time_width=0.7),
                      *during([FadeOut(r[2]), FadeOut(d[2]), *disappear(*trace)], 0, 0.4),
                      *during([r[1].animate.move_to(self.rx_pos[2]).set_color(GOLD),
                               r[0].animate.move_to(self.rx_pos[1]).set_color(GOLD),
                               w.animate.move_to(self.rx_pos[0]),
                               d[1].animate.move_to(self.tx_pos[2]), d[0].animate.move_to(self.tx_pos[1])], 0.3, 0.9),
                      *during(appear(new0, shift=0.25 * RIGHT), 0.6, 1.0), run_time=1.5)
            self.rxd, self.txd, self.wd = [w, r[0], r[1]], [new0, d[0], d[1]], None
            c.wait_until("years ago")
            # the link shrinks to the bottom; a parallel ghost above
            gone = [tag1, tag2, self.in_l, self.out_l, self.nameL, self.nameR]
            link = VGroup(*[m for m in self.mobjects if isinstance(m, VMobject) and m not in gone])
            self.remove(*link)
            self.add(link)
            self.link = link
            link.generate_target()
            link.target.shift(2.0 * DOWN)
            self.play(*during(disappear(*gone), 0, 0.4), *during([MoveToTarget(link)], 0.35, 1.0),
                      run_time=1.6)
            gy = [2.7, 2.35, 2.0]
            self.gl = [Line(_p(-2.5, y), _p(2.5, y)).set_stroke(DIM, 4) for y in gy]
            self.gD = [MathTex(f"D_{i}", font_size=32, color=DIM).next_to(l.get_start(), LEFT, buff=0.12)
                       for i, l in enumerate(self.gl)]
            self.gQ = [MathTex(f"Q_{i}", font_size=32, color=DIM).next_to(l.get_end(), RIGHT, buff=0.12)
                       for i, l in enumerate(self.gl)]
            self.gc = Line(_p(-2.5, 1.65), _p(2.5, 1.65)).set_stroke(DIM, 4)
            self.gcl = T("CLK", 28, DIM).next_to(self.gc.get_start(), LEFT, buff=0.12)
            c.wait_until("one wire per bit")
            self.play(*[Create(l) for l in self.gl],
                      *during(appear(*self.gD, *self.gQ, shift=None, lag=0.1), 0.3, 1.0),  # early: the wire ends' names
                      run_time=1.5)
            self.tag8 = T("often 8 or more", 30, DIM, t2c={"8": GOLD}).next_to(self.gQ[1], RIGHT, buff=0.45)
            c.wait_until("eight or more")
            self.play(*appear(self.tag8), run_time=1.0)
            c.wait_until("another wire")
            self.play(Create(self.gc), *during(appear(self.gcl, shift=None), 0.4, 1.0), run_time=1.2)  # early: the clock wire's name
            c.wait_until("cable")
            # {cable}: the ghost thickens into a heavy bundle
            self.cab_l = T("heavy, costly cable", 32).move_to(_p(0, 3.3))
            self.play(*[l.animate.set_stroke(width=20, opacity=0.7) for l in (*self.gl, self.gc)],
                      *during(appear(self.cab_l), 0.3, 1.0), run_time=1.6)
            c.wait_until("fewer")
            # {fewer}: 3 data wires -> 1
            self.count = T("3 data wires → 1", 36, t2c={"3": GOLD, "1": GOLD}).move_to(_p(0, 0.75))
            self.play(*appear(self.count), run_time=1.2)  # early: the count sums up the sentence

    # ------------------------------------------------------------------ c2.link.4
    def clip4(self):
        with self.say("c2.link.4", gap=1.4) as c:
            # {usb}
            self.play(*disappear(*self.gl, self.gc, *self.gD, *self.gQ, self.gcl, self.tag8, self.cab_l),
                      run_time=1.0)
            usb_l = T("USB: a serial link", 36).move_to(_p(0.5, 3.25))
            icon = usb_icon().next_to(usb_l, LEFT, buff=0.4)
            c.wait_until(own_word=usb_l)
            self.play(*appear(icon, usb_l, shift=None, lag=0.2),
                      VShowPassingFlash(self.serial.copy().set_stroke(YELLOW, 9), time_width=0.8), run_time=1.3)
            c.wait_until("no separate clock")
            tag = T("no clock wire: the receiver recovers it from the data", 28).move_to(_p(0, 2.6))
            clk = [self.bus, *self.stubs, *self.jdots, self.clk_l]
            self.play(*set_alpha(clk, 0.3), *during(appear(tag), 0.3, 1.0), run_time=1.4)
            c.wait_until("bits go one")
            # {cost}: one bit at a time
            l1 = T("one bit at a time", 36).move_to(_p(0, 3.25))
            self.play(*during(disappear(icon, usb_l, tag), 0, 0.45), *during(appear(l1), 0.5, 1.0), run_time=1.4)
            l2 = T("same time per word → bits N× faster", 36, t2c={"N×": GOLD}).move_to(_p(0, 2.6))
            c.wait_until(own_word=l2)
            self.play(*appear(l2), run_time=1.0)
            l3a = T("3 bits: ×3", 36, t2c={"3": GOLD}).move_to(_p(-2.2, 1.95))
            l3b = T("a byte: ×8", 36, t2c={"×8": GOLD}).move_to(_p(2.2, 1.95))
            c.wait_until("three times")
            self.play(*appear(l3a), run_time=1.0)
            c.wait_until("eight times")
            self.play(*appear(l3b), run_time=1.0)
            c.wait_until("trade")
            # {trade}: a small balance
            by = 0.6
            beam = Line(_p(-3.2, by), _p(3.2, by)).set_stroke(FG, 4)
            fulc = Polygon(_p(0, by), _p(-0.28, by - 0.38), _p(0.28, by - 0.38)).set_stroke(FG, 3).set_fill(BG, 1)
            bl = T("much less cable", 32, GREEN).next_to(_p(-2.3, by), UP, buff=0.15)
            br = T("faster bit rate", 32, GOLD).next_to(_p(2.3, by), UP, buff=0.15)
            self.play(*during(disappear(self.count), 0, 0.4),
                      *during([GrowFromCenter(beam), FadeIn(fulc)], 0.4, 0.8),
                      *during(appear(bl, br, lag=0.3), 0.5, 1.0),  # early: both sides of the trade in one sentence
                      run_time=min(1.6, c.until(floor=1.0)))
