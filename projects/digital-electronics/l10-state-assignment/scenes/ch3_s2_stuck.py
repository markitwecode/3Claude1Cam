"""Chapter 3, scene 2: all zeros. The lecturer's question, the student's answer, the ring stuck at
00000, and the ring's table, which has no row for it. Clips c3.stuck.1 – c3.stuck.3.

Opens on ch3_s1_hook.handover_shot() (ring with LEDs + the waveform panel, output flat), clock ticking.
"""
# style: 2
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


_S1 = load_scene("ch3_s1_hook")
_S5 = load_scene("ch2_s5_ring")
RING_STATES = _S5.RING_STATES

DIG_Y = -0.65            # Q digits under the flip-flops
READ_Y = -2.35           # "state = 00000"
TAB_C = _p(2.35, 0.2)    # the table, clip 3
SMALL_W, SMALL_C = 5.2, _p(-4.0, 2.3)   # the circuit, shrunk, clip 3
DIMROW_X = -3.75       # well clear of the table's left edge


def bubble(text, size=36, tail=UP, color=FG):
    """A speech bubble: rounded box (BG fill) round the text, a small tail on the `tail` side."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.22, width=t.width + 0.7, height=t.height + 0.5)
    box.set_stroke(DIM, 2.5).set_fill(BG, 1).move_to(t)
    edge = box.get_top() if tail is UP else box.get_bottom()
    x0 = box.get_left()[0] + 1.0
    s = 1 if tail is UP else -1
    tip = Polygon(_p(x0 - 0.18, edge[1]), _p(x0 + 0.18, edge[1]), _p(x0 - 0.28, edge[1] + s * 0.2))
    tip.set_stroke(DIM, 2.5).set_fill(BG, 1)
    g = VGroup(tip, box, t)
    g.text, g.box = t, box
    return g


class Stuck(NarratedScene):
    def construct(self):
        hs = _S1.handover_shot()
        self.add(hs)
        self.rl, self.pn = hs[0], hs[1]
        self.remove(hs)
        self.add(self.rl, self.pn)          # same picture, as two pieces
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- helpers ------------------------------------------------------------------------------------
    def ticks(self, rt, period=1.2, t0=0.0, dur=0.8):
        out, t = [], t0
        while t + dur <= rt + 1e-6:
            out += [time_span(VShowPassingFlash(m, time_width=0.6), t, t + dur) for m in self.rl.clk_paths()]
            t += period
        return out

    def tick_to(self, c, cue=None, own_word=None):
        """Keep the clock ticking until the cue."""
        while c.until(cue, floor=0, own_word=own_word) > 1.3:
            self.play(*self.ticks(1.2), run_time=1.2)
        c.wait_until(cue, own_word=own_word)

    @staticmethod
    def _dip(m, a):
        """The digit empties while its bit rides the wire, and refills as it lands."""
        m.set_opacity(1 - 0.85 * min(1.0, a / 0.25, (1 - a) / 0.2))

    def tokens(self, t0, t1):
        """A small GREEN 0 rides each Q -> next D wire (e's round the top into a), in [t0, t1] s."""
        out = []
        for path in self.rl.pass_paths():
            tok = Mono("0", 30, GREEN)
            set_backstroke(tok, width=6)
            tok.move_to(path.get_start()).set_opacity(0)

            def upd(m, a, path=path):
                m.move_to(path.point_from_proportion(a))
                m.set_opacity(min(1.0, a / 0.12, (1 - a) / 0.12))
            out.append(time_span(UpdateFromAlphaFunc(tok, upd, rate_func=smooth, remover=True), t0, t1))
        return out

    # -- c3.stuck.1: the question, the five ?s, the student's answer ---------------------------------
    def clip1(self):
        rl = self.rl
        with self.say("c3.stuck.1") as c:
            b1 = self.b1 = bubble("Why isn't this working?", 36, tail=UP).move_to(_p(0, 3.38))
            c.wait_until(own_word=b1.text)
            self.play(*appear(b1, shift=None), *self.ticks(1.2), run_time=1.2)
            self.tick_to(c, "think")
            # one ? per flip-flop, inside its own LED ring: what is it holding?
            qs = self.qs = [T("?", 30, RED).move_to(l.get_center()) for l in rl.leds]
            self.play(*appear(*qs, lag=0.15), *self.ticks(1.8), run_time=1.8)
            self.tick_to(c, "student")
            b2 = self.b2 = bubble("“We need to initialise it into one of the used states.”", 32,
                                  tail=DOWN).move_to(_p(0, -3.3))
            self.tick_to(c, own_word=b2.text)
            self.play(*appear(b2, shift=0.25 * UP), *self.ticks(1.2), run_time=1.2)
            self.tick_to(c)

    # -- c3.stuck.2: all zeros; an edge shifts zeros into zeros ---------------------------------------
    def clip2(self):
        rl, pn = self.rl, self.pn
        with self.say("c3.stuck.2") as c:
            digs = self.digs = [Mono("0", 48, GREEN).move_to(_p(f.box.get_x(), DIG_Y)) for f in rl.ffs]
            self.play(*during(disappear(self.b1, *self.qs, pn), 0, 0.45),
                      *during(appear(*digs, lag=0.15), 0.45, 1), run_time=min(2.0, c.until("the state")))
            # readout, table order e d c b a; laid out for its final "state = 00000 → 00000"
            lab = T("state =", 40)
            d1 = Mono("00000", 48, GREEN)
            arr = T("→", 44)
            d2 = Mono("00000", 48, GREEN)
            full = VGroup(lab, d1, arr, d2).arrange(RIGHT, buff=0.3).move_to(_p(0, READ_Y))
            arr.match_y(d1)
            d2.align_to(d1, DOWN)
            lab.align_to(d1, DOWN)
            short_dx = (full.get_right()[0] - d1.get_right()[0]) / 2
            VGroup(lab, d1).shift(short_dx * RIGHT)
            self.rd = (lab, d1, arr, d2)
            c.wait_until(own_word=lab)
            self.play(*during(disappear(self.b2), 0, 0.45),
                      *during(appear(lab, d1, lag=0.3), 0.45, 1), run_time=1.6)
            c.wait_until("shift")

            # one edge: the zeros ride the wires only while the clock edge lasts
            # the bits leave their boxes: the digits under them empty while the riders travel
            self.play(*self.ticks(2.0, dur=2.0), *self.tokens(0, 2.0),
                      *[time_span(UpdateFromAlphaFunc(d, lambda m, a: m.set_opacity(1 - 0.85 * a)), 0, 0.4)
                        for d in digs], run_time=2.0)
            c.wait_until("copies")
            new = [Mono("0", 48, GREEN).move_to(d) for d in digs]
            anims = []
            for o, n in zip(digs, new):
                anims += swap(o, n)
            self.play(*anims, *[time_span(FlashAround(n, color=GREEN, time_width=1.5), 0.6, 1.6) for n in new],
                      run_time=1.6)
            self.digs = digs = new
            c.wait_until("same")

            # the next state: all zeros again
            self.play(*during([lab.animate.shift(short_dx * LEFT), d1.animate.shift(short_dx * LEFT)], 0, 0.5),
                      *during(appear(arr, d2, lag=0.3, shift=None), 0.5, 1), run_time=1.6)
            self.play(FlashAround(d2, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("forever")

            # two more edges, faster
            for _ in range(2):
                self.play(*self.ticks(1.2, dur=1.2), *self.tokens(0.1, 1.2),
                          time_span(FlashAround(d2, color=YELLOW, time_width=1.5), 1.2, 1.9),
                          *[time_span(FlashAround(d, color=GREEN, time_width=1.5), 1.2, 1.9) for d in digs],
                          *[time_span(UpdateFromAlphaFunc(d, self._dip), 0, 1.25) for d in digs],
                          run_time=1.9)
            c.wait_until()

    # -- c3.stuck.3: the table has no row for 00000 -------------------------------------------------
    def clip3(self):
        rl, digs = self.rl, self.digs
        lab, d1, arr, d2 = self.rd
        tab = _S5.ring_table(center=TAB_C)
        unused = T("Unused states. Lots!", 32, DIM).move_to(_p(TAB_C[0], -2.85))
        with self.say("c3.stuck.3") as c:
            grp = VGroup(rl, *digs)
            s = SMALL_W / grp.width
            pivot = grp.get_center()
            shift = SMALL_C - pivot
            moves = [rl.animate.scale(s, about_point=pivot).shift(shift)]
            for d in digs:
                d.generate_target()
                d.target.scale(s, about_point=pivot).shift(shift).scale(1.45).shift(0.14 * DOWN)
                moves.append(MoveToTarget(d))
            rows = [VGroup(*tab.cur[k], *tab.nxt[k]) for k in range(5)]
            self.play(*during(disappear(lab, d1, arr, d2), 0, 0.3),
                      *during(moves, 0, 0.5),
                      *during(appear(VGroup(tab.titles, tab.head_l, tab.head_r, tab.hline, tab.vline),
                                     *rows, unused, lag=0.12, shift=None), 0.45, 1),  # early: the table, shown whole
                      run_time=min(2.6, c.until("rows")))
            c.wait_until("rows")

            # each row: two 1s side by side
            flashes = []
            for k in range(5):
                for j, ch in enumerate(RING_STATES[k]):
                    if ch == "1":
                        flashes.append(time_span(FlashAround(tab.cur[k][j], color=GOLD, time_width=1.5),
                                                 0.5 * k, 0.5 * k + 1.2))
            self.play(*flashes, run_time=min(3.2, c.until("missing")))
            c.wait_until("missing")

            # 00000 looks for its row
            dr = VGroup(Mono("00000", 40, DIM), T("→", 40, DIM), T("?", 48, RED)).arrange(RIGHT, buff=0.22)
            dr[1].match_y(dr[0])
            dr.move_to(_p(DIMROW_X, tab.row_y(0)))
            self.play(*appear(dr, shift=0.25 * RIGHT), run_time=1.0)
            self.wait(0.4)
            for k in range(1, 5):
                self.play(dr.animate.move_to(_p(DIMROW_X, tab.row_y(k))), run_time=0.7)
                self.wait(0.35)
            self.play(dr.animate.move_to(_p(DIMROW_X, -2.75)), run_time=0.8)
            self.play(FlashAround(dr[2], color=RED, time_width=1.5), run_time=1.2)
            c.wait_until("nothing")

            ticks = [check_mark().move_to(_p(6.3, tab.row_y(k))) for k in range(5)]
            self.play(*appear(*ticks, lag=0.2, shift=None), run_time=1.6)
            c.wait_until()
