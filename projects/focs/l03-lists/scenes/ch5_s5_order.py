"""Chapter 5, scene 5: comparing strings. The four operators, the character-by-character rule
(a box sliding to the first difference), lexicographic order, the code table, and the
"Zebra" < "apple" surprise.

Every comparison and code on screen was checked in the OCaml 5.4 toplevel:
  "apple" < "banana", "app" < "apple", "Zebra" < "apple"  ->  - : bool = true
  Char.code 'A' 'B' 'C' 'Z' = 65 66 67 90;  'a' 'b' 'c' 'z' = 97 98 99 122
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── layout ─────────────────────────────────────────────────────────────────────
B = 1.05                   # side of a character cell in the comparison rows
LETTER = 54                # font size of the letters in those cells
X0 = -2.6                  # x of column 0 (rows are left-aligned so columns line up)
ROW_Y = (0.15, -1.1)       # the two strings being compared, stacked
EXPR_Y, REPLY_Y = 2.35, 1.4
LIFT = 2.8                 # cmp.1 sits this much lower, and rises when the rows arrive
OPS_Y = EXPR_Y - LIFT + 1.35   # the operator row (cmp.1 only, before the lift)
CAP_Y = -2.4               # "lexicographic order", under the rows
# the code table: big and centred for cmp.3 (header above it), then each part turns into the
# small version at the bottom (header left of the codes) for cmp.4
BIG = dict(tb=1.0, d=0.9, g=1.5, box_y=0.0, code_y=-1.05, lsize=52, csize=42, hsize=44, above=True)
SMALL = dict(tb=0.8, d=0.8, g=1.6, box_y=0.35, code_y=-0.65, lsize=44, csize=36, hsize=34, above=False)
T_SHRINK = 0.85            # the small table is shrunk by this about its centre ...
T_BOX_LOW = -2.4           # ... and dropped so its cell row ends up here
DIMMED = 0.3

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_MASTERS = {}


# ── helpers (local to this scene) ──────────────────────────────────────────────
def letter(ch, size, x, y):
    """One Menlo glyph centred on column x, on the baseline every other letter of this size
    shares (all come from one master Text, so 'p' hangs and 'Z' stands as in running text)."""
    if size not in _MASTERS:
        _MASTERS[size] = Mono(ALPHA, size=size)
    m = _MASTERS[size]
    g = m[ALPHA.index(ch)].copy()
    return g.move_to([x, y + g.get_y() - m.get_y(), 0])


def col(i, y=0.0):
    return np.array([X0 + i * B, y, 0])


class Row:
    """A string as a strip of touching character cells (no arrows: it is not a list).
    boxes and letters are separate VGroups, each added to the scene on its own."""

    def __init__(self, word, y):
        self.boxes = VGroup(*[Square(B, stroke_color=BLUE, stroke_width=3).move_to(col(i, y))
                              for i in range(len(word))])
        self.letters = VGroup(*[letter(ch, LETTER, X0 + i * B, y) for i, ch in enumerate(word)])


def col_box(i):
    """The sliding highlight (P8): one box over column i of both rows, behind the letters."""
    h = ROW_Y[0] - ROW_Y[1] + B + 0.16
    r = Rectangle(width=B + 0.16, height=h).set_stroke(YELLOW, 4).set_fill(YELLOW, 0.16)
    return r.move_to(col(i, (ROW_Y[0] + ROW_Y[1]) / 2)).set_z_index(-1)


def expr_code(src, y):
    c = Code(src, size=56).move_to([0, y, 0])
    c.find("<").set_color(YELLOW)
    return c


class CodeTable:
    """A B C … Z   a b c … z in cells, Char.code's numbers underneath in GOLD.
    Every cell, code, dot group and the header is its own top-level mobject (`parts`)."""

    def __init__(self, tb, d, g, box_y, code_y, lsize, csize, hsize, above):
        # tb: cell side; d: room for the dots; g: the gap between the blocks
        self.box_y, self.code_y = box_y, code_y
        self.header = Mono("Char.code", size=hsize, color=YELLOW)
        block_w = 4 * tb + d                              # A B C … Z
        lead = 0 if above else self.header.width + 0.4    # header beside the codes, or above
        a0 = -(lead + 2 * block_w + g) / 2 + lead + tb / 2   # centre of the 'A' cell
        geo = (tb, d, tb / 0.8, box_y, code_y, lsize, csize)
        self.caps, self.cap_codes, self.cap_dots = self.block(
            a0, geo, [("A", 65), ("B", 66), ("C", 67), None, ("Z", 90)])
        self.lows, self.low_codes, self.low_dots = self.block(
            a0 + block_w + g, geo, [("a", 97), ("b", 98), ("c", 99), None, ("z", 122)])
        if above:
            self.header.move_to([0, box_y + tb / 2 + 0.5 + self.header.height / 2, 0])
        else:
            self.header.next_to(self.cap_codes[0], LEFT, buff=0.4)
        self.parts = [self.header, *self.caps, *self.cap_codes, *self.cap_dots,
                      *self.lows, *self.low_codes, *self.low_dots]

    @staticmethod
    def block(x0, geo, entries):
        tb, d, s, box_y, code_y, lsize, csize = geo
        xs = [x0, x0 + tb, x0 + 2 * tb, None, x0 + 3 * tb + d]
        cells, codes, dots = [], [], []
        for x, e in zip(xs, entries):
            if e is None:
                cx = x0 + 2.5 * tb + d / 2
                for y in (box_y, code_y):
                    dots.append(VGroup(*[Dot(radius=0.05 * s, color=DIM) for _ in range(3)])
                                .arrange(RIGHT, buff=0.12 * s).move_to([cx - 0.05 * s * (y == code_y), y, 0]))
                continue
            ch, n = e
            cells.append(VGroup(Square(tb, stroke_color=BLUE, stroke_width=3).move_to([x, box_y, 0]),
                                letter(ch, lsize, x, box_y)))
            codes.append(Mono(str(n), size=csize, color=GOLD).move_to([x, code_y, 0]))
        return cells, codes, dots

    def shrunk(self):
        """Shrink every part about the table's centre and drop it to the bottom of the frame
        (used on the SMALL table to get the cmp.4 targets)."""
        p = np.array([0, (self.box_y + self.code_y) / 2, 0])
        dy = T_BOX_LOW - (p[1] + T_SHRINK * (self.box_y - p[1]))
        for m in self.parts:
            m.scale(T_SHRINK, about_point=p).shift(UP * dy)
        return self

    def shrink_anims(self):
        """For a 1.5 s play: every cell, code and dot group turns into its counterpart in the
        small table at the bottom (letters keep their current opacity); the header fades out
        above and back in beside the codes once they have landed (so it never crosses the cells)."""
        small = CodeTable(**SMALL).shrunk()
        for b, t in zip(self.caps + self.lows, small.caps + small.lows):
            t[1].set_opacity(b[1].get_fill_opacity())
        anims = [Transform(b, t) for b, t in zip(self.parts[1:], small.parts[1:])]
        anims += [time_span(FadeOut(self.header, shift=0.3 * UP), 0, 0.6),
                  time_span(FadeIn(small.header, shift=0.3 * RIGHT), 0.9, 1.5)]
        self.header = small.header
        self.parts[0] = small.header
        return anims


def restyle(mob, op=None, shift=None):
    """One Transform that dims/restores (P9) and moves `mob` together. Opacity goes on the
    fill of filled parts (glyphs) and on the stroke of outlines (cells, dashes)."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            if op is not None:
                leaf.set_opacity(op)
        elif op is not None:
            leaf.set_stroke(opacity=op)
    if shift is not None:
        t.shift(shift)
    return Transform(mob, t)


