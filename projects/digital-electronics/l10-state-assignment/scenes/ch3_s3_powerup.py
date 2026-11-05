"""Chapter 3, scene 3: the power-up problem, three remedies, the traffic light self-starts. Clips c3.power.1 – c3.power.3.

Shared: remedy_cards() (the three numbered cards, per-card .box .num .lines .word(key)) and
selfstart_tag(card) for s4 / s5 / s8. Reuses ch1_s1_hook's traffic_ring / make_ff / lamp_column.
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

S1 = load_scene("ch1_s1_hook")
traffic_ring, make_ff, ring_flash = S1.traffic_ring, S1.make_ff, S1.ring_flash


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the three remedy cards (shared with s4, s5, s8) ----------------------------------------------
REMEDY_LINES = [
    ["Check to see if the", "FSM can eventually", "enter a known state",
     "from any of the", "unused states"],
    ["If not, add additional", "logic to do this, i.e.,", "include unused states",
     "in the state transition", "table along with a", "valid next state"],
    ["Alternatively use", "asynchronous Clear", "and Preset FF inputs",
     "to set a known (used)", "state at power up"],
]
CARD_W, CARD_H, CARD_GAP = 4.3, 3.85, 0.15


def remedy_card(i, size=28):
    """Card i (0-based): GOLD number, slide wording left-aligned. .box .num .lines .word(key)."""
    num = T(str(i + 1), 44, GOLD)
    lines = VGroup(*[T(s, size) for s in REMEDY_LINES[i]]).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.16, width=CARD_W, height=CARD_H)
    box.set_stroke(DIM, 2).set_fill(BG, 1)
    num.move_to(box.get_corner(UL) + _p(0.22 + num.width / 2, -0.2 - num.height / 2))
    lines.next_to(num, DOWN, buff=0.22).align_to(num, LEFT)
    card = VGroup(box, num, lines)
    card.box, card.num, card.lines = box, num, lines

    def word(key):
        # Text has no glyphs for spaces: index glyphs by the space-free string.
        for ln in card.lines:
            if key in ln.text:
                start = len(ln.text[:ln.text.index(key)].replace(" ", ""))
                n = len(key.replace(" ", ""))
                return VGroup(*ln[start:start + n])
        raise ValueError(f"{key!r} not on card {i + 1}")

    card.word = word
    return card


def remedy_cards():
    """The three cards side by side, centred on ORIGIN; .cards[i]."""
    cards = [remedy_card(i) for i in range(3)]
    g = VGroup(*cards).arrange(RIGHT, buff=CARD_GAP)
    g.cards = cards
    return g


def selfstart_tag(card):
    """GREEN 'self-starting' pill just under a card."""
    t = T("self-starting", 30, GREEN)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.5, height=0.62)
    box.set_stroke(GREEN, 2.5).set_fill(BG, 1)
    t.move_to(box)
    g = VGroup(box, t).next_to(card, DOWN, buff=0.2)
    g.box, g.text = box, t
    return g


# ---- clip 1 pieces --------------------------------------------------------------------------------
FF_Y = 0.25
FF_XS = [-1.4, 1.5, 4.4]
FF_S = 0.7
RAIL_Y = 2.05
SW_C = _p(-4.8, FF_Y)


def ff_bit(ff, b):
    return T(b, 44, GREEN).next_to(ff.q_w, RIGHT, buff=0.14)


def power_switch():
    body = RoundedRectangle(corner_radius=0.15, width=1.0, height=1.7).set_stroke(FG, 3).set_fill("#16181D", 1)
    lever = RoundedRectangle(corner_radius=0.08, width=0.66, height=0.66)
    lever.set_stroke(width=0).set_fill(DIM, 1).move_to(body.get_center() + 0.38 * DOWN)
    g = VGroup(body, lever).move_to(SW_C)
    g.body, g.lever = body, lever
    return g


def loop_sketch():
    """Four GREEN used states in a ring (left), two DIM unused ones with RED arrows round (right)."""
    c0 = _p(-2.6, 0.3)
    rad, r = 1.35, 0.45
    pos = [c0 + rad * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, 0, -PI / 2, PI)]
    used = [Circle(radius=r).set_stroke(GREEN, 4).set_fill(BG, 1).move_to(p) for p in pos]
    used_arrows = []
    for i in range(4):
        a, b = pos[i], pos[(i + 1) % 4]
        d = (b - a) / np.linalg.norm(b - a)
        arr = CurvedArrow(a + d * (r + 0.1), b - d * (r + 0.1), angle=-0.5).set_stroke(GREEN, 3)
        arr.set_fill(GREEN, 1)
        used_arrows.append(arr)
    u1, u2 = _p(2.2, 0.3), _p(4.6, 0.3)
    unused = [Circle(radius=r).set_stroke(DIM, 4).set_fill(BG, 1).move_to(p) for p in (u1, u2)]
    def on(c, deg):   # a point on circle c's rim (just outside the stroke), at angle deg
        a = deg * DEGREES
        return c + (r + 0.04) * np.array([np.cos(a), np.sin(a), 0])

    top = CurvedArrow(on(u1, 50), on(u2, 130), angle=-0.9, color=RED, stroke_width=4, tip_length=0.24)
    bot = CurvedArrow(on(u2, -130), on(u1, -50), angle=-0.9, color=RED, stroke_width=4, tip_length=0.24)
    return VGroup(*used_arrows, *used), VGroup(*unused), [top, bot]


def quote(*lines, size=32, y=-2.6):
    g = VGroup(*[T(s, size, FG, slant=ITALIC) for s in lines]).arrange(DOWN, buff=0.14)
    return g.move_to(_p(0, y))


# ---- clip 3 layout --------------------------------------------------------------------------------
RING_HUB = _p(-3.0, -0.75)
RING_S = 0.62
UNUSED = {   # code: (position, target ring state index, next-state code)
    "000": (_p(-5.6, -2.95), 3, "010"),
    "011": (_p(-5.6, 1.0), 0, "100"),
    "101": (_p(-0.25, 1.3), 1, "110"),
    "111": (_p(-0.9, -3.1), 2, "001"),
}
COL1_X, COL2_X = 1.1, 2.95
ROW_Y = [0.35, -0.4, -1.15, -1.9]
HEAD_Y = 1.3


def unused_circle(code):
    pos = UNUSED[code][0]
    circ = Circle(radius=0.52).set_stroke(DIM, 3).set_fill(BG, 1).move_to(pos)
    txt = Mono(code, 30, DIM).move_to(pos)
    g = VGroup(circ, txt)
    g.circ, g.txt = circ, txt
    return g


class PowerUp(NarratedScene):
    def construct(self):
        # ============================================================ c3.power.1
        with self.say("c3.power.1") as c:
            remember = T("“Remember, I said…”", 40, DIM, slant=ITALIC).move_to(_p(0, 0.6))
            self.play(*appear(remember), run_time=1.0)  # early: the lecturer's words, not voiced
            c.wait_until("so here's")
            heading = T("FSM Problems", 50, YELLOW).move_to(_p(0, 3.25))
            self.play(*appear(heading), run_time=min(1.2, c.until("power")))
            c.wait_until("power")

            # power switch and three flip-flops
            sw = power_switch()
            sw_txt = T("OFF", 30, DIM).next_to(sw, DOWN, buff=0.25)
            ffs = [make_ff(size=56).scale(FF_S, about_point=ORIGIN).shift(_p(x, FF_Y)) for x in FF_XS]
            leds = [Circle(radius=0.17).set_stroke(DIM, 2).set_fill(S1.LAMP_OFF, 1)
                    .move_to(_p(ff.box.get_x(), ff.box.get_top()[1] + 0.32)) for ff in ffs]
            rail = VMobject().set_points_as_corners(
                [sw.get_top(), _p(SW_C[0], RAIL_Y), _p(ffs[-1].box.get_x(), RAIL_Y)]).set_stroke(DIM, 3)
            drops = [Line(_p(ld.get_x(), RAIL_Y), ld.get_top()).set_stroke(DIM, 3) for ld in leds]
            self.play(*during(disappear(remember), 0, 0.4), *during(
                [FadeIn(VGroup(sw, sw_txt, rail, *drops)), *[FadeIn(f) for f in ffs], *[FadeIn(ld) for ld in leds]],
                0.45, 1.0), run_time=min(1.6, c.until("each flip-flop")))
            c.wait_until("comes up")
            sw_on = T("ON", 30, GREEN).move_to(sw_txt)
            self.play(sw.lever.animate.move_to(sw.body.get_center() + 0.38 * UP).set_fill(GREEN, 1),
                      *swap(sw_txt, sw_on),
                      rail.animate.set_stroke(GREEN), *[d.animate.set_stroke(GREEN) for d in drops],
                      *[ld.animate.set_fill(GREEN, 1).set_stroke(GREEN) for ld in leds],
                      run_time=1.0)
            # Q values flicker, then settle at random: 1, 0, 1
            seq = [["1", "1", "0"], ["0", "1", "1"], ["1", "0", "1"]]
            vals = [ff_bit(f, b) for f, b in zip(ffs, seq[0])]
            self.play(*[FadeIn(v) for v in vals], run_time=0.4)
            for bits in seq[1:]:
                new = [ff_bit(f, b) for f, b in zip(ffs, bits)]
                anims = []
                for o, n in zip(vals, new):
                    anims += swap(o, n)
                self.play(*anims, run_time=0.5)
                vals = new
            c.wait_until("so the machine")
            cap1 = quote("The state of the FFs could by chance", "be in one of the unused states")
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("stuck")

            # the stuck loop sketch
            used, unused, red = loop_sketch()
            sweep_clear(self, *[FadeIn(m) for m in (*used, *unused)], keep=[heading, cap1])
            cap2 = quote("stuck in some unanticipated sequence of states", "which never goes back to a used state")
            self.play(*[Create(a) for a in red],
                      *during(disappear(cap1), 0, 0.4),
                      *during(appear(cap2, shift=None), 0.6, 1.0), run_time=1.6)
            for _ in range(2):
                if c.until() < 2.2:
                    break
                self.play(Succession(*[VShowPassingFlash(a.copy().set_stroke(YELLOW, 7), time_width=0.6)
                                       for a in red]), run_time=2.0)

        # ============================================================ c3.power.2
        with self.say("c3.power.2") as c:
            question = T("What can be done?", 50, YELLOW).move_to(heading)
            self.play(*swap(heading, question), run_time=min(1.3, c.until("one")))
            board = remedy_cards().move_to(_p(0, -0.15))
            cards = board.cards
            c.wait_until("one")
            self.play(*during(disappear(used, unused, *red, cap2), 0, 0.45),  # early: slide card, read whole
                      *during(appear(cards[0], shift=None), 0.5, 1.0), run_time=1.6)
            tag = selfstart_tag(cards[0])
            c.wait_until("called", own_word=tag.text)
            self.play(*appear(tag), FlashAround(cards[0].word("eventually"), color=GREEN),
                      run_time=1.2)
            c.wait_until("two")
            self.play(*appear(cards[1], shift=None), run_time=1.0)  # early: slide card, read whole
            c.wait_until("three")
            self.play(*appear(cards[2], shift=None), run_time=1.0)  # early: slide card, read whole

        # ============================================================ c3.power.3
        with self.say("c3.power.3") as c:
            group = VGroup(board, tag)
            group.generate_target()
            group.target.scale(0.4).move_to(_p(0, 2.55))
            for k in (1, 2):
                group.target[0][k].set_opacity(DIMMED)
            group.target[0][0].box.set_stroke(YELLOW, 2)
            ring = traffic_ring(code_size=48).scale(RING_S)
            ring.shift(RING_HUB - ring._hub.get_center())
            self.play(*during(disappear(question), 0, 0.4), *during(MoveToTarget(group), 0.3, 0.85),
                      *during(FadeIn(ring), 0.55, 1.0), run_time=min(2.4, c.until("codes")))
            c.wait_until("codes")
            codes = [ring.code_at(i, t) for i, t in enumerate(["100", "110", "001", "010"])]
            self.play(*appear(*codes, lag=0.3), run_time=1.4)
            c.wait_until("four patterns")
            circles = {k: unused_circle(k) for k in UNUSED}
            self.play(*appear(*circles.values(), shift=None, lag=0.4), run_time=1.8)
            c.wait_until("feed")

            # the table
            h1 = VGroup(T("Start", 30), T("state", 30)).arrange(DOWN, buff=0.08).move_to(_p(COL1_X, HEAD_Y))
            h2 = VGroup(T("Next state", 30), T("logic output", 30)).arrange(DOWN, buff=0.08)
            h2.move_to(_p(COL2_X, HEAD_Y))
            hline = Line(_p(0.45, 0.82), _p(4.15, 0.82)).set_stroke(DIM, 2)
            vline = Line(_p(1.95, 1.72), _p(1.95, -2.3)).set_stroke(DIM, 2)
            self.play(*appear(h1, h2), FadeIn(hline), FadeIn(vline), run_time=1.2)
            outs = []
            for k, (code, cue, nxt) in enumerate([("000", "r1", "r2"), ("011", "r2", "r3"),
                                                  ("101", "r3", "r4"), ("111", "r4", "all")]):
                c.wait_until(cue)
                pos, idx, nxt_code = UNUSED[code]
                s = Mono(code, 36, FG).move_to(_p(COL1_X, ROW_Y[k]))
                o = Mono(nxt_code, 36, GREEN).move_to(_p(COL2_X, ROW_Y[k]))
                outs.append(o)
                target = ring.circles[idx]
                d = target.get_center() - pos
                d = d / np.linalg.norm(d)
                arr = Arrow(pos + d * 0.52, target.get_center() - d * (target.width / 2),
                            buff=0.06, stroke_width=5, color=GREEN, tip_length=0.26,
                            max_tip_length_to_length_ratio=0.4)
                rt = min(1.6, 0.6 * c.until(nxt))
                self.play(*appear(s, o, lag=0.35), GrowArrow(arr), ring_flash(target), run_time=rt)

            c.wait_until("all")
            br = Brace(VGroup(*outs), RIGHT, buff=0.25).set_color(GREEN)
            br_t = VGroup(T("Which are all", 30, GREEN), T("valid states", 30, GREEN)).arrange(
                DOWN, buff=0.08, aligned_edge=LEFT).next_to(br, RIGHT, buff=0.2)
            self.play(GrowFromCenter(br), *appear(br_t, shift=None), run_time=1.2)  # early: slide bracket
            c.wait_until("into the cycle")
            verdict = T("So it does self start", 36, GREEN).move_to(_p(2.6, -2.95))
            self.play(*appear(verdict), run_time=1.0)  # early: slide wording, voiced as "self-starting"
            c.wait_until("so the traffic light")
            self.play(FlashAround(tag, color=GREEN), FlashAround(verdict, color=GREEN), run_time=1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
