"""Chapter 5, scene 4: two flip-flops, the sequential codes, and the output s = s1. Clips c5.codes.1 – c5.codes.3.

Opens on s3's handover_shot() (the bare sync_diagram()) and shrinks it to the left.
Shared helpers (load_scene("ch5_s4_twoffs")):
- `place(g)`: the left placement of any sync_diagram(): scale DIAG_SCALE (0.55) about ORIGIN, then
  shift DIAG_SHIFT (-3.9, 0.05). The coded diagram (codes + unused) then spans x -6.58..-1.03,
  y -1.82..1.78, centre (-3.80, -0.02).
- `coded_diagram()`: place(sync_diagram(codes=CODES, unused=True)).
- `ff_pair()`: two D flip-flops (make_ff, no clock wire), s1 at (1.0, 2.0), s0 at (4.2, 2.0), scale 0.6;
  .ffs [s1, s0], .outs [MathTex s_1, s_0 GREEN], .tag ("FF labels [s1 s0]") under them.
- `output_table()`: state | s1 s0 | s; .rows[i] (state, s1, s0, s), .head, .col(j) cells of column j.
- `s_eq()`: GREEN MathTex "s = s_1" 60.
- `nologic_wire(pair)`: GREEN wire from s1's Q end up and right to an arrow, "s" label; .wire .s_l.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch5_s3_diagram")
C1 = load_scene("ch1_s4_choice")
NL = load_scene("ch2_s6_nologic")


def _p(x, y):
    return np.array([x, y, 0.0])


CODES = {"Hunt": "00", "Sight": "01", "Sync": "10"}
DIAG_SCALE = 0.55
DIAG_SHIFT = _p(-3.9, 0.05)


def place(g):
    return g.scale(DIAG_SCALE, about_point=ORIGIN).shift(DIAG_SHIFT)


def coded_diagram():
    return place(S3.sync_diagram(codes=CODES, unused=True))


FF_SCALE = 0.6
FF_Y = 2.0


def ff_pair():
    ffs, outs = [], []
    for x, name in ((1.0, "s_1"), (4.2, "s_0")):
        f = NL.make_ff(ORIGIN, size=48)
        f.remove(f.clk_w)
        # clock triangle enlarged (native one is 0.2 wide at FF_SCALE: invisible in the shrunk pair)
        f.tri.scale(1.8, about_point=f.tri.get_bottom()).set_stroke(FG, 4)
        f.scale(FF_SCALE, about_point=ORIGIN).shift(_p(x, FF_Y))
        o = MathTex(name, font_size=44, color=GREEN).next_to(f.q_w, RIGHT, buff=0.12)
        ffs.append(f)
        outs.append(o)
    tag = VGroup(T("FF labels", 30, DIM), Mono("[s1 s0]", 30, GREEN)).arrange(RIGHT, buff=0.22)
    tag.move_to(_p(2.75, 0.85))
    g = VGroup(*ffs, *outs, tag)
    g.ffs, g.outs, g.tag = ffs, outs, tag
    return g


COL_X = (0.0, 1.6, 2.4, 3.6)
ROW_Y = (-0.15, -0.9, -1.65, -2.4, -3.15)


def output_table():
    head = [T("state", 30, DIM), MathTex("s_1", font_size=42, color=GREEN),
            MathTex("s_0", font_size=42, color=GREEN), MathTex("s", font_size=42, color=YELLOW)]
    data = [("Hunt", "0", "0", "0"), ("Sight", "0", "1", "0"), ("Sync", "1", "0", "1"), ("", "1", "1", "–")]
    for m, x in zip(head, COL_X):
        m.move_to(_p(x, ROW_Y[0]))
    rows = []
    for k, (n, a, b, s) in enumerate(data):
        y = ROW_Y[k + 1]
        col = DIM if k == 3 else None
        cells = [T(n, 32, YELLOW).move_to(_p(COL_X[0], y))] if n else []
        for d, x in zip((a, b, s), COL_X[1:]):
            c = col or (GOLD if d == "1" else FG)
            cells.append((T(d, 34, c) if d == "–" else Mono(d, 34, c)).move_to(_p(x, y)))
        rows.append(VGroup(*cells))
    hline = Line(_p(-0.75, -0.53), _p(4.1, -0.53)).set_stroke(DIM, 2)
    v1 = Line(_p(0.85, 0.2), _p(0.85, -3.5)).set_stroke(DIM, 2)
    v2 = Line(_p(3.0, 0.2), _p(3.0, -3.5)).set_stroke(DIM, 2)
    g = VGroup(*head, hline, v1, v2, *rows)
    g.head, g.rows, g.lines = head, rows, [hline, v1, v2]
    g.col = lambda j, n=3: [head[j]] + [rows[k][j] for k in range(n)]
    return g


def s_eq():
    return MathTex("s", "=", "s_1", font_size=60, color=GREEN).move_to(_p(5.55, -1.3))


def nologic_wire(pair):
    q_end = pair.ffs[0].q_w.get_right()
    top = FF_Y + 1.05
    wire = VMobject().set_points_as_corners([q_end + 0.25 * LEFT, _p(q_end[0] - 0.25, top), _p(5.9, top)])
    wire.set_stroke(GREEN, 5)
    tip = Triangle().set_stroke(width=0).set_fill(GREEN, 1).scale(0.12).rotate(-PI / 2).move_to(_p(5.95, top))
    s_l = MathTex("s", font_size=44, color=GREEN).next_to(tip, RIGHT, buff=0.12)
    g = VGroup(wire, tip, s_l)
    g.wire, g.tip, g.s_l = wire, tip, s_l
    return g


class TwoFlipFlops(NarratedScene):
    def construct(self):
        diag = S3.handover_shot()
        self.add(diag)
        coded = coded_diagram()

        # ---------------------------------------------------------------- c5.codes.1
        with self.say("c5.codes.1") as c:
            ladder = C1.doubling_ladder(label_size=40, pat_size=36)
            rows = VGroup(*ladder.rows[:2]).copy()
            rows.scale(0.82).move_to(_p(3.0, 1.1))
            diag.generate_target()
            place(diag.target)
            self.play(MoveToTarget(diag), run_time=1.3)
            self.play(*appear(*rows, lag=0.5), run_time=1.3)
            c.wait_until("ladder")
            f = MathTex(r"\lceil \log_2 3 \rceil", "=", "2", font_size=60, color=GOLD).move_to(_p(3.0, -1.2))
            self.play(*appear(f), FlashAround(rows[1], run_time=1.6, time_width=1.5),
                      *recolor(rows[1][0], YELLOW), run_time=1.6)
            c.wait_until("labels")
            pair = ff_pair()
            self.play(*during(disappear(rows), 0, 0.45), f.animate.move_to(_p(3.0, -1.0)),
                      *during(appear(*pair.ffs, shift=None), 0.4, 1), run_time=1.4)
            self.play(*appear(*pair.outs, pair.tag, lag=0.3), run_time=1.2)

        # ---------------------------------------------------------------- c5.codes.2
        with self.say("c5.codes.2") as c:
            self.play(FlashAround(pair.tag[1], run_time=1.5, time_width=1.5))
            for name in ("hunt", "sight", "sync"):
                c.wait_until(name)
                code = coded.code[name.capitalize()]
                self.play(*appear(code), FlashAround(coded.name[name.capitalize()], run_time=1.2,
                                                     time_width=1.5), run_time=1.2)
            c.wait_until("unused")
            u = coded.unused
            self.play(*appear(u.circle, u.code, shift=None), run_time=1.0)
            c.wait_until(own_word=u.label)
            self.play(*appear(u.label), run_time=0.9)

        # ---------------------------------------------------------------- c5.codes.3
        with self.say("c5.codes.3", gap=3.0) as c:
            tab = output_table()
            self.play(*during(disappear(f), 0, 0.45),
                      *during(appear(*tab.head, *tab.lines, shift=None, lag=0.1), 0.45, 1), run_time=1.4)
            self.play(*appear(*tab.rows, lag=0.35), run_time=min(1.6, c.until("It must be")))
            c.wait_until("column")
            box1 = SurroundingRectangle(VGroup(*[m.copy() for m in tab.col(1)]), color=YELLOW,
                                        buff=0.14).set_stroke(YELLOW, 4)
            box2 = SurroundingRectangle(VGroup(*[m.copy() for m in tab.col(3)]), color=YELLOW,
                                        buff=0.14).set_stroke(YELLOW, 4)
            self.play(FadeIn(box1), run_time=0.9)
            c.wait_until("It's one in the Sync state")
            self.play(FadeIn(box2), run_time=0.9)
            c.wait_until("equal")
            eq = s_eq()
            self.play(*appear(eq), run_time=1.2)
            c.wait_until("So the output")
            self.play(FlashAround(eq, run_time=1.5, time_width=1.5))
            c.wait_until("why")
            sync_row = tab.rows[2]
            self.play(*disappear(box1, box2), FlashAround(sync_row, run_time=1.4, time_width=1.5),
                      run_time=1.4)
            c.wait_until("never occurs")
            tag = T("never occurs", 30, DIM).next_to(tab.rows[3], RIGHT, buff=0.55)
            self.play(FlashAround(tab.rows[3], color=FG, run_time=1.3, time_width=1.5),
                      *appear(tag), run_time=1.3)
            c.wait_until("nologic")
            w = nologic_wire(pair)
            lbl = T("no output logic", 30, GREEN).move_to(_p(3.9, FF_Y + 1.38))
            self.play(Create(w.wire), *during(appear(w.tip, w.s_l, shift=None), 0.6, 0.85),
                      *during(appear(lbl), 0.75, 1), run_time=1.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
