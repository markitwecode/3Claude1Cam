"""Chapter 6, scene 1: hook. From the FPGA down to gates and transistors, the turn to electronics,
the road ahead, and the chapter's question: what moves in a wire? Clips c6.hook.1 – c6.hook.3.

open_card(): the shot ch5_s8 ends on and this scene opens on (s2's Loop with a lit lamp in its slot,
electrons parked, under the Part 6 line). Ends on ch6_s2_electrons.opening_shot() (handover).
No ch5_s2_array.py exists, so the 4x4 FPGA array is drawn here (TEAL CLBs, PURPLE switch
matrices, DIM IOBs).
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

S2 = load_scene("ch6_s2_electrons")

PART6 = "Part 6 · Electricity, from charge to Kirchhoff"


def part6_line():
    return T(PART6, 40).move_to([0, 3.2, 0])


def open_card():
    """ch5_s8's last frame and this scene's first: s2's Loop with a lit lamp in its slot, the
    electrons parked on their home slots, under the Part 6 line. .loop .els .lamp .part"""
    loop = S2.Loop()
    loop.wire.remove(loop.slot_fill)
    els = S2.LoopElectrons(loop)
    lmp = loop.place(S2.lamp(lit=True))
    part = part6_line()
    g = VGroup(loop, els, lmp, part)
    g.loop, g.els, g.lamp, g.part = loop, els, lmp, part
    return g


def handover_shot():
    return S2.opening_shot()


# ---------------------------------------------------------------------------------------------
# FPGA array (4x4), gates, transistors
# ---------------------------------------------------------------------------------------------
PITCH, CLB_S, ARR_SCALE = 1.4, 0.8, 0.85
PICK = (2, 2)   # the CLB the camera dives into


def fpga():
    """Returns (rest, chosen): everything but the chosen CLB, and the chosen CLB, scaled and
    centred on ORIGIN together."""
    chans = [(k - 2) * PITCH for k in range(5)]
    route = VGroup(*[Line([-2.8, y, 0], [2.8, y, 0]) for y in chans],
                   *[Line([x, -2.8, 0], [x, 2.8, 0]) for x in chans]).set_stroke(DIM, 2, opacity=0.6)
    sms = VGroup(*[Square(0.34).move_to([x, y, 0]) for x in chans for y in chans]) \
        .set_stroke(PURPLE, 3).set_fill(BG, 1)
    clbs, chosen = VGroup(), None
    for i in range(4):
        for j in range(4):
            sq = Square(CLB_S).move_to([(i - 1.5) * PITCH, (j - 1.5) * PITCH, 0]) \
                .set_stroke(TEAL, 4).set_fill(BG, 1)
            if (i, j) == PICK:
                chosen = sq
            else:
                clbs.add(sq)
    iobs = VGroup()
    for k in range(4):
        c = (k - 1.5) * PITCH
        for p, horiz in (([c, 3.5, 0], True), ([c, -3.5, 0], True), ([3.5, c, 0], False), ([-3.5, c, 0], False)):
            r = Rectangle(width=0.55 if horiz else 0.32, height=0.32 if horiz else 0.55).move_to(p)
            iobs.add(r)
    iobs.set_stroke(DIM, 3).set_fill(BG, 1)
    rest = VGroup(route, sms, clbs, iobs)
    VGroup(rest, chosen).scale(ARR_SCALE)
    return rest, chosen


def and_gate(w=1.4, h=1.1):
    r = h / 2
    body = VMobject()
    body.set_points_as_corners([[w / 2 - r, -r, 0], [-w / 2, -r, 0], [-w / 2, r, 0], [w / 2 - r, r, 0]])
    arc = Arc(radius=r, start_angle=PI / 2, angle=-PI, arc_center=[w / 2 - r, 0, 0])
    g = VGroup(body, arc).set_stroke(FG, 4)
    g.out = np.array([w / 2, 0, 0])
    g.ins = [np.array([-w / 2, 0.25 * h, 0]), np.array([-w / 2, -0.25 * h, 0])]
    return g


def or_gate(w=1.4, h=1.1):
    tl, bl, tip = np.array([-w / 2, h / 2, 0]), np.array([-w / 2, -h / 2, 0]), np.array([w / 2, 0, 0])
    back = ArcBetweenPoints(tl, bl, angle=-0.9)
    top = ArcBetweenPoints(tl, tip, angle=-0.55)
    bot = ArcBetweenPoints(bl, tip, angle=0.55)
    g = VGroup(back, top, bot).set_stroke(FG, 4)
    g.out = tip
    xin = -w / 2 + 0.12
    g.ins = [np.array([xin, 0.25 * h, 0]), np.array([xin, -0.25 * h, 0])]
    return g


def _at(g, p):
    """Move gate g to p, keeping its .out/.ins pin points in step."""
    d = np.array(p) - g.get_center()
    g.shift(d)
    g.out = g.out + d
    g.ins = [q + d for q in g.ins]
    return g


def wire(*pts):
    return VMobject().set_points_as_corners([np.array(p) for p in pts]).set_stroke(FG, 3)


def transistor(s=0.32):
    ch = Line([0, -s / 2, 0], [0, s / 2, 0])
    gb = Line([-0.08, -s / 2.6, 0], [-0.08, s / 2.6, 0])
    gl = Line([-0.08, 0, 0], [-0.22, 0, 0])
    d = VMobject().set_points_as_corners([[0, s / 2 - 0.04, 0], [0.13, s / 2 - 0.04, 0], [0.13, s / 2 + 0.06, 0]])
    so = VMobject().set_points_as_corners([[0, -s / 2 + 0.04, 0], [0.13, -s / 2 + 0.04, 0], [0.13, -s / 2 - 0.06, 0]])
    return VGroup(ch, gb, gl, d, so).set_stroke(DIM, 3)


WIRE_Y = 0.5     # the output wire / s2's tube centre
ZOOM, ZP_X = 4.0, 1.0


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.7)   # handover: end on s2's opening shot, unfaded

    # -- c6.hook.1: title, FPGA, gates, transistors, the turn --------------------------------------
    def clip1(self):
        oc = open_card()
        self.add(oc.loop, oc.els, oc.lamp, oc.part)
        self.wait(0.7)
        with self.say("c6.hook.1") as c:
            card = title_card(PART6)
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            part = oc.part
            self.play(*during([FadeOut(oc.loop), FadeOut(oc.els), FadeOut(oc.lamp)], 0, 0.35),  # early: title card
                      *during([part.animate.scale(36 / 40).move_to(card.part)], 0.25, 0.75),
                      *during([FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule)], 0.7, 1.0),  # early: title card
                      run_time=1.6)
            self.remove(part)
            self.add(card.part)
            self.play(*appear(card.course), run_time=0.9)  # early: title card read whole

            # {last}: the FPGA array
            c.wait_until("last")
            rest, chosen = fpga()
            sweep_clear(self, time_span(FadeIn(rest), 0.6, 1.4), time_span(FadeIn(chosen), 0.6, 1.4),
                        run_time=1.4)
            c.wait_until("logic blocks")
            self.play(FlashAround(chosen, color=YELLOW, time_width=1.5, buff=0.08), run_time=1.5)

            # {gates}: dive into one CLB; gates inside
            c.wait_until("gates")
            big = Rectangle(width=8.4, height=4.8).set_stroke(TEAL, 4).set_fill(BG, 0).move_to([0, -0.1, 0])
            a1 = _at(and_gate(), [-1.7, 0.95, 0])
            a2 = _at(and_gate(), [-1.7, -1.15, 0])
            og = _at(or_gate(1.8, 1.4), [1.4, -0.1, 0])
            L, R = big.get_left()[0], big.get_right()[0]
            ins = VGroup(*[wire([L, p[1], 0], p) for g in (a1, a2) for p in g.ins])
            mid = VGroup(wire(a1.out, [0.0, a1.out[1], 0], [0.0, og.ins[0][1], 0], og.ins[0]),
                         wire(a2.out, [0.0, a2.out[1], 0], [0.0, og.ins[1][1], 0], og.ins[1]))
            outw = wire(og.out, [R, og.out[1], 0])
            c_pt = chosen.get_center()
            self.play(*during([rest.animate.scale(5, about_point=c_pt).set_opacity(0)], 0, 0.7),
                      *during([Transform(chosen, big)], 0, 0.7),
                      *during([FadeIn(VGroup(a1, a2, og)), FadeIn(VGroup(ins, mid, outw))], 0.55, 1.0),
                      run_time=min(2.0, c.until("transistors")))
            self.remove(rest)
            c.wait_until("transistors")

            # {transistors}: one gate goes translucent, transistors inside
            # sized and placed to sit wholly inside the gate body (clear of the curved top/bottom)
            trs = VGroup(*[transistor().scale(0.8).move_to(og.get_center() + np.array([dx, dy, 0]))
                           for dx in (-0.38, 0.0) for dy in (0.19, -0.19)])
            self.play(*set_alpha([a1, a2, ins, mid, outw, chosen], DIMMED),
                      og.animate.set_stroke(opacity=0.35), FadeIn(trs),
                      run_time=min(1.5, c.until("turn")))
            c.wait_until("turn")

            # {turn}: everything slides away, the section title arrives
            sec = T("Electronics, Devices and Circuits", 52).move_to([0, 0.45, 0])
            sub = T("Underlying Concepts", 36, DIM).next_to(sec, DOWN, buff=0.4)
            board = [chosen, a1, a2, og, ins, mid, outw, trs]
            self.play(*during([m.animate.shift(15 * LEFT) for m in board], 0, 0.6),  # early: section title (p. 163)
                      *during(appear(sec, sub, lag=0.3), 0.5, 1.0),
                      run_time=2.2)
            self.remove(*board)
            self.sec, self.sub = sec, sub

    # -- c6.hook.2: the road ahead -------------------------------------------------------------------
    def clip2(self):
        sec, sub = self.sec, self.sub
        with self.say("c6.hook.2") as c:
            y = 0.3
            s1 = Circle(radius=0.28).set_stroke(FG, 4).set_fill(BG, 1).move_to([-3.6, y, 0])
            s2 = Circle(radius=0.28).set_stroke(FG, 4).set_fill(BG, 1).move_to([3.6, y, 0])
            road = Arrow(s1.get_right(), s2.get_left(), buff=0.15, stroke_width=4, color=FG,
                         max_tip_length_to_length_ratio=0.06)
            self.play(sec.animate.scale(0.85).move_to([0, 3.15, 0]),
                      sub.animate.move_to([0, 2.45, 0]), run_time=1.2)
            self.play(GrowFromCenter(s1), GrowArrow(road), GrowFromCenter(s2), run_time=1.0)

            c.wait_until("concepts")
            lab1 = T("Underlying concepts", 36).move_to([-3.6, y - 0.75, 0])
            self.play(*appear(lab1), run_time=0.9)
            tags = [T(t, 30, DIM) for t in ("electrical circuits", "circuit theory", "materials")]
            for k, tg in enumerate(tags):
                tg.move_to([-3.6, y - 1.5 - 0.55 * k, 0])
            for tg in tags:
                c.wait_until(own_word=tg)
                self.play(*appear(tg), run_time=0.7)

            c.wait_until("gatesnext")
            lab2 = T("Transistors → gates", 36).move_to([3.6, y - 0.75, 0])
            self.play(*appear(lab2), run_time=1.0)

            c.wait_until("today")
            mk = marker(YELLOW).move_to(above(s1, buff=0.2))
            here = T("you are here", 30, YELLOW).move_to([-3.6, 2.15, 0])
            self.play(*during(disappear(sub), 0, 0.4),
                      *during([FadeIn(mk, shift=0.3 * DOWN)], 0.4, 1.0),
                      *during(appear(here), 0.4, 1.0), run_time=1.3)
            chain = T("charge → … → Kirchhoff", 30).move_to([-3.6, 1.6, 0])
            c.wait_until(own_word=chain)
            self.play(*appear(chain), run_time=1.0)

    # -- c6.hook.3: one gate's output wire, and the question ---------------------------------------
    def clip3(self):
        with self.say("c6.hook.3") as c:
            gate = _at(or_gate(), [0, 0, 0])
            gate.scale(1.6)
            gate.out = gate.out * 1.6
            gate.ins = [q * 1.6 for q in gate.ins]
            _at(gate, [-2.6, WIRE_Y, 0])
            gap = 2 * S2.TUBE_R / ZOOM
            xg = gate.out[0]
            wtube = VGroup(Line([xg, WIRE_Y + gap / 2, 0], [7.05, WIRE_Y + gap / 2, 0]),
                           Line([xg, WIRE_Y - gap / 2, 0], [7.05, WIRE_Y - gap / 2, 0])).set_stroke(FG, 5)
            gins = VGroup(*[wire([-6.3, p[1], 0], p) for p in gate.ins]).set_stroke(width=4)
            v0 = T("0", 44).move_to([-0.4, WIRE_Y + 0.6, 0])
            sweep_clear(self, time_span(FadeIn(gate), 0.6, 1.3), time_span(FadeIn(gins), 0.6, 1.3),
                        time_span(FadeIn(wtube), 0.6, 1.3), time_span(FadeIn(v0), 0.7, 1.3), run_time=1.3)

            c.wait_until("question")
            v1 = T("1", 44, GREEN).move_to(v0)
            self.play(*swap(v0, v1), run_time=1.0)

            # {question}: zoom toward the wire
            c.wait_until("what is actually")
            zp = np.array([ZP_X, WIRE_Y, 0])
            self.play(*during(disappear(v1), 0, 0.3),
                      *during([m.animate.scale(ZOOM, about_point=zp) for m in (gate, gins, wtube)], 0.2, 1.0),
                      run_time=1.8)
            tube, q, how = S2.opening_shot()
            self.remove(gate, gins, wtube)
            self.add(tube)
            self.play(*appear(q, shift=None), run_time=1.0)

            c.wait_until("measure")
            self.play(*appear(how), run_time=1.0)
