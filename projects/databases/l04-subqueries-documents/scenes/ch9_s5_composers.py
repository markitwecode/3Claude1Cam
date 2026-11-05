"""Chapter 9, scene 5: Exercise 14, composers with a join. Clips c9.composers.1 – c9.composers.4.

EXPORTS (static, no updaters; `load_scene("ch9_s5_composers").<name>()`):
- recap_r5(): the two Alan Parker cards (people-row style: BLUE frame, DIM cell bars, Mono 34; person IDs
  YELLOW, name and year FG) with their DIM T 30 credit line under each, centred at ORIGIN, ~8.3 wide,
  ~3.6 tall. `.cards` (two person_card VGroups: `.frame .pid .name .year .sub`).
- person_card(pid, name, year, sub=None, size=34, sub_size=30, sub_side=DOWN): one such card at ORIGIN.
Ends on an empty frame.
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

S1 = load_scene("ch9_s1_intro")
S2 = load_scene("ch9_s2_pairs")
C35 = load_scene("ch3_s5_semijoin")

JOIN_D = ("SELECT DISTINCT name FROM people AS p\nJOIN has_position AS hp\n  ON hp.person_id = p.person_id\n"
          " AND hp.position = 'composer'\nORDER BY name;")
SOL = ("SELECT DISTINCT p.person_id, p.name\nFROM people AS p\nJOIN has_position AS hp\n"
       "  ON hp.person_id = p.person_id\n AND hp.position = 'composer'\nORDER BY p.name;")
VAR = ("SELECT p.name\nFROM people AS p\nJOIN has_position AS hp\n  ON hp.person_id = p.person_id\n"
       " AND hp.position = 'composer'\nGROUP BY p.person_id, p.name\nORDER BY p.name;")
SOL_ROWS = [("nm1621450", "A.C. Newman"), ("nm0006246", "A.R. Rahman"),
            ("nm7541028", "Aaron May"), ("nm0956374", "Aaron Zigman")]
ALAN = [("nm0000570", "Alan Parker", "1944", "director · The Life of David Gale (2003)"),
        ("nm0662029", "Alan Parker", "1944", "composer · What's Eating Gilbert Grape (1993)")]
SAM = [("nm0680767", "Sam Phillips", "1962", "Die Hard with a Vengeance"),
       ("nm0680771", "Sam Phillips", "1948", "Ace Ventura: When Nature Calls"),
       ("nm1012657", "Sam Phillips", "1984", "Far from the Madding Crowd")]
CODE_X = -4.35      # left edge of the hero code in clips 3-4
CODE_TOP = 3.5


# ---------------------------------------------------------------- shared pieces
def person_card(pid, name, year, sub=None, size=34, sub_size=30, sub_side=DOWN):
    pad = 0.25
    texts = [Mono(pid, size, YELLOW), Mono(name, size, FG), Mono(year, size, FG)]
    widths = [t.width + 2 * pad for t in texts]
    h = 0.022 * size
    W = sum(widths)
    frame_box = Rectangle(width=W, height=h).set_stroke(BLUE, 2).set_fill(BG, 0)
    x = -W / 2
    bars = []
    for j, (t, w) in enumerate(zip(texts, widths)):
        t.move_to([x + w / 2, 0, 0])
        x += w
        if j < 2:
            bars.append(Line([x, -h / 2, 0], [x, h / 2, 0]).set_stroke(DIM, 1.5))
    frame = VGroup(frame_box, *bars)
    g = VGroup(frame, *texts)
    g.frame, g.pid, g.name, g.year = frame, texts[0], texts[1], texts[2]
    g.sub = None
    if sub:
        s = T(sub, sub_size, DIM)
        if sub_side is DOWN or (isinstance(sub_side, np.ndarray) and sub_side[1] < 0):
            s.next_to(frame_box, DOWN, buff=0.18).align_to(frame_box, LEFT)
        else:
            s.next_to(frame_box, RIGHT, buff=0.25)
        g.sub = s
        g.add(s)
    return g


def recap_r5():
    cards = [person_card(*a) for a in ALAN]
    cards[1].next_to(cards[0], DOWN, buff=0.75).align_to(cards[0], LEFT)
    g = VGroup(*cards).move_to(ORIGIN)
    g.cards = cards
    return g


def res_table(cols, rows, size=30, pitch=0.5, gap=0.6):
    """Slide-style result: DIM header, DIM rule, FG rows, DIM dot. Header's top-left at ORIGIN."""
    heads = [Mono(c, size, DIM) for c in cols]
    cells = [[Mono(v, size, FG) for v in r] for r in rows]
    widths = [max([heads[j].width] + [cells[i][j].width for i in range(len(rows))]) for j in range(len(cols))]
    xs = [sum(widths[:j]) + gap * j for j in range(len(cols))]
    for j, hd in enumerate(heads):
        hd.move_to([0, -0.2, 0]).align_to([xs[j], 0, 0], LEFT)
    for i, r in enumerate(cells):
        for j, t in enumerate(r):
            t.move_to([0, -0.2 - (i + 1) * pitch - 0.08, 0]).align_to([xs[j], 0, 0], LEFT)
    W = xs[-1] + widths[-1]
    rule = Line([-0.1, -0.45, 0], [W + 0.1, -0.45, 0]).set_stroke(DIM, 2)
    dot = Mono("·", size, DIM).move_to([0, -0.2 - (len(rows) + 1) * pitch - 0.08, 0]).align_to([0, 0, 0], LEFT)
    g = VGroup(*heads, rule, *[t for r in cells for t in r], dot)
    g.heads, g.cells, g.rule, g.dot, g.xs, g.W = heads, cells, rule, dot, xs, W
    return g


