"""Chapter 1, scene 1: hook (title, Lecture 4 recap, the running chain sorted, comparisons, the
chapter question). Clips c1.hook.1 – c1.hook.3.

Look set here for the lecture: the running chain ConsChain([3, 5, 9, 4, 7]) at ORIGIN (library
defaults); the "done" picture ConsChain([3, 4, 5, 7, 9]) at ORIGIN with check_mark(GREEN) scaled
0.8, next_to(chain, RIGHT, buff=0.22).
End shot (scene 2 opens from it): two YELLOW T(size 44) lines, centred on x = 0:
  "How many comparisons does sorting need?"  at y = +0.45
  "Could a cleverer method need fewer?"      at y = -0.40
"""
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
from lib.titles import title_card  # noqa: E402

RUNNING = [3, 5, 9, 4, 7]
SORTED = [3, 4, 5, 7, 9]

# Lecture 4 thumbnails
THUMB_W, THUMB_H = 4.1, 1.6
THUMB_XS = (-4.4, 0.0, 4.4)
THUMB_Y = 0.0
HEADER_Y = 1.4
INNER_W = 3.6
THUMB_DIM = 0.45             # thumbnails sit at this opacity until one is lifted
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
BOX = 0.75                   # L4's primes row (ch2_s3_faster)
HERO_W = 10.0                # the lifted primes row
HERO_Y = 0.4
CAPTION_Y = -1.25

TICK_SCALE, TICK_BUFF = 0.8, 0.22
ARC_SAG = 0.8                # comparison arcs dip this far below the boxes
Q_SIZE = 44
Q1_Y, Q2_Y = 2.45, 1.6       # question lines over the chain
END_Q1_Y, END_Q2_Y = 0.45, -0.4


def dim_static(mob, k):
    """Multiply every part's fill and stroke opacity by k (no animation)."""
    for m in mob.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * k, family=False)
        m.set_stroke(opacity=m.get_stroke_opacity() * k, family=False)
    return mob


def frame_at(x):
    return RoundedRectangle(corner_radius=0.18, width=THUMB_W, height=THUMB_H) \
        .set_stroke(DIM, 2).move_to(RIGHT * x + UP * THUMB_Y)


def coin(v, r=0.42):
    """L4's coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    return VGroup(disc, T(str(v), size=34, color=GOLD).move_to(disc))


def primes_shot():
    """L4's 16 sorted primes; the discarded left half faded, a GOLD brace on the kept half."""
    row = VGroup()
    for p in PRIMES:
        sq = Square(BOX, stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=1)
        row.add(VGroup(sq, T(str(p), 34, GOLD).move_to(sq)))
    row.arrange(RIGHT, buff=0)
    for box in row[:8]:
        dim_static(box, 0.35)
    brace = Brace(VGroup(*row[8:]), DOWN, buff=0.12, color=GOLD)
    cost = MathTex(r"O(\log n)", font_size=48, color=GOLD).next_to(brace, DOWN, buff=0.12)
    return VGroup(row, brace, cost)


def light(cell, on=True):
    return [cell.box.animate.set_stroke(YELLOW if on else BLUE),
            cell.label.animate.set_color(YELLOW if on else FG)]


def compare_marks(a_cell, b_cell):
    """YELLOW arc under two boxes (dipping ARC_SAG) and its '≤ ?' at the bottom."""
    p = a_cell.box.get_bottom() + DOWN * 0.12
    q = b_cell.box.get_bottom() + DOWN * 0.12
    chord = q[0] - p[0]
    arc = ArcBetweenPoints(p, q, angle=4 * np.arctan(2 * ARC_SAG / chord)).set_stroke(YELLOW, 4)
    low = np.array([(p[0] + q[0]) / 2, p[1] - ARC_SAG, 0])
    ask = MathTex(r"\le\ ?", font_size=48, color=YELLOW).next_to(low, DOWN, buff=0.14)
    return arc, ask


