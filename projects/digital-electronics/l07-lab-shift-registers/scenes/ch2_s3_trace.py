"""Chapter 2, scene 3: following the bits through p. 102's timing diagram. Clips c2.trace.1 – c2.trace.4.

Top strip: L8 ch2_s3's build_chain() (loaded by path, as ch1_s1 does), at 0.55, in-box D/Q labels and
Q risers dropped, one digit per box (DIM "?" / GOLD bit). Timing diagram: L6 ch2_s4's square style
(row_y ± AMP 0.2, stroke 4, thin DIM guides, YELLOW ▲ on CLK, MathTex labels starting DIM), rebuilt
here for nine rising edges and rows CLK, D_in, Q_0, Q_1, Q_2. Unknown stretches: both levels plus a
faint GREEN fill. Starts and ends on an empty frame.
"""
# style: 2
import importlib.util
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


def _load_l8():
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch2_s3_shiftreg.py"
    spec = importlib.util.spec_from_file_location("_l08_ch2_s3_shiftreg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8 = _load_l8()


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the strip: L8's chain at 0.55 along the top --------------------------------------------------
STRIP_S = 0.55


def build_strip():
    C = L8.build_chain()
    for f in C.ffs:
        f.remove(f.d_l, f.q_l)
    shapes = VGroup(*C.ffs, *C.links, C.tail, C.bus, *C.jdots, *C.clk_ws)
    shapes.scale(STRIP_S, about_point=ORIGIN)
    din = MathTex("D_{in}", font_size=32, color=BLUE).next_to(C.ffs[0].d_w.get_start(), LEFT, buff=0.1)
    clk = T("CLK", 28, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.12)
    names = [T(f"FF{i}", 28).next_to(f.box, UP, buff=0.1) for i, f in enumerate(C.ffs)]
    strip = VGroup(shapes, din, clk, *names)
    strip.shift(_p(-6.3, 3.5) - _p(strip.get_left()[0], strip.get_top()[1]))
    strip.boxes = [f.box for f in C.ffs]
    return strip


def sdigit(ch, box):
    return T(ch, 36, DIM if ch == "?" else GOLD).move_to(box.get_center())


# ---- the timing diagram (L6 square style, nine edges) ---------------------------------------------
X0, X1 = -5.4, 6.4
P = (X1 - X0) / 9.2
RISE = [X0 + 0.6 * P + k * P for k in range(9)]
DLY = 0.15 * P
XE = [r + DLY for r in RISE] + [X1]          # Q changes just after each edge; XE[9] = end of the trace
AMP = 0.2
ROW_Y = [1.0, 0.15, -0.7, -1.55, -2.4]
PITCH = ROW_Y[0] - ROW_Y[1]
TEXS = [r"\mathrm{CLK}", r"D_{in}", "Q_0", "Q_1", "Q_2"]
COLS = [YELLOW, BLUE, GREEN, GREEN, GREEN]
DIN = [0, 0, 1, 1, 1, 0, 0, 1, 1]
QV = [[0, 0, 1, 1, 1, 0, 0, 1, 1],
      [None, 0, 0, 1, 1, 1, 0, 0, 1],
      [None, None, 0, 0, 1, 1, 1, 0, 0]]
STATES = ["0??", "00?", "100", "110", "111", "011", "001", "100", "110"]


def yl(row, b):
    return ROW_Y[row] + (AMP if b else -AMP)


def path(row, pts, color=None, width=4):
    return (VMobject().set_points_as_corners([_p(x, yl(row, b)) for x, b in pts])
            .set_stroke(color or COLS[row], width))


def clk_wave():
    f0 = X0 + 0.1 * P
    pts = [(X0, 1), (f0, 1), (f0, 0)]
    for r in RISE:
        pts += [(r, 0), (r, 1), (r + P / 2, 1), (r + P / 2, 0)]
    pts.append((X1, 0))
    return path(0, pts)


def din_wave():
    pts, lv = [(X0, 0)], 0
    for k in (1, 4, 6):
        x = RISE[k] + P / 2
        pts += [(x, lv), (x, 1 - lv)]
        lv = 1 - lv
    pts.append((X1, lv))
    return path(1, pts)


def seg(q, k):
    """Q_q's trace from edge k+1's change to the next one (row 2 + q)."""
    b = QV[q][k]
    prev = QV[q][k - 1] if k > 0 and QV[q][k - 1] is not None else None
    if prev is None:
        pts = [(XE[k], 1 - b), (XE[k], b), (XE[k + 1], b)]
    elif prev != b:
        pts = [(XE[k], prev), (XE[k], b), (XE[k + 1], b)]
    else:
        pts = [(XE[k], b), (XE[k + 1], b)]
    return path(2 + q, pts)


def ublock(row, xa, xb):
    hi = Line(_p(xa, yl(row, 1)), _p(xb, yl(row, 1))).set_stroke(GREEN, 4)
    lo = Line(_p(xa, yl(row, 0)), _p(xb, yl(row, 0))).set_stroke(GREEN, 4)
    fill = Rectangle(width=xb - xa, height=2 * AMP).move_to(_p((xa + xb) / 2, ROW_Y[row]))
    fill.set_stroke(width=0).set_fill(GREEN, 0.15)
    return VGroup(fill, hi, lo)


def q0_trace(x_end):
    """Q_0's known trace as one path, from its first change to x_end (for flashes and ghosts)."""
    pts = [(XE[0], 1), (XE[0], 0)]
    lv = 0
    for k in range(1, 9):
        if XE[k] > x_end:
            break
        if QV[0][k] != lv:
            pts += [(XE[k], lv), (XE[k], QV[0][k])]
            lv = QV[0][k]
    pts.append((x_end, lv))
    return path(2, pts)


class Trace(NarratedScene):
    def construct(self):
        self.build()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def build(self):
        self.strip = build_strip()
        self.state = "???"
        self.digs = [sdigit("?", b) for b in self.strip.boxes]
        self.labels = [MathTex(t, font_size=36, color=DIM).move_to(_p(0, y)).align_to(_p(X0 - 0.3, 0), RIGHT)
                       for t, y in zip(TEXS, ROW_Y)]
        g_top, g_bot = ROW_Y[0] + AMP + 0.12, ROW_Y[4] - AMP - 0.12
        self.guides = [Line(_p(x, g_top), _p(x, g_bot)).set_stroke(DIM, 1.5).set_z_index(-2) for x in RISE]
        self.nums = [T(str(k + 1), 28, DIM).move_to(_p(x, g_top + 0.28)) for k, x in enumerate(RISE)]
        self.ups = [Triangle().scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(x, ROW_Y[0]))
                    for x in RISE]
        self.dval = [T(str(b), 28, BLUE).move_to(_p(x + 0.2, (yl(0, 0) + yl(1, 1)) / 2))
                     for b, x in zip(DIN, RISE)]
        self.segs = [[seg(q, k) if QV[q][k] is not None else None for k in range(9)] for q in range(3)]
        self.unk = [[ublock(2 + q, X0, XE[0])] for q in range(3)]
        self.cur = None

    # ---- helpers ---------------------------------------------------------------------------------
    def to_state(self, k):
        anims = []
        for i, ch in enumerate(STATES[k]):
            if ch != self.state[i]:
                new = sdigit(ch, self.strip.boxes[i])
                anims += swap(self.digs[i], new)
                self.digs[i] = new
        self.state = STATES[k]
        return anims

    def mark_edge(self, k):
        anims = [self.nums[k].animate.set_color(YELLOW)]
        if self.cur is not None and self.cur != k:
            anims.append(self.nums[self.cur].animate.set_color(DIM))
        self.cur = k
        return anims

    def dots_at(self, k):
        return _p(RISE[k], yl(1, DIN[k])), _p(XE[k] + 0.12, yl(2, QV[0][k]))

    # ---- clip 1: the diagram, the clock, the input, the unknown start ----------------------------
    def clip1(self):
        with self.say("c2.trace.1") as c:
            self.play(FadeIn(self.strip), *[FadeIn(d) for d in self.digs], run_time=1.0)
            self.play(*appear(*self.labels, lag=0.12, shift=0.2 * RIGHT),  # early: the diagram's empty frame, rows filled one by one
                      *[GrowFromEdge(g, UP) for g in self.guides],
                      *[FadeIn(n) for n in self.nums],
                      run_time=min(1.6, c.until("clock")))
            c.wait_until("clock")
            self.clk = clk_wave()
            self.play(Create(self.clk), self.labels[0].animate.set_color(YELLOW),
                      run_time=min(2.0, c.until("nine")), rate_func=linear)
            c.wait_until("nine")
            self.play(LaggedStart(*[FadeIn(u, shift=0.12 * DOWN) for u in self.ups], lag_ratio=0.2),
                      run_time=min(1.4, c.until("input")))
            c.wait_until("input")
            self.din = din_wave()
            self.play(Create(self.din), self.labels[1].animate.set_color(BLUE),
                      run_time=min(1.8, c.until("read at")), rate_func=linear)
            words = [("zero", 0), ("zero", 1), ("one", 0), ("one", 1), ("one", 2),
                     ("zero", 2), ("zero", 3), ("one", 3), ("one", 4)]
            for i, (w, n) in enumerate(words):
                c.wait_until(w, nth=n)
                self.play(*appear(self.dval[i], shift=0.12 * DOWN), run_time=0.5)
            c.wait_until("unknown")
            self.play(*appear(*[u[0] for u in self.unk], lag=0.2, shift=None),
                      *[self.labels[r].animate.set_color(GREEN) for r in (2, 3, 4)],
                      run_time=min(1.4, c.until("both levels")))
            c.wait_until("both levels")
            self.tag = T("unknown", 30, GREEN).move_to(_p(0, -3.1)).align_to(_p(X0, 0), LEFT)
            self.play(*appear(self.tag), run_time=1.0)

    # ---- clip 2: Q_0 edge by edge ----------------------------------------------------------------
    def q0_edge(self, k, rt):
        bd, gd = self.dots_at(k)
        self.play(*self.mark_edge(k), self.bdot.animate.move_to(bd), run_time=0.6 * rt)
        self.play(Create(self.segs[0][k]), self.gdot.animate.move_to(gd), *self.to_state(k), run_time=rt)

    def clip2(self):
        with self.say("c2.trace.2") as c:
            bd, gd = self.dots_at(0)
            self.bdot = Dot(bd, radius=0.09, color=BLUE)
            self.gdot = Dot(gd, radius=0.09, color=GREEN)
            self.play(*self.mark_edge(0), FadeIn(self.bdot, scale=0.5), run_time=0.8)
            c.wait_until("so cue")
            self.play(Create(self.segs[0][0]), FadeIn(self.gdot, scale=0.5), *self.to_state(0),
                      run_time=min(1.5, c.until("moment")))
            c.wait_until("e2")
            self.q0_edge(1, min(1.3, 0.5 * c.until("e3")))
            c.wait_until("e3")
            self.q0_edge(2, min(1.3, 0.5 * c.until("e5")))
            c.wait_until("e5")
            self.q0_edge(3, 0.8)
            self.q0_edge(4, 0.8)
            c.wait_until("e6")
            self.q0_edge(5, min(1.2, 0.5 * c.until("copy")))
            c.wait_until("copy")
            self.play(*disappear(self.bdot, self.gdot), self.nums[self.cur].animate.set_color(DIM),
                      run_time=0.5)
            self.cur = None
            x_end = XE[6]
            r1, r4 = RISE[1] + P / 2, RISE[4] + P / 2
            dflash = path(1, [(X0, 0), (r1, 0), (r1, 1), (r4, 1), (r4, 0), (x_end, 0)], color=YELLOW, width=6)
            qflash = q0_trace(x_end).set_stroke(YELLOW, 6)
            self.play(VShowPassingFlash(dflash, time_width=0.5), VShowPassingFlash(qflash, time_width=0.5),
                      run_time=min(2.0, c.until()))

    # ---- clip 3: Q_1 and Q_2, then the last three edges ------------------------------------------
    def clip3(self):
        with self.say("c2.trace.3") as c:
            self.play(FlashAround(self.labels[3], color=GREEN, run_time=1.0))
            c.wait_until("old value")
            ext1 = ublock(3, XE[0], XE[1])
            self.unk[1].append(ext1)
            src = self.unk[0][0]
            arr = Arrow(_p(src.get_center()[0], yl(2, 0) - 0.06), _p(ext1.get_center()[0] - 0.1, yl(3, 1) + 0.06),
                        buff=0, stroke_width=3, tip_length=0.16,
                        max_tip_length_to_length_ratio=0.35).set_color(GREEN)
            self.play(GrowArrow(arr), FadeIn(ext1), run_time=min(1.5, c.until("q1known")))
            c.wait_until("q1known")
            self.play(FadeOut(arr), Create(self.segs[1][1], rate_func=linear), run_time=min(1.4, c.until("as zero")))
            c.wait_until("q1rest")
            self.play(Succession(*[Create(self.segs[1][k], rate_func=linear) for k in range(2, 6)]),
                      run_time=min(2.6, c.until("q2")))
            c.wait_until("q2")
            ext2 = ublock(4, XE[0], XE[2])
            self.unk[2].append(ext2)
            self.play(FadeIn(ext2), FlashAround(self.labels[4], color=GREEN),
                      run_time=min(1.2, c.until("stays unknown")))
            c.wait_until("third edge")
            self.play(Succession(*[Create(self.segs[2][k], rate_func=linear) for k in range(2, 6)]),
                      run_time=min(2.0, c.until("run")))
            c.wait_until("run")
            rt = min(1.0, (c.until() - 0.1) / 3)
            for k in (6, 7, 8):
                self.play(*self.mark_edge(k), *[Create(self.segs[q][k], rate_func=linear) for q in range(3)],
                          *self.to_state(k), run_time=rt)

    # ---- clip 4: same waveform, the first 1, the slide's line, forgetting ------------------------
    def clip4(self):
        with self.say("c2.trace.4") as c:
            x_g = X1 - 2 * P
            self.play(*disappear(self.tag), self.nums[self.cur].animate.set_color(DIM), run_time=0.8)
            self.cur = None
            g1 = q0_trace(x_g).set_stroke(YELLOW, 6, opacity=0.7).shift(PITCH * DOWN)
            self.play(FadeIn(g1, shift=PITCH * DOWN), run_time=0.8)
            self.play(g1.animate.shift(P * RIGHT), run_time=1.0)
            c.wait_until("same waveform")
            g2 = q0_trace(x_g).set_stroke(YELLOW, 6, opacity=0.7).shift(2 * PITCH * DOWN)
            self.play(FadeOut(g1), FadeIn(g2, shift=2 * PITCH * DOWN), run_time=1.0)
            self.play(g2.animate.shift(2 * P * RIGHT), run_time=1.4)
            c.wait_until("first")
            self.play(FadeOut(g2), *disappear(*self.digs), run_time=0.8)
            c.wait_until("edge three")

            def hbox(q, k):
                return (Rectangle(width=0.62, height=2 * AMP + 0.36).move_to(_p(XE[k] + 0.08, ROW_Y[2 + q]))
                        .set_stroke(GOLD, 3).set_fill(GOLD, 0.18).set_z_index(-1))

            box = hbox(0, 2)
            hop = T("1", 36, GOLD).move_to(self.strip.boxes[0].get_center())
            self.play(FadeIn(box), *appear(hop, shift=0.15 * DOWN), run_time=min(1.0, c.until("edge four")))
            c.wait_until("edge four")
            self.play(Transform(box, hbox(1, 3)), hop.animate.move_to(self.strip.boxes[1].get_center()),
                      run_time=min(1.0, c.until("edge five")))
            c.wait_until("edge five")
            self.play(Transform(box, hbox(2, 4)), hop.animate.move_to(self.strip.boxes[2].get_center()),
                      run_time=1.0)
            c.wait_until("slide")
            quote = T("“See data moves one position\nto the right on application\nof each clock edge”",
                      28, slant=ITALIC, line_spacing=1.0)
            quote.move_to(_p(3.5, 2.85))
            self.play(*disappear(box, hop), *appear(quote, shift=None), run_time=min(1.2, c.until("forget")))
            c.wait_until("forget")
            self.play(LaggedStart(*[FlashAround(VGroup(*self.unk[q]), color=GREEN, time_width=1.2)
                                    for q in range(3)], lag_ratio=0.6),
                      run_time=min(2.2, c.until("every output")))
            t1 = T("after 3 edges: all known", 30, GREEN)
            t2 = T("N stages: N edges", 30, YELLOW)
            VGroup(t1, t2).arrange(RIGHT, buff=1.0).move_to(_p(0.5, -3.1))
            c.wait_until("every output")
            self.play(*appear(t1), run_time=1.0)
            c.wait_until("in general")
            self.play(*appear(t2), run_time=1.0)
