"""Chapter 7, scene 6: recap of the solutions, the five-sort scoreboard, next lecture, end card.
Clips c7.recap.1 – c7.recap.3.

Plan
- c7.recap.1: {recap} four DIM tile frames (2 x 2); each filled on its mark with the visual that
  taught it, its short line under it: {r1} s2's staircase() + three_chains(); {r2} s3's select_code()
  + dups_reply(), the pair (m, rest) flashed; {r3} s4's reversed rows only, re-stacked
  tighter so the cells and pass labels read at ~20 (no creep tag); select rewrapped to 6 lines; {r4} s5's rule_pair().
- c7.recap.2: {board} the grid sweeps out, s4's bubble_board() (time column kept) comes in, scaled
  0.85 to leave a tag column on the right; {slow} RED O(n^2) tags on insertion / selection / bubble;
  {fast} GREEN O(n log n) on quicksort / merge sort, their random counts and the floor value flash.
- c7.recap.3: {next} the board shrinks to the top and dims; "Next lecture: Datatypes and Trees";
  ch6 s6's vehicle_reply() on "define types", binary_tree() on "build trees". {end} hold; the end
  card stays ~8 s after the last word, then fades.
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

S2 = load_scene("ch7_s2_selcost")
S3 = load_scene("ch7_s3_selcode")
S4 = load_scene("ch7_s4_bubcost")
S5 = load_scene("ch7_s5_bubcode")
R6 = load_scene("ch6_s6_recap")

TILE_X = (-3.4, 3.4)
TILE_Y = (1.875, -1.875)
TILE_W, TILE_H = 6.5, 3.45
PIC_W, PIC_H = 6.0, 2.35
LINE = 30


def fit(m, w, h):
    s = min(w / m.width, h / m.height)
    m.scale(s, scale_stroke=True)
    return m


class Tile:
    def __init__(self, col, row):
        self.c = np.array([TILE_X[col], TILE_Y[row], 0])
        self.frame = RoundedRectangle(corner_radius=0.12, width=TILE_W, height=TILE_H) \
            .set_stroke(DIM, 1.5).move_to(self.c)

    def place(self, pic, w=PIC_W, h=PIC_H, dy=0.32):
        fit(pic, w, h)
        return pic.move_to(self.c + UP * dy)

    def text(self, s, color=FG):
        t = T(s, LINE, color)
        if t.width > TILE_W - 0.4:
            t.scale_to_fit_width(TILE_W - 0.4)
        return t.move_to(self.c + DOWN * (TILE_H / 2 - 0.32))


# select, wrapped so the tile can show it at ~20 (same code as s3's, if/then/else on their own lines)
SELECT_WRAPPED = ("let rec select m rest = function\n"
                  "  | [] -> (m, rest)\n"
                  "  | x::xs ->\n"
                  "      if x <= m\n"
                  "      then select x (m::rest) xs\n"
                  "      else select m (x::rest) xs")


def select_wrapped():
    code = Code(SELECT_WRAPPED, size=28)
    for k in range(3):
        code.find("select", nth=k).set_color(YELLOW)
    return code


def reversed_rows(pitch=0.68, size=32):
    """s4's reversed rows (the 9 rides to the end in row one, the YELLOW 3 creeps forward),
    re-stacked at a tighter pitch with larger labels so they read inside a tile."""
    pr = S4.pass_rows()
    rows = pr.rev_rows
    for k, ch in enumerate(rows):
        ch.shift(UP * (S4.REV_YS[0] - k * pitch - ch.get_y()))
    labs = [T(f"pass {k}", size, DIM).next_to(ch, LEFT, buff=0.4) if k else
            T("reversed", size, DIM).next_to(ch, LEFT, buff=0.4) for k, ch in enumerate(rows)]
    return VGroup(*rows, *labs)


def until(c, cue=None, frac=0.6, lo=0.6, hi=1.5):
    return max(lo, min(hi, frac * c.until(cue)))


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)          # the end card, held still; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- c7.recap.1
    def clip1(self):
        with self.say("c7.recap.1") as c:
            tiles = [Tile(0, 0), Tile(1, 0), Tile(0, 1), Tile(1, 1)]
            self.play(LaggedStart(*[FadeIn(t.frame) for t in tiles], lag_ratio=0.2),
                      run_time=min(1.0, c.until("r1")))

            # r1: the staircase beside the three chains
            c.wait_until("r1")
            t = tiles[0]
            stair, chains = S2.staircase(), S2.three_chains()
            pic = VGroup(stair, chains).arrange(RIGHT, buff=0.45)
            t.place(pic, 6.1, 2.65, 0.25)
            self.play(*appear(stair, chains, shift=None, lag=0.4), run_time=1.6)  # early: recalled picture, its labels are not read
            l1 = t.text("n(n − 1)/2, whatever the order", GOLD)
            c.wait_until("whatever the order")
            self.play(*appear(l1), run_time=1.0)

            # r2: select and its pair, the duplicates kept
            c.wait_until("r2")
            t = tiles[1]
            code, reply = select_wrapped(), S3.dups_reply(28)
            pic = VGroup(code, reply).arrange(DOWN, buff=0.25)
            t.place(pic, 6.1, 2.62, 0.3)
            self.play(*appear(code, shift=None), run_time=1.2)
            pair = code.find("(m, rest)")
            c.wait_until("the smallest item")
            self.play(FlashAround(pair, run_time=1.5, time_width=1.5), *recolor(pair, YELLOW))
            c.wait_until("so repeats survive")
            l2 = t.text("a pair: every copy survives", GREEN)
            self.play(*appear(reply, shift=None), *appear(l2), run_time=1.2)

            # r3: the pass rows, the 9 riding to the end; the reversed list's 3 creeping forward
            c.wait_until("r3")
            t = tiles[2]
            rev = reversed_rows()
            t.place(rev, 6.1, 2.55, 0.3)
            rows, labs = rev[:6], rev[6:]
            self.play(*appear(*rows, shift=None, lag=0.15), run_time=1.4)  # early: recalled picture, pass labels not read
            c.wait_until("comparisons each")
            self.play(*appear(*labs, shift=None, lag=0.1), run_time=1.2)  # early: recalled labels, not read
            l3 = t.text("≤ n passes of n − 1  ·  sorted: n − 1", GOLD)
            c.wait_until("one pass")
            self.play(*appear(l3), run_time=1.0)

            # r4: <= over the struck-through <
            c.wait_until("r4")
            t = tiles[3]
            rp = S5.rule_pair(56)
            fit(rp, PIC_W, PIC_H * 0.85)
            rp.move_to(t.c + UP * 0.32)
            l4 = t.text("swap only when x > y", GREEN)
            self.play(*appear(rp, shift=None), run_time=1.2)
            self.play(*appear(l4), run_time=1.0)

    # ---------------------------------------------------------------- c7.recap.2
    def clip2(self):
        with self.say("c7.recap.2") as c:
            sb = S4.bubble_board(ratios=False)
            sb.scale(0.85).to_edge(LEFT, buff=0.5).move_to([sb.get_x(), 0.0, 0])
            self.sb = sb
            sweep_clear(self, *appear(sb, shift=None), run_time=2.0)  # early: the board shown whole, then walked

            rows_y = [sb.row_labels[r].get_y() for r in range(3)] + [sb.sel_row[0].get_y(),
                                                                     sb.bub_row[0].get_y()]
            tag_x = (sb.get_right()[0] + 6.6) / 2

            def tag(s, col, r):
                return MathTex(s, font_size=40, color=col).move_to([tag_x, rows_y[r], 0])

            slow = [tag(r"O(n^2)", RED, r) for r in (0, 3, 4)]
            c.wait_until("slow")
            self.play(*appear(*slow, shift=None, lag=0.3), run_time=1.4)
            self.play(*flash([sb.cells[0][0], sb.sel_row[1], sb.bub_row[1]], color=RED,
                             run_time=1.5, time_width=1.5))

            fast = [tag(r"O(n\log n)", GREEN, r) for r in (1, 2)]
            c.wait_until("fast")
            self.play(*appear(*fast, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("close to the floor")
            self.play(*flash([sb.cells[1][0], sb.cells[2][0], sb.floor_value], color=GREEN,
                             run_time=1.5, time_width=1.5))
            self.tags = slow + fast

    # ---------------------------------------------------------------- c7.recap.3
    def clip3(self):
        with self.say("c7.recap.3") as c:
            board = VGroup(self.sb, *self.tags)
            self.play(board.animate.scale(0.55).to_edge(UP, buff=0.45).set_opacity(DIMMED),
                      run_time=1.4)
            nt = T("Next lecture: Datatypes and Trees", 46, t2c={"Datatypes and Trees": YELLOW})
            nt.move_to(UP * 0.15)
            self.play(*appear(nt), run_time=1.0)

            veh = R6.vehicle_reply(30).move_to(DOWN * 0.95)
            c.wait_until("define types")
            self.play(*appear(veh, shift=None), run_time=1.2)

            tree = R6.binary_tree(radius=0.27, dx=0.85, dy=0.68)
            tree.move_to(DOWN * 2.4)
            c.wait_until("build trees")
            self.play(*appear(tree, shift=None), run_time=1.2)
            c.wait_until("end")
