"""Chapter 1, scene 4: putting the i back: cos(ix) = cosh x. Clips c1.cosix.1 – c1.cosix.4.

Owns the dictionary card (`dictionary_card`), imported by ch1_s5_sinix, ch1_s6_dictionary,
ch1_s7_recap (later ch2 s3/s6, ch4 s3). Ends on `handover_shot()`: the card's header and row 1,
small, top-right; ch1_s5_sinix opens on it.
"""
# style: 2
# handover: next
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- coloured maths
_COL = {"B": BLUE, "T": TEAL, "P": PINK, "G": GOLD, "U": PURPLE, "F": FG, "Y": YELLOW, "D": DIM}


def ctex(src, pattern, size=52):
    """MathTex coloured glyph by glyph: one letter of `pattern` per glyph in reading order
    (B blue, T teal, P pink, G gold, U purple, F fg, Y yellow, D dim; spaces ignored)."""
    m = MathTex(src, font_size=size)
    pat = pattern.replace(" ", "")
    glyphs = m[0]
    assert len(glyphs) == len(pat), (src, len(glyphs), len(pat))
    for g, ch in zip(glyphs, pat):
        g.set_color(_COL[ch])
    return m


def at_glyph(m, idx, x, y):
    """Shift m so its glyph idx is centred at (x, y)."""
    m.shift(np.array([x, y, 0]) - m[0][idx].get_center())
    return m


def words_var(before, var, after="", size=30, color=DIM):
    """Prose with an italic maths variable inside: T(before) x T(after)."""
    parts = []
    if before:
        parts.append(T(before, size=size, color=color))
    v = MathTex(var, font_size=size * 1.3, color=color)
    parts.append(v)
    if after:
        parts.append(T(after, size=size, color=color))
    g = VGroup(*parts).arrange(RIGHT, buff=0.14 * size / 30)
    v.align_to(parts[0][-1] if before else parts[-1][0], DOWN)
    return g


# ---------------------------------------------------------------- the dictionary card
CARD_ROWS = [
    (r"\cos(ix) = \cosh x", "BBBFPFFF TTTTF", "(90)"),
    (r"\sin(ix) = i \sinh x", "BBBFPFFF P TTTTF", "(91)"),
    (r"\tan(ix) = i \tanh x", "BBBFPFFF P TTTTF", "(92)"),
]
CARD_EQ = 7          # glyph index of "=" in every row


def dictionary_card(rows=3, full=False):
    """The cos/sin/tan(ix) dictionary card. `rows` = how many rows are shown (1–3); the layout is
    always that of the full 3-row card, so rows never move as the card grows.
    small (full=False): top-right corner; full=True: big, centred.
    Returns a VGroup(header, *shown rows) with .header, .rows (shown), .all_rows (all three,
    positioned); each row is VGroup(tex, num) with .tex and .num."""
    k = 1.5 if full else 1.0
    pitch = 0.74 * k
    all_rows = []
    for i, (src, pat, num) in enumerate(CARD_ROWS):
        tex = ctex(src, pat, size=40 * k)
        at_glyph(tex, CARD_EQ, 0, -i * pitch)
        n = T(num, size=28 * k, color=DIM)
        row = VGroup(tex, n)
        row.tex, row.num = tex, n
        all_rows.append(row)
    right = max(r.tex.get_right()[0] for r in all_rows) + 0.4 * k
    for r in all_rows:
        r.num.move_to([right, r.tex[0][CARD_EQ].get_y(), 0], aligned_edge=LEFT)
    left = min(r.tex.get_left()[0] for r in all_rows)
    header = words_var("for every complex", "x", size=30 * k, color=YELLOW)
    header.move_to([left, all_rows[0].tex.get_top()[1] + 0.3 * k, 0], aligned_edge=DL)
    whole = VGroup(header, *all_rows)
    if full:
        whole.move_to(ORIGIN)
    else:
        whole.to_corner(UR, buff=0.5)
    card = VGroup(header, *all_rows[:rows])
    card.header = header
    card.rows = all_rows[:rows]
    card.all_rows = all_rows
    return card


def handover_shot():
    """Last frame of this scene / first of ch1_s5_sinix: header + row 1, small, top-right."""
    return dictionary_card(rows=1)


