"""Chapter 2, scene 2: every turn re-reads everything. Clips c2.turns.1 – c2.turns.5.

Layout
- c2.turns.1: opens on ch1 s6's layout exactly (scenes/ch1_s6_builder.py): builder node at (-4.95, 3.0),
  3.1 x 1.15, BLUE stroke 3, AGENT_FILL, T 30 "scene-builder / ch4_s3_trace" (stem YELLOW); GOLD bar at
  x -6.1, width 0.8, bottom -3.2, fill 0.9, BG separators 3, GOLD "context" T 28 under it. On "beside a
  builder" the bar slides to x -4.2 and the box to (1.8, -0.3) (ch1's box sits right above the bar,
  and the bar is about to grow a "thinking" segment). {resend}: YELLOW sweep while the segments regroup
  into GOLD shades; labels in ch1's style (T 28 at bar x + 0.6): instructions / files read / replies /
  thinking.
- c2.turns.2: the bar copies itself into a 25-bar staircase on axes (origin (-3.3, -2.45)); area fill,
  equal-area rectangle + dashed average line, formula under the axes; DIM nrev inset upper left.
- c2.turns.3: staircase shifts left 3.0; BLUE price column top right; rows light on their words;
  the staircase recolours GREEN body / GOLD sliver / RED cap.
- c2.turns.4: GREEN tag in the body, GOLD->RED tag over the steps, the studio's dollar split bar
  under the price column, PURPLE Sonnet column beside it.
- c2.turns.5: board clears to the price columns; builder + ch1's own bar return in ch1 s6's exact
  layout with a GREEN cached look (outline + ch1's "cached" tag); clock; cached look fades; bar flashes
  GOLD, "re-written at $5 per million".

Reusable helpers (s4, s5, s6): context_bar, builder_box, staircase, stair_chart, stair_outline,
stair_area, stair_edge, stair_kinds, price_column, sonnet_column.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ── placement helpers ────────────────────────────────────────────────────────────────────────
def left_at(mob, x, y):
    mob.move_to([0, y, 0])
    return mob.shift(RIGHT * (x - mob.get_left()[0]))


def right_at(mob, x, y):
    mob.move_to([0, y, 0])
    return mob.shift(RIGHT * (x - mob.get_right()[0]))


# ── ch1 s6: the builder box and the GOLD context bar (as in scenes/ch1_s6_builder.py) ────────
AGENT_FILL = interpolate_color(ManimColor(BG), ManimColor(BLUE), 0.15)
BOX_C = np.array([-4.95, 3.0, 0.0])           # ch1 s6: builder node centre
BOX_W, BOX_H = 3.1, 1.15
BAR_X, BAR_W, BAR_BOTTOM = -6.1, 0.8, -3.2     # ch1 s6: bar centre x, width, bottom
LAB_DX = 0.6                                   # ch1 s6: labels T 28, left-aligned at BAR_X + 0.6
WORK_BAR_X = -4.2                              # clip 1 after "beside a builder"
WORK_BOX_C = np.array([1.8, -0.3, 0.0])


def builder_box(center=BOX_C):
    """ch1 s6's builder node: BLUE stroke 3, AGENT_FILL, T 30 "scene-builder / ch4_s3_trace", stem YELLOW."""
    box = RoundedRectangle(corner_radius=0.15, width=BOX_W, height=BOX_H).set_stroke(BLUE, 3)
    box.set_fill(AGENT_FILL, 1)
    label = T("scene-builder\nch4_s3_trace", 30)
    for tk in select(label, "ch4_s3_trace"):
        tk.set_color(YELLOW)
    label.move_to(box)
    g = VGroup(box, label).move_to(center)
    g.box, g.label = box, label
    return g


def context_bar(heights, x=BAR_X, bottom=BAR_BOTTOM, width=BAR_W, color=GOLD, colors=None):
    """ch1 s6's context bar: bottom-anchored segments, fill GOLD 0.9, BG separators (stroke 3).
    `colors` (one per segment) only for the regrouped bar's shades."""
    segs = VGroup()
    y = bottom
    for k, h in enumerate(heights):
        seg = Rectangle(width=width, height=h).set_fill(colors[k] if colors else color, 0.9).set_stroke(BG, 3)
        seg.move_to([x, y + h / 2, 0])
        segs.add(seg)
        y += h
    return segs


