"""Chapter 6, scene 8: recap in five panels, then Part 7 and the next lecture. Clips c6.recap.1 – c6.recap.2.

Five panels (three over two), DIM frames lit BLUE while they are built, each a small copy of the
shot that taught it with its two-line caption under it: {h} s2's s = 1 hyperbola, tiny quarter
labels, dashed asymptotes; {p} s1's glimpse pair driven by one GOLD θ (s3 clip 4's readout);
{t} s4's two orientations, the right branches turning a quarter turn; {c} s5's table, Example 36's
ellipse row lit GREEN; {o} s6's collapse onto the solid crossing lines, then point, parabola and
parallel-line icons. Clip 2: the panels sweep away for s7's four G cards and the Part 7 note, then
"Next: differentiation". End card held ~8 s, then fade.
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch6_s2_hyperbola")
HOOK = load_scene("ch6_s1_hook")
S3 = load_scene("ch6_s3_param")
S4 = load_scene("ch6_s4_turn")
S5 = load_scene("ch6_s5_classify")
S6 = load_scene("ch6_s6_odd_cases")
S7 = load_scene("ch6_s7_hints")

PH = 3.5
TOP_Y, BOT_Y = 1.95, -1.8
CENTRES = [np.array([-4.45, TOP_Y, 0]), np.array([0, TOP_Y, 0]), np.array([4.45, TOP_Y, 0]),
           np.array([-2.9, BOT_Y, 0]), np.array([3.8, BOT_Y, 0])]
WIDTHS = [4.3, 4.3, 4.3, 7.4, 5.6]
REG_H = 2.3
CAP = 28


def frame_at(k):
    return RoundedRectangle(corner_radius=0.15, width=WIDTHS[k], height=PH).set_stroke(DIM, 2).move_to(CENTRES[k])


def region(k):
    return CENTRES[k] + np.array([0, 0.3 if k == 3 else 0.42, 0])


def fit(m, k, w=None, h=REG_H, at=None):
    w = (WIDTHS[k] - 0.4) if w is None else w
    m.scale(min(w / m.width, h / m.height))
    m.move_to(region(k) if at is None else at)
    return m


def cap_line(k, i, mob):
    """Caption line i (0 = upper, 1 = lower) under panel k's picture."""
    return mob.move_to(CENTRES[k] + np.array([0, -1.05 - 0.43 * i, 0]))


def light(frame):
    return restyle(frame, outline=BLUE, width=3)


def unlight(frame):
    return restyle(frame, outline=DIM, width=2)


def s2_place(m, k_scale, centre):
    return m.scale(k_scale, about_point=S2.C).shift(centre - S2.C)


