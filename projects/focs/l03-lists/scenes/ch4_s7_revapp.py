"""Chapter 4, scene 7: reversing in linear time. Card piles, rev_app, its flat trace, what
rev_app means in general, the rev wrapper, one cons per element, the n(n+1)/2 vs n graph and
two computers with the same shapes. Clips c4.rev.1 - c4.rev.5.

Layout: T = top band (rev_app header / rev def + reply), L = the two piles (x -6.4..-2.4),
R = the trace column (rows left-aligned at X0, size 36, DIM => arrows as in ch3_s3_trace).
Cards and graph ported from archive/v1/scenes/s7_rev.py. Every `rev_app` / `rev` is YELLOW
(ch3's convention: the function name keeps its colour everywhere).

STATUS: built; check clean except counter ticks (0/1/2 are meant to flick by) and two dwell
values exactly at their threshold. Ends on an empty frame (graph fades, nothing carried over).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# s8 reuses this exact text.
REV_APP = """let rec rev_app xs ys =
  match xs, ys with
  | [], ys    -> ys
  | x::xs, ys -> rev_app xs (x::ys)"""
TRACE = ["rev_app [1; 2; 3] []", "rev_app [2; 3] [1]", "rev_app [3] [2; 1]",
         "rev_app [] [3; 2; 1]", "[3; 2; 1]"]
REV = "let rev xs = rev_app xs []"
REV_REPLY = "val rev : 'a list -> 'a list = <fun>"

HERO = 40        # rev_app while it is the hero (rev.2)
SMALL = 28       # rev_app as the header over the trace (rev.3, rev.4)
SIZE = 36        # trace rows and the examples in the right column
X0 = -0.8        # left edge of every row in the right column
BASE = [0.7, -0.1, -0.9, -1.7, -2.5]     # baselines of the trace rows
ARROW_GAP = 0.3

# ── cards & piles (v1 s7_rev) ──────────────────────────────────────────────────
CARD_W, CARD_H = 1.4, 0.8
SLOT = 0.92                     # vertical step between stacked cards
BIG = 1.4                       # cards drawn larger while alone on screen (rev.1)
WIDE = (np.array([-2.6, -1.75, 0.0]), np.array([2.6, -1.75, 0.0]))   # rev.1
MID = (np.array([-1.3, -2.4, 0.0]), np.array([1.3, -2.4, 0.0]))      # under the code (rev.2)
SIDE = (np.array([-5.7, -1.9, 0.0]), np.array([-3.1, -1.9, 0.0]))    # beside the trace

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789")


def card(v):
    box = RoundedRectangle(width=CARD_W, height=CARD_H, corner_radius=0.12, stroke_color=BLUE,
                           stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(box, value_label(v).move_to(box))


def outline():
    """An empty pile: a dashed card-shaped slot."""
    return DashedVMobject(RoundedRectangle(width=CARD_W, height=CARD_H, corner_radius=0.12,
                                           stroke_color=DIM, stroke_width=3), num_dashes=22)


def slot(base, k, s=1.0):
    return base + UP * SLOT * s * k


def gesture(start, end, color, angle=-0.55 * PI):
    """Curved dashed arrow: 'this card goes over there'."""
    arc = ArcBetweenPoints(start, end, angle=angle, color=color, stroke_width=3)
    arc.add_tip(tip_length=0.2, tip_width=0.2)
    tip = arc.pop_tips()[0]
    return VGroup(DashedVMobject(arc, num_dashes=14), tip)


# ── code rows (ch3_s3_trace) ───────────────────────────────────────────────────
def baseline(code):
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def part(code, sub, nth=0, line=None):
    """The glyphs of `sub` in `code`, as a fresh VGroup (never added to the scene itself)."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def C(src, size):
    """Code with the function names YELLOW wherever they appear (ch3's convention: the name
    keeps its colour everywhere): every `rev_app` and every standalone `rev`."""
    code = Code(src, size=size)
    for m in re.finditer(r"\brev_app\b|\brev\b", code.src):
        code._span(m.start(), m.end()).set_color(YELLOW)
    return code


