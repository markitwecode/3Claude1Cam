"""Chapter 6, scene 7: recap and next. Clips c6.recap.1 – c6.recap.3."""
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


DIM_W = 3
TASK_COLORS = {1: BLUE, 2: GREEN, 3: TEAL, 4: FG}

# grid: three tiles on top, two wider ones below; captions (two lines, T 28) under each
TOP_C = [_p(-4.6, 2.2), _p(0, 2.2), _p(4.6, 2.2)]
BOT_C = [_p(-3.4, -1.13), _p(3.4, -1.13)]
CAP_TOP = (0.6, 0.2)
CAP_BOT = (-2.83, -3.23)


def dim_arrow(xa, xb, y, color, tex, size=30, label_dir=UP):
    arr = DoubleArrow(_p(xa, y), _p(xb, y), buff=0, stroke_width=DIM_W, tip_length=0.13,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.1)
    return VGroup(arr, lab)


def caption(text, x, y):
    return T(text, 28).move_to(_p(x, y))


def task_sq(n, side=0.28):
    return RoundedRectangle(width=side, height=side, corner_radius=0.06).set_stroke(width=0) \
        .set_fill(TASK_COLORS[n], 0.85)


# ---- s2's stopwatch (ch6_s2_speed.make_stopwatch), scaled -----------------------------------
def make_stopwatch(center, k=0.7):
    face = Circle(radius=0.3).set_stroke(FG, 3).set_fill(BG, 1)
    stem = Line(face.get_top(), face.get_top() + 0.1 * UP).set_stroke(FG, 3)
    crown = RoundedRectangle(width=0.18, height=0.08, corner_radius=0.03).set_stroke(FG, 2) \
        .set_fill(FG, 1).next_to(stem, UP, buff=0)
    th = TAU * 0.85
    hand = Line(ORIGIN, 0.22 * np.array([np.sin(th), np.cos(th), 0])).set_stroke(GOLD, 3)
    w = VGroup(face, stem, crown, hand)
    w.scale(k, about_point=ORIGIN).shift(np.array(center))
    return w


# ---- s4/s5 timeline pieces, at tile scale ----------------------------------------------------
def stage_rect(task, x_left, y, w, h):
    col = TASK_COLORS[task]
    return Rectangle(width=w, height=h).set_stroke(col, 3).set_fill(col, 0.18).move_to(_p(x_left + w / 2, y))


def hatch(x_left, y, width, height, spacing=0.13, color=DIM):
    x0, x1 = x_left, x_left + width
    y0 = y - height / 2
    lines = VGroup()
    k = x0 - height + spacing / 2
    while k < x1:
        xa, xb = max(x0, k), min(x1, k + height)
        if xb - xa > 0.02:
            lines.add(Line([xa, y0 + xa - k, 0], [xb, y0 + xb - k, 0]).set_stroke(color, 2, 0.6))
        k += spacing
    outline = Rectangle(width=width, height=height).set_stroke(color, 2).move_to(_p(x0 + width / 2, y))
    return VGroup(outline, lines)


# ---- s6's flip-flop / pipelined path (ch6_s6_registers), unlabelled --------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
K = 0.75
RX = (-5.0, 0.0, 5.0)
HX = (BOX_W / 2 + WIRE) * K
BLK_H = 1.3
BUS_DY = -(BOX_H / 2 + EN_WIRE) * K
BUS_X0 = -5.6


def make_reg(x, fy):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4).set_fill(BG, 1)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    br = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    g = VGroup(d_w, q_w, qb_w, br, box, tri)
    g.scale(K, about_point=ORIGIN).shift(_p(x, fy))
    gh = []
    for k in (2, 1):
        r = Rectangle(width=BOX_W * K, height=BOX_H * K).set_stroke(DIM, 3).set_fill(BG, 1)
        r.move_to(box.get_center() + 0.1 * k * (UP + RIGHT))
        gh.append(r)
    return VGroup(*gh, g)


