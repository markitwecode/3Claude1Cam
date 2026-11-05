"""Chapter 1, scene 6: what "differentiable" demands. Clips c1.diff.1 – c1.diff.5.

Exports (for ch2 s3/s5, ch3 s3, ch1 recap):
  diff_box()  -> VGroup: the notes' differentiability box, BLUE border, every h TEAL.
                 .border .head .a .b .then .eq .lq .eqsign .rq   (lq / rq: left / right quotient)
  thumbs()    -> VGroup(v, step): the |x| V (left) and the Heaviside step (right) as at {runmod}:
                 s5's v_graph() / step_graph() scaled uniformly by 0.4 (so the V's arms are at 45deg).
                 v: .ax .curve .corner (.dot = .corner)
                 step: .ax .left .right .jump .hole .dot (.lo = .left, .hi = .right)
                 (changed 2026-11-03: was a 3.6 x 1.3 non-uniform redraw; same names kept as aliases)
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

HAND = "Bradley Hand"           # the lecturer's handwriting (as in L10)
H_MAP = {"h": TEAL}

# where things sit
BOX_SMALL_W = 8.6               # the box shrunk to the top (c3 on)
BOX_SMALL_TOP = 3.55
BOX_SMALL_SC = 0.86             # c3-c4: the box's text at ~26, so the graphs and three rows fit below
THUMB_Y = -1.5                  # the thumbnails' x-axes
V_POS = np.array([-3.4, THUMB_Y, 0])     # where each thumbnail's axes' origin sits
STEP_POS = np.array([3.4, THUMB_Y, 0])
ROW_A, ROW_B, ROW_C = -2.2, -2.7, -3.2


def hmath(tex, size=40, color=FG):
    """MathTex with every h TEAL (no 'h' may appear inside a command)."""
    return MathTex(tex, font_size=size, color=color, tex_to_color_map=H_MAP)


def diff_box():
    """The notes' differentiability box (p50), verbatim."""
    head = T("For a function f(x) to be differentiable at x:", 30)
    a = T("(a) the function must be continuous", 30)
    b = T("(b) the derivative f′ exists if it is finite and defined.", 30, disable_ligatures=True)
    then = VGroup(MathTex(r"\Rightarrow", font_size=32),
                  T("the left- and right-hand limits must be the same:", 30)).arrange(RIGHT, buff=0.15)
    lines = VGroup(head, a, b, then).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    lq = hmath(r"\lim_{h \to 0}\Big(\frac{f(x) - f(x-h)}{h}\Big)", 38)
    eqsign = MathTex("=", font_size=38)
    rq = hmath(r"\lim_{h \to 0}\Big(\frac{f(x+h) - f(x)}{h}\Big)", 38)
    eq = VGroup(lq, eqsign, rq).arrange(RIGHT, buff=0.3)
    VGroup(lines, eq).arrange(DOWN, buff=0.3)
    border = Rectangle(width=max(lines.width, eq.width) + 0.7,
                       height=lines.height + eq.height + 0.3 + 0.5).set_stroke(BLUE, 3)
    border.move_to(VGroup(lines, eq))
    box = VGroup(border, head, a, b, then, eq)
    box.border, box.head, box.a, box.b, box.then = border, head, a, b, then
    box.eq, box.lq, box.eqsign, box.rq = eq, lq, eqsign, rq
    return box


THUMB_K = 0.4                   # uniform scale of s5's graphs (unit 1.6 -> 0.64)


def thumbs():
    """s5's V and step (`load_scene("ch1_s5_fail").v_graph()` / `.step_graph()`), each scaled uniformly
    by THUMB_K, axes' origins level at y = THUMB_Y; dots and the hole kept at radius 0.08."""
    s5 = load_scene("ch1_s5_fail")
    v = s5.v_graph().scale(THUMB_K)
    step = s5.step_graph().scale(THUMB_K)
    for d in (v.corner, step.hole, step.dot):
        d.scale(0.08 / (0.09 * THUMB_K))
    v.shift(V_POS - v.ax.c2p(0, 0))
    step.shift(STEP_POS - step.ax.c2p(0, 0))
    v.dot = v.corner                        # older name
    step.lo, step.hi = step.left, step.right  # older names
    return VGroup(v, step)


