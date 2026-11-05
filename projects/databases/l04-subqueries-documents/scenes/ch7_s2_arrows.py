"""Chapter 7, scene 2: the two arrows, -> (JSON) and ->> (text). Clips c7.arrows.1 – c7.arrows.4.

Exports (`load_scene("ch7_s2_arrows")`, static):
    recap_thumb() -> VGroup at ORIGIN: `->` -> TEAL "The Kid" (json), `->>` -> BLUE The Kid (varchar).

Layout: query on top, its result in the middle, The Kid's tree (a subset of s1's, size 26) as the
map along the bottom, so every value rises out of the tree into its cell without crossing the query.
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

J = load_scene("ch4_s2_json")
H = load_scene("ch7_s1_hook")
P = load_scene("ch7_s3_paths")

QUERY = """SELECT movie->'title' AS title_json,
       movie->>'title' AS title_text,
       movie->'genres' AS genres
FROM   movies
WHERE movie_id = 'tt0012349';"""

STEPS = ["movie", "movie->'actors'", "movie->'actors'->0", "movie->'actors'->0->>'name'"]
GENRES_JSON = '["Comedy","Drama","Family"]'
VS = 28            # result values / headers / type tags
MAP_TOP = -1.25
HEAD_Y, TYPE_Y, RULE_Y, VAL_Y = 0.45, 0.03, -0.25, -0.62


# ══ pieces ═════════════════════════════════════════════════════════════════════

def map_tree():
    """The Kid's map: title, genres (3), actors -> 0 -> name; nothing folded (a subset of s1's tree, at 28)."""
    kv = J.kid_value()
    v = {"title": kv["title"], "genres": kv["genres"],
         "actors": [{"name": kv["actors"][0]["name"]}]}
    t = J.json_tree(v, size=28, row_gap=0.46, label_pad=0.3, trunk_gap=0.15)
    for p, k in t.kinds.items():
        if k == "leaf":
            t.nodes[p].set_color(TEAL)
    t.orig = {}
    for p in t.paths:
        if t.kinds[p] in ("leaf", "more"):
            t.orig[p] = t.nodes[p].get_color()
        if p in t.labels:
            t.orig[("label",) + p] = t.labels[p].get_color()
    t.move_to([0, MAP_TOP - t.height / 2, 0])
    return t


def genres_cell():
    """`["Comedy","Drama","Family"]` as separate texts: brackets TEAL, items TEAL, commas DIM."""
    ref = Mono(GENRES_JSON, VS)
    spans = [("[", 0, 1, TEAL), ('"Comedy"', 1, 9, TEAL), (",", 9, 10, DIM), ('"Drama"', 10, 17, TEAL),
             (",", 17, 18, DIM), ('"Family"', 18, 26, TEAL), ("]", 26, 27, TEAL)]
    parts = []
    for s, a, b, col in spans:
        m = Mono(s, VS, col)
        m.move_to(VGroup(*ref[a:b]).get_center())
        parts.append(m)
    g = VGroup(*parts)
    g.items = [parts[1], parts[3], parts[5]]
    g.punct = [parts[0], parts[2], parts[4], parts[6]]
    return g


def result_columns():
    """Three columns: header, DuckDB type tag, value; left-aligned, laid out across the frame."""
    specs = [("title_json", "json", Mono('"The Kid"', VS, TEAL)),
             ("title_text", "varchar", Mono("The Kid", VS, BLUE)),
             ("genres", "json", genres_cell())]
    cols = []
    for h, ty, v in specs:
        cols.append((Mono(h, VS, FG, weight=BOLD), Mono(ty, VS, DIM), v))
    widths = [max(a.width, b.width, c.width) for a, b, c in cols]
    gap = 0.75
    x = -(sum(widths) + gap * (len(cols) - 1)) / 2
    for (h, ty, v), w in zip(cols, widths):
        for m, y in ((h, HEAD_Y), (ty, TYPE_Y), (v, VAL_Y)):
            m.move_to([x + m.width / 2, y, 0])
        x += w + gap
    left = cols[0][0].get_left()[0]
    right = x - gap
    rule = Line([left - 0.1, RULE_Y, 0], [right + 0.1, RULE_Y, 0]).set_stroke(DIM, 2)
    return cols, rule


def route(src, dst, via=(), same=True, k=VS / 28):
    """A copy of `src` travels through `via` to `dst` (never over other text). same=True: the
    copy turns into dst (same text; caller swaps in dst after the play). same=False: it fades
    just before dst fades in. Returns (anims, copy); call with run_time=1 scale via rate."""
    base = src.copy()
    cp = src.copy().set_opacity(0)
    pts = [src.get_center(), *[np.array([x, y, 0]) for x, y in via], dst.get_center()]
    path = VMobject().set_points_smoothly(pts) if len(pts) > 2 else Line(pts[0], pts[1])
    c0, c1 = ManimColor(src.get_color()), ManimColor(dst.get_color())
    end = 1.0 if same else 0.8
    s_l, s_r, s_b, s_t = src.get_left()[0], src.get_right()[0], src.get_bottom()[1], src.get_top()[1]

    def upd(m, a):
        t = smooth(min(1.0, a / end))
        m.become(base)
        m.scale(1 + (k - 1) * t)
        if same:
            m.set_color(interpolate_color(c0, c1, t))
        m.move_to(path.point_from_proportion(t))
        gx = max(m.get_left()[0] - s_r, s_l - m.get_right()[0])
        gy = max(m.get_bottom()[1] - s_t, s_b - m.get_top()[1])
        op = float(np.clip((max(gx, gy) - 0.6) / 0.5, 0, 1))      # invisible until it has left its source
        if not same:
            op *= float(np.clip((0.84 - a) / 0.12, 0, 1))
        m.set_opacity(op)

    return UpdateFromAlphaFunc(cp, upd, rate_func=linear), cp


def recap_thumb():
    """s8's thumbnail: `->` -> TEAL "The Kid" (json), `->>` -> BLUE The Kid (varchar)."""
    rows = []
    for op, val, col, ty in (("->", '"The Kid"', TEAL, "json"), ("->>", "The Kid", BLUE, "varchar")):
        o = Mono(op, 40, YELLOW)
        v = Mono(val, 40, col)
        t = Mono(ty, 28, col)
        rows.append((o, v, t))
    ox = 0.0
    for i, (o, v, t) in enumerate(rows):
        y = 0.6 - 1.2 * i
        o.move_to([ox - o.width / 2, y, 0])
    g = VGroup()
    for i, (o, v, t) in enumerate(rows):
        y = 0.6 - 1.2 * i
        a = Arrow([ox + 0.2, y, 0], [ox + 1.2, y, 0], buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.3).set_color(DIM)
        v.move_to([ox + 1.45 + v.width / 2, y, 0])
        t.next_to(v, RIGHT, buff=0.35).align_to(v, DOWN)
        g.add(o, a, v, t)
    return g.move_to(ORIGIN)


