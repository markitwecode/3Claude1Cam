"""Chapter 4, scene 3: the change program, clause by clause. Clips c4.code.1 – c4.code.5.

Opens on s2's end shot (the three observation cards stacked at the right), which steps aside for
the code. Layout: the code (Code 28, line_spacing 1.15) spans the width at the top, left edge
x = -6.5, top y = 3.25. One YELLOW highlight box slides clause to clause. Free space: right of lines 1-3
(card 1, the raise tags) and the band under the code (tags, insets, the forget demo, the reply).
Ends on the code and the reply `val change : ...` (Code 28, left x = -6.5, under the code).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = (
    "let rec change till amt =\n"
    "  match till, amt with\n"
    "  | _, 0         -> []\n"
    '  | [], _        -> raise (Failure "no more coins!")\n'
    "  | c::till, amt -> if amt < c then change till amt\n"
    "                    else c :: change (c::till) (amt - c)"
)
REPLY = "val change : int list -> int -> int list = <fun>"
CODE_SIZE = 28
CODE_LEFT = -6.5
CODE_TOP = 3.25
CODE_SPACING = 1.15
TAG = 32
CARD_TEXT = 32                # s2's card styling (obs_cards below)
CARD_PAD = 0.26
CARD_SCALE = 0.875            # beside the clauses: text 28
S2_RIGHT, S2_TOP = 6.56, 0.975   # s2's end shot: the stack alone, scale 1


def obs_cards():
    """Three observation cards: BLUE bold number, FG text (T 32), DIM rounded frame, equal widths.
    Copied from scenes/ch4_s2_idea.py (keep the two in step)."""
    specs = [("1.", ["change for 0 = no coins"]),
             ("2.", ["largest coin fits?", "use it, reduce the amount"]),
             ("3.", ["too large? remove it"])]
    parts = []
    for num, lines in specs:
        txt = VGroup(*[T(s, size=CARD_TEXT) for s in lines]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        n = T(num, size=CARD_TEXT, color=BLUE, weight=BOLD)
        n.next_to(txt[0], LEFT, buff=0.28).align_to(txt[0][0], DOWN)
        content = VGroup(n, *txt)
        nil = None
        if num == "1.":
            nil = Mono("[]", size=36, color=TEAL).next_to(txt[0], RIGHT, buff=0.5)
            nil.set_y(txt[0][0].get_y())
            content.add(nil)
        parts.append((n, list(txt), nil, content))
    width = max(p[3].width for p in parts) + 2 * CARD_PAD
    cards = VGroup()
    for n, lines, nil, content in parts:
        frame = RoundedRectangle(corner_radius=0.16, width=width, height=content.height + 2 * CARD_PAD)
        frame.set_stroke(DIM, 2).set_fill(BG, 0)
        content.move_to(frame).align_to(frame, LEFT).shift(RIGHT * CARD_PAD)
        card = VGroup(frame, n, *lines, *([nil] if nil is not None else []))
        card.frame, card.num, card.lines, card.nil = frame, n, lines, nil
        cards.add(card)
    cards.arrange(DOWN, buff=0.24)
    return cards


def tag(text, color=FG, size=TAG):
    return T(text, size=size, color=color)


def pointer(start, end, color):
    return Arrow(start, end, buff=0.06, stroke_width=4, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35, color=color)


def place(m, left=None, cx=None, top=None, bottom=None, right=None):
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if cx is not None:
        m.shift(RIGHT * (cx - m.get_center()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    return m


def inset_frame(content, pad=0.15, extra_right=0.2):
    """DIM rounded frame round an inset; extra room on the right (a Code line's last glyph
    sits flush with its bounding box)."""
    fr = RoundedRectangle(corner_radius=0.1, width=content.width + 2 * pad + extra_right,
                          height=content.height + 2 * pad).set_stroke(DIM, 2).set_fill(BG, 0)
    place(fr, left=content.get_left()[0] - pad, top=content.get_top()[1] + pad)
    return fr


def toplevel(src, color):
    """A toplevel reply line, one colour."""
    m = Code(src, size=CODE_SIZE)
    m.set_color(color)
    return m


class ChangeCode(NarratedScene):
    def construct(self):
        code = Code(SRC, size=CODE_SIZE, line_spacing=CODE_SPACING)
        code.shift(RIGHT * (CODE_LEFT - code.get_left()[0]) + UP * (CODE_TOP - code.get_top()[1]))
        self.code = code
        self.L = [code.line(i) for i in range(6)]
        self.B = code.get_bottom()[1]                      # top of the band under the code
        self.x1 = max(self.L[1].get_right()[0], self.L[2].get_right()[0])   # free space right of lines 1-3
        self.raise_g = code.find("raise", line=3)
        # The cards as they return, one by one, beside their clauses.
        self.k1, self.k2, self.k3 = [k.scale(CARD_SCALE) for k in obs_cards()]

        # Hand-off from s2: its end shot, the three cards alone at the right.
        self.stack = obs_cards()
        self.stack.to_edge(RIGHT, buff=0.55)
        place(self.stack, top=S2_TOP)
        self.play(FadeIn(self.stack), run_time=0.7)
        self.wait(0.3)

        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

        # End on the code and the reply alone.
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.annot], run_time=0.8)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ helpers
    def r1_tag(self, text, color):
        """A tag in the space right of line 3, with an arrow down to clause 2's `raise`."""
        t = tag(text, color)
        place(t, left=self.x1 + 1.0, bottom=self.L[3].get_top()[1] + 0.26)
        a = pointer(t.get_left() + 0.06 * LEFT + 0.04 * DOWN,
                    self.raise_g.get_top() + 0.2 * RIGHT + 0.05 * UP, color)
        return t, a

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        code, L, B = self.code, self.L, self.B
        with self.say("c4.code.1") as c:
            self.play(FadeOut(self.stack, shift=0.6 * RIGHT), time_span(FadeIn(code, shift=0.2 * UP), 0.3, 1.5),
                      run_time=1.5)
            c.wait_until("match")
            self.play(FlashUnder(code.find("match till, amt with", line=1), color=YELLOW), run_time=1.6)

            c.wait_until("pair")
            pair = tag("a pair, as in append and zip")
            pair.next_to(L[1], RIGHT, buff=0.6)
            self.play(FlashAround(code.find("till, amt", line=1), color=YELLOW),
                      FadeIn(pair, shift=0.3 * LEFT), run_time=1.3)

            c.wait_until("zero")
            self.box = token_box(code.find("_, 0         -> []", line=2), L[2])
            self.play(FadeIn(self.box),
                      pair.animate.next_to(L[0], RIGHT, buff=0.6).set_opacity(0.45), run_time=1.2)

            card1 = self.k1
            place(card1, left=self.x1 + 0.55, bottom=L[3].get_top()[1] + 0.24)
            c.wait_until("our first observation")
            self.play(FadeIn(card1, shift=0.4 * LEFT), run_time=1.0)

            c.wait_until("its pattern")
            self.play(FlashUnder(code.find("_, 0", line=2), color=YELLOW), run_time=1.4)

            c.wait_until("const")
            zero = code.find("0", line=2)
            const = place(tag("a constant: matches only 0", GOLD), left=-6.3, top=B - 0.45)
            self.play(FlashAround(zero, color=GOLD), *recolor(zero, GOLD),
                      FadeIn(const, shift=0.3 * UP), run_time=1.4)

            c.wait_until("any")
            any_t = tag("wildcard: any till")
            any_t.next_to(const, DOWN, buff=0.32, aligned_edge=LEFT)
            self.play(FlashAround(code.find("_", line=2), color=YELLOW),
                      FadeIn(any_t, shift=0.3 * UP), run_time=1.3)

            c.wait_until("change for zero is nil")
            nil_code = code.find("[]", line=2)
            self.play(FlashAround(nil_code, color=TEAL), FlashAround(card1.nil, color=TEAL),
                      *recolor(nil_code, TEAL), run_time=1.5)
        self.c1 = (pair, card1, const, any_t)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        code, L, B = self.code, self.L, self.B
        pair, card1, const, any_t = self.c1
        with self.say("c4.code.2") as c:
            clause2 = code.find('[], _        -> raise (Failure "no more coins!")', line=3)
            self.play(Transform(self.box, token_box(clause2, L[3])), FadeOut(pair), run_time=1.5)
            c.wait_until("the till is empty")
            self.play(FlashUnder(code.find("[]", line=3), color=TEAL), run_time=1.3)

            c.wait_until("raise")
            rexpr = code.find('raise (Failure "no more coins!")', line=3)
            self.play(*recolor(rexpr, RED), *[FadeOut(m) for m in (card1, const, any_t)], run_time=1.2)
            c.wait_until("called failure")
            self.play(FlashUnder(code.find('Failure "no more coins!"', line=3), color=RED), run_time=1.6)

            c.wait_until("first")
            first, arr = self.r1_tag("our first raise", YELLOW)
            self.play(FadeIn(first, shift=0.3 * DOWN), GrowArrow(arr), run_time=1.2)

            # Two insets: OCaml's own exception (L3), then ours.
            lab1 = T("from OCaml", size=TAG, color=DIM)
            exc1 = toplevel('Exception: Match_failure ("//toplevel//", 1, 7).', DIM)
            ins1 = VGroup(lab1, exc1).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            fr1 = inset_frame(ins1)
            inset1 = VGroup(fr1, ins1)
            place(inset1, left=-6.5, top=B - 0.3)

            lab2 = T("from our program", size=TAG, color=FG)
            exc2 = toplevel('Exception: Failure "no more coins!".', RED)
            ins2 = VGroup(lab2, exc2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            fr2 = inset_frame(ins2)
            inset2 = VGroup(fr2, ins2)
            inset2.next_to(inset1, DOWN, buff=0.2, aligned_edge=LEFT)

            c.wait_until("before")
            self.play(FadeIn(inset1, shift=0.3 * UP), run_time=1.2)

            c.wait_until("own")
            src = code.find('Failure "no more coins!"', line=3)
            dst = exc2.find('Failure "no more coins!"')
            dst_ids = {id(g) for g in dst}
            rest = [g for g in exc2.line(0) if id(g) not in dst_ids]
            self.play(*[TransformFromCopy(s, d) for s, d in zip(src, dst)],
                      *[FadeIn(g) for g in rest], FadeIn(fr2), FadeIn(lab2), run_time=1.8)
            settle(self, inset2)

            later = tag("exceptions: a later lecture", DIM)
            later.next_to(inset2, RIGHT, buff=0.4)
            if later.get_right()[0] > 6.6:
                later = VGroup(tag("exceptions:", DIM), tag("a later lecture", DIM)).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.14)
                later.next_to(inset2, RIGHT, buff=0.4)
            c.wait_until("later")
            self.play(FadeIn(later, shift=0.3 * UP), run_time=1.0)
        self.c2 = (first, arr, inset1, inset2, later)

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        code, L, B = self.code, self.L, self.B
        first, arr, inset1, inset2, later = self.c2
        with self.say("c4.code.3") as c:
            clause3 = VGroup(*code.find("c::till, amt -> if amt < c then change till amt", line=4), *L[5])
            self.play(Transform(self.box, token_box(clause3, VGroup(*L[4], *L[5]))),
                      FadeOut(first), FadeOut(arr), run_time=1.5)

            c.wait_until("names")
            pat = code.find("c::till", line=4)
            self.play(FlashUnder(pat, color=YELLOW), run_time=1.4)

            c.wait_until("first coin")
            cg = pat[0:1]
            first_coin = place(tag("first coin", YELLOW), cx=cg.get_center()[0], top=B - 0.3)
            a1 = pointer(first_coin.get_top() + 0.04 * UP, cg.get_bottom() + 0.04 * DOWN, YELLOW)
            self.play(*[FadeOut(m) for m in (inset1, inset2, later)],
                      time_span(FadeIn(first_coin, shift=0.3 * UP), 0.4, 1.3),
                      time_span(GrowArrow(a1), 0.4, 1.3), *recolor(cg, YELLOW), run_time=1.3)

            c.wait_until("the rest")
            tg = pat[3:7]
            rest = place(tag("the rest", TEAL), left=tg.get_left()[0] + 0.2, top=B - 0.95)
            rest2 = tag(": a new name", TEAL)
            rest2.next_to(rest, RIGHT, buff=0.04).align_to(rest, DOWN)
            a2 = pointer(rest.get_corner(UL) + 0.3 * RIGHT + 0.04 * UP, tg.get_bottom() + 0.04 * DOWN, TEAL)
            self.play(*recolor(tg, TEAL), FadeIn(rest, shift=0.3 * UP), GrowArrow(a2), run_time=1.2)

            c.wait_until("fresh")
            self.play(FadeIn(rest2, shift=0.2 * LEFT), run_time=1.0)

            c.wait_until("from here on")
            later_tills = [code.find("till", line=4, nth=1), code.find("till", line=5)]
            self.play(*[FlashUnder(t, color=TEAL) for t in later_tills], run_time=1.6)

            c.wait_until("small")
            ifp = code.find("if amt < c then change till amt", line=4)
            ul = underline(ifp, YELLOW, buff=0.07)
            self.play(Create(ul), run_time=1.2)

            card3 = self.k3
            place(card3, right=6.3, top=B - 0.3)
            c.wait_until("too large")
            self.play(FadeIn(card3, shift=0.4 * LEFT), run_time=1.0)

            c.wait_until("obs3")
            self.play(FlashAround(card3, color=BLUE, time_width=1.5), run_time=1.5)
        self.c3 = (first_coin, a1, rest, rest2, a2, ul)
        self.card3 = card3

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        code, L, B = self.code, self.L, self.B
        with self.say("c4.code.4") as c:
            elsep = code.find("else c :: change (c::till) (amt - c)", line=5)
            self.play(Transform(self.box, token_box(elsep, L[5])),
                      *[FadeOut(m) for m in self.c3], run_time=1.3)

            card2 = self.k2
            place(card2, left=-6.5, top=B - 0.3)
            c.wait_until("the coin fits")
            self.play(FadeIn(card2, shift=0.4 * LEFT), run_time=1.0)

            c.wait_until("cons")
            self.play(FlashAround(code.find("c ::", line=5), color=TEAL), run_time=1.4)
            c.wait_until("the amount minus")
            amt = code.find("(amt - c)", line=5)
            self.play(FlashUnder(amt, color=GOLD), run_time=1.4)

            c.wait_until("back")
            ct = code.find("(c::till)", line=5)
            self.play(Transform(self.box, token_box(ct, L[5])), FadeOut(self.card3), run_time=1.2)
            c.wait_until("it's the coin")
            self.play(*recolor(ct[1:2], YELLOW), *recolor(ct[4:8], TEAL), run_time=1.2)

            c.wait_until("again")
            back_t = place(tag("put the coin back", YELLOW), cx=ct.get_center()[0], top=B - 0.3)
            self.play(FadeIn(back_t, shift=0.3 * UP), run_time=1.0)

            # Forget it: (c::till) becomes till, in RED.
            c.wait_until("forget")
            for g in [*ct, *amt]:
                g.save_state()
            step = (ct[8].get_center()[0] - ct[0].get_center()[0]) / 8
            strike = Line(back_t.get_left() + 0.08 * LEFT, back_t.get_right() + 0.08 * RIGHT,
                          color=RED, stroke_width=4)
            self.play(*[g.animate.set_opacity(0) for g in (ct[0], ct[1], ct[2], ct[3], ct[8])],
                      *[g.animate.shift(LEFT * 4 * step).set_color(RED) for g in ct[4:8]],
                      *[g.animate.shift(LEFT * 5 * step) for g in amt],
                      FadeOut(self.box), Create(strike), run_time=1.6)

            call = Code("change [50; 20; 10; 5; 2; 1] 43", size=CODE_SIZE)
            place(call, left=-4.2, top=B - 1.15)
            exc3 = toplevel('Exception: Failure "no more coins!".', RED)
            exc3.next_to(call, DOWN, buff=0.2, aligned_edge=LEFT)
            c.wait_until("short")
            self.play(time_span(FadeOut(card2), 0, 0.5), time_span(FadeIn(call, shift=0.3 * UP), 0.3, 1.1),
                      run_time=1.1)
            c.wait_until("would fail")
            self.play(FadeIn(exc3, shift=0.3 * UP), run_time=1.0)

            sum_l = MathTex(r"20 + 10 + 5 + 2 + 1", font_size=48, color=GOLD)
            sum_r = MathTex(r"= 38", font_size=48, color=GOLD)
            VGroup(sum_l, sum_r).arrange(RIGHT, buff=0.2).next_to(exc3, DOWN, buff=0.3)
            c.wait_until("twenty")
            self.play(Write(sum_l), run_time=min(2.2, c.until("thirty-eight", floor=1.0)))
            c.wait_until("thirty-eight")
            self.play(FadeIn(sum_r, shift=0.2 * LEFT), run_time=1.0)
        self.c4 = (back_t, strike)
        self.demo = (call, exc3, sum_l, sum_r)
        self.undo = [*ct, *amt]

    # ------------------------------------------------------------------ clip 5
    def clip5(self):
        code, L, B = self.code, self.L, self.B
        with self.say("c4.code.5") as c:
            self.play(*[Restore(g) for g in self.undo], *[FadeOut(m) for m in self.c4], run_time=1.1)
            reply = Code(REPLY, size=CODE_SIZE)
            place(reply, left=CODE_LEFT, top=B - 0.6)
            self.play(FadeIn(reply, shift=0.3 * UP), run_time=1.0)

            p1 = reply.find("int list", nth=0)
            p2 = reply.find("int", nth=1)
            p3 = reply.find("int list", nth=1)
            braces, labels = [], []
            for p, text in ((p1, "till"), (p2, "amount"), (p3, "coins to hand over")):
                b = Brace(p, DOWN, buff=0.1).set_color(DIM)
                lab = tag(text).next_to(b, DOWN, buff=0.1)
                braces.append(b)
                labels.append(lab)
            if labels[2].get_left()[0] < labels[1].get_right()[0] + 0.35:
                labels[2].shift(RIGHT * (labels[1].get_right()[0] + 0.35 - labels[2].get_left()[0]))

            # The forget demo clears as the first brace grows (it needs the rows under the reply).
            c.wait_until("the till")
            self.play(*[time_span(FadeOut(m), 0, 0.6) for m in self.demo],
                      time_span(GrowFromCenter(braces[0]), 0.4, 1.4),
                      time_span(FadeIn(labels[0], shift=0.2 * UP), 0.4, 1.4), run_time=1.4)
            for i, cue in ((1, "the amount"), (2, "the coins")):
                c.wait_until(cue)
                self.play(GrowFromCenter(braces[i]), FadeIn(labels[i], shift=0.2 * UP), run_time=0.9)

            c.wait_until("ints")
            self.play(*[FlashUnder(reply.find("int", nth=k), color=GREEN) for k in range(3)], run_time=1.5)
            c.wait_until("subtracts")
            minus = code.find("-", line=5)
            int_only = place(tag("int only", GREEN), cx=minus.get_center()[0], top=B - 0.22)
            self.play(FlashAround(minus, color=GREEN), FadeIn(int_only, shift=0.3 * UP), run_time=1.3)

            c.wait_until("fits")
            never, arr2 = self.r1_tag("never returns", RED)
            self.play(FlashAround(self.raise_g, color=RED), FadeIn(never, shift=0.3 * DOWN),
                      GrowArrow(arr2), run_time=1.3)
            c.wait_until("stand in")
            self.play(FlashUnder(p3, color=GREEN), run_time=1.5)
        self.annot = [*braces, *labels, int_only, never, arr2]
