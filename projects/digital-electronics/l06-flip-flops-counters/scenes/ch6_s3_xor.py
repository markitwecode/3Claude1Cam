"""Chapter 6, scene 3: D1 is an exclusive or (Q1 | Q0 | D1 compared row by row). Clips c6.xor.1 – c6.xor.3."""
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


# ---- ch5_s6's mod_table() (copied verbatim) --------------------------------------------------
MT_GX = (-2.8, 0.0, 2.8)
MT_DX = 0.72
MT_DEC = -4.1
MT_SEPS = (-1.4, 1.4)
MT_TITLE_Y, MT_HEAD_Y, MT_RULE_Y = 3.45, 2.75, 2.35
MT_ROW0_Y, MT_PITCH = 1.9, 0.6
MT_TOP, MT_BOT = 3.8, -2.65
MT_CELL, MT_HEAD = 40, 42


def mt_row_y(i):
    return MT_ROW0_Y - i * MT_PITCH


def mod_table(filled=True, x=0.0):
    titles = VGroup(*[T(s, 30).move_to(_p(gx, MT_TITLE_Y))
                      for s, gx in zip(("Current state", "Next state", "FF inputs"), MT_GX)])
    head_tex = (["Q_2", "Q_1", "Q_0"], ["Q_2'", "Q_1'", "Q_0'"], ["D_2", "D_1", "D_0"])
    head_col = (GREEN, GREEN, BLUE)
    heads = VGroup(*[VGroup(*[MathTex(t, font_size=MT_HEAD, color=col).move_to(_p(gx + (j - 1) * MT_DX, MT_HEAD_Y))
                              for j, t in enumerate(ts)])
                     for ts, col, gx in zip(head_tex, head_col, MT_GX)])
    lines = VGroup(*[Line(_p(sx, MT_TOP), _p(sx, MT_BOT)).set_stroke(DIM, 2) for sx in MT_SEPS])
    lines.add(Line(_p(MT_DEC - 0.35, MT_RULE_Y), _p(MT_GX[2] + 1.35, MT_RULE_Y)).set_stroke(DIM, 2))
    skel = VGroup(titles, heads, lines)

    def bits_row(v, gx):
        return VGroup(*[MathTex(b, font_size=MT_CELL).move_to(_p(gx + (j - 1) * MT_DX, mt_row_y(i)))
                        for j, b in enumerate(format(v, "03b"))])
    dec, cur, nxt, inp = VGroup(), VGroup(), VGroup(), VGroup()
    for i in range(8):
        dec.add(MathTex(str(i), font_size=MT_CELL, color=GOLD).move_to(_p(MT_DEC, mt_row_y(i))))
        cur.add(bits_row(i, MT_GX[0]))
        nxt.add(bits_row((i + 1) % 8, MT_GX[1]))
        inp.add(bits_row((i + 1) % 8, MT_GX[2]))
    g = VGroup(skel, dec, cur, nxt, inp) if filled else VGroup(skel)
    for m in (skel, dec, cur, nxt, inp):
        m.shift(RIGHT * x)
    g.skel, g.titles, g.heads, g.lines = skel, titles, heads, lines
    g.dec, g.cur, g.nxt, g.inp = dec, cur, nxt, inp
    g.groups = [cur, nxt, inp]
    g.col = lambda gi, j: VGroup(*[row[j] for row in g.groups[gi]])
    return g


# ---- layout -----------------------------------------------------------------------------------
TX = -2.15                     # table placement: left edge at x = -6.6 (as in ch6 s1/s2/s4)
Q1X, Q0X, D1X = TX + MT_GX[0], TX + MT_GX[0] + MT_DX, TX + MT_GX[2]    # -4.95, -4.23, 0.65
# the comparison trio, right of the table
CQ1, CQ0, CSEP, CD1 = 2.55, 3.15, 3.52, 3.9
# the XOR truth table, right of the trio, rows level with rows 1-4
XA, XB, XSEP, XR = 4.75, 5.25, 5.55, 6.1
BAND = -3.05                   # clear band under the table the copies travel through
Q1_BITS = [(i >> 1) & 1 for i in range(8)]
Q0_BITS = [i & 1 for i in range(8)]
D1_BITS = [((i + 1) >> 1) & 1 for i in range(8)]


