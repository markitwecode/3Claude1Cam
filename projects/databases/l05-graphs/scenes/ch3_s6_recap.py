"""Chapter 3, scene 6: recap in a 2 x 3 grid, then next time (Lawrence and Radcliffe). Clips c3.recap.1 – c3.recap.3.

Panels (left to right, top row then bottom row), each a small callback with its short line under it:
  1 two one-edge drawings merging at m (s3 costar_v)   2 one-line V opening into two pieces + YELLOW comma, then a star
  3 mirrored Vs, twin rows, <> -> < beside them, row 2 struck RED 4 s4 kid_chords, 10 choose 2 = 45, 10 choose 3 = 120
  5 s5 potter_collapse rows -> Radcliffe Watson 8, name1 / name2 braced   6 next time: Lawrence, Radcliffe
Then full frame: the co-star V tried between them (0 rows), gone; ch4 s1's open_card() chain grows; held ~8 s.
"""
# style: 2
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch3_s3_twins")
S4 = load_scene("ch3_s4_predict")
S5 = load_scene("ch3_s5_aggregate")
H4 = load_scene("ch4_s1_hook")

CX = (-4.55, 0.0, 4.55)
CY = (1.7, -1.75)
CAP_DY = -1.4


def cell(i):
    return CX[i % 3], CY[i // 3]


def caption(i, text, color=FG):
    cx, cy = cell(i)
    return T(text, 30, color=color).move_to([cx, cy + CAP_DY, 0])


def mini_v(left_at, m_at, right_at, r, size, left="p1", right="p2"):
    v = S3.costar_v(left_at, m_at, right_at, r=r, size=size, left=left, right=right)
    v.remove(*v.tags)
    return v


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()

    # ------------------------------------------------------------ c3.recap.1: panels 1-3
    def clip1(self):
        with self.say("c3.recap.1") as c:
            # panel 1: two one-edge drawings, their m's merge
            cx, cy = cell(0)
            py, my = cy + 1.25, cy - 0.3
            p1 = S3.vnode("p1", PINK, [cx - 1.55, py, 0], 0.4, 28)
            p2 = S3.vnode("p2", PINK, [cx + 1.55, py, 0], 0.4, 28)
            m1 = S3.vnode("m", BLUE, [cx - 0.6, my, 0], 0.4, 28)
            m2 = S3.vnode("m", BLUE, [cx + 0.6, my, 0], 0.4, 28)
            a1, _ = S3.into(p1, m1)
            a2, _ = S3.into(p2, m2)
            merged = mini_v([cx - 1.55, py, 0], [cx, my, 0], [cx + 1.55, py, 0], 0.4, 28)
            c.wait_until("recap")
            self.play(*appear(VGroup(a1, p1, m1), VGroup(a2, p2, m2), shift=None, lag=0.4), run_time=1.2)
            c.wait_until("same name")
            self.play(*flash([m1.lab, m2.lab], color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("same vertex")
            self.play(*during([FadeOut(m2.lab)], 0, 0.3),
                      *during([m1.circ.animate.move_to(merged.m), m2.circ.animate.move_to(merged.m),
                               m1.lab.animate.move_to(merged.m).set_color(YELLOW),
                               Transform(a1, merged.arrows[0]), Transform(a2, merged.arrows[1])], 0.25, 1),
                      run_time=1.6)
            self.remove(m2.circ)
            cap1 = caption(0, "same name, same vertex")
            c.wait_until("two edges")
            self.play(*flash([m1.circ], color=YELLOW, time_width=1.5), *appear(cap1), run_time=1.2)
            self.p1 = [a1, a2, p1, p2, m1, cap1]

            # panel 2: the one-line V opens into two pieces joined by a comma; then any shape (a star)
            cx, cy = cell(1)
            r, sz = 0.32, 24
            top, low = cy + 1.3, cy + 0.3
            v = mini_v([cx - 1.4, top, 0], [cx, low, 0], [cx + 1.4, top, 0], r, sz)
            q1 = S3.vnode("p1", PINK, [cx - 1.75, top, 0], r, sz)
            q2 = S3.vnode("p2", PINK, [cx + 1.75, top, 0], r, sz)
            n1 = S3.vnode("m", BLUE, [cx - 0.75, low, 0], r, sz)
            n2 = S3.vnode("m", BLUE, [cx + 0.75, low, 0], r, sz)
            b1, _ = S3.into(q1, n1)
            b2, _ = S3.into(q2, n2)
            comma = T(",", 96, color=YELLOW).move_to([cx, low + 0.1, 0])
            c.wait_until("r2")
            self.play(*appear(v, shift=None), run_time=1.0)
            c.wait_until("commas")
            self.play(v.left.animate.move_to(q1), v.right.animate.move_to(q2), v.m.animate.move_to(n1),
                      Transform(v.arrows[0], b1), Transform(v.arrows[1], b2),
                      *during(appear(n2, shift=None), 0.5, 1), *during(appear(comma), 0.6, 1), run_time=1.5)
            sp = [cx, cy + 0.6, 0]
            star = mini_v([cx - 1.4, cy + 1.3, 0], sp, [cx + 1.4, cy + 1.3, 0], r, sz)
            p3 = S3.vnode("p3", PINK, [cx, cy - 0.5, 0], r, sz)
            a3 = Arrow(p3.circ.get_top() + 0.04 * UP, star.m.circ.get_bottom() + 0.04 * DOWN, buff=0,
                       stroke_width=4, color=FG, max_tip_length_to_length_ratio=0.45, tip_length=0.18)
            cap2 = caption(1, "one line or commas,\nany shape")
            c.wait_until("any shape")
            self.play(*during(disappear(v, n2, comma), 0, 0.45),
                      *during(appear(VGroup(star, a3, p3), cap2, shift=None, lag=0.3), 0.5, 1), run_time=1.4)
            self.p2 = [star, a3, p3, cap2]

            # panel 3: mirrored Vs, twin rows, <> -> <
            cx, cy = cell(2)
            vy, vm = cy + 1.3, cy + 0.55
            va = mini_v([cx - 1.72, vy, 0], [cx - 1.1, vm, 0], [cx - 0.48, vy, 0], 0.3, 24)
            vb = mini_v([cx + 0.48, vy, 0], [cx + 1.1, vm, 0], [cx + 1.72, vy, 0], 0.3, 24,
                        left="p2", right="p1")
            rows = []
            for k, (a, b) in enumerate((("Chaplin", "Coogan"), ("Coogan", "Chaplin"))):
                y = cy - 0.15 - 0.45 * k
                rows.append(VGroup(T(a, 28).move_to([cx - 0.3, y, 0]), T(b, 28).move_to([cx + 1.3, y, 0])))
            op_at = [cx - 1.65, cy - 0.375, 0]
            ne = Code("<>", size=40)
            ne.find("<>").set_color(YELLOW)
            ne.move_to(op_at)
            lt = Code("<", size=40)
            lt.find("<").set_color(YELLOW)
            lt.move_to(op_at)
            c.wait_until("r3")
            self.play(*appear(va, vb, shift=None, lag=0.4), run_time=1.2)
            c.wait_until("twice")
            self.play(*appear(*rows, ne, shift=None, lag=0.4), run_time=1.4)  # early: the rows and the <> condition
            cap3 = caption(2, "less-than\nkeeps one twin")
            c.wait_until("less-than")
            self.play(*edit(ne, lt), *during(appear(cap3, shift=None), 0.4, 1), run_time=1.3)
            strike = Line(rows[1].get_left() + 0.12 * LEFT, rows[1].get_right() + 0.12 * RIGHT,
                          stroke_width=4, color=RED)
            c.wait_until("keeps exactly one")
            self.play(*set_alpha([vb, rows[1]], DIMMED), Create(strike), run_time=min(0.9, c.until(floor=0.4) - 0.1))
            self.p3 = [va, vb, *rows, lt, strike, cap3]

    # ------------------------------------------------------------ c3.recap.2: panels 4-5
    def clip2(self):
        with self.say("c3.recap.2") as c:
            cx, cy = cell(3)
            kc = S4.kid_chords()
            lab45 = kc.label
            kc.remove(lab45)
            kc.ring.movie.remove(kc.ring.movie.lab)
            kc.scale(1.6 / kc.ring.height).move_to([cx, cy + 0.95, 0])
            lab45.scale(30 / 36).move_to([cx, cy - 0.22, 0])
            lab120 = T("10 choose 3 = 120", 30, color=GOLD).move_to([cx, cy - 0.62, 0])
            cap4 = caption(3, "predict the count")
            self.play(*appear(kc.ring, cap4, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("ten actors")
            self.play(LaggedStart(*[Create(ch) for ch in kc.chords], lag_ratio=0.06),
                      run_time=min(1.8, c.until("forty-five")))
            c.wait_until("forty-five")
            self.play(*appear(lab45), run_time=1.0)
            c.wait_until("hundred")
            self.play(*appear(lab120), run_time=1.0)
            self.p4 = [*kc.chords, kc.ring, lab45, lab120, cap4]

            # panel 5: eight rows collapse into 8; the non-aggregates are the keys
            cx, cy = cell(4)
            pc = S5.potter_collapse()
            tab = VGroup(pc.header, pc.rule, *pc.rows)
            tab.scale(1.6 / tab.height).move_to([cx, cy + 0.95, 0])
            res = VGroup(T("Radcliffe", 30), T("Watson", 30), T("8", 36, color=GOLD)).arrange(RIGHT, buff=0.6)
            res[2].align_to(res[0], DOWN)
            res.move_to([cx, cy + 0.85, 0])
            res.p1, res.p2, res.count = res
            c.wait_until("r5")
            self.play(*appear(pc.header, pc.rule, *pc.rows, shift=None, lag=0.05), run_time=1.2)  # early: a picture of the rows
            c.wait_until("everything")
            self.play(*during(disappear(pc.header, pc.rule, *pc.rows, lag=0.03), 0, 0.5),  # early: the collapsed row, read later
                      *during(appear(res, shift=None), 0.5, 1), run_time=1.6)
            cap5 = caption(4, "non-aggregates\nare the keys")
            c.wait_until("aggregates")
            self.play(*flash([res.count], color=GOLD, time_width=1.5), *appear(cap5), run_time=1.0)
            braces, names = [], []
            for part, nm in ((res.p1, "name1"), (res.p2, "name2")):
                b = span_brace(part.get_left(), part.get_right(), DOWN, color=YELLOW, buff=0.12)
                b.move_to([part.get_x(), res.get_bottom()[1] - 0.12 - b.height / 2, 0])
                braces.append(b)
                names.append(Mono(nm, 28, color=YELLOW).next_to(b, DOWN, buff=0.12))
            c.wait_until("grouping")
            self.play(*[GrowFromCenter(b) for b in braces], *appear(*names, lag=0.2),
                      run_time=min(1.0, c.until(floor=0.5)))
            self.p5 = [res, *braces, *names, cap5]

    # ------------------------------------------------------------ c3.recap.3: next time
    def clip3(self):
        card = H4.open_card()
        jl, dr = card.pair.jl, card.pair.dr
        cx, cy = cell(5)
        sl = H4.vertex(color=PINK, r=0.4).circle.move_to([cx - 1.2, cy + 0.75, 0])
        sr = H4.vertex(color=PINK, r=0.4).circle.move_to([cx + 1.2, cy + 0.75, 0])
        nl = T("Lawrence", 28).next_to(sl, DOWN, buff=0.2)
        nr = T("Radcliffe", 28).next_to(sr, DOWN, buff=0.2)
        cap6 = caption(5, "next time", YELLOW)
        with self.say("c3.recap.3", gap=0.35) as c:
            self.play(*appear(sl, sr, shift=None), *appear(nl, nr, cap6, lag=0.3), run_time=1.2)  # early: the two names
            c.wait_until("never")
            old = [*self.p1, *self.p2, *self.p3, *self.p4, *self.p5, nl, nr, cap6]
            self.play(*during([FadeOut(m) for m in old], 0, 0.45),
                      *during([ReplacementTransform(sl, jl.circle), ReplacementTransform(sr, dr.circle)], 0.3, 0.9),
                      *during(appear(jl.label, dr.label, shift=None), 0.75, 1), run_time=1.8)

            # the co-star V tried between them
            m = S3.vnode("m", BLUE, [0, 1.6, 0], 0.6, 40)
            arr_l, tag_l = S3.into(SimpleNamespace(circ=jl.circle), m)
            arr_r, tag_r = S3.into(SimpleNamespace(circ=dr.circle), m)
            c.wait_until("co-star")
            self.play(GrowArrow(arr_l), GrowArrow(arr_r), *appear(m, tag_l, tag_r, shift=None, lag=0.2),
                      run_time=1.4)
            zero = T("0 rows", 40, t2c={"0": GOLD}).move_to([0, 0.0, 0])
            c.wait_until("nothing")
            self.play(*appear(zero), m.circ.animate.set_stroke(RED), run_time=1.0)

            # chains of any length
            ch = card.pair.chain
            dash, dots = ch[0], list(ch[1:])
            c.wait_until("chain")
            self.play(*during(disappear(arr_l, arr_r, m, tag_l, tag_r), 0, 0.3),
                      *during([Create(dash, lag_ratio=1.0, rate_func=linear)], 0.3, 1),
                      *[a for k, d in enumerate(dots)
                        for a in during([FadeIn(d, scale=0.5)], 0.24 + 0.7 * (k + 1) / 6, 0.36 + 0.7 * (k + 1) / 6)],
                      run_time=2.6)
            c.wait_until(own_word=card.line, cue="any length")
            self.play(*during(disappear(zero), 0, 0.4), *during(appear(card.pair.q, card.line, lag=0.3), 0.4, 1),
                      run_time=1.6)
        # end card, exactly ch4 s1's first frame, held unchanged
        self.remove(*self.mobjects)
        self.add(card)
        self.wait(7.6)
