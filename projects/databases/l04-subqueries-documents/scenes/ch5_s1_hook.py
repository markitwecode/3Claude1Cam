"""Chapter 5, scene 1: how many times is Chaplin's name stored? Clips c5.hook.1 – c5.hook.3.

Exports (import with `H = load_scene("ch5_s1_hook")`; all static, no updaters):

    H.open_card() -> VGroup, ch5's first frame (= ch4 s7's end card):
        .kid   The Kid's TEAL doc card (ch4 s3 doc_card look, Code 19), centre (-3.8, 0.4),
               "Charles Chaplin" GOLD (other strings FG)
        .fan   VGroup of 5 DIM TEAL movie cards (MovieCard, 1.32 x 2.1), The Gold Rush, City Lights,
               Modern Times, The Great Dictator, Chaplin, centres x 0.125 + 1.44 i, arced, tilted
        .copies VGroup of their 16 GOLD "Charles Chaplin" tags (4, 4, 4, 3, 1; T 14) (parts of .fan)
        .buy   GOLD "buy" tag at (-3.8, -2.75)    .cost  RED "cost" tag at (3.0, -2.75)
    H.MOVIES  [(title, credits)]: The Kid 5, The Gold Rush 4, City Lights 4, Modern Times 4,
              The Great Dictator 3, Chaplin 1  (21 has_position rows)
    H.movie_card(title, n, w=1.9, h=1.9, title_size=20, tag_size=17, pitch=0.26)
        -> MovieCard(.frame TEAL doc frame, .title T, .tags VGroup of n GOLD "Charles Chaplin")
    H.split_frame() -> VGroup(.divider DIM line x=0.3, .rel BLUE "relational" (-4.3, 3.5),
                              .doc TEAL "documents" (4.5, 3.5))
    H.people_side() -> VGroup, the left half:
        .card  VGroup(.table ch1 s2 TableCard("people"), .vbox YELLOW box, .values {col: Mono YELLOW})
               scaled 0.85, centre x -3.6, top 2.85 (Chaplin's one row, transposed)
        .one   GOLD "1" right of his name          .strips 6 VGroups of thin BLUE bars (5,4,4,4,3,1)
        .arrows VGroup of 21 BLUE arrows, bar tops -> the row's box   .label DIM "refers by person_id"
    H.docs_side() -> VGroup, the right half: .own Chaplin's own TEAL card (name YELLOW), centre
        (3.65, 2.15); .cards 6 MovieCards (tags BOLD) (3 x 2 grid, centres x 1.63/3.65/5.67, y 0.1/-1.95), 21
        GOLD tags; .counter GOLD "21 copies in 6 movie documents" at (3.65, -3.35)
    H.question() -> T "Bug or feature?" 44 YELLOW at (0, 3.3); .bug .feature (glyph VGroups)
    H.handover_shot() -> the last frame: split_frame + people_side + docs_side dimmed to 0.25
        (GOLD tags full), question with "Bug" RED and "feature" GREEN.
        .split .left .right .q, as above.
    H.dim_static(mob, a) multiplies every part's built opacity by a (H.dim(mob, a): the Transform).
    H.recap_r1() -> thumbnail at ORIGIN (~6.6 x 2.6): .row one BLUE people row "Charles Chaplin",
        .cards six small TEAL cards (3 x 2) with .copies 21 GOLD tag bars (5,4,4,4,3,1).
"""
# style: 2
# handover: next
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

D = load_scene("ch4_s3_movie")
SCH = load_scene("ch1_s2_schema")

MOVIES = [("The Kid", 5), ("The Gold Rush", 4), ("City Lights", 4), ("Modern Times", 4),
          ("The Great Dictator", 3), ("Chaplin", 1)]
NAME = "Charles Chaplin"
LX, RX = -3.6, 3.65
DIV_X = 0.3
GRID = [(1.63, 0.1), (3.65, 0.1), (5.67, 0.1), (1.63, -1.95), (3.65, -1.95), (5.67, -1.95)]
KEYS = ["actors", "directors", "producers", "writers", "composers"]
SAID = ["actor", "director", "producer", "writer", "composer"]
ACTORS = ["Chaplin", "Coogan", "Purviance", "Miller", "Austin", "Bains", "Baker", "Bergman",
          "Biby", "Blinn"]


