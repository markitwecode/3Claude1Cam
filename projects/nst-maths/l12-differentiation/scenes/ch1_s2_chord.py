"""Chapter 1, scene 2: from chord to tangent line. Clips c1.chord.1 – c1.chord.5.

Exports (the series' recurring Figure 29 and the boxed definition (103)):

figure29(dx=0.5, tangent=False, chord=True, braces=True, q_labels=None, x0=1.0) -> VGroup
    Built at full size in absolute position (axes origin at FIG_ORIGIN = (-5.6, -3, 0); x in
    [0, 1.8] over 7 units, y in [0, 5] over 6 units). Bounding box about x -5.9..1.8, y -3.5..3.6.
    Callers scale / move the whole group. Parts (attributes; None when switched off):
      .axes        Axes (DIM, no ticks, tips)
      .xlab .ylab  MathTex "x" at the x-axis end, "y(x)" above the y-axis
      .curve       BLUE y = x^3, x in [0, 1.7]
      .p_dot .p_drop .p_lab    YELLOW dot at x0, DIM dashed drop line, "x" under the axis
      .q_dot                   YELLOW dot at x0 + dx
      .q_drop .q_lab           dashed drop and "x + \\delta x" (q_labels; default dx >= 0.25)
      .run_leg .rise_leg .right_angle   the dashed right-angle corner (braces)
      .run_brace .run_lab      TEAL brace under the run, "\\delta x"           (braces)
      .rise_brace .rise_lab    TEAL brace right of the rise,
                               "\\delta y = y(x+\\delta x) - y(x)" (5 parts)    (braces)
      .chord .chord_lab        TEAL chord through both dots (1.1 back, 4.2 forward of P), "chord"
      .tangent .tangent_lab    GREEN tangent at x0 (same extent), "tangent"   (tangent=True)
    Helpers: chord_line(axes, dx, x0), tangent_line(axes, x0), chord_label_pos(axes, dx, x0),
    corner_tag() (the "y = x^3, at x = 1" tag: MathTex size 36, FG, to_corner(UR, buff=0.5)).

definition_box(size=44, right_pad=0.95) -> VGroup(rect, formula, num)
      .formula  MathTex parts [dy/dx, =, lim, (y(x+dx)-y(x))/dx, =, lim, dy/dx-quotient]
                (\\delta x, \\delta y isolated and TEAL; part 0 GREEN; select(formula, r"\\delta y"))
      .rect     YELLOW box (stroke 3), extra room on the right (right_pad) for "-> 0" labels
      .num      "(103)" DIM T 28 just above the box's top-right corner
    Built centred on ORIGIN.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

FIG_ORIGIN = np.array([-5.6, -3.0, 0.0])
BACK, FWD = 1.1, 4.2          # chord/tangent extent from P, screen units


def tx(s, size=40, color=FG, iso=(), colors=None):
    """MathTex with isolated substrings coloured."""
    parts = s if isinstance(s, (list, tuple)) else [s]
    m = MathTex(*parts, font_size=size, color=color, substrings_to_isolate=list(iso) or None)
    for k, c in (colors or {}).items():
        m.set_color_by_tex(k, c)
    return m


def _f(x):
    return x ** 3


def _pt(axes, x):
    return axes.c2p(x, _f(x))


def _line_through(p, d, color):
    d = d / np.linalg.norm(d)
    return Line(p - BACK * d, p + FWD * d, color=color, stroke_width=4)


def chord_line(axes, dx, x0=1.0):
    p, q = _pt(axes, x0), _pt(axes, x0 + dx)
    return _line_through(p, q - p, TEAL)


def tangent_line(axes, x0=1.0):
    p = _pt(axes, x0)
    d = axes.c2p(x0 + 1, _f(x0) + 3 * x0 ** 2) - axes.c2p(x0, _f(x0))
    return _line_through(p, d, GREEN)


def _dir_norm(axes, dx, x0):
    p, q = _pt(axes, x0), _pt(axes, x0 + dx)
    d = (q - p) / np.linalg.norm(q - p)
    return p, d, np.array([-d[1], d[0], 0.0])


def chord_label_pos(axes, dx, x0=1.0):
    p, d, n = _dir_norm(axes, dx, x0)
    return p + (FWD - 0.5) * d - 0.95 * n


def corner_tag():
    return MathTex(r"y = x^3,\ \text{at}\ x = 1", font_size=36, color=FG).to_corner(UR, buff=0.5)


def figure29(dx=0.5, tangent=False, chord=True, braces=True, q_labels=None, x0=1.0):
    if q_labels is None:
        q_labels = dx >= 0.25
    g = VGroup()
    axes = Axes(x_range=[0, 1.8, 2], y_range=[0, 5, 10], x_length=7, y_length=6, tips=True,
                axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3})
    axes.shift(FIG_ORIGIN - axes.c2p(0, 0))
    g.axes = axes
    g.xlab = MathTex("x", font_size=40).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
    g.ylab = MathTex("y(x)", font_size=40).next_to(axes.y_axis.get_end(), UP, buff=0.12)
    g.curve = axes.plot(_f, x_range=[0, 1.7], color=BLUE, stroke_width=5)
    P, Q = _pt(axes, x0), _pt(axes, x0 + dx)
    C = axes.c2p(x0 + dx, _f(x0))
    g.p_drop = DashedLine(P, axes.c2p(x0, 0), color=DIM, dash_length=0.1, stroke_width=3)
    g.p_dot = Dot(P, radius=0.09, color=YELLOW)
    g.q_dot = Dot(Q, radius=0.09, color=YELLOW)
    g.q_drop = g.q_lab = None
    if q_labels:
        g.q_drop = DashedLine(Q, axes.c2p(x0 + dx, 0), color=DIM, dash_length=0.1, stroke_width=3)
        g.q_lab = tx(r"x + \delta x", 40, iso=[r"\delta x"], colors={r"\delta x": TEAL})
        g.q_lab.next_to(axes.c2p(x0 + dx, 0), DOWN, buff=0.22)
    g.p_lab = MathTex("x", font_size=40).next_to(axes.c2p(x0, 0), DOWN, buff=0.22)
    if g.q_lab is not None:
        g.p_lab.align_to(g.q_lab, DOWN)
    for k in ("run_leg", "rise_leg", "right_angle", "run_brace", "run_lab", "rise_brace", "rise_lab"):
        setattr(g, k, None)
    if braces:
        g.run_leg = DashedLine(P, C, color=DIM, dash_length=0.1, stroke_width=3)
        g.rise_leg = DashedLine(C, Q, color=DIM, dash_length=0.1, stroke_width=3)
        s = 0.2
        g.right_angle = VMobject(color=DIM, stroke_width=2).set_points_as_corners(
            [C + s * LEFT, C + s * LEFT + s * UP, C + s * UP])
        g.run_brace = Brace(Line(P, C), DOWN, buff=0.1, color=TEAL)
        g.run_lab = tx(r"\delta x", 40, TEAL).next_to(g.run_brace, DOWN, buff=0.1)
        g.rise_brace = Brace(Line(C, Q), RIGHT, buff=0.1, color=TEAL)
        g.rise_lab = tx([r"\delta y", "=", r"y(x+\delta x)", "-", "y(x)"], 40,
                        iso=[r"\delta x", r"\delta y"],
                        colors={r"\delta x": TEAL, r"\delta y": TEAL})
        g.rise_lab.next_to(g.rise_brace, RIGHT, buff=0.15)
    g.chord = g.chord_lab = None
    if chord:
        g.chord = chord_line(axes, dx, x0)
        g.chord_lab = T("chord", 34, TEAL).move_to(chord_label_pos(axes, dx, x0))
    g.tangent = g.tangent_lab = None
    if tangent:
        g.tangent = tangent_line(axes, x0)
        p, d, n = _dir_norm(axes, 1e-6, x0)
        g.tangent_lab = T("tangent", 34, GREEN).move_to(p + 3.3 * d - 1.0 * n)
    order = ["axes", "xlab", "ylab", "curve", "p_drop", "q_drop", "run_leg", "rise_leg",
             "right_angle", "run_brace", "run_lab", "rise_brace", "rise_lab", "chord", "tangent",
             "chord_lab", "tangent_lab", "p_lab", "q_lab", "p_dot", "q_dot"]
    for k in order:
        m = getattr(g, k)
        if m is not None:
            g.add(m)
    return g


def definition_box(size=44, right_pad=0.95):
    f = tx([r"\frac{dy}{dx}", "=", r"\lim_{\delta x \to 0}", r"\frac{y(x+\delta x) - y(x)}{\delta x}",
            "=", r"\lim_{\delta x \to 0}", r"\frac{\delta y}{\delta x}"], size,
           iso=[r"\delta x", r"\delta y"], colors={r"\delta x": TEAL, r"\delta y": TEAL})
    f[0].set_color(GREEN)
    f.move_to(ORIGIN)
    pad = 0.35
    rect = Rectangle(width=f.width + pad + right_pad, height=f.height + 2 * pad,
                     color=YELLOW, stroke_width=3)
    rect.move_to(f.get_center() + (right_pad - pad) / 2 * RIGHT)
    num = T("(103)", 28, DIM).next_to(rect.get_corner(UR), UP, buff=0.1).align_to(rect, RIGHT)
    g = VGroup(rect, f, num)
    g.rect, g.formula, g.num = rect, f, num
    g.shift(-g[0].get_center())
    return g


def slope_row(dx_s, slope_s, color=None):
    r = tx([rf"\delta x = {dx_s}:", r"\quad \text{slope}\ ", slope_s], 38, iso=[r"\delta x"],
           colors={r"\delta x": TEAL})
    r[2].set_color(color or GOLD)
    return r


RD_FRAC = np.array([4.4, 2.2, 0])
RD_ROW = np.array([4.4, 1.0, 0])
TABLE_X = 4.5                 # the slope table's centre x
ROW_DIM = 0.5                 # earlier rows of the table


class ChordToTangent(NarratedScene):
    def construct(self):
        fig = figure29(dx=0.5, tangent=True)
        self.fig = fig
        ax = fig.axes

        # ---------------- c1.chord.1: curve, point, step, rise
        with self.say("c1.chord.1") as c:
            self.play(Create(ax), *appear(fig.xlab, fig.ylab), run_time=1.5)
            c.wait_until("drawn")
            self.play(Create(fig.curve), run_time=1.8)
            c.wait_until("point")
            self.play(GrowFromCenter(fig.p_dot), Create(fig.p_drop), run_time=1.0)
            c.wait_until("at ex")
            self.play(*appear(fig.p_lab), run_time=0.9)
            c.wait_until("small amount")
            self.play(Create(fig.run_leg), GrowFromCenter(fig.run_brace), run_time=1.2)
            c.wait_until("delta ex")
            self.play(*appear(fig.run_lab), run_time=0.9)
            c.wait_until("second point")
            self.play(GrowFromCenter(fig.q_dot), Create(fig.q_drop), run_time=1.0)
            c.wait_until("plus delta")
            self.play(*appear(fig.q_lab), run_time=0.9)
            c.wait_until("rise")
            rl = fig.rise_lab
            self.play(Create(fig.rise_leg), Create(fig.right_angle), GrowFromCenter(fig.rise_brace),
                      run_time=1.2)
            self.play(*appear(rl[0]), run_time=0.8)
            c.wait_until("the height")
            self.play(*appear(rl[1], rl[2]), run_time=1.0)
            c.wait_until("minus")
            self.play(*appear(rl[3], rl[4]), run_time=0.9)
            settle(self, rl)

        # ---------------- c1.chord.2: chord, slope readout, example values
        with self.say("c1.chord.2") as c:
            self.play(Create(fig.chord), run_time=1.5)
            c.wait_until(own_word=fig.chord_lab)
            self.play(*appear(fig.chord_lab), run_time=0.9)
            c.wait_until("rise over")
            self.play(FlashAround(rl[0], time_width=1.5), FlashAround(fig.run_lab, time_width=1.5),
                      run_time=1.5)
            frac = tx(r"\frac{\delta y}{\delta x}", 52, TEAL).move_to(RD_FRAC)
            c.wait_until("delta why over")
            self.play(*appear(frac), run_time=1.0)
            tag = corner_tag()
            c.wait_until("why equals")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("half")
            # the slope table: one row per delta x, earlier rows dimmed, the limit row last
            row = slope_row("0.5", "4.75")
            row2 = slope_row("0.1", "3.31")
            row3 = slope_row("0.01", "3.03")
            row_g = tx([r"\delta x \to 0:", r"\quad \text{slope}\ ", "3"], 38, GREEN,
                       iso=[r"\delta x"], colors={r"\delta x": TEAL})
            table = VGroup(row, row2, row3, row_g).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            table.shift((TABLE_X - table.get_x()) * RIGHT + (RD_ROW[1] - row.get_y()) * UP)
            self.table = table
            self.play(*appear(row[0]), run_time=0.9)
            c.wait_until("four point")
            self.play(*appear(row[1], row[2]), run_time=1.0)
            settle(self, row)

            c.wait_until("tenth")
            clutter = [fig.run_brace, fig.run_lab, fig.rise_brace, rl, fig.run_leg, fig.rise_leg,
                       fig.right_angle, fig.q_drop, fig.q_lab]
            self.play(*during(disappear(*clutter), 0, 0.3), *during(self.swing(0.5, 0.1), 0.2, 1.0),
                      *during(set_alpha([row], ROW_DIM), 0.3, 0.7),
                      *during(appear(row2), 0.35, 0.8), run_time=2.2)
            c.wait_until("hundredth")
            self.play(*self.swing(0.1, 0.01), *during(set_alpha([row2], ROW_DIM), 0.3, 0.7),
                      *during(appear(row3), 0.35, 0.8), run_time=1.8)

        # ---------------- c1.chord.3: settle on the tangent, the derivative, the definition
        with self.say("c1.chord.3") as c:
            ghosts = VGroup(*[chord_line(ax, d).set_stroke(opacity=0.3) for d in (0.5, 0.25, 0.1)])
            P = _pt(ax, 1.0)
            a0 = np.arctan2(*(_dir_norm(ax, 0.5, 1.0)[1][[1, 0]]))
            a1 = np.arctan2(*(_dir_norm(ax, 1e-6, 1.0)[1][[1, 0]]))
            arc = Arc(radius=3.0, start_angle=a0, angle=a1 - a0, arc_center=P, color=TEAL,
                      stroke_width=4)
            arc.add_tip(tip_length=0.22, tip_width=0.22)
            arc_lab = tx(r"\delta x \to 0", 36, TEAL)
            arc_lab.next_to(arc.get_start(), LEFT, buff=0.45).shift(0.3 * UP)   # left of the arc, clear of the table
            self.play(FadeIn(ghosts), Create(arc), run_time=1.5)
            self.play(*appear(arc_lab), run_time=0.9)
            c.wait_until("settle")
            self.play(ReplacementTransform(fig.chord, fig.tangent), FadeOut(fig.q_dot),
                      fig.chord_lab.animate.set_opacity(0), run_time=2.0)
            self.remove(fig.chord_lab)
            _, d_t, n_t = _dir_norm(ax, 1e-6, 1.0)
            fig.tangent_lab.move_to(P + 2.6 * d_t - 0.95 * n_t)   # below the line, clear of the table
            c.wait_until(own_word=fig.tangent_lab)
            self.play(*appear(fig.tangent_lab), run_time=1.0)
            c.wait_until("here its slope")
            row, row2, row3, row_g = self.table
            self.play(*set_alpha([row3], ROW_DIM), *during(appear(row_g), 0.2, 1.0), run_time=1.3)
            c.wait_until("derivative")
            deriv = T("the derivative", 36, GREEN).next_to(row_g, DOWN, buff=0.35)
            self.play(*appear(deriv), run_time=1.0)

            c.wait_until("box")
            figg = VGroup(ax, fig.xlab, fig.ylab, fig.curve, fig.p_drop, ghosts, fig.tangent,
                          fig.tangent_lab, fig.p_lab, fig.p_dot)
            self.remove(*figg.get_family())
            self.add(figg)
            self.fig_small = figg
            self.labs = {fig.xlab: [40, 1.0], fig.ylab: [40, 1.0], fig.p_lab: [40, 1.0],
                         fig.tangent_lab: [34, 1.0]}
            readout = VGroup(frac, row_g, deriv)
            tgt = VGroup(frac.copy().move_to([0, 2.2, 0]), row_g.copy().move_to([0, 1.0, 0]),
                         deriv.copy())
            tgt[2].next_to(tgt[1], DOWN, buff=0.4)
            tgt.move_to([0.6, 1.85, 0])
            for m, t in zip(readout, tgt):
                m.generate_target()
                m.target.move_to(t)
            self.shrink_target(figg, 0.5, -3.7)
            self.play(*during(disappear(arc, arc_lab, row, row2, row3), 0, 0.4), MoveToTarget(figg),
                      *during([MoveToTarget(m) for m in readout], 0.3, 1.0), run_time=1.8)
            box = definition_box()
            three_w = 1.0
            box.move_to([-(three_w + 0.3) / 2, -1.45, 0])
            self.play(*appear(box), run_time=1.2)
            c.wait_until("delta why over")
            self.play(FlashAround(box.formula[6], time_width=1.5), run_time=1.5)
            later = T("limits, properly: Chapter 5 of the notes", 28, DIM).move_to([0, -3.25, 0])
            c.wait_until("later")
            self.play(*appear(later), run_time=1.0)

        # ---------------- c1.chord.4: 0/0, Newton, resolved
        with self.say("c1.chord.4", gap=1.6) as c:
            fm = box.formula
            self.play(FlashAround(fm[6], time_width=1.5), run_time=1.5)
            dy = select(fm, r"\delta y")[0]
            dxs = select(fm, r"\delta x")
            dxb = dxs[len(dxs) - 1]
            top0 = tx(r"\to 0", 30, TEAL).next_to(dy, RIGHT, buff=0.12)
            bot0 = tx(r"\to 0", 30, TEAL).next_to(dxb, RIGHT, buff=0.12)
            c.wait_until("top")
            self.play(*appear(top0, shift=None), run_time=0.9)
            c.wait_until("bottom")
            self.play(*appear(bot0, shift=None), run_time=0.9)
            q00 = tx([r"\frac{0}{0}", r"\,?"], 52, YELLOW).next_to(box.rect, RIGHT, buff=0.35)
            self.play(*appear(q00), run_time=1.0)
            newton = T("Newton", 48, YELLOW)
            century = T("17th century", 32)
            contro = T("controversial", 30, RED)
            VGroup(newton, century, contro).arrange(DOWN, buff=0.3).move_to([4.7, 1.55, 0])
            c.wait_until("newton")
            self.play(*appear(newton), run_time=1.0)
            c.wait_until("seventeenth")
            self.play(*appear(century), run_time=0.9)
            c.wait_until(own_word=contro)
            self.play(*appear(contro), run_time=0.9)
            c.wait_until("here to three")
            three = tx("3", 60, GREEN).move_to(q00)
            self.play(*swap(q00, three), FlashAround(row_g[2], time_width=1.5),
                      *during(disappear(later), 0, 0.45), run_time=1.5)
            quote = T("“another mathematical crisis successfully resolved”", 32,
                      slant=ITALIC).move_to([0, -3.25, 0])
            c.wait_until("lecturer")
            self.play(*appear(quote), run_time=1.2)

        # ---------------- c1.chord.5: linearity
        with self.say("c1.chord.5", gap=3.0) as c:
            figg = self.fig_small
            others = [m for m in self.mobjects if m is not figg]
            self.shrink_target(figg, 0.8, -4.6)
            self.play(*during(disappear(*others), 0, 0.5), *during(MoveToTarget(figg), 0.3, 1.0),
                      run_time=1.6)
            title = T("Differentiation is a linear operation", 38, t2c={"linear operation": YELLOW})
            title.move_to([2.0, 3.3, 0])
            c.wait_until(own_word=title)
            self.play(*appear(title), run_time=1.2)
            fg = {"{f}": BLUE, "{g}": PURPLE}
            sum_eq = tx(r"\frac{d}{dx}\big({f} + {g}\big) = \frac{d{f}}{dx} + \frac{d{g}}{dx}", 48,
                        iso=["{f}", "{g}"], colors=fg).move_to([2.0, 1.75, 0])
            c.wait_until("sum")
            self.play(*appear(sum_eq), run_time=1.2)
            const = tx(r"\frac{d}{dx}\big({c}\,{f}\big) = {c}\,\frac{d{f}}{dx}", 48,
                       iso=["{c}", "{f}"], colors={"{f}": BLUE})
            const.move_to([2.0, 0.15, 0])
            cs = select(const, "{c}")
            c_in, c_out = cs[0], cs[1]
            c_out.set_opacity(0)
            c.wait_until("constant")
            self.play(*appear(const), run_time=1.0)
            c.wait_until("comes out")
            c_mv = c_in.copy()
            self.add(c_mv)
            self.play(c_mv.animate(path_arc=-0.7 * PI).move_to(c_out), run_time=1.5)

            dlt = {r"\delta x": TEAL, "{f}": BLUE, "{g}": PURPLE}
            iso = [r"\delta x", "{f}", "{g}"]
            lhs = tx(r"\frac{({f}+{g})(x+\delta x) - ({f}+{g})(x)}{\delta x}", 40, iso=iso, colors=dlt)
            eq = tx("=", 40)
            fq = tx(r"\frac{{f}(x+\delta x) - {f}(x)}{\delta x}", 40, iso=iso, colors=dlt)
            pl = tx("+", 40)
            gq = tx(r"\frac{{g}(x+\delta x) - {g}(x)}{\delta x}", 40, iso=iso, colors=dlt)
            VGroup(lhs, eq, fq, pl, gq).arrange(RIGHT, buff=0.3).move_to([0, -2.1, 0])
            c.wait_until("quotient")
            self.play(*appear(lhs), run_time=1.0)
            c.wait_until("splits")
            self.play(FlashUnder(lhs, time_width=1.5), run_time=1.2)
            self.play(*appear(eq, fq, pl, gq, shift=None, lag=0.3), run_time=1.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def shrink_target(self, group, s, x, top=3.45):
        """Target: group scaled by s, labels kept at ~30 pt, left-right centre x, top at `top`."""
        group.generate_target()
        t = group.target
        t.scale(s)
        for lab, st in self.labs.items():
            if lab in group.submobjects:
                size, cur = st
                k = (30 / size) / (cur * s)
                t.submobjects[group.submobjects.index(lab)].scale(k)
                st[1] = 30 / size
            else:
                st[1] *= s
        t.move_to([x, 0, 0])
        t.shift((top - t.get_top()[1]) * UP)
        # the "tangent" label sits just below-right of the tangent's far end, clear of line and curve
        fig = self.fig
        if fig.tangent in group.submobjects and fig.tangent_lab in group.submobjects:
            tan_t = t.submobjects[group.submobjects.index(fig.tangent)]
            lab_t = t.submobjects[group.submobjects.index(fig.tangent_lab)]
            end = tan_t.get_end()
            lab_t.move_to(end + (lab_t.width / 2 + 0.05) * RIGHT + (lab_t.height / 2 + 0.15) * DOWN)

    def swing(self, d0, d1):
        """The chord rotates about P as dx goes geometrically from d0 to d1; dot and label follow."""
        fig, ax = self.fig, self.fig.axes

        def dx(a):
            return d0 * (d1 / d0) ** a

        return [
            UpdateFromAlphaFunc(fig.chord, lambda m, a: m.become(chord_line(ax, dx(a)))),
            UpdateFromAlphaFunc(fig.q_dot, lambda m, a: m.move_to(_pt(ax, 1.0 + dx(a)))),
            UpdateFromAlphaFunc(fig.chord_lab, lambda m, a: m.move_to(chord_label_pos(ax, dx(a)))),
        ]
