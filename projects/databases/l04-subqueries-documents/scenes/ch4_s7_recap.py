"""Chapter 4, scene 7: recap, then the teaser for ch5. Clips c4.recap.1 – c4.recap.3.

Five small callbacks, one per sentence, each with its short line under it, built left to right in
two rows (top: s2's Ada tree, s1's schema cards collapsing into s3's The Kid card; bottom: s4, s5,
s6 recap thumbs). On {next} they dim and clear; the frame then builds, piece by piece, exactly
load_scene("ch5_s1_hook").open_card() (ch5's first frame), holds it ~8 s, and fades.
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
SCH = load_scene("ch1_s2_schema")
D = load_scene("ch4_s3_movie")
PER = load_scene("ch4_s4_person")
SHP = load_scene("ch4_s5_shape")
STO = load_scene("ch4_s6_store")
H5 = load_scene("ch5_s1_hook")

TOP_Y, TOP_CAP_Y = 2.3, 0.85          # top row: picture centre, caption centre
BOT_Y, BOT_CAP_TOP = -1.15, -2.45     # bottom row: picture centre, caption top
CAP = 28


def caption(text, x, y=None, top=None, **kw):
    t = T(text, CAP, **kw)
    if top is not None:
        t.move_to([x, top - t.height / 2, 0])
    else:
        t.move_to([x, y, 0])
    return t


def fit(mob, w, h, center):
    mob.scale(min(w / mob.width, h / mob.height))
    return mob.move_to(center)


def ada_subset():
    v = J.ada_value()
    return J.json_tree({k: v[k] for k in ("name", "languages", "email")}, size=26)


class Recap(NarratedScene):
    def construct(self):
        self.part1()
        self.part2()
        self.next_time()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c4.recap.1
    def part1(self):
        with self.say("c4.recap.1") as c:
            # r1: Ada's tree (a subset: an object, an array, plain values, the PINK null)
            c.wait_until("r1")
            t1 = ada_subset().move_to([-2.6, TOP_Y, 0])
            cap1 = caption("JSON: objects, arrays, values, a tree", t1.get_x(), TOP_CAP_Y)
            self.play(*appear(t1, shift=None), run_time=min(1.2, c.until("r2")))
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=min(1.0, c.until("r2")))

            # r2: the seven BLUE schema cards collapse into The Kid's one TEAL card
            c.wait_until("r2")
            ctr = np.array([4.4, TOP_Y, 0])
            sm = fit(SCH.schema_map(), 3.9, 2.1, ctr)
            self.play(*appear(sm, shift=None), run_time=min(1.0, c.until("one piece")))
            c.wait_until("everything")
            kid = fit(D.kid_doc(), 3.0, 2.15, ctr)
            cards = list(sm.cards.values())
            self.play(*during(disappear(sm.arrow_group, sm.count_group), 0, 0.3),
                      *during([cd.animate.scale(0.3).move_to(ctr).set_opacity(0) for cd in cards], 0.1, 0.6),
                      *during([FadeIn(kid, scale=0.6)], 0.55, 1), run_time=min(1.8, c.until("one piece") + 0.6))
            self.remove(*sm.get_family())
            cap2 = caption("one movie, one document", 4.4, TOP_CAP_Y)
            c.wait_until(own_word=cap2, cue="one piece")
            self.play(*appear(cap2), run_time=min(1.0, c.until("r3")))

            # r3: Chaplin's long key list beside Hitchcock's five keys
            c.wait_until("r3")
            t3 = fit(PER.recap_thumb(), 4.3, 2.1, [-4.45, BOT_Y, 0])
            cap3 = caption("keys only where\nthey apply", t3.get_x(), top=BOT_CAP_TOP)
            self.play(*appear(t3, shift=None), run_time=min(1.2, c.until("shapes")))
            c.wait_until(own_word=cap3, cue="applies")
            self.play(*appear(cap3), run_time=min(1.0, c.until()))
            self.r = [t1, cap1, kid, cap2, t3, cap3]

    # ------------------------------------------------------------ c4.recap.2
    def part2(self):
        with self.say("c4.recap.2") as c:
            # r4: the two-way copies
            c.wait_until("r4")
            t4 = fit(SHP.recap_thumb(), 4.2, 2.1, [0.65, BOT_Y, 0])
            cap4 = caption("every link stored twice", t4.get_x(), top=BOT_CAP_TOP, t2c={"twice": GOLD})
            self.play(*appear(t4, shift=None), run_time=min(1.2, c.until("stored twice")))
            c.wait_until(own_word=cap4)
            self.play(*appear(cap4), run_time=min(1.0, c.until("stored twice")))
            c.wait_until("stored twice")
            self.play(VShowPassingFlash(t4.a1.copy().set_stroke(YELLOW, 5), time_width=0.6),
                      VShowPassingFlash(t4.a2.copy().set_stroke(YELLOW, 5), time_width=0.6),
                      run_time=min(1.2, c.until("copies")))
            c.wait_until("copies")
            self.play(*flash([t4.name_k, t4.name_c, t4.title_k, t4.title_c], color=GOLD, time_width=1.5),
                      run_time=min(1.5, c.until("r5")))

            # r5: the movies table card with its closed TEAL boxes
            c.wait_until("r5")
            t5 = fit(STO.recap_thumb(), 3.1, 2.1, [5.05, BOT_Y, 0])
            cap5 = caption("a JSON column:\nstructure unchecked", t5.get_x(), top=BOT_CAP_TOP,
                           t2c={"unchecked": RED})
            self.play(*appear(t5, shift=None), run_time=min(1.2, c.until("JSON column")))
            c.wait_until(own_word=cap5, cue="JSON column")
            self.play(*appear(cap5), run_time=min(1.0, c.until("never checks")))
            c.wait_until("never checks")
            self.play(FlashAround(t5, color=RED, time_width=1.5), run_time=min(1.5, c.until()))
            self.r += [t4, cap4, t5, cap5]

    # ------------------------------------------------------------ c4.recap.3
    def next_time(self):
        end = H5.open_card()
        name = end.kid.code.find('"Charles Chaplin"')
        name.set_color(FG)
        with self.say("c4.recap.3", gap=0.0) as c:
            c.wait_until("next")
            self.play(*set_alpha(self.r, DIMMED), run_time=min(0.9, c.until("chaplin's name")))
            sweep_clear(self, time_span(FadeIn(end.kid, shift=0.2 * DOWN), 0.6, 1.2),
                        run_time=min(1.2, max(0.8, c.until("chaplin's name"))))
            c.wait_until("chaplin's name")
            self.play(*recolor(name, GOLD), FlashAround(name, color=GOLD, time_width=1.5),
                      run_time=min(1.4, c.until("more places")))
            # the five DIM movie cards, then the copies of the GOLD name spread across them
            c.wait_until("more places")
            fan = end.fan
            self.play(*appear(*[m for cd in fan for m in (cd.frame, cd.title)], shift=0.2 * LEFT, lag=0.1),  # early: the cards' titles are never read
                      run_time=min(1.2, c.until("cost") * 0.45))
            tags = [t for cd in fan for t in cd.tags]
            self.play(*appear(*tags, shift=0.15 * DOWN, lag=0.08),
                      run_time=min(1.6, max(0.8, c.until("cost"))))
            settle(self, fan)
            # buy / cost
            c.wait_until(own_word=end.buy.word, cue="buy")
            self.play(*appear(end.buy), run_time=min(1.0, c.until("cost")))
            c.wait_until(own_word=end.cost.word)
            self.play(*appear(end.cost), run_time=min(1.0, c.until()))
        self.wait(7.7)      # the end card (= ch5's first frame), ~8 s after the last word; music carries it
