"""Chapter 2, scene 1: title card, the two shapes of a list from chapter 1, the open question
"head of [] = ?" (scene 3 answers it), how can a function tell the shapes apart, and the plan.

Clips c2.hook.1 - c2.hook.3.

STATUS (paused): done: all 3 clips built, renders clean, dwell 0 flags, no clip overruns
(54.9 s vs 53.2 s narration+gaps + 1.15 s fade); remaining: a final full-size look at the
hook.2 -> hook.3 transition after the last timing fix; known issues: "no head" / "nil" /
"cons" in the shrunk top band are ~29-32 pt (legal but small).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, TransformMatchingStrings, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

# The two shapes side by side: the big nil on the left, the chain 1 -> 2 -> 3 -> [] on the
# right. Together they span ~10 of the frame's 14.2 units.
SHAPE_Y = 1.0
NIL_X = -4.65
CHAIN_X = 1.48
LABEL_DY = 1.1          # "nil" / "cons" sit this far under the shapes
Q_Y = -2.45             # the question's row (the subtitles' row before it)
COVER = "#2A2E35"       # the grey cover over the unknown list


# ── helpers (local to this scene) ───────────────────────────────────────────────
def span_brace(left_pt, right_pt, direction=UP, color=DIM, inset=0.06, buff=0.15):
    """A brace over (or under) the horizontal span left_pt..right_pt."""
    line = Line(left_pt + RIGHT * inset, right_pt + LEFT * inset)
    return Brace(line, direction, buff=buff, color=color)


def question_mob(size=48):
    """`head of [] = ?`, laid out as in chapter 1's last scene (scene 3 brings it back)."""
    return VGroup(T("head", size=size, color=YELLOW), T("of", size=size), Code("[]", size=size),
                  T("=", size=size), T("?", size=round(size * 1.75), color=GOLD)).arrange(RIGHT, buff=0.3)


def which_shape(size=44):
    words = T("which shape", size=size)
    q = T("?", size=round(size * 1.45), color=GOLD).next_to(words, RIGHT, buff=0.08)
    q.align_to(words[0], DOWN)       # sit the "?" on the baseline ("p" hangs below it)
    return VGroup(words, q)


