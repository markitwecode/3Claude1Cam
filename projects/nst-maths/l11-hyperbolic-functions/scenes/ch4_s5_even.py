"""Chapter 4, scene 5: only even multiples of π. Clips c4.even.1 – c4.even.4.

Opens on ch4_s4_cases's handover_shot() (card + braced system + GREEN x = nπ).
Exports: `xeq_line()` (x = 2πm, 2πm BLUE; .rhs = glyphs 2..4), `yres_line()` (y = ±ln(2 + √3),
± YELLOW, ln(2 + √3) TEAL; .pm = glyph 2, .ln = glyphs 3..11), both at their handover places, and
`handover_shot()` (card + those two lines, graphs cleared); ch4_s6_lattice opens on it.
"""
# style: 2
# handover: next
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

S4 = load_scene("ch4_s4_cases")
S3 = load_scene("ch4_s3_split")
S1 = load_scene("ch4_s1_hook")
ex35_card, system_group, npi_line = S3.ex35_card, S4.system_group, S4.npi_line

COL = {"B": BLUE, "T": TEAL, "P": PINK, "G": GOLD, "U": PURPLE, "F": FG, "Y": YELLOW, "D": DIM,
       "g": GREEN, "R": RED}

SZ = 44                         # the system's size (same as scene 4)
HZ = 60                         # the hero equation
HERO = np.array([0.0, -0.45, 0])
WZ = 52                         # clip 3 working line
WORK = np.array([0.0, -1.35, 0])
FINAL_SZ = 52
FINAL_EQ_X = -1.6               # handover: both "=" at this x
FINAL_Y = (0.55, -0.75)

SRC_E0 = (r"\cos x \cosh y = 2", "BBBF TTTTF F F")
SRC_E1 = (r"\cos(n\pi) \cosh y = 2", "BBBF gg F TTTTF F F")
SRC_E2 = (r"(-1)^n \cosh y = 2", "FFFF g TTTTF F F")
SRC_X = (r"x = 2\pi m", "FF BBB")
SRC_CY = (r"\cosh y = 2", "TTTTF F F")
SRC_INV = (r"y = \pm\cosh^{-1} 2 = \pm\ln\left(2 + \sqrt{2^2 - 1}\right)", "FFY TTTTTT FF Y TTTTTTTTTTTT")
SRC_INV2 = (r"y = \pm\cosh^{-1} 2 = \pm\ln\left(2 + \sqrt{3}\right)", "FFY TTTTTT FF Y TTTTTTTTT")
SRC_Y = (r"y = \pm\ln\left(2 + \sqrt{3}\right)", "FFY TTTTTTTTT")
SRC_ABOUT = (r"\approx \pm 1.32", "FY GGGG")
SRC_ODD = (r"-\cosh y = 2", "F TTTTF F F")
SRC_TAG = (r"\cosh(-y) = \cosh y", "TTTTFFFFF TTTTF")


def mt(src, pattern, size=SZ):
    """MathTex coloured glyph by glyph (one pattern letter per glyph; spaces ignored)."""
    m = MathTex(src, font_size=size)
    pat = pattern.replace(" ", "")
    assert len(m[0]) == len(pat), (src, len(m[0]), len(pat))
    for g, ch in zip(m[0], pat):
        g.set_color(COL[ch])
    return m


def at_eq(m, x, y):
    """Shift m so its "=" (glyph 1) is centred at (x, y)."""
    m.shift(np.array([x, y, 0]) - m[0][1].get_center())
    return m


# ---------------------------------------------------------------- handover builders
def xeq_line():
    """x = 2πm at its handover place (2πm BLUE)."""
    m = at_eq(mt(*SRC_X, size=FINAL_SZ), FINAL_EQ_X, FINAL_Y[0])
    m.rhs = VGroup(*m[0][2:5])
    return m


def yres_line():
    """y = ±ln(2 + √3) at its handover place (± YELLOW, ln(2 + √3) TEAL)."""
    m = at_eq(mt(*SRC_Y, size=FINAL_SZ), FINAL_EQ_X, FINAL_Y[1])
    m.pm, m.ln = m[0][2], VGroup(*m[0][3:12])
    return m


def handover_shot():
    """Last frame / ch4_s6_lattice's first: the card, x = 2πm over y = ±ln(2 + √3)."""
    return VGroup(ex35_card("top"), xeq_line(), yres_line())


