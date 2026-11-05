"""Chapter 5, scene 4: escape sequences. \\" for a double quote, \\\\ for a backslash, \\n for
a newline (two symbols, one character), and printing "I\\nLIKE\\nCHEESE\\n".

Clips c5.esc.1 – c5.esc.4. Every string and reply on screen was checked with `ocaml` (5.4.1).
NB: the lecture notes print the double-quote escape as "\\\\"; that is the backslash. The double
quote is "\\"" (String.length "\\"" = 1).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

ESC = YELLOW        # escape sequences (backslash and the character after it)
PUZZLE = 60         # the "She said" line
ROW = 52            # the escape table
TERM = 48           # text inside the output window
SCREEN = "#151920"  # the output window's face (as ch5_s1_hook's terminal)
DIMMED = 0.4


# ── helpers (local to this scene) ──────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph, then swapped for the whole object; never
# wrapped in a VGroup/AnimationGroup (LESSONS.md).
def paint_escapes(code):
    """Colour every escape sequence (\\" \\\\ \\n) of a Code, both of its symbols."""
    i, src = 0, code.src
    while i < len(src):
        if src[i] == "\\":
            code._span(i, i + 2).set_color(ESC)
            i += 2
        else:
            i += 1
    return code


def escapes(code):
    """The glyphs of each escape sequence in `code`, one list per sequence."""
    out, i, src = [], 0, code.src
    while i < len(src):
        if src[i] == "\\":
            out.append(list(code._span(i, i + 2)))
            i += 2
        else:
            i += 1
    return out


def underline(glyphs, color, buff=0.14, width=5):
    g = VGroup(*glyphs)
    return Line(g.get_corner(DL), g.get_corner(DR), color=color, stroke_width=width).shift(DOWN * buff)


def esc_box(glyphs, line, color=ESC):
    """P8 highlight box around one escape sequence: faint fill behind the text."""
    g = VGroup(*glyphs)
    r = Rectangle(width=g.width + 0.08, height=line.height + 0.2)
    r.move_to([g.get_x(), line.get_y(), 0]).set_stroke(color, 2).set_fill(color, 0.18)
    return r.set_z_index(-1)


def terminal(width=6.4, height=4.4):
    """A plain terminal window (the look of ch5_s1_hook's): rounded frame, title bar, dots."""
    frame = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                             stroke_color=DIM, stroke_width=3).set_fill(SCREEN, 1)
    bar_y = frame.get_top()[1] - 0.45
    bar = Line([frame.get_left()[0], bar_y, 0], [frame.get_right()[0], bar_y, 0],
               stroke_color=DIM, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.07, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.15)
    dots.move_to([frame.get_left()[0] + 0.55, (frame.get_top()[1] + bar_y) / 2, 0])
    return VGroup(frame, bar, dots)


def return_arrow(start, end, gap_y, color=ESC):
    """The jump a newline makes: from just after the end of one line, down into the gap
    between the lines (gap_y), back to the left margin, and into the start of the next."""
    start, end = np.array(start, dtype=float), np.array(end, dtype=float)
    left = end[0] - 0.3
    path = VMobject().set_points_as_corners([start, [start[0], gap_y, 0], [left, gap_y, 0],
                                             [left, end[1], 0]]).set_stroke(color, 4)
    tip = Arrow([left, end[1], 0], end, buff=0, stroke_width=4, color=color, tip_length=0.16,
                max_tip_length_to_length_ratio=1.0, max_stroke_width_to_length_ratio=20)
    return VGroup(path, tip)


def boxes_for(code):
    """A P8 box behind every escape sequence of `code`."""
    return VGroup(*[esc_box(e, code) for e in escapes(code)])


