"""Chapter 1, scene 7: off the end of the list, where take and drop get used, and the recap.
Clips c1.edges.1 – c1.edges.3 (the chapter's last scene).

Layout
- edges.1: the short chain 3 -> 5 -> 9 -> [] (library default size) across the top; under it the
  toplevel in two columns, take's on the left, drop's on the right (Code 30). Count 10 first (with
  a YELLOW copy of the chain under the original), then the copy clears, the 10 row rises and the
  0 and (-1) rows fill in, boxed GOLD with "i <= 0". On {nofail} the chain gives way to the head and
  nil clause of both functions, whose `| [] -> []` lines glow TEAL; GREEN "no exception" below.
- edges.2: scene 1's running chain at ORIGIN; DIM cut in the middle, which slides to scene 1's GOLD
  cut after the 5 on "rounded down"; `List.length xs / 2` under the chain; take 2 xs / drop 2 xs
  rise over their halves.
- edges.3: the recap (L3 pattern: "Recap" 48, BLUE bullets, T 34 / Mono 32, costs GOLD), then
  the end card: the running chain at ORIGIN, GOLD marker over the 9, "Is 9 in this list?"
  (ch2's hook shot) and "Next: searching a list"; holds END_CARD s, then clears.

STATUS: check clean apart from small dwell shortfalls at clip boundaries (drop 2 xs block 3.7 s
before the recap clears it; "no exception" 4.2 s into edges.2's sweep).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── shared with scene 1 (one place) ────────────────────────────────────────────
SHORT = [3, 5, 9]
RUN = [3, 5, 9, 4, 7]
CUT_HALF = 1.05            # the cut runs +-1.05 about the chain's centre line
CUT_DASH = 0.12
CUT_WIDTH = 5

# ── this scene's layout ────────────────────────────────────────────────────────
SHORT_Y = 2.65             # short chain across the top (edges.1)
COPY_Y = 1.2               # take 10's fresh copy, under it
GRID = 30                  # toplevel code size in the two columns
TAKE_X, DROP_X = -6.4, 0.3 # left edges of take's and drop's columns
ROW_Y = [1.15, -0.15, -1.45]
RISE = 1.25                # the 10 row starts this much lower, under the copy
SNIP_Y = 2.8               # the two functions' heads, where the chain was
OK_Y = -3.1                # "no exception"
END_CARD = 7.6             # the end card holds this long after the last clip's tail


def lines_of(src, size, left=None, cy=0.0, cx=0.0):
    """Lay out `src` as one Code (exact pitch and indentation), then hand back each line as
    its own top-level copy, so lines can enter, move and fade independently."""
    code = Code(src, size=size)
    code.move_to([cx, cy, 0])
    if left is not None:
        code.align_to(np.array([left, 0, 0]), LEFT)
    return code, [code.line(i).copy() for i in range(src.count("\n") + 1)]


def part(code, lines, i, s, nth=0):
    """Glyphs of substring `s` in line i, picked from the copied line."""
    full = list(code.line(i))
    return VGroup(*[lines[i][full.index(g)] for g in code.find(s, line=i, nth=nth)])


def span(anim, a, b, rt):
    """time_span by fractions of the play's run_time, so a shortened play still completes it."""
    return time_span(anim, a * rt, b * rt)


def tag(text, color, size=30):
    """A small outlined pill (ch2's style), here for the forward link."""
    t = T(text, size=size, color=color)
    pill = RoundedRectangle(corner_radius=0.22, width=t.width + 0.55, height=t.height + 0.36,
                            stroke_color=color, stroke_width=2.5).set_fill(color, opacity=0.10)
    pill.move_to(t)
    return VGroup(pill, t)


def cost(big, word, size=34):
    return [MathTex(big, font_size=size + 8, color=GOLD), T(word, size=size, color=GOLD)]


def key(name):
    return Mono(f"{name}:", size=38, t2c={name: YELLOW})


def cut_at(x, color=GOLD, width=CUT_WIDTH):
    return DashedLine([x, CUT_HALF, 0], [x, -CUT_HALF, 0], dash_length=CUT_DASH,
                      color=color, stroke_width=width)