def implies(row, base):
    return (MathTex(r"\Rightarrow", font_size=58, color=DIM)
            .next_to(row, LEFT, buff=ARROW_GAP).set_y(base + 0.12))


class LinearReverse(NarratedScene):
    def construct(self):
        self.setup_piles()
        self.card_piles()     # c4.rev.1
        self.the_code()       # c4.rev.2
        self.trace()          # c4.rev.3
        self.meaning()        # c4.rev.4
        self.cost()           # c4.rev.5
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── helpers ────────────────────────────────────────────────────────────────
    def setup_piles(self):
        L, R = WIDE
        self.cards = {v: card(v) for v in (1, 2, 3)}
        for k, v in enumerate((3, 2, 1)):                 # 1 on top
            self.cards[v].scale(BIG).move_to(slot(L, k, BIG))
        self.out_L = outline().scale(BIG).move_to(L)
        self.out_R = outline().scale(BIG).move_to(R)
        self.s = BIG

    def card_target(self, v, pos, color=BLUE, scale=1.0):
        t = self.cards[v].copy().scale(scale).move_to(pos)
        t.set_opacity(1)
        t[0].set_stroke(color)
        return t

    def lift(self, v, color=YELLOW):
        crd = self.cards[v]
        return Transform(crd, self.card_target(v, crd.get_center() + UP * 0.3 * self.s, color))

    def move(self, v, pos, arc=-PI / 2, scale=1.0):
        return Transform(self.cards[v], self.card_target(v, pos, BLUE, scale), path_arc=arc)

    def birth(self, dst, moves, ins=None, wrappers=None, rest_span=None):
        """Animations that build `dst` (a Code not on screen yet) out of copies of glyphs
        elsewhere (P11/P13). moves: (src, src_sub, src_nth, dst_sub, dst_nth, path_arc).
        Glyphs of dst not moved fade in (all of them, or only `ins`). Returns (anims, wrappers);
        commit() swaps the wrappers for dst once the play is over."""
        anims, used = [], set()
        wrappers = [] if wrappers is None else wrappers
        for w in wrappers:
            used |= {id(g) for g in w}
        for src, s_sub, s_nth, d_sub, d_nth, arc in moves:
            tgt = part(dst, d_sub, d_nth)
            anims.append(TransformFromCopy(part(src, s_sub, s_nth), tgt, path_arc=arc))
            wrappers.append(tgt)
            used |= {id(g) for g in tgt}
        if ins is None:
            rest = [g for g in dst.text if id(g) not in used]
        else:
            rest = [g for sub, nth in ins for g in part(dst, sub, nth)]
        if rest:
            r = VGroup(*rest)
            fade = FadeIn(r, shift=0.15 * DOWN)
            anims.append(time_span(fade, *rest_span) if rest_span else fade)
            wrappers.append(r)
        return anims, wrappers

    def commit(self, dst, wrappers):
        self.remove(*wrappers)
        self.add(dst)

    # ── c4.rev.1: reversing a pile of cards ───────────────────────────────────
    def card_piles(self):
        L, R = WIDE
        cards = self.cards
        badge = VGroup(Mono("nrev", 48, color=RED), MathTex(r"O(n^2)", font_size=72, color=RED))
        badge.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        self.badge = badge
        with self.say("c4.rev.1") as c:
            self.play(FadeIn(badge, scale=0.9), run_time=1.0)
            c.wait_until("cards")
            self.play(badge.animate.scale(0.65).move_to(UP * 3.1),
                      LaggedStart(*[FadeIn(cards[v], shift=0.3 * DOWN) for v in (3, 2, 1)],
                                  lag_ratio=0.25),
                      FadeIn(self.out_R), run_time=1.6)

            c.wait_until("take the top card")
            self.play(self.lift(1), run_time=0.8)
            c.wait_until("put it on a new pile")
            self.play(self.move(1, slot(R, 0, BIG)), time_span(FadeOut(self.out_R), 1.2, 1.5),
                      run_time=1.5)

            c.wait_until("again")
            self.play(self.move(2, slot(R, 1, BIG)), run_time=1.3)
            self.play(self.move(3, slot(R, 2, BIG)), run_time=0.9)

            c.wait_until("done")
            self.out_L.move_to(slot(L, 0, BIG))
            self.play(Create(self.out_L), run_time=1.0)
            c.wait_until("the new pile")
            self.play(FlashAround(VGroup(*cards.values()), color=YELLOW, time_width=1.5),
                      run_time=1.6)

    # ── c4.rev.2: rev_app, the code ───────────────────────────────────────────
    def the_code(self):
        L, R = MID
        cards = self.cards
        code = self.code = C(REV_APP, size=HERO).to_edge(UP, buff=0.55)
        y_lab = L[1] - CARD_H / 2 - 0.4
        self.lab_xs = Mono("xs", 36, color=FG).move_to([L[0], y_lab, 0])
        self.lab_ys = Mono("ys", 36, color=TEAL).move_to([R[0], y_lab, 0])

        with self.say("c4.rev.2") as c:
            back = [self.move(v, slot(L, k), arc=PI / 2, scale=1 / BIG)
                    for k, v in enumerate((3, 2, 1))]
            self.out_R.scale(1 / BIG).move_to(R)
            self.play(FadeOut(self.badge, shift=0.3 * UP), FadeOut(self.out_L),
                      LaggedStart(*back, lag_ratio=0.15),
                      FadeIn(code, shift=0.3 * DOWN), time_span(FadeIn(self.out_R), 1.2, 1.8),
                      run_time=1.8)
            self.s = 1.0
            self.out_L.scale(1 / BIG)

            c.wait_until("the pile exes")
            box = self.box = token_box(code.find("xs", line=0), code.line(0))
            self.play(FadeIn(box), TransformFromCopy(part(code, "xs", line=0), self.lab_xs),
                      run_time=1.2)
            c.wait_until("the pile whys")
            self.play(Transform(box, token_box(code.find("ys", line=0), code.line(0))),
                      TransformFromCopy(part(code, "ys", line=0), self.lab_ys), run_time=1.2)

            c.wait_until("base")
            self.play(Transform(box, token_box(code.find("[]", line=2), code.line(2))),
                      run_time=1.0)
            c.wait_until("the answer is whys")
            self.play(Transform(box, token_box(code.find("ys", line=2, nth=1), code.line(2))),
                      FlashAround(self.lab_ys, color=TEAL), run_time=1.0)

            c.wait_until("step")
            self.play(Transform(box, token_box(code.find("x::xs", line=3), code.line(3))),
                      run_time=1.0)
            c.wait_until("take the head")
            self.play(Transform(box, token_box(code.find("x", line=3), code.line(3))),
                      self.lift(1), run_time=1.0)
            c.wait_until("cons it onto whys")
            self.gest = gesture(cards[1].get_top() + UP * 0.1,
                                self.out_R.get_top() + UP * 0.12, TEAL)
            self.play(Transform(box, token_box(code.find("(x::ys)", line=3), code.line(3))),
                      Create(self.gest), run_time=1.3)

            c.wait_until("recur")
            self.play(Transform(box, token_box(code.find("rev_app xs", line=3), code.line(3))),
                      FlashAround(VGroup(cards[2], cards[3]), color=YELLOW), run_time=1.2)

    # ── c4.rev.3: the trace, one card per line ────────────────────────────────
    def step(self, k, run_time, extra=()):
        """Card k+1 crosses to the second pile while trace row k+1 is born from row k."""
        MOVES = [
            [("rev_app", 0, "rev_app", 0, 0), ("[", 0, "[", 0, 0), ("2; 3]", 0, "2; 3]", 0, 0),
             ("1", 0, "1", 0, -0.9), ("[", 1, "[", 1, 0), ("]", 1, "]", 1, 0)],
            [("rev_app", 0, "rev_app", 0, 0), ("[", 0, "[", 0, 0), ("3]", 0, "3]", 0, 0),
             ("2", 0, "2", 0, -0.9), (";", 0, ";", 0, -0.9), ("[", 1, "[", 1, 0),
             ("1]", 0, "1]", 0, 0)],
            [("rev_app", 0, "rev_app", 0, 0), ("[", 0, "[", 0, 0), ("]", 0, "]", 0, 0),
             ("3", 0, "3", 0, -0.9), ("[", 1, "[", 1, 0), ("2; 1]", 0, "2; 1]", 0, 0)],
        ]
        src, dst = self.rows[k], self.rows[k + 1]
        anims, w = self.birth(dst, [(src, *m) for m in MOVES[k]])
        self.play(*anims, self.move(k + 1, slot(SIDE[1], k)),
                  FadeIn(self.arrows[k + 1], shift=0.15 * DOWN), *extra, run_time=run_time)
        self.commit(dst, w)

    def trace(self):
        L, R = SIDE
        d = SIDE[0] - MID[0]
        cards, code = self.cards, self.code
        rows = self.rows = [put(C(s, size=SIZE), X0, b) for s, b in zip(TRACE, BASE)]
        arrows = self.arrows = [None] + [implies(r, b) for r, b in zip(rows[1:], BASE[1:])]

        with self.say("c4.rev.3") as c:
            head = code.copy().scale(SMALL / HERO).move_to(UP * 2.55)
            self.play(Transform(code, head), FadeOut(self.box), FadeOut(self.gest),
                      Transform(cards[1], self.card_target(1, slot(L, 2))),
                      *[m.animate.shift(d) for m in (cards[2], cards[3], self.out_R,
                                                     self.lab_xs, self.lab_ys)],
                      run_time=1.3)
            self.out_L.move_to(L)
            self.play(FadeIn(rows[0], shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("the one moves across")
            self.step(0, 1.8, extra=[time_span(FadeOut(self.out_R), 1.4, 1.8)])
            c.wait_until("t2")
            self.step(1, 1.4)
            c.wait_until("t3")
            self.step(2, 1.0)

            c.wait_until("t4")
            self.play(Create(self.out_L), FlashAround(part(rows[3], "[]"), color=TEAL),
                      run_time=1.0)
            c.wait_until("return the second")
            anims, w = self.birth(rows[4], [(rows[3], "[3; 2; 1]", 0, "[3; 2; 1]", 0, 0)])
            self.play(*anims, FadeIn(arrows[4], shift=0.15 * DOWN), run_time=1.5)
            self.commit(rows[4], w)
            c.wait_until("three two one")
            self.play(FlashAround(rows[4], color=GREEN),
                      FlashAround(VGroup(*cards.values()), color=YELLOW), run_time=1.3)

            c.wait_until("flat")
            self.flat = SurroundingRectangle(VGroup(*rows[:4]), color=GREEN, buff=0.1)
            self.iter_lab = T("iterative", 34, color=DIM).next_to(self.flat, DOWN, buff=0.22,
                                                                  aligned_edge=RIGHT)
            self.play(Create(self.flat), time_span(FadeIn(self.iter_lab, shift=0.2 * DOWN),
                                                   0.8, 1.6), run_time=1.6)
            c.wait_until("hands over")
            self.play(LaggedStart(*[FlashAround(a, color=YELLOW) for a in arrows[1:4]],
                                  lag_ratio=0.4), run_time=1.6)
            c.wait_until("is iterative")
            self.play(FlashUnder(self.iter_lab, color=YELLOW), run_time=1.0)

    # ── c4.rev.4: what rev_app means; the rev wrapper ─────────────────────────
    def meaning(self):
        L, R = SIDE
        cards, rows, arrows = self.cards, self.rows, self.arrows
        y_res = BASE[0] - 1.1
        call = put(C("rev_app [1; 2; 3] [4; 5]", size=SIZE), X0, BASE[0])
        res = put(C("[3; 2; 1; 4; 5]", size=SIZE), X0, y_res)
        arr = implies(res, y_res)
        piles = [*cards.values(), self.out_L, self.lab_xs, self.lab_ys]

        with self.say("c4.rev.4") as c:
            gone = [*rows[1:], *arrows[1:], self.flat, self.iter_lab]
            anims, w = self.birth(call, [(rows[0], "rev_app [1; 2; 3]", 0,
                                          "rev_app [1; 2; 3]", 0, 0)])
            self.play(*anims, FadeOut(rows[0]),
                      LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.08),
                      *set_alpha(piles, 0.35), run_time=1.5)
            self.commit(call, w)

            c.wait_until("reverses exes")
            ul_x = underline(part(call, "1; 2; 3"), BLUE)
            ul_r = underline(part(res, "3; 2; 1"), BLUE)
            anims, w = self.birth(res, [(call, str(v), 0, str(v), 0, -PI / 3) for v in (1, 2, 3)],
                                  ins=[("[", 0), (";", 0), (";", 1)])
            self.play(*anims, FadeIn(arr, shift=0.15 * DOWN), time_span(Create(ul_x), 0, 0.6),
                      time_span(Create(ul_r), 0.8, 1.4), run_time=1.4)

            c.wait_until("puts the result")
            ul_y = underline(part(call, "4; 5"), TEAL)
            ul_t = underline(part(res, "4; 5"), TEAL)
            anims, w = self.birth(res, [(call, "4; 5]", 0, "4; 5]", 0, 0)], ins=[(";", 2)],
                                  wrappers=w)
            self.play(*anims, time_span(Create(ul_y), 0, 0.5), time_span(Create(ul_t), 0.6, 1.1),
                      run_time=1.1)
            self.commit(res, w)

            # to reverse on its own: whys starts empty
            c.wait_until("wrap")
            back = [self.move(v, slot(L, k), arc=PI / 2) for k, v in enumerate((3, 2, 1))]
            self.out_R.move_to(R)
            self.play(*set_alpha([self.lab_xs, self.lab_ys], 1), FadeOut(self.out_L),
                      LaggedStart(*back, lag_ratio=0.2), time_span(FadeIn(self.out_R), 1.0, 1.6),
                      run_time=1.6)
            self.out_L.set_stroke(opacity=1)

            c.wait_until("whys empty")
            call0 = put(C(TRACE[0], size=SIZE), X0, BASE[0])
            res0 = put(C("[3; 2; 1]", size=SIZE), X0, y_res)
            a1, w1 = self.birth(call0, [(call, "rev_app [1; 2; 3]", 0, "rev_app [1; 2; 3]", 0, 0)])
            a2, w2 = self.birth(res0, [(res, "[3; 2; 1", 0, "[3; 2; 1", 0, 0),
                                       (res, "]", 0, "]", 0, 0)])
            self.play(*a1, *a2, FadeOut(call), FadeOut(res), FadeOut(ul_y), FadeOut(ul_t),
                      FlashAround(self.out_R, color=TEAL), run_time=1.5)
            self.commit(call0, w1)
            self.commit(res0, w2)

            c.wait_until("rev")
            df = C(REV, size=40).move_to(UP * 2.95)
            reply = C(REV_REPLY, size=28).next_to(df, DOWN, buff=0.35)
            anims, w = self.birth(df, [(call0, "rev_app", 0, "rev_app", 0, 0),
                                       (call0, "[]", 0, "[]", 0, 0)], rest_span=(0.5, 1.4))
            self.play(time_span(FadeOut(self.code, shift=0.3 * UP), 0, 0.6), *anims,
                      FadeOut(ul_x), FadeOut(ul_r),
                      time_span(FadeIn(reply, shift=0.15 * DOWN), 1.5, 2.2), run_time=2.2)
            self.commit(df, w)
            self.df, self.reply = df, reply

            c.wait_until("with nil")
            self.play(FlashAround(part(df, "[]"), color=TEAL),
                      FlashAround(part(call0, "[]"), color=TEAL), run_time=1.2)
        self.call0, self.res0, self.arr = call0, res0, arr

    # ── c4.rev.5: one cons per card; the graph; why big O ─────────────────────
    def cost(self):
        L, R = SIDE
        cards = self.cards
        with self.say("c4.rev.5", gap=2.4) as c:
            # the example becomes the toplevel call rev [1; 2; 3]; the counter asks the cost
            q = put(C("rev [1; 2; 3]", size=SIZE), X0, BASE[0])
            ans = put(C("- : int list = [3; 2; 1]", size=SIZE), X0, BASE[0] - 1.1)
            a1, w1 = self.birth(q, [(self.call0, "rev", 0, "rev", 0, 0),
                                    (self.call0, "[1; 2; 3]", 0, "[1; 2; 3]", 0, 0)])
            a2, w2 = self.birth(ans, [(self.res0, "[3; 2; 1]", 0, "[3; 2; 1]", 0, 0)])
            lbl = T("conses:", 40, color=GOLD)
            digits = [T(str(i), 40, color=GOLD) for i in range(4)]
            VGroup(lbl, digits[0]).arrange(RIGHT, buff=0.2).move_to([(L[0] + R[0]) / 2, 1.1, 0])
            for dg in digits[1:]:
                dg.move_to(digits[0])
            self.play(*a1, *a2, FadeOut(self.call0), FadeOut(self.res0), FadeOut(self.arr),
                      time_span(FadeIn(lbl, shift=0.2 * DOWN), 0.6, 1.3),
                      time_span(FadeIn(digits[0], shift=0.2 * DOWN), 0.6, 1.3), run_time=1.3)
            self.commit(q, w1)
            self.commit(ans, w2)

            c.wait_until("one cons for each")
            spans = [(0.0, 1.0), (1.15, 1.95), (2.1, 2.8)]
            anims = []
            for k, (a, b) in enumerate(spans):
                anims += [time_span(self.move(k + 1, slot(R, k)), a, b),
                          time_span(FadeOut(digits[k], shift=0.2 * UP), b - 0.15, b + 0.1),
                          time_span(FadeIn(digits[k + 1], shift=0.2 * UP), b - 0.15, b + 0.1)]
            self.out_L.move_to(L)
            self.play(*anims, time_span(FadeOut(self.out_R), 0.7, 1.0),
                      time_span(FadeIn(self.out_L), 2.5, 2.8), run_time=2.9)

            c.wait_until("exact")
            n = MathTex("n", font_size=56, color=GOLD)
            w1 = T("conses,", 36, color=GOLD)
            w2 = T("exactly", 36, color=YELLOW)
            grp = VGroup(n, w1, w2).arrange(RIGHT, buff=0.2)
            n.shift(UP * (w1[0].get_bottom()[1] - n.get_bottom()[1]))
            w2.shift(UP * (w1[0].get_bottom()[1] - w2[0].get_bottom()[1]))
            grp.move_to([(L[0] + R[0]) / 2, 1.1, 0])
            self.play(ReplacementTransform(digits[3], n, path_arc=PI / 2),
                      ReplacementTransform(lbl, w1), FadeIn(w2, shift=0.2 * LEFT), run_time=1.2)

            c.wait_until("linear time")
            big_o = MathTex("O(n)", font_size=72, color=GOLD).move_to([2.8, -1.95, 0])
            self.play(TransformFromCopy(n, big_o, path_arc=-PI / 4), run_time=1.3)

            # ── the graph (v1 s7_rev), right; the exact count and O(n) stay on the left ──
            c.wait_until("graph")
            axes = Axes(x_range=[0, 20, 5], y_range=[0, 220, 50], x_length=6.4, y_length=5.2,
                        tips=True, axis_config={"color": "#BBBBBB", "stroke_width": 2})
            axes.shift(np.array([-1.9, -2.45, 0]) - axes.c2p(0, 0))
            nums = VGroup(
                *[MathTex(str(v), font_size=34, color=DIM).next_to(axes.c2p(v, 0), DOWN, buff=0.2)
                  for v in (10, 20)],
                *[MathTex(str(v), font_size=34, color=DIM).next_to(axes.c2p(0, v), LEFT, buff=0.2)
                  for v in (100, 200)])
            xlab = VGroup(T("list length", 34), MathTex("n", font_size=42)).arrange(RIGHT, buff=0.15)
            xlab.next_to(axes.x_axis, DOWN, buff=0.6)
            ylab = T("conses", 34).next_to(axes.y_axis, UP, buff=0.15)
            big_o.generate_target().move_to([(L[0] + R[0]) / 2, -0.3, 0])
            sweep_clear(self, MoveToTarget(big_o), time_span(Create(axes), 0.3, 1.2),
                        time_span(FadeIn(nums), 0.6, 1.2), time_span(FadeIn(xlab), 0.6, 1.2),
                        time_span(FadeIn(ylab), 0.6, 1.2), keep=[n, w1, w2, big_o], run_time=1.2)

            c.wait_until("curve")
            curve = axes.plot(lambda x: x * (x + 1) / 2, x_range=[0, 20], color=RED,
                              stroke_width=5)
            nname = Mono("nrev", 32, color=RED)
            nform = MathTex(r"\frac{n(n+1)}{2}", font_size=42, color=RED)
            VGroup(nname, nform).arrange(DOWN, buff=0.15).next_to(axes.c2p(20, 210), RIGHT,
                                                                  buff=0.3)
            self.play(Create(curve), time_span(FadeIn(nname, shift=0.2 * LEFT), 1.0, 1.6),
                      time_span(FadeIn(nform, shift=0.2 * LEFT), 1.0, 1.6), run_time=1.6)

            c.wait_until("line")
            line = axes.plot(lambda x: x, x_range=[0, 20], color=GREEN, stroke_width=5)
            rname = Mono("rev", 32, color=GREEN)
            rform = MathTex("n", font_size=42, color=GREEN)
            VGroup(rname, rform).arrange(DOWN, buff=0.15).next_to(axes.c2p(20, 20), RIGHT,
                                                                  buff=0.3).shift(UP * 0.35)
            self.play(Create(line), time_span(FadeIn(rname, shift=0.2 * LEFT), 0.8, 1.4),
                      time_span(FadeIn(rform, shift=0.2 * LEFT), 0.8, 1.4), run_time=1.4)

            c.wait_until("count conses exactly")
            self.play(FlashAround(VGroup(n, w1, w2), color=GOLD), FlashAround(nform, color=GOLD),
                      FlashAround(rform, color=GOLD), run_time=1.5)
            c.wait_until("why bother with big o")
            self.play(FlashAround(big_o, color=YELLOW), run_time=1.2)

            c.wait_until("vary")
            ylab2 = T("time", 34).next_to(axes.y_axis, UP, buff=0.15)
            self.play(FadeTransform(ylab, ylab2), run_time=1.0)
            c.wait_until("from one computer")
            curve_b = DashedVMobject(axes.plot(lambda x: 2.5 * x * (x + 1) / 2, x_range=[0, 12.8],
                                               color=RED, stroke_width=4), num_dashes=30)
            line_b = DashedVMobject(axes.plot(lambda x: 2.5 * x, x_range=[0, 20], color=GREEN,
                                              stroke_width=4), num_dashes=30)
            legend = VGroup(
                VGroup(Line(ORIGIN, RIGHT * 0.6, color=DIM, stroke_width=4),
                       T("computer A", 30, color=DIM)).arrange(RIGHT, buff=0.2),
                VGroup(DashedLine(ORIGIN, RIGHT * 0.6, color=DIM, stroke_width=4,
                                  dash_length=0.1),
                       T("computer B", 30, color=DIM)).arrange(RIGHT, buff=0.2),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([(L[0] + R[0]) / 2, -1.75, 0])
            self.play(Create(curve_b), Create(line_b), FadeIn(legend, lag_ratio=0.3),
                      run_time=1.8)

            c.wait_until("big o describes")
            o2 = MathTex("O(n^2)", font_size=44, color=RED).move_to(nform)
            o1 = MathTex("O(n)", font_size=42, color=GREEN).move_to(rform)
            self.play(FadeTransform(nform, o2), FadeTransform(rform, o1), run_time=1.0)
            c.wait_until("wherever you run it")
            self.play(FlashAround(o2, color=YELLOW), FlashAround(o1, color=YELLOW),
                      run_time=max(0.6, min(1.2, c.remaining)))
