"""Chapter 1, scene 5: reading a data-sheet timing diagram. Clips c1.sheet.1 – c1.sheet.3."""
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


# ============================================================================
# Data-sheet timing-diagram kit (shared spec: ch1_s2/s3, ch2–ch7 copy it)
# ============================================================================
WAVE_W = 4          # stroke of every trace
ROW_H = 0.8         # high-to-low height of a row
SLOPE = 0.35        # horizontal run of a sloped edge
GUIDE_W = 1.5       # thin grey guides
DIM_W = 3           # dimension arrows


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
    """One polyline clock trace from x0 to x1 centred on y; `edges` = x centres of every edge
    (alternating rise/fall from the start level). slope=0 gives the square L6 style."""
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [np.array([x0, level, 0])]
    for xc in edges:
        other = hi if level == lo else lo
        pts.append(np.array([xc - slope / 2, level, 0]))
        pts.append(np.array([xc + slope / 2, other, 0]))
        level = other
    pts.append(np.array([x1, level, 0]))
    wave = VMobject().set_points_as_corners(pts)
    wave.set_stroke(color, WAVE_W)
    return wave


def bus(x0, x1, y, crossings, h=ROW_H, color=BLUE):
    """A data row: two parallel lines (high and low) from x0 to x1 that swap through an X on each
    interval (a, b) in `crossings` (left to right; touching intervals make a hatched run).
    Returns a VGroup ordered left to right, with `.runs` (pairs of lines) and `.xs` (each X)."""
    lo, hi = y - h / 2, y + h / 2
    g = VGroup()
    g.runs, g.xs = [], []
    cur = x0
    for a, b in list(crossings) + [(x1, x1)]:
        if a - cur > 1e-3:
            run = VGroup(Line([cur, hi, 0], [a, hi, 0]), Line([cur, lo, 0], [a, lo, 0]))
            run.set_stroke(color, WAVE_W)
            g.add(run)
            g.runs.append(run)
        if b - a > 1e-3:
            x = VGroup(Line([a, hi, 0], [b, lo, 0]), Line([a, lo, 0], [b, hi, 0]))
            x.set_stroke(color, WAVE_W)
            g.add(x)
            g.xs.append(x)
        cur = b
    return g


def hatch(a, b, n):
    """n touching crossover intervals filling [a, b]: the settling run."""
    w = (b - a) / n
    return [(a + i * w, a + (i + 1) * w) for i in range(n)]


def guide(x, y_top, y_bot):
    """Thin grey vertical guide."""
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    """Dimension arrow: thin double-headed line from xa to xb at y, small tips, with a
    same-colour MathTex label above (UP) or below (DOWN). Returns VGroup(arrow, label)."""
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def sweep_in(group, x0, x1):
    """Draw every line of `group` left to right, as if a pen swept from x0 to x1."""
    leaves = group.family_members_with_points()
    origs = [m.copy() for m in leaves]

    def upd(_, a):
        X = x0 + a * (x1 - x0)
        for leaf, orig in zip(leaves, origs):
            lx0, lx1 = orig.get_left()[0], orig.get_right()[0]
            if lx1 - lx0 < 1e-6:
                frac = 1.0 if X >= lx0 else 0.0
            else:
                frac = min(1.0, max(0.0, (X - lx0) / (lx1 - lx0)))
            if a >= 1:
                frac = 1.0
            leaf.pointwise_become_partial(orig, 0, frac)
            # a zero-length partial renders as a stray dot (round cap): hide it until it has length
            leaf.set_stroke(opacity=orig.get_stroke_opacity() if frac * (lx1 - lx0) > 0.15 or frac >= 1
                            else 0)

    return UpdateFromAlphaFunc(group, upd)
# ============================================================================


def grow_dim(arr):
    """Grow a dim_arrow's DoubleArrow from its centre, rebuilt each frame at the true tip size
    (GrowFromCenter shrinks the tips into a lone arrowhead at the start). Ends exactly as built."""
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()
    min_len = 0.4

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        L = a * np.linalg.norm(end - start)
        if L < min_len:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)


def and_gate(left, y, color=FG):
    """A small AND gate body (0.8 x 0.8) with two input stubs, output at (left + 0.8, y)."""
    r = 0.4
    body = VGroup(
        Line([left, y + r, 0], [left + r, y + r, 0]),
        Arc(radius=r, start_angle=PI / 2, angle=-PI, arc_center=[left + r, y, 0]),
        Line([left + r, y - r, 0], [left, y - r, 0]),
        Line([left, y - r, 0], [left, y + r, 0]),
        Line([left - 0.3, y + 0.18, 0], [left, y + 0.18, 0]),
        Line([left - 0.3, y - 0.18, 0], [left, y - 0.18, 0]),
    )
    body.set_stroke(color, 3)
    return body


