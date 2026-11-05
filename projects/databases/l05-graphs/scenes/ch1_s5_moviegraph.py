"""Chapter 1, scene 5: our movies as a property graph (Slide 97). Clips c1.movies.1 – c1.movies.4.

Exports for later scenes (load_scene("ch1_s5_moviegraph")):
  house_graph()    Slide 97, fitted to the frame (natural layout x0.8): Coogan TL, Chaplin TR, The Kid BL,
                   The Gold Rush BR. .v[key] (circle only; .circle), .tags[key], .cards[key],
                   .edges["coogan_kid" | "chaplin_kid" | "chaplin_gold" | "directed"] (.arrow .label),
                   .roles["coogan_kid"] (two-line GOLD card; Chaplin's roles live on fan() and the fold view,
                   no room for them here at 28); keys coogan chaplin kid gold.
  fan()            Chaplin's five typed edges to The Kid, full size, top of frame (lanes y 2.5 .. 0.5):
                   .kid .chaplin (vertex, name above), .lanes[i] (.path .tip), .labels[i], .props[i]
                   (each on a BG plate .label_bgs[i] / .prop_bgs[i]),
                   .types; order ACTED_IN, COMPOSED_FOR, DIRECTED, PRODUCED, WROTE (has_position's row order).
  seven_tables()   Lecture 4's seven BLUE table cards (2.6 x 0.62, title T 30), a column in Lecture 4's order
                   movies ratings genres has_genre people has_position plays_role; .cards, .by_name[name].
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

S4 = load_scene("ch1_s4_propgraph")
S2 = load_scene("ch1_s2_lasttime")
vertex, label_tag, tag_on, prop_card = S4.vertex, S4.label_tag, S4.tag_on, S4.prop_card
typed_edge, grow_edge = S4.typed_edge, S4.grow_edge


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- Slide 97
HC, HR, HS = 4.4, 1.81, 0.93     # natural column x, row y; the whole is scaled by HS to fit


def roles_card2(value):
    """A GOLD roles card on two lines ('roles:' over the list), narrower than prop_card's one line."""
    r0 = Mono("roles:", size=28)
    r1 = Mono(value, size=28)
    VGroup(r0, r1).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    r1.shift(0.3 * RIGHT)
    rows = VGroup(r0, r1)
    box = RoundedRectangle(corner_radius=0.12, width=rows.width + 0.5, height=rows.height + 0.4)
    box.set_stroke(GOLD, 2.5).set_fill(GOLD, 0.08).move_to(rows)
    g = VGroup(box, r0, r1)
    g.box, g.rows = box, [r0, r1]
    return g


def house_graph():
    spec = [("coogan", "Jackie Coogan", "Person", P(-HC, HR)),
            ("chaplin", "Charles Chaplin", "Person", P(HC, HR)),
            ("kid", "The Kid", "Movie", P(-HC, -HR)),
            ("gold", "The Gold Rush", "Movie", P(HC, -HR))]
    props = {"coogan": [("name", "Jackie Coogan"), ("birthyear", "1914")],
             "chaplin": [("name", "Charles Chaplin"), ("birthyear", "1889")],
             "kid": [("title", "The Kid"), ("year", "1921")],
             "gold": [("title", "The Gold Rush"), ("year", "1925")]}
    v, tags, cards = {}, {}, {}
    for key, name, kind, at in spec:
        vv = vertex(name, kind, at=at)
        vv.remove(vv.label)               # the card carries the name
        v[key] = vv
        side = LEFT if at[0] < 0 else RIGHT
        tags[key] = label_tag(f":{kind}").next_to(vv.circle, side, buff=0.15)
        card = prop_card(props[key])
        card.next_to(vv.circle, UP if at[1] > 0 else DOWN, buff=0.15)
        cards[key] = card
    e = {}
    e["coogan_kid"] = typed_edge(v["coogan"], v["kid"], "ACTED_IN")
    e["coogan_kid"].label.next_to(e["coogan_kid"].arrow, LEFT, buff=0.15).set_y(0.45)
    e["chaplin_kid"] = typed_edge(v["chaplin"], v["kid"], "ACTED_IN")
    e["chaplin_kid"].label.move_to(P(0.7, 1.08))
    e["chaplin_gold"] = typed_edge(v["chaplin"], v["gold"], "ACTED_IN")
    e["chaplin_gold"].label.next_to(e["chaplin_gold"].arrow, RIGHT, buff=0.15).set_y(-0.45)
    e["directed"] = typed_edge(v["chaplin"], v["kid"], "DIRECTED", angle=-0.54)
    e["directed"].label.next_to(e["directed"].arrow.point_from_proportion(0.5), DOWN, buff=0.18).shift(0.8 * RIGHT)
    roles = {"coogan_kid": roles_card2("['The Child']")}
    roles["coogan_kid"].align_to(P(-HC + 0.15, 0), LEFT).align_to(P(0, 1.2), UP)
    g = VGroup(*v.values(), *tags.values(), *cards.values(), *e.values(), *roles.values())
    g.scale(HS, about_point=ORIGIN)
    g.v, g.tags, g.cards, g.edges, g.roles = v, tags, cards, e, roles
    return g


