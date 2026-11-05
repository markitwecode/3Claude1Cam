"""Chapter 6, scene 3: one-hot next-state equations read straight off the table (p. 142). Clips c6.inspect.1 – c6.inspect.4.

Opens on ch6_s2_codes.handover_shot(); ends on handover_shot() = d_stack() (s4 opens on it).
Shared helpers (load_scene("ch6_s3_inspect")): the chapter's equation style.
- `eq_line(lhs, tokens, size=EQ_SIZE, tags=True)`: one equation as a single MathTex (one piece per
  token). lhs e.g. "D_2" (BLUE) then "=", or None for a bare expression. tokens: factors and the
  signs "+", "(", ")"; a factor starting "s_" or "\\overline{s" is a state variable (GREEN),
  anything else an input (BLUE); "\\cdot" is put between adjacent factors (and before "(" / after
  ")"). tags: True = a YELLOW T 28 state-name tag (Sync/Sight/Hunt) under each plain s_k; "all" =
  under overlined ones too; False = none. Tags share one y, 0.12 under the lowest variable.
  Attrs .tex .pieces (all MathTex pieces in order) .lhs (VGroup D,= or None) .eqsign .factors
  (one piece per token, None for signs) .terms (list of piece lists, split at top-level +)
  .plus (top-level + pieces) .tags (VGroup) .term_tags (list of tag lists per term).
- `put_line(line, left_x, y)`: moves a line so its first piece's left edge is at left_x and its
  "=" (or its tex centre if no lhs) sits at height y. Returns line.
- `RAW[lhs]`: the token lists of p. 142's D_2, D_1, D_0. `raw_line(lhs, size=EQ_SIZE)`.
- Build position here: size 44, left edge x EQ_LEFT (-0.4), "=" at y LINE_Y (D_2 1.6,
  D_1 0.0, D_0 -1.6); right of the table.
- `d_stack(size=STACK_SIZE)`: the final shot: VGroup(lines, names); .lines = VGroup(D_2, D_1, D_0
  lines, size 52, "=" signs aligned, pitch 1.55), .names = VGroup of YELLOW T 32 line names
  (Sync, Sight, Hunt) right-aligned 0.4 left of the D's. Centred on ORIGIN: x -4.4..4.4, y 2.1..-2.1.
- `handover_shot()`: d_stack().
"""
# style: 2
# handover: next
import re
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

S2 = load_scene("ch6_s2_codes")
S5 = load_scene("ch5_s5_table")
S6 = load_scene("ch5_s6_d1")
S7 = load_scene("ch5_s7_d0")


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- shared: the equation style
EQ_SIZE = 44
STACK_SIZE = 52
TAG_SIZE = 28
STATE_TAG = {"s_2": "Sync", "s_1": "Sight", "s_0": "Hunt"}
LINE_NAME = {"D_2": "Sync", "D_1": "Sight", "D_0": "Hunt"}
SIGNS = ("+", "(", ")")
RAW = {
    "D_2": ["s_1", "e", "r", "+", "s_2", r"\overline{e}", "+", "s_2", "e", "r"],
    "D_1": ["s_0", "r", "+", "s_1", r"\overline{e}"],
    "D_0": ["s_0", r"\overline{r}", "+", "s_1", "e", r"\overline{r}", "+", "s_2", "e", r"\overline{r}"],
}
EQ_LEFT = -0.4
LINE_Y = {"D_2": 1.6, "D_1": 0.0, "D_0": -1.6}


def _is_state(tok):
    return tok.startswith("s_") or tok.startswith(r"\overline{s")


