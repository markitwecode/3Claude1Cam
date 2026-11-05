"""Chapter 3, scene 4: what pairs are for (book, lookup both ways, cost, squares). Clips c3.pairs.1 – c3.pairs.3.

PLAN
  pairs.1  `let book = zip ...` + reply at the top; the three tuple cells are built from the
           reply's tuples, `book` points at the first. {assoc}: the notes' MathTex under the
           cells with a two-way arrow under each pair; names YELLOW, numbers GOLD (cells and
           x/y); DIM "a telephone directory" at the bottom.
  pairs.2  code + MathTex clear; query `"Cleo" -> ?` top-left, GOLD pointer + box walk the
           name parts (cross, cross, tick), 47 lifts into the "?". {back}: `? <- 35` top-right,
           the walk again on the number parts (cross at 21, tick at 35), "Bob" lifts out.
  pairs.3  DIM "linear search (last time)" + RED "very slowly"; {big}: the chain shrinks and
           stretches (... and []), brace "a million pairs", GOLD counter to 1,000,000 as the
           pointer sweeps. Clear; [1; 2; 3] -> arrows -> [(1, 1); (2, 4); (3, 9)] from copies,
           label, DIM "how to write it: a later lecture". Clear to empty.
STATUS  check clean but for dwell notes: the {big} counter clears on "applying" (kept in sync
        with the topic change) and the last aside gets a 2 s hold.
        c3.pairs.1 re-voiced ("it's a list, and each of its cells holds a pair"): all its cues
        are marks/phrases, re-resolved from the new timings, no code change; re-checked clean.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── tuple cells, shared look with ch3_s3_order's answer cells (keep in step) ──────────
PAIR_W = 2.7        # value-box width of a tuple cell (height CELL = 1.0, pointer box PTR_W)
PAIR_SIZE = 30      # tuple text inside the cell: CMU Serif (like value_label), FG at first
PAIR_LINK = 0.6     # arrow length between tuple cells

BOOK = [("Amy", 21), ("Bob", 35), ("Cleo", 47)]
CODE_IN = 'let book = zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]'
REPLY = 'val book : (string * int) list =\n  [("Amy", 21); ("Bob", 35); ("Cleo", 47)]'
CODE_SIZE = 30

CHAIN_Y = 0.0
PTR_Y = CHAIN_Y - CELL / 2 - 0.38      # the walking pointer, under the cells
MARK_Y = CHAIN_Y - CELL / 2 - 1.05     # crosses / ticks, under the pointer
ROW_Y = 2.6                            # the two queries
TAG_Y = -3.0                           # DIM tags at the bottom

BIG_S = 0.93        # {big}: chain scale
BIG_Y = 0.8         # {big}: chain centre height


class PairCell(VGroup):
    """[ ("Amy", 21) | • ]: one cons cell whose value is a pair."""

    def __init__(self, name, num, color=BLUE, **kw):
        super().__init__(**kw)
        self.box = Rectangle(width=PAIR_W, height=CELL, stroke_color=color, stroke_width=3,
                             fill_color=BG, fill_opacity=1)
        self.ptr = Rectangle(width=PTR_W, height=CELL, stroke_color=color, stroke_width=3,
                             fill_color=BG, fill_opacity=1).next_to(self.box, RIGHT, buff=0)
        self.dot = Dot(self.ptr.get_center(), radius=0.07, color=FG)
        self.label = T(f'("{name}", {num})', size=PAIR_SIZE).move_to(self.box)
        self.label.set_z_index(2)          # above a highlight box (z 1) above the cell (z 0)
        k = len(name) + 2                  # glyphs: ( "name" , num )   (no glyph for spaces)
        self.name_part = self.label[1:1 + k]
        self.num_part = self.label[2 + k:2 + k + len(str(num))]
        self.add(self.box, self.ptr, self.dot, self.label)

    def tail_start(self):
        return self.dot.get_center()

    def entry(self):
        return self.box.get_left()


class PairChain(VGroup):
    """ConsChain's layout with tuple cells: .cells[i], .arrows[i] (out of cell i), .nil."""

    def __init__(self, pairs, **kw):
        super().__init__(**kw)
        self.cells = [PairCell(n, v) for n, v in pairs]
        x = 0.0
        for c in self.cells:
            c.move_to(RIGHT * x, aligned_edge=LEFT)
            x += PAIR_W + PTR_W + PAIR_LINK
        self.nil = Nil().move_to(RIGHT * (x + 0.25))
        targets = self.cells[1:] + [self.nil]
        self.arrows = [link(c, t) for c, t in zip(self.cells, targets)]
        self.add(*self.cells, *self.arrows, self.nil)
        self.move_to(UP * CHAIN_Y)


def ptr_arrow(start, end):
    return Arrow(start, end, buff=0, stroke_width=3, color=FG,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16)


