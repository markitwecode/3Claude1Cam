"""Chapter 7, scene 2: Exercise 5.1's solution, selection sort's cost (4 + 3 + 2 + 1 = 10 on the
running list; N - 1 comparisons for any order; T(n+1) = T(n) + n, O(n^2) in every case; the
scoreboard's new row). Clips c7.selcost.1 - c7.selcost.5.

Opens from an empty frame: ch6 s4's four_cards() row fades in, card 5.1 grows from its first card.
Counts checked with OCaml 5.4.1 (selsort with a tallying <=): 10 on [3;5;9;4;7], on sorted, on
reversed and on [3;5;3;1;5]; 49,995,000 on the notes' 10,000-item rs and on 10,000 sorted items.

Exports (for s4 and the recap):
  selsort_board()  ch6 s2's board3("full"), raised 0.35, its floor row lowered 0.95, with the YELLOW "selection sort" row: GOLD "49,995,000", DIM "—",
                   RED "49,995,000". Attributes as board3, plus .sel_label, .sel_cells (3).
  staircase()      the GOLD staircase 4 / 3 / 2 / 1 (blocks 0.55, left edge x -4.6, top y -0.95) with
                   GOLD counts "4" "3" "2" "1" right of the rows. .rows[r][j], .labels[r].
  three_chains()   the three small lists (running; sorted, GREEN label; reversed, RED label), each
                   with its GOLD "10". .chains, .labels, .tens.
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

K = load_scene("ch6_s4_hints1")          # the exercise-card kit
B = load_scene("ch6_s2_summary")         # board3()

RUNNING = [3, 5, 9, 4, 7]
S = 0.75                                 # chain scale (as card 5.1's)
RUN_Y = 2.3                              # the running chain
OUT_X0, OUT_Y = -5.1, -0.2               # the output chain (left edge, y)
SX, STOP, U = -4.6, -0.95, 0.55          # the staircase: left edge, top edge, block side
SB_UP = 0.35                             # the scoreboard is raised this much ...
SB_DROP = 0.95                           # ... and its floor row lowered this much, for the new row


# ── exports ──────────────────────────────────────────────────────────────────────
def staircase():
    rows = VGroup()
    labels = VGroup()
    for r, n in enumerate((4, 3, 2, 1)):
        y = STOP - (r + 0.5) * U
        row = VGroup(*[Square(U, stroke_color=BG, stroke_width=4, fill_color=GOLD, fill_opacity=0.85)
                       .move_to([SX + (j + 0.5) * U, y, 0]) for j in range(n)])
        rows.add(row)
        labels.add(T(str(n), 34, GOLD).move_to([SX + n * U + 0.25, y, 0], aligned_edge=LEFT))
    g = VGroup(rows, labels)
    g.rows, g.labels = rows, labels
    return g


def small_list(values, color=BLUE):
    ch = K.mini_chain(values, side=0.6, gap=0.3, size=34, color=color)
    last = ch.boxes[-1]
    nil = Mono("[]", 32, TEAL).next_to(last, RIGHT, buff=0.3)
    arr = Arrow(last.get_right(), nil.get_left(), buff=0.03, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.5, tip_length=0.12)
    ch.add(arr, nil)
    ch.nil = nil
    return ch


CH_YS = (2.75, 1.95, 1.15)


def three_chains():
    chains, labels, tens = VGroup(), VGroup(), VGroup()
    for vals, (name, col), y in zip((RUNNING, sorted(RUNNING), sorted(RUNNING, reverse=True)),
                                    (("running", DIM), ("sorted", GREEN), ("reversed", RED)), CH_YS):
        ch = small_list(vals).move_to([-2.5, y, 0], aligned_edge=LEFT)
        lab = T(name, 32, col).move_to([-3.0, y, 0], aligned_edge=RIGHT)
        ten = T("10", 44, GOLD).move_to([ch.get_right()[0] + 0.55, y, 0], aligned_edge=LEFT)
        chains.add(ch)
        labels.add(lab)
        tens.add(ten)
    g = VGroup(chains, labels, tens)
    g.chains, g.labels, g.tens = chains, labels, tens
    return g


def _board_layout():
    """board3("full") plus the selection row, in board3's own coordinates, floor row moved down."""
    b = B.board3("full")
    pitch = B.B3_YS[0] - B.B3_YS[1]
    y = B.B3_YS[2] - pitch
    lab = T("selection sort", 30, YELLOW).move_to([B.B3_LX, y, 0], aligned_edge=LEFT)
    cells = VGroup(T("49,995,000", 40, GOLD).move_to([B.B3_XS[0], y, 0]),
                   T("—", 40, DIM).move_to([B.B3_XS[1], y, 0]),
                   T("49,995,000", 40, RED).move_to([B.B3_XS[2], y, 0]))
    floor = [b.floor_label, b.floor_value, b.floor_line, b.optimal]
    for m in floor:
        m.shift(DOWN * SB_DROP)
    return b, lab, cells, floor, pitch


