"""Chapter 1, scene 4: reading a chip (DIL package, pin 1, pin numbering, power pins, part number).
Clips c1.chips.1 – c1.chips.5.

Shared drawings (ch2 s4 calls back to the part-number split):
- `part_split(center=ORIGIN, size=80, gap=4.5)` -> VGroup of three Texts "74", "HC", "00" with
  `.whole_at(center)` positions (adjacent, reads as one "74HC00") and `.split_at(center)` positions
  (columns `gap` apart); `.parts`, `.colors` (BLUE series, GREEN technology, YELLOW function),
  `.tags` ("the series" / "the technology" / "the function"); `split_box(part, color)` is the box.
- `nand_gate()` / `nor_gate()` (L6 ch1_s2 gate style: BLUE 4-stroke, BG fill) and `Gate`.
- `pin_label(chip, k, mob, extra)` places a label outward of pin k (works on a rotated chip);
  `attach_pin_label` keeps it there with an updater.
The chip drawing itself is ch1_s3_breadboard's `DipChip`, loaded with load_scene.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

_bb = load_scene("ch1_s3_breadboard")
DipChip, PIN_GREY = _bb.DipChip, _bb.PIN_GREY

P = 1.05                    # hero chip pitch
HERO = ORIGIN
SMALL16 = np.array([5.0, 2.8, 0])
CHIP4 = 1.9 * UP


# ── gates (L6 ch1_s2_rslatch style) ───────────────────────────────────────────────
GATE_COLOR = BLUE


def _p(x, y):
    return np.array([x, y, 0.0])


class Gate(VGroup):
    def __init__(self, body, ins, out, bubble=None, color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body, self.bubble = body, bubble
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        if bubble is not None:
            bubble.set_stroke(color, 4).set_fill(BG, 1)
            self.add(bubble)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def nand_gate(color=GATE_COLOR):
    """AND body + output bubble, ~1.5 wide x 1.2 tall, centred near ORIGIN."""
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    bubble = Circle(radius=0.1).move_to(_p(0.7, 0))
    return Gate(b, [(-0.7, 0.3), (-0.7, -0.3)], (0.8, 0.0), bubble=bubble, color=color)


def nor_gate(color=GATE_COLOR):
    """Distinctive-shape NOR (OR body + bubble), 1.6 wide x 1.2 tall (L6 ch1_s2's nor_gate)."""
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    bubble = Circle(radius=0.1).move_to(_p(0.8, 0))
    return Gate(b, [(-0.56, 0.3), (-0.56, -0.3)], (0.9, 0.0), bubble=bubble, color=color)


# ── pin labels that follow the chip (also when it turns) ──────────────────────────
def pin_label(chip, k, mob, extra=0.0):
    """The point to move `mob` to so it sits just outward of pin k (beyond it by `extra`)."""
    n = len(chip.pins)
    s = chip.pin(n).get_center() - chip.pin(1).get_center()     # bottom row -> top row
    s = s / np.linalg.norm(s)
    pitch = np.linalg.norm(chip.pin(2).get_center() - chip.pin(1).get_center())
    d = -s if k <= n // 2 else s
    half = abs(d[0]) * mob.width / 2 + abs(d[1]) * mob.height / 2
    return chip.pin(k).get_center() + d * (0.225 * pitch + 0.14 + extra + half)


def attach_pin_label(mob, chip, k, extra=0.0):
    mob.move_to(pin_label(chip, k, mob, extra))
    mob.add_updater(lambda m: m.move_to(pin_label(chip, k, m, extra)))
    return mob


def pin_numbers(chip, ks, size=28, color=FG, follow=False, ref=None):
    """{k: T(k)} beside each pin k; `ref` = a chip whose layout places them (default chip)."""
    ref = ref or chip
    out = {}
    for k in ks:
        t = T(str(k), size=size, color=color)
        if follow:
            attach_pin_label(t, chip, k)
        else:
            t.move_to(pin_label(ref, k, t))
        out[k] = t
    return out


# ── the part-number split (shared: L7 ch2 s4 calls back to it) ────────────────────
SPLIT_COLORS = (BLUE, GREEN, YELLOW)


def part_split(center=ORIGIN, size=80, gap=4.5):
    """'74HC00' as one Text at `center` (show it whole, e.g. fly it off the chip), with
    `.parts[i]` = [glyph, glyph] of "74", "HC", "00" (lists, never wrap them to play),
    `.split_moves()` -> the per-glyph moves that spread the parts into columns `gap` apart,
    `.cols` (the column centres), `.colors` and `.tags`."""
    g = T("74HC00", size=size).move_to(center)
    g.parts = [[g[0], g[1]], [g[2], g[3]], [g[4], g[5]]]
    g.colors = SPLIT_COLORS
    g.tags = ("the series", "the technology", "the function")
    g.cols = [np.array(center) + RIGHT * gap * (i - 1) for i in range(3)]

    def split_moves():
        out = []
        for part, col in zip(g.parts, g.cols):
            d = col - VGroup(*part).get_center()
            out += [gl.animate.shift(d) for gl in part]
        return out
    g.split_moves = split_moves
    return g


def split_box(part, color):
    box = SurroundingRectangle(VGroup(*part), color=color, buff=0.18, corner_radius=0.08)
    return box.set_stroke(color, 3).set_fill(color, 0.12).set_z_index(-1)


def booklet(color=FG):
    page = RoundedRectangle(corner_radius=0.05, width=0.8, height=1.05).set_stroke(color, 3).set_fill(BG, 1)
    spine = Line(page.get_corner(UL) + RIGHT * 0.14, page.get_corner(DL) + RIGHT * 0.14).set_stroke(color, 3)
    lines = VGroup(*[Line(LEFT * 0.18, RIGHT * 0.25).shift(UP * y + RIGHT * 0.04).set_stroke(DIM, 3)
                     for y in (0.25, 0.05, -0.15)])
    return VGroup(page, spine, lines)


class ChipsScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c1.chips.1: the package, 14 pins, the 16-pin counter ─────────────────────
    def clip1(self):
        chip = self.chip = DipChip(14, "74HC00", pitch=P).shift(HERO)
        title = T("Dual in Line (DIL) package", 44).move_to(3.2 * UP)
        pins_lbl = T("14 pins, 7 a side", 36)
        pins_lbl.move_to(HERO + DOWN * (chip.height / 2 + 0.55))
        with self.say("c1.chips.1") as c:
            self.play(FadeIn(chip, shift=0.3 * UP), run_time=1.2)
            c.wait_until(own_word=title)
            self.play(*appear(title), run_time=1.0)
            c.wait_until("pins")
            self.play(*appear(pins_lbl), *[FlashAround(p, color=YELLOW, buff=0.04, stroke_width=3)
                                           for p in chip.pins], run_time=1.2)
            c.wait_until("sixteen")
            s = 0.72
            left = HERO + LEFT * 3.5
            c16 = self.chip16 = DipChip(16, "counter", pitch=P * s).move_to(HERO + RIGHT * 3.5)
            lbl16 = T("the lab's counter: 16 pins", 32).move_to(
                HERO + RIGHT * 3.5 + DOWN * (chip.height * s / 2 + 0.55))
            self.play(chip.animate.scale(s).move_to(left),
                      pins_lbl.animate.move_to([left[0], lbl16.get_y(), 0]),
                      *during([FadeIn(c16, shift=LEFT * 1.2)], 0.3, 1),
                      *during(appear(lbl16), 0.6, 1), run_time=min(1.8, c.until()))
        self.title, self.pins_lbl, self.lbl16 = title, pins_lbl, lbl16

    # ── c1.chips.2: pin 1, the notch, counting ───────────────────────────────────
    def clip2(self):
        chip, c16 = self.chip, self.chip16
        with self.say("c1.chips.2") as c:
            self.play(FlashAround(chip.pin(1), color=PINK, buff=0.08), run_time=1.0)
            c.wait_until("older chips")
            self.play(*during(disappear(self.title, self.pins_lbl, self.lbl16), 0, 0.4),
                      *during([chip.animate.scale(1 / 0.72).move_to(HERO),
                              c16.animate.scale(0.4 / (P * 0.72)).move_to(SMALL16)], 0.4, 1),
                      run_time=1.3)
            c.wait_until("white dot")
            dot = Dot(chip.pin(1).get_center() + UP * 0.48 * P, radius=0.13)
            dot.set_fill(FG, 1).set_stroke(PINK, 3)
            self.play(FadeIn(dot, scale=0.5), run_time=0.8)
            c.wait_until("laser")
            self.play(restyle(chip.label, op=0.35, fill=DIM), FadeOut(dot), run_time=1.5)
            c.wait_until("notch")
            pin1_lbl = T("pin 1 end", 34, color=PINK).next_to(chip.body, LEFT, buff=0.45)
            self.play(FlashAround(chip.notch, color=PINK, buff=0.1),
                      chip.notch.animate(rate_func=there_and_back).scale(1.35),
                      *appear(pin1_lbl, shift=0.2 * RIGHT), run_time=1.2)
            c.wait_until("wrong")
            gc = np.array([0, -2.55, 0])
            ghost = DipChip(14, "74HC00", pitch=0.5).rotate(PI).move_to(gc).set_opacity(0.45)
            ref = DipChip(14, "74HC00", pitch=0.5).move_to(gc)
            red = pin_numbers(ghost, range(1, 15), color=RED, ref=ref)
            self.play(FadeIn(ghost, shift=0.2 * UP),
                      *during(appear(*red.values(), lag=0.05, shift=None), 0.4, 1), run_time=1.2)
            nums = self.nums = pin_numbers(chip, range(1, 15), follow=True)
            c.wait_until("one to seven")
            self.play(*during(disappear(ghost, *red.values(), pin1_lbl), 0, 0.3),
                      *during(appear(*[nums[k] for k in range(1, 8)], lag=0.35, shift=None), 0.3, 1),
                      run_time=min(2.8, c.until("then eight")))
            c.wait_until("then eight")
            a = nums[7].get_center() + RIGHT * 0.5
            b = nums[8].get_center() + RIGHT * 0.5
            arc = self.arc = CurvedArrow(a, b, angle=0.85 * PI, color=YELLOW, stroke_width=4)
            self.play(Create(arc, run_time=0.9), *appear(*[nums[k] for k in range(8, 15)], lag=0.35, shift=None),
                      run_time=min(2.2, 0.85 * c.until()))

    # ── c1.chips.3: power pins, the quarter turn, exceptions ─────────────────────
    def clip3(self):
        chip, c16, nums = self.chip, self.chip16, self.nums
        gnd = attach_pin_label(T("GND (0V)", 34, color=DIM), chip, 7, extra=0.55)
        vcc = attach_pin_label(T("Vcc (5V)", 34, color=GOLD), chip, 14, extra=0.55)
        with self.say("c1.chips.3", gap=2.6) as c:   # hold on the exceptions before the board clears
            self.play(FadeOut(self.arc),
                      chip.pin(7).animate.set_fill(DIM), nums[7].animate.set_color(DIM), run_time=1.0)
            self.play(*appear(gnd), run_time=0.8)
            c.wait_until("five volts")
            self.play(chip.pin(14).animate.set_fill(GOLD), nums[14].animate.set_color(GOLD),
                      *appear(vcc), run_time=1.0)
            c.wait_until("opposite corners")
            diag = DashedLine(chip.pin(7).get_center(), chip.pin(14).get_center(),
                              dash_length=0.16).set_stroke(YELLOW, 4)
            corners = T("opposite corners", 36, color=YELLOW).move_to(2.3 * DOWN)
            self.play(Create(diag), *appear(corners), run_time=1.2)
            c.wait_until("sixteen")
            n8 = T("8", 28, color=DIM).move_to(pin_label(c16, 8, T("8", 28)))
            n16 = T("16", 28, color=GOLD).move_to(pin_label(c16, 16, T("16", 28)))
            self.play(c16.pin(8).animate.set_fill(DIM), c16.pin(16).animate.set_fill(GOLD),
                      *appear(n8, n16, shift=None), run_time=1.0)
            self.play(FlashAround(c16.pin(8), color=YELLOW, buff=0.05),
                      FlashAround(c16.pin(16), color=GOLD, buff=0.05), run_time=1.0)
            self.n16 = VGroup(n8, n16)
            c.wait_until("quarter turn")
            self.play(*disappear(diag, corners), run_time=0.7)
            self.play(chip.animate.scale(0.62).move_to(1.0 * UP + 0.8 * LEFT), run_time=0.9)
            self.play(Rotate(chip, -PI / 2, about_point=chip.body.get_center()), run_time=1.6)
            c.wait_until("bottom left")
            rule = T("notch up:  bottom left: ground  ·  top right: 5 V", 36).move_to(1.95 * DOWN)
            self.play(*appear(rule), run_time=1.0)
            self.play(FlashAround(gnd, color=DIM), FlashAround(vcc, color=GOLD), run_time=1.2)
            c.wait_until("exceptions")
            exc = T("However, there are exceptions!", 36, color=YELLOW).move_to(2.7 * DOWN)
            none = T("none among the lab's chips", 30, color=DIM).move_to(3.25 * DOWN)
            self.play(*during(disappear(gnd, vcc), 0, 0.3),
                      *during([Rotate(chip, PI / 2, about_point=chip.body.get_center())], 0.3, 0.8),
                      *during(appear(exc), 0.3, 0.7), run_time=min(2.2, c.until()))
            c.wait_until("none among")
            self.play(*appear(none), run_time=min(1.0, c.until()))
        self.gnd, self.vcc, self.rule, self.exc = gnd, vcc, rule, VGroup(exc, none)

    # ── c1.chips.4: 74 | HC | 00 ──────────────────────────────────────────────────
    def clip4(self):
        chip = self.chip
        split = part_split(center=0.45 * DOWN)
        cols = split.cols
        with self.say("c1.chips.4", gap=2.2) as c:
            self.play(*disappear(self.rule, self.exc, self.chip16, self.n16, *self.nums.values()),
                      chip.pin(7).animate.set_fill(PIN_GREY), chip.pin(14).animate.set_fill(PIN_GREY), run_time=0.8)
            self.play(chip.animate.scale(1 / 0.62).move_to(CHIP4), run_time=0.9)
            c.wait_until("seventy-four")
            self.play(Transform(chip.label, split), run_time=min(1.5, c.until("series")))
            chip.remove(chip.label)
            self.remove(chip.label)
            self.add(split)
            c.wait_until("series")
            self.play(*split.split_moves(), run_time=1.2)
            tags, subs = [], []
            for i, (part, col) in enumerate(zip(split.parts, split.colors)):
                tags.append(T(split.tags[i], 34, color=col).move_to([cols[i][0], -1.5, 0]))
            boxes = [split_box(p, col) for p, col in zip(split.parts, split.colors)]
            self.play(GrowFromCenter(boxes[0]), *appear(tags[0]), run_time=1.0)
            c.wait_until("nineteen-sixties")
            s0 = T("since the 1960s", 30).move_to([cols[0][0], -2.1, 0])
            self.play(*appear(s0), run_time=1.0)

            c.wait_until("technology")
            self.play(GrowFromCenter(boxes[1]), *appear(tags[1]), run_time=1.0)
            c.wait_until("high-speed")
            s1 = T("high-speed CMOS", 30).move_to([cols[1][0], -2.1, 0])
            self.play(*appear(s1), run_time=1.0)
            c.wait_until("bipolar")
            bip = T("bipolar: power-hungry, expensive", 28, color=DIM).move_to([cols[1][0], -2.8, 0])
            strike = Line(bip.get_left() + LEFT * 0.1, bip.get_right() + RIGHT * 0.1).set_stroke(RED, 4)
            self.play(*appear(bip), run_time=1.0)
            c.wait_until("power-hungry")
            self.play(Create(strike), run_time=1.0)
            c.wait_until("nearly every chip")
            self.play(FlashUnder(s1, color=GREEN), run_time=1.5)

            c.wait_until("function")
            self.play(GrowFromCenter(boxes[2]), *appear(tags[2]), run_time=1.0)
            c.wait_until("four two-input")
            s2 = T("4 × 2-input NAND", 30).move_to([cols[2][0], -2.1, 0])
            gates = [nand_gate().scale(0.7).move_to(CHIP4 + RIGHT * x) for x in (-2.4, -0.8, 0.8, 2.4)]
            self.play(*appear(s2), *[FadeIn(g) for g in gates], run_time=1.2)   # all four together
            c.wait_until("quad nand")
            s3 = T("= quad NAND", 30, color=YELLOW).move_to([cols[2][0], -2.65, 0])
            self.play(*appear(s3), run_time=min(1.0, c.until()))

    # ── c1.chips.5: 7400 vs 7402, the booklet ────────────────────────────────────
    def clip5(self):
        warn = T("Never take the pin out of an IC for granted!", 40, color=RED)
        with self.say("c1.chips.5") as c:
            sweep_clear(self, *appear(warn), run_time=1.4)
            c.wait_until("here's")
            self.play(warn.animate.scale(0.8).move_to(3.25 * UP), run_time=1.0)
            chips, labels, nums = [], [], []
            for x, name, kind in ((-3.4, "7400", "quad NAND"), (3.4, "7402", "quad NOR")):
                ch = DipChip(14, name, pitch=0.75).move_to([x, 0.5, 0])
                chips.append(ch)
                nums.append(pin_numbers(ch, range(1, 15)))
                labels.append(T(f"{name}  ·  {kind}", 34).move_to([x, -1.4, 0]))
            c.wait_until("seventy-four zero zero")
            self.play(FadeIn(chips[0], shift=0.2 * UP), *appear(*nums[0].values(), lag=0.03, shift=None),
                      run_time=1.2)
            self.play(*appear(labels[0]), run_time=0.8)
            c.wait_until("seventy-four zero two")
            self.play(FadeIn(chips[1], shift=0.2 * UP), *appear(*nums[1].values(), lag=0.03, shift=None),
                      run_time=1.2)
            self.play(*appear(labels[1]), run_time=0.8)
            c.wait_until("same package")
            anims = []
            for ch, nm in zip(chips, nums):
                anims += [ch.pin(7).animate.set_fill(DIM), nm[7].animate.set_color(DIM),
                          ch.pin(14).animate.set_fill(GOLD), nm[14].animate.set_color(GOLD)]
            self.play(*anims, run_time=1.2)
            words = (("three", 0, 3), ("six", 0, 6), ("eight", 0, 8), ("eleven", 0, 11),
                     ("one", 1, 1), ("four", 1, 4), ("ten", 1, 10), ("thirteen", 1, 13))
            for i, (w, ci, k) in enumerate(words):
                c.wait_until(w)
                nxt = words[i + 1][0] if i + 1 < len(words) else "booklet"
                self.play(chips[ci].pin(k).animate.set_fill(GREEN), nums[ci][k].animate.set_color(GREEN),
                          run_time=min(0.6, c.until(nxt)))
            c.wait_until("booklet")
            book = booklet()
            blbl = T("pin-out booklet: in the lab", 34)
            VGroup(book, blbl).arrange(RIGHT, buff=0.4).move_to(2.75 * DOWN)
            self.play(FadeIn(book, shift=0.2 * UP), *appear(blbl), run_time=1.0)
            c.wait_until("use it")
            self.play(FlashAround(book, color=YELLOW), run_time=min(1.0, c.until()))
        self.wait(1.5)