def bar_caption(x=BAR_X, bottom=BAR_BOTTOM):
    """ch1 s6's GOLD "context" (T 28) under the bar."""
    return T("context", 28, color=GOLD).move_to([x, bottom - 0.35, 0])


def bar_label(text, x_bar, y, color=FG, size=28):
    """ch1 s6's segment label: T 28, left-aligned 0.6 right of the bar's centre."""
    return left_at(T(text, size, color=color), x_bar + LAB_DX, y)


# the bar as ch1 s6 leaves it: kit 1.9, packet .45, file .45, check output .45, image .9,
# then a second pass .25 / .25 / .5
CH1_H = [1.9, 0.45, 0.45, 0.45, 0.9, 0.25, 0.25, 0.5]
ORDER = [0, 2, 4, 5, 7, 1, 3, 6]          # instructions | files read | replies
THINK_H, ADD_H = 1.0, 0.15
# regroup shades of GOLD (regroup only): instructions GOLD, files read lighter, replies darker, thinking redder
FILES_C = ManimColor(GOLD).interpolate(ManimColor(WHITE), 0.32)
REPLIES_C = ManimColor(GOLD).interpolate(ManimColor(BG), 0.32)
THINK_C = ManimColor(GOLD).interpolate(ManimColor(RED), 0.45)
KIND_C = [GOLD, REPLIES_C, FILES_C, REPLIES_C, FILES_C, FILES_C, REPLIES_C, FILES_C]
SPANS = [("instructions", 0.0, 1.9), ("files read", 1.9, 4.0), ("replies", 4.0, 5.15),
         ("thinking", 5.15, 6.15)]                   # offsets above BAR_BOTTOM


def regroup_y():
    y, out = BAR_BOTTOM, {}
    for i in ORDER:
        out[i] = y + CH1_H[i] / 2
        y += CH1_H[i]
    return out


# ── the staircase: one bar per turn ───────────────────────────────────────────────────────────
STAIR_N, STAIR_PITCH, STAIR_W = 25, 0.24, 0.2
STAIR_H0, STAIR_STEP, STAIR_SLIVER = 0.35, 0.175, 0.1     # cap = step - sliver = 0.075


def staircase(n=STAIR_N, pitch=STAIR_PITCH, bar_w=STAIR_W, h0=STAIR_H0, step=STAIR_STEP,
              sliver=STAIR_SLIVER, kinds=False, plain=GOLD, body=GREEN, write=GOLD, out=RED):
    """Bars per turn, bottom-left corner at ORIGIN; bar i is h0 + i*step tall and is
    VGroup(body, sliver, cap): body = the previous bar's height (re-read), then a thin sliver (new
    tokens written to the cache) and a thin cap (output), so sliver + cap = one step.
    kinds=False draws all three parts in `plain` (the context bar's GOLD); stair_kinds() recolours."""
    bars = VGroup()
    cap = step - sliver
    for i in range(n):
        h = h0 + i * step
        parts, y = [], 0.0
        for hh, col in ((h - step, body), (sliver, write), (cap, out)):
            r = Rectangle(width=bar_w, height=hh).set_stroke(width=0)
            r.set_fill(col if kinds else plain, 1.0)
            r.move_to([i * pitch + bar_w / 2, y + hh / 2, 0])
            parts.append(r)
            y += hh
        bar = VGroup(*parts)
        bar.body, bar.sliver, bar.cap = parts
        bars.add(bar)
    return bars


def stair_chart(origin, x_len=6.4, y_len=5.1, inset=0.15, **stair_kw):
    """Staircase on DIM axes "turns" (x) / "context" (y). VGroup(frame, bars); `.frame .bars`;
    frame = VGroup(x axis, y axis, x label, y label)."""
    o = np.array(origin, dtype=float)
    bars = staircase(**stair_kw).shift(o + RIGHT * inset)
    kw = dict(buff=0, stroke_width=3, tip_length=0.2, max_tip_length_to_length_ratio=0.1, color=DIM)
    xa = Arrow(o, o + RIGHT * x_len, **kw)
    ya = Arrow(o, o + UP * y_len, **kw)
    xl = T("turns", 30, color=DIM).next_to(xa, RIGHT, buff=0.15)
    yl = T("context", 30, color=DIM).next_to(ya, UP, buff=0.12)
    yl.shift(RIGHT * (o[0] - 0.1 - yl.get_left()[0]))
    frame = VGroup(xa, ya, xl, yl)
    chart = VGroup(frame, bars)
    chart.frame, chart.bars = frame, bars
    return chart