class EscapeSequences(NarratedScene):
    def construct(self):
        puzzle = self.the_puzzle()
        table = self.the_fix(puzzle)
        length = self.newline(puzzle, table)
        self.cheese(length)
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.05), run_time=1.0)
        self.wait(0.1)  # a truly empty last frame

    def settle(self, whole, *parts):
        """Swap pieces animated on their own for the whole object they belong to."""
        self.remove(*parts)
        self.add(whole)

    # esc.1: how do you put a double quote inside a string?
    def the_puzzle(self):
        want = Mono('She said "hi"', size=52).move_to(UP * 0.9)
        inner = [want[7], want[10]]                       # the two quote marks
        want_lab = T("we want:", size=38, color=DIM).next_to(want, LEFT, buff=0.45)
        want_lab.align_to(want[0], DOWN)
        q = T("?", size=110, color=GOLD).move_to(DOWN * 0.7)
        naive = Code('"She said "hi""', size=PUZZLE).move_to(DOWN * 0.7)
        nt = naive.text                                   # 13 glyphs: " S h e s a i d " h i " "
        ends_here = underline(nt[0:9], RED)

        with self.say("c5.esc.1") as c:
            # "Here's a puzzle." (P23: the question is an object on screen)
            self.play(FadeIn(q, scale=0.5, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("suppose")
            self.play(FadeIn(want, shift=0.3 * DOWN), FadeIn(want_lab, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("double quote")
            self.play(*[FlashAround(g, color=ESC, buff=0.08) for g in inner],
                      *[g.animate.set_color(ESC) for g in inner], run_time=1.0)
            c.wait_until("how would you")
            self.play(FlashAround(q, color=GOLD, time_width=1.5, buff=0.15), run_time=1.2)

            # "If you just type the quote": the text drops into the code line, and the "?"
            # becomes the string's two outer quotes
            c.wait_until("problem")
            self.play(TransformFromCopy(want, VGroup(*nt[1:12])),
                      FadeTransform(q, VGroup(nt[0], nt[12])), run_time=1.5)
            self.settle(naive, *nt)

            # "OCaml thinks the string ends right there."
            c.wait_until("ocaml thinks")
            self.play(Create(ends_here), run_time=1.0)
            c.wait_until("right there")
            self.play(FlashAround(nt[8], color=RED, buff=0.08), nt[8].animate.set_color(RED),
                      *[g.animate.set_opacity(DIMMED) for g in nt[9:13]], run_time=0.8)
        return want, want_lab, naive, ends_here

    # esc.2: backslash-quote, backslash-backslash
    def the_fix(self, puzzle):
        want, want_lab, naive, ends_here = puzzle
        UP_BY = 1.55                                      # the puzzle makes room for the table
        fixed = paint_escapes(Code('"She said \\"hi\\""', size=PUZZLE))
        fixed.move_to(naive).shift(UP * UP_BY)
        ft = fixed.text                                   # 15 glyphs, \ at 8 and 12
        whole = underline(ft, GREEN)
        e1, e2 = escapes(fixed)
        boxes = [esc_box(e, fixed) for e in (e1, e2)]

        head = T("escape sequences", size=46, color=ESC)
        rows = [paint_escapes(Code(s, size=ROW)) for s in ('"\\""', '"\\\\"')]
        labels = [T(s, size=42) for s in ("a double quote", "a backslash")]
        X0, LX = -3.6, -1.0                               # code column, label column
        head.move_to([X0, -0.75, 0], aligned_edge=LEFT)
        for i, (r, lab) in enumerate(zip(rows, labels)):
            y = -1.7 - 0.95 * i
            r.move_to([X0, y, 0], aligned_edge=LEFT)
            lab.move_to([LX, y, 0], aligned_edge=LEFT)
        row_boxes = [boxes_for(r) for r in rows]

        nt = naive.text
        moves = list(zip(range(8), range(8))) + [(8, 9), (9, 10), (10, 11), (11, 13), (12, 14)]

        with self.say("c5.esc.2") as c:
            # "The fix is called an escape sequence": the puzzle moves up for the table
            c.wait_until("escape sequence")
            self.play(VGroup(want, want_lab, naive, ends_here).animate.shift(UP * UP_BY),
                      time_span(FadeIn(head, shift=0.3 * DOWN), 0.5, 1.4), run_time=1.4)

            # "and it starts with a backslash": a backslash drops in before each inner quote
            c.wait_until("backslash")
            self.play(*[ReplacementTransform(nt[i], ft[j]) for i, j in moves],
                      FadeIn(ft[8], shift=0.4 * DOWN), FadeIn(ft[12], shift=0.4 * DOWN),
                      FadeOut(ends_here), run_time=1.5)
            self.settle(fixed, *ft)

            # "a backslash means the next character is special": each pair is one unit
            c.wait_until("the next character")
            self.play(*[FadeIn(b) for b in boxes], *[FlashAround(VGroup(*e), color=ESC, buff=0.1)
                                                    for e in (e1, e2)], run_time=1.0)

            # "So backslash, double quote, stands for a double quote"
            c.wait_until("so backslash")
            r1 = rows[0].text
            self.play(TransformFromCopy(VGroup(*e1), VGroup(r1[1], r1[2])),
                      FadeIn(VGroup(r1[0], r1[3]), scale=0.8), FadeIn(row_boxes[0]), run_time=1.2)
            self.settle(rows[0], *r1)
            c.wait_until("stands for")
            self.play(FadeIn(labels[0], shift=0.3 * LEFT), run_time=1.0)
            # "that doesn't end the string": now the string runs to the very end
            c.wait_until("doesn't end")
            self.play(Create(whole), run_time=1.0)

            # "to get a backslash itself, you type two backslashes in a row"
            c.wait_until("backslash itself")
            self.play(FadeIn(labels[1], shift=0.3 * LEFT), run_time=1.0)
            c.wait_until("two backslashes")
            r2 = rows[1].text
            self.play(TransformFromCopy(r1[1], r2[1]), TransformFromCopy(r1[1], r2[2]),
                      FadeIn(VGroup(r2[0], r2[3]), scale=0.8), FadeIn(row_boxes[1]), run_time=1.2)
            self.settle(rows[1], *r2)

        self.puzzle_all = [want, want_lab, fixed, whole, *boxes]
        return head, rows, labels, row_boxes

    # esc.3: \n is a newline: two symbols, one character
    def newline(self, puzzle, table):
        head, rows, labels, row_boxes = table
        UP_BY = 3.65                                      # the table takes the top
        row3 = paint_escapes(Code('"\\n"', size=ROW))
        lab3 = T("a newline", size=42)
        y3 = rows[1].get_y() - 0.95 + UP_BY
        row3.move_to([rows[0].get_left()[0], y3, 0], aligned_edge=LEFT)
        lab3.move_to([labels[0].get_left()[0], y3, 0], aligned_edge=LEFT)
        box3 = boxes_for(row3)

        # a tiny picture of the jump: end of one line -> start of the next
        bars = VGroup(Rectangle(width=1.9, height=0.14), Rectangle(width=1.3, height=0.14))
        bars.set_stroke(width=0).set_fill(DIM, 0.8).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        bars.move_to([lab3.get_right()[0] + 1.5, y3, 0], aligned_edge=LEFT)
        jump = return_arrow(bars[0].get_right() + RIGHT * 0.12, bars[1].get_left() + LEFT * 0.08,
                            bars.get_y())

        nl = escapes(row3)[0]
        brace = Brace(VGroup(*nl), DOWN, buff=0.12, color=GOLD)
        two = T("2 symbols", size=36, t2c={"2": GOLD}).next_to(brace, DOWN, buff=0.12)

        length = Code('String.length "\\n"', size=52).move_to(DOWN * 1.95)
        paint_escapes(length)
        len_box = boxes_for(length)
        length.find("String.length").set_color(YELLOW)
        reply = Code("- : int = 1", size=52)
        reply.next_to(length, DOWN, buff=0.5).align_to(length, LEFT)
        one = reply.find("1")[0]

        with self.say("c5.esc.3") as c:
            # the puzzle has been solved and read; the table moves up for the newline
            self.play(LaggedStart(*[FadeOut(m) for m in self.puzzle_all], lag_ratio=0.1),
                      VGroup(head, *rows, *labels, *row_boxes).animate.shift(UP * UP_BY), run_time=1.5)

            c.wait_until("backslash en")
            self.play(FadeIn(row3, shift=0.3 * DOWN), FadeIn(box3, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("for a newline")
            self.play(FadeIn(lab3, shift=0.3 * LEFT), run_time=1.0)
            c.wait_until("a jump")
            self.play(FadeIn(bars), time_span(Create(jump), 0.3, 1.4), run_time=1.4)

            # "two symbols when you type it"
            c.wait_until("two symbols")
            self.play(GrowFromCenter(brace), FadeIn(two, shift=0.3 * DOWN), run_time=1.0)

            # "but String dot length says it's just a single character"
            c.wait_until("string dot length")
            self.play(FadeIn(length, shift=0.3 * DOWN), FadeIn(len_box, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("says")
            rest = [g for g in reply.text if g is not one]
            self.play(ReplacementTransform(VGroup(*length.find('"\\n"')).copy(), one),
                      *[FadeIn(g, shift=0.3 * DOWN) for g in rest], run_time=1.2)
            self.settle(reply, one, *rest)
            c.wait_until("single character")
            self.play(FlashAround(reply.find("1")[0], color=GOLD, buff=0.1), run_time=1.0)
        return VGroup(length, len_box, reply)

    # esc.4: printing "I\nLIKE\nCHEESE\n" gives three lines
    def cheese(self, length):
        src = '"I\\nLIKE\\nCHEESE\\n"'
        s = paint_escapes(Code(src, size=44)).move_to(UP * 2.6)
        s_boxes = boxes_for(s)
        call = paint_escapes(Code("print_string " + src, size=44)).move_to(UP * 2.6)
        call.find("print_string").set_color(YELLOW)
        lit = call.find(src)
        fn = call.find("print_string")
        nls = escapes(s)

        win = terminal().move_to(DOWN * 1.05)
        x0 = win[0].get_left()[0] + 0.85
        top = win[1].get_y()
        ys = [top - 0.7 - 0.92 * i for i in range(4)]
        words = ["I", "LIKE", "CHEESE"]
        out = [Mono(w, size=TERM).move_to([x0, ys[i], 0], aligned_edge=LEFT) for i, w in enumerate(words)]
        cursor = Rectangle(width=0.26, height=0.5, stroke_width=0).set_fill(FG, 0.8)
        cursor.move_to([x0 + 0.13, ys[3], 0])
        jumps = [return_arrow([o.get_right()[0] + 0.15, ys[i], 0], [x0 - 0.06, ys[i + 1], 0],
                              (ys[i] + ys[i + 1]) / 2) for i, o in enumerate(out)]

        with self.say("c5.esc.4", gap=0.9) as c:  # a little extra hold on the printed lines
            # "So look at this string." The table clears; the length result steps back
            keep = {id(m) for m in length.get_family()}
            old = [m for m in self.mobjects if id(m) not in keep]
            code, box, reply = length
            self.play(LaggedStart(*[FadeOut(m) for m in old], lag_ratio=0.08),
                      code.animate.set_opacity(DIMMED), reply.animate.set_opacity(DIMMED),
                      box.animate.set_fill(opacity=0.07).set_stroke(opacity=DIMMED),
                      time_span(FadeIn(s, shift=0.3 * DOWN), 0.6, 1.5),
                      time_span(FadeIn(s_boxes, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)

            # "I, backslash en, like, backslash en, cheese, backslash en."
            for k in range(3):
                c.wait_until("backslash", nth=k)
                self.play(FlashAround(VGroup(*nls[k]), color=ESC, buff=0.08), run_time=0.9)

            # "When you print it": print_string goes in front, an output window opens
            c.wait_until("print")
            st = s.text
            lt = [g for g in lit]
            self.play(FadeOut(length),
                      *[ReplacementTransform(a, b) for a, b in zip(st, lt)],
                      s_boxes.animate.shift(lt[0].get_center() - st[0].get_center()),
                      FadeIn(VGroup(*fn), shift=0.3 * RIGHT),
                      time_span(FadeIn(win, scale=0.96), 0.4, 1.0), run_time=1.0)
            self.settle(call, *lt, *fn)

            # "it comes out as three separate lines": each word, then its \n jumps down.
            # The first line slowly, the rest quicker (P24)
            cnls = escapes(call)
            for i, (w, o) in enumerate(zip(words, out)):
                rt = (0.7, 0.6) if i == 0 else (0.5, 0.5)
                self.play(TransformFromCopy(VGroup(*call.find(w)), o), run_time=rt[0])
                extra = [FadeIn(cursor)] if i == 2 else []
                self.play(FlashAround(VGroup(*cnls[i]), color=ESC, buff=0.08), Create(jumps[i]),
                          *extra, run_time=rt[1])

            # "I. Like. Cheese."
            c.wait_until("lines")
            self.play(LaggedStart(*[FlashUnder(o, color=ESC) for o in out], lag_ratio=0.3), run_time=1.6)
