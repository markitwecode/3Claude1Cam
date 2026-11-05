"""Chapter 2, scene 4: where the tokens go now. Clips c2.split.1 – c2.split.5.

Built from the briefs (no ch1_s2 / ch2_s1 / ch2_s2 files existed): master shot, question card and
staircase styling are defined here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

K = 0.0125      # units per 1k tokens
B = -2.0        # staircase baseline
NB = 25


def agent(w, h, label=None, size=30, mono=False, outline=BLUE, fill_op=0.15, label_color=FG):
    # copied from scenes/ch1_s2_crew.py
    back = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(width=0).set_fill(BG, 1)
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(outline, 3).set_fill(BLUE, fill_op)
    g = VGroup(back, rect)
    if label:
        t = (Mono if mono else T)(label, size=size, color=label_color)
        if t.width > w - 0.2:
            t.scale_to_fit_width(w - 0.2)
        g.add(t)
    return g


def builder_box(w, h):
    return RoundedRectangle(corner_radius=min(0.15, h / 3), width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)


def row_xs(cx, n, w, gap):
    pitch = w + gap
    return [cx + (i - (n - 1) / 2) * pitch for i in range(n)]


def conn(a, b, width=2):
    return Line(a.get_bottom(), b.get_top()).set_stroke(DIM, width).set_z_index(-1)


ROW = 26.5
FILES_C = ManimColor(GOLD).interpolate(ManimColor(WHITE), 0.32)
REPLIES_C = ManimColor(GOLD).interpolate(ManimColor(BG), 0.32)
THINK_C = ManimColor(GOLD).interpolate(ManimColor(RED), 0.45)
BAR_COLS = [GOLD, FILES_C, REPLIES_C, THINK_C, GOLD]


def context_bar(heights, x, bottom, width=0.9):
    # as scenes/ch2_s2_turns.py context_bar (regrouped shades of GOLD, BG separators)
    segs = VGroup()
    y = bottom
    for k, h in enumerate(heights):
        h = max(h, 0.002)
        seg = Rectangle(width=width, height=h).set_fill(BAR_COLS[k], 0.9).set_stroke(BG, 3)
        seg.move_to([x, y + h / 2, 0])
        segs.add(seg)
        y += h
    return segs


def box(label, w, h=0.7, color=BLUE, size=28):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3)
    r.set_fill(color, 0.18)
    return VGroup(r, T(label, size=size))


def stair_bar(i, cx):
    h = (12 + 120 * (i / (NB - 1)) ** 0.8) * K
    x = cx - 2.5 + 0.1 + i * 0.2
    body = Rectangle(width=0.17, height=h - 0.07).set_fill(GREEN, 1).set_stroke(width=0)
    gold = Rectangle(width=0.17, height=0.035).set_fill(GOLD, 1).set_stroke(width=0)
    red = Rectangle(width=0.17, height=0.035).set_fill(RED, 1).set_stroke(width=0)
    body.move_to([x, B + (h - 0.07) / 2, 0])
    gold.move_to([x, B + h - 0.0525, 0])
    red.move_to([x, B + h - 0.0175, 0])
    return VGroup(body, gold, red)


def shift_all(items, vec):
    return [m.animate.shift(vec) for m in items]


# Manim CE's Brace path, with the two arms given separate lengths so the tip can sit off-centre.
_BRACE_PATH = (
    "m0.01216 0c-0.01152 0-0.01216 6.103e-4 -0.01216 0.01311v0.007762c0.06776 "
    "0.122 0.1799 0.1455 0.2307 0.1455h{a}c0.03046 3.899e-4 0.07964 0.00449 "
    "0.1246 0.02636 0.0537 0.02695 0.07418 0.05816 0.08648 0.07769 0.001562 "
    "0.002538 0.004539 0.002563 0.01098 0.002563 0.006444-2e-8 0.009421-2.47e-"
    "5 0.01098-0.002563 0.0123-0.01953 0.03278-0.05074 0.08648-0.07769 0.04491"
    "-0.02187 0.09409-0.02597 0.1246-0.02636h{b}c0.05077 0 0.1629-0.02346 "
    "0.2307-0.1455v-0.007762c-1.78e-6 -0.0125-6.365e-4 -0.01311-0.01216-0.0131"
    "1-0.006444-3.919e-8 -0.009348 2.448e-5 -0.01091 0.002563-0.0123 0.01953-"
    "0.03278 0.05074-0.08648 0.07769-0.04491 0.02187-0.09416 0.02597-0.1246 "
    "0.02636h{c}c-0.04786 0-0.1502 0.02094-0.2185 0.1256-0.06833-0.1046-0.1706"
    "-0.1256-0.2185-0.1256h{d}c-0.03046-3.899e-4 -0.07972-0.004491-0.1246-0.02"
    "636-0.0537-0.02695-0.07418-0.05816-0.08648-0.07769-0.001562-0.002538-"
    "0.004467-0.002563-0.01091-0.002563z"
)


def offset_brace(x0, x1, xt, y_top, color=GOLD, height=0.22):
    """A downward brace from x0 to x1 (top edge at y_top) with its tip at xt; same look as Brace."""
    import svgelements as se
    from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
    w = x1 - x0
    left = 2 * (xt - x0) - 0.4527
    right = 2 * w - 0.9055 - left
    path = se.Path(_BRACE_PATH.format(a=left, b=right, c=-right, d=-left))
    br = VMobjectFromSVGPath(path_obj=path, stroke_width=0, fill_opacity=1.0)
    br.flip(RIGHT)
    br.stretch_to_fit_width(w).stretch_to_fit_height(height)
    br.move_to([x0, y_top, 0], aligned_edge=UL)
    br.set_fill(color, 1).set_stroke(width=0)
    return br


class Breakdown(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------ master shot (as ch1_s2_crew)
        you = T("you", size=36, color=YELLOW).move_to([0, 3.4, 0])
        producer = agent(3.2, 0.8, "producer", 32).move_to([0, 2.45, 0])
        planner = agent(2.8, 0.7, "series-planner", ROW).move_to([-5.1, 1.0, 0])
        writers = VGroup(*[agent(2.8, 0.7, "script-writer" if k == 0 else None, ROW)
                           .move_to([-1.7 + 0.1 * k, 1.0 + 0.1 * k, 0]) for k in (2, 1, 0)])
        voice = agent(2.8, 0.7, "vk voice", ROW, mono=True, outline=DIM, label_color=DIM).move_to([1.7, 1.0, 0])
        dir_back = VGroup(*[agent(2.8, 0.7, None, 28, outline=DIM, fill_op=0.06)
                            .move_to([5.1 + 0.08 * k, 1.0 + 0.08 * k, 0]) for k in (2, 1)])
        dir_front = agent(2.8, 0.7, "chapter-director", ROW).move_to([5.1, 1.0, 0])
        builders = [builder_box(0.75, 0.45).move_to([x, -0.5, 0]) for x in row_xs(3.0, 8, 0.75, 0.15)]
        blabel = T("scene-builder × 6–8", size=28, color=DIM).move_to([3.0, -1.05, 0])
        top_conns = VGroup(Line(you.get_bottom() + 0.05 * DOWN, producer.get_top()).set_stroke(DIM, 2).set_z_index(-1),
                           *[conn(producer, b) for b in (planner, writers[-1], voice, dir_front)])
        bconn = VGroup(*[conn(dir_front, b) for b in builders])
        wfront = writers[-1]
        w_n = T("×N", size=ROW, color=DIM).move_to([wfront.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
        d_n = T("×N", size=ROW, color=DIM).move_to([dir_front.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
        bx0 = 3.0
        master = [top_conns, bconn, you, producer, planner, writers, voice, dir_back, dir_front,
                  *builders, blabel, w_n, d_n]

        # ------------------------------------------------------------ clip 1
        with self.say("c2.split.1") as c:
            self.play(LaggedStart(*[FadeIn(m) for m in master], lag_ratio=0.04), run_time=2.0)
            c.wait_until("scene")
            gold_label = T("scene-builders $278\n94 runs (18 fix passes)", size=30, color=GOLD,
                           line_spacing=0.9).move_to([bx0, -1.2, 0])
            self.play(*[b.animate.set_stroke(GOLD).set_fill(GOLD, 0.35) for b in builders],
                      ReplacementTransform(blabel, gold_label), run_time=1.5)
            c.wait_until("old")
            ghosts = []
            for x_ in row_xs(3.0, 8, 0.75, 0.15):
                g = builder_box(0.75, 0.45).set_stroke(DIM, 3).set_fill(DIM, 0.12).move_to([x_, -2.2, 0])
                ghosts.append(g)
            old_label = T("older general-purpose\nscene agents $217", size=30, color=DIM,
                          line_spacing=0.9).move_to([bx0, -2.95, 0])
            self.play(*[FadeIn(g, shift=0.3 * DOWN) for g in ghosts], FadeIn(old_label, shift=0.3 * DOWN), run_time=1.5)
            c.wait_until("two hundred and seventeen")
            br = Brace(Line([-0.65, -0.25, 0], [-0.65, -2.45, 0]), direction=LEFT, color=GOLD, buff=0.1)
            br_t = T("scene work\n≈ 78%", size=36, color=GOLD).next_to(br, LEFT, buff=0.2)
            self.play(GrowFromCenter(br), FadeIn(br_t, shift=0.3 * LEFT), run_time=1.2)
            c.wait_until("gates")
            tags = [T("$9", size=34, color=GOLD).move_to([-5.1, 0.36, 0]),
                    T("$17", size=34, color=GOLD).move_to([-1.7, 0.36, 0]),
                    T("$40", size=34, color=GOLD).move_to([6.1, 1.78, 0])]
            self.play(*[FadeIn(t_, shift=0.3 * DOWN) for t_ in tags], run_time=1.5)
            c.wait_until("about ten percent")
            # planner box left edge (-6.5) to the director stack's right edge (6.66); tip off-centre,
            # over the empty left, so the label clears the builders and "scene work"
            gb = set_backstroke(offset_brace(-6.5, 6.66, -4.4, 0.08), width=6)
            gb_t = T("≈ 10%", size=34, color=GOLD).next_to([-4.4, gb.get_bottom()[1], 0], DOWN, buff=0.12)
            self.play(GrowFromCenter(gb), FadeIn(gb_t), run_time=1.0)
            c.wait_until("producer")
            ptxt = T("producer sessions\n$72 · ≈ 11%", size=30, color=GOLD, line_spacing=0.9)
            ptxt.next_to(producer, LEFT, buff=0.3)
            self.play(FlashAround(producer, color=GOLD, run_time=1.2), FadeIn(ptxt, shift=0.3 * RIGHT))
            c.wait_until("eleven percent")
            pnote = T("mostly one early session\n(168M cache reads)", size=28, color=DIM, line_spacing=0.9)
            pnote.next_to(producer, RIGHT, buff=0.3)
            self.play(FadeIn(pnote, shift=0.3 * LEFT), run_time=1.0)

        # ------------------------------------------------------------ clip 2
        with self.say("c2.split.2") as c:
            self.wait(1.0)
            keep = builders[0]
            others = [m for m in self.mobjects if m is not keep]
            big = box("scene-builder", 2.8, 0.7, size=28).move_to([-5.2, 3.0, 0])
            bar_y0 = -3.3
            sc = 4.4 / 132
            small = context_bar([10 * sc, 0, 0, 0, 2 * sc], -5.2, bar_y0)
            full = context_bar([10 * sc, 62 * sc, 28 * sc, 24 * sc, 8 * sc], -5.2, bar_y0)
            self.play(*[FadeOut(m) for m in others], ReplacementTransform(keep, big[0]), FadeIn(big[1]),
                      run_time=1.8)
            card = RoundedRectangle(corner_radius=0.2, width=9.6, height=3.3, stroke_color=DIM, stroke_width=3)
            card.move_to([1.7, 1.85, 0])
            title = T("a typical fresh build (median of 76)", size=36, color=YELLOW).move_to([1.7, 3.1, 0])
            l1 = T("first turn 12k (10k cached + 2k new)", size=34).move_to([1.7, 2.25, 0])
            l2 = T("25 turns · peak 132k", size=34).move_to([1.7, 1.55, 0])
            l3 = T("2.0M re-read · $3.15", size=34, color=GOLD).move_to([1.7, 0.85, 0])
            self.play(FadeIn(card), FadeIn(title, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("first")
            self.play(FadeIn(l1, shift=0.3 * DOWN), FadeIn(small), run_time=1.0)
            c.wait_until("grow")
            self.play(FadeIn(l2, shift=0.3 * DOWN), run_time=0.8)
            self.play(Transform(small, full), run_time=min(3.5, c.until("total", floor=1.0) - 0.2),
                      rate_func=linear)
            c.wait_until("total")
            self.play(FadeIn(l3, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("fix")
            fcard = RoundedRectangle(corner_radius=0.2, width=7.4, height=1.5, stroke_color=DIM, stroke_width=3)
            fcard.move_to([1.7, -0.7, 0])
            ftxt = T("fix pass (median of 18)\n7 turns · peak 30k · 0.2M · $0.25", size=30,
                     line_spacing=0.9).move_to(fcard)
            self.play(FadeIn(fcard), FadeIn(ftxt, shift=0.3 * DOWN), run_time=1.2)

        # ------------------------------------------------------------ clip 3
        with self.say("c2.split.3") as c:
            start = T("start ≈ $0.01 ≈ 0.4% of a build", size=34, color=GREEN).move_to([1.7, -2.4, 0])
            self.play(FadeIn(start, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("cache")
            kit = T("shared kit", size=28, color=GREEN).move_to([-3.6, bar_y0 + 0.35, 0])
            self.play(FlashAround(small[0], color=GREEN, run_time=1.5, time_width=1.5),
                      small[0].animate.set_fill(GREEN, 1), FadeIn(kit, shift=0.3 * RIGHT), run_time=1.5)
            c.wait_until("your second question")
            old = [big, small, kit, card, title, l1, l2, l3, fcard, ftxt, start]
            qcard = RoundedRectangle(corner_radius=0.2, width=12.8, height=2.4, stroke_color=DIM, stroke_width=3)
            qcard.move_to([0, 0.9, 0])
            qtxt = T("Do we need so many scene-builders per chapter?\nStarting an agent costs money.",
                     size=38, line_spacing=0.9).move_to(qcard)
            self.play(*[FadeOut(m) for m in old], FadeIn(qcard), FadeIn(qtxt), run_time=1.5)
            c.wait_until("do we need so many builders")
            self.play(qcard.animate.set_stroke(YELLOW), run_time=0.6)
            c.wait_until("answer")
            ans = T("Fewer would cost more.", size=52, color=YELLOW).move_to([0, -1.2, 0])
            self.play(FadeIn(ans, shift=0.3 * UP), run_time=1.0)

        # ------------------------------------------------------------ clip 4
        with self.say("c2.split.4") as c:
            cx1, cx2 = -3.4, 3.4
            ax1 = Line([cx1 - 2.6, B, 0], [cx1 + 2.6, B, 0], color=DIM, stroke_width=3)
            ax2 = Line([cx2 - 2.6, B, 0], [cx2 + 2.6, B, 0], color=DIM, stroke_width=3)
            bars1 = [stair_bar(i, cx1) for i in range(NB)]
            bars2 = [stair_bar(i, cx2) for i in range(NB)]
            s1l = T("scene 1", size=32).move_to([cx1, -2.4, 0])
            s2l = T("scene 2", size=32).move_to([cx2, -2.4, 0])
            sub1 = T("25 turns · avg ≈ 80k", size=30, color=DIM).move_to([cx1, 3.45, 0])
            sub2 = T("25 turns · avg ≈ 80k", size=30, color=DIM).move_to([cx2, 3.45, 0])
            self.wait(3.0)
            self.play(FadeOut(qcard), FadeOut(qtxt), FadeOut(ans), run_time=0.8)
            self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(s1l), FadeIn(s2l),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars1], lag_ratio=0.05),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars2], lag_ratio=0.05),
                      run_time=3.0)
            self.play(FadeIn(sub1, shift=0.3 * DOWN), FadeIn(sub2, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("one")
            shift = 0.6
            builder = box("one builder", 12.4, 0.6, size=30).move_to([0, -3.1, 0])
            self.play(*shift_all([ax1, *bars1, s1l, sub1], shift * RIGHT),
                      *shift_all([ax2, *bars2, s2l, sub2], shift * LEFT),
                      GrowFromCenter(builder), run_time=1.8)
            cx1, cx2 = cx1 + shift, cx2 - shift
            c.wait_until("plinth")
            plinth = Rectangle(width=5.0, height=130 * K).set_fill(GOLD, 0.35).set_stroke(GOLD, 3)
            plinth.move_to([cx2, B + 65 * K, 0])
            plinth.set_z_index(-1)
            ptag = T("≈ 130k left from scene 1", size=30).move_to(plinth)
            self.play(GrowFromEdge(plinth, DOWN), FadeIn(ptag), run_time=1.2)
            self.play(*shift_all(bars2, 130 * K * UP), run_time=1.8)
            c.wait_until("grows as before")
            sub2b = T("starts at ≈ 130k, grows as before", size=30, color=GOLD).move_to([cx2, 3.45, 0])
            self.play(FadeTransform(sub2, sub2b), run_time=1.2)
            c.wait_until("each")
            avg2 = DashedLine([cx2 - 2.6, B + 190 * K, 0], [cx2 + 2.6, B + 190 * K, 0],
                              color=YELLOW, stroke_width=4)
            avg2.set_z_index(5)
            avg1 = DashedLine([cx1 - 2.6, B + 80 * K, 0], [cx1 + 2.6, B + 80 * K, 0],
                              color=DIM, stroke_width=4)
            avg1.set_z_index(5)
            a2t = T("≈ 190k a turn on average", size=30, color=YELLOW).move_to([cx2, 2.75, 0])
            a1t = T("≈ 80k", size=30, color=DIM).move_to([cx1 - 3.15, B + 80 * K, 0])
            self.play(Create(avg2), FadeIn(a2t, shift=0.3 * DOWN), run_time=1.5)
            self.play(Create(avg1), FadeIn(a1t), run_time=1.2)
            c.wait_until("more")
            gold_t = T("4.0M → ≈ 6.75M", size=48, color=GOLD).move_to([cx1, 2.5, 0])
            self.play(FadeIn(gold_t, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("roughly seventy percent more")
            red_t = T("≈ 70% more re-reading", size=36, color=RED).move_to([cx1, 1.7, 0])
            self.play(FadeIn(red_t, shift=0.3 * DOWN), run_time=1.0)

        # ------------------------------------------------------------ clip 5
        with self.say("c2.split.5") as c:
            gone = [ax1, *bars1, s1l, avg1, a1t, builder, sub1]
            tbar = Rectangle(width=2.4, height=0.5).set_fill(BLUE, 0.5).set_stroke(BLUE, 3)
            tbar.move_to([-6.1 + 1.2, 0.3, 0])
            tbar_l = T("time", size=30, color=DIM).move_to([-4.9, 0.85, 0])
            self.play(*[FadeOut(m) for m in gone], FadeIn(tbar), FadeIn(tbar_l), run_time=1.2)
            tbar2 = Rectangle(width=4.8, height=0.5).set_fill(BLUE, 0.5).set_stroke(BLUE, 3)
            tbar2.move_to([-6.1 + 2.4, 0.3, 0])
            slow_t = T("≈ 2× as long", size=40, color=YELLOW).move_to([-3.7, -0.5, 0])
            self.play(Transform(tbar, tbar2), FadeIn(slow_t, shift=0.3 * DOWN), run_time=1.5)
            ta = box("scene 1", 1.9, 0.7, size=28).move_to([-4.8, -1.6, 0])
            tb = box("scene 2", 1.9, 0.7, size=28).move_to([-2.2, -1.6, 0])
            self.play(FadeIn(ta), FadeIn(tb), run_time=0.6)
            c.wait_until("mix")
            qm = T("?", size=72, color=RED).move_to([-3.5, -2.8, 0])
            self.play(ta.animate.move_to([-3.7, -1.6, 0]).rotate(0.3),
                      tb.animate.move_to([-3.3, -1.7, 0]).rotate(-0.25),
                      FadeIn(qm, shift=0.3 * DOWN),
                      FadeOut(gold_t), FadeOut(red_t), FadeOut(sub2b), FadeOut(a2t), run_time=1.2)
            c.wait_until("same")
            self.play(FlashAround(plinth, color=GOLD, run_time=1.5, time_width=1.5))
            c.wait_until("fresh")
            t1 = T("late fix notes\n→ a fresh builder", size=30, color=DIM, line_spacing=0.9).move_to([-3.6, 0.7, 0])
            t2 = T("producer stays out\nof scene work", size=30, color=DIM, line_spacing=0.9).move_to([-3.6, -0.7, 0])
            self.play(*[FadeOut(m) for m in (tbar, tbar_l, slow_t, ta, tb, qm)],
                      FadeIn(t1, shift=0.3 * RIGHT), run_time=1.0)
            c.wait_until("lean")
            self.play(FadeIn(t2, shift=0.3 * RIGHT), run_time=1.0)

        self.wait(2.7)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
