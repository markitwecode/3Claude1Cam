"""Chapter 1, scene 3: Mealy machines (refresher of L9 pp. 122-123) and p. 145's compact state table.
Clips c1.mealy.1 - c1.mealy.4.

Shared helpers (import with load_scene("ch1_s3_mealy")):
- `MACHINE`: p. 145's 15 rows, (state, next X=0, next X=1, Y X=0, Y X=1), verbatim.
- `state_table(rows=MACHINE, size=30, pitch=0.37, top=2.45, x0=0.0, rules_after=("A", "C", "G"))`:
  the lecture's compact table. Parts: `.rows[r]` (VGroup row; `.rows[r].cells` = [state, n0, n1, y0, y1],
  each a Text), `.cell(r, c)`, `.col(c)` (VGroup of column c's cells), `.row_of(letter)`,
  `.h_cs .h_ns .h_out` (headers), `.subs` (the four "X=0"/"X=1" Texts), `.xs` (their X glyphs, BLUE),
  `.y` (the Y glyph of "Output (Y)"), `.rules`, `.seps`, `.head` (all header parts),
  `.col_box(cols, color=YELLOW)` / `.row_box(r, color=YELLOW)`: highlight Rectangles (not added).
  Light letters as spoken with `recolor(tbl.cell(r, c), YELLOW)`; appear rows with
  `appear(*tbl.rows)` and then `settle(scene, tbl)`.
- `mealy_label(inp, out, size=44)`: arc label "inp/out", input BLUE, slash FG, output GREEN;
  `.inp .slash .out`.
- `moore_schematic()`: L10 ch1 s2's Moore schematic (same coordinates); dict of parts + "all".
"""
# style: 2
import importlib.util
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
from lib.paths import load_scene  # noqa: E402


def _load_l10(stem):
    path = Path(__file__).resolve().parents[2] / "l10-state-assignment" / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_l10_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L10M = _load_l10("ch1_s2_machines")


