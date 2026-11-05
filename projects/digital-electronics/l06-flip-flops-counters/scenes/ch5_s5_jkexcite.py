"""Chapter 5, scene 5: the J-K excitation table, built from the J-K truth table one transition at a time. Clips c5.jk.1 – c5.jk.4."""
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


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# Shared tables (ch3_s3_jk's grid_table / jk_table styling)
# =============================================================================================
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    """ch1_s2's grid_table: rows of strings ('$...' -> MathTex, else T); header row at y = 0,
    column centres xs (or ('L', x) for left-aligned). VGroup(*rows, lines), .rows, .lines."""
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            if s.startswith("$"):
                m = MathTex(s[1:], font_size=size, color=col)
            else:
                m = T(s, size=size * 0.82, color=col)
            x = xs[j]
            if isinstance(x, tuple):
                m.move_to(_p(x[1], -i * pitch), aligned_edge=LEFT)
                m.set_y(-i * pitch)
            else:
                m.move_to(_p(x, -i * pitch))
            cells.append(m)
        out.append(VGroup(*cells))
    top, bot = 0.4, -(len(rows) - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.3, -pitch / 2),
                   _p(out[0].get_right()[0] + 0.3, -pitch / 2)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines = out, lines
    return g


PITCH = 0.8
L_XS = [0, 0.75, 2.15, ("L", 3.0)]     # J, K, Q', comment
L_SEPS = [1.45, 2.7]
R_XS = [0, 0.85, 2.95, 3.95]           # Q, Q', J, K
R_SEPS = [1.9]


def jk_truth_table(pitch=PITCH):
    """ch3_s3's jk_table() cut to slide p. 98: `J K | Q' | comment` (hold / reset / set / toggle).
    Header row at y = 0, J column at x = 0. J, K BLUE; Q', Q, Q-bar GREEN; "toggle" YELLOW.
    .rows[0] header, .rows[1..4] (cells: J, K, Q', comment), .lines."""
    rows = [["$J", "$K", "$Q'", "comment"],
            ["$0", "$0", "$Q", "hold"],
            ["$0", "$1", "$0", "reset"],
            ["$1", "$0", "$1", "set"],
            ["$1", "$1", r"$\overline{Q}", "toggle"]]
    tab = grid_table(rows, L_XS, size=44, pitch=pitch, seps=L_SEPS)
    r = tab.rows
    for m in r[0][0:2]:
        m.set_color(BLUE)
    for i in (0, 1, 4):
        r[i][2].set_color(GREEN)
    r[4][3].set_color(YELLOW)
    return tab


def jk_exc_table(pitch=PITCH, x_color=FG):
    """The J-K excitation table (slide p. 98), same styling: header `Q Q' | J K` (Q, Q' GREEN;
    J, K BLUE), rows 00|0 x, 01|1 x, 10|x 1, 11|x 0 (x is a lowercase MathTex x, colour x_color).
    Header row at y = 0, Q column at x = 0; columns Q 0, Q' 0.85, J 2.95, K 3.95, separator 1.9.
    About 4.25 wide; 3.98 tall at pitch 0.8 (3.42 at pitch 0.66, as d_exc_table).
    .rows[0] header, .rows[1..4] (cells: Q, Q', J, K), .lines; .xs = the four x cells."""
    rows = [["$Q", "$Q'", "$J", "$K"],
            ["$0", "$0", "$0", "$x"],
            ["$0", "$1", "$1", "$x"],
            ["$1", "$0", "$x", "$1"],
            ["$1", "$1", "$x", "$0"]]
    tab = grid_table(rows, R_XS, size=44, pitch=pitch, seps=R_SEPS)
    h = tab.rows[0]
    h[0].set_color(GREEN)
    h[1].set_color(GREEN)
    h[2].set_color(BLUE)
    h[3].set_color(BLUE)
    tab.xs = [tab.rows[1][3], tab.rows[2][3], tab.rows[3][2], tab.rows[4][2]]
    for m in tab.xs:
        m.set_color(x_color)
    return tab


D_XS = [0, 0.9, 2.1]      # ch5_s4_dexcite's d_exc_table() columns
D_SEPS = [1.5]


