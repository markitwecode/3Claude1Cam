"""Chapter 1, scene 4: combining whole results with set operations. Clips c1.setops.1 – c1.setops.3.

Owns the running visual *the Venn of Crime and Drama* (reused by ch1 s8, L4 ch7 s6, ch8 s3).
Reuse it with `load_scene("ch1_s4_setops")`:

    mod = load_scene("ch1_s4_setops")
    v = mod.venn()        # static VGroup centred on the circles' midpoint at ORIGIN (no updaters);
                          #   about 5.3 wide, 4.4 tall (names above the circles reach y = +2.65)
    v.crime, v.drama      # the two BLUE circles (radius 1.6, centres at x = -0.85 / +0.85)
    v.crime_only, v.both, v.drama_only   # region shapes, BLUE fill at opacity 0 (fill them yourself)
    v.regions             # dict: "crime_only" "both" "drama_only" -> region shape
    v.crime_name, v.drama_name           # YELLOW T 40 "Crime" / "Drama"
    v.crime_tag, v.drama_tag             # DIM T 30 "genre 6" / "genre 8"
    v.crime_total, v.drama_total         # GOLD T 36 "621" / "1,691" beside the names
    v.counts              # dict of GOLD T 36: "crime_only" 224, "both" 397, "drama_only" 1,294,
                          #   "crime" 621, "drama" 1,691 (the last two are the totals)
    mod.fill(v, ["both"])  # -> list of anims: those regions filled (BLUE 0.45), the others cleared
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

R_VENN = 1.6
D_VENN = 0.85
FILL_OP = 0.45
REGION_KEYS = ["crime_only", "both", "drama_only"]


def venn():
    crime = Circle(radius=R_VENN).move_to(D_VENN * LEFT).set_stroke(BLUE, 4).set_fill(BG, 0)
    drama = Circle(radius=R_VENN).move_to(D_VENN * RIGHT).set_stroke(BLUE, 4).set_fill(BG, 0)
    both = Intersection(crime, drama)
    crime_only = Difference(crime, drama)
    drama_only = Difference(drama, crime)
    for r in (both, crime_only, drama_only):
        r.set_stroke(width=0).set_fill(BLUE, 0)

    def name_row(name, total, x):
        n = T(name, 40, YELLOW)
        t = T(total, 36, GOLD)
        row = VGroup(n, t).arrange(RIGHT, buff=0.22, aligned_edge=DOWN).move_to([x, 2.5, 0])
        return n, t

    crime_name, crime_total = name_row("Crime", "621", -1.6)
    drama_name, drama_total = name_row("Drama", "1,691", 1.6)
    crime_tag = T("genre 6", 30, DIM).next_to(crime_name, DOWN, buff=0.14, aligned_edge=LEFT)
    drama_tag = T("genre 8", 30, DIM).next_to(drama_name, DOWN, buff=0.14, aligned_edge=LEFT)

    n_crime_only = T("224", 36, GOLD).move_to([-1.6, -0.35, 0])
    n_both = T("397", 36, GOLD).move_to([0, 0.25, 0])
    n_drama_only = T("1,294", 36, GOLD).move_to([1.6, -0.35, 0])

    v = VGroup(crime_only, both, drama_only, crime, drama,
               crime_name, crime_total, crime_tag, drama_name, drama_total, drama_tag,
               n_crime_only, n_both, n_drama_only)
    v.crime, v.drama = crime, drama
    v.crime_only, v.both, v.drama_only = crime_only, both, drama_only
    v.regions = {"crime_only": crime_only, "both": both, "drama_only": drama_only}
    v.crime_name, v.drama_name = crime_name, drama_name
    v.crime_tag, v.drama_tag = crime_tag, drama_tag
    v.crime_total, v.drama_total = crime_total, drama_total
    v.counts = {"crime_only": n_crime_only, "both": n_both, "drama_only": n_drama_only,
                "crime": crime_total, "drama": drama_total}
    return v


def fill(v, keys, op=FILL_OP):
    anims = []
    for k in REGION_KEYS:
        r = v.regions[k]
        target = op if k in keys else 0
        if abs(r.get_fill_opacity() - target) > 1e-3:
            anims.append(r.animate.set_fill(BLUE, target))
    return anims


def result_line(n):
    return T(f"{n} rows", 40, t2c={n: GOLD})


CODE_SIZE = 30
TOP_SRC = "SELECT movie_id\nFROM has_genre\nWHERE genre_id = 6"
BOT_SRC = "SELECT movie_id\nFROM has_genre\nWHERE genre_id = 8;"


def narrow_form(s1, slot_w=2.4):
    """s1's SELECT form with shorter slots, so two fit side by side at full text size."""
    f = s1.select_form()
    for row in f:
        left = row.box.get_left()
        row.box.stretch_to_fit_width(slot_w).align_to(left, LEFT)
    return f


