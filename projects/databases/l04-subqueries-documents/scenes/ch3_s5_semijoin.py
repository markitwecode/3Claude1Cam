"""Chapter 3, scene 5: EXISTS is the semijoin. Clips c3.semi.1 – c3.semi.4.

Shared pieces (later scenes: `from lib.paths import load_scene; m = load_scene("ch3_s5_semijoin")`):
- `plan_box(op, detail=None, size=32)` -> DuckDB EXPLAIN box at ORIGIN: BLUE rounded frame, op Mono FG,
  DIM rule, detail Mono DIM (str or list of str); `.box .op .rule .details` (list).
- `zimmer_tag(size=36)` -> GOLD T "Hans Zimmer × 72".
- `counts(size=72)` -> VGroup(left, right): GOLD "3,281" over DIM Mono "JOIN", GOLD "1,086" over
  "EXISTS", 5 apart, at ORIGIN; `.join_n .exists_n` (the numbers), `.left .right`.
- `join_code(size)`, `exists_code(size, colored)`, `distinct_code(size)`: the three queries (Code, verbatim).
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
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- shared pieces
def plan_box(op, detail=None, size=32):
    op_t = Mono(op, size, FG, weight=BOLD)
    if detail is None:
        lines = []
    elif isinstance(detail, str):
        lines = [detail]
    else:
        lines = list(detail)
    dets = [Mono(d, size - 4, DIM) for d in lines]
    w = max([op_t.width] + [d.width for d in dets]) + 0.7
    parts = [op_t]
    rule = None
    if dets:
        rule = Line(LEFT * (w / 2 - 0.15), RIGHT * (w / 2 - 0.15)).set_stroke(DIM, 1.5)
        parts.append(rule)
        parts += dets
    inner = VGroup(*parts).arrange(DOWN, buff=0.18)
    box = RoundedRectangle(corner_radius=0.08, width=w, height=inner.height + 0.5).set_stroke(BLUE, 2.5)
    box.move_to(inner)
    g = VGroup(box, *parts).move_to(ORIGIN)
    g.box, g.op, g.rule, g.details = box, op_t, rule, dets
    return g


def zimmer_tag(size=36):
    return T("Hans Zimmer × 72", size, GOLD)


def counts(size=72):
    def col(n, lab):
        num = T(n, size, GOLD)
        tag = Mono(lab, 30, DIM).next_to(num, DOWN, buff=0.3)
        return VGroup(num, tag)
    left, right = col("3,281", "JOIN"), col("1,086", "EXISTS")
    left.move_to(LEFT * 2.5)
    right.move_to(RIGHT * 2.5)
    g = VGroup(left, right).move_to(ORIGIN)
    g.left, g.right, g.join_n, g.exists_n = left, right, left[0], right[0]
    return g


def join_code(size=28):
    return Code("SELECT name FROM people AS p\nJOIN has_position AS hp\n  ON hp.person_id = p.person_id\n"
                " AND hp.position = 'composer'\nORDER BY name;", size=size)


def exists_code(size=28, colored=False):
    code = Code("SELECT name FROM people AS p\nWHERE EXISTS (\n    SELECT 1 FROM has_position AS hp\n"
                "    WHERE hp.person_id = p.person_id\n      AND hp.position = 'composer'\n)\n"
                "ORDER BY name;", size=size)
    if colored:
        for g in outer_p(code):
            g.set_color(YELLOW)
    return code


def outer_p(code):
    """Glyphs of the outer person in exists_code: the alias `p` and `p.person_id` in the subquery."""
    return [code.find("AS p", line=0)[-1], *code.find("p.person_id", line=3, nth=1)]


def distinct_code(size=32):
    return Code("SELECT DISTINCT p.person_id, p.name\nFROM people AS p\nJOIN has_position AS hp\n"
                "  ON hp.person_id = p.person_id\n AND hp.position = 'composer';", size=size)


def result_col(names, count, size=30, pitch=0.5):
    head = Mono("name", size, DIM)
    rows = [Mono(n, size, FG) for n in names]
    dot = Mono("·", size, DIM)
    for i, r in enumerate(rows + [dot]):
        r.move_to([0, -(i + 1) * pitch - 0.1, 0]).align_to(head, LEFT)
    w = max(r.width for r in rows) + 0.2
    rule = Line(head.get_corner(DL) + 0.1 * DOWN + 0.1 * LEFT,
                head.get_corner(DL) + 0.1 * DOWN + (w - 0.1) * RIGHT).set_stroke(DIM, 2)
    cnt = T(f"{count} rows", 36, GOLD).next_to(dot, DOWN, buff=0.35).align_to(head, LEFT)
    g = VGroup(head, rule, *rows, dot, cnt)
    g.head, g.rule, g.rows, g.dot, g.count = head, rule, rows, dot, cnt
    return g


def place_col(g, left_x=1.2, head_y=1.9):
    g.shift([left_x - g.head.get_left()[0], head_y - g.head.get_y(), 0])
    return g


def chip(text, color=FG, width=1.9, size=30, mono=False):
    lab = (Mono(text, size, color) if mono else T(text, size, color))
    box = RoundedRectangle(corner_radius=0.08, width=width, height=0.5).set_stroke(color, 2)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.lab = box, lab
    return g


class Semijoin(NarratedScene):
    def construct(self):
        q = self.clip1()
        self.clip2(q)
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c3.semi.1
    def clip1(self):
        with self.say("c3.semi.1") as c:
            ne = Mono("NOT EXISTS", 64, BLUE)
            self.play(*appear(ne, shift=None), run_time=0.8)  # early: s4's closing words, carried over
            c.wait_until("the word not")
            ex = Mono("EXISTS", 64, BLUE)
            self.play(*edit(ne, ex), run_time=1.2)
            c.wait_until("ask")
            self.play(ex.animate.scale(0.75).move_to(UP * 2.0), run_time=1.0)
            q = T("Who is credited as a composer on at least one movie?", 36, YELLOW).move_to(DOWN * 0.3)
            c.wait_until(own_word=q)
            self.play(*appear(q), run_time=1.0)

            c.wait_until("join")
            self.play(*during(disappear(ex), 0, 0.4),
                      *during([q.animate.scale(32 / 36).move_to(UP * 3.35)], 0.4, 1), run_time=1.4)
            code = join_code(28)
            code.move_to([0, 0.6, 0]).align_to([-6.6, 0, 0], LEFT)
            self.play(*appear(code), run_time=1.0)  # early: the query is shown whole, then read
            c.wait_until("the position is composer")
            self.play(FlashUnder(code.find("hp.position = 'composer'", line=3), run_time=1.5,
                                 time_width=1.5), run_time=1.5)

            c.wait_until("many")
            res = place_col(result_col(["A.C. Newman", "A.R. Rahman", "A.R. Rahman", "A.R. Rahman"], "3,281"))
            self.play(*appear(res.head, res.rule, *res.rows, res.dot, lag=0.2), run_time=1.5)
            c.wait_until(own_word=res.count)
            self.play(*appear(res.count),
                      *[FlashAround(r, run_time=1.5, time_width=1.5) for r in res.rows[1:]], run_time=1.5)

            c.wait_until("zimmer")
            zt = zimmer_tag().next_to(res.count, DOWN, buff=0.45).align_to(res.count, LEFT)
            self.play(*appear(zt), run_time=1.0)

            c.wait_until("credit")
            boxes, links = [], []
            for r in res.rows:
                b = chip("composer", DIM, width=2.1, size=28, mono=True).move_to([5.35, r.get_y(), 0])
                ln = Line(r.get_right() + 0.15 * RIGHT, b.get_left() + 0.08 * LEFT).set_stroke(DIM, 2)
                boxes.append(b)
                links.append(ln)
            self.play(*[Create(ln) for ln in links], *appear(*boxes, shift=None, lag=0.2), run_time=1.5)
            cap = T("one row per credit", 32, FG).move_to([4.0, -3.2, 0])
            c.wait_until("one row per credit")
            self.play(*appear(cap), run_time=1.0)
        return q

    # ------------------------------------------------------------ c3.semi.2
    def clip2(self, q):
        with self.say("c3.semi.2") as c:
            ec = exists_code(28)
            ec.move_to([0, 0.4, 0]).align_to([-6.6, 0, 0], LEFT)
            sweep_clear(self, *appear(ec), keep=[q])

            c.wait_until("code")
            others = [g for i in (0, 1, 2, 5, 6) for g in ec.line(i)]
            self.play(*set_alpha(others, 0.4), run_time=1.0)
            c.wait_until("this person's")
            pp = ec.find("p.person_id", line=3, nth=1)
            self.play(*recolor(outer_p(ec), YELLOW), FlashUnder(pp, run_time=1.2), run_time=1.2)

            c.wait_until("once")
            res = place_col(result_col(["A.C. Newman", "A.R. Rahman", "Aaron May", "Aaron Zigman"], "1,086"),
                            left_x=2.5)
            self.play(*set_alpha(others, 1), *appear(res.head, res.rule, *res.rows, res.dot, lag=0.15),
                      run_time=1.5)
            self.play(*appear(res.count), run_time=0.8)

            c.wait_until("each")
            cn = self.cn = counts(60).move_to([0, -2.55, 0])
            self.play(*appear(cn.left[1], cn.right[1], shift=None), *appear(cn.join_n),
                      *fly(select(res.count, "1,086")[0], cn.exists_n), run_time=1.5)

    # ------------------------------------------------------------ c3.semi.3
    def clip3(self):
        with self.say("c3.semi.3") as c:
            alg = MathTex(r"\text{people}", r"\ltimes_{\text{person\_id}}", r"\big(",
                          r"\sigma_{\text{position}=\text{'composer'}}(\text{has\_position})", r"\big)",
                          font_size=54, color=BLUE)
            if alg.width > 11.5:
                alg.scale_to_fit_width(11.5)
            alg.move_to(UP * 2.6)
            lab = T("semijoin", 30, DIM).next_to(alg[1], UP, buff=0.25)
            sweep_clear(self, *appear(alg, shift=None), keep=[self.cn])
            c.wait_until(own_word=lab)
            self.play(*appear(lab), run_time=1.0)

            c.wait_until("expr")
            brace = Brace(alg[3], DOWN, buff=0.12, color=DIM)
            blab = T("only the composer credits", 30, FG).next_to(brace, DOWN, buff=0.12)
            self.play(GrowFromCenter(brace), *disappear(self.cn), run_time=1.0)
            c.wait_until("filtered down")
            self.play(*appear(blab), run_time=1.0)  # early: names what 'filtered down to the composers' says

            c.wait_until("keeps")
            ys = [-0.05, -0.65, -1.25, -1.85]
            credits = [chip("composer", DIM, width=2.3, size=28, mono=True).move_to([-0.6, y, 0]) for y in ys]
            people = [chip(n, BLUE, width=1.9).move_to([-4.8, y, 0])
                      for n, y in (("Ana", -0.65), ("Ben", -1.85), ("Cleo", -2.8))]
            links = [Line(people[0].get_right(), credits[i].get_left()).set_stroke(DIM, 2) for i in range(3)]
            links.append(Line(people[1].get_right(), credits[3].get_left()).set_stroke(DIM, 2))
            h_people = T("people", 30, DIM).move_to([-4.8, 0.62, 0])
            h_cred = T("composer credits", 30, DIM).move_to([-0.6, 0.62, 0])
            self.play(*appear(h_people, *people, lag=0.15),
                      *appear(h_cred, *credits, lag=0.1), *[Create(ln) for ln in links], run_time=1.5)
            c.wait_until("at least one match")
            outs = [chip(n, GREEN, width=1.9).move_to([2.9, y, 0]) for n, y in (("Ana", -0.65), ("Ben", -1.85))]
            h_out = T("result", 30, DIM).move_to([2.9, 0.62, 0])
            self.play(*[restyle(p, outline=GREEN, fill=GREEN) for p in people[:2]],
                      restyle(people[2], op=0.4), *appear(h_out, *outs, shift=None, lag=0.15), run_time=1.5)

            c.wait_until("nocols")
            cross = Cross(VGroup(*credits), stroke_color=RED, stroke_width=6)
            self.play(*set_alpha(credits + [h_cred], 0.4), Create(cross), run_time=1.0)

            c.wait_until("nodup")
            tag = T("1 row, not 3", 30, FG).next_to(outs[0], RIGHT, buff=0.25)
            self.play(*[VShowPassingFlash(ln.copy().set_stroke(YELLOW, 5), time_width=0.6) for ln in links[:3]],
                      FlashAround(outs[0], run_time=1.5, time_width=1.5),
                      *appear(tag), run_time=1.5)  # early: says 'never repeats a row'

            c.wait_until("plan")
            pb = plan_box("HASH_JOIN", "Join Type: SEMI", size=40).move_to(DOWN * 1.3)
            ex_lab = Mono("EXPLAIN", 28, DIM).next_to(pb, UP, buff=0.25)
            sweep_clear(self, *appear(ex_lab, pb, lag=0.2), keep=[alg, lab])
            semi = select(pb.details[0], "SEMI")[0]
            c.wait_until("join type semi")
            self.play(*recolor(list(semi), YELLOW), FlashUnder(semi, run_time=1.2), run_time=1.2)

    # ------------------------------------------------------------ c3.semi.4
    def clip4(self):
        with self.say("c3.semi.4") as c:
            dc = distinct_code(32).move_to(UP * 0.7)
            sweep_clear(self, *appear(dc))

            c.wait_until("same")
            n = T("1,086 rows", 44, GOLD).move_to(DOWN * 2.1)
            self.play(*appear(n), run_time=1.0)

            c.wait_until("why")
            pp = dc.find("p.person_id", line=0)
            box = token_box(pp, dc.line(0))
            qm = T("?", 60, YELLOW).next_to(box, UP, buff=0.15)
            self.play(FadeIn(box), *appear(qm), run_time=1.2)

            c.wait_until("ex14")
            tag = T("Exercise 14", 32, DIM).next_to(qm, RIGHT, buff=0.35)
            self.play(FlashUnder(dc.find("p.name", line=0), run_time=1.5, time_width=1.5), *appear(tag), run_time=1.5)  # early: the brief tags the question it answers

            c.wait_until("intent")
            ec = exists_code(32, colored=True).move_to(UP * 0.2)
            sweep_clear(self, *appear(ec))
            c.wait_until("at least one credit")
            self.play(FlashAround(ec, run_time=2.0, time_width=1.5), run_time=2.0)
