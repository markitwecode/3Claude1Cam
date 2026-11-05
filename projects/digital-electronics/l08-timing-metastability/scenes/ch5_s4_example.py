"""Chapter 5, scene 4: the slide's worked example, set up. Clips c5.example.1 – c5.example.4.

Shots: p. 114's card on the left (tau, T_0, t_su GOLD, N), a small time axis under it with a BLUE
change tick every 5 s -> YELLOW question + "T_c = ?" on the right, a GOLD year-in-seconds sum,
"1 year ~ 31.5 x 10^6 s" -> s3's mtbf_formula() on the right; MTBF, t_su, tau, N T_0 are replaced
one by one by values flying in from the card (mtbf_example()) -> both T_c flash, YELLOW rings
outside / inside the exponential -> RED "no closed form solution", GREEN "trial and error" -> the
equation alone moves compact to the top (s5 opens from it).
"""
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
from lib.style import *  # noqa: E402,F403


# =============================================================================================
# mtbf_formula() / mtbf_example(): MTBF = T_c e^((T_c - t_su)/tau) / (N T_0), and the same with
# the slide's values substituted (p. 114). Coloured like ch4_s6's pfail_formula(): T_c YELLOW,
# t_su GOLD. Built from parts so one state can turn into the next part by part:
# F.parts[name] (lhs, eq, n0..n6, bar, dN, dT), F.tex[name]; F.tc_out / F.tc_in = the two T_c.
# The fraction bar is a Line, so its width follows the wider of numerator and denominator.
# =============================================================================================
MT_SIZE = 50
MT_CENTER = np.array([1.6, 0.0, 0.0])
Q_X = 2.75   # c2's question column (card full size)

SYM = dict(lhs=r"\mathrm{MTBF}", x=r"t_{su}", y=r"\tau}", den=[("dN", r"N\,"), ("dT", r"T_0")])
VAL = dict(lhs=r"31.5\times10^{6}", x=r"500\times10^{-12}", y=r"(200\times10^{-12})}",
           den=[("dN", r"(0.2)\,"), ("dT", r"150\times10^{-12}")])


