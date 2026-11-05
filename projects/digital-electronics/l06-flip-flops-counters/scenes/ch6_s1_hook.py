"""Chapter 6, scene 1: hook: the modified table, D = Q', the logic block, three tools. Clips c6.hook.1 – c6.hook.2."""
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- ch5_s6_modtable's mod_table() (copied verbatim) -----------------------------------------
MT_GX = (-2.8, 0.0, 2.8)      # column-group centres (current, next, FF inputs), rel. to x
MT_DX = 0.72                  # column pitch inside a group (bit 2, 1, 0 at -DX, 0, +DX)
MT_DEC = -4.1                 # GOLD decimal column, rel. to x
MT_SEPS = (-1.4, 1.4)         # vertical rules between the groups, rel. to x
MT_TITLE_Y, MT_HEAD_Y, MT_RULE_Y = 3.45, 2.75, 2.35
MT_ROW0_Y, MT_PITCH = 1.9, 0.6                 # data row i at y = 1.9 - 0.6 i (row 7 at -2.3)
MT_TOP, MT_BOT = 3.8, -2.65
MT_CELL, MT_HEAD = 40, 42                      # MathTex sizes of data cells / column headers


def mt_row_y(i):
    return MT_ROW0_Y - i * MT_PITCH


def mod_table(filled=True, x=0.0):
    """The counter's modified state transition table (slide p. 99), in ch3_s3 jk_table()'s cell
    styling (MathTex cells, DIM stroke-2 rules). Absolute y (titles 3.45, headers 2.75, rows
    1.9 - 0.6 i); the Next-state group is centred at `x` (this scene ends with x = 0: the table
    spans about x -4.25 .. 4.05, 8.3 wide).
    Titles "Current state" / "Next state" / "FF inputs" (T 30, FG); headers Q2 Q1 Q0 and
    Q2' Q1' Q0' GREEN, D2 D1 D0 BLUE (MathTex 42); data cells FG MathTex 40, decimals 0..7 GOLD.
    The returned VGroup holds .skel (= VGroup(titles, heads, lines)) and, if filled, .dec .cur
    .nxt .inp too; the data rows are always built and reachable as attributes (filled=False:
    the empty skeleton, rows ready to be animated in).
    .titles[g], .heads[g] (VGroup of 3), .lines, .dec[i], .cur[i] / .nxt[i] / .inp[i] (VGroup of
    3 cells, bit 2 first), .groups = [cur, nxt, inp], .col(g, j) -> VGroup of column j of group g."""
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


# ---- ch5_s2_sync's make_ff / sync_structure() (copied verbatim) ----------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
CH_X = (-4.3, 0.0, 4.3)
FEED_Y = -BOX_H / 2 - EN_WIRE          # -2.3: the clock bus
STUB_Y = 1.75


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.1))
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.2)).set_stroke(YELLOW, 5)
    else:
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


