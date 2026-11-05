"""Chapter 6, scene 1: the hook. Title card, then last chapter's all-ways `change` (In [72]) with
its two copying spots, `allc` and `@`; lecture 3's two accumulator fixes; the question "can
accumulators speed up making change?"; the chapter plan (six exercise cards). Clips c6.hook.1 –
c6.hook.2.

hook.1  {title} title_card("Part 6 · Faster, and exercises"), centred. {code} In [72] fades in
        as the hero; `allc` (the call on line 9) and then `@` get GOLD boxes. {copy} each box
        sprouts a GOLD "copies" tag; mini cons cells duplicate out of it, again and again.
hook.2  {lecture3} the cells go; In [72] shrinks to the top-left; "Lecture 3" (DIM) on the right.
        {length} `nlength` -> `addlen`, tag "accumulator" on the arrow. {reverse} `nrev` ->
        `rev_app`, GOLD O(n²) -> O(n). {ask} the column dims; "accumulators" (YELLOW) is born
        from the tag, the boxed `allc` and `@` fly out of the code, a GOLD "?" between them (left
        up to the end). {plan} In [72] dims, six dim cards 4.1–4.6 slide in along the bottom;
        on "six exercises" they light up to L3's BigCard look (numbers only).

The In [72] shot, for s4 to reuse (dimmed):
  - hero (hook.1): Code(IN72, size=22), centred at x 0 with its top at y 3.1 (about 11.4 x 4.6 units).
    `allc` and `@` of line 9 (0-based) recoloured GOLD, each behind a
    token_box(glyphs, code.line(9), color=GOLD) (stroke 2, fill 0.25, z -1). "copies" tags:
    T("copies", 32, GOLD) at y -1.85 under each token (the `@` one pulled in to x <= 6.6), with a
    GOLD Arrow (stroke 4, tip 0.18) from the tag's top to the box's bottom.
  - small (hook.2): the same code and boxes scaled by 0.65 about the code's top-left corner,
    which moves to (-6.6, 3.45); tags, arrows and cells are gone. At the end it sits at 0.35
    opacity (boxes: stroke 0.35, fill 0.09).
In [72] is ch5's string, column for column (`else` one column left of `if`), so the two chapters
match across the cut; ch6's brief quotes the inner lines one column further right.

The title card comes up 1.6 s before the voice (it is read for 3.9 s, like ch4's).
STATUS: built; check clean apart from dwell notes (title card 3.9 s; In [72] is long code, on screen
the whole scene) and In [72]'s size 22 (ch5's end-card size; the brief wants it small).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

# ── In [72] (notes p. 34), column for column as ch5 has it (scenes/ch5_s7_recap.py) ───────────────────────
IN72 = """let rec change till amt =
  match till, amt with
  | _       , 0   -> [ [] ]
  | []      , _   -> []
  | c::till , amt -> if amt < c then change till amt
                    else let rec allc = function
                           | [] -> []
                           | cs :: css -> (c::cs) :: allc css
                         in
                           allc (change (c::till) (amt - c)) @
                                 change till amt"""
CALL_LINE = 9                       # "allc (change (c::till) (amt - c)) @"

# ── layout ──────────────────────────────────────────────────────────────────────
CODE_SIZE, CODE_TOP = 22, 3.1       # the hero shot of hook.1
TAG_Y = -1.85                       # the "copies" tags
CELL_Y, CELL_K, CELL_PITCH = -2.75, 0.6, 1.05
N_COPIES = 4                        # mini cells per row (the first, then three copies)

SMALL_K, SMALL_UL = 0.65, np.array([-6.6, 3.45, 0])   # In [72] in hook.2
COL_X = 4.0                         # lecture 3's column: the arrows' centre
HEAD_Y, ROW_A, TAG_A, ROW_B, COST_B = 3.15, 2.35, 1.72, 0.95, 0.32
NAME_SIZE = 32
ASK_Y = -1.05                       # the question row
CARD_Y = -2.85                      # the six exercise cards
CARD_FILL = "#161A21"               # L3's card face (projects/focs/l03-lists/scenes/ch5_s6_sumlast.py)
CARD_W, CARD_H = 1.6, 1.05
CARD_DIM_STROKE, CARD_DIM_NUM = 0.45, 0.4
CODE_DIMMED = 0.35


class Tag(VGroup):
    """L3's pill tag (ch5_s6_sumlast.Tag)."""

    def __init__(self, text, color=BLUE, **kw):
        super().__init__(**kw)
        self.label = T(text, size=28, color=color)
        self.box = RoundedRectangle(corner_radius=0.22, width=self.label.width + 0.4, height=0.48)
        self.box.set_stroke(color, 2).set_fill(color, 0.12)
        self.box.move_to(self.label)
        self.add(self.box, self.label)


