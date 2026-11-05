"""Chapter 5, scene 7: irrational and complex exponents give infinitely many values. Clips c5.inf.1 – c5.inf.4.

Shared helpers (import with load_scene("ch5_s7_infinite")):
  frame3_fill(frame)   gallery frame 3: GOLD circle (schematic radius for 2^{sqrt2} ~ 2.67) densely dotted
                       (values of (2i)^{sqrt2}, n = -200..200, TEAL; principal GREEN) + label above the frame
                       "(2i)^{sqrt2}   r = 2^{sqrt2} ~ 2.67"; .circ .dots (ordered n = 0, 1, -1, 2, ...) .principal .label.
  frame4_fill(frame)   gallery frame 4: values of (2i)^{0.1+0.03i}, n = -5..10, on a faint TEAL spiral
                       (radii drawn as r^0.6 so it fits; still a log spiral); .curve .dots .principal .label.
  gallery_caption(frame, text)   s6's filled_caption, nudged so frames 3-4 captions keep a gap.
  full_gallery()       the four frames, all filled and captioned (no card): for the recap.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch5_s3_two_i")
S5 = load_scene("ch5_s5_count")
S6 = load_scene("ch5_s6_finite")

SQ2 = float(np.sqrt(2))
LN2 = float(np.log(2))
W = complex(0.1, 0.03)          # the spiral's exponent (ours)
CAP3 = "irrational: ∞"
CAP4 = "imaginary part: ∞"
WC, R, COL, ROWS = S6.WC, S6.R, S6.COL, S6.ROWS
O4 = np.array([3.7, 1.7, 0])   # work-area spiral origin
U4 = 1.1                        # its unit


# ---------------------------------------------------------------- shared helpers
def gallery_caption(frame, text):
    cap = S6.filled_caption(frame, text)
    return cap.shift({CAP3: 0.25, CAP4: 0.2}.get(text, 0.0) * RIGHT)


def frame3_fill(frame):
    o = frame.origin
    rad = 0.92
    circ = Circle(radius=rad, color=GOLD, stroke_width=2.5).move_to(o)
    order = [0]
    for k in range(1, 201):
        order += [k, -k]
    dots = VGroup()
    for n in order:
        a = SQ2 * (PI / 2 + TAU * n)
        p = o + rad * np.array([np.cos(a), np.sin(a), 0])
        if n == 0:
            principal = Dot(p, radius=0.075, color=GREEN).set_z_index(2)
            dots.add(principal)
        else:
            dots.add(Dot(p, radius=0.028, color=TEAL))
    lab = MathTex("(", "2i", r")^{\sqrt2}", font_size=32)
    lab[1].set_color(YELLOW)
    rl = MathTex(r"r = 2^{\sqrt2}\approx 2.67", font_size=30, color=GOLD)
    label = VGroup(lab, rl).arrange(RIGHT, buff=0.35)
    label.next_to(frame.box, UP, buff=0.15)
    g = VGroup(circ, dots, label)
    g.circ, g.dots, g.principal, g.label, g.name, g.radius = circ, dots, principal, label, lab, rl
    return g


def spiral_point(origin, unit, n, p=0.6):
    v = W * complex(LN2, PI / 2 + TAU * n)
    rr = unit * np.exp(v.real) ** p
    return np.array(origin, dtype=float) + rr * np.array([np.cos(v.imag), np.sin(v.imag), 0])


def spiral(origin, unit, dot_r=0.06, ns=range(-5, 11)):
    curve = VMobject().set_points_as_corners([spiral_point(origin, unit, t)
                                               for t in np.linspace(-5.3, 10.4, 500)])
    curve.set_stroke(TEAL, 2, opacity=0.35)
    dots = VGroup()
    principal = None
    for n in ns:
        d = Dot(spiral_point(origin, unit, n), radius=dot_r * (1.5 if n == 0 else 1),
                color=GREEN if n == 0 else TEAL).set_z_index(2)
        if n == 0:
            principal = d
        dots.add(d)
    return curve, dots, principal


def spiral_label(size=32):
    lab = MathTex("(", "2i", r")^{0.1+0.03i}", font_size=size)
    lab[1].set_color(YELLOW)
    return lab


def frame4_fill(frame):
    curve, dots, principal = spiral(frame.origin, frame.u, dot_r=0.045)
    label = spiral_label().next_to(frame.box, UP, buff=0.15)
    g = VGroup(curve, dots, label)
    g.curve, g.dots, g.principal, g.label = curve, dots, principal, label
    return g


def full_gallery():
    shot = S6.handover_shot()
    frames = shot[1]
    f3, f4 = frames[2], frames[3]
    fill3, fill4 = frame3_fill(f3), frame4_fill(f4)
    caps = []
    for f, txt in ((f3, CAP3), (f4, CAP4)):
        cap = gallery_caption(f, txt)
        f.remove(f.caption)
        f.caption = cap
        caps.append(cap)
    g = VGroup(*shot[1:], fill3, caps[0], fill4, caps[1])
    g.frames = list(frames)
    g.fills = [shot[2], shot[4], fill3, fill4]
    return g


def on_circle(turns):
    return S6.on_circle(turns)


def reveal(dots, counter=None, n0=0):
    """Dots (added at opacity 0) light up one after another over the play; counter shows n0 + count."""
    state = {"k": 0}

    def f(m, a):
        k = int(round(a * len(dots)))
        for d in dots[state["k"]:k]:
            d.set_opacity(1)
        state["k"] = max(state["k"], k)
        if counter is not None:
            counter.set_value(n0 + state["k"])
    return UpdateFromAlphaFunc(dots, f)


def hidden_dots(points, radius=0.035, color=TEAL):
    return VGroup(*[Dot(p, radius=radius, color=color).set_opacity(0) for p in points])


# ---------------------------------------------------------------- scene
class Infinite(NarratedScene):
    def construct(self):
        shot = S6.handover_shot()
        self.add(shot)
        card, frames = shot[0], shot[1]
        f1, f2, f3, f4 = frames

        # ---------------- clip 1: irrational exponent, dots never repeat
        with self.say("c5.inf.1") as c:
            head = MathTex(r"\text{iii)}\quad", "z_2", r"\text{ real and irrational}", font_size=44)
            head[1].set_color(YELLOW)
            S6.left_at(head, ROWS[0])
            self.play(card.animate.scale(0.72).move_to([0, 3.28, 0]), run_time=1.0)
            self.play(*appear(head), run_time=0.9)  # early: case heading
            c.wait_until("like root two")
            ex = MathTex("z_2", "=", r"\sqrt2", font_size=48)
            ex[0].set_color(YELLOW)
            ex[2].set_color(GOLD)
            S6.left_at(ex, ROWS[1])
            self.play(*appear(ex), run_time=1.0)

            c.wait_until("step")
            fac = MathTex(r"e^{2\pi i n\sqrt2}", font_size=56, color=TEAL)
            fac.next_to(ex, RIGHT, buff=0.9)
            unit = Circle(radius=R, color=DIM, stroke_width=2).move_to(WC)
            axes = S6.work_axes(WC, R)
            theta = ValueTracker(0)   # in turns
            dot = Dot(on_circle(0), radius=0.1, color=YELLOW).set_z_index(3)
            dot.add_updater(lambda m: m.move_to(on_circle(theta.get_value())))
            arrow = always_redraw(lambda: Arrow(WC, on_circle(theta.get_value()), buff=0, color=TEAL,
                                                stroke_width=4, max_tip_length_to_length_ratio=0.15))
            landing = VGroup(Dot(on_circle(0), radius=0.08, color=TEAL).set_z_index(2))
            self.play(*appear(fac, shift=None), FlashAround(card.factor, run_time=1.2),
                      FadeIn(unit), FadeIn(axes), run_time=1.2)
            self.play(FadeIn(dot), FadeIn(arrow), FadeIn(landing[0]), run_time=0.6)

            cnt = VGroup(MathTex("n =", font_size=40), Integer(0, font_size=40))
            cnt.arrange(RIGHT, buff=0.18)
            S6.left_at(cnt, ROWS[2])

            def step(k, rt):
                self.play(theta.animate.set_value((k + 1) * SQ2), run_time=rt)
                d = Dot(on_circle((k + 1) * SQ2), radius=0.08, color=TEAL).set_z_index(2)
                landing.add(d)
                self.add(d)
                cnt[1].set_value(k + 1)

            step(0, max(0.8, min(2.0, c.until("never") - 0.2)))
            c.wait_until("never")
            self.play(*appear(cnt), run_time=0.8)
            step(1, 1.3)
            budget = c.until("whole number")
            for k in range(2, 5):
                step(k, max(0.4, min(0.8, (budget - 2.1) / 3)))
            c.wait_until("whole number")
            iff = MathTex(r"n\sqrt2\in\mathbb{Z}\ \text{ only for }\ n = 0", font_size=40)
            iff.move_to([0, ROWS[2], 0]).align_to([-0.6, 0, 0], LEFT)
            self.play(*appear(iff), run_time=1.0)
            budget = c.until("norepeat")
            for k in range(5, 10):
                step(k, max(0.3, min(0.6, (budget - 0.2) / 5)))
            c.wait_until("norepeat")
            dot.clear_updaters()
            arrow.clear_updaters()
            self.remove(theta)
            pts = [on_circle(n * SQ2) for n in range(11, 301)]
            cloud = hidden_dots(pts, radius=0.04)
            self.add(cloud)
            self.play(*during([FadeOut(dot), FadeOut(arrow)], 0, 0.15),
                      reveal(cloud, cnt[1], 10), rate_func=linear,
                      run_time=max(1.0, c.until("infinite") - 0.1))
            c.wait_until("infinite")
            inf = MathTex(r"\infty", r"\text{ many values}", font_size=44, color=YELLOW)
            inf.move_to(fac).align_to(fac, LEFT)
            self.play(*swap(fac, inf), run_time=1.2)

        # ---------------- clip 2: one modulus, one circle, filled densely; frame 3
        with self.say("c5.inf.2") as c:
            mod = MathTex(r"\text{all with modulus }", r"|z_1|^{z_2}", font_size=40)
            mod[1].set_color(GOLD)
            mod.move_to(iff).align_to(iff, LEFT)
            self.play(*swap(iff, mod), run_time=1.2)
            c.wait_until("circle")
            self.play(restyle(unit, outline=GOLD, width=3),
                      VShowPassingFlash(unit.copy().set_stroke(GOLD, 6), time_width=0.4), run_time=1.5)
            c.wait_until("dense")
            pts2 = [on_circle(n * SQ2) for n in range(301, 1201)]
            cloud2 = hidden_dots(pts2, radius=0.035)
            self.add(cloud2)
            self.play(reveal(cloud2, cnt[1], 300), rate_func=linear,
                      run_time=max(1.5, min(3.2, c.until("example") - 0.2)))

            c.wait_until("example")
            fill3 = frame3_fill(f3)
            for d in fill3.dots:
                d.set_opacity(0)
            self.add(fill3.dots)
            self.play(*appear(fill3.name), Create(fill3.circ), run_time=1.2)
            self.play(reveal(fill3.dots), rate_func=linear, run_time=1.6)
            c.wait_until("radius")
            self.play(*appear(fill3.radius), run_time=1.0)
            cap3 = gallery_caption(f3, CAP3)
            self.play(*swap(f3.caption, cap3), run_time=min(1.2, max(0.6, c.remaining - 0.1)))
            settle(self, fill3)

        # ---------------- clip 3: complex exponent, different moduli
        with self.say("c5.inf.3") as c:
            head4 = MathTex(r"\text{iv)}\quad", "z_2", "=", "x", "+", "i", "y", r",\quad", "y", r"\neq 0",
                            font_size=50)
            head4[1].set_color(YELLOW)
            for i in (5, 6, 8):
                head4[i].set_color(PINK)
            head4.move_to([0, 2.15, 0])
            sweep_clear(self, *appear(head4, shift=None), keep=[shot, fill3, cap3], run_time=1.6)  # early: case heading
            c.wait_until("formula")
            form = MathTex(r"\left|e^{2\pi i n z_2}\right|", "=", r"e^{-2\pi n y}", font_size=60, color=GOLD)
            form.move_to([0, 1.2, 0])
            self.play(*appear(form, shift=None), run_time=1.6)
            c.wait_until("differ")
            diff = MathTex(r"\text{different for different }", "n", font_size=42)
            diff.move_to([0, 0.3, 0])
            self.play(*appear(diff), run_time=1.0)
            c.wait_until("infinite2")
            inf2 = MathTex(r"\infty", r"\text{ many values, with different moduli}", font_size=42)
            inf2[0].set_color(YELLOW)
            inf2.move_to([0, 0.3, 0])
            self.play(*swap(diff, inf2), run_time=1.2)
            c.wait_until("x")
            self.play(head4[3].animate.set_color(DIM), FlashAround(head4[3], run_time=1.2), run_time=1.2)

        # ---------------- clip 4: the ray of 2^i, the spiral, the gallery
        with self.say("c5.inf.4") as c:
            ray = S3.two_i_ray(step=1.0, center=[-2.2, 1.15, 0], n_max=1, size=28, dot_r=0.09)
            sweep_clear(self, time_span(FadeIn(ray), 0.7, 1.5), keep=[shot, fill3, cap3], run_time=1.5)
            xz = MathTex(r"2^{\,i}:", r"\quad x = 0,\ \ y = 1", font_size=44)
            xz.move_to([0, 1.55, 0]).align_to([0.0, 0, 0], LEFT)
            c.wait_until("equal to zero")
            self.play(*appear(xz), run_time=1.0)
            c.wait_until("one ray")
            apart = MathTex(r"\text{values a factor }", r"e^{2\pi}\approx 535", r"\text{ apart}", font_size=40)
            apart[1].set_color(GOLD)
            apart.move_to([0, 0.55, 0]).align_to(xz, LEFT)
            self.play(*appear(apart), *flash([ray.tick_labels[0]]), run_time=1.2)

            c.wait_until("real part")
            unit4 = Circle(radius=U4, color=DIM, stroke_width=2).move_to(O4)
            axes4 = S6.work_axes(O4, U4)
            curve, sdots, sprin = spiral(O4, U4, dot_r=0.07)
            slab = spiral_label(36).move_to([0, 0.35, 0]).align_to([6.55, 0, 0], RIGHT)
            self.play(*during(disappear(xz, apart, ray), 0, 0.3),
                      *during([FadeIn(unit4), FadeIn(axes4)], 0.3, 0.55),
                      *during([Create(curve), *appear(*sdots, shift=None, lag=0.12)], 0.4, 1),
                      run_time=2.6)
            self.play(*appear(slab), run_time=0.8)
            c.wait_until("trace out")
            fill4 = frame4_fill(f4)
            self.play(ReplacementTransform(curve, fill4.curve),
                      *[ReplacementTransform(a, b) for a, b in zip(sdots, fill4.dots)],
                      ReplacementTransform(slab, fill4.label),
                      FadeOut(unit4), FadeOut(axes4), run_time=1.5)
            settle(self, fill4)
            cap4 = gallery_caption(f4, CAP4)
            self.play(*swap(f4.caption, cap4), run_time=1.0)

            c.wait_until("gallery")
            prev = None
            for f, cue in zip(frames, ("one value", "q values", "filled densely", "and a spiral")):
                c.wait_until(cue)
                anims = [restyle(f.box, outline=YELLOW, width=3.5)]
                if prev is not None:
                    anims.append(restyle(prev.box, outline=DIM, width=2))
                self.play(*anims, run_time=0.8)
                prev = f
            c.wait_until()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