class Hook(NarratedScene):
    def construct(self):
        self.clip_title()
        self.clip_sort()
        self.clip_question()

    # ── c1.hook.1: title card, Lecture 4 thumbnails, the promise ─────────────────────────
    def clip_title(self):
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · How fast can we sort?")
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.2)
            c.wait_until("lecture five")
            self.play(FadeIn(card.course, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("Computer Science")
            self.play(FadeIn(card.part, shift=0.2 * DOWN), run_time=1.0)

            # Lecture 4 in three thumbnails
            header = T("Lecture 4", 36, DIM).move_to(UP * HEADER_Y)
            frames = [frame_at(x) for x in THUMB_XS]
            search = ConsChain(RUNNING)
            search.scale(INNER_W / search.width).move_to(frames[0]).shift(DOWN * 0.1)
            coins = VGroup(*[coin(v) for v in [50, 20, 10, 5, 2]]).arrange(RIGHT, buff=0.28)
            coins.scale(INNER_W / coins.width).move_to(frames[1])
            self.hero = primes_shot()
            primes = self.hero.copy()
            primes.scale(INNER_W / primes.width).move_to(frames[2])
            self.hero.scale(HERO_W / self.hero.width).move_to(UP * HERO_Y)
            for t in (search, coins, primes):
                dim_static(t, THUMB_DIM)
            thumbs = [search, coins, primes]

            c.wait_until("we built")
            sweep_clear(self,
                        time_span(FadeIn(header, shift=0.2 * DOWN), 0.5, 1.4),
                        time_span(LaggedStart(*[a for f, t in zip(frames, thumbs)
                                                for a in (FadeIn(f), FadeIn(t, shift=0.2 * DOWN))],
                                              lag_ratio=0.18), 0.6, 2.4),
                        run_time=2.4)

            # search, one cell at a time: a GOLD pointer steps along the little chain
            c.wait_until("searched them")
            pointer = marker(GOLD, scale=0.17).move_to(above(search.cells[0].box, buff=0.08))
            self.play(FadeIn(pointer, shift=0.15 * DOWN), run_time=0.6)
            c.wait_until("one cell at a time")
            for i in (1, 2, 3):
                self.play(pointer.animate.move_to(above(search.cells[i].box, buff=0.08)),
                          run_time=0.55 if i == 1 else 0.4)
                self.wait(0.15)

            # making change
            c.wait_until("made change")
            self.play(FlashAround(frames[1], color=GOLD, time_width=1.5),
                      run_time=min(1.5, c.until("promise", floor=0.8)))

            # the promise: the primes row lifts out of the row, big, with its caption
            caption = T("sorted data can be searched fast", 40, YELLOW).move_to(UP * CAPTION_Y)
            c.wait_until("promise")
            self.play(*[time_span(FadeOut(m), 0.0, 0.8)
                        for m in (header, frames[0], search, pointer, frames[1], coins, frames[2])],
                      time_span(ReplacementTransform(primes, self.hero), 0.2, 1.7),
                      time_span(FadeIn(caption, shift=0.3 * DOWN), 1.1, 2.0),
                      run_time=2.0)

    # ── rearranging a chain: cells slide (arcing), arrows redrawn ────────────────────────
    def rearrange(self, src, dst, extra=(), run_time=3.0):
        """Fade src's arrows, slide each cell to the cell of dst holding the same value, grow
        dst's arrows; then swap in dst as one clean object. extra: anims run over [0, 0.6]."""
        spots = {cell.value: cell.get_center() for cell in dst.cells}
        move_end = run_time - 0.6
        moves = [time_span(cell.animate(path_arc=-PI / 2).move_to(spots[cell.value]), 0.3, move_end)
                 for cell in src.cells if not np.allclose(cell.get_center(), spots[cell.value])]
        fades = [time_span(FadeOut(a), 0.0, 0.5) for a in src.arrows]
        grows = [time_span(GrowArrow(a), move_end - 0.1 + 0.1 * i, move_end + 0.2 + 0.1 * i)
                 for i, a in enumerate(dst.arrows)]
        self.play(*fades, *moves, *grows, *[time_span(e, 0.0, 0.6) for e in extra],
                  run_time=run_time)
        self.remove(*src.get_family(), *dst.arrows)
        self.add(dst)

    # ── c1.hook.2: the running chain, sorted, then compared two at a time ───────────────
    def clip_sort(self):
        with self.say("c1.hook.2") as c:
            chain = ConsChain(RUNNING)
            parts = [m for i, cell in enumerate(chain.cells) for m in (cell, chain.arrows[i])]
            parts.append(chain.nil)
            c.wait_until("running list")
            sweep_clear(self, time_span(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN) for m in parts],
                                                    lag_ratio=0.15), 0.4, 2.2),
                        run_time=2.2)
            settle(self, chain)

            # sorting = rearranging into increasing order
            c.wait_until("sort")
            done = ConsChain(SORTED)
            self.rearrange(chain, done, run_time=min(3.0, max(2.0, 0.9 * c.until("three", nth=1))))
            tick = check_mark(GREEN).scale(TICK_SCALE).next_to(done, RIGHT, buff=TICK_BUFF)
            c.wait_until("three", nth=1)
            self.play(Create(tick), run_time=0.9)

            # back to the unsorted chain
            c.wait_until("compare")
            chain = ConsChain(RUNNING)
            self.rearrange(done, chain, extra=[FadeOut(tick)], run_time=1.8)
            self.chain = chain
            cells = chain.cells

            # comparing two items at a time: 9 vs 4, 5 vs 4, 3 vs 4
            base = [(1.0, 0.25, 0.45, 0.6), (0.75, 0.15, 0.4, 0.5), (0.7, 0.15, 0.4, 0.0)]
            k = min(1.0, (c.until(None, floor=0.1) - 0.1) / sum(sum(b) for b in base))
            arc = ask = ans = None
            prev = None
            for (i, says_yes), (t_move, t_hold, t_ans, t_after) in zip(
                    [(2, False), (1, False), (0, True)], base):
                new_arc, new_ask = compare_marks(cells[i], cells[3])
                if arc is None:
                    self.play(*light(cells[i]), *light(cells[3]), Create(new_arc),
                              FadeIn(new_ask, shift=0.2 * DOWN), run_time=k * t_move)
                    arc, ask = new_arc, new_ask
                else:
                    self.play(*light(cells[prev], False), *light(cells[i]),
                              Transform(arc, new_arc), ask.animate.move_to(new_ask),
                              FadeOut(ans), run_time=k * t_move)
                self.wait(k * t_hold)
                ans = (T("yes", 36, GREEN) if says_yes else T("no", 36, RED)) \
                    .next_to(ask, DOWN, buff=0.2)
                self.play(FadeIn(ans, shift=0.2 * DOWN), run_time=k * t_ans)
                if t_after:
                    self.wait(k * t_after)
                prev = i
            self.marks = (arc, ask, ans)

    # ── c1.hook.3: the chapter question ──────────────────────────────────────────────────
    def clip_question(self):
        with self.say("c1.hook.3") as c:
            cells = self.chain.cells
            q1 = T("How many comparisons does sorting need?", Q_SIZE, YELLOW).move_to(UP * Q1_Y)
            q2 = T("Could a cleverer method need fewer?", Q_SIZE, YELLOW).move_to(UP * Q2_Y)
            # the last answer stays up a moment; the question takes over as it is read
            c.wait_until("this chapter")
            end = min(1.5, max(1.0, c.until("How many comparisons")))
            self.play(*[time_span(FadeOut(m), 0.0, 0.7) for m in self.marks],
                      *[time_span(a, 0.0, 0.7) for a in light(cells[0], False) + light(cells[3], False)],
                      time_span(FadeIn(q1, shift=0.3 * DOWN), 0.3, end), run_time=end)

            c.wait_until("clever")
            self.play(FadeIn(q2, shift=0.3 * DOWN), run_time=1.2)

            c.wait_until("get away")
            self.play(FadeOut(self.chain), q1.animate.move_to(UP * END_Q1_Y),
                      q2.animate.move_to(UP * END_Q2_Y), run_time=min(1.5, c.until(None, floor=0.8)))

        self.wait(1.0)
        self.play(FadeOut(q1), FadeOut(q2), run_time=1.0)
        self.wait(0.15)
