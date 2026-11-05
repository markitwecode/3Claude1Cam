"""Chapter 3, scene 3: a sum of cosines as the real part of a geometric sum, and its picture. Clips c3.sum.1 – c3.sum.4."""
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

# ---------------------------------------------------------------- shared helpers (ch3 s6, s7, s8 reuse them)
O = np.array([0.9, -1.0, 0.0])   # plane origin on screen
U = 1.15                         # screen units per plane unit
XR = (-0.7, 2.9)                 # plane extent (plane units)
YR = (-0.15, 3.85)
ROW = 0.30                       # vertical step between staggered shadow rows (screen units)
N6, TH6 = 6, PI / 6              # this scene's chain
# sum.4's own layout (the helpers' defaults above stay as s6/s7/s8 use them): a little higher and
# a little smaller, so the six shadow rows can sit far enough apart for readable labels.
O4 = np.array([1.1, -0.6, 0.0])
U4 = 1.05
ROW4 = 0.42


def P(x, y, origin=O, unit=U):
    return np.array(origin, dtype=float) + unit * np.array([x, y, 0.0])


def argand_plane(origin=O, unit=U, xr=XR, yr=YR):
    """ch2's Argand look (faint half-unit grid, FG axes at 0.7, MathTex Re/Im, DIM unit circle), cropped
    to xr × yr. The grid and the circle stay above the real axis when yr[0] > -0.5 (room for shadows)."""
    step = 0.5
    grid = VGroup()
    gy0 = max(yr[0], 0.0) if yr[0] > -0.5 else yr[0]
    for k in range(int(np.ceil(xr[0] / step)), int(np.floor(xr[1] / step)) + 1):
        if k:
            grid.add(Line(P(k * step, gy0, origin, unit), P(k * step, yr[1], origin, unit)))
    for k in range(int(np.ceil(gy0 / step)), int(np.floor(yr[1] / step)) + 1):
        if k:
            grid.add(Line(P(xr[0], k * step, origin, unit), P(xr[1], k * step, origin, unit)))
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow(P(xr[0], 0, origin, unit), P(xr[1], 0, origin, unit), **ax_kw).set_opacity(0.7)
    y_ax = Arrow(P(0, yr[0], origin, unit), P(0, yr[1], origin, unit), **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}", font_size=34, color=DIM).next_to(x_ax.get_end(), UP, buff=0.12).shift(0.2 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    if yr[0] > -0.5:
        circle = Arc(radius=unit, start_angle=0, angle=PI, arc_center=np.array(origin, dtype=float),
                     color=DIM, stroke_width=2.5)
    else:
        circle = Circle(radius=unit, color=DIM, stroke_width=2.5).move_to(origin)
    g = VGroup(grid, x_ax, y_ax, circle, re, im)
    g.grid, g.axes, g.circle, g.re, g.im = grid, VGroup(x_ax, y_ax), circle, re, im
    return g


def chain_points(n, theta, start=0.0, r=1.0, origin=O, unit=U):
    """Tip-to-tail points of the arrows r^k e^{i(start + k theta)}, k = 0..n-1 (n+1 points)."""
    pts = [np.array(origin, dtype=float)]
    for k in range(n):
        a = start + k * theta
        pts.append(pts[-1] + unit * (r ** k) * np.array([np.cos(a), np.sin(a), 0.0]))
    return pts


def _arrow(a, b, color, width=6, tip=0.24):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.3)


def unit_chain(n, theta, start=0.0, r=1.0, origin=O, unit=U, color=GOLD):
    """GOLD arrows e^{ik theta} (times r^k, turned by start) tip to tail from origin; .pts (points), .end."""
    pts = chain_points(n, theta, start, r, origin, unit)
    g = VGroup(*[_arrow(pts[k], pts[k + 1], color) for k in range(n)])
    g.pts, g.end = pts, pts[-1]
    return g


def chain_shadow(n, theta, start=0.0, r=1.0, origin=O, unit=U, row=ROW, color=BLUE):
    """Each arrow's shadow on the real axis, BLUE, end to end in x; staggered one row below the
    axis per arrow (row=0: all on the axis). A zero-length shadow is a dot."""
    pts = chain_points(n, theta, start, r, origin, unit)
    y0 = np.array(origin, dtype=float)[1]
    g = VGroup()
    for k in range(n):
        y = y0 - row * (k + 1)
        a, b = np.array([pts[k][0], y, 0]), np.array([pts[k + 1][0], y, 0])
        if abs(b[0] - a[0]) < 0.08:
            g.add(Dot(a, radius=0.06, color=color))
        else:
            g.add(_arrow(a, b, color, width=5, tip=0.16))
    g.pts = pts
    return g


