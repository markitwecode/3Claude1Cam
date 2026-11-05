"""Chapter 9, scene 8: Exercise 16, what's different. Clips c9.compare.1 – c9.compare.4.

Opens on s7's handover shot (our generated The Kid, left). The JSON database's The Kid joins it on
the right; same facts (✓ ✓, GOLD 2,935); the billing order (crossing name lines, has_position card,
GOLD 6); Flow (null vs a missing key; the LEFT JOIN plan's phantom actor, s3's padded row); the
JSON's extra keys, the subqueries that could add them, trivia_entries with no table; ch5 s6's
source-of-truth arrow. Ends on an empty frame.

EXPORTS (static; `load_scene("ch9_s8_compare").<name>()`):
- recap_marks(): VGroup `.same` (GREEN ✓ + T 32 GREEN "same facts") over `.trivia` (Mono 26 RED
  "trivia_entries" + RED ✗), left-aligned, centred at ORIGIN.
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

S7 = load_scene("ch9_s7_build")
D = load_scene("ch4_s3_movie")
SCH = load_scene("ch1_s2_schema")
R5 = load_scene("ch5_s6_why")
S3 = load_scene("ch9_s3_left")

JSON_KID = "\n".join([
    "{", '  "movie_id": "tt0012349",', '  "title": "The Kid",', '  "year": 1921,',
    '  "type": "movie", "minutes": 68,',
    '  "genres": [', '    "Comedy", "Drama", "Family"', "  ],",
    '  "rating": 8.2, "rating_votes": 142991,',
    '  "actors": [',
    '    {"name": "Charles Chaplin", …},',
    '    {"name": "Edna Purviance", …},',
    '    {"name": "Jackie Coogan", …},',
    "    /* 7 more */", "  ],",
    '  /* 4 crew lists */',
    '  "trivia_entries": [/* 5 items */ ]', "}"])

FLOW_DOC = "\n".join([
    "{", '  "movie_id": "tt4772188",', '  "title": "Flow",', '  "year": 2024,',
    '  "genres": [', '    "Adventure", "Animation", "Family"', "  ],",
    '  "actors": null', "}"])

PATCH_SRC = """SELECT json_object('movie_id', m.movie_id,
                   'title', m.title, 'year', m.year,
                   'genres', list(DISTINCT g.name),
                   'actors', list(DISTINCT json_object(
                       'person_id', p.person_id, 'name', p.name)))
FROM movies AS m
LEFT JOIN has_genre AS hg ON hg.movie_id = m.movie_id
LEFT JOIN genres AS g ON g.genre_id = hg.genre_id
LEFT JOIN has_position AS hp ON hp.movie_id = m.movie_id
                            AND hp.position = 'actor'
