"""Chapter 4, scene 1: Hook. Clips c4.hook.1 – c4.hook.3.

Plan
- opening: open_card() (ch3's end card: "Next: how good is quicksort?", small scoreboard, pivot
  tree with RED empty left branch and YELLOW "?", struck-through append code) held 0.7 s, then
  the title card.
- c4.hook.1: title card; {last} the card returns without its title; {fast} tree and code fade,
  the board grows to full size; quicksort's cells pulse on their numbers, "174 s" turns RED.
- c4.hook.2: {tree} board shrinks to the top-left, the pivot tree takes the centre, code back in
  its corner; {lopsided} GOLD caption "lopsided", "?" pulses; "0" (RED) on the empty left branch,
  "4" on the right, each on its words.
- c4.hook.3: {ask} board leaves, tree shrinks to the lower half; YELLOW "Why is it usually so
  fast?", then "What if every split is lopsided?", then DIM "Then: quicksort without @" with the
  struck-through code sliding in beside it. Ends on an empty frame.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.paths import load_scene  # noqa: E402
from lib.titles import title_card  # noqa: E402

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402

TITLE_Y = 3.3
SB_SMALL_W = 6.4                    # open card: board width
SB_SMALL_C = (-3.4, 0.25)          # open card: board centre
TREE_C = (3.6, 0.0)                 # open card: tree centre
TREE_H = 4.4                        # open card: tree height (with its "?")
CODE_SIZE = 28


# ── pieces ────────────────────────────────────────────────────────────────────
def scoreboard():
    """The board at full size: insertion sort and quicksort filled, quicksort's row lit YELLOW."""
    sb = make_scoreboard(bound="118,458")
    for row, vals in ((0, ("25,146,194", "174 s")), (1, ("158,058", "0.74 s"))):
        for col, val in enumerate(vals):
            v = T(val, 44, GOLD).move_to(sb.cells[row][col])
            sb.cells[row].submobjects[col] = v
    qrow = VGroup(sb.row_labels[1], *sb.cells[1])
    lit = Rectangle(width=sb.width + 0.3, height=qrow.height + 0.3)
    lit.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).move_to([sb.get_x(), qrow.get_y(), 0])
    lit.set_z_index(-1)
    sb.add(lit)
    sb.lit = lit
    return sb


def pivot_tree():
    """ch3 s6's pivot tree (call_tree circle form), pivots YELLOW, the root's empty left branch
    RED, a YELLOW "?" over the root. .ct .root .left_edge (root's empty left stub) .right_edge
    (root to 7) .q"""
    ct = load_scene("ch3_s6_trace").call_tree([3, 5, 9, 4, 7], form="circles")
    for nd in ct.nodes:
        nd.pivot_glyph.set_color(YELLOW)
    root = ct.root
    left = root.stubs["left"].set_color(RED)
    right = next(nd for nd in ct.nodes if nd.pivot == 7).edge
    q = T("?", 64, YELLOW).next_to(root.body, UP, buff=0.2)
    tree = VGroup(ct, q)
    tree.ct, tree.root, tree.left_edge, tree.right_edge, tree.q = ct, root, left, right, q
    return tree


def append_code():
    code = Code("(quick l) @ (a :: quick r)", size=CODE_SIZE)
    code.set_color(DIM)
    code.find("@").set_color(GOLD)
    strike = Line(code.get_left() + 0.12 * LEFT, code.get_right() + 0.12 * RIGHT).set_stroke(DIM, 3)
    g = VGroup(code, strike)
    g.code, g.strike = code, strike
    return g


def card_parts():
    """Board, tree and code laid out as on the opening card (no title)."""
    sb = scoreboard()
    sb.full_scale = 1.0
    sb.scale(SB_SMALL_W / sb.width)
    sb.move_to([*SB_SMALL_C, 0])
    tree = pivot_tree()
    tree.scale(TREE_H / tree.height).move_to([*TREE_C, 0])
    code = append_code()
    code.move_to([0, -3.15, 0])
    return sb, tree, code


def open_card():
    """ch4's first frame (ch3's end card): "Next" title, small board, pivot tree, struck code."""
    title = T("Next: how good is quicksort?", 52, t2c={"how good is quicksort?": YELLOW})
    title.move_to(UP * TITLE_Y)
    sb, tree, code = card_parts()
    card = VGroup(title, sb, tree, code)
    card.title, card.sb, card.tree, card.code = title, sb, tree, code
    return card


PULSE = (lambda t: there_and_back((2 * t) % 1.0))


