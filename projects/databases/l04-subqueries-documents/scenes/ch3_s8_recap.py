"""Chapter 3, scene 8: try these (Exercises 13 and 14, with hints), then the recap. Clips c3.recap.1 – c3.recap.5.

Recap: ch1_s8_recap's pattern, four DIM slots along the top; each callback big while its sentence
plays, then it shrinks into its slot. Ends non-empty by design (chapter's last scene; reversed join onto
ch4 s1, which opens on the same card and clears it itself): the last frame is
load_scene("ch4_s1_hook").open_card().
"""
# style: 2
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SCH = load_scene("ch1_s2_schema")
H1 = load_scene("ch3_s1_hook")
LOOP = load_scene("ch3_s2_correlated")
IMM = load_scene("ch3_s4_immune")
SEMI = load_scene("ch3_s5_semijoin")
LOOPS = load_scene("ch3_s6_loops")
KIT = load_scene("ch3_s7_toolkit")
DER = load_scene("ch2_s6_derive")
DOC = load_scene("ch4_s3_movie")

SCH.SCHEMA.setdefault("r", (("x", "y"), ()))
SCH.SCHEMA.setdefault("s", (("y", "z"), ()))

EX13 = ["Exercise 13. The following pairs of queries are over",
        "two tables, r with columns x and y, and s with columns",
        "y and z. For each pair, say whether the two queries",
        "always return the same result. If they do not, give an",
        "example database on which the results differ."]
EX14 = ["Exercise 14. Write a query that returns the names of",
        "people who are credited as a composer on at least one",
        "movie, like on the slide, but using an inner join instead",
        "of the EXISTS or IN operator. Be careful that it still",
        "gives the right answer if two different people in the",
        "database happen to have the same name."]
PAIRS = [
    ("SELECT r.x FROM r WHERE r.y IN (SELECT s.y FROM s);",
     "SELECT r.x FROM r JOIN s ON r.y = s.y;"),
    ("SELECT r.x FROM r JOIN s ON r.y = s.y AND s.z = 99;",
     "SELECT r.x FROM r JOIN s ON r.y = s.y WHERE s.z = 99;"),
    ("SELECT r.x FROM r LEFT JOIN s ON r.y = s.y AND s.z = 99;",
     "SELECT r.x FROM r LEFT JOIN s ON r.y = s.y WHERE s.z = 99;"),
    ("SELECT r.x FROM r LEFT JOIN s ON r.y = s.y WHERE s.y IS NULL;",
     "SELECT r.x FROM r WHERE r.y NOT IN (SELECT s.y FROM s);"),
]
RESULT_1977 = [("Annie Hall", None), ("Close Encounters of the Third Kind", "John Williams"),
               ("Star Wars: Episode IV - A New Hope", "John Williams")]
HINT_X = 0.3          # centre of the hint pictures
CORNER = [(-5.6, -3.3), (5.6, -3.3)]   # the two collapsed exercise cards
SLOT_X = (-4.95, -1.65, 1.65, 4.95)     # ch1_s8_recap's strip of four slots
SLOT_Y = 2.85
SLOT_W, SLOT_H = 3.1, 1.3
HERO_W, HERO_H, HERO_Y = 12.6, 4.9, -0.4
LINE_Y = -3.3


END_CARD = lambda: load_scene("ch4_s1_hook").open_card()    # ch4's first frame (.toolkit .doc .brace .label)


# ---------------------------------------------------------------- helpers
def fit(mob, w, h, center, most=10.0):
    mob.scale(min(w / mob.width, h / mob.height, most))
    mob.move_to(center)
    return mob


def ex_card(lines, size=30, extra_h=0.0):
    head = lines[0].split(".")[0] + "."
    text = VGroup(*[T(s, size, t2c={head: YELLOW} if i == 0 else None) for i, s in enumerate(lines)])
    text.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.2, width=text.width + 0.8, height=text.height + 0.7 + extra_h)
    box.set_stroke(DIM, 2).set_fill(BG, 0)
    text.move_to(box).align_to(box, UP).shift(0.35 * DOWN)
    g = VGroup(box, text)
    g.box, g.text = box, text
    return g


def table(name, x, top, scale=1.0):
    card = SCH.TableCard(name, 0, 0)
    card.scale(scale)
    card.move_to([x, top - card.height / 2, 0])
    return card