class Ch7S2Arrows(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── helpers ───────────────────────────────────────────────────────────────
    def light(self, glyphs, color=YELLOW):
        orig = [g.get_color() for g in glyphs]
        return recolor(glyphs, color), (lambda: [g.animate.set_color(c) for g, c in zip(glyphs, orig)])

    # ── c7.arrows.1: the query; -> and ->> ─────────────────────────────────────
    def clip1(self):
        shot = H.handover_shot()
        old = shot.tree
        self.add(shot)                                  # s1's last frame, exactly
        self.remove(shot)
        self.add(shot.table, shot.cell_box, shot.link, *old.submobjects, shot.tags)

        tree = map_tree()
        self.tree = tree
        moves, drop = [], [shot.table, shot.cell_box, shot.link, shot.tags]
        kept = []
        for p in old.paths:
            parts = [(old.nodes, tree.nodes), (old.edges, tree.edges), (old.labels, tree.labels)]
            for od, nd in parts:
                if p in od:
                    if p in nd:
                        moves.append(Transform(od[p], nd[p]))
                        kept.append(od[p])
                    else:
                        drop.append(od[p])

        with self.say("c7.arrows.1") as c:
            self.play(*during([FadeOut(m) for m in drop], 0, 0.4), *during(moves, 0.4, 1.0),
                      run_time=1.6)
            self.remove(*kept)
            self.add(tree)
            q = Code(QUERY, size=28).move_to([0, 2.2, 0])
            self.q = q
            self.play(*appear(q), run_time=1.0)
            c.wait_until("picks the movie")
            self.play(FlashUnder(q.line(4), color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until("three things")

            cols, rule = result_columns()
            self.cols, self.rule = cols, rule
            for _, ty, _ in cols:
                ty.set_opacity(0.45)
            heads = [m for h, ty, _ in cols for m in (h, ty)]
            self.play(*appear(*heads, lag=0.15), Create(rule), run_time=1.6)  # early: the result's column headers are code, shown whole before they're filled

            c.wait_until("single")
            a1 = q.find("->", line=0)
            on1, off1 = self.light(a1)
            self.play(*on1, run_time=0.8)
            c.wait_until("here title")
            v1 = cols[0][2]
            src = tree.node("title")
            anim, cp = route(src, v1, via=[(src.get_x() - 0.9, VAL_Y + 0.02)])
            self.play(anim, run_time=1.8)
            self.remove(cp)
            self.add(v1)

            c.wait_until("quoted")
            self.play(FlashAround(v1[0], color=TEAL, run_time=1.4, time_width=1.5),
                      FlashAround(v1[-1], color=TEAL, run_time=1.4, time_width=1.5))

            c.wait_until("double")
            a2 = q.find("->>", line=1)
            on2, self.off2 = self.light(a2)
            self.play(*off1(), *on2, run_time=0.8)
            c.wait_until("returns the kid", nth=0)
            v2 = cols[1][2]
            anim, cp = route(src, v2, same=False)
            self.play(anim, time_span(FadeIn(v2), 1.8 * 0.84, 1.8), run_time=1.8)
            self.remove(cp)

    # ── c7.arrows.2: the types; genres as a JSON array ─────────────────────────
    def clip2(self):
        cols, tree, q = self.cols, self.tree, self.q
        tys = [ty for _, ty, _ in cols]
        with self.say("c7.arrows.2") as c:
            c.wait_until("types")
            self.play(*[ty.animate.set_opacity(1).set_color(FG) for ty in tys], run_time=1.0)
            self.play(*flash(tys, color=FG, run_time=1.2, time_width=1.5))
            c.wait_until("json")
            self.play(*[tys[i].animate.set_color(TEAL) for i in (0, 2)], run_time=1.0)
            self.play(FlashAround(cols[0][2], color=TEAL, run_time=1.4, time_width=1.5))
            c.wait_until("text")
            self.play(tys[1].animate.set_color(BLUE), run_time=1.0)
            self.play(FlashAround(cols[1][2], color=BLUE, run_time=1.4, time_width=1.5))

            c.wait_until("genres")
            a3 = q.find("->", line=2)
            on3, self.off3 = self.light(a3)
            self.play(*self.off2(), *on3, run_time=0.8)
            cell = cols[2][2]
            anims, cps = [], []
            for i, item in enumerate(cell.items):
                s = tree.node("genres", i)
                tx = item.get_x()
                anim, cp = route(s, item, via=[(tx - 0.25, s.get_y() + 0.3)])
                anims.append(anim)
                cps.append(cp)
            self.play(*anims, run_time=1.8)
            self.remove(*cps)
            self.add(*cell.items)
            self.play(*appear(*cell.punct, shift=None, lag=0.1),
                      FlashAround(tree.node("genres"), color=TEAL, run_time=1.2, time_width=1.5),
                      run_time=1.0)

    # ── c7.arrows.3: chaining arrows down the tree ─────────────────────────────
    def clip3(self):
        cols, tree, q = self.cols, self.tree, self.q
        with self.say("c7.arrows.3") as c:
            # the two title columns move up into the query's place
            # the result moves up into the query's place
            moves = [m.animate.shift(1.6 * UP)
                     for m in [self.rule, *cols[0], *cols[1], *cols[2][:2], *cols[2][2].submobjects]]
            gone = [q]
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45), *during(moves, 0.4, 1.0),
                      run_time=min(1.8, c.until("deeper")))
            c.wait_until("deeper")
            self.play(FlashAround(VGroup(*cols[0]), color=TEAL, run_time=1.5, time_width=1.5),
                      *set_alpha([*cols[1], *cols[2][:2], *cols[2][2].submobjects], DIMMED))
            c.wait_until("go deeper")

            exprs = [Code(s, size=48) for s in STEPS]
            left = -exprs[-1].width / 2
            for e in exprs:
                e.move_to([left + e.width / 2, 2.4, 0])
            sweep_clear(self, *[time_span(FadeIn(m, shift=0.2 * UP), 0.6, 1.2)
                                for m in exprs[0]], *[time_span(a, 0.6, 1.2) for a in P.light_step(tree, (), flash=False)],
                        keep=[tree] + list(tree.submobjects))
            c.wait_until("chain")

            # -> 'actors'
            arr_t = Mono('[{…}, {…}, {…}, …]', 34, TEAL)
            arr_n = T("10 actors", 30, DIM)
            arr = VGroup(arr_t, arr_n).arrange(RIGHT, buff=0.4).move_to([0, 0.75, 0])
            self.play(*edit(exprs[0], exprs[1]), *P.light_step(tree, ("actors",)),
                      *during(appear(arr), 0.5, 1.0), run_time=1.5)
            c.wait_until("arrow zero")

            # -> 0
            obj_t = Mono('{"person_id":"nm0000122",\n "name":"Charles Chaplin",\n "roles":["A Tramp"]}',
                         28, TEAL, line_spacing=1.0)
            obj_b = RoundedRectangle(corner_radius=0.12, width=obj_t.width + 0.5,
                                     height=obj_t.height + 0.36).set_stroke(TEAL, 2.5).set_fill(TEAL, 0.08)
            obj = VGroup(obj_b, obj_t)
            obj.move_to([0, 0.75, 0])
            obj_b.move_to(obj_t)
            self.play(*edit(exprs[1], exprs[2]), *P.light_step(tree, ("actors", 0)),
                      *swap(arr, obj), run_time=1.3)
            c.wait_until("double arrow name")

            # ->> 'name'
            name = Mono("Charles Chaplin", 48, BLUE)
            ty = Mono("varchar", VS, BLUE)
            res = VGroup(name, ty).arrange(RIGHT, buff=0.4, aligned_edge=DOWN).move_to([0, 0.75, 0])
            self.play(*edit(exprs[2], exprs[3]), *P.light_step(tree, ("actors", 0, "name")),
                      *swap(obj, res), run_time=1.4)
            self.expr, self.res = exprs[3], res
            settle(self, tree)

            c.wait_until("steps")
            edges = [tree.edge("actors"), tree.edge("actors", 0), tree.edge("actors", 0, "name")]
            self.play(*[time_span(VShowPassingFlash(e.copy().set_stroke(YELLOW, 8), time_width=0.8),
                                  0.6 * i, 0.6 * i + 1.0) for i, e in enumerate(edges)],
                      run_time=2.2)
            chunks = [exprs[3].find("->'actors'"), exprs[3].find("->0"), exprs[3].find("->>'name'")]
            self.play(*[time_span(FlashUnder(g, color=YELLOW, time_width=1.5), 0.4 * i, 0.4 * i + 1.0)
                        for i, g in enumerate(chunks)], run_time=1.8)

            c.wait_until("print")
            self.play(FlashAround(name, color=BLUE, run_time=1.6, time_width=1.5))

    # ── c7.arrows.4: shorthand for two functions; not standard ─────────────────
    def clip4(self):
        tree = self.tree
        with self.say("c7.arrows.4") as c:
            rows = []
            for op, fn in (("->", "json_extract(movie, 'title')"),
                           ("->>", "json_extract_string(movie, 'title')")):
                rows.append((Mono(op, 40, YELLOW), MathTex("=", font_size=48), Code(fn, size=32)))
            x_eq = -4.0
            cards = []
            for i, (o, eq, f) in enumerate(rows):
                y = 2.9 - 1.35 * i
                eq.move_to([x_eq, y, 0])
                o.move_to([x_eq - 0.45 - o.width / 2, y, 0])
                f.move_to([x_eq + 0.45 + f.width / 2, y, 0])
            w = max(f.get_right()[0] for _, _, f in rows) - min(o.get_left()[0] for o, _, _ in rows) + 0.7
            cx = (max(f.get_right()[0] for _, _, f in rows) + min(o.get_left()[0] for o, _, _ in rows)) / 2
            for i, (o, eq, f) in enumerate(rows):
                b = RoundedRectangle(corner_radius=0.15, width=w, height=1.05).set_stroke(BLUE, 2.5)
                b.set_fill(BLUE, 0.06).move_to([cx, eq.get_y(), 0])
                cards.append(VGroup(b, o, eq, f))
            shift = -cx
            for cd in cards:
                cd.shift(shift * RIGHT)
            sweep_clear(self, *[time_span(FadeIn(cd, shift=0.25 * DOWN), 0.6 + 0.3 * i, 1.4 + 0.3 * i)
                                for i, cd in enumerate(cards)], keep=[tree], run_time=1.7)
            c.wait_until("standard")
            f1 = T("not standard SQL", 32, DIM).move_to([0, 0.6, 0])
            self.play(*appear(f1), run_time=1.0)
            c.wait_until("postgres")
            f2 = T("PostgreSQL uses the same operators", 32, DIM).next_to(f1, DOWN, buff=0.3)
            self.play(*appear(f2), run_time=1.0)
