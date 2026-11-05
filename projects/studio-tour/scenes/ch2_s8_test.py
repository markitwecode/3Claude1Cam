"""Chapter 2, scene 8: the levers, this video as the test, and the recap. Clips c2.test.1 – c2.test.6.

Layout
- c2.test.1: board "The levers, ranked" (T 48, y 3.2); four rows, icon x -4.4, GOLD rank x -3.3, text
  T 34 from x -2.85: s5's stacked peak bar (RED thinking), s6's model dial, s5's RED lookup tiles,
  a GOLD image tile.
- c2.test.2: the board collapses into a strip at y 3.3 (icon + rank + one word); GREEN column
  "Habits that already save" on the left (check bullets).
- c2.test.3: BLUE column "Don't cut" on the right; a DIM rule at y -1.62 and three DIM caveats.
- c2.test.4: boards clear; "This video is the test"; 16 scene boxes (ch1 / ch2 rows, Mono s1–s8),
  each with a grey "?" builder icon; legend on the right (BLUE / dimmed BLUE / PURPLE); YELLOW
  outline + "you are here" on ch2 s8; GOLD meter "cost per finished scene" fed by three DIM inputs,
  pointing at an empty TEAL page STATUS.md. No values anywhere.
- c2.test.5: "Recap"; five small panels (3 + 2), one per recap sentence, each the visual that taught
  it: master shot + TEAL file hand-offs, s2's GREEN/GOLD/RED staircase, s4's plinth chart, s6's
  dials, s7's review board.
- c2.test.6: the recap rises 1.05; YELLOW card "Your next step" below. End card: hold ~8 s, fade.

Helpers below are copied from the scenes named above each block (not imported).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ── copied from ch2_s1_hook.py (crew_tree = ch1_s2_crew.py's master shot) ─────────────────────
def _agent(w, h, label=None, size=30, mono=False, outline=BLUE, fill_op=0.15, label_color=FG):
    back = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(width=0).set_fill(BG, 1)
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(outline, 3).set_fill(BLUE, fill_op)
    g = VGroup(back, rect)
    if label:
        t = (Mono if mono else T)(label, size=size, color=label_color)
        if t.width > w - 0.3:
            t.scale_to_fit_width(w - 0.3)
        g.add(t)
    return g


def _conn(a, b):
    return Line(a.get_bottom(), b.get_top()).set_stroke(DIM, 2).set_z_index(-1)


def crew_tree():
    ROW = 28
    you = T("you", size=36, color=YELLOW).move_to([0, 3.4, 0])
    producer = _agent(3.2, 0.8, "producer", 32).move_to([0, 2.45, 0])
    planner = _agent(2.8, 0.7, "series-planner", ROW).move_to([-5.1, 1.0, 0])
    writers = VGroup(*[_agent(2.8, 0.7, "script-writer" if k == 0 else None, ROW)
                       .move_to([-1.7 + 0.1 * k, 1.0 + 0.1 * k, 0]) for k in (2, 1, 0)])
    voice = _agent(2.8, 0.7, "vk voice", ROW, mono=True, outline=DIM, label_color=DIM).move_to([1.7, 1.0, 0])
    dir_back = VGroup(*[_agent(2.8, 0.7, None, 28, outline=DIM, fill_op=0.06)
                        .move_to([5.1 + 0.08 * k, 1.0 + 0.08 * k, 0]) for k in (2, 1)])
    dir_front = _agent(2.8, 0.7, "chapter-director", ROW).move_to([5.1, 1.0, 0])
    xs = [3.0 + (i - 3.5) * 0.9 for i in range(8)]
    builders = [RoundedRectangle(corner_radius=0.15, width=0.75, height=0.45).set_stroke(BLUE, 3)
                .set_fill(BLUE, 0.15).move_to([x, -0.5, 0]) for x in xs]
    brow = VGroup(*builders)
    blabel = T("scene-builder × 6–8", size=28, color=DIM).move_to([3.0, -1.05, 0])
    top_conns = VGroup(Line(you.get_bottom() + 0.05 * DOWN, producer.get_top()).set_stroke(DIM, 2).set_z_index(-1),
                       *[_conn(producer, b) for b in (planner, writers[-1], voice, dir_front)])
    bconn = VGroup(*[_conn(dir_front, b) for b in builders])
    wfront = writers[-1]
    w_n = T("×N", size=ROW, color=DIM).move_to([wfront.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
    d_n = T("×N", size=ROW, color=DIM).move_to([dir_front.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
    tree = VGroup(top_conns, bconn, you, producer, planner, writers, voice, dir_back, dir_front,
                  brow, blabel, w_n, d_n)
    agents = [producer[1], planner[1], wfront[1], dir_front[1]] + [b for b in builders]
    labels = [you, producer[2], planner[2], wfront[2], voice[2], dir_front[2], blabel, w_n, d_n]
    return tree, agents, labels


def mini_crew():
    """The master shot without its labels (as s1 shrinks it), and without the you -> producer line."""
    tree, _, labels = crew_tree()
    for lab in labels:
        for parent in tree.get_family():
            if lab in parent.submobjects:
                parent.remove(lab)
    tree[0].remove(tree[0][0])
    return tree


# ── copied from ch2_s3_history.py ─────────────────────────────────────────────────────────────
def page(w=0.8, h=1.0, color=TEAL):
    """A file: a page with a folded corner."""
    f = 0.25
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0])
    body.set_stroke(color, 3).set_fill(color, 0.12)
    fold = VMobject().set_points_as_corners([[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0],
                                             [w / 2, h / 2 - f, 0]]).set_stroke(color, 2)
    return VGroup(body, fold)


# ── copied from ch2_s2_turns.py ───────────────────────────────────────────────────────────────
def staircase(n=25, pitch=0.24, bar_w=0.2, h0=0.35, step=0.175,
              sliver=0.1, kinds=False, plain=GOLD, body=GREEN, write=GOLD, out=RED):
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


def stair_kinds(bars, t0=0.0, lag=0.05, dur=0.8, body=GREEN, write=GOLD, out=RED):
    anims = []
    for i, b in enumerate(bars):
        s = t0 + i * lag
        for part, col in zip((b.body, b.sliver, b.cap), (body, write, out)):
            anims.append(time_span(part.animate.set_fill(col, 1.0), s, s + dur))
    return anims


def mini_stair_chart():
    """s2's staircase small, all GOLD (stair_kinds recolours it), on DIM axes."""
    bars = staircase(n=25, pitch=0.13, bar_w=0.1, h0=0.12, step=0.0575, sliver=0.03).shift(0.12 * RIGHT)
    kw = dict(buff=0, stroke_width=3, tip_length=0.15, max_tip_length_to_length_ratio=0.1, color=DIM)
    axes = VGroup(Arrow(ORIGIN, 3.6 * RIGHT, **kw), Arrow(ORIGIN, 1.68 * UP, **kw))
    g = VGroup(axes, bars)
    g.axes, g.bars = axes, bars
    return g


