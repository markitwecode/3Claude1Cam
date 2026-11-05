"""Chapter 3, scene 2: the two cases of a list as two cards (empty: 0; head on a tail:
1 + length of xs), then nlength in OCaml, why it needs `rec` (OCaml's real error without it),
and the deeper idea: one clause per shape, each call on a shorter tail.

Clips c3.def.1 – c3.def.4.

STATUS: done; check.py clean (no overruns, dwell or layout flags). Fix pass: def.3 overrun
(last play now 0.9 x the time left), self-reference arrow now ends under `nlength` (it pointed
at line 1's `0`), code lowered (CODE_Y -0.5) so naive/recursive sit clear of the cards, chain
lowered to match, "tail" cue in def.4 now nth=1. The no-rec error text is OCaml 5.4.1's real
output (verified with `ocaml`).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, select, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = """let rec nlength = function
  | [] -> 0
  | x :: xs -> 1 + nlength xs"""

LBL = 48            # card labels at hero size (x CARD_S = 30 in the top band)
NUM = 60            # the GOLD numbers on the cards
PIC = 1.3           # cell size on the cards
HERO_Y = 0.0        # the cards' row in def.1
CARD_S = 0.62       # the cards shrink to this when the code arrives ...
TOP_Y = 2.45        # ... and move up to this row
CODE_Y = -0.5         # low enough to leave room for the naive/recursive labels
DIM_TO = 0.3        # spotlight level for the card not being talked about (P9)


# ── helpers (local to this scene) ───────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph and then swapped for the whole object
# (settle); never wrapped in a Group (LESSONS.md).
def restyle(mob, op=None, scale=None, center=None):
    """One Transform that dims/restores (P9), scales and moves `mob` together. Opacity goes
    on the fill of filled parts (text, tips, cells) and on the stroke of bare outlines."""
    t = mob.copy()
    if op is not None:
        for leaf in t.family_members_with_points():
            if leaf.get_fill_opacity() > 0:
                leaf.set_opacity(op)
            else:
                leaf.set_stroke(opacity=op)
    if scale is not None:
        t.scale(scale)
    if center is not None:
        t.move_to(center)
    return Transform(mob, t)


def code_box(code, glyphs, lines, color=YELLOW):
    """The sliding highlight (P8): as tall as the code lines it covers, as wide as the
    glyphs, thin stroke and faint fill, behind the text."""
    g = VGroup(*glyphs)
    ls = VGroup(*[code.line(i) for i in lines])
    top, bot = ls.get_top()[1], ls.get_bottom()[1]
    r = Rectangle(width=g.width + 0.22, height=top - bot + 0.16)
    r.move_to([g.get_x(), (top + bot) / 2, 0])
    return r.set_stroke(color, 2).set_fill(color, opacity=0.2).set_z_index(-1)


def mono_cell(name):
    """A cons cell at card size whose value is a name in code font (x)."""
    cell = ConsCell(name).scale(PIC)
    cell.remove(cell.label)
    cell.label = Mono(name, size=LBL).move_to(cell.box)
    cell.add(cell.label)
    return cell


def baseline_row(*parts, buff=0.22):
    """Words/symbols side by side, sitting on one baseline (the first part's first glyph)."""
    row = VGroup(*parts).arrange(RIGHT, buff=buff)
    base = parts[0][0].get_bottom()[1]
    for p in parts[1:]:
        if isinstance(p, Text) and p.text in ("+", "="):
            p.set_y(parts[0][1].get_y() if len(parts[0]) > 1 else p.get_y())
        else:
            p.shift(UP * (base - p[0].get_bottom()[1]))
    return row


def connector(start, end, out):
    """A TEAL link that leaves `start` sideways, runs out to x = `out` and comes back into
    `end` sideways, with a dot at each end."""
    path = CubicBezier(start, [out, start[1], 0], [out, end[1], 0], end).set_stroke(TEAL, 3)
    return path, Dot(start, radius=0.06, color=TEAL), Dot(end, radius=0.06, color=TEAL)


class FollowingTheShape(NarratedScene):
    def construct(self):
        self.build_cards()
        self.two_cases()
        self.the_code()
        self.recursion()
        self.the_shape()
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.06),
                  run_time=1.2)
        self.wait(0.1)  # a truly empty last frame

    def settle(self, card, add=(), drop=()):
        """Make freshly animated pieces part of their card (and drop replaced ones), then
        put the whole card back on screen as one object."""
        card.remove(*drop)
        self.remove(*card.get_family(), *add)
        card.add(*add)
        self.add(card)

    # ── the two cards, laid out once (P4) ──────────────────────────────────────
    def build_cards(self):
        # left: the empty list
        nil = Nil(size=110)
        nil.scale_to_fit_height(1.05).move_to(DOWN * 0.6)
        b_nil = Brace(nil, UP, buff=0.2, color=DIM)
        q_l = T("?", size=NUM, color=GOLD).next_to(b_nil, UP, buff=0.15)
        zero = T("0", size=NUM, color=GOLD).next_to(b_nil, UP, buff=0.15)

        # right: a head, x, on a tail, xs (a dashed box: we don't know how long it is)
        cell = mono_cell("x")
        tail = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=3.6, height=PIC),
                              num_dashes=44).set_stroke(BLUE, 3)
        tail.next_to(cell, RIGHT, buff=0.9)
        xs = Mono("xs", size=LBL).move_to(tail)
        arrow = Arrow(cell.tail_start(), tail.get_left(), buff=0, stroke_width=3, color=FG,
                      max_tip_length_to_length_ratio=0.3, tip_length=0.2)
        pic = VGroup(cell, arrow, tail, xs).move_to(DOWN * 0.6)
        b_all = Brace(pic, UP, buff=0.2, color=DIM)
        q_r = T("?", size=NUM, color=GOLD).next_to(b_all, UP, buff=0.15)
        b_head = Brace(VGroup(cell.box, cell.ptr), UP, buff=0.2, color=DIM)
        b_tail = Brace(tail, UP, buff=0.2, color=DIM)
        len_xs = baseline_row(T("length of", size=LBL), Mono("xs", size=LBL), buff=0.2)
        len_xs.next_to(b_tail, UP, buff=0.15)
        one = T("1", size=NUM, color=GOLD).next_to(b_head, UP, buff=0.15)
        one.align_to(len_xs[0][0], DOWN)
        plus = T("+", size=LBL).move_to([(one.get_right()[0] + len_xs.get_left()[0]) / 2,
                                         len_xs[0][1].get_y(), 0])

        # frames: same height, side by side, the row centred
        pad = 0.42
        top = one.get_top()[1] + pad
        bot = pic.get_bottom()[1] - pad
        f_r = RoundedRectangle(corner_radius=0.25, width=pic.width + 2 * pad + 0.2, height=top - bot)
        f_r.move_to([pic.get_x(), (top + bot) / 2, 0])
        f_l = RoundedRectangle(corner_radius=0.25, width=2.7, height=top - bot)
        f_l.move_to([nil.get_x(), (top + bot) / 2, 0])
        for f in (f_l, f_r):
            f.set_stroke(DIM, 2.5)
        left = VGroup(f_l, nil)
        right = VGroup(f_r, pic)
        # place the left card beside the right one, then centre the row (labels included)
        left_parts = VGroup(left, b_nil, q_l, zero)
        left_parts.shift(RIGHT * (f_r.get_left()[0] - 0.6 - f_l.get_right()[0]))
        row = VGroup(left_parts, right, b_all, q_r, b_head, b_tail, len_xs, one, plus)
        row.shift(UP * (HERO_Y - f_r.get_y()) + LEFT * VGroup(f_l, f_r).get_x())

        self.cards = dict(left=left, right=right, nil=nil, b_nil=b_nil, q_l=q_l, zero=zero,
                          cell=cell, tail=tail, xs=xs, b_all=b_all, q_r=q_r, b_head=b_head,
                          b_tail=b_tail, len_xs=len_xs, one=one, plus=plus, f_l=f_l, f_r=f_r)

    # def.1: empty -> 0; head on a tail -> 1 + length of xs
    def two_cases(self):
        k = self.cards
        left, right = k["left"], k["right"]

        with self.say("c3.def.1") as c:
            # "The trick is to think about the two kinds of list, one at a time."  Both shapes
            # first (P2), then one at a time.
            self.play(FadeIn(left, shift=0.3 * UP), time_span(FadeIn(right, shift=0.3 * UP), 0.4, 1.8),
                      run_time=1.8)

            # "First, the empty list."
            c.wait_until("empty")
            self.play(restyle(right, DIM_TO), FlashAround(k["nil"], color=TEAL, time_width=1.5),
                      run_time=1.2)
            # "How long is it?"
            c.wait_until("how long is it")
            self.play(GrowFromCenter(k["b_nil"]), FadeIn(k["q_l"], shift=0.25 * DOWN),
                      run_time=1.0)
            # "Zero, of course."  The question turns into the answer (P23).
            c.wait_until("zero")
            self.play(FadeTransform(k["q_l"], k["zero"]), run_time=1.2)
            self.settle(left, add=[k["b_nil"], k["zero"]])

            # "Second, a head, ex, consed onto a tail, exes."
            c.wait_until("cons")
            self.play(restyle(left, 0.4), restyle(right, 1), run_time=1.0)
            c.wait_until("head")
            self.play(FlashAround(k["cell"], color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("a tail")
            self.play(FlashAround(k["tail"], color=BLUE, time_width=1.5), run_time=1.0)
            # "How long is that?"
            c.wait_until("how long is that")
            self.play(GrowFromCenter(k["b_all"]), FadeIn(k["q_r"], shift=0.25 * DOWN), run_time=1.0)

            # "It's one more than the length of exes."  The one brace splits in two: 1 for the
            # head, plus the length of the tail.
            c.wait_until("plus")
            self.play(ReplacementTransform(k["b_all"], k["b_head"]),
                      TransformFromCopy(k["b_all"], k["b_tail"]),
                      FadeTransform(k["q_r"], k["one"]),
                      time_span(FadeIn(k["plus"], shift=0.25 * DOWN), 1.0, 1.9),
                      time_span(FadeIn(k["len_xs"], shift=0.25 * DOWN), 1.1, 2.0), run_time=2.0)
            self.settle(right, add=[k["b_head"], k["b_tail"], k["one"], k["plus"], k["len_xs"]])

            # "One for the head, plus however many elements are in the tail."
            c.wait_until("one for the head")
            self.play(FlashAround(VGroup(k["cell"], k["one"]), color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("plus however")
            self.play(FlashAround(VGroup(k["tail"], k["len_xs"]), color=GOLD, time_width=1.5), run_time=1.2)

    # def.2: the same thing in OCaml; the box slides over the clauses (P8)
    def the_code(self):
        k = self.cards
        left, right = k["left"], k["right"]
        code = Code(SRC, size=40).move_to(UP * CODE_Y)
        code.find("nlength", line=2).set_color(YELLOW)   # the name keeps its colour everywhere
        self.code = code
        name = code.find("nlength", line=0)
        naive = T("naive", size=32)
        naive[0].set_color(YELLOW)
        naive.shift(name[0].get_center() - naive[0].get_center())
        self.naive = naive

        # where the cards go: the row shrinks into the top band
        row_end = VGroup(left, right).copy().scale(CARD_S).move_to(UP * TOP_Y)
        naive.set_y((row_end.get_bottom()[1] + code.get_top()[1]) / 2)   # midway, clear of both

        def box(sub, lines, nth=0):
            return code_box(code, code.find(sub, line=lines[0], nth=nth), lines)

        bars = [*code.find("|", line=1), *code.find("|", line=2)]

        with self.say("c3.def.2") as c:
            # "And that's exactly what you write in OCaml."
            self.play(restyle(left, 1, CARD_S, row_end[0].get_center()),
                      restyle(right, 1, CARD_S, row_end[1].get_center()),
                      time_span(FadeIn(code, shift=0.3 * UP), 0.7, 2.0), run_time=2.0)

            # "We'll call this function en-length."
            c.wait_until("function")
            self.play(FlashAround(name, color=YELLOW, time_width=1.5), run_time=1.2)
            # "The en stands for naive, just like en-sum in lecture two, and you'll soon see why."
            c.wait_until("naive")
            self.play(FadeIn(naive, shift=0.25 * DOWN),
                      FlashAround(name[0], color=YELLOW, buff=0.06, time_width=1.5), run_time=1.1)

            # "The function has two clauses, each starting with a vertical bar."
            c.wait_until("two clauses")
            hb = code_box(code, [*code.line(1), *code.line(2)], (1, 2))
            self.play(FadeIn(hb), run_time=1.0)
            c.wait_until("vertical bar")
            self.play(hb.animate.become(code_box(code, bars, (1, 2))), run_time=1.0)

            # "The empty list gives zero."  (its card stays lit, the other steps back)
            c.wait_until("nil")
            self.play(hb.animate.become(code_box(code, code.line(1), (1,))), restyle(right, DIM_TO),
                      run_time=1.2)
            # "And ex consed onto exes gives one, plus en-length of exes."
            c.wait_until("step")
            self.play(hb.animate.become(box("x :: xs", (2,))), restyle(right, 1), restyle(left, DIM_TO),
                      run_time=1.2)
            c.wait_until("gives one")
            self.play(hb.animate.become(box("1 + nlength xs", (2,))), run_time=1.2)
        self.hb = hb

    # def.3: nlength calls itself, hence `let rec`; without it, OCaml's real error
    def recursion(self):
        k, code, hb = self.cards, self.code, self.hb
        name = code.find("nlength", line=0)
        use = code.find("nlength", line=2)
        rec = code.find("rec", line=0)
        rest = code.find("nlength = function", line=0)
        dx = rec.get_left()[0] - rest.get_left()[0]           # "rec " closes up when left out

        # ends under the right half of the name, clear of line 1's `0`
        self_arrow = CurvedArrow(use[1].get_top() + UP * 0.1, name[5].get_bottom() + DOWN * 0.1,
                                 angle=-PI / 4, color=YELLOW, stroke_width=4, tip_length=0.2)
        recursive = T("recursive", size=32)
        recursive[:3].set_color(BLUE)
        recursive.shift(rec.get_center() - VGroup(*recursive[:3]).get_center())
        recursive.set_y(self.naive.get_y())

        err = VGroup(Mono("Error: Unbound value nlength", size=30, color=RED),
                     Mono("Hint: If this is a recursive definition,", size=30, color=RED),
                     Mono("you should add the rec keyword on line 1", size=30, color=RED))
        err.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        err.next_to(code, DOWN, buff=0.4).align_to(code, LEFT)
        # OCaml marks the unknown name with carets; underline it the same way
        carets = Line(use.get_corner(DL), use.get_corner(DR), color=RED, stroke_width=4).shift(DOWN * 0.1)
        hint_rec = select(err[2], "rec")[0]

        with self.say("c3.def.3") as c:
            # "Notice that en-length calls itself, on the tail."
            self.play(restyle(k["left"], 1), hb.animate.become(code_box(code, use, (2,))), run_time=1.0)
            c.wait_until("calls itself")
            self.play(Create(self_arrow), run_time=1.3)
            c.wait_until("on the tail")
            self.play(hb.animate.become(code_box(code, code.find("xs", line=2, nth=1), (2,))), run_time=0.8)

            # "That's why the definition starts with let rec, short for recursive, and not just let."
            c.wait_until("let rec")
            self.play(FadeOut(self.naive), hb.animate.become(code_box(code, rec, (0,))),
                      FlashAround(rec, color=BLUE, time_width=1.5), run_time=1.0)
            c.wait_until("recursive")
            self.play(FadeIn(recursive, shift=0.25 * DOWN), run_time=1.0)

            # "It tells OCaml that the name en-length can be used inside its own definition."
            c.wait_until("the name")
            self.play(FlashAround(name, color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("used inside")
            self.play(FlashAround(use, color=YELLOW, time_width=1.5),
                      VShowPassingFlash(self_arrow.copy().remove(self_arrow.tip).set_stroke(YELLOW, 8),
                                        time_width=0.5), run_time=1.4)

            # "Leave out the rec, ..."
            c.wait_until("norec")
            self.play(FadeOut(hb), FadeOut(self_arrow), FadeOut(recursive), run_time=0.8)
            c.wait_until("the rec")
            self.play(*[FadeOut(g, shift=0.3 * UP) for g in rec],
                      *[g.animate.shift(RIGHT * dx) for g in rest], run_time=1.2)
            # "... and OCaml rejects the code."  Its reply, word for word (OCaml 5.4.1).
            c.wait_until("rejects")
            self.play(LaggedStart(*[FadeIn(line, shift=0.25 * DOWN) for line in err], lag_ratio=0.3),
                      Create(carets), run_time=1.5)
            # "It says en-length isn't defined yet, ..."
            c.wait_until("isn't defined")
            self.play(FlashUnder(select(err[0], "Unbound value nlength")[0], color=RED, time_width=1.5),
                      run_time=1.0)
            # "... and even suggests adding the rec."  The hint's rec goes back where it belongs.
            c.wait_until("even suggests")
            self.play(*[TransformFromCopy(h, g) for h, g in zip(hint_rec, rec)],
                      *[g.animate.shift(LEFT * dx) for g in rest],
                      run_time=min(1.5, 0.9 * c.until(None, floor=1.0)))
            self.remove(*code.get_family())
            self.add(code)
        self.err, self.carets = err, carets

    # def.4: one clause per shape; each call on a shorter tail, down to the empty list
    def the_shape(self):
        k, code = self.cards, self.code
        f_l, f_r = k["f_l"], k["f_r"]
        bar = code.find("|", line=1)[0]
        l_path, l_d0, l_d1 = connector(bar.get_left() + LEFT * 0.18, f_l.get_left(), out=-6.0)
        end_r = code.find("xs", line=2, nth=1).get_right() + RIGHT * 0.18
        r_path, r_d0, r_d1 = connector(end_r, f_r.get_right(), out=6.15)

        chain = ConsChain([5, 6, 7]).scale(0.75).move_to(DOWN * 2.45)
        cap = T("each call: one element shorter", size=32).next_to(chain, DOWN, buff=0.35)
        use_xs = code.find("nlength xs", line=2)

        with self.say("c3.def.4") as c:
            # "Here's the deeper idea."  The error has done its job and steps back.
            self.play(*[line.animate.set_opacity(0.4) for line in self.err], FadeOut(self.carets),
                      run_time=1.0)

            # "A list is either empty, or a head on a tail, and the function has a clause for
            # each of those two shapes."  Each clause links to its card.
            c.wait_until("either empty")
            self.play(Create(l_path), FadeIn(l_d0), time_span(FadeIn(l_d1), 0.8, 1.2),
                      f_l.animate.set_stroke(TEAL), run_time=1.2)
            c.wait_until("head on a tail")
            self.play(Create(r_path), FadeIn(r_d0), time_span(FadeIn(r_d1), 0.8, 1.2),
                      f_r.animate.set_stroke(TEAL), run_time=1.2)
            c.wait_until("a clause for each")
            self.play(FlashAround(code.line(1), color=TEAL, time_width=1.5),
                      FlashAround(code.line(2), color=TEAL, time_width=1.5), run_time=1.3)

            # "Each recursive call works on the tail, which is one element shorter."
            c.wait_until("smaller")
            hb = code_box(code, use_xs, (2,))
            self.play(LaggedStart(*[FadeOut(line) for line in self.err], lag_ratio=0.15),
                      time_span(FadeIn(chain, shift=0.3 * UP), 0.6, 1.6), FadeIn(hb), run_time=1.6)
            cells, arrows = chain.cells, chain.arrows

            def peel(i):
                return [cells[i].animate.set_opacity(0.15), arrows[i].animate.set_opacity(0.15)]

            c.wait_until("tail", nth=1)      # "on the tail" (nth=0 is "a head on a tail")
            self.play(*peel(0), run_time=1.0)
            c.wait_until("one element shorter")
            self.play(FadeIn(cap, shift=0.25 * DOWN), run_time=1.0)

            # "So the calls must eventually reach the empty list, and that's where they stop."
            c.wait_until("ends")
            self.play(*peel(1), run_time=0.8)
            c.wait_until("eventually")
            self.play(*peel(2), run_time=0.8)
            c.wait_until("empty list")
            self.play(FlashAround(chain.nil, color=TEAL, time_width=1.5),
                      hb.animate.become(code_box(code, code.line(1), (1,))), run_time=1.1)
            c.wait_until("where they stop")
            self.play(FlashAround(f_l, color=TEAL, time_width=1.5),
                      VShowPassingFlash(l_path.copy().set_stroke(TEAL, 7), time_width=0.5), run_time=1.2)

            # "Most functions on lists work this way. The recursion follows the shape of the data."
            c.wait_until("follows the shape")
            self.play(VShowPassingFlash(l_path.copy().set_stroke(TEAL, 7), time_width=0.5),
                      VShowPassingFlash(r_path.copy().set_stroke(TEAL, 7), time_width=0.5),
                      FlashAround(f_l, color=TEAL, time_width=1.5),
                      FlashAround(f_r, color=TEAL, time_width=1.5), run_time=1.5)
