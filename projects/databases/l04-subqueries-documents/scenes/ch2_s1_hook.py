"""Chapter 2, scene 1: hook, the NOT IN query that quietly returns nothing. Clips c2.hook.1 – c2.hook.3.

Exports (static, built where they sit on screen):
- open_card() -> VGroup(.grid .cell .column .labels .tags): ch2's first frame = ch1 s8's last.
  Icons centred at (-4.5, 0.6), (0, 0.6), (4.5, 0.6); labels T 36 FG at y -1.25; tags Mono 32 at y -1.95.
- shape_icon(kind) -> the "table" / "value" / "column" icon, full size, at ORIGIN.
- corner_icons() -> VGroup(table_pair, value_pair) with .grid .cell .labels, top-left corner.
- four_slots(small=False) -> VGroup(.slots (4 x VGroup(rect, q)), .marks, .count): 2 x 2 slots of
  3.2 x 1.0 (a 3.0 x 0.8 movie card fits) with a GOLD "4" at the end. Full size centred at (0, -0.6);
  small=True: scaled 0.5 at (4.4, -1.45), as in c2.hook.3.
- trap_shot() -> VGroup(.query .outline .result .silent .chip): the end of {plan}.
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
from lib.titles import title_card  # noqa: E402

QUERY = """SELECT title FROM movies
WHERE year NOT IN (SELECT deathyear FROM people);"""

ICON_X = (-4.5, 0.0, 4.5)
ICON_Y = 0.6
LABEL_Y = -1.25
TAG_Y = -1.95
SMALL_W, SMALL_H = 0.55, 0.40


# ---------- icons ----------
def _small_cell(header=False):
    r = Rectangle(width=SMALL_W, height=SMALL_H).set_stroke(BLUE, 3)
    r.set_fill(BLUE, 0.35 if header else 0)
    return r


def _grid_icon():
    rows = []
    for i in range(4):
        rows.append(VGroup(*[_small_cell(header=(i == 0)) for _ in range(3)]).arrange(RIGHT, buff=0))
    return VGroup(*rows).arrange(DOWN, buff=0)


def _cell_icon():
    box = Rectangle(width=1.5, height=0.8).set_stroke(BLUE, 3).set_fill(BLUE, 0.12)
    val = T("7.17", 36, GOLD).move_to(box)
    g = VGroup(box, val)
    g.box, g.value = box, val
    return g


def _column_icon():
    return VGroup(*[_small_cell(header=(i == 0)) for i in range(6)]).arrange(DOWN, buff=0)


def shape_icon(kind):
    """'table' (3 x 4 grid), 'value' (one cell with GOLD 7.17), 'column' (6 cells), at ORIGIN."""
    return {"table": _grid_icon, "value": _cell_icon, "column": _column_icon}[kind]()


def open_card():
    grid = shape_icon("table").move_to([ICON_X[0], ICON_Y, 0])
    cell = shape_icon("value").move_to([ICON_X[1], ICON_Y, 0])
    column = shape_icon("column").move_to([ICON_X[2], ICON_Y, 0])
    labels = VGroup(*[T(s, 36).move_to([x, LABEL_Y, 0])
                      for s, x in zip(("a table", "a value", "a column"), ICON_X)])
    tags = VGroup(Mono("FROM", 32, DIM).move_to([ICON_X[0], TAG_Y, 0]),
                  Mono(">", 32, DIM).move_to([ICON_X[1], TAG_Y, 0]),
                  Mono("IN", 32, BLUE).move_to([ICON_X[2], TAG_Y, 0]))
    card = VGroup(grid, cell, column, labels, tags)
    card.grid, card.cell, card.column, card.labels, card.tags = grid, cell, column, labels, tags
    return card


def corner_icons():
    grid = shape_icon("table").scale(0.5).move_to([-6.0, 3.2, 0])
    cell = shape_icon("value")
    cell.box.scale(0.6)
    cell.value.become(T("7.17", 28, GOLD))
    cell.move_to([-4.5, 3.2, 0])
    l1 = T("a table", 28).move_to([-6.0, 2.48, 0])
    l2 = T("a value", 28).move_to([-4.5, 2.48, 0])
    pair = VGroup(VGroup(grid, l1), VGroup(cell, l2))
    pair.grid, pair.cell, pair.labels = grid, cell, VGroup(l1, l2)
    return pair


# ---------- slots ----------
def four_slots(small=False):
    slots = []
    for _ in range(4):
        rect = RoundedRectangle(corner_radius=0.15, width=3.2, height=1.0).set_stroke(DIM, 2.5)
        q = T("?", 56, GOLD).move_to(rect)
        s = VGroup(rect, q)
        s.rect, s.q = rect, q
        slots.append(s)
    grid = VGroup(*slots).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3))
    count = T("4", 72, GOLD).next_to(grid, RIGHT, buff=0.5)
    g = VGroup(grid, count)
    g.move_to([0, -0.6, 0])
    g.slots, g.marks, g.count = grid, VGroup(*[s.q for s in slots]), count
    if small:
        g.scale(0.5).move_to([4.4, -1.45, 0])
    return g


# ---------- the trap ----------
def _query():
    return Code(QUERY, size=30).move_to([0, 1.45, 0])


def _result():
    box = Rectangle(width=2.6, height=1.5).set_stroke(DIM, 2)
    div = Line(box.get_left(), box.get_right()).set_stroke(DIM, 2)
    head = Mono("title", 32, DIM).move_to(box.get_center() + 0.375 * UP)
    rows = Mono("0 rows", 32, RED).move_to(box.get_center() + 0.375 * DOWN)
    g = VGroup(box, div, head, rows).move_to([-4.4, -1.45, 0])
    g.box, g.div, g.head, g.rows = box, div, head, rows
    return g


def _silent():
    return T("no error · no warning", 32, DIM).move_to([-0.4, -1.45, 0])


def _outline(query):
    return SurroundingRectangle(query, color=RED, buff=0.2).set_stroke(RED, 2)


def _chip(query):
    word = query.find("deathyear")
    lab = Mono("NULL", 28, PINK)
    box = RoundedRectangle(corner_radius=0.1, width=lab.width + 0.3, height=lab.height + 0.24)
    box.set_stroke(PINK, 2).set_fill(PINK, 0.12)
    chip = VGroup(box, lab)
    lab.move_to(box)
    chip.move_to([word.get_x(), 0.3, 0])
    return chip


def trap_shot():
    q = _query()
    g = VGroup(q, _outline(q), _result(), _silent(), _chip(q))
    g.query, g.outline, g.result, g.silent, g.chip = g
    return g


# ---------- the callbacks of clip 1 ----------
def _table_callback():
    outer = Code("SELECT * FROM", size=32)
    inner = Code("(SELECT … FROM movies)", size=30)
    box = RoundedRectangle(corner_radius=0.12, width=inner.width + 0.4, height=inner.height + 0.4)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.1)
    inner.move_to(box)
    sub = VGroup(box, inner)
    slot = DashedVMobject(Rectangle(width=box.width, height=box.height), num_dashes=40).set_stroke(DIM, 2)
    slot.next_to(outer, RIGHT, buff=0.3)
    row = VGroup(outer, slot).move_to([0, 1.5, 0])
    sub.move_to(slot).shift(1.4 * UP)
    label = T("a table", 36).next_to(slot, DOWN, buff=0.35)
    return outer, slot, sub, label


class Hook(NarratedScene):
    def construct(self):
        card = open_card()
        self.add(card)
        self.wait(0.7)
        corner = corner_icons()

        # ---- clip 1: title, then the two callbacks ----
        with self.say("c2.hook.1") as c:
            tc = title_card("Part 2 · NOT IN and the NULL trap")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("table")

            outer, slot, sub, lab_t = _table_callback()
            sweep_clear(self, time_span(FadeIn(outer), 0.5, 1.0), time_span(FadeIn(slot), 0.5, 1.0),
                        time_span(FadeIn(sub), 0.6, 1.0), run_time=1.0)
            self.play(sub.animate.move_to(slot), run_time=1.0)
            self.play(*appear(lab_t), run_time=0.6)
            row_a = VGroup(outer, slot, sub, lab_t)
            c.wait_until("value")

            s7 = load_scene("ch1_s7_scalar")
            where = Code("WHERE rating >", size=32)
            subq = s7.subquery_code(30)
            subq.next_to(where, RIGHT, buff=0.3)
            VGroup(where, subq).move_to([0, -1.2, 0])
            self.play(*appear(where, subq, lag=0.2), run_time=0.9)
            c.wait_until("where a value")
            val = _cell_icon().next_to(where, RIGHT, buff=0.3)
            lab_v = T("a value", 36).next_to(val, DOWN, buff=0.35)
            self.play(*swap(subq, val), run_time=1.0)
            self.play(*appear(lab_v), run_time=0.6)
            row_b = VGroup(where, val, lab_v)
            c.wait_until()

        # ---- clip 2: callbacks shrink to the corner; the question; four slots ----
        with self.say("c2.hook.2") as c:
            pair_t, pair_v = corner
            shrink = [row_a.animate.scale(0.2).move_to(pair_t).set_opacity(0),
                      row_b.animate.scale(0.2).move_to(pair_v).set_opacity(0)]
            self.play(*during(shrink, 0, 0.6), *during([FadeIn(pair_t), FadeIn(pair_v)], 0.55, 1),
                      run_time=1.5)
            self.remove(*row_a.get_family(), *row_b.get_family())
            question = T("Which movies came out in a year in which\nnone of the people in the database died?",
                         34, YELLOW, line_spacing=0.9).move_to([1.0, 3.15, 0])
            c.wait_until("Which movies")
            self.play(*appear(question), run_time=1.2)
            c.wait_until("four")
            slots = four_slots()
            self.play(*appear(*slots.slots, lag=0.25), run_time=1.5)
            self.play(*appear(slots.count), run_time=0.8)
            c.wait_until()

        # ---- clip 3: the natural query, zero rows, silence ----
        with self.say("c2.hook.3") as c:
            trap = trap_shot()
            query = trap.query
            small = four_slots(small=True)
            self.play(*during([slots.animate.scale(0.5).move_to(small),
                               *set_alpha([question], 0.5)], 0, 0.7),
                      *during(appear(query), 0.4, 1), run_time=1.6)
            c.wait_until("Year not in")
            self.play(FlashUnder(query.find("year NOT IN (SELECT deathyear FROM people)"),
                                 run_time=2, time_width=1.5))
            c.wait_until("zero")
            res = trap.result
            self.play(*appear(VGroup(res.box, res.div, res.head), res.rows, lag=0.5), run_time=1.2)
            c.wait_until("silent")
            self.play(*appear(trap.silent), run_time=1.0)
            c.wait_until("Just an empty")
            self.play(FlashAround(res, color=RED, run_time=2, time_width=1.5))
            c.wait_until("worse")
            self.play(FadeIn(trap.outline), run_time=1.0)
            c.wait_until("plan")
            self.play(*appear(trap.chip), run_time=1.0)
            c.wait_until()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
