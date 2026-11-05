"""Chapter 1, scene 5: a query where a table goes (derived tables). Clips c1.derived.1 – c1.derived.4.

Shared pieces (later scenes: `from lib.paths import load_scene; m = load_scene("ch1_s5_derived")`):
- `derived_code(select="SELECT year, n_movies", name=True, size=30)` -> slide 61's query as Code,
  derived-table parentheses BLUE and `AS per_year` YELLOW (name=False drops ` AS per_year`).
  `inner_glyphs(code)` / `outer_glyphs(code)` -> lists of glyph groups of the inner / outer query.
- `having_code(size=30)` -> s3's HAVING query (Code, verbatim).
- `result_table(header, rows, size=36)` -> Mono table, `.header .rule .rows` (each row VGroup(key, value),
  values GOLD). `derived_result(size=36)` -> the `year | n_movies` / 2013 153 / 2014 146 / 2016 147 table.
- `plan_diagram(width=4.1)` -> three-box plan, bottom to top "scan movies", "group by year, count",
  "filter > 140", centred at ORIGIN (box pitch 1.0); `.boxes .labels .arrows` (lists, bottom up).
- `handover_shot()` -> VGroup(derived_code()) at ORIGIN: the last frame (s6 opens on it).
"""
# style: 2
# handover: next
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

S1 = load_scene("ch1_s1_hook")

COMMENT = "-- Which years have more than 140 movie releases?"


def derived_code(select="SELECT year, n_movies", name=True, size=30):
    tail = ") AS per_year" if name else ")"
    src = "\n".join([COMMENT, select, "FROM (SELECT year, COUNT(*) AS n_movies",
                     "       FROM movies GROUP BY year" + tail, "WHERE n_movies > 140;"])
    code = Code(src, size=size)
    code.find("(", line=2).set_color(BLUE)
    code.find(")", line=3, nth=0).set_color(BLUE)
    if name:
        code.find("AS per_year", line=3).set_color(YELLOW)
    return code


def inner_glyphs(code):
    return [*code.find("SELECT year, COUNT(*) AS n_movies", line=2),
            *code.find("FROM movies GROUP BY year", line=3)]


def outer_glyphs(code):
    out = [*code.line(1), *code.find("FROM", line=2), *code.line(4)]
    try:
        out += [*code.find("AS per_year", line=3)]
    except ValueError:
        pass
    return out


def having_code(size=30):
    return Code("SELECT year, COUNT(*) AS n_movies\nFROM   movies\nGROUP BY year\n"
                "HAVING COUNT(*) > 140\nORDER BY year;", size=size)


def vdots():
    return VGroup(*[Dot(radius=0.03, color=DIM) for _ in range(3)]).arrange(DOWN, buff=0.05)


def result_table(header, rows, size=36, pitch=None):
    pitch = pitch or 0.0155 * size
    h0, h1 = Mono(header[0], size, FG), Mono(header[1], size, FG)
    h1.next_to(h0, RIGHT, buff=0.6)
    right = h1.get_right()[0]
    out_rows = []
    for i, (k, v) in enumerate(rows):
        y = h0.get_y() - (i + 1) * pitch - 0.12
        a = vdots() if k == "⋮" else Mono(str(k), size, FG)
        a.move_to([0, y, 0]).align_to(h0, LEFT)
        b = vdots() if v == "⋮" else Mono(str(v), size, GOLD)
        b.move_to([0, y, 0])
        b.shift((right - b.get_right()[0]) * RIGHT)
        out_rows.append(VGroup(a, b))
    rule = Line(h0.get_corner(DL) + 0.1 * DOWN + 0.1 * LEFT,
                [right + 0.1, h0.get_bottom()[1] - 0.1, 0]).set_stroke(DIM, 2)
    g = VGroup(h0, h1, rule, *out_rows)
    g.header, g.rule, g.rows = VGroup(h0, h1), rule, out_rows
    return g


def derived_result(size=36):
    return result_table(("year", "n_movies"), [(2013, 153), (2014, 146), (2016, 147)], size=size)


PLAN_LABELS = ["scan movies", "group by year, count", "filter > 140"]


