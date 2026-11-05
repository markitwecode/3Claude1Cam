"""Chapter 2, scene 6: why NOT IN can never be true. Clips c2.derive.1 – c2.derive.6.

Exports (for the recap and ch3):
  and_chain()       The Kid's AND chain: VGroup(true_part, and_, null_part) at ORIGIN:
                    GREEN "2,685 links: TRUE" AND PINK "20,494 links: NULL".
  fixed_query()     the death-year query with the IS NOT NULL line (Code 30, centred at y=2.6).
  final_results()   the end shot: the four GREEN movie cards (column, left) beside NOT IN's
                    RED "0 rows" result box (right). .cards (list) .result
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

S1 = load_scene("ch2_s1_hook")
S2 = load_scene("ch2_s2_absent")
S3 = load_scene("ch2_s3_notin")
S4 = load_scene("ch2_s4_trap")
S5 = load_scene("ch2_s5_logic")
SCH = load_scene("ch1_s2_schema")

HEAD_SRC = "c NOT IN (v1, v2, …, vn)"
EXP_SRC = "(c <> v1) AND (c <> v2) AND … AND (c <> vn)"
FIX_SRC = """SELECT title FROM movies
WHERE year NOT IN (SELECT deathyear FROM people
                   WHERE deathyear IS NOT NULL);"""
FOUR = [("The Kid", 1921), ("Sherlock Jr.", 1924), ("The General", 1926),
        ("It Happened One Night", 1934)]

LANE_Y = 2.5
GATE_X = 0.6
CARD_X = -3.0
CHAIN_Y = 0.6
CHAIN_X = -0.7
COL_W = 5.9


# ---------------------------------------------------------------- shared looks

def pill(text, color, size=28):
    """One link of a chain: a comparison in a rounded box tinted by its truth value."""
    lab = Mono(text, size, FG)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.4, height=0.62)
    box.set_stroke(color, 3).set_fill(color, 0.15)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def summary(text, color, t2c):
    lab = T(text, 32, FG, t2c=t2c)
    box = RoundedRectangle(corner_radius=0.16, width=lab.width + 0.5, height=0.66)
    box.set_stroke(color, 3).set_fill(color, 0.15)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def and_word():
    return Mono("AND", 28, BLUE)


def and_chain():
    g = summary("2,685 links: TRUE", GREEN, {"2,685": GOLD, "TRUE": GREEN})
    a = and_word()
    p = summary("20,494 links: NULL", PINK, {"20,494": GOLD, "NULL": PINK})
    ch = VGroup(g, a, p).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
    ch.true_part, ch.and_, ch.null_part = g, a, p
    return ch


def fixed_query():
    return Code(FIX_SRC, size=30).move_to([0, 2.6, 0])


def _old_query(fixed):
    q = Code(S1.QUERY, size=30)
    q.align_to(fixed, LEFT).align_to(fixed, UP)
    return q


def _slot():
    rect = RoundedRectangle(corner_radius=0.15, width=COL_W, height=0.82).set_stroke(DIM, 2.5)
    q = T("?", 44, GOLD).move_to(rect)
    s = VGroup(rect, q)
    s.rect, s.q = rect, q
    return s


def slot_column(center):
    col = VGroup(*[_slot() for _ in FOUR]).arrange(DOWN, buff=0.18).move_to(center)
    return col


def green_card(title, year):
    return S2.movie_card(title, year, size=28, color=GREEN, min_width=COL_W - 0.2)


def _result_box():
    r = S1._result().scale(1.6)
    return r


def final_results():
    col = slot_column([-2.3, 0, 0])
    cards = [green_card(t, y).move_to(s) for (t, y), s in zip(FOUR, col)]
    res = _result_box().move_to([3.7, 0, 0])
    g = VGroup(*cards, res)
    g.cards, g.result = cards, res
    return g


def bell(color=RED):
    dome = Arc(radius=0.18, start_angle=0, angle=PI, arc_center=[0, 0.1, 0])
    left = Line([-0.18, 0.1, 0], [-0.27, -0.18, 0])
    right = Line([0.18, 0.1, 0], [0.27, -0.18, 0])
    rim = Line([-0.33, -0.18, 0], [0.33, -0.18, 0])
    knob = Line([0, 0.28, 0], [0, 0.36, 0])
    g = VGroup(dome, left, right, rim, knob).set_stroke(color, 4)
    clap = Dot([0, -0.27, 0], radius=0.06, color=color)
    return VGroup(g, clap)


def compress(scene, pills, extras, target):
    """Several links collapse into one summary pill: texts fade, boxes merge, summary fades in."""
    texts = [p.label for p in pills] + list(extras)
    boxes = VGroup(*[p.box.copy() for p in pills])
    for p in pills:
        scene.remove(*p.get_family())
    scene.add(*texts, boxes)
    return [*during(disappear(*texts), 0, 0.4),
            *during([ReplacementTransform(boxes, target.box)], 0.2, 0.8),
            *during(appear(target.label, shift=None), 0.6, 1)]


# ---------------------------------------------------------------- the scene

class Derive(NarratedScene):
    def hold(self, t):
        if t > 0.05:
            self.wait(t)

    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ clip 1: NOT IN = AND chain
    def clip1(self):
        with self.say("c2.derive.1") as c:
            head = Code(HEAD_SRC, size=48).move_to([0, 1.3, 0])
            exp = Code(EXP_SRC, size=34).move_to([0, -0.4, 0])
            self.play(*appear(head), run_time=1.0)  # early: the operator under discussion, named at once

            c.wait_until("differs")
            self.play(*appear(exp, shift=0.6 * DOWN), run_time=min(1.5, c.until("chain")))

            c.wait_until("chain")
            ne = [exp.find("<>", nth=i) for i in range(3)]
            dots = exp.find("…")
            self.play(*recolor(ne[0], YELLOW), FlashAround(ne[0], time_width=1.5), run_time=1.0)
            c.wait_until("second")
            self.play(*recolor(ne[1], YELLOW), FlashAround(ne[1], time_width=1.5), run_time=1.0)
            c.wait_until("and so on")
            self.play(FlashAround(dots, time_width=1.5), run_time=1.0)
            c.wait_until("very end")
            self.play(*recolor(ne[2], YELLOW), FlashAround(ne[2], time_width=1.5), run_time=1.0)

            c.wait_until("and")
            ands = [exp.find("AND", nth=i) for i in range(3)]
            lab = T("NOT IN: an AND chain", 32, FG, t2c={"AND": BLUE}).next_to(exp, DOWN, buff=0.5)
            self.play(*[a for g in ands for a in recolor(g, BLUE)], *flash(ands, color=BLUE),
                      *appear(lab), run_time=1.2)
            orl = S3.or_line()
            orlab = T("IN: an OR chain", 30, DIM).next_to(orl, RIGHT, buff=0.5)
            self.play(*appear(orl, orlab, shift=None, lag=0.3), run_time=1.0)  # early: pairs the parked OR line with its name
            self.c1 = (head, exp, lab, orl, orlab)

    # ------------------------------------------------------------ clip 2: The Kid's chain
    def clip2(self):
        with self.say("c2.derive.2") as c:
            kid = S4.kid_card().scale(1 / 1.2).move_to([CARD_X, LANE_Y, 0])
            gate = S5.where_gate(1.2).move_to([GATE_X, LANE_Y + 0.1, 0])
            slots = S1.four_slots().scale(0.55).move_to([4.4, LANE_Y, 0])
            s0 = slots.slots[0]
            ghost = T("The Kid", 28, DIM).move_to(s0.rect)
            s0.rect.set_stroke(GREEN)
            s0.remove(s0.q)
            s0.add(ghost)
            self.hold(c.until("green") - 1.9)
            sweep_clear(self, *appear(kid, gate, slots, lag=0.2, shift=None),  # early: the setting: The Kid, the WHERE gate, the four slots
                        run_time=1.8)

            final = and_chain().move_to([CHAIN_X, CHAIN_Y, 0])
            G, A, P = final.true_part, final.and_, final.null_part

            c.wait_until("green")
            gp = [pill(f"1921 <> {y}", GREEN) for y in (1977, 1984, 1958)]
            ga = [and_word() for _ in range(2)]
            gd = Mono("…", 32, GREEN)
            row = VGroup(gp[0], ga[0], gp[1], ga[1], gp[2], gd).arrange(RIGHT, buff=0.2)
            gd.shift(0.05 * RIGHT)
            row.move_to([0, CHAIN_Y, 0])
            self.play(*appear(gp[0], ga[0], gp[1], ga[1], gp[2], gd, lag=0.3, shift=None), run_time=2.2)

            c.wait_until("pink")
            self.play(*compress(self, gp, ga + [gd], G), run_time=1.5)
            self.remove(G.box, G.label)
            self.add(G)
            pp = pill("1921 <> NULL", PINK)
            pa = and_word()
            pd = Mono("…", 32, PINK)
            prow = VGroup(pp, pa, pd).arrange(RIGHT, buff=0.2)
            prow.align_to(P, LEFT).set_y(CHAIN_Y)
            self.play(*appear(A, pp, pa, pd, lag=0.3, shift=None), run_time=1.6)

            c.wait_until("need")
            self.play(*compress(self, [pp], [pa, pd], P), run_time=1.4)
            self.remove(P.box, P.label)
            self.add(P)
            cap = T("AND chain: TRUE only if every link is TRUE", 34, FG,
                    t2c={"AND": BLUE, "TRUE": GREEN}).move_to([0, -0.4, 0])
            self.play(*appear(cap), run_time=1.0)

            c.wait_until("one")
            grid = S5.truth_grids(complete=True).AND
            if grid.width > 6.0:
                grid.scale_to_fit_width(6.0)
            if grid.height > 2.6:
                grid.scale_to_fit_height(2.6)
            grid.move_to([0, -2.15, 0])
            self.play(*appear(grid, shift=0.3 * UP), run_time=1.0)  # early: the AND table, read as a whole
            cell = grid.cell("T", "N")
            c.wait_until("is null", nth=1)
            self.play(cell.box.animate.set_stroke(PINK, 4).set_fill(PINK, 0.35),
                      FlashAround(cell, color=PINK, time_width=1.5), run_time=1.2)

            c.wait_until("single")
            outline = SurroundingRectangle(final, buff=0.18, corner_radius=0.2).set_stroke(PINK, 3)
            verdict = Mono("NULL", 36, PINK).next_to(outline, RIGHT, buff=0.3)
            self.play(FlashAround(P, color=PINK, time_width=1.5), run_time=1.0)
            self.play(FadeIn(outline), *recolor([G.box], PINK), *appear(verdict, shift=None), run_time=1.4)

            c.wait_until("dropped")
            self.play(*S5.gate_bounce(gate, kid, PINK, run_time=1.6))
            self.remove(kid)
            q = T("?", 31, GOLD).move_to(s0.rect)
            self.play(*swap(ghost, q), s0.rect.animate.set_stroke(DIM), run_time=1.0)
            self.remove(q, *slots.get_family())
            s0.remove(ghost)
            s0.add(q)
            self.add(slots)
            self.c2 = dict(gate=gate, slots=slots, final=final, outline=outline, verdict=verdict,
                           cap=cap, grid=grid)

    # ------------------------------------------------------------ clip 3: The Gold Rush, 0 rows
    def clip3(self):
        d = self.c2
        gate = d["gate"]
        with self.say("c2.derive.3") as c:
            kidrow = VGroup(d["final"], d["outline"], d["verdict"])
            klab = T("The Kid", 30, YELLOW)
            tgt = kidrow.copy()
            VGroup(klab, tgt).arrange(RIGHT, buff=0.35).move_to([0, -2.6, 0])
            self.play(*during(disappear(d["cap"], d["grid"]), 0, 0.4),
                      *during([kidrow.animate.move_to(tgt)], 0.4, 1), run_time=1.6)
            self.play(*appear(klab, shift=None), run_time=0.8)  # early: names the parked chain

            rush = S2.movie_card("The Gold Rush", 1925).move_to([CARD_X, LANE_Y, 0])
            rush.align_to([-6.3, 0, 0], LEFT)
            r1 = pill("1925 <> 1977", GREEN)
            r2 = pill("1925 <> 1925", DIM)
            ra = [and_word() for _ in range(2)]
            rd = Mono("…", 32, FG)
            rrow = VGroup(r1, ra[0], r2, ra[1], rd).arrange(RIGHT, buff=0.2)
            glab = T("The Gold\nRush", 30, FG)
            VGroup(glab, rrow).arrange(RIGHT, buff=0.35)
            rout = SurroundingRectangle(rrow, buff=0.18, corner_radius=0.2).set_stroke(RED, 3)
            rver = Mono("FALSE", 36, RED).next_to(rout, RIGHT, buff=0.3)
            VGroup(glab, rrow, rout, rver).move_to([0, 0.5, 0])
            c.wait_until("Gold Rush")
            self.play(*appear(rush, shift=None), run_time=1.0)
            self.play(*appear(glab, shift=None), run_time=0.8)

            c.wait_until("nineteen twenty-five")
            self.play(*appear(r1, ra[0], r2, ra[1], rd, lag=0.3, shift=None), run_time=1.8)

            c.wait_until("two people")
            names = T("Jane Connelly · Jean C. Havez", 28, DIM).next_to(r2, DOWN, buff=0.25)
            self.play(r2.box.animate.set_stroke(RED).set_fill(RED, 0.2), FlashAround(r2, color=RED, time_width=1.5),
                      *appear(names), run_time=1.4)

            c.wait_until("false")
            self.play(FadeIn(rout), *appear(rver, shift=None), run_time=1.2)
            self.play(*S5.gate_bounce(gate, rush, RED, run_time=1.6))
            self.remove(rush)

            c.wait_until("right reason")
            ok = check_mark(GREEN).next_to(rver, DOWN, buff=0.3)
            self.play(FadeIn(ok, scale=0.6), run_time=0.8)

            c.wait_until("every")
            toks = [S2.movie_card(t, y, size=28).move_to([CARD_X, LANE_Y, 0]).align_to([-6.3, 0, 0], LEFT)
                    for t, y in FOUR[1:]]
            for i, tok in enumerate(toks):
                self.play(FadeIn(tok), run_time=0.3)
                self.play(*S5.gate_bounce(gate, tok, PINK, run_time=0.9 if i else 1.1))
                self.remove(tok)

            c.wait_until("None is true")
            res = _result_box().scale(0.65).move_to(d["slots"])
            self.play(*swap(d["slots"], res), run_time=1.2)
            self.c3 = res

    # ------------------------------------------------------------ clip 4: the tiny list
    def clip4(self):
        with self.say("c2.derive.4") as c:
            self.hold(c.until("three") - 1.4)
            sweep_clear(self, run_time=1.4)
            X0 = -6.0
            rows = []
            specs = [("3 NOT IN (1, 2, NULL)", "(3 <> 1) AND (3 <> 2) AND (3 <> NULL)", "NULL", PINK, 2.7),
                     ("1 IN (1, 2, NULL)", "(1 = 1) OR (1 = 2) OR (1 = NULL)", "true", GREEN, 0.75),
                     ("3 IN (1, 2, NULL)", "(3 = 1) OR (3 = 2) OR (3 = NULL)", "NULL", PINK, -1.2)]
            for h, e, r, col, y in specs:
                hc = Code(h, size=40).move_to([0, y, 0]).align_to([X0, 0, 0], LEFT)
                ec = Code(e, size=30).move_to([0, y - 0.72, 0]).align_to([X0 + 0.4, 0, 0], LEFT)
                arr = Mono("→", 40, DIM).move_to([2.0, y, 0])
                rv = Mono(r, 40, col).next_to(arr, RIGHT, buff=0.3)
                rows.append((hc, ec, arr, rv))

            h1, e1, a1, v1 = rows[0]
            c.wait_until("three")
            self.play(*appear(h1, shift=None), run_time=1.0)
            self.play(*appear(e1), run_time=1.2)
            c.wait_until("The answer is null")
            link = e1.find("(3 <> NULL)")
            self.play(*recolor(link, PINK), *appear(a1, v1, lag=0.3, shift=None), run_time=1.4)
            c.wait_until("plainly")
            self.play(FlashAround(h1.find("(1, 2, NULL)"), time_width=1.5), run_time=1.2)

            c.wait_until("safe")
            orl = S3.or_line()
            self.play(*appear(orl, shift=None), run_time=1.0)
            self.play(FlashAround(orl, color=TEAL, time_width=1.5), run_time=1.2)

            h2, e2, a2, v2 = rows[1]
            c.wait_until("found")
            self.play(*appear(h2, shift=None), run_time=1.0)
            self.play(*appear(e2), run_time=1.0)
            c.wait_until("true or null")
            self.play(*recolor(e2.find("(1 = 1)"), GREEN), FlashAround(e2.find("(1 = 1)"), color=GREEN, time_width=1.5),
                      *appear(a2, v2, lag=0.3, shift=None), run_time=1.4)

            h3, e3, a3, v3 = rows[2]
            c.wait_until("miss")
            self.play(*appear(h3, shift=None), *appear(e3), run_time=1.2)
            self.play(*recolor(e3.find("(3 = NULL)"), PINK), *appear(a3, v3, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("which the where")
            gate = S5.where_gate(1.0).move_to([5.9, v3.get_y() + 0.1, 0])
            self.play(*appear(gate, shift=None), run_time=0.8)
            v3c = v3.copy()
            self.add(v3c)
            self.play(*S5.gate_bounce(gate, v3c, RED, back=0.6, run_time=1.4))
            self.remove(v3c)

    # ------------------------------------------------------------ clip 5: the fix
    def clip5(self):
        with self.say("c2.derive.5") as c:
            fix = fixed_query()
            old = _old_query(fix)
            sweep_clear(self, *appear(old, shift=None), run_time=1.4)
            self.play(*edit(old, fix), run_time=min(1.5, c.until("filter")))
            box = token_box(fix.line(2), fix.line(2), color=GREEN)
            self.play(FadeIn(box), run_time=0.8)
            self.fix, self.fixbox = fix, box

            c.wait_until("filter")
            bar = S5.death_bar(11.0, height=0.5, center=[0, 0.7, 0])
            klab = T("2,685", 32, GOLD).next_to(bar.known, DOWN, buff=0.2).align_to(bar.frame, LEFT)
            nlab = T("20,494 NULL", 32, PINK).move_to(bar.null)
            self.play(FadeIn(bar.frame), FadeIn(bar.known), FadeIn(bar.null),
                      *appear(klab, nlab, shift=None, lag=0.2), run_time=1.2)
            c.wait_until("not null")
            self.hold(c.until("green") - 1.5)
            self.play(*during(disappear(nlab), 0, 0.35),
                      bar.null.animate.shift(4 * RIGHT).set_opacity(0),
                      bar.frame.animate.set_stroke(opacity=0), run_time=1.4)
            self.remove(bar.null, bar.frame)

            c.wait_until("green")
            ch = and_chain().move_to([0.6, -0.9, 0])
            kl = T("The Kid", 30, YELLOW).next_to(ch, LEFT, buff=0.4)
            self.play(*appear(kl, ch, shift=None, lag=0.2), run_time=1.0)
            G = ch.true_part
            gout = SurroundingRectangle(G, buff=0.18, corner_radius=0.2).set_stroke(GREEN, 3)
            gver = Mono("TRUE", 36, GREEN).next_to(gout, RIGHT, buff=0.3)
            self.play(*during([ch.null_part.animate.shift(3 * RIGHT).set_opacity(0),
                               ch.and_.animate.shift(3 * RIGHT).set_opacity(0)], 0, 0.5),
                      *during([FadeIn(gout)], 0.4, 0.8), *during(appear(gver, shift=None), 0.6, 1),
                      run_time=1.6)
            self.remove(*ch.null_part.get_family(), *ch.and_.get_family())

            c.wait_until("four")
            col = slot_column([-2.3, -1.15, 0])
            kg = VGroup(kl, G, gout, gver)
            kt = VGroup(G.copy(), gout.copy(), gver.copy())
            kt.move_to([3.8, -0.9, 0])
            kl_t = kl.copy().next_to(kt, UP, buff=0.3).align_to(kt, LEFT)
            self.play(*during(disappear(bar.known, klab), 0, 0.45),
                      *during([kl.animate.move_to(kl_t), *[m.animate.move_to(t) for m, t in zip((G, gout, gver), kt)]], 0, 0.6),
                      *during(appear(*col, lag=0.15, shift=None), 0.5, 1), run_time=1.8)
            self.kg = kg

            cards = []
            cues = ["the kid sherlock", "Sherlock", "The General", "It Happened"]
            for (t, y), s, cue in zip(FOUR, col, cues):
                card = green_card(t, y).move_to(s)
                c.wait_until(cue)
                self.play(*swap(s, card, shift=None), run_time=0.8)
                cards.append(card)
            self.cards = cards

    # ------------------------------------------------------------ clip 6: safe key, alarm bell
    def clip6(self):
        fix, cards = self.fix, self.cards
        with self.say("c2.derive.6") as c:
            pr = SCH.schema_map().cards["plays_role"].copy().scale(28 / 24)
            pr.move_to([3.9, -1.1, 0])
            self.play(*during(disappear(*self.kg), 0, 0.45), *during(appear(pr, shift=None), 0.5, 1), run_time=1.6)

            c.wait_until("primary key")
            ul = pr.underlines["movie_id"]
            self.play(ul.animate.set_stroke(GREEN, 4), FlashUnder(pr.rows["movie_id"], color=GREEN, time_width=1.5),
                      *recolor(pr.rows["movie_id"], GREEN), run_time=1.2)
            c.wait_until("never be null")
            nn = T("never NULL", 30, GREEN, t2c={"NULL": PINK}).next_to(pr, DOWN, buff=0.3)
            self.play(*appear(nn), run_time=1.0)

            c.wait_until("alarm")
            notin = fix.find("NOT IN")
            ring = SurroundingRectangle(notin, buff=0.12, corner_radius=0.15).set_stroke(RED, 4)
            b = bell().move_to([notin.get_x(), fix.line(2).get_y(), 0])
            self.play(FadeIn(ring), *appear(b, shift=None), run_time=0.8)
            for _ in range(2):
                self.play(ring.animate.scale(1.12), Rotate(b, 0.35, rate_func=wiggle),
                          rate_func=there_and_back, run_time=0.7)

            c.wait_until("Ask yourself")
            end = final_results()
            self.play(*during(disappear(fix, self.fixbox, ring, b, pr, nn), 0, 0.45),
                      *during([m.animate.move_to(e) for m, e in zip(cards, end.cards)], 0.3, 0.9),
                      *during(appear(end.result, shift=None), 0.55, 1), run_time=1.8)
            c.wait_until()
            self.wait(1.5)
