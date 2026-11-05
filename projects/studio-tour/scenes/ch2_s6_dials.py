"""Chapter 2, scene 6: Two dials, the model and the effort. Clips c2.dials.1 – c2.dials.5.

Self-contained helpers (no earlier scenes existed to copy from):
  build_dials()   the two dials ("model": BLUE Opus / PURPLE Sonnet, "effort": needle at default).
                  Reused small in s8: copy this function verbatim.
  builder_box()   BLUE "scene builder" box carrying the dials.
  master_shot()   mini crew shot: producer / planner, writer, director / 4 builders + fix pass.
"""
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
def _polar(r, deg):
    a = deg * DEGREES
    return np.array([r * np.cos(a), r * np.sin(a), 0.0])


def build_dials(gap=3.2):
    """VGroup(model_dial, effort_dial), centred on ORIGIN, dial centres `gap` apart.

    Each dial: .rim (Circle r 0.8, DIM stroke 4, BG fill) .hub .needle (FG, stroke 5) .name (T 30 DIM).
    model: BLUE arc + "Opus" (T 28) upper-left, PURPLE arc + "Sonnet" upper-right, needle on Opus (135°).
    effort: DIM arc over the top with 5 ticks, needle at the default (90°).
    Light a dial with dial.rim.animate.set_stroke(YELLOW, 6).
    """
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


def builder_box():
    rect = RoundedRectangle(corner_radius=0.2, width=6.4, height=3.6).set_stroke(BLUE, 4).set_fill(BLUE, 0.08)
    title = T("scene builder", 34, BLUE).next_to(rect.get_top(), DOWN, buff=0.25)
    dials = build_dials().move_to(rect.get_center() + 0.3 * DOWN)
    g = VGroup(rect, title, dials)
    g.rect, g.title, g.dials = rect, title, dials
    return g


def agent_box(name, w=2.6, h=0.8, size=30):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.12)
    t = T(name, size).move_to(r)
    g = VGroup(r, t)
    g.box, g.label = r, t
    return g


def master_shot():
    prod = agent_box("producer").move_to(2.0 * UP)
    row1 = VGroup(*[agent_box(n) for n in ("planner", "writer", "director")]).arrange(RIGHT, buff=0.6)
    row1.move_to(0.5 * UP)
    builders = VGroup(*[agent_box(n, w=1.5, h=0.7, size=28) for n in ("build", "build", "build", "build", "fix")])
    builders.arrange(RIGHT, buff=0.3).move_to(1.6 * DOWN)
    tag = T("builders", 28, DIM).next_to(builders, LEFT, buff=0.3)
    g = VGroup(prod, row1, builders, tag)
    g.prod, g.row1, g.builders, g.tag = prod, row1, builders, tag
    return g


def opus_lock():
    body = Rectangle(width=0.24, height=0.19).set_stroke(BLUE, 2).set_fill(BLUE, 1)
    shackle = Arc(radius=0.085, start_angle=0, angle=PI).set_stroke(BLUE, 3)
    shackle.next_to(body, UP, buff=0)
    lock = VGroup(body, shackle)
    return VGroup(lock, T("Opus", 28, BLUE)).arrange(RIGHT, buff=0.1)


def small_card(text, size=30):
    """Card 1 of ch2_s1_hook's question_cards(), small: DIM rounded box (corner 0.2, stroke 3,
    BG fill), serif FG text left-aligned 0.5 in. Text kept at 30 rather than scaling the 34."""
    t = T(text, size=size, line_spacing=0.9)
    r = RoundedRectangle(corner_radius=0.2, width=t.width + 1.0, height=t.height + 0.5, stroke_color=DIM,
                         stroke_width=3, fill_color=BG, fill_opacity=1)
    t.move_to(r).align_to(r, LEFT).shift(0.5 * RIGHT)
    g = VGroup(r, t)
    g.box, g.text = r, t
    return g


def card_lit(card):
    """As ch2_s1_hook: lit = YELLOW outline + YELLOW text."""
    return [card.box.animate.set_stroke(YELLOW), card.text.animate.set_color(YELLOW)]


# copied from ch2_s5_anatomy.py (peak_bar and its _stack)
GOLD_SHADES = ("#B8824A", GOLD, "#F7C68C", "#D39552")   # startup, images, tool output, writes


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


