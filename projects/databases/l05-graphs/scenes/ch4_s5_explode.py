"""Chapter 4, scene 5: ranges, the bare star, and the explosion of path counts. Clips c4.explode.1 – c4.explode.4."""
# style: 2
import sys
from math import log10
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

IND = " " * 13          # aligns under "MATCH path = "
CS = 28                 # code size (51-char first line ≈ 11.9 wide)


def query(star):
    return (f"MATCH path = (a:Person {{name: 'Jennifer Lawrence'}})\n"
            f"{IND}-[:ACTED_IN{star}]-\n"
            f"{IND}(b:Person {{name: 'Daniel Radcliffe'}})\n"
            f"RETURN count(path);")


CRASH6 = (f"MATCH path = (a:Person {{name: 'Jennifer Lawrence'}})\n"
          f"{IND}-[:ACTED_IN*6]- (b:Person)\n"
          f"RETURN count(path);")
CRASH_BARE = (f"MATCH path = (a:Person {{name: 'Jennifer Lawrence'}})\n"
              f"{IND}-[:ACTED_IN*]-\n"
              f"{IND}(b:Person {{name: 'Daniel Radcliffe'}})\n"
              f"RETURN count(path);")

CODE_TOP = 2.9

# the table: length | paths | different people at the end
LENGTHS = [2, 4, 6, 8]
PATHS = [153, 12160, 700512, 39584716]
PEOPLE = [117, 3985, 12686, 14072]
CEILING = 14581
ROW_Y = [1.65, 0.5, -0.65, -1.8]
HEAD_Y = 2.75


def place_code(code):
    code.shift([-code.get_center()[0], CODE_TOP - code.get_top()[1], 0])
    return code


def _monotone(xs, ys, n=80):
    """Fritsch–Carlson monotone cubic through (xs, ys), sampled n times (no overshoot)."""
    xs, ys = np.array(xs, float), np.array(ys, float)
    h = np.diff(xs)
    d = np.diff(ys) / h
    m = np.zeros(len(xs))
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, len(xs) - 1):
        m[i] = 0 if d[i - 1] * d[i] <= 0 else 3 * (h[i - 1] + h[i]) / ((2 * h[i] + h[i - 1]) / d[i - 1] + (h[i] + 2 * h[i - 1]) / d[i])
    out = []
    for t in np.linspace(xs[0], xs[-1], n):
        i = min(np.searchsorted(xs, t, side="right") - 1, len(xs) - 2)
        s = (t - xs[i]) / h[i]
        h00, h10, h01, h11 = 2 * s**3 - 3 * s**2 + 1, s**3 - 2 * s**2 + s, -2 * s**3 + 3 * s**2, s**3 - s**2
        out.append((t, h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1]))
    return out


def paths_plot():
    """The {curve} plot: log-scale y (10^0..10^8), x = path length 2–8.

    Returns a VGroup with parts: .axes, .yticks (10^2..10^8 labels), .xticks (2,4,6,8),
    .log_label ("log scale"), .x_label ("path length"), .gold_curve, .gold_dots (4), .gold_label
    ("paths"), .pink_curve, .pink_dots (4), .pink_label ("people"), .ceiling (DashedLine at 14,581),
    .ceiling_label (2 lines). Sits at its scene position (x -6.3..6.2, y -3.5..3.4); scale/move freely.
    """
    ax = Axes(x_range=[1, 8.6, 1], y_range=[0, 8, 2], x_length=7.0, y_length=5.4, tips=False,
              axis_config={"color": DIM, "stroke_width": 2.5})
    ax.shift(np.array([-5.4, -2.6, 0]) - ax.c2p(1, 0))
    yt = VGroup(*[MathTex(f"10^{{{k}}}", font_size=34, color=DIM).next_to(ax.c2p(1, k), LEFT, buff=0.18)
                  for k in (2, 4, 6, 8)])
    xt = VGroup(*[T(str(k), 30, DIM).next_to(ax.c2p(k, 0), DOWN, buff=0.18) for k in LENGTHS])
    log_label = T("log scale", 28, DIM).next_to(ax.c2p(1, 8), UP, buff=0.22).align_to(yt, LEFT)
    x_label = T("path length", 28, DIM).next_to(ax.c2p(4.8, 0), DOWN, buff=0.62)

    def curve(vals, color):
        pts = [(x, log10(v)) for x, v in zip(LENGTHS, vals)]
        c = VMobject().set_points_smoothly([ax.c2p(x, y) for x, y in _monotone(*zip(*pts))])
        c.set_stroke(color, 5)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.09, color=color) for x, y in pts])
        return c, dots

    gc, gd = curve(PATHS, GOLD)
    pc, pd = curve(PEOPLE, PINK)
    gl = T("paths", 32, GOLD).next_to(gd[-1], RIGHT, buff=0.22)
    pl = T("people", 32, PINK).next_to(ax.c2p(7.0, log10(PEOPLE[2]) - 0.75), ORIGIN)
    cy = log10(CEILING)
    ceil = DashedLine(ax.c2p(1, cy), ax.c2p(8.6, cy), dash_length=0.14).set_stroke(FG, 2.5)
    cl = VGroup(T("14,581 connected to her", 30, FG), T("(counting herself)", 28, DIM))
    cl.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(ceil, RIGHT, buff=0.25)
    g = VGroup(ax, yt, xt, log_label, x_label, gc, gd, gl, pc, pd, pl, ceil, cl)
    (g.axes, g.yticks, g.xticks, g.log_label, g.x_label, g.gold_curve, g.gold_dots, g.gold_label,
     g.pink_curve, g.pink_dots, g.pink_label, g.ceiling, g.ceiling_label) = g
    return g