class Edges(NarratedScene):
    def construct(self):
        self.past_the_end()
        self.where_used()
        self.recap()
        # End card: the running chain, the pointer and the question hold under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── edges.1: more than the list has; zero and negative counts; no exception ──────────
    def past_the_end(self):
        short = ConsChain(SHORT).move_to([0, SHORT_Y, 0])
        copy = ConsChain(SHORT, color=YELLOW).move_to([0, COPY_Y, 0])
        copy_lab = T("a copy", size=32, color=YELLOW).next_to(copy, RIGHT, buff=0.4)

        take_src = ["take 10 [3; 5; 9]\n- : int list = [3; 5; 9]",
                    "take 0 [3; 5; 9]\n- : int list = []",
                    "take (-1) [3; 5; 9]\n- : int list = []"]
        drop_src = ["drop 10 [3; 5; 9]\n- : int list = []",
                    "drop 0 [3; 5; 9]\n- : int list = [3; 5; 9]",
                    "drop (-1) [3; 5; 9]\n- : int list = [3; 5; 9]"]
        lift = [-RISE, 0, 0]
        take = [lines_of(s, GRID, TAKE_X, ROW_Y[k] + lift[k]) for k, s in enumerate(take_src)]
        drop = [lines_of(s, GRID, DROP_X, ROW_Y[k] + lift[k]) for k, s in enumerate(drop_src)]
        tl = [ln for _, ln in take]     # tl[row][0] input, tl[row][1] reply
        dl = [ln for _, ln in drop]
        ten = part(take[0][0], tl[0], 0, "10")

        low = [*tl[1], *tl[2], *dl[1], *dl[2]]
        top = max(m.get_top()[1] for m in [*tl[1], *dl[1]]) + 0.16
        bot = min(m.get_bottom()[1] for m in [*tl[2], *dl[2]]) - 0.16
        right = max(m.get_right()[0] for m in low) + 0.2
        left = TAKE_X - 0.2
        box = RoundedRectangle(corner_radius=0.18, width=right - left, height=top - bot)
        box.move_to([(left + right) / 2, (top + bot) / 2, 0]).set_stroke(GOLD, 2.5).set_fill(opacity=0)
        le0 = MathTex(r"i \le 0", font_size=42, color=GOLD).next_to(box, DOWN, buff=0.14)

        snip_t = lines_of("let rec take i = function\n  | [] -> []", GRID, TAKE_X, SNIP_Y)[1]
        snip_d = lines_of("let rec drop i = function\n  | [] -> []", GRID, DROP_X, SNIP_Y)[1]
        ok = VGroup(check_mark(GREEN), T("no exception", size=36, color=GREEN))
        ok.arrange(RIGHT, buff=0.22).move_to([0, OK_Y, 0])

        with self.say("c1.edges.1") as c:
            # {off} "What if you ask for more elements than the list has?"
            self.play(FadeIn(short, shift=0.3 * UP), run_time=1.0)
            c.wait_until("ask for more")
            self.play(FadeIn(tl[0][0], shift=0.25 * DOWN), run_time=min(1.0, c.until("than the list")))
            c.wait_until("than the list")
            self.play(FlashAround(ten, color=GOLD, time_width=1.5),
                      run_time=min(1.4, 0.9 * c.until("takeall")))

            # {takeall} "Take ten, of three, five, nine, gives three, five, nine, a fresh copy ..."
            c.wait_until("gives three")
            self.play(FadeIn(tl[0][1], shift=0.25 * DOWN), run_time=min(1.0, c.until("nine a fresh")))
            c.wait_until("nine a fresh")
            rt = min(1.6, 0.9 * c.until("dropall"))
            self.play(*[TransformFromCopy(a, b) for a, b in zip(short.cells, copy.cells)],
                      *[ReplacementTransform(a.copy(), b) for a, b in zip(short.arrows, copy.arrows)],
                      TransformFromCopy(short.nil, copy.nil),
                      span(FadeIn(copy_lab, shift=0.3 * LEFT), 0.55, 1.0, rt),
                      run_time=rt)
            settle(self, copy)

            # {dropall} "And drop ten gives nil."
            c.wait_until("dropall")
            self.play(FadeIn(dl[0][0], shift=0.25 * DOWN), run_time=min(0.9, c.until("gives nil")))
            c.wait_until("gives nil")
            self.play(FadeIn(dl[0][1], shift=0.25 * DOWN), run_time=min(0.9, 0.9 * c.until("zero")))

            # {zero} "With a count of zero, or a negative count, take gives nil, and drop gives the
            # whole list back."  The copy goes, the 10 row rises; the 0 inputs come in under it.
            c.wait_until("zero")
            self.play(time_span(FadeOut(copy), 0, 0.7), time_span(FadeOut(copy_lab), 0, 0.7),
                      *[time_span(m.animate.shift(RISE * UP), 0.2, 1.1) for m in [*tl[0], *dl[0]]],
                      time_span(FadeIn(tl[1][0], shift=0.25 * DOWN), 0.8, 1.6),
                      time_span(FadeIn(dl[1][0], shift=0.25 * DOWN), 0.9, 1.7),
                      run_time=1.7)
            c.wait_until("or a negative")
            rt = min(1.2, 0.9 * c.until("take gives nil"))
            self.play(FadeIn(tl[2][0], shift=0.25 * DOWN), FadeIn(dl[2][0], shift=0.25 * DOWN),
                      span(Create(box), 0.25, 1.0, rt), span(FadeIn(le0, shift=0.2 * UP), 0.5, 1.0, rt),
                      run_time=rt)
            c.wait_until("take gives nil")
            self.play(LaggedStart(FadeIn(tl[1][1], shift=0.25 * DOWN), FadeIn(tl[2][1], shift=0.25 * DOWN),
                                  lag_ratio=0.3),
                      run_time=min(1.1, 0.9 * c.until("and drop gives")))
            c.wait_until("and drop gives")
            self.play(LaggedStart(FadeIn(dl[1][1], shift=0.25 * DOWN), FadeIn(dl[2][1], shift=0.25 * DOWN),
                                  lag_ratio=0.3),
                      run_time=min(1.1, 0.9 * c.until("nofail")))

            # {nofail} "Either way, the nil clause catches the end of the list, so neither function
            # ever raises an exception."  The functions' heads take the chain's place.
            c.wait_until("nofail")
            self.play(span(FadeOut(short, shift=0.3 * UP), 0, 0.55, 1.4),
                      *[span(FadeIn(m, shift=0.2 * DOWN), 0.3 + 0.07 * k, 0.8 + 0.07 * k, 1.4)
                        for k, m in enumerate([snip_t[0], snip_d[0], snip_t[1], snip_d[1]])],
                      run_time=1.4)
            c.wait_until("the nil clause")
            self.play(snip_t[1].animate.set_color(TEAL), snip_d[1].animate.set_color(TEAL),
                      FlashAround(snip_t[1], color=TEAL, time_width=1.5),
                      FlashAround(snip_d[1], color=TEAL, time_width=1.5),
                      run_time=min(1.5, 0.9 * c.until("neither function")))
            c.wait_until("neither function")
            self.play(FadeIn(ok, shift=0.25 * UP), run_time=1.0)

    # ── edges.2: where they are used: split in half (merge sort, next lecture) ──────────
    def where_used(self):
        run = ConsChain(RUN)
        cells = run.cells
        x_cut = (cells[1].ptr.get_right()[0] + cells[2].box.get_left()[0]) / 2   # -1.774
        mid = cut_at(0.0, color=DIM, width=4)
        cut = cut_at(x_cut)
        xs = label_pointer("xs", cells[0], direction=DOWN)
        merge = tag("Lecture 5: merge sort", DIM).move_to([0, 3.15, 0])
        _, half = lines_of("List.length xs / 2\n- : int = 2", 40, cy=-2.25)
        _, tk = lines_of("take 2 xs\n- : int list = [3; 5]", 32, -6.45, 1.9)
        _, dp = lines_of("drop 2 xs\n- : int list = [9; 4; 7]", 32, -0.3, 1.9)

        with self.say("c1.edges.2") as c:
            # {use} "So where would you use them?"  The board holds through the question; on
            # "Typically" scene 1's running chain comes back.
            c.wait_until("typically")
            rt = min(1.4, 0.9 * c.until("into equal parts"))
            sweep_clear(self, span(FadeIn(run, shift=0.3 * UP), 0.35, 1.0, rt), run_time=rt)

            # "Typically, to split a collection into equal parts, and process each part recursively."
            c.wait_until("into equal parts")
            self.play(Create(mid), run_time=min(1.0, c.until("half")))

            # {half} "In the next lecture, merge sort does exactly that."
            c.wait_until("merge sort")
            self.play(FadeIn(merge, shift=0.25 * DOWN), run_time=1.0)

            # "It takes half the length, and half of five, rounded down, is two."
            c.wait_until("half the length")
            self.play(FadeIn(half[0], shift=0.25 * DOWN), FadeIn(xs, shift=0.2 * UP),
                      run_time=min(1.2, 0.9 * c.until("rounded down")))
            c.wait_until("rounded down")
            self.play(ReplacementTransform(mid, cut), run_time=min(1.3, max(0.6, c.until("is two"))))
            c.wait_until("is two")
            self.play(FadeIn(half[1], shift=0.25 * DOWN), run_time=min(0.9, 0.9 * c.until("so take gives")))

            # {split} "So take gives three, five, and drop gives nine, four, seven."
            c.wait_until("so take gives")
            rt = min(1.3, 0.9 * c.until("and drop gives"))
            self.play(span(FadeIn(tk[0], shift=0.4 * UP), 0, 0.8, rt), span(FadeIn(tk[1], shift=0.4 * UP), 0.2, 1.0, rt),
                      *flash([cells[0], cells[1]], YELLOW, time_width=1.5),
                      run_time=rt)
            c.wait_until("and drop gives")
            rt = min(1.1, 0.9 * c.remaining)
            self.play(span(FadeIn(dp[0], shift=0.4 * UP), 0, 0.8, rt), span(FadeIn(dp[1], shift=0.4 * UP), 0.2, 1.0, rt),
                      *flash([cells[2], cells[3], cells[4]], YELLOW, time_width=1.5),
                      run_time=rt)
        self.merge = merge
        self.run = run

    # ── edges.3: the recap, then the end card (ch2's hook shot) ─────────────────────────
    def recap(self):
        run = self.run
        title = T("Recap", size=48).move_to([0, 3.15, 0])
        R = 40                                    # recap text size (L3's 34, scaled up ~18%)
        specs = [
            [key("take"), T("the front", size=R), T("·", size=R, color=DIM), key("drop"),
             T("the rest", size=R)],
            [key("take"), T("waiting conses + a copy", size=R)],
            [*cost(r"O(i)", "time and space", R)],
            [key("drop"), T("iterative,", size=R), T("1 new cell,", size=R), T("shares the rest", size=R)],
            [*cost(r"O(i)", "time,", R), *cost(r"O(1)", "space", R)],
            [T("past the end: they stop,", size=R), T("no exception", size=R, color=GREEN)],
        ]
        SUB = (2, 4)                              # cost lines: no bullet, under their row's text
        rows = []
        for k, ln in enumerate(specs):
            body = VGroup(*ln).arrange(RIGHT, buff=0.24)
            for i, m in enumerate(body):          # a cost's word sits on its O(..)'s baseline
                if isinstance(m, MathTex) and i + 1 < len(body):
                    body[i + 1].align_to(m, DOWN).shift(UP * 0.07)
            if k == 3:                            # commas drop the bbox: share one cap line
                body[1].align_to(body[2], UP)
                body[3].align_to(body[2], UP)
            if k in SUB:
                rows.append(body)
            else:
                dot = Dot(radius=0.08, color=BLUE).next_to(body, LEFT, buff=0.32)
                rows.append(VGroup(dot, *body))
        rows = VGroup(*rows)
        left = -max(r.width for r in rows) / 2
        for r, y in zip(rows, [2.2, 1.35, 0.72, -0.15, -0.78, -1.65]):
            r.move_to([left, y, 0], aligned_edge=LEFT)
        rows[2].align_to(rows[1][2], LEFT)        # under "waiting conses"
        rows[4].align_to(rows[3][2], LEFT)        # under "iterative,"

        pointer = marker(GOLD, scale=0.24).move_to(above(run.cells[2].box))
        question = T("Is 9 in this list?", size=50, color=YELLOW, t2c={"9": GOLD}).move_to(UP * 2.35)
        nxt = VGroup(T("Next:", size=36, color=DIM), T("searching a list", size=36))
        nxt.arrange(RIGHT, buff=0.25).move_to(DOWN * 2.45)
        RUN_LOW = 2.9                                # the chain waits under the recap at y = -RUN_LOW

        def show(row, a, b, run_time, dim=None):
            anims = [FadeIn(m, shift=0.25 * UP) for m in row[a:b]]
            if dim is not None:
                anims += [r.animate.set_opacity(0.5) for r in dim]
            self.play(*anims, run_time=run_time)

        with self.say("c1.edges.3") as c:
            # {recap} "Let's recap."  The forward-link tag gives way to the title; the split holds.
            rt = min(1.1, 0.9 * c.until("r1"))
            self.play(span(FadeOut(self.merge, shift=0.3 * UP), 0, 0.6, rt),
                      span(FadeIn(title, shift=0.3 * DOWN), 0.35, 1.0, rt), run_time=rt)

            # {r1} "Take returns the front of a list, and drop returns the rest."  The board
            # clears as the first line comes in.
            c.wait_until("r1")
            rt = min(1.6, 0.95 * c.until("and drop returns"))
            sweep_clear(self, *[span(FadeIn(m, shift=0.25 * UP), 0.45, 1.0, rt) for m in rows[0][0:3]],
                        keep=[title], run_time=rt)
            c.wait_until("and drop returns")
            show(rows[0], 3, 6, min(1.2, 0.9 * c.until("r2")))
            settle(self, rows[0])

            # {r2} "Take leaves a cons waiting for every element it takes, and copies each one,
            # so it needs big O of eye time and space."
            c.wait_until("r2")
            show(rows[1], 0, 3, 1.4, dim=[rows[0]])
            settle(self, rows[1])
            c.wait_until("so it needs")
            show(rows[2], 0, 2, min(1.3, 0.9 * c.until("r3")))
            settle(self, rows[2])

            # {r3} "Drop is iterative.  It rebuilds just one cell, and shares the rest of the list.
            # That's big O of eye time, and constant space."
            c.wait_until("r3")
            show(rows[3], 0, 3, min(1.4, c.until("it rebuilds")), dim=[rows[1], rows[2]])
            c.wait_until("it rebuilds")
            show(rows[3], 3, 4, min(1.0, c.until("shares the rest")))
            c.wait_until("shares the rest")
            show(rows[3], 4, 5, min(1.0, 0.9 * c.until("that's big")))
            settle(self, rows[3])
            c.wait_until("that's big")
            show(rows[4], 0, 2, min(1.0, c.until("constant space")))
            c.wait_until("constant space")
            show(rows[4], 2, 4, min(1.0, 0.9 * c.until("r4")))
            settle(self, rows[4])

            # {r4} "And past the end of the list, both simply stop, with no exception."
            c.wait_until("r4")
            show(rows[5], 0, 2, min(1.4, c.until("with no exception")), dim=[rows[3], rows[4]])
            c.wait_until("with no exception")
            show(rows[5], 2, 3, min(1.0, 0.9 * c.until("next")))
            settle(self, rows[5])

            # {next} "Next time, a question programs ask all the time."  The chain waits under
            # the recap; then the recap gives way and the chain takes the centre.
            c.wait_until("next")
            run.shift(RUN_LOW * DOWN)
            self.play(FadeIn(run, shift=0.3 * UP), run_time=1.2)

            # "Is this element in the list?"  The recap gives way; the chain takes the centre,
            # the pointer drops over the 9 and the question comes in.
            c.wait_until("is this element")
            rt = min(1.9, max(1.0, c.remaining - 0.05))
            sweep_clear(self, span(run.animate.shift(RUN_LOW * UP), 0.1, 0.6, rt),
                        span(FadeIn(question, shift=0.3 * DOWN), 0.45, 0.85, rt),
                        span(FadeIn(pointer, shift=0.3 * DOWN), 0.55, 0.9, rt),
                        span(FadeIn(nxt, shift=0.2 * UP), 0.65, 1.0, rt),
                        keep=[run], run_time=rt)
