"""Chapter 2, scene 3: the first lecture, 450 million tokens, and the fixes. Clips c2.history.1 – c2.history.4."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- helpers
def ctx_bar(w, h, n_total, n_fill, color=GOLD, center=ORIGIN, show_frame=False):
    """Series context bar (as ch1_s6's bar): GOLD 0.9 bottom-anchored segments, BG separators (stroke 3).
    The frame is an invisible placeholder for layout unless show_frame (the token gauge only)."""
    frame = Rectangle(width=w, height=h).set_stroke(DIM, 2, opacity=1 if show_frame else 0) \
        .set_fill(opacity=0).move_to(center)
    frame.set_z_index(2)
    seg_h = h / n_total
    segs = VGroup(*[
        Rectangle(width=w, height=seg_h).set_stroke(BG, 3).set_fill(color, 0.9)
        .move_to(frame.get_bottom() + UP * seg_h * (i + 0.5))
        for i in range(n_fill)
    ])
    return frame, segs


def agent_box(w, h, center=ORIGIN):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h).set_stroke(BLUE, 3) \
        .set_fill(BLUE, 0.06).move_to(center)


def page(w=0.8, h=1.0, color=TEAL):
    """A file: a page with a folded corner."""
    f = 0.25
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0])
    body.set_stroke(color, 3).set_fill(color, 0.12)
    fold = VMobject().set_points_as_corners([[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0],
                                             [w / 2, h / 2 - f, 0]]).set_stroke(color, 2)
    return VGroup(body, fold)


def hatch(w, h, spacing=0.18, color=DIM):
    """Diagonal hatching filling a w x h box centred on ORIGIN."""
    lines = VGroup()
    c = -h + spacing / 2
    while c < w:
        x0, x1 = max(0, c), min(w, h + c)
        if x1 > x0:
            lines.add(Line([x0 - w / 2, x0 - c - h / 2, 0], [x1 - w / 2, x1 - c - h / 2, 0])
                      .set_stroke(color, 2))
        c += spacing
    return lines


def thumb():
    r = Rectangle(width=0.46, height=0.32).set_stroke(FG, 1.5).set_fill(BG, 1)
    m = Polygon([-0.17, -0.11, 0], [-0.04, 0.06, 0], [0.04, -0.03, 0], [0.09, 0.02, 0],
                [0.17, -0.11, 0]).set_stroke(width=0).set_fill(TEAL, 0.9)
    s = Dot([0.12, 0.08, 0], radius=0.035, color=GOLD)
    return VGroup(r, m, s)


def card(content, tag, w=8.2, h=0.8):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(GREEN, 3) \
        .set_fill(GREEN, 0.08)
    content.move_to(box.get_left() + RIGHT * (0.3 + content.width / 2))
    t = T(tag, 28, color=DIM).move_to(box.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
    return VGroup(box, content, t)


class History(NarratedScene):
    def construct(self):
        # ============================================================ clip 1
        with self.say("c2.history.1") as c:
            GX, GW, GH, GB = -5.1, 1.2, 5.2, -2.6          # gauge final x, width, height, bottom
            g_frame, g_fill = ctx_bar(GW, GH, 12, 12, center=[GX, GB + GH / 2, 0], show_frame=True)
            limit = Line([GX - 0.8, GB + GH, 0], [GX + 0.8, GB + GH, 0]).set_stroke(RED, 6)
            limit.set_z_index(3)
            limit_lbl = T("the plan's limit", 30, color=RED)
            limit_lbl.next_to(limit, RIGHT, buff=0.2)
            g_lbl = T("≈ 450M tokens", 32).next_to(g_frame, DOWN, buff=0.3)
            gauge = VGroup(g_frame, limit, limit_lbl, g_lbl)
            gauge.shift(RIGHT * 5.1)
            g_fill.shift(RIGHT * 5.1)

            self.play(FadeIn(g_frame), GrowFromCenter(limit), run_time=1.0)
            self.play(FadeIn(limit_lbl, shift=0.3 * LEFT), run_time=0.8)
            c.wait_until("run")
            self.play(FadeIn(g_lbl, shift=0.3 * UP), run_time=0.8)
            self.play(GrowFromEdge(g_fill, DOWN), run_time=c.until("limit"), rate_func=linear)

            # chapters: ch1 built, ch2–ch5 half built
            chapters = VGroup()
            for i in range(5):
                box = Rectangle(width=1.3, height=2.6).set_stroke(BLUE, 3)
                lbl = Mono(f"ch{i + 1}", 32).next_to(box, DOWN, buff=0.25)
                if i == 0:
                    box.set_fill(BLUE, 0.45)
                    chapters.add(VGroup(box, lbl))
                else:
                    lower = Rectangle(width=1.3, height=1.3).set_stroke(width=0).set_fill(DIM, 0.15)
                    lower.move_to(box.get_bottom(), aligned_edge=DOWN)
                    h = hatch(1.3, 1.3).move_to(lower)
                    chapters.add(VGroup(box, lower, h, lbl))
            chapters.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to([2.2, -0.2, 0])
            brace = span_brace(chapters[1][0].get_corner(UL), chapters[4][0].get_corner(UR),
                               direction=UP)
            half = T("half built", 32, color=DIM).next_to(brace, UP, buff=0.15)

            gauge_all = VGroup(gauge, g_fill)
            self.play(FlashAround(limit, color=RED, run_time=1.0, time_width=1.5),
                      time_span(gauge_all.animate.shift(LEFT * 5.1), 0.2, 1.4),
                      time_span(LaggedStart(*[FadeIn(ch, shift=0.3 * UP) for ch in chapters],
                                            lag_ratio=0.15), 0.4, 1.6), run_time=1.6)
            self.play(GrowFromCenter(brace), FadeIn(half, shift=0.3 * DOWN), run_time=0.9)

        # ============================================================ clip 2
        with self.say("c2.history.2") as c:
            main = agent_box(6.2, 6.0, center=[2.4, -0.3, 0])
            main_lbl = T("one main session", 40).move_to([2.4, 2.15, 0])
            m_frame, m_fill = ctx_bar(1.4, 4.2, 11, 10, center=[0.9, -0.9, 0])
            gauge_keep = [gauge_all]
            c.wait_until("did everything")
            sweep_clear(self, time_span(FadeIn(main), 0.5, 1.4),
                        time_span(FadeIn(main_lbl, shift=0.3 * DOWN), 0.7, 1.6),
                        time_span(FadeIn(m_frame), 0.9, 1.6), keep=gauge_keep, run_time=1.6)
            self.play(GrowFromEdge(m_fill, DOWN), run_time=1.2, rate_func=rush_into)
            k854 = T("854k", 44, color=GOLD).next_to(m_fill, RIGHT, buff=0.3).align_to(m_fill, UP)
            self.play(FadeIn(k854, shift=0.3 * DOWN), run_time=0.8)

            c.wait_until("notify")
            bubble = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.5).set_stroke(YELLOW, 3)
            badge = Dot(bubble.get_corner(UR), radius=0.1, color=RED)
            icon = VGroup(bubble, badge).move_to([4.5, 1.0, 0])
            self.play(GrowFromCenter(icon), run_time=0.6)
            self.play(FlashAround(icon, run_time=1.0, time_width=1.5))
            sweep = Arrow(m_fill.get_corner(DL) + LEFT * 0.4 + DOWN * 0.05,
                          m_fill.get_corner(UL) + LEFT * 0.4 + UP * 0.05,
                          buff=0, stroke_width=6, color=GOLD)
            path = Line(m_fill.get_bottom(), m_fill.get_top()).set_stroke(YELLOW, 14)
            self.play(GrowArrow(sweep), VShowPassingFlash(path, time_width=0.5),
                      run_time=2.0, rate_func=linear)
            per_turn = T("≈ 0.8M a turn", 34, color=GOLD)
            per_turn.move_to([1.9, -1.2, 0], aligned_edge=LEFT)
            self.play(FadeIn(per_turn, shift=0.3 * LEFT), run_time=0.9)

            c.wait_until("share")
            slice_ = Rectangle(width=GW, height=0.38 * GH).set_stroke(BG, 3).set_fill(RED, 1)
            slice_.move_to(g_frame.get_bottom(), aligned_edge=DOWN).set_z_index(1)
            slice_lbl = T("170M · 38%", 32, color=RED).next_to(slice_, RIGHT, buff=0.3)
            self.play(GrowFromEdge(slice_, DOWN), run_time=1.2)
            self.play(FadeIn(slice_lbl, shift=0.3 * LEFT), run_time=0.8)

        # ============================================================ clip 3
        with self.say("c2.history.3") as c:
            units = VGroup()
            for frac in (9, 6, 11, 8, 10):
                box = agent_box(1.1, 3.0)
                fr, sg = ctx_bar(0.55, 2.5, 11, frac, center=box.get_center() + DOWN * 0.1)
                units.add(VGroup(box, fr, sg))
            units.arrange(RIGHT, buff=0.6).move_to([2.55, 0.3, 0])
            row_lbl = T("6–11M per scene", 34, color=GOLD).next_to(units, DOWN, buff=0.4)
            keep = gauge_keep + [slice_, slice_lbl]
            sweep_clear(self, time_span(LaggedStart(*[FadeIn(u, shift=0.3 * UP) for u in units],
                                                    lag_ratio=0.15), 0.4, 1.8),
                        keep=keep, run_time=1.8)
            self.play(FadeIn(row_lbl, shift=0.3 * DOWN), run_time=0.8)

            c.wait_until("onboard")
            self.play(*[FadeOut(m) for m in keep],
                      units.animate.scale(0.4).move_to([-4.9, 2.85, 0]),
                      row_lbl.animate.move_to([-3.0, 2.85, 0], aligned_edge=LEFT),
                      run_time=1.0)
            big = agent_box(3.2, 5.4, center=[-1.0, -0.7, 0])
            big_lbl = T("scene agent", 30).move_to([-1.0, 1.6, 0])
            b_frame, b_fill = ctx_bar(1.2, 4.2, 12, 3, center=[-1.0, -1.0, 0])
            docs = page().move_to([-4.8, 0.7, 0])
            others = page().move_to([-4.8, -1.5, 0])
            docs_lbl = Mono("docs", 28, color=TEAL).next_to(docs, DOWN, buff=0.2)
            others_lbl = Mono("other scenes", 28, color=TEAL).next_to(others, DOWN, buff=0.2)
            self.play(TransformFromCopy(units[0][0], big), FadeIn(big_lbl), FadeIn(b_frame),
                      LaggedStart(FadeIn(VGroup(docs, docs_lbl)), FadeIn(VGroup(others, others_lbl)),
                                  lag_ratio=0.4),
                      run_time=1.2)
            pours = [docs.copy(), others.copy(), docs.copy()]
            for p in pours:
                self.add(p)
            dest = b_frame.get_bottom() + UP * 0.5
            onboard = T("≈ 15 turns · 60–80k", 30, color=GOLD)
            onboard.move_to([0.9, b_fill.get_center()[1], 0], aligned_edge=LEFT)
            self.play(*[time_span(p.animate.move_to(dest).scale(0.3).set_opacity(0), 0.3 * i, 0.3 * i + 1.0)
                        for i, p in enumerate(pours)],
                      time_span(GrowFromEdge(b_fill, DOWN), 0.4, 1.6),
                      time_span(FadeIn(onboard, shift=0.3 * LEFT), 1.2, 2.0),
                      run_time=2.0)
            self.remove(*pours)

            c.wait_until("loop")
            C, R = np.array([4.6, 0.3, 0]), 1.25
            angs = [90, -30, 210]
            names = ["render", "image", "patch"]
            nodes = VGroup(*[T(n, 30).move_to(C + R * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0]))
                             for n, a in zip(names, angs)])
            arcs = VGroup()
            for a in angs:
                arc = Arc(radius=R, start_angle=(a - 30) * DEGREES, angle=-60 * DEGREES, arc_center=C)
                arc.set_stroke(DIM, 3).add_tip(tip_length=0.2)
                arcs.add(arc)
            loop_lbl = T("20–60 turns", 32, color=GOLD).move_to(C + DOWN * (R + 0.75))
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.3),
                      LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(loop_lbl, shift=0.3 * DOWN),
                      *[VShowPassingFlash(a.copy().set_stroke(YELLOW, 6), time_width=0.6) for a in arcs],
                      run_time=1.2)

            c.wait_until("images")
            thumbs = VGroup()
            base = b_fill.get_top()[1] + 0.22
            for r in range(7):
                for col in (-0.29, 0.29):
                    thumbs.add(thumb().move_to([-1.0 + col, base + 0.42 * r, 0]))
            img_node = nodes[1].get_center()
            n300 = T("≈ 300 images", 34, color=GOLD).move_to([0.9, 1.7, 0], aligned_edge=LEFT)
            self.play(LaggedStart(*[GrowFromPoint(t, img_node) for t in thumbs], lag_ratio=0.15),
                      time_span(FadeIn(n300, shift=0.3 * LEFT), 0.2, 1.0), run_time=2.4)

        # ============================================================ clip 4
        with self.say("c2.history.4") as c:
            BX = 4.6
            t_frame, t_fill = ctx_bar(1.4, 5.0, 12, 12, center=[BX, 0.4, 0])
            tall = VGroup(t_frame, t_fill)
            heading = T("fewer turns  ·  less context", 40,
                        t2c={"turns": GOLD, "context": GOLD}).move_to([-2.5, 3.25, 0])

            items = [
                ("nested", card(T("nested agents", 30), "context")),
                ("kit", card(T("scene-builder type · cached kit", 30), "context")),
                ("packet", card(VGroup(Mono("vk packet", 30), T("· ≈ 1k tokens", 30)).arrange(RIGHT, buff=0.15),
                                "turns + context")),
                ("check", card(VGroup(Mono("vk check", 30), T("· a lint, not images", 30)).arrange(RIGHT, buff=0.15),
                               "turns")),
                ("lib", card(T("shared helper library", 30), "turns")),
            ]
            cards = VGroup()
            for i, (cue, cd) in enumerate(items):
                cd.move_to([-2.5, 2.1 - 1.1 * i, 0])
                cards.add(cd)
            # the image stack holds through "Each fix aims at turns or context", then clears
            c.wait_until("nested")
            sweep_clear(self, time_span(ReplacementTransform(units, tall), 0.0, 1.4),
                        time_span(row_lbl.animate.next_to(t_frame, DOWN, buff=0.3), 0.0, 1.4),
                        time_span(FadeIn(heading, shift=0.3 * DOWN), 0.8, 1.6),
                        time_span(FadeIn(cards[0], shift=0.4 * RIGHT), 0.8, 1.6),
                        keep=[units, row_lbl], run_time=1.6)
            for (cue, cd) in items[1:]:
                c.wait_until(cue)
                self.play(FadeIn(cd, shift=0.4 * RIGHT), run_time=1.0)

            c.wait_until("result")
            _, new_fill = ctx_bar(1.4, 5.0, 12, 4, color=GREEN, center=[BX, 0.4, 0])
            res_lbl = T("2.3–3.8M per scene", 34, color=GREEN).next_to(t_frame, DOWN, buff=0.3)
            res_sub = T("finished, check-clean", 28, color=GREEN).next_to(res_lbl, DOWN, buff=0.15)
            ghost = DashedVMobject(SurroundingRectangle(t_fill, buff=0).set_stroke(DIM, 2), num_dashes=40)
            self.play(ReplacementTransform(t_fill, new_fill), FadeIn(ghost),
                      FadeTransform(row_lbl, res_lbl), run_time=1.8)
            self.play(FadeIn(res_sub, shift=0.3 * DOWN), run_time=0.8)

            c.wait_until("research")
            rbox = RoundedRectangle(corner_radius=0.15, width=4.3, height=1.3).set_stroke(DIM, 2)
            rtxt = VGroup(T("≈ 90M one-off research", 28, color=DIM),
                          T("done once, reused", 28, color=DIM)).arrange(DOWN, buff=0.15)
            research = VGroup(rbox, rtxt.move_to(rbox)).move_to([BX - 0.2, 1.75, 0])
            self.play(FadeOut(ghost), FadeIn(research, shift=0.3 * DOWN), run_time=1.0)

        self.wait(3.7)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
