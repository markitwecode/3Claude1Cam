"""Chapter 5, scene 1: title card, where strings show up, then the hook question:
is a string secretly a list of characters? The question stays open (ch5_s3 answers it).

Clips c5.hook.1 – c5.hook.3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

QUOTE = YELLOW     # string quote marks (same as ch5_s2)
TERM = 48          # text size inside the terminal window
SCREEN = "#151920"  # the terminal's face, a shade lighter than the background
BOX = 1.5          # side of a letter box in the "cat" picture
CAT_Y, Q_Y, GHOST_Y = 1.75, -0.05, -1.85


# ── helpers (local to this scene) ──────────────────────────────────────────────
# Parts of a Text/Code are animated glyph by glyph and then swapped for the whole object
# (settle), never wrapped in a Group: see LESSONS.md.
def chars(code, ch):
    """Every glyph of `code` that is the character `ch`."""
    return [g for k in range(code.src.count(ch)) for g in code.find(ch, nth=k)]


def mini_card(label):
    frame = RoundedRectangle(corner_radius=0.08, width=1.15, height=0.8,
                             stroke_color=DIM, stroke_width=2.5)
    return VGroup(frame, T(label, size=30, color=DIM).move_to(frame))


def terminal(width=8.0, height=4.4):
    """A plain terminal window: rounded frame, a title bar with three dots."""
    frame = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                             stroke_color=DIM, stroke_width=3).set_fill(SCREEN, 1)
    bar_y = frame.get_top()[1] - 0.45
    bar = Line([frame.get_left()[0], bar_y, 0], [frame.get_right()[0], bar_y, 0],
               stroke_color=DIM, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.07, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.15)
    dots.move_to([frame.get_left()[0] + 0.55, (frame.get_top()[1] + bar_y) / 2, 0])
    return VGroup(frame, bar, dots)


def letter_box(ch):
    sq = Square(BOX, stroke_color=BLUE, stroke_width=3)
    return VGroup(sq, Mono(ch, size=80, color=GOLD).move_to(sq))


def ghost_cell(ch, at):
    """A cons cell drawn dashed and dim, its value box centred at `at`: the list a string
    might secretly be. cell.center / cell.tail are its value-box centre and pointer dot."""
    sq = Square(CELL).move_to(at).set_stroke(DIM, 3)
    tr, br = sq.get_corner(UR), sq.get_corner(DR)
    ptr_path = VMobject().set_points_as_corners([tr, tr + RIGHT * PTR_W, br + RIGHT * PTR_W, br])
    ptr_path.set_stroke(DIM, 3)
    box = DashedVMobject(sq, num_dashes=16, dashed_ratio=0.55)
    ptr = DashedVMobject(ptr_path, num_dashes=9, dashed_ratio=0.55)
    dot = Dot(at + RIGHT * (CELL + PTR_W) / 2, radius=0.07, color=DIM)
    label = Mono(ch, size=44, color=DIM).move_to(at)
    cell = VGroup(box, ptr, dot, label)
    cell.left, cell.tail, cell.label = sq.get_left(), dot.get_center(), label
    return cell


def ghost_chain(letters, center):
    step = CELL + PTR_W + LINK
    width = len(letters) * step + 0.6               # cells and links, then nil
    x0 = center[0] - width / 2 + CELL / 2
    cells = [ghost_cell(ch, np.array([x0 + i * step, center[1], 0])) for i, ch in enumerate(letters)]
    nil = Text("[]", font=MONO, font_size=42, color=DIM)
    nil.move_to([x0 + len(letters) * step - CELL / 2 + nil.width / 2, center[1], 0])
    targets = [c.left for c in cells[1:]] + [nil.get_left() + LEFT * 0.05]
    arrows = [Arrow(c.tail, t, buff=0, stroke_width=3, color=DIM,
                    max_tip_length_to_length_ratio=0.3, tip_length=0.16)
              for c, t in zip(cells, targets)]
    chain = VGroup(*cells, *arrows, nil)
    chain.cells, chain.arrows, chain.nil = cells, arrows, nil
    return chain


class Hook(NarratedScene):
    def construct(self):
        card, minis = self.title()
        window, bottom = self.where_strings(card, minis)
        self.the_question(window, bottom)
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.08),
                  run_time=1.2)
        self.wait(0.1)  # a truly empty last frame

    def settle(self, whole, *parts):
        """Swap pieces animated on their own for the whole object they belong to."""
        self.remove(*parts)
        self.add(whole)

    # hook.1: the title card; five exercise cards wait underneath
    def title(self):
        card = title_card("Part 5 · Strings, characters, and exercises")
        minis = VGroup(*[mini_card(f"3.{i}") for i in range(1, 6)]).arrange(RIGHT, buff=0.35)
        minis.move_to(DOWN * 2.75)

        with self.say("c5.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
            c.wait_until("lecture")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("we'll finish")
            self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("five")
            self.play(FadeIn(minis, shift=0.3 * UP, lag_ratio=0.2), run_time=1.3)
        return card, minis

    # hook.2: why strings: a program talking to a person; a number has to become text
    def where_strings(self, card, minis):
        word = select(card.part, "Strings")[0]

        win = terminal().move_to(UP * 0.1)
        x0 = win[0].get_left()[0] + 0.6
        top = win[1].get_y()
        ys = [top - 0.85 - 0.95 * i for i in range(4)]

        def line(s, i, color=FG):
            t = Mono(s, size=TERM, color=color)
            return t.move_to([x0, ys[i], 0], aligned_edge=LEFT)

        prompt = line("Name?", 0)
        ada = Mono("Ada", size=TERM, color=BLUE)
        ada.next_to(prompt, RIGHT, buff=0.38).align_to(prompt, DOWN)
        hello = line("Hello, Ada!", 1)
        hello[6:9].set_color(BLUE)        # the name the user typed, echoed back
        total = line("Total: 42", 2)
        total[6:8].set_color(GOLD)
        # a block cursor, sitting just after the last thing printed or typed
        cursor = Rectangle(width=0.26, height=0.5, stroke_width=0).set_fill(FG, 0.8)

        def cursor_after(mob=None, i=None):
            if mob is not None:
                return cursor.copy().next_to(mob, RIGHT, buff=0.12)
            return cursor.copy().move_to([x0 + 0.13, ys[i], 0])

        # where the window goes when the number needs the space, and the number itself
        num = Code("string_of_int 42", size=52).move_to(DOWN * 0.75)
        num.find("string_of_int").set_color(YELLOW)
        reply = Code('- : string = "42"', size=46).move_to(DOWN * 2.15)
        for g in chars(reply, '"'):
            g.set_color(QUOTE)

        with self.say("c5.hook.2") as c:
            # "why do we need strings at all?": the word lights up, the exercises step back
            c.wait_until("strings")
            self.play(FlashUnder(word, color=YELLOW), *[g.animate.set_color(YELLOW) for g in word],
                      *[m[0].animate.set_stroke(opacity=0.35) for m in minis],
                      *[m[1].animate.set_opacity(0.35) for m in minis], run_time=1.0)

            # "Strings are how programs handle text": the card clears for a screen
            c.wait_until("programs")
            self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.1),
                      time_span(FadeIn(win, scale=0.96), 0.5, 1.5), run_time=1.5)

            # "how a program talks to the people using it": it asks, the person types
            c.wait_until("talks")
            cur = cursor_after(prompt)
            self.play(FadeIn(prompt), FadeIn(cur), run_time=0.6)
            c.wait_until("people")
            end = cursor_after(ada)
            self.play(AddTextLetterByLetter(ada, run_time=0.6),
                      cur.animate(rate_func=linear).move_to(end), run_time=0.6)

            # "Every prompt, every message, every answer on the screen."
            c.wait_until("every prompt")
            self.play(FlashAround(prompt, color=YELLOW, buff=0.1), run_time=0.9)
            c.wait_until("every message")
            cur.move_to(cursor_after(i=2))     # a printed line: the cursor jumps to the next one
            self.play(FadeIn(hello, shift=0.2 * UP), run_time=0.7)
            c.wait_until("every answer")
            cur.move_to(cursor_after(i=3))
            self.play(FadeIn(total, shift=0.2 * UP), run_time=0.7)

            # {numbers}: the screen moves up; the program's result is a number ...
            window = VGroup(win, prompt, ada, hello, total, cur)
            c.wait_until("numbers")
            self.play(window.animate.scale(0.62).to_edge(UP, buff=0.45), run_time=1.5)
            c.wait_until("crunches")
            n42 = num.find("42")
            dx = num.get_x() - n42.get_x()
            n42.shift(RIGHT * dx)              # alone, the number sits in the middle
            self.play(FadeIn(n42, shift=0.3 * DOWN), run_time=1.0)
            # ... which has to be turned into a string
            c.wait_until("turn")
            fn = num.find("string_of_int")
            self.play(time_span(n42.animate.shift(LEFT * dx), 0, 0.55),
                      time_span(FadeIn(fn, shift=0.3 * RIGHT), 0.45, 1.0), run_time=1.0)
            self.settle(num, n42, fn)
            c.wait_until("into strings")
            digits = reply.find("42")
            prefix = reply.find("- : string =")
            quotes = VGroup(*chars(reply, '"'))
            self.play(TransformFromCopy(num.find("42"), digits), FadeIn(prefix, shift=0.3 * DOWN),
                      time_span(FadeIn(quotes, scale=1.4), 0.8, 1.3), run_time=1.3)
            self.settle(reply, digits, prefix, quotes)

            # "just so you can read them": the string is what the screen shows
            c.wait_until("just so")
            self.play(FlashAround(reply.find('"42"'), color=GOLD, buff=0.08),
                      FlashAround(total[6:8], color=GOLD, buff=0.08), run_time=min(1.0, c.until()))
        return window, VGroup(num, reply)

    # hook.3: a string looks like a list ... is it one? (left open)
    def the_question(self, window, bottom):
        cat = Code('"cat"', size=110).move_to(UP * CAT_Y)
        for g in chars(cat, '"'):
            g.set_color(QUOTE)
        boxes = VGroup(*[letter_box(ch) for ch in "cat"]).arrange(RIGHT, buff=0).move_to(UP * CAT_Y)
        q_left = Mono('"', size=110, color=QUOTE).next_to(boxes, LEFT, buff=0.3)
        q_right = Mono('"', size=110, color=QUOTE).next_to(boxes, RIGHT, buff=0.3)
        for q in (q_left, q_right):
            q.align_to(boxes, UP).shift(DOWN * 0.1)
        q = T("?", size=110, color=GOLD).move_to(UP * Q_Y)
        ghost = ghost_chain("cat", UP * GHOST_Y)

        with self.say("c5.hook.3") as c:
            # "a string looks a lot like a list": the screen gives way to a string
            self.play(FadeOut(window, shift=0.3 * UP),
                      time_span(FadeIn(cat, shift=0.3 * DOWN), 0.5, 1.5), run_time=1.5)

            # {letters} "a sequence of characters, in order": the letters get a box each
            c.wait_until("letters")
            glyphs = cat.text
            self.play(*[ReplacementTransform(glyphs[i + 1], boxes[i][1]) for i in range(3)],
                      ReplacementTransform(glyphs[0], q_left), ReplacementTransform(glyphs[4], q_right),
                      time_span(LaggedStart(*[Create(b[0]) for b in boxes], lag_ratio=0.3), 0.4, 1.5),
                      run_time=1.5)
            self.remove(*cat.get_family())
            string = VGroup(q_left, boxes, q_right)
            self.settle(string, *[b[0] for b in boxes], *[b[1] for b in boxes], q_left, q_right)

            # the number example has been read; it clears for the question
            c.wait_until("in order")
            self.play(FadeOut(bottom, shift=0.3 * DOWN), run_time=1.0)

            # "So here's a question." (P23: the question is an object on screen)
            c.wait_until("question")
            self.play(FadeIn(q, scale=0.5, shift=0.25 * DOWN), run_time=1.0)

            # "secretly just a list of characters?": the letters drop into a ghost chain
            c.wait_until("just a list")
            frames = VGroup(*[VGroup(cell[0], cell[1], cell[2]) for cell in ghost.cells])
            labels = [cell.label for cell in ghost.cells]
            # (the copies swing outwards, so the middle one doesn't pass through the "?")
            arcs = (PI / 3, -PI / 2, -PI / 3)
            self.play(*[TransformFromCopy(boxes[i][1], labels[i], path_arc=arcs[i]) for i in range(3)],
                      time_span(Create(frames, lag_ratio=0.2), 0.3, 1.5),
                      time_span(FadeIn(VGroup(*ghost.arrows, ghost.nil), lag_ratio=0.2), 1.0, 1.8),
                      run_time=1.8)
            self.settle(ghost, frames, *labels, VGroup(*ghost.arrows, ghost.nil))

            # "Hold that thought." The question stays open.
            c.wait_until("hold")
            self.play(FlashAround(q, color=GOLD, time_width=1.5, buff=0.15), run_time=1.5)
