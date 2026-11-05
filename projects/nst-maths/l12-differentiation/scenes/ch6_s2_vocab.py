"""Chapter 6, scene 2: the vocabulary of stationary points, concavity and inflection. Clips c6.vocab.1 – c6.vocab.4."""
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

_s1 = load_scene("ch6_s1_hook")
notes_figure = _s1.notes_figure

STRIP_Y = -3.0
FLIP_Y = -3.31   # flips end 0.5 above the frame edge
LABEL_SIZE = 32


def _arrow(start, end, buff=0.12):
    return Arrow(start, end, buff=buff, stroke_width=3, color=FG,
                 max_tip_length_to_length_ratio=0.35, tip_length=0.18)


def _flat_tangent(dot, half=0.75):
    c = dot.get_center()
    return Line(c + half * LEFT, c + half * RIGHT, color=GREEN, stroke_width=5).set_z_index(1)


def labelled_figure():
    """The scene's last frame, static and full size: the notes' figure with its labels and the y'' strip.
    Parts: .fig (NotesFigure: .axes .curve .dots .peak .valley .bend1 .bend2 .flat .at_x)
    .dots (= .fig.dots) .labels (VGroup lmax, lmin, inflect, rising) with
    .lmax / .lmin = VGroup(text, arrow), .inflect = VGroup(text, arrow to bend1, arrow to bend2),
    .rising = VGroup(text (2 lines), arrow); .strip = VGroup(ylab, signs, dashes, flips) with
    .strip.ylab (y''), .strip.signs (4 MathTex: - + - +), .strip.dashes (3 DashedLines through
    bend1, bend2, flat), .strip.flips (3 MathTex: -|+, +|-, -|+)."""
    lf = VGroup()
    fig = notes_figure()
    lf.fig, lf.dots = fig, fig.dots
    pk, vl, b1, b2, fl = (d.get_center() for d in fig.dots)

    t = T("local maximum", LABEL_SIZE).move_to(pk + 0.95 * UP)
    lf.lmax = VGroup(t, _arrow(t.get_bottom(), pk))
    t = T("local minimum", LABEL_SIZE).move_to(vl + 0.72 * DOWN + 0.17 * LEFT)
    lf.lmin = VGroup(t, _arrow(t.get_top(), vl, buff=0.06))
    t = T("point of inflection", LABEL_SIZE).move_to([-1.35, 1.05, 0])
    lf.inflect = VGroup(t, _arrow(t.get_bottom() + 0.9 * LEFT, b1), _arrow(t.get_bottom() + 0.9 * RIGHT, b2))
    t = T("(rising) stationary\npoint of inflection", LABEL_SIZE, line_spacing=0.8).move_to([2.45, 1.75, 0])
    lf.rising = VGroup(t, _arrow(t.get_bottom() + 0.5 * RIGHT, fl))
    lf.labels = VGroup(lf.lmax, lf.lmin, lf.inflect, lf.rising)
    lf.labels.lmax, lf.labels.lmin, lf.labels.inflect, lf.labels.rising = lf.lmax, lf.lmin, lf.inflect, lf.rising

    xs = [fig.at_x(_s1.X_MIN)[0], b1[0], b2[0], fl[0], fig.at_x(_s1.X_MAX)[0]]
    strip = VGroup()
    strip.ylab = MathTex(r"y''", font_size=48, color=FG).move_to([xs[0] - 0.75, STRIP_Y, 0])
    strip.signs = VGroup(*[
        MathTex(s, font_size=60, color=(GREEN if s == "+" else RED)).move_to([(a + b) / 2, STRIP_Y, 0])
        for s, a, b in zip("-+-+", xs[:-1], xs[1:])])
    strip.dashes = VGroup(*[
        DashedLine(p + 0.15 * DOWN, [p[0], FLIP_Y + 0.2, 0], dash_length=0.12, color=DIM, stroke_width=3)
        for p in (b1, b2, fl)])
    strip.flips = VGroup(*[
        MathTex(f, font_size=36, color=FG).move_to([p[0], FLIP_Y, 0])
        for f, p in zip((r"-\,|\,+", r"+\,|\,-", r"-\,|\,+"), (b1, b2, fl))])
    strip.add(strip.ylab, strip.signs, strip.dashes, strip.flips)
    lf.strip = strip
    lf.add(fig, lf.labels, strip)
    return lf


