"""Chapter 4, scene 2: higher derivatives and their notation. Clips c4.higher.1 – c4.higher.4.

Opens on an empty frame: (112) d^n y/dx^n, its recursive definition and the linear tag; the
definition shrinks to a strip over the x^3 derivative chain (ch1's card, built out link by link);
the notes' grey Note box (operator power vs power of the derivative) with the 6x != 9x^4 contrast;
then everything shrinks left, dimmed, beside the f^(n) notation card. Ends on an empty frame.

Exports (all built at ORIGIN, scale 1 = the size used in this scene's own shots unless noted)
- chain_card() -> VGroup(frame, expr): expr = MathTex("x^3", "\\to", "3x^2", "\\to", "6x", "\\to",
  "6", "\\to", "0", "\\to", "0,\\,0,\\,0,\\,\\dots", font_size=44); x^3 BLUE, 3x^2 6x 6 0 GREEN,
  arrows FG, the tail (last two parts) DIM. frame: cube_card()'s RoundedRectangle style (corner 0.15,
  YELLOW stroke 2.5, no fill, 0.3 padding). Attributes .frame .expr .terms (5) .arrows (4) .tail.
  chain_frame(card, k) -> the frame round terms 0..k (k = 5: with the tail), left edge kept.
- notation_card() -> VGroup(frame, main, power, zero): main = f^{(n)} = d^n f/dx^n (MathTex 56,
  f BLUE, (n) YELLOW); power = VGroup(f^n DIM MathTex 56, "a power" T 30 DIM) to its right;
  zero = f^{(0)} = f below main (f BLUE, (0) YELLOW); frame DIM stroke 2, corner 0.2, 0.4 padding.
- power_contrast(with_label=False) -> VGroup(six, neq, square[, label]): MathTex 56 parts
  six "6x" GREEN, neq "\\neq" RED, square "(3x^2)^2 = 9x^4" RED; label "second derivative" T 30
  GREEN under six when with_label.
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


# ---------------------------------------------------------------- exported helpers
def _card_style():
    try:
        f = load_scene("ch1_s3_cube").cube_card().frame
        return f.get_stroke_color(), f.get_stroke_width()
    except Exception:
        return YELLOW, 2.5


def chain_frame(card, k=5):
    """The card's frame drawn round terms 0..k only (k=5 includes the tail); left edge kept."""
    e = card.expr
    parts = VGroup(*e[: 2 * k + 1]) if k < 5 else e
    pad = card.frame.height - e.height
    col, w = card.frame.get_stroke_color(), card.frame.get_stroke_width()
    r = RoundedRectangle(corner_radius=0.15 * pad / 0.6, width=parts.width + pad, height=card.frame.height)
    r.set_stroke(col, w).set_fill(opacity=0)
    r.move_to(card.frame).align_to(card.frame, LEFT)
    return r


def chain_card():
    expr = MathTex("x^3", r"\to", "3x^2", r"\to", "6x", r"\to", "6", r"\to", "0",
                   r"\to", r"0,\,0,\,0,\,\dots", font_size=44, color=FG)
    expr[0].set_color(BLUE)
    for i in (2, 4, 6, 8):
        expr[i].set_color(GREEN)
    expr[9].set_color(DIM)
    expr[10].set_color(DIM)
    col, w = _card_style()
    frame = RoundedRectangle(corner_radius=0.15, width=expr.width + 0.6, height=expr.height + 0.6)
    frame.set_stroke(col, w).set_fill(opacity=0).move_to(expr)
    card = VGroup(frame, expr).move_to(ORIGIN)
    card.frame, card.expr = frame, expr
    card.terms = [expr[i] for i in (0, 2, 4, 6, 8)]
    card.arrows = [expr[i] for i in (1, 3, 5, 7)]
    card.tail = VGroup(expr[9], expr[10])
    return card


