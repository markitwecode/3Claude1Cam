"""Chapter 6, scene 4: the exercises begin. Four cards; then 5.1 (selection sort's cost) and 5.2
(selection sort in OCaml), each grown out of its pill onto a hero card: the task, its example, a
GOLD "?" wherever an answer would go (never a solution), one hint beneath, a still "pause" beat.
Clips c6.ex.1 - c6.ex.4.

THE EXERCISE-CARD KIT (the first half of this file) is shared: ch6_s5_hints2, ch6_s6 (recap) and
the ch7 solution scenes import it read-only, e.g.

    from scenes.ch6_s4_hints1 import (four_cards, make_strip, HeroCard, Slot, Tag, pause_tag,
                                      enter_card, exit_card, card_5_1, TODO, CURRENT, DONE, ...)

Importing it has no side effects (definitions only; `__all__` lists the kit, so `import *` does
not pull in this scene's class). L4's kit (projects/focs/l04-more-lists/scenes/ch6_s5_hints1.py),
adapted to four cards and to style-2 transitions (cards grow without text morphs). API:

  EX_NUMS, EX_TITLES, EX_TASKS   the four cards: "5.1".."5.4", titles, task sentences (verbatim)
  EX51_* / EX52_*    5.1's and 5.2's card text and code, verbatim
  RUNNING            [3, 5, 9, 4, 7], the chapter's running list
  UNZIP_SRC          L4 ch3's unzip (In [65]), verbatim; UNZIP_LET its line 3
  L2_ROWS            Lecture 2's recurrence table (lhs, rhs) as ch2_s5 shows it; l2_table(size)
  four_cards()       the overview: four dim BigCards in one row (y 0.2) + DIM note
                     "Solutions: bonus chapter" ("bonus chapter" YELLOW) at y -2.1; header
                     "Exercises" (T 52) sits at y 3.0 here. VGroup with .cards and .note.
  BigCard(i)         one overview card (BIG_W x BIG_H): .frame .num (T 44) .name (T 28, DIM, 2 lines)
  make_strip(states) the four pills, top left at y STRIP_Y (z 2: cards pass under them);
                     states TODO / CURRENT / DONE; restyled(pill, state) animates one.
                     This scene ends with [DONE, CURRENT, TODO, TODO] (then fades it all).
  HeroCard(i, height, step=ROW_STEP, lifted=None)  the current exercise, CARD_W wide, top at
                     CARD_TOP: .frame, .header ("Exercise 5.k  ·  Title", T 38, number YELLOW),
                     .row_y(k) / .at_row(mob, k) (row 0 = header), .tag(text, color),
                     .lower(*items), .lift(drop=()) (anims: up to the top and, with `lifted`,
                     the frame shrinks to that height while `drop` fades), .keep(*mobs), .bottom
  card_5_1(), card_5_2()  the hero cards as stated, fully built and lowered (see each builder
                     for its attributes); card.whole() -> VGroup of what the card shows when stated
  Slot(type_src=None, ...)  dashed box with a GOLD "?"; with a type: "?  : <type>" (GREEN, 'a PINK)
  Tag(text, color)   a rounded label
  enter_card(strip, card, extra=(), light=True) / exit_card(strip, card, extra)
                     grow out of / shrink back into its pill (then scene.remove(card.frame))
  mini_chain(values), tiles(values), hint_label(card), pause_tag(), pause_icon(),
  fit(c, cue), first_cue(c, *cues), hold_for(scene, born, n), finish(scene), glyph(code, sub)
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import above, appear, disappear, during, marker, recolor, span_brace, swap, token_box  # noqa: E402,F401
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

__all__ = [
    "CARD_FILL", "CARD_W", "CARD_L", "CARD_R", "CARD_TOP", "PAD", "COL_X", "CONTENT_R", "ROW0",
    "ROW_STEP", "STRIP_Y", "PILL_W", "PILL_H", "CODE_DIM", "CARD_CENTER_Y", "BIG_W", "BIG_H",
    "EX_NUMS", "EX_TITLES", "EX_CARD_LINES", "EX_TASKS", "RUNNING",
    "EX51_LINES", "EX52_TASK", "EX52_NAME", "EX52_TYPE", "EX52_TESTS", "EX52_TAG",
    "UNZIP_SRC", "UNZIP_LET", "L2_ROWS",
    "TODO", "CURRENT", "DONE", "PILL_STYLE",
    "row_y", "at_row", "fit", "first_cue", "Pill", "make_strip", "restyled", "BigCard",
    "four_cards", "Slot", "Tag", "HeroCard", "card_5_1", "card_5_2", "mini_chain", "tiles",
    "l2_table", "hint_label", "pause_icon", "pause_tag", "enter_card", "exit_card", "hold_for",
    "finish", "glyph",
]

# ── the exercise-card kit (shared with ch6_s5, ch6_s6 and ch7) ─────────────────────
CARD_FILL = "#161A21"          # a card's face: a shade lighter than the background
CARD_W = 13.0                  # hero card width (frame is 14.2 wide)
CARD_L, CARD_R = -CARD_W / 2, CARD_W / 2
CARD_TOP = 2.72                # just under the strip of pills
PAD = 0.42
COL_X = CARD_L + PAD           # left edge of a card's content
CONTENT_R = CARD_R - PAD       # right edge of a card's content
ROW0 = CARD_TOP - 0.46         # centre of the header row
ROW_STEP = 0.75                # default row pitch inside a card
STRIP_Y = 3.2                  # the strip of pills (top left) and the pause tag (top right)
PILL_W, PILL_H = 1.0, 0.5
CODE_DIM = 0.6                 # opacity of "remember this" code in a hint
CARD_CENTER_Y = 0.0            # while it's being stated, a card waits centred in the frame
BIG_W, BIG_H = 3.1, 2.0        # an overview card (four in a row)

EX_NUMS = ("5.1", "5.2", "5.3", "5.4")
EX_TITLES = ("Selection sort's cost", "Selection sort in OCaml", "Bubble sort's cost",
             "Bubble sort in OCaml")
EX_CARD_LINES = (("Selection sort's", "cost"), ("Selection sort", "in OCaml"),
                 ("Bubble sort's", "cost"), ("Bubble sort", "in OCaml"))   # overview cards, 2 lines
EX_TASKS = (
    "Remove a smallest item to head the result; sort the rest recursively. "
    "State, with justification, the time complexity.",
    "Implement selection sort in OCaml.",
    None,                      # 5.3 / 5.4: their text lives in ch6_s5_hints2 (card_5_3, card_5_4)
    None,
)
RUNNING = [3, 5, 9, 4, 7]

# 5.1: EX_TASKS[0] as it is wrapped on the card
EX51_LINES = ("Remove a smallest item to head the result;",
              "sort the rest recursively.",
              "State, with justification, the time complexity.")
# 5.2 (results and type checked by the script-writer with a trial selsort, OCaml 5.4.1)
EX52_TASK = EX_TASKS[1]
EX52_NAME, EX52_TYPE = "selsort", "'a list -> 'a list"
EX52_TESTS = (("selsort [3; 5; 9; 4; 7]", "[3; 4; 5; 7; 9]"),
              ("selsort [3; 5; 3; 1; 5]", "[1; 3; 3; 5; 5]"))
EX52_TAG = "repeats"

# code the hints quote from earlier lectures (verbatim)
UNZIP_SRC = ("let rec unzip = function\n"                          # L4 ch3, In [65]
             "  | [] -> ([], [])\n"
             "  | (x, y)::pairs ->\n"
             "      let xs, ys = unzip pairs in\n"
             "      (x::xs, y::ys)")
UNZIP_LET = 3                                                      # the line a let pattern is on
L2_ROWS = ((r"T(n+1) = T(n) + 1", "O(n)"),                         # Lecture 2's table (ch2_s5)
           (r"T(n+1) = T(n) + n", "O(n^2)"),
           (r"T(n) = T(n/2) + 1", r"O(\log n)"),
           (r"T(n) = 2T(n/2) + n", r"O(n\log n)"))

TODO, CURRENT, DONE = "todo", "current", "done"
PILL_STYLE = {TODO: (DIM, 2.0, DIM), CURRENT: (YELLOW, 3.0, YELLOW), DONE: (BLUE, 2.5, FG)}


def row_y(k, step=ROW_STEP):
    return ROW0 - step * k


def at_row(mob, k, x=COL_X, step=ROW_STEP):
    """Left-align `mob` at x on card row k (row 0 is the header row), before lower()."""
    return mob.move_to([x, row_y(k, step), 0], aligned_edge=LEFT)


def fit(c, cue, frac=0.7, lo=0.6, hi=1.5):
    """A run_time that leaves a hold before `cue` (about 60-70% motion, the rest still)."""
    return min(hi, max(lo, frac * c.until(cue, floor=0.0)))


def first_cue(c, *cues):
    """The first of several cues that exists in the clip (for lines being re-voiced)."""
    for cue in cues:
        try:
            c.at(cue)
            return cue
        except KeyError:
            pass
    raise KeyError(f"{c.id}: none of {cues}")


class Pill(VGroup):
    """A small exercise card in the strip: just its number."""

    def __init__(self, i, state=TODO, **kw):
        super().__init__(**kw)
        self.i = i
        self.frame = RoundedRectangle(corner_radius=0.12, width=PILL_W, height=PILL_H)
        self.frame.set_fill(CARD_FILL, 1)
        self.num = T(EX_NUMS[i], size=28)
        self.add(self.frame, self.num)
        self.restyle(state)

    def restyle(self, state):
        stroke, width, text = PILL_STYLE[state]
        self.frame.set_stroke(stroke, width)
        self.num.set_color(text)
        self.state = state
        return self


def make_strip(states):
    """The four pills in a row, top left (4.48 wide, left edge at CARD_L, y STRIP_Y), z 2."""
    s = VGroup(*[Pill(i, st) for i, st in enumerate(states)]).arrange(RIGHT, buff=0.16)
    s.move_to([CARD_L, STRIP_Y, 0], aligned_edge=LEFT)
    s.set_z_index(2)
    return s


def restyled(pill, state):
    """Animate a pill (already on screen) to a new state."""
    target = pill.copy().restyle(state)
    pill.state = state
    return Transform(pill, target)


class BigCard(VGroup):
    """One of the four cards as the hero of the overview: number and title (two lines)."""

    def __init__(self, i, **kw):
        super().__init__(**kw)
        self.i = i
        self.frame = RoundedRectangle(corner_radius=0.2, width=BIG_W, height=BIG_H)
        self.frame.set_stroke(DIM, 2.5).set_fill(CARD_FILL, 1)
        self.num = T(EX_NUMS[i], size=44).move_to(self.frame.get_center() + UP * 0.48)
        self.name = VGroup(*[T(s, size=28, color=DIM) for s in EX_CARD_LINES[i]])
        self.name.arrange(DOWN, buff=0.14).move_to(self.frame.get_center() + DOWN * 0.38)
        self.add(self.frame, self.num, self.name)


def four_cards():
    """The overview: four dim cards in one row and the note. See the module docstring."""
    cards = VGroup(*[BigCard(i) for i in range(4)]).arrange(RIGHT, buff=0.2).move_to(UP * 0.2)
    note = T("Solutions: bonus chapter", size=34, color=DIM, t2c={"bonus chapter": YELLOW})
    note.move_to(DOWN * 2.1)
    row = VGroup(cards, note)
    row.cards, row.note = cards, note
    return row


class Slot(VGroup):
    """The dashed box where the student's code goes, with a GOLD "?". Without a type: a box of
    the given size with a big "?". With a type: one row, "?  : <type>", the type GREEN, 'a PINK."""

    def __init__(self, type_src=None, width=3.4, height=1.3, size=30, **kw):
        super().__init__(**kw)
        if type_src is None:
            self.q = T("?", size=72, color=GOLD)
            self.sig = None
            parts = [self.q]
            w, h = width, height
        else:
            self.q = T("?", size=40, color=GOLD)
            self.sig = Code(": " + type_src, size=size).set_color(GREEN)
            self.sig.find(":")[0].set_color(FG)
            k = 0
            while True:
                try:
                    self.sig.find("'a", nth=k).set_color(PINK)
                except ValueError:
                    break
                k += 1
            VGroup(self.q, self.sig).arrange(RIGHT, buff=0.32)
            parts = [self.q, self.sig]
            w, h = VGroup(*parts).width + 0.6, 0.6
        self.box = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=w, height=h),
                                  num_dashes=int(6 * (w + h))).set_stroke(DIM, 2.5)
        VGroup(*parts).move_to(self.box)
        self.add(self.box, *parts)


