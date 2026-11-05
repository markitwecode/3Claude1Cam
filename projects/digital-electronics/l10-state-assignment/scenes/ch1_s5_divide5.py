"""Chapter 1, scene 5: the divide-by-5 counter: spec, waveform, five states, three flip-flops. Clips c1.divide.1 – c1.divide.3.

Shared (imported by s6, s8, ch2-ch3):
  clock_wave(width, height, periods, ...)   L6's ClockWave (rising_x(i), period).
  divide5_wave(width=9.8, height=0.7, periods=10, gap=1.5, label_size=40)
      the chapter's running waveform: CLK over Output (high 2 periods, low 3), wave centred on ORIGIN,
      labels hanging left. Attrs .clk .out (VGroup of 4 pieces) .pieces .guides .clk_label
      .out_label .rise_x (list) .changes (edge indices [0, 2, 5, 7]) .clk_y .out_y .period
  state_ring(codes=None, radius=RING_R, center=ORIGIN, code_size=30)
      the five-state ring, L6 state_ring style: BLUE nodes clockwise from 12 o'clock, GOLD state
      numbers inside, FG arrows i -> i+1, GREEN codes just outside (default "? ? ?").
      VGroup(arrows, nodes, codes); attrs .nodes .circles .nums .arrows .codes .center
      .code_at(i, text, color=GREEN, size=code_size) -> a Mono placed in node i's code slot.
  handover_shot()  = state_ring() at ORIGIN (this scene's last frame; s6 opens on it).
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


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- L6 ClockWave (ch1_s3_clock.py), trimmed to the parts used ---------------------------------
class ClockWave(VGroup):
    def __init__(self, width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True,
                 down_arrows=False, stroke_width=4, **kw):
        super().__init__(**kw)
        p = width / (periods + 0.5)
        x0, lo, hi = -width / 2, -height / 2, height / 2
        pts, self._rise, self._fall = [[x0, lo, 0]], [], []
        x = x0 + p / 2
        for _ in range(periods):
            pts += [[x, lo, 0], [x, hi, 0]]
            self._rise.append(x - x0)
            x += p / 2
            pts += [[x, hi, 0], [x, lo, 0]]
            self._fall.append(x - x0)
            x += p / 2
        pts.append([x0 + width, lo, 0])
        self.wave = VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width)
        self.period, self._width = p, width
        tri = 0.11 * min(1.0, height / 0.7)
        self.ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1)
                            .move_to([x0 + r, 0, 0]) for r in (self._rise if up_arrows else [])])
        self.downs = VGroup()
        self.add(self.wave, self.ups, self.downs)

    def rising_x(self, i):
        return self.wave.get_left()[0] + self._rise[i] * self.wave.width / self._width


def clock_wave(width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True, down_arrows=False):
    return ClockWave(width, height, periods, color, up_arrows, down_arrows)


# ---- the chapter's running waveform --------------------------------------------------------------
def divide5_wave(width=9.8, height=0.7, periods=10, gap=1.5, label_size=40, pattern=(1, 1, 0, 0, 0)):
    """CLK (YELLOW, up-arrows) over Output (GREEN): Output holds pattern[k % 5] from rising edge k
    (before edge 0 it shows pattern[-1]). Thin DIM guides at every rising edge. The wave is centred
    on ORIGIN (CLK at +gap/2, Output at -gap/2); the labels hang to its left."""
    clk_y, out_y = gap / 2, -gap / 2
    clk = clock_wave(width, height, periods).shift(UP * clk_y)
    rx = [clk.rising_x(i) for i in range(periods)]
    x0, x1 = -width / 2, width / 2
    lev = lambda b: out_y + (height / 2 if b else -height / 2)  # noqa: E731
    vals = [pattern[k % 5] for k in range(periods)]
    changes = [k for k in range(periods) if vals[k] != (vals[k - 1] if k else pattern[-1])]
    pieces, b = [], pattern[-1]
    cur = [_p(x0, lev(b))]
    for j, k in enumerate(changes):
        if j > 0:
            cur.append(_p(rx[k], lev(b)))
            pieces.append(VMobject().set_points_as_corners(cur).set_stroke(GREEN, 4))
            cur = [_p(rx[k], lev(b))]
        else:
            cur.append(_p(rx[k], lev(b)))
        b = vals[k]
        cur.append(_p(rx[k], lev(b)))
    cur.append(_p(x1, lev(b)))
    pieces.append(VMobject().set_points_as_corners(cur).set_stroke(GREEN, 4))
    out = VGroup(*pieces)
    top, bot = clk_y + height / 2 + 0.12, out_y - height / 2 - 0.12
    guides = VGroup(*[Line(_p(x, bot), _p(x, top)).set_stroke(DIM, 1.5) for x in rx]).set_z_index(-1)
    clk_label = T("CLK", label_size, YELLOW).next_to(_p(x0, clk_y), LEFT, buff=0.3)
    out_label = T("Output", label_size, GREEN).next_to(_p(x0, out_y), LEFT, buff=0.3)
    g = VGroup(guides, clk, out, clk_label, out_label)
    g.clk, g.out, g.pieces, g.guides = clk, out, pieces, guides
    g.clk_label, g.out_label = clk_label, out_label
    g.rise_x, g.changes, g.clk_y, g.out_y, g.period = rx, changes, clk_y, out_y, clk.period
    return g


# ---- the five-state ring (L6 state_ring style) ---------------------------------------------------
NODE_R = 0.5
RING_R = 1.35


def _dirn(i, n=5):
    a = PI / 2 - TAU * i / n
    return np.array([np.cos(a), np.sin(a), 0.0])


def state_ring(codes=None, radius=RING_R, center=ORIGIN, code_size=30):
    """Five states clockwise from 12 o'clock: BLUE nodes, GOLD numbers inside, FG arrows i -> i+1,
    GREEN codes just outside each node (default "? ? ?")."""
    center = np.array(center, dtype=float)
    codes = list(codes) if codes is not None else ["? ? ?"] * 5
    nodes, circles, nums, arrows = [], [], [], []
    for i in range(5):
        p = center + radius * _dirn(i)
        circ = Circle(radius=NODE_R, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        num = T(str(i), 34, GOLD).move_to(p)
        circles.append(circ)
        nums.append(num)
        nodes.append(VGroup(circ, num))
    for i in range(5):
        p, q = center + radius * _dirn(i), center + radius * _dirn((i + 1) % 5)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + (NODE_R + 0.04) * u, q - (NODE_R + 0.04) * u, buff=0, color=FG,
                            stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4))

    def code_at(i, text, color=GREEN, size=code_size):
        m = Mono(text, size=size, color=color)
        d = _dirn(i)
        half = abs(d[0]) * m.width / 2 + abs(d[1]) * m.height / 2
        return m.move_to(center + (radius + NODE_R + 0.14 + half) * d)

    code_ms = [code_at(i, s) for i, s in enumerate(codes)]
    ring = VGroup(VGroup(*arrows), VGroup(*nodes), VGroup(*code_ms))
    ring.nodes, ring.circles, ring.nums, ring.arrows, ring.codes = nodes, circles, nums, arrows, code_ms
    ring.code_at, ring.center = code_at, center
    return ring


def handover_shot():
    """The last frame: the five-state ring alone at centre, codes "? ? ?" (s6 opens on it)."""
    return state_ring()


# ---- scene-local pieces --------------------------------------------------------------------------
_S1 = load_scene("ch1_s1_hook")


def dff(center):
    """s1's make_ff (L6's D flip-flop: D, Q, Q-bar, clock triangle), at s3's half scale."""
    g = _S1.make_ff(size=56).scale(0.5, about_point=ORIGIN).shift(center)
    g.q_end = g.q_w.get_end()
    return g