# ══ helpers ════════════════════════════════════════════════════════════════════

def _plain(code):
    """String values FG (the lexer makes every string GOLD; here GOLD means 'a copy')."""
    gold = ManimColor(GOLD).to_hex().lower()
    for g in code.text.submobjects:
        if g.get_fill_color().to_hex().lower() == gold:
            g.set_color(FG)
    return code


def _card(src, size, at, gold=(), yellow=()):
    card = D.doc_card(src, size=size)
    _plain(card.code)
    for s in gold:
        card.code.find(s).set_color(GOLD)
    for s in yellow:
        card.code.find(s).set_color(YELLOW)
    card.move_to(at)
    return card


def dim_static(mob, a=DIMMED):
    for p in mob.get_family():
        bf, bs = getattr(p, "_base", (p.get_fill_opacity(), p.get_stroke_opacity()))
        p.set_fill(opacity=bf * a, family=False)
        p.set_stroke(opacity=bs * a, family=False)
    return mob


def dim(mob, a=DIMMED):
    return SCH.card_alpha(mob, a)


class MovieCard(VGroup):
    def __init__(self, title, n, w=1.9, h=1.9, title_size=20, tag_size=17, pitch=0.26,
                 title_color=FG, tag_weight=BOLD):
        super().__init__()
        self.frame = D.doc_card(width=w, height=h).frame
        t = T(title, title_size, title_color)
        if t.width > w - 0.2:
            words = title.split(" ")
            k = (len(words) + 1) // 2
            t = T(" ".join(words[:k]) + "\n" + " ".join(words[k:]), title_size, title_color)
        self.title = t.move_to(self.frame.get_top() + DOWN * (0.13 + t.height / 2))
        self.tags = VGroup(*[T(NAME, tag_size, GOLD, weight=tag_weight) for _ in range(n)])
        for g in self.tags:
            if g.width > w - 0.22:
                g.scale_to_fit_width(w - 0.22)
        y0 = self.title.get_bottom()[1] - 0.14
        for i, g in enumerate(self.tags):
            g.move_to([self.frame.get_x(), y0 - g.height / 2 - i * pitch, 0])
        self.add(self.frame, self.title, self.tags)


def movie_card(title, n, **kw):
    return MovieCard(title, n, **kw)


def _tag(word, color):
    w = T(word, 40, color)
    box = (RoundedRectangle(corner_radius=0.18, width=w.width + 0.6, height=0.75)
           .set_stroke(color, 3).set_fill(color, 0.12))
    g = VGroup(box, w.move_to(box))
    g.box, g.word = box, w
    return g


# ══ open card ══════════════════════════════════════════════════════════════════

OPEN_SRC = "\n".join(['{', '  "title": "The Kid",', '  "actors": [', '    {',
                      '      "name": "Charles Chaplin",', '      /* … */', '    },',
                      '    /* 9 more */', '  ]', '}'])


def open_card():
    g = VGroup()
    g.kid = _card(OPEN_SRC, 19, [-3.8, 0.4, 0], gold=['"Charles Chaplin"'])
    g.fan = VGroup()
    angles = [6, 3, 0, -3, -6]
    lift = [0.0, 0.14, 0.2, 0.14, 0.0]
    for i, (title, n) in enumerate(MOVIES[1:]):
        cd = MovieCard(title, n, w=1.32, h=2.1, title_size=16, tag_size=14, pitch=0.24, title_color=DIM,
                       tag_weight=NORMAL)
        cd.frame.set_stroke(TEAL, 3, opacity=0.45).set_fill(TEAL, 0.03)
        cd.rotate(angles[i] * DEGREES)
        cd.move_to([0.125 + 1.44 * i, 0.45 + lift[i], 0])
        g.fan.add(cd)
    g.copies = VGroup(*[t for cd in g.fan for t in cd.tags])
    g.buy = _tag("buy", GOLD).move_to([-3.8, -2.75, 0])
    g.cost = _tag("cost", RED).move_to([3.0, -2.75, 0])
    g.add(g.kid, g.fan, g.buy, g.cost)
    return g