def peak_bar(x=-2.75, bottom=-3.5, height=5.1, width=1.2, label_size=28):
    """ch2_s5_anatomy's peak context bar (132k): GOLD_SHADES segments, RED thinking on top."""
    outline, segs = _stack((12, 15, 11, 8, 86), (*GOLD_SHADES, RED), x, bottom, height, width, 132)
    header = T("peak ≈ 132k", 34, t2c={"132k": GOLD}).next_to(outline, UP, buff=0.32)
    texts = (("startup 12k", "12k"), ("images 15k (5 × ∼3k)", "15k"),
             ("tool output 11k", "11k"), ("writes and patches 8k", "8k"))
    lx = outline.get_right()[0] + 0.3
    labels, ticks = VGroup(), VGroup()
    prev = -10.0
    for (txt, num), seg in zip(texts, segs[:4]):
        lab = T(txt, label_size, t2c={num: GOLD})
        y = max(seg.get_y(), prev + 0.47)
        prev = y
        lab.move_to([lx, y, 0], aligned_edge=LEFT)
        ticks.add(Line([outline.get_right()[0] + 0.05, seg.get_y(), 0], [lx - 0.07, y, 0])
                  .set_stroke(DIM, 2))
        labels.add(lab)
    think = T("thinking ≈ 80k", 32, color=RED)
    think.move_to([lx, segs[4].get_y() + 0.42, 0], aligned_edge=LEFT)
    labels.add(think)
    bar = VGroup(outline, segs, ticks, labels, header)
    bar.outline, bar.segs, bar.think, bar.labels, bar.ticks, bar.header = (
        outline, segs, segs[4], labels, ticks, header)
    return bar


K = 0.017          # units per dollar in the cost bars
BAR_W = 1.6


def cost_bar(parts, x, base):
    segs = VGroup()
    y = base
    for v, col in parts:
        h = v * K
        r = Rectangle(width=BAR_W, height=h).set_stroke(col, 2).set_fill(col, 0.85)
        r.move_to([x, y + h / 2, 0])
        y += h
        segs.add(r)
    return segs


def seg_label(text, seg):
    return T(text, 28, BG, weight=BOLD).move_to(seg)


