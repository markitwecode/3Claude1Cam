"""Chapter 9, scene 4: Exercise 13, pair four (LEFT JOIN ... IS NULL vs NOT IN). Clips c9.notin.1 – c9.notin.4.

Layout: s2's growing database top-left (fixed); pair 4 as the hero on the right (s2's place, Code 34) in
clip 1, then shrunk to Code 28 at the top right with each query's result card beside it. The bottom
band (y -0.9 .. -3.5, full width) is the work area: the LEFT JOIN table, then the NOT IN chains (one row
per r row, pills in s2's pill style), then ch2's trap picture, then the result cards side by side
(NOT IN ⊆ LEFT JOIN = NOT EXISTS) with the NOT EXISTS query bottom-left. Ends empty.

EXPORTS: recap_r4(): row 3's NOT IN chain (`30 <> 10` AND `30 <> 10` AND `30 <> NULL`, PINK outline)
over the NOT IN card (RED "0 rows") beside the NOT EXISTS card (GREEN 2, 3), labelled; static, at ORIGIN.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch9_s2_pairs")
DER = load_scene("ch2_s6_derive")
H31 = load_scene("ch3_s1_hook")

F = 28 / 34                       # hero shrink for clips 2-4
UL0 = np.array([-1.0, 2.85, 0])   # pair_code's top-left
LIFT = 0.65 * UP                  # new top 3.5
CARD_X = 5.85
LJ_TOP, NI_TOP = 3.5, 1.244
REL_Y = 1.6

# LEFT JOIN table
JX = (-3.6, -2.4, -1.0, 0.2)
VX = 2.4
JH_Y = -1.05
JROW_Y = (-1.6, -2.15, -2.7, -3.25)

# NOT IN chains
LAB_X = -6.55
CH_X = -4.25
CROW_Y = (-1.62, -2.4, -3.18)
RY = (10, None, 30)
SY = (10, 10, None)

# clip 4's result row
ROW_TOP = -0.75
NI_X, SUB_X, LJ_X, EQ_X, NE_X = -0.2, 1.05, 2.3, 3.6, 4.9

NE_SRC = "SELECT r.x FROM r\nWHERE NOT EXISTS\n  (SELECT 1 FROM s\n   WHERE s.y = r.y);"


def sval(v):
    return "NULL" if v is None else str(v)


def pill(text, color):
    return S2.paint(S2.pill(text), color)


def link_color(a, b):
    if a is None or b is None:
        return PINK
    return RED if a == b else GREEN


def chain(k, y=0.0):
    """Row k's NOT IN chain, all three links: VGroup p0, AND, p1, AND, p2 (left edge at x 0)."""
    items = []
    for j, b in enumerate(SY):
        if j:
            items.append(Mono("AND", 28, BLUE))
        items.append(pill(f"{sval(RY[k])} <> {sval(b)}", link_color(RY[k], b)))
    g = VGroup(*items).arrange(RIGHT, buff=0.15)
    g.shift(np.array([-g.get_left()[0], y - g.get_y(), 0]))
    return g


def outline(mobs, color):
    g = VGroup(*mobs)
    box = RoundedRectangle(corner_radius=0.16, width=g.width + 0.2, height=0.68).set_stroke(color, 3)
    return box.move_to(g)


def row_label(k):
    return Mono(f"({k + 1}, {sval(RY[k])})", 28, t2c={"NULL": PINK})


def empty_card():
    """NOT IN's card emptied: the header row and DuckDB's footer `0 rows`, RED."""
    h = S2.COLH_H + 0.1
    box = Rectangle(width=1.2, height=h).set_stroke(BLUE, 2.5).set_fill(BG, 0)
    box.move_to([0, -h / 2, 0])
    head = Mono("x", 28, DIM).move_to(box)
    foot = Mono("0 rows", 28, RED).next_to(box, DOWN, buff=0.15)
    g = VGroup(box, head, foot)
    g.box, g.head, g.foot = box, head, foot
    return g


def recap_r4():
    ch = chain(2)
    ol = outline(ch, PINK)
    top = VGroup(ch, ol).move_to([0, 1.2, 0])
    ni = S2.place_top(empty_card(), -1.6, 0.4)
    ne = S2.place_top(S2.result_card([2, 3]), 1.6, 0.4)
    ne.vals.set_color(GREEN)
    ni_l = Mono("NOT IN", 28, YELLOW).next_to(ni, DOWN, buff=0.3)
    ne_l = Mono("NOT EXISTS", 28, YELLOW).move_to([ne.box.get_x(), ni_l.get_y(), 0])
    return VGroup(top, ni, ne, ni_l, ne_l).move_to(ORIGIN)