# ---------------------------------------------------------------- the fan of five
FAN_X, FAN_Y, LANE_DY = 5.6, 2.5, 0.5
FAN_FLAT = 3.9
FAN_TYPES = ["ACTED_IN", "COMPOSED_FOR", "DIRECTED", "PRODUCED", "WROTE"]
FAN_PROPS = ["roles: ['A Tramp']", "job: 'composer'", "job: 'director'", "job: 'producer'",
             "job: 'written by'"]


def arrow_tip(point, direction, color, length=0.25, width=0.25):
    d = normalize(direction)
    p = rotate_vector(d, PI / 2)
    base = point - d * length
    return Polygon(point, base + p * width / 2, base - p * width / 2).set_stroke(color, 1).set_fill(color, 1)


def lane(ch_c, kid_c, k, r=0.5, color=FG):
    """Chaplin -> The Kid lane k: leaves Chaplin's rim 20k degrees below horizontal, runs flat at
    y = FAN_Y - k*LANE_DY, enters The Kid symmetrically."""
    a = np.radians(20 * k)
    y = ch_c[1] - LANE_DY * k
    ds = np.array([-np.cos(a), -np.sin(a), 0])          # out of Chaplin, toward lower left
    de = np.array([np.cos(a), -np.sin(a), 0])           # out of The Kid, toward lower right
    S = ch_c + (r + 0.06) * ds
    E = kid_c + (r + 0.06) * de                         # tip point
    Eb = E + 0.22 * de                                  # where the stroke ends (tip base)
    A, B = P(FAN_FLAT, y), P(-FAN_FLAT, y)
    path = VMobject()
    path.start_new_path(S)
    path.add_cubic_bezier_curve_to(S + 0.6 * ds, A + 0.8 * RIGHT, A)
    path.add_line_to(B)
    path.add_cubic_bezier_curve_to(B + 0.8 * LEFT, Eb + 0.5 * de, Eb)
    path.set_stroke(color, 4)
    tip = arrow_tip(E, -de, color)
    g = VGroup(path, tip)
    g.path, g.tip, g.y = path, tip, y
    return g


def fan():
    kid = vertex("The Kid", "Movie", at=P(-FAN_X, FAN_Y))
    ch = vertex("Charles Chaplin", "Person", at=P(FAN_X, FAN_Y))
    for vv in (kid, ch):
        vv.label.next_to(vv.circle, UP, buff=0.18)
    if ch.label.get_right()[0] > 6.55:
        ch.label.shift((6.55 - ch.label.get_right()[0]) * RIGHT)
    lanes, labels, props, lbgs, pbgs = [], [], [], [], []
    for k, (t, pr) in enumerate(zip(FAN_TYPES, FAN_PROPS)):
        ln = lane(ch.circle.get_center(), kid.circle.get_center(), k)
        lab = Mono(t, size=28).move_to(P(0, ln.y)).align_to(P(-FAN_FLAT + 0.15, 0), LEFT)
        lab.set_y(ln.y).set_z_index(2)
        pp = Mono(pr, size=28, color=GOLD).move_to(P(0, ln.y)).align_to(P(-0.6, 0), LEFT)
        pp.set_y(ln.y).set_z_index(2)
        lb = BackgroundRectangle(lab, color=BG, fill_opacity=1, buff=0.1).set_z_index(1)
        pb = BackgroundRectangle(pp, color=BG, fill_opacity=1, buff=0.1).set_z_index(1)
        lanes.append(ln)
        labels.append(lab)
        props.append(pp)
        lbgs.append(lb)
        pbgs.append(pb)
    g = VGroup(kid, ch, *lanes, *lbgs, *pbgs, *labels, *props)
    g.kid, g.chaplin, g.lanes, g.labels, g.props, g.types = kid, ch, lanes, labels, props, FAN_TYPES
    g.label_bgs, g.prop_bgs = lbgs, pbgs     # BG plates that cut the lane under each text
    return g


