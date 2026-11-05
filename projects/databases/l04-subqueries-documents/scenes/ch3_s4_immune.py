"""Chapter 3, scene 4: why NOT EXISTS can't be fooled by NULLs. Clips c3.immune.1 – c3.immune.5.

Exports (static, built where they sit on screen):
- sealed_box() -> VGroup(.box .title .nulls .arrow .count): the {count} shot, right half of the
  split screen: BLUE rounded subquery box (DIM "subquery" inside, top left) with three PINK NULL
  chips inside, a GOLD arrow out of its bottom and the GOLD count "0 or 2" ("or" DIM) below it.
"""
# style: 2
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

QUERY = """SELECT title FROM movies AS m
WHERE NOT EXISTS (
    SELECT 1 FROM people AS p
    WHERE p.deathyear = m.year
);"""
FOUR = ["The Kid", "Sherlock Jr.", "The General", "It Happened One Night"]
LOOP_ROWS = [("The Kid", "1921"), ("Sherlock Jr.", "1924"), ("The Gold Rush", "1925"), None]

LANE_Y = -0.85
GATE_X = 4.7
COUNT_X = 6.25
BOX_L, BOX_R, BOX_T, BOX_B = -2.0, 6.75, 2.85, -2.48
BAR_C = np.array([1.1, 1.0, 0])
BAR_W, BAR_H = 5.4, 0.75
VERDICT_Y = -3.3


def _s(name):
    return load_scene(name)


# ---------------------------------------------------------------- pieces
def _query():
    q = Code(QUERY, size=32)
    q.find("AS m", line=0)[-1].set_color(YELLOW)
    q.find("m.year", line=3).set_color(YELLOW)
    q.move_to([0, -0.35, 0]).align_to([-6.5, 0, 0], LEFT)
    return q


def _result():
    x, w, h = 4.4, 4.5, 0.56
    head = Mono("title", 28, DIM).move_to([x, 1.75, 0])
    rows = []
    for i, t in enumerate(FOUR):
        y = 1.15 - i * 0.66
        r = Rectangle(width=w, height=h).set_stroke(GREEN, 3).set_fill(BG, 0).move_to([x, y, 0])
        lab = T(t, 30).move_to(r)
        rows.append(VGroup(r, lab))
    return head, rows


def _not_in_band():
    ts = _s("ch2_s1_hook").trap_shot()
    q, res = ts.query, ts.result
    q.scale(26 / 30)
    res.scale(0.82)
    band = VGroup(q, res).arrange(RIGHT, buff=0.4).move_to([0, -2.9, 0])
    return q, res


def _cursor(left, k, i):
    row = left.rows[i]
    r = Rectangle(width=left.width_all * k + 0.4, height=0.5)
    r.set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.12).set_z_index(-1)
    r.move_to([left.title.get_left()[0] + left.width_all * k / 2, row.get_center()[1], 0])
    return r


def _token(v, count):
    ch = _s("ch2_s5_logic").chip(v, 30)
    n = T(f"× {count}", 28, GOLD)
    return VGroup(ch, n).arrange(RIGHT, buff=0.2)


def _counter(n):
    return Mono(str(n), 44, color=GOLD).move_to([COUNT_X, LANE_Y + 0.12, 0])


def sealed_box():
    s5 = _s("ch2_s5_logic")
    box = RoundedRectangle(corner_radius=0.2, width=5.0, height=2.4).set_stroke(BLUE, 3)
    box.move_to([3.55, 1.3, 0])
    title = T("subquery", 28, DIM).move_to(box.get_corner(UL) + np.array([0.85, -0.35, 0]))
    nulls = VGroup(*[s5.chip("N", 28).move_to(p) for p in ([2.3, 0.85, 0], [3.9, 1.55, 0], [5.2, 0.8, 0])])
    arrow = Arrow([3.55, 0.1, 0], [3.55, -0.75, 0], buff=0, stroke_width=4).set_color(GOLD)
    count = Mono("0 or 2", 40, GOLD, t2c={"or": DIM}).move_to([3.55, -1.05, 0])
    g = VGroup(box, title, nulls, arrow, count)
    g.box, g.title, g.nulls, g.arrow, g.count = box, title, nulls, arrow, count
    return g