# ---------------------------------------------------------------- derivation lines
SRC_COSX = (r"\cos x = \frac{e^{ix} + e^{-ix}}{2}", "BBBFF GPGF UUPU FF")
SRC_COSHX = (r"\cosh x = \frac{e^{x} + e^{-x}}{2}", "TTTTFF GGF UUU FF")
SRC_COSZ = (r"\cos z = \frac{e^{iz} + e^{-iz}}{2}", "BBBFF GPGF UUPU FF")
SRC_D = (r"\cos(ix) = \frac{e^{i \cdot ix} + e^{-i \cdot ix}}{2}", "BBBFPFFF GPGPG F UUPUPU FF")
SRC_E = (r"= \frac{e^{i^2 x} + e^{-i^2 x}}{2}", "F GPPG F UUPPU FF")
SRC_F = (r"= \frac{e^{-x} + e^{-i^2 x}}{2}", "F UUU F UUPPU FF")
SRC_G = (r"= \frac{e^{-x} + e^{x}}{2}", "F UUU F GG FF")
SRC_H = (r"= \frac{e^{x} + e^{-x}}{2}", "F GG F UUU FF")
SRC_RESULT = CARD_ROWS[0][:2]
SRC_CHECK = (r"\cos(i) = \cosh 1 \approx 1.54", "BBBFPFF TTTTF F YYYY")

XEQ = -2.0                     # x of the column's "=" signs
ROW_Y = [2.3, 0.5, -1.3]       # rows of the derivation column
NOTE_X = 3.9                   # right-hand notes
SZ = 52


def grp(m, a, b):
    """A fresh VGroup of glyphs a..b-1 (for flashes / positions only, never animated itself)."""
    return VGroup(*m[0][a:b])


def thumbnail():
    """Small copy of ch1_s2_define's graph: e^x GOLD, e^-x PURPLE, cosh TEAL, midpoint at x = 1."""
    ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-3, 5, 1], x_length=4.2, y_length=3.2, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": False})
    ax.move_to([-4.3, -1.85, 0])
    l5 = math.log(5)
    ex = ax.plot(lambda x: math.exp(x), x_range=[-2.5, l5], color=GOLD, stroke_width=4)
    emx = ax.plot(lambda x: math.exp(-x), x_range=[-l5, 2.5], color=PURPLE, stroke_width=4)
    a5 = math.acosh(5)
    ch = ax.plot(lambda x: math.cosh(x), x_range=[-a5, a5], color=TEAL, stroke_width=5)
    pg = Dot(ax.c2p(1, math.e), radius=0.07, color=GOLD)
    pu = Dot(ax.c2p(1, 1 / math.e), radius=0.07, color=PURPLE)
    seg = DashedLine(pg.get_center(), pu.get_center(), dash_length=0.06, color=DIM, stroke_width=2)
    mid = Dot(ax.c2p(1, math.cosh(1)), radius=0.1, color=TEAL)
    g = VGroup(ax, ex, emx, ch, seg, pg, pu, mid)
    g.ax, g.curves, g.pts, g.mid = ax, [ex, emx, ch], [seg, pg, pu], mid
    return g


def band():
    """Cosine wave (BLUE) between dashed y = 1 and y = -1, and the point 1.54 above it."""
    cy, u, x0, w = -2.0, 0.75, 1.3, 4.8
    sx = w / (4 * PI)
    wave = ParametricFunction(lambda t: np.array([x0 + sx * t, cy + u * math.cos(t), 0]),
                              t_range=[0, 4 * PI], color=BLUE, stroke_width=4)
    top = DashedLine([x0 - 0.1, cy + u, 0], [x0 + w + 0.1, cy + u, 0], dash_length=0.12,
                     color=DIM, stroke_width=2)
    bot = DashedLine([x0 - 0.1, cy - u, 0], [x0 + w + 0.1, cy - u, 0], dash_length=0.12,
                     color=DIM, stroke_width=2)
    one = MathTex("1", font_size=34, color=DIM).next_to(top, LEFT, buff=0.15)
    mone = MathTex("-1", font_size=34, color=DIM).next_to(bot, LEFT, buff=0.15)
    px = x0 + sx * 2 * PI
    dot = Dot([px, cy + u * 1.543, 0], radius=0.11, color=YELLOW)
    val = MathTex("1.54", font_size=40, color=YELLOW).next_to(dot, RIGHT, buff=0.18)
    g = VGroup(wave, top, bot, one, mone, dot, val)
    g.wave, g.top, g.bot, g.one, g.mone, g.dot, g.val = wave, top, bot, one, mone, dot, val
    return g


