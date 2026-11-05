"""Chapter 5, scene 6: why denormalise anyway (reads, a stored count, the trade, source of truth).
Clips c5.why.1 – c5.why.4.

Exports (import with `W = load_scene("ch5_s6_why")`), all static, built at ORIGIN:

    W.mini_doc(width=1.9, height=2.4, color=TEAL) -> VGroup, a TEAL document card in ch4 s3's
        doc_card() look (no code): .back (BG backing, opaque), .frame, .brace (Mono "{"), .lines (3 rules).
    W.derived_stack(with_label=True) -> VGroup: .docs [3 mini_docs, back to front, offset 0.3 diagonally],
        .label (TEAL T 32 "derived data, like a cache", under the stack; None without it). ~2.5 x 3.6.
    W.recap_r5() -> VGroup, the scene's final picture (~12.9 x 3.8): .map (ch1 schema map, 0.42),
        .source (GREEN "source of truth (normalised)"), .arrow (YELLOW) + .query (YELLOW "query"),
        .stack (derived_stack(), with its .label as .derived).
Tallies verified on movies.duckdb (-readonly): The Kid = movies 1, ratings 1, has_genre 3, genres 3,
has_position 14, people 10, plays_role 12 = 44 rows. Forum values are made up (illustration only).
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

SCH = load_scene("ch1_s2_schema")
PAGE = load_scene("ch4_s1_hook")
DOC = load_scene("ch4_s3_movie")

TALLY = [("movies", 1), ("ratings", 1), ("has_genre", 3), ("genres", 3),
         ("has_position", 14), ("people", 10), ("plays_role", 12)]


# ---------------------------------------------------------------- shared pieces
def mini_doc(width=1.9, height=2.4, color=TEAL):
    frame = DOC.doc_card(width=width, height=height).frame
    frame.set_stroke(color, 3).set_fill(color, 0.06)
    back = frame.copy().set_stroke(width=0).set_fill(BG, 1)
    brace = Mono("{", int(26 + 8 * height / 2.4), color)
    brace.move_to(frame.get_corner(UL) + np.array([0.35, -0.42, 0]))
    lines = VGroup(*[Line(LEFT * 0.5, RIGHT * 0.5).set_stroke(color, 3) for _ in range(3)])
    lines.arrange(DOWN, buff=0.32 * height / 2.4, aligned_edge=LEFT)
    lines[0].scale(1.25, about_edge=LEFT)
    lines[2].scale(0.7, about_edge=LEFT)
    lines.move_to(frame).shift(0.15 * RIGHT + 0.2 * DOWN)
    g = VGroup(back, frame, brace, lines)
    g.back, g.frame, g.brace, g.lines = back, frame, brace, lines
    return g


def derived_stack(with_label=True):
    docs = [mini_doc() for _ in range(3)]
    for i, d in enumerate(docs):
        d.shift((i - 1) * np.array([0.3, -0.3, 0]))
    g = VGroup(*docs)
    g.docs, g.label = docs, None
    if with_label:
        g.label = T("derived data, like a cache", 32, TEAL)
        g.label.next_to(VGroup(*docs), DOWN, buff=0.45)
        g.add(g.label)
    g.move_to(ORIGIN)
    return g


def source_map(k=0.42):
    m = SCH.schema_map()
    m.remove(m.count_group)
    m.scale(k)
    return m


def recap_r5():
    m = source_map()
    m.move_to([-3.9, 0.6, 0])
    source = T("source of truth (normalised)", 34, GREEN).move_to([-3.9, -1.3, 0])
    arrow = Arrow([-0.95, 0.6, 0], [1.45, 0.6, 0], buff=0, stroke_width=5, color=YELLOW,
                  max_tip_length_to_length_ratio=0.15)
    query = T("query", 32, YELLOW).next_to(arrow, UP, buff=0.18)
    stack = derived_stack()
    stack.shift(np.array([3.95, 0.6, 0]) - VGroup(*stack.docs).get_center())
    g = VGroup(m, source, arrow, query, stack)
    g.map, g.source, g.arrow, g.query, g.stack, g.derived = m, source, arrow, query, stack, stack.label
    return g


def disk_icon(color=DIM):
    w, h, e = 0.9, 0.62, 0.26
    top = Ellipse(width=w, height=e).set_stroke(color, 3).move_to(UP * h / 2)
    sides = VGroup(Line([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0]),
                   Line([w / 2, h / 2, 0], [w / 2, -h / 2, 0])).set_stroke(color, 3)
    bottom = Arc(radius=w / 2, start_angle=PI, angle=PI).stretch(e / w, 1).move_to(
        DOWN * (h / 2 + e / 4)).set_stroke(color, 3)
    return VGroup(top, sides, bottom)


def travel(mob, path, fade=0.15):
    """mob runs along path, fading in at the start and out at the end."""
    def upd(m, a):
        m.move_to(path.point_from_proportion(a))
        m.set_opacity(max(0.0, min(1.0, a / fade, (1 - a) / fade)))
    return UpdateFromAlphaFunc(mob, upd)


def col_pointer(text, table, cell, color):
    """A label under a RowTable, its arrow pointing up at the column of `cell`."""
    bot = table.frame.get_bottom()[1]
    lab = T(text, 32, color).move_to([cell.get_x(), bot - 0.85, 0])
    arr = Arrow(lab.get_top() + UP * 0.06, [cell.get_x(), bot - 0.06, 0], buff=0, stroke_width=3,
                color=color, max_tip_length_to_length_ratio=0.35, tip_length=0.15)
    return VGroup(lab, arr)


# ---------------------------------------------------------------- the balance
PIV = np.array([0.0, 1.5, 0.0])
HALF, STR, TILT = 3.6, 0.4, 10 * DEGREES


def pan(head, lines, color, width=5.8, height=2.0):
    box = RoundedRectangle(corner_radius=0.15, width=width, height=height).set_stroke(DIM, 3)
    box.set_fill(color, 0)
    txt = VGroup(head, *lines).arrange(DOWN, buff=0.16)
    txt.move_to(box)
    g = VGroup(box, txt)
    g.box, g.txt, g.head = box, txt, head
    return g


class Ch5S6Why(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c5.why.1: count the reads ----
    def clip1(self):
        with self.say("c5.why.1") as c:
            q = T("Why denormalise?", 56)
            self.play(*appear(q), run_time=1.0)  # early: the scene's question, asked in this sentence
            c.wait_until("reads")

            # the reads picture sits centred while the rows fly; at {locality} it lifts to make room
            YC = 0.25
            m = source_map(0.55)
            m.shift(RIGHT * (-6.65 - m.get_left()[0]) + UP * (YC - m.get_y()))
            page = PAGE.mock_page().scale(0.44)
            page.move_to([m.get_right()[0] + 0.4 + page.width / 2, YC, 0])
            doc = mini_doc(2.3, 3.0).move_to([5.4, YC, 0])
            sweep_clear(self, *appear(*m.arrow_group, *m.card_group, page, doc, shift=None, lag=0.06),
                        run_time=2.0)  # early: the whole picture first, then walked
            settle(self, m)
            c.wait_until("to show")

            cd = m.cards
            cols = [p for n in cd for p in list(cd[n].rows.values()) + list(cd[n].underlines.values())]
            lights = [a for n, _ in TALLY for a in m.light(n)]
            self.play(*lights, *set_alpha(cols, 0), run_time=min(1.2, c.until("gather")))
            c.wait_until("gather")

            # rows fly from each card to the page, a GOLD tally per card
            rng = np.random.default_rng(4)
            bars, anims, nums = [], [], []
            rt = min(4.0, c.until("doc") - 0.3)
            step, fly_t = (rt - 1.1) / len(TALLY), 0.9
            for k, (name, n) in enumerate(TALLY):
                card = cd[name]
                body = np.array([card.box.get_x(), (card.divider.get_y() + card.box.get_bottom()[1]) / 2, 0])
                num = T(str(n), 34, GOLD).move_to(body)
                nums.append(num)
                t0 = k * step
                anims.append(time_span(FadeIn(num, scale=0.8), t0, t0 + 0.5))
                for i in range(n):
                    b = Rectangle(width=0.26, height=0.07).set_stroke(width=0).set_fill(YELLOW, 1)
                    b.set_opacity(0)
                    a0 = body + np.array([rng.uniform(-0.35, 0.35), rng.uniform(-0.1, 0.1), 0])
                    a1 = page.frame.get_center() + np.array([rng.uniform(-1.0, 1.0), rng.uniform(-1.1, 1.1), 0])
                    path = Line(a0, a1)
                    bars.append(b)
                    s = t0 + 0.4 * i / max(1, n)
                    anims.append(time_span(travel(b, path), s, s + fly_t))
            total = T("44 rows, 7 tables", 38, GOLD).move_to([m.get_x(), m.get_bottom()[1] - 0.5, 0])
            anims.append(time_span(FadeIn(total, shift=0.2 * DOWN), rt - 0.9, rt))
            self.add(*bars)
            self.play(*anims, run_time=rt)
            self.remove(*bars)
            c.wait_until("doc")

            ghost = VGroup(doc.frame.copy(), doc.lines.copy())
            self.play(ghost.animate.scale(0.5).move_to(page.frame).set_opacity(0), run_time=1.4)
            self.remove(ghost)
            one = T("1 document", 38, GOLD)
            one.move_to([min(doc.get_x(), 6.5 - one.width / 2), total.get_y(), 0])
            self.play(*appear(one), run_time=0.9)
            c.wait_until("locality")

            lift = 3.45 - m.get_top()[1]
            loc = T("locality: data read together is stored together", 36, YELLOW).move_to([0, -3.25, 0])
            self.play(*during([x.animate.shift(UP * lift) for x in (m, page, doc, total, one, *nums)], 0, 0.6),
                      *during(appear(loc), 0.55, 1),
                      run_time=1.8)  # early: the definition, read as it is spoken
            c.wait_until("cost")

            dk = disk_icon().move_to([0.9, -1.65, 0])
            dl = T("disk, or another machine", 28, DIM).next_to(dk, DOWN, buff=0.16)
            p_left = ArcBetweenPoints([total.get_x(), total.get_bottom()[1] - 0.1, 0],
                                      dk.get_left() + LEFT * 0.1, angle=PI / 5)
            p_right = ArcBetweenPoints([one.get_x(), one.get_bottom()[1] - 0.1, 0],
                                       dk.get_right() + RIGHT * 0.1, angle=-PI / 5)
            for p, col in ((p_left, GOLD), (p_right, TEAL)):
                p.set_stroke(col, 2, opacity=0.35)
            self.play(*appear(dk, dl, shift=None), Create(p_left), Create(p_right),
                      run_time=min(0.9, c.until(None)))
            # 44 separate trips spread over the whole sentence, against one for the document
            n = 44
            trt = max(1.0, c.until(None) - 0.2)
            dots = [Dot(radius=0.08, color=GOLD).set_opacity(0) for _ in range(n)]
            per = min(0.55, trt * 0.3)
            lag = (trt - per) / (n - 1)
            td = Dot(radius=0.12, color=TEAL).set_opacity(0)
            self.add(*dots, td)
            self.play(*[time_span(travel(d, p_left), i * lag, i * lag + per) for i, d in enumerate(dots)],
                      time_span(travel(td, p_right), 0, min(1.2, trt)), run_time=trt, rate_func=linear)
            self.remove(*dots, td)
            self.page = page

    # ---- c5.why.2: a stored count in a forum ----
    def clip2(self):
        with self.say("c5.why.2") as c:
            th = SCH.RowTable("threads", ["thread_id", "title", "reply_count"],
                              [["1", "Best film?", "3"], ["2", "Lost reels", "2"]],
                              [[FG, FG, GOLD], [FG, FG, GOLD]], size=28, pitch=0.58)
            rows6 = [["11", "1"], ["12", "1"], ["13", "2"], ["14", "1"], ["15", "2"], ["16", "1"]]
            rp = SCH.RowTable("replies", ["reply_id", "thread_id"], rows6[:5], [[FG, FG]] * 5,
                              size=28, pitch=0.58)
            rp6 = SCH.RowTable("replies", ["reply_id", "thread_id"], rows6, [[FG, FG]] * 5 + [[YELLOW] * 2],
                               size=28, pitch=0.58)
            gap = 1.1
            w = th.width + gap + rp.width
            SCH.place(th, left=-w / 2, top=2.6)
            SCH.place(rp, right=w / 2, top=2.6)
            rp6.shift(rp.frame.get_corner(UL) - rp6.frame.get_corner(UL))
            sweep_clear(self, *appear(th, rp, lag=0.5), run_time=2.0)
            c.wait_until("number of replies")

            col = VGroup(th.head[2], th.cell(0, 2), th.cell(1, 2))
            self.play(FlashAround(col, run_time=1.6, time_width=1.5),
                      th.head[2].animate.set_color(GOLD), run_time=1.6)
            c.wait_until("counting")

            # the counting sweep over replies
            def rbox(i):
                r = rp.rows[i]
                return Rectangle(width=rp.frame[0].width - 0.08, height=0.5).move_to(
                    [rp.frame[0].get_x(), r.get_y(), 0]).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.2).set_z_index(-1)
            box = rbox(0)
            self.play(FadeIn(box), *recolor(rp.rows[0], YELLOW), run_time=0.5)
            for i in range(1, 5):
                anims = [Transform(box, rbox(i))]
                if rows6[i][1] == "1":
                    anims += recolor(rp.rows[i], YELLOW)
                self.play(*anims, run_time=0.35)
            cnt = T("counted: 3", 34, GOLD).next_to(rp.frame, DOWN, buff=0.35)
            self.play(*appear(cnt), FadeOut(box), run_time=0.6)
            x = Cross(cnt, stroke_color=RED, stroke_width=6, scale_factor=0.9)
            self.play(GrowFromCenter(x), run_time=min(0.6, c.until("relational")))
            c.wait_until("relational")

            three = th.cell(0, 2)
            den = col_pointer("denormalisation", th, three, YELLOW)
            self.play(FlashAround(three, run_time=1.4, time_width=1.5), *appear(den), run_time=1.4)
            c.wait_until("extra")

            self.play(*during(disappear(cnt, x), 0, 0.4),
                      *during(recolor([g for i in range(5) for g in rp.rows[i]], FG), 0, 0.4),
                      *during([ReplacementTransform(rp.frame, rp6.frame)], 0.3, 0.8),
                      *during(appear(rp6.rows[5], shift=None), 0.6, 1), run_time=1.4)
            self.add(rp6.rows[5])
            c.wait_until("every new reply")

            four = Mono("4", 28, GOLD).move_to(three)
            plus = Mono("+1", 32, GOLD, weight=BOLD).next_to(th.frame, RIGHT, buff=0.18).set_y(three.get_y())
            sec = col_pointer("a second write", th, three, RED)
            rt = max(0.8, min(1.4, c.remaining - 2.0))
            self.play(*swap(three, four), *swap(den, sec), *during(appear(plus, shift=0.2 * UP), 0.4, 0.8),
                      time_span(FlashAround(four, color=RED, time_width=1.5), 0.55 * rt, rt),
                      run_time=rt)  # early: the two writes land with the sentence so they hold before it ends
            plus.set_color(GOLD).set_opacity(1)

    # ---- c5.why.3: the trade ----
    def clip3(self):
        with self.say("c5.why.3") as c:
            beam = Line(PIV + LEFT * HALF, PIV + RIGHT * HALF).set_stroke(FG, 6)
            post = Line(PIV, [0, -2.45, 0]).set_stroke(FG, 5)
            base = Polygon([-0.9, -2.9, 0], [0.9, -2.9, 0], [0.3, -2.45, 0], [-0.3, -2.45, 0])
            base.set_stroke(FG, 3).set_fill(DIM, 0.5)
            dot = Dot(PIV, radius=0.11, color=FG)
            gain = pan(T("Reads", 38, GREEN), [T("fast and simple", 30)], GREEN)
            price = pan(T("Writes", 38, RED), [T("more data to write and store", 30),
                                             T("every copy kept consistent", 30)], RED)
            gain.txt.move_to(gain.box)
            strings = [Line(beam.get_start(), beam.get_start() + DOWN * STR),
                       Line(beam.get_end(), beam.get_end() + DOWN * STR)]
            for s in strings:
                s.set_stroke(FG, 3)
            pans = [gain, price]

            def lay(th):
                ends = [PIV + HALF * s * np.array([np.cos(th), np.sin(th), 0]) for s in (-1, 1)]
                beam.put_start_and_end_on(ends[0], ends[1])
                for e, s, p in zip(ends, strings, pans):
                    s.put_start_and_end_on(e, e + DOWN * STR)
                    p.move_to(e + DOWN * (STR + p.box.height / 2))
            lay(0)
            frame_parts = [post, base, beam, dot, *strings, gain.box, price.box]
            sweep_clear(self, *appear(*frame_parts, shift=None, lag=0.05), run_time=1.8)
            c.wait_until(own_word=gain.head)
            self.play(restyle(gain.box, outline=GREEN), *appear(gain.txt), run_time=1.0)
            c.wait_until(own_word=price.head)
            self.play(restyle(price.box, outline=RED), *appear(price.txt), run_time=1.0)  # early: the pan's whole load, read through this sentence
            c.wait_until("mostly")

            choose = T("mostly read, rarely updated → denormalise", 40, YELLOW).move_to([0, 3.25, 0])
            rig = VGroup(beam, *strings, gain, price)
            self.play(*appear(choose),
                      time_span(UpdateFromAlphaFunc(rig, lambda m, a: lay(TILT * smooth(a))), 0.4, 2.4),
                      run_time=2.4)
            self.add(gain.txt, price.txt)
            c.wait_until("movies")

            page = PAGE.mock_page().scale(0.5).move_to([-1.0, -0.65, 0])
            bal = [post, base, beam, dot, *strings, gain, price]
            self.play(*during(disappear(*bal), 0, 0.45), *during(appear(page, shift=None), 0.5, 1),
                      run_time=1.2)
            fr = page.frame
            reads = []
            for i in range(8):
                y = fr.get_top()[1] - 0.35 - i * (fr.height - 0.7) / 7
                reads.append(Arrow([3.4, y, 0], [fr.get_right()[0] + 0.05, y, 0], buff=0, stroke_width=4,
                                   color=GREEN, max_tip_length_to_length_ratio=0.12))
            rlab = T("read", 34, GREEN).next_to(reads[0], RIGHT, buff=0.25).set_y(fr.get_y())
            edit_a = Arrow([-5.6, fr.get_y(), 0], [fr.get_left()[0] - 0.05, fr.get_y(), 0], buff=0,
                           stroke_width=4, color=RED, max_tip_length_to_length_ratio=0.15)
            elab = T("credits change", 30, RED).next_to(edit_a, DOWN, buff=0.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in reads], lag_ratio=0.15), *appear(rlab),  # early: the reads land first so the rare edit can hold
                      run_time=min(1.2, max(0.6, c.remaining - 3.2)))
            # the rare edit lands ~2 s before the clip ends, so it holds on screen
            self.play(GrowArrow(edit_a), *appear(elab),  # early: the rare edit lands so it holds before the line ends
                      run_time=max(0.6, min(1.0, c.remaining - 2.0)))

    # ---- c5.why.4: source of truth, derived data ----
    def clip4(self):
        with self.say("c5.why.4") as c:
            rule = T("Best if you can regenerate the denormalised data at any time.", 32).move_to([0, -3.0, 0])
            sweep_clear(self, run_time=1.0)
            c.wait_until(own_word=rule)
            self.play(*appear(rule), run_time=1.0)
            c.wait_until("source")

            r = recap_r5().shift(0.35 * UP)
            m = r.map
            self.play(*appear(*m.arrow_group, *m.card_group, shift=None, lag=0.05), run_time=1.4)
            settle(self, m)
            self.play(*appear(r.source), run_time=1.0)
            c.wait_until("derived")

            docs = r.stack.docs
            self.play(GrowArrow(r.arrow), *during(appear(*docs, shift=None, lag=0.3), 0.3, 1),
                      run_time=1.6)
            c.wait_until("like a cache")
            self.play(*appear(r.derived), run_time=1.0)
            c.wait_until(own_word=r.query)
            self.play(*appear(r.query), run_time=0.9)
            c.wait_until("broken")

            front = docs[2]
            fr = front.frame
            crack = VMobject().set_points_as_corners([
                fr.get_top() + LEFT * 0.15, fr.get_center() + np.array([0.2, 0.55, 0]),
                fr.get_center() + np.array([-0.25, 0.1, 0]), fr.get_center() + np.array([0.25, -0.35, 0]),
                fr.get_bottom() + RIGHT * 0.05]).set_stroke(RED, 5)
            self.play(restyle(fr, outline=RED), *recolor([front.brace, *front.lines], RED),
                      Create(crack), run_time=1.0)
            c.wait_until("regen")

            self.play(*disappear(front, crack), run_time=0.8)
            new = mini_doc(color=GREEN).move_to(front)
            self.play(VShowPassingFlash(r.arrow.copy().set_stroke(GREEN, 8), time_width=0.6, run_time=1.0),
                      time_span(FadeIn(new), 0.6, 1.3), run_time=1.3)
            self.play(*recolor(select(rule, "regenerate")[0], GREEN), run_time=min(0.8, c.until(None)))