def _velocity_inset():
    box = RoundedRectangle(corner_radius=0.15, width=3.9, height=1.7, stroke_color=DIM, stroke_width=2,
                           fill_color=BG, fill_opacity=1).move_to([4.75, -2.75, 0])
    track = Line(box.get_left() + 0.35 * RIGHT, box.get_right() + 0.35 * LEFT, color=DIM, stroke_width=3)
    track.shift(0.25 * UP)
    dot = Dot(track.get_start(), radius=0.12, color=YELLOW)
    stop = track.get_end() + 0.45 * LEFT
    readout = MathTex(r"v = 0", font_size=44, color=GREEN).move_to([box.get_x(), box.get_y() - 0.4, 0])
    return box, track, dot, stop, readout


def _concavity_panel(x, up):
    """A cup (up=True) or cap with three GREEN tangent lines, its label and its y'' sign."""
    s = 1 if up else -1
    w, h = 1.0, 0.65

    def f(u):
        return s * h * (u / w) ** 2

    def df(u):
        return s * 2 * h * u / w ** 2
    base = np.array([x, 3.05 - (0 if up else -0.0), 0])
    arc = ParametricFunction(lambda u: base + np.array([u, f(u) - (h / 2) * s, 0]), t_range=[-w, w],
                             color=BLUE, stroke_width=5)
    tans = VGroup()
    for u in (-0.6, 0.0, 0.6):
        p = base + np.array([u, f(u) - (h / 2) * s, 0])
        d = np.array([1, df(u), 0])
        d = d / np.linalg.norm(d)
        tans.add(Line(p - 0.4 * d, p + 0.4 * d, color=GREEN, stroke_width=4))
    label = T("concave up" if up else "concave down", LABEL_SIZE).move_to([x, 2.15, 0])
    sign = MathTex(r"y'' > 0" if up else r"y'' < 0", font_size=44,
                   color=GREEN if up else RED).move_to([x, 1.55, 0])
    return arc, tans, label, sign


