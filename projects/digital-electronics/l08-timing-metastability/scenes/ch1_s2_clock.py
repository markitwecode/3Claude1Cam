"""Chapter 1, scene 2: period and frequency; why a faster clock does more, and why it can't be
arbitrarily fast. Clips c1.clock.1 – c1.clock.3."""
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


# =============================================================================================
# Shared: the clock wave (L6 ch1_s1_hook.py, verbatim) and the T_c dimension arrow.
# ch1_s8 (recap) shrinks clock_with_period() into a panel.
# =============================================================================================
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


def dim_arrow(x0, x1, y, color=YELLOW, guide_bottom=None, label=None, gap=0.2):
    """Lecture-wide dimension arrow: thin double-headed line (stroke 3, small tips) from x0 to x1
    at height y, thin DIM vertical guides (stroke 1.5, as ch1_s3/ch1_s5) at both ends (down to guide_bottom), optional label
    (a mobject, coloured `color`) centred above. VGroup with .line .guides .label."""
    line = DoubleArrow([x0, y, 0], [x1, y, 0], buff=0, stroke_width=3, tip_length=0.14,
                       max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=20,
                       color=color)
    lo = y - 0.6 if guide_bottom is None else guide_bottom
    guides = VGroup(*[Line([x, lo, 0], [x, y + 0.18, 0]).set_stroke(DIM, 1.5) for x in (x0, x1)])
    g = VGroup(guides, line)
    g.line, g.guides, g.label = line, guides, None
    if label is not None:
        label.set_color(color).next_to(line, UP, buff=gap)
        g.add(label)
        g.label = label
    return g


WAVE_W, WAVE_H, WAVE_Y, ARROW_Y = 10.0, 1.0, 1.9, 2.8


def clock_with_period(periods=5, i=1, label=True):
    """The scene's hero: the clock wave (centred, y=WAVE_Y) with the T_c arrow over rising edges
    i → i+1, label "T_c  clock period". VGroup(wave, arrow) with .wave .arrow."""
    wave = clock_wave(width=WAVE_W, height=WAVE_H, periods=periods).move_to([0, WAVE_Y, 0])
    lbl = None
    if label:
        lbl = MathTex("T_c", font_size=48)
    arrow = dim_arrow(wave.rising_x(i), wave.rising_x(i + 1), ARROW_Y,
                      guide_bottom=WAVE_Y - WAVE_H / 2, label=lbl, gap=0.12)
    g = VGroup(wave, arrow)
    g.wave, g.arrow = wave, arrow
    return g
# =============================================================================================


