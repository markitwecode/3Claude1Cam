"""Chapter 2, scene 3: one step at a time: p. 148's one-step test for equivalence. Clips c2.step.1 - c2.step.4.

Opens on ch2_s2_definition's handover_shot() (dim table + shrunk definition card); ends on an empty frame.

Shared drawing (import with load_scene("ch2_s3_onestep")):
- `pq_diagram(marks=True)`: p. 148's diagram at its home (left half): circles p, q stacked on the
  left, p', q' on the right (YELLOW letters), arcs p -> p', q -> q' labelled x_p/y_p, x_q/y_q
  (x BLUE, y GREEN). `.p .q .pp .qp` (VGroup(circle, letter), `.circle`, `.letter`), `.arcs` [2],
  `.labels` [2] (MathTex, `.inp`, `.out`), `.eq_pq`, `.eq_next` (GOLD vertical ≡ between p and q,
  p' and q'; in the group only with marks=True).
- `fan_left(d, letters=("p'", "q'"), labels=True)`: the other input's pair, drawn left of p and q of
  a scale-1 diagram d: `.circs` [2], `.arcs` [2], `.labels`, `.eq` (not in the group).
"""
# style: 2
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch2_s2_definition")
S1 = load_scene("ch2_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ shared: p. 148's p/q diagram
R_PQ = 0.45
P_HOME = _p(-3.4, 1.1)
DX, DY = 3.2, 2.8
FAN_DX = 2.7


def _state(tex, center, color=YELLOW, size=48, r=R_PQ):
    c = Circle(radius=r).set_stroke(FG, 3).set_fill(BG, 0).move_to(center)
    t = MathTex(tex, font_size=size, color=color).move_to(center)
    g = VGroup(c, t)
    g.circle, g.letter = c, t
    return g


def _arc(a, b, r=R_PQ, stroke=3):
    d = b - a
    u = d / np.linalg.norm(d)
    return Arrow(a + u * r, b - u * r, buff=0, stroke_width=stroke, color=FG, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.2)


def _mlabel(s, size=40):
    m = MathTex(f"x_{s}", "/", f"y_{s}", font_size=size)
    m[0].set_color(BLUE)
    m[2].set_color(GREEN)
    m.inp, m.out = m[0], m[2]
    return m


def _equiv(center, size=60):
    return MathTex(r"\equiv", font_size=size, color=GOLD).rotate(PI / 2).move_to(center)


def pq_diagram(marks=True):
    p0 = P_HOME
    q0 = p0 + DY * DOWN
    pp0, qp0 = p0 + DX * RIGHT, q0 + DX * RIGHT
    p, q, pp, qp = _state("p", p0), _state("q", q0), _state("p'", pp0), _state("q'", qp0)
    arcs = [_arc(p0, pp0), _arc(q0, qp0)]
    labels = [_mlabel("p").next_to(arcs[0], UP, buff=0.12), _mlabel("q").next_to(arcs[1], DOWN, buff=0.12)]
    eq_pq, eq_next = _equiv((p0 + q0) / 2), _equiv((pp0 + qp0) / 2)
    g = VGroup(p, q, pp, qp, *arcs, *labels)
    if marks:
        g.add(eq_pq, eq_next)
    g.p, g.q, g.pp, g.qp, g.arcs, g.labels = p, q, pp, qp, arcs, labels
    g.eq_pq, g.eq_next = eq_pq, eq_next
    return g


def fan_left(d, letters=("p'", "q'"), labels=True):
    """The other input's pair, drawn to the left of p and q (d at scale 1)."""
    p0, q0 = d.p.get_center(), d.q.get_center()
    a0, b0 = p0 + FAN_DX * LEFT, q0 + FAN_DX * LEFT
    if letters:
        circs = [_state(letters[0], a0), _state(letters[1], b0)]
    else:
        circs = [Circle(radius=R_PQ).set_stroke(FG, 3).set_fill(BG, 0).move_to(m) for m in (a0, b0)]
    arcs = [_arc(p0, a0), _arc(q0, b0)]
    g = VGroup(*circs, *arcs)
    g.circs, g.arcs = circs, arcs
    g.labels = []
    if labels:
        g.labels = [_mlabel("p").next_to(arcs[0], UP, buff=0.12), _mlabel("q").next_to(arcs[1], DOWN, buff=0.12)]
        g.add(*g.labels)
    g.eq = _equiv((a0 + b0) / 2)
    return g


# ------------------------------------------------------------------ local pieces
def _rich(s, size, rules):
    """T line with the given regex matches recoloured (ligatures off: string index = glyph index)."""
    t = T(s, size, disable_ligatures=True)
    for pat, col in rules:
        for m in re.finditer(pat, s):
            for g in t.submobjects[m.start():m.end()]:
                g.set_color(col)
    return t


RICH = [(r"(?<!\w)[pq]′?(?!\w)", YELLOW), (r"(?<!\w)x(?!\w)", BLUE), (r"(?<!\w)y(?!\w)", GREEN), (r"≡", GOLD)]

BULLET1 = [
    "In practice, 2 states p and q can be considered to",
    "be equivalent if for any input bit sequence x , the",
    "corresponding outputs y are identical and the next",
    "states p′ and q′ are equivalent, i.e., p′ ≡ q′",
]
BULLET2 = [
    "This is in contrast to row matching where p′ and q′ have",
    "to be the same, i.e., the identical state.",
]


def bullet(lines, size=28):
    return VGroup(*[_rich(s, size, RICH) for s in lines]).arrange(DOWN, buff=0.17, aligned_edge=LEFT)


def center_for(g, f, p_target):
    """Where to move_to g after scaling it by f so that g.p lands on p_target."""
    v = g.p.get_center() - g.get_center()
    return p_target - f * v


def detach(scene, *mobs):
    """Take parts out of their on-screen groups and put them on screen on their own (no visible change)."""
    for top in list(scene.mobjects):
        for m in top.get_family():
            for x in mobs:
                if x in m.submobjects:
                    m.remove(x)
    scene.add(*mobs)


# clip 3: output-sequence rows
RX0, RP, BOX, GAP = -1.9, 0.78, 0.56, 0.35
ROW_Y = (1.05, -1.05)
NBOX = 8


def _box(x, y):
    return Square(BOX).set_stroke(GREEN, 3).set_fill(GREEN, 0.2).move_to(_p(x, y))


def _seq_label(s, primes, size=36):
    m = MathTex(r"\text{sequence from }", s + "'" * primes, font_size=size)
    m[1].set_color(YELLOW)
    return m


def _brace(boxes, side):
    if side > 0:
        return span_brace(boxes[0].get_corner(UL), boxes[-1].get_corner(UR), direction=UP, buff=0.12)
    return span_brace(boxes[0].get_corner(DL), boxes[-1].get_corner(DR), direction=DOWN, buff=0.12)


def _next_to_brace(lab, br, side):
    return lab.next_to(br, UP if side > 0 else DOWN, buff=0.1)



def compact_lanes(k=0.62):
    """s1's two lanes, header dropped and "start in" labels moved left of each lane, so they fit
    the band above the A/D diagram at a readable size (text 30 * k)."""
    g = S1.two_lanes()
    g.remove(g.xlabel, *g.inputs, *g.arrow_labels[1])   # lane D's inputs repeat lane A's
    for l in range(2):
        g.labels[l].next_to(g.circles[l][0], LEFT, buff=0.3)
    return g.scale(k)


class OneStep(NarratedScene):
    def construct(self):
        hs = S2.handover_shot()
        self.tbl0, self.card = hs[0], hs[1]
        self.add(self.tbl0, self.card)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------------- c2.step.1
    def clip1(self):
        card = self.card
        with self.say("c2.step.1") as c:
            card.generate_target()
            card.target.scale_to_fit_width(3.0).to_corner(UL, buff=0.4)
            self.play(*during(disappear(self.tbl0), 0, 0.5), MoveToTarget(card), run_time=1.4)
            title = T("State Equivalence", 44).move_to(_p(1.75, 3.35))
            self.play(*appear(title), run_time=0.9)  # early: the slide's title, shown whole
            b1 = bullet(BULLET1).next_to(title, DOWN, buff=0.35)
            b1.set_x(1.75)
            self.play(*appear(b1, shift=None), run_time=1.0)  # early: the slide's bullet, read whole
            self.title, self.b1 = title, b1

            d = pq_diagram(marks=False)
            d.shift(1.05 * DOWN)
            self.d = d
            c.wait_until("arcs")
            self.play(*appear(d.p, d.q, lag=0.3), run_time=1.2)
            c.wait_until("each moves")
            self.play(*[GrowArrow(a) for a in d.arcs], *appear(d.pp, d.qp, shift=None, lag=0.2), run_time=1.6)
            c.wait_until("labelled")
            self.play(*appear(*d.labels, shift=None, lag=0.3), run_time=1.2)
            settle(self, d)

    # -------------------------------------------------------------- c2.step.2
    def clip2(self):
        d = self.d
        with self.say("c2.step.2") as c:
            self.play(*during(disappear(self.card, self.title, self.b1), 0, 0.5),
                      *during([d.animate.shift(1.05 * UP)], 0.4, 1.0), run_time=1.6)
            KX, CX = 2.15, 2.45
            ys = (1.7, 0.6, -0.5, -1.75)

            def kw(s, y):
                return T(s, 40, DIM).move_to(_p(0, y)).align_to(_p(KX, 0), RIGHT)

            def clause(m, y):
                return m.move_to(_p(0, y)).align_to(_p(CX, 0), LEFT)

            c1 = MathTex("x_p = x_q", ",", font_size=56)
            c1[0].set_color(BLUE)
            c2 = MathTex("y_p = y_q", font_size=56, color=GREEN)
            c3 = MathTex("p'", r"\equiv", "q'", font_size=56)
            c4 = MathTex("p", r"\equiv", "q", font_size=56)
            for m in (c3, c4):
                m[0].set_color(YELLOW)
                m[1].set_color(GOLD)
                m[2].set_color(YELLOW)
            rows = [clause(m, y) for m, y in zip((c1, c2, c3, c4), ys)]
            k_if, k_and, k_then = kw("if", ys[0]), kw("and", ys[2]), kw("then", ys[3])
            for k, m in ((k_if, c1), (k_and, c3), (k_then, c4)):
                k.align_to(m, DOWN)

            c.wait_until("inputs")
            self.play(*appear(k_if, c1, lag=0.2), *flash([lb.inp for lb in d.labels], color=BLUE, time_width=1.5),
                      run_time=1.3)
            c.wait_until("outputs")
            self.play(*appear(c2), *flash([lb.out for lb in d.labels], color=GREEN, time_width=1.5), run_time=1.3)
            c.wait_until("nexts")
            self.play(*appear(k_and, c3, lag=0.2), GrowFromCenter(d.eq_next), run_time=1.5)
            c.wait_until("are equivalent")
            self.play(*appear(k_then, c4, lag=0.2), GrowFromCenter(d.eq_pq),
                      run_time=min(1.5, max(0.8, c.until("each") - 0.1)))
            settle(self, d, add=[d.eq_next, d.eq_pq])
            self.rule = [k_if, k_and, k_then, c1, c2, c3, c4]

            c.wait_until("each")
            f = fan_left(d)
            tag0 = MathTex("x = 0", font_size=40, color=BLUE).next_to(d.pp, UP, buff=0.75)
            tag1 = MathTex("x = 1", font_size=40, color=BLUE).next_to(f.circs[0], UP, buff=0.75)
            self.play(*[GrowArrow(a) for a in f.arcs], *appear(*f.circs, shift=None),
                      *appear(*f.labels, tag0, tag1, lag=0.15), GrowFromCenter(f.eq), run_time=1.8)
            self.fan = [*f.circs, *f.arcs, *f.labels, f.eq, tag0, tag1]

    # -------------------------------------------------------------- c2.step.3
    def clip3(self):
        d = self.d
        with self.say("c2.step.3") as c:
            k = 0.75
            ctr = center_for(d, k, _p(-5.9, ROW_Y[0]))
            self.dk = k
            # p's row (the question is only asked: the screen holds through the pause)
            c.wait_until("the output sequence from state")
            pb = [_box(RX0 + i * RP, ROW_Y[0]) for i in range(NBOX)]
            self.play(*during(disappear(*self.rule, *self.fan), 0, 0.35),
                      *during([d.animate.scale(k).move_to(ctr)], 0.3, 0.75),
                      *during(appear(*pb, shift=None, lag=0.06), 0.55, 1.0), run_time=2.2)
            c.wait_until("first output")
            yp = MathTex("y_p", font_size=40, color=GREEN).next_to(pb[0], UP, buff=0.15)
            self.play(*[b.animate.shift(GAP * RIGHT) for b in pb[1:]], run_time=1.0)
            self.play(*appear(yp), run_time=0.8)
            c.wait_until("followed")
            br_p = _brace(pb[1:], +1)
            lab_p = _next_to_brace(_seq_label("p", 1), br_p, +1)
            self.play(GrowFromCenter(br_p), run_time=0.9)
            c.wait_until("from its next state")
            self.play(*appear(lab_p), run_time=1.0)

            # q's row, built the same way in one go
            c.wait_until("same goes")
            qb = [_box(RX0 + i * RP + (GAP if i else 0), ROW_Y[1]) for i in range(NBOX)]
            yq = MathTex("y_q", font_size=40, color=GREEN).next_to(qb[0], DOWN, buff=0.15)
            br_q = _brace(qb[1:], -1)
            lab_q = _next_to_brace(_seq_label("q", 1), br_q, -1)
            self.play(*appear(*qb, shift=None, lag=0.04), run_time=1.0)
            self.play(*appear(yq, br_q, lab_q, shift=0.2 * UP, lag=0.2), run_time=1.0)

            # match
            c.wait_until("match")
            eqs = [MathTex("=", font_size=56, color=GOLD).rotate(PI / 2).move_to(_p(pb[0].get_x(), 0))]
            self.play(GrowFromCenter(eqs[0]), FlashAround(VGroup(pb[0], qb[0]), color=GOLD, time_width=1.5),
                      run_time=1.2)
            c.wait_until("next states are equivalent")
            eqv = _equiv(_p(br_p.get_x(), 0), 60)
            self.play(GrowFromCenter(eqv), run_time=1.0)
            c.wait_until("whole sequences")
            self.play(*recolor(pb + qb, GOLD), FlashAround(VGroup(*pb), color=GOLD, time_width=1.5),
                      FlashAround(VGroup(*qb), color=GOLD, time_width=1.5), run_time=1.6)

            # repeat: the bracket splits again, twice
            c.wait_until("repeat")
            for j, cue in ((2, None), (3, "and so on")):
                if cue:
                    c.wait_until(cue)
                nb_p = _brace([b.copy().shift(GAP * RIGHT) for b in pb[j:]], +1)
                nb_q = _brace([b.copy().shift(GAP * RIGHT) for b in qb[j:]], -1)
                nl_p = _next_to_brace(_seq_label("p", j), nb_p, +1)
                nl_q = _next_to_brace(_seq_label("q", j), nb_q, -1)
                e = MathTex("=", font_size=56, color=GOLD).rotate(PI / 2).move_to(_p(pb[j - 1].get_x(), 0))
                rt = 1.6 if j == 2 else 1.2
                self.play(*[b.animate.shift(GAP * RIGHT) for b in pb[j:] + qb[j:]],
                          Transform(br_p, nb_p), Transform(br_q, nb_q),
                          *swap(lab_p, nl_p, shift=None), *swap(lab_q, nl_q, shift=None),
                          eqv.animate.move_to(_p(nb_p.get_x(), 0)),
                          *during([GrowFromCenter(e)], 0.5, 1.0), run_time=rt)
                lab_p, lab_q = nl_p, nl_q
                eqs.append(e)
            dots = [T("…", 44, GOLD).next_to(pb[-1], RIGHT, buff=0.25), T("…", 44, GOLD).next_to(qb[-1], RIGHT, buff=0.25)]
            self.play(*appear(*dots, shift=None), run_time=0.8)

    # -------------------------------------------------------------- c2.step.4
    def clip4(self):
        d = self.d
        with self.say("c2.step.4") as c:
            k = 0.8
            ctr = center_for(d, k / self.dk, _p(2.1, 0.5))
            b2 = bullet(BULLET2, 30).move_to(_p(0, 2.95))
            sweep_clear(self, d.animate.scale(k / self.dk).move_to(ctr), *appear(b2, shift=None), keep=[d],
                        run_time=1.4)  # early: the slide's last bullet, read whole

            # row matching: a copy of the diagram, p' and q' merged
            c.wait_until("rowmatch")
            dc = pq_diagram(marks=True)
            dc.scale(k)
            dc.move_to(center_for(dc, 1, _p(-4.6, 0.5)))
            self.play(*appear(dc, shift=None), run_time=1.0)
            r = dc.pp.circle.width / 2
            mid = (dc.pp.get_center() + dc.qp.get_center()) / 2
            new_arcs = [_arc(dc.p.get_center(), mid, r), _arc(dc.q.get_center(), mid, r)]
            l0 = dc.labels[0].copy()
            l1 = dc.labels[1].copy()
            l0.move_to(new_arcs[0].get_center() + 0.42 * UP + 0.1 * RIGHT)
            l1.move_to(new_arcs[1].get_center() + 0.42 * DOWN + 0.1 * RIGHT)
            detach(self, dc.eq_next, dc.qp.letter)
            self.play(*during(disappear(dc.eq_next, dc.qp.letter), 0, 0.35),
                      *during([dc.pp.letter.animate.move_to(mid), dc.qp.circle.animate.move_to(mid),
                               dc.pp.circle.animate.move_to(mid).set_stroke(GOLD, 4),
                               Transform(dc.arcs[0], new_arcs[0]), Transform(dc.arcs[1], new_arcs[1]),
                               dc.labels[0].animate.move_to(l0), dc.labels[1].animate.move_to(l1)], 0.35, 0.8),
                      run_time=1.6)
            dc.remove(dc.qp)
            self.remove(dc.qp.circle)
            cap_rm = MathTex(r"\text{row matching: }", "p'", "=", "q'", font_size=40)
            cap_rm[1].set_color(YELLOW)
            cap_rm[2].set_color(GOLD)
            cap_rm[3].set_color(YELLOW)
            cap_rm.move_to(_p(dc.p.get_x() + 1.3, -2.85))
            self.play(*appear(cap_rm), FlashAround(dc.pp, color=GOLD, time_width=1.5), run_time=1.0)

            c.wait_until("here")
            cap_eq = MathTex(r"\text{equivalence: }", "p'", r"\equiv", "q'", font_size=40)
            cap_eq[1].set_color(YELLOW)
            cap_eq[2].set_color(GOLD)
            cap_eq[3].set_color(YELLOW)
            cap_eq.move_to(_p(d.p.get_x() + 1.3, -2.85))
            self.play(*appear(cap_eq), FlashAround(d.eq_next, color=GOLD, time_width=1.5), run_time=1.3)

            # A and D
            c.wait_until("ad")
            tbl = S2.dim_table()
            lanes = compact_lanes().move_to(_p(1.3, 0)).to_edge(UP, buff=0.5)
            detach(self, d.eq_pq, d.eq_next)
            f = 1 / k
            ctr = center_for(d, f, _p(1.2, 0.3))
            others = [m for m in self.mobjects if m is not d]
            self.play(*during(disappear(*others), 0, 0.4), *during([d.animate.scale(f).move_to(ctr)], 0.3, 0.8),
                      *during([FadeIn(tbl)], 0.5, 1.0), *during(appear(lanes, shift=None), 0.55, 1.0), run_time=1.8)
            out_pos = lambda st, side: st.get_center() + _p(0, 0.78 * side)  # noqa: E731

            def letter_fly(st, name, src, run=True):
                """The circle's letter becomes the table's: its cell flashes, the old letter rises out,
                the new one rises in (a copy can't leave the table without crossing other cells)."""
                new = T(name, 40).move_to(st.circle)
                old = st.letter
                detach(self, old)
                return new, [*swap(old, new), FlashAround(src, color=YELLOW, time_width=1.5)]

            def fly(src, dst, arc=None):   # outputs: the same cell flash, the value drops in
                return [*appear(dst), FlashAround(src, color=GREEN, time_width=1.5)]

            ra, rd = tbl.row_of("A"), tbl.row_of("D")
            boxes = [Rectangle(width=tbl.rows[r].width + 0.3, height=0.34).move_to(tbl.rows[r])
                     .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.18).set_z_index(-1) for r in (ra, rd)]
            self.play(*[FadeIn(b) for b in boxes], run_time=0.8)
            nA, a1 = letter_fly(d.p, "A", tbl.cell(ra, 0))
            nD, a2 = letter_fly(d.q, "D", tbl.cell(rd, 0))
            oA = T("0", 34, GREEN).move_to(out_pos(d.p, 1))
            oD = T("0", 34, GREEN).move_to(out_pos(d.q, -1))
            self.play(*a1, *a2, *fly(tbl.cell(ra, 3), oA, arc=-PI / 5), *fly(tbl.cell(rd, 3), oD, arc=-PI / 5),
                      run_time=1.6)

            c.wait_until("on input zero")
            z = [T("0", 36, BLUE).move_to(lb) for lb in d.labels]
            detach(self, *d.labels)
            self.play(*swap(d.labels[0], z[0]), *swap(d.labels[1], z[1]), run_time=1.0)
            c.wait_until("goes to dee")
            nD2, a3 = letter_fly(d.pp, "D", tbl.cell(ra, 1))
            oD2 = T("0", 34, GREEN).move_to(out_pos(d.pp, 1))
            self.play(*a3, *fly(tbl.cell(rd, 3), oD2, arc=-PI / 5), run_time=1.5)
            c.wait_until("goes back")
            nA2, a4 = letter_fly(d.qp, "A", tbl.cell(rd, 1))
            oA2 = T("0", 34, GREEN).move_to(out_pos(d.qp, -1))
            self.play(*a4, *fly(tbl.cell(ra, 3), oA2, arc=-PI / 5), run_time=1.5)

            c.wait_until("onone")
            fl = fan_left(d, letters=None, labels=False)
            nC = T("C", 40).move_to(fl.circs[0])
            nE = T("E", 40).move_to(fl.circs[1])
            ones = [T("1", 36, BLUE).next_to(fl.arcs[0], UP, buff=0.12),
                    T("1", 36, BLUE).next_to(fl.arcs[1], DOWN, buff=0.12)]
            oC = T("1", 34, GREEN, weight=BOLD).move_to(out_pos(fl.circs[0], 1))
            oE = T("1", 34, GREEN, weight=BOLD).move_to(out_pos(fl.circs[1], -1))
            rc, re_ = tbl.row_of("C"), tbl.row_of("E")
            self.play(*[GrowArrow(a) for a in fl.arcs], *appear(*fl.circs, *ones, shift=None),
                      *appear(nC, nE, shift=None), *flash([tbl.cell(ra, 2), tbl.cell(rd, 2)], time_width=1.5),
                      *fly(tbl.cell(rc, 3), oC, arc=-PI / 5), *fly(tbl.cell(re_, 3), oE, arc=-PI / 5),
                      run_time=1.8)

            c.wait_until("still be equivalent")
            qs = []
            for a, b in ((d.pp, d.qp), (fl.circs[0], fl.circs[1])):
                m = (a.get_center() + b.get_center()) / 2
                e = _equiv(m, 56)
                qm = T("?", 40, GOLD).next_to(e, RIGHT, buff=0.22)
                qs.append(VGroup(e, qm))
            self.play(*appear(*qs, shift=None, lag=0.3), run_time=1.2)
        self.wait(1.2)   # the open question holds a moment before the fade
