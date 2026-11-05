"""Chapter 4, scene 4: making 43p, call by call. Clips c4.trace.1 – c4.trace.3.

Scene 2's setting returns: s2's till (till_chain / till_pointer copied from ch4_s2_idea, centred
(0, 0.85); s2 has it at y 1.8, but here the call line sits above it) and the current call as one line of
Code 40 across the top (left edge -6.1), rewritten token by token at each of the ten calls. The
answer row (Code 44, left edge -6.1, centre y -1.75) has the big GOLD amount counter (T 110 at
(5.0, -1.75), DIM "amount" above it) at its right. A skip: the head cell fades sliding left, `till`
moves one cell right. A use: a copy of the head disc drops into the row as a YELLOW `x ::`; the
counter rolls down. `change [1] 0` becomes the TEAL `[]`.
c4.trace.3: the till and call clear, the row rises to (left -4.6, centre y 1.85); DIM brace +
YELLOW "waiting" (ch1 take-trace style); DIM "not iterative", GOLD "one waiting cons per coin".
Then ch1's collapse: a copy born on the row below (DIM ⇒), the conses fire inside out under a
GREEN box into `[20; 20; 2; 1]`, OCaml's reply below, the GOLD sum beside the result, then the 99p call and reply.

STATUS: built; check clean apart from by-design dwell notes (the call line's quick trace steps,
the transient collapsing copy).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the coin and the till: copied from ch4_s2_idea (shared look), not imported ──
COIN_R = 0.42                # the coin disc reused by ch4-ch7 (copied from ch1_s1_hook)
COIN_LABEL = 34
TILL = [50, 20, 10, 5, 2, 1]
S = 0.85                     # till chain scale: six cells + [] = 12.1 wide
PITCH = (CELL + PTR_W + LINK) * S
TILL_Y = 0.85                # chain centre (s2 has 1.8; here the call line sits above it)


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def till_chain(values, scale=S):
    """The till: ConsChain(values) scaled `scale`; each cell's label is coin(v, r=COIN_R*scale)
    (the value stays size 34). Nil TEAL as in ConsChain. Centred on ORIGIN."""
    chain = ConsChain(values).scale(scale)
    for cell in chain.cells:
        cell.remove(cell.label)
        cell.label = coin(cell.value, r=COIN_R * scale).move_to(cell.box)
        cell.add(cell.label)
    return chain


def till_pointer(cell, name="till", length=0.75):
    """YELLOW Mono name above a cell with a short arrow down to its box."""
    tip = cell.box.get_top()
    lab = Mono(name, size=36, color=YELLOW).move_to(tip + UP * (length + 0.3))
    arr = Arrow(lab.get_bottom(), tip, buff=0.06, stroke_width=3, color=YELLOW,
                max_tip_length_to_length_ratio=0.35, tip_length=0.15)
    return VGroup(lab, arr)


# ── keyed code lines: every token has a key, so a rewrite can move token to token ─
CALLS = [([50, 20, 10, 5, 2, 1], 43), ([20, 10, 5, 2, 1], 43), ([20, 10, 5, 2, 1], 23),
         ([20, 10, 5, 2, 1], 3), ([10, 5, 2, 1], 3), ([5, 2, 1], 3), ([2, 1], 3), ([2, 1], 1),
         ([1], 1), ([1], 0)]
ANSWER = [20, 20, 2, 1]
CALL99 = "change [50; 20; 10; 5; 2; 1] 99"
REPLY99 = "- : int list = [50; 20; 20; 5; 2; 2]"

CALL_SIZE, CALL_LEFT, CALL_Y = 40, -6.1, 3.2
ROW_SIZE, ROW_LEFT, ROW_Y = 44, -6.1, -1.75
COUNTER_SIZE, COUNTER_POS = 110, np.array([5.0, ROW_Y, 0])
X0 = -4.6                          # left edge of the trace rows in c4.trace.3
A_Y = 1.85                         # centre of the pending row once it has risen
ROW_PITCH = 1.1
TOP_SIZE = 34                      # the replies and the 99p call
CALL99_BASE, REPLY99_BASE = -1.95, -2.8
ROLL = 0.35                        # the counter roll; stays under the "amount" label
SLIDE = 1.4                        # how far a skipped cell slides as it goes
DIM_OP = 0.35

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


def kcode(parts, size):
    """A Code from (text, key) parts; code.spans maps each key to its character span."""
    src, spans = "", {}
    for text, key in parts:
        if key is not None:
            spans[key] = (len(src), len(src) + len(text))
        src += text
    code = Code(src, size=size)
    code.spans = spans
    return code


def P(code, *keys):
    """The glyphs of the keyed tokens, as a fresh VGroup (in the order given)."""
    g = VGroup()
    for k in keys:
        g.add(*code._span(*code.spans[k]))
    return g


def token(code, key):
    a, b = code.spans[key]
    return code.src[a:b]


def call_parts(till, amt):
    off = len(TILL) - len(till)
    parts = [("change", "fn"), (" ", None), ("[", "lb")]
    for j, v in enumerate(till):
        parts.append((str(v), f"t{off + j}"))
        if j < len(till) - 1:
            parts += [(";", f"s{off + j}"), (" ", None)]
    return parts + [("]", "rb"), (" ", None), (str(amt), "amt")]


def row_parts(k, vals=ANSWER):
    """The answer row with k conses fired: k=0 `20 :: 20 :: 2 :: 1 :: []`, k=4 `[20; 20; 2; 1]`.
    A cons's `::` (key c_i) becomes the `;` after its value once it fires."""
    n = len(vals)
    parts = []
    for i in range(n - k):
        parts += [(str(vals[i]), f"n{i}"), (" ", None), ("::", f"c{i}"), (" ", None)]
    parts.append(("[", "lb"))
    for i in range(n - k, n):
        parts.append((str(vals[i]), f"n{i}"))
        if i < n - 1:
            parts += [(";", f"c{i}"), (" ", None)]
    return parts + [("]", "rb")]


