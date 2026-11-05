"""Chapter 6, scene 8: recap in six panels, the lecture's road, and Lecture 11's silhouette. Clips c6.recap.1 – c6.recap.3.

Grid as ch2_s8_recap / ch5_s8_recap: "Recap" T 40 at (0, 3.4), six faint DIM slot frames (ch2's 3 x 2 grid),
each panel's picture fitted in the slot, its line (T 28) under it, earlier panels veiled.
 r1 s2's onehot_diagram("top") over onehot_ffs() (arc labels dropped); r2 s2's onehot_table row 4
 (010 | 11 | 100) with its heads, s3's full term, s2-bar and s0-bar struck, edited to s1.e.r;
 r3 s4's check_table + rule_line(words=False); r4 s5's final_line over truth_table;
 r5 s6's arcs_diagram, the three arcs into Sync lit at the cue; r6 s7's panels() (no caption), GOLD line.
{lecture}: tiles shrink away, s7's final_board() centred. {road}: the board shrinks to the top; the road
"binary count -> sliding -> ring -> one-hot" builds below it (names lit YELLOW on the board as each lands),
thumbnails ch2_s1 binary_circuit, ch2_s4 sliding_circuit, ch2_s5 ring_circle, s2's onehot_ffs.
Clip 3: p. 144's headings, a generic five-circle diagram (two circles with identical arcs into B pulse),
they merge; three flip-flops -> two, ceil(log2 5) = 3 -> ceil(log2 4) = 2 (GOLD); or (DIM) DIM X's in a K-map outline.
End card (Lecture 11 opens on it): end_card() = the headings + the merged picture; handover_shot() returns it.
"""
# style: 2
# handover: next
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

G2 = load_scene("ch2_s8_recap")          # slot_frame, caption, veil, vis_center, VIS_W/H
H21 = load_scene("ch2_s1_hook")          # binary_circuit
H24 = load_scene("ch2_s4_slidecircuit")  # sliding_circuit
H25 = load_scene("ch2_s5_ring")          # ring_circle
NL = load_scene("ch2_s6_nologic")        # make_ff
S2 = load_scene("ch6_s2_codes")
S3 = load_scene("ch6_s3_inspect")
S4 = load_scene("ch6_s4_onehot_rule")
S5 = load_scene("ch6_s5_d0")
S6 = load_scene("ch6_s6_arcs")
S7 = load_scene("ch6_s7_verdict")
veil = G2.veil


def _p(x, y):
    return np.array([x, y, 0.0])


def fit_slot(m, i, w=G2.VIS_W, h=G2.VIS_H, dy=0.0):
    return G2.fit(m, G2.vis_center(i) + dy * UP, w, h)


# =============================================================================================
# panel pictures (native, fitted by the scene)
# =============================================================================================
def p1_onehot():
    d = S2.onehot_diagram("top")
    d.remove(*d.labels)
    d.scale(0.9).move_to(_p(0, 0.0))
    ff = S2.onehot_ffs(xs=(-3.0, 0.0, 3.0))
    ff.next_to(d, DOWN, buff=0.25).set_x(0)
    g = VGroup(d, ff)
    g.d, g.ff = d, ff
    return g


R2_XS = ((0.0, 0.62, 1.24), (2.14, 2.76), (3.66, 4.28, 4.9))
R2_HEADS = (("s_2", "s_1", "s_0"), ("e", "r"), ("s_2'", "s_1'", "s_0'"))
R2_ROW = ("010", "11", "100")


def p2_row():
    cols = (GREEN, BLUE, GREEN)
    heads = VGroup(*[VGroup(*[MathTex(h, font_size=40, color=col).move_to(_p(x, 0.62)) for h, x in zip(hs, xs)])
                     for hs, xs, col in zip(R2_HEADS, R2_XS, cols)])
    row = VGroup(*[VGroup(*[MathTex(ch, font_size=40, color=GOLD if (g == 0 and ch == "1") else FG).move_to(_p(x, 0))
                            for ch, x in zip(s, xs)])
                   for g, (s, xs) in enumerate(zip(R2_ROW, R2_XS))])
    top, bot = 1.0, -0.32
    seps = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in (1.69, 3.21)])
    rule = Line(_p(-0.3, 0.32), _p(5.2, 0.32)).set_stroke(DIM, 2)
    full = S3.eq_line(None, S3.FULL, size=48, tags=False)
    full.tex.move_to(_p(2.45, -1.0))
    g = VGroup(heads, row, seps, rule, full.tex)
    g.heads, g.row, g.full = heads, row, full
    return g


