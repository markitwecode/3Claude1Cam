"""Chapter 2, scene 2: De Moivre's theorem, derived and pictured. Clips c2.thm.1 – c2.thm.5."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# The Argand plane: origin on screen, unit length, half-extent of the axes.
O = np.array([-3.3, -0.2, 0.0])
U = 1.9            # unit circle radius on screen
U_ZOOM = 0.95      # unit after zooming out for r^4 (clip 4)
EXT = 3.0
THETA = 25         # degrees
COL_X = 3.6        # centre of the right-hand column
EQ_X = 1.3         # x of the aligned "=" in the derivation chain


def argand_plane(center=O, unit=U, extent=EXT):
    """PLAN.md's running Argand plane: faint grid, Re/Im axes, DIM unit circle."""
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
    re = MathTex(r"\mathrm{Re}", font_size=34, color=DIM).next_to(x_ax.get_end(), DOWN, buff=0.15).shift(0.25 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    circle = Circle(radius=unit, color=DIM, stroke_width=2.5).move_to(center)
    g = VGroup(grid, x_ax, y_ax, circle, re, im)
    g.grid, g.axes, g.circle = grid, VGroup(x_ax, y_ax), circle
    return g


def ray(deg, color=GOLD, r=1.0, center=O, unit=U):
    """An arrow from the origin at angle deg, of modulus r."""
    a = np.deg2rad(deg)
    end = center + unit * r * np.array([np.cos(a), np.sin(a), 0])
    return Arrow(center, end, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.14,
                 tip_length=0.28, color=color)


def theta_arc(k, color=YELLOW, center=O, radius=0.6, step=THETA):
    """The arc from k·θ to (k+1)·θ (k may be negative for clockwise)."""
    return Arc(radius=radius, start_angle=np.deg2rad(k * step), angle=np.deg2rad(step),
               arc_center=center, color=color, stroke_width=4)


def theta_label(center=O):
    a = np.deg2rad(THETA / 2)
    return MathTex(r"\theta", font_size=38, color=YELLOW).move_to(center + 0.92 * np.array([np.cos(a), np.sin(a), 0]))


def power_steps(n=4, center=O, unit=U, dim=0.4):
    """The arrows e^{iθ}, e^{2iθ} … e^{inθ} with a YELLOW θ-arc per step, as clip 3 leaves them:
    earlier arrows dimmed, the last bright. Returns VGroup(arrows, arcs, θ label); .arrows .arcs .label."""
    arrows = VGroup(*[ray(THETA * (k + 1), center=center, unit=unit) for k in range(n)])
    for a in arrows[:-1]:
        a.set_opacity(dim)
    arcs = VGroup(*[theta_arc(k, center=center) for k in range(n)])
    lab = theta_label(center)
    g = VGroup(arrows, arcs, lab)
    g.arrows, g.arcs, g.label = arrows, arcs, lab
    return g


def put(m, eq, side, buff=0.18):
    """Place m beside the '=' eq, its first glyph centred on the '=' line."""
    m.next_to(eq, side, buff=buff)
    m.shift(UP * (eq.get_center()[1] - m[0][0].get_center()[1]))
    return m


def color_parts(m, colors):
    for i, c in colors.items():
        m[i].set_color(c)
    return m


class Theorem(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- the number and its power
    def clip1(self):
        with self.say("c2.thm.1") as c:
            plane = argand_plane()
            self.plane = plane
            self.play(FadeIn(plane), run_time=0.9)  # early: axis labels belong to the plane
            a1 = ray(THETA)
            self.a1 = a1
            self.play(GrowArrow(a1), run_time=min(1.2, c.until("angle theta")))
            arc, lab = theta_arc(0), theta_label()
            self.arc1, self.th1 = arc, lab
            c.wait_until("angle theta")
            self.play(Create(arc), FadeIn(lab, shift=0.15 * DOWN), run_time=0.9)

            # {euler}: z = cos θ + i sin θ, then = e^{iθ}
            c.wait_until("euler")
            r1a = MathTex("z", "=", r"\cos\theta", "+", r"i\sin\theta", font_size=44)
            color_parts(r1a, {2: BLUE, 4: PINK})
            r1b = MathTex("=", r"e^{i\theta}", font_size=44)
            r1b[1].set_color(GOLD)
            r1b.next_to(r1a, RIGHT, buff=0.2)
            r1b.shift(UP * (r1a[1].get_center()[1] - r1b[0].get_center()[1]))
            ref = T("(71)", 28, DIM)
            row1 = VGroup(r1a, r1b)
            row1.move_to([COL_X - 0.4, 2.6, 0])
            ref.next_to(row1, RIGHT, buff=0.35)
            self.play(*appear(r1a), run_time=1.0)
            c.wait_until("euler's formula")
            self.play(*appear(r1b, ref, lag=0.4), run_time=1.2)
            self.row1, self.ref = row1, ref

            # {power}: z^n = (cos θ + i sin θ)^n
            c.wait_until("power")
            eq2 = MathTex("=", font_size=44).move_to([EQ_X, 1.5, 0])
            zn = put(MathTex("z^{n}", font_size=44), eq2, LEFT)
            rhs2 = MathTex("(", r"\cos\theta", "+", r"i\sin\theta", ")", "^{n}", font_size=44)
            color_parts(rhs2, {1: BLUE, 3: PINK})
            put(rhs2, eq2, RIGHT)
            self.play(*appear(VGroup(zn, eq2), rhs2, lag=0.3), run_time=1.4)
            self.zn, self.eq2, self.rhs2 = zn, eq2, rhs2

            # {note}: the outer n is the power
            c.wait_until("note")
            tag = T("n: the power\n(not the turn count)", 28, YELLOW, t2s={"n:": ITALIC})
            tag.move_to([0, 0, 0]).align_to(np.array([6.55, 0, 0]), RIGHT).align_to(np.array([0, 0.85, 0]), UP)
            npow = rhs2[5]
            tag_arrow = Arrow(tag.get_top() + 0.6 * RIGHT + 0.05 * UP, npow.get_corner(DR) + 0.05 * RIGHT,
                              buff=0.06, stroke_width=3, tip_length=0.16, color=YELLOW)
            self.play(*recolor(npow, YELLOW), GrowArrow(tag_arrow), *appear(tag), run_time=1.2)
            self.tag = VGroup(tag, tag_arrow)

    # ---------------------------------------------------------------- the chain and the box
    def clip2(self):
        with self.say("c2.thm.2") as c:
            # {rule}: = (e^{iθ})^n
            eq3 = MathTex("=", font_size=44).move_to([EQ_X, 0.4, 0])
            rhs3 = MathTex("(", r"e^{i\theta}", ")", "^{n}", font_size=44)
            color_parts(rhs3, {1: GOLD, 3: YELLOW})
            put(rhs3, eq3, RIGHT)
            c.wait_until("multiply")
            self.play(*during(disappear(self.tag), 0, 0.45),
                      *during(appear(eq3, rhs3, lag=0.2), 0.5, 1), run_time=1.6)

            # {chain}: = e^{inθ}, the outer n sliding into the exponent
            c.wait_until("chain")
            eq4 = MathTex("=", font_size=44).move_to([EQ_X, -0.7, 0])
            rhs4 = MathTex(r"e^{in\theta}", font_size=44, color=GOLD)
            rhs4[0][2].set_color(YELLOW)
            put(rhs4, eq4, RIGHT)
            g = rhs4[0]
            self.play(*appear(eq4), *fly(rhs3[3], g[2], arc=1.6), run_time=1.6)
            self.play(FadeIn(g[0]), FadeIn(g[1]), FadeIn(g[3]), run_time=min(1.0, c.until("and by")))
            settle(self, rhs4)

            # {back}: = cos nθ + i sin nθ
            c.wait_until("back")
            eq5 = MathTex("=", font_size=44).move_to([EQ_X, -1.8, 0])
            rhs5 = MathTex(r"\cos n\theta", "+", r"i\sin n\theta", font_size=44)
            color_parts(rhs5, {0: BLUE, 2: PINK})
            put(rhs5, eq5, RIGHT)
            c.wait_until("cosine")
            self.play(*appear(eq5, rhs5, lag=0.3), run_time=1.4)

            # {box}: first = last, boxed
            c.wait_until("box")
            self.play(*[FadeOut(m) for m in (self.plane, self.a1, self.arc1, self.th1, self.row1, self.ref,
                                             eq3, rhs3, eq4, rhs4)], run_time=1.0)
            eqb = MathTex("=", font_size=52).move_to([0, -0.5, 0])
            lhs = MathTex(r"\cos n\theta", "+", r"i\sin n\theta", font_size=52)
            color_parts(lhs, {0: BLUE, 2: PINK})
            rhs = MathTex("(", r"\cos\theta", "+", r"i\sin\theta", ")", "^{n}", font_size=52)
            color_parts(rhs, {1: BLUE, 3: PINK})
            put(lhs, eqb, LEFT, buff=0.25)
            put(rhs, eqb, RIGHT, buff=0.25)
            body = VGroup(lhs, eqb, rhs)
            body.shift(-body.get_center()[0] * RIGHT)
            rect = SurroundingRectangle(body, color=YELLOW, buff=0.4, stroke_width=3)
            title = T("De Moivre’s theorem", 44).next_to(rect, UP, buff=0.35)
            self.play(*during(disappear(self.zn, self.eq2, eq5), 0, 0.35),
                      *during([ReplacementTransform(rhs5, lhs), ReplacementTransform(self.rhs2, rhs)], 0.25, 1),
                      run_time=1.6)
            self.play(FadeIn(eqb), FadeIn(rect), *appear(title), run_time=1.0)
            self.boxg = VGroup(title, rect, lhs, eqb, rhs)
            self.lhs, self.rhsb, self.body = lhs, rhs, body

            # {read}: each side lights up as it is read
            c.wait_until("read")
            # each box centred on its own side, tall enough that the superscript n sits well inside
            hl_h = rhs.height + 0.4
            hl = token_box(lhs, lhs, pad=0.45, height=hl_h)
            self.play(FadeIn(hl), run_time=0.6)
            c.wait_until("equals")
            self.play(Transform(hl, token_box(rhs, rhs, pad=0.45, height=hl_h)), run_time=1.0)
            c.wait_until("all to the power")
            self.play(FadeOut(hl), run_time=min(1.0, c.until()))

    # ---------------------------------------------------------------- the picture
    def clip3(self):
        with self.say("c2.thm.3") as c:
            # {picture}: box to the top right, the plane back
            self.remove(*self.boxg)
            self.add(self.boxg)
            plane = argand_plane()
            a1 = ray(THETA)
            arc, lab = theta_arc(0), theta_label()
            self.play(self.boxg.animate.scale(0.66).move_to([3.55, 2.95, 0]),
                      *during(appear(plane, a1, lag=0.3), 0.3, 1), run_time=1.6)  # early: axis labels belong to the plane
            self.play(Create(arc), FadeIn(lab), run_time=0.8)
            self.plane, self.a1, self.arc1, self.th1 = plane, a1, arc, lab

            # {lengths}
            rule = T("× : lengths multiply, angles add", 30)
            rule.move_to([COL_X, 1.45, 0])
            c.wait_until(own_word=rule)
            self.play(*appear(rule), run_time=1.0)
            self.rule = rule

            # {two} {three} {four}: the arrow steps round, one θ-arc per step
            arrows, arcs = [a1], [arc]
            for k, (cue, rt) in enumerate((("two", 1.8), ("three", 1.3), ("four", 1.1)), start=1):
                c.wait_until(cue)
                new = arrows[-1].copy()
                arc_k = theta_arc(k)
                self.play(Rotate(new, angle=np.deg2rad(THETA), about_point=O), Create(arc_k),
                          *set_alpha([arrows[-1]], 0.4), run_time=rt)
                arrows.append(new)
                arcs.append(arc_k)
            self.arrows, self.arcs = arrows, arcs

            # {length}: tips stay on the unit circle; 1 × 1 × 1 × 1 = 1
            c.wait_until("length")
            c.wait_until("its length")
            ring = plane.circle.copy().set_stroke(GOLD, 5)
            self.play(VShowPassingFlash(ring, time_width=0.6), run_time=1.6)
            ones = MathTex(r"1 \times 1 \times 1 \times 1 = 1", font_size=44, color=GOLD).move_to([COL_X, 0.4, 0])
            c.wait_until("one times one")
            self.play(*appear(ones), run_time=1.0)
            self.ones = ones

    # ---------------------------------------------------------------- "rather trivial", and modulus r
    def clip4(self):
        with self.say("c2.thm.4") as c:
            quote = T("“the proof is\nrather trivial”", 36, slant=ITALIC)
            who = T("the lecturer, 00:08:01", 28, DIM)
            card = VGroup(quote, who).arrange(DOWN, buff=0.25).move_to([COL_X, -1.5, 0])
            c.wait_until(own_word=quote)
            self.play(*appear(quote, who, lag=0.4), run_time=1.2)

            # {general}: keep the unit arrows θ and 4θ only, zooming out (unit halves) to make room for r^4
            c.wait_until("general")
            a1, a2, a3, a4 = self.arrows
            circ_s = Circle(radius=U_ZOOM, color=DIM, stroke_width=2.5).move_to(O)
            self.play(*during(disappear(a2, a3, *self.arcs, self.th1), 0, 0.5),
                      *during([Transform(self.plane.circle, circ_s),
                               Transform(a1, ray(THETA, unit=U_ZOOM)),
                               Transform(a4, ray(4 * THETA, unit=U_ZOOM))], 0.3, 1), run_time=1.6)

            # modulus r: the formula replaces the quote; the unit-only 1 × 1 × 1 × 1 = 1 goes as the r arrow comes in
            c.wait_until("with a modulus")
            form = MathTex(r"(r\,e^{i\theta})^{n}", "=", "r^{n}", r"e^{in\theta}", font_size=44)
            form[2].set_color(GOLD)
            form.move_to([COL_X, -1.5, 0])
            ar = ray(THETA, r=1.3, unit=U_ZOOM)
            self.play(*swap(card, form), GrowArrow(ar), *set_alpha([a1, a4], 0.35), *disappear(self.ones),
                      run_time=1.4)

            # r^4 at 4θ, straight after, so r⁴ ≈ 2.86 stays up longer
            ar4 = ray(4 * THETA, r=1.3 ** 4, unit=U_ZOOM)
            r4 = MathTex(r"r^4 \approx 2.86", font_size=34, color=GOLD)
            r4.next_to(ar4.get_end(), LEFT, buff=0.2)
            set_backstroke(r4)
            self.play(ReplacementTransform(ar.copy(), ar4), *during(appear(r4), 0.5, 1),
                      run_time=min(1.5, c.until()))
            self.ar, self.ar4, self.r4, self.form, self.a4 = ar, ar4, r4, form, a4

    # ---------------------------------------------------------------- n = -1: the mirror
    def clip5(self):
        with self.say("c2.thm.5") as c:
            # {negative}: back to the unit arrow at θ
            a1 = self.a1
            circ = Circle(radius=U, color=DIM, stroke_width=2.5).move_to(O)
            arc, lab = theta_arc(0), theta_label()
            c.wait_until("too")
            self.play(*during(disappear(self.ar, self.ar4, self.r4, self.a4), 0, 0.4),
                      *during([Transform(self.plane.circle, circ), Transform(a1, ray(THETA))], 0.2, 0.8),
                      *during([Create(arc), FadeIn(lab)], 0.7, 1), run_time=1.6)

            # {minus}: n = −1 gives cos θ − i sin θ
            c.wait_until("minus")
            nline = MathTex("n", "=", "-1", font_size=44)
            nline[0].set_color(YELLOW)
            nline.move_to([COL_X, 1.2, 0])
            self.play(*during(disappear(self.rule, self.form), 0, 0.45),
                      *during(appear(nline), 0.5, 1), run_time=1.2)
            conj = MathTex(r"\cos\theta", "-", r"i\sin\theta", font_size=48)
            color_parts(conj, {0: BLUE, 2: PINK})
            conj.move_to([COL_X, -0.1, 0])
            c.wait_until("you get")
            self.play(*appear(conj), run_time=1.2)

            # {mirror}: the arrow turned back by θ
            c.wait_until("mirror")
            pa = ray(-THETA, color=PURPLE)
            parc = theta_arc(-1, color=PURPLE)
            plab = MathTex(r"e^{-i\theta}", font_size=44, color=PURPLE)
            plab.next_to(pa.get_end(), DR, buff=0.12)
            set_backstroke(plab)
            self.play(ReplacementTransform(a1.copy(), pa), Create(parc), run_time=1.6)
            self.play(*appear(plab), run_time=0.9)

            # {conj}: the conjugate
            c.wait_until("conjugate")
            self.play(FlashAround(conj, color=PURPLE), FlashAround(plab, color=PURPLE), run_time=1.5)