class SmallCard(VGroup):
    """L3's BigCard (frame DIM 2.5 on CARD_FILL, FG number), small and with its number only."""

    def __init__(self, num, **kw):
        super().__init__(**kw)
        self.frame = RoundedRectangle(corner_radius=0.16, width=CARD_W, height=CARD_H)
        self.frame.set_stroke(DIM, 2.5).set_fill(CARD_FILL, 1)
        self.num = T(num, size=40).move_to(self.frame)
        self.add(self.frame, self.num)


def on_baseline(m, s, y):
    """Put a Mono/T word's baseline at y (measured on its first "e")."""
    e = m[s.replace(" ", "").index("e")]
    return m.shift(UP * (y - e.get_bottom()[1]))


def blank_cell():
    """A mini cons cell with no value: a copy, not data to read."""
    cell = ConsCell(2)
    cell.remove(cell.label)
    return cell.scale(CELL_K)


def dim_box(box, op):
    """A token box's stroke and fill, dimmed together (fill stays 0.25 of the stroke)."""
    return box.animate.set_stroke(opacity=op).set_fill(opacity=0.25 * op)


def dim_tag(tag, op):
    return [tag.box.animate.set_stroke(opacity=op).set_fill(opacity=0.12 * op),
            tag.label.animate.set_opacity(op)]


