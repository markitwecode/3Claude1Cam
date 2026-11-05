"""Chapter 4, scene 3: tracing append [1; 2; 3] [4]. Clips c4.trace.1 - c4.trace.3.

The trace is a stack of lines in ch3_s3_trace's style (Code 40, pitch 0.85, DIM ⇒ column, rows
left-aligned, BLUE call box riding down, BLUE clause box): each line is born from copies of the
one above (the head flies to the front, the new `::` out of the step clause). The waiting conses
turn YELLOW; a copy of the last line collapses in place, inside out, into GREEN [1; 2; 3; 4].
Then: not iterative, the box scans the first arguments, a DIM inset of ch3's `1 + (1 + (1 + 0))`,
and the GOLD space cost.

STATUS: built; check clean apart from dwell notes on the in-place collapse (row 5 and
`1 :: (2 :: [3; 4])` are transient states; the voice says "Three onto four, then two, then one"
in ~2 s, and row 4 keeps the same text on screen throughout). 65.0 s vs 60.6 s narration
(2.4 s end hold for the GOLD cost label).
Layout for s5/s7: Code 40 rows, baselines 1.2 / 0.35 / -0.5 / -1.35 / -2.2 / -3.05 (pitch 0.85),
rows left-aligned with the widest row + ⇒ column centred, ⇒ = MathTex 64 DIM, gap 0.3, at
baseline + 0.13; clause lines Code 30 centred at y 2.8; BLUE hbox height 0.66 on the call.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

CLAUSES = "| [], ys    -> ys\n| x::xs, ys -> x :: append xs ys"
ROWS = ["append [1; 2; 3] [4]", "1 :: append [2; 3] [4]", "1 :: (2 :: append [3] [4])",
        "1 :: (2 :: (3 :: append [] [4]))", "1 :: (2 :: (3 :: [4]))", "1 :: (2 :: (3 :: [4]))"]
CALLS = ["append [1; 2; 3] [4]", "append [2; 3] [4]", "append [3] [4]", "append [] [4]", "[4]"]
FIRST = ["[1; 2; 3]", "[2; 3]", "[3]", "[]"]
UNWIND = ["1 :: (2 :: [3; 4])", "1 :: [2; 3; 4]", "[1; 2; 3; 4]"]
BUILT = ["[3; 4]", "[2; 3; 4]", "[1; 2; 3; 4]"]

SIZE = 40                                       # trace rows, as ch3_s3_trace
BASE = [1.2, 0.35, -0.5, -1.35, -2.2, -3.05]    # baseline of each trace row (pitch 0.85, as ch3)
ARROW_GAP = 0.3
CODE_DIM = 0.35

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ+-=:")


# ── helpers (ch3_s3_trace's, so the two traces look the same) ───────────────────
def baseline(code):
    """y of the text baseline of a Code."""
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE and ch not in "+-=:":
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def G(code, sub, nth=0, line=None):
    """The glyphs of `sub` in `code`, as a fresh VGroup."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def implies():
    return MathTex(r"\Rightarrow", font_size=64, color=DIM)


def hbox(mob, color, center_y, height=0.66, pad=0.12, fill=0.18):
    """The P8 highlight box: thin stroke, faint fill, behind the text, fixed height."""
    r = Rectangle(width=mob.width + 2 * pad, height=height, stroke_color=color, stroke_width=2.5)
    r.set_fill(color, opacity=fill).set_z_index(-1)
    return r.move_to([mob.get_x(), center_y, 0])


def slide_through(box, targets, run_time):
    """One box gliding through several positions in a single play (no Succession wrapper)."""
    states = [box.copy()] + [t.copy() for t in targets]
    n = len(targets)

    def update(m, a):
        x = a * n
        i = min(int(x), n - 1)
        m.interpolate(states[i], states[i + 1], smooth(x - i))

    return UpdateFromAlphaFunc(box, update, run_time=run_time)