def train(srcs, xs_lane, xd_lane, x_dst, color_to=None):
    """Copies of `srcs` (cells of one table column) travel: step sideways into the lane next to
    their column, down the lane to the clear band under the table, along it, up the lane next to
    the destination column and into their row there. All move at one speed, so the column
    travels as a train with its spacing kept and never passes over another digit."""
    copies, paths = [], []
    for s in srcs:
        y = s.get_y()
        pts = [s.get_center(), _p(xs_lane, y), _p(xs_lane, BAND), _p(xd_lane, BAND), _p(xd_lane, y), _p(x_dst, y)]
        segs = [np.linalg.norm(b - a) for a, b in zip(pts[:-1], pts[1:])]
        copies.append(s.copy())
        paths.append((pts, segs, sum(segs)))
    lmax = max(p[2] for p in paths)
    c0 = ManimColor(srcs[0].get_color())

    def make(pts, segs, total):
        w0 = [None]

        def f(m, dist):
            if w0[0] is None:
                w0[0] = m.width
            dd = min(dist, total)
            m.scale(w0[0] * (1 - 0.2 * min(1, dd / 0.4, (total - dd) / 0.4)) / m.width)
            d = dd
            for k, sl in enumerate(segs):
                if d <= sl or k == len(segs) - 1:
                    u = 0 if sl == 0 else min(d / sl, 1)
                    m.move_to(pts[k] + u * (pts[k + 1] - pts[k]))
                    break
                d -= sl
            if color_to is not None:
                w = np.clip((dd / total - 0.3) / 0.4, 0, 1)
                m.set_color(interpolate_color(c0, ManimColor(color_to), w))
        return f
    out = [(m, make(*p)) for m, p in zip(copies, paths)]
    return (out, lmax), VGroup(*copies)


def play_train(scene, train_, run_time, last=(), parts=7, step=0.36):
    """Plays a train: a quick lift (the copies leave their sources at once, no doubled digits),
    then the travel in `parts` short plays (one smooth progress overall), so each play's stretch
    of path is nearly straight; `last` (time_span'd to its end) rides on the final part."""
    movers, lmax = train_
    scene.play(*[UpdateFromAlphaFunc(m, (lambda f: lambda mm, a: f(mm, step * a))(f), rate_func=rush_from)
                 for m, f in movers], run_time=0.3)
    rt = (run_time - 0.3) / parts
    for k in range(parts):
        def g(f, k=k):
            return lambda m, a: f(m, step + (lmax - step) * smooth((k + a) / parts))
        extra = [time_span(FadeIn(x), max(0.0, rt - 0.3), rt) for x in last] if k == parts - 1 else []
        scene.play(*[UpdateFromAlphaFunc(m, g(f), rate_func=linear) for m, f in movers], *extra, run_time=rt)


def row_box(i0, i1=None, color=YELLOW):
    """Highlight box round trio rows i0..i1 (all three columns)."""
    i1 = i0 if i1 is None else i1
    top, bot = mt_row_y(i0) + 0.27, mt_row_y(i1) - 0.27
    r = Rectangle(width=CD1 - CQ1 + 0.75, height=top - bot).move_to(_p((CQ1 + CD1) / 2, (top + bot) / 2))
    return r.set_stroke(color, 2).set_fill(color, 0.15).set_z_index(-1)


