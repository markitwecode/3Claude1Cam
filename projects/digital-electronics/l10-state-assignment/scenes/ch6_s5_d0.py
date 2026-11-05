"""Chapter 6, scene 5: simplifying D0 to r̄·(s0 + e), checked in a truth table, read on the diagram. Clips c6.dzero.1 – c6.dzero.4.

Opens from empty; ends on an empty frame.
Shared helpers (load_scene("ch6_s5_d0")):
- `final_line(size=FINAL_SIZE)`: ch6_s3's eq_line for `D_0 = \\overline{r}\\cdot(s_0 + e)` (no tags).
- `expanded_line(size=FINAL_SIZE)`: the bare `= \\overline{r}\\cdot s_0 + \\overline{r}\\cdot e` (built by expr()).
- `final_pair(size=FINAL_SIZE)`: VGroup(final_line, expanded_line) stacked, "=" signs aligned, centred
  on ORIGIN; .top .bottom.
- `truth_table(size=TABLE_SIZE)`: the check table, headers s_0 e | s̄0·e | s0 + s̄0·e | s0 + e, rows
  00 01 10 11; centred on ORIGIN (about 9.4 x 3.6). .heads (list of MathTex) .cells[r][c] (MathTex
  "0"/"1", FG) .rules (VGroup of Lines) .col_x .row_y.
- `expr(tokens, size)`: a single MathTex in eq_line's colours, "=" allowed as a token, "1" a factor
  (GREEN); .pieces.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch6_s3_inspect")
S2 = load_scene("ch6_s2_codes")
eq_line, put_line, raw_line, EQ_SIZE = S3.eq_line, S3.put_line, S3.raw_line, S3.EQ_SIZE

RB, S0B = r"\overline{r}", r"\overline{s_0}"


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- shared helpers
FINAL_SIZE = 52
TABLE_SIZE = 40
_SIGNS = ("+", "(", ")", "=")


def expr(tokens, size=EQ_SIZE):
    strings, kinds, prev = [], [], None
    for tok in tokens:
        is_f = tok not in _SIGNS
        if prev is not None and (prev not in _SIGNS or prev == ")") and (is_f or tok == "("):
            strings.append(r"\cdot")
            kinds.append("sign")
        strings.append(tok)
        if not is_f:
            kinds.append("sign")
        elif tok == "1":
            kinds.append("one")
        elif tok.startswith("s_") or tok.startswith(r"\overline{s"):
            kinds.append("state")
        else:
            kinds.append("input")
        prev = tok
    tex = MathTex(*strings, font_size=size)
    cols = {"sign": FG, "state": GREEN, "input": BLUE, "one": GREEN}
    for k, kind in enumerate(kinds):
        tex[k].set_color(cols[kind])
    tex.pieces = [tex[k] for k in range(len(strings))]
    tex.strings = strings
    return tex


def final_line(size=FINAL_SIZE):
    return eq_line("D_0", [RB, "(", "s_0", "+", "e", ")"], size=size, tags=False)


def expanded_line(size=FINAL_SIZE):
    return expr(["=", RB, "s_0", "+", RB, "e"], size)


def final_pair(size=FINAL_SIZE):
    top = final_line(size)
    bot = expanded_line(size)
    bot.shift(top.eqsign.get_center() - bot.pieces[0].get_center() + 0.0 * UP)
    bot.shift((top.tex.get_height() * 0.5 + 0.55 * size / 52 + bot.get_height() * 0.5) * DOWN)
    bot.shift((top.eqsign.get_x() - bot.pieces[0].get_x()) * RIGHT)
    g = VGroup(top, bot)
    g.move_to(ORIGIN)
    g.top, g.bottom = top, bot
    return g


TABLE_HEADS = ["s_0", "e", S0B + r"\cdot e", r"s_0 + " + S0B + r"\cdot e", "s_0 + e"]
TABLE_ROWS = [("0", "0", "0", "0", "0"), ("0", "1", "1", "1", "1"),
              ("1", "0", "0", "1", "1"), ("1", "1", "0", "1", "1")]
TABLE_COLS = (-3.85, -2.85, -1.05, 1.5, 3.95)
TABLE_PITCH = 0.72


def truth_table(size=TABLE_SIZE):
    heads = []
    for x, h in zip(TABLE_COLS, TABLE_HEADS):
        m = MathTex(h, font_size=size)
        m.set_color(FG)
        m.move_to(_p(x, 0))
        heads.append(m)
    heads[0].set_color(GREEN)
    heads[1].set_color(BLUE)
    hy = 1.45
    for m in heads:
        m.set_y(hy)
    row_y = [hy - 0.95 - k * TABLE_PITCH for k in range(4)]
    cells = []
    for r, row in enumerate(TABLE_ROWS):
        cells.append([MathTex(v, font_size=size, color=FG).move_to(_p(x, row_y[r]))
                      for x, v in zip(TABLE_COLS, row)])
    left, right = TABLE_COLS[0] - 0.6, TABLE_COLS[-1] + 0.9
    top, bot = hy + 0.45, row_y[-1] - 0.42
    rules = VGroup(Line(_p(left, hy - 0.5), _p(right, hy - 0.5)).set_stroke(DIM, 2))
    for xa, xb in ((TABLE_COLS[1], TABLE_COLS[2]), (TABLE_COLS[2], TABLE_COLS[3]), (TABLE_COLS[3], TABLE_COLS[4])):
        xm = (xa + xb) / 2
        if xa == TABLE_COLS[1]:
            xm = TABLE_COLS[1] + 0.55
        rules.add(Line(_p(xm, top), _p(xm, bot)).set_stroke(DIM, 2))
    g = VGroup(*heads, *[c for row in cells for c in row], rules)
    shift = -g.get_center()
    g.shift(shift)
    g.heads, g.cells, g.rules = heads, cells, rules
    g.col_x = [x + shift[0] for x in TABLE_COLS]
    g.row_y = [y + shift[1] for y in row_y]
    g.head_y = hy + shift[1]
    return g


# ---------------------------------------------------------------- local layout
LEFT_X = -3.3
ROW_Y = [2.65, 1.65, 0.65, -0.35]
WORK_Y = [-1.5, -2.55]
LAW_Y = -3.3
DIAG_K = 0.85
DIAG_C = _p(2.75, -0.1)


def corner_rule():
    r = eq_line(S0B, ["s_1", "+", "s_2"], size=36, tags=False)
    r.pieces[0].set_color(GREEN)
    r.to_corner(UL, buff=0.5)
    return r


def d_line(tokens):
    return eq_line("D_0", tokens, tags=False)


def small_diagram():
    d = S2.onehot_diagram()
    d.scale(DIAG_K, about_point=ORIGIN)
    grow = 29 / (32 * DIAG_K)
    for n in S2.STATES:
        d.name[n].scale(grow)
        d.code[n].scale(grow)
    d.shift(DIAG_C - d.get_center())
    return d


def row_box(table, r0, r1, color=YELLOW):
    ys = [table.row_y[r0], table.row_y[r1]]
    w = table.col_x[-1] - table.col_x[0] + 1.7
    h = abs(ys[0] - ys[1]) + 0.62
    box = Rectangle(width=w, height=h).set_stroke(color, 2).set_fill(color, 0.15)
    box.move_to(_p((table.col_x[0] + table.col_x[-1]) / 2 + 0.1, sum(ys) / 2))
    box.set_z_index(-1)
    return box


class SimplifyD0(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ factor out
    def clip1(self):
        with self.say("c6.dzero.1") as c:
            self.corner = corner_rule()
            L1 = put_line(d_line(S3.RAW["D_0"]), LEFT_X, ROW_Y[0])
            self.play(*appear(L1), run_time=1.0)  # early: the line is named as it is shown
            self.play(*appear(self.corner, shift=None), run_time=0.8)  # early: s4's rule, kept for reference
            c.wait_until("pair")
            pair = L1.terms[1] + [L1.plus[1]] + L1.terms[2]
            self.play(*recolor(pair, YELLOW), run_time=min(1.2, c.until("swap")))
            c.wait_until("swap")

            L2 = put_line(d_line(["s_0", RB, "+", "(", "s_1", "+", "s_2", ")", "e", RB]), LEFT_X, ROW_Y[1])
            self.play(*appear(L2, shift=0.4 * DOWN), *set_alpha([L1], 0.4), run_time=1.5)
            self.wait(0.3)
            brk = VGroup(*L2.pieces[6:11]).copy()
            self.play(FlashAround(brk, run_time=1.0, time_width=1.5),
                      FlashAround(self.corner.tex.copy(), run_time=1.0, time_width=1.5, color=GREEN),
                      run_time=1.0)
            L2b = put_line(d_line(["s_0", RB, "+", S0B, "e", RB]), LEFT_X, ROW_Y[1])
            self.play(*edit(L2.tex, L2b.tex), run_time=min(1.3, c.until("out")))
            self.remove(*L2.get_family())
            self.add(L2b)
            c.wait_until("out")

            rbars = [L2b.factors[1], L2b.factors[5]]
            self.play(*recolor(rbars, YELLOW), run_time=1.0)
            self.wait(0.4)
            L3 = put_line(d_line([RB, "(", "s_0", "+", S0B, "e", ")"]), LEFT_X, ROW_Y[2])
            L3.factors[0].set_color(YELLOW)
            self.play(*appear(L3, shift=0.4 * DOWN), run_time=min(1.5, c.until("bracket")))
            c.wait_until("bracket")
            self.box3 = token_box(L3.pieces[4:11], L3.tex, color=YELLOW)
            self.play(FadeIn(self.box3), *set_alpha([L2b], 0.4), run_time=1.0)
            self.L1, self.L2, self.L3 = L1, L2b, L3

    # ------------------------------------------------------------ the bracket simplifies
    def clip2(self):
        with self.say("c6.dzero.2") as c:
            L3 = self.L3
            W1 = expr(["s_0", "+", S0B, "e", "=", "(", "s_0", "+", S0B, ")", "(", "s_0", "+", "e", ")"])
            W1.shift(_p(L3.eqsign.get_x() - W1.pieces[5].get_x(), WORK_Y[0] - W1.pieces[5].get_y()))
            W0 = expr(["s_0", "+", S0B, "e"])
            W0.shift(W1.pieces[0].get_left() - W0.pieces[0].get_left())
            self.play(*fly(VGroup(*L3.pieces[5:10]), W0), *set_alpha([self.L1], 0.25),
                      run_time=min(1.5, c.until("law")))
            c.wait_until("law")

            law = VGroup(T("distributive law (OR over AND):", 30, DIM),
                         MathTex(r"A + B\cdot C = (A + B)\cdot(A + C)", font_size=36, color=FG))
            law.arrange(RIGHT, buff=0.3).move_to(_p(0, LAW_Y))
            self.play(*appear(law), run_time=1.0)
            c.wait_until("split")
            self.play(*edit(W0, W1), run_time=1.5)
            self.wait(0.6)
            L4 = put_line(d_line([RB, "(", "s_0", "+", S0B, ")", "(", "s_0", "+", "e", ")"]), LEFT_X, ROW_Y[3])
            self.play(*appear(L4, shift=0.4 * DOWN), run_time=min(1.5, c.until("one") - 0.3))
            c.wait_until("one")

            gbox = token_box(W1.pieces[6:11], W1, color=GREEN)
            self.play(FadeIn(gbox), run_time=0.8)
            W2 = expr(["=", "1", "(", "s_0", "+", "e", ")"])
            W2.shift(_p(W1.pieces[5].get_x() - W2.pieces[0].get_x(), WORK_Y[1] - W2.pieces[0].get_y()))
            derive(self, W1, W2, run_time=min(1.6, c.until("result")))
            c.wait_until("result")
            W3 = expr(["=", "s_0", "+", "e"])
            W3.shift(_p(W2.pieces[0].get_x() - W3.pieces[0].get_x(), WORK_Y[1] - W3.pieces[0].get_y()))
            self.play(*edit(W2, W3), run_time=min(1.3, c.until()))
            self.W1, self.W3 = W1, W3

    # ------------------------------------------------------------ check it in a table
    def clip3(self):
        with self.say("c6.dzero.3") as c:
            claim = expr(["s_0", "+", S0B, "e", "=", "s_0", "+", "e"], 48).move_to(_p(0, 3.05))
            tab = truth_table().move_to(_p(0, -0.15))
            frame = VGroup(*tab.heads, tab.rules)
            sweep_clear(self, keep=[self.W1, self.W3], run_time=1.0)
            self.play(*during(disappear(self.W1, self.W3), 0, 0.45),
                      *during(appear(claim, frame, shift=None), 0.5, 1), run_time=1.4)
            c.wait_until("It has only four rows")
            rows = [VGroup(*r) for r in tab.cells]
            self.play(*appear(*rows, lag=0.3, shift=None), run_time=1.4)
            c.wait_until("s0one")

            box = row_box(tab, 2, 3)
            hi = [tab.cells[r][k] for r in (2, 3) for k in (3, 4)]
            self.play(FadeIn(box), *recolor(hi, GOLD), run_time=1.0)
            c.wait_until("s0zero")
            box0 = row_box(tab, 0, 1)
            linked = [tab.cells[r][k] for r in (0, 1) for k in (1, 3, 4)]
            self.play(Transform(box, box0), *recolor(hi, FG), *recolor(linked, TEAL), run_time=1.3)
            c.wait_until("same")

            last = [tab.cells[r][k] for r in range(4) for k in (3, 4)]
            ticks = [check_mark().scale(0.8).move_to(_p(tab.col_x[-1] + 1.35, y)) for y in tab.row_y]
            self.play(FadeOut(box), *recolor(last, GREEN), *recolor([tab.cells[0][1], tab.cells[1][1]], FG),
                      run_time=1.0)
            self.play(*appear(*ticks, lag=0.15, shift=None), run_time=0.8)
            c.wait_until("rule")
            rule = MathTex(r"A + \overline{A}\cdot B = A + B", font_size=52, color=YELLOW).move_to(_p(0, -3.2))
            self.play(*appear(rule), run_time=1.0)
            self.rule = rule

    # ------------------------------------------------------------ the final line, read on the diagram
    def clip4(self):
        with self.say("c6.dzero.4") as c:
            pair = final_pair().move_to(_p(0, 0.2))
            sweep_clear(self, time_span(FadeIn(pair.top), 0.6, 1.2), keep=[self.rule])
            c.wait_until("Multiplied out")
            self.play(*appear(pair.bottom, shift=None), run_time=1.2)
            c.wait_until("meaning")

            d = small_diagram()
            pair.generate_target()
            pair.target.scale(44 / 52).move_to(_p(-4.85, 0.0))
            self.play(MoveToTarget(pair), *disappear(self.rule), run_time=1.3)
            self.play(*appear(d, shift=None), run_time=1.0)  # early: the whole diagram, then walked
            lit = [d.circle["Hunt"], d.arcs[3], d.arcs[7], d.arcs[2], d.labels[3], d.labels[7], d.labels[2]]
            for m in lit:
                m.save_state()
            c.wait_until("Hunt next")
            self.play(S2.glow_state(d, "Hunt"), run_time=1.0)
            c.wait_until("hunting already")
            self.play(S2.light_arc(d, 3), *recolor([d.labels[3]], YELLOW), run_time=1.0)
            c.wait_until("expecting it")
            self.play(S2.light_arc(d, 7), S2.light_arc(d, 2), *recolor([d.labels[7], d.labels[2]], YELLOW),
                      run_time=1.0)
            c.wait_until("stay")

            # the Hunt highlight goes off first, so no yellow arc leaves Sync while its loop is the topic
            self.play(*[Restore(m) for m in lit], run_time=0.8)
            self.play(*[VShowPassingFlash(d.arcs[i].copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for i in (0, 5)], run_time=1.2)
            z1 = MathTex("D_0", "=", "0", font_size=36)
            z2 = z1.copy()
            for z in (z1, z2):
                z[0].set_color(BLUE)
                z[2].set_color(GOLD)
            z1.next_to(d.labels[0], LEFT, buff=0.3)
            z2.next_to(d.labels[5], RIGHT, buff=0.35)
            self.play(*appear(z1, z2, lag=0.3), run_time=1.2)
