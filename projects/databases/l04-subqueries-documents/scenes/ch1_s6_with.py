"""Chapter 1, scene 6: name it first: WITH (common table expressions). Clips c1.with.1 – c1.with.3.

Shared pieces (later scenes: `from lib.paths import load_scene; m = load_scene("ch1_s6_with")`):
- `with_code(size=28, comments=True)` -> slide 62's WITH query as Code at ORIGIN, `per_year` YELLOW,
  the WITH parentheses BLUE. comments=False drops the two comments (6 lines).
- `chained_code(size=25)` -> the chained WITH (per_year, busy), names YELLOW, at ORIGIN.
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
S5 = load_scene("ch1_s5_derived")

WITH_LINES = [
    "-- Define per_year as a name you can refer to later",
    "WITH per_year AS (",
    "    SELECT year, COUNT(*) AS n_movies",
    "    FROM movies GROUP BY year",
    ")",
    "SELECT year, n_movies FROM per_year -- Now use it",
    "WHERE n_movies > 140;",
]

CHAINED_LINES = [
    "WITH per_year AS (",
    "    SELECT year, COUNT(*) AS n_movies",
    "    FROM movies GROUP BY year",
    "),",
    "busy AS (",
    "    SELECT year FROM per_year WHERE n_movies > 140",
    ")",
    "SELECT COUNT(*) AS n_years FROM busy;",
]


def _color_names(code, lines, names):
    for i, l in enumerate(lines):
        if l.lstrip().startswith("--"):
            continue
        for nm in names:
            for k in range(l.count(nm)):
                code.find(nm, line=i, nth=k).set_color(YELLOW)


def with_code(size=28, comments=True):
    lines = list(WITH_LINES)
    if not comments:
        lines = lines[1:]
        lines[4] = "SELECT year, n_movies FROM per_year"
    code = Code("\n".join(lines), size=size)
    _color_names(code, lines, ["per_year"])
    o = 1 if comments else 0
    code.find("(", line=o).set_color(BLUE)
    code.find(")", line=o + 3).set_color(BLUE)
    return code.move_to(ORIGIN)


def chained_code(size=25):
    code = Code("\n".join(CHAINED_LINES), size=size)
    _color_names(code, CHAINED_LINES, ["per_year", "busy"])
    return code.move_to(ORIGIN)


def derived_thumb(size):
    """s5's derived_code() without its comment line (same text and colours)."""
    src = "\n".join(S5.derived_code().src.split("\n")[1:])
    code = Code(src, size=size)
    code.find("(", line=1).set_color(BLUE)
    code.find(")", line=2, nth=0).set_color(BLUE)
    code.find("AS per_year", line=2).set_color(YELLOW)
    return code


HAVING_WRAP = """SELECT year,
  COUNT(*) AS n_movies
FROM   movies
GROUP BY year
HAVING COUNT(*) > 140
ORDER BY year;"""


def wrapped_derived(size):
    """s5's derived query (no comment) re-wrapped into short lines; same tokens and colours."""
    code = Code("\n".join(["SELECT year, n_movies", "FROM (", "  SELECT year,", "    COUNT(*) AS n_movies",
                            "  FROM movies", "  GROUP BY year", ") AS per_year", "WHERE n_movies > 140;"]),
                size=size)
    code.find("(", line=1).set_color(BLUE)
    code.find(")", line=6).set_color(BLUE)
    code.find("AS per_year", line=6).set_color(YELLOW)
    return code


def wrapped_with(size):
    """with_code(comments=False) re-wrapped into short lines; same tokens and colours."""
    lines = ["WITH per_year AS (", "  SELECT year,", "    COUNT(*) AS n_movies", "  FROM movies",
             "  GROUP BY year", ")", "SELECT year, n_movies", "FROM per_year", "WHERE n_movies > 140;"]
    code = Code("\n".join(lines), size=size)
    _color_names(code, lines, ["per_year"])
    code.find("(", line=0).set_color(BLUE)
    code.find(")", line=5).set_color(BLUE)
    return code


NARROW_OPS = [r"\gamma_{\text{year}}", r"\sigma_{>140}", r"\gamma_{\text{count}}"]