class Ch6S8Recap(NarratedScene):
    def construct(self):
        frames = [frame_at(k) for k in range(5)]

        # ------------------------------------------------------------ c6.recap.1
        with self.say("c6.recap.1") as c:
            self.play(*appear(*frames, shift=None, lag=0.15),  # early: the five empty panels, shown whole then filled
                      run_time=min(1.4, c.until("h")))
            c.wait_until("h")

            # ---- {h}: x^2 - y^2 = s^2, quarter labels, asymptotes
            WIN = 1.85
            kp = WIN / (2 * S2.H)
            hc = region(0) + 0.22 * DOWN
            h_axes = s2_place(S2.make_axes(), kp, hc)
            h_br = s2_place(S2.make_branches(), kp, hc)
            h_as = s2_place(S2.make_asymptotes(), kp, hc)

            def h_pt(x, y):
                return s2_place(VectorizedPoint(S2.to_world(x, y)), kp, hc).get_center()
            signs = [MathTex(sg, font_size=36, color=YELLOW).move_to(h_pt(sx * 2.75, sy * 1.25))
                     for sg, sx, sy in (("+", 1, 1), ("+", -1, 1), ("-", 1, -1), ("-", -1, -1))]
            cap_h0 = MathTex(r"x^2 - y^2 = s^2", font_size=32).move_to(region(0) + np.array([0, 0.98, 0]))
            cap_h1 = cap_line(0, 0, T("two branches,", CAP))
            cap_h2 = cap_line(0, 1, T("two asymptotes", CAP))
            self.play(light(frames[0]), *appear(h_axes, shift=None), *appear(cap_h0),
                      run_time=min(1.2, c.until("hyperbola")))
            c.wait_until("hyperbola")
            self.play(*appear(h_br.right, h_br.left, shift=None, lag=0.2),
                      *appear(*signs, shift=None, lag=0.15),
                      run_time=min(1.3, c.until("two branches")))
            c.wait_until(own_word=cap_h1)
            self.play(*appear(cap_h1), run_time=min(1.0, c.until("two asymptotes")))
            c.wait_until("two asymptotes")
            self.play(*appear(h_as, shift=None), *appear(cap_h2), run_time=min(1.0, c.until("p")))
            c.wait_until("p")

            # ---- {p}: the glimpse pair, one GOLD theta
            pair = HOOK.glimpse_pair()
            pair.remove(pair.clabel, pair.hlabel)
            pair.hyper_panel.shift(1.9 * LEFT)
            th = pair.theta
            th.set_value(0.25)
            pair.update(0)
            pc = region(1) + 0.28 * DOWN
            fit(pair, 1, w=3.9, h=1.8, at=pc)
            pair.update(0)
            ro = S3.readout(th, size=30).move_to(region(1) + np.array([0, 1.0, 0]))
            cc = pair.circle.get_center()
            u = pair.circle.width / 2
            rad = always_redraw(lambda: Line(cc, pair.cdot.get_center()).set_stroke(FG, 2.5))
            arc = always_redraw(lambda: Arc(radius=0.36 * u, start_angle=0, angle=th.get_value(),
                                            arc_center=cc).set_stroke(GOLD, 4))
            cap_p1 = cap_line(1, 0, T("cosh and sinh", CAP))
            cap_p2 = cap_line(1, 1, T("draw the hyperbola", CAP))
            self.play(unlight(frames[0]), light(frames[1]),
                      *appear(pair.circle_panel, pair.hyper_panel, pair.cdot, pair.hdot, rad, arc, ro,
                              shift=None, lag=0.1), *appear(cap_p1),
                      run_time=min(1.3, c.until("just as")))
            c.wait_until("draw it")
            self.play(*appear(cap_p2), th.animate.set_value(0.95), run_time=min(2.2, c.until("hyperbolic")))
            ro[1].clear_updaters()
            c.wait_until("hyperbolic")
            self.play(VShowPassingFlash(pair.right.copy().set_stroke(YELLOW, 7), time_width=0.5),
                      FlashAround(ro, run_time=1.6, time_width=1.5), run_time=1.6)
            c.wait_until("t")

            # ---- {t}: two orientations, the quarter turn
            L = S4.left_picture()
            R = S4.right_picture()
            dots, _ = S4.vertex_marks()
            pics = VGroup(L, R, dots)
            kt = 3.9 / pics.width
            pics.scale(kt).move_to(region(2) + 0.25 * UP)
            eqL = S4.eq_parts("x^2", "y^2", 28).next_to(L, DOWN, buff=0.12)
            eqR = S4.eq_parts("y^2", "x^2", 28).next_to(R, DOWN, buff=0.12)
            eqR.set_y(eqL.get_y())
            rc = R.axes.get_center()
            R.branches.rotate(-PI / 2, about_point=rc)
            cap_t1 = cap_line(2, 0, T("flip the right-hand side:", CAP))
            cap_t2 = cap_line(2, 1, T("a quarter turn", CAP))
            self.play(unlight(frames[1]), light(frames[2]),
                      *appear(L, eqL, shift=None, lag=0.2), *appear(cap_t1),
                      run_time=min(1.3, c.until("hyperbola")))
            c.wait_until("hyperbola")
            self.play(*appear(R.axes, R.asym, R.branches, eqR, shift=None, lag=0.15),
                      run_time=min(0.9, c.until("quarter turn")))
            c.wait_until("quarter turn")
            self.play(Rotate(R.branches, PI / 2, about_point=rc), *appear(cap_t2),
                      run_time=min(1.4, c.until("c")))
            self.play(*appear(*dots, shift=None), run_time=min(0.6, c.until("c")))
            c.wait_until("c")

            # ---- {c}: the table, Example 36's ellipse row lit
            tab = S5.classify_table(lit=1)
            tab.rows[1].name.set_color(FG)
            for r in tab.rows:
                r.name.scale(1.12, about_edge=LEFT)
            row_light = tab.light
            tab.remove(row_light)
            o0, w0 = tab.get_center(), tab.width
            fit(tab, 3, h=2.6)
            row_light.scale(tab.width / w0, about_point=o0).shift(tab.get_center() - o0)
            cap_c1 = T("complete the squares, read the signs", CAP).move_to(CENTRES[3] + np.array([0, -1.27, 0]))
            self.play(unlight(frames[2]), light(frames[3]), *appear(*tab.rows, shift=None, lag=0.2),
                      run_time=min(1.4, c.until("complete the squares")))
            c.wait_until(own_word=cap_c1)
            self.play(*appear(cap_c1), run_time=1.0)
            c.wait_until("read the signs")
            self.play(FadeIn(row_light), tab.rows[1].name.animate.set_color(GREEN),
                      run_time=min(1.0, c.until("o")))
            c.wait_until("o")

            # ---- {o}: the collapse onto the crossing lines, then the odd cases
            oc = region(4) + 1.25 * LEFT
            ko = REG_H / (2 * S2.H)
            col = s2_place(S6.collapse_shot(), ko, oc)
            o_as = s2_place(S2.make_asymptotes(), ko, oc)
            s_tr = ValueTracker(1.0)
            o_br = always_redraw(lambda: s2_place(S2.make_branches(s_tr.get_value()), ko, oc))
            ix = CENTRES[4][0] + 1.6
            pt = S6.point_icon(0.75).move_to([ix, region(4)[1] + 0.6, 0])
            pb = S6.parabola_icon(0.75).move_to([ix - 0.6, region(4)[1] - 0.5, 0])
            pl = S6.parallel_icon(0.75).move_to([ix + 0.6, region(4)[1] - 0.5, 0])
            cap_o1 = cap_line(4, 0, MathTex(r"f = 0,\ \text{or a missing square:}", font_size=32))
            cap_o2 = cap_line(4, 1, T("the odd cases", CAP))
            self.play(unlight(frames[3]), light(frames[4]), *appear(col.axes, o_as, o_br, shift=None, lag=0.1),
                      *appear(cap_o1), run_time=min(1.0, c.until("zero")))
            c.wait_until("zero")
            self.play(s_tr.animate.set_value(0.03), run_time=min(2.0, c.until("odd cases")))
            c.wait_until(own_word=cap_o2)
            self.play(*appear(cap_o2), run_time=min(1.0, c.until("crossing lines")))
            c.wait_until("crossing lines")
            self.play(*disappear(o_br, o_as), FadeIn(col.lines), run_time=min(0.9, c.until("a point")))
            c.wait_until("a point")
            self.play(*appear(pt, pb, pl, shift=None, lag=0.45), run_time=min(1.4, c.remaining - 0.05))

        # ------------------------------------------------------------ c6.recap.2
        with self.say("c6.recap.2") as c:
            row = S7.hints_row(lit=True)
            row.move_to([0, 1.6, 0])
            note = S7.sheet_note().move_to([0, -0.45, 0])
            head = T("Next: differentiation", 48).move_to([0, -1.75, 0])
            sub = T("(Chapter 4 of the notes)", 32, color=DIM).move_to([0, -2.5, 0])
            # the panels are gone before the first card arrives (on "the bonus")
            self.play(*disappear(*list(self.mobjects)), run_time=min(0.8, c.until("the bonus")))
            c.wait_until("the bonus")
            self.play(*appear(*row, shift=None, lag=0.15), run_time=1.3)
            c.wait_until("section g")
            self.play(*appear(note), run_time=min(1.0, c.until("next")))
            c.wait_until("next")
            self.play(*appear(head), run_time=min(1.0, c.until("chapter four")))
            c.wait_until("chapter four")
            self.play(*appear(sub), run_time=min(1.0, c.until("bye")))
            c.wait_until("bye")
        self.wait(7.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
