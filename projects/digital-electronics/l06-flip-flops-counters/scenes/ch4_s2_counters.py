"""Chapter 4, scene 2: what a counter is; the 3-bit state ring; uses; ripple vs synchronous. Clips c4.def.1 – c4.def.4."""
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


# ---------------------------------------------------------------- shared helpers (copy these)
RING_R = 2.3        # ring radius (node centres)
NODE_R = 0.5        # node circle radius


def edge_tick(color=YELLOW, w=0.4, h=0.28, width=4):
    """A small rising clock edge: low, up, high."""
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [[-w / 2, -h / 2, 0], [0, -h / 2, 0], [0, h / 2, 0], [w / 2, h / 2, 0]])


def state_ring(n_bits=3, radius=RING_R):
    """The chapter's running counter: 2^n nodes clockwise from the top (000 at 12 o'clock).

    Built centred on ORIGIN. Node i: BLUE circle (r 0.5, stroke 4) holding its bits (Mono 28, GREEN);
    its GOLD decimal (T 34) sits 0.85 inward. arrows[i] goes i -> i+1 (FG, stroke 3); arrows[-1] is the
    wrap 111 -> 000. ring.hub is an invisible dot at the centre (moves with the ring);
    ring.out_point(i, d) is the point d beyond node i's centre, radially outward.
    """
    n = 2 ** n_bits
    hub = Dot(ORIGIN, radius=0.01).set_opacity(0)

    def dirn(i):
        a = PI / 2 - TAU * i / n
        return np.array([np.cos(a), np.sin(a), 0.0])

    nodes, circles, bits, decimals, arrows = [], [], [], [], []
    for i in range(n):
        p = radius * dirn(i)
        circ = Circle(radius=NODE_R, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        b = Mono(format(i, f"0{n_bits}b"), size=28, color=GREEN).move_to(p)
        circles.append(circ)
        bits.append(b)
        nodes.append(VGroup(circ, b))
        decimals.append(T(str(i), 34, color=GOLD).move_to(p - 0.85 * dirn(i)))
    for i in range(n):
        p, q = radius * dirn(i), radius * dirn((i + 1) % n)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + (NODE_R + 0.04) * u, q - (NODE_R + 0.04) * u, buff=0, color=FG,
                            stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4))
    ring = VGroup(VGroup(*arrows), VGroup(*nodes), VGroup(*decimals), hub)
    ring.nodes, ring.circles, ring.bits, ring.decimals, ring.arrows, ring.hub = (
        nodes, circles, bits, decimals, arrows, hub)
    ring.out_point = lambda i, d=0.68: ring.hub.get_center() + (radius + d) * dirn(i) * (
        ring.circles[0].width / (2 * NODE_R))
    return ring


def _p(x, y):
    return np.array([x, y, 0.0])


# digital_watch() copied from ch4_s1_hook.py (same geometry and colours)
WATCH_W, WATCH_H = 8.6, 4.6
WATCH_C = _p(0, 0.85)          # body centre
CASE = "#1B1F26"                # body / strap fill
LCD = "#0A0C10"                 # display window fill
DIGITS = 72                     # Mono size of 12:00:00


def digital_watch(secs="00"):
    """Body 8.6 x 4.6 (DIM stroke 4, fill #1B1F26) centred at (0, 0.85), straps 0.45 above and
    below; display window 6.4 x 1.4 (DIM stroke 3, fill #0A0C10) at (0, 2.1); Mono 72 "12:00:"
    FG + seconds GOLD."""
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
    full = Mono("12:00:" + secs, DIGITS).move_to(ref).align_to(ref, LEFT)
    sec = Mono(secs, DIGITS, GOLD).align_to(full, RIGHT).align_to(full, DOWN)
    lead = Mono("12:00:", DIGITS).align_to(ref, LEFT).align_to(ref, DOWN)
    g = VGroup(straps, body, window, lead, sec)
    g.straps, g.body, g.window, g.lead, g.secs = straps, body, window, lead, sec
    return g