def p3_check():
    ct = S4.check_table()
    rl = S4.rule_line(size=48, words=False)
    rl.next_to(ct, DOWN, buff=0.45)
    g = VGroup(ct, rl)
    g.ct, g.rl = ct, rl
    return g


def p4_d0():
    fl = S5.final_line()
    tt = S5.truth_table()
    tt.scale(0.5).next_to(fl, DOWN, buff=0.4)
    g = VGroup(fl, tt)
    g.fl, g.tt = fl, tt
    return g


def p5_arcs(lit=False):
    d = S6.sync_arcs_shot() if lit else S6.arcs_diagram()
    d.remove(*d.labels)
    return d


def p6_panels():
    P = S7.panels()
    P.remove(P.caption)
    return P


# =============================================================================================
# the road
# =============================================================================================
BOARD_C = _p(0, 0.5)
BOARD_K = 0.66
BOARD_TOP = 3.48
ROAD_XS = (-5.1, -1.7, 1.7, 5.1)
ROAD_LY = -1.35
THUMB_Y, THUMB_W, THUMB_H = -2.65, 3.2, 1.7
ROAD_NAMES = ("binary count", "sliding", "ring", "one-hot")


def road_thumbs():
    b = H21.binary_circuit()
    s = H24.sliding_circuit()
    r = H25.ring_circle(center=ORIGIN, bits="11000")
    o = S2.onehot_ffs()
    out = []
    for m, x in zip((b, s, r, o), ROAD_XS):
        G2.fit(m, _p(x, THUMB_Y), THUMB_W, THUMB_H)
        out.append(m)
    return out


def road_labels():
    labs = [T(n, 34).move_to(_p(x, ROAD_LY)) for n, x in zip(ROAD_NAMES, ROAD_XS)]
    for lab in labs:   # one baseline: every name's first letter (b, s, r, o) sits on it
        lab.shift((ROAD_LY - 0.16 - lab[0].get_bottom()[1]) * UP)
    arrows = [Arrow(a.get_right() + 0.15 * RIGHT, b.get_left() + 0.15 * LEFT, buff=0, stroke_width=3,
                    color=DIM, max_tip_length_to_length_ratio=0.25, tip_length=0.18)
              for a, b in zip(labs, labs[1:])]
    return labs, arrows


# =============================================================================================
# Lecture 11's silhouette and the end card
# =============================================================================================
NODE_R = 0.45
POS = {"A": _p(-5.4, -0.05), "B": _p(-3.55, -0.05), "C": _p(-1.7, -0.05),
       "D": _p(-4.5, -2.45), "E": _p(-2.6, -2.45), "M": _p(-3.55, -2.45)}
FF_Y = 0.3
FF_XS3 = (1.35, 3.05, 4.75)
FF_XS2 = (2.2, 3.9)
FF_K = 0.45
LOG_C = _p(3.05, -1.05)
OR_C = _p(3.05, -1.72)
KMAP_C = _p(3.05, -2.78)
KMAP_CELL = 0.36
X_CELLS = ((0, 3), (2, 1), (3, 2), (1, 0))


def headings():
    nxt = T("Next lecture", 30, DIM).move_to(_p(0, 3.5))
    h1 = T("Digital Electronics: Sequential Logic", 34).move_to(_p(0, 2.95))
    h2 = T("Further Considerations", 48).move_to(_p(0, 2.3))
    h3 = T("Elimination of Redundant States", 36, YELLOW).move_to(_p(0, 1.55))
    g = VGroup(nxt, h1, h2, h3)
    g.nxt, g.h1, g.h2, g.h3 = nxt, h1, h2, h3
    return g


def node(name, color=BLUE):
    return Circle(radius=NODE_R).set_stroke(color, 4).set_fill(BG, 1).move_to(POS[name])


