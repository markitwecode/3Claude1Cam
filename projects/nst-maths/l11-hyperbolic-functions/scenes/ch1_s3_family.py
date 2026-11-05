"""Chapter 1, scene 3: tanh and the three reciprocals. Clips c1.family.1 – c1.family.4.

Module-level builders imported by ch1_s7_recap: family_card() (tanh row on top, then the three
reciprocal rows; BLUE circular parents, TEAL hyperbolic children, DIM equation numbers) and
inverse_card() (the RED cosh^{-1} x != 1/cosh x warning).
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
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- maths helpers
def mt(src, size=48, color=FG, cmap=None):
    """MathTex in one colour, with glyph ranges recoloured: cmap = {(a, b): colour}."""
    m = MathTex(src, font_size=size, color=color)
    for (a, b), col in (cmap or {}).items():
        for g in m[0][a:b]:
            g.set_color(col)
    return m


def G(m, a, b):
    """Glyphs a..b-1 of a MathTex, as a fresh VGroup (for copies, flashes, fly sources)."""
    return VGroup(*m[0][a:b])


def at_glyph(m, idx, x, y):
    """Shift m so its glyph idx is centred at (x, y)."""
    m.shift(np.array([x, y, 0]) - m[0][idx].get_center())
    return m


def num(n, size=28):
    return T(f"({n})", size=size, color=DIM)


# glyph layouts (checked): exponentials coloured GOLD e^x, PURPLE e^{-x}
def cosh_def(size=34):
    return mt(r"\cosh x = \tfrac{1}{2}\left(e^{x} + e^{-x}\right)", size,
              cmap={(0, 4): TEAL, (10, 12): GOLD, (13, 16): PURPLE})


def sinh_def(size=34):
    return mt(r"\sinh x = \tfrac{1}{2}\left(e^{x} - e^{-x}\right)", size,
              cmap={(0, 4): TEAL, (10, 12): GOLD, (13, 16): PURPLE})


def value_tex(name, val, size=38):
    """s2's label style: "sinh 1 ≈ 1.18" with TEAL name, GOLD numbers."""
    return mt(rf"\{name} 1 \approx {val}", size, cmap={(0, 4): TEAL, (4, 5): GOLD, (6, 10): GOLD})


SRC_TAN = r"\tan x = \frac{\sin x}{\cos x}"
SRC_TANH = r"\tanh x = \frac{\sinh x}{\cosh x}"
CARD_ROWS = [  # (parent src, parent '=' index, child src, child '=' index, number)
    (SRC_TAN, 4, SRC_TANH, 5, None),
    (r"\sec x = \frac{1}{\cos x}", 4, r"\operatorname{sech} x = \frac{1}{\cosh x}", 5, 87),
    (r"\operatorname{cosec} x = \frac{1}{\sin x}", 6, r"\operatorname{cosech} x = \frac{1}{\sinh x}", 7, 88),
    (r"\cot x = \frac{1}{\tan x}", 4, r"\coth x = \frac{1}{\tanh x}", 5, 89),
]
# index of the trailing "h" of every hyperbolic name in each child row
CARD_H = [(3, 9, 15), (3, 11), (5, 13), (3, 11)]
CARD_SIZE = 44
CARD_EQ_X = (-3.4, 2.3)
CARD_ROW_Y = (1.75, 0.5, -0.75, -2.0)
HEAD_Y = 2.95


def pulse(glyph, color=YELLOW, scale=1.3):
    """A colour pulse of one glyph in place: to `color` and `scale`x, then back (no wrapper)."""
    base, c0, ctr = glyph.copy(), glyph.get_color(), glyph.get_center()

    def upd(m, a):
        w = there_and_back(a)
        m.become(base.copy().scale(1 + (scale - 1) * w, about_point=ctr)
                 .set_color(interpolate_color(ManimColor(c0), ManimColor(color), w)))
    return UpdateFromAlphaFunc(glyph, upd)


def family_card(size=CARD_SIZE):
    """The family card at full size (frame-centred): VGroup of rows, each VGroup(parent, child, num).
    Attributes: .rows .parents .children .nums (num is an empty VGroup for the tanh row) .eq
    (list of (parent '=' idx, child '=' idx)). Scale/move the whole card for a small recap."""
    k = size / CARD_SIZE
    rows, parents, children, nums, eq = [], [], [], [], []
    for (ps, pe, cs, ce, n), y in zip(CARD_ROWS, CARD_ROW_Y):
        p = at_glyph(mt(ps, size, BLUE), pe, CARD_EQ_X[0] * k, y * k)
        ch = at_glyph(mt(cs, size, TEAL), ce, CARD_EQ_X[1] * k, y * k)
        nm = num(n).scale(k).move_to([4.75 * k, y * k, 0]) if n else VGroup()
        rows.append(VGroup(p, ch, nm))
        parents.append(p)
        children.append(ch)
        nums.append(nm)
        eq.append((pe, ce))
    card = VGroup(*rows)
    card.rows, card.parents, card.children, card.nums, card.eq = rows, parents, children, nums, eq
    return card