class WhatPairsAreFor(NarratedScene):
    def construct(self):
        self.clip_book()
        self.clip_lookup()
        self.clip_cost_and_squares()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c3.pairs.1: book, its cells, what a list of pairs means ──────────────────────
    def clip_book(self):
        with self.say("c3.pairs.1") as c:
            code_in = Code(CODE_IN, size=CODE_SIZE)
            reply = Code(REPLY, size=CODE_SIZE)
            code_in.find("book").set_color(YELLOW)
            reply.find("book").set_color(YELLOW)
            reply.next_to(code_in, DOWN, buff=0.3, aligned_edge=LEFT)
            VGroup(code_in, reply).move_to(UP * 2.65)
            self.play(FadeIn(code_in, shift=0.2 * DOWN),
                      time_span(FadeIn(reply, shift=0.2 * UP), 0.9, 1.9), run_time=1.9)

            # {cells} each tuple of the reply becomes a cell
            c.wait_until("cells")
            chain = PairChain(BOOK)
            anims = []
            for i, cell in enumerate(chain.cells):
                s = 0.35 * i
                src = reply.find(f'("{BOOK[i][0]}", {BOOK[i][1]})')
                anims += [time_span(FadeIn(m), s, s + 0.8) for m in (cell.box, cell.ptr, cell.dot)]
                anims.append(time_span(TransformFromCopy(src, cell.label), s, s + 1.4))
                anims.append(time_span(GrowArrow(chain.arrows[i]), s + 0.9, s + 1.5))
            anims.append(time_span(FadeIn(chain.nil), 1.6, 2.1))
            book_lbl = label_pointer("book", chain.cells[0].box, UP, color=YELLOW, size=34,
                                     length=0.45)
            anims.append(time_span(FadeIn(book_lbl, shift=0.3 * DOWN), 1.7, 2.4))
            self.play(*anims, run_time=2.4)
            settle(self, chain)

            # {assoc} the general shape: first part <-> second part
            c.wait_until("assoc")
            mt = MathTex(r"[(x_1, y_1), \ldots, (x_n, y_n)]", font_size=52,
                         substrings_to_isolate=["x_1", "y_1", "x_n", "y_n"]).move_to(DOWN * 1.6)
            xs = [mt.get_part_by_tex("x_1"), mt.get_part_by_tex("x_n")]
            ys = [mt.get_part_by_tex("y_1"), mt.get_part_by_tex("y_n")]
            ay = mt.get_bottom()[1] - 0.2
            twoway = [DoubleArrow([x.get_x() - 0.05, ay, 0], [y.get_x() + 0.05, ay, 0], buff=0,
                                  stroke_width=3, color=FG, tip_length=0.12,
                                  max_tip_length_to_length_ratio=0.3)
                      for x, y in zip(xs, ys)]
            self.play(FadeIn(mt, shift=0.2 * UP), run_time=1.0)
            c.wait_until("associates")
            self.play(*[GrowFromCenter(a) for a in twoway], run_time=1.0)

            # names YELLOW, numbers GOLD, in the cells and in the shape
            c.wait_until("each name")
            self.play(*[a for cell in chain.cells for a in recolor(cell.name_part, YELLOW)],
                      *[a for x in xs for a in recolor(x, YELLOW)], run_time=0.8)
            c.wait_until("its number")
            self.play(*[a for cell in chain.cells for a in recolor(cell.num_part, GOLD)],
                      *[a for y in ys for a in recolor(y, GOLD)], run_time=0.8)
            c.wait_until("telephone")
            tag = T("a telephone directory", size=32, color=DIM).move_to(UP * TAG_Y)
            self.play(FadeIn(tag, shift=0.2 * DOWN), run_time=1.0)

        self.chain, self.book_lbl, self.tag = chain, book_lbl, tag

    # ── c3.pairs.2: look up by name, then by number ──────────────────────────────────
    def clip_lookup(self):
        chain, cells = self.chain, self.chain.cells

        def at(glyphs, y):
            return [glyphs.get_x(), y, 0]

        def hbox(glyphs, cell):
            return token_box(glyphs, cell.label, color=GOLD).set_z_index(1)

        with self.say("c3.pairs.2") as c:
            q1_name = T('"Cleo"', size=44, color=YELLOW)
            arr_r = MathTex(r"\longrightarrow", font_size=48, color=FG)
            q1_mark = T("?", size=48, color=GOLD)
            VGroup(q1_name, arr_r, q1_mark).arrange(RIGHT, buff=0.35).move_to([-3.5, ROW_Y, 0])
            sweep_clear(self, time_span(FadeIn(q1_name, arr_r, q1_mark, shift=0.3 * DOWN), 0.6, 1.4),
                        keep=[chain, self.book_lbl, self.tag], run_time=1.4)

            c.wait_until("search from the front")
            ptr = marker(GOLD).rotate(PI).move_to(at(cells[0].name_part, PTR_Y))
            self.play(FadeIn(ptr, shift=0.3 * UP), run_time=0.8)
            c.wait_until("comparing names")
            box = hbox(cells[0].name_part, cells[0])
            self.play(GrowFromCenter(box), run_time=0.8)

            # {found} not Amy, not Bob, but Cleo
            c.wait_until("found")
            marks = [cross_mark().move_to(at(cells[0].name_part, MARK_Y))]
            self.play(FadeIn(marks[0], scale=0.5), run_time=0.5)
            for i, cue in ((1, "not Bob"), (2, "but Cleo")):
                c.wait_until(cue)
                m = (cross_mark() if i == 1 else check_mark()).move_to(at(cells[i].name_part, MARK_Y))
                marks.append(m)
                self.play(ptr.animate.move_to(at(cells[i].name_part, PTR_Y)),
                          Transform(box, hbox(cells[i].name_part, cells[i])),
                          time_span(FadeIn(m, scale=0.5), 0.4, 0.8), run_time=0.8)
            c.wait_until("forty-seven")
            ans47 = T("47", size=44, color=GOLD).next_to(arr_r, RIGHT, buff=0.35)
            self.play(TransformFromCopy(cells[2].num_part, ans47), FadeOut(q1_mark, scale=0.5),
                      run_time=1.3)

            # {back} the other way: whose number is 35?
            c.wait_until("back")
            q2_mark = T("?", size=48, color=YELLOW)
            arr_l = MathTex(r"\longleftarrow", font_size=48, color=FG)
            q2_num = T("35", size=44, color=GOLD)
            VGroup(q2_mark, arr_l, q2_num).arrange(RIGHT, buff=0.35).move_to([3.5, ROW_Y, 0])
            self.play(*[FadeOut(m) for m in marks],
                      FadeIn(q2_mark, arr_l, q2_num, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("whose number")
            self.play(ptr.animate.move_to(at(cells[0].num_part, PTR_Y)),
                      Transform(box, hbox(cells[0].num_part, cells[0])), run_time=1.0)
            c.wait_until("compare the numbers")
            x21 = cross_mark().move_to(at(cells[0].num_part, MARK_Y))
            self.play(FadeIn(x21, scale=0.5), run_time=0.5)
            c.wait_until("instead")
            self.play(ptr.animate.move_to(at(cells[1].num_part, PTR_Y)),
                      Transform(box, hbox(cells[1].num_part, cells[1])), run_time=0.5)
            c.wait_until("bob")
            tick35 = check_mark().move_to(at(cells[1].num_part, MARK_Y))
            ans_bob = T('"Bob"', size=44, color=YELLOW).next_to(arr_l, LEFT, buff=0.35)
            self.play(FadeIn(tick35, scale=0.5),
                      time_span(TransformFromCopy(cells[1].name_part, ans_bob), 0.15, 1.0),
                      FadeOut(q2_mark, scale=0.5), run_time=1.0)

        self.ptr = ptr

    # ── c3.pairs.3: slow for big books; pairs from a function ────────────────────────
    def clip_cost_and_squares(self):
        chain, ptr = self.chain, self.ptr
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil

        with self.say("c3.pairs.3") as c:
            ls = T("linear search (last time)", size=32, color=DIM).move_to(UP * TAG_Y)
            slow = T("very slowly", size=34, color=RED)
            row = VGroup(ls.copy(), slow).arrange(RIGHT, buff=0.6).move_to(UP * TAG_Y)
            ls_final = row[0].get_center()
            self.play(FadeTransform(self.tag, ls), run_time=1.0)
            c.wait_until("very slowly")
            self.play(ls.animate.move_to(ls_final), FadeIn(slow, shift=0.2 * LEFT), run_time=1.0)

            # {big} the chain stretches: Amy, Bob, Cleo, ..., []
            c.wait_until("big")
            S = BIG_S
            dots = VGroup(*[Dot(radius=0.055, color=FG) for _ in range(3)]).arrange(RIGHT, buff=0.2)
            dot_x = S * cells[2].dot.get_x()
            dots.move_to([dot_x + 0.75 + dots.width / 2, 0, 0])
            nil_w = S * nil.width
            nil_x = dots.get_right()[0] + 0.8 + nil_w / 2
            left = S * chain.get_left()[0]
            D = RIGHT * (-(left + nil_x + nil_w / 2) / 2) + UP * BIG_Y
            dots.shift(D)
            nil_c = np.array([nil_x, 0, 0]) + D
            new_dot = S * cells[2].dot.get_center() + D
            a2 = ptr_arrow(new_dot, dots.get_left() + LEFT * 0.1)
            a3 = ptr_arrow(dots.get_right() + RIGHT * 0.1, nil_c + LEFT * (nil_w / 2 + 0.05))
            ptr_y = BIG_Y - S * CELL / 2 - 0.32
            gone = [m for m in self.mobjects if m not in (chain, ptr, ls, slow)]
            self.play(*[time_span(FadeOut(m), 0, 0.6) for m in gone],
                      *[m.animate.scale(S, about_point=ORIGIN).shift(D)
                        for m in (*cells, arrows[0], arrows[1])],
                      Transform(arrows[2], a2),
                      nil.animate.scale(S, about_point=ORIGIN).move_to(nil_c),
                      ptr.animate.move_to([S * cells[0].name_part.get_x() + D[0], ptr_y, 0]),
                      time_span(FadeIn(dots), 0.6, 1.1), time_span(GrowArrow(a3), 0.7, 1.2),
                      run_time=1.2)

            c.wait_until("million names")
            top_y = BIG_Y + S * CELL / 2
            brace = Brace(Line([cells[0].get_left()[0], top_y, 0], [nil.get_right()[0], top_y, 0]),
                          direction=UP, buff=0.15).set_color(DIM)
            blabel = T("a million pairs", size=36).next_to(brace, UP, buff=0.12)
            self.play(GrowFromCenter(brace), FadeIn(blabel, shift=0.2 * DOWN), run_time=0.9)

            # a GOLD counter climbs as the pointer sweeps the whole chain
            c.wait_until("million comparisons")
            up_to = T("up to", size=40, color=GOLD)
            slot = Integer(1_000_000, font_size=52, color=GOLD)
            words = T("comparisons", size=40, color=GOLD)
            VGroup(up_to, slot, words).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.2)
            wy = words.get_y()
            tr = ValueTracker(0)
            num = Integer(0, font_size=52).set_color(GOLD)

            def count(m):                    # left edge and baseline stay put as digits appear
                m.set_value(tr.get_value())
                m.set_color(GOLD)
                m.shift(slot[0].get_corner(DL) - m[0].get_corner(DL))

            def follow(w):
                w.next_to(num, RIGHT, buff=0.25).set_y(wy)

            count(num)
            follow(words)
            self.play(FadeIn(up_to, num, words), run_time=0.3)
            num.add_updater(count)
            words.add_updater(follow)
            self.play(tr.animate.set_value(1_000_000),
                      ptr.animate.move_to([nil.get_x(), ptr_y, 0]),
                      rate_func=linear, run_time=1.5)
            num.clear_updaters()
            words.clear_updaters()

            # {square} a list of pairs from a function: each number with its square
            c.wait_until("applying")
            top = Code("[1; 2; 3]", size=48).move_to(UP * 2.1)
            sweep_clear(self, time_span(FadeIn(top, shift=0.3 * DOWN), 0.7, 1.5), run_time=1.5)
            res = Code("[(1, 1); (2, 4); (3, 9)]", size=44).move_to(DOWN * 0.4)
            els = [top.find(str(n)) for n in (1, 2, 3)]
            pairs = [res.find(f"({n}, {n * n})") for n in (1, 2, 3)]
            c.wait_until("each element")
            maps = [Arrow(e.get_bottom() + DOWN * 0.15, p.get_top() + UP * 0.22, buff=0,
                          stroke_width=4, color=YELLOW, tip_length=0.2,
                          max_tip_length_to_length_ratio=0.2) for e, p in zip(els, pairs)]
            self.play(LaggedStart(*[GrowArrow(a) for a in maps], lag_ratio=0.25), run_time=1.2)

            c.wait_until("for instance")
            anims = []
            for g in (res.find("["), res.find(";", nth=0), res.find(";", nth=1), res.find("]")):
                anims += [time_span(FadeIn(x), 0, 0.8) for x in g]
            for i, (e, p) in enumerate(zip(els, pairs)):
                s = 0.4 * i
                anims.append(time_span(TransformFromCopy(e, p[1]), s, s + 1.0))
                anims.append(time_span(TransformFromCopy(e, p[3]), s + 0.2, s + 1.2))
                anims += [time_span(FadeIn(p[k]), s, s + 0.8) for k in (0, 2, 4)]
            self.play(*anims, run_time=0.8 + 1.2)
            settle(self, res)

            c.wait_until("with its square")
            lab = T("each number, with its square", size=36).move_to(DOWN * 1.5)
            self.play(FadeIn(lab, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("later")
            later = T("how to write it: a later lecture", size=32, color=DIM).move_to(DOWN * 2.7)
            self.play(FadeIn(later, shift=0.2 * DOWN), run_time=1.0)
        self.wait(2.0)   # let the last lines sit before the frame clears