class Ch9S4NotIn(NarratedScene):
    def construct(self):
        self.pair4()
        self.null_r()
        self.null_s()
        self.verdict()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c9.notin.1
    def pair4(self):
        with self.say("c9.notin.1") as c:
            d = S2.db([(1, 10), (3, 30)], [(10, 99), (10, 5)], r_slots=[0, 2])
            self.d = d
            st = S2.strip(4)
            self.st = st
            self.play(*appear(d.r, d.s, st, lag=0.3, shift=None), run_time=1.2)  # early: the scene's board
            hero = S2.pair_code(4)
            self.a, self.b = hero.a, hero.b
            self.play(*appear(hero.a, hero.b, lag=0.4, shift=None),  # early: the pair, shown whole
                      run_time=min(1.4, c.until("lj")))
            c.wait_until("lj")
            isn = hero.a.find("IS NULL")
            self.play(*recolor(isn, YELLOW), FlashUnder(isn, color=YELLOW, run_time=1.4, time_width=1.5),
                      run_time=1.4)
            c.wait_until("ni")
            nin = hero.b.find("NOT IN")
            self.play(*recolor(nin, YELLOW), FlashUnder(nin, color=YELLOW, run_time=1.4, time_width=1.5),
                      run_time=1.4)
            c.wait_until("ask")
            ask = T("Same result?", 40, YELLOW).move_to([2.4, -2.35, 0])
            self.ask = ask
            self.play(*appear(ask), run_time=0.9)
            c.wait_until("hint")
            hint = DER.and_chain().scale(0.7).move_to([2.4, -3.15, 0])
            self.hint = hint
            self.play(*during(appear(hint, shift=None), 0, 0.45),  # early: part two's AND chain, a callback picture
                      time_span(FlashAround(hint.null_part, color=PINK, time_width=1.5), 0.7, 1.6), run_time=1.6)

    # ------------------------------------------------------------ c9.notin.2
    def null_r(self):
        d, a, b = self.d, self.a, self.b
        with self.say("c9.notin.2") as c:
            ins = S2.insert_code("INSERT INTO r VALUES\n  (2, NULL);")
            mv = [m.animate.scale(F, about_point=UL0).shift(LIFT) for m in (a, b)]
            self.play(*during(disappear(self.ask, self.hint, self.st), 0, 0.4),
                      *during(mv, 0.2, 0.8),
                      *during(appear(ins, shift=None), 0.55, 1), run_time=1.6)
            c.wait_until("the row two")
            row = d.r.make_row(1, (2, None))
            self.play(*flash([ins.find("2"), ins.find("NULL", line=1)]),
                      *during(appear(row, shift=0.3 * RIGHT), 0.3, 1), run_time=1.3)
            settle(self, d.r, add=[row])
            d.r.rows[1] = row

            # -- {ljnull}: the LEFT JOIN table
            c.wait_until("ljnull")
            head = VGroup(*[Mono(t, 28, DIM).move_to([x, JH_Y, 0]) for t, x in zip(("r.x", "r.y", "s.y", "s.z"), JX)],
                          Mono("s.y IS NULL", 28, YELLOW).move_to([VX, JH_Y, 0]))
            hdiv = Line([JX[0] - 0.6, JH_Y - 0.3, 0], [VX + 1.4, JH_Y - 0.3, 0]).set_stroke(DIM, 1.5)
            vals = ((1, 10, 10, 99), (1, 10, 10, 5), (2, None), (3, 30, None, None))
            jrows = []
            for vs, y in zip(vals, JROW_Y):
                r = VGroup(*[S2.value_text(v).move_to([x, y, 0]) for v, x in zip(vs, JX)])
                if len(vs) == 4:
                    r.set_opacity(0.4)
                jrows.append(r)
            self.play(*during(disappear(ins), 0, 0.4),
                      *during(appear(VGroup(head, hdiv), *jrows, lag=0.15, shift=None), 0.3, 1),
                      run_time=min(1.6, c.until("since null equals ten")))
            c.wait_until("since null equals ten")
            pp = VGroup(pill("NULL = 10", PINK), pill("NULL = 10", PINK)).arrange(RIGHT, buff=0.15)
            pp.move_to([JX[2] - 0.6, JROW_Y[2], 0], aligned_edge=LEFT)
            self.play(*appear(pp, shift=None), run_time=1.0)
            c.wait_until("padded")
            pad = VGroup(*[S2.value_text(None).move_to([x, JROW_Y[2], 0]) for x in JX[2:]])
            self.play(*swap(pp, pad), run_time=1.0)
            marks = []
            for k, y in enumerate(JROW_Y):
                m = (check_mark() if k >= 2 else cross_mark()).move_to([VX, y, 0])
                marks.append(m)
            self.play(*set_alpha([jrows[0], jrows[1], jrows[3]], 1),
                      *appear(*marks, lag=0.1, shift=None), run_time=1.0)
            self.ljt = [head, hdiv, *jrows, pad, *marks]

            # -- {ninull}: the NOT IN chains
            c.wait_until("ninull")
            c.wait_until("twice")
            labs = [row_label(k).move_to([LAB_X, y, 0], aligned_edge=LEFT) for k, y in enumerate(CROW_Y)]
            chains = [chain(k, y).shift(CH_X * RIGHT) for k, y in enumerate(CROW_Y)]
            self.labs, self.chains = labs, chains
            sweep_clear(self, *during(appear(*labs, lag=0.2, shift=None), 0.5, 1),
                        keep=[d.r, d.s, a, b], run_time=1.3)
            self.play(*appear(chains[1][:3], shift=None), *flash([d.r.cell(1, 1)], color=PINK),
                      run_time=min(1.2, c.until("both links")))
            c.wait_until("both links")
            ols = [None, outline(chains[1][:3], PINK), None]
            self.play(GrowFromCenter(ols[1]), *set_alpha([labs[1]], 0.4), run_time=1.0)
            ols[0] = outline(chains[0][:3], RED)
            ols[2] = outline(chains[2][:3], GREEN)
            self.play(*appear(chains[0][:3], chains[2][:3], lag=0.3, shift=None), run_time=1.0)
            self.play(GrowFromCenter(ols[0]), GrowFromCenter(ols[2]),
                      *set_alpha([labs[0]], 0.4), *recolor(labs[2], GREEN),
                      run_time=min(1.0, c.until("res1")))
            self.ols = ols

            # -- {res1}: the results
            c.wait_until("res1")
            ljc = S2.place_top(S2.result_card([2, 3]), CARD_X, LJ_TOP)
            self.ljc = ljc
            self.play(*appear(VGroup(ljc.box, ljc.head, ljc[1]), shift=None), run_time=0.7)
            self.play(*appear(*ljc.vals, lag=0.4, shift=None), run_time=1.0)
            settle(self, ljc, add=list(ljc.vals))
            c.wait_until("not in returns")
            nic = S2.place_top(S2.result_card([3], slots=2), CARD_X, NI_TOP)
            self.nic = nic
            self.play(*appear(nic, shift=None), run_time=0.9)
            rel = MathTex(r"\neq", font_size=60, color=RED).move_to([CARD_X, REL_Y, 0])
            self.rel = rel
            self.play(*appear(rel, shift=None), run_time=min(0.8, c.until()))

    # ------------------------------------------------------------ c9.notin.3
    def null_s(self):
        d = self.d
        with self.say("c9.notin.3") as c:
            ins = S2.insert_code("INSERT INTO s VALUES\n  (NULL, 1);")
            self.play(*appear(ins, shift=None), run_time=0.9)
            c.wait_until("the row null")
            row = d.s.make_row(2, (None, 1))
            self.play(*flash([ins.find("NULL", line=1), ins.find("1", line=1)]),
                      *during(appear(row, shift=0.3 * DOWN), 0.3, 1), run_time=1.3)
            settle(self, d.s, add=[row])
            d.s.rows[2] = row

            # -- {ljsame}
            c.wait_until("ljsame")
            np_ = pill("NULL = …", PINK).move_to([d.s.x, -0.88, 0])
            self.play(*during(disappear(ins), 0, 0.45), *during(appear(np_, shift=None), 0.45, 1),
                      run_time=1.2)
            nothing = T("matches nothing", 30, DIM).next_to(np_, RIGHT, buff=0.3)
            c.wait_until(own_word=nothing, cue="matches nothing")
            self.play(*appear(nothing, shift=None), run_time=0.9)
            c.wait_until("still returns")
            self.play(FlashAround(self.ljc, color=GREEN, run_time=1.5, time_width=1.5), run_time=1.5)

            # -- {chain}: every chain grows a NULL link
            c.wait_until("chain")
            self.play(*disappear(np_, nothing), run_time=0.7)
            self.play(*appear(*[ch[3:] for ch in self.chains], lag=0.3, shift=None), run_time=1.5)
            new_ols = [outline(ch, col) for ch, col in zip(self.chains, (RED, PINK, PINK))]
            self.play(*[ReplacementTransform(o, n) for o, n in zip(self.ols, new_ols)],
                      *set_alpha([self.labs[2]], 0.4), run_time=1.3)
            self.ols = new_ols

            # -- {empty}
            c.wait_until("empty")
            emp = S2.place_top(empty_card(), CARD_X, NI_TOP)
            self.play(*swap(self.nic, emp), run_time=1.2)
            self.nic = emp
            self.play(FlashAround(emp.foot, color=RED, run_time=1.2, time_width=1.5), run_time=1.2)

            # -- {trap}: part two's picture, small
            c.wait_until("trap")
            trap = H31.trap_back().scale(0.7).move_to([0.3, -2.2, 0])
            self.trap = trap
            sweep_clear(self, time_span(FadeIn(trap), 0.6, 1.3),
                        keep=[d.r, d.s, self.a, self.b, self.ljc, self.nic, self.rel], run_time=1.3)

    # ------------------------------------------------------------ c9.notin.4
    def verdict(self):
        d, a, b = self.d, self.a, self.b
        nulls = [d.r.cell(1, 1), d.s.cell(2, 0)]
        with self.say("c9.notin.4") as c:
            cap = T("no NULL in either y column: always the same", 32, GREEN).move_to([0, -1.9, 0])
            self.play(*swap(self.trap, cap), *set_alpha(nulls, DIMMED), run_time=1.3)

            # -- {lose}: NOT IN ⊆ LEFT JOIN
            c.wait_until("lose")
            ljc, nic = self.ljc, self.nic
            paths = []
            for card, x in ((nic, NI_X), (ljc, LJ_X)):
                c0 = card.get_center()
                dy = ROW_TOP - card.box.get_top()[1]
                paths.append(VMobject().set_points_as_corners([c0, c0 + dy * UP, c0 + dy * UP + (x - card.box.get_x()) * RIGHT]))
            self.play(*during(disappear(self.rel), 0, 0.25),
                      *during([cap.animate.scale(30 / 32).move_to([2.25, -3.35, 0])], 0, 0.35),
                      *during([MoveAlongPath(nic, paths[0])], 0.25, 0.75),
                      *during([MoveAlongPath(ljc, paths[1])], 0.45, 1), run_time=2.2)
            mid = ROW_TOP - ljc.box.height / 2
            sub = MathTex(r"\subseteq", font_size=60, color=YELLOW).move_to([SUB_X, mid, 0])
            lab_y = ljc.box.get_bottom()[1] - 0.32
            ni_l = Mono("NOT IN", 26, YELLOW).move_to([NI_X, lab_y, 0])
            lj_l = Mono("LEFT JOIN", 26, YELLOW).move_to([LJ_X, lab_y, 0])
            self.play(*appear(ni_l, sub, lj_l, lag=0.3, shift=None), run_time=min(1.4, c.until("exists")))

            # -- {exists}
            c.wait_until("exists")
            ne = Code(NE_SRC, size=28)
            ne.shift(np.array([-6.55 - ne.get_left()[0], ROW_TOP - ne.get_top()[1], 0]))
            self.play(*appear(ne, shift=None), run_time=1.0)
            nec = S2.place_top(S2.result_card([2, 3]), NE_X, ROW_TOP)
            nec.vals.set_color(GREEN)
            eq = MathTex("=", font_size=60, color=GREEN).move_to([EQ_X, mid, 0])
            ne_l = Mono("NOT EXISTS", 26, YELLOW).move_to([NE_X, lab_y, 0])
            self.play(*appear(eq, nec, ne_l, lag=0.3, shift=None), run_time=min(1.4, c.until("alarm")))

            # -- {alarm}: check both y columns
            c.wait_until("alarm")
            boxes = []
            for card in (d.r, d.s):
                j = 1 if card is d.r else 0
                top = card.top - S2.HEAD_H
                bot = card.box.get_bottom()[1]
                boxes.append(Rectangle(width=1.05, height=top - bot - 0.08).set_stroke(YELLOW, 4)
                             .move_to([card.col_x(j), (top + bot) / 2, 0]))
            self.play(*set_alpha(nulls, 1), *[GrowFromCenter(bx) for bx in boxes],
                      *recolor(b.find("NOT IN"), YELLOW), run_time=1.2)
            self.play(*flash(nulls, color=PINK), run_time=1.2)