class CosIx(NarratedScene):
    def born(self, src, dst, si=0):
        """derive() without the copy sitting on its source: a copy of src fades in on dst's row
        (dropping a little), then is edited into dst."""
        cp = src.copy().shift((dst[0][0].get_y() - src[0][si].get_y()) * UP)
        self.play(FadeIn(cp, shift=0.4 * DOWN), run_time=0.8)
        self.play(*edit(cp, dst), run_time=1.4)

    def construct(self):
        # ---------------------------------------------------------------- 1: cos z
        with self.say("c1.cosix.1") as c:
            cosx = ctex(*SRC_COSX, size=44).move_to([-3.4, 0.3, 0])
            coshx = ctex(*SRC_COSHX, size=44).move_to([3.4, 0.3, 0])
            n84 = T("(84)", size=28, color=DIM).next_to(coshx, DOWN, buff=0.35)
            self.play(*appear(cosx, coshx, n84, lag=0.2), run_time=1.0)
            c.wait_until("cosz")
            self.play(*disappear(coshx, n84), run_time=0.8)
            cosz = ctex(*SRC_COSZ, size=60).move_to([0, 0.4, 0])
            self.play(*edit(cosx, cosz), run_time=1.5)
            note = words_var("any complex", "z").next_to(cosz, DOWN, buff=0.55)
            c.wait_until("complex")
            self.play(*appear(note), run_time=0.9)
            c.wait_until("It's E to the eye zed")
            self.play(FlashAround(grp(cosz, 5, 8), color=GOLD, run_time=1.3, time_width=1.5))
            c.wait_until("plus E to the minus")
            self.play(FlashAround(grp(cosz, 9, 13), color=PURPLE, run_time=1.3, time_width=1.5))

        # ---------------------------------------------------------------- 2: z = ix, i^2 = -1
        with self.say("c1.cosix.2") as c:
            tgt = cosz.copy().scale(SZ / 60)
            at_glyph(tgt, 4, XEQ, ROW_Y[0])
            cosz.target = tgt
            self.play(MoveToTarget(cosz), *disappear(note), run_time=1.3)
            tag = ctex(r"z = ix", "YYPY", size=48).move_to([NOTE_X, ROW_Y[0] + 0.15, 0])
            c.wait_until("Put zed equal")
            self.play(*appear(tag), run_time=1.0)
            d = at_glyph(ctex(*SRC_D, size=SZ), 7, XEQ, ROW_Y[0])
            c.wait_until("eye times ex")
            self.play(*edit(cosz, d), run_time=1.5)
            tag_note = words_var("", "x", "complex too").next_to(tag, DOWN, buff=0.3)
            c.wait_until("complex")
            self.play(*appear(tag_note), run_time=0.9)
            c.wait_until("isq")
            self.play(FlashAround(grp(d, 9, 13), run_time=1.5, time_width=1.5))
            e = at_glyph(ctex(*SRC_E, size=SZ), 0, XEQ, ROW_Y[1])
            c.wait_until("That's eye squared")
            self.born(d, e, si=7)
            margin = ctex(r"i^2 = -1", "YYYYY", size=50).rotate(6 * DEGREES)
            margin.move_to([NOTE_X, ROW_Y[1] + 0.05, 0])
            c.wait_until("margin")
            self.play(*appear(margin), run_time=1.0)
            self.play(*flash([grp(e, 2, 4), grp(e, 8, 10)]), run_time=1.0)
            f = at_glyph(ctex(*SRC_F, size=SZ), 0, XEQ, ROW_Y[2])
            c.wait_until("flip")
            self.born(e, f)
            c.wait_until("the minus in front")
            self.play(FlashAround(grp(f, 6, 9), run_time=1.4, time_width=1.5))
            g = at_glyph(ctex(*SRC_G, size=SZ), 0, XEQ, ROW_Y[2])
            c.wait_until("two minuses")
            self.play(*edit(f, g), run_time=1.5)
            c.wait_until("You get E to the ex")
            self.play(FlashAround(grp(g, 5, 7), color=GOLD, run_time=1.2, time_width=1.5))

        # ---------------------------------------------------------------- 3: swap, = cosh x
        with self.say("c1.cosix.3") as c:
            h = at_glyph(ctex(*SRC_H, size=SZ), 0, XEQ, ROW_Y[2])
            c.wait_until("The two exponentials")
            t1, t2 = list(g[0][1:4]), list(g[0][5:7])
            d1 = grp(h, 4, 7).get_center() - VGroup(*t1).get_center()
            d2 = grp(h, 1, 3).get_center() - VGroup(*t2).get_center()
            anims = []
            for gl in t1:      # e^{-x} arches over to the right
                p = gl.get_center()
                path = VMobject().set_points_smoothly(
                    [p, p + 0.55 * UP + 0.2 * d1, p + 0.6 * UP + 0.5 * d1, p + 0.55 * UP + 0.8 * d1, p + d1])
                anims.append(MoveAlongPath(gl, path))
            for gl in t2:      # e^{x} slides straight left underneath
                anims += during([gl.animate.shift(d2)], 0.15, 0.85)
            anims += during([FadeOut(g[0][4])], 0, 0.15)
            anims += during([FadeIn(h[0][3])], 0.85, 1)
            self.play(*anims, run_time=2.0)
            self.remove(*g.get_family(), h[0][3])
            self.add(h)
            cosh84 = ctex(*SRC_COSHX, size=40).move_to([4.0, ROW_Y[2], 0])
            l84 = T("(84)", size=28, color=DIM).next_to(cosh84, DOWN, buff=0.3)
            c.wait_until("order")
            self.play(*appear(cosh84, l84, lag=0.4), run_time=1.3)
            c.wait_until("It's E to the ex")
            self.play(*flash([grp(h, 1, 3), grp(cosh84, 6, 8)], color=GOLD), run_time=1.1)
            c.wait_until("plus E to the minus ex")
            self.play(*flash([grp(h, 4, 7), grp(cosh84, 9, 12)], color=PURPLE), run_time=1.1)
            c.wait_until("exactly cosh")
            self.play(FlashAround(grp(cosh84, 0, 5), color=TEAL, run_time=1.3, time_width=1.5))
            result = ctex(*SRC_RESULT, size=80).move_to([0, 0.3, 0])
            box = SurroundingRectangle(result, color=YELLOW, buff=0.35, stroke_width=4)
            n90 = T("(90)", size=34, color=DIM).next_to(box, RIGHT, buff=0.35)
            c.wait_until("boxed")
            sweep_clear(self, FadeIn(result), GrowFromCenter(box), FadeIn(n90), run_time=1.8)

        # ---------------------------------------------------------------- 4: cos i = 1.54
        with self.say("c1.cosix.4") as c:
            card = dictionary_card(rows=1)
            row = card.rows[0]
            # the box shrinks with the result into the row and fades on the way (no empty box left behind)
            box_end = SurroundingRectangle(row.tex, color=YELLOW, buff=0.12, stroke_width=2).set_stroke(opacity=0)
            self.play(ReplacementTransform(result, row.tex), ReplacementTransform(n90, row.num),
                      ReplacementTransform(box, box_end), run_time=1.5)
            self.remove(box_end)
            self.play(*appear(card.header), run_time=0.8)  # early: card header, not read aloud
            check = ctex(*SRC_CHECK, size=56).move_to([-0.6, 1.1, 0])
            c.wait_until("The cosine of eye")
            self.play(*appear(check), run_time=1.0)
            c.wait_until("about one point")
            self.play(FlashAround(grp(check, 13, 17), run_time=1.3, time_width=1.5))
            th = thumbnail()
            c.wait_until("midpoint")
            self.play(*appear(th.ax, *th.curves, *th.pts, shift=None, lag=0.15), run_time=1.3)
            self.play(FlashAround(th.mid, color=TEAL, run_time=1.3, time_width=1.5),
                      *appear(th.mid, shift=None), run_time=1.3)
            bd = band()
            c.wait_until("stuck")
            self.play(Create(bd.wave), *appear(bd.top, bd.bot, bd.one, bd.mone, shift=None),
                      run_time=1.5)
            c.wait_until("bigger")
            self.play(FlashAround(grp(check, 13, 17), run_time=1.5, time_width=1.5),
                      *appear(bd.dot, bd.val, lag=0.3), run_time=1.5)
            c.wait_until("stuck between")
            self.play(VShowPassingFlash(Line(bd.top.get_left(), bd.top.get_right()).set_stroke(YELLOW, 5)),
                      VShowPassingFlash(Line(bd.bot.get_left(), bd.bot.get_right()).set_stroke(YELLOW, 5)),
                      run_time=1.3)
            c.wait_until("breaks free")
            self.play(FlashAround(VGroup(bd.dot, bd.val), run_time=1.4, time_width=1.5))

        keep = set(card.get_family())
        rest = [m for m in self.mobjects if m not in keep]
        self.play(*disappear(*rest), run_time=1.0)
        self.wait(1.0)
