"""Chapter 2, scene 7: recap, six callbacks in a 3x2 grid, ending on ch3's opening card. Clips c2.recap.1 – c2.recap.3.

Plan: tiles fill left to right, top to bottom, each with a DIM caption under it.
r1 {absent}: s2/s3's three queries (LEFT JOIN … IS NULL, EXCEPT, NOT IN) arrive big, each card ending
in GREEN "Flow, Kaiva", then shrink into tile 1. {column}: s3's `year IN (` + `)`, the column icon rises
into the parens, GREEN check (tile 2). {logic}: s5's rule card and AND grid big in the lower half; the
TRUE AND NULL cell sends out GREEN and RED ghosts, which merge back as PINK NULL; the pair shrinks into
tile 3. {where}: s5's WHERE gate in tile 4, TRUE passes, FALSE and NULL bounce.
r2 {chain}: s6's AND chain (parts stacked to fit the tile), the PINK link pulses (tile 5). {fix}: s6's
`WHERE deathyear IS NOT NULL` line, then the four GREEN cards beside the RED "0 rows" (tile 6).
r3 {next}: the grid sweeps away and ch3's open_card() is built (The Kid row, arrow, plays_role card,
"at least one?", 12 rows lit, EXISTS), held ~8 s, then faded. The thumbnails are small on purpose.
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

S2 = load_scene("ch2_s2_absent")
S3 = load_scene("ch2_s3_notin")
S5 = load_scene("ch2_s5_logic")
S6 = load_scene("ch2_s6_derive")
C3 = load_scene("ch3_s1_hook")

TX = (-4.6, 0.0, 4.6)
TY = (2.25, -1.35)          # tile content centres, rows 1 and 2
CAP_TOP = (0.9, -2.7)
TILE_W, TILE_H = 4.0, 2.2


def tile_center(i):
    return np.array([TX[i % 3], TY[i // 3], 0])


def fit(m, w=TILE_W, h=TILE_H):
    m.scale(min(w / m.width, h / m.height))
    return m


def caption(text, i):
    t = T(text, 28, DIM)
    t.move_to([TX[i % 3], CAP_TOP[i // 3] - t.height / 2, 0])
    return t


def query_card(code):
    res = T("Flow, Kaiva", 28, GREEN)
    inner = VGroup(code, res).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.15, width=inner.width + 0.6, height=inner.height + 0.5)
    box.set_stroke(BLUE, 2).set_fill(opacity=0)
    inner.move_to(box)
    return VGroup(box, inner)


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(7.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------ c2.recap.1
    def clip1(self):
        with self.say("c2.recap.1", gap=0.45) as c:
            # {absent}: three ways, big first
            lj = query_card(S2.leftjoin_query(28))
            ex = query_card(S2.except_query(28))
            ni_code = S3.notin_query()
            ni_code.scale(28 / 34)
            ni = query_card(ni_code)
            top = VGroup(lj, ex).arrange(RIGHT, buff=0.45, aligned_edge=UP)
            cards = VGroup(top, ni).arrange(DOWN, buff=0.35)
            fit(cards, 12.4, 5.0).move_to([0, 0.75, 0])
            cap1 = T("three ways to ask\nabout absence", 28, DIM)
            cap1.next_to(cards, DOWN, buff=0.3)
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=1.0)
            for card, cue in ((lj, "a left join"), (ex, "except"), (ni, "not in")):
                c.wait_until(cue)
                self.play(*appear(card, shift=None), run_time=min(0.9, c.until(floor=0.5)))

            # {column}: the absent cards settle into tile 1
            c.wait_until("column")
            k = min(TILE_W / cards.width, TILE_H / cards.height)
            cap1_t = caption("three ways to ask\nabout absence", 0)
            self.play(cards.animate.scale(k).move_to(tile_center(0)),
                      cap1.animate.move_to(cap1_t), run_time=1.2)
            col = S3.column_into_in()
            fit(col).move_to(tile_center(1))
            self.play(*appear(col.head, col.close, shift=None), run_time=0.8)
            c.wait_until("goes after")
            self.play(FadeIn(col.column, shift=1.0 * UP), run_time=1.2)
            cap2 = caption("a column goes after IN", 1)
            c.wait_until("membership")
            self.play(*appear(col.check, shift=None), *appear(cap2), run_time=0.8)

            # {logic}: rule card and AND grid, big in the lower half
            c.wait_until("logic")
            rule = S5.rule_card()
            rule.scale(5.4 / rule.width)
            andg = S5.truth_grids(complete=True).AND
            tn = andg.cell("T", "N")          # the one cell the recap works out again
            q = S5.truth_value("?", tn.value.size_hint).move_to(tn.box)
            q.size_hint = tn.value.size_hint
            tn.remove(tn.value)
            tn.add(q)
            tn.value = q
            tn.box.set_stroke(PINK)
            k0 = 3.5 / andg.width
            andg.scale(k0)
            hero = VGroup(rule, andg).arrange(RIGHT, buff=0.45)
            hero.move_to([-1.75, -1.95, 0])
            self.remove(hero)
            self.play(*appear(rule, shift=None), run_time=1.0)  # early: the rule card is shown whole, then read
            c.wait_until("combine")
            self.play(*appear(andg, shift=None), run_time=1.0)

            cell = andg.cell("T", "N")
            gs = [S5.ghost("T", "AND", "T", "T"), S5.ghost("T", "AND", "F", "F")]
            kg = 3.0 / max(g.width for g in gs)
            for g in gs:
                g.scale(kg)
            gx = andg.get_right()[0] + 0.45 + 1.5
            gs[0].move_to([gx, cell.get_y() + 0.4, 0])
            gs[1].move_to([gx, cell.get_y() - 0.4, 0])
            c.wait_until("try both")
            self.play(*fly(cell, gs[0]), run_time=1.0)
            self.play(*fly(cell, gs[1]), run_time=1.0)

            c.wait_until("agree")
            self.play(FlashAround(rule.lines[2], color=YELLOW, run_time=1.5, time_width=1.5))

            c.wait_until("otherwise")
            old = cell.value
            new = S5.truth_value("N", old.size_hint).scale(k0).move_to(cell.box)
            merge = [g.animate.scale(0.3).move_to(cell).set_opacity(0) for g in gs]
            self.play(*during(merge, 0, 0.45), *during(swap(old, new), 0.45, 1),
                      FlashAround(rule.lines[3], color=PINK, run_time=1.6, time_width=1.5),
                      run_time=1.6)
            for g in gs:
                self.remove(g)
            cell.remove(old)
            cell.add(new)
            cell.value = new
            self.remove(new)
            self.add(andg)

            # {where}: logic shrinks into tile 3 (via the empty lower right), gate in tile 4
            c.wait_until("where")
            P = hero.get_center()
            kh = min(TILE_W / hero.width, TILE_H / hero.height)
            parked = np.array([TX[2], TY[1], 0])
            self.play(*[m.animate.scale(kh, about_point=P).shift(parked - P) for m in (rule, andg)],
                      run_time=0.7)
            gate = S5.where_gate(2.0)
            toks = [S5.chip(v, 32) for v in "TFN"]
            toks[0].move_to([-0.35 - toks[0].width / 2, 0, 0])
            for prev, t in zip(toks, toks[1:]):
                t.next_to(prev, LEFT, buff=0.18)
            lo, hi = toks[2].get_left()[0], 1.3 + toks[0].width / 2
            kw = min(0.64, 4.2 / (hi - lo))
            mid = np.array([(lo + hi) / 2, 0.225, 0])
            for m in (gate, *toks):
                m.scale(kw, about_point=ORIGIN).shift(tile_center(3) - kw * mid)
            cap3 = caption("unknown: try both", 2)
            cap4 = caption("WHERE keeps\nonly TRUE", 3)
            up = tile_center(2) - parked
            self.play(*[m.animate.shift(up) for m in (rule, andg)],
                      *during(appear(cap3, shift=None), 0.5, 1),
                      *during(appear(gate, *toks, cap4, shift=None, lag=0.1), 0.3, 1), run_time=0.9)
            self.play(*S5.gate_pass(gate, toks[0], beyond=1.3 * kw, run_time=0.9))
            rest = c.until(floor=1.0)
            self.play(*S5.gate_bounce(gate, toks[1], RED, back=0.9 * kw, run_time=rest / 2))
            self.remove(toks[1])
            self.play(*S5.gate_bounce(gate, toks[2], PINK, back=0.9 * kw, run_time=c.until(floor=0.5)))
            self.remove(toks[2])

    # ------------------------------------------------------------ c2.recap.2
    def clip2(self):
        with self.say("c2.recap.2") as c:
            ch = S6.and_chain()
            ch.arrange(DOWN, buff=0.15)
            fit(ch, TILE_W, 2.0).move_to(tile_center(4))
            self.play(*appear(ch.true_part, ch.and_, ch.null_part, shift=None, lag=0.3), run_time=1.3)
            cap5 = caption("one NULL spoils\nNOT IN", 4)
            c.wait_until(own_word=cap5)
            self.play(Succession(FlashAround(ch.null_part, color=PINK, run_time=1.0, time_width=1.5),
                                 FlashAround(ch.null_part, color=PINK, run_time=1.0, time_width=1.5)),
                      *appear(cap5), run_time=2.0)

            c.wait_until("fix")
            line = S6.fixed_query().find("WHERE deathyear IS NOT NULL")
            line.scale(TILE_W / line.width)
            res = S6.final_results()
            res.scale(TILE_W / res.width)
            VGroup(line, res).arrange(DOWN, buff=0.3).move_to(tile_center(5))
            cap6 = caption("filter out the NULLs", 5)
            self.play(*appear(line, cap6, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("subquery")
            self.play(*appear(*res.cards, res.result, shift=None, lag=0.15), run_time=1.2)

    # ------------------------------------------------------------ c2.recap.3
    def clip3(self):
        with self.say("c2.recap.3", gap=0.0) as c:
            oc = C3.open_card(lit=False, exists=True)
            c.wait_until("really meant")
            sweep_clear(self, *appear(oc.kid, shift=None), run_time=1.4)
            c.wait_until("for this movie")
            self.play(*appear(oc.card, shift=None), GrowArrow(oc.arrow), run_time=1.2)
            c.wait_until(own_word=oc.question)
            self.play(*appear(oc.question),
                      LaggedStart(*[s.animate.set_fill(YELLOW, 0.85) for s in oc.lit], lag_ratio=0.12),
                      run_time=1.6)
            c.wait_until(own_word=oc.exists)
            self.play(*appear(oc.exists), run_time=1.0)
