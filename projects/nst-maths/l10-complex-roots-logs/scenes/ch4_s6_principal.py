"""Chapter 4, scene 6: principal values: the box, notation, ln(-1)+ln(-1) vs ln 1, F18. Clips c4.prin.1 – c4.prin.5."""
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


# ---------------------------------------------------------------- Argand plane (copied from ch2_s1_hook)
def argand_plane(O, U, xr=(-2.0, 2.0), yr=(-1.6, 2.5), labels=True, unit=True):
    """Re/Im axes, faint grid, DIM unit circle (ch2_s1_hook's look; origin O, U screen units per unit)."""
    def P(x, y):
        return O + U * np.array([x, y, 0])
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(P(x, yr[0]), P(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(int(np.ceil(yr[0])), int(np.floor(yr[1])) + 1):
        if y:
            grid.add(Line(P(xr[0], y), P(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(P(xr[0], 0), P(xr[1], 0) + 0.2 * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    yax = Arrow(P(0, yr[0]), P(0, yr[1]) + 0.2 * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    g = VGroup(grid, xax, yax)
    if labels:
        g.add(T("Re", size=30).next_to(xax.get_end(), DOWN, buff=0.15))
        g.add(T("Im", size=30).next_to(yax.get_end(), RIGHT, buff=0.15))
    if unit:
        g.add(Circle(radius=U, color=DIM, stroke_width=2).move_to(O))
    return g


# ---------------------------------------------------------------- the angle picture (reused by the recap)
AO = np.array([-2.6, -0.25, 0])   # plane origin on screen
AU = 1.3


def AP(x, y):
    return AO + AU * np.array([x, y, 0])


def _spiral(t0, t1):
    r = lambda t: 0.42 + 0.065 * t  # noqa: E731
    return ParametricFunction(lambda t: AP(r(t) * np.cos(t), r(t) * np.sin(t)),
                              t_range=[t0, t1], color=YELLOW, stroke_width=5)


def pull_back_shot():
    """pi + pi = 2pi on the Argand plane, the GREEN principal range (open at -pi), and the RED
    pull-back by one full turn to 0. Final state of clip c4.prin.4's picture."""
    s = VGroup()
    s.plane = argand_plane(AO, AU, xr=(-1.6, 1.6), yr=(-1.6, 1.6))
    s.m1 = MathTex("-1", font_size=40).next_to(AP(-1, 0), DL, buff=0.08)
    s.p1 = MathTex("1", font_size=40).next_to(AP(1, 0), DR, buff=0.08)
    s.arrow = Arrow(AO, AP(1, 0), buff=0, color=FG, stroke_width=5, max_tip_length_to_length_ratio=0.15)
    s.spiral1 = _spiral(0, PI)
    s.spiral2 = _spiral(PI, TAU)
    s.green = Arc(radius=0.28 * AU, start_angle=-PI + 0.3, angle=TAU - 0.3, arc_center=AO,
                  color=GREEN, stroke_width=6)
    s.open_end = Circle(radius=0.07, color=GREEN, stroke_width=3).set_fill(BG, 1).move_to(s.green.get_start())
    s.closed_end = Dot(s.green.get_end(), radius=0.07, color=GREEN)
    s.red = Arc(radius=1.3 * AU, start_angle=0.12, angle=-(TAU - 0.24), arc_center=AO,
                color=RED, stroke_width=5)
    s.red.add_tip(tip_length=0.25, tip_width=0.25)
    s.red_label = MathTex(r"-2\pi", font_size=40, color=RED).move_to(AP(-1.25, 1.25))
    s.angle_label = MathTex("0", font_size=44, color=GREEN).move_to(AP(0.62, 0.72))
    s.add(s.plane, s.m1, s.p1, s.green, s.open_end, s.closed_end, s.spiral1, s.spiral2,
          s.arrow, s.red, s.red_label, s.angle_label)
    return s


# ---------------------------------------------------------------- the ln 2i ladder (s4's spec, small)
LX0, LY0 = 1.5, -0.4     # w-plane origin on screen (Im axis at x = LX0)
LCOL = 3.6               # x of the column Re w = ln 2
LS = 0.33                # screen units per unit of Im w


def ladder_ln2i():
    L = VGroup()
    L.re_axis = Arrow([LX0 - 0.4, LY0, 0], [6.3, LY0, 0], buff=0, stroke_width=2.5, color=FG,
                      max_tip_length_to_length_ratio=0.03)
    L.im_axis = Arrow([LX0, -3.3, 0], [LX0, 3.55, 0], buff=0, stroke_width=2.5, color=FG,
                      max_tip_length_to_length_ratio=0.03)
    L.line = DashedLine([LCOL, -3.2, 0], [LCOL, 3.4, 0], dash_length=0.12, color=GOLD, stroke_width=3)
    L.ln2 = MathTex(r"\ln 2", font_size=32, color=GOLD).next_to([LCOL, LY0, 0], DR, buff=0.12)
    L.rungs = {}
    for n in (-1, 0, 1):
        L.rungs[n] = Dot([LCOL, LY0 + LS * (PI / 2 + TAU * n), 0], radius=0.08, color=TEAL)
    top, bot = L.rungs[1].get_y(), L.rungs[-1].get_y()
    L.fade = VGroup(*[Dot([LCOL, top + d, 0], radius=0.06, color=TEAL).set_opacity(o)
                      for d, o in ((0.4, 0.55), (0.75, 0.25))],
                    *[Dot([LCOL, bot - d, 0], radius=0.06, color=TEAL).set_opacity(o)
                      for d, o in ((0.4, 0.55), (0.75, 0.25))])
    L.brace = Brace(Line(L.rungs[0].get_center(), L.rungs[1].get_center()), direction=LEFT,
                    buff=0.15, color=TEAL)
    L.brace_label = MathTex(r"2\pi i", font_size=34, color=TEAL).next_to(L.brace, LEFT, buff=0.12)
    L.strip = Rectangle(width=6.3 - LX0 - 0.1, height=LS * TAU, stroke_width=0).set_fill(GREEN, 0.12)
    L.strip.move_to([(LX0 + 6.2) / 2, LY0, 0])
    L.pi = MathTex(r"\pi", font_size=32, color=GREEN).next_to([LX0, LY0 + LS * PI, 0], LEFT, buff=0.12)
    L.mpi = MathTex(r"-\pi", font_size=32, color=GREEN).next_to([LX0, LY0 - LS * PI, 0], LEFT, buff=0.12)
    L.tag = T("principal value", size=30, color=GREEN).next_to(L.rungs[0], RIGHT, buff=0.25)
    L.add(L.strip, L.re_axis, L.im_axis, L.line, L.ln2, *L.rungs.values(), L.fade)
    return L


def mini_plane(center, u=0.95, ext=1.3):
    xax = Arrow(center + u * ext * LEFT, center + u * ext * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.06)
    yax = Arrow(center + u * ext * DOWN, center + u * ext * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.06)
    return VGroup(xax, yax)


BOX_LINES = [
    "Often the principal value of ln z is",
    "defined by choosing just one of these",
    "possible values of θ, and the usual",
    "convention with ln z is to choose",
    "−π < θ ≤ π. For example,",
    "on sheet 1 question 10",
    "note that the principal values in (a)",
    "and (b) differ by (almost) 2πi. This",
    "will be considered further in later",
    "maths courses.",
]


def clear_to(scene, *incoming, keep=(), run_time=1.2):
    """Everything not kept fades out together (first half), incoming arrives in the second half."""
    keep_ids = {id(m) for k in keep for m in k.get_family()}
    out = [FadeOut(m) for m in scene.mobjects if id(m) not in keep_ids]
    scene.play(*during(out, 0, 0.45), *during(list(incoming), 0.5, 1), run_time=run_time)


class Principal(NarratedScene):
    def construct(self):
        # ============================================================ clip 1: the box, the strip
        with self.say("c4.prin.1") as c:
            lines = VGroup(*[T(s, size=28, disable_ligatures=True, t2s={"principal value": ITALIC} if i == 0 else {})
                             for i, s in enumerate(BOX_LINES)])
            lines.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            frame = SurroundingRectangle(lines, color=DIM, buff=0.35, corner_radius=0.12, stroke_width=2)
            box = VGroup(frame, lines)
            box.scale(1.2).move_to([0, 0, 0])
            self.box_lines = lines
            self.play(*appear(box, shift=None), run_time=1.5)  # early: the box is shown whole, then walked
            c.wait_until("choose")
            rng = select(lines[4], "−π < θ ≤ π")[0]
            self.play(*recolor(rng, GREEN), FlashUnder(rng, color=GREEN, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("rung")

            L = ladder_ln2i()
            self.play(box.animate.scale(1 / 1.2).move_to([-3.55, 0, 0]),
                      run_time=min(1.5, c.until("picks out")))
            self.play(*appear(VGroup(L.re_axis, L.im_axis, L.line, L.ln2), shift=None),
                      *appear(*L.rungs.values(), *L.fade, lag=0.1, shift=None),
                      GrowFromCenter(L.brace), FadeIn(L.brace_label), run_time=1.5)
            c.wait_until("inside")
            self.play(FadeIn(L.strip), *appear(L.pi, L.mpi, shift=None),
                      L.rungs[0].animate.set_color(GREEN).scale(1.25), run_time=1.5)
            c.wait_until(own_word=L.tag)
            self.play(*appear(L.tag, shift=0.2 * LEFT), run_time=1.0)

        # ============================================================ clip 2: notation
        with self.say("c4.prin.2") as c:
            self.play(*disappear(box), run_time=1.0)
            c.wait_until("capital")
            Ln = MathTex(r"\mathrm{Ln}\, z", font_size=60).move_to([-3.6, 1.6, 0])
            self.play(*appear(Ln), run_time=1.0)
            strike = Line(Ln.get_corner(DL) + 0.15 * DL, Ln.get_corner(UR) + 0.15 * UR, color=RED, stroke_width=6)
            self.play(Create(strike), run_time=0.8)
            c.wait_until("same")
            whole_brace = Brace(Line([0, L.fade[3].get_y(), 0], [0, L.fade[1].get_y(), 0]), direction=LEFT,
                                color=DIM).move_to([0.75, LY0 + 0.3, 0])
            whole_brace.set_y((L.fade[3].get_y() + L.fade[1].get_y()) / 2)
            ln_all = MathTex(r"\ln z", font_size=48).next_to(whole_brace, LEFT, buff=0.15)
            self.play(GrowFromCenter(whole_brace), *appear(ln_all, shift=0.2 * RIGHT), run_time=1.5)
            ln_one = MathTex(r"\ln z", font_size=40, color=GREEN).next_to(L.tag, UP, buff=0.15, aligned_edge=LEFT)
            c.wait_until("principal value")
            self.play(*appear(ln_one), run_time=1.0)
            c.wait_until("quote")
            quote = T("“please bear with this\nabuse of the notation”", size=36, slant=ITALIC)
            quote.move_to([-3.6, -1.4, 0])
            self.play(*appear(quote), run_time=1.2)
            c.wait_until("tag")
            self.play(FlashAround(VGroup(ln_one, L.tag), color=GREEN, run_time=2, time_width=1.5),
                      run_time=2)

        # ============================================================ clip 3: the box warns; ln(-1)+ln(-1) vs ln 1
        with self.say("c4.prin.3") as c:
            box.move_to([-3.55, 0, 0])
            note = T("an older sheet's numbering", size=28, color=DIM)
            sheet = select(lines[5], "sheet 1 question 10")[0]
            note.next_to(frame, RIGHT, buff=0.7).set_y(lines[5].get_y())
            note_arrow = Arrow(note.get_left() + 0.1 * LEFT, lines[5].get_right() + 0.1 * RIGHT, buff=0.05,
                               color=DIM, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            clear_to(self, FadeIn(box), run_time=1.2)
            self.play(*appear(note, shift=0.2 * LEFT), GrowArrow(note_arrow), run_time=1.0)
            c.wait_until("break")
            diff = select(lines[7], "(almost) 2πi")[0]
            self.play(*recolor(diff, GOLD), FlashUnder(diff, color=GOLD, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("example")

            XL = -6.2
            zz = MathTex(r"z_1 = z_2 = -1", font_size=52).move_to([3.6, 2.6, 0])
            self.play(*appear(zz), run_time=1.2)
            c.wait_until("each")
            zz.generate_target()
            zz.target.move_to([0, 3.0, 0]).align_to([XL, 0, 0], LEFT)
            self.play(*during([FadeOut(box), FadeOut(note), FadeOut(note_arrow)], 0, 0.5),
                      *during([MoveToTarget(zz)], 0.35, 1), run_time=1.4)
            l1 = MathTex(r"\ln(-1) = i\pi", font_size=48).move_to([0, 1.8, 0]).align_to([XL, 0, 0], LEFT)
            l2 = l1.copy().move_to([0, 0.85, 0]).align_to([XL, 0, 0], LEFT)
            t1 = T("principal value", size=30, color=GREEN).next_to(l1, RIGHT, buff=0.45)
            t2 = t1.copy().next_to(l2, RIGHT, buff=0.45)
            self.play(*appear(l1), *appear(t1, shift=0.2 * LEFT), run_time=1.2)
            self.play(*appear(l2, t2, lag=0.2), run_time=1.1)
            c.wait_until("so the two")
            s_ = MathTex(r"\ln(-1) + \ln(-1) = ", r"2\pi i", font_size=48).move_to([0, -0.3, 0])
            s_.align_to([XL, 0, 0], LEFT)
            s_[1].set_color(YELLOW)
            self.play(*appear(s_), run_time=1.3)
            c.wait_until("product")
            pz = MathTex(r"z_1 z_2 = 1", font_size=48).move_to([0, -1.55, 0]).align_to([XL, 0, 0], LEFT)
            self.play(*appear(pz), run_time=1.0)
            c.wait_until("principal log of one")
            l0 = MathTex(r"\ln 1 = ", r"0", font_size=48).move_to([0, -2.6, 0]).align_to([XL, 0, 0], LEFT)
            l0[1].set_color(YELLOW)
            t0 = T("principal value", size=30, color=GREEN).next_to(l0, RIGHT, buff=0.45)
            self.play(*appear(l0), *appear(t0, shift=0.2 * LEFT), run_time=1.2)
            c.wait_until("differ")

            CX = 4.3
            sl = VGroup()
            sl.line = DashedLine([CX, -2.3, 0], [CX, 2.3, 0], dash_length=0.12, color=GOLD, stroke_width=3)
            r0 = Dot([CX, -1.2, 0], radius=0.09, color=GREEN)
            r1 = Dot([CX, 1.2, 0], radius=0.08, color=TEAL)
            fades = VGroup(*[Dot([CX, y, 0], radius=0.06, color=TEAL).set_opacity(o)
                             for y, o in ((1.6, 0.55), (1.95, 0.25), (-1.6, 0.55), (-1.95, 0.25))])
            lab1 = MathTex(r"2\pi i", font_size=40, color=YELLOW).next_to(r1, LEFT, buff=0.3)
            lab0 = MathTex(r"0", font_size=40, color=YELLOW).next_to(r0, LEFT, buff=0.3)
            sbrace = Brace(Line(r0.get_center(), r1.get_center()), direction=RIGHT, buff=0.2, color=TEAL)
            sbl = MathTex(r"2\pi i", font_size=36, color=TEAL).next_to(sbrace, RIGHT, buff=0.12)
            neq = MathTex(r"2\pi i \neq 0", font_size=48, color=RED).move_to([CX, -2.95, 0])
            self.play(*appear(sl.line, r0, r1, fades, shift=None, lag=0.1),
                      *appear(lab1, lab0, lag=0.2, shift=None),
                      FlashAround(s_[1], run_time=1.2), FlashAround(l0[1], run_time=1.2),
                      run_time=min(1.4, 0.55 * c.until()))
            self.play(GrowFromCenter(sbrace), FadeIn(sbl), *appear(neq), run_time=min(1.0, c.until()))

        # ============================================================ clip 4: why, in angles
        with self.say("c4.prin.4", gap=3.0) as c:
            S = pull_back_shot()
            small = VGroup(sl.line, r0, r1, fades, lab1, lab0, sbrace, sbl, neq)
            clear_to(self, FadeIn(VGroup(S.plane, S.m1, S.p1)), keep=[small], run_time=1.4)
            c.wait_until("add")
            S.arrow.rotate(PI, about_point=AO)
            pi_lab = MathTex(r"\pi", font_size=44, color=YELLOW).move_to(S.angle_label)
            self.play(GrowArrow(S.arrow), Create(S.spiral1), run_time=1.5)
            self.play(*appear(pi_lab), run_time=0.8)
            c.wait_until("gives two pi")
            two_pi = MathTex(r"2\pi", font_size=44, color=YELLOW).move_to(S.angle_label)
            self.play(Rotate(S.arrow, PI, about_point=AO), Create(S.spiral2, rate_func=linear),
                      run_time=1.6)
            self.play(*swap(pi_lab, two_pi), run_time=1.0)
            c.wait_until("outside")
            self.play(Create(S.green), FadeIn(S.open_end), FadeIn(S.closed_end), run_time=1.5)
            self.play(VShowPassingFlash(S.spiral2.copy().set_stroke(YELLOW, 10), time_width=0.6),
                      FlashAround(two_pi, color=RED, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("pull")
            self.play(Create(S.red), run_time=2.0)
            self.play(*appear(S.red_label), run_time=0.8)
            c.wait_until("to zero")
            self.play(*swap(two_pi, S.angle_label), run_time=1.0)
            c.wait_until("lesson")
            ok = T("whole ladders:\nthe rule holds", size=30, color=GREEN)
            bad = T("principal values:\noff by one rung", size=30, t2c={"off by one rung": RED})
            ok.move_to([3.9, 1.3, 0])
            bad.move_to([3.9, -0.4, 0])
            self.play(*disappear(sl.line, r0, r1, fades, lab1, lab0, sbrace, sbl), run_time=0.8)
            self.play(*appear(ok, bad, lag=0.5), run_time=1.6)  # early: the pair is the takeaway, read as the sentence runs

        # ============================================================ clip 5: F18
        with self.say("c4.prin.5", gap=4.5) as c:
            head = T("F18. Find the (natural) logarithms of the following:", size=36).move_to([0, 3.1, 0])
            items = VGroup(*[MathTex(s, font_size=44) for s in
                             (r"\text{(a)}\; -1", r"\text{(b)}\; i", r"\text{(c)}\; 1 + i",
                              r"\text{(d)}\; (x + iy)^*", r"\text{(e)}\; ire^{i\theta}")])
            items.arrange(RIGHT, buff=0.7).move_to([0, 2.15, 0])
            clear_to(self, FadeIn(head, shift=0.25 * DOWN), run_time=1.2)
            self.play(*appear(*items, lag=0.3), run_time=1.6)  # early: the question as printed
            c.wait_until("hint")
            tpl = MathTex(r"r\,e^{i(\theta + ", r"2\pi n", r")}", r"\;\longrightarrow\;",
                          r"\ln r + i(\theta + ", r"2\pi n", r")", font_size=52).move_to([0, 0.75, 0])
            tpl[1].set_color(TEAL)
            tpl[5].set_color(TEAL)
            self.play(*appear(tpl), run_time=1.5)
            c.wait_until("conj")
            dc = np.array([-4.3, -2.05, 0])
            u = 1.15
            pd = mini_plane(dc, u)
            th = 0.6
            zpt = dc + u * np.array([np.cos(th), np.sin(th), 0])
            zbar = dc + u * np.array([np.cos(th), -np.sin(th), 0])
            zr = Line(dc, zpt, color=YELLOW, stroke_width=3)
            zd = Dot(zpt, radius=0.08, color=YELLOW)
            za = Arc(radius=0.55, start_angle=0, angle=th, arc_center=dc, color=YELLOW, stroke_width=4)
            zal = MathTex(r"\theta", font_size=40, color=YELLOW).move_to(dc + 0.75 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))
            zbr = Line(dc, zbar, color=TEAL, stroke_width=3)
            zbd = Dot(zbar, radius=0.08, color=TEAL)
            zba = Arc(radius=0.55, start_angle=0, angle=-th, arc_center=dc, color=TEAL, stroke_width=4)
            zbal = MathTex(r"-\theta", font_size=40, color=TEAL).move_to(dc + 0.85 * np.array([np.cos(th / 2), -np.sin(th / 2), 0]) + 0.1 * RIGHT)
            dlab = MathTex(r"\text{(d)}", font_size=40).next_to(pd, LEFT, buff=0.3)
            self.play(*appear(pd, dlab, shift=None), Create(zr), FadeIn(zd), Create(za), FadeIn(zal),
                      FlashUnder(items[3], color=YELLOW, run_time=1.4), run_time=1.4)
            self.play(Create(zbr), FadeIn(zbd), Create(zba), FadeIn(zbal), run_time=1.3)
            c.wait_until("times")
            ec = np.array([4.0, -2.05, 0])
            pe = mini_plane(ec, u)
            a0 = 0.45
            v0 = Arrow(ec, ec + 1.05 * u * np.array([np.cos(a0), np.sin(a0), 0]), buff=0, color=FG,
                       stroke_width=4, max_tip_length_to_length_ratio=0.2)
            v0l = MathTex(r"re^{i\theta}", font_size=40).next_to(v0.get_end(), RIGHT, buff=0.1)
            v1 = Arrow(ec, ec + 1.05 * u * np.array([np.cos(a0 + PI / 2), np.sin(a0 + PI / 2), 0]), buff=0,
                       color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.2)
            v1l = MathTex(r"ire^{i\theta}", font_size=40, color=YELLOW).next_to(v1.get_end(), LEFT, buff=0.1)
            qa = Arc(radius=0.62, start_angle=a0, angle=PI / 2, arc_center=ec, color=YELLOW, stroke_width=4)
            qa.add_tip(tip_length=0.15, tip_width=0.15)
            qal = MathTex(r"+\tfrac{\pi}{2}", font_size=40, color=YELLOW).move_to(
                ec + 0.85 * np.array([np.cos(a0 + PI / 4), np.sin(a0 + PI / 4), 0]) + 0.2 * UP + 0.15 * RIGHT)
            elab = MathTex(r"\text{(e)}", font_size=40).next_to(pe, RIGHT, buff=0.3)
            self.play(*appear(pe, elab, shift=None), GrowArrow(v0), FadeIn(v0l),
                      FlashUnder(items[4][0][3:], color=YELLOW, run_time=1.2), run_time=1.2)
            self.play(Create(qa), *fly(v0, v1), run_time=1.5)
            self.play(*appear(v1l, qal), run_time=0.9)
            c.wait_until("sol")
            sol = T("Solutions: Part 8", size=34).move_to([0, -2.1, 0])
            self.play(*appear(sol), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