def notation_card():
    main = MathTex("f", "^{(n)}", "=", r"\frac{d^n f}{dx^n}", font_size=56, color=FG)
    main[0].set_color(BLUE)
    main[1].set_color(YELLOW)
    frac = main[3]
    num = [g for g in frac if g.get_y() > frac.get_y() + 0.1]
    max(num, key=lambda g: g.get_x()).set_color(BLUE)          # the f in d^n f
    pw = MathTex("f^n", font_size=56, color=DIM)
    pw_tag = T("a power", 30, DIM)
    power = VGroup(pw, pw_tag)
    pw.next_to(main, RIGHT, buff=1.1).match_y(main[0])
    pw_tag.next_to(pw, DOWN, buff=0.25)
    zero = MathTex("f", "^{(0)}", "=", "f", font_size=56, color=FG)
    zero[0].set_color(BLUE)
    zero[1].set_color(YELLOW)
    zero[3].set_color(BLUE)
    zero.next_to(main, DOWN, buff=0.7).align_to(main, LEFT)
    body = VGroup(main, power, zero)
    frame = RoundedRectangle(corner_radius=0.2, width=body.width + 0.8, height=body.height + 0.8)
    frame.set_stroke(DIM, 2).set_fill(opacity=0).move_to(body)
    card = VGroup(frame, main, power, zero).move_to(ORIGIN)
    card.frame, card.main, card.power, card.zero = frame, main, power, zero
    return card


def power_contrast(with_label=False):
    parts = [MathTex("6x", font_size=56, color=GREEN), MathTex(r"\neq", font_size=56, color=RED),
             MathTex("(3x^2)^2 = 9x^4", font_size=56, color=RED)]
    row = VGroup(*parts).arrange(RIGHT, buff=0.3)
    for p in parts[1:]:
        p.align_to(parts[0], DOWN)
    parts[1].match_y(parts[0])
    g = VGroup(*parts)
    g.six, g.neq, g.square = parts
    if with_label:
        lab = T("second derivative", 30, GREEN).next_to(row, DOWN, buff=0.35).align_to(row, LEFT)
        g.add(lab)
        g.label = lab
    g.move_to(ORIGIN)
    return g


# ---------------------------------------------------------------- scene-only pieces
def note_box():
    head = T("Note: In general", 32, FG, t2w={"Note:": BOLD})
    eq = MathTex(r"\frac{d^n y}{dx^n}", r"\equiv", r"\left(\frac{d}{dx}\right)^n", "y", r"\neq",
                 r"\left(\frac{dy}{dx}\right)^n", font_size=54, color=FG)
    eq.next_to(head, DOWN, buff=0.4).align_to(head, LEFT)
    body = VGroup(head, eq)
    box = RoundedRectangle(corner_radius=0.15, width=body.width + 0.9, height=body.height + 0.7)
    box.set_stroke(DIM, 2).set_fill(DIM, 0.18).move_to(body)
    box.set_z_index(-1)
    g = VGroup(box, head, eq)
    g.box, g.head, g.eq = box, head, eq
    return g


def shrink_dim(m, s, about, shift, op):
    t = m.copy()
    t.scale(s, about_point=about).shift(shift)
    for sm in t.get_family():
        sm.set_fill(opacity=sm.get_fill_opacity() * op, family=False)
        sm.set_stroke(opacity=sm.get_stroke_opacity() * op, family=False)
    return Transform(m, t)