def _place(g):
    g.shift(UP * SB_UP)
    return g


def selsort_board():
    b, lab, cells, floor, pitch = _board_layout()
    g = VGroup(b, lab, cells)
    _place(g)
    g.board, g.sel_label, g.sel_cells, g.floor = b, lab, cells, floor
    for name in ("rule", "row_labels", "col_headers", "tally_tag", "cells", "floor_line",
                 "floor_label", "floor_value", "col3_header", "col3_cells", "optimal"):
        setattr(g, name, getattr(b, name))
    return g


# ── helpers ──────────────────────────────────────────────────────────────────────
def fit(c, cue=None, frac=0.7, lo=0.6, hi=1.5, nth=0):
    return min(hi, max(lo, frac * c.until(cue, floor=0.0, nth=nth)))


def mk_point(cell):
    return above(cell.box, buff=0.18)


def cmp_arc(a, b):
    p, q = a.box.get_bottom() + DOWN * 0.08, b.box.get_bottom() + DOWN * 0.08
    d = q[0] - p[0]
    arc = ArcBetweenPoints(p, q, angle=min(2.2, 8 * 0.42 / d)).set_stroke(FG, 2.5)
    return arc


def cmp_label(arc):
    return T("≤ ?", 30).move_to(arc.get_bottom() + DOWN * 0.24)