def chord_sketch(side):
    """Tiny sketch: a BLUE curve, a TEAL chord from x-h to x (left) or x to x+h (right)."""
    f = lambda t: 0.28 * t * t + 0.25 * t  # noqa: E731
    sc = 0.62
    curve = ParametricFunction(lambda t: np.array([sc * t, sc * f(t), 0]), t_range=[-1.5, 1.5]).set_stroke(BLUE, 3)
    t0, t1 = (-1.0, 0.0) if side == "left" else (0.0, 1.0)
    p0, p1 = np.array([sc * t0, sc * f(t0), 0]), np.array([sc * t1, sc * f(t1), 0])
    chord = Line(p0, p1).set_stroke(TEAL, 5)
    dots = VGroup(Dot(p0, radius=0.06, color=TEAL), Dot(p1, radius=0.06, color=TEAL))
    base = -0.32
    axis = Line([-1.5 * sc, base, 0], [1.5 * sc, base, 0]).set_stroke(DIM, 2)
    guides = VGroup(*[DashedLine(p, [p[0], base, 0], dash_length=0.06).set_stroke(DIM, 2) for p in (p0, p1)])
    if side == "left":
        labs = [hmath(r"x-h", 30), MathTex("x", font_size=30)]
    else:
        labs = [MathTex("x", font_size=30), hmath(r"x+h", 30)]
    for lab, p in zip(labs, (p0, p1)):
        lab.next_to([p[0], base, 0], DOWN, buff=0.12)
    return VGroup(axis, curve, guides, chord, dots, *labs)


def row(tex, x_left, y, color=FG, size=34):
    m = MathTex(tex, font_size=size, color=color)
    m.move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
    return m


