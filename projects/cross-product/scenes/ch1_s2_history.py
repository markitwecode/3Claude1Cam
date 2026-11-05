"""Chapter 1, scene 2: Hamilton's product, split in two. Clips c1.hist.1 – c1.hist.4.

Layout: a GOLD-ticked timeline along the bottom for the whole scene (1843, 1844, 1873, 1880s,
1890s). Clip 1: Broom Bridge silhouette, the rule carved into its face. Clip 2: the rule rides as a
header; q = w + xi + yj + zk (scalar GOLD / vector TEAL); the product of two pure arrows splits into
-a.b (GOLD) + a x b (TEAL). Clip 3: that equation rides as a dim header over Grassmann, Maxwell,
Gibbs/Heaviside, then cracks at the plus and its halves fly apart. Clip 4: dot/cross names, the
Nature letter war, vectors win; only a x b stays.

Handoff to ch1_s3: ends on MathTex(r"\\mathbf a\\times\\mathbf b", font_size=72, color=TEAL) alone
at ORIGIN, held ~2 s, then faded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TL_Y = -2.95
TICK_X = {"1843": -5.3, "1844": -3.6, "1873": -0.8, "1880s": 2.0, "1890s": 4.7}
HEAD_Y = 3.1
STONE = "#3A3F48"
STONE_EDGE = "#8C929C"
Q_TEX = ("q", "=", "w", "+", r"x\,\mathbf i+y\,\mathbf j+z\,\mathbf k")
PROD_TEX = ("(", "a_1", r"\mathbf i", "+", "a_2", r"\mathbf j", "+", "a_3", r"\mathbf k", ")",
            "(", "b_1", r"\mathbf i", "+", "b_2", r"\mathbf j", "+", "b_3", r"\mathbf k", ")")
RHS_TEX = ("=", r"-\,", r"\mathbf a\cdot\mathbf b", "+", r"\mathbf a\times\mathbf b")

BASE, DECK = -1.6, 1.25          # bridge water line and deck top
ARCH_W, ARCH_H = 2.1, 1.35       # arch opening (half-width, height)
RING_W, RING_H = 2.4, 1.6        # arch ring


def glyph(m, i):
    """Glyph i of a MathTex part (the dry run's stub MathTex may have fewer)."""
    return m[i] if len(m.submobjects) > i else m


def ts(anim, a, b, rt):
    """time_span as fractions of the play's run_time (safe when run_time is cue-clamped)."""
    return time_span(anim, a * rt, b * rt)


def p3(x, y):
    return np.array([x, y, 0.0])


def stone_bridge():
    pts = [p3(-4.7, BASE), p3(-4.25, DECK - 0.2), p3(-4.05, DECK), p3(4.05, DECK),
           p3(4.25, DECK - 0.2), p3(4.7, BASE), p3(ARCH_W, BASE)]
    for th in np.linspace(0, PI, 49)[1:-1]:
        pts.append(p3(ARCH_W * np.cos(th), BASE + ARCH_H * np.sin(th)))
    pts += [p3(-ARCH_W, BASE), p3(-4.7, BASE)]
    body = VMobject().set_points_as_corners(pts)
    body.set_fill(STONE, 1).set_stroke(STONE_EDGE, 3)
    coping = Line(p3(-4.05, DECK - 0.2), p3(4.05, DECK - 0.2), color=STONE_EDGE, stroke_width=2)
    ring = VMobject().set_points_as_corners(
        [p3(RING_W * np.cos(th), BASE + RING_H * np.sin(th)) for th in np.linspace(0, PI, 49)])
    ring.set_stroke(STONE_EDGE, 2)
    vous = VGroup(*[
        Line(p3(ARCH_W * np.cos(th), BASE + ARCH_H * np.sin(th)),
             p3(RING_W * np.cos(th), BASE + RING_H * np.sin(th)), color=STONE_EDGE, stroke_width=2)
        for th in np.linspace(0, PI, 11)[1:-1]])
    water = Line(p3(-5.6, BASE), p3(5.6, BASE), color=BLUE, stroke_width=3)
    ripples = VGroup(Line(p3(-1.2, BASE - 0.2), p3(-0.4, BASE - 0.2)),
                     Line(p3(0.3, BASE - 0.32), p3(1.1, BASE - 0.32)))
    ripples.set_stroke(BLUE, 2, opacity=0.7)
    return VGroup(water, ripples, body, coping, ring, vous)


def make_book():
    cover = RoundedRectangle(corner_radius=0.08, width=2.3, height=3.0)
    cover.set_fill("#1B2F4A", 1).set_stroke(BLUE, 3)
    spine = Line(cover.get_corner(UL) + 0.28 * RIGHT, cover.get_corner(DL) + 0.28 * RIGHT,
                 color=BLUE, stroke_width=3)
    frame = Rectangle(width=1.45, height=1.0).set_stroke(GOLD, 2)
    frame.move_to(cover.get_center() + 0.55 * UP + 0.14 * RIGHT)
    bars = VGroup(*[Line(0.5 * LEFT, 0.5 * RIGHT, color=GOLD, stroke_width=3) for _ in range(2)])
    bars.arrange(DOWN, buff=0.2).move_to(frame)
    foot = Line(0.35 * LEFT, 0.35 * RIGHT, color=GOLD, stroke_width=3)
    foot.move_to(cover.get_center() + 0.85 * DOWN + 0.14 * RIGHT)
    return VGroup(cover, spine, frame, bars, foot)


def letter_card():
    box = RoundedRectangle(corner_radius=0.06, width=1.5, height=0.7)
    box.set_fill(BG, 1).set_stroke(FG, 2)
    word = T("Nature", 28, slant=ITALIC).move_to(box)
    return VGroup(box, word)


def fly_card(card, path):
    card.move_to(path.get_start()).set_opacity(0)

    def upd(m, t):
        m.move_to(path.point_from_proportion(t))
        m.set_opacity(min(1.0, 5 * t, 5 * (1 - t)))
    return UpdateFromAlphaFunc(card, upd)


class HistoryScene(NarratedScene):
    def construct(self):
        self.tl = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---------------------------------------------------------------- helpers
    def tick(self, year):
        x = TICK_X[year]
        ln = Line(p3(x, TL_Y - 0.14), p3(x, TL_Y + 0.14), color=GOLD, stroke_width=4)
        lab = T(year, 30, GOLD).next_to(ln, DOWN, buff=0.1)
        self.tl += [ln, lab]
        return [GrowFromCenter(ln), FadeIn(lab, shift=0.2 * UP)]

    def beat(self, c, nxt, *anims, rt=1.5, frac=0.75):
        avail = c.until(nxt) if nxt else c.remaining
        self.play(*anims, run_time=max(0.3, min(rt, frac * avail)))
        if nxt:
            c.wait_until(nxt)

    # ---------------------------------------------------------------- clip 1: the bridge
    def clip1(self):
        with self.say("c1.hist.1") as c:
            bridge = stone_bridge()
            cap = T("Brougham (Broom) Bridge, Royal Canal, Dublin", 30, DIM).move_to(p3(0, -2.3))
            self.beat(c, "sixteenth of October",
                      FadeIn(bridge, shift=0.2 * UP), FadeIn(cap, shift=0.2 * UP), rt=1.6)

            date = T("16 October 1843", 48).move_to(p3(0, 3.05))
            self.tl_line = Line(p3(-6.3, TL_Y), p3(6.3, TL_Y), color=DIM, stroke_width=3)
            self.tl.append(self.tl_line)
            rt = min(1.5, 0.75 * c.until("hamilton"))
            self.play(FadeIn(date, shift=0.3 * DOWN), Create(self.tl_line),
                      *[ts(a, 0.4, 1.0, rt) for a in self.tick("1843")], run_time=rt)
            c.wait_until("hamilton")

            name = T("William Rowan Hamilton", 40, YELLOW).move_to(p3(0, 2.2))
            self.beat(c, "in a flash", FadeIn(name, shift=0.3 * DOWN), rt=1.0)

            face = p3(0, (BASE + RING_H + DECK - 0.2) / 2)
            self.beat(c, "carve", Flash(face, color=YELLOW, line_length=0.45, num_lines=14,
                                        flash_radius=0.7, line_stroke_width=4), rt=1.0, frac=0.9)

            self.beat(c, "rule", *[m.animate.set_opacity(0.4) for m in (date, name, cap)], rt=1.0)

            self.rule = MathTex(r"i^2=j^2=k^2=ijk=-1", font_size=60).move_to(face)
            write_t = min(c.remaining - 0.3, max(2.5, c.until("minus one") + 0.6))
            self.play(Write(self.rule, rate_func=linear), run_time=write_t)

    # ---------------------------------------------------------------- clip 2: quaternions, the product
    def clip2(self):
        with self.say("c1.hist.2") as c:
            rule = self.rule
            q = MathTex(*Q_TEX, font_size=72).move_to(p3(0, 0.75))
            rule.generate_target()
            rule.target.scale(0.7).move_to(p3(0, HEAD_Y))
            rt = min(1.7, 0.8 * c.until("number part"))
            sweep_clear(self, MoveToTarget(rule), ts(Write(q), 0.3, 1.0, rt),
                        keep=[rule, *self.tl], run_time=rt)
            c.wait_until("number part")

            self.beat(c, "arrow part", FlashUnder(q[2], color=GOLD), rt=1.0, frac=0.9)
            self.beat(c, "names", FlashUnder(q[4], color=TEAL), rt=1.0, frac=0.9)

            h = q.height + 0.3
            wbox = Rectangle(width=q[2].width + 0.32, height=h).set_stroke(GOLD, 4)
            wbox.move_to(p3(q[2].get_x(), q.get_y()))
            vbox = Rectangle(width=q[4].width + 0.32, height=h).set_stroke(TEAL, 4)
            vbox.move_to(p3(q[4].get_x(), q.get_y()))
            slab = T("scalar", 36, GOLD).next_to(wbox, DOWN, buff=0.25)
            vlab = T("vector", 36, TEAL).next_to(vbox, DOWN, buff=0.25)
            self.beat(c, "the vector part", Create(wbox), q[2].animate.set_color(GOLD),
                      FadeIn(slab, shift=0.25 * UP), rt=1.0)
            self.beat(c, "multiply", Create(vbox), q[4].animate.set_color(TEAL),
                      FadeIn(vlab, shift=0.25 * UP), rt=1.0)

            # the rule leaves; q with its two named parts rides up as the header
            for m in (q, wbox, vbox):
                m.generate_target()
            VGroup(q.target, wbox.target, vbox.target).scale(0.62).move_to(p3(0, 3.18))
            slab.target = T("scalar", 30, GOLD).next_to(wbox.target, DOWN, buff=0.1)
            vlab.target = T("vector", 30, TEAL).next_to(vbox.target, DOWN, buff=0.1)
            self.qhead = [q, wbox, vbox, slab, vlab]

            prod = MathTex(*PROD_TEX, font_size=56).move_to(p3(0, 0.95))
            for i in (1, 4, 7):
                prod[i].set_color(BLUE)
            for i in (11, 14, 17):
                prod[i].set_color(YELLOW)
            self.prod = prod
            rt = min(1.8, 0.85 * c.until("split"))
            sweep_clear(self, *[MoveToTarget(m) for m in self.qhead], ts(Write(prod), 0.3, 1.0, rt),
                        keep=[*self.qhead, *self.tl], run_time=rt)
            c.wait_until("split")

            rhs = MathTex(*RHS_TEX, font_size=60).move_to(p3(0, -0.4))
            glyph(rhs[2], 0).set_color(BLUE)
            glyph(rhs[2], 2).set_color(YELLOW)
            glyph(rhs[4], 0).set_color(BLUE)
            glyph(rhs[4], 2).set_color(YELLOW)
            self.rhs = rhs
            self.beat(c, "dot", ReplacementTransform(prod.copy(), rhs), rt=1.8, frac=0.8)

            nb = Brace(VGroup(rhs[1], rhs[2]), DOWN, buff=0.15, color=GOLD)
            nl = T("a number", 34, GOLD).next_to(nb, DOWN, buff=0.15)
            self.beat(c, "cross", rhs[1].animate.set_color(GOLD), rhs[2].animate.set_color(GOLD),
                      GrowFromCenter(nb), FadeIn(nl, shift=0.25 * DOWN), rt=1.2)

            vb = Brace(rhs[4], DOWN, buff=0.15, color=TEAL)
            vl = T("a vector", 34, TEAL).next_to(vb, DOWN, buff=0.15)
            vl.match_y(nl)
            self.beat(c, None, rhs[4].animate.set_color(TEAL),
                      GrowFromCenter(vb), FadeIn(vl, shift=0.25 * DOWN), rt=1.2)

    # ---------------------------------------------------------------- clip 3: Grassmann .. Gibbs/Heaviside
    def clip3(self):
        with self.say("c1.hist.3") as c:
            prod, rhs = self.prod, self.rhs
            self.beat(c, "Hermann Grassmann", *self.tick("1844"), rt=1.0)

            # the equation rides along as a dim one-line header; q's header, braces, labels go
            prod.generate_target()
            rhs.generate_target()
            row = VGroup(prod.target, rhs.target).arrange(RIGHT, buff=0.2)
            rhs.target.shift((prod.target.get_y() - rhs.target[0].get_y()) * UP)
            row.scale_to_fit_width(8.6).move_to(p3(0, HEAD_Y))
            prod.target.set_opacity(0.6)
            rhs.target.set_opacity(0.6)
            gname = T("Hermann Grassmann", 40, YELLOW).move_to(p3(0, 2.05))
            rt = min(1.4, 0.9 * c.until("two vectors"))
            sweep_clear(self, MoveToTarget(prod), MoveToTarget(rhs),
                        ts(FadeIn(gname, shift=0.3 * DOWN), 0.45, 1.0, rt),
                        keep=[prod, rhs, *self.tl], run_time=rt)
            c.wait_until("two vectors")

            O, A, B = p3(-2.5, -1.45), p3(3.6, 0.3), p3(1.3, 2.0)
            va = Arrow(O, O + A, buff=0, color=BLUE, stroke_width=6)
            vb = Arrow(O, O + B, buff=0, color=YELLOW, stroke_width=6)
            la = MathTex(r"\mathbf a", font_size=48, color=BLUE).next_to(O + 0.55 * A, DOWN, buff=0.15)
            lb = MathTex(r"\mathbf b", font_size=48, color=YELLOW).next_to(O + 0.5 * B, LEFT, buff=0.15)
            self.beat(c, "piece of plane",
                      LaggedStart(GrowArrow(va), GrowArrow(vb), lag_ratio=0.3),
                      FadeIn(la, lb), rt=1.1, frac=0.8)

            style = dict(fill_color=PURPLE, fill_opacity=0.45, stroke_color=PURPLE, stroke_width=2)

            def para(t):
                t = max(t, 1e-3)
                return Polygon(O, O + A, O + A + t * B, O + t * B, **style)
            patch = para(0)
            self.add(patch)
            self.bring_to_back(patch)
            C = O + (A + B) / 2
            orient = Arc(radius=0.45, start_angle=-0.5, angle=1.55 * PI, arc_center=C,
                         color=FG, stroke_width=4).add_tip(tip_length=0.2)
            plab = T("a piece of plane", 36).move_to(O + B + A / 2 + 0.55 * UP)
            rt = min(1.6, 0.8 * c.until("maxwell"))
            self.play(UpdateFromAlphaFunc(patch, lambda m, t: m.become(para(t))),
                      ts(Create(orient), 0.5, 1.0, rt),
                      ts(FadeIn(plab, shift=0.2 * DOWN), 0.5, 1.0, rt), run_time=rt)
            c.wait_until("maxwell")

            # Maxwell, 1873: Grassmann shrinks left and dims, the book comes in on the right
            grass = [gname, va, vb, la, lb, orient, plab]
            for m in grass + [patch]:
                m.generate_target()
            tg = VGroup(*[m.target for m in grass + [patch]])
            tg.scale(0.8).move_to(p3(-3.6, tg.get_y()))
            for m in grass:
                if m is orient:      # an open arc: dim the stroke, keep it unfilled; the tip is filled
                    m.target.set_stroke(opacity=0.5)
                    for sub in m.target.submobjects:
                        sub.set_fill(opacity=0.5)
                else:
                    m.target.set_opacity(0.5)
            patch.target.set_fill(opacity=0.22).set_stroke(opacity=0.5)

            book = make_book().scale(0.85)
            mname = T("Maxwell", 44, YELLOW)
            mlines = VGroup(*[T(s, 32, slant=ITALIC) for s in ("A Treatise on", "Electricity and", "Magnetism")])
            mlines.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            mtext = VGroup(mname, mlines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            VGroup(book, mtext).arrange(RIGHT, buff=0.5).move_to(p3(2.2, 0.1))
            rt = min(1.7, 0.8 * c.until("Hamilton's language"))
            self.play(*[MoveToTarget(m) for m in grass + [patch]], *self.tick("1873"),
                      ts(FadeIn(book, shift=0.3 * UP), 0.3, 0.85, rt),
                      ts(FadeIn(mtext, shift=0.3 * DOWN), 0.45, 1.0, rt), run_time=rt)
            c.wait_until("Hamilton's language")

            # "Hamilton's language": the quaternion equation lights back up
            self.beat(c, "gibbs", prod.animate.set_opacity(1), rhs.animate.set_opacity(1),
                      FlashAround(VGroup(prod, rhs), color=YELLOW, time_width=1.5), rt=1.6)

            # Gibbs and Heaviside, 1880s
            ggrp = VGroup(T("J. Willard Gibbs", 40, YELLOW), T("Yale", 32, DIM)).arrange(DOWN, buff=0.18)
            ggrp.move_to(p3(-4.1, 1.65))
            hgrp = VGroup(T("Oliver Heaviside", 40, YELLOW), T("England", 32, DIM)).arrange(DOWN, buff=0.18)
            hgrp.move_to(p3(4.1, 1.65))
            indep = T("independently", 30, DIM, slant=ITALIC).match_y(ggrp[0])
            rt = min(1.5, 0.8 * c.until("heaviside"))
            sweep_clear(self, *self.tick("1880s"), ts(FadeIn(ggrp, shift=0.3 * DOWN), 0.4, 1.0, rt),
                        keep=[prod, rhs, *self.tl], run_time=rt)
            c.wait_until("heaviside")
            self.beat(c, "each on his own", FadeIn(hgrp, shift=0.3 * DOWN), rt=1.0)
            self.beat(c, "apart", FadeIn(indep), rt=0.8)
            self.ggrp, self.hgrp, self.indep = ggrp, hgrp, indep

            # the equation cracks at the plus; the halves fly apart
            self.remove(rhs)
            self.add(*rhs)
            dotp, crossp = rhs[2], rhs[4]
            plus = rhs[3]
            crack = VMobject().set_points_as_corners([
                plus.get_center() + p3(dx, dy) for dx, dy in
                ((0.02, 0.42), (-0.07, 0.2), (0.07, 0.02), (-0.06, -0.18), (0.03, -0.42))])
            crack.set_stroke(FG, 3)
            fall = [prod, rhs[0], rhs[1], plus]
            rt = min(1.3, 0.85 * c.until("kept its two halves"))
            self.play(ts(Create(crack), 0.0, 0.4, rt),
                      *[ts(m.animate.shift(0.3 * DOWN).set_opacity(0.3), 0.3, 1.0, rt) for m in fall],
                      ts(dotp.animate.shift(0.35 * LEFT), 0.3, 1.0, rt),
                      ts(crossp.animate.shift(0.35 * RIGHT), 0.3, 1.0, rt), run_time=rt)
            c.wait_until("kept its two halves")

            ref_d = MathTex(r"\mathbf a\cdot\mathbf b", font_size=72)
            ref_c = MathTex(r"\mathbf a\times\mathbf b", font_size=72)
            dotp.generate_target()
            dotp.target.scale(ref_d.width / dotp.width).move_to(p3(-2.8, 0.25))
            crossp.generate_target()
            crossp.target.scale(ref_c.width / crossp.width).move_to(p3(2.8, 0.25))
            self.beat(c, None, *[FadeOut(m, shift=0.3 * DOWN) for m in fall + [crack]],
                      MoveToTarget(dotp), MoveToTarget(crossp), rt=1.8)
            self.dotp, self.crossp = dotp, crossp

    # ---------------------------------------------------------------- clip 4: names, war, the arrow half
    def clip4(self):
        with self.say("c1.hist.4") as c:
            dotp, crossp = self.dotp, self.crossp
            self.beat(c, "with a cross",
                      *[m.animate.set_opacity(DIMMED) for m in (self.hgrp, self.indep)],
                      glyph(dotp, 1).animate(rate_func=there_and_back).scale(2.6), rt=1.2, frac=0.85)

            quote = VGroup(
                T("“It is written C = A × B and read A cross B.", 28, slant=ITALIC),
                T("For this reason it is often called the cross product.”", 28, slant=ITALIC),
                T("Gibbs–Wilson, Vector Analysis (1901)", 28, DIM),
            ).arrange(DOWN, buff=0.12).move_to(p3(0, -1.85))
            self.beat(c, "the names", glyph(crossp, 1).animate(rate_func=there_and_back).scale(2.0),
                      FadeIn(quote, shift=0.2 * UP), rt=1.1, frac=0.85)

            dlab = T("dot product", 36, GOLD).next_to(dotp, DOWN, buff=0.4)
            clab = T("cross product", 36, TEAL).next_to(crossp, DOWN, buff=0.4)
            self.beat(c, "war", FadeIn(dlab, shift=0.25 * DOWN), FadeIn(clab, shift=0.25 * DOWN), rt=1.1)

            # 1890s: the two camps; the products regroup on the vectors side
            dot_t = dotp.copy().scale(0.85).move_to(p3(0, 0.75))
            cross_t = crossp.copy().scale(0.85).move_to(p3(0, -0.3)).align_to(dot_t, LEFT)
            lx = max(dot_t.get_right()[0], cross_t.get_right()[0]) + 0.45
            dlab_t = dlab.copy().match_y(dot_t)
            dlab_t.set_x(lx + dlab_t.width / 2)
            clab_t = clab.copy().match_y(cross_t)
            clab_t.set_x(lx + clab_t.width / 2)
            rows = VGroup(dot_t, cross_t, dlab_t, clab_t)
            rows.move_to(p3(3.9, 0.22))
            for m, t in ((dotp, dot_t), (crossp, cross_t), (dlab, dlab_t), (clab, clab_t)):
                m.target = t
            quat_h = T("quaternions", 44).move_to(p3(-3.9, 1.8))
            vec_h = T("vectors", 44).move_to(p3(rows.get_x(), 1.8))
            q2 = MathTex(*Q_TEX, font_size=48).move_to(p3(-3.9, 0.25))
            rt = min(1.9, 0.9 * c.until("fought it out"))
            self.play(FadeOut(self.ggrp, self.hgrp, self.indep), *self.tick("1890s"),
                      *[MoveToTarget(m) for m in (dotp, crossp, dlab, clab)],
                      ts(FadeIn(quat_h, q2, shift=0.3 * DOWN), 0.45, 1.0, rt),
                      ts(FadeIn(vec_h, shift=0.3 * DOWN), 0.55, 1.0, rt), run_time=rt)
            c.wait_until("fought it out")

            cards = [letter_card() for _ in range(3)]
            paths = [ArcBetweenPoints(p3(-1.6, 1.15), p3(1.6, 1.15), angle=-PI / 3),
                     ArcBetweenPoints(p3(1.6, 0.95), p3(-1.6, 0.95), angle=-PI / 4),
                     ArcBetweenPoints(p3(-1.6, 1.2), p3(1.6, 1.2), angle=-PI / 2.5)]
            self.beat(c, "won", LaggedStart(*[fly_card(k, p) for k, p in zip(cards, paths)],
                                            lag_ratio=0.35), rt=2.8, frac=0.95)
            self.remove(*cards)

            self.beat(c, "why", vec_h.animate.set_color(GREEN),
                      quat_h.animate.set_opacity(DIMMED), q2.animate.set_opacity(DIMMED), rt=1.0)

            final = MathTex(r"\mathbf a\times\mathbf b", font_size=72, color=TEAL).move_to(ORIGIN)
            others = [m for m in self.mobjects if m is not crossp]
            self.play(LaggedStart(*[FadeOut(m) for m in others], lag_ratio=0.06),
                      ReplacementTransform(crossp, final), run_time=min(1.6, c.remaining - 0.2))