def xor_table():
    heads = VGroup(MathTex("A", font_size=MT_HEAD).move_to(_p(XA, MT_HEAD_Y)),
                   MathTex("B", font_size=MT_HEAD).move_to(_p(XB, MT_HEAD_Y)),
                   MathTex("A", r"\oplus", "B", font_size=34).move_to(_p(XR, MT_HEAD_Y)))
    heads[2][1].set_color(YELLOW)
    rows = VGroup()
    for i in range(4):
        a, b = i >> 1, i & 1
        rows.add(VGroup(*[MathTex(str(v), font_size=MT_CELL).move_to(_p(x, mt_row_y(i)))
                          for v, x in ((a, XA), (b, XB), (a ^ b, XR))]))
    bot = mt_row_y(3) - 0.38
    lines = VGroup(Line(_p(XSEP, 3.1), _p(XSEP, bot)).set_stroke(DIM, 2),
                   Line(_p(XA - 0.3, MT_RULE_Y), _p(6.6, MT_RULE_Y)).set_stroke(DIM, 2))
    title = T("XOR", 30, YELLOW).move_to(_p((XA + XR) / 2, MT_TITLE_Y))
    g = VGroup(title, heads, rows, lines)
    g.title, g.heads, g.rows, g.lines = title, heads, rows, lines
    return g


