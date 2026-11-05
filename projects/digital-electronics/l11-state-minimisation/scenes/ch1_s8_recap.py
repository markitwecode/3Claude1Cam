"""Chapter 1, scene 8: p. 147's warning, the six-slot recap, the teaser for Part 2. Clips c1.recap.1 – c1.recap.3.

Exposes end_card() (= handover_shot()): the last frame, two states with different rows and the
same outputs, a YELLOW "?", a faint implication-table staircase, the part line "Part 2 · When are two states the same?".
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

S2 = load_scene("ch1_s2_why")
S3 = load_scene("ch1_s3_mealy")
S4 = load_scene("ch1_s4_tree")
S6 = load_scene("ch1_s6_cascade")
S7 = load_scene("ch1_s7_left")


def _p(x, y):
    return np.array([x, y, 0.0])


def fit(m, w, h, center):
    k = min(w / m.width, h / m.height)
    m.scale(k).move_to(center)
    return m


# ---------------------------------------------------------------- recap slots
SW, SH = 4.3, 3.3
SLOT_X = (-4.5, 0.0, 4.5)
SLOT_Y = (1.8, -1.8)
VIS_W, VIS_H = 3.9, 2.2


def slot_center(i):
    return _p(SLOT_X[i % 3], SLOT_Y[i // 3])


def slot_frame(i):
    return RoundedRectangle(corner_radius=0.15, width=SW, height=SH).set_stroke(DIM, 1.5).move_to(slot_center(i))


def vis_center(i):
    return slot_center(i) + _p(0, 0.36)


def caption(i, text):
    t = T(text, 28, line_spacing=0.8)
    return t.move_to(slot_center(i)).align_to(slot_center(i) + _p(0, -0.84), UP)


def r1_visual():
    lad = S2.ladder()
    b15 = S2.ladder_bracket(lad, 3, 15)
    b7 = S2.ladder_bracket(lad, 2, 7, x=b15.brace.get_left()[0])
    top = VGroup(lad, b15, b7)
    chips = S2.code_chips()
    top.scale(0.33)
    chips.scale(0.3)
    g = VGroup(top, chips).arrange(DOWN, buff=0.15)
    return fit(g, VIS_W, VIS_H, vis_center(0))


def r2_visual():
    a = S4.StateCircle("A", radius=0.6, size=40).move_to(_p(-1.6, 0))
    cc = S4.StateCircle("C", radius=0.6, size=40).move_to(_p(1.6, 0))
    arc = S3.L10M._arc(_p(-1.0, 0.15), _p(1.0, 0.15), -0.7)
    lab = S4.mealy_label(1, 0, 44).move_to(_p(0, 1.1))
    top = VGroup(a, cc, arc, lab).scale(0.62)
    row = S3.state_table([S3.MACHINE[0]], rules_after=()).scale(0.56)
    g = VGroup(top, row).arrange(DOWN, buff=0.2)
    fit(g, VIS_W, VIS_H, vis_center(1))
    g.top, g.row = top, row
    return g


def r3_visual():
    return fit(S4.tree_diagram(), VIS_W, VIS_H, vis_center(2))


class MiniMerge(VGroup):
    """D on top, H and I below; H and I identical (GOLD)."""

    def __init__(self):
        super().__init__()
        P = {"D": _p(0, 1.0), "H": _p(-1.2, -0.6), "I": _p(1.2, -0.6)}
        self.P = P
        self.st = {n: S4.StateCircle(n).move_to(p) for n, p in P.items()}
        for n in "HI":
            self.st[n].circle.set_stroke(GOLD, 4)
        self.arcs, self.labels = {}, {}
        for x, tgt, side in ((0, "H", -1), (1, "I", 1)):
            s, e = S4._edge(P["D"], P[tgt]), S4._edge(P[tgt], P["D"])
            self.arcs[x] = Arrow(s, e, buff=0, stroke_width=3, color=FG, tip_length=0.18,
                                 max_tip_length_to_length_ratio=0.2)
            self.labels[x] = S4.place_on_arc(S4.mealy_label(x, 0, out_color=DIM), s, e, side)
        self.add(*self.st.values(), *self.arcs.values(), *self.labels.values())

    def swung(self):
        """D's input-1 arc redirected to H (curving below the straight 0 arc), and where its label goes."""
        d, h = self.st["D"].get_center(), self.st["H"].get_center()
        r = self.st["D"].circle.width / 2
        ang_s, ang_e = np.deg2rad(-70), np.deg2rad(-5)
        s = d + r * np.array([np.cos(ang_s), np.sin(ang_s), 0])
        e = h + r * np.array([np.cos(ang_e), np.sin(ang_e), 0])
        arc = Arrow(s, e, buff=0, stroke_width=3 * self.k, color=FG, tip_length=0.18 * self.k,
                    max_tip_length_to_length_ratio=0.2, path_arc=-0.9)
        mid = arc.point_from_proportion(0.5)
        return arc, mid + _p(0.38, -0.22) * self.k


