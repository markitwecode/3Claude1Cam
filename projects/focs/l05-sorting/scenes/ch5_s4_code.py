"""Chapter 5, scene 4: tmergesort's code, the take/drop split, and how it differs from quicksort.
Clips c5.code.1 – c5.code.3.

Layout
- code.1/2: YELLOW `merge (xs, ys)` reference top-left; the notes' tmergesort hero (Code 34, as
  separate line copies), one YELLOW box sliding clause to clause, DIM tags "top-down" and
  "one item (...)", the toplevel reply under it on {type}.
- {split}: the code keeps only its three `let` lines, shrunk to the top; L4 ch1 s7's where_used
  shot (same strings, sizes and relative layout, 0.6 lower) under it: running chain + xs, the
  GOLD cut after cell 2, `List.length xs / 2`, take/drop lifted over their halves.
  `split_shot()` (module level) draws chain + GOLD cut + the two lifted halves, for s7's recap.
- code.3: table, rows divide/conquer/combine, columns quicksort/merge sort; the GOLD comparisons
  badge travels from quicksort's divide cell down a clear corridor into merge sort's combine
  cell. On {arrays} the table dims and shrinks to the top; array strip left, running chain right.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── shared with L4 ch1 s7 (where_used) ─────────────────────────────────────────
RUN = [3, 5, 9, 4, 7]
CUT_HALF = 1.05
CUT_DASH = 0.12
CUT_WIDTH = 5
SHOT_DY = -0.6             # L4's shot sits at ORIGIN; here it is lowered under the shrunk code

# ── this scene's layout ────────────────────────────────────────────────────────
HERO = 34                  # hero code size
HERO_CY = 0.2
SMALL = 28                 # the three let lines after {split}
SMALL_TOP = 3.55
SRC = """let rec tmergesort = function
  | [] -> []
  | [x] -> [x]
  | xs ->
      let k = List.length xs / 2 in
      let l = tmergesort (take k xs) in
      let r = tmergesort (drop k xs) in
      merge (l, r)"""
REPLY = "val tmergesort : 'a list -> 'a list = <fun>"

LAB_X, Q_X, M_X = -5.4, -1.6, 4.2       # table columns
HEAD_Y, DIV_Y, CON_Y, COM_Y = 2.95, 1.85, -0.1, -1.15
BADGE_DY = -0.85                         # badge under its cell's text
CORRIDOR_X = 1.25                        # clear vertical lane between the two columns
CAPTION_Y = -3.2


def lines_of(src, size, left=None, cy=0.0, cx=0.0):
    """As L4: lay out one Code, hand back each line as its own top-level copy."""
    code = Code(src, size=size)
    code.move_to([cx, cy, 0])
    if left is not None:
        code.align_to(np.array([left, 0, 0]), LEFT)
    return code, [code.line(i).copy() for i in range(src.count("\n") + 1)]


def part(code, lines, i, s, nth=0):
    full = list(code.line(i))
    return VGroup(*[lines[i][full.index(g)] for g in code.find(s, line=i, nth=nth)])


def span(anim, a, b, rt):
    return time_span(anim, a * rt, b * rt)


def cut_at(x, color=GOLD, width=CUT_WIDTH):
    return DashedLine([x, CUT_HALF, 0], [x, -CUT_HALF, 0], dash_length=CUT_DASH,
                      color=color, stroke_width=width)


def pill(content, color, pad_w=0.5, pad_h=0.32):
    box = RoundedRectangle(corner_radius=0.2, width=content.width + pad_w, height=content.height + pad_h,
                           stroke_color=color, stroke_width=2.5).set_fill(color, opacity=0.10)
    box.move_to(content)
    return VGroup(box, content)


def split_parts():
    """L4 ch1 s7's where_used shot, lowered by SHOT_DY."""
    run = ConsChain(RUN).shift(SHOT_DY * UP)
    cells = run.cells
    x_cut = (cells[1].ptr.get_right()[0] + cells[2].box.get_left()[0]) / 2
    cut = cut_at(x_cut).shift(SHOT_DY * UP)
    xs = label_pointer("xs", cells[0], direction=DOWN)
    _, half = lines_of("List.length xs / 2\n- : int = 2", 40, cy=-2.25 + SHOT_DY)
    _, tk = lines_of("take 2 xs\n- : int list = [3; 5]", 32, -6.45, 1.9 + SHOT_DY)
    _, dp = lines_of("drop 2 xs\n- : int list = [9; 4; 7]", 32, -0.3, 1.9 + SHOT_DY)
    return run, cut, xs, half, tk, dp


def split_shot():
    """The finished take/drop split: running chain, GOLD cut after cell 2, the two lifted halves."""
    run, cut, _, _, tk, dp = split_parts()
    return VGroup(run, cut, *tk, *dp)


