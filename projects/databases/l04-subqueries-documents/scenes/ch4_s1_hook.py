"""Chapter 4, scene 1: hook, IMDb's page for The Kid built from seven tables. Clips c4.hook.1 – c4.hook.4.

Exports (static, no updaters):

    H = load_scene("ch4_s1_hook")
    card = H.open_card()     # ch4's first frame (ch3 s8 ends on it), STATUS.md Chapter 4 "Opening card":
                             #   .toolkit  ch3 s7's toolkit_card(), fitted into 6.2 x 4.6 at (-3.3, 0)
                             #   .doc      empty TEAL doc-card frame 3.4 x 4.4 at (3.9, 0)
                             #   .brace    TEAL Mono 64 "{" (doc left + 0.5, doc top - 0.6)
                             #   .label    "The Kid" T 32 FG at (3.9, 2.6)
    page = H.mock_page()     # the IMDb mock, 6.6 x 7.1, centred at ORIGIN:
                             #   .frame (DIM rounded rect) .poster (grey box)
                             #   .title "The Kid (1921)"  .genres "Comedy · Drama · Family"  .rating "★ 8.2"
                             #   .header = VGroup(title, genres, rating)
                             #   .director .writer (VGroup(.label DIM, .name FG)); .crew = VGroup(director, writer)
                             #   .cast_head "Cast"; .cast_rows[i] (VGroup(.actor, .role)), i = 0..3
                             #     (Chaplin / A Tramp, Coogan / The Child, Miller / The Man, Purviance / The Woman)
                             #   .more DIM "…"; .cast = VGroup(cast_head, *cast_rows, more); .rules (2 DIM lines)
                             #   .pieces = [header+poster, crew, cast] (the page's three flat parts)
    H.CAST                   # [(actor, role), ...] as on the page
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
from lib.titles import title_card  # noqa: E402

KIT = load_scene("ch3_s7_toolkit")
DOC = load_scene("ch4_s3_movie")
SCH = load_scene("ch1_s2_schema")


# ---------------------------------------------------------------- ch4's opening card
def open_card():
    tk = KIT.toolkit_card()
    tk.scale(min(6.2 / tk.width, 4.6 / tk.height)).move_to([-3.3, 0, 0])
    doc = DOC.doc_card(width=3.4, height=4.4).frame.move_to([3.9, 0, 0])
    brace = Mono("{", 64, TEAL)
    brace.move_to([doc.get_left()[0] + 0.5, doc.get_top()[1] - 0.6, 0])
    label = T("The Kid", 32, FG).move_to([3.9, 2.6, 0])
    g = VGroup(tk, doc, brace, label)
    g.toolkit, g.doc, g.brace, g.label = tk, doc, brace, label
    return g


# ---------------------------------------------------------------- the IMDb mock page
CAST = [("Charles Chaplin", "A Tramp"), ("Jackie Coogan", "The Child"),
        ("Carl Miller", "The Man"), ("Edna Purviance", "The Woman")]
PAGE_W, PAGE_H = 6.6, 7.1


def _left(mob, x, y):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def mock_page():
    L = -PAGE_W / 2
    frame = RoundedRectangle(corner_radius=0.15, width=PAGE_W, height=PAGE_H)
    frame.set_stroke(DIM, 2).set_fill(FG, 0.03)
    poster = Rectangle(width=1.2, height=1.7).set_stroke(DIM, 2).set_fill(DIM, 0.35)
    poster.move_to([L + 0.35, 3.25, 0], aligned_edge=UL)
    tx = L + 2.0
    title = _left(T("The Kid (1921)", 44), tx, 2.9)
    genres = _left(T("Comedy · Drama · Family", 28), tx, 2.3)
    rating = _left(T("★ 8.2", 32, GOLD), tx, 1.75)
    header = VGroup(title, genres, rating)
    rule1 = Line([L + 0.35, 1.25, 0], [-L - 0.35, 1.25, 0]).set_stroke(DIM, 1.5)

    def crew_row(lab, name, y):
        r = VGroup(_left(T(lab, 28, DIM), L + 0.35, y), _left(T(name, 30), L + 2.4, y))
        r.label, r.name = r[0], r[1]
        return r

    director = crew_row("Director", "Charles Chaplin", 0.8)
    writer = crew_row("Writer", "Charles Chaplin", 0.3)
    crew = VGroup(director, writer)
    rule2 = Line([L + 0.35, -0.15, 0], [-L - 0.35, -0.15, 0]).set_stroke(DIM, 1.5)
    cast_head = _left(T("Cast", 32, weight=BOLD), L + 0.35, -0.6)
    rows = []
    for i, (a, r) in enumerate(CAST):
        y = -1.15 - 0.47 * i
        row = VGroup(_left(T(a, 28), L + 0.35, y), _left(T(r, 28, slant=ITALIC), L + 3.6, y))
        row.actor, row.role = row[0], row[1]
        rows.append(row)
    more = _left(T("…", 30, DIM), L + 0.35, -3.0)
    cast = VGroup(cast_head, *rows, more)
    rules = VGroup(rule1, rule2)
    g = VGroup(frame, poster, header, rule1, crew, rule2, cast)
    g.frame, g.poster, g.title, g.genres, g.rating, g.header = frame, poster, title, genres, rating, header
    g.director, g.writer, g.crew = director, writer, crew
    g.cast_head, g.cast_rows, g.more, g.cast, g.rules = cast_head, rows, more, cast, rules
    g.pieces = [VGroup(poster, header), crew, cast]
    return g


# ---------------------------------------------------------------- wiring helpers
def wire(points, color=YELLOW):
    return VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in points]).set_stroke(color, 2.5)


LIT_COLS = {"movies": ["title", "year"], "ratings": ["rating"], "has_genre": ["genre_id"],
            "genres": ["name"], "has_position": ["position"], "people": ["name"], "plays_role": ["role"]}
PAGE_K, PAGE_X = 0.72, -4.6
MAP_K = 0.65


class Hook(NarratedScene):
    def construct(self):
        oc = open_card()
        self.add(oc.toolkit, oc.doc, oc.brace, oc.label)
        self.wait(0.7)
        tk = oc.toolkit

        # ---- clip 1: title; the toolkit card glows on its EXISTS rows, then slides off ----
        with self.say("c4.hook.1") as c:
            tc = title_card("Part 4 · A movie in one piece")
            tg = VGroup(tc.title, tc.rule, tc.course, tc.part)
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            tg.move_to([0, 3.45 - tg.height / 2, 0])
            tk_h = tg.get_bottom()[1] - 0.45 - (-3.5)
            tk_tgt = tk.copy()
            tk_tgt.scale(tk_h / tk.height).move_to([0, -3.5 + tk_h / 2, 0])
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4),
                        time_span(Transform(tk, tk_tgt), 0.3, 1.4),
                        keep=[tk], run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("card")
            box = KIT.row_box(tk, 7, 2)
            self.play(FadeIn(box), *recolor(list(tk.rows[7]) + list(tk.rows[8]), YELLOW),
                      run_time=min(1.2, c.until("completely")))
            self.play(FlashAround(VGroup(tk.rows[7], tk.rows[8]), run_time=1.5, time_width=1.5))
            c.wait_until("completely")
            self.play(VGroup(tk, box).animate.shift(9 * LEFT).set_opacity(0),
                      run_time=min(1.5, c.until(None)))
            self.remove(tk, box)

        # ---- clip 2: the page, part by part ----
        page = mock_page()
        with self.say("c4.hook.2", gap=0.8) as c:
            sweep_clear(self, time_span(FadeIn(page), 0.6, 1.6), run_time=1.6)  # early: the whole page first, then walked
            c.wait_until("header")
            self.play(*recolor(page.header, YELLOW), run_time=1.0)
            c.wait_until("crew")
            self.play(*recolor(page.header, FG), *recolor(page.header[2], GOLD),
                      *recolor([page.director.name, page.writer.name], YELLOW), run_time=1.0)
            c.wait_until("cast")
            self.play(*recolor([page.director.name, page.writer.name], FG),
                      *recolor([page.cast_head] + [r for row in page.cast_rows for r in row], YELLOW),
                      run_time=1.0)
            c.wait_until("build")
            m = SCH.schema_map()
            m.remove(m.count_group)
            m.scale(MAP_K)
            m.shift(RIGHT * (6.75 - m.get_right()[0]) + UP * (-0.15 - m.get_center()[1]))
            page.generate_target()
            page.target[6][:5].set_color(FG)        # cast head and rows back to FG as the page moves
            page.target.scale(PAGE_K).move_to([PAGE_X, 0, 0])
            self.play(*during([MoveToTarget(page)], 0, 0.6),
                      *during(appear(m.arrow_group, *m.card_group, shift=None, lag=0.08), 0.4, 1),
                      run_time=2.0)
            settle(self, m)

        # ---- clip 3: wire each page part to its tables; count tables ----
        cd = m.cards
        box_l = {n: cd[n].box.get_left()[0] for n in cd}
        y_top = min(cd[n].box.get_bottom()[1] for n in ("genres", "ratings", "people"))
        y_mid = max(cd[n].box.get_top()[1] for n in ("has_genre", "movies", "has_position"))
        lane_y = [y_mid + f * (y_top - y_mid) for f in (0.25, 0.5, 0.75)]
        page_r = page.frame.get_right()[0]
        gap_l = min(box_l["genres"], box_l["has_genre"])
        lane_x = [page_r + f * (gap_l - page_r) for f in (0.3, 0.5, 0.7)]
        x_left_col = (cd["has_genre"].box.get_right()[0] + box_l["movies"]) / 2
        x_right_col = (cd["movies"].box.get_right()[0] + box_l["has_position"]) / 2

        def row_y(n, col):
            return cd[n].rows[col].get_y()

        def start(part):
            return (part.get_right()[0] + 0.12, part.get_y())

        def ends(n):
            return (box_l[n], row_y(n, LIT_COLS[n][0]))

        sx, sy = start(page.title)
        w_movies = wire([(sx, sy), (lane_x[0], sy), (lane_x[0], lane_y[2]), (x_left_col, lane_y[2]),
                         (x_left_col, ends("movies")[1]), ends("movies")])
        sx, sy = start(page.rating)
        xr = box_l["ratings"] + 0.35
        w_ratings = wire([(sx, sy), (lane_x[1], sy), (lane_x[1], lane_y[1]), (xr, lane_y[1]),
                          (xr, cd["ratings"].box.get_bottom()[1])])
        sx, sy = start(page.genres)
        w_hg = wire([(sx, sy), (lane_x[2], sy), (lane_x[2], ends("has_genre")[1]), ends("has_genre")])
        w_gn = wire([(lane_x[2], sy), (lane_x[2], ends("genres")[1]), ends("genres")])
        cx_ = page.crew.get_right()[0] + 0.12
        cy_ = page.crew.get_y()
        w_hp = wire([(cx_, cy_), (lane_x[1], cy_), (lane_x[1], lane_y[0]), (x_right_col, lane_y[0]),
                     (x_right_col, ends("has_position")[1]), ends("has_position")])
        w_pp = wire([(x_right_col, lane_y[0]), (x_right_col, ends("people")[1]), ends("people")])
        rows_g = VGroup(*page.cast_rows)
        rx, ry = rows_g.get_right()[0] + 0.12, rows_g.get_y()
        w_pr = wire([(rx, ry), (lane_x[0], ry), (lane_x[0], ends("plays_role")[1]), ends("plays_role")])
        wires = []

        ctr_y = 3.1
        ctr_x = m.card_group.get_center()[0]
        lab = T("tables:", 40, GOLD)
        nums = [T(str(k), 40, GOLD) for k in range(1, 8)]
        lab.move_to([ctr_x - 0.25, ctr_y, 0])
        for nm in nums:
            nm.next_to(lab, RIGHT, buff=0.2).align_to(lab, DOWN)
        cur = [None]

        def step(names, w, parts, k, cue, first=False):
            anims = [Create(w)]
            for n in names:
                anims += m.light(n) + recolor([cd[n].rows[col] for col in LIT_COLS[n]], YELLOW)
            anims += recolor(parts, YELLOW)
            if wires:
                anims += [wires[-1].animate.set_stroke(opacity=0.45)]
            if first:
                anims += appear(lab, nums[k - 1])
            else:
                anims += swap(cur[0], nums[k - 1])
            cur[0] = nums[k - 1]
            rt = 1.4 if first else 1.1
            self.play(*anims, run_time=min(rt, c.until(cue)) if cue else rt)  # early: the GOLD tally counts the tables as they are named
            wires.append(w)

        with self.say("c4.hook.3") as c:
            step(["movies"], w_movies, [page.title], 1, "t_ratings", first=True)
            c.wait_until("t_ratings")
            step(["ratings"], w_ratings, [page.rating], 2, "t_genres")
            c.wait_until("t_genres")
            step(["has_genre"], w_hg, [page.genres], 3, "plus genres")
            c.wait_until("plus genres")
            step(["genres"], w_gn, [], 4, "t_crew")
            c.wait_until("t_crew")
            step(["has_position"], w_hp, [page.director.name, page.writer.name], 5, "plus people")
            c.wait_until("plus people")
            step(["people"], w_pp, [], 6, "t_roles")
            c.wait_until("t_roles")
            step(["plays_role"], w_pr, [r.role for r in page.cast_rows], 7, "seven")
            c.wait_until("seven")
            big = T("7 tables → 1 page", 56, GOLD).move_to([ctr_x, ctr_y, 0])
            self.play(*swap(VGroup(lab, cur[0]), big), run_time=1.2)

        # ---- clip 4: flat pieces, then the question ----
        with self.say("c4.hook.4", gap=2.5) as c:
            page.save_state()
            self.play(FlashAround(page.frame, color=TEAL, run_time=2, time_width=1.5))
            c.wait_until("the database has cut")
            centre = m.card_group.get_center()
            drift = [cd[n].animate.shift(0.12 * (cd[n].get_center() - centre)) for n in cd]
            self.play(*disappear(*wires, m.arrow_group), *drift,
                      page.frame.animate.set_stroke(opacity=0).set_fill(opacity=0),
                      page.pieces[0].animate.shift(0.3 * UP), page.pieces[2].animate.shift(0.3 * DOWN),
                      run_time=min(1.8, c.until("question")))
            c.wait_until("question")
            k = 0.8 / PAGE_K
            page.saved_state.scale(k).move_to([0, 0.35, 0])
            self.play(*during(disappear(m.card_group, big), 0, 0.5),
                      *during([Restore(page)], 0.3, 1), run_time=1.6)
            outline = (RoundedRectangle(corner_radius=0.2, width=page.width + 0.5, height=page.height + 0.5)
                       .set_stroke(TEAL, 3).set_fill(TEAL, 0.06).move_to(page))
            lb = Mono("{", 120, TEAL).next_to(outline, LEFT, buff=0.3)
            rb = Mono("}", 120, TEAL).next_to(outline, RIGHT, buff=0.3)
            q = T("in one piece?", 36, TEAL).next_to(outline, DOWN, buff=0.25)
            self.play(FadeIn(outline), *appear(lb, rb, q, shift=None, lag=0.3), run_time=1.4)  # early: the question asked on screen, then held

        self.play(*[FadeOut(mo) for mo in self.mobjects], run_time=1.0)
        self.wait(0.15)
