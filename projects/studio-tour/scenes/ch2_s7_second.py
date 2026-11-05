"""Chapter 2, scene 7: A second opinion (Gemini's review board). Clips c2.second.1 – c2.second.5.

Reusable for s8's recap: review_card(text, state, width, size) and verdict(card, state),
board_title(). Card = RoundedRectangle (stroke 3, fill 0.12 of its colour) + T label.
States: neutral FG outline, green GREEN, red RED, dim DIM (label DIM too).
"""
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

STATE_COLOR = {"neutral": FG, "green": GREEN, "red": RED, "dim": DIM}


def review_card(text, state="neutral", width=10.0, size=30, height=None):
    """A review-board card: rounded box + label; .box and .label are its parts."""
    col = STATE_COLOR[state]
    label = T(text, size, DIM if state == "dim" else FG)
    h = height or max(0.8, label.height + 0.4)
    box = RoundedRectangle(corner_radius=0.15, width=width, height=h)
    box.set_stroke(col, 3).set_fill(col, 0.12 if state != "neutral" else 0.0)
    label.move_to(box)
    card = VGroup(box, label)
    card.box, card.label = box, label
    return card


def verdict(card, state):
    """Animations that turn a card to a verdict colour (stroke + faint fill)."""
    col = STATE_COLOR[state]
    anims = [card.box.animate.set_stroke(col, 3).set_fill(col, 0.12)]
    if state == "dim":
        anims.append(card.label.animate.set_color(DIM))
    return anims


def board_title():
    t = T("Gemini's review", 48).move_to(UP * 3.3)
    s = T("each claim checked against the code and transcripts", 28, DIM).move_to(UP * 2.65)
    return t, s


def tag(text, color=DIM, size=28):
    return T(text, size, color)


LX, RX = -3.5, 3.5
ROWS = [1.7, 0.5, -0.7, -1.9]
BAND_Y = -3.05


def slot(col, row):
    return [LX if col == 0 else RX, ROWS[row], 0]


def small_card(text, state, col, row):
    return review_card(text, state, width=6.4, size=28, height=1.05).move_to(slot(col, row))


def swap_reason(old, new):
    """Old reason fades out, then the new one rises in: no glyph morph between unlike texts."""
    return [time_span(FadeOut(old), 0, 0.5), time_span(FadeIn(new, shift=0.3 * UP), 0.5, 1.2)]


def card_to_item(card, item):
    """The adopted card shrinks into the item's number, then the item fades in: never overlapping."""
    return [time_span(FadeOut(card, target_position=item[0].get_center(), scale=0.15), 0, 0.7),
            time_span(FadeIn(item, shift=0.3 * RIGHT), 0.7, 1.5)]


