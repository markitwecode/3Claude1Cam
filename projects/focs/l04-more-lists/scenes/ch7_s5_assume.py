"""Chapter 7, scene 5: Exercise 4.4, hidden assumptions. Clips c7.assume.1 - c7.assume.6.

PLAN
Opening (as in s2-s7): ch6's strip fades in (4.1-4.3 DONE, 4.4 CURRENT); card 4.4 grows out of
its pill onto a HeroCard: header, the three change headers stacked (greedy / every way / faster,
ch6's labels), on "till" the till/amt column turns YELLOW under one box, the two questions (ch6's
text), pause tag as the voice pauses (on "broken"); the card shrinks back into its pill,
which stays CURRENT until the final fade (as ch7_s2).
Then, under the strip:
- four GREEN assumption chips, one per cue, big in the middle; on "Now let's break them" they shrink into
  one row along the bottom (y CHIP_Y) and three small code cards come in along the top (In [71]
  greedy, In [72] every way, In [73] faster: verbatim thumbnails, legend labels). The card a
  result belongs to lights YELLOW (RED when it crashes). Results live in the band y 1.05..-2.75.
- c7.assume.3: chip 1 RED. Greedy trace of change [5; 0] 3 (each line born from the one above,
  the same call boxed); {stack} the waiting conses flash, the RED Stack overflow line (kept, dimmed,
  through {tail}); {tail} faster: the call with a blinking cursor (no reply), the inner call
  rewritten in place with chg growing, a memory gauge rising to RED; {neg} the same trace with -1,
  the amount 3, 4, 5 rising, the Stack overflow line flashes again.
- c7.assume.4: chip 2 RED. Greedy call with -3, the till chain with the till pointer walking past
  every coin to [], the RED Failure; {empty} `- : int list list = []` under every way + faster.
- c7.assume.5: chip 3 RED. The till chain [1; 2; 5], pointer on the smallest coin; {nine} the call
  and reply, nine GOLD pennies born from the reply's 1s; {allways} two columns of the eight ways
  (descending till / ascending till), matching ways linked TEAL.
- c7.assume.6: chip 4 RED. change [5; 2; 1; 2] 4 and every way's reply; {dup} the three [2; 2]
  YELLOW, [2; 1; 1] linked to [1; 1; 2]; {six} GOLD "6 answers, 3 ways"; {greedyok} greedy's
  [2; 2] with a GREEN check; {close} the results go, the chips (all GREEN) stack up again,
  bracketed "the caller's job"; held, then everything fades (the strip too) to an empty frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch6_s5_hints1 import (CARD_FILL, CARD_TOP, COL_X, CURRENT, DONE, EX44_HEADERS,  # noqa: E402
                                  EX44_LABELS, EX_TASKS, TODO, HeroCard, enter_card,
                                  finish, fit, make_strip, pause_tag)
from scenes.ch4_s3_code import SRC as GREEDY_SRC  # noqa: E402   In [71]
from scenes.ch5_s4_code import SRC as EVERY_SRC  # noqa: E402    In [72]
from scenes.ch6_s2_accs import SRC as FASTER_SRC  # noqa: E402   In [73]
from scenes.ch1_s1_hook import coin  # noqa: E402
from scenes.ch4_s2_idea import till_chain, till_pointer  # noqa: E402

STATES = [DONE, DONE, DONE, CURRENT, TODO, TODO]

# ── card 4.4 (ch6's text and headers) ─────────────────────────────────────────────
_Q = EX_TASKS[3].split("? ", 1)
Q1, Q2 = _Q[0] + "?", _Q[1]
HDR_SIZE = 34
HDR_Y = (1.6, 0.97, 0.34)            # the three change headers (card at the top, before lower())
Q_Y = (-0.55, -1.2)                  # the two questions
CARD_H = CARD_TOP - (Q_Y[1] - 0.5)

# ── the solution board ─────────────────────────────────────────────────────────────
VC_W, VC_H, VC_TOP = 4.15, 1.2, 2.45  # the three code cards along the top
VC_X = (-4.35, 0.0, 4.35)
VC_LABELS = EX44_LABELS               # "greedy", "every way", "faster"
VC_SRCS = (GREEDY_SRC, EVERY_SRC, FASTER_SRC)
# results live in the band y 1.05 .. -2.75, between the code cards and the chips

ASSUME = ("every coin > 0", "amt ≥ 0", "till in descending order", "no coin repeated")
ASSUME_CUES = ("pos", "nonneg", "desc", "norepeat")
CHIP_Y = -3.22                        # the chips' row along the bottom
CHIP_SIZE = 28
BIG = 1.6                             # the chips while they are being stated
BIG_Y = (1.2, 0.2, -0.8, -1.8)
STACK_S = 1.3                         # ... and when they come back on {close}
STACK_Y = (0.55, -0.3, -1.15, -2.0)

TR_SIZE = 38                          # traces
CODE_X, ARR_X = -4.9, -5.48           # trace code left edge, the DIM => column
TR_Y = (0.72, 0.12, -0.48, -1.08, -1.68)
REPLY_X, REPLY_Y = -6.4, -2.32        # the Stack overflow line
STACK = "Stack overflow during evaluation (looping recursion?)."

T_X, T_SIZE = -3.2, 30                # the faster version's panel
T_CALL_Y, T_CUR_Y, T_LINE_Y = 0.72, 0.14, -0.85
G_X, G_W, G_TOP, G_BOT = 5.95, 0.44, 0.5, -1.85

R_X, R_SIZE = -6.0, 30                # calls and replies (clips 4-6)
FAIL = 'Exception: Failure "no more coins!".'
EMPTY = "- : int list list = []"
NINE_TYPE, NINE_LIST = "- : int list =", "[1; 1; 1; 1; 1; 1; 1; 1; 1]"
DESC_SOLS = ("[5; 2; 2]", "[5; 2; 1; 1]", "[5; 1; 1; 1; 1]", "[2; 2; 2; 2; 1]",
             "[2; 2; 2; 1; 1; 1]", "[2; 2; 1; 1; 1; 1; 1]", "[2; 1; 1; 1; 1; 1; 1; 1]",
             "[1; 1; 1; 1; 1; 1; 1; 1; 1]")
ASC_SOLS = ("[1; 1; 1; 1; 1; 1; 1; 1; 1]", "[1; 1; 1; 1; 1; 1; 1; 2]", "[1; 1; 1; 1; 1; 2; 2]",
            "[1; 1; 1; 1; 5]", "[1; 1; 1; 2; 2; 2]", "[1; 1; 2; 5]", "[1; 2; 2; 2; 2]", "[2; 2; 5]")
COL_SIZE, COL_GAP = 26, 0.62          # the two columns of eight ways (a dense listing: 26)
COL_HEAD_Y, COL_Y0, COL_STEP = 0.72, 0.2, 0.37
REP_CALL = "change [5; 2; 1; 2] 4"
REP_TYPE = "- : int list list ="
REP_LIST = "[[2; 2]; [2; 1; 1]; [2; 2]; [1; 1; 1; 1]; [1; 1; 2]; [2; 2]]"   # one line, as the toplevel prints it: 26
GREEDY_REP = "- : int list = [2; 2]"


# ── helpers ────────────────────────────────────────────────────────────────────────
def code_line(src, size, x, y, color=None):
    """A line of code, left edge at x, centred on y."""
    m = Code(src, size=size).move_to([x, y, 0], aligned_edge=LEFT)
    if color is not None:
        m.set_color(color)
    return m


def pieces(src, subs, size, x, y):
    """Lay out a whole line, then return copies of the glyphs of each substring, in place (each an
    independent mobject). A sub may be (text, nth)."""
    full = code_line(src, size, x, y)
    out = []
    for sub in subs:
        s, n = sub if isinstance(sub, tuple) else (sub, 0)
        out.append(VGroup(*[g.copy() for g in full.find(s, nth=n)]))
    return out


def whole(src, size, x, y):
    return pieces(src, [src], size, x, y)[0]


def implies(y):
    return MathTex(r"\Rightarrow", font_size=40, color=DIM).move_to([ARR_X, y, 0])


class Chip(VGroup):
    """An assumption: GREEN text in a GREEN rounded frame (RED while it is being broken)."""

    def __init__(self, text, **kw):
        super().__init__(**kw)
        self.label = T(text, size=CHIP_SIZE, color=GREEN, t2f={"till": MONO, "amt": MONO})
        self.box = RoundedRectangle(corner_radius=0.16, width=self.label.width + 0.48, height=0.5)
        self.box.set_stroke(GREEN, 2.5).set_fill(GREEN, 0.08).move_to(self.label)
        self.add(self.box, self.label)


def paint(chip, color):
    return [chip.box.animate.set_stroke(color).set_fill(color, 0.08), chip.label.animate.set_color(color)]


class VersionCard(VGroup):
    """One change function as a small card: its code (verbatim, a thumbnail) and a legend label."""

    def __init__(self, label, src, k, x, **kw):
        super().__init__(**kw)
        self.frame = RoundedRectangle(corner_radius=0.16, width=VC_W, height=VC_H)
        self.frame.set_stroke(DIM, 2).set_fill(CARD_FILL, 1).move_to([x, VC_TOP - VC_H / 2, 0])
        self.code = Code(src, size=20).scale(k)
        self.code.move_to([x, VC_TOP - VC_H / 2 - 0.08, 0])
        self.label = T(label, size=30, color=FG)
        self.label.move_to([self.frame.get_left()[0] + 0.3, VC_TOP, 0], aligned_edge=LEFT)
        self.patch = Rectangle(width=self.label.width + 0.24, height=0.14)
        self.patch.set_stroke(width=0).set_fill(BG, 1).move_to(self.label)
        self.add(self.frame, self.code, self.patch, self.label)


def version_cards():
    raw = [Code(s, size=20) for s in VC_SRCS]
    k = min(min((VC_W - 0.4) / r.width, (VC_H - 0.45) / r.height) for r in raw)
    return [VersionCard(lab, src, k, x) for lab, src, x in zip(VC_LABELS, VC_SRCS, VC_X)]


def light(card, color=None):
    """A card's state: None (resting), YELLOW (its result is on screen), RED (it crashed)."""
    if color is None:
        return [card.frame.animate.set_stroke(DIM, 2), card.label.animate.set_color(FG)]
    return [card.frame.animate.set_stroke(color, 3.5), card.label.animate.set_color(color)]


