"""Chapter 7, scene 4: Exercise 5.3's solution, bubble sort's cost (passes as rows, n - 1 passes of
n - 1 comparisons, reversed / sorted / random input, the scoreboard row). Clips c7.bubcost.1 - 6.

Exports for ch7 s5 and the recap: bubble_board() (the five-row scoreboard as this scene leaves it)
and pass_rows() (the 3 5 9 4 7 chain's pass rows with the 9 riding, and the reversed list's rows
with the YELLOW 3). Counts checked with OCaml 5.4.1: 12 comparisons in 3 passes; reversed 20 in 5;
sorted 4 in 1; rs 99,990,000 in 10,000 passes (sorted rs 9,999; reversed rs 99,990,000).
ch7 s2's selsort_board() did not exist when this was built: the selection-sort row is built here
from ch6 s2's board3() (selsort_board_here()).
"""
# style: 2
import sys
from math import atan
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

K = load_scene("ch6_s4_hints1")          # the exercise-card kit
H2 = load_scene("ch6_s5_hints2")         # card_5_3, bracket_over
SUM = load_scene("ch6_s2_summary")       # board3
bracket_over = H2.bracket_over

RUNNING = [3, 5, 9, 4, 7]

# ── pass rows (the running chain) ────────────────────────────────────────────────
ROW_S, ROW_LAB = 0.6, 1.3
CX = -1.3
ROW_YS = (2.3, 0.95, -0.4, -1.75)
CHAIN_ROWS = ([3, 5, 9, 4, 7], [3, 5, 4, 7, 9], [3, 4, 5, 7, 9], [3, 4, 5, 7, 9])
CHAIN_GREEN = (0, 1, 2, 5)              # settled cells (the last k) per row

# ── reversed rows ────────────────────────────────────────────────────────────────
REV_S, REV_LAB = 0.55, 1.35
RCX = -1.3
REV_YS = tuple(2.8 - 1.1 * k for k in range(6))
REV_ROWS = ([9, 7, 5, 4, 3], [7, 5, 4, 3, 9], [5, 4, 3, 7, 9], [4, 3, 5, 7, 9], [3, 4, 5, 7, 9],
            [3, 4, 5, 7, 9])
REV_GREEN = (0, 1, 2, 3, 4, 5)

# ── the board ────────────────────────────────────────────────────────────────────
BOARD_YS = (1.1, 0.28, -0.54, -1.36, -2.18)
BOARD_FLOOR_Y = -2.98


def run_chain(values, s=ROW_S, lab=ROW_LAB):
    ch = ConsChain(values).scale(s)
    for cell in ch.cells:
        cell.label.scale(lab).set_z_index(1)
    ch.nil.scale(lab, about_edge=LEFT)     # [] back to a readable size
    return ch


def pass_label(k, chain, size=30):
    t = T(f"pass {k}", size=size, color=DIM)
    return t.next_to(chain, LEFT, buff=0.4)


def labs_of(ch):
    return sorted([c.label for c in ch.cells], key=lambda m: m.get_x())


def colour_static(ch, values, green_from, yellow=None):
    """Colour a freshly built row: cells from index green_from on GREEN; value `yellow` YELLOW."""
    for i, cell in enumerate(ch.cells):
        if i >= green_from:
            cell.box.set_stroke(GREEN)
            cell.label.set_color(GREEN)
        if yellow is not None and values[i] == yellow:
            cell.label.set_color(YELLOW)
    return ch


def rider_arrow(ch, a, b):
    y = ch.cells[a].get_top()[1] + 0.08
    return CurvedArrow([ch.cells[a].get_center()[0], y, 0], [ch.cells[b].get_center()[0], y, 0],
                       angle=-0.6, color=YELLOW, stroke_width=4, tip_length=0.2)