class Tag(VGroup):
    def __init__(self, text, color=BLUE, **kw):
        super().__init__(**kw)
        self.label = T(text, size=28, color=color)
        self.box = RoundedRectangle(corner_radius=0.22, width=self.label.width + 0.4, height=0.48)
        self.box.set_stroke(color, 2).set_fill(color, 0.12)
        self.box.move_to(self.label)
        self.add(self.box, self.label)


class HeroCard(VGroup):
    """The current exercise, big. Only its frame and header are in the group; the builder adds
    the rest as attributes (rows at card.row_y(k), slots, tags) and `parts`, what whole() shows.

    Laid out at the top of the frame; lower(...) drops the card and its items to the middle,
    where it waits while it's being stated, and lift() takes it back up for its hint (with
    `lifted`, the frame also shrinks to that height and the items in `drop` fade)."""

    def __init__(self, i, height, step=ROW_STEP, lifted=None, **kw):
        super().__init__(**kw)
        self.i, self.h, self.step = i, height, step
        self.h_lift = height if lifted is None else lifted
        self.drop_y = max(0.0, CARD_TOP - (CARD_CENTER_Y + height / 2))
        self.frame = RoundedRectangle(corner_radius=0.22, width=CARD_W, height=height)
        self.frame.set_stroke(YELLOW, 3).set_fill(CARD_FILL, 1)
        self.frame.move_to([0, CARD_TOP - height / 2, 0])
        num = f"Exercise {EX_NUMS[i]}"
        self.header = self.at_row(T(f"{num}  ·  {EX_TITLES[i]}", size=38,
                                    t2c={num: YELLOW, "·": DIM}), 0)
        self.add(self.frame, self.header)
        self.tags = []
        self.parts = [self.frame, self.header]   # what whole() shows (builders extend it)
        self.shown = [self.header]                # everything on the card that leaves with it

    def row_y(self, k):
        return row_y(k, self.step)

    def at_row(self, mob, k, x=COL_X):
        return at_row(mob, k, x, self.step)

    @property
    def bottom(self):
        """Where the card's bottom edge is once lifted (hints are laid out against this)."""
        return CARD_TOP - self.h_lift

    def lower(self, *items):
        """Call once everything for the card is built: drop it all to the waiting position."""
        for m in (self.frame, self.header, *self.tags, *items):
            m.shift(DOWN * self.drop_y)
        return self

    def lift(self, drop=()):
        """Animations taking the card and what's kept on it up to the top; the frame shrinks to
        the lifted height while `drop` (shown items that don't go up) fades first."""
        drop = list(drop)
        frame = RoundedRectangle(corner_radius=0.22, width=CARD_W, height=self.h_lift)
        frame.match_style(self.frame).move_to([0, CARD_TOP - self.h_lift / 2, 0])
        self.shown = [m for m in self.shown if m not in drop]
        return ([*during([FadeOut(m) for m in drop], 0, 0.45)]
                + during([Transform(self.frame, frame)], 0.15 if drop else 0, 1)
                + during([m.animate.shift(UP * self.drop_y) for m in self.shown], 0.15 if drop else 0, 1))

    def tag(self, text, color=BLUE):
        t = Tag(text, color)
        prev = self.tags[-1] if self.tags else self.header
        t.next_to(prev, RIGHT, buff=0.2 if self.tags else 0.45).set_y(self.row_y(0))
        self.tags.append(t)
        return t

    def keep(self, *mobs):
        self.shown.extend(mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def whole(self):
        """Everything the card shows when stated, as one group (for a scene that just adds it)."""
        return VGroup(*self.parts)


def mini_chain(values, side=0.5, gap=0.26, size=30, color=BLUE):
    """A compact chain of boxed values with small arrows (no []): 3.34 wide for five values."""
    boxes = VGroup(*[Square(side).set_stroke(color, 2.5).set_fill(BG, 1) for _ in values])
    boxes.arrange(RIGHT, buff=gap)
    vals = VGroup(*[T(str(v), size=size).move_to(b) for v, b in zip(values, boxes)])
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.03, stroke_width=2.5, color=FG,
                            max_tip_length_to_length_ratio=0.5, tip_length=0.12)
                      for a, b in zip(boxes[:-1], boxes[1:])])
    g = VGroup(boxes, arrows, vals)
    g.boxes, g.arrows, g.vals = boxes, arrows, vals
    return g


