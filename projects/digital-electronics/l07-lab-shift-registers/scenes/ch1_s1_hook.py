"""Chapter 1, scene 1: hook: spaghetti fails, neat wiring works, the road. Clips c1.hook.1 – c1.hook.3.

Reuses s6's logbook_page / bare_board / connection_wires (its board is s3's Breadboard, 1.2x wide),
so the neat layout is exactly s6's finished board. No LED on the board (producer's rule): failure is a
RED "?", success a GREEN tick. Part-2 sketch: L8 ch2_s3's build_chain(), drawn DIM with a YELLOW clock.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

S3 = load_scene("ch1_s3_breadboard")
S6 = load_scene("ch1_s6_wiring")


def _load_l8():
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch2_s3_shiftreg.py"
    spec = importlib.util.spec_from_file_location("_l08_ch2_s3_shiftreg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8 = _load_l8()


def _p(x, y):
    return np.array([x, y, 0.0])


# ── layout ────────────────────────────────────────────────────────────────────────
PAGE_S, PAGE_AT = 0.68, _p(-4.4, -0.2)
BOARD_S, BOARD_TO = 0.84, _p(2.28, -0.2)
CORNER = _p(5.55, 3.45)


def place_board(m):
    return m.scale(BOARD_S, about_point=S6.BOARD_AT).shift(BOARD_TO - S6.BOARD_AT)


def part2_sketch():
    """L6/L8's three-flip-flop chain, DIM, with its clock in YELLOW; centred on ORIGIN."""
    C = L8.build_chain()
    clock = [C.bus, *C.jdots, *C.clk_ws, C.clk_l]
    for m in C.all:
        if not any(m is k for k in clock):
            m.set_color(DIM)
    for f in C.ffs:
        f.tri.set_fill(BG, 1)
    texts = [*C.names, *C.qls, C.din, C.clk_l]
    for f in C.ffs:
        f.remove(f.d_l, f.q_l)
        texts += [f.d_l, f.q_l]
    lines = VGroup(*[m for m in C.all if not any(m is t for t in texts)])
    texts = VGroup(*texts)
    shift = -VGroup(lines, texts).get_center()
    lines.shift(shift)
    texts.shift(shift)
    return lines, texts


def spaghetti(p1, p2, c1, c2, color, width=7):
    """A long looping jumper wire: a cubic from p1 to p2 through handles c1, c2 (board coords)."""
    path = CubicBezier(p1, _p(*c1), _p(*c2), p2)
    path.set_stroke(color, width)
    path.set_stroke(S3.WIRE_DARK, width + 3, background=True)
    return VGroup(path, Dot(p1, radius=0.06, color=S3.LEG_GREY), Dot(p2, radius=0.06, color=S3.LEG_GREY))


# handles for the six connections + two power wires, all inside the board, looping across the chip
SPAG_HANDLES = [((3.5, 3.2), (5.5, -3.2)), ((5.8, -2.8), (4.5, 3.0)), ((-3.0, 3.0), (-2.8, -3.2)),
                ((6.0, -1.0), (-3.0, 3.2)), ((-3.1, -3.2), (6.2, 0.5)), ((-3.0, 0.2), (5.0, 3.2))]
POWER_HANDLES = [((2.0, -2.6), (-3.2, -1.0)), ((-2.0, 2.6), (5.0, 2.6))]


# ── road icons ────────────────────────────────────────────────────────────────────
def icon_box():
    body = Rectangle(width=1.3, height=0.75).set_stroke(BLUE, 4).set_fill(BLUE, 0.15)
    lid = Polygon(_p(-0.65, 0.375), _p(0.65, 0.375), _p(0.45, 0.75), _p(-0.85, 0.75)).set_stroke(BLUE, 4)
    clasp = Rectangle(width=0.22, height=0.14).set_stroke(BLUE, 3).move_to(body.get_top() + DOWN * 0.12)
    return VGroup(body, lid, clasp).move_to(ORIGIN)


def icon_board():
    b = S3.Breadboard(cols=26, pitch=0.4)
    return b.scale_to_fit_width(1.6).move_to(ORIGIN)


def icon_chip():
    ch = S3.DipChip(14, "74HC00", pitch=0.2)
    ch.remove(ch.label)
    ch.body.set_stroke(DIM, 3)
    return ch.scale_to_fit_width(1.4).move_to(ORIGIN)


def icon_wire():
    w = S6.route([_p(-0.6, -0.25), _p(-0.6, 0.25), _p(0.6, 0.25), _p(0.6, -0.25)], BLUE)
    return w.move_to(ORIGIN)


