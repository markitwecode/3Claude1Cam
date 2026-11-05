"""Chapter 1, scene 3: watching take run. Clips c1.trace.1 – c1.trace.3.

Opens on scene 2's last shot (take's code, Code 36 centred (0, 0.423), and its reply, Code 32
centred (-0.1, -1.886)). The code shrinks to the upper left and DIMs; the step line lights on
each step. The trace is a stack of rows in L3 ch4_s3_trace's style (Code 40, pitch 0.84, DIM ⇒
column, rows left-aligned), each born from copies of the row above; the count is GOLD and ticks
2 → 1 → 0; list elements FG. The waiting conses turn YELLOW; a copy of `3 :: 5 :: []` collapses
in place, inside out, into GREEN [3; 5], with OCaml's reply beside it. In c1.trace.3 the trace
slides left to make room: "not iterative", a DIM inset of append's trace row, the walk, and the
GOLD space cost.

STATUS: built; check clean apart from dwell notes on s2's reprised reply (fades as the clip
starts) and the transient copy `3 :: 5 :: []` that collapses in place (row 3 keeps that text).
65.5 s vs 58.9 s narration (0.8 s opening fade-in, 1.6 s hold for the GOLD cost, end on the code).

Layout for s4/s6: trace rows Code 40, baselines 0.1 / -0.74 / -1.58 / -2.42 / -3.26 (pitch 0.84),
rows left-aligned; ⇒ = MathTex 64 DIM, gap 0.3, at baseline + 0.13. In c1.trace.1–2 the ⇒ column
+ widest row is centred; from c1.trace.3 the ⇒ column's left edge is at x = -6.6.
End shot: take's code alone = Code(TAKE_SRC, 36) scaled by 28/36, left edge -6.6, top 3.55,
opacity 0.35.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TAKE_SRC = """let rec take i = function
  | [] -> []
  | x::xs ->
      if i > 0 then x :: take (i - 1) xs
      else []"""
TAKE_REPLY = "val take : int -> 'a list -> 'a list = <fun>"

# scene 2's last shot (from the s2 builder)
S2_CODE_SIZE = 36
S2_CODE_CENTER = (0.0, 0.423, 0)
S2_REPLY_SIZE = 32
S2_REPLY_CENTER = (-0.100, -1.886, 0)

# take's code in its upper-left spot (scene 4 opens from it)
CODE_SCALE = 28 / S2_CODE_SIZE
CODE_LEFT, CODE_TOP = -6.6, 3.55
CODE_DIM = 0.35

ROWS = ["take 2 [3; 5; 9; 4; 7]", "3 :: take 1 [5; 9; 4; 7]", "3 :: 5 :: take 0 [9; 4; 7]",
        "3 :: 5 :: []", "3 :: 5 :: []"]
FIRST = ["[3; 5; 9; 4; 7]", "[5; 9; 4; 7]", "[9; 4; 7]"]
UNWIND = ["3 :: [5]", "[3; 5]"]
BUILT = ["[5]", "[3; 5]"]
REPLY = "- : int list = [3; 5]"
APPEND_ROW = "1 :: (2 :: (3 :: append [] [4]))"

SIZE = 40
BASE = [0.1, -0.74, -1.58, -2.42, -3.26]
ARROW_GAP = 0.3
LEFT_END = -6.6          # left of the ⇒ column once the trace slides left (c1.trace.3)
UNSEEN = 0.3             # opacity of the 9, 4, 7 that take never looks at

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


# ── helpers (L3 ch4_s3_trace's, so the traces look the same) ────────────────────
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


def G(code, sub, nth=0, line=None):
    """The glyphs of `sub` in `code`, as a fresh VGroup."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def all_of(code, sub):
    """Every occurrence of `sub` in `code`, each as a VGroup of glyphs."""
    out, n = [], 0
    while True:
        try:
            out.append(G(code, sub, n))
        except ValueError:
            return out
        n += 1


