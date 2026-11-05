"""Chapter 6, scene 3: Exercise 20.2, the busiest composers. Clips c6.composers.1 – c6.composers.4.

Exports for the recap (ch6 s7), static:
- recap_tile() -> VGroup(.result, .jw1932, .jw1903): "Hans Zimmer  72" (72 GOLD), the row the stack
  of "Hans Zimmer" rows collapses to, with the two PINK "John Williams" circles beside it
  (born 1932 / born 1903 under them). About 9.6 x 2.4, centred on ORIGIN.
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

EX = load_scene("ch5_s7_exercises")
MATCH = load_scene("ch2_s3_match")

# ---------------------------------------------------------------- code
SRC = ["MATCH (p:Person) -[:COMPOSED_FOR]-> (m:Movie)",
       "RETURN p.name, count(*) AS movies",
       "ORDER BY movies DESC",
       "LIMIT 5;"]
SAFE = "RETURN p.person_id, p.name, count(*) AS movies"
CODE_SIZE = 30
CODE_L = -6.0
CODE_TOP = 3.1


def _full_code():
    full = Code("\n".join(SRC), size=CODE_SIZE)
    full.align_to([CODE_L, 0, 0], LEFT).align_to([0, CODE_TOP, 0], UP)
    return full


def code_line(i, src=None):
    """Line i of the query as its own Code, placed where it sits in the full 4-line block."""
    full = _full_code()
    ln = Code(src or SRC[i], size=CODE_SIZE)
    g0, f0 = ln.line(0)[0], full.line(i)[0]
    ln.shift(f0.get_center() - g0.get_center())
    return paint(ln)


def paint(code):
    for key, col in (("p.person_id", YELLOW), ("p.name", YELLOW), ("count(*)", GOLD)):
        try:
            code.find(key).set_color(col)
        except ValueError:
            pass
    return code


def brace_under(glyphs, line, color):
    b = span_brace(glyphs.get_left(), glyphs.get_right(), DOWN, color=color, buff=0.15)
    b.move_to([b.get_x(), line.get_bottom()[1] - 0.12 - b.height / 2, 0])
    return b


# ---------------------------------------------------------------- reply table
ROW_Y = [-0.25, -0.77, -1.29, -1.81, -2.33]
ROW6_Y = -3.17
CUT_Y = -2.73
HDR_Y = 0.5
NAME_L, SEP_X, COUNT_X = -4.3, 0.5, 1.3
REPLY = [("Hans Zimmer", "72"), ("James Newton Howard", "52"), ("Danny Elfman", "49"),
         ("John Williams", "48"), ("Marco Beltrami", "42")]
ROW6 = ("Michael Giacchino", "41")
IDS = ["nm0001877", "nm0006133", "nm0000384", "nm0002354", "nm0001937"]


def reply_row(name, count, y, name_l=NAME_L, count_x=COUNT_X):
    n = T(name, 34).move_to([0, y, 0]).align_to([name_l, 0, 0], LEFT)
    k = T(count, 34, GOLD).move_to([count_x, y, 0])
    k.align_to(n, DOWN)
    row = VGroup(n, k)
    row.name, row.count = n, k
    return row


def reply_head(cols, left, right, bottom_y):
    """cols: [(text, x, align)] ; DIM header, rule under it, column lines down to bottom_y."""
    hdr = VGroup()
    for text, x, how in cols:
        h = Mono(text, 28, DIM).move_to([x, HDR_Y, 0])
        if how == "left":
            h.align_to([x, 0, 0], LEFT)
        hdr.add(h)
    rule = Line([left, HDR_Y - 0.33, 0], [right, HDR_Y - 0.33, 0], color=DIM, stroke_width=2)
    return hdr, rule


# ---------------------------------------------------------------- people
def person(lines, center, r=0.8, size=28):
    circ = Circle(radius=r).set_stroke(PINK, 4).set_fill(
        interpolate_color(ManimColor(BG), ManimColor(PINK), 0.22), 1).move_to(center)
    lab = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.06).move_to(center)
    v = VGroup(circ, lab)
    v.circ, v.lab = circ, lab
    return v


def movie_dot(point, r=0.13):
    return Circle(radius=r).set_stroke(BLUE, 3).set_fill(BLUE, 0.35).move_to(point)


def edge(a, ra, b, rb, color=FG, width=3):
    return EX.edge_between(a, ra, b, rb, color=color, width=width)


# ---------------------------------------------------------------- recap
def recap_tile():
    res = reply_row("Hans Zimmer", "72", 0, name_l=0, count_x=3.4)
    res.move_to(ORIGIN)
    j1 = person(["John", "Williams"], ORIGIN, r=0.8)
    j1.born = T("born 1932", 28, DIM).next_to(j1, DOWN, buff=0.15)
    j2 = person(["John", "Williams"], ORIGIN, r=0.8)
    j2.born = T("born 1903", 28, DIM).next_to(j2, DOWN, buff=0.15)
    g1, g2 = VGroup(j1, j1.born), VGroup(j2, j2.born)
    people = VGroup(g1, g2).arrange(RIGHT, buff=0.7)
    tile = VGroup(res, people).arrange(RIGHT, buff=1.2).move_to(ORIGIN)
    res.set_y(j1.get_y())
    tile.result, tile.jw1932, tile.jw1903 = res, g1, g2
    return tile


class Composers(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ clip 1: the card
    def clip1(self):
        with self.say("c6.composers.1") as c:
            cards = EX.exercise_cards().scale(1.2).move_to(ORIGIN)
            self.play(*appear(*cards, lag=0, shift=None), run_time=0.4)
            card = cards[1]
            self.remove(card)
            self.add(card.box, card.num)
            panel = EX.exercise_panel("20.2")
            others = [cards[i] for i in (0, 2, 3, 4)]
            self.play(*during([ReplacementTransform(card.box, panel.frame)], 0, 0.7),
                      *during([FadeOut(card.num), *[FadeOut(o) for o in others]], 0, 0.45),
                      *during(appear(panel.title), 0.5, 1), run_time=1.3)
            c.wait_until(own_word=panel.question[0])
            self.play(*appear(panel.qgrp, shift=0.15 * DOWN), run_time=1.0)  # early: the card's question is shown whole
            c.wait_until("stop")
            bars = load_scene("ch6_s1_intro").pause_icon().next_to(panel.title, RIGHT, buff=0.45)
            self.play(FadeIn(bars), run_time=0.6)
        self.panel, self.pause = panel, bars

    # ------------------------------------------------------------ clip 2: edge, rows, group
    def clip2(self):
        panel = self.panel
        title = panel.title
        title.generate_target()
        title.target.scale(0.6).to_corner(UL, buff=0.5)
        self.tag = title

        # the one-edge pattern
        py, px = 2.15, 2.8
        sp = MATCH.stencil("Person", "p").at([-px, py, 0])
        sm = MATCH.stencil("Movie", "m").at([px, py, 0])
        for st, col in ((sp, PINK), (sm, BLUE)):
            st.ring.set_stroke(col, 5)
            st.name_tag.set_fill(col)
            st.label_tag.set_fill(col)
        arr = Arrow(sp.ring.get_right(), sm.ring.get_left(), buff=0.08, stroke_width=4, color=FG,
                    max_tip_length_to_length_ratio=0.08)
        elab = Mono("COMPOSED_FOR", 30).next_to(arr, UP, buff=0.12)
        pattern = [sp, sm, arr, elab]

        # Hans Zimmer's fan
        hz = person(["Hans", "Zimmer"], [-4.7, -1.3, 0], r=0.78)
        ys = [0.35 - 0.48 * i for i in range(8)]
        dots = [movie_dot([-1.6, y, 0]) for y in ys]
        hzc = hz.circ.get_center()
        edges = [edge(hzc, 0.78, d.get_center(), 0.15, width=2.5) for d in dots]
        rows = [T("Hans Zimmer", 32).move_to([0, y, 0]).align_to([-0.7, 0, 0], LEFT) for y in ys]
        rbr = Brace(VGroup(*rows), RIGHT, buff=0.25, color=DIM)
        rlab = T("72 rows", 32, GOLD).next_to(rbr, RIGHT, buff=0.18)

        with self.say("c6.composers.2") as c:
            self.play(*during(disappear(panel.frame, panel.qgrp, self.pause), 0, 0.45),
                      *during([MoveToTarget(title)], 0.2, 0.8),
                      *during(appear(sp, sm, lag=0.15, shift=None), 0.5, 0.85),
                      *during([GrowArrow(arr)], 0.65, 1), *during(appear(elab), 0.7, 1),
                      run_time=1.8)
            c.wait_until("rows")
            self.play(*appear(hz, shift=None), *appear(*dots, lag=0.04, shift=None), *[GrowFromPoint(e, hzc) for e in edges], run_time=1.4)  # early: the fan is the picture this sentence walks
            c.wait_until("is a row")
            self.play(VShowPassingFlash(edges[0].copy().set_stroke(YELLOW, 6), time_width=0.6),
                      *during(appear(rows[0], shift=0.3 * RIGHT), 0.4, 1), run_time=1.5)
            self.play(VShowPassingFlash(edges[1].copy().set_stroke(YELLOW, 6), time_width=0.6),
                      *during(appear(rows[1], shift=0.3 * RIGHT), 0.4, 1), run_time=0.9)
            self.play(*[VShowPassingFlash(e.copy().set_stroke(YELLOW, 6), time_width=0.6) for e in edges[2:]],
                      *during(appear(*rows[2:], lag=0.1, shift=0.3 * RIGHT), 0.3, 1), run_time=1.3)
            c.wait_until("every film")
            self.play(GrowFromCenter(rbr), *appear(rlab, shift=None),  # early: counts the rows just made (one per film)
                      run_time=min(1.0, max(0.4, c.until("group") - 0.1)))

            # {group}: the code, the rows slide under it
            c.wait_until("group")
            l1, l2 = code_line(0), code_line(1)
            dx = (NAME_L - rows[0].get_left()[0]) * RIGHT
            self.play(*during(disappear(*pattern, hz, *edges, *dots), 0, 0.45),
                      *during([m.animate.shift(dx) for m in rows + [rbr, rlab]], 0.2, 0.8),
                      *during(appear(l1, l2, lag=0.3, shift=None), 0.5, 1),
                      run_time=min(1.8, c.until("as in part three")))
            key = l2.find("p.name")
            kb = brace_under(key, l2, YELLOW)
            ktag = T("grouping key", 30, YELLOW).next_to(kb, DOWN, buff=0.1)
            c.wait_until("plain expressions")
            self.play(GrowFromCenter(kb), *appear(ktag), run_time=1.0)  # early: names the plain expression the sentence is about

            # the collapse (ch3 s5's implicit grouping)
            c.wait_until("grouped by name")
            rt = c.until("sort")
            yc = (ys[0] + ys[-1]) / 2
            res = reply_row("Hans Zimmer", "72", ROW_Y[0])
            self.play(*[r.animate.set_y(yc - (i - 3.5) * 0.36) for i, r in enumerate(rows)],
                      *disappear(rbr, rlab), *recolor(rows, YELLOW), run_time=min(1.0, 0.45 * rt))
            self.play(*during(disappear(*rows), 0, 0.45), *during(appear(res, shift=None), 0.5, 1),
                      run_time=min(1.0, 0.45 * rt))

            # {sort}
            c.wait_until("sort")
            l3, l4 = code_line(2), code_line(3)
            self.play(*during(disappear(kb, ktag), 0, 0.4),
                      *during(appear(l3, l4, lag=0.3, shift=None), 0.4, 1), run_time=1.2)  # early: the clause is read as it lands
            self.play(FlashAround(l3, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("keep five")
            self.play(FlashAround(l4, time_width=1.5), run_time=min(1.2, c.until(floor=0.5)))
        self.code = [l1, l2, l3, l4]
        self.res = res

    # ------------------------------------------------------------ clip 3: the reply
    def clip3(self):
        res = self.res
        bottom = ROW_Y[-1] - 0.32
        hdr, rule = reply_head([("p.name", NAME_L, "left"), ("movies", COUNT_X, "c")],
                               NAME_L - 0.15, COUNT_X + 0.65, bottom)
        sep = Line([SEP_X, HDR_Y + 0.25, 0], [SEP_X, bottom, 0], color=DIM, stroke_width=2)
        rows = [res] + [reply_row(n, k, y) for (n, k), y in zip(REPLY[1:], ROW_Y[1:])]
        r6 = reply_row(*ROW6, ROW6_Y).set_opacity(0.45)
        cut = DashedLine([NAME_L - 0.25, CUT_Y, 0], [COUNT_X + 0.75, CUT_Y, 0], color=RED,
                         stroke_width=3, dash_length=0.12)
        lim6 = Mono("LIMIT 6", 28, DIM).next_to(r6.name, LEFT, buff=0.35)
        gt = T("42 > 41", 36, GOLD).next_to(cut, RIGHT, buff=0.4)

        with self.say("c6.composers.3") as c:
            self.play(*appear(hdr, rule, sep, lag=0.15, shift=None), run_time=0.9)
            self.play(FlashAround(res, color=GOLD, time_width=1.5), run_time=1.2)
            for r in rows[1:]:
                c.wait_until(own_word=r.name)
                self.play(*appear(r, shift=None), run_time=0.8)
            c.wait_until("sixth")
            self.play(Create(cut), *appear(lim6, shift=None), run_time=1.2)
            c.wait_until(own_word=r6.name)
            self.play(*appear(r6, shift=None), run_time=0.8)
            c.wait_until("no tie")
            self.play(*appear(gt, shift=None), *flash([rows[4].count, r6.count], color=GOLD),
                      run_time=1.2)

            # {once}
            note_a = T("one COMPOSED_FOR\nedge per composer", 30, line_spacing=0.9)
            note_b = T("per film", 30)
            dist = Code("count(DISTINCT m)", size=28)
            tick = check_mark(GREEN).scale(0.7)
            same = T("same six rows", 28, GREEN)
            sline = VGroup(tick, same).arrange(RIGHT, buff=0.2)
            note = VGroup(note_a, note_b, dist, sline).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            note_b.shift(0.0 * DOWN)
            dist.shift(0.2 * DOWN)
            sline.shift(0.2 * DOWN)
            note.move_to([0, -0.55, 0]).align_to([6.55, 0, 0], RIGHT)
            c.wait_until("once")
            self.play(*flash([self.code[1].find("count(*)")], color=GOLD), run_time=1.2)
            c.wait_until("because")
            self.play(*appear(note_a, note_b, lag=0.4), run_time=min(1.2, c.until(floor=0.6)))  # early: the note states the reason this sentence gives
            rem = c.until(floor=0.3)
            if rem > 1.4:
                self.play(*appear(dist, sline, lag=0.4, shift=None), run_time=min(1.2, rem - 0.2))
            self.board3 = [hdr, rule, sep, *rows, r6, cut, lim6, gt, note_a, note_b]
            self.late_note = [dist, sline] if rem > 1.4 else []

    # ------------------------------------------------------------ clip 4: the namesake trap
    def clip4(self):
        l2 = self.code[1]
        y = -0.55
        jw1 = person(["John", "Williams"], [-3.5, y, 0])
        jw2 = person(["John", "Williams"], [3.5, y, 0])
        b1 = T("born 1932", 30, DIM).next_to(jw1, LEFT, buff=0.3)
        b2 = T("born 1903", 30, DIM).next_to(jw2, RIGHT, buff=0.3)
        dy = -2.2
        c1 = jw1.circ.get_center()
        cdots = [movie_dot([x, dy, 0]) for x in (-5.5, -4.8, -4.1, -3.4, -2.7)]
        cedges = [edge(c1, 0.8, d.get_center(), 0.15, width=2.5) for d in cdots]
        adot1 = movie_dot([-1.5, dy, 0])
        aedge1 = edge(c1, 0.8, adot1.get_center(), 0.15, color=DIM, width=2.5)
        clab = Mono("48 COMPOSED_FOR", 28).move_to([-4.1, -2.75, 0])
        alab1 = Mono("1 ACTED_IN", 28, DIM).move_to([-1.5, -3.25, 0])
        c2 = jw2.circ.get_center()
        adots2 = [movie_dot([x, dy, 0]) for x in (2.8, 4.2)]
        aedges2 = [edge(c2, 0.8, d.get_center(), 0.15, color=DIM, width=2.5) for d in adots2]
        alab2 = Mono("2 ACTED_IN", 28, DIM).move_to([3.5, -2.75, 0])
        tick = check_mark(GREEN).scale(1.1).move_to([0, y + 0.15, 0])
        luck = T("luck", 30, YELLOW).next_to(tick, DOWN, buff=0.25)

        with self.say("c6.composers.4") as c:
            self.play(FlashAround(l2.find("p.name"), color=RED, time_width=1.5), run_time=1.5)
            c.wait_until(own_word=jw1.lab[0], cue="two")
            sweep_clear(self, *appear(jw1, jw2, lag=0.3, shift=None), keep=[self.tag, *self.code],
                        run_time=1.4)
            c.wait_until("thirty-two")
            self.play(*appear(b1, shift=None), *[GrowFromPoint(e, c1) for e in cedges + [aedge1]],
                      *appear(*cdots, adot1, lag=0.04, shift=None), run_time=1.2)
            self.play(*appear(clab, alab1, lag=0.4), run_time=1.0)
            c.wait_until("oh three")
            self.play(*appear(b2, shift=None), *[GrowFromPoint(e, c2) for e in aedges2],
                      *appear(*adots2, lag=0.1, shift=None), *appear(alab2), run_time=1.2)

            # {luck}
            c.wait_until("luck")
            self.play(*[VShowPassingFlash(e.copy().set_stroke(YELLOW, 6), time_width=0.6) for e in cedges],
                      *recolor([clab], YELLOW), run_time=1.3)
            c.wait_until("nothing merges")
            self.play(Create(tick), run_time=0.8)
            c.wait_until(own_word=luck, cue="that's luck")
            self.play(*appear(luck), run_time=0.8)

            # {safe}
            c.wait_until("safe")
            l2b = code_line(1, SAFE)
            self.play(*edit(l2, l2b), run_time=1.6)
            self.code[1] = l2b

            id_l, sep1, name_l, sep2, cnt_x = -3.9, -1.1, -0.8, 4.1, 4.9
            bottom = ROW_Y[-1] - 0.32
            hdr, rule = reply_head([("p.person_id", id_l, "left"), ("p.name", name_l, "left"),
                                    ("movies", cnt_x, "c")], id_l - 0.15, cnt_x + 0.65, bottom)
            seps = [Line([x, HDR_Y + 0.25, 0], [x, bottom, 0], color=DIM, stroke_width=2)
                    for x in (sep1, sep2)]
            rows = []
            for (n, k), pid, yy in zip(REPLY, IDS, ROW_Y):
                r = reply_row(n, k, yy, name_l=name_l, count_x=cnt_x)
                i = Mono(pid, 28, YELLOW).move_to([0, yy, 0]).align_to([id_l, 0, 0], LEFT)
                rows.append(VGroup(i, r.name, r.count))
                rows[-1].count = r.count
            c.wait_until("one person")
            sweep_clear(self, *appear(hdr, rule, *seps, *rows, lag=0.12, shift=None),  # early: the table shown whole, then compared
                        keep=[self.tag, *self.code], run_time=min(2.0, c.until("same five rows")))
            c.wait_until("same five rows")
            self.play(*flash([r.count for r in rows], color=GOLD), run_time=min(1.4, c.until(floor=0.6)))