def tiles(values, side=0.85, gap=0.22, size=40):
    """A row of GOLD tiles with values (things being compared)."""
    sq = VGroup(*[Square(side).set_stroke(GOLD, 3).set_fill(GOLD, 0.15) for _ in values])
    sq.arrange(RIGHT, buff=gap)
    vals = VGroup(*[T(str(v), size=size).move_to(s) for v, s in zip(values, sq)])
    g = VGroup(sq, vals)
    g.sq, g.vals = sq, vals
    return g


def l2_table(size=40, pitch=0.68, color=DIM):
    """Lecture 2's recurrence table as ch2_s5 showed it: two left-aligned columns, no row lit.
    VGroup of rows, each VGroup(lhs, rhs); top-left at ORIGIN (move it as a whole)."""
    lhs = [MathTex(a, font_size=size, color=color) for a, _ in L2_ROWS]
    rhs = [MathTex(b, font_size=size, color=color) for _, b in L2_ROWS]
    x2 = max(m.width for m in lhs) + 0.6
    rows = VGroup()
    for k, (a, b) in enumerate(zip(lhs, rhs)):
        a.move_to([0, -pitch * k, 0], aligned_edge=LEFT)
        b.move_to([x2, -pitch * k, 0], aligned_edge=LEFT)
        rows.add(VGroup(a, b))
    return rows


