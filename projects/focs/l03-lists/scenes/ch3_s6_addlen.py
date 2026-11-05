"""Chapter 3, scene 6: the accumulator. addlen's code, the unnamed argument that `function`
introduces, its type in three pieces, the flat trace with a count box riding the chain,
nlength's staircase beside addlen's flat column, what "tail" means in tail-recursive, and
the costs.

Clips c3.acc.1 - c3.acc.6.

STATUS (done, check-clean): all six clips; beats image reviewed. Ends on addlen's definition
alone (addlen_code(ADDLEN, 40) at UP * 0.15, as in acc.1), then fades: ch3_s7_recap picks
it up from there.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import restyle, settle  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

ADDLEN = "let rec addlen n = function\n  | []    -> n\n  | x::xs -> addlen (n + 1) xs"
FLAT = ["addlen 0 [a; b; c]", "addlen 1 [b; c]", "addlen 2 [c]", "addlen 3 []", "3"]
GROW = ["nlength [a; b; c]", "1 + nlength [b; c]", "1 + (1 + nlength [c])",
        "1 + (1 + (1 + nlength []))", "1 + (1 + (1 + 0))"]
WAITING = {1: 1, 2: 2, 3: 3, 4: 3}     # how many "1 +"s are still waiting in each staircase row

S = 1.15            # chain scale: a, b, c and nil span ~60% of the frame width
DIM_TO = 0.25       # spotlight: everything else drops to this (PATTERNS P9)
CODE_SIZE = 40
GAP = 1.25          # room opened after `n` for the unnamed argument
TRACE_SIZE = 36     # the flat trace under the chain
CMP_SIZE = 30       # both traces side by side
CMP_PITCH = 0.62
CMP_BASE0 = 2.15    # baseline of the first row of each column
STAIR_LEFT = -5.75  # left edge of the staircase's code (its arrows sit left of it)
FLAT_LEFT = 1.75


# ── helpers (local to this scene) ───────────────────────────────────────────────
# Anything that animates part of a Code works on its glyphs one by one: wrapping them in a
# VGroup/AnimationGroup makes manim pull them out of the Code (LESSONS.md).
def addlen_code(src, size):
    """addlen's code: the count `n` in GOLD wherever it appears, the name in YELLOW."""
    code = Code(src, size=size)
    for m in re.finditer(r"\bn\b", code.src):
        code._span(m.start(), m.end()).set_color(GOLD)
    for m in re.finditer(r"\baddlen\b", code.src):
        code._span(m.start(), m.end()).set_color(YELLOW)
    return code


def highlight(mob, color, buff=0.08):
    """3b1b's highlight box (P8): thin stroke, faint fill, drawn behind the text."""
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.06, stroke_width=2)
    return box.set_fill(color, 0.18).set_z_index(-1)


def ghost(mob, color=TEAL, buff=0.1, dashes=22):
    return DashedVMobject(SurroundingRectangle(mob, buff=buff, corner_radius=0.08),
                          num_dashes=dashes).set_stroke(color, 3)


def per_glyph(glyphs, fn):
    return [fn(g.animate) for g in glyphs]


_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


def baseline(m):
    """y of the text baseline of a Code / Mono / T object."""
    src, glyphs = (m.src, m.text) if isinstance(m, Code) else (m.text, m)
    chars = [ch for ch in src if not ch.isspace()]
    for ch, g in zip(chars, glyphs):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return m.get_bottom()[1]


def put(m, left, base):
    """Move a text object so its left edge is at x=left and its baseline at y=base."""
    m.shift(RIGHT * (left - m.get_left()[0]) + UP * (base - baseline(m)))
    return m


def trace(srcs, left, base0, pitch, size):
    """Evaluation trace: rows of (⇒, Code), the code left-aligned at x=left."""
    rows = []
    for i, s in enumerate(srcs):
        code = put(Code(s, size=size), left, base0 - pitch * i)
        if i == 0:
            arrow = VectorizedPoint(code.get_left())      # the first row has no ⇒
        else:
            arrow = MathTex(r"\Rightarrow", font_size=size * 1.6, color=DIM)
            arrow.next_to(code, LEFT, buff=0.25).set_y(base0 - pitch * i + 0.0101 * size / 2)
        rows.append(VGroup(arrow, code))
    return rows