# ---------------------------------------------------------------- Lecture 4's seven tables
SEVEN = ["movies", "ratings", "genres", "has_genre", "people", "has_position", "plays_role"]


def table_chip(name):
    box = RoundedRectangle(corner_radius=0.1, width=2.6, height=0.62)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.06)
    t = T(name, 30, BLUE).move_to(box)
    g = VGroup(box, t)
    g.box, g.title, g.name = box, t, name
    return g


def seven_tables():
    cards = [table_chip(n) for n in SEVEN]
    g = VGroup(*cards).arrange(DOWN, buff=0.22)
    g.cards, g.by_name = cards, dict(zip(SEVEN, cards))
    return g


# ---------------------------------------------------------------- clip 3: the fold view
def fold_graph():
    kid = vertex("The Kid", "Movie", at=P(-1.9, 2.25))
    ch = vertex("Charles Chaplin", "Person", at=P(4.7, 2.25))
    edge = typed_edge(ch, kid, "ACTED_IN", side=DOWN)
    roles = prop_card([("roles", "['A Tramp']")], color=GOLD)
    roles.move_to(P(edge.arrow.get_center()[0], 2.95))
    card = prop_card([("title", "The Kid"), ("year", "1921"), ("rating", "8.2"),
                      ("genres", "['Comedy', 'Drama', 'Family']")])
    card.next_to(kid.label, DOWN, buff=0.3).align_to(P(-3.5, 0), LEFT)
    g = VGroup(kid, ch, edge, card.box, *card.rows[:2])
    g.kid, g.ch, g.edge, g.roles, g.card = kid, ch, edge, roles, card
    return g


FOLD_COL_X = -5.3
FOLD_Y = {"plays_role": 2.9, "people": 2.05, "has_position": 1.2, "movies": 0.35,
          "ratings": None, "genres": None, "has_genre": None}


def counts_panel():
    mv = Circle(radius=0.45).set_stroke(BLUE, 4).set_fill(BLUE, 0.2)
    ps = Circle(radius=0.45).set_stroke(PINK, 4).set_fill(PINK, 0.2)
    mtag, ptag = label_tag(":Movie"), label_tag(":Person")
    mnum, pnum = T("2,935", 48, GOLD), T("23,179", 48, GOLD)
    movie = VGroup(mv, mtag, mnum)
    person = VGroup(ps, ptag, pnum)
    for grp in (movie, person):
        grp[1].next_to(grp[0], RIGHT, buff=0.3)
        grp[2].next_to(grp[1], RIGHT, buff=0.35)
    movie.move_to(P(-3.3, 0.9))
    person.move_to(P(-3.3, -0.9))
    person.align_to(movie, LEFT)
    nums = ["29,153", "3,281", "3,166", "7,429", "6,782"]
    order = [0, 3, 4, 1, 2]     # ACTED_IN, PRODUCED, WROTE, COMPOSED_FOR, DIRECTED (largest first)
    rows = []
    for i, k in enumerate(order):
        lab = Mono(FAN_TYPES[k], 32)
        num = Mono(nums[k], 32, color=GOLD)
        lab.move_to(P(0, 1.6 - 0.8 * i)).align_to(P(1.2, 0), LEFT)
        num.move_to(P(0, 1.6 - 0.8 * i)).align_to(P(6.3, 0), RIGHT)
        rows.append(VGroup(lab, num))
    head = T("five edge types", 30, DIM).next_to(rows[0], UP, buff=0.4).align_to(rows[0], LEFT)
    g = VGroup(movie, person, head, *rows)
    g.movie, g.person, g.head, g.rows = movie, person, head, rows
    return g