def card_headers(size=34):
    """BLUE / TEAL column headers that sit over family_card()'s columns."""
    hc = T("cosine, sine, tangent", size, BLUE).move_to([-3.4, HEAD_Y, 0])
    hh = T("cosh, shine, tanch", size, TEAL).move_to([2.6, HEAD_Y, 0])
    return VGroup(hc, hh)


def inverse_card(size=52):
    """The RED warning: cosh^{-1} x != 1/cosh x, in a RED rounded frame, centred at ORIGIN.
    .tex (glyphs: 0-3 cosh, 4-5 ^{-1}, 6 x, 7-8 !=, 9 1, 10 bar, 11-14 cosh, 15 x), .box."""
    tex = mt(r"\cosh^{-1} x \neq \frac{1}{\cosh x}", size, RED)
    box = SurroundingRectangle(tex, color=RED, buff=0.35, corner_radius=0.15).set_stroke(RED, 3)
    card = VGroup(box, tex)
    card.tex, card.box = tex, box
    return card


NOTES_TEXT = ("When spoken, the names ‘hyperbolic cosine’,\n"
              "‘hyperbolic sine’ and ‘hyperbolic tangent’ are often\n"
              "abbreviated to ‘cosh’, ‘shine’ and ‘tanch’.")


def speech(word):
    return T(f"“{word}”", 30, YELLOW, slant=ITALIC)


