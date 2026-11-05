"""STATUS (paused): done: ex.1-ex.5 rendered (99 s), dwell 0 flags, reviewed at 480p; owns the
shared card kit (s7 imports it). remaining: ch5_s8_tails.py NOT STARTED. Plan for it: strip
fades in (4 DONE, 3.5 CURRENT), HeroCard(4, height~3.22, slot "'a list -> 'a list list");
task "Return all the tails of a list." row 1; `tails [1; 2; 3]  ⇒` row 2; result row at y~-0.1
full width, four dashed placeholders at "four lists", each element TransformFromCopy'd from the
input's suffix on {whole}/{two}/{three}, `[]` TEAL on {nil}. ex.12: card.lift() + hint_label(1),
ConsChain 1,2,3 (S~0.85) left, TEAL box hopping whole -> [2;3] -> [3] -> nil (matching result
turns TEAL), DIM "Bonus question:" + GOLD "how many new cons cells?" right; pause_tag on {try}.
Recap: exit_card, strip fades as title "Lists" + DIM rule (bookends the title card) arrives;
6 rows (icon col x~-5.4, text left x~-4.2, T 32 / Code 30 / MathTex 44, pitch 0.75 from y 2.0):
mini cons cell | "Every list is [] or head :: tail, and cons is O(1)"; `x :: xs` | "Pattern
matching: a case for each shape"; `'a 'b` | "Polymorphism: one function, lists of any type";
GOLD box n | "An accumulator makes it iterative: O(1) space"; RED `@` -> TEAL `::` on {r6} |
`nrev` O(n^2) then "-> rev_app O(n)" + "reduction in strength"; `"abc"` | "string and char are
types of their own, not lists". ch1-style: new row in, previous dims to 0.5; {next} all back to
1 + five DONE pills at y~-2.95; {bonus} "-> Solutions: bonus chapter"; end card holds ~8 s after
the last word (coordinator), then finish(). known issues: none seen; hint codes for 3.1 are shown
unindented so nlength/addlen fit side by side.

Chapter 5, scene 6: the exercises begin. The five exercise cards, then 3.1 (sum) and
3.2 (last). Each exercise grows out of its card onto a hero card: the task, its example,
and a GOLD "?" in a dashed slot where the student's code would go. Then one hint below the
card, and a still "pause and try it" beat. Never a solution: those are in the bonus chapter.

Clips c5.ex.1 - c5.ex.5.

The exercise-card kit below (strip of pills, hero card, slot, tags, hint label, pause tag,
enter/exit moves) is shared with ch5_s7_evensid.py and ch5_s8_tails.py, which import it,
so all five exercises look and move the same way.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, VShowPassingFlash, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the exercise-card kit (shared with ch5_s7 and ch5_s8) ──────────────────────────
CARD_FILL = "#161A21"          # a card's face: a shade lighter than the background
CARD_W = 13.0                  # hero card width (frame is 14.2 wide)
CARD_L, CARD_R = -CARD_W / 2, CARD_W / 2
CARD_TOP = 2.72                # just under the strip of pills
PAD = 0.42
COL_X = CARD_L + PAD           # left edge of the card's content
ROW0 = CARD_TOP - 0.46         # centre of the header row
ROW_STEP = 0.75                # row pitch inside a card
STRIP_Y = 3.2                  # the strip of five pills (top left) and the pause tag (top right)
PILL_W, PILL_H = 1.0, 0.5
CODE_DIM = 0.6                 # opacity of "remember this" code in a hint
CARD_CENTER_Y = 0.0            # while it's being stated, a card waits centred in the frame

EXERCISES = [("3.1", ["sum"]), ("3.2", ["last"]), ("3.3", ["even", "positions"]),
             ("3.4", ["two strange", "types"]), ("3.5", ["tails"])]
TODO, CURRENT, DONE = "todo", "current", "done"
PILL_STYLE = {TODO: (DIM, 2.0, DIM), CURRENT: (YELLOW, 3.0, YELLOW), DONE: (BLUE, 2.5, FG)}


def row_y(k):
    return ROW0 - ROW_STEP * k


def at_row(mob, k, x=COL_X):
    """Left-align `mob` at x on card row k (row 0 is the header row)."""
    return mob.move_to([x, row_y(k), 0], aligned_edge=LEFT)


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
        self.num = T(EXERCISES[i][0], size=28)
        self.add(self.frame, self.num)
        self.restyle(state)

    def restyle(self, state):
        stroke, width, text = PILL_STYLE[state]
        self.frame.set_stroke(stroke, width)
        self.num.set_color(text)
        self.state = state
        return self


def make_strip(states):
    s = VGroup(*[Pill(i, st) for i, st in enumerate(states)]).arrange(RIGHT, buff=0.16)
    return s.move_to([CARD_L, STRIP_Y, 0], aligned_edge=LEFT)


def restyled(pill, state):
    """Animate a pill (already on screen) to a new state."""
    target = pill.copy().restyle(state)
    pill.state = state
    return Transform(pill, target)


class BigCard(VGroup):
    """One of the five cards as the hero of the overview: number and short name."""

    def __init__(self, i, **kw):
        super().__init__(**kw)
        self.frame = RoundedRectangle(corner_radius=0.2, width=2.4, height=1.8)
        self.frame.set_stroke(DIM, 2.5).set_fill(CARD_FILL, 1)
        self.num = T(EXERCISES[i][0], size=46).move_to(self.frame.get_center() + UP * 0.38)
        self.name = VGroup(*[T(w, size=28, color=DIM) for w in EXERCISES[i][1]]).arrange(DOWN, buff=0.1)
        self.name.move_to(self.frame.get_center() + DOWN * 0.05, aligned_edge=UP)
        self.add(self.frame, self.num, self.name)


class Slot(VGroup):
    """The dashed box where the student's code goes: its target type on top, a GOLD "?"."""

    def __init__(self, type_src, height=1.6, **kw):
        super().__init__(**kw)
        self.sig = Code(type_src, size=28)
        w = max(3.4, self.sig.width + 0.6)
        self.box = DashedVMobject(RoundedRectangle(corner_radius=0.18, width=w, height=height),
                                  num_dashes=int(6 * (w + height))).set_stroke(DIM, 2.5)
        self.sig.move_to(self.box.get_top() + DOWN * 0.36)
        self.q = T("?", size=84, color=GOLD)
        self.q.move_to([self.box.get_x(), (self.sig.get_bottom()[1] + self.box.get_bottom()[1]) / 2, 0])
        self.add(self.box, self.sig, self.q)


