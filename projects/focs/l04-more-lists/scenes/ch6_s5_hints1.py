"""Chapter 6, scene 5: the exercises begin. Six cards; then 4.1 (set union), 4.2 (split by sign)
and 4.3 (another zip), each grown out of its pill onto a hero card: the task, its example, a GOLD
"?" wherever an answer would go (never a solution), one hint beneath, a still "pause" beat.
Clips c6.ex.1 - c6.ex.7.

THE EXERCISE-CARD KIT (the first half of this file) is shared: ch6_s6_hints2, ch6_s7_recap and the
ch7 scenes import it, e.g.

    from scenes.ch6_s5_hints1 import (six_cards, make_strip, HeroCard, Slot, pause_tag,
                                      enter_card, exit_card, TODO, CURRENT, DONE, ...)

Importing it has no side effects (definitions only; `__all__` lists the kit, so `import *` does
not pull in this scene's class). L3's kit (projects/focs/l03-lists/scenes/ch5_s6_sumlast.py),
adapted to six cards. API:

  EX_NUMS, EX_TITLES, EX_TASKS  the six cards: "4.1".."4.6", titles, task sentences (verbatim;
                     EX_TASKS[5] is None: 4.6's card is its code, EX46_TYPES / EX46_CALLS)
  EX41_* .. EX46_*   each card's code, verbatim (example, result, type, In [74], headers ...)
  MEMBER_REPLY, UNZIP_SRC, ZIP3_SRC, PHONE_EQUAL, PHONE_SHORT, ZIP74_WARNING  quoted hint code
  six_cards()        the overview: six dim BigCards in two rows of three (one row of six is not
                     legible: titles up to 20 characters) + DIM note "Solutions: bonus chapter"
                     ("bonus chapter" YELLOW). Returns a VGroup with .cards (6 BigCards) and
                     .note, at this scene's positions: rows y 1.35 / -0.30 (cards 4.1 x 1.45,
                     x -4.3 / 0 / 4.3), note y -2.95; here the header "Exercises" (T 52) sits
                     at y 3.0. Move the group as a whole if you need it elsewhere.
  BigCard(i)         one overview card: .frame .num (T 42) .name (T 28, DIM)
  make_strip(states) the six small pills, top left at y STRIP_Y; states TODO / CURRENT / DONE;
                     restyled(pill, state) animates one. This scene ends with [DONE]*3 + [TODO]*3.
  HeroCard(i, height, step=ROW_STEP)  the current exercise, CARD_W wide, top at CARD_TOP:
                     .frame, .header ("Exercise 4.k  ·  Title", T 38, number YELLOW),
                     .row_y(k) / .at_row(mob, k, x=COL_X) (row 0 = header), .tag(text, color)
                     (tags on the header row), .lower(*items) (call once all is built: drops the
                     card and items to the centre while it's stated), .lift() (anims taking it
                     and everything kept back up for the hint), .keep(*mobs), .bottom (lifted)
  Slot(type_src=None, ...)  the dashed box where the student's code goes, with a GOLD "?";
                     with a type it is one row: "?  : <type>" (type GREEN)
  Tag(text, color)   a rounded label (card.tag makes and places one)
  enter_card(strip, card) / exit_card(strip, card, extra)  grow out of / shrink back into its
                     pill (then scene.remove(card.frame))
  hint_label(card, chapter=None), pause_tag() (top right, "pause and try it"), pause_icon(),
  split_line(src, parts, ...), fit(c, cue), first_cue, hold_for(scene, born, n), finish(scene),
  glyph(code, sub, ...)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, select, time_span  # noqa: E402
from lib.kit import token_box  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

__all__ = [
    "CARD_FILL", "CARD_W", "CARD_L", "CARD_R", "CARD_TOP", "PAD", "COL_X", "CONTENT_R", "ROW0",
    "ROW_STEP", "STRIP_Y", "PILL_W", "PILL_H", "CODE_DIM", "CARD_CENTER_Y", "BIG_W", "BIG_H",
    "EX_NUMS", "EX_TITLES", "EX_TASKS",
    "EX41_CALL", "EX41_RESULT", "EX41_TAG", "EX42_INPUT", "EX42_RESULT", "EX42_TYPE",
    "EX43_ZIP", "EX43_REPLY", "EX43_QUESTION", "EX44_HEADERS", "EX44_LABELS", "EX46_TYPES",
    "EX46_CALLS", "MEMBER_REPLY", "UNZIP_SRC", "ZIP3_SRC", "PHONE_EQUAL", "PHONE_SHORT",
    "ZIP74_WARNING",
    "TODO", "CURRENT", "DONE", "PILL_STYLE",
    "row_y", "at_row", "fit", "first_cue", "Pill", "make_strip", "restyled", "BigCard",
    "six_cards", "Slot", "Tag", "HeroCard", "split_line", "hint_label", "pause_icon",
    "pause_tag", "enter_card", "exit_card", "hold_for", "finish", "glyph",
]

# ── the exercise-card kit (shared with ch6_s6, ch6_s7 and ch7) ─────────────────────
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
BIG_W, BIG_H = 4.1, 1.45       # an overview card

EX_NUMS = ("4.1", "4.2", "4.3", "4.4", "4.5", "4.6")
EX_TITLES = ("Set union", "Split by sign", "Another zip", "Hidden assumptions",
             "Counting the ways", "What the types force")
EX_TASKS = (
    "Sets are lists with no repeats. Using member, code set union.",
    "Return two lists: the non-negative numbers, and the negative ones.",
    "How does it differ?",
    "What do the change functions assume about till and amt? "
    "What could happen if those assumptions fail?",
    "Two coin values: show there are O(n) ways to make change for n (ignoring order). "
    "Three values? Four? …",
    None,                      # 4.6: the card is its code (EX46_TYPES, EX46_CALLS)
)

# each card's code (verbatim; checked by the script-writer)
EX41_CALL, EX41_RESULT, EX41_TAG = "union [4; 7; 1] [6; 4; 7]", "[1; 6; 4; 7]", "any order"
EX42_INPUT, EX42_RESULT = "[3; -1; 0; -5; 2]", "([3; 0; 2], [-1; -5])"
EX42_TYPE = "int list -> int list * int list"
EX43_ZIP = ("let rec zip xs ys =\n"                       # In [74]
            "  match xs, ys with\n"
            "  | (x::xs, y::ys) -> (x, y) :: zip xs ys\n"
            "  | ([], [])   -> []")
EX43_REPLY = "val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>"
EX43_QUESTION = "How does it differ?"
EX44_HEADERS = ("let rec change till amt =", "let rec change till amt =",
                "let rec change till amt chg chgs =")
EX44_LABELS = ("greedy", "every way", "faster")
EX46_TYPES = ("val f : 'a * 'b -> 'b * 'a", "val g : 'a -> 'a list")
EX46_CALLS = ("f (1, true)", "g 0")

# code the hints quote from earlier chapters (verbatim)
MEMBER_REPLY = "val member : 'a -> 'a list -> bool = <fun>"         # ch2
UNZIP_SRC = ("let rec unzip = function\n"                          # ch3, In [65]
             "  | [] -> ([], [])\n"
             "  | (x, y)::pairs ->\n"
             "      let xs, ys = unzip pairs in\n"
             "      (x::xs, y::ys)")
ZIP3_SRC = ("let rec zip xs ys =\n"                                # ch3, In [64]
            "  match xs, ys with\n"
            "  | (x::xs, y::ys) -> (x, y) :: zip xs ys\n"
            "  | _ -> []")
PHONE_EQUAL = 'zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]'             # ch3's phone book
PHONE_SHORT = 'zip ["Amy"; "Bob"; "Cleo"] [21; 35]'
ZIP74_WARNING = ("Warning 8 [partial-match]: this pattern-matching is not exhaustive.\n"
                 "  Here is an example of a case that is not matched: (x::xs, [])")

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
    """The six pills in a row, top left (6.8 wide, left edge at CARD_L, y STRIP_Y)."""
    s = VGroup(*[Pill(i, st) for i, st in enumerate(states)]).arrange(RIGHT, buff=0.16)
    return s.move_to([CARD_L, STRIP_Y, 0], aligned_edge=LEFT)


def restyled(pill, state):
    """Animate a pill (already on screen) to a new state."""
    target = pill.copy().restyle(state)
    pill.state = state
    return Transform(pill, target)


class BigCard(VGroup):
    """One of the six cards as the hero of the overview: number and title."""

    def __init__(self, i, **kw):
        super().__init__(**kw)
        self.i = i
        self.frame = RoundedRectangle(corner_radius=0.2, width=BIG_W, height=BIG_H)
        self.frame.set_stroke(DIM, 2.5).set_fill(CARD_FILL, 1)
        self.num = T(EX_NUMS[i], size=42).move_to(self.frame.get_center() + UP * 0.3)
        self.name = T(EX_TITLES[i], size=28, color=DIM).move_to(self.frame.get_center() + DOWN * 0.34)
        self.add(self.frame, self.num, self.name)


def six_cards():
    """The overview: six dim cards (two rows of three) and the note. See the module docstring."""
    cards = VGroup(*[BigCard(i) for i in range(6)])
    for i, b in enumerate(cards):
        b.move_to([(i % 3 - 1) * (BIG_W + 0.2), 1.35 if i < 3 else -0.30, 0])
    note = T("Solutions: bonus chapter", size=34, color=DIM, t2c={"bonus chapter": YELLOW})
    note.move_to(DOWN * 2.95)
    row = VGroup(cards, note)
    row.cards, row.note = cards, note
    return row


class Slot(VGroup):
    """The dashed box where the student's code goes, with a GOLD "?". Without a type: a box of
    the given size with a big "?". With a type: one row, "?  : <type>", the type GREEN."""

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
            VGroup(self.q, self.sig).arrange(RIGHT, buff=0.32)
            parts = [self.q, self.sig]
            w, h = VGroup(*parts).width + 0.6, 0.52
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
    """The current exercise, big. Only its frame and header come with it; the rest is built by
    the scene (rows at card.row_y(k), slots, tags on the header row) and shown beat by beat.

    Everything is laid out at the top of the frame; then lower(...) drops the card and its
    items to the middle, where it waits while it's being stated (a balanced frame), and
    lift() takes it back up when its hint needs the room below."""

    def __init__(self, i, height, step=ROW_STEP, **kw):
        super().__init__(**kw)
        self.i, self.h, self.step = i, height, step
        self.drop_y = max(0.0, CARD_TOP - (CARD_CENTER_Y + height / 2))
        self.frame = RoundedRectangle(corner_radius=0.22, width=CARD_W, height=height)
        self.frame.set_stroke(YELLOW, 3).set_fill(CARD_FILL, 1)
        self.frame.move_to([0, CARD_TOP - height / 2, 0])
        num = f"Exercise {EX_NUMS[i]}"
        self.header = self.at_row(T(f"{num}  ·  {EX_TITLES[i]}", size=38,
                                    t2c={num: YELLOW, "·": DIM}), 0)
        self.add(self.frame, self.header)
        self.tags = []
        self.shown = [self.header]      # everything on the card that leaves with it

    def row_y(self, k):
        return row_y(k, self.step)

    def at_row(self, mob, k, x=COL_X):
        return at_row(mob, k, x, self.step)

    @property
    def bottom(self):
        """Where the card's bottom edge is once lifted (hints are laid out against this)."""
        return CARD_TOP - self.h

    def lower(self, *items):
        """Call once everything for the card is built: drop it all to the waiting position."""
        for m in (self.frame, self.header, *self.tags, *items):
            m.shift(DOWN * self.drop_y)
        return self

    def lift(self):
        """Animations taking the card and everything shown on it up to the top."""
        return [m.animate.shift(UP * self.drop_y) for m in (self.frame, *self.shown)]

    def tag(self, text, color=BLUE):
        t = Tag(text, color)
        prev = self.tags[-1] if self.tags else self.header
        t.next_to(prev, RIGHT, buff=0.2 if self.tags else 0.45).set_y(self.row_y(0))
        self.tags.append(t)
        return t

    def keep(self, *mobs):
        self.shown.extend(mobs)
        return mobs[0] if len(mobs) == 1 else mobs