def sync_structure(k=0.85, center=_p(0, -0.5)):
    """Three D flip-flops on one clock, a combinational-logic box above, Q wires up, D wires down.
    Parts: .ffs .bus .jdot .clk_l .q_labels .d_labels .q_up .d_down .box .box_l .cur_l .next_l
    .cur_br .next_br (thin brackets across the three Q / the three D wires, the labels at their ends);
    .core = VGroup(ffs, bus, jdot, clk_l) (s1's end shot); .q_spot(i) / .d_spot(i): where a GOLD/GREEN
    value digit sits just above Q_i's / D_i's pin wire (outside the box); .clk_paths(): fresh
    YELLOW paths (bus, then each clock wire) for a clock pulse."""
    ffs = [make_ff(_p(x, 0)) for x in CH_X]
    bus = Line(_p(CH_X[0], FEED_Y), _p(CH_X[2], FEED_Y)).set_stroke(YELLOW, 5)
    jdot = Dot(_p(CH_X[1], FEED_Y), radius=0.09, color=YELLOW)
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    q_labels = [MathTex(f"Q_{i}", font_size=48, color=GREEN).move_to(_p(x + 1.15, 1.85))
                for i, x in enumerate(CH_X)]
    d_labels = [MathTex(f"D_{i}", font_size=48, color=BLUE).move_to(_p(x - 1.15, 1.85))
                for i, x in enumerate(CH_X)]
    box_y0, box_h = 3.45, 1.2
    box = RoundedRectangle(corner_radius=0.3, width=12.4, height=box_h).set_stroke(BLUE, 4)
    box.set_fill(BG, 1).move_to(_p(0, box_y0 + box_h / 2))
    box_l = T("combinational logic", 52, FG).move_to(box)
    q_up = [poly([(x + BOX_W / 2 + WIRE, PIN_Y), (x + BOX_W / 2 + WIRE, box_y0)], GREEN) for x in CH_X]
    d_down = [poly([(x - BOX_W / 2 - WIRE, box_y0), (x - BOX_W / 2 - WIRE, PIN_Y)], BLUE) for x in CH_X]
    qx = [x + BOX_W / 2 + WIRE for x in CH_X]
    dx = [x - BOX_W / 2 - WIRE for x in CH_X]

    def bracket(x0, x1, y, color):
        cap = 0.16
        br = VGroup(Line(_p(x0, y), _p(x1, y)), Line(_p(x0, y - cap), _p(x0, y + cap)),
                    Line(_p(x1, y - cap), _p(x1, y + cap))).set_stroke(color, 2.5)
        br.set_z_index(-1)
        return br
    cur_br = bracket(qx[0], qx[2], 3.12, GREEN)          # across the three Q wires
    next_br = bracket(dx[0], dx[2], 2.5, BLUE)          # across the three D wires
    cur_l = T("current state", 35, GREEN).next_to(_p(qx[0], 3.12), LEFT, buff=0.2)
    next_l = T("next state", 35, BLUE).next_to(_p(dx[2], 2.5), RIGHT, buff=0.2)
    # spots for value digits (unscaled), moved along with the group by invisible dots
    q_pts = [Dot(_p(x + 1.15, 1.08), radius=0.01).set_opacity(0) for x in CH_X]
    d_pts = [Dot(_p(x - 1.15, 1.08), radius=0.01).set_opacity(0) for x in CH_X]
    g = VGroup(*ffs, bus, jdot, clk_l, *q_labels, *d_labels, *q_up, *d_down, box, box_l, cur_br, cur_l, next_br, next_l,
               *q_pts, *d_pts)
    g.scale(k, about_point=ORIGIN).shift(center)
    g.ffs, g.bus, g.jdot, g.clk_l, g.q_labels, g.d_labels = ffs, bus, jdot, clk_l, q_labels, d_labels
    g.q_up, g.d_down, g.box, g.box_l, g.cur_l, g.next_l = q_up, d_down, box, box_l, cur_l, next_l
    g.cur_br, g.next_br = cur_br, next_br
    g.core = VGroup(*ffs, bus, jdot, clk_l)
    g.q_spot = lambda i: q_pts[i].get_center()
    g.d_spot = lambda i: d_pts[i].get_center()

    def clk_paths():
        return ([bus.copy().set_stroke(YELLOW, 10)],
                [f.clk_w.copy().set_stroke(YELLOW, 10) for f in ffs])
    g.clk_paths = clk_paths
    return g


# =============================================================================================
# Scene-only helpers and layout
# =============================================================================================
TAB_K = 0.45                 # the table shrinks to this as it leaves for the upper left
ST_K, ST_C = 0.85, _p(0, -0.4)   # the logic structure while the question is asked
EQ_Y = -3.4                  # the D_i = ... row, one under each flip-flop
ROW = 3                      # the row that lights: 011 -> 100 -> 100


def group_box(tab, g, color):
    """A box round a whole column group (title, headers, all eight rows)."""
    box = SurroundingRectangle(VGroup(tab.titles[g], tab.heads[g], tab.groups[g]), color=color, buff=0.14)
    return box.set_stroke(color, 3).set_fill(color, 0.1).set_z_index(-1)


