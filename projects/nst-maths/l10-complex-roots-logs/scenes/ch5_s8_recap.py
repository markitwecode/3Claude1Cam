"""Chapter 5, scene 8: recap in five cards, then the turning arrow and its shadow next time. Clips c5.recap.1 – c5.recap.2."""
# style: 2
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

S2 = load_scene("ch5_s2_define")
S3 = load_scene("ch5_s3_two_i")
S5 = load_scene("ch5_s5_count")
S7 = load_scene("ch5_s7_infinite")
PH = load_scene("ch6_s3_phasor")

LN2 = float(np.log(2))
TOP_CAP_Y = 0.3     # centre of the top row's two-line captions
BOT_CAP_Y = -3.35    # the bottom row's one-line captions
CAP = 38             # caption size (MathTex)

NC = np.array([3.6, -0.35, 0.0])   # the "next time" plane's centre
SC = 0.7                           # its scale
LIST_X, LIST_TOP, LIST_GAP = -6.4, 3.0, 0.45


def strip_text(g):
    """Remove every Text / MathTex inside g (labels are unreadable at thumbnail size)."""
    for sub in list(g.submobjects):
        if isinstance(sub, (Text, MathTex, SingleStringMathTex)):
            g.remove(sub)
        else:
            strip_text(sub)
    return g


def caption(*lines, y=TOP_CAP_Y, x=0.0):
    mobs = [MathTex(s, font_size=CAP) for s in lines]
    g = VGroup(*mobs).arrange(DOWN, buff=0.16)
    g.move_to([x, y, 0])
    return g


def card_r1():
    d = S2.definition_box(size=120, note=False)
    pic = VGroup(d.box, d.tex)
    pic.scale(3.6 / d.box.width).move_to([-4.6, 3.2, 0])
    lx = d.lnz.get_center()[0]
    top = d.box.get_bottom()[1] - 0.3
    lad = S5.ladder(ns=(-1, 0, 1), x=lx, y0=top - 0.6, pitch=0.45, brace=False, ext=0.18)
    cap = caption(r"\text{every rung of }\ln z", r"\text{gives a value}", x=-4.6)
    return d, lad, cap


def card_r2():
    ray = S3.two_i_ray(step=0.95, angle=LN2, center=np.array([-0.1, 2.35, 0]), n_max=1, size=30, dot_r=0.09)
    i0 = ray.ns.index(0)
    n0 = ray.n_labels[i0]
    for k in range(len(ray.ns)):
        ray.tick_labels[k].set_opacity(0)
    cap = caption(r"2^i = e^{-2\pi n}", r"(\cos\ln 2 + i\sin\ln 2)", x=-0.1)
    return ray, n0, cap


def card_r3():
    strip = S3.two_i_ray(step=1.05, angle=0, center=np.array([4.45, 2.4, 0]), n_max=1, size=30,
                         tick_tex=[r"e^{-5\pi/2}", r"e^{-\pi/2}", r"e^{3\pi/2}"],
                         n_tex=["n=1", "n=0", "n=-1"], dot_r=0.1)
    for k, n in enumerate(strip.ns):
        strip.tick_labels[k].set_color(GREEN if n == 0 else TEAL)
    cap = caption(r"i^i = e^{-\pi/2 - 2\pi n}", r"\text{all real}", x=4.45)
    return strip, cap


def card_r4():
    lad = S5.ladder(ns=(-1, 0, 1, 2), x=-5.55, y0=-1.85, pitch=0.55, brace=True, ext=0.3)
    factor = S5.question_card().factor.copy()
    factor.scale(1.45).move_to([-3.65, -1.25, 0])
    arrows = [Arrow(lad.rungs[n].get_center(), factor.get_left(), buff=0.14, stroke_width=2.5,
                    color=TEAL, tip_length=0.14, max_tip_length_to_length_ratio=0.2)
              for n in (2, 1, 0, -1)]
    cap = caption(r"\text{count the factors}", y=BOT_CAP_Y, x=-4.6)
    return lad, factor, arrows, cap