def pass_rows():
    """Static: .chain_rows (4 chains, ROW_YS) .chain_labels .rider (the 9's YELLOW arrow, row 1);
    .rev_rows (6 chains, REV_YS, the 3 YELLOW) .rev_labels ("reversed", "pass 1".."pass 5")
    .creep_tag ("1 place per pass"). Two layouts (not shown together): .chains, .reversed."""
    chains, clabs = [], []
    for k, (vals, y) in enumerate(zip(CHAIN_ROWS, ROW_YS)):
        ch = run_chain(vals).move_to([CX, y, 0])
        colour_static(ch, vals, 5 - CHAIN_GREEN[k])
        chains.append(ch)
        if k:
            clabs.append(pass_label(k, ch))
    rider = rider_arrow(chains[1], 2, 4)
    revs, rlabs = [], []
    for k, (vals, y) in enumerate(zip(REV_ROWS, REV_YS)):
        ch = run_chain(vals, REV_S, REV_LAB).move_to([RCX, y, 0])
        colour_static(ch, vals, 5 - REV_GREEN[k], yellow=3)
        revs.append(ch)
        rlabs.append(pass_label(k, ch, 28) if k else T("reversed", 28, DIM).next_to(ch, LEFT, buff=0.4))
    tag = creep_tag(revs)
    g = VGroup(VGroup(*chains, *clabs, rider), VGroup(*revs, *rlabs, tag))
    g.chains, g.reversed = g[0], g[1]
    g.chain_rows, g.chain_labels, g.rider = chains, clabs, rider
    g.rev_rows, g.rev_labels, g.creep_tag = revs, rlabs, tag
    return g


def creep_tag(revs):
    return T("1 place per pass", 30, YELLOW).move_to([2.45, REV_YS[1], 0], aligned_edge=LEFT)


def selsort_board_here():
    """ch6 s2's board3() re-spaced to five row slots, plus the YELLOW selection-sort row:
    random "49,995,000", time DIM "-", sorted RED "49,995,000". .sel_row = (label, c0, c1, c2)."""
    sb = SUM.board3("full")
    for r in range(3):
        dy = BOARD_YS[r] - sb.row_labels[r].get_y()
        sb.row_labels[r].shift(UP * dy)
        sb.cells[r].shift(UP * dy)
    dy = BOARD_FLOOR_Y - sb.floor_label.get_y()
    for m in (sb.floor_label, sb.floor_value, sb.floor_line, sb.optimal):
        m.shift(UP * dy)
    x0 = sb.floor_line.get_left()[0]
    sb.floor_line.become(Line([x0, BOARD_FLOOR_Y, 0], [-1.3, BOARD_FLOOR_Y, 0]).set_stroke(GOLD, 3))
    sb.optimal.next_to(sb.floor_line, RIGHT, buff=0.25)
    sb.sel_row = board_row("selection sort", ("49,995,000", GOLD), ("—", DIM), ("49,995,000", RED), 3)
    sb.add(*sb.sel_row)
    return sb


def board_row(name, *cells_and_r):
    *cells, r = cells_and_r
    y = BOARD_YS[r]
    lab = T(name, 30, YELLOW).move_to([SUM.B3_LX, y, 0], aligned_edge=LEFT)
    vals = [T(v, 40, col).move_to([x, y, 0]) for (v, col), x in zip(cells, SUM.B3_XS)]
    return (lab, *vals)


def ratio_arc(top_cell, bottom_cell, text, sag):
    """A GOLD arc from the bubble cell (below) up to another row's cell, bulging right, labelled."""
    x = max(top_cell.get_right()[0], bottom_cell.get_right()[0]) + 0.1
    p0, p1 = [x, bottom_cell.get_y(), 0], [x, top_cell.get_y(), 0]
    d = abs(p1[1] - p0[1])
    ang = 4 * atan(2 * sag / d)
    arc = CurvedArrow(p0, p1, angle=ang, color=GOLD, stroke_width=3, tip_length=0.18)
    lab = T(text, 32, GOLD).move_to([x + sag + 0.12, (p0[1] + p1[1]) / 2, 0], aligned_edge=LEFT)
    return arc, lab


