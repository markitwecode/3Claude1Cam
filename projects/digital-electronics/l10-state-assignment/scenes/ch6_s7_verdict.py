"""Chapter 6, scene 7: one-hot or sequential? Gates counted side by side, the slide's verdict, the scoreboard's
final row and the lecture's thread. Clips c6.verdict.1 – c6.verdict.3.

Shared helpers (load_scene("ch6_s7_verdict")), for s8:
- `panels()`: the two panels as clip 1 leaves them (full frame, a DIM divider at x 0). VGroup(left, right, divider,
  caption); .left / .right each VGroup(title, ffs, *eqs, s, tag, icons, total, invs) with attrs .title .ffs .eqs
  .s .tag (GREEN "no output logic") .icons (VGroup of per-line icon groups; .flat = every icon in order) .total
  (GOLD "7 gates" / "8 gates") .invs (inverter icons with their input letters). Left: ch5's ff_pair (s1 s0),
  D1 / D0 in ch5's term colours, s = s_1. Right: ch6 s2's onehot_ffs (Sync Sight Hunt tags), ch6 s3 eq_line
  D2 / D1 / D0 (factored), s = s_2. .caption: the DIM "gates counted ..." line at y -3.32.
- `final_board()`: ch5 s7's sync_board(with_row=True) plus the row "one-hot | 3 | 8 | none" in slot 8
  (y -2.5); .onehot_row. Native ch2 scale at ch5's place, x -6.5..-0.05, y 3.69..-2.7.
- `thread()`: p. 132's "Depends what we are trying to optimise" (T 40 italic, two lines) with DIM branch arrows
  to "Complexity" and "Speed" (T 40 BLUE), in the right column (x 0.9..6.2, y 2.0..-1.1). .dep .opt .items .arrows
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

S2 = load_scene("ch6_s2_codes")
S3 = load_scene("ch6_s3_inspect")
S4 = load_scene("ch5_s4_twoffs")
S6 = load_scene("ch5_s6_d1")
S7 = load_scene("ch5_s7_d0")
S27 = load_scene("ch2_s7_tradeoff")


def _p(x, y):
    return np.array([x, y, 0.0])


PANEL_X = (-3.55, 3.55)
LEFT_X = (-6.4, 0.7)          # left edge of each panel's equations
TITLE_Y = 3.3
FF_TOP = 2.8
EQ_SIZE = 40
EQ_YS = (0.45, -0.3, -1.05)
S_Y = -1.7
ICON_Y = -2.22
TOTAL_Y = -2.84
ICON_K = 0.32


# ---------------------------------------------------------------- gate icons
def gate_icon(kind):
    """kind: 'and2', 'and3', 'or2', 'or3', 'not'. L6's gate bodies with short input/output stubs, small."""
    g = {"and2": lambda: S7.and_n(2), "and3": lambda: S7.and_n(3), "or2": lambda: S7.or_n(2),
         "or3": lambda: S7.or_n(3), "not": S7.inverter}[kind]()
    n = {"and2": 2, "and3": 3, "or2": 2, "or3": 3, "not": 1}[kind]
    stubs = [Line(g.inp(i) + 0.35 * LEFT, g.inp(i)).set_stroke(BLUE, 4) for i in range(n)]
    stubs.append(Line(g.out(), g.out() + 0.3 * RIGHT).set_stroke(BLUE, 4))
    icon = VGroup(*stubs, g).scale(ICON_K)
    for m in icon.family_members_with_points():
        if m.get_stroke_width() > 0:
            m.set_stroke(width=3)
    return icon


def icon_row(spec, cx):
    groups = VGroup(*[VGroup(*[gate_icon(k) for k in line]).arrange(RIGHT, buff=0.1) for line in spec])
    groups.arrange(RIGHT, buff=0.42).move_to(_p(cx, ICON_Y))
    groups.flat = [i for g in groups for i in g]
    return groups


def inv_icon(var):
    lab = MathTex(var, font_size=36, color=BLUE)
    ic = gate_icon("not")
    return VGroup(lab, ic).arrange(RIGHT, buff=0.1)


def _readable_pins(f, k=1.32):
    """The shrunk boxes' D / Q / Q-bar labels back up to size 28."""
    for lab in (f.d_l, f.q_l, f.qb_l):
        lab.scale(k)