def icon_checklist():
    sheet = Rectangle(width=1.0, height=1.25).set_stroke(FG, 3)
    rows = VGroup()
    for i, y in enumerate((0.33, 0.0, -0.33)):
        ln = Line(_p(-0.12, y), _p(0.36, y)).set_stroke(DIM, 4)
        tk = check_mark().scale(0.45).move_to(_p(-0.28, y))
        if i == 2:
            tk = Square(0.22).set_stroke(DIM, 3).move_to(_p(-0.28, y))
        rows.add(ln, tk)
    return VGroup(sheet, rows).move_to(ORIGIN)


def icon_probe():
    body = RoundedRectangle(corner_radius=0.08, width=0.22, height=0.8).set_stroke(RED, 4).set_fill(RED, 0.3)
    grip = Line(_p(-0.18, -0.05), _p(0.18, -0.05)).set_stroke(RED, 4)
    tip = Line(_p(0, 0.4), _p(0, 0.75)).set_stroke(FG, 4)
    cable = CubicBezier(_p(0, -0.4), _p(0, -0.8), _p(0.6, -0.4), _p(0.65, -0.8)).set_stroke(RED, 4)
    g = VGroup(cable, body, grip, tip).rotate(-PI / 6)
    return g.move_to(ORIGIN)


ROAD = [("box", icon_box), ("breadboard", icon_board), ("chips", icon_chip),
        ("wiring", icon_wire), ("order", icon_checklist), ("faults", icon_probe)]