class Explode(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- ranges
    def clip1(self):
        with self.say("c4.explode.1") as c:
            code = place_code(Code(query("*4"), size=CS))
            self.play(*appear(code, shift=None), run_time=1.0)
            box = token_box(code.find("*4"), code.line(1))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("range")
            new = place_code(Code(query("*2..6"), size=CS))
            nbox = token_box(new.find("*2..6"), new.line(1))
            self.play(*edit(code, new), Transform(box, nbox), run_time=1.5)
            code = new
            c.wait_until("twosix")
            self.play(FlashUnder(code.find("*2..6"), run_time=1.5, time_width=1.5))

            # reply + the sum underneath
            c.wait_until("zero plus eight")
            s1 = T("0 + 8 + 495", 48, GOLD).move_to([-3.0, -1.4, 0])
            self.play(*appear(s1), run_time=1.0)
            c.wait_until("total")
            head = Mono("count(path)", 30, DIM)
            rule = Line(LEFT, RIGHT).set_stroke(DIM, 2).set_width(head.width + 0.3)
            val = Mono("503", 44, GOLD)
            reply = VGroup(head, rule, val).arrange(DOWN, buff=0.18).move_to([3.4, -1.2, 0])
            s2 = T("0 + 8 + 495 = 503", 48, GOLD)
            s2.shift(s1[0].get_center() - s2[0].get_center())
            self.play(*edit(s1, s2), *appear(head, rule, val, shift=None, lag=0.2), run_time=1.5)
            s1 = s2

            c.wait_until("upto")
            new = place_code(Code(query("*..4"), size=CS))
            nbox = token_box(new.find("*..4"), new.line(1))
            note = T("1 to 4", 44, DIM).move_to([-3.0, -1.4, 0])
            v8 = Mono("8", 44, GOLD).move_to(val)
            self.play(*edit(code, new), Transform(box, nbox), run_time=1.5)
            code = new
            c.wait_until("as in star")
            self.play(*swap(s1, note), *swap(val, v8), run_time=1.2)
            val = v8

            c.wait_until("bare")
            new = place_code(Code(query("*"), size=CS))
            nbox = token_box(new.find("*"), new.line(1))
            self.play(*edit(code, new), Transform(box, nbox), run_time=1.5)
            code = new
            note2 = T("1 or more", 44, DIM).move_to(note)
            q = T("?", 72, GOLD).move_to(val)
            self.play(*swap(note, note2), *swap(val, q), run_time=1.2)
            c.wait_until("how")
            self.play(FlashAround(q, run_time=1.5, time_width=1.5))
        self.code, self.box, self.reply_head, self.reply_rule, self.q, self.note = code, box, head, rule, q, note2

    # ---------------------------------------------------------------- the fan and the table
    def clip2(self):
        with self.say("c4.explode.2") as c:
            rad = [g for g in self.code.line(2)]
            self.play(*disappear(*rad), run_time=0.8)
            rest = place_code(Code(query("*"), size=CS))
            for g in rest.line(2):
                g.set_opacity(0)
            self.remove(*self.code.get_family())
            self.add(rest)
            me = Dot([-4.6, -0.3, 0], radius=0.13, color=PINK)
            name = VGroup(T("Jennifer", 28), T("Lawrence", 28)).arrange(DOWN, buff=0.1, aligned_edge=RIGHT)
            name.next_to(me, LEFT, buff=0.2)
            h_len = T("length", 30, DIM).move_to([-0.5, HEAD_Y, 0])
            h_paths = T("paths", 30, GOLD)
            h_paths.move_to([3.5 - h_paths.width / 2, HEAD_Y, 0])
            sweep_clear(self, *appear(me, name, h_len, h_paths, shift=None, lag=0.15), run_time=1.6)

            # her 17 films, each with 9 co-stars
            c.wait_until("one")
            ys = np.linspace(2.35, -2.85, 17)
            films = VGroup(*[Square(0.17).set_stroke(BLUE, 0).set_fill(BLUE, 1).move_to([-3.5, y, 0]) for y in ys])
            lines = VGroup(*[Line(me.get_center(), f.get_left(), buff=0.12).set_stroke(BLUE, 1.6, opacity=0.6)
                             for f in films])
            stars = VGroup(*[Dot([-3.1 + 0.2 * k, y, 0], radius=0.05, color=PINK) for y in ys for k in range(9)])
            l2 = Mono("2", 40).move_to([-0.5, ROW_Y[0], 0])
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.04),
                      LaggedStart(*[FadeIn(f, scale=0.5) for f in films], lag_ratio=0.04),
                      FadeIn(l2), run_time=1.6)
            c.wait_until("nine other actors")
            self.play(LaggedStart(*[FadeIn(d) for d in stars], lag_ratio=0.01), run_time=1.6)
            c.wait_until("seventeen times nine")
            f_left = T("17 × 9 =", 40, GOLD)
            f_num = Mono("153", 40, GOLD)
            formula = VGroup(f_left, f_num).arrange(RIGHT, buff=0.2).move_to([-3.6, -3.45, 0])
            self.play(*appear(f_left, f_num, shift=None, lag=0.4), run_time=1.2)
            c.wait_until("nine a hundred")
            p0 = self.pcell(PATHS[0], 0)
            self.play(*fly(f_num, p0, arc=PI / 6), run_time=1.5)
            fan = VGroup(lines, films, stars)
            settle(self, fan)

            rows = [(l2, p0)]
            for i, cue in ((1, "grow"), (2, "six"), (3, "eight")):
                c.wait_until(cue)
                li = Mono(str(LENGTHS[i]), 40).move_to([-0.5, ROW_Y[i], 0])
                pi = self.pcell(PATHS[i], i)
                extra = []
                if i == 1:
                    extra = [restyle(fan, 0.35)]
                if i == 2:
                    foot = T("lengths 6 and 8 counted outside Traverse, with Cypher's rules", 28, DIM)
                    foot.move_to([0, -3.5, 0])
                    extra = [*swap(formula, foot)]
                self.play(*appear(li, pi, shift=None, lag=0.2), *extra, run_time=1.0)  # early: footnote read as a note
                rows.append((li, pi))
            self.foot = foot

            # one path carries on
            c.wait_until("factor")
            d = stars[8]
            self.play(restyle(lines[0], op=1, outline=YELLOW), restyle(films[0], op=1),
                      restyle(d, op=1, fill=YELLOW), FlashAround(d, color=YELLOW), run_time=1.5)

            arcs = []
            for i, (cue, nth, txt) in enumerate((("about eighty", 0, "× 79"), ("then sixty", 0, "× 58"),
                                                 ("sixty again", 0, "× 57"))):
                c.wait_until(cue, nth=nth)
                a = CurvedArrow([3.7, ROW_Y[i] - 0.05, 0], [3.7, ROW_Y[i + 1] + 0.05, 0], angle=-PI / 1.6,
                                color=GOLD, stroke_width=3, tip_length=0.18)
                lab = T(txt, 32, GOLD).next_to(a, RIGHT, buff=0.15)
                self.play(Create(a), *appear(lab, shift=None), run_time=0.9)
                arcs += [a, lab]
        self.me, self.name, self.fan = me, name, fan
        self.rows, self.heads, self.arcs = rows, [h_len, h_paths], arcs

    def pcell(self, v, i):
        m = Mono(f"{v:,}", 40, GOLD)
        m.move_to([3.5 - m.width / 2, ROW_Y[i], 0])
        return m

    # ---------------------------------------------------------------- people, and the plot
    def clip3(self):
        with self.say("c4.explode.3") as c:
            self.play(*disappear(self.fan, self.me, self.name), run_time=0.9)
            dx = -3.5 * RIGHT
            items = self.heads + [m for r in self.rows for m in r] + self.arcs
            h_people = T("different people at the end", 30, PINK).move_to([3.3, HEAD_Y, 0])
            self.play(*[m.animate.shift(dx) for m in items], run_time=1.3)
            c.wait_until("people")   # already past: the voice names it at the start
            self.play(*appear(h_people), run_time=0.9)

            cells = []
            for i, cue in enumerate(("hundred and seventeen", "four thousand", "twelve and a half",
                                     "fourteen thousand")):
                c.wait_until(cue)
                m = Mono(f"{PEOPLE[i]:,}", 40, PINK)
                m.move_to([4.4 - m.width / 2, ROW_Y[i], 0])
                self.play(*appear(m, shift=None), run_time=0.7)
                cells.append(m)

            # the table becomes the plot
            c.wait_until("curve")
            plot = paths_plot()
            frame = [plot.axes, plot.yticks, plot.xticks, plot.log_label, plot.x_label]
            sweep_clear(self, *appear(*frame, shift=None, lag=0.1), run_time=1.6)  # early: axis labels belong to the frame
            self.play(Create(plot.gold_curve), LaggedStart(*[FadeIn(d, scale=0.5) for d in plot.gold_dots], lag_ratio=0.25),
                      Create(plot.pink_curve), LaggedStart(*[FadeIn(d, scale=0.5) for d in plot.pink_dots], lag_ratio=0.25),
                      run_time=1.6)
            self.play(*appear(plot.gold_label, plot.pink_label, shift=None, lag=0.2), run_time=0.8)  # early: curve legend

            c.wait_until("ceiling")
            self.play(Create(plot.ceiling), run_time=1.3)
            c.wait_until("fourteen thousand five hundred")
            self.play(*appear(plot.ceiling_label, shift=None), run_time=1.0)

            c.wait_until("runout")
            self.play(VShowPassingFlash(plot.gold_curve.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.6)
            c.wait_until("people run out")
            self.play(VShowPassingFlash(plot.pink_curve.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.6)

            c.wait_until("per")
            top, bot = plot.gold_dots[-1].get_center(), plot.pink_dots[-1].get_center()
            gap = DoubleArrow(bot + 0.12 * UP, top + 0.12 * DOWN, buff=0, color=GOLD, stroke_width=3,
                              tip_length=0.18)
            per = T("≈ 2,800 paths per person", 32, GOLD).next_to(gap, RIGHT, buff=0.25)
            per.shift((gap.get_center()[1] - per.get_center()[1]) * UP)
            self.play(GrowFromCenter(gap), run_time=1.0)
            self.play(*appear(per, shift=None), run_time=1.0)
        self.plot = plot

    # ---------------------------------------------------------------- the crash
    def clip4(self):
        with self.say("c4.explode.4", gap=2.6) as c:
            self.play(*flash(list(self.plot.gold_dots[2:]), color=YELLOW, run_time=1.5, time_width=1.5))

            c.wait_until("crash")
            code = place_code(Code(CRASH6, size=CS))
            sweep_clear(self, *appear(code, shift=None), run_time=1.6)
            err = Mono("Error: unreachable", 36, RED).move_to([0, -0.4, 0])
            c.wait_until("error unreachable")
            self.play(*appear(err), run_time=1.0)
            c.wait_until("meaning")
            tag = T("the engine gave up; it says nothing about the graph", 30, DIM).move_to([0, -1.4, 0])
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("barecrash")
            new = place_code(Code(CRASH_BARE, size=CS))
            self.play(*edit(code, new), run_time=1.6)
            code = new
            c.wait_until("same way")
            self.play(FlashAround(err, color=RED, run_time=1.5, time_width=1.5))

            c.wait_until("lesson")
            box = token_box(code.find("*"), code.line(1))
            q = T("?", 72, GOLD).move_to([0, -0.9, 0])
            self.play(FadeIn(box), *disappear(err, tag), *during(appear(q, shift=None), 0.45, 1), run_time=1.0)
            c.wait_until("but it can")
            big = T("a very large number of paths", 48, GOLD).move_to(q)
            self.play(*swap(q, big), run_time=1.2)