def d_exc_table():
    """Copied from ch5_s4_dexcite: header `Q Q' | D` (Q, Q' GREEN, D BLUE), rows 00|0, 01|1,
    10|0, 11|1 (FG). Header row at y = 0, Q column at x = 0."""
    rows = [["$Q", "$Q'", "$D"],
            ["$0", "$0", "$0"],
            ["$0", "$1", "$1"],
            ["$1", "$0", "$0"],
            ["$1", "$1", "$1"]]
    tab = grid_table(rows, D_XS, size=44, pitch=0.66, seps=D_SEPS)
    h = tab.rows[0]
    h[0].set_color(GREEN)
    h[1].set_color(GREEN)
    h[2].set_color(BLUE)
    return tab


# =============================================================================================
# Layout and scene-only helpers
# =============================================================================================
LX, HY = -5.6, 1.1        # truth table: J column x, header y
RX = 1.3                  # excitation table: Q column x (same header y)
SLOT = 0.25               # two arriving copies sit at cell x -/+ SLOT before they merge
CY = -3.0                               # corridor under both tables
LANE_L = LX - 0.9                       # left of the truth table's J column
GUT_L = LX + L_SEPS[0]                  # gap between the K and Q' columns (on the separator)
CHAN_R = RX + R_SEPS[0]                 # gap between the Q' and J columns of the excitation table
LANE_R = RX + R_XS[3] + 0.75            # right of the excitation table's K column


def row_y(i):
    return HY - i * PITCH


LEGS = (1, 1, 2, 1, 1)     # 10%-steps per leg: step out, down, along the corridor, up, in


def travel(src, pts, dst_pt, start, reveal_y=None):
    """A copy of src travels along straight legs src -> pts -> dst_pt (5 legs), starting at step
    `start` of its play (steps of 10%) and taking LEGS steps per leg, so every corner lands on a
    10% mark (the overlap audit interpolates between those marks). Invisible until it starts,
    parked 0.35 out from src; fades in on the way down. Returns (copy, animation)."""
    c0 = src.get_center()
    v = pts[0] - c0
    p0 = c0 + 0.35 * v / np.linalg.norm(v)
    corners = [p0, *pts, dst_pt]
    marks = np.cumsum([start, *LEGS]) / 10.0         # leg k runs from marks[k] to marks[k + 1]
    cp = src.copy().move_to(p0).set_opacity(0)

    def f(m, a):
        if a <= marks[0]:
            m.move_to(p0).set_opacity(0)
            return
        k = min(len(LEGS) - 1, int(np.searchsorted(marks, a, side="left")) - 1)
        u = (a - marks[k]) / (marks[k + 1] - marks[k])
        u = min(1.0, max(0.0, u))
        m.move_to(corners[k] + u * (corners[k + 1] - corners[k]))   # steady speed, no pauses
        # hidden while it steps out sideways (it would read as an extra digit in its row);
        # fades in on the way down, once below its row
        if k == 0:
            op = 0.0
        elif k == 1 and reveal_y is not None:          # inside the table: only once below it
            op = min(1.0, max(0.0, (reveal_y - m.get_y()) / 0.3))
        elif k == 1:
            op = min(1.0, u / 0.35)
        else:
            op = 1.0
        m.set_opacity(op)
    return cp, UpdateFromAlphaFunc(cp, f, rate_func=linear)


def pulse(m, to=YELLOW, base=FG, end=None, s=0.0, e=1.0):
    """Colour pulse base -> to -> end (default base) with a small swell, in [s, e] of the play."""
    ref = m.copy()
    end = base if end is None else end

    def f(mob, a):
        t = min(1.0, max(0.0, (a - s) / (e - s)))
        k = there_and_back(t)
        col = interpolate_color(ManimColor(base), ManimColor(to), k) if t < 0.5 else \
            interpolate_color(ManimColor(end), ManimColor(to), k)
        mob.become(ref.copy().scale(1 + 0.35 * k).set_color(col))
    return UpdateFromAlphaFunc(m, f, rate_func=linear)