class SecondOpinion(NarratedScene):
    def construct(self):
        title, sub = board_title()

        # ---- 1: the board
        with self.say("c2.second.1") as c:
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("checked")
            cards = VGroup(*[review_card("idea", width=3.6, height=1.2) for _ in range(3)])
            cards.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.3)
            self.play(FadeIn(sub, shift=0.3 * DOWN),
                      LaggedStart(*[FadeIn(k, shift=0.3 * UP) for k in cards], lag_ratio=0.25),
                      run_time=1.8)
            c.wait_until("board")
            g = tag("held up", GREEN, 32).next_to(cards[0], DOWN, buff=0.3)
            r = tag("failed", RED, 32).next_to(cards[2], DOWN, buff=0.3)
            self.play(*verdict(cards[0], "green"), *verdict(cards[2], "red"), run_time=1.2)
            self.play(FadeIn(g, shift=0.3 * DOWN), FadeIn(r, shift=0.3 * DOWN), run_time=1.0)

        # ---- 2: skip / voice / lived
        with self.say("c2.second.2") as c:
            skip = small_card("skip the render + beats image\nwhile the lint has flags", "neutral", 0, 0)
            self.play(FadeIn(skip, shift=0.3 * UP), run_time=1.0)
            c.wait_until("true since the check")
            self.play(*verdict(skip, "green"), run_time=1.0)
            c.wait_until("small")
            t1 = tag("≈ 1–2 image reads a build\n3–5% · cheap", GOLD).move_to(slot(1, 0))
            self.play(FadeOut(cards), FadeOut(g), FadeOut(r), FadeIn(t1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("voice")
            voice = small_card("several-model voice check\ninside vk voice", "neutral", 0, 1)
            self.play(FadeIn(voice, shift=0.3 * UP), run_time=1.0)
            c.wait_until("true and its best idea")
            star = Star(n=5, outer_radius=0.24, color=YELLOW, fill_opacity=1)
            t2 = tag("best idea: quality", YELLOW)
            st = VGroup(star, t2).arrange(RIGHT, buff=0.2).move_to(slot(1, 1))
            self.play(*verdict(voice, "green"), FadeIn(st, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("lived")
            page = VGroup(Rectangle(width=2.8, height=1.3).set_stroke(TEAL, 3).set_fill(TEAL, 0.12),
                          T("LESSONS.md", 30, TEAL))
            page[1].move_to(page[0])
            page.move_to([RX, -0.8, 0])
            stamp = VGroup(Rectangle(width=4.2, height=0.8).set_stroke(DIM, 3),
                           T("directors: don't read", 30, DIM))
            stamp[1].move_to(stamp[0])
            stamp.rotate(-0.1).move_to([RX, -2.3, 0])
            self.play(FadeIn(page, shift=0.3 * UP), run_time=1.0)
            c.wait_until("that directors are told")
            self.play(FadeIn(stamp, scale=1.4), run_time=0.8)

        # ---- 3: holds
        with self.say("c2.second.3") as c:
            hc = small_card("vk holds: summed audio durations,\nsampled before each clip's end", "neutral", 0, 2)
            self.play(FadeOut(t1), FadeOut(st), FadeOut(page), FadeOut(stamp),
                      FadeIn(hc, shift=0.3 * UP), run_time=1.2)
            tiles = VGroup(*[VGroup(Square(0.78).set_stroke(BLUE, 3).set_fill(BLUE, 0.12), T(str(i + 1), 30))
                             for i in range(6)])
            for i, t in enumerate(tiles):
                t[0].move_to([1.0 + i * 1.0, 0.9, 0])
                t[1].move_to(t[0])
            self.play(LaggedStart(*[FadeIn(t, shift=0.3 * UP) for t in tiles], lag_ratio=0.15), run_time=1.5)
            c.wait_until("worse")
            self.play(*verdict(hc, "green"), run_time=0.8)
            w = tag("worse than stated", RED, 32).move_to([RX, 1.9, 0])
            self.play(FadeIn(w, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("any animation outside")
            gap_x = (tiles[2][0].get_right()[0] + tiles[3][0].get_left()[0]) / 2 + 0.175
            ln = Line([gap_x, 0.25, 0], [gap_x, -0.35, 0]).set_stroke(RED, 5)
            mt = T("animation outside a say block", 28, RED).move_to([RX, -0.65, 0])
            self.play(FadeIn(ln, shift=0.3 * UP), FadeIn(mt, shift=0.3 * UP), run_time=0.9)
            self.play(*[t[0].animate.shift(RIGHT * 0.35).set_stroke(RED, 3) for t in tiles[3:]],
                      *[t[1].animate.shift(RIGHT * 0.35) for t in tiles[3:]], run_time=1.3)

        # ---- 4: rejected
        with self.say("c2.second.4") as c:
            specs = [("pre-made skeletons + a shared\nhelper file per chapter",
                      "≈ 1k tokens of boilerplate · breaks: builders never share files"),
                     ("many small Edit calls", "median 0 · real waste: ≈ 9 lookups"),
                     ("a 12–15 turn cap", "arbitrary · turns aren't the main cost")]
            rc = [small_card(a, "neutral", 1, i) for i, (a, _) in enumerate(specs)]
            self.play(*[FadeOut(m) for m in (tiles, w, ln, mt)],
                      LaggedStart(*[FadeIn(k, shift=0.3 * UP) for k in rc], lag_ratio=0.25), run_time=1.5)
            c.wait_until("skeleton")
            self.play(*verdict(rc[0], "red"), run_time=0.8)
            c.wait_until("builders already write")
            r0 = tag(specs[0][1], FG).move_to([0, BAND_Y, 0])
            self.play(FadeIn(r0, shift=0.3 * UP), run_time=1.0)
            c.wait_until("edits")
            c.wait_until("wrong the median")
            r1 = tag(specs[1][1], FG).move_to([0, BAND_Y, 0])
            self.play(*verdict(rc[1], "red"), *swap_reason(r0, r1), run_time=1.2)
            c.wait_until("cap")
            r2 = tag(specs[2][1], FG).move_to([0, BAND_Y, 0])
            self.play(*verdict(rc[2], "red"), run_time=0.8)
            c.wait_until("arbitrary")
            self.play(*swap_reason(r1, r2), run_time=1.2)

        # ---- 5: agreed, missed, changes
        with self.say("c2.second.5") as c:
            ag = small_card("Sonnet for fix passes: agreed", "green", 0, 3)
            self.play(FadeIn(ag, shift=0.3 * UP), run_time=1.0)
            c.wait_until("missed")
            ms = small_card("effort level", "dim", 1, 3)
            stamp = VGroup(Rectangle(width=1.9, height=0.6).set_stroke(RED, 3).set_fill(BG, 0.9), T("missed", 28, RED))
            stamp[1].move_to(stamp[0])
            stamp.rotate(0.1).move_to(ms.get_right() + LEFT * 0.95)
            self.play(FadeIn(ms, shift=0.3 * UP), run_time=1.0)
            self.play(FadeIn(stamp, scale=1.4), run_time=0.8)
            c.wait_until("changes")
            headt = T("Changes made 2026-10-27", 44).move_to(UP * 3.3)
            self.play(FadeOut(sub), FadeOut(r2), ReplacementTransform(title, headt), run_time=1.2)
            c.wait_until("you saw them in part one")
            self.play(*[FadeOut(m) for m in rc + [ag, ms, stamp]],
                      voice.animate.move_to([LX, 2.15, 0]),
                      hc.animate.move_to([LX, 1.1, 0]),
                      skip.animate.move_to([LX, 0.05, 0]), run_time=1.5)

            def item(n, text, y):
                body = T(text, 30)
                body.move_to([-5.6, y, 0], aligned_edge=LEFT)
                num = T(str(n), 32, GREEN).next_to(body, LEFT, buff=0.3)
                return VGroup(num, body)

            i1 = item(1, "vk voice: several Whisper models must agree;\nflagged sentences kept with what was heard, and listed", 2.15)
            i2 = item(2, "vk holds: each frame from the render's real timings", 1.1)
            i3 = item(3, "builder prompt: the library's complete signatures ·\nvk check: no render while overrun, sync or layout flags remain", 0.05)
            c.wait_until("c1")
            self.play(*card_to_item(voice, i1), run_time=1.5)
            c.wait_until("c2")
            self.play(*card_to_item(hc, i2), run_time=1.5)
            c.wait_until("c3")
            self.play(*card_to_item(skip, i3), run_time=1.5)
            c.wait_until("plus a check that skips")
            ta = Mono("  overrun: <clip>: the block runs <n> s past its clip\n"
                      "    (the next clip starts late: shorten run_times\n"
                      "     or cue earlier)", 28, FG, t2c={"<clip>": DIM, "<n>": DIM, "overrun:": RED})
            tb = Mono("  render and beats image skipped until the audit is\n"
                      "    clean (--render-anyway to render with these flags)", 28, FG)
            ov = VGroup(ta, tb).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            ov.move_to([0, -2.0, 0]).align_to([-6.4, 0, 0], LEFT)
            self.play(FadeIn(ov, shift=0.3 * UP), run_time=1.2)
        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
