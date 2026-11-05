"""Chapter 3, scene 5: nlength is polymorphic, but wasteful (O(n) space, stack overflow),
and Lecture 2's nsum built the same staircase. Clips c3.poly.1, c3.cost.1, c3.cost.2.

OCaml replies verified on 5.4.1: val nlength : 'a list -> int = <fun>; 4 / 2 / 3; nsum 3 = 6;
nlength on 1e6 .. 20e6 elements all fine, 40e6 -> "Stack overflow during evaluation". So the
stack picture never shows a million crashing: the column races to 1,000,000 (which fits), then
keeps growing off the top of the frame while the 1,000,000 mark slides down near the floor, and
only that much longer stack turns RED with "stack overflow".

poly.1: code + reply (type GREEN, 'a PINK), three calls on strings / bools / lists, the
  elements sealed in boxes (never looked at), `x` matched but unused, each element counted.
cost.1: the chain a, b, c tosses one `1 +` per call onto a pile with a GOLD counter riding its
  top; the chain becomes a million long and the pile races to 1,000,000 (always_redraw column
  driven by L = log10 n); memory brace -> O(n) space; then the stack runs off the top, RED.
cost.2: nlength's and nsum's traces stacked, the same staircase; nested calls boxed;
  "not tail-recursive" and the cure.

STATUS (built): check clean apart from intended flags: "overlap" in poly.1 (the GOLD counts sit
  on opaque seals over the hidden elements) and "cut off" at the end of cost.1 (the stack runs
  off the top of the frame on purpose).
"""
import sys
from math import log
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = """let rec nlength = function
  | [] -> 0
  | x :: xs -> 1 + nlength xs"""
REPLY = "val nlength : 'a list -> int = <fun>"
CALLS = ['nlength ["to"; "be"; "or"; "not"]', "nlength [true; false]", "nlength [[3]; []; [5; 6]]"]
ANSWERS = ["- : int = 4", "- : int = 2", "- : int = 3"]
ELEMS = [['"to"', '"be"', '"or"', '"not"'], ["true", "false"], ["[3]", "[]", "[5; 6]"]]
ROW_Y = [-0.6, -1.65, -2.7]
SEAL = "#232830"

GROW = ["nlength [a; b; c]", "1 + nlength [b; c]", "1 + (1 + nlength [c])",
        "1 + (1 + (1 + nlength []))", "1 + (1 + (1 + 0))"]
NSUM = ["nsum 3", "3 + (nsum 2)", "3 + (2 + (nsum 1))", "3 + (2 + (1 + (nsum 0)))",
        "3 + (2 + (1 + 0))"]
TR_SIZE = 30
TR_PITCH = 0.62
TR_BASE1 = 2.9          # baseline of nlength's first trace row
TR_BASE2 = -0.75        # baseline of nsum's first trace row
TR_SHIFT = 3.0          # traces move left by this to make room for the verdict

# the stack of waiting additions
SX = 2.0                # column centre x
SW = 1.8                # column width
FLOOR = -2.9
PITCH0 = 0.62           # one "1 +" box
BOXF = "#1E222A"
L3 = log(3, 10)
MIN_SEP = 0.07          # separators closer than this fade out (power-of-2 levels of detail)


def col_height(L):
    """Height of the stack for n = 10**L: piecewise-linear, 3 boxes -> 1.86, a million -> 5.0
    (fits the frame), 10**7.5 -> 7.6 (runs off the top)."""
    pts = [(L3, 3 * PITCH0), (6.0, 5.0), (7.5, 7.6)]
    if L <= pts[1][0]:
        (a, ha), (b, hb) = pts[0], pts[1]
    else:
        (a, ha), (b, hb) = pts[1], pts[2]
    return ha + (hb - ha) * (L - a) / (b - a)


def clip01(v):
    return float(min(1.0, max(0.0, v)))


def live(func):
    """Like always_redraw, but swaps in fresh children every frame: become() would keep the
    largest set of children ever drawn (stale '1 +' texts, extra digits)."""
    g = VGroup(*func().submobjects)
    g.add_updater(lambda m: setattr(m, "submobjects", list(func().submobjects)))
    return g