def narrow_tower(width=2.6):
    """s1's tower() with narrower bricks, so it fits beside the chained WITH."""
    base = S1.table_card("movies")
    bricks = [S1.brick(tex, width=width) for tex in NARROW_OPS]
    icons = []
    y = base.box.get_top()[1]
    parts = [base]
    for b in bricks:
        icon = S1.table_icon().move_to([0, y + S1.GAP / 2, 0])
        b.move_to([0, y + S1.GAP + S1.BRICK_H / 2, 0])
        y = b.box.get_top()[1]
        icons.append(icon)
        parts += [icon, b]
    g = VGroup(*parts)
    g.base, g.bricks, g.icons = base, bricks, icons
    return g


def glyph_box(code, lines, color=BLUE, buff=0.14):
    probe = VGroup(*[g.copy() for i in lines for g in code.line(i)])
    return SurroundingRectangle(probe, buff=buff, corner_radius=0.08).set_stroke(color, 2.5).set_fill(color, 0.07)


def glyphs(code, lines):
    return [g for i in lines for g in code.line(i)]


class With(NarratedScene):
    def construct(self):
        shot = S5.handover_shot()
        self.add(shot)
        old = shot[0]

        # ---- c1.with.1: the inner query lifts to the top; define, use, read top to bottom
        with self.say("c1.with.1") as c:
            code = with_code()
            pairs = []
            for sub, lo, ln in (("SELECT year, COUNT(*) AS n_movies", 2, 2),
                                ("FROM movies GROUP BY year", 3, 3),
                                ("WHERE n_movies > 140;", 4, 6)):
                pairs += list(zip(old.find(sub, line=lo), code.find(sub, line=ln)))
            pairs += list(zip(old.find("per_year", line=3), code.find("per_year", line=5)))
            moved_old = {id(a) for a, _ in pairs}
            moved_new = {id(b) for _, b in pairs}
            outs = [g for g in old.text if id(g) not in moved_old]
            ins = [g.copy() for g in code.text if id(g) not in moved_new]
            k = 28 / 30
            moves = [a.animate.scale(k).move_to(b) for a, b in pairs]
            self.play(*during([FadeOut(g) for g in outs], 0, 0.35),
                      *during(moves, 0.25, 0.7),
                      *during([FadeIn(g) for g in ins], 0.65, 1.0), run_time=2.0)
            self.remove(shot, *shot.get_family(), *ins)
            self.add(code)

            c.wait_until("keyword")
            self.play(FlashUnder(code.find("WITH", line=1), color=BLUE, time_width=1.5), run_time=1.2)

            c.wait_until("define")
            box = glyph_box(code, range(1, 5))
            self.play(FadeIn(box), *set_alpha(glyphs(code, [5, 6]), 0.35), run_time=1.2)

            c.wait_until("use")
            per5 = code.find("per_year", line=5)
            per1 = code.find("per_year", line=1)
            self.play(Transform(box, glyph_box(code, [5, 6])),
                      *set_alpha(glyphs(code, [5, 6]), 1),
                      *set_alpha([g for g in glyphs(code, range(1, 5)) if g not in per1], 0.35),
                      run_time=1.4)
            # YELLOW link from FROM per_year back up to the definition, routed in the gaps
            xv = max(per5.get_center()[0], code.line(3).get_right()[0] + 0.25)
            xr = code.line(2).get_right()[0] + 0.35
            y3 = code.line(3).get_center()[1]
            y1 = per1.get_center()[1]
            p0 = [xv, per5.get_top()[1] + 0.08, 0]
            path = VMobject().set_points_as_corners([p0, [xv, y3, 0], [xr, y3, 0], [xr, y1, 0]])
            path.set_stroke(YELLOW, 3)
            tip = Arrow([xr, y1, 0], [code.line(1).get_right()[0] + 0.12, y1, 0], buff=0, stroke_width=3,
                        color=YELLOW, max_tip_length_to_length_ratio=0.12)
            c.wait_until("exactly")
            self.play(Create(path), FlashUnder(per5, color=YELLOW, time_width=1.5), run_time=1.0)
            self.play(GrowArrow(tip), FlashUnder(per1, color=YELLOW, time_width=1.5), run_time=0.8)

            c.wait_until("read")
            self.play(*disappear(box, path, tip),
                      *set_alpha([g for g in code.text], 0.3), run_time=0.6)
            xa = code.get_left()[0] - 0.35
            eye = Arrow([xa, code.line(0).get_top()[1] + 0.05, 0], [xa, code.line(6).get_bottom()[1] - 0.05, 0],
                        buff=0, stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.08)
            rt = 2.2
            lit = []
            for i in range(7):
                a0 = rt * i / 7.5
                lit += [time_span(an, a0, a0 + 0.5) for an in set_alpha(list(code.line(i)), 1)]
            self.play(GrowArrow(eye, rate_func=linear, run_time=rt), *lit, run_time=rt)

        # ---- c1.with.2: like a variable; several names; the tower
        with self.say("c1.with.2", gap=1.0) as c:
            self.play(*disappear(eye), code.animate.shift(1.6 * UP), run_time=1.4)

            sk_a = Mono("let per_year = ( … ) in", 40, DIM, t2c={"per_year": YELLOW})
            sk_b0 = Mono("…", 40, DIM)
            sk_b = Mono("… per_year … per_year …", 40, DIM, t2c={"per_year": YELLOW})
            sk_a.move_to([0, -1.5, 0])
            sk_b0.next_to(sk_a, DOWN, buff=0.9).align_to(sk_a, LEFT).shift(0.66 * RIGHT)
            sk_b.next_to(sk_a, DOWN, buff=0.9).align_to(sk_a, LEFT).shift(0.66 * RIGHT)
            sk_b0.align_to(sk_b, UP)
            c.wait_until("ocaml")
            self.play(*appear(sk_a, sk_b0, lag=0.3), run_time=1.2)

            c.wait_until("reuse")
            self.play(*swap(sk_b0, sk_b), run_time=1.2)
            defn = select(sk_a, "per_year")[0]
            uses = select(sk_b, "per_year")
            links = [Arrow(u.get_top() + 0.04 * UP, defn.get_bottom() + 0.04 * DOWN, buff=0.04,
                           stroke_width=3, color=YELLOW, max_tip_length_to_length_ratio=0.25) for u in uses]
            self.play(*[GrowArrow(a) for a in links], run_time=1.2)

            c.wait_until("several")
            chained = chained_code().move_to([6.5, 0.2, 0], aligned_edge=RIGHT)
            bare = with_code(comments=False)
            bare.align_to(code, LEFT).shift((code.line(1).get_y() - bare.line(0).get_y()) * UP)
            self.play(*disappear(sk_a, sk_b, *links), *edit(code, bare), run_time=1.0)
            # shared definition slides into place; the rest is rewritten around it
            pairs = [(a, b) for i in range(3) for a, b in zip(bare.line(i), chained.line(i))]
            outs = glyphs(bare, range(3, 6))
            ins = [g.copy() for g in glyphs(chained, range(3, 8))]
            k = 25 / 28
            self.play(*during([FadeOut(g) for g in outs], 0, 0.35),
                      *during([a.animate.scale(k).move_to(b) for a, b in pairs], 0.25, 0.7),
                      *during([FadeIn(g) for g in ins], 0.65, 1.0), run_time=2.0)
            self.remove(*bare.get_family(), *ins)
            self.add(chained)
            code = chained

            tw = narrow_tower()
            tw.scale(2.4 / tw.width).move_to([-5.25, -0.5, 0])
            bricks, icons = tw.bricks, tw.icons
            c.wait_until("tower")
            self.play(*appear(tw, shift=0.2 * UP), run_time=1.4)
            self.play(*set_alpha([*bricks, *icons], 0.35), run_time=0.8)

            blocks = [range(0, 4), range(4, 7), [7]]
            cbox = None
            for k, cue in enumerate(("pergroup", "busy", "final")):
                c.wait_until(cue)
                nb = glyph_box(code, blocks[k], color=YELLOW, buff=0.1)
                anims = [*set_alpha([bricks[k], icons[k]], 1), bricks[k].box.animate.set_stroke(YELLOW, 4)]
                if k > 0:
                    anims.append(bricks[k - 1].box.animate.set_stroke(BLUE, 3))
                if cbox is None:
                    cbox = nb
                    anims.append(FadeIn(cbox))
                else:
                    anims.append(Transform(cbox, nb))
                if k == 2:
                    three = Mono("3", 44, GOLD).next_to(bricks[2], UP, buff=0.3)
                    anims += during(appear(three, shift=0.2 * DOWN), 0.4, 1.0)
                self.play(*anims, run_time=1.4)

        # ---- c1.with.3: three ways, same rows, same plan
        with self.say("c1.with.3", gap=1.8) as c:
            # columns laid out as before (the old size-13 thumbnails only fix the column x's)
            slots = [S3.having_query(size=13), derived_thumb(13), with_code(size=13, comments=False)]
            heads = [T("HAVING clause", 30), T("derived table", 30), T("common table expression", 28)]
            tables = [S5.derived_result(size=30) for _ in range(3)]
            widths = [max(cd.width, tb.width, hd.width) for cd, tb, hd in zip(slots, tables, heads)]
            gap = 0.4
            x = -(sum(widths) + 2 * gap) / 2
            for cd, tb, hd, w in zip(slots, tables, heads, widths):
                cx = x + w / 2
                hd.move_to([cx, 3.25, 0])
                cd.move_to([cx, 0, 0]).align_to([0, 2.8, 0], UP)
                tb.move_to([cx, 0, 0]).align_to([0, 0.95, 0], UP)
                x += w + gap
            layout = VGroup(*slots, *heads, *tables)
            if layout.width > 12.4:
                layout.scale(12.4 / layout.width)
            layout.move_to([0, layout.get_y(), 0]).align_to([0, 3.5, 0], UP)
            # tables sit just above the plan strip; the re-wrapped queries fill the band above them
            plan_top = -2.95 + 0.31 + 0.2
            for tb in tables:
                tb.shift((plan_top + 0.52 - tb.get_bottom()[1]) * UP)
            codes = [Code(HAVING_WRAP, size=20), wrapped_derived(20), wrapped_with(20)]
            top = min(hd.get_bottom()[1] for hd in heads) - 0.14
            bottom = tables[0].get_top()[1] + 0.16
            pitch = slots[1].get_x() - slots[0].get_x()
            k = min((top - bottom) / max(cd.height for cd in codes),
                    (min(pitch, slots[2].get_x() - slots[1].get_x()) - 0.3) / max(cd.width for cd in codes), 1.0)
            for cd, sl in zip(codes, slots):
                cd.scale(k).move_to([sl.get_x(), 0, 0]).align_to([0, top, 0], UP)

            self.play(*during(disappear(*self.mobjects), 0, 0.45),
                      *during(appear(*codes, shift=None, lag=0.25), 0.5, 1.0), run_time=1.8)  # early: the three versions shown whole, then walked

            for k, cue in enumerate(("having", "derived", "cte")):
                c.wait_until(cue)
                hd = heads[k]
                self.play(*appear(hd, tables[k], lag=0.2), run_time=1.0)

            c.wait_until("results")
            self.play(*[FlashAround(tb, color=GREEN, time_width=1.5, buff=0.2) for tb in tables],
                      run_time=1.5)

            plan = S5.plan_diagram(width=3.8, size=28)
            xs = (-4.4, 0, 4.4)
            py = -2.95
            for i in range(3):
                plan.boxes[i].move_to([xs[i], py, 0])
                plan.labels[i].move_to(plan.boxes[i])
            harrows = [Arrow(plan.boxes[i].get_right(), plan.boxes[i + 1].get_left(), buff=0.06,
                             stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.4) for i in range(2)]
            strip = VGroup(*plan.boxes, *plan.labels, *harrows)
            frame = SurroundingRectangle(strip, buff=0.2, corner_radius=0.12).set_stroke(DIM, 2)
            downs = [Arrow([tb.get_x(), tb.get_bottom()[1] - 0.05, 0], [tb.get_x(), frame.get_top()[1], 0],
                           buff=0.04, stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.3)
                     for tb in tables]
            c.wait_until("duck")
            self.play(*appear(*[VGroup(b, l) for b, l in zip(plan.boxes, plan.labels)], shift=None, lag=0.2),  # early: the plan is shown whole
                      FadeIn(frame), *[GrowArrow(a) for a in harrows + downs], run_time=1.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