class Hook(NarratedScene):
    def construct(self):
        self.two_shapes()
        self.which_one()
        self.plan()
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # hook.1: title card; nil and cons, side by side; the question from chapter 1
    def two_shapes(self):
        card = title_card("Part 2 · Pattern matching")

        nil = Nil(size=96).move_to([NIL_X, SHAPE_Y, 0])
        chain = ConsChain([1, 2, 3]).move_to([CHAIN_X, SHAPE_Y, 0])
        cells = chain.cells
        nil_lab = T("nil", size=40, color=TEAL).move_to([NIL_X, SHAPE_Y - LABEL_DY, 0])
        cons_lab = T("cons", size=40, color=BLUE).move_to([CHAIN_X, SHAPE_Y - LABEL_DY, 0])
        nil_lab.align_to(cons_lab, DOWN)

        # head / tail braces above the chain (scene 2 puts x and l in exactly these places)
        top_y = cells[0].box.get_top()[1]
        head_br = span_brace(cells[0].box.get_corner(UL), cells[0].box.get_corner(UR), color=YELLOW)
        head_lab = T("head", size=36, color=YELLOW).next_to(head_br, UP, buff=0.12)
        tail_br = span_brace(cells[1].box.get_corner(UL),
                             np.array([chain.nil.get_right()[0], top_y, 0]), color=TEAL)
        tail_lab = T("tail", size=36, color=TEAL).next_to(tail_br, UP, buff=0.12)
        tail_lab.align_to(head_lab, DOWN)

        question = question_mob().move_to([0, Q_Y, 0])
        q_head, q_of, q_nil, q_eq, q_mark = question

        with self.say("c2.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
            c.wait_until("in the last chapter")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("every list")
            self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)

            # "...is one of two things."  The subtitles step down to a lower third, where they
            # stay to be read; "Lists" heads the two shapes until the chain needs its place.
            c.wait_until("one of two things")
            self.play(card.course.animate.move_to([0, Q_Y + 0.05, 0]),
                      card.part.animate.move_to([0, Q_Y - 0.65, 0]), run_time=1.3)

            # "Either it's nil, the empty list."
            c.wait_until("nil")
            self.play(FadeIn(nil, scale=0.8), FadeIn(nil_lab, shift=0.25 * UP), run_time=1.2)

            # "Or it's a head, consed onto a tail."
            c.wait_until("cons")
            self.play(time_span(FadeOut(card.title, shift=0.3 * UP), 0, 0.5),
                      time_span(FadeOut(card.rule), 0, 0.5),
                      time_span(LaggedStart(*[FadeIn(m, shift=0.3 * LEFT) for m in chain], lag_ratio=0.12),
                                0.35, 1.1),
                      FadeIn(cons_lab, shift=0.25 * UP), run_time=c.until("a head", floor=1.1))
            self.play(GrowFromCenter(head_br), FadeIn(head_lab, shift=0.25 * DOWN),
                      time_span(FadeOut(card.course), 0, 0.8), time_span(FadeOut(card.part), 0.1, 0.9),
                      run_time=1.1)
            c.wait_until("tail")
            self.play(GrowFromCenter(tail_br), FadeIn(tail_lab, shift=0.25 * DOWN), run_time=1.1)

            # "What should happen if you ask for the head of an empty list?"  The question goes
            # on screen as an object, built from the pieces it is about (P5, P23).
            c.wait_until("what should happen")
            self.play(TransformFromCopy(head_lab, q_head), FadeIn(q_of, shift=0.25 * DOWN), run_time=1.3)
            c.wait_until("empty list")
            self.play(TransformFromCopy(nil.label, q_nil.text), FadeIn(q_eq),
                      time_span(FadeIn(q_mark, scale=0.5, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # {pause=1.5}: the question holds

        self.nil, self.chain = nil, chain
        self.nil_lab, self.cons_lab = nil_lab, cons_lab
        self.braces = [head_br, head_lab, tail_br, tail_lab]
        self.head_lab = head_lab
        self.question = question

    # hook.2: no first cell, so no head; then how does a function know which shape it got?
    def which_one(self):
        nil, chain = self.nil, self.chain

        # a pointer reaches for the nil's first cell, level with the chain's "head"
        reach = T("head", size=40, color=YELLOW).move_to([NIL_X, self.head_lab.get_y(), 0])
        reach_arrow = Arrow(reach.get_bottom() + DOWN * 0.06, nil.get_top() + UP * 0.08, buff=0,
                            stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.35,
                            tip_length=0.18)
        no_head = T("no head", size=40, color=RED).move_to(reach).align_to(reach, DOWN)

        # the machine: a list under a grey cover slides into a function
        fbox = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.35, stroke_color=BLUE,
                                stroke_width=3).set_fill(BG, opacity=1)
        flab = T("function", size=40)
        cover = RoundedRectangle(corner_radius=0.15, width=2.7, height=1.15, stroke_color=DIM,
                                 stroke_width=3).set_fill(COVER, opacity=1)
        clab = T("a list", size=36)
        MY = -0.55
        fbox.move_to([-0.2, MY, 0])
        flab.move_to(fbox)
        cover.move_to([-4.15, MY, 0])
        clab.move_to(cover)
        feed = Arrow(cover.get_right(), fbox.get_left(), buff=0.12, stroke_width=4, color=DIM,
                     max_tip_length_to_length_ratio=0.3, tip_length=0.2)
        ask = which_shape().next_to(fbox, RIGHT, buff=0.6)
        # the function reaching back for the front of the list (a curved pointer, below)
        grab = ArcBetweenPoints(fbox.get_bottom() + LEFT * 0.9 + DOWN * 0.08,
                                cover.get_corner(DL) + RIGHT * 0.45 + DOWN * 0.08,
                                angle=-PI / 3, color=YELLOW, stroke_width=4)
        grab.add_tip(tip_length=0.22, tip_width=0.22)

        top = VGroup(nil, chain, self.nil_lab, self.cons_lab, reach, reach_arrow)
        q_low = Q_Y - 0.4

        with self.say("c2.hook.2") as c:
            # "There's nothing there to give back."
            self.play(FadeIn(reach, shift=0.25 * DOWN), GrowArrow(reach_arrow), run_time=1.2)
            # "The empty list has no first cell, so it has no head."
            c.wait_until("no first cell")
            self.play(FlashAround(nil, color=RED, time_width=1.5), reach_arrow.animate.set_color(RED),
                      run_time=1.2)
            c.wait_until("no head")
            self.play(TransformMatchingStrings(reach, no_head), run_time=1.0)
            top.remove(reach)
            top.add(no_head)

            # "And behind that sits a bigger question."  The two shapes move up and stay as
            # the two options; the question steps down.
            c.wait_until("bigger")
            top.generate_target()
            top.target.scale(0.8).to_edge(UP, buff=0.45).set_x(0.15)
            self.play(LaggedStart(*[FadeOut(m) for m in self.braces], lag_ratio=0.1),
                      MoveToTarget(top), self.question.animate.set_y(q_low), run_time=1.8)

            # "When a function is handed a list,"
            c.wait_until("when a function")
            cover_group = VGroup(cover, clab)
            cover_group.shift(LEFT * 3.5)
            self.play(FadeIn(fbox), FadeIn(flab),
                      time_span(cover_group.animate.shift(RIGHT * 3.5), 0.3, 1.6),
                      time_span(GrowArrow(feed), 1.3, 1.8), run_time=1.8)
            # "how can it tell which of the two shapes it got?"
            c.wait_until("which of the")
            self.play(FadeIn(ask, shift=0.25 * LEFT),
                      LaggedStart(FlashAround(nil, color=TEAL, time_width=1.5),
                                  FlashAround(chain, color=BLUE, time_width=1.5), lag_ratio=0.5),
                      run_time=1.8)

            # "It has to know, before it reaches for a head that might not exist."
            c.wait_until("reaches for")
            self.play(time_span(Create(grab), 0, 1.1),
                      time_span(FlashAround(cover, color=GOLD, time_width=1.5), 0.85, 1.95),
                      run_time=min(1.95, c.remaining))

        self.machine = [fbox, flab, cover, clab, feed, grab]
        self.top = top
        self.ask = ask

    # hook.3: both questions, one idea: pattern matching; then a glimpse of 'a
    def plan(self):
        q1, q2 = self.question, self.ask
        q1_t = q1.copy().move_to([0, 1.35, 0]).align_to(RIGHT * -0.85, RIGHT)
        q2_t = q2.copy().move_to([0, 0.1, 0]).align_to(RIGHT * -0.85, RIGHT)
        brace = Brace(VGroup(q1_t, q2_t), RIGHT, buff=0.3, color=DIM)
        idea = T("pattern matching", size=56, color=YELLOW).next_to(brace, RIGHT, buff=0.35)

        alpha_type = Code("'a list", size=60).move_to([0, -1.7, 0])
        tick = alpha_type.find("'a")
        alpha = MathTex(r"\alpha", font_size=72, color=PINK).next_to(tick, DOWN, buff=0.3)

        with self.say("c2.hook.3") as c:
            # "In this chapter, we'll answer both questions"  (the board clears around them, P18)
            self.play(time_span(LaggedStart(*[FadeOut(m) for m in (*self.top, *self.machine)],
                                            lag_ratio=0.05), 0, 0.8),
                      time_span(Transform(q1, q1_t), 0.45, 1.6), time_span(Transform(q2, q2_t), 0.45, 1.6),
                      run_time=1.6)
            c.wait_until("both questions")
            self.play(LaggedStart(FlashAround(q1, color=GOLD, time_width=1.5),
                                  FlashAround(q2, color=GOLD, time_width=1.5), lag_ratio=0.4), run_time=1.5)
            # "with a single idea, called pattern matching."
            c.wait_until("pattern matching")
            self.play(GrowFromCenter(brace), FadeIn(idea, shift=0.3 * LEFT), run_time=1.5)

            # "Along the way, we'll meet some strange-looking types, with a little alpha in them."
            c.wait_until("strange-looking types")
            self.play(FadeIn(alpha_type, shift=0.3 * UP), run_time=1.2)
            c.wait_until("alpha")
            self.play(FlashAround(tick, color=PINK, time_width=1.5),
                      FadeIn(alpha, shift=0.25 * DOWN), run_time=1.3)

            # "And we'll see how they let a single function work on lists of every kind."
            c.wait_until("every kind")
            self.play(FlashAround(VGroup(alpha_type, alpha), color=PINK, time_width=1.5), run_time=1.5)
