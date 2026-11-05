"""Chapter 2, scene 5: three-valued logic from one idea. Clips c2.logic.1 – c2.logic.6.

Exports (reused by s4, s6 and the recap):
  null_cell(width=1.6, height=0.7, size=32)        PINK NULL cell: .box .label
  death_bar(width=12.0, height=0.6)                 VGroup(known, null); .frame .known .null
                                                    .before (959) .after (1,726) .parts_of_known
  rule_card(size=30)                                VGroup(box, lines); .box .lines[0..3]
  truth_grids(complete=False, ...)                  VGroup(AND, OR, NOT): AND|OR side by side, NOT a 1x3 strip under; grid.cell(a, b=None)
                                                    with a, b in "T" "F" "N"; cell .box .value
  truth_value(v, size=28), chip(v, size=40)
  where_gate(height=2.0, label=True)                .posts .bar .label
  gate_pass(gate, token, beyond=2.2, run_time=2.0)  -> list of anims (token passes, bar opens)
  gate_bounce(gate, token, color=RED, back=0.9, run_time=1.6) -> list (token bounces, fades)
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


# ---------------------------------------------------------------- shared looks

TOTAL, KNOWN, NULLS, BEFORE, AFTER = 23179, 2685, 20494, 959, 1726
VCOL = {"T": GREEN, "F": RED, "N": PINK}
VNAME = {"T": "TRUE", "F": "FALSE", "N": "NULL"}
AND_T = {("T", "T"): "T", ("T", "F"): "F", ("T", "N"): "N",
         ("F", "T"): "F", ("F", "F"): "F", ("F", "N"): "F",
         ("N", "T"): "N", ("N", "F"): "F", ("N", "N"): "N"}
OR_T = {("T", "T"): "T", ("T", "F"): "T", ("T", "N"): "T",
        ("F", "T"): "T", ("F", "F"): "F", ("F", "N"): "N",
        ("N", "T"): "T", ("N", "F"): "N", ("N", "N"): "N"}
NOT_T = {("T", None): "F", ("F", None): "T", ("N", None): "N"}


def _key(v):
    return None if v is None else str(v)[0].upper()


def null_cell(width=1.6, height=0.7, size=32):
    """The PINK NULL cell (s4's strip uses the same look)."""
    box = Rectangle(width=width, height=height).set_stroke(PINK, 3).set_fill(PINK, 0.12)
    label = Mono("NULL", size, PINK).move_to(box)
    g = VGroup(box, label)
    g.box, g.label = box, label
    return g


def death_bar(width=12.0, height=0.6, center=ORIGIN):
    """All 23,179 people in true proportions: GOLD known block (2,685) left, PINK NULL block
    (20,494) right. The VGroup holds (known, null); .frame is the full DIM outline, and
    .before / .after split the known block into 959 + 1,726 (not in the group: add them).
    Built at `center` (the extras are outside the group, so place it here, not by moving it)."""
    unit = width / TOTAL
    c = np.array(center, dtype=float)
    left = c[0] - width / 2
    frame = Rectangle(width=width, height=height).set_stroke(DIM, 2).set_fill(opacity=0).move_to(c)

    def block(n0, n, color, op, stroke=None):
        r = Rectangle(width=n * unit, height=height)
        r.set_fill(color, op).set_stroke(stroke or color, 2)
        r.move_to([left + (n0 + n / 2) * unit, c[1], 0])
        return r

    known = block(0, KNOWN, GOLD, 0.85)
    null = block(KNOWN, NULLS, PINK, 0.12)
    before = block(0, BEFORE, GOLD, 0.85, stroke=BG)
    after = block(BEFORE, AFTER, GOLD, 0.85, stroke=BG)
    g = VGroup(known, null)
    g.frame, g.known, g.null, g.before, g.after = frame, known, null, before, after
    g.parts_of_known = VGroup(before, after)
    return g


def _arrow(size=30, color=DIM):
    return MathTex(r"\rightarrow", font_size=size * 1.25, color=color)


def rule_card(size=30):
    """The one rule, as a card: 4 lines, left-aligned in a YELLOW-outlined box."""
    l1 = T("NULL = could be TRUE, could be FALSE", size,
           t2c={"NULL": PINK, "TRUE": GREEN, "FALSE": RED})
    l2 = T("try both", size)
    l3 = VGroup(T("same answer", size), _arrow(size), T("that answer", size)).arrange(RIGHT, buff=0.18)
    l4 = VGroup(T("different", size), _arrow(size), T("NULL", size, PINK)).arrange(RIGHT, buff=0.18)
    for l in (l3, l4):
        l[1].align_to(l[0], DOWN).shift(0.02 * UP)
    lines = VGroup(l1, l2, l3, l4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.15, width=lines.width + 0.7,
                           height=lines.height + 0.5).set_stroke(YELLOW, 2).set_fill(opacity=0)
    lines.move_to(box)
    g = VGroup(box, lines)
    g.box, g.lines = box, lines
    return g


def truth_value(v, size=28):
    v = _key(v)
    if v == "?":
        return T("?", size, PINK)
    return T(VNAME[v], size, VCOL[v])


def chip(v, size=40):
    """A row token / value chip: TRUE GREEN, FALSE RED, NULL PINK."""
    v = _key(v)
    label = T(VNAME[v], size, VCOL[v])
    box = RoundedRectangle(corner_radius=0.12, width=label.width + 0.45,
                           height=size * 0.0095 + 0.45).set_stroke(VCOL[v], 3).set_fill(VCOL[v], 0.15)
    label.move_to(box)
    g = VGroup(box, label)
    g.box, g.label = box, label
    return g


class TruthGrid(VGroup):
    """unary=True, strip=False: NOT as a column (rows = input). strip=True: NOT as a 1x3 strip,
    one row: the operator name, then each input (TRUE / FALSE / NULL) followed by its cell."""
    def __init__(self, op, table, unary=False, cell_w=1.2, head_w=1.3, row_h=0.75, size=28,
                 complete=False, strip=False, pair_gap=0.35):
        super().__init__()
        self.op, self.table, self.cells = op, table, {}
        keys = ["T", "F", "N"]
        cols = [None] if unary else keys
        xs = [head_w + cell_w * (j + 0.5) for j in range(len(cols))]
        corner = Mono(op, size, YELLOW)
        self.heads = VGroup()
        if unary and strip:
            corner.move_to([head_w / 2, 0, 0])
            self.corner = corner
            self.add(corner, self.heads)
            pitch = head_w + cell_w + pair_gap
            for i, a in enumerate(keys):
                hx = head_w + pair_gap + i * pitch + head_w / 2
                self.heads.add(T(VNAME[a], size, VCOL[a]).move_to([hx, 0, 0]))
                self._cell(a, None, hx + head_w / 2 + cell_w / 2, 0, cell_w, row_h, size, complete)
            return
        if unary:
            corner.move_to([xs[0], 0, 0])
        else:
            corner.move_to([head_w / 2, 0, 0])
        self.corner = corner
        self.add(corner)
        if not unary:
            for j, b in enumerate(cols):
                h = T(VNAME[b], size, VCOL[b]).move_to([xs[j], 0, 0])
                self.heads.add(h)
        for i, a in enumerate(keys):
            h = T(VNAME[a], size, VCOL[a]).move_to([head_w / 2, -(i + 1) * row_h, 0])
            self.heads.add(h)
        self.add(self.heads)
        for i, a in enumerate(keys):
            for j, b in enumerate(cols):
                self._cell(a, b, xs[j], -(i + 1) * row_h, cell_w, row_h, size, complete)

    def _cell(self, a, b, x, y, cell_w, row_h, size, complete):
        table = self.table
        unknown = (a == "N" or b == "N") and not complete
        box = Rectangle(width=cell_w - 0.08, height=row_h - 0.08)
        box.set_stroke(PINK if unknown else DIM, 2).set_fill(opacity=0)
        box.move_to([x, y, 0])
        val = truth_value("?" if unknown else table[(a, b)], size).move_to(box)
        cell = VGroup(box, val)
        val.size_hint = size
        cell.box, cell.value, cell.key = box, val, (a, b)
        self.cells[(a, b)] = cell
        self.add(cell)

    def cell(self, a, b=None):
        return self.cells[(_key(a), _key(b))]

    def unknown_cells(self):
        return [c for c in self.cells.values() if c.value.text == "?"]


def truth_grids(complete=False, cell_w=1.6, head_w=1.45, row_h=0.7, size=27, buff=0.45):
    """AND and OR as 3x3 grids (rows a, columns b) side by side, NOT as a 1x3 strip centred
    under them. complete=False: every cell with a NULL input holds a PINK '?'. Returns
    VGroup(AND, OR, NOT) with .AND .OR .NOT, centred on ORIGIN."""
    kw = dict(cell_w=cell_w, head_w=head_w, row_h=row_h, size=size, complete=complete)
    a = TruthGrid("AND", AND_T, **kw)
    o = TruthGrid("OR", OR_T, **kw)
    n = TruthGrid("NOT", NOT_T, unary=True, strip=True, **kw)
    ao = VGroup(a, o).arrange(RIGHT, buff=buff, aligned_edge=UP).move_to(ORIGIN)
    n.next_to(ao, DOWN, buff=0.25)
    n.set_x(0)
    g = VGroup(a, o, n)
    g.move_to(ORIGIN)
    g.AND, g.OR, g.NOT = a, o, n
    return g


def truth_grids_mini(pitch=0.4, buff=0.5):
    """Thumbnail of the complete tables (for small fly-ins): coloured squares, no text but the
    operator names (Mono 28, YELLOW) above. VGroup of three VGroup(name, squares)."""
    out = VGroup()
    for name, table, cols in (("AND", AND_T, "TFN"), ("OR", OR_T, "TFN"), ("NOT", NOT_T, [None])):
        sq = VGroup()
        for i, a in enumerate("TFN"):
            for j, b in enumerate(cols):
                v = table[(a, b)]
                sq.add(Square(pitch - 0.06).set_fill(VCOL[v], 0.8).set_stroke(width=0)
                       .move_to([j * pitch, -i * pitch, 0]))
        out.add(VGroup(Mono(name, 28, YELLOW).next_to(sq, UP, buff=0.15), sq))
    out.arrange(RIGHT, buff=buff, aligned_edge=DOWN)
    return out


def where_gate(height=2.0, label=True, color=FG):
    """A WHERE gate on a horizontal lane: two posts (top, bottom) and the bar between them."""
    pw, ph = 0.24, 0.32
    top = Rectangle(width=pw, height=ph).set_fill(DIM, 1).set_stroke(width=0).move_to([0, height / 2 - ph / 2, 0])
    bot = Rectangle(width=pw, height=ph).set_fill(DIM, 1).set_stroke(width=0).move_to([0, -height / 2 + ph / 2, 0])
    bar = Line(top.get_bottom(), bot.get_top()).set_stroke(color, 6)
    g = VGroup(top, bot, bar)
    g.posts, g.bar, g.label = VGroup(top, bot), bar, None
    if label:
        lbl = Mono("WHERE", 30, BLUE).next_to(top, UP, buff=0.15)
        g.add(lbl)
        g.label = lbl
    return g


def _ease(a):
    return smooth(float(np.clip(a, 0, 1)))


def _fade_to(mob, orig, k):
    for m, o in zip(mob.get_family(), orig.get_family()):
        m.set_fill(opacity=o.get_fill_opacity() * k)
        m.set_stroke(opacity=o.get_stroke_opacity() * k)


def gate_pass(gate, token, beyond=2.2, run_time=2.0):
    """Token (left of the gate, on its lane) passes: the bar opens GREEN as it goes through."""
    start = token.get_center().copy()
    gx = gate.bar.get_x()
    end = start.copy()
    end[0] = gx + beyond
    half = token.width / 2
    bar0 = gate.bar.copy()

    def x_at(a):
        return start[0] + (end[0] - start[0]) * _ease(a)

    def upd_tok(m, a):
        m.move_to([x_at(a), start[1], 0])

    def upd_bar(m, a):
        d = abs(x_at(a) - gx)
        open_ = float(np.clip(1 - (d - half) / 0.5, 0, 1))
        m.become(bar0)
        m.set_stroke(interpolate_color(ManimColor(bar0.get_stroke_color()), ManimColor(GREEN), open_),
                     opacity=1 - 0.85 * open_)

    return [UpdateFromAlphaFunc(token, upd_tok, run_time=run_time, rate_func=linear),
            UpdateFromAlphaFunc(gate.bar, upd_bar, run_time=run_time, rate_func=linear)]


def gate_bounce(gate, token, color=RED, back=0.9, run_time=1.6):
    """Token runs into the bar, which flashes `color`, then bounces back and fades out
    (remove the token afterwards)."""
    start = token.get_center().copy()
    gx = gate.bar.get_x()
    contact = gx - token.width / 2 - 0.08
    orig = token.copy()
    bar0 = gate.bar.copy()
    hit = 0.45

    def upd_tok(m, a):
        if a < hit:
            x, y, k = start[0] + (contact - start[0]) * _ease(a / hit), start[1], 1.0
        else:
            s = _ease((a - hit) / (1 - hit))
            x, y, k = contact - back * s, start[1] - 0.25 * s, 1 - s
        m.become(orig)
        m.move_to([x, y, 0])
        _fade_to(m, orig, k)

    def upd_bar(m, a):
        w = float(np.clip(1 - abs(a - hit) / 0.3, 0, 1))
        m.become(bar0)
        m.set_stroke(interpolate_color(ManimColor(bar0.get_stroke_color()), ManimColor(color), w))

    return [UpdateFromAlphaFunc(token, upd_tok, run_time=run_time, rate_func=linear),
            UpdateFromAlphaFunc(gate.bar, upd_bar, run_time=run_time, rate_func=linear)]


def ghost(a, op, b, res):
    """One branch of the rule: 'FALSE AND TRUE -> FALSE', outlined in the result's colour."""
    expr = T(f"{VNAME[a]} {op} {VNAME[b]}", 28,
             t2c={"TRUE": GREEN, "FALSE": RED})
    content = VGroup(expr, _arrow(28), T(VNAME[res], 30, VCOL[res])).arrange(RIGHT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.12, width=content.width + 0.45, height=0.7)
    box.set_stroke(VCOL[res], 2).set_fill(opacity=0)
    content.move_to(box)
    return VGroup(box, content)


# ---------------------------------------------------------------- the scene

class Logic(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- helpers
    def fill_anims(self, pairs, a0=0.0, a1=1.0, lag=0.0):
        """pairs: [(cell, v)]. Swap each '?' for its value, cells staggered by `lag` (fraction)."""
        anims, n = [], len(pairs)
        span = (a1 - a0) - lag * (n - 1)
        for i, (cell, v) in enumerate(pairs):
            new = truth_value(v, cell.value.size_hint).move_to(cell.box)
            s = a0 + i * lag
            anims += during(swap(cell.value, new) + [cell.box.animate.set_stroke(DIM, 2)], s, s + span)
            self._pending.append((cell, new))
        return anims

    def commit(self):
        for cell, new in self._pending:
            new.size_hint = cell.value.size_hint
            cell.remove(cell.value)
            cell.add(new)
            cell.value = new
        self._pending = []
        settle(self, self.grids)

    # -- c2.logic.1: NULL marks a missing value
    def clip1(self):
        with self.say("c2.logic.1") as c:
            nc = null_cell(width=2.8, height=1.2, size=60)
            self.nc = nc
            c.wait_until("about null")
            self.play(FadeIn(nc, scale=0.9), run_time=1.0)
            c.wait_until("it marks")
            self.play(nc.animate.move_to([-3.6, 0, 0]), run_time=min(1.2, c.until("maybe")))
            l1 = T("value unknown", 36, DIM)
            l2 = VGroup(T("not applicable", 36, DIM),
                        T("(death year of someone alive)", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            l1.move_to([0, 1.0, 0], aligned_edge=LEFT).set_x(-0.9 + l1.width / 2)
            l2.move_to([0, -1.0, 0]).set_x(-0.9 + l2.width / 2)
            ln1 = Line(nc.get_right() + 0.15 * RIGHT, l1.get_left() + 0.15 * LEFT).set_stroke(DIM, 2)
            ln2 = Line(nc.get_right() + 0.15 * RIGHT, l2[0].get_left() + 0.15 * LEFT).set_stroke(DIM, 2)
            c.wait_until("maybe it's unknown")
            self.play(GrowFromPoint(ln1, ln1.get_start()), *appear(l1), run_time=1.0)
            c.wait_until("nothing to record")
            self.play(GrowFromPoint(ln2, ln2.get_start()), *appear(l2), run_time=1.0)
            c.wait_until("treat")
            merged = T("unknown", 48, PINK)
            merged.move_to([-0.9 + merged.width / 2, 0, 0])
            ln3 = Line(nc.get_right() + 0.15 * RIGHT, merged.get_left() + 0.2 * LEFT).set_stroke(PINK, 3)
            self.play(*set_alpha([l1, l2, ln1, ln2], 0.35),
                      *during(appear(merged, ln3, shift=None), 0.3, 1), run_time=1.5)
            self.old1 = [l1, l2, ln1, ln2, merged, ln3]

    # -- c2.logic.2: 1921 <> NULL is NULL
    def clip2(self):
        with self.say("c2.logic.2") as c:
            nc = self.nc
            f = 2.2 / nc.box.width
            num = Mono("1921", 56, GOLD)
            op = Mono("<>", 56)
            ph = nc.copy().scale(f)
            arr = MathTex(r"\rightarrow", font_size=72)
            slot = Rectangle(width=2.2, height=0.95).set_opacity(0)
            row1 = VGroup(num, op, ph, arr, slot).arrange(RIGHT, buff=0.4).move_to([0, 2.1, 0])
            c.wait_until("nineteen")
            self.play(*during(disappear(*self.old1), 0, 0.4),
                      nc.animate.scale(f).move_to(ph),
                      *during(appear(num, op, lag=0.2), 0.5, 1), run_time=1.6)

            # can't tell: the NULL could be any year
            c.wait_until("cant")
            q = Mono("?", 48, PINK).move_to(nc.box)
            self.play(*swap(nc.label, q), run_time=1.0)
            c.wait_until("might be nineteen")
            y = Mono("1921", 40, GOLD).move_to(nc.box)
            res = T("FALSE", 48, RED).move_to(slot)
            self.play(*swap(q, y), *appear(arr, res, shift=None, lag=0.2), run_time=1.0)  # early: a comparison result, not a label
            c.wait_until("or anything else")
            for yr in ("1958", "1977", "2003"):
                ny = Mono(yr, 40, GOLD).move_to(nc.box)
                anims = swap(y, ny)
                if yr == "1958":
                    nres = T("TRUE", 48, GREEN).move_to(slot)
                    anims += swap(res, nres)
                    res = nres
                self.play(*anims, run_time=0.6)  # early: a comparison result, not a label
                y = ny
            c.wait_until("result")
            q2 = Mono("?", 48, PINK).move_to(nc.box)
            out = null_cell(width=2.2, height=0.95, size=47).move_to(slot)
            self.play(*swap(y, q2), *swap(res, out), run_time=1.2)
            c.wait_until("it's null")
            back = Mono("NULL", 47, PINK).move_to(nc.box)
            self.play(*swap(q2, back), run_time=1.0)

            # NULL = NULL is NULL
            c.wait_until("isnull")
            a = null_cell(width=2.2, height=0.95, size=47)
            eq = Mono("=", 56)
            b = null_cell(width=2.2, height=0.95, size=47)
            lhs = VGroup(a, eq, b).arrange(RIGHT, buff=0.4)
            lhs.next_to([arr.get_left()[0], 0.65, 0], LEFT, buff=0.4)
            arr2 = MathTex(r"\rightarrow", font_size=72).move_to([arr.get_x(), 0.65, 0])
            out2 = null_cell(width=2.2, height=0.95, size=47).move_to([slot.get_x(), 0.65, 0])
            self.play(*appear(a, eq, b, lag=0.2), run_time=1.0)
            c.wait_until("is null")
            self.play(*appear(arr2, out2, shift=None, lag=0.2), run_time=0.9)

            # the left join's own test
            c.wait_until("that's why")
            code1 = Code("WHERE deathyear = NULL", size=36)
            code2 = Code("WHERE deathyear IS NULL", size=36)
            x0 = num.get_left()[0]
            code1.move_to([0, -1.05, 0]).set_x(x0 + code1.width / 2)
            code2.move_to([0, -2.25, 0]).set_x(x0 + code2.width / 2)
            cnt1 = T("0 rows", 36, RED).move_to([0, -1.05, 0])
            cnt2 = T("20,494 rows", 36, GOLD).move_to([0, -2.25, 0])
            cx = code2.get_right()[0] + 0.7
            cnt1.set_x(cx + cnt1.width / 2)
            cnt2.set_x(cx + cnt2.width / 2)
            self.play(*appear(code1, cnt1, code2, lag=0.35), run_time=1.2)
            c.wait_until("is null", nth=1)
            box = SurroundingRectangle(code2.find("IS NULL"), color=YELLOW, buff=0.08)
            self.play(FadeIn(box), *appear(cnt2), run_time=min(1.0, c.until(floor=0.5)))

    # -- c2.logic.3: three values, one rule
    def clip3(self):
        with self.say("c2.logic.3") as c:
            c.wait_until("possible")
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
            chips = VGroup(*[chip(v, 52) for v in "TFN"]).arrange(RIGHT, buff=0.6).move_to(ORIGIN)
            for ch, cue in zip(chips, ("true", "false", "and null")):
                c.wait_until(cue)
                self.play(*appear(ch), run_time=0.7)

            c.wait_until("how")
            card = rule_card(30).to_edge(UP, buff=0.3)
            self.card = card
            grids = truth_grids()
            grids.move_to([0, card.get_bottom()[1] - 0.22 - grids.height / 2, 0])
            self.grids = grids
            # the chips fly up and become the AND grid's column labels
            heads = grids.AND.heads
            anims = []
            for j, ch in enumerate(chips):
                ch.label.generate_target()
                ch.label.target.scale(heads[j].height / ch.label.height).move_to(heads[j])
                anims.append(MoveToTarget(ch.label))
            rest = [grids.AND.corner, *heads[3:], *grids.AND.cells.values()]
            # the boxes are gone before the labels leave them (no label crossing an outline)
            self.play(*during([FadeOut(ch.box) for ch in chips], 0, 0.2),
                      *during(anims, 0.2, 0.55),
                      *during(appear(*rest, shift=None, lag=0.02), 0.45, 0.8),
                      *during(appear(grids.OR, grids.NOT, lag=0.4), 0.55, 1), run_time=2.4)
            for j, ch in enumerate(chips):
                self.remove(*ch.get_family())
                ch.label.become(heads[j])
                heads.submobjects[j] = ch.label
            self.remove(*[m for m in rest])
            settle(self, grids)

            c.wait_until("rule")
            qs = [cl.box for g in grids for cl in g.unknown_cells()]
            self.play(*flash(qs, color=PINK), run_time=1.5)

            card = self.card
            c.wait_until("one rule")
            self.play(GrowFromCenter(card.box), run_time=1.0)
            for line, cue in zip(card.lines, ("treat null as", "try both", "if the two answers agree",
                                             "if they disagree")):
                c.wait_until(cue)
                self.play(*appear(line), run_time=1.0)  # early: the rule card line is shown as its sentence starts
            settle(self, card)

    # -- c2.logic.4: the rule fills the NULL cells
    def clip4(self):
        g = self.grids
        self._pending = []
        gy = g.NOT.get_bottom()[1] - 0.25 - 0.35
        with self.say("c2.logic.4") as c:
            cell = g.AND.cell("F", "N")
            box = SurroundingRectangle(cell.box, color=YELLOW, buff=0.05).set_stroke(width=4)
            self.play(FadeIn(box), *set_alpha([g.OR, g.NOT], DIMMED), run_time=1.2)

            def two_ghosts(a, b_vals, cues):
                gs = [ghost(a, "AND", b, AND_T[(a, b)]) for b in b_vals]
                VGroup(*gs).arrange(RIGHT, buff=0.5).move_to([-0.3, gy, 0])
                for gh, cue in zip(gs, cues):
                    c.wait_until(cue)
                    self.play(*appear(gh), run_time=1.0)
                return gs

            gs = two_ghosts("F", "TF", ("if the null were true", "if it were false"))
            c.wait_until("agree")
            self.play(*during(disappear(*gs), 0, 0.45),
                      *self.fill_anims([(cell, "F")], 0.45, 1), run_time=1.5)
            self.commit()

            c.wait_until("ta")
            cell = g.AND.cell("T", "N")
            self.play(Transform(box, SurroundingRectangle(cell.box, color=YELLOW, buff=0.05).set_stroke(width=4)),
                      run_time=1.0)
            gs = two_ghosts("T", "TF", ("one way", "the other way"))
            c.wait_until("disagree")
            self.play(*during(disappear(*gs), 0, 0.45),
                      *self.fill_anims([(cell, "N")], 0.45, 1), run_time=1.5)
            self.commit()

            c.wait_until("or")
            cell = g.OR.cell("T", "N")
            self.play(*set_alpha([g.OR], 1),
                      Transform(box, SurroundingRectangle(cell.box, color=YELLOW, buff=0.05).set_stroke(width=4)),
                      run_time=1.2)
            c.wait_until("true or null")
            self.play(*self.fill_anims([(cell, "T")]), run_time=1.0)
            self.commit()
            c.wait_until("but false or null")
            cell = g.OR.cell("F", "N")
            self.play(Transform(box, SurroundingRectangle(cell.box, color=YELLOW, buff=0.05).set_stroke(width=4)),
                      run_time=0.8)
            self.play(*self.fill_anims([(cell, "N")]), run_time=1.0)
            self.commit()

            c.wait_until("not")
            cell = g.NOT.cell("N")
            self.play(*set_alpha([g.NOT], 1),
                      Transform(box, SurroundingRectangle(cell.box, color=YELLOW, buff=0.05).set_stroke(width=4)),
                      run_time=1.2)
            c.wait_until("so it's null")
            self.play(*self.fill_anims([(cell, "N")]), run_time=1.0)
            self.commit()
            self.box = box

    # -- c2.logic.5: full tables, then WHERE keeps only TRUE
    def clip5(self):
        g = self.grids
        with self.say("c2.logic.5") as c:
            rest = [(cl, gr.table[cl.key]) for gr in (g.AND, g.OR) for cl in gr.unknown_cells()]
            self.play(FadeOut(self.box, run_time=0.5), *self.fill_anims(rest, 0.1, 1, lag=0.12), run_time=2.4)
            self.commit()

            c.wait_until("where")
            gate = where_gate(2.0).move_to([3.6, -0.75, 0])
            lane_y = gate.bar.get_y()
            mini = truth_grids_mini()
            mini.move_to([0, lane_y, 0]).to_edge(LEFT, buff=0.6)
            self.play(*during(disappear(g), 0, 0.45), *during(appear(mini, shift=None), 0.5, 1), run_time=1.6)
            self.play(*appear(gate, shift=None), run_time=1.0)

            toks = [chip(v, 32) for v in "TFN"]
            for i, t in enumerate(toks):
                t.move_to([gate.bar.get_x() - 1.4 - 1.9 * i, lane_y, 0])
            c.wait_until("a where clause")
            self.play(*appear(*toks, shift=0.25 * RIGHT, lag=0.2), run_time=1.0)
            c.wait_until("is true")
            self.play(*gate_pass(gate, toks[0], beyond=2.2, run_time=min(1.8, c.until("drop"))))
            c.wait_until("drop")
            self.play(*gate_bounce(gate, toks[1], RED, run_time=1.5))
            self.remove(toks[1])
            self.play(*gate_bounce(gate, toks[2], PINK, run_time=min(1.5, c.until(floor=0.8))))
            self.remove(toks[2])

    # -- c2.logic.6: a question and its opposite miss the NULLs
    def clip6(self):
        card = self.card
        with self.say("c2.logic.6") as c:
            q1 = Code("SELECT COUNT(*) FROM people\nWHERE deathyear < 2000;", size=28)
            q2 = Code("SELECT COUNT(*) FROM people\nWHERE NOT (deathyear < 2000);", size=28)
            q1.to_edge(LEFT, buff=0.6).set_y(0.75)
            q2.to_edge(LEFT, buff=0.6).set_y(-0.45)
            bar = death_bar(12.0, center=[0, -1.8, 0])
            total = T("23,179 people", 30, DIM).next_to(bar.frame, UP, buff=0.15).align_to(bar.frame, RIGHT)
            sweep_clear(self, *appear(q1), FadeIn(bar.frame), *appear(total, shift=None),
                        keep=[card], run_time=1.8)
            gx = 2.3
            cx = 3.2
            c.wait_until("you get nine")
            cnt1 = T("959", 40, GOLD).move_to([cx, q1.get_y(), 0], aligned_edge=LEFT)
            self.play(GrowFromEdge(bar.before, LEFT), *appear(cnt1), run_time=1.4)
            c.wait_until("opposite")
            self.play(*appear(q2), run_time=1.0)
            c.wait_until("you get one thousand")
            cnt2 = T("1,726", 40, GOLD).move_to([cx, q2.get_y(), 0], aligned_edge=LEFT)
            self.play(GrowFromEdge(bar.after, LEFT), *appear(cnt2), run_time=1.4)

            c.wait_until("sum")
            brace = span_brace(bar.before.get_corner(DL), bar.after.get_corner(DR), DOWN, color=GOLD)
            lbl = T("2,685", 36, GOLD).next_to(brace, DOWN, buff=0.12)
            self.play(GrowFromCenter(brace), *appear(lbl), run_time=1.4)

            c.wait_until("fall")
            nl = T("20,494 NULL", 34, PINK).next_to(bar.null, DOWN, buff=0.3)
            g1 = where_gate(1.0, label=False).move_to([gx, q1.get_y(), 0])
            g2 = where_gate(1.0, label=False).move_to([gx, q2.get_y(), 0])
            self.play(FadeIn(bar.null), *appear(nl), *appear(g1, g2, shift=None, lag=0.2), run_time=1.4)
            t1 = chip("N", 28).move_to([gx - 1.2, q1.get_y(), 0])
            t2 = chip("N", 28).move_to([gx - 1.2, q2.get_y(), 0])
            self.play(*appear(t1, t2, shift=0.2 * RIGHT), run_time=0.7)
            self.play(*gate_bounce(g1, t1, PINK, back=0.5, run_time=1.6),
                      *gate_bounce(g2, t2, PINK, back=0.5, run_time=1.6))
            self.remove(t1, t2)
            c.wait_until()
