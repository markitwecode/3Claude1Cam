"""Chapter 7, scene 1: hook: the series RC circuit and its one complex number. Clips c7.hook.1 – c7.hook.4.

Owns the chapter's circuit: `circuit(center, scale)` (imported by s2, s3, s4, s6). Same drawing as
ch6 s6's closing shot (copied), recoloured to ch7's palette: I GOLD, R BLUE, C PINK, V FG.
Ends on `handover_shot()`: the circuit (CIRC_POS, CIRC_SCALE) with "V = ? · I", the YELLOW box on
"?" and its PINK "complex" tag. s2 opens on it.
"""
# style: 2
# handover: next
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

# ---------------------------------------------------------------- the chapter's circuit
# raw geometry (ch6 s6's drawing)
_L, _RX, _TOP, _BOT = -5.0, 0.4, 0.15, -2.75
_CY = (_TOP + _BOT) / 2
_Z0, _Z1 = -3.3, -1.3
_GAP = 0.14

CIRC_POS = np.array([-2.55, 0.0, 0.0])     # final (handover) centre of the whole circuit group
CIRC_SCALE = 1.1
EQ_POS = np.array([4.2, 0.0, 0.0])


def tex(*parts, size=44, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def circuit(center=CIRC_POS, scale=CIRC_SCALE):
    """The series RC circuit (Example 32, notes p. 28). Returns a VGroup with named parts:
    .wires (VGroup of 7 Lines), .source (VGroup(circle, ∼)), .resistor (zigzag), .capacitor
    (VGroup(plate1, plate2)), .current (GOLD Arrow, bottom wire, pointing left), and labels
    .V .R .C .I. The whole group's bounding-box centre is put at `center`, scaled by `scale`
    (scale 1 = ch6's size, 7.3 x 4.3 incl. labels)."""
    w = dict(color=FG, stroke_width=3)
    src_c = Circle(radius=0.42, color=FG, stroke_width=3).move_to([_L, _CY, 0])
    sim = tex(r"\sim", size=48).move_to(src_c)
    v_lbl = tex("V", size=40).next_to(src_c, LEFT, buff=0.22)
    zx = np.linspace(_Z0, _Z1, 9)
    zig = VMobject().set_points_as_corners(
        [[x, _TOP + (0 if k in (0, 8) else (0.22 if k % 2 else -0.22)), 0]
         for k, x in enumerate(zx)]).set_stroke(BLUE, 3)
    r_lbl = tex("R", size=40, color=BLUE).move_to([(_Z0 + _Z1) / 2, _TOP + 0.6, 0])
    p1 = Line([_RX - 0.45, _CY + _GAP, 0], [_RX + 0.45, _CY + _GAP, 0], color=PINK, stroke_width=4)
    p2 = Line([_RX - 0.45, _CY - _GAP, 0], [_RX + 0.45, _CY - _GAP, 0], color=PINK, stroke_width=4)
    c_lbl = tex("C", size=40, color=PINK).next_to(p1, RIGHT, buff=0.25).shift(DOWN * _GAP)
    wires = VGroup(
        Line([_L, _CY + 0.42, 0], [_L, _TOP, 0], **w), Line([_L, _TOP, 0], [_Z0, _TOP, 0], **w),
        Line([_Z1, _TOP, 0], [_RX, _TOP, 0], **w), Line([_RX, _TOP, 0], [_RX, _CY + _GAP, 0], **w),
        Line([_RX, _CY - _GAP, 0], [_RX, _BOT, 0], **w), Line([_RX, _BOT, 0], [_L, _BOT, 0], **w),
        Line([_L, _BOT, 0], [_L, _CY - 0.42, 0], **w))
    mid = (_L + _RX) / 2
    i_arr = Arrow([mid + 0.5, _BOT, 0], [mid - 0.5, _BOT, 0], buff=0, color=GOLD,
                  stroke_width=4, tip_length=0.24, max_tip_length_to_length_ratio=0.4)
    i_lbl = tex("I", size=40, color=GOLD).next_to(i_arr, DOWN, buff=0.15)
    source = VGroup(src_c, sim)
    capacitor = VGroup(p1, p2)
    g = VGroup(wires, source, v_lbl, zig, r_lbl, capacitor, c_lbl, i_arr, i_lbl)
    g.scale(scale, about_point=ORIGIN).move_to(center)
    g.wires, g.source, g.resistor, g.capacitor, g.current = wires, source, zig, capacitor, i_arr
    g.V, g.R, g.C, g.I = v_lbl, r_lbl, c_lbl, i_lbl
    return g


def question_eq(pos=EQ_POS):
    q = tex("V", "=", "?", r"\cdot", "I", size=64).move_to(pos)
    q[4].set_color(GOLD)
    q[0:2].shift(LEFT * 0.2)
    q[3:].shift(RIGHT * 0.12)
    return q


def question_box(q):
    return SurroundingRectangle(q[2], color=YELLOW, buff=0.14, stroke_width=3)


def complex_tag(box):
    return T("complex", 30, PINK).next_to(box, DOWN, buff=0.22)


def handover_shot():
    circ = circuit()
    q = question_eq()
    box = question_box(q)
    return VGroup(circ, q, box, complex_tag(box))


# ---------------------------------------------------------------- drifting charges
# base points on free stretches of wire (raw coords) and the clockwise direction there
_CHARGES = [((-4.6, _TOP), RIGHT), ((-3.8, _TOP), RIGHT), ((-0.85, _TOP), RIGHT),
            ((-0.15, _TOP), RIGHT), ((_RX, -0.45), DOWN), ((_RX, -2.15), DOWN),
            ((-0.35, _BOT), LEFT), ((-1.1, _BOT), LEFT), ((-3.5, _BOT), LEFT),
            ((-4.35, _BOT), LEFT), ((_L, -2.25), UP), ((_L, -0.4), UP)]


def charge_dots(circ, amp=0.2, period=2.6):
    """DIM dots that slosh back and forth along the circuit's wires, following circ if it moves."""
    ref0, ref1 = np.array([_L, _TOP, 0.0]), np.array([_Z0, _TOP, 0.0])
    dots = VGroup(*[Dot(radius=0.055, color=DIM) for _ in _CHARGES])
    clock = {"t": 0.0}

    def upd(g, dt):
        clock["t"] += dt
        a, b = circ.wires[1].get_start(), circ.wires[1].get_end()
        s = np.linalg.norm(b - a) / np.linalg.norm(ref1 - ref0)
        off = amp * np.sin(TAU * clock["t"] / period)
        for d, ((x, y), dirn) in zip(g, _CHARGES):
            raw = np.array([x, y, 0.0]) + off * dirn
            d.move_to(a + s * (raw - ref0))
            d.set(width=0.11 * s)
        return g

    dots.add_updater(upd)
    upd(dots, 0)
    return dots


# ---------------------------------------------------------------- ch6 s4's pair (copied look)
def last_pair(center=np.array([0.0, 0.75, 0.0])):
    c = np.array(center, dtype=float)
    h_ax = Line(c + LEFT * 2.3, c + RIGHT * 2.3, color=DIM, stroke_width=2)
    v_ax = Line(c + DOWN * 1.6, c + UP * 2.4, color=DIM, stroke_width=2)
    ph = PI / 6
    u1 = np.array([np.cos(ph), np.sin(ph), 0.0])
    u2 = np.array([np.cos(ph + PI / 2), np.sin(ph + PI / 2), 0.0])
    gold = Arrow(c, c + 1.9 * u1, buff=0, stroke_width=6, color=GOLD, tip_length=0.26,
                 max_tip_length_to_length_ratio=0.3).set_z_index(2)
    purple = Arrow(c, c + 2.5 * u2, buff=0, stroke_width=6, color=PURPLE, tip_length=0.26,
                   max_tip_length_to_length_ratio=0.3).set_z_index(2)
    el = 0.32
    elbow = VMobject().set_points_as_corners([c + el * u1, c + el * (u1 + u2), c + el * u2])
    elbow.set_stroke(FG, 2.5)
    g_lbl = tex(r"A\,e^{i\omega t}", size=40, color=GOLD).next_to(gold.get_end(), RIGHT, buff=0.15)
    p_lbl = tex(r"i\omega A\,e^{i\omega t}", size=40, color=PURPLE)
    p_lbl.next_to(purple.get_end(), LEFT, buff=0.12)
    set_backstroke(g_lbl, width=5)
    set_backstroke(p_lbl, width=5)
    rule = tex(r"\dfrac{d}{dt}", r"\;\longrightarrow\;", r"\times", "i", r"\omega", size=54)
    rule[3].set_color(PINK)
    rule.move_to([0, -2.45, 0])
    return VGroup(h_ax, v_ax), gold, g_lbl, purple, elbow, p_lbl, rule


class Hook(NarratedScene):
    def construct(self):
        # ============================================================ clip 1
        with self.say("c7.hook.1") as c:
            card = title_card("Part 7 · Impedance")
            card.title.scale_to_fit_width(12.4)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      run_time=1.0)
            self.play(*appear(card.course), run_time=0.7)  # early: title card
            self.play(*appear(card.part), run_time=0.7)  # early: title card

            c.wait_until("last")
            axes, gold, g_lbl, purple, elbow, p_lbl, rule = last_pair()
            self.play(*during([FadeOut(m) for m in (card.title, card.rule, card.course, card.part)],
                              0, 0.45),
                      *during([Create(axes)], 0.4, 0.8),
                      *during([GrowArrow(gold)], 0.5, 1.0), run_time=1.8)
            self.play(*appear(g_lbl, shift=None), run_time=0.8)
            c.wait_until("complex form")
            self.play(GrowArrow(purple), Create(elbow), run_time=1.2)
            self.play(*appear(p_lbl, shift=None), run_time=0.8)

            c.wait_until("multiply")
            self.play(*appear(rule), run_time=1.2)

            c.wait_until("today")
            last = [axes, gold, g_lbl, purple, elbow, p_lbl, rule]
            self.play(*set_alpha(last, DIMMED), run_time=min(1.2, c.until()))

        # ============================================================ clip 2
        with self.say("c7.hook.2") as c:
            header = T("Example 32: Impedance of AC circuit", 44).move_to([0, 3.3, 0])
            self.play(*during(disappear(*last), 0, 0.45),
                      *during(appear(header), 0.5, 1.0), run_time=1.6)  # early: header read as "Example thirty-two"

            c.wait_until("circuit")
            circ = circuit(center=[0, 0.5, 0], scale=CIRC_SCALE)
            self.play(LaggedStart(*[Create(wl) for wl in circ.wires], lag_ratio=0.1),
                      Create(circ.source[0]), run_time=1.6)
            self.play(*appear(circ.source[1], circ.V, shift=None), Create(circ.resistor),
                      *during(appear(circ.R), 0.4, 1.0), run_time=1.1)
            self.play(GrowFromCenter(circ.capacitor[0]), GrowFromCenter(circ.capacitor[1]),
                      *during(appear(circ.C), 0.4, 1.0), run_time=1.0)
            self.play(GrowArrow(circ.current), *during(appear(circ.I), 0.4, 1.0), run_time=1.0)
            self.remove(*circ.get_family())
            self.add(circ)
            dots = charge_dots(circ)
            self.play(FadeIn(dots), run_time=0.8)

            c.wait_until("find")
            task = T("Find the complex resistance of a capacitor and resistor\n"
                     "connected in series to an applied alternating voltage.", 32,
                     line_spacing=1.0).move_to([0, -2.95, 0])
            self.play(*appear(task), run_time=1.2)

        # ============================================================ clip 3
        with self.say("c7.hook.3") as c:
            self.play(circ.animate.scale(0.75 / CIRC_SCALE).move_to([-3.85, 0.6, 0]), run_time=1.5)

            quote = T("“I'm one of the computer scientists\n"
                      "who also does this. Is it okay that\n"
                      "I didn't understand any of that\n"
                      "physics stuff?”", 28, slant=ITALIC, line_spacing=1.0)
            who = T("a student, end of lecture", 28, DIM)
            body = VGroup(quote, who).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            frame = RoundedRectangle(corner_radius=0.2, width=body.width + 0.6,
                                     height=body.height + 0.5, stroke_color=DIM, stroke_width=2)
            frame.move_to([3.0, 1.35, 0])
            body.move_to(frame)
            c.wait_until(own_word=quote)
            self.play(FadeIn(frame), *appear(quote, shift=None), run_time=1.2)
            self.play(*appear(who, shift=None), run_time=0.8)

            c.wait_until("answer")
            ans = T("“Yes, yes, yes,\nthat's absolutely fine.”", 30, line_spacing=1.0)
            tick = check_mark(GREEN)
            reply = VGroup(tick, ans).arrange(RIGHT, buff=0.3)
            reply.move_to([3.0, -0.95, 0])
            self.play(*appear(ans), run_time=1.0)
            self.play(Create(tick), run_time=0.6)

            c.wait_until("plan")
            corner = np.array([6.2, 3.4, 0])
            cardg = VGroup(frame, body, reply)
            self.play(*during([cardg.animate.scale(0.25).move_to(corner).set_opacity(0)], 0, 0.6),
                      *during(disappear(header, task), 0, 0.5),
                      *during([circ.animate.scale(CIRC_SCALE / 0.75).move_to(CIRC_POS)], 0.3, 1.0),
                      run_time=2.0)
            self.remove(*cardg.get_family())

        # ============================================================ clip 4
        with self.say("c7.hook.4") as c:
            others = [circ.wires, circ.source, circ.V, circ.capacitor, circ.C, circ.current, circ.I]
            ohm = tex("V", "=", "R", "I", size=64).move_to(EQ_POS)
            ohm[2].set_color(BLUE)
            ohm[3].set_color(GOLD)
            self.play(*set_alpha(others, DIMMED), FadeOut(dots),
                      *during(appear(ohm), 0.3, 1.0), run_time=1.4)
            dots.clear_updaters()
            self.remove(dots)

            c.wait_until("question")
            q = question_eq()
            self.play(*set_alpha(others, 1.0), run_time=1.0)
            self.play(*edit(ohm, q), run_time=1.5)
            box = question_box(q)
            self.play(FadeIn(box), run_time=0.7)

            c.wait_until("complex")
            tag = complex_tag(box)
            self.play(*appear(tag), run_time=1.0)
        self.wait(1.0)