def arc(a, b, color=FG, angle=0.0):
    pa, pb = POS[a], POS[b]
    u = (pb - pa) / np.linalg.norm(pb - pa)
    if angle:
        return CurvedArrow(pa + NODE_R * _rot(u, angle / 2), pb - NODE_R * _rot(u, -angle / 2), angle=angle,
                           color=color, stroke_width=3, tip_length=0.2)
    return Arrow(pa + NODE_R * u, pb - NODE_R * u, buff=0.05, stroke_width=3, color=color,
                 max_tip_length_to_length_ratio=0.2, tip_length=0.2)


def _rot(u, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * u[0] - s * u[1], s * u[0] + c * u[1], 0.0])


def five_diagram():
    nodes = {n: node(n) for n in "ABCDE"}
    arcs = {"AB": arc("A", "B"), "BC": arc("B", "C"),
            "AD": arc("A", "D"), "CE": arc("C", "E"), "DB": arc("D", "B"), "EB": arc("E", "B")}
    g = VGroup(*arcs.values(), *nodes.values())
    g.nodes, g.arcs = nodes, arcs
    return g


def four_diagram():
    nodes = {n: node(n) for n in "ABC"}
    nodes["M"] = node("M", YELLOW)
    arcs = {"AB": arc("A", "B"), "BC": arc("B", "C"),
            "AM": arc("A", "M"), "CM": arc("C", "M"), "MB": arc("M", "B", YELLOW)}
    g = VGroup(*arcs.values(), *nodes.values())
    g.nodes, g.arcs = nodes, arcs
    return g


def ff_box(x):
    f = NL.make_ff(ORIGIN, size=52)
    f.remove(f.clk_w, f.qb_w, f.qb_l)
    f.tri.scale(1.8, about_point=f.tri.get_bottom()).set_stroke(FG, 4)
    f.scale(FF_K, about_point=ORIGIN).shift(_p(x, FF_Y))
    return f


def ff_boxes(xs):
    return VGroup(*[ff_box(x) for x in xs])


def log_line(n):
    k = {5: 3, 4: 2}[n]
    return MathTex(r"\lceil \log_2 " + str(n) + r" \rceil = " + str(k), font_size=48, color=GOLD).move_to(LOG_C)


def kmap_box():
    c, s = KMAP_C, KMAP_CELL
    W = 4 * s
    L, top = c[0] - W / 2, c[1] + W / 2
    grid = VGroup(Square(side_length=W).move_to(c),
                  *[Line(_p(L + k * s, top), _p(L + k * s, top - W)) for k in (1, 2, 3)],
                  *[Line(_p(L, top - k * s), _p(L + W, top - k * s)) for k in (1, 2, 3)]).set_stroke(DIM, 2)
    xs = VGroup(*[MathTex("X", font_size=30, color=DIM).move_to(_p(L + (k + 0.5) * s, top - (r + 0.5) * s))
                  for r, k in X_CELLS])
    g = VGroup(grid, xs)
    g.grid, g.xs = grid, xs
    return g


def or_word():
    return T("or", 30, DIM, slant=ITALIC).move_to(OR_C)


def end_card():
    h = headings()
    d = four_diagram()
    ff = ff_boxes(FF_XS2)
    lg = log_line(4)
    orw = or_word()
    km = kmap_box()
    g = VGroup(h, d, ff, lg, orw, km)
    g.heads, g.diagram, g.ffs, g.log, g.orw, g.kmap = h, d, ff, lg, orw, km
    return g


def handover_shot():
    return end_card()