class Datasheet(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------- c1.sheet.1
        with self.say("c1.sheet.1") as c:
            ty = 2.3
            l_edges = [-5.3, -4.15, -3.0, -1.85]
            r_edges = [e + 7.4 for e in l_edges]
            sq_left = clock_wave(-6.0, -1.4, ty, l_edges, h=0.7, slope=0, color=FG)
            sq_right = clock_wave(1.4, 6.0, ty, r_edges, h=0.7, slope=0, color=FG)
            sl_right = clock_wave(1.4, 6.0, ty, r_edges, h=0.7, slope=0.3, color=FG)
            lec6 = T("lecture 6", 32, DIM).move_to([-3.7, 3.2, 0])
            dsheet = T("data sheet", 32, DIM).move_to([3.7, 3.2, 0])
            real = T("real edges take time", 30, YELLOW).move_to([3.7, 1.4, 0])

            self.play(Create(sq_left), run_time=1.5)
            c.wait_until("datasheet")
            self.play(*fly(sq_left, sq_right), run_time=1.5)
            self.play(*appear(dsheet))
            c.wait_until(own_word=lec6)
            self.play(*appear(lec6))
            c.wait_until("slope")
            self.play(Transform(sq_right, sl_right), run_time=1.6)
            c.wait_until(own_word=real)
            self.play(*appear(real))

        # ---------------------------------------------------------- c1.sheet.2
        with self.say("c1.sheet.2") as c:
            ry = -0.9
            busA = bus(-6.0, -2.4, ry, [], h=0.7)
            busB = bus(-2.4, -0.6, ry, [(-2.4, -2.0)], h=0.7)
            busC = bus(-0.6, 2.4, ry, hatch(-0.6, 1.4, 4), h=0.7)
            lblA = T("0 or 1:\nwe don't care which", 30).move_to([-4.2, -2.05, 0])
            tag = T("when, not what", 30, YELLOW, slant=ITALIC).move_to([-4.2, -3.0, 0])
            lblX = T("the value changes here", 30).move_to([-2.2, -0.05, 0])
            lblH = T("may change several times", 30).move_to([0.4, -1.85, 0])

            self.play(sweep_in(busA, -6.0, -2.4), run_time=1.6)
            c.wait_until("that means")
            self.play(*appear(lblA))
            c.wait_until("when")
            self.play(*appear(tag))
            c.wait_until("cross")
            self.play(sweep_in(busB, -2.4, -0.6), run_time=1.4)
            c.wait_until(own_word=lblX)
            self.play(*appear(lblX))
            c.wait_until("hatch")
            self.play(sweep_in(busC, -0.6, 2.4), run_time=1.8)
            c.wait_until(own_word=lblH)
            self.play(*appear(lblH))

            c.wait_until("glitch")
            gate = and_gate(3.3, ry)
            wire = VGroup(Line([4.1, ry, 0], [5.2, ry, 0]), Line([5.5, ry, 0], [6.5, ry, 0]))
            wire.set_stroke(FG, 3)
            spike = VMobject().set_points_as_corners(
                [[5.2, ry, 0], [5.25, ry + 0.6, 0], [5.45, ry + 0.6, 0], [5.5, ry, 0]])
            spike.set_stroke(RED, 4)
            haz = T("hazards", 30, DIM).move_to([4.9, -1.85, 0])
            self.play(*appear(VGroup(gate, wire), spike, haz, shift=None, lag=0.3),
                      run_time=min(1.4, c.until() * 0.4))
            arc = CurvedArrow([5.25, ry + 0.75, 0], [0.4, ry + 0.45, 0], angle=0.55,
                              color=RED, stroke_width=3, tip_length=0.18)
            self.play(Create(arc), run_time=min(1.2, c.until() * 0.6))

        # ---------------------------------------------------------- c1.sheet.3
        with self.say("c1.sheet.3") as c:
            c.wait_until("timing diagram")
            sweep_clear(self, run_time=min(1.2, c.until("clk")))

            yC, yQ, yD = 2.1, 0.4, -1.3
            X0, X1 = -4.6, 6.3
            e1, fall, e2 = -2.8, 0.7, 4.2
            xq = -1.6
            lab_x = -5.9
            clk = clock_wave(X0, X1, yC, [e1, fall, e2], color=YELLOW)
            clk_lab = T("CLK", 40, YELLOW).move_to([lab_x, yC, 0])
            g1, g2 = guide(e1, 3.25, -2.6), guide(e2, 3.25, -2.6)
            tc = dim_arrow(e1, e2, 3.05, YELLOW, "T_c")
            q0 = bus(X0, X1, yQ, [(xq - 0.2, xq + 0.2)], color=GREEN)
            q0_lab = MathTex("Q_0", font_size=48, color=GREEN).move_to([lab_x, yQ, 0])
            gq = guide(xq, yQ + 0.6, -2.6)
            tpc = dim_arrow(e1, xq, -2.4, PINK, "t_{pc}", label_dir=DOWN)
            d1 = bus(X0, X1, yD, hatch(fall, 2.7, 4) + [(3.1, 3.5)], color=BLUE)
            d1_lab = MathTex("D_1", font_size=48, color=BLUE).move_to([lab_x, yD, 0])

            c.wait_until("clk")
            self.play(*appear(clk_lab), sweep_in(clk, X0, X1), run_time=2.0)
            c.wait_until("tc")
            self.play(Create(g1), Create(g2), run_time=1.0)
            self.play(grow_dim(tc[0]), *appear(tc[1]), run_time=1.2)

            c.wait_until("q0")
            self.play(*appear(q0_lab), sweep_in(q0, X0, X1), run_time=1.8)
            c.wait_until("crosses over")
            self.play(Create(gq), FlashAround(q0.xs[0], color=PINK), run_time=1.2)
            c.wait_until("delay after")
            self.play(grow_dim(tpc[0]), *appear(tpc[1]), run_time=1.2)

            c.wait_until("d1")
            self.play(*appear(d1_lab), sweep_in(d1, X0, X1), run_time=2.0)

            c.wait_until("times")
            xs = d1.xs
            self.play(*[time_span(x.animate.set_color(YELLOW), 0.5 * i, 0.5 * i + 0.6)
                        for i, x in enumerate(xs)],
                      run_time=0.5 * (len(xs) - 1) + 0.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