# ── ch2_s4_breakdown.py: stair_bar geometry and the GOLD plinth, scaled down ─────────────────
SK = 0.0125     # units per 1k tokens in s4


def s4_stairs(cx, base, sx, sy, lift=0.0, cap=0.03):
    bars = VGroup()
    for i in range(25):
        h = (12 + 120 * (i / 24) ** 0.8) * SK * sy
        x = cx + (-2.5 + 0.1 + i * 0.2) * sx
        w = 0.17 * sx
        y0 = base + lift
        body = Rectangle(width=w, height=h - 2 * cap).set_fill(GREEN, 1).set_stroke(width=0)
        gold = Rectangle(width=w, height=cap).set_fill(GOLD, 1).set_stroke(width=0)
        red = Rectangle(width=w, height=cap).set_fill(RED, 1).set_stroke(width=0)
        body.move_to([x, y0 + (h - 2 * cap) / 2, 0])
        gold.move_to([x, y0 + h - 1.5 * cap, 0])
        red.move_to([x, y0 + h - 0.5 * cap, 0])
        bars.add(VGroup(body, gold, red))
    return bars


def mini_plinth_chart(sx=0.38, sy=0.5):
    """s4 clip 4 small: scene 1's staircase, and scene 2's lifted onto the GOLD plinth."""
    cx1, cx2 = -1.05, 1.05
    ax1 = Line([cx1 - 2.6 * sx, 0, 0], [cx1 + 2.6 * sx, 0, 0], color=DIM, stroke_width=3)
    ax2 = Line([cx2 - 2.6 * sx, 0, 0], [cx2 + 2.6 * sx, 0, 0], color=DIM, stroke_width=3)
    ph = 130 * SK * sy
    plinth = Rectangle(width=5.0 * sx, height=ph).set_fill(GOLD, 0.35).set_stroke(GOLD, 2)
    plinth.move_to([cx2, ph / 2, 0]).set_z_index(-1)
    bars1 = s4_stairs(cx1, 0, sx, sy)
    bars2 = s4_stairs(cx2, 0, sx, sy, lift=ph)
    g = VGroup(ax1, ax2, bars1, plinth, bars2)
    g.ax1, g.ax2, g.bars1, g.plinth, g.bars2 = ax1, ax2, bars1, plinth, bars2
    return g


