"""Chapter 5, scene 5: how many values does z1^z2 have? The ladder, the split, the question. Clips c5.count.1 – c5.count.4.

Shared helpers (import with load_scene("ch5_s5_count")):
  ladder(...)          the chapter's log ladder (vertical line, GREEN principal rung, TEAL rungs,
                       brace "2πi"); options for rung labels and a line label (ch5 s1: Re w = ln 2).
  question_card(...)   the card "How many distinct numbers does e^{2πinz₂} give, as n runs through ℤ?";
                       .factor (TEAL), .z2 (its z₂ glyphs), .box, .line1, .line2.
  gallery_frames()     four small captioned Argand planes in a row along the bottom;
                       frame .box .plane .caption .origin .u, and frame.P(x, y) -> screen point.
  handover_shot()      question card (z₂ YELLOW) + the four empty frames: this scene's last frame.
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
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- shared helpers
GENERIC_RUNGS = {0: "principal value", 1: r"+\,2\pi i", 2: r"+\,4\pi i", -1: r"-\,2\pi i"}


def ladder(ns=(-1, 0, 1, 2), x=-5.2, y0=-1.7, pitch=1.1, labels=None, label_size=34,
           line_label=None, brace=True, ext=0.6):
    """The log ladder, built by ch4 s4's ladder() so the look matches exactly (GOLD dashed line,
    GREEN principal rung, TEAL rungs, a few fading TEAL dots past the end rungs, TEAL brace "2πi"
    left of the 0→1 gap); ch4's ln 2 / π/2 ticks are dropped. Rung n sits at (x, y0 + n*pitch);
    the line runs from the lowest rung − ext to the highest + ext.
    labels: None (no labels), True (generic: "principal value", "+ 2πi", "+ 4πi", "− 2πi"),
    or a dict n -> string (MathTex; n = 0 "principal value" is ch4's GREEN tag: alone it keeps ch4's
    place, with other labels it sits on its rung's row, left-aligned with them).
    line_label: MathTex string written above the line's top, e.g. r"\\mathrm{Re}\\,w=\\ln 2".
    Returns a VGroup with .line (the dashed line plus its fading dots) .rungs {n: Dot} .brace
    .brace_label .labels {n: mob} .label_group .line_label .y(n)."""
    from lib.paths import load_scene
    ch4 = load_scene("ch4_s4_ln2i")
    sx = ch4.W_SX
    sy = pitch / (2 * PI)
    origin = np.array([x - sx * ch4.LN2, y0 - sy * PI / 2, 0.0])   # rung 0 lands on (x, y0)
    lo, hi = y0 + min(ns) * pitch - ext, y0 + max(ns) * pitch + ext
    fade_step = min(0.28, ext / 2.2)
    src = ch4.ladder(origin=origin, sx=sx, sy=sy, ns=tuple(ns), n_fade=2, fade_step=fade_step,
                     y_lo=lo, y_hi=hi)
    g = VGroup()
    g.line = VGroup(src.line, src.fade_top, src.fade_bot)
    g.add(g.line)
    g.rungs = dict(src.dots)
    for n in ns:
        g.add(g.rungs[n])
    g.brace = g.brace_label = None
    if brace and 0 in ns and 1 in ns:
        g.brace, g.brace_label = src.brace, src.brace_label
        g.add(g.brace, g.brace_label)
    ys = {n: src.point(n)[1] for n in ns}
    g.labels = {}
    if labels is True:
        labels = GENERIC_RUNGS
    labels = {n: s for n, s in (labels or {}).items() if n in ys}
    for n, s in labels.items():
        if n == 0 and s == "principal value":
            m = src.tag
            if len(labels) > 1:
                m.move_to([x + 0.6, ys[0], 0], aligned_edge=LEFT)
        else:
            col = GREEN if n == 0 else TEAL
            plain = not any(ch in s for ch in "\\^_")
            m = T(s, size=30, color=col) if plain else MathTex(s, font_size=label_size, color=col)
            m.move_to([x + 0.6, ys[n], 0], aligned_edge=LEFT)
        g.labels[n] = m
    g.label_group = VGroup(*[g.labels[n] for n in sorted(g.labels)])
    g.line_label = None
    if line_label:
        g.line_label = MathTex(line_label, font_size=34, color=DIM).next_to(g.line, UP, buff=0.15)
    g.y = lambda n: ys[n]
    return g


def question_card(highlight=False):
    """Top-of-frame card: 'How many distinct numbers does e^{2πinz₂} give, / as n runs through ℤ?'
    factor TEAL; highlight=True paints its z₂ YELLOW (the state at the end of ch5 s5)."""
    line1 = MathTex(r"\text{How many distinct numbers does }", r"e^{2\pi i n z_2}", r"\text{ give,}",
                    font_size=40)
    line2 = MathTex(r"\text{as } n \text{ runs through } \mathbb{Z}\text{?}", font_size=40)
    line1[1].set_color(TEAL)
    txt = VGroup(line1, line2).arrange(DOWN, buff=0.28)
    box = RoundedRectangle(corner_radius=0.18, width=txt.width + 0.8, height=txt.height + 0.5,
                           color=DIM, stroke_width=2)
    card = VGroup(box, line1, line2)
    box.move_to(txt)
    card.move_to([0, 2.85, 0])
    card.box, card.line1, card.line2 = box, line1, line2
    card.factor = line1[1]
    glyphs = sorted(line1[1], key=lambda m: m.get_right()[0])   # z₂ = the two rightmost glyphs
    card.z2 = VGroup(*glyphs[-2:])
    if highlight:
        card.z2.set_color(YELLOW)
    return card


GALLERY_CAPTIONS = ("integer", "fraction p/q", "irrational", "imaginary part")


def gallery_frame(center, caption, w=2.9, h=2.1, u=0.68):
    """One small Argand plane (faint grid, axes, Re/Im, DIM unit circle, as ch2's argand_plane)
    in a DIM rounded frame, caption below."""
    c = np.array(center, dtype=float)
    f = VGroup()
    f.origin, f.u = c, u
    f.P = lambda x, y: c + u * np.array([x, y, 0.0])
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, color=DIM, stroke_width=2).move_to(c)
    xr, yr = (-1.75, 1.5), (-1.3, 0.95)
    grid = VGroup()
    for v in (-1, 1):
        grid.add(Line(f.P(v, yr[0]), f.P(v, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
        grid.add(Line(f.P(xr[0], v), f.P(xr[1], v), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(f.P(xr[0], 0), f.P(xr[1] + 0.2, 0), buff=0, stroke_width=2, color=FG,
                max_tip_length_to_length_ratio=0.08)
    yax = Arrow(f.P(0, yr[0]), f.P(0, yr[1] + 0.15), buff=0, stroke_width=2, color=FG,
                max_tip_length_to_length_ratio=0.08)
    re = T("Re", size=28).next_to(xax.get_end(), DOWN, buff=0.08).shift(0.05 * LEFT)
    im = T("Im", size=28).next_to(yax.get_end(), RIGHT, buff=0.1).shift(0.12 * DOWN)
    unit = Circle(radius=u, color=DIM, stroke_width=2).move_to(c)
    f.plane = VGroup(grid, xax, yax, re, im, unit)
    f.box = box
    f.caption = T(caption, size=30, color=FG, t2s={"p/q": ITALIC}).next_to(box, DOWN, buff=0.15)
    f.add(box, f.plane, f.caption)
    return f


def gallery_frames():
    """The four frames in a row along the bottom (centres x = −4.8, −1.6, 1.6, 4.8; y = −1.75)."""
    g = VGroup(*[gallery_frame([x, -1.75, 0], cap) for x, cap in zip((-4.8, -1.6, 1.6, 4.8), GALLERY_CAPTIONS)])
    g.frames = list(g)
    return g


def handover_shot():
    return VGroup(question_card(highlight=True), gallery_frames())


# ---------------------------------------------------------------- scene
class Count(NarratedScene):
    def construct(self):
        # ---------------- clip 1: the general case, the definition
        with self.say("c5.count.1") as c:
            head = MathTex(r"\text{General powers }", r"z_1^{\,z_2},", r"\qquad z_1,\, z_2\in\mathbb{C}",
                           font_size=50).move_to([0, 2.3, 0])
            head[1].set_color(YELLOW)
            self.play(*appear(head), run_time=1.0)  # early: heading
            c.wait_until("question")
            q = T("How many different values?", size=44, color=YELLOW).move_to([0, 1.1, 0])
            self.play(*appear(q), run_time=1.0)
            c.wait_until("def")
            defn = MathTex(r"z_1^{\,z_2}", "=", r"e^{z_2 \ln z_1}", font_size=80).move_to([0, -1.2, 0])
            self.play(*appear(defn, shift=None), run_time=1.5)

        # ---------------- clip 2: the ladder, the shorthand
        with self.say("c5.count.2") as c:
            lad = ladder(labels=True)
            self.play(*during(disappear(head, q), 0, 0.45),
                      *during([defn.animate.scale(48 / 80).move_to([1.8, 2.75, 0])], 0.3, 0.85),
                      *during([FadeIn(lad.line), *[GrowFromCenter(lad.rungs[n]) for n in lad.rungs]], 0.5, 1),
                      run_time=1.8)
            self.play(GrowFromCenter(lad.brace), *appear(lad.brace_label), run_time=0.8)  # early: recap of ch4's ladder

            c.wait_until("rungs")
            withl = MathTex(r"\text{with }", r"\ln z_1", "=", r"\ln z_1", "+", r"2\pi i n",
                            font_size=48).move_to([1.8, 0.55, 0])
            withl[5].set_color(TEAL)
            self.play(*appear(withl, shift=None), run_time=1.2)
            self.play(*appear(*[lad.labels[n] for n in (0, 1, 2, -1)], lag=0.3), run_time=1.4)

            c.wait_until("abuse")
            self.play(*flash([withl[1], withl[3]]), run_time=1.5)
            c.wait_until("principal value", nth=0)
            arr = Arrow(withl[3].get_bottom() + 0.95 * DOWN, withl[3].get_bottom() + 0.08 * DOWN,
                        buff=0, stroke_width=3, color=GREEN, max_tip_length_to_length_ratio=0.3)
            tag = T("principal value", size=30, color=GREEN).next_to(arr, DOWN, buff=0.1)
            self.play(GrowArrow(arr), *appear(tag), run_time=1.2)

            c.wait_until("theta", nth=0)
            th = MathTex(r"\theta", "=", r"\theta", "+", r"2\pi n", font_size=48)
            th[4].set_color(TEAL)
            th.move_to([withl[2].get_x(), -1.95, 0]).shift((withl[2].get_x() - th[1].get_x()) * RIGHT)
            self.play(*appear(th, shift=None), run_time=1.0)
            br_seg = Line([withl.get_right()[0] + 0.25, withl.get_top()[1], 0],
                          [withl.get_right()[0] + 0.25, th.get_bottom()[1], 0])
            br = Brace(br_seg, direction=RIGHT, buff=0.05, color=DIM)
            habit = T("same\nhabit", size=30, color=DIM, line_spacing=0.8).next_to(br, RIGHT, buff=0.12)
            self.play(GrowFromCenter(br), *appear(habit, shift=None), run_time=min(1.0, c.until(floor=0.5)))

        # ---------------- clip 3: the split
        with self.say("c5.count.3") as c:
            self.play(*disappear(withl, arr, tag, th, br, habit), run_time=0.8)
            split = MathTex(r"z_1^{\,z_2}", "=", r"e^{z_2 \ln z_1}", r"\cdot", r"e^{2\pi i n z_2}",
                            font_size=52).move_to([1.6, 2.75, 0])
            self.play(*edit(defn, split), run_time=1.6)

            c.wait_until("fixed")
            b1 = Brace(split[2], direction=DOWN, buff=0.12, color=GREEN)
            l1 = T("one fixed number", size=30, color=GREEN).next_to(b1, DOWN, buff=0.1)
            l1.align_to(split[2], RIGHT).shift(0.15 * RIGHT)
            self.play(*recolor(split[2], GREEN), GrowFromCenter(b1), run_time=1.0)
            c.wait_until(own_word=l1)
            self.play(*appear(l1), run_time=0.9)

            c.wait_until("factor")
            b2 = Brace(split[4], direction=DOWN, buff=0.12, color=TEAL)
            l2 = T("depends on n", size=30, color=TEAL, t2s={" n": ITALIC}).next_to(b2, DOWN, buff=0.1)
            l2.align_to(split[4], LEFT).shift(0.1 * LEFT)
            self.play(*recolor(split[4], TEAL), GrowFromCenter(b2), run_time=1.0)
            self.play(*appear(l2), run_time=0.9)  # early: the brief's tag for the factor; its 'n' is said in this sentence

            c.wait_until("rungs2")
            copies_tex = {-1: r"e^{-2\pi i z_2}", 0: r"e^{0} = 1", 1: r"e^{2\pi i z_2}", 2: r"e^{4\pi i z_2}"}
            arrows, copies = [], []
            for n in (-1, 0, 1, 2):
                y = lad.y(n)
                a = Arrow([-1.75, y, 0], [-1.0, y, 0], buff=0, stroke_width=2.5, color=TEAL,
                          max_tip_length_to_length_ratio=0.25)
                m = MathTex(copies_tex[n], font_size=40, color=TEAL).move_to([-0.85, y, 0], aligned_edge=LEFT)
                arrows.append(a)
                copies.append(m)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25),
                      *appear(*copies, lag=0.25, shift=None), run_time=min(2.0, c.until(floor=0.6)))

        # ---------------- clip 4: the question card and the four cases
        with self.say("c5.count.4") as c:
            ladder_side = [lad, *lad.label_group, *arrows, *copies]
            c.wait_until("how many")
            # the ladder and its factors stay while the question forms; the split steps right, between rungs
            self.play(*during(disappear(l1, l2, b1, b2), 0, 0.45),
                      *during([split.animate(path_arc=-PI / 3).move_to([3.4, -0.05, 0])], 0.4, 1), run_time=1.3)
            card = question_card()
            self.play(*fly(split[4], card.factor),
                      *during(appear(card.box, card.line1[0], card.line1[2], card.line2, shift=None), 0.5, 1),
                      run_time=1.6)
            self.play(*during(disappear(*ladder_side), 0, 0.45),
                      *during([split.animate.move_to([0, 0.35, 0])], 0.4, 1),
                      run_time=min(1.3, c.until("depends", floor=0.8)))

            c.wait_until("depends")
            self.play(*recolor(card.z2, YELLOW), FlashUnder(card.z2, color=YELLOW, buff=0.06, run_time=1.5),
                      run_time=1.5)

            c.wait_until("cases")
            self.play(*disappear(split), run_time=0.7)
            frames = gallery_frames()
            for f, cue in zip(frames, ("integers", "fractions", "irrational", "imaginary")):
                c.wait_until(cue)
                self.play(*appear(f, shift=None), run_time=0.8)
        self.wait(1.0)   # handover: s6 opens on handover_shot()