def split_line(src, parts, size=36, k=None, x=COL_X, y=None, step=ROW_STEP):
    """Lay out a whole line of code (left edge at x, on card row k or at height y), then
    return each part as its own Code placed exactly where it sits in the line (same glyphs,
    so the same box), to reveal them one by one."""
    full = Code(src, size=size)
    if k is not None:
        at_row(full, k, x, step)
    if y is not None:
        full.move_to([x, y, 0], aligned_edge=LEFT)
    out = []
    for p in parts:
        piece = Code(p, size=size)
        piece.move_to(VGroup(*full.find(p)))
        out.append(piece)
    return out


def hint_label(card, chapter=None):
    text = "Hint" if chapter is None else f"Hint · from chapter {chapter}"
    lab = T(text, size=32, color=DIM, t2c={"Hint": YELLOW})
    return lab.move_to([COL_X, card.bottom - 0.4, 0], aligned_edge=LEFT)


def pause_icon(color=YELLOW, h=0.34):
    bars = VGroup(*[RoundedRectangle(corner_radius=0.03, width=h * 0.3, height=h) for _ in range(2)])
    bars.arrange(RIGHT, buff=h * 0.27).set_stroke(width=0).set_fill(color, 1)
    return bars


def pause_tag():
    tag = VGroup(pause_icon(), T("pause and try it", size=30)).arrange(RIGHT, buff=0.22)
    return tag.move_to([CARD_R, STRIP_Y, 0], aligned_edge=RIGHT)