# ── copied from ch2_s5_anatomy.py ─────────────────────────────────────────────────────────────
TILE = 0.45
TILE_GAP = 0.13
TILE_OPACITY = 0.85
GOLD_SHADES = ("#B8824A", GOLD, "#F7C68C", "#D39552")   # startup, images, tool output, writes


def turn_tile(color, size=TILE, opacity=TILE_OPACITY):
    t = RoundedRectangle(corner_radius=0.13 * size, width=size, height=size)
    return t.set_fill(color, opacity).set_stroke(color, 2)


def tile_row(n, color, size=TILE, gap=TILE_GAP, opacity=TILE_OPACITY):
    return VGroup(*[turn_tile(color, size, opacity) for _ in range(n)]).arrange(RIGHT, buff=gap)


def _stack(values, colors, x, bottom, height, width, total):
    outline = Rectangle(width=width, height=height).set_stroke(DIM, 2).set_fill(BG, 0)
    outline.move_to([x, bottom + height / 2, 0])
    segs = VGroup()
    y = bottom
    for v, col in zip(values, colors):
        h = height * v / total
        seg = Rectangle(width=width, height=h).set_fill(col, 1).set_stroke(BG, 3)
        seg.move_to([x, y + h / 2, 0])
        segs.add(seg)
        y += h
    return outline, segs


# ── copied from ch2_s6_dials.py ───────────────────────────────────────────────────────────────
def _polar(r, deg):
    a = deg * DEGREES
    return np.array([r * np.cos(a), r * np.sin(a), 0.0])


def build_dials(gap=3.2):
    def dial(name):
        rim = Circle(radius=0.8).set_stroke(DIM, 4).set_fill(BG, 1)
        hub = Dot(ORIGIN, radius=0.07, color=FG)
        name_t = T(name, 30, DIM).next_to(rim, DOWN, buff=0.16)
        g = VGroup(rim, hub, name_t)
        g.rim, g.hub, g.name = rim, hub, name_t
        return g

    m = dial("model")
    opus_arc = Arc(radius=0.62, start_angle=96 * DEGREES, angle=78 * DEGREES).set_stroke(BLUE, 8)
    son_arc = Arc(radius=0.62, start_angle=6 * DEGREES, angle=78 * DEGREES).set_stroke(PURPLE, 8)
    opus_t = T("Opus", 28, BLUE).move_to([-0.72, 1.08, 0])
    son_t = T("Sonnet", 28, PURPLE).move_to([0.86, 1.08, 0])
    m_needle = Line(ORIGIN, _polar(0.55, 135)).set_stroke(FG, 5)
    m.add(opus_arc, son_arc, opus_t, son_t, m_needle)
    m.hub.set_z_index(1)
    m.needle, m.opus, m.sonnet = m_needle, opus_t, son_t

    e = dial("effort")
    e_arc = Arc(radius=0.62, start_angle=0, angle=PI).set_stroke(DIM, 6)
    ticks = VGroup(*[Line(_polar(0.5, d), _polar(0.68, d)).set_stroke(FG, 3) for d in (0, 45, 90, 135, 180)])
    e_needle = Line(ORIGIN, _polar(0.55, 90)).set_stroke(FG, 5)
    e.add(e_arc, ticks, e_needle)
    e.hub.set_z_index(1)
    e.needle = e_needle

    m.shift(gap / 2 * LEFT)
    e.shift(gap / 2 * RIGHT)
    g = VGroup(m, e)
    g.model, g.effort = m, e
    return g


# ── copied from ch2_s7_second.py ──────────────────────────────────────────────────────────────
STATE_COLOR = {"neutral": FG, "green": GREEN, "red": RED, "dim": DIM}


