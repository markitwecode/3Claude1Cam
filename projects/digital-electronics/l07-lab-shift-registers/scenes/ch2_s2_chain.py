"""Chapter 2, scene 2: a chain of D flip-flops, what one edge does, why not latches. Clips c2.chain.1 – c2.chain.4.

Opens on ch2_s1's handover_shot() (L8 ch2_s3's build_chain(fy=-0.5) + YELLOW "?"), clears the "?" and
highlights the parts in place. Digits GOLD at L8's digit_pos(); edge arrows run below the pin row with
ghosts of the old values; the what-if swaps each triangle for L6 ch1's EN square (latch_symbol style).
Ends on an empty frame (s3 draws its own strip).
"""
# style: 2
import importlib.util
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


def _load_l8():
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch2_s3_shiftreg.py"
    spec = importlib.util.spec_from_file_location("_l08_ch2_s3_shiftreg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8 = _load_l8()
S1 = load_scene("ch2_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


def square_wave(x0, x1, y, rises, falls, h=0.4, color=YELLOW, sl=0.1, width=4):
    ev = sorted([(x, 1) for x in rises] + [(x, 0) for x in falls])
    lo, hi = y - h / 2, y + h / 2
    lev = lo
    pts = [_p(x0, lev)]
    for x, up in ev:
        new = hi if up else lo
        pts += [_p(x - sl / 2, lev), _p(x + sl / 2, new)]
        lev = new
    pts.append(_p(x1, lev))
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


def up_arrow(x, y, color=YELLOW):
    return Arrow(_p(x + 0.16, y - 0.32), _p(x + 0.16, y + 0.38), buff=0, stroke_width=5,
                 tip_length=0.18, max_tip_length_to_length_ratio=0.35, color=color)


TR_Y = -2.85                       # traces under the chain
RISES = [-4.6, -3.1, -1.6]
FALLS = [-3.85, -2.35, -0.85]
ARROW_Y = -0.75                    # edge arrows, below the pin row


class ShiftChain(NarratedScene):
    def construct(self):
        shot = S1.handover_shot()
        self.C, self.q = shot.C, shot.q
        self.add(*self.C.all, self.q)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- the parts
    def clip1(self):
        C = self.C
        with self.say("c2.chain.1", gap=0.8) as c:
            self.play(*disappear(self.q), *[FlashAround(f.box, time_width=1.5, buff=0.12) for f in C.ffs],
                      *[FlashUnder(n, buff=0.08) for n in C.names], run_time=min(1.6, c.until("din")))
            c.wait_until("din")

            d0 = C.ffs[0].d_w
            path = Line(d0.get_start(), d0.get_end()).set_stroke(YELLOW, 8)
            self.play(FlashUnder(C.din, color=BLUE, buff=0.1),
                      VShowPassingFlash(path, time_width=0.6), run_time=1.4)
            c.wait_until("qs")

            # Q -> next D
            qy = C.qy
            paths = [Line(_p(C.ffs[i].box.get_right()[0], qy), _p(C.ffs[i + 1].box.get_left()[0], qy))
                     .set_stroke(YELLOW, 8) for i in range(2)]
            self.play(*[VShowPassingFlash(p, time_width=0.6) for p in paths], run_time=1.4)
            c.wait_until("up to its own label")
            self.play(*[VShowPassingFlash(r.copy().set_stroke(YELLOW, 8), time_width=0.7) for r in C.risers],
                      run_time=1.0)
            for k, word in enumerate(["cue zero", "cue one", "cue two"]):
                c.wait_until(word)
                self.play(FlashUnder(C.qls[k], color=GREEN, buff=0.08), run_time=0.7)
            c.wait_until("clk")

            bus = C.bus.copy().set_stroke(YELLOW, 9)
            self.play(VShowPassingFlash(bus, time_width=0.6), run_time=1.0)
            self.play(*[f.tri.animate.set_stroke(YELLOW, 4) for f in C.ffs],
                      *[FlashAround(f.tri, time_width=1.5, buff=0.1) for f in C.ffs], run_time=1.2)
            c.wait_until("nobubble")

            # inset: one clock input, big, with no bubble -> rising edge
            cx, cy = -3.0, 2.35
            edge = VMobject().set_points_as_corners(
                [_p(-0.9, 0.85), _p(-0.9, 0), _p(0.9, 0), _p(0.9, 0.85)]).set_stroke(FG, 4)
            tri = Polygon(_p(-0.32, 0), _p(0.32, 0), _p(0, 0.5)).set_stroke(YELLOW, 5)
            wire = Line(_p(0, -0.65), _p(0, 0)).set_stroke(YELLOW, 5)
            inset = VGroup(edge, tri, wire).move_to(_p(cx, cy))
            nob = T("no bubble", 30, DIM).next_to(inset, DOWN, buff=0.2)
            tr = square_wave(-1.4, 2.8, cy, [-0.6, 1.4], [0.4, 2.4])
            ups = [up_arrow(x, cy) for x in (-0.6, 1.4)]
            tag = T("rising edge", 32, YELLOW).next_to(tr, RIGHT, buff=0.35)
            self.play(FlashAround(C.ffs[1].tri, time_width=1.5, buff=0.1),
                      FadeIn(inset), *appear(nob), run_time=1.0)
            self.play(Create(tr, rate_func=linear), *[GrowArrow(a) for a in ups], *appear(tag), run_time=1.0)
            self.panel = [inset, nob, tr, *ups, tag]

    # ---------------------------------------------------------------- one edge
    def clip2(self):
        C = self.C
        with self.say("c2.chain.2", gap=1.8) as c:
            self.dig = [L8.digit(s, f) for s, f in zip("100", C.ffs)]
            self.din_v = T("0", 32, DIM).move_to(_p(-4.3, C.qy + 0.28))
            self.trace = square_wave(-5.6, -0.4, TR_Y, RISES, FALLS)
            self.tr_l = T("CLK", 30, YELLOW).next_to(self.trace, LEFT, buff=0.2)
            self.play(*appear(*self.dig, self.din_v, lag=0.2),
                      Create(self.trace, rate_func=linear), FadeIn(self.tr_l), run_time=1.4)
            c.wait_until("Every flip-flop copies")
            self.play(*disappear(*self.panel), run_time=0.8)

            dpaths = [Line(f.d_w.get_start(), f.d_w.get_end()).set_stroke(YELLOW, 8) for f in C.ffs]
            self.play(*[VShowPassingFlash(p, time_width=0.7) for p in dpaths],
                      *[FlashUnder(f.d_l, color=BLUE, buff=0.06) for f in C.ffs], run_time=1.2)
            c.wait_until("left-hand")
            full = [Line(_p(-5.45, C.qy), C.ffs[0].box.get_left() * RIGHT + _p(0, C.qy))] + [
                Line(_p(C.ffs[i].box.get_right()[0], C.qy), _p(C.ffs[i + 1].box.get_left()[0], C.qy))
                for i in range(2)]
            self.play(*[VShowPassingFlash(p.set_stroke(YELLOW, 8), time_width=0.7) for p in full], run_time=1.2)
            c.wait_until("old")

            # the edge: three arrows at the same instant, each carrying its old value
            spans = [(-5.4, -4.15), (-3.05, -0.75), (0.35, 2.65)]
            self.arrows = [Arrow(_p(a, ARROW_Y), _p(b, ARROW_Y), buff=0, stroke_width=5, tip_length=0.2,
                                 color=YELLOW) for a, b in spans]
            srcs = [self.din_v, self.dig[0], self.dig[1]]
            self.ghosts = [s.copy().set_opacity(0.55).move_to(_p(a + 0.3, ARROW_Y - 0.32))
                           for s, (a, _) in zip(srcs, spans)]
            ends = [_p(b - 0.32, ARROW_Y - 0.32) for _, b in spans]
            self.ups = [up_arrow(RISES[0], TR_Y)]
            self.play(GrowArrow(self.ups[0]), *[GrowArrow(a) for a in self.arrows],
                      *[FadeIn(g) for g in self.ghosts],
                      *during([g.animate.move_to(e) for g, e in zip(self.ghosts, ends)], 0.3, 1.0), run_time=1.6)
            self.tag = T("all at once: the old values", 34, YELLOW).move_to(_p(-0.2, 2.0))
            self.play(*appear(self.tag), run_time=1.0)  # early: the beat's caption, said as "old value"
            c.wait_until("move")

            # the bits move one place right
            new = [g for g in self.ghosts]
            self.play(*during(disappear(*self.dig, *self.arrows), 0, 0.45),
                      *during([g.animate.move_to(L8.digit_pos(f)).set_color(GOLD).set_opacity(1)
                               for g, f in zip(new, C.ffs)], 0.35, 1.0), run_time=1.0)
            self.dig = new
            self.shift_a = Arrow(_p(0.8, TR_Y + 0.15), _p(3.8, TR_Y + 0.15), buff=0, stroke_width=6, color=BLUE)
            self.shift_l = T("one place per edge", 30, BLUE).next_to(self.shift_a, DOWN, buff=0.2)
            self.play(GrowArrow(self.shift_a), *appear(self.shift_l), run_time=0.8)

            # two more edges, quicker
            for k, bits in ((1, "001"), (2, "000")):
                old, nd = self.dig, [L8.digit(s, f) for s, f in zip(bits, C.ffs)]
                ua = up_arrow(RISES[k], TR_Y)
                self.ups.append(ua)
                anims, keep = [GrowArrow(ua)], []
                for i in range(3):
                    if old[i].text == nd[i].text:
                        keep.append(old[i])
                    elif k == 2 and i == 2:      # the 1 leaves through Q_2
                        anims += during([old[i].animate.shift(1.7 * RIGHT).set_opacity(0)], 0, 0.6)
                        anims += during(appear(nd[i], shift=None), 0.45, 1.0)
                        keep.append(nd[i])
                    else:
                        anims += swap(old[i], nd[i])
                        keep.append(nd[i])
                self.play(*anims, run_time=0.7)
                if k == 2:
                    self.remove(old[2])
                self.dig = keep
                self.wait(0.7 if k == 1 else 0.15)      # 0, 0, 1 readable before the 1 leaves

    # ---------------------------------------------------------------- what if: latches
    def clip3(self):
        C = self.C
        with self.say("c2.chain.3") as c:
            gone = [*self.dig, self.din_v, self.trace, self.tr_l, *self.ups, self.shift_a, self.shift_l, self.tag]
            self.play(*disappear(*gone), run_time=0.8)
            self.sq, self.en = [], []
            for f in C.ffs:
                b = f.box
                self.sq.append(Square(side_length=0.22).set_stroke(FG, 3).set_fill(BG, 1)
                               .move_to(b.get_bottom()))
                self.en.append(MathTex(r"\mathrm{EN}", font_size=28, color=BLUE)
                               .move_to(b.get_bottom() + 0.3 * UP))
            self.l6 = T("what if: Lecture 6's transparent D latches", 32, DIM).move_to(_p(-0.2, 2.2))
            self.play(*[f.tri.animate.set_stroke(opacity=0).set_fill(opacity=0) for f in C.ffs],
                      *[FadeIn(s) for s in self.sq], *appear(*self.en, shift=None),
                      *set_alpha(C.names, 0), *appear(self.l6), run_time=1.5)   # latches: no FF names
            c.wait_until("race")

            tr = square_wave(-4.0, 4.0, TR_Y, [-2.0], [2.0])
            band = Rectangle(width=4.0, height=0.75).set_stroke(width=0).set_fill(YELLOW, 0.15).move_to(_p(0, TR_Y))
            tl = T("CLK", 30, YELLOW).next_to(tr, LEFT, buff=0.2)
            self.play(Create(tr, rate_func=linear), FadeIn(tl), time_span(FadeIn(band), 0.5, 1.2), run_time=1.2)
            c.wait_until("every stage is open")
            self.play(*[FlashAround(s, time_width=1.5, buff=0.08) for s in self.sq],
                      *[b.animate.set_fill(YELLOW, 0.12) for b in [f.box for f in C.ffs]], run_time=1.0)
            c.wait_until("runs straight through")

            one = T("1", 32, GOLD).move_to(_p(-4.3, C.qy + 0.28))
            self.play(*appear(one, shift=None), run_time=0.5)
            run = Line(_p(-4.56, C.qy), _p(4.61, C.qy)).set_stroke(GOLD, 9)
            ds = [T("1", 40, GOLD).move_to(f.box.get_center() + 0.12 * DOWN) for f in C.ffs]
            anims = [VShowPassingFlash(run, time_width=0.35, rate_func=linear)]
            for i, d in enumerate(ds):
                a = 0.12 + 0.3 * i
                anims += during(appear(d, shift=None), a, a + 0.18)
            self.play(*anims, run_time=1.6)
            c.wait_until("one go")
            x = cross_mark(RED).scale(1.8).move_to(_p(5.45, -0.5))
            self.play(FadeIn(x, scale=1.3), run_time=0.8)
            c.wait_until("instant")

            # an instant, not a window: then back to flip-flops on "the edge"
            self.recap = T("an instant, not a window", 44, t2c={"an instant": YELLOW}).move_to(_p(-0.2, 2.2))
            self.play(*swap(self.l6, self.recap), run_time=min(1.2, c.until("the edge")))
            c.wait_until("the edge")
            self.play(*disappear(tr, tl, band, one, *ds, x, *self.sq, *self.en),
                      *[f.box.animate.set_fill(BG, 0) for f in C.ffs],
                      *[f.tri.animate.set_stroke(YELLOW, 5, opacity=1).set_fill(BG, 1) for f in C.ffs],
                      *[n.animate.set_fill(opacity=1) for n in C.names], run_time=0.9)   # restyle cannot restore from 0
            self.play(*[FlashAround(f.tri, time_width=1.5, buff=0.1) for f in C.ffs], run_time=1.0)
            c.wait_until("nextlec")
            self.next8 = T("Lecture 8: why the hand-over is clean", 30, DIM).move_to(_p(-0.2, -3.0))
            self.play(*appear(self.next8), run_time=1.0)  # early: a tag for the sentence, read as it goes

    # ---------------------------------------------------------------- names
    def clip4(self):
        C = self.C
        with self.say("c2.chain.4", gap=1.0) as c:
            self.play(*disappear(self.recap, self.next8), run_time=0.7)
            title = T("Shift register", 56).move_to(_p(-0.2, 3.05))
            self.play(*appear(title), run_time=1.0)
            c.wait_until("serial")

            br_s = Brace(VGroup(C.din, C.ffs[0].d_w), UP, buff=0.1, color=BLUE)   # D_in and its wire
            lab_s = T("serial input:\none bit\nat a time", 30, t2c={"serial input:": BLUE}, line_spacing=0.9)
            lab_s.next_to(br_s, UP, buff=0.18)
            lab_s.shift(RIGHT * min(0, C.names[0].get_left()[0] - 0.2 - lab_s.get_right()[0]))   # left of "FF0"
            self.play(GrowFromCenter(br_s), *appear(lab_s), run_time=1.2)
            c.wait_until("parallel")

            br_p = Brace(VGroup(*C.qls), UP, buff=0.15, color=GREEN)
            lab_p = T("parallel output: all at once", 32, t2c={"parallel output:": GREEN})
            lab_p.next_to(br_p, UP, buff=0.18)
            self.play(GrowFromCenter(br_p), *appear(lab_p), run_time=1.2)
            for k, word in enumerate(["cue zero", "cue one", "cue two"]):
                c.wait_until(word)
                self.play(FlashUnder(C.qls[k], color=GREEN, buff=0.08), run_time=0.6)