def enter_card(strip, card, light=True):
    """The card grows out of its pill, which lights up as the current one (light=False if
    the pill is already lit, e.g. a strip that is fading in with it)."""
    p = strip[card.i]
    anims = [TransformFromCopy(p.frame, card.frame), FadeTransform(p.num.copy(), card.header)]
    return anims + ([restyled(p, CURRENT)] if light else [])


def exit_card(strip, card, extra=()):
    """Everything on the card (and `extra`, the hint) fades; the frame shrinks back into its
    pill, which is now marked done. Call scene.remove(card.frame) after the play."""
    p = strip[card.i]
    done = p.copy().restyle(DONE)
    return ([FadeOut(m) for m in (*card.shown, *extra)]
            + [Transform(card.frame, done.frame), restyled(p, DONE)])


def hold_for(scene, born, text_len):
    """Before a scene's final fade: let text born at `born` reach its reading time."""
    need = 4.0 + text_len / 12.0 + 0.2
    if scene.time < born + need:
        scene.wait(born + need - scene.time)


def finish(scene):
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)
    scene.wait(0.15)   # the last play() never renders its final (empty) frame


def glyph(code, sub, line=None, nth=0, idx=0):
    """One glyph: character `idx` of the nth occurrence of `sub`."""
    return code.find(sub, line=line, nth=nth)[idx]


