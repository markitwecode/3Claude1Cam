"""Chapter 1, scene 1: title card; the traffic light's four-state ring; flip-flops hold bits; two, three
or four flip-flops give different codes; which pattern for which state?; the lecture's road.
Clips c1.hook.1 – c1.hook.3.

Chapter-wide helper owned here (s3, s4, s8 import it):
- traffic_ring(codes=None, code_size=36, code_gap=0.3, rx=3.0, ry=1.7, r=0.72) -> VGroup centred
  on ORIGIN. Four BLUE state circles, clockwise from 12 o'clock: 0 red (top), 1 red-and-amber
  (right), 2 green (bottom), 3 amber (left); each holds a three-lamp column (red, amber, green; lit
  in its own colour, dark when off). Slightly curved DIM-FG arrows i -> i+1 (arrows[3] amber -> red).
  codes: optional list of 4 strings (state order above) -> GREEN Mono codes beside each circle
  (right of top/right/bottom circles, left of the left one), `code_gap` from the circle edge.
  Attributes: .states[i] (VGroup circle+lamps), .circles, .lamps[i] (3 lamp Circles), .arrows,
  .codes (list of Mono, or [] without codes), .hub (centre point).
  ring.code_at(i, text, gap=None) -> a new GREEN Mono placed where code i goes (follows the ring's
  current scale/position; not added to the ring). ring.inner(i, d=0.25) -> point just inside the
  ring next to state i (where the YELLOW dot sits). ring.slot(i, gap) -> point gap/2 out from
  circle i on the code side.
  Native size about 7.4 x 4.8 without codes.
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
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the traffic-light ring (chapter-wide) -------------------------------------------------------
LAMP_RED = "#FC4A3F"
LAMP_AMBER = "#FFB22E"
LAMP_GREEN = "#5DD05A"
LAMP_OFF = "#2A2E36"
STATE_LAMPS = [(1, 0, 0), (1, 1, 0), (0, 0, 1), (0, 1, 0)]   # red, red+amber, green, amber
STATE_NAMES = ["red", "red and amber", "green", "amber"]


def lamp_column(lit, scale=1.0):
    housing = RoundedRectangle(corner_radius=0.12, width=0.44, height=1.08)
    housing.set_stroke(DIM, 2).set_fill("#16181D", 1)
    lamps = []
    for k, (on, col) in enumerate(zip(lit, (LAMP_RED, LAMP_AMBER, LAMP_GREEN))):
        lamp = Circle(radius=0.135).move_to(_p(0, 0.34 - 0.34 * k))
        lamp.set_stroke(width=0).set_fill(col if on else LAMP_OFF, 1)
        lamps.append(lamp)
    g = VGroup(housing, *lamps)
    g.housing, g.lamps = housing, lamps
    return g.scale(scale)


def traffic_ring(codes=None, code_size=36, code_gap=0.3, rx=3.0, ry=1.7, r=0.72):
    centres = [_p(0, ry), _p(rx, 0), _p(0, -ry), _p(-rx, 0)]
    ring = VGroup()
    states, circles, lamps = [], [], []
    for i, c in enumerate(centres):
        circ = Circle(radius=r).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(c)
        col = lamp_column(STATE_LAMPS[i], scale=r / 0.62).move_to(c)
        st = VGroup(circ, col)
        states.append(st)
        circles.append(circ)
        lamps.append(col.lamps)
    arrows = []
    for i in range(4):
        a, b = centres[i], centres[(i + 1) % 4]
        d = (b - a) / np.linalg.norm(b - a)
        start, end = a + d * (r + 0.12), b - d * (r + 0.12)
        arr = CurvedArrow(start, end, angle=-0.45).set_stroke(FG, 3)
        arr.set_fill(FG, 1)
        arrows.append(arr)
    ring.add(*arrows, *states)
    hub = VectorizedPoint(ORIGIN)
    ring.add(hub)
    ring.states, ring.circles, ring.lamps, ring.arrows, ring._hub = states, circles, lamps, arrows, hub
    ring._r0, ring._code_size, ring._gap = r, code_size, code_gap

    def scale_now():
        return ring.circles[0].width / (2 * ring._r0)

    def side(i):
        return LEFT if i == 3 else RIGHT

    def slot(i, gap=None):
        g = (ring._gap if gap is None else gap) * scale_now()
        circ = ring.circles[i]
        edge = circ.get_left() if i == 3 else circ.get_right()
        return edge + side(i) * g / 2

    def code_at(i, text, gap=None):
        s = scale_now()
        g = (ring._gap if gap is None else gap) * s
        m = Mono(text, size=ring._code_size, color=GREEN).scale(s)
        circ = ring.circles[i]
        if i == 3:
            m.next_to(circ, LEFT, buff=g)
        else:
            m.next_to(circ, RIGHT, buff=g)
        m.set_y(circ.get_y())
        return m

    def inner(i, d=0.25):
        c = ring.circles[i].get_center()
        h = ring._hub.get_center()
        v = (h - c) / np.linalg.norm(h - c)
        return c + v * (ring.circles[i].width / 2 + d * scale_now())

    ring.slot, ring.code_at, ring.inner = slot, code_at, inner
    ring.codes = []
    if codes is not None:
        ring.codes = [code_at(i, t) for i, t in enumerate(codes)]
        ring.add(*ring.codes)
    return ring


# ---- L6 make_ff (D flip-flop), copied from ch2_s1_hook -------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D", size=36):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, size, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", size, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar(size).move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# ---- this scene's layout --------------------------------------------------------------------------
RING_C = _p(0, 1.0)
FF_Y = -2.45
FF_PITCH = 2.5
CODE_GAP = 0.8          # room for the "?" between each state and its code
CODES = {
    2: ["00", "01", "10", "11"],
    3: ["100", "110", "001", "010"],
    4: ["1000", "0100", "0010", "0001"],
}


def ff_unit(x, bit):
    ff = make_ff(size=56).scale(0.55, about_point=ORIGIN).shift(_p(x, FF_Y))
    val = T(bit, 44, GREEN).next_to(ff.q_w, RIGHT, buff=0.14)
    return ff, val


def ff_x(i, n):
    return (i - (n - 1) / 2) * FF_PITCH - 0.2


def chip(text, prefix, icon=None, color=FG, size=30):
    t = T(text, size, color, t2c={prefix: GOLD})
    parts = [t]
    if icon is not None:
        icon.next_to(t, LEFT, buff=0.22)
        parts = [icon, t]
    body = VGroup(*parts)
    box = RoundedRectangle(corner_radius=0.14, width=body.width + 0.5, height=0.78)
    box.set_stroke(DIM, 2).set_fill(BG, 1).move_to(body)
    g = VGroup(box, *parts)
    g.box, g.text = box, t
    return g


def ring_flash(circ):
    """A flash that runs round a state circle (FlashAround's square box read as stray brackets)."""
    halo = Circle(radius=circ.width / 2 + 0.1).move_to(circ).set_stroke(YELLOW, 5)
    return VShowPassingFlash(halo, time_width=1.0)


def wave_icon():
    pts = [(0, 0), (0.12, 0), (0.12, 0.3), (0.3, 0.3), (0.3, 0), (0.48, 0), (0.48, 0.3), (0.66, 0.3)]
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(GREEN, 3)


class Hook(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- c1.hook.1
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · Which bits for which state?")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole
            c.wait_until("lights")

            ring = traffic_ring(code_gap=CODE_GAP).shift(RING_C)
            sweep_clear(self, AnimationGroup(*[FadeIn(m) for m in ring.arrows], *[FadeIn(s, scale=0.9) for s in ring.states],
                                             lag_ratio=0.12), run_time=min(1.8, c.until("red")))
            c.wait_until("red")

            dot = Dot(ring.inner(0), radius=0.11, color=YELLOW)
            self.play(FadeIn(dot, scale=0.5), ring_flash(ring.circles[0]), run_time=0.7)
            for i, cue in enumerate(["red and amber", "then green", "then amber", "back to red"]):
                c.wait_until(cue)
                nxt = (i + 1) % 4
                self.play(dot.animate.move_to(ring.inner(nxt)), ring_flash(ring.circles[nxt]),
                          run_time=0.8)
            c.wait_until("built from")

            units = [ff_unit(ff_x(0, 1), "0")]
            ff_a, val_a = units[0]
            self.play(FadeIn(ff_a, shift=0.25 * UP), run_time=1.0)
            c.wait_until("zero")
            self.play(*appear(val_a, shift=None), run_time=0.7)
            c.wait_until("a one")
            v1 = T("1", 44, GREEN).move_to(val_a)
            self.play(*swap(val_a, v1), run_time=min(0.9, max(0.4, c.remaining - 0.05)))
            units[0] = (ff_a, v1)

        # ---------------------------------------------------------------- c1.hook.2
        with self.say("c1.hook.2") as c:
            # {two}: a second flip-flop; red's pattern 00 (the dot sits on red)
            ff_b, val_b = ff_unit(ff_x(0, 2), "0")
            v0 = T("0", 44, GREEN).move_to(units[0][1]).shift(RIGHT * FF_PITCH / 2)
            self.play(units[0][0].animate.shift(RIGHT * FF_PITCH / 2),
                      *swap(units[0][1], v0, shift=None),
                      run_time=1.0)
            self.play(FadeIn(ff_b, shift=0.25 * RIGHT), *appear(val_b, shift=None), run_time=1.0)
            units = [(ff_b, val_b), (units[0][0], v0)]
            c.wait_until("codes2")

            codes = [ring.code_at(i, t, gap=CODE_GAP) for i, t in enumerate(CODES[2])]
            self.play(*appear(*codes, shift=None, lag=0.5), run_time=min(2.6, c.until("three")))
            c.wait_until("three")

            # {three}: a third flip-flop slides in; codes become Lecture 9's
            for n, cue in ((3, "three"), (4, "four")):
                c.wait_until(cue)
                bits = CODES[n][0]            # red's code, left to right = leftmost flip-flop first
                ff_n, val_n = ff_unit(ff_x(0, n), bits[0])
                anims = [u[0].animate.shift(RIGHT * FF_PITCH / 2) for u in units]
                new_units = [(ff_n, val_n)]
                for k, (f, v) in enumerate(units):
                    target_bit = bits[k + 1]
                    nv = T(target_bit, 44, GREEN).move_to(v).shift(RIGHT * FF_PITCH / 2)
                    if v.text != target_bit:
                        anims += swap(v, nv, shift=None)
                    else:
                        anims.append(Transform(v, nv))
                        nv = v
                    new_units.append((f, nv))
                new_codes = [ring.code_at(i, t, gap=CODE_GAP) for i, t in enumerate(CODES[n])]
                edits = []            # all four codes change together: old out whole, new in whole
                for old, new in zip(codes, new_codes):
                    edits += swap(old, new, shift=None)
                self.play(*anims, during([FadeIn(ff_n, shift=0.25 * RIGHT)], 0.4, 1)[0],
                          *during(appear(val_n, shift=None), 0.4, 1), *edits, run_time=1.5)
                codes = new_codes
                units = new_units

            c.wait_until("question")
            # {question}: flip-flops make way for the question; "?" between each state and its code
            cap = T("Which bits for which state?", 44)
            cap.move_to(_p(0, -2.6))
            qs = [T("?", 40, YELLOW).move_to(ring.slot(i, CODE_GAP)) for i in range(4)]
            ff_parts = [m for u in units for m in u]
            self.play(*disappear(*ff_parts), run_time=0.8)
            self.play(*appear(cap, shift=None), *appear(*qs, lag=0.15), run_time=1.0)
            for n in (2, 3):
                self.wait(min(0.6, c.remaining * 0.3))
                new_codes = [ring.code_at(i, t, gap=CODE_GAP) for i, t in enumerate(CODES[n])]
                sw = []
                for old, new in zip(codes, new_codes):
                    sw += swap(old, new)
                self.play(*sw, run_time=min(0.9, max(0.4, c.remaining - 0.1)))
                codes = new_codes

        # ---------------------------------------------------------------- c1.hook.3
        with self.say("c1.hook.3") as c:
            # {road}: the ring shrinks to the left
            self.play(*disappear(*codes, *qs, cap, dot), run_time=0.8)
            self.play(ring.animate.scale(0.5).move_to(_p(-4.8, 0)), run_time=1.3)

            road_x = -2.5
            ys = [2.6, 1.3, 0.0, -1.3, -2.6]
            road = Line(_p(road_x, ys[0]), _p(road_x, ys[-1])).set_stroke(DIM, 3)
            stops = [Dot(_p(road_x, y), radius=0.09, color=DIM) for y in ys]
            self.play(Create(road), *[FadeIn(s) for s in stops[1:]], run_time=min(1.0, c.until("counter")))
            c.wait_until("counter")

            specs = [
                ("counter", "Parts 1–2: one counter, three ways", "Parts 1–2:", wave_icon()),
                ("wake", "Part 3: waking up in an unused pattern", "Part 3:", None),
                ("onehot", "Part 4: one-hot", "Part 4:", None),
                ("exam", "Parts 5–6: an exam machine, two ways", "Parts 5–6:", None),
            ]
            chips = []
            for k, (cue, text, prefix, icon) in enumerate(specs):
                c.wait_until(cue)
                ch = chip(text, prefix, icon)
                ch.next_to(_p(road_x + 0.35, ys[k + 1]), RIGHT, buff=0)
                chips.append(ch)
                self.play(*appear(ch, shift=0.2 * LEFT), stops[k + 1].animate.set_color(YELLOW),
                          run_time=0.9)  # early: a road chip, read as the voice names the part
            c.wait_until("refresh")

            ref = chip("refresher: Lecture 9", "Lecture 9", color=FG, size=30)
            ref.box.set_stroke(YELLOW, 3)
            ref.next_to(_p(road_x + 0.35, ys[0]), RIGHT, buff=0)
            self.play(*appear(ref, shift=0.2 * LEFT), FadeIn(stops[0]), *set_alpha(chips, 0.5),
                      *[s.animate.set_color(DIM) for s in stops[1:]], run_time=1.0)  # early: chip named by the sentence
            self.play(FlashAround(ref, color=YELLOW, run_time=1.5, time_width=1.5),
                      stops[0].animate.set_color(YELLOW), run_time=1.5)
            c.wait_until(None)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