def waiting_lines(row, k, size):
    """YELLOW underlines under the k "1 +"s still waiting in a staircase row."""
    code = row[1]
    y = baseline(code) - 0.0101 * size * 0.55
    lines = []
    for j in range(k):
        g = code.find("1 +", nth=j)
        lines.append(Line([g.get_left()[0], y, 0], [g.get_right()[0], y, 0], color=YELLOW, stroke_width=4))
    return lines


def count_frame():
    return RoundedRectangle(width=1.0, height=0.82, corner_radius=0.12).set_stroke(GOLD, 3).set_fill(BG, 1)


def count_num(k):
    return Mono(str(k), size=40, color=GOLD)


def cost(big, word, color=GOLD):
    o = MathTex(big, font_size=52, color=color)
    w = T(word, size=34, color=color)
    g = VGroup(o, w).arrange(RIGHT, buff=0.22)
    w.align_to(o, DOWN).shift(UP * 0.07)
    return g


class TheAccumulator(NarratedScene):
    def construct(self):
        self.the_idea()          # acc.1
        self.unnamed_argument()  # acc.2
        self.flat_trace()        # acc.3
        self.side_by_side()      # acc.4
        self.which_tail()        # acc.5
        self.costs()             # acc.6
        # HANDOFF to ch3_s7_recap (it opens with the wrapper that calls addlen): the last picture
        # is addlen's definition alone, addlen_code(ADDLEN, 40) centred at UP * 0.15 (`addlen`
        # YELLOW, `n` GOLD), exactly as acc.1 first showed it; then the usual fade to empty.
        code = self.code
        code.restore()                      # acc.1's layout (acc.2 opened a slot in it)
        gone = list(self.mobjects)
        self.play(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.02),
                  time_span(FadeIn(code, shift=0.3 * UP), 0.6, 1.5), run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(code), run_time=0.8)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # ── acc.1: carry the count along; the code; n, its base case and its step ──────
    def the_idea(self):
        chain = ConsChain(["a", "b", "c"]).scale(S).move_to(DOWN * 0.55)
        cells, nil = chain.cells, chain.nil
        stops = [*cells, nil]
        top = cells[0].box.get_top()[1]
        tags = [Code("1 +", size=36).set_color(YELLOW).move_to([c.box.get_x(), top + 0.42, 0]) for c in cells]
        hover = lambda m: np.array([m.get_x() if m is nil else m.box.get_x(), top + 1.45, 0])  # noqa: E731
        frame = count_frame().move_to(hover(cells[0]))
        nums = [count_num(k) for k in range(4)]
        nums[0].move_to(frame)

        code = addlen_code(ADDLEN, CODE_SIZE).move_to(UP * 0.15)
        n0 = code.find(" n ", line=0)                 # the standalone n (not the one in "addlen")
        hl = highlight(n0, GOLD)
        so_far = T("count so far", size=32, color=GOLD).next_to(n0, UP, buff=0.42)

        with self.say("c3.acc.1") as c:
            # "Here's the idea."
            self.play(FadeIn(chain, shift=0.3 * UP), run_time=1.5)
            # "Instead of leaving each addition for later,"  (nlength's waiting additions, one per cell)
            c.wait_until("leaving")
            self.play(LaggedStart(*[FadeIn(t, shift=0.25 * DOWN) for t in tags], lag_ratio=0.3), run_time=1.4)
            # "we do it right away, and carry the running count along with us."
            c.wait_until("now")
            self.play(FadeIn(frame, shift=0.25 * DOWN), FadeIn(nums[0], shift=0.25 * DOWN), run_time=0.8)
            for i in range(3):   # each addition is done as we pass its cell: the tag flies into the box
                dst = hover(stops[i + 1])
                nums[i + 1].move_to(dst)
                self.play(time_span(tags[i].animate.move_to(frame).scale(0.4).set_opacity(0), 0, 0.45),
                          time_span(frame.animate.move_to(dst), 0.35, 1.0),
                          time_span(ReplacementTransform(nums[i], nums[i + 1]), 0.3, 1.0), run_time=1.0)
                self.remove(tags[i])

            # "This is add-len."  The chain makes way; the count waits above the code's n.
            c.wait_until("code")
            spot = n0.get_center() + UP * 0.95
            self.play(LaggedStart(*[FadeOut(m) for m in (*chain.arrows[::-1], *cells[::-1], nil)], lag_ratio=0.08),
                      FadeIn(code, shift=0.3 * UP), frame.animate.move_to(spot),
                      nums[3].animate.move_to(spot), run_time=1.6)
            code.save_state()   # the scene ends on this exact picture of the code (handoff to s7)

            # "Its first argument, en, is the count so far."  The count box becomes the highlight on n (P5).
            c.wait_until("n")
            n_copy = n0[0].copy()
            self.play(ReplacementTransform(frame, hl), FadeTransform(nums[3], n_copy),
                      FadeIn(so_far, shift=0.25 * DOWN), run_time=1.5)
            self.remove(n_copy)

            # "When the list runs out, en has counted every element, so the answer is simply en."
            c.wait_until("nil")
            self.play(hl.animate.become(highlight(code.find("[]    -> n", line=1), GOLD)), run_time=1.2)
            c.wait_until("simply")
            n1 = code.find("n", line=1)
            self.play(FlashAround(n1, color=GOLD, time_width=1.5), run_time=1.2)

            # "Otherwise, we ignore the head, add one to en, and carry on down the tail."
            c.wait_until("ignore")
            x = code.find("x", line=2)
            self.play(hl.animate.become(highlight(code.find("x::xs", line=2), BLUE)),
                      *per_glyph(x, lambda a: a.set_opacity(0.3)), run_time=1.0)
            c.wait_until("add one")
            self.play(hl.animate.become(highlight(code.find("(n + 1)", line=2), GOLD)), run_time=0.9)
            c.wait_until("carry on")
            self.play(FlashAround(code.find("xs", line=2, nth=1), color=BLUE, time_width=1.5), run_time=1.0)
        self.code, self.hl, self.so_far = code, hl, so_far

    # ── acc.2: where's the list? `function`'s unnamed argument; the type in three pieces ──
    def unnamed_argument(self):
        code, hl = self.code, self.hl
        n0 = code.find(" n ", line=0)
        rest0 = code.find("= function", line=0)

        with self.say("c3.acc.2") as c:
            # "Add-len names only one argument, en."
            c.wait_until("one argument")
            self.play(hl.animate.become(highlight(n0, GOLD)), run_time=1.0)

            # "So where's the list?"  A slot opens after n: an argument with no name yet.
            c.wait_until("where's")
            self.play(FadeOut(self.so_far), *per_glyph(rest0, lambda a: a.shift(RIGHT * GAP)), run_time=1.2)
            eq = code.find("=", line=0)
            slot_c = np.array([(n0.get_right()[0] + eq.get_left()[0]) / 2, n0.get_y(), 0])
            frame = DashedVMobject(RoundedRectangle(width=GAP - 0.4, height=0.66, corner_radius=0.1),
                                   num_dashes=18).set_stroke(TEAL, 3).move_to(slot_c)
            frame.align_to(code.line(0), DOWN).shift(DOWN * 0.08)
            q = T("?", size=44, color=TEAL).move_to(frame)
            self.play(Create(frame), FadeIn(q, scale=0.6), run_time=1.0)

            # "Remember that the word function introduces an argument of its own."
            c.wait_until("function")
            fn = code.find("function", line=0)
            self.play(hl.animate.become(highlight(fn, BLUE)), FlashAround(fn, color=BLUE, time_width=1.5),
                      run_time=1.2)
            c.wait_until("introduces")
            arc = CurvedArrow(fn.get_top() + UP * 0.12, frame.get_top() + UP * 0.1, angle=TAU / 5,
                              color=BLUE, stroke_width=3, tip_length=0.18)
            self.play(Create(arc), run_time=1.4)

            # "That argument has no name."
            c.wait_until("has no name")
            unnamed = T("unnamed argument", size=32, color=TEAL)
            unnamed.next_to(arc, UP, buff=0.12).set_x(frame.get_x() + 0.6)
            self.play(FadeIn(unnamed, shift=0.25 * DOWN), run_time=1.0)

            # "Instead, it's matched straight away against the patterns underneath."
            c.wait_until("matched")
            pats = [ghost(code.find("[]", line=1)), ghost(code.find("x::xs", line=2))]
            self.play(FadeOut(hl),
                      LaggedStart(*[TransformFromCopy(frame, p, path_arc=PI / 3) for p in pats], lag_ratio=0.4),
                      run_time=2.0)

            # "Here, that's what breaks open the list."
            c.wait_until("here")
            self.play(FlashAround(code.find("x::xs", line=2), color=TEAL, time_width=1.5),
                      *per_glyph(code.find("::", line=2), lambda a: a.scale(1.25)), run_time=1.2)
            self.play(*per_glyph(code.find("::", line=2), lambda a: a.scale(1 / 1.25)), run_time=0.6)

            # "So add-len really takes two arguments,"  ...the block rises to make room for the type
            c.wait_until("two arguments")
            block = [code, frame, q, arc, unnamed, *pats]
            lift = UP * 0.85
            self.play(FlashAround(n0, color=GOLD, time_width=1.5), FlashAround(frame, color=TEAL, time_width=1.5),
                      *[m.animate.shift(lift) for m in block], run_time=1.4)

            # "and OCaml gives its type as int to alpha list to int."
            reply = Code("val addlen : int -> 'a list -> int = <fun>", size=30)
            reply.next_to(code, DOWN, buff=0.65)
            c.wait_until("ocaml")
            self.play(FadeIn(reply, shift=0.25 * DOWN), run_time=1.0)

            # the type splits into its three pieces (copies, so the reply stays whole)
            pieces = VGroup(Code("int", size=40), Code("->", size=40), Code("'a list", size=40),
                            Code("->", size=40), Code("int", size=40)).arrange(RIGHT, buff=0.75)
            pieces.next_to(reply, DOWN, buff=0.65)
            for p in (pieces[1], pieces[3]):
                p.set_color(DIM)
            sources = [reply.find("int", nth=0), reply.find("->", nth=0), reply.find("'a list"),
                       reply.find("->", nth=1), reply.find("int", nth=1)]
            c.wait_until("int")
            self.play(*[TransformFromCopy(s, p) for s, p in zip(sources, pieces)], run_time=1.6)
            settle(self, pieces)   # the pieces arrived one by one: put them back in their group

            labels = ["the count", "any list", "the length"]
            braces, labs = [], []
            for p, text in zip((pieces[0], pieces[2], pieces[4]), labels):
                b = Brace(p, DOWN, buff=0.12, color=DIM)
                braces.append(b)
                labs.append(T(text, size=34).next_to(b, DOWN, buff=0.14))
            # "First comes the count, an integer."
            c.wait_until("t1")
            self.play(GrowFromCenter(braces[0]), FadeIn(labs[0], shift=0.25 * DOWN),
                      FlashAround(n0, color=GOLD, time_width=1.5), run_time=1.3)
            # "Then a list of any type, so add-len is polymorphic too."
            c.wait_until("t2")
            self.play(GrowFromCenter(braces[1]), FadeIn(labs[1], shift=0.25 * DOWN),
                      FlashAround(frame, color=TEAL, time_width=1.5), run_time=1.3)
            # "And out comes the length, another integer."
            c.wait_until("t3")
            self.play(GrowFromCenter(braces[2]), FadeIn(labs[2], shift=0.25 * DOWN), run_time=1.3)
        self.top_block = [code, frame, q, arc, unnamed, *pats, reply]
        self.type_row = [pieces, *braces, *labs]

    # ── acc.3: the flat trace, with the count box riding above the current cell ──────
    def flat_trace(self):
        chain = ConsChain(["a", "b", "c"]).scale(S).move_to(UP * 1.0)
        cells, nil = chain.cells, chain.nil
        stops = [*cells, nil]
        top = cells[0].box.get_top()[1]
        hover = lambda m: np.array([m.get_x() if m is nil else m.box.get_x(), top + 0.62, 0])  # noqa: E731
        frame = count_frame().move_to(hover(cells[0]))
        word = T("count", size=30, color=DIM).next_to(frame, UP, buff=0.12)
        nums = [count_num(k) for k in range(4)]
        nums[0].move_to(frame)
        rows = trace(FLAT, left=-2.6, base0=-0.35, pitch=0.72, size=TRACE_SIZE)
        rows[4][1].set_color(GOLD)

        def ride(i, run_time):
            """the count ticks i -> i+1 while the box moves on to the next stop; cell i dims"""
            dst = hover(stops[i + 1])
            nums[i + 1].move_to(dst)
            return [frame.animate.move_to(dst), word.animate.shift(dst - frame.get_center()),
                    ReplacementTransform(nums[i], nums[i + 1]),
                    cells[i].animate.set_opacity(DIM_TO), chain.arrows[i].animate.set_opacity(DIM_TO)]

        def write_row(i, pairs, fresh, run_time, extra=()):
            """Row i comes out of what is already on screen (P5): each (source, target glyphs)
            pair flies over as a copy, `fresh` glyphs fade in; then the copies give way to the
            row itself (nothing is faded out, nothing is left stacked)."""
            copies = [t.copy() for _, t in pairs]
            news = [m.copy() for m in fresh]
            self.play(*[TransformFromCopy(s, cp) for (s, _), cp in zip(pairs, copies)],
                      *[FadeIn(m, shift=0.2 * DOWN) for m in news], *extra, run_time=run_time)
            self.remove(*copies, *news)
            self.add(rows[i])

        def next_call(i, run_time, extra=()):
            """`addlen k [rest]` from the call above: the name and the list's tail carry down,
            the new count comes out of the count box."""
            arrow, code = rows[i]
            prev = rows[i - 1][1]
            _, k, lst = FLAT[i].split(" ", 2)
            pairs = [(prev.find("addlen"), code.find("addlen")), (nums[i], code.find(k)),
                     (prev.find("["), code.find("[")), (prev.find(lst[1:]), code.find(lst[1:]))]
            write_row(i, pairs, [arrow], run_time, extra)

        with self.say("c3.acc.3") as c:
            # "Let's watch it run, starting the count at zero."  The code goes; the type steps back.
            self.play(LaggedStart(*[FadeOut(m) for m in self.top_block], lag_ratio=0.06),
                      *[restyle(m, 0.3) for m in self.type_row],
                      time_span(FadeIn(chain, shift=0.3 * DOWN), 0.6, 1.6), run_time=1.6)
            c.wait_until("count")
            self.play(FadeIn(frame, shift=0.25 * DOWN), FadeIn(nums[0], shift=0.25 * DOWN),
                      FadeIn(word, shift=0.25 * DOWN), run_time=1.0)

            # "Add-len of zero, and A, B, C."  The 0 in the call comes out of the count box (P5).
            c.wait_until("s1")
            first = rows[0][1]
            write_row(0, [(nums[0], first.find("0"))], [first.find("addlen"), first.find("[a; b; c]")], 1.5)

            # "The list isn't empty, so we add one to the count, and move on to the tail."
            c.wait_until("isn't empty")
            self.play(FlashAround(cells[0], color=BLUE, time_width=1.5), run_time=1.1)
            c.wait_until("add one")
            one = count_num(1).move_to(frame)
            self.play(ReplacementTransform(nums[0], one), FlashAround(frame, color=GOLD, time_width=1.5), run_time=1.1)
            nums[0] = one
            c.wait_until("move on")
            nums[1] = one   # already ticked: just ride on to b
            dst = hover(cells[1])
            self.play(frame.animate.move_to(dst), word.animate.shift(dst - frame.get_center()),
                      one.animate.move_to(dst), cells[0].animate.set_opacity(DIM_TO),
                      chain.arrows[0].animate.set_opacity(DIM_TO), run_time=1.3)

            # "That gives add-len of one, and B, C."  The call is rewritten from the one above.
            c.wait_until("s2")
            next_call(1, 1.6, [LaggedStart(*[FadeOut(m) for m in self.type_row], lag_ratio=0.1)])

            # "Then two, and C."  "Then three, and nil."  Quicker now (P24).
            for i, cue in ((1, "s3"), (2, "s4")):
                c.wait_until(cue)
                self.play(*ride(i, 1.0), run_time=1.0)
                next_call(i + 1, 1.1)

            # "Now the list is empty, so the answer is the count, three."
            c.wait_until("s5")
            self.play(FlashAround(nil, color=TEAL, time_width=1.5), run_time=1.1)
            c.wait_until("the answer")
            arrow4, three = rows[4]
            write_row(4, [(nums[3], three)], [arrow4], 1.5)
        self.chain_bits = [chain, frame, word, nums[3]]
        self.flat_rows = rows

    # ── acc.4: nlength's staircase beside addlen's flat column ─────────────────────
    def side_by_side(self):
        rows = self.flat_rows
        new_flat = trace(FLAT, left=FLAT_LEFT, base0=CMP_BASE0, pitch=CMP_PITCH, size=CMP_SIZE)
        new_flat[4][1].set_color(GOLD)
        stair = trace(GROW, left=STAIR_LEFT, base0=CMP_BASE0, pitch=CMP_PITCH, size=CMP_SIZE)
        unders = {i: waiting_lines(stair[i], k, CMP_SIZE) for i, k in WAITING.items()}
        name_y = CMP_BASE0 + 0.85
        stair_x = VGroup(*[r[1] for r in stair]).get_x()
        flat_x = VGroup(*[r[1] for r in new_flat]).get_x()
        names = [Code("nlength", size=36).set_color(YELLOW).move_to([stair_x, name_y, 0]),
                 Code("addlen", size=36).set_color(YELLOW).move_to([flat_x, name_y, 0])]

        # the shape of each column: the staircase's right edge marches out; the flat one doesn't
        pad = 0.18
        st_edge = VMobject().set_points_as_corners(
            [[stair[i][1].get_right()[0] + pad, baseline(stair[i][1]) + d, 0]
             for i in range(4) for d in (0.36, -0.14)])
        st_edge = DashedVMobject(st_edge, num_dashes=24).set_stroke(YELLOW, 3)
        fx = new_flat[0][1].get_right()[0] + pad
        fl_edge = DashedVMobject(Line([fx, baseline(new_flat[0][1]) + 0.36, 0],
                                      [fx, baseline(new_flat[3][1]) - 0.14, 0]), num_dashes=14).set_stroke(GREEN, 3)

        with self.say("c3.acc.4") as c:
            # "Now put the two traces side by side."  The chain goes; addlen's trace moves right.
            self.play(LaggedStart(*[FadeOut(m) for m in self.chain_bits], lag_ratio=0.1),
                      *[Transform(a, b) for a, b in zip(rows, new_flat)],
                      FadeIn(names[1], shift=0.25 * DOWN), run_time=1.6)

            # "En-length's expression grows longer at every step, as the additions pile up."
            c.wait_until("grows")
            self.play(FadeIn(names[0], shift=0.25 * DOWN), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r, shift=0.2 * RIGHT), *[Create(u) for u in unders.get(i, [])])
                                    for i, r in enumerate(stair)], lag_ratio=0.45), run_time=3.0)
            c.wait_until("pile up")
            self.play(Create(st_edge), run_time=1.0)

            # "Add-len's stays the same size."
            c.wait_until("flat")
            self.play(Create(fl_edge), run_time=1.0)

            # "Each call just hands over to the next call, with nothing left to do afterwards."
            c.wait_until("hand")
            hands = []
            for i in range(4):
                a, b = rows[i][1], rows[i + 1][1]
                x0 = fx + 0.15
                hands.append(CurvedArrow([x0, a.get_y() - 0.05, 0], [x0, b.get_y() + 0.1, 0], angle=-PI / 1.6,
                                         color=GREEN, stroke_width=3, tip_length=0.14))
            self.play(LaggedStart(*[Create(h) for h in hands], lag_ratio=0.5), run_time=2.4)

            # "The recursive calls don't nest."
            c.wait_until("iter")
            lab_y = baseline(stair[4][1]) - 0.95
            nest = [T("calls nest", size=32, color=DIM).move_to([stair_x, lab_y, 0]),
                    T("calls don't nest", size=32, color=GREEN).move_to([flat_x, lab_y, 0])]
            self.play(FadeIn(nest[1], shift=0.25 * DOWN), run_time=1.0)
            self.play(FadeIn(nest[0], shift=0.25 * DOWN), run_time=1.0)

            # "As lecture two put it, add-len is iterative, or tail-recursive."  The labels get their names.
            c.wait_until("iterative")
            tr = [T("not tail-recursive", size=32, color=DIM).move_to(nest[0]),
                  T("tail-recursive", size=32, color=GREEN).move_to(nest[1])]
            self.play(FadeTransform(nest[1], tr[1]), FadeTransform(nest[0], tr[0]), run_time=1.5)
        self.stair, self.unders, self.names = stair, unders, names
        self.edges, self.hands, self.tr = [st_edge, fl_edge], hands, tr
        self.flat_x, self.stair_x, self.lab_y = flat_x, stair_x, lab_y

    # ── acc.5: the tail in tail-recursive is not a list's tail ───────────────────
    def which_tail(self):
        rows, tr = self.flat_rows, self.tr
        tail_word = select(tr[1], "tail")[0]
        y1 = self.lab_y - 1.05            # the free band under the labels

        mini = ConsChain(["a", "b", "c"]).scale(0.7)      # 0.7: its letters stay at size ≥ 29
        mini.move_to([self.flat_x - 0.05, y1 + 0.1, 0])
        t_brace = Brace(VGroup(*mini.cells[1:], mini.nil), DOWN, buff=0.1, color=DIM)
        t_lab = T("tail", size=32).next_to(t_brace, DOWN, buff=0.1)
        mini_pic = VGroup(mini, t_brace, t_lab)
        cross = Cross(mini_pic, stroke_color=RED, stroke_width=7, scale_factor=1.05)

        left = Code("1 + nlength xs", size=CMP_SIZE).move_to([self.stair_x, y1 + 0.2, 0])
        left.find("nlength").set_color(YELLOW)
        right = addlen_code("addlen (n + 1) xs", CMP_SIZE).move_to([self.flat_x, y1 + 0.2, 0])
        l_box = SurroundingRectangle(left.find("1 +"), color=YELLOW, buff=0.08, stroke_width=3)
        r_box = SurroundingRectangle(right, color=GREEN, buff=0.1, stroke_width=3)
        l_lab = T("still to do", size=32, color=YELLOW).next_to(l_box, DOWN, buff=0.18)
        r_lab = T("last thing", size=32, color=GREEN).next_to(r_box, DOWN, buff=0.18)

        with self.say("c3.acc.5") as c:
            # "Careful with that word, tail, again."  (a flash under it, and a colour that stays: P7)
            self.play(FlashUnder(tail_word, color=YELLOW, time_width=1.5),
                      *per_glyph(tail_word, lambda a: a.set_color(YELLOW)), run_time=1.2)
            # "...again": the tail we already know, a list's tail
            c.wait_until("again")
            self.play(FadeIn(mini, shift=0.25 * UP), GrowFromCenter(t_brace), FadeIn(t_lab, shift=0.2 * UP),
                      run_time=1.2)
            # "The tail in tail-recursive has nothing to do with the tail of a list."
            c.wait_until("nothing to do")
            self.play(Create(cross), run_time=1.0)

            # "It means the recursive call is the very last thing the function does."
            c.wait_until("last")
            self.play(LaggedStart(FadeOut(cross), FadeOut(mini_pic), lag_ratio=0.2),
                      time_span(FadeIn(left, shift=0.25 * UP), 0.5, 1.4),
                      time_span(FadeIn(right, shift=0.25 * UP), 0.5, 1.4), run_time=1.4)
            c.wait_until("very last")
            self.play(Create(r_box), FadeIn(r_lab, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("function does")
            self.play(Create(l_box), FadeIn(l_lab, shift=0.2 * DOWN), run_time=1.0)

            # "So there's nothing to remember, and OCaml can reuse the same space for every call."
            # One fixed-size frame: every call fits in the same space.
            c.wait_until("nothing")
            w = rows[0][1].width + 0.3
            h = CMP_PITCH * 0.9

            def slot(i):
                code = rows[i][1]
                return [code.get_left()[0] - 0.15 + w / 2, baseline(code) + 0.11, 0]

            space = Rectangle(width=w, height=h).set_stroke(GOLD, 3).set_fill(GOLD, 0.1).move_to(slot(0))
            space.set_z_index(-1)
            self.play(FadeIn(space), run_time=0.8)
            c.wait_until("reuse")
            self.play(Succession(*[space.animate(rate_func=smooth).move_to(slot(i)) for i in (1, 2, 3)]),
                      run_time=2.1)
        self.tail_bits = [left, right, l_box, r_box, l_lab, r_lab]
        self.space = space

    # ── acc.6: O(1) space, O(n) time ───────────────────────────────────────────
    def costs(self):
        rows = self.flat_rows
        y_space = self.lab_y - 0.95
        y_time = y_space - 0.8
        l_space = cost(r"O(n)", "space", color=DIM).move_to([self.stair_x, y_space, 0])
        r_space = cost(r"O(1)", "space").move_to([self.flat_x, y_space, 0])
        l_time = cost(r"O(n)", "time", color=DIM).move_to([self.stair_x, y_time, 0])
        r_time = cost(r"O(n)", "time").move_to([self.flat_x, y_time, 0])
        r_time.align_to(r_space, LEFT)

        with self.say("c3.acc.6") as c:
            # "That means add-len needs only a fixed amount of space, however long the list is."
            self.play(LaggedStart(*[FadeOut(m) for m in self.tail_bits], lag_ratio=0.08), run_time=1.2)
            c.wait_until("however long")
            self.play(FadeIn(l_space, shift=0.25 * UP), run_time=1.0)
            # "Big O of one."
            c.wait_until("big o of one")
            self.play(FadeOut(self.space), Write(r_space[0]), FadeIn(r_space[1], shift=0.2 * LEFT), run_time=1.2)

            # "But its time is still big O of en."
            c.wait_until("time")
            self.play(Write(r_time[0]), FadeIn(r_time[1], shift=0.2 * LEFT), FadeIn(l_time, shift=0.25 * UP),
                      run_time=1.2)

            # "There's no way to find the length of a list without visiting each of its elements."
            c.wait_until("visiting")
            heads = [rows[0][1].find("a", nth=1), rows[1][1].find("b"), rows[2][1].find("c")]
            self.play(LaggedStart(*[FlashAround(h, color=YELLOW, time_width=1.5) for h in heads], lag_ratio=0.6),
                      run_time=2.4)

            # "Same time as before, but far less space."
            c.wait_until("sum")
            self.play(FlashAround(l_time, color=GOLD, time_width=1.5), FlashAround(r_time, color=GOLD, time_width=1.5),
                      run_time=1.2)
            c.wait_until("far less")
            self.play(FlashAround(r_space, color=GOLD, time_width=1.5), run_time=1.2)