# ── this scene ───────────────────────────────────────────────────────────────────
H41 = 0.46 + 3 * ROW_STEP + 0.46     # 4.1: header, two task rows, the example
STEP42 = 0.66
H42 = 0.46 + 4 * STEP42 + 0.06 + 0.42   # 4.2: header, two task rows, the slot, the example


def t_part(text, sub):
    """A copy of the glyphs of `sub` in a T line, in place (to reveal a line piece by piece)."""
    return select(text, sub)[0].copy()


class ExercisesHints1(NarratedScene):
    def construct(self):
        self.overview()
        self.union_card()
        self.union_hint()
        self.sign_card()
        self.sign_hint()
        self.zip_card()
        self.zip_hint()
        hold_for(self, self.pause_born, len("pause and try it"))
        # 4.3 shrinks back into its pill; the strip (4.1-4.3 done) holds, then fades: s6 opens on it
        self.play(*exit_card(self.strip, self.card, [*self.hint, self.tag]), run_time=1.1)
        self.remove(self.card.frame)
        self.wait(0.9)
        finish(self)

    # ex.1: "Exercises", the six cards, the routine (task, hint, pause), solutions elsewhere
    def overview(self):
        header = T("Exercises", size=52).move_to(UP * 3.0)
        ov = six_cards()
        bigs, note = ov.cards, ov.note
        s1, s2 = T("the task", size=36), T("a hint", size=36)
        s3 = VGroup(pause_icon(h=0.36), T("pause", size=36)).arrange(RIGHT, buff=0.2)
        a1, a2 = [Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, stroke_width=3, color=DIM,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.16) for _ in range(2)]
        steps = VGroup(s1, a1, s2, a2, s3).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.95)

        with self.say("c6.ex.1") as c:
            # "Now it's your turn."
            self.play(FadeIn(header, shift=0.3 * DOWN), run_time=1.0)
            # "The notes end with six exercises."
            c.wait_until("six")
            self.play(LaggedStart(*[FadeIn(b, shift=0.3 * UP) for b in bigs], lag_ratio=0.15),
                      run_time=2.2)
            # "As in lecture three, I'll state each one, give you a hint, and then pause, ..."
            c.wait_until("state")
            self.play(FadeIn(s1, shift=0.25 * DOWN), run_time=fit(c, "a hint", hi=0.9))
            c.wait_until("a hint")
            self.play(GrowArrow(a1), FadeIn(s2, shift=0.25 * DOWN), run_time=fit(c, "then pause", hi=0.9))
            c.wait_until("then pause")
            self.play(GrowArrow(a2), FadeIn(s3, shift=0.25 * DOWN), run_time=0.9)
            # "The worked solutions are in the bonus chapter, for after you've had a go."
            c.wait_until("bonus")
            self.play(FadeIn(note, shift=0.25 * UP), run_time=1.0)
        self.bigs, self.ov_header, self.steps, self.note = bigs, header, steps, note

    # ex.2: the cards shrink into the strip; 4.1 grows into the hero card
    def union_card(self):
        strip = make_strip([TODO] * 6)
        card = HeroCard(0, height=H41)
        r1 = card.at_row(T("Sets are lists with no repeats.", size=34), 1)
        r2 = card.at_row(T("Using member, code set union.", size=34, t2c={"member": YELLOW}), 2)
        slot = Slot(width=3.6, height=1.25)
        slot.move_to([CONTENT_R - slot.width / 2, (card.row_y(1) + card.row_y(2)) / 2, 0])
        ex_in, ex_out = split_line(f"{EX41_CALL}  ⇒  {EX41_RESULT}", [EX41_CALL, f"⇒  {EX41_RESULT}"],
                                   size=34, y=card.row_y(3))
        tag = card.tag(EX41_TAG)
        card.lower(r1, r2, slot, ex_in, ex_out)

        with self.say("c6.ex.2") as c:
            # "Exercise four point one."  The overview clears; its cards become the strip.
            anims = [FadeOut(m) for m in (self.ov_header, *self.steps)]
            for b, p in zip(self.bigs, strip):
                anims += [Transform(b.frame, p.frame.copy()), Transform(b.num, p.num.copy()),
                          FadeOut(b.name, scale=0.5)]
            self.play(*anims, run_time=1.0)
            self.remove(*[m for b in self.bigs for m in b.get_family()])
            self.add(strip)
            self.play(*enter_card(strip, card), run_time=1.0)
            # "You can represent a set as a list with no repeated items."
            c.wait_until("sets")
            self.play(FadeIn(r1, shift=0.25 * DOWN), run_time=1.0)
            # "Using member, from chapter two, write a function for set union."
            c.wait_until("task")
            self.play(FadeIn(r2, shift=0.25 * DOWN), FadeIn(slot.box), FadeIn(slot.q, scale=0.7),
                      run_time=1.1)
            # "Take the lists four, seven, one, and six, four, seven."
            c.wait_until("example")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), FadeOut(self.note), run_time=1.0)
            # "Their union should be one, six, four, seven."
            c.wait_until("their union")
            self.play(FadeIn(ex_out, shift=0.25 * LEFT), run_time=0.9)
            # "Any order is fine."
            c.wait_until("order")
            self.play(FadeIn(tag, shift=0.2 * DOWN), run_time=0.8)
        card.keep(r1, r2, slot.box, slot.q, ex_in, ex_out, tag)
        self.strip, self.card, self.ex_in = strip, card, ex_in

    # ex.3: hint: member (ch2); walk the first list, ask of each element; pause
    def union_hint(self):
        card, ex_in = self.card, self.ex_in
        hl = hint_label(card, 2)
        reply = Code(MEMBER_REPLY, size=28).set_opacity(CODE_DIM)
        reply.move_to([COL_X, hl.get_y() - 0.58, 0], aligned_edge=LEFT)
        xs, ys = Code("[4; 7; 1]", size=48), Code("[6; 4; 7]", size=48)
        VGroup(xs, ys).arrange(RIGHT, buff=1.3).move_to(DOWN * 2.9)
        elems = [glyph(xs, d) for d in ("4", "7", "1")]
        qs = [T("?", size=40, color=GOLD).move_to([e.get_x(), xs.get_top()[1] + 0.42, 0]) for e in elems]
        ring = SurroundingRectangle(ys, color=BLUE, buff=0.16, corner_radius=0.12, stroke_width=3)
        tag = pause_tag()

        with self.say("c6.ex.3") as c:
            # "Here's the hint."  The card goes up; member's type comes back from chapter 2.
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4),
                      time_span(FadeIn(reply, shift=0.25 * DOWN), 0.8, 1.6), run_time=1.6)
            # "Walk down the first list, one element at a time."  (the two lists come out of the example)
            c.wait_until("walk")
            self.play(TransformFromCopy(VGroup(*ex_in.find("[4; 7; 1]")), xs),
                      TransformFromCopy(VGroup(*ex_in.find("[6; 4; 7]")), ys),
                      run_time=fit(c, "one element", hi=1.3))
            box = token_box([elems[0]], xs, color=YELLOW, pad=0.2)
            c.wait_until("one element")
            self.play(FadeIn(box), FadeIn(qs[0], shift=0.2 * DOWN), run_time=0.7)
            c.wait_until("at a time")
            self.play(Transform(box, token_box([elems[1]], xs, color=YELLOW, pad=0.2)),
                      FadeIn(qs[1], shift=0.2 * DOWN), run_time=0.5)
            # "Keep only the elements that are missing from the second list."
            c.wait_until("keep")
            self.play(Transform(box, token_box([elems[2]], xs, color=YELLOW, pad=0.2)),
                      FadeIn(qs[2], shift=0.2 * DOWN), run_time=0.5)
            c.wait_until("second list")
            self.play(Create(ring), FlashAround(ys, color=BLUE, buff=0.3), run_time=1.1)
            # "Pause the video, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.hint = [hl, reply, xs, ys, box, *qs, ring]
        self.tag = tag

    # ex.4: 4.1 shrinks back into its pill; 4.2 grows
    def sign_card(self):
        strip = self.strip
        card = HeroCard(1, height=H42, step=STEP42)
        l1 = card.at_row(T("Return two lists: the non-negative numbers,", size=34), 1)
        p1, p2 = t_part(l1, "Return two lists:"), t_part(l1, "the non-negative numbers,")
        p3 = card.at_row(T("and the negative ones.", size=34), 2)
        slot = card.at_row(Slot(EX42_TYPE, size=30), 3)
        ex_in, ex_out = split_line(f"{EX42_INPUT}  ⇒  {EX42_RESULT}", [EX42_INPUT, f"⇒  {EX42_RESULT}"],
                                   size=34, y=card.row_y(4) - 0.06)
        card.lower(p1, p2, p3, slot, ex_in, ex_out)

        with self.say("c6.ex.4") as c:
            # "Exercise four point two."
            self.play(*exit_card(strip, self.card, self.hint), run_time=1.0)
            self.remove(self.card.frame)
            self.play(*enter_card(strip, card), run_time=1.0)
            # "Write a function that takes a list of integers and returns two lists."
            c.wait_until("task")
            self.play(FadeIn(slot.box), FadeIn(slot.q, scale=0.7), FadeIn(slot.sig, shift=0.2 * DOWN),
                      FadeOut(self.tag), run_time=fit(c, "returns two lists", hi=1.2))
            c.wait_until("returns two lists")
            self.play(FadeIn(p1, shift=0.25 * DOWN), run_time=0.9)
            # "The first holds the numbers that are zero or more."
            c.wait_until("first")
            self.play(FadeIn(p2, shift=0.25 * DOWN), run_time=1.0)
            # "The second holds the negative ones."
            c.wait_until("second")
            self.play(FadeIn(p3, shift=0.25 * DOWN), run_time=1.0)
            # "So three, minus one, zero, minus five, two, splits into three, zero, two, and ..."
            c.wait_until("example")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("splits into")
            self.play(FadeIn(ex_out, shift=0.25 * LEFT), run_time=0.9)
        card.keep(p1, p2, p3, slot.box, slot.q, slot.sig, ex_in, ex_out)
        self.card, self.ex_in = card, ex_in

    # ex.5: hint from chapter 3: unzip builds two results, its let takes them apart; mind the 0
    def sign_hint(self):
        card, ex_in = self.card, self.ex_in
        hl = hint_label(card, 3)
        uz = Code(UNZIP_SRC, size=28).set_opacity(CODE_DIM)
        uz.move_to([CONTENT_R + 0.1, card.bottom - 0.22, 0], aligned_edge=UR)
        let_line = uz.line(3)
        zero = glyph(ex_in, "0")
        z0 = Code("0", size=48).set_color(GOLD)
        za = Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, stroke_width=4, color=GOLD,
                   max_tip_length_to_length_ratio=0.3, tip_length=0.18)
        zq = T("?", size=48, color=GOLD)
        hl.set_y(uz.line(1)[0].get_y())
        VGroup(z0, za, zq).arrange(RIGHT, buff=0.25).move_to([(COL_X + uz.get_left()[0]) / 2,
                                                                 uz.line(3)[0].get_y() - 0.1, 0])
        tag = pause_tag()

        with self.say("c6.ex.5") as c:
            # "The hint is in chapter three."
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # "You're building two results at once, just as unzip did."
            c.wait_until("two")
            self.play(FadeIn(uz, shift=0.25 * UP), run_time=1.0)
            # "So remember how unzip used a let, to take its pair of results apart."
            c.wait_until("let")
            self.play(*[g.animate.set_fill(YELLOW, opacity=1) for g in let_line],
                      FlashAround(VGroup(*let_line), color=YELLOW, time_width=1.5), run_time=1.5)
            # "And watch where zero goes."  Then the screen is still.
            c.wait_until("zero")
            self.play(zero.animate.set_color(GOLD), FlashAround(zero, color=GOLD, buff=0.08),
                      TransformFromCopy(zero, z0), run_time=1.3)
            self.play(GrowArrow(za), FadeIn(zq, shift=0.2 * LEFT), run_time=0.8)
            # "Pause, and try it."
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.hint = [hl, uz, z0, za, zq]
        self.tag = tag

    # ex.6: 4.2 shrinks back; 4.3 grows: In [74], its new last clause, its type, the question
    def zip_card(self):
        strip = self.strip
        zc = Code(EX43_ZIP, size=30)
        card = HeroCard(2, height=0.84 + zc.height + 0.34)
        zc.move_to([COL_X, ROW0 - 0.38, 0], aligned_edge=UL)
        pat = zc.find("([], [])", line=3)
        g_lab = T("chapter 3:", size=30, color=DIM)
        ghost = Code("| _ -> []", size=30).set_opacity(0.45)
        VGroup(g_lab, ghost).arrange(RIGHT, buff=0.3)
        g_lab.move_to([zc.line(3)[-1].get_right()[0] + 1.3, zc.line(3)[0].get_y(), 0], aligned_edge=LEFT)
        ghost.next_to(g_lab, RIGHT, buff=0.3)
        q_tag = card.tag(EX43_QUESTION, GOLD)
        card.lower(zc, g_lab, ghost)
        reply = Code(EX43_REPLY, size=28).move_to([0, card.frame.get_bottom()[1] - 0.38, 0])

        with self.say("c6.ex.6") as c:
            # "Exercise four point three."  Then a still beat.
            self.play(*exit_card(strip, self.card, self.hint), run_time=1.0)
            self.remove(self.card.frame)
            self.play(*enter_card(strip, card), run_time=1.0)
            # "Here's another version of the zip function."
            c.wait_until("code")
            self.play(FadeIn(zc, shift=0.25 * DOWN), FadeOut(self.tag), run_time=1.4)
            # "Where chapter three's version had a wildcard, this one has a clause for two empty lists."
            c.wait_until("wildcard")
            self.play(FadeIn(g_lab, shift=0.2 * LEFT), FadeIn(ghost, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("two empty lists")
            self.play(*[g.animate.set_color(YELLOW) for g in pat],
                      FlashAround(VGroup(*pat), color=YELLOW, time_width=1.5), run_time=1.4)
            # "Its type is exactly the same."
            c.wait_until("type")
            self.play(FadeIn(reply, shift=0.25 * UP), run_time=1.0)
            # "So how does it behave differently?"
            c.wait_until("task")
            self.play(FadeIn(q_tag, shift=0.2 * DOWN), run_time=0.9)
        card.keep(zc, g_lab, ghost, q_tag, reply)      # the reply goes up with the card
        self.card = card

    # ex.7: hint: ch3's phone book, even and uneven; the warning OCaml prints; pause
    def zip_hint(self):
        card = self.card
        hl = hint_label(card)
        hl.set_y(card.bottom - 0.38 - 0.55)          # under the reply (lifted to card.bottom - 0.38)
        c1, c2 = Code(PHONE_EQUAL, size=28), Code(PHONE_SHORT, size=28)
        c1.move_to([hl.get_right()[0] + 0.55, hl.get_y(), 0], aligned_edge=LEFT)
        c2.move_to([c1.get_left()[0], c1.get_y() - 0.52, 0], aligned_edge=LEFT)
        ax = c1.get_right()[0] + 0.45
        arrs, qs = [], []
        for cl in (c1, c2):
            a = Mono("⇒", size=28).move_to([ax, cl.get_y(), 0], aligned_edge=LEFT)
            arrs.append(a)
            qs.append(T("?", size=40, color=GOLD).next_to(a, RIGHT, buff=0.3))
        warn = Code(ZIP74_WARNING, size=23).set_color(RED)
        warn.move_to([0, c2.get_y() - 0.78, 0])
        hidden = warn.find("(x::xs, [])", line=1)
        for g in hidden:
            g.set_opacity(0)                 # the example is never shown: the "?" covers it
        hv = VGroup(*hidden)
        cover = RoundedRectangle(corner_radius=0.08, width=hv.width + 0.3, height=0.44)
        cover.move_to(hv).set_stroke(GOLD, 2.5).set_fill(GOLD, 0.15)
        cq = T("?", size=32, color=GOLD).move_to(cover)
        tag = pause_tag()

        with self.say("c6.ex.7") as c:
            # "Here's the hint."
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # "Try it on two lists of the same length, and then on lists of different lengths."
            c.wait_until("two lists")
            self.play(FadeIn(c1, shift=0.25 * DOWN), FadeIn(arrs[0], shift=0.2 * RIGHT),
                      FadeIn(qs[0], scale=0.7), run_time=1.0)
            c.wait_until("different lengths")
            self.play(FadeIn(c2, shift=0.25 * DOWN), FadeIn(arrs[1], shift=0.2 * RIGHT),
                      FadeIn(qs[1], scale=0.7), run_time=0.8)
            # "Also, when you type it in, OCaml prints a warning."
            c.wait_until("warning")
            self.play(FadeIn(warn, shift=0.25 * UP), FadeIn(cover), FadeIn(cq, scale=0.7), run_time=1.3)
            # "Read it carefully, because it even gives you an example."
            c.wait_until("an example")
            self.play(FlashAround(cover, color=GOLD, time_width=1.5, buff=0.08), run_time=1.4)
            # "Pause, and think it through."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time
        self.hint = [hl, c1, c2, *arrs, *qs, warn, cover, cq]
        self.tag = tag
