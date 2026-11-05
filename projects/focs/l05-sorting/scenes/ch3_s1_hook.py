"""Chapter 3, scene 1: Hook. Clips c3.hook.1 – c3.hook.3.

Plan
- opening: ch2's end card (rebuilt as WhyAndRecap.teaser leaves it) held 0.7 s, then the title card.
- c3.hook.1: title card; {last} the end card returns (no "Next" title); "?" pulse on "scoreboard";
  {slow} the split fades, the board grows to centre; 25,146,194 then 174 s flash.
- c3.hook.2: {race} board shrinks to the top; RED bar "insertion sort · 174 s" grows, GOLD sliver
  "quicksort · 0.74 s" under it on one scale; {under} the sliver flashes; {trick} "What's the trick?".
- c3.hook.3: {split} the chain 5 3 9 4 7 [] under the question; pivot lifts YELLOW, 3 4 left
  under "≤ 5", 9 7 right under "> 5"; {plan} three DIM tags; the chain rejoins and rises to the
  top: handover_shot() (ConsChain scale 0.8 at (0, 2.6)).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402

HS_SCALE, HS_Y = 0.8, 2.6          # the handover chain: scale and centre y (x = 0)
ROW_Y = 1.2                        # the split's chain row in c3.hook.3
LR_Y = -0.3                        # the two halves' row
LIFT = 0.65                        # pivot lift


def handover_shot():
    """The last frame: the running list 5 → 3 → 9 → 4 → 7 → [] across the top."""
    return ConsChain([5, 3, 9, 4, 7]).scale(HS_SCALE).move_to([0, HS_Y, 0])


def end_card():
    """ch2 s7's end card (WhyAndRecap.teaser's final frame), minus its "Next: quicksort" title.
    Same construction and order of operations as the teaser."""
    sb = make_scoreboard(bound="118,458")
    for col, val in enumerate(("25,146,194", "174 s")):
        v = T(val, 44, GOLD).move_to(sb.cells[0][col])
        sb.cells[0].submobjects[col] = v

    CH, yc, lift, drop = 0.55, -2.37, 0.4, 0.85
    top = 2.78
    avail = top - (yc + lift + CH / 2 + 0.15)
    s_big = min(5.75 / sb.height, 11.6 / sb.width)
    s_small = min(avail / sb.height, 12.0 / sb.width)
    sb.scale(s_big)
    sb.move_to([0, top - sb.height / 2, 0])

    qrow = VGroup(sb.row_labels[1], *sb.cells[1])
    lit = Rectangle(width=sb.width + 0.3, height=qrow.height + 0.3)
    lit.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).move_to([sb.get_x(), qrow.get_y(), 0])
    lit.set_z_index(-1)
    sb.add(lit)
    sb.scale(s_small / s_big)
    sb.move_to([0, top - sb.height / 2, 0])

    pivot = ConsCell(5, color=YELLOW).scale(CH).move_to([0, yc + lift, 0])
    pivot.label.set_color(YELLOW)
    L = ConsChain([3, 4]).scale(CH).move_to([-3.4, yc - drop, 0])
    R = ConsChain([9, 7]).scale(CH).move_to([3.4, yc - drop, 0])
    le = T("≤ 5", 40, t2c={"5": YELLOW}).next_to(L, UP, buff=0.3)
    gt = T("> 5", 40, t2c={"5": YELLOW}).next_to(R, UP, buff=0.3)
    split = VGroup(pivot, L, R, le, gt)
    card = VGroup(sb, split)
    card.sb, card.split, card.s_big, card.s_small = sb, split, s_big, s_small
    return card


def tag(text):
    t = T(text, 36, DIM)
    box = RoundedRectangle(corner_radius=0.15, width=t.width + 0.5, height=t.height + 0.4)
    box.set_stroke(DIM, 2).move_to(t)
    return VGroup(box, t)


class QuicksortHook(NarratedScene):
    def construct(self):
        self.opening()
        self.clip_title()
        self.clip_race()
        self.clip_split()

    # ── before the first line: ch2's end card, then the title card ────────────────
    def opening(self):
        nxt = T("Next: quicksort", 52, t2c={"quicksort": YELLOW}).move_to(UP * 3.3)
        old = end_card()
        self.card = card = title_card("Part 3 · Quicksort")
        self.add(nxt, old)
        self.wait(0.7)
        self.play(*during([FadeOut(nxt), FadeOut(old)], 0, 0.45),  # early: title card / the scoreboard returns whole
                  *during([FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule)], 0.45, 1.0),
                  run_time=1.6)

    # ── c3.hook.1 ────────────────────────────────────────────────────────────────
    def clip_title(self):
        card = self.card
        ec = end_card()
        sb, split = ec.sb, ec.split
        self.sb = sb

        with self.say("c3.hook.1") as c:
            self.play(FadeIn(card.course, shift=0.2 * DOWN),  # early: title card
                      time_span(FadeIn(card.part, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            c.wait_until("last")
            sweep_clear(self, time_span(FadeIn(sb, shift=0.2 * UP), 0.6, 1.5),  # early: title card / the scoreboard returns whole
                        time_span(FadeIn(split), 0.9, 1.6), run_time=1.6)
            c.wait_until("scoreboard")
            pulse = (lambda t: there_and_back((2 * t) % 1.0))
            self.play(*[q.animate(rate_func=pulse).scale(1.4) for q in sb.cells[1]],
                      run_time=min(1.2, c.until("slow")))
            c.wait_until("slow")
            sb.generate_target()
            sb.target.scale(ec.s_big / ec.s_small).move_to([0, 0.1, 0])
            self.play(*during([FadeOut(split)], 0, 0.45),
                      *during([MoveToTarget(sb)], 0.35, 1.0), run_time=1.6)
            c.wait_until("twenty-five million")
            self.play(FlashAround(sb.cells[0][0], color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("hundred and seventy-four")
            self.play(FlashAround(sb.cells[0][1], color=GOLD, time_width=1.5),
                      run_time=min(1.5, c.until()))

    # ── c3.hook.2 ────────────────────────────────────────────────────────────────
    def clip_race(self):
        sb = self.sb
        x0, full = -5.5, 11.0
        lab1 = T("insertion sort · 174 s", 36, RED)
        bar1 = Rectangle(width=full, height=0.42).set_fill(RED, 0.85).set_stroke(width=0)
        bar1.move_to([x0 + full / 2, -1.2, 0])
        lab1.next_to(bar1, UP, buff=0.22).align_to(bar1, LEFT)
        w2 = full * 0.74 / 174
        bar2 = Rectangle(width=w2, height=0.42).set_fill(GOLD, 1).set_stroke(width=0)
        bar2.move_to([x0 + w2 / 2, -2.7, 0])
        lab2 = T("quicksort · 0.74 s", 36, GOLD)
        lab2.next_to(bar2, UP, buff=0.22).align_to(bar2, LEFT)
        question = T("What's the trick?", 64, YELLOW).move_to(UP * 0.3)
        self.question = question

        with self.say("c3.hook.2") as c:
            sb.generate_target()
            sb.target.scale(3.3 / sb.height)
            sb.target.move_to([0, 3.5 - sb.target.height / 2, 0])
            self.play(MoveToTarget(sb), run_time=1.2)
            rt = max(1.6, min(3.2, 0.9 * c.until("zero point seven four")))
            self.play(FadeIn(lab1, shift=0.2 * DOWN, run_time=0.8),  # early: bar's caption, read with it
                      GrowFromEdge(bar1, LEFT, rate_func=linear, run_time=rt), run_time=rt)
            c.wait_until("zero point seven four")
            self.play(*appear(lab2), GrowFromEdge(bar2, LEFT), run_time=1.0)  # early: caption with its bar
            c.wait_until("under")
            self.play(FlashAround(bar2, color=YELLOW, time_width=1.5, buff=0.12),
                      FlashAround(lab2, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("three minutes")
            self.play(FlashAround(bar1, color=RED, time_width=1.5), run_time=min(1.5, c.until("trick")))
            c.wait_until("trick")
            sweep_clear(self, time_span(FadeIn(question, scale=0.9), 0.6, 1.3),
                        run_time=min(1.3, c.until()))

    # ── c3.hook.3 ────────────────────────────────────────────────────────────────
    def clip_split(self):
        q = self.question
        chain = ConsChain([5, 3, 9, 4, 7]).scale(HS_SCALE).move_to([0, ROW_Y, 0])
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil
        home = [cl.get_center().copy() for cl in cells]

        # the split's targets
        L = ConsChain([3, 4], with_nil=False).scale(HS_SCALE).move_to([-3.6, LR_Y, 0])
        R = ConsChain([9, 7], with_nil=False).scale(HS_SCALE).move_to([3.6, LR_Y, 0])
        piv_up = ConsCell(5, color=YELLOW).scale(HS_SCALE).move_to(home[0] + LIFT * UP)
        piv_up.label.set_color(YELLOW)
        piv_mid = piv_up.copy().move_to([0, ROW_Y + LIFT, 0])
        plab = T("pivot", 36, YELLOW).next_to(piv_up, LEFT, buff=0.25)
        le = T("≤ 5", 40, t2c={"5": YELLOW}).next_to(L, UP, buff=0.3)
        gt = T("> 5", 40, t2c={"5": YELLOW}).next_to(R, UP, buff=0.3)

        tags = VGroup(tag("the idea"), tag("the code"), tag("a trace"))
        tags.arrange(RIGHT, buff=0.7).move_to([0, -2.3, 0])

        with self.say("c3.hook.3", gap=0.0) as c:
            self.play(*during([q.animate.scale(52 / 64).move_to(UP * 3.15)], 0, 0.55),
                      *during([FadeIn(m) for m in (*cells, *arrows, nil)], 0.5, 1.0),
                      run_time=1.6)
            c.wait_until("pivot")
            self.play(Transform(cells[0], piv_up), FadeOut(arrows[0]),
                      time_span(FadeIn(plab, shift=0.2 * RIGHT), 0.5, 1.2), run_time=1.2)
            c.wait_until("smaller")
            self.play(*[FadeOut(a) for a in arrows[1:]], FadeOut(nil),
                      cells[1].animate.move_to(L.cells[0]),
                      cells[3].animate.move_to(L.cells[1]),
                      time_span(FadeIn(le, shift=0.2 * DOWN), 0.7, 1.3), run_time=1.3)
            c.wait_until("larger")
            plab.generate_target()
            plab.target.next_to(piv_mid, LEFT, buff=0.25)
            self.play(cells[2].animate.move_to(R.cells[0]),
                      cells[4].animate.move_to(R.cells[1]),
                      Transform(cells[0], piv_mid), MoveToTarget(plab),
                      time_span(FadeIn(gt, shift=0.2 * DOWN), 0.7, 1.3),
                      run_time=min(1.3, c.until("plan") + 0.4))
            c.wait_until("idea")
            self.play(*appear(tags[0]), run_time=1.0)
            c.wait_until("ocaml")
            self.play(*appear(tags[1]), run_time=1.0)  # early: names the code part
            c.wait_until("watch")
            self.play(*appear(tags[1 + 1]), run_time=1.0)  # early: names the trace part
            # the split rejoins into the running list
            c.wait_until("running list")
            back = ConsCell(5).scale(HS_SCALE).move_to(home[0])
            fresh = ConsChain([5, 3, 9, 4, 7]).scale(HS_SCALE).move_to([0, ROW_Y, 0])
            new_arrows, new_nil = list(fresh.arrows), fresh.nil
            rt = max(1.4, min(1.8, c.until() + 0.3))
            self.play(*during([FadeOut(plab), FadeOut(le), FadeOut(gt)], 0, 0.3),
                      *during([Transform(cells[0], back)], 0.2, 0.5),
                      # arcs keep the crossing cells apart: 3 and 4 dip below, 9 bows above
                      *during([cells[i].animate(path_arc=arc).move_to(home[i])
                               for i, arc in ((1, PI / 3), (2, PI / 2), (3, PI / 2), (4, 0))],
                              0.45, 0.85),
                      *during([FadeIn(m) for m in (*new_arrows, new_nil)], 0.75, 1.0),
                      run_time=rt)

        # tags and question clear; the chain rises to the top (the handover shot)
        self.wait(0.6)
        shot = handover_shot()
        self.play(*during([FadeOut(q), *[FadeOut(t) for t in tags]], 0, 0.45),
                  *during([Transform(cells[i], shot.cells[i]) for i in range(5)]
                         + [Transform(new_arrows[i], shot.arrows[i]) for i in range(5)]
                         + [Transform(new_nil, shot.nil)], 0.35, 1.0),
                  run_time=1.6)
        for m in (*cells, *new_arrows, new_nil):
            self.remove(*m.get_family())
        self.add(shot)
        self.wait(1.0)
