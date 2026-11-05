"""Chapter 4, scene 2: the fundamental theorem of algebra, by peeling roots. Clips c4.fta.1 – c4.fta.4."""
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

CORNER_SCALE = 0.55
CHAIN_SIZE = 44


# ---------------------------------------------------------------- shared builders (s6, s7 reuse)
def peel_chain(size=CHAIN_SIZE):
    """The peeling chain: three lines (and a gap of vertical dots), GREEN brackets.
    .lines = [l1, l2, l3]; .dots; l1 = P=, (z-z1), Q;  l2 = P=, (z-z1), (z-z2), R;
    l3 = P=, a_n, (z-z1), (z-z2), cdots, (z-zn)."""
    l1 = MathTex(r"P(z) =", r"(z - z_1)", r"\,Q(z)", font_size=size)
    l2 = MathTex(r"P(z) =", r"(z - z_1)", r"(z - z_2)", r"\,R(z)", font_size=size)
    l3 = MathTex(r"P(z) =", r"a_n", r"(z - z_1)", r"(z - z_2)", r"\cdots", r"(z - z_n)", font_size=size)
    for part in (l1[1], l2[1], l2[2], l3[2], l3[3], l3[5]):
        part.set_color(GREEN)
    dots = MathTex(r"\vdots", font_size=size)
    g = VGroup(l1, l2, dots, l3).arrange(DOWN, buff=0.62, aligned_edge=LEFT)
    dots.move_to([l1[1].get_x(), dots.get_y(), 0])
    g.move_to(ORIGIN)
    g.lines, g.dots = [l1, l2, l3], dots
    return g


def peel_labels(chain):
    """The DIM degree labels under Q, R and a_n, and the GREEN brace under the n brackets."""
    l1, l2, l3 = chain.lines
    d1 = MathTex(r"\text{degree } n-1", font_size=30, color=DIM).next_to(l1[2], RIGHT, buff=0.45)
    d2 = MathTex(r"\text{degree } n-2", font_size=30, color=DIM).next_to(l2[3], RIGHT, buff=0.45)
    d1.align_to(l1[2], DOWN)
    d2.align_to(l2[3], DOWN)
    d0 = MathTex(r"\text{degree } 0", font_size=30, color=DIM).next_to(l3[1], DOWN, buff=0.12)
    d0.align_to(l3[1], RIGHT)
    br = span_brace(l3[2].get_corner(DL), l3[5].get_corner(DR), color=GREEN, buff=0.12)
    bl = T("n factors, n roots", 30, GREEN, t2s={"n": ITALIC}).next_to(br, DOWN, buff=0.1)
    return d1, d2, d0, br, bl


def not_poly_tag(target, size=32):
    """RED underline under `target` (the \\cos z of the question) with "not a polynomial" below."""
    line = underline(target, RED, buff=0.12)
    lab = T("not a polynomial", size, RED).next_to(line, DOWN, buff=0.15)
    g = VGroup(line, lab)
    g.line, g.label = line, lab
    return g