def _stair_corners(bars):
    pts = []
    for i, b in enumerate(bars):
        top = b.get_top()[1]
        x0 = b.get_left()[0]
        x1 = bars[i + 1].get_left()[0] if i + 1 < len(bars) else b.get_right()[0]
        pts += [[x0, top, 0], [x1, top, 0]]
    return pts


def stair_outline(bars, **style):
    """The staircase as one closed shape (gaps between bars included)."""
    base = bars.get_bottom()[1]
    pts = [[bars[0].get_left()[0], base, 0]] + _stair_corners(bars) + [[bars[-1].get_right()[0], base, 0]]
    return Polygon(*pts, **style)


def stair_area(bars):
    base = bars.get_bottom()[1]
    c = _stair_corners(bars)
    return sum((c[k + 1][0] - c[k][0]) * (c[k][1] - base) for k in range(0, len(c), 2))


def stair_edge(bars):
    """Open path along the top edge of the steps (for flashes)."""
    return VMobject().set_points_as_corners(_stair_corners(bars))


def stair_kinds(bars, t0=0.0, lag=0.05, dur=0.8, body=GREEN, write=GOLD, out=RED):
    """Recolour by kind, bar by bar left to right: one time_span'd anim per part (no wrappers)."""
    anims = []
    for i, b in enumerate(bars):
        s = t0 + i * lag
        for part, col in zip((b.body, b.sliver, b.cap), (body, write, out)):
            anims.append(time_span(part.animate.set_fill(col, 1.0), s, s + dur))
    return anims


# ── the price column (Opus, BLUE) and the Sonnet column (PURPLE) ──────────────────────────────
TAB_L, TAB_R, TAB_TOP, TAB_BOT = 0.85, 4.75, 3.5, 0.0
SON_L, SON_R = 4.9, 6.6
HEAD_Y, SUB_Y = 3.05, 2.55
ROW_Y = (1.95, 1.33, 0.71)
ROW_C = (GREEN, GOLD, RED)


def price_column():
    """BLUE frame, header "Opus" / "per million tokens", three rows. Names start DIM; prices are
    coloured (GREEN / GOLD / RED). `.frame .header .names .incl .prices .row(i)`."""
    frame = RoundedRectangle(corner_radius=0.15, width=TAB_R - TAB_L, height=TAB_TOP - TAB_BOT)
    frame.set_stroke(BLUE, 3).set_fill(BLUE, 0.06).move_to([(TAB_L + TAB_R) / 2, (TAB_TOP + TAB_BOT) / 2, 0])
    opus = left_at(T("Opus,", 36, color=BLUE), TAB_L + 0.3, HEAD_Y)
    per = left_at(T("per million tokens", 28, color=DIM), TAB_L + 0.3, SUB_Y)
    header = VGroup(opus, per)
    names = VGroup(*[left_at(T(s, 30, color=DIM), TAB_L + 0.3, y)
                     for s, y in zip(("cache read", "cache write", "output"), ROW_Y)])
    incl = left_at(T("(incl. thinking)", 28, color=DIM), TAB_L + 0.3, ROW_Y[2] - 0.4)
    prices = VGroup(*[right_at(T(s, 30, color=col), TAB_R - 0.3, y)
                      for s, col, y in zip(("$0.20", "$5", "$20"), ROW_C, ROW_Y)])
    col = VGroup(frame, header, names, incl, prices)
    col.frame, col.header, col.names, col.incl, col.prices = frame, header, names, incl, prices
    col.row = lambda i: VGroup(names[i], prices[i], incl) if i == 2 else VGroup(names[i], prices[i])
    return col