# ---------------------------------------------------------------- equations
def term_line(lhs, terms, colors, size=EQ_SIZE):
    """ch5's term_eq look (separate pieces, terms in their loop colours), laid out with arrange."""
    lh = MathTex(lhs, "=", font_size=size, color=FG)
    lh[0].set_color(BLUE)
    parts = [lh]
    ts = []
    for k, (t, col) in enumerate(zip(terms, colors)):
        if k:
            parts.append(MathTex("+", font_size=size, color=FG))
        m = MathTex(t, font_size=size, color=col)
        ts.append(m)
        parts.append(m)
    g = VGroup(*parts).arrange(RIGHT, buff=0.2)
    g.lhs, g.terms = lh, ts
    return g


def s_line(var):
    return MathTex("s", "=", var, font_size=40, color=GREEN)


def no_logic_tag(s):
    return T("no output logic", 30, GREEN).next_to(s, RIGHT, buff=0.5)


ONEHOT_EQS = (("D_2", [r"\overline{s_0}", "e", "r", "+", "s_2", r"\overline{e}"]),
              ("D_1", ["s_0", "r", "+", "s_1", r"\overline{e}"]),
              ("D_0", [r"\overline{r}", "(", "s_0", "+", "e", ")"]))
SEQ_ICONS = (("and2", "and2", "and3", "or3"), ("and2", "and3", "or2"))
HOT_ICONS = (("and3", "and2", "or2"), ("and2", "and2", "or2"), ("or2", "and2"))


def _left_panel():
    cx = PANEL_X[0]
    title = T("Sequential (Part 5)", 36, FG).move_to(_p(cx, TITLE_Y))
    pair = S4.ff_pair()
    pair.remove(pair.tag)
    for f, o in zip(pair.ffs, pair.outs):
        f.scale(0.75, about_point=ORIGIN)
        o.next_to(f.q_w, RIGHT, buff=0.12)
        _readable_pins(f)
    ffs = VGroup(*pair.ffs, *pair.outs)
    ffs.shift(_p(cx - ffs.get_center()[0], FF_TOP - pair.ffs[0].box.get_top()[1]))
    d1 = term_line("D_1", S6.D1_TERMS, S6.D1_COLORS)
    d0 = term_line("D_0", S7.D0_TERMS, S7.D0_COLORS)
    for ln, y in zip((d1, d0), EQ_YS):
        ln.move_to(_p(0, y)).align_to(_p(LEFT_X[0], 0), LEFT)
    s = s_line("s_1").move_to(_p(0, S_Y)).align_to(_p(LEFT_X[0], 0), LEFT)
    tag = no_logic_tag(s)
    icons = icon_row(SEQ_ICONS, cx)
    total = T("7 gates", 40, GOLD).move_to(_p(cx - 1.5, TOTAL_Y))
    invs = VGroup(inv_icon("e")).move_to(_p(cx + 1.6, TOTAL_Y))
    g = VGroup(title, ffs, d1, d0, s, tag, icons, total, invs)
    g.title, g.ffs, g.eqs, g.s, g.tag, g.icons, g.total, g.invs = title, ffs, [d1, d0], s, tag, icons, total, invs
    g.pair = pair
    return g


def _right_panel():
    cx = PANEL_X[1]
    title = T("One-hot (Part 6)", 36, FG).move_to(_p(cx, TITLE_Y))
    ffs = S2.onehot_ffs(xs=(-2.15, 0.0, 2.15), y=0.0, scale=0.45)
    for f in ffs.ffs:
        _readable_pins(f)
    ffs.shift(_p(cx - ffs.get_center()[0], FF_TOP - ffs.ffs[0].box.get_top()[1]))
    eqs = [S3.put_line(S3.eq_line(lhs, toks, size=EQ_SIZE, tags=False), LEFT_X[1], y)
           for (lhs, toks), y in zip(ONEHOT_EQS, EQ_YS)]
    s = s_line("s_2").move_to(_p(0, S_Y)).align_to(_p(LEFT_X[1], 0), LEFT)
    tag = no_logic_tag(s)
    icons = icon_row(HOT_ICONS, cx)
    total = T("8 gates", 40, GOLD).move_to(_p(cx - 1.5, TOTAL_Y))
    invs = VGroup(inv_icon("e"), inv_icon("r")).arrange(RIGHT, buff=0.4).move_to(_p(cx + 1.6, TOTAL_Y))
    g = VGroup(title, ffs, *eqs, s, tag, icons, total, invs)
    g.title, g.ffs, g.eqs, g.s, g.tag, g.icons, g.total, g.invs = title, ffs, eqs, s, tag, icons, total, invs
    return g