def shadow_labels(n, theta_tex=r"\theta", origin=O, row=ROW, size=28):
    """1, cos θ, cos 2θ, … right-aligned just left of the origin, one per shadow row."""
    g = VGroup()
    for k in range(n):
        tex = "1" if k == 0 else (rf"\cos{theta_tex}" if k == 1 else rf"\cos {k}{theta_tex}")
        m = MathTex(tex, font_size=size, color=BLUE)
        m.move_to([0, np.array(origin)[1] - row * (k + 1), 0]).align_to(np.array(origin) + 0.25 * LEFT, RIGHT)
        g.add(m)
    return g


def turn_marks(pts, theta, start=0.0, radius=0.38, ext=0.6):
    """At each joint: a DIM dashed continuation of the previous arrow and a YELLOW arc of theta."""
    marks = []
    for k in range(1, len(pts) - 1):
        a0 = start + (k - 1) * theta
        d = DashedLine(pts[k], pts[k] + ext * np.array([np.cos(a0), np.sin(a0), 0]), color=DIM,
                       stroke_width=2, dash_length=0.07)
        arc = Arc(radius=radius, start_angle=a0, angle=theta, arc_center=pts[k], color=YELLOW, stroke_width=4)
        marks.append(VGroup(d, arc))
    return marks