def _clk_pts(x0, x1, rises, per):
    pts = [(x0, 0)]
    for r in rises:
        pts += [(r, 0), (r, 1), (r + per / 2, 1), (r + per / 2, 0)]
    return pts + [(x1, 0)]


def _toggle_pts(x0, x1, edges):
    pts, b = [(x0, 0)], 0
    for x in edges:
        pts += [(x, b), (x, 1 - b)]
        b = 1 - b
    return pts + [(x1, b)]


def _trace(pts, y, amp, color, width=3):
    return VMobject().set_points_as_corners([_p(x, y + (amp if b else -amp)) for x, b in pts]).set_stroke(color, width)


def l6_inset():
    """L6 ch3 s4's toggle traces in miniature: CLK (f), Q (f/2), the dim next stage (f/4)."""
    x0, x1 = -2.6, 2.0
    per = (x1 - x0) / 6.3
    rises = [x0 + 0.5 * per + k * per for k in range(6)]
    ys, amp = (0.55, 0.0, -0.55), 0.16
    clk = _trace(_clk_pts(x0, x1, rises, per), ys[0], amp, YELLOW)
    q = _trace(_toggle_pts(x0, x1, rises), ys[1], amp, GREEN)
    q4 = _trace(_toggle_pts(x0, x1, rises[1::2]), ys[2], amp, GOLD).set_stroke(opacity=0.5)
    labs = [MathTex(s, font_size=36, color=GOLD).next_to(_p(x1, y), RIGHT, buff=0.25)
            for s, y in zip(("f", "f/2", "f/4"), ys)]
    labs[2].set_opacity(0.55)
    traces = VGroup(clk, q, q4)
    frame = RoundedRectangle(corner_radius=0.15, width=VGroup(traces, *labs).width + 0.6,
                             height=traces.height + 0.55).set_stroke(DIM, 2)
    frame.move_to(VGroup(traces, *labs))
    cap = T("Lecture 6", 28, DIM).next_to(frame, LEFT, buff=0.3)
    g = VGroup(frame, traces, *labs, cap)
    g.frame, g.traces, g.labs, g.cap = frame, traces, labs, cap
    return g