class Ch6Hook(NarratedScene):
    def construct(self):
        self.build()
        self.recall()
        self.question()
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── everything, built up front ────────────────────────────────────────────────
    def build(self):
        self.card = title_card("Part 6 · Faster, and exercises")

        code = Code(IN72, size=CODE_SIZE)
        code.move_to([0, CODE_TOP - code.height / 2, 0])
        self.code = code
        line = code.line(CALL_LINE)
        self.allc = code.find("allc", line=CALL_LINE)
        self.app = code.find("@", line=CALL_LINE)
        self.boxes = [token_box(g, line, color=GOLD) for g in (self.allc, self.app)]

        self.tags, self.tag_arrows, self.rows = [], [], []
        for glyphs, box in zip((self.allc, self.app), self.boxes):
            x = VGroup(*glyphs).get_x()
            lab = T("copies", size=32, color=GOLD).move_to([x, TAG_Y, 0])
            if lab.get_right()[0] > 6.6:
                lab.shift((6.6 - lab.get_right()[0]) * RIGHT)
            arr = Arrow(lab.get_top() + 0.05 * UP, [x, box.get_bottom()[1] - 0.04, 0], buff=0,
                        stroke_width=4, color=GOLD, max_tip_length_to_length_ratio=0.3, tip_length=0.18)
            x0 = min(x, 6.6 - CELL_K * 0.75)
            row = [blank_cell().move_to([x0 - i * CELL_PITCH, CELL_Y, 0]) for i in range(N_COPIES)]
            self.tags.append(lab)
            self.tag_arrows.append(arr)
            self.rows.append(row)

        # lecture 3's column: old name -> new name, on two rows
        self.head = T("Lecture 3", size=30, color=DIM).move_to([COL_X, HEAD_Y, 0])
        self.fix = []
        for y, old, new in ((ROW_A, "nlength", "addlen"), (ROW_B, "nrev", "rev_app")):
            arr = Arrow(LEFT * 0.35, RIGHT * 0.35, buff=0, stroke_width=3, color=DIM,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.16).move_to([COL_X, y, 0])
            a = Mono(old, size=NAME_SIZE, color=DIM)
            a.move_to([arr.get_left()[0] - 0.25, y, 0], aligned_edge=RIGHT)
            b = Mono(new, size=NAME_SIZE)
            b.move_to([arr.get_right()[0] + 0.25, y, 0], aligned_edge=LEFT)
            for m, s in ((a, old), (b, new)):     # same baseline: every name has an "e"
                on_baseline(m, s, y - 0.09)
            self.fix.append((a, arr, b))
        self.acc_tag = Tag("accumulator", color=YELLOW).move_to([COL_X, TAG_A, 0])
        nrev, _, rev_app = self.fix[1]
        self.on2 = MathTex(r"O(n^2)", font_size=40, color=GOLD).move_to([nrev.get_x(), COST_B, 0])
        self.on = MathTex(r"O(n)", font_size=40, color=GOLD).move_to([rev_app.get_x(), COST_B, 0])

        # the question row: [allc] [@]   ?   accumulators
        full = Mono("allc  @", size=44, color=GOLD)
        self.q_allc = Mono("allc", size=44, color=GOLD).move_to(VGroup(*full[:4]))
        self.q_app = Mono("@", size=44, color=GOLD).move_to(full[4])
        self.q_boxes = [token_box(self.q_allc, full, color=GOLD), token_box(self.q_app, full, color=GOLD)]
        left = VGroup(full, self.q_allc, self.q_app, *self.q_boxes)
        self.q_mark = T("?", size=80, color=GOLD)
        self.q_word = T("accumulators", size=44, color=YELLOW)
        row = VGroup(left, self.q_mark, self.q_word).arrange(RIGHT, buff=0.75)
        row.move_to([0, ASK_Y, 0])
        self.q_mark.set_y(ASK_Y)
        self.q_word.set_y(ASK_Y)

        self.cards = VGroup(*[SmallCard(f"4.{i}") for i in range(1, 7)]).arrange(RIGHT, buff=0.26)
        self.cards.move_to([0, CARD_Y, 0])
        for cd in self.cards:
            cd.frame.set_stroke(opacity=CARD_DIM_STROKE)
            cd.num.set_opacity(CARD_DIM_NUM)

    # ── hook.1: In [72] and its two copying spots ────────────────────────────────
    def recall(self):
        card, code = self.card, self.code
        # The card comes up just before the voice, so it can be read (the code is due at 3.4 s).
        self.play(
            time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.7),
            time_span(GrowFromCenter(card.rule), 0, 0.7),
            time_span(FadeIn(card.course, shift=0.25 * DOWN), 0.15, 0.85),
            time_span(FadeIn(card.part, shift=0.25 * DOWN), 0.3, 1.0),
            run_time=1.0,
        )
        self.wait(0.6)
        with self.say("c6.hook.1") as c:
            # "Last time, we found every way to make change."
            # "We used all-see to put a coin on the front of every solution, ..."
            c.wait_until("code")
            self.play(time_span(FadeOut(card, shift=0.3 * UP), 0, 0.7),
                      time_span(FadeIn(code, shift=0.2 * UP), 0.3, 1.5), run_time=1.5)
            c.wait_until("all-see")
            self.play(FadeIn(self.boxes[0], scale=1.15), *recolor(self.allc, GOLD),
                      FlashAround(VGroup(*self.allc), color=GOLD, time_width=1.5), run_time=1.2)
            # "... and append, the at sign, to join the two lists of answers."
            c.wait_until("append")
            self.play(FadeIn(self.boxes[1], scale=1.15), *recolor(self.app, GOLD),
                      FlashAround(VGroup(*self.app), color=GOLD, time_width=1.5), run_time=1.2)

            # "Both of those copy cells, over and over again."  Each box sprouts a tag, and cells
            # duplicate out of it: the first slowly, the next faster, the rest quick.
            c.wait_until("copy")
            self.play(*[GrowArrow(a) for a in self.tag_arrows],
                      *[FadeIn(t, shift=0.3 * DOWN) for t in self.tags], run_time=0.9)
            self.play(*[ReplacementTransform(b.copy(), r[0]) for b, r in zip(self.boxes, self.rows)],
                      run_time=min(1.0, max(0.6, 0.9 * c.until("over and over"))))
            c.wait_until("over and over")
            for i, rt in zip(range(1, N_COPIES), (0.6, 0.45, 0.35)):
                self.play(*[ReplacementTransform(r[i - 1].copy(), r[i]) for r in self.rows], run_time=rt)

    # ── hook.2: lecture 3's fixes, the question, the plan ────────────────────────
    def question(self):
        code, boxes = self.code, self.boxes
        (nlength, arr_a, addlen), (nrev, arr_b, rev_app) = self.fix
        anchor = code.get_corner(UL)

        def to_small(m):
            return m.animate.scale(SMALL_K, about_point=anchor).shift(SMALL_UL - anchor)

        with self.say("c6.hook.2") as c:
            # "We've met this kind of waste before."  (the copies hold through "waste")
            c.wait_until("waste")
            cells = [m for r in self.rows for m in r]
            self.play(*[time_span(FadeOut(m), 0, 0.6) for m in (*cells, *self.tags, *self.tag_arrows)],
                      to_small(code), *[to_small(b) for b in boxes],
                      time_span(FadeIn(self.head, shift=0.25 * DOWN), 0.9, 1.6), run_time=1.6)
            # (the lines below are born by ReplacementTransform from a copy: TransformFromCopy into
            # a target with fewer glyphs leaves a duplicated glyph on it)

            # "In lecture three, an accumulator made length iterative."
            c.wait_until("length")
            self.play(FadeIn(nlength, shift=0.25 * DOWN), run_time=0.8)
            c.wait_until("an accumulator")
            self.play(GrowArrow(arr_a), ReplacementTransform(nlength.copy(), addlen),
                      time_span(FadeIn(self.acc_tag, shift=0.2 * DOWN), 0.5, 1.4), run_time=1.4)

            # "And building the answer with cons, instead of appending, made reverse fast."
            c.wait_until("reverse")
            self.play(FadeIn(nrev, shift=0.25 * DOWN), FadeIn(self.on2, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("made reverse fast")
            self.play(GrowArrow(arr_b), ReplacementTransform(nrev.copy(), rev_app),
                      ReplacementTransform(self.on2.copy(), self.on), run_time=1.4)

            # "So can accumulators speed up making change too?"  The column steps back; its tag
            # becomes the question's word; the two boxes come out of In [72]; "?" between them.
            c.wait_until("ask")
            col = [self.head, nlength, arr_a, addlen, nrev, arr_b, rev_app, self.on2, self.on]
            self.play(ReplacementTransform(self.acc_tag.label.copy(), self.q_word),
                      *[m.animate.set_opacity(0.4) for m in col], *dim_tag(self.acc_tag, 0.4),
                      run_time=1.4)
            c.wait_until("making change")
            self.play(ReplacementTransform(VGroup(*self.allc).copy(), self.q_allc),
                      ReplacementTransform(VGroup(*self.app).copy(), self.q_app),
                      *[ReplacementTransform(b.copy(), qb) for b, qb in zip(boxes, self.q_boxes)],
                      time_span(FadeIn(self.q_mark, scale=0.6), 0.8, 1.5), run_time=1.5)

            # "That's the first half of this chapter."  In [72] steps back; the plan's second
            # half, six exercise cards, slides in along the bottom (dim for now).
            c.wait_until("plan")
            self.play(code.animate.set_opacity(CODE_DIMMED), *[dim_box(b, CODE_DIMMED) for b in boxes],
                      LaggedStart(*[FadeIn(cd, shift=0.6 * LEFT) for cd in self.cards], lag_ratio=0.15),
                      run_time=1.8)
            # "In the second half, I'll hand you six exercises to try on your own."
            c.wait_until("six exercises")
            self.play(*[cd.frame.animate.set_stroke(opacity=1) for cd in self.cards],
                      *[cd.num.animate.set_opacity(1) for cd in self.cards], run_time=1.0)