def eq_line(lhs, tokens, size=EQ_SIZE, tags=True):
    strings, kinds, tok_of = [], [], []
    if lhs:
        strings += [lhs, "="]
        kinds += ["lhs", "eq"]
        tok_of += [None, None]
    prev = None
    for ti, tok in enumerate(tokens):
        is_f = tok not in SIGNS
        if prev is not None and (prev not in SIGNS or prev == ")") and (is_f or tok == "("):
            strings.append(r"\cdot")
            kinds.append("cdot")
            tok_of.append(None)
        strings.append(tok)
        kinds.append(("state" if _is_state(tok) else "input") if is_f else "sign")
        tok_of.append(ti)
        prev = tok
    tex = MathTex(*strings, font_size=size)
    cols = {"lhs": BLUE, "eq": FG, "state": GREEN, "input": BLUE, "cdot": FG, "sign": FG}
    pieces = [tex[k] for k in range(len(strings))]
    for p, k in zip(pieces, kinds):
        p.set_color(cols[k])
    factors = [None] * len(tokens)
    terms, cur, plus, depth = [], [], [], 0
    tag_list, term_tags, cur_tags = [], [], []
    for p, k, ti, s in zip(pieces, kinds, tok_of, strings):
        if k in ("lhs", "eq"):
            continue
        if ti is not None:
            factors[ti] = p
        if s == "(":
            depth += 1
        if s == ")":
            depth -= 1
        if s == "+" and depth == 0:
            terms.append(cur)
            term_tags.append(cur_tags)
            plus.append(p)
            cur, cur_tags = [], []
            continue
        cur.append(p)
        if k == "state" and tags and (tags == "all" or s.startswith("s_")):
            key = "s_" + re.search(r"s_(\d)", s).group(1)
            tg = T(STATE_TAG[key], TAG_SIZE, YELLOW).next_to(p, DOWN, buff=0.12)
            tag_list.append(tg)
            cur_tags.append(tg)
    terms.append(cur)
    term_tags.append(cur_tags)
    if tag_list:
        y = min(t.get_y() for t in tag_list)
        for t in tag_list:
            t.set_y(y)
    tg = VGroup(*tag_list)
    g = VGroup(tex, tg)
    g.tex, g.pieces, g.factors, g.terms, g.plus, g.tags, g.term_tags = tex, pieces, factors, terms, plus, tg, term_tags
    g.lhs = VGroup(pieces[0], pieces[1]) if lhs else None
    g.eqsign = pieces[1] if lhs else None
    return g


def put_line(line, left_x, y):
    ref = line.eqsign if line.eqsign is not None else line.tex
    line.shift(_p(left_x - line.pieces[0].get_left()[0], y - ref.get_y()))
    return line


def raw_line(lhs, size=EQ_SIZE):
    return eq_line(lhs, RAW[lhs], size=size)


STACK_PITCH = 1.55
STACK_YS = (1.75, 0.2, -1.35)


def d_stack(size=STACK_SIZE):
    lines = VGroup(*[put_line(raw_line(n, size), 0.0, y) for n, y in zip(("D_2", "D_1", "D_0"), STACK_YS)])
    names = VGroup()
    for n, ln in zip(("D_2", "D_1", "D_0"), lines):
        nm = T(LINE_NAME[n], 32, YELLOW)
        nm.next_to(ln.pieces[0], LEFT, buff=0.4).set_y(ln.eqsign.get_y())
        names.add(nm)
    g = VGroup(lines, names)
    g.shift(-g.get_center()[0] * RIGHT + (-(lines[0].tex.get_top()[1] + lines[2].tags.get_bottom()[1]) / 2) * UP)
    g.lines, g.names = lines, names
    return g


def handover_shot():
    return d_stack()


# ---------------------------------------------------------------- local
TABLE_K = 0.82
TABLE_UL = _p(-6.6, 2.4)
FULL = [r"\overline{s_2}", "s_1", r"\overline{s_0}", "e", "r"]
NOTE = ("“Remember when interpreting this table, because of the 1-hot",
        "shift structure, only 1 FF is 1 at a time, consequently it is",
        "straightforward to write down the next state equations”")
CAP_Y = -3.15
D1_MAP = S6.D1_MAP
D0_MAP = (("", "1", "1", ""), ("1", "1", "", ""), ("X", "X", "X", "X"), ("", "", "", ""))


def ghost_maps():
    m1 = S6.kmap4(D1_MAP, title="For FF 1:")
    g1 = VGroup(m1.grid, *[lp for lp, _ in S6.d1_parts(m1)])
    m0 = S6.kmap4(D0_MAP, title="For FF 0:")
    g0 = VGroup(m0.grid, S6.loop4(m0, S7.PINK_CELLS, PINK, 0.08), S6.loop4(m0, S7.PURPLE_CELLS, PURPLE, 0.08))
    out = VGroup()
    for g, x in ((g1, -5.0), (g0, -2.1)):
        out.add(S7.dimmed_copy(g, 2.5 / g.width, _p(x, 1.2), op=0.35))
    return out


