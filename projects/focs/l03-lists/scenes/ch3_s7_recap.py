"""Chapter 3, scene 7: the wrapper `length` that supplies addlen's zero (addlen 10 gives 13, the
wrong start; length gives 4, type 'a list -> int like nlength), the recap, and the chapter's end
card with the chapter 4 teaser (append's two chains joining, a list flipping under "how slow?").
Clips c3.wrap.1, c3.recap.1 – c3.recap.2 (the chapter's last scene).

Replies (trivial, as the brief quotes them): let length xs = addlen 0 xs ->
val length : 'a list -> int = <fun>; addlen 10 [5; 6; 7] -> - : int = 13;
length [5; 6; 7; 8] -> - : int = 4.

STATUS: done; tools/check.py clean (88.1 s render vs 75.7 s narration + gaps + 2 s breath after
the wrapper + 8 s end card). Opens on addlen_code(ADDLEN, 40) at UP * 0.15 = s6's last shot.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

ADDLEN = "let rec addlen n = function\n  | []    -> n\n  | x::xs -> addlen (n + 1) xs"

# ── layout ──────────────────────────────────────────────────────────────────────
DEF_CUT, DEF_Y0, DEF_TOP = 0.15, 1.9, 2.75   # addlen's code: where s6 left it, lifted, then shrunk to the top
CALL_Y = (-0.15, -0.95, -1.75)      # the three "addlen 0 ..." calls
LDEF_Y, REPLY_Y, GHOST_Y = 1.15, 0.4, -0.2
ROW_SIZE, PAD = 32, 21              # session rows: input padded so the replies form a column
ROW1_Y, ROW2_Y = -1.35, -2.65
NEXT_Y, JOIN_Y, REV_Y = -0.95, -2.0, -3.05  # teaser rows under the recap
HEAD_X, CHAIN_L, CH_S = -4.6, -2.1, 0.8     # teaser: header column, chains' left edge, chain scale
SECTION_BREATH = 2.0                        # a still beat after the wrapper's payoff, before the recap


def g(code, sub, nth=0):
    """Glyphs of a substring of a Code, as a fresh VGroup."""
    return VGroup(*code.find(sub, nth=nth))


def addlen_code(src, size):
    """addlen's code as in ch3_s6: the count `n` in GOLD, the name in YELLOW."""
    code = Code(src, size=size)
    for m in re.finditer(r"\bn\b", code.src):
        code._span(m.start(), m.end()).set_color(GOLD)
    for m in re.finditer(r"\baddlen\b", code.src):
        code._span(m.start(), m.end()).set_color(YELLOW)
    return code


def named(src, size, *names):
    code = Code(src, size=size)
    for nm in names:
        g(code, nm).set_color(YELLOW)
    return code


def cost(big, word, color=GOLD, size=34):
    o = MathTex(big, font_size=size + 8, color=color)
    w = T(word, size=size, color=color)
    grp = VGroup(o, w).arrange(RIGHT, buff=0.2)
    w.align_to(o, DOWN).shift(UP * 0.06)
    return grp