# ══ bridge: ch4 s5's two-way copies (composed here; ch4 s5 isn't built yet) ═══════

KID_SRC = "\n".join(['{', '  "movie_id": "tt0012349",', '  "title": "The Kid",', '  "actors": [',
                     '    {', '      "person_id": "nm0000122",', '      "name": "Charles Chaplin",',
                     '      "roles": ["A Tramp"]', '    },', '    /* 9 more */', '  ]', '}'])
CHAP_SRC = "\n".join(['{', '  "person_id": "nm0000122",', '  "name": "Charles Chaplin",',
                      '  "acted_in": [', '    {', '      "movie_id": "tt0012349",',
                      '      "title": "The Kid",', '      "year": 1921,', '      "roles": ["A Tramp"]',
                      '    },', '    /* … */', '  ]', '}'])


def bridge():
    g = VGroup()
    g.kid = _card(KID_SRC, 20, [-3.4, -0.1, 0], gold=['"Charles Chaplin"'])
    g.chap = _card(CHAP_SRC, 20, [3.4, -0.1, 0], gold=['"The Kid"', "1921"])
    k, c = g.kid, g.chap
    pid = k.code.find('"nm0000122"')
    mid = c.code.find('"tt0012349"')
    a1 = Arrow([pid.get_right()[0] + 0.05, pid.get_y(), 0],
               [c.frame.get_left()[0], c.code.line(1).get_y(), 0],
               buff=0.04, stroke_width=3, color=FG, tip_length=0.18)
    a2 = Arrow([c.frame.get_left()[0], mid.get_y(), 0],
               [k.frame.get_right()[0], k.code.line(1).get_y(), 0],
               buff=0.04, stroke_width=3, color=FG, tip_length=0.18)
    g.arrows = [a1, a2]
    g.name_k = k.code.find('"Charles Chaplin"')
    g.name_c = c.code.find('"Charles Chaplin"')
    g.add(k, c, a1, a2)
    return g


# ══ the split ══════════════════════════════════════════════════════════════════

def split_frame():
    g = VGroup()
    g.divider = Line([DIV_X, 3.0, 0], [DIV_X, -3.55, 0]).set_stroke(DIM, 2)
    g.rel = T("relational", 36, BLUE).move_to([-4.3, 3.5, 0])
    g.doc = T("documents", 36, TEAL).move_to([4.5, 3.5, 0])
    g.add(g.divider, g.rel, g.doc)
    for m in g:
        SCH._remember(m)
    return g


