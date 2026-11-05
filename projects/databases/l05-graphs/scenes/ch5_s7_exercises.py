"""Chapter 5, scene 7: Your turn, five exercises with one hint each. Clips c5.ex.1 – c5.ex.5."""
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
from lib.style import *  # noqa: E402,F403

EXERCISE_KEYS = ["20.1", "20.2", "20.3", "21", "22"]


def exercise_cards():
    """The five exercise cards in a row, centred on ORIGIN (9.9 x 1.1).

    Returns a VGroup of 5 cards; each card is VGroup(box, num) with attributes
    .box (DIM RoundedRectangle 1.7 x 1.1, stroke 3), .num (DIM T size 48, e.g. "20.1") and .key (the string).
    """
    cards = VGroup()
    for key in EXERCISE_KEYS:
        box = RoundedRectangle(corner_radius=0.15, width=1.7, height=1.1).set_stroke(DIM, 3)
        num = T(key, size=48, color=DIM).move_to(box)
        card = VGroup(box, num)
        card.box, card.num, card.key = box, num, key
        cards.add(card)
    cards.arrange(RIGHT, buff=0.35)
    return cards


PANEL_C = np.array([0.0, 0.5, 0.0])
ROW_SCALE = 0.6
ROW_POS = np.array([-3.0, -3.33, 0.0])


# The question on each card, as on-screen lines, and its text size.
QUESTIONS = {
    "20.1": ["Which movies did Charles Chaplin", "both direct and act in?"],
    "20.2": ["Who are the five people who composed", "the music for the most movies?"],
    "20.3": ["On which movies did both Lana Wachowski", "and Lilly Wachowski work, in any position?"],
    "21": ["Write a SQL query that returns the same result as",
           "the Cypher co-star query (Slide 106).",
           "Compare the two queries."],
    "22": ["Genres as a list property, or as Genre vertices with",
           "HAS_GENRE edges? For each design, count the movies that",
           "are both Romance and Comedy. Advantages and disadvantages?"],
}
QUESTION_SIZE = {"20.1": 36, "20.2": 36, "20.3": 36, "21": 34, "22": 30}


def question_block(lines, size=32):
    q = VGroup(*[T(s, size=size) for s in lines]).arrange(DOWN, buff=0.16)
    qmark = T("?", size=64, color=GOLD)
    qmark.next_to(q, RIGHT, buff=0.5)
    grp = VGroup(q, qmark)
    grp.move_to([0, 0, 0]).align_to([0, 2.62, 0], UP)
    return grp, q, qmark


def exercise_panel(key):
    """The hero card for exercise `key` ("20.1" ... "22"), no hint, at its place in this scene.

    Returns VGroup(frame, title, qgrp), 13.2 x 6.1, centred at (0, 0.5) (y 3.55 .. -2.55), with attributes
    .frame (RoundedRectangle corner 0.3, DIM stroke 2), .title (T "Exercise 20.1", 44, YELLOW, at y 3.1),
    .qgrp = VGroup(question, qmark) with top at y 2.62, .question (VGroup of T lines, size QUESTION_SIZE[key]),
    .qmark (GOLD T "?" 64, right of the question), .key.
    """
    frame = RoundedRectangle(corner_radius=0.3, width=13.2, height=6.1).set_stroke(DIM, 2).move_to(PANEL_C)
    title = T(f"Exercise {key}", size=44, color=YELLOW).move_to([0, 3.1, 0])
    qgrp, q, qmark = question_block(QUESTIONS[key], QUESTION_SIZE[key])
    panel = VGroup(frame, title, qgrp)
    panel.frame, panel.title, panel.qgrp, panel.question, panel.qmark, panel.key = frame, title, qgrp, q, qmark, key
    return panel


def edge_between(a, ra, b, rb, angle=0.0, color=FG, width=3, tip=True):
    a, b = np.array(a), np.array(b)
    u = (b - a) / np.linalg.norm(b - a)
    s, e = a + u * ra, b - u * rb
    if abs(angle) < 1e-6:
        line = Line(s, e)
    else:
        line = ArcBetweenPoints(s, e, angle=angle)
    line.set_stroke(color, width)
    if tip:
        line.add_tip(tip_length=0.18, tip_width=0.16)
        line.tip.set_fill(color, 1).set_stroke(color, 0)
    return line


def node(center, r, color, label_lines, size=28):
    circ = Circle(radius=r).set_stroke(color, 4).set_fill(BG, 1).move_to(center)
    lab = VGroup(*[T(s, size=size) for s in label_lines]).arrange(DOWN, buff=0.06).move_to(center)
    return VGroup(circ, lab)