class JKExcitation(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---------------------------------------------------------------- building blocks
    def row_box(self, i):
        """YELLOW outline round the whole truth-table row i."""
        tab = self.truth
        left = LX - 0.38
        right = tab.rows[0][3].get_right()[0] + 0.25
        return Rectangle(width=right - left, height=PITCH - 0.16).set_stroke(YELLOW, 3) \
            .set_fill(opacity=0).move_to(_p((left + right) / 2, row_y(i)))

    def light_box(self, i):
        left, right = RX - 0.42, RX + R_XS[3] + 0.55
        return Rectangle(width=right - left, height=PITCH - 0.16).set_stroke(YELLOW, 2) \
            .set_fill(YELLOW, 0.12).move_to(_p((left + right) / 2, row_y(i))).set_z_index(-1)

    def fly_col(self, col, srcs, tgt, s=0.0):
        """Copies of column col (0 = J, 1 = K) of truth rows srcs fly to the excitation row tgt.
        Returns (copies, anims). J copies go down the left lane, under the tables and up the
        Q'|J gap; K copies down the K|Q' gap, under the tables and up the right lane.
        s = 0: the copies start at 0% and 40% of the play; s > 0 (the play also merges the
        previous cell in its first 30%): at 30% and 40%."""
        ty = row_y(tgt)
        cx = RX + R_XS[2 + col]
        slots = [cx + SLOT, cx - SLOT] if col == 0 else [cx - SLOT, cx + SLOT]
        starts = (0, 4) if s < 0.2 else (3, 4)
        copies, anims = [], []
        for st, r, sx in zip(starts, srcs, slots):
            src = self.truth.rows[r][col]
            ry = row_y(r)
            if col == 0:
                pts = [_p(LANE_L, ry), _p(LANE_L, CY), _p(CHAN_R, CY), _p(CHAN_R, ty)]
            else:
                pts = [_p(GUT_L, ry), _p(GUT_L, CY), _p(LANE_R, CY), _p(LANE_R, ty)]
            cp, an = travel(src, pts, _p(sx, ty), st,
                            reveal_y=None if col == 0 else row_y(4) - 0.35)
            copies.append(cp)
            anims.append(an)
        return copies, anims

    def merge(self, copies, result, a=0.0, b=1.0):
        """The two landed copies fade where they are, the merged value appears in the cell."""
        mid = a + 0.5 * (b - a)
        return [*during(disappear(*copies), a, a + 0.45 * (b - a)),
                *during(appear(result, shift=None), mid, b)]

    def light(self, i, old=None, boxes=()):
        """Anims: the excitation row i lights YELLOW (the light box slides from row old)."""
        er = self.exc.rows
        anims = [*recolor(er[i][0], YELLOW), *recolor(er[i][1], YELLOW)]
        if old is None:
            anims.append(FadeIn(self.lbox))
        else:
            anims += [*recolor(er[old][0], FG), *recolor(er[old][1], FG),
                      self.lbox.animate.set_y(row_y(i))]
        if boxes:
            anims += disappear(*boxes)
        return anims

    # -------------------------------------------------------------- c5.jk.1
    def clip1(self):
        with self.say("c5.jk.1") as c:
            head = T("Excitation table", 52).move_to(_p(0, 0.45))
            sub = T("for any type of flip-flop", 36, color=DIM).next_to(head, DOWN, buff=0.45)
            self.play(*appear(head), run_time=1.2)
            c.wait_until("any type")
            self.play(*appear(sub), run_time=1.0)
            c.wait_until("jk")
            jk = T("the J-K flip-flop", 40, color=BLUE).move_to(sub)
            self.play(*swap(sub, jk), run_time=1.2)

            c.wait_until("truth")
            tab = jk_truth_table().shift(_p(LX, HY))
            self.truth = tab
            ttl = T("Truth table", 36, color=DIM).move_to(_p(LX + 2.0, HY + 1.8))
            r_ttl = T("Excitation table", 36, color=DIM).move_to(_p(RX + 1.95, HY + 1.8))
            self.r_ttl = r_ttl
            head.generate_target()
            head.target.become(r_ttl)
            self.play(*during(disappear(jk), 0, 0.4),
                      *during([MoveToTarget(head)], 0.25, 0.85),
                      *during(appear(ttl, tab.rows[0], tab.lines, lag=0.15), 0.45, 1.0),
                      run_time=2.0)  # early: table header shown whole, then walked row by row
            self.remove(head)
            self.add(r_ttl)
            self.l_ttl = ttl

            cues = ["rows", "zero one is reset", "one zero is set", "and one one is toggle"]
            for i, cue in enumerate(cues, start=1):
                c.wait_until(cue)
                self.play(*appear(*tab.rows[i], lag=0.2), run_time=1.2)

            c.wait_until("roles")
            tag_j = T("J acts as S", 30, color=BLUE)
            tag_j.move_to(_p(0, HY + 1.12)).align_to(_p(LX - 0.15, 0), LEFT)
            tag_k = T("K acts as R", 30, color=BLUE)
            tag_k.move_to(_p(0, HY + 0.6)).align_to(_p(LX + L_XS[1] - 0.15, 0), LEFT)
            self.tags = VGroup(tag_j, tag_k)
            self.play(*appear(tag_j), run_time=1.0)
            c.wait_until("and kay")
            self.play(*appear(tag_k), run_time=1.0)

            c.wait_until("goal")
            exc = jk_exc_table().shift(_p(RX, HY))
            self.exc = exc
            self.res = {}
            for i in range(1, 5):
                r = exc.rows[i]
                self.res[(i, 0)], self.res[(i, 1)] = r[2], r[3]
                r.remove(r[2], r[3])
            self.play(*appear(exc.rows[0], exc.lines, *exc.rows[1:], lag=0.15),
                      run_time=1.8)  # early: the empty table is shown whole, then filled
            self.lbox = self.light_box(1)

    # -------------------------------------------------------------- c5.jk.2
    def clip2(self):
        with self.say("c5.jk.2") as c:
            self.play(*self.light(1), run_time=1.0)
            c.wait_until("hold")
            b_hold = self.row_box(1)
            self.play(FadeIn(b_hold), run_time=0.8)
            c.wait_until("reset")
            b_reset = self.row_box(2)
            self.play(FadeIn(b_reset), run_time=0.8)

            c.wait_until("jzero")
            cps, an = self.fly_col(0, [1, 2], 1)
            self.play(*an, run_time=min(2.0, 0.75 * c.until("kfree")))
            self.play(*self.merge(cps, self.res[(1, 0)]), run_time=min(0.8, c.until("kfree")))

            c.wait_until("kfree")
            cps, an = self.fly_col(1, [1, 2], 1)
            self.play(*an, run_time=2.0)
            c.wait_until("either")
            self.play(*self.merge(cps, self.res[(1, 1)]), run_time=1.0)
            c.wait_until("x")
            self.play(pulse(self.res[(1, 1)]), run_time=1.4)
            self.boxes = [b_hold, b_reset]

    # -------------------------------------------------------------- c5.jk.3
    def clip3(self):
        with self.say("c5.jk.3") as c:
            # ---- 0 -> 1: set, toggle -> 1 x
            self.play(*self.light(2, old=1, boxes=self.boxes), run_time=1.2)
            c.wait_until("set does it")
            b1 = self.row_box(3)
            self.play(FadeIn(b1), run_time=0.8)
            c.wait_until("so does toggle")
            b2 = self.row_box(4)
            self.play(FadeIn(b2), run_time=0.8)
            c.wait_until("both have jay")
            jc, ja = self.fly_col(0, [3, 4], 2)
            self.play(*ja, run_time=min(1.6, 0.9 * c.until("so jay is one")))
            c.wait_until("so jay is one")
            kc, ka = self.fly_col(1, [3, 4], 2, s=0.25)
            self.play(*self.merge(jc, self.res[(2, 0)], 0, 0.3), *ka,
                      run_time=min(1.9, 0.85 * c.until("t10")))
            self.play(*self.merge(kc, self.res[(2, 1)]), run_time=min(0.8, c.until("t10")))

            # ---- 1 -> 0: reset, toggle -> x 1
            c.wait_until("t10")
            self.play(*self.light(3, old=2, boxes=[b1, b2]), run_time=1.0)
            c.wait_until("by reset")
            b1 = self.row_box(2)
            self.play(FadeIn(b1), run_time=0.6)
            c.wait_until("by toggle")
            b2 = self.row_box(4)
            self.play(FadeIn(b2), run_time=0.6)
            c.wait_until("here kay")
            kc, ka = self.fly_col(1, [2, 4], 3)
            self.play(*ka, run_time=min(1.3, 0.9 * c.until("and jay")))
            c.wait_until("and jay")
            jc, ja = self.fly_col(0, [2, 4], 3, s=0.25)
            self.play(*self.merge(kc, self.res[(3, 1)], 0, 0.3), *ja,
                      run_time=min(1.6, 0.8 * c.until("t11")))
            self.play(*self.merge(jc, self.res[(3, 0)]), run_time=min(0.7, c.until("t11")))

            # ---- 1 -> 1: hold, set -> x 0
            c.wait_until("t11")
            q_j = MathTex("?", font_size=44, color=YELLOW).move_to(_p(RX + R_XS[2], row_y(4)))
            q_k = MathTex("?", font_size=44, color=YELLOW).move_to(_p(RX + R_XS[3], row_y(4)))
            self.play(*self.light(4, old=3, boxes=[b1, b2]), run_time=1.0)
            self.play(*appear(q_j, q_k, shift=None, lag=0.2), run_time=0.9)
            c.wait_until("t11ans")
            b1 = self.row_box(1)
            self.play(FadeIn(b1), run_time=0.6)
            c.wait_until("or set")
            b2 = self.row_box(3)
            self.play(FadeIn(b2), run_time=0.6)
            c.wait_until("so kay")
            kc, ka = self.fly_col(1, [1, 3], 4, s=0.1)
            self.play(*during(disappear(q_k), 0, 0.2), *ka,
                      run_time=min(1.3, 0.85 * c.until("and again")))
            c.wait_until("and again")
            jc, ja = self.fly_col(0, [1, 3], 4, s=0.25)
            rt = min(1.5, 0.75 * c.until())
            self.play(*self.merge(kc, self.res[(4, 1)], 0, 0.3), *during(disappear(q_j), 0, 0.2),
                      *ja, run_time=rt)
            self.play(*self.merge(jc, self.res[(4, 0)]), run_time=max(0.4, min(0.7, c.until())))
            self.boxes = [b1, b2]

    # -------------------------------------------------------------- c5.jk.4
    def clip4(self):
        exc = self.exc
        settle(self, exc, add=[self.res[k] for k in sorted(self.res)])
        with self.say("c5.jk.4") as c:
            er = exc.rows
            dx = -5.6 - RX
            exc.generate_target()
            exc.target.shift(_p(dx, -0.2))
            for k in (0, 1):
                exc.target.rows[4][k].set_color(FG)     # the lit row goes back to FG as it moves
            self.play(*during(disappear(self.truth, self.tags, self.l_ttl, self.lbox, *self.boxes), 0, 0.4),
                      *during([MoveToTarget(exc), self.r_ttl.animate.shift(_p(dx, -0.2))], 0.35, 1.0),
                      run_time=min(1.8, c.until("one")))
            c.wait_until("one")
            xs = [self.res[(1, 1)], self.res[(2, 1)], self.res[(3, 0)], self.res[(4, 0)]]
            self.play(*[pulse(m, end=YELLOW, s=0.22 * k, e=0.22 * k + 0.34) for k, m in enumerate(xs)],
                      run_time=2.6)

            c.wait_until("free")
            # a generic 2-by-2 K-map: 1 1 / X X; the loop round the 1s grows to take in the X's
            side = 1.1
            kx, ky = 1.0, -0.55
            cells = VGroup()
            vals = VGroup()
            for k, v in enumerate(["1", "1", "X", "X"]):
                cx = kx + (k % 2 - 0.5) * side
                cy = ky + (0.5 - k // 2) * side
                cells.add(Square(side).set_stroke(DIM, 2).move_to(_p(cx, cy)))
                vals.add(MathTex(v, font_size=48, color=(YELLOW if v == "X" else FG)).move_to(_p(cx, cy)))
            km_ttl = T("K-map", 30, color=DIM).next_to(cells, UP, buff=0.35)
            self.play(*appear(cells, vals, lag=0.2, shift=None), *appear(km_ttl), run_time=1.2)
            c.wait_until("free cells")
            small = RoundedRectangle(corner_radius=0.25, width=2 * side - 0.16, height=side - 0.16) \
                .set_stroke(GREEN, 4).move_to(_p(kx, ky + side / 2))
            self.play(GrowFromCenter(small), run_time=1.0)
            c.wait_until("bigger groups")
            big = RoundedRectangle(corner_radius=0.3, width=2 * side - 0.12, height=2 * side - 0.12) \
                .set_stroke(GREEN, 4).move_to(_p(kx, ky))
            self.play(ReplacementTransform(small, big), run_time=1.5)

            c.wait_until("dnone")
            dt = d_exc_table().scale(0.85)
            dt.move_to(_p(4.65, -0.55))
            d_ttl = T("D flip-flop", 30, color=DIM).next_to(dt, UP, buff=0.3)
            self.play(*appear(dt, d_ttl, lag=0.2), run_time=1.0)
            self.play(FlashAround(dt, color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)