def hint_label(card, chapter=None):
    text = "Hint" if chapter is None else f"Hint · from {chapter}"
    lab = T(text, size=32, color=DIM, t2c={"Hint": YELLOW})
    return lab.move_to([COL_X, card.bottom - 0.4, 0], aligned_edge=LEFT)


def pause_icon(color=YELLOW, h=0.34):
    bars = VGroup(*[RoundedRectangle(corner_radius=0.03, width=h * 0.3, height=h) for _ in range(2)])
    bars.arrange(RIGHT, buff=h * 0.27).set_stroke(width=0).set_fill(color, 1)
    return bars


def pause_tag():
    tag = VGroup(pause_icon(), T("pause and try it", size=30)).arrange(RIGHT, buff=0.22)
    return tag.move_to([CARD_R, STRIP_Y, 0], aligned_edge=RIGHT)


def enter_card(strip, card, extra=(), light=True):
    """The card's frame grows out of its pill (which lights up as the current one, unless
    light=False); the header, then `extra`, fade in once it has nearly landed. No text morphs."""
    p = strip[card.i]
    anims = [*during([TransformFromCopy(p.frame, card.frame)], 0, 0.6),
             *during(appear(card.header, *extra, lag=0.15), 0.5, 1)]
    return anims + ([restyled(p, CURRENT)] if light else [])