# ---------------------------------------------------------------- illustrations
def strip(e1):
    """n = 0..3 → cos(nπ) = 1, −1, 1, −1, under cos(nπ)."""
    hn = MathTex("n", font_size=36, color=GREEN)
    hc = mt(r"\cos(n\pi)", "BBBFggF", 36)
    x0 = -3.4
    hn.move_to([x0, -1.75, 0], aligned_edge=RIGHT)
    hc.move_to([x0, -2.45, 0], aligned_edge=RIGHT)
    hn.align_to(hc, RIGHT)
    cols = []
    for k, v in enumerate(["1", "-1", "1", "-1"]):
        a = MathTex(str(k), font_size=36, color=GREEN).move_to([x0 + 0.85 + 0.95 * k, -1.75, 0])
        b = MathTex(v, font_size=36, color=GOLD).move_to([x0 + 0.85 + 0.95 * k, -2.45, 0])
        cols.append((a, b))
    return hn, hc, cols


def circle_thumb():
    c = np.array([3.4, -2.1, 0])
    r = 0.75
    circ = Circle(radius=r, color=BLUE, stroke_width=4).move_to(c)
    axis = Line(c + 1.1 * LEFT, c + 1.1 * RIGHT, color=DIM, stroke_width=2)
    one = MathTex("1", font_size=30, color=GOLD).next_to(c + r * RIGHT, DR, buff=0.08)
    mone = MathTex("-1", font_size=30, color=GOLD).next_to(c + r * LEFT, DL, buff=0.08)
    dot = Dot(c + r * RIGHT, radius=0.11, color=YELLOW)
    return c, circ, axis, one, mone, dot


