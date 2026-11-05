"""Chapter 1, scene 8: recap, one callback per sentence filling a strip of four slots, ending on ch2's opening card. Clips c1.recap.1 – c1.recap.3.

Plan: four empty DIM slots along the top on {recap}. Each recap sentence shows its callback big in
the middle, in its original look, with its DIM line under it; when the next sentence starts, the
callback shrinks into its slot (the line fades) and the next one arrives:
r1 s1's tower beside s1's form, the count brick RED over the form -> s3's running order, WHERE and
HAVING lit; r2 s4's Venn, lens lit, 397 GOLD, then the lens doubled for UNION ALL; r3 s5's query,
the derived table glowing, then `WITH per_year AS (…)`; r4 s7's subquery collapsing into the 7.17 chip.
On {shape} ch2's open_card() parts arrive under the strip (the column DIM, a "?" as its label); on
{next} the column brightens, "a column" replaces the "?", IN arrives. The strip fades during the
end-card hold; the last frame is exactly load_scene("ch2_s1_hook").open_card().
Ends non-empty by design (chapter's last scene; reversed join onto ch2 s1). The thumbnails are
small text on purpose (recap strip).
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

S1 = load_scene("ch1_s1_hook")
S3 = load_scene("ch1_s3_form")
S4 = load_scene("ch1_s4_setops")
S5 = load_scene("ch1_s5_derived")
S7 = load_scene("ch1_s7_scalar")
S2N = load_scene("ch2_s1_hook")

SLOT_X = (-4.95, -1.65, 1.65, 4.95)
SLOT_Y = 2.85
SLOT_W, SLOT_H = 3.1, 1.3
HERO_Y = -0.45          # centre of the hero area (y -2.7 .. 1.8)
LINE_Y = -3.25
END_HOLD = 8.0


def line(text):
    return T(text, 32, DIM).move_to([0, LINE_Y, 0])


def with_snippet(size=30):
    code = Code("WITH per_year AS (…)", size=size)
    code.find("per_year").set_color(YELLOW)
    return code


def into_slot(mobs, i):
    """Animations shrinking the top-level mobs (as one picture) into slot i."""
    bb = VGroup(*[m.copy() for m in mobs])
    k = min((SLOT_W - 0.25) / bb.width, (SLOT_H - 0.2) / bb.height)
    ctr = bb.get_center()
    dst = np.array([SLOT_X[i], SLOT_Y, 0])
    # shrink in place first, then rise straight up into the slot (never sweeps over other slots)
    starts = [m.copy() for m in mobs]

    def make(m, s0):
        def upd(mob, a):
            a1 = smooth(min(1.0, a / 0.45))
            a2 = smooth(max(0.0, (a - 0.45) / 0.55))
            ax = min(1.0, 1.6 * a2)          # sideways first, so it clears the neighbouring slot
            d = dst - ctr
            mob.become(s0.copy().scale(1 + (k - 1) * a1, about_point=ctr)
                       .shift(np.array([ax * d[0], a2 * d[1], 0])))
        return UpdateFromAlphaFunc(m, upd)
    return [make(m, s0) for m, s0 in zip(mobs, starts)]


class Recap(NarratedScene):
    def construct(self):
        self.thumbs = []
        self.clip1()
        self.clip2()
        self.clip3()

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        with self.say("c1.recap.1") as c:
            self.slots = [RoundedRectangle(corner_radius=0.12, width=SLOT_W, height=SLOT_H)
                          .set_stroke(DIM, 1.5, opacity=0.6).move_to([x, SLOT_Y, 0]) for x in SLOT_X]
            self.play(*appear(*self.slots, shift=None, lag=0.2), run_time=min(1.2, c.until("r1")))

            # r1: the tower (two bricks, its output waiting on top) beside the form
            c.wait_until("r1")
            tw = S1.tower()
            tw.remove(tw.bricks[2])
            tw.scale(0.9)
            form = S1.select_form().scale(0.9)
            pair = VGroup(tw, form).arrange(RIGHT, buff=0.6).move_to([0, HERO_Y, 0])
            pair.remove(tw, form)
            self.play(*appear(tw, shift=None), run_time=1.2)

            c.wait_until("every query is a form")
            l1 = line("algebra stacks; SQL is a form")
            self.play(*appear(form, l1, shift=None, lag=0.3), run_time=1.3)

            c.wait_until("fixed boxes")
            gb = form.slots["GROUP BY"].box
            brick = S1.count_brick()
            brick.scale(gb.width / brick.box.width).move_to(gb)
            brick.box.set_stroke(RED, 4)
            self.play(FadeIn(brick, shift=0.3 * DOWN), run_time=min(1.0, c.until("that's why")))

            # running order: WHERE before GROUP BY, HAVING after
            c.wait_until("that's why")
            run = S3.run_column().scale(0.9).move_to(form)
            self.play(*swap(form, run), *during(disappear(brick), 0, 0.45), run_time=1.2)

            c.wait_until("where clause")
            w = run.stages["WHERE"]
            self.play(w.box.animate.set_stroke(YELLOW, 3), *recolor(w.kw, YELLOW),
                      FlashAround(w.box, color=YELLOW, time_width=1.5),
                      run_time=min(1.4, c.until("having clause")))
            c.wait_until("having clause")
            h = run.stages["HAVING"]
            self.play(h.box.animate.set_stroke(YELLOW, 3), *recolor(h.kw, YELLOW),
                      FlashAround(h.box, color=YELLOW, time_width=1.5),
                      run_time=min(1.4, c.until("r2")))

            # r2: r1 into its slot; the Venn, lens lit, 397 GOLD
            c.wait_until("r2")
            v = S4.venn()
            v.remove(v.crime_tag, v.drama_tag, v.crime_total, v.drama_total,
                     v.counts["crime_only"], v.counts["drama_only"])
            v.both.set_fill(BLUE, 0.45)
            v.move_to([-1.2, HERO_Y + 0.1, 0])
            l2 = line("set operations: side by side")
            self.play(*during(into_slot([tw, run], 0), 0, 0.55), *during(disappear(l1), 0, 0.4),
                      *during(appear(v, l2, shift=None, lag=0.2), 0.55, 1), run_time=1.6)
            self.thumbs.append([tw, run])

            c.wait_until("union all")
            lens = v.both.copy().set_fill(GOLD, 0.3).set_stroke(GOLD, 3)
            lens_n = v.counts["both"].copy()
            self.add(lens, lens_n)
            dx = 3.6 - v.both.get_center()[0]
            tag = Mono("UNION ALL", 32, BLUE).move_to([3.6, v.both.get_bottom()[1] - 0.5, 0])
            self.play(*S4.fill(v, ["crime_only", "both", "drama_only"]),
                      lens.animate.shift(dx * RIGHT), lens_n.animate.shift(dx * RIGHT),
                      *during(appear(tag), 0.6, 1), run_time=min(1.6, c.until()))
            self.cur = ([v, lens, lens_n, tag], l2)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        with self.say("c1.recap.2") as c:
            # r3: r2 into its slot; a query where a table goes
            dc = S5.derived_code().move_to([0, HERO_Y + 0.85, 0])
            l3 = line("a query where a table goes")
            mobs, old = self.cur
            self.play(*during(into_slot(mobs, 1), 0, 0.55), *during(disappear(old), 0, 0.4),
                      *during(appear(dc, l3, shift=None, lag=0.2), 0.55, 1), run_time=1.6)
            self.thumbs.append(mobs)

            c.wait_until("derived table")
            # one tight band per line, so the glow never covers `AS per_year`
            l2g = [*dc.find("(", line=2), *dc.find("SELECT year, COUNT(*) AS n_movies", line=2)]
            l3g = [*dc.find("FROM movies GROUP BY year", line=3), *dc.find(")", line=3)]
            bands = [SurroundingRectangle(VGroup(*[g.copy() for g in gl]), buff=0.07)
                     .set_stroke(width=0).set_fill(BLUE, 0.2).set_z_index(-1) for gl in (l2g, l3g)]
            self.play(*[FadeIn(b) for b in bands],
                      *[FlashAround(b, color=BLUE, time_width=1.5) for b in bands], run_time=1.5)
            glow = VGroup(*bands)
            settle(self, glow)

            c.wait_until("with clause")
            wc = with_snippet().move_to([0, dc.get_bottom()[1] - 0.75, 0])
            self.play(*appear(wc), run_time=min(1.0, c.until("read top to bottom")))
            c.wait_until("read top to bottom")
            self.play(FlashAround(wc.find("per_year"), color=YELLOW, time_width=1.5),
                      run_time=min(1.3, c.until("r4")))

            # r4: r3 into its slot; a query where a value goes
            c.wait_until("r4")
            pre = Code("rating >", size=30)
            sub = S7.subquery_code()
            row = VGroup(pre, sub).arrange(RIGHT, buff=0.25).move_to([0, HERO_Y, 0])
            row.remove(pre, sub)
            l4 = line("a query where a value goes")
            self.play(*during(into_slot([dc, glow, wc], 2), 0, 0.55), *during(disappear(l3), 0, 0.4),
                      *during(appear(pre, sub, l4, shift=None, lag=0.2), 0.55, 1),  # early: the panel's caption
                      run_time=1.6)
            self.thumbs.append([dc, glow, wc])

            c.wait_until("runs once")
            self.play(FlashAround(sub, color=GOLD, time_width=1.5), run_time=1.0)

            c.wait_until("collapses")
            chip = S7.avg_chip()
            chip.next_to(pre, RIGHT, buff=0.2)
            self.play(*during([sub.animate.scale(0.12).move_to(chip).set_opacity(0)], 0, 0.5),
                      *during([FadeIn(chip, scale=0.6)], 0.5, 1.0), run_time=1.3)
            self.remove(sub)

            c.wait_until("goes where a value goes")
            pair = VGroup(pre.copy(), chip.copy())
            ctr = pair.get_center()
            d = np.array([0, HERO_Y, 0]) - ctr
            self.play(pre.animate.scale(1.5, about_point=ctr).shift(d),
                      chip.animate.scale(1.5, about_point=ctr).shift(d),
                      run_time=min(1.2, c.until()))
            self.cur = ([pre, chip], l4)

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        card = S2N.open_card()
        col = card.column
        col.save_state()
        for i, cell in enumerate(col):
            cell.set_stroke(DIM, 3).set_fill(DIM, 0.25 if i == 0 else 0)
        q = T("?", 44, DIM).move_to(card.labels[2])

        with self.say("c1.recap.3") as c:
            # r4 into its slot; the three shapes arrive
            mobs, old = self.cur
            self.play(*during(into_slot(mobs, 3), 0, 0.45), *during(disappear(old), 0, 0.35),
                      *during(appear(card.grid, card.labels[0], card.tags[0],  # early: the end card, shown whole
                                     card.cell, card.labels[1], card.tags[1], col, q,
                                     shift=None, lag=0.12), 0.45, 1), run_time=min(2.4, c.until("next")))
            self.thumbs.append(mobs)

            c.wait_until("next")
            self.play(Restore(col), run_time=1.2)
            c.wait_until("whole column")
            self.play(*swap(q, card.labels[2]), run_time=1.2)
            c.wait_until("in operator")
            self.play(*appear(card.tags[2]), run_time=1.0)
            self.play(FlashAround(card.tags[2], color=BLUE, time_width=1.5), run_time=1.5)

        # end card: the recap strip fades, ch2's opening card stays
        self.wait(1.5)
        strip = [m for mobs in self.thumbs for m in mobs] + self.slots
        self.play(*[FadeOut(m) for m in strip], run_time=1.5)
        for m in list(self.mobjects):
            if m not in card.get_family():
                self.remove(m)
        settle(self, card)
        self.wait(END_HOLD - 3.0)
