"""Chapter 2, scene 7: recap, then the co-star card that opens chapter 3. Clips c2.recap.1 – c2.recap.2.

Each recap idea is shown big in the centre (the visual that taught it, from its scene's export) with
its short line beneath; on the next cue it shrinks into its slot in a row of five along the top.
On {next} the row clears and ch3's opening card (ch3_s1_hook.open_card()) is built from its own
parts; the scene ends on that object unchanged, held ~8 s (reversed join with ch3, no fade-out).
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

S2 = load_scene("ch2_s2_vertex")
S3 = load_scene("ch2_s3_match")
S4 = load_scene("ch2_s4_edge")
S5 = load_scene("ch2_s5_props")
S6 = load_scene("ch2_s6_vssql")
C3 = load_scene("ch3_s1_hook")

HERO_C = np.array([0.0, -0.35, 0])    # centre of the hero area
HERO_W, HERO_H = 11.0, 4.0            # hero area
CAP_Y = -3.35                         # caption line under the hero
SLOT_Y, SLOT_W, SLOT_H = 2.95, 2.45, 1.45
SLOT_X = [-5.6, -2.8, 0.0, 2.8, 5.6]


def fit_hero(g, up=1.15):
    s = min(HERO_W / g.width, HERO_H / g.height, up)
    g.scale(s).move_to(HERO_C)
    return g


def caption(text):
    return T(text, 34).move_to([0, CAP_Y, 0])


def r2_panel():
    """Three BLUE Movie circles of scene 3's patch, the stencil on The Kid, its row and the count."""
    patch = S3.movie_patch()
    movies = patch.movies[:3]
    col = VGroup(*movies)
    kid = movies[0]
    st = S3.stencil().at(kid.circle.get_center())
    row = S3.row_text("The Kid", 0)
    row.next_to(kid.name, RIGHT, buff=2.0).set_y(kid.name.get_y())
    box = Rectangle(width=row.width + 0.6, height=0.62).set_stroke(DIM, 2).move_to(row)
    row = VGroup(box, row)
    count = T("2,935", 56, GOLD)
    count.move_to([row.get_center()[0], movies[1].circle.get_y() - 0.4, 0])
    g = VGroup(col, st, row, count)
    fit_hero(g)
    g.shift(LEFT * 0.6)
    g.col, g.kid, g.st, g.row, g.count = col, kid, st, row, count
    return g


