"""Chapter 4, scene 1: hook: from ch3's rescued ring to one-hot vs binary for eight states. Clips c4.hook.1 – c4.hook.2.
Opens exactly on ch3_s8_recap's end_card(); its part line travels into the title card.

Shared (standalone, ch4 s2 and s8 import them; s3 builds its cells in the same style):
  hot_bit(b, size)          a cell's digit: GOLD 1 or GREEN 0.
  cell_box(bit, side)       BLUE rounded square, faintly GOLD-filled when it holds a 1.
  onehot_row(n=8, hot=0)    n cells in a row on one YELLOW CLK line (stubs up to each cell), a DIM
                            wrap arrow over the top from the last cell back to the first; centred
                            on ORIGIN. .boxes .digits .clk .stubs .clk_label .wrap .pos(i) .side
  binary_trio(bits="000")   three cells reading `bits`, centred on ORIGIN. .boxes .digits .pos(i) .side
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
from lib.titles import title_card  # noqa: E402

S5 = load_scene("ch2_s5_ring")


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- shared helpers
CELL_SIDE = 0.9
CELL_PITCH = 1.05
BIT_SIZE = 44


def hot_bit(b, size=BIT_SIZE):
    return Mono("1", size, color=GOLD) if int(b) else Mono("0", size, color=GREEN)


def cell_box(bit, side=CELL_SIDE):
    b = RoundedRectangle(corner_radius=0.1, width=side, height=side)
    return S5.ring_cell_style(b, bit)


def _cells(bits, side, pitch):
    n = len(bits)
    pos = [_p((i - (n - 1) / 2) * pitch, 0) for i in range(n)]
    boxes = [cell_box(bits[i], side).move_to(pos[i]) for i in range(n)]
    digits = [hot_bit(bits[i]).move_to(pos[i]) for i in range(n)]
    return pos, boxes, digits


def onehot_row(n=8, hot=0, side=CELL_SIDE, pitch=CELL_PITCH):
    bits = [1 if i == hot else 0 for i in range(n)]
    pos, boxes, digits = _cells(bits, side, pitch)
    y_clk = -side / 2 - 0.45
    x0, x1 = pos[0][0] - side / 2 - 0.25, pos[-1][0] + side / 2 + 0.1
    clk = Line(_p(x0, y_clk), _p(x1, y_clk)).set_stroke(YELLOW, 4)
    stubs = [Line(_p(p[0], y_clk), _p(p[0], -side / 2)).set_stroke(YELLOW, 3) for p in pos]
    clk_label = T("CLK", 30, YELLOW).next_to(clk.get_left(), DOWN, buff=0.14, aligned_edge=LEFT)
    wrap = CurvedArrow(pos[-1] + (side / 2 + 0.08) * UP, pos[0] + (side / 2 + 0.08) * UP, angle=0.6,
                       color=DIM, stroke_width=3, tip_length=0.18)
    wrap.set_fill(opacity=0)
    wrap.tip.set_fill(DIM, 1)
    g = VGroup(clk, *stubs, wrap, *boxes, clk_label, *digits)
    g.boxes, g.digits, g.clk, g.stubs, g.clk_label, g.wrap = boxes, digits, clk, stubs, clk_label, wrap
    g.pos = lambda i: g.boxes[i].get_center()
    g.side = side
    return g


def binary_trio(bits="000", side=CELL_SIDE, pitch=CELL_PITCH):
    pos, boxes, digits = _cells(bits, side, pitch)
    g = VGroup(*boxes, *digits)
    g.boxes, g.digits = boxes, digits
    g.pos = lambda i: g.boxes[i].get_center()
    g.side = side
    return g


# ---------------------------------------------------------------- the recap ring (ch2 s5 / ch3)
RING_SC = 1.0
RING_C = _p(0, 0.1)


def recap_ring():
    """ch2_s5's ring_circle with d, e = 1 (ch3's rescue) and RED active-low S pins (ch3_s6's
    pin() look) on d (pointing down, clear of its letter) and e (pointing up)."""
    bits = "00011"                       # a b c d e
    r = S5.ring_circle(center=ORIGIN, bits=bits)
    r.scale(RING_SC, about_point=ORIGIN).shift(RING_C)
    pins = []
    for i, u, side in ((3, DOWN, RIGHT), (4, UP, LEFT)):
        box = r.boxes[i]
        edge = box.get_center() + box.height / 2 * u
        rb = 0.09
        bub = Circle(radius=rb).set_stroke(RED, 3).set_fill(BG, 1).move_to(edge + rb * u)
        w = Line(edge + 2 * rb * u, edge + (2 * rb + 0.55) * u).set_stroke(RED, 5)
        lab = T("S", 28, RED).next_to(w, side, buff=0.12)
        pins.append(VGroup(bub, w, lab))
    return r, pins, list(bits)


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ ring stepping
    def ring_step(self):
        old = self.rbits
        new = [old[-1]] + old[:-1]          # a <- e, b <- a, ...
        anims = []
        for i in range(5):
            if new[i] != old[i]:
                d = S5.cell_bit(new[i], 40).scale(RING_SC).move_to(self.ring.boxes[i])
                anims += swap(self.rdig[i], d, shift=0.12 * UP)
                self.rdig[i] = d
                box = self.ring.boxes[i]
                anims.append(box.animate.set_fill(GOLD, 0.22) if int(new[i]) else box.animate.set_fill(BG, 1))
        self.rbits = new
        return anims

    def ring_ticks(self, c, cue, period=1.5, rt=0.7):
        while c.until(cue, floor=0) >= period:
            self.wait(period - rt)
            self.play(*self.ring_step(), run_time=rt)

    def clip1(self):
        card = title_card("Part 4 · One-hot")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        end = load_scene("ch3_s8_recap").end_card()
        self.add(*end)
        with self.say("c4.hook.1") as c:
            part4 = end.part
            self.wait(0.7)   # ch3's end card holds a moment: the cut reads as a continuation
            self.play(*during(disappear(end.row), 0, 0.4),
                      *during([part4.animate.scale(card.part.height / part4.height).move_to(card.part)], 0.1, 0.6),
                      *during(appear(card.title, card.rule, card.course, lag=0.2), 0.55, 1),  # early: title card
                      run_time=min(1.5, c.until("last", floor=1.0)))
            self.remove(part4)
            self.add(card.part)
            c.wait_until("last")
            self.wait(min(1.2, c.until("fun", floor=0) - 3.0))   # the title card reads ~2 s before the ring comes in

            ring, pins, bits = recap_ring()
            self.ring, self.pins, self.rbits = ring, pins, bits
            tag = T("Part 3: start in a used state", 34, t2c={"Part 3:": DIM})
            tag.move_to(_p(0, 3.35))
            sweep_clear(self, *appear(ring, *pins, tag, shift=None, lag=0.1), run_time=1.6)  # early: recap tag
            self.rdig = list(ring.digits)
            ring.remove(*self.rdig)
            self.add(*self.rdig)

            self.ring_ticks(c, "fun")
            c.wait_until("fun")

            # the two flip-flops beyond the three that five states need
            extra = [ring.boxes[3], ring.boxes[4]]
            fun = T("+2,  “a bit of fun”", 34, t2c={"+2,": GOLD})
            fun.move_to(_p(0, -3.25))
            self.play(*[b.animate.set_stroke(GOLD, 8) for b in extra], *appear(fun), run_time=1.2)
            c.wait_until("for fun")
            self.wait(0.6)
            self.play(*[b.animate.set_stroke(BLUE, 4) for b in extra], run_time=0.8)
            self.ring_ticks(c, "real")
            c.wait_until("real")

            # the ring slides away; one-hot arrives
            line = T("one-hot: used a lot", 52, t2c={"one-hot:": YELLOW})
            going = [ring, *pins, *self.rdig, tag, fun]
            self.play(*during([FadeOut(m, shift=4 * LEFT) for m in going], 0, 0.6),
                      *during(appear(line, shift=None), 0.55, 1), run_time=min(2.0, c.until(floor=1.2)))
            self.line = line

    # ------------------------------------------------------------ the two machines stepping
    def mk_digit(self, b, at, op):
        d = hot_bit(b).move_to(at)
        d.set_opacity(op)
        return d

    def machine_step(self):
        s0, s1 = self.state, (self.state + 1) % 8
        anims = []
        L, R = self.left, self.right
        # one-hot: the 1 moves on one cell
        for i, b in ((s0, 0), (s1, 1)):
            d = self.mk_digit(b, L.pos(i), self.op_left)
            anims += swap(self.ldig[i], d, shift=0.12 * UP)
            self.ldig[i] = d
            box = L.boxes[i]
            anims.append(box.animate.set_fill(GOLD, 0.22 * self.op_left) if b else box.animate.set_fill(BG, 1))
        # binary: count
        ob, nb = f"{s0:03b}", f"{s1:03b}"
        for i in range(3):
            if ob[i] != nb[i]:
                d = self.mk_digit(nb[i], R.pos(i), self.op_right)
                anims += swap(self.rdig2[i], d, shift=0.12 * UP)
                self.rdig2[i] = d
                box = R.boxes[i]
                anims.append(box.animate.set_fill(GOLD, 0.22 * self.op_right) if int(nb[i])
                             else box.animate.set_fill(BG, 1))
        num = Mono(str(s1), 56, color=GOLD).move_to(self.num)
        anims += swap(self.num, num, shift=0.15 * UP)
        self.num = num
        self.state = s1
        return anims

    # A steady beat: a tick every PERIOD s on a fixed grid; cue actions fit in between.
    PERIOD, TICK_RT = 1.4, 0.75

    def idle(self, dt):
        if dt > 1e-3:
            self.wait(dt)

    def tick(self, *extra):
        self.idle(self.next_tick - self.time)
        self.play(*self.machine_step(), *extra, run_time=self.TICK_RT)
        self.next_tick += self.PERIOD
        self.last_end = self.time

    def beat_to(self, t):
        """Keep ticking on the grid while a whole tick still fits before scene time t."""
        while self.next_tick + self.TICK_RT <= t + 1e-6:
            self.tick()
        self.idle(t - self.time)

    def act(self, t, make, rt):
        """make() builds the anims once the running ticks are done (they replace digits). At scene time t (after the running tick), play anims alone; the grid moves on only if
        they run into the next tick's slot."""
        self.beat_to(t)
        self.idle(self.last_end - self.time)
        self.play(*make(), run_time=rt)
        self.next_tick = max(self.next_tick, self.time + 0.1)

    def side_alpha(self, side, op):
        """Dim / restore one machine (boxes' outlines, CLK, digits) without touching box fills."""
        if side == "left":
            self.op_left = op
            m, digs = self.left, self.ldig
            parts = [m.clk, *m.stubs, m.clk_label, m.wrap]
        else:
            self.op_right = op
            m, digs = self.right, self.rdig2
            parts = list(m.clk_parts)
        anims = [b.animate.set_stroke(opacity=op) for b in m.boxes]
        anims += [restyle(p, op) for p in parts]
        anims += [d.animate.set_opacity(op) for d in digs]
        return anims

    def clip2(self):
        # two separate machines: the row of eight (left), a gap holding the "?", the trio on its own CLK
        side, pitch, y = 0.8, 0.92, 0.3
        left = onehot_row(8, 0, side=side, pitch=pitch)
        left.shift(_p(-6.3 - left.clk.get_left()[0], y))
        right = binary_trio("000", side=side, pitch=pitch)
        right.move_to(_p(left.boxes[-1].get_right()[0] + 2.0 + right.width / 2, y))
        y_clk = left.clk.get_y()
        rx0, rx1 = right.boxes[0].get_left()[0] - 0.25, right.boxes[-1].get_right()[0] + 0.1
        rclk = Line(_p(rx0, y_clk), _p(rx1, y_clk)).set_stroke(YELLOW, 4)
        rstubs = [Line(_p(b.get_x(), y_clk), _p(b.get_x(), b.get_bottom()[1])).set_stroke(YELLOW, 3)
                  for b in right.boxes]
        rclk_label = T("CLK", 30, YELLOW).next_to(rclk.get_left(), DOWN, buff=0.14, aligned_edge=LEFT)
        right.add_to_back(rclk, *rstubs)
        right.add(rclk_label)
        right.clk_parts = [rclk, *rstubs, rclk_label]
        self.gap_x = (left.boxes[-1].get_right()[0] + right.boxes[0].get_left()[0]) / 2
        word = T("state", 36, color=DIM)
        num = Mono("0", 56, color=GOLD)
        head = VGroup(word, num).arrange(RIGHT, buff=0.3).move_to(_p(0, 2.5))
        self.left, self.right, self.num, self.state = left, right, num, 0
        self.op_left = self.op_right = 1.0

        with self.say("c4.hook.2") as c:
            self.play(*during(disappear(self.line), 0, 0.3),
                      *during(appear(head, right, left, lag=0.2), 0.3, 1),
                      run_time=min(2.4, 0.85 * c.until("binary")))
            self.ldig, self.rdig2 = list(left.digits), list(right.digits)
            left.remove(*self.ldig)
            right.remove(*self.rdig2)
            self.add(*self.ldig, *self.rdig2)
            head.remove(num)
            self.add(num)
            c.wait_until("binary")

            # right: binary counting (left dimmed, still in step); then a steady beat to the end
            self.next_tick, self.last_end = self.time + 0.7, self.time
            self.play(*self.side_alpha("left", 0.35), run_time=0.6)
            self.act(c.at("step"), lambda: [*self.side_alpha("left", 1.0), *self.side_alpha("right", 0.45)], 0.6)

            n8 = T("8 flip-flops", 36, t2c={"8": GOLD}).next_to(left.clk_label, DOWN, buff=0.35)
            n8.set_x((left.boxes[0].get_x() + left.boxes[-1].get_x()) / 2)
            n3 = T("3 flip-flops", 36, t2c={"3": GOLD}).move_to(_p(right.boxes[1].get_x(), n8.get_y()))
            self.act(c.at("count"), lambda: [*self.side_alpha("right", 1.0), *appear(n8)], 0.6)
            self.beat_to(c.at(own_word=n3, cue="three") - 0.2)
            self.tick(*appear(n3))

            q = T("?", 96, color=YELLOW).move_to(_p(self.gap_x, left.boxes[0].get_y()))
            ask = T("What do we gain from one flip-flop per state?", 38).move_to(_p(0, -2.85))
            self.act(c.at("question"), lambda: [*self.side_alpha("left", 0.55), *self.side_alpha("right", 0.55),
                                        *appear(q, shift=None)], 0.6)
            self.tick(*appear(ask))
            self.beat_to(c.end)
        self.beat_to(self.time + 1.4)
        self.wait(0.6)
