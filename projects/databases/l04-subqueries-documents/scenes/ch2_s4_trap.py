"""Chapter 2, scene 4: the trap in full (The Kid should be in the answer; the NULL-filled column). Clips c2.trap.1 – c2.trap.3.

Exports:
- kid_card() -> s2's movie_card("The Kid", 1921) lit YELLOW (GOLD year), scale 1.2, at ORIGIN.
- people_strip() -> VGroup(.header .rows .names .cells .dots): the deathyear column of people,
  rows named (Chaplin 1977, Coogan 1984, Purviance 1958, Zimmer NULL, Hanks NULL, …),
  built where it sits in this scene (right side, x ≈ 2..6.5, y ≈ 2.4..-2.3).
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

_s1 = load_scene("ch2_s1_hook")
_s2 = load_scene("ch2_s2_absent")
_s5 = load_scene("ch2_s5_logic")

NOACTORS = """SELECT movie_id, title FROM movies
WHERE movie_id NOT IN (SELECT movie_id FROM plays_role);"""

PEOPLE = [("Charles Chaplin", 1977), ("Jackie Coogan", 1984), ("Edna Purviance", 1958),
          ("Hans Zimmer", None), ("Tom Hanks", None)]

CELL_X, CELL_W, CELL_H = 2.75, 1.6, 0.62
ROW_Y0, ROW_PITCH = 1.45, 0.72
NAME_X = 3.8
TOKEN_X = 1.2
QUERY_SCALE = 0.9
QUERY_TOP = np.array([0, 3.2, 0])
SLOTS_SCALE = 0.875
SLOTS_AT = np.array([-2.9, -2.4, 0])
BAR_W, BAR_H, BAR_C = 11.5, 1.0, np.array([0, 0.3, 0])


def kid_card():
    card = _s2.movie_card("The Kid", 1921, color=YELLOW).scale(1.2)
    return card


def year_cell(year, center):
    if year is None:
        g = _s5.null_cell(width=CELL_W, height=CELL_H, size=30)
    else:
        box = Rectangle(width=CELL_W, height=CELL_H).set_stroke(BLUE, 3).set_fill(BG, 0)
        label = Mono(str(year), 30, GOLD).move_to(box)
        g = VGroup(box, label)
        g.box, g.label = box, label
    g.move_to(center)
    return g


def people_strip():
    header = Mono("deathyear", 30, DIM).move_to([CELL_X, ROW_Y0 + 0.75, 0])
    cells, names, rows = [], [], []
    for i, (name, year) in enumerate(PEOPLE):
        y = ROW_Y0 - i * ROW_PITCH
        c = year_cell(year, [CELL_X, y, 0])
        n = T(name, 28, FG)
        n.move_to([NAME_X, y, 0], aligned_edge=LEFT)
        cells.append(c)
        names.append(n)
        rows.append(VGroup(c, n))
    dots = T("…", 36, DIM).move_to([CELL_X, ROW_Y0 - len(PEOPLE) * ROW_PITCH + 0.1, 0])
    g = VGroup(header, *rows, dots)
    g.header, g.rows, g.dots = header, rows, dots
    g.cells, g.names = cells, names
    return g


class Trap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- clip 1
    def clip1(self):
        trap = _s1.trap_shot()
        self.trap = trap
        q = trap.query
        with self.say("c2.trap.1") as c:
            self.play(FadeIn(trap), run_time=1.0)
            c.wait_until("same")
            na = Code(NOACTORS, size=28)
            na.set_opacity(0.45)
            na.move_to([0, 3.2, 0]).to_edge(LEFT, buff=0.5)
            dx = na.find("NOT IN").get_left()[0] - q.find("NOT IN").get_left()[0]
            self.na = na
            self.play(FadeIn(na, shift=0.4 * DOWN),
                      *[m.animate.shift(dx * RIGHT) for m in (q, trap.outline, trap.chip)],
                      run_time=1.5)
            self.play(FlashUnder(q.find("NOT IN (SELECT"), color=YELLOW, run_time=1.5, time_width=1.5),
                      FlashUnder(na.find("NOT IN (SELECT"), color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until("zero")
            self.play(FlashAround(trap.result.rows, color=RED, run_time=2, time_width=1.5))

    # ---------------------------------------------------------------- clip 2
    def clip2(self):
        trap = self.trap
        q = trap.query
        with self.say("c2.trap.2") as c:
            slots = _s1.four_slots().scale(SLOTS_SCALE).move_to(SLOTS_AT)
            self.slots = slots
            self.play(*during(disappear(self.na, trap.silent, trap.chip, trap.outline, trap.result), 0, 0.45),
                      *during([q.animate.scale(QUERY_SCALE).move_to(QUERY_TOP)], 0.45, 1),
                      run_time=1.6)
            self.play(*appear(*slots.slots, slots.count, lag=0.15, shift=None), run_time=1.0)
            c.wait_until("The Kid came out")
            kid = kid_card().move_to([-2.4, 0.9, 0])
            self.kid = kid
            self.play(*appear(kid), run_time=1.0)
            c.wait_until("twenty-one")
            self.play(FlashAround(kid.year, color=YELLOW, run_time=1.5, time_width=1.5))

            c.wait_until("scan")
            strip = people_strip()
            self.strip = strip
            self.play(*appear(strip.header, *strip.rows, strip.dots, lag=0.12, shift=None), run_time=1.2)
            token = Mono("1921", 30, YELLOW).move_to([TOKEN_X, ROW_Y0, 0])
            frame = Rectangle(width=CELL_W + 0.14, height=CELL_H + 0.14).set_stroke(YELLOW, 4)
            frame.move_to(strip.cells[0])
            self.play(*fly(kid.year, token, arc=-PI / 4), FadeIn(frame), run_time=1.5)
            for i in range(1, len(PEOPLE) + 1):
                y = ROW_Y0 - i * ROW_PITCH
                rt = 0.6 if i == 1 else 0.4
                if i == len(PEOPLE):
                    y += 0.1
                self.play(token.animate.set_y(y), frame.animate.set_y(y), run_time=rt)
            c.wait_until("none")
            died = T("died in 1921: 0", 32, GOLD).move_to([CELL_X + 1.3, -3.05, 0])
            self.died = died
            c.wait_until(own_word=died)
            self.play(*appear(died), run_time=1.0)

            c.wait_until("should")
            slot = slots.slots[0]
            kid.generate_target()
            kid.target.scale(SLOTS_SCALE / 1.2).move_to(slot.rect)
            kid.target.box.set_stroke(GREEN, 3)
            kid.target.title.set_color(DIM)
            self.play(*during(disappear(slot.q, token, frame), 0, 0.4), *during([MoveToTarget(kid)], 0.3, 1),
                      run_time=1.8)
            slot.remove(slot.q)
            here = T("should be here", 30, GREEN).next_to(slot.rect, UP, buff=0.2)
            self.here = here
            self.play(*appear(here), run_time=1.0)

    # ---------------------------------------------------------------- clip 3
    def clip3(self):
        q = self.trap.query
        strip = self.strip
        with self.say("c2.trap.3") as c:
            bar = _s5.death_bar(BAR_W, height=BAR_H, center=BAR_C)
            outline = Rectangle(width=BAR_W, height=BAR_H).set_stroke(GOLD, 3).move_to(BAR_C)
            total = T("23,179 people", 32, GOLD).next_to(outline, UP, buff=0.25).align_to(outline, RIGHT)
            boxes = [cl.box for cl in strip.cells]
            texts = [cl.label for cl in strip.cells] + list(strip.names) + [strip.header, strip.dots]
            copies = VGroup(*[b.copy() for b in boxes])
            self.remove(*strip.get_family())
            self.add(*texts, copies)
            self.play(*during(disappear(*texts, self.died), 0, 0.45),
                      *during([ReplacementTransform(copies, outline)], 0.3, 1),
                      *during(set_alpha([self.kid, self.slots, self.here], 0.35), 0, 0.6),
                      run_time=1.8)
            self.play(*appear(total), run_time=1.0)

            c.wait_until("known")
            known_lab = T("2,685 known death years", 30, GOLD)
            known_lab.next_to(outline, DOWN, buff=0.3).align_to(outline, LEFT)
            self.play(*during(disappear(self.here), 0, 0.4), *during([FadeIn(bar.known)], 0, 1),
                      *during(appear(known_lab), 0.4, 1), run_time=1.4)

            c.wait_until("nulls")
            null_lab = VGroup(T("20,494", 40, PINK), Mono("NULL", 36, PINK)).arrange(RIGHT, buff=0.22)
            null_lab.move_to(bar.null).shift(0.6 * LEFT)
            self.play(FadeIn(bar.null), *appear(null_lab, shift=None), run_time=1.4)
            pct = T("88%", 48, PINK).move_to([bar.null.get_right()[0] - 1.1, BAR_C[1], 0])
            c.wait_until("That's eighty-eight")
            self.play(*appear(pct, shift=None), run_time=1.0)

            alive = T("alive", 30, DIM).move_to([0.2, known_lab.get_y(), 0])
            unknown = T("died, year unknown?", 30, DIM).move_to([3.6, known_lab.get_y(), 0])
            c.wait_until(own_word=alive)
            self.play(*appear(alive), run_time=1.0)
            c.wait_until(own_word=unknown)
            self.play(*appear(unknown), run_time=1.0)

            c.wait_until("ask")
            notin = q.find("NOT IN")
            box = token_box(notin, q.line(1))
            self.play(FadeIn(box), run_time=1.0)
            x = notin.get_x()
            top = box.get_bottom()[1] - 0.1
            bottom = bar.null.get_top()[1] + 0.08
            line = Line([x, top, 0], [x, bottom, 0]).set_stroke(YELLOW, 4)
            ques = T("?", 56, YELLOW).move_to([x + 0.5, (top + bottom) / 2, 0])
            self.play(Create(line), *appear(ques, shift=None), run_time=1.5)
