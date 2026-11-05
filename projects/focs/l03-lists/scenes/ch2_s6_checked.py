"""Chapter 2, scene 6: type checking happens at compile time (a bad sum never reaches run time, a
good one runs), the guarantee that buys, reading [] : 'a list, the recap and the chapter's end card.
Clips c2.check.1 – c2.check.3, c2.recap.1 – c2.recap.2 (the chapter's last scene).

Verified (ocaml 5.4.1): hd ["cat"; "dog"] + 1 -> Error: This expression has type string /
but an expression was expected of type int (underline = hd ["cat"; "dog"]); hd [1; 2; 3] + 1 ->
- : int = 2; [] -> - : 'a list = []; 1 :: [] -> - : int list = [1]; "cat" :: [] ->
- : string list = ["cat"]; null [] -> - : bool = true.

STATUS: done; tools/check.py clean (113.4 s render vs 102.4 s narration + gaps + 8 s end card).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, VShowPassingFlash, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── layout ──────────────────────────────────────────────────────────────────────
TL0, TL_Y, TL_L, TL_R = 0.3, 2.5, -6.3, 6.3   # the compile-time | run-time line: built at TL0, then up
GATE_X, PLAY_X = -0.85, 0.85             # the type check (end of compile time), ▶ (start of run time)
START_X, STOP_X, RUN_X = -5.9, GATE_X - 0.95, 3.0   # marker: entry, where a rejected sum stops, a run
ROW_X, SUM = -6.2, 44                    # check.1: left edge and size of the two sums
BAD_Y, ERR_Y, GOOD_Y = 1.0, (-0.05, -0.6), -2.25
CH_Y, LIFT_Y = 0.4, -2.2                 # check.2: the int chain, hd's result lifted out of it
S_X, S_SIZE, S_PAD = -6.105, 38, 14      # check.3 session: left edge, size, input column width
S_Y = (1.9, 0.75, -0.4, -1.55)


def g(code, sub, nth=0):
    """Glyphs of a substring of a Code, as a fresh VGroup."""
    return VGroup(*code.find(sub, nth=nth))


def session_row(inp, reply):
    # input and reply as ONE Code so their baselines match; the padding sets the reply column
    return Code(inp.ljust(S_PAD) + reply, size=S_SIZE)


def build(scene, code, pairs=(), rest=(), shown=(), run_time=1.5):
    """Finish `code` on screen: each (source, target glyphs) flies out of a copy of its source
    (P5) while `rest` fades in; then the glyph wrappers are swapped for the real Code."""
    anims = [TransformFromCopy(src, dst) for src, dst in pairs]
    anims += [FadeIn(r, shift=0.2 * LEFT) for r in rest]
    scene.play(*anims, run_time=run_time)
    scene.remove(*[d for _, d in pairs], *rest, *shown)
    scene.add(code)


class CheckedBeforeRuns(NarratedScene):
    def construct(self):
        self.compile_time()
        self.guarantee()
        self.read_nil()
        self.recap()
        self.teaser()
        # End card: the finished recap and the teaser hold, fully visible, under the music.
        self.wait(8.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.3)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # check.1: a timeline; the bad sum is stopped at the type check, the good one runs
    def compile_time(self):
        green = Line([TL_L, TL0, 0], [-0.08, TL0, 0], stroke_width=8, color=GREEN)
        blue = Arrow([0.08, TL0, 0], [TL_R, TL0, 0], buff=0, stroke_width=8, color=BLUE,
                     max_tip_length_to_length_ratio=0.05, max_stroke_width_to_length_ratio=10)
        gate = Circle(radius=0.36, color=GREEN, stroke_width=5).set_fill(BG, 1).move_to([GATE_X, TL0, 0])
        tick = check_mark(GREEN)
        tick.scale_to_fit_width(0.4).move_to(gate)
        play_tri = Triangle().set_fill(BLUE, 1).set_stroke(width=0).rotate(-PI / 2)
        play_tri.scale_to_fit_height(0.52).move_to([PLAY_X, TL0, 0])
        for m in (gate, tick, play_tri):
            m.set_z_index(2)
        comp_lab = T("compile time", size=36, color=GREEN).move_to([(TL_L - 0.08) / 2, TL0 + 0.55, 0])
        run_lab = T("run time", size=36, color=BLUE).move_to([(TL_R + 0.08) / 2, TL0 + 0.55, 0])
        timeline = [green, blue, gate, tick, play_tri, comp_lab, run_lab]

        bad = Code('hd ["cat"; "dog"] + 1', size=SUM)
        g(bad, "hd").set_color(YELLOW)
        bad.move_to([ROW_X, BAD_Y, 0], aligned_edge=LEFT)
        bad_call, bad_plus = g(bad, 'hd ["cat"; "dog"]'), g(bad, "+ 1")
        under = underline(bad_call, RED)
        err1 = Mono("Error: This expression has type string", size=30, t2c={"Error:": RED, "string": GREEN})
        err1.move_to([ROW_X, ERR_Y[0], 0], aligned_edge=LEFT)
        err2 = Mono("but an expression was expected of type int", size=30, t2c={"int": GREEN})
        err2.move_to([0, ERR_Y[1], 0]).align_to(select(err1, "This")[0], LEFT)   # as the toplevel indents it

        good = Code("hd [1; 2; 3] + 1".ljust(20) + "- : int = 2", size=SUM)
        g(good, "hd").set_color(YELLOW)
        good.move_to([ROW_X, GOOD_Y, 0], aligned_edge=LEFT)
        good_in = g(good, "hd [1; 2; 3] + 1")

        m_bad = Dot([START_X, TL_Y, 0], radius=0.15, color=YELLOW).set_z_index(3)
        x_bad = cross_mark(RED, r=0.24).move_to([STOP_X, TL_Y, 0]).set_z_index(2)
        m_good = Dot([START_X, TL_Y, 0], radius=0.15, color=YELLOW).set_z_index(4)

        with self.say("c2.check.1") as c:
            # "All of this type checking happens before your program runs, at what's called compile time."
            self.play(Create(green), time_span(AnimationGroup(GrowFromCenter(gate), Create(tick)), 0.7, 1.6),
                      run_time=1.6)
            c.wait_until("before your program runs")
            self.play(GrowArrow(blue), GrowFromCenter(play_tri), FadeIn(run_lab, shift=0.3 * DOWN), run_time=1.5)
            c.wait_until("compile time")
            self.play(FadeIn(comp_lab, shift=0.3 * DOWN), run_time=1.0)

            # "So suppose you take the head of cat and dog, and try to add one to it."  The timeline
            # moves up out of the way.
            c.wait_until("mix")
            self.play(*[m.animate.shift((TL_Y - TL0) * UP) for m in timeline],
                      time_span(FadeIn(bad_call, shift=0.25 * DOWN), 0.5, 1.5), run_time=1.5)
            c.wait_until("add one")
            self.play(FadeIn(bad_plus, shift=0.25 * DOWN), FadeIn(m_bad, scale=0.4), run_time=1.0)
            self.remove(bad_call, bad_plus)
            self.add(bad)

            # "OCaml rejects it straight away."  It is stopped at the check; it never reaches ▶.
            c.wait_until("reject")
            self.play(m_bad.animate.move_to([STOP_X, TL_Y, 0]), run_time=0.8)
            self.play(ReplacementTransform(m_bad, x_bad), Create(under),
                      LaggedStart(FadeIn(err1, shift=0.2 * DOWN), FadeIn(err2, shift=0.2 * DOWN), lag_ratio=0.35),
                      run_time=1.5)

            # "The head of a string list is a string, and you can't add a number to a string."
            c.wait_until("is a string")
            box = token_box(select(err1, "string")[0], err1)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("add a number")
            self.play(Transform(box, token_box(select(err2, "int")[0], err2)), run_time=1.0)

            # "Do the same sum with the list one, two, three instead, and it's fine."
            c.wait_until("fine")
            self.play(FadeOut(box), FadeIn(good_in, shift=0.25 * DOWN), FadeIn(m_good, scale=0.4), run_time=1.2)
            c.wait_until("and it's fine")
            rt = min(1.6, c.until("answer is two", floor=0.9))
            self.play(m_good.animate.move_to([RUN_X, TL_Y, 0]).set_color(GREEN),
                      time_span(FlashAround(gate, color=GREEN, time_width=1.5), 0.35 * rt, rt), run_time=rt)

            # "The answer is two."  It comes out of the run.
            c.wait_until("answer is two")
            build(self, good, pairs=[(m_good, g(good, "2", nth=1))], rest=[g(good, "- : int =")],
                  shown=[good_in], run_time=1.3)

        self.timeline = timeline
        self.gate, self.run_line = gate, blue

    # check.2: checking early buys guarantees; every element has the same type, so hd's is known
    def guarantee(self):
        chain = ConsChain([1, 2, 3]).scale(1.1).move_to([0, CH_Y, 0])
        tags = [Mono("int", size=32, color=GREEN).next_to(cell.box, DOWN, buff=0.25) for cell in chain.cells]
        head = chain.cells[0]
        val = value_label(1, size=46).move_to([head.box.get_x(), LIFT_Y, 0])
        val_tag = tags[0].copy().next_to(val, DOWN, buff=0.25)
        hd_arrow = Arrow(tags[0].get_bottom() + DOWN * 0.1, val.get_top() + UP * 0.15, buff=0,
                         color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.22)
        hd_lab = Mono("hd", size=34, color=YELLOW).next_to(hd_arrow, LEFT, buff=0.25)
        ghost = Code('"cat"', size=46).set_opacity(0.5).move_to([val.get_x() + 2.6, LIFT_Y, 0])
        ghost_tag = Mono("string", size=32, color=RED).next_to(ghost, DOWN, buff=0.25).align_to(val_tag, DOWN)
        no = Cross(ghost, stroke_color=RED, stroke_width=5, scale_factor=1.05)

        with self.say("c2.check.2") as c:
            # "Checking early buys you strong guarantees once the program does run."
            c.wait_until("strong guarantees")
            self.play(FlashAround(self.gate, color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until("does run")
            path = Line([0.3, TL_Y, 0], [TL_R - 0.2, TL_Y, 0]).set_stroke(GREEN, 12)
            self.play(VShowPassingFlash(path, time_width=0.5), run_time=1.3)

            # "For example, every element of a list is sure to have the same type."
            c.wait_until("same")
            sweep_clear(self, *set_alpha(self.timeline, 0.4),
                        time_span(FadeIn(chain, lag_ratio=0.15), 0.5, 1.6), keep=self.timeline, run_time=1.6)
            c.wait_until("same type")
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in tags], lag_ratio=0.25), run_time=1.2)

            # "So whatever the head function hands back, its type is already known."
            c.wait_until("hands back")
            self.play(GrowArrow(hd_arrow), FadeIn(hd_lab, shift=0.2 * RIGHT),
                      TransformFromCopy(head.label, val), TransformFromCopy(tags[0], val_tag), run_time=1.5)
            c.wait_until("already known")
            self.play(FlashAround(val_tag, color=GREEN, time_width=1.5), run_time=1.2)

            # "You'll never find a string where you expected a number."
            c.wait_until("never find")
            self.play(FadeIn(ghost, shift=0.2 * DOWN), FadeIn(ghost_tag, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("expected a number")
            self.play(Create(no), run_time=0.8)

    # check.3: [] : 'a list read at last; consing decides 'a; null [] never needs to
    def read_nil(self):
        rows = [session_row("[]", "- : 'a list = []"),
                session_row("1 :: []", "- : int list = [1]"),
                session_row('"cat" :: []', '- : string list = ["cat"]'),
                session_row("null []", "- : bool = true")]
        for row, y in zip(rows, S_Y):
            row.move_to([S_X, y, 0], aligned_edge=LEFT)
        g(rows[3], "null").set_color(YELLOW)
        r0 = rows[0]
        alpha = g(r0, "'a")
        box = token_box(g(r0, "'a list"), r0)
        dashed = DashedVMobject(token_box(alpha, r0, color=PINK).set_fill(opacity=0), num_dashes=18)
        dashed.set_stroke(PINK, 3)
        open_lab = T("still open", size=30, color=PINK).next_to(alpha, UP, buff=0.4)
        ins = [g(rows[1], "1 :: []"), g(rows[2], '"cat" :: []'), g(rows[3], "null []")]
        nil_ty = Code("'a list", size=30).next_to(g(rows[3], "[]"), DOWN, buff=0.3)

        def born(i, ty, item, item_src):
            """Row i's reply out of row 0's: '- :' and 'list =' carry over, 'a becomes `ty`,
            the [] opens around the consed item."""
            row = rows[i]
            brackets = VGroup(*g(row, "[", nth=1), *g(row, "]", nth=1))
            return [(g(r0, "- :"), g(row, "- :")), (alpha, g(row, ty)), (g(r0, "list ="), g(row, "list =")),
                    (g(r0, "[]", nth=1), brackets), (item_src, item)]

        with self.say("c2.check.3") as c:
            # "And now we can finally read a type from chapter one."
            c.wait_until("chapter one")
            rt = min(1.5, c.until("niltype", floor=1.0))
            sweep_clear(self, time_span(FadeIn(r0, shift=0.25 * DOWN), 0.45 * rt, rt), run_time=rt)

            # "The empty list has type alpha list."
            c.wait_until("niltype")
            self.play(FlashAround(g(r0, "[]"), color=TEAL, time_width=1.5), run_time=1.0)
            c.wait_until("alpha list")
            self.play(FadeIn(box), run_time=0.8)

            # "That's a list whose element type is still open."
            c.wait_until("element type")
            self.play(FadeTransform(box, dashed), run_time=1.0)
            c.wait_until("still open")
            self.play(FadeIn(open_lab, shift=0.25 * DOWN), run_time=1.0)

            # "Cons an integer onto it, and alpha becomes int."
            c.wait_until("int")
            self.play(FadeIn(ins[0], shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("alpha becomes int")
            build(self, rows[1], pairs=born(1, "int", g(rows[1], "1", nth=1), g(rows[1], "1")),
                  shown=[ins[0]], run_time=1.6)

            # "Cons a string onto it, and alpha becomes string."
            c.wait_until("string")
            self.play(FadeIn(ins[1], shift=0.25 * DOWN), run_time=0.8)
            c.wait_until("alpha becomes string")
            build(self, rows[2], pairs=born(2, "string", g(rows[2], '"cat"', nth=1), g(rows[2], '"cat"')),
                  shown=[ins[1]], run_time=1.3)

            # "And null of nil is simply true."  Its [] still has type 'a list.
            c.wait_until("null")
            self.play(FadeIn(ins[2], shift=0.25 * DOWN), TransformFromCopy(g(r0, "'a list"), nil_ty), run_time=1.4)
            c.wait_until("simply true")
            build(self, rows[3], rest=[g(rows[3], "- : bool = true")], shown=[ins[2]], run_time=1.0)

            # "Its alpha never gets decided, and it never needs to be."
            c.wait_until("its alpha")
            self.play(FlashAround(g(nil_ty, "'a"), color=PINK, time_width=1.5),
                      FlashAround(dashed, color=PINK, time_width=1.5), run_time=1.4)

    # recap.1: five lines, each on its cue while the one before steps back
    def recap(self):
        title = T("Recap", size=48).move_to([0, 3.25, 0])
        hd_nil, tl_nil = Code("hd []", size=32), Code("tl []", size=32)
        g(hd_nil, "hd").set_color(YELLOW)
        g(tl_nil, "tl").set_color(YELLOW)
        lines = [
            VGroup(T("Patterns take a list apart by shape:", size=34), Code("[]", size=32), T("or", size=34),
                   Code("x :: l", size=32)).arrange(RIGHT, buff=0.22),
            T("Clauses are tried in order; patterns name the parts", size=34),
            VGroup(hd_nil, T("and", size=34), tl_nil, T("raise an exception; OCaml warns first", size=34))
            .arrange(RIGHT, buff=0.22),
            VGroup(Code("'a", size=32), T("is a type variable: one function for every type", size=34))
            .arrange(RIGHT, buff=0.22),
            T("All of it is checked before the program runs", size=34, t2c={"checked": GREEN}),
        ]
        rows = VGroup(*[VGroup(Dot(radius=0.07, color=BLUE), ln).arrange(RIGHT, buff=0.3) for ln in lines])
        left = -max(r.width for r in rows) / 2
        for i, r in enumerate(rows):
            r.move_to([left, 2.4 - 0.6 * i, 0], aligned_edge=LEFT)

        with self.say("c2.recap.1") as c:
            # "Let's recap."
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("r1")
            sweep_clear(self, time_span(FadeIn(rows[0], shift=0.25 * UP, lag_ratio=0.02), 0.6, 1.6),
                        keep=[title], run_time=1.6)
            for i, cue in enumerate(("r2", "r3", "r4", "r5"), start=1):
                c.wait_until(cue)
                self.play(FadeIn(rows[i], shift=0.25 * UP, lag_ratio=0.02),
                          rows[i - 1].animate.set_opacity(0.5), run_time=1.5)
        self.rows = rows

    # recap.2: the teaser: how many cells, when you can only see the first?
    def teaser(self):
        nxt = VGroup(T("Next:", size=40, color=DIM), T("the length of a list", size=40, color=YELLOW))
        nxt.arrange(RIGHT, buff=0.25).move_to([0, -0.95, 0])
        q = T("how many?", size=36, color=GOLD).move_to([0, -1.75, 0])
        chain = ConsChain([5, 6, 7]).scale(0.8).move_to([0, -2.65, 0])
        first = chain.cells[0]

        with self.say("c2.recap.2") as c:
            # "Next time, we'll put patterns and recursion together."  The recap comes back to full.
            self.play(*[r.animate.set_opacity(1) for r in self.rows[:4]], FadeIn(nxt, shift=0.25 * UP), run_time=1.2)

            # "How do you count the elements of a list, when all you can see is its first cell?"
            c.wait_until("count")
            self.play(FadeIn(chain, lag_ratio=0.1), FadeIn(q, shift=0.25 * DOWN), run_time=1.4)
            c.wait_until("all you can see")
            self.play(first.box.animate.set_stroke(YELLOW), first.ptr.animate.set_stroke(YELLOW),
                      *set_alpha([*chain.cells[1:], *chain.arrows, chain.nil], DIMMED), run_time=1.2)

            # "We'll write a function that computes the length of any list."
            c.wait_until("the length")
            self.play(FlashAround(select(nxt[1], "length")[0], color=YELLOW, time_width=1.5), run_time=1.4)
