"""Chapter 3, scene 3: NOT EXISTS, the antijoin. Clips c3.anti.1 – c3.anti.4.

Opens on ch3_s2_correlated's handover shot (outer loop at size 28, tags, card, counter, plan lines),
brings the query back top-left, ends on an empty frame.
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

S2C = load_scene("ch3_s2_correlated")
S2A = load_scene("ch2_s2_absent")
cell = S2A.cell

Q_GROW = 1.35            # query Code 20 -> 27
VERSIONS = [["LEFT JOIN", "… IS NULL"], ["EXCEPT"], ["NOT IN"], ["NOT EXISTS"]]


# ---------------------------------------------------------------- helpers
def version_card(name_lines, color=BLUE, w=2.15):
    """A small card: the version's name on top, the two titles it returns below. 2.1 x 2.1."""
    head = VGroup(*[Mono(s, 27, FG) for s in name_lines]).arrange(DOWN, buff=0.1)
    titles = VGroup(T("Flow", 28), T("Kaiva", 28)).arrange(DOWN, buff=0.16)
    h = 0.15 + 0.75 + 0.15 + titles.height + 0.25
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h).set_stroke(color, 3).set_fill(BG, 1)
    top = box.get_top()[1]
    head.move_to([0, top - 0.15 - 0.375, 0])
    div = Line([-w / 2 + 0.2, top - 1.05, 0], [w / 2 - 0.2, top - 1.05, 0]).set_stroke(DIM, 2)
    titles.move_to([0, (top - 1.05 + box.get_bottom()[1]) / 2, 0])
    card = VGroup(box, head, div, titles)
    card.box, card.head, card.div, card.titles = box, head, div, titles
    return card


def result_table(x0=2.0, y_head=3.0):
    """movie_id | title: Flow, Kaiva in ch2's GREEN result look."""
    rc = [(x0 + 1.35, 2.7), (x0 + 3.55, 1.7)]
    heads = VGroup(Mono("movie_id", 28, DIM).move_to([rc[0][0], y_head, 0]),
                   Mono("title", 28, DIM).move_to([rc[1][0], y_head, 0]))
    rows = []
    for y, (mid, tt) in zip([y_head - 0.6, y_head - 1.2], [("tt4772188", "Flow"), ("tt27719898", "Kaiva")]):
        r = VGroup(cell(Mono(mid, 28), rc[0][1], color=GREEN, center=[rc[0][0], y, 0]),
                   cell(T(tt, 28), rc[1][1], color=GREEN, center=[rc[1][0], y, 0]))
        for m in r:
            m.rect.set_stroke(GREEN, 3)
        rows.append(r)
    return heads, rows


TERM_W, TERM_H, TERM_TOP = 6.6, 3.9, 0.35


def terminal_frame(cx):
    f = RoundedRectangle(corner_radius=0.15, width=TERM_W, height=TERM_H).set_stroke(DIM, 2).set_fill(BG, 0)
    f.move_to([cx, TERM_TOP - TERM_H / 2, 0])
    return f


def term_prompt(frame, sql):
    x0 = frame.get_left()[0] + 0.15
    code = Code(sql, 27, lang="sql")
    code.move_to([0, TERM_TOP - 0.4, 0]).align_to([x0, 0, 0], LEFT)
    return code


def term_column(frame, head, rows):
    x0 = frame.get_left()[0] + 0.6
    h = Mono(head, 27, DIM).move_to([0, TERM_TOP - 0.95, 0]).align_to([x0, 0, 0], LEFT)
    rule = Line([x0, TERM_TOP - 1.2, 0], [x0 + 4.4, TERM_TOP - 1.2, 0]).set_stroke(DIM, 1.5)
    rs = [Mono(s, 27).move_to([0, TERM_TOP - 1.5 - 0.42 * i, 0]).align_to([x0, 0, 0], LEFT)
          for i, s in enumerate(rows)]
    dot = T("·", 32, DIM).move_to([x0 + 0.1, TERM_TOP - 1.5 - 0.42 * len(rows) + 0.04, 0])
    return VGroup(h, rule, *rs, dot)


