"""Chapter 3, scene 5: the ring's trap: rotation keeps the pattern, 32 states split into eight loops,
seven of them traps; the ring can't self-start. Clips c3.loops.1 – c3.loops.4.

Shared (s8 reuses the eight loops):
  LOOPS                 the eight loops' first patterns (e d c b a), OURS = "00011".
  loop_icon(p, r, color, size)  one loop: a circle of five dots with a ▼ (or, for 00000 / 11111, one
                        dot with a self-arrow), its Mono label below (1s GOLD). Built with the circle's
                        centre at ORIGIN; .shape .label .path (circle / self-arc, for flashes).
  loops_row(y, r, size, pitch)  the eight loops side by side, OURS GREEN, the seven others RED;
                        .loops[k], .ours.
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

_RING = load_scene("ch2_s5_ring")
_HOOK = load_scene("ch3_s1_hook")
_POWER = load_scene("ch3_s3_powerup")
ring_circle, cell_bit, RING_STATES = _RING.ring_circle, _RING.cell_bit, _RING.RING_STATES


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the eight loops (shared with s8) -------------------------------------------------------------
LOOPS = ["00000", "11111", "00001", "00011", "00101", "00111", "01011", "01111"]
OURS = "00011"


def _ang(k, n=5):
    a = PI / 2 - TAU * k / n
    return np.array([np.cos(a), np.sin(a), 0.0])


def loop_icon(pattern, r=0.42, color=BLUE, size=28):
    if pattern in ("00000", "11111"):
        dot = Dot(_p(0, -0.65 * r), radius=0.09, color=color)
        arc = Arc(radius=0.75 * r, start_angle=-PI / 2 + 0.5, angle=TAU - 1.0, arc_center=_p(0, 0.1 * r))
        arc.set_stroke(color, 3)
        arc.add_tip(tip_length=0.14, tip_width=0.14)
        arc.get_tip().set_fill(color, 1).set_stroke(color, 1)
        shape = VGroup(arc, dot)
        path = Arc(radius=0.75 * r, start_angle=-PI / 2 + 0.5, angle=TAU - 1.0, arc_center=_p(0, 0.1 * r))
    else:
        circ = Circle(radius=r).set_stroke(color, 3)
        dots = [Dot(r * _ang(k), radius=0.075, color=color) for k in range(5)]
        tip = Triangle().scale(0.085).rotate(PI).set_stroke(width=0).set_fill(color, 1).move_to(_p(r, 0))
        shape = VGroup(circ, *dots, tip)
        path = Circle(radius=r)
    label = Mono(pattern, size, t2c={"1": GOLD})
    label.move_to(_p(0, -r - 0.2 - label.height / 2))
    g = VGroup(shape, label)
    g.shape, g.label, g.path, g.pattern = shape, label, path, pattern
    return g


def place(icon, pos):
    """Shift an icon (built at ORIGIN) so its circle centre sits at pos; the path goes with it."""
    icon.shift(pos)
    icon.path.shift(pos)
    return icon


def loops_row(y=0.6, r=0.55, size=30, pitch=1.6):
    loops = []
    for k, p in enumerate(LOOPS):
        col = GREEN if p == OURS else RED
        loops.append(place(loop_icon(p, r, col, size), _p((k - 3.5) * pitch, y)))
    g = VGroup(*loops)
    g.loops, g.ours = loops, loops[LOOPS.index(OURS)]
    return g


def big_loop(center=_p(0, -0.6), R=1.9, size=36):
    """The GREEN loop opened up: its five codes round a circle, ▼ between them."""
    center = np.array(center, dtype=float)
    circ = Circle(radius=R).set_stroke(GREEN, 3).move_to(center)
    codes, bgs, tips = [], [], []
    for k, s in enumerate(RING_STATES):
        code = Mono(s, size, t2c={"1": GOLD}).move_to(center + R * _ang(k))
        bgs.append(BackgroundRectangle(code, color=BG, fill_opacity=1, buff=0.1))
        codes.append(code)
        a = PI / 2 - TAU * (k + 0.5) / 5
        t = Triangle().scale(0.1).set_stroke(width=0).set_fill(GREEN, 1)
        t.rotate(a - PI)   # point clockwise (tangent at a - 90°)
        t.move_to(center + R * np.array([np.cos(a), np.sin(a), 0]))
        tips.append(t)
    ring = VGroup(circ, *tips)
    g = VGroup(ring, *bgs, *codes)
    g.ring, g.codes, g.bgs, g.circ = ring, codes, bgs, circ
    return g


# ---- clip 1: the ring of five -------------------------------------------------------------------
RC = _p(-3.5, 0.0)
RX = [1.4 + 0.75 * j for j in range(5)]           # readout columns e d c b a
RY_HEAD, RY = 1.55, [0.6, -0.35, -1.3]

# ---- clip 3: the wave panel ---------------------------------------------------------------------
PX0, PP, PN, PH = -3.7, 0.82, 10, 0.62
PLAB_X = -4.2
CLK_Y = 1.45
ROW_Y = {"00000": 0.3, "11111": -0.85, "00101": -2.0}
WANT_Y = -3.15
CROSS_X = 5.1


def wave_pts(pattern, y, x0=PX0, p=PP, n=PN, h=PH):
    lev = lambda b: y + (h / 2 if b else -h / 2)  # noqa: E731
    pts = []
    for j in range(n):
        b = pattern[j % len(pattern)]
        pts += [_p(x0 + j * p, lev(b)), _p(x0 + (j + 1) * p, lev(b))]
    return pts


def out_wave(pattern, y):
    return VMobject().set_points_as_corners(wave_pts(pattern, y)).set_stroke(GREEN, 4)


def rails(y):
    """Faint DIM guides at a row's 0 and 1 levels, so a flat line reads as 0 or 1."""
    return VGroup(*[DashedLine(_p(PX0, y + d), _p(PX0 + PN * PP, y + d), dash_length=0.08)
                    .set_stroke(DIM, 1.5, opacity=0.6) for d in (-PH / 2, PH / 2)],
                  *[T(v, 28, DIM).move_to(_p(PX0 - 0.22, y + d)) for v, d in (("0", -PH / 2), ("1", PH / 2))])


