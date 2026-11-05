"""Chapter 3, scene 1: hook. A tiny phone book: names over numbers in matching order, paired
into one list and split back; the general picture, zip and unzip. Clips c3.hook.1 – c3.hook.2.

Layout shared with ch3_s5 (replays the pairing backwards): see the constants below.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

NAMES = ['"Amy"', '"Bob"', '"Cleo"']
NUMS = ["21", "35", "47"]

# the phone book (shared with ch3_s5)
LIST_SIZE = 44      # Code size of the two stacked lists
NAMES_Y = 0.9       # centre y of ["Amy"; "Bob"; "Cleo"]
NUMS_Y = -0.6       # centre y of [21; 35; 47] (numbers spread under the names' columns)
PAIRS_SIZE = 34     # Code size of the pairs list
PAIRS_Y = -2.65     # centre y of [("Amy", 21); ("Bob", 35); ("Cleo", 47)]
TEX_SIZE = 54       # the general picture


def maps_arrow(start, end, color=FG):
    """A long mapsto: an arrow from start to end with a short bar across its tail."""
    arrow = Arrow(start, end, buff=0, stroke_width=5, color=color,
                  max_tip_length_to_length_ratio=0.14)
    tick = Line(start + 0.17 * UP, start + 0.17 * DOWN, stroke_width=5, color=color)
    return arrow, tick


def dimmed_copy(mob, op):
    """A copy of `mob` at opacity `op` (fill of filled parts, stroke of outlines), to Transform to."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_opacity(op)
        else:
            leaf.set_stroke(opacity=op)
    return t


# the names fly down past the numbers row: Amy round its left end, Bob through the gap
# between 21 and 35, Cleo through the gap between 35 and 47
NAME_DETOUR = [-1.4, -0.95, -1.55]


def bump_path(offset):
    """Straight from start to end plus a sideways bump (full `offset` halfway)."""
    def path(start, end, alpha):
        return start + alpha * (end - start) + 4 * alpha * (1 - alpha) * offset
    return path


def without(glyphs, *groups):
    ids = {id(g) for grp in groups for g in grp}
    return [g for g in glyphs if id(g) not in ids]