class Tag(VGroup):
    def __init__(self, text, color=BLUE, **kw):
        super().__init__(**kw)
        self.label = T(text, size=28, color=color)
        self.box = RoundedRectangle(corner_radius=0.22, width=self.label.width + 0.4, height=0.48)
        self.box.set_stroke(color, 2).set_fill(color, 0.12)
        self.box.move_to(self.label)
        self.add(self.box, self.label)


class HeroCard(VGroup):
    """The current exercise, big. Only its frame and header come with it; the rest is built
    by the scene (rows at row_y(k), the slot top-right under the header row, tags on the
    header row) and shown beat by beat.

    Everything is laid out at the top of the frame; then lower(...) drops the card and its
    items to the middle, where it waits while it's being stated (a balanced frame), and
    lift() takes it back up when its hint needs the room below."""

    def __init__(self, i, height, slot_type=None, slot_height=1.6, **kw):
        super().__init__(**kw)
        self.i = i
        self.h = height
        self.drop_y = max(0.0, CARD_TOP - (CARD_CENTER_Y + height / 2))
        self.frame = RoundedRectangle(corner_radius=0.22, width=CARD_W, height=height)
        self.frame.set_stroke(YELLOW, 3).set_fill(CARD_FILL, 1)
        self.frame.move_to([0, CARD_TOP - height / 2, 0])
        self.header = at_row(T(f"Exercise {EXERCISES[i][0]}", size=38, color=YELLOW), 0)
        self.add(self.frame, self.header)
        self.slot = None
        if slot_type:
            self.slot = Slot(slot_type, height=slot_height)
            self.slot.move_to([CARD_R - 0.25, row_y(0) - 0.36, 0], aligned_edge=UR)
        self.tags = []
        self.shown = [self.header]      # everything on the card that leaves with it

    @property
    def bottom(self):
        """Where the card's bottom edge is once lifted (hints are laid out against this)."""
        return CARD_TOP - self.h

    def lower(self, *items):
        """Call once everything for the card is built: drop it all to the waiting position."""
        for m in (self.frame, self.header, *([self.slot] if self.slot else []), *self.tags, *items):
            m.shift(DOWN * self.drop_y)
        return self

    def lift(self):
        """Animations taking the card and everything shown on it up to the top."""
        return [m.animate.shift(UP * self.drop_y) for m in (self.frame, *self.shown)]

    def tag(self, text, color=BLUE):
        t = Tag(text, color)
        prev = self.tags[-1] if self.tags else self.header
        t.next_to(prev, RIGHT, buff=0.2 if self.tags else 0.45).set_y(row_y(0))
        self.tags.append(t)
        return t

    def keep(self, *mobs):
        self.shown.extend(mobs)
        return mobs[0] if len(mobs) == 1 else mobs


