"""Chapter 1, scene 4: notation, and who invented it. Clips c1.notation.1 – c1.notation.4.

Opens on s3's handover shot (the x^3 -> 3x^2 card, top-left), which stays untouched until the end.
(103)'s box returns, its GREEN dy/dx lifts out to the centre, then parks top-right while a timeline
builds: Newton / Leibniz, the dates, the quarrel, their styles, Britain vs the rest, Newton's dot,
Euler and Lagrange, India. The timeline clears into the notes' "Other notations" line, lit item by
item, the dot notation, and what this course uses. Last: dy/dx splits into the operator d/dx acting
on y; then dy over dx pulled apart, "not a quotient", and the Part 3 preview. Ends on an empty frame.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TL_Y = 0.3                    # timeline height
XN, XL, X87, XE, XG, XI = -3.0, 0.6, 2.4, 4.2, 5.75, -5.6
NAME_Y = 1.95
YEAR_Y = -0.1
CAP_Y = -0.7
R1, R2, R3 = -1.6, -2.4, -3.2
DY_POS = np.array([5.7, 3.0, 0])


def mtx(s, size=44, color=FG):
    return MathTex(s, font_size=size, color=color)


def tick(x, color=GOLD, h=0.14):
    return Line([x, TL_Y - h, 0], [x, TL_Y + h, 0], color=color, stroke_width=4)


def year(x, s, cap):
    t = tick(x)
    y = T(s, 30, GOLD).move_to([x, YEAR_Y, 0])
    c = T(cap, 28, DIM, line_spacing=0.8).move_to([x, CAP_Y, 0])
    return t, y, c


def zigzag(x0, x1, y, n=6, amp=0.12):
    pts = []
    for i in range(n + 1):
        pts.append([x0 + (x1 - x0) * i / n, y + (amp if i % 2 else -amp), 0])
    return VMobject().set_points_as_corners(pts).set_stroke(RED, 4)


def frac_parts(m):
    """(top glyphs left to right, bar, bottom glyphs left to right) of a one-fraction MathTex."""
    g = list(m.submobjects)
    bar = max(g, key=lambda s: s.width / max(s.height, 1e-3))
    cy = bar.get_center()[1]
    top = sorted([s for s in g if s is not bar and s.get_center()[1] > cy], key=lambda s: s.get_x())
    bot = sorted([s for s in g if s is not bar and s.get_center()[1] < cy], key=lambda s: s.get_x())
    return top, bar, bot


def split_moves(hero, split):
    """dy/dx comes apart into d/dx and y: every glyph slides to its place, nothing fades."""
    (d1, y), bar, bot = frac_parts(hero[0])
    (d2,), bar2, bot2 = frac_parts(split[0])
    anims = [d1.animate.move_to(d2).set_color(BLUE),
             y.animate(path_arc=-0.6).move_to(split[1]).set_color(GREEN),
             bar.animate.stretch_to_fit_width(bar2.width).move_to(bar2).set_color(BLUE)]
    anims += [a.animate.move_to(b).set_color(BLUE) for a, b in zip(bot, bot2)]
    return anims


class Notation(NarratedScene):
    def construct(self):
        card = load_scene("ch1_s3_cube").handover_shot()
        self.add(card)
        self.card = card
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ history
    def clip1(self):
        box = load_scene("ch1_s2_chord").definition_box()
        box.scale(min(1.0, 11.5 / box.width)).move_to(1.3 * DOWN)
        hero = mtx(r"\frac{dy}{dx}", 110, GREEN).move_to(0.6 * UP)
        self.hero = hero

        line = Line([-6.5, TL_Y, 0], [6.6, TL_Y, 0], color=FG, stroke_width=3)
        newton = T("Isaac\nNewton", 32, YELLOW, line_spacing=0.8).move_to([XN, NAME_Y, 0])
        leib = T("Gottfried Wilhelm\nLeibniz", 32, YELLOW, line_spacing=0.8).move_to([XL, NAME_Y, 0])
        t86, y86, c86 = year(XL, "1686", "Leibniz\npublishes")
        t87, y87, c87 = year(X87, "1687", "Newton\npublishes")
        t65, y65, c65 = year(XN, "1665/66", "Newton's\nbreakthrough")
        brace = span_brace([XN, TL_Y + 0.14, 0], [XL, TL_Y + 0.14, 0], direction=UP, color=GOLD, buff=0.08)
        blab = T("some 20 years", 30, GOLD).next_to(brace, UP, buff=0.1)
        zig = zigzag(XN + 0.7, XL - 1.6, NAME_Y)
        qcap = T("each claiming\nto have been first", 28, RED, line_spacing=0.8)
        qcap.move_to([zig.get_center()[0], 3.05, 0])
        self.tl = dict(line=line, newton=newton, leib=leib, caps=[c65, c86, c87], brace=brace, blab=blab)

        with self.say("c1.notation.1") as c:
            self.play(*appear(box, shift=None), run_time=1.0)
            c.wait_until("dee why")
            self.play(FlashAround(box.formula[0], run_time=1.5, time_width=1.5))
            c.wait_until("has a history")
            self.play(*during(disappear(box), 0, 0.45), *fly(box.formula[0], hero), run_time=1.5)
            c.wait_until("two")
            self.play(hero.animate.scale(48 / 110).move_to(DY_POS), run_time=1.5)
            self.play(Create(line), run_time=1.0)
            c.wait_until(own_word=newton)
            self.play(*appear(newton), run_time=1.0)
            c.wait_until(own_word=leib)
            self.play(*appear(leib), run_time=1.0)
            c.wait_until("published")
            self.play(*appear(t86, y86, c86, shift=None, lag=0.3), run_time=1.3)
            c.wait_until("Newton", nth=1)
            self.play(*appear(t87, y87, c87, shift=None, lag=0.3), run_time=1.3)
            c.wait_until("breakthrough")
            self.play(*appear(t65, y65, c65, shift=None, lag=0.3), run_time=1.3)
            c.wait_until("twenty years")
            self.play(GrowFromCenter(brace), *appear(blab, shift=None), run_time=1.2)
            c.wait_until("quarrel")
            self.play(Create(zig), *appear(qcap), run_time=1.3)
        self.zig, self.qcap = zig, qcap

    def clip2(self):
        tl = self.tl
        limits = T("limits", 30).move_to([XN, R1, 0])
        geo = T("geometric arguments", 30).move_to([XL, R1, 0])
        dd = mtx(r"\frac{d}{dx}", 44, BLUE).move_to([XL - 0.55, R2, 0])
        integ = mtx(r"\int", 44, BLUE).move_to([XL + 0.55, R2, 0])
        brit = T("Britain, 18th century", 30, DIM).move_to([XN - 0.45, R3, 0])
        rest = T("rest of the world", 30, DIM).move_to([XL, R3, 0])
        arr = Arrow([2.45, R3 - 0.3, 0], [2.45, R3 + 0.4, 0], buff=0, color=GREEN, stroke_width=5)
        prog = T("more progress", 28, GREEN).next_to(arr, RIGHT, buff=0.15)
        dotf = MathTex(r"\dot{x}", "=", r"\frac{dx}{dt}", font_size=40, color=FG).move_to([XN, R2, 0])
        dot_glyph = min(dotf[0], key=lambda s: s.width * s.height)
        dot_glyph.set_color(YELLOW)
        still = T("still used", 28, DIM).next_to(dotf, RIGHT, buff=0.2)
        edot = Dot([XE, TL_Y, 0], radius=0.07, color=YELLOW)
        ename = T("Euler", 32, YELLOW).move_to([XE, NAME_Y, 0])
        enot = mtx(r"Df,\ D^2 f", 36, BLUE).move_to([XE, YEAR_Y, 0])
        gdot = Dot([XG, TL_Y, 0], radius=0.07, color=YELLOW)
        gname = T("Lagrange", 32, YELLOW).move_to([XG, NAME_Y, 0])
        gnot = mtx(r"f',\ f''", 36, BLUE).move_to([XG, YEAR_Y, 0])
        stud = T("his student", 28, DIM).move_to([XG, CAP_Y, 0])
        itick = tick(XI, DIM)
        inote = T("India: similar\nideas, a couple\nof centuries\nearlier", 28, DIM, line_spacing=0.8)
        inote.move_to([XI, 0, 0]).align_to(itick, UP).shift(0.4 * DOWN)
        inote.to_edge(LEFT, buff=0.5)

        with self.say("c1.notation.2", gap=1.2) as c:
            c.wait_until(own_word=limits)
            self.play(*disappear(self.zig, self.qcap),
                      *set_alpha(tl["caps"] + [tl["brace"], tl["blab"]], 0.45), *during(appear(limits), 0.4, 1),
                      run_time=1.4)
            c.wait_until(own_word=geo)
            self.play(*appear(geo), run_time=1.0)
            c.wait_until("dee by dee ex")
            self.play(*appear(dd), run_time=1.0)
            c.wait_until("integral")
            self.play(*appear(integ), run_time=1.0)
            c.wait_until(own_word=brit)
            self.play(*appear(brit), run_time=1.0)
            c.wait_until(own_word=rest)
            self.play(*appear(rest), run_time=1.0)
            c.wait_until("progress")
            self.play(GrowArrow(arr), *appear(prog), run_time=1.2)
            c.wait_until("dot")
            self.play(*appear(dotf), run_time=1.2)
            c.wait_until("survives")
            self.play(*appear(still), run_time=1.0)
            c.wait_until("Oiler")
            self.play(GrowFromCenter(edot), *appear(ename), run_time=1.0)
            c.wait_until("capital D")
            self.play(*appear(enot), run_time=1.0)
            c.wait_until(own_word=gname)
            self.play(GrowFromCenter(gdot), *appear(gname, stud, lag=0.4), run_time=1.2)
            c.wait_until("primes")
            self.play(*appear(gnot), run_time=1.0)
            c.wait_until("India")
            self.play(GrowFromCenter(itick), *appear(inote), run_time=1.2)

    # ------------------------------------------------------------------ the notes' list
    def clip3(self):
        title = T("Other notations", 36, DIM).move_to(2.55 * UP)
        parts = [r"\frac{dy}{dx}", r",\quad", r"\frac{d}{dx}y", r",\quad", "y'", r",\quad",
                 "y_x", r",\quad", "y_{,x}", r",\quad", "Dy"]
        lst = MathTex(*parts, font_size=64, color=FG).move_to(1.3 * UP)
        lst.set_opacity(0.3)
        self.lst = lst
        items = [lst[i] for i in (0, 2, 4, 6, 8, 10)]
        commas = [lst[i] for i in (1, 3, 5, 7, 9)]

        dotu = MathTex(r"\dot{u}", r"\equiv", r"\frac{du}{dt}", font_size=52, color=FG).move_to(1.75 * DOWN)
        min(dotu[0], key=lambda s: s.width * s.height).set_color(YELLOW)
        ulab = VGroup(T("a function of time,", 30, DIM), MathTex("u(t)", font_size=36, color=DIM))
        ulab.arrange(RIGHT, buff=0.15).next_to(dotu, DOWN, buff=0.35)

        ticks = [check_mark(GREEN).scale(0.8).next_to(items[i], DOWN, buff=0.3) for i in (0, 1, 2)]
        ty = min(t.get_center()[1] for t in ticks)
        for t in ticks:
            t.set_y(ty)
        course = T("this course", 30, GREEN).next_to(VGroup(*ticks), DOWN, buff=0.2)
        later = T("later, especially\nnext term", 28, DIM, line_spacing=0.8)
        later.next_to(items[5], DOWN, buff=0.3)
        self.board3 = [title, dotu, ulab, *ticks, course, later]

        def light(*idx, rt=1.0):
            anims = []
            for i in idx:
                anims += set_alpha([items[i]], 1)
                if i > 0:
                    anims += set_alpha([commas[i - 1]], 1)
            self.play(*anims, *[FlashUnder(items[i], color=YELLOW) for i in idx], run_time=rt)

        with self.say("c1.notation.3", gap=1.5) as c:
            keep = [self.card]
            sweep_clear(self, *appear(title, lst, lag=0.3), keep=keep, run_time=1.8)  # early: the list shown whole, then walked
            c.wait_until("First")
            light(0, rt=1.2)
            c.wait_until("acting")
            light(1)
            c.wait_until("prime")
            light(2, rt=0.8)
            c.wait_until("subscript")
            light(3, 4, rt=0.8)
            c.wait_until("capital D")
            light(5, rt=0.8)
            c.wait_until("time")
            self.play(*appear(dotu), run_time=1.2)
            self.play(*appear(ulab), run_time=1.0)
            c.wait_until("fractions")
            self.play(*appear(ticks[0], ticks[1], shift=None, lag=0.3), run_time=1.0)
            c.wait_until("primes")
            self.play(*appear(ticks[2], shift=None), *appear(course), run_time=1.0)
            c.wait_until("capital D comes")
            self.play(*appear(later), run_time=1.0)

    # ------------------------------------------------------------------ operator, not a quotient
    def clip4(self):
        lst = self.lst
        hero = mtx(r"\frac{dy}{dx}", 96, GREEN).move_to(1.5 * UP)
        split = MathTex(r"\frac{d}{dx}", r"y", font_size=96, color=FG)
        split.arrange(RIGHT, buff=0.5).move_to(1.5 * UP)
        split[0].set_color(BLUE)
        split[1].set_color(GREEN)
        acting_arc = CurvedArrow(split[0].get_top() + 0.15 * UP + 0.2 * RIGHT,
                                 split[1].get_top() + 0.15 * UP, angle=-PI / 2, color=FG)
        acting = T("acting on y", 30).next_to(acting_arc, UP, buff=0.1)
        opl = T("differential operator", 30, BLUE).next_to(split[0], DOWN, buff=0.3)

        frac = mtx(r"\frac{dy}{dx}", 80).move_to([-2.0, -2.0, 0])
        g = frac[0]
        bar = max(g, key=lambda s: s.width / max(s.height, 1e-3))
        cy = bar.get_center()[1]
        top = [s for s in g if s is not bar and s.get_center()[1] > cy]
        bot = [s for s in g if s is not bar and s.get_center()[1] < cy]
        qmark = T("?", 56, YELLOW)
        preview = MathTex(r"\frac{dx}{dy} = 1 \Big/ \frac{dy}{dx}", font_size=40, color=DIM)
        preview.move_to([3.4, -2.0, 0])
        p3 = T("proved in Part 3", 30, DIM).next_to(preview, DOWN, buff=0.3)

        with self.say("c1.notation.4") as c:
            others = [m for m in self.mobjects if m is not self.card]
            self.play(*during(disappear(*others), 0, 0.45), *during(fly(lst[0], hero), 0.3, 1.0),
                      run_time=1.8)
            c.wait_until("as an operator")
            self.play(*split_moves(hero, split), run_time=1.6)
            self.remove(hero)
            self.add(split)
            self.play(*appear(opl), run_time=1.0)
            c.wait_until("acting")
            self.play(Create(acting_arc), *appear(acting), run_time=1.2)
            c.wait_until("quotient")
            self.play(*set_alpha([split, opl, acting_arc, acting], 0.4), *appear(frac, shift=None),
                      run_time=1.0)
            self.play(*[s.animate.shift(0.35 * UP) for s in top],
                      *[s.animate.shift(0.35 * DOWN) for s in bot],
                      bar.animate.stretch(1.8, 0), run_time=1.5)
            qmark.next_to(frac, RIGHT, buff=0.35)
            self.play(*appear(qmark), run_time=0.8)
            c.wait_until("treat")
            self.play(*appear(preview), run_time=1.2)
            c.wait_until("is not")
            tag = T("not a quotient", 30, RED).next_to(bar, LEFT, buff=0.3)
            self.play(bar.animate.set_color(RED), *appear(tag), run_time=1.2)
            c.wait_until("part three")
            self.play(*appear(p3), run_time=1.0)