def sonnet_column():
    """PURPLE frame beside the price column: "Sonnet", $0.20 / $2.50 / $10, marks = / ½ / ½."""
    frame = RoundedRectangle(corner_radius=0.15, width=SON_R - SON_L, height=TAB_TOP - TAB_BOT)
    frame.set_stroke(PURPLE, 3).set_fill(PURPLE, 0.06).move_to([(SON_L + SON_R) / 2, (TAB_TOP + TAB_BOT) / 2, 0])
    head = T("Sonnet", 36, color=PURPLE).move_to([(SON_L + SON_R) / 2, HEAD_Y, 0])
    prices = VGroup(*[right_at(T(s, 30, color=PURPLE), SON_R - 0.52, y)
                      for s, y in zip(("$0.20", "$2.50", "$10"), ROW_Y)])
    marks = VGroup(MathTex("=", font_size=34, color=PURPLE),
                   MathTex(r"\tfrac{1}{2}", font_size=36, color=PURPLE),
                   MathTex(r"\tfrac{1}{2}", font_size=36, color=PURPLE))
    for m, y in zip(marks, ROW_Y):
        m.move_to([SON_R - 0.27, y, 0])
    col = VGroup(frame, head, prices, marks)
    col.frame, col.head, col.prices, col.marks = frame, head, prices, marks
    return col


# ── small pieces local to this scene ──────────────────────────────────────────────────────────
def plate_tag(text, color, size=30):
    t = T(text, size, color=color)
    box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.4, height=t.height + 0.32)
    box.set_stroke(color, 2.5).set_fill(BG, 0.92).move_to(t)
    return VGroup(box, t)


def nrev_inset(top_left):
    """FoCS L3 ch4's nrev staircase, small and DIM: rows of 1..5 blocks under an empty row 0."""
    u = 0.16
    rows = VGroup()
    for r in range(1, 6):
        row = VGroup(*[Square(side_length=u).set_fill(DIM, 0.6).set_stroke(BG, 1.5) for _ in range(r)])
        rows.add(row.arrange(RIGHT, buff=0))
    rows.arrange(DOWN, buff=0, aligned_edge=LEFT)
    rows.shift(np.array(top_left) + DOWN * u - rows.get_corner(UL))
    lbl = T("nrev · Lecture 3", 28, color=DIM).next_to(rows, RIGHT, buff=0.28)
    return VGroup(rows, lbl)


def clock(center, r=0.36):
    face = Circle(radius=r).set_stroke(FG, 3).move_to(center)
    hour = Line(center, center + UP * r * 0.5).set_stroke(FG, 4)
    minute = Line(center, center + UP * r * 0.8).set_stroke(YELLOW, 3)
    g = VGroup(face, hour, minute)
    g.face, g.hour, g.minute = face, hour, minute
    return g


O1 = np.array([-3.3, -2.45, 0.0])     # staircase origin, clip 2 (centred)
SHIFT2 = LEFT * 3.0                   # clips 3–4: room for the price column