def place_tl(mob, left, top):
    mob.shift([left - mob.get_left()[0], top - mob.get_top()[1], 0])
    return mob


def strike(glyphs, color=RED):
    return Line(glyphs.get_left() + 0.06 * LEFT, glyphs.get_right() + 0.06 * RIGHT).set_stroke(color, 5)


class Ch9S5Composers(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c9.composers.1
    def clip1(self):
        with self.say("c9.composers.1") as c:
            row = S1.ex_row()
            self.play(*appear(row, shift=None), run_time=0.8)  # early: the exercise row is the frame we open on
            big = S1.big_card(14)
            others = [row.cards[n] for n in (13, 15, 16)]
            self.play(*during([FadeOut(m) for m in others] + [FadeOut(row.cards[14].head),
                                                               FadeOut(row.cards[14].title)], 0, 0.4),
                      ReplacementTransform(row.cards[14].box.copy(), big.box),
                      *during([FadeOut(row.cards[14].box)], 0, 0.3),
                      *during(appear(big.text, shift=None), 0.55, 1),
                      run_time=min(2.0, c.until("List the people")))  # early: the exercise card is read aloud
            self.remove(*row.get_family())
            c.wait_until("It must stay right")
            self.play(*appear(big.hint), run_time=1.0)  # early: the hint is part of the exercise card
            c.wait_until("stop")
            self.play(*appear(big.pause, shift=None), run_time=0.8)
            self.big = big

    # ------------------------------------------------------------ c9.composers.2
    def clip2(self):
        with self.say("c9.composers.2") as c:
            code = C35.join_code(32)
            place_tl(code, -6.3, 3.3)
            jc = S2.join_card()
            jc.scale_to_fit_height(2.3)
            jc.move_to([4.6, 1.0, 0])
            jc.set_color(DIM)
            sweep_clear(self, *during(appear(code, jc, shift=None), 0.5, 1))  # early: the query is shown whole, then read

            c.wait_until("three thousand")
            n = T("3,281 rows", 44, GOLD).move_to([4.3, -1.2, 0])
            self.play(*appear(n), run_time=1.0)
            c.wait_until("Hans Zimmer")
            zt = C35.zimmer_tag(36)
            zc = check_mark().scale(0.8).next_to(zt, RIGHT, buff=0.2)
            VGroup(zt, zc).next_to(n, DOWN, buff=0.4).set_x(n.get_x())
            self.play(*appear(zt, zc), run_time=1.0)

            c.wait_until("distinct")
            dcode = Code(JOIN_D, size=32)
            place_tl(dcode, -6.3, 3.3)
            for g in dcode.find("DISTINCT"):
                g.set_color(YELLOW)
            self.play(*edit(code, dcode), run_time=min(1.5, c.until("whole")))
            code = dcode

            c.wait_until("whole")
            tab = res_table(["name"], [["A.C. Newman"], ["A.R. Rahman"], ["A.R. Rahman"]])
            place_tl(tab, -6.2, -0.35)
            tab.remove(tab.dot)
            self.play(*appear(*tab, lag=0.1, shift=None), run_time=1.2)
            last = tab.cells[2][0]
            row_l, row_r = tab.rule.get_left()[0], tab.rule.get_right()[0]
            br = span_brace([row_l, last.get_bottom()[1], 0], [row_r, last.get_bottom()[1], 0],
                            direction=DOWN, color=YELLOW, buff=0.12)
            cap = T("DISTINCT compares whole rows", 32, YELLOW).next_to(br, DOWN, buff=0.15)
            cap.align_to(tab, LEFT)
            c.wait_until(own_word=cap)
            self.play(GrowFromCenter(br), *appear(cap), run_time=1.2)

    # ------------------------------------------------------------ c9.composers.3
    def clip3(self):
        with self.say("c9.composers.3") as c:
            sol = Code(SOL, size=30)
            place_tl(sol, CODE_X, CODE_TOP)
            pid = sol.find("p.person_id", line=0)
            for g in pid:
                g.set_color(YELLOW)
            sweep_clear(self, *during(appear(sol, shift=None), 0.5, 1))  # early: the answer is shown whole, then read

            c.wait_until("person ID")
            self.play(FlashUnder(pid, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("result")
            tab = res_table(["person_id", "name"], [list(r) for r in SOL_ROWS])
            place_tl(tab, CODE_X + 0.1, sol.get_bottom()[1] - 0.25)
            self.play(*appear(*tab, lag=0.08, shift=None), run_time=1.5)
            c.wait_until("one thousand")
            n = T("1,086 rows", 44, GOLD).move_to([3.7, tab.cells[1][0].get_y(), 0])
            self.play(*appear(n), run_time=1.0)
            c.wait_until("the same as exists")
            eq = VGroup(T("=", 44, GREEN), Mono("EXISTS", 30, DIM), T("1,086", 36, GOLD)).arrange(RIGHT, buff=0.25)
            eq.next_to(n, DOWN, buff=0.45)
            self.play(*appear(eq), run_time=1.0)

            c.wait_until("group")
            var = Code(VAR, size=30)
            place_tl(var, CODE_X, CODE_TOP)
            drop = [tab.heads[0], *[r[0] for r in tab.cells]]
            dx = tab.xs[1] - tab.xs[0]
            keep = [tab.heads[1], *[r[1] for r in tab.cells]]
            new_rule = Line(tab.rule.get_left(), tab.rule.get_left() + RIGHT * (tab.W - dx)).set_stroke(DIM, 2)
            new_rule.shift(DOWN * 0.54)
            self.play(*edit(sol, var),
                      *during(disappear(*drop), 0, 0.4),
                      *during([m.animate.shift(LEFT * dx + DOWN * 0.54) for m in keep]
                              + [tab.dot.animate.shift(DOWN * 0.54), Transform(tab.rule, new_rule)], 0.4, 1),
                      run_time=min(2.0, c.until()))
            self.remove(*drop)
            self.code, self.tab, self.keep, self.n, self.eq = var, tab, keep, n, eq

    # ------------------------------------------------------------ c9.composers.4
    def clip4(self):
        with self.say("c9.composers.4") as c:
            var, tab, keep, n = self.code, self.tab, self.keep, self.n
            sol = Code(SOL, size=30)
            place_tl(sol, CODE_X, CODE_TOP)
            pid = sol.find("p.person_id,", line=0)
            for g in pid:
                g.set_color(YELLOW)
            self.play(*edit(var, sol),
                      *[m.animate.shift(UP * 0.54) for m in keep + [tab.dot, tab.rule]],
                      run_time=1.3)
            st = strike(pid)
            self.play(Create(st), *recolor(pid, RED), run_time=1.0)

            c.wait_until("luck")
            luck = T("luck", 30, DIM).next_to(n, RIGHT, buff=0.3)
            self.play(FlashAround(n, run_time=1.5, time_width=1.5), *appear(luck), run_time=1.5)  # early: the tag sums up the line

            # ---- the two Alan Parkers
            c.wait_until("alan")
            r5 = recap_r5().shift(DOWN * 0.45)
            a, b = r5.cards
            for card in (a, b):
                card.remove(card.sub)
            ghost = Mono("DISTINCT p.name", 30, DIM).move_to([0, 2.9, 0])
            sweep_clear(self, *during(appear(a, b, lag=0.3, shift=None), 0.5, 1))
            c.wait_until("both born")
            self.play(*appear(ghost, shift=None),
                      *during([FadeOut(b, shift=0.7 * UP)], 0, 0.7),
                      *set_alpha([a.pid], 0.25), run_time=1.5)
            c.wait_until("One is credited")
            self.play(*disappear(ghost),
                      *during([FadeIn(b, shift=0.7 * DOWN)], 0.2, 1),
                      *set_alpha([a.pid], 1), run_time=1.2)
            sub_a, sub_b = r5.cards[0].sub, r5.cards[1].sub
            c.wait_until(own_word=sub_a)
            self.play(*appear(sub_a), run_time=1.0)
            c.wait_until(own_word=sub_b)
            self.play(*appear(sub_b), run_time=1.0)

            # ---- actors
            c.wait_until("actors")
            pos = Code(" AND hp.position = 'composer'", size=32).move_to([0, 3.25, 0])
            sweep_clear(self, *during(appear(pos, shift=None), 0.5, 1), run_time=1.0)
            pos2 = Code(" AND hp.position = 'actor'", size=32).move_to([0, 3.25, 0])
            for g in pos2.find("'actor'"):
                g.set_color(YELLOW)
            self.play(*edit(pos, pos2), run_time=1.0)

            c.wait_until("distinct name loses")
            q1 = Code("SELECT DISTINCT p.name", size=28)
            q2 = Code("SELECT DISTINCT p.person_id, p.name", size=28)
            place_tl(q1, -6.3, 2.45)
            place_tl(q2, -6.3, 1.75)
            n1 = T("15,458 rows", 36, GOLD).move_to(q1).align_to([2.5, 0, 0], LEFT)
            n2 = T("15,473 rows", 36, GOLD).move_to(q2).align_to([2.5, 0, 0], LEFT)
            minus = T("−15", 44, RED).move_to([5.7, (n1.get_y() + n2.get_y()) / 2, 0])
            self.play(*during(disappear(pos2), 0, 0.35), *during(appear(q1, n1, q2, n2, lag=0.25, shift=None), 0.35, 1), run_time=1.6)  # early: the counts are the result being read  # noqa: E501
            self.play(*appear(minus), run_time=0.8)

            c.wait_until("three different actors")
            sams = [person_card(*s, size=28, sub_size=28, sub_side=RIGHT) for s in SAM]
            for i, s in enumerate(sams):
                s.shift([-6.5 - s.frame.get_left()[0], 0.35 - 1.05 * i - 0.3, 0])
            self.play(*appear(*sams, lag=0.3, shift=None), run_time=1.3)
            c.wait_until("become one")
            s0 = sams[0]
            self.play(*during([FadeOut(s, shift=0.45 * UP) for s in sams[1:]], 0, 0.7),
                      restyle(s0.frame, outline=RED), s0.name.animate.set_color(RED),
                      *set_alpha([s0.pid], 0.25), run_time=1.5)

            c.wait_until("key")
            others = [m for s in sams for m in (s.name, s.year, s.sub)]
            self.play(*[FadeIn(s, shift=0.45 * DOWN) for s in sams[1:]],
                      restyle(s0.frame, outline=BLUE, width=2), s0.name.animate.set_color(FG),
                      *set_alpha([s0.pid], 1), run_time=1.3)
            c.wait_until("Keys")
            self.play(*set_alpha(others + [q1, q2, n1, n2], 0.35),
                      *flash([s.pid for s in sams]), run_time=1.5)
