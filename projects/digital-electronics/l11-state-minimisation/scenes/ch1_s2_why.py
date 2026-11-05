"""Chapter 1, scene 2: why fewer states? p. 144's two bullets; fewer flip-flops (the L10 ladder:
15 states -> 4, 7 -> 3), more unused codes as don't cares, more freedom; 'may': only across a power
of two. Clips c1.why.1 – c1.why.4.

Chapter-wide helpers owned here (s7 and the s8 recap reuse them):
- ladder(scale=LAD_SCALE) -> L10 ch1 s4's doubling_ladder(), scaled; same attributes (.rows, .labs,
  .counts, .pats), centred on ORIGIN.
- ladder_bracket(lad, row, n, x=None) -> VGroup(brace, tag, formula): a GOLD brace on row `row`
  (0-based: 3 is the "4" row), tag "n states" (GOLD) over \\lceil \\log_2 n \\rceil = k (YELLOW
  brackets). x = brace's left x (default just right of the row's patterns). Attributes .brace .tag .formula.
- code_chips(unused=("110", "111"), crossed=True, pitch=1.45, row_gap=1.3) -> VGroup of eight GREEN
  code chips 000..111 (two rows of four, L10 ch1 s3's pattern_chip), unused ones DIM with a GOLD X
  laid on the chip (chip_cross). Attributes .chips (by code index), .crosses (dict code -> X).
- pattern_chip(code), chip_cross(chip): L10 ch1 s3's chip and don't-care X.
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


def _load_l10(stem):
    path = Path(__file__).resolve().parents[2] / "l10-state-assignment" / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_l10_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L10C = _load_l10("ch1_s4_choice")
doubling_ladder = L10C.doubling_ladder
ceil_log2 = L10C.ceil_log2


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- chapter-wide helpers ------------------------------------------------------------------------
LAD_SCALE = 0.84


def ladder(scale=LAD_SCALE):
    lad = doubling_ladder(pat_size=34)
    lad.scale(scale)
    return lad


def ladder_bracket(lad, row, n, x=None):
    r = lad.rows[row]
    if x is None:
        x = lad.pats[row].get_right()[0] + 0.12
    h = max(r.height, 0.5)
    c = r.get_y()
    brace = Brace(Line(_p(x, c + h / 2), _p(x, c - h / 2)), direction=RIGHT, buff=0.05, color=GOLD)
    k = int(np.ceil(np.log2(n)))
    tag = T(f"{n} states", 30, GOLD)
    f = MathTex(r"\lceil", rf"\log_2 {n}", r"\rceil", rf"= {k}", font_size=34, color=FG)
    f[0].set_color(YELLOW)
    f[2].set_color(YELLOW)
    stack = VGroup(tag, f).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    stack.next_to(brace, RIGHT, buff=0.12)
    g = VGroup(brace, tag, f)
    g.brace, g.tag, g.formula = brace, tag, f
    return g


def pattern_chip(code):
    box = RoundedRectangle(corner_radius=0.12, width=1.2, height=0.72).set_stroke(DIM, 2).set_fill(BG, 1)
    txt = Mono(code, 34, FG).move_to(box)
    g = VGroup(box, txt)
    g.box, g.txt, g.code = box, txt, code
    return g


def chip_cross(chip):
    """A GOLD don't-care X laid on an unused chip, over its DIM code."""
    return cross_mark(color=GOLD, r=0.26).set_stroke(width=6).move_to(chip).set_z_index(2)


def _green(ch):
    ch.box.set_stroke(GREEN, 4)
    ch.txt.set_color(GREEN)
    return ch