class EveryTurnRereads(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c2.turns.1: the bar returns; each turn re-sends all of it ──
    def clip1(self):
        with self.say("c2.turns.1") as c:
            self.builder = builder_box()
            self.bar = context_bar(CH1_H)
            self.ctx = bar_caption()
            self.play(FadeIn(self.builder, shift=0.3 * DOWN), GrowFromEdge(self.bar, DOWN),
                      FadeIn(self.ctx, shift=0.2 * UP), run_time=min(1.4, 0.8 * c.until("beside")))
            # ch1's layout; then the builder comes beside the bar, leaving the bar room to grow
            c.wait_until("beside")
            dx = RIGHT * (WORK_BAR_X - BAR_X)
            self.play(self.builder.animate.move_to(WORK_BOX_C), self.bar.animate.shift(dx),
                      self.ctx.animate.shift(dx), run_time=min(1.4, 0.9 * c.until("nomemory")))
            c.wait_until("nomemory")
            self.mem = VGroup(T("no memory", 28, color=DIM), T("between turns", 28, color=DIM))
            self.mem.arrange(DOWN, buff=0.12).next_to(self.builder, DOWN, buff=0.3)
            self.play(FadeIn(self.mem, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("resend")
            x = WORK_BAR_X
            ys = regroup_y()
            top = BAR_BOTTOM + sum(CH1_H)
            band = Rectangle(width=BAR_W + 0.24, height=0.45).set_stroke(width=0)
            band.set_fill(YELLOW, 0).set_z_index(5)

            def sweep(m, a):
                m.move_to([x, BAR_BOTTOM + a * (top - BAR_BOTTOM), 0])
                m.set_fill(YELLOW, 0.7 * np.sin(PI * a))

            self.play(UpdateFromAlphaFunc(band, sweep, remover=True, rate_func=linear),
                      *[seg.animate.move_to([x, ys[i], 0]).set_fill(KIND_C[i], 0.9) for i, seg in enumerate(self.bar)],
                      run_time=min(1.8, 0.9 * c.until("instructions")))

            self.labels = []
            cues = ["instructions", "every file", "every reply", "own thinking"]
            nxt = cues[1:] + ["adds"]
            self.think = None
            for (text, y0, y1), cue, after in zip(SPANS, cues, nxt):
                c.wait_until(cue)
                lbl = bar_label(text, x, BAR_BOTTOM + (y0 + y1) / 2)
                anims = [FadeIn(lbl, shift=0.2 * RIGHT)]
                if text == "thinking":
                    self.think = Rectangle(width=BAR_W, height=THINK_H).set_fill(THINK_C, 0.9).set_stroke(BG, 3)
                    self.think.move_to([x, BAR_BOTTOM + y0 + THINK_H / 2, 0])
                    anims.insert(0, GrowFromEdge(self.think, DOWN))
                self.play(*anims, run_time=min(1.0, 0.85 * c.until(after)))
                self.labels.append(lbl)

            c.wait_until("adds")
            self.add_seg = Rectangle(width=BAR_W, height=ADD_H).set_fill(GOLD, 0.9).set_stroke(BG, 3)
            self.add_seg.move_to([x, BAR_BOTTOM + SPANS[-1][2] + ADD_H / 2, 0])
            self.play(FadeIn(self.add_seg, shift=0.5 * DOWN),
                      FlashAround(self.add_seg, color=YELLOW, time_width=1.5),
                      run_time=min(1.0, 0.9 * c.until()))
            settle(self, self.bar, add=[self.think, self.add_seg])

    # ── c2.turns.2: one bar per turn = a staircase; cost = area ──
    def clip2(self):
        with self.say("c2.turns.2") as c:
            chart = self.chart = stair_chart(O1)
            self.play(FadeOut(self.builder), FadeOut(self.mem), FadeOut(self.ctx), FadeIn(chart.frame),
                      run_time=0.8)

            # the bar copies itself left to right; the last copy is the bar itself
            self.bar.set_z_index(2)
            bars = chart.bars
            dt, d = 0.07, 0.9
            anims = []
            for i, b in enumerate(bars[:-1]):
                ghost = b.copy().stretch_to_fit_height(self.bar.height).stretch_to_fit_width(BAR_W)
                ghost.move_to(self.bar)
                anims.append(time_span(TransformFromCopy(ghost, b), i * dt, i * dt + d))
            n = len(bars)
            anims.append(time_span(ReplacementTransform(self.bar, bars[-1]), (n - 1) * dt, (n - 1) * dt + d))
            anims += [time_span(FadeOut(m), 0.2, 0.8) for m in self.labels]
            self.play(*anims)
            settle(self, chart)

            c.wait_until("area")
            self.poly = stair_outline(bars).set_fill(YELLOW, 0.3).set_stroke(YELLOW, 3)
            self.area_lbl = T("tokens read = area", 36, color=YELLOW).move_to([-0.9, 2.15, 0])
            self.play(FadeIn(self.poly), FadeIn(self.area_lbl, shift=0.3 * DOWN),
                      run_time=min(1.5, 0.8 * c.until("formula")))

            c.wait_until("formula")
            w = bars[-1].get_right()[0] - bars[0].get_left()[0]
            h = stair_area(bars) / w
            base = bars.get_bottom()[1]
            rect = Rectangle(width=w, height=h).set_fill(YELLOW, 0.3).set_stroke(YELLOW, 0)
            rect.move_to([bars[0].get_left()[0] + w / 2, base + h / 2, 0])
            self.avg = DashedLine([O1[0], base + h, 0], [bars[-1].get_right()[0], base + h, 0],
                                  dash_length=0.12).set_stroke(YELLOW, 3)
            self.play(ReplacementTransform(self.poly, rect), Create(self.avg),
                      run_time=min(1.8, 0.5 * c.until("nrev")))
            self.rect = rect
            self.formula = T("cost ≈ turns × average context", 36, t2c={"average context": YELLOW})
            self.formula.move_to([bars.get_center()[0], -3.0, 0])
            self.play(FadeIn(self.formula, shift=0.3 * UP), run_time=min(1.0, 0.9 * c.until("nrev")))

            c.wait_until("nrev")
            self.inset = nrev_inset([bars[0].get_left()[0] + 0.05, 1.7, 0])
            self.play(FadeIn(self.inset, shift=0.2 * DOWN), run_time=min(1.0, 0.9 * c.until()))

    # ── c2.turns.3: three prices; recolour the staircase by kind ──
    def clip3(self):
        with self.say("c2.turns.3") as c:
            pc = self.prices = price_column()
            sweep_clear(self, self.chart.animate.shift(SHIFT2), self.inset.animate.shift(SHIFT2),
                        time_span(FadeIn(pc.frame), 0.6, 1.5), time_span(FadeIn(pc.names), 0.8, 1.5),
                        time_span(FadeIn(pc.incl), 0.8, 1.5),
                        keep=[self.chart, self.inset], run_time=1.5)

            c.wait_until("opus charges")
            self.play(FadeIn(pc.header, shift=0.25 * DOWN), FadeOut(self.inset),
                      run_time=min(1.0, 0.9 * c.until("reads")))

            for i, (cue, after) in enumerate((("reads", "writes"), ("writes", "output"), ("output", "recolour"))):
                c.wait_until(cue)
                anims = [pc.names[i].animate.set_color(ROW_C[i]), FadeIn(pc.prices[i], shift=0.2 * DOWN)]
                if i == 2:
                    anims.append(pc.incl.animate.set_color(RED))
                self.play(*anims, run_time=min(1.0, 0.9 * c.until(after)))
            settle(self, pc)

            c.wait_until("recolour")
            bars = self.chart.bars
            self.play(*stair_kinds(bars), run_time=min(2.05, 0.95 * c.until("green body")))

            c.wait_until("green body")
            self.play(FlashAround(pc.row(0), color=GREEN, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("gold sliver")))
            c.wait_until("gold sliver")
            self.play(FlashAround(pc.row(1), color=GOLD, time_width=1.5),
                      VShowPassingFlash(stair_edge(bars).set_stroke(GOLD, 6), time_width=0.4),
                      run_time=min(1.4, 0.9 * c.until("red cap")))
            c.wait_until("red cap")
            self.play(FlashAround(pc.row(2), color=RED, time_width=1.5),
                      VShowPassingFlash(stair_edge(bars).set_stroke(RED, 6), time_width=0.4),
                      run_time=min(1.4, 0.9 * c.until()))

    # ── c2.turns.4: tokens vs dollars; the split; Sonnet ──
    def clip4(self):
        with self.say("c2.turns.4") as c:
            bars = self.chart.bars
            base = bars.get_bottom()[1]
            body_x = (bars[8].get_left()[0] + bars[-1].get_right()[0]) / 2
            self.body_tag = plate_tag("most of the tokens", GREEN).move_to([body_x, base + 0.75, 0])
            self.play(FadeIn(self.body_tag, shift=0.2 * DOWN), run_time=min(1.0, 0.8 * c.until("slivers")))

            c.wait_until("slivers")
            self.sliver_tag = T("most of the dollars", 32).set_color_by_gradient(GOLD, RED)
            left_at(self.sliver_tag, bars[0].get_left()[0] + 0.05, 1.8)
            self.play(FadeIn(self.sliver_tag, shift=0.3 * DOWN),
                      VShowPassingFlash(stair_edge(bars).set_stroke(YELLOW, 6), time_width=0.4),
                      run_time=min(1.5, 0.9 * c.until("split")))

            # the studio's dollars at Opus list prices: 25 / 31 / 44 %
            c.wait_until("split")
            dl, dr, dy, dh = TAB_L, SON_R, -1.0, 0.5
            title = left_at(T("the studio's dollars", 28, color=DIM), dl, -0.45)
            self.play(FadeIn(title, shift=0.2 * DOWN), run_time=min(0.9, 0.8 * c.until("percent")))
            shares = ((0.25, GREEN, "reads", "25%"), (0.31, GOLD, "writes", "31%"), (0.44, RED, "output", "44%"))
            x = dl
            self.dollars = [title]
            for (frac, col, name, pct), cue, after in zip(shares, ("percent", "cache writes", "output"),
                                                          ("cache writes", "output", "sonnet")):
                wseg = frac * (dr - dl)
                seg = Rectangle(width=wseg, height=dh).set_fill(col, 1.0).set_stroke(BG, 2.5)
                seg.move_to([x + wseg / 2, dy, 0])
                lab = VGroup(T(name, 30, color=col), T(pct, 30, color=col)).arrange(DOWN, buff=0.1)
                lab.next_to(seg, DOWN, buff=0.18)
                x += wseg
                c.wait_until(cue)
                self.play(GrowFromEdge(seg, LEFT), FadeIn(lab, shift=0.2 * UP),
                          run_time=min(1.0, 0.85 * c.until(after)))
                self.dollars += [seg, lab]

            # Sonnet: same for reads, half for the other two
            c.wait_until("sonnet")
            sc = self.sonnet = sonnet_column()
            pc = self.prices
            self.play(FadeIn(sc.frame), FadeIn(sc.head, shift=0.2 * DOWN),
                      run_time=min(0.9, 0.85 * c.until("twenty cents")))
            c.wait_until("twenty cents")
            self.play(TransformFromCopy(pc.prices[0], sc.prices[0]), FadeIn(sc.marks[0], shift=0.2 * LEFT),
                      run_time=min(1.0, 0.85 * c.until("half")))
            c.wait_until("half")
            self.play(*[FadeIn(m, shift=0.2 * LEFT) for m in sc.marks[1:]],
                      run_time=min(0.8, 0.85 * c.until("two dollars")))
            c.wait_until("two dollars")
            self.play(TransformFromCopy(pc.prices[1], sc.prices[1]),
                      run_time=min(0.9, 0.85 * c.until("ten dollars")))
            c.wait_until("ten dollars")
            self.play(TransformFromCopy(pc.prices[2], sc.prices[2]), run_time=min(0.9, 0.9 * c.until()))
            settle(self, sc)

    # ── c2.turns.5: the cache expires; a cold agent re-writes it all ──
    def clip5(self):
        with self.say("c2.turns.5", gap=2.3) as c:
            builder = builder_box()                       # ch1 s6's exact layout and bar
            bar = context_bar(CH1_H)
            ctx = bar_caption()
            cached = SurroundingRectangle(bar, color=GREEN, buff=0.08).set_stroke(GREEN, 4)
            ctag = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=0.5).set_stroke(GREEN, 2),
                          T("cached", 28, color=GREEN))   # ch1 s6's "cached" tag
            ctag[1].move_to(ctag[0])
            left_at(ctag, BAR_X + LAB_DX, -0.6)
            sweep_clear(self, time_span(FadeIn(builder, shift=0.3 * DOWN), 0.5, 1.4),
                        time_span(GrowFromEdge(bar, DOWN), 0.5, 1.4), time_span(FadeIn(ctx), 0.5, 1.4),
                        time_span(FadeIn(cached), 0.9, 1.4), time_span(GrowFromCenter(ctag), 0.9, 1.4),
                        keep=[self.prices, self.sonnet], run_time=1.4)

            c.wait_until("rule of thumb")
            ck = clock(np.array([BOX_C[0] + BOX_W / 2 + 0.6, BOX_C[1], 0.0]))
            hour = T("≈ 1 hour", 28, color=DIM).next_to(ck, RIGHT, buff=0.2)
            self.play(FadeIn(ck), FadeIn(hour, shift=0.2 * LEFT), run_time=min(0.9, 0.8 * c.until("expires")))

            c.wait_until("expires")
            self.play(Rotate(ck.minute, angle=-TAU, about_point=ck.face.get_center(), rate_func=linear),
                      run_time=min(1.6, 0.9 * c.until("an hour")))
            c.wait_until("an hour")
            self.play(FadeOut(cached), FadeOut(ctag), *[s.animate.set_fill(opacity=0.4) for s in bar],
                      run_time=min(0.9, 0.85 * c.until("cold")))

            c.wait_until("cold")
            label = bar_label("re-written at $5 per million", BAR_X, -0.6, color=GOLD, size=32)
            self.play(*[s.animate.set_fill(opacity=0.9) for s in bar],
                      FlashAround(bar, color=GOLD, time_width=1.5, stroke_width=6),
                      FadeIn(label, shift=0.2 * RIGHT), run_time=min(1.4, 0.9 * c.until("five dollars")))

            c.wait_until("five dollars")
            self.play(FlashAround(self.prices.row(1), color=GOLD, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until()))