class VocabScene(NarratedScene):
    def construct(self):
        shot = _s1.handover_shot()
        fig = shot.fig
        self.add(fig, shot.qs, shot.question, shot.row, shot.odd, shot.even)
        lf = labelled_figure()
        pk, vl, b1, b2, fl = fig.dots

        # ---- c6.vocab.1: stationary point, flat tangents, velocity, the three
        with self.say("c6.vocab.1") as c:
            self.play(*disappear(shot.qs, shot.question, shot.row, shot.odd, shot.even),
                      run_time=min(1.0, c.until("a stationary point")))
            c.wait_until("a stationary point")
            stat = MathTex(r"\text{stationary point:}\quad \dfrac{dy}{dx} = 0", font_size=50).move_to(3.05 * UP)
            self.play(*appear(stat), run_time=min(1.2, c.until("flat")))
            c.wait_until("flat")
            tangents = [_flat_tangent(d) for d in (pk, vl, fl)]
            self.play(LaggedStart(*[GrowFromCenter(t) for t in tangents], lag_ratio=0.3),
                      run_time=min(1.6, c.until("velocity")))
            c.wait_until("velocity")
            box, track, vdot, stop, readout = _velocity_inset()
            self.play(FadeIn(box), Create(track), FadeIn(vdot, scale=0.5), run_time=1.0)
            self.play(vdot.animate.move_to(stop), rate_func=rate_functions.ease_out_cubic,
                      run_time=min(5.5, c.until("is stationary")))
            c.wait_until("is stationary")
            self.play(*appear(readout, shift=None), run_time=min(1.0, c.until("three")))
            c.wait_until("three")
            self.play(*disappear(box, track, vdot, readout),
                      *set_alpha([b1, b2], DIMMED),
                      *flash([pk, vl, fl]), run_time=min(1.5, c.until("the peak")))
            for word, d in (("the peak", pk), ("valley", vl), ("flat spot", fl)):
                c.wait_until(word)
                self.play(FlashAround(d, time_width=1.5, buff=0.12), run_time=1.0)

        # ---- c6.vocab.2: local max / min, turning points
        with self.say("c6.vocab.2") as c:
            lmax_t, lmax_a = lf.lmax
            lmin_t, lmin_a = lf.lmin
            self.play(*appear(lmax_t), run_time=min(1.0, c.until("higher")))
            c.wait_until("higher")
            level = DashedLine(pk.get_center() + 0.15 * RIGHT, [6.7, pk.get_y(), 0], dash_length=0.15,
                               color=YELLOW, stroke_width=3)
            self.play(Create(level), run_time=min(1.6, c.until("min")), rate_func=linear)
            climb = fig.axes.plot(_s1.curve_y, x_range=[1.9, _s1.X_MAX, 0.01], color=YELLOW, stroke_width=9)
            self.play(VShowPassingFlash(climb, time_width=0.6), run_time=min(1.5, c.until("min")))
            c.wait_until("min")
            self.play(*appear(lmin_t, shift=0.25 * UP), run_time=min(1.0, c.until("turning")))
            c.wait_until("turning")
            brace = span_brace([pk.get_x(), 0, 0], [vl.get_x(), 0, 0]).move_to(
                [(pk.get_x() + vl.get_x()) / 2, -2.6, 0])
            brace.set_color(YELLOW)
            turning = T("turning points", LABEL_SIZE, YELLOW).next_to(brace, DOWN, buff=0.15)
            self.play(*disappear(level), GrowFromCenter(brace), run_time=1.0)
            self.play(*appear(turning), run_time=min(1.0, c.until()))

        # ---- c6.vocab.3: concavity, then the y'' sign strip
        with self.say("c6.vocab.3") as c:
            self.play(*disappear(stat, *tangents), run_time=min(1.2, c.until("like a cup")))
            c.wait_until("like a cup")
            up_arc, up_tans, up_lab, up_sign = _concavity_panel(-1.0, True)
            self.play(*during(disappear(brace, turning), 0, 0.35),
                      *during([Create(up_arc)], 0.3, 0.8),
                      *during([GrowFromCenter(t) for t in up_tans], 0.5, 1.0),
                      run_time=min(2.0, c.until("concave up")))
            c.wait_until("concave up")
            self.play(*appear(up_lab), run_time=min(1.0, c.until("upsign")))
            c.wait_until("upsign")
            self.play(*appear(up_sign, shift=None), run_time=min(1.0, c.until("down")))
            c.wait_until("like a cap")
            dn_arc, dn_tans, dn_lab, dn_sign = _concavity_panel(2.6, False)
            self.play(Create(dn_arc), LaggedStart(*[GrowFromCenter(t) for t in dn_tans], lag_ratio=0.3),
                      run_time=min(1.5, c.until("concave down")))
            c.wait_until("concave down")
            self.play(*appear(dn_lab), run_time=min(1.0, c.until("downsign")))
            c.wait_until("downsign")
            self.play(*appear(dn_sign, shift=None), run_time=min(1.0, c.until("strip")))
            c.wait_until("strip")
            st = lf.strip
            rt = min(3.0, c.until())
            self.play(*during(disappear(up_arc, up_tans, up_lab, up_sign, dn_arc, dn_tans, dn_lab, dn_sign), 0, 0.3),
                      *during(appear(st.ylab, shift=None), 0.25, 0.45),
                      *during([Create(d) for d in st.dashes], 0.25, 0.6),
                      *during(appear(*st.signs, shift=None, lag=0.4), 0.4, 1.0),
                      run_time=rt)

        # ---- c6.vocab.4: inflection, the notes' labels, the spelling note
        with self.say("c6.vocab.4", gap=2.5) as c:
            self.play(*set_alpha([b1, b2], 1), *flash([b1, b2, fl]), run_time=min(1.5, c.until("sign")))
            c.wait_until("sign")
            self.play(*appear(*st.flips, shift=None, lag=0.5), run_time=min(2.0, c.until("labels")))
            c.wait_until("lmax")
            self.play(GrowArrow(lmax_a), FlashAround(lmax_t, time_width=1.5), run_time=min(1.0, c.until("lmin")))
            c.wait_until("lmin")
            self.play(GrowArrow(lmin_a), FlashAround(lmin_t, time_width=1.5), run_time=min(1.0, c.until("two")))
            c.wait_until("two")
            inf_t, inf_a1, inf_a2 = lf.inflect
            self.play(*appear(inf_t), GrowArrow(inf_a1), GrowArrow(inf_a2), run_time=min(1.2, c.until("rising")))
            c.wait_until("rising")
            ris_t, ris_a = lf.rising
            self.play(*appear(ris_t), GrowArrow(ris_a), run_time=min(1.2, c.until("spell")))
            c.wait_until("spell")
            note = T("The spellings ‘inflection’ and ‘inflexion’ are both acceptable\n"
                     "and are used interchangeably.", 28, DIM, line_spacing=0.8)
            nbox = RoundedRectangle(corner_radius=0.12, width=note.width + 0.6, height=note.height + 0.4,
                                    stroke_width=0, fill_color="#262A31", fill_opacity=1)
            card = VGroup(nbox, note).move_to(3.05 * UP)
            note.move_to(nbox)
            self.play(*appear(card, shift=None), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