def mtbf_state(lhs, x, y, dparts, size=MT_SIZE, center=MT_CENTER):
    """One state of the equation; each argument is a tex string (SYM / VAL entries)."""
    num_tex = [r"T_c", r"\,e^{(", r"T_c", r"-", x, r")/", y]
    num = MathTex(*num_tex, font_size=size)
    num[0].set_color(YELLOW)
    num[2].set_color(YELLOW)
    if x == SYM["x"] or x == VAL["x"]:
        num[4].set_color(GOLD)
    den = MathTex(*[t for _, t in dparts], font_size=size)
    L = MathTex(lhs, font_size=size)
    if lhs == VAL["lhs"]:
        L.set_color(GOLD)
    eq = MathTex("=", font_size=size)
    w = max(num.width, den.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(FG, 3.5)
    num.next_to(bar, UP, buff=0.16)
    den.next_to(bar, DOWN, buff=0.18)
    eq.next_to(bar, LEFT, buff=0.3)
    eq.set_y(bar.get_y())
    L.next_to(eq, LEFT, buff=0.3)
    L.shift((bar.get_y() - L[0][0].get_y()) * UP)
    F = VGroup(L, eq, num, bar, den)
    F.move_to(center)
    F.parts = {"lhs": L, "eq": eq, "bar": bar}
    F.tex = {"lhs": lhs, "eq": "=", "bar": "bar"}
    for i, (name, t) in enumerate(dparts):
        F.parts[name] = den[i]
        F.tex[name] = t
    for i, t in enumerate(num_tex):
        F.parts[f"n{i}"] = num[i]
        F.tex[f"n{i}"] = t
    F.tc_out, F.tc_in = num[0], num[2]
    F.num, F.den, F.lhs, F.bar = num, den, L, bar
    return F


def mtbf_formula(size=MT_SIZE, center=MT_CENTER):
    return mtbf_state(SYM["lhs"], SYM["x"], SYM["y"], SYM["den"], size, center)


def mtbf_example(size=MT_SIZE, center=MT_CENTER):
    return mtbf_state(VAL["lhs"], VAL["x"], VAL["y"], VAL["den"], size, center)


def tc_ring(glyph, pad=0.2, width=4):
    """The YELLOW ring round one T_c (pad 0.12, width 3 for the one in the exponent)."""
    return Ellipse(width=glyph.width + pad, height=glyph.height + 0.8 * pad).move_to(glyph).set_stroke(YELLOW, width)


# =============================================================================================
# example_card(): p. 114's characteristics; mini_axis(): s2's time axis, small (grey axis,
# BLUE change ticks every `every` s)
# =============================================================================================
CARD_W, CARD_H = 5.0, 5.6
CARD_CENTER = np.array([-4.1, 0.9, 0.0])


def card_row(sym, val, color=FG, size=46):
    """'sym = val' as VGroup(MathTex 'sym =', MathTex val), so [1] is a whole text (a fly source)."""
    full = MathTex(sym, "=", val, font_size=size)
    a = MathTex(sym + "=", font_size=size, color=color).move_to(VGroup(full[0], full[1]))
    b = MathTex(val, font_size=size, color=color).move_to(full[2])
    r = VGroup(a, b)
    r.eq_pt = full[1].get_center()
    return r


def example_card():
    box = RoundedRectangle(corner_radius=0.2, width=CARD_W, height=CARD_H).set_stroke(DIM, 2)
    box.move_to(CARD_CENTER)
    title = T("Metastability - Example", 32).move_to(box.get_top() + 0.45 * DOWN)
    sub = T("flip-flop characteristics", 30, color=DIM).next_to(title, DOWN, buff=0.4)
    tau = card_row(r"\tau", r"200\,\mathrm{ps}")
    t0 = card_row(r"T_0", r"150\,\mathrm{ps}")
    tsu = card_row(r"t_{su}", r"500\,\mathrm{ps}", GOLD)
    n = card_row(r"N", r"0.2")
    rows = VGroup(tau, t0, tsu, n)
    for i, r in enumerate(rows):
        r.shift(sub.get_bottom() + (0.75 + 0.72 * i) * DOWN - r.eq_pt)
    note = T("changes per second,\non average", 28).next_to(n, DOWN, buff=0.22)
    note.set_x(box.get_x())
    C = VGroup(box, title, sub, tau, t0, tsu, n, note)
    C.box, C.title, C.sub, C.tau, C.t0, C.tsu, C.n, C.note = box, title, sub, tau, t0, tsu, n, note
    return C


def mini_axis(x0=-6.45, length=4.7, y=-2.45, seconds=25, every=5):
    axis = Line([x0, y, 0], [x0 + length, y, 0]).set_stroke(DIM, 3)
    k = length / seconds
    ticks = VGroup(*[Line([x0 + k * s, y - 0.17, 0], [x0 + k * s, y + 0.17, 0]).set_stroke(BLUE, 5)
                     for s in range(every, seconds + 1, every)])
    labels = VGroup(*[T(f"{s} s" if s else "0", 28, color=DIM).move_to([x0 + k * s, y - 0.42, 0])
                      for s in range(0, seconds + 1, every)])
    A = VGroup(axis, ticks, labels)
    A.axis, A.ticks, A.labels = axis, ticks, labels
    return A


# =============================================================================================


def substitute(scene, old, new, sources, run_time, arc=None):
    """old (on screen) becomes new part by part: shared parts slide, changed parts leave, and each
    new part flies in from sources[name] (or fades in)."""
    anims, leaving, arriving = [], [], []
    for name, part in old.parts.items():
        tgt = new.parts.get(name)
        if tgt is None:
            leaving.append(part)
        elif name == "bar":
            anims.append(Transform(part, tgt.copy()))
        elif old.tex[name] == new.tex[name]:
            anims.append(part.animate.move_to(tgt))
        else:
            leaving.append(part)
    arriving = [n for n in new.parts if old.tex.get(n) != new.tex[n]]
    fl, fades = [], []
    for name in arriving:
        if name in sources:
            f = fly(sources[name], new.parts[name], arc=(arc or {}).get(name))
            if name in ("dN", "dT", "n4", "n6"):   # card rows sit close: leave them quickly: leave it quickly (else the copy doubles it)
                for an in f:
                    an.rate_func = rush_from
            fl += f
        else:
            fades += appear(new.parts[name], shift=None)
    out = during(disappear(*leaving), 0, 0.4) if leaving else []
    scene.play(*out, *during(anims, 0.15, 0.75), *during(fl, 0.0, 0.95), *during(fades, 0.55, 1.0),
               run_time=run_time)
    scene.remove(*old.get_family())
    scene.remove(*new.get_family())
    scene.add(new)


class Example(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- c5.example.1: the card
        with self.say("c5.example.1") as c:
            C = example_card()
            self.play(FadeIn(C.box), *appear(C.title), run_time=min(1.2, c.until("chars")))  # early: card title
            c.wait_until("chars", own_word=C.sub)
            self.play(*appear(C.sub), run_time=1.0)
            for row, cue in ((C.tau, "tau"), (C.t0, "tnought"), (C.tsu, "tsu")):
                c.wait_until(cue)
                self.play(*appear(row), run_time=1.0)
            c.wait_until("rate")
            A = mini_axis()
            self.play(*appear(C.n, C.note, lag=0.4), run_time=1.4)
            self.play(Create(A.axis), *appear(A.labels, shift=None), run_time=1.0)
            self.play(LaggedStart(*[GrowFromCenter(t) for t in A.ticks], lag_ratio=0.35), run_time=1.5)
            c.wait_until("about once")
            cap = T("about once every 5 s", 30, color=BLUE).move_to([A.axis.get_center()[0], -3.42, 0])
            self.play(*appear(cap), run_time=1.0)

        # ---------------------------------------------------------------- c5.example.2: the question
        with self.say("c5.example.2") as c:
            q = T("How long must the clock period be\nfor the MTBF to exceed 1 year?", 34, color=YELLOW)
            q.move_to([Q_X, 2.95, 0])
            tc_q = MathTex("T_c", "=", "?", font_size=60)
            tc_q[0].set_color(YELLOW)
            tc_q.next_to(q, DOWN, buff=0.55)
            self.play(*appear(q), run_time=1.2)
            c.wait_until("clock period")
            self.play(*appear(tc_q), run_time=1.0)
            c.wait_until("year")
            ysum = MathTex(r"365", r"\times 24", r"\times 3600", r"= 31{,}536{,}000\ \mathrm{s}",
                           font_size=46, color=GOLD)
            ysum.move_to([Q_X, -0.4, 0])
            c.wait_until("three hundred")
            self.play(*appear(ysum[0]), run_time=1.0)
            c.wait_until("times twentyfour")
            self.play(*appear(ysum[1]), run_time=1.0)
            c.wait_until("three thousand")
            self.play(*appear(ysum[2]), run_time=1.0)
            self.play(*appear(ysum[3], shift=None), run_time=1.0)
            settle(self, ysum)
            c.wait_until("about")
            about = MathTex(r"1\ \text{year}", r"\approx", r"31.5\times10^{6}", r"\ \mathrm{s}", font_size=50)
            about[2].set_color(GOLD)
            about.next_to(ysum, DOWN, buff=0.6)
            self.play(*fly(ysum[3], about), run_time=1.5)

        # ---------------------------------------------------------------- c5.example.3: substitute
        with self.say("c5.example.3") as c:
            F0 = mtbf_formula()
            rows = [C.tau, C.tsu, C.t0, C.n]   # compact column: the exponent pair on top, the denominator pair below
            moves, swapped = [], []   # tau and N slide; T_0 and t_su trade places (fade out, fade in)
            for i, r in enumerate(rows):
                t = r.copy().scale(0.8)
                t.shift([-5.6, 2.6 - 0.75 * i, 0] - t[0][0][-1].get_center())
                if r in (C.t0, C.tsu):
                    swapped.append((r, t))
                else:
                    r.target = t
                    moves.append(MoveToTarget(r))
            self.play(*during(disappear(q, tc_q, ysum, A, cap, C.box, C.title, C.sub, C.note,
                                        *[o for o, _ in swapped]), 0, 0.45),
                      *during([about.animate.move_to([MT_CENTER[0] + 0.5, 3.1, 0]), *moves], 0.3, 0.8),
                      *during(appear(*[t for _, t in swapped], shift=None), 0.5, 0.9),
                      *during(appear(F0, shift=None), 0.55, 1.0),
                      run_time=min(1.6, c.until("left")))
            C.tsu, C.t0 = swapped[0][1], swapped[1][1]
            rows = [C.tau, C.tsu, C.t0, C.n]
            c.wait_until("our target")
            F1 = mtbf_state(VAL["lhs"], SYM["x"], SYM["y"], SYM["den"])
            substitute(self, F0, F1, {"lhs": about[2]}, arc={"lhs": PI / 4}, run_time=min(2.0, c.until("right")))
            c.wait_until("the setup time")
            F2 = mtbf_state(VAL["lhs"], VAL["x"], VAL["y"], SYM["den"])
            substitute(self, F1, F2, {"n4": C.tsu[1], "n6": C.tau[1]}, arc={"n4": -PI / 4, "n6": -PI / 4}, run_time=min(2.2, c.until("below")))
            c.wait_until("is zero point two")
            F3 = mtbf_example()
            substitute(self, F2, F3, {"dN": C.n[1], "dT": C.t0[1]}, arc={"dN": PI / 2, "dT": PI / 4}, run_time=min(2.2, c.until("unknown")))
            c.wait_until("unknown")
            self.play(*flash([F3.tc_out, F3.tc_in]), run_time=1.5)

        # ---------------------------------------------------------------- c5.example.4: twice
        with self.say("c5.example.4") as c:
            self.play(*set_alpha([*rows, about], DIMMED), run_time=1.0)
            c.wait_until("outside")
            r_out = tc_ring(F3.tc_out)
            self.play(GrowFromCenter(r_out), run_time=1.0)
            c.wait_until("inside")
            r_in = tc_ring(F3.tc_in, pad=0.12, width=3)
            self.play(GrowFromCenter(r_in), run_time=1.0)
            c.wait_until("noclosed")
            nc = T("This equation has no closed form solution", 34, color=RED)
            tag = T("trial and error", 34, color=GREEN)
            tbox = RoundedRectangle(corner_radius=0.15, width=tag.width + 0.5, height=tag.height + 0.4)
            tbox.set_stroke(GREEN, 2.5)
            row = VGroup(nc, VGroup(tbox, tag)).arrange(RIGHT, buff=0.55).move_to([0, -2.95, 0])
            tag.move_to(tbox)
            self.play(*appear(nc), run_time=1.2)
            c.wait_until("guess")
            self.play(FadeIn(tbox), *appear(tag), run_time=1.0)  # early: answers "what the slide does", read with it

        self.wait(1.6)
        # the equation alone, compact across the top: ch5_s5 opens from here
        self.play(*during(disappear(*rows, about, nc, tbox, tag, r_out, r_in), 0, 0.5),
                  *during([F3.animate.scale(0.8).move_to([0, 2.75, 0])], 0.35, 1.0), run_time=1.8)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
