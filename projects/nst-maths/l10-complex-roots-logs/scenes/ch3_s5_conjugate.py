"""Chapter 3, scene 5: Example 30, make the denominator real with the conjugate. Clips c3.conj.1 – c3.conj.5."""
# style: 2
# handover: next
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

S1 = load_scene("ch3_s1_hook")
S4 = load_scene("ch3_s4_geometric")
TH = load_scene("ch2_s2_theorem")

HS = 52                 # hero size
Y_H = 0.2               # hero row
RS = 44                 # working rows
Y_R1 = -1.55            # first working row (substitutions, bottom / top expansion)
Y_R2 = -2.5             # second working row
Y_R3 = -3.3             # small third row ((77) copy, modulus)
EQX = -1.4              # x of the aligned '=' in the bottom expansion

EI, EMI, EIN, EIN1 = r"e^{i\theta}", r"e^{-i\theta}", r"e^{iN\theta}", r"e^{i(N-1)\theta}"


# ---------------------------------------------------------------- small builders
def mt(parts, size=RS):
    """MathTex from (tex, colour) pairs; one submobject per pair."""
    m = MathTex(*[p for p, _ in parts], font_size=size)
    for sub, (_, col) in zip(m, parts):
        sub.set_color(col)
    return m


def pieces(groups, size=RS):
    """One MathTex per group of (tex, colour) parts, each where a single MathTex of all the parts puts it."""
    flat = [p for g in groups for p in g]
    ref = mt(flat, size)
    out, k = [], 0
    for g in groups:
        m = mt(g, size)
        for sub, r in zip(m, ref[k:k + len(g)]):
            sub.move_to(r)
        out.append(m)
        k += len(g)
    return VGroup(*out)


def frac(top, bot, gap=0.16):
    w = max(top.width, bot.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3.5, color=FG)
    top.next_to(bar, UP, buff=gap)
    bot.next_to(bar, DOWN, buff=gap)
    g = VGroup(top, bar, bot)
    g.top, g.bar, g.bot = top, bar, bot
    return g


def one_minus(e, col, size=HS, paren=False):
    if paren:
        return mt([("(1-", FG), (e, col), (")", FG)], size)
    return mt([("1-", FG), (e, col)], size)


def hero(body, size=HS, y=Y_H):
    """S_N = Re[ body ], body a VGroup whose `.bar` (or first fraction's bar) sets the maths axis."""
    S = MathTex("S_N", font_size=size)
    eq = MathTex("=", font_size=size)
    Re = MathTex(r"\mathrm{Re}", font_size=size, color=BLUE)
    lb = MathTex("[", font_size=size).stretch_to_fit_height(body.height + 0.3)
    rb = MathTex("]", font_size=size).stretch_to_fit_height(body.height + 0.3)
    axis = body.axis_y if hasattr(body, "axis_y") else body.get_center()[1]
    x = 0.0
    for m, buff in ((S, 0.0), (eq, 0.2), (Re, 0.2), (lb, 0.1), (body, 0.12), (rb, 0.12)):
        m.shift((x + buff - m.get_left()[0]) * RIGHT)
        x = m.get_right()[0]
    for m in (S, eq, Re):
        m.set_y(axis + (m.get_center()[1] - m.get_center()[1]))
    S.set_y(axis - 0.06)
    eq.set_y(axis)
    Re.set_y(axis)
    lb.set_y(body.get_center()[1])
    rb.set_y(body.get_center()[1])
    g = VGroup(S, eq, Re, lb, body, rb)
    g.shift(np.array([-g.get_center()[0], y - axis, 0]))
    g.S, g.eq, g.Re, g.lb, g.body, g.rb = S, eq, Re, lb, body, rb
    return g


def body1():
    F = frac(one_minus(EIN, GOLD), one_minus(EI, GOLD))
    F.axis_y = F.bar.get_y()
    return F


def body2():
    F1 = frac(one_minus(EIN, GOLD), one_minus(EI, GOLD))
    F2 = frac(one_minus(EMI, PURPLE), one_minus(EMI, PURPLE))
    times = MathTex(r"\times", font_size=HS)
    g = VGroup(F1, times, F2).arrange(RIGHT, buff=0.25)
    times.set_y(F1.bar.get_y())
    F2.shift((F1.bar.get_y() - F2.bar.get_y()) * UP)
    g.F1, g.times, g.F2, g.axis_y = F1, times, F2, F1.bar.get_y()
    return g


def top_product(size=HS):
    return mt([("(1-", FG), (EIN, GOLD), (")(1-", FG), (EMI, PURPLE), (")", FG)], size)


