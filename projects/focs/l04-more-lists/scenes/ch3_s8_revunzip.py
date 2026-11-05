"""Chapter 3, scene 8: revUnzip, iterative but backwards; the extra reversal it forces; the
chapter recap and the end card (ch4 teaser: coins and a till). Clips c3.rev.1 – c3.rev.4.

Layout
- rev.1: s5's and s7's unzips stacked (size 28; side by side would need ~18 units), DIM
  "waiting" tags on their cons steps. Then the hero revUnzip (size 38), braces under the three
  arguments of its recursive call, OCaml's reply under it (size 28, wrapped after "->" as s7
  wraps conspair's reply).
- rev.2: L3 ch4's card piles in a top band (pairs | xs | ys, labels left of each pile), the
  trace under them (size 26, each row born from the one above, DIM => as in L3), the reply at
  the bottom (wrapped after "=" with OCaml's 2-space indent: one line would be 67 characters).
- rev.3: the fixed call + reply, List.rev book's three new cells (ch2's pair cells), the cost
  comparison, then the Lecture 3 caveat.
- rev.4: ch2-style recap (title, five lines that step back to 0.5) and the end card.

STATUS: built; re-synced to the re-voiced c3.rev.1 / c3.rev.3. Check clean except dwell on the
5 s s5/s7 callback (the narration moves on) and small-text notes on the trace (size 26) and the
0.7-scaled recap on the end card (24).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

UNZIP_LET = ("let rec unzip = function\n"
             "  | [] -> ([], [])\n"
             "  | (x, y)::pairs ->\n"
             "      let xs, ys = unzip pairs in\n"
             "      (x::xs, y::ys)")
UNZIP_CP = ("let rec unzip = function\n"
            "  | [] -> ([], [])\n"
            "  | xy :: pairs -> conspair (xy, unzip pairs)")
REV = ("let rec revUnzip = function\n"
       "  | ([], xs, ys) -> (xs, ys)\n"
       "  | ((x, y)::pairs, xs, ys) ->\n"
       "      revUnzip (pairs, x::xs, y::ys)")
REV_REPLY = ("val revUnzip : ('a * 'b) list * 'a list * 'b list ->\n"
             "  'a list * 'b list = <fun>")
TRACE = ['revUnzip ([("Amy", 21); ("Bob", 35); ("Cleo", 47)], [], [])',
         'revUnzip ([("Bob", 35); ("Cleo", 47)], ["Amy"], [21])',
         'revUnzip ([("Cleo", 47)], ["Bob"; "Amy"], [35; 21])',
         'revUnzip ([], ["Cleo"; "Bob"; "Amy"], [47; 35; 21])',
         '(["Cleo"; "Bob"; "Amy"], [47; 35; 21])']
BACK = '(["Cleo"; "Bob"; "Amy"], [47; 35; 21])'
BACK_NAMES, BACK_NUMS = '["Cleo"; "Bob"; "Amy"]', "[47; 35; 21]"
TRACE_REPLY = "- : string list * int list =\n  " + BACK
FIX = "revUnzip (List.rev book, [], [])"
FIXED = '(["Amy"; "Bob"; "Cleo"], [21; 35; 47])'
FIX_REPLY = "- : string list * int list =\n  " + FIXED
BOOK = [("Amy", 21), ("Bob", 35), ("Cleo", 47)]
COINS = [50, 20, 10, 5, 2, 1]

# ── layout ──────────────────────────────────────────────────────────────────────
OLD_SIZE, OLD_LEFT, OLD_TOPS = 28, -6.1, (2.75, -0.7)
HERO, HERO_Y = 38, 1.25
REPLY_SIZE, REPLY_Y = 28, -2.0
LABEL = 30

CARD_H, HALF_W, SLOT = 0.6, 1.2, 0.68
PILE_BASE = 1.62
PILE_X = (-3.4, 0.9, 4.0)        # pairs, xs, ys
ROW_SIZE, XL, ARROW_W = 26, -6.35, 0.8
BASE = [0.6, -0.02, -0.64, -1.26, -1.88]
REPLY2_BASE = -2.62
ARC = -0.9

FIX_Y, CELLS_Y, COST_Y, COMP_Y = 2.95, 0.4, -0.75, -1.95
COMP_UP, LEC_Y, RULE_Y = 0.95, -0.75, -1.4

TITLE_Y = 3.1
ROW_Y = (1.85, 0.8, -0.25, -1.3, -2.35)
TEXT_SIZE, SAID = 34, 0.5
END_SCALE, END_TOP, END_OP = 0.7, 3.55, 0.45
NEXT_Y, TEASE_Y = -0.65, -2.25
END_CARD = 8.0

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789")


# ── code helpers ────────────────────────────────────────────────────────────────
def C(src, size, line_spacing=0.9):
    """Code with every function name YELLOW and every 'b PURPLE."""
    code = Code(src, size=size, line_spacing=line_spacing)
    for m in re.finditer(r"\brevUnzip\b|\bunzip\b|\bconspair\b", code.src):
        code._span(m.start(), m.end()).set_color(YELLOW)
    for m in re.finditer(r"'b", code.src):
        code._span(m.start(), m.end()).set_color(PURPLE)
    return code