def set_alpha(mobs, op):
    return [restyle(m, op) for m in mobs]


def rewrite(old, new, keep):
    """Rewrite one Code line into another in place: the glyphs of each (old, new) substring
    pair slide to their new spots, the rest of the old line fades out and the rest of the new
    one fades in. Animations are per glyph (LESSONS.md: never wrap glyphs in a Group).
    Afterwards call scene.swap(old, new)."""
    anims, used_o, used_n = [], set(), set()
    for so, sn in keep:
        for a, b in zip(old.find(so), new.find(sn)):
            anims.append(Transform(a, b.copy()))
            used_o.add(id(a))
            used_n.add(id(b))
    anims += [FadeOut(g, shift=0.2 * UP) for g in old.text if id(g) not in used_o]
    anims += [FadeIn(g, shift=0.2 * UP) for g in new.text if id(g) not in used_n]
    return anims


class ComparingStrings(NarratedScene):
    def construct(self):
        self.operators()
        self.the_rule()
        self.the_codes()
        self.zebra()
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.1)  # a truly empty last frame

    def swap(self, old, new):
        """After rewrite(): replace the moved and faded glyphs by the real new Code."""
        self.remove(*old.get_family(), *new.get_family())
        self.add(new)

    # cmp.1: the four operators, and is "apple" < "banana"?
    def operators(self):
        expr = expr_code('"apple" < "banana"', EXPR_Y - LIFT)
        lt = expr.find("<")[0]
        lt.set_opacity(0)                       # the operator slot starts empty
        slot = DashedVMobject(Square(0.62), num_dashes=12).set_stroke(DIM, 3).move_to(lt)

        ops = [Mono(s, size=56) for s in ("<", "<=", ">", ">=")]
        VGroup(*ops).arrange(RIGHT, buff=1.3).move_to([0, OPS_Y, 0])
        for o in ops:
            o.set_opacity(0.25)
        reply = Code("- : bool = true", size=42).move_to([0, REPLY_Y - LIFT, 0])

        top = Row("apple", ROW_Y[0])
        bot = Row("banana", ROW_Y[1])

        with self.say("c5.cmp.1") as c:
            # {ops}: two strings and an empty slot between them
            self.play(FadeIn(expr, shift=0.3 * DOWN), Create(slot), run_time=1.0)

            # {four}: the whole row of operators first (P2), each lit as it is named
            c.wait_until("four")
            self.play(LaggedStart(*[FadeIn(o, shift=0.3 * DOWN) for o in ops], lag_ratio=0.15),
                      run_time=1.2)
            for o, cue, nth in ((ops[0], "less than", 0), (ops[1], "or equal", 0),
                                (ops[2], "greater", 0), (ops[3], "or equal", 1)):
                c.wait_until(cue, nth=nth)
                self.play(o.animate.set_opacity(1), FlashUnder(o, color=FG, time_width=1.5),
                          run_time=0.7)

            # {apple}: "less than" drops out of the row into the slot (P5)
            c.wait_until("apple")
            fly = lt.copy().set_opacity(1)
            self.play(ops[0].animate.set_color(YELLOW),
                      TransformFromCopy(ops[0], fly), FadeOut(slot),
                      *[o.animate.set_opacity(0.35) for o in ops[1:]],
                      run_time=c.until("banana", floor=1.2))
            self.remove(fly)
            lt.set_opacity(1)

            # {yes}: OCaml's answer
            c.wait_until("yes")
            self.play(FadeIn(reply, shift=0.3 * DOWN), run_time=1.0)

            # "Apple comes first in the dictionary": the code rises, the words stack up
            # in dictionary order, apple on top
            c.wait_until("apple comes")
            self.play(*[time_span(FadeOut(o, shift=0.3 * UP), 0.1 * k, 0.5 + 0.1 * k)
                        for k, o in enumerate(ops)],
                      time_span(expr.animate.shift(UP * LIFT), 0.2, 1.3),
                      time_span(reply.animate.shift(UP * LIFT), 0.2, 1.3), run_time=1.3)
            c.wait_until("dictionary")
            self.play(TransformFromCopy(VGroup(*expr.find("apple")), top.letters),
                      time_span(TransformFromCopy(VGroup(*expr.find("banana")), bot.letters), 0.2, 1.5),
                      run_time=1.5)

        self.expr, self.reply, self.top, self.bot = expr, reply, top, bot

    # cmp.2: character by character, to the first difference; lexicographic order
    def the_rule(self):
        expr, reply, top, bot = self.expr, self.reply, self.top, self.bot
        app = Row("app", ROW_Y[0])
        gap = DashedVMobject(Square(B), num_dashes=16).set_stroke(DIM, 3).move_to(col(3, ROW_Y[0]))
        expr2 = expr_code('"app" < "apple"', EXPR_Y)
        caption = T("lexicographic order", size=44).move_to([X0 + 2 * B, CAP_Y, 0])

        with self.say("c5.cmp.2") as c:
            # {rule}: each letter gets its own cell
            c.wait_until("character")
            self.play(Create(top.boxes, lag_ratio=0.15), Create(bot.boxes, lag_ratio=0.15), run_time=1.5)

            # {first}: the box lands on the first pair
            c.wait_until("the first")
            hb = col_box(0)
            self.play(FadeIn(hb), run_time=0.8)
            c.wait_until("different")
            self.play(FlashAround(hb, color=YELLOW, time_width=1.5), run_time=1.0)
            # "that settles it": nothing after the first difference matters (P9)
            c.wait_until("settles it")
            rest = [*top.letters[1:], *top.boxes[1:], *bot.letters[1:], *bot.boxes[1:]]
            self.play(*set_alpha(rest, 0.22), run_time=1.0)

            # {same}: a pair that starts the same. apple steps down, app arrives on top
            c.wait_until("same")
            down = DOWN * (ROW_Y[0] - ROW_Y[1])
            self.play(FadeOut(bot.letters), FadeOut(bot.boxes),
                      time_span(restyle(top.letters, 1, shift=down), 0.1, 1.2),
                      time_span(restyle(top.boxes, 1, shift=down), 0.1, 1.2),
                      time_span(FadeIn(app.boxes, shift=0.3 * DOWN), 0.6, 1.5),
                      time_span(FadeIn(app.letters, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)
            apple = top
            # the box walks on while the pairs match; the old line steps back
            c.wait_until("move on")
            self.play(hb.animate.move_to(col(1, hb.get_y())), *set_alpha([expr, reply], DIMMED),
                      run_time=0.7)
            c.wait_until("and so on")
            self.play(hb.animate.move_to(col(2, hb.get_y())), run_time=0.7)

            # {prefix}: app runs out first
            c.wait_until("runs out")
            self.play(hb.animate.move_to(col(3, hb.get_y())), Create(gap), run_time=1.0)
            c.wait_until("that string")
            self.play(app.letters.animate.set_color(YELLOW),
                      FlashAround(VGroup(app.boxes, gap), color=YELLOW, time_width=1.5), run_time=1.0)

            # "So app comes before apple": the code line becomes that comparison
            c.wait_until("so app")
            self.play(*rewrite(expr, expr2, [('"apple"', '"apple"'), ("<", "<")]),
                      restyle(reply, 1), run_time=1.2)
            self.swap(expr, expr2)

            # {name}
            c.wait_until("name")
            self.play(FadeIn(caption, shift=0.3 * DOWN), run_time=1.0)

        self.expr, self.app, self.gap_box, self.apple, self.hb, self.caption = expr2, app, gap, apple, hb, caption

    # cmp.3: every character has a number; the code table
    def the_codes(self):
        tab = CodeTable(**BIG)
        self.tab = tab
        old = [self.expr, self.reply, self.hb, self.app.boxes, self.app.letters, self.gap_box,
               self.apple.boxes, self.apple.letters]

        with self.say("c5.cmp.3") as c:
            # {codes}: the rule's name moves to the corner and stays there
            self.play(self.caption.animate.scale(0.7).set_color(DIM).to_corner(UL, buff=0.5), run_time=1.0)

            # "Every character": clear the board (P18) for the characters, in cells (P2)
            c.wait_until("every character")
            cells = [*tab.caps[:3], tab.cap_dots[0], tab.caps[3], *tab.lows[:3], tab.low_dots[0], tab.lows[3]]
            self.play(LaggedStart(*[FadeOut(m) for m in old], lag_ratio=0.08),
                      time_span(LaggedStart(*[FadeIn(m, shift=0.3 * DOWN) for m in cells], lag_ratio=0.1),
                                0.5, 1.9), run_time=1.9)
            c.wait_until("ascii")
            self.play(FadeIn(tab.header, shift=0.3 * DOWN), run_time=0.8)

            # {upper}: capitals, then their codes, 65 to 90
            c.wait_until("capital")
            self.play(FlashAround(VGroup(*tab.caps, tab.cap_dots[0]), color=YELLOW, time_width=1.5),
                      run_time=0.9)
            c.wait_until("codes")
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN)
                                    for m in [*tab.cap_codes[:3], tab.cap_dots[1], tab.cap_codes[3]]],
                                  lag_ratio=0.3), run_time=1.4)

            # {lower}: lowercase starts at 97 (the jump from 90 is the gap)
            c.wait_until("lowercase")
            self.play(FlashAround(VGroup(*tab.lows, tab.low_dots[0]), color=YELLOW, time_width=1.5),
                      run_time=0.8)
            c.wait_until("start at")
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN)
                                    for m in [*tab.low_codes[:3], tab.low_dots[1], tab.low_codes[3]]],
                                  lag_ratio=0.3), run_time=1.4)

            # {bycode}: it's the numbers that get compared
            c.wait_until("by those codes")
            self.play(*set_alpha([cell[1] for cell in tab.caps + tab.lows], 0.4),
                      FlashUnder(VGroup(*tab.cap_codes), color=GOLD, time_width=1.5),
                      FlashUnder(VGroup(*tab.low_codes), color=GOLD, time_width=1.5), run_time=1.3)

    # cmp.4: "Zebra" < "apple"? Ask, hold, answer; then why
    def zebra(self):
        tab = self.tab
        expr = expr_code('"Zebra" < "apple"', EXPR_Y)
        reply = Code("- : bool = true", size=42).move_to([0, REPLY_Y, 0])
        trues = list(reply.find("true"))
        q = T("?", size=60, color=GOLD)
        q.move_to(VGroup(*trues)).align_to(trues[0], LEFT).shift(UP * 0.04)
        for g in trues:
            g.set_opacity(0)                    # the answer starts as a question mark
        zeb, apple = Row("Zebra", ROW_Y[0]), Row("apple", ROW_Y[1])

        lab90 = Mono("90", size=42, color=GOLD).move_to(col(0, ROW_Y[0]) + LEFT * (B / 2 + 0.6))
        lab97 = Mono("97", size=42, color=GOLD).move_to(col(0, ROW_Y[1]) + LEFT * (B / 2 + 0.6))
        z_cell, a_cell = tab.caps[-1], tab.lows[0]

        with self.say("c5.cmp.4", gap=0.6) as c:   # a little extra hold on the final picture
            # {zebra}: the table makes room; the new question, with its answer left open (P23)
            self.play(*tab.shrink_anims(),
                      time_span(FadeIn(expr, shift=0.3 * DOWN), 0.4, 1.5),
                      time_span(FadeIn(reply, shift=0.3 * DOWN), 0.6, 1.5),
                      time_span(FadeIn(q, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)

            # "Zebra ... or apple": both strings drop into the rows
            c.wait_until("zebra with")
            self.play(FadeIn(zeb.boxes), FadeIn(apple.boxes),
                      TransformFromCopy(VGroup(*expr.find("Zebra")), zeb.letters),
                      TransformFromCopy(VGroup(*expr.find("apple")), apple.letters), run_time=1.0)
            c.wait_until("capital")
            self.play(FlashAround(zeb.boxes[0], color=YELLOW, time_width=1.5), run_time=0.8)
            c.wait_until("lowercase")
            self.play(FlashAround(apple.boxes, color=YELLOW, time_width=1.5), run_time=0.8)

            # {answer}: the "?" becomes OCaml's answer
            c.wait_until("answer")
            ans = VGroup(*[g.copy().set_opacity(1) for g in trues])
            self.play(ReplacementTransform(q, ans), run_time=1.2)
            self.remove(ans)
            for g in trues:
                g.set_opacity(1)
            c.wait_until("zebra is smaller")
            self.play(zeb.letters.animate.set_color(YELLOW),
                      FlashAround(zeb.boxes, color=YELLOW, time_width=1.5), run_time=1.0)

            # {why}: the box is back on the first pair, Z against a, and their codes come up
            # out of the table
            c.wait_until("why")
            hb = col_box(0)
            self.play(FadeIn(hb), run_time=0.8)
            c.wait_until("is ninety")
            self.play(z_cell[0].animate.set_stroke(YELLOW, width=4), restyle(z_cell[1], 1),
                      TransformFromCopy(tab.cap_codes[-1], lab90), run_time=1.2)
            c.wait_until("is ninety-seven")
            self.play(a_cell[0].animate.set_stroke(YELLOW, width=4), restyle(a_cell[1], 1),
                      TransformFromCopy(tab.low_codes[0], lab97), run_time=1.2)

            # {every}: the whole capital block sits below the whole lowercase block
            c.wait_until("every capital")
            self.play(*set_alpha([cell[1] for cell in tab.caps + tab.lows], 1),
                      FlashAround(VGroup(*tab.caps, *tab.cap_codes), color=YELLOW, time_width=1.5),
                      run_time=1.0)
            c.wait_until("every lowercase")
            gap_x = (tab.caps[-1].get_right()[0] + tab.lows[0].get_left()[0]) / 2
            less = Mono("<", size=72, color=YELLOW).move_to(
                [gap_x, (tab.caps[0].get_y() + tab.cap_codes[0].get_y()) / 2, 0])
            self.play(FlashAround(VGroup(*tab.lows, *tab.low_codes), color=YELLOW, time_width=1.5),
                      GrowFromCenter(less), run_time=1.2)

            # {careful}: watch out for capitals
            c.wait_until("this way")
            self.play(zeb.letters[0].animate.set_color(RED), expr.find("Z")[0].animate.set_color(RED),
                      FlashAround(zeb.boxes[0], color=RED, time_width=1.5),
                      run_time=c.until("watch out", floor=0.8))
