"""Chapter 4, scene 4: two real equations, one dead end. Clips c4.cases.1 – c4.cases.4.

Opens on ch4_s3_split's handover_shot() (Example 35 card + the result line).
Exports: `system_group()` (the braced real/imaginary system, upper left), `npi_line()` (GREEN
x = nπ, n ∈ Z beside the system), `case_tree(right=..., steps=True)` (root sin x sinh y = 0, the
sinh y = 0 branch ending in a RED ∅, the sin x = 0 branch ending in a GREEN result; s7's recap
reuses it with right=r"x = 2\\pi m", steps=False), `handover_shot()` (card + system + x = nπ).
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

S3 = load_scene("ch4_s3_split")
S1 = load_scene("ch4_s1_hook")
ctex, grp, ex35_card, result_line = S3.ctex, S3.grp, S3.ex35_card, S3.result_line

SZ = 44                 # system / tree maths
RES_SZ = 60             # the result line
Y_RES = 1.55
SYS_Y = 0.85            # the system's centre (upper left)
CLIP1_K = 1.2           # the system's scale while it is built (clip 1)
CLIP1_POS = np.array([0.0, -1.25, 0])
AXIS_CFG = {"stroke_color": DIM, "stroke_width": 2, "include_ticks": True, "tick_size": 0.06}  # ch1_s2_define
ILL = np.array([-3.9, -2.05, 0])   # lower-left illustration spot (graph, wave, circle)

SRC_RHS = (r"\cos x \cosh y - i \sin x \sinh y = 2", "BBBF TTTTF F P BBBF TTTTF F F")
SRC_GHOST = (r"+\,0\,i", "DYP")
SRC_L1 = (r"\cos x \cosh y = 2", "BBBF TTTTF F F")
SRC_L2A = (r"-\sin x \sinh y = 0", "F BBBF TTTTF F F")
SRC_L2 = (r"\sin x \sinh y = 0", "BBBF TTTTF F F")
SRC_LB = (r"\sinh y = 0", "TTTTF F F")
SRC_RB = (r"\sin x = 0", "BBBF F F")
SRC_Y0 = (r"y = 0", "FFF")
SRC_C0 = (r"\cosh 0 = 1", "TTTTFFF")
SRC_CX = (r"\cos x = 2", "BBBFFF")


# ---------------------------------------------------------------- shared builders
def system_group():
    """The lecturer's braced system, upper left: cos x cosh y = 2 over sin x sinh y = 0."""
    l1, l2 = ctex(*SRC_L1, size=SZ), ctex(*SRC_L2, size=SZ)
    lines = VGroup(l1, l2).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
    brace = Brace(lines, LEFT, buff=0.2, color=FG)
    g = VGroup(brace, l1, l2)
    g.to_edge(LEFT, buff=0.6).set_y(SYS_Y)
    g.brace, g.l1, g.l2 = brace, l1, l2
    return g


def npi_line():
    """GREEN x = nπ, n ∈ Z, beside the real equation (handover position)."""
    m = MathTex(r"x = n\pi,\ n \in \mathbb{Z}", font_size=SZ, color=GREEN)
    sysg = system_group()
    m.next_to(sysg.l1, RIGHT, buff=1.1).align_to(sysg.l1, DOWN)
    return m


