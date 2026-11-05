"""Chapter 1, scene 1: title card, then the hook question (front vs end).

Clips c1.hook.1 – c1.hook.3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

BOX = 1.4  # element boxes are CELL scaled up: the hook picture spans ~2/3 of the frame


def elem_box(v, color=BLUE):
    """A list element seen 'from the outside': a box with its value (a scaled ConsCell box)."""
    box = Square(CELL, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(box, value_label(v).move_to(box)).scale(BOX)


def elem_row(values=(3, 5, 9)):
    return VGroup(*[elem_box(v) for v in values]).arrange(RIGHT, buff=0.2)


def side_arrow(start, end):
    return Arrow(start, end, buff=0.15, color=DIM, stroke_width=4,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.2)


class Hook(NarratedScene):
    def construct(self):
        row = self.title_card()
        picture, front = self.question(row)
        self.not_the_same(picture, front)

    # hook.1: title card; the word "Lists" becomes a list
    def title_card(self):
        title = T("Lists", size=96)
        rule = Line(LEFT * 2.8, RIGHT * 2.8, stroke_width=2, color=DIM)
        course = T("Foundations of Computer Science · Lecture 3", size=36, color=DIM)
        part = T("Part 1 · Building lists", size=36)
        VGroup(title, rule, course, part).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        rule.shift(UP * 0.08)

        row = elem_row()

        with self.say("c1.hook.1") as c:
            self.play(FadeIn(title, shift=0.3 * DOWN), GrowFromCenter(rule), run_time=1.0)
            c.wait_until("foundations")
            self.play(FadeIn(course, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("all about lists")
            self.play(FadeIn(part, shift=0.25 * DOWN), run_time=1.0)

            # "Lists are the simplest way to hold a collection of things":
            # the title word turns into a list, in place; the subtitles stay to be read
            row.move_to(title)
            c.wait_until("collection")
            self.play(FadeTransform(title, row), FadeOut(rule), run_time=1.5)
        self.card_rest = VGroup(course, part)
        return row

    # hook.2: a new element for the front (ask, hold), then one for the end (ask, hold)
    def question(self, row):
        home = row.copy().move_to(ORIGIN)   # where the row settles for the question

        def newcomer(side):
            box = elem_box(1, color=YELLOW)
            edge = home.get_left() if side is LEFT else home.get_right()
            box.move_to(edge + side * (1.2 + box.width / 2))
            arrow = side_arrow(box.get_edge_center(-side), edge)
            q = T("?", size=96, color=GOLD).next_to(box, UP, buff=0.35)
            return box, arrow, q

        new_front, a_front, q_front = newcomer(LEFT)
        new_end, a_end, q_end = newcomer(RIGHT)
        front = VGroup(new_front, a_front, q_front)

        with self.say("c1.hook.2") as c:
            # "Suppose you have a list": the card's subtitles make way, the list takes centre
            c.wait_until("front")
            self.play(LaggedStart(FadeOut(self.card_rest[1]), FadeOut(self.card_rest[0]),
                                  lag_ratio=0.2),
                      row.animate.move_to(ORIGIN), run_time=1.5)

            # "...add one more element to the front. How much work is that?"
            c.wait_until("add one more")
            self.play(FadeIn(new_front, shift=1.2 * RIGHT),
                      time_span(GrowArrow(a_front), 0.7, 1.5), run_time=1.5)
            c.wait_until("how much work")
            self.play(FadeIn(q_front, scale=0.5, shift=0.25 * DOWN), run_time=1.0)

            # "Now suppose you want to add it to the end instead." Spotlight the new case.
            c.wait_until("end")
            self.play(front.animate.set_opacity(0.25), FadeIn(new_end, shift=1.2 * LEFT),
                      time_span(GrowArrow(a_end), 0.7, 1.5), run_time=1.5)
            c.wait_until("how much work", nth=1)
            self.play(FadeIn(q_end, scale=0.5, shift=0.25 * DOWN), run_time=1.0)
        picture = VGroup(row, new_front, a_front, q_front, new_end, a_end, q_end)
        return picture, front

    # hook.3: they don't cost the same (which is which stays open)
    def not_the_same(self, picture, front):
        q_y = front[2].get_y()
        approx = MathTex(r"\approx", font_size=96).move_to([0, q_y, 0])
        neq = MathTex(r"\neq", font_size=96, color=YELLOW).move_to([0, q_y, 0])
        top = VGroup(picture, approx)

        # where the picture goes to make room for the chart
        lifted = top.copy().scale(0.8).to_edge(UP, buff=0.75)

        # a cost chart that hints the two differ, without saying which is which
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=6.4, y_length=2.6,
                    tips=True, axis_config={"color": DIM, "include_ticks": False,
                                            "stroke_width": 3, "tip_width": 0.22,
                                            "tip_height": 0.22})
        x_lab = T("length of the list", size=32, color=DIM)
        y_lab = T("work", size=32, color=DIM)
        x_lab.next_to(axes.x_axis, DOWN, buff=0.25)
        y_lab.next_to(axes.y_axis, LEFT, buff=0.25).align_to(axes.y_axis, UP)
        chart = VGroup(axes, x_lab, y_lab).next_to(lifted, DOWN, buff=0.55)
        flat = axes.plot(lambda x: 0.9, x_range=[0, 5.6], color=GOLD, stroke_width=6)
        rise = axes.plot(lambda x: 0.15 + 0.6 * x, x_range=[0, 5.6], color=GOLD, stroke_width=6)

        with self.say("c1.hook.3") as c:
            # "You might guess these cost about the same. They don't."
            self.play(front.animate.set_opacity(1), run_time=1.0)
            c.wait_until("the same")
            self.play(FadeIn(approx, scale=0.5), run_time=1.0)
            c.wait_until("they don't")
            self.play(Transform(approx, neq), run_time=1.0)

            # "One of them takes a single step, no matter how long the list is.
            #  The other gets slower and slower as the list grows."
            c.wait_until("diff")
            top.save_state()
            self.play(top.animate.scale(0.8).move_to(lifted),
                      time_span(Create(axes), 0.6, 1.6),
                      time_span(FadeIn(VGroup(x_lab, y_lab)), 0.9, 1.6), run_time=1.6)
            c.wait_until("no matter")
            self.play(Create(flat), run_time=1.5)
            c.wait_until("slower")
            self.play(Create(rise), run_time=2.0)

            # "By the end of this chapter, you'll see exactly why": keep the open question
            c.wait_until("why")
            self.play(LaggedStart(FadeOut(rise), FadeOut(flat), FadeOut(chart), lag_ratio=0.15),
                      Restore(top), run_time=1.5)

        self.play(LaggedStart(*[FadeOut(m) for m in (*picture, approx)], lag_ratio=0.06),
                  run_time=1.0)