ROAD_CUES = ["box", "board", "chips", "wiring", "order", "faults"]


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c1.hook.1: title card; the promised shift register, parked in the corner as "Part 2"
    def clip1(self):
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · Before the hardware lab")
            if card.title.width > 12.6:
                card.title.scale_to_fit_width(12.6)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course), run_time=0.8)  # early: title card, read as a whole
            self.play(*appear(card.part), run_time=0.8)  # early: title card, read as a whole
            c.wait_until("promise")
            sk, sk_txt = part2_sketch()
            for m in (sk, sk_txt):
                m.shift(UP * 0.4)
            self.sketch = sk
            sweep_clear(self, FadeIn(sk, shift=0.2 * UP), FadeIn(sk_txt, shift=0.2 * UP), run_time=1.4)
            tag = T("Part 2", 40, DIM).next_to(sk, DOWN, buff=0.45)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=0.9)
            c.wait_until("hardware labs")
            small = sk.copy().scale_to_fit_width(2.0).move_to(CORNER)
            tag_t = tag.copy().scale(0.7).next_to(small, LEFT, buff=0.25)
            self.play(Transform(sk, small), Transform(tag, tag_t), *during(disappear(sk_txt), 0, 0.35), run_time=min(1.8, c.until(floor=0.8)))
            self.tag = tag

    # c1.hook.2: diagram + empty board; spaghetti; it fails
    def clip2(self):
        with self.say("c1.hook.2") as c:
            page = S6.logbook_page()
            page_txt = VGroup(page.ic_label, *page.gate_labels, page.tag, *page.pin_labels.values())
            page.remove(page.ic_label)
            VGroup(page, page_txt).move_to(UP * 0.1)
            b, chip, nums, power = S6.bare_board()
            neat = S6.connection_wires(b)
            ends = [(w.path.get_start(), w.path.get_end()) for w in neat]
            p_ends = [(w[0].get_start(), w[0].get_end()) for w in power]
            spag = [spaghetti(p1, p2, h1, h2, w.path.get_stroke_color())
                    for (p1, p2), (h1, h2), w in zip(ends, SPAG_HANDLES, neat)]
            spag += [spaghetti(p1, p2, h1, h2, col, width=6)
                     for (p1, p2), (h1, h2), col in zip(p_ends, POWER_HANDLES, (GOLD, DIM))]
            for m in (b, chip, *power, *neat, *spag):
                place_board(m)
            self.page, self.b, self.chip, self.power, self.neat = page, b, chip, power, neat
            self.play(FadeIn(page, shift=0.3 * UP), FadeIn(page_txt, shift=0.3 * UP), run_time=1.0)
            c.wait_until("empty breadboard")
            small = page.copy().scale(PAGE_S).move_to(PAGE_AT)
            self.play(Transform(page, small), *during(disappear(page_txt), 0, 0.35),
                      *during([FadeIn(b)], 0.45, 1), run_time=1.3)
            self.play(FadeIn(chip, shift=0.25 * DOWN), run_time=0.8)
            c.wait_until("anyhow")
            order = [spag[i] for i in (1, 6, 3, 0, 4, 7, 2, 5)]
            self.play(LaggedStart(*[Create(w) for w in order], lag_ratio=0.45),
                      run_time=min(4.2, c.until("electrical spaghetti") - 0.2))
            self.spag = order
            lab = set_backstroke(T("electrical spaghetti", 40, RED, slant=ITALIC), BG, 6)
            lab.move_to(_p(0.6, 3.3))
            c.wait_until(own_word=lab)
            self.play(*appear(lab), run_time=1.0)
            self.lab = lab
            c.wait_until("dark")
            q = set_backstroke(T("?", 150, RED, weight=BOLD), BG, 10).move_to(chip.get_center() + UP * 0.1)
            q.set_z_index(10)
            self.play(FadeIn(q, scale=0.6), run_time=0.8)
            self.q = q

    # c1.hook.3: rewind, neat wiring works; the question; the road
    def clip3(self):
        with self.say("c1.hook.3") as c:
            rw = VGroup(Triangle().rotate(PI / 2), Triangle().rotate(PI / 2)).set_stroke(FG, 0).set_fill(FG, 1)
            rw.arrange(RIGHT, buff=-0.15).scale(0.45)
            rw = VGroup(Circle(radius=0.75).set_stroke(FG, 4).set_fill(BG, 0.85), rw.move_to(ORIGIN))
            rw.move_to(self.chip.get_center()).set_z_index(10)
            self.play(*swap(self.q, rw), *disappear(self.lab), run_time=0.8)
            self.play(LaggedStart(*[Uncreate(w) for w in reversed(self.spag)], lag_ratio=0.3),
                      run_time=max(0.6, c.until("neat") - 0.1))
            c.wait_until("neat")
            neat = [*self.power, *self.neat]
            self.play(*disappear(rw), run_time=0.6)
            self.play(LaggedStart(*[Create(w) for w in neat], lag_ratio=0.35),
                      run_time=min(2.6, c.until("this time") - 0.1))
            c.wait_until("works")
            tick = check_mark(GREEN).scale(3.2).move_to(self.chip.get_center() + UP * 0.1)
            tick.set_stroke(width=16).set_z_index(10)
            self.play(GrowFromCenter(tick), run_time=1.0)

            # the question: the board shrinks up, two lines below
            c.wait_until("question")
            parts = [self.b, self.chip, *neat, tick]
            self.board_parts = parts
            ctr = self.b.get_center()
            self.play(*disappear(self.page), run_time=0.8)
            self.play(*[m.animate.scale(0.48, about_point=ctr).shift(_p(0, 1.45) - ctr) for m in parts],
                      run_time=1.4)
            q1 = T("diagram → a circuit that works first time", 44,
                   t2c={"diagram": YELLOW, "works first time": GREEN})
            q2 = T("fault → found fast", 44, t2c={"fault": RED, "found fast": GREEN})
            VGroup(q1, q2).arrange(DOWN, buff=0.45).move_to(_p(0, -1.9))
            c.wait_until(own_word=q1)
            self.play(*appear(q1), run_time=1.0)
            c.wait_until(own_word=q2)
            self.play(*appear(q2), run_time=1.0)

            # the road: six icons, dim, each lit as it is named
            c.wait_until("road")
            icons, labels, veils = [], [], []
            xs = [-5.5 + 2.2 * i for i in range(6)]
            for (name, make), x in zip(ROAD, xs):
                ic = make().move_to(_p(x, -0.4))
                lb = T(name, 32).next_to(_p(x, -1.3), DOWN, buff=0)
                veil = Rectangle(width=2.0, height=2.6).set_stroke(width=0).set_fill(BG, 0.75)
                veil.move_to(_p(x, -0.75)).set_z_index(20)
                icons.append(ic)
                labels.append(lb)
                veils.append(veil)
            self.add(*veils)
            qs = VGroup(q1, q2)
            qt = qs.copy().scale(0.75).arrange(DOWN, buff=0.3).move_to(_p(-0.6, 2.55))
            self.play(*disappear(*self.board_parts), run_time=0.7)
            self.play(Transform(q1, qt[0]), Transform(q2, qt[1]),  # early: the road shown whole, then walked
                      *during([FadeIn(m) for m in icons + labels], 0.4, 1), run_time=1.3)
            for i, cue in enumerate(ROAD_CUES):
                c.wait_until(cue)
                self.play(FadeOut(veils[i]), run_time=min(0.7, c.until(floor=0.3)))
            rest = c.until(floor=0.5)
            self.play(FlashAround(VGroup(icons[0], labels[0]), color=YELLOW, buff=0.2),
                      icons[0].animate.scale(1.15), labels[0].animate.set_color(YELLOW),
                      run_time=min(1.2, rest))