def code_chips(unused=("110", "111"), crossed=True, pitch=1.45, row_gap=1.3):
    chips = []
    for j in range(8):
        ch = _green(pattern_chip(format(j, "03b")))
        ch.move_to(_p((j % 4 - 1.5) * pitch, -(j // 4 - 0.5) * row_gap))
        chips.append(ch)
    g = VGroup(*chips)
    g.chips, g.crosses = chips, {}
    for code in unused:
        ch = chips[int(code, 2)]
        ch.box.set_stroke(DIM, 2)
        ch.txt.set_color(DIM)
        if crossed:
            x = chip_cross(ch)
            g.add(x)
            g.crosses[code] = x
    return g


# ---- scene-local drawings ------------------------------------------------------------------------
R = 0.55
NODES = {"A": _p(-4.5, -1.3), "B": _p(-1.5, -0.2), "C": _p(-1.5, -2.4), "D": _p(1.5, -1.3), "E": _p(4.5, -1.3)}


def state(name):
    c = Circle(radius=R).set_stroke(BLUE, 4).move_to(NODES[name])
    lab = T(name, 38).move_to(c)
    g = VGroup(c, lab)
    g.circle, g.lab = c, lab
    return g


def arc(a, b):
    pa, pb = NODES[a], NODES[b]
    u = (pb - pa) / np.linalg.norm(pb - pa)
    return Arrow(pa + R * u, pb - R * u, buff=0.06, stroke_width=4, color=FG,
                 max_tip_length_to_length_ratio=0.15)


def kmap_outline(cell=0.8):
    cells = [[Square(cell).set_stroke(DIM, 2) for _ in range(4)] for _ in range(2)]
    for r in range(2):
        for k in range(4):
            cells[r][k].move_to(_p((k - 1.5) * cell, (0.5 - r) * cell))
    grid = VGroup(*[s for row in cells for s in row])
    cols = VGroup(*[Mono(s, 28, DIM).next_to(cells[0][k], UP, buff=0.12) for k, s in enumerate(["00", "01", "11", "10"])])
    rows = VGroup(*[Mono(s, 28, DIM).next_to(cells[r][0], LEFT, buff=0.15) for r, s in enumerate(["0", "1"])])
    title = T("next-state K-map", 30, DIM).next_to(cols, UP, buff=0.25)
    g = VGroup(title, cols, rows, grid)
    g.cells, g.title = cells, title
    return g


BULLET2 = ["In general, reducing the number of states may",
           "reduce the number of FFs required and may also reduce the",
           "complexity of the next state logic owing to the presence of",
           "more unused states (don’t cares)"]


class Why(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- p. 144: unnecessary states -------------------------------------------------------------
    def clip1(self):
        with self.say("c1.why.1") as c:
            head = T("Elimination of Redundant States", 46).move_to(_p(0, 3.35))
            self.head = head
            self.play(*appear(head), run_time=1.0)   # early: slide heading, shown as the slide opens
            b1 = VGroup(T("•  Sometimes, when designing state machines it is possible that", 32),
                        T("unnecessary states may be introduced", 32)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            b1[1].shift(0.42 * RIGHT)
            b1.move_to(_p(0, 2.1))
            c.wait_until("When you design")
            self.play(*appear(*b1, lag=0.3), run_time=1.2)   # early: the slide's bullet, read in paraphrase
            self.b1 = b1

            st = {k: state(k) for k in NODES}
            arcs = {(a, b): arc(a, b) for a, b in [("A", "B"), ("B", "D"), ("D", "E"), ("A", "C"), ("C", "D")]}
            steps = [("draw", "A", []), ("draw the diagram", "B", [("A", "B")]),
                     ("one state at a time", "D", [("B", "D")]), ("new situation", "E", [("D", "E")]),
                     ("fresh circle", "C", [("A", "C"), ("C", "D")])]
            for i, (cue, name, new_arcs) in enumerate(steps):
                c.wait_until(cue)
                anims = [*[GrowArrow(arcs[k]) for k in new_arcs],
                         *during([GrowFromCenter(st[name].circle), FadeIn(st[name].lab)], 0.3, 1)]
                self.play(*anims, run_time=1.2 if i < 2 else 0.9)
            self.st, self.arcs = st, arcs

            c.wait_until("same")
            pair = [st["B"].circle, st["C"].circle, arcs[("B", "D")], arcs[("C", "D")]]
            rings = [VShowPassingFlash(st[k].circle.copy().set_stroke(GOLD, 9), time_width=0.6) for k in "BC"]
            self.play(*recolor(pair, GOLD), *rings, run_time=min(1.6, c.until(floor=0.8)))

    # -- fewer flip-flops ------------------------------------------------------------------------
    def clip2(self):
        with self.say("c1.why.2") as c:
            b2 = VGroup(*[T(s, 30) for s in BULLET2]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            dot = T("•", 30).next_to(b2[0], LEFT, buff=0.2)
            b2.add(dot)
            b2.move_to(_p(0, 2.7))
            self.b2 = b2
            sweep_clear(self, *appear(*b2[:4], dot, lag=0.15), keep=[],
                        run_time=min(1.6, c.until("fewer")))
            c.wait_until("fewer")
            hot = select(b2[1], "reduce the number of FFs required")[0]
            self.play(*recolor(hot, YELLOW), FlashUnder(hot, color=YELLOW, run_time=1.4, time_width=1.5), run_time=1.4)

            c.wait_until("ladder")
            lad = ladder()
            lad.move_to(_p(0, -0.8)).align_to(_p(-6.6, 0), LEFT)
            lad.set_opacity(DIMMED)
            self.lad = lad
            self.play(FadeIn(lad), run_time=1.0)   # early: whole ladder shown dim, then walked row by row
            cues = ["One flip-flop", "two give four", "three give eight", "four give sixteen"]
            for i, cue in enumerate(cues):
                c.wait_until(cue)
                self.play(restyle(lad.rows[i], op=1), FlashAround(lad.counts[i], color=YELLOW, run_time=0.9),
                          run_time=0.9 if i == 0 else 0.7)

            c.wait_until("fifteen")
            b15 = ladder_bracket(lad, 3, 15)
            self.play(GrowFromCenter(b15.brace), *during(appear(b15.tag, b15.formula, lag=0.3), 0.25, 1), run_time=1.5)
            self.b15 = b15
            c.wait_until("seven")
            b7 = ladder_bracket(lad, 2, 7, x=b15.brace.get_left()[0])
            self.play(GrowFromCenter(b7.brace), *during(appear(b7.tag, b7.formula, lag=0.3), 0.25, 1),
                      run_time=min(1.5, c.until(floor=0.8)))
            self.b7 = b7

    # -- more unused codes -----------------------------------------------------------------------
    def clip3(self):
        with self.say("c1.why.3") as c:
            hot = select(self.b2[3], "more unused states (don’t cares)")[0]
            self.play(*recolor(hot, YELLOW), FlashUnder(hot, color=YELLOW, run_time=1.4, time_width=1.5), run_time=1.4)

            c.wait_until("eight")
            lad = self.lad
            grid = code_chips(unused=(), crossed=False)
            grid.move_to(_p(-2.9, -0.8))
            gone = [*[m for i, r in enumerate(lad.rows) for m in r if not (i == 2 and m is lad.pats[2])],
                    self.b15, self.b7]
            src = lad.pats[2]
            src.generate_target()
            src.target.scale(1.3).move_to(grid)
            self.play(*during(disappear(*gone), 0, 0.35), *during([MoveToTarget(src)], 0.15, 0.55),
                      *during(swap(src, grid), 0.55, 1), run_time=min(2.2, c.until("six")))
            self.remove(*lad.get_family())
            c.wait_until("six")
            dead = [grid.chips[6], grid.chips[7]]
            self.play(*[ch.box.animate.set_stroke(DIM, 2) for ch in dead],
                      *[ch.txt.animate.set_color(DIM) for ch in dead], run_time=1.2)

            c.wait_until("don't cares")
            crosses = [chip_cross(ch) for ch in dead]
            dc = T("don’t care", 36, GOLD).next_to(VGroup(*dead), DOWN, buff=0.35)
            self.play(*appear(*crosses, shift=0.15 * DOWN, lag=0.2), *during(appear(dc), 0.4, 1), run_time=1.4)
            km = kmap_outline().move_to(_p(3.7, -0.7))
            c.wait_until("K-maps")
            self.play(*appear(km.title, km[1], km[2], km[3], lag=0.15), run_time=1.0)
            kx = [cross_mark(color=GOLD, r=0.19).set_stroke(width=6).move_to(km.cells[1][k]) for k in (3, 2)]   # 110, 111
            self.play(*[ReplacementTransform(x, k, path_arc=-0.6) for x, k in zip(crosses, kx)],
                      run_time=min(1.6, c.until("lecturer")))
            c.wait_until("freedom")
            free = T("more freedom to assign the codes", 32, YELLOW).move_to(_p(-2.9, -3.1))
            self.play(*appear(free), run_time=1.0)

    # -- 'may': only across a power of two ------------------------------------------------------
    def clip4(self):
        with self.say("c1.why.4") as c:
            mays = [select(self.b2[0], "may")[0], select(self.b2[1], "may")[0]]
            c.wait_until("word may")
            self.play(*recolor(mays[0], YELLOW), FlashAround(mays[0], color=YELLOW, run_time=1.2), run_time=1.2)
            c.wait_until("twice")
            self.play(*recolor(mays[1], YELLOW), FlashAround(mays[1], color=YELLOW, run_time=1.2), run_time=1.2)

            c.wait_until("cross")
            lad = ladder()
            lad.move_to(_p(0, -0.62)).align_to(_p(-6.6, 0), LEFT)
            b15 = ladder_bracket(lad, 3, 15)
            sweep_clear(self, FadeIn(lad), FadeIn(b15), keep=[self.b2], run_time=1.4)   # early: the ladder returns whole, as in clip 2
            y = (lad.rows[2].get_bottom()[1] + lad.rows[3].get_top()[1]) / 2
            line = Line(_p(lad.get_left()[0] - 0.1, y), _p(b15.get_left()[0] - 0.1, y)).set_stroke(YELLOW, 5)
            pw = T("a power of two", 32, YELLOW).next_to(lad.pats[2], RIGHT, buff=0.4)
            c.wait_until("power of two")
            self.play(GrowFromCenter(line), *during(appear(pw), 0.3, 1), run_time=1.2)

            c.wait_until("nine")
            b9 = ladder_bracket(lad, 3, 9)   # same brace on row 4: 15 is rewritten to 9, "= 4" stays put
            self.play(*edit(b15.tag, b9.tag), *edit(b15.formula, b9.formula),
                      run_time=1.5)
            st4 = T("still 4", 32, YELLOW).next_to(b9.formula, DOWN, buff=0.2).align_to(b9.formula, LEFT)
            c.wait_until("still need")
            self.play(*appear(st4), run_time=0.9)

            c.wait_until("Part three")
            later = T("Part 3: 8 states → 6, still 3 flip-flops", 30, DIM).move_to(_p(-2.2, -3.25))
            self.play(*appear(later, shift=None), run_time=1.0)
        self.wait(2.0)
