"""Chapter 6, scene 1: hook: part six's title, the scoreboard full, which sort is best? Clips c6.hook.1 – c6.hook.2.

STATUS: phase 2, complete. open_card() (ch5's end card, opened on here), bucket_row()/num_tile()
(scene 3's radix pieces), handover_shot() (scene 2 opens on it). {last}: running chain, GOLD cut,
take/drop halves lift apart, right half sorts, zipper into 3 -> 4 -> 5 -> 7 -> 9 -> [] + tick.
{always}: chain shrinks up over ch4 s2's recursion_tree(), GOLD O(n log n). {slower}/{safe}: two
time cards, "nearly 3 times as fast", the notes' verdict; clip 2's first play sweeps it into the board.
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
from lib.paths import load_scene  # noqa: E402

from scenes.ch1_s4_contest import SB_TALLY, make_scoreboard  # noqa: E402

TITLE_Y = 3.3          # the end-card title's y (ch2 s7's "Next: quicksort")
FILLED = (("25,146,194", "174 s"), ("158,058", "0.53 s"), ("120,392", "1.4 s"))


# ------------------------------------------------------------------ radix pieces (scene 3 imports these)
def bucket_row(color=BLUE, pitch=1.2, width=1.0, height=0.9, label_size=40):
    """Ten open-topped buckets in a row, labelled 0..9 underneath, centred on ORIGIN.

    Returns a VGroup(buckets, labels) with attributes:
      buckets  VGroup of 10 U-shaped VMobjects (stroke `color`, 4), `width` x `height`, at pitch `pitch`.
      labels   VGroup of 10 T `label_size` digits "0".."9" (colour `color`), 0.15 under each bucket.
      slot(i)  -> the point where a tile resting in bucket i has its bottom centre (the floor + 0.06).
    Default size: 11.8 wide, ~1.4 tall.
    """
    buckets = VGroup()
    for i in range(10):
        x = (i - 4.5) * pitch
        b = VMobject().set_points_as_corners([
            [x - width / 2, height / 2, 0], [x - width / 2, -height / 2, 0],
            [x + width / 2, -height / 2, 0], [x + width / 2, height / 2, 0]])
        b.set_stroke(color, 4)
        buckets.add(b)
    labels = VGroup(*[T(str(i), size=label_size, color=color).next_to(b, DOWN, buff=0.15)
                      for i, b in enumerate(buckets)])
    row = VGroup(buckets, labels)
    row.buckets = buckets
    row.labels = labels

    def slot(i):
        b = row.buckets[i]
        return np.array([b.get_x(), b.get_bottom()[1] + 0.06 * b.height / height, 0])
    row.slot = slot
    return row


def num_tile(n, size=40):
    """A GOLD number tile for a two-digit n: rounded box 0.9 x 0.7 (GOLD stroke 3, BG fill),
    digits Mono `size` GOLD. Attributes: .box, .text (the Mono), .digits (= .text, 2 glyphs),
    .tens, .ones (single glyphs; e.g. `tile.ones.animate.set_color(YELLOW)`), .n."""
    box = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.7)
    box.set_stroke(GOLD, 3).set_fill(BG, 1)
    text = Mono(f"{n:02d}", size=size, color=GOLD).move_to(box)
    tile = VGroup(box, text)
    tile.box, tile.text, tile.digits = box, text, text
    tile.tens, tile.ones = text[0], text[1]
    tile.n = n
    return tile


def place_tile(tile, row, i):
    """Rest `tile` on the floor of bucket i of `row` (any scale)."""
    return tile.move_to(row.slot(i), aligned_edge=DOWN)


# ------------------------------------------------------------------ the filled scoreboard
def filled_board():
    """make_scoreboard(bound="118,458") with all six cells as ch2–ch5 leave them (GOLD T 44)."""
    sb = make_scoreboard(bound="118,458")
    for r, vals in enumerate(FILLED):
        for col, val in enumerate(vals):
            sb.cells[r].submobjects[col] = T(val, 44, GOLD).move_to(sb.cells[r][col])
    return sb


def fit_board(sb, top, bottom, true_tally=True):
    """Scale the board to span y = top .. bottom (centred at x = 0); the DIM tally tag is
    re-set so it stays at true size 28 (min secondary-text size) at its scaled place."""
    sb.scale((top - bottom) / sb.height)
    sb.move_to([0, (top + bottom) / 2, 0])
    if not true_tally:
        return sb
    old = sb.tally_tag
    new = T(SB_TALLY, size=28, color=DIM).move_to(old)
    old.become(new)
    return sb


# ------------------------------------------------------------------ ch5's end card / this scene's first frame
def open_card():
    """The card ch5's last scene ends on and this scene opens on (static, deterministic).

    Attributes: .title, .board, .buckets, .tiles, .tag (see the report / below)."""
    title = T("Next: which sort is best?", 52, t2c={"which sort is best?": YELLOW}).move_to(UP * TITLE_Y)

    sb = filled_board()
    fit_board(sb, 2.6, -2.05, true_tally=False)   # scaled whole, as ch2 s7's end card

    row = bucket_row(color=DIM).scale(0.75)
    tag = T("no comparisons", 34, GOLD)
    gap = 0.4
    total = row.width + gap + tag.width
    row.move_to([-total / 2 + row.width / 2, -3.6 + row.height / 2, 0])
    tag.next_to(row.buckets, RIGHT, buff=gap)

    tiles = VGroup()
    for n in (53, 19, 51):
        t = num_tile(n).scale(0.75)
        place_tile(t, row, n % 10)
        tiles.add(t)

    card = VGroup(title, sb, row, tiles, tag)
    card.title, card.board, card.buckets, card.tiles, card.tag = title, sb, row, tiles, tag
    return card


# ------------------------------------------------------------------ the last frame (scene 2 opens on it)
def handover_shot():
    """s1's last frame: the filled board, YELLOW question above, two DIM tags under it.
    Attributes: .board, .question, .tags (VGroup), .tag_radix, .tag_ex."""
    question = T("Which sort is best?", 52, YELLOW).move_to(UP * TITLE_Y)
    sb = filled_board()
    fit_board(sb, 2.76, -2.76)
    tag_radix = T("a sort with no comparisons", 34, DIM)
    tag_ex = T("4 exercises", 34, DIM)
    tags = VGroup(tag_radix, tag_ex).arrange(RIGHT, buff=1.4).move_to(DOWN * 3.38)
    shot = VGroup(sb, question, tags)
    shot.board, shot.question, shot.tags = sb, question, tags
    shot.tag_radix, shot.tag_ex = tag_radix, tag_ex
    return shot



# ------------------------------------------------------------------ {last}: split and zip (ch5 s4 / s2)
RUN = [3, 5, 9, 4, 7]
S = 0.75               # chain scale in the recap
ROW_T, ROW_B = 1.35, -1.35   # the halves' rows after the split


def chain(vals, s=S):
    """ConsChain scaled by s, values kept readable (as ch5 s2's Zipper)."""
    ch = ConsChain(list(vals)).scale(s)
    k = max(1.0, 31 / (42 * s))
    for m in [cl.label for cl in ch.cells] + [ch.nil.label]:
        m.scale(k)
    return ch


def at_cell(ch, i, pt):
    """Shift chain ch so its cell i is centred on pt."""
    return ch.shift(np.array(pt) - ch.cells[i].get_center())


def path(start, end, horizontal_first=True):
    mid = [end[0], start[1], 0] if horizontal_first else [start[0], end[1], 0]
    return VMobject().set_points_as_corners([start, mid, end])


class HookScene(NarratedScene):
    def construct(self):
        card0 = open_card()
        self.add(card0)                      # ch5's last frame: an invisible cut
        self.wait(0.7)

        card = title_card("Part 6 · Which sort? And exercises")
        with self.say("c6.hook.1") as c:
            # {title}: the end card clears into the title card
            sweep_clear(self,  # early: the title card is shown whole as the line starts
                        time_span(FadeIn(card.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(card.rule), 0.6, 1.4), run_time=1.4)
            self.play(*appear(card.course, card.part, lag=0.4), run_time=1.2)  # early: title card
            self.recap(c, card)

        shot = handover_shot()
        with self.say("c6.hook.2", gap=0) as c:
            # {board}: the recap clears (first half), the full scoreboard arrives (second half)
            sweep_clear(self, *appear(shot.board, shift=None), run_time=1.6)
            c.wait_until("which")
            self.play(*appear(shot.question), run_time=1.0)
            c.wait_until("more")
            c.wait_until(own_word=shot.tag_radix)
            self.play(*appear(shot.tag_radix), run_time=1.0)
            c.wait_until(own_word=shot.tag_ex)
            self.play(*appear(shot.tag_ex), run_time=1.0)
        self.wait(1.0)                       # hold the handover shot into scene 2

    # ---------------------------------------------------------------- c6.hook.1 after {title}
    def recap(self, c, card):
        run = chain(RUN).move_to(ORIGIN)
        xs = [cl.get_x() for cl in run.cells]
        nil_x = run.nil.get_x()

        # {last}: the title card goes, the running chain arrives
        c.wait_until("last")
        rt = min(1.6, max(1.0, 0.95 * c.until("split")))
        self.play(*during(disappear(card.title, card.rule, card.course, card.part), 0, 0.45),
                  *during(appear(run, shift=None), 0.5, 1.0), run_time=rt)

        # split: the GOLD cut after cell 2
        c.wait_until("split")
        x_cut = (run.cells[1].ptr.get_right()[0] + run.cells[2].box.get_left()[0]) / 2
        cut = DashedLine([x_cut, 0.75, 0], [x_cut, -0.75, 0], dash_length=0.12, color=GOLD, stroke_width=5)
        self.play(GrowFromCenter(cut), run_time=min(0.9, max(0.4, 0.9 * c.until("take"))))

        # take / drop: the halves lift apart, labelled
        L = at_cell(chain([3, 5]), 0, [xs[0], ROW_T, 0])
        R = at_cell(chain([9, 4, 7]), 0, [xs[2], ROW_B, 0])
        tk = Mono("take 2 xs", 32, t2c={"take": YELLOW, "2": GOLD}).next_to(VGroup(*L.cells), UP, buff=0.35)
        dp = Mono("drop 2 xs", 32, t2c={"drop": YELLOW, "2": GOLD}).next_to(VGroup(*R.cells), DOWN, buff=0.35)
        c.wait_until("take")
        up_parts = [run.cells[0], run.cells[1], run.arrows[0]]
        dn_parts = [run.cells[2], run.cells[3], run.cells[4], *run.arrows[2:], run.nil]
        rt = min(1.6, max(1.2, 0.95 * c.until("merged")))
        self.play(*during([FadeOut(cut), FadeOut(run.arrows[1])], 0, 0.3),
                  *during([m.animate.shift(UP * ROW_T) for m in up_parts], 0.1, 0.7),
                  *during([m.animate.shift(UP * ROW_B) for m in dn_parts], 0.1, 0.7),
                  *during([FadeIn(L.nil)], 0.6, 0.9),
                  *during(appear(tk, dp, lag=0.3), 0.55, 1.0), run_time=rt)
        self.remove(*run.get_family(), L.nil)
        self.add(L, R)

        # merged the two sorted halves: [9; 4; 7] sorts itself, then the zipper
        c.wait_until("merged")
        Rs = at_cell(chain([4, 7, 9]), 0, [xs[2], ROW_B, 0])
        self.play(*swap(R, Rs), FlashAround(L, run_time=1.0, time_width=1.5),
                  run_time=min(0.9, max(0.7, c.until("halves"))))

        out = chain([3, 4, 5, 7, 9]).move_to(ORIGIN)
        tick = check_mark(GREEN).move_to(out.nil.get_center() + UP * 0.85)
        moves = [  # (mobject, end point, window)
            (L.cells[0], [xs[0], 0, 0], (0.08, 0.4)),
            (Rs.cells[0], [xs[1], 0, 0], (0.18, 0.52)),
            (L.cells[1], [xs[2], 0, 0], (0.3, 0.64)),
            (Rs.cells[1], [xs[3], 0, 0], (0.42, 0.74)),
            (Rs.cells[2], [xs[4], 0, 0], (0.5, 0.82)),
            (Rs.nil, [nil_x, 0, 0], (0.55, 0.85)),
        ]
        anims = during([FadeOut(m) for m in (*L.arrows, L.nil, *Rs.arrows, tk, dp)], 0, 0.15)
        for m, end, (a, b) in moves:
            anims += during([MoveAlongPath(m, path(m.get_center(), np.array(end, dtype=float)))], a, b)
        anims += during([GrowArrow(ar) for ar in out.arrows], 0.8, 0.95)
        anims += during([FadeIn(tick, scale=0.5)], 0.85, 1.0)
        self.play(*anims, run_time=1.8)
        self.remove(*L.get_family(), *Rs.get_family(), *out.arrows)
        self.add(out)

        # {always}: the chain shrinks up; ch4's balanced tree beneath it
        head = VGroup(out, tick)
        self.remove(out, tick)
        self.add(head)
        tree = load_scene("ch4_s2_average").recursion_tree().scale(0.75).move_to(UP * 0.25)
        big_o = VGroup(MathTex(r"O(n \log n)", font_size=52, color=GOLD),
                       T(", even at worst", 42, GOLD)).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        big_o.move_to(DOWN * 2.55)
        c.wait_until("always")
        self.play(*during([head.animate.scale(0.55).move_to(UP * 3.2)], 0, 0.6),
                  *during(appear(*tree.rows, tree.dots, lag=0.2, shift=None), 0.3, 1.0), run_time=2.0)
        self.play(*flash(tree.rows[1]), run_time=1.2)
        c.wait_until("worst case")
        self.play(*appear(big_o), run_time=1.0)

        # {slower}: two GOLD times side by side
        def timecard(name, t, x):
            g = VGroup(T(name, 40), T(t, 64, GOLD)).arrange(DOWN, buff=0.3).move_to([x, 0.5, 0])
            return g
        ms = timecard("merge sort", "1.4 s", -4.4)
        qs = timecard("quicksort", "0.53 s", 4.4)
        fast = T("nearly 3 times as fast", 34).move_to([0, ms[1].get_y(), 0])
        c.wait_until("slower")
        sweep_clear(self, big_o.animate.scale(0.75).move_to(UP * 3.2), *appear(ms), keep=[big_o],
                    run_time=1.6)
        c.wait_until(own_word=qs[0])
        self.play(*appear(qs), run_time=1.0)
        c.wait_until("nearly")
        self.play(*appear(fast), run_time=1.0)

        # {safe}: the notes' verdict under them
        verdict = T("Merge sort is safe but slow.", 52, t2c={"safe": GREEN, "slow": RED}).move_to(DOWN * 2.3)
        c.wait_until("safe")
        self.play(*appear(verdict), run_time=1.0)  # early: its words follow within 2 s
        c.wait_until()