def baseline(code):
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its (first line's) baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def part(code, sub, nth=0, line=None):
    """The glyphs of `sub` in `code`, as a fresh VGroup (never added to the scene itself)."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def implies(row, base):
    return (MathTex(r"\Rightarrow", font_size=44, color=DIM)
            .next_to(row, LEFT, buff=0.25).set_y(base + 0.1))


def birth(dst, moves):
    """Animations that build `dst` (a Code not on screen yet) out of copies of glyphs elsewhere.
    moves: (src, src_sub, src_nth, dst_sub, dst_nth, path_arc). Glyphs of dst not moved fade in.
    Returns (anims, wrappers); commit() swaps the wrappers for dst once the play is over."""
    anims, wrappers, used = [], [], set()
    for src, s_sub, s_nth, d_sub, d_nth, arc in moves:
        tgt = part(dst, d_sub, d_nth)
        anims.append(TransformFromCopy(part(src, s_sub, s_nth), tgt, path_arc=arc))
        wrappers.append(tgt)
        used |= {id(g) for g in tgt}
    rest = [g for g in dst.text if id(g) not in used]
    if rest:
        r = VGroup(*rest)
        anims.append(FadeIn(r, shift=0.15 * DOWN))
        wrappers.append(r)
    return anims, wrappers


# ── text helpers ────────────────────────────────────────────────────────────────
def tline(text, size=TEXT_SIZE, monos=(), color=FG):
    """Serif text with some substrings set in the code font, coloured."""
    t2f, t2c = {}, {}
    for sub, col in monos:
        i = text.index(sub)
        key = f"[{i}:{i + len(sub)}]"
        t2f[key], t2c[key] = MONO, col
    t = T(text, size=size, color=color, t2f=t2f, t2c=t2c)
    t.src = text
    return t


def text_base(t):
    chars = [ch for ch in t.src if not ch.isspace()]
    for ch, g in zip(chars, t):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return t.get_bottom()[1]


def two_part(a, b, buff=0.16):
    b.next_to(a, RIGHT, buff=buff)
    b.shift(UP * (text_base(a) - text_base(b)))
    return VGroup(a, b)


def multiply_opacity(mob, k):
    """Scale every part's opacity by k in place (ch2's recap)."""
    for leaf in mob.family_members_with_points():
        leaf.set_fill(opacity=leaf.get_fill_opacity() * k, family=False)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * k, family=False)
    return mob


def faded(mob, k):
    return multiply_opacity(mob.copy(), k)


# ── cards and piles (L3 ch4's rev_app) ─────────────────────────────────────────
def half_card(text, color):
    box = RoundedRectangle(width=HALF_W, height=CARD_H, corner_radius=0.1, stroke_color=BLUE,
                           stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(box, T(text, size=30, color=color).move_to(box))


def outline(w):
    """An empty pile: a dashed card-shaped slot."""
    return DashedVMobject(RoundedRectangle(width=w, height=CARD_H, corner_radius=0.1,
                                           stroke_color=DIM, stroke_width=3), num_dashes=22)


def slot(x, k):
    return np.array([x, PILE_BASE + SLOT * k, 0.0])


# ── s4's tuple cells (scenes/ch3_s4_pairs.py, copied: keep in step) ─────────────────
PAIR_W = 2.7        # value-box width of a tuple cell (height CELL = 1.0, pointer box PTR_W)
PAIR_SIZE = 30      # tuple text inside the cell: CMU Serif (like value_label), FG
PAIR_LINK = 0.6     # arrow length between tuple cells


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
        self.label.set_z_index(2)
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


# ── the teaser: coins and a till ────────────────────────────────────────────────
def coin(v, r):
    disc = Circle(radius=r, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.14)
    return VGroup(disc, T(str(v), size=32, color=GOLD).move_to(disc))


def till():
    body = Polygon([-1.0, -0.42, 0], [1.0, -0.42, 0], [0.82, 0.42, 0], [-0.82, 0.42, 0],
                   stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=1)
    keys = VGroup(*[Square(0.17, stroke_color=BLUE, stroke_width=2) for _ in range(6)])
    keys.arrange_in_grid(rows=2, cols=3, buff=0.1).move_to(body).shift(0.05 * DOWN)
    stalk = Line([0.5, 0.42, 0], [0.5, 0.62, 0], stroke_color=BLUE, stroke_width=3)
    display = Rectangle(width=0.9, height=0.34, stroke_color=BLUE, stroke_width=3)
    display.move_to([0.5, 0.79, 0])
    drawer = Rectangle(width=2.3, height=0.42, stroke_color=BLUE, stroke_width=3,
                       fill_color=BG, fill_opacity=1).next_to(body, DOWN, buff=0)
    handle = Line(LEFT * 0.25, RIGHT * 0.25, stroke_color=BLUE, stroke_width=4).move_to(drawer)
    t = VGroup(body, keys, stalk, display, drawer, handle)
    t.drawer = drawer
    return t


class RevUnzip(NarratedScene):
    def construct(self):
        self.iterative()      # c3.rev.1
        self.trace()          # c3.rev.2
        self.the_fix()        # c3.rev.3
        self.recap()          # c3.rev.4
        # End card: the dimmed recap and the teaser hold, fully visible, under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.3)
        self.wait(0.15)

    # ── c3.rev.1: neither unzip is iterative; revUnzip ────────────────────────────
    def iterative(self):
        u1 = C(UNZIP_LET, OLD_SIZE)
        u1.move_to([OLD_LEFT, OLD_TOPS[0], 0], aligned_edge=UL)
        u2 = C(UNZIP_CP, OLD_SIZE)
        u2.move_to([OLD_LEFT, OLD_TOPS[1], 0], aligned_edge=UL)
        waits = []
        for code, sub, line in ((u1, "(x::xs, y::ys)", 4), (u2, "conspair (xy, unzip pairs)", 2)):
            box = SurroundingRectangle(part(code, sub, line=line), color=DIM, buff=0.1,
                                       stroke_width=2, corner_radius=0.06)
            tag = T("waiting", size=LABEL, color=DIM).next_to(box, RIGHT, buff=0.25)
            waits += [box, tag]

        code = self.code = C(REV, HERO).move_to([0, HERO_Y, 0])
        reply = C(REV_REPLY, REPLY_SIZE).move_to([0, REPLY_Y, 0])
        l3 = code.line(3)
        y_low = min(g.get_bottom()[1] for g in l3)
        slots = [code.find(s, line=3) for s in ("pairs", "x::xs", "y::ys")]

        def brace(glyphs, color):
            g = VGroup(*glyphs)
            return span_brace(np.array([g.get_left()[0], y_low, 0]),
                              np.array([g.get_right()[0], y_low, 0]), DOWN, color)

        braces = [brace(slots[0], DIM), brace(slots[1], TEAL), brace(slots[2], TEAL)]
        labs = [T(s, size=LABEL, color=col).next_to(b, DOWN, buff=0.12)
                for s, col, b in zip(("pairs to do", "xs so far", "ys so far"),
                                     (FG, TEAL, TEAL), braces)]

        with self.say("c3.rev.1") as c:
            # "Both versions of unzip leave work waiting on the way back, so neither is iterative."
            self.play(time_span(FadeIn(u1, shift=0.2 * DOWN), 0, 1.0),
                      time_span(FadeIn(u2, shift=0.2 * DOWN), 0.3, 1.3), run_time=1.3)
            c.wait_until("work waiting")
            self.play(*[FadeIn(m, shift=0.15 * LEFT) for m in waits], run_time=0.9)

            # "Making it iterative gives this function, rev-unzip."
            c.wait_until("acc")
            sweep_clear(self, time_span(FadeIn(code, shift=0.3 * DOWN), 0.5, 1.6), run_time=1.6)
            c.wait_until("this function")
            self.play(FadeIn(reply, shift=0.2 * DOWN), run_time=1.0)

            # "It takes a triple, made of the remaining pairs, and two accumulators, exes and whys."
            c.wait_until("triple")
            self.play(*[time_span(GrowFromCenter(b), 0.2 * i, 0.2 * i + 0.8)
                        for i, b in enumerate(braces)], run_time=1.2)
            c.wait_until("the remaining pairs")
            self.play(FadeIn(labs[0], shift=0.3 * DOWN), run_time=0.9)
            c.wait_until("two accumulators")
            self.play(time_span(FadeIn(labs[1], shift=0.3 * DOWN), 0, 0.8),
                      time_span(FadeIn(labs[2], shift=0.3 * DOWN), 0.3, 1.1), run_time=1.1)

            # "When the pairs are used up, it returns the two accumulators."
            c.wait_until("base")
            box = token_box(code.find("([], xs, ys) -> (xs, ys)", line=1), code.line(1))
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("returns the two accumulators")
            self.play(FlashAround(part(code, "(xs, ys)", line=1), color=TEAL, time_width=1.5),
                      run_time=1.2)

            # "Otherwise, it conses ex onto exes, and why onto whys, and carries on with the rest."
            c.wait_until("step")
            b2 = token_box(code.find("((x, y)::pairs, xs, ys) ->", line=2), code.line(2))
            b3 = token_box(code.line(3), code.line(3))
            left = min(b2.get_left()[0], b3.get_left()[0])
            right = max(b2.get_right()[0], b3.get_right()[0])
            box2 = b2.copy().stretch_to_fit_width(right - left).stretch_to_fit_height(
                b2.get_top()[1] - b3.get_bottom()[1])
            box2.move_to([(left + right) / 2, (b2.get_top()[1] + b3.get_bottom()[1]) / 2, 0])
            self.play(Transform(box, box2), run_time=1.0)
            c.wait_until("conses ex onto exes")
            self.play(TransformFromCopy(code.find("x", line=2)[0], code.find("x", line=3)[0],
                                        path_arc=0.6 * PI),
                      run_time=min(1.2, max(0.6, c.until("why onto whys") - 0.1)))
            c.wait_until("why onto whys")
            self.play(TransformFromCopy(code.find("y", line=2)[0], code.find("y", line=3)[0],
                                        path_arc=0.6 * PI), run_time=1.1)
            c.wait_until("carries on with the rest")
            self.play(FlashAround(VGroup(*slots[0]), color=YELLOW, time_width=1.5), run_time=1.1)

            # "Iteration can build several results at once, each in its own argument position."
            c.wait_until("many")
            self.play(FadeOut(box), run_time=0.8)
            c.wait_until("each in its own")
            d = max(1.2, min(2.2, c.remaining - 0.1))
            self.play(*[time_span(FlashAround(VGroup(*s), color=col, time_width=1.5),
                                  i * d / 4, i * d / 4 + d / 2)
                        for i, (s, col) in enumerate(zip(slots, (YELLOW, TEAL, TEAL)))], run_time=d)

    # ── c3.rev.2: the trace, one pair card per call ──────────────────────────────
    def step(self, k, run_time, extra=()):
        """Pair card k splits; its halves land on the xs and ys piles while row k+1 is born
        from row k."""
        MOVES = [
            [("revUnzip ([", 0, "revUnzip ([", 0, 0),
             ('("Bob", 35); ("Cleo", 47)]', 0, '("Bob", 35); ("Cleo", 47)]', 0, 0),
             ('"Amy"', 0, '"Amy"', 0, ARC), ("21", 0, "21", 0, ARC)],
            [("revUnzip ([", 0, "revUnzip ([", 0, 0), ('("Cleo", 47)]', 0, '("Cleo", 47)]', 0, 0),
             ('"Bob"', 0, '"Bob"', 0, ARC), ("35", 0, "35", 0, ARC),
             ('"Amy"]', 0, '"Amy"]', 0, 0), ("21]", 0, "21]", 0, 0)],
            [("revUnzip ([", 0, "revUnzip ([", 0, 0),
             ('"Cleo"', 0, '"Cleo"', 0, ARC), ("47", 0, "47", 0, ARC),
             ('"Bob"; "Amy"]', 0, '"Bob"; "Amy"]', 0, 0), ("35; 21]", 0, "35; 21]", 0, 0)],
        ]
        src, dst = self.rows[k], self.rows[k + 1]
        anims, w = birth(dst, [(src, *m) for m in MOVES[k]])
        name, num = BOOK[k]
        nh, vh = self.names[name], self.nums[num]
        self.play(*anims, FadeIn(self.arrows[k + 1], shift=0.15 * DOWN),
                  Transform(nh, nh.copy().move_to(slot(PILE_X[1], k)), path_arc=-0.3 * PI),
                  Transform(vh, vh.copy().move_to(slot(PILE_X[2], k)), path_arc=-0.22 * PI),
                  *extra, run_time=run_time)
        self.remove(*w)
        self.add(dst)

    def trace(self):
        rows = self.rows = [put(C(s, ROW_SIZE), XL if i == 0 else XL + ARROW_W, b)
                            for i, (s, b) in enumerate(zip(TRACE, BASE))]
        arrows = self.arrows = [None] + [implies(r, b) for r, b in zip(rows[1:], BASE[1:])]
        reply = self.trace_reply = put(C(TRACE_REPLY, ROW_SIZE), XL + ARROW_W, REPLY2_BASE)

        self.names, self.nums = {}, {}
        for k, (name, num) in enumerate(BOOK):
            pos = slot(PILE_X[0], 2 - k)                     # Amy on top
            self.names[name] = half_card(name, YELLOW).move_to(pos + LEFT * HALF_W / 2)
            self.nums[num] = half_card(str(num), GOLD).move_to(pos + RIGHT * HALF_W / 2)
        out_p = outline(2 * HALF_W).move_to(slot(PILE_X[0], 0))
        out_x = outline(HALF_W).move_to(slot(PILE_X[1], 0))
        out_y = outline(HALF_W).move_to(slot(PILE_X[2], 0))
        widths = (2 * HALF_W, HALF_W, HALF_W)
        pile_labs = [Mono(s, size=LABEL, color=col).next_to(slot(x, 0) + LEFT * w / 2, LEFT, buff=0.3)
                     for s, col, x, w in zip(("pairs", "xs", "ys"), (FG, TEAL, TEAL), PILE_X, widths)]
        self.pile_labs = pile_labs

        with self.say("c3.rev.2") as c:
            # "Let's run it on the phone book, starting with two empty lists."
            cards = [m for name, num in reversed(BOOK) for m in (self.names[name], self.nums[num])]
            sweep_clear(self,
                        *[time_span(FadeIn(m, shift=0.3 * DOWN), 0.5 + 0.12 * (i // 2),
                                    1.3 + 0.12 * (i // 2)) for i, m in enumerate(cards)],
                        time_span(FadeIn(pile_labs[0]), 0.9, 1.6),
                        time_span(FadeIn(rows[0], shift=0.2 * DOWN), 1.1, 2.0), run_time=2.0)
            c.wait_until("starting with two empty lists")
            self.play(FadeIn(out_x), FadeIn(out_y), FadeIn(pile_labs[1]), FadeIn(pile_labs[2]),
                      FlashAround(part(rows[0], "[], []"), color=TEAL, time_width=1.5), run_time=1.2)

            # "Amy and twenty-one move across."
            c.wait_until("t1")
            self.step(0, min(1.8, max(1.0, c.until("t2") - 0.2)),
                      extra=[time_span(FadeOut(out_x), 1.2, 1.5), time_span(FadeOut(out_y), 1.2, 1.5)])
            # "Then Bob and thirty-five, on top."
            c.wait_until("t2")
            self.step(1, 1.4)
            # "Then Cleo and forty-seven."
            c.wait_until("t3")
            self.step(2, 1.1, extra=[time_span(Create(out_p), 0.6, 1.1)])

            # "Nothing piles up, because each call just hands over to the next."
            c.wait_until("flat")
            flat = SurroundingRectangle(VGroup(*rows[:4], *arrows[1:4]), color=GREEN, buff=0.1)
            iter_lab = T("iterative", size=32, color=DIM).next_to(flat, DOWN, buff=0.2,
                                                                 aligned_edge=RIGHT)
            self.play(Create(flat), time_span(FadeIn(iter_lab, shift=0.2 * DOWN), 0.8, 1.6),
                      run_time=1.6)
            c.wait_until("hands over")
            self.play(*[time_span(FlashAround(a, color=YELLOW), 0.35 * i, 0.35 * i + 0.9)
                        for i, a in enumerate(arrows[1:4])], run_time=1.6)

            # "The pairs are used up, so we return the two lists."
            c.wait_until("done")
            anims, w = birth(rows[4], [(rows[3], BACK_NAMES + ", " + BACK_NUMS, 0,
                                        BACK_NAMES + ", " + BACK_NUMS, 0, 0)])
            self.play(time_span(FlashAround(part(rows[3], "[]"), color=TEAL, time_width=1.5), 0, 1.0),
                      time_span(FlashAround(out_p, color=TEAL, time_width=1.5), 0, 1.0),
                      *[time_span(a, 0.6, 2.0) for a in anims],
                      time_span(FadeIn(arrows[4], shift=0.15 * DOWN), 0.6, 1.4), run_time=2.0)
            self.remove(*w)
            self.add(rows[4])
            c.wait_until("return the two lists")
            anims, w = birth(reply, [(rows[4], BACK, 0, BACK, 0, 0)])
            self.play(*anims, run_time=min(1.4, max(0.8, c.until("backwards") - 0.1)))
            self.remove(*w)
            self.add(reply)

            # "Cleo, Bob, Amy."
            c.wait_until("backwards")
            self.play(*recolor(rows[4].find(BACK_NAMES), RED), *recolor(reply.find(BACK_NAMES), RED),
                      FlashAround(VGroup(*self.names.values()), color=RED, time_width=1.5),
                      run_time=1.2)
            # "Both lists come out backwards."
            c.wait_until("both lists")
            self.play(*recolor(rows[4].find(BACK_NUMS), RED), *recolor(reply.find(BACK_NUMS), RED),
                      FlashAround(VGroup(*self.nums.values()), color=RED, time_width=1.5),
                      run_time=1.2)

    # ── c3.rev.3: the accumulators; the fix and what it costs ────────────────────
    def the_fix(self):
        call = C(FIX, 36).move_to([0, FIX_Y, 0])
        reply = C(FIX_REPLY, 28).next_to(call, DOWN, buff=0.32, aligned_edge=LEFT)
        for g in reply.find(FIXED):
            g.set_color(GREEN)
        chain = PairChain(list(reversed(BOOK))).move_to([0, CELLS_Y, 0])
        parts = [p for i, cell in enumerate(chain.cells) for p in (cell, chain.arrows[i])] + [chain.nil]
        cost_lab = T("+ one cell per pair, + one pass", size=32, color=GOLD).move_to([0, COST_Y, 0])

        left = tline("revUnzip + reversal", 38, monos=(("revUnzip", YELLOW),))
        vs = T("vs", size=32, color=DIM)
        right = tline("unzip", 38, monos=(("unzip", YELLOW),))
        comp = VGroup(left, vs, right).arrange(RIGHT, buff=0.8).move_to([0, COMP_Y, 0])
        for m in (vs, right):
            m.shift(UP * (text_base(left) - (text_base(m) if hasattr(m, "src") else m.get_bottom()[1])))
        more = T("probably more", size=32, color=GOLD).next_to(left, DOWN, buff=0.22)

        lec = T("Lecture 3", size=30, color=DIM).move_to([0, LEC_Y, 0])
        rule = T("an accumulator that forces an extra reversal can lose", size=36, color=YELLOW)
        rule.move_to([0, RULE_Y, 0])

        xs_pile = VGroup(*self.names.values(), self.pile_labs[1])
        ys_pile = VGroup(*self.nums.values(), self.pile_labs[2])

        with self.say("c3.rev.3") as c:
            # "That's the accumulators at work."
            self.play(FlashAround(xs_pile, color=TEAL, time_width=1.5),
                      FlashAround(ys_pile, color=TEAL, time_width=1.5), run_time=1.3)
            # "Like rev-app, they build by consing onto the front."
            c.wait_until("consing onto the front")
            self.play(FlashAround(self.names["Cleo"], color=YELLOW, time_width=1.5),
                      FlashAround(self.nums[47], color=YELLOW, time_width=1.5), run_time=1.2)

            # "To fix it, reverse the input first."
            c.wait_until("fix")
            sweep_clear(self, time_span(FadeIn(call, shift=0.3 * DOWN), 0.5, 1.4),
                        time_span(FadeIn(reply, shift=0.2 * DOWN), 1.3, 2.1), run_time=2.1)

            # "But that reversal copies the whole list of pairs, which costs one extra pass, and one
            # new cell for each pair."
            c.wait_until("copy")
            box = token_box(call.find("List.rev book"), call, color=GOLD)
            self.play(FadeIn(box), *recolor(call.find("List.rev book"), GOLD), run_time=0.9)
            c.wait_until("copies the whole list")
            d = min(0.15 * len(parts) + 0.8, max(1.2, c.until("one extra pass") - 0.1))
            lag = (d - 0.8) / len(parts)
            self.play(*[time_span(FadeIn(p, shift=0.4 * DOWN), lag * i, lag * i + 0.8)
                        for i, p in enumerate(parts)], run_time=d)
            c.wait_until("one extra pass")
            self.play(FadeIn(cost_lab, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("one new cell for each pair")
            self.play(*[time_span(FlashAround(cell.box, color=GOLD, time_width=1.5), 0.3 * i, 0.3 * i + 0.9)
                        for i, cell in enumerate(chain.cells)], run_time=1.5)

            # "So in total, rev-unzip will probably cost more than plain unzip, despite being
            # iterative."
            c.wait_until("total")
            self.play(FadeIn(comp, shift=0.2 * UP), restyle(reply, op=0.4), run_time=1.2)
            c.wait_until("probably cost more")
            self.play(FadeIn(more, shift=0.3 * DOWN), run_time=1.0)

            # "It's the warning from lecture three again. An accumulator that forces an extra
            # reversal can lose."
            c.wait_until("rule")
            d = UP * (COMP_UP - comp.get_y())
            sweep_clear(self, comp.animate.shift(d).build(), more.animate.shift(d).build(),
                        time_span(FadeIn(lec, shift=0.2 * DOWN), 0.5, 1.3),
                        time_span(FadeIn(rule, shift=0.2 * DOWN), 0.6, 1.5),
                        keep=[comp, more], run_time=1.9)
            c.wait_until("an accumulator that forces")
            self.play(FlashUnder(rule, color=YELLOW, time_width=1.5), run_time=1.6)

    # ── c3.rev.4: recap and the end card ─────────────────────────────────────────
    def recap(self):
        title = T("Recap", size=48).move_to([0, TITLE_Y, 0])
        Y, B = YELLOW, BLUE
        specs = [
            (("zip pairs up two lists,", (("zip", Y),)), ("drops the surplus", ())),
            (("_ matches anything;", (("_", FG),)), ("clauses tried in order, so it goes last", ())),
            (("a list of pairs: a directory,", ()), ("searched one pair at a time", ())),
            (("unzip: two results at once,", (("unzip", Y),)), ("with let and a pattern", (("let", B),))),
            (("conspair: no let;", (("conspair", Y), ("let", B))),
             ("revUnzip: iterative, but backwards", (("revUnzip", Y),))),
        ]
        rows = [two_part(tline(a, monos=ma), tline(b, monos=mb),
                         buff=0.26 if mb and b.startswith(mb[0][0]) else 0.16)
                for (a, ma), (b, mb) in specs]
        x_left = -max(r.width for r in rows) / 2
        for r, y in zip(rows, ROW_Y):
            r.move_to([x_left, y, 0], aligned_edge=LEFT)
        cues = ["drops the surplus", "since clauses", "searched one pair", "with a let and a pattern",
                "does it iteratively"]
        up = 0.25 * UP

        with self.say("c3.rev.4") as c:
            # "Let's recap."
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=min(1.0, c.until("r1")))
            for i, row in enumerate(rows):
                c.wait_until(f"r{i + 1}")
                a, b = row
                if i == 0:
                    sweep_clear(self, time_span(FadeIn(a, shift=up), 0.5, 1.5), keep=[title],
                                run_time=1.5)
                else:
                    prev = rows[i - 1]
                    self.play(Transform(prev, faded(prev, SAID)), FadeIn(a, shift=up), run_time=1.2)
                c.wait_until(cues[i])
                self.play(FadeIn(b, shift=up), run_time=1.0)
                settle(self, row)
                if i == 4:
                    c.wait_until("but backwards")
                    self.play(*recolor(select(b, "backwards")[0], RED), run_time=0.8)

            # "Next time, we put lists to work, with a till full of coins, and a program that
            # makes change."
            c.wait_until("next")
            recap = VGroup(*rows)
            settle(self, recap)
            target = recap.copy().scale(END_SCALE)
            target.move_to([0, END_TOP - target.height / 2, 0])
            for row, k in zip(target, [END_OP / SAID] * 4 + [END_OP]):
                multiply_opacity(row, k)
            nxt = VGroup(T("Next:", size=40, color=DIM), T("making change", size=40, color=YELLOW))
            nxt.arrange(RIGHT, buff=0.25).move_to([0, NEXT_Y, 0])
            nxt[0].shift(UP * (text_base_plain(nxt[1], "making change") - text_base_plain(nxt[0], "Next:")))
            self.play(time_span(FadeOut(title, shift=0.3 * UP), 0, 0.8),
                      time_span(Transform(recap, target), 0, 1.2),
                      time_span(FadeIn(nxt, shift=0.3 * DOWN), 1.0, 1.8), run_time=1.8)

            coins = VGroup(*[coin(v, r) for v, r in zip(COINS, (0.52, 0.48, 0.44, 0.4, 0.38, 0.36))])
            coins.arrange(RIGHT, buff=0.22)
            t = till()
            VGroup(coins, t).arrange(RIGHT, buff=0.8).move_to([0, TEASE_Y, 0])
            c.wait_until("a till full of coins")
            src = t.drawer.get_center()
            self.play(FadeIn(t, shift=0.2 * UP),
                      *[time_span(FadeIn(cn, target_position=src, scale=0.3), 0.5 + 0.18 * (5 - i),
                                  1.3 + 0.18 * (5 - i)) for i, cn in enumerate(coins)],
                      run_time=2.3)
            c.wait_until("makes change")
            self.play(FlashUnder(nxt[1], color=YELLOW, time_width=1.5), run_time=1.0)


def text_base_plain(t, src):
    chars = [ch for ch in src if not ch.isspace()]
    for ch, g in zip(chars, t):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return t.get_bottom()[1]