def _rattle(m, phase):
    base = m.get_center().copy()

    def upd(mob, a):
        env = np.sin(PI * a)
        mob.move_to(base + 0.13 * env * np.array([np.sin(10 * PI * a + phase), np.cos(8 * PI * a + phase), 0]))

    return UpdateFromAlphaFunc(m, upd, rate_func=linear)


def _bump_up(m, top_y):
    """A token rises until it touches top_y, then sinks back and fades (remove afterwards)."""
    start = m.get_center().copy()
    orig = m.copy()
    rise = top_y - m.get_top()[1]

    def upd(mob, a):
        if a < 0.4:
            dy, k = rise * smooth(a / 0.4), 1.0
        else:
            s = smooth((a - 0.4) / 0.6)
            dy, k = rise - 0.35 * s, 1 - s
        mob.become(orig)
        mob.move_to(start + np.array([0, dy, 0]))
        for x, o in zip(mob.get_family(), orig.get_family()):
            x.set_fill(opacity=o.get_fill_opacity() * k)
            x.set_stroke(opacity=o.get_stroke_opacity() * k)

    return UpdateFromAlphaFunc(m, upd, rate_func=linear)


# ---------------------------------------------------------------- scene
class Immune(NarratedScene):
    def construct(self):
        s5 = _s("ch2_s5_logic")
        self.clip1()
        self.clip2(s5)
        self.clip3(s5)
        self.clip4(s5)
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------- 1: the four movies
    def clip1(self):
        with self.say("c3.immune.1") as c:
            back = _s("ch3_s1_hook").trap_back()
            back.scale(0.95).move_to([0, 0.3, 0])
            self.play(*appear(back), run_time=1.0)  # early: callback, ch3 s1's result picture
            c.wait_until("question")
            question = T("Which movies came out in a year in which\nnone of the people in the database died?",
                         32, YELLOW, line_spacing=0.9)
            question.move_to([0, 2.95, 0])
            self.play(*during(disappear(back), 0, 0.45), *during(appear(question), 0.4, 1), run_time=1.6)
            c.wait_until("query")
            q = _query()
            self.play(*appear(q, shift=None), run_time=1.5)
            c.wait_until("four")
            head, rows = _result()
            self.play(*appear(head), run_time=1.0)
            c.wait_until("the kid")
            self.play(*appear(*rows, lag=1.0), run_time=min(3.9, 0.9 * c.until("same")))
            c.wait_until("same")
            nq, nres = _not_in_band()
            self.play(*appear(nq, nres, lag=0.3), run_time=1.2)
            self.play(*flash(rows, color=GREEN, run_time=1.2))

    # -------------------------------------------------------- 2: the nulls are still there
    def clip2(self, s5):
        with self.say("c3.immune.2") as c:
            loop = _s("ch3_s2_correlated").outer_loop(left_title="movies", left_rows=LOOP_ROWS,
                                                       right_title="people", right_cols=("deathyear",),
                                                       right_rows=[("1977",)])
            left = loop.left
            k = 28 / 24
            left.scale(k, about_point=left.title.get_left())
            left.shift([-6.55 - left.title.get_left()[0], 1.65 - left.title.get_y(), 0])
            self.left, self.k = left, k
            strip = _s("ch2_s4_trap").people_strip()
            sweep_clear(self, time_span(FadeIn(left), 0.6, 1.4), time_span(FadeIn(strip), 0.8, 1.6))
            c.wait_until("no death year")
            bar = s5.death_bar(width=BAR_W, height=BAR_H, center=BAR_C)
            frame = bar.frame
            self.play(FadeOut(strip, target_position=BAR_C, scale=0.3),
                      *during([FadeIn(frame), FadeIn(bar)], 0.4, 1), run_time=1.6)
            pink = T("20,494 NULL", 30, t2c={"20,494": GOLD, "NULL": PINK})
            pink.next_to(bar.null, DOWN, buff=0.22)
            self.play(*appear(pink), run_time=1.0)  # early: the count the voice is reading
            c.wait_until("compare")
            expr = Mono("NULL = 1921", 32, t2c={"NULL": PINK, "1921": GOLD}).move_to([2.6, LANE_Y, 0])
            self.play(*appear(expr), run_time=1.0)
            c.wait_until("gives unknown")
            nchip = s5.chip("N", 32).move_to([2.6, LANE_Y, 0])
            self.play(*swap(expr, nchip), run_time=1.2)
            c.wait_until("ask")
            qmark = T("?", 64, YELLOW).move_to(bar.null)
            self.play(*appear(qmark), run_time=1.0)
        self.bar, self.frame, self.pink, self.qmark, self.nchip = bar, frame, pink, qmark, nchip

    # -------------------------------------------------------- 3: follow The Kid
    def clip3(self, s5):
        left, bar = self.left, self.bar
        with self.say("c3.immune.3") as c:
            cursor = _cursor(left, self.k, 0)
            box = RoundedRectangle(corner_radius=0.2, width=BOX_R - BOX_L, height=BOX_T - BOX_B)
            box.set_stroke(BLUE, 3).move_to([(BOX_L + BOX_R) / 2, (BOX_T + BOX_B) / 2, 0])
            box_t = T("subquery", 28, DIM).next_to(box, UP, buff=0.12).align_to(box, LEFT).shift(0.2 * RIGHT)
            self.play(FadeIn(cursor), *disappear(self.qmark, self.nchip), FadeIn(box), run_time=1.2)
            c.wait_until("from")
            pre = Mono("WHERE p.deathyear =", 30, BLUE, t2c={"p.deathyear": FG})
            pre.move_to([0, 2.35, 0]).align_to([BOX_L + 0.4, 0, 0], LEFT)
            year = Mono("1921", 30, GOLD).next_to(pre, RIGHT, buff=0.22)
            year.align_to(pre, DOWN)
            self.play(*during(fly(left.rows[0][1], year), 0, 0.6), *during(appear(pre, box_t), 0.6, 1), run_time=2.2)
            c.wait_until("false")
            gold = T("2,685 known death years", 30, t2c={"2,685": GOLD})
            gold.next_to(bar.known, UP, buff=0.22).align_to(bar.known, LEFT)
            c.wait_until(own_word=gold)
            self.play(*appear(gold), run_time=1.0)
            c.wait_until("so each")
            ftok = _token("F", "2,685").move_to([0, LANE_Y + 0.4, 0]).align_to([BOX_L + 0.4, 0, 0], LEFT)
            self.play(*appear(ftok), run_time=1.2)
            c.wait_until("null")
            ntok = _token("N", "20,494").move_to([0, LANE_Y - 0.4, 0]).align_to(ftok, LEFT)
            self.play(*appear(ntok), run_time=1.2)
            c.wait_until("drop")
            gate = s5.where_gate(height=1.4)
            gate.shift(np.array([GATE_X, LANE_Y, 0]) - gate.bar.get_center())
            cap = T("WHERE keeps\nTRUE only", 28, DIM, t2c={"TRUE": GREEN}, line_spacing=0.8)
            cap.move_to([GATE_X, -2.0, 0])
            c.wait_until(own_word=cap)
            self.play(*appear(gate, cap, lag=0.4), run_time=1.3)
            c.wait_until("so all")
            toks = VGroup(ftok, ntok)
            self.play(*s5.gate_bounce(gate, toks, color=RED, back=0.9, run_time=1.8))
            self.remove(toks, ftok, ntok)
            c.wait_until("zero")
            counter = _counter(0)
            rows_l = T("rows", 28, DIM).next_to(counter, DOWN, buff=0.15)
            self.play(*appear(counter, rows_l), run_time=1.0)
            c.wait_until("returns zero")
            self.play(FlashAround(counter, run_time=1.2, color=GOLD))
            c.wait_until("true")
            notex = Mono("NOT EXISTS", 32, BLUE).move_to([1.2, VERDICT_Y, 0])
            verdict = s5.chip("T", 32).next_to(notex, RIGHT, buff=0.5)
            self.play(*appear(notex, verdict, lag=0.5), run_time=1.4)
            c.wait_until("so the kid")
            self.play(*recolor(left.rows[0], GREEN), cursor.animate.set_stroke(GREEN).set_fill(GREEN, 0.12),
                      run_time=1.0)
        self.cursor, self.box, self.box_t, self.pre, self.year = cursor, box, box_t, pre, year
        self.gold, self.gate, self.cap, self.counter, self.rows_l = gold, gate, cap, counter, rows_l
        self.notex, self.verdict = notex, verdict

    # -------------------------------------------------------- 4: The Gold Rush, then the difference
    def clip4(self, s5):
        left = self.left
        with self.say("c3.immune.4") as c:
            year2 = Mono("1925", 30, GOLD).move_to(self.year)
            self.play(Transform(self.cursor, _cursor(left, self.k, 2)), *swap(self.year, year2),
                      *disappear(self.verdict), run_time=1.5)
            c.wait_until("two")
            rows = []
            for i, (name, y) in enumerate((("Jane Connelly", "1925"), ("Jean C. Havez", "1925"))):
                n = T(name, 28)
                yr = Mono(y, 28, GOLD)
                ch = s5.chip("T", 28)
                r = VGroup(n, yr, ch).arrange(RIGHT, buff=0.3)
                yr.align_to(n, DOWN)
                r.move_to([0, -0.45 - 0.8 * i, 0]).align_to([BOX_L + 0.4, 0, 0], LEFT)
                rows.append(r)
            self.play(*appear(*rows, lag=0.5), run_time=1.5)
            c.wait_until("so the subquery")
            tok = VGroup(rows[0][2].copy(), rows[1][2].copy())
            self.add(tok)
            beyond = (COUNT_X - 0.3 - tok.width / 2) - GATE_X
            self.play(*s5.gate_pass(self.gate, tok, beyond=beyond, run_time=1.6))
            c2 = _counter(2)
            self.play(*disappear(tok), *swap(self.counter, c2), run_time=1.0)
            c.wait_until("and not exists")
            fv = s5.chip("F", 32).next_to(self.notex, RIGHT, buff=0.5)
            self.play(*appear(fv), *set_alpha([left.rows[2]], DIMMED), run_time=1.2)
            c.wait_until("difference")
            div = DashedLine([0, 3.4, 0], [0, -3.4, 0], dash_length=0.12).set_stroke(DIM, 2)
            h_l = Mono("NOT IN", 36, RED).move_to([-3.55, 3.15, 0])
            h_r = Mono("NOT EXISTS", 36, BLUE).move_to([3.55, 3.15, 0])
            sweep_clear(self, time_span(FadeIn(div), 0.6, 1.2), time_span(FadeIn(h_l), 0.7, 1.3),
                        time_span(FadeIn(h_r), 0.8, 1.4), run_time=1.4)
            c.wait_until("chain")
            chain = _s("ch2_s6_derive").and_chain()
            chain.arrange(DOWN, buff=0.25).move_to([-4.0, 1.4, 0])
            self.play(*appear(chain.true_part, chain.and_, chain.null_part, lag=0.4), run_time=1.6)  # early: ch2 s6's chain, shown whole
            c.wait_until("so a null")
            chip = s5.chip("N", 28)
            chip.next_to(chain.null_part, RIGHT, buff=0.25)
            end = np.array([chip.get_x(), -1.4, 0])
            where = Mono("WHERE", 32, BLUE).move_to(end).shift(LEFT * (chip.width / 2 + 0.25))
            where.shift(LEFT * where.width / 2)
            arr = Arrow(chip.get_bottom(), end + 0.42 * UP, buff=0.08, stroke_width=3).set_color(PINK)
            self.play(FadeIn(chip), GrowArrow(arr), *appear(where), run_time=1.2)
            self.play(chip.animate.move_to(end), run_time=1.5)
            c.wait_until("count")
            sb = sealed_box()
            self.play(FadeIn(sb.box), *appear(sb.title, *sb.nulls, lag=0.15), run_time=1.0)
            self.play(*[_rattle(n, 1.3 * i) for i, n in enumerate(sb.nulls)],
                      *during([GrowArrow(sb.arrow)], 0.3, 0.6), *during(appear(sb.count), 0.55, 1),
                      run_time=1.8)
            c.wait_until("never")
            arr2 = Arrow([3.55, -1.3, 0], [3.55, -1.95, 0], buff=0, stroke_width=3).set_color(DIM)
            verdict = T("TRUE or FALSE", 36, t2c={"TRUE": GREEN, "FALSE": RED, "or": DIM}).move_to([3.55, -2.3, 0])
            capn = T("a count is never unknown", 32).move_to([3.55, -3.1, 0])
            self.play(GrowArrow(arr2), *appear(verdict), run_time=1.2)
            self.play(*appear(capn), run_time=1.0)  # early: caption sums up the line being said
            c.wait_until("the null never")
            self.play(*[_rattle(n, 0.7 * i) for i, n in enumerate(sb.nulls)],
                      FlashAround(sb.box, color=BLUE, run_time=1.6), run_time=1.6)

    # -------------------------------------------------------- 5: DuckDB's plan
    def clip5(self):
        s = _s("ch3_s5_semijoin")
        with self.say("c3.immune.5") as c:
            root = s.plan_box("HASH_JOIN", "Join Type: ANTI").move_to([0, 2.4, 0])
            scan_m = s.plan_box("SEQ_SCAN", "movies.main.movies").move_to([-3.7, 0.15, 0])
            filt = s.plan_box("FILTER", "(deathyear IS NOT NULL)").move_to([3.3, 0.15, 0])
            scan_p = s.plan_box("SEQ_SCAN", "movies.main.people").move_to([3.3, -2.3, 0])

            def edge(a, b):
                return Line(a.box.get_bottom(), b.box.get_top()).set_stroke(DIM, 2.5)

            edges = [edge(root, scan_m), edge(root, filt), edge(filt, scan_p)]
            sweep_clear(self, *[time_span(FadeIn(m), 0.6 + 0.2 * i, 1.4 + 0.2 * i)
                                for i, m in enumerate([root, scan_m, filt, scan_p])],
                        *[time_span(FadeIn(e), 1.2, 2.0) for e in edges], run_time=2.0)  # early: plan shown whole, then walked
            c.wait_until("anti")
            anti = root.details[0]
            self.play(anti.animate.set_color(BLUE), FlashAround(anti, color=BLUE), run_time=1.4)
            c.wait_until("filter")
            cond = filt.details[0]
            self.play(cond.animate.set_color(YELLOW), FlashAround(cond), run_time=1.4)
            c.wait_until("the very fix")
            tag = T("part 2's fix", 28, DIM).move_to([1.55, -1.08, 0])
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("safe")
            nul = _s("ch2_s5_logic").chip("N", 26).move_to([4.95, -1.15, 0])
            self.play(FadeIn(nul, shift=0.2 * UP), run_time=0.8)
            self.play(_bump_up(nul, filt.box.get_bottom()[1] - 0.04),
                      time_span(filt.box.animate.set_stroke(RED), 0.5, 0.9),
                      run_time=1.6)
            self.remove(nul)
            self.play(filt.box.animate.set_stroke(BLUE), run_time=0.5)
            c.wait_until("single")
            plan = VGroup(root, scan_m, filt, scan_p, *edges)
            bracket = SurroundingRectangle(plan, color=YELLOW, buff=0.22, corner_radius=0.15).set_stroke(YELLOW, 2.5)
            cap = T("one join,\nnot one scan per movie", 32, t2c={"one join,": YELLOW}).move_to([-3.7, -2.15, 0])
            self.play(FadeIn(bracket), *appear(cap), run_time=1.5)