def plan_diagram(width=4.1, size=30):
    boxes, labels, arrows = [], [], []
    for i, txt in enumerate(PLAN_LABELS):
        box = RoundedRectangle(corner_radius=0.1, width=width, height=0.62).set_stroke(FG, 2.5)
        box.move_to([0, (i - 1) * 1.0, 0])
        lab = T(txt, size, FG).move_to(box)
        boxes.append(box)
        labels.append(lab)
    for i in range(2):
        a = Arrow(boxes[i].get_top(), boxes[i + 1].get_bottom(), buff=0.04, stroke_width=3,
                  max_tip_length_to_length_ratio=0.45, color=DIM)
        arrows.append(a)
    g = VGroup(*boxes, *labels, *arrows)
    g.boxes, g.labels, g.arrows = boxes, labels, arrows
    return g


def small_form(scale=0.8):
    """s1's form scaled down, keywords kept at Mono 28 and right-aligned to their slots."""
    f = S1.select_form().scale(scale)
    for r in f:
        r.kw.scale(28 / (30 * scale))
        r.kw.next_to(r.box, LEFT, buff=0.14)
    return f


def line_swap(scene, out_glyphs, in_glyphs):
    """Old glyphs rise out (0-45%), new ones rise in (55-100%); other glyphs untouched.
    Returns (anims, finish) where finish(old, new) puts the new Code on screen as one object."""
    outs = [g.animate.shift(0.2 * UP).set_opacity(0) for g in out_glyphs]
    copies, ins = [], []
    for g in in_glyphs:
        cp = g.copy().shift(0.2 * DOWN).set_opacity(0)
        copies.append(cp)
        ins.append(Transform(cp, g.copy()))
    scene.add(*copies)

    def finish(old, new):
        scene.remove(old, *copies)
        scene.add(new)
    return during(outs, 0, 0.45) + during(ins, 0.55, 1.0), finish


def carry_early(scene, src, dst, via=()):
    """s1's carry(), but the copy shrinks to dst's size in the first 40% of the path."""
    a0, a1 = src.get_center(), dst.get_center()
    pts = [a0] + [np.array(p, dtype=float) for p in via] + [a1]
    seg = [np.linalg.norm(q - p) for p, q in zip(pts, pts[1:])]
    cum = np.concatenate([[0], np.cumsum(seg)]) / sum(seg)
    k = min(1.0, dst.height / src.height, dst.width / src.width)

    def path(a):
        i = min(int(np.searchsorted(cum, a, side="right")) - 1, len(seg) - 1)
        f = (a - cum[i]) / max(cum[i + 1] - cum[i], 1e-9)
        return interpolate(pts[i], pts[i + 1], f)

    tmpl = src.copy()
    cp = src.copy().set_opacity(0.3)
    scene.add(cp)

    def upd(m, a):
        m.become(tmpl)
        m.scale(interpolate(1, k, min(1, a / 0.4))).move_to(path(a))
        m.set_opacity((0.3 + 0.7 * min(1, a / 0.3)) * (1 - max(0, (a - 0.8) / 0.2)))

    return [UpdateFromAlphaFunc(cp, upd, remover=True), *during([FadeIn(dst)], 0.8, 1.0)]


def handover_shot():
    return VGroup(derived_code().move_to(ORIGIN))


def ghost_table():
    data = [("⋮", "⋮"), (2011, 93), (2012, 80), (2013, 153), (2014, 146), (2015, 135),
            (2016, 147), (2017, 120), (2018, 127), ("⋮", "⋮")]
    t = result_table(("year", "n_movies"), data, size=28, pitch=0.335)
    frame = DashedVMobject(SurroundingRectangle(t, buff=0.22).set_stroke(BLUE, 2), num_dashes=60)
    g = VGroup(frame, t)
    g.frame, g.table = frame, t
    return g