def time_column(sb):
    """The DECstation-time column's parts (header and five cells)."""
    return [sb.col_headers[1], *[sb.cells[r][1] for r in range(3)], sb.sel_row[2], sb.bub_row[2]]


def bubble_board(ratios=False):
    """The five-row board: selsort_board_here() + the YELLOW bubble-sort row .bub_row (random
    "99,990,000", time DIM "-", sorted GREEN "9,999") and the GOLD note .note "reversed: 99,990,000"
    (bottom right). ratios=True: as this scene's last frame, the time column gone and the GOLD
    "x 2" / "~ x 4" arcs in its place (.x2, .x4: (arc, label))."""
    sb = selsort_board_here()
    sb.bub_row = board_row("bubble sort", ("99,990,000", GOLD), ("—", DIM), ("9,999", GREEN), 4)
    sb.add(*sb.bub_row)
    sb.note = T("reversed: 99,990,000", 28, GOLD).move_to([6.6, BOARD_FLOOR_Y, 0], aligned_edge=RIGHT)
    sb.add(sb.note)
    sb.x2 = ratio_arc(sb.sel_row[1], sb.bub_row[1], "× 2", 0.22)
    sb.x4 = ratio_arc(sb.cells[0][0], sb.bub_row[1], "≈ × 4", 0.4)
    if ratios:
        for m in time_column(sb):
            m.set_opacity(0)
        sb.add(*sb.x2, *sb.x4)
    return sb


NOTE_S = 28 / 44                         # "passes: 10,000" shrinks from T 44 to T 28


def ride_to_note(m):
    """m (T 44 below the rs caption) slides left, then up the empty left strip, shrinking to a T 28
    note at the board's top left (row-label column, header height): a quadratic Bezier via the
    corner, so it never crosses the caption or the arrow."""
    m.save_state()
    s = m.get_center().copy()
    e = m.copy().scale(NOTE_S).move_to([SUM.B3_LX, 2.65, 0], aligned_edge=LEFT).get_center()
    k = np.array([e[0], s[1], 0])

    def upd(mob, a):
        mob.restore()
        mob.scale(1 + (NOTE_S - 1) * a)
        mob.move_to((1 - a) ** 2 * s + 2 * a * (1 - a) * k + a ** 2 * e)
    return UpdateFromAlphaFunc(m, upd)


def arc_path(start, end, sag):
    """A path from start to end bulging upwards by `sag`."""
    d = abs(end[0] - start[0])
    ang = 4 * atan(2 * sag / d)
    return ArcBetweenPoints(start, end, angle=-ang if end[0] > start[0] else ang)


