"""Chapter 5, scene 1: Hook. Title card, the ln 2i ladder recalled, 2^3 by multiplication, then i^i ?. Clips c5.hook.1 – c5.hook.2."""
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

COUNT = load_scene("ch5_s5_count")


def ii_question(size=130):
    """The big i^i (both i's PINK) with a YELLOW "?" beside it, centred at ORIGIN.
    Returns a VGroup with .ii (MathTex) and .q (the "?")."""
    ii = MathTex(r"i^{i}", font_size=size, color=PINK)
    q = T("?", size=int(size * 0.8), color=YELLOW)
    q.next_to(ii, RIGHT, buff=0.3).align_to(ii, DOWN)
    g = VGroup(ii, q).move_to(ORIGIN)
    g.ii, g.q = ii, q
    return g


class Ch5S1Hook(NarratedScene):
    def construct(self):
        # ------------------------------------------------ clip 1
        with self.say("c5.hook.1") as c:
            card = title_card("Part 5 · Complex powers")
            card.title.scale_to_fit_width(min(card.title.width, 12.4))
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      run_time=0.8)
            self.play(*appear(card.course, card.part, lag=0.3), run_time=0.8)  # early: title card
            c.wait_until("ladder")

            # the card slides right and shrinks (stays readable); the ladder grows in on the left
            for m, s in ((card.title, 0.55), (card.rule, 0.55), (card.course, 0.85), (card.part, 0.85)):
                m.generate_target().scale(s)
            VGroup(*[m.target for m in (card.title, card.rule, card.course, card.part)]).arrange(
                DOWN, buff=0.35).move_to([2.9, 0.3, 0])
            self.play(*[MoveToTarget(m) for m in (card.title, card.rule, card.course, card.part)],
                      run_time=1.2)

            lad = COUNT.ladder(ns=(-1, 0, 1, 2), x=-0.4, y0=-1.5, pitch=1.0,
                               labels={0: "principal value"},
                               line_label=r"\mathrm{Re}\,w=\ln 2", brace=True, ext=0.5)
            rungs = [lad.rungs[n] for n in sorted(lad.rungs)]
            board = VGroup(lad, lad.line_label, lad.labels[0])
            board.scale(1.15).to_edge(LEFT, buff=0.6).set_y(-0.3)
            self.play(Create(lad.line), FadeIn(lad.line_label, shift=0.2 * DOWN), run_time=1.0)
            self.play(*appear(*rungs, shift=None, lag=0.25), run_time=1.2)
            self.play(*appear(lad.labels[0]), FlashAround(lad.rungs[0], color=GREEN),  # early: recap label
                      run_time=1.0)
            c.wait_until("two pi")
            self.play(GrowFromCenter(lad.brace), *appear(lad.brace_label, shift=None),
                      run_time=min(1.2, c.until("today")))
            c.wait_until("today")

            board.generate_target()
            board.target.scale(1 / 1.15).to_edge(LEFT, buff=0.5).set_y(-0.4)
            self.play(*disappear(card.title, card.rule, card.course, card.part),
                      MoveToTarget(board), run_time=min(1.2, 0.6 * c.remaining))
            self.play(*set_alpha([board], 0.4), run_time=min(0.6, 0.8 * c.remaining))

        # ------------------------------------------------ clip 2
        hx = 2.0
        with self.say("c5.hook.2") as c:
            cube = MathTex(r"2^3", "=", "2", r"\cdot", "2", r"\cdot", "2", "=", "8", font_size=84)
            cube.move_to([hx, 2.3, 0])
            cube[0].set_color(GOLD)
            cube[8].set_color(GOLD)
            self.play(*appear(cube[0], cube[1]), run_time=1.0)
            c.wait_until("multiply")
            twos = [cube[2], VGroup(cube[3], cube[4]), VGroup(cube[5], cube[6])]
            for t in twos:
                self.play(*appear(t, shift=None), run_time=0.6)
            c.wait_until("eight")
            self.play(*appear(cube[7], cube[8], lag=0.2), run_time=0.9)
            c.wait_until("so what")

            q = ii_question().move_to([hx, -0.2, 0])
            self.play(*appear(q.ii), run_time=1.0)
            self.play(*appear(q.q), run_time=0.7)
            c.wait_until("no way")

            tri = VGroup(MathTex(r"i \cdot i \cdot \ldots", font_size=60, color=PINK),
                         T("(i times?)", size=40, color=DIM)).arrange(RIGHT, buff=0.35)
            tri.move_to([hx, -2.4, 0])
            self.play(*appear(tri[0]), run_time=1.0)
            c.wait_until(own_word=tri[1])
            self.play(*appear(tri[1]), run_time=0.8)
            strike = Line(tri.get_left() + 0.15 * LEFT, tri.get_right() + 0.15 * RIGHT,
                          color=RED, stroke_width=6)
            self.play(Create(strike), run_time=0.8)
            c.wait_until("claim")

            tag = T("real?", size=40, color=YELLOW).next_to(q.q, DOWN, buff=0.35)
            self.play(*set_alpha([tri, strike], 0.4), run_time=0.8)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=0.9)
            c.wait_until("promise")
            self.play(FlashAround(VGroup(q, tag), color=YELLOW, run_time=2, time_width=1.5),
                      run_time=min(2.0, c.until("and see why")))
            c.wait_until()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
