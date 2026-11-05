"""Chapter 4, scene 5: two kinds of document, and the copies that travel with each ID. Clips c4.shape.1 – c4.shape.3.

Exports (import with `S = load_scene("ch4_s5_shape")`; all static, no updaters):

    S.two_way(gold=True) -> VGroup, the two-way copies picture (ch5 counts on it, Lecture 5 calls back):
        .kid   The Kid's TEAL doc card (ch4 s3 doc_card, Code 20, strings FG), centre x -3.4, top y 2.2:
               movie_id, title, actors [ {person_id "nm0000122", name "Charles Chaplin", roles ["A Tramp"]},
               /* 9 more */ ]
        .chap  Chaplin's card, centre x 3.4, top y 2.2: person_id, name, acted_in [ {movie_id "tt0012349",
               title "The Kid", year 1921, roles ["A Tramp"]}, /* … */ ]
        .a1    FG arrow, The Kid's "nm0000122" -> Chaplin's card (at his person_id line)
        .a2    FG arrow, Chaplin's "tt0012349" -> The Kid's card (at its movie_id line)
        .pid_k .mid_c (the ID glyphs), .name_k .name_c, .title_k .title_c .year_c, .roles_k
        .elem_k .elem_c (lists of the element's code lines), .cross (the arrows' crossing point)
        gold=True: the copies .name_k, .title_c, .year_c are GOLD (with quotes).
    S.recap_thumb() -> two_way() scaled 0.45, centred at ORIGIN (~5.8 x 2.4), for ch4 s7's {r4}.
    S.overview() -> VGroup(.movies, .people, .ref, .back, .cap1, .cap2): slide 73 as two TEAL cards.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

D = load_scene("ch4_s3_movie")
SCH = load_scene("ch1_s2_schema")
NM, TT = "nm0000122", "tt0012349"


# ══ the two-way copies ═════════════════════════════════════════════════════════

KID_SRC = "\n".join(['{', '  "movie_id": "tt0012349",', '  "title": "The Kid",', '  "actors": [',
                     '    {', '      "person_id": "nm0000122",', '      "name": "Charles Chaplin",',
                     '      "roles": ["A Tramp"]', '    },', '    /* 9 more */', '  ]', '}'])
CHAP_SRC = "\n".join(['{', '  "person_id": "nm0000122",', '  "name": "Charles Chaplin",',
                      '  "acted_in": [', '    {', '      "movie_id": "tt0012349",',
                      '      "title": "The Kid",', '      "year": 1921,', '      "roles": ["A Tramp"]',
                      '    },', '    /* … */', '  ]', '}'])
TW_SIZE, TW_TOP, TW_X = 20, 2.2, 3.4


def _plain(code):
    """String values FG (the lexer makes every string GOLD; here GOLD means 'a copy')."""
    gold = ManimColor(GOLD).to_hex().lower()
    for g in code.text.submobjects:
        if g.get_fill_color().to_hex().lower() == gold:
            g.set_color(FG)
    return code


def _card(src, x):
    card = D.doc_card(src, size=TW_SIZE)
    _plain(card.code)
    card.move_to([x, 0, 0])
    card.shift(UP * (TW_TOP - card.get_top()[1]))
    return card


def _cross(p1, p2, q1, q2):
    d1, d2 = p2 - p1, q2 - q1
    m = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
    t = np.linalg.solve(m, (q1 - p1)[:2])[0]
    return p1 + t * d1


def two_way(gold=True):
    g = VGroup()
    k, c = _card(KID_SRC, -TW_X), _card(CHAP_SRC, TW_X)
    g.kid, g.chap = k, c
    g.pid_k = k.code.find(f'"{NM}"')
    g.mid_c = c.code.find(f'"{TT}"')
    g.name_k = k.code.find('"Charles Chaplin"')
    g.name_c = c.code.find('"Charles Chaplin"')
    g.title_k = k.code.find('"The Kid"')
    g.title_c = c.code.find('"The Kid"')
    g.year_c = c.code.find("1921")
    g.roles_k = k.code.find("A Tramp")
    g.elem_k = [k.code.line(i) for i in range(4, 9)]
    g.elem_c = [c.code.line(i) for i in range(4, 10)]
    p1 = np.array([g.pid_k.get_right()[0] + 0.05, g.pid_k.get_y(), 0])
    p2 = np.array([c.frame.get_left()[0], c.code.line(1).get_y(), 0])
    q1 = np.array([c.frame.get_left()[0], g.mid_c.get_y(), 0])
    q2 = np.array([k.frame.get_right()[0], k.code.line(1).get_y(), 0])
    g.a1 = Arrow(p1, p2, buff=0.04, stroke_width=3, color=FG, tip_length=0.18)
    g.a2 = Arrow(q1, q2, buff=0.04, stroke_width=3, color=FG, tip_length=0.18)
    g.cross = _cross(p1, p2, q1, q2)
    if gold:
        for m in (g.name_k, g.title_c, g.year_c):
            m.set_color(GOLD)
    g.add(k, c, g.a1, g.a2)
    return g


def recap_thumb():
    return two_way().scale(0.45).move_to(ORIGIN)


# ══ slide 73: the two kinds of document ════════════════════════════════════════

OV_FS, OV_P, OV_W, OV_TOP, OV_X = 22, 0.36, 4.9, 3.5, 3.4
MOVIE_ROWS = [("movie_id, title, year", None), ("type, minutes", None), ("rating, rating_votes", None),
              ("genres: [string, ...]", None), ("actors: [", None),
              ("person_id", "a"), ("name", "a"), ("roles: [...]", "a"),
              ("directors, producers,", None), ("writers, composers: [", None),
              ("person_id", "c"), ("name, job", "c"),
              ("trivia_entries:", None), ("  [string, ...]", None)]
PEOPLE_ROWS = [("person_id, name", None), ("birthyear, deathyear", None), ("acted_in: [", None),
               ("movie_id", "a"), ("title, year", "a"), ("roles: [...]", "a"),
               ("directed, produced,", None), ("wrote, composed_for: [", None),
               ("movie_id", "c"), ("title, year", "c"), ("job", "c")]


def _ov_card(name, sub, rows, cx, key):
    g = VGroup()
    L = cx - OV_W / 2
    top = OV_TOP
    head = VGroup(Mono(name, 30, TEAL, weight=BOLD), T(sub, 28, DIM)).arrange(RIGHT, buff=0.25)
    head.move_to([cx, top - 0.38, 0])
    g.head_y = top - 0.38
    div = Line([L, top - 0.75, 0], [L + OV_W, top - 0.75, 0]).set_stroke(TEAL, 2, opacity=0.6)
    y = top - 0.75 - 0.32
    texts, boxes, prev = [], {}, None
    for i, (s, box) in enumerate(rows):
        if i and box != prev:
            y -= 0.08
        t, bot = SCH._placed(s.strip(), OV_FS, FG, NORMAL, y,
                             left=L + (0.55 if box or s.startswith(" ") else 0.3))
        t.bot = bot
        texts.append(t)
        if box:
            boxes.setdefault(box, []).append(t)
        prev = box
        y -= OV_P
    h = top - (y + OV_P - 0.32)
    frame = D._frame(OV_W, h).move_to([cx, top - h / 2, 0])
    rects, closers = [], []
    for b, ts in boxes.items():
        right = max(t.get_right()[0] for t in ts) + 0.2
        left = L + 0.38
        hi, lo = ts[0].get_y() + 0.2, ts[-1].get_y() - 0.2
        r = (RoundedRectangle(corner_radius=0.1, width=right - left, height=hi - lo)
             .set_stroke(TEAL, 2).set_fill(TEAL, 0).move_to([(left + right) / 2, (hi + lo) / 2, 0]))
        rects.append(r)
        cl, _ = SCH._placed("]", OV_FS, FG, NORMAL, ts[-1].get_y(), left=right + 0.1)
        closers.append(cl)
    t0 = texts[0]
    kg = select(t0, key)[0]
    ul = Line([kg.get_left()[0], t0.bot + 0.02, 0], [kg.get_right()[0], t0.bot + 0.02, 0]).set_stroke(FG, 2.5)
    g.frame, g.head, g.div, g.rows, g.boxes, g.rects, g.closers, g.ul = (
        frame, head, div, texts, boxes, rects, closers, ul)
    g.content = [head, div, *texts, ul, *rects, *closers]
    g.add(frame, *g.content)
    return g


def _fk(points, color=FG):
    return SCH._fk([(x, y, 0) for x, y in points], color)


def overview():
    g = VGroup()
    m = _ov_card("movies", "one per movie", MOVIE_ROWS, -OV_X, "movie_id")
    p = _ov_card("people", "one per person", PEOPLE_ROWS, OV_X, "person_id")
    g.movies, g.people = m, p
    ref, back = [], []
    for b in ("a", "c"):
        t = m.boxes[b][0]
        y = t.get_y()
        ref.append(_fk([(t.get_right()[0] + 0.1, y), (-0.25, y), (-0.25, p.head_y + 0.1),
                        (p.frame.get_left()[0], p.head_y + 0.1)]))
        t = p.boxes[b][0]
        y = t.get_y()
        back.append(_fk([(t.get_left()[0] - 0.1, y), (0.25, y), (0.25, m.head_y - 0.1),
                         (m.frame.get_right()[0], m.head_y - 0.1)]))
    g.ref, g.back = ref, back
    cap1 = T("Arrows: references by ID.", 28, DIM)
    cap2 = T("Names and titles are also copied.", 28, DIM)
    VGroup(cap1, cap2).arrange(RIGHT, buff=0.22).move_to([0, -3.42, 0])
    g.cap1, g.cap2 = cap1, cap2
    g.copied = ([select(m.boxes[b][1], "name")[0] for b in ("a", "c")]
                + [select(p.boxes[b][1], w)[0] for b in ("a", "c") for w in ("title", "year")])
    g.add(m, p, *ref, *back, cap1, cap2)
    return g


# ══ plays_role's one row ═══════════════════════════════════════════════════════

def plays_role_card():
    g = VGroup()
    vals = [Mono(v, 26) for v in (NM, TT, "A Tramp")]
    ws = [v.width + 0.5 for v in vals]
    w, hh, rh = sum(ws), 0.5, 0.55
    top = 3.5
    box = Rectangle(width=w, height=hh + rh).set_stroke(BLUE, 3).move_to([0, top - (hh + rh) / 2, 0])
    header = Rectangle(width=w, height=hh).set_stroke(BLUE, 0).set_fill(BLUE, 0).move_to([0, top - hh / 2, 0])
    div = Line([-w / 2, top - hh, 0], [w / 2, top - hh, 0]).set_stroke(BLUE, 2)
    title, _ = SCH._placed("plays_role", 28, FG, BOLD, top - hh / 2, cx=0)
    ry = top - hh - rh / 2
    strip = Rectangle(width=w - 0.1, height=rh - 0.1).set_stroke(BLUE, 0).set_fill(BLUE, 0.3)
    strip.move_to([0, ry, 0])
    x = -w / 2
    seps = []
    for i, (v, cw) in enumerate(zip(vals, ws)):
        v.move_to([x + cw / 2, ry, 0])
        x += cw
        if i < 2:
            seps.append(Line([x, top - hh, 0], [x, top - hh - rh, 0]).set_stroke(BLUE, 2))
    g.box, g.strip, g.vals, g.title = box, strip, vals, title
    g.add(header, strip, box, div, *seps, title, *vals)
    return g


def _elem_box(lines, frame):
    left = min(l.get_left()[0] for l in lines) - 0.14
    right = max(max(l.get_right()[0] for l in lines) + 0.08, frame.get_right()[0] - 0.12)
    hi = lines[0].get_top()[1] + 0.08
    lo = lines[-1].get_bottom()[1] - 0.08
    r = (RoundedRectangle(corner_radius=0.08, width=right - left, height=hi - lo)
         .set_stroke(BLUE, 3).set_fill(BLUE, 0.12).move_to([(left + right) / 2, (hi + lo) / 2, 0]))
    r.set_z_index(-1)
    return r


# ══ the scene ══════════════════════════════════════════════════════════════════

class Shape(NarratedScene):
    def construct(self):
        ov = overview()
        m, p = ov.movies, ov.people

        # ---- clip 1: the shape of the whole database ----
        with self.say("c4.shape.1") as c:
            self.play(*appear(m.frame, p.frame, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("movies")
            rt = min(2.7, c.until("ref"))
            self.play(*during(appear(*m.content, shift=None, lag=0.06), 0, 0.6),
                      *during(appear(*p.content, shift=None, lag=0.06), 0.35, 1),
                      run_time=rt)
            c.wait_until("ref")
            self.play(*[Create(a) for a in ov.ref], run_time=1.8)
            self.play(FlashAround(p.head, run_time=1.2, time_width=1.5))
            self.play(*appear(ov.cap1), run_time=1.0)   # early: the slide's caption, read as the arrows land
            c.wait_until("back")
            self.play(*[Create(a) for a in ov.back], run_time=1.5)
            self.play(FlashAround(m.head, run_time=1.0, time_width=1.5))
            self.play(*appear(ov.cap2), run_time=min(1.0, c.until()))   # early: the slide's caption, read before the copies turn GOLD

        # ---- clip 2: what travels with each ID ----
        tw = two_way(gold=False)
        with self.say("c4.shape.2") as c:
            self.play(*recolor(ov.copied, GOLD), run_time=1.2)
            self.play(*flash(ov.copied, color=GOLD, run_time=1.2, time_width=1.5))
            c.wait_until("name")
            old = list(self.mobjects)
            self.play(*during(disappear(*old), 0, 0.45),
                      *during(appear(tw.kid, tw.chap, shift=None, lag=0.15), 0.5, 1), run_time=1.6)
            self.play(FlashAround(tw.pid_k, run_time=1.2, time_width=1.5), GrowArrow(tw.a1), run_time=1.3)
            c.wait_until("It also keeps")
            self.play(FlashAround(tw.name_c, run_time=1.0, time_width=1.5), run_time=1.0)
            self.play(*recolor(tw.name_k, GOLD), FlashAround(tw.name_k, color=GOLD, time_width=1.5),
                      run_time=1.3)
            c.wait_until("title")
            self.play(FlashAround(tw.mid_c, run_time=1.2, time_width=1.5), GrowArrow(tw.a2), run_time=1.3)
            c.wait_until("It also keeps", nth=1)
            self.play(FlashAround(tw.title_k, run_time=1.0, time_width=1.5), run_time=1.0)
            self.play(*recolor(tw.title_c, GOLD), *recolor(tw.year_c, GOLD),
                      FlashAround(tw.title_c, color=GOLD, time_width=1.5),
                      FlashAround(tw.year_c, color=GOLD, time_width=1.5), run_time=1.3)
            c.wait_until("why")
            q = T("Why copy them?", 40, YELLOW).move_to([0, 3.0, 0])
            self.play(*appear(q), run_time=1.0)
            c.wait_until("own")
            ans = T("So each document is useful on its own.", 36, FG).move_to([0, 3.0, 0])
            self.play(*swap(q, ans), run_time=1.2)
            H = load_scene("ch4_s1_hook")
            page = H.mock_page()
            title = T("The Kid (1921)", 36)
            block = VGroup(page.cast_head, *page.cast_rows, page.more)
            title.next_to(page.cast_head, UP, buff=0.4, aligned_edge=LEFT)
            block.add(title)
            row0 = page.cast_rows[0]
            block.shift(RIGHT * (1.0 - block.get_left()[0])
                        + UP * (tw.roles_k.get_y() - row0.role.get_y()))
            frame = (RoundedRectangle(corner_radius=0.15, width=block.width + 0.7, height=block.height + 0.6)
                     .set_stroke(DIM, 2).set_fill(FG, 0.03).move_to(block))
            view = VGroup(frame, title, page.cast_head, *page.cast_rows[1:], page.more)
            self.play(*during(disappear(tw.chap, tw.a1, tw.a2), 0, 0.45),   # early: the page shown whole, its cast read next
                      *during(appear(view, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("The movie page")
            self.play(*flash([tw.name_k, tw.roles_k], run_time=1.2, time_width=1.5),   # early: the cast list, read as a whole
                      *during(appear(row0.actor, row0.role, shift=None, lag=0.3), 0.35, 1), run_time=1.8)

        # ---- clip 3: one fact, stored twice ----
        pr = plays_role_card()
        bk, bc = _elem_box(tw.elem_k, tw.kid.frame), _elem_box(tw.elem_c, tw.chap.frame)
        x2 = set_backstroke(T("×2", 44, TEAL, weight=BOLD)).move_to(
            [(tw.kid.frame.get_right()[0] + tw.chap.frame.get_left()[0]) / 2, tw.cross[1], 0])
        cap = T("Each movie–person relationship is stored twice, once in each direction.", 28, FG)
        cap.move_to([0, 3.0, 0])
        with self.say("c4.shape.3") as c:
            c.wait_until("playsrole")
            self.play(*during(disappear(view, row0.actor, row0.role, ans), 0, 0.45),
                      *during(appear(tw.chap, tw.a1, tw.a2, shift=None, lag=0.1), 0.5, 1), run_time=1.6)
            self.play(*appear(pr, shift=None), run_time=1.2)
            c.wait_until("split")
            self.play(FlashAround(pr.strip, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("inmovie")
            self.play(ReplacementTransform(pr.strip.copy(), bk), run_time=1.6)
            c.wait_until("inperson")
            self.play(ReplacementTransform(pr.strip.copy(), bc), run_time=1.6)
            self.play(*disappear(pr), run_time=1.0)
            c.wait_until("twice")
            self.play(*appear(x2, cap, shift=None, lag=0.4), run_time=1.4)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