def caption():
    a = T("gates counted: AND, OR; not inverters (flip-flop", 28, DIM)
    q = MathTex(r"\overline{Q}", font_size=34, color=DIM)
    b = T("outputs are free)", 28, DIM)
    g = VGroup(a, q, b).arrange(RIGHT, buff=0.13)
    q.align_to(a, DOWN)
    return g.move_to(_p(0, -3.32))


def panels():
    left, right = _left_panel(), _right_panel()
    div = Line(_p(0, 3.1), _p(0, -2.5)).set_stroke(DIM, 2)
    cap = caption()
    g = VGroup(left, right, div, cap)
    g.left, g.right, g.divider, g.caption = left, right, div, cap
    return g


# ---------------------------------------------------------------- clip 2 pieces
QUOTE = ("“So in this example, the 1 hot\nis easier to design, but it\nresults in slightly more hardware\n"
         "compared with the sequential\nstate assignment design”")


def raw_ghost():
    head = T("one-hot, straight from the diagram", 28, DIM)
    lines = VGroup(*[S3.eq_line(n, S3.RAW[n], size=32, tags=False) for n in ("D_2", "D_1", "D_0")])
    lines.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    if lines.width > 6.2:
        lines.scale_to_fit_width(6.2)
    for ln in lines:
        ln.set_opacity(0.55)
    g = VGroup(head, lines).arrange(DOWN, buff=0.35).move_to(_p(PANEL_X[0], -0.15))
    g.head, g.lines = head, lines
    return g


# ---------------------------------------------------------------- clip 3: the scoreboard and the thread
ONEHOT_ROW = ("one-hot", "3", "8", "none")


def final_board():
    sb = S7.sync_board(with_row=True)
    row = VGroup(*[S7.sb_cell(sb, 8, k, s) for k, s in enumerate(ONEHOT_ROW)])
    sb.add(row)
    sb.rows.append(row)
    sb.onehot_row = row
    return sb


def thread():
    dep = T("Depends what we are trying\nto optimise", 36, slant=ITALIC, line_spacing=0.9).move_to(_p(3.45, 1.5))
    opt = select(dep, "optimise")[0]
    cx = T("Complexity", 40, BLUE).move_to(_p(2.1, -0.75))
    sp = T("Speed", 40, BLUE).move_to(_p(5.2, -0.75))
    arrows = [Arrow(opt.get_bottom() + 0.12 * DOWN, d.get_top() + 0.12 * UP, buff=0, stroke_width=3, color=DIM,
                    max_tip_length_to_length_ratio=0.12) for d in (cx, sp)]
    g = VGroup(dep, *arrows, cx, sp)
    g.dep, g.opt, g.items, g.arrows = dep, opt, [cx, sp], arrows
    return g


def col_box(col, left, right):
    """One GOLD highlight band behind a scoreboard column, from x left to right (the gaps between columns);
    fill only, so no edge ever cuts a glyph, settled or while it slides to the next column."""
    top, bot = col.get_top()[1] + 0.14, col.get_bottom()[1] - 0.14
    return (Rectangle(width=right - left, height=top - bot).move_to(_p((left + right) / 2, (top + bot) / 2))
            .set_stroke(width=0).set_fill(GOLD, 0.2).set_z_index(-1))


def col_edges(sb, k):
    """x span for column k: halfway into the gaps to its neighbours (0.15 past the text at the board's ends)."""
    def span(j):
        ms = [sb.head[j], *[r[j] for r in sb.rows]]
        return min(m.get_left()[0] for m in ms), max(m.get_right()[0] for m in ms)
    lo, hi = span(k)
    left = (span(k - 1)[1] + lo) / 2 if k > 0 else lo - 0.15
    right = (hi + span(k + 1)[0]) / 2 if k + 1 < len(sb.head) else hi + 0.15
    return left, right