def argand_plane(center=ORIGIN, unit=1.0, extent=1.5):
    """L10's running Argand plane (faint grid, Re/Im axes), unit circle BLUE here."""
    center = np.array(center, dtype=float)
    step = unit / 2
    n = int(extent // step)
    grid = VGroup()
    for k in range(-n, n + 1):
        if k == 0:
            continue
        grid.add(Line(center + [k * step, -extent, 0], center + [k * step, extent, 0]))
        grid.add(Line(center + [-extent, k * step, 0], center + [extent, k * step, 0]))
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow(center + [-extent, 0, 0], center + [extent, 0, 0], **ax_kw).set_opacity(0.7)
    y_ax = Arrow(center + [0, -extent, 0], center + [0, extent, 0], **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}", font_size=30, color=DIM).next_to(x_ax.get_end(), DOWN, buff=0.15).shift(0.25 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=30, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    circle = Circle(radius=unit, color=BLUE, stroke_width=3).move_to(center)
    g = VGroup(grid, x_ax, y_ax, circle, re, im)
    g.grid, g.axes, g.circle = grid, VGroup(x_ax, y_ax), circle
    return g


def poly_line(size=44):
    return MathTex(r"P(z) \equiv a_0 + a_1 z + a_2 z^2 + \cdots + a_{n-1} z^{n-1} + ", r"a_n z^n",
                   font_size=size)


def roots_row(size=44, tsize=36):
    eq = MathTex(r"P(z) = 0", font_size=size)
    txt = T("has n (complex) roots", tsize, t2c={"n": GREEN, "roots": GREEN}, t2s={"n": ITALIC})
    row = VGroup(eq, txt).arrange(RIGHT, buff=0.3)
    txt.align_to(eq, DOWN)
    return row


class FTA(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c4.fta.1: the theorem as the notes state it
    def clip1(self):
        shot = load_scene("ch4_s1_hook").handover_shot()
        self.add(shot)
        q = self.q = shot.q
        with self.say("c4.fta.1") as c:
            qm = T("?", 40, YELLOW)
            target = q.copy().scale(CORNER_SCALE)
            VGroup(target, qm).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.6)
            self.qm = qm
            q.generate_target()
            q.target.scale(CORNER_SCALE).move_to(target)
            self.play(*during(disappear(shot.sub, shot.many), 0, 0.4),
                      *during([MoveToTarget(q)], 0.3, 1.0),
                      *during(appear(qm, shift=None), 0.75, 1.0), run_time=1.6)
            self.remove(shot)
            self.add(q, qm)
            head = self.head = MathTex(r"2.7\ \text{Fundamental theorem of algebra}", font_size=44)
            head.to_corner(UL, buff=0.6)
            tag = self.tag = T("end of Chapter 2 of the notes", 28, DIM).next_to(head, DOWN, buff=0.2,
                                                                                aligned_edge=LEFT)
            self.play(*appear(head, tag, lag=0.4), run_time=1.4)  # early: a section heading, read as a whole

            c.wait_until("poly")
            poly = self.poly = poly_line().move_to([0, 1.75, 0])
            deg = self.deg = MathTex(r"\text{degree } n \geq 1", font_size=32).next_to(poly, DOWN, buff=0.22)
            self.play(*appear(poly), run_time=1.5)
            c.wait_until("degree")
            self.play(*appear(deg), run_time=1.0)

            c.wait_until("coeffs")
            co = MathTex(r"a_0, \ldots, a_n \in \mathbb{C}", font_size=40)
            ann = MathTex(r"a_n \neq 0", font_size=40, color=YELLOW)
            VGroup(co, ann).arrange(RIGHT, buff=1.4).move_to([0, 0.3, 0])
            self.co, self.ann = co, ann
            self.play(*appear(co), run_time=1.2)
            c.wait_until("leading")
            box = self.box = token_box(poly[1], poly, height=0.75)
            self.play(FadeIn(box), run_time=0.9)
            self.play(*appear(ann), run_time=1.0)

            c.wait_until("roots")
            rr = self.rr = roots_row().move_to([0, -0.8, 0])
            poss = self.poss = T("(possibly repeated)", 30, DIM).next_to(rr, DOWN, buff=0.15)
            self.play(*appear(rr), run_time=1.5)
            c.wait_until("repeated")
            self.play(*appear(poss), run_time=min(1.0, c.until("fundamental")))
            c.wait_until("fundamental")
            self.play(FlashAround(head, time_width=1.5), run_time=min(1.6, c.until()))

    # ---- c4.fta.2: one root is enough, peel it off
    def clip2(self):
        with self.say("c4.fta.2") as c:
            self.play(*set_alpha([self.poly, self.deg, self.co, self.ann, self.box], 0.4), run_time=1.0)
            c.wait_until("one")
            weak = self.weak = T("every polynomial equation has at least one complex root", 32,
                                 t2c={"at least one": YELLOW}).move_to([0, -2.85, 0])
            self.play(*appear(weak), run_time=1.2)
            ud = MathTex(r"\Updownarrow", font_size=48, color=YELLOW)
            ud.move_to([0, (self.poss.get_bottom()[1] + weak.get_top()[1]) / 2, 0])
            self.play(GrowFromCenter(ud), run_time=1.0)

            # peel: clear the statement, keep the weak form on top
            c.wait_until("peel")
            self.play(*during(disappear(self.poly, self.deg, self.co, self.ann, self.box,
                                        self.rr, self.poss, ud, self.tag), 0, 0.45),
                      *during([weak.animate.scale(0.85).move_to([0, 2.45, 0]).set_opacity(0.7)], 0.45, 1.0),
                      run_time=1.6)
            ch = self.chain = peel_chain().move_to([0, -0.45, 0])
            d1, d2, d0, br, bl = self.labels = peel_labels(ch)
            l1, l2, l3 = ch.lines
            c.wait_until("Then")
            self.play(*appear(l1), run_time=1.5)
            c.wait_until("degree")
            self.play(*appear(d1), run_time=1.0)

            c.wait_until("again")
            derive(self, l1, l2, run_time=2.0)
            self.play(*appear(d2), run_time=1.0)  # early: names R's degree; the voice says 'degree' next line

            c.wait_until("down")
            derive(self, l2, l3, run_time=2.0)
            self.play(*appear(ch.dots, shift=None), run_time=0.8)
            c.wait_until("leading")
            self.play(*appear(d0), run_time=1.0)

            c.wait_until("count")
            self.play(GrowFromCenter(br), run_time=1.0)
            self.play(*appear(bl), run_time=1.0)

    # ---- c4.fta.3: z^3 - 1
    def clip3(self):
        ch = self.chain
        d1, d2, d0, br, bl = self.labels
        allc = VGroup(*ch.lines, ch.dots, br)
        settle(self, allc)
        self.allc = allc
        with self.say("c4.fta.3") as c:
            allc.generate_target()
            allc.target.scale(0.66).set_opacity(0.45)
            allc.target.move_to([-6.6 + allc.target.width / 2, 0.7, 0])
            bl.generate_target()
            bl.target.set_opacity(0.6).next_to(allc.target[-1], DOWN, buff=0.12)
            self.play(*during(disappear(self.weak, d1, d2, d0), 0, 0.45),
                      *during([MoveToTarget(allc), MoveToTarget(bl)], 0.3, 1.0), run_time=1.6)
            settle(self, allc, add=[bl])

            X = 2.5
            ex = MathTex(r"z^3 - 1", font_size=48).move_to([X, 2.05, 0])
            c.wait_until("Take")
            self.play(*appear(ex), run_time=1.0)

            c.wait_until("root1")
            r1 = MathTex(r"z = 1", font_size=40, color=GREEN)
            r23 = MathTex(r"z = -\tfrac{1}{2} \pm \tfrac{\sqrt{3}}{2}\,", r"i", font_size=40)
            r23[1].set_color(PINK)
            VGroup(r1, r23).arrange(RIGHT, buff=1.0).move_to([X, 0.95, 0])
            self.play(*appear(r1), run_time=1.0)

            c.wait_until("factor")
            fac = MathTex(r"z^3 - 1", r"=", r"(z - 1)", r"(z^2 + z + 1)", font_size=48).move_to([X, 2.05, 0])
            fac[2].set_color(GREEN)
            self.play(*edit(ex, fac), run_time=1.6)
            c.wait_until("two complex")
            self.play(*appear(r23), run_time=1.2)

            c.wait_until("circle")
            P = np.array([4.0, -1.85, 0])
            u = 1.05
            ap = argand_plane(P, u, 1.5)
            self.play(*appear(ap, shift=None), run_time=1.0)
            dots = [Dot(P + u * np.array([np.cos(a), np.sin(a), 0]), radius=0.11, color=GREEN)
                    for a in (0, 2 * PI / 3, 4 * PI / 3)]
            c.wait_until("evenly")
            self.play(*appear(*dots, shift=None, lag=0.35), run_time=1.5)
            self.ex_stuff = [fac, r1, r23, ap, *dots]

            c.wait_until("three")
            three = T("degree 3: 3 roots", 34, t2c={"3 roots": GREEN}).move_to([0.6, -1.85, 0])
            self.play(*appear(three), run_time=1.0)
            self.ex_stuff.append(three)

    # ---- c4.fta.4: history, then back to cos z = 2
    def clip4(self):
        allc = self.allc
        with self.say("c4.fta.4") as c:
            note = T("not a formal proof", 32, DIM, slant=ITALIC)
            note.next_to(allc, DOWN, buff=0.35).align_to(allc, LEFT)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("hard part")
            l1 = self.chain.lines[0]
            self.play(*disappear(*self.ex_stuff), *set_alpha([allc], 1.0), run_time=1.0)
            self.play(FlashAround(l1[1], run_time=1.5, time_width=1.5, color=YELLOW))

            # the theorem card and its history strip
            poly = poly_line(40)
            rr = roots_row(40, 34)
            card_in = VGroup(poly, rr).arrange(DOWN, buff=0.3)
            frame = SurroundingRectangle(card_in, color=DIM, buff=0.25, corner_radius=0.15).set_stroke(width=2)
            card = VGroup(frame, card_in).move_to([0, 1.65, 0])
            c.wait_until("roth")
            sweep_clear(self, *appear(card, shift=None), keep=[self.head, self.q, self.qm], run_time=1.4)

            roth = T("Roth 1608", 30, t2c={"1608": GOLD})
            gauss = VGroup(T("Gauss 1799", 30, t2c={"1799": GOLD}),
                           MathTex(r"(a_j \in \mathbb{R})", font_size=32)).arrange(RIGHT, buff=0.15)
            argand = VGroup(T("Argand 1806", 30, t2c={"1806": GOLD}),
                            MathTex(r"(a_j \in \mathbb{C},\ \text{first complete proof})", font_size=32)
                            ).arrange(RIGHT, buff=0.15)
            strip = VGroup(roth, gauss, argand).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            strip.next_to(card, DOWN, buff=0.4)
            for row in (gauss, argand):
                row[0].align_to(row[1], DOWN).shift(0.04 * UP)
            self.play(*appear(roth), run_time=1.0)
            c.wait_until("gauss")
            self.play(*appear(gauss), run_time=1.0)
            c.wait_until("argand")
            self.play(*appear(argand), run_time=1.2)

            # cos z = 2 comes back from the corner
            c.wait_until("bridge")
            q, qm = self.q, self.qm
            back = q.copy().scale(1 / CORNER_SCALE)
            qm2 = qm.copy().scale(1.4)
            VGroup(back, qm2).arrange(RIGHT, buff=0.2).move_to([0, -2.35, 0])
            self.play(*during(disappear(q, qm), 0, 0.45),
                      *during(appear(back, qm2, shift=0.2 * UP, lag=0.15), 0.5, 1.0), run_time=1.6)
            q, qm = self.q, self.qm = back, qm2
            tag = not_poly_tag(q[0][0:4])
            c.wait_until(own_word=tag.label)
            self.play(GrowFromCenter(tag.line), *appear(tag.label), run_time=1.0)

            c.wait_until("promise")
            self.play(*set_alpha([card, strip], DIMMED), run_time=1.2)
            c.wait_until("look")
            self.play(FlashAround(q, run_time=1.5, time_width=1.5))
