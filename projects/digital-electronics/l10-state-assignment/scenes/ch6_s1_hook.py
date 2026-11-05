"""Chapter 6, scene 1: hook: the synchroniser again, its two K-maps, and one-hot's extra flip-flop. Clips c6.hook.1 – c6.hook.2.

Opens on ch5_s8_recap.end_card(); its Part 6 line travels into the title card. {last}: ch5 s3's diagram
(codes [10] [00] [01], "FF labels [s1 s0]") full size; {kmaps}: it moves to ch6 s2's "left" placement,
two flip-flops (s1, s0) below it, ch5 s6/s7's maps (no headings) and equations on the right.
Clip 2: maps dim to the right edge, a Part 4 one-hot row inset steps its GOLD 1, the codes edit into
one-hot, a third flip-flop (s2), "+1 flip-flop", "?"; {answer}: all but the diagram clears, the
diagram grows back to full size and its arcs shimmer.
Ends exactly on ch6_s2_codes.opening_shot() (s2 opens on it).
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
from lib.titles import title_card  # noqa: E402

D3 = load_scene("ch5_s3_diagram")
S6 = load_scene("ch5_s6_d1")
S7 = load_scene("ch5_s7_d0")
H4 = load_scene("ch4_s1_hook")
C2 = load_scene("ch6_s2_codes")


def _p(x, y):
    return np.array([x, y, 0.0])


CODES2 = {"Sync": "10", "Hunt": "00", "Sight": "01"}      # Sync, Hunt, Sight order, as ONEHOT
DIAG_S = 0.7
DIAG_SHIFT = _p(-3.3, 0.6)
LABEL_UP = _p(-3.4, 3.35)
FF_XS = {0: -5.4, 1: -3.05, 2: -0.7}     # k: s2 (new), s1, s0
FF_Y = -2.85
FF_S = 0.55
MAP_S = 0.7
MAP_XS = (1.95, 5.0)
MAP_Y = 1.1
KM_DIM_S = 0.82
KM_DIM_C = _p(4.1, -1.15)
D0_MAP = (("", "1", "1", ""), ("1", "1", "", ""), ("X", "X", "X", "X"), ("", "", "", ""))
INSET_C = _p(2.4, 2.75)
INSET_S = 0.7


def handover_shot():
    return C2.opening_shot()


def place(d):
    """This scene's side placement: scale 0.7, names and codes grown back to >= 26 pt."""
    d.scale(DIAG_S, about_point=ORIGIN).shift(DIAG_SHIFT)
    for n in D3.STATES:
        d.name[n].scale(1.17)
        if d.code[n] is not None:
            d.code[n].scale(1.2)
    d.code["Sight"].shift(0.2 * LEFT)
    return d


def onehot_placed():
    d = C2.onehot_diagram()
    return place(d)


def old_label():
    return VGroup(T("FF labels", 30, DIM), Mono("[s1 s0]", 30, GREEN)).arrange(RIGHT, buff=0.22)


def small_maps():
    m1 = S6.kmap4(S6.D1_MAP, center=_p(MAP_XS[0], MAP_Y), scale=MAP_S)
    m0 = S6.kmap4(D0_MAP, center=_p(MAP_XS[1], MAP_Y), scale=MAP_S)
    for m in (m1, m0):
        m.remove(m.col_heads, m.row_heads, m.corner, m.bars)
    for (r, k), col in zip(S6.D1_ESSENTIAL, S6.D1_COLORS):
        m1.ent[r][k].set_color(col)
    # ch5 s6's loops; at this size the TEAL pill is drawn narrower than the PURPLE loop's right edge,
    # so the two never share an edge (they would read as one 3-cell column)
    l1 = [loop_xy(m1, cells, col, inset, inset) for (cells, inset), col in zip(S6.D1_LOOPS, S6.D1_COLORS)]
    l1[2] = loop_xy(m1, S6.D1_LOOPS[2][0], TEAL, 0.3, 0.04)
    l0 = [S6.loop4(m0, S7.PINK_CELLS, PINK, 0.08), S6.loop4(m0, S7.PURPLE_CELLS, PURPLE, 0.08)]
    n1 = MathTex("D_1", font_size=44, color=BLUE).next_to(m1.grid, UP, buff=0.25)
    n0 = MathTex("D_0", font_size=44, color=BLUE).next_to(m0.grid, UP, buff=0.25)
    e1 = S6.term_eq("D_1", S6.D1_TERMS, S6.D1_COLORS, 0.0, 0.0, xs=(-2.05, 0.3, 2.8))
    e0 = S6.term_eq("D_0", S7.D0_TERMS, S7.D0_COLORS, 0.0, 0.0, xs=(-0.9, 1.75))
    for e in (e1, e0):
        e.scale(0.8)
    e1.move_to(_p(3.55, -1.0))
    e0.move_to(_p(3.55, -2.1))
    e0.align_to(e1, LEFT)
    xs = VGroup(*[m1.ent[2][k] for k in range(4)], *[m0.ent[2][k] for k in range(4)])
    g = VGroup(m1, m0, n1, n0, *l1, *l0, e1, e0)
    g.m1, g.m0, g.n1, g.n0, g.l1, g.l0, g.e1, g.e0, g.xs = m1, m0, n1, n0, l1, l0, e1, e0, xs
    return g