# =============================================================================================
class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.end()

    def dim_previous(self):
        out = []
        for t in self.panels:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    def show_panel(self, pic, cap, c, cue, rt=1.0):
        c.wait_until(cue)
        self.play(*self.dim_previous(), FadeIn(pic), *appear(cap, shift=None), run_time=rt)  # early: panel shown whole

    # -- c6.recap.1 ---------------------------------------------------------------------------------
    def clip1(self):
        with self.say("c6.recap.1") as c:
            head = T("Recap", 40).move_to(_p(0, 3.4))
            frames = [G2.slot_frame(i) for i in range(6)]
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames],  # early: the scene's heading
                      run_time=min(1.2, c.until("r1")))

            # r1: one flip-flop per state
            p1 = p1_onehot()
            fit_slot(p1, 0)
            cap1 = G2.caption(0, ["one flip-flop per state"])
            self.show_panel(p1, cap1, c, "r1")
            c.wait_until("own flip-flop")
            self.play(*flash(list(p1.d.one.values()), color=GOLD, time_width=1.5),
                      *flash([f.box for f in p1.ff.ffs], color=YELLOW, time_width=1.5),
                      run_time=min(1.5, c.until("r2", floor=0.8)))
            self.panels.append(VGroup(p1, cap1))

            # r2: the row, the full term; the cold flip-flops struck out
            p2 = p2_row()
            k = fit_slot(p2, 1)
            cap2 = G2.caption(1, ["name only the hot flip-flop"])
            self.show_panel(p2, cap2, c, "r2")
            c.wait_until("just that flip-flop")
            fp = p2.full.pieces
            strikes = [Line(m.get_corner(DL) + 0.03 * DL, m.get_corner(UR) + 0.03 * UR).set_stroke(RED, 3)
                       for m in (fp[0], fp[4])]
            self.play(*[Create(s) for s in strikes], *recolor([fp[0], fp[4]], DIM),
                      run_time=min(1.0, c.until("and the inputs")))
            c.wait_until("and the inputs")
            res = S3.eq_line(None, ["s_1", "e", "r"], size=48, tags=False)
            res.tex.scale(k).move_to(p2.full.tex)
            self.play(*during(disappear(*strikes), 0, 0.4), *edit(p2.full.tex, res.tex),
                      run_time=min(1.5, c.until("r3", floor=0.8)))
            p2.remove(p2.full.tex)
            p2.add(res.tex)
            self.panels.append(VGroup(p2, cap2))

            # r3: in the used states, s0-bar = s1 + s2
            p3 = p3_check()
            fit_slot(p3, 2)
            cap3 = G2.caption(2, ["in used states"])
            self.show_panel(p3, cap3, c, "r3")
            c.wait_until("same as")
            self.play(FlashAround(p3.rl, time_width=1.5),
                      *flash([r.mark for r in p3.ct.rows[:3]], color=GREEN, time_width=1.5),
                      run_time=min(1.5, c.until("r4", floor=0.8)))
            self.panels.append(VGroup(p3, cap3))

            # r4: D0 = r-bar (s0 + e)
            p4 = p4_d0()
            fit_slot(p4, 3)
            cap4 = G2.caption(3, ["distributive law"])
            self.show_panel(p4, cap4, c, "r4")
            c.wait_until("shrinks")
            self.play(FlashAround(p4.fl, time_width=1.5), run_time=min(1.5, c.until("r5", floor=0.8)))
            self.panels.append(VGroup(p4, cap4))

            # r5: OR the incoming arcs
            p5 = p5_arcs()
            lit = p5_arcs(lit=True)
            fit_slot(p5, 4)
            fit_slot(lit, 4)
            cap5 = G2.caption(4, ["OR the incoming arcs"])
            self.show_panel(p5, cap5, c, "r5")
            c.wait_until("arcs coming into")
            into = S6.INTO["Sync"]
            self.play(*[Transform(p5.arcs[i], lit.arcs[i]) for i in into],
                      Transform(p5.circle["Sync"], lit.circle["Sync"]),
                      *[VShowPassingFlash(lit.arcs[i].copy().set_stroke(YELLOW, 5), time_width=0.6) for i in into],
                      run_time=min(1.5, c.until("r6", floor=0.8)))
            self.panels.append(VGroup(p5, cap5))

            # r6: the price
            p6 = p6_panels()
            fit_slot(p6, 5)
            cap6 = G2.caption(5, ["+1 flip-flop, +1 gate"], color=GOLD)
            self.show_panel(p6, cap6, c, "r6")
            c.wait_until("one more gate")
            self.play(FlashUnder(cap6, color=GOLD, time_width=1.5), run_time=min(1.2, c.until(floor=0.6)))
            self.panels.append(VGroup(p6, cap6))

    # -- c6.recap.2: the lecture's road -----------------------------------------------------------------
    def clip2(self):
        board = self.board = S7.final_board()
        board.move_to(BOARD_C)
        with self.say("c6.recap.2") as c:
            olds = list(self.mobjects)
            # strictly one after the other: the old grid is gone before the board's text starts to show
            self.play(*during([FadeOut(m, scale=0.5) for m in olds], 0, 0.4),  # early: s7's scoreboard returns whole
                      *during([FadeIn(board)], 0.55, 1.0), run_time=min(2.0, c.until("road")))
            c.wait_until("road")
            board.generate_target()
            board.target.scale(BOARD_K)
            board.target.move_to(_p(0, BOARD_TOP - board.target.height / 2))
            self.play(MoveToTarget(board), run_time=min(1.5, c.until("binary count")))
            labs, arrows = road_labels()
            thumbs = road_thumbs()
            # only the names that feed the road light: binary, sliding, ring, then both one-hot rows
            # (traffic light's and the synchroniser's); Lecture 9 and sequential stay as they are
            names = [[board.rows[0][0]], [board.rows[1][0]], [board.rows[2][0]],
                     [r[0] for r in board.rows if r[0].text == "one-hot"]]
            cues = ("binary count", "sliding codes", "the ring", "one-hot codes")
            for k, cue in enumerate(cues):
                c.wait_until(cue)
                nxt = c.until(cues[k + 1]) if k < 3 else c.until(floor=0.8)
                extra = [GrowArrow(arrows[k - 1])] if k else []
                self.play(*recolor(names[k], YELLOW), *extra, *appear(labs[k]),
                          FadeIn(thumbs[k]), run_time=min(1.2, nxt))

    # -- c6.recap.3: next lecture -------------------------------------------------------------------------
    def clip3(self):
        h = headings()
        d5 = five_diagram()
        d4 = four_diagram()
        ff3 = ff_boxes(FF_XS3)
        log5 = log_line(5)
        km = kmap_box()
        orw = or_word()
        with self.say("c6.recap.3") as c:
            sweep_clear(self, *appear(h.nxt, h.h1, shift=None, lag=0.2), run_time=min(1.6, c.until("further considerations")))  # early: the slide's heading
            c.wait_until("further considerations")
            self.play(*appear(h.h2), run_time=min(1.0, c.until("redundant")))
            c.wait_until("redundant")
            self.play(*appear(h.h3, shift=None), FadeIn(d5),  # early: p. 144's heading with its picture
                      run_time=min(1.2, c.until("more states")))
            c.wait_until("more states")
            pair = [d5.nodes["D"], d5.nodes["E"]]
            twins = [d5.arcs["DB"], d5.arcs["EB"]]
            self.play(*[n.animate.set_stroke(YELLOW, 6) for n in pair], *recolor(twins, YELLOW),
                      *flash(pair, time_width=1.5), run_time=min(1.4, c.until("really needs")))
            c.wait_until("really needs")
            self.play(*appear(*ff3, shift=None, lag=0.15), *appear(log5, shift=None),
                      run_time=min(1.2, c.until("remove")))

            c.wait_until("remove")
            self.play(ReplacementTransform(d5.nodes["D"], d4.nodes["M"]),
                      ReplacementTransform(d5.nodes["E"], d4.nodes["M"].copy()),
                      ReplacementTransform(d5.arcs["AD"], d4.arcs["AM"]),
                      ReplacementTransform(d5.arcs["CE"], d4.arcs["CM"]),
                      ReplacementTransform(d5.arcs["DB"], d4.arcs["MB"]),
                      ReplacementTransform(d5.arcs["EB"], d4.arcs["MB"].copy()),
                      run_time=min(1.6, c.until("fewer flip-flops")))
            self.remove(*self.mobjects)
            self.add(h, d4, ff3, log5)
            c.wait_until("fewer flip-flops")
            moves = [ff3[k].animate.shift((FF_XS2[k] - FF_XS3[k]) * RIGHT) for k in (0, 1)]
            log4 = log_line(4)
            self.play(*during(disappear(ff3[2]), 0, 0.45), *during(moves, 0.3, 1.0), *edit(log5, log4),
                      run_time=min(1.6, c.until("or more")))
            # the alternative: keep the codes, and the unused ones become don't cares
            c.wait_until("or more")
            self.play(*appear(orw, shift=None), FadeIn(km.grid), run_time=min(0.8, c.until("don't cares")))
            c.wait_until("don't cares")
            self.play(*appear(*km.xs, shift=None, lag=0.2), run_time=min(1.2, c.until(floor=0.6)))

    # -- end card: Lecture 11 opens on it ---------------------------------------------------------------
    def end(self):
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(8.0)