class Exercises(NarratedScene):
    def construct(self):
        self.cards = exercise_cards()
        self.ex1()
        self.ex2()
        self.ex3()
        self.ex4()
        self.ex5()
        self.wait(1.5)
        self.close_card(4)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------- shared card moves ----------
    def open_card(self, i, rt=1.0):
        card = self.cards[i]
        self.hero = exercise_panel(card.key)
        self.panel = self.hero.frame
        self.title = self.hero.title
        self.items = [self.title]
        self.play(*during([ReplacementTransform(card.box.copy(), self.panel),
                           card.box.animate.set_stroke(YELLOW),
                           card.num.animate.set_color(YELLOW)], 0, 0.6),
                  *during(appear(self.title), 0.5, 1), run_time=rt)

    def close_card(self, i, rt=1.0):
        card = self.cards[i]
        tick = check_mark(DIM).scale(0.4).next_to(card.box, UP, buff=0.08)
        target = card.box.copy().set_stroke(DIM, 2)
        self.play(*during(disappear(*self.items), 0, 0.45),
                  *during([Transform(self.panel, target)], 0.3, 1),
                  *during([card.box.animate.set_stroke(DIM), card.num.animate.set_color(DIM)], 0.5, 1),
                  *during(appear(tick, shift=None), 0.6, 1), run_time=rt)
        self.remove(self.panel)

    def show_question(self, c, early=False):
        grp, q = self.hero.qgrp, self.hero.question
        if not early:
            c.wait_until(own_word=q[0])
        self.play(*appear(grp, shift=0.15 * DOWN), run_time=1.0)  # early: the card's question is shown whole
        self.items.append(grp)
        return grp

    def pause_label(self, c):
        lbl = T("pause and try it", size=30, color=DIM).move_to([4.75, 3.1, 0])
        if c.remaining - 2.1 > 0.05:
            self.wait(c.remaining - 2.1)
        self.play(*appear(lbl, shift=None), run_time=0.6)  # early: marks the scripted 2 s pause
        self.items.append(lbl)

    # ---------- intro + 20.1 ----------
    def ex1(self):
        with self.say("c5.ex.1") as c:
            header = T("Your turn", size=56).move_to([0, 2.3, 0])
            self.play(*appear(header), run_time=min(1.0, c.until("five")))
            c.wait_until("five")
            self.cards.move_to([0, 0.1, 0])
            self.play(*appear(*self.cards, lag=0.25), run_time=1.5)
            note = T("solutions: bonus chapter", size=32, color=DIM).move_to([0, -1.4, 0])
            c.wait_until(own_word=note)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("e201")
            row_target = self.cards.copy().scale(ROW_SCALE).move_to(ROW_POS)
            note_target = note.copy().scale(28 / 32)
            note_target.move_to([6.4 - note_target.width / 2, ROW_POS[1], 0])
            self.play(*during(disappear(header), 0, 0.45),
                      *during([self.cards.animate.become(row_target), note.animate.become(note_target)], 0.2, 1),
                      run_time=1.1)
            self.open_card(0, rt=1.0)
            self.show_question(c)

            c.wait_until("hint1")
            pl = Mono("(p)", size=60, color=PINK).move_to([-3.0, -0.3, 0])
            pr = Mono("(p)", size=60, color=PINK).move_to([3.0, -0.3, 0])
            self.play(*appear(pl, pr, lag=0.3), run_time=1.0)
            c.wait_until("twice")
            circ = Circle(radius=0.85).set_stroke(PINK, 5).move_to([0, -0.3, 0])
            p = Mono("p", size=60, color=PINK).move_to(circ)
            self.play(*during([pl.animate.shift(1.9 * RIGHT).set_opacity(0),
                               pr.animate.shift(1.9 * LEFT).set_opacity(0)], 0, 0.5),
                      *during([GrowFromCenter(circ), FadeIn(p)], 0.5, 1), run_time=1.6)
            self.remove(pl, pr)
            tag = T("same name = same vertex", size=36).next_to(circ, DOWN, buff=0.4)
            c.wait_until("what does that force")
            self.play(*appear(tag), run_time=1.0)
            self.items += [circ, p, tag]
            self.pause_label(c)

    # ---------- 20.2 ----------
    def ex2(self):
        with self.say("c5.ex.2") as c:
            self.close_card(0)
            self.open_card(1)
            self.show_question(c)

            c.wait_until("hint2")
            types = VGroup(*[Mono(s, size=28) for s in
                             ["ACTED_IN", "DIRECTED", "PRODUCED", "WROTE", "COMPOSED_FOR"]])
            types.arrange(RIGHT, buff=0.5).move_to([0, 0.75, 0])
            self.play(*appear(*types, lag=0.15, shift=None), run_time=0.8)

            def wbox(w):
                return (Rectangle(width=w.width + 0.26, height=0.52).set_stroke(YELLOW, 2)
                        .set_fill(YELLOW, 0.2).move_to(w).set_z_index(-1))
            box = wbox(types[0])
            which = T("which one?", size=30, color=YELLOW).move_to([0, 0.15, 0])
            self.play(FadeIn(box), *appear(which), run_time=0.6)
            self.play(Succession(*[Transform(box, wbox(w), run_time=0.4) for w in types[1:]]),
                      run_time=1.6)

            code = Code("RETURN p1.name AS name1, p2.name AS name2,\n       count(*) AS movies", size=30)
            code.move_to([0, -1.85, 0])
            keys = code.find("p1.name AS name1, p2.name AS name2")
            brace = Brace(keys, direction=UP, buff=0.1, color=GREEN)
            blab = T("grouping keys", size=30, color=GREEN).next_to(brace, UP, buff=0.12)
            c.wait_until(own_word=blab, cue="implicit grouping")
            self.play(FadeOut(box), *appear(code, shift=None), GrowFromCenter(brace), *appear(blab),
                      run_time=min(1.2, c.until(floor=0.6)))
            self.items += [types, which, code, brace, blab]
            self.pause_label(c)

    # ---------- 20.3 ----------
    def ex3(self):
        with self.say("c5.ex.3") as c:
            self.close_card(1)
            self.open_card(2)
            self.show_question(c)

            c.wait_until("hint3")
            arrow = Mono("-->", size=72).move_to([-3.6, -0.4, 0])
            atag = T("any type", size=32, color=YELLOW).next_to(arrow, DOWN, buff=0.4)
            self.play(*appear(arrow, shift=None), run_time=0.9)
            c.wait_until(own_word=atag)
            self.play(*appear(atag), run_time=0.9)

            c.wait_until("repeats")
            lana = node([0.9, 0.55, 0], 0.65, PINK, ["Lana"], size=30)
            lilly = node([0.9, -1.75, 0], 0.65, PINK, ["Lilly"], size=30)
            movie = node([4.6, -0.6, 0], 0.7, BLUE, ["movie"], size=30)
            edges = VGroup(
                *[edge_between(lana[0].get_center(), 0.65, movie[0].get_center(), 0.7, a, width=2.5)
                  for a in (-0.4, 0.0, 0.4)],
                *[edge_between(lilly[0].get_center(), 0.65, movie[0].get_center(), 0.7, a, width=2.5)
                  for a in (-0.3, 0.3)])
            self.play(*appear(lana, lilly, movie, lag=0.2, shift=None), run_time=1.0)
            self.play(*[GrowFromPoint(e, e.get_start()) for e in edges], run_time=1.2)
            rows = T("rows?", size=36, color=GOLD).next_to(movie, DOWN, buff=0.3)
            c.wait_until("do some movies appear")
            self.play(*appear(rows), run_time=1.0)
            self.items += [arrow, atag, lana, lilly, movie, edges, rows]
            self.pause_label(c)

    # ---------- 21 ----------
    def ex4(self):
        with self.say("c5.ex.4") as c:
            self.close_card(2)
            self.open_card(3)
            self.show_question(c)

            c.wait_until("hint4")
            edge_txt = Mono("-[:ACTED_IN]->", size=36, color=YELLOW).move_to([-3.3, -0.15, 0])
            # ch2 s6's colour-matched pair: PINK tail dot, BLUE head dot, YELLOW arrow <-> YELLOW name line
            tail = Dot([edge_txt[0].get_left()[0] - 0.16, edge_txt.get_y(), 0], radius=0.09, color=PINK)
            head = Dot([edge_txt[-1].get_right()[0] + 0.16, edge_txt.get_y(), 0], radius=0.09, color=BLUE)
            edge = VGroup(tail, edge_txt, head)
            card = RoundedRectangle(corner_radius=0.12, width=3.2, height=1.8) \
                .set_stroke(BLUE, 3).set_fill(BLUE, 0.06).move_to([3.4, -0.15, 0])
            hdr = Line(card.get_corner(UL) + 0.6 * DOWN, card.get_corner(UR) + 0.6 * DOWN).set_stroke(YELLOW, 2)
            rws = VGroup(*[Line(card.get_left() + 0.3 * RIGHT, card.get_right() + 0.3 * LEFT)
                           .set_stroke(DIM, 2).shift((-0.35 - 0.4 * k) * UP) for k in range(2)])
            hid = T("?", size=44, color=GOLD).move_to(card.get_top() + 0.3 * DOWN)
            table = VGroup(card, hdr, rws, hid)
            both = DoubleArrow(edge.get_right() + 0.25 * RIGHT, card.get_left() + 0.35 * LEFT,
                               buff=0, stroke_width=3, tip_length=0.2).set_color(DIM)
            self.play(*appear(edge, shift=None), run_time=0.9)
            self.play(GrowFromCenter(both), *appear(table, shift=None), run_time=1.2)

            c.wait_until("lt")
            lt = Mono("WHERE p1.person_id < p2.person_id", size=32, color=YELLOW)
            sql = T("in SQL?", size=32)
            row = VGroup(lt, sql).arrange(RIGHT, buff=0.5).move_to([0, -1.85, 0])
            self.play(*appear(lt, shift=None), run_time=1.0)
            c.wait_until("the job")
            self.play(*appear(sql), run_time=0.9)
            self.items += [edge, table, both, lt, sql]
            self.pause_label(c)

    # ---------- 22 ----------
    def ex5(self):
        with self.say("c5.ex.5") as c:
            self.close_card(3)
            self.open_card(4)
            self.show_question(c, early=True)

            # design A: the list property
            ma = node([-3.8, -0.15, 0], 0.62, BLUE, ["Annie", "Hall"])
            key = Mono("genres:", size=28, color=DIM)
            lst = Mono("['Comedy', 'Romance']", size=28)
            for g in select(lst, "["):
                g.set_color(TEAL)
            for g in select(lst, "]"):
                g.set_color(TEAL)
            for s in ("'Comedy'", "'Romance'"):
                for g in select(lst, s):
                    g.set_color(GOLD)
            prop = VGroup(key, lst).arrange(DOWN, buff=0.14).next_to(ma, DOWN, buff=0.3)
            c.wait_until("list of strings")
            self.play(*appear(ma, prop, lag=0.4, shift=None), run_time=1.4)

            # design B: Genre vertices
            c.wait_until("vertex")
            mb = node([0.9, -0.5, 0], 0.62, BLUE, ["Annie", "Hall"])
            com = node([5.2, 0.25, 0], 0.8, PURPLE, ["Comedy"])
            rom = node([5.2, -1.6, 0], 0.8, PURPLE, ["Romance"])
            e1 = edge_between(mb[0].get_center(), 0.62, com[0].get_center(), 0.8)
            e2 = edge_between(mb[0].get_center(), 0.62, rom[0].get_center(), 0.8)
            labs = VGroup()
            for e, side in ((e1, 1), (e2, -1)):
                v = e.get_end() - e.get_start()
                ang = np.arctan2(v[1], v[0])
                lab = Mono("HAS_GENRE", size=28, color=DIM).rotate(ang)
                nrm = np.array([-np.sin(ang), np.cos(ang), 0]) * side
                lab.move_to((e.get_start() + e.get_end()) / 2 + 0.28 * nrm)
                labs.add(lab)
            self.play(*appear(mb, shift=None), run_time=0.8)
            self.play(GrowFromPoint(e1, e1.get_start()), GrowFromPoint(e2, e2.get_start()),  # early: the genre vertices are part of design B, named later
                      *appear(com, rom, lag=0.2, shift=None), run_time=1.4)
            c.wait_until(own_word=labs[0], cue="has-genre")
            self.play(*appear(*labs, lag=0.2, shift=None), run_time=0.9)

            c.wait_until("hint5")
            qa = T("?", size=48, color=GOLD).move_to([-3.8, 0.78, 0])
            qb = T("?", size=48, color=GOLD).move_to([0.9, 0.62, 0])
            self.play(*appear(qa, qb, lag=0.3), run_time=1.0)
            norm = T("normalisation (Lecture 4)", size=30, color=DIM).move_to([0, -2.2, 0])
            c.wait_until(own_word=norm)
            self.play(*appear(norm), run_time=1.0)
            self.items += [ma, prop, mb, com, rom, e1, e2, labs, qa, qb, norm]
            self.pause_label(c)
