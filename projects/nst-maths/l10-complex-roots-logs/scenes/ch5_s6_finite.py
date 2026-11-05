"""Chapter 5, scene 6: integer and rational exponents give finitely many values. Clips c5.fin.1 – c5.fin.5.

Shared helpers (import with load_scene("ch5_s6_finite")):
  frame1_dot(frame)    gallery frame 1's fill: GREEN dot at -4 (schematic, left end of the real axis)
                       and the label "(2i)^2 = -4" above the frame; .dot .label.
  frame2_ring(frame)   gallery frame 2's fill: ch2's ring of five (GOLD dashed circle, GREEN first
                       dot at pi/10, TEAL others) scaled to the frame; .circ .dots.
  filled_caption(frame, text)   a replacement caption in the frame's caption slot.
  handover_shot()      card + frames, 1-2 filled ("integer: 1 value", "fraction p/q: q values"; labels
                       "(2i)^2 = -4" and "(2i)^{1/5}" above), 3-4 empty.
"""
# style: 2
# handover: next
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

S5 = load_scene("ch5_s5_count")

CAP1 = "integer: 1 value"
CAP2 = "fraction p/q: q values"
WC = np.array([-4.6, 1.2, 0])     # work circle centre
R = 1.2                           # work unit-circle radius
RC = np.array([-4.6, 1.3, 0])     # ring-of-five centre in the work area
COL = -2.6                        # left edge of the right-hand column
ROWS = (2.2, 1.3, 0.4, -0.3)


# ---------------------------------------------------------------- shared helpers
def filled_caption(frame, text):
    """A frame's caption once filled (size 28, so neighbouring captions keep a gap)."""
    cap = T(text, size=28, color=FG, t2s={"p/q": ITALIC, ": q": ITALIC})
    nudge = {CAP1: -0.35, CAP2: 0.1}.get(text, 0.0)   # frames 1-2 captions lean apart
    return cap.move_to(frame.caption).shift(nudge * RIGHT)


def frame1_dot(frame):
    dot = Dot(frame.P(-1.5, 0), radius=0.09, color=GREEN)
    lab = MathTex("(", "2i", r")^2 = -4", font_size=32)
    lab[1].set_color(YELLOW)
    lab.next_to(frame.box, UP, buff=0.15)
    g = VGroup(dot, lab)
    g.dot, g.label = dot, lab
    return g


def ring_work():
    """ch2 s1's ring_of_five(), unchanged in size, moved to RC."""
    S2 = load_scene("ch2_s1_hook")
    circ, dots = S2.ring_of_five()
    g = VGroup(circ, dots)
    g.shift(RC - S2.O)
    g.circ, g.dots = circ, dots
    return g


def frame2_ring(frame):
    S2 = load_scene("ch2_s1_hook")
    circ, dots = S2.ring_of_five()
    g = VGroup(circ, dots)
    g.scale(frame.u / S2.U, about_point=S2.O).shift(frame.origin - S2.O)
    for d in dots:
        d.scale(1.35)
    circ.set_stroke(width=2.5)
    g.circ, g.dots = circ, dots
    return g


def frame2_label(frame):
    """Gallery frame 2's label, in frame 1's style: "(2i)^{1/5}" above the frame."""
    lab = MathTex("(", "2i", r")^{1/5}", font_size=32)
    lab[1].set_color(YELLOW)
    return lab.next_to(frame.box, UP, buff=0.15)


def handover_shot():
    card = S5.question_card(highlight=True)
    frames = S5.gallery_frames()
    f1, f2 = frames[0], frames[1]
    caps = [filled_caption(f, txt) for f, txt in ((f1, CAP1), (f2, CAP2))]
    for f, cap in zip((f1, f2), caps):
        f.remove(f.caption)
        f.caption = cap
    return VGroup(card, frames, frame1_dot(f1), caps[0], frame2_ring(f2), caps[1], frame2_label(f2))


def on_circle(turns, r=R, c=WC):
    a = TAU * turns
    return c + r * np.array([np.cos(a), np.sin(a), 0])


def work_axes(c, r):
    return VGroup(Line(c + (r + 0.25) * LEFT, c + (r + 0.25) * RIGHT, stroke_width=1.5, color=DIM),
                  Line(c + (r + 0.2) * DOWN, c + (r + 0.2) * UP, stroke_width=1.5, color=DIM))