# ---------------------------------------------------------------- scene
class Sum(NarratedScene):
    def construct(self):
        # ---------------- clip 1: the sum, written out
        with self.say("c3.sum.1") as c:
            c.wait_until("sigma")
            A = MathTex("S_N", "=", r"\sum_{k=0}^{N-1}", r"\cos k\theta", font_size=60).move_to([0, 2.5, 0])
            A[3].set_color(BLUE)
            self.play(*appear(A), run_time=min(1.2, c.until("written")))
            c.wait_until("written")
            B = MathTex("=", "1", "+", r"\cos\theta", "+", r"\cos 2\theta", "+", r"\cdots", "+",
                        r"\cos(N-1)\theta", font_size=54).move_to([0, 0.9, 0])
            for i in (3, 5, 9):
                B[i].set_color(BLUE)
            self.play(*appear(B), run_time=1.5)
            self.A, self.B = A, B

        # ---------------- clip 2: each cosine is a real part
        with self.say("c3.sum.2") as c:
            A, B = self.A, self.B
            c.wait_until("each cosine")
            self.play(*flash([B[3], B[5], B[9]], color=BLUE), run_time=1.5)
            c.wait_until("cosk")
            C = MathTex(r"\cos k\theta", "=", r"\mathrm{Re}", r"\big[", r"e^{ik\theta}", r"\big]",
                        font_size=54).move_to([0, -0.9, 0])
            C[0].set_color(BLUE)
            C[2].set_color(BLUE)
            self.play(*appear(C), run_time=1.2)
            c.wait_until("swap")
            A2 = MathTex("S_N", "=", r"\mathrm{Re}", r"\Big[", r"\sum_{k=0}^{N-1}", r"e^{ik\theta}", r"\Big]",
                         font_size=60).move_to([0, 2.5, 0])
            A2[2].set_color(BLUE)
            self.play(*during(disappear(B), 0, 0.4), *edit(A, A2), run_time=min(1.8, c.until("eq")))
            c.wait_until("eq")
            tag = MathTex("(79)", font_size=34, color=DIM).next_to(A2, RIGHT, buff=0.6)
            self.play(*appear(tag), run_time=1.0)
            self.A2, self.C, self.tag = A2, C, tag

        # ---------------- clip 3: the inside is a geometric progression
        with self.say("c3.sum.3", gap=1.3) as c:
            A2, C, tag = self.A2, self.C, self.tag
            self.play(FlashAround(VGroup(A2[4], A2[5]), run_time=1.5, time_width=1.5),
                      *disappear(C), *set_alpha([tag], 0.5), run_time=1.5)
            c.wait_until("terms")
            D = MathTex("1", "+", r"e^{i\theta}", "+", r"e^{2i\theta}", "+", r"e^{3i\theta}", "+", r"\cdots",
                        font_size=60).move_to([0, 0.75, 0])
            self.play(*appear(D), run_time=1.5)
            c.wait_until("times")
            terms = [D[0], D[2], D[4], D[6]]
            yb = D.get_bottom()[1] - 0.12
            hops, labs = [], []
            for a, b in zip(terms, terms[1:]):
                arr = CurvedArrow([a.get_x() + 0.05, yb, 0], [b.get_x() - 0.05, yb, 0], angle=PI / 2,
                                  color=GOLD, stroke_width=3, tip_length=0.16)
                lab = MathTex(r"\times e^{i\theta}", font_size=36, color=GOLD).next_to(arr, DOWN, buff=0.16)
                hops.append(arr)
                labs.append(lab)
            # labels fade in where they sit (no drop): a drop from above would pass through the hops
            self.play(Create(hops[0]), *appear(labs[0], shift=None), run_time=1.2)
            self.play(*[Create(h) for h in hops[1:]], *appear(*labs[1:], shift=None, lag=0.3), run_time=1.2)  # early: the same hop, repeated
            E = MathTex("=", r"\sum_{k=0}^{N-1}", r"\big(e^{i\theta}\big)^k", font_size=56).move_to([-2.8, -2.2, 0])
            E[2].set_color(GOLD)
            self.play(*appear(E), run_time=min(1.0, c.until("gp")))  # early: the progression form, read with {gp}
            c.wait_until("gp")
            t1 = T("geometric progression", size=40, color=YELLOW)
            t2a = T("first term", size=36)
            t2 = VGroup(t2a, MathTex("1", font_size=44)).arrange(RIGHT, buff=0.2)
            t3a = T("common ratio", size=36)
            t3 = VGroup(t3a, MathTex(r"e^{i\theta}", font_size=44, color=GOLD)).arrange(RIGHT, buff=0.2)
            tags = VGroup(t1, t2, t3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, -2.2, 0])
            self.play(*appear(t1), run_time=1.0)
            c.wait_until(own_word=t2a)
            self.play(*appear(t2), run_time=1.0)
            c.wait_until(own_word=t3a)
            self.play(*appear(t3), run_time=1.0)

        # ---------------- clip 4: the picture: a chain of unit arrows and its shadow
        with self.say("c3.sum.4", gap=2.3) as c:
            A2 = self.A2
            plane = argand_plane(origin=O4, unit=U4)
            chain = unit_chain(N6, TH6, origin=O4, unit=U4)
            pts = chain.pts
            A2.generate_target()
            A2.target.scale(0.72).move_to([-4.0, 2.6, 0])
            sweep_clear(self, MoveToTarget(A2), FadeIn(plane), keep=[A2], run_time=1.6)
            c.wait_until("arrow of length one")
            self.play(GrowArrow(chain[0]), run_time=1.2)
            c.wait_until("tip to tail")
            self.play(GrowArrow(chain[1]), run_time=1.0)
            c.wait_until("six")
            nt = MathTex(r"N = 6,\quad \theta = \tfrac{\pi}{6}", font_size=44).move_to([-4.0, 1.2, 0])
            self.play(LaggedStart(*[GrowArrow(a) for a in chain[2:]], lag_ratio=0.5), *appear(nt),
                      run_time=min(2.2, c.until("curl")))
            c.wait_until("curl")
            marks = turn_marks(pts, TH6)
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.4), run_time=2.2)
            c.wait_until("end")
            dot = Dot(pts[-1], radius=0.11, color=YELLOW)
            end_lab = MathTex(r"\sum e^{ik\theta}", font_size=40, color=YELLOW)
            end_lab.next_to(dot, RIGHT, buff=0.55)   # clear of the last arrow, which rises into the dot
            set_backstroke(end_lab)
            self.play(*disappear(*marks), FadeIn(dot, scale=0.5), *appear(end_lab), run_time=1.2)
            c.wait_until("shadow")
            shadow = chain_shadow(N6, TH6, origin=O4, unit=U4, row=ROW4)
            self.play(LaggedStart(*[ReplacementTransform(a.copy(), s) for a, s in zip(chain, shadow)],
                                  lag_ratio=0.35), run_time=min(3.0, c.until("shadow of an arrow")))
            c.wait_until("shadow of an arrow")
            labs = shadow_labels(N6, origin=O4, row=ROW4, size=34)
            for lab, sh in zip(labs, shadow):   # each label just right of its own shadow, on its row
                lab.next_to([sh.get_right()[0], sh.get_y(), 0], RIGHT, buff=0.18)   # (clear of the drop line)
            self.play(*appear(*labs, lag=0.3), run_time=1.8)  # early: the row labels are read as a list
            c.wait_until("total")
            end_x = pts[-1][0]
            low = O4[1] - ROW4 * N6
            drop = DashedLine(pts[-1], [end_x, low - 0.1, 0], color=BLUE, stroke_width=2, dash_length=0.08)
            br = span_brace(O4 + [0, low - O4[1], 0], np.array([end_x, low, 0]), direction=DOWN, color=BLUE,
                            buff=0.12)
            sn = MathTex("S_N", font_size=48, color=BLUE).next_to(br, RIGHT, buff=0.25).align_to(br, UP)
            self.play(Create(drop), GrowFromCenter(br), *during(appear(sn), 0.4, 1.0), run_time=1.4)
            self.play(FlashAround(A2[0], color=BLUE, time_width=1.5), run_time=1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