# ---------------------------------------------------------------- scene
class Dials(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # c2.dials.1 ------------------------------------------------------
    def clip1(self):
        with self.say("c2.dials.1") as c:
            box = builder_box().move_to(0.8 * DOWN)
            fm = Mono("model: opus", 40, t2c={"opus": BLUE}).next_to(box, UP, buff=0.5)
            self.play(FadeIn(box.rect), FadeIn(box.title, shift=0.2 * DOWN),
                      LaggedStart(*[FadeIn(d, scale=0.9) for d in box.dials], lag_ratio=0.3),
                      run_time=1.8)
            self.play(FadeIn(fm, shift=0.3 * DOWN), run_time=0.9)
            c.wait_until("model")

            card = small_card("Can any step run on Sonnet instead of Opus?").move_to(3.0 * UP)
            md = box.dials.model
            self.play(md.rim.animate.set_stroke(YELLOW, 6), md.name.animate.set_color(YELLOW),
                      FlashAround(md, run_time=1.2, color=YELLOW),
                      time_span(FadeIn(card, shift=0.3 * DOWN), 0.4, 1.4), run_time=1.4)
            self.play(*card_lit(card), run_time=0.8)
            c.wait_until("only")

            ms = master_shot()
            gold = VGroup(T("≈ 80% of what today's four agent types spend", 32, GOLD),
                          T("($278 of ≈ $344)", 30, GOLD)).arrange(DOWN, buff=0.15).move_to(2.85 * DOWN)
            sweep_clear(self, time_span(FadeIn(ms, lag_ratio=0.1), 0.5, 1.6), keep=[card], run_time=1.6)
            self.play(*[b.box.animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.18) for b in ms.builders],
                      ms.tag.animate.set_color(YELLOW),
                      time_span(FadeIn(gold, shift=0.2 * UP), 0.5, 1.5), run_time=1.5)
            c.wait_until("gates")

            tags = VGroup()
            for b, role in zip(ms.row1, ("plan", "teaching", "review")):
                tg = VGroup(T("judgment gate", 28, GREEN), T(role, 28, GREEN)).arrange(DOWN, buff=0.06)
                tg.next_to(b, DOWN, buff=0.12)
                tags.add(tg)
            locks = VGroup(*[opus_lock().next_to(b, UP, buff=0.08, aligned_edge=RIGHT) for b in ms.row1])
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * DOWN) for t in tags], lag_ratio=0.25),
                      *[b.box.animate.set_stroke(GREEN, 4) for b in ms.row1],
                      time_span(LaggedStart(*[FadeIn(lk, shift=0.2 * DOWN) for lk in locks], lag_ratio=0.2), 0.5, 1.6),
                      run_time=1.6)
            c.wait_until()

    # c2.dials.2 ------------------------------------------------------
    def clip2(self):
        with self.say("c2.dials.2") as c:
            base = -2.3
            ox, sx = -1.6, 1.6
            opus = cost_bar([(40.8, GREEN), (85.5, GOLD), (152, RED)], ox, base)
            son = cost_bar([(40.8, GREEN), (85.5, GOLD), (152, RED)], sx, base)
            o_lbl = VGroup(*[seg_label(s, g) for s, g in zip(("$40.8", "$85.5", "$152"), opus)])
            legend = VGroup(*[T(s, 30, col).next_to(g, LEFT, buff=0.35).set_y(g.get_y())
                              for s, col, g in zip(("re-reading", "writes", "output"), (GREEN, GOLD, RED), opus)])
            o_name = T("Opus", 36, BLUE).next_to(opus, DOWN, buff=0.25)
            s_name = T("Sonnet", 36, PURPLE).next_to(son, DOWN, buff=0.25).set_y(o_name.get_y())
            o_tot = T("$278", 36, BLUE).next_to(opus, UP, buff=0.2)
            self.opus, self.son, self.o_lbl = opus, son, o_lbl

            sweep_clear(self, time_span(LaggedStart(*[GrowFromEdge(s, DOWN) for s in opus], lag_ratio=0.4), 0.5, 1.9),
                        time_span(FadeIn(legend, lag_ratio=0.2), 0.8, 1.9),
                        time_span(FadeIn(o_name), 0.5, 1.4), time_span(FadeIn(o_lbl), 1.4, 1.9), run_time=1.9)
            self.play(*[TransformFromCopy(a, b) for a, b in zip(opus, son)], FadeIn(s_name, shift=0.2 * DOWN),
                      FadeIn(o_tot, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("drop")

            # Sonnet's rates: writes and output halve
            g_top = son[0].get_top()[1]
            gold_t = son[1].copy().stretch_to_fit_height(son[1].height / 2).move_to(
                [sx, g_top + son[1].height / 4, 0])
            red_t = son[2].copy().stretch_to_fit_height(son[2].height / 2).move_to(
                [sx, gold_t.get_top()[1] + son[2].height / 4, 0])
            s_tot = T("$159", 36, PURPLE).move_to([sx, red_t.get_top()[1] + 0.2 + o_tot.height / 2, 0])
            self.play(Transform(son[1], gold_t), Transform(son[2], red_t), run_time=2.0)
            self.play(TransformFromCopy(o_tot, s_tot), run_time=1.2)
            less = T("≈ 43% less", 36, GREEN).next_to(s_tot, RIGHT, buff=0.5)
            c.wait_until("forty-three")
            self.play(FadeIn(less, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("bars")

            s_g = seg_label("$40.8", son[0])
            self.play(TransformFromCopy(o_lbl[0], s_g), FlashAround(opus[0], color=GREEN, run_time=1.5),
                      FlashAround(son[0], color=GREEN, run_time=1.5), run_time=1.5)
            c.wait_until("halve")

            s_rest = VGroup(seg_label("$42.75", son[1]), seg_label("$76", son[2]))
            self.play(TransformFromCopy(o_lbl[1], s_rest[0]), TransformFromCopy(o_lbl[2], s_rest[1]),
                      FlashAround(son[1], color=GOLD, run_time=1.5), FlashAround(son[2], color=RED, run_time=1.5),
                      run_time=1.5)
            self.bars = VGroup(opus, son, o_lbl, s_g, s_rest, o_name, s_name, o_tot, s_tot)
            self.s_tot, self.less, self.legend = s_tot, less, legend
            c.wait_until()

    # c2.dials.3 ------------------------------------------------------
    def clip3(self):
        with self.say("c2.dials.3") as c:
            catch = VGroup(T("only if it takes the", 36, YELLOW), T("same number of turns", 36, YELLOW)).arrange(
                DOWN, buff=0.15).move_to([3.4, 2.97, 0])
            self.play(FadeOut(self.legend), FadeOut(self.less),
                      self.bars.animate.shift((-6.25 - self.opus.get_left()[0]) * RIGHT), run_time=1.5)
            self.play(FadeIn(catch, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("bench")

            title = T("SWE-Bench Pro", 30).move_to([4.55, 1.88, 0])
            rows = VGroup()
            for name, score, col in (("Opus", 90, BLUE), ("Sonnet 5.5", 81, PURPLE)):
                lbl = T(name, 28, col)
                b = Rectangle(width=score * 0.04, height=0.34).set_stroke(col, 2).set_fill(col, 0.85)
                v = T(f"≈ {score}", 28, BG, weight=BOLD)
                rows.add(VGroup(lbl, b, v))
            for i, r in enumerate(rows):
                r[1].move_to([2.75 + r[1].width / 2, 1.4 - 0.44 * i, 0])
                r[0].next_to(r[1], LEFT, buff=0.2)
                r[2].move_to(r[1].get_right() + 0.5 * LEFT)
            bench = VGroup(title, rows)
            self.play(FadeIn(title, shift=0.2 * DOWN),
                      LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in rows], lag_ratio=0.4), run_time=1.8)
            c.wait_until("grow")

            base = self.opus.get_bottom()[1]
            steps = VGroup()
            for i in range(1, 13):
                h = 0.17 * i
                s = Rectangle(width=0.42, height=h)
                if i <= 8:
                    s.set_stroke(PURPLE, 2).set_fill(PURPLE, 0.6)
                else:
                    s.set_stroke(RED, 3).set_fill(PURPLE, 0.15)
                s.move_to([0.4 + 0.42 * (i - 0.5), base + h / 2, 0])
                steps.add(s)
            base_steps, extra = steps[:8], steps[8:]
            turns = T("Sonnet's turns", 28, PURPLE).next_to(base_steps, UP, buff=0.3, aligned_edge=LEFT)
            turns.set_y(base_steps.get_top()[1] + 0.35)
            ex_lbl = VGroup(T("extra check runs", 28, RED), T("review rounds", 28, RED)).arrange(
                DOWN, buff=0.1, aligned_edge=RIGHT)
            ex_lbl.next_to(extra, UP, buff=0.15).align_to(extra, RIGHT)
            self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in base_steps], lag_ratio=0.15),
                      time_span(FadeIn(turns), 0.6, 1.5), run_time=1.5)

            o_top, s_top = self.opus.get_top()[1], self.son.get_top()[1]
            w = self.son.width
            rise = Rectangle(width=w, height=o_top - s_top).set_stroke(RED, 3).set_fill(RED, 0.15)
            rise.move_to([self.son.get_x(), (o_top + s_top) / 2, 0])
            level = DashedLine([self.opus.get_left()[0] - 0.1, o_top, 0], [self.son.get_right()[0] + 0.1, o_top, 0],
                               dash_length=0.1).set_stroke(BLUE, 2)
            new_tot = T("≈ $278", 36, PURPLE).next_to(rise, UP, buff=0.2)
            self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in extra], lag_ratio=0.3),
                      time_span(LaggedStart(*[FadeIn(l, shift=0.2 * DOWN) for l in ex_lbl], lag_ratio=0.3), 0.4, 1.6),
                      GrowFromEdge(rise, DOWN), Create(level),
                      time_span(FadeOut(self.s_tot, shift=0.3 * UP), 0, 0.9), time_span(FadeIn(new_tot, shift=0.3 * UP), 1.3, 2.5),
                      run_time=2.5)
            c.wait_until("under")

            cav = VGroup(T("transcripts may undercount output", 28, DIM),
                         T("→ Sonnet's saving would be larger", 28, DIM)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            cav.move_to([3.4, -2.95, 0])
            self.play(FadeIn(cav, shift=0.2 * UP), run_time=1.0)
            self.cav = cav
            c.wait_until()

    # c2.dials.4 ------------------------------------------------------
    def clip4(self):
        with self.say("c2.dials.4") as c:
            ms = master_shot().shift(0.4 * DOWN)
            fix = ms.builders[4]
            sweep_clear(self, time_span(FadeIn(ms, lag_ratio=0.1), 0.5, 1.4), run_time=1.4)
            self.play(fix.box.animate.set_stroke(PURPLE, 4).set_fill(PURPLE, 0.5),
                      FlashAround(fix, color=PURPLE, run_time=1.0), run_time=1.0)
            c.wait_until("safe")

            safe = T("the safe place for Sonnet", 32, GREEN).next_to(fix, DOWN, buff=0.35)
            safe.shift((min(6.5 - safe.get_right()[0], 0)) * RIGHT)
            self.play(FadeIn(safe, shift=0.2 * UP), run_time=1.0)
            c.wait_until("prod")

            note = VGroup(T("Sonnet? small saving:", 28, DIM), T("lean now", 28, DIM)).arrange(
                DOWN, buff=0.08, aligned_edge=LEFT).next_to(ms.prod, RIGHT, buff=0.4)
            self.play(FadeIn(note, shift=0.2 * LEFT), ms.prod.box.animate.set_stroke(DIM, 3), run_time=1.0)
            c.wait_until()

    # c2.dials.5 ------------------------------------------------------
    def clip5(self):
        with self.say("c2.dials.5") as c:
            box = builder_box().move_to([-3.35, -0.4, 0])
            ed, md = box.dials.effort, box.dials.model
            head = T("effort level: how much it thinks before it acts", 36).move_to(3.0 * UP)
            sweep_clear(self, time_span(FadeIn(box), 0.4, 1.4), run_time=1.4)
            self.play(ed.rim.animate.set_stroke(YELLOW, 6), ed.name.animate.set_color(YELLOW),
                      FlashAround(ed, run_time=1.2), time_span(FadeIn(head, shift=0.2 * DOWN), 0.2, 1.2),
                      run_time=1.2)
            c.wait_until("tuned")

            tuned = T("set per agent type · never tuned", 30, DIM).next_to(box, DOWN, buff=0.4)
            self.play(FadeIn(tuned, shift=0.2 * UP), run_time=1.0)
            c.wait_until("direct")

            pk = peak_bar(x=2.0, bottom=-2.6, height=4.0, width=0.9)
            think, think_t = pk.think, pk.labels[4]
            arrow = Arrow([box.get_right()[0] - 0.05, ed.rim.get_y(), 0], think.get_left(), buff=0.12,
                          stroke_width=4).set_color(RED)
            self.play(Create(pk.outline), FadeIn(pk.header, shift=0.2 * DOWN),
                      LaggedStart(*[GrowFromEdge(sg, DOWN) for sg in pk.segs], lag_ratio=0.2), run_time=1.4)
            self.play(GrowArrow(arrow), FadeIn(think_t, shift=0.2 * LEFT), FlashAround(think, color=RED, run_time=1.2),
                      run_time=1.2)
            c.wait_until("again")

            short = think.copy().stretch_to_fit_height(think.height * 0.55, about_edge=DOWN)
            checks = VGroup(*[Square(0.55).set_stroke(RED, 3).set_fill(BG, 0) for _ in range(3)]).arrange(RIGHT, buff=0.15)
            checks.move_to([think_t.get_left()[0], -0.45, 0], aligned_edge=LEFT)
            more = T("more check runs", 28, RED).next_to(checks, DOWN, buff=0.25, aligned_edge=LEFT)
            self.play(Transform(think, short), run_time=1.5)
            self.play(LaggedStart(*[GrowFromCenter(sq) for sq in checks], lag_ratio=0.3),
                      time_span(FadeIn(more, shift=0.2 * UP), 0.5, 1.5), run_time=1.5)
            c.wait_until("measure")

            tags = VGroup(*[T("measure it", 30, YELLOW).next_to(box, UP, buff=0.2).set_x(d.rim.get_x())
                            for d in (md, ed)])
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * DOWN) for t in tags], lag_ratio=0.3),
                      md.rim.animate.set_stroke(YELLOW, 6), run_time=1.2)
            c.wait_until()
