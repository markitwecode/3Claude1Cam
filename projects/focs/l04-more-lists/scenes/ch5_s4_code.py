"""Chapter 5, scene 4: the code for every way to make change (In [72]). Clips c5.code.1 – c5.code.4.

HAND-OFF TO s5 (ch5_s5_allc): the scene ends on In [72] alone, then fades it.
  code = Code(SRC, size=24)            # default line_spacing, default highlighting, every line opacity 1
  code.shift(RIGHT * (-6.2 - code.get_left()[0]) + UP * (3.6 - code.get_top()[1]))
  i.e. CODE_SIZE = 24, left x = -6.2, top y = 3.6 (bounding box of the whole Code).
  SRC is verbatim the notes' In [72] (p. 34), `else` one column left of `if`.

Layout: the code fills the width at the top (62 columns at size 24 is ~12.4 wide). Free space it
leaves: right of lines 0-3 (clip 1's [[]] / [] boxes), left of lines 4-10 (clip 2/3 labels), the
line-8 slot above `(c::till)` ("c goes back"), and the band under the code (the greedy inset, the
dead-end row, then OCaml's reply and the three checks).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = (
    "let rec change till amt =\n"
    "  match till, amt with\n"
    "  | _       , 0   -> [ [] ]\n"
    "  | []      , _   -> []\n"
    "  | c::till , amt -> if amt < c then change till amt\n"
    "                    else let rec allc = function\n"
    "                           | [] -> []\n"
    "                           | cs :: css -> (c::cs) :: allc css\n"
    "                         in\n"
    "                           allc (change (c::till) (amt - c)) @\n"
    "                                 change till amt"
)
CODE_SIZE = 24
CODE_LEFT = -6.2
CODE_TOP = 3.6

REPLY = "val change : int list -> int -> int list list = <fun>"
CHECKS = [("change [5; 2] 0", "- : int list list = [[]]"),
          ("change [5; 2] 1", "- : int list list = []"),
          ("change [5; 2] 6", "- : int list list = [[2; 2; 2]]")]
REPLY_GAP = 0.22          # code bottom -> reply top
ROW_PITCH = 0.44          # baseline to baseline in the check stack
FIRST_ROW_DROP = 0.58     # reply baseline -> first check baseline
REPLY_COL = 0.9           # gap between a call and its reply

LABEL = 30
BOX_SCALE = 0.85          # the [[]] / [] boxes beside clauses 1 and 2

# ── the coin (copied from ch1_s1_hook) and the chapter's solution boxes ──────────
COIN_R = 0.42
COIN_LABEL = 34
SMALL = 0.6               # coins inside a solution


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def solution(values):
    """One solution (an int list): small coins in a row inside a TEAL box; [] is the box empty."""
    side = 2 * COIN_R * SMALL
    if values:
        coins = VGroup(*[coin(v).scale(SMALL) for v in values]).arrange(RIGHT, buff=0.1)
        w = coins.width + 0.24
    else:
        coins = VGroup()
        w = side + 0.24
    box = RoundedRectangle(corner_radius=0.1, width=w, height=side + 0.24).set_stroke(TEAL, 3)
    if values:
        box.move_to(coins)
    return VGroup(box, coins)


def solutions(sols):
    """A list of solutions: solution boxes in a row inside a bigger TEAL box; [] is it empty."""
    inner_h = 2 * COIN_R * SMALL + 0.24
    if sols:
        row = VGroup(*sols).arrange(RIGHT, buff=0.2)
        w, h = row.width + 0.4, row.height + 0.4
    else:
        row = VGroup()
        w = h = inner_h + 0.4
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(TEAL, 4)
    if sols:
        box.move_to(row)
    return VGroup(box, row)


_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


def baseline(code):
    """y of the text baseline of a Code."""
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def G(glyphs):
    return VGroup(*glyphs)


class ChangeAllCode(NarratedScene):
    def construct(self):
        code = Code(SRC, size=CODE_SIZE)
        code.shift(RIGHT * (CODE_LEFT - code.get_left()[0]) + UP * (CODE_TOP - code.get_top()[1]))
        code.save_state()
        self.code = code
        self.L = [code.line(i) for i in range(11)]
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        # end on In [72] alone (s5 opens from it), then an empty frame
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def find(self, sub, line, nth=0):
        return self.code.find(sub, line=line, nth=nth)

    # ── c5.code.1: header as in greedy, the two base clauses, no more raise ──────
    def clip1(self):
        code, L = self.code, self.L
        with self.say("c5.code.1") as c:
            self.play(FadeIn(code, shift=0.2 * UP), run_time=1.5)

            c.wait_until("It starts just like")
            head = G([*L[0], *L[1]])
            brace = Brace(head, RIGHT, buff=0.25).set_color(DIM)
            greedy = T("as in greedy", size=LABEL, color=DIM).next_to(brace, RIGHT, buff=0.2)
            self.play(GrowFromCenter(brace), FadeIn(greedy, shift=0.3 * LEFT), run_time=1.0)

            c.wait_until("match")
            self.play(FlashUnder(G(self.find("match till, amt with", 1)), color=YELLOW), run_time=1.5)

            c.wait_until("first")
            self.box = token_box(self.find("_       , 0   -> [ [] ]", 2), L[2])
            self.play(FadeIn(self.box), FadeOut(brace), FadeOut(greedy), run_time=1.2)

            # [[]]: a list holding one empty solution, out of the clause's result
            ok = solutions([solution([])]).scale(BOX_SCALE)
            ok_lab = T("one way", size=LABEL, color=GREEN)
            y0 = L[2].get_center()[1] + 0.1
            ok.move_to([-0.4 + ok.width / 2, y0, 0])
            ok_lab.next_to(ok, RIGHT, buff=0.25)
            nil = solutions([]).scale(BOX_SCALE)
            nil.move_to([ok_lab.get_right()[0] + 0.9 + nil.width / 2, y0, 0])
            no_lab = T("no ways", size=LABEL, color=RED).next_to(nil, RIGHT, buff=0.25)

            c.wait_until("a list holding")
            src = G(self.find("[ [] ]", 2))
            self.play(FadeIn(ok, target_position=src.get_center(), scale=0.35),
                      time_span(FadeIn(ok_lab, shift=0.3 * LEFT), 0.6, 1.5), run_time=1.5)

            c.wait_until("second")
            self.play(Transform(self.box, token_box(self.find("[]      , _   -> []", 3), L[3])), run_time=1.2)
            c.wait_until("gives no solutions")
            src = G(self.find("[]", 3, nth=1))
            self.play(FadeIn(nil, target_position=src.get_center(), scale=0.35),
                      time_span(FadeIn(no_lab, shift=0.3 * LEFT), 0.6, 1.5), run_time=1.5)

            # greedy's raise, struck out: this version returns [] instead
            rz = Code('raise (Failure "no more coins!")', size=CODE_SIZE).set_color(RED)
            g_lab = T("greedy", size=28, color=DIM)
            body = VGroup(g_lab, rz).arrange(RIGHT, buff=0.4)
            g_lab.align_to(rz, DOWN).shift(0.02 * DOWN)
            fr = SurroundingRectangle(body, buff=0.22, corner_radius=0.1, color=DIM, stroke_width=2)
            inset = VGroup(fr, body).move_to([0, code.get_bottom()[1] - 1.05, 0])
            strike = Line(rz.get_left() + 0.12 * LEFT, rz.get_right() + 0.12 * RIGHT).set_stroke(FG, 5)

            c.wait_until("noraise")
            self.play(FadeIn(inset, shift=0.3 * UP), run_time=1.0)
            c.wait_until("this version")
            self.play(Create(strike), *set_alpha([rz], 0.55), run_time=0.9)
            settle(self, inset)
            c.wait_until("returns nil")
            self.play(FlashAround(src, color=TEAL), FlashAround(nil, color=TEAL),
                      run_time=min(1.3, max(0.7, c.remaining)))
        self.c1 = (ok, ok_lab, nil, no_lab)
        self.inset = VGroup(inset, strike)

    # ── c5.code.2: the third clause, too big -> skip, else both ──────────────────
    def clip2(self):
        code, L = self.code, self.L
        with self.say("c5.code.2") as c:
            self.play(Transform(self.box, token_box(self.find("c::till", 4), L[4])),
                      *[time_span(FadeOut(m), 0.5, 1.3) for m in self.c1], run_time=1.5)

            cg = self.find("c", 4)
            tg = self.find("till", 4)
            lab_c = T("largest coin", size=LABEL, color=YELLOW)
            lab_c.next_to(self.box, DOWN, buff=0.14)
            lab_c.set_x(max(G(cg).get_x(), -6.55 + lab_c.width / 2))
            lab_r = T("rest of the till", size=LABEL, color=TEAL)
            lab_r.next_to(lab_c, DOWN, buff=0.18)
            lab_r.set_x(max(G(tg).get_x() + 0.3, -6.55 + lab_r.width / 2))

            c.wait_until("largest coin")
            self.play(*recolor(cg, YELLOW), FadeIn(lab_c, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("the rest of the till")
            self.play(FlashUnder(G(tg), color=TEAL), FadeIn(lab_r, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("toobig")
            ifx = self.find("if amt < c then change till amt", 4)
            self.play(Transform(self.box, token_box(ifx, L[4])), FadeOut(self.inset), run_time=1.5)
            big = T("too big: skip only", size=LABEL, color=BLUE)
            big.next_to(self.box, UP, buff=0.12).set_x(G(ifx).get_x())
            c.wait_until("too big")
            self.play(FadeIn(big, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("We make change from the rest")
            self.play(FlashUnder(G(self.find("change till amt", 4)), color=BLUE),
                      FadeOut(lab_c), FadeOut(lab_r), run_time=1.5)

            c.wait_until("else")
            allc_def = [*self.find("let rec allc = function", 5), *L[6], *L[7], *L[8]]
            self.play(Transform(self.box, token_box(self.find("else", 5), L[5])), FadeOut(big),
                      *set_alpha(allc_def, 0.3), run_time=1.5)
            settle(self, code)

    # ── c5.code.3: use c (it goes back), skip c, @, a dead end adds nothing, allc ─
    def clip3(self):
        code, L = self.code, self.L
        lb = dict(height=L[9].height + 0.12)
        with self.say("c5.code.3") as c:
            use = self.find("allc (change (c::till) (amt - c))", 9)
            lab_use = T("use c", size=LABEL, color=YELLOW)
            lab_use.next_to(token_box(use, L[9], **lb), LEFT, buff=0.2)
            self.play(Transform(self.box, token_box(use, L[9], **lb)), *recolor(use, YELLOW),
                      FadeIn(lab_use, shift=0.3 * RIGHT), run_time=1.5)

            c.wait_until("back")
            back = self.find("(c::till)", 9)
            lab_back = T("c goes back", size=28, color=TEAL)
            lab_back.move_to([G(back).get_x(), (L[7].get_bottom()[1] + self.box.get_top()[1]) / 2, 0])
            self.play(FlashAround(G(back), color=TEAL), FadeIn(lab_back, shift=0.2 * DOWN), run_time=1.5)

            c.wait_until("skipcall")
            skip = self.find("change till amt", 10)
            lab_skip = T("skip c", size=LABEL, color=BLUE)
            lab_skip.next_to(token_box(skip, L[10], **lb), LEFT, buff=0.2)
            self.play(Transform(self.box, token_box(skip, L[10], **lb)), *recolor(skip, BLUE),
                      FadeIn(lab_skip, shift=0.3 * RIGHT), run_time=1.5)

            c.wait_until("at")
            at = self.find("@", 9)
            self.play(Transform(self.box, token_box(at, L[9], **lb)), *recolor(at, GOLD), run_time=1.2)
            self.play(FlashAround(G(at), color=GOLD), run_time=1.2)

            # [] @ [[2; 2; 2]] = [[2; 2; 2]]
            dead = solutions([])
            at_m = Mono("@", size=48, color=GOLD)
            row = solutions([solution([2, 2, 2])])
            eq = MathTex("=", font_size=60, color=FG)
            res = row.copy()
            line = VGroup(dead, at_m, row, eq, res).arrange(RIGHT, buff=0.4)
            line.move_to([0, (code.get_bottom()[1] - 3.5) / 2 - 0.05, 0])
            c.wait_until("deadend")
            self.play(FadeIn(row, shift=0.3 * UP), run_time=1.0)
            self.play(FadeIn(dead, shift=0.5 * RIGHT), FadeIn(at_m, shift=0.5 * RIGHT), run_time=1.0)
            c.wait_until("changes nothing")
            self.play(FadeIn(eq), TransformFromCopy(row, res), run_time=1.5)

            c.wait_until("allc")
            ag = self.find("allc", 9)
            self.play(Transform(self.box, token_box(ag, L[9], **lb)), FlashAround(G(ag), color=YELLOW),
                      run_time=1.5)
            settle(self, code)
        self.c3 = (self.box, lab_use, lab_back, lab_skip, dead, at_m, row, eq, res)

    # ── c5.code.4: OCaml's reply, then the three checks ──────────────────────────
    def clip4(self):
        code = self.code
        reply = Code(REPLY, size=CODE_SIZE)
        reply.shift(RIGHT * (CODE_LEFT - reply.get_left()[0]) + UP * (code.get_bottom()[1] - REPLY_GAP - reply.get_top()[1]))
        rb = baseline(reply)
        calls, outs = [], []
        for i, (q, a) in enumerate(CHECKS):
            cq = put(Code(q, size=CODE_SIZE), CODE_LEFT, rb - FIRST_ROW_DROP - i * ROW_PITCH)
            ca = Code(a, size=CODE_SIZE)
            if i == 2:
                ca.set_color(GREEN)
            put(ca, cq.get_right()[0] + REPLY_COL, rb - FIRST_ROW_DROP - i * ROW_PITCH)
            calls.append(cq)
            outs.append(ca)
        with self.say("c5.code.4") as c:
            self.play(*[time_span(FadeOut(m), 0, 0.8) for m in self.c3],
                      time_span(Restore(code), 0, 1.2),
                      time_span(FadeIn(reply, shift=0.3 * UP), 0.5, 1.5), run_time=1.5)

            c.wait_until("It takes")
            self.play(FlashUnder(G(reply.find("int list -> int")), color=GREEN), run_time=1.3)
            c.wait_until("returns")
            ret = reply.find("int list list")
            self.play(*recolor(ret, GREEN), FlashAround(G(ret), color=GREEN), run_time=1.5)
            settle(self, reply)

            c.wait_until("check")
            self.play(LaggedStart(*[FadeIn(q, shift=0.3 * UP) for q in calls], lag_ratio=0.25), run_time=1.5)
            for i, cue in enumerate(("zero", "one", "six")):
                c.wait_until(cue)
                self.play(FadeIn(outs[i], shift=0.3 * LEFT), run_time=1.0)
                if i == 1:
                    c.wait_until("No way")
                    self.play(FlashUnder(G(outs[1].find("[]")), color=RED), run_time=1.0)
            c.wait_until("the answer from our tree")
            self.play(FlashAround(G(outs[2].find("[[2; 2; 2]]")), color=GREEN), run_time=1.5)
        # the code alone for s5
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in (reply, *calls, *outs)], run_time=1.0)
