"""Chapter 2, scene 2: asking about absence (LEFT JOIN ... IS NULL, and EXCEPT). Clips c2.absent.1 – c2.absent.3."""
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
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- shared pieces (chapter-wide)

def movie_card(title, year, size=32, color=BLUE, min_width=3.0):
    """The chapter's movie card: BLUE rounded box, FG title, DIM dot, GOLD year ("Flow · 2024").
    ~3.0 x 0.8 at the default size; wider for long titles. Parts: .box .title .dot .year .label"""
    t = T(title, size, FG)
    d = T("·", size, DIM)
    y = T(str(year), size, GOLD)
    label = VGroup(t, d, y).arrange(RIGHT, buff=0.16)
    y.align_to(t, DOWN)
    d.move_to([d.get_x(), t.get_y(), 0])
    box = RoundedRectangle(corner_radius=0.16, width=max(min_width, label.width + 0.6),
                           height=0.8 * size / 32)
    box.set_stroke(color, 3).set_fill(BG, 1)
    label.move_to(box)
    card = VGroup(box, label)
    card.box, card.title, card.dot, card.year, card.label = box, t, d, y, label
    return card


LEFTJOIN_SRC = """SELECT m.movie_id, m.title
FROM movies AS m
LEFT JOIN plays_role AS r
  ON m.movie_id = r.movie_id
WHERE r.movie_id IS NULL;"""

EXCEPT_SRC = """SELECT movie_id, title
FROM movies
EXCEPT
SELECT movie_id, title
FROM movies JOIN plays_role
  USING (movie_id);"""


def leftjoin_query(size=28):
    return Code(LEFTJOIN_SRC, size=size, lang="sql")


def except_query(size=28):
    return Code(EXCEPT_SRC, size=size, lang="sql")


CAPTION_Y = 3.4
PARK_SCALE = 0.875          # card text 28
FLOW_PARK = np.array([5.3, 3.3, 0])
KAIVA_PARK = np.array([5.3, 2.5, 0])


def top_caption():
    return T("Which movies have no actors?", 40, YELLOW).move_to([0, CAPTION_Y, 0])


def parked_cards():
    flow = movie_card("Flow", 2024).scale(PARK_SCALE).move_to(FLOW_PARK)
    kaiva = movie_card("Kaiva", 2023).scale(PARK_SCALE).move_to(KAIVA_PARK)
    return flow, kaiva


def handover_shot():
    """Last frame: the caption and the two parked cards (s3 opens on it)."""
    flow, kaiva = parked_cards()
    return VGroup(top_caption(), flow, kaiva)


# ---------------------------------------------------------------- scene-local helpers

def cell(content, w, h=0.6, color=BLUE, center=ORIGIN):
    r = Rectangle(width=w, height=h).set_stroke(color, 2).set_fill(BG, 0)
    r.move_to(center)
    content.move_to(r)
    g = VGroup(r, content)
    g.rect, g.content = r, content
    return g


COLS = [(0.95, 1.6), (3.0, 2.5), (5.35, 2.2)]   # (centre x, width): title | r.movie_id | r.role


def join_row(title, rid, role, y, rid_color=FG, role_color=FG):
    rid_mob = Mono(rid, 28, rid_color)
    role_mob = Mono(role, 28, role_color) if role == "NULL" else T(role, 28, role_color)
    cells = [cell(T(title, 28), COLS[0][1], center=[COLS[0][0], y, 0]),
             cell(rid_mob, COLS[1][1], center=[COLS[1][0], y, 0]),
             cell(role_mob, COLS[2][1], center=[COLS[2][0], y, 0])]
    return cells


class AbsentScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.finale()

    # ------------------------------------------------------------ clip 1
    def clip1(self):
        with self.say("c2.absent.1") as c:
            cap = top_caption()
            self.cap = cap
            c.wait_until("Which movies")
            self.play(*appear(cap), run_time=1.0)  # early: the caption is the question being asked
            c.wait_until("two")
            flow = movie_card("Flow", 2024).scale(1.3).move_to([-2.4, -0.2, 0])
            kaiva = movie_card("Kaiva", 2023).scale(1.3).move_to([2.4, -0.2, 0])
            self.flow, self.kaiva = flow, kaiva
            self.play(*appear(flow, kaiva, lag=0.3), run_time=1.2)  # early: "two movies" is their cue
            c.wait_until("Flow")
            self.play(FlashAround(flow, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("and Kaiva")
            self.play(FlashAround(kaiva, color=YELLOW, time_width=1.5), run_time=1.2)

            c.wait_until("hard")
            self.play(flow.animate.scale(PARK_SCALE / 1.3).move_to(FLOW_PARK),
                      kaiva.animate.scale(PARK_SCALE / 1.3).move_to(KAIVA_PARK), run_time=1.0)

            # rows that are there, and the one that isn't
            head = Mono("plays_role", 32, DIM).move_to([0, 2.05, 0])
            ys = [1.2, 0.35, -0.5, -1.35]
            texts = ["The Kid · A Tramp", "The Kid · The Child", None, "The Kid · The Woman"]
            rows, slot = [], None
            for y, s in zip(ys, texts):
                if s is None:
                    r = Rectangle(width=6.4, height=0.7).move_to([0, y, 0])
                    slot = DashedVMobject(r.set_stroke(DIM, 2), num_dashes=40)
                    continue
                rows.append(cell(T(s, 34, t2c={"·": DIM}), 6.4, h=0.7, color=BLUE, center=[0, y, 0]))
            note = T("no row for Flow", 30, DIM, slant=ITALIC).next_to(slot, RIGHT, buff=0.3)
            bar = Line([-3.6, 0, 0], [3.6, 0, 0]).set_stroke(YELLOW, 4)
            where = Mono("WHERE", 32, YELLOW).next_to(bar, LEFT, buff=0.2)
            filt = VGroup(bar, where).move_to([-0.6, 1.7, 0])
            self.play(*appear(head, *rows, slot, note, filt, lag=0.12), run_time=1.2)
            T_SW = 2.4
            y0, y1 = 1.7, -1.9
            lights = []
            for r in rows:
                f = (y0 - r.get_y()) / (y0 - y1)
                lights.append(time_span(r.rect.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.18),
                                        f * T_SW, min(T_SW, f * T_SW + 0.35)))
            self.play(filt.animate.shift((y1 - y0) * UP), *lights, run_time=T_SW, rate_func=linear)

            c.wait_until("earlier")
            lj = Mono("LEFT JOIN", 36, DIM).move_to([-2.2, -2.85, 0])
            ex = Mono("EXCEPT", 36, DIM).move_to([2.2, -2.85, 0])
            self.lj, self.ex = lj, ex
            self.filter_shot = [head, *rows, slot, note, filt]
            self.play(*appear(lj, ex, lag=0.4), run_time=1.0)

    # ------------------------------------------------------------ clip 2
    def clip2(self):
        with self.say("c2.absent.2") as c:
            q = leftjoin_query()
            q.to_edge(LEFT, buff=0.4).move_to([q.get_x(), -0.45, 0])
            self.q1 = q
            self.play(*during(disappear(*self.filter_shot), 0, 0.4),
                      *during([self.lj.animate.scale(30 / 36).next_to(q, UP, buff=0.35, aligned_edge=LEFT)],
                              0.4, 1), run_time=1.2)
            self.play(*appear(q, shift=None), run_time=1.0)

            # movies rows: every movie survives
            c.wait_until("pad")
            heads = [Mono(s, 28, DIM).move_to([x, 1.2, 0])
                     for s, (x, _) in zip(["title", "r.movie_id", "r.role"], COLS)]
            kid = cell(T("The Kid", 28), COLS[0][1], center=[COLS[0][0], 0.6, 0])
            flow = cell(T("Flow", 28), COLS[0][1], center=[COLS[0][0], 0.0, 0])
            kaiva = cell(T("Kaiva", 28), COLS[0][1], center=[COLS[0][0], -0.6, 0])
            self.play(*appear(heads[0], kid, flow, kaiva, lag=0.25), *disappear(self.ex), run_time=1.0)
            # the join: The Kid fans out into its rows
            self.play(flow.animate.move_to([COLS[0][0], -1.9, 0]),
                      kaiva.animate.move_to([COLS[0][0], -2.5, 0]), run_time=0.9)
            k1 = join_row("The Kid", "tt0012349", "A Tramp", 0.6)
            k2 = join_row("The Kid", "tt0012349", "The Child", 0.0)
            k3 = join_row("The Kid", "tt0012349", "The Woman", -0.6)
            more = T("… 12 rows", 28, DIM, t2c={"12": GOLD}).move_to([3.35, -1.2, 0])
            self.play(*appear(heads[1], heads[2], k1[1], k1[2], *k2, *k3, more, lag=0.08),
                      run_time=min(1.8, 0.9 * c.until("A movie with no match")))
            c.wait_until("A movie with no match")
            fr = join_row("Flow", "NULL", "NULL", -1.9, rid_color=PINK, role_color=PINK)
            kr = join_row("Kaiva", "NULL", "NULL", -2.5, rid_color=PINK, role_color=PINK)
            self.play(*appear(fr[1], fr[2], kr[1], kr[2], lag=0.2), run_time=1.4)
            self.play(*flash([fr[1], fr[2], kr[1], kr[2]], color=PINK, time_width=1.5), run_time=1.5)

            # WHERE r.movie_id IS NULL
            c.wait_until("isnull")
            dims = [g.animate.set_opacity(0.35) for i in range(4) for g in q.line(i)]
            self.play(*dims, FlashAround(q.line(4), color=YELLOW, time_width=1.5), run_time=1.5)
            kid_rows = [kid, k1[1], k1[2], *k2, *k3, more]
            green = [m.rect.animate.set_stroke(GREEN, 3) for m in (flow, fr[1], fr[2], kaiva, kr[1], kr[2])]
            self.play(*set_alpha(kid_rows, DIMMED), *green, run_time=1.2)
            self.play(*[FadeOut(m, shift=0.3 * RIGHT) for m in kid_rows], run_time=0.9)

            c.wait_until("left with Flow")
            old = VGroup(*heads, flow, kaiva, *fr[1:], *kr[1:])
            rh = [Mono("movie_id", 28, DIM), Mono("title", 28, DIM)]
            RC = [(2.75, 2.7), (4.95, 1.7)]
            for h, (x, _) in zip(rh, RC):
                h.move_to([x, 0.6, 0])
            res = VGroup(*rh)
            for y, (mid, tt) in zip([0.0, -0.6], [("tt4772188", "Flow"), ("tt27719898", "Kaiva")]):
                res.add(cell(Mono(mid, 28), RC[0][1], color=GREEN, center=[RC[0][0], y, 0]),
                        cell(T(tt, 28), RC[1][1], color=GREEN, center=[RC[1][0], y, 0]))
            for m in res[2:]:
                m.rect.set_stroke(GREEN, 3)
            self.res = res
            self.play(*swap(old, res), run_time=1.3)

            c.wait_until("test")
            box = SurroundingRectangle(q.find("IS NULL"), color=YELLOW, buff=0.08)
            self.isnull_box = box
            self.play(GrowFromCenter(box), run_time=1.0)
            c.wait_until("Equals null")
            eq = Mono("= NULL", 30, RED)
            x = cross_mark().scale(0.8)
            zero = T("0 rows", 30, DIM)
            tease = VGroup(eq, x, zero).arrange(RIGHT, buff=0.3)
            tease.next_to(box, DOWN, buff=0.55).align_to(box, LEFT)
            self.tease = tease
            self.play(*appear(eq, x, zero, lag=0.25), run_time=0.9)

    # ------------------------------------------------------------ clip 3
    def clip3(self):
        cap, flow, kaiva = self.cap, self.flow, self.kaiva
        with self.say("c2.absent.3") as c:
            q1 = self.q1
            self.play(*set_alpha([q1], DIMMED), *disappear(self.res, self.tease, self.isnull_box, self.lj),
                      run_time=0.9)
            self.play(*disappear(q1), run_time=0.7)
            q2 = except_query()
            q2.to_edge(LEFT, buff=0.5).move_to([q2.get_x(), 0.45, 0])
            exl = Mono("EXCEPT", 30, DIM).next_to(q2, UP, buff=0.35, aligned_edge=LEFT)
            self.play(*appear(q2, shift=None), *appear(exl), run_time=1.0)

            # the set picture
            C = np.array([3.7, -0.5, 0])
            R, r = 2.45, 1.98
            Ci = C + (R - r) * UP
            outer = Circle(radius=R).move_to(C).set_stroke(BLUE, 4)
            inner = Circle(radius=r).move_to(Ci).set_stroke(BLUE, 3).set_fill(BLUE, 0.12)
            ol = VGroup(T("every movie", 30), T("2,935", 32, GOLD)).arrange(RIGHT, buff=0.3)
            ol.move_to(C + (R + 0.42) * DOWN)
            il = VGroup(T("movies with", 30), T("a role", 30)).arrange(DOWN, buff=0.12).move_to(Ci + 0.75 * UP)
            inum = T("2,933", 32, GOLD).next_to(il, DOWN, buff=0.22)
            c.wait_until("all")
            self.play(GrowFromCenter(outer), *appear(ol), run_time=1.0)
            c.wait_until("minus")
            self.play(GrowFromCenter(inner), *appear(il, inum, lag=0.3), run_time=1.5)  # early: "every movie that appears in plays role"

            c.wait_until("left")
            sliver = Difference(outer.copy(), inner.copy()).set_stroke(width=0).set_fill(GREEN, 0.35)
            sliver.set_z_index(-1)
            fl = T("Flow", 30, GREEN).move_to(C + np.array([-0.7, -1.95, 0]))
            kl = T("Kaiva", 30, GREEN).move_to(C + np.array([0.65, -1.95, 0]))
            two = T("2", 44, GOLD).move_to(C + np.array([-2.75, -1.75, 0]))
            self.play(FadeIn(sliver), FlashAround(sliver, color=GREEN, time_width=1.5), run_time=1.2)
            tick = Line(two.get_right() + 0.12 * RIGHT, C + np.array([-1.5, -1.75, 0])).set_stroke(GREEN, 3)
            self.play(*appear(fl, kl, lag=0.3), run_time=1.0)
            self.play(*appear(two), Create(tick), run_time=0.8)

            c.wait_until("ids")
            ids = [q2.find("movie_id", nth=0), q2.find("movie_id", nth=1)]
            uls = [underline(g, YELLOW, buff=0.08) for g in ids]
            self.play(*[GrowFromEdge(u, LEFT) for u in uls], run_time=1.2)

            # titles repeat
            c.wait_until("repeat")
            X = -4.3
            pairs = [
                (movie_card("The Italian Job", 1969, size=28), movie_card("The Italian Job", 2003, size=28)),
                (movie_card("The Mummy", 1999, size=28), movie_card("The Mummy", 2017, size=28)),
                (movie_card("Total Recall", 1990, size=28), movie_card("Total Recall", 2012, size=28)),
            ]
            for (a, b), y in zip(pairs, [2.0, 0.3, -1.4]):
                a.move_to([X, y, 0])
                b.move_to([X, y - 0.8, 0])
            tr90, tr12 = pairs[2]
            self.play(*disappear(q2, exl, *uls), run_time=0.9)
            c.wait_until(own_word=tr90.title)
            self.play(*appear(tr90, tr12, lag=0.3), run_time=1.0)
            c.wait_until("The Mummy")
            self.play(*appear(*pairs[1], lag=0.3), run_time=1.0)
            self.play(*appear(*pairs[0], lag=0.3), run_time=1.0)

            # what if Total Recall 1990 had no actors?
            c.wait_until("cancel")
            whatif = T("what if", 32, DIM, slant=ITALIC).move_to([-0.4, -3.15, 0])
            self.play(*during(appear(whatif) + disappear(fl, kl, two, tick), 0, 0.4),
                      *during([tr90.animate.move_to(C + 1.85 * DOWN)], 0.35, 1), run_time=1.8)
            tr12c = tr12.copy().move_to(Ci + 1.2 * DOWN)
            self.play(*fly(tr12, tr12c), run_time=max(1.0, min(1.3, c.until("cancel it out"))))
            c.wait_until("cancel it out")
            strike = Line(tr90.title.get_left() + 0.1 * LEFT, tr90.year.get_right() + 0.1 * RIGHT)
            strike.set_stroke(RED, 5)
            arr = Arrow(tr12c.get_bottom(), tr90.get_top(), buff=0.04, stroke_width=4,
                        max_tip_length_to_length_ratio=0.5).set_color(RED)
            self.play(GrowArrow(arr), tr90.box.animate.set_stroke(RED, 3),
                      tr12c.box.animate.set_stroke(RED, 3), run_time=0.9)
            keys = VGroup(T("compare keys,", 34, YELLOW), T("not titles", 34, YELLOW)).arrange(DOWN, buff=0.15)
            keys.move_to([-0.35, 0.25, 0])
            self.keys = keys
            self.play(Create(strike), *appear(keys), run_time=0.9)
            c.wait_until("vanish")
            self.play(*disappear(tr90, strike, arr), run_time=1.0)

    def finale(self):
        self.wait(3.4)
        keep = [self.cap, self.flow, self.kaiva]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in keep], run_time=1.2)
        self.wait(1.0)