def row_box(tab, i, color=YELLOW):
    box = SurroundingRectangle(VGroup(tab.dec[i], tab.cur[i], tab.inp[i]), color=color, buff=0.12)
    return box.set_stroke(color, 3).set_fill(color, 0.12).set_z_index(-1)


def fn_eq(i, rhs=None):
    """D_i = f(Q_2, Q_1, Q_0)  (rhs None), or D_i = ?  (rhs '?')."""
    if rhs is None:
        m = MathTex(f"D_{i}", "=", "f(", "Q_2", ",", "Q_1", ",", "Q_0", ")", font_size=36)
        for k in (3, 5, 7):
            m[k].set_color(GREEN)
    else:
        m = MathTex(f"D_{i}", "=", rhs, font_size=40)
        m[2].set_color(YELLOW)
    m[0].set_color(BLUE)
    return m


def chip(text):
    lab = T(text, 40)
    box = RoundedRectangle(corner_radius=0.18, width=lab.width + 0.6, height=1.0).set_stroke(FG, 3)
    box.move_to(lab)
    g = VGroup(box, lab)
    g.box, g.lab = box, lab
    return g


class Hook(NarratedScene):
    def construct(self):
        card = self.card = title_card("Part 6 · From table to circuit")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        self.wait(0.3)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(FadeIn(card.course), run_time=0.6)  # early: title card
        self.play(FadeIn(card.part), run_time=0.6)  # early: title card
        self.wait(3.6)
        self.tab = mod_table(filled=True, x=0.0)
        self.clip1()
        self.clip2()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c6.hook.1
    def clip1(self):
        tab, card = self.tab, self.card
        with self.say("c6.hook.1") as c:
            # {title}: the card holds, then the table returns as ch5 s6 left it
            c.wait_until("modified")
            self.play(*disappear(card.title, card.rule, card.course, card.part), run_time=0.8)
            self.play(*appear(tab, shift=None), run_time=1.2)  # early: the table returns whole
            c.wait_until("zero to seven")
            dbox = SurroundingRectangle(tab.dec, color=GOLD, buff=0.14).set_stroke(GOLD, 3)
            dbox.set_fill(GOLD, 0.1).set_z_index(-1)
            self.play(FadeIn(dbox), run_time=0.8)
            c.wait_until("table")

            # {table}: one row lights, arrows current -> next -> inputs
            rbox = row_box(tab, ROW)
            y = mt_row_y(ROW)
            a1 = Arrow(_p(MT_SEPS[0] - 0.45, y), _p(MT_SEPS[0] + 0.45, y), buff=0, stroke_width=5,
                       color=YELLOW, max_tip_length_to_length_ratio=0.35)
            a2 = Arrow(_p(MT_SEPS[1] - 0.45, y), _p(MT_SEPS[1] + 0.45, y), buff=0, stroke_width=5,
                       color=YELLOW, max_tip_length_to_length_ratio=0.35)
            self.play(FadeOut(dbox), FadeIn(rbox), run_time=1.0)
            c.wait_until("next state")
            self.play(GrowArrow(a1), run_time=0.9)
            c.wait_until("flip-flop inputs")
            self.play(GrowArrow(a2), run_time=0.9)
            c.wait_until("equal")

            # {equal}: the next-state and FF-inputs blocks flash together; D = Q'
            nbox, ibox = group_box(tab, 1, GREEN), group_box(tab, 2, BLUE)
            self.play(*disappear(rbox, a1, a2), run_time=0.6)
            self.play(FadeIn(nbox), FadeIn(ibox),
                      FlashAround(nbox, run_time=1.6, time_width=1.5, color=GREEN),
                      FlashAround(ibox, run_time=1.6, time_width=1.5, color=BLUE), run_time=1.6)
            eq = set_backstroke(MathTex("=", font_size=72, color=YELLOW), width=14)
            eq.move_to(_p(MT_SEPS[1], (mt_row_y(0) + mt_row_y(7)) / 2))
            rule = MathTex("D", "=", "Q'", font_size=56, color=YELLOW).move_to(_p(MT_SEPS[1], -3.25))
            self.play(*appear(eq, shift=None), *appear(rule), run_time=1.0)
            self.eqs = [eq, rule, nbox]
            self.ibox = ibox

    # ------------------------------------------------------------------ c6.hook.2
    def clip2(self):
        tab = self.tab
        S = self.S = sync_structure(k=ST_K, center=ST_C)
        with self.say("c6.hook.2") as c:
            # {logic}: only the inputs stay lit
            self.play(FlashAround(self.ibox, run_time=1.5, time_width=1.5, color=BLUE), run_time=1.5)
            c.wait_until("block")

            # {block}: the table shrinks away to the upper left, the structure comes in
            self.play(*during(disappear(self.ibox, *self.eqs), 0, 0.3),
                      *during([FadeOut(tab, shift=_p(-4.6, 2.2), scale=TAB_K)], 0.05, 0.55),
                      *during(appear(*S.ffs, S.bus, S.jdot, S.clk_l, shift=None, lag=0.1), 0.4, 0.75),
                      *during(appear(*S.q_up, *S.d_down, S.box, S.box_l, *S.q_labels, *S.d_labels,
                                     S.cur_br, S.cur_l, S.next_br, S.next_l, shift=None, lag=0.03), 0.7, 1.0),
                      run_time=2.6)  # early: the structure shown whole
            settle(self, S)
            c.wait_until("outputs")
            self.play(*[VShowPassingFlash(w.copy().set_stroke(GREEN, 9), time_width=0.6) for w in S.q_up],
                      run_time=1.2)
            c.wait_until("inputs")
            self.play(*[VShowPassingFlash(w.copy().set_stroke(BLUE, 9), time_width=0.6) for w in S.d_down],
                      run_time=1.2)
            c.wait_until("function")

            # {function}: D_i = f(Q_2, Q_1, Q_0), each under its flip-flop
            eqs = [fn_eq(i) for i in range(3)]
            for k, e in enumerate(eqs):
                e.move_to(_p(S.ffs[k].box.get_x(), EQ_Y))
            self.play(*appear(*eqs, lag=0.5), run_time=min(2.0, c.until("current state")))
            c.wait_until("current state")
            self.play(*[VShowPassingFlash(w.copy().set_stroke(GREEN, 9), time_width=0.6) for w in S.q_up],
                      S.box.animate.set_stroke(YELLOW, 6), run_time=1.4)
            q = T("?", 96, YELLOW).move_to(S.box)
            self.play(S.box.animate.set_stroke(BLUE, 4 * ST_K), *swap(S.box_l, q), run_time=1.2)  # early: the question, asked in the pause
            c.wait_until("question")

            # {question}: each f(...) becomes ?
            new = [fn_eq(i, "{?}") for i in range(3)]
            for e, n in zip(eqs, new):
                n.move_to(e)
            self.play(*[a for e, n in zip(eqs, new) for a in edit(e, n)], run_time=1.2)
            c.wait_until("for the job")

            # {tools}: three chips, one per word
            chips = [chip(s) for s in ("inspection", "Boolean algebra", "K-maps")]
            for k, ch in enumerate(chips):
                ch.move_to(_p(0, 1.3 - 1.4 * k))
            sweep_clear(self, run_time=1.0)
            for ch, cue in zip(chips, ("inspection", "boolean", "kay-maps")):
                c.wait_until(own_word=ch.lab, cue=cue)
                self.play(*appear(ch), run_time=0.8)
            c.wait_until("all")

            # {all}: they line up as the chapter's road; the counter at its end
            gap = 0.9
            total = sum(ch.width for ch in chips) + gap * 2
            x = -total / 2
            road_y = 0.0
            for ch in chips:
                ch.generate_target()
                ch.target.move_to(_p(x + ch.width / 2, road_y))
                x += ch.width + gap
            arrows = [Arrow(_p(chips[k].target.get_right()[0] + 0.1, road_y),
                            _p(chips[k + 1].target.get_left()[0] - 0.1, road_y),
                            buff=0, stroke_width=4, color=DIM, max_tip_length_to_length_ratio=0.3)
                      for k in range(2)]
            self.play(*[MoveToTarget(ch) for ch in chips], run_time=1.5)
            self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)
