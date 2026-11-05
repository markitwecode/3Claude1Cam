"""Chapter 7, scene 2: H1 and H2, the basic skills. Clips c7.basics.1 – c7.basics.5.

Opens on ch7_s1's handover_shot() (the lit card row): card H1 grows out of the row next to ch2 s2's
table; the printed answers drop in under the parts; the power-rule row glows. (e), (f), (g) gather
in a left column and are worked at the right. H2's card arrives with the table (empty tick boxes on
rows sin..tanh), collapses to a strip of its printed answers, and every derivation ticks its row
and its answer. Ends on an empty frame.

Shared (load_scene("ch7_s2_basics")):
  placed_table()     ch2 s2's table_card(), scaled to 6.6 tall, at the left (x ~ -6.6..-2.1)
  tick_boxes(table)  empty DIM boxes right of rows 3..8 (sin, cos, sinh, cosh, tan, tanh); dict row -> box
  tick(box)          the GREEN check mark in a box
  ticked_table()     VGroup(table, boxes, ticks) with every box ticked; .table .boxes .ticks
  sin_line(size=44)  sin x = (e^{ix} - e^{-ix})/(2i), e^{ix} GOLD, e^{-ix} PURPLE, i PINK
  variable_tags()    VGroup of three VGroup(symbol, "variable") for t, y, omega, all YELLOW
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

_s1 = load_scene("ch7_s1_intro")
_t22 = load_scene("ch2_s2_table")
_q26 = load_scene("ch2_s6_quotient")
table_card, row_glow = _t22.table_card, _t22.row_glow

TABLE_H = 6.6
TABLE_LEFT = -6.6
CARD_S = 0.78
CARD_RIGHT = 6.6
WX = 2.6                 # workspace centre x (right of the table)
STRIP_Y = (3.45, 2.9)
Y_ = YELLOW

H1_ANS = ["2x", "4x^3+2", "anx^{n-1}+b", "e^x", r"a+2bt\sin\theta", "2x^{-1/3}/3",
          "-(1+y)^{-2}", "1/x"]
H2_ANS = [r"\cos x", r"-\sin\theta", r"\sec^2 t", r"-it\cos(-i\omega t)", r"\cosh x", r"\sinh x",
          r"\mathrm{sech}^2 x", r"2\,\mathrm{sech}^2 2x"]


# ------------------------------------------------------------------ helpers

def X(*parts, size=44, color=FG):
    """MathTex from pieces; a piece is a tex string or (tex, colour). m[i] is piece i."""
    strs = [p if isinstance(p, str) else p[0] for p in parts]
    m = MathTex(*strs, font_size=size, color=color)
    for i, p in enumerate(parts):
        if not isinstance(p, str):
            m[i].set_color(p[1])
    return m


def placed_table():
    t = table_card()
    t.scale(TABLE_H / t.height)
    t.move_to([TABLE_LEFT + t.width / 2, 0, 0])
    return t


def tick_boxes(table):
    x = table.get_right()[0] + 0.32
    out = {}
    for j in range(3, 9):
        y = table.rows[j].lhs.get_center()[1]
        out[j] = Square(0.34).set_stroke(DIM, 2).set_fill(opacity=0).move_to([x, y, 0])
    return out


def tick(box):
    return check_mark(GREEN).scale(0.62).set_stroke(width=6).move_to(box)


def ticked_table():
    t = placed_table()
    boxes = tick_boxes(t)
    ticks = {j: tick(b) for j, b in boxes.items()}
    g = VGroup(t, *boxes.values(), *ticks.values())
    g.table, g.boxes, g.ticks = t, boxes, ticks
    return g


def sin_line(size=44):
    m = X(r"\sin x =", r"\frac{", ("e^{ix}", GOLD), "-", ("e^{-ix}", PURPLE), "}{2", ("i", PINK), "}",
          size=size)
    m[2][1].set_color(PINK)
    m[4][2].set_color(PINK)
    return m


def var_tag(color=YELLOW, text="variable"):
    return T(text, 30, color)


def variable_tags():
    out = VGroup()
    for s in ("t", "y", r"\omega"):
        sym = MathTex(s, font_size=48, color=YELLOW)
        out.add(VGroup(sym, var_tag().next_to(sym, DOWN, buff=0.2)))
    return out.arrange(RIGHT, buff=0.8)


def answered_card(maker, answers):
    """The card spread to leave a line under each part, its printed answers (GREEN) there; scaled,
    at the right. .core = VGroup(frame, label, body) (same family as maker()), .answers."""
    card = maker()
    parts = card.parts
    D = 0.55
    nrows = len(parts) // 2
    for r in range(nrows):
        for k in (2 * r, 2 * r + 1):
            parts[k].shift(r * D * DOWN)
    ans = []
    for r in range(nrows):
        bot = min(parts[2 * r].get_bottom()[1], parts[2 * r + 1].get_bottom()[1])
        for k in (2 * r, 2 * r + 1):
            a = MathTex(answers[k], font_size=40, color=GREEN)
            a.move_to([0, bot - 0.14 - a.height / 2, 0]).align_to(parts[k][0][3], LEFT)
            ans.append(a)
    fr = card.frame
    new = RoundedRectangle(corner_radius=0.2, width=fr.width, height=fr.height + nrows * D)
    new.set_stroke(DIM, 2).set_fill(opacity=0).align_to(fr, UP).set_x(fr.get_x())
    fr.become(new)
    card.add(VGroup(*ans))
    card.scale(CARD_S)
    card.move_to([CARD_RIGHT - card.width / 2, 0, 0])
    card.answers = ans
    card.core = VGroup(card.frame, card.label, card.body)
    return card


def rt(c, want, nxt=None, frac=0.9, nth=0):
    return max(0.3, min(want, frac * c.until(nxt, nth=nth)))


def align_eq(line, eq_glyph, ref_glyph):
    line.shift((ref_glyph.get_x() - eq_glyph.get_x()) * RIGHT)
    return line


# ------------------------------------------------------------------ the scene

class Ch7S2Basics(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------------- H1
    def clip1(self):
        row = _s1.handover_shot()
        self.add(row)
        table = placed_table()
        h1 = answered_card(_s1.h1_card, H1_ANS)
        plain = _s1.h1_card().scale(CARD_S)
        plain.move_to(h1.get_x() * RIGHT).align_to(h1, UP)
        with self.say("c7.basics.1") as c:
            self.play(*during(disappear(row[1], row[2], row[3]), 0, 0.4),  # early: the table is shown whole, then walked
                      *during([Transform(row[0], plain)], 0.15, 0.8),
                      *during(appear(table, shift=None), 0.55, 1),
                      run_time=rt(c, 2.4, "printed"))
            c.wait_until("printed")
            card = row[0]
            self.play(Transform(card, h1.core), run_time=rt(c, 1.0, "power", 0.4))
            self.remove(card)
            self.frame_, self.label_, self.intro_ = card.frame, card.label, card.intro
            self.parts_ = list(card.parts)
            self.add(self.frame_, self.label_, self.intro_, *self.parts_)
            self.ans_ = h1.answers
            self.play(*appear(*self.ans_, lag=0.15), run_time=rt(c, 1.6, "power"))
            c.wait_until("power")
            glow = row_glow(table, 0, YELLOW)
            src = np.array([table.hrule.get_right()[0] + 0.05, glow.get_y(), 0])
            P, A = self.parts_, self.ans_
            xl = self.frame_.get_left()[0] + 0.06
            xg = P[1].get_left()[0] - 0.22

            def route(k, gap_y):
                end = P[k].get_left() + 0.08 * LEFT
                if gap_y is None:
                    pts = [src, end]
                else:
                    pts = [src, [xl, gap_y, 0], [xg, gap_y, 0], [xg, end[1], 0], end]
                return VMobject().set_points_as_corners([np.array(q) for q in pts]).set_stroke(YELLOW, 2, 0.7)

            g0 = (self.intro_.get_bottom()[1] + max(P[0].get_top()[1], P[1].get_top()[1])) / 2
            g2 = (min(A[2].get_bottom()[1], A[3].get_bottom()[1]) + max(P[4].get_top()[1], P[5].get_top()[1])) / 2
            lines = [route(0, None), route(1, g0), route(2, None), route(5, g2)]
            for ln in lines:
                ln.set_z_index(-2)
            self.play(FadeIn(glow), run_time=rt(c, 0.8, "three of them", 0.3))
            self.play(*[Create(ln) for ln in lines], *recolor([g for k in (0, 1, 2, 5) for g in self.parts_[k][0][:3]], YELLOW),
                      run_time=rt(c, 1.5, "three of them", 0.5))
            c.wait_until("three of them")
            keep = (4, 5, 6)
            gone = [table, glow, *lines, self.frame_, self.label_, self.intro_]
            gone += [self.parts_[k] for k in range(8) if k not in keep]
            gone += [self.ans_[k] for k in range(8) if k not in keep]
            self.play(*disappear(*gone), run_time=rt(c, 0.9, None, 0.4))
            # the three gather in a left column
            k_s = 36 / (40 * CARD_S)
            self.col = []
            anims_eg, anims_f = [], []
            for n, k in enumerate(keep):
                p, a = self.parts_[k], self.ans_[k]
                tp = p.copy().scale(k_s)
                ta = a.copy().scale(k_s)
                off = (a.get_center() - p.get_center()) * k_s
                tp.move_to([-6.4 + tp.width / 2, 2.1 - 2.0 * n, 0])
                ta.move_to(tp.get_center() + off)
                ta.align_to(tp[0][3], LEFT)
                an = [Transform(p, tp), Transform(a, ta)]
                (anims_f if k == 5 else anims_eg).extend(an)
                self.col.append((p, a, VGroup(tp, ta)))
            self.play(*during(anims_eg, 0, 0.6), *during(anims_f, 0.4, 1), run_time=rt(c, 1.4, None, 0.95))

    # -------------------------------------------------------------- (e) (f) (g)
    def clip2(self):
        def hbox(n):
            return (SurroundingRectangle(self.col[n][2], color=YELLOW, buff=0.15, corner_radius=0.1)
                    .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.06).set_z_index(-1))

        with self.say("c7.basics.2") as c:
            # (e): t is the variable
            box = hbox(0)
            e1 = X(r"\frac{d}{dt}", r"\big(a", "t", "+b", "t^2", r"\sin\theta", r"\big)", size=52)
            e1.move_to([WX, 1.5, 0])
            self.play(FadeIn(box), *during(appear(e1), 0.3, 1), run_time=rt(c, 1.5, "time t", 0.9))
            c.wait_until("time t")
            vt = var_tag().next_to(e1[2], DOWN, buff=0.35)
            self.play(*recolor([e1[2], e1[4][0], e1[0][-1]], YELLOW), *appear(vt),
                      run_time=rt(c, 1.0, "theta is a constant"))
            c.wait_until("theta is a constant")
            ct = var_tag(DIM, "constant").next_to(e1[5], DOWN, buff=0.35)
            self.play(e1[5].animate.set_color(DIM), *appear(ct), run_time=rt(c, 1.0, "just a number"))
            c.wait_until("just a number")
            e2 = X("=", "a+2b", ("t", Y_), (r"\sin\theta", DIM), size=52)
            e2.next_to(e1, DOWN, buff=1.25).align_to(e1[1], LEFT)
            self.play(*appear(e2), run_time=rt(c, 1.0, "frac", 0.5))
            self.play(*flash([self.col[0][1]], GREEN), run_time=rt(c, 1.2, "frac", 0.8))
            c.wait_until("frac")
            # (f): a fractional power
            f1 = X(r"\frac{d}{dx}", "x^{2/3}", "=", (r"\tfrac{2}{3}", Y_), "x^{2/3-1}", size=52)
            f1.move_to([WX, 1.2, 0])
            self.play(*during(disappear(e1, e2, vt, ct), 0, 0.45),
                      *during([Transform(box, hbox(1))], 0.2, 0.8),
                      *during(appear(f1), 0.5, 1), run_time=rt(c, 1.6, "two thirds", nth=1))
            c.wait_until("two thirds", nth=1)
            f2 = X("=", (r"\tfrac{2}{3}", Y_), "x^{-1/3}", size=52)
            align_eq(f2, f2[0], f1[2]).set_y(-0.5)
            f3e = MathTex("=", font_size=52).move_to([f1[2].get_x(), -2.0, 0])
            f3 = MathTex("2x^{-1/3}/3", font_size=52, color=GREEN).next_to(f3e, RIGHT, buff=0.2)
            self.play(*appear(f2), run_time=rt(c, 1.2, "minus one third"))
            c.wait_until("minus one third")
            self.play(*fly(self.col[1][1], f3), *during(appear(f3e, shift=None), 0.8, 1), run_time=rt(c, 1.4, "wy", 0.8))
            c.wait_until("wy")
            # (g): y is the variable
            g1 = X(r"\frac{d}{d", ("y", Y_), "}", r"\frac{1}{1+", ("y", Y_), "}", size=52)
            g1.move_to([WX, 1.6, 0])
            vy = var_tag().next_to(g1, DOWN, buff=0.3).set_x(g1[4].get_x())
            self.play(*during(disappear(f1, f2, f3e, f3), 0, 0.45),
                      *during([Transform(box, hbox(2))], 0.2, 0.8),
                      *during(appear(g1), 0.5, 1), run_time=rt(c, 1.6, "is why"))
            c.wait_until(own_word=vy)
            self.play(*appear(vy), run_time=rt(c, 1.0, "one over"))
            c.wait_until("one over")
            g2 = X(r"\frac{1}{1+", ("y", Y_), "}", "=", "(1+", ("y", Y_), ")^{-1}", size=52)
            g2.move_to([WX, -0.5, 0])
            self.play(*appear(g2), run_time=rt(c, 1.2, "so its derivative"))
            c.wait_until("so its derivative")
            g3 = X(r"\frac{d}{d", ("y", Y_), "}", "(1+", ("y", Y_), ")^{-1}", "=", "-(1+", ("y", Y_), ")^{-2}",
                   size=52)
            g3.move_to([WX, -2.2, 0])
            self.play(*appear(g3), run_time=rt(c, 1.2))
            self.play(*flash([self.col[2][1]], GREEN), run_time=rt(c, 1.2))
            self.work_ = [g1, g2, g3, vy, box]

    # -------------------------------------------------------------- H2: sin, cos, sinh, cosh
    def clip3(self):
        table = placed_table()
        boxes = tick_boxes(table)
        h2 = answered_card(_s1.h2_card, H2_ANS)
        self.table, self.boxes = table, boxes
        with self.say("c7.basics.3") as c:
            sweep_clear(self, *appear(table, *boxes.values(), shift=None, lag=0.05),
                        *appear(h2, shift=None), run_time=rt(c, 2.2, "write each"))
            self.remove(h2)
            pieces = [h2.frame, h2.label, h2.intro, *h2.parts]
            self.add(*pieces, *h2.answers)
            c.wait_until("sin")
            # collapse the card to a strip of its answers along the top
            items, labs = [], []
            for i, s in enumerate(H2_ANS):
                lab = Tex(f"({'abcdefgh'[i]})", font_size=30, color=DIM)
                a = MathTex(s, font_size=30, color=GREEN)
                items.append(VGroup(lab, a).arrange(RIGHT, buff=0.12))
                labs.append(lab)
            rows = [VGroup(*items[:4]).arrange(RIGHT, buff=0.45), VGroup(*items[4:]).arrange(RIGHT, buff=0.45)]
            for r, y in zip(rows, STRIP_Y):
                r.move_to([WX, y, 0])
            w = max(r.width for r in rows)
            if w > 7.9:
                for r in rows:
                    r.scale(7.9 / w)
            self.items = items
            self.strip_ans = h2.answers
            l1 = sin_line(48).move_to([WX, 1.25, 0])
            self.play(*during(disappear(*pieces), 0, 0.4),
                      *during([Transform(h2.answers[i], items[i][1]) for i in range(8)], 0.35, 0.85),
                      *during(appear(*labs, shift=None, lag=0.05), 0.55, 1),
                      *during(appear(l1), 0.7, 1), run_time=rt(c, 2.4, "down"))
            c.wait_until("down")
            l2 = X(r"\frac{d}{dx}\sin x =", r"\frac{", ("i", PINK), ("e^{ix}", GOLD), "-", r"(", ("-i", PINK),
                   ")", ("e^{-ix}", PURPLE), "}{2", ("i", PINK), "}", size=48)
            l2[3][1].set_color(PINK)
            l2[8][2].set_color(PINK)
            align_eq(l2, l2[0][-1], l1[0][-1]).set_y(-0.4)
            derive(self, l1, l2, run_time=rt(c, 2.0, "and minus eye"))
            c.wait_until("and minus eye")
            self.play(*flash([l2[2]], PINK), run_time=rt(c, 1.0, "cancel", 0.5))
            self.play(*flash([l2[6]], PINK), run_time=rt(c, 1.0, "cancel", 0.8))
            c.wait_until("cancel")
            l3 = X("=", r"\frac{", ("e^{ix}", GOLD), "+", ("e^{-ix}", PURPLE), "}{2}", "=", r"\cos x", size=48)
            l3[2][1].set_color(PINK)
            l3[4][2].set_color(PINK)
            align_eq(l3, l3[0], l2[0][-1]).set_y(-2.1)
            self.play(*appear(l3), run_time=rt(c, 1.4, "cosine of ex"))
            c.wait_until("cosine of ex")
            self.play(*self.done(3, 0), run_time=rt(c, 1.0, "rest"))
            c.wait_until("rest")
            # the rest, quickly
            lc = X(r"\cos\theta", r"\;\to\;", r"-\sin\theta", size=48).move_to([WX, 1.3, 0])
            self.play(*during(disappear(l1, l2, l3), 0, 0.4), *during(appear(lc), 0.5, 1),
                      run_time=rt(c, 1.4, "to minus sine"))
            c.wait_until("to minus sine")
            self.play(*self.done(4, 1), run_time=rt(c, 0.8, "shine"))
            c.wait_until("shine")
            ls = X(r"\tfrac12(", ("e^x", GOLD), "-", ("e^{-x}", PURPLE), ")", r"\;\to\;",
                   r"\tfrac12(", ("e^x", GOLD), "+", ("e^{-x}", PURPLE), ")", size=48).move_to([WX, 0.0, 0])
            self.play(*appear(ls), *self.done(5, 4), run_time=rt(c, 1.2, "cosh", nth=1))
            c.wait_until("cosh", nth=1)
            lh = X(r"\tfrac12(", ("e^x", GOLD), "+", ("e^{-x}", PURPLE), ")", r"\;\to\;",
                   r"\tfrac12(", ("e^x", GOLD), "-", ("e^{-x}", PURPLE), ")", size=48).move_to([WX, -1.3, 0])
            self.play(*appear(lh), run_time=rt(c, 1.0, "to shine"))
            c.wait_until("to shine")
            self.play(*self.done(6, 5), run_time=rt(c, 0.8))
            self.work_ = [lc, ls, lh]

    def done(self, j, i):
        """Tick table row j (or none) and printed answer i."""
        out = []
        if j is not None:
            out.append(GrowFromCenter(tick(self.boxes[j])))
        ab = (SurroundingRectangle(self.items[i], color=GREEN, buff=0.08, corner_radius=0.08)
              .set_stroke(GREEN, 2).set_fill(GREEN, 0.12).set_z_index(-1))
        out.append(FadeIn(ab))
        return out

    # -------------------------------------------------------------- tanh, tan, tanh 2x
    def clip4(self):
        with self.say("c7.basics.4") as c:
            t1 = X(r"\tanh x =", r"\frac{", ("e^x", GOLD), "-", ("e^{-x}", PURPLE), "}{", ("e^x", GOLD), "+",
                   ("e^{-x}", PURPLE), "}", size=48)
            t1.move_to([WX - 0.9, 1.4, 0])
            self.play(*during(disappear(*self.work_), 0, 0.4), *during(appear(t1), 0.5, 1),
                      run_time=rt(c, 1.5, "swap"))
            c.wait_until("swap")
            num = VGroup(t1[2], t1[3], t1[4])
            den = VGroup(t1[6], t1[7], t1[8])
            tx = t1.get_right()[0] + 1.0
            top = T("top", 30, YELLOW).move_to([tx, num.get_y(), 0], aligned_edge=LEFT)
            bot = T("bottom", 30, YELLOW).move_to([tx, den.get_y(), 0], aligned_edge=LEFT)
            self.play(*appear(top, bot, lag=0.4), run_time=rt(c, 1.0, "and the bottom"))
            a1 = CurvedArrow(top.get_right() + 0.15 * RIGHT, bot.get_right() + 0.15 * RIGHT + 0.05 * UP,
                             angle=-PI * 0.75, color=YELLOW, stroke_width=3, tip_length=0.18)
            a2 = CurvedArrow(bot.get_left() + 0.15 * LEFT, top.get_left() + 0.15 * LEFT + 0.05 * DOWN,
                             angle=-PI * 0.75, color=YELLOW, stroke_width=3, tip_length=0.18)
            self.play(Create(a1), run_time=rt(c, 0.9, "and the bottom"))
            c.wait_until("and the bottom")
            self.play(Create(a2), run_time=rt(c, 1.0, "qrule"))
            c.wait_until("qrule")
            qb = _q26.quotient_box(36)
            qb.move_to([WX, -0.75, 0])
            self.play(*appear(qb, shift=None), run_time=rt(c, 1.0, "over the bottom squared", 0.4))
            c.wait_until("minus the top")
            B, Tp = r"\text{bottom}^2", r"\text{top}^2"
            fl = X(r"\frac{d}{dx}\tanh x =", r"\frac{", (B, Y_), "-", (Tp, Y_), "}{", (B, Y_), "}", size=44)
            fl.move_to([WX, -2.75, 0])
            self.play(*appear(fl), run_time=rt(c, 1.2, "four"))
            c.wait_until("four")
            # the squares differ by four
            fa = X("(", ("e^{2x}", GOLD), "+2+", ("e^{-2x}", PURPLE), ")-(", ("e^{2x}", GOLD), "-2+",
                   ("e^{-2x}", PURPLE), ")", "=", "4", size=40).move_to([WX, 0.15, 0])
            self.play(*during(disappear(t1, top, bot, a1, a2, qb), 0, 0.45),
                      *during([fl.animate.move_to([WX, 1.5, 0])], 0.3, 0.85),
                      *during(appear(fa), 0.6, 1), run_time=rt(c, 2.0, "and the bottom is"))
            c.wait_until("and the bottom is")
            fb = X(r"\text{bottom} =", ("e^x", GOLD), "+", ("e^{-x}", PURPLE), r"= 2\cosh x", size=40)
            fb.move_to([WX, -0.85, 0])
            self.play(*appear(fb), run_time=rt(c, 1.0, "so that's"))
            c.wait_until("so that's")
            fc = X(r"\frac{4}{(2\cosh x)^2}", "=", r"\frac{1}{\cosh^2 x}", "=", (r"\mathrm{sech}^2 x", GREEN),
                   size=44)
            fc.move_to([WX, -2.3, 0])
            self.play(*appear(fc), run_time=rt(c, 1.4, "secant squared"))
            c.wait_until("secant squared")
            self.play(*self.done(8, 6), run_time=rt(c, 0.9, "tan"))
            c.wait_until("tan")
            ta = X(r"\tan t =", r"\frac{", ("e^{it}", GOLD), "-", ("e^{-it}", PURPLE), "}{", ("i", PINK), "(",
                   ("e^{it}", GOLD), "+", ("e^{-it}", PURPLE), ")}", r"\;\to\;", (r"\sec^2 t", GREEN), size=48)
            for k in (2, 8):
                ta[k][1].set_color(PINK)
            for k in (4, 10):
                ta[k][2].set_color(PINK)
            ta.move_to([WX, 0.9, 0])
            self.play(*during(disappear(fl, fa, fb, fc), 0, 0.4), *during(appear(ta), 0.5, 1),
                      run_time=rt(c, 1.5, "secant squared", nth=1, frac=0.95))
            self.play(*self.done(7, 2), run_time=rt(c, 0.8, "chain"))
            c.wait_until("chain")
            ch = X(r"\tanh 2x", r"\;\to\;", ("2", Y_), r"\,\mathrm{sech}^2 2x", size=48).move_to([WX, -1.2, 0])
            self.play(*appear(ch), run_time=rt(c, 1.2, "factor of two"))
            c.wait_until("factor of two")
            self.play(*flash([ch[2]], YELLOW), *self.done(None, 7), run_time=rt(c, 1.0))
            self.work_ = [ta, ch]

    # -------------------------------------------------------------- (d): the omega trap
    def clip5(self):
        with self.say("c7.basics.5") as c:
            q = X(r"\frac{d}{d", (r"\omega", Y_), "}", r"\sin(-", ("i", PINK), (r"\omega", Y_), ("t", DIM), ")",
                  size=52).move_to([WX, 2.0, 0])
            self.play(*during(disappear(*self.work_), 0, 0.4), *during(appear(q), 0.5, 1),
                      run_time=rt(c, 1.5, "omega", nth=1))
            c.wait_until("omega", nth=1)
            vw = var_tag().next_to(q[1], DOWN, buff=0.3)
            vc = var_tag(DIM, "constant").next_to(q[6], DOWN, buff=0.3)
            self.play(*appear(vw, vc, lag=0.4), run_time=rt(c, 1.2, "dict"))  # early: tags name roles, never said
            c.wait_until("dict")
            d1 = X(("i", PINK), r"\cdot(-", ("i", PINK), r"\omega t) = \omega t", size=44).move_to([WX, 0.55, 0])
            self.play(*appear(d1), run_time=rt(c, 1.2, "so the sine"))
            c.wait_until("so the sine")
            d2 = X(r"\sin(-", ("i", PINK), r"\omega t) =", r"\frac{", (r"e^{\omega t}", GOLD), "-",
                   (r"e^{-\omega t}", PURPLE), "}{2", ("i", PINK), "}", "=", r"\frac{\sinh(\omega t)}{", ("i", PINK),
                   "}", size=44).move_to([WX, -0.85, 0])
            self.play(*appear(d2), run_time=rt(c, 1.5, "that's minus eye"))
            c.wait_until("that's minus eye")
            d3 = X(r"\sin(-", ("i", PINK), r"\omega t) = -", ("i", PINK), r"\sinh(\omega t)", size=44)
            align_eq(d3, d3[2][-2], d2[2][-1]).set_y(-2.35)
            self.play(*appear(d3), run_time=rt(c, 1.2, "wrt"))
            c.wait_until("wrt")
            self.play(*during(disappear(d1, d2), 0, 0.45),
                      *during([d3.animate.set_y(0.5)], 0.35, 1), run_time=rt(c, 1.5, "minus eye t"))
            c.wait_until("minus eye t")
            r = X("-", ("i", PINK), "t", r"\cosh(\omega t)", size=48)
            r[2].set_color(YELLOW)
            r.move_to([0.9, -0.75, 0])
            rbox = SurroundingRectangle(r, color=YELLOW, buff=0.18).set_stroke(YELLOW, 3)
            self.play(*appear(r), run_time=rt(c, 1.2, "printed2", 0.5))
            self.play(FadeIn(rbox), run_time=rt(c, 0.8, "printed2", 0.8))
            c.wait_until("printed2")
            eq = MathTex("=", font_size=48).next_to(rbox, RIGHT, buff=0.3)
            p = MathTex(H2_ANS[3], font_size=48, color=GREEN).next_to(eq, RIGHT, buff=0.3)
            self.play(*appear(eq, shift=None), *during(appear(p), 0.3, 1), *flash([self.items[3]], GREEN), run_time=rt(c, 1.5, "since"))
            c.wait_until("since")
            j = X(r"\cos(-", ("i", PINK), r"\omega t) = \cosh(\omega t)", size=40)
            j.move_to([VGroup(rbox, p).get_x(), -1.85, 0])
            self.play(*appear(j), *self.done(None, 3), run_time=rt(c, 1.2, "slip"))
            c.wait_until("slip")
            s = MathTex(r"-i\omega\cosh(\omega t)", font_size=44, color=RED).move_to([0.9, -2.65, 0])
            st = T("d/dt: the wrong variable", 30, RED).next_to(s, RIGHT, buff=0.5)
            if st.get_right()[0] > 6.5:
                st.next_to(s, DOWN, buff=0.2).align_to(s, LEFT)
            tick_right = max(b.get_right()[0] for b in self.boxes.values())
            if st.get_left()[0] < tick_right + 0.5:
                st.shift((tick_right + 0.5 - st.get_left()[0]) * RIGHT)
            self.play(*appear(s), *during(appear(st), 0.4, 1), run_time=rt(c, 1.5))