def cosh_thumb():
    ax = Axes(x_range=[-2, 2, 1], y_range=[0, 4, 1], x_length=2.6, y_length=1.7, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": False})
    ax.move_to([4.9, -2.55, 0])
    lim = math.acosh(4.0)
    curve = ax.plot(math.cosh, x_range=[-lim, lim, 0.02], color=TEAL, stroke_width=4)
    one = DashedLine(ax.c2p(-2, 1), ax.c2p(2, 1), dash_length=0.08, color=DIM, stroke_width=2)
    lab = mt(r"\cosh y \ge 1", "TTTTFFG", 34).next_to(ax, UP, buff=0.25)
    return VGroup(ax, one, curve), lab


def big_cosh():
    """ch4_s3's cosh panel plot, scaled up, lower left."""
    p = S3.cosh_panel()
    plot = p.plot
    plot.scale(1.3)
    plot.shift(np.array([-3.0, -1.85, 0]) - p.axes.get_center())
    p.dots.set_color(GREEN)
    return p


def small_fig26():
    f = S1.fig26()
    f.scale(0.6)
    f.shift(np.array([1.1, -0.85, 0]) - f.ax.get_left())
    ax = f.ax
    # the figure's own labels (INV_C / PURPLE), back to 30 pt at ch3's spot
    for lab, y, d in ((f.lab_up, 3, UP), (f.lab_lo, -3, DOWN)):
        lab.scale(30 / (36 * 0.6))
        lab.next_to(ax.c2p(6.2, y), d, buff=0.18)
    f.vline = Line(ax.c2p(2, -2.3), ax.c2p(2, 2.3), color=YELLOW, stroke_width=4)
    f.two = MathTex("2", font_size=30, color=YELLOW).next_to(ax.c2p(2, -2.3), DOWN, buff=0.1)
    r = math.acosh(2.0)
    f.d_up = Dot(ax.c2p(2, r), radius=0.09, color=YELLOW)
    f.d_lo = Dot(ax.c2p(2, -r), radius=0.09, color=YELLOW)
    return f


def travel(cp, dst, k):
    """Copy flies at full opacity: it shows only once it has cleared its source line."""
    start = cp.copy().set_opacity(1)
    end = start.copy().scale(k).move_to(dst)

    def upd(m, t):
        m.become(start.copy().scale(1 + (k - 1) * t).move_to(
            interpolate(start.get_center(), end.get_center(), t)))
        m.set_opacity(min(1.0, max(0.0, (t - 0.2) / 0.12)))
    return UpdateFromAlphaFunc(cp, upd)


class Even(NarratedScene):
    def construct(self):
        h = S4.handover_shot()
        self.card, sysg, self.npi = h[0], h[1], h[2]
        self.sysg = sysg
        self.add(self.card, sysg.brace, sysg.l1, sysg.l2, self.npi)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.outro()

    # ------------------------------------------------------------ c4.even.1
    def clip1(self):
        sysg, npi = self.sysg, self.npi
        with self.say("c4.even.1") as c:
            e0 = mt(*SRC_E0, size=HZ).move_to(HERO)
            self.play(*fly(sysg.l1, e0, arc=-PI / 2.5), run_time=1.4)
            # substitute: x leaves, the rest opens up, nπ flies down from x = nπ
            e1 = mt(*SRC_E1, size=HZ).move_to(HERO)
            g0, g1 = e0[0], e1[0]
            moves = [g0[i].animate.move_to(g1[i]) for i in range(3)]
            moves += [g0[i].animate.move_to(g1[i + 3]) for i in range(4, 11)]
            parens = [g1[3].copy(), g1[6].copy()]
            fl = []
            for src_i, dst_i in ((2, 4), (3, 5)):
                cp = npi[0][src_i].copy().set_opacity(0)
                fl.append(cp)
            flights = [travel(cp, g1[d], HZ / SZ) for cp, d in zip(fl, (4, 5))]
            self.play(*during([FadeOut(g0[3], shift=0.2 * UP)], 0, 0.35),
                      *during(moves, 0.2, 0.7),
                      *during(flights, 0.25, 1.0),
                      *during([FadeIn(p) for p in parens], 0.65, 1.0),
                      run_time=min(1.8, c.until("cosine of")))
            self.remove(*e0.get_family(), *fl, *parens)
            self.add(e1)
            self.e = e1

            c.wait_until("cosine of")
            hn, hc, cols = strip(e1)
            cc, circ, axis, one, mone, dot = circle_thumb()
            self.play(*appear(hn, hc), FadeIn(circ), FadeIn(axis), run_time=1.0)
            self.play(*appear(*cols[0]), FadeIn(dot), *appear(one), run_time=0.9)
            for k in (1, 2, 3):
                extra = appear(mone) if k == 1 else []
                self.play(Rotate(dot, PI, about_point=cc), *appear(*cols[k]), *extra,
                          run_time=0.9 if k == 1 else 0.7)
                if k == 1:
                    self.wait(0.3)
            self.strip = [hn, hc, *[m for col in cols for m in col], circ, axis, one, mone, dot]

            c.wait_until("in short")
            e2 = mt(*SRC_E2, size=HZ).move_to(HERO)
            a, b = e1[0], e2[0]
            # cos, n, pi fade out while -1 and n fade in; the brackets and the rest slide
            outs = [FadeOut(a[i]) for i in (0, 1, 2, 4, 5)]
            ins = [FadeIn(b[i].copy()) for i in (1, 2, 4)]
            slides = [a[3].animate.move_to(b[0]), a[6].animate.move_to(b[3])]
            slides += [a[i].animate.move_to(b[i - 2]) for i in range(7, 14)]
            self.play(*during(outs, 0, 0.35), *during(slides, 0.12, 0.42), *during(ins, 0.28, 0.78),
                      run_time=1.5)
            self.remove(*e1.get_family(), *[x.mobject for x in ins])
            self.add(e2)
            self.e = e2

            c.wait_until("so minus one")
            self.play(FlashUnder(e2, color=YELLOW, run_time=1.5, time_width=1.5))
            self.play(*disappear(*self.strip), run_time=1.0)

    # ------------------------------------------------------------ c4.even.2
    def clip2(self):
        e = self.e
        g = e[0]
        y_sign = e.get_bottom()[1] - 0.45
        with self.say("c4.even.2") as c:
            c.wait_until("cosh is at least")
            thumb, tlab = cosh_thumb()
            self.play(FadeIn(thumb), *appear(tlab), run_time=1.2)
            c.wait_until("positive")
            pos = MathTex(r"> 0", font_size=40, color=GREEN).move_to([VGroup(*g[5:10]).get_x(), y_sign, 0])
            self.play(*appear(pos), run_time=1.0)

            c.wait_until("two is positive")
            two = MathTex(r"> 0", font_size=40, color=GREEN).move_to([g[11].get_x() + 0.1, y_sign, 0])
            self.play(*appear(two), run_time=1.0)

            c.wait_until("so what must")
            q = MathTex("?", font_size=48, color=YELLOW).move_to([VGroup(*g[0:5]).get_x(), y_sign, 0])
            self.play(*appear(q), FlashAround(VGroup(*g[0:5]), color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=1.5)  # early: the question mark is the question being asked

            c.wait_until("plus one")
            plus = MathTex(r"+1", font_size=40, color=GREEN).move_to(q)
            self.play(*swap(q, plus), run_time=1.0)

            c.wait_until("if n were odd")
            odd_l = MathTex(r"n\ \text{odd:}", font_size=40, color=FG)
            odd_l.move_to([-6.3, -2.25, 0], aligned_edge=LEFT)
            odd_e = mt(*SRC_ODD, size=44).next_to(odd_l, RIGHT, buff=0.5)
            odd_e.shift((odd_l[0][0].get_bottom()[1] - odd_e[0][1].get_bottom()[1]) * UP)
            self.play(*disappear(thumb, tlab), run_time=0.8)
            self.play(*appear(odd_l, odd_e), run_time=1.2)  # early: the case and its equation are one clause

            c.wait_until("never negative")
            cross = cross_mark().next_to(odd_e, RIGHT, buff=0.45)
            note_e = MathTex(r"\cosh y = -2", font_size=40, color=RED)
            note_t = T("impossible", 32, color=RED)
            note = VGroup(note_e, note_t).arrange(RIGHT, buff=0.25).next_to(cross, RIGHT, buff=0.45)
            note_t.align_to(note_e, DOWN)
            self.play(FadeIn(cross, scale=1.3), *appear(note), run_time=1.2)  # early: the reason is the "never negative" clause

            c.wait_until("so n must be even")
            even_l = MathTex(r"n\ \text{even:}", font_size=40, color=FG)
            even_l.move_to([-6.3, -3.15, 0], aligned_edge=LEFT)
            self.play(*set_alpha([odd_l, odd_e, cross, note], 0.4), *appear(even_l), run_time=1.2)

            c.wait_until("write it as")
            n2m = MathTex(r"n = 2m,\ m \in \mathbb{Z}", font_size=44, color=GREEN)
            n2m.next_to(even_l, RIGHT, buff=0.5).align_to(even_l, DOWN)
            self.play(*appear(n2m), run_time=1.2)
            self.even_l, self.n2m = even_l, n2m
            self.play(FlashAround(n2m, color=GREEN, run_time=1.4, time_width=1.5))

    # ------------------------------------------------------------ c4.even.3
    def clip3(self):
        sysg = self.sysg
        with self.say("c4.even.3") as c:
            sweep_clear(self, keep=[self.card, sysg.brace, self.even_l, self.n2m], run_time=1.4)

            c.wait_until("ex equals two pi")
            xl = mt(*SRC_X, size=SZ).move_to(sysg.l1, aligned_edge=LEFT)
            self.play(*during(disappear(self.even_l, self.n2m), 0, 0.45), *during(appear(xl), 0.4, 1.0),
                      run_time=1.4)

            c.wait_until("and cosh of why")
            cl = mt(*SRC_CY, size=SZ).move_to(sysg.l2, aligned_edge=LEFT)
            self.play(*appear(cl), run_time=1.0)
            self.xl, self.cl = xl, cl

            c.wait_until("for the second")
            inv = mt(*SRC_INV, size=WZ).move_to(WORK)
            derive(self, cl, inv, run_time=2.0)

            c.wait_until("with two as the input")
            gi = inv[0]
            under = VGroup(*gi[19:23])
            box = SurroundingRectangle(under, color=YELLOW, buff=0.08, stroke_width=3)
            self.play(FadeIn(box), FlashAround(under, color=YELLOW, run_time=1.4, time_width=1.5),
                      run_time=1.4)

            c.wait_until("which is three")
            inv2 = mt(*SRC_INV2, size=WZ).move_to(inv, aligned_edge=LEFT)
            a, b = inv[0], inv2[0]
            box2 = SurroundingRectangle(b[19], color=YELLOW, buff=0.1, stroke_width=3)
            three = [b[i].copy() for i in (17, 18, 19)]
            # 2^2 - 1 fades out as 3 fades in, the box closes onto it, the root and bracket follow
            self.play(*during([FadeOut(a[i]) for i in range(17, 23)], 0, 0.6),
                      *during([FadeIn(t) for t in three], 0.25, 0.85),
                      *during([Transform(box, box2), a[23].animate.move_to(b[20])], 0.1, 0.85),
                      run_time=1.5)
            self.remove(*inv.get_family(), *three)
            self.add(inv2)

            c.wait_until("that gives")
            about = mt(*SRC_ABOUT, size=WZ)
            yl = mt(*SRC_Y, size=WZ)
            row = VGroup(yl, about).arrange(RIGHT, buff=0.35).move_to(WORK)
            about.align_to(yl[0][0], DOWN)
            self.play(*disappear(box), run_time=0.6)
            self.play(*edit(inv2, yl), run_time=1.5)
            self.play(FlashAround(yl, color=TEAL, run_time=1.4, time_width=1.5))

            c.wait_until("about")
            self.play(*appear(about), run_time=1.0)
            self.yl, self.about = yl, about

    # ------------------------------------------------------------ c4.even.4
    def clip4(self):
        sysg, yl, about, cl = self.sysg, self.yl, self.about, self.cl
        with self.say("c4.even.4", gap=0.2) as c:
            # the result takes cosh y = 2's row in the system
            k = SZ / WZ
            yl.generate_target()
            yl.target.scale(k).move_to(sysg.l2, aligned_edge=LEFT)
            about.generate_target()
            about.target.scale(k)
            about.target.next_to(yl.target, RIGHT, buff=0.3).align_to(yl.target[0][0], DOWN)
            self.play(*during(disappear(cl), 0, 0.4),
                      *during([MoveToTarget(yl), MoveToTarget(about)], 0.35, 1.0),
                      run_time=1.5)
            p = big_cosh()
            ax = p.axes
            self.play(FadeIn(ax), *appear(p.ylab), Create(p.curve), FadeIn(p.two), *appear(p.lab),
                      FlashAround(yl[0][2], color=YELLOW, run_time=1.3, time_width=1.5), run_time=1.3)

            c.wait_until("non-negative")
            d_r, d_l = p.dots[1], p.dots[0]
            prin = T("principal", 30, color=GREEN).next_to(d_r, DR, buff=0.12)
            self.play(GrowFromCenter(d_r), run_time=0.8)
            c.wait_until(own_word=prin)
            self.play(*appear(prin), run_time=1.0)

            c.wait_until("any real number")
            axis_line = Line(ax.c2p(-2.2, 0), ax.c2p(2.2, 0)).set_stroke(YELLOW, 6)
            self.play(VShowPassingFlash(axis_line, time_width=0.6, run_time=1.6))

            c.wait_until("cosh is even")
            arr = CurvedDoubleArrow(d_r.get_center() + 0.15 * UP, d_l.get_center() + 0.15 * UP, angle=0.9,
                                    color=FG, stroke_width=3, tip_length=0.2)
            tag = mt(*SRC_TAG, size=34).next_to(ax, UP, buff=0.15)
            self.play(Create(arr), *appear(tag), run_time=1.5)

            c.wait_until("both give")
            drops = [DashedLine(d.get_center(), ax.c2p(s * math.acosh(2), 0), dash_length=0.08,
                                color=DIM, stroke_width=2) for d, s in ((d_l, -1), (d_r, 1))]
            ticks = [MathTex(t, font_size=30, color=GOLD).next_to(ax.c2p(s * math.acosh(2), 0), DOWN, buff=0.12)
                     for t, s in (("-1.32", -1), ("1.32", 1))]
            self.play(GrowFromCenter(d_l), *[Create(d) for d in drops], *appear(*ticks, lag=0.15),
                      run_time=1.3)

            c.wait_until("the line at height")
            f = small_fig26()
            self.play(FadeIn(f.ax), Create(f.upper), Create(f.lower), *appear(f.lab_up, f.lab_lo),
                      run_time=1.3)
            c.wait_until("crosses")
            self.play(GrowFromEdge(f.vline, DOWN), *appear(f.two),
                      GrowFromCenter(f.d_up), GrowFromCenter(f.d_lo), run_time=1.2)

            c.wait_until("keep only")
            lost = T("half the solutions lost", 32, color=RED).next_to(f.lab_lo, DOWN, buff=0.35)
            lost.set_x(f.ax.get_center()[0] + 1.3)
            grey = [f.lower, f.lab_lo, f.d_lo, d_l]
            self.play(*recolor(grey, DIM), *appear(lost), run_time=1.0)
            c.wait_until(None)
            back = [f.lower, f.lab_lo, f.d_lo, d_l, f.d_up, f.upper]
            self.play(*recolor(back, GREEN), run_time=min(1.2, c.until(None)))
            self.graphs = [ax, p.ylab, p.curve, p.two, p.lab, d_r, d_l, prin, arr, tag, *drops, *ticks,
                           f.ax, f.upper, f.lower, f.lab_up, f.lab_lo, f.vline, f.two, f.d_up, f.d_lo, lost]

    # ------------------------------------------------------------ handover
    def outro(self):
        self.wait(1.2)
        xl, yl = self.xl, self.yl
        xl.target = xeq_line()
        yl.target = yres_line()
        self.play(*during(disappear(*self.graphs, self.sysg.brace, self.about), 0, 0.45),
                  *during([MoveToTarget(xl), MoveToTarget(yl)], 0.4, 1.0), run_time=2.0)
        self.wait(1.0)
