"""Chapter 6, scene 7: the recap of the five solutions, and the lecture's end card. Clip c6.recap.1
(the chapter's and the lecture's last scene).

A table, one row per exercise, walked on the narration: the five exercise pills (the ch5 card kit,
read-only import) stand down the left from "Let's recap" (TODO); each row lights its pill (CURRENT)
while the row before steps back to 0.5 and its pill turns DONE. Columns: function name in YELLOW,
GOLD "time" and "space" costs under DIM headers, a short note on the right.
  3.1 `sum` O(n) O(n), the space cost rewriting to O(1) on "to big O of one", GREEN check "accumulator"
      (not `nsum` -> `sum`: the n would be up only ~2 s before it drops; the voice says "sum")
  3.2 `last` O(n) O(1) "already iterative"; the time cost flashes on "the walk to the end"
  3.3 `evens` O(n) O(n) "three clauses", RED cross "accumulator"
  3.4 `id   : 'a -> 'a` "returns its argument" / `loop : 'a -> 'b` "never returns" ('a 'b PINK)
  3.5 `tails` O(n) O(n) "every tail is shared" ("shared" TEAL)
{end}: every row back to 1, the pills all DONE with a GREEN ripple; "Next lecture: More on Lists"
(Lecture 4 in COURSE.md); the finished card holds 8 s under the music, then fades.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import CURRENT, DONE, TODO, Pill, fit, restyled  # noqa: E402  the exercise-card kit

# ── layout ──────────────────────────────────────────────────────────────────────
TITLE_Y, HEAD_Y, NEXT_Y = 3.25, 2.45, -3.25
R1, R2, R3, R4A, R4B, R5 = 1.65, 0.85, 0.05, -0.75, -1.45, -2.25     # row centres
PILL_Y = (R1, R2, R3, (R4A + R4B) / 2, R5)
X_PILL, X_NAME, X_TIME, X_SPACE, X_NOTE = -6.1, -5.15, -2.6, -1.05, 0.1
BASE = 0.14                      # a row's baseline sits this far below the row's centre
NAME_SIZE, COST_SIZE, NOTE_SIZE = 38, 44, 34
DIM_ROW = 0.5                    # a row that has been said steps back to this
END_CARD = 8.0                   # the finished card holds under the music swell


def seat(mob, glyph, y):
    """Shift mob so `glyph` (a letter that sits on the baseline) sits on row y's baseline."""
    return mob.shift(UP * (y - BASE - glyph.get_bottom()[1]))


def name(src, y):
    m = Mono(src, size=NAME_SIZE, color=YELLOW)
    m.shift(RIGHT * (X_NAME - m.get_left()[0]))
    return seat(m, m[0], y)


def cost(tex, x, y):
    m = MathTex(tex, font_size=COST_SIZE, color=GOLD).move_to([x, 0, 0])
    return seat(m, m[0][0], y)            # the "O" on the baseline


def note(text, y, x=X_NOTE, **kw):
    m = T(text, size=NOTE_SIZE, **kw)
    m.shift(RIGHT * (x - m.get_left()[0]))
    return seat(m, m[0], y)


def mark_note(mark, text, y):
    """A check or cross mark, then a note, on row y."""
    mark.move_to([X_NOTE + mark.width / 2, y - BASE + 0.15, 0])
    return mark, note(text, y, x=mark.get_right()[0] + 0.22)


def typed(src, y):
    """`name : type` in Code, the name YELLOW and the type variables PINK."""
    code = Code(src, size=NAME_SIZE)
    nm = src.split()[0]
    code._span(0, len(nm)).set_color(YELLOW)
    for m in re.finditer(r"'[ab]", src):
        code._span(m.start(), m.end()).set_color(PINK)
    code.shift(RIGHT * (X_NAME - code.get_left()[0]))
    return seat(code, code.find(nm)[0], y)


