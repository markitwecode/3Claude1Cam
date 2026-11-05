"""Chapter 5, scene 2: char and string, two separate types. 'a' vs "a" (length 1), "abc",
then String.length and ^ (with @ for lists as a dim reminder).

Clips c5.str.1 – c5.str.3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

QUOTE = YELLOW            # quote marks, single and double
LX, RX = -3.55, 3.45      # column centres: char | string
HEAD_Y, LIT_Y, REP_Y, LEN_Y = 2.05, 0.55, -0.95, -2.1
LIT, REP = 104, 40        # literal and reply sizes in the two columns
STRIP = 0.76              # the columns shrink to this for String.length and ^
ROW_A, ROW_B, ROW_C = 0.05, -1.65, -2.85  # String.length / ^ / the @ reminder
X_IN, X_OUT = -6.1, 6.3   # inputs start at X_IN, replies end at X_OUT
IN, OUT = 44, 38          # input and reply sizes in the bottom rows


# ── helpers (local to this scene) ──────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph and then swapped for the whole Code
# (settle / swap), never wrapped in a Group: see LESSONS.md.
def chars(code, ch):
    """Every glyph of `code` that is the character `ch`."""
    return [g for k in range(code.src.count(ch)) for g in code.find(ch, nth=k)]


def quoted(code):
    """Colour every quote mark (single or double) of `code` in the quote colour."""
    for ch in "'\"":
        for g in chars(code, ch):
            g.set_color(QUOTE)
    return code


def grow(old, new, mapping):
    """Slide old's glyphs onto new's (mapping: old index -> new index); the rest of new
    fades in. Returns the animations; call swap(old, new) after the play."""
    anims = [old.text[i].animate.move_to(new.text[j]) for i, j in mapping.items()]
    anims += [FadeIn(new.text[j], shift=LEFT * 0.15) for j in range(len(new.text))
              if j not in mapping.values()]
    return anims


def on_baseline(mob, glyph, ref):
    """Shift `mob` up or down so its `glyph` sits on the same baseline as `ref` (pick glyphs
    without descenders)."""
    return mob.shift(UP * (ref.get_bottom()[1] - glyph.get_bottom()[1]))


class CharsAndStrings(NarratedScene):
    def construct(self):
        self.char_column()
        self.string_column()
        self.length_and_join()
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.06),
                  run_time=1.2)
        self.wait(0.1)  # a truly empty last frame

    def settle(self, whole, *parts):
        """Swap pieces animated on their own for the whole object they belong to."""
        self.remove(*parts)
        self.add(whole)

    def swap(self, old, new):
        """After grow(): the moved glyphs and the faded-in ones become the real new Code."""
        self.remove(*old.get_family(), *new.get_family())
        self.add(new)

    # str.1: char, written in single quotes
    def char_column(self):
        self.head_c = Mono("char", size=52, color=GREEN).move_to([LX, HEAD_Y, 0])
        self.head_s = Mono("string", size=52, color=GREEN).move_to([RX, HEAD_Y, 0])
        on_baseline(self.head_s, self.head_s[0], self.head_c[0])   # 's' and 'c' sit on the baseline
        self.divider = Line(UP * 2.5, DOWN * 2.6, color=DIM, stroke_width=2)

        lit = quoted(Code("'a'", size=LIT)).move_to([LX, LIT_Y, 0])
        rep = quoted(Code("- : char = 'a'", size=REP)).move_to([LX, REP_Y, 0])

        with self.say("c5.str.1") as c:
            # "two separate types for text"
            c.wait_until("two")
            self.play(FadeIn(VGroup(self.head_c, self.head_s), shift=0.3 * DOWN, lag_ratio=0.3),
                      Create(self.divider), run_time=1.5)

            # "The first is char": spotlight the left column
            c.wait_until("char")
            self.play(FlashUnder(self.head_c, color=GREEN), self.head_s.animate.set_opacity(0.3),
                      run_time=1.0)

            # "You write a character in single quotes": first the quotes ...
            c.wait_until("single quotes")
            quotes = VGroup(*chars(lit, "'"))
            self.play(FadeIn(quotes, shift=0.3 * DOWN), run_time=0.8)
            # ... "Put the letter A in single quotes": then the letter drops in
            c.wait_until("letter a")
            letter = lit.find("a")
            self.play(FadeIn(letter, shift=0.4 * DOWN), run_time=0.9)
            self.settle(lit, quotes, letter)

            # {reply} "OCaml tells you its type is char": the reply comes out of the input
            c.wait_until("reply")
            body, prefix = rep.find("'a'"), rep.find("- : char =")
            self.play(TransformFromCopy(VGroup(*lit.text), body), FadeIn(prefix, shift=0.3 * DOWN),
                      run_time=1.2)
            self.settle(rep, body, prefix)
            c.wait_until("is char", nth=1)
            self.play(FlashUnder(rep.find("char"), color=GREEN), run_time=1.0)
        self.lit_c, self.rep_c = lit, rep

    # str.2: string, written in double quotes; "a" is a string of length 1, "abc" of length 3
    def string_column(self):
        lit = quoted(Code('"a"', size=LIT)).move_to([RX, LIT_Y, 0])
        lit3 = quoted(Code('"abc"', size=LIT)).move_to([RX, LIT_Y, 0])
        rep = quoted(Code('- : string = "a"', size=REP)).move_to([RX, REP_Y, 0])
        rep3 = quoted(Code('- : string = "abc"', size=REP)).move_to([RX, REP_Y, 0])
        word = T("length", size=40)
        one = T("1", size=40, color=GOLD)
        VGroup(word, one).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to([RX, LEN_Y, 0])
        three = T("3", size=40, color=GOLD).move_to(one, aligned_edge=DL)

        with self.say("c5.str.2") as c:
            # "The second type is string."
            self.play(self.head_s.animate.set_opacity(1), FlashUnder(self.head_s, color=GREEN),
                      run_time=1.0)

            # "You write a string in double quotes."
            c.wait_until("double quotes")
            quotes = VGroup(*chars(lit, '"'))
            self.play(FadeIn(quotes, shift=0.3 * DOWN), run_time=0.8)

            # {same} "the letter A in double quotes": the same letter, carried across
            c.wait_until("letter a")
            letter = lit.find("a")
            self.play(TransformFromCopy(self.lit_c.find("a"), letter, path_arc=-PI / 4), run_time=1.5)
            self.settle(lit, quotes, letter)

            # "It's a string, of length one."
            c.wait_until("it's a string")
            body, prefix = rep.find('"a"'), rep.find("- : string =")
            self.play(TransformFromCopy(VGroup(*lit.text), body), FadeIn(prefix, shift=0.3 * DOWN),
                      run_time=1.2)
            self.settle(rep, body, prefix)
            c.wait_until("length one")
            self.play(FadeIn(VGroup(word, one), shift=0.3 * DOWN), run_time=0.8)

            # {abc} "A, B, C, in double quotes": the string grows, letter by letter
            c.wait_until("a b c")
            self.play(*grow(lit, lit3, {0: 0, 1: 1, 2: 4})[:3],
                      time_span(FadeIn(lit3.text[2], shift=LEFT * 0.15), 0.3, 0.9),
                      time_span(FadeIn(lit3.text[3], shift=LEFT * 0.15), 0.7, 1.3), run_time=1.5)
            self.swap(lit, lit3)
            c.wait_until("is a string")
            n = len(rep.text)
            self.play(*grow(rep, rep3, {**{i: i for i in range(n - 1)}, n - 1: n + 1}), run_time=0.9)
            self.swap(rep, rep3)
            c.wait_until("length three")
            self.play(Transform(one, three), FlashAround(one, color=GOLD, buff=0.1), run_time=0.8)
        self.lit_s, self.rep_s, self.length = lit3, rep3, VGroup(word, one)

    # str.3: String.length counts; ^ joins two strings (as @ joins two lists)
    def length_and_join(self):
        # the two columns, shrunk into a strip along the top (the headers have done their job)
        cols = VGroup(self.lit_c, self.rep_c, self.lit_s, self.rep_s, self.length)
        strip = cols.copy().scale(STRIP, about_point=[0, cols.get_y(), 0])
        strip.shift(UP * (3.45 - strip.get_top()[1]))
        div_end = Line([0, strip.get_top()[1], 0], [0, strip.get_bottom()[1], 0],
                       color=DIM, stroke_width=2)

        # row A: String.length "abc"   - : int = 3
        len_in = quoted(Code('String.length "abc"', size=IN)).move_to([X_IN, ROW_A, 0], aligned_edge=LEFT)
        len_in.find("String.length").set_color(YELLOW)
        len_out = Code("- : int = 3", size=OUT).move_to([X_OUT, ROW_A, 0], aligned_edge=RIGHT)
        on_baseline(len_out, len_out.find("i")[0], len_in.find("S")[0])
        abc = len_in.find("abc")
        brace3 = Brace(abc, DOWN, buff=0.1, color=GOLD)
        n3 = T("3", size=36, color=GOLD).next_to(brace3, DOWN, buff=0.1)

        # row B: "abc" ^ "def"   - : string = "abcdef"
        cat_in = quoted(Code('"abc" ^ "def"', size=IN)).move_to([X_IN, ROW_B, 0], aligned_edge=LEFT)
        cat_out = quoted(Code('- : string = "abcdef"', size=OUT)).move_to([X_OUT, ROW_B, 0],
                                                                          aligned_edge=RIGHT)
        on_baseline(cat_out, cat_out.find("a", nth=0)[0], cat_in.find("a")[0])
        caret = cat_in.find("^").set_color(YELLOW)
        letters6 = cat_out.find("abcdef")
        brace6 = Brace(letters6, DOWN, buff=0.1, color=GOLD)
        n6 = T("6", size=36, color=GOLD).next_to(brace6, DOWN, buff=0.1)

        # the reminder: @ does the same for lists (dim, its @ right under the ^)
        lists = Code("[1; 2] @ [3]", size=IN)
        for ch in "[];":
            for g in chars(lists, ch):
                g.set_color(TEAL)
        lists.shift(np.array([caret.get_x(), ROW_C, 0]) - lists.find("@").get_center())
        lists.set_opacity(0.45)
        at = lists.find("@")

        # a longer hold on the finished picture: the ^ / @ pair needs reading time (dwell)
        with self.say("c5.str.3", gap=1.9) as c:
            # "To find out how long a string is": the columns step up into a strip
            # (the headers go first, so the rising columns never pass through them)
            self.play(time_span(FadeOut(self.head_c, shift=0.2 * UP), 0, 0.5),
                      time_span(FadeOut(self.head_s, shift=0.2 * UP), 0, 0.5),
                      cols.animate.become(strip), Transform(self.divider, div_end), run_time=1.5)

            # "use String dot length"
            c.wait_until("use")
            fn = len_in.find("String.length")
            self.play(FadeIn(fn, shift=0.3 * DOWN), run_time=0.8)
            # "of A, B, C": the string comes down from the column above
            c.wait_until("of a b c")
            arg = len_in.find('"abc"')
            self.play(TransformFromCopy(VGroup(*self.lit_s.text), arg), run_time=1.0)
            self.settle(len_in, fn, arg)
            # "gives three": a brace counts the letters, and that count is the reply
            c.wait_until("gives three")
            prefix = len_out.find("- : int =")
            self.play(GrowFromCenter(brace3), FadeIn(n3, shift=0.2 * DOWN),
                      time_span(TransformFromCopy(n3, len_out.find("3")), 0.6, 1.5),
                      time_span(FadeIn(prefix, shift=0.2 * LEFT), 0.6, 1.5), run_time=1.5)
            self.settle(len_out, prefix, len_out.find("3"))

            # {caret} "To join two strings together": two strings ...
            c.wait_until("caret")
            parts = [cat_in.find('"abc"'), cat_in.find('"def"')]
            self.play(FadeIn(parts[0], shift=0.3 * DOWN), FadeIn(parts[1], shift=0.3 * DOWN),
                      run_time=1.0)
            # ... "use the caret symbol"
            c.wait_until("caret symbol")
            self.play(FadeIn(caret, scale=1.6), FlashAround(caret, color=YELLOW, buff=0.12), run_time=1.0)
            self.settle(cat_in, caret, *parts)

            # {join} "A, B, C, joined with D, E, F, gives a single string of six letters"
            c.wait_until("join")
            self.play(FlashUnder(cat_in.find("abc"), color=GOLD), run_time=0.8)
            c.wait_until("d e f")
            self.play(FlashUnder(cat_in.find("def"), color=GOLD), run_time=0.8)
            c.wait_until("gives a single")
            prefix = cat_out.find("- : string =")
            outer = VGroup(*chars(cat_out, '"'))
            self.play(TransformFromCopy(cat_in.find("abc"), cat_out.find("abc")),
                      TransformFromCopy(cat_in.find("def"), cat_out.find("def")),
                      time_span(FadeIn(prefix, shift=0.2 * LEFT), 0.5, 1.5),
                      time_span(FadeIn(outer), 0.9, 1.5), run_time=1.5)
            self.settle(cat_out, cat_out.find("abc"), cat_out.find("def"), prefix, outer)
            c.wait_until("six")
            self.play(GrowFromCenter(brace6), FadeIn(n6, shift=0.2 * DOWN), run_time=0.8)

            # {like} "the caret symbol does for strings what the at sign does for lists"
            c.wait_until("like")
            self.play(FadeIn(lists, shift=0.3 * UP), FlashAround(caret, color=YELLOW, buff=0.12),
                      run_time=1.0)
            c.wait_until("at sign")
            self.play(FlashAround(at, color=YELLOW, buff=0.12),
                      *[g.animate.set_color(YELLOW).set_opacity(1) for g in at], run_time=1.0)