class Family(NarratedScene):
    def regroup(self, m, *wrappers):
        """Pieces of m were animated one by one: put m back on screen as one object."""
        for w in wrappers:
            self.remove(w)
        self.remove(*m.get_family())
        self.add(m)

    def born(self, c, parent, child, pe, ce, n, rt=2.0):
        """A TEAL row grows out of its BLUE parent: a copy slides right, then gains its 'h'."""
        moved = parent.copy()
        moved.shift(child[0][ce].get_center() - moved[0][pe].get_center())
        self.play(*fly(parent, moved), run_time=0.55 * rt)
        self.play(*edit(moved, child), run_time=0.45 * rt)
        if n is not None and len(n):
            self.play(*appear(n), run_time=0.6)

    def construct(self):
        RX = 2.9      # hyperbolic column centre (clips 1-2)
        LX = -3.4     # circular column centre
        ROW = 0.8

        # ---------------------------------------------------------------- 1: tanh
        with self.say("c1.family.1") as c:
            cdef = cosh_def().move_to([-6.4, 3.25, 0], aligned_edge=LEFT)
            n84 = num(84).next_to(cdef, RIGHT, buff=0.3)
            sdef = sinh_def().next_to(n84, RIGHT, buff=0.8)
            n85 = num(85).next_to(sdef, RIGHT, buff=0.3)
            self.play(*appear(cdef, n84, sdef, n85, shift=None, lag=0.15),  # early: s2's definitions, carried over
                      run_time=0.9)
            tan = mt(SRC_TAN, 52, BLUE).move_to([LX, ROW, 0])
            self.play(*appear(tan), run_time=1.0)
            tanh = mt(SRC_TANH, 52, TEAL).move_to([RX, ROW, 0])
            c.wait_until("the hyperbolic tangent")
            t_num, t_den = G(tanh, 6, 11), G(tanh, 12, 17)
            t_lhs, t_bar = G(tanh, 0, 6), tanh[0][11]
            # copies of the two names drop out just under their definitions, then fly into place
            # (a copy flying off its source would run over the rest of that definition)
            rt = min(1.6, c.until("cosh") + 0.3)
            m_num, m_den = G(sdef, 0, 5).copy().shift(0.9 * DOWN), G(cdef, 0, 5).copy().shift(0.9 * DOWN)
            self.play(*appear(m_num, m_den, lag=0), run_time=0.4 * rt)
            self.play(*fly(m_num, t_num), *fly(m_den, t_den),
                      *during(disappear(m_num, m_den), 0, 0.3), run_time=0.6 * rt)
            self.play(*appear(t_lhs, t_bar, shift=None, lag=0.2), run_time=0.8)
            self.regroup(tanh, t_num, t_den, t_lhs)

            # {one}: the numbers from s2 make tanh 1
            c.wait_until("one")
            ls = value_tex("sinh", "1.18").move_to([LX - 0.9, -1.05, 0])
            lc = value_tex("cosh", "1.54").move_to([LX - 0.9, -1.95, 0])
            self.play(*appear(ls, lc, lag=0.3), run_time=1.0)
            t1 = mt(r"\tanh 1 \approx \frac{1.18}{1.54} \approx 0.76", 48,
                    cmap={(0, 4): TEAL, (4, 5): GOLD, (6, 10): GOLD, (11, 15): GOLD, (16, 20): GOLD})
            t1.move_to([RX, -1.5, 0])
            n_top, n_bot = G(t1, 6, 10), G(t1, 11, 15)
            t1_head, t1_bar, t1_tail = G(t1, 0, 6), t1[0][10], G(t1, 15, 20)
            c.wait_until("one point one eight")
            self.play(*during(fly(G(ls, 6, 10), n_top) + fly(G(lc, 6, 10), n_bot), 0, 0.45),
                      *during(appear(t1_head, t1_bar, shift=None, lag=0.1), 0.55, 1.0),
                      run_time=1.5)
            c.wait_until("tanch of one")
            self.play(*appear(t1_tail, shift=None), run_time=0.9)
            self.regroup(t1, n_top, n_bot, t1_head, t1_tail)

            # {expand}: write both in exponentials; the halves cancel
            c.wait_until("expand")
            self.play(*disappear(ls, lc, t1), run_time=0.8)
            ex = mt(r"\tanh x = \frac{\frac{1}{2}(e^{x} - e^{-x})}{\frac{1}{2}(e^{x} + e^{-x})}", 52,
                    cmap={(0, 4): TEAL, (10, 12): GOLD, (13, 16): PURPLE, (22, 24): GOLD, (25, 28): PURPLE})
            at_glyph(ex, 5, tanh[0][5].get_x(), -2.0)
            self.play(*appear(ex, shift=0.5 * DOWN), run_time=min(1.4, c.until("a half")))
            c.wait_until("a half")
            halves = [G(ex, 6, 9), G(ex, 18, 21)]
            self.play(*[FlashAround(h, color=YELLOW, time_width=1.5) for h in halves],
                      *recolor(list(ex[0][6:9]) + list(ex[0][18:21]), YELLOW), run_time=1.3)
            fin = mt(r"\tanh x = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}}", 52,
                     cmap={(0, 4): TEAL, (6, 8): GOLD, (9, 12): PURPLE, (13, 15): GOLD, (16, 19): PURPLE})
            at_glyph(fin, 5, ex[0][5].get_x(), ex[0][5].get_y())
            c.wait_until("What's left")
            self.play(*edit(ex, fin), run_time=1.6)
            n86 = num(86).next_to(fin, RIGHT, buff=0.35)
            self.play(*appear(n86, shift=None), run_time=0.7)

        # ---------------------------------------------------------------- 2: the names
        with self.say("c1.family.2") as c:
            box_t = VGroup(*[T(ln, 30, FG) for ln in NOTES_TEXT.split("\n")])
            box_t.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.15, width=box_t.width + 0.9, height=box_t.height + 0.9)
            box.set_fill("#262A31", 1).set_stroke(DIM, 1.5)
            notes = VGroup(box, box_t).move_to([0, -1.95, 0])
            box_t.move_to(box)
            c.wait_until("The notes say")
            self.play(*during(disappear(fin, n86), 0, 0.45),
                      *during(appear(notes, shift=None), 0.5, 1.0),  # early: the notes' box, quoted whole
                      run_time=1.3)
            s_cosh = speech("cosh").next_to(G(cdef, 0, 4), DOWN, buff=0.2)
            s_shine = speech("shine").next_to(G(sdef, 0, 4), DOWN, buff=0.2)
            s_tanch = speech("tanch").next_to(G(tanh, 0, 4), DOWN, buff=0.4)
            c.wait_until(own_word=s_cosh)
            self.play(*appear(s_cosh, shift=0.15 * DOWN), run_time=0.7)
            c.wait_until(own_word=s_shine)
            self.play(*appear(s_shine, shift=0.15 * DOWN), run_time=min(0.5, c.until("tanch")))
            c.wait_until(own_word=s_tanch)
            self.play(*appear(s_tanch, shift=0.15 * DOWN), run_time=0.6)
            hdr = card_headers()
            hc, hh = hdr[0].copy().move_to([LX, 2.0, 0]), hdr[1].copy().move_to([RX, 2.0, 0])
            c.wait_until(own_word=hc)
            self.play(*appear(hc), run_time=1.0)
            c.wait_until(own_word=hh)
            self.play(*appear(hh), run_time=1.0)

        # ---------------------------------------------------------------- 3: the family card
        card = family_card()
        with self.say("c1.family.3") as c:
            # each spoken name leaves with its definition (no lagged sweep: labels must not outlive them)
            gone = [cdef, n84, sdef, n85, s_cosh, s_shine, s_tanch, notes]
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during([ReplacementTransform(tan, card.parents[0]),
                               ReplacementTransform(tanh, card.children[0]),
                               hc.animate.move_to(hdr[0]), hh.animate.move_to(hdr[1])], 0.3, 1.0),
                      run_time=2.2)
            c.wait_until("secant")
            self.play(*appear(*card.parents[1:], lag=0.5), run_time=2.0)  # early: the three named in one breath
            c.wait_until("The hyperbolic secant")
            self.born(c, card.parents[1], card.children[1], *card.eq[1], card.nums[1], rt=2.2)
            c.wait_until("cosech")
            self.born(c, card.parents[2], card.children[2], *card.eq[2], card.nums[2], rt=1.8)
            c.wait_until("coth")
            self.born(c, card.parents[3], card.children[3], *card.eq[3], card.nums[3], rt=1.6)
            c.wait_until("one extra letter")
            hs = [card.children[i][0][j] for i, idx in enumerate(CARD_H) for j in idx]
            T_ = min(2.2, c.until())
            dur = 0.5 * T_                               # each h pulses for half the play, staggered
            self.play(*[time_span(pulse(h), k * (T_ - dur) / (len(hs) - 1), k * (T_ - dur) / (len(hs) - 1) + dur) for k, h in enumerate(hs)],
                      run_time=T_)

        # ---------------------------------------------------------------- 4: sech is not cosh^{-1}
        with self.say("c1.family.4", gap=1.1) as c:
            sech = card.children[1]
            others = [m for m in list(card.parents) + list(card.children) + [card.nums[i] for i in (1, 2, 3)]
                      + [hc, hh] if m is not sech]
            self.play(*set_alpha(others, DIMMED), run_time=1.0)
            c.wait_until("The hyperbolic secant")
            tgt = sech.copy().scale(52 / CARD_SIZE)
            at_glyph(tgt, 5, -3.6, 0.6)
            self.play(*during([FadeOut(m) for m in others], 0, 0.45),
                      *during([sech.animate.move_to(tgt.get_center()).scale(52 / CARD_SIZE)], 0.3, 1.0),
                      run_time=1.6)
            inv = inverse_card()
            inv.shift(np.array([3.4, 0.6, 0]) - inv.tex[0][10].get_center() + np.array([0, 0, 0]))
            inv.shift([0, tgt[0][7].get_y() - inv.tex[0][10].get_y(), 0])
            c.wait_until("inv")
            self.play(*appear(inv, shift=None), run_time=1.0)
            c.wait_until("small minus one")
            self.play(FlashAround(G(inv.tex, 4, 6), color=RED, time_width=1.5), run_time=1.4)
            undo = T("the inverse: undoes cosh", 32).next_to(inv, DOWN, buff=0.5)
            ln_line = VGroup(T("built from", 30, DIM), MathTex(r"\ln", font_size=44, color=TEAL))
            ln_line.arrange(RIGHT, buff=0.18).next_to(undo, DOWN, buff=0.3)
            c.wait_until(own_word=undo)
            self.play(*appear(undo), run_time=1.0)
            c.wait_until("logarithms")
            self.play(*appear(ln_line), run_time=0.8)  # early: "built" is paraphrased as "built from logarithms"
            tag = T("Part 3", 30, DIM).next_to(inv, UP, buff=0.2, aligned_edge=RIGHT)
            c.wait_until("later")
            self.play(*appear(tag), run_time=0.8)

        # after the last line: the notes go with the card's move, the card parks in the corner
        small = inv.copy().scale(0.6).to_corner(UR, buff=0.5).shift(0.45 * DOWN)
        self.play(*during(disappear(undo, ln_line), 0, 0.45),
                  *during([inv.animate.scale(0.6).move_to(small),
                           tag.animate.next_to(small, UP, buff=0.15, aligned_edge=RIGHT)], 0.2, 1.0),
                  run_time=1.5)
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