class Recap(NarratedScene):
    def construct(self):
        title = T("Recap", size=48).move_to([0, TITLE_Y, 0])
        pills = [Pill(i, TODO).move_to([X_PILL, y, 0]) for i, y in enumerate(PILL_Y)]
        heads = [T(w, size=30, color=DIM).move_to([x, 0, 0]) for w, x in (("time", X_TIME), ("space", X_SPACE))]
        for h in heads:
            seat(h, h[0], HEAD_Y)

        # 3.1: sum O(n), space O(n) -> O(1)
        sum_ = name("sum", R1)
        t1, s1n, s1 = cost("O(n)", X_TIME, R1), cost("O(n)", X_SPACE, R1), cost("O(1)", X_SPACE, R1)
        chk, acc1 = mark_note(check_mark(GREEN), "accumulator", R1)
        # 3.2: last O(n) O(1)
        last, t2, s2 = name("last", R2), cost("O(n)", X_TIME, R2), cost("O(1)", X_SPACE, R2)
        iter2 = note("already iterative", R2)
        # 3.3: evens O(n) O(n)
        evens, t3, s3 = name("evens", R3), cost("O(n)", X_TIME, R3), cost("O(n)", X_SPACE, R3)
        three = note("three clauses", R3)
        crs = cross_mark(RED, r=0.16).move_to([three.get_right()[0] + 0.55, R3 - BASE + 0.15, 0])
        acc3 = note("accumulator", R3, x=crs.get_right()[0] + 0.22)
        # 3.4: the two strange types, colons aligned
        ida, loopb = typed("id   : 'a -> 'a", R4A), typed("loop : 'a -> 'b", R4B)
        ida.shift(RIGHT * (loopb.find(":")[0].get_x() - ida.find(":")[0].get_x()))
        arg4, never4 = note("returns its argument", R4A), note("never returns", R4B)
        # 3.5: tails O(n) O(n), every tail shared
        tails, t5, s5 = name("tails", R5), cost("O(n)", X_TIME, R5), cost("O(n)", X_SPACE, R5)
        shared = note("every tail is shared", R5, t2c={"shared": TEAL})

        nxt = VGroup(T("Next lecture:", size=40, color=DIM), T("More on Lists", size=40, color=YELLOW))
        nxt.arrange(RIGHT, buff=0.25)
        nxt[1].align_to(nxt[0], DOWN)
        nxt.move_to([0, NEXT_Y, 0])

        def enter(*mobs, lag=0.2):
            return LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in mobs], lag_ratio=lag)

        def step(k, prev_row):
            """Row k's pill lights up; the row before steps back and its pill is done."""
            return [restyled(pills[k - 1], DONE), restyled(pills[k], CURRENT), *set_alpha(prev_row, DIM_ROW)]

        with self.say("c6.recap.1") as c:
            # {recap} "Let's recap."  The title drops in; the five exercises stand down the left.
            self.play(FadeIn(title, shift=0.3 * DOWN),
                      LaggedStart(*[FadeIn(p, shift=0.2 * RIGHT) for p in pills], lag_ratio=0.15),
                      run_time=min(1.4, 0.95 * c.until("r1")))

            # {r1} "For sum, an accumulator cut the space from big O of en to big O of one."
            c.wait_until("r1")
            self.play(restyled(pills[0], CURRENT), *[FadeIn(h) for h in heads], enter(sum_, t1, s1n),
                      run_time=1.2)
            c.wait_until("an accumulator")
            self.play(FadeIn(chk, scale=0.6), FadeIn(acc1, shift=0.2 * LEFT),
                      run_time=fit(c, "to big O of one", frac=0.6, hi=1.0))
            c.wait_until("to big O of one")
            self.play(ReplacementTransform(s1n, s1),
                      time_span(FlashAround(s1, color=GOLD, time_width=1.5), 0.4, 1.5), run_time=1.5)
            row1 = [sum_, t1, s1, chk, acc1]

            # {r2} "Last is already iterative, but it can't avoid the walk to the end."
            c.wait_until("r2")
            self.play(*step(1, row1), enter(last, t2, s2, iter2), run_time=1.5)
            c.wait_until("the walk")
            self.play(FlashAround(t2, color=GOLD, time_width=1.5), run_time=min(1.4, c.until("r3") - 0.1))
            row2 = [last, t2, s2, iter2]

            # {r3} "The even positions need three clauses, and an accumulator wouldn't help."
            c.wait_until("r3")
            self.play(*step(2, row2), enter(evens, t3, s3), run_time=fit(c, "three clauses", frac=0.8, hi=1.3))
            c.wait_until("three clauses")
            self.play(FadeIn(three, shift=0.2 * LEFT), run_time=fit(c, "and an accumulator", hi=1.0))
            c.wait_until("and an accumulator")
            self.play(FadeIn(crs, scale=0.6), FadeIn(acc3, shift=0.2 * LEFT),
                      run_time=fit(c, "r4", frac=0.8, hi=1.0))
            row3 = [evens, t3, s3, three, crs, acc3]

            # {r4} "Alpha to alpha forces a function to return its argument, and alpha to beta is
            # safe because loop never returns."
            c.wait_until("r4")
            self.play(*step(3, row3), FadeIn(ida, shift=0.2 * UP),
                      run_time=fit(c, "return its argument", frac=0.75, hi=1.3))
            c.wait_until("return its argument")
            self.play(FadeIn(arg4, shift=0.2 * LEFT), run_time=fit(c, "alpha to beta", hi=1.0))
            c.wait_until("alpha to beta")
            self.play(FadeIn(loopb, shift=0.2 * UP), run_time=fit(c, "never returns", frac=0.75, hi=1.2))
            c.wait_until("never returns")
            self.play(FadeIn(never4, shift=0.2 * LEFT), run_time=fit(c, "r5", frac=0.8, hi=1.0))
            row4 = [ida, arg4, loopb, never4]

            # {r5} "And tails is only big O of en, because every tail is shared."
            c.wait_until("r5")
            self.play(*step(4, row4), enter(tails, t5, s5), run_time=fit(c, "every tail", frac=0.8, hi=1.3))
            c.wait_until("every tail")
            self.play(FadeIn(shared, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("shared")
            self.play(FlashAround(select(shared, "shared")[0], color=TEAL, time_width=1.5), run_time=1.2)
            
            # {end} "Well done."  Every row comes back; the five exercises are all done.
            c.wait_until("well done")
            self.play(*set_alpha(row1 + row2 + row3 + row4, 1), restyled(pills[4], DONE),
                      LaggedStart(*[FlashAround(p, color=GREEN, time_width=1.5) for p in pills], lag_ratio=0.15),
                      run_time=min(1.5, 0.95 * c.until("see you")))

            # "See you in the next lecture."
            c.wait_until("see you")
            self.play(FadeIn(nxt, shift=0.25 * UP), run_time=1.0)

        # End card: the finished recap and the next lecture hold under the music, then fade.
        self.wait(END_CARD)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.3)
        self.wait(0.15)   # the last play() never renders its final (empty) frame