def loop_xy(m, cells, color, ix, iy):
    """S6.loop4 with separate horizontal / vertical insets (in cells)."""
    sqs = VGroup(*[m.sq(r, k) for r, k in cells])
    w, h = sqs.width - 2 * ix * m.s, sqs.height - 2 * iy * m.s
    return RoundedRectangle(corner_radius=min(0.3 * m.s, w / 2.01), width=w, height=h,
                            stroke_color=color, stroke_width=4).move_to(sqs)


def dim_target(mob, op, keep=(), keep_op=0.75):
    keep_ids = {id(x) for k in keep for x in k.get_family()}
    t = mob.copy()
    for src, m in zip(mob.family_members_with_points(), t.family_members_with_points()):
        o = keep_op if id(src) in keep_ids else op
        if m.get_fill_opacity() > 0:
            m.set_fill(opacity=o * m.get_fill_opacity())
        if m.get_stroke_width() > 0:
            m.set_stroke(opacity=o * m.get_stroke_opacity())
    return t


def ff_unit(k):
    u = C2.onehot_ff(k, _p(FF_XS[k], FF_Y), scale=FF_S, out_size=38)
    return VGroup(u.ff, u.out)


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(1.0)      # handover: hold ch6 s2's opening shot

    # ------------------------------------------------------------ c6.hook.1
    def clip1(self):
        card = title_card("Part 6 · One-hot, straight from the diagram")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        end = load_scene("ch5_s8_recap").end_card()
        self.add(end)
        with self.say("c6.hook.1") as c:
            part = end.part
            self.remove(end)
            rest = [m for m in end if m is not part]
            self.add(*rest, part)
            self.wait(0.7)   # ch5's end card holds a moment: the cut reads as a continuation
            self.play(*during(disappear(*rest), 0, 0.4),
                      *during([part.animate.scale(card.part.height / part.height).move_to(card.part)], 0.1, 0.6),
                      *during(appear(card.title, card.rule, card.course, lag=0.2), 0.55, 1),  # early: title card
                      run_time=min(1.6, c.until("last", floor=1.0)))
            self.remove(part)
            self.add(card.part)
            c.wait_until("last")

            # {last}: ch5 s3's diagram, with Part 5's codes
            d = D3.sync_diagram(codes=CODES2)
            lab = old_label().move_to(C2.LABEL_CORNER)
            lab.align_to(C2.opening_shot()[1], LEFT)
            self.d, self.lab = d, lab
            # the card is gone before the diagram starts to fade in (no title text over the arcs)
            card_parts = [m for m in self.mobjects]
            back = during(appear(d, lab, shift=None, lag=0.2), 0.48, 1.0)
            self.play(*during(disappear(*card_parts), 0, 0.42), *back, run_time=1.8)  # early: the diagram returns whole, as the brief asks
            c.wait_until("hunt")
            t1 = c.at("sight") - c.at("hunt")
            t2 = c.at("sync") - c.at("hunt")
            anims = []
            for n, st in (("Hunt", 0.0), ("Sight", t1), ("Sync", t2)):
                anims.append(time_span(d.circle[n].animate(rate_func=there_and_back).set_stroke(YELLOW, 7),
                                       st, st + 1.0))
            self.play(*anims, run_time=t2 + 1.0)

            # {kmaps}: the diagram to the left, its two flip-flops below, the maps on the right
            c.wait_until("kmaps")
            tgt = place(D3.sync_diagram(codes=CODES2))
            d.target = tgt
            self.ffs = {k: ff_unit(k) for k in (1, 2)}
            lab2 = old_label().move_to(LABEL_UP)
            self.play(*during(disappear(lab), 0, 0.25),
                      *during([MoveToTarget(d)], 0.1, 0.6),
                      *during(appear(lab2, shift=None), 0.6, 0.85),
                      *during(appear(self.ffs[1], self.ffs[2], lag=0.3), 0.55, 1.0),
                      run_time=min(2.2, c.until("inputs", floor=1.5)))
            self.lab = lab2
            km = small_maps()
            self.km = km
            c.wait_until("inputs")
            self.play(*appear(km.e1, km.e0, lag=0.4), run_time=min(1.4, c.until("four-variable", floor=1.0)))
            c.wait_until("four-variable")
            self.play(*appear(km.m1, km.m0, km.n1, km.n0, shift=None, lag=0.2),
                      run_time=min(1.5, c.until("don't cares", floor=1.0)))
            c.wait_until("don't cares")
            self.play(*flash(list(km.xs), color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("groups")
            self.play(*[FadeIn(lp) for lp in (*km.l1, *km.l0)], run_time=1.2)
            settle(self, km)

    # ------------------------------------------------------------ c6.hook.2
    def clip2(self):
        d, lab, km, ffs = self.d, self.lab, self.km, self.ffs
        with self.say("c6.hook.2") as c:
            # {same}: the maps dim and slide to the edge
            t = dim_target(km, 0.4, keep=(*km.l1, *km.l0))   # loops stay coloured enough to tell apart
            t.scale(KM_DIM_S).move_to(KM_DIM_C)
            km.target = t
            self.play(MoveToTarget(km), run_time=min(1.6, c.until("part four", floor=1.0)))
            c.wait_until("part four")
            row = H4.onehot_row(n=5, hot=0)
            row.remove(row.clk_label)
            row.scale(INSET_S).move_to(INSET_C)
            tag = T("Part 4: one-hot", 30, t2c={"Part 4:": DIM}).next_to(row, DOWN, buff=0.2)
            self.play(*appear(row, tag, lag=0.3), run_time=1.2)
            self.row, self.tag = row, tag
            digs = list(row.digits)
            row.remove(*digs)
            self.add(*digs)
            self.digs, self.hot = digs, 0
            while c.until("codes", floor=0) > 1.6:
                self.wait(0.8)
                self.play(*self.step(), run_time=0.6)
            c.wait_until("codes")

            # {codes}: the codes become one-hot, the corner label gains s2
            oh = onehot_placed()
            new_codes = [oh.code[n].copy() for n in D3.STATES]
            old_codes = [d.code[n] for n in D3.STATES]
            d.remove(*old_codes)
            self.add(*old_codes)
            nl = C2.ff_label()
            nl.shift(lab[0].get_center() - nl[0].get_center())
            self.remove(lab)
            self.add(lab[0], lab[1])
            anims = []
            for o, n in zip(old_codes, new_codes):
                anims += edit(o, n)
            anims += edit(lab[1], nl[1])
            self.play(*anims, run_time=min(1.8, c.until("three", floor=1.2)))
            self.remove(lab[0], nl[1])
            self.add(nl)
            self.lab = lab = nl
            settle(self, d, add=new_codes)
            for n, g in zip(D3.STATES, new_codes):
                d.code[n] = g
            c.wait_until("three")
            ffs[0] = ff_unit(0)
            # box and its s_2 label arrive together, as one piece
            self.play(FadeIn(ffs[0], shift=0.25 * DOWN), *self.step(), run_time=1.2)

            # {question}
            c.wait_until("question")
            plus = T("+1 flip-flop", 34, YELLOW).next_to(ffs[0][0].box, UP, buff=0.3)
            self.play(*appear(plus), ffs[0][0].box.animate.set_stroke(YELLOW, 5), run_time=1.0)
            c.wait_until("buy")
            q = T("?", 96, YELLOW).move_to(_p(1.2, -2.6))
            self.play(*appear(q), run_time=1.0)
            c.wait_until("how much easier")
            self.play(FlashAround(q, color=YELLOW, time_width=1.5), *self.step(), run_time=1.2)

            # {answer}: everything but the diagram goes; it grows back to full size
            c.wait_until("answer")
            final = C2.opening_shot()
            going = [km, row, tag, *self.digs, plus, q, *ffs.values(), lab]
            self.play(*during(disappear(*going), 0, 0.3),
                      *during([ReplacementTransform(d, final[0])], 0.3, 0.85),
                      *during(appear(final[1], shift=None), 0.88, 1.0),
                      run_time=min(2.2, c.until(floor=1.5)))
            self.remove(*self.mobjects)
            self.add(final)
            paths = []
            for a in final[0].arcs:
                p = a.copy()
                p.pop_tips()
                p.set_stroke(YELLOW, 7)
                paths.append(p)
            self.play(LaggedStart(*[VShowPassingFlash(p, time_width=0.6) for p in paths], lag_ratio=0.12),
                      run_time=min(2.0, c.until(floor=1.0)))
            self.remove(*paths)

    # ------------------------------------------------------------ the inset's hot 1 steps along
    def step(self):
        n = len(self.digs)
        i, j = self.hot, (self.hot + 1) % n
        anims = []
        for k, b in ((i, 0), (j, 1)):
            nd = H4.hot_bit(b).scale(INSET_S).move_to(self.row.boxes[k])
            anims += swap(self.digs[k], nd, shift=0.1 * UP)
            self.digs[k] = nd
            box = self.row.boxes[k]
            anims.append(box.animate.set_fill(GOLD, 0.22) if b else box.animate.set_fill(BG, 1))
        self.hot = j
        return anims