class MergeSortCode(NarratedScene):
    def construct(self):
        self.code_walk()
        self.contrast()
        self.wait(4.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── code.1 / code.2 up to {type} ─────────────────────────────────────────
    def code_walk(self):
        code, ln = lines_of(SRC, HERO, cy=HERO_CY)
        for i, name in [(4, "k ="), (5, "l ="), (6, "r =")]:
            part(code, ln, i, name)[0].set_color(FG)
        for i, name in [(5, "tmergesort"), (6, "tmergesort"), (5, "take"), (6, "drop"), (7, "merge")]:
            part(code, ln, i, name).set_color(YELLOW)
        self.code, self.ln = code, ln

        ref = Mono("merge (xs, ys)", size=30, color=YELLOW).to_corner(UL, buff=0.5)
        t_glyph = ln[0][list(code.line(0)).index(code.find("tmergesort", line=0)[0])]
        top_down = T("top-down", size=30, color=DIM)
        top_down.move_to([t_glyph.get_x() + 1.45, t_glyph.get_top()[1] + 0.6, 0])
        td_arrow = Arrow(top_down.get_corner(DL) + 0.1 * RIGHT, t_glyph.get_top(), buff=0.08,
                         stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.3)
        one = T("one item (quicksort's pattern, Part 3)", size=30, color=DIM)
        one.next_to(ln[2], RIGHT, buff=0.7)
        reply = Code(REPLY, size=30).move_to([0, -2.95, 0])

        def box_on(i, s):
            return token_box(part(code, ln, i, s), ln[i])

        with self.say("c5.code.1") as c:
            self.play(*appear(ref), run_time=1.0)
            c.wait_until("code")
            self.play(*appear(*ln, lag=0.12), run_time=min(2.0, 0.9 * c.until("name")))  # early: the code is shown whole, then walked
            c.wait_until("name")
            self.play(*appear(top_down), GrowArrow(td_arrow), FlashAround(t_glyph, color=YELLOW, time_width=1.5),
                      run_time=min(1.4, 0.9 * c.until("nil")))
            c.wait_until("nil")
            box = box_on(1, "[] -> []")
            self.play(FadeIn(box), run_time=min(1.0, c.until("single")))
            c.wait_until("single")
            self.play(Transform(box, box_on(2, "[x] -> [x]")), run_time=min(1.0, 0.9 * c.until("one item")))
            c.wait_until(own_word=one)
            self.play(*appear(one), run_time=min(1.0, 0.9 * c.until("half")))
            c.wait_until("half")
            self.play(Transform(box, box_on(3, "xs ->")), run_time=min(1.0, 0.9 * c.until("kay is half")))
            c.wait_until("kay is half")
            self.play(Transform(box, box_on(4, "let k = List.length xs / 2 in")), run_time=1.0)

        with self.say("c5.code.2") as c:
            self.play(Transform(box, box_on(5, "tmergesort (take k xs)")), run_time=1.0)
            c.wait_until("right")
            self.play(Transform(box, box_on(6, "tmergesort (drop k xs)")), run_time=1.0)
            c.wait_until("merge")
            self.play(Transform(box, box_on(7, "merge (l, r)")), run_time=1.0)
            c.wait_until("type")
            self.play(FadeOut(box), *appear(reply), run_time=1.2)
            c.wait_until("split")
            self.split_play(c, [ref, top_down, td_arrow, one, reply])
            self.split_rest(c)

    # ── code.2 from {split}: L4's where_used shot ─────────────────────────────
    def split_play(self, c, extras):
        ln = self.ln
        keep = [ln[4], ln[5], ln[6]]
        gone = [ln[0], ln[1], ln[2], ln[3], ln[7], *extras]
        small = VGroup(*[m.copy() for m in keep]).scale(SMALL / HERO)
        small.move_to([0, 0, 0]).align_to(np.array([0, SMALL_TOP, 0]), UP)
        run, cut, xs, half, tk, dp = split_parts()
        self.shot = (run, cut, xs, half, tk, dp)
        rt = 2.0
        self.play(*during(disappear(*gone), 0, 0.4),
                  *[during([m.animate.scale(SMALL / HERO).move_to(t.get_center())], 0.35, 0.8)[0]
                    for m, t in zip(keep, small)],
                  *during([FadeIn(run, shift=0.3 * UP)], 0.65, 1.0),
                  *during(appear(xs), 0.8, 1.0),
                  run_time=rt)
        self.small = keep

    def split_rest(self, c):
        run, cut, xs, half, tk, dp = self.shot
        cells = run.cells
        c.wait_until("half the length")
        self.play(*appear(half[0]), run_time=min(1.0, 0.9 * c.until("is two")))
        c.wait_until("is two")
        self.play(*appear(half[1]), GrowFromCenter(cut), run_time=min(1.0, 0.9 * c.until("take")))
        c.wait_until("take")
        rt = min(1.4, 0.9 * c.until("drop"))
        self.play(span(FadeIn(tk[0], shift=0.4 * UP), 0, 0.8, rt), span(FadeIn(tk[1], shift=0.4 * UP), 0.2, 1.0, rt),
                  *flash([cells[0], cells[1]], YELLOW, time_width=1.5), run_time=rt)
        c.wait_until("drop")
        rt = 1.4
        self.play(span(FadeIn(dp[0], shift=0.4 * UP), 0, 0.8, rt), span(FadeIn(dp[1], shift=0.4 * UP), 0.2, 1.0, rt),
                  *flash([cells[2], cells[3], cells[4]], YELLOW, time_width=1.5), run_time=rt)
        even = T("2 and 3: differ by at most 1", size=30, color=GOLD)
        even.move_to(half[1]).align_to(np.array([1.3, 0, 0]), LEFT)
        c.wait_until("even")
        self.play(*appear(even), run_time=1.0)

    # ── code.3: quicksort vs merge sort ───────────────────────────────────────
    def contrast(self):
        def cell(text, x, y, color=FG, size=32):
            return T(text, size=size, color=color).move_to([x, y, 0])

        heads = [cell("quicksort", Q_X, HEAD_Y, YELLOW, 36), cell("merge sort", M_X, HEAD_Y, YELLOW, 36)]
        rule = Line([-6.4, HEAD_Y - 0.45, 0], [6.4, HEAD_Y - 0.45, 0], color=DIM, stroke_width=2)
        rows = [cell(w, LAB_X, y, DIM, 34) for w, y in
                [("divide", DIV_Y), ("conquer", CON_Y), ("combine", COM_Y)]]
        q_div = cell("partition round a pivot", Q_X, DIV_Y)
        badge = pill(VGroup(T("n − 1", size=28, color=GOLD), T("comparisons", size=28, color=GOLD))
                     .arrange(DOWN, buff=0.12), GOLD)
        badge.move_to([Q_X, DIV_Y + BADGE_DY, 0])
        q_con = cell("sort both parts", Q_X, CON_Y)
        q_com = cell("append", Q_X, COM_Y)
        m_div = cell("count out half", M_X, DIV_Y)
        m_none = cell("no comparisons", M_X, DIV_Y + BADGE_DY, GREEN, 30)
        m_con = cell("sort both halves", M_X, CON_Y)
        m_com = cell("merge", M_X, COM_Y, YELLOW)
        caption = T("the work moves from dividing to combining", size=34).move_to([0, CAPTION_Y, 0])

        with self.say("c5.code.3") as c:
            c.wait_until("with quicksort")
            rt = min(1.4, max(1.0, 0.9 * c.until("both of them")))
            sweep_clear(self, span(FadeIn(VGroup(*heads, rule, *rows), shift=0.2 * DOWN), 0.5, 1.0, rt),  # early: the empty table is the frame
                        run_time=rt)
            c.wait_until("quick")
            self.play(*appear(q_div), run_time=1.0)  # early: the divide cell, on "works hard to divide"
            c.wait_until("comparing every")
            self.play(GrowFromCenter(badge), run_time=1.0)  # early: on "comparing every item"
            c.wait_until("and then all")
            self.play(*appear(q_con), run_time=1.0)  # early: the conquer step, between divide and the append
            c.wait_until("append")
            self.play(*appear(q_com), run_time=1.0)
            c.wait_until("counting out")
            self.play(*appear(m_div), run_time=1.0)
            c.wait_until("no comparisons")
            self.play(*appear(m_none), run_time=1.0)
            self.wait(0.6)
            self.play(*appear(m_con), run_time=1.0)  # early: the conquer step, read before combining
            c.wait_until("moves")
            self.play(*appear(m_com), run_time=1.0)
            path = VMobject().set_points_as_corners([
                badge.get_center(), [CORRIDOR_X, DIV_Y + BADGE_DY, 0],
                [CORRIDOR_X, COM_Y + BADGE_DY, 0], [M_X, COM_Y + BADGE_DY, 0]])
            self.play(MoveAlongPath(badge, path), run_time=min(2.2, 0.7 * c.until("the work has")))
            self.play(*appear(caption), run_time=1.0)

            # {arrays}: the table dims, then gives way to arrays vs lists
            table = [*heads, rule, *rows, q_div, badge, q_con, q_com, m_div, m_none, m_con, m_com, caption]
            strip = VGroup(*[Square(1.0, color=BLUE, stroke_width=3) for _ in RUN]).arrange(RIGHT, buff=0)
            strip.move_to([0, 2.05, 0])
            vals = VGroup(*[value_label(v, size=42).move_to(s) for v, s in zip(RUN, strip)])
            hard = T("hard to code for arrays", size=34, color=DIM).next_to(strip, DOWN, buff=0.4)
            chain = ConsChain(RUN).move_to([0, -1.2, 0])
            nat = T("natural for lists", size=34, color=GREEN).next_to(chain, DOWN, buff=0.45)

            c.wait_until("arrays")
            self.play(*set_alpha(table, DIMMED), run_time=1.0)
            c.wait_until("hard to code")
            rt = min(2.0, 0.9 * c.until("lists"))
            sweep_clear(self, span(FadeIn(strip), 0.5, 0.85, rt), span(FadeIn(vals), 0.55, 0.9, rt),
                        span(FadeIn(hard, shift=0.25 * DOWN), 0.65, 1.0, rt), run_time=rt)
            c.wait_until("lists")
            self.play(FadeIn(chain, shift=0.3 * UP), run_time=1.2)
            c.wait_until(own_word=nat)
            self.play(*appear(nat), run_time=1.0)