def row_of(card, col):
    return card.rows[col].get_center()[1]


def null_in(card, col):
    chip = H1.null_chip().scale(0.8)
    chip.move_to([card.box.get_right()[0] - chip.width / 2 - 0.15, row_of(card, col), 0])
    return chip


def pill(text, size=28):
    lab = Mono(text, size)
    box = RoundedRectangle(corner_radius=0.12, width=lab.width + 0.45, height=0.62).set_stroke(BLUE, 2.5)
    lab.move_to(box)
    return VGroup(box, lab)


def pair_block(i, a, b, size=24):
    code = Code(a + "\n" + b, size=size)
    num = T(f"{i}.", 32, GOLD)
    num.next_to(code.line(0), LEFT, buff=0.3)
    g = VGroup(num, code)
    g.num, g.code = num, code
    return g


def result_rows(size=26):
    rows = VGroup()
    for k, (title, comp) in enumerate(RESULT_1977):
        t = Mono(title, size)
        c = Mono(comp if comp else "null", size, color=FG if comp else PINK)
        t.move_to([0, -k * 0.55, 0], aligned_edge=LEFT)
        c.move_to([t.get_left()[0] + 7.8, -k * 0.55, 0], aligned_edge=LEFT)
        rows.add(VGroup(t, c))
    return rows


def caption(text, t2c=None, size=30):
    return T(text, size, t2c=t2c).move_to([0, LINE_Y, 0])


def mini_card(title):
    lab = T(title, 28)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.5, height=0.7).set_stroke(DIM, 2)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def into_slot(mobs, i):
    """ch1_s8_recap's move: the top-level mobs (as one picture) shrink in place, then rise into slot i."""
    bb = VGroup(*[m.copy() for m in mobs])
    k = min((SLOT_W - 0.25) / bb.width, (SLOT_H - 0.2) / bb.height)
    ctr = bb.get_center()
    dst = np.array([SLOT_X[i], SLOT_Y, 0])
    starts = [m.copy() for m in mobs]

    def make(m, s0):
        def upd(mob, a):
            a1 = smooth(min(1.0, a / 0.45))
            a2 = smooth(max(0.0, (a - 0.45) / 0.55))
            ax = min(1.0, 1.6 * a2)
            d = dst - ctr
            mob.become(s0.copy().scale(1 + (k - 1) * a1, about_point=ctr)
                       .shift(np.array([ax * d[0], a2 * d[1], 0])))
        return UpdateFromAlphaFunc(m, upd)
    return [make(m, s0) for m, s0 in zip(mobs, starts)]


def r1_loop():
    """s2's outer loop (its own layout, text 28), cursor on The Kid, Kid rows lit, counter 12."""
    kw = dict(LOOP.S2_LOOP)
    kw.update(right_rows=LOOP.S2_ROWS[:5] + [None], lx=-6.2, rx=6.2, ltop=1.5, ctop=2.0, count_y=-0.4)
    loop = LOOP.outer_loop(**kw)
    for i in range(1, 5):
        loop.card.rows[i].set_color(YELLOW)
    old = loop.counter
    loop.remove(old)
    loop.add(Mono("12", 44, color=GOLD).move_to(old))
    return VGroup(loop, loop.cursor_at(0))


def r2_pair():
    """s4's sealed box (its GOLD count coming out to the right) over ch3 s1's trap_back()."""
    box = IMM.sealed_box()
    box.remove(box.arrow)
    box.count.next_to(box.box, RIGHT, buff=1.3)
    arrow = Arrow(box.box.get_right(), box.count.get_left(), buff=0.15, stroke_width=4).set_color(GOLD)
    box.add(arrow)
    trap = H1.trap_back()
    return VGroup(box, trap).arrange(DOWN, buff=0.3)


def _inner(src, first, last):
    """Lines first..last of one of s6's loops, comments dropped, dedented: its inner loop."""
    lines = [l.split("  #")[0].rstrip() for l in src.splitlines()[first:last + 1]]
    return textwrap.dedent("\n".join(lines))


SEMI_LOOP = _inner(LOOPS.SEMI_SRC, 2, 5)    # for credit … break
ANTI_LOOP = _inner(LOOPS.ANTI_SRC, 3, 6)    # for role … break