def mini_graph(center):
    pos = {"coogan": P(-1.5, 1.2), "chaplin": P(1.5, 1.2), "kid": P(-1.5, -1.2), "gold": P(1.5, -1.2)}
    col = {"coogan": PINK, "chaplin": PINK, "kid": BLUE, "gold": BLUE}
    circ = {k: Circle(radius=0.4).set_stroke(col[k], 4).set_fill(col[k], 0.2).move_to(pos[k] + center)
            for k in pos}
    arrows = []
    for a, b in [("coogan", "kid"), ("chaplin", "kid"), ("chaplin", "gold")]:
        ca, cb = circ[a].get_center(), circ[b].get_center()
        d = normalize(cb - ca)
        ln = Line(ca + d * 0.46, cb - d * 0.46).set_stroke(FG, 4)
        ln.add_tip(tip_length=0.22, tip_width=0.22)
        ln.tip.set_fill(FG, 1).set_stroke(FG, 1)
        arrows.append(ln)
    g = VGroup(*arrows, *circ.values())
    g.circ, g.arrows = circ, arrows
    return g


def flow(src, point, move_rt=0.8, fade_rt=0.25):
    """A copy of src travels to point and fades there (for a second source of the same target)."""
    cp = src.copy()
    return Succession(cp.animate(run_time=move_rt).move_to(point), FadeOut(cp, run_time=fade_rt))


def ghost_flow(card, point):
    """A copy of a table card travels to point: invisible until it has left the card, gone on arrival."""
    cp = card.copy()
    start = cp.get_center()

    def upd(m, a):
        m.move_to(start + (point - start) * smooth(a))
        o = float(np.clip((a - 0.4) / 0.15, 0, 1)) * float(np.clip((1 - a) / 0.2, 0, 1))
        m.box.set_stroke(opacity=o)
        m.box.set_fill(opacity=0.06 * o)
        m.title.set_opacity(o)
    upd(cp, 0)
    return UpdateFromAlphaFunc(cp, upd, remover=True)


