"""Chapter 3, scene 8: recap in six panels on a 3 x 2 grid, then a teaser for one-hot. Clips c3.recap.1 – c3.recap.3.

Layout as ch2_s8_recap (its slot_frame / vis_center / fit / caption / veil are imported): "Recap" T 40
at (0, 3.4), six faint DIM slot frames, each panel's picture fitted into its slot, its line (T 28) under it,
earlier panels dimmed under a BG veil.
 r1 s1's handover shot (ring_leds + wave_panel), the flat output drawn under ticking CLK;
 r2 s2's five GREEN 0s, a YELLOW clock-edge arrow, five GREEN 0s again;
 r3 s3's remedy_cards(); r4 s4's check_rings(arrows=True); r5 s5's eight loops (in two rows of four);
 r6 a D flip-flop with s6's pin(ff, "S") (bubble), its level 1 -> 0 -> 1, beside s1's ghost_wave((0,0,1,1,0))
 with s7's solid output traced over it.
{next}: the grid sweeps away; eight flip-flops in a row, one GOLD LED lit, stepping on each CLK tick;
"one flip-flop per state" and, on {real}, a GREEN "used for real" pill.
End card (handover to ch4 s1): end_card() = the row with LED 0 lit + "Part 4 · One-hot" T 40 at (0, 3.2).
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

G2 = load_scene("ch2_s8_recap")          # the recap grid
S1 = load_scene("ch3_s1_hook")
P3 = load_scene("ch3_s3_powerup")
C4 = load_scene("ch3_s4_check")
L5 = load_scene("ch3_s5_loops")
P6 = load_scene("ch3_s6_preset")
N6 = load_scene("ch2_s6_nologic")        # make_ff
slot, slot_frame, vis_center, fit, caption, veil = (G2.slot, G2.slot_frame, G2.vis_center, G2.fit,
                                                    G2.caption, G2.veil)
COL_X = G2.COL_X


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the eight-flip-flop row and the end card (ch4 s1 opens on end_card()) -------------------------
FF8_N, FF8_PITCH = 8, 1.55
FF8_W, FF8_H, FF8_Y = 0.95, 1.3, 0.15
LED8_Y, LED8_R = 1.5, 0.26
BUS8_Y = -1.05
END_LIT = 0


def led8(on):
    c = Circle(radius=LED8_R)
    return set_led8(c, on)


def set_led8(c, on):
    if on:
        return c.set_stroke(GOLD, 3).set_fill(GOLD, 0.9)
    return c.set_stroke(DIM, 3).set_fill(BG, 0)


def ff8_row(lit=END_LIT):
    """Eight flip-flops side by side, a LED above each (only `lit` on, GOLD), a common CLK bus below.
    .boxes .leds .bus .clk_l .lit"""
    xs = [(k - (FF8_N - 1) / 2) * FF8_PITCH for k in range(FF8_N)]
    boxes, tris, stubs, leds, pins, dots = [], [], [], [], [], []
    hb = FF8_Y - FF8_H / 2
    for k, x in enumerate(xs):
        boxes.append(Rectangle(width=FF8_W, height=FF8_H).set_stroke(FG, 4).move_to(_p(x, FF8_Y)))
        tris.append(Polygon(_p(x - 0.15, hb), _p(x + 0.15, hb), _p(x, hb + 0.22)).set_stroke(FG, 3)
                    .set_fill(BG, 1))
        stubs.append(Line(_p(x, FF8_Y + FF8_H / 2), _p(x, LED8_Y - LED8_R)).set_stroke(FG, 4))
        leds.append(led8(k == lit).move_to(_p(x, LED8_Y)))
        pins.append(Line(_p(x, BUS8_Y), _p(x, hb)).set_stroke(YELLOW, 4))
        if k < FF8_N - 1:
            dots.append(Dot(_p(x, BUS8_Y), radius=0.07, color=YELLOW))
    bus = Line(_p(xs[0] - 0.85, BUS8_Y), _p(xs[-1], BUS8_Y)).set_stroke(YELLOW, 4)
    clk_l = T("CLK", 30, YELLOW).next_to(bus.get_left(), DOWN, buff=0.15).align_to(bus, LEFT)
    g = VGroup(bus, *pins, *dots, *boxes, *tris, *stubs, *leds, clk_l)
    g.boxes, g.leds, g.bus, g.pins, g.clk_l, g.lit = boxes, leds, bus, pins, clk_l, lit
    return g


def part4_line():
    return T("Part 4 · One-hot", 40).move_to(_p(0, 3.2))


def end_card():
    """ch3's last frame: the eight-flip-flop row (LED END_LIT lit) under "Part 4 · One-hot"."""
    row = ff8_row(END_LIT)
    part = part4_line()
    g = VGroup(row, part)
    g.row, g.part = row, part
    return g