def exit_card(strip, card, extra=()):
    """Everything on the card (and `extra`, the hint) fades first; then the frame shrinks back
    under its pill, which is now marked done. Call scene.remove(card.frame) after the play."""
    p = strip[card.i]
    done = p.copy().restyle(DONE).frame.set_fill(CARD_FILL, 0)
    return ([*during([FadeOut(m) for m in (*card.shown, *extra)], 0, 0.45)]
            + during([Transform(card.frame, done)], 0.2, 1) + [restyled(p, DONE)])


def hold_for(scene, born, text_len):
    """Before a scene's final fade: let text born at `born` reach its reading time."""
    need = 4.0 + text_len / 12.0 + 0.2
    if scene.time < born + need:
        scene.wait(born + need - scene.time)


def finish(scene):
    scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=1.0)
    scene.wait(0.15)   # the last play() never renders its final (empty) frame


def glyph(code, sub, line=None, nth=0, idx=0):
    """One glyph: character `idx` of the nth occurrence of `sub`."""
    return code.find(sub, line=line, nth=nth)[idx]


# ── the cards of this scene ─────────────────────────────────────────────────────────
STEP51 = 0.62
H51 = 5.72                     # header, three task rows, the result row, the chain, its brace
L51 = 0.46 + 3 * STEP51 + 0.38  # lifted for the hint: header and task only
CHAIN_S = 0.75                 # the running chain on card 5.1 (8.96 wide)


def card_5_1():
    """Card 5.1 as stated, built and lowered. Attributes:
    .rows (3 T lines, EX51_LINES; .rows[2] is the task's last sentence),
    .chain (ConsChain(RUNNING) at scale 0.75, values re-enlarged), .res_lbl ("result", DIM),
    .lift_by (how far cell 0 rises into the result row), .tail and .tail_q (the result's tail
    arrow and its GOLD "?", for after the lift), .brace and .brace_lbl ("sort the rest") under
    cells 1..4 and [] (as they sit, cell 0 removed). whole() = frame, header, rows, chain."""
    card = HeroCard(0, height=H51, step=STEP51, lifted=L51)
    card.rows = [card.at_row(T(s, size=34), k + 1) for k, s in enumerate(EX51_LINES)]
    chain = ConsChain(RUNNING).scale(CHAIN_S)
    for cell in chain.cells:
        cell.label.scale(1.1)
    chain.move_to([COL_X + 1.45 + chain.width / 2, -1.55, 0])
    card.chain = chain
    card.res_lbl = T("result", size=30, color=DIM)
    card.lift_by = 1.1
    res_y = chain.get_y() + card.lift_by
    card.res_lbl.move_to([COL_X, res_y, 0], aligned_edge=LEFT)
    c0 = chain.cells[0]
    dot = c0.tail_start() + UP * card.lift_by
    card.tail_q = T("?", size=48, color=GOLD).move_to([dot[0] + 1.25, res_y, 0])
    card.tail = Arrow(dot, card.tail_q.get_left(), buff=0.05, stroke_width=3, color=FG,
                      max_tip_length_to_length_ratio=0.3, tip_length=0.18)
    card.tail.shift(RIGHT * 0.0)
    bot = chain.cells[1].get_bottom()[1]
    card.brace = span_brace([chain.cells[1].get_left()[0], bot, 0],
                            [chain.nil.get_right()[0], bot, 0], color=DIM)
    card.brace_lbl = T("sort the rest", size=30).next_to(card.brace, DOWN, buff=0.12)
    card.lower(*card.rows, chain, card.res_lbl, card.tail, card.tail_q, card.brace, card.brace_lbl)
    card.parts += [*card.rows, chain]
    return card


STEP52 = 0.74
H52 = 0.46 + 4 * STEP52 + 0.45  # header, task, slot, two tests
L52 = 0.46 + 2 * STEP52 + 0.45  # lifted for the hint: header, task, slot


