"""Chapter 2, scene 8: the seven-panel recap and the teaser for Part 3. Clips c2.recap.1 - c2.recap.2.

Opens on ch2_s7_columna's handover_shot(). Panels (4 + 3) reuse each scene's own drawing.
Exposes end_card(): the last frame (s7's shot, the nine empty open cells outlined YELLOW, a YELLOW "?"
beside each of column A's five live implied pairs, the part line "Part 3 · Solving the implication
table"). ch3 s1 opens on it.
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

L1 = load_scene("ch2_s1_hook")
L2 = load_scene("ch2_s2_definition")
L3 = load_scene("ch2_s3_onestep")
L4 = load_scene("ch2_s4_implied")
L5 = load_scene("ch2_s5_layout")
L6 = load_scene("ch2_s6_outputs")
L7 = load_scene("ch2_s7_columna")


def _p(x, y):
    return np.array([x, y, 0.0])


def fit(m, w, h, center):
    k = min(w / m.width, h / m.height)
    m.scale(k).move_to(center)
    return m


# ---------------------------------------------------------------- recap slots (4 + 3)
TOP_W = (3.15, 3.15, 2.85, 3.85)      # r4's two-part caption needs the widest slot
TOP_XS = [-6.65 + sum(TOP_W[:k]) + 0.1 * k + TOP_W[k] / 2 for k in range(4)]
TOP = dict(h=3.5, y=1.8)
BOT = dict(w=4.3, h=3.3, xs=(-4.45, 0.0, 4.45), y=-1.8)


def slot_center(i):
    return _p(TOP_XS[i], TOP["y"]) if i < 4 else _p(BOT["xs"][i - 4], BOT["y"])


def slot_w(i):
    return TOP_W[i] if i < 4 else BOT["w"]


def slot_frame(i):
    h = TOP["h"] if i < 4 else BOT["h"]
    return RoundedRectangle(corner_radius=0.15, width=slot_w(i), height=h).set_stroke(DIM, 1.5).move_to(slot_center(i))


def vis_center(i, dx=0.0):
    return slot_center(i) + _p(dx, 0.75 if i < 4 else 0.5)


def vis_wh(i):
    return (slot_w(i) - 0.35, 1.75 if i < 4 else 1.9)


def caption(i, text, **kw):
    t = T(text, 28, line_spacing=0.8, **kw)
    return t.move_to(slot_center(i) + _p(0, -1.0 if i < 4 else -1.1))


def stacked_lanes():
    """s1's two lanes (circles, FG arrows, GOLD-boxed output rows facing each other, GOLD "=" between),
    packed tight for a recap panel: "start in A" above lane A, "start in D" below lane D, input row
    dropped, so the labels stay readable when the whole thing is shrunk to a panel (text ~20 at 1080p)."""
    pitch, r = 0.95, 0.3
    xs = [pitch * k - 2 * pitch for k in range(5)]
    lane_y, out_y, lab_y = (1.07, -1.07), (0.42, -0.42), (1.72, -1.72)
    g = VGroup()
    boxes = []
    for l, seq in enumerate(L1.LANES):
        cs = [VGroup(Circle(radius=r).set_stroke(FG, 3).set_fill(BG, 0).move_to(_p(x, lane_y[l])),
                     T(s, 32).move_to(_p(x, lane_y[l]))) for x, s in zip(xs, seq)]
        ars = [Arrow(cs[i].get_right(), cs[i + 1].get_left(), buff=0.03, stroke_width=3, color=FG,
                     tip_length=0.13, max_tip_length_to_length_ratio=0.5) for i in range(4)]
        outs = [(T(L1.OUT[s], 32, GREEN, weight=BOLD) if L1.OUT[s] == "1" else T(L1.OUT[s], 32))
                .move_to(_p(x, out_y[l])) for x, s in zip(xs, seq)]
        box = (Rectangle(width=4 * pitch + 0.7, height=0.46).move_to(_p(0, out_y[l]))
               .set_stroke(GOLD, 2.5).set_fill(GOLD, 0.15).set_z_index(-1))
        lab = T(f"start in {seq[0]}", 37).move_to(_p(0, lab_y[l])).align_to(cs[0], LEFT)
        boxes.append(box)
        g.add(lab, *cs, *ars, box, *outs)
    eq = T("=", 66, GOLD, weight=BOLD).rotate(PI / 2).move_to(_p(xs[2], 0)).set_z_index(1)
    g.add(eq)
    g.eq, g.out_boxes = eq, boxes
    return g


def r1_visual():
    # the lanes get the panel's full height above its caption
    return fit(stacked_lanes(), slot_w(0) - 0.35, 2.05, slot_center(0) + _p(0, 0.62))


def r2_visual():
    return fit(L2.machine_boxes(), *vis_wh(1), vis_center(1))


def r3_visual():
    return fit(L3.pq_diagram(marks=True), *vis_wh(2), vis_center(2))


def r4_visual():
    fork = L4.decision_fork()
    card = L4.promise_card("p ≡ q, if p′ ≡ q′", 38).move_to(_p(3.4, -1.0))
    g = VGroup(fork.top, *fork.arms, fork.lab_l, fork.box, fork.cross, fork.lab_r, card)
    fit(g, *vis_wh(3), vis_center(3))
    g.fork, g.card = fork, card
    return g


def r5_visuals():
    w, h = vis_wh(4)
    it = fit(L5.implication_table(), w, h, vis_center(4, -0.45))
    g8 = fit(L5.grid8(), w, h, vis_center(4, -0.45))
    n28 = T("28", 48, GOLD).move_to(it.cell("A", "B").get_center() + _p(1.55, -0.15))
    return g8, it, n28


def r6_visual():
    shot = L6.handover_shot()
    g = VGroup(shot[1], shot[2], shot[3])
    fit(g, *vis_wh(5), vis_center(5))
    g.it, g.dots, g.crosses = shot[1], shot[2], shot[3]
    return g


def r7_visual():
    shot = L6.handover_shot()
    it, dots, crosses = shot[1], shot[2], shot[3]
    rows = "BCDEFGH"
    cells = [it.cell("A", r) for r in rows]
    xs = [crosses.by[f"A-{r}"] for r in "CEFH"]
    letters = [it.row_letter(r) for r in rows] + [it.col_letter("A")]
    ldots = [dots.rows[r] for r in "CEFH"]
    pairs = L7.column_a_pairs(it)
    g = VGroup(*cells, *xs, *letters, *ldots, *pairs)
    fit(g, 1.3, 2.95, slot_center(6) + _p(-1.45, 0))     # the strip runs the panel's full height
    g.base = VGroup(*cells, *xs, *letters, *ldots)
    g.pairs = pairs
    g.ce = pairs[3]
    g.cells = {r: c for r, c in zip(rows, cells)}
    lanes = fit(stacked_lanes(), 2.75, 1.95, slot_center(6) + _p(0.7, 0.62))
    return g, lanes


# ---------------------------------------------------------------- the end card (ch3 s1 opens on it)
OPEN9 = ["B-D", "B-G", "C-E", "C-F", "C-H", "D-G", "E-F", "E-H", "F-H"]
LIVE = (0, 1, 3, 4, 5)     # column A's pairs that still stand (index 2 is the struck A-D)


def end_card():
    shot = L7.handover_shot()
    it = shot[0][1]
    cells = [it.cell(*p.split("-")) for p in OPEN9]
    for sq in cells:
        sq.set_z_index(1).set_stroke(YELLOW, 5)
    pairs = [shot[1 + i] for i in LIVE]
    qs = [set_backstroke(T("?", 28, YELLOW).next_to(p, RIGHT, buff=0.03), width=6).set_z_index(2) for p in pairs]
    nxt = T("Part 3 · Solving the\nimplication table", 36, line_spacing=0.85).move_to(_p(4.35, 2.8))
    g = VGroup(shot, *qs, nxt)
    g.shot, g.it, g.open_cells, g.qs, g.next = shot, it, cells, qs, nxt
    return g


# ---------------------------------------------------------------- the scene
class Recap(NarratedScene):
    def construct(self):
        self.add(L7.handover_shot())
        self.clip1()
        self.clip2()
        self.play(*appear(self.ec.next), run_time=1.2)
        self.wait(8.0)   # the end card, held; the music carries it. The chapter ends on it (ch3 s1 opens on it)

    # -- r1 - r4 ------------------------------------------------------------------------------
    def clip1(self):
        with self.say("c2.recap.1") as c:
            frames = [slot_frame(i) for i in range(7)]
            sweep_clear(self, *[time_span(FadeIn(f), 0.5 + 0.08 * i, 1.0 + 0.08 * i) for i, f in enumerate(frames)],
                        keep=[], run_time=1.5)
            c.wait_until("r1")

            v1 = r1_visual()
            self.play(FadeIn(v1), run_time=1.2)
            cap1 = caption(0, "different rows,\nsame outputs")
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("same outputs")
            self.play(FlashAround(v1.eq, color=GOLD, time_width=1.5),
                      *flash(v1.out_boxes, color=GOLD, time_width=1.5), run_time=1.4)
            c.wait_until("r2")

            v2 = r2_visual()
            self.play(FadeIn(v2), run_time=1.2)
            cap2 = caption(1, "same outputs\nfor every input\nsequence")
            c.wait_until(own_word=cap2)
            self.play(*appear(cap2), FlashAround(v2.eq, color=GOLD, time_width=1.5, run_time=1.4), run_time=1.4)
            c.wait_until("r3")

            v3 = r3_visual()
            v3.remove(v3.eq_next)
            self.play(FadeIn(v3), run_time=1.2)
            cap3 = caption(2, "same outputs,\nequivalent\nnext states")
            c.wait_until(own_word=cap3)
            self.play(*appear(cap3), run_time=1.0)
            c.wait_until("equivalent next states")
            self.play(FadeIn(v3.eq_next, scale=1.3), FlashAround(v3.eq_next, color=GOLD, time_width=1.5),
                      run_time=1.4)
            c.wait_until("r4")

            v4 = r4_visual()
            f = v4.fork
            cap4a = caption(3, "differ: settled")
            cap4b = caption(3, "same: implied pairs")
            VGroup(cap4a, cap4b).arrange(DOWN, buff=0.12).move_to(caption(3, "x\nx"))
            self.play(FadeIn(f.top), *[GrowArrow(a) for a in f.arms], run_time=1.0)
            c.wait_until(own_word=cap4a)
            self.play(FadeIn(f.lab_l), FadeIn(f.box), *[Create(l) for l in f.cross], *appear(cap4a),
                      run_time=1.2)
            c.wait_until("If they match")
            self.play(FadeIn(f.lab_r), run_time=1.0)
            c.wait_until("implied pairs")
            self.play(Create(v4.card.frame), FadeIn(v4.card.text), *appear(cap4b), run_time=1.3)
            c.wait_until("promises")
            self.play(FlashAround(v4.card, color=YELLOW, time_width=1.5), run_time=min(1.4, c.until(floor=0.6)))

    # -- r5 - r7, then next time -------------------------------------------------------------
    def clip2(self):
        with self.say("c2.recap.2") as c:
            g8, it5, n28 = r5_visuals()
            cap5 = caption(4, "a cell for every pair")
            self.play(FadeIn(g8), *appear(cap5), run_time=1.2)
            c.wait_until("staircase")
            moves = [ReplacementTransform(g8.cell(*p.split("-")), it5.cell(*p.split("-"))) for p in it5.pairs]
            moves += [ReplacementTransform(g8.col_letter(l), it5.col_letter(l)) for l in "ABCDEFG"]
            moves += [ReplacementTransform(g8.row_letter(l), it5.row_letter(l)) for l in "BCDEFGH"]
            gone = [g8.cell(a, b) for a in "ABCDEFGH" for b in "ABCDEFGH" if not a < b]
            gone += [g8.col_letter("H"), g8.row_letter("A")]
            self.play(*moves, *[FadeOut(m) for m in gone], run_time=min(1.5, c.until("twenty-eight")))
            settle(self, it5)
            c.wait_until("twenty-eight")
            self.play(*appear(n28, shift=None), FlashAround(n28, color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("r6")

            v6 = r6_visual()
            cap6 = caption(5, "different outputs:\n16 crosses", t2c={"16": GOLD})
            self.play(FadeIn(v6.it), FadeIn(v6.dots), *appear(cap6), run_time=1.0)
            c.wait_until("crossed out")
            n = len(v6.crosses)
            self.play(*[time_span(Create(x), 0.05 * i, 0.05 * i + 0.5) for i, x in enumerate(v6.crosses)],
                      run_time=0.05 * (n - 1) + 0.5)
            c.wait_until("r7")

            v7, lanes = r7_visual()
            cap7 = caption(6, "column A:\nthree promises", t2c={"three": GOLD})
            cap7.move_to(slot_center(6) + _p(0.65, -0.95))
            self.play(FadeIn(v7.base), *appear(cap7), run_time=1.0)
            self.play(*[FadeIn(p) for p in v7.pairs], run_time=1.0)
            c.wait_until("promises")
            self.play(*flash([v7.cells[r] for r in "BDG"], color=YELLOW, time_width=1.5), run_time=1.3)
            c.wait_until("r7b")

            self.play(FadeIn(lanes), run_time=0.7)
            c.wait_until("just one of them")
            self.play(*recolor(v7.ce, GOLD), FlashAround(v7.ce, color=GOLD, time_width=1.5), run_time=1.4)
            c.wait_until("next")

            ec = end_card()
            self.ec = ec
            for sq in ec.open_cells:
                sq.set_stroke(FG, 2)
            sweep_clear(self, FadeIn(ec.shot), keep=[], run_time=1.6)
            c.wait_until("the other nine cells")
            self.play(*[time_span(sq.animate.set_stroke(YELLOW, 5), 0.18 * i, 0.18 * i + 0.6)
                        for i, sq in enumerate(ec.open_cells)], run_time=0.18 * 8 + 0.6)
            c.wait_until("which")
            self.play(*appear(*ec.qs, lag=0.25), run_time=min(1.4, c.until(floor=0.8)))