# ---------------------------------------------------------------- the scene
class MovieGraph(NarratedScene):
    def construct(self):
        self.clip_build()
        self.clip_fan()
        self.clip_fold()
        self.clip_naming()
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1.movies.1
    def clip_build(self):
        hg = house_graph()
        self.hg = hg
        tg = S2.tangle()
        keys = ("coogan", "chaplin", "kid", "gold")
        with self.say("c1.movies.1") as c:
            self.play(FadeIn(*tg.lines, *[tg.v[k].circle for k in keys]), run_time=1.0)
            self.wait(0.4)
            self.play(*[tg.v[k].circle.animate.move_to(hg.v[k].circle).scale(HS) for k in keys],
                      *[FadeOut(ln) for ln in tg.lines],
                      run_time=min(1.6, c.until("coogan")))
            self.remove(*tg.get_family())
            self.add(*[hg.v[k] for k in keys])
            c.wait_until("coogan")
            self.play(*appear(hg.tags["coogan"], hg.cards["coogan"], lag=0.35),
                      run_time=min(1.4, c.until("chaplin")))
            c.wait_until("chaplin")
            self.play(*appear(hg.tags["chaplin"], hg.cards["chaplin"], lag=0.35),
                      run_time=min(1.4, c.until("films")))
            c.wait_until("films")
            self.play(*appear(hg.tags["kid"], hg.tags["gold"], shift=None),
                      run_time=min(1.0, c.until("the kid")))
            c.wait_until("the kid")
            self.play(*appear(hg.cards["kid"]), run_time=min(1.0, c.until("the gold rush")))
            c.wait_until("the gold rush")
            self.play(*appear(hg.cards["gold"]), run_time=min(1.0, c.until("edges")))
            c.wait_until("edges")
            acted = [hg.edges[k] for k in ("coogan_kid", "chaplin_kid", "chaplin_gold")]
            self.play(LaggedStart(*[grow_edge(e.arrow) for e in acted], lag_ratio=0.3),
                      run_time=min(1.8, c.until("from the person")))
            c.wait_until("from the person")
            self.play(*[VShowPassingFlash(e.arrow.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for e in acted], run_time=1.4)
            c.wait_until("acted")
            self.play(*appear(hg.edges["coogan_kid"].label), run_time=min(1.0, c.until("as the child")))
            c.wait_until("as the child")
            self.play(*appear(hg.roles["coogan_kid"]), run_time=min(1.0, c.until("chaplin acted")))
            c.wait_until("chaplin acted")
            self.play(*appear(hg.edges["chaplin_kid"].label, hg.edges["chaplin_gold"].label, lag=0.25),
                      run_time=min(1.1, c.until("directed")))
            c.wait_until("directed")
            self.play(grow_edge(hg.edges["directed"].arrow), run_time=0.9)
            self.play(*appear(hg.edges["directed"].label), run_time=min(0.8, c.until(None)))
        settle(self, hg)

    # ------------------------------------------------------------ c1.movies.2
    def clip_fan(self):
        hg = self.hg
        fn = fan()
        self.fn = fn
        ch, kid = hg.v["chaplin"], hg.v["kid"]
        others = [m for m in hg.submobjects if m is not ch and m is not kid]
        hp_colors = [[DIM] * 4] + [[FG, FG, FG, DIM if r == 1 else FG] for r in range(1, 6)]
        body = S2.grid(S2.HP_ROWS, hp_colors)
        card = S2.table_card("has_position", body, body.width + 0.6)
        card.move_to(P(0, 0)).align_to(P(0, 0.05), UP)
        rows = list(body[1:])
        note = T("49,811 rows = 49,811 edges", 32, GOLD)
        note.match_y(card.title).align_to(card.box, RIGHT).shift(0.3 * LEFT)

        with self.say("c1.movies.2") as c:
            c.wait_until("five jobs")
            self.play(*during([FadeOut(m) for m in others], 0, 0.45),
                      *during([ch.animate.move_to(fn.chaplin.circle).scale(1 / HS),
                               kid.animate.move_to(fn.kid.circle).scale(1 / HS)], 0.2, 0.8),
                      *during(appear(fn.kid.label, fn.chaplin.label), 0.55, 1),  # early: the two names return with their circles
                      run_time=min(1.8, c.until("fan")))
            self.remove(*hg.get_family())
            self.add(fn.kid.circle, fn.chaplin.circle)
            c.wait_until("fan")
            self.play(LaggedStart(*[Succession(Create(ln.path, run_time=1.0), FadeIn(ln.tip, run_time=0.25))
                                    for ln in fn.lanes], lag_ratio=0.18),
                      run_time=min(2.0, c.until("acted in")))
            for k, word in [(0, "acted in"), (2, "directed"), (3, "produced"), (4, "wrote"),
                            (1, "composed for")]:
                c.wait_until(word)
                extra = [fn.prop_bgs[0], fn.props[0]] if k == 0 else []
                self.play(FadeIn(fn.label_bgs[k]), *appear(fn.labels[k], *extra, shift=0.12 * DOWN, lag=0.3),
                          run_time=min(0.7 if k == 0 else 0.5, c.until("rows")))
            c.wait_until("rows")
            self.play(*appear(card.box, card.title, *body, shift=0.4 * UP, lag=0.04),  # early: the table arrives whole
                      run_time=min(1.0, c.until("in fact")))
            box = token_box(rows[0], rows[0], height=0.44)
            self.play(FadeIn(box), *recolor([fn.labels[0]], YELLOW), run_time=0.45)
            for k in range(1, 5):
                self.play(Transform(box, token_box(rows[k], rows[k], height=0.44)),
                          *recolor([fn.labels[k]], YELLOW), *recolor([fn.labels[k - 1]], FG),
                          run_time=0.35)
            c.wait_until("all")
            self.play(FadeOut(box), *recolor([fn.labels[4]], FG), *appear(note), run_time=1.0)
            c.wait_until("forty-nine thousand")
            self.play(FlashAround(note, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("job")
            self.play(*recolor([r[2] for r in rows], YELLOW), *recolor(fn.labels, YELLOW),
                      *flash(fn.labels), run_time=1.2)
            c.wait_until("the job column")
            self.play(*recolor([r[3] for r in rows[1:]], GOLD),
                      *[FadeIn(b) for b in fn.prop_bgs[1:]],
                      *appear(*fn.props[1:], shift=0.12 * DOWN, lag=0.2),
                      run_time=min(1.4, c.until(None)))
        self.rows_card = card
        self.note = note

    # ------------------------------------------------------------ c1.movies.3
    def clip_fold(self):
        fg = fold_graph()
        st = seven_tables()
        tb = st.by_name
        rate_y = fg.card.rows[2].get_y()
        ys = dict(FOLD_Y, ratings=rate_y, genres=rate_y - 0.87, has_genre=rate_y - 1.74)
        for n, cd in tb.items():
            cd.move_to(P(FOLD_COL_X, ys[n]))
        note = VGroup(T("30,303 roles", 30, GOLD),
                      T("on 29,153 ACTED_IN edges", 30, GOLD),
                      T("1,007 edges hold more than one", 28, DIM)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        note.to_edge(RIGHT, buff=0.5).align_to(P(0, -1.75), UP)
        gc = DashedVMobject(Circle(radius=0.5).set_stroke(DIM, 3), num_dashes=18)
        gc.move_to(P(-2.6, -2.5))
        gq = T("Genre?", 30, DIM).next_to(gc, RIGHT, buff=0.25)
        ex = T("Exercise 22", 28, DIM)
        exbox = RoundedRectangle(corner_radius=0.1, width=ex.width + 0.3, height=0.5).set_stroke(DIM, 2)
        exbox.move_to(ex)
        extag = VGroup(exbox, ex).next_to(gq, DOWN, buff=0.2).align_to(gq, LEFT)
        row3 = fg.card.rows[3]
        cp = counts_panel()

        with self.say("c1.movies.3") as c:
            sweep_clear(self, *appear(*st.cards, lag=0.06, shift=None),  # early: the seven tables shown whole, then folded in one by one
                        *appear(fg, shift=None), run_time=1.3)
            self.play(*flash([tb["people"], fg.ch.circle, tb["movies"], fg.kid.circle,
                              tb["has_position"], fg.edge.arrow]), run_time=min(1.0, c.until("roles")))
            c.wait_until("roles")
            self.play(*fly(tb["plays_role"], fg.roles),
                      *set_alpha([tb["people"], tb["movies"], tb["has_position"]], 0.4),
                      run_time=min(1.5, c.until("its a list")))
            c.wait_until("its a list")
            self.play(*appear(*note, lag=0.5), run_time=min(1.6, c.until("rating")))
            c.wait_until("rating")
            self.play(*fly(tb["ratings"], fg.card.rows[2]), *set_alpha([tb["plays_role"]], 0.4),
                      run_time=min(1.4, c.until("genres")))
            c.wait_until("genres")
            self.play(*during([ghost_flow(tb["has_genre"], row3.get_center())], 0, 0.6),
                      *during(fly(tb["genres"], row3), 0.3, 1.0),
                      *set_alpha([tb["ratings"]], 0.4), run_time=1.8)
            box = token_box(select(row3, "'Comedy'")[0], row3, height=0.42)
            c.wait_until("comedy")
            self.play(FadeIn(box), *set_alpha([tb["genres"], tb["has_genre"]], 0.4), run_time=0.4)
            for w in ("drama", "family"):
                c.wait_until(w)
                self.play(Transform(box, token_box(select(row3, f"'{w.capitalize()}'")[0], row3, height=0.42)),
                          run_time=0.4)
            c.wait_until("nogenre")
            self.play(FadeOut(box), FadeIn(gc), *appear(gq), run_time=1.0)
            self.play(*appear(extag), run_time=1.0)  # early: the exercise is named in this sentence
            c.wait_until("counts")
            sweep_clear(self, *appear(cp.movie, cp.person, cp.head, *cp.rows, lag=0.12, shift=None),  # early: the totals shown whole, then read
                        run_time=min(1.6, c.until("two thousand")))
            c.wait_until("two thousand")
            self.play(FlashAround(cp.movie, color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("twenty-three")
            self.play(FlashAround(cp.person, color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("five types")
            self.play(FlashAround(VGroup(*cp.rows), color=GOLD, time_width=1.5), run_time=min(1.4, c.until(None)))

    # ------------------------------------------------------------ c1.movies.4
    def clip_naming(self):
        ch = vertex("Charles Chaplin", "Person", at=P(-3.7, 1.0))
        kid = vertex("The Kid", "Movie", at=P(3.7, 1.0))
        ctag, ktag = tag_on(label_tag(":Person"), ch), tag_on(label_tag(":Movie"), kid)
        edge = typed_edge(ch, kid, "DIRECTED")
        pic = VGroup(ch, kid, ctag, ktag, edge)
        n1 = T("Charles Chaplin", 48, PINK)
        d0 = T("D", 48)
        d1 = T("IRECTED", 36).next_to(d0, RIGHT, buff=0.03, aligned_edge=DOWN)
        verb = VGroup(d0, d1)
        n2 = T("The Kid", 48, BLUE)
        sent = VGroup(n1, verb, n2).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to(P(0, -1.5))
        tags = [T(s, 30, DIM).next_to(w, DOWN, buff=0.3) for s, w in
                (("noun", n1), ("past-tense verb", verb), ("noun", n2))]
        for t in tags:
            t.set_y(tags[0].get_y())

        st = seven_tables()
        tb = st.by_name
        grid_pos = {"movies": (0, 0), "ratings": (1, 0), "genres": (0, 1), "has_genre": (1, 1),
                    "people": (0, 2), "has_position": (1, 2), "plays_role": (0, 3)}
        for n, (cx, ry) in grid_pos.items():
            tb[n].move_to(P(-4.9 + 2.8 * cx, 1.5 - 0.9 * ry))
        both = T("both just tables", 32, YELLOW).move_to(P(-3.5, -2.25))
        mg = mini_graph(P(3.7, 0.3))
        things = T("things: vertices", 30, YELLOW).move_to(P(3.7, 2.85))
        th_arrows = [Arrow(things.get_bottom() + 0.05 * DOWN + s * 0.6 * RIGHT,
                           mg.circ[k].get_top() + 0.06 * UP, buff=0, stroke_width=3,
                           max_tip_length_to_length_ratio=0.35).set_color(YELLOW)
                     for k, s in (("coogan", -1), ("chaplin", 1))]
        rel = T("relationships: edges", 30, YELLOW).move_to(P(3.7, -2.45))
        mid = mg.arrows[1].get_center()
        rel_arrow = Arrow(rel.get_top() + 0.08 * UP, mid + 0.12 * DOWN, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.15).set_color(YELLOW)

        with self.say("c1.movies.4") as c:
            sweep_clear(self, *appear(pic, shift=None), run_time=min(1.5, c.until("labels are nouns")))  # early: one edge, the zoom
            c.wait_until("labels are nouns")
            self.play(*flash([ctag, ktag]), *recolor([ctag.text, ktag.text], YELLOW), run_time=1.2)
            c.wait_until("edge types are verbs")
            self.play(FlashAround(edge.label, time_width=1.5), *recolor([edge.label], YELLOW), run_time=1.2)
            c.wait_until("sentence")
            self.play(*fly(ch.label, n1), *fly(kid.label, n2), *during(appear(verb), 0.4, 1),
                      FlashAround(edge.label, time_width=1.5), run_time=min(1.6, c.until("distinct")))
            self.play(*appear(*tags, lag=0.2), run_time=min(1.0, c.until("distinct")))
            c.wait_until("to the relational model")
            sweep_clear(self, *appear(*st.cards, lag=0.06, shift=None),  # early: all seven, the same shape
                        run_time=min(1.4, c.until("people and has position")))
            c.wait_until("people and has position")
            self.play(restyle(tb["people"].box, outline=YELLOW, width=4),
                      restyle(tb["has_position"].box, outline=YELLOW, width=4),
                      *recolor([tb["people"].title, tb["has_position"].title], YELLOW), run_time=1.0)
            c.wait_until(own_word=both)
            self.play(*appear(both), run_time=1.0)
            c.wait_until("knows")
            self.play(FadeIn(mg), run_time=min(1.2, c.until("things are vertices")))
            c.wait_until(own_word=things)
            self.play(*appear(things), *[GrowArrow(a) for a in th_arrows], run_time=1.0)
            c.wait_until(own_word=rel)
            self.play(*appear(rel), GrowArrow(rel_arrow), run_time=min(1.0, c.until(None)))
