"""Chapter 1, scene 4: what makes a good assignment? (p. 132's optimisation tree: complexity,
technology, area, wiring, speed; algorithms exist), then the one fixed thing: the doubling ladder and
the minimum ceil(log2 m) flip-flops; more than the minimum is allowed. Clips c1.choice.1 – c1.choice.4.

Chapter-wide helper owned here (s8 shows it small as recap slot r2):
- doubling_ladder(label_size=34, pat_size=28, with_formula=False) -> VGroup centred on ORIGIN.
  Four rows "1 flip-flop: 2 patterns", "2: 4", "3: 8", "4: 16" (counts GOLD), each with its bit
  patterns in GREEN Mono beside it (0 1 / 00 01 10 11 / 2 x 4 block / 4 x 4 block). About 10.3 x 4.4.
  Attributes: .rows[i] (VGroup lab, cnt, pats), .labs, .counts, .pats; with_formula=True adds
  .formula (ceil_log2(), YELLOW brackets) to the right of the rows, the whole group re-centred.
- ceil_log2(size=110, bracket_color=YELLOW) -> MathTex "\\lceil \\log_2 m \\rceil"; [0], [2] brackets.
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


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the doubling ladder (chapter-wide: s8 recap r2) ---------------------------------------------
PATTERNS = [
    ["0 1"],
    ["00 01 10 11"],
    ["000 001 010 011", "100 101 110 111"],
    ["0000 0001 0010 0011", "0100 0101 0110 0111", "1000 1001 1010 1011", "1100 1101 1110 1111"],
]


def ceil_log2(size=110, bracket_color=YELLOW):
    m = MathTex(r"\lceil", r"\log_2 m", r"\rceil", font_size=size, color=FG)
    m[0].set_color(bracket_color)
    m[2].set_color(bracket_color)
    return m


def doubling_ladder(label_size=34, pat_size=28, with_formula=False):
    labs = [T("1 flip-flop:", label_size)] + [T(f"{n}:", label_size) for n in (2, 3, 4)]
    counts = [T("2 patterns", label_size, GOLD)] + [T(str(c), label_size, GOLD) for c in (4, 8, 16)]
    pats = []
    for lines in PATTERNS:
        blk = VGroup(*[Mono(s, pat_size, GREEN) for s in lines]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        pats.append(blk)
    cnt_l = 0.25
    pat_l = cnt_l + max(c.width for c in counts) + 0.6
    rows = []
    y = 0.0
    for i in range(4):
        h = max(pats[i].height, labs[i].height)
        cy = y - h / 2
        pats[i].move_to(_p(0, cy)).align_to(_p(pat_l, 0), LEFT)
        labs[i].move_to(_p(0, cy)).align_to(_p(0, 0), RIGHT)
        counts[i].move_to(_p(0, cy)).align_to(_p(cnt_l, 0), LEFT)
        rows.append(VGroup(labs[i], counts[i], pats[i]))
        y -= h + 0.45
    lad = VGroup(*rows)
    lad.rows, lad.labs, lad.counts, lad.pats = rows, labs, counts, pats
    if with_formula:
        f = ceil_log2()
        f.next_to(VGroup(*rows), RIGHT, buff=1.0)
        lad.add(f)
        lad.formula = f
    lad.move_to(ORIGIN)
    return lad


# ---- small drawings ------------------------------------------------------------------------------
def nand(center=ORIGIN, w=0.5, h=0.42, color=BLUE, width=3):
    g = VGroup(
        Line(_p(-w / 2, h / 2), _p(0, h / 2)),
        Line(_p(-w / 2, -h / 2), _p(0, -h / 2)),
        Line(_p(-w / 2, h / 2), _p(-w / 2, -h / 2)),
        Arc(radius=h / 2, start_angle=PI / 2, angle=-PI),
        Circle(radius=0.055).move_to(_p(h / 2 + 0.055, 0)),
    ).set_stroke(color, width)
    g.shift(center)
    g.out_pt = lambda: g[4].get_right()
    g.in_pt = lambda k: g[2].get_center() + UP * (h / 4) * (1 if k == 0 else -1)
    return g


def ff_gates():
    """A master-slave D flip-flop at gate level, small: 8 NAND gates in four columns."""
    xs, ys = [-1.5, -0.5, 0.5, 1.5], [0.42, -0.42]
    gates = [[nand(_p(x, y)) for y in ys] for x in xs]
    wires = VGroup()

    def wire(pts):
        wires.add(VMobject().set_points_as_corners(pts))

    for c in range(3):
        for r in range(2):
            a = gates[c][r].out_pt()
            b = gates[c + 1][r].in_pt(0 if r == 0 else 1)
            mx = (a[0] + b[0]) / 2
            wire([a, _p(mx, a[1]), _p(mx, b[1]), b])
    for c in (1, 3):   # cross-coupled pairs
        top, bot = gates[c]
        a, b = top.out_pt(), bot.in_pt(0)
        wire([a, a + RIGHT * 0.12, b + LEFT * 0.12 + DOWN * 0.0, b])
        a, b = bot.out_pt(), top.in_pt(1)
        wire([a, a + RIGHT * 0.12, b + LEFT * 0.12, b])
    for r in range(2):
        for k in range(2):
            p = gates[0][r].in_pt(k)
            wire([p + LEFT * 0.35, p])
    wires.set_stroke(FG, 2)
    g = VGroup(wires, *[gt for col in gates for gt in col])
    return g


def tangle():
    """Six small gates and a tangle of YELLOW wires between them."""
    left = [nand(_p(-1.4, y), w=0.42, h=0.34) for y in (0.55, 0, -0.55)]
    right = [nand(_p(1.4, y), w=0.42, h=0.34) for y in (0.55, 0, -0.55)]
    pairs = [(0, 2, 1), (0, 1, 0), (1, 0, 0), (1, 2, 0), (2, 0, 1), (2, 1, 1), (1, 1, 1), (2, 2, 1),
             (0, 0, 1)]
    wires = VGroup()
    for i, j, k in pairs:
        a, b = left[i].out_pt(), right[j].in_pt(k)
        wires.add(CubicBezier(a, a + RIGHT * 1.2 + UP * 0.25 * (j - i), b + LEFT * 1.2 + DOWN * 0.3 * (i - j), b))
    wires.set_stroke(YELLOW, 2.5)
    g = VGroup(VGroup(*left, *right), wires)
    g.gates, g.wires = g[0], wires
    return g


def fpga_icon():
    body = Square(1.3).set_stroke(BLUE, 3).set_fill(BG, 1)
    grid = VGroup(*[Square(0.22).move_to(_p(-0.42 + 0.28 * i, -0.42 + 0.28 * j))
                    for i in range(4) for j in range(4)]).set_stroke(BLUE, 1.5).set_fill(BLUE, 0.25)
    pins = VGroup()
    for k in range(5):
        t = -0.5 + 0.25 * k
        for a, b in ((_p(t, 0.65), _p(t, 0.85)), (_p(t, -0.65), _p(t, -0.85)),
                     (_p(0.65, t), _p(0.85, t)), (_p(-0.65, t), _p(-0.85, t))):
            pins.add(Line(a, b))
    pins.set_stroke(DIM, 3)
    return VGroup(pins, body, grid)


def dip_icon():
    body = Rectangle(width=2.0, height=0.8).set_stroke(BLUE, 3).set_fill(BG, 1)
    notch = Arc(radius=0.12, start_angle=-PI / 2, angle=PI).move_to(body.get_left() + RIGHT * 0.06)
    notch.set_stroke(BLUE, 3)
    pins = VGroup()
    for k in range(7):
        x = -0.78 + 0.26 * k
        pins.add(Line(_p(x, 0.4), _p(x, 0.62)), Line(_p(x, -0.4), _p(x, -0.62)))
    pins.set_stroke(DIM, 5)
    return VGroup(pins, body, notch)


def branch(src, dst):
    a = src.get_bottom() + DOWN * 0.12
    b = dst.get_top() + UP * 0.12
    return Arrow(a, b, buff=0, stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.08)


def row_brace(row, x):
    c = row.get_y()
    h = 0.9
    return Brace(Line(_p(x, c + h / 2), _p(x, c - h / 2)), direction=RIGHT, buff=0.1, color=GOLD)


class Choice(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- what makes a good assignment? -------------------------------------------------------------
    def clip1(self):
        with self.say("c1.choice.1") as c:
            head = T("State Assignment", 52)
            q = T("?", 60, YELLOW)
            VGroup(head, q).arrange(RIGHT, buff=0.25).move_to(_p(0, 3.2))
            self.play(*appear(head, q, lag=0.4), run_time=1.2)
            self.head, self.q = head, q
            c.wait_until("depends")
            quote = T("As we have mentioned previously, state assignment is\n"
                      "not necessarily obvious or straightforward", 30, line_spacing=0.9)
            quote.move_to(_p(0, 2.05))
            self.play(*appear(quote), run_time=1.0)
            c.wait_until("depends on")
            dep = T("Depends what we are trying to optimise, e.g.,", 34)
            dep.move_to(_p(0, 0.85))
            self.play(*appear(dep), run_time=1.0)
            c.wait_until("complexity")
            opt = select(dep, "optimise")[0]
            cx = T("Complexity", 40, BLUE).move_to(_p(-3.0, -0.85))
            a1 = branch(opt, cx)
            self.play(GrowArrow(a1), *during(appear(cx), 0.4, 1), run_time=1.5)
            c.wait_until("FPGA")
            fp = fpga_icon().move_to(_p(-4.7, -1.95))
            fpl = T("FPGA", 30).next_to(fp, DOWN, buff=0.15)
            self.play(FadeIn(fp, shift=0.2 * DOWN), *during(appear(fpl), 0.3, 1), run_time=1.2)
            c.wait_until("series")
            dp = dip_icon().move_to(_p(-1.4, -1.95))
            dpl = T("74 series logic chips", 30).next_to(dp, DOWN, buff=0.3).set_y(fpl.get_y())
            self.play(FadeIn(dp, shift=0.2 * DOWN), *during(appear(dpl), 0.3, 1), run_time=1.2)
            self.quote, self.dep, self.cx, self.a1 = quote, dep, cx, a1
            self.icons = [fp, fpl, dp, dpl]

    def clip2(self):
        with self.say("c1.choice.2") as c:
            up = 2.4 * UP
            area = T("FF implementation may take less chip area\n"
                     "than you may think given their\n"
                     "gate level representation", 30, line_spacing=0.9)
            area.move_to(_p(0, 0.35)).align_to(_p(-6.3, 0), LEFT)
            gone = [self.head, self.q, self.quote, *self.icons]
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during([m.animate.shift(up) for m in (self.dep, self.cx, self.a1)], 0.25, 0.75),
                      *during(appear(area), 0.6, 1), run_time=min(1.8, c.until("drawing")))
            ffd = ff_gates().move_to(_p(3.6, 0.35))
            self.play(FadeIn(ffd), run_time=min(0.9, c.until("suggests")))
            c.wait_until("suggests")
            box = Square(0.7).set_stroke(BLUE, 3).move_to(ffd)
            ffl = T("FF", 28, BLUE).move_to(box)
            self.play(ReplacementTransform(ffd, box), *during(appear(ffl, shift=None), 0.6, 1),
                      run_time=min(1.6, c.until("wiring")))
            c.wait_until("wiring")
            wtx = T("Wiring complexity can be as big an issue\nas gate complexity", 30, line_spacing=0.9)
            wtx.move_to(_p(0, -1.25)).align_to(area, LEFT)
            tg = tangle().move_to(_p(3.6, -1.25))
            self.play(*appear(wtx), FadeIn(tg.gates), run_time=1.0)
            self.play(*[Create(w) for w in tg.wires], run_time=min(1.6, c.until("speed")))
            c.wait_until("speed")
            sp = T("Speed", 40, BLUE).move_to(_p(3.6, self.cx.get_y()))
            opt = select(self.dep, "optimise")[0]
            a2 = branch(opt, sp)
            dimmed = [area, box, ffl, wtx, tg]
            self.play(GrowArrow(a2), *during(appear(sp), 0.4, 1), *set_alpha(dimmed, 0.4), run_time=1.5)
            c.wait_until("algorithms")
            alg = T("Algorithms do exist for selecting the ‘optimising’ state assignment,\n"
                    "but are not suitable for manual execution", 30, line_spacing=0.9)
            alg.move_to(_p(0, -2.85))
            self.play(*appear(alg), run_time=1.0)
            self.alg = alg
            c.wait_until("far too heavy")
            hot = select(alg, "not suitable for manual execution")[0]
            self.play(*recolor(hot, YELLOW), FlashUnder(hot, run_time=1.5, time_width=1.5), run_time=1.5)

    # -- the fixed thing: the minimum ---------------------------------------------------------------
    def clip3(self):
        with self.say("c1.choice.3") as c:
            head = T("The minimum number of flip-flops", 44).move_to(_p(0, 3.3))
            sweep_clear(self, time_span(FadeIn(head, shift=0.2 * DOWN), 0.6, 1.2), run_time=1.2)
            lad = doubling_ladder().move_to(_p(-1.0, -0.4))
            self.lad, self.head2 = lad, head
            cues = [None, "two give four", "three give eight", "four give sixteen"]
            c.wait_until("ladder")
            for i, row in enumerate(lad.rows):
                if cues[i]:
                    c.wait_until(cues[i])
                self.play(*appear(*row, lag=0.3), run_time=1.2 if i == 0 else 0.9)
            bx = lad.pats[2].get_right()[0] + 0.25
            c.wait_until("eight")
            br = row_brace(lad.rows[2], bx)
            tag = T("8 states", 34, GOLD).next_to(br, RIGHT, buff=0.15)
            self.play(GrowFromCenter(br), *during(appear(tag), 0.3, 1), run_time=1.2)
            c.wait_until("five")
            tag5 = T("5 states", 34, GOLD).move_to(tag)   # five states also need three: brace stays on row 3
            self.play(*swap(tag, tag5), run_time=1.2)
            c.wait_until("since")
            lt = T("4 patterns < 5 states", 32, RED).next_to(lad.pats[1], RIGHT, buff=0.5)
            if lt.get_right()[0] > 6.55:
                lt.shift((6.55 - lt.get_right()[0]) * RIGHT)
            self.play(FlashAround(lad.rows[1], color=RED, run_time=1.4, time_width=1.5),
                      *recolor(lad.counts[1], RED), *during(appear(lt), 0.3, 1), run_time=1.4)
            c.wait_until("threestates")
            d = row_brace(lad.rows[1], bx).get_center() - br.get_center()
            self.play(*during(disappear(lt), 0, 0.4), *during([br.animate.shift(d), tag5.animate.shift(d)], 0.4, 1),
                      *recolor(lad.counts[1], GOLD), run_time=min(1.0, c.until("formula", floor=0.6)))   # brace and label travel together
            tag3 = T("3 states", 34, GOLD).move_to(tag5)
            self.play(*swap(tag5, tag3), run_time=min(0.8, c.until("formula")))
            c.wait_until("formula")
            l1 = T("If we have m states, we need", 30)
            l2 = VGroup(T("at least", 30), MathTex(r"\log_2 m", font_size=40), T("FFs", 30))
            l2.arrange(RIGHT, buff=0.16)
            l2[1].align_to(l2[0], DOWN).shift(0.1 * DOWN)
            l3 = T("(or more informally, bits)", 30)
            l4 = T("to encode the states", 30)
            ftx = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            ftx.move_to(_p(3.8, 1.35))
            moves = []
            for i in range(4):
                y = 1.2 - 1.0 * i
                lab, cnt = lad.labs[i], lad.counts[i]
                moves.append(lab.animate.align_to(_p(-3.4, 0), RIGHT).set_y(y))
                moves.append(cnt.animate.align_to(_p(-3.15, 0), LEFT).set_y(y))
            self.play(*during(disappear(br, tag3, *lad.pats), 0, 0.3), *during(moves, 0.2, 0.65),
                      *during(appear(*ftx, lag=0.2), 0.6, 1), run_time=1.8)
            c.wait_until("log base two")
            ce = ceil_log2(110, bracket_color=FG).move_to(_p(3.8, -1.05))
            self.play(*appear(ce), run_time=0.9)
            c.wait_until("rounded up")
            ru = T("rounded up", 32, YELLOW).next_to(ce, DOWN, buff=0.3)
            self.play(*recolor([ce[0], ce[2]], YELLOW), *flash([ce[0], ce[2]]),
                      *during(appear(ru), 0.3, 1), run_time=min(1.2, c.until(floor=0.6)))
            self.ftx, self.ce, self.ru = ftx, ce, ru

    def clip4(self):
        with self.say("c1.choice.4", gap=1.2) as c:
            more = T("More than the minimum: allowed", 44, GREEN).move_to(self.head2)
            self.play(*swap(self.head2, more), *during(disappear(*self.lad.labs, *self.lad.counts,
                                       *self.ftx, self.ce, self.ru), 0, 0.5), run_time=1.3)
            c.wait_until("traffic light")
            ring = load_scene("ch1_s1_hook").traffic_ring(["100", "110", "001", "010"], code_size=50)
            ring.scale(0.6).move_to(_p(-3.5, 0.15))
            self.play(FadeIn(ring), run_time=1.0)
            c.wait_until("three flip-flops")
            tl = T("3 flip-flops for 4 states\n(minimum 2)", 30, line_spacing=0.9).move_to(_p(-3.5, -2.35))
            self.play(*appear(tl), run_time=1.0)
            c.wait_until("today")
            today = T("… some using more FFs\nthan the minimum", 34, line_spacing=0.9)
            today.move_to(_p(3.6, 1.2))
            self.play(*appear(today), run_time=1.2)
            c.wait_until("fun")
            fun = T("“just a bit of fun, just to show\nyou how creative you can be”", 32, YELLOW,
                    slant=ITALIC, line_spacing=0.9)
            fun.move_to(_p(3.6, -0.9))
            self.play(*appear(fun), run_time=1.2)