def term_count(frame):
    x0 = frame.get_left()[0] + 0.6
    return Mono("30,303 rows", 28, GOLD).move_to([0, TERM_TOP - TERM_H + 0.4, 0]).align_to([x0, 0, 0], LEFT)


# ---------------------------------------------------------------- scene
class NotExists(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ clip 1: the operator, Kid and Flow
    def clip1(self):
        shot = S2C.handover_shot()
        loop = shot.loop
        cursor = loop.cursor
        kid_tag, flow_tag = shot.tags[0], shot.tags[1]
        plan_a, plan_b = shot.plan[0], shot.plan[1]
        # exactly s2's last frame, added piece by piece so each can leave on its own
        self.add(loop.left, loop.card, loop.counter, loop.counter_label, cursor,
                 kid_tag, flow_tag, plan_a, plan_b)
        # the query comes back top-left, grown (Code 20 -> 27); s2 took it off at {loop}
        q, arrow = shot.query, shot.arrow
        QP = q.get_corner(UL)
        VGroup(q, arrow).scale(Q_GROW, about_point=QP)
        self.q, self.arrow = q, arrow

        with self.say("c3.anti.1") as c:
            # make room: card, counter and plan lines go, the loop (s2's size) drops a little,
            # the query returns above it
            movers = [loop.left, cursor, kid_tag, flow_tag]
            dy = (q.get_bottom()[1] - 0.35) - loop.left.title.get_top()[1]   # just under the query
            moves = [m.animate.shift(dy * UP) for m in movers]
            self.play(*during(disappear(loop.card, loop.counter, loop.counter_label, plan_a, plan_b), 0, 0.4),
                      *during(moves, 0.35, 0.75), *during(appear(q, arrow, shift=None), 0.7, 1.0), run_time=1.6)

            ne = q.find("NOT EXISTS (")
            ne_box = token_box(ne, q.line(2), BLUE, pad=0.16)
            self.play(GrowFromCenter(ne_box), FlashAround(ne, color=BLUE, time_width=1.5), run_time=1.2)

            def rule(a, b, key):
                g = VGroup(T(a, 28, t2c={key: BLUE}), T(b, 28))
                return g.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

            r1 = rule("EXISTS is true if subquery", "returns ≥ 1 rows;", "EXISTS")
            r2 = rule("NOT EXISTS is true if subquery", "returns 0 rows.", "NOT EXISTS")
            r1.move_to([0, -0.05, 0]).align_to([0.9, 0, 0], LEFT)
            r2.next_to(r1, DOWN, buff=0.4).align_to(r1, LEFT)
            self.rules = (r1, r2)
            c.wait_until("exists")
            self.play(*appear(r1), run_time=1.0)
            c.wait_until("notexists")
            self.play(*appear(r2), run_time=1.0)

            # The Kid: 12 rows -> FALSE, dropped
            c.wait_until("kid")
            self.play(FlashAround(kid_tag, color=YELLOW, time_width=1.5), run_time=1.2)
            false = VGroup(T("→", 28, DIM), Mono("FALSE", 28, RED)).arrange(RIGHT, buff=0.15)
            false.move_to(kid_tag).align_to(kid_tag, LEFT)
            c.wait_until("false")
            self.play(*swap(kid_tag, false), run_time=1.2)
            c.wait_until("dropped")
            self.play(*set_alpha([loop.left.rows[0], false], DIMMED), run_time=1.0)

            # Flow: 0 rows -> TRUE, stays
            c.wait_until("zero rows")
            self.play(FlashAround(flow_tag, color=YELLOW, time_width=1.5), run_time=1.2)
            true = VGroup(T("→", 28, DIM), Mono("TRUE", 28, GREEN)).arrange(RIGHT, buff=0.15)
            true.move_to(flow_tag).align_to(flow_tag, LEFT)
            c.wait_until("stays")
            self.play(*swap(flow_tag, true),
                      cursor.animate.set_stroke(GREEN, 2.5).set_fill(GREEN, 0.12), run_time=1.2)

            # the whole query's result
            c.wait_until("result")
            heads, rows = result_table()
            self.play(*appear(heads, *rows, lag=0.3, shift=None), run_time=1.4)  # early: the result table, shown whole

            # the same two, three other ways
            # right of the loop's FALSE/TRUE, filling to the right margin
            x0 = max(false.get_right()[0], true.get_right()[0]) + 0.35
            cw = min(2.3, (6.6 - x0 - 0.24) / 3)
            cards = [version_card(v, w=cw) for v in VERSIONS[:3]]
            for i, card in enumerate(cards):
                card.move_to([0, -1.75, 0]).align_to([x0 + i * (cw + 0.12), 0, 0], LEFT)
            self.cards = cards
            c.wait_until("left join")
            self.play(*during(disappear(*self.rules), 0, 0.45),
                      *during(appear(cards[0], shift=0.25 * RIGHT), 0.5, 1.0), run_time=1.4)
            c.wait_until("keyword")
            self.play(*appear(cards[1], cards[2], shift=0.25 * RIGHT, lag=0.5), run_time=1.3)

    # ------------------------------------------------------------ clip 2: SELECT 1 doesn't matter
    def clip2(self):
        q = self.q
        with self.say("c3.anti.2") as c:
            one = q.find("SELECT 1")
            box = token_box(one, q.line(3), YELLOW, pad=0.16)
            self.play(GrowFromCenter(box), run_time=0.8)
            c.wait_until("matter")
            sweep_clear(self, keep=[q, box], run_time=1.2)
            cap = T("only: any rows?", 32, DIM).next_to(q.line(3), RIGHT, buff=0.6)
            self.play(*appear(cap), run_time=1.0)

            # the lecturer's live demo
            c.wait_until("demo")
            f1, f2 = terminal_frame(-3.4), terminal_frame(3.4)
            self.play(*appear(f1, f2, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("Select role")
            p1 = term_prompt(f1, "SELECT role FROM plays_role;")
            self.play(*appear(p1, shift=None), run_time=1.0)
            c.wait_until("gives")
            col1 = term_column(f1, "role", ["A Tramp", "The Lone Prospector", "A Tramp", "A Factory Worker"])
            self.play(*appear(col1, shift=None), run_time=1.0)  # early: the demo's output, read as a whole
            c.wait_until("thirty")
            n1 = term_count(f1)
            self.play(*appear(n1), run_time=1.0)

            c.wait_until("ones")
            p2 = term_prompt(f2, "SELECT 1 FROM plays_role;")
            self.play(*appear(p2, shift=None), run_time=1.0)
            c.wait_until("gives", nth=1)
            col2 = term_column(f2, "1", ["1"] * 4)
            self.play(*appear(col2, shift=None), run_time=1.0)
            c.wait_until("exactly")
            n2 = term_count(f2)
            self.play(*appear(n2), run_time=1.0)

            # any value would do
            c.wait_until("any")
            cur_p, cur_c = p2, col2
            for sql, head, val, rt in [("SELECT 'x' FROM plays_role;", "'x'", "x", 0.8),
                                       ("SELECT 42 FROM plays_role;", "42", "42", 0.6)]:
                np_ = Code(sql, 27, lang="sql").move_to(cur_p).align_to(cur_p, LEFT)
                nc = term_column(f2, head, [val] * 4)
                self.play(*edit(cur_p, np_), *swap(cur_c, nc), run_time=rt)
                cur_p, cur_c = np_, nc
                self.wait(0.15)
            c.wait_until("usual habit")
            back_p = Code("SELECT 1 FROM plays_role;", 27, lang="sql").move_to(cur_p).align_to(cur_p, LEFT)
            back_c = term_column(f2, "1", ["1"] * 4)
            self.play(*edit(cur_p, back_p), *swap(cur_c, back_c), FlashAround(n2, color=GOLD, time_width=1.5),
                      run_time=min(1.0, c.until(floor=0.6)))

    # ------------------------------------------------------------ clip 3: the antijoin
    def clip3(self):
        with self.say("c3.anti.3") as c:
            alg = MathTex(r"\text{movies}", r"\,\triangleright", r"_{\text{movie\_id}}", r"\,\text{plays\_role}",
                          font_size=72, color=BLUE)
            alg.move_to([0, 0.4, 0])
            lab = T("antijoin", 34, DIM).next_to(alg[1], DOWN, buff=0.55)
            sweep_clear(self, *appear(alg, shift=None), run_time=1.4)
            c.wait_until("antijoin")
            self.play(*appear(lab), run_time=1.0)

            def hbox(m):
                return SurroundingRectangle(m, buff=0.1).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1)

            c.wait_until("Movies")
            box = hbox(alg[0])
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("plays role")
            self.play(Transform(box, hbox(alg[3])), run_time=0.7)
            c.wait_until("on movie")
            self.play(Transform(box, hbox(alg[2])), run_time=0.7)
            c.wait_until("no match")
            self.play(FadeOut(box), run_time=0.6)

            # the lecturer's picture: LEFT JOIN ... IS NULL
            c.wait_until("lj")
            lab2 = T("antijoin", 34, DIM)
            alg_t = alg.copy().scale(0.7)
            VGroup(alg_t, lab2).arrange(RIGHT, buff=0.5).move_to([0, 3.05, 0])
            lab2.align_to(alg_t[0], DOWN)
            self.play(*during(disappear(lab), 0, 0.35),
                      *during([alg.animate.scale(0.7).move_to(alg_t)], 0.25, 0.75),
                      *during(appear(lab2, shift=None), 0.75, 1.0), run_time=1.6)

            ys = [1.2, 0.65, 0.1, -0.4, -0.9, -1.45]
            MX, MW = -5.3, 2.6
            PX, PW = -2.55, 2.3
            mh = Mono("movies", 27, DIM).move_to([MX, 1.85, 0])
            mrows = []
            for y, t in zip(ys, ["The Kid", "Sherlock Jr.", "The Gold Rush", None, "Kaiva", "Flow"]):
                if t is None:
                    mrows.append(S2C._vdots(h=0.3).move_to([MX, y, 0]))
                else:
                    mrows.append(cell(T(t, 27), MW, h=0.48, center=[MX, y, 0]))
            ph = Mono("plays_role", 27, DIM).move_to([PX, 1.85, 0])
            prows = [cell(T(t, 27), PW, h=0.48, center=[PX, y, 0])
                     for y, t in zip(ys[:3], ["A Tramp", "Bride", "Car Thief"])]
            pdots = S2C._vdots(h=0.3).move_to([PX, ys[3], 0])
            meet = [Line(mrows[0].get_right(), p.get_left()).set_stroke(BLUE, 2) for p in prows]
            lj = Mono("LEFT JOIN … IS NULL", 27, DIM).move_to([(MX + PX) / 2, -2.4, 0])
            self.play(*appear(mh, *mrows, lag=0.08, shift=None), *appear(ph, *prows, pdots, lag=0.1, shift=None),
                      run_time=1.2)
            self.play(*[Create(m) for m in meet], *appear(lj), run_time=1.0)

            # the pile: one row per role, plus two padded with NULL
            TX, TW, RX, RW = 1.35, 2.1, 3.55, 2.3
            th = Mono("title", 27, DIM).move_to([TX, 1.85, 0])
            rh = Mono("role", 27, DIM).move_to([RX, 1.85, 0])
            pile = []
            for y, (t, r) in zip(ys[:3], [("The Kid", "A Tramp"), ("The Kid", "Bride"), ("The Kid", "Car Thief")]):
                pile.append(VGroup(cell(T(t, 27), TW, h=0.48, center=[TX, y, 0]),
                                   cell(T(r, 27), RW, h=0.48, center=[RX, y, 0])))
            pile_dots = VGroup(S2C._vdots(h=0.3).move_to([TX, ys[3], 0]), S2C._vdots(h=0.3).move_to([RX, ys[3], 0]))
            pads = []
            for y, t in zip(ys[4:], ["Kaiva", "Flow"]):
                pads.append([cell(T(t, 27), TW, h=0.48, center=[TX, y, 0]),
                             cell(Mono("NULL", 27, PINK), RW, h=0.48, center=[RX, y, 0])])
            wmax = Integer(30305, font_size=44).width
            CL = TX + 0.4 - wmax / 2
            counter = Integer(0, font_size=44, color=GOLD).move_to([TX + 0.4, -2.4, 0]).align_to([CL, 0, 0], LEFT)
            counter.add_updater(lambda m: m.align_to([CL, 0, 0], LEFT))
            crow = T("rows", 28, DIM).move_to([0, -2.4, 0]).align_to([CL + wmax + 0.25, 0, 0], LEFT)
            crow.align_to(counter, DOWN)
            c.wait_until("waste")
            self.play(*appear(th, rh, shift=None), FadeIn(counter), FadeIn(crow), run_time=0.8)  # early: the counter's unit
            rt = max(1.5, c.until("padded") - 0.2)
            self.play(*appear(*pile, pile_dots, lag=0.5, shift=0.15 * DOWN),
                      ChangeDecimalToValue(counter, 30303, rate_func=linear), run_time=rt)
            c.wait_until("padded")
            self.play(*appear(*pads[0], *pads[1], lag=0.2, shift=None),
                      ChangeDecimalToValue(counter, 30305), run_time=1.4)
            self.play(*flash([pads[0][1], pads[1][1]], color=PINK, time_width=1.5), run_time=1.2)

            # the filter throws away all but two
            c.wait_until("filter")
            reds = [m.rect.animate.set_stroke(RED, 3) for r in pile for m in r]
            self.play(*reds, pile_dots.animate.set_color(RED), run_time=0.8)
            self.play(*[FadeOut(m, shift=0.6 * DOWN) for m in (*pile, pile_dots)], run_time=1.0)
            counter.clear_updaters()
            two = Integer(2, font_size=44, color=GOLD).move_to(counter).align_to([CL, 0, 0], LEFT)
            self.play(*swap(counter, two), run_time=0.8)

            # the antijoin never builds them
            c.wait_until("skip")
            arrows = [Arrow(mrows[i].get_right(), pads[i - 4][0].get_left(), buff=0.12, stroke_width=5,
                            max_tip_length_to_length_ratio=0.08).set_color(BLUE) for i in (4, 5)]
            self.play(*set_alpha([ph, *prows, pdots, *meet, lj, rh], DIMMED),
                      *disappear(pads[0][1], pads[1][1]), run_time=0.9)
            self.play(*[GrowArrow(a) for a in arrows],
                      *[p[0].rect.animate.set_stroke(GREEN, 3) for p in pads], run_time=1.2)

    # ------------------------------------------------------------ clip 4: which to write
    def clip4(self):
        with self.say("c3.anti.4") as c:
            cards = [version_card(v, w=2.6) for v in VERSIONS]
            for card in cards:
                card.scale(1.15)
            VGroup(*cards).arrange(RIGHT, buff=0.3).move_to([0, 1.0, 0])
            self.play(*during(disappear(*self.mobjects), 0, 0.45),
                      *during(appear(*cards, lag=0.25, shift=None), 0.5, 1.0), run_time=1.8)

            c.wait_until("notes")
            n1 = T("a good optimiser runs LEFT JOIN … IS NULL and NOT EXISTS", 30, DIM)
            n2 = T("the same way (notes, p. 35)", 30, DIM)
            notes = VGroup(n1, n2).arrange(DOWN, buff=0.15).move_to([0, -1.45, 0])
            self.play(*appear(notes), cards[0].box.animate.set_stroke(YELLOW, 3),
                      cards[3].box.animate.set_stroke(YELLOW, 3), run_time=1.2)

            c.wait_until("reads")
            reads = T("pick the one that reads best", 38).move_to([0, -2.95, 0])
            self.play(*appear(reads), run_time=1.0)

            c.wait_until("best")
            query = Code(S2C.QUERY, 28, lang="sql")
            question = VGroup(T("Which movies", 40, YELLOW), T("have no actors?", 40, YELLOW))
            question.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            VGroup(query, question).arrange(RIGHT, buff=0.9).move_to([0, 0.2, 0])
            self.play(*during(disappear(*cards, notes, reads), 0, 0.45),
                      *during(appear(query, shift=None), 0.5, 1.0), run_time=1.6)
            ne = query.find("NOT EXISTS (")
            nb = token_box(ne, query.line(2), YELLOW, pad=0.16)
            self.play(GrowFromCenter(nb), FlashAround(query, color=BLUE, time_width=1.5), run_time=1.2)
            c.wait_until("Which movies have no row")
            self.play(*appear(question, lag=0.4), run_time=1.2)
            self.play(FlashUnder(question[1], color=YELLOW, time_width=1.5), run_time=1.2)
