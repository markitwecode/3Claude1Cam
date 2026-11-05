"""Chapter 2, scene 2: matching a single vertex, (m:Movie). Clips c2.vertex.1 – c2.vertex.5."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- building blocks
TS = 28                     # table text size
X0 = -6.3                   # table's left edge


def vertex(r=1.4, name_size=72, label_size=44):
    """BLUE Movie circle: VGroup(circle, name m, label Movie under it)."""
    c = Circle(radius=r).set_stroke(BLUE, 6).set_fill(BLUE, 0.15)
    n = Mono("m", name_size, color=YELLOW).move_to(c)
    lab = Mono("Movie", label_size, color=BLUE).next_to(c, DOWN, buff=0.18)
    return VGroup(c, n, lab)


def put_vertex(v, center):
    v.shift(np.array(center) - v[0].get_center())
    return v


def card(lines, size=30):
    """Property card: VGroup(box, VGroup(lines))."""
    texts = VGroup(*[Mono(s, size, t2c={"1921": GOLD}) for s in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.12, width=texts.width + 0.45,
                           height=texts.height + 0.4).set_stroke(BLUE, 2.5).set_fill(BG, 1)
    box.move_to(texts)
    return VGroup(box, texts)


def top_left(mob, x, top):
    mob.shift([x - mob.get_left()[0], top - mob.get_top()[1], 0])
    return mob


def cols():
    x1 = X0 + Mono("Gone Baby Gone", TS).width + 0.45
    x2 = x1 + Mono("m.year", TS).width + 0.45
    return X0, x1, x2


def cell(s, x, top, color=FG):
    return top_left(Mono(s, TS, color=color), x, top)


def vertex_hero():
    """The hero as it stands after {braces}, beside (m:Movie {title: 'The Kid', year: 1921}); at ORIGIN."""
    v = vertex(0.8, 52, 32)
    k = card(["title: 'The Kid'", "year: 1921"])
    k.next_to(v[0], RIGHT, buff=0.3)
    code = Code("(m:Movie {title: 'The Kid', year: 1921})", size=32)
    top = VGroup(v, k)
    code.next_to(top, DOWN, buff=0.5)
    g = VGroup(v, k, code)
    return g.move_to(ORIGIN)


class Vertex(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ circle -> (m:Movie)
    def clip1(self):
        with self.say("c2.vertex.1") as c:
            v = put_vertex(vertex(), [-3.4, 0.0, 0])
            self.v = v
            self.play(GrowFromCenter(v[0]), *appear(v[1], v[2], lag=0.3),  # early: the whole vertex first, then walked
                      run_time=min(1.6, c.until("circle")))
            c.wait_until("circle")

            code = Code("(m:Movie)", size=64).move_to([3.3, 1.0, 0])
            op, cl = code.find("("), code.find(")")
            ghost = v[0].copy().set_fill(opacity=0)
            ell = Ellipse(width=code.width + 0.5, height=code.height + 0.8).move_to(code)
            ell.set_stroke(BLUE, 4)
            self.play(Transform(ghost, ell), run_time=1.5)
            self.play(FadeOut(ghost), FadeIn(op), FadeIn(cl), run_time=0.9)
            c.wait_until("round brackets")
            box = token_box(VGroup(op, cl), code)
            lab = T("circle", 32, YELLOW).next_to(box, UP, buff=0.3)
            self.play(FadeIn(box), *appear(lab), run_time=1.0)

            c.wait_until("name")
            m_dst = code.find("m")
            self.play(*fly(v[1], m_dst), run_time=1.5)
            box2 = token_box(m_dst, code)
            lab2 = T("name", 32, YELLOW).next_to(box2, UP, buff=0.3).set_y(lab.get_y())
            self.play(Transform(box, box2), *appear(lab2), run_time=1.2)

            c.wait_until("label")
            mv_dst = code.find(":Movie")
            self.play(*fly(v[2], code.find("Movie")), *during([FadeIn(code.find(":"))], 0.6, 1), run_time=1.5)
            box3 = token_box(mv_dst, code)
            lab3 = T("label", 32, YELLOW).next_to(box3, DOWN, buff=0.3)
            self.play(Transform(box, box3), *appear(lab3), run_time=1.2)
        settle(self, code)
        self.code, self.box, self.labs = code, box, [lab, lab2, lab3]

    # ------------------------------------------------------------ MATCH ... RETURN, the table
    def clip2(self):
        v = self.v
        with self.say("c2.vertex.2") as c:
            code2 = top_left(Code("MATCH (m:Movie)", size=32), -5.6, 3.45)
            self.play(*during(disappear(self.box, *self.labs), 0, 0.35),
                      *during(edit(self.code, code2), 0.15, 1),
                      run_time=max(1.2, min(1.6, c.until("return"))))
            c.wait_until("return")
            code3 = top_left(Code("MATCH (m:Movie)\nRETURN m.title", size=32), -5.6, 3.45)
            v.target = put_vertex(vertex(0.7, 48, 32), [4.8, 2.6, 0])
            self.play(*edit(code2, code3), MoveToTarget(v), run_time=1.6)

            c.wait_until("run")
            x0, x1, x2 = cols()
            hdr = cell("m.title", x0, 0.85, DIM)
            rule = Line([x0 - 0.1, 0.42, 0], [x0 + Mono("Blue Is the Warmest Colour", TS).width + 0.1, 0.42, 0])
            rule.set_stroke(DIM, 2)
            titles = ["The Kid", "Titane", "Gone Baby Gone", "The Dig", "Blue Is the Warmest Colour"]
            tops = [0.2 - 0.52 * i for i in range(6)]
            rows = [cell(s, x0, tops[i]) for i, s in enumerate(titles)]
            dots = top_left(T("…", 34, DIM), x0, tops[5])
            self.play(*appear(hdr, rule, *rows, dots, lag=0.2), run_time=2.0)  # early: a result table, read whole
            foot = top_left(T("2935 rows", 34, GOLD), x0, -2.95)
            c.wait_until("two thousand", own_word=foot)
            self.play(*appear(foot), run_time=1.0)

            c.wait_until("more")
            code4 = top_left(Code("MATCH (m:Movie)\nRETURN m.title, m.year, m.genres", size=32), -5.6, 3.45)
            self.play(*edit(code3, code4), run_time=1.6)
            c.wait_until("each row")
            dots.generate_target()
            top_left(dots.target, x0, tops[3])
            foot.generate_target()
            top_left(foot.target, x0, tops[3] - 0.85)
            self.play(*during(disappear(rows[3], rows[4]), 0, 0.45),
                      *during([MoveToTarget(dots), MoveToTarget(foot)], 0.35, 1), run_time=1.1)
            years = ["1921", "2021", "2007"]
            genres = ["['Comedy', 'Drama', 'Family']", "['Drama', 'Horror', 'Sci-Fi']",
                      "['Crime', 'Drama', 'Mystery']"]
            h1, h2 = cell("m.year", x1, 0.85, DIM), cell("m.genres", x2, 0.85, DIM)
            ycells = [cell(s, x1, tops[i], GOLD) for i, s in enumerate(years)]
            gcells = [cell(s, x2, tops[i]) for i, s in enumerate(genres)]
            wide = Line([x0 - 0.1, 0.42, 0], [gcells[2].get_right()[0] + 0.1, 0.42, 0]).set_stroke(DIM, 2)
            self.play(Transform(rule, wide), *appear(h1, h2, *[m for p in zip(ycells, gcells) for m in p], lag=0.15),
                      run_time=1.8)

            c.wait_until("list")
            gbox = SurroundingRectangle(gcells[0], color=YELLOW, buff=0.1)
            self.play(FadeIn(gbox), run_time=1.0)
            c.wait_until("one property")
            k = card(["genres: [...]"], size=28)
            k.next_to(v[2], DOWN, buff=0.2).set_x(v[0].get_x())
            self.play(*appear(k), run_time=1.0)
        self.k = k
        self.code = code4
        self.table = VGroup(hdr, rule, rows[0], rows[1], rows[2], dots, foot, h1, h2, *ycells, *gcells, gbox)
        self.table_parts = [hdr, rule, rows[0], rows[1], rows[2], dots, foot, h1, h2, *ycells, *gcells, gbox]

    # ------------------------------------------------------------ SQL ghost
    def clip3(self):
        code = self.code
        with self.say("c2.vertex.3") as c:
            sql = top_left(Code("SELECT …\nFROM …\nWHERE …", size=32, lang="sql"), 0.4, 0.15)
            sql.set_opacity(0.75)
            c.wait_until("sequel")
            sweep_clear(self, *appear(sql, shift=None), keep=[code, self.v, self.k], run_time=1.4)
            c.wait_until("plays the part")
            ret, sel = code.find("RETURN"), sql.find("SELECT")
            a1 = Arrow(ret.get_bottom() + 0.1 * DOWN, sel.get_left() + 0.15 * LEFT, buff=0,
                       stroke_width=4, color=GREEN, tip_length=0.2)
            self.play(GrowArrow(a1), *flash([ret, sel], color=GREEN), run_time=1.5)

            c.wait_until("from")
            mt = code.find("MATCH")
            start = mt.get_left() + 0.12 * LEFT
            fr, wh = sql.find("FROM"), sql.find("WHERE")
            arcs = [CurvedArrow(start, g.get_left() + 0.15 * LEFT, angle=2.4, color=GREEN,
                                tip_length=0.2).set_stroke(width=4) for g in (fr, wh)]
            self.play(Create(arcs[0]), Create(arcs[1]), *flash([mt], color=GREEN), run_time=1.8)

            c.wait_until("comes from")
            self.play(FlashAround(fr, color=GREEN, run_time=1.2, time_width=1.5))
            c.wait_until("look like")
            self.play(FlashAround(wh, color=GREEN, run_time=1.2, time_width=1.5))
        self.ghost = [sql, a1, *arcs]

    # ------------------------------------------------------------ WHERE vs braces
    def clip4(self):
        v, code = self.v, self.code
        with self.say("c2.vertex.4") as c:
            code.generate_target()
            top_left(code.target, -6.1, 0.85)
            v.target = put_vertex(vertex(0.8, 52, 32), [-2.6, 2.45, 0])
            self.play(*during(disappear(*self.ghost, self.k), 0, 0.4),
                      *during([MoveToTarget(code)], 0.2, 0.65),
                      *during([MoveToTarget(v)], 0.55, 1), run_time=min(2.0, c.until("where") - 1.0))
            q = T("The Kid?", 48, YELLOW).move_to([0.4, 2.45, 0])
            self.play(*appear(q), run_time=min(0.9, c.until("where")))

            c.wait_until("where")
            wcode = top_left(Code("MATCH (m:Movie)\nWHERE m.title = 'The Kid' AND m.year = 1921\n"
                                  "RETURN m.title, m.year, m.genres;", size=32), -6.1, 0.85)
            self.play(*edit(code, wcode), run_time=1.8)
            c.wait_until("equals")
            self.play(*flash([wcode.find("m.title = 'The Kid'")]), run_time=1.2)
            c.wait_until("nineteen")
            self.play(*flash([wcode.find("m.year = 1921")]), run_time=1.2)

            c.wait_until("braces")
            bcode = top_left(Code("MATCH (m:Movie {title: 'The Kid', year: 1921})\n"
                                  "RETURN m.title, m.year, m.genres;", size=32), -6.1, 0.85)
            mid = top_left(Code("MATCH (m:Movie {title: 'The Kid', year: 1921})\n \n"
                                "RETURN m.title, m.year, m.genres;", size=32), -6.1, 0.85)
            self.play(*edit(wcode, mid), run_time=1.8)
            self.play(*edit(mid, bcode), run_time=0.9)
            k = card(["title: 'The Kid'", "year: 1921"])
            k.next_to(v[0], RIGHT, buff=0.3)
            self.play(*during(disappear(q), 0, 0.45), *during([FadeIn(k[0])], 0.45, 1), run_time=1.0)
            src_t = bcode.find("title: 'The Kid'")
            src_y = bcode.find("year: 1921")
            self.play(*during(fly(src_t, k[1][0]), 0, 0.6), *during(fly(src_y, k[1][1]), 0.4, 1),
                      run_time=2.0)
            settle(self, k)

            c.wait_until("same")
            x0, x1, x2 = cols()
            hdr = [cell("m.title", x0, -1.25, DIM), cell("m.year", x1, -1.25, DIM),
                   cell("m.genres", x2, -1.25, DIM)]
            row = [cell("The Kid", x0, -1.9), cell("1921", x1, -1.9, GOLD),
                   cell("['Comedy', 'Drama', 'Family']", x2, -1.9)]
            rule = Line([x0 - 0.1, -1.67, 0], [row[2].get_right()[0] + 0.1, -1.67, 0]).set_stroke(DIM, 2)
            self.play(*appear(*hdr, rule, *row, lag=0.12), run_time=1.5)
            one = top_left(T("1 row", 34, GOLD), x0, -2.7)
            tick = check_mark().next_to(one, RIGHT, buff=0.3)
            self.play(*appear(one), GrowFromCenter(tick), run_time=1.0)
            c.wait_until("The Kid", nth=1)
            self.play(FlashUnder(row[0], run_time=1.0, time_width=1.5))
            c.wait_until("comedy")
            self.play(FlashUnder(row[2], run_time=1.2, time_width=1.5))

    # ------------------------------------------------------------ case sensitivity
    def clip5(self):
        with self.say("c2.vertex.5") as c:
            q1 = Code("match (m:Movie) return m.title", size=36)
            q1.move_to([-1.5, 1.3, 0])
            c.wait_until("keywords")
            cap1 = T("keywords: any case", 32, DIM)
            sep = T("·", 32, DIM)
            cap2 = T("labels and property names: exact", 32, DIM)
            VGroup(cap1, sep, cap2).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
            sweep_clear(self, *appear(q1, shift=None), keep=[], run_time=1.6)
            self.play(*appear(cap1), run_time=0.9)
            c.wait_until("capitals")
            self.play(*flash([q1.find("match"), q1.find("return")]), run_time=1.4)
            c.wait_until("as in sequel")
            r1 = T("2935 rows", 36, GOLD).next_to(q1, RIGHT, buff=0.6)
            t1 = check_mark().next_to(r1, RIGHT, buff=0.3)
            self.play(*appear(r1), GrowFromCenter(t1), run_time=1.0)  # early: the query's reply, not a spoken label

            c.wait_until("data")
            self.play(*appear(sep, cap2), run_time=1.0)
            self.play(*flash([q1.find("Movie"), q1.find("title")]), run_time=1.4)

            c.wait_until("wrong")
            q2 = Code("MATCH (m:movie) RETURN m.title", size=36)
            q2.align_to(q1, LEFT).set_y(-0.5)
            self.play(*appear(q2, shift=None), run_time=1.0)
            c.wait_until("lower-case")
            mbox = token_box(VGroup(q2.find("movie")[0]), q2, color=RED, pad=0.14)
            self.play(FadeIn(mbox), run_time=0.8)
            c.wait_until("zero rows")
            r2 = T("0 rows", 36, RED).next_to(q2, RIGHT, buff=0.6).align_to(r1, LEFT)
            self.play(*appear(r2), run_time=1.0)
            c.wait_until("spelling")
            # colour pulse (no stroke path, so nothing can be left behind)
            self.play(cap2.animate(rate_func=there_and_back).set_color(YELLOW), run_time=1.6)
