"""Chapter 6, scene 2: the full scoreboard, a sorted-input column, O(n^2) is catastrophic, match the
algorithm to the application. Clips c6.sum.1 – c6.sum.4.

Opens on ch6 s1's handover_shot(). Exports board3() (ch7 s2, s4, s6 reuse it).
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch1_s4_contest import SB_ROWS, SB_TALLY  # noqa: E402

S1 = load_scene("ch6_s1_hook")
FILLED = S1.FILLED

# ------------------------------------------------------------------ the three-column board (ch7 reuses it)
B3_LX = -6.5                       # left edge of the row labels
B3_XS = (-2.0, 1.55, 4.9)          # x centres of the three value columns
B3_HY = (2.85, 2.46)               # y of the two header lines
B3_RULE_Y = 1.62
B3_YS = (0.8, -0.4, -1.6)          # row y centres
B3_FLOOR_Y = -2.75
SORTED = (("9,999", GREEN), ("49,995,000", RED), ("64,608", GREEN))


def board3(stage="full", with_optimal=True):
    """The scoreboard with a third column "comparisons on / 10,000 sorted items", in frame
    coordinates (no scaling; spans x -6.5 .. 6.6, y 3.0 .. -2.9).

    Built from ch6 s1's filled_board() (same submobject order, every part re-set in place), so a
    two-column board can Transform into stage "two". Sizes: row labels YELLOW T 30, headers T 28,
    tally tag DIM T 28, cells GOLD T 40, floor label/value GOLD T 30.
    stage: "two"  the two-column relayout only (no col3, no optimal tag);
           "ask"  plus col3 header and three GOLD "?" cells;
           "full" col3 cells filled: GREEN "9,999", RED "49,995,000", GREEN "64,608".
    Attributes (as make_scoreboard): .rule .row_labels .col_headers (3 entries; [0] and [2] are
    two-line VGroups) .tally_tag .cells[r][c] (c = 0, 1, 2) .floor_line .floor_label .floor_value,
    plus .col3_header, .col3_cells (VGroup of the 3), .optimal (GOLD T 28 "O(n log n) is optimal"
    0.25 right of the floor line, in the group only when with_optimal and stage != "two").
    """
    sb = S1.filled_board()
    for i, lab in enumerate(sb.row_labels):
        lab.become(T(SB_ROWS[i], 30, YELLOW).move_to([B3_LX, B3_YS[i], 0], aligned_edge=LEFT))
    h1 = sb.col_headers[0]
    h1[0].become(T("comparisons on", 28).move_to([B3_XS[0], B3_HY[0], 0]))
    h1[1].become(T("10,000 random items", 28).move_to([B3_XS[0], B3_HY[1], 0]))
    sb.col_headers[1].become(T("DECstation time", 28).move_to([B3_XS[1], B3_HY[1], 0]))
    sb.tally_tag.become(T(SB_TALLY, 28, DIM).next_to(h1, DOWN, buff=0.16))
    sb.rule.become(Line([B3_LX, B3_RULE_Y, 0], [6.6, B3_RULE_Y, 0]).set_stroke(DIM, 2))
    for r, vals in enumerate(FILLED):
        for c, v in enumerate(vals):
            sb.cells[r][c].become(T(v, 40, GOLD).move_to([B3_XS[c], B3_YS[r], 0]))
    sb.floor_label.become(T("lower bound ≈", 30, GOLD).move_to([B3_LX, B3_FLOOR_Y, 0], aligned_edge=LEFT))
    sb.floor_value.become(T("118,458", 30, GOLD).next_to(sb.floor_label, RIGHT, buff=0.2))
    x0 = sb.floor_value.get_right()[0] + 0.35
    sb.floor_line.become(Line([x0, B3_FLOOR_Y, 0], [B3_XS[0] + 1.6, B3_FLOOR_Y, 0]).set_stroke(GOLD, 3))

    head3 = VGroup(T("comparisons on", 28), T("10,000 sorted items", 28))
    head3[0].move_to([B3_XS[2], B3_HY[0], 0])
    head3[1].move_to([B3_XS[2], B3_HY[1], 0])
    if stage == "full":
        col3 = VGroup(*[T(v, 40, col).move_to([B3_XS[2], y, 0]) for (v, col), y in zip(SORTED, B3_YS)])
    else:
        col3 = VGroup(*[T("?", 40, GOLD).move_to([B3_XS[2], y, 0]) for y in B3_YS])
    optimal = T("O(n log n) is optimal", 28, GOLD).next_to(sb.floor_line, RIGHT, buff=0.25)

    sb.col3_header, sb.col3_cells, sb.optimal = head3, col3, optimal
    if stage != "two":
        sb.col_headers.add(head3)
        for r in range(3):
            sb.cells[r].add(col3[r])
        if with_optimal:
            sb.add(optimal)
    return sb


# ------------------------------------------------------------------ small icons for the match rows
def dice(color=FG, side=0.62):
    face = RoundedRectangle(corner_radius=0.1, width=side, height=side).set_stroke(color, 3)
    d = side * 0.27
    pips = VGroup(*[Dot([x, y, 0], radius=0.05, color=color)
                    for x, y in ((-d, d), (d, d), (0, 0), (-d, -d), (d, -d))])
    return VGroup(face, pips)


def small_chain(values, scale=0.42, color=BLUE, size=28):
    """A ConsChain scaled down, its values and [] re-set at true size `size` (readable)."""
    ch = ConsChain(values, color=color).scale(scale)
    for cell in ch.cells:
        cell.label.become(value_label(cell.value, size).move_to(cell.box))
    ch.nil.label.become(Mono("[]", size, TEAL).move_to(ch.nil.label))
    return ch


def array_row(values, color=BLUE, side=0.6, size=28):
    boxes = VGroup(*[Square(side).set_stroke(color, 3) for _ in values]).arrange(RIGHT, buff=0)
    nums = VGroup(*[Mono(str(v), size, GOLD).move_to(b) for v, b in zip(values, boxes)])
    return VGroup(boxes, nums)


ICON_X = -3.15
TEXT_X = -0.3
MATCH_YS = (1.95, 0.45, -1.05, -2.55)


class Summary(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------------- the board, row by row
    def clip1(self):
        shot = S1.handover_shot()
        self.add(*shot.submobjects)
        board = self.board = shot.board
        with self.say("c6.sum.1") as c:
            full = S1.filled_board()
            full.row_labels.set_color(FG)
            self.play(*during(disappear(shot.question, shot.tags), 0, 0.45),
                      *during([Transform(board, full)], 0.4, 1),
                      run_time=min(2.0, c.until("optimal")))
            c.wait_until("optimal")
            floor = VGroup(board.floor_label, board.floor_value, board.floor_line)
            self.play(FlashAround(floor, color=GOLD, time_width=1.5),
                      VShowPassingFlash(board.floor_line.copy().set_stroke(YELLOW, 7), time_width=0.6),
                      run_time=1.6)
            self.opt = T("O(n log n) is optimal", 30, GOLD).next_to(board.floor_line, RIGHT, buff=0.25)
            c.wait_until("is optimal")
            self.play(*appear(self.opt), run_time=1.0)

            notes_txt = (("simple to code; too slow (quadratic)", {"quadratic": RED}),
                         ("fast on average; quadratic in worst case", {"quadratic": RED}),
                         ("optimal in theory; often slower than quicksort", {"optimal": GREEN}))
            cues = (("insertion", "seventy-four"), ("quick", "half a second"), ("merge", "One point four"))
            self.notes = []
            for r, ((txt, t2c), (mark, tcue)) in enumerate(zip(notes_txt, cues)):
                note = T(txt, 28, t2c=t2c)
                note.move_to([-6.0, board.row_labels[r].get_y() - 0.55, 0], aligned_edge=LEFT)
                self.notes.append(note)
                c.wait_until(mark)
                anims = recolor([board.row_labels[r]], YELLOW)
                if r > 0:
                    anims += recolor([board.row_labels[r - 1]], FG)
                self.play(*anims, run_time=0.8)
                c.wait_until(own_word=note)
                self.play(*appear(note), run_time=1.0)
                c.wait_until(tcue)
                self.play(FlashAround(board.cells[r][1], time_width=1.5), run_time=1.5)

    # -------------------------------------------------------------- the sorted column
    def clip2(self):
        board = self.board
        with self.say("c6.sum.2") as c:
            two = board3("two")
            ask = board3("ask")
            opt_t = board3("full").optimal
            self.play(*during(disappear(*self.notes), 0, 0.4),
                      *during([Transform(board, two), Transform(self.opt, opt_t)], 0.3, 1),
                      run_time=min(2.0, c.until("already sorted")))
            c.wait_until("already sorted")
            self.play(*appear(ask.col3_header, *ask.col3_cells, lag=0.2), run_time=1.4)  # early: the new column is shown as it is introduced, then filled
            self.col3 = list(ask.col3_cells)
            for r, cue in enumerate(("nine thousand", "forty-nine million", "sixty-four thousand")):
                c.wait_until(cue)
                v, col = SORTED[r]
                new = T(v, 40, col).move_to(self.col3[r])
                self.play(*swap(self.col3[r], new), run_time=1.2)
                self.col3[r] = new
            c.wait_until("flip")
            a, b = board.cells[1][0], self.col3[1]
            boxes = [SurroundingRectangle(m, color=YELLOW, buff=0.15).set_stroke(YELLOW, 3) for m in (a, b)]
            self.play(*[FadeIn(bx) for bx in boxes], run_time=1.0)
            arrow = CurvedArrow(boxes[0].get_bottom() + 0.05 * DOWN, boxes[1].get_bottom() + 0.05 * DOWN,
                                angle=0.35, color=YELLOW).set_stroke(width=4)
            self.play(Create(arrow), run_time=1.5)
            self.flip = (boxes, arrow)

    # -------------------------------------------------------------- n^2 is catastrophic: the table
    def clip3(self):
        with self.say("c6.sum.3") as c:
            c.wait_until("worst case")
            self.play(FlashAround(self.col3[1], color=RED, time_width=1.5), run_time=1.5)
            c.wait_until("N squared")
            gone = list(self.mobjects)
            title = T("O(n²) is catastrophic", 48, RED).move_to(UP * 3.3)
            self.play(*during([m.animate.shift(15 * LEFT) for m in gone], 0, 0.6),
                      *during(appear(title), 0.55, 1), run_time=2.2)  # early: the title lands as the board leaves, on "N squared is catastrophic"
            self.remove(*gone)
            self.title = title

            xs = (-4.6, -1.5, 1.6, 4.7)
            ys = (1.15, -0.05, -1.25)
            heads = [T(h, 34).move_to([x, ys[0], 0]) for h, x in zip(("complexity", "1 second", "1 minute", "1 hour"), xs)]
            rule = Line([-6.2, 0.65, 0], [6.2, 0.65, 0]).set_stroke(DIM, 2)
            rows = []
            for y, tex, nums in ((ys[1], r"n \log n", ("140", "4 895", "204 095")),
                                 (ys[2], r"n^2", ("31", "244", "1 897"))):
                row = [MathTex(tex, font_size=50).move_to([xs[0], y, 0])]
                row += [T(n, 44, GOLD).move_to([x, y, 0]) for n, x in zip(nums, xs[1:])]
                rows.append(row)
            tag = T("Lecture 2: one unit of cost takes 1 millisecond", 30, DIM).move_to(DOWN * 2.6)
            c.wait_until("table")
            self.play(*appear(rule, *heads, shift=None, lag=0.15), run_time=1.2)  # early: the table's header is shown whole, then walked
            self.play(*appear(*rows[0], *rows[1], shift=None, lag=0.08), run_time=1.4)
            c.wait_until("millisecond")
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("hour")
            col = Rectangle(width=2.6, height=3.35).move_to([xs[3], (ys[0] + ys[2]) / 2, 0])
            col.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.1).set_z_index(-1)
            self.play(FadeIn(col), *recolor([heads[3]], YELLOW), run_time=1.0)
            c.wait_until("two hundred thousand")
            self.play(*recolor([rows[0][3]], GREEN), FlashAround(rows[0][3], color=GREEN, time_width=1.5),
                      run_time=1.5)
            c.wait_until("just one thousand")
            self.play(*recolor([rows[1][3]], RED), FlashAround(rows[1][3], color=RED, time_width=1.5),
                      run_time=1.5)

    # -------------------------------------------------------------- match the algorithm to the application
    def clip4(self):
        with self.say("c6.sum.4") as c:
            question = T("Which sort is best?", 52, YELLOW).move_to(UP * 3.3)
            sweep_clear(self, *appear(question), run_time=1.6)
            answer = T("Match the algorithm to the application", 46, YELLOW).move_to(UP * 3.3)
            c.wait_until("match the algorithm")
            self.play(*swap(question, answer), run_time=1.2)

            def place(icon, text, y):
                icon.move_to([ICON_X, y, 0])
                text.move_to([TEXT_X, y, 0], aligned_edge=LEFT)

            # nearly sorted
            chain = small_chain([3, 4, 5, 7, 9], color=GREEN)
            l1 = T("nearly sorted: insertion sort", 36, t2c={"insertion sort": GREEN})
            l2 = T("quicksort", 32, RED)
            txt = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            place(chain, txt, MATCH_YS[0])
            strike = Line(l2.get_left() + 0.08 * LEFT, l2.get_right() + 0.08 * RIGHT).set_stroke(RED, 4)
            c.wait_until("nearly")
            self.play(FadeIn(chain), run_time=1.0)
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("quicksort")
            self.play(*appear(l2), run_time=0.8)
            self.play(GrowFromEdge(strike, LEFT), run_time=0.6)

            # never slow
            tree = S1_tree()
            t2 = T("never slow: merge sort", 36, t2c={"merge sort": GREEN})
            place(tree, t2, MATCH_YS[1])
            c.wait_until("guarantee")
            self.play(FadeIn(tree), run_time=1.0)
            c.wait_until(own_word=t2)
            self.play(*appear(t2), run_time=1.0)

            # random data
            shuf = small_chain([5, 9, 3, 7])
            die = dice()
            icon3 = VGroup(die, shuf).arrange(RIGHT, buff=0.25)
            r1 = T("random data: quicksort", 36, t2c={"quicksort": GREEN})
            r2 = T("(shuffle first)", 32, DIM)
            t3 = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            place(icon3, t3, MATCH_YS[2])
            c.wait_until("random")
            self.play(FadeIn(icon3), run_time=1.0)
            self.play(*appear(r1), run_time=1.0)
            c.wait_until("shuffling")
            self.play(*appear(r2), run_time=1.0)

            # arrays vs lists
            arr = array_row([5, 9, 3, 7, 4])
            lst = small_chain([5, 9, 3])
            a1 = T("arrays: quicksort in place", 36, t2c={"quicksort": GREEN})
            a2 = T("lists: merge sort", 36, t2c={"merge sort": GREEN})
            t4 = VGroup(a1, a2).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            t4.move_to([TEXT_X, MATCH_YS[3], 0], aligned_edge=LEFT)
            arr.move_to([ICON_X, a1.get_y(), 0])
            lst.move_to([ICON_X, a2.get_y(), 0])
            c.wait_until("arrays")
            self.play(FadeIn(arr), run_time=0.8)
            self.play(*appear(a1), run_time=1.0)
            c.wait_until("merge sort suits")
            self.play(FadeIn(lst), *appear(a2), run_time=1.0)
        self.wait(4.0)


def S1_tree():
    """ch4's balanced recursion tree, small (the match row's icon)."""
    t = load_scene("ch4_s2_average").recursion_tree(width=4.2, leaves=8, pitch=0.34, box_h=0.22)
    for row in t.rows:            # labels would be unreadably small: the tree's shape is the icon
        for node in row:
            node.remove(node.label)
    t.remove(t.dots)
    return t
