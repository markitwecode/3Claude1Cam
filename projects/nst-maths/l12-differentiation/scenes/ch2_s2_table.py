"""Chapter 2, scene 2: a short table, and where it comes from. Clips c2.table.1 – c2.table.5.

Exports (reused by ch2_s1 thumbnail, ch2_s6, ch2_s7, ch7_s2):
- table_card(size=44) -> the §4.2 table, full size, centred on ORIGIN. `.header` (y | y′, rules),
  `.blocks[i]` (`.caption`, `.rows`, `.vrule`, `.rule`), `.rows[j]` (0..8) each VGroup(lhs, rhs)
  with `.lhs/.rhs` (MathTex; row 2's lhs is [\\ln(ax), = \\ln a + \\ln x]), `.hrule`, `.pitch`, `.full_w`.
- row_glow(card, j, color=GREEN) -> highlight band behind row j (works at any card scale).
- euler_line(size=48) -> e^{iax} = cos(ax) + i sin(ax), e^{iax} GOLD, every i PINK.
- open_shot() -> the scene's first frame (reversed handover: ch2_s1 ends on it): header and block 1's
  caption at full size, block 1's three left-hand entries faint (DIMMED), no derivatives yet.
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

X0 = -6.4                         # workspace left edge (clips 3-5)
TABLE_POS = np.array([4.15, 0.0, 0])
TABLE_W = 5.0                     # the card's width once shrunk to the right third
BLOCK_DIM = 0.4
OPEN_TOP = 3.7
OPEN_SCALE = 0.9


def mt(*parts, size=44, color=FG):
    """MathTex from pieces; a piece is a tex string or (tex, colour)."""
    strs = [p if isinstance(p, str) else p[0] for p in parts]
    m = MathTex(*strs, font_size=size, color=color)
    for i, p in enumerate(parts):
        if not isinstance(p, str):
            m[i].set_color(p[1])
    return m


def _caption(lines):
    out = VGroup()
    for ln in lines:
        if isinstance(ln, str):
            out.add(T(ln, 30, slant=ITALIC))
        else:
            out.add(VGroup(T(ln[0], 30, slant=ITALIC), mt(("e^{ax}", GOLD), size=36))
                    .arrange(RIGHT, buff=0.14, aligned_edge=DOWN))
    return out.arrange(DOWN, buff=0.12, aligned_edge=LEFT)


def table_card(size=44):
    Y = YELLOW
    spec = [
        (["functions you should know", "how to differentiate"], [
            ([r"x^{a}"], [("a", Y), r"x^{a-1}"]),
            ([("e^{ax}", GOLD)], [("a", Y), ("e^{ax}", GOLD)]),
            ([r"\ln(ax)", r"= \ln a + \ln x"], [r"\frac{1}{x}"]),
        ]),
        (["worth remembering, but can be", ("derived from",)], [
            ([r"\sin(ax)"], [("a", Y), r"\cos(ax)"]),
            ([r"\cos(ax)"], [("-a", Y), r"\sin(ax)"]),
            ([r"\sinh(ax)"], [("a", Y), r"\cosh(ax)"]),
            ([r"\cosh(ax)"], [("a", Y), r"\sinh(ax)"]),
        ]),
        (["worth remembering (but can be derived)"], [
            ([r"\tan(ax)"], [("a", Y), r"\sec^2(ax)"]),
            ([r"\tanh(ax)"], [("a", Y), r"\,\mathrm{sech}^2(ax)"]),
        ]),
    ]
    built = [(_caption(cap), [(mt(*l, size=size), mt(*r, size=size)) for l, r in rows]) for cap, rows in spec]
    maxl = max(l.width for _, rows in built for l, _ in rows)
    maxr = max(r.width for _, rows in built for _, r in rows)
    pad, gap, pitch = 0.3, 0.42, 0.84
    LX, DIV = 0.0, maxl + gap
    RX = DIV + gap
    LE, RE = LX - pad, RX + maxr + pad
    capw = max(c.width for c, _ in built)
    RE = max(RE, LX + capw + pad)

    def hline(y, color=DIM, w=2):
        return Line([LE, y, 0], [RE, y, 0]).set_stroke(color, w)

    def vline(y0, y1):
        return Line([DIV, y0, 0], [DIV, y1, 0]).set_stroke(DIM, 2)

    hy = mt("y", size=size).move_to([LX + maxl / 2, 0, 0])
    hyp = mt("y'", size=size, color=GREEN).move_to([RX + maxr / 2, 0, 0])
    top_rule = hline(0.5, FG, 2.5)
    hrule = hline(-0.5, FG, 2.5)
    header = VGroup(top_rule, hy, hyp, vline(0.5, -0.5), hrule)
    header.hy, header.hyp = hy, hyp
    card = VGroup(header)
    card.header, card.hrule, card.blocks, card.rows = header, hrule, [], []
    cur = -0.5
    for cap, rows in built:
        cap.move_to([LX + cap.width / 2, cur - 0.22 - cap.height / 2, 0])
        cur = cap.get_bottom()[1] - 0.18
        rgs = []
        y0 = cur
        for k, (l, r) in enumerate(rows):
            h = max(pitch, r.height + 0.2, l.height + 0.2)
            y = y0 - h / 2
            y0 -= h
            l.move_to([LX + l.width / 2, y, 0])
            r.move_to([RX + r.width / 2, y, 0])
            rg = VGroup(l, r)
            rg.lhs, rg.rhs, rg.h = l, r, h
            rgs.append(rg)
        y_end = y0
        vr = vline(cur, y_end)
        rule = hline(y_end)
        block = VGroup(cap, vr, *rgs, rule)
        block.caption, block.rows, block.vrule, block.rule = cap, rgs, vr, rule
        cur = y_end
        card.add(block)
        card.blocks.append(block)
        card.rows.extend(rgs)
    card.pitch, card.full_w = pitch, RE - LE
    card.move_to(ORIGIN)
    return card


def row_glow(card, j, color=GREEN):
    w = card.hrule.width
    h = card.rows[j].h * w / card.full_w
    y = card.rows[j].lhs.get_center()[1]
    return (Rectangle(width=w, height=0.94 * h).move_to([card.hrule.get_center()[0], y, 0])
            .set_stroke(color, 2).set_fill(color, 0.16).set_z_index(-1))


def euler_line(size=48):
    m = mt(("e^{iax}", GOLD), "=", r"\cos(ax)", "+", ("i", PINK), r"\sin(ax)", size=size)
    m[0][1].set_color(PINK)
    return m


def _place_open(card):
    card.scale(OPEN_SCALE)
    top = VGroup(card.header, card.blocks[0])
    card.shift([-top.get_center()[0], OPEN_TOP - top.get_top()[1], 0])
    for j in range(3):
        card.rows[j].lhs[0].set_opacity(DIMMED)
    b = card.blocks[0]
    return [card.header, b.caption, b.vrule, b.rule] + [card.rows[j].lhs[0] for j in range(3)]


def open_shot():
    return VGroup(*_place_open(table_card()))


def rt(c, want, nxt=None, frac=0.9, nth=0):
    """run_time: `want`, cut to fit before cue `nxt` (or the clip end)."""
    return max(0.3, min(want, frac * c.until(nxt, nth=nth)))


class TableScene(NarratedScene):
    def construct(self):
        self.card = table_card()
        self.add(*_place_open(self.card))       # opens on open_shot() (ch2_s1 grows its thumbnail into it)
        self.glows = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- c2.table.1
    def clip1(self):
        card = self.card
        r1, r2, r3 = card.rows[:3]
        with self.say("c2.table.1") as c:
            c.wait_until("short table")
            self.play(FlashUnder(card.blocks[0].caption, run_time=2, time_width=1.5))
            c.wait_until("power")
            self.play(*set_alpha([r1.lhs[0]], 1), run_time=rt(c, 0.8, "bring"))
            c.wait_until("bring")
            self.play(*fly(r1.lhs[0][1], r1.rhs[0]), run_time=rt(c, 1.5, "lower it"))
            c.wait_until("lower it")
            self.play(*appear(r1.rhs[1]), run_time=rt(c, 1.0, "exp"))
            c.wait_until("exp")
            self.play(*set_alpha([r2.lhs[0]], 1), run_time=rt(c, 0.8, "gives back"))
            c.wait_until("gives back")
            self.play(*fly(r2.lhs[0], r2.rhs[1]), run_time=rt(c, 1.4, "times that constant"))
            c.wait_until("times that constant")
            self.play(*fly(r2.lhs[0][1], r2.rhs[0], arc=PI / 2), run_time=rt(c, 1.3, "log"))
            c.wait_until("log")
            self.play(*set_alpha([r3.lhs[0]], 1), run_time=rt(c, 0.8, "one over ex"))
            c.wait_until("one over ex")
            self.play(*appear(r3.rhs), run_time=rt(c, 1.0))

    # ---------------------------------------------------------------- c2.table.2
    def clip2(self):
        card = self.card
        r3 = card.rows[2]
        lx = r3.lhs.get_left()[0]
        with self.say("c2.table.2") as c:
            q = T("?", 48, YELLOW).next_to(r3.rhs, RIGHT, buff=0.4)
            self.play(*appear(q), run_time=rt(c, 1.0, "split"))
            c.wait_until("split")
            ex = mt(r"\ln(ax)", "=", r"\ln a", "+", r"\ln x", size=44 * OPEN_SCALE)
            y_ex = card.blocks[0].rule.get_y() - 0.6
            ex.move_to([lx + ex.width / 2, y_ex, 0])
            self.ex = ex
            self.play(*fly(r3.lhs[0], ex[0]), run_time=rt(c, 1.3, "sum of two logs"))
            c.wait_until("sum of two logs")
            self.play(*appear(*ex[1:], lag=0.2), run_time=rt(c, 1.2, "const"))
            c.wait_until("const")
            box = SurroundingRectangle(ex[2], color=YELLOW, buff=0.1)
            self.play(GrowFromCenter(box), run_time=rt(c, 0.8, "just a number"))
            zero = mt("0", size=44).move_to([ex[2].get_x(), y_ex - 1.3, 0])
            a0 = Arrow(box.get_bottom(), zero.get_top(), buff=0.1, stroke_width=3, color=FG,
                       max_tip_length_to_length_ratio=0.35)
            ctag = T("a constant", 30, YELLOW).next_to(a0, LEFT, buff=0.3)
            c.wait_until(own_word=ctag)
            self.play(*appear(ctag), run_time=rt(c, 1.0, "derivative zero"))
            c.wait_until("derivative zero")
            self.play(GrowArrow(a0), *appear(zero), run_time=rt(c, 1.2, "so only"))
            c.wait_until("so only")
            onex = mt(r"\frac{1}{x}", color=GREEN).move_to([ex[4].get_x(), y_ex - 1.4, 0])
            ax_ = Arrow(ex[4].get_bottom(), onex.get_top(), buff=0.1, stroke_width=3, color=GREEN,
                        max_tip_length_to_length_ratio=0.35)
            self.play(GrowArrow(ax_), *appear(onex), run_time=rt(c, 1.2, "is left"))
            ok = check_mark().move_to(q)
            self.play(*swap(q, ok), run_time=rt(c, 1.0, "exists"))
            c.wait_until("exists")
            cond = mt("ax > 0", size=40, color=YELLOW).next_to(ex, RIGHT, buff=1.0)
            self.play(*appear(cond), run_time=rt(c, 1.0, "must be positive"))
            c.wait_until("proof")
            ptag = T("proof: part 3", 30, DIM).next_to(onex, RIGHT, buff=0.45)
            self.play(*appear(ptag), run_time=rt(c, 0.7))  # early: tags the sentence's "prove"
            self.clip2_junk = [ok, box, ctag, a0, zero, ax_, onex, cond, ptag]

    # ---------------------------------------------------------------- c2.table.3
    def clip3(self):
        card = self.card
        r3 = card.rows[2]
        ex = self.ex
        with self.say("c2.table.3") as c:
            # the expansion's "= ln a + ln x" rises into row 3; everything else of the derivation goes
            c.wait_until("the notes say")
            d = r3.lhs[0].get_center() - ex[0].get_center()
            self.play(*during(disappear(*self.clip2_junk, ex[0]), 0, 0.45),
                      *during([p.animate.shift(d) for p in ex[1:]], 0.35, 1), run_time=rt(c, 1.5, "can all"))
            self.remove(*[m for p in ex for m in p.get_family()])
            self.add(r3.lhs[1])
            top = VGroup(card.header, card.blocks[0])
            settle(self, top)
            c.wait_until("can all")
            cc = card.get_center()
            s = min(TABLE_W / card.width, 7.3 / card.height)
            tgt = top.copy().scale(s, about_point=cc).shift(TABLE_POS - cc)
            top.target = tgt
            for b in card.blocks[1:]:
                b.scale(s, about_point=cc).shift(TABLE_POS - cc)
                b.set_opacity(BLOCK_DIM)
            self.play(*during([MoveToTarget(top)], 0, 0.6),
                      *during(appear(card.blocks[1], card.blocks[2], shift=0.3 * UP, lag=0.2), 0.5, 1),  # early: the rest of the table shown whole, then walked
                      run_time=rt(c, 2.2, "hyp"))
            settle(self, card)
            c.wait_until("hyp")
            self.play(*flash([card.rows[5], card.rows[6]]), run_time=rt(c, 1.5, "half the difference"))

            sh = mt(r"\sinh(ax)", "=", r"\tfrac12", r"\big(", ("e^{ax}", GOLD), "-", ("e^{-ax}", PURPLE), r"\big)",
                    size=40)
            sh.move_to([X0 + sh.width / 2, 2.9, 0])
            ch = mt(r"\cosh(ax)", "=", r"\tfrac12", r"\big(", ("e^{ax}", GOLD), "+", ("e^{-ax}", PURPLE), r"\big)",
                    size=40)
            ch.move_to([X0 + ch.width / 2, -0.55, 0])
            c.wait_until("half the difference")
            self.play(*appear(sh), run_time=rt(c, 1.0, "cosh is half"))
            c.wait_until("cosh is half")
            self.play(*appear(ch), run_time=rt(c, 1.0, "diffhyp"))
            c.wait_until("diffhyp")

            def dline(mid, second, y):
                m = mt(r"\frac{d}{dx}", r"\sinh(ax)", "=", r"\tfrac12", r"\big(", *mid, r"\big)", size=40)
                return m.move_to([X0 + m.width / 2, y, 0])

            d0 = dline([("e^{ax}", GOLD), "-", ("e^{-ax}", PURPLE)], None, 1.75)
            derive(self, sh, d0, run_time=rt(c, 2.0, "gives back itself"))
            self.play(FlashAround(d0[5][1], run_time=1.2, time_width=1.5),
                      FlashAround(d0[7][2], run_time=1.2, time_width=1.5))
            d1 = dline([("a", YELLOW), ("e^{ax}", GOLD), "-", ("(-a)", YELLOW), ("e^{-ax}", PURPLE)], None, 1.75)
            self.play(*edit(d0, d1), run_time=rt(c, 1.5, "in the second one"))
            c.wait_until("in the second one")
            self.play(FlashAround(d1[8], run_time=1.5, time_width=1.5))
            c.wait_until("flip")
            d2 = dline([("a", YELLOW), ("e^{ax}", GOLD), ("+", YELLOW), ("a", YELLOW), ("e^{-ax}", PURPLE)], None, 1.75)
            self.play(*edit(d1, d2), run_time=rt(c, 1.5, "the derivative of shine"))
            c.wait_until("the derivative of shine")
            eq1 = mt("=", ("a", YELLOW), r"\cosh(ax)", size=40)
            eq1.shift([d2[2].get_x() - eq1[0].get_x(), 0.75 - eq1.get_y(), 0])
            g6 = row_glow(card, 5)
            self.glows.append(g6)
            self.play(*appear(eq1), *set_alpha([card.rows[5]], 1), FadeIn(g6), run_time=rt(c, 1.2, "cosh"))
            c.wait_until("cosh")
            c1 = mt(r"\frac{d}{dx}", r"\cosh(ax)", "=", r"\tfrac12", r"\big(", ("a", YELLOW), ("e^{ax}", GOLD), "-",
                    ("a", YELLOW), ("e^{-ax}", PURPLE), r"\big)", size=40)
            c1.move_to([X0 + c1.width / 2, -1.7, 0])
            derive(self, ch, c1, run_time=rt(c, 1.8))
            self.wait(0.3)
            eq2 = mt("=", ("a", YELLOW), r"\sinh(ax)", size=40)
            eq2.shift([c1[2].get_x() - eq2[0].get_x(), -2.7 - eq2.get_y(), 0])
            g7 = row_glow(card, 6)
            self.glows.append(g7)
            self.play(*appear(eq2), *set_alpha([card.rows[6]], 1), FadeIn(g7), run_time=rt(c, 1.2))

    # ---------------------------------------------------------------- c2.table.4
    def clip4(self):
        card = self.card
        r4, r5 = card.rows[3], card.rows[4]
        with self.say("c2.table.4") as c:
            self.play(*flash([r4, r5]), run_time=rt(c, 1.5, "lecture ten"))
            c.wait_until("lecture ten")
            sweep_clear(self, keep=[card, *self.glows], run_time=rt(c, 1.0, "euler"))
            c.wait_until("euler")
            eut = mt(("e^{i\\theta}", GOLD), "=", r"\cos\theta", "+", ("i", PINK), r"\sin\theta", size=48)
            eut[0][1].set_color(PINK)
            eut.move_to([X0 + eut.width / 2, 3.1, 0])
            self.play(*appear(eut), run_time=rt(c, 1.0, "the constant times"))
            c.wait_until("the constant times")
            eu = euler_line(48)
            eu.move_to([X0 + eu.width / 2, 3.1, 0])
            self.play(*edit(eut, eu), run_time=rt(c, 1.5, "left"))
            c.wait_until("left")
            dl = mt(r"\frac{d}{dx}", ("e^{iax}", GOLD), "=", ("i", PINK), ("a", YELLOW), ("e^{iax}", GOLD))
            dl[1][1].set_color(PINK)
            dl[5][1].set_color(PINK)
            dl.move_to([X0 + dl.width / 2, 1.95, 0])
            # the two sides as separate texts (same TeX run, so the same spacing), so the ia can fly across
            dll = [mt(r"\frac{d}{dx}"), mt(("e^{iax}", GOLD)), mt("=")]
            dll[1][0][1].set_color(PINK)
            for k, m in zip((0, 1, 2), dll):
                m.move_to(dl[k])
            dlr = mt(("i", PINK), ("a", YELLOW), ("e^{iax}", GOLD))
            dlr[2][1].set_color(PINK)
            dlr.shift(dl[3].get_center() - dlr[0].get_center())
            self.play(*fly(eu[0], dll[1]), *during(appear(dll[0], dll[2]), 0.4, 1), run_time=rt(c, 1.5, "brings out"))
            c.wait_until("brings out")
            self.play(*flash([dll[1][0][1], dll[1][0][2]]), run_time=rt(c, 1.0, "expand"))
            self.play(*fly(dll[1], dlr[2], arc=0.8 * PI), run_time=rt(c, 1.2, "expand"))
            self.play(*appear(dlr[0], dlr[1], shift=0.25 * DOWN), run_time=rt(c, 0.8, "expand"))
            settle(self, dlr)
            c.wait_until("expand")
            exl = mt(("i", PINK), ("a", YELLOW), r"\big(", r"\cos ax", "+", ("i", PINK), r"\sin ax", r"\big)",
                     "=", ("-a", YELLOW), r"\sin ax", "+", ("i", PINK), ("a", YELLOW), r"\cos ax", size=38)
            exl.move_to([X0 + exl.width / 2, 0.8, 0])
            self.play(*appear(*exl[:8], lag=0.05), run_time=rt(c, 1.2, "eye times eye"))
            c.wait_until("eye times eye")
            self.play(*flash([exl[0], exl[5]]), *recolor([exl[0], exl[5]], YELLOW), run_time=rt(c, 1.2, "minus one"))
            ii = mt(r"i \cdot i = -1", size=38, color=YELLOW).next_to(dl, RIGHT, buff=0.7)
            c.wait_until("minus one")
            self.play(*appear(ii), run_time=rt(c, 1.0, "so the real part"))
            c.wait_until("so the real part")
            self.play(*appear(*exl[8:11], lag=0.15), *recolor([exl[0], exl[5]], PINK),
                      run_time=rt(c, 1.1, "and the imaginary"))
            c.wait_until("and the imaginary")
            self.play(*appear(*exl[11:], lag=0.15), run_time=rt(c, 1.1, "match"))
            settle(self, exl)
            c.wait_until("match")
            ma = mt("=", r"\frac{d}{dx}\cos(ax)", "+", ("i", PINK), r"\frac{d}{dx}\sin(ax)", size=40)
            ma.move_to([X0 + 0.5 + ma.width / 2, -0.4, 0])
            self.play(*appear(ma[0], ma[1]), run_time=rt(c, 1.1, "and the imaginary part", nth=1))
            c.wait_until("and the imaginary part", nth=1)
            self.play(*appear(ma[2], ma[3], ma[4]), run_time=rt(c, 1.1, "pair"))
            settle(self, ma)
            c.wait_until("pair")
            re_top = VGroup(*exl[9:11])
            im_top = VGroup(*exl[12:15])
            im_bot = VGroup(*ma[3:5])
            l_re = Line(re_top.get_bottom() + 0.08 * DOWN, ma[1].get_top() + 0.08 * UP).set_stroke(FG, 4)
            l_im = Line(im_top.get_bottom() + 0.08 * DOWN, im_bot.get_top() + 0.08 * UP).set_stroke(PINK, 4)
            self.play(Create(l_re), Create(l_im), run_time=rt(c, 1.0, "both rules"))
            q1 = mt(r"\frac{d}{dx}\cos(ax)", "=", ("-a", YELLOW), r"\sin(ax)", size=40)
            q2 = mt(r"\frac{d}{dx}\sin(ax)", "=", ("a", YELLOW), r"\cos(ax)", size=40)
            q1.move_to([X0 + q1.width / 2, -1.8, 0])
            q2.move_to([X0 + q2.width / 2, -2.85, 0])
            g4, g5 = row_glow(card, 3), row_glow(card, 4)
            self.glows += [g4, g5]
            self.q12 = [q1, q2]
            self.play(*appear(q1, q2, lag=0.3), *set_alpha([r4, r5], 1), FadeIn(g4), FadeIn(g5),
                      run_time=rt(c, 1.6))

    # ---------------------------------------------------------------- c2.table.5
    def clip5(self):
        card = self.card
        with self.say("c2.table.5") as c:
            l1 = mt(r"\cos(ix) = \cosh x", size=36)
            l1[0][4].set_color(PINK)
            l2 = mt(r"\sin(ix) = i\sinh x", size=36)
            l2[0][4].set_color(PINK)
            l2[0][8].set_color(PINK)
            lines = VGroup(l1, l2).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            l2.shift((l1[0][7].get_x() - l2[0][7].get_x()) * RIGHT)       # align the = signs
            frame = SurroundingRectangle(lines, color=DIM, buff=0.3, corner_radius=0.12).set_stroke(DIM, 2)
            dcard = VGroup(frame, lines)
            dcard.move_to([X0 + dcard.width / 2, 3.55 - dcard.height / 2, 0])
            sweep_clear(self, *appear(dcard), keep=[card, *self.glows, *self.q12],
                        run_time=rt(c, 1.6, "cosine of eye"))
            c.wait_until("cosine of eye")
            self.play(FlashAround(l1, run_time=1.5, time_width=1.5))
            c.wait_until("so the cosine rule")
            self.play(FlashAround(self.q12[0], run_time=1.2, time_width=1.5))
            dv1 = mt(r"\frac{d}{dx}\cos(", ("i", PINK), "x)", "=", "-", ("i", PINK), r"\sin(", ("i", PINK), "x)")
            dv1.move_to([X0 + dv1.width / 2, 0.55, 0])
            dv2 = mt("=", "-", ("i", PINK), r"\cdot", ("i", PINK), r"\sinh x", "=", (r"\sinh x", GREEN))
            dv2.shift([dv1[3].get_x() - dv2[0].get_x(), -0.6 - dv2.get_y(), 0])
            self.play(*appear(dv1), run_time=rt(c, 1.1, "turns into"))
            c.wait_until("turns into")
            self.play(*appear(dv2), FlashAround(card.rows[6], run_time=1.5, time_width=1.5),
                      run_time=rt(c, 1.5, "tan"))
            c.wait_until("tan")
            b3 = card.blocks[2]
            self.play(*set_alpha(b3.rows, 1), *flash(b3.rows), *disappear(*self.q12),
                      run_time=rt(c, 1.5, "quotient rule"))
            ql = T("quotient rule, later in this part", 30, YELLOW)
            tip = np.array([card.hrule.get_left()[0] - 0.12, VGroup(*b3.rows).get_center()[1], 0])
            ql.move_to(tip + (0.75 + ql.width / 2) * LEFT)
            qa = Arrow(ql.get_right(), tip, buff=0.12, stroke_width=3, color=YELLOW,
                       max_tip_length_to_length_ratio=0.35)
            qtag = VGroup(ql, qa)
            c.wait_until(own_word=qtag[0])
            self.play(*appear(qtag), run_time=rt(c, 1.0, "sheet"))
            c.wait_until("sheet")
            st = VGroup(T("Examples Sheet I · H2:", 32), T("write in exponentials", 30, DIM)) \
                .arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            sf = SurroundingRectangle(st, color=BLUE, buff=0.28, corner_radius=0.12).set_stroke(BLUE, 2)
            sheet = VGroup(sf, st)
            sheet.move_to([X0 + sheet.width / 2, -1.95, 0])
            self.play(*appear(sheet), run_time=rt(c, 0.8))  # early: the sheet card shown as the sentence names it