def real_bottom(size=HS):
    return MathTex(r"2(1-\cos\theta)", font_size=size, color=BLUE)


def body3():
    F = frac(top_product(), real_bottom())
    F.axis_y = F.bar.get_y()
    return F


def final_top(size=HS):
    return mt([("1-", FG), (EMI, PURPLE), ("-", FG), (EIN, GOLD), ("+", FG), (EIN1, GOLD)], size)


def body4():
    F = frac(final_top(), real_bottom())
    F.axis_y = F.bar.get_y()
    return F


def header():
    head = T("Example 30", 38, weight=BOLD).scale(0.8)
    band = Rectangle(width=head.width + 0.6, height=head.height + 0.36).set_fill(GREEN, 0.22).set_stroke(GREEN, 0)
    head.move_to(band)
    g = VGroup(band, head).move_to([0, 3.5, 0])
    g.head, g.band = head, band
    return g


def s3_line():
    """s3's (79) line, small, under the toolbox (Re BLUE, (79) DIM)."""
    A = MathTex("S_N", "=", r"\mathrm{Re}", r"\Big[", r"\sum_{k=0}^{N-1}", r"e^{ik\theta}", r"\Big]", font_size=38)
    A[2].set_color(BLUE)
    tag = MathTex("(79)", font_size=28, color=DIM).next_to(A, RIGHT, buff=0.35)
    g = VGroup(A, tag)
    tb = S1.toolbox()
    g.next_to(tb, DOWN, buff=0.35).align_to(tb, LEFT)
    g.line, g.tag = A, tag
    return g


def formula_block():
    """s4's geometric-series formula with its RED flag, top right."""
    f = S4.geo_formula().scale(0.66)
    f.to_corner(UR, buff=0.5)
    flag = S4.lam_flag().scale(0.85).next_to(f, DOWN, buff=0.22).align_to(f, RIGHT)
    g = VGroup(f, flag)
    g.formula, g.flag = f, flag
    return g


def final_line():
    return hero(body4())


def handover_shot():
    """The {done} frame: header, toolbox, (79) line, s4's formula and flag, and the final S_N line."""
    return VGroup(header(), S1.toolbox(), s3_line(), formula_block(), final_line())


# ---------------------------------------------------------------- the bottom expansion (s8 reuses it)
B1_G = [[("(", FG)], [("1-", FG), (EI, GOLD)], [(")(", FG)], [("1-", FG), (EMI, PURPLE)], [(")", FG)],
        [("=", FG)], [("2", FG)], [("-", FG), (EI, GOLD)], [("-", FG), (EMI, PURPLE)]]
B2_G = [[("=", FG)], [(r"2-2\cos\theta", BLUE)], [("=", FG)], [(r"2(1-\cos\theta)", BLUE)]]


def conj_rows(eqx=EQX, y1=Y_R1, y2=Y_R2, size=RS):
    """The conjugate step for the bottom, two rows with their '=' aligned:
    (1 − e^{iθ})(1 − e^{−iθ}) = 2 − e^{iθ} − e^{−iθ}
                              = 2 − 2cos θ = 2(1 − cos θ)
    Returns (B1, B2): VGroups of pieces (B1_G / B2_G groups)."""
    B1 = pieces(B1_G, size)
    B1.shift(np.array([eqx - B1[5].get_x(), y1 - B1[5].get_y(), 0]))
    B2 = pieces(B2_G, size)
    B2.shift(np.array([eqx - B2[0].get_x(), y2 - B2[0].get_y(), 0]))
    return B1, B2


def conj_step(size=RS):
    """For ch3_s8_recap: the whole bottom expansion as one VGroup, centred at ORIGIN."""
    B1, B2 = conj_rows(size=size)
    return VGroup(B1, B2).move_to(ORIGIN)


# ---------------------------------------------------------------- the inset and the L9 card
IC = np.array([-4.6, -2.0, 0])
IU = 1.1
ITH = 55 * DEGREES


