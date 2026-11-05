"""Chapter 1, scene 3: SQL's fixed form; written order vs running order; WHERE vs HAVING. Clips c1.form.1 – c1.form.4.

Shared pieces (later scenes: `from lib.paths import load_scene; m = load_scene("ch1_s3_form")`):
- `having_query(size=34)` -> slide 45's query as Code (5 lines: SELECT / FROM / GROUP BY / HAVING / ORDER BY).
- `result_table(size=32)` -> its 3-row result `year | n_movies` (counts GOLD), built at ORIGIN;
  `.header` (VGroup of the two names), `.years`, `.counts` (lists of Mono), `.rules` (VGroup).
- `run_column()` -> the seven clauses in running order, each a numbered BLUE stage box;
  `.stages[name]` -> row with `.num .box .kw`. Rows at pitch 0.72, centred at ORIGIN.
- `YEAR_COUNTS` -> [(year, n_movies)] for 2012-2019 (verified on movies.duckdb).
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

HAVING_SQL = """SELECT year, COUNT(*) AS n_movies
FROM   movies
GROUP BY year
HAVING COUNT(*) > 140
ORDER BY year;"""

WHERE_SQL = """SELECT year, COUNT(*) AS n_movies
FROM   movies
WHERE  n_movies > 140
GROUP BY year
ORDER BY year;"""

RESULT = [(2013, 153), (2014, 146), (2016, 147)]
YEAR_COUNTS = [(2012, 80), (2013, 153), (2014, 146), (2015, 135),
               (2016, 147), (2017, 120), (2018, 127), (2019, 125)]
RUN_ORDER = ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY", "LIMIT"]
RUN_PITCH = 0.72


def having_query(size=34):
    return Code(HAVING_SQL, size=size)


def result_table(size=32):
    hy, hn = Mono("year", size, FG), Mono("n_movies", size, FG)
    xs = (-1.1, 1.2)
    hy.move_to([xs[0], 0.9, 0])
    hn.move_to([xs[1], 0.9, 0])
    years, counts = [], []
    for i, (y, n) in enumerate(RESULT):
        yy = 0.15 - i * 0.6
        years.append(Mono(str(y), size, FG).move_to([xs[0], yy, 0]))
        counts.append(Mono(str(n), size, GOLD).move_to([xs[1], yy, 0]))
    hline = Line([-2.2, 0.55, 0], [2.6, 0.55, 0]).set_stroke(DIM, 2)
    vline = Line([0.0, 1.2, 0], [0.0, -1.35, 0]).set_stroke(DIM, 2)
    rules = VGroup(hline, vline)
    g = VGroup(rules, hy, hn, *years, *counts)
    g.header, g.years, g.counts, g.rules = VGroup(hy, hn), years, counts, rules
    return g


def run_column():
    rows, stages = [], {}
    for i, name in enumerate(RUN_ORDER):
        y = -i * RUN_PITCH
        box = RoundedRectangle(corner_radius=0.1, width=2.8, height=0.56)
        box.set_stroke(BLUE, 2).set_fill(BLUE, 0.1).move_to([0.0, y, 0])
        num = T(str(i + 1), 30, DIM).move_to([1.8, y, 0])
        kw = Mono(name, 30, BLUE).move_to(box)
        row = VGroup(num, box, kw)
        row.num, row.box, row.kw = num, box, kw
        rows.append(row)
        stages[name] = row
    g = VGroup(*rows).move_to(ORIGIN)
    g.stages = stages
    return g


def offsets(c, cues):
    """Seconds from now to each (cue, nth)."""
    return [c.until(q, floor=0.0, nth=n) for q, n in cues]


class Form(NarratedScene):
    def construct(self):
        self.s1 = load_scene("ch1_s1_hook")
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c1.form.1: the form; written order vs running order
    def clip1(self):
        s1 = self.s1
        with self.say("c1.form.1", gap=3.0) as c:
            form = s1.select_form().move_to(ORIGIN)
            self.play(*appear(form, shift=None), run_time=1.2)  # early: the form returns whole, then walked
            self.form = form

            c.wait_until("clauses")
            names = ["select", "from", "where", "group by", "having", "order by", "limit"]
            offs = offsets(c, [(n, 0) for n in names])
            T_ = offs[-1] + 0.9
            self.play(*[time_span(FlashAround(form.slots[s].box, color=YELLOW, time_width=1.5),
                                  max(0, o - 0.1), max(0, o - 0.1) + 0.9)
                        for s, o in zip(s1.FORM_SLOTS, offs)], run_time=T_)

            c.wait_until("once")
            once = [T("×1", 30, DIM).next_to(r.box, RIGHT, buff=0.25) for r in form]
            self.play(*appear(*once, shift=None, lag=0.08), run_time=1.2)

            c.wait_until("order")
            col = run_column()
            shift = 0.55
            form_target = form.copy().move_to([-6.6 + shift + form.width / 2, 0, 0])
            col.move_to([5.9 + shift - col.width / 2, form.get_y(), 0])
            col.shift(UP * (form[0].get_y() - col[0].get_y()))
            self.play(*[m.animate.shift(form_target.get_center() - form.get_center()) for m in (form, *once)],
                      run_time=1.4)
            h_w = T("write", 34, DIM).next_to(form, UP, buff=0.45)
            h_r = T("run", 34, DIM).move_to([col.get_x(), h_w.get_y(), 0])
            c.wait_until("write")
            self.play(*appear(h_w), run_time=0.8)
            c.wait_until("they run")
            self.play(*appear(h_r), *appear(*[col.stages[n].num for n in RUN_ORDER], shift=None, lag=0.05),
                      run_time=1.0)

            c.wait_until("run")
            cues = [("from", 1), ("where", 1), ("group by", 1), ("having", 1),
                    ("select", 1), ("order by", 1), ("limit", 1)]
            offs = offsets(c, cues)
            T_ = min(offs[-1] + 1.0, c.until())
            anims = during(disappear(*once), 0, 0.6 / T_)
            for name, o in zip(RUN_ORDER, offs):
                st = col.stages[name]
                a = max(0.7, o - 0.3) / T_
                b = min(1.0, (o + 0.85) / T_)
                anims += during(fly(form.slots[name].kw, st.kw), a, b)
                anims += during([FadeIn(st.box)], a + 0.6 * (b - a), b)
            self.play(*anims, run_time=T_)
            self.col, self.heads = col, (h_w, h_r)

    # ---- c1.form.2: slide 45's query; group, keep, result
    def clip2(self):
        with self.say("c1.form.2") as c:
            code = having_query().move_to([0, 3.5, 0], aligned_edge=UP)
            c.wait_until("more than")
            sweep_clear(self, *appear(code, shift=None), run_time=1.6)

            base_y, k = -2.8, 2.3 / 153
            xs = [-4.9 + 1.4 * i for i in range(len(YEAR_COUNTS))]
            baseline = Line([-5.7, base_y, 0], [5.7, base_y, 0]).set_stroke(DIM, 2)
            years = [Mono(str(y), 30, FG).move_to([x, base_y - 0.38, 0]) for x, (y, n) in zip(xs, YEAR_COUNTS)]
            bars = [Rectangle(width=0.9, height=n * k).set_stroke(BLUE, 2).set_fill(BLUE, 0.3)
                    .move_to([x, base_y + n * k / 2, 0]) for x, (y, n) in zip(xs, YEAR_COUNTS)]
            counts = [Mono(str(n), 30, GOLD).move_to([x, base_y + 0.3, 0]) for x, (y, n) in zip(xs, YEAR_COUNTS)]

            c.wait_until("group")
            box = token_box(code.line(2), code.line(2))
            self.play(FadeIn(box), *appear(baseline, *years, shift=None, lag=0.06), run_time=1.0)

            src = code.find("movies").get_center()
            chips, drops = [], []
            rng = np.random.default_rng(3)
            for i, x in enumerate(xs):
                for j in range(3):
                    ch = RoundedRectangle(corner_radius=0.03, width=0.5, height=0.1)
                    ch.set_stroke(width=0).set_fill(BLUE, 0.9).move_to(src).set_opacity(0)
                    end = np.array([x, base_y + 0.15, 0])
                    t0 = 0.05 + 0.9 * rng.random()

                    def upd(m, a, s=src.copy(), e=end):
                        m.move_to(interpolate(s, e, a))
                        m.set_fill(opacity=0.9 * np.sin(PI * a))

                    chips.append(ch)
                    drops.append(time_span(UpdateFromAlphaFunc(ch, upd, remover=True), t0, t0 + 0.8))
            grows = [time_span(GrowFromEdge(b, DOWN), 0.4 + 0.1 * i, 1.6 + 0.1 * i) for i, b in enumerate(bars)]
            self.play(*drops, *grows, *during(appear(*counts, shift=None, lag=0.08), 0.7, 1.0), run_time=2.2)

            c.wait_until("having")
            ty = base_y + 140 * k
            thr = DashedLine([-5.7, ty, 0], [5.7, ty, 0], dash_length=0.12).set_stroke(YELLOW, 3)
            thr_l = Mono("140", 30, GOLD).next_to(thr, RIGHT, buff=0.15)
            self.play(Transform(box, token_box(code.line(3), code.line(3))),
                      *during([Create(thr), *appear(thr_l, shift=None)], 0.1, 1.0), run_time=1.4)
            low = [i for i, (y, n) in enumerate(YEAR_COUNTS) if n <= 140]
            c.wait_until("over a hundred")
            self.play(*set_alpha([m for i in low for m in (bars[i], years[i], counts[i])], DIMMED), run_time=1.2)

            c.wait_until("result")
            keep = [i for i in range(len(YEAR_COUNTS)) if i not in low]
            tab = result_table().shift(1.5 * LEFT + 1.3 * DOWN)
            c.wait_until("twenty thirteen")
            anims = during(disappear(thr, thr_l), 0.12, 0.25)
            anims += during([FadeOut(box), *disappear(baseline, *[bars[i] for i in keep],
                                                     *[m for i in low for m in (bars[i], years[i], counts[i])])],
                           0, 0.2)
            anims += during(appear(tab.rules, tab.header, shift=None, lag=0.1), 0.12, 0.35)
            for r, i in enumerate(keep):
                a = 0.25 + 0.25 * r
                anims += during(fly(counts[i], tab.counts[r]), a, a + 0.12)
                anims += during(fly(years[i], tab.years[r]), a + 0.12, a + 0.24)
                anims += during(disappear(years[i], counts[i]), a + 0.15, a + 0.25)
            self.play(*anims, run_time=max(3.2, c.until("eye")))
            settle(self, tab)

            c.wait_until("eye")
            self.play(tab.animate.shift(1.5 * RIGHT), run_time=0.8)
            nums = [T(str(r + 1), 36, YELLOW).move_to([tab.get_left()[0] - 0.5, tab.years[r].get_y(), 0])
                    for r in range(3)]
            self.play(*appear(*nums, shift=None, lag=0.5), run_time=1.8)
            c.wait_until("three", nth=1)
            self.play(FlashAround(nums[2], color=YELLOW, time_width=1.5), run_time=1.0)
            self.code, self.tab, self.nums = code, tab, nums

    # ---- c1.form.3: WHERE instead of HAVING -> binder error; why, in running order
    def clip3(self):
        with self.say("c1.form.3") as c:
            old = self.code
            new = Code(WHERE_SQL, size=34)
            new.move_to(old.get_corner(UL), aligned_edge=UL)
            self.play(*during(disappear(*self.tab, *self.nums), 0, 0.4),
                      *during(edit(old, new), 0.3, 1.0), run_time=2.2)
            code = new

            l1 = Mono("Binder Error: WHERE clause cannot contain aggregates!", 28, RED)
            l3 = Mono("LINE 1: SELECT year, COUNT(*) AS n_movies", 28, RED)
            l1.move_to([0, -0.8, 0])
            l3.next_to(l1, DOWN, buff=0.75).align_to(l1, LEFT)
            cnt = select(l3, "COUNT(*)")[0]
            caret = Mono("^", 28, RED)
            caret.move_to([cnt[0].get_x(), l3.get_bottom()[1] - 0.25, 0])
            c.wait_until(own_word=l1)
            self.play(*appear(l1, l3, caret, shift=None, lag=0.3), run_time=1.4)  # early: the reply is shown whole

            c.wait_until("caret")
            nm = code.find("n_movies", line=2)
            cs = code.find("COUNT(*)", line=0)
            b1 = token_box(nm, code.line(2))
            b2 = token_box(cs, code.line(0))
            arr = Arrow(nm.get_corner(UR) + 0.35 * LEFT + 0.05 * UP, cs.get_bottom() + 0.05 * DOWN, buff=0.08,
                        stroke_width=4, max_tip_length_to_length_ratio=0.3).set_color(YELLOW)
            self.play(FadeIn(b1), FadeIn(b2), GrowArrow(arr), run_time=1.5)
            self.play(caret.animate.set_color(YELLOW), FlashAround(caret, color=YELLOW, time_width=1.5),
                      run_time=1.0)

            c.wait_until("why")
            col = run_column().move_to([-4.6, 0, 0])
            sweep_clear(self, *appear(col, shift=None), run_time=1.6)

            rng = np.random.default_rng(7)
            palette = [BLUE, BLUE, BLUE]
            kinds = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
            rng.shuffle(kinds)
            xs = [-2.2 + 0.52 * i for i in range(len(kinds))]

            def band(name):
                return col.stages[name].get_y()

            dots = [Dot([x, band("FROM"), 0], radius=0.11, color=palette[kd]) for x, kd in zip(xs, kinds)]
            self.play(*appear(*dots, shift=None, lag=0.03), run_time=0.8)

            c.wait_until("the where clause")
            drop = [3, 8, 12]
            wb = col.stages["WHERE"].box
            self.play(wb.animate.set_stroke(YELLOW, 3),
                      *[d.animate.shift(DOWN * RUN_PITCH) for i, d in enumerate(dots) if i not in drop],
                      *[FadeOut(dots[i], shift=0.3 * DOWN) for i in drop], run_time=1.6)
            dots = [d for i, d in enumerate(dots) if i not in drop]
            kinds = [kd for i, kd in enumerate(kinds) if i not in drop]

            c.wait_until("single movies")
            self.play(*[FlashAround(d, color=YELLOW, buff=0.06, time_width=1.5) for d in dots], run_time=1.2)

            c.wait_until("after")
            gb = col.stages["GROUP BY"].box
            centres = [-1.0, 1.6, 4.2]
            moves, clusters = [], []
            for g in range(3):
                mem = [d for d, kd in zip(dots, kinds) if kd == g]
                n = len(mem)
                for j, d in enumerate(mem):
                    moves.append(d.animate.move_to([centres[g] + 0.3 * (j - (n - 1) / 2), band("GROUP BY"), 0]))
                w = 0.3 * (n - 1) + 0.5
                clusters.append(RoundedRectangle(corner_radius=0.18, width=w, height=0.5)
                                .set_stroke(palette[g], 2.5).set_fill(palette[g], 0.08)
                                .move_to([centres[g], band("GROUP BY"), 0]))
            self.play(wb.animate.set_stroke(BLUE, 2), gb.animate.set_stroke(YELLOW, 3),
                      *moves, *during([GrowFromCenter(cl) for cl in clusters], 0.6, 1.0), run_time=1.5)
            hb = col.stages["HAVING"].box
            c.wait_until("sees the groups")
            self.play(gb.animate.set_stroke(BLUE, 2), hb.animate.set_stroke(YELLOW, 3),
                      *[m.animate.shift(DOWN * RUN_PITCH) for m in (*dots, *clusters)],
                      run_time=min(1.2, c.until(floor=0.5)))

    # ---- c1.form.4: WHERE and HAVING are both sigma; the third brick has nowhere to go
    def clip4(self):
        s1 = self.s1
        with self.say("c1.form.4") as c:
            f = MathTex(r"\sigma_{\ldots}", r"\Big(", r"\gamma_{\ldots}", r"\big(", r"\sigma_{\ldots}",
                        r"(\text{movies})", r"\big)", r"\Big)", font_size=110, color=FG)
            f[0].set_color(BLUE)
            f[4].set_color(BLUE)
            f.move_to(0.5 * UP)
            sweep_clear(self, *appear(f, shift=None), run_time=1.2)
            lw = Mono("WHERE", 36, BLUE).move_to([f[4].get_x(), -1.9, 0])
            lh = Mono("HAVING", 36, BLUE).move_to([f[0].get_x(), -1.9, 0])
            aw = Arrow(lw.get_top(), f[4].get_bottom(), buff=0.15, stroke_width=4).set_color(BLUE)
            ah = Arrow(lh.get_top(), f[0].get_bottom(), buff=0.15, stroke_width=4).set_color(BLUE)
            self.play(*appear(lw, shift=None), GrowArrow(aw), run_time=0.9)
            self.play(*appear(lh, shift=None), GrowArrow(ah), run_time=0.9)

            c.wait_until("selection")
            self.play(FlashAround(f[0], color=BLUE, time_width=1.5),
                      FlashAround(f[4], color=BLUE, time_width=1.5), run_time=1.5)

            c.wait_until("two")
            self.play(FlashAround(lw, color=YELLOW, time_width=1.5),
                      FlashAround(lh, color=YELLOW, time_width=1.5), run_time=1.5)

            c.wait_until("used having")
            form = s1.select_form()
            form.move_to([-6.3 + form.width / 2, 0.3, 0])
            filled = {"SELECT": "year, count(*)", "FROM": "movies", "GROUP BY": "year", "HAVING": "count(*) > 140"}
            content = [s1.slot_content(form, n, sql) for n, sql in filled.items()]
            ticks = [s1.slot_tick(form, n) for n in filled]
            for n in filled:
                form.slots[n].box.set_stroke(GREEN, 2.5)
            sweep_clear(self, *appear(form, *content, *ticks, shift=None, lag=0.05), run_time=1.6)  # early: the full form returns whole

            b3 = s1.count_brick()
            gb_box = form.slots["GROUP BY"].box
            hover = np.array([gb_box.get_right()[0] + 0.3 + b3.width / 2, gb_box.get_y(), 0])
            b3.move_to(hover)
            cap = b3.caption.next_to(b3, DOWN, buff=0.3)
            self.play(FadeIn(b3, shift=0.4 * LEFT), *appear(cap, shift=None), run_time=1.2)  # early: the brick's caption from s1
            self.play(b3.box.animate.set_stroke(RED, 4), run_time=0.8)

            c.wait_until("third selection")
            self.play(FlashAround(form.slots["HAVING"].box, color=RED, time_width=1.5), run_time=1.2)
            c.wait_until("second group by")
            self.play(FlashAround(gb_box, color=RED, time_width=1.5), run_time=1.2)

            c.wait_until("nowhere to go")
            start = b3.get_center()

            def shake(m, a):
                m.move_to(start + RIGHT * 0.16 * np.sin(a * 6 * PI) * (1 - a))

            self.play(UpdateFromAlphaFunc(b3, shake), run_time=1.2)