class Differentiable(NarratedScene):
    def construct(self):
        self.definition()
        self.the_box()
        self.run_mod()
        self.run_step()
        self.implies()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- c1
    def definition(self):
        with self.say("c1.diff.1") as c:
            hand = Text("f is differentiable at x if", font=HAND, font_size=44, color=YELLOW)
            dlim = hmath(r"\lim_{h \to 0}", 52, YELLOW)
            dfrac = hmath(r"\frac{f(x+h) - f(x)}{h}", 52, YELLOW)
            dmath = VGroup(dlim, dfrac).arrange(RIGHT, buff=0.2)
            tail = Text("exists and finite.", font=HAND, font_size=44, color=YELLOW)
            line2 = VGroup(dmath, tail).arrange(RIGHT, buff=0.4)
            hand.move_to(2.5 * UP)
            line2.move_to(1.0 * UP)
            self.hand, self.dmath, self.tail = hand, dmath, tail

            c.wait_until(own_word=hand)
            self.play(*appear(hand), run_time=1.2)
            c.wait_until("this limit")
            self.play(*appear(dmath), run_time=1.5)
            c.wait_until(own_word=tail)
            self.play(*appear(tail), run_time=1.0)

            # {quot}: (103)'s quotient slides up under the definition's fraction
            c.wait_until("quot")
            quot = MathTex(r"\frac{f(x+\delta x) - f(x)}{\delta x}", font_size=52,
                           tex_to_color_map={r"\delta x": TEAL})
            quot.move_to([dfrac.get_x(), -2.4, 0])
            self.play(*appear(quot, shift=None), run_time=0.9)
            self.play(quot.animate.move_to([dfrac.get_x(), -0.9, 0]), run_time=1.5)
            c.wait_until("over a small step")
            self.play(*flash(select(quot, r"\delta x"), color=TEAL), run_time=1.5)

            # {rename}: delta x becomes h
            c.wait_until("rename")
            quot_h = hmath(r"\frac{f(x+h) - f(x)}{h}", 52).move_to(quot)
            self.play(*edit(quot, quot_h), run_time=1.8)
            tag = T("h: just a variable", 32, color=DIM, t2c={"h:": TEAL})
            tag.next_to(quot_h, RIGHT, buff=0.7)
            self.play(*appear(tag), run_time=1.0)  # early: the tag names the rename just made; the next sentence reads it
            self.quot, self.tag = quot_h, tag

    # ---------------------------------------------------------------- c2
    def the_box(self):
        with self.say("c1.diff.2") as c:
            box = diff_box()
            defn = VGroup(self.hand, self.dmath, self.tail)
            s = 0.66
            box.move_to([0, 1.8 - box.height / 2, 0])
            self.box = box
            # the definition shrinks to the top; the box arrives below it
            self.play(*during(disappear(self.quot, self.tag), 0, 0.3),  # early: the notes' box shown whole, then walked line by line
                      *during([m.animate.scale(s, about_point=ORIGIN).shift(3.3 * UP - s * 2.5 * UP
                                                                         + 0.0 * RIGHT)
                               for m in (self.hand, self.dmath, self.tail)], 0.15, 0.6),
                      *during(appear(box, shift=None), 0.6, 1.0),
                      run_time=min(2.4, c.until("a")))  # early: the notes' box shown whole, then walked line by line
            self.defn = defn

            c.wait_until("a")
            self.play(*recolor(box.a, YELLOW), *flash([box.a]), run_time=1.2)
            c.wait_until("b")
            self.play(*recolor(box.a, FG), *recolor(box.b, YELLOW), *flash([box.b]), run_time=1.2)

            c.wait_until("lefthand")
            hl = SurroundingRectangle(box.lq, color=YELLOW, buff=0.1).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12)
            hl.set_z_index(-1)
            lsk = chord_sketch("left").next_to(box.border, DOWN, buff=0.15).set_x(box.lq.get_x())
            self.play(*recolor(box.b, FG), FadeIn(hl), run_time=1.0)
            self.play(*appear(lsk, shift=None), run_time=1.2)
            c.wait_until("righthand")
            rsk = chord_sketch("right").next_to(box.border, DOWN, buff=0.15).set_x(box.rq.get_x())
            hr = SurroundingRectangle(box.rq, color=YELLOW, buff=0.1).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12)
            hr.set_z_index(-1)
            self.play(Transform(hl, hr), *appear(rsk, shift=None), run_time=1.3)
            self.hl, self.lsk, self.rsk = hl, lsk, rsk

    # ---------------------------------------------------------------- c3
    def run_mod(self):
        with self.say("c1.diff.3") as c:
            box = self.box
            pair = thumbs()
            v, step = pair
            sc = BOX_SMALL_SC
            self.play(*during(disappear(self.hand, self.dmath, self.tail, self.hl, self.lsk, self.rsk), 0, 0.35),
                      *during([box.animate.scale(sc).move_to([0, BOX_SMALL_TOP - sc * box.height / 2, 0])], 0.3, 0.75),
                      *during(appear(v, step, shift=None, lag=0.2), 0.55, 1.0),
                      run_time=min(2.4, c.until("its continuous")))
            self.v, self.step = v, step

            # (a) for the V; the step waits, dimmed
            xl_v = v.get_left()[0] - 0.1
            va = row(r"\text{(a) continuous}", xl_v, ROW_A)
            vtick = check_mark().scale(0.8).next_to(va, RIGHT, buff=0.3)
            c.wait_until("its continuous")
            self.play(*appear(va), *set_alpha([step], 0.3), run_time=1.0)
            c.wait_until("first test passes")
            self.play(*appear(vtick, shift=None), run_time=0.8)

            # {modsides}: the two chords, then the row
            c.wait_until("modsides")
            ax = v.ax
            hh = 1.5
            chords = VGroup(Line(ax.c2p(-hh, hh), ax.c2p(0, 0)), Line(ax.c2p(0, 0), ax.c2p(hh, hh))).set_stroke(TEAL, 7)
            cdots = VGroup(*[Dot(ax.c2p(x, hh), radius=0.07, color=TEAL) for x in (-hh, hh)])
            vb = row(r"\text{(b) left } {-1}\text{, right } {+1}", xl_v, ROW_B)
            self.play(Create(chords[0]), FadeIn(cdots[0]), run_time=1.0)
            self.play(Create(chords[1]), FadeIn(cdots[1]), *appear(vb), run_time=1.2)

            c.wait_until("modfail")
            vne = row(r"-1 \neq +1", xl_v + 0.6, ROW_C, color=RED)
            vcross = cross_mark().next_to(vne, RIGHT, buff=0.35)
            self.play(*appear(vne), run_time=1.0)
            self.play(*appear(vcross, shift=None), run_time=0.8)
            self.vcol = [v, va, vtick, chords, cdots, vb, vne, vcross]

    # ---------------------------------------------------------------- c4
    def run_step(self):
        with self.say("c1.diff.4") as c:
            step = self.step
            sx = step.ax
            self.play(*set_alpha(self.vcol, 0.3), *set_alpha([step], 1), run_time=1.2)

            s_lo = T("slope 0", 30, color=GREEN).move_to(sx.c2p(-1.45, 0) + 0.3 * UP)
            s_hi = T("slope 0", 30, color=GREEN).move_to(sx.c2p(1.45, 1) + 0.3 * UP)
            c.wait_until(own_word=s_lo)
            self.play(*appear(s_lo, s_hi, lag=0.3), run_time=1.2)

            xl_s = step.get_left()[0] - 0.1
            sbp = row(r"\text{(b)}", xl_s, ROW_B)
            q00 = MathTex(r"0 = 0\,?", font_size=34, color=YELLOW).next_to(sbp, RIGHT, buff=0.25)
            c.wait_until("seem to agree")
            self.play(*appear(sbp, q00), run_time=1.0)

            c.wait_until("jump")
            self.play(FlashAround(step.jump, color=RED, run_time=1.5, time_width=1.5), run_time=1.5)
            sa = row(r"\text{(a) not continuous}", xl_s, ROW_A)
            scross = cross_mark().next_to(sa, RIGHT, buff=0.3)
            c.wait_until("not continuous")
            self.play(*appear(sa, shift=None), run_time=1.0)
            self.play(*appear(scross, shift=None), run_time=0.8)

            c.wait_until("blow")
            left = MathTex(r"\text{left: } 1/", "h", r"\to \infty", font_size=34, color=RED)
            left[1].set_color(TEAL)
            right = MathTex(r"\text{right: } 0", font_size=34)
            left.next_to(sbp, RIGHT, buff=0.25)
            right.move_to([0, ROW_C, 0]).align_to(left, LEFT)
            self.play(*swap(q00, VGroup(left, right)), run_time=min(1.6, c.until()))
            self.scol = [step, s_lo, s_hi, sbp, left, right, sa, scross]

    # ---------------------------------------------------------------- c5
    def implies(self):
        with self.say("c1.diff.5") as c:
            line = MathTex(r"\text{If } f' \text{ exists, then } \Delta f \to 0 \text{ as }", r"\Delta x",
                           r"\to 0 \;\Rightarrow\; f \text{ is continuous.}", font_size=40)
            line[1].set_color(TEAL)
            line.move_to(2.75 * UP)
            r1 = hmath(r"f(x+h) - f(x) =", 42)
            r2 = hmath(r"h \cdot \frac{f(x+h) - f(x)}{h}", 42)
            r3 = MathTex(r"\to\; 0 \cdot f'(x) = 0", font_size=42)
            reason = VGroup(r1, r2, r3).arrange(RIGHT, buff=0.2).move_to(1.45 * UP)
            # the box and the thumbnails clear; the notes' line takes the top
            c.wait_until("if the derivative exists")
            self.play(*during(disappear(self.box, *self.vcol, *self.scol), 0, 0.45),
                      *during(appear(line, shift=None), 0.5, 1.0),
                      run_time=1.6)
            c.wait_until("the change in f")
            self.play(*appear(reason, shift=None), run_time=1.5)
            c.wait_until("so it goes to zero")
            self.play(*flash([r3], color=GREEN), run_time=1.5)

            c.wait_until("cont")
            cont = MathTex(r"\text{differentiable} \;\Rightarrow\; \text{continuous}", font_size=40, color=GREEN)
            cont.move_to([-3.4, -0.2, 0])
            self.play(*appear(cont), run_time=1.0)
            c.wait_until("converse")
            conv = MathTex(r"\text{continuous} \;\not\Rightarrow\; \text{differentiable}", font_size=40, color=RED)
            conv.move_to([0, -1.1, 0]).align_to(cont, LEFT)
            vthumb = thumbs()[0].scale(0.9).move_to([3.6, -0.65, 0])
            self.play(*appear(conv), run_time=1.0)
            c.wait_until("mod ex shows it")
            self.play(*appear(vthumb, shift=None), run_time=1.0)

            # {finite}: Example 40's circle, centre (1, 0), radius 3
            c.wait_until("finite")
            u = 0.65
            ctr = np.array([3.2, -0.6, 0])
            P = lambda x, y: ctr + u * np.array([x - 1, y, 0])  # noqa: E731
            xaxis = Line(P(-2.8, 0), P(4.8, 0)).set_stroke(DIM, 2)
            circ = Circle(radius=3 * u).set_stroke(BLUE, 4).move_to(P(1, 0))
            t_m2 = MathTex("-2", font_size=30, color=DIM).next_to(P(-2, 0), DL, buff=0.1)
            t_4 = MathTex("4", font_size=30, color=DIM).next_to(P(4, 0), DR, buff=0.1)
            self.play(*during(disappear(line, reason, vthumb), 0, 0.4),
                      *during([cont.animate.shift(2.8 * UP), conv.animate.shift(2.8 * UP)], 0.4, 0.8),
                      *during(appear(xaxis, circ, t_m2, t_4, shift=None), 0.6, 1.0),
                      run_time=1.8)

            c.wait_until("vertical")
            tl = Line(P(-2, -3.4), P(-2, 3.4)).set_stroke(RED, 4)
            tr = Line(P(4, -3.4), P(4, 3.4)).set_stroke(RED, 4)
            self.play(Create(tl), Create(tr), run_time=1.2)
            lab_l = T("slope: infinite", 30, color=RED).next_to(tl, UP, buff=0.12)
            lab_r = T("slope: infinite", 30, color=RED).next_to(tr, DOWN, buff=0.12)
            c.wait_until(own_word=lab_l)
            self.play(*appear(lab_l, lab_r, lag=0.3), run_time=1.2)

            c.wait_until("circle")
            part = T("Part 3", 30, color=DIM).next_to(circ, DOWN, buff=0.15).shift(0.4 * LEFT)
            self.play(*appear(part), run_time=1.0)
        self.wait(1.2)
