"""Chapter 4, scene 6: infinitely many solutions, a lattice in the Argand plane. Clips c4.lattice.1 – c4.lattice.4.

Opens on ch4_s5_even's handover_shot() (card + x = 2πm over y = ±ln(2 + √3)); ends on an empty frame.
Exports `lattice(...)`: the Argand lattice of cos z = 2 (L10 argand_plane styling: faint grid, FG
arrows at 0.7; Re z FG, Im z PINK; ticks -4π..4π; GREEN crosses at 2πm ± i ln(2 + √3); BLUE 2π brace,
TEAL ln(2 + √3) ≈ 1.32 brace; ⋯ and faded crosses past both edges). Attributes: .base .pairs
(list, m = ms[0]..ms[-1]) .pair(m) .crosses .faded .dots .bh .bh_lab .b2 .b2_lab .origin.
`answer_line(size)`: z = 2πm ± i ln(2 + √3), m ∈ Z (parts 0..6, coloured by origin).
"""
# style: 2
import math
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

S5 = load_scene("ch4_s5_even")
S2 = load_scene("ch4_s2_fta")
D = load_scene("ch1_s2_define")
mt = S5.mt

H = math.log(2 + math.sqrt(3))            # 1.3169...
XS, YS = 0.34, 0.95                       # lattice units per real unit (2π → 2.14)
LAT_C = np.array([0.0, -1.15, 0])
GRAPH_C = np.array([2.6, -1.6, 0])
THUMB_C = np.array([-4.1, -0.6, 0])
THUMB_S = 0.38


# ---------------------------------------------------------------- shared builders
def cross(p, size=0.26, color=GREEN, width=5):
    d = size / 2
    return VGroup(Line(p + d * UL, p + d * DR), Line(p + d * UR, p + d * DL)).set_stroke(color, width)


def lattice(center=LAT_C, xs=XS, ys=YS, half_w=6.5, half_h=2.05, ms=range(-2, 3), size=30, extras=True):
    """The roots of cos z = 2 on an Argand plane (see module docstring)."""
    o = np.array(center, dtype=float)

    def pt(x, y):
        return o + np.array([x * xs, y * ys, 0])

    grid = VGroup()
    k = 1
    while k * PI * xs < half_w - 0.05:
        for s in (1, -1):
            x = s * k * PI * xs
            grid.add(Line(o + [x, -half_h, 0], o + [x, half_h, 0]))
        k += 1
    k = 1
    while k * 0.5 * ys < half_h - 0.05:
        for s in (1, -1):
            y = s * k * 0.5 * ys
            grid.add(Line(o + [-half_w, y, 0], o + [half_w, y, 0]))
        k += 1
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow(o + [-half_w, 0, 0], o + [half_w, 0, 0], **ax_kw).set_opacity(0.7)
    y_ax = Arrow(o + [0, -half_h, 0], o + [0, half_h, 0], **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}\,z", font_size=size, color=FG).next_to(x_ax.get_end(), UP, buff=0.15)
    re.shift(0.3 * LEFT)
    im = MathTex(r"\mathrm{Im}\,z", font_size=size, color=PINK).next_to(y_ax.get_end(), LEFT, buff=0.15)
    im.shift(0.2 * DOWN)
    ticks, tlabs = VGroup(), VGroup()
    for m, s in zip(range(-2, 3), [r"-4\pi", r"-2\pi", "0", r"2\pi", r"4\pi"]):
        p = pt(2 * PI * m, 0)
        ticks.add(Line(p + 0.07 * DOWN, p + 0.07 * UP).set_stroke(DIM, 2))
        lab = MathTex(s, font_size=max(28, size - 2), color=DIM).move_to(p + 0.34 * DOWN)
        if m == 0:
            lab.shift(0.2 * RIGHT)
        tlabs.add(lab)
    base = VGroup(grid, x_ax, y_ax, ticks, tlabs, re, im)
    pairs = [VGroup(cross(pt(2 * PI * m, H)), cross(pt(2 * PI * m, -H))) for m in ms]
    g = VGroup(base, *pairs)
    g.base, g.pairs, g.ms, g.origin, g.pt = base, pairs, list(ms), o, pt
    g.crosses = VGroup(*pairs)
    g.pair = lambda m: pairs[list(ms).index(m)]
    if extras:
        m_hi = max(ms) + 1
        g.faded = VGroup(*[cross(pt(2 * PI * s * m_hi, sg * H)) for s in (-1, 1) for sg in (1, -1)])
        g.faded.set_stroke(opacity=0.3)
        xd = (2 * PI * (m_hi - 0.5))
        g.dots = VGroup(*[MathTex(r"\cdots", font_size=40, color=GREEN).move_to(pt(s * xd, sg * H))
                          for s in (-1, 1) for sg in (1, -1)])
        top = pt(0, H)
        g.b2 = span_brace(top, pt(2 * PI, H), direction=UP, color=BLUE)
        g.b2_lab = MathTex(r"2\pi", font_size=34, color=BLUE).next_to(g.b2, UP, buff=0.08)
        g.bh = Brace(Line(o, top), direction=LEFT, buff=0.14, color=TEAL)
        g.bh_lab = MathTex(r"\ln\left(2 + \sqrt{3}\right) \approx 1.32", font_size=size, color=TEAL)
        g.bh_lab.next_to(g.bh, LEFT, buff=0.1)
        g.add(g.faded, g.dots, g.b2, g.b2_lab, g.bh, g.bh_lab)
    return g


