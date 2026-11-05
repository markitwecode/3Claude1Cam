"""Chapter 10, scene 7: Recap of the lecture, then Next: Lecture 5. Clips c10.recap.1 – c10.recap.2.

Clip 1: the recap grid fills its top row, one callback per sentence (s2's tests + verdicts, s3's validator,
s4's path + 9 documents vs 1 row), each with a DIM line under it; the one before dims to 0.5.
Clip 2: the bottom row (s5's bars + ID lists, s6's genre table + casts). On {next} the grid dims, then
sweeps away as "Next: Lecture 5 · Graph Databases" arrives on top; on "the tangle" ch6 s3's tangle grows in
the centre; on {bacon} a DIM Kevin Bacon vertex at the right edge and a dashed path of hops toward it.
End card held ~8 s, then fade to empty.
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

S2 = load_scene("ch10_s2_choose")
S3 = load_scene("ch10_s3_schema")
S4 = load_scene("ch10_s4_rename")
S5 = load_scene("ch10_s5_directors")
S6 = load_scene("ch10_s6_genres")
G3 = load_scene("ch6_s3_graph")

TOP_Y, BOT_Y = 3.6, -0.45          # top edge of each row's visual
CAP_SIZE = 30


def item(vis, cap, w, h):
    """ch9 s9's recap item: the callback scaled into w x h, its short line(s) under it (DIM here)."""
    vis.scale(min(w / vis.width, h / vis.height))
    capt = VGroup(*[T(s, CAP_SIZE, DIM) for s in cap.split("\n")]).arrange(DOWN, buff=0.12)
    capt.next_to(vis, DOWN, buff=0.22)
    g = VGroup(vis, capt)
    g.vis, g.cap = vis, capt
    return g


def place(it, x, top):
    it.shift([x - it.vis.get_x(), top - it.vis.get_top()[1], 0])
    return it


def grid():
    i1 = place(item(S2.recap_r1(), "tree or tangle ·\nhow often it changes ·\none shape or many", 4.4, 2.3),
               -4.6, TOP_Y)
    i2 = place(item(S3.recap_r2(), "a schema sees one\ndocument at a time", 4.4, 2.6), 0.0, TOP_Y)
    i3 = place(item(S4.recap_r3(), "every copy of a name", 4.4, 2.6), 4.6, TOP_Y)
    i4 = place(item(S5.recap_r4(), "json_array_length ·\nlist_has_any, by ID", 6.2, 2.0), -3.45, BOT_Y)
    i5 = place(item(S6.recap_r5(), "cast to a number ·\ncount what's behind the average", 6.2, 2.0),
               3.45, BOT_Y)
    return [i1, i2, i3, i4, i5]


KEYS = ("coogan", "chaplin", "kid", "gold")
BACON_POS = np.array([5.25, -2.0, 0])


def next_card():
    head = T("Next: Lecture 5 · Graph Databases", 48).move_to([0, 3.1, 0])
    tg = G3.tangle().scale(0.8).move_to([-1.3, -0.35, 0])
    bc = Circle(radius=0.4).set_stroke(DIM, 4).set_fill(DIM, 0.15).move_to(BACON_POS)
    bl = T("Kevin Bacon", 32, DIM).next_to(bc, DOWN, buff=0.15)
    bacon = VGroup(bc, bl)
    start = tg.v["gold"].circle
    p0 = start.get_right()
    hops = [np.array([2.3, -0.8, 0]), np.array([3.7, -2.25, 0])]
    dots = VGroup(*[Dot(h, radius=0.1, color=DIM) for h in hops])
    pts = [p0, *hops, bc.get_left()]
    segs = VGroup(*[DashedLine(a, b, dash_length=0.12, dashed_ratio=0.55).set_stroke(DIM, 3)
                    for a, b in zip(pts[:-1], pts[1:])])
    g = VGroup(head, tg, segs, dots, bacon)
    g.head, g.tangle, g.segs, g.dots, g.bacon = head, tg, segs, dots, bacon
    return g


class Ch10S7Recap(NarratedScene):
    def construct(self):
        items = grid()
        with self.say("c10.recap.1") as c:
            prev = None
            for it, cue in zip(items[:3], ("r1", "r2", "r3")):
                c.wait_until(cue)
                dim = set_alpha([prev], 0.5) if prev else []
                self.play(*dim, *appear(it.vis, it.cap, lag=0.3), run_time=1.5)  # early: callback shown whole
                prev = it
        with self.say("c10.recap.2") as c:
            for it, cue in zip(items[3:], ("r4", "r5")):
                c.wait_until(cue)
                self.play(*set_alpha([prev], 0.5), *appear(it.vis, it.cap, lag=0.3), run_time=1.5)  # early: callback shown whole
                prev = it

            card = next_card()
            c.wait_until("next")
            self.play(*set_alpha(items, DIMMED), run_time=1.0)
            c.wait_until("graph databases")
            sweep_clear(self, *appear(card.head, shift=None), run_time=min(1.6, c.until("The tangle from part six")))
            c.wait_until("The tangle from part six")
            tg = card.tangle
            self.play(*[GrowFromCenter(tg.v[k].circle) for k in KEYS], run_time=1.0)
            self.play(*[Create(l) for l in tg.lines],
                      *appear(*[tg.v[k].label for k in KEYS], shift=None, lag=0.1),
                      run_time=1.5)
            c.wait_until("bacon")
            self.play(Succession(*[Create(s) for s in card.segs], run_time=2.0),
                      *appear(*card.dots, lag=0.4), run_time=2.0)
            c.wait_until(own_word=card.bacon[1])
            self.play(*appear(card.bacon), run_time=1.0)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)
