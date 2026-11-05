"""Chapter 2, scene 4: why patterns beat head and tail. `second` written as hd (tl xs) compiles
silently and crashes on [3] at run time; written with a pattern, OCaml warns first (x::[]).
Clips c2.why.1 – c2.why.4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# full frame (clips 1-2): version A alone
CAP_Y = 3.3
DEF_Y, SLOT_Y, VAL_Y = 2.4, 1.4, 0.45
CALL_P = np.array([-4.25, -0.95, 0])
REPLY_P = np.array([-4.25, -2.05, 0])
CHAIN_P = np.array([2.65, -1.62, 0])
TLROW_Y, EXC_Y = -2.62, -3.3
# split (clips 3-4): A on the left (faded), B on the right
LX, RX = -3.45, 3.45
TOP_Y = 3.1             # the caption leaves at the split; both definitions move up
A_SLOT_Y, A_CALL_Y, A_EXC_Y = 2.05, 0.4, -0.5
LOW_Y = -2.45           # A's crashed [3] and B's x::[] sit on one row, joined by a TEAL line
B_CHAIN_Y, WARN_Y = -0.6, 0.25
CAPTION_Y = -3.35
FADED = 0.4

A_SRC = "let second xs = hd (tl xs)"
B_SRC = "let second = function\n  | x :: y :: rest -> y"
W_SRC = ("Warning 8 [partial-match]:\n"      # ch2_s3's warning box, wrapped to fit a half
         "this pattern-matching\n"
         "is not exhaustive.\n"
         "Here is an example of a\n"
         "case that is not matched:\n"
         "x::[]")
EXC_SRC = 'Exception: Match_failure ("//toplevel//", 1, 7).'


# ── helpers (local to this scene) ───────────────────────────────────────────────
def recolor_code(code, base, spans):
    """A Code block read as plain terminal output: one base colour, a few spans picked out."""
    code.text.set_color(base)
    for sub, color in spans:
        VGroup(*code.find(sub)).set_color(color)
    return code


def pointer(text, x, top, color=YELLOW):
    """A ▼ marker over a cell (at x, above height `top`) with a short code label on it."""
    tri = marker(color).move_to([x, top + 0.38, 0])
    lab = Mono(text, size=30, color=color).next_to(tri, UP, buff=0.1)
    return VGroup(lab, tri)


def born_from(scene, pairs, code, run_time, extra=(), shift=0.2 * DOWN):
    """Bring `code` on screen: each (source, substring, nth, keep_source) glyph run flies out of
    its source while the rest fades in; then the pieces are swapped for the real Code."""
    used, pieces, anims = set(), [], []
    for src, sub, nth, keep in pairs:
        glyphs = code.find(sub, nth=nth)
        used |= {id(g) for g in glyphs}
        piece = VGroup(*[g.copy() for g in glyphs])
        pieces.append(piece)
        anims.append(TransformFromCopy(src, piece) if keep else ReplacementTransform(src, piece))
    rest = VGroup(*[g.copy() for g in code.text if id(g) not in used])
    scene.play(*anims, FadeIn(rest, shift=shift), *extra, run_time=run_time)
    scene.remove(*pieces, rest)
    scene.add(code)


class WhyPatterns(NarratedScene):
    def construct(self):
        self.version_a()
        self.single()
        self.version_b()
        self.warning()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # why.1: second = hd (tl xs); it works on [3; 5; 9]; OCaml says nothing
    def version_a(self):
        hd0 = Code("hd", size=64).move_to([-1.6, 0.2, 0])
        tl0 = Code("tl", size=64).move_to([1.6, 0.2, 0])
        cap = T("the second element", size=40).move_to(UP * CAP_Y)
        a_def = Code(A_SRC, size=44).move_to(UP * DEF_Y)
        val = Code("val second : 'a list -> 'a = <fun>", size=32).move_to(UP * VAL_Y)
        call = Code("second [3; 5; 9]", size=34).move_to(CALL_P)
        reply = Code("- : int = 5", size=34).move_to(REPLY_P)
        chain = ConsChain([3, 5, 9]).move_to(CHAIN_P)
        cells, arrows = chain.cells, chain.arrows
        top = cells[0].box.get_top()[1]
        ptr = pointer("xs", cells[0].box.get_x(), top)
        slot_box = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=a_def.width + 0.5, height=0.8),
                                  num_dashes=60).set_stroke(DIM, 2.5).move_to(UP * SLOT_Y)
        slot_txt = T("no warning", size=30, color=DIM, slant=ITALIC).move_to(slot_box)

        with self.say("c2.why.1") as c:
            # "Now, you could take lists apart using nothing but head and tail."
            self.play(LaggedStart(FadeIn(hd0, shift=0.3 * DOWN), FadeIn(tl0, shift=0.3 * DOWN), lag_ratio=0.3),
                      run_time=1.4)
            # "Say you want the second element of a list."
            c.wait_until("task")
            self.play(FadeIn(cap, shift=0.3 * DOWN), run_time=1.0)
            # "That's the head of the tail."  hd and tl fly into the definition; OCaml's reply follows
            c.wait_until("combo")
            born_from(self, [(hd0, "hd", 0, False), (tl0, "tl", 0, False)], a_def, run_time=2.0,
                      extra=[time_span(FadeIn(val, shift=0.2 * DOWN), 1.1, 2.0)])
            # "Try it on three, five, nine."
            c.wait_until("works")
            parts = [cells[0], arrows[0], cells[1], arrows[1], cells[2], arrows[2], chain.nil]
            self.play(FadeIn(call, shift=0.2 * DOWN),
                      LaggedStart(*[FadeIn(m) for m in parts], lag_ratio=0.15),
                      time_span(FadeIn(ptr, shift=0.2 * DOWN), 1.2, 1.9), run_time=1.9)
            # "The tail is five, nine, ..."  tl moves the marker on to the 5
            c.wait_until("the tail is")
            self.play(Transform(ptr, pointer("tl xs", cells[1].box.get_x(), top)),
                      restyle(cells[0], 0.35), restyle(arrows[0], 0.35), run_time=1.2)
            # "... and its head is five."  hd lifts the 5 out into the reply
            c.wait_until("its head")
            born_from(self, [(cells[1].label, "5", 0, True)], reply, run_time=1.5)
            # "And notice that this time, OCaml prints no warning at all."
            c.wait_until("silent")
            self.play(Create(slot_box), time_span(FadeIn(slot_txt), 0.8, 1.6), run_time=1.6)
            # "There's no pattern here for it to check."
            c.wait_until("There's no pattern")
            self.play(FlashUnder(VGroup(*a_def.find("xs")), color=YELLOW, time_width=1.5), run_time=1.3)

        self.cap, self.a_def, self.val, self.call, self.reply = cap, a_def, val, call, reply
        self.chain, self.ptr, self.top = chain, ptr, top
        self.slot_box, self.slot_txt = slot_box, slot_txt

    # why.2: second [3]: tl [3] is fine, hd [] raises Match_failure, and nothing warned us
    def single(self):
        chain, top = self.chain, self.top
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil
        call2 = Code("second [3]", size=34).move_to(CALL_P).align_to(self.call, LEFT)
        pitch = cells[1].get_left()[0] - cells[0].get_left()[0]
        # [3] alone: [] slides up to the 3, and the pair re-centres where the long chain was
        span_mid = (cells[0].get_left()[0] + nil.get_right()[0] - 2 * pitch) / 2
        s = CHAIN_P[0] - span_mid
        nil_x = nil.get_x() - 2 * pitch + s
        ptr2 = pointer("xs", cells[0].box.get_x() + s, top)
        tl_row = VGroup(Code("tl [3]", size=32),
                        recolor_code(Code("- : int list = []", size=32), GREEN, []),
                        check_mark(GREEN)).arrange(RIGHT, buff=0.45).move_to([CHAIN_P[0], TLROW_Y, 0])
        exc = Code(EXC_SRC, size=30).move_to(UP * EXC_Y)
        exc.text.set_color(RED)
        cross = cross_mark(RED).move_to([nil_x, nil.get_y(), 0])
        found = T("found only at run time", size=32, color=RED).move_to(REPLY_P)

        with self.say("c2.why.2") as c:
            # "But what about a list with only a single element, ..."
            self.play(FadeOut(self.reply), FadeOut(self.ptr), restyle(cells[0], 1), restyle(arrows[0], 1),
                      run_time=1.0)
            # "... like the list containing just three?"
            c.wait_until("like the list")
            self.play(FadeTransform(self.call, call2),
                      *[FadeOut(m) for m in (cells[1], arrows[1], cells[2], arrows[2])],
                      cells[0].animate.shift(RIGHT * s), arrows[0].animate.shift(RIGHT * s),
                      nil.animate.shift(RIGHT * (s - 2 * pitch)),
                      time_span(FadeIn(ptr2, shift=0.2 * DOWN), 1.2, 1.8), run_time=1.8)
            # "Its tail is nil, and that part is fine."
            c.wait_until("tail")
            self.play(Transform(ptr2, pointer("tl xs", nil_x, top)),
                      restyle(cells[0], 0.35), restyle(arrows[0], 0.35),
                      time_span(FadeIn(tl_row, shift=0.2 * DOWN), 0.6, 1.6), run_time=1.6)
            # "But then we ask for the head of nil."
            c.wait_until("head")
            self.play(Transform(ptr2, pointer("hd (tl xs)", nil_x, top, RED)),
                      FlashAround(nil, color=RED, time_width=1.5), run_time=1.3)
            # "Match failure."
            c.wait_until("crash")
            self.play(FadeIn(exc, shift=0.3 * DOWN), Create(cross), run_time=1.2)
            # "And nothing warned us."
            c.wait_until("late")
            self.play(FlashAround(self.slot_box, color=RED, time_width=1.5),
                      self.slot_txt.animate.set_color(RED), run_time=1.5)
            # "This mistake only shows up while the program is running, ..."
            c.wait_until("this mistake")
            self.play(FadeIn(found, shift=0.3 * DOWN), run_time=1.0)
            # "... on exactly the wrong input."
            c.wait_until("wrong input")
            rt = min(1.2, c.remaining - 0.05)
            if rt > 0.6:
                self.play(FlashAround(call2, color=RED, time_width=1.5), run_time=rt)

        self.call2, self.exc, self.cross = call2, exc, cross
        self.tl_row, self.ptr2, self.found = tl_row, ptr2, found

    # why.3: A packs into the left half and fades; B, the pattern version, lies over 3 → 5 → 9 → []
    def version_b(self):
        cells, arrows, nil = self.chain.cells, self.chain.arrows, self.chain.nil
        a_def, call2, cross = self.a_def, self.call2, self.cross
        slot_box2 = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=6.3, height=0.75),
                                   num_dashes=60).set_stroke(DIM, 2.5).move_to([LX, A_SLOT_Y, 0])
        slot_txt2 = T("no warning", size=28, color=RED, slant=ITALIC).move_to(slot_box2)
        exc2 = Code("Exception: Match_failure …", size=28).move_to([LX, A_EXC_Y, 0])
        exc2.text.set_color(RED)
        low = [cells[0], arrows[0], nil, cross]
        cen = np.array([(cells[0].get_left()[0] + nil.get_right()[0]) / 2, cells[0].get_y(), 0])
        low_to = np.array([LX, LOW_Y, 0])

        b_def = Code(B_SRC, size=32).move_to([RX, 0, 0])
        b_def.shift(UP * (TOP_Y - b_def.line(0).get_y()))
        bchain = ConsChain([3, 5, 9]).scale(0.8).move_to([RX, B_CHAIN_Y, 0])
        bparts = [bchain.cells[0], bchain.arrows[0], bchain.cells[1], bchain.arrows[1],
                  bchain.cells[2], bchain.arrows[2], bchain.nil]
        pat = b_def.find("x :: y :: rest")
        hl = token_box(pat, b_def.line(1))
        lx = label_pointer("x", bchain.cells[0].box, UP, color=FG)
        ly = label_pointer("y", bchain.cells[1].box, UP, color=YELLOW)
        btop = bchain.cells[2].box.get_top()[1]
        brace = span_brace(np.array([bchain.cells[2].box.get_left()[0], btop, 0]),
                           np.array([bchain.nil.get_right()[0], btop, 0]), direction=UP, color=FG)
        rest_lab = T("rest", size=30).next_to(brace, UP, buff=0.12).set_y(lx[0].get_y())

        with self.say("c2.why.3") as c:
            # "That's why taking lists apart with head and tail is so hard to get right."
            self.play(FlashUnder(VGroup(*a_def.find("hd (tl xs)")), color=YELLOW, time_width=1.5),
                      run_time=1.5)
            # "Every call quietly assumes the list is long enough."  A packs into the left half
            c.wait_until("every call")
            self.play(*[FadeOut(m) for m in (self.cap, self.val, self.tl_row, self.ptr2, self.found)],
                      a_def.animate.scale(28 / 44).move_to([LX, TOP_Y, 0]),
                      ReplacementTransform(self.slot_box, slot_box2),
                      ReplacementTransform(self.slot_txt, slot_txt2),
                      call2.animate.move_to([LX, A_CALL_Y, 0]),
                      ReplacementTransform(self.exc, exc2),
                      *[m.animate.scale(0.85, about_point=cen).shift(low_to - cen) for m in low],
                      run_time=2.0)
            # "Here's the same function, written with a pattern instead."
            c.wait_until("pattern")
            a_parts = [a_def, slot_box2, slot_txt2, call2, exc2, *low]
            self.play(*set_alpha(a_parts, FADED), Write(b_def), run_time=2.0)
            # "The pattern spells out exactly what we expect."
            c.wait_until("shape")
            self.play(FadeIn(hl), LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in bparts], lag_ratio=0.15),
                      run_time=1.8)
            # "Some element, ex, ..."
            c.wait_until("some element")
            self.play(TransformFromCopy(VGroup(*b_def.find("x", line=1)), lx[0]), GrowArrow(lx[1]),
                      run_time=1.2)
            # "... then a second element, called why, ..."
            c.wait_until("called why")
            y_pat = b_def.find("y", line=1)
            self.play(TransformFromCopy(VGroup(*y_pat), ly[0]), GrowArrow(ly[1]),
                      *recolor(y_pat, YELLOW), run_time=1.2)
            # "... then the rest of the list."
            c.wait_until("the rest")
            self.play(GrowFromCenter(brace), TransformFromCopy(VGroup(*b_def.find("rest")), rest_lab),
                      run_time=1.3)
            # "And the answer is that second element."
            c.wait_until("give")
            y_res = b_def.find("y", line=1, nth=1)
            self.play(*recolor(y_res, YELLOW), FlashAround(VGroup(*y_res), color=YELLOW, time_width=1.5),
                      FlashAround(bchain.cells[1], color=YELLOW, time_width=1.5), run_time=1.5)
            # "You can almost see the shape of the list in the code."
            c.wait_until("picture")
            self.play(FlashAround(VGroup(*pat), color=YELLOW, time_width=1.5),
                      FlashAround(VGroup(*bparts), color=YELLOW, time_width=1.5), run_time=1.8)

        self.a_parts, self.low = a_parts, low
        self.slot_box2, self.slot_txt2, self.exc2 = slot_box2, slot_txt2, exc2
        self.b_stuff = [hl, *bparts, lx[0], lx[1], ly[0], ly[1], brace, rest_lab]

    # why.4: OCaml's warning for B; its example x::[] is exactly A's crash; the final split
    def warning(self):
        cells, nil, cross = self.chain.cells, self.chain.nil, self.cross
        wtext = recolor_code(Code(W_SRC, size=28), FG,
                             [("Warning 8 [partial-match]:", YELLOW), ("x::[]", TEAL)])
        wtext.move_to([RX, WARN_Y, 0])
        wbox = SurroundingRectangle(wtext, buff=0.2, color=YELLOW, stroke_width=3, corner_radius=0.08)
        one = ConsChain(["x"]).scale(0.85).move_to([RX, LOW_Y, 0])
        tie = Line(nil.get_right() + RIGHT * 0.3, one.cells[0].get_left() + LEFT * 0.3,
                   color=TEAL, stroke_width=4)
        cap_a = T("silent until it crashes", size=32, color=RED).move_to([LX, CAPTION_Y, 0])
        cap_b = T("warned before it runs", size=32, color=GREEN).move_to([RX, CAPTION_Y, 0])
        q_arrow = Arrow(one.nil.get_right() + RIGHT * 0.15, one.nil.get_right() + RIGHT * 0.85, buff=0,
                        color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.35, tip_length=0.18)
        q = T("?", size=48, color=GOLD).next_to(q_arrow, RIGHT, buff=0.15)

        with self.say("c2.why.4") as c:
            # "And now OCaml can check our work."
            self.play(LaggedStart(*[FadeOut(m) for m in self.b_stuff], lag_ratio=0.05),
                      time_span(Create(wbox), 0.5, 1.5), time_span(FadeIn(wtext, shift=0.2 * DOWN), 0.7, 1.8),
                      run_time=1.8)
            # "It warns that this match is not exhaustive, ..."
            c.wait_until("it warns")
            self.play(FlashUnder(VGroup(*wtext.line(1)), color=YELLOW, time_width=1.5),
                      FlashUnder(VGroup(*wtext.line(2)), color=YELLOW, time_width=1.5), run_time=1.3)
            # "... and the example it gives is ex cons nil, ..."
            c.wait_until("example")
            self.play(FlashAround(VGroup(*wtext.find("x::[]")), color=TEAL, time_width=1.5), run_time=1.2)
            # "... a list with just a single element."  x::[] drawn: one cell, then nil
            c.wait_until("a list with just")
            # (ReplacementTransform from copies: TransformFromCopy re-aligns its *target*, which
            # leaves an Arrow target without points of its own)
            self.play(*[ReplacementTransform(VGroup(*wtext.find(s, line=5)).copy(), m)
                        for s, m in (("x", one.cells[0]), ("::", one.arrows[0]), ("[]", one.nil))],
                      run_time=1.6)
            # "That's precisely the case that crashed before."
            c.wait_until("same")
            crashed = [self.call2, self.exc2, *self.low]
            self.play(*set_alpha(crashed, 1), Create(tie),
                      time_span(FlashAround(self.call2, color=TEAL, time_width=1.5), 0.6, 1.8), run_time=1.8)
            # "With head and tail, nobody warns you."
            c.wait_until("lesson")
            self.play(FadeIn(cap_a, shift=0.3 * DOWN), *set_alpha([self.slot_box2, self.slot_txt2], 1),
                      FlashAround(self.slot_box2, color=RED, time_width=1.5), run_time=1.3)
            # "With patterns, OCaml spots the missing shapes before the program ever runs, ..."
            c.wait_until("with patterns")
            self.play(FadeIn(cap_b, shift=0.3 * DOWN), FlashAround(wbox, color=GREEN, time_width=1.5),
                      run_time=1.3)
            # "... and it's up to you to decide what those shorter lists should do."
            c.wait_until("you")
            self.play(GrowArrow(q_arrow), FadeIn(q, shift=0.2 * LEFT), run_time=1.2)
            # "So in practice, you'll rarely need head and tail at all."
            c.wait_until("seldom")
            self.play(*set_alpha([*self.a_parts, tie], DIMMED), run_time=1.5)