def answer_line(size=56):
    """z = 2πm ± i ln(2 + √3), m ∈ Z: 2πm BLUE, ± YELLOW, i PINK, ln(2 + √3) TEAL."""
    a = MathTex("z", "=", r"2\pi m", r"\pm", "i", r"\ln\left(2 + \sqrt{3}\right)", r",\quad m \in \mathbb{Z}",
                font_size=size)
    a[2].set_color(BLUE)
    a[3].set_color(YELLOW)
    a[4].set_color(PINK)
    a[5].set_color(TEAL)
    return a


# ---------------------------------------------------------------- the check
SRC_L1 = (r"\cos\left(i\ln\left(2 + \sqrt{3}\right)\right) = \cosh\left(\ln\left(2 + \sqrt{3}\right)\right)",
          "BBB F P TTTTTTTTT F F TTTT F TTTTTTTTT F")
SRC_L2 = (r"= \tfrac{1}{2}\left(2 + \sqrt{3} + \tfrac{1}{2 + \sqrt{3}}\right) = \tfrac{1}{2}\left(2 + \sqrt{3} + 2 - \sqrt{3}\right) = 2",
          "F FFF F GGGGG F UUUUUUU F F FFF F GGGGG F UUUUU F F Y")
SRC_SIDE = (r"(2 + \sqrt{3})(2 - \sqrt{3}) = 4 - 3 = 1", "GGGGGGG UUUUUUU FFFFFF")