def people_side():
    g = VGroup()
    tc = SCH.TableCard("people", 0, 0)
    cols = SCH.SCHEMA["people"][0]
    vals = dict(zip(cols, SCH.KID_ROWS["people"][0]))
    vw = 3.5
    vbox = Rectangle(width=vw, height=len(cols) * SCH.PITCH + SCH.PAD_B).set_stroke(YELLOW, 3)
    vbox.move_to([tc.box.get_right()[0] + vw / 2, -SCH.HDR - vbox.height / 2, 0])
    values = {}
    for col in cols:
        t, _ = SCH._placed(vals[col], SCH.COL_SIZE, YELLOW, NORMAL, tc.row_y(col),
                           left=tc.box.get_right()[0] + 0.22)
        values[col] = t
    card = VGroup(tc, vbox, *values.values())
    card.table, card.vbox, card.values = tc, vbox, values
    card.scale(0.85).move_to([LX, 2.85 - card.height * 0.5, 0])
    g.card = card
    g.one = T("1", 48, GOLD).move_to([vbox.get_right()[0] + 0.42, values["name"].get_y(), 0])
    # 21 has_position rows as thin bars, grouped by movie
    bw, bh, pitch, gap, top = 0.14, 1.0, 0.23, 0.28, -1.15
    total = sum((n - 1) * pitch + bw for _, n in MOVIES) + gap * (len(MOVIES) - 1)
    x = LX - total / 2
    g.strips = []
    for _, n in MOVIES:
        grp = VGroup()
        for j in range(n):
            grp.add(Rectangle(width=bw, height=bh).set_stroke(BLUE, 1.5).set_fill(BLUE, 0.55)
                    .move_to([x + bw / 2 + j * pitch, top - bh / 2, 0]))
        x += (n - 1) * pitch + bw + gap
        g.strips.append(grp)
    bars = [b for grp in g.strips for b in grp]
    l, r, y = vbox.get_left()[0] + 0.25, vbox.get_right()[0] - 0.25, vbox.get_bottom()[1]
    g.arrows = VGroup(*[
        Arrow(b.get_top(), [l + (r - l) * i / (len(bars) - 1), y, 0], buff=0.05, stroke_width=2,
              color=BLUE, tip_length=0.12, max_tip_length_to_length_ratio=0.1)
        for i, b in enumerate(bars)])
    g.label = T("refers by person_id", 28, DIM).move_to([LX, -2.8, 0])
    g.add(card, g.one, *g.strips, g.arrows, g.label)
    for m in [card, g.one, *g.strips, g.arrows, g.label]:
        SCH._remember(m)
    return g


OWN_SRC = "\n".join(['{', '  "name": "Charles Chaplin",', '  /* … */', '}'])


def docs_side():
    g = VGroup()
    g.own = _card(OWN_SRC, 20, [RX, 2.15, 0], yellow=['"Charles Chaplin"'])
    g.cards = [MovieCard(t, n).move_to([x, y, 0]) for (t, n), (x, y) in zip(MOVIES, GRID)]
    g.counter = T("21 copies in 6 movie documents", 30, GOLD).move_to([RX, -3.35, 0])
    g.add(g.own, *g.cards, g.counter)
    for m in [g.own, g.counter] + [p for cd in g.cards for p in (cd.frame, cd.title)]:
        SCH._remember(m)
    return g


def question():
    q = T("Bug or feature?", 44, YELLOW).move_to([0, 3.3, 0])
    q.bug = select(q, "Bug")[0]
    q.feature = select(q, "feature")[0]
    return q


def _dimmables(sp, ps, ds):
    return ([sp.divider, sp.rel, sp.doc, ps.card, ps.one, *ps.strips, ps.arrows, ps.label, ds.own,
             ds.counter] + [p for cd in ds.cards for p in (cd.frame, cd.title)])


def handover_shot():
    sp, ps, ds = split_frame(), people_side(), docs_side()
    for m in _dimmables(sp, ps, ds):
        dim_static(m)
    q = question()
    q.bug.set_color(RED)
    q.feature.set_color(GREEN)
    g = VGroup(sp, ps, ds, q)
    g.split, g.left, g.right, g.q = sp, ps, ds, q
    return g


# ══ s7 recap thumbnail ═════════════════════════════════════════════════════════

def recap_r1():
    g = VGroup()
    box = Rectangle(width=2.7, height=0.6).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)
    g.row = VGroup(box, Mono(NAME, 22, FG).move_to(box))
    g.row.move_to([-1.95, 0, 0])
    g.cards, g.copies = VGroup(), VGroup()
    for i, (_, n) in enumerate(MOVIES):
        fr = D.doc_card(width=0.95, height=1.2).frame
        fr.move_to([1.15 + (i % 3) * 1.1, 0.67 - (i // 3) * 1.34, 0])
        bars = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.62, height=0.08)
                        .set_stroke(width=0).set_fill(GOLD, 1)
                        .move_to(fr.get_top() + DOWN * (0.22 + 0.18 * j)) for j in range(n)])
        g.cards.add(VGroup(fr, bars))
        g.copies.add(*bars)
    g.add(g.row, g.cards)
    g.move_to(ORIGIN)
    return g


