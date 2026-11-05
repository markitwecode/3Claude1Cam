"""Chapter 8, scene 3: grouping over documents (unnest rebuilds has_genre; GROUP BY; Mongo's $unwind).
Clips c8.group.1 – c8.group.4.

Exports (import with `G = load_scene("ch8_s3_group")`), all static VGroups, no updaters:

    G.genre_bars(size=32, max_len=4.0, pitch=0.75, header=True) -> VGroup centred at ORIGIN,
        about 7.3 wide, 3.9 tall (with header): the five results of slide 90's query.
        .rows[i]   VGroup(name, bar, count), i = 0..4 in result order (Drama .. Crime)
        .names[i]  T FG genre names, right-aligned on one column
        .bars[i]   BLUE Rectangle (fill 0.6), left edges aligned, length ∝ n (Drama = max_len)
        .counts[i] GOLD T "1,691" "878" "869" "719" "621", just right of each bar
        .head      VGroup(Mono DIM "genre" over the names, Mono DIM "n_movies" over the bars)
                   (empty VGroup with header=False)
        Grow a bar with GrowFromEdge(bars.bars[i], LEFT).
    G.recap_thumb() -> VGroup(.bars (genre_bars()), .card (ch1 s2's has_genre TableCard),
        .count (GOLD T 30 "7,826 rows" under the card)), bars left, card right, about 11.4 wide,
        centred at ORIGIN; scale it into a slot.
    G.kid_pairs(size=28) -> The Kid's three unnested rows as a table: columns `title | genre`,
        "The Kid" FG, genres BLUE (SQL strings), BLUE frame, DIM column rules, bold FG header
        (ch1 RowTable look). .frame .head .rows[i] .cell(i, j); top-left corner at ORIGIN.
    G.pair_table(cols, rows, colors, widths=None, size=28, pitch=0.5, pad=0.16, name=None)
        the builder behind it (widths: fix column widths so tables of different lengths line up).
    G.GENRES5, G.KID_PAIRS (data, verified on movies-json.duckdb / movies.duckdb).
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

SCH = load_scene("ch1_s2_schema")
VN = load_scene("ch1_s4_setops")
F5 = load_scene("ch5_s5_forms")
P7 = load_scene("ch7_s3_paths")

# ══ data (verified) ════════════════════════════════════════════════════════════
GENRES5 = [("Drama", "1,691", 1691), ("Comedy", "878", 878), ("Action", "869", 869),
           ("Adventure", "719", 719), ("Crime", "621", 621)]
KID_PAIRS = [["The Kid", "Comedy"], ["The Kid", "Drama"], ["The Kid", "Family"]]
PAIRS = KID_PAIRS + [["Metropolis", "Drama"], ["Metropolis", "Sci-Fi"]]
HG_ROWS = [["tt0012349", "5"], ["tt0012349", "8"], ["tt0012349", "11"],
           ["tt0017136", "8"], ["tt0017136", "22"]]

SQL = """SELECT   genre, COUNT(*) AS n_movies
FROM     movies, unnest(movie->>'$.genres[*]') AS t(genre)
GROUP BY genre
ORDER BY n_movies DESC, genre
LIMIT    5;"""

MONGO = """db.movies.aggregate([
  { $unwind: "$genres" },
  { $group: { _id: "$genres", n_movies: { $sum: 1 } } },
  { $sort: { n_movies: -1, _id: 1 } },
  { $limit: 5 }
])"""


# ══ exports ════════════════════════════════════════════════════════════════════
def genre_bars(size=32, max_len=4.0, pitch=0.75, header=True):
    names, bars, counts, rows = [], [], [], []
    for i, (g, s, n) in enumerate(GENRES5):
        y = -pitch * i
        name = T(g, size)
        name.move_to([0, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max_len * n / GENRES5[0][2], height=0.0095 * size * 1.9)
        bar.set_stroke(BLUE, 2).set_fill(BLUE, 0.6)
        bar.move_to([0.25, y, 0], aligned_edge=LEFT)
        cnt = T(s, size, GOLD)
        cnt.next_to(bar, RIGHT, buff=0.2)
        names.append(name)
        bars.append(bar)
        counts.append(cnt)
        rows.append(VGroup(name, bar, cnt))
    head = VGroup()
    if header:
        hg = Mono("genre", 28, DIM).move_to([0, pitch * 0.95, 0], aligned_edge=RIGHT)
        hn = Mono("n_movies", 28, DIM).move_to([counts[0].get_right()[0], pitch * 0.95, 0], aligned_edge=RIGHT)
        hn.align_to(hg, DOWN)
        head.add(hg, hn)
    g = VGroup(head, *rows)
    g.rows, g.names, g.bars, g.counts, g.head = rows, names, bars, counts, head
    return g.move_to(ORIGIN)


def recap_thumb():
    bars = genre_bars()
    card = SCH.schema_map().cards["has_genre"].copy()
    count = T("7,826 rows", 30, GOLD).next_to(card, DOWN, buff=0.3)
    side = VGroup(card, count)
    g = VGroup(bars, side).arrange(RIGHT, buff=1.0)
    g.bars, g.card, g.count = bars, card, count
    return g.move_to(ORIGIN)


def pair_table(cols, rows, colors, widths=None, size=28, pitch=0.5, pad=0.16, name=None):
    if widths is None:
        widths = [max([Mono(c, size, weight=BOLD).width] + [Mono(r[j], size).width for r in rows]) + 2 * pad
                  for j, c in enumerate(cols)]
    xs = [sum(widths[:j]) for j in range(len(cols))]
    W, H = sum(widths), pitch * (1 + len(rows))
    box = Rectangle(width=W, height=H).set_stroke(BLUE, 2).set_fill(BG, 0)
    box.move_to([W / 2, -H / 2, 0])
    hline = Line([0, -pitch, 0], [W, -pitch, 0]).set_stroke(BLUE, 2)
    vlines = [Line([x, 0, 0], [x, -H, 0]).set_stroke(DIM, 1.5) for x in xs[1:]]
    frame = VGroup(box, hline, *vlines)
    head = VGroup(*[SCH._placed(c, size, FG, BOLD, -pitch / 2, left=xs[j] + pad)[0]
                    for j, c in enumerate(cols)])
    cells = [[SCH._placed(v, size, colors[i][j], NORMAL, -pitch * (i + 1.5), left=xs[j] + pad)[0]
              for j, v in enumerate(r)] for i, r in enumerate(rows)]
    rws = [VGroup(*r) for r in cells]
    g = VGroup(frame, head, *rws)
    g.label = None
    if name:
        g.label = Mono(name, size + 2, BLUE, weight=BOLD)
        g.label.next_to([0, 0, 0], UP, buff=0.12).align_to(box, LEFT)
        g.add(g.label)
    g.frame, g.head, g.rows, g.widths = frame, head, rws, widths
    g.cell = lambda i, j: rws[i][j]
    return g


def _pairs(rows, widths=None, size=28):
    return pair_table(["title", "genre"], rows, [[FG, BLUE] for _ in rows], widths=widths, size=size)


def kid_pairs(size=28):
    widths = _pairs(PAIRS, size=size).widths
    return _pairs(KID_PAIRS, widths=widths, size=size)


def _dots(x, y):
    return VGroup(*[Dot([x, y + d, 0], radius=0.035, color=DIM) for d in (0.15, 0, -0.15)])


# ══ scene ══════════════════════════════════════════════════════════════════════
class Ch8S3Group(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        with self.say("c8.group.1") as c:
            q = Code(SQL, size=26)
            q.move_to([0, 0.4, 0])
            self.q = q
            self.play(*appear(q), run_time=1.2)   # early: the query is what the line is about
            c.wait_until("double")
            arrow_g = q.find("->>")
            orig = [g.get_color() for g in arrow_g]
            self.play(*recolor(arrow_g, YELLOW), FlashAround(arrow_g, run_time=1.4, time_width=1.5),
                      run_time=1.4)
            c.wait_until("plain string")
            tab = kid_pairs()
            tab.shift(np.array([-4.9, -0.2, 0]))
            lst = P7.list_box(["Comedy", "Drama", "Family"], size=28, per_line=(1, 1, 1))
            lst.move_to([2.2, tab.rows[1].get_y(), 0])
            for i, ln in enumerate(lst.lines):   # each item on its row's line, so it flies straight across
                ln.shift(UP * (tab.cell(i, 1).get_y() - lst.items[i].get_y()))
            body = VGroup(*lst.lines)
            lst.frame.stretch_to_fit_height(body.height + 0.32).move_to(body)
            lab = T("The Kid", 34).next_to(lst, UP, buff=0.3).align_to(lst, LEFT)
            self.play(*[g.animate.set_color(col) for g, col in zip(arrow_g, orig)],
                      q.animate.move_to([0, 3.5 - q.height / 2, 0]), run_time=1.0)
            self.play(*appear(lab, lst, lag=0.3), run_time=1.0)   # early: names the list
            c.wait_until("kid")
            arr = Arrow(lst.get_left() + 0.15 * LEFT, [tab.get_right()[0] + 0.15, lst.get_y(), 0], buff=0,
                        stroke_width=4, color=DIM, max_tip_length_to_length_ratio=0.3)
            self.play(GrowArrow(arr), *appear(tab.frame, tab.head, *[tab.cell(k, 0) for k in range(3)],
                                              shift=None), run_time=1.0)
            for k, word in enumerate(["comedy", "drama", "and family"]):
                c.wait_until(word)
                rt = 1.0 if k == 0 else min(0.8, max(0.6, c.until() - 0.1))
                opening = during(disappear(lst.frame, *lst.punct), 0, 0.35) if k == 0 else []
                self.play(*opening, *fly(lst.items[k], tab.cell(k, 1), arc=0), run_time=rt)
            self.lst, self.lab, self.arr, self.tab = lst, lab, arr, tab

    def clip2(self):
        q, tab = self.q, self.tab
        with self.say("c8.group.2") as c:
            full = _pairs(PAIRS, widths=tab.widths)
            TOP, LX = 1.35, -5.9
            full.shift(np.array([LX, TOP, 0]))
            v = full.get_corner(UL) - tab.frame[0].get_corner(UL)
            q.generate_target()
            q.target.scale(0.6).move_to([0, 3.65 - q.height * 0.6 / 2, 0]).set_opacity(0.4)
            self.play(*during(disappear(self.lst, self.lab, self.arr), 0, 0.4),
                      *during([tab.animate.shift(v)], 0.35, 1.0),
                      MoveToTarget(q), run_time=1.6)
            anchor = np.array([LX, TOP + 0.38, 0])
            vt = ValueTracker(3)
            counter = always_redraw(lambda: T(f"{int(round(vt.get_value())):,} rows", 32, GOLD)
                                    .move_to(anchor, aligned_edge=LEFT))
            self.play(Transform(tab.frame, full.frame), FadeIn(counter), run_time=1.0)
            extra = [full.rows[3], full.rows[4]]
            dl = _dots(full.get_center()[0], full.get_bottom()[1] - 0.32)
            self.play(*appear(*extra, dl, lag=0.25, shift=None),
                      vt.animate(rate_func=linear).set_value(7826),
                      run_time=max(1.0, min(2.6, c.until("hasgenre") - 0.3)))
            counter.clear_updaters()

            c.wait_until("hasgenre")
            card = SCH.schema_map().cards["has_genre"].copy()
            card.move_to([3.7, TOP - card.box.height / 2, 0], aligned_edge=ORIGIN)
            card.shift(UP * (TOP - card.box.get_top()[1]))
            self.play(FadeIn(card, shift=1.5 * LEFT), run_time=1.3)
            c.wait_until("seven thousand", nth=1)
            cnt_r = T("7,826 rows", 30, GOLD).next_to(card, DOWN, buff=0.3)
            self.play(*appear(cnt_r), run_time=1.0)   # early: read as "seven thousand ... again"

            c.wait_until("same")
            hg = pair_table(["movie_id", "genre_id"], HG_ROWS,
                            [[DIM, YELLOW] for _ in HG_ROWS], name="has_genre")
            hg.shift(np.array([5.9 - hg.frame[0].width, TOP, 0]))
            cnt_t = cnt_r.copy().move_to([0, TOP + 0.38, 0]).align_to(hg.frame[0], RIGHT)
            self.play(*swap(card, hg), cnt_r.animate.move_to(cnt_t), run_time=1.5)
            dashes = [DashedLine([full.get_right()[0] + 0.15, r.get_y(), 0],
                                 [hg.get_left()[0] - 0.15, r.get_y(), 0],
                                 dash_length=0.08).set_stroke(DIM, 2)
                      for r in [hg.rows[i] for i in range(5)]]
            hdots = _dots(hg.frame[0].get_center()[0], dl.get_y())
            cap = T("same 7,826 (movie, genre) pairs, names for IDs", 30, t2c={"7,826": GOLD})
            cap.move_to([0, -2.6, 0])
            self.play(*[Create(d) for d in dashes], *appear(hdots, shift=None), run_time=1.2)
            self.play(*appear(cap), run_time=1.0)

            c.wait_until("rebuilt")
            js = F5.genres_line(30).move_to([0, 3.15, 0])
            tag = T("first normal form, part 5", 28, DIM).move_to([0, 2.5, 0])
            self.play(*swap(q, js), run_time=1.3)
            self.play(*appear(tag), FlashAround(VGroup(*tab.rows), color=TEAL, time_width=1.5),
                      FlashAround(VGroup(*hg.rows[:3]), color=TEAL, time_width=1.5), run_time=1.5)
            self.full, self.extra, self.dl, self.js, self.tag = full, extra, dl, js, tag

    def clip3(self):
        q, tab = self.q, self.tab
        with self.say("c8.group.3") as c:
            bars = genre_bars().move_to([2.9, -0.2, 0])
            sweep_clear(self, *appear(bars.head, shift=None), keep=[tab, *self.extra, self.js, self.tag])
            # the rows drop into their genre bins (the bar slots, still empty)
            slot = lambda i: bars.bars[i].get_left() + 0.45 * RIGHT
            dr, co = tab.cell(1, 1), tab.cell(0, 1)
            self.play(*during([co.animate.move_to(slot(1)).set_opacity(0)], 0, 0.5),
                      *during([dr.animate.move_to(slot(0)).set_opacity(0)], 0.5, 1.0),
                      run_time=max(0.6, min(1.3, c.until("result") - 0.05)))

            c.wait_until("result")
            self.play(*during(disappear(tab, *self.extra, self.js, self.tag), 0, 0.5),
                      GrowFromEdge(bars.bars[0], LEFT), *appear(bars.names[0], bars.counts[0], shift=None),
                      run_time=1.4)
            for i, word in [(1, "comedy"), (2, "action"), (3, "adventure"), (4, "crime")]:
                c.wait_until(word)
                self.play(GrowFromEdge(bars.bars[i], LEFT), *appear(bars.names[i], bars.counts[i], shift=None),
                          run_time=min(1.0, max(0.5, c.until(word) + 0.9)))

            c.wait_until("venn")
            v = VN.venn()
            v.remove(v.counts["crime_only"], v.counts["both"], v.counts["drama_only"], v.crime_tag, v.drama_tag)
            v.scale(0.8).move_to([-3.9, bars.rows[2].get_y() + 0.1, 0])
            self.play(*appear(v, shift=None), run_time=1.2)
            c.wait_until("venn diagram")
            self.play(FlashAround(v.crime_total, time_width=1.5), FlashAround(bars.counts[4], time_width=1.5),
                      FlashAround(v.drama_total, time_width=1.5), FlashAround(bars.counts[0], time_width=1.5),
                      run_time=1.6)
            self.bars, self.venn = bars, v

    def clip4(self):
        q = self.q
        with self.say("c8.group.4") as c:
            q.set_opacity(1)
            q.scale((24 / 26) / 0.6).move_to([-5.5, 3.45, 0], aligned_edge=UL)
            sweep_clear(self, *appear(q, shift=None), run_time=1.6)

            c.wait_until("pipeline")
            code = Code(MONGO, size=24, lang="javascript")
            code.move_to([-5.5, 0.17, 0], aligned_edge=UL)
            frame = RoundedRectangle(corner_radius=0.15, width=12.9, height=code.height + 0.5)
            frame.set_stroke(DIM, 2).set_fill(BG, 0)
            frame.move_to([-6.6 + 6.45, code.get_center()[1], 0])
            lab = T("MongoDB", 32).next_to(frame, UP, buff=0.15).align_to(frame, LEFT).shift(0.15 * RIGHT)
            self.play(*appear(lab, frame, shift=None, lag=0.2), run_time=1.0)   # early: "Mongo D B" is spelled out
            self.play(*appear(code, shift=None), run_time=1.2)

            c.wait_until("steps")
            nums, ys = [], []
            for i in range(1, 5):
                y = code.find("{", line=i).get_center()[1]
                ys.append(y)
                nums.append(Mono(str(i), 26, YELLOW).move_to([-5.9, y, 0]))
            down = Arrow([-6.3, ys[0] + 0.22, 0], [-6.3, ys[3] - 0.22, 0], buff=0, stroke_width=4,
                         color=YELLOW, max_tip_length_to_length_ratio=0.15)
            bracket = Line([-6.3, q.get_top()[1] - 0.05, 0], [-6.3, q.get_bottom()[1] + 0.05, 0])
            bracket.set_stroke(BLUE, 5)
            self.play(*appear(*nums, lag=0.35, shift=None), GrowArrow(down), run_time=1.8)
            self.play(GrowFromCenter(bracket), run_time=1.0)

            c.wait_until("unwind")
            uw, un = code.find("$unwind"), q.find("unnest")
            self.play(*set_alpha([q, code, frame, lab, down, bracket, *nums], 0.3), run_time=1.0)
            box_uw = token_box(uw, code.line(1))
            self.play(*[g.animate.set_color(YELLOW).set_opacity(1) for g in uw], FadeIn(box_uw),
                      run_time=1.0)
            c.wait_until("dollar unwind")
            box_un = token_box(un, q.line(1))
            link_ = Line(box_un.get_bottom(), box_uw.get_top()).set_stroke(YELLOW, 3)
            self.play(*[g.animate.set_color(YELLOW).set_opacity(1) for g in un], FadeIn(box_un),
                      Create(link_), run_time=1.5)