def avg_graph():
    """ch1 s2's averaging picture, small: same axis style, e^y GOLD, e^-y PURPLE."""
    ax = Axes(x_range=[D.X_LO, D.X_HI, 1], y_range=[-0.5, 5, 1], x_length=4.0, y_length=3.3, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": True, "tick_size": 0.06})
    ax.move_to(GRAPH_C)
    ex, emx = D.exp_curve(ax, width=4), D.emx_curve(ax, width=4)
    l_ex = set_backstroke(MathTex("e^{y}", font_size=34, color=GOLD))
    l_ex.next_to(ax.c2p(math.log(4.6), 4.6), LEFT, buff=0.2)
    l_emx = set_backstroke(MathTex("e^{-y}", font_size=34, color=PURPLE))
    l_emx.next_to(ax.c2p(-1.2, math.exp(1.2)), LEFT, buff=0.25)
    return ax, ex, emx, l_ex, l_emx


class Lattice(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c4.lattice.1
    def clip1(self):
        card, xl, yl = S5.handover_shot()
        self.add(card, xl, yl)
        self.card = card
        full = answer_line(56)
        ans = VGroup(*full[0:6])
        mz = full[6]
        full.move_to(ORIGIN)
        full.shift(-ans.get_center()[0] * RIGHT)      # the main part centred at x = 0
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.28, corner_radius=0.12).set_stroke(width=3)
        with self.say("c4.lattice.1") as c:
            self.play(xl.animate.shift(0.8 * UP), yl.animate.shift(0.6 * DOWN), run_time=0.8)
            self.play(*fly(xl.rhs, full[2]), *fly(yl.pm, full[3]), *fly(yl.ln, full[5]),
                      *during(appear(full[0], full[1], full[4], shift=None, lag=0.1), 0.5, 1.0),
                      *during([FadeIn(box)], 0.6, 1.0),
                      run_time=min(1.7, c.until("re")))
            settle(self, ans)
            c.wait_until("re")
            self.play(FlashAround(full[2], color=BLUE, run_time=1.5, time_width=1.5))
            c.wait_until("im")
            self.play(FlashAround(full[5], color=TEAL, run_time=1.5, time_width=1.5),
                      FlashAround(VGroup(full[3], full[4]), color=YELLOW, run_time=1.5, time_width=1.5))
            self.play(*disappear(xl, yl), run_time=0.8)
            c.wait_until("m")
            dx = (full.get_center() - ans.get_center())[0]
            box2 = SurroundingRectangle(full, color=YELLOW, buff=0.28, corner_radius=0.12).set_stroke(width=3)
            box2.shift(-dx * RIGHT)
            mz.shift(-dx * RIGHT)
            self.play(ans.animate.shift(-dx * RIGHT), Transform(box, box2),
                      *during(appear(mz, shift=None), 0.45, 1.0), run_time=1.5)
        self.answer = VGroup(box, ans, mz)
        settle(self, self.answer)

    # ------------------------------------------------------------ c4.lattice.2
    def clip2(self):
        lat = self.lat = lattice()
        p0 = lat.pair(0)
        with self.say("c4.lattice.2") as c:
            self.play(self.answer.animate.scale(0.6).move_to([0, 1.5, 0]),
                      *during(appear(lat.base, shift=None), 0.35, 1.0), run_time=2.0)
            c.wait_until("straight above")
            self.play(GrowFromCenter(p0[0]), GrowFromCenter(p0[1]), run_time=1.2)
            c.wait_until("about one point three two")
            self.play(GrowFromCenter(lat.bh), *appear(lat.bh_lab, shift=None), run_time=1.2)
            c.wait_until("conj")
            top, bot = p0[0].get_center(), p0[1].get_center()
            dash = DashedLine(top, bot, dash_length=0.12, color=YELLOW, stroke_width=3)
            self.play(Create(dash), run_time=1.2)
            c.wait_until("mirror images")
            ghost = p0[0].copy().set_stroke(YELLOW)
            self.play(Rotate(ghost, PI, axis=RIGHT, about_point=lat.origin), run_time=1.6)
            self.play(FadeOut(ghost), FlashAround(p0[1], color=YELLOW, run_time=1.2), run_time=1.2)
            c.wait_until("at two pi")
            self.play(ReplacementTransform(p0.copy(), lat.pair(1)), *during(disappear(dash), 0, 0.4), run_time=1.3)
            c.wait_until("at four pi")
            self.play(ReplacementTransform(lat.pair(1).copy(), lat.pair(2)), run_time=0.9)
            c.wait_until("at minus two pi")
            self.play(ReplacementTransform(p0.copy(), lat.pair(-1)), run_time=0.8)
            self.play(ReplacementTransform(lat.pair(-1).copy(), lat.pair(-2)), run_time=0.7)
            c.wait_until("forever")
            self.play(*appear(*lat.dots, shift=None, lag=0.1), *appear(*lat.faded, shift=None, lag=0.1),
                      run_time=1.4)
            c.wait_until("infinite")
            inf = T("infinitely many", 40, YELLOW).move_to([3.9, -3.2, 0])
            self.play(*appear(inf), run_time=1.0)
            c.wait_until("spaced")
            self.play(GrowFromCenter(lat.b2), *appear(lat.b2_lab), run_time=1.2)
        self.inf = inf
        settle(self, lat)

    # ------------------------------------------------------------ c4.lattice.3
    def clip3(self):
        lat, answer = self.lat, self.answer
        top = lat.pair(0)[0]
        l1 = mt(*SRC_L1, size=44).move_to([0, 2.15, 0])
        l1a, l1b = VGroup(*l1[0][0:15]), VGroup(*l1[0][15:])
        l2 = mt(*SRC_L2, size=42).move_to([0, 1.1, 0])
        g = l2[0]
        l2a, l2b, l2c = VGroup(*g[0:19]), VGroup(*g[19:36]), VGroup(*g[36:38])
        tick = check_mark().next_to(l2, RIGHT, buff=0.35)
        ax, ex, emx, l_ex, l_emx = avg_graph()
        vline = Line(ax.c2p(H, -0.3), ax.c2p(H, 4.8)).set_stroke(TEAL, 3)
        hl = MathTex("1.32", font_size=30, color=TEAL).next_to(ax.c2p(H, -0.5), DOWN, buff=0.1).shift(0.35 * LEFT)
        gd = Dot(ax.c2p(H, 2 + math.sqrt(3)), radius=0.09, color=GOLD)
        pd = Dot(ax.c2p(H, 2 - math.sqrt(3)), radius=0.09, color=PURPLE)
        md = Dot(ax.c2p(H, 2), radius=0.11, color=YELLOW)
        g_lab = MathTex(r"2 + \sqrt{3} \approx 3.73", font_size=32, color=GOLD).next_to(gd, RIGHT, buff=0.2)
        p_lab = MathTex(r"2 - \sqrt{3} \approx 0.27", font_size=32, color=PURPLE).next_to(pd, RIGHT, buff=0.2)
        p_lab.shift(0.38 * DOWN)
        m_lab = MathTex("2", font_size=36, color=YELLOW).next_to(md, RIGHT, buff=0.2)
        side = mt(*SRC_SIDE, size=34).move_to([THUMB_C[0], -2.75, 0])
        with self.say("c4.lattice.3") as c:
            self.play(FlashAround(top, color=YELLOW, run_time=1.2, time_width=1.5))
            lat.save_state()
            answer.save_state()
            lat.generate_target()
            tg = lat.target
            tg.scale(THUMB_S).move_to(THUMB_C)
            for m in (*tg.base[4:7], tg.dots, tg.bh_lab, tg.b2_lab):
                m.set_opacity(0)
            self.play(*during(disappear(self.card, self.inf), 0, 0.45),
                      *during([MoveToTarget(lat),
                               answer.animate.scale(0.9).move_to([0, 3.15, 0])], 0.2, 1.0), run_time=1.6)
            c.wait_until("cosh")
            self.play(*appear(l1a), run_time=1.0)
            c.wait_until("equals the hyperbolic")
            self.play(*appear(l1b), run_time=1.0)
            c.wait_until("avg")
            self.play(FadeIn(ax), Create(ex), Create(emx), run_time=1.5)
            self.play(*appear(l_ex, l_emx, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("up")
            self.play(Create(vline), *appear(hl, shift=None), run_time=1.2)
            c.wait_until("so E to the why")
            self.play(GrowFromCenter(gd), *appear(g_lab, shift=None), run_time=1.2)
            c.wait_until("down")
            self.play(GrowFromCenter(pd), *appear(l2a), run_time=1.4)
            c.wait_until("which is two minus")
            self.play(*appear(p_lab, shift=None), run_time=1.0)
            c.wait_until("because their product")
            self.play(*appear(side), run_time=1.2)
            c.wait_until("mid")
            self.play(*appear(l2b), run_time=1.4)
            gc, pc = gd.copy(), pd.copy()
            self.play(gc.animate.move_to(md), pc.animate.move_to(md), run_time=1.2)
            self.remove(gc, pc)
            self.add(md)
            self.play(*appear(m_lab, shift=None), FlashAround(md, color=YELLOW, run_time=1.0), run_time=1.0)
            c.wait_until("exactly two")
            self.play(*appear(l2c), run_time=1.0)
            c.wait_until("It works")
            self.play(Create(tick), run_time=0.8)
        self.check = [l1a, l1b, l2a, l2b, l2c, tick, ax, ex, emx, l_ex, l_emx, vline, hl, gd, pd, md,
                      g_lab, p_lab, m_lab, side]

    # ------------------------------------------------------------ c4.lattice.4
    def clip4(self):
        lat, answer = self.lat, self.answer
        bot = lat.pair(0)[1]
        tag = MathTex(r"\cosh(-y) = \cosh y", font_size=32, color=TEAL)
        with self.say("c4.lattice.4") as c:
            self.play(*during(disappear(*self.check), 0, 0.45),  # early: the card returns to its place, not a new label
                      *during([Restore(lat), Restore(answer)], 0.25, 0.85),
                      *during(appear(self.card, shift=None), 0.6, 1.0), run_time=2.0)
            tag.next_to(bot, DOWN, buff=0.3).align_to(lat.origin + 0.25 * LEFT, RIGHT)
            c.wait_until("because cosh")
            self.play(FlashAround(bot, color=TEAL, run_time=1.2, time_width=1.5),
                      *appear(tag, shift=None), run_time=1.2)
            c.wait_until("period")
            self.play(*[p.animate.set_stroke(width=8) for p in lat.pairs],
                      LaggedStart(*[FlashAround(p, color=GREEN, buff=0.15) for p in lat.pairs], lag_ratio=0.15),
                      run_time=1.6)
            c.wait_until("shift")
            row = VGroup(*[p.copy() for p in lat.pairs], *[f.copy() for f in lat.faded])
            row.set_stroke(YELLOW, 6)
            for f in row[len(lat.pairs):]:
                f.set_stroke(opacity=0.3)
            self.add(row)
            self.play(row.animate.shift(2 * PI * XS * RIGHT), run_time=2.6, rate_func=smooth)
            c.wait_until("contrast")

            # two cards
            ch = S2.peel_chain()
            _, _, _, br, _ = S2.peel_labels(ch)
            left = VGroup(ch, br)
            left.scale_to_fit_width(5.3).move_to([-3.35, 0.7, 0])
            cap_l = T("degree n: exactly n roots", 34, GREEN, t2s={"n": ITALIC}).move_to([-3.35, -1.35, 0])
            small = lattice(center=[3.35, 0.75, 0], xs=0.19, ys=0.6, half_w=2.7, half_h=1.3, size=28,
                            extras=False)
            cap_r = MathTex(r"\cos z - 2\text{: infinitely many}", font_size=40, color=YELLOW)
            cap_r.move_to([3.35, -1.35, 0])
            fr_l = RoundedRectangle(corner_radius=0.2, width=6.2, height=4.9, stroke_color=GREEN,
                                    stroke_width=3).move_to([-3.35, -0.05, 0])
            fr_r = fr_l.copy().set_stroke(YELLOW).move_to([3.35, -0.05, 0])
            sweep_clear(self, FadeIn(fr_l), FadeIn(fr_r), run_time=1.6)
            c.wait_until("A polynomial")
            self.play(*appear(left, shift=None), run_time=1.4)
            c.wait_until(own_word=cap_l)
            self.play(*appear(cap_l), run_time=1.0)
            c.wait_until("Cosine of zed minus two")
            self.play(*appear(small, shift=None), run_time=1.4)
            c.wait_until("infinitely many")
            self.play(*appear(cap_r), run_time=1.0)
            tag2 = S2.not_poly_tag(cap_r[0][0:4])
            tag2.label.set_x(3.35)
            c.wait_until(own_word=tag2.label)
            self.play(GrowFromCenter(tag2.line), *appear(tag2.label), run_time=1.2)