SPEC = ("We wish to investigate some state assignment options\n"
        "to implement a divide by 5 counter which gives a 1\n"
        "output for 2 clock edges and is 0 for 3 clock edges")
WAVE_C = _p(0.15, -0.15)            # the running waveform's centre in clips 1-2
RING_C = _p(-3.3, -1.4)            # the ring's centre in clip 3 (handover: shifted back to ORIGIN)
FF_Y, FF_X = -1.6, (0.95, 3.1, 5.25)


class Divide5(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.ending()

    # -- c1.divide.1: the spec, the black box, the waveform ----------------------------------------
    def clip1(self):
        with self.say("c1.divide.1") as c:
            head = T("Example Problem", 48).move_to(_p(0, 3.1))
            spec = T(SPEC, 34, line_spacing=0.9).move_to(_p(0, 1.5))
            self.spec = spec
            self.play(*appear(head, spec, lag=0.4), run_time=1.4)  # early: the slide, shown whole and then read
            c.wait_until("noinputs")
            box = Rectangle(width=2.4, height=1.6).set_stroke(BLUE, 4).move_to(_p(0, -1.6))
            qm = T("?", 80, YELLOW).move_to(box)
            self.play(FadeIn(box), *appear(qm), run_time=0.8)
            clk_in = Arrow(_p(-3.3, -1.6), box.get_left(), buff=0, color=YELLOW, stroke_width=5,
                           max_tip_length_to_length_ratio=0.15)
            clk_t = T("CLK", 40, YELLOW).next_to(clk_in, LEFT, buff=0.25)
            out_a = Arrow(box.get_right(), _p(3.3, -1.6), buff=0, color=GREEN, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)
            out_t = T("Output", 40, GREEN).next_to(out_a, RIGHT, buff=0.25)
            self.play(GrowArrow(clk_in), *appear(clk_t),  # early: the box's two ports, one diagram; Output is named next
                      *during([GrowArrow(out_a), *appear(out_t)], 0.4, 1.0), run_time=1.3)

            c.wait_until("high")
            w = divide5_wave().shift(WAVE_C)
            self.w = w
            self.play(*during(disappear(head, box, qm, clk_in, clk_t, out_a, out_t), 0, 0.45),
                      *during([spec.animate.scale(30 / 34).move_to(_p(0, 2.75))], 0.1, 0.75),
                      *during(appear(w.clk_label, w.clk, w.out_label, shift=None, lag=0.15), 0.45, 1.0),
                      *during([FadeIn(w.guides)], 0.6, 1.0),
                      run_time=1.4)
            p = w.pieces
            self.play(Create(p[0]), run_time=min(1.3, c.until("low") - 0.05), rate_func=linear)
            c.wait_until("low")
            self.play(Create(p[1]), run_time=min(1.1, c.until("repeat") - 0.05), rate_func=linear)
            c.wait_until("repeat")
            self.play(Succession(Create(p[2]), Create(p[3])), run_time=1.4, rate_func=linear)

            c.wait_until("edges")
            for k, cue in zip(w.changes[:2], ("changes only", "rising edge")):
                c.wait_until(cue)
                g = w.guides[k]
                self.play(g.animate.set_stroke(YELLOW, 3),
                          VShowPassingFlash(g.copy().set_stroke(YELLOW, 8), time_width=0.6),
                          FlashAround(w.clk.ups[k], color=YELLOW, buff=0.08),
                          run_time=1.2)

    # -- c1.divide.2: five periods, the name, L6's dividers, f and f/5 -----------------------------
    def clip2(self):
        w = self.w
        with self.say("c1.divide.2") as c:
            top = w.clk.get_top()[1]
            brace = span_brace(_p(w.rise_x[0], top), _p(w.rise_x[5], top), direction=UP, color=GOLD)
            g0, g5 = w.guides[0].get_x(), w.guides[5].get_x()   # the drawn edges (rise_x predates any shift)
            brace.stretch_to_fit_width(g5 - g0).set_x((g0 + g5) / 2)  # tips on the two output rises
            blab = T("5 clock periods", 36, GOLD).next_to(brace, UP, buff=0.15)
            self.brace, self.blab = brace, blab
            self.play(*during(disappear(self.spec), 0, 0.45),
                      *during([GrowFromCenter(brace)], 0.35, 1.0), run_time=1.5)
            c.wait_until(own_word=blab)
            self.play(*appear(blab), run_time=1.0)

            c.wait_until("name")
            div = MathTex(r"\div\,5", font_size=60, color=GOLD)
            title = T("divide-by-5 counter", 48)
            VGroup(div, title).arrange(RIGHT, buff=0.45).move_to(_p(0, 3.2))
            self.div, self.title = div, title
            c.wait_until(own_word=title)
            self.play(*appear(div, title, lag=0.3), run_time=1.2)

            c.wait_until("lecture6")
            ins = l6_inset().move_to(_p(-0.3, -2.75))
            self.ins = ins
            self.play(FadeIn(ins.frame), *appear(ins.cap, shift=None),
                      *[Create(t) for t in ins.traces], run_time=1.5)
            self.play(*appear(*ins.labs, lag=0.35), run_time=min(1.3, c.until("byfive")))

            c.wait_until("byfive")
            f1 = MathTex("f", font_size=44, color=GOLD).next_to(_p(w.clk.get_right()[0], w.clk.get_y()), RIGHT, buff=0.3)
            f5 = MathTex("f/5", font_size=44, color=GOLD).next_to(w.out.get_right(), RIGHT, buff=0.3)
            self.f1, self.f5 = f1, f5
            self.play(*fly(ins.labs[0], f1), run_time=1.3)
            self.play(*appear(f5), run_time=1.0)

    # -- c1.divide.3: five states, three flip-flops, c b a -----------------------------------------
    def clip3(self):
        w = self.w
        with self.say("c1.divide.3") as c:
            # the waveform goes up and shrinks; a GOLD box walks its five periods, a state per period
            moving = [w.guides, w.clk, *w.pieces, w.clk_label, w.out_label, self.brace, self.f1, self.f5]
            s = 0.7
            o = w.clk.get_center() * 0 + WAVE_C
            new_top = o[1] + s * (self.brace.get_top()[1] - o[1])
            v = _p(-0.15, 3.55 - new_top)
            self.play(*during(disappear(self.ins, self.title, self.div, self.blab), 0, 0.45),
                      *during([m.animate.scale(s, about_point=o).shift(v) for m in moving], 0.3, 1.0),
                      run_time=1.3)
            rx = [g.get_x() for g in w.guides]   # the drawn edges, after the move
            ytop = w.clk.get_top()[1] + 0.08
            ybot = w.out.get_bottom()[1] - 0.08

            def pbox(k):
                return (Rectangle(width=rx[k + 1] - rx[k], height=ytop - ybot)
                        .set_stroke(GOLD, 2).set_fill(GOLD, 0.18).move_to(_p((rx[k] + rx[k + 1]) / 2, (ytop + ybot) / 2))
                        .set_z_index(-2))

            ring = state_ring().shift(RING_C)
            self.ring = ring
            box = pbox(0)
            self.play(FadeIn(box), *appear(ring.nodes[0], shift=0.5 * DOWN), run_time=0.9)
            for k in range(1, 5):
                self.play(Transform(box, pbox(k)), *appear(ring.nodes[k], shift=0.5 * DOWN), run_time=0.55)
            self.play(*during([FadeOut(box)], 0, 0.4), *[GrowArrow(a) for a in ring.arrows],
                      *during(appear(*ring.codes, lag=0.1), 0.3, 1.0),
                      run_time=min(1.5, c.until("threeffs")))
            settle(self, ring)

            c.wait_until("threeffs")
            ffs = [dff(_p(x, FF_Y)) for x in FF_X]
            note = T("5 states: 3 flip-flops", 36, GOLD).move_to(_p(3.1, 0.1))
            self.play(*appear(*ffs, lag=0.25), run_time=1.3)
            self.play(*appear(note), run_time=1.0)

            c.wait_until("names")
            labs = [T(n, 40, GREEN).move_to(ff.q_end + _p(0, 0.38)) for n, ff in zip("cba", ffs)]
            for lab, cue in zip(labs, ("see", "bee", "and a")):
                c.wait_until(cue)
                self.play(*appear(lab), run_time=0.5)
            for ff, lab in zip(ffs, labs):
                settle(self, ff, add=[lab])     # each flip-flop leaves with its label
            code0 = ring.codes[0]
            header = VGroup(*[Mono(n, 30, GREEN).move_to(_p(code0[i].get_x(), code0.get_top()[1] + 0.27))
                              for i, n in enumerate("cba")])
            c.wait_until("written")
            self.play(*appear(header), run_time=1.0)
            tag_t = T("rightmost bit", 30, YELLOW).next_to(header[2], RIGHT, buff=0.75)
            tag_a = Arrow(tag_t.get_left(), header[2].get_right(), buff=0.08, stroke_width=3, color=YELLOW,
                          max_tip_length_to_length_ratio=0.35, tip_length=0.15)
            c.wait_until("on the right")
            self.play(GrowArrow(tag_a), *appear(tag_t, shift=None), run_time=1.0)
            self.header, self.tag = header, VGroup(tag_t, tag_a)

    # -- handover: everything clears but the ring, which settles at centre --------------------------
    def ending(self):
        self.wait(2.8)
        ring = self.ring
        sweep_clear(self, ring.animate.shift(-RING_C), keep=[ring], run_time=2.2)
        self.wait(1.0)