def card_word(card, key):
    """Glyphs of key on a remedy card, indexed without spaces (Text has no space glyphs)."""
    for ln in card.lines:
        flat = ln.text.replace(" ", "")
        k = key.replace(" ", "")
        if k in flat:
            i = flat.index(k)
            return VGroup(*ln[i:i + len(k)])
    raise ValueError(key)


def wanted_wave(y):
    path = VMobject().set_points_as_corners(wave_pts((1, 1, 0, 0, 0), y))
    return DashedVMobject(path, num_dashes=70, dashed_ratio=0.55).set_stroke(GREEN, 3, opacity=0.6)


class Loops(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c3.loops.1: the ring rotates its pattern ------------------------------------------------
    def readout_row(self, edcba, y):
        return VGroup(*[cell_bit(b, 48).move_to(_p(RX[j], y)) for j, b in enumerate(edcba)])

    def step(self, rt):
        ring, digs, bits = self.ring, self.digs, self.bits
        new_bits = bits[-1] + bits[:-1]          # a..e: a' = e, b' = a, ...
        anims = [d.animate(path_arc=-TAU / 5).move_to(ring.pos((i + 1) % 5)) for i, d in enumerate(digs)]
        for i, b in enumerate(ring.boxes):
            anims.append(b.animate.set_fill(GOLD, 0.22) if new_bits[i] == "1" else b.animate.set_fill(BG, 1))
        anims.append(VShowPassingFlash(ring.close.copy().set_stroke(YELLOW, 8), time_width=0.8))
        self.play(*anims, run_time=rt)
        self.digs = [digs[(i - 1) % 5] for i in range(5)]
        self.bits = new_bits

    def clip1(self):
        self.bits = "10100"                         # a..e: pattern 00101 (e d c b a)
        ring = ring_circle(RC, R=2.1, bits=self.bits)
        self.ring, self.digs = ring, list(ring.digits)
        head = VGroup(*[T(ch, 36, color=GREEN).move_to(_p(RX[j], RY_HEAD)) for j, ch in enumerate("edcba")])
        rows = [self.readout_row(self.bits[::-1], RY[0])]
        with self.say("c3.loops.1") as c:
            self.play(FadeIn(ring), run_time=1.4)
            self.play(*appear(head, rows[0], lag=0.4), run_time=1.0)  # early: the readout header, read whole
            c.wait_until("think about what a ring does")
            self.play(*[VShowPassingFlash(a.copy().set_stroke(YELLOW, 8), time_width=0.8)
                        for a in ring.arrows + [ring.close]], run_time=1.5)
            c.wait_until("rotate")
            self.step(min(1.8, c.until("wraps round")))
            rows.append(self.readout_row(self.bits[::-1], RY[1]))
            self.play(*appear(rows[1]), run_time=0.9)
            c.wait_until("wraps round")
            self.step(1.6)
            rows.append(self.readout_row(self.bits[::-1], RY[2]))
            self.play(*appear(rows[2]), run_time=0.9)
            c.wait_until("same")
            cap = T("same pattern, moved round", 36).move_to(_p(np.mean([RX[0], RX[-1]]), -2.5))
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("only moves round")
            ones = [r[j] for r in rows for j in range(5) if r[j].text == "1"]
            self.play(*flash(ones, color=GOLD, run_time=1.6, time_width=1.5))
            c.wait_until("the number of ones")
            ring_ones = [d for d in self.digs if d.text == "1"]
            self.play(*flash(ring_ones, color=GOLD, run_time=1.6, time_width=1.5))
        self.c1_cap = cap

    # -- c3.loops.2: eight loops, one ours ----------------------------------------------------------
    def clip2(self):
        grid_pos = [_p(-4.8 + 3.2 * (k % 4), 1.3 if k < 4 else -1.6) for k in range(8)]
        icons = [place(loop_icon(p, 0.8, BLUE, 32), grid_pos[k]) for k, p in enumerate(LOOPS)]
        self.icons = icons
        with self.say("c3.loops.2") as c:
            sweep_clear(self, *appear(*icons, shift=None, lag=0.15), run_time=2.2)
            c.wait_until("single")
            singles, fives = icons[:2], icons[2:]
            self.play(*set_alpha(fives, DIMMED), *flash([i.shape for i in singles], run_time=1.4),
                      run_time=1.4)
            c.wait_until("five")
            self.play(*set_alpha(fives, 1), *set_alpha(singles, DIMMED), run_time=1.0)
            self.play(*flash([i.shape for i in fives], run_time=1.4, time_width=1.5))
            c.wait_until("count")
            count = T("8 loops", 48, GOLD).move_to(_p(0, 3.3))
            self.play(*set_alpha(singles, 1), *appear(count), run_time=1.0)
            c.wait_until("ours")
            ours = icons[LOOPS.index(OURS)]
            self.play(ours.shape.animate.set_color(GREEN), *flash([ours.shape], color=GREEN, run_time=1.2),
                      run_time=1.2)
            c.wait_until("two ones side by side")
            self.row_pos = [_p(-5.6 + 1.6 * k, 3.0) for k in range(8)]
            targets = []
            for k, p in enumerate(LOOPS):
                t = place(loop_icon(p, 0.42, GREEN if p == OURS else BLUE, 28), self.row_pos[k])
                targets.append(t)
            top = [Transform(icons[k], targets[k]) for k in range(4)]
            bottom = [Transform(icons[k], targets[k]) for k in range(4, 8)]
            for k in range(8):
                icons[k].path = targets[k].path
            self.play(*during(disappear(count), 0, 0.3), *during(top, 0.2, 0.65), *during(bottom, 0.55, 1.0),
                      run_time=1.6)
            big = big_loop()
            self.play(TransformFromCopy(ours.shape, big.ring),
                      *during(appear(*[VGroup(big.bgs[k], big.codes[k]) for k in range(5)],
                                     shift=None, lag=0.2), 0.3, 1.0),
                      run_time=min(1.8, c.until("trap")))
            self.remove(big.ring, *big.bgs, *big.codes)
            self.add(big)
            self.big = big
            c.wait_until("trap")
            others = [i.shape for i in icons if i.pattern != OURS]
            self.play(*[s.animate.set_color(RED) for s in others], run_time=min(1.2, c.until(floor=0.6)))

    # -- c3.loops.3: each trap's output ------------------------------------------------------------
    def clip3(self):
        icons = self.icons
        by = {i.pattern: i for i in icons}
        clk = VGroup(*[_HOOK.clk_period(PX0 + j * PP, CLK_Y, p=PP, h=PH) for j in range(PN)])
        clk_l = T("CLK", 32, YELLOW).next_to(_p(PLAB_X, CLK_Y), LEFT, buff=0)
        with self.say("c3.loops.3") as c:
            others = [i.shape for i in icons if i.pattern != OURS]
            self.play(*flash(others, color=RED, run_time=1.4))
            c.wait_until("all zeros gives")
            self.play(*during(disappear(self.big), 0, 0.5), *during(appear(clk, clk_l, shift=None), 0.4, 1.0),
                      run_time=1.2)
            rows = {}
            for key, cue in (("00000", "all zeros gives"), ("11111", "and all ones")):
                c.wait_until(cue)
                lab = Mono(key, 30, t2c={"1": GOLD}).next_to(_p(PLAB_X, ROW_Y[key]), LEFT, buff=0)
                wave = out_wave((int(key[3]),), ROW_Y[key])
                self.play(FlashAround(by[key].label, color=RED, run_time=1.4), *appear(lab, rails(ROW_Y[key]), shift=None),
                          *during([Create(wave)], 0.35, 1.0), run_time=1.4)
                x = cross_mark().move_to(_p(CROSS_X, ROW_Y[key]))
                self.play(*appear(x, shift=None), run_time=0.6)
                rows[key] = VGroup(lab, wave, x)
            c.wait_until("apart")
            self.play(*flash([by["00101"].shape], color=RED, run_time=1.4))
            c.wait_until("take two ones")
            key = "00101"
            lab = Mono("10010", 30, t2c={"1": GOLD}).next_to(_p(PLAB_X, ROW_Y[key]), LEFT, buff=0)
            want_l = T("wanted", 30, GREEN).next_to(_p(PLAB_X, WANT_Y), LEFT, buff=0)
            want = wanted_wave(WANT_Y)
            self.play(FlashAround(by[key].label, color=RED, run_time=1.2), *appear(lab, rails(ROW_Y[key]), shift=None),
                      run_time=1.2)
            self.play(*appear(want_l, shift=None), FadeIn(want), run_time=1.0)
            c.wait_until("the output goes high")
            wave = out_wave((1, 0, 1, 0, 0), ROW_Y[key])
            self.play(Create(wave), run_time=min(4.5, c.until("then low for two") + 1.0), rate_func=linear)
            x3 = cross_mark().move_to(_p(CROSS_X, ROW_Y[key]))
            self.play(*appear(x3, shift=None), run_time=min(0.6, c.until("exactly")))
            c.wait_until("exactly")
            big = big_loop()
            sweep_clear(self, FadeIn(big), keep=icons, run_time=1.4)
            unders = []
            for code in big.codes:
                s = code.text
                ones = [j for j, ch in enumerate(s) if ch == "1"]
                if ones[1] - ones[0] == 1:
                    unders.append(underline(VGroup(code[ones[0]], code[ones[1]]), GOLD, buff=0.1))
                else:
                    unders += [underline(code[j], GOLD, buff=0.1) for j in ones]
            self.play(*[GrowFromCenter(u) for u in unders], run_time=1.0)
            wrap_code = next(cd for cd in big.codes if cd.text == "10001")
            lo = wrap_code.get_bottom()[1] - 0.22
            wrap = ArcBetweenPoints(_p(wrap_code[4].get_x(), lo), _p(wrap_code[0].get_x(), lo), angle=-PI / 2)
            wrap.set_stroke(GOLD, 3).add_tip(tip_length=0.14, tip_width=0.14)
            wrap.get_tip().set_fill(GOLD, 1).set_stroke(GOLD, 1)
            self.play(Create(wrap), run_time=0.8)
            unders.append(wrap)
            cap = T("exactly two 1s, side by side", 36).move_to(_p(0, -3.3))
            self.play(*appear(cap), run_time=min(1.0, c.until(floor=0.5)))
            self.big, self.unders, self.cap2 = big, unders, cap

    # -- c3.loops.4: no way out; the remedies ------------------------------------------------------
    def clip4(self):
        icons = self.icons
        row = loops_row(y=1.1)
        with self.say("c3.loops.4") as c:
            anims = []
            for k in range(8):
                anims.append(Transform(icons[k], row.loops[k]))
                icons[k].path = row.loops[k].path
            cap = T("27 unused states: none reaches a used state", 36).move_to(_p(0, -0.9))
            self.play(*during(disappear(self.big, *self.unders, self.cap2), 0, 0.4), *during(anims, 0.3, 0.8),
                      *during(appear(cap), 0.6, 1.0), run_time=2.2)
            c.wait_until("ever reaches")
            self.play(*[VShowPassingFlash(i.path.copy().set_stroke(GREEN if i.pattern == OURS else RED, 8),
                                          time_width=0.6) for i in icons], run_time=1.8)
            c.wait_until("can never start")
            self.play(*flash([cap], color=RED, run_time=1.6, time_width=1.5))

            c.wait_until("two")
            board = _POWER.remedy_cards().move_to(_p(0, 0.55))
            cards = board.cards
            sweep_clear(self, *appear(board, shift=None), run_time=1.6)  # early: s3's cards, read whole
            self.play(*set_alpha([cards[0]], 0.4), cards[1].box.animate.set_stroke(YELLOW, 4),
                      run_time=min(1.0, c.until("whole point")))
            c.wait_until("whole point")
            x = Cross(cards[1].box, stroke_color=RED, stroke_width=6, scale_factor=0.8)
            note = T("the ring's point: no logic", 36, RED).move_to(_p(0, -2.35))
            self.play(Create(x), cards[1].box.animate.set_stroke(RED, 4), *appear(note), run_time=1.2)
            c.wait_until("three")
            self.play(*set_alpha([cards[1], x], 0.4), cards[2].box.animate.set_stroke(YELLOW, 4),
                      run_time=1.2)
            c.wait_until("by force")
            self.play(*recolor(card_word(cards[2], "Clear"), YELLOW), *recolor(card_word(cards[2], "Preset"), YELLOW),
                      run_time=1.2)