def card_r5():
    g = strip_text(S7.full_gallery())
    frames = g.frames
    ref = VGroup(*frames)
    c = ref.get_center().copy()
    s = 8.4 / ref.width
    dst = np.array([2.3, -1.35, 0])
    g.scale(s, about_point=c).shift(dst - c)
    pieces = [VGroup(f, fill) for f, fill in zip(frames, g.fills)]
    xs = [f.get_center()[0] for f in frames]
    y = frames[0].get_bottom()[1] - 0.42
    counts = [MathTex(t, font_size=44, color=GOLD).move_to([x, y, 0]) for t, x in zip(("1", "q", r"\infty", r"\infty"), xs)]
    seps = [MathTex(r"\cdot", font_size=44, color=DIM).move_to([(xs[k] + xs[k + 1]) / 2, y, 0]) for k in range(3)]
    return pieces, counts, seps


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(8.0)   # end card; the music swells and carries it
        self.ph.clear_updaters()
        self.moving.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    def clip1(self):
        with self.say("c5.recap.1") as c:
            # r1: the boxed definition, the ladder hanging from ln z
            c.wait_until("r1")
            d, lad1, cap1 = card_r1()
            self.play(FadeIn(d.box), *appear(d.tex, shift=None), run_time=1.0)
            c.wait_until("log zed")
            self.play(FlashUnder(d.lnz, color=GOLD, run_time=1.2, time_width=1.5))
            c.wait_until("values")
            rungs1 = [lad1.rungs[n] for n in (-1, 0, 1)]
            self.play(FadeIn(lad1.line), *appear(*rungs1, shift=None, lag=0.2), run_time=1.2)
            c.wait_until("rungs")
            self.play(*appear(cap1), run_time=1.0)  # early: the recap line sums up the sentence
            p1 = [d.box, d.tex, lad1.line, *rungs1]

            # r2: the values of 2^i on one ray
            c.wait_until("r2")
            ray, n0, cap2 = card_r2()
            self.play(Create(ray.line), FadeIn(ray.ticks), run_time=1.2)
            c.wait_until("infinitely many")
            i0 = ray.ns.index(0)
            others = [ray.dots[k] for k in range(len(ray.ns)) if k != i0]
            self.play(GrowFromCenter(ray.dots[i0]), *appear(n0, shift=None),
                      *appear(*others, ray.many, shift=None, lag=0.15), run_time=1.3)
            c.wait_until("one ray")
            self.play(VShowPassingFlash(ray.line.copy().set_stroke(YELLOW, 7), time_width=0.6), run_time=1.2)
            c.wait_until("moduli")
            self.play(*appear(cap2), run_time=1.0)  # early: the recap line sums up the sentence
            p2 = [ray.line, ray.ticks, *ray.dots, ray.many, n0]

            # r3: i^i on the positive real axis
            c.wait_until("r3")
            strip, cap3 = card_r3()
            self.play(Create(strip.line), FadeIn(strip.ticks), *appear(*strip.dots, shift=None, lag=0.15),
                      FadeIn(strip.many), run_time=1.4)
            c.wait_until("real")
            self.play(*appear(cap3), run_time=1.0)  # early: the recap line sums up the sentence
            c.wait_until("principal")
            k0 = strip.ns.index(0)
            self.play(*appear(strip.tick_labels[k0]),
                      FlashAround(strip.dots[k0], color=GREEN, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("minus pi over two")
            others3 = [strip.tick_labels[k] for k in range(len(strip.ns)) if k != k0]
            self.play(*appear(*others3, shift=None, lag=0.2), run_time=min(1.0, c.until("r4")))
            p3 = [strip.line, strip.ticks, *strip.dots, strip.many, *strip.tick_labels]

            # r4: the ladder's rungs feed the factor
            c.wait_until("r4")
            lad4, factor, arrows, cap4 = card_r4()
            rungs4 = [lad4.rungs[n] for n in (-1, 0, 1, 2)]
            self.play(FadeIn(lad4.line), *appear(*rungs4, shift=None, lag=0.15),
                      GrowFromCenter(lad4.brace), *appear(lad4.brace_label, shift=None), run_time=1.2)
            c.wait_until("counting")
            self.play(*appear(cap4), run_time=1.0)  # early: the recap line sums up the sentence
            c.wait_until("factors")
            self.play(*appear(factor), run_time=1.0)
            c.wait_until("two pi eye")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
                      run_time=min(1.5, c.until(None)))
            if c.remaining > 1.4:
                self.play(FlashAround(factor, color=TEAL, run_time=1.2, time_width=1.5), run_time=1.2)
            p4 = [lad4.line, *rungs4, lad4.brace, lad4.brace_label, factor, *arrows]

            self.pics = [*p1, *p2, *p3, *p4]
            self.caps = [cap1, cap2, cap3, cap4]

    def clip2(self):
        heading = T("Next time", 40, color=DIM).move_to([NC[0], 3.3, 0])
        plane = strip_text(PH.argand_plane())
        circ = PH.plane_circle()
        VGroup(plane, circ).scale(SC, about_point=PH.P0).shift(NC - PH.P0)
        next_cap = T("a swinging pendulum, as a shadow", 30).move_to([NC[0], -3.35, 0])

        ph = ValueTracker(PH.PHI0)
        op = ValueTracker(0.0)

        def build():
            p = ph.get_value()
            g = VGroup(PH.shadow(p), PH.phasor_arrow(p).set_z_index(3))
            g.scale(SC, about_point=PH.P0).shift(NC - PH.P0)
            return g.set_opacity(op.get_value())

        moving = always_redraw(build)
        self.ph, self.moving = ph, moving

        with self.say("c5.recap.2") as c:
            # r5: the gallery, one frame per count
            pieces, counts, seps = card_r5()
            for k, cue in enumerate(("r5", "fraction", "irrational", "complex")):
                c.wait_until(cue)
                extra = [*appear(seps[k - 1], shift=None)] if k else []
                self.play(FadeIn(pieces[k]), *appear(counts[k]), *extra, run_time=1.0)
            c.wait_until("next")

            # the pictures go; the lines gather into the recap list on the left
            cap5 = VGroup(counts[0], seps[0], counts[1], seps[1], counts[2], seps[2], counts[3])
            self.remove(*counts, *seps)
            self.add(cap5)
            caps = [*self.caps, cap5]
            y = LIST_TOP
            moves = []
            for k, cap in enumerate(caps):
                cap.generate_target()
                if k < 4:
                    cap.target.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
                else:
                    cap.target.arrange(RIGHT, buff=0.2)
                cap.target.scale(1.2)
                cap.target.move_to([0, y - cap.target.height / 2, 0]).align_to([LIST_X, 0, 0], LEFT)
                y -= cap.target.height + LIST_GAP
            mid = (LIST_TOP + y + LIST_GAP) / 2
            for k, cap in enumerate(caps):
                cap.target.shift(-mid * UP)
                a = 0.3 + 0.13 * k
                moves += during([MoveToTarget(cap)], a, a + 0.18)
            self.play(*during([FadeOut(p) for p in [*self.pics, *pieces]], 0, 0.3),
                      *moves, run_time=2.6)
            c.wait_until("physical world")
            self.play(*appear(heading), FadeIn(plane), Create(circ), run_time=1.2)

            ph.add_updater(lambda m, dt: m.increment_value(PH.OMEGA * dt))
            self.add(ph, moving)
            c.wait_until(own_word=next_cap)
            self.play(*appear(next_cap), op.animate.set_value(1.0), run_time=1.2)