class HigherDerivatives(NarratedScene):
    def construct(self):
        # ---------------- c4.higher.1: the nth derivative
        with self.say("c4.higher.1") as c:
            eq1 = MathTex(r"\frac{d^n y}{dx^n}", font_size=80, color=FG).move_to(UP * 0.7)
            tag = T("(112)", 34, DIM).next_to(eq1, LEFT, buff=0.6)
            label = T("the nth derivative", 34, YELLOW, t2s={"n": ITALIC}).next_to(eq1, DOWN, buff=0.5)
            self.play(*appear(eq1, tag, lag=0.3), run_time=1.2)  # early: equation number, shown with its formula
            c.wait_until(own_word=label)
            self.play(*appear(label), run_time=1.0)

            rec = MathTex(r"\frac{d^n y}{dx^n}", r"\equiv", r"\frac{d}{dx}\left(\frac{d^{n-1} y}{dx^{n-1}}\right)",
                          font_size=60, color=FG)
            rec[2].set_color(YELLOW)
            g1 = VGroup(tag, eq1, label)
            tgt = g1.copy()
            row = VGroup(tgt, rec).arrange(RIGHT, buff=1.1).move_to(UP * 0.7)
            rec.match_y(tgt[1])
            c.wait_until("recursive")
            self.play(*during([g1.animate.move_to(tgt)], 0, 0.6), *during(appear(rec), 0.45, 1),
                      run_time=min(2.2, c.until("trivial")))
            lin = T("linear: sums split, constants come out", 32, DIM, t2c={"linear:": YELLOW})
            lin.next_to(rec, DOWN, buff=0.7).set_y(label.get_y() - 0.75)
            c.wait_until("linear")
            self.play(*appear(lin), run_time=1.0)

        # ---------------- c4.higher.2: x^3's chain
        with self.say("c4.higher.2") as c:
            card = chain_card()
            stages = [chain_frame(card, k) for k in range(6)]
            whole = VGroup(card, *stages)
            whole.scale(min(10.5 / card.width, 1.6)).move_to(DOWN * 0.6)
            offs = [-st.get_x() for st in stages]          # shift that centres stage k
            e = card.expr
            for i, part in enumerate(e):                  # each part placed for the stage it enters on
                part.shift(offs[min((i + 1) // 2, 5)] * RIGHT)
            stages = [st.shift(offs[k] * RIGHT) for k, st in enumerate(stages)]
            card.frame.become(stages[0])
            strip_y = 3.0
            self.play(*during(disappear(tag, eq1, label, lin), 0, 0.45),
                      *during([rec.animate.scale(0.62).move_to(UP * strip_y)], 0.2, 0.8),
                      *during([FadeIn(card.frame), FadeIn(e[0], shift=0.25 * DOWN)], 0.5, 1),
                      run_time=1.8)
            c.wait_until("three ex squared")
            for k, cue, rt in ((1, "three ex squared", 1.5), (2, "second", 1.5), (3, "third", 1.2), (4, "zero", 1.2), (5, "rest", 1.2)):
                if cue:
                    c.wait_until(cue)
                d = (offs[k] - offs[k - 1]) * RIGHT
                shown = list(e[: 2 * k - 1]) if k < 5 else list(e[:9])
                new = [e[2 * k - 1], e[2 * k]] if k < 5 else [e[9], e[10]]
                self.play(*during([Transform(card.frame, stages[k])] + [p.animate.shift(d) for p in shown], 0, 0.6),
                          *during(appear(*new, lag=0.3), 0.4, 1), run_time=rt)
            settle(self, card)

        # ---------------- c4.higher.3: the Note box and 6x vs 9x^4
        with self.say("c4.higher.3") as c:
            note = note_box()
            note.move_to(DOWN * 1.75)
            card_tgt = card.copy().scale(7.2 / card.width).move_to(UP * 2.75)
            self.play(*during(disappear(rec), 0, 0.45),
                      *during([Transform(card, card_tgt)], 0.2, 0.8),
                      *during(appear(note.box, note.head, note.eq, lag=0.2), 0.5, 1),
                      run_time=2.0)
            ops = note.eq[2]
            pw = note.eq[5]
            c.wait_until("apply")
            self.play(ops.animate.set_color(GREEN), FlashAround(ops, color=GREEN, time_width=1.5), run_time=1.6)
            c.wait_until("power")
            self.play(pw.animate.set_color(RED), FlashAround(pw, color=RED, time_width=1.5), run_time=1.6)

            pc = power_contrast(with_label=True).move_to(UP * 0.75)
            c.wait_until("six")
            self.play(*fly(card.terms[2], pc.six), run_time=1.5)
            c.wait_until(own_word=pc.label)
            self.play(*appear(pc.label), run_time=1.0)
            c.wait_until("square")
            self.play(*fly(card.terms[1], pc.square, arc=PI / 2), *during(appear(pc.neq), 0.55, 1), run_time=1.6)

        # ---------------- c4.higher.4: f^(n)
        with self.say("c4.higher.4") as c:
            nc = notation_card()
            nc.scale(1.2).move_to(RIGHT * 3.4 + DOWN * 0.1)
            old = [m for m in self.mobjects if isinstance(m, VMobject) and m.has_points() or (isinstance(m, VMobject) and len(m.submobjects))]
            fam = [set(id(x) for x in m.get_family()[1:]) for m in old]
            old = [m for m in old if not any(id(m) in f for f in fam)]   # each piece moved once
            about = VGroup(*old).get_center()
            s = 0.55
            shift = np.array([-3.9, -0.1, 0]) - about
            self.play(*during([shrink_dim(m, s, about, shift, 0.45) for m in old], 0, 0.6),
                      *during(appear(nc.frame, nc.main, lag=0.2), 0.55, 1), run_time=2.0)
            c.wait_until("powernote")
            self.play(*appear(*nc.power, lag=0.3), run_time=1.2)
            c.wait_until("zero")
            self.play(*appear(nc.zero), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
