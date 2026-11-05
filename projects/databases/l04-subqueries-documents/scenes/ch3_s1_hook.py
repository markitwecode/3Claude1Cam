"""Chapter 3, scene 1: hook, NOT IN found zero; the question is "at least one row?". Clips c3.hook.1 – c3.hook.2.

Exports (static, built where they sit on screen):
- open_card(lit=True, exists=True) -> VGroup(.kid .arrow .card .lit .question .exists): ch3's first
  frame = ch2 s7's last. The Kid's YELLOW row card left, a YELLOW arrow into a small BLUE plays_role
  card right (16 row strips, .lit = its 12 Kid strips, YELLOW), GOLD "at least one?" above the arrow,
  BLUE Mono EXISTS below it. lit=False / exists=False: the same picture unlit / without EXISTS.
- trap_back() -> VGroup(.result .cards): the RED "0 rows" result and the four GREEN movie cards
  (3.0 x 0.8) as they sit in this scene's {last} shot.
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

# ---------- the "at least one?" picture ----------
ROW_X = -4.6
KID_Y, FLOW_Y = 1.0, -1.0
CARD_X, CARD_TOP, CARD_W = 4.0, 2.3, 2.8
HDR = 0.5
N_STRIPS, STRIP_PITCH, STRIP_H, STRIP_W = 16, 0.24, 0.15, 2.4
KID_STRIPS = range(2, 14)          # 12 contiguous rows (plays_role sorted by movie)
MID_X = -0.1
UNLIT = (BLUE, 0.3)
LIT = (YELLOW, 0.85)


def movie_row(title, year, color=YELLOW):
    box = RoundedRectangle(corner_radius=0.12, width=3.6, height=0.9).set_stroke(color, 3)
    box.set_fill(color, 0.12)
    t = T(title, 36)
    y = T(year, 36, GOLD)
    txt = VGroup(t, y).arrange(RIGHT, buff=0.4).move_to(box)
    g = VGroup(box, txt)
    g.box, g.title, g.year = box, t, y
    return g


def plays_role_card():
    h = HDR + 0.1 + N_STRIPS * STRIP_PITCH + 0.1
    box = Rectangle(width=CARD_W, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
    box.move_to([CARD_X, CARD_TOP - h / 2, 0])
    div = Line([CARD_X - CARD_W / 2, CARD_TOP - HDR, 0],
               [CARD_X + CARD_W / 2, CARD_TOP - HDR, 0]).set_stroke(BLUE, 2)
    title = Mono("plays_role", 28, weight=BOLD).move_to([CARD_X, CARD_TOP - HDR / 2, 0])
    strips = VGroup()
    top = CARD_TOP - HDR - 0.1
    for i in range(N_STRIPS):
        s = Rectangle(width=STRIP_W, height=STRIP_H).set_stroke(width=0).set_fill(*UNLIT)
        s.move_to([CARD_X, top - STRIP_PITCH * (i + 0.5), 0])
        strips.add(s)
    g = VGroup(box, div, title, strips)
    g.box, g.div, g.title, g.strips = box, div, title, strips
    return g


def row_arrow(y):
    return Arrow([ROW_X + 1.85, y, 0], [CARD_X - CARD_W / 2, y, 0], buff=0.08,
                 stroke_width=4, color=YELLOW)


def open_card(lit=True, exists=True):
    kid = movie_row("The Kid", "1921").move_to([ROW_X, KID_Y, 0])
    card = plays_role_card()
    arrow = row_arrow(KID_Y)
    lit_strips = VGroup(*[card.strips[i] for i in KID_STRIPS])
    if lit:
        lit_strips.set_fill(*LIT)
    question = T("at least one?", 36, GOLD).move_to([MID_X, KID_Y + 0.55, 0])
    ex = Mono("EXISTS", 40, BLUE).move_to([MID_X, 0, 0])
    g = VGroup(kid, arrow, card, question)
    if exists:
        g.add(ex)
    g.kid, g.arrow, g.card, g.lit, g.question, g.exists = kid, arrow, card, lit_strips, question, ex
    return g


# ---------- the trap, carried over from ch2 ----------
MOVIES = (("The Kid", "1921"), ("Sherlock Jr.", "1924"), ("The General", "1926"),
          ("It Happened One Night", "1934"))
GRID_C = (0.6, -0.6)
RESULT_C = (-5.2, -0.6)
SLOT_SCALE = 1.15          # 28-pt titles need a 3.45 x 0.92 card


def _ch2():
    return load_scene("ch2_s1_hook")


def green_card(title, year):
    box = RoundedRectangle(corner_radius=0.12, width=3.0 * SLOT_SCALE, height=0.8 * SLOT_SCALE)
    box.set_stroke(GREEN, 3)
    box.set_fill(GREEN, 0.12)
    if T(title, 28).width + 0.3 + T(year, 28).width > box.width - 0.2:
        a, b = title.rsplit(" ", 2)[0], " ".join(title.split(" ")[-2:])
        l1 = T(a, 28)
        l2 = VGroup(T(b, 28), T(year, 28, GOLD)).arrange(RIGHT, buff=0.25)
        txt = VGroup(l1, l2).arrange(DOWN, buff=0.06)
    else:
        txt = VGroup(T(title, 28), T(year, 28, GOLD)).arrange(RIGHT, buff=0.25)
    txt.move_to(box)
    return VGroup(box, txt)


def _slots():
    s = _ch2().four_slots().scale(SLOT_SCALE)
    s.shift(np.array([*GRID_C, 0]) - s.slots.get_center())
    return s


def trap_back():
    slots = _slots()
    result = _ch2().trap_shot().result.move_to([*RESULT_C, 0])
    cards = VGroup(*[green_card(t, y).move_to(sl.rect) for (t, y), sl in zip(MOVIES, slots.slots)])
    g = VGroup(result, cards)
    g.result, g.cards = result, cards
    return g


def null_chip():
    lab = Mono("NULL", 28, PINK)
    box = RoundedRectangle(corner_radius=0.1, width=lab.width + 0.3, height=lab.height + 0.24)
    box.set_stroke(PINK, 2).set_fill(PINK, 0.12)
    lab.move_to(box)
    return VGroup(box, lab)


class Hook(NarratedScene):
    def construct(self):
        self.add(open_card())
        self.wait(0.7)

        # ---- clip 1: title, then the trap ----
        with self.say("c3.hook.1") as c:
            tc = title_card("Part 3 · EXISTS: semijoins and antijoins")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("last")

            query = _ch2().trap_shot().query.move_to([0, 2.4, 0])
            back = trap_back()
            slots = _slots()
            sweep_clear(self, time_span(FadeIn(query), 0.6, 1.4), run_time=1.4)
            self.play(*appear(back.result, *[sl.rect for sl in slots.slots], shift=None, lag=0.15), run_time=1.0)
            self.play(*[FadeIn(cd, shift=0.15 * DOWN) for cd in back.cards], run_time=1.0)  # early: the four movies, named on {four}
            c.wait_until("four")

            self.play(*flash(back.cards, color=GREEN), *appear(slots.count),
                      run_time=min(1.2, c.until("zero")))
            c.wait_until("zero")
            silent = _ch2().trap_shot().silent.move_to([-4.4, -2.65, 0])
            self.play(FlashAround(back.result.rows, color=RED, run_time=1.5, time_width=1.5),
                      *appear(silent), run_time=1.5)

        # ---- clip 2: the simpler question ----
        with self.say("c3.hook.2", gap=2.0) as c:
            self.play(*[FadeOut(m, scale=0.4) for m in self.mobjects], run_time=1.2)
            c.wait_until("ask")

            shot = open_card(lit=False, exists=False)
            self.play(*appear(shot.kid, shot.card, lag=0.3), run_time=1.2)
            self.play(GrowArrow(shot.arrow), *appear(shot.question), run_time=1.2)
            c.wait_until("kid")

            twelve = T("12", 56, GOLD).move_to([CARD_X + CARD_W / 2 + 0.6, KID_Y, 0])
            n = len(shot.lit)
            self.play(*[time_span(s.animate.set_fill(*LIT), 0.1 * i, 0.1 * i + 0.6)
                        for i, s in enumerate(shot.lit)],
                      time_span(FadeIn(twelve, shift=0.2 * DOWN), 0.1 * n, 0.1 * n + 0.6),
                      run_time=0.1 * n + 0.6)
            c.wait_until("flow")

            flow = movie_row("Flow", "2024").move_to([ROW_X, FLOW_Y, 0])
            farrow = row_arrow(FLOW_Y)
            zero = T("0", 56, GOLD).move_to([CARD_X + CARD_W / 2 + 0.6, FLOW_Y, 0])
            # The Kid's matches go back to unlit (and its row dims) before Flow's arrow lands,
            # so Flow's arrow visibly lights nothing.
            self.play(*during([s.animate.set_fill(*UNLIT) for s in shot.lit]
                              + [shot.kid.box.animate.set_stroke(opacity=0.5).set_fill(opacity=0.06),
                                 shot.kid.title.animate.set_opacity(0.5),
                                 shot.kid.year.animate.set_opacity(0.5)]
                              + set_alpha([shot.arrow, twelve], 0.5), 0, 0.45),
                      *during(appear(flow) + [GrowArrow(farrow)], 0.35, 1),
                      run_time=1.4)
            self.play(*appear(zero), run_time=0.8)
            c.wait_until("direct")

            ex = shot.exists
            self.play(FadeIn(ex, shift=0.4 * RIGHT), run_time=1.2)
            c.wait_until("fool")

            chip = null_chip().move_to([-3.0, -3.0, 0])
            self.play(FadeIn(chip, scale=0.6), run_time=0.5)
            self.play(chip.animate(rate_func=rush_into).move_to([-1.75, -0.4, 0]), run_time=0.6)
            self.play(FadeOut(chip, shift=np.array([-1.6, -2.6, 0]), rate_func=rush_from), run_time=0.9)
            c.wait_until("how")

            q = T("?", 64, YELLOW).next_to(ex, RIGHT, buff=0.35)
            self.play(*appear(q), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