def board_title():
    t = T("Gemini's review", 48).move_to(UP * 3.3)
    s = T("each claim checked against the code and transcripts", 28, DIM).move_to(UP * 2.65)
    return t, s


def mini_card(state, width=1.05, height=0.36):
    """review_card()'s box (stroke 3, fill 0.12 of its colour), without the label."""
    col = STATE_COLOR[state]
    return RoundedRectangle(corner_radius=0.1, width=width, height=height).set_stroke(col, 3).set_fill(col, 0.12)


# ── this scene ────────────────────────────────────────────────────────────────────────────────
LOWER_BLUE = ManimColor(BLUE).interpolate(ManimColor(BG), 0.45)


def top_left(mob, x, top):
    mob.move_to([0, 0, 0])
    return mob.shift([x - mob.get_left()[0], top - mob.get_top()[1], 0])


def builder_icon(color, op=0.2, q=False):
    r = RoundedRectangle(corner_radius=0.1, width=0.56, height=0.38).set_stroke(color, 2).set_fill(color, op)
    if not q:
        return VGroup(r)
    return VGroup(r, T("?", 28, color).move_to(r))


def scene_box(name):
    rect = RoundedRectangle(corner_radius=0.1, width=0.8, height=1.0).set_stroke(BLUE, 2).set_fill(BLUE, 0.06)
    lab = Mono(name, 28).move_to(rect.get_center() + 0.25 * UP)
    icon = builder_icon(DIM, 0.15, q=True).move_to(rect.get_center() + 0.17 * DOWN)
    g = VGroup(rect, lab, icon)
    g.rect, g.lab, g.icon = rect, lab, icon
    return g