def inset():
    plane = TH.argand_plane(center=IC, unit=IU, extent=1.45)
    p = lambda x, y: IC + IU * np.array([x, y, 0])  # noqa: E731
    e = Arrow(IC, p(np.cos(ITH), np.sin(ITH)), buff=0, stroke_width=4, color=GOLD,
              max_tip_length_to_length_ratio=0.2, tip_length=0.16)
    e_lab = MathTex(EI, font_size=32, color=GOLD).next_to(e.get_end(), RIGHT, buff=0.12)
    w = p(1 - np.cos(ITH), -np.sin(ITH))
    w_arrow = Arrow(IC, w, buff=0, stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.2,
                    tip_length=0.16)
    w_dot = Dot(w, radius=0.07, color=YELLOW)
    im = DashedLine(p(1 - np.cos(ITH), 0), w, dash_length=0.08, color=PINK, stroke_width=5)
    w_lab = MathTex(r"1-" + EI, font_size=32, color=YELLOW).next_to(w_dot, RIGHT, buff=0.15)
    g = VGroup(plane, e, e_lab, im, w_arrow, w_dot, w_lab)
    g.plane, g.e, g.e_lab, g.im, g.w_arrow, g.w_dot, g.w_lab = plane, e, e_lab, im, w_arrow, w_dot, w_lab
    return g


def l9_card():
    eqn = mt([(r"\frac{3+i}{1-i}", FG), (r"\cdot", FG), (r"\frac{1+i}{1+i}", FG), ("=", FG),
              (r"\frac{2+4i}{2}", FG), ("=", FG), ("1+2i", FG)], 40)
    title = T("Example 27 · Lecture 9", 30, DIM)
    inner = VGroup(title, eqn).arrange(DOWN, buff=0.3)
    box = RoundedRectangle(corner_radius=0.15, width=inner.width + 0.6, height=inner.height + 0.5)
    box.set_stroke(DIM, 2).set_fill(BG, 1)
    box.move_to(inner)
    g = VGroup(box, title, eqn).move_to([3.55, -2.4, 0])
    g.box, g.title, g.eqn = box, title, eqn
    return g


def frame_of(h):
    return [h.S, h.eq, h.Re, h.lb, h.rb]


def relayout(cur, new):
    """Move the on-screen S_N = Re[ ] frame pieces (cur: list) onto a new hero's."""
    new = frame_of(new)
    return [cur[i].animate.move_to(new[i]) for i in range(3)] + [Transform(cur[i], new[i]) for i in (3, 4)]


