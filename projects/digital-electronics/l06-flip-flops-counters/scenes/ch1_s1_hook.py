"""Chapter 1, scene 1: hook: scattered memories, a clock, memories that change in step. Clips c1.hook.1 – c1.hook.3."""
# style: 2
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


# ---------------------------------------------------------------------------------------------
# Shared visuals of chapter 1 (s2, s3, s4, s6, s7 copy these two blocks verbatim).
# ---------------------------------------------------------------------------------------------
def _bit_style(bit):
    """(colour, stroke width, fill opacity) of a memory cell holding `bit`."""
    return (GREEN, 4, 0.16) if bit else (DIM, 3, 0.0)


def memory_cell(bit=0, size=1.1):
    """One-bit memory: rounded square with a 0/1 inside. GREEN bright for 1, DIM for 0.
    VGroup(box, digit) with .box .digit .bit .size; built at ORIGIN."""
    col, sw, fo = _bit_style(bit)
    box = RoundedRectangle(corner_radius=0.16 * size, width=size, height=size)
    box.set_stroke(col, sw).set_fill(col, fo)
    digit = T(str(bit), size=44 * size / 1.1, color=col)
    digit.move_to(box)
    cell = VGroup(box, digit)
    cell.box, cell.digit, cell.bit, cell.size = box, digit, bit, size
    return cell


def flip_cell(cell, bit=None):
    """Animations that set `cell` to `bit` (default: the other bit): the digit is swapped (old rises
    out, new rises in) and the box recoloured. Returns (anims, new_digit); after the play call
    finish_flip(scene, cell, new_digit, bit)."""
    bit = 1 - cell.bit if bit is None else bit
    col, sw, fo = _bit_style(bit)
    new = T(str(bit), size=44, color=col)
    new.set_height(cell.digit.height).move_to(cell.box)
    anims = [*swap(cell.digit, new, shift=0.12 * UP),
             cell.box.animate.set_stroke(col, sw).set_fill(col, fo)]
    return anims, new


def finish_flip(scene, cell, new_digit, bit):
    """Put the new digit into the cell group and the cell back on screen as one object."""
    old = cell.digit
    settle(scene, cell, add=[new_digit], drop=[old])
    cell.digit, cell.bit = new_digit, bit


class ClockWave(VGroup):
    """YELLOW clock square wave: starts low for half a period, then `periods` cycles (high half,
    low half). Flat levels, sharp vertical edges, small ▲ on every rising edge (▼ on falling
    edges if down_arrows). .wave (the line), .ups, .downs; .period; .rising_x(i)/.falling_x(i)
    give the current absolute x of edge i. Default 9.9 × 0.7, period 1.8, centred at ORIGIN."""

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
        self.downs = VGroup(*[Triangle().rotate(PI).scale(tri).set_stroke(width=0).set_fill(color, 1)
                              .move_to([x0 + f, 0, 0]) for f in (self._fall if down_arrows else [])])
        self.add(self.wave, self.ups, self.downs)

    def rising_x(self, i):
        return self.wave.get_left()[0] + self._rise[i] * self.wave.width / self._span()  # scale-safe

    def falling_x(self, i):
        return self.wave.get_left()[0] + self._fall[i] * self.wave.width / self._span()

    def _span(self):
        return self._width


def clock_wave(width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True, down_arrows=False):
    return ClockWave(width, height, periods, color, up_arrows, down_arrows)


# ---------------------------------------------------------------------------------------------

GRID_SHRINK = 0.78
GRID_UP = 0.25


