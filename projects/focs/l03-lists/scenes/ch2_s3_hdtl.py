"""Chapter 2, scene 3: head and tail written with a pattern, OCaml's "not exhaustive"
warning, hd [] raising Match_failure, and the answer to the opening question.

STATUS (paused): done: all five clips (c2.hdtl.1-5) built; renders clean at 480p15
(~106.7 s vs 104.1 s narration + gaps + fade); dwell 0 flags after the last-clip gap was
raised to 2.0 s. remaining: visual review of the render (contact sheet + key frames:
ghost `let hd xs = …` alignment, warning box fit at 12.5 units wide, clip-3 frame is
top-heavy, hd [] drawing at ROW_Y); confirm the "head of [] = ?" object matches whatever
ch2_s1_hook builds (mirrors ch1_s6: T head/of, Code [], GOLD ?). known issues: none
seen yet, but nothing has been looked at frame by frame.

Clips c2.hdtl.1 - c2.hdtl.5.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

HERO, CODE = 60, 48          # hd's definition alone (hero), then with the examples below it
HERO_Y = -0.2                # the hero line while it is explained on its own
HD_Y, TL_Y = 2.95, 2.05      # the two definitions once the examples arrive
CALL_Y, LAB_Y, CHAIN_Y = 1.05, 0.12, -0.95
REPLY_Y, NOTE_Y = -2.45, -3.2
WARN_Y, VAL_Y = 1.35, -0.25  # OCaml's answer to the definition (clip 3)
ROW_Y, EXC_Y, TLROW_Y = -0.85, -2.05, -2.95   # hd [], its exception, tl [] (clip 4)
DIM_TO = 0.3                 # spotlight: everything else drops to this (PATTERNS P9)

W_SRC = ("Warning 8 [partial-match]:\n"
         "this pattern-matching is not exhaustive.\n"
         "Here is an example of a case that is not matched: []")
EXC_SRC = 'Exception: Match_failure ("//toplevel//", 1, 7).'


# ── helpers (local to this scene) ───────────────────────────────────────────────
def tbox(glyphs, line, color=YELLOW, pad=0.09):
    """The sliding highlight (P8): thin stroke, faint fill, behind the text, as tall as `line`."""
    g, ln = VGroup(*glyphs), VGroup(*line)
    box = Rectangle(width=max(g.width + 2 * pad, 0.42), height=ln.height + 2 * pad,
                    stroke_color=color, stroke_width=2).set_fill(color, opacity=0.25)
    return box.move_to([g.get_x(), ln.get_y(), 0]).set_z_index(-1)


def opacity(mobs, value):
    # A list, to unpack into play(): an AnimationGroup would add a new Group of these
    # (already on screen) mobjects on top of the scene and change the drawing order.
    return [m.animate.set_opacity(value) for m in mobs]


def born_from(scene, sources, code, parts, rest, run_time=1.5, extra=()):
    """Bring `code` on screen: each glyph run in `parts` flies out of a copy of the matching
    source (P5) while the `rest` fades in; then the pieces are swapped for the real Code."""
    pieces = [VGroup(*code.find(p)) for p in parts]
    others = VGroup(*[g for r in rest for g in code.find(r)])
    scene.play(*[TransformFromCopy(s, p) for s, p in zip(sources, pieces)],
               FadeIn(others, shift=0.2 * DOWN), *extra, run_time=run_time)
    scene.remove(*pieces, others)
    scene.add(code)


def check_mark(color=GREEN, size=0.42):
    tick = VMobject().set_points_as_corners([[-0.5, 0.05, 0], [-0.15, -0.35, 0], [0.5, 0.45, 0]])
    return tick.set_stroke(color, 7).scale(size)


def recolor_code(code, base, spans):
    """A Code block read as plain terminal output: one base colour, a few spans picked out."""
    code.text.set_color(base)
    for sub, color in spans:
        VGroup(*code.find(sub)).set_color(color)
    return code


class HeadTailEmpty(NarratedScene):
    def construct(self):
        self.head()
        self.tail()
        self.warning()
        self.empty()
        self.answer()
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # hdtl.1: hd with its pattern where the argument's name would go; hd [1; 2; 3] = 1
    def head(self):
        hd = Code("let hd (x::l) = x", size=HERO).move_to(UP * HERO_Y)
        line = list(hd.text)
        pattern = list(hd.find("(x::l)"))
        px, pl, rx = hd.find("x")[0], hd.find("l)")[0], hd.find("x", nth=1)[0]

        # the usual shape, as a ghost above: `let hd xs = …`, with xs over the pattern's slot
        ghost = Code("let hd xs = …", size=HERO)
        ghost.text.set_color(DIM)
        ghost.shift(RIGHT * (hd.find("let")[0].get_x() - ghost.find("let")[0].get_x()))
        xs = list(ghost.find("xs"))
        VGroup(*xs).shift(RIGHT * (VGroup(*pattern).get_x() - VGroup(*xs).get_x()))
        VGroup(*ghost.find("= …")).shift(RIGHT * (hd.find("=")[0].get_x() - ghost.find("=")[0].get_x()))
        ghost.set_y(HERO_Y + 1.2)
        ghost_rest = [g for g in ghost.text if g not in xs]

        call = Code("hd [1; 2; 3]", size=40).move_to(UP * CALL_Y)
        chain = ConsChain([1, 2, 3]).move_to(UP * CHAIN_Y)
        cells = chain.cells
        x_box = DashedVMobject(SurroundingRectangle(cells[0], buff=0.1), num_dashes=30).set_stroke(YELLOW, 3)
        x_lab = Mono("x", size=40, color=YELLOW).next_to(x_box, UP, buff=0.12)
        brace = Brace(VGroup(cells[1], cells[2], chain.nil), UP, buff=0.12, color=TEAL)
        l_lab = Mono("l", size=40, color=TEAL).next_to(brace, UP, buff=0.08)
        l_lab.align_to(x_lab, DOWN)
        reply = Code("- : int = 1", size=40).move_to(UP * REPLY_Y)

        with self.say("c2.hdtl.1") as c:
            # "Here's the head function, written with a pattern."
            self.play(FadeIn(hd, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("pattern")
            self.play(FlashUnder(VGroup(*pattern), color=TEAL, time_width=1.5), run_time=1.2)

            # "This time there's no keyword, function."  The ordinary shape appears above, as a ghost.
            c.wait_until("where")
            self.play(FadeIn(ghost, shift=0.25 * DOWN), run_time=1.2)
            # "Instead, the pattern sits right where the argument's name would normally go."
            c.wait_until("instead")
            hb = tbox(pattern, line)
            self.play(FadeIn(hb), run_time=0.8)
            c.wait_until("argument's name")
            self.play(hb.animate.become(tbox(xs, ghost.text)), run_time=1.0)
            # the name gives way: xs sinks into the pattern's slot and is gone (the box follows)
            c.wait_until("go")
            self.remove(ghost)
            xs_piece, rest_piece = VGroup(*xs), VGroup(*ghost_rest)
            self.add(xs_piece, rest_piece)
            self.play(FadeOut(xs_piece, shift=DOWN * 1.2), FadeOut(rest_piece),
                      hb.animate.become(tbox(pattern, line)), run_time=1.4)

            # "It says, the argument must be some head, ex, consed onto some tail, ell."
            c.wait_until("some head")
            self.play(hb.animate.become(tbox([px], line)), px.animate.set_color(YELLOW), run_time=0.8)
            c.wait_until("consed")
            self.play(hb.animate.become(tbox(hd.find("::"), line)), run_time=0.7)
            c.wait_until("some tail")
            self.play(hb.animate.become(tbox([pl], line, TEAL)), pl.animate.set_color(TEAL), run_time=0.8)
            # "And the answer is ex."
            c.wait_until("answer")
            self.play(hb.animate.become(tbox([rx], line)), rx.animate.set_color(YELLOW), run_time=0.9)

            # "So on the list one, two, three, ..."  The definition moves up for its example.
            c.wait_until("call")
            self.play(FadeOut(hb), hd.animate.scale(CODE / HERO).move_to(UP * HD_Y),
                      time_span(FadeIn(call, shift=0.3 * DOWN), 0.7, 1.5), run_time=1.5)
            c.wait_until("list")
            self.play(FadeIn(chain, shift=0.3 * UP), run_time=1.2)
            # "... ex matches the first element, ..."  The pattern lies over the chain (P5).
            c.wait_until("ex matches")
            self.play(TransformFromCopy(px, x_lab), Create(x_box),
                      time_span(TransformFromCopy(pl, l_lab), 0.4, 1.5),
                      time_span(GrowFromCenter(brace), 0.4, 1.5), run_time=1.5)
            # "... and the head function gives back one."  The 1 comes out of its cell.
            c.wait_until("and the head function")
            born_from(self, [cells[0].label], reply, ["1"], ["- : int ="], run_time=1.2)

        self.hd, self.hd_line, self.px = hd, line, px
        self.call, self.chain, self.reply = call, chain, reply
        self.x_bits, self.l_bits = [x_box, x_lab], [brace, l_lab]

    # hdtl.2: tl is the same line with l at the end; tl [7; 6; 5] = [6; 5], a whole list
    def tail(self):
        hd, chain = self.hd, self.chain
        cells = chain.cells
        tl = Code("let tl (x::l) = l", size=CODE)
        tl.find("x")[0].set_color(YELLOW)
        tl.find("l)")[0].set_color(TEAL)
        tl.find("l", nth=2)[0].set_color(TEAL)
        tl.align_to(hd, LEFT).set_y(TL_Y)
        tl_line = list(tl.text)
        hd_rx, tl_rl = hd.find("x", nth=1)[0], tl.find("l", nth=2)[0]

        call2 = Code("tl [7; 6; 5]", size=40).move_to(self.call)
        new_vals = [value_label(v).move_to(cell.label) for v, cell in zip((7, 6, 5), cells)]
        reply2 = Code("- : int list = [6; 5]", size=40).move_to(UP * REPLY_Y)
        note = T("a list, not an element", size=32, color=RED).move_to(UP * NOTE_Y)

        with self.say("c2.hdtl.2") as c:
            # "The tail function is identical, ..."  It is born from a copy of hd's line.
            self.play(TransformFromCopy(hd, tl), run_time=1.8)
            # "... except for what it gives back at the very end."
            c.wait_until("very end")
            self.play(FlashAround(tl_rl, color=TEAL, time_width=1.5), run_time=1.0)
            # "Instead of ex, it hands back ell."  One box hops between the two endings (P8).
            c.wait_until("instead of")
            hb = tbox([hd_rx], self.hd_line)
            self.play(FadeIn(hb), run_time=0.6)
            c.wait_until("hands back")
            self.play(hb.animate.become(tbox([tl_rl], tl_line, TEAL)), run_time=0.9)

            # "So the tail of seven, six, five is six, five."  Same pattern, new list.
            c.wait_until("call")
            self.play(FadeOut(hb), FadeOut(self.reply), Transform(self.call, call2), run_time=1.1)
            c.wait_until("seven")
            self.play(*[Transform(cell.label, v) for cell, v in zip(cells, new_vals)], run_time=1.0)
            c.wait_until("is six")
            self.play(*opacity(self.x_bits, 0.35),
                      FlashAround(VGroup(*self.l_bits), color=TEAL, time_width=1.5), run_time=1.0)
            born_from(self, [cells[1].label, cells[2].label], reply2, ["6", "5"],
                      ["- : int list =", "[", ";", "]"], run_time=1.4)

            # "And remember from chapter one, that's a whole list, not a single element."
            c.wait_until("whole list")
            self.play(FlashAround(VGroup(*reply2.find("[6; 5]")), color=TEAL, time_width=1.5),
                      FadeIn(note, shift=0.25 * DOWN), run_time=1.2)

        self.tl_stuff = [tl, self.call, chain, *self.x_bits, *self.l_bits, reply2, note]

    # hdtl.3: OCaml's reply to hd: the warning first, then the type; its example is []
    def warning(self):
        hd = self.hd
        wtext = recolor_code(Code(W_SRC, size=28), FG, [("Warning 8 [partial-match]:", YELLOW), ("[]", TEAL)])
        wtext.move_to(UP * WARN_Y)
        wbox = SurroundingRectangle(wtext, buff=0.2, color=YELLOW, stroke_width=3, corner_radius=0.08)
        val = Code("val hd : 'a list -> 'a = <fun>", size=32).move_to(UP * VAL_Y)
        w_nil = VGroup(*wtext.find("[]"))
        nil_box = SurroundingRectangle(w_nil, buff=0.07, color=RED, stroke_width=4)

        with self.say("c2.hdtl.3") as c:
            # "But when you type the head function into OCaml, something new happens."
            self.play(FlashAround(hd, color=YELLOW, time_width=1.5), *opacity(self.tl_stuff, DIM_TO),
                      run_time=1.2)
            # "Before it even tells you the type, it prints a warning."  The tail example makes way;
            # OCaml's output arrives in the order it prints it: the warning, then the type.
            c.wait_until("prints a warning")
            self.play(LaggedStart(*[FadeOut(m) for m in self.tl_stuff], lag_ratio=0.05),
                      time_span(Create(wbox), 0.4, 1.4), time_span(FadeIn(wtext, shift=0.2 * DOWN), 0.6, 1.6),
                      time_span(FadeIn(val, shift=0.2 * DOWN), 1.5, 2.3), run_time=2.3)
            # "It says this pattern matching is not exhaustive."
            c.wait_until("pattern matching")
            self.play(FlashUnder(VGroup(*wtext.line(1)), color=YELLOW, time_width=1.5), run_time=1.3)
            # "And it even shows you an example of such a list."
            c.wait_until("example")
            self.play(FlashUnder(VGroup(*wtext.find("Here is an example of a case that is not matched:")),
                                 color=YELLOW, time_width=1.5), run_time=1.4)
            # "The empty list."
            c.wait_until("nil")
            self.play(Create(nil_box), run_time=0.8)

        self.wtext, self.wbox, self.val, self.w_nil, self.nil_box = wtext, wbox, val, w_nil, nil_box

    # hdtl.4: accepted anyway; hd [] finds no first cell and raises Match_failure; so does tl []
    def empty(self):
        hd = self.hd
        hdnil = Code("hd []", size=40)
        draw_x = 1.6
        hdnil.move_to([draw_x - 3.6, ROW_Y, 0])
        big_nil = Nil(size=56).move_to([draw_x, ROW_Y, 0])
        nbox = DashedVMobject(Rectangle(width=CELL + PTR_W + 0.2, height=CELL + 0.2),
                              num_dashes=30).set_stroke(YELLOW, 3).move_to(big_nil)
        nx = Mono("x", size=40, color=YELLOW).next_to(nbox, UP, buff=0.12)
        cross = Cross(nbox, stroke_color=RED, stroke_width=6, scale_factor=0.75)
        pbox = SurroundingRectangle(VGroup(*hd.find("(x::l)")), color=RED, buff=0.07, stroke_width=4)
        exc = Code(EXC_SRC, size=30)
        exc.text.set_color(RED)
        exc.move_to(UP * EXC_Y)

        tlnil = Code("tl []", size=36)
        short = Code("Exception: Match_failure …", size=28)
        short.text.set_color(RED)
        VGroup(tlnil, short).arrange(RIGHT, buff=0.6).move_to(UP * TLROW_Y)
        short.align_to(tlnil, DOWN).shift(DOWN * 0.02)

        with self.say("c2.hdtl.4") as c:
            # "It's only a warning, so OCaml accepts the function anyway."
            self.play(FlashAround(self.wbox, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("accepts")
            self.play(FlashAround(self.val, color=GREEN, time_width=1.5), run_time=1.2)

            # "But watch what happens when you ask for the head of the empty list."
            # The [] comes out of the warning that predicted it (P5).
            c.wait_until("head of the empty list")
            born_from(self, [self.w_nil], hdnil, ["[]"], ["hd"], run_time=1.5,
                      extra=[FadeOut(self.val)])

            # "The pattern needs a first cell, and there isn't one."
            c.wait_until("nofit")
            self.play(TransformFromCopy(VGroup(*hdnil.find("[]")), big_nil), run_time=1.2)
            c.wait_until("first cell")
            self.play(TransformFromCopy(self.px, nx), Create(nbox), run_time=1.2)
            c.wait_until("there isn't one")
            self.play(nbox.animate.set_stroke(RED), nx.animate.set_color(RED), Create(cross), run_time=1.0)
            # "No clause fits, so there's no answer to give back."
            c.wait_until("no clause fits")
            self.play(Create(pbox), run_time=1.0)

            # "Instead, OCaml raises an exception, called match failure."
            c.wait_until("raises")
            self.play(FadeIn(exc, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("match failure")
            self.play(FlashUnder(VGroup(*exc.find("Match_failure")), color=RED, time_width=1.5), run_time=1.2)

            # "The tail function fails in exactly the same way."  Same exception, smaller.
            c.wait_until("tail")
            pieces = VGroup(*short.find("Exception: Match_failure"))
            dots = VGroup(*short.find("…"))
            self.play(FadeIn(tlnil, shift=0.25 * DOWN),
                      TransformFromCopy(VGroup(*exc.find("Exception: Match_failure")), pieces),
                      time_span(FadeIn(dots), 0.9, 1.5), run_time=1.5)
            self.remove(pieces, dots)
            self.add(short)

        self.hdnil, self.exc, self.tlrow = hdnil, exc, [tlnil, short]
        self.board = [hd, pbox, self.wbox, self.wtext, self.nil_box, big_nil, nbox, nx, cross]

    # hdtl.5: "head of [] = ?" returns and the ? becomes an error (P23); then the guard
    def answer(self):
        size = 52
        parts = [T("head", size=size, color=YELLOW), T("of", size=size), Code("[]", size=size),
                 T("=", size=size)]
        qmark = T("?", size=96, color=GOLD)
        err = T("error", size=60, color=RED)
        q_row = VGroup(*parts, qmark).arrange(RIGHT, buff=0.32).move_to(UP * 2.35)
        a_row = VGroup(*[p.copy() for p in parts], err).arrange(RIGHT, buff=0.32).move_to(UP * 2.35)
        err.align_to(parts[0], DOWN).shift(DOWN * 0.02)
        a_row[:4].align_to(q_row[:4], DOWN)   # same baseline as before: only x moves

        g_null = Code("null xs = false", size=40)
        g_hd = Code("hd xs", size=40)
        g_arrow = Arrow(LEFT * 0.75, RIGHT * 0.75, buff=0, color=GREEN, stroke_width=5,
                        max_tip_length_to_length_ratio=0.25, tip_length=0.22)
        tick = check_mark()
        guard = VGroup(g_null, g_arrow, g_hd, tick).arrange(RIGHT, buff=0.4).move_to(UP * -2.35)
        tick.shift(LEFT * 0.1)
        g_false = VGroup(*g_null.find("false"))

        with self.say("c2.hdtl.5", gap=2.0) as c:
            # "So that's the answer to our opening question."  The definition, its warning and
            # the picture make way (P18); the evidence (hd [] and its exception) moves up.
            self.play(LaggedStart(*[FadeOut(m) for m in self.board], lag_ratio=0.05),
                      self.hdnil.animate.move_to(UP * 0.75), self.exc.animate.move_to(UP * -0.1),
                      *[m.animate.shift(UP * 1.6) for m in self.tlrow], run_time=1.6)
            c.wait_until("opening question")
            self.play(FadeIn(q_row, shift=0.3 * DOWN), run_time=1.2)
            self.remove(q_row)
            self.add(*parts, qmark)   # top-level, so the ? can turn into the answer on its own

            # "The head of an empty list isn't nil, or zero, or anything else."  (hold: P23)
            # "It's an error."
            c.wait_until("error")
            self.play(FadeTransform(qmark, err),
                      *[p.animate.move_to(t) for p, t in zip(parts, a_row[:4])], run_time=1.3)
            self.play(FlashAround(err, color=RED, time_width=1.5),
                      FlashUnder(VGroup(*self.exc.find("Match_failure")), color=RED, time_width=1.5),
                      run_time=1.0)

            # "So if a list might be empty, check it with null first, ..."  The whole guard
            # appears (P2), the part after the check still dim.
            c.wait_until("null")
            self.play(*[FadeOut(m) for m in self.tlrow], run_time=1.0)
            c.wait_until("check it")
            for m in (g_arrow, g_hd):
                m.set_opacity(0.3)
            self.play(FadeIn(g_null, shift=0.25 * UP), time_span(FadeIn(g_arrow), 0.4, 1.1),
                      time_span(FadeIn(g_hd), 0.4, 1.1), run_time=1.1)
            # "... and only ask for the head when null says false."
            c.wait_until("safe")
            self.play(g_arrow.animate.set_opacity(1), g_hd.animate.set_opacity(1), run_time=1.0)
            c.wait_until("says false")
            self.play(FlashAround(g_false, color=TEAL, time_width=1.5), Create(tick), run_time=1.0)