def r4_visual():
    m = MiniMerge()
    w0 = m.width
    fit(m, VIS_W, VIS_H, vis_center(3))
    m.k = m.width / w0
    return m


def r5_visual():
    g = S6.matched_table()
    return fit(g, VIS_W, VIS_H, vis_center(4))


def r6_visual():
    d = S7.seven_diagram()
    d.scale(0.29)
    w1 = Mono("0101", 32, BLUE)
    orr = T("or", 28, DIM)
    w2 = Mono("1001", 32, BLUE)
    words = VGroup(w1, orr, w2).arrange(DOWN, buff=0.18)
    g = VGroup(d, words).arrange(RIGHT, buff=0.3)
    fit(g, VIS_W, VIS_H, vis_center(5))
    g.d, g.w1, g.orr, g.w2 = d, w1, orr, w2
    return g


# ---------------------------------------------------------------- the end card (handover to ch2 s1)
def staircase(n=8, cell=0.28, center=_p(0, -1.55)):
    cells = VGroup()
    for col in range(n - 1):
        for row in range(col, n - 1):
            sq = Square(cell).move_to(_p(col * cell, -row * cell))
            cells.add(sq)
    cells.set_stroke(DIM, 2, opacity=0.4).set_fill(opacity=0)
    cells.move_to(center).set_z_index(-2)
    return cells


def end_card():
    g = VGroup()
    inp = Mono("0110", 44, BLUE).move_to(_p(0, 2.95))
    circles, rows, ins, outs, out_arrows = [], [], [], [], []
    for sx, name, nxt in ((-1, "p", ("B", "C")), (1, "q", ("D", "E"))):
        c = S4.StateCircle(name, radius=0.55, size=52).move_to(_p(3.0 * sx, 1.5))
        circles.append(c)
        ins.append(Arrow(_p(0.8 * sx, 2.75), c.get_center() + 0.5 * normalize(_p(-3.0 * sx, 1.25)), buff=0,
                         stroke_width=3, color=BLUE, tip_length=0.2, max_tip_length_to_length_ratio=0.25))
        a0 = c.get_center() + _p(0.5 * sx, 0)
        out_arrows.append(Arrow(a0, a0 + _p(1.0 * sx, 0), buff=0, stroke_width=3, color=GREEN, tip_length=0.2,
                                max_tip_length_to_length_ratio=0.3))
        outs.append(Mono("0010", 44, GREEN).next_to(out_arrows[-1], RIGHT if sx > 0 else LEFT, buff=0.15))
        row = S3.state_table([(name, *nxt, "0", "0")], rules_after=()).scale(0.62)
        row.move_to(_p(3.2 * sx, -0.55))
        rows.append(row)
    q = T("?", 96, YELLOW).move_to(_p(0, 0.7))
    stair = staircase()
    VGroup(stair, inp, *ins, *circles, *rows, *out_arrows, *outs, q).shift(0.75 * DOWN)
    nxt = T("Part 2 · When are two states the same?", 40).move_to(_p(0, 3.2))   # L10's part-line style
    g.add(stair, inp, *ins, *circles, *rows, *out_arrows, *outs, q, nxt)
    g.inp, g.ins, g.circles, g.rows, g.out_arrows, g.outs = inp, ins, circles, rows, out_arrows, outs
    g.q, g.stair, g.next = q, stair, nxt
    return g


def handover_shot():
    return end_card()