class TracingAppend(NarratedScene):
    def construct(self):
        self.setup_layout()
        self.down_the_list()   # c4.trace.1
        self.unwind()          # c4.trace.2
        self.the_shape()       # c4.trace.3
        self.wait(2.4)         # the GOLD cost label gets its reading time
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── layout, built up front ────────────────────────────────────────────────
    def setup_layout(self):
        self.clauses = Code(CLAUSES, size=30).move_to([0, 2.8, 0])
        rows = [Code(s, size=SIZE) for s in ROWS]
        self.left = -(rows[3].width + implies().width + ARROW_GAP) / 2   # left of the ⇒ column
        self.x0 = self.left + implies().width + ARROW_GAP                # left edge of every row
        for r, b in zip(rows, BASE):
            put(r, self.x0, b)
            G(r, "[4]").set_color(TEAL)          # ys rides along untouched
        for j in range(3):                       # the copy that collapses has waiting conses too
            G(rows[5], f"{j + 1} ::").set_color(YELLOW)
        self.rows = rows
        self.arrows = [None] + [implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + 0.13)
                                for r, b in zip(rows[1:], BASE[1:])]
        self.box_dy = rows[0].get_y() - BASE[0]
        u = [Code(s, size=SIZE) for s in UNWIND]
        for k, m in enumerate(u):
            put(m, self.x0, BASE[5])
            G(m, BUILT[k]).set_color(GREEN)
            for j in range(2 - k):
                G(m, f"{j + 1} ::").set_color(YELLOW)
        self.u = u

    def box_y(self, k):
        return BASE[k] + self.box_dy

    def call_box(self, k):
        return hbox(G(self.rows[k], CALLS[k]), BLUE, self.box_y(k))

    def clause_box(self, line):
        glyphs = self.clauses.line(line)
        return hbox(glyphs, BLUE, glyphs.get_y(), height=0.5, pad=0.14)

    def birth(self, k, pairs, fades=(), run_time=1.5):
        """Row k+1 is born from row k: shared parts copied down, the head and the new `::`
        flying in on an arc, the call box riding onto the new call."""
        dst = self.rows[k + 1]
        anims, targets = [], []
        for src, d_sub, d_nth, arc in pairs:
            t = G(dst, d_sub, d_nth)
            anims.append(TransformFromCopy(src, t, path_arc=arc))
            targets.append(t)
        for d_sub, d_nth in fades:
            t = G(dst, d_sub, d_nth)
            anims.append(FadeIn(t, shift=0.2 * DOWN))
            targets.append(t)
        anims.append(FadeIn(self.arrows[k + 1], shift=0.2 * DOWN))
        anims.append(Transform(self.cbox, self.call_box(k + 1)))
        self.play(*anims, run_time=run_time)
        self.remove(*targets)
        self.add(dst)

    def step_cons(self):
        """The `::` of the step clause's answer, `x :: append xs ys`."""
        return G(self.clauses, "::", nth=1, line=1)

    # ── trace.1: down the first list, one head at a time ───────────────────────
    def down_the_list(self):
        r = self.rows
        with self.say("c4.trace.1") as c:
            # "Let's run it on one, two, three, with four."
            self.play(FadeIn(self.clauses, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("one two three")
            self.play(FadeIn(r[0], shift=0.3 * DOWN), run_time=min(1.2, 0.8 * c.until("s1")))

            # "The first list has a head, one."
            c.wait_until("s1")
            self.cbox = self.call_box(0)
            self.lbox = self.clause_box(1)
            self.play(FadeIn(self.cbox), FadeIn(self.lbox), run_time=0.8)
            c.wait_until("a head")
            self.play(FlashAround(G(r[0], "1"), color=YELLOW, time_width=1.5), run_time=1.2)

            # "So the answer is one, consed onto the append of two, three, with four."
            c.wait_until("so the answer")
            self.birth(0, [(G(r[0], "1"), "1", 0, -0.9),
                           (self.step_cons(), "::", 0, 0.6),
                           (G(r[0], "append ["), "append [", 0, 0),
                           (G(r[0], "2; 3]"), "2; 3]", 0, 0),
                           (G(r[0], "[4]"), "[4]", 0, 0)], run_time=2.0)

            # "Same again.  Two, consed onto the append of three, with four."
            c.wait_until("two consed")
            self.birth(1, [(G(r[1], "1 ::"), "1 ::", 0, 0),
                           (G(r[1], "2"), "2", 0, -0.9),
                           (self.step_cons(), "::", 1, 0.6),
                           (G(r[1], "append ["), "append [", 0, 0),
                           (G(r[1], "3]"), "3]", 0, 0),
                           (G(r[1], "[4]"), "[4]", 0, 0)],
                       fades=[("(", 0), (")", 0)], run_time=1.5)

            # "Then three, consed onto the append of nil, with four."
            c.wait_until("s3")
            self.birth(2, [(G(r[2], "1 :: (2 ::"), "1 :: (2 ::", 0, 0),
                           (G(r[2], "3"), "3", 0, -0.9),
                           (self.step_cons(), "::", 2, 0.6),
                           (G(r[2], "append ["), "append [", 0, 0),
                           (G(r[2], "]"), "]", 0, 0),
                           (G(r[2], "[4]"), "[4]", 0, 0),
                           (G(r[2], ")"), ")", 1, 0)],
                       fades=[("(", 1), (")", 0)], run_time=1.2)

            # "Now the first list is empty, so that append is just four."
            c.wait_until("empty")
            self.play(FlashAround(G(r[3], "[]"), color=TEAL, time_width=1.5),
                      Transform(self.lbox, self.clause_box(0)),
                      run_time=min(1.0, 0.9 * c.until("so that append")))
            c.wait_until("so that append")
            self.birth(3, [(G(r[3], "1 :: (2 :: (3 ::"), "1 :: (2 :: (3 ::", 0, 0),
                           (G(r[3], "[4]"), "[4]", 0, 0),
                           (G(r[3], "))"), "))", 0, 0)],
                       run_time=min(1.2, max(0.8, c.remaining - 0.5)))
            if c.remaining > 0.7:
                self.play(FlashAround(G(r[4], "[4]"), color=TEAL, time_width=1.5),
                          run_time=min(1.0, c.remaining))

    # ── trace.2: the waiting conses, then the collapse from the inside out ─────
    def unwind(self):
        r = self.rows
        r4, r5 = r[4], r[5]
        conses4 = [G(r4, f"{j + 1} ::") for j in range(3)]
        left = conses4[0].get_left()[0]
        right = conses4[2].get_right()[0]
        y = r4.get_bottom()[1]
        brace = span_brace(np.array([left, y, 0]), np.array([right, y, 0]), DOWN, color=DIM)
        waiting = T("waiting", size=34, color=YELLOW).next_to(brace, DOWN, buff=0.12)

        with self.say("c4.trace.2") as c:
            # "Look at what has piled up."  The code steps back; the staircase of waiting
            # conses turns YELLOW, row by row.
            anims = [self.clauses.animate.set_opacity(CODE_DIM), FadeOut(self.lbox), FadeOut(self.cbox)]
            for k in range(1, 5):
                for j in range(min(k, 3)):
                    for a in recolor(G(r[k], f"{j + 1} ::"), YELLOW):
                        anims.append(time_span(a, 0.3 * (k - 1), 0.3 * (k - 1) + 0.8))
            self.play(*anims, run_time=1.8)

            # "The one, the two and the three are each waiting to be consed on."  One flash
            # per spoken number; the brace and its label arrive with the first.
            c.wait_until("the one")
            offs = [0.0, c.at("the two") - c.at("the one"), c.at("the three") - c.at("the one")]
            anims = [time_span(GrowFromCenter(brace), 0, 0.9),
                     time_span(FadeIn(waiting, shift=0.3 * DOWN), 0.3, 1.2)]
            anims += [time_span(FlashAround(conses4[j], color=YELLOW, time_width=1.5),
                                offs[j], offs[j] + 0.9) for j in range(3)]
            self.play(*anims, run_time=max(1.3, min(offs[2] + 0.9, c.until("finally"))))

            # "Only now, with the first list used up, can the conses actually happen,
            #  from the inside out."
            c.wait_until("used up")
            self.play(FlashAround(G(r[3], "[]"), color=TEAL, time_width=1.5),
                      run_time=min(1.0, 0.9 * c.until("actually happen")))
            c.wait_until("actually happen")
            self.play(FadeOut(brace), FadeOut(waiting), TransformFromCopy(r4, r5),
                      FadeIn(self.arrows[5], shift=0.2 * DOWN),
                      run_time=min(1.4, 0.9 * c.until("inside out")))
            c.wait_until("inside out")
            ubox = hbox(G(r5, "(3 :: [4])"), GREEN, self.box_y(5))
            self.play(FadeIn(ubox), run_time=min(0.8, 0.9 * c.until("done")))

            # "Three onto four, then two, then one."  Each cons fires in place.
            u = self.u
            steps = [
                (r5, u[0], [("1 :: (2 ::", 0, "1 :: (2 ::", 0), ("3", 0, "3", 0), ("::", 2, ";", 0),
                            ("[", 0, "[", 0), ("4]", 0, "4]", 0), (")", 1, ")", 0)],
                 [("(", 1), (")", 0)]),
                (u[0], u[1], [("1 ::", 0, "1 ::", 0), ("2", 0, "2", 0), ("::", 1, ";", 0),
                              ("[", 0, "[", 0), ("3; 4]", 0, "3; 4]", 0)],
                 [("(", 0), (")", 0)]),
                (u[1], u[2], [("1", 0, "1", 0), ("::", 0, ";", 0), ("[", 0, "[", 0),
                              ("2; 3; 4]", 0, "2; 3; 4]", 0)], []),
            ]
            cues = ["done", "then two", "then one"]
            for i, (src, dst, pairs, gone) in enumerate(steps):
                c.wait_until(cues[i])
                nxt = c.until(cues[i + 1]) if i < 2 else c.until("answer")
                anims, targets = [], []
                for s_sub, s_nth, d_sub, d_nth in pairs:
                    t = G(dst, d_sub, d_nth)
                    anims.append(ReplacementTransform(G(src, s_sub, s_nth), t))
                    targets.append(t)
                for s_sub, s_nth in gone:
                    anims.append(FadeOut(G(src, s_sub, s_nth)))
                anims.append(ubox.animate.become(hbox(G(dst, BUILT[i]), GREEN, self.box_y(5))))
                self.play(*anims, run_time=min(1.2 if i == 0 else 1.0, max(0.6, 0.9 * nxt)))
                self.remove(*src.get_family(), *targets)
                self.add(dst)

            # "One, two, three, four."
            c.wait_until("answer")
            self.play(FlashAround(u[2], color=GREEN, time_width=1.5), FadeOut(ubox), run_time=1.5)
        self.rows[5] = u[2]

    # ── trace.3: not iterative; same shape as nlength; the space it costs ───────
    def the_shape(self):
        r = self.rows
        title = T("not iterative", size=48)
        title.move_to([self.left + title.width / 2, 3.05, 0])

        # the DIM inset: ch3_s3_trace's last row, small, with its pile of waiting "1 +"s
        inset_code = Code("1 + (1 + (1 + 0))", size=30)
        caption = T("nlength, last chapter", size=30, color=DIM)
        body = VGroup(caption, inset_code).arrange(DOWN, buff=0.22)
        frame = SurroundingRectangle(body, color=DIM, buff=0.2, corner_radius=0.12).set_stroke(width=2)
        inset = VGroup(frame, body)
        inset.move_to([6.55 - inset.width / 2, 3.45 - inset.height / 2, 0])
        inset_code.set_opacity(0.6)
        ib = baseline(inset_code)
        pluses = [G(inset_code, "1 +", j) for j in range(3)]
        unders = [Line([p.get_left()[0], ib - 0.09, 0], [p.get_right()[0], ib - 0.09, 0],
                       color=YELLOW, stroke_width=4) for p in pluses]

        cost = T("space: one per element of xs", size=36, color=GOLD)
        cost.move_to([6.55 - cost.width / 2, 0, 0])
        cost.shift(UP * (BASE[5] - cost.get_bottom()[1] + 0.02))
        conses4 = [G(r[4], f"{j + 1} ::") for j in range(3)]

        with self.say("c4.trace.3") as c:
            # "So append is not iterative."
            self.play(FadeOut(self.clauses), FadeIn(title, shift=0.3 * DOWN), run_time=1.0)

            # "It scans its first argument, sets up a string of conses, and only then does them."
            c.wait_until("scan")
            sbox = hbox(G(r[0], FIRST[0]), YELLOW, self.box_y(0))
            self.play(FadeIn(sbox), run_time=0.5)
            self.play(slide_through(sbox, [hbox(G(r[k], FIRST[k]), YELLOW, self.box_y(k))
                                           for k in range(1, 4)],
                                    run_time=min(2.1, max(0.9, 0.9 * c.until("sets up")))))
            c.wait_until("sets up")
            self.play(Transform(sbox, hbox(G(r[4], "1 :: (2 :: (3 ::"), YELLOW, self.box_y(4))),
                      run_time=min(1.2, 0.9 * c.until("only then")))
            c.wait_until("only then")
            self.play(Transform(sbox, hbox(r[5], GREEN, self.box_y(5))),
                      run_time=min(1.2, 0.9 * c.until("echo")))

            # "It's the same shape as the first length function from last chapter,
            #  with its pile of one-pluses."
            c.wait_until("echo")
            self.play(FadeOut(sbox), FadeIn(inset, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("pile")
            anims = [time_span(Create(u), 0.25 * j, 0.25 * j + 0.7) for j, u in enumerate(unders)]
            anims += [time_span(FlashUnder(conses4[j], color=YELLOW, time_width=1.5),
                                0.25 * j, 0.25 * j + 0.9) for j in range(3)]
            self.play(*anims, run_time=min(1.5, max(0.9, 0.9 * c.until("space"))))

            # "And those waiting conses take up space, one for each element of the first list."
            c.wait_until("space")
            self.play(FadeIn(cost, shift=0.3 * DOWN), run_time=0.9)
            c.wait_until("one for each")
            nums = [G(r[0], str(j + 1)) for j in range(3)]
            anims = []
            for j in range(3):
                for m in (conses4[j], nums[j]):
                    anims.append(time_span(FlashAround(m, color=GOLD, time_width=1.5),
                                           0.4 * j, 0.4 * j + 1.0))
            self.play(*anims, run_time=min(1.8, max(1.0, c.remaining)))
