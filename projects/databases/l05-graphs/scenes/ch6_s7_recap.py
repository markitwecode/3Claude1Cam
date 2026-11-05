"""Chapter 6, scene 7: recap of the five exercise solutions, then the lecture's end card. Clips c6.recap.1 – c6.recap.2.

Each sentence brings its solution's tile up big at the centre with its line under it; on the next
sentence the tile docks into a strip along the top. On {next} the strip dims, the teaser, a ghost
WITH RECURSIVE and ch5 s2's Lawrence -> Radcliffe path come up; the end card holds ~8 s.
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

S2 = load_scene("ch5_s2_bfs")
R1 = load_scene("ch6_s2_chaplin")
R2 = load_scene("ch6_s3_composers")
R3 = load_scene("ch6_s4_wachowski")
R4 = load_scene("ch6_s5_sql")
R5 = load_scene("ch6_s6_genres")

HERO_Y = -0.15
HERO_W, HERO_H = 13.0, 3.4
CAP_BUFF = 0.6
SLOT_X = [-5.5, -2.75, 0.0, 2.75, 5.5]
SLOT_Y = 2.95
SLOT_W, SLOT_H = 2.4, 0.9
LAB_Y = 2.08
TEASER_Y = -2.9

LINES = ["same name, same vertex",
         "plain RETURN expressions are the grouping keys;\nperson IDs keep namesakes apart",
         "edges multiply rows; DISTINCT folds them",
         "every edge in the pattern is a join",
         "list: denormalised  ·  vertices: normalised"]
SHORT = ["same vertex", "keys + IDs", "DISTINCT", "edge = join", "list vs vertex"]


def chaplin_tile():
    t = R1.recap_tile()
    ch = T("Charles Chaplin", 30).next_to(t.p, DOWN, buff=0.3).align_to(t.p, RIGHT)
    kid = T("The Kid", 30).next_to(t.m, DOWN, buff=0.3).align_to(t.m, LEFT)
    g = VGroup(t, ch, kid).move_to(ORIGIN)
    g.p, g.m = t.p, t.m
    return g


def hero_fit(tile):
    k = min(1.0, HERO_W / tile.width, HERO_H / tile.height)
    tile.scale(k).move_to((0, HERO_Y, 0))
    return tile


def caption(i, tile):
    cap = T(LINES[i], 36, t2c={"DISTINCT": BLUE, "RETURN": BLUE})
    cap.next_to(tile, DOWN, buff=CAP_BUFF)
    return cap


def slot_label(i):
    return T(SHORT[i], 28).move_to((SLOT_X[i], LAB_Y, 0))


def dock(scene, tile, cap, i, incoming=()):
    """Two plays. 1: the caption goes, the tile shrinks while sliding sideways to under its slot.
    2: it rises into slot i (its own column, so it crosses nothing), its short label drops in, and
    `incoming` (the next tile and line) arrives once it has left the centre. Returns the label."""
    k = min(SLOT_W / tile.width, SLOT_H / tile.height)
    scene.play(*during(disappear(cap), 0, 0.4),
               tile.animate.scale(k).move_to((SLOT_X[i], tile.get_y(), 0)), run_time=1.0)
    lab = slot_label(i)
    scene.play(tile.animate.move_to((SLOT_X[i], SLOT_Y, 0)), *during(appear(lab, shift=None), 0.86, 1),
               *incoming, run_time=1.5 if incoming else 1.0)
    return lab


def arrive(tile, cap):
    return [*during(appear(tile, shift=None), 0.6, 0.85), *during(appear(cap), 0.72, 1)]


def end_path():
    p = S2.lr_path(names=S2.LR_NAMES, pitch=2.0, above_films=True)
    return p.move_to((0, 0.05, 0))


class Recap(NarratedScene):
    def construct(self):
        tiles = [hero_fit(chaplin_tile()), hero_fit(R2.recap_tile()), hero_fit(R3.recap_tile()),
                 hero_fit(R4.recap_tile()), hero_fit(R5.recap_tile())]
        caps = [caption(i, t) for i, t in enumerate(tiles)]
        strip = []

        # ------------------------------------------------ clip 1: five solutions
        with self.say("c6.recap.1") as c:
            title = T("Recap", 52).move_to((0, 0.3, 0))
            self.play(*appear(title), run_time=min(1.0, c.until("r1")))  # early: a title
            c.wait_until("r1")

            # r1: Chaplin's fused loop
            self.play(*during(disappear(title), 0, 0.4), *during(appear(tiles[0], shift=None), 0.3, 0.75),
                      *during(appear(caps[0]), 0.55, 1), run_time=1.8)
            self.play(FlashAround(tiles[0].p, run_time=1.5, time_width=1.5, color=YELLOW))
            c.wait_until("r2")

            # r2: the composers
            lab = dock(self, tiles[0], caps[0], 0, arrive(tiles[1], caps[1]))
            strip += [tiles[0], lab]
            c.wait_until("grouping keys")
            self.play(FlashAround(tiles[1].result, run_time=1.5, time_width=1.5))
            c.wait_until("person IDs")
            self.play(*flash([tiles[1].jw1932, tiles[1].jw1903], color=TEAL, run_time=1.5, time_width=1.5))
            c.wait_until("r3")

            # r3: the Wachowskis
            lab = dock(self, tiles[1], caps[1], 1, arrive(tiles[2], caps[2]))
            strip += [tiles[1], lab]
            c.wait_until("return distinct")
            self.play(FlashAround(tiles[2][2], run_time=1.5, time_width=1.5, color=BLUE))
            c.wait_until("r4")

            # r4: the same query in SQL
            lab = dock(self, tiles[2], caps[2], 2, arrive(tiles[3], caps[3]))
            strip += [tiles[2], lab]
            c.wait_until("grouping yourself")
            self.play(FlashAround(tiles[3][0][4][1], run_time=1.2, time_width=1.5),
                      run_time=min(1.2, c.until("r5")))
            c.wait_until("r5")

            # r5: genres, list against vertices
            lab = dock(self, tiles[3], caps[3], 3, arrive(tiles[4], caps[4]))
            strip += [tiles[3], lab]

        # ------------------------------------------------ clip 2: next lecture, end card
        with self.say("c6.recap.2") as c:
            lab = dock(self, tiles[4], caps[4], 4)
            strip += [tiles[4], lab]
            self.play(*set_alpha(strip, 0.4), run_time=0.8)

            tz = T("Next lecture: Datalog and recursive queries", 36, DIM).move_to((0, TEASER_Y, 0))
            c.wait_until(own_word=tz)
            self.play(*appear(tz), run_time=1.0)
            ghost = Mono("WITH RECURSIVE", 32, BLUE).set_opacity(0.4).move_to((0, -1.85, 0))
            c.wait_until("recursive")
            self.play(*appear(ghost, shift=None), run_time=1.0)
            path = end_path()
            c.wait_until("chains")
            self.play(*appear(path, shift=None), run_time=min(1.2, c.until("end", floor=0.8)))
            c.wait_until("end")
            self.play(*[VShowPassingFlash(e.copy().set_stroke(YELLOW, 6), time_width=0.6) for e in path.edges],
                      run_time=min(1.0, c.until(floor=0.5)))

        self.wait(8)        # the end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