# ══ the scene ══════════════════════════════════════════════════════════════════

class Hook(NarratedScene):
    def construct(self):
        self.add(open_card())
        self.wait(0.7)
        self.clip1()
        self.clip2()
        self.clip3()

    def clip1(self):
        with self.say("c5.hook.1") as c:
            tc = title_card("Part 5 · One fact, one place")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.5, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.5, 1.4),
                        time_span(FadeIn(tc.course, shift=0.25 * DOWN), 0.6, 1.4),
                        time_span(FadeIn(tc.part, shift=0.25 * DOWN), 0.6, 1.4),
                        run_time=1.4)  # early: title card
            c.wait_until("count")

            b = bridge()
            sweep_clear(self, time_span(FadeIn(b.kid), 0.6, 1.4), time_span(FadeIn(b.chap), 0.8, 1.6),
                        run_time=1.6)
            self.play(*[GrowArrow(a) for a in b.arrows], run_time=1.0)
            c.wait_until("How many times")
            self.play(FlashAround(b.name_k, time_width=1.5), FlashAround(b.name_c, time_width=1.5),
                      run_time=1.8)
            c.wait_until("relational")

            self.sp = sp = split_frame()
            self.ps = ps = people_side()
            sweep_clear(self, time_span(FadeIn(sp.divider), 0.6, 1.4),
                        time_span(FadeIn(sp.rel, shift=0.25 * DOWN), 0.6, 1.4),
                        time_span(FadeIn(ps.card), 0.8, 1.7), run_time=1.7)
            c.wait_until("once")
            self.play(*appear(ps.one), FlashAround(ps.card.values["name"], time_width=1.5),
                      run_time=1.4)
            c.wait_until("refs")
            self.play(*appear(*ps.strips, shift=None, lag=0.15), run_time=1.5)
            c.wait_until("refers")
            n = len(ps.arrows)
            anims = [during(GrowArrow(a), 0.5 * i / (n - 1), 0.5 * i / (n - 1) + 0.5)[0]
                     for i, a in enumerate(ps.arrows)]
            self.play(*anims, *during(appear(ps.label), 0.5, 1.0), run_time=min(2.0, c.until()))
            settle(self, ps.arrows)

    def clip2(self):
        sp, ps = self.sp, self.ps
        with self.say("c5.hook.2", gap=0.8) as c:
            c.wait_until(own_word=sp.doc)
            self.play(*appear(sp.doc), run_time=1.0)
            c.wait_until("own")
            self.ds = ds = docs_side()
            self.play(*appear(ds.own, shift=None), run_time=1.2)
            c.wait_until("copies")
            self.play(*appear(*[p for cd in ds.cards for p in (cd.frame, cd.title)], shift=None,
                              lag=0.08), run_time=1.2)  # early: the six movies, counted on "six"
            # each credit row gives off a GOLD copy, which lifts clear of the strips,
            # flies to its movie's card and becomes a name tag there
            golds, ends, arcs = [], [], []
            for row, (grp, cd) in enumerate(zip(ps.strips, ds.cards)):
                for bar, tag in zip(grp, cd.tags):
                    golds.append(Dot([bar.get_x(), -0.8, 0], radius=0.075, color=GOLD))
                    ends.append(Dot(tag.get_center(), radius=0.075, color=GOLD))
                    arcs.append(0.0 if row < 3 else 0.7)
            self.play(*[FadeIn(g, shift=0.75 * UP) for g in golds], run_time=1.0)
            self.wait(0.3)
            self.play(*[Transform(g, e, path_arc=a) for g, e, a in zip(golds, ends, arcs)],
                      run_time=1.5)
            tags = [t for cd in ds.cards for t in cd.tags]
            self.play(*during([FadeOut(g) for g in golds], 0, 0.5),
                      *during([FadeIn(t, scale=0.6) for t in tags], 0.2, 1.0), run_time=0.9)
            c.wait_until("six movie")
            self.play(*appear(ds.counter), run_time=1.0)
            c.wait_until("kid")

            # The Kid's card grows; its five tags take their keys
            kid = ds.cards[0]
            others = [ds.own] + [p for cd in ds.cards[1:] for p in (cd.frame, cd.title, *cd.tags)]
            big = (RoundedRectangle(corner_radius=0.2, width=5.8, height=4.2)
                   .set_stroke(TEAL, 3).set_fill(TEAL, 0.06).move_to([RX, -0.5, 0]))
            top, left = big.get_top()[1], big.get_left()[0]
            kid.title.generate_target()
            kid.title.target.scale(32 / 20).move_to([RX, top - 0.45, 0])
            keys = []
            for i, (tag, key) in enumerate(zip(kid.tags, KEYS)):
                y = top - 1.2 - 0.6 * i
                tag.generate_target()
                tag.target.scale_to_fit_width(2.45)
                tag.target.move_to([left + 3.0 + tag.target.width / 2, y, 0])
                km = Mono(f'"{key}":', 24, FG)
                keys.append(km.move_to([left + 0.35 + km.width / 2, y, 0]))
            self.play(*during(disappear(*others), 0, 0.4),
                      *during([ReplacementTransform(kid.frame, big), MoveToTarget(kid.title),
                               *[MoveToTarget(t) for t in kid.tags]], 0.3, 1.0), run_time=2.0)
            for km, word in zip(keys, SAID):
                c.wait_until(word)
                self.play(*appear(km, shift=0.15 * RIGHT), run_time=min(0.6, max(0.3, c.until(word, nth=0))))
            c.wait_until("titles")

            # the title is copied too
            kt = _card("\n".join(['{', '  "title": "The Kid",', '  /* … */', '}']), 24, [RX, 1.85, 0],
                       yellow=['"The Kid"'])
            self.play(*during(disappear(kid.title, *kid.tags, *keys), 0, 0.45),
                      *during([ReplacementTransform(big, kt.frame)], 0.3, 0.85),
                      *during(appear(kt.code, shift=None), 0.6, 1.0), run_time=1.6)
            persons = []
            for i, nm in enumerate(ACTORS):
                fr = D.doc_card(width=1.12, height=1.0).frame
                fr.move_to([RX + (i % 5 - 2) * 1.19, -0.05 - (i // 5) * 1.2, 0])
                who = T(nm, 19, FG).move_to(fr.get_top() + DOWN * 0.27)
                cp = T("The Kid", 20, GOLD).move_to(fr.get_center() + DOWN * 0.17)
                persons.append(VGroup(fr, who, cp))
            self.play(*appear(*persons, shift=None, lag=0.08), run_time=1.6)  # early: actors' surnames, not read
            ten = T("10 people documents", 30, GOLD).move_to([RX, -2.3, 0])
            c.wait_until("own document")
            self.play(FlashAround(kt.code.find('"The Kid"'), color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("ten people")
            self.play(*appear(ten), *flash([p[2] for p in persons], color=GOLD), run_time=1.4)
            self.kt, self.persons, self.ten = kt, persons, ten

    def clip3(self):
        sp, ps, ds = self.sp, self.ps, self.ds
        with self.say("c5.hook.3", gap=1.0) as c:
            fresh = docs_side()
            parts = [fresh.own] + [p for cd in fresh.cards for p in (cd.frame, cd.title, *cd.tags)]
            self.play(*during(disappear(self.kt.frame, self.kt.code, *self.persons, self.ten), 0, 0.45),
                      *during(appear(*parts, shift=None, lag=0.01), 0.5, 1.0), run_time=1.4)
            fresh.counter = ds.counter
            q = question()
            self.play(*[dim(m) for m in _dimmables(sp, ps, fresh)], *during(appear(q), 0.3, 1.0),
                      run_time=1.6)
            c.wait_until("answer")
            self.play(*recolor(q.bug, RED), *recolor(q.feature, GREEN),
                      FlashAround(q.bug, color=RED, time_width=1.5),
                      FlashAround(q.feature, color=GREEN, time_width=1.5), run_time=1.5)
            c.wait_until()