class BubbleCost(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        K.hold_for(self, self.last_born, len("≈ × 4"))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── helpers ──
    def bracket_at(self, ch, i, color=YELLOW):
        return bracket_over(ch.cells[i], ch.cells[i + 1]).set_stroke(color)

    def le_label(self, br):
        return T("≤ ?", 28, t2c={"?": GOLD}).next_to(br, UP, buff=0.1)

    def slide(self, br, lbl, ch, i, color=YELLOW, rt=0.8):
        nb = self.bracket_at(ch, i, color)
        self.play(Transform(br, nb), lbl.animate.next_to(nb, UP, buff=0.1), run_time=rt)

    def swap_cells(self, labs, vals, i, rt):
        a, b = labs[i], labs[i + 1]
        pa, pb = a.get_center().copy(), b.get_center().copy()
        self.play(a.animate(path_arc=-0.6 * PI).move_to(pb),
                  b.animate(path_arc=-0.6 * PI).move_to(pa), run_time=rt)
        labs[i], labs[i + 1] = b, a
        vals[i], vals[i + 1] = vals[i + 1], vals[i]

    def settled(self, ch, labs, idx, color=GREEN):
        anims = []
        for i in idx:
            anims += [ch.cells[i].box.animate.set_stroke(color), labs[i].animate.set_color(color)]
        return anims

    def copy_row(self, above, y, k, size=30, rt=1.0, extra=()):
        row = above.copy().move_to([above.get_x(), y, 0])
        lbl = pass_label(k, row, size)
        # the copy drops in from just under its source (never drawn over it), then holds
        self.play(*appear(row, shift=0.3 * DOWN), *during(appear(lbl, shift=None), 0.4, 1), *extra,
                  run_time=rt)
        return row, lbl

    def quick_pass(self, ch, labs, vals, step, swap_rt):
        br = self.bracket_at(ch, 0)
        lbl = self.le_label(br)
        self.play(FadeIn(br), FadeIn(lbl), run_time=step)
        for i in range(4):
            if i:
                self.slide(br, lbl, ch, i, RED if vals[i] > vals[i + 1] else YELLOW, rt=step)
            elif vals[0] > vals[1]:
                self.play(br.animate.set_stroke(RED), run_time=0.3)
            if vals[i] > vals[i + 1]:
                self.swap_cells(labs, vals, i, swap_rt)
        return br, lbl

    # ── 1: the cards; 5.3 grows; pairs, the loop, the task, pause ──
    def clip1(self):
        row = K.four_cards()
        card = H2.card_5_3()
        chain = card.chain
        q = T("?", 44, GOLD).next_to(card.rows[2], RIGHT, buff=0.3)
        tag = K.pause_tag()
        with self.say("c7.bubcost.1") as c:
            self.play(*appear(row.cards, row.note, lag=0.2), run_time=0.8)  # early: the overview, recalled
            c.wait_until("bubble")
            src = row.cards[2].frame
            others = [m for m in (*row.cards, row.note) if m is not row.cards[2]]
            self.play(*during([TransformFromCopy(src, card.frame)], 0, 0.6),
                      *during([FadeOut(m) for m in (*others, row.cards[2])], 0, 0.45),
                      *during(appear(card.header), 0.5, 1), run_time=1.4)
            self.play(*appear(*card.rows, lag=0.3), run_time=1.2)  # early: the task shown whole, then walked
            c.wait_until("pairs")
            self.play(*appear(chain, shift=0.2 * UP), run_time=1.0)
            self.play(GrowFromCenter(card.bracket), run_time=0.8)
            c.wait_until(own_word=card.in_lbl, cue="out of order")
            self.play(*appear(card.in_lbl), run_time=0.9)
            c.wait_until("repeat")
            self.play(Create(card.loop), run_time=1.2)
            c.wait_until(own_word=card.loop_lbl, cue="pass after pass")
            self.play(*appear(card.loop_lbl), run_time=0.9)
            c.wait_until("task")
            self.play(card.rows[2].animate.set_color(YELLOW),
                      FlashUnder(card.rows[2], color=YELLOW, time_width=1.5), run_time=1.5)
            self.play(*appear(q), run_time=0.8)
            c.wait_until("stop")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.7)
            self.play(FlashAround(tag[0], color=YELLOW, time_width=1.5, buff=0.12), run_time=1.2)
        self.card, self.tag, self.q = card, tag, q

    # ── 2: pass 1 ──
    def clip2(self):
        card = self.card
        chain = card.chain
        leaving = [card.frame, card.header, *card.rows, card.bracket, card.in_lbl, card.loop,
                   card.loop_lbl, self.q, self.tag]
        with self.say("c7.bubcost.2") as c:
            top = run_chain(RUNNING).move_to([CX, ROW_YS[0], 0])
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.45),
                      *during([Transform(chain, top)], 0.3, 1), run_time=1.4)
            row1, lbl1 = self.copy_row(chain, ROW_YS[1], 1, rt=1.2)
            labs, vals = labs_of(row1), list(RUNNING)

            c.wait_until("three and five")
            br = self.bracket_at(row1, 0)
            le = self.le_label(br)
            self.play(GrowFromCenter(br), *appear(le, shift=None), run_time=0.8)
            c.wait_until("five and nine")
            self.slide(br, le, row1, 1)

            c.wait_until("nine")
            self.slide(br, le, row1, 2, RED, rt=0.7)
            self.swap_cells(labs, vals, 2, 1.2)
            c.wait_until("nine and seven")
            self.slide(br, le, row1, 3, RED, rt=0.7)
            self.swap_cells(labs, vals, 3, 1.2)

            c.wait_until("rides")
            rider = rider_arrow(row1, 2, 4)
            self.play(*during(disappear(br, le), 0, 0.4), *during([Create(rider)], 0.3, 1), run_time=1.4)
            self.play(*self.settled(row1, labs, [4]), FlashAround(labs[4], color=GREEN, buff=0.1),
                      run_time=1.0)

            c.wait_until("count")
            n4 = T("4 comparisons", 30, GOLD).next_to(row1, RIGHT, buff=0.4).shift(UP * 0.2)
            self.play(*appear(n4), run_time=0.9)
            c.wait_until("minus one")
            n1 = T("= n − 1", 30, GOLD).next_to(n4, DOWN, buff=0.15, aligned_edge=LEFT)
            self.play(*appear(n1), run_time=0.9)
        self.rows, self.row_lbls = [chain, row1], [lbl1]
        self.labs1, self.vals1 = labs, vals
        self.notes = [rider, n4, n1]

    # ── 3: passes 2 and 3; 3 x 4 = 12 ──
    def clip3(self):
        with self.say("c7.bubcost.3") as c:
            row2, l2 = self.copy_row(self.rows[1], ROW_YS[2], 2, rt=0.9)
            labs, vals = labs_of(row2), list(self.vals1)
            br, le = self.quick_pass(row2, labs, vals, 0.35, 0.7)
            self.play(*disappear(br, le), *self.settled(row2, labs, [3]), run_time=0.6)

            c.wait_until("third")
            row3, l3 = self.copy_row(row2, ROW_YS[3], 3, rt=0.9)
            labs3, vals3 = labs_of(row3), list(vals)
            br, le = self.quick_pass(row3, labs3, vals3, 0.35, 0.7)
            stop = T("no swaps: stop", 30, GOLD).next_to(row3, RIGHT, buff=0.4)
            tick = check_mark().next_to(stop, RIGHT, buff=0.3)
            self.play(*during(disappear(br, le), 0, 0.4), *during(appear(stop), 0.35, 1), run_time=0.9)
            self.play(*self.settled(row3, labs3, range(5)), Create(tick), run_time=0.8)

            c.wait_until("twelve")
            twelve = MathTex(r"3 \times 4 = 12", font_size=60, color=GOLD).move_to([4.9, -3.0, 0])
            self.play(*appear(twelve), run_time=1.0)
        self.rows += [row2, row3]
        self.row_lbls += [l2, l3]
        self.notes += [stop, tick]
        self.twelve = twelve

    # ── 4: why n passes; worst case; reversed input ──
    def clip4(self):
        board = [*self.rows, *self.row_lbls, *self.notes]
        cap = T("each pass settles the largest unsettled item", 32)
        cap.move_to([-6.5, -3.0, 0], aligned_edge=LEFT)
        with self.say("c7.bubcost.4") as c:
            self.play(*set_alpha(board, 0.3), *during(appear(cap), 0.3, 1), run_time=1.2)

            c.wait_until("after")
            l_a = T("n − 1 passes settle everything", 40, GOLD).move_to(UP * 1.1)
            l_b = T("+ 1 pass with no swaps", 40, GOLD).move_to(UP * 0.1)
            sweep_clear(self, cap.animate.move_to(UP * 2.4), keep=[cap], run_time=1.4)
            self.play(*appear(l_a), run_time=1.0)
            c.wait_until("one more pass")
            self.play(*appear(l_b), run_time=1.0)

            c.wait_until("worst")
            nn = MathTex(r"n \times (n-1)", font_size=64, color=GOLD)
            on2 = MathTex(r"O(n^2)", font_size=64, color=RED)
            VGroup(nn, on2).arrange(RIGHT, buff=1.0).move_to(DOWN * 1.5)
            self.play(*appear(nn), run_time=1.0)
            c.wait_until("big o")
            self.play(*appear(on2), run_time=1.0)

            c.wait_until("reversed")
            worst = VGroup(nn, on2)
            wt = worst.copy().scale(0.7).move_to([4.5, REV_YS[0], 0])
            r0 = run_chain(REV_ROWS[0], REV_S, REV_LAB).move_to([RCX, REV_YS[0], 0])
            rl0 = T("reversed", 28, DIM).next_to(r0, LEFT, buff=0.4)
            sweep_clear(self, worst.animate.become(wt), *appear(r0, rl0, shift=None, lag=0.1),
                        keep=[nn, on2], run_time=1.3)
            rows, lbls = [r0], [rl0]
            vals = list(REV_ROWS[0])
            row_vals = [list(vals)]
            for k in (1, 2, 3, 4):
                if k == 2:
                    c.wait_until("creeps")
                    tag = creep_tag(rows)
                    threes = [labs_of(r)[v.index(3)] for r, v in zip(rows, row_vals)]
                    self.play(*[m.animate.set_color(YELLOW) for m in threes],
                              *during(appear(tag, shift=0.2 * LEFT), 0.3, 1), run_time=1.0)
                fast = k > 1
                row, lbl = self.copy_row(rows[-1], REV_YS[k], k, size=28, rt=0.45 if fast else 0.7)
                labs = labs_of(row)
                m = 5 - k                        # the rider goes from place 0 to place m
                start, end = labs[0].get_center().copy(), labs[m].get_center().copy()
                anims = [MoveAlongPath(labs[0], arc_path(start, end, 0.5))]
                for j in range(1, m + 1):
                    anims.append(labs[j].animate.move_to(labs[j - 1].get_center()))
                self.play(*anims, run_time=0.55 if fast else 1.1)
                labs = labs[1:m + 1] + [labs[0]] + labs[m + 1:]
                vals = vals[1:m + 1] + [vals[0]] + vals[m + 1:]
                green = [i for i in range(m, 5) if vals[i] != 3]
                self.play(*self.settled(row, labs, green), run_time=0.35 if fast else 0.5)
                rows.append(row)
                lbls.append(lbl)
                row_vals.append(list(vals))
            c.wait_until("twenty")
            row, lbl = self.copy_row(rows[-1], REV_YS[5], 5, size=28, rt=0.5)
            labs = labs_of(row)
            anims = [row.cells[i].box.animate.set_stroke(GREEN) for i in range(5)]
            anims += [labs[i].animate.set_color(GREEN) for i in range(5) if vals[i] != 3]
            self.play(*anims, run_time=0.5)
            twenty = MathTex(r"5 \times 4 = 20", font_size=60, color=GOLD).move_to([4.5, 0.0, 0])
            self.play(*appear(twenty), run_time=0.9)
        self.rev = [*rows, *lbls, tag, twenty, nn, on2]

    # ── 5: best and average case ──
    def clip5(self):
        sch = run_chain(sorted(RUNNING), 0.7, 1.25).move_to(UP * 1.6)
        for cell in sch.cells:
            cell.box.set_stroke(GREEN)
            cell.ptr.set_stroke(GREEN)
        with self.say("c7.bubcost.5") as c:
            c.wait_until("swaps nothing")
            sweep_clear(self, *appear(sch, shift=None), run_time=1.2)
            labs, vals = labs_of(sch), sorted(RUNNING)
            br, le = self.quick_pass(sch, labs, vals, 0.45, 0.7)
            four = T("4 = n − 1", 44, GOLD).move_to([-3.2, -0.2, 0])
            self.play(*during(disappear(br, le), 0, 0.4), *during(appear(four), 0.35, 1), run_time=1.1)
            c.wait_until("linear")
            on = MathTex(r"O(n)", font_size=64, color=GREEN).move_to([0.6, -0.2, 0])
            self.play(*appear(on), run_time=0.9)
            c.wait_until("insertion")
            ins = T("insertion sort: n − 1", 30, DIM).move_to([2.3, -0.2, 0], aligned_edge=LEFT)
            self.play(*appear(ins), run_time=0.9)

            sq = VGroup(*[Square(0.6).set_stroke(DIM, 2.5) for _ in range(15)]).arrange(RIGHT, buff=0.12)
            sq.move_to(UP * 0.5)
            mid = sq[7]
            mid.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.35)
            small = T("smallest", 30, YELLOW).next_to(mid, DOWN, buff=0.2)
            c.wait_until("smallest")
            sweep_clear(self, *appear(sq, small, shift=None, lag=0.3), run_time=1.6)
            c.wait_until("moves forward")
            back = CurvedArrow(mid.get_top() + UP * 0.1, sq[0].get_top() + UP * 0.1, angle=0.9,
                               color=YELLOW, stroke_width=4, tip_length=0.22)
            per = T("about n/2 places · 1 per pass", 32, YELLOW).next_to(back, UP, buff=0.15)
            self.play(Create(back), run_time=1.2)
            self.play(*appear(per), run_time=0.9)

            c.wait_until("half")
            half = T("≥ about n/2 passes × (n − 1)", 40, GOLD).move_to(DOWN * 1.4)
            self.play(*appear(half), run_time=1.0)
            c.wait_until("quadratic")
            on2 = MathTex(r"O(n^2)", font_size=64, color=RED).move_to(DOWN * 2.7)
            self.play(*appear(on2), run_time=1.0)

    # ── 6: rs, the scoreboard ──
    def clip6(self):
        cap = T("… ends 16807., 1.", 60, GOLD, t2c={"1.": YELLOW}).move_to(UP * 0.6)
        one = select(cap, "1.")[0]
        with self.say("c7.bubcost.6") as c:
            c.wait_until("worse")
            sweep_clear(self, *appear(cap, shift=None), run_time=1.3)
            tag = T("first seed · smallest of all", 32, YELLOW)
            tag.next_to(one, UP, buff=0.7).align_to(one, RIGHT).shift(RIGHT * 0.3)
            pt = Arrow(tag.get_bottom() + 0.05 * DOWN, one.get_top() + 0.05 * UP, buff=0.05,
                       color=YELLOW, stroke_width=3, max_tip_length_to_length_ratio=0.3)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), GrowArrow(pt), run_time=1.0)

            c.wait_until("all")
            back = Arrow(cap.get_right() + DOWN * 0.75, cap.get_left() + DOWN * 0.75, buff=0,
                         color=YELLOW, stroke_width=5)
            passes = T("passes: 10,000", 44, GOLD).next_to(back, DOWN, buff=0.45)
            self.play(GrowArrow(back), *during(appear(passes), 0.3, 1), run_time=1.4)

            c.wait_until("ninety-nine")
            sb = bubble_board()
            bub, note = sb.bub_row, sb.note
            sb.remove(*bub, note)
            # "passes: 10,000" rides along (left, then up the clear left strip) to a small note
            # top left, above the row labels, while the rest clears; the board then fades in.
            sweep_clear(self, *during([ride_to_note(passes)], 0, 0.5), *appear(sb, shift=None),
                        keep=[passes], run_time=2.0)
            self.play(*appear(bub[0], bub[1], lag=0.3, shift=0.2 * UP), run_time=1.1)
            self.play(*appear(bub[2], bub[3], lag=0.3, shift=0.2 * UP), run_time=0.9)
            c.wait_until("reversed")
            self.play(*appear(note), run_time=0.9)

            c.wait_until("twice")
            (a2, x2), (a4, x4) = sb.x2, sb.x4
            self.play(*during(disappear(*time_column(sb)), 0, 0.4), *during([Create(a2)], 0.3, 1),
                      *during(appear(x2, shift=None), 0.6, 1),
                      FlashAround(sb.sel_row[1], color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("four times")
            self.play(Create(a4), *during(appear(x4, shift=None), 0.4, 1),
                      FlashAround(sb.cells[0][0], color=YELLOW, time_width=1.5), run_time=1.2)
            self.last_born = self.time