def built_keys(k, n=len(ANSWER)):
    keys = ["lb"]
    for i in range(n - k, n):
        keys.append(f"n{i}")
        if i < n - 1:
            keys.append(f"c{i}")
    return keys + ["rb"]


def paint_row(code, k, n=len(ANSWER)):
    for i in range(n - k):
        P(code, f"n{i}", f"c{i}").set_color(YELLOW)
    P(code, *built_keys(k)).set_color(TEAL if k == 0 else GREEN)
    return code


def reply_code(vals):
    parts = [("- : int list =", "head"), (" ", None)] + row_parts(len(vals), vals)
    code = kcode(parts, TOP_SIZE)
    P(code, *built_keys(len(vals), len(vals))).set_color(GREEN)
    return code


# ── helpers from ch1_s3_trace (L3 ch4_s3_trace's), so the traces look the same ──
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


def implies():
    return MathTex(r"\Rightarrow", font_size=64, color=DIM)


def hbox(mob, color, center_y, height=0.74, pad=0.12, fill=0.18):
    """The P8 highlight box: thin stroke, faint fill, behind the text, fixed height."""
    r = Rectangle(width=mob.width + 2 * pad, height=height, stroke_color=color, stroke_width=2.5)
    r.set_fill(color, opacity=fill).set_z_index(-1)
    return r.move_to([mob.get_x(), center_y, 0])


def rt(c, cue, cap, floor=0.4, frac=0.9):
    """A run_time that ends before the cue."""
    return min(cap, max(floor, frac * c.until(cue)))


