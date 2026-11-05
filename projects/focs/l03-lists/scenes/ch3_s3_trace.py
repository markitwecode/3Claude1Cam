"""STATUS: all 4 clips built; check clean (70.1 s vs 66.4 s narration). Fix passes done: trace.3
overrun (final flash takes what is left of the clip); trace.4 composition (both columns centred on
y=0, dimmed trace fitted beside the calls at ~0.76 scale, final "3" at full opacity).
known issues: trace.1-3 frame is top-heavy (content in the upper 2/3); trace.4 uses gap=1.7 so the last reply
gets its reading time (end-of-scene hold).

Chapter 3, scene 3: nlength [a; b; c] traced by hand. The expression grows a staircase of
waiting "1 +"s (each row born from the row above, the new "1 +" from the code's own clause),
then unwinds in place from the inside out; OCaml confirms.

Clips c3.trace.1 - c3.trace.4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

NLENGTH = """
let rec nlength = function
  | [] -> 0
  | x :: xs -> 1 + nlength xs
"""
ROWS = ["nlength [a; b; c]", "1 + nlength [b; c]", "1 + (1 + nlength [c])",
        "1 + (1 + (1 + nlength []))", "1 + (1 + (1 + 0))"]
CALLS = ["nlength [a; b; c]", "nlength [b; c]", "nlength [c]", "nlength []", "0"]
UNWIND = ["1 + (1 + 1)", "1 + 2", "3"]

SIZE = 40                           # trace rows (the hero): the widest row spans ~66% of the frame
BASE = [1.1, 0.25, -0.6, -1.45, -2.3]   # baseline of each trace row
ARROW_GAP = 0.3
DIMMED = 0.35

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ+-=:")


# ── helpers (local to this scene) ───────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph (or as a fresh VGroup used only as a transform
# target, removed again right after): wrapping on-screen glyphs in a group that play() adds
# would pull them out of their Code (LESSONS.md).
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
    """3b1b's highlight box (PATTERNS P8): thin stroke, faint fill, behind the text, with a
    fixed height so it keeps its shape as it slides from term to term."""
    r = Rectangle(width=mob.width + 2 * pad, height=height, stroke_color=color, stroke_width=2.5)
    r.set_fill(color, opacity=fill).set_z_index(-1)
    return r.move_to([mob.get_x(), center_y, 0])


def under(glyphs, base, color=YELLOW):
    """The yellow underline of one waiting "1 +" (v1's pending_line, one per addition)."""
    y = base - 0.13
    return Line([glyphs.get_left()[0], y, 0], [glyphs.get_right()[0], y, 0],
                color=color, stroke_width=5)


class WatchingItRun(NarratedScene):
    def construct(self):
        self.setup_layout()
        self.first_step()     # c3.trace.1
        self.down_to_nil()    # c3.trace.2
        self.unwind()         # c3.trace.3
        self.check()          # c3.trace.4
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.1)  # a truly empty last frame

    # ── layout, built up front (P4) ────────────────────────────────────────────
    def setup_layout(self):
        self.code = Code(NLENGTH, size=30).move_to([0, 2.8, 0])
        rows = [Code(s, size=SIZE) for s in ROWS]
        widest = rows[3].width + implies().width + ARROW_GAP
        self.x0 = -widest / 2 + implies().width + ARROW_GAP    # left edge of every row's code
        for r, b in zip(rows, BASE):
            put(r, self.x0, b)
        self.rows = rows
        self.arrows = [None] + [implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + 0.13)
                                for r, b in zip(rows[1:], BASE[1:])]
        # vertical centre of a row's highlight box (rows with brackets/parens all agree)
        self.box_dy = rows[0].get_y() - BASE[0]
        # the waiting "1 +"s: k underlines in row k (3 in the last row)
        self.segs = [[under(G(r, "1 +", j), b) for j in range(min(k, 3))]
                     for k, (r, b) in enumerate(zip(rows, BASE))]

    def call_box(self, k):
        return hbox(G(self.rows[k], CALLS[k]), BLUE, BASE[k] + self.box_dy)

    def clause_box(self, line):
        glyphs = self.code.line(line)
        y = self.code.line(line).get_y()
        return hbox(glyphs, BLUE, y, height=0.5, pad=0.14)

    def birth(self, k, copies, from_code, fades, run_time):
        """Row k+1 is born from row k (P11/P13): the parts it shares are copied down, the new
        "1 +" (or the 0) flies out of the code's clause (P5), the box rides onto the new call
        (P12) and the waiting "1 +"s get their underlines."""
        src, dst = self.rows[k], self.rows[k + 1]
        anims, targets = [], []
        for s_sub, s_nth, d_sub, d_nth in copies:
            t = G(dst, d_sub, d_nth)
            anims.append(TransformFromCopy(G(src, s_sub, s_nth), t))
            targets.append(t)
        c_sub, c_line, d_sub, d_nth = from_code
        t = G(dst, d_sub, d_nth)
        anims.append(TransformFromCopy(G(self.code, c_sub, line=c_line), t, path_arc=-0.6))
        targets.append(t)
        for d_sub, d_nth in fades:
            t = G(dst, d_sub, d_nth)
            anims.append(FadeIn(t, shift=0.2 * DOWN))
            targets.append(t)
        anims.append(FadeIn(self.arrows[k + 1], shift=0.2 * DOWN))
        anims.append(Transform(self.cbox, self.call_box(k + 1)))
        old, new = self.segs[k], self.segs[k + 1]
        for j, seg in enumerate(new):
            if j < len(old):
                anims.append(TransformFromCopy(old[j], seg))
            else:
                anims.append(Succession(Wait(run_time * 0.55), Create(seg, run_time=run_time * 0.45)))
        self.play(*anims, run_time=run_time)
        self.remove(*targets)
        self.add(dst)

    # trace.1: nlength [a; b; c]; head a, tail [b; c]; the second clause gives row 1
    def first_step(self):
        code, r0 = self.code, self.rows[0]
        b1 = Code("x  = a", size=32)
        b2 = Code("xs = [b; c]", size=32)
        put(b1, 3.0, BASE[0] + 0.32)
        put(b2, 3.0, BASE[0] - 0.3)

        with self.say("c3.trace.1") as c:
            # "Let's run en-length on a list of three elements, A, B, C."
            self.play(FadeIn(code, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("list")
            self.play(FadeIn(r0, shift=0.3 * DOWN), run_time=1.2)

            # "The list isn't empty."  The box marks the call being worked on.
            c.wait_until("s1")
            self.cbox = self.call_box(0)
            self.play(FadeIn(self.cbox), run_time=1.0)

            # "Its head is A,"  x = a, the name from the pattern, the value from the list (P5)
            c.wait_until("head")
            self.play(TransformFromCopy(G(code, "x", line=2), G(b1, "x")),
                      TransformFromCopy(G(r0, "a"), G(b1, "a")), FadeIn(G(b1, "=")), run_time=1.0)
            self.remove(*b1.text)
            self.add(b1)
            # "and its tail is B, C."
            c.wait_until("tail")
            self.play(TransformFromCopy(G(code, "xs", line=2), G(b2, "xs")),
                      TransformFromCopy(G(r0, "b; c"), G(b2, "b; c")),
                      FadeIn(G(b2, "=")), FadeIn(G(b2, "[")), FadeIn(G(b2, "]")), run_time=1.0)
            self.remove(*b2.text)
            self.add(b2)

            # "So the second clause applies,"
            c.wait_until("second clause")
            self.lbox = self.clause_box(2)
            self.play(FadeIn(self.lbox), run_time=1.0)

            # "and we get one, plus en-length of B, C."
            c.wait_until("one")
            self.birth(0, copies=[("nlength [", 0, "nlength [", 0), ("b; c]", 0, "b; c]", 0)],
                       from_code=("1 +", 2, "1 +", 0), fades=[], run_time=2.0)
        self.bindings = (b1, b2)

    # trace.2: the same step twice more, then nil and the first clause
    def down_to_nil(self):
        with self.say("c3.trace.2") as c:
            # "Same again."  The bindings belonged to the first call.
            self.play(FadeOut(self.bindings[0]), FadeOut(self.bindings[1]), run_time=1.0)

            # "B, C isn't empty, so en-length of B, C becomes one, plus en-length of C."
            c.wait_until("becomes")
            self.birth(1, copies=[("1 +", 0, "1 +", 0), ("nlength [", 0, "nlength [", 0), ("c]", 0, "c]", 0)],
                       from_code=("1 +", 2, "1 +", 1), fades=[("(", 0), (")", 0)], run_time=1.6)

            # "And en-length of C becomes one, plus en-length of nil."
            c.wait_until("becomes", nth=1)
            self.birth(2, copies=[("1 + (1 +", 0, "1 + (1 +", 0), ("nlength [", 0, "nlength [", 0),
                                  ("]", 0, "]", 0), (")", 0, ")", 1)],
                       from_code=("1 +", 2, "1 +", 2), fades=[("(", 1), (")", 0)], run_time=1.4)

            # "At last the list is empty."
            c.wait_until("empty")
            self.play(FlashAround(G(self.rows[3], "[]"), color=TEAL, time_width=1.5), run_time=1.2)
            # "The first clause applies,"
            c.wait_until("first clause")
            self.play(self.lbox.animate.become(self.clause_box(1)), run_time=1.0)
            # "and en-length of nil is zero."  The 0 comes out of the first clause.
            c.wait_until("en-length of nil")
            self.birth(3, copies=[("1 + (1 + (1 +", 0, "1 + (1 + (1 +", 0), ("))", 0, "))", 0)],
                       from_code=("0", 1, "0", 0), fades=[], run_time=1.3)

    # trace.3: nothing has been added yet; unwind the last row in place, inside out
    def unwind(self):
        r4 = self.rows[4]
        y_box = BASE[4] + self.box_dy
        segs4 = self.segs[4]
        waiting = T("waiting", size=34, color=YELLOW)
        waiting.next_to(VGroup(*segs4), DOWN, buff=0.3)
        upper = [m for k in range(4) for m in (self.rows[k], self.arrows[k], *self.segs[k]) if m is not None]
        u = [Code(s, size=SIZE) for s in UNWIND]
        for m in u:
            put(m, self.x0, BASE[4])

        with self.say("c3.trace.3") as c:
            # "Now look at what we've built."  The code and boxes step back; the staircase of
            # waiting additions flashes once, top to bottom.
            self.play(self.code.animate.set_opacity(DIMMED), FadeOut(self.lbox), FadeOut(self.cbox),
                      LaggedStart(*[FlashUnder(VGroup(*G(self.rows[k], "1 +", j)), color=YELLOW,
                                               time_width=1.5)
                                    for k in range(1, 5) for j in range(len(self.segs[k]))],
                                  lag_ratio=0.15), run_time=1.6)
            # "One plus, one plus, one plus zero."  One flash per spoken "one plus" (P6)
            for j in range(3):
                c.wait_until("one plus", nth=j)
                part = G(r4, "1 + 0") if j == 2 else G(r4, "1 +", j)
                self.play(FlashAround(part, color=YELLOW, time_width=1.5), run_time=0.9)

            # "Not a single addition has happened yet."  Spotlight on the last row (P9).
            c.wait_until("none")
            self.play(*[m.animate.set_opacity(DIMMED) for m in upper], run_time=1.2)
            # "Each of them was waiting for an answer from further down."
            c.wait_until("waiting")
            self.play(FadeIn(waiting, shift=0.25 * DOWN), run_time=1.0)

            # "Only now can they run, from the inside out."  A box lands on the innermost sum.
            c.wait_until("inside out")
            ubox = hbox(G(r4, "(1 + 0)"), GOLD, y_box)
            self.play(FadeIn(ubox), run_time=0.8)

            # "One plus zero is one."  (P12: the sum becomes its value; the box rides along)
            steps = [  # (source, target, prefix, inner, inner target (sub, nth), tail pairs)
                (r4, u[0], "1 + (1 +", "(1 + 0)", ("1", 2), [(")", 1, ")", 0)]),
                (u[0], u[1], "1 +", "(1 + 1)", ("2", 0), []),
                (u[1], u[2], None, "1 + 2", ("3", 0), []),
            ]
            cues = [("u1", "is one"), ("u2", "is two"), ("u3", "is three")]
            for i, ((src, dst, prefix, inner, (t_sub, t_nth), tails), (mark, said)) in enumerate(zip(steps, cues)):
                c.wait_until(mark)
                if i:   # "One plus one" / "And one plus two": the box widens onto the next sum
                    self.play(ubox.animate.become(hbox(G(src, inner), GOLD, y_box)), run_time=0.8)
                c.wait_until(said)
                anims, targets = [], []
                if prefix:
                    t = G(dst, prefix)
                    anims.append(ReplacementTransform(G(src, prefix), t))
                    targets.append(t)
                for s_sub, s_nth, d_sub, d_nth in tails:
                    t = G(dst, d_sub, d_nth)
                    anims.append(ReplacementTransform(G(src, s_sub, s_nth), t))
                    targets.append(t)
                t = G(dst, t_sub, t_nth)
                anims.append(ReplacementTransform(G(src, inner), t))
                targets.append(t)
                anims.append(ubox.animate.become(hbox(t, GOLD, y_box)))
                anims.append(Uncreate(segs4[2 - i]))
                if i == 2:
                    anims.append(FadeOut(waiting, shift=0.25 * DOWN))
                self.play(*anims, run_time=1.3)
                self.remove(*src.get_family(), *targets)
                self.add(dst)
            # the flash takes what is left of the clip (≤ 1.2 s) so the block never overruns
            self.play(FlashAround(u[2], color=GOLD, time_width=1.5),
                      run_time=max(0.8, min(1.2, c.remaining)))
        self.ubox = ubox
        self.rows[4] = u[2]
        self.segs[4] = []

    # trace.4: OCaml's own replies beside the (dimmed) trace
    def check(self):
        left, right, col_gap, cy = -6.55, 6.55, 0.9, 0.0   # frame margins, gap between columns
        qs = [Code("nlength []", size=36), Code("nlength [5; 6; 7]", size=36)]
        rs = [Code("- : int = 0", size=36), Code("- : int = 3", size=36)]
        calls = (qs[0], rs[0], qs[1], rs[1])
        for m, b in zip(calls, (1.35, 0.7, -0.6, -1.25)):
            put(m, 0, b)
        # the calls sit against the right margin, vertically centred on cy
        top, bot = max(m.get_top()[1] for m in calls), min(m.get_bottom()[1] for m in calls)
        xr = right - max(m.width for m in calls)
        for m in calls:
            m.shift(RIGHT * xr + UP * (cy - (top + bot) / 2))

        # the dimmed trace takes all the room left of them (≈ 0.76 of its trace.3 size), centred on cy
        parts = [m for k in range(5) for m in (self.rows[k], self.arrows[k], *self.segs[k]) if m is not None]
        whole = VGroup(*[m.copy() for m in parts])     # for the geometry only, never added
        about = whole.get_center()
        s = min(0.8, (xr - col_gap - left) / whole.width)
        shift = np.array([left - (about[0] - whole.width * s / 2), cy - about[1], 0])
        final3 = self.rows[4]

        with self.say("c3.trace.4", gap=1.7) as c:
            # "OCaml agrees."  The trace steps aside, dimmed (P9); the two questions arrive.
            c.wait_until("check")
            anims = [m.animate.scale(s, about_point=about).shift(shift).set_opacity(
                1 if m is final3 else 0.4) for m in parts]
            self.play(*anims, FadeOut(self.code), FadeOut(self.ubox),
                      LaggedStart(FadeIn(qs[0], shift=0.25 * DOWN), FadeIn(qs[1], shift=0.25 * DOWN),
                                  lag_ratio=0.3), run_time=1.2)
            # "En-length of nil is zero,"
            c.wait_until("c1")
            self.play(FadeIn(rs[0], shift=0.25 * DOWN), run_time=1.0)
            # "and en-length of five, six, seven is three."
            c.wait_until("c2")
            self.play(FadeIn(rs[1], shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("three")
            three = G(rs[1], "3")
            self.play(FlashAround(three, color=GOLD, time_width=1.5),
                      FlashAround(final3, color=GOLD, time_width=1.5), run_time=1.2)
