"""STATUS (done): all 8 clips; vk check clean (137.1 s vs 129.6 s narration; c6.sum.6 has gap=2.4
so the finished addsum/sum code can be read). Remaining dwell notes are accepted: the opening
row (continuity from s1's last shot; held 0.9 s). Others are within 1.5 s of their need.
(fix pass 2) clip 7 is a stacked trace: calls made dim to 0.4, the total box leaves each
old total dimmed over its cell, and on "each call replaces" the history folds into `=> 17`;
addsum/sum and their replies (dimmed 0.5) stay in a top band at 28 through clip 7.

Chapter 6, scene 2: Exercise 3.1 solved. nsum grows out of nlength (same shape), its
type, its trace with the waiting additions stacked as GOLD plates in a "pending additions"
column, O(n) time and space, the stack overflowing, the common slip (x + addsum total xs)
that brings the stack back; then the accumulator addsum / sum, its flat trace with the
total riding the chain, and the time / space table. Clips c6.sum.1 - c6.sum.8.

Opens on s1's five-card row (ch5_s6's overview, BigCards at UP * 0.7); card 3.1 grows into
the kit's hero card; the kit's pause tag on {stop}.

The pending column (s4 reuses it): plates PW x PH = 2.0 x 0.7, stroke GOLD 3, fill PLATE_FILL,
Mono 36 GOLD text, centred at x = CX = 4.9, stacked up from a GOLD floor line at y = FLOOR =
-1.0 (2.5 wide, stroke 3); label T("pending additions", 30, GOLD) centred 0.42 under the floor.
Waiting additions in the trace: their `+` GOLD and a GOLD underline (ch3_s3's style, 5 px,
0.13 under the baseline); plates are born from them (TransformFromCopy) and pop back into the
expression on the unwind.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import BigCard, HeroCard, at_row, pause_tag  # noqa: E402  (read-only kit)

# ── code and replies (verified with ocaml 5.4.1) ─────────────────────────────────
NLENGTH = "let rec nlength = function\n  | [] -> 0\n  | x :: xs -> 1 + nlength xs"
NLEN_X = NLENGTH.replace("1 + nlength", "x + nlength")
NSUM = "let rec nsum = function\n  | [] -> 0\n  | x :: xs -> x + nsum xs"
WRONG = "let rec addsum total = function\n  | [] -> total\n  | x :: xs -> x + addsum total xs"
ADDSUM = "let rec addsum total = function\n  | [] -> total\n  | x :: xs -> addsum (total + x) xs"
SUMDEF = "let sum xs = addsum 0 xs"
R_NSUM = "val nsum : int list -> int = <fun>"
R_NLEN = "val nlength : 'a list -> int = <fun>"
R_ADDSUM = "val addsum : int -> int list -> int = <fun>"
R_SUM = "val sum : int list -> int = <fun>"
R_17 = "- : int = 17"

ROWS = ["nsum [3; 5; 9]", "3 + nsum [5; 9]", "3 + (5 + nsum [9])",
        "3 + (5 + (9 + nsum []))", "3 + (5 + (9 + 0))"]
UNWIND = ["3 + (5 + 9)", "3 + 14", "17"]
FLAT = ["addsum 0 [3; 5; 9]", "addsum 3 [5; 9]", "addsum 8 [9]", "addsum 17 []", "17"]
TOTALS = [0, 3, 8, 17]
WAITS = ("3 +", "5 +", "9 +")

# ── layout ─────────────────────────────────────────────────────────────────────
HERO = 44                                  # nsum while it is being built (clips 2-3)
HERO_UL = np.array([-5.5, 1.8, 0])
SMALL = 32                                 # nsum parked top left (clips 4-5)
SMALL_UL = np.array([-6.3, 3.55, 0])
TR = 40                                    # nsum's trace rows
X0 = -5.5                                  # left edge of the trace rows' code
BASE = [1.0, 0.2, -0.6, -1.4, -2.2]        # their baselines
REPLY_BASE = -3.0
TAG_Y = 1.2                                # cost tags under the parked nsum
WRONG_UL = np.array([-6.3, 0.45, 0])
SHRINK = 0.875                             # nsum block, dimmed, in the iterative half
# the pending-additions column (shared look with ch6 s4)
CX, PW, PH, FLOOR = 4.9, 2.0, 0.7, -1.0
PLATE_FILL = "#1E222A"
# the flat trace
TOP_UL = np.array([-6.3, 3.6, 0])           # addsum, sum and their replies, at 28
REPLY_DIM = 0.5
TS = 32                                    # the stacked trace (bottom left)
TX = -5.7
TB0, TP = -0.15, 0.53                      # its first baseline and pitch (a gap under the code)
HIST = 0.4                                 # calls already made
S_CHAIN = 0.8                              # the chain (bottom right)
CHAIN_C = np.array([3.55, -1.7, 0])
DIM_TO = 0.25


# ── helpers (local) ──────────────────────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph, or as fresh VGroups used only as transform
# targets that are removed again right after (wrapping on-screen glyphs pulls them out).
_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


def baseline(m):
    """y of the text baseline of a Code / Mono / T object."""
    src, glyphs = (m.src, m.text) if isinstance(m, Code) else (m.text, m)
    chars_ = [ch for ch in src if not ch.isspace()]
    for ch, g in zip(chars_, glyphs):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return m.get_bottom()[1]


def put(m, left, base):
    """Move a text object so its left edge is at x=left and its baseline at y=base."""
    m.shift(RIGHT * (left - m.get_left()[0]) + UP * (base - baseline(m)))
    return m


def gold_total(code):
    """The running total in GOLD wherever it appears."""
    for k in range(code.src.count("total")):
        code.find("total", nth=k).set_color(GOLD)
    return code


def implies():
    return MathTex(r"\Rightarrow", font_size=64, color=DIM)


def under(glyphs, base, color=GOLD):
    """The underline of one waiting addition (ch3_s3's pending style)."""
    y = base - 0.13
    return Line([glyphs.get_left()[0], y, 0], [glyphs.get_right()[0], y, 0], color=color, stroke_width=5)


def plate(text, k):
    """One pending addition as a plate on the stack (k = 0 is the bottom one)."""
    r = Rectangle(width=PW, height=PH).set_stroke(GOLD, 3).set_fill(PLATE_FILL, 1)
    r.move_to([CX, FLOOR + PH * (k + 0.5), 0])
    if text is None:
        return VGroup(r)
    # z 1: TransformFromCopy targets are added before FadeIn ones, so keep the text on top
    return VGroup(r, Mono(text, size=36, color=GOLD).move_to(r).set_z_index(1))


def rack():
    floor = Line([CX - PW / 2 - 0.25, FLOOR, 0], [CX + PW / 2 + 0.25, FLOOR, 0]).set_stroke(GOLD, 3)
    label = T("pending additions", size=30, color=GOLD).move_to([CX, FLOOR - 0.42, 0])
    return floor, label


def cost_tag(word, big, wsize=34, osize=48):
    w = T(word, size=wsize, color=GOLD)
    o = MathTex(big, font_size=osize, color=GOLD)
    g = VGroup(w, o).arrange(RIGHT, buff=0.2)
    w.shift(UP * (o[0][0].get_bottom()[1] - baseline(w)))
    return g


def count_frame():
    return RoundedRectangle(width=1.0, height=0.82, corner_radius=0.12).set_stroke(GOLD, 3).set_fill(BG, 1)


class SumAList(NarratedScene):
    def construct(self):
        self.card_beat()       # c6.sum.1
        self.build_nsum()      # c6.sum.2
        self.its_type()        # c6.sum.3
        self.trace_nsum()      # c6.sum.4
        self.cost_and_slip()   # c6.sum.5
        self.accumulator()     # c6.sum.6
        self.flat_trace()      # c6.sum.7
        self.compare()         # c6.sum.8
        self.wait(0.6)     # the table's last word, O(1), gets its reading time
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── sum.1: the row of five cards; 3.1 grows into the hero card; pause ─────────
    def card_beat(self):
        bigs = VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * 0.7)
        card = HeroCard(0, height=3.2)
        lines = [T("Sum a list's elements.", size=36),
                 T("Recursive first, then iterative.", size=36),
                 T("Comment on the improvement in efficiency.", size=36, t2c={"efficiency": GOLD})]
        for k, m in enumerate(lines, start=1):
            at_row(m, k)
        card.lower(*lines)
        tag = pause_tag()

        # s1 ends on this row alone: fade the same row back in
        self.play(LaggedStart(*[FadeIn(b) for b in bigs], lag_ratio=0.1), run_time=0.8)
        self.wait(0.9)     # settle and hold, as s3-s6 do
        with self.say("c6.sum.1") as c:
            # "Exercise three point one."  The card grows out of its small card.
            big = bigs[0]
            self.play(TransformFromCopy(big.frame, card.frame), FadeTransform(big.num.copy(), card.header),
                      *[FadeOut(b) for b in bigs], run_time=1.5)
            # "Code a recursive function to sum the elements of a list, then an iterative
            # version, and comment on the improvement in efficiency."
            c.wait_until("code a recursive")
            self.play(FadeIn(lines[0], shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("then an iterative")
            self.play(FadeIn(lines[1], shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("comment on")
            self.play(FadeIn(lines[2], shift=0.25 * DOWN), run_time=1.0)
            # "Pause here if you want to try it."  Then still.
            c.wait_until("stop")
            self.play(FadeIn(tag, shift=0.2 * DOWN), run_time=1.0)

    # ── sum.2: nlength's shape becomes nsum ───────────────────────────────────────
    def build_nsum(self):
        nl = Code(NLENGTH, size=HERO).move_to(HERO_UL, aligned_edge=UL).set_opacity(0.4)
        nlx = Code(NLEN_X, size=HERO).move_to(HERO_UL, aligned_edge=UL)
        code = Code(NSUM, size=HERO).move_to(HERO_UL, aligned_edge=UL)

        with self.say("c6.sum.2") as c:
            # "The recursive version has the same shape as en-length."  (the lecture's, dimmed)
            c.wait_until("same shape")
            sweep_clear(self, time_span(FadeIn(nl, shift=0.2 * DOWN), 0.5, 1.4), run_time=1.4)
            # "The sum of nil is zero."  The first clause is the same: it lights up.
            c.wait_until("the sum of nil")
            self.play(*[g.animate.set_opacity(1) for g in nl.line(1)], run_time=1.0)
            # "And the sum of a head, ex, consed onto exes, ..."
            c.wait_until("step")
            self.play(*[g.animate.set_opacity(1) for g in nl.line(2)], run_time=1.0)
            # "... is ex plus the sum of exes."  The 1 gives way to the head x.
            c.wait_until("is ex plus")
            new_x = VGroup(nlx.find("x +", line=2)[0])
            self.play(FadeOut(nl.find("1", line=2), shift=0.3 * UP),
                      TransformFromCopy(nl.find("x", line=2), new_x, path_arc=-0.9), run_time=1.5)
            self.remove(*nl.get_family(), new_x)
            for g in nlx.line(0):
                g.set_opacity(0.4)
            self.add(nlx)
            # "As in the lecture, we'll call it en-sum, ..."
            c.wait_until("name")
            pairs = [(nlx.find("let rec"), code.find("let rec")),
                     (nlx.find("nlength", line=0), code.find("nsum", line=0)),
                     (nlx.find("= function"), code.find("= function")),
                     (nlx.line(1), code.line(1)),
                     (nlx.find("| x :: xs -> x +", line=2), code.find("| x :: xs -> x +", line=2)),
                     (nlx.find("nlength", line=2), code.find("nsum", line=2)),
                     (nlx.find("xs", line=2, nth=1), code.find("xs", line=2, nth=1))]
            self.play(*[ReplacementTransform(a, b) for a, b in pairs], run_time=1.5)
            self.remove(*nlx.get_family(), *[b for _, b in pairs])
            self.add(code)
            # "... en for naive."
            c.wait_until("en for naive")
            self.play(FlashAround(code.find("n", line=0), color=YELLOW, time_width=1.5), run_time=1.0)
        self.code = code

    # ── sum.3: its type, against nlength's ────────────────────────────────────────
    def its_type(self):
        code = self.code
        r1 = put(Code(R_NSUM, size=36), HERO_UL[0], code.get_bottom()[1] - 0.8)
        r2 = put(Code(R_NLEN, size=36), HERO_UL[0], baseline(r1) - 0.85)
        r2.shift(RIGHT * (r1.find(":").get_x() - r2.find(":").get_x()))   # types line up
        r2.set_opacity(0.45)

        with self.say("c6.sum.3") as c:
            # "Its type is int list to int."
            self.play(FadeIn(r1, shift=0.25 * DOWN), run_time=1.0)
            # "Unlike length, it isn't polymorphic, ..."  PINK 'a against GREEN int
            c.wait_until("notpoly")
            self.play(FadeIn(r2, shift=0.25 * DOWN),
                      time_span(FlashAround(r2.find("'a"), color=PINK, time_width=1.5), 0.5, 1.5),
                      run_time=1.5)
            # "... because plus only works on integers."
            c.wait_until("plus only")
            self.play(FlashAround(code.find("+"), color=YELLOW, time_width=1.5),
                      FlashAround(r1.find("int"), color=GREEN, time_width=1.5), run_time=1.2)
        self.types = (r1, r2)

    # ── sum.4: the staircase, the pending column, the unwind ──────────────────────
    def birth(self, src, dst, copies, news, fades, arrow, run_time, extra=()):
        """Row dst is born from row src (P11/P13): shared parts copied down, the new head and
        `+` flown in from where they come from, brackets faded in."""
        anims, targets = [], []
        for s, t in copies:
            anims.append(TransformFromCopy(s, t))
            targets.append(t)
        for s, t in news:
            anims.append(TransformFromCopy(s, t, path_arc=-0.6))
            targets.append(t)
        for t in fades:
            anims.append(FadeIn(t, shift=0.2 * DOWN))
            targets.append(t)
        anims.append(FadeIn(arrow, shift=0.2 * DOWN))
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*targets)
        self.add(dst)

    def trace_nsum(self):
        code = self.code
        rows = [put(Code(s, size=TR), X0, b) for s, b in zip(ROWS, BASE)]
        arrows = [None] + [implies().next_to(r, LEFT, buff=0.3).set_y(b + 0.13)
                           for r, b in zip(rows[1:], BASE[1:])]
        u = [put(Code(s, size=TR), X0, BASE[4]) for s in UNWIND]
        for r in (rows[4], u[0], u[1]):          # additions still waiting there: GOLD +
            for g in chars(r, "+"):
                g.set_color(GOLD)
        r0, r1, r2, r3, r4 = rows
        plus = code.find("+")
        plates = [plate(s, k) for k, s in enumerate(WAITS)]
        floor, label = rack()
        under3 = [under(r3.find(s), BASE[3]) for s in WAITS]
        under4 = [under(r4.find(s), BASE[4]) for s in WAITS]
        reply = put(Code(R_17, size=36), X0, REPLY_BASE)

        with self.say("c6.sum.4") as c:
            # "Let's trace it on three, five, nine."  nsum steps up to the top left.
            self.play(code.animate.scale(SMALL / HERO).move_to(SMALL_UL, aligned_edge=UL), run_time=1.2)
            c.wait_until("three five nine")
            self.play(FadeIn(r0, shift=0.25 * DOWN), run_time=1.0)

            # "It becomes three plus en-sum of five, nine."  (first step slow)
            c.wait_until("s1")
            self.birth(r0, r1, copies=[(r0.find("nsum ["), r1.find("nsum [")), (r0.find("5; 9]"), r1.find("5; 9]"))],
                       news=[(r0.find("3"), r1.find("3")), (plus, r1.find("+"))],
                       fades=[], arrow=arrows[1], run_time=1.8,
                       extra=[FadeOut(m) for m in self.types])     # the types have had their time
            # "Then three plus five plus en-sum of nine."
            c.wait_until("s2")
            self.birth(r1, r2, copies=[(r1.find("3 +"), r2.find("3 +")), (r1.find("nsum ["), r2.find("nsum [")),
                                       (r1.find("9]"), r2.find("9]"))],
                       news=[(r1.find("5"), r2.find("5")), (plus, r2.find("+", nth=1))],
                       fades=[r2.find("("), r2.find(")")], arrow=arrows[2], run_time=1.5)
            # "Then three plus five plus nine plus en-sum of nil."
            c.wait_until("s3")
            self.birth(r2, r3, copies=[(r2.find("3 + (5 +"), r3.find("3 + (5 +")), (r2.find("nsum ["), r3.find("nsum [")),
                                       (r2.find("]"), r3.find("]")), (r2.find(")"), r3.find(")", nth=1))],
                       news=[(r2.find("9"), r3.find("9")), (plus, r3.find("+", nth=2))],
                       fades=[r3.find("(", nth=1), r3.find(")")], arrow=arrows[3], run_time=1.3)

            # "Look at those additions, waiting."  They turn GOLD, and stack up like plates.
            c.wait_until("pending")
            anims = [time_span(a, 0.0, 0.8) for a in recolor(chars(r3, "+"), GOLD)]
            anims += [time_span(Create(ln), 0.0, 0.8) for ln in under3]
            anims += [time_span(Create(floor), 0.3, 0.9)]
            for k, (p, s) in enumerate(zip(plates, WAITS)):
                a, b = 0.5 + 0.4 * k, 1.4 + 0.4 * k
                anims += [time_span(FadeIn(p[0]), a, b),
                          time_span(TransformFromCopy(r3.find(s), p[1], path_arc=-0.4), a, b)]
            anims += [time_span(FadeIn(label, shift=0.2 * UP), 1.7, 2.4)]
            self.play(*anims, run_time=2.4)
            for p in plates:
                self.remove(*p.get_family())
                self.add(p)

            # "None can happen until we reach nil, ..."  nsum of nil is 0 (the first clause)
            c.wait_until("reach nil")
            self.birth(r3, r4, copies=[(r3.find("3 + (5 + (9 +"), r4.find("3 + (5 + (9 +")),
                                       (r3.find("))"), r4.find("))"))],
                       news=[(code.find("0", line=1), r4.find("0"))], fades=[], arrow=arrows[4],
                       run_time=1.3, extra=[TransformFromCopy(a, b) for a, b in zip(under3, under4)])
            # "... so they all sit on the stack."
            c.wait_until("sit on the stack")
            self.play(FlashAround(VGroup(*plates), color=GOLD, time_width=1.5), run_time=1.0)

            # "Then they finally happen, giving seventeen."  Plates pop from the top, each
            # back into its sum, which becomes its value (in place, inside out).
            steps = [(r4, u[0], [((")", 1), (")", 0)), (("3 + (5 +", 0), ("3 + (5 +", 0))], "(9 + 0)", "9"),
                     (u[0], u[1], [(("3 +", 0), ("3 +", 0))], "(5 + 9)", "14"),
                     (u[1], u[2], [], "3 + 14", "17")]
            for i, (src, dst, keeps, inner, res) in enumerate(steps):
                anims, targets = [], []
                for (a, an), (b, bn) in keeps:
                    t = dst.find(b, nth=bn)
                    anims.append(ReplacementTransform(src.find(a, nth=an), t))
                    targets.append(t)
                t = dst.find(res)
                anims.append(ReplacementTransform(src.find(inner), t))
                targets.append(t)
                anims += [FadeOut(plates[2 - i], target_position=src.find(inner).get_center(), scale=0.4),
                          Uncreate(under4[2 - i])]
                if i == 0:
                    c.wait_until("unwind")
                    self.play(*anims, run_time=0.75)
                elif i == 1:
                    self.play(*anims, run_time=0.7)
                else:
                    c.wait_until("total")
                    rt = max(0.8, min(1.1, c.remaining - 0.03))
                    self.play(*[time_span(a, 0.0, min(0.75, rt - 0.05)) for a in anims],
                              time_span(FadeIn(reply, shift=0.2 * DOWN), 0.45, rt), run_time=rt)
                self.remove(*src.get_family(), *targets)
                self.add(dst)
        self.rows, self.arrows, self.under3 = rows, arrows, under3
        self.final17, self.reply17 = u[2], reply
        self.floor, self.label = floor, label

    # ── sum.5: costs, the overflow, the common slip ───────────────────────────────
    def cost_and_slip(self):
        code = self.code
        t_time = cost_tag("time", "O(n)").move_to([SMALL_UL[0], TAG_Y, 0], aligned_edge=LEFT)
        t_space = cost_tag("space", "O(n)").next_to(t_time, RIGHT, buff=0.7)
        t_space.shift(UP * (t_time[1].get_y() - t_space[1].get_y()))
        floor, label = self.floor, self.label
        plates = [plate(s, k) for k, s in enumerate(WAITS)]
        extra = [plate(None, k) for k in range(3, 7)]        # up to the top of the frame
        so = T("stack overflow", size=36, color=RED).move_to(label)
        wrong = gold_total(Code(WRONG, size=SMALL)).move_to(WRONG_UL, aligned_edge=UL)
        wframe = SurroundingRectangle(wrong, buff=0.18, corner_radius=0.1).set_stroke(RED, 3)
        wreply = Code(R_ADDSUM, size=28)
        wreply.next_to(wframe, DOWN, buff=0.28).align_to(wrong, LEFT)
        xplus = wrong.find("x +")
        wunder = under(xplus, xplus[0].get_bottom()[1])
        plates2 = [plate(s, k) for k, s in enumerate(WAITS)]
        floor2, label2 = rack()

        with self.say("c6.sum.5") as c:
            # "So en-sum takes big O of en time, ..."  The staircase goes; its answer stays a moment.
            staircase = [*self.rows[:4], *self.arrows[1:], *self.under3]
            c.wait_until("time")
            self.play(LaggedStart(*[FadeOut(m) for m in staircase], lag_ratio=0.08),
                      time_span(FadeIn(t_time, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # "... and also big O of en space, for that stack of pending additions."
            c.wait_until("space")
            self.play(FadeIn(t_space, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("stack of pending")
            self.play(*[time_span(FadeIn(p, shift=0.3 * DOWN), 0.25 * k, 0.25 * k + 0.6) for k, p in enumerate(plates)],
                      time_span(FlashAround(t_space, color=GOLD, time_width=1.5), 0.3, 1.2), run_time=1.2)

            # "On a long enough list, it can run out of stack."  The pile runs off the top.
            c.wait_until("overflow")
            starts = [0.25, 0.6, 0.88, 1.1]
            self.play(FadeOut(self.final17), FadeOut(self.reply17),
                      *[time_span(FadeIn(p, shift=0.3 * DOWN), s, s + 0.35) for p, s in zip(extra, starts)],
                      run_time=1.7)
            self.play(*[p[0].animate.set_stroke(RED) for p in (*plates, *extra)],
                      *[p[1].animate.set_color(RED) for p in plates],
                      floor.animate.set_stroke(RED), FadeOut(label), FadeIn(so), run_time=0.8)

            # "A common slip is to add an accumulator, ..."
            c.wait_until("slip")
            self.play(FadeIn(wrong, shift=0.25 * DOWN), run_time=1.1)
            c.wait_until("accumulator")
            self.play(FadeIn(wreply, shift=0.2 * DOWN),
                      FlashAround(wrong.find("total"), color=GOLD, time_width=1.5), run_time=1.0)
            # "... but still write ex plus add-sum of the rest."
            c.wait_until("still write")
            self.play(Create(wframe), FlashAround(wrong.find("x + addsum total xs"), color=RED, time_width=1.5),
                      run_time=1.2)
            # "The addition still waits, and the stack is back."
            c.wait_until("the addition still waits")
            anims = [time_span(a, 0.0, 0.7) for a in recolor([xplus[1]], GOLD)]
            anims += [time_span(FadeOut(m), 0.0, 0.6) for m in (*plates, *extra, floor, so)]
            anims += [time_span(Create(wunder), 0.0, 0.7), time_span(Create(floor2), 0.4, 1.0),
                      time_span(FadeIn(label2, shift=0.2 * UP), 1.0, 1.7)]
            for k, p in enumerate(plates2):
                a, b = 0.5 + 0.3 * k, 1.2 + 0.3 * k
                anims += [time_span(FadeIn(p[0]), a, b),
                          time_span(TransformFromCopy(xplus, p[1], path_arc=-0.4), a, b)]
            self.play(*anims, run_time=1.8)
            for p in plates2:
                self.remove(*p.get_family())
                self.add(p)
        self.t_time, self.t_space = t_time, t_space
        self.slip_bits = [wrong, wframe, wreply, wunder, *plates2, floor2, label2]

    # ── sum.6: the accumulator ────────────────────────────────────────────────────
    def accumulator(self):
        block = [self.code, self.t_time, self.t_space]
        tags_after = VGroup(self.t_time, self.t_space).copy().scale(SHRINK, about_point=SMALL_UL)
        add = gold_total(Code(ADDSUM, size=36))
        add.move_to([SMALL_UL[0], tags_after.get_bottom()[1] - 0.42, 0], aligned_edge=UL)
        ar = Code(R_ADDSUM, size=30).next_to(add, DOWN, buff=0.28, aligned_edge=LEFT)
        sd = Code(SUMDEF, size=36).next_to(ar, DOWN, buff=0.38, aligned_edge=LEFT)
        sr = Code(R_SUM, size=30).next_to(sd, DOWN, buff=0.26, aligned_edge=LEFT)
        lines = [add.line(i) for i in range(3)]

        with self.say("c6.sum.6", gap=2.4) as c:     # a breath to read the finished code
            # "The cure, as for length, is an accumulator."  The slip goes; nsum steps back.
            c.wait_until("accumulator")
            self.play(*[m.animate.scale(SHRINK, about_point=SMALL_UL).set_opacity(0.4) for m in block],
                      run_time=1.0)
            # "Add-sum carries a running total."  The slip makes way for it.
            c.wait_until("addsum")
            self.play(*[FadeOut(m) for m in self.slip_bits],
                      time_span(FadeIn(lines[0], shift=0.25 * DOWN), 0.5, 1.4), run_time=1.4)
            c.wait_until("running total")
            self.play(FlashAround(add.find("total"), color=GOLD, time_width=1.5), run_time=1.0)
            # "On the empty list, it returns the total."
            c.wait_until("acc_base")
            self.play(FadeIn(lines[1], shift=0.25 * DOWN), run_time=1.0)
            # "Otherwise, it adds the head to the total, and carries on with the tail."
            c.wait_until("acc_step")
            self.play(FadeIn(lines[2], shift=0.25 * DOWN), run_time=1.0)
            self.remove(*lines)
            self.add(add)
            c.wait_until("adds the head")
            self.play(FlashAround(add.find("(total + x)"), color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("carries on")
            self.play(FadeIn(ar, shift=0.2 * DOWN), run_time=0.9)
            # "Sum starts it off from zero."
            c.wait_until("wrap")
            self.play(FadeIn(sd, shift=0.25 * DOWN), time_span(FadeIn(sr, shift=0.2 * DOWN), 0.3, 1.1),
                      run_time=1.1)
        self.add_code, self.sd, self.ar, self.sr = add, sd, ar, sr

    # ── sum.7: the flat trace, stacked; the total riding the chain ─────────────────
    def flat_trace(self):
        add, ar, sd, sr = self.add_code, self.ar, self.sd, self.sr
        # top band: addsum and sum with their replies (dimmed), all at 28
        add_t = add.copy().scale(28 / 36).move_to(TOP_UL, aligned_edge=UL)
        ar_t = ar.copy().scale(28 / 30).next_to(add_t, DOWN, buff=0.16, aligned_edge=LEFT)
        sd_t = sd.copy().scale(28 / 36).next_to(ar_t, DOWN, buff=0.24, aligned_edge=LEFT)
        sr_t = sr.copy().scale(28 / 30).next_to(sd_t, DOWN, buff=0.16, aligned_edge=LEFT)
        moves = [(add, add_t, 28 / 36, 1.0), (ar, ar_t, 28 / 30, REPLY_DIM),
                 (sd, sd_t, 28 / 36, 1.0), (sr, sr_t, 28 / 30, REPLY_DIM)]
        # bottom right: the chain, the total box riding above the current cell
        chain = ConsChain([3, 5, 9]).scale(S_CHAIN).move_to(CHAIN_C)
        cells, nil = chain.cells, chain.nil
        stops = [*cells, nil]
        top = cells[0].box.get_top()[1]

        def hover(m):
            return np.array([m.get_x() if m is nil else m.box.get_x(), top + 0.6, 0])

        frame = count_frame().move_to(hover(cells[0]))
        word = T("total", size=30, color=DIM).next_to(frame, UP, buff=0.1)
        nums = [Mono(str(v), size=40, color=GOLD).set_z_index(1) for v in TOTALS]   # over the box
        nums[0].move_to(frame)
        # bottom left: the trace, one line per call; none is wider than the one before
        srcs = ["sum [3; 5; 9]", *FLAT]
        tb = [TB0 - TP * k for k in range(len(srcs))]
        lines = [put(Code(f, size=TS), TX, y) for f, y in zip(srcs, tb)]
        arrows = [None] + [MathTex(r"\Rightarrow", font_size=TS * 1.6, color=DIM)
                           .next_to(ln, LEFT, buff=0.22).set_y(y + 0.0101 * TS / 2)
                           for ln, y in zip(lines[1:], tb[1:])]
        reply = put(Code(R_17, size=TS), TX, tb[-1] - TP)

        def ride(i):
            """The box moves on to the next stop; the head it passed joins the total. The old
            total stays behind, dimmed, over the cell it belonged to (the trace's history)."""
            dst = hover(stops[i + 1])
            nums[i + 1].move_to(dst)
            return [frame.animate.move_to(dst), word.animate.shift(dst - frame.get_center()),
                    nums[i].animate.set_opacity(HIST),
                    TransformFromCopy(cells[i].label, nums[i + 1], path_arc=-0.5),
                    cells[i].animate.set_opacity(DIM_TO), chain.arrows[i].animate.set_opacity(DIM_TO)]

        def next_line(i, pairs):
            """Line i is born under line i-1 (P11): its parts fly in from where they come
            from; line i-1 steps back into the history. Returns (anims, targets)."""
            anims, tgts = [], []
            for src, sub in pairs:
                t = lines[i].find(sub)
                anims.append(TransformFromCopy(src, t))
                tgts.append(t)
            anims.append(FadeIn(arrows[i], shift=0.2 * DOWN))
            anims.append(lines[i - 1].animate.set_opacity(HIST))
            if arrows[i - 1] is not None:
                anims.append(arrows[i - 1].animate.set_opacity(HIST))
            return anims, tgts

        def settle_line(i, tgts):
            self.remove(*tgts)
            self.add(lines[i])

        def step(i):   # lines[i] = "addsum k [rest]", from lines[i-1] and the box
            prev, cur = lines[i - 1], lines[i]
            k = str(TOTALS[i - 1])
            rest = FLAT[i - 1].split("[", 1)[1]                       # e.g. "5; 9]" or "]"
            prev_rest = FLAT[i - 2].split("[", 1)[1]
            tail = prev_rest[prev_rest.index(";") + 2:] if ";" in prev_rest else "]"
            assert tail == rest, (tail, rest)
            pairs = [(prev.find("addsum"), "addsum"), (nums[i - 1], k), (prev.find("["), "[")]
            pairs.append((prev.find(tail, nth=prev.src.count(tail) - 1), rest))
            return next_line(i, pairs)

        with self.say("c6.sum.7") as c:
            # "On the same list,"  nsum goes; the code and its replies move up; chain; the call
            self.play(*[FadeOut(m) for m in (self.code, self.t_time, self.t_space)],
                      *[m.animate.scale(k).move_to(t.get_corner(UL), aligned_edge=UL).set_opacity(op)
                        for m, t, k, op in moves],
                      time_span(FadeIn(chain, shift=0.3 * DOWN), 0.4, 1.2),
                      time_span(FadeIn(lines[0], shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            # "the total starts at zero, with three, five, nine to go."  The 0 is sum's.
            c.wait_until("t1")
            self.play(FadeIn(frame, shift=0.25 * DOWN), FadeIn(word, shift=0.25 * DOWN),
                      TransformFromCopy(sd.find("0"), nums[0], path_arc=0.5), run_time=1.0)
            c.wait_until("with three")
            anims, tgts = next_line(1, [(sd.find("addsum"), "addsum"), (nums[0], "0"),
                                        (lines[0].find("[3; 5; 9]"), "[3; 5; 9]")])
            self.play(*anims, run_time=1.4)
            settle_line(1, tgts)

            # "Then three, with five, nine to go."  (first step slow: ride, then the call)
            c.wait_until("t2")
            self.play(*ride(0), run_time=1.2)
            anims, tgts = step(2)
            self.play(*anims, run_time=1.3)
            settle_line(2, tgts)

            # "Then eight, with nine to go."  "Then seventeen, with nothing left."  (quicker)
            for i, cue in ((1, "t3"), (2, "t4")):
                c.wait_until(cue)
                anims, tgts = step(i + 2)      # listed first: it copies the box number as it lands
                self.play(*[time_span(a, 0.5, 1.3) for a in anims],
                          *[time_span(a, 0.0, 0.8) for a in ride(i)], run_time=1.3)
                settle_line(i + 2, tgts)
            c.wait_until("nothing left")
            self.play(FlashAround(nil, color=TEAL, time_width=1.5),
                      FlashAround(lines[4].find("[]"), color=TEAL, time_width=1.5), run_time=1.0)

            # "Nothing waits."  The answer is the total; every line was as short as the last.
            c.wait_until("flat")
            anims, tgts = next_line(5, [(nums[3], "17")])
            self.play(*[time_span(a, 0.0, 1.0) for a in anims],
                      time_span(FadeIn(reply, shift=0.2 * DOWN), 0.7, 1.5), run_time=1.5)
            settle_line(5, tgts)
            # "Each call replaces the call before it."  The history folds into the last line.
            c.wait_until("each call replaces")
            fold = [FadeOut(m, shift=DOWN * (tb[5] - tb[k])) for k, m in enumerate(lines[:5])]
            fold += [FadeOut(m, shift=DOWN * (tb[5] - tb[k])) for k, m in enumerate(arrows[:5]) if m is not None]
            self.play(*fold, *[FadeOut(n) for n in nums[:3]], run_time=1.2)
        self.answer = (arrows[5], lines[5], reply)

    # ── sum.8: the comment on efficiency ──────────────────────────────────────────
    def compare(self):
        cx = [-3.4, 0.2, 3.4]
        ys = [1.3, 0.1, -1.2]
        hdrs = [T("time", size=36, color=DIM).move_to([cx[1], ys[0], 0]),
                T("space", size=36, color=DIM).move_to([cx[2], ys[0], 0])]
        hdrs[1].shift(UP * (baseline(hdrs[0]) - baseline(hdrs[1])))
        rule = Line([-4.7, 0.78, 0], [4.7, 0.78, 0]).set_stroke(DIM, 2)
        names = [Mono("nsum", size=44, color=YELLOW).move_to([cx[0], ys[1], 0]),
                 Mono("sum", size=44, color=YELLOW).move_to([cx[0], ys[2], 0])]
        o = [[MathTex("O(n)", font_size=60, color=GOLD).move_to([cx[k], ys[1], 0]) for k in (1, 2)],
             [MathTex(big, font_size=60, color=GOLD).move_to([cx[k], ys[2], 0]) for k, big in ((1, "O(n)"), (2, "O(1)"))]]
        for row, name in zip(o, names):
            name.shift(UP * (row[0][0][0].get_bottom()[1] - baseline(name)))

        with self.say("c6.sum.8") as c:
            # "So, the comment on efficiency."  The table, with nsum's row.
            c.wait_until("comment")
            sweep_clear(self, time_span(FadeIn(rule), 0.6, 1.4),
                        *[time_span(FadeIn(m, shift=0.2 * DOWN), 0.7, 1.6) for m in (*hdrs, names[0], *o[0])],
                        keep=self.answer, run_time=1.6)
            # "Both versions take big O of en time, ..."
            c.wait_until("time")
            self.play(*[FadeOut(m) for m in self.answer],
                      FadeIn(names[1], shift=0.2 * DOWN), FadeIn(o[1][0], shift=0.2 * DOWN), run_time=1.0)
            # "... since each visits every element."
            c.wait_until("each visits")
            self.play(FlashAround(o[0][0], color=GOLD, time_width=1.5),
                      FlashAround(o[1][0], color=GOLD, time_width=1.5), run_time=1.2)
            # "The gain is in space, from big O of en down to big O of one, ..."
            c.wait_until("gain")
            self.play(FlashAround(o[0][1], color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("from big o of en")
            self.play(TransformFromCopy(o[0][1], o[1][1]), run_time=1.5)
            # "... because the calls no longer nest."
            c.wait_until("no longer nest")
            self.play(FlashAround(o[1][1], color=GOLD, time_width=1.5), run_time=1.0)
