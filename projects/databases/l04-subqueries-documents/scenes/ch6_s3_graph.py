"""Chapter 6, scene 3: many-to-many is not a tree. Clips c6.graph.1 – c6.graph.5.

Exports (import with `G3 = load_scene("ch6_s3_graph")`; all static, built at ORIGIN):

    G3.tangle() -> VGroup, L4's tangle = Lecture 5 ch1 s2's `tangle()` exactly: circles r 0.5,
        stroke 4, fill 0.2; Coogan (-2.4, 1.4), Chaplin (2.4, 1.4) PINK, names T 32 FG above;
        The Kid (-2.4, -1.4), The Gold Rush (2.4, -1.4) BLUE, names below; FG lines stroke 4 cut at
        the circle edges, order Coogan–Kid, Chaplin–Kid, Chaplin–Gold Rush. `.v["coogan"|"chaplin"|
        "kid"|"gold"]` (each `.circle`, `.label`), `.lines`, `.people`, `.movies`. ~7.7 x 4.8.
    G3.fetch_board() -> VGroup: The Kid's IDs-only card (`.card`: `.frame .head .rows .foot`, each
        row `.chip` DIM person_id + `.role`) on the right, ten people cards (`.people`) on the left,
        `.arrows` chip -> person card. ~13 x 7.
    G3.recap_thumb() -> VGroup for s7's {r2}: `.tangle` (small) left; `.copies` (s1's
        two_way_copies) above `.fetch` (fetch_board, the "1 + 10 fetches" arrows) right. No caption.
        ~8.3 x 4.5.
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

H = load_scene("ch6_s1_hook")
D = load_scene("ch4_s3_movie")


# ══ the tangle (geometry copied from L5 ch1_s2_lasttime.py) ════════════════════

R_VERT = 0.5
TANGLE_POS = {
    "coogan": np.array([-2.4, 1.4, 0]),
    "chaplin": np.array([2.4, 1.4, 0]),
    "kid": np.array([-2.4, -1.4, 0]),
    "gold": np.array([2.4, -1.4, 0]),
}
TANGLE_NAMES = {"coogan": "Jackie Coogan", "chaplin": "Charles Chaplin",
                "kid": "The Kid", "gold": "The Gold Rush"}
TANGLE_SIDES = {"coogan": UP, "chaplin": UP, "kid": DOWN, "gold": DOWN}


def vertex(name, pos, color, label_side=DOWN):
    c = Circle(radius=R_VERT).set_stroke(color, 4).set_fill(color, 0.2).move_to(pos)
    lab = T(name, 32, FG).next_to(c, label_side, buff=0.14)
    v = VGroup(c, lab)
    v.circle, v.label = c, lab
    return v


def _four(pos, sides):
    v = {}
    for key in ("coogan", "chaplin"):
        v[key] = vertex(TANGLE_NAMES[key], pos[key], PINK, sides[key])
    for key in ("kid", "gold"):
        v[key] = vertex(TANGLE_NAMES[key], pos[key], BLUE, sides[key])
    pairs = [("coogan", "kid"), ("chaplin", "kid"), ("chaplin", "gold")]
    lines = [Line(pos[a], pos[b], buff=R_VERT).set_stroke(FG, 4) for a, b in pairs]
    g = VGroup(*lines, v["coogan"], v["chaplin"], v["kid"], v["gold"])
    g.v, g.lines = v, lines
    g.people, g.movies = [v["chaplin"], v["coogan"]], [v["kid"], v["gold"]]
    return g


def tangle():
    return _four(TANGLE_POS, TANGLE_SIDES)


# ══ the growing graph ══════════════════════════════════════════════════════════

# Laid out (searched) so that lines cross each other but never run through a label.
GROWN_POS = {"coogan": np.array([-1.6, 1.8, 0]), "chaplin": np.array([1.0, 2.4, 0]),
             "kid": np.array([-1.0, -0.3, 0]), "gold": np.array([4.99, -1.44, 0])}
GROWN_SIDES = {**TANGLE_SIDES, "kid": DR}
CROSS_POS = {"goddard": ((1.75, -2.76), LEFT), "mann": ((1.5, -0.1), UL), "garcia": ((2.0, -1.2), DL),
             "downey": ((2.67, -3.3), LEFT)}
R_SMALL = 0.28
ACTOR_X = -3.4
ACTORS = ["Edna Purviance", "Carl Miller", "Albert Austin", "Beulah Bains",
          "Nellie Bly Baker", "Edward Biby", "B.F. Blinn", "Henry Bergman"]
MOVIES = [("City Lights", (3.75, 3.0)), ("Modern Times", (3.75, 1.8)),
          ("The Great\nDictator", (3.75, 0.6)), ("Chaplin\n(1992)", (3.54, -3.03))]


def small_vertex(name, pos, color, side, size=28):
    c = Circle(radius=R_SMALL).set_stroke(color, 3).set_fill(color, 0.2).move_to([pos[0], pos[1], 0])
    lab = set_backstroke(T(name, size, FG, line_spacing=0.8), width=5)
    lab.next_to(c, side, buff=0.12)
    v = VGroup(c, lab)
    v.circle, v.label = c, lab
    return v


def edge(a, b, width=3, color=FG):
    pa, pb = a.circle.get_center(), b.circle.get_center()
    ra, rb = a.circle.width / 2, b.circle.width / 2
    u = (pb - pa) / np.linalg.norm(pb - pa)
    return Line(pa + u * ra, pb - u * rb).set_stroke(color, width)


def grown():
    """Everything clip 2 draws, keyed. `.four` is the tangle in its new places."""
    g = VGroup()
    g.four = _four(GROWN_POS, GROWN_SIDES)
    fv = g.four.v
    ys = np.linspace(2.8, -2.8, 8)
    g.actors = [small_vertex(n, (ACTOR_X, y), PINK, LEFT) for n, y in zip(ACTORS, ys)]
    g.henry = g.actors[-1]
    g.kid_lines = [edge(fv["kid"], a) for a in g.actors]
    g.movies = [small_vertex(n, p, BLUE, RIGHT) for n, p in MOVIES]
    cl, mt, gd, c92 = g.movies
    g.c92 = c92
    g.chap_lines = [edge(fv["chaplin"], m) for m in g.movies]
    g.bergman_lines = [edge(g.henry, fv["gold"]), edge(g.henry, mt)]
    goddard = small_vertex("Paulette Goddard", CROSS_POS["goddard"][0], PINK, CROSS_POS["goddard"][1])
    mann = small_vertex("Hank\nMann", CROSS_POS["mann"][0], PINK, CROSS_POS["mann"][1])
    garcia = small_vertex("Al Ernest Garcia", CROSS_POS["garcia"][0], PINK, CROSS_POS["garcia"][1])
    g.cross = [goddard, mann, garcia]
    g.cross_lines = [edge(goddard, mt), edge(goddard, gd), edge(mann, cl), edge(mann, mt),
                     edge(garcia, cl), edge(garcia, mt)]
    g.downey = small_vertex("Robert Downey Jr.", CROSS_POS["downey"][0], PINK, CROSS_POS["downey"][1])
    g.downey_line = edge(g.downey, c92)
    dc = g.downey.circle.get_center()
    g.downey_more = []
    for ang in np.linspace(-125, -15, 20) * DEGREES:
        u = np.array([np.cos(ang), np.sin(ang), 0])
        g.downey_more.append(Line(dc + u * R_SMALL, dc + u * 3.2).set_stroke(FG, 2))
    g.labels = ([a.label for a in g.actors]
                + [m.label for m in g.movies] + [p.label for p in g.cross] + [g.downey.label])
    return g


def haze(scale, seed=4):
    """Many small vertices around the shrunken graph, each tied to its nearest neighbours."""
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < 240:
        p = np.array([rng.uniform(-6.9, 6.9), rng.uniform(-3.9, 3.9), 0])
        if abs(p[0]) < 1.9 * scale / 0.42 and abs(p[1]) < 1.5 * scale / 0.42:
            continue
        pts.append(p)
    anchors = [scale * np.array([x, y, 0]) for x, y in
               [(-3.4, 2.8), (-3.4, -2.8), (-3.4, 0.4), (4.0, 3.0), (4.0, -2.4), (1.0, 2.4), (4.0, 0.6)]]
    every = pts + anchors
    lines, dots = VGroup(), VGroup()
    for i, p in enumerate(pts):
        d = sorted(range(len(every)), key=lambda j: np.linalg.norm(every[j] - p))
        for j in d[1:3]:
            lines.add(Line(p, every[j]).set_stroke(FG, 1.5, opacity=0.4))
        col = BLUE if i % 7 == 0 else PINK
        dots.add(Dot(p, radius=0.06, color=col).set_fill(col, 0.85))
    return VGroup(lines, dots)


# ══ The Kid's IDs-only card and the fetch board ════════════════════════════════

CAST = [("nm0000122", "Charles Chaplin", "A Tramp"), ("nm0701012", "Edna Purviance", "The Woman"),
        ("nm0001067", "Jackie Coogan", "The Child"), ("nm0588033", "Carl Miller", "The Man"),
        ("nm0042317", "Albert Austin", "Car Thief +1"), ("nm0047800", "Beulah Bains", "Bride"),
        ("nm0048798", "Nellie Bly Baker", "Slum Nurse"),
        ("nm0074788", "Henry Bergman", "Professor Guido +1"),
        ("nm0080930", "Edward Biby", "Orphan Asylum Driver"), ("nm0088471", "B.F. Blinn", "His Assistant")]
ROW_PITCH = 0.44
CARD_S = 27


def ids_card():
    head = D.json_code('{ "movie_id": "tt0012349",\n  "title": "The Kid",\n  "actors": [', CARD_S)
    rows = VGroup()
    x0 = head.get_left()[0] + 0.5
    y0 = head.get_bottom()[1] - 0.36
    for i, (pid, _, role) in enumerate(CAST):
        txt = Mono(f'"{pid}"', 27, DIM)
        box = (RoundedRectangle(corner_radius=0.08, width=txt.width + 0.24, height=0.38)
               .set_stroke(DIM, 2).set_fill(DIM, 0.12))
        txt.move_to(box)
        chip = VGroup(box, txt)
        chip.move_to([x0, y0 - i * ROW_PITCH, 0], aligned_edge=LEFT)
        r = T(role, 28, FG, t2c={"+1": DIM}).next_to(chip, RIGHT, buff=0.25)
        r.set_y(chip.get_y())
        row = VGroup(chip, r)
        row.chip, row.role = chip, r
        rows.add(row)
    foot = D.json_code('  ]}', CARD_S)
    foot.next_to(rows, DOWN, buff=0.16).align_to(head, LEFT).shift(RIGHT * 0.45)
    body = VGroup(head, rows, foot)
    frame = D.fit_frame(body, size=CARD_S)
    card = VGroup(frame, head, rows, foot)
    card.frame, card.head, card.rows, card.foot = frame, head, rows, foot
    return card


def person_card(name):
    f = D.doc_card(None, width=3.1, height=0.5).frame
    t = T(name, 28, FG).move_to(f)
    g = VGroup(f, t)
    g.frame, g.name = f, t
    return g


def fetch_board():
    card = ids_card()
    card.move_to([6.5 - card.width / 2, 0, 0])
    people = VGroup(*[person_card(n) for _, n, _ in CAST])
    people.arrange(DOWN, buff=0.14).move_to([-5.0, 0, 0])
    card.move_to([6.55 - card.width / 2, 0, 0])
    arrows = VGroup(*[Arrow(row.chip.get_left(), p.get_right(), buff=0.08, stroke_width=3,
                            tip_length=0.16, color=FG)
                      for row, p in zip(card.rows, people)])
    g = VGroup(card, people, arrows)
    g.card, g.people, g.arrows = card, people, arrows
    return g


def recap_thumb():
    t = tangle().scale(0.45)
    cp = H.two_way_copies()
    cp.scale_to_fit_width(4.2)
    fb = fetch_board()
    # At thumbnail scale the names and roles are ~2 px specks whose neighbouring glyphs sit within
    # 0.01 of each other (read by the layout lint as stacked copies): draw them as plain outlines.
    for parent, attr in [(p, "name") for p in fb.people] + [(r, "role") for r in fb.card.rows]:
        t_ = getattr(parent, attr)
        flat = VGroup(*[VMobject().set_points(g.points).match_style(g) for g in t_.submobjects])
        parent.submobjects[parent.submobjects.index(t_)] = flat
        setattr(parent, attr, flat)
    fb.scale_to_fit_width(4.2)
    right = VGroup(cp, fb).arrange(DOWN, buff=0.35)
    g = VGroup(t, right).arrange(RIGHT, buff=0.6)
    g.move_to(ORIGIN)
    g.tangle, g.copies, g.fetch = t, cp, fb
    return g


# ══ code ═══════════════════════════════════════════════════════════════════════

APP_SRC = "\n".join([
    'movie = movies_by_id.get("tt0012349")  # 1 fetch',
    'for actor in movie["actors"]:          # 10 more',
    '    person = people_by_id.get(actor["person_id"])',
    '    print(person["name"], actor["roles"])'])
SLIDE_SRC = "\n".join([
    'results = []',
    'for movie in movies:                # scan the movies',
    '    rating = ratings_by_movie_id.get(movie["movie_id"])',
    '    if rating is not None:          # no rating, no row',
    '        results.append((movie["title"], rating))'])
OUTPUT = ["Charles Chaplin ['A Tramp']", "Edna Purviance ['The Woman']", "Jackie Coogan ['The Child']"]
CODE_S = 27

KID5_SRC = '{\n  "movie_id": "tt0012349",\n  "title": "The Kid",\n  "actors": [/* 10 IDs */]\n}'
CHAP5_SRC = ('{\n  "person_id": "nm0000122",\n  "name": "Charles Chaplin",\n  "birthyear": 1889,\n'
             '  "deathyear": 1977\n}')
N_MOVIES, GRID_COLS, GRID_ROWS = 2935, 60, 49
FOUND_IDX = [212, 801, 1377, 1904, 2560]


def movie_grid():
    x0, x1, y0, y1 = -0.2, 6.5, -0.9, 3.3
    px, py = (x1 - x0) / GRID_COLS, (y1 - y0) / GRID_ROWS
    cols, found = VGroup(), VGroup()
    for ci in range(GRID_COLS):
        col = VGroup()
        for ri in range(GRID_ROWS):
            idx = ci * GRID_ROWS + ri
            if idx >= N_MOVIES:
                break
            r = (Rectangle(width=px * 0.72, height=py * 0.74).set_stroke(width=0)
                 .set_fill(TEAL, 0.22).move_to([x0 + px * (ci + 0.5), y1 - py * (ri + 0.5), 0]))
            r.col = ci
            (found if idx in FOUND_IDX else col).add(r)
        cols.add(col)
    return cols, found


def box_at(center, w, h, color):
    return (RoundedRectangle(corner_radius=0.3, width=w, height=h).set_stroke(color, 4)
            .set_fill(color, 0.08).move_to(center))


class Ch6S3Graph(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── 1: try to make it a tree ────────────────────────────────────────────────
    def clip1(self):
        tg = tangle()
        v = tg.v
        self.tg = tg
        with self.say("c6.graph.1") as c:
            c.wait_until(own_word=v["chaplin"].label)
            self.play(*appear(v["chaplin"]), run_time=1.0)
            c.wait_until(own_word=v["coogan"].label)
            self.play(*appear(v["coogan"]), run_time=1.0)
            c.wait_until("The Kid")
            self.play(*appear(v["kid"]), Create(tg.lines[0]), Create(tg.lines[1]), run_time=1.0)
            c.wait_until("Gold Rush")
            self.play(*appear(v["gold"]), Create(tg.lines[2]), run_time=1.0)
            settle(self, tg)

            # nest: Chaplin inside The Kid, and again inside The Gold Rush
            c.wait_until("nest")
            self.play(*[ln.animate.set_stroke(opacity=0) for ln in tg.lines], run_time=1.0)
            tg.save_state()
            c.wait_until("Put Chaplin")
            v["chaplin"].set_z_index(2)
            v["kid"].set_z_index(2)
            kbox = box_at([-2.6, -1.2, 0], 3.8, 2.4, BLUE)
            self.play(Transform(v["kid"].circle, kbox),
                      v["kid"].label.animate.next_to(kbox, DOWN, buff=0.14),
                      v["chaplin"].animate.move_to(kbox.get_center() + DOWN * 0.05),
                      run_time=min(1.8, c.until("also go")))
            c.wait_until("also go")
            gbox = box_at([2.6, -1.2, 0], 3.8, 2.4, BLUE)
            ccopy = v["chaplin"].copy()
            ccopy.move_to(gbox.get_center() + DOWN * 0.05)
            ccopy[0].set_stroke(GOLD).set_fill(GOLD, 0.2)
            ccopy[1].set_color(GOLD)
            self.play(Transform(v["gold"].circle, gbox),
                      v["gold"].label.animate.next_to(gbox, DOWN, buff=0.14),
                      *during(fly(v["chaplin"], ccopy), 0.2, 1.0), run_time=min(1.6, c.until("flip")))

            # flip: The Kid inside Chaplin, and Coogan reaches for it too
            c.wait_until("flip")
            self.play(Restore(tg), *during([FadeOut(ccopy)], 0, 0.4), run_time=1.3)
            cbox = box_at([2.6, 1.0, 0], 3.8, 2.4, PINK)
            self.play(Transform(v["chaplin"].circle, cbox),
                      v["chaplin"].label.animate.next_to(cbox, UP, buff=0.14),
                      v["kid"].animate.move_to(cbox.get_center() + DOWN * 0.05),
                      *set_alpha([v["gold"]], DIMMED), run_time=1.6)
            c.wait_until("Jackie Coogan", nth=1)
            kc = v["kid"].circle
            cc = v["coogan"].circle
            u = kc.get_center() - cc.get_center()
            u = u / np.linalg.norm(u)
            reach = Line(cc.get_center() + u * R_VERT, kc.get_center() - u * R_VERT).set_stroke(RED, 5)
            self.play(Create(reach), run_time=1.2)
            tag = set_backstroke(T("two parents", 36, RED)).move_to([-0.6, 0.35, 0])
            c.wait_until("both")
            self.play(*appear(tag), run_time=1.0)  # early: the tag holds through the whole sentence

            # orphan
            c.wait_until("orphan")
            self.play(Transform(tg, tangle().shift(LEFT * 1.3)),
                      *during(disappear(reach, tag), 0, 0.4), run_time=1.5)
            lone = Circle(radius=R_VERT).set_stroke(PINK, 4).set_fill(PINK, 0.2).move_to([4.7, -0.2, 0])
            q = T("?", 72, RED).next_to(lone, UP, buff=0.2)
            c.wait_until("no movies")
            self.play(*appear(lone, q, lag=0.3), run_time=1.0)
            self.lone = VGroup(lone, q)

    # ── 2: the picture grows into a graph ───────────────────────────────────────
    def clip2(self):
        tg = self.tg
        g = grown()
        with self.say("c6.graph.2") as c:
            self.play(Transform(tg, g.four), *during(disappear(*self.lone), 0, 0.4),
                      run_time=min(1.6, c.until("other actors")))
            c.wait_until("other actors")
            self.play(*[Create(ln) for ln in g.kid_lines], *appear(*g.actors, lag=0.1),  # early: the cast fans out as a group
                      run_time=1.6)
            c.wait_until("other movies")
            self.play(*[Create(ln) for ln in g.chap_lines], *appear(*g.movies, lag=0.15, shift=None),  # early: Chaplin's movies join as a group
                      run_time=1.6)

            # cross
            c.wait_until("cross")
            self.play(FlashAround(g.henry.label, run_time=1.2, time_width=1.5),
                      g.henry.label.animate.set_color(YELLOW), run_time=1.2)
            c.wait_until("Gold Rush")
            for ln in g.bergman_lines:
                ln.set_stroke(YELLOW, 4)
            self.play(*[Create(ln) for ln in g.bergman_lines], run_time=1.5)
            c.wait_until("start to cross")
            self.play(*[Create(ln) for ln in g.cross_lines], *appear(*g.cross, lag=0.3),  # early: the other cross-linked actors
                      *[ln.animate.set_stroke(FG, 3) for ln in g.bergman_lines],
                      g.henry.label.animate.set_color(FG), run_time=1.8)

            # downey
            c.wait_until("downey")
            self.play(*flash([g.c92.label]), g.c92.circle.animate.set_stroke(YELLOW), run_time=1.2)
            c.wait_until(own_word=g.downey.label)
            self.play(*appear(g.downey, shift=None), Create(g.downey_line), g.c92.circle.animate.set_stroke(BLUE),
                      run_time=1.2)
            c.wait_until("twenty more")
            self.play(*[time_span(Create(ln), 0.05 * i, 0.05 * i + 0.6) for i, ln in enumerate(g.downey_more)],
                      run_time=1.6)

            gg = VGroup(tg, *g.kid_lines, *g.chap_lines, *g.bergman_lines, *g.cross_lines, g.downey_line,
                        *g.downey_more, *g.actors, *g.movies, *g.cross, g.downey)
            settle(self, gg)

            # reach: pull back into a haze
            c.wait_until("reach")
            labels = [v.label for v in tg.v.values()] + g.labels
            self.play(*[lab.animate.set_opacity(0) for lab in labels], run_time=0.8)
            self.play(gg.animate.scale(0.42, about_point=ORIGIN), run_time=1.6)
            hz = haze(0.42)
            k = ValueTracker(0)
            cpos = np.array([0, -3.25, 0])

            def counter():
                t = T(f"{int(k.get_value()):,} of 2,935 movies", 44, GOLD).move_to(cpos)
                return VGroup(BackgroundRectangle(t, color=BG, fill_opacity=0.9, buff=0.15), t)

            cnt = always_redraw(counter)
            self.add(cnt)
            self.play(FadeIn(hz[0], lag_ratio=0.002), FadeIn(hz[1], lag_ratio=0.004),
                      k.animate(rate_func=linear).set_value(2902),
                      run_time=max(1.5, min(3.5, c.until("graph") - 0.5)))
            cnt.clear_updaters()
            gg.add(hz)
            settle(self, gg)
            self.gg, self.cnt = gg, cnt

            c.wait_until("graph")
            cap_t = T("not a tree but a graph", 52, YELLOW).move_to([0, 3.2, 0])
            cap = VGroup(BackgroundRectangle(cap_t, color=BG, fill_opacity=0.9, buff=0.18), cap_t)
            self.play(*appear(cap), run_time=1.0)
            self.cap = cap

    # ── 3: two ways out ─────────────────────────────────────────────────────────
    def clip3(self):
        gg = self.gg
        with self.say("c6.graph.3", gap=1.4) as c:
            panel = (RoundedRectangle(corner_radius=0.25, width=8.7, height=7.0)
                     .set_stroke(TEAL, 2).set_fill(TEAL, 0.05).move_to([2.25, 0, 0]))
            self.play(*during(disappear(self.cnt), 0, 0.4),
                      *during([gg.animate.scale(0.28).move_to([-4.65, 0, 0])], 0.2, 1.0), run_time=1.6)
            self.play(FadeIn(panel), run_time=1.0)

            cp = H.two_way_copies()
            cp.move_to([0, -0.9, 0])
            panel2 = (RoundedRectangle(corner_radius=0.25, width=13.0, height=5.4)
                      .set_stroke(TEAL, 2).set_fill(TEAL, 0.05).move_to([0, -0.9, 0]))
            c.wait_until("twice")
            self.play(*during(disappear(self.cap), 0, 0.4),
                      gg.animate.scale(0.72).move_to([-5.0, 2.6, 0]), FadeOut(panel), run_time=1.5)
            c.wait_until("in the movie")
            self.play(*appear(cp.kid), run_time=1.0)
            c.wait_until("in the person")
            self.play(*appear(cp.chap), *[GrowArrow(a) for a in cp.arrows], run_time=1.2)
            c.wait_until("copied names")
            self.play(*flash([cp.name_k, cp.title_c, cp.year_c], color=GOLD), run_time=1.5)

            tag = T("every copy kept in step", 36, RED).move_to([2.6, 2.6, 0])
            c.wait_until("cost")
            self.play(*appear(tag), run_time=1.0)  # early: the cost is named as the sentence about it starts

            # ids: the IDs-only card
            c.wait_until("ids")
            fb = fetch_board()
            sweep_clear(self, *during(appear(fb.card), 0.5, 1.0), run_time=1.6)
            c.wait_until("fetch")
            n = len(fb.arrows)
            anims = []
            for i, (a, p) in enumerate(zip(fb.arrows, fb.people)):
                anims.append(time_span(GrowArrow(a), 0.22 * i, 0.22 * i + 0.8))
                anims.append(time_span(FadeIn(p, shift=0.15 * LEFT), 0.22 * i + 0.5, 0.22 * i + 1.1))
            self.play(*anims, run_time=0.22 * (n - 1) + 1.1)
            jl = T("a join", 40, YELLOW).move_to([-2.4, 3.3, 0])
            c.wait_until(own_word=jl)
            self.play(*appear(jl), run_time=1.0)

    # ── 4: the application's join ───────────────────────────────────────────────
    def clip4(self):
        app = Code(APP_SRC, size=CODE_S, lang="python")
        slide = Code(SLIDE_SRC, size=CODE_S, lang="python")
        ag = app.find(".get", line=2)
        sg = slide.find(".get", line=2)
        app.move_to(ORIGIN)
        slide.move_to(ORIGIN)
        slide.shift(RIGHT * (ag.get_left()[0] - sg.get_left()[0]))
        pair_l = min(app.get_left()[0], slide.get_left()[0])
        pair_r = max(app.get_right()[0], slide.get_right()[0])
        dx = -(pair_l + pair_r) / 2
        app.shift(RIGHT * dx)
        slide.shift(RIGHT * dx)
        app.shift(UP * (3.5 - app.get_top()[1]))
        slide.shift(UP * (0.5 - slide.get_top()[1]))

        outs = VGroup(*[Mono(s, CODE_S) for s in OUTPUT])
        outs.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        more = T("… 7 more", 30, DIM)
        more.next_to(outs, DOWN, buff=0.2, aligned_edge=LEFT)
        VGroup(outs, more).next_to(app, DOWN, buff=0.45).align_to(app, LEFT)

        k = ValueTracker(0)
        cpos = np.array([4.2, 0.0, 0])

        def counter():
            n = int(round(k.get_value()))
            return T("1 fetch" if n == 0 else f"1 + {n} fetches", 40, GOLD).move_to(cpos)

        with self.say("c6.graph.4", gap=1.2) as c:
            sweep_clear(self, *during(appear(app), 0.5, 1.0), run_time=1.6)
            c.wait_until("fetches the movie")
            box = token_box(app.find('.get("tt0012349")', line=0), app.line(0))
            cnt = always_redraw(counter)
            self.play(FadeIn(box), FadeIn(cnt), run_time=1.0)
            c.wait_until("then each actor")
            self.play(Transform(box, token_box(app.find('.get(actor["person_id"])', line=2), app.line(2))),
                      run_time=0.8)
            self.play(k.animate(rate_func=linear).set_value(3),
                      *[time_span(FadeIn(o), 0.67 * i + 0.1, 0.67 * i + 0.6) for i, o in enumerate(outs)],
                      run_time=2.1)
            self.play(k.animate(rate_func=linear).set_value(10), FadeIn(more), run_time=1.2)
            cnt.clear_updaters()
            c.wait_until("eleven")
            self.play(FlashAround(cnt, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("slide")
            cnt2 = cnt.copy().move_to([6.3 - cnt.width / 2, 0.95, 0])
            self.play(*during(disappear(outs, more), 0, 0.4),
                      *during([cnt.animate.move_to(cnt2)], 0.15, 0.6),
                      *during(appear(slide, shift=None), 0.55, 1.0), run_time=1.8)
            box2 = token_box(slide.find('.get(movie["movie_id"])', line=2), slide.line(2))
            self.play(FadeIn(box2), *flash([box, box2]), run_time=1.5)

            lab_app = T("your code", 32, FG).move_to([0, 0.95, 0]).align_to(app, LEFT)
            lab_db = T("the database", 32, FG).next_to(slide, DOWN, buff=0.3).align_to(slide, LEFT)
            self.play(*appear(lab_db), run_time=1.0)  # early: names slide 48's loop as the voice describes it
            c.wait_until("your code")
            self.play(*appear(lab_app), run_time=1.0)

    # ── 5: both directions; the way out; next lecture ──────────────────────────
    def clip5(self):
        kid = D.doc_card(KID5_SRC, size=22)
        chap = D.doc_card(CHAP5_SRC, size=22)
        kid.move_to([-6.5 + kid.width / 2, 0.3, 0])
        chap.move_to([6.5 - chap.width / 2, 0.3, 0])
        xa, xb = kid.get_right()[0] + 0.1, chap.get_left()[0] - 0.1
        a_cast = Arrow([xa, 0.75, 0], [xb, 0.75, 0], buff=0, stroke_width=4, color=FG, tip_length=0.22)
        a_mov = Arrow([xb, -0.15, 0], [xa, -0.15, 0], buff=0, stroke_width=4, color=FG, tip_length=0.22)
        l_cast = T("cast", 32, FG).next_to(a_cast, UP, buff=0.15)
        l_mov = T("movies", 32, FG).next_to(a_mov, DOWN, buff=0.15)

        with self.say("c6.graph.5", gap=2.2) as c:
            sweep_clear(self, *during(appear(kid, chap, lag=0.3), 0.5, 1.0), run_time=1.6)
            self.play(GrowArrow(a_cast), GrowArrow(a_mov), *appear(l_cast, l_mov, lag=0.3),  # early: both directions named together
                      run_time=min(1.2, c.until("cast")))
            c.wait_until("cast")
            self.play(a_cast.animate.set_color(GREEN), l_cast.animate.set_color(GREEN),
                      *flash([kid.code.find('"actors"')], color=GREEN), run_time=1.2)
            c.wait_until("movies")
            qm = T("?", 56, RED).next_to(l_mov, RIGHT, buff=0.15)
            self.play(a_mov.animate.set_color(RED), l_mov.animate.set_color(RED), *appear(qm), run_time=1.2)

            # read all 2,935 to find five
            c.wait_until("His document")
            cols, found = movie_grid()
            self.play(*during(disappear(kid, a_cast, a_mov, l_cast, l_mov, qm), 0, 0.4),
                      *during([chap.animate.move_to([-3.6, 1.6, 0])], 0.25, 0.75),
                      *during([FadeIn(cols), FadeIn(found)], 0.55, 1.0), run_time=1.6)
            k = ValueTracker(0)
            cpos = np.array([3.15, -1.6, 0])
            cnt = always_redraw(lambda: T(f"{int(k.get_value()):,} read", 40, GOLD).move_to(cpos))
            self.add(cnt)
            sweep = max(2.5, min(3.6, c.until("fixes") - 1.3))
            w = 0.25
            step = (sweep - w) / GRID_COLS
            anims = [time_span(col.animate.set_fill(TEAL, 0.9), step * i, step * i + w)
                     for i, col in enumerate(cols)]
            anims += [time_span(f.animate.set_fill(YELLOW, 1).scale(2.6), step * f.col, step * f.col + w)
                      for f in found]
            self.play(*anims, k.animate(rate_func=linear).set_value(N_MOVIES), run_time=sweep)
            cnt.clear_updaters()
            done = T("2,935 read, 5 found", 40, GOLD).move_to(cpos)
            self.play(*swap(cnt, done), run_time=0.9)

            # fixes
            fx1 = T("store it twice", 36, GREEN).move_to([-3.6, -0.6, 0])
            fx2 = T("secondary index: person ID → movies", 30, GREEN).move_to([3.15, -2.7, 0])
            c.wait_until(own_word=fx1)
            self.play(*appear(fx1), run_time=1.0)
            c.wait_until(own_word=fx2)
            self.play(*appear(fx2), run_time=1.0)

            # next: the tangle returns, glowing
            c.wait_until("next")
            tg = tangle()
            halos = VGroup(*[Circle(radius=R_VERT + 0.12).set_stroke(v.circle.get_stroke_color(), 14, opacity=0.25)
                             .move_to(v.circle) for v in tg.v.values()])
            cap = T("Lecture 5: graph databases", 44, YELLOW).move_to([0, -3.15, 0])
            sweep_clear(self, FadeIn(tg), *during(appear(cap), 0.6, 1.0), run_time=1.6)
            self.play(FadeIn(halos), *[VShowPassingFlash(ln.copy().set_stroke(YELLOW, 8), time_width=0.6)
                                       for ln in tg.lines], run_time=1.5)