class Hook(NarratedScene):
    def construct(self):
        self.rng = random.Random(6)
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- helpers --------------------------------------------------------------------------
    def flip_play(self, cells, run_time, span=(0.0, 1.0), extra=(), rate_func=smooth):
        """One play that flips every cell in `cells` during `span` of it (plus `extra` anims)."""
        anims, news = [], []
        for cell in cells:
            a, new = flip_cell(cell)
            anims += a
            news.append((cell, new, 1 - cell.bit))
        self.play(*during(anims, *span), *extra, run_time=run_time, rate_func=rate_func)
        for cell, new, bit in news:
            finish_flip(self, cell, new, bit)

    def flicker(self, c, cue=None):
        """Scattered, irregular flips, one cell at a time, until the cue (or clip end)."""
        last = None
        while True:
            rem = c.until(cue, floor=0)
            if rem < 0.75:
                break
            cell = self.rng.choice([x for x in self.cells if x is not last])
            last = cell
            self.flip_play([cell], run_time=0.5)
            pause = self.rng.choice([0.08, 0.15, 0.3, 0.45, 0.7, 0.2])
            self.wait(max(0.01, min(pause, c.until(cue, floor=0) - 0.05)))
        c.wait_until(cue)

    # -- clip 1: title, the grid, scattered flips ------------------------------------------
    def clip1(self):
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · Clocks and the transparent D latch")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole

            bits = [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1]
            self.cells = [memory_cell(b) for b in bits]
            grid = VGroup(*self.cells).arrange_in_grid(4, 4, buff=0.3).move_to(ORIGIN)
            c.wait_until("grid")
            sweep_clear(self, *appear(*self.cells, shift=None, lag=0.06),
                        run_time=min(2.0, c.until("Each one")))
            del grid   # cells live on screen one by one; never add the grid itself

            c.wait_until("zero")
            zero_cell, one_cell = self.cells[10], self.cells[9]   # a 0 and a 1 side by side
            self.play(FlashAround(zero_cell, color=FG, time_width=1.5),
                      run_time=min(1.2, c.until("or a one")))
            c.wait_until("or a one")
            self.play(FlashAround(one_cell, color=GREEN, time_width=1.5),
                      run_time=min(1.2, c.until("scatter")))

            c.wait_until("scatter")
            self.flicker(c)

    # -- clip 2: the clock, flips in step, the question ------------------------------------
    def clip2(self):
        with self.say("c1.hook.2") as c:
            wave = clock_wave()
            wave.move_to([0.35, -3.15, 0])
            clock_lbl = T("clock", size=32, color=YELLOW).next_to(wave, LEFT, buff=0.35)
            shrink = [cell.animate.scale(GRID_SHRINK, about_point=ORIGIN).shift(GRID_UP * UP)
                      for cell in self.cells]
            self.play(*shrink, FadeIn(wave, shift=2.5 * LEFT),
                      *during(appear(clock_lbl), 0.5, 1), run_time=min(2.0, c.until("together")))
            self.flicker(c, "together")

            # the beat: a guide line sweeps the wave; cells change only on the rising edge
            p = wave.period
            x0 = wave.wave.get_left()[0]
            guide = Line([x0, -3.75, 0], [x0, -2.55, 0]).set_stroke(FG, 2, opacity=0.7)
            self.play(FadeIn(guide), run_time=0.5)
            beat_rt = min(1.2, max(0.6, (c.until("question") - 0.15) / 3))
            for k in range(3):
                self.beat(guide, x0 + (k + 1) * p, beat_rt)

            c.wait_until("question")
            question = VGroup(T("How do you make a memory change", size=38, color=YELLOW),
                              T("only when the clock says so?", size=38, color=YELLOW)
                              ).arrange(DOWN, buff=0.16).move_to(3.0 * UP)
            self.play(*appear(question, shift=0.2 * DOWN), run_time=1.2)  # early: question read whole
            c.wait_until("clock says so")
            self.beat(guide, x0 + 4 * p, min(1.4, max(0.8, c.until() - 0.1)))

    def beat(self, guide, x_to, run_time):
        """Guide sweeps one period; it crosses the rising edge at half time, and the chosen
        cells all flip on that edge at once."""
        n = self.rng.choice([4, 5, 6])
        cells = self.rng.sample(self.cells, n)
        self.flip_play(cells, run_time=run_time, span=(0.5, 0.78),
                       extra=[guide.animate(rate_func=linear).set_x(x_to)], rate_func=linear)

    # -- clip 3: the road ------------------------------------------------------------------
    def clip3(self):
        with self.say("c1.hook.3", gap=1.5) as c:
            names = ["latch", "flip-flop", "counter"]
            boxes = [RoundedRectangle(corner_radius=0.18, width=2.9, height=1.3)
                     .set_stroke(DIM, 3).set_fill(BG, 1) for _ in names]
            VGroup(*boxes).arrange(RIGHT, buff=1.25).move_to(0.4 * UP)
            arrows = [Arrow(a.get_right(), b.get_left(), buff=0.15, stroke_width=4)
                      .set_color(DIM) for a, b in zip(boxes, boxes[1:])]
            labels = [T(n, size=44).move_to(b) for n, b in zip(names, boxes)]

            c.wait_until("road")
            # all at once (a lagged sweep over 16 separate cells read as a scrambled pyramid)
            self.play(*disappear(*self.mobjects), run_time=0.8)
            self.play(*appear(boxes[0], arrows[0], boxes[1], arrows[1], boxes[2],
                              shift=None, lag=0.15),
                      run_time=max(0.6, min(1.2, c.until("latch") - 0.05)))
            for i, cue in enumerate(["latch", "flipflop", "counter"]):
                c.wait_until(cue, own_word=labels[i])
                nxt = ["flipflop", "counter", None][i]
                self.play(*appear(labels[i], shift=0.2 * DOWN),
                          boxes[i].animate.set_stroke(YELLOW, 4),
                          run_time=min(1.0, max(0.5, c.until(nxt) - 0.1)) if nxt else 1.0)

            c.wait_until("start")
            sub = T("transparent D latch", size=36, color=YELLOW).next_to(boxes[0], DOWN, buff=0.4)
            self.play(labels[0].animate.set_color(YELLOW),
                      *set_alpha([boxes[1], boxes[2], labels[1], labels[2], *arrows], 0.3),
                      *during(appear(sub), 0.35, 1), run_time=1.4)  # early: "today is step one" names it