def square_wave_line(nf, color=YELLOW, stroke_width=4):
    """The hero wave's line for a fractional period count nf: same layout as ClockWave
    (period WAVE_W / (nf + 0.5), low half-period first), cut off at the right edge."""
    p = WAVE_W / (nf + 0.5)
    x0, x1 = -WAVE_W / 2, WAVE_W / 2
    lo, hi = WAVE_Y - WAVE_H / 2, WAVE_Y + WAVE_H / 2
    pts, x = [[x0, lo, 0]], x0 + p / 2
    while x < x1 - 1e-6:
        pts += [[x, lo, 0], [x, hi, 0]]
        xf = x + p / 2
        if xf >= x1 - 1e-6:
            pts.append([x1, hi, 0])
            break
        pts += [[xf, hi, 0], [xf, lo, 0]]
        x = xf + p / 2
    else:
        pts.append([x1, lo, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width)


def led_icon():
    bulb = Circle(radius=0.22).set_stroke(RED, 3).set_fill(RED, 0.55)
    legs = VGroup(Line([-0.08, -0.22, 0], [-0.08, -0.5, 0]), Line([0.08, -0.22, 0], [0.08, -0.5, 0]))
    legs.set_stroke(DIM, 3)
    return VGroup(legs, bulb)


def chip_icon():
    body = Square(0.62).set_stroke(BLUE, 3).set_fill(BLUE, 0.2)
    pins = VGroup()
    for k in (-0.18, 0, 0.18):
        for side in (LEFT, RIGHT, UP, DOWN):
            d = np.array(side, dtype=float)
            perp = np.array([-d[1], d[0], 0.0])
            a = 0.31 * d + k * perp
            pins.add(Line(a, a + 0.13 * d))
    pins.set_stroke(BLUE, 2.5)
    return VGroup(pins, body)


def row_tex(*parts):
    """MathTex of a table row; parts that are numbers go GOLD."""
    m = MathTex(*parts, font_size=44)
    for p, sub in zip(parts, m):
        sub.set_color(GOLD if p.strip().isdigit() else FG)
    return m


class ClockPeriod(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- clip 1: period, frequency, hertz ------------------------------------------------
    def clip1(self):
        with self.say("c1.clock.1") as c:
            hero = clock_with_period()
            self.hero = hero
            wave, arrow = hero.wave, hero.arrow
            self.play(FadeIn(wave.wave, shift=1.5 * LEFT), run_time=min(1.6, c.until("period") - 0.6))
            self.play(LaggedStart(*[FadeIn(u, shift=0.15 * UP) for u in wave.ups], lag_ratio=0.2),
                      run_time=0.8)
            self.add(wave)
            c.wait_until("period")
            name = T("clock period", size=32, color=YELLOW)
            name.next_to(arrow.label, RIGHT, buff=0.3).align_to(arrow.label, DOWN)
            self.play(*[FadeIn(g) for g in arrow.guides], GrowFromCenter(arrow.line),
                      *during(appear(arrow.label, name), 0.4, 1), run_time=1.8)
            self.period_name = name
            c.wait_until("repeat")
            # copies appear in place, one period at a time (sliding them overlapped into one long span)
            tiles = []
            for k in (0, 2, 3):
                t = VGroup(arrow.guides.copy(), arrow.line.copy())
                t.shift((wave.rising_x(k) - wave.rising_x(1)) * RIGHT)
                tiles.append(t)
            self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.45), run_time=1.6)
            self.tiles = tiles
            c.wait_until("freq")
            formula = MathTex("f_c", "=", r"\frac{1}{T_c}", font_size=56)
            formula[0].set_color(YELLOW)
            formula.move_to([-4.6, 0.3, 0])
            flabel = VGroup(T("clock frequency:", size=32, color=YELLOW),
                            T("rising edges per second", size=30)).arrange(DOWN, aligned_edge=LEFT,
                                                                             buff=0.14)
            flabel.next_to(formula, RIGHT, buff=0.6)
            self.play(*appear(formula), run_time=1.2)
            self.play(*appear(flabel), *flash(wave.ups), run_time=1.4)
            c.wait_until("hertz")
            hz = T("unit: hertz (Hz)", size=32).next_to(flabel, RIGHT, buff=0.8)
            hz[5:10].set_color(YELLOW)
            self.play(*appear(hz), run_time=1.0)  # early: unit label lands on "hertz"
            self.freq = VGroup(formula, flabel, hz)

    # -- clip 2: 1 Hz vs 1 GHz -------------------------------------------------------------
    def clip2(self):
        with self.say("c1.clock.2", gap=1.4) as c:
            x_left = -4.6
            r1 = row_tex("1", r"\,\text{Hz}", r"\;\leftrightarrow\;", "T_c", "=", "1", r"\,\text{s}")
            r1.move_to([0, -1.15, 0]).align_to([x_left, 0, 0], LEFT)
            led = led_icon().move_to([-5.8, -1.05, 0])
            tag1 = T("lecture 6's counter", size=30, color=DIM).next_to(r1, RIGHT, buff=0.6)
            self.play(*appear(tag1), FadeIn(led), run_time=1.0)  # early: tag on "Lecture"
            c.wait_until("one hertz")
            self.play(*appear(r1), run_time=1.2)

            c.wait_until("fast")
            r2 = row_tex("1", r"\,\text{GHz}", r"\;\leftrightarrow\;", "T_c", "=", "1", r"\,\text{ns}")
            r2.move_to([0, -2.35, 0]).align_to([x_left, 0, 0], LEFT)
            chip = chip_icon().move_to([-5.8, -2.35, 0])
            self.play(FadeIn(chip), *appear(r2), run_time=1.4)
            c.wait_until("billionth")
            sub = MathTex(r"1\,\text{ns} = 10^{-9}\,\text{s}", font_size=38)
            sub.next_to(r2[3], DOWN, buff=0.25).align_to(r2[3], LEFT)
            sub[0][0].set_color(GOLD)
            sub[0][4:8].set_color(GOLD)
            self.play(*appear(sub), run_time=1.0)

            c.wait_until("several")
            tag2 = T("several GHz", size=30, color=GOLD).next_to(r2, RIGHT, buff=0.6)
            self.play(*appear(tag2), *flash([chip]), run_time=1.2)

            c.wait_until("inverse")
            inv = MathTex(r"f_c\!\uparrow", r"\iff", r"T_c\!\downarrow", font_size=44)
            inv[0].set_color(YELLOW)
            inv.move_to([4.9, -1.75, 0])
            self.play(*appear(inv), run_time=1.2)
            self.table = [r1, r2, led, chip, tag1, tag2, sub, inv]

    # -- clip 3: more work per second, and the limit ---------------------------------------
    def clip3(self):
        with self.say("c1.clock.3", gap=2.5) as c:
            wave = self.hero.wave
            work = VGroup(T("All things being equal, increasing the clock frequency", size=30),
                          T("increases the ‘work’ that a digital system", size=30),
                          T("can accomplish per unit time", size=30)
                          ).arrange(DOWN, buff=0.12).move_to([0, -2.75, 0])
            work[1][12:18].set_color(YELLOW)
            sweep_clear(self, *appear(work), keep=[wave, self.hero.arrow, self.period_name],  # early: quoted bullet shown whole
                        run_time=min(2.0, c.until("step")))

            c.wait_until("step")
            budget = c.until("limit") + 0.4
            dots = self.drop_dots(wave)
            self.play(*disappear(self.hero.arrow, self.period_name),
                      *during([FadeIn(d, shift=0.5 * DOWN) for d in dots], 0.3, 1),
                      run_time=min(1.4, 0.36 * budget))
            for n in (8, 11):
                new = clock_wave(width=WAVE_W, height=WAVE_H, periods=n).move_to([0, WAVE_Y, 0])
                new_dots = self.drop_dots(new)
                # the wave stays a clean square wave while it compresses: redrawn from the
                # (fractional) period count, edges slide left and new periods enter at the right
                periods = ValueTracker(len(wave._rise))
                live = always_redraw(lambda: square_wave_line(periods.get_value()))
                self.remove(wave)
                self.add(live, wave.ups)
                # old dots/arrows leave before the wave moves; new ones arrive once it has settled
                self.play(*during([FadeOut(u) for u in wave.ups], 0, 0.2),
                          *during([FadeOut(d) for d in dots], 0, 0.2),
                          *during([periods.animate.set_value(n)], 0.2, 0.65),
                          *during([FadeIn(u) for u in new.ups], 0.65, 0.85),
                          *during([FadeIn(d, shift=0.5 * DOWN) for d in new_dots], 0.68, 1),
                          run_time=max(1.0, min(1.5, 0.32 * budget)))
                live.clear_updaters()
                self.remove(live, new.ups)
                self.add(new)
                wave, dots = new, new_dots

            c.wait_until("because every period")
            i = 5
            xa, xb = wave.rising_x(i), wave.rising_x(i + 1)
            band = Rectangle(width=xb - xa, height=2.5).set_stroke(width=0).set_fill(YELLOW, 0.12)
            band.move_to([(xa + xb) / 2, 1.25, 0]).set_z_index(-1)
            self.play(*disappear(*dots), FadeIn(band), run_time=1.2)
            c.wait_until("enough time")
            box = Rectangle(width=xb - xa - 0.08, height=0.85).set_stroke(DIM, 2.5).set_fill(DIM, 0.35)
            box.move_to([(xa + xb) / 2, 0.55, 0])
            blabel = T("the circuit's work for one step", size=30, color=FG).next_to(box, DOWN, buff=0.3)
            self.play(GrowFromCenter(box), *during(appear(blabel), 0.4, 1), run_time=1.5)

            c.wait_until("measure")
            qarrow = dim_arrow(xa, xb, ARROW_Y, guide_bottom=WAVE_Y - WAVE_H / 2,
                               label=MathTex("T_c", "\\,?", font_size=48), gap=0.12)
            question = MathTex(r"\text{how short can }", "T_c", r"\text{ be?}", font_size=48)
            question.set_color(YELLOW).move_to([0, -1.35, 0])
            self.play(*[FadeIn(g) for g in qarrow.guides], GrowFromCenter(qarrow.line),
                      *during(appear(qarrow.label), 0.3, 0.7), *during(appear(question), 0.5, 1),
                      run_time=1.6)  # early: question read whole

    def drop_dots(self, wave):
        """GOLD dots under the wave, one per rising edge (one step each); not yet on screen."""
        y = WAVE_Y - WAVE_H / 2 - 0.55
        return [Dot([wave.rising_x(k), y, 0], radius=0.09, color=GOLD) for k in range(len(wave._rise))]