class WrapperAndRecap(NarratedScene):
    def construct(self):
        self.wrapper()
        self.recap()
        self.teaser()
        # End card: the finished recap and the teaser hold, fully visible, under the music.
        self.wait(8.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.3)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # ── wrap.1: length supplies the zero; the wrong start; the type ────────────────
    def wrapper(self):
        code = addlen_code(ADDLEN, 40).move_to(UP * DEF_CUT)   # exactly s6's last shot
        left = code.get_left()[0]
        calls = [named(f"addlen 0 {lst}", 36, "addlen").move_to([left, y, 0], aligned_edge=LEFT)
                 for lst, y in zip(("[5; 6; 7]", "[8; 9]", "[4]"), CALL_Y)]

        ldef = named("let length xs = addlen 0 xs", 40, "addlen").move_to([0, LDEF_Y, 0])
        zero = g(ldef, "0")
        reply = Code("val length : 'a list -> int = <fun>", size=32)
        reply.move_to([ldef.get_left()[0], REPLY_Y, 0], aligned_edge=LEFT)
        g(reply, "length").set_color(YELLOW)
        ghost = Code("val nlength : 'a list -> int = <fun>", size=32).move_to([0, GHOST_Y, 0])
        g(ghost, "nlength").set_color(YELLOW)
        ghost.shift(RIGHT * (g(reply, "'a list -> int").get_x() - g(ghost, "'a list -> int").get_x()))
        ghost.set_opacity(0.45)

        row_x = ldef.get_left()[0]
        row1 = named("addlen 10 [5; 6; 7]".ljust(PAD) + "- : int = 13", ROW_SIZE, "addlen")
        row1.move_to([row_x, ROW1_Y, 0], aligned_edge=LEFT)
        row2 = named("length [5; 6; 7; 8]".ljust(PAD) + "- : int = 4", ROW_SIZE, "length")
        row2.move_to([row_x, ROW2_Y, 0], aligned_edge=LEFT)
        box = token_box(row1.find("10"), row1, color=RED)
        wrong = T("wrong start", size=30, color=RED).next_to(box, DOWN, buff=0.15)
        space = cost(r"O(1)", "space").next_to(g(row2, "- : int = 4"), RIGHT, buff=0.6)

        with self.say("c3.wrap.1") as c:
            # "There's one small annoyance left."  addlen fades back in where s6 left it, then
            # lifts to make room for three calls to it.
            self.play(FadeIn(code), run_time=1.0)
            self.play(code.animate.move_to([0, DEF_Y0, 0]),
                      *[time_span(FadeIn(cl, shift=0.2 * UP), 0.4 + 0.3 * i, 1.1 + 0.3 * i)
                        for i, cl in enumerate(calls)], run_time=min(1.7, c.until("every time") - 0.4))

            # "Nobody wants to pass in a zero every time they ask for a length."
            c.wait_until("every time")
            self.play(*[FlashAround(g(cl, "0"), color=GOLD, time_width=1.5) for cl in calls],
                      run_time=min(1.4, 0.9 * c.until("wrap")))

            # "So we wrap add-len in a tiny function, called length, that supplies the zero for us."
            c.wait_until("wrap")
            self.play(code.animate.scale(0.8).move_to([0, DEF_TOP, 0]),
                      run_time=min(1.2, 0.8 * c.until("called length")))
            c.wait_until("called length")
            rest = [g(ldef, "let length xs ="), g(ldef, "xs", nth=1)]
            dst = g(ldef, "addlen 0")
            self.play(TransformFromCopy(g(calls[0], "addlen 0"), dst), *[FadeOut(cl) for cl in calls],
                      *[FadeIn(r, shift=0.2 * DOWN) for r in rest], run_time=1.6)
            self.remove(dst, *rest)
            self.add(ldef)

            # "That zero matters, because it's where the count starts."  0 and the count n flash.
            c.wait_until("start")
            n0 = code._span(ADDLEN.index(" n ") + 1, ADDLEN.index(" n ") + 2)
            self.play(FlashAround(zero, color=GOLD, time_width=1.5),
                      FlashAround(n0, color=GOLD, time_width=1.5), run_time=1.6)

            # "Start at ten instead, and add-len of ten, and the list five, six, seven, gives thirteen."
            c.wait_until("ten")
            in1 = [g(row1, "addlen"), g(row1, "[5; 6; 7]")]
            ten = g(row1, "10")
            self.play(TransformFromCopy(zero, ten), *[FadeIn(p, shift=0.2 * UP) for p in in1],
                      run_time=1.5)
            c.wait_until("gives thirteen")
            rep1 = g(row1, "- : int = 13")
            self.play(FadeIn(rep1, shift=0.2 * LEFT), Create(box),
                      time_span(FadeIn(wrong, shift=0.2 * DOWN), 0.4, 1.2),
                      run_time=min(1.2, 0.9 * c.until("four")))
            self.remove(ten, rep1, *in1)
            self.add(row1)

            # "With the wrapper, length of five, six, seven, eight gives four."
            c.wait_until("four")
            nm2 = g(row2, "length")
            lst2 = g(row2, "[5; 6; 7; 8]")
            self.play(*set_alpha([row1, wrong], 0.45),
                      box.animate.set_stroke(opacity=0.45).set_fill(opacity=0.11),
                      TransformFromCopy(g(ldef, "length"), nm2), FadeIn(lst2, shift=0.2 * UP),
                      run_time=1.5)
            c.wait_until("gives four")
            rep2 = g(row2, "- : int = 4")
            self.play(FadeIn(rep2, shift=0.2 * LEFT), run_time=1.0)
            self.remove(nm2, lst2, rep2)
            self.add(row2)

            # "And its type is alpha list to int, just like en-length."
            c.wait_until("type")
            self.play(FadeIn(reply, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("just like")
            self.play(FadeIn(ghost, shift=0.2 * UP), run_time=0.8)

            # "Same answer, in constant space."
            c.wait_until("same answer")
            self.play(FlashAround(g(row2, "4"), color=GOLD, time_width=1.5),
                      FadeIn(space, shift=0.2 * LEFT), run_time=1.2)
        self.wait(SECTION_BREATH)
        self.payoff = [ldef, reply, ghost, row2, space]

    # ── recap.1: five lines, each on its cue while the one before steps back ───────
    def recap(self):
        title = T("Recap", size=48).move_to([0, 3.25, 0])
        nl = Code("nlength", size=32).set_color(YELLOW)
        lines = [
            [T("Recursion follows the list's shape:", size=34), Code("[]", size=32), T("and", size=34),
             Code("x :: xs", size=32)],
            [T("All the clauses go in one definition, split by", size=34), Code("|", size=32)],
            [T("A second", size=34), Code("let", size=32), T("replaces the first", size=34, disable_ligatures=True)],
            [nl, T("takes any", size=34), Code("'a list", size=32), T("but needs", size=34),
             *cost(r"O(n)", "space")],
            [T("An accumulator works as it goes:", size=34), *cost(r"O(n)", "time,"),
             *cost(r"O(1)", "space")],
        ]
        rows = []
        for ln in lines:
            body = VGroup(*ln).arrange(RIGHT, buff=0.22)
            rows.append(VGroup(Dot(radius=0.07, color=BLUE), *body))
            rows[-1][0].next_to(body, LEFT, buff=0.3)
        rows = VGroup(*rows)
        # a cost's word sits a touch low beside its O(..): keep that baseline tweak
        for row in rows[3:]:
            for i, m in enumerate(row):
                if isinstance(m, MathTex) and i + 1 < len(row):
                    row[i + 1].align_to(m, DOWN).shift(UP * 0.06)
        left = -max(r.width for r in rows) / 2
        for i, r in enumerate(rows):
            r.move_to([left, 2.4 - 0.6 * i, 0], aligned_edge=LEFT)

        def part(row, a, b, run_time):
            self.play(*[FadeIn(m, shift=0.25 * UP) for m in row[a:b]], run_time=run_time)

        with self.say("c3.recap.1") as c:
            # "Let's recap."  The top clears for the title; the wrapper's payoff stays a moment.
            sweep_clear(self, time_span(FadeIn(title, shift=0.3 * DOWN), 0.4, 1.0), keep=self.payoff,
                        run_time=min(1.0, c.until("r1")))

            # "A recursive function on lists follows the shape of the list, with a clause for the
            # empty list, and a clause for a head on a tail."
            c.wait_until("r1")
            sweep_clear(self, time_span(FadeIn(rows[0], shift=0.25 * UP, lag_ratio=0.02), 0.5, 1.7),
                        keep=[title], run_time=1.7)
            c.wait_until("the empty list")
            self.play(FlashAround(rows[0][2], color=TEAL, time_width=1.5), run_time=1.2)
            c.wait_until("a head on a tail")
            self.play(FlashAround(rows[0][4], color=TEAL, time_width=1.5), run_time=1.2)

            # "The clauses belong in a single definition, separated by vertical bars."
            c.wait_until("r2")
            self.play(FadeIn(rows[1], shift=0.25 * UP, lag_ratio=0.02),
                      rows[0].animate.set_opacity(0.5), run_time=1.5)
            c.wait_until("vertical bars")
            self.play(FlashAround(rows[1][2], color=YELLOW, time_width=1.5), run_time=1.0)

            # "A second let doesn't extend the first.  It replaces it."
            c.wait_until("a second let")
            self.play(FadeIn(rows[2], shift=0.25 * UP, lag_ratio=0.02),
                      rows[1].animate.set_opacity(0.5), run_time=1.5)
            c.wait_until("it replaces it")
            self.play(FlashUnder(select(rows[2][3], "replaces")[0], color=YELLOW), run_time=1.2)

            # "En-length works on lists of any type, but it leaves an addition waiting for every
            # element, so it needs big O of en space."
            c.wait_until("r3")
            self.play(*[FadeIn(m, shift=0.25 * UP) for m in rows[3][:4]],
                      rows[2].animate.set_opacity(0.5), run_time=1.5)
            c.wait_until("so it needs")
            part(rows[3], 4, 7, 1.2)
            settle(self, rows[3])

            # "An accumulator does the work as it goes.  Add-len still takes big O of en time, but
            # only constant space."
            c.wait_until("r4")
            self.play(*[FadeIn(m, shift=0.25 * UP) for m in rows[4][:2]],
                      rows[3].animate.set_opacity(0.5), run_time=1.5)
            c.wait_until("still takes")
            part(rows[4], 2, 4, 1.0)
            c.wait_until("only constant")
            part(rows[4], 4, 6, 1.0)
            settle(self, rows[4])
        self.rows = rows

    # ── recap.2: the teaser: append joins two chains; reverse, and how slow? ───────
    def teaser(self):
        nxt = VGroup(T("Next:", size=40, color=DIM), T("append and reverse", size=40, color=YELLOW))
        nxt.arrange(RIGHT, buff=0.25).move_to([0, NEXT_Y, 0])

        app = Code("[1; 2; 3] @ [4]", size=32).move_to([HEAD_X, JOIN_Y, 0])
        a = ConsChain([1, 2, 3]).scale(CH_S)
        b = ConsChain([4], color=TEAL).scale(CH_S)
        VGroup(a, b).arrange(RIGHT, buff=0.45).move_to([CHAIN_L, JOIN_Y, 0], aligned_edge=LEFT)
        joined = ConsChain([1, 2, 3, 4]).scale(CH_S)
        joined.shift(a.cells[0].get_center() - joined.cells[0].get_center())
        delta = joined.cells[3].get_center() - b.cells[0].get_center()

        slow = T("how slow?", size=36, color=GOLD).move_to([HEAD_X, REV_Y, 0])
        rv = ConsChain([1, 2, 3]).scale(CH_S).move_to([CHAIN_L, REV_Y, 0], aligned_edge=LEFT)
        l0, l2 = rv.cells[0].label, rv.cells[2].label
        for lab in (l0, l2):
            lab.set_z_index(2)     # above the other cells' opaque boxes while they swap

        with self.say("c3.recap.2") as c:
            # "Next time, we'll write our own function for joining two lists end to end."
            self.play(*[r.animate.set_opacity(1) for r in self.rows[:4]],
                      FadeIn(nxt, shift=0.25 * UP), run_time=1.2)
            c.wait_until("our own function")
            self.play(FadeIn(app, shift=0.2 * UP), FadeIn(a, lag_ratio=0.1), FadeIn(b, lag_ratio=0.1),
                      run_time=min(1.3, 0.8 * c.until("end to end")))
            c.wait_until("end to end")
            self.play(a.nil.animate.set_opacity(0), b.animate.shift(delta),
                      Transform(a.arrows[2], joined.arrows[2]),
                      run_time=min(1.5, 0.9 * c.until("rev")))

            # "And we'll see why the obvious way to reverse a list turns out to be surprisingly slow."
            c.wait_until("rev")
            self.play(FadeIn(rv, lag_ratio=0.1), run_time=1.0)
            c.wait_until("reverse a list")
            p0, p2 = l0.get_center(), l2.get_center()
            self.play(l0.animate(path_arc=-PI / 3).move_to(p2), l2.animate(path_arc=-PI / 3).move_to(p0),
                      run_time=1.5)
            c.wait_until("surprisingly slow")
            self.play(FadeIn(slow, shift=0.25 * DOWN), run_time=1.0)