class Recap(NarratedScene):
    def construct(self):
        self.thumbs = []
        self.clip1()
        self.clip2()
        self.wait(8.0)   # end card = ch3_s1_hook.open_card(), held, no fade (reversed join; brief)

    # ------------------------------------------------------------ helpers
    def replace_panel(self, panel, cap, i, *incoming, run_time=1.4):
        """panel + caption rise out (first 45%); incoming animations arrive in the second half."""
        out = during([FadeOut(panel, shift=0.3 * UP), FadeOut(cap, shift=0.3 * UP)], 0.0, 0.45)
        inc = [a for x in incoming for a in (x if isinstance(x, list) else [x])]
        self.play(*out, *inc, run_time=run_time)
        self.remove(*panel.get_family(), *cap.get_family())

    # ------------------------------------------------------------ c2.recap.1
    def clip1(self):
        with self.say("c2.recap.1", gap=1.5) as c:
            # r1: the vertex
            c.wait_until("r1")
            hero = fit_hero(S2.vertex_hero())
            v, k, code = hero[0], hero[1], hero[2]
            cap1 = caption("a vertex: round brackets")
            self.play(GrowFromCenter(v[0]), *appear(v[1], v[2], code, lag=0.2),  # early: the whole vertex first, then walked
                      run_time=1.4)
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("round brackets")
            self.play(*flash([code.find("("), code.find(")", nth=0)]), run_time=1.5)
            c.wait_until("curly braces")
            self.play(*appear(k), FlashAround(code.find("{title: 'The Kid', year: 1921}"),
                                              time_width=1.5), run_time=1.5)
            settle(self, hero)

            # r2: matching = placements, one row each
            c.wait_until("r2")
            p2 = r2_panel()
            st_rest = p2.st.get_center() + LEFT * 1.9 * (p2.kid.circle.width / 0.8)
            p2.st.shift(st_rest - p2.st.get_center())
            cap2 = caption("one placement = one row")
            self.replace_panel(hero, cap1, 0, during(appear(p2.col, p2.st, lag=0.15), 0.5, 1.0))
            c.wait_until("placement")
            self.play(p2.st.animate.shift(p2.kid.circle.get_center() - p2.st.centre()), run_time=1.0)
            self.play(*fly(p2.kid.name, p2.row[1]), FadeIn(p2.row[0]), run_time=1.2)
            self.play(*appear(p2.count, shift=None), run_time=0.8)
            c.wait_until("one row")
            self.play(*appear(cap2), run_time=1.0)
            settle(self, p2, add=[p2.col, p2.st, p2.row, p2.count])

            # r3: an edge, two edges, two rows
            c.wait_until("r3")
            p3 = fit_hero(S4.et_pair())
            arrows, person, movie, rows = p3
            cap3 = caption("an edge: square brackets; two edges, two rows")
            self.replace_panel(p2, cap2, 1, during(appear(person, movie, lag=0.2), 0.5, 1.0))
            c.wait_until("arrow")
            self.play(*[GrowArrow(arrows[i]) for i in (0, 2)],
                      *appear(arrows[1], arrows[3], lag=0.2), run_time=1.4)  # early: the two edge types label the arrows just drawn
            c.wait_until("square brackets")
            self.play(*appear(cap3), run_time=1.0)
            c.wait_until("several edges")
            self.play(*appear(rows[0], rows[1], lag=0.4), run_time=1.4)
            settle(self, p3)

            # r4: the arrowhead sets the direction
            c.wait_until("r4")
            p4 = fit_hero(S5.arrow_forms())
            cap4 = caption("the arrowhead sets the direction")
            self.replace_panel(p3, cap3, 2, during(appear(*p4.rows, lag=0.3), 0.45, 1.0), run_time=1.6)
            self.play(*appear(cap4), run_time=0.9)
            c.wait_until("leaving it out")
            self.play(FlashAround(p4.rows[1].code, time_width=1.5), run_time=1.4)
            settle(self, p4)

            # r5: an edge is a join through has_position
            c.wait_until("r5")
            p5 = fit_hero(S6.edge_join_panel())
            cap5 = caption("an edge ≈ a join with has_position")
            self.replace_panel(p4, cap4, 3, during(appear(p5, cap5, lag=0.3), 0.5, 1.0), run_time=1.6)
            c.wait_until("has position")
            self.play(FlashAround(p5.lines[0], time_width=1.5), run_time=1.4)

    # ------------------------------------------------------------ c2.recap.2
    def clip2(self):
        card = C3.open_card()
        with self.say("c2.recap.2") as c:
            sweep_clear(self, time_span(FadeIn(card.m), 0.6, 1.2), run_time=1.2)
            c.wait_until("two arrows")
            self.play(*appear(card.p1, card.p2, lag=0.0, shift=None),
                      *[GrowArrow(a) for a in card.arrows], run_time=1.4)
            self.play(*appear(*card.types, lag=0.0), run_time=0.9)  # early: the edge types belong to the arrows just drawn
            c.wait_until("costars")
            self.play(*flash([card.p1.circ, card.p2.circ], color=PINK), run_time=1.2)
            c.wait_until("co-stars")
            self.play(*appear(card.caption), run_time=1.0)
            self.play(*appear(card.pattern, shift=None), run_time=1.0)  # early: the pattern sits faint under its caption
            c.wait_until(own_word=card.most, cue="count")
            self.play(*appear(card.most), run_time=1.0)
            settle(self, card)