def implies():
    return MathTex(r"\Rightarrow", font_size=64, color=DIM)


def hbox(mob, color, center_y, height=0.66, pad=0.12, fill=0.18):
    """The P8 highlight box: thin stroke, faint fill, behind the text, fixed height."""
    r = Rectangle(width=mob.width + 2 * pad, height=height, stroke_color=color, stroke_width=2.5)
    r.set_fill(color, opacity=fill).set_z_index(-1)
    return r.move_to([mob.get_x(), center_y, 0])


def slide_through(box, targets, run_time):
    """One box gliding through several positions in a single play."""
    states = [box.copy()] + [t.copy() for t in targets]
    n = len(targets)

    def update(m, a):
        x = a * n
        i = min(int(x), n - 1)
        m.interpolate(states[i], states[i + 1], smooth(x - i))

    return UpdateFromAlphaFunc(box, update, run_time=run_time)


def paint(row):
    """Trace colours: list elements FG, the count GOLD (`::` and `[]` TEAL from the highlighter)."""
    for d in "34579":
        for g in all_of(row, d):
            g.set_color(FG)
    for d in "012":
        for g in all_of(row, d):
            g.set_color(GOLD)
    return row


class WatchingTake(NarratedScene):
    def construct(self):
        self.build()
        # scene 2's last shot comes back where it left
        self.play(FadeIn(self.code), FadeIn(self.reply_s2), run_time=0.8)
        self.down_the_list()   # c1.trace.1
        self.unwind()          # c1.trace.2
        self.the_shape()       # c1.trace.3
        self.wait(1.6)         # the GOLD cost line gets its reading time
        # end on take's code alone, DIM, in its upper-left spot (scene 4 opens from it)
        sweep_clear(self, keep=[self.code], run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(self.code), run_time=1.0)
        self.wait(0.15)

    # ── layout, built up front ────────────────────────────────────────────────
    def build(self):
        self.code = Code(TAKE_SRC, size=S2_CODE_SIZE).move_to(S2_CODE_CENTER)
        self.reply_s2 = Code(TAKE_REPLY, size=S2_REPLY_SIZE).move_to(S2_REPLY_CENTER)
        t = self.code.copy().scale(CODE_SCALE)
        t.shift(RIGHT * (CODE_LEFT - t.get_left()[0]) + UP * (CODE_TOP - t.get_top()[1]))
        t.set_opacity(CODE_DIM)
        self.code.target = t

        rows = [paint(Code(s, size=SIZE)) for s in ROWS]
        aw = implies().width
        self.left = -(rows[2].width + aw + ARROW_GAP) / 2        # ⇒ column, centred layout
        self.x0 = self.left + aw + ARROW_GAP                     # left edge of every row
        for r, b in zip(rows, BASE):
            put(r, self.x0, b)
        for s in ("3 ::", "5 ::"):                               # the copy that collapses
            G(rows[4], s).set_color(YELLOW)
        self.rows = rows
        self.arrows = [None] + [implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + 0.13)
                                for r, b in zip(rows[1:], BASE[1:])]
        self.box_dy = rows[0].get_y() - BASE[0]

        u = [paint(Code(s, size=SIZE)) for s in UNWIND]
        for k, m in enumerate(u):
            put(m, self.x0, BASE[4])
            G(m, BUILT[k]).set_color(GREEN)
        G(u[0], "3 ::").set_color(YELLOW)
        self.u = u

        self.reply = Code(REPLY, size=32)
        put(self.reply, u[1].get_right()[0] + 0.7, BASE[4])
        G(self.reply, "[3; 5]").set_color(GREEN)

    def box_y(self, k):
        return BASE[k] + self.box_dy

    def light(self, line, op):
        """The step line of take's code brightening (op=1) or stepping back (op=CODE_DIM)."""
        return [g.animate.set_opacity(op) for g in self.code.line(line)]

    def birth(self, k, pairs, run_time=1.5):
        """Row k+1 is born from row k: shared parts copied down, the head and the new `::`
        flying in on an arc."""
        dst = self.rows[k + 1]
        anims, targets = [], []
        for src, d_sub, d_nth, arc in pairs:
            t = G(dst, d_sub, d_nth)
            anims.append(TransformFromCopy(src, t, path_arc=arc))
            targets.append(t)
        anims.append(FadeIn(self.arrows[k + 1], shift=0.2 * DOWN))
        self.play(*anims, run_time=run_time)
        self.remove(*targets)
        self.add(dst)

    def step_cons(self):
        """The `::` of take's step line, `x :: take (i - 1) xs`."""
        return G(self.code, "::", line=3)

    # ── trace.1: down the list, the count ticking ───────────────────────────────
    def down_the_list(self):
        r, code = self.rows, self.code
        with self.say("c1.trace.1") as c:
            # "Let's take two from our list, three, five, nine, four, seven."
            self.play(MoveToTarget(code), FadeOut(self.reply_s2), run_time=1.3)
            self.play(FadeIn(r[0], shift=0.3 * DOWN), run_time=1.0)

            # "The list has a head, three, and two is greater than zero."
            c.wait_until("s1")
            self.play(*self.light(3, 1.0), run_time=min(0.8, 0.9 * c.until("a head")))
            c.wait_until("a head")
            self.play(FlashAround(G(r[0], "3"), color=YELLOW, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("two is greater")))
            c.wait_until("two is greater")
            self.play(FlashAround(G(r[0], "2"), color=GOLD, time_width=1.5),
                      FlashAround(G(code, "i > 0", line=3), color=GOLD, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("so the answer")))

            # "So the answer is three, consed onto take one, of five, nine, four, seven."
            c.wait_until("so the answer")
            self.birth(0, [(G(r[0], "3"), "3", 0, -0.9),
                           (self.step_cons(), "::", 0, 0.6),
                           (G(r[0], "take"), "take", 0, 0),
                           (G(r[0], "2"), "1", 0, 0),
                           (G(r[0], "["), "[", 0, 0),
                           (G(r[0], "5; 9; 4; 7]"), "5; 9; 4; 7]", 0, 0)], run_time=2.0)

            # "Same again.  Keep the five, and take zero, of nine, four, seven."
            c.wait_until("s2")
            self.play(FlashUnder(G(code, "x :: take (i - 1) xs", line=3), color=YELLOW,
                                 time_width=1.5),
                      run_time=min(1.0, 0.9 * c.until("keep the five")))
            c.wait_until("keep the five")
            self.birth(1, [(G(r[1], "3 ::"), "3 ::", 0, 0),
                           (G(r[1], "5"), "5", 0, -0.9),
                           (self.step_cons(), "::", 1, 0.6),
                           (G(r[1], "take"), "take", 0, 0),
                           (G(r[1], "1"), "0", 0, 0),
                           (G(r[1], "["), "[", 0, 0),
                           (G(r[1], "9; 4; 7]"), "9; 4; 7]", 0, 0)], run_time=1.5)

            # "Now the count is zero, so that take gives nil, however much of the list is left."
            c.wait_until("s3")
            self.play(*self.light(3, CODE_DIM), *self.light(4, 1.0),
                      FlashAround(G(r[2], "0"), color=GOLD, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("so that take")))
            c.wait_until("so that take")
            self.birth(2, [(G(r[2], "3 :: 5 ::"), "3 :: 5 ::", 0, 0),
                           (G(r[2], "take 0 [9; 4; 7]"), "[]", 0, 0)],
                       run_time=min(1.3, 0.9 * c.until("however much")))
            c.wait_until("however much")
            self.play(*[g.animate.set_opacity(UNSEEN) for k in range(3)
                        for g in G(r[k], "9; 4; 7")],
                      run_time=min(1.2, max(0.5, c.remaining - 0.1)))

    # ── trace.2: the waiting conses, then the collapse from the inside out ─────
    def unwind(self):
        r = self.rows
        r3, r4 = r[3], r[4]
        piles = [G(r3, "3 ::"), G(r3, "5 ::")]
        y = r3.get_bottom()[1]
        brace = span_brace(np.array([piles[0].get_left()[0], y, 0]),
                           np.array([piles[1].get_right()[0], y, 0]), DOWN, color=DIM)
        waiting = T("waiting", size=34, color=YELLOW).next_to(brace, DOWN, buff=0.12)

        with self.say("c1.trace.2") as c:
            # "Look at what has piled up."  The conses turn YELLOW, row by row.
            anims = self.light(4, CODE_DIM)
            for k in (1, 2, 3):
                for s in (["3 ::"] if k == 1 else ["3 ::", "5 ::"]):
                    for a in recolor(G(r[k], s), YELLOW):
                        anims.append(time_span(a, 0.35 * (k - 1), 0.35 * (k - 1) + 0.8))
            anims += [time_span(GrowFromCenter(brace), 0.7, 1.5),
                      time_span(FadeIn(waiting, shift=0.3 * DOWN), 0.9, 1.8)]
            self.play(*anims, run_time=1.8)

            # "The three and the five are each waiting to be consed on."  One flash each.
            c.wait_until("the three")
            off = max(0.3, c.at("the five") - c.at("the three"))
            self.play(time_span(FlashAround(piles[0], color=YELLOW, time_width=1.5), 0, 1.0),
                      time_span(FlashAround(piles[1], color=YELLOW, time_width=1.5),
                                off, off + 1.0),
                      run_time=off + 1.0)

            # "Only now can those conses happen, from the inside out."
            c.wait_until("happen")
            self.play(FadeOut(brace), FadeOut(waiting), TransformFromCopy(r3, r4),
                      FadeIn(self.arrows[4], shift=0.2 * DOWN),
                      run_time=min(1.2, max(0.8, 0.9 * c.until("inside out"))))
            c.wait_until("inside out")
            ubox = hbox(G(r4, "5 :: []"), GREEN, self.box_y(4))
            self.play(FadeIn(ubox), run_time=min(0.8, 0.9 * c.until("five onto nil")))

            # "Five onto nil, then three onto that."  Each cons fires in place.
            u = self.u
            steps = [
                (r4, u[0], [("3 ::", 0, "3 ::", 0), ("5", 0, "5", 0),
                            ("[", 0, "[", 0), ("]", 0, "]", 0)], [("::", 1)]),
                (u[0], u[1], [("3", 0, "3", 0), ("::", 0, ";", 0),
                              ("[", 0, "[", 0), ("5]", 0, "5]", 0)], []),
            ]
            cues = ["five onto nil", "then three", "answer"]
            for i, (src, dst, pairs, gone) in enumerate(steps):
                c.wait_until(cues[i])
                anims, targets = [], []
                for s_sub, s_nth, d_sub, d_nth in pairs:
                    t = G(dst, d_sub, d_nth)
                    anims.append(ReplacementTransform(G(src, s_sub, s_nth), t))
                    targets.append(t)
                for s_sub, s_nth in gone:
                    anims.append(FadeOut(G(src, s_sub, s_nth)))
                anims.append(ubox.animate.become(hbox(G(dst, BUILT[i]), GREEN, self.box_y(4))))
                self.play(*anims, run_time=min(1.2, max(0.6, 0.85 * c.until(cues[i + 1]))))
                self.remove(*src.get_family(), *targets)
                self.add(dst)
            self.rows[4] = u[1]

            # "The answer is three, five."  OCaml agrees.
            c.wait_until("answer")
            rep = self.reply
            val = G(rep, "[3; 5]")
            head = G(rep, "- : int list =")
            self.play(FlashAround(u[1], color=GREEN, time_width=1.5), FadeOut(ubox),
                      time_span(TransformFromCopy(G(u[1], "[3; 5]"), val), 0.3, 1.5),
                      time_span(FadeIn(head, shift=0.2 * LEFT), 0.5, 1.5),
                      run_time=1.5)
            self.remove(val, head)
            self.add(rep)

    # ── trace.3: not iterative; append's shape; the space it costs ─────────────
    def the_shape(self):
        r, arrows = self.rows, self.arrows
        dx = LEFT_END - self.left
        moving = [*r, *arrows[1:], self.reply]

        title = T("not iterative", size=44)
        title.move_to([6.6 - title.width / 2, (BASE[0] + BASE[1]) / 2 + 0.25, 0])

        # where the rows will be once they slide left
        r3_right = r[3].get_right()[0] + dx
        inset_code = Code(APPEND_ROW, size=28)
        for j in range(3):
            G(inset_code, f"{j + 1} ::").set_color(YELLOW)
        G(inset_code, "[4]").set_color(TEAL)
        frame = SurroundingRectangle(inset_code, color=DIM, buff=0.15, corner_radius=0.1)
        frame.set_stroke(width=2)
        VGroup(inset_code, frame).move_to([6.6 - frame.width / 2,
                                           r[3].get_y() + 0.02, 0])
        inset_code.set_opacity(0.6)
        tag = T("last lecture", size=28, color=DIM)
        tag.next_to(frame, UP, buff=0.08).align_to(frame, RIGHT)
        assert frame.get_left()[0] > r3_right + 0.3, "inset crowds row 3"

        cost = T("space: one waiting cons per element taken", size=30, color=GOLD)
        cost.move_to([6.6 - cost.width / 2, 0, 0])
        cost.shift(UP * (BASE[3] - cost.get_bottom()[1] + 0.03))

        with self.say("c1.trace.3") as c:
            # "So take is not iterative."  The trace slides left to make room.
            self.play(*[m.animate.shift(dx * RIGHT) for m in moving],
                      time_span(FadeIn(title, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)

            # "It has the same shape as append, from last lecture."
            c.wait_until("echo")
            self.play(FadeIn(frame), FadeIn(inset_code), FadeIn(tag, shift=0.2 * DOWN),
                      run_time=min(1.0, 0.9 * c.until("last lecture")))
            c.wait_until("last lecture")
            self.play(FlashUnder(G(r[3], "3 :: 5 ::"), color=YELLOW, time_width=1.5),
                      FlashUnder(G(inset_code, "1 :: (2 :: (3 ::"), color=YELLOW, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("walks down")))

            # "It walks down the list, leaves a cons waiting at every step,
            #  and only then builds the answer."
            c.wait_until("walks down")
            box = hbox(G(r[0], FIRST[0]), BLUE, self.box_y(0))
            self.play(FadeIn(box), run_time=0.5)
            self.play(slide_through(box, [hbox(G(r[k], FIRST[k]), BLUE, self.box_y(k))
                                          for k in (1, 2)],
                                    run_time=min(1.6, max(0.8, 0.9 * c.until("leaves a cons")))))
            c.wait_until("leaves a cons")
            self.play(Transform(box, hbox(G(r[3], "3 :: 5 ::"), YELLOW, self.box_y(3))),
                      run_time=min(1.0, 0.9 * c.until("only then")))
            c.wait_until("only then")
            self.play(Transform(box, hbox(G(r[4], "[3; 5]"), GREEN, self.box_y(4))),
                      run_time=min(1.0, 0.9 * c.until("space")))

            # "Each of those waiting conses takes up space, one for every element taken."
            c.wait_until("space")
            self.play(FadeOut(box), FadeOut(frame), FadeOut(inset_code), FadeOut(tag),
                      FlashAround(G(r[3], "3 ::"), color=GOLD, time_width=1.5),
                      FlashAround(G(r[3], "5 ::"), color=GOLD, time_width=1.5),
                      time_span(FadeIn(cost, shift=0.3 * LEFT), 0.3, 1.2), run_time=1.6)
            # "We'll count that cost shortly."