def make_gauge():
    outline = RoundedRectangle(corner_radius=0.08, width=G_W, height=G_TOP - G_BOT)
    outline.set_stroke(DIM, 2.5).move_to([G_X, (G_TOP + G_BOT) / 2, 0])
    level = ValueTracker(0.04)
    inner = G_TOP - G_BOT - 0.1

    def bar():
        v = level.get_value()
        h = max(0.02, v * inner)
        col = interpolate_color(ManimColor(GOLD), ManimColor(RED), min(1.0, max(0.0, (v - 0.55) / 0.4)))
        r = Rectangle(width=G_W - 0.14, height=h).set_stroke(width=0).set_fill(col, 0.9)
        return r.move_to([G_X, G_BOT + 0.05 + h / 2, 0])

    fill = always_redraw(bar)
    label = T("memory", size=28, color=DIM).next_to(outline, UP, buff=0.16)
    return outline, fill, level, label


def blinker(cursor):
    cursor.clock = 0.0

    def tick(m, dt):
        m.clock += dt
        m.set_fill(opacity=1.0 if (m.clock % 1.0) < 0.6 else 0.0)

    cursor.add_updater(tick)




class HiddenAssumptions(NarratedScene):
    def construct(self):
        self.strip = make_strip(STATES)
        self.play(FadeIn(self.strip, lag_ratio=0.1), run_time=0.8)
        self.card44()
        self.four()
        self.zero_coin()
        self.negative_amount()
        self.ascending()
        self.repeated()
        self.wait(3.6)          # the closing board: the four assumptions, the caller's job
        finish(self)

    # ── c7.assume.1: card 4.4 ─────────────────────────────────────────────────────────
    def card44(self):
        card = HeroCard(3, CARD_H)
        names = [T(lab, size=30, color=DIM) for lab in EX44_LABELS]
        hdr_x = COL_X + max(n.width for n in names) + 0.4
        rows = []
        for name, src, y in zip(names, EX44_HEADERS, HDR_Y):
            code = Code(src, size=HDR_SIZE).move_to([hdr_x, y, 0], aligned_edge=LEFT)
            name.next_to(code, LEFT, buff=0.4).align_to(code.find("let"), DOWN)
            rows.append(VGroup(name, code).set_z_index(1))     # above the till/amt box
        q1 = T(Q1, size=32, t2c={"till": YELLOW, "amt": YELLOW}, t2f={"till": MONO, "amt": MONO})
        q2 = T(Q2, size=32)
        for q, y in zip((q1, q2), Q_Y):
            q.move_to([COL_X, y, 0], aligned_edge=LEFT)
        cols = [(r[1].find("till"), r[1].find("amt")) for r in rows]
        box = SurroundingRectangle(VGroup(*[g for t, a in cols for g in (*t, *a)]),
                                   color=YELLOW, buff=0.14, corner_radius=0.1)
        box.set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.12)
        card.lower(*rows, q1, q2, box)
        card.keep(*rows, box, q1, q2)

        with self.say("c7.assume.1") as c:
            self.play(*enter_card(self.strip, card, light=False), run_time=fit(c, "What do", hi=1.4))
            c.wait_until("What do")
            self.play(FadeIn(q1, shift=0.2 * DOWN),
                      time_span(LaggedStart(*[FadeIn(r, shift=0.25 * RIGHT) for r in rows],
                                            lag_ratio=0.3), 0.6, 2.2),
                      run_time=2.2)
            c.wait_until("till")
            anims = [a for t, m in cols for a in (*recolor(t, YELLOW), *recolor(m, YELLOW))]
            self.play(*anims, FadeIn(box), run_time=1.0)
            c.wait_until("happen")
            self.play(FadeIn(q2, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("broken")
            ptag = pause_tag()
            self.play(FadeIn(ptag, shift=0.2 * DOWN), run_time=1.2)
        self.card, self.ptag = card, ptag

    # ── c7.assume.2: four assumptions ─────────────────────────────────────────────────
    def four(self):
        chips = [Chip(t) for t in ASSUME]
        VGroup(*chips).arrange(RIGHT, buff=0.15).move_to([0, CHIP_Y, 0])
        bigs = [ch.copy().scale(BIG) for ch in chips]
        left = -max(b.width for b in bigs) / 2
        for b, y in zip(bigs, BIG_Y):
            b.move_to([left, y, 0], aligned_edge=LEFT)
        self.chips = chips
        self.cards = version_cards()

        with self.say("c7.assume.2") as c:
            c.wait_until("four assumptions")
            # as ch7_s2: the card shrinks back into its pill, which stays CURRENT for the solution
            self.play(*[FadeOut(m) for m in (*self.card.shown, self.ptag)],
                      Transform(self.card.frame, self.strip[3].frame.copy()), run_time=1.0)
            self.remove(self.card.frame)
            for b, cue, nxt in zip(bigs, ASSUME_CUES, (*ASSUME_CUES[1:], "Now")):
                c.wait_until(cue)
                self.play(FadeIn(b, shift=0.25 * DOWN), run_time=fit(c, nxt, lo=0.7, hi=1.0))
            c.wait_until("Now")
            self.play(LaggedStart(*[ReplacementTransform(b, s) for b, s in zip(bigs, chips)],
                                  lag_ratio=0.08, run_time=1.5),
                      time_span(LaggedStart(*[FadeIn(v, shift=0.2 * DOWN) for v in self.cards],
                                            lag_ratio=0.2), 0.6, 2.0),
                      run_time=2.0)

    # ── c7.assume.3: a coin worth zero (and a negative coin) ────────────────────────────
    def trace(self, srcs):
        """The pieces of a greedy trace: line 0, line 1, (cons, call) for lines 2 and 3, dots, =>s."""
        l0 = whole(srcs[0], TR_SIZE, CODE_X, TR_Y[0])
        l1 = whole(srcs[1], TR_SIZE, CODE_X, TR_Y[1])
        out = [l0, l1]
        for k in (2, 3):
            cons, rest = srcs[k].rsplit(" change", 1)
            out += pieces(srcs[k], [cons, "change" + rest], TR_SIZE, CODE_X, TR_Y[k])
        dots = T("…", size=44).move_to([CODE_X, TR_Y[4], 0], aligned_edge=LEFT)
        arrows = [implies(y) for y in TR_Y[1:]]
        return (*out, dots, arrows)

    def zero_coin(self):
        g, e, f = self.cards
        chip = self.chips[0]
        l0, l1, cons2, call2, cons3, call3, dots, arr = self.trace(
            ["change [5; 0] 3", "change [0] 3", "0 :: change [0] 3", "0 :: 0 :: change [0] 3"])
        reply = code_line(STACK, 28, REPLY_X, REPLY_Y, color=RED)

        with self.say("c7.assume.3") as c:
            # {zero}
            self.play(*paint(chip, RED), FlashAround(chip, color=RED, time_width=1.5), *light(g, YELLOW),
                      time_span(FadeIn(l0, shift=0.2 * DOWN), 0.4, 1.3), run_time=1.3)
            c.wait_until("Using it")
            self.play(TransformFromCopy(l0, l1), FadeIn(arr[0]), run_time=fit(c, "nothing", lo=0.9, hi=1.3))
            c.wait_until("nothing")
            self.play(TransformFromCopy(l1, call2), FadeIn(cons2, arr[1], shift=0.2 * RIGHT),
                      run_time=fit(c, "reached", lo=0.8, hi=1.1))
            c.wait_until("reached")
            self.play(TransformFromCopy(cons2, cons3), TransformFromCopy(call2, call3), FadeIn(arr[2]),
                      time_span(FadeIn(dots, arr[3]), 0.6, 1.1), run_time=1.1)
            c.wait_until("same call")
            boxes = [token_box(m, m, color=YELLOW).set_z_index(-1) for m in (l1, call2, call3)]
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.25), run_time=1.0)
            # {stack}: greedy and every way leave work waiting
            c.wait_until("stack")
            self.play(*light(e, YELLOW), run_time=0.8)
            c.wait_until("waiting")
            self.play(LaggedStart(FlashUnder(cons2, color=YELLOW), FlashUnder(cons3, color=YELLOW),
                                  lag_ratio=0.3), run_time=1.2)
            c.wait_until("out of stack")
            self.play(FadeIn(reply, shift=0.2 * DOWN), *light(g, RED), *light(e, RED), run_time=0.8)
            # {tail}: the faster version runs on
            c.wait_until("tail")
            trace = [l0, l1, cons2, call2, cons3, call3, dots, *arr, *boxes]
            call = code_line("change [5; 0] 3 [] []", T_SIZE, T_X, T_CALL_Y)
            cursor = Rectangle(width=0.16, height=0.34).set_stroke(width=0).set_fill(FG, 1)
            cursor.move_to([T_X + 0.08, T_CUR_Y, 0])
            outline, fill, level, mem = make_gauge()
            self.play(*[FadeOut(m) for m in trace], reply.animate.set_opacity(0.35),
                      *light(g), *light(e), *light(f, YELLOW),
                      time_span(FadeIn(call, cursor, outline, fill, mem, shift=0.2 * DOWN), 0.5, 1.4),
                      run_time=1.4)
            blinker(cursor)
            steps = ["[]", "[0]", "[0; 0]", "[0; 0; 0]", "[0; 0; 0; 0]", "[0; 0; 0; 0; 0]"]
            lines = [pieces(f"change [0] 3 {chg} []", ["change [0] 3", chg, ("[]", 1 if chg == "[]" else 0)],
                            T_SIZE, T_X, T_LINE_Y) for chg in steps]
            pre, chg, tl = lines[0]
            c.wait_until("last thing")
            self.play(TransformFromCopy(call, pre), TransformFromCopy(call.find("[]"), chg),
                      TransformFromCopy(call.find("[]", nth=1), tl), run_time=fit(c, "runs on", lo=0.9, hi=1.3))
            c.wait_until("runs on")
            levels = (0.18, 0.32, 0.47, 0.62, 0.76)
            for k in range(1, len(steps)):
                if k == 3:
                    c.wait_until("growing")
                _, nchg, ntl = lines[k]
                self.play(ReplacementTransform(chg, nchg), ReplacementTransform(tl, ntl),
                          level.animate.set_value(levels[k - 1]),
                          run_time=(0.9, 0.7, 0.7, 0.55, 0.55)[k - 1], rate_func=linear)
                chg, tl = nchg, ntl
            c.wait_until("memory")
            self.play(level.animate(rate_func=linear).set_value(1.0),
                      time_span(outline.animate.set_stroke(RED, 3.5), 0.5, 1.2),
                      time_span(FlashAround(outline, color=RED, time_width=1.5), 0.5, 1.2), run_time=1.2)
            # {neg}: a negative coin
            c.wait_until("neg")
            n0, n1, ncons2, ncall2, ncons3, ncall3, ndots, narr = self.trace(
                ["change [5; -1] 3", "change [-1] 3", "-1 :: change [-1] 4", "-1 :: -1 :: change [-1] 5"])
            cursor.clear_updaters()
            cursor.set_fill(opacity=1.0)
            fill.clear_updaters()
            panel = [call, cursor, pre, chg, tl, outline, fill, mem]
            self.play(*[FadeOut(m) for m in panel], *light(f), *light(g, YELLOW), *light(e, YELLOW),
                      time_span(FadeIn(n0, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            self.remove(level)
            c.wait_until("no better")
            self.play(TransformFromCopy(n0, n1), FadeIn(narr[0]), run_time=fit(c, "Each use", lo=0.6, hi=0.9))
            c.wait_until("Each use")
            self.play(TransformFromCopy(n1, ncall2), FadeIn(ncons2, narr[1], shift=0.2 * RIGHT),
                      time_span(FlashAround(ncall2[-1], color=GOLD, time_width=1.5), 0.3, 0.9), run_time=0.9)
            c.wait_until("bigger")
            self.play(TransformFromCopy(ncons2, ncons3), TransformFromCopy(ncall2, ncall3), FadeIn(narr[2]),
                      time_span(FlashAround(ncall3[-1], color=GOLD, time_width=1.5), 0.3, 0.9),
                      time_span(FadeIn(ndots, narr[3]), 0.5, 0.9), run_time=0.9)
            c.wait_until("never reaches")
            self.play(reply.animate.set_opacity(1.0), FlashAround(reply, color=RED, time_width=1.5),
                      *light(g, RED), *light(e, RED), run_time=1.0)
        self.board = [n0, n1, ncons2, ncall2, ncons3, ncall3, ndots, *narr, reply]

    # ── c7.assume.4: a negative amount ────────────────────────────────────────────────
    def negative_amount(self):
        g, e, f = self.cards
        c1, c2 = self.chips[0], self.chips[1]
        call = code_line("change [50; 20; 10; 5; 2; 1] (-3)", R_SIZE, R_X, 0.72)
        chain = till_chain([50, 20, 10, 5, 2, 1], scale=0.72).move_to([0, -0.85, 0])
        ptr = till_pointer(chain.cells[0], length=0.35)
        fail = code_line(FAIL, R_SIZE, R_X, -1.85, color=RED)
        empty = Code(EMPTY, size=R_SIZE).move_to([2.2, -2.45, 0])

        with self.say("c7.assume.4") as c:
            self.play(*paint(c1, GREEN), *paint(c2, RED), FlashAround(c2, color=RED, time_width=1.5),
                      *light(e), *light(g, YELLOW), run_time=1.0)
            c.wait_until("negative amount")
            self.play(*[FadeOut(m) for m in self.board],
                      time_span(FadeIn(call, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            c.wait_until("Every coin")
            self.play(FadeIn(chain, lag_ratio=0.1), FadeIn(ptr, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("skips")
            xs = [cell.box.get_x() for cell in chain.cells] + [chain.nil.get_x()]
            for k in range(6):
                self.play(ptr.animate.shift(RIGHT * (xs[k + 1] - xs[k])),
                          restyle(chain.cells[k], op=0.3), run_time=0.6 if k == 0 else 0.32)
            c.wait_until("raises")
            self.play(chain.nil.animate.set_color(RED), FlashAround(chain.nil, color=RED, time_width=1.5),
                      FadeIn(fail, shift=0.2 * DOWN), *light(g, RED), run_time=1.1)
            c.wait_until("empty")
            self.play(*light(g), *light(e, YELLOW), *light(f, YELLOW), FadeIn(empty, shift=0.2 * DOWN),
                      run_time=1.0)
        self.board = [call, chain, ptr, fail, empty]

    # ── c7.assume.5: a till in increasing order ────────────────────────────────────────
    def ascending(self):
        g, e, f = self.cards
        c2, c3 = self.chips[1], self.chips[2]
        chain = till_chain([1, 2, 5]).move_to([0, -0.75, 0])
        ptr = till_pointer(chain.cells[0])
        call = code_line("change [1; 2; 5] 9", R_SIZE, R_X, 0.72)
        rtype, rlist = pieces(f"{NINE_TYPE} {NINE_LIST}", [NINE_TYPE, NINE_LIST], R_SIZE, R_X, 0.1)
        ones = [rlist[i] for i in range(1, len(rlist), 2)]          # [ 1 ; 1 ; ... 1 ]
        row = VGroup(*[coin(1, r=0.3) for _ in ones]).arrange(RIGHT, buff=0.14)
        row.move_to([rlist.get_x(), -0.95, 0])
        pennies = list(row)

        heads, cols = [], []
        for k, (till, sols) in enumerate((("[5; 2; 1]", DESC_SOLS), ("[1; 2; 5]", ASC_SOLS))):
            rows = [Code(s, size=COL_SIZE) for s in sols]
            for i, r in enumerate(rows):
                y = COL_Y0 - COL_STEP * i
                if k == 0:
                    r.move_to([-COL_GAP, y, 0], aligned_edge=RIGHT)
                else:
                    r.move_to([COL_GAP, y, 0], aligned_edge=LEFT)
            widest = max(rows, key=lambda r: r.width)
            heads.append(Code(f"change {till} 9", size=R_SIZE).move_to([widest.get_x(), COL_HEAD_Y, 0]))
            cols.append(rows)
        key = [tuple(sorted(s)) for s in ASC_SOLS]
        links = []
        for i, s in enumerate(DESC_SOLS):
            j = key.index(tuple(sorted(s)))
            a, b = cols[0][i].get_right() + RIGHT * 0.08, cols[1][j].get_left() + LEFT * 0.08
            links.append(Line(a, b).set_stroke(TEAL, 2.5, opacity=0.85))

        with self.say("c7.assume.5") as c:
            self.play(*paint(c2, GREEN), *paint(c3, RED), FlashAround(c3, color=RED, time_width=1.5),
                      *light(e), *light(f), run_time=1.0)
            c.wait_until("increasing")
            self.play(*[FadeOut(m) for m in self.board],
                      time_span(FadeIn(chain, lag_ratio=0.15), 0.4, 1.3), run_time=1.3)
            c.wait_until("Greedy still")
            self.play(*light(g, YELLOW), FadeIn(ptr, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("smallest")
            self.play(FlashAround(chain.cells[0].label, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("nine")
            self.play(FadeOut(chain), FadeOut(ptr), time_span(FadeIn(call, shift=0.2 * DOWN), 0.4, 1.1),
                      time_span(FadeIn(rtype, rlist, shift=0.2 * DOWN), 0.8, 1.5), run_time=1.5)
            c.wait_until("hands back")
            self.play(LaggedStart(*[TransformFromCopy(o, p) for o, p in zip(ones, pennies)], lag_ratio=0.08),
                      run_time=1.4)
            c.wait_until("allways")
            # greedy's call is the right-hand heading; its answer is the first way on the right
            self.play(ReplacementTransform(call, heads[1]), ReplacementTransform(rlist, cols[1][0]),
                      FadeOut(rtype), *[FadeOut(p) for p in pennies], *light(g), *light(e, YELLOW),
                      *light(f, YELLOW), time_span(FadeIn(heads[0], shift=0.2 * DOWN), 0.4, 1.1), run_time=1.1)
            rest = [r for pair in zip(cols[0], [None, *cols[1][1:]]) for r in pair if r is not None]
            self.play(LaggedStart(*[FadeIn(r, shift=0.15 * DOWN) for r in rest], lag_ratio=0.06), run_time=1.2)
            self.play(LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.1), run_time=1.0)
        self.board = [*heads, *cols[0], *cols[1], *links]

    # ── c7.assume.6: a repeated coin; the caller's job ─────────────────────────────────
    def repeated(self):
        g, e, f = self.cards
        c3, c4 = self.chips[2], self.chips[3]
        rlist = Code(REP_LIST, size=26).move_to([0, -0.45, 0])
        x0 = rlist.get_left()[0]
        call = code_line(REP_CALL, R_SIZE, x0, 0.72)
        rtype = code_line(REP_TYPE, 26, x0, 0.12)
        twos = [rlist.find("[2; 2]", nth=n) for n in range(3)]
        a, b = rlist.find("[2; 1; 1]"), rlist.find("[1; 1; 2]")
        arc = ArcBetweenPoints(a.get_bottom() + DOWN * 0.12, b.get_bottom() + DOWN * 0.12, angle=PI / 5)
        arc.set_stroke(TEAL, 3)
        six = T("6 answers, 3 ways", size=40, color=GOLD).move_to([0, -1.68, 0])
        grep = code_line(GREEDY_REP, R_SIZE, x0, -2.38)
        tick = check_mark(GREEN).next_to(grep, RIGHT, buff=0.4)

        with self.say("c7.assume.6") as c:
            self.play(*paint(c3, GREEN), *paint(c4, RED), FlashAround(c4, color=RED, time_width=1.5),
                      run_time=1.1)
            c.wait_until("Make four")
            self.play(*[FadeOut(m) for m in self.board], *light(f),
                      time_span(FadeIn(call, shift=0.2 * DOWN), 0.5, 1.3), run_time=1.3)
            c.wait_until("two again")
            self.play(FlashAround(call.find("2", nth=1), color=YELLOW, time_width=1.5),
                      time_span(FadeIn(rtype, rlist, shift=0.2 * DOWN), 0.3, 1.2), run_time=1.2)
            c.wait_until("dup")
            self.play(*[an for t in twos for an in recolor(t, YELLOW)],
                      LaggedStart(*[FlashUnder(t, color=YELLOW) for t in twos], lag_ratio=0.25), run_time=1.3)
            c.wait_until("turns up again")
            self.play(*recolor(a, TEAL), *recolor(b, TEAL), Create(arc), run_time=1.3)
            c.wait_until("six")
            self.play(FadeIn(six, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("greedyok")
            self.play(*light(e), *light(g, YELLOW), FadeIn(grep, shift=0.2 * DOWN),
                      time_span(FadeIn(tick, scale=0.6), 0.4, 0.9), run_time=0.9)
            c.wait_until("close")
            board = [call, rtype, rlist, arc, six, grep, tick]
            left = -5.55
            for ch, y in zip(self.chips, STACK_Y):
                ch.generate_target()
                ch.target.scale(STACK_S).move_to([left, y, 0], aligned_edge=LEFT)
            c4.target.box.set_stroke(GREEN).set_fill(GREEN, 0.08)
            c4.target.label.set_color(GREEN)
            self.play(*[FadeOut(m) for m in board], *light(g),
                      time_span(LaggedStart(*[MoveToTarget(ch) for ch in self.chips], lag_ratio=0.08), 0.4, 1.7),
                      run_time=1.7)
            brace = Brace(VGroup(*self.chips), direction=RIGHT, buff=0.3, color=FG)
            job = T("the caller's job", size=40, color=YELLOW).next_to(brace, RIGHT, buff=0.3)
            c.wait_until("caller")
            self.play(GrowFromCenter(brace), FadeIn(job, shift=0.25 * LEFT), run_time=1.0)