def r4_loops(size=26):
    """s6's two inner loops (comments left out), the changed lines and `break` YELLOW."""
    semi = Code(SEMI_LOOP, size=size, lang="python")
    semi.line(2).set_color(YELLOW)
    semi.line(3).set_color(YELLOW)
    anti = Code(ANTI_LOOP, size=size, lang="python")
    anti.find("matched").set_color(YELLOW)
    anti.find("break").set_color(YELLOW)
    return VGroup(semi, anti).arrange(DOWN, buff=0.35, aligned_edge=LEFT)


class Recap(NarratedScene):
    def construct(self):
        self.exercise13()
        self.hints()
        self.exercise14()
        self.recap()
        self.next_time()

    # ------------------------------------------------------------ c3.recap.1
    def exercise13(self):
        with self.say("c3.recap.1") as c:
            card = ex_card(EX13, size=34).move_to([0, 2.05, 0])
            self.ex13 = card
            self.play(*appear(card, shift=None), run_time=min(1.2, c.until("tables")))  # early: the exercise card, read whole
            c.wait_until("tables")
            r = table("r", -2.8, -0.55, scale=1.5)
            s = table("s", 2.8, -0.55, scale=1.5)
            self.play(*appear(r, s, lag=0.3), run_time=min(1.4, c.until("the first has")))
            first = T("first", 30, DIM).next_to(r, DOWN, buff=0.25)
            second = T("second", 30, DIM).next_to(s, DOWN, buff=0.25)
            c.wait_until(own_word=first)
            self.play(*appear(first), run_time=0.8)
            c.wait_until(own_word=second)
            self.play(*appear(second), run_time=0.8)
            c.wait_until("pairs")
            sweep_clear(self, run_time=min(1.0, c.until("for each pair")))
            pairs = VGroup(*[pair_block(i + 1, a, b) for i, (a, b) in enumerate(PAIRS)])
            pairs.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
            fit(pairs, 12.6, 6.6, [0, 0, 0])
            self.pairs = pairs
            self.play(*appear(*pairs, lag=0.35), run_time=min(2.0, c.until("for each pair")))  # early: the four pairs, shown whole then walked

    # ------------------------------------------------------------ c3.recap.2
    def hints(self):
        pairs = self.pairs
        with self.say("c3.recap.2", gap=1.4) as c:
            pairs.generate_target()
            pairs.target.scale(11.4 / pairs.width).move_to([0, 0, 0]).align_to([0, 3.65, 0], UP)
            head = T("Hints", 36, YELLOW).move_to([0, -0.85, 0]).align_to([-6.4, 0, 0], LEFT)
            self.play(*during([MoveToTarget(pairs)], 0, 0.7), *during(appear(head), 0.5, 1),
                      run_time=min(1.4, c.until("one")))
            c.wait_until("one")
            # -- pair 1: one row of r meets two rows of s
            rp = pill("(1, 5)").move_to([HINT_X - 3.2, -2.4, 0])
            sp1 = pill("(5, 10)").move_to([HINT_X + 1.2, -1.85, 0])
            sp2 = pill("(5, 20)").move_to([HINT_X + 1.2, -2.95, 0])
            rh = Mono("r", 30, BLUE, weight=BOLD).next_to(rp, UP, buff=0.2)
            sh = Mono("s", 30, BLUE, weight=BOLD).next_to(sp1, UP, buff=0.15)
            others = [pairs[1], pairs[2], pairs[3]]
            self.play(*set_alpha(others, DIMMED), *appear(rh, rp, sh, sp1, sp2, lag=0.15),
                      run_time=min(1.4, c.until("when one row")))
            c.wait_until("when one row")
            a1 = Arrow(rp.get_right(), sp1.get_left(), buff=0.12, stroke_width=4).set_color(YELLOW)
            a2 = Arrow(rp.get_right(), sp2.get_left(), buff=0.12, stroke_width=4).set_color(YELLOW)
            twice = T("twice?", 36, YELLOW).next_to(VGroup(sp1, sp2), RIGHT, buff=0.6)
            self.play(GrowArrow(a1), GrowArrow(a2), *during(appear(twice), 0.45, 1),
                      run_time=min(1.4, c.until("two")))
            pic1 = [rp, sp1, sp2, rh, sh, a1, a2, twice]
            # -- pair 2: ON or WHERE, inner join
            c.wait_until("two")
            self.play(*during(disappear(*pic1), 0, 0.45), *set_alpha([pairs[0]], DIMMED),
                      *set_alpha([pairs[1]], 1), run_time=min(1.2, c.until("does it matter")))
            same = T("inner join: same?", 36, YELLOW).move_to([HINT_X, -1.55, 0])
            c.wait_until(own_word=same)
            self.play(*appear(same), run_time=min(1.0, c.until("does it matter")))
            on = Mono("ON", 48, BLUE).move_to([HINT_X - 2.0, -2.75, 0])
            orw = T("or", 32, DIM).move_to([HINT_X, -2.75, 0])
            where = Mono("WHERE", 48, BLUE).move_to([HINT_X + 2.4, -2.75, 0])
            c.wait_until("on clause")
            self.play(*appear(on), run_time=min(0.8, c.until("where clause")))
            c.wait_until("where clause")
            self.play(*appear(orw, where, lag=0.2), run_time=min(1.0, c.until("three")))
            pic2 = [same, on, orw, where]
            # -- pair 3: the left join, slide 54's 1977 result
            c.wait_until("three")
            rows = result_rows().move_to([HINT_X, -2.05, 0])
            self.play(*during(disappear(*pic2), 0, 0.45), *set_alpha([pairs[1]], DIMMED),
                      *set_alpha([pairs[2]], 1), *during(appear(*rows, lag=0.2), 0.45, 1),
                      run_time=min(1.8, c.until("where")))
            c.wait_until("where")
            annie = rows[0]
            strike = Line(annie.get_left() + 0.15 * LEFT, annie.get_right() + 0.15 * RIGHT).set_stroke(RED, 5)
            two = T("2 rows", 32, GOLD).next_to(rows, DOWN, buff=0.3).align_to(rows, RIGHT)
            self.play(Create(strike), *recolor(annie, RED), run_time=min(1.4, c.until("four")))
            self.play(*appear(two), run_time=min(0.9, c.until("four")))
            pic3 = [*rows, strike, two]
            # -- pair 4: a NULL in s's y column, then in r's
            c.wait_until("four")
            r = table("r", HINT_X - 2.4, -0.95, scale=1.1)
            s = table("s", HINT_X + 2.4, -0.95, scale=1.1)
            self.play(*during(disappear(*pic3), 0, 0.45), *set_alpha([pairs[2]], DIMMED),
                      *set_alpha([pairs[3]], 1), *during(appear(r, s, lag=0.2), 0.45, 1),
                      run_time=min(1.6, c.until("null value")))
            c.wait_until("null value")
            n_s = null_in(s, "y")
            self.play(*appear(n_s, shift=0.5 * DOWN), run_time=min(1.0, c.until("or what if")))
            c.wait_until("or what if")
            n_r = null_in(r, "y")
            self.play(*appear(n_r, shift=0.5 * DOWN), run_time=min(1.0, c.until("think back")))
            c.wait_until("think back")
            chain = DER.and_chain().scale(0.8).move_to([HINT_X, -3.05, 0])
            self.play(*appear(chain), run_time=min(0.9, c.until()))

    # ------------------------------------------------------------ c3.recap.3
    def exercise14(self):
        with self.say("c3.recap.3") as c:
            card = ex_card(EX14, extra_h=0.85).move_to([0, 0.2, 0])
            hint = T("What does DISTINCT compare?", 36, YELLOW)
            hint.move_to([0, card.box.get_bottom()[1] + 0.6, 0])
            sweep_clear(self, time_span(FadeIn(card), 0.6, 1.3), run_time=1.3)  # early: the exercise card, read whole
            c.wait_until(own_word=hint)
            self.play(*appear(hint), run_time=min(1.0, c.until()))
            self.ex14 = VGroup(card, hint)

    # ------------------------------------------------------------ c3.recap.4
    def recap(self):
        with self.say("c3.recap.4", gap=1.0) as c:
            card, hint = self.ex14
            m13 = mini_card("Exercise 13").move_to([*CORNER[0], 0])
            m14 = mini_card("Exercise 14").move_to([*CORNER[1], 0])
            slots = [RoundedRectangle(corner_radius=0.12, width=SLOT_W, height=SLOT_H)
                     .set_stroke(DIM, 1.5, opacity=0.6).move_to([x, SLOT_Y, 0]) for x in SLOT_X]
            self.play(*during(disappear(card.text, hint), 0, 0.35), *during([Transform(card.box, m14.box)], 0.1, 0.7),
                      *during(appear(m14.label, m13, shift=None), 0.6, 1),
                      *during(appear(*slots, shift=None, lag=0.2), 0.3, 1), run_time=min(1.6, c.until("r1")))
            self.remove(*card.get_family(), *hint.get_family())
            self.add(m14.box)
            self.corner, self.slots = [m13, m14], slots

            # r1: the outer loop, cursor on The Kid, counter 12
            c.wait_until("r1")
            t1 = fit(r1_loop(), HERO_W, HERO_H, [0, HERO_Y, 0], most=1.0)
            cap1 = caption("a correlated subquery: once per outer row")
            self.play(*appear(t1, shift=None), run_time=min(1.2, c.until("r2")))  # early: a callback picture (its "rows" tag is never read)
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=min(1.0, c.until("r2")))

            # r2: r1 into its slot; the sealed box over the four GREEN movies and NOT IN's RED "0 rows"
            c.wait_until("r2")
            t2 = fit(r2_pair(), HERO_W, HERO_H, [0, HERO_Y, 0], most=1.0)
            cap2 = caption("NOT EXISTS: the antijoin, immune to NULL", t2c={"NOT EXISTS": BLUE, "NULL": PINK})
            self.play(*during(into_slot([t1], 0), 0, 0.55), *during(disappear(cap1), 0, 0.4),
                      *during(appear(t2, cap2, shift=None, lag=0.2), 0.55, 1), run_time=min(1.8, c.until("r3")))

            # r3: r2 into its slot; the two GOLD counts
            c.wait_until("r3")
            t3 = SEMI.counts().move_to([0, HERO_Y, 0])
            cap3 = caption("EXISTS: the semijoin, each left row at most once", t2c={"EXISTS": BLUE}, size=28)
            self.play(*during(into_slot([t2], 1), 0, 0.55), *during(disappear(cap2), 0, 0.4),
                      *during(appear(t3, cap3, shift=None, lag=0.2), 0.55, 1), run_time=min(1.8, c.until("three thousand")))
            c.wait_until("become")
            self.play(FlashAround(t3.exists_n, run_time=1.5, time_width=1.5), run_time=min(1.5, c.until("r4")))

            # r4: r3 into its slot; the two loops, break lines YELLOW
            c.wait_until("r4")
            t4 = fit(r4_loops(), HERO_W, HERO_H, [0, HERO_Y, 0], most=1.0)
            cap4 = caption("stop at the first match")
            self.play(*during(into_slot([t3], 2), 0, 0.55), *during(disappear(cap3), 0, 0.4),
                      *during(appear(t4, shift=None), 0.55, 1), run_time=min(1.8, c.until("stops")))
            c.wait_until("stops")
            self.play(*appear(cap4), run_time=min(1.0, c.until()))
            self.t4, self.cap4 = t4, cap4

    # ------------------------------------------------------------ c3.recap.5
    def next_time(self):
        end = END_CARD()
        with self.say("c3.recap.5") as c:
            self.play(*during(into_slot([self.t4], 3), 0, 0.8), *during(disappear(self.cap4), 0, 0.5),
                      run_time=min(1.4, c.until("toolkit")))
            c.wait_until("toolkit")
            big = end.toolkit.copy()
            big.scale(6.9 / big.height).move_to(ORIGIN)
            sweep_clear(self, time_span(FadeIn(big), 0.75, 1.5), run_time=1.5)  # early: the toolkit card, a callback shown whole
            c.wait_until("something completely")
            self.play(ReplacementTransform(big, end.toolkit), run_time=min(1.8, c.until("doc")))
            c.wait_until("doc")
            self.play(FadeIn(end.doc, scale=0.9), *during(appear(end.brace, shift=None), 0.4, 1),
                      run_time=min(1.4, c.until("with the kid")))
            c.wait_until("with the kid")
            self.play(*appear(end.label), run_time=min(1.0, c.until()))
        self.wait(7.7)      # the end card (= ch4's first frame), ~8 s after the last word; no fade (see docstring)