class Derived(NarratedScene):
    def construct(self):
        # ---- c1.derived.1: a table comes out of a query; it goes in FROM; slide 61
        with self.say("c1.derived.1") as c:
            fa = small_form()
            fa.move_to([-3.9, -0.4, 0])
            fa_sel = S1.slot_content(fa, "SELECT", "year, count(*)")
            fa_gb = S1.slot_content(fa, "GROUP BY", "year")
            fa_from = S1.slot_content(fa, "FROM", "movies")
            card = S1.table_card("movies").move_to([-3.9, 2.65, 0])
            self.play(*appear(fa, fa_sel, fa_gb, card, shift=None, lag=0.2), run_time=1.6)  # early: the form is shown whole

            c.wait_until("returns")
            lane = fa.get_right()[0] + 1.0
            self.play(*carry_early(self, card.label, fa_from,
                                via=[(lane, card.label.get_y(), 0), (lane, fa_from.get_y(), 0)]), run_time=1.6)
            out = S1.table_icon(BLUE, scale=3).move_to([0, -0.4, 0])
            c.wait_until("table back")
            self.play(GrowFromPoint(out, fa.get_right()), run_time=1.2)

            c.wait_until("anywhere")
            fb = small_form().move_to([3.9, -0.4, 0])
            self.play(*appear(fb, shift=None), run_time=1.0)  # early: the empty form is shown whole
            slot = fb.slots["FROM"].box
            tgt = out.copy().scale_to_fit_height(0.36)
            tgt.move_to(slot).align_to(slot.get_left() + 0.2 * RIGHT, LEFT)
            self.play(out.animate.become(tgt), run_time=1.6)

            c.wait_until("from")
            code = derived_code().move_to(ORIGIN)
            sweep_clear(self, *appear(code, shift=None), run_time=1.4)
            parens = [code.find("(", line=2), code.find(")", line=3, nth=0)]
            c.wait_until("parentheses")
            self.play(*flash(parens, color=BLUE, time_width=1.5), run_time=1.4)
            c.wait_until("from clause")
            self.play(FlashUnder(code.find("FROM", line=2), color=BLUE, time_width=1.5), run_time=1.2)
            c.wait_until("name")
            name = code.find("AS per_year", line=3)
            self.play(FlashUnder(name, color=YELLOW, time_width=1.5), run_time=1.4)

            region = [*code.find("(", line=2), *code.find("SELECT year, COUNT(*) AS n_movies", line=2),
                      *code.find("FROM movies GROUP BY year) AS per_year", line=3)]
            dbox = SurroundingRectangle(VGroup(*[g.copy() for g in region]), buff=0.12,
                                        corner_radius=0.08).set_stroke(BLUE, 2.5)
            dlab = T("derived table", 34, BLUE)
            dlab.move_to([0, code.line(4).get_y(), 0]).align_to(dbox, RIGHT)
            c.wait_until(own_word=dlab)
            self.play(FadeIn(dbox), *appear(dlab), run_time=1.2)

        # ---- c1.derived.2: inner, outer, result; the plan; same algebra
        with self.say("c1.derived.2") as c:
            up = 2.2 * UP
            ghost = ghost_table()
            ghost.move_to([0, -1.6, 0]).align_to([-6.3, 0, 0], LEFT)
            self.play(*during([code.animate.shift(up), dbox.animate.shift(up), dlab.animate.shift(up)], 0, 0.6),
                      *during(appear(ghost, shift=None), 0.55, 1.0), run_time=2.0)  # early: the ghost table is a picture
            self.play(*set_alpha(outer_glyphs(code) + [*code.line(0)], DIMMED), run_time=1.0)

            c.wait_until("outer")
            self.play(*set_alpha(outer_glyphs(code), 1), *set_alpha(inner_glyphs(code), DIMMED),
                      run_time=1.2)
            gt = ghost.table
            rows = gt.rows
            keep = [rows[3], rows[4], rows[6]]
            drop = [r for r in rows if r not in keep]
            self.remove(ghost)
            self.add(ghost.frame, *gt.header, gt.rule, *rows)
            c.wait_until("keeps the rows")
            self.play(FlashUnder(code.line(4), color=YELLOW, time_width=1.5),
                      *disappear(*drop, lag=0.05), run_time=1.6)
            y0 = rows[0].get_y() - 0.06
            slots = [np.array([r.get_x(), y0 - 0.48 * i, 0]) for i, r in enumerate(keep)]
            body = VGroup(gt.header.copy(), gt.rule.copy(),
                          *[r.copy().move_to(p) for r, p in zip(keep, slots)])
            frame2 = SurroundingRectangle(body, buff=0.22).set_stroke(BLUE, 2.5)
            self.play(*[r.animate.move_to(p) for r, p in zip(keep, slots)],
                      *during([FadeOut(ghost.frame)], 0, 0.5), *during([FadeIn(frame2)], 0.5, 1.0),
                      run_time=1.2)
            res = VGroup(*gt.header, gt.rule, *keep, frame2)
            settle(self, res)

            c.wait_until("same")
            self.play(FlashAround(VGroup(*keep), color=GREEN, time_width=1.5),
                      frame2.animate.set_stroke(GREEN, 3), run_time=1.4)

            hav = having_code(30)
            hav.move_to([0, -1.85, 0]).align_to([-6.5, 0, 0], LEFT)
            PX = 4.7
            plan = plan_diagram(width=3.8, size=28).move_to([PX, -2.0, 0])
            a_d = Arrow([PX, code.line(3).get_bottom()[1] - 0.05, 0], plan.boxes[2].get_top(), buff=0.08,
                        stroke_width=3, color=DIM)
            a_h = Arrow([hav.get_right()[0] + 0.05, plan.boxes[1].get_y(), 0], plan.boxes[1].get_left(), buff=0.08,
                        stroke_width=3, color=DIM)
            c.wait_until("plan")
            self.play(*disappear(dbox, dlab), *set_alpha([*code.line(0)], 0.6),
                      *set_alpha(inner_glyphs(code), 1), run_time=1.0)
            self.play(*appear(*[VGroup(b, l) for b, l in zip(plan.boxes, plan.labels)], shift=0.2 * UP, lag=0.3),  # early: the plan is shown whole, then walked
                      *[GrowArrow(a) for a in plan.arrows], GrowArrow(a_d), run_time=1.8)
            c.wait_until("having version")
            self.play(*during(disappear(res), 0, 0.45), *during(appear(hav, shift=None), 0.45, 1.0),
                      *during([GrowArrow(a_h)], 0.7, 1.0), run_time=1.6)
            for k, cue in enumerate(("scan", "group them", "then filter")):
                c.wait_until(cue)
                extra = []
                if k == 2:
                    extra = [FlashUnder(code.line(4), color=YELLOW, time_width=1.5),
                             FlashUnder(hav.line(3), color=YELLOW, time_width=1.5)]
                self.play(FlashAround(plan.boxes[k], color=YELLOW, time_width=1.5), *extra, run_time=1.0)

            # algebra: plan -> s1's bricks (movies, gamma, sigma)
            card2 = S1.table_card("movies").scale(0.76).move_to(plan.boxes[0])
            g1 = S1.group_brick().scale(0.76).move_to(plan.boxes[1])
            g2 = S1.keep_brick().scale(0.76).move_to(plan.boxes[2])
            icons = [S1.table_icon(BLUE, 0.76).move_to([PX, y, 0]) for y in (-2.46, -1.5)]
            c.wait_until("algebra")
            self.remove(*[m for b, l in zip(plan.boxes, plan.labels) for m in (b, l)])
            self.add(*plan.boxes, *plan.labels)
            self.play(*during(disappear(*plan.labels, *plan.arrows), 0, 0.45),
                      *during([ReplacementTransform(plan.boxes[0], card2.box),
                               ReplacementTransform(plan.boxes[1], g1.box),
                               ReplacementTransform(plan.boxes[2], g2.box)], 0.2, 0.8),
                      *during(appear(card2[1], card2[2], card2.label, g1.op, g2.op, *icons,
                                     shift=None, lag=0.1), 0.5, 1.0),
                      run_time=2.0)
            tw = VGroup(card2, icons[0], g1, icons[1], g2)
            settle(self, tw)

        # ---- c1.derived.3: the outer query is a fresh form; the third brick finds a home
        with self.say("c1.derived.3") as c:
            form = small_form()
            form.move_to([0, 0.4 - form.height / 2, 0]).align_to([-6.5, 0, 0], LEFT)
            self.play(*during(disappear(hav, a_d, a_h), 0, 0.45),
                      *during(appear(form, shift=None), 0.45, 1.0), run_time=1.6)  # early: the empty form is shown whole
            self.play(*set_alpha(inner_glyphs(code), DIMMED), run_time=1.0)

            b3 = S1.count_brick().scale(0.76).move_to([PX, 0.0, 0])
            b3.box.set_stroke(RED, 4)
            c.wait_until("empty again")
            self.play(*[time_span(FlashAround(r.box, color=BLUE, time_width=1.5), 0.1 * i, 0.1 * i + 0.9)
                        for i, r in enumerate(form)],
                      *during(appear(b3, shift=0.25 * DOWN), 0.4, 1.0), run_time=1.6)

            code1 = derived_code("SELECT COUNT(*) AS n_years").move_to(code)
            for g in inner_glyphs(code1):
                g.set_opacity(DIMMED)
            for g in code1.line(0):
                g.set_opacity(0.6)
            sel = form.slots["SELECT"].box
            b3t = b3.copy().scale_to_fit_height(sel.height - 0.04).move_to(sel)
            b3t.box.set_stroke(GREEN, 3)
            c.wait_until("swap")
            ls, fin = line_swap(self, [*code.line(1)], [*code1.line(1)])
            self.play(*ls, b3.animate.become(b3t), sel.animate.set_stroke(GREEN, 2.5), run_time=1.8)
            fin(code, code1)
            code = code1

            nhead = Mono("n_years", 40, FG)
            nrule = Line(nhead.get_corner(DL) + 0.12 * DOWN + 0.1 * LEFT,
                         nhead.get_corner(DR) + 0.12 * DOWN + 0.1 * RIGHT).set_stroke(DIM, 2)
            three = Mono("3", 48, GOLD).next_to(nrule, DOWN, buff=0.3)
            nres = VGroup(nhead, nrule, three).move_to([PX, -1.8, 0])
            c.wait_until("answer")
            self.play(*swap(tw, nres), run_time=1.4)

            c.wait_until("rule")
            name = code.find("AS per_year", line=3)
            self.play(FlashAround(name, color=YELLOW, time_width=1.5), run_time=1.4)
            lab = T("SQL standard: a name is required", 30, FG)
            lab.move_to([0, code.line(4).get_y(), 0]).align_to(code, RIGHT)
            c.wait_until(own_word=lab)
            self.play(*appear(lab), run_time=1.0)

            lab2 = T("DuckDB: the name is optional", 30, FG).next_to(lab, DOWN, buff=0.3).align_to(lab, RIGHT)
            code2 = derived_code("SELECT COUNT(*) AS n_years", name=False).move_to(code).align_to(code, LEFT)
            code2.align_to(code, UP)
            for g in inner_glyphs(code2):
                g.set_opacity(DIMMED)
            for g in code2.line(0):
                g.set_opacity(0.6)
            c.wait_until("duck")
            ls, fin = line_swap(self, [*code.find("AS per_year", line=3)], [])
            self.play(*appear(lab2), *ls, run_time=1.6)
            fin(code, code2)
            code = code2
            tick = check_mark(GREEN).next_to(three, RIGHT, buff=0.35)
            self.play(FlashAround(three, color=GREEN, time_width=1.5), *appear(tick, shift=None), run_time=1.2)

        # ---- c1.derived.4: read it inside out; nesting gets hard
        with self.say("c1.derived.4", gap=2.0) as c:
            final = handover_shot()[0]
            self.play(*during(disappear(form, b3, nres, tick, lab, lab2), 0, 0.4),
                      *during(edit(code, final), 0.42, 1.0), run_time=2.2)
            code = final

            seg_top = code.line(1)
            seg_in2 = VGroup(*code.find("(", line=2), *code.find("SELECT year, COUNT(*) AS n_movies", line=2))
            seg_in3 = code.find("FROM movies GROUP BY year)", line=3)
            eye = token_box(seg_top, seg_top)
            c.wait_until("read")
            self.play(FadeIn(eye), run_time=1.0)
            c.wait_until("jump")
            self.play(Transform(eye, token_box(seg_in2, code.line(2)), path_arc=-0.6), run_time=1.2)
            self.play(Transform(eye, token_box(seg_in3, code.line(3))), run_time=1.0)
            c.wait_until("back out")
            self.play(Transform(eye, token_box(seg_top, seg_top), path_arc=0.6), run_time=1.2)

            sketch = Mono("( ( ( … ) ) )", 44, DIM).move_to([0, -2.6, 0])
            c.wait_until("deeper")
            self.play(*appear(sketch), run_time=1.0)

        self.play(*disappear(sketch, eye), run_time=0.8)
        self.wait(1.0)