class Ch3S1Hook(NarratedScene):
    def construct(self):
        # ── the phone book ───────────────────────────────────────────────
        names = Code('["Amy"; "Bob"; "Cleo"]', size=LIST_SIZE).move_to(UP * NAMES_Y)
        name_g = [names.find(n) for n in NAMES]
        for g in name_g:
            g.set_color(YELLOW)
        cols = [g.get_center()[0] for g in name_g]
        names_frame = without(names.line(0), *name_g)

        numbers = Code("[21; 35; 47]", size=LIST_SIZE).move_to(UP * NUMS_Y)
        num_g = [numbers.find(n) for n in NUMS]
        semis = [numbers.find(";", nth=i) for i in range(2)]
        for i, g in enumerate(num_g):
            dx = cols[i] - g.get_center()[0]
            g.shift(dx * RIGHT)
            if i < 2:
                semis[i].shift(dx * RIGHT)
        numbers.find("[").set_x(names.find("[").get_x())
        numbers.find("]").set_x(names.find("]").get_x())
        nums_frame = without(numbers.line(0), *num_g)

        top = names.line(0).get_bottom()[1] - 0.15
        bot = numbers.line(0).get_top()[1] + 0.15
        lines = [Line([x, top, 0], [x, bot, 0], stroke_width=2.5, color=DIM) for x in cols]

        pairs = Code('[("Amy", 21); ("Bob", 35); ("Cleo", 47)]', size=PAIRS_SIZE).move_to(UP * PAIRS_Y)
        p_name = [pairs.find(n) for n in NAMES]
        for g in p_name:
            g.set_color(YELLOW)
        p_num = [pairs.find(n) for n in NUMS]
        p_whole = [pairs.find(f"({n}, {m})") for n, m in zip(NAMES, NUMS)]
        p_bits = [without(p_whole[i], p_name[i], p_num[i]) for i in range(3)]
        p_frame = without(pairs.line(0), *p_whole)

        heading = T("a tiny phone book", 44).move_to(UP * 2.7)

        # back from the pairs to the two lists
        back = CurvedArrow(pairs.line(0).get_right() + LEFT * 0.45 + UP * 0.38,
                           np.array([names.line(0).get_right()[0] + 0.4, (NAMES_Y + NUMS_Y) / 2, 0]),
                           angle=PI / 2, color=GOLD, stroke_width=5)
        q = T("?", 60, GOLD).next_to(back, RIGHT, buff=0.18)


        # ── the general picture ──────────────────────────────────────────
        xs = MathTex("[", "x_1", ",", r"\ldots", ",", "x_n", "]", font_size=TEX_SIZE)
        ys = MathTex("[", "y_1", ",", r"\ldots", ",", "y_n", "]", font_size=TEX_SIZE)
        for i in (1, 5):
            xs[i].set_color(PINK)
            ys[i].set_color(PURPLE)
        left = VGroup(xs, ys).arrange(DOWN, buff=0.45)
        brace = Brace(left, RIGHT, buff=0.2)
        tip = brace.get_tip()
        r_start = tip + RIGHT * 0.35 + UP * 0.3
        r_end = r_start + RIGHT * 2.3
        zarrow, ztick = maps_arrow(r_start, r_end)
        rp = MathTex("[(", "x_1", ",", "y_1", "),", r"\ldots", ",(", "x_n", ",", "y_n", ")]",
                     font_size=TEX_SIZE)
        for i in (1, 7):
            rp[i].set_color(PINK)
        for i in (3, 9):
            rp[i].set_color(PURPLE)
        rp.next_to(r_end, RIGHT, buff=0.35).set_y(tip[1])
        uarrow, utick = maps_arrow(np.array([r_end[0], tip[1] - 0.3, 0]),
                                   np.array([r_start[0], tip[1] - 0.3, 0]), YELLOW)
        zip_lab = Mono("zip", 40, YELLOW).next_to(zarrow, UP, buff=0.2)
        unzip_lab = Mono("unzip", 40, YELLOW).next_to(uarrow, DOWN, buff=0.2)
        pic = VGroup(left, brace, zarrow, ztick, rp, uarrow, utick, zip_lab, unzip_lab)
        if pic.width > 11.8:
            pic.scale(11.8 / pic.width)
        pic.move_to(DOWN * 0.8)

        # ── c3.hook.1 ────────────────────────────────────────────────────
        with self.say("c3.hook.1") as c:
            card = title_card("Part 3 · Lists of pairs: zip and unzip")
            self.play(
                time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.7),
                time_span(GrowFromCenter(card.rule), 0, 0.7),
                time_span(FadeIn(card.course, shift=0.25 * DOWN), 0.1, 0.8),
                time_span(FadeIn(card.part, shift=0.25 * DOWN), 0.2, 0.9),
                run_time=0.9,
            )
            # the card holds through "Last time ..." and "... a tiny phone book"; on "names" it
            # clears, the heading drops in and the names list builds, each name on its word
            c.wait_until("names")
            starts = [max(0.7, c.until(w) - 0.15) for w in ("Amy", "Bob", "Cleo")]
            self.play(
                *[time_span(FadeOut(m), 0, 0.6) for m in (card.title, card.rule, card.course, card.part)],
                time_span(FadeIn(heading, shift=0.3 * DOWN), 0.3, 1.1),
                *[time_span(FadeIn(g), 0.4, 1.1) for g in names_frame],
                *[time_span(FadeIn(g, shift=0.25 * DOWN), s, s + 0.7)
                  for s, grp in zip(starts, name_g) for g in grp],
                run_time=starts[-1] + 0.7,
            )
            settle(self, names)

            # numbers: frame on "numbers", each number on its word, under its name
            c.wait_until("numbers")
            starts = [max(0.5, c.until(w) - 0.15) for w in ("twenty-one", "thirty-five", "forty-seven")]
            self.play(
                *[time_span(FadeIn(g), 0, 0.8) for g in nums_frame],
                *[time_span(FadeIn(g, shift=0.25 * DOWN), s, s + 0.7)
                  for s, grp in zip(starts, num_g) for g in grp],
                run_time=starts[-1] + 0.7,
            )
            settle(self, numbers)

            # matching order: each column's line grows from the name (on its word) down to its
            # number (reaching it as the number is said)
            pairs_said = [("Amy", "twenty-one"), ("Bob", "thirty-five"), ("Cleo", "forty-seven")]
            for i, (name, num) in enumerate(pairs_said):
                c.wait_until(name, nth=1)
                rt = min(1.2, max(0.6, c.until(num, nth=1) + 0.3))
                nxt = c.until(pairs_said[i + 1][0], nth=1) if i < 2 else c.remaining
                self.play(Create(lines[i]), run_time=min(rt, 0.9 * nxt))
            c.wait_until()

        # ── c3.hook.2 ────────────────────────────────────────────────────
        with self.say("c3.hook.2") as c:
            # each name and its number slide together into one pair
            rt = min(2.4, 0.8 * c.until("split"))
            u = rt / 3.0
            anims = [time_span(FadeIn(g), 0, 0.8 * u) for g in p_frame]
            for i in range(3):
                s = i * 0.7 * u
                e = s + 1.6 * u
                anims += [time_span(TransformFromCopy(a, b, path_func=bump_path(NAME_DETOUR[i] * RIGHT)), s, e)
                          for a, b in zip(name_g[i], p_name[i])]
                anims += [time_span(TransformFromCopy(a, b), s, e) for a, b in zip(num_g[i], p_num[i])]
                anims += [time_span(FadeIn(g), s + 0.5 * u, e) for g in p_bits[i]]
            self.play(*anims, run_time=rt)
            settle(self, pairs)

            # and back again?
            c.wait_until("split")
            k = min(0.8, 0.8 * c.until("general"))
            self.play(time_span(Create(back), 0, k), time_span(FadeIn(q, shift=0.2 * LEFT), 0, 0.4 * k),
                      run_time=k)
            c.wait_until("general")

            # in general: the two specific lists shrink and dim to the top; the pairs give way
            # to the general picture as it starts
            specific = VGroup(names, numbers, *lines)
            tgt = dimmed_copy(specific, 0.3).scale(0.65).move_to(UP * 2.75)
            k = min(1.3, 0.9 * c.until("list of exes"))
            self.play(FadeOut(heading), Transform(specific, tgt),
                      time_span(FadeOut(back), 0.3 * k, k), time_span(FadeOut(q), 0.3 * k, k),
                      run_time=k)
            c.wait_until("list of exes")
            self.play(FadeOut(pairs), FadeIn(xs, shift=0.25 * DOWN),
                      run_time=min(0.9, 0.8 * c.until("list of whys")))
            c.wait_until("list of whys")
            self.play(FadeIn(ys, shift=0.25 * DOWN), run_time=min(0.9, 0.8 * c.until("one list of pairs")))
            c.wait_until("one list of pairs")
            rt = min(2.4, 0.9 * c.until("zipname"))
            u = rt / 2.4
            moved = [(xs[1], rp[1]), (ys[1], rp[3]), (xs[5], rp[7]), (ys[5], rp[9])]
            self.play(
                time_span(GrowFromCenter(brace), 0, 0.7 * u),
                time_span(GrowArrow(zarrow), 0.3 * u, 1.0 * u),
                time_span(FadeIn(ztick), 0.3 * u, 0.8 * u),
                *[time_span(TransformFromCopy(a, b), 0.8 * u, 2.4 * u) for a, b in moved],
                *[time_span(FadeIn(rp[i]), 1.2 * u, 2.2 * u) for i in (0, 2, 4, 5, 6, 8, 10)],
                run_time=rt,
            )
            settle(self, rp)

            c.wait_until("zipname")
            self.play(zarrow.animate.set_color(YELLOW), ztick.animate.set_color(YELLOW),
                      FadeIn(zip_lab, shift=0.3 * DOWN),
                      run_time=min(1.0, 0.8 * c.until("unzipname")))
            c.wait_until("unzipname")
            self.play(GrowArrow(uarrow), FadeIn(utick), FadeIn(unzip_lab, shift=0.3 * UP),
                      run_time=min(1.0, max(0.6, 0.9 * c.remaining)))
            c.wait_until()

        # the answer alone, centred, held
        self.play(FadeOut(specific), pic.animate.move_to(ORIGIN), run_time=1.2)
        self.wait(2.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