class SelectionCost(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        K.hold_for(self, self.versus_born, 8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # 1: card 5.1, restated; pause
    def clip1(self):
        row = K.four_cards()
        card = K.card_5_1()
        chain, c0 = card.chain, card.chain.cells[0]
        tag = K.pause_tag()
        icon, ptext = tag[0], tag[1]
        with self.say("c7.selcost.1") as c:
            self.play(*appear(*row.cards, lag=0.2), run_time=0.8)  # early: the overview, recalled
            src = row.cards[0].frame
            others = [m for m in row.cards if m is not row.cards[0]]
            self.wait(0.5)
            self.play(*during([TransformFromCopy(src, card.frame)], 0, 0.6),  # early: the task shown whole, then walked
                      *during([FadeOut(m) for m in (*others, row.cards[0])], 0, 0.45),
                      *during(appear(card.header, *card.rows, icon, lag=0.12), 0.5, 1),
                      run_time=1.6)
            # "It looks through the items, finds a smallest one, and removes it, ..."
            c.wait_until("smallest")
            self.play(*appear(chain, shift=0.2 * UP), run_time=1.0)
            c.wait_until("finds a smallest")
            self.play(*recolor([c0.label], YELLOW), FlashAround(c0, color=YELLOW, buff=0.1),
                      run_time=1.1)
            c.wait_until("removes it")
            self.play(c0.animate.shift(UP * card.lift_by), *disappear(chain.arrows[0]), run_time=1.3)
            chain.remove(chain.arrows[0])
            c.wait_until(own_word=card.res_lbl, cue="head")
            self.play(*appear(card.res_lbl, shift=0.2 * RIGHT), run_time=0.8)
            # "The tail comes from sorting the remaining items, recursively."
            c.wait_until("rest")
            self.play(GrowFromCenter(card.brace), *appear(card.brace_lbl), run_time=1.2)
            self.play(GrowArrow(card.tail), *appear(card.tail_q, shift=0.2 * LEFT), run_time=1.0)
            # "State its time complexity, with justification."
            c.wait_until("task")
            self.play(card.rows[2].animate.set_color(YELLOW),
                      FlashUnder(card.rows[2], color=YELLOW, time_width=1.5), run_time=1.5)
            # "Pause here, and try it."
            c.wait_until("stop")
            self.play(*appear(ptext, shift=0.2 * LEFT), run_time=0.7)
            self.play(FlashAround(icon, color=YELLOW, time_width=1.5, buff=0.12), run_time=1.2)

    # 2: selection sort on the running list: 4 + 3 + 2 + 1 = 10
    def clip2(self):
        run = ConsChain(RUNNING).scale(S)
        for cell in run.cells:
            cell.label.scale(1.1)
        run.move_to([0, RUN_Y, 0])
        cells = run.cells
        ref = ConsChain(sorted(RUNNING)).scale(S)
        ref.move_to([OUT_X0, OUT_Y, 0], aligned_edge=LEFT)
        out_nil = Nil().scale(S).move_to(ref.cells[0].get_left(), aligned_edge=LEFT).set_y(OUT_Y)
        res_lbl = T("result", 30, DIM).move_to([OUT_X0 - 0.3, OUT_Y, 0], aligned_edge=RIGHT)
        sc = staircase()
        mk = marker(YELLOW).move_to(mk_point(cells[0]))
        mk_lbl = T("smallest so far", 30, YELLOW).next_to(mk, RIGHT, buff=0.2)
        mkg = VGroup(mk, mk_lbl)

        rarrows = {i: run.arrows[i] for i in range(5)}     # out of cell i (to the next remaining, or [])
        remaining = list(range(5))
        out_cells = []
        out_arrows = []

        def nil_at(k):
            if k < 5:
                return out_nil.copy().move_to(ref.cells[k].get_left(), aligned_edge=LEFT).set_y(OUT_Y)
            return out_nil.copy().move_to(ref.nil)

        def drop(w, next_first=None, t0=0.0, t1=1.0):
            """Animations: winner cell w leaves the running chain for the output's next slot
            (in the [t0, t1] part of its play)."""
            def D(an, x, y):
                return during(an, t0 + x * (t1 - t0), t0 + y * (t1 - t0))
            k = len(out_cells)
            cell = cells[w]
            cell.generate_target()
            cell.target.move_to(ref.cells[k])
            cell.target.box.set_stroke(GREEN)
            cell.target.ptr.set_stroke(GREEN)
            cell.target.label.set_color(GREEN)
            new_nil = nil_at(k + 1)
            new_arr = link(cell.target, new_nil)
            pos = remaining.index(w)
            anims = D([FadeOut(rarrows.pop(w))], 0, 0.35)
            if pos > 0:
                prev = remaining[pos - 1]
                nxt = remaining[pos + 1] if pos + 1 < len(remaining) else None
                anims += D([FadeOut(rarrows[prev])], 0, 0.35)
                bridge = link(cells[prev], cells[nxt] if nxt is not None else run.nil)
                rarrows[prev] = bridge
                anims += D([GrowArrow(bridge)], 0.55, 1)
            remaining.remove(w)
            anims += D([out_nil.animate.move_to(new_nil)], 0, 0.5)
            anims += D([MoveToTarget(cell)], 0.15, 0.85)
            anims += D([GrowArrow(new_arr)], 0.75, 1)
            if next_first is not None:
                anims += D([mkg.animate.shift(mk_point(cells[next_first]) - mk.get_center())], 0.3, 0.9)
            out_cells.append(cell)
            out_arrows.append(new_arr)
            return anims

        def next_after(w):
            return next((i for i in remaining if i != w), None)

        def round_anims(r, t1):
            """One quick round on what's left, in [0, t1] of its play: the marker walks to the
            winner, the row of blocks grows, its count."""
            m = remaining[0]
            seq = [m]
            for j in remaining[1:]:
                if RUNNING[j] <= RUNNING[m]:
                    m = j
                seq.append(m)
            n = len(remaining) - 1
            anims = []
            for jj, blk in enumerate(sc.rows[r]):
                a = 0.6 * t1 * jj / n
                anims += during([GrowFromEdge(blk, LEFT)], a, a + 0.4 * t1)
                if seq[jj + 1] != seq[jj]:
                    anims += during([mkg.animate.shift(mk_point(cells[seq[jj + 1]]) - mk_point(cells[seq[jj]]))],
                                    a, a + 0.4 * t1)
            anims += during(appear(sc.labels[r]), 0.5 * t1, t1)
            return anims, m

        def one_round(r, cue_next, cap):
            rt = min(cap, max(1.0, 0.95 * c.until(cue_next, floor=0.0)))
            an, w = round_anims(r, 0.5)
            self.play(*an, *drop(w, next_first=next_after(w), t0=0.5, t1=1.0), run_time=rt)

        with self.say("c7.selcost.2") as c:
            # "Watch it on our running list."
            sweep_clear(self, *appear(run, out_nil, lag=0.3), run_time=1.6)
            # "To find the smallest, keep the smallest so far, ..."
            c.wait_until(own_word=mk_lbl, cue="scan")
            self.play(*appear(mkg), run_time=0.9)
            # "... and compare it with each other item in turn."
            c.wait_until("and compare")
            step = min(0.75, max(0.45, (c.until("four", floor=0.0) - 1.1 - 4 * 0.15) / 3))
            arc = lbl = num = None
            for k, j in enumerate((1, 2, 3, 4)):
                a2 = cmp_arc(cells[0], cells[j])
                l2 = cmp_label(a2)
                blk = sc.rows[0][k]
                n2 = sc.labels[0] if k == 3 else T(str(k + 1), 34, GOLD).move_to(
                    [SX + (k + 1) * U + 0.25, sc.rows[0].get_y(), 0], aligned_edge=LEFT)
                if k == 0:
                    self.play(Create(a2), *appear(l2, shift=None), GrowFromEdge(blk, LEFT),
                              *appear(n2), run_time=1.1)
                    arc, lbl = a2, l2
                else:
                    self.play(Transform(arc, a2), lbl.animate.move_to(l2), GrowFromEdge(blk, LEFT),
                              *swap(num, n2), run_time=step)
                num = n2
                self.wait(0.15)
            # "The three wins all four comparisons, so it heads the result."
            word = T("comparisons", 34, GOLD).next_to(sc.labels[0], RIGHT, buff=0.2)
            c.wait_until("four")
            self.play(*appear(word, shift=0.2 * LEFT), FlashAround(cells[0], color=YELLOW, buff=0.1),
                      run_time=1.1)
            c.wait_until("heads")
            self.play(*during(disappear(arc, lbl), 0, 0.3), *drop(0, next_first=1),
                      *during(appear(res_lbl, shift=0.2 * RIGHT), 0.7, 1), run_time=1.5)
            # "The four items left take three comparisons, then two, then one."
            c.wait_until("next")
            one_round(1, "then two", 1.6)
            c.wait_until("then two")
            one_round(2, "then one", 1.3)
            c.wait_until("then one")
            one_round(3, "total", 1.2)
            self.play(*drop(remaining[0]), *during(disappear(mkg), 0, 0.4),
                      *during([FadeOut(run.nil)], 0.5, 1), run_time=0.8)
            # "Four, plus three, plus two, plus one, makes ten."
            total = MathTex("4", "+", "3", "+", "2", "+", "1", "=", "10", font_size=60, color=GOLD)
            total.move_to([1.9, sc.rows[1].get_y() - 0.25, 0])
            c.wait_until("total")
            rt = min(1.8, max(1.0, 0.9 * c.until("makes ten", floor=0.0)))
            anims = during(disappear(word), 0, 0.2)
            for r in range(4):
                a = 0.2 * r
                path = Line(sc.rows[r].get_left(), sc.rows[r].get_right()).set_stroke(YELLOW, 8)
                anims += during([VShowPassingFlash(path, time_width=0.6)], a, a + 0.3)
                anims += during(appear(*total[max(0, 2 * r - 1):2 * r + 1], shift=None, lag=0.1), a + 0.05, a + 0.4)
            self.play(*anims, run_time=rt)
            tick = check_mark(GREEN).next_to(out_nil, RIGHT, buff=0.4)
            c.wait_until("makes ten")
            self.play(*appear(total[7], total[8], shift=None, lag=0.2), FadeIn(tick, scale=0.6),
                      run_time=min(1.0, max(0.5, c.until(floor=0.0))))
            settle(self, total)

    # 3: sorted or reversed: still 10; every other item loses once
    def clip3(self):
        tc = three_chains()
        qs = [T("?", 44, GOLD).move_to(t, aligned_edge=LEFT) for t in tc.tens]
        vals = RUNNING
        tl_sq = VGroup(*[Square(1.0).set_stroke(YELLOW if v == 3 else DIM, 3)
                         .set_fill(YELLOW if v == 3 else DIM, 0.15) for v in vals]).arrange(RIGHT, buff=0.45)
        tl_sq.move_to([0, -0.4, 0])
        tl_v = VGroup(*[T(str(v), 44, YELLOW if v == 3 else DIM).move_to(s) for v, s in zip(vals, tl_sq)])
        lost = [T("lost", 28, RED).next_to(s, DOWN, buff=0.18) for v, s in zip(vals, tl_sq) if v != 3]
        cap1 = T("every other item must lose once", 30)
        dot = T("·", 30, DIM)
        cap2 = T("one loser per comparison", 30)
        cap = VGroup(cap1, dot, cap2).arrange(RIGHT, buff=0.3).move_to([0, -2.05, 0])
        nn = T("N items: N − 1 comparisons", 40, GOLD).move_to([0, -3.0, 0])
        with self.say("c7.selcost.3") as c:
            # "Now try sorted input, or reversed."
            sweep_clear(self, *appear(tc.labels[0], tc.chains[0], qs[0], lag=0.15), run_time=1.1)  # early: the running list, recalled
            for i in (1, 2):
                c.wait_until(cue=("sorted", "reversed")[i - 1])
                self.play(*appear(tc.labels[i], tc.chains[i], qs[i], lag=0.12), run_time=0.9)
            # "Still ten."
            c.wait_until("same")
            self.play(*[a for i in range(3) for a in during(swap(qs[i], tc.tens[i]), 0.1 * i, 0.7 + 0.1 * i)],
                      run_time=1.2)
            # "Here's why."
            c.wait_until("loser")
            self.play(*appear(*tl_sq, shift=None, lag=0.1), *appear(*tl_v, shift=None, lag=0.1),
                      run_time=1.1)
            # "Every item except the smallest must lose a comparison, ..."
            c.wait_until(own_word=cap1, cue="every")
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("lose")
            self.play(*appear(*lost, lag=0.2), run_time=1.3)
            # "... and each comparison has just one loser."
            c.wait_until(own_word=cap2, cue="one loser")
            self.play(*appear(dot, cap2, lag=0.15), run_time=1.0)
            # "So finding the smallest of N items takes N minus one comparisons, whatever their order."
            c.wait_until(own_word=nn)
            self.play(*appear(nn), run_time=1.1)
            c.wait_until("minus one")
            self.play(FlashUnder(nn, color=GOLD, time_width=1.5), run_time=1.3)

    # 4: T(n+1) = T(n) + n; Lecture 2's table; n(n-1)/2, O(n^2) in every case
    def clip4(self):
        q = MathTex(r"T(n) = {?}", font_size=64, color=GOLD).move_to([0, 0.6, 0])
        rec = MathTex(r"T(n+1) = T(n) + n", font_size=64).move_to([0, 0.6, 0])
        tab = K.l2_table(size=40)
        tab.shift(np.array([-6.4, 1.95, 0]) - tab[0][0].get_left())
        tab[1][1].set_color(YELLOW)
        tag = T("nsumsum · insertion sort's worst case", 30, DIM).move_to(
            [-6.4, tab[3].get_y() - 0.75, 0], aligned_edge=LEFT)
        RX = 3.9
        closed = MathTex(r"T(n) = \frac{n(n-1)}{2}", font_size=50).move_to([RX, 1.6, 0])
        o_red = MathTex("O(n^2)", font_size=60, color=RED).move_to([RX, 0.25, 0])
        cases = []
        for name, x in (("best", RX - 1.8), ("average", RX), ("worst", RX + 1.8)):
            w = T(name, 32).move_to([x, -0.95, 0])
            o = MathTex("O(n^2)", font_size=40, color=RED).move_to([x, -1.55, 0])
            cases.append((w, o))
        tline = T("removing it: one more walk at most  ·  time O(n²)", 32,
                  t2c={"time O(n²)": RED, "·": DIM}).move_to([0, -2.85, 0])
        with self.say("c7.selcost.4") as c:
            # "So sorting one more item adds exactly N comparisons."
            c.wait_until("adds")
            sweep_clear(self, *appear(q, shift=None), run_time=1.4)  # early: ch6's hint, recalled
            # "Tee of N plus one equals tee of N, plus N."
            c.wait_until("tee of n plus one")
            self.play(*swap(q, rec), run_time=1.3)
            # "That's lecture two's N-sum-sum row again, ..."
            c.wait_until("table")
            rec.generate_target()
            rec.target.scale(40 / 64).move_to(tab[1][0]).set_color(YELLOW)
            rest = [tab[0][0], tab[0][1], tab[1][1], tab[2][0], tab[2][1], tab[3][0], tab[3][1]]
            self.play(*during([MoveToTarget(rec)], 0, 0.55),
                      *during(appear(*rest, shift=0.3 * LEFT, lag=0.08), 0.5, 1), run_time=2.0)
            c.wait_until("insertion")
            self.play(*appear(tag), FlashAround(VGroup(rec.copy(), tab[1][1].copy()), color=YELLOW,
                                                time_width=1.5, buff=0.12), run_time=1.3)
            # "It adds up to N times N minus one, over two, which is big O of N squared."
            c.wait_until("closed")
            self.play(*appear(closed, shift=None), run_time=1.2)
            c.wait_until("big o")
            self.play(*fly(tab[1][1], o_red), run_time=1.4)
            # "The order never matters, so that's the best, average and worst case at once."
            names = ("best", "average", "worst", "time")
            for k, (w, o) in enumerate(cases):
                c.wait_until(names[k])
                self.play(*appear(w, o, lag=0.15), run_time=fit(c, names[k + 1], frac=0.9, lo=0.45, hi=0.9))
            # "Removing the smallest costs at most one more walk along the list, ..."
            c.wait_until(own_word=tline, cue="time")
            self.play(*appear(tline), run_time=1.1)

    # 5: the scoreboard's new row
    def clip5(self):
        fin = selsort_board()
        board = fin.board
        dy = SB_DROP
        for m in fin.floor:
            m.shift(UP * dy)
        lab, cells = fin.sel_label, fin.sel_cells
        ins_r, ins_s = board.cells[0][0], board.col3_cells[0]
        with self.say("c7.selcost.5") as c:
            # "Back to the scoreboard."
            sweep_clear(self, *appear(board, shift=None), run_time=1.6)  # early: the scoreboard, recalled
            # "On our ten thousand random numbers, selection sort makes forty-nine million, ..."
            c.wait_until(own_word=lab, cue="selection sort")
            self.play(*[m.animate.shift(DOWN * dy) for m in fin.floor],
                      *during(appear(lab, shift=0.4 * RIGHT), 0.4, 1), run_time=1.4)
            c.wait_until("million")
            self.play(*appear(cells[0], cells[1], lag=0.3), run_time=1.2)
            # "On sorted numbers, exactly the same."
            c.wait_until("sorted")
            self.play(*appear(cells[2]), run_time=1.0)
            self.play(FlashAround(cells[2], color=RED, time_width=1.5), run_time=1.2)
            # "That's twice insertion sort's count on random input, ..."
            c.wait_until("versus")
            a0 = ins_r.get_right() + RIGHT * 0.15
            a1 = cells[0].get_right() + RIGHT * 0.15
            arr = CurvedArrow(a0, a1, angle=-0.9, color=GOLD).set_stroke(width=3)
            x2 = T("× 2", 36, GOLD).move_to([arr.get_right()[0] + 0.5, (a0[1] + a1[1]) / 2, 0])
            self.play(FlashAround(ins_r, time_width=1.5), FlashAround(cells[0], time_width=1.5),
                      run_time=1.3)
            self.play(Create(arr), *appear(x2, shift=0.2 * LEFT), run_time=1.2)
            self.versus_born = self.time
            # "... and on sorted input, insertion sort needs under ten thousand."
            c.wait_until("on sorted input")
            self.play(FlashAround(ins_s, color=GREEN, time_width=1.5),
                      FlashAround(cells[2], color=RED, time_width=1.5), run_time=1.4)