class QuickCostHook(NarratedScene):
    def construct(self):
        self.opening()
        self.clip_last()
        self.clip_tree()
        self.clip_ask()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── before the first line: the opening card, then the title card ─────────────
    def opening(self):
        old = open_card()
        self.card = card = title_card("Part 4 · How good is quicksort?")
        self.add(old)
        self.wait(0.7)
        self.play(*during([FadeOut(old)], 0, 0.45),  # early: title card
                  *during([FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule)], 0.45, 1.0),
                  run_time=1.6)

    # ── c4.hook.1 ────────────────────────────────────────────────────────────────
    def clip_last(self):
        card = self.card
        sb, tree, code = card_parts()
        self.sb, self.tree, self.code = sb, tree, code
        small_w = sb.width

        with self.say("c4.hook.1") as c:
            self.play(FadeIn(card.course, shift=0.2 * DOWN),  # early: title card
                      time_span(FadeIn(card.part, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            c.wait_until("last")
            sweep_clear(self, time_span(FadeIn(sb, shift=0.2 * UP), 0.6, 1.4),  # early: the card returns whole
                        time_span(FadeIn(tree), 0.8, 1.6), time_span(FadeIn(code), 1.0, 1.8),
                        run_time=1.8)
            c.wait_until("fast")
            sb.generate_target()
            sb.target.scale(12.4 / small_w).move_to([0, -0.15, 0])
            self.play(*during([FadeOut(tree), FadeOut(code)], 0, 0.45),
                      *during([MoveToTarget(sb)], 0.3, 1.0), run_time=1.8)
            c.wait_until("hundred and fifty-eight")
            self.play(sb.cells[1][0].animate(rate_func=PULSE).scale(1.3),
                      FlashAround(sb.lit, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("zero point seven four")
            self.play(sb.cells[1][1].animate(rate_func=PULSE).scale(1.3), run_time=1.2)
            c.wait_until("insertion sort")
            self.play(sb.cells[0][1].animate.set_color(RED),
                      FlashAround(sb.cells[0][1], color=RED, time_width=1.5),
                      run_time=min(1.5, c.until()))

    # ── c4.hook.2 ────────────────────────────────────────────────────────────────
    def clip_tree(self):
        sb, tree, code = self.sb, self.tree, self.code
        zero = T("0", 44, RED)
        four = T("4", 44, FG)
        cap = T("lopsided", 44, GOLD)
        self.extras = VGroup(zero, four, cap)

        with self.say("c4.hook.2") as c:
            sb.generate_target()
            sb.target.scale(5.0 / sb.width)
            sb.target.move_to([-6.6 + sb.target.width / 2, 3.5 - sb.target.height / 2, 0])
            tree.scale(5.7 / tree.height).move_to([2.0, 0.5, 0])
            code.move_to([6.6 - code.width / 2, -3.25, 0])
            self.play(*during([MoveToTarget(sb)], 0, 0.6),
                      *during([FadeIn(tree, scale=0.9)], 0.4, 1.0),
                      *during([FadeIn(code)], 0.6, 1.0), run_time=1.8)
            c.wait_until("lopsided")
            zero.next_to(tree.left_edge.get_end(), DOWN + LEFT, buff=0.12)
            four.next_to(tree.right_edge.get_center(), UP + RIGHT, buff=0.1)
            cap.next_to(zero, DOWN, buff=0.4).align_to(zero, LEFT)
            self.play(*appear(cap), FlashAround(tree.q, color=YELLOW, time_width=1.5),
                      tree.q.animate(rate_func=PULSE).scale(1.35), run_time=1.5)
            c.wait_until("nothing went left")
            self.play(*appear(zero), VShowPassingFlash(tree.left_edge.copy().set_stroke(RED, 10),
                                                        time_width=0.6), run_time=1.5)
            c.wait_until("all four")
            self.play(*appear(four), VShowPassingFlash(tree.right_edge.copy().set_stroke(YELLOW, 8),
                                                        time_width=0.6), run_time=min(1.5, c.until()))

    # ── c4.hook.3 ────────────────────────────────────────────────────────────────
    def clip_ask(self):
        sb, tree, code = self.sb, self.tree, self.code
        q1 = T("Why is it usually so fast?", 44, YELLOW).move_to(UP * 3.25)
        q2 = T("What if every split is lopsided?", 44, YELLOW).move_to(UP * 2.4)
        q3 = T("Then: quicksort without @", 36, DIM)
        code_t = code.copy().scale(1.0)
        row = VGroup(q3, code_t).arrange(RIGHT, buff=0.6).move_to(UP * 1.6)
        q3.align_to(code_t.code, DOWN)
        lower = VGroup(tree, self.extras)

        with self.say("c4.hook.3", gap=3.5) as c:
            # final size and height at once; parked left of the code's path until the code has risen
            top = code_t.get_bottom()[1] - 0.4
            bottom = -3.35
            lower.generate_target()
            lower.target.scale((top - bottom) / lower.height)
            lower.target.move_to([-0.15 - lower.target.width / 2, (top + bottom) / 2, 0])
            self.play(*during([FadeOut(sb)], 0, 0.45),
                      *during([MoveToTarget(lower)], 0.2, 1.0), run_time=1.5)
            c.wait_until(own_word=q1)
            self.play(*appear(q1), run_time=1.0)
            c.wait_until(own_word=q2)
            self.play(*appear(q2), run_time=1.0)
            c.wait_until("later", own_word=q3)
            # the code rises beside q3, then the tree slides under the questions (x = 0)
            self.play(*during(appear(q3), 0, 0.5), *during([code.animate.move_to(code_t)], 0, 0.55),
                      *during([lower.animate.set_x(0)], 0.55, 1.0), run_time=2.2)
