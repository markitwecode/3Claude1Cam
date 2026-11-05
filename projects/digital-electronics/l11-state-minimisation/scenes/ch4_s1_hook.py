"""Chapter 4, scene 1: hook: the 6-state table, "how?", L10's 74HC chips, one chip for any machine. Clips c4.hook.1 – c4.hook.2.
Opens exactly on open_card() (ch3 s8 ends on it); its part line travels into the title card.

Shared (standalone; ch3 s8 and ch4 s2 import them with load_scene("ch4_s1_hook")):
  six_table()              p. 155's 6-state table in ch1_s3_mealy's look (T 34 cells, pitch 0.5, DIM rules,
                           GREEN "Output (Y)", GREEN bold 1s), centred on ORIGIN. ch1_s3's
                           state_table() is Mealy-only (two output columns), so this is its style
                           with one output column. .rows[r].cells .cell(r, c) .head .rules .seps
  package(label=None, w, h, n_pins)
                           L8 ch1_s1's chip() (loaded by path), the part number swapped for a small
                           DIM T 30 (None: blank). .shell (body, pins, notch) .lab (or None) .body
  open_card()              ch3 s8's last shot / this scene's first: six_table() inside a blank
                           package(w 8, h 4.8, 10 pins) at (0, -0.1), "a chip you can program"
                           (T 36) at y -3.35, part line (T 40) at y 3.2. .chip .table .cap .part
  three_wired()            L10's divide-by-5 as three packages 74HC08, 74HC86, 74HC74 (w 2.6,
                           h 1.5, 7 pins, at x -4.2, 0, 4.2, y -0.4) with DIM wires between their
                           top pins. .pkgs (list) .wires (VGroup)
  four_wired()             the "different machine": 74HC08, 74HC86, 74HC08, 74HC74 at x -4.95,
                           -1.65, 1.65, 4.95, rewired. .pkgs .wires
  merged_package()         one big blank package (w 6, h 3.2, 10 pins) at (0, 0.35) with a YELLOW
                           "?" (T 120) on its face. .chip .q
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


def _load_l8(stem):
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_l8_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8H = _load_l8("ch1_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


PART_LINE = "Part 4 · State machines on a programmable chip"

# ---------------------------------------------------------------- the 6-state table (p. 155)
SIX = [("A", "A", "C", "0"), ("B", "F", "H", "0"), ("C", "C", "A", "1"),
       ("F", "F", "B", "1"), ("G", "B", "H", "0"), ("H", "C", "G", "1")]
SIX_COLS = (0.0, 1.7, 2.8, 4.9)


def six_table(rows=SIX, size=34, pitch=0.5):
    top = 0.0
    xs_ = SIX_COLS
    h_cs = T("Present\nState", size, line_spacing=0.8).move_to(_p(xs_[0], top + 0.84))
    h_ns = T("Next State", size).move_to(_p((xs_[1] + xs_[2]) / 2, top + 1.0))
    h_out = T("Output (Y)", size, GREEN).move_to(_p(xs_[3], top + 0.84))
    subs = [T(s, size, t2c={"X": BLUE}).move_to(_p(xs_[i + 1], top + 0.5)) for i, s in enumerate(["X=0", "X=1"])]
    left, right = xs_[0] - 0.8, xs_[3] + 1.2
    bottom = top - (len(rows) - 1) * pitch - pitch / 2
    head_rule = Line(_p(left, top + 0.27), _p(right, top + 0.27)).set_stroke(DIM, 2)
    seps = VGroup(*[Line(_p(x, top + 1.25), _p(x, bottom)).set_stroke(DIM, 2) for x in (0.9, 3.5)])
    row_mobs = []
    for r, vals in enumerate(rows):
        y = top - r * pitch
        cells = []
        for c, v in enumerate(vals):
            t = T(v, size, GREEN, weight=BOLD) if (c == 3 and v == "1") else T(v, size)
            cells.append(t.move_to(_p(xs_[c], y)))
        row = VGroup(*cells)
        row.cells = cells
        row_mobs.append(row)
    head = VGroup(h_cs, h_ns, h_out, *subs)
    rules = VGroup(head_rule)
    tbl = VGroup(head, rules, seps, *row_mobs)
    tbl.move_to(ORIGIN)
    tbl.head, tbl.rules, tbl.seps, tbl.rows, tbl.subs = head, rules, seps, row_mobs, subs
    tbl.cell = lambda r, c: row_mobs[r].cells[c]
    return tbl


# ---------------------------------------------------------------- packages (L8's chip())
def package(label=None, w=2.6, h=1.5, n_pins=7, size=30):
    g = L8H.chip("x", w=w, h=h, n_pins=n_pins)
    g.remove(g.lab)
    g.shell = VGroup(g.body, *g.pins, g.notch)
    if label is None:
        g.lab = None
    else:
        g.lab = T(label, size, DIM).move_to(g.body)
        g.add(g.lab)
    return g


def open_card():
    chip = package(None, w=8.0, h=4.8, n_pins=10).move_to(_p(0, -0.1))
    tbl = six_table().move_to(chip.body)
    cap = T("a chip you can program", 36).move_to(_p(0, -3.35))
    part = T(PART_LINE, 40).move_to(_p(0, 3.2))
    g = VGroup(chip, tbl, cap, part)
    g.chip, g.table, g.cap, g.part = chip, tbl, cap, part
    return g


PKG_W, PKG_H, PKG_PINS, PKG_Y = 2.6, 1.5, 7, -0.4
TOP_PIN = PKG_Y + PKG_H / 2 + 0.25


def pin_x(cx, j):
    return cx - PKG_W / 2 + (j + 0.5) * PKG_W / PKG_PINS


def wire(xa, xb, lane):
    return VMobject().set_points_as_corners(
        [_p(xa, TOP_PIN), _p(xa, lane), _p(xb, lane), _p(xb, TOP_PIN)]).set_stroke(DIM, 3)


def _wired(labels, xs, plan):
    pkgs = [package(lab).move_to(_p(x, PKG_Y)) for lab, x in zip(labels, xs)]
    wires = VGroup(*[wire(pin_x(xs[a], i), pin_x(xs[b], j), lane) for (a, i), (b, j), lane in plan])
    g = VGroup(*pkgs, wires)
    g.pkgs, g.wires, g.xs = pkgs, wires, list(xs)
    return g


THREE_X = (-4.2, 0.0, 4.2)
FOUR_X = (-4.95, -1.65, 1.65, 4.95)


def three_wired():
    return _wired(("74HC08", "74HC86", "74HC74"), THREE_X,
                  [((0, 4), (1, 0), 1.05), ((0, 6), (2, 2), 2.25), ((1, 4), (2, 0), 1.35),
                   ((1, 6), (2, 4), 1.65), ((0, 1), (2, 6), 1.95)])


def four_wired():
    return _wired(("74HC08", "74HC86", "74HC08", "74HC74"), FOUR_X,
                  [((0, 6), (1, 0), 1.05), ((1, 3), (2, 5), 1.05), ((0, 5), (2, 1), 1.95),
                   ((0, 2), (3, 5), 2.35), ((1, 6), (3, 1), 1.65), ((2, 3), (3, 3), 1.35)])


MERGED_C = _p(0, 0.35)


def merged_package():
    chip = package(None, w=6.0, h=3.2, n_pins=10).move_to(MERGED_C)
    q = T("?", 120, YELLOW).move_to(MERGED_C)
    g = VGroup(chip, q)
    g.chip, g.q = chip, q
    return g


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        card = title_card(PART_LINE)
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        end = open_card()
        self.add(*end)
        with self.say("c4.hook.1") as c:
            part4 = end.part
            self.wait(0.7)   # ch3's end card holds a moment: the cut reads as a continuation
            self.play(*during(disappear(end.chip, end.table, end.cap), 0, 0.4),
                      *during([part4.animate.scale(card.part.height / part4.height).move_to(card.part)], 0.1, 0.6),
                      *during(appear(card.title, card.rule, card.course, lag=0.2), 0.55, 1),  # early: title card
                      run_time=min(1.5, c.until("last", floor=1.0)))
            self.remove(part4)
            self.add(card.part)
            c.wait_until("last")

            # {last}: the 6-state table, the merged states A and C (Present State column) GOLD, "8 -> 6 states"
            tbl = six_table().move_to(_p(-2.7, 0.1))
            sweep_clear(self, *appear(tbl, shift=None), run_time=1.6)
            c.wait_until("equivalent")
            merged = [tbl.cell(r, 0) for r, row in enumerate(SIX) if row[0] in "AC"]   # the merged states' names only
            self.play(*[m.animate.set_color(GOLD) for m in merged], run_time=1.0)
            tag = T("8 → 6 states", 48, GOLD).move_to(_p(3.9, 0.1))
            c.wait_until("eight states")
            self.play(*appear(tag), run_time=min(1.0, c.until("build", floor=0.5)))
            c.wait_until("build")

            # {build}: the table goes, "how?" takes its place
            how = T("how?", 80, YELLOW).move_to(tbl)
            self.play(*swap(tbl, how), run_time=min(1.4, c.until("question", floor=0.8)))
            self.tag, self.how = tag, how

    def clip2(self):
        A = three_wired()
        tags = [T(s, 32, YELLOW) for s in ("and gates", "exclusive-or gates", "flip-flops")]
        for t, p in zip(tags, A.pkgs):
            t.move_to(_p(p.get_x(), -1.95))
        with self.say("c4.hook.2") as c:
            self.play(*during(disappear(self.how, self.tag), 0, 0.35),
                      *during(appear(*A.pkgs, lag=0.3), 0.3, 1), run_time=2.2)  # early: chip numbers aren't spoken
            # keep each package's shell and part number as separate top-level pieces
            for p in A.pkgs:
                self.remove(p)
                self.add(p.shell, p.lab)
            c.wait_until("kinds")

            for t in tags:
                c.wait_until(own_word=t)
                self.play(*appear(t), run_time=0.8)
            c.wait_until("joined up")
            self.play(*[Create(w) for w in A.wires], run_time=min(1.4, c.until("change", floor=0.6)))
            c.wait_until("change")

            # {change}: the wires flash RED, the board is rewired, a second 74HC08 slides in
            self.play(*[w.animate.set_stroke(RED, 5) for w in A.wires], run_time=0.6)
            B = four_wired()
            moves = []
            for k, (p, t) in enumerate(zip(A.pkgs, tags)):
                nx = B.xs[[0, 1, 3][k]]
                dx = (nx - p.get_x()) * RIGHT
                moves += [p.shell.animate.shift(dx), p.lab.animate.shift(dx), t.animate.shift(dx)]
            new = B.pkgs[2]
            self.play(*during([FadeOut(w) for w in A.wires], 0, 0.35),
                      *during(moves, 0.2, 0.7),
                      *during([FadeIn(new, shift=0.8 * DOWN)], 0.45, 0.85),
                      *during([Create(w) for w in B.wires], 0.65, 1),
                      run_time=min(2.2, c.until("one", floor=1.2)))
            self.remove(new)
            self.add(new.shell, new.lab)
            shells = [p.shell for p in A.pkgs] + [new.shell]
            labs = [p.lab for p in A.pkgs] + [new.lab]
            c.wait_until("one")

            # {one}: everything slides together into one blank package with a "?"
            M = merged_package()
            # labels, tags and wires fade first; the bare packages slide together and shrink into a row
            # that fits inside the merged package's body, which fades in around them; then they fade
            # into it and the "?" takes their place
            T_all = c.until("question", floor=2.0)
            s_ = 0.42
            gx = [-1.95, -0.65, 0.65, 1.95]
            shells = sorted(shells, key=lambda m: m.get_x())   # left to right, so no two cross
            gather = [sh.animate.scale(s_).move_to(MERGED_C + gx[k] * RIGHT) for k, sh in enumerate(shells)]
            self.play(*during(disappear(*labs, *tags, *B.wires), 0, 0.3),
                      *during(gather, 0.25, 0.8),
                      *during([FadeIn(M.chip, scale=1.08)], 0.65, 1),
                      run_time=min(1.9, 0.62 * T_all))
            self.play(*during([FadeOut(sh) for sh in shells], 0, 0.6),
                      *during(appear(M.q, shift=None), 0.4, 1),
                      run_time=min(1.0, max(0.5, c.until("question", floor=0.5))))
            cap = T("one chip, any state machine?", 40).move_to(_p(0, -2.55))
            c.wait_until(own_word=cap, cue="question")
            self.play(*appear(cap), run_time=1.0)
