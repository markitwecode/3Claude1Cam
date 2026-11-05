"""Chapter 5, scene 4: i to the power i, worked by the definition; every value is real. Clips c5.ii.1 – c5.ii.4.

Shared: `recipe_card()` (module level) draws the four-step method card for complex powers
(1. polar base with 2πn TEAL, 2. take ln, 3. multiply by the exponent, 4. exponentiate);
the chapter recap (s8) reuses it.
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

HOOK = load_scene("ch5_s1_hook")
DEF = load_scene("ch5_s2_define")
S3 = load_scene("ch5_s3_two_i")

ROW = 64                      # derivation rows
EQ_X = -3.6                   # x of every row's "="
ROW_Y = (1.4, 0.2, -1.0, -2.2)

# small Argand plane on the right
PS = 0.7
PO = np.array([4.3, -0.4, 0.0])
PU = S3.U * PS


def Q(x, y):
    return PO + PU * np.array([x, y, 0.0])


def small_plane():
    pl = S3.argand_plane(xr=(-1.3, 1.45), yr=(-1.3, 1.5))
    pl.scale(PS, about_point=S3.O).shift(PO - S3.O)
    xax, yax = pl[1], pl[2]
    re = T("Re", size=30).next_to(xax.get_end(), DOWN, buff=0.15)
    im = T("Im", size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    pl.remove(pl[3], pl[4])
    pl.add(re, im)
    return pl


def row(tex, y, eq_index, pinks=(), teals=None, size=ROW):
    m = MathTex(tex, font_size=size, color=FG)
    for k in pinks:
        m[0][k].set_color(PINK)
    if teals:
        m[0][teals[0]:teals[1]].set_color(TEAL)
    m.shift(np.array([EQ_X, y, 0]) - m[0][eq_index].get_center())
    return m


# ---------------------------------------------------------------- shared helper
def recipe_card(size=40):
    """The method card for complex powers, centred at ORIGIN.
    VGroup with .box (BLUE rounded rectangle), .title, .steps (4 rows, each VGroup(num, body...)),
    .tealn (the TEAL 2πn glyphs of step 1)."""
    title = T("The method", size=size + 4, color=BLUE)

    def num(k):
        return T(f"{k}.", size=size, color=YELLOW)

    polar = MathTex(r"|z|\,e^{i(\arg z+2\pi n)}", font_size=size + 8, color=FG)
    polar[0][11:14].set_color(TEAL)
    s1 = VGroup(num(1), T("write the base as", size=size), polar).arrange(RIGHT, buff=0.25)
    s2 = VGroup(num(2), T("take", size=size), MathTex(r"\ln", font_size=size + 8)).arrange(RIGHT, buff=0.22)
    s3 = VGroup(num(3), T("multiply by the exponent", size=size)).arrange(RIGHT, buff=0.25)
    s4 = VGroup(num(4), T("exponentiate", size=size)).arrange(RIGHT, buff=0.25)
    for s in (s2, s3, s4):
        s[1].align_to(s[0], DOWN)
    s2[2].align_to(s2[1], DOWN)
    steps = VGroup(s1, s2, s3, s4).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
    title.next_to(steps, UP, buff=0.45).align_to(steps, LEFT)
    body = VGroup(title, steps)
    box = RoundedRectangle(corner_radius=0.25, width=body.width + 1.0, height=body.height + 0.8,
                           color=BLUE, stroke_width=3).move_to(body)
    g = VGroup(box, title, steps).move_to(ORIGIN)
    g.box, g.title, g.steps, g.tealn = box, title, steps, polar[0][11:14]
    return g


class IToTheI(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(2.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c5.ii.1
    def clip1(self):
        with self.say("c5.ii.1") as c:
            q = HOOK.ii_question(size=130).move_to(0.3 * UP)
            self.play(*appear(q), run_time=1.0)
            c.wait_until("def")

            dbox = DEF.definition_box(size=44, note=False)
            dbox.shift(np.array([0.7, 2.35, 0]) - dbox.tex.get_center())
            self.play(*during([q.animate.scale(0.55).move_to([-5.5, 2.75, 0])], 0, 0.6),
                      *during(appear(dbox), 0.4, 1), run_time=min(1.6, c.until("eye log eye")))
            r1 = row(r"i^{i}=e^{i\ln i}", ROW_Y[0], 2, pinks=(0, 1, 4, 7))
            arr = CurvedArrow(dbox.box.get_bottom() + 0.6 * LEFT + 0.05 * DOWN,
                              r1.get_right() + 0.25 * RIGHT, angle=-1.1, color=YELLOW, stroke_width=3,
                              tip_length=0.2)
            self.play(Create(arr), *during(appear(r1), 0.35, 1), run_time=1.5)
            c.wait_until("need")

            self.play(FlashAround(r1[0][5:8], color=YELLOW, run_time=1.6, time_width=1.5),
                      *recolor(r1[0][5:7], YELLOW), run_time=1.6)
            c.wait_until("polar")

            plane = small_plane()
            self.play(FadeIn(plane), run_time=min(1.0, 0.4 * c.until("turns")))
            rad = Arrow(PO, Q(0, 1), buff=0, color=GOLD, stroke_width=6, max_tip_length_to_length_ratio=0.15)
            idot = Dot(Q(0, 1), radius=0.11, color=PINK)
            arc = Arc(radius=0.42, start_angle=0, angle=PI / 2, arc_center=PO, color=YELLOW, stroke_width=4)
            self.play(GrowArrow(rad), GrowFromCenter(idot), Create(arc), run_time=1.4)
            ilab = MathTex("i", font_size=44, color=PINK).next_to(idot, RIGHT, buff=0.15).shift(0.26 * UP)  # above the circle: on it, the arc reads as "−i"
            one = MathTex("1", font_size=36, color=GOLD).next_to(rad, LEFT, buff=0.15)
            pi2 = MathTex(r"\pi/2", font_size=36, color=YELLOW).move_to(PO + 0.85 * np.array([0.9, 0.55, 0]))
            for m in (ilab, one, pi2):
                set_backstroke(m, width=8)
            self.play(*appear(ilab, one, pi2, lag=0.3), run_time=min(1.3, c.until("turns")))
            c.wait_until("turns")

            r2a = row(r"i=e^{i\pi/2}", ROW_Y[1], 1, pinks=(0, 3))
            self.play(*appear(r2a), run_time=1.0)
            c.wait_until("plus two pi n")

            r2 = row(r"i=e^{i(\pi/2+2\pi n)}", ROW_Y[1], 1, pinks=(0, 3), teals=(8, 12))
            sweeper = Arrow(PO, Q(0, 1), buff=0, color=TEAL, stroke_width=6, max_tip_length_to_length_ratio=0.15)
            full = Arc(radius=0.28, start_angle=PI / 2, angle=TAU, arc_center=PO, color=TEAL, stroke_width=4)

            def turn(m, a):
                ang = PI / 2 + a * TAU
                m.become(Arrow(PO, PO + PU * np.array([np.cos(ang), np.sin(ang), 0]), buff=0, color=TEAL,
                               stroke_width=6, max_tip_length_to_length_ratio=0.15))

            self.add(sweeper)
            self.play(UpdateFromAlphaFunc(sweeper, turn), Create(full), *edit(r2a, r2),
                      run_time=min(2.2, c.until()))
            self.remove(sweeper)
            self.q, self.dbox, self.arr, self.r1, self.r2 = q, dbox, arr, r1, r2
            self.plane_mobs = [plane, rad, idot, arc, ilab, one, pi2, full]

    # ------------------------------------------------------------------ c5.ii.2
    def clip2(self):
        r1, r2 = self.r1, self.r2
        with self.say("c5.ii.2") as c:
            r3 = row(r"\ln i=i(\pi/2+2\pi n)", ROW_Y[2], 3, pinks=(2, 4), teals=(9, 13))
            self.play(FlashAround(r2[0][3:13], color=YELLOW, run_time=1.6, time_width=1.5),
                      *during(appear(r3), 0.35, 1), run_time=1.6)
            c.wait_until("mult")

            r4 = row(r"i^{i}=e^{i\cdot i(\pi/2+2\pi n)}", ROW_Y[3], 2, pinks=(0, 1, 4, 6), teals=(11, 15))
            self.play(*during(disappear(*self.plane_mobs), 0, 0.5),
                      FlashAround(r1[0][4], color=PINK, run_time=1.6, time_width=1.5),
                      *during(appear(r4), 0.4, 1), run_time=1.6)
            c.wait_until("square")

            self.play(*flash([r4[0][4], r4[0][6]], color=PINK, run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("minus pi over two")
            r4b = row(r"i^{i}=e^{-\pi/2-2\pi n}", ROW_Y[3], 2, pinks=(0, 1), teals=(8, 12))
            self.play(*edit(r4, r4b), run_time=min(1.8, c.until("answer")))
            c.wait_until("answer")

            box = SurroundingRectangle(r4b, color=YELLOW, buff=0.25, stroke_width=4)
            self.play(FadeIn(box), *set_alpha([r1, r2, r3], 0.4), run_time=1.2)
            ans = VGroup(r4b, box)
            settle(self, ans)
            c.wait_until("notes")

            nl = [MathTex(s, font_size=36, color=FG) for s in
                  (r"z=i^{i}", r"\ln z=i\ln i", r"=i\,[\,i(\pi/2+2\pi n)\,]", r"=-(\pi/2+2\pi n)",
                   r"z=e^{-(\pi/2+2\pi n)}")]
            head = T("the notes", size=30, color=DIM)
            notes = VGroup(head, *nl).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            for m in nl[2:4]:
                m.shift(0.55 * RIGHT)
            notes.move_to([4.5, -0.15, 0]).align_to(np.array([2.9, 0, 0]), LEFT)
            tick = check_mark().scale(0.8)
            same = T("same answer", size=30, color=GREEN)
            tag = VGroup(tick, same).arrange(RIGHT, buff=0.2).next_to(notes, DOWN, buff=0.4).align_to(notes, LEFT)
            self.play(*appear(head, *nl, lag=0.3), run_time=min(2.2, c.until("same")))  # early: the notes' route, shown whole as one block
            c.wait_until(own_word=same)
            self.play(*appear(tick, same, lag=0.2), run_time=min(1.0, c.until(floor=0.5)))
            self.ans, self.r4b, self.box, self.r3 = ans, r4b, box, r3
            self.notes, self.notes_tag = notes, tag

    # ------------------------------------------------------------------ c5.ii.3
    def clip3(self):
        ans, r4b, box = self.ans, self.r4b, self.box
        with self.say("c5.ii.3") as c:
            self.play(FlashAround(box, color=YELLOW, run_time=1.6, time_width=1.5), run_time=1.6)
            c.wait_until("noeye")

            left = [self.q, self.dbox, self.arr, self.r1, self.r2, self.r3]
            self.play(*during(disappear(*left), 0, 0.45),
                      *during([ans.animate.scale(1.15).move_to([-0.6, 2.6, 0])], 0.4, 1), run_time=1.6)
            self.play(*flash([r4b[0][3:]], color=YELLOW, run_time=1.2), run_time=1.2)
            real = T("real", size=48, color=BLUE)
            c.wait_until(own_word=real)
            real.next_to(box, RIGHT, buff=0.5)
            self.play(*recolor(r4b[0][3:], BLUE), restyle(box, outline=BLUE), *appear(real), run_time=1.4)
            c.wait_until("principal")

            strip = S3.two_i_ray(step=2.9, angle=0, center=np.array([0, 0.5, 0]), n_max=1, size=36,
                                 tick_tex=[r"\approx 0.00039", r"e^{-\pi/2}\approx 0.208", r"\approx 111"],
                                 n_tex=[r"n=1", r"n=0", r"n=-1"], dot_r=0.13)
            for k, n in enumerate(strip.ns):
                strip.tick_labels[k].set_color(GREEN if n == 0 else TEAL)
            i0 = strip.ns.index(0)
            self.play(*during(disappear(self.notes, self.notes_tag), 0, 0.45),
                      *during([Create(strip.line), FadeIn(strip.ticks)], 0.4, 1), run_time=1.6)
            self.play(GrowFromCenter(strip.dots[i0]),
                      *appear(strip.n_labels[i0], strip.tick_labels[i0], lag=0.3), run_time=1.4)
            c.wait_until("others")

            for n, cue in ((1, "others"), (-1, "minus one")):
                c.wait_until(cue)
                k = strip.ns.index(n)
                extra = [FadeIn(strip.many)] if n == -1 else []
                self.play(GrowFromCenter(strip.dots[k]), *appear(strip.n_labels[k], strip.tick_labels[k], lag=0.3),
                          *extra, run_time=1.2)
            c.wait_until("axis")

            ray = S3.two_i_ray(step=1.0, n_max=1, size=30, center=np.array([1.2, -2.25, 0]), dot_r=0.09)
            lab = MathTex(r"2^{i}", font_size=48, color=FG).move_to([-1.6, -2.25, 0])
            self.play(FadeIn(ray), *appear(lab), run_time=0.9)
            self.play(VShowPassingFlash(strip.line.copy().set_stroke(YELLOW, 7), time_width=0.5),
                      VShowPassingFlash(ray.line.copy().set_stroke(YELLOW, 7), time_width=0.5),
                      run_time=min(1.6, c.until(floor=0.5)))

    # ------------------------------------------------------------------ c5.ii.4
    def clip4(self):
        with self.say("c5.ii.4") as c:
            quote = T("“probably the hardest problems you're going to get\non the complex numbers”",
                      size=38, slant=ITALIC, line_spacing=1.0)
            who = T("the lecturer", size=38, color=DIM)
            who.next_to(quote, DOWN, buff=0.3).align_to(quote, RIGHT)
            qg = VGroup(quote, who).move_to(0.3 * UP)
            sweep_clear(self, *during(appear(quote, who, lag=0.4), 0.5, 1), run_time=1.6)
            c.wait_until("recipe")

            card = recipe_card(size=38)
            card.move_to([0, -0.8, 0])
            self.play(*during([qg.animate.scale(0.8).move_to([0, 2.72, 0])], 0, 0.6),
                      *during([FadeIn(card.box), *appear(card.title)], 0.45, 1),
                      run_time=min(1.6, c.until("write the base")))
            steps = card.steps
            for k, cue in enumerate(("write the base", "s2", "s3", "s4")):
                c.wait_until(cue)
                self.play(*appear(steps[k], shift=0.2 * RIGHT), run_time=1.0)
                if k == 0:
                    self.play(*flash([card.tealn], color=TEAL, run_time=1.2), run_time=1.2)
            c.wait_until()
            settle(self, card)