def case_tree(right=r"x = n\pi,\ n \in \mathbb{Z}", steps=True, center=np.array([2.6, 0.2, 0])):
    """The case tree. Attributes: .root .edges (left, right) .either .orr .lb .rb (branch
    equations) .steps (y = 0, cosh 0 = 1, cos x = 2; empty list if steps=False) .empty (RED ∅)
    .rres (GREEN right result). .left / .right: everything on that side (for dimming)."""
    c = np.array(center)
    root = ctex(*SRC_L2, size=SZ).move_to(c + np.array([0, 1.15, 0]))
    lb = ctex(*SRC_LB, size=SZ).move_to(c + np.array([-2.0, -0.5, 0]))
    rb = ctex(*SRC_RB, size=SZ).move_to(c + np.array([2.0, -0.5, 0]))
    e_l = Line(root.get_bottom() + 0.5 * LEFT + 0.15 * DOWN, lb.get_top() + 0.15 * UP,
               color=DIM, stroke_width=3)
    e_r = Line(root.get_bottom() + 0.5 * RIGHT + 0.15 * DOWN, rb.get_top() + 0.15 * UP,
               color=DIM, stroke_width=3)
    either = T("either", 30, color=DIM).next_to(e_l.get_center(), LEFT, buff=0.45)
    orr = T("or", 30, color=DIM).next_to(e_r.get_center(), RIGHT, buff=0.45)
    st = []
    if steps:
        y = lb.get_y()
        for i, src in enumerate((SRC_Y0, SRC_C0, SRC_CX)):
            st.append(ctex(*src, size=SZ).move_to([lb.get_x(), y - 0.72 * (i + 1), 0]))
        ey = y - 0.72 * 4
    else:
        ey = y_r = lb.get_y() - 0.95
    empty = MathTex(r"\emptyset", font_size=64, color=RED).move_to([lb.get_x(), ey, 0])
    rres = MathTex(right, font_size=SZ, color=GREEN).move_to([rb.get_x(), lb.get_y() - 0.8, 0])
    g = VGroup(root, e_l, e_r, either, orr, lb, rb, *st, empty, rres)
    g.root, g.edges, g.either, g.orr, g.lb, g.rb = root, (e_l, e_r), either, orr, lb, rb
    g.steps, g.empty, g.rres = st, empty, rres
    g.left = [e_l, either, lb, *st, empty]
    g.right = [e_r, orr, rb, rres]
    return g


def handover_shot():
    """Last frame / ch4_s5_even's first: the card, the braced system, GREEN x = nπ."""
    return VGroup(ex35_card("top"), system_group(), npi_line())


# ---------------------------------------------------------------- illustrations
def sinh_graph():
    ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-4, 4, 2], x_length=4.4, y_length=3.0, tips=False,
              axis_config=AXIS_CFG).move_to(ILL)
    hi = math.asinh(4)
    curve = ax.plot(math.sinh, x_range=[-hi, hi, 0.02], color=TEAL, stroke_width=5)
    lab = MathTex(r"\sinh y", font_size=36, color=TEAL).move_to(ax.c2p(-1.25, 2.6))
    ylab = MathTex("y", font_size=32, color=DIM).next_to(ax.c2p(2.2, 0), DOWN, buff=0.15)
    dot = Dot(ax.c2p(0, 0), radius=0.1, color=YELLOW)
    g = VGroup(ax, ylab, curve, lab)
    g.ax, g.ylab, g.curve, g.lab, g.dot = ax, ylab, curve, lab, dot
    return g


def wave_thumb():
    w = S1.wave_shot()
    b = w.band
    g = VGroup(w.ax, b.fill, b.dash_up, b.dash_lo, w.wave, w.line)
    g.scale_to_fit_width(5.0).move_to(ILL)
    two = MathTex("2", font_size=36, color=YELLOW).next_to(w.line, LEFT, buff=0.15)
    cos = MathTex(r"\cos x", font_size=34, color=BLUE).next_to(b.dash_lo, DOWN, buff=0.15)
    return VGroup(g, two, cos)


def unit_circle():
    r = 0.95
    circ = Circle(radius=r, color=BLUE, stroke_width=4).move_to(ILL)
    axis = Line(ILL + 1.4 * LEFT, ILL + 1.4 * RIGHT, color=DIM, stroke_width=2)
    d0 = Dot(ILL + r * RIGHT, radius=0.11, color=GREEN)
    dpi = Dot(ILL + r * LEFT, radius=0.11, color=GREEN)
    pos = MathTex(r"0,\ \pi,\ 2\pi,\ \ldots", font_size=36, color=FG).next_to(circ, UP, buff=0.25)
    neg = MathTex(r"-\pi,\ -2\pi,\ \ldots", font_size=36, color=FG).next_to(circ, DOWN, buff=0.25)
    return circ, axis, d0, dpi, pos, neg


def under_arrow(src, dst, color, angle):
    a = src.get_bottom() + 0.14 * DOWN
    b = dst.get_bottom() + 0.14 * DOWN
    return CurvedArrow(a, b, angle=angle, color=color, stroke_width=4, tip_length=0.2)


