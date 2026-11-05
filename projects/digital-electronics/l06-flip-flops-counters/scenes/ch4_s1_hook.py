"""Chapter 4, scene 1: hook: a digital watch counts its crystal's vibrations. Clips c4.hook.1 – c4.hook.2.

Title card; {last}: ch3's J-K, T and D (RED PRE/CLR) symbols, shrinking away on {work}. Hero: a
digital watch (module-level digital_watch(), copied by s2 and s6) reading 12:00:00, seconds GOLD;
a quartz crystal streams a fast YELLOW square wave; the seconds tick twice; a "?" box ("something
counts") sits between wave and display; three BLUE outlines fill it; the two questions appear
under the watch; on {plan} the outlines become ch3_s7's ripple chain of T flip-flops (bubble
clocks), with a RED "avoid" tag.
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


# ---- ch3's flip-flop symbol (ch3_s7_recap.make_ff + ch3_s6_async's scale / lab_k) ---------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
CLR_DX = 0.55


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False, scale=1.0, lab_k=1.0):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    top_clk = -hb - (0.22 if bubble else 0.02)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, top_clk)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    parts = [*in_w, q_w, qb_w, clk_w, box, tri]
    if bubble:   # hollow: BG fill, stroke thinned with the scale
        bub = Circle(radius=0.1).set_stroke(FG, max(2, 3 * scale)).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, clk_w, q_w, qb_w, in_w
    g.labels = [*in_l, q_l, qb_l]
    g.scale(scale, about_point=ORIGIN)
    for lab in g.labels:
        lab.scale(lab_k, about_point=lab.get_center())
    g.shift(_p(*center[:2]))
    return g


def pin(ff, kind, size=30, length=None):
    """ch3_s6_async.pin: a RED async pin, PRE on top (centre), CLR underneath (right of the clock)."""
    s = ff.box.width / BOX_W
    c, hb = ff.box.get_center(), ff.box.height / 2
    L = (length if length is not None else EN_WIRE) * s
    if kind == "PRE":
        a = c + hb * UP
        b = a + L * UP
        w = Line(a, b).set_stroke(RED, 5)
        lab = T("PRE", size, RED).next_to(b, UP, buff=0.12)
    else:
        a = c + CLR_DX * s * RIGHT + hb * DOWN
        b = a + L * DOWN
        w = Line(a, b).set_stroke(RED, 5)
        lab = T("CLR", size, RED).next_to(b, DOWN, buff=0.12)
    return w, lab


def last_row():
    """{last}: J-K, T, and D with RED PRE / CLR, in a row at 0.9."""
    s = 0.9
    k = 30 / (36 * s)
    jk = make_ff((-4.3, 0), ins=(("J", PIN_Y), ("K", -PIN_Y)), scale=s, lab_k=k)
    tf = make_ff((0, 0), ins=(("T", PIN_Y),), scale=s, lab_k=k)
    d = make_ff((4.3, 0), scale=s, lab_k=k)
    pw, pl = pin(d, "PRE", 30)
    cw, cl = pin(d, "CLR", 30)
    d.add(pw, pl, cw, cl)
    return VGroup(jk, tf, d)


# ---- ch3_s7_recap.ripple_chain: three T flip-flops (bubble clocks), each Q clocks the next ------
CH_X = (-4.3, 0.0, 4.3)
LED_Y = 2.3
CH_K = 0.78
CH_C = _p(0, 0.5)


def led(on=False):
    return Circle(radius=0.21).set_stroke(GREEN, 3).set_fill(GREEN, 0.9 if on else 0.0)


def ripple_chain():
    hb = BOX_H / 2
    ffs = [make_ff(_p(x, 0), ins=(("T", PIN_Y),), bubble=True) for x in CH_X]
    ones = [MathTex("1", font_size=44, color=BLUE).next_to(f.in_w[0].get_start(), LEFT, buff=0.12)
            for f in ffs]
    wires, dots, leds = [], [], []
    for k, x in enumerate(CH_X):
        jx = x + BOX_W / 2 + WIRE + 0.4
        w = [_p(x + BOX_W / 2 + WIRE, PIN_Y), _p(jx, PIN_Y), _p(jx, LED_Y - 0.21)]
        wires.append(VMobject().set_points_as_corners(w).set_stroke(GREEN, 5))
        leds.append(led().move_to(_p(jx, LED_Y)))
        if k < 2:
            ffs[k + 1].clk_w.set_stroke(GREEN)
            down = [_p(jx, PIN_Y), _p(jx, -hb - EN_WIRE), _p(CH_X[k + 1], -hb - EN_WIRE)]
            wires.append(VMobject().set_points_as_corners(down).set_stroke(GREEN, 5))
            dots.append(Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN))
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    g = VGroup(*ffs, *ones, *wires, *dots, *leds, clk_l)
    g.scale(CH_K, about_point=ORIGIN).move_to(CH_C)
    g.ffs, g.ones, g.wires, g.dots, g.leds, g.clk_l = ffs, ones, wires, dots, leds, clk_l
    return g


def count_leds(leds, values):
    n = len(values)

    def f_for(bit):
        def f(m, a):
            v = values[min(int(a * n), n - 1)]
            m.set_fill(GREEN, 0.9 if (v >> bit) & 1 else 0.0)
        return f
    return [UpdateFromAlphaFunc(l, f_for(b)) for b, l in enumerate(leds)]


# ---- the digital watch (s2 and s6 copy this) ----------------------------------------------------
WATCH_C = _p(0, 0.85)          # body centre
WATCH_W, WATCH_H = 8.6, 4.6     # body
CASE = "#1B1F26"                # body / strap fill
LCD = "#0A0C10"                 # display window fill
DIGITS = 72                     # Mono size of 12:00:00


def digital_watch(secs="00"):
    """Body 8.6 x 4.6 (DIM stroke 4, fill #1B1F26) centred at (0, 0.85), straps 0.45 above and
    below; display window 6.4 x 1.4 (DIM stroke 3, fill #0A0C10) at (0, 2.1); Mono 72 "12:00:"
    FG + seconds GOLD. Returns VGroup(straps, body, window, lead, secs); .secs_text(s) builds a
    new seconds text in place (for swap)."""
    body = RoundedRectangle(corner_radius=0.6, width=WATCH_W, height=WATCH_H)
    body.set_stroke(DIM, 4).set_fill(CASE, 1).move_to(WATCH_C)
    top, bot = body.get_top()[1], body.get_bottom()[1]
    straps = VGroup(
        Polygon(_p(-2.3, top), _p(2.3, top), _p(2.0, top + 0.45), _p(-2.0, top + 0.45)),
        Polygon(_p(-2.3, bot), _p(2.3, bot), _p(2.0, bot - 0.45), _p(-2.0, bot - 0.45)),
    ).set_stroke(DIM, 4).set_fill(CASE, 1)
    window = RoundedRectangle(corner_radius=0.15, width=6.4, height=1.4)
    window.set_stroke(DIM, 3).set_fill(LCD, 1).move_to(WATCH_C + _p(0, 1.25))
    ref = Mono("12:00:00", DIGITS).move_to(window)

    def secs_text(s):
        full = Mono("12:00:" + s, DIGITS).move_to(ref).align_to(ref, LEFT)
        t = Mono(s, DIGITS, GOLD)
        t.align_to(full, RIGHT).align_to(full, DOWN)
        return t

    lead = Mono("12:00:", DIGITS).align_to(ref, LEFT).align_to(ref, DOWN)
    sec = secs_text(secs)
    g = VGroup(straps, body, window, lead, sec)
    g.straps, g.body, g.window, g.lead, g.secs = straps, body, window, lead, sec
    g.secs_text = secs_text
    return g


def quartz(center):
    """A small quartz can: rounded capsule with two leads (FG / DIM)."""
    can = RoundedRectangle(corner_radius=0.22, width=1.0, height=0.5).set_stroke(FG, 3).set_fill(PURPLE, 0.35)
    can.move_to(center)
    legs = VGroup(*[Line(can.get_left() + _p(0, dy), can.get_left() + _p(-0.25, dy)).set_stroke(DIM, 3)
                    for dy in (0.1, -0.1)])
    return VGroup(legs, can)


def square_points(x0, x1, y, amp, period, phase):
    """Corner points of a square wave from x0 to x1, shifted right by phase."""
    half = period / 2
    k = np.floor((x0 - phase) / half)
    edge = phase + k * half
    pts = []
    high = int(k) % 2 == 0
    x = x0
    while x < x1:
        nxt = min(edge + half, x1)
        yy = y + (amp if high else -amp)
        pts += [_p(x, yy), _p(nxt, yy)]
        x = nxt
        edge += half
        high = not high
    return pts


class Hook(NarratedScene):
    def construct(self):
        card = title_card("Part 4 · Counters, and the ripple counter")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(FadeIn(card.course), run_time=0.6)  # early: title card
        self.play(FadeIn(card.part), run_time=0.6)  # early: title card
        self.wait(4.5)
        self.card = card
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c4.hook.1
    def clip1(self):
        with self.say("c4.hook.1") as c:
            # {last}: the card goes, ch3's three symbols appear
            row = last_row()
            c.wait_until("last")
            self.play(*during([FadeOut(self.card)], 0, 0.45),
                      *during(appear(*row, shift=None, lag=0.3), 0.45, 1.0), run_time=2.0)  # early: last time's symbols, shown whole
            c.wait_until("work")

            # {work}: they shrink away; the watch appears
            self.play(FadeOut(row, scale=0.3), run_time=1.0)
            w = self.watch = digital_watch()
            self.play(*appear(w, shift=None), run_time=min(1.2, c.until("crystal")))
            c.wait_until("crystal")

            # {crystal}: a quartz crystal inside; a fast YELLOW wave streams out of it
            qz = quartz(_p(-3.15, WATCH_C[1] - 0.8))
            qlab = T("quartz", 28, DIM).next_to(qz, DOWN, buff=0.18)
            self.play(*appear(qz, shift=None), run_time=0.8)
            x0 = qz.get_right()[0] + 0.12
            self.box_c = _p(2.5, qz.get_center()[1])
            x_end = self.box_c[0] - 1.1 - 0.12
            y = qz.get_center()[1]
            head = ValueTracker(x0 + 0.01)
            wave = VMobject().set_stroke(YELLOW, 4)
            wave.phase = 0.0

            def upd(m, dt):
                m.phase += dt * 1.6
                m.set_points_as_corners(square_points(x0, head.get_value(), y, 0.26, 0.2, m.phase))
            upd(wave, 0)
            wave.add_updater(upd)
            self.add(wave)
            self.play(head.animate.set_value(x_end), *appear(qlab, shift=None), run_time=1.5, rate_func=linear)
            wlab = T("tens of thousands per second", 30, GOLD).move_to(_p((x0 + x_end) / 2 - 0.35, y + 0.85))
            c.wait_until(own_word=wlab)
            self.play(*appear(wlab), run_time=1.0)
            c.wait_until("tick")

            # {tick}: the seconds tick twice, a GREEN pulse each time
            for s in ("01", "02"):
                new = w.secs_text(s)
                self.play(*swap(w.secs, new, shift=0.15 * UP),
                          run_time=0.7)
                w.remove(w.secs)
                w.secs = new
                w.add(new)
                self.play(new.animate(rate_func=there_and_back).set_color(GREEN), run_time=0.5)   # GREEN pulse
            c.wait_until("count")

            # {count}: a GOLD "?" box between the wave and the display
            box = Rectangle(width=2.2, height=1.2).set_stroke(FG, 3).set_fill(BG, 1).move_to(self.box_c)
            q = T("?", 56, GOLD).move_to(box)
            arr = Arrow(box.get_top() + _p(-0.3, 0), _p(box.get_top()[0] - 0.3, w.window.get_bottom()[1]),
                        buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.35).set_color(FG)
            self.play(GrowFromCenter(box), *during(appear(q, shift=None), 0.4, 1.0), run_time=1.2)
            self.play(GrowArrow(arr), run_time=0.8)
            clab = T("something counts", 30, FG).next_to(box, DOWN, buff=0.2)
            c.wait_until("counting")
            self.play(*appear(clab), run_time=1.0)
            self.qz, self.qlab, self.wave, self.wlab = qz, qlab, wave, wlab
            self.box, self.q, self.arr, self.clab = box, q, arr, clab

    # ------------------------------------------------------------------ c4.hook.2
    def clip2(self):
        with self.say("c4.hook.2", gap=3.2) as c:
            # {question}: three BLUE outlines fill the box; the question under the watch
            outl = VGroup(*[Rectangle(width=0.5, height=0.85).set_stroke(BLUE, 4) for _ in range(3)])
            outl.arrange(RIGHT, buff=0.22).move_to(self.box)
            c.wait_until("question")
            self.play(*swap(self.q, outl), run_time=1.0)
            q1 = T("How do you build a counter from flip-flops?", 38).move_to(_p(0, -2.5))
            q2 = T("What can go wrong?", 38, RED).move_to(_p(0, -3.3))
            c.wait_until(own_word=q1)
            self.play(*appear(q1), run_time=1.0)
            c.wait_until(own_word=q2)
            self.play(*appear(q2), run_time=1.0)
            c.wait_until("plan")

            # {plan}: the watch goes; the outlines become the ripple chain's T boxes
            ch = ripple_chain()
            ghosts = [ch.ffs[i].box.copy() for i in range(3)]
            self.wave.clear_updaters()
            old = [self.watch, self.qz, self.qlab, self.wave, self.wlab, self.box, self.arr, self.clab]
            self.play(*during([FadeOut(m) for m in old], 0, 0.45),
                      *during([ReplacementTransform(o, g) for o, g in zip(outl, ghosts)], 0.2, 1.0),
                      run_time=min(1.8, c.until("ripple counter")))
            self.play(*appear(ch, shift=None), run_time=1.2)
            self.remove(*ghosts)
            c.wait_until("watch it count")
            # the chain counts 1..7, 0 (about 0.4 s a state, ending with the clip); the RED "avoid" tag lands on its word mid-count
            tag_t = T("avoid", 34, RED)
            tag = VGroup(SurroundingRectangle(tag_t, color=RED, buff=0.14, corner_radius=0.1).set_stroke(RED, 3),
                         tag_t).move_to(_p(0, 3.35))
            rt = min(3.6, c.until(floor=2.8))
            f = min(0.75, c.until("avoid", floor=0.0) / rt)
            self.play(*count_leds(ch.leds, [1, 2, 3, 4, 5, 6, 7, 0]),
                      *during(appear(tag), f, f + 0.25), run_time=rt, rate_func=linear)