def pipe_native(fy=0.3):
    """Registers at x -5/0/5 on one YELLOW CLK line, stage blocks between (native scale)."""
    pin = fy + PIN_Y * K
    regs = [make_reg(x, fy) for x in RX]
    a, b = RX[0] + HX, RX[2] - HX
    m0, m1 = RX[1] - HX, RX[1] + HX

    def block(x0, x1):
        return Rectangle(width=x1 - x0, height=BLK_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(
            _p((x0 + x1) / 2, pin))
    b1, b2 = block(a, m0), block(m1, b)
    by = fy + BUS_DY
    bus = Line(_p(BUS_X0, by), _p(RX[2], by)).set_stroke(YELLOW, 5)
    dots = [Dot(_p(x, by), radius=0.08, color=YELLOW) for x in RX[:2]]
    return VGroup(*regs, b1, b2, bus, *dots), regs, b1, b2, bus


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)                                                     # end card; music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ r1, r2, r3
    def clip1(self):
        with self.say("c6.recap.1") as c:
            # ---- r1: s2's system box, stopwatch and exit tally
            cx, cy = TOP_C[0][:2]
            box = RoundedRectangle(width=2.6, height=0.95, corner_radius=0.15).set_stroke(FG, 3) \
                .move_to(_p(cx, cy + 0.62))
            ten = dim_arrow(cx - 1.0, cx + 1.0, cy + 0.45, GOLD, r"10\,\mathrm{ns}", size=30)
            watch = make_stopwatch(_p(cx - 1.1, cy - 0.3))
            lat = T("latency", 28, YELLOW).move_to(_p(cx - 1.1, cy - 0.85))
            marks = [Line(_p(cx + 0.92 + 0.18 * i, cy - 0.5), _p(cx + 0.92 + 0.18 * i, cy - 0.1))
                     .set_stroke(GOLD, 4) for i in range(3)]
            thr = T("throughput", 28, YELLOW).move_to(_p(cx + 1.1, cy - 0.85))
            cap1a = caption("how long for one", cx, CAP_TOP[0])
            cap1b = caption("how many per second", cx, CAP_TOP[1])

            c.wait_until("r1")
            self.play(FadeIn(box), *appear(ten, watch, lat, shift=None, lag=0.2), run_time=1.3)
            c.wait_until("takes", own_word=cap1a)
            self.play(*appear(cap1a, shift=None), run_time=1.0)
            c.wait_until("Throughput")
            self.play(*[FadeIn(m, shift=0.1 * DOWN) for m in marks], *appear(thr, shift=None), run_time=1.0)
            c.wait_until("per second", own_word=cap1b)
            self.play(*appear(cap1b, shift=None), run_time=1.0)

            # ---- r2: s3's spatial copies and the box split into stages
            cx, cy = TOP_C[1][:2]
            copies = [RoundedRectangle(width=1.7, height=0.62, corner_radius=0.12).set_stroke(FG, 3)
                      .move_to(_p(cx - 1.05, cy + y)) for y in (0.42, -0.4)]
            csq = [task_sq(1).move_to(copies[0]), task_sq(2).move_to(copies[1])]
            halves = [Rectangle(width=0.9, height=1.45).set_stroke(BLUE, 3).move_to(_p(cx + x, cy + 0.01))
                      for x in (0.65, 1.55)]
            nums = [T(str(k + 1), 30, BLUE).move_to(h) for k, h in enumerate(halves)]
            cap2a = caption("spatial: copies", cx, CAP_TOP[0])
            cap2b = caption("temporal: stages", cx, CAP_TOP[1])

            c.wait_until("r2")
            self.play(FadeIn(copies[0]), TransformFromCopy(copies[0], copies[1]),
                      *[FadeIn(s, scale=0.6) for s in csq], run_time=1.4)
            self.play(*appear(cap2a, shift=None), run_time=1.0)
            c.wait_until("Temporal")
            self.play(*[FadeIn(h) for h in halves], *appear(*nums, shift=None, lag=0.3), run_time=1.3)
            c.wait_until("into stages", own_word=cap2b)
            self.play(*appear(cap2b, shift=None), run_time=1.0)

            # ---- r3: s4's two lanes with idle hatching
            cx, cy = TOP_C[2][:2]
            P = 3.4 * 0.39
            w, h = P / 2, 0.35
            x0 = cx - 1.5 * P
            l1, l2 = cy + 0.25, cy - 0.6

            def slot(p, s):
                return x0 + p * P + s * w
            boxes = [stage_rect(1, slot(0, 0), l1, w, h), stage_rect(1, slot(0, 1), l2, w, h),
                     stage_rect(2, slot(1, 0), l1, w, h), stage_rect(2, slot(1, 1), l2, w, h),
                     stage_rect(3, slot(2, 0), l1, w, h)]
            tcs = [dim_arrow(x0 + i * P + 0.04, x0 + (i + 1) * P - 0.04, cy + 0.72, YELLOW, "T_c", size=28)
                   for i in range(3)]
            h1 = [hatch(slot(p, 1), l1, w, h) for p in range(3)]
            h2 = [hatch(slot(p, 0), l2, w, h) for p in range(3)]
            idle1 = set_backstroke(T("idle", 28), width=7).move_to(h1[0])
            idle2 = set_backstroke(T("idle", 28), width=7).move_to(h2[0])
            cap3a = caption("one task per period,", cx, CAP_TOP[0])
            cap3b = caption("stages idle", cx, CAP_TOP[1])

            c.wait_until("r3")
            self.play(*appear(*tcs, shift=None, lag=0.15),
                      *[FadeIn(b) for b in boxes], run_time=1.4)
            c.wait_until("fills", own_word=cap3a)
            self.play(*appear(cap3a, shift=None), run_time=1.0)
            c.wait_until("and each stage's")
            self.play(*appear(*h1, *h2, shift=None, lag=0.1),
                      *during(appear(idle1, idle2, cap3b, shift=None), 0.5, 1.0),
                      run_time=min(1.4, c.until(floor=0.5)))

    # ------------------------------------------------------------------ r4, r5
    def clip2(self):
        with self.say("c6.recap.2", gap=1.9) as c:
            # ---- r4: s5's staircase, its latency brace and the one-stage T_c arrow
            cx, cy = BOT_C[0][:2]
            s = 0.4
            w, h, pitch = 1.7 * s, 0.9 * s, 1.3 * s
            x0, top = cx - 2.9, cy + 0.62
            A = [stage_rect(r + 1, x0 + r * w, top - r * pitch, w, h) for r in range(4)]
            B = [stage_rect(r + 1, x0 + (r + 1) * w, top - r * pitch, w, h) for r in range(4)]
            brace = span_brace(_p(x0 + 3 * w, top - 3 * pitch - h / 2), _p(x0 + 5 * w, top - 3 * pitch - h / 2),
                               DOWN, color=GOLD, buff=0.08)
            latx = MathTex(r"\text{Latency}", "=", "2", "T_c", font_size=34)
            latx[2].set_color(GOLD)
            latx[3].set_color(YELLOW)
            latx.next_to(brace, RIGHT, buff=0.3).shift(0.1 * UP)
            tc = dim_arrow(x0 + 3 * w + 0.03, x0 + 4 * w - 0.03, top, YELLOW, "T_c", size=30)
            cap4a = caption("2 periods, each", cx, CAP_BOT[0])
            cap4b = caption("about half as long", cx, CAP_BOT[1])

            self.play(*[FadeIn(m) for pair in zip(A, B) for m in pair], run_time=1.5)
            c.wait_until("latency")
            self.play(GrowFromCenter(brace), *during(appear(latx, shift=None), 0.4, 1.0), run_time=1.5)
            c.wait_until("but each", own_word=cap4a)
            self.play(*appear(cap4a, shift=None), run_time=1.0)
            c.wait_until("about", own_word=cap4b)
            self.play(FadeIn(tc[0]), *appear(tc[1], cap4b, shift=None), run_time=1.0)

            # ---- r5: s6's registers between the stages on one CLK line
            cx, cy = BOT_C[1][:2]
            k = 0.42
            g, regs, b1, b2, bus = pipe_native()
            g.scale(k, about_point=_p(0.3, 0.3)).shift(_p(cx - 0.3 + 0.25, cy - 0.3 - 0.05))
            reg_l = [T("register", 28).next_to(r, UP, buff=0.12) for r in regs]
            for lb in reg_l:
                lb.set_y(reg_l[0].get_y())
            st_y = (b1.get_bottom()[1] + bus.get_y()) / 2
            st_l = [T("stage 1", 28, BLUE).move_to(_p(b1.get_x(), st_y)),
                    T("stage 2", 28, BLUE).move_to(_p(b2.get_x(), st_y))]
            clk = T("CLK", 28, YELLOW).next_to(bus.get_start(), LEFT, buff=0.12)
            toks = [task_sq(2, 0.26).move_to(b1), task_sq(1, 0.26).move_to(b2)]
            cap5a = caption("registers keep", cx, CAP_BOT[0])
            cap5b = caption("tokens apart", cx, CAP_BOT[1])

            c.wait_until("r5")
            self.play(FadeIn(g), *appear(*reg_l, st_l[0], st_l[1], clk, cap5a, shift=None, lag=0.1), run_time=1.4)  # early: the diagram's labels come with it, on "registers"
            self.play(*[FadeIn(t, scale=0.6) for t in toks], *appear(cap5b, shift=None), run_time=1.0)

    # ------------------------------------------------------------------ next: ch7's circuit
    def clip3(self):
        with self.say("c6.recap.3") as c:
            def blk(x, y, wd, ht):
                return Rectangle(width=wd, height=ht).set_stroke(DIM, 3).set_fill(BG, 1).move_to(_p(x, y))

            def ff(x):
                b = Rectangle(width=0.9, height=1.5).set_stroke(DIM, 3).set_fill(BG, 1).move_to(_p(x, 0))
                t = Polygon(_p(x - 0.14, -0.75), _p(x + 0.14, -0.75), _p(x, -0.53)).set_stroke(DIM, 3)
                return VGroup(b, t)

            def wire(*pts):
                return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(DIM, 3)

            ffi, ffo = ff(-5.4), ff(5.4)
            cb1, cb2 = blk(-3.2, 0.85, 1.4, 0.9), blk(-3.2, -0.85, 1.4, 0.9)
            cb3, cb4 = blk(-0.7, 0, 1.4, 1.1), blk(3.0, 0, 1.5, 1.1)
            wires = [wire((-4.95, 0), (-4.4, 0)),
                     wire((-4.4, 0), (-4.4, 0.85), (-3.9, 0.85)),
                     wire((-4.4, 0), (-4.4, -0.85), (-3.9, -0.85)),
                     wire((-2.5, 0.85), (-1.9, 0.85), (-1.9, 0.3), (-1.4, 0.3)),
                     wire((-2.5, -0.85), (-1.9, -0.85), (-1.9, -0.3), (-1.4, -0.3)),
                     wire((0.0, 0), (2.25, 0)),
                     wire((3.75, 0), (4.95, 0))]
            fork = Dot(_p(-4.4, 0), radius=0.07, color=DIM)
            bus = wire((-6.0, -1.5), (5.4, -1.5))
            brs = [wire((x, -1.5), (x, -0.75)) for x in (-5.4, 5.4)]
            circuit = VGroup(*wires, fork, bus, *brs, cb1, cb2, cb3, cb4, ffi, ffo)
            head = T("Next: a real circuit", 44).move_to(_p(0, 3.0))

            RXN = 1.12
            outline = DashedVMobject(Rectangle(width=0.8, height=1.3), num_dashes=24) \
                .set_stroke(GOLD, 3).move_to(_p(RXN, 0))
            q = T("?", 56, GOLD).move_to(_p(RXN, 1.2))
            reg_box = Rectangle(width=0.8, height=1.3).set_stroke(YELLOW, 4).set_fill(BG, 1).move_to(_p(RXN, 0))
            reg_tri = Polygon(_p(RXN - 0.13, -0.65), _p(RXN + 0.13, -0.65), _p(RXN, -0.45)).set_stroke(YELLOW, 3)
            reg_br = Line(_p(RXN, -1.5), _p(RXN, -0.65)).set_stroke(YELLOW, 3)
            reg = VGroup(reg_br, reg_box, reg_tri)
            faster = T("how much faster?", 44, GOLD).move_to(_p(0, -2.7))

            c.wait_until("a real circuit")
            sweep_clear(self, time_span(FadeIn(circuit), 0.6, 1.6),
                        time_span(FadeIn(head, shift=0.2 * DOWN), 0.8, 1.6), run_time=1.6)
            self.play(FadeIn(outline), *appear(q), run_time=1.0)  # early: the teaser's question mark

            n = 2

            def blink(m, a):
                m.set_stroke(opacity=0.3 + 0.7 * (0.5 + 0.5 * np.cos(TAU * n * a)))
            self.play(UpdateFromAlphaFunc(outline, blink, rate_func=linear),
                      run_time=c.until("add", floor=0.5))
            outline.set_stroke(opacity=1)
            self.play(*during([FadeOut(outline)], 0, 0.5),
                      *during([FadeIn(reg)], 0.3, 1.0), run_time=1.4)
            c.wait_until("buy", own_word=faster)
            self.play(*appear(faster), run_time=1.0)