# ---------------------------------------------------------------- the scene
class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()

    # -- p. 147's warning ---------------------------------------------------------------------
    def clip1(self):
        with self.say("c1.recap.1", gap=1.4) as c:
            tbl = S3.state_table(S6.ROWS_FINAL).scale(0.72).move_to(_p(-3.6, 1.6))
            self.play(FadeIn(tbl), run_time=1.2)   # early: p. 147's final table, a picture
            c.wait_until("slide")

            bullet = T("However, we note row matching is\nnot sufficient to find all the\n"
                       "equivalent states except for\ncertain special cases", 30, line_spacing=0.9,
                       disable_ligatures=True)
            bullet.move_to(_p(-3.6, -1.55))
            self.play(*appear(bullet), run_time=1.2)   # early: the slide's bullet, verbatim; the voice paraphrases it
            c.wait_until("not sufficient")
            hot = select(bullet, "not sufficient")[0]
            self.play(*recolor(hot, YELLOW), FlashUnder(hot, color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("here")

            d = S7.seven_diagram().scale(0.6).move_to(_p(3.7, 1.15))
            self.play(FadeIn(d), run_time=1.2)
            tick = check_mark(GREEN)
            tl = T("smallest possible here", 30, GREEN)
            row = VGroup(tick, tl).arrange(RIGHT, buff=0.2).move_to(_p(3.7, -1.55))
            c.wait_until(own_word=tl)
            self.play(*appear(tick, tl, lag=0.2), run_time=1.0)
            c.wait_until("later")

            tag = T("Part 3", 30, YELLOW)
            pill = RoundedRectangle(corner_radius=0.2, width=tag.width + 0.5, height=tag.height + 0.35)
            pill.set_stroke(YELLOW, 2).move_to(tag)
            ptag = VGroup(pill, tag).move_to(_p(3.7, -2.5))
            c.wait_until(own_word=tag)
            self.play(*appear(ptag), run_time=1.0)
            self.c1 = [tbl, bullet, d, tick, tl, ptag]

    # -- the six-slot recap -------------------------------------------------------------------
    def clip2(self):
        with self.say("c1.recap.2", gap=1.2) as c:
            frames = [slot_frame(i) for i in range(6)]
            sweep_clear(self, *[time_span(FadeIn(f), 0.6 + 0.1 * i, 1.2 + 0.1 * i) for i, f in enumerate(frames)],
                        keep=[], run_time=min(1.7, c.until("r1")))
            c.wait_until("r1")

            v1 = r1_visual()
            cap1 = caption(0, "fewer flip-flops,\nmore don't cares")
            self.play(FadeIn(v1), *appear(cap1), run_time=1.3)
            c.wait_until("r2")

            v2 = r2_visual()
            cap2 = caption(1, "Mealy: input/output\non the arc")
            self.play(FadeIn(v2.top), *appear(cap2), run_time=1.3)
            c.wait_until("compact table")
            self.play(FadeIn(v2.row, shift=0.15 * DOWN), run_time=1.2)
            c.wait_until("r3")

            v3 = r3_visual()
            cap3 = caption(2, "fifteen states,\nfour layers")
            self.play(FadeIn(v3), *appear(cap3, shift=None), run_time=1.3)
            c.wait_until("r4")

            m = r4_visual()
            self.play(FadeIn(m), run_time=1.0)
            self.play(*flash([m.st["H"], m.st["I"]], color=GOLD, time_width=1.5), run_time=1.4)
            cap4 = caption(3, "replace, then delete")
            c.wait_until(own_word=cap4)
            arc, pos = m.swung()
            self.play(Transform(m.arcs[1], arc), m.labels[1].animate.move_to(pos), *appear(cap4),
                      run_time=1.5)
            c.wait_until("delete")
            i_st = m.st["I"]
            self.play(*during(disappear(i_st.letter), 0, 0.35),
                      *during([i_st.circle.animate.move_to(m.st["H"].get_center()).set_stroke(opacity=0)], 0.1, 1.0),
                      run_time=1.5)
            self.remove(i_st.circle)
            m.remove(i_st)
            c.wait_until("r5")

            v5 = r5_visual()
            self.play(FadeIn(v5.tbl), run_time=1.2)   # early: s6's table, a picture
            c.wait_until("new matches")
            self.play(*[FadeIn(b) for b in v5.boxes.values()], run_time=1.2)
            cap5 = caption(4, "go round until\nnothing matches")
            c.wait_until(own_word=cap5)
            self.play(*appear(cap5), run_time=1.0)
            c.wait_until("r6")

            v6 = r6_visual()
            cap6 = caption(5, "seven states")
            self.play(FadeIn(v6.d), *appear(cap6), run_time=1.3)
            c.wait_until("zero one zero one")
            self.play(*appear(v6.w1), run_time=1.0)
            c.wait_until("one zero zero one")
            self.play(*appear(v6.orr, v6.w2, lag=0.3), run_time=min(1.2, c.until(floor=0.6)))

    # -- next time ------------------------------------------------------------------------------
    def clip3(self):
        ec = end_card()
        with self.say("c1.recap.3") as c:
            sweep_clear(self, *appear(*ec.circles, *ec.rows, lag=0.15), keep=[], run_time=1.6)
            self.play(*appear(ec.inp), *[GrowArrow(a) for a in ec.ins], run_time=1.2)
            self.play(*[GrowArrow(a) for a in ec.out_arrows], *appear(*ec.outs, shift=None, lag=0.2),
                      run_time=1.2)
            c.wait_until("tell them apart")
            self.play(*appear(ec.q), run_time=min(1.0, c.until("stronger", floor=0.5)))
            c.wait_until("stronger")
            self.play(FadeIn(ec.stair), run_time=min(1.8, c.until(floor=0.8)))
        self.play(*appear(ec.next), run_time=1.2)
        self.wait(8.0)   # the end card, held; the music carries it (handover to ch2 s1)