def split_line(src, parts, size=36, k=None, x=COL_X, y=None):
    """Lay out a whole line of code (left edge at x, on card row k or at height y), then
    return each part as its own Code placed exactly where it sits in the line (same glyphs,
    so the same box), to reveal them one by one."""
    full = Code(src, size=size)
    if k is not None:
        at_row(full, k, x)
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
# chapter 3's code, with the clauses unindented so the two fit side by side (same code)
NLENGTH = """let rec nlength = function
| [] -> 0
| x :: xs -> 1 + nlength xs"""
ADDLEN = """let rec addlen n = function
| []    -> n
| x::xs -> addlen (n + 1) xs"""
S = 1.0          # the 3 -> 5 -> 9 -> [] chain of the 3.2 hint (~52% of the frame width)


def flash_along(src, dst, color=YELLOW, run_time=1.0):
    path = Line(src.tail_start(), dst.entry()).set_stroke(color, 8)
    return VShowPassingFlash(path, time_width=0.6, run_time=run_time)


class ExercisesSumLast(NarratedScene):
    def construct(self):
        self.overview()
        self.sum_card()
        self.sum_hint()
        self.last_card()
        self.last_hint()
        hold_for(self, self.pause_born, len("pause and try it"))
        finish(self)

    # ex.1: "Exercises", the five cards, the routine (task, hint, pause), solutions elsewhere
    def overview(self):
        header = T("Exercises", size=52).move_to(UP * 2.85)
        bigs = VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * 0.7)
        s1, s2 = T("the task", size=36), T("one hint", size=36)
        s3 = VGroup(pause_icon(h=0.36), T("pause", size=36)).arrange(RIGHT, buff=0.2)
        a1, a2 = [Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, stroke_width=3, color=DIM,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.16) for _ in range(2)]
        steps = VGroup(s1, a1, s2, a2, s3).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.3)
        note = T("Solutions: bonus chapter", size=36, color=DIM, t2c={"bonus chapter": YELLOW})
        note.move_to(DOWN * 2.75)

        with self.say("c5.ex.1") as c:
            # "Now it's your turn."
            self.play(FadeIn(header, shift=0.3 * DOWN), run_time=1.0)
            # "The notes end with five exercises, ..."  (the five cards, the hero of this line)
            c.wait_until("five exercises")
            self.play(LaggedStart(*[FadeIn(b, shift=0.3 * UP) for b in bigs], lag_ratio=0.15), run_time=2.2)
            # "For each exercise, I'll state it, give you a single hint, and then pause, ..."
            c.wait_until("state")
            self.play(FadeIn(s1, shift=0.25 * DOWN), run_time=fit(c, "single hint", hi=0.9))
            c.wait_until("single hint")
            self.play(GrowArrow(a1), FadeIn(s2, shift=0.25 * DOWN), run_time=fit(c, "then pause", hi=0.9))
            c.wait_until("then pause")
            self.play(GrowArrow(a2), FadeIn(s3, shift=0.25 * DOWN), run_time=0.9)
            # "There are no solutions here. The worked solutions are in a bonus chapter, ..."
            c.wait_until("worked solutions")
            self.play(FadeIn(note, shift=0.25 * UP), run_time=1.0)
        self.bigs, self.ov_header, self.steps, self.note = bigs, header, steps, note

    # ex.2: the cards shrink into the strip; 3.1 grows into the hero card
    def sum_card(self):
        strip = make_strip([TODO] * 5)
        card = HeroCard(0, height=2.72, slot_type="int list -> int")
        task = at_row(T("Add up the elements of an int list.", size=34), 1)
        ex_in, ex_out = split_line("sum [1; 2; 3; 4]  ⇒  10", ["sum [1; 2; 3; 4]", "⇒  10"], k=2)
        tags = [card.tag("recursive"), card.tag("iterative"), card.tag("efficiency?", GOLD)]
        card.lower(task, ex_in, ex_out)
        slot = card.slot

        with self.say("c5.ex.2") as c:
            # "Exercise three point one."  The overview clears; its cards become the strip (P18:
            # keep what the next idea builds on). The note at the bottom stays a little longer.
            anims = [FadeOut(m) for m in (self.ov_header, *self.steps)]
            for b, p in zip(self.bigs, strip):
                anims += [Transform(b.frame, p.frame.copy()), Transform(b.num, p.num.copy()),
                          FadeOut(b.name, scale=0.5)]
            self.play(*anims, run_time=1.1)
            self.remove(*[m for b in self.bigs for m in b.get_family()])
            self.add(strip)
            self.play(*enter_card(strip, card), run_time=1.2)

            # "Write a function that adds up the elements of a list of integers."
            c.wait_until("task")
            self.play(FadeIn(task, shift=0.25 * DOWN), FadeIn(slot.box), FadeIn(slot.q, scale=0.7), run_time=1.1)
            c.wait_until("integers")
            self.play(FadeIn(slot.sig, shift=0.2 * DOWN), run_time=0.8)

            # "The sum of one, two, three, four is ten."
            c.wait_until("the sum of")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), FadeOut(self.note), run_time=1.0)
            c.wait_until("is ten")
            self.play(FadeIn(ex_out, shift=0.25 * LEFT), run_time=0.8)

            # "Write it twice. First recursively, and then iteratively."
            c.wait_until("recursively")
            self.play(FadeIn(tags[0], shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("iteratively")
            self.play(FadeIn(tags[1], shift=0.2 * DOWN), run_time=0.8)
            # "Then comment on how much the iterative version improves the efficiency."
            c.wait_until("how much")
            self.play(FadeIn(tags[2], shift=0.2 * DOWN), run_time=0.8)
        card.keep(task, slot.box, slot.q, slot.sig, ex_in, ex_out, *tags)
        self.strip, self.card = strip, card

    # ex.3: hint: nlength's shape, addlen's running total; compare their space; pause
    def sum_hint(self):
        card = self.card
        hl = hint_label(card, 3)
        nl = Code(NLENGTH, size=28).set_opacity(CODE_DIM)
        al = Code(ADDLEN, size=28).set_opacity(CODE_DIM)
        top = hl.get_bottom()[1] - 0.66
        nl.move_to([-6.6, top, 0], aligned_edge=UL)
        al.move_to([6.6, top, 0], aligned_edge=UR)
        divider = Line(UP * 0.75, DOWN * 0.75, color=DIM, stroke_width=2)
        divider.move_to([(nl.get_right()[0] + al.get_left()[0]) / 2, (nl.get_y() + al.get_y()) / 2, 0])
        lab_y = (hl.get_bottom()[1] + top) / 2 - 0.02
        rec_lab = card.tags[0].copy().move_to([nl.get_x(), lab_y, 0])
        running = T("running total", size=30, color=GOLD)
        it_lab = card.tags[1].copy().move_to([al.get_x() - (running.width + 0.3) / 2, lab_y, 0])
        running.next_to(it_lab, RIGHT, buff=0.3)
        ns = [glyph(al, " n ", line=0), glyph(al, "-> n", line=1, idx=2), glyph(al, "(n", line=2, idx=1)]
        braces, spaces = [], []
        for code in (nl, al):
            b = Brace(code, DOWN, buff=0.06, color=GOLD)
            braces.append(b)
            spaces.append(T("space?", size=32, color=GOLD).next_to(b, DOWN, buff=0.06))
        tag = pause_tag()

        with self.say("c5.ex.3") as c:
            # "Here's the hint."  The card goes up to make room for it.
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # "The recursive version has the same shape as en-length, from chapter three."
            # (the "recursive" tag on the card comes down onto the code it means, P5)
            c.wait_until("same shape")
            self.play(TransformFromCopy(card.tags[0], rec_lab), FadeIn(nl, shift=0.25 * UP), run_time=1.5)
            # "The iterative version carries a running total, the way add-len carried a count."
            c.wait_until("addlen")
            self.play(TransformFromCopy(card.tags[1], it_lab), FadeIn(al, shift=0.25 * UP), Create(divider),
                      run_time=1.5)
            c.wait_until("running total")
            self.play(*[FlashAround(g, color=GOLD, buff=0.06) for g in ns],
                      *[g.animate.set_fill(GOLD, opacity=1) for g in ns],
                      FadeIn(running, shift=0.2 * LEFT), run_time=1.3)
            # "So when you compare them, think about space."
            c.wait_until("think about space")
            self.play(GrowFromCenter(braces[0]), FadeIn(spaces[0], shift=0.2 * DOWN),
                      GrowFromCenter(braces[1]), FadeIn(spaces[1], shift=0.2 * DOWN), run_time=1.2)
            # "Pause the video, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time
        self.hint = [hl, nl, al, divider, rec_lab, it_lab, running, *braces, *spaces]
        self.tag = tag

    # ex.4: 3.1 shrinks back into its pill; 3.2 grows
    def last_card(self):
        strip = self.strip
        card = HeroCard(1, height=2.72, slot_type="'a list -> 'a")
        task = at_row(T("Return the last element of a list.", size=34), 1)
        ex_in, ex_out = split_line("last [3; 5; 9]  ⇒  9", ["last [3; 5; 9]", "⇒  9"], k=2)
        t1, t2 = card.tag("non-empty lists only"), card.tag("how efficiently?", GOLD)
        card.lower(task, ex_in, ex_out)
        slot = card.slot

        with self.say("c5.ex.4") as c:
            # "Exercise three point two."
            self.play(*exit_card(strip, self.card, self.hint), run_time=1.1)
            self.remove(self.card.frame)
            self.play(*enter_card(strip, card), run_time=1.2)
            # "Write a function that returns the last element of a list."
            c.wait_until("task")
            self.play(FadeIn(task, shift=0.25 * DOWN), FadeIn(slot.box), FadeIn(slot.q, scale=0.7),
                      FadeOut(self.tag), run_time=1.1)
            c.wait_until("of a list")
            self.play(FadeIn(slot.sig, shift=0.2 * DOWN), run_time=0.8)
            # "The last element of three, five, nine is nine."
            c.wait_until("nine")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), run_time=fit(c, "is nine", hi=1.0))
            c.wait_until("is nine")
            self.play(FadeIn(ex_out, shift=0.25 * LEFT), run_time=0.8)
            # "You can assume the list has at least one element."
            c.wait_until("nonempty")
            self.play(FadeIn(t1, shift=0.2 * DOWN), run_time=0.9)
            # "And the real question is, how efficiently can this be done?"
            c.wait_until("how efficiently")
            self.play(FadeIn(t2, shift=0.2 * DOWN), run_time=0.9)
        card.keep(task, slot.box, slot.q, slot.sig, ex_in, ex_out, t1, t2)
        self.card = card

    # ex.5: hint from chapter 1: walk the arrows to the cell that points at nil
    def last_hint(self):
        card = self.card
        hl = hint_label(card, 1)
        chain = ConsChain([3, 5, 9]).scale(S).move_to(DOWN * 2.05)
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil

        def above(m, buff=0.25):
            return m.get_top() + UP * buff

        arc = ArcBetweenPoints(above(cells[0].box), above(nil), angle=-PI / 3.2)
        jump = DashedVMobject(arc, num_dashes=22).set_stroke(DIM, 3)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(RED, 7).scale(0.2)
        cross.move_to(arc.point_from_proportion(0.5))
        marker = SurroundingRectangle(cells[0], color=YELLOW, buff=0.12, stroke_width=5)
        q = T("?", size=72, color=GOLD).next_to(cells[2].box, UP, buff=0.22)
        others = [*cells[1:], *arrows, nil]
        tag = pause_tag()

        with self.say("c5.ex.5") as c:
            # "The hint comes from chapter one."  The card goes up; chapter 1's chain comes back.
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4),
                      time_span(FadeIn(chain, shift=0.3 * UP), 0.6, 1.6), run_time=1.6)
            # "There's no shortcut to the end of a list."
            c.wait_until("no shortcut")
            self.play(Create(jump), time_span(FadeIn(cross, scale=1.4), 0.8, 1.2), run_time=1.2)
            # "You have to follow the arrows, cell by cell."  (a cursor walks; the rest fade, P9)
            c.wait_until("you have to")
            self.play(FadeOut(jump), FadeOut(cross), Create(marker),
                      *[m.animate.set_opacity(0.25) for m in others], run_time=fit(c, "the arrows", hi=0.9))
            for i, cue in ((1, "the arrows"), (2, "cell by cell")):
                c.wait_until(cue)
                self.play(cells[i - 1].animate.set_opacity(0.25), arrows[i - 1].animate.set_opacity(1),
                          cells[i].animate.set_opacity(1), marker.animate.move_to(cells[i]), run_time=0.8)
            # "So ask yourself this. Which pattern tells you that you've reached the last cell?"
            c.wait_until("which pattern")
            self.play(FadeIn(q, shift=0.25 * DOWN), FlashAround(cells[2], color=GOLD, time_width=1.5),
                      run_time=1.2)
            c.wait_until("last cell")
            self.play(arrows[2].animate.set_opacity(1).set_color(TEAL), nil.animate.set_opacity(1),
                      flash_along(cells[2], nil, color=TEAL), run_time=1.0)
            # "Pause, and give it a go."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time