# ── helpers (local to this scene) ───────────────────────────────────────────────
_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789")


def baseline(code):
    """y of the text baseline of a Code."""
    chars_ = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars_, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def implies():
    return MathTex(r"\Rightarrow", font_size=46, color=DIM)


def under(glyphs, base, color=YELLOW):
    """The yellow underline of one waiting addition."""
    y = base - 0.11
    return Line([glyphs.get_left()[0], y, 0], [glyphs.get_right()[0], y, 0],
                color=color, stroke_width=4)


def stack_box(y_center):
    """One waiting `1 +`, as it sits on the pile."""
    r = Rectangle(width=SW, height=PITCH0).set_stroke(YELLOW, 3).set_fill(BOXF, 1)
    r.move_to([SX, y_center, 0])
    t = Mono("1 +", size=30, color=YELLOW).move_to(r)
    return VGroup(r, t)


def count_label(num, under_mob):
    """'<num> elements' centred under a brace."""
    words = T("elements", size=32)
    g = VGroup(num, words).arrange(RIGHT, buff=0.16)
    num.shift(UP * (words.get_bottom()[1] - num[0].get_bottom()[1]))   # share the baseline
    g.next_to(under_mob, UP, buff=0.14)
    return g


class AnyTypeButWasteful(NarratedScene):
    def construct(self):
        self.polymorphic()   # c3.poly.1
        self.waiting()       # c3.cost.1
        self.staircase()     # c3.cost.2
        self.wait(3.5)       # end hold on the verdict
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c3.poly.1: any type at all ───────────────────────────────────────────────
    def polymorphic(self):
        code = Code(SRC, size=36).move_to([0, 2.45, 0])
        reply = Code(REPLY, size=32).move_to([0, 0.9, 0])
        reply.find("nlength").set_color(YELLOW)
        reply.find("list -> int").set_color(GREEN)
        self.code, self.reply = code, reply

        calls = [Code(s, size=32) for s in CALLS]
        answers = [Code(s, size=32) for s in ANSWERS]
        for cl in calls:
            cl.find("nlength").set_color(YELLOW)
        wc = max(c.width for c in calls)
        wa = max(a.width for a in answers)
        x0 = -(wc + 0.75 + wa) / 2
        for cl, an, y in zip(calls, answers, ROW_Y):
            cl.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
            an.align_to([x0 + wc + 0.75, 0, 0], LEFT)
            an.shift(UP * (baseline(cl) - baseline(an)))
        self.calls, self.answers = calls, answers

        with self.say("c3.poly.1") as c:
            self.play(FadeIn(code, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("reply")
            name_dst = reply.find("nlength")
            others = VGroup(*[g for g in reply.text if not any(g is n for n in name_dst)])
            self.play(TransformFromCopy(code.find("nlength"), name_dst),
                      FadeIn(others, shift=0.2 * DOWN),
                      run_time=min(1.6, 0.8 * c.until("alpha list to int")))
            settle(self, reply)
            c.wait_until("alpha list to int")
            box = token_box(reply.find("'a list -> int"), reply, GREEN, pad=0.18)
            self.play(FadeIn(box), run_time=min(1.0, 0.6 * c.until("alpha")))
            c.wait_until("alpha")
            alpha = reply.find("'a")
            self.play(Transform(box, token_box(alpha, reply, PINK, pad=0.18)),
                      run_time=min(1.2, 0.6 * c.until("any type")))
            c.wait_until("any type")
            any_t = T("any type", size=32, color=PINK).next_to(reply, DOWN, buff=0.22)
            any_t.set_x(alpha.get_x())
            self.play(FadeIn(any_t, shift=0.3 * UP), run_time=min(1.0, 0.8 * c.until("strings")))
            self.any_t, self.alpha_box = any_t, box

            # three calls drop in, one per word
            for k, cue in enumerate(["strings", "bools", "lists"]):
                c.wait_until(cue)
                nxt = ["bools", "lists", "why"][k]
                self.play(LaggedStart(FadeIn(calls[k], shift=0.3 * DOWN),
                                      FadeIn(answers[k], shift=0.3 * DOWN), lag_ratio=0.35),
                          run_time=min(1.0, 0.85 * c.until(nxt)))

            # nlength never looks inside: each element sealed in a box
            c.wait_until("never looks inside")
            seals, nums = [], []
            for cl, elems in zip(calls, ELEMS):
                h = cl.height + 0.16
                row_s, row_n = [], []
                for i, e in enumerate(elems):
                    g = cl.find(e)
                    s = Rectangle(width=g.width + 0.18, height=h).set_stroke(BLUE, 2.5)
                    s.set_fill(SEAL, 1).move_to([g.get_x(), cl.get_y(), 0]).set_z_index(1)
                    row_s.append(s)
                    row_n.append(T(str(i + 1), size=30, color=GOLD).move_to(s).set_z_index(2))
                seals.append(row_s)
                nums.append(row_n)
            self.play(LaggedStart(*[FadeIn(s, scale=1.15) for row in seals for s in row],
                                  lag_ratio=0.12),
                      run_time=min(1.8, 0.8 * c.until("head")))
            self.seals, self.nums = seals, nums

            # the head x: matched, never used
            c.wait_until("head")
            x = code.find("x", line=2)
            hbox = token_box(x, code.line(2), YELLOW, pad=0.2)
            self.play(FadeIn(hbox), FadeOut(box), run_time=min(1.0, 0.6 * c.until("never used")))
            c.wait_until("never used")
            self.x_color = x[0].get_color()
            self.play(Transform(hbox, token_box(code.find("1 + nlength xs"), code.line(2), YELLOW)),
                      *recolor(x, DIM), run_time=min(1.5, 0.7 * c.until("counted")))

            # each element just gets counted: 1 + per element
            c.wait_until("counted")
            self.play(Transform(hbox, token_box(code.find("1 +"), code.line(2), YELLOW)),
                      LaggedStart(*[AnimationGroup(*[FadeIn(row[i], scale=0.6)
                                                     for row in nums if i < len(row)])
                                    for i in range(4)], lag_ratio=0.45),
                      run_time=min(2.0, 0.6 * c.until("free")))
            self.play(*[FlashAround(a.find(str(n)), color=GOLD, time_width=1.5)
                        for a, n in zip(answers, (4, 2, 3))],
                      run_time=min(1.4, 0.8 * c.until("free")))

            # other languages; in OCaml it is free
            c.wait_until("free")
            rows = calls + answers + [n for r in nums for n in r]
            self.play(*set_alpha(rows, 0.35), FadeOut(hbox),
                      *[s.animate.set_stroke(opacity=0.35) for r in seals for s in r],
                      run_time=min(1.2, 0.6 * c.until("flexibility")))
            c.wait_until("flexibility")
            tbox = token_box(reply.find("'a list -> int"), reply, GREEN, pad=0.18)
            self.play(FadeIn(tbox), run_time=min(1.0, 0.6 * c.until("for free")))
            self.type_box = tbox
            c.wait_until("for free")
            self.play(FlashAround(code, color=GREEN, time_width=1.5, buff=0.2),
                      run_time=min(2.0, 0.9 * c.remaining))

    # ── c3.cost.1: the additions that wait ─────────────────────────────────────
    def column(self):
        """The pile of waiting additions for n = 10**L (always_redraw)."""
        L = self.L.get_value()
        n = 10 ** L
        h = col_height(L)
        pitch = h / n
        red = self.red.get_value()
        edge = interpolate_color(ManimColor(YELLOW), ManimColor(RED), red)
        dense = clip01(log(PITCH0 / pitch) / log(PITCH0 / MIN_SEP))
        fill = interpolate_color(ManimColor(BOXF), ManimColor(YELLOW), 0.3 * dense)
        fill = interpolate_color(fill, ManimColor(RED), 0.3 * red)
        body = Rectangle(width=SW, height=h).set_stroke(edge, 3).set_fill(fill, 1)
        body.move_to([SX, FLOOR + h / 2, 0])
        g = VGroup(body)
        s = 1
        while s * pitch < MIN_SEP:
            s *= 2
        a_odd = clip01((s * pitch - MIN_SEP) / MIN_SEP)
        width = 1.5 + 1.5 * clip01((pitch - MIN_SEP) / 0.23)
        k = s
        while k < n - 1e-6:
            y = FLOOR + k * pitch
            if y > 4.3:
                break
            op = 1.0 if k % (2 * s) == 0 else a_odd
            if op > 0.01:
                g.add(Line([SX - SW / 2, y, 0], [SX + SW / 2, y, 0]).set_stroke(edge, width,
                                                                                 opacity=op))
            k += s
        a_txt = clip01((pitch - 0.3) / 0.15)
        if a_txt > 0.01:
            sc = min(1.0, pitch / PITCH0)
            for i in range(int(n + 1e-6)):
                t = self.one_plus.copy().scale(sc).move_to([SX, FLOOR + (i + 0.5) * pitch, 0])
                g.add(t.set_opacity(a_txt))
        return g

    def counter(self):
        """GOLD count of the waiting additions, riding the top of the pile (P19)."""
        if self.racing:
            L = self.L.get_value()
            n = 10 ** L
            v = min(n, 1e6)
            y = FLOOR + v * col_height(L) / n
        else:
            v, y = self.cnt.get_value(), self.top.get_value()
        tick = Line([SX + SW / 2 + 0.06, y, 0], [SX + SW / 2 + 0.42, y, 0], color=GOLD,
                    stroke_width=4)
        num = Integer(int(round(v)), font_size=44, color=GOLD).next_to(tick, RIGHT, buff=0.12)
        return VGroup(tick, num)

    def waiting(self):
        code = self.code
        chain = ConsChain(["a", "b", "c"]).scale(0.75)
        chain.move_to([0, 0.45, 0]).align_to([-6.4, 0, 0], LEFT)
        floor = Line([SX - SW / 2 - 0.4, FLOOR, 0], [SX + SW / 2 + 0.4, FLOOR, 0],
                     color=DIM, stroke_width=4)
        caption = T("additions waiting", size=30, color=DIM).next_to(floor, DOWN, buff=0.2)
        self.L, self.red = ValueTracker(L3), ValueTracker(0)
        self.cnt, self.top = ValueTracker(1), ValueTracker(FLOOR + PITCH0)
        self.racing = False
        self.one_plus = Mono("1 +", size=30, color=YELLOW)

        with self.say("c3.cost.1") as c:
            # wasteful: clear the examples, the code moves aside, a list and a floor arrive
            code.generate_target()
            code.target.scale(0.8).to_corner(UL, buff=0.5)
            code.target.find("x", line=2).set_color(self.x_color)
            sweep_clear(self, MoveToTarget(code),
                        time_span(FadeIn(chain, shift=0.3 * DOWN), 0.6, 1.5),
                        time_span(Create(floor), 0.8, 1.5), time_span(FadeIn(caption), 1.0, 1.6),
                        keep=[code], run_time=min(1.6, 0.8 * c.until("additions")))
            c.wait_until("additions")
            pbox = token_box(code.find("1 +"), code.line(2), YELLOW, pad=0.16)
            self.play(FadeIn(pbox), run_time=min(0.9, 0.7 * c.until("had to wait")))

            # one `1 +` tossed onto the pile per call
            cursor = SurroundingRectangle(chain.cells[0], color=YELLOW, buff=0.08)
            boxes = []
            cues = ["had to wait", "keep track", "until the recursion"]
            nexts = ["keep track", "until the recursion", "end of the list"]
            for k in range(3):
                c.wait_until(cues[k])
                rt = min(1.3, 0.85 * c.until(nexts[k]))
                cell = chain.cells[k]
                box = stack_box(FLOOR + PITCH0 * (k + 0.5))
                start = box.copy().scale(0.45).move_to(cell.get_top() + 0.35 * UP)
                cur = SurroundingRectangle(cell, color=YELLOW, buff=0.08)
                anims = [time_span(FadeIn(cursor) if k == 0 else Transform(cursor, cur),
                                   0, 0.35 * rt),
                         time_span(ReplacementTransform(start, box, path_arc=-0.6 * PI),
                                   0.2 * rt, rt)]
                if k == 0:
                    self.cnt_mob = live(self.counter)
                    anims.append(time_span(FadeIn(self.cnt_mob), 0.8 * rt, rt))
                else:
                    anims += [time_span(self.cnt.animate.set_value(k + 1), 0.7 * rt, rt),
                              time_span(self.top.animate.set_value(FLOOR + PITCH0 * (k + 1)),
                                        0.2 * rt, rt)]
                self.play(*anims, run_time=rt)
                boxes.append(box)

            # the end of the list: three elements, three additions waiting
            c.wait_until("end of the list")
            brace = Brace(VGroup(*chain.cells), UP, buff=0.12, color=DIM)
            label = count_label(T("3", size=34, color=GOLD), brace)
            self.play(Transform(cursor, SurroundingRectangle(chain.nil, color=YELLOW, buff=0.1)),
                      FlashAround(chain.nil, color=TEAL, time_width=1.5, buff=0.16),
                      time_span(GrowFromCenter(brace), 0.3, 1.0),
                      time_span(FadeIn(label, shift=0.3 * DOWN), 0.4, 1.0), run_time=1.0)
            c.wait_until("three")
            self.play(FadeOut(cursor), FlashUnder(label[0], color=GOLD, time_width=1.5),
                      run_time=min(1.0, 0.6 * c.until("three additions")))
            c.wait_until("three additions")
            self.play(FlashAround(VGroup(*boxes), color=YELLOW, time_width=1.5, buff=0.12),
                      FlashAround(self.cnt_mob[1], color=GOLD, time_width=1.5),
                      run_time=min(1.6, 0.9 * c.until("million")))

            # a million elements: the chain gets long, the pile races to 1,000,000
            c.wait_until("a million elements")
            D = 1.0
            start = chain.cells[1].tail_start()
            end = chain.cells[2].entry() + D * RIGHT
            long_arrow = Arrow(start, end, buff=0, stroke_width=3, color=FG,
                               max_tip_length_to_length_ratio=0.3, tip_length=0.12)
            dots = MathTex(r"\cdots", font_size=48, color=DIM).move_to(
                long_arrow.get_center() + 0.25 * DOWN)
            far = VGroup(chain.cells[0].copy(), chain.cells[2].copy().shift(D * RIGHT))
            brace2 = Brace(far, UP, buff=0.12, color=DIM)
            label2 = count_label(T("1,000,000", size=34, color=GOLD), brace2)
            self.play(chain.cells[2].animate.shift(D * RIGHT),
                      chain.arrows[2].animate.shift(D * RIGHT),
                      chain.nil.animate.shift(D * RIGHT),
                      Transform(chain.arrows[1], long_arrow), FadeIn(dots, shift=0.2 * UP),
                      Transform(brace, brace2),
                      FadeOut(label[0], shift=0.25 * UP), FadeIn(label2[0], shift=0.25 * UP),
                      ReplacementTransform(label[1], label2[1]),
                      FadeOut(pbox),
                      run_time=min(1.5, 0.8 * c.until("leaves")))
            label = label2

            c.wait_until("leaves")
            self.remove(*boxes)
            self.racing = True
            col = live(self.column)
            self.add(col)
            self.bring_to_front(self.cnt_mob)
            self.play(self.L.animate.set_value(6.0), rate_func=smooth,
                      run_time=max(1.5, min(3.2, c.until("space") - 0.6)))

            # memory grows with the length: O(n) space
            c.wait_until("memory")
            mbrace = Brace(Line([SX - SW / 2, FLOOR, 0], [SX - SW / 2, FLOOR + 5.0, 0]), LEFT,
                           buff=0.15, color=GOLD)
            mlabel = T("memory", size=36, color=GOLD).next_to(mbrace, LEFT, buff=0.15)
            self.play(GrowFromCenter(mbrace), FadeIn(mlabel, shift=0.3 * RIGHT),
                      run_time=min(1.2, 0.7 * c.until("length of the list")))
            c.wait_until("length of the list")
            self.play(FlashAround(label, color=GOLD, time_width=1.5, buff=0.14),
                      run_time=min(1.5, 0.8 * c.until("big O")))
            c.wait_until("big O")
            big_o = VGroup(MathTex("O(", "n", ")", font_size=80, color=GOLD),
                           T("space", size=44, color=GOLD))
            big_o.arrange(RIGHT, buff=0.3).move_to([-3.3, -2.3, 0])
            big_o[1].align_to(big_o[0][0], DOWN)
            self.play(FadeTransform(mlabel.copy(), big_o),
                      run_time=min(1.8, 0.8 * c.until("where en is the length")))
            c.wait_until("where en is the length")
            label3 = count_label(T("n", size=36, color=GOLD, slant=ITALIC), brace)
            self.play(FadeOut(label[0], shift=0.2 * UP),
                      TransformFromCopy(big_o[0][1], label3[0], path_arc=-0.4 * PI),
                      ReplacementTransform(label[1], label3[1]),
                      run_time=min(1.6, 0.8 * c.until("long enough")))

            # a long enough list runs out of room
            c.wait_until("long enough")
            self.play(FadeOut(mbrace), FadeOut(mlabel), run_time=0.6)
            self.play(self.L.animate.set_value(7.5), rate_func=smooth,
                      run_time=max(1.2, min(2.8, c.until("crash") - 0.2)))
            c.wait_until("crash")
            overflow = T("stack overflow", size=40, color=RED)
            overflow.move_to([0, 3.25, 0]).align_to([6.5, 0, 0], RIGHT)
            self.play(self.red.animate.set_value(1), FadeIn(overflow, shift=0.3 * LEFT),
                      run_time=min(1.0, 0.9 * c.remaining))
            self.col = col

    # ── c3.cost.2: the same staircase as nsum ──────────────────────────────────
    def staircase(self):
        def trace(srcs, base0, name):
            rows = [Code(s, size=TR_SIZE) for s in srcs]
            for r in rows:
                if name in r.src:
                    r.find(name).set_color(YELLOW)
            return rows, [base0 - TR_PITCH * i for i in range(len(srcs))]

        rows1, base1 = trace(GROW, TR_BASE1, "nlength")
        rows2, base2 = trace(NSUM, TR_BASE2, "nsum")
        aw = implies().width
        widest = max(r.width for r in rows1 + rows2) + aw + 0.25
        x0 = -widest / 2 + aw + 0.25
        arrows = []
        for rows, bases in ((rows1, base1), (rows2, base2)):
            for i, (r, b) in enumerate(zip(rows, bases)):
                put(r, x0, b)
                if i:
                    arrows.append(implies().next_to(r, LEFT, buff=0.25).set_y(b + 0.1))
        lec2 = T("Lecture 2", size=30, color=DIM).next_to(rows2[0], RIGHT, buff=0.6)
        lec2.shift(UP * (base2[0] - lec2.get_bottom()[1]))
        # the waiting additions: k underlines in row k (3 in the last row)
        segs1 = [under(rows1[k].find("1 +", nth=j), base1[k]) for k in range(1, 5)
                 for j in range(min(k, 3))]
        segs2 = [under(rows2[k].find(p), base2[k]) for k in range(1, 5)
                 for p in ("3 +", "2 +", "1 +")[:min(k, 3)]]
        everything = rows1 + rows2 + arrows + [lec2] + segs1 + segs2

        with self.say("c3.cost.2") as c:
            c.wait_until("built")
            entering = []
            for rows in (rows1, rows2):
                entering += [FadeIn(r, shift=0.2 * DOWN) for r in rows]
            rt = max(1.4, min(2.2, c.until("three plus") - 1.2))
            sweep_clear(self, time_span(LaggedStart(*entering, lag_ratio=0.12), 0.5, rt),
                        time_span(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.1),
                                  0.8, rt),
                        time_span(FadeIn(lec2, shift=0.2 * LEFT), 0.9 * rt, rt),
                        run_time=rt)
            c.wait_until("staircase")
            self.play(LaggedStart(*[Create(s) for s in segs1 + segs2], lag_ratio=0.05),
                      run_time=min(1.2, 0.8 * c.until("three plus")))

            # three plus, two plus, one plus zero, along nsum's last row
            last = rows2[4]
            c.wait_until("three plus")
            tb = token_box(last.find("3 +"), last, YELLOW, pad=0.16)
            self.play(FadeIn(tb), run_time=min(0.6, 0.8 * c.until("two plus")))
            for cue, nxt, piece in (("two plus", "one plus", "2 +"), ("one plus", "zero", "1 +"),
                                    ("zero", "nest", "0")):
                c.wait_until(cue)
                self.play(Transform(tb, token_box(last.find(piece), last, YELLOW, pad=0.16)),
                          run_time=min(0.6, 0.8 * c.until(nxt)))

            # the recursive calls nest inside each other
            c.wait_until("nest")
            subs1 = [None, "(1 + (1 + nlength []))", "(1 + nlength [])", "nlength []"]
            subs2 = [None, "(2 + (1 + (nsum 0)))", "(1 + (nsum 0))", "(nsum 0)"]
            nests = []
            for row, subs in ((rows1[3], subs1), (rows2[3], subs2)):
                lvl = []
                for i, s in enumerate(subs):
                    g = VGroup(*row.text) if s is None else row.find(s)
                    pad, h = 0.24 - 0.06 * i, 0.74 - 0.1 * i
                    lvl.append(Rectangle(width=g.width + 2 * pad, height=h)
                               .set_stroke(BLUE, 3).move_to([g.get_x(), row.get_y(), 0]))
                nests.append(lvl)
            spot = {id(m) for m in [rows1[3], rows2[3], arrows[2], arrows[6]]
                    + segs1[3:6] + segs2[3:6]}
            others = [m for m in everything if id(m) not in spot]
            self.play(FadeOut(tb), *set_alpha(others, DIMMED),
                      time_span(LaggedStart(*[AnimationGroup(Create(nests[0][i]),
                                                             Create(nests[1][i]))
                                              for i in range(4)], lag_ratio=0.35), 0.4,
                                min(2.4, 0.8 * c.until("inside it"))),
                      run_time=min(2.4, 0.8 * c.until("inside it")))

            # each waits for the call inside it, then does one more addition
            c.wait_until("inside it")
            self.play(LaggedStart(*[AnimationGroup(
                VShowPassingFlash(nests[0][i].copy().set_stroke(YELLOW, 6), time_width=0.6),
                VShowPassingFlash(nests[1][i].copy().set_stroke(YELLOW, 6), time_width=0.6))
                for i in (3, 2, 1, 0)], lag_ratio=0.3),
                run_time=min(2.0, 0.8 * c.until("one more addition")))
            c.wait_until("one more addition")
            pieces = [(rows1[3].find("1 +", nth=j), rows2[3].find(p))
                      for j, p in ((2, "1 +"), (1, "2 +"), (0, "3 +"))]
            self.play(LaggedStart(*[AnimationGroup(FlashAround(a, time_width=1.5),
                                                   FlashAround(b, time_width=1.5))
                                    for a, b in pieces], lag_ratio=0.35),
                      run_time=min(1.8, 0.8 * c.until("tail")))

            # not tail-recursive; the cure
            c.wait_until("tail")
            self.play(*[FadeOut(b) for lvl in nests for b in lvl],
                      *[restyle(m, op=1, shift=TR_SHIFT * LEFT) for m in everything],
                      run_time=min(1.5, 0.8 * c.until("not tail-recursive")))
            right = max(r.get_right()[0] for r in rows1 + rows2) + 0.2
            top = rows1[0].get_top()[1] + 0.05
            bot = rows2[4].get_bottom()[1] - 0.1
            vbrace = Brace(Line([right, top, 0], [right, bot, 0]), RIGHT, buff=0.12, color=RED)
            cx = (vbrace.get_right()[0] + 6.6) / 2
            verdict = T("not tail-recursive", size=40, color=RED).move_to([cx, 0.55, 0])
            c.wait_until("not tail-recursive")
            self.play(GrowFromCenter(vbrace), FadeIn(verdict, shift=0.3 * LEFT),
                      run_time=min(1.2, 0.8 * c.until("cure")))
            c.wait_until("cure")
            cure = VGroup(T("the cure:", size=34, color=GREEN),
                          T("an accumulating argument", size=32, color=GREEN))
            cure.arrange(DOWN, buff=0.2).move_to([cx, -0.6, 0])
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in cure], lag_ratio=0.5),
                      run_time=min(1.6, 0.9 * c.remaining))