# ---------------------------------------------------------------- the scene
class Counters(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------ definition, sketch, n-bit counter
    def clip1(self):
        with self.say("c4.def.1") as c:
            q = T("What is a counter?", 48).move_to(UP * 3.0)
            self.play(*appear(q), run_time=min(1.0, c.until("fsm")))
            c.wait_until("fsm")

            defn = T("A counter is a clocked sequential finite state machine\n"
                     "that goes through a predetermined sequence of states", 34,
                     t2c={"clocked": YELLOW, "predetermined sequence of states": BLUE},
                     line_spacing=1.1).move_to(UP * 3.0)
            self.play(*swap(q, defn), run_time=min(1.2, c.until("gloss")))
            self.defn = defn
            c.wait_until("gloss")

            # {gloss}: four states in a row, a clock tick on each arrow
            xs = [-3.3, -1.1, 1.1, 3.3]
            y = 0.7
            circles = [Circle(radius=0.42, color=BLUE, stroke_width=4).move_to([x, y, 0]) for x in xs]
            arrows = [Arrow(circles[i].get_right(), circles[i + 1].get_left(), buff=0.1, color=FG,
                            stroke_width=3, tip_length=0.2) for i in range(3)]
            ticks = [edge_tick().next_to(a, UP, buff=0.15) for a in arrows]
            self.play(*appear(*circles, lag=0.2, shift=None), run_time=min(1.4, c.until("each clock edge")))
            self.play(*[GrowArrow(a) for a in arrows], *appear(*ticks, lag=0.15, shift=None),
                      run_time=min(1.2, c.until("each clock edge")))
            dot = Dot(circles[0].get_center(), radius=0.14, color=YELLOW)
            self.play(FadeIn(dot, scale=0.5), run_time=0.6)
            c.wait_until("each clock edge")
            for i in range(3):
                rt = [1.1, 0.9, 0.9][i]
                self.play(dot.animate(path_arc=-PI / 2).move_to(circles[i + 1]),
                          ticks[i].animate(rate_func=there_and_back).scale(1.5),
                          run_time=min(rt, c.until("binary")))
                self.wait(min(0.4, c.until("binary", floor=0)))
            self.sketch = VGroup(*circles, *arrows, *ticks, dot)
            c.wait_until("binary")

            # {binary}: n-bit counter, n FFs, 2^n states
            bin_a = MathTex(r"n\text{-bit binary counter:}", font_size=46)
            bin_b = MathTex(r"n\ \text{flip-flops},\ ", r"2^n", r"\ \text{states}", font_size=46)
            bin_b[1].set_color(GOLD)
            VGroup(bin_a, bin_b).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to(DOWN * 0.8)
            self.play(*appear(bin_a), run_time=1.0)
            c.wait_until("It has N")
            self.play(*appear(bin_b), run_time=min(1.2, c.until("order")))
            c.wait_until("order")

            # {order}: 0, 1, 2, ..., 2^n - 1, 0, 1, ...
            row = MathTex("0", r",\ ", "1", r",\ ", "2", r",\ ", r"\dots", r",\ ", "2^n - 1",
                          r",\ ", "0", r",\ ", "1", r",\ ", r"\dots", font_size=50).move_to(DOWN * 2.1)
            row[8].set_color(GOLD)
            c.wait_until("zero")
            self.play(*appear(*row[0:6], lag=0.3, shift=None), run_time=min(1.4, c.until("and so on")))
            c.wait_until("and so on")
            self.play(*appear(*row[6:8], shift=None), run_time=0.7)
            c.wait_until("up to")
            self.play(*appear(*row[8:10], shift=None), run_time=min(1.0, c.until("goes back")))
            c.wait_until("and then")
            # the tail of the row arrives, then a YELLOW arrow curves from the second 0 back to the first
            back = CurvedArrow(row[10].get_bottom() + 0.12 * DOWN, row[0].get_bottom() + 0.12 * DOWN,
                               angle=-PI / 4, color=YELLOW, stroke_width=4, tip_length=0.22)
            self.play(*during(appear(*row[10:], lag=0.2, shift=None), 0, 0.4),
                      *during([Create(back)], 0.4, 1.0),
                      run_time=min(1.8, c.until(floor=0.9)))
            self.row = VGroup(*row, back)
            self.bin = VGroup(bin_a, bin_b)

    # ------------------------------------------------ the 3-bit ring
    def clip2(self):
        with self.say("c4.def.2") as c:
            ring = state_ring().shift(RIGHT * -1.4 + DOWN * 0.55)
            self.ring = ring
            c.wait_until("with three")
            self.play(*[FadeOut(m) for m in (self.sketch, self.bin, self.row)],
                      self.defn.animate.scale(0.82).move_to(UP * 3.05), run_time=1.0)
            self.play(*appear(*ring.nodes, lag=0.15, shift=None), run_time=min(1.6, c.until("eight")))
            self.play(*[GrowArrow(a) for a in ring.arrows], run_time=min(0.9, c.until("eight")))
            c.wait_until("eight")

            # {eight}: 2^3 = 8, decimals 0..7
            eight = MathTex(r"2^3 = 8", font_size=64, color=GOLD).move_to([4.4, 2.0, 0])
            self.play(*appear(eight), run_time=1.0)
            c.wait_until("counts from zero")
            self.play(*appear(*ring.decimals, lag=0.2, shift=None), run_time=min(1.8, c.until("bits")))
            settle(self, ring)
            c.wait_until("bits")

            # {bits}: Q2 Q1 Q0, Q2 the most significant bit
            head = MathTex("Q_2", r"\ \ Q_1", r"\ \ Q_0", font_size=56, color=GREEN).move_to([4.4, 0.4, 0])
            self.play(*appear(head), run_time=1.0)
            tag = label_pointer("most significant\nbit", head[0], direction=DOWN, color=YELLOW, size=30)
            c.wait_until(own_word=tag[0], cue="most significant")
            self.play(*appear(tag, shift=None), run_time=1.0)   # arrow + label fade in together, in place under Q2
            self.side = VGroup(eight, head, tag)
            c.wait_until("wrap")

            # {wrap}: a dot steps round the ring, one clock tick per step
            dot = Dot(ring.out_point(0), radius=0.14, color=YELLOW)
            tick = edge_tick(w=0.5, h=0.34, width=5).move_to(ring.hub)
            self.play(FadeIn(dot, scale=0.5), *appear(tick, shift=None), run_time=0.6)
            budget = max(2.0, c.until("after seven") - 0.1)
            weights = [1.5, 1.2, 0.9, 0.8, 0.8, 0.8, 0.8]
            hub = ring.hub.get_center()
            for k, wgt in enumerate(weights):
                rt = budget * wgt / sum(weights)
                self.play(Rotate(dot, angle=-PI / 4, about_point=hub, rate_func=smooth),
                          tick.animate(rate_func=there_and_back).scale(1.4),
                          run_time=0.75 * rt)
                self.wait(0.25 * rt)
            c.wait_until("wraps back")
            self.play(Rotate(dot, angle=-PI / 4, about_point=hub),
                      tick.animate(rate_func=there_and_back).scale(1.4),
                      ring.arrows[-1].animate.set_color(YELLOW),
                      run_time=min(1.2, c.until(floor=0.5)))
            self.dot, self.tick = dot, tick

    # ------------------------------------------------ what counters are for
    def clip3(self):
        with self.say("c4.def.3") as c:
            ring = self.ring
            self.play(*during([FadeOut(self.defn), FadeOut(self.side), FadeOut(self.dot), FadeOut(self.tick)], 0, 0.5),
                      *during([ring.animate.move_to([-3.75, -0.2, 0])], 0.3, 1.0), run_time=1.4)
            c.wait_until("counting")

            items = [T("Counting", 32),
                     T("Producing delays of a\nparticular duration", 32),
                     T("Sequencers for control\nlogic in a processor", 32),
                     T("Divide by m counter\n(a divider), as used\nin a digital watch", 32)]
            uses = VGroup(*items).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            uses.move_to([1.6, -0.1, 0]).align_to([-0.4, 0, 0], LEFT)
            for it, cue, nxt in zip(items, ["counting", "delays", "sequencers", "divider"],
                                    ["delays", "sequencers", "divider", "memories"]):
                c.wait_until(cue)
                if cue != "divider":
                    self.play(*appear(it), run_time=min(1.0, c.until(nxt)))
            watch = digital_watch()
            watch.scale(4.6 / watch.width).move_to(ring.get_center())
            for m in watch.family_members_with_points():
                m.set_stroke(width=m.get_stroke_width() * 0.6)
            # {divider}: the ring has done its job; the watch takes its place beside the list
            self.play(*during([FadeOut(ring)], 0, 0.45), *during([FadeIn(watch, scale=0.85)], 0.45, 1.0),
                      *during(appear(items[3]), 0.3, 1.0), run_time=min(1.6, c.until("memories")))
            c.wait_until("memories")

            # {memories}: the ring and watch go, the list moves left, the aside card arrives
            self.play(*during([FadeOut(watch)], 0, 0.4),
                      *during([uses.animate.to_edge(LEFT, buff=0.5)], 0.4, 1.0), run_time=1.4)
            lines = [T("Memories", 30, color=FG),
                     T("Shift register", 30, color=FG),
                     T("Parallel loading shift register:\n    parallel to serial conversion", 30, color=DIM),
                     T("Serial in, parallel out shift register:\n    serial to parallel conversion", 30, color=DIM)]
            body = VGroup(*lines).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            frame = RoundedRectangle(corner_radius=0.2, width=body.width + 0.8, height=body.height + 0.8,
                                     color=DIM, stroke_width=2).move_to(body)
            card = VGroup(frame, body)
            card.move_to([2.3, -0.3, 0])
            self.play(FadeIn(frame), *appear(lines[0]), run_time=1.0)
            c.wait_until("shift registers")
            self.play(*appear(lines[1]), run_time=0.8)
            c.wait_until("convert data")
            self.play(*appear(*lines[2:], lag=0.5), run_time=min(1.6, c.until("next lecture")))
            nxt = T("next lecture", 30, color=YELLOW, slant=ITALIC).next_to(frame, UP, buff=0.2).align_to(frame, RIGHT)
            c.wait_until("next lecture")
            self.play(*appear(nxt), run_time=1.0)

    # ------------------------------------------------ two kinds; why study ripple
    def clip4(self):
        with self.say("c4.def.4") as c:
            c.wait_until("two basic")
            self.play(FadeOut(*self.mobjects), run_time=min(1.0, c.until("ripple")))
            ripple = T("ripple\ncounters", 48).move_to([-3.4, 1.9, 0])
            sync = T("synchronous\ncounters", 48).move_to([3.4, 1.9, 0])
            c.wait_until("ripple")
            self.play(*appear(ripple), run_time=0.6)
            c.wait_until("sync")
            self.play(*appear(sync), run_time=1.0)
            c.wait_until("avoid")

            avoid = T("do not follow synchronous\ndesign principles:\navoid if at all possible",
                      30, color=RED).move_to([-3.4, -0.8, 0])
            self.play(*appear(avoid), run_time=1.2)
            c.wait_until("why")

            lens = Circle(radius=1.5, color=YELLOW, stroke_width=8).set_fill(YELLOW, 0.06).move_to(ripple)
            d = np.array([np.cos(-PI / 4), np.sin(-PI / 4), 0.0])
            handle = Line(lens.get_center() + 1.5 * d, lens.get_center() + 2.5 * d,
                          color=YELLOW, stroke_width=14)
            glass = VGroup(lens, handle)
            self.play(FadeIn(glass, scale=1.25), run_time=1.4)
            quote = T("We will now look at the problems with ripple counters", 34).move_to(DOWN * 3.0)
            self.play(*appear(quote), run_time=1.0)
        self.wait(1.5)   # let the closing line sit before the fade