class TheTest(NarratedScene):
    def construct(self):
        self.levers()
        self.habits()
        self.keep()
        self.test()
        self.recap()
        self.next_step()
        # end card: the finished recap + the next step; the music carries it
        self.wait(7.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c2.test.1: the levers, ranked ──────────────────────────────────────────────────────────
    def levers(self):
        title = T("The levers, ranked", 48).move_to([0, 3.2, 0])
        out, segs = _stack((12, 15, 11, 8, 86), (*GOLD_SHADES, RED), 0, -0.5, 1.0, 0.42, 132)
        think = VGroup(out, segs)
        dial = build_dials().model
        dial.remove(dial.name, dial.opus, dial.sonnet)
        dial.scale(0.55)
        tiles = VGroup(tile_row(4, RED, size=0.24, gap=0.07),
                       tile_row(4, RED, size=0.24, gap=0.07)).arrange(DOWN, buff=0.07)
        image = turn_tile(GOLD, size=0.6)
        icons = [think, dial, tiles, image]
        texts = [T("thinking → effort level", 34, t2c={"thinking": RED}),
                 T("the model", 34),
                 VGroup(T("turns → fewer lookups,", 34, t2c={"lookups": RED}),
                        T("no renders while must-fix flags remain", 34)).arrange(DOWN, aligned_edge=LEFT, buff=0.16),
                 T("context → images only ≈ 10%", 34, t2c={"images": GOLD, "10%": GOLD})]
        nums = [T(str(i + 1), 44, GOLD) for i in range(4)]
        for ic, n, t, y in zip(icons, nums, texts, (1.9, 0.6, -0.65, -2.3)):
            first = t[0] if isinstance(t, VGroup) else t
            t.move_to([0, 0, 0])
            t.shift([-2.85 - t.get_left()[0], y - first.get_y(), 0])
            n.move_to([-3.3, y, 0])
            ic.move_to([-4.4, t.get_y(), 0])
        self.title, self.icons, self.nums, self.texts = title, icons, nums, texts

        with self.say("c2.test.1", gap=0.8) as c:
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.0)
            for i, (cue, nxt) in enumerate((("thinking", "model"), ("model", "turns"),
                                            ("turns", "context"), ("context", None))):
                c.wait_until(cue)
                self.play(FadeIn(icons[i], scale=0.8), FadeIn(nums[i], shift=0.2 * RIGHT),
                          FadeIn(texts[i], shift=0.2 * RIGHT), run_time=min(1.2, 0.6 * c.until(nxt)))

    # ── c2.test.2: habits that already save ────────────────────────────────────────────────────
    def habits(self):
        short = ("thinking", "model", "turns", "context")
        heights = (0.6, 0.5, 0.45, 0.42)
        items, compact = [], []
        for i in range(4):
            ic_t = self.icons[i].copy()
            ic_t.scale(heights[i] / ic_t.height)
            n_t = T(str(i + 1), 32, GOLD)
            l_t = T(short[i], 28)
            items.append(VGroup(ic_t, n_t, l_t).arrange(RIGHT, buff=0.15))
        VGroup(*items).arrange(RIGHT, buff=0.75).move_to([0, 3.3, 0])
        for i, it in enumerate(items):
            compact += [time_span(Transform(self.icons[i], it[0]), 0.0, 1.3),
                        time_span(Transform(self.nums[i], it[1]), 0.0, 1.3),
                        time_span(FadeOut(self.texts[i]), 0.1 + 0.2 * i, 0.8 + 0.2 * i),
                        time_span(FadeIn(it[2]), 0.4, 1.3)]
        compact.append(time_span(FadeOut(self.title), 0.0, 1.0))

        head = T("Habits that already save", 36, GREEN).move_to([0, 2.35, 0])
        head.shift((-6.45 - head.get_left()[0]) * RIGHT)
        h1 = T("fix notes within the hour,\nor a fresh builder ($0.25),\nnot a cold 300–400k agent", 28,
               t2c={"$0.25": GOLD, "300–400k": GOLD})
        h2 = T("a lean producer\n(once 38% of a lecture)", 28, t2c={"38%": GOLD})
        h3 = T("one director at a time\n(two at once ≈ half the wall time)", 28)
        top = 1.95
        bullets = []
        for h in (h1, h2, h3):
            top_left(h, -5.9, top)
            top = h.get_bottom()[1] - 0.32
            bullets.append(check_mark(GREEN).scale(0.6).move_to([-6.2, h.get_top()[1] - 0.14, 0]))

        with self.say("c2.test.2") as c:
            self.play(*compact, time_span(FadeIn(head, shift=0.3 * DOWN), 0.5, 1.5))
            for h, b, cue, nxt in zip((h1, h2, h3), bullets, ("notes", "lean", "onedir"), ("lean", "onedir", None)):
                c.wait_until(cue)
                self.play(Create(b), FadeIn(h, shift=0.2 * RIGHT), run_time=min(1.2, 0.5 * c.until(nxt)))

    # ── c2.test.3: don't cut; three caveats ───────────────────────────────────────────────────
    def keep(self):
        head = T("Don't cut", 36, BLUE).move_to([0, 2.35, 0])
        head.shift((0.6 - head.get_left()[0]) * RIGHT)
        k1 = top_left(T("planner, writers, directors", 28), 1.1, 1.95)
        k1b = T("≈ 10% · the gates", 28, t2c={"≈ 10%": GOLD}).next_to(k1, DOWN, buff=0.16, aligned_edge=LEFT)
        k2 = top_left(T("agent startup ≈ $0.01", 28, t2c={"$0.01": GOLD}), 1.1, k1b.get_bottom()[1] - 0.32)
        dots = [Dot([0.85, k.get_top()[1] - 0.13, 0], radius=0.07, color=BLUE) for k in (k1, k2)]

        rule = Line([-6.45, -1.62, 0], [6.45, -1.62, 0]).set_stroke(DIM, 2)
        cys = (-2.05, -2.55, -3.05)
        cnums = [T(str(i + 1), 28, DIM).move_to([-6.25, y, 0]) for i, y in enumerate(cys)]
        cav = [T(s, 28, DIM) for s in ("dollars: Opus list prices, a relative weight",
                                       "counts: transcripts on disk (nearly all)",
                                       "how the plan weighs Sonnet vs Opus: not published")]
        for t, y in zip(cav, cys):
            t.move_to([0, y, 0]).shift((-5.9 - t.get_left()[0]) * RIGHT)

        with self.say("c2.test.3", gap=1.4) as c:
            self.play(FadeIn(head, shift=0.3 * DOWN), run_time=0.9)
            self.play(GrowFromCenter(dots[0]), FadeIn(k1, shift=0.2 * RIGHT), run_time=1.0)
            c.wait_until("about ten percent")
            self.play(FadeIn(k1b, shift=0.2 * RIGHT), run_time=1.0)
            c.wait_until("startup")
            self.play(GrowFromCenter(dots[1]), FadeIn(k2, shift=0.2 * RIGHT), run_time=1.0)
            c.wait_until("caveats")
            self.play(Create(rule), LaggedStart(*[FadeIn(n, shift=0.2 * DOWN) for n in cnums], lag_ratio=0.3),
                      run_time=min(1.4, 0.8 * c.until("rel")))
            for t, cue, nxt in zip(cav, ("rel", "disk", "plan"), ("disk", "plan", None)):
                c.wait_until(cue)
                self.play(FadeIn(t, shift=0.2 * RIGHT), run_time=min(1.0, 0.5 * c.until(nxt)))
        self.cav_mobs = [rule, *cnums, *cav]

    # ── c2.test.4: this video is the test ─────────────────────────────────────────────────────
    def test(self):
        title = T("This video is the test", 44, t2c={"the test": YELLOW}).move_to([0, 3.3, 0])
        boxes, row_labs = [], []
        for r, (ch, y) in enumerate((("ch1", 2.0), ("ch2", 0.8))):
            lab = Mono(ch, 30).move_to([0, y, 0])
            lab.shift((-5.8 - lab.get_right()[0]) * RIGHT)
            row_labs.append(lab)
            for j in range(8):
                boxes.append(scene_box(f"s{j + 1}").move_to([-5.2 + 0.93 * j, y, 0]))
        here_box = boxes[15]
        here = T("you are here", 30, YELLOW).next_to(here_box, DOWN, buff=0.2)

        def entry(color, text, y):
            ic = builder_icon(color, 0.35).move_to([2.35, y, 0])
            t = T(text, 30, color).move_to([0, y, 0])
            t.shift((2.8 - t.get_left()[0]) * RIGHT)
            return VGroup(ic, t)

        legend = [entry(BLUE, "Opus as now", 2.3), entry(LOWER_BLUE, "Opus at lower effort", 1.7),
                  entry(PURPLE, "Sonnet", 1.1)]
        note = T("rotated across scenes", 28, DIM).move_to([0, 0.5, 0])
        note.shift((2.07 - note.get_left()[0]) * RIGHT)

        my = -2.2
        meter = RoundedRectangle(corner_radius=0.2, width=5.0, height=1.1).set_stroke(GOLD, 4).set_fill(GOLD, 0.1)
        meter.move_to([-0.25, my, 0])
        m_lab = T("cost per finished scene", 30, GOLD).move_to(meter)
        inputs, arrows = [], []
        for k, (s, y) in enumerate((("fix passes", -1.55), ("check runs", -2.2), ("review notes", -2.85))):
            t = T(s, 28, DIM).move_to([0, y, 0])
            t.shift((-3.5 - t.get_right()[0]) * RIGHT)
            inputs.append(t)
            arrows.append(Arrow([-3.4, y, 0], [meter.get_left()[0], my + (y - my) * 0.3, 0], buff=0.05,
                                stroke_width=3, tip_length=0.16, color=DIM))
        pg = page().scale(0.75).move_to([3.2, my, 0])
        out_arrow = Arrow([meter.get_right()[0], my, 0], [pg.get_left()[0], my, 0], buff=0.1,
                          stroke_width=3, tip_length=0.18, color=GOLD)
        st_lab = Mono("STATUS.md", 30, TEAL).move_to([0, -1.95, 0])
        st_lab.shift((3.75 - st_lab.get_left()[0]) * RIGHT)
        go_lab = T("results go here", 28, DIM).move_to([0, -2.5, 0])
        go_lab.shift((3.75 - go_lab.get_left()[0]) * RIGHT)

        with self.say("c2.test.4", gap=1.5) as c:
            c.wait_until("the test")
            # the boards clear; the caveats (just said) go as the scenes arrive
            sweep_clear(self, time_span(FadeIn(title, shift=0.3 * DOWN), 0.6, 1.4), keep=self.cav_mobs, run_time=1.4)
            c.wait_until("scenes")
            self.play(*[time_span(FadeOut(m), 0, 0.8) for m in self.cav_mobs],
                      *[FadeIn(l, shift=0.2 * RIGHT) for l in row_labs],
                      LaggedStart(*[FadeIn(b, shift=0.15 * DOWN) for b in boxes], lag_ratio=0.08),
                      run_time=min(2.0, 0.8 * c.until("rotated across scenes")))
            c.wait_until("rotated across scenes")
            self.play(FadeIn(note, shift=0.2 * DOWN), run_time=min(0.9, 0.7 * c.until("asnow")))
            for e, cue, nxt in zip(legend, ("asnow", "lower", "sonnet"), ("lower", "sonnet", "watching")):
                c.wait_until(cue)
                self.play(FadeIn(e, shift=0.2 * RIGHT), run_time=min(0.9, 0.7 * c.until(nxt)))
            c.wait_until("watching")
            self.play(here_box.rect.animate.set_stroke(YELLOW, 4),
                      FlashAround(here_box, color=YELLOW, time_width=1.5),
                      FadeIn(here, shift=0.3 * UP), run_time=1.5)
            c.wait_until("measure")
            self.play(FadeIn(meter), FadeIn(m_lab, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("fix passes")
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * RIGHT) for t in inputs], lag_ratio=0.45),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.45),
                      run_time=min(2.4, 0.9 * c.until("status")))
            c.wait_until("status")
            self.play(time_span(GrowArrow(out_arrow), 0, 0.7), time_span(FadeIn(pg, shift=0.2 * RIGHT), 0.3, 1.0),
                      time_span(FadeIn(st_lab, shift=0.2 * DOWN), 0.3, 1.0),
                      time_span(FadeIn(go_lab, shift=0.2 * DOWN), 0.4, 1.1))
        self.status_mobs = [inputs, arrows, out_arrow, pg, st_lab, go_lab]

    # ── c2.test.5: recap, one small panel per sentence ────────────────────────────────────────
    def recap(self):
        title = T("Recap", 48).move_to([0, 3.3, 0])
        Y1, Y2, C1, C2 = 1.5, -0.9, 0.35, -2.1

        # r1: the master shot + TEAL file hand-offs
        tree = mini_crew().scale(0.3)
        pgs = VGroup(*[page().scale(0.3) for _ in range(4)]).arrange(RIGHT, buff=0.6)
        hand = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, stroke_width=3, tip_length=0.12,
                              color=DIM) for a, b in zip(pgs[:-1], pgs[1:])])
        conveyor = VGroup(pgs, hand)
        v1 = VGroup(tree, conveyor).arrange(DOWN, buff=0.25).move_to([-4.45, Y1, 0])
        cap1 = T("crew + file hand-offs", 30, t2c={"file hand-offs": TEAL}).move_to([-4.45, C1, 0])
        # r2: s2's staircase, recoloured on "dollars"
        v2 = mini_stair_chart().move_to([0, Y1, 0])
        cap2 = T("cost ≈ turns × context", 30).move_to([0, C1, 0])
        # r3: s4's plinth chart
        v3 = mini_plinth_chart().move_to([4.45, Y1, 0])
        cap3 = T("scene work ≈ 78%", 30, GOLD).move_to([4.45, C1, 0])
        # r4: s6's dials
        v4 = build_dials().scale(0.6)
        for d in (v4.model, v4.effort):                       # keep its labels at 28 on screen
            d.name.scale(28 / (30 * 0.6)).next_to(d.rim, DOWN, buff=0.1)
        mc = v4.model.rim.get_center()
        v4.model.opus.scale(1 / 0.6).move_to(mc + np.array([-0.62, 0.62, 0]))
        v4.model.sonnet.scale(1 / 0.6).move_to(mc + np.array([0.78, 0.62, 0]))
        v4.move_to([-2.8, Y2, 0])
        cap4 = T("measure both dials", 30).move_to([-2.8, C2, 0])
        # r5: s7's review board
        btitle = board_title()[0].scale(0.6)
        cards = VGroup(VGroup(*[mini_card("green") for _ in range(3)]).arrange(RIGHT, buff=0.15),
                       VGroup(*[mini_card("red") for _ in range(3)]).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.15)
        v5 = VGroup(btitle, cards).arrange(DOWN, buff=0.25).move_to([2.8, Y2, 0])
        cap5 = T("second opinion → 3 changes", 30, t2c={"3 changes": GREEN}).move_to([2.8, C2, 0])

        panels = [VGroup(v1, cap1), VGroup(v2, cap2), VGroup(v3, cap3), VGroup(v4, cap4), VGroup(v5, cap5)]
        self.recap_title, self.panels = title, panels

        def caption(cap, t0):
            return time_span(FadeIn(cap, shift=0.2 * DOWN), t0, t0 + 0.8)

        with self.say("c2.test.5") as c:
            # clear oldest first; the meter and STATUS.md go last
            last = [m for g in self.status_mobs for m in (g if isinstance(g, list) else [g])]
            first = [m for m in self.mobjects if m not in last]
            c.wait_until("both parts")
            self.play(LaggedStart(*[FadeOut(m) for m in first], lag_ratio=0.04),
                      time_span(FadeIn(title, shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)

            c.wait_until("r1")
            self.play(*[FadeOut(m) for m in last], FadeIn(tree, shift=0.2 * DOWN), run_time=1.2)
            seq = [FadeIn(pgs[0], shift=0.15 * RIGHT)]
            for a, p in zip(hand, pgs[1:]):
                seq += [GrowArrow(a), FadeIn(p, shift=0.15 * RIGHT)]
            self.play(time_span(LaggedStart(*seq, lag_ratio=0.35), 0, 1.6), caption(cap1, 0.8))
            settle(self, panels[0])

            c.wait_until("r2")
            self.play(time_span(FadeIn(v2.axes), 0, 0.5),
                      time_span(LaggedStart(*[GrowFromEdge(b, DOWN) for b in v2.bars], lag_ratio=0.06), 0.1, 1.6),
                      caption(cap2, 0.9))
            c.wait_until("dollars")
            self.play(*stair_kinds(v2.bars))
            settle(self, panels[1])

            c.wait_until("r3")
            self.play(time_span(FadeIn(v3.ax1), 0, 0.4), time_span(FadeIn(v3.ax2), 0, 0.4),
                      time_span(LaggedStart(*[GrowFromEdge(b, DOWN) for b in v3.bars1], lag_ratio=0.04), 0.1, 0.9),
                      time_span(GrowFromEdge(v3.plinth, DOWN), 0.3, 0.9),
                      time_span(LaggedStart(*[GrowFromEdge(b, DOWN) for b in v3.bars2], lag_ratio=0.04), 0.7, 1.5),
                      caption(cap3, 0.8))
            c.wait_until("fewer builders")
            self.play(FlashAround(v3.plinth, color=GOLD, time_width=1.5), run_time=min(1.2, c.until("r4")))
            settle(self, panels[2])

            c.wait_until("r4")
            self.play(time_span(FadeIn(v4.model, shift=0.2 * UP), 0, 0.9),
                      time_span(FadeIn(v4.effort, shift=0.2 * UP), 0.3, 1.2), caption(cap4, 0.8))
            settle(self, panels[3])

            c.wait_until("r5")
            self.play(time_span(FadeIn(btitle, shift=0.2 * DOWN), 0, 0.8),
                      time_span(LaggedStart(*[FadeIn(k, shift=0.15 * UP) for k in (*cards[0], *cards[1])],
                                            lag_ratio=0.15), 0.2, 1.3),
                      caption(cap5, 0.9))
            settle(self, panels[4])

    # ── c2.test.6: your next step ─────────────────────────────────────────────────────────────
    def next_step(self):
        head = T("Your next step", 34, YELLOW)
        l1 = T("When the results are in STATUS.md, choose the default model", 30, t2c={"STATUS.md": TEAL})
        l2 = T("and effort for the builders, and for the fix passes", 30)
        body = VGroup(head, l1, l2)
        top_left(head, -6.0, 0)
        top_left(l1, -6.0, head.get_bottom()[1] - 0.14)
        top_left(l2, -6.0, l1.get_bottom()[1] - 0.1)
        card = RoundedRectangle(corner_radius=0.2, width=12.6, height=body.height + 0.46).set_stroke(YELLOW, 3)
        card.set_fill(YELLOW, 0.06).move_to([0, -3.3 + card.height / 2, 0])   # 0.7 clear below
        body.shift(card.get_center() - body.get_center())

        with self.say("c2.test.6") as c:
            self.play(FadeOut(self.recap_title), *[p.animate.shift(1.1 * UP) for p in self.panels], run_time=1.2)
            c.wait_until("your next step")
            self.play(FadeIn(card), FadeIn(head, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("Once the results")
            self.play(LaggedStart(FadeIn(l1, shift=0.2 * RIGHT), FadeIn(l2, shift=0.2 * RIGHT), lag_ratio=0.5),
                      run_time=min(1.8, 0.8 * c.until()))