class Cases(NarratedScene):
    def construct(self):
        self.res0 = S3.handover_shot()
        self.card, self.old_res = self.res0[0], self.res0[1]
        self.add(self.res0)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)

    # ------------------------------------------------------------ c4.cases.1
    def clip1(self):
        with self.say("c4.cases.1") as c:
            res = ctex(*SRC_RHS, size=RES_SZ)
            ghost = ctex(*SRC_GHOST, size=RES_SZ).set_opacity(0.75)
            row = VGroup(res, ghost).arrange(RIGHT, buff=0.22)
            ghost.align_to(res, DOWN)
            row.move_to([0, Y_RES, 0])
            self.remove(self.res0)
            self.add(self.card, self.old_res)
            self.play(*edit(self.old_res, res), run_time=min(1.6, c.until("two complex numbers")))
            c.wait_until("their real parts")
            self.play(FlashUnder(grp(res, 0, 9), color=BLUE, run_time=1.5, time_width=1.5))
            c.wait_until("their imaginary parts")
            self.play(FlashUnder(grp(res, 9, 20), color=PINK, run_time=1.5, time_width=1.5))

            c.wait_until("zero")
            self.play(*appear(ghost, shift=None), run_time=1.0)
            self.play(FlashAround(ghost[0][1], color=YELLOW, run_time=1.4, time_width=1.5))

            # the system, built at clip-1 size below the line
            sysg = system_group()
            self.sys_final = sysg.get_center()
            sysg.scale(CLIP1_K).move_to(CLIP1_POS)
            l1, l2, brace = sysg.l1, sysg.l2, sysg.brace
            l2a = ctex(*SRC_L2A, size=SZ).scale(CLIP1_K)
            l2a.align_to(l1, LEFT).set_y(l2.get_y())

            c.wait_until("realeq")
            a1 = under_arrow(grp(res, 0, 9), res[0][21], FG, PI / 3)
            self.play(Create(a1), run_time=1.2)
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("imageq")
            a2 = under_arrow(grp(res, 11, 20), ghost[0][1], PINK, PI / 2)
            self.play(*during(disappear(a1), 0, 0.45), *during([Create(a2)], 0.4, 1), run_time=1.5)
            self.play(*appear(l2a), GrowFromCenter(brace), run_time=1.2)
            c.wait_until("drop")
            self.play(FlashAround(l2a[0][0], color=YELLOW, run_time=1.2, time_width=1.5))
            self.play(*edit(l2a, l2), run_time=min(1.5, c.until(None)))
            settle(self, sysg)
            self.res, self.ghost, self.a2, self.sysg = res, ghost, a2, sysg

    # ------------------------------------------------------------ c4.cases.2
    def clip2(self):
        sysg = self.sysg
        with self.say("c4.cases.2") as c:
            self.play(*during(disappear(self.res, self.ghost, self.a2), 0, 0.4),
                      *during([sysg.animate.scale(1 / CLIP1_K).move_to(self.sys_final)], 0.35, 1),
                      run_time=min(2.0, c.until("for two real unknowns")))
            note = T("2 equations, 2 unknowns: x, y", 34, t2s={"x": ITALIC, "y": ITALIC})
            note.next_to(sysg.l1, RIGHT, buff=1.4).align_to(sysg.l1, DOWN)
            c.wait_until("for two real unknowns")
            self.play(*appear(note), run_time=1.0)   # early: names the two lines just built
            c.wait_until("tip")
            tip = T("start with the one that equals 0", 34, color=YELLOW)
            tip.next_to(sysg.l2, RIGHT, buff=1.4).align_to(sysg.l2, DOWN).align_to(note, LEFT)
            self.play(*appear(tip), run_time=0.7)
            self.play(FlashAround(sysg.l2[0][-1], color=YELLOW, run_time=1.4, time_width=1.5))
            c.wait_until("a product is zero")
            self.play(*flash([grp(sysg.l2, 0, 4), grp(sysg.l2, 4, 9)], color=YELLOW, run_time=1.6,
                             time_width=1.5))

            c.wait_until("either")
            tree = case_tree()
            self.tree = tree
            self.play(*during(disappear(note, tip), 0, 0.45),
                      *during(fly(sysg.l2, tree.root), 0.35, 1), run_time=1.7)
            self.play(*appear(tree.lb, shift=0.3 * DOWN), GrowFromPoint(tree.edges[0], tree.edges[0].get_start()),
                      *appear(tree.either, shift=None), run_time=1.3)
            c.wait_until("or sine of ex")
            self.play(*appear(tree.rb, shift=0.3 * DOWN), GrowFromPoint(tree.edges[1], tree.edges[1].get_start()),
                      *appear(tree.orr, shift=None), run_time=1.3)
            c.wait_until("two cases")
            self.play(*flash([tree.lb, tree.rb], color=YELLOW, run_time=1.6, time_width=1.5))

    # ------------------------------------------------------------ c4.cases.3
    def clip3(self):
        tree = self.tree
        y0, c0, cx = tree.steps
        with self.say("c4.cases.3") as c:
            self.play(FlashAround(tree.lb, color=TEAL, run_time=1.5, time_width=1.5),
                      *set_alpha([tree.edges[1], tree.orr, tree.rb], 0.35), run_time=1.5)
            c.wait_until("graph")
            gr = sinh_graph()
            self.play(*appear(gr.ax, gr.ylab, shift=None), run_time=1.0)
            self.play(Create(gr.curve), *appear(gr.lab, shift=None), run_time=1.5)
            c.wait_until("at the origin")
            self.play(GrowFromCenter(gr.dot), run_time=0.8)
            self.play(FlashAround(gr.dot, color=YELLOW, run_time=1.4, time_width=1.5))
            c.wait_until("y0")
            self.play(*appear(y0), run_time=1.0)
            c.wait_until("sub")
            self.play(FlashAround(self.sysg.l1, color=YELLOW, run_time=1.6, time_width=1.5))
            c.wait_until("cosh of zero")
            self.play(*appear(c0), run_time=1.0)
            c.wait_until("so cosine of ex")
            self.play(*appear(cx), run_time=1.0)
            c.wait_until("dead")
            wave = wave_thumb()
            self.play(*swap(VGroup(gr, gr.dot), wave, shift=None), run_time=1.2)
            self.play(*appear(tree.empty, shift=None), FlashAround(tree.empty, color=RED, run_time=1.4,
                                                                   time_width=1.5), run_time=1.4)
            c.wait_until("so this case is empty")
            self.play(*set_alpha(tree.left, 0.35), run_time=1.0)
            self.wave = wave

    # ------------------------------------------------------------ c4.cases.4
    def clip4(self):
        tree = self.tree
        with self.say("c4.cases.4", gap=0) as c:
            self.play(*disappear(self.wave), *set_alpha([tree.edges[1], tree.orr, tree.rb], 1),
                      FlashAround(tree.rb, color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("circle")
            circ, axis, d0, dpi, pos, neg = unit_circle()
            self.play(Create(circ), Create(axis), run_time=1.3)
            c.wait_until("at zero")
            self.play(GrowFromCenter(d0), run_time=0.8)
            c.wait_until("at pi")
            self.play(GrowFromCenter(dpi), run_time=0.8)
            c.wait_until("at two pi")
            self.play(*appear(pos), run_time=1.0)
            c.wait_until("negative multiples")
            self.play(*appear(neg), run_time=1.0)
            c.wait_until("npi")
            xn = tree.rres
            self.play(*appear(xn), run_time=1.2)
            self.play(FlashAround(xn, color=GREEN, run_time=1.4, time_width=1.5))
            c.wait_until("alive")
            alive = T("still alive", 32, color=GREEN).next_to(xn, DOWN, buff=0.3)
            self.play(*appear(alive), run_time=0.7)   # early: tags the surviving case as it is said
            c.wait_until("feed")
            keep = {id(self.card), id(self.sysg), id(xn)}
            rest = [m for m in self.mobjects if id(m) not in keep]
            self.play(*during(disappear(*rest), 0, 0.45),
                      *during([xn.animate.move_to(npi_line().get_center())], 0.45, 1),
                      run_time=min(2.0, c.until(None)))
