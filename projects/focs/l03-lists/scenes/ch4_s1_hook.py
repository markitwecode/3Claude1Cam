"""Chapter 4, scene 1: title card, ch1's front-vs-end question on cells, then @ and List.rev.

Clips c4.hook.1 - c4.hook.2.

STATUS: built (both clips). Layout:
hook.1  title card (ch3 style); on {front} "Lists" FadeTransforms into ConsChain [3,5,9] (S=1.1,
        CHAIN_Y=-0.6) while the subtitles slide to a lower third; "single cons": YELLOW cell 1 +
        arrow join at the front (chain recentres), GOLD "1 cons" above, GOLD O(1) below.  {end}:
        subtitles go, dashed YELLOW ghost cell 1 over the 9 -> [] arrow, GOLD "?" above it.  {walk}:
        DIM box walks 1 -> 3 -> 5 -> 9, DIM "walk the whole list" under the end.  "worse": "?" RED.
hook.2  "two tools": sweep; both inputs (size 44).  {at}: `[3; 5; 9] @ [2; 10]` => result born
        from copies (ch1_s3 idiom); {rev}: `List.rev [3; 5; 9]` => ch1's drop-and-swap.  {build}:
        dashed YELLOW boxes on `@` / `List.rev` + YELLOW "build both ourselves".  {slow}: board
        slides left, @ rows dim to 0.35, ch1-hook-style chart (DIM "work" / "length of the list");
        RED quadratic on "painfully", GREEN line on {fast} (curves, not words: dwell).
Verified with ocaml 5.4.1: [3; 5; 9] @ [2; 10] -> - : int list = [3; 5; 9; 2; 10];
List.rev [3; 5; 9] -> - : int list = [9; 5; 3].
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

S = 1.1                              # 1 -> 3 -> 5 -> 9 -> [] spans ~10.6 units
STEP = (CELL + PTR_W + LINK) * S     # distance between neighbouring cells
CHAIN_Y = -0.6                       # the cell row
SUB_Y = (-2.6, -3.15)                # the card's subtitles, parked as a lower third
GHOST_UP = 1.7                       # the hovering end cell sits this far above the row

CODE = 44                            # hook.2 code size
X0_START, X0_END = -2.96, -5.35      # code column's left edge: centred, then slid left for the chart
HEAD_Y, APP_Y, APP_RES_Y, REV_Y, REV_RES_Y = 2.75, 1.65, 0.5, -1.0, -2.15
CHART_X, CHART_Y = 4.7, -0.85        # the chart sits beside the List.rev rows


# ── helpers (local to this scene) ───────────────────────────────────────────────
def slink(src, dst, color=FG):
    """lib.style.link at this scene's scale (tip scaled like the chain's own arrows)."""
    return Arrow(src.tail_start(), dst.entry(), buff=0, stroke_width=3, color=color,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16 * S)


def ghost_cell(value, color=YELLOW):
    """A dashed, not-yet-real cons cell (same footprint as ConsCell at scale S)."""
    box = Square(CELL * S)
    ptr = Rectangle(width=PTR_W * S, height=CELL * S).next_to(box, RIGHT, buff=0)
    outline = VGroup(DashedVMobject(box, num_dashes=16), DashedVMobject(ptr, num_dashes=10))
    outline.set_stroke(color, 3)
    lab = value_label(value, color=color).scale(S).move_to(box)
    return VGroup(outline, lab)


def dashed_box(mob):
    return DashedVMobject(SurroundingRectangle(mob, color=YELLOW, buff=0.14, stroke_width=3),
                          num_dashes=28)


class Hook(NarratedScene):
    def construct(self):
        self.front_and_end()
        self.free_tools()
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.06),
                  run_time=1.2)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # hook.1: title card; the word becomes ch1's list; front is one cons, the end is a question
    def front_and_end(self):
        card = title_card("Part 4 · Append and reverse")
        chain = ConsChain([3, 5, 9]).scale(S)
        chain.shift(UP * (CHAIN_Y - chain.cells[0].box.get_y()))
        cells = chain.cells
        home = RIGHT * STEP / 2   # recentre once the front cell joins

        new = ConsCell(1, color=YELLOW).scale(S)
        new.move_to(cells[0].get_center() + home + LEFT * STEP)
        chain.shift(home)
        new_arrow = slink(new, cells[0], color=YELLOW)
        ghost = ghost_cell(1).move_to([chain.arrows[2].get_x(), CHAIN_Y + GHOST_UP, 0])
        chain.shift(-home)
        one_cons = T("1 cons", size=40, color=GOLD).next_to(new, UP, buff=0.3)
        o1 = MathTex(r"O(1)", font_size=60, color=GOLD).next_to(new, DOWN, buff=0.35)
        q = T("?", size=96, color=GOLD).next_to(ghost, UP, buff=0.3)
        walker = SurroundingRectangle(new, color=DIM, buff=0.12, corner_radius=0.08,
                                      stroke_width=5)
        walk = T("walk the whole list", size=32, color=DIM)
        walk.move_to([ghost.get_x(), o1.get_y(), 0])

        with self.say("c4.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
            c.wait_until("asked")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("almost")
            self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)

            # {front}: "...the front of a list": the word becomes ch1's list; subtitles step down
            c.wait_until("front")
            self.play(FadeTransform(card.title, chain), FadeOut(card.rule),
                      card.course.animate.move_to([0, SUB_Y[0], 0]),
                      card.part.animate.move_to([0, SUB_Y[1], 0]), run_time=1.6)

            # "a single cons, one new cell": the new cell joins at the front
            c.wait_until("single cons")
            self.play(chain.animate.shift(home), FadeIn(new, shift=RIGHT * 1.2),
                      time_span(GrowArrow(new_arrow), 0.8, 1.5),
                      time_span(FadeIn(one_cons, shift=0.3 * DOWN), 1.0, 1.7), run_time=1.7)
            # "however long the list is"
            c.wait_until("however long")
            self.play(FadeIn(o1, shift=0.3 * UP), run_time=1.0)

            # {end}: "But what about adding it to the end?"
            c.wait_until("end")
            self.play(LaggedStart(FadeOut(card.part), FadeOut(card.course), lag_ratio=0.2),
                      time_span(FadeIn(ghost, shift=0.3 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("to the end")
            self.play(FadeIn(q, scale=0.5, shift=0.25 * DOWN), run_time=1.0)

            # {walk}: "you'd have to walk the whole list": a marker steps from the head
            c.wait_until("walk")
            self.play(Create(walker), FadeIn(walk, shift=0.3 * UP), run_time=1.0)
            c.wait_until("walk the whole")
            steps = [Transform(walker, walker.copy().move_to(cells[i].get_center()))
                     for i in range(3)]
            self.play(Succession(*steps), run_time=max(1.4, min(1.9, c.until("worse") - 0.2)))

            # {more}: "The truth is a little worse": the question stays, now RED
            c.wait_until("worse")
            self.play(q.animate.set_color(RED).scale(1.15),
                      FlashAround(q, color=RED, time_width=1.5), FadeOut(walker), run_time=1.5)

    # hook.2: ch1's two free tools; we build both; reverse comes slow, then fast
    def free_tools(self):
        app = Code("[3; 5; 9] @ [2; 10]", size=CODE).move_to([X0_START, APP_Y, 0],
                                                               aligned_edge=LEFT)
        app.find("@").set_color(YELLOW)
        app_res = Code("[3; 5; 9; 2; 10]", size=CODE).move_to([X0_START, APP_RES_Y, 0],
                                                               aligned_edge=LEFT)
        arrow1 = Mono("⇒", size=72).next_to(app_res, LEFT, buff=0.35)

        rev = Code("List.rev [3; 5; 9]", size=CODE).move_to([X0_START, REV_Y, 0],
                                                             aligned_edge=LEFT)
        rev.find("List.rev").set_color(YELLOW)
        rev_res = Code("[9; 5; 3]", size=CODE)
        rev_res.move_to(rev.find("[3; 5; 9]")).set_y(REV_RES_Y)
        arrow2 = Mono("⇒", size=72).next_to(rev_res, LEFT, buff=0.35)

        heading = T("build both ourselves", size=40, color=YELLOW)
        heading.move_to([X0_START, HEAD_Y, 0], aligned_edge=LEFT)

        axes = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=3.8, y_length=3.0,
                    tips=True, axis_config={"color": DIM, "include_ticks": False,
                                            "stroke_width": 3, "tip_width": 0.22,
                                            "tip_height": 0.22})
        axes.move_to([CHART_X, CHART_Y, 0])
        x_lab = T("length of the list", size=32, color=DIM)
        y_lab = T("work", size=32, color=DIM)
        x_lab.next_to(axes.x_axis, DOWN, buff=0.25)
        y_lab.next_to(axes.y_axis, LEFT, buff=0.25).align_to(axes.y_axis, UP)
        slow_curve = axes.plot(lambda x: 0.11 * x * x, x_range=[0, 5.6], color=RED, stroke_width=6)
        fast_line = axes.plot(lambda x: 0.15 * x, x_range=[0, 5.6], color=GREEN, stroke_width=6)

        with self.say("c4.hook.2", gap=0.8) as c:   # a little extra hold on the final picture
            # "two tools that come free with OCaml": the board clears, both inputs arrive
            c.wait_until("two tools")
            sweep_clear(self, time_span(FadeIn(app, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(FadeIn(rev, shift=0.3 * DOWN), 0.8, 1.6), run_time=1.6)

            # {at}: the at sign joins two lists; the result is born from copies of both
            c.wait_until("at")
            self.play(FlashAround(app.find("@"), color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("joins")
            part1 = [VGroup(*app.find("3; 5; 9")), VGroup(*app_res.find("3; 5; 9"))]
            part2 = [VGroup(*app.find("2; 10")), VGroup(*app_res.find("2; 10"))]
            rest = VGroup(arrow1, app_res.find("["), app_res.find("]"), app_res.find(";", nth=2))
            self.play(TransformFromCopy(*part1), TransformFromCopy(*part2), FadeIn(rest),
                      run_time=max(1.0, min(1.6, c.until("rev") - 0.1)))
            self.remove(part1[1], part2[1], rest)
            self.add(arrow1, app_res)

            # {rev}: List.rev; 3, 5, 9 drop, then 3 and 9 trade ends (ch1's picture)
            c.wait_until("rev")
            self.play(FlashAround(rev.find("List.rev"), color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("reverses")
            spots = [rev_res.find(d)[0].get_center() for d in "953"]
            drops = [rev.find(d)[0].copy() for d in "359"]
            frame = VGroup(arrow2, rev_res.find("["), rev_res.find("]"),
                           *[g for k in range(2) for g in rev_res.find(";", nth=k)])
            self.play(*[d.animate.move_to(p) for d, p in zip(drops, spots)], run_time=0.8)
            self.play(drops[0].animate(path_arc=PI / 2).move_to(spots[2]),
                      drops[2].animate(path_arc=PI / 2).move_to(spots[0]), FadeIn(frame),
                      run_time=1.0)
            self.remove(*drops, frame)
            self.add(arrow2, rev_res)

            # {build}: "we build both of them ourselves": boxed as blueprints
            c.wait_until("build")
            box_app, box_rev = dashed_box(app.find("@")), dashed_box(rev.find("List.rev"))
            self.play(Create(box_app), Create(box_rev),
                      time_span(FadeIn(heading, shift=0.3 * DOWN), 0.3, 1.3), run_time=1.3)

            # {slow}: reverse takes the spotlight; the board slides left for a cost chart
            c.wait_until("slow")
            d = LEFT * (X0_START - X0_END)
            self.play(*[restyle(m, op=0.35, shift=d) for m in (app, app_res, arrow1, box_app)],
                      *[m.animate.shift(d) for m in (rev, rev_res, arrow2, box_rev, heading)],
                      time_span(Create(axes), 0.6, 1.6),
                      time_span(FadeIn(x_lab, y_lab), 0.9, 1.6), run_time=1.6)
            c.wait_until("painfully")
            self.play(Create(slow_curve), run_time=max(1.0, min(2.0, c.until("fast") - 0.1)))

            # {fast}: "and a small change that makes it fast"
            c.wait_until("fast")
            self.play(Create(fast_line),
                      run_time=max(1.0, min(2.0, c.until("makes it fast") + 0.4)))