class XorD1(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---- c6.xor.1: D1 reads 0 1 1 0 0 1 1 0; Q1, Q0, D1 copied out side by side ---------------
    def clip1(self):
        tab = self.tab = mod_table(filled=True, x=TX)
        d1_cells = tab.col(2, 1)
        self.d1box = SurroundingRectangle(VGroup(tab.heads[2][1], d1_cells), color=BLUE, buff=0.12).set_stroke(BLUE, 3)
        self.play(FadeIn(tab), run_time=0.8)   # early: the table returns whole from the earlier scenes
        with self.say("c6.xor.1") as c:
            # {d1}: the D1 column boxed
            self.play(FadeIn(self.d1box), run_time=0.3)
            c.wait_until("read")
            # {read}: its entries light on their spoken words
            words = [("zero", 0), ("one", 1), ("one", 2), ("zero", 1), ("zero", 2), ("one", 3), ("one", 4), ("zero", 3)]
            offs = [max(0.0, c.at(w, nth=n) - c.at("read")) for w, n in words]
            self.play(*[time_span(cell.animate.set_color(YELLOW), t, t + 0.4) for cell, t in zip(d1_cells, offs)],
                      run_time=offs[-1] + 0.4)
            c.wait_until("pair")
            # {pair}: the source columns boxed; the Q1 | Q0 | D1 group fades in, already in place
            th = self.trio_heads = VGroup(MathTex("Q_1", font_size=MT_HEAD, color=GREEN).move_to(_p(CQ1, MT_HEAD_Y)),
                                          MathTex("Q_0", font_size=MT_HEAD, color=GREEN).move_to(_p(CQ0, MT_HEAD_Y)),
                                          MathTex("D_1", font_size=MT_HEAD, color=BLUE).move_to(_p(CD1, MT_HEAD_Y)))
            self.trio_lines = VGroup(Line(_p(CSEP, 3.1), _p(CSEP, MT_BOT)).set_stroke(DIM, 2),
                                     Line(_p(CQ1 - 0.35, MT_RULE_Y), _p(CD1 + 0.35, MT_RULE_Y)).set_stroke(DIM, 2))

            def col_copy(src, x):
                return VGroup(*[m.copy().set_color(FG).set_x(x) for m in src])
            self.cq1 = col_copy(tab.col(0, 1), CQ1)
            self.cq0 = col_copy(tab.col(0, 2), CQ0)
            self.cd1 = col_copy(d1_cells, CD1)

            def cbox(head, cells, color):
                return SurroundingRectangle(VGroup(head, cells), color=color, buff=0.12).set_stroke(color, 3)
            sboxes = [cbox(VGroup(tab.heads[0][1], tab.heads[0][2]), VGroup(tab.col(0, 1), tab.col(0, 2)), GREEN)]
            self.dboxes = VGroup(cbox(th[:2], VGroup(self.cq1, self.cq0), GREEN), cbox(th[2], self.cd1, BLUE))
            self.play(*[FadeIn(bx) for bx in sboxes], run_time=min(1.0, c.until("beside it")))
            c.wait_until("beside it")
            self.play(*appear(VGroup(th, self.trio_lines, self.cq1, self.cq0, self.cd1), self.dboxes, shift=None, lag=0.3),
                      run_time=min(1.5, c.until("compare them")))
            c.wait_until("compare them")
            self.play(*[FadeOut(bx) for bx in sboxes], run_time=min(1.0, c.until(floor=0.3)))

    # ---- c6.xor.2: rows compared; the rule; XOR; D1 = Q0 xor Q1; rows 5-8 repeat ---------------
    def clip2(self):
        cq1, cq0, cd1 = self.cq1, self.cq0, self.cd1

        def row_colors(i):
            col = YELLOW if Q1_BITS[i] != Q0_BITS[i] else DIM
            return col

        with self.say("c6.xor.2") as c:
            box = row_box(0)
            # {r1}: table dims, row 1 boxed, the pair glows
            self.play(*set_alpha([self.tab, self.d1box], 0.35), FadeIn(box), FadeOut(self.dboxes),
                      *recolor([cq1[0], cq0[0]], row_colors(0)), run_time=min(1.2, c.until("dee one is")))
            for i in range(4):
                if i > 0:
                    c.wait_until(f"r{i + 1}")
                    self.play(Transform(box, row_box(i)), *recolor([cq1[i], cq0[i]], row_colors(i)),
                              run_time=min(1.0, c.until("dee one is", nth=i)))
                c.wait_until("dee one is", nth=i)
                self.play(*recolor([cd1[i]], row_colors(i)), FlashAround(cd1[i], color=row_colors(i), buff=0.12),
                          run_time=min(1.0, c.until(f"r{i + 2}" if i < 3 else "rule")))
            c.wait_until("rule")
            # {rule}
            rule = MathTex(r"D_1 = 1", r"\text{ exactly when }", r"Q_1 \neq Q_0", font_size=34)
            rule[0].set_color(BLUE)
            rule[2].set_color(YELLOW)
            rule.move_to(_p(4.25, -3.25))
            self.play(FadeOut(box), *appear(rule), run_time=min(0.9, c.until("name")))
            c.wait_until("name")
            # {name}: the XOR truth table slides in, row for row with ours
            xt = self.xt = xor_table()
            self.play(*appear(xt.title, xt.heads, xt.lines, xt.rows, shift=0.4 * LEFT, lag=0.15),
                      run_time=min(1.6, c.until("equals cue zero")))
            c.wait_until("equals cue zero")
            also = VGroup(T("Also,", 32),
                          MathTex("D_1", "=", "Q_0", r"\oplus", "Q_1", font_size=48)).arrange(RIGHT, buff=0.3)
            also[1][0].set_color(BLUE)
            also[1][2].set_color(GREEN)
            also[1][4].set_color(GREEN)
            also[1][3].set_color(YELLOW)
            also.move_to(_p(4.35, -3.25))
            self.also = also
            self.play(*swap(rule, also), run_time=min(1.4, c.until("rest")))
            c.wait_until("rest")
            # {rest}: rows 5-8 light together, the same pattern
            box2 = self.box2 = row_box(4, 7)
            anims = [FadeIn(box2)]
            for i in range(4, 8):
                anims += recolor([cq1[i], cq0[i], cd1[i]], row_colors(i))
            self.play(*anims, run_time=min(1.4, c.until(floor=0.5)))

    # ---- c6.xor.3: xor with 0 keeps, with 1 flips; Q1 flips after every Q0 = 1 -------------------
    def clip3(self):
        cq1, cq0, cd1 = self.cq1, self.cq0, self.cd1
        with self.say("c6.xor.3") as c:
            # {words}: the XOR table makes way for two lines
            l1 = MathTex("Q", r"\oplus", "0", "=", "Q", font_size=40)
            l2 = MathTex("Q", r"\oplus", "1", "=", r"\overline{Q}", font_size=40)
            for l in (l1, l2):
                l[1].set_color(YELLOW)
            l1.move_to(_p(5.45, 2.3))
            l2.move_to(_p(5.45, 0.5))
            keep = T("keep", 30, GREEN).next_to(l1, DOWN, buff=0.25)
            flip = T("flip", 30, YELLOW).next_to(l2, DOWN, buff=0.25)
            resets = [FadeOut(self.box2)]
            for i in range(8):
                resets += recolor([cq1[i], cq0[i]], FG)
            resets += recolor(list(cd1), DIM)
            self.play(*swap(self.xt, VGroup(l1, l2)), *resets, run_time=min(1.4, c.until("keeps a bit")))
            c.wait_until("keeps a bit")
            self.play(*appear(keep), run_time=min(1.0, c.until("flips it")))
            c.wait_until("flips it")
            self.play(*appear(flip), run_time=min(1.0, c.until("so when cue zero is zero")))
            c.wait_until("so when cue zero is zero")
            # {hold}: only the hold idea: the keep line boxed, the Q0 = 0 rows' Q0 cells boxed GREEN
            wbox = SurroundingRectangle(VGroup(l1, keep), color=GREEN, buff=0.15).set_stroke(GREEN, 2)
            zboxes = [SurroundingRectangle(cq0[i], color=GREEN, buff=0.1).set_stroke(GREEN, 2) for i in (0, 2, 4, 6)]
            self.play(FadeIn(wbox), *[FadeIn(b) for b in zboxes],
                      run_time=min(1.2, c.until("and when cue zero is one")))
            c.wait_until("and when cue zero is one")
            # {flip}: box slides to the flip line; arrows wherever Q1 changes
            arrows = VGroup()
            ax = CQ1 - 0.2
            for i in (1, 3, 5):
                arrows.add(CurvedArrow(_p(ax, mt_row_y(i) - 0.04), _p(ax, mt_row_y(i + 1) + 0.04), angle=0.9 * PI,
                                       color=YELLOW, stroke_width=4, tip_length=0.12))
            wx = 1.82
            y8, y1 = mt_row_y(7), mt_row_y(0)
            yb = y8 - 0.42             # leaves from below row 8, clear of its digit
            path = VMobject().set_points_as_corners([_p(CQ1 - 0.05, yb), _p(wx, yb), _p(wx, y1), _p(wx + 0.12, y1)])
            path.set_stroke(YELLOW, 4)
            head = Arrow(_p(wx + 0.1, y1), _p(ax, y1), buff=0, stroke_width=4, tip_length=0.15,
                         max_tip_length_to_length_ratio=0.5, color=YELLOW)
            wrap = VGroup(path, head)
            arrows.add(wrap)
            fbox = SurroundingRectangle(VGroup(l2, flip), color=YELLOW, buff=0.15).set_stroke(YELLOW, 2)
            self.play(*during([FadeOut(wbox)], 0, 0.3), *during([FadeIn(fbox)], 0.3, 0.6),
                      *during([FadeOut(b) for b in zboxes], 0, 0.3),
                      LaggedStart(*[Create(a) for a in arrows[:3]],
                                  Succession(Create(path), GrowArrow(head)), lag_ratio=0.3),
                      run_time=min(2.0, c.until("check it on the table")))
            c.wait_until("check it on the table")
            # {check}: the Q0 = 1 entry in each arrow's starting row lights
            self.play(*recolor([cq0[i] for i in (1, 3, 5, 7)], YELLOW),
                      *[FadeIn(SurroundingRectangle(cq0[i], color=YELLOW, buff=0.1).set_stroke(YELLOW, 2))
                        for i in (1, 3, 5, 7)],
                      run_time=min(1.4, c.until("every time cue one changes")))