class SetOps(NarratedScene):
    def construct(self):
        s1 = load_scene("ch1_s1_hook")

        # ---- layout -------------------------------------------------------------
        v = venn().shift([-3.6, -0.1, 0])
        ref = Code(TOP_SRC + "\nINTERSECT\n" + BOT_SRC, size=CODE_SIZE)
        ref.move_to([0, 0.3, 0]).align_to([1.0, 0, 0], LEFT)
        top = Code(TOP_SRC, size=CODE_SIZE).align_to(ref, UP).align_to(ref, LEFT)
        bot = Code(BOT_SRC, size=CODE_SIZE).align_to(ref, DOWN).align_to(ref, LEFT)
        kw_y = ref.line(3).get_center()[1]

        def keyword(word):
            return Code(word, size=CODE_SIZE).move_to([0, kw_y, 0]).align_to(ref, LEFT)

        res_pos = np.array([ref.get_left()[0], -2.4, 0])

        def place_result(m):
            return m.move_to(res_pos).align_to(ref, LEFT)

        # ---- clip 1: Crime, Drama, INTERSECT / UNION / EXCEPT ----------------------
        with self.say("c1.setops.1") as c:
            self.add(v.crime_only, v.both, v.drama_only)
            self.play(GrowFromCenter(v.crime), GrowFromCenter(v.drama), run_time=1.5)
            c.wait_until("crime")

            self.play(*appear(top), run_time=1.0)
            c.wait_until(own_word=v.crime_name)
            self.play(*appear(v.crime_name, v.crime_tag, lag=0.3), run_time=1.0)
            c.wait_until("six hundred")
            self.play(*appear(v.crime_total), run_time=0.8)

            c.wait_until("drama")
            self.play(*appear(bot), run_time=1.0)
            c.wait_until(own_word=v.drama_name)
            self.play(*appear(v.drama_name, v.drama_tag, lag=0.3), run_time=1.0)
            c.wait_until("There are one thousand")
            self.play(*appear(v.drama_total), run_time=0.8)

            c.wait_until("intersect")
            kw = keyword("INTERSECT")
            self.play(*appear(kw), *fill(v, ["both"]), run_time=1.2)
            c.wait_until("three hundred")
            res = place_result(result_line("397"))
            self.play(*appear(v.counts["both"], res, lag=0.3), run_time=1.2)

            c.wait_until("union")
            kw2 = keyword("UNION")
            self.play(*swap(kw, kw2), *fill(v, REGION_KEYS), run_time=1.4)
            kw = kw2
            c.wait_until("nine hundred")
            res2 = place_result(result_line("1,915"))
            self.play(*appear(v.counts["crime_only"], v.counts["drama_only"], lag=0.3),
                      *swap(res, res2), run_time=1.4)
            res = res2

            c.wait_until("except")
            kw2 = keyword("EXCEPT")
            self.play(*swap(kw, kw2), *fill(v, ["crime_only"]), run_time=1.4)
            kw = kw2
            c.wait_until("two hundred")
            res2 = place_result(result_line("224"))
            self.play(*swap(res, res2), FlashAround(v.counts["crime_only"], time_width=1.5),
                      run_time=min(1.5, c.until()))
            res = res2
        settle(self, v)

        # ---- clip 2: same columns, sets vs multisets, UNION ALL -------------------
        with self.say("c1.setops.2") as c:
            ids = [top.find("movie_id"), bot.find("movie_id")]
            a = ids[0].get_right() + 0.15 * RIGHT
            b = ids[1].get_right() + 0.15 * RIGHT
            xr = ref.get_right()[0] + 0.3
            link_line = VMobject().set_points_as_corners(
                [a, [xr, a[1], 0], [xr, b[1], 0], b]).set_stroke(GREEN, 4)
            self.play(*recolor(ids[0], GREEN), *recolor(ids[1], GREEN), Create(link_line),
                      run_time=1.6)
            c.wait_until("sets")
            self.play(FlashAround(kw, time_width=1.5), run_time=1.5)
            c.wait_until("a set")
            tag = T("set", 30, DIM).next_to(res, DOWN, buff=0.18, aligned_edge=LEFT)
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("unionall")
            tag2 = T("multiset", 30, DIM).next_to(res, DOWN, buff=0.18, aligned_edge=LEFT)
            self.play(*swap(tag, tag2), run_time=1.2)
            tag = tag2

            c.wait_until("all version")
            kw2 = keyword("UNION ALL")
            self.play(*swap(kw, kw2), *fill(v, REGION_KEYS), run_time=1.5)
            kw = kw2
            c.wait_until("which keeps the duplicates")
            lens = v.both.copy().set_fill(GOLD, 0.3).set_stroke(GOLD, 3)
            lens_n = v.counts["both"].copy()
            self.add(lens, lens_n)
            dx = -0.1 - v.both.get_center()[0]
            self.play(lens.animate.shift(dx * RIGHT), lens_n.animate.shift(dx * RIGHT),
                      run_time=1.8)

            c.wait_until("union all returns")
            res2 = place_result(result_line("2,312"))
            self.play(*swap(res, res2), run_time=1.2)
            res = res2
            c.wait_until("exactly")
            total = T("621 + 1,691 = 2,312", 40, GOLD).move_to([v.get_center()[0], -2.55, 0])
            self.play(*appear(total), run_time=1.2)

            c.wait_until("twice")
            self.play(FlashAround(v.counts["both"], time_width=1.5),
                      FlashAround(lens_n, time_width=1.5), run_time=2.0)

        # ---- clip 3: algebra bricks vs SQL forms side by side ---------------------
        with self.say("c1.setops.3") as c:
            towers, glue = self.build_towers(s1)
            parts = [p for t in towers for p in t]
            sweep_clear(self, *during(appear(*parts, lag=0.1, shift=None), 0.55, 1), run_time=2.2)
            c.wait_until("one more brick")
            self.play(*appear(glue), run_time=1.2)

            c.wait_until("side")
            lf = narrow_form(s1).move_to([-3.4, 0.3, 0])
            rf = narrow_form(s1).move_to([3.4, 0.3, 0])
            sweep_clear(self, *during(appear(lf, rf, lag=0.3, shift=None), 0.55, 1), run_time=1.6)
            bar = RoundedRectangle(corner_radius=0.12, width=1.5, height=lf.height)
            bar.set_stroke(BLUE, 3).set_fill(BLUE, 0.15).move_to([0, lf.get_center()[1], 0])
            bar_kw = Mono("UNION", 28, BLUE).move_to(bar)
            c.wait_until("side by side")
            self.play(*appear(bar, bar_kw, shift=None), run_time=1.0)

            c.wait_until("notinput")
            icon = s1.table_icon(GOLD, 1.6).next_to(lf, DOWN, buff=0.35)
            start = icon.get_right() + 0.1 * RIGHT
            end = rf.slots["FROM"].box.get_right() + 0.05 * RIGHT
            lane_y = icon.get_center()[1]
            lane_x = rf.get_right()[0] + 0.5
            route = VMobject().set_points_as_corners(
                [start, [lane_x, lane_y, 0], [lane_x, end[1], 0]]).set_stroke(GOLD, 4)
            tip = Arrow([lane_x, end[1], 0], end, buff=0, color=GOLD, stroke_width=4,
                        max_tip_length_to_length_ratio=0.5)
            self.play(*appear(icon, shift=None), run_time=0.6)
            self.play(Succession(Create(route, run_time=1.1), GrowArrow(tip, run_time=0.4)),
                      run_time=1.5)
            c.wait_until("input")
            cross = cross_mark(RED).scale(1.4).move_to([(start[0] + lane_x) / 2, lane_y, 0])
            self.play(GrowFromCenter(cross), run_time=min(0.8, c.until()))

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def build_towers(self, s1):
        towers = []
        for g, x in ((6, -1.9), (8, 1.9)):
            card = s1.table_card("has_genre")
            card.label.scale_to_fit_width(2.2).move_to(card.box.get_top() + 0.3 * DOWN)
            card.move_to([x, -2.7 + card.height / 2, 0])
            sel = s1.brick(r"\sigma_{\text{genre\_id}=%d}" % g, width=3.2)
            proj = s1.brick(r"\pi_{\text{movie\_id}}", width=3.2)
            parts = [card]
            y = card.get_top()[1]
            for b in (sel, proj):
                icon = s1.table_icon().move_to([x, y + s1.GAP / 2, 0])
                b.move_to([x, y + s1.GAP + s1.BRICK_H / 2, 0])
                y = b.box.get_top()[1]
                parts += [icon, b]
            parts.append(s1.table_icon().move_to([x, y + s1.GAP / 2, 0]))
            towers.append(parts)
        top_y = towers[0][-1].get_center()[1] + s1.GAP / 2
        glue = s1.brick(r"\cap", width=7.0).move_to([0, top_y + s1.BRICK_H / 2, 0])
        return towers, glue