# ---------------------------------------------------------------- the scene
class Verdict(NarratedScene):
    def construct(self):
        P = panels()
        L, R = P.left, P.right
        self.P = P

        # ---- clip 1: count them side by side
        with self.say("c6.verdict.1") as c:
            self.play(*appear(L.title, R.title, shift=None, lag=0.2), GrowFromCenter(P.divider),  # early: panel titles
                      *appear(L.ffs, R.ffs, lag=0.3), run_time=min(1.6, c.until("side by side")))
            c.wait_until("side by side")
            self.play(*appear(*L.eqs, L.s, *R.eqs, R.s, lag=0.15), run_time=1.8)
            c.wait_until(own_word=P.caption[0])
            self.play(*appear(P.caption, shift=None), run_time=1.0)
            c.wait_until("seq")
            self.play(*[FlashAround(f.box, color=YELLOW, run_time=1.5, time_width=1.5) for f in L.pair.ffs],
                      *appear(*L.icons.flat, lag=0.3), run_time=min(2.2, c.until("seven gates")))
            c.wait_until("seven gates")
            self.play(*appear(L.total), run_time=1.0)
            c.wait_until("hot")
            self.play(*[FlashAround(f.box, color=YELLOW, run_time=1.5, time_width=1.5) for f in R.ffs.ffs],
                      *appear(*R.icons.flat, lag=0.3), run_time=min(2.4, c.until("eight gates")))
            c.wait_until("eight gates")
            self.play(*appear(R.total), run_time=1.0)
            c.wait_until("dee zero factored")
            self.play(FlashUnder(R.eqs[2].tex, color=YELLOW, run_time=1.5, time_width=1.5),
                      FlashAround(R.icons[2], color=YELLOW, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("needs one")
            self.play(*appear(L.invs), run_time=1.0)
            c.wait_until("needs two")
            self.play(*appear(*R.invs, lag=0.3), run_time=1.0)
            c.wait_until("none")
            self.play(*appear(L.tag, R.tag, lag=0.2), run_time=1.0)

        # ---- clip 2: the verdict, the extra, the raw route
        with self.say("c6.verdict.2", gap=1.6) as c:
            card = S27.quote_card(QUOTE, 28).move_to(_p(PANEL_X[0], -0.35))
            gone = [*L.eqs, L.s, L.tag, *L.icons.flat, L.invs, L.total, P.caption]
            self.play(*during(disappear(*gone), 0, 0.45), *during(appear(card, shift=None), 0.5, 1),
                      run_time=1.6)
            c.wait_until("extra")
            third = R.ffs.ffs[2]
            self.play(restyle(third.box, outline=GOLD, width=7),
                      FlashAround(third.box, color=GOLD, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("plus one gate")
            orx = R.icons[2][0]
            self.play(orx.animate.set_stroke(GOLD),
                      FlashAround(orx, color=GOLD, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("raw")
            ghost = raw_ghost().move_to(_p(PANEL_X[0], 1.0))   # the whole left panel is the one-hot raw route now
            self.play(*swap(card, ghost), *during(disappear(L.title, L.ffs), 0, 0.45), run_time=1.4)
            c.wait_until("eleven gates")
            tot = T("8 AND + 3 OR = 11 gates", 36, GOLD).move_to(_p(PANEL_X[0], -2.15))
            self.play(*appear(tot), run_time=1.0)
            c.wait_until("saved")
            arr = Arrow(tot.get_right() + 0.1 * RIGHT, R.total.get_left() + 0.1 * LEFT, buff=0, color=GOLD,
                        stroke_width=5, tip_length=0.22, max_tip_length_to_length_ratio=0.2)
            minus = T("−3", 40, GOLD).next_to(arr.get_center(), DOWN + LEFT, buff=0.25)
            self.play(GrowArrow(arr), *during(appear(minus), 0.4, 1), run_time=1.5)

        # ---- clip 3: the scoreboard's final row and the thread
        with self.say("c6.verdict.3") as c:
            sb = final_board()
            row = sb.onehot_row
            sb.remove(row)
            sweep_clear(self, FadeIn(sb), run_time=min(1.8, c.until("final row")))  # early: the scoreboard returns whole
            c.wait_until("final row")
            self.play(*appear(*row, lag=0.35), run_time=1.4)
            th = thread()
            c.wait_until("thread")
            self.play(*appear(th.dep, *th.items, lag=0.3), *[GrowArrow(a) for a in th.arrows],  # early: ch1's thread, shown whole
                      run_time=1.6)
            c.wait_until("no single best")
            self.play(*recolor(th.opt, YELLOW), FlashUnder(th.opt, color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            col1 = VGroup(sb.head[1], *[r[1] for r in sb.rows])
            col2 = VGroup(sb.head[2], *[r[2] for r in sb.rows])
            c.wait_until("flip-flops")
            box = col_box(col1, *col_edges(sb, 1))
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("logic")
            self.play(Transform(box, col_box(col2, *col_edges(sb, 2))),
                      FlashUnder(th.items[0], color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("speed")
            self.play(FlashUnder(th.items[1], color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
