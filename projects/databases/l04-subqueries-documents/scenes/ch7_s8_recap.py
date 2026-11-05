"""Chapter 7, scene 8: the chapter recap, then the end card (ch8's opening card). Clips c7.recap.1 – c7.recap.3.

Six callbacks in a 3 x 2 grid (r1 s2's thumb, r2 a trimmed rebuild of s3's lit walk, r3 s4's dict_grid + GOLD 321,
r4 s5's thumb, r5/r6 lighter rebuilds of s6's / s7's thumbs, text >= 18 in the cells), each with its short line, earlier ones dimmed to 0.4.
{next}: the grid clears to ch8 s1's open_card(lifted=False); {rows}: the chips lift half way, landing on
exactly open_card(lifted=True), held ~8 s as the end card. Reversed join (ch8 s1 opens on it): no fade,
no handover mark; the "pieces left" end flag is by design.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch7_s2_arrows")
S3 = load_scene("ch7_s3_paths")
S4 = load_scene("ch7_s4_cast")
S5 = load_scene("ch7_s5_parens")
S6 = load_scene("ch7_s6_arrays")
S7 = load_scene("ch7_s7_missing")
N8 = load_scene("ch8_s1_hook")

THUMB_W, THUMB_H = 4.3, 2.2
COL_X = [-4.6, 0.0, 4.6]
ROW_TOP = [2.82, -0.33]
LABELS = [
    "-> keeps JSON,\n->> gives a string",
    "$  ·  .key  ·  [0]  ·  [*]",
    "cast before\ncomparing numbers",
    "parentheses around\nevery arrow",
    "list_contains  ·\nlist_has_all",
    "json_exists  ·\nmissing key = NULL",
]
DIM_TO = 0.4


LIT_FILL = interpolate_color(ManimColor(BG), ManimColor(TEAL), 0.28)
KS = 22          # r2's text size before scaling (lands ~19 in its cell)


def _node(txt):
    t = Mono(txt, KS + 2, TEAL)
    box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=0.46)
    box.set_fill(LIT_FILL, 1).set_stroke(TEAL, 4)
    t.move_to(box)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def _edge(*pts):
    return VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in pts]).set_stroke(TEAL, 4)


def r2_thumb():
    """s3's walk, trimmed to what the line names: $ -> actors -> [0] -> name "Charles Chaplin" lit TEAL,
    and the [*] fork across the three genres (same lit style as s3's walk_tree)."""
    g_y, a_y, l_y = 0.75, -0.1, -0.95
    root = _node("$").move_to([0.3, (g_y + a_y) / 2, 0])
    rx = root.get_right()[0]
    star = _node("[*]").move_to([2.5, g_y, 0])
    zero = _node("[0]").move_to([2.5, a_y, 0])
    e_g = _edge((rx, root.get_y()), (rx + 0.2, root.get_y()), (rx + 0.2, g_y), (star.get_left()[0], g_y))
    e_a = _edge((rx, root.get_y()), (rx + 0.2, root.get_y()), (rx + 0.2, a_y), (zero.get_left()[0], a_y))
    k_g = Mono("genres", KS, TEAL)
    k_g.move_to([(rx + 0.2 + star.get_left()[0]) / 2, g_y + 0.24, 0])
    k_a = Mono("actors", KS, TEAL)
    k_a.move_to([(rx + 0.2 + zero.get_left()[0]) / 2, a_y + 0.24, 0])
    leaves, forks = VGroup(), VGroup()
    sx = star.get_right()[0]
    for i, name in enumerate(["Comedy", "Drama", "Family"]):
        y = g_y + 0.34 * (1 - i)
        lf = Mono(f'"{name}"', KS, TEAL)
        lf.move_to([sx + 0.55 + lf.width / 2, y, 0])
        leaves.add(lf)
        forks.add(_edge((sx, g_y), (sx + 0.2, g_y), (sx + 0.2, y), (sx + 0.45, y)))
    leaf = Mono('"Charles Chaplin"', KS, TEAL)
    leaf.move_to([zero.get_x() + 0.35, l_y, 0])
    e_n = _edge((zero.get_x(), zero.get_bottom()[1]), (zero.get_x(), leaf.get_top()[1] + 0.08))
    k_n = Mono("name", KS, TEAL).next_to(e_n, RIGHT, buff=0.12)
    g = VGroup(e_g, e_a, forks, e_n, root, star, zero, k_g, k_a, k_n, leaves, leaf)
    g.leaves = leaves
    return g


def r4_thumb():
    t = S5.recap_thumb()
    t.err.scale(1.3, about_edge=DOWN)
    return t


def r5_thumb():
    """s6's thumb, lighter: the Crime/Drama Venn with GOLD 397, list_contains -> GOLD 72."""
    r, d = 0.75, 0.4
    crime = Circle(radius=r).move_to(d * LEFT).set_stroke(BLUE, 4).set_fill(BG, 0)
    drama = Circle(radius=r).move_to(d * RIGHT).set_stroke(BLUE, 4).set_fill(BG, 0)
    both = Intersection(crime, drama).set_stroke(width=0).set_fill(BLUE, 0.45)
    n = T("397", 28, GOLD).move_to(both)
    cn = T("Crime", 24, YELLOW).next_to(crime, LEFT, buff=0.12)
    dn = T("Drama", 24, YELLOW).next_to(drama, RIGHT, buff=0.12)
    venn = VGroup(both, crime, drama, n, cn, dn)
    fn = Mono("list_contains", 26, BLUE)
    arrow = Arrow(LEFT, RIGHT, buff=0, stroke_width=4).set_color(DIM).scale(0.3)
    m = T("72", 34, GOLD)
    row = VGroup(fn, arrow, m).arrange(RIGHT, buff=0.2)
    g = VGroup(venn, row).arrange(DOWN, buff=0.3)
    g.venn, g.row = venn, row
    return g


def r6_thumb():
    """s7's thumb, lighter: the BLUE and TEAL 1,086 frames, birth_year -> PINK NULL."""
    cards = VGroup()
    for col in (BLUE, TEAL):
        num = T("1,086", 36, GOLD)
        frame = RoundedRectangle(corner_radius=0.15, width=1.9, height=0.85)
        frame.set_stroke(col, 3).set_fill(col, 0.06)
        num.move_to(frame)
        cards.add(VGroup(frame, num))
    cards.arrange(RIGHT, buff=0.35)
    key = Mono("birth_year", 28, FG)
    arr = Arrow(LEFT, RIGHT, buff=0, stroke_width=4, color=PINK).scale(0.3)
    nul = Mono("NULL", 28, PINK)
    typo = VGroup(key, arr, nul).arrange(RIGHT, buff=0.2)
    g = VGroup(cards, typo).arrange(DOWN, buff=0.4)
    g.cards, g.typo = cards, typo
    return g


def r3_thumb():
    g = S4.dict_grid()
    n = T("321", 48, GOLD)
    out = VGroup(g, n).arrange(RIGHT, buff=0.8)
    out.grid, out.num = g, n
    return out


def place(t, i):
    r, k = divmod(i, 3)
    t.scale(min(THUMB_W / t.width, THUMB_H / t.height))
    t.move_to([COL_X[k], ROW_TOP[r] - THUMB_H / 2, 0])
    return t


def label(i):
    r, k = divmod(i, 3)
    lab = T(LABELS[i], 28, line_spacing=0.9)
    lab.move_to([COL_X[k], ROW_TOP[r] - THUMB_H - 0.2 - lab.height / 2, 0])
    return lab


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()

    def dim_prev(self):
        return set_alpha(self.shown, DIM_TO) if self.shown else []

    # ------------------------------------------------------------ c7.recap.1
    def clip1(self):
        self.shown = []
        with self.say("c7.recap.1") as c:
            title = T("Recap", 44).move_to([0, 3.22, 0])
            self.play(*appear(title, shift=None), run_time=1.0)  # early: the recap title
            c.wait_until("r1")

            # r1: -> keeps JSON, ->> gives a string
            t1 = place(S2.recap_thumb(), 0)
            l1 = label(0)
            top, bot = VGroup(*t1[0:4]), VGroup(*t1[4:8])
            self.play(*appear(top, l1, lag=0.3, shift=None), run_time=1.2)  # early: the recap line lands on {r1}
            c.wait_until("double arrow")
            self.play(*appear(bot, shift=None), run_time=1.0)
            settle(self, t1)
            self.shown = [t1, l1]
            c.wait_until("r2")

            # r2: the JSON path walk
            t2 = place(r2_thumb(), 1)
            l2 = label(1)
            self.play(*self.dim_prev(), *appear(t2, l2, lag=0.3, shift=None), run_time=1.4)  # early: the recap line lands on {r2}
            c.wait_until("a star")
            self.play(*flash([t2.leaves], color=TEAL,
                             run_time=1.5, time_width=1.5), run_time=1.5)
            self.shown += [t2, l2]
            c.wait_until("r3")

            # r3: cast before comparing
            t3 = place(r3_thumb(), 2)
            l3 = label(2)
            self.play(*self.dim_prev(), *appear(t3.grid, l3, lag=0.3, shift=None), run_time=1.4)  # early: the recap line lands on {r3}
            c.wait_until("cast")
            self.play(*appear(t3.num, shift=None), run_time=1.0)
            settle(self, t3)
            c.wait_until("ninety-nine")
            self.play(FlashAround(t3.grid.col_box, run_time=1.5, time_width=1.5), run_time=1.5)
            self.shown += [t3, l3]

    # ------------------------------------------------------------ c7.recap.2
    def clip2(self):
        with self.say("c7.recap.2", gap=1.0) as c:
            # r4: parentheses
            t4 = place(r4_thumb(), 3)
            l4 = label(3)
            self.play(*self.dim_prev(), *appear(t4.err, l4, lag=0.3, shift=None), run_time=1.2)  # early: the recap line lands on {r4}
            c.wait_until("parentheses")
            self.play(*appear(t4.code, shift=None), run_time=min(1.0, c.until("r5")))
            settle(self, t4)
            self.shown += [t4, l4]
            c.wait_until("r5")

            # r5: list_contains / list_has_all
            t5 = place(r5_thumb(), 4)
            l5 = label(4)
            self.play(*self.dim_prev(), *appear(t5.venn, l5, lag=0.3, shift=None), run_time=1.2)  # early: the recap line lands on {r5}
            c.wait_until("list contains")
            self.play(*appear(t5.row, shift=None), run_time=1.0)
            settle(self, t5)
            self.shown += [t5, l5]
            c.wait_until("r6")

            # r6: json_exists, missing key = NULL
            t6 = place(r6_thumb(), 5)
            l6 = label(5)
            self.play(*self.dim_prev(), *appear(t6.cards, l6, lag=0.3, shift=None), run_time=1.2)  # early: the recap line lands on {r6}
            c.wait_until("missing key")
            self.play(*appear(t6.typo, shift=None), run_time=1.0)
            settle(self, t6)
            self.shown += [t6, l6]

    # ------------------------------------------------------------ c7.recap.3
    def clip3(self):
        with self.say("c7.recap.3", gap=8.0) as c:
            oc = N8.open_card(lifted=False)
            tgt = N8.open_card(lifted=True)
            sweep_clear(self, time_span(FadeIn(oc.table), 0.75, 1.6),
                        time_span(FadeIn(oc.cell), 1.0, 1.6),
                        time_span(FadeIn(oc.tag), 1.0, 1.6),
                        time_span(FadeIn(oc.link), 1.1, 1.6),
                        time_span(FadeIn(oc.doc), 1.1, 1.6),
                        *[time_span(FadeIn(ch), 1.1 + 0.05 * i, 1.35 + 0.05 * i) for i, ch in enumerate(oc.chips)],
                        run_time=1.8)
            c.wait_until("rows")
            self.play(*during(appear(*tgt.slots, shift=None, lag=0.06), 0, 0.6),
                      *during([ch.animate.move_to(t.get_center()) for ch, t in zip(oc.chips, tgt.chips)],
                              0.15, 1),
                      run_time=min(2.4, c.until()))
            settle(self, oc, add=[tgt.slots])
        # end card: held through the 8 s gap, no fade (ch8 s1 opens on exactly this)