def left_at(mob, y, x=COL):
    mob.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    return mob


# ---------------------------------------------------------------- scene
class Finite(NarratedScene):
    def construct(self):
        shot = S5.handover_shot()
        self.add(shot)
        card, frames = shot[0], shot[1]
        f1, f2 = frames[0], frames[1]
        card_c = card.get_center()

        # ---------------- clip 1: integer exponent, whole turns
        with self.say("c5.fin.1") as c:
            self.play(card.animate.scale(0.72).move_to([0, 3.28, 0]), run_time=1.0)
            head = MathTex(r"\text{i)}\quad", "z_2", r"= m \in \mathbb{Z}", font_size=44)
            head[1].set_color(YELLOW)
            left_at(head, ROWS[0])
            self.play(*appear(head), run_time=0.9)  # early: case heading
            c.wait_until("factor")

            fac = MathTex(r"e^{2\pi i n m}", "=", "?", font_size=56)
            fac[0].set_color(TEAL)
            left_at(fac, ROWS[1])
            # TeX sets "?" as a closing symbol (no space after "="): place it where "1" will sit
            ref = left_at(MathTex(r"e^{2\pi i n m}", "=", "1", font_size=56), ROWS[1])
            fac[2].move_to(ref[2])
            fac[1].set_opacity(0)
            fac[2].set_opacity(0)
            unit = Circle(radius=R, color=DIM, stroke_width=2).move_to(WC)
            axes = work_axes(WC, R)
            one_lab = MathTex("1", font_size=34).next_to(on_circle(0), DR, buff=0.08)
            theta = ValueTracker(0)
            dot = Dot(on_circle(0), radius=0.1, color=YELLOW).set_z_index(3)
            dot.add_updater(lambda m: m.move_to(on_circle(theta.get_value() / TAU)))
            arrow = always_redraw(lambda: Arrow(WC, on_circle(theta.get_value() / TAU), buff=0,
                                                color=TEAL, stroke_width=4,
                                                max_tip_length_to_length_ratio=0.15))
            self.play(*appear(fac[0], shift=None), FlashAround(card.factor, run_time=1.2),
                      FadeIn(unit), FadeIn(axes), run_time=1.2)
            self.play(FadeIn(dot), FadeIn(arrow), *appear(one_lab, shift=None), run_time=0.8)
            arcs = [Arc(radius=0.32 + 0.16 * k, start_angle=0, angle=TAU, arc_center=WC,
                        color=TEAL, stroke_width=3) for k in range(3)]
            budget = max(1.5, c.until("room") - 0.4)
            for k, (frac, cap) in enumerate(zip((0.42, 0.32, 0.26), (2.0, 1.4, 1.0))):
                self.play(theta.animate.set_value(TAU * (k + 1)), Create(arcs[k]),
                          run_time=min(cap, frac * budget))
            dot.clear_updaters()
            arrow.clear_updaters()
            self.remove(theta)
            c.wait_until("room")
            fac[1].set_opacity(1)
            fac[2].set_opacity(1).set_color(YELLOW)
            self.play(*appear(fac[1], fac[2], shift=None, lag=0.2), run_time=0.9)
            c.wait_until("one")
            one = MathTex("1", font_size=56).move_to(fac[2]).set_color(FG)
            self.play(*swap(fac[2], one), run_time=1.0)
            fac.remove(fac[2])
            fac.add(one)
            c.wait_until("lands")
            self.play(FlashAround(dot, run_time=1.2), FlashAround(one, run_time=1.2), run_time=1.2)

        # ---------------- clip 2: one value, De Moivre, (2i)^2
        with self.say("c5.fin.2") as c:
            one_val = T("one value", size=34, color=GREEN).next_to(fac, RIGHT, buff=0.5)
            c.wait_until(own_word=one_val)
            self.play(*appear(one_val), run_time=0.9)
            c.wait_until("formula")
            form = MathTex("z_1^m", "=", "|z_1|^m", r"e^{i", r"m\theta_1", "}", font_size=48)
            form[2].set_color(GOLD)
            form[4].set_color(YELLOW)
            left_at(form, ROWS[2])
            self.play(*appear(form, shift=None), run_time=1.5)
            c.wait_until("demoivre")
            tag = T("De Moivre, Part 2", size=32, color=FG).next_to(form, RIGHT, buff=0.6)
            self.play(*appear(tag), run_time=0.9)
            c.wait_until("example")
            fill1 = frame1_dot(f1)
            self.play(*appear(fill1.label), GrowFromCenter(fill1.dot), run_time=1.0)
            cap1 = filled_caption(f1, CAP1)
            self.play(*swap(f1.caption, cap1), run_time=1.0)

        # ---------------- clip 3: rational exponent, the star
        with self.say("c5.fin.3") as c:
            head2 = MathTex(r"\text{ii)}\quad", "z_2", r"= p/q", r"\text{ in lowest terms,}", r"\; q > 0",
                            font_size=40)
            head2[1].set_color(YELLOW)
            left_at(head2, ROWS[0])
            fac2 = MathTex(r"e^{2\pi i", r"(p/q)", r"n}", font_size=56).set_color(TEAL)
            left_at(fac2, ROWS[1])
            self.play(*during(disappear(form, tag, one_val, arrow, *arcs), 0, 0.45),
                      *swap(head, head2), *swap(fac, fac2), run_time=1.4)  # early: case heading
            c.wait_until("step")
            self.play(*recolor(fac2[1], YELLOW), *flash([fac2[1]]), run_time=1.2)

            c.wait_until("star")
            pq = MathTex("p/q", "=", "2/5", font_size=44)
            pq[2].set_color(GOLD)
            pq.next_to(fac2, RIGHT, buff=0.7)
            self.play(*appear(pq), run_time=0.8)
            landing = [Dot(on_circle(0), radius=0.09, color=TEAL).set_z_index(2)]
            self.add(landing[0])
            stops = [0, 0.4, 0.8, 0.2, 0.6]
            chords = []

            def jump(i, rt):
                a, b = on_circle(stops[i % 5]), on_circle(stops[(i + 1) % 5])
                ch = Line(a, b, color=TEAL, stroke_width=4)
                chords.append(ch)
                self.play(Create(ch), dot.animate.move_to(b), run_time=rt, rate_func=smooth)
                if i + 1 < 5:
                    d = Dot(b, radius=0.09, color=TEAL).set_z_index(2)
                    landing.append(d)
                    self.add(d)

            budget = max(2.0, c.until("room2") - 0.3)
            for i, frac in enumerate((0.36, 0.26, 0.2, 0.18)):
                jump(i, min((1.6, 1.1, 0.9, 0.8)[i], frac * budget))
            c.wait_until("room2")
            how = T("how many?", size=40, color=YELLOW)
            left_at(how, ROWS[2])
            self.play(*appear(how), run_time=0.9)
            c.wait_until("q")
            qv = T("q distinct values (here 5)", size=36, t2s={"q": ITALIC}, t2c={"5": GOLD})
            left_at(qv, ROWS[2])
            self.play(*swap(how, qv), run_time=1.2)
            c.wait_until("repeat")
            jump(4, 1.3)
            steps = T("5 steps = 2 full turns", size=34, color=FG)
            left_at(steps, ROWS[3])
            self.play(*appear(steps), FlashAround(landing[0], run_time=1.0), run_time=1.0)
            c.wait_until("list")
            lst = MathTex(r"n = 0, 1, \dots, q-1", font_size=44)
            left_at(lst, ROWS[2])
            self.play(*swap(qv, lst), run_time=1.2)

        # ---------------- clip 4: why lowest terms
        with self.say("c5.fin.4") as c:
            hx = head2.get_x()
            sweep_clear(self, FlashUnder(head2[3], run_time=1.2), *recolor(head2[3], YELLOW),
                        keep=[shot, fill1, cap1, head2], run_time=1.6)
            c.wait_until("twofour")
            tf = MathTex("2/4", "=", "1/2", font_size=60).move_to([hx, 1.3, 0])
            self.play(*appear(tf, shift=None), run_time=1.2)
            c.wait_until("half")
            xs = (-2.25, -0.75, 0.75, 2.25)
            slots = [RoundedRectangle(corner_radius=0.12, width=1.2, height=0.85, color=BLUE,
                                      stroke_width=2).move_to([hx + x, 0.35, 0]) for x in xs]
            vals = [MathTex(v, font_size=44, color=col).move_to(s)
                    for v, col, s in zip(("1", "-1", "1", "-1"), (GREEN, GREEN, DIM, DIM), slots)]
            self.play(*[FadeIn(s) for s in slots], *appear(vals[0], vals[1], shift=None, lag=0.3),
                      run_time=1.2)
            c.wait_until("two quarters", nth=1)
            lab4 = T("2 values, not 4", size=36).next_to(tf, RIGHT, buff=0.6)
            self.play(*appear(vals[2], vals[3], shift=None, lag=0.3), run_time=0.9)
            self.play(*appear(lab4), run_time=0.9)
            c.wait_until("not four")
            crosses = [Cross(s, stroke_color=RED, stroke_width=5, scale_factor=0.8) for s in slots[2:]]
            self.play(*[GrowFromCenter(x) for x in crosses], run_time=1.0)
            c.wait_until("cancel")
            self.play(FlashAround(tf[2], run_time=1.2), run_time=1.2)

        # ---------------- clip 5: (2i)^(1/5) is the ring of five
        with self.say("c5.fin.5") as c:
            L1 = MathTex("(", "2i", r")^{1/5}", "=", r"e^{(1/5)\ln", "2i", "}", font_size=52)
            L2 = MathTex("=", r"e^{(1/5)(\ln 2 + i(\pi/2 +", r"2\pi n", "))}", font_size=52)
            L3 = MathTex("=", "2^{1/5}", r"e^{i(\pi/10 +", r"2\pi n", "/5)}", font_size=52)
            for m in (L1[1], L1[5]):
                m.set_color(YELLOW)
            L2[2].set_color(TEAL)
            L3[1].set_color(GOLD)
            L3[3].set_color(TEAL)
            XEQ = -0.6
            L1.move_to([0, ROWS[0], 0]).shift((XEQ - L1[3].get_x()) * RIGHT)
            for L, y in ((L2, 1.15), (L3, 0.1)):
                L.move_to([0, y, 0]).shift((XEQ - L[0].get_x()) * RIGHT)
            c.wait_until("seen")
            sweep_clear(self, *appear(L1, shift=None), keep=[shot, fill1, cap1], run_time=1.4)
            c.wait_until("log")
            self.play(*appear(L2, shift=None), run_time=1.5)
            c.wait_until("result")
            self.play(*appear(L3, shift=None), run_time=1.5)

            c.wait_until("back")
            ring = ring_work()
            raxes = work_axes(RC, 1.38)
            l3_target = L3.copy().move_to([0, ROWS[0], 0]).align_to([COL, 0, 0], LEFT)
            self.play(*during(disappear(L1, L2), 0, 0.4),
                      *during([L3.animate.move_to(l3_target)], 0.4, 1),
                      *during([FadeIn(raxes), FadeIn(ring.circ), *[FadeIn(d, scale=0.5) for d in ring.dots]],
                              0.3, 1),
                      run_time=1.8)
            zl = MathTex("z^5 =", "2i", font_size=52)
            zl[1].set_color(YELLOW)
            left_at(zl, 1.15)
            self.play(*appear(zl), run_time=0.9)
            c.wait_until("same")
            same = T("same five points", size=40, color=GREEN)
            left_at(same, 0.1)
            self.play(*appear(same), run_time=0.9)
            self.wait(min(1.0, max(0.0, c.remaining - 3.0)))
            target = frame2_ring(f2)
            self.play(ReplacementTransform(ring.circ, target.circ),
                      *[ReplacementTransform(d, t) for d, t in zip(ring.dots, target.dots)],
                      FadeOut(raxes), *during(appear(frame2_label(f2), shift=None), 0.45, 1), run_time=1.5)
            cap2 = filled_caption(f2, CAP2)
            self.play(*swap(f2.caption, cap2), run_time=min(1.0, max(0.5, c.remaining - 0.1)))

        self.wait(0.2)
        # ---------------- back to the shot: work cleared, card home
        self.play(*during(disappear(L3, zl, same), 0, 0.5),
                  *during([card.animate.scale(1 / 0.72).move_to(card_c)], 0.4, 1), run_time=1.3)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)   # handover: s7 opens on handover_shot()