def handover_shot():
    return end_card()


# ---- r6: s7's output wave (b, pattern 0 0 1 1 0) drawn solid over s1's ghost --------------------------
def solid_wave(pattern=(0, 0, 1, 1, 0)):
    x = lambda j: S1.W_X0 + j * S1.W_P  # noqa: E731
    lev = lambda b: S1.W_OUT_Y + (S1.W_H / 2 if b else -S1.W_H / 2)  # noqa: E731
    pts = []
    for j in range(S1.W_N):
        b = pattern[j % 5]
        pts += [_p(x(j), lev(b)), _p(x(j + 1), lev(b))]
    return VMobject().set_points_as_corners(pts).set_stroke(GREEN, 4)


class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.end()

    def dim_previous(self):
        out = []
        for t in self.panels:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    @staticmethod
    def flashes(paths, rt, period, width=0.6):
        out, t = [], 0.0
        while t + width <= rt + 1e-6:
            out += [time_span(VShowPassingFlash(m.copy(), time_width=0.6), t, t + width) for m in paths]
            t += period
        return out

    # -- c3.recap.1: r1 flat output, r2 zeros shift zeros, r3 the three remedies --------------------
    def clip1(self):
        with self.say("c3.recap.1") as c:
            head = T("Recap", 40).move_to(_p(0, 3.4))
            frames = [slot_frame(i) for i in range(6)]
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames],
                      run_time=min(1.2, c.until("r1")))  # early: the scene's heading

            # r1: the ring of five with its LEDs; under ticking CLK the output stays flat
            c.wait_until("r1")
            shot = S1.handover_shot()
            fit(shot, vis_center(0))
            rl, pn = shot[0], shot[1]
            cap1 = caption(0, ["switched on,", "it sat at 0"])
            self.play(FadeIn(rl), FadeIn(pn.labels), *[FadeIn(p) for p in pn.clk_pieces],
                      *appear(cap1, shift=None), run_time=1.0)
            rt = max(1.2, min(2.2, c.until("r2") - 0.2))
            n = len(pn.out_pieces)
            dt = rt / n
            self.play(*[time_span(Create(o, rate_func=linear), j * dt, (j + 1) * dt)
                        for j, o in enumerate(pn.out_pieces)],
                      *self.flashes(rl.clk_paths(width=4), rt, rt / 3), run_time=rt)
            self.panels.append(VGroup(shot, cap1))

            # r2: all zeros; one clock edge shifts zeros into zeros
            c.wait_until("r2")
            x, vc = COL_X[1], vis_center(1)
            xs = [x - 0.35 + (k - 2) * 0.55 for k in range(5)]
            top = [Mono("0", 40, GREEN).move_to(_p(xx, vc[1] + 0.6)) for xx in xs]
            bot = [Mono("0", 40, GREEN).move_to(_p(xx, vc[1] - 0.6)) for xx in xs]
            ax = x + 1.45
            edge = Arrow(_p(ax, vc[1] + 0.55), _p(ax, vc[1] - 0.55), buff=0, color=YELLOW, stroke_width=4,
                         tip_length=0.2, max_tip_length_to_length_ratio=0.3)
            tick = S1.clk_period(0, 0, p=0.5, h=0.3).move_to(_p(ax - 0.42, vc[1]))
            cap2 = caption(1, ["00000 → 00000"], t2c={"00000": GREEN})
            self.play(*self.dim_previous(), *appear(*top, lag=0.1, shift=None), run_time=1.0)
            c.wait_until("a ring of zeros")
            self.play(GrowArrow(edge), FadeIn(tick), run_time=0.8)
            c.wait_until("shifts zeros")
            self.play(*appear(*bot, shift=0.45 * DOWN, lag=0.1), *during(appear(cap2, shift=None), 0.6, 1.0),
                      run_time=max(1.4, min(1.6, c.until("r3"))))
            self.panels.append(VGroup(*top, *bot, edge, tick, cap2))

            # r3: the three remedies, each lit on its phrase
            c.wait_until("r3")
            cards = P3.remedy_cards()
            fit(cards, vis_center(2))
            cap3 = caption(2, ["check · add logic ·", "set a used state"])
            self.play(*self.dim_previous(), FadeIn(cards), run_time=1.0)  # early: the three cards, shown whole then walked
            for i, cue in enumerate(("check", "add logic", "force")):
                c.wait_until(cue)
                self.play(FlashAround(cards.cards[i], time_width=1.5), cards.cards[i].box.animate.set_stroke(GOLD),
                          run_time=min(1.2, c.until(floor=0.6)))
            self.play(*appear(cap3, shift=None), run_time=min(1.0, c.until(floor=0.5)))
            self.panels.append(VGroup(cards, cap3))

    # -- c3.recap.2: r4 the counters find their way back, r5 eight loops, r6 the set pin ---------------
    def clip2(self):
        with self.say("c3.recap.2") as c:
            # r4: the two rings with their unused states and escape arrows
            g = C4.check_rings(arrows=True)
            fit(g, vis_center(3) + 0.1 * UP, h=1.8)
            cap4 = caption(3, ["self-starting", "(by luck)"])
            ins = []
            for cr in g:
                ins += [FadeIn(cr.ring)] + [FadeIn(u) for u in cr.unused.values()]
            self.play(*self.dim_previous(), *ins, run_time=1.0)  # early: the panel's rings, shown whole
            c.wait_until("find their way back")
            esc = [e for cr in g for e in cr.esc]
            self.play(*[time_span(GrowArrow(e), 0.15 * i, 0.15 * i + 0.8) for i, e in enumerate(esc)],
                      run_time=0.15 * (len(esc) - 1) + 0.8)
            c.wait_until("self-starting")
            self.play(*appear(cap4, shift=None), run_time=min(1.0, c.until("r5", floor=0.5)))
            self.panels.append(VGroup(g, cap4))

            # r5: the eight loops, ours GREEN
            c.wait_until("r5")
            lr = L5.loops_row()
            for k, icon in enumerate(lr.loops):
                cur = _p((k - 3.5) * 1.6, 0.6)
                tgt = _p((k % 4 - 1.5) * 1.6, 0.0 if k < 4 else -2.0)
                icon.shift(tgt - cur)
            fit(lr, vis_center(4))
            cap5 = caption(4, ["8 loops, 1 ours"], t2c={"8": GOLD, "1": GOLD})
            self.play(*self.dim_previous(), *appear(*lr.loops, lag=0.15, shift=None),  # early: the loops, shown whole
                      run_time=min(1.8, c.until("thirty-two", floor=1.0)))
            c.wait_until("only one")
            self.play(FlashAround(lr.ours, color=GREEN, time_width=1.5), *appear(cap5, shift=None),
                      run_time=min(1.2, c.until("r6", floor=0.6)))
            self.panels.append(VGroup(lr, cap5))

            # r6: active-low set pin, pulsed; the ring runs
            c.wait_until("r6")
            x, vc = COL_X[2], vis_center(5)
            ff = N6.make_ff(ORIGIN, size=40)
            sp = P6.pin(ff, "S", size=40)
            fg = VGroup(ff, sp)
            fit(fg, _p(x - 1.25, vc[1] - 0.15), w=1.3, h=1.75)
            lvl = value_label("1", 30, GOLD).next_to(sp.wire, LEFT, buff=0.12)
            ghost = S1.ghost_wave((0, 0, 1, 1, 0))
            solid = solid_wave()
            wv = VGroup(ghost, solid)
            wv.scale_to_fit_width(2.35).stretch_to_fit_height(0.55).move_to(_p(x + 0.7, vc[1] - 0.15))
            cap6 = caption(5, ["active-low set:", "start used"])
            self.play(*self.dim_previous(), FadeIn(fg), FadeIn(ghost), *appear(cap6, shift=None),  # early: the panel's flip-flop and line, shown whole
                      run_time=1.0)
            self.play(*appear(lvl, shift=None), run_time=0.6)
            c.wait_until("forced")
            lvl0 = value_label("0", 30, RED).move_to(lvl)
            self.play(*swap(lvl, lvl0), FlashAround(sp.bub, color=RED, time_width=1.5), run_time=1.0)
            c.wait_until("set inputs")
            lvl1 = value_label("1", 30, GOLD).move_to(lvl)
            self.play(*swap(lvl0, lvl1), run_time=min(0.9, c.until("and it ran", floor=0.6)))
            c.wait_until("and it ran")
            self.play(Create(solid, rate_func=linear), run_time=min(1.6, c.until(floor=0.8)))
            self.panels.append(VGroup(fg, lvl1, wv, cap6))

    # -- c3.recap.3: next time, one flip-flop per state --------------------------------------------
    def step(self):
        row = self.row
        old, new = row.lit, (row.lit + 1) % FF8_N
        row.lit = new
        paths = [row.bus.copy().set_stroke(YELLOW, 8)] + [p.copy().set_stroke(YELLOW, 8) for p in row.pins]
        return (during([VShowPassingFlash(p, time_width=0.6) for p in paths], 0, 0.5)
                + during([set_led8(row.leds[old].animate, False), set_led8(row.leds[new].animate, True)], 0.35, 0.8))

    def clip3(self):
        with self.say("c3.recap.3") as c:
            row = self.row = ff8_row(0)
            # the whole grid fades together (no lag), then the row arrives
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.5),
                      *during([FadeIn(row)], 0.5, 1.0), run_time=1.4)
            cap = self.cap = T("one flip-flop per state", 36).move_to(_p(-1.6, -2.45))
            pill_t = T("used for real", 32, GREEN)
            pill_b = RoundedRectangle(corner_radius=0.22, width=pill_t.width + 0.5, height=0.66)
            pill_b.set_stroke(GREEN, 2.5).set_fill(BG, 1)
            pill_t.move_to(pill_b)
            tag = self.tag = VGroup(pill_b, pill_t).next_to(cap, RIGHT, buff=0.6)
            c.wait_until("one flip-flop")
            self.play(*appear(cap, shift=None), *self.step(), run_time=1.2)
            c.wait_until("real")
            self.play(*appear(tag, shift=None), *self.step(), run_time=min(1.2, c.until(floor=0.8)))
            self.play(*self.step(), run_time=min(1.1, max(0.8, c.until())))

    # -- end card: the light keeps stepping; "Part 4 · One-hot" -------------------------------------
    def end(self):
        part = part4_line()
        self.play(*appear(part), *self.step(), run_time=1.3)
        self.play(*self.step(), run_time=1.3)
        self.wait(0.6)
        self.play(*disappear(self.cap, self.tag), *self.step(), run_time=1.3)
        self.play(*self.step(), run_time=1.3)
        self.wait(0.6)
        self.play(*self.step(), run_time=1.3)
        assert self.row.lit == END_LIT
        self.wait(1.2)                     # handover: ch4 s1 opens on end_card()