class Inspect(NarratedScene):
    def construct(self):
        shot = S2.handover_shot()
        self.diag0, self.table, self.chips = shot[0], shot[1], shot[2]
        self.add(self.diag0, self.table, self.chips)
        self.l2, self.l1, self.l0 = (put_line(raw_line(n), EQ_LEFT, LINE_Y[n]) for n in ("D_2", "D_1", "D_0"))
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

    # ------------------------------------------------------------------ helpers
    def row_box(self, i):
        return S5.cell_box([self.table.rows[i]], YELLOW, buff=0.06)

    def col_items(self, j):
        t = self.table
        return [t.heads[2][j], *t.col(2, j)]

    def col_box(self, j):
        t = self.table
        return SurroundingRectangle(VGroup(*self.col_items(j)), buff=0.08).set_stroke(BLUE, 3)

    def ones(self, j):
        return [self.table.cell(i, 2, j) for i, r in enumerate(S2.ONEHOT_ROWS) if r[2][j] == "1"]

    def sources(self, i):
        t, r = self.table, S2.ONEHOT_ROWS[i]
        return [t.cell(i, 0, r[0].index("1")), t.rows[i][1]]

    def add_term(self, line, k, row, rt):
        """Row `row` lights (box slides there) and term k of `line` appears with its + and tag."""
        new = [line.plus[k - 1]] if k > 0 else []
        new += list(line.terms[k]) + list(line.term_tags[k])
        if k == 0:
            self.rowbox = self.row_box(row)
            box = [FadeIn(self.rowbox)]
        else:
            box = [Transform(self.rowbox, self.row_box(row))]
        self.play(*during(box, 0, 0.45), *during(appear(*new, lag=0, shift=0.15 * DOWN), 0.4, 1.0),
                  *during(flash(self.sources(row)), 0.3, 1.0), run_time=rt)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        t = self.table
        with self.say("c6.inspect.1") as c:
            t.generate_target()
            t.target.scale(TABLE_K)
            tg = t.target
            tg.shift(TABLE_UL - _p(tg.heads.get_left()[0] - 0.25, tg.heads.get_top()[1]))
            self.play(*during(disappear(self.chips, self.diag0, t.titles), 0, 0.4),
                      *during([MoveToTarget(t)], 0.3, 1.0), run_time=1.6)
            note = self.note = VGroup(*[T(s, 30) for s in NOTE]).arrange(DOWN, buff=0.18).move_to(_p(0, -2.5))
            self.play(*appear(*note, lag=0.3), run_time=1.2)   # early: the slide's note, quoted whole
            c.wait_until("only one flip-flop")
            hot = select(note[1], "only 1 FF is 1 at a time")[0]
            self.play(*recolor(hot, YELLOW), *flash([hot]), run_time=1.5)

            c.wait_until("row")
            self.rowbox = self.row_box(4)
            self.play(FadeIn(self.rowbox), run_time=1.0)

            c.wait_until("full")
            full = self.full = eq_line(None, FULL, tags=False)
            put_line(full, 0.6, LINE_Y["D_2"])
            self.play(*appear(full, shift=0.15 * DOWN), *during(flash(self.sources(4)), 0.2, 1.0), run_time=1.2)
            cap = self.cap = T("Part 5 style: the whole code", 30, DIM).next_to(full, DOWN, buff=1.05)
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)

            c.wait_until("drop")
            fp = full.pieces
            self.play(FlashAround(t.cell(4, 0, 1), color=GOLD, run_time=1.5, time_width=1.5),
                      *recolor([fp[0], fp[4]], DIM), run_time=1.5)

            c.wait_until("so naming")
            dropped = [fp[0], fp[1], fp[3], fp[4]]
            kept = [fp[2], fp[5], fp[6], fp[7], fp[8]]
            dest = self.l2.terms[0]
            self.play(*during([FadeOut(m, shift=0.35 * UP) for m in dropped], 0, 0.45),
                      *during([Transform(a, b.copy()) for a, b in zip(kept, dest)], 0.35, 1.0), run_time=1.6)
            self.remove(*full.get_family())
            self.add(*dest)
            cap2 = self.cap2 = T("One-hot: name the hot flip-flop", 30, GREEN).move_to(cap)
            self.play(*swap(cap, cap2), run_time=1.2)
            c.wait_until("ess one")
            self.play(*appear(*self.l2.term_tags[0]), run_time=1.0)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        t, l2 = self.table, self.l2
        with self.say("c6.inspect.2") as c:
            self.play(*disappear(*self.note, self.rowbox), run_time=1.0)
            self.colbox = self.col_box(0)
            self.play(GrowFromCenter(self.colbox), *set_alpha(self.col_items(1) + self.col_items(2), DIMMED),
                      *appear(*l2.lhs), run_time=1.5)
            c.wait_until("find its ones")
            ones = self.ones(0)
            self.play(*recolor(ones, YELLOW), *flash(ones), run_time=1.2)

            c.wait_until("t1")
            self.rowbox = self.row_box(4)
            self.play(*during(disappear(self.cap2), 0, 0.4), FadeIn(self.rowbox), FlashAround(VGroup(*l2.terms[0]), run_time=1.5, time_width=1.5),
                      *during(flash(self.sources(4)), 0, 0.8), run_time=1.5)

            c.wait_until("t2")
            self.add_term(l2, 1, 5, 1.6)
            c.wait_until("t3")
            self.add_term(l2, 2, 7, 1.4)

            c.wait_until("sum")
            self.play(*recolor(l2.plus, YELLOW), *flash(l2.plus), run_time=1.2)
            settle(self, l2)

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        t, l2, l1 = self.table, self.l2, self.l1
        with self.say("c6.inspect.3") as c:
            xcell = self.xcell = t.cell(5, 1, 1)
            self.play(Transform(self.rowbox, self.row_box(5)), *recolor(l2.plus, FG), run_time=1.0)
            self.play(FlashAround(xcell, run_time=1.2), xcell.animate.set_color(YELLOW), run_time=1.2)

            c.wait_until("the value of ar")
            ebar = l2.terms[1][-1]
            gap = 0.6
            dot = MathTex(r"\cdot", font_size=EQ_SIZE, color=FG).move_to(l2.terms[0][1]).set_x(ebar.get_right()[0] + 0.2)
            slot = DashedVMobject(Rectangle(width=0.42, height=0.55), num_dashes=16).set_stroke(DIM, 3)
            slot.next_to(dot, RIGHT, buff=0.12)
            movers = [l2.plus[1], *l2.terms[2], *l2.term_tags[2]]
            self.play(*[m.animate.shift(gap * RIGHT) for m in movers],
                      *during(appear(dot, slot, shift=None, lag=0), 0.7, 1.0), run_time=1.2)
            c.wait_until("simply drops out")
            self.play(*during(disappear(dot, slot), 0, 0.45),
                      *during([m.animate.shift(gap * LEFT) for m in movers], 0.35, 1.0), run_time=1.4)
            settle(self, l2)
            cap3 = self.cap3 = T("X under an input: that input drops out", 28, DIM).move_to(_p(2.7, CAP_Y))
            self.play(*appear(cap3), run_time=1.0)   # early: the rule just spoken, summed up

            c.wait_until("d1")
            self.play(*recolor(self.ones(0), FG), xcell.animate.set_color(FG), FadeOut(self.rowbox),
                      run_time=1.0)
            self.play(Transform(self.colbox, self.col_box(1)), *set_alpha(self.col_items(0), DIMMED),
                      *set_alpha(self.col_items(1), 1), *appear(*l1.lhs), run_time=1.5)
            c.wait_until("its ones are")
            ones = self.ones(1)
            self.play(*recolor(ones, YELLOW), *flash(ones), run_time=1.0)
            self.add_term(l1, 0, 1, 1.2)
            c.wait_until("sight with ee at zero")
            self.add_term(l1, 1, 2, 1.4)

            c.wait_until("d1eq")
            self.play(FlashAround(l1.tex, run_time=1.6, time_width=1.5), run_time=1.6)
            settle(self, l1)

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        t, l1, l0 = self.table, self.l1, self.l0
        with self.say("c6.inspect.4") as c:
            self.play(*disappear(self.cap3), *recolor(self.ones(1), FG), FadeOut(self.rowbox),
                      run_time=1.0)
            self.play(Transform(self.colbox, self.col_box(2)), *set_alpha(self.col_items(1), DIMMED),
                      *set_alpha(self.col_items(2), 1), *appear(*l0.lhs), run_time=1.5)
            c.wait_until("has three ones")
            ones = self.ones(2)
            self.play(*recolor(ones, YELLOW), *flash(ones), run_time=1.0)

            c.wait_until("u1")
            self.add_term(l0, 0, 0, 1.2)
            c.wait_until("u2")
            self.add_term(l0, 1, 3, 1.2)
            c.wait_until("u3")
            self.add_term(l0, 2, 6, 1.2)
            c.wait_until("d0eq")
            self.play(FlashAround(l0.tex, run_time=1.6, time_width=1.5), run_time=1.6)
            settle(self, l0)

            c.wait_until("nokmap")
            ghosts = self.ghosts = ghost_maps()
            # the column and row boxes leave with the table (first in the sweep's lag order)
            for bx in (self.colbox, self.rowbox):
                if bx in self.mobjects:
                    self.mobjects.remove(bx)
                self.mobjects.insert(0, bx)
            sweep_clear(self, FadeIn(ghosts), keep=[self.l2, self.l1, self.l0], run_time=1.6)
            c.wait_until("no need for k-maps")
            self.play(*disappear(ghosts), run_time=1.0)
            c.wait_until("because the other")
            stack = d_stack()
            self.play(*during([Transform(a, b) for a, b in zip((self.l2, self.l1, self.l0), stack.lines)], 0, 0.7),
                      *during(appear(*stack.names, lag=0.2), 0.6, 1.0), run_time=2.2)
        # handover: the stack stays on screen; s4 opens on handover_shot()