def card_5_2():
    """Card 5.2 as stated, built and lowered. Attributes:
    .task (T), .name (Code "selsort", YELLOW), .slot (Slot(EX52_TYPE)), .tests (two Codes,
    "selsort [...]  ⇒  [...]"), .rep (Tag "repeats", beside the second test).
    whole() = frame, header, task, name, slot, tests, rep."""
    card = HeroCard(1, height=H52, step=STEP52, lifted=L52)
    card.task = card.at_row(T(EX52_TASK, size=36), 1)
    card.name = Code(EX52_NAME, size=36).set_color(YELLOW)
    card.at_row(card.name, 2)
    card.slot = Slot(EX52_TYPE, size=34)
    card.slot.next_to(card.name, RIGHT, buff=0.4).set_y(card.row_y(2))
    card.tests = [card.at_row(Code(f"{a}  ⇒  {b}", size=30), 3 + k) for k, (a, b) in enumerate(EX52_TESTS)]
    card.rep = Tag(EX52_TAG, PURPLE).next_to(card.tests[1], RIGHT, buff=0.4)
    card.lower(card.task, card.name, card.slot, *card.tests, card.rep)
    card.parts += [card.task, card.name, card.slot, *card.tests, card.rep]
    return card


# ── this scene ───────────────────────────────────────────────────────────────────
class ExercisesHints1(NarratedScene):
    def construct(self):
        self.overview()
        self.sel_card()
        self.sel_hint()
        self.code_card_and_hint()
        hold_for(self, self.pause_born, len("pause and try it"))
        finish(self)

    # ex.1: "Exercises", the four cards, the routine, solutions elsewhere
    def overview(self):
        header = T("Exercises", size=52).move_to(UP * 3.0)
        ov = four_cards()
        tag = pause_tag()
        with self.say("c6.ex.1") as c:
            # "Now it's your turn."
            self.play(*appear(header), run_time=1.0)  # early: the section title
            # "The notes end with four exercises, about two more sorts."
            c.wait_until("four")
            self.play(*appear(*ov.cards, shift=0.3 * UP, lag=0.2), run_time=2.0)  # early: the four cards shown whole, each named later
            # "As before, I'll state each one, give you a hint, and pause, ..."
            c.wait_until("and pause")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.7)
            self.play(FlashAround(tag, color=YELLOW, time_width=1.5, buff=0.15), run_time=1.3)
            # "The worked solutions are in the bonus chapter, ..."
            c.wait_until("bonus")
            self.play(*appear(ov.note, shift=0.25 * UP), run_time=1.0)
        self.ov_header, self.ov, self.ov_tag = header, ov, tag

    # ex.2: the cards shrink into the strip; 5.1 grows: task, the running chain, 3 out, the rest
    def sel_card(self):
        strip = make_strip([TODO] * 4)
        card = card_5_1()
        chain, c0 = card.chain, card.chain.cells[0]
        with self.say("c6.ex.2") as c:
            # "Exercise five point one is about selection sort."  Overview -> strip; 5.1 grows.
            anims = [FadeOut(m) for m in (self.ov_header, self.ov_tag)]
            for b, p in zip(self.ov.cards, strip):
                anims += [Transform(b.frame, p.frame.copy()), Transform(b.num, p.num.copy()),
                          FadeOut(b.name, scale=0.5)]
            self.play(*anims, run_time=1.0)
            self.remove(*[m for b in self.ov.cards for m in b.get_family()])
            self.add(strip)
            self.play(*enter_card(strip, card, card.rows), *during([FadeOut(self.ov.note)], 0, 0.4),
                      run_time=1.6)  # early: the task shown whole, then walked
            # "It looks through the items, finds a smallest one, and removes it, ..."
            c.wait_until("smallest")
            self.play(*appear(chain, shift=0.2 * UP), run_time=1.0)
            c.wait_until("finds a smallest")
            self.play(*recolor([c0.label], YELLOW), FlashAround(c0, color=YELLOW, buff=0.1),
                      run_time=1.1)
            c.wait_until("removes it")
            self.play(c0.animate.shift(UP * card.lift_by), *disappear(chain.arrows[0]),
                      run_time=1.3)
            chain.remove(chain.arrows[0])        # gone for good: a later FadeOut(chain) must not revive it
            c.wait_until(own_word=card.res_lbl, cue="head")
            self.play(*appear(card.res_lbl, shift=0.2 * RIGHT), run_time=0.8)
            # "The tail comes from sorting the remaining items, recursively."
            c.wait_until("rest")
            self.play(GrowFromCenter(card.brace), *appear(card.brace_lbl), run_time=1.2)
            self.play(GrowArrow(card.tail), *appear(card.tail_q, shift=0.2 * LEFT), run_time=1.0)
            # "State its time complexity, with justification."
            c.wait_until("task")
            self.play(card.rows[2].animate.set_color(YELLOW),
                      FlashUnder(card.rows[2], color=YELLOW, time_width=1.5), run_time=1.5)
        card.keep(*card.rows, chain, card.res_lbl, card.tail, card.tail_q, card.brace,
                  card.brace_lbl)
        self.strip, self.card = strip, card

    # ex.3: hint: comparisons to find a smallest; does order matter; recurrence; pause
    def sel_hint(self):
        card = self.card
        drop = [card.chain, card.res_lbl, card.tail, card.tail_q, card.brace, card.brace_lbl]
        hl = hint_label(card)
        tl = tiles(RUNNING).move_to([-2.4, -2.05, 0])
        mk = marker(YELLOW).move_to(above(tl.sq[0], buff=0.18))
        mk_lbl = T("smallest so far", size=30, color=YELLOW).next_to(mk, RIGHT, buff=0.25)
        cnt = T("comparisons: ?", size=36, color=GOLD).move_to([1.6, -1.65, 0], aligned_edge=LEFT)
        cnt_n = T("n items: ?", size=36, color=GOLD).move_to([1.6, -2.5, 0], aligned_edge=LEFT)
        scan = SurroundingRectangle(tl.sq[1], color=BLUE, buff=0.09, corner_radius=0.08, stroke_width=3)
        orders = [mini_chain(v) for v in (RUNNING, sorted(RUNNING), sorted(RUNNING, reverse=True))]
        og = VGroup(*orders).arrange(DOWN, buff=0.32).move_to([-3.3, -2.05, 0])
        oqs = [T("?", size=44, color=GOLD).next_to(o, RIGHT, buff=0.5) for o in orders]
        tn = MathTex(r"T(n) = {?}", font_size=56, color=GOLD).move_to([-0.2, -2.0, 0])
        tab = l2_table(size=30, pitch=0.58)
        tab.move_to([CONTENT_R + 0.1, -2.0, 0], aligned_edge=RIGHT)
        # {recur}: the three questions pack into a compact column on the left and stay for the pause
        cs = 28 / 30                                     # chain values stay at 28
        o_dst = [o.copy().scale(cs) for o in orders]
        VGroup(*o_dst).arrange(DOWN, buff=0.14).move_to([COL_X + 0.1, -1.95, 0], aligned_edge=LEFT)
        q_dst = [q.copy().scale(36 / 44).next_to(o, RIGHT, buff=0.35) for q, o in zip(oqs, o_dst)]
        cnt_dst = cnt.copy().scale(30 / 36).move_to([COL_X + 0.1, -3.2, 0], aligned_edge=LEFT)
        cnt_n_dst = cnt_n.copy().scale(30 / 36).next_to(cnt_dst, RIGHT, buff=0.55)
        tag = pause_tag()

        with self.say("c6.ex.3", gap=2.1) as c:
            # "Here's the hint."  The example goes; the card goes up; the hint label beneath.
            self.play(*card.lift(drop), *during(appear(hl), 0.55, 1), run_time=1.4)
            # "How many comparisons does it take to find the smallest of five items?"
            c.wait_until("min")
            self.play(*appear(tl, cnt, lag=0.3), run_time=1.1)
            c.wait_until(own_word=mk_lbl, cue="the smallest")
            self.play(*appear(mk, mk_lbl), FadeIn(scan), run_time=0.7)
            for k in (2, 3, 4):
                self.play(Transform(scan, SurroundingRectangle(tl.sq[k], color=BLUE, buff=0.09,
                                                               corner_radius=0.08, stroke_width=3)),
                          run_time=0.4)
            # "And of N items?"
            c.wait_until("and of n items")
            self.play(*appear(cnt_n), run_time=0.9)
            # "Does that number depend on the order the items arrive in?"
            c.wait_until("order")
            self.play(*during(disappear(tl, mk, mk_lbl, scan), 0, 0.4),
                      *during(appear(*orders, lag=0.3), 0.4, 1), run_time=1.6)
            self.play(*appear(*oqs, lag=0.2), run_time=0.9)
            # "Then write a recurrence for the whole sort, ... and look for it in lecture two's table."
            c.wait_until("recur")
            self.play(*during(disappear(cnt, cnt_n), 0, 0.3),
                      *during([Transform(m, d) for m, d in zip([*orders, *oqs], [*o_dst, *q_dst])], 0.1, 0.6),
                      *during(appear(cnt_dst, cnt_n_dst, shift=None), 0.5, 0.8),
                      *during(appear(tn), 0.7, 1), run_time=min(2.2, c.until("table")))
            c.wait_until("table")
            self.play(*appear(*tab, shift=0.3 * LEFT, lag=0.15), run_time=1.3)
            # "Pause the video, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.6)
        self.hint = [hl, tn, *tab, *orders, *oqs, cnt_dst, cnt_n_dst]
        self.tag = tag

    # ex.4: 5.1 shrinks back; 5.2 grows: task, slot, the tests; hint: one helper, two results
    def code_card_and_hint(self):
        strip = self.strip
        card = card_5_2()
        hl = hint_label(card)
        box_t = T("one job, two results", size=30)
        box = RoundedRectangle(corner_radius=0.18, width=box_t.width + 0.5, height=0.75)
        box.set_stroke(BLUE, 3).set_fill(BLUE, 0.1)
        box_t.move_to(box)
        arr = Arrow(UP * 0.22, DOWN * 0.22, buff=0, stroke_width=3, color=FG,
                    max_tip_length_to_length_ratio=0.35, tip_length=0.18)
        lp, q1, cm, q2, rp = (T("(", size=50), T("?", size=50, color=GOLD), T(",", size=50),
                              T("?", size=50, color=GOLD), T(")", size=50))
        pair = VGroup(lp, q1, cm, q2, rp).arrange(RIGHT, buff=0.2)
        cm.next_to(q1, RIGHT, buff=0.6)
        q2.next_to(cm, RIGHT, buff=0.6).set_y(q1.get_y())
        rp.next_to(q2, RIGHT, buff=0.2).set_y(lp.get_y())
        cm.align_to(q1, DOWN).shift(DOWN * 0.1)
        helper = VGroup(VGroup(box, box_t), arr, pair).arrange(DOWN, buff=0.15)
        l1 = T("smallest", size=30, color=DIM).next_to(q1, DOWN, buff=0.18)
        l2 = T("rest", size=30, color=DIM).next_to(q2, DOWN, buff=0.18).align_to(l1, UP)
        hgroup = VGroup(box, box_t, arr, lp, q1, cm, q2, rp, l1, l2)
        hgroup.move_to([0, card.bottom - 0.78, 0], aligned_edge=UP)
        dy = card.h - card.h_lift            # the hint sits this much lower until the tests go
        for m in (hl, box, box_t):
            m.shift(DOWN * dy)
        uz = Code(UNZIP_SRC, size=28).set_opacity(CODE_DIM)
        uz.move_to([CONTENT_R + 0.1, card.bottom - 0.3, 0], aligned_edge=UR)
        let_line = uz.line(UNZIP_LET)
        dx = (COL_X + 0.05 + hgroup.width / 2) - hgroup.get_x()
        tag = pause_tag()

        with self.say("c6.ex.4", gap=0.7) as c:
            # "Exercise five point two."  Then a still beat.
            self.play(*exit_card(strip, self.card, [*self.hint, self.tag]), run_time=0.9)
            self.remove(self.card.frame)
            self.play(*enter_card(strip, card), run_time=0.9)
            # "Implement selection sort in OCaml."
            c.wait_until(own_word=card.task, cue="implement")
            self.play(*appear(card.task, card.name, lag=0.3),
                      *during([FadeIn(card.slot, shift=0.2 * DOWN)], 0.4, 1), run_time=1.4)
            # "Test it on our list, and on three, five, three, one, five, which has repeats."
            c.wait_until("test")
            self.play(*appear(card.tests[0]), run_time=1.0)
            c.wait_until("three five three")
            self.play(*appear(card.tests[1]), run_time=1.0)
            c.wait_until("repeats")
            self.play(*appear(card.rep, shift=0.2 * LEFT), run_time=0.8)
            card.keep(card.task, card.name, card.slot, *card.tests, card.rep)
            # "Here's the hint."  The tests go; the card goes up; the hint label beneath.
            c.wait_until("hint")
            self.play(*[m.animate.shift(UP * card.drop_y) for m in (card.frame, *card.shown)],
                      *during(appear(hl), 0.55, 1), run_time=1.2)
            card.drop_y = 0.0
            # "Finding the smallest item and removing it can be one job."
            c.wait_until("two")
            self.play(*appear(box, box_t, lag=0.1), run_time=1.0)  # early: the helper's caption, named over the next lines
            # "So write a helper that returns both at once, ..."  The tests go; the card shrinks.
            c.wait_until("returns both")
            frame = card.frame.copy().stretch_to_fit_height(card.h_lift)
            frame.move_to([0, CARD_TOP - card.h_lift / 2, 0])
            self.play(*during([FadeOut(m) for m in (*card.tests, card.rep)], 0, 0.3),
                      *during([Transform(card.frame, frame)], 0.2, 0.75),
                      *during([m.animate.shift(UP * dy) for m in (hl, box, box_t)], 0.3, 0.8),
                      *during([GrowArrow(arr)], 0.7, 1),
                      *during(appear(lp, q1, cm, q2, rp, lag=0.05), 0.75, 1), run_time=2.0)
            card.shown = [m for m in card.shown if m not in (*card.tests, card.rep)]
            c.wait_until(own_word=l1, cue="the smallest item and")
            self.play(*appear(l1), run_time=0.7)
            c.wait_until(own_word=l2, cue="the rest")
            self.play(*appear(l2), run_time=0.7)
            # "That's two results, like unzip in lecture four, and a let pattern takes them apart."
            c.wait_until("unzip")
            self.play(*[m.animate.shift(RIGHT * dx) for m in hgroup],
                      *during([FadeIn(uz, shift=0.25 * LEFT)], 0.4, 1), run_time=1.4)
            c.wait_until("let pattern")
            self.play(*[g.animate.set_fill(YELLOW, opacity=1) for g in let_line],
                      FlashAround(VGroup(*let_line), color=YELLOW, time_width=1.5), run_time=1.5)
            # "Pause, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time