def _p(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ shared: the compact table
MACHINE = [
    ("A", "B", "C", "0", "0"), ("B", "D", "E", "0", "0"), ("C", "F", "G", "0", "0"),
    ("D", "H", "I", "0", "0"), ("E", "J", "K", "0", "0"), ("F", "L", "M", "0", "0"),
    ("G", "N", "P", "0", "0"), ("H", "A", "A", "0", "0"), ("I", "A", "A", "0", "0"),
    ("J", "A", "A", "0", "1"), ("K", "A", "A", "0", "0"), ("L", "A", "A", "0", "1"),
    ("M", "A", "A", "0", "0"), ("N", "A", "A", "0", "0"), ("P", "A", "A", "0", "0"),
]
TABLE_COLS = (0.0, 1.6, 2.7, 4.0, 5.1)


def state_table(rows=MACHINE, size=30, pitch=0.37, top=2.45, x0=0.0, rules_after=("A", "C", "G")):
    xs_ = [x0 + c for c in TABLE_COLS]
    h_cs = T("Current\nState", size, line_spacing=0.8).move_to(_p(xs_[0], top + 0.75))
    h_ns = T("Next State", size).move_to(_p((xs_[1] + xs_[2]) / 2, top + 1.0))
    h_out = T("Output (Y)", size, GREEN).move_to(_p((xs_[3] + xs_[4]) / 2, top + 1.0))
    subs = [T(s, size, t2c={"X": BLUE}).move_to(_p(xs_[i + 1], top + 0.5))
            for i, s in enumerate(["X=0", "X=1", "X=0", "X=1"])]
    left, right = xs_[0] - 0.7, xs_[4] + 0.55
    bottom = top - (len(rows) - 1) * pitch - pitch / 2
    head_rule = Line(_p(left, top + 0.27), _p(right, top + 0.27)).set_stroke(DIM, 2)
    seps = VGroup(*[Line(_p(x, top + 1.25), _p(x, bottom)).set_stroke(DIM, 2)
                    for x in ((xs_[0] + xs_[1]) / 2 + 0.05, (xs_[2] + xs_[3]) / 2)])
    row_mobs = []
    rules = VGroup(head_rule)
    for r, vals in enumerate(rows):
        y = top - r * pitch
        cells = []
        for c, v in enumerate(vals):
            if c >= 3 and v == "1":
                t = T(v, size, GREEN, weight=BOLD)
            else:
                t = T(v, size)
            cells.append(t.move_to(_p(xs_[c], y)))
        row = VGroup(*cells)
        row.cells = cells
        row_mobs.append(row)
        if vals[0] in rules_after and r < len(rows) - 1:
            rules.add(Line(_p(left, y - pitch / 2), _p(right, y - pitch / 2)).set_stroke(DIM, 1.5))
    head = VGroup(h_cs, h_ns, h_out, *subs)
    tbl = VGroup(head, rules, seps, *row_mobs)
    tbl.head, tbl.rules, tbl.seps, tbl.rows = head, rules, seps, row_mobs
    tbl.h_cs, tbl.h_ns, tbl.h_out, tbl.subs = h_cs, h_ns, h_out, subs
    tbl.xs = [s[0] for s in subs]
    tbl.y = select(h_out, "Y")[0]
    tbl.pitch = pitch
    tbl.cell = lambda r, c: row_mobs[r].cells[c]
    tbl.col = lambda c: VGroup(*[row.cells[c] for row in row_mobs])
    tbl.row_of = lambda letter: [v[0] for v in rows].index(letter)

    def col_box(cols, color=YELLOW):
        xa = min(row_mobs[0].cells[c].get_x() for c in cols) - 0.48
        xb = max(row_mobs[0].cells[c].get_x() for c in cols) + 0.48
        ya = subs[0].get_top()[1] + 0.12
        yb = row_mobs[-1].cells[0].get_y() - pitch / 2
        return (Rectangle(width=xb - xa, height=ya - yb).move_to(_p((xa + xb) / 2, (ya + yb) / 2))
                .set_stroke(color, 2).set_fill(color, 0.15).set_z_index(-1))

    def row_box(r, color=YELLOW):
        row = row_mobs[r]
        xa = row.cells[0].get_x() - 0.25
        xb = h_out.get_right()[0] + 0.05
        return (Rectangle(width=xb - xa, height=pitch * 0.98).move_to(_p((xa + xb) / 2, row.cells[0].get_y()))
                .set_stroke(color, 2).set_fill(color, 0.18).set_z_index(-1))

    tbl.col_box, tbl.row_box = col_box, row_box
    return tbl


def mealy_label(inp, out, size=44):
    a = T(inp, size, BLUE)
    s = T("/", size, FG)
    b = T(out, size, GREEN)
    g = VGroup(a, s, b).arrange(RIGHT, buff=0.05)
    g.inp, g.slash, g.out = a, s, b
    return g


# ------------------------------------------------------------------ L10's Moore schematic
def moore_schematic():
    """L10 ch1 s2 clip2's schematic, same coordinates and helpers."""
    dff, bus_slash, logic_box = L10M.dff, L10M.bus_slash, L10M.logic_box
    inp = T("Inputs", 32, BLUE).move_to(_p(-6.15, 0))
    in_w = Arrow(_p(-5.48, 0), _p(-4.7, 0), buff=0, stroke_width=4,
                 max_tip_length_to_length_ratio=0.3).set_color(BLUE)
    in_s, in_n = bus_slash(-5.05, 0, "n", BLUE)
    b1, b1t = logic_box("Next state\ncombinational\nlogic", -3.4)
    d_w = Arrow(_p(-2.1, 0), _p(-0.7, 0), buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.2).set_color(BLUE)
    d_s, d_m = bus_slash(-1.4, 0, "m", BLUE)
    ff = dff(_p(0, -0.45))
    qb_w = Line(_p(0.7, -0.9), _p(1.0, -0.9)).set_stroke(GREEN, 3)
    q_w = Arrow(_p(0.7, 0), _p(1.75, 0), buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.25).set_color(GREEN)
    q_s, q_m = bus_slash(1.42, 0, "m", GREEN)
    b2, b2t = logic_box("Optional\ncombinational\nlogic", 3.05)
    out_w = Arrow(_p(4.35, 0), _p(5.05, 0), buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.3).set_color(GREEN)
    outp = T("Outputs", 32, GREEN).next_to(out_w, RIGHT, buff=0.12)
    tap = Dot(_p(1.05, 0), radius=0.07, color=GREEN)
    loop_up = VMobject().set_points_as_corners([_p(1.05, 0), _p(1.05, 1.9), _p(-3.4, 1.9)])
    loop_up.set_stroke(GREEN, 4)
    loop_dn = Arrow(_p(-3.4, 1.9), _p(-3.4, 1.0), buff=0, stroke_width=4,
                    max_tip_length_to_length_ratio=0.3).set_color(GREEN)
    cs = T("Current state", 30, GREEN).move_to(_p(-1.2, 2.3))
    clk_w = Line(_p(0, -2.05), _p(0, -1.47)).set_stroke(YELLOW, 4)
    clk = T("CLK", 30, YELLOW).next_to(clk_w.get_start(), LEFT, buff=0.12)
    parts = dict(inp=inp, in_w=in_w, in_s=in_s, in_n=in_n, b1=b1, b1t=b1t, d_w=d_w, d_s=d_s, d_m=d_m,
                 ff=ff, qb_w=qb_w, q_w=q_w, q_s=q_s, q_m=q_m, tap=tap, b2=b2, b2t=b2t, out_w=out_w,
                 outp=outp, loop_up=loop_up, loop_dn=loop_dn, cs=cs, clk_w=clk_w, clk=clk)
    parts["all"] = list(parts.values())
    return parts


def _circle(name, center, r=0.6, size=40):
    c = Circle(radius=r).set_stroke(FG, 3).move_to(center)
    t = (MathTex(name, font_size=size + 8) if "_" in name else T(name, size)).move_to(center)
    return c, t


class Mealy(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1: Moore -> Mealy schematic
    def clip1(self):
        with self.say("c1.mealy.1") as c:
            head = T("Moore and Mealy", 48).move_to(_p(-0.6, 3.4))
            chip_t = T("refresher: Lecture 9", 28, DIM)
            chip_b = RoundedRectangle(corner_radius=0.15, width=chip_t.width + 0.4,
                                      height=chip_t.height + 0.3).set_stroke(DIM, 2)
            chip = VGroup(chip_b, chip_t).move_to(_p(4.75, 3.4))
            chip_t.move_to(chip_b)
            self.head, self.chip = head, chip
            self.play(*appear(head), run_time=1.0)
            self.play(*appear(chip, shift=None), run_time=0.8)  # early: chip tags the refresher just named
            c.wait_until("moore")

            P = moore_schematic()
            self.P = P
            shown = [m for m in P["all"] if m not in (P["clk"], P["clk_w"])]
            self.play(*appear(*shown, P["clk_w"], P["clk"], shift=None, lag=0.04),  # early: whole schematic at once
                      run_time=2.0)
            tag = T("Moore: outputs from the state alone", 30, t2c={"Moore:": GREEN}).move_to(_p(0, -3.25))
            self.play(*appear(tag), run_time=1.0)  # early: tag sums up the sentence being said
            c.wait_until("mealy")

            new_b2t = T("combinational\nlogic", 28, line_spacing=0.85).move_to(P["b2"])
            path = VMobject().set_points_as_corners([_p(-5.3, 0), _p(-5.3, -2.6), _p(2.6, -2.6), _p(2.6, -1.2)])
            path.set_stroke(BLUE, 4)
            tip = Arrow(_p(2.6, -1.4), _p(2.6, -1.0), buff=0, stroke_width=4,
                        max_tip_length_to_length_ratio=0.6).set_color(BLUE)
            m_dot = Dot(_p(-5.3, 0), radius=0.07, color=BLUE)
            self.play(*swap(P["b2t"], new_b2t), run_time=1.2)  # early: the box changes as the Mealy line is said
            P["all"] = [new_b2t if m is P["b2t"] else m for m in P["all"]]
            P["b2t"] = new_b2t
            self.play(FadeIn(m_dot), Create(path), time_span(GrowArrow(tip), 1.2, 1.6), run_time=1.6)
            mtag = T("Mealy: outputs from the state and the inputs", 30,
                     t2c={"Mealy:": BLUE}).move_to(_p(0, -3.25))
            self.play(*swap(tag, mtag), run_time=min(1.2, c.until("schematic")))
            self.mtag = mtag
            self.mwire = [path, tip, m_dot]
            c.wait_until("schematic")

            full = VMobject().set_points_as_corners([_p(-5.3, 0), _p(-5.3, -2.6), _p(2.6, -2.6), _p(2.6, -1.0)])
            self.play(VShowPassingFlash(full.set_stroke(YELLOW, 9), time_width=0.5),
                      VShowPassingFlash(Line(_p(0.7, 0), _p(1.75, 0)).set_stroke(YELLOW, 9), time_width=0.8),
                      run_time=1.8)
            c.wait_until("the inputs directly")
            self.play(VShowPassingFlash(full.copy().set_stroke(YELLOW, 9), time_width=0.5),
                      FlashAround(P["b2"], time_width=1.5),
                      run_time=min(1.6, max(0.6, c.remaining)))

    # ------------------------------------------------------------ c2: labels on arcs
    def clip2(self):
        with self.say("c1.mealy.2") as c:
            self.play(*disappear(self.head, self.chip, self.mtag), run_time=0.7)
            sch = VGroup(*self.P["all"], *self.mwire)
            target = sch.copy().scale(0.3).to_corner(UL, buff=0.45).set_opacity(0)
            ca, ta = _circle("s_1", _p(-5.0, -0.6))
            cb, tb = _circle("s_2", _p(-1.8, -0.6))
            arc = L10M._arc(_p(-4.4, -0.45), _p(-2.4, -0.45), -0.7)
            mt = T("Mealy", 36).move_to(_p(-3.4, -1.85))
            self.play(*during([Transform(sch, target)], 0, 0.6),
                      *during(appear(ca, ta, cb, tb, mt, shift=None, lag=0.1), 0.3, 1),
                      time_span(Create(arc), 0.8, 1.5), run_time=1.5)
            self.remove(*sch.get_family())
            c.wait_until("label")

            lab = mealy_label("1", "0", 48).move_to(_p(-3.4, 0.5))
            cap_i = T("input", 30, BLUE).next_to(lab, LEFT, buff=0.3)
            cap_o = T("output", 30, GREEN).next_to(lab, RIGHT, buff=0.3)
            self.play(*appear(lab), run_time=1.0)
            self.play(*appear(cap_i, cap_o, shift=None, lag=0.4), run_time=1.2)  # early: names the parts just said
            c.wait_until("moorearc")

            pa = Circle(radius=0.6).set_stroke(FG, 3).move_to(_p(1.8, -0.6))
            pb = Circle(radius=0.6).set_stroke(FG, 3).move_to(_p(5.0, -0.6))
            na = MathTex("s_1", font_size=42).move_to(pa.get_center() + 0.18 * UP)
            nb = MathTex("s_2", font_size=42).move_to(pb.get_center() + 0.18 * UP)
            oa = T("0", 34, GREEN).move_to(pa.get_center() + 0.25 * DOWN)
            ob = T("1", 34, GREEN).move_to(pb.get_center() + 0.25 * DOWN)
            arc2 = L10M._arc(_p(2.4, -0.45), _p(4.4, -0.45), -0.7)
            lab2 = T("1", 48, BLUE).move_to(_p(3.4, 0.5))
            mo = T("Moore", 36).move_to(_p(3.4, -1.85))
            self.play(*appear(pa, na, oa, pb, nb, ob, mo, shift=None, lag=0.08),
                      time_span(Create(arc2), 0.8, 1.5), run_time=1.5)
            self.play(*appear(lab2), run_time=0.8)
            c.wait_until("output comes")
            self.play(*flash([oa, ob], color=GREEN, time_width=1.5), run_time=min(1.4, max(0.5, c.remaining)))

    # ------------------------------------------------------------ c3: p. 145's table
    def clip3(self):
        with self.say("c1.mealy.3") as c:
            tbl = state_table(x0=-2.0)
            self.tbl = tbl
            sweep_clear(self, *appear(tbl.head, tbl.rules[0], tbl.seps, shift=None, lag=0.1), run_time=1.2)
            self.play(*appear(*tbl.rows, *tbl.rules[1:], shift=None, lag=0.1),  # early: table shown whole, then walked
                      run_time=min(1.6, c.until("xy")))
            settle(self, tbl)
            c.wait_until("xy")

            self.play(*flash([*tbl.xs, tbl.y], time_width=1.5), run_time=1.5)
            c.wait_until("cols")

            box = tbl.col_box([1, 2])
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("outs")
            self.play(Transform(box, tbl.col_box([3, 4])), run_time=1.3)
            c.wait_until("letters")

            letters = [row.cells[0] for row in tbl.rows]
            step, span = 0.17, 0.34     # one colour pulse per letter, top to bottom, no rings overlapping

            def pulse(m):
                def f(mob, a):
                    mob.set_color(interpolate_color(ManimColor(FG), ManimColor(YELLOW), np.sin(PI * a)))
                return UpdateFromAlphaFunc(m, f)
            fl = [time_span(pulse(l), step * i, step * i + span) for i, l in enumerate(letters)]
            self.play(FadeOut(box), *fl, run_time=step * 14 + span)
            c.wait_until("skipping")

            yb = (letters[13].get_y() + letters[14].get_y()) / 2
            brace = Brace(VGroup(*letters), LEFT, buff=0.2).set_color(GOLD)
            no_o = T("no O", 28).move_to(_p(brace.get_left()[0] - 0.55, yb))
            self.play(*appear(no_o, shift=None), run_time=0.8)
            c.wait_until("fifteen")
            fif = T("15", 40, GOLD).next_to(brace, LEFT, buff=0.15)
            self.play(GrowFromCenter(brace), *appear(fif, shift=None), run_time=min(1.0, c.remaining))
            self.side = [brace, no_o, fif]

    # ------------------------------------------------------------ c4: row A, compact vs long
    def clip4(self):
        tbl = self.tbl
        with self.say("c1.mealy.4") as c:
            self.play(*[m.animate.shift(3.1 * LEFT) for m in [tbl, *self.side]], run_time=1.0)
            rbox = tbl.row_box(0)
            self.play(FadeIn(rbox), run_time=0.7)
            c.wait_until("zero")

            z = [tbl.cell(0, 1), tbl.cell(0, 3)]
            o = [tbl.cell(0, 2), tbl.cell(0, 4)]
            c.wait_until("state bee")
            self.play(*recolor(z[:1], YELLOW), *flash(z[:1], time_width=1.5), run_time=1.0)
            c.wait_until("output zero")
            self.play(*recolor(z[1:], YELLOW), *flash(z[1:], time_width=1.5), run_time=1.0)
            c.wait_until("one")
            self.play(*recolor(z, FG), *recolor(o[:1], YELLOW), *flash(o[:1], time_width=1.5), run_time=1.0)
            c.wait_until("also with output")
            self.play(*recolor(o[1:], YELLOW), *flash(o[1:], time_width=1.5), run_time=1.0)
            c.wait_until("arcs")

            S4 = load_scene("ch1_s4_tree")
            k = 0.85     # s4's tree spacing (A over B and C), at this scene's scale
            pa_ = _p(3.7, 1.6)
            pb_ = pa_ + k * (S4.POS["B"] - S4.POS["A"]) * _p(1, 1.4)
            pc_ = pa_ + k * (S4.POS["C"] - S4.POS["A"]) * _p(1, 1.4)
            ca, ta = _circle("A", pa_, r=0.55)
            cb, tb = _circle("B", pb_, r=0.55)
            cc, tc = _circle("C", pc_, r=0.55)

            def edge(a, b):
                d = (b - a) / np.linalg.norm(b - a)
                return Arrow(a + d * 0.55, b - d * 0.55, buff=0, stroke_width=4,
                             max_tip_length_to_length_ratio=0.12).set_color(FG)
            ab, ac = edge(pa_, pb_), edge(pa_, pc_)
            self.play(*appear(ca, ta, shift=None), run_time=0.8)
            self.play(*appear(cb, tb, cc, tc, shift=None, lag=0.2), GrowArrow(ab), GrowArrow(ac), run_time=1.4)
            l00 = S4.place_on_arc(S4.mealy_label(0, 0, size=40), ab.get_start(), ab.get_end(), -1)
            l10 = S4.place_on_arc(S4.mealy_label(1, 0, size=40), ac.get_start(), ac.get_end(), 1)
            c.wait_until("zero slash zero")
            self.play(*appear(l00), run_time=0.8)
            c.wait_until("one slash zero")
            self.play(*appear(l10), run_time=0.8)
            mini = [ca, ta, cb, tb, cc, tc, ab, ac, l00, l10]
            c.wait_until("compact")

            self.play(FadeOut(rbox), *recolor(o, FG), *disappear(*self.side), run_time=0.8)
            pairs = [tbl.col_box([1, 2]).set_opacity(0), tbl.col_box([3, 4]).set_opacity(0)]
            self.play(*flash(pairs, time_width=1.5), run_time=1.6)
            c.wait_until("long")

            self.play(*disappear(*mini), run_time=0.7)
            gx = [1.7, 2.95, 4.2, 5.45]
            top = tbl.rows[0].cells[0].get_y()
            gh = VGroup(T("Current\nState", 28, line_spacing=0.8).move_to(_p(gx[0], top + 0.75)),
                        T("X", 28, BLUE).move_to(_p(gx[1], top + 0.75)),
                        T("Next\nState", 28, line_spacing=0.8).move_to(_p(gx[2], top + 0.75)),
                        T("Y", 28, GREEN).move_to(_p(gx[3], top + 0.75)))
            grule = Line(_p(gx[0] - 0.7, top + 0.27), _p(gx[3] + 0.4, top + 0.27)).set_stroke(DIM, 2)
            ghead = VGroup(gh, grule).set_opacity(0.75)
            grows = []
            n = 16
            for i in range(n):
                s, nx = MACHINE[i // 2][0], MACHINE[i // 2][1 + i % 2]
                y_ = MACHINE[i // 2][3 + i % 2]
                y = top - i * tbl.pitch
                row = VGroup(T(s, 30).move_to(_p(gx[0], y)), T(str(i % 2), 30, BLUE).move_to(_p(gx[1], y)),
                             T(nx, 30).move_to(_p(gx[2], y)), T(y_, 30, GREEN).move_to(_p(gx[3], y)))
                row.set_opacity(0.75 if i < 8 else 0.75 * (n - i) / (n - 7))   # A A B B C C D D read clearly
                grows.append(row)
            self.play(*appear(ghead, *grows, shift=None, lag=0.12),  # early: the ghost unrolls as one picture
                      run_time=min(3.0, c.until("count")), rate_func=linear)
            c.wait_until("fifteen")

            r15 = T("15 rows", 36, GOLD).move_to(_p(tbl.seps.get_center()[0] + 0.6, -3.4))
            r15.set_x(VGroup(tbl.h_cs, tbl.h_out).get_center()[0])
            self.play(*appear(r15), run_time=0.9)
            c.wait_until("thirty")
            r30 = T("30 rows", 36, GOLD).move_to(_p((gx[0] + gx[3]) / 2, -3.4))
            self.play(*appear(r30), run_time=min(0.9, max(0.4, c.remaining)))