LEFT JOIN people AS p ON p.person_id = hp.person_id
GROUP BY m.movie_id, m.title, m.year;"""
GHOST = '"actors":[{"person_id":null,"name":null}]'

KID_KEYS = ["movie_id", "title", "year", "type", "minutes", "genres", "rating", "rating_votes",
            "actors", "directors", "producers", "writers", "composers", "trivia_entries"]
BUILT = ("movie_id", "title", "year", "genres", "actors")
KEY_SIZE, KEY_X, KEY_TOP, KEY_PITCH = 28, 2.6, 2.75, 0.43
KEY_HEAD_Y = 3.45
MAP_K, MAP_C = 0.6, np.array([-2.9, 0.45, 0])

L_SCALE, CARD_Y = 0.8, 0.45
R_SIZE = 17


# ---------------------------------------------------------------- exports
def recap_marks():
    same = VGroup(check_mark(GREEN), T("same facts", 32, GREEN)).arrange(RIGHT, buff=0.25)
    triv = VGroup(Mono("trivia_entries", KEY_SIZE, RED), cross_mark()).arrange(RIGHT, buff=0.3)
    g = VGroup(same, triv).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(ORIGIN)
    g.same, g.trivia = same, triv
    return g


# ---------------------------------------------------------------- pieces
def key_slot(i):
    return KEY_TOP - i * KEY_PITCH


def key_column(names, color=FG):
    """Mono keys at the fixed slots of KID_KEYS (a missing key leaves its slot empty)."""
    out = {}
    for k in names:
        t = SCH._placed(k, KEY_SIZE, color, NORMAL, key_slot(KID_KEYS.index(k)), left=KEY_X)[0]
        out[k] = t
    return out


def right_card():
    card = D.doc_card(JSON_KID, size=R_SIZE)
    for g in chars(card.code, "…"):
        g.set_color(DIM)
    return card


class Ch9S8Compare(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ same facts
    def clip1(self):
        shot = S7.handover_shot()
        self.add(shot)
        kid = shot[0]
        with self.say("c9.compare.1") as c:
            shot.generate_target()
            shot.target.scale(L_SCALE)
            lw = shot.target.width
            rc = right_card()
            gap = 1.2
            total = lw + gap + rc.width
            x0 = -total / 2
            shot.target.move_to([x0 + lw / 2, CARD_Y, 0])
            rc.move_to([x0 + lw + gap + rc.width / 2, CARD_Y, 0])
            gx = x0 + lw + gap / 2
            self.play(MoveToTarget(shot), *during(appear(rc, shift=None), 0.4, 1), run_time=1.6)
            self.kid, self.rc = kid, rc

            c.wait_until("same")
            lg, rg = kid.code.line(5), rc.code.line(6)
            la = VGroup(*[kid.code.line(i) for i in range(8, 14)])
            ra = VGroup(*[rc.code.line(i) for i in range(10, 13)])
            ck1 = check_mark(GREEN).move_to([gx, (lg.get_y() + rg.get_y()) / 2, 0])
            ck2 = check_mark(GREEN).move_to([gx, (la.get_y() + ra.get_y()) / 2, 0])
            self.play(*flash([lg, rg, la, ra], color=GREEN, time_width=1.5), run_time=1.4)
            self.play(*appear(ck1, ck2, shift=None, lag=0.3), run_time=1.0)

            c.wait_until("for all")
            fact = T("2,935 of 2,935 movies: same genres, same set of actors", 32, GOLD)
            fact.move_to([0, -3.0, 0])
            self.play(*appear(fact), run_time=1.0)  # early: the count is said as "two thousand…" first
            self.checks, self.fact = [ck1, ck2], fact

    # ------------------------------------------------------------ billing order
    def clip2(self):
        with self.say("c9.compare.2", gap=0.9) as c:
            ys = [2.3, 1.5, 0.7, -0.1]
            xl, xr = -1.3, 1.3
            h_ours = T("ours", 32, DIM).move_to([-3.3, 3.2, 0])
            h_json = T("JSON database (billing order)", 32, DIM).move_to([3.3, 3.2, 0])

            def name(s, i, left):
                t = Mono(s, 32, DIM if s == "…" else FG).move_to([0, ys[i], 0])
                return t.align_to([xl, 0, 0], RIGHT) if left else t.align_to([xr, 0, 0], LEFT)

            ours = [name(s, i, True) for i, s in enumerate(["Charles Chaplin", "Jackie Coogan",
                                                             "Albert Austin", "…"])]
            jsn = [name(s, i, False) for i, s in enumerate(["Charles Chaplin", "Edna Purviance",
                                                             "Jackie Coogan", "…"])]
            sweep_clear(self, *during(appear(h_ours, h_json, shift=None), 0.5, 1), keep=[self.fact], run_time=1.4)  # early: column headings

            for t in jsn[:3]:
                c.wait_until(own_word=t)
                self.play(*appear(t, shift=None), run_time=0.7)
            self.play(*appear(jsn[3], shift=None), run_time=0.5)

            c.wait_until("ours came out")
            self.play(*appear(*ours, shift=None, lag=0.25), run_time=1.3)  # early: our order, shown whole

            def ln(i, j, color):
                return Line([xl + 0.15, ys[i], 0], [xr - 0.15, ys[j], 0]).set_stroke(color, 4)

            lines = [ln(0, 0, GREEN), ln(1, 2, YELLOW), ln(2, 3, YELLOW), ln(3, 1, YELLOW)]
            c.wait_until("found the rows")
            self.play(*[Create(x) for x in lines], run_time=1.5)

            c.wait_until("noorder")
            hp = SCH.schema_map().cards["has_position"]
            hp.move_to([-4.3, -2.2, 0])
            tag = T("no billing order", 30, DIM).next_to(hp, RIGHT, buff=0.4)
            self.play(*during(disappear(self.fact), 0, 0.45),
                      *during(appear(hp, shift=None), 0.45, 1), run_time=1.4)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=0.9)

            c.wait_until("only six")
            six = T("same order: 6 movies", 34, GOLD).move_to([3.9, -2.2, 0])
            self.play(*appear(six), run_time=1.0)  # early: "six" is said before "same order"
            self.board2 = [h_ours, h_json, *ours, *jsn, *lines, hp, tag, six]

    # ------------------------------------------------------------ Flow
    def clip3(self):
        with self.say("c9.compare.3") as c:
            flow = D.doc_card(FLOW_DOC, size=24)
            flow.move_to([-2.85, 0, 0])
            h_flow = T("ours", 30, DIM).next_to(flow, UP, buff=0.3)
            keys = key_column([k for k in KID_KEYS if k != "actors"])
            col = list(keys.values())
            head = T("JSON database", 30, DIM).move_to([KEY_X + 1.5, KEY_HEAD_Y, 0])
            c.wait_until("flow")
            sweep_clear(self, *during(appear(flow, h_flow, shift=None), 0.5, 1), run_time=1.4)
            self.play(*appear(head, *col, shift=None, lag=0.04), run_time=1.2)  # early: the key list shown whole

            c.wait_until("genre")
            self.play(*flash([flow.code.line(5)], color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until("comes out null")
            nul = flow.code.find("null")
            self.play(FlashAround(nul, color=PINK, time_width=1.5), run_time=1.2)

            c.wait_until("leaves the key out")
            hole = DashedVMobject(Rectangle(width=1.6, height=0.36), num_dashes=18)
            hole.set_stroke(DIM, 2).move_to([0, key_slot(8), 0]).align_to([KEY_X - 0.08, 0, 0], LEFT)
            self.play(FadeIn(hole), run_time=1.0)
            self.board3a = [flow, h_flow, head, *col, hole]

            c.wait_until("phantom")
            code = Code(PATCH_SRC, size=21)
            code.move_to([0, 0, 0]).align_to([0, 3.55, 0], UP)
            sweep_clear(self, *during(appear(code, shift=None), 0.5, 1), run_time=1.4)
            c.wait_until("left joins")
            hits = [code.find("LEFT JOIN", nth=k) for k in range(4)] + \
                   [code.find("DISTINCT", nth=k) for k in range(2)]
            self.play(*[a for h in hits for a in recolor(h, YELLOW)],
                      *flash(hits, time_width=1.5), run_time=1.4)

            c.wait_until("phantom actor")
            ghost = D.json_code(GHOST, size=28)
            ghost.move_to([-1.4, -2.05, 0])
            obj = ghost.find('{"person_id":null,"name":null}')
            box = DashedVMobject(SurroundingRectangle(obj, buff=0.07, corner_radius=0.1),
                                 num_dashes=40).set_stroke(PINK, 2.5)
            plab = T("phantom actor", 30, PINK).next_to(box, DOWN, buff=0.25)
            self.play(*appear(ghost, shift=None), run_time=1.0)
            self.play(FadeIn(box), *appear(plab), run_time=1.0)
            c.wait_until("null id")
            self.play(*flash([ghost.find("null", nth=0), ghost.find("null", nth=1)], color=PINK,
                             time_width=1.5), run_time=1.2)

            c.wait_until("its pair")
            row = S3.padded_row()
            if row.width > 3.6:
                row.scale_to_fit_width(3.6)
            row.move_to([4.6, -2.9, 0])
            self.play(*appear(row, shift=None), run_time=0.9)
            self.play(FlashAround(row, color=PINK, time_width=1.5), run_time=1.2)

    # ------------------------------------------------------------ more, trivia, truth
    def clip4(self):
        with self.say("c9.compare.4") as c:
            keys = key_column(KID_KEYS)
            for k, t in keys.items():
                t.set_color(GREEN if k in BUILT else DIM)
            col = list(keys.values())
            head = T("JSON database: The Kid", 30, DIM).move_to([KEY_X + 1.5, KEY_HEAD_Y, 0])
            m = R5.source_map(MAP_K).move_to(MAP_C)
            c.wait_until("hold more")
            sweep_clear(self, *during(appear(m, head, *col, shift=None, lag=0.03), 0.5, 1), run_time=1.6)  # early: list shown whole

            roles = Mono("+ roles", KEY_SIZE, DIM).next_to(keys["actors"], RIGHT, buff=0.25)
            for cue, ks in [("type", ["type", "minutes"]), ("rating", ["rating", "rating_votes"])]:
                c.wait_until(cue)
                self.play(*flash([keys[k] for k in ks], time_width=1.5), run_time=1.0)
            c.wait_until("roles")
            self.play(*appear(roles), run_time=0.8)
            c.wait_until("crew")
            crew = ["directors", "producers", "writers", "composers"]
            self.play(*flash([keys[k] for k in crew], time_width=1.5), run_time=1.0)

            c.wait_until("add")
            cd = m.cards
            pairs = [("movies", "type"), ("movies", "minutes"), ("ratings", "rating"),
                     ("ratings", "rating_votes"), ("plays_role", None)] + [("has_position", k) for k in crew]
            flashes, greens = [], []
            for i, (card, k) in enumerate(pairs):
                tgt = roles if k is None else keys[k]
                src = cd[card].box.get_right() + LEFT * 0.05
                path = ArcBetweenPoints(src, tgt.get_left() + LEFT * 0.12, angle=-0.35)
                path.set_stroke(GREEN, 4)
                t0 = 0.04 * i
                flashes += during(VShowPassingFlash(path, time_width=0.6), t0, t0 + 0.55)
                greens += during(recolor(tgt, GREEN), t0 + 0.45, t0 + 0.65)
            self.play(*flashes, *greens, run_time=2.0)

            c.wait_until("trivia")
            tr = keys["trivia_entries"]
            self.play(*recolor(tr, RED), FlashAround(tr, color=RED, time_width=1.5), run_time=1.2)
            c.wait_until("no query")
            hole = DashedVMobject(Rectangle(width=1.9, height=1.0), num_dashes=28).set_stroke(DIM, 2.5)
            hole.move_to([-1.6, tr.get_y(), 0])
            reach = DashedLine(tr.get_left() + LEFT * 0.15, hole.get_right() + RIGHT * 0.1,
                               dash_length=0.12).set_stroke(RED, 3)
            x = cross_mark().move_to(hole)
            self.play(Create(reach), FadeIn(hole), run_time=1.2)
            self.play(FadeIn(x, scale=0.6), run_time=0.7)

            c.wait_until("truth")
            r5 = R5.recap_r5()
            m.generate_target()
            m.target.scale(0.42 / MAP_K).move_to(r5.map)
            marks = recap_marks()
            ttgt = marks.trivia.copy().move_to([3.95, -2.75, 0])
            others = [k for k in col if k is not tr] + [roles, head]
            self.play(*during(disappear(*others, hole, reach), 0, 0.45),
                      *during([MoveToTarget(m), tr.animate.move_to(ttgt[0]),
                               x.animate.move_to(ttgt[1])], 0.2, 1), run_time=1.8)
            c.wait_until("documents derived")
            self.play(GrowArrow(r5.arrow), *appear(r5.query), *during(appear(r5.stack, shift=None), 0.3, 1),
                      run_time=1.6)
            c.wait_until("source of truth")
            self.play(*appear(r5.source), run_time=1.0)
            c.wait_until("except the trivia")
            self.play(FlashAround(VGroup(tr, x), color=RED, time_width=1.5), run_time=1.2)
        self.wait(3.0)