class Making43p(NarratedScene):
    def construct(self):
        self.build()
        # scene 2's setting comes back: the till and its pointer
        self.play(*[FadeIn(m) for m in self.till_parts], run_time=0.8)
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(2.8)          # the 99p reply gets its reading time
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── layout, built up front ────────────────────────────────────────────────
    def build(self):
        chain = till_chain(TILL).move_to([0, TILL_Y, 0])
        self.till = till_pointer(chain.cells[0])
        self.cells, self.arrows = list(chain.cells), list(chain.arrows)
        self.till_parts = [*self.cells, *self.arrows, chain.nil, self.till]

        self.counter = T("43", size=COUNTER_SIZE, color=GOLD).move_to(COUNTER_POS)
        self.amt_lab = T("amount", size=30, color=DIM).next_to(self.counter, UP, buff=0.6)  # s2/s6 label

        self.calls = [kcode(call_parts(t, a), CALL_SIZE) for t, a in CALLS]
        self.calls[0].move_to([0, CALL_Y, 0])
        base = baseline(self.calls[0])
        for code in self.calls:
            put(code, CALL_LEFT, base)
        self.call = self.calls[0]

        # the answer row, revealed piece by piece
        self.row = paint_row(kcode(row_parts(0), ROW_SIZE), 0).move_to([0, ROW_Y, 0])
        self.row.shift(RIGHT * (ROW_LEFT - self.row.get_left()[0]))
        self.pieces = [P(self.row, f"n{i}", f"c{i}") for i in range(len(ANSWER))]
        self.nil_piece = P(self.row, "lb", "rb")

        # c4.trace.3: the row rises; brace, labels, the collapsing copy, replies
        row = self.row
        self.rise = RIGHT * (X0 - row.get_left()[0]) + UP * (A_Y - row.get_y())
        base_a = baseline(row) + self.rise[1]
        y = row.get_bottom()[1] + self.rise[1]
        lx = P(row, "n0").get_left()[0] + self.rise[0]
        rx = P(row, "c3").get_right()[0] + self.rise[0]
        self.brace = span_brace(np.array([lx, y, 0]), np.array([rx, y, 0]), DOWN, color=DIM)
        self.waiting = T("waiting", size=34, color=YELLOW).next_to(self.brace, DOWN, buff=0.12)
        mid_x = X0 + row.width / 2
        ny = self.waiting.get_y() - 1.1
        self.notiter = T("not iterative", size=36, color=DIM).move_to([mid_x, ny, 0])
        self.space = T("one waiting cons per coin", size=36, color=GOLD).move_to([mid_x, ny - 0.7, 0])

        base_b = base_a - ROW_PITCH
        self.rowB = put(paint_row(kcode(row_parts(0), ROW_SIZE), 0), X0, base_b)
        self.u = [put(paint_row(kcode(row_parts(k), ROW_SIZE), k), X0, base_b) for k in (1, 2, 3, 4)]
        self.arrowB = implies().next_to(self.rowB, LEFT, buff=0.3).set_y(base_b + 0.14)
        self.box_y = self.rowB.get_y()

        self.reply = put(reply_code(ANSWER), X0, base_b - ROW_PITCH)
        self.check = MathTex("20", "+", "20", "+", "2", "+", "1", "=", "43",
                             font_size=52, color=GOLD)          # beside the GREEN result
        self.check.shift(RIGHT * (self.u[3].get_right()[0] + 0.8 - self.check.get_left()[0])
                         + UP * (base_b - self.check.get_bottom()[1]))

        self.call99 = put(Code(CALL99, size=TOP_SIZE), X0, CALL99_BASE)
        self.reply99 = put(Code(REPLY99, size=TOP_SIZE), X0, REPLY99_BASE)
        VGroup(*self.reply99.find("[50; 20; 20; 5; 2; 2]")).set_color(GREEN)

    # ── step pieces ───────────────────────────────────────────────────────────
    def rewrite(self, k):
        """Anims that rewrite the call line into call k, token by token, and the cleanup."""
        old, new = self.call, self.calls[k]
        anims, targets = [], []
        for key in old.spans:
            src = P(old, key)
            if key not in new.spans:
                anims.append(FadeOut(src, shift=0.5 * LEFT))
                continue
            t = P(new, key)
            if token(old, key) == token(new, key):
                anims.append(ReplacementTransform(src, t))
            else:                                    # the amount rolls down
                anims += [FadeOut(src, shift=0.4 * UP), FadeIn(t, shift=0.4 * UP)]
            targets.append(t)
        self.call = new

        def done():
            self.remove(old, *targets)
            self.add(new)
        return anims, done

    def step(self, anims, k=None, run_time=1.0, span=None):
        """Play anims plus (optionally) the rewrite to call k, which may run in a time span."""
        done = None
        if k is not None:
            more, done = self.rewrite(k)
            if span is not None:
                more = [time_span(a, *span) for a in more]
            anims = list(anims) + more
        self.play(*anims, run_time=run_time)
        if done:
            done()

    def skip(self, i):
        """The head cell fades sliding off left; `till` moves on to the next cell."""
        return [FadeOut(self.cells[i], shift=SLIDE * LEFT),
                FadeOut(self.arrows[i], shift=SLIDE * LEFT),
                self.till.animate.shift(RIGHT * PITCH)]

    def drop(self, i, slot):
        """A copy of cell i's disc drops into the answer row as a YELLOW `x ::`."""
        return FadeTransform(self.cells[i].label.copy(), self.pieces[slot], stretch=False)

    def tick(self, v):
        new = T(str(v), size=COUNTER_SIZE, color=GOLD).move_to(COUNTER_POS)
        anims = [FadeOut(self.counter, shift=ROLL * UP), FadeIn(new, shift=ROLL * UP)]
        self.counter = new
        return anims

    # ── c4.trace.1: skip 50, use 20, use 20 again ─────────────────────────────
    def clip1(self):
        with self.say("c4.trace.1") as c:
            # "Let's make change for forty-three."
            self.play(FadeIn(self.call, shift=0.3 * DOWN), run_time=1.0)
            self.play(TransformFromCopy(P(self.call, "amt"), self.counter),
                      FadeIn(self.amt_lab, shift=0.2 * DOWN), run_time=rt(c, "fifty", 1.2, 0.6, 1.0))

            # "Forty-three is less than fifty,"
            c.wait_until("fifty")
            self.play(FlashAround(self.counter, color=GOLD, time_width=1.5),
                      run_time=rt(c, "less than fifty", 1.0, 0.5))
            c.wait_until("less than fifty")
            self.play(FlashAround(self.cells[0].label, color=RED, time_width=1.5),
                      run_time=rt(c, "the fifty goes", 1.0, 0.5))
            # "so the fifty goes, and we carry on with the rest of the till."
            c.wait_until("the fifty goes")
            self.step(self.skip(0), run_time=rt(c, "carry on", 1.5, 0.8))
            c.wait_until("carry on")
            self.step([], 1, run_time=1.5)

            # "Twenty fits."
            c.wait_until("twenty fits")
            self.play(FlashAround(self.cells[1].label, color=GREEN, time_width=1.5),
                      run_time=rt(c, "answer starts", 1.2, 0.6))
            # "So the answer starts with twenty,"
            c.wait_until("answer starts")
            self.play(self.drop(1, 0), run_time=rt(c, "consed onto", 1.5, 0.8))
            # "consed onto the change for twenty-three,"
            c.wait_until("consed onto")
            self.step(self.tick(23), 2, run_time=rt(c, "still at the front", 1.5, 0.8))
            # "with twenty still at the front of the till."
            c.wait_until("still at the front")
            self.play(FlashAround(self.cells[1], color=YELLOW, time_width=1.5),
                      run_time=rt(c, "fits again", 1.5, 0.6))

            # "Twenty fits again, and three is left."
            c.wait_until("fits again")
            self.step([self.drop(1, 1)] + [time_span(a, 0.4, 1.4) for a in self.tick(3)], 3,
                      run_time=min(1.4, c.remaining), span=(0.4, 1.4))

    # ── c4.trace.2: skip 20, 10, 5; use 2; skip 2; use 1; nil ──────────────────
    def clip2(self):
        with self.say("c4.trace.2") as c:
            # "Three is less than twenty, less than ten, and less than five,"
            cues = ["than twenty", "than ten", "than five", "one call each"]
            for j, (i, k) in enumerate([(1, 4), (2, 5), (3, 6)]):
                c.wait_until(cues[j])
                self.step(self.skip(i), k, run_time=rt(c, cues[j + 1], 0.9 if j == 0 else 0.8, 0.5))
            # "so those coins go, one call each."
            c.wait_until("one call each")
            self.play(FlashAround(self.call, color=YELLOW, time_width=1.5),
                      run_time=rt(c, "two fits", 1.2, 0.6))

            # "Two fits, and one is left."
            c.wait_until("two fits")
            self.play(FlashAround(self.cells[4].label, color=GREEN, time_width=1.5),
                      self.drop(4, 2), run_time=rt(c, "one is left", 1.3, 0.7))
            c.wait_until("one is left")
            self.step(self.tick(1), 7, run_time=rt(c, "too large", 1.0, 0.6))

            # "Now two is too large, so it goes too."
            c.wait_until("too large")
            self.play(FlashAround(self.cells[4].label, color=RED, time_width=1.5),
                      run_time=rt(c, "it goes", 0.9, 0.5))
            c.wait_until("it goes")
            self.step(self.skip(4), 8, run_time=rt(c, "one fits", 1.0, 0.6))

            # "One fits, and zero is left."
            c.wait_until("one fits")
            self.play(FlashAround(self.cells[5].label, color=GREEN, time_width=1.5),
                      self.drop(5, 3), run_time=rt(c, "zero is left", 1.3, 0.7))
            c.wait_until("zero is left")
            self.step(self.tick(0), 9, run_time=rt(c, "change for zero", 1.0, 0.6))

            # "And change for zero is nil."  The last call becomes the TEAL [].
            c.wait_until("change for zero")
            self.play(FadeTransform(self.call.copy(), self.nil_piece, stretch=False),
                      run_time=rt(c, "nil", 1.5, 0.8))
            c.wait_until("nil")
            self.play(FlashAround(self.nil_piece, color=TEAL, time_width=1.5), run_time=1.0)
        # the row is whole: one Code again
        self.remove(*self.pieces, self.nil_piece)
        self.add(self.row)

    # ── c4.trace.3: the waiting conses, the collapse, the reply, 99p ──────────
    def clip3(self):
        row = self.row
        with self.say("c4.trace.3") as c:
            # "Look at what has piled up."  The till and the call clear; the row rises.
            sweep_clear(self, time_span(row.animate.shift(self.rise), 0.2, 1.4),
                        time_span(GrowFromCenter(self.brace), 1.1, 1.8),
                        time_span(FadeIn(self.waiting, shift=0.3 * DOWN), 1.2, 1.9),
                        keep=[row], run_time=min(1.9, c.until("a twenty")))

            # "A twenty, another twenty, a two and a one, each waiting to be consed on"
            cues = ["a twenty", "another twenty", "a two", "a one"]
            c.wait_until(cues[0])
            t0 = c.at(cues[0])
            offs = [max(0.0, c.at(q) - t0) for q in cues]
            self.play(*[time_span(FlashAround(P(row, f"n{i}", f"c{i}"), color=YELLOW,
                                              time_width=1.5), o, o + 1.0)
                        for i, o in enumerate(offs)], run_time=offs[-1] + 1.0)

            # "So change is not iterative."
            c.wait_until("notiter")
            self.play(FadeIn(self.notiter, shift=0.3 * DOWN), run_time=1.0)

            # "Like take, it holds one waiting cons for every coin it hands over."
            c.wait_until("space")
            self.play(FadeIn(self.space, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("every coin")
            self.play(*[time_span(FlashAround(P(row, f"n{i}", f"c{i}"), color=GOLD,
                                              time_width=1.5), 0.25 * i, 0.25 * i + 0.9)
                        for i in range(4)], run_time=rt(c, "fire", 1.65, 0.8, 1.0))

            # "Now the conses happen, from the inside out,"
            c.wait_until("fire")
            ubox = hbox(P(self.rowB, "n3", "c3", "lb", "rb"), GREEN, self.box_y)
            self.play(FadeOut(self.brace), FadeOut(self.waiting),
                      TransformFromCopy(row, self.rowB), FadeIn(self.arrowB, shift=0.2 * DOWN),
                      time_span(FadeIn(ubox), 0.6, 0.9), run_time=0.9)
            budget = c.until("answer") + 1.4
            src = self.rowB
            for k, frac in enumerate([0.3, 0.25, 0.22, 0.23]):
                dst = self.u[k]
                anims, targets = [], []
                for key in src.spans:
                    s = P(src, key)
                    if key in dst.spans:
                        t = P(dst, key)
                        anims.append(ReplacementTransform(s, t))
                        targets.append(t)
                    else:
                        anims.append(FadeOut(s))
                anims.append(ubox.animate.become(hbox(P(dst, *built_keys(k + 1)), GREEN,
                                                      self.box_y)))
                self.play(*anims, run_time=max(0.5, frac * budget))
                self.remove(src, *targets)
                self.add(dst)
                src = dst

            # "and out comes twenty, twenty, two, one."  OCaml agrees.
            final = self.u[3]
            rep = self.reply
            val, head = P(rep, *built_keys(4)), P(rep, "head")
            self.play(FlashAround(final, color=GREEN, time_width=1.5), FadeOut(ubox),
                      time_span(FadeOut(self.notiter), 0, 0.6),
                      time_span(FadeOut(self.space), 0, 0.6),
                      time_span(TransformFromCopy(P(final, *built_keys(4)), val), 0.3, 1.4),
                      time_span(FadeIn(head, shift=0.2 * LEFT), 0.5, 1.4),
                      run_time=min(1.4, max(0.8, c.until("check") - 0.1)))
            self.remove(val, head)
            self.add(rep)

            # "That adds up to forty-three."  The result's values become the GOLD sum.
            c.wait_until("check")
            chk = self.check
            src_keys = ["n0", "c0", "n1", "c1", "n2", "c2", "n3"]
            anims = [TransformFromCopy(P(final, key), chk[j]) for j, key in enumerate(src_keys)]
            anims += [time_span(FadeIn(chk[7], shift=0.2 * LEFT), 0.8, 1.5),
                      time_span(FadeIn(chk[8], shift=0.2 * LEFT), 0.9, 1.5)]
            self.play(*anims, run_time=1.5)
            self.remove(*chk)
            self.add(chk)

            # "Try ninety-nine pence instead,"
            c.wait_until("ninety")
            self.play(*[m.animate.set_opacity(DIM_OP) for m in (row, self.arrowB, final)],
                      time_span(FadeIn(self.call99, shift=0.3 * DOWN), 0.2, 1.2),
                      run_time=rt(c, "nn", 1.2, 0.8, 1.0))
            # "and you get fifty, twenty, twenty, five, two, two."
            c.wait_until("nn")
            self.play(FadeIn(self.reply99, shift=0.3 * DOWN), run_time=1.2)