class Ch3S5Conjugate(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ---------------- substitute into the geometric-series formula
    def clip1(self):
        with self.say("c3.conj.1") as c:
            self.tb = S1.toolbox()
            self.s3 = s3_line()
            self.fb = formula_block()
            self.hd = header()
            self.play(*appear(self.tb, self.s3, self.fb.formula, self.fb.flag, shift=None, lag=0.2),  # early: carried over from s1, s3, s4
                      run_time=min(1.6, c.until("this is example")))
            c.wait_until(own_word=self.hd.head)
            self.play(*appear(self.hd, shift=None), run_time=1.0)

            c.wait_until("sub")
            sa = MathTex("a", "=", "1", font_size=RS)
            sl = mt([(r"\lambda", GOLD), ("=", FG), (EI, GOLD)], RS)
            VGroup(sa, sl).arrange(RIGHT, buff=1.2).move_to([-2.6, Y_R1, 0])
            sl.align_to(sa, DOWN)
            # one glyph at a time: an underline flash under just that glyph (a ring round 'a' also caught λ)
            c.wait_until("first term")
            self.play(FlashUnder(self.fb.formula[3][0], buff=0.06, run_time=1.2, time_width=1.5),
                      *appear(sa), run_time=min(1.5, c.until("lambda")))
            c.wait_until("lambda")
            lam_src = self.fb.formula[3][1]
            self.play(FlashUnder(lam_src, buff=0.06, run_time=1.2, time_width=1.5), *appear(sl), run_time=1.5)

            c.wait_until("lamN")
            s2 = mt([(r"\lambda^N", GOLD), ("=", FG), (r"(e^{i\theta})^N", GOLD)], RS)
            s2c = mt([("=", FG), (EIN, GOLD)], RS)
            VGroup(s2, s2c).arrange(RIGHT, buff=0.2).move_to([0, Y_R2, 0]).to_edge(RIGHT, buff=0.8)
            s2c.align_to(s2[1], DOWN)
            self.play(*appear(s2), run_time=1.0)
            c.wait_until("times N theta")
            self.play(*appear(s2c), run_time=0.9)

            c.wait_until("fraction")
            H = hero(body1())
            A = self.s3.line
            self.play(FlashAround(VGroup(A[0], A[2]), run_time=1.2, time_width=1.5),
                      *appear(H.S, H.eq, H.Re, H.lb, H.rb, shift=None, lag=0.1), run_time=1.5)
            c.wait_until("one minus")
            self.play(FlashAround(s2c[1], run_time=1.2, time_width=1.5), *appear(H.body.top),
                      run_time=min(1.5, c.until("all over")))
            c.wait_until("all over")
            self.play(FlashAround(sl[2], run_time=1.2, time_width=1.5), GrowFromCenter(H.body.bar),
                      *appear(H.body.bot), run_time=1.5)
            self.H, self.subs = H, [sa, sl, s2, s2c]
            self.frame = frame_of(H)

    # ---------------- the bottom is complex; recall Example 27
    def clip2(self):
        with self.say("c3.conj.2") as c:
            H = self.H
            q = MathTex("?", font_size=HS, color=YELLOW).next_to(H.Re, UP, buff=0.15)
            self.play(*during(disappear(*self.subs), 0, 0.5), *during(appear(q), 0.4, 1.0), run_time=1.4)
            self.q = q
            c.wait_until("bottom")
            glow = SurroundingRectangle(H.body.bot, color=YELLOW, buff=0.1, corner_radius=0.06)
            glow.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1)
            self.play(FadeIn(glow), FlashAround(H.body.bot, run_time=1.5, time_width=1.5), run_time=1.5)
            self.glow = glow

            c.wait_until("complex")
            I = inset()
            self.play(*appear(I.plane, shift=None), GrowArrow(I.e), *appear(I.e_lab, shift=None),
                      run_time=1.4)
            c.wait_until("and the real part")
            self.play(GrowArrow(I.w_arrow), FadeIn(I.w_dot), *appear(I.w_lab, shift=None), run_time=1.3)
            self.play(Create(I.im), run_time=1.0)
            self.I = I

            c.wait_until("recall")
            K = l9_card()
            self.play(*appear(K.box, K.title, K.eqn, shift=None, lag=0.2), run_time=1.3)
            c.wait_until("trick")
            mid = K.eqn[2]
            self.play(*recolor([mid], YELLOW), FlashAround(mid, run_time=1.5, time_width=1.5), run_time=1.5)
            self.K = K

    # ---------------- multiply by the conjugate; expand the bottom
    def clip3(self):
        with self.say("c3.conj.3") as c:
            self.play(*disappear(self.I, self.glow), run_time=1.0)
            c.wait_until("conj")
            H, H2 = self.H, hero(body2())
            B = H2.body
            self.play(*during(disappear(self.K), 0, 0.4), *during(relayout(self.frame, H2), 0, 0.5),
                      *during([self.q.animate.next_to(H2.Re, UP, buff=0.15),
                               H.body.animate.move_to(B.F1)], 0, 0.5),
                      *during(appear(B.times, B.F2, shift=None, lag=0.3), 0.45, 1.0),
                      run_time=min(2.0, c.until("bottom2")))
            self.F1, self.times, self.F2 = H.body, B.times, B.F2

            c.wait_until("bottom2")
            B1, B2 = conj_rows()
            self.play(FlashAround(self.F1.bot, run_time=1.2, time_width=1.5),
                      FlashAround(self.F2.bot, run_time=1.2, time_width=1.5),
                      *during(appear(*B1[0:6], shift=None, lag=0.1), 0.3, 1.0), run_time=1.8)

            c.wait_until("ones")
            one = MathTex("1", font_size=RS).move_to(B1[6])
            p1 = MathTex("+1", font_size=RS).next_to(one, RIGHT, buff=0.12).align_to(one, DOWN)
            self.play(FlashAround(B1[1][0][0], run_time=1.2, time_width=1.5),
                      FlashAround(B1[3][0][0], run_time=1.2, time_width=1.5), *appear(one), run_time=1.2)
            c.wait_until("and E to the eye theta")
            self.play(FlashAround(B1[1][1], run_time=1.2, time_width=1.5),
                      FlashAround(B1[3][1], run_time=1.2, time_width=1.5), *appear(p1), run_time=1.2)
            c.wait_until("one too")
            self.play(*swap(VGroup(one, p1), B1[6]), run_time=1.2)

            c.wait_until("cross")
            self.play(FlashAround(VGroup(B1[1][1], B1[3][0][0]), run_time=1.2, time_width=1.5),
                      *appear(B1[7]), run_time=1.2)
            c.wait_until("and minus")
            self.play(FlashAround(VGroup(B1[1][0][0], B1[3][1]), run_time=1.2, time_width=1.5),
                      *appear(B1[8]), run_time=1.2)
            self.B1, self.B2 = B1, B2

    # ---------------- the mirror pair: a real bottom
    def clip4(self):
        with self.say("c3.conj.4") as c:
            B1, B2 = self.B1, self.B2
            self.play(FlashAround(VGroup(B1[7], B1[8]), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("adding up")
            src = self.tb[0]
            dst = S1.tool_lines()[0].scale(0.62)
            dst.move_to([0, Y_R1, 0]).to_edge(RIGHT, buff=0.5)
            self.play(FlashAround(src, run_time=1.5, time_width=1.5), *appear(dst), run_time=1.5)
            self.c77 = dst

            c.wait_until("real")
            self.play(*appear(B2[0], B2[1], shift=None, lag=0.3), run_time=1.2)
            c.wait_until("one minus cosine")
            self.play(*appear(B2[2], B2[3], shift=None, lag=0.3), run_time=1.2)
            tag = T("real", 32, BLUE).next_to(B2[3], RIGHT, buff=0.35)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), *disappear(self.q), run_time=1.0)
            self.tag = tag

            c.wait_until("mod")
            mod = pieces([[("=", FG)], [(r"|1-", FG), (EI, GOLD), (r"|^2", FG)]], 38)
            mod.shift(np.array([EQX - mod[0].get_x(), Y_R3 - mod[0].get_y(), 0]))
            self.play(*appear(mod, shift=None), run_time=1.2)
            self.mod = mod

    # ---------------- the top, four terms
    def clip5(self):
        with self.say("c3.conj.5") as c:
            B1, B2 = self.B1, self.B2
            H3 = hero(body3())
            out = [*B1, B2[0], B2[1], B2[2], self.tag, self.mod, self.c77, self.F1, self.times, self.F2]
            self.play(*during(disappear(*out), 0, 0.45),
                      *during(relayout(self.frame, H3), 0.2, 0.8),
                      *during([Transform(B2[3], H3.body.bot)], 0.4, 1.0),
                      *during(appear(H3.body.top, H3.body.bar, shift=None), 0.55, 1.0),
                      run_time=min(1.8, c.until("it has four")))
            bot = B2[3]

            c.wait_until("it has four")
            R = pieces([[("(1-", FG), (EIN, GOLD), (")(1-", FG), (EMI, PURPLE), (")", FG)], [("=", FG)],
                        [("1", FG)], [("-", FG), (EMI, PURPLE)], [("-", FG), (EIN, GOLD)], [("+", FG)],
                        [(EIN1, GOLD)]], RS)
            R.move_to([0, Y_R1, 0])
            prod = mt([(EIN, GOLD), (EMI, PURPLE)], RS)
            prod.align_to(R[6], LEFT).align_to(R[6], DOWN)
            lhs = R[0]
            self.play(FlashAround(H3.body.top, run_time=1.2, time_width=1.5),
                      *during(appear(lhs, R[1], shift=None, lag=0.2), 0.3, 1.0), run_time=1.5)

            c.wait_until("t1")
            self.play(FlashAround(VGroup(lhs[0][1], lhs[2][2]), run_time=1.0, time_width=1.5),
                      *appear(R[2], shift=None), run_time=1.0)
            c.wait_until("t2")
            self.play(FlashAround(VGroup(lhs[0][1], lhs[3]), run_time=1.2, time_width=1.5),
                      *appear(R[3]), run_time=1.2)
            c.wait_until("t3")
            self.play(FlashAround(VGroup(lhs[1], lhs[2][2]), run_time=1.2, time_width=1.5),
                      *appear(R[4]), run_time=1.2)
            c.wait_until("t4")
            self.play(FlashAround(VGroup(lhs[1], lhs[3]), run_time=1.2, time_width=1.5),
                      *appear(R[5], prod, lag=0.2), run_time=1.3)

            c.wait_until("adds")
            note = MathTex(r"N\theta-\theta=(N-1)\theta", font_size=38, color=YELLOW)
            note.next_to(prod, DOWN, buff=0.45).align_to(prod, RIGHT).shift(0.3 * RIGHT)
            if note.get_right()[0] > 6.6:
                note.shift((6.6 - note.get_right()[0]) * RIGHT)
            self.play(*appear(note), run_time=1.2)
            self.play(FlashAround(note, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("so that last one")
            self.play(*edit(prod, R[6]), run_time=1.5)

            c.wait_until("done")
            H4 = final_line()
            self.play(*during(disappear(H3.body.top), 0, 0.4),
                      *during(relayout(self.frame, H4), 0.2, 0.8),
                      *during([Transform(H3.body.bar, H4.body.bar), bot.animate.move_to(H4.body.bot)], 0.2, 0.8),
                      *during(appear(H4.body.top, shift=None), 0.55, 1.0),
                      run_time=1.6)
            self.play(*disappear(*R[0:6], note), run_time=min(1.0, c.until()))
            self.remove(*self.mobjects)
            self.add(handover_shot())
            c.wait_until()
        self.wait(0.6)
