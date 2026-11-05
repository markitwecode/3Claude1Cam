"""Chapter 6, scene 5: power, P = IV, derived step by step from V_L = E/Q and I = Q/t. Clips c6.power.1 – c6.power.3.

Opens on ch6_s4_volts.handover_shot() (the loop, lamp lit), which shrinks to the top left. The
derivation is a column of lines aligned on "=", each made from a copy of the one above; the two
definitions sit in a side column, rearrange, and their right-hand sides fly into the slots.
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

S3 = load_scene("ch6_s3_current")

FS = 64                      # derivation lines
SIDE = 46                    # the small definitions
X_EQ = 0.8                   # the column's "=" signs
ROWS = [1.45, -0.02, -1.5, -2.72]
X_SIDE = 4.9
SMALL, BIG = 0.5, 0.72  # the loop: top-left while deriving; back for the example
COL = {"I": GOLD, "V_L": TEAL, "V": TEAL}


def mt(*parts, size=FS):
    m = MathTex(*parts, font_size=size)
    for i, p in enumerate(parts):
        m[i].set_color(COL.get(p, FG))
    return m


def frac_line(num, den="t", y=0.0):
    """P_L = num/den with a drawn bar, "=" at (X_EQ, y). .lhs .num .bar .den"""
    lhs = mt("P_L", "=")
    n, d = mt(*num), mt(den)
    w = max(n.width, d.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(FG, 4)
    n.next_to(bar, UP, buff=0.14)
    d.next_to(bar, DOWN, buff=0.14)
    fr = VGroup(n, bar, d).next_to(lhs, RIGHT, buff=0.25)
    fr.shift(UP * (lhs[1].get_y() - bar.get_y()))
    g = VGroup(lhs, n, bar, d)
    g.shift([X_EQ - lhs[1].get_x(), y - lhs[1].get_y(), 0])
    g.lhs, g.num, g.bar, g.den = lhs, n, bar, d
    return g


def at_eq(m, eq_index, y, x=X_EQ):
    return m.shift([x - m[eq_index].get_x(), y - m[eq_index].get_y(), 0])


def _find(root, pred):
    for m in root.get_family():
        if pred(m):
            return m
    return None


def _labels(g):
    b = g.loop.battery
    return [g.vb.label, g.vl.label, b.plus_sign, b.minus_sign]


def _shot():
    return load_scene("ch6_s4_volts").handover_shot()


class Power(NarratedScene):
    def construct(self):
        shot = _shot()
        self.add(shot)
        self.clip1(shot)
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)


    # -----------------------------------------------------------------------------------------
    def clip1(self, shot):
        self.shot = shot
        with self.say("c6.power.1") as c:
            tgt = shot.copy().scale(SMALL)
            tgt.move_to([-6.6 + tgt.width / 2, 3.5 - tgt.height / 2, 0])
            for m in _labels(tgt):
                m.set_fill(opacity=0)        # too small to read up there; back for the example
            self.play(Transform(shot, tgt), run_time=1.2)
            lp = shot.lamp
            q = Tex(r"What is the power dissipated", r"($P_L$) in the lamp?", font_size=46)
            VGroup(*q).arrange(DOWN, buff=0.16)
            q.move_to([2.0, 2.95, 0])
            tag = MathTex("P_L", font_size=44, color=YELLOW)
            tag.next_to(lp.circle, LEFT, buff=0.22)
            c.wait_until("power")
            self.play(*appear(q, tag, lag=0.4), run_time=1.2)  # early: the question is read as a whole
            self.q, self.tag = q, tag

            c.wait_until("def")
            l1 = frac_line(["E"], "t", ROWS[0])
            self.play(*appear(l1, shift=None), run_time=1.0)
            self.l1 = l1

            units = MathTex(r"\mathrm{J/s} = \text{watts (W)}", font_size=44, color=DIM)
            units.next_to(l1, RIGHT, buff=0.8).set_y(l1.lhs[1].get_y())
            c.wait_until("joule")
            self.play(*appear(units), run_time=1.0)  # early: "joule per second" is the J/s

            c.wait_until("energy it converts")
            self.play(*recolor([l1.num[0]], YELLOW), FlashAround(l1.num[0], run_time=1.2, time_width=1.5),
                      run_time=1.2)
            c.wait_until("divided by the time")
            self.play(*recolor([l1.den[0]], YELLOW), FlashAround(l1.den[0], run_time=1.2, time_width=1.5),
                      run_time=1.2)

            c.wait_until("how")
            vcard = MathTex(r"V_L", r"=", r"\frac{E}{Q}", font_size=SIDE)   # s4's
            vcard[0].set_color(TEAL)
            vcard.move_to([X_SIDE, ROWS[1] + 0.35, 0])
            icard = S3.i_eq_qt(SIDE).move_to([X_SIDE, ROWS[2] + 0.35, 0])
            self.play(*recolor([l1.num[0], l1.den[0]], FG), run_time=0.8)
            self.play(*appear(vcard, icard, lag=0.5), run_time=min(1.5, c.until(floor=0.8)))
            self.vcard, self.icard, self.units = vcard, icard, units

    # -----------------------------------------------------------------------------------------
    def _slide_in(self, rule, slot, carried=(), lead=None, **kw):
        """The boxed rule's right-hand side slides into the new line's slot: the rule's left side
        and "=" fade, its right-hand glyphs move and grow into `slot`; the new line's other pieces
        come in around them; `carried` (src glyph, dst glyph) pairs fly down from the line above."""
        k = FS / SIDE
        anims = during([FadeOut(rule[0]), FadeOut(rule[1])], 0, 0.3)
        anims += during([g.animate.scale(k).move_to(d) for g, d in zip(rule[2:], slot)], 0.25, 1)
        for a_, b_, arc in carried:
            anims += during(fly(a_, b_, arc=arc), 0.1, 1)
        return anims

    def _swap_in(self, rule, line):
        self.remove(*rule.get_family())
        self.remove(*line.get_family())
        self.add(line)

    def clip2(self):
        l1, vcard, icard = self.l1, self.vcard, self.icard
        with self.say("c6.power.2") as c:
            # {sub1}: V_L = E/Q, "so the energy is ..." rearranges to E = Q V_L, boxed
            self.play(FlashAround(vcard, run_time=1.2, time_width=1.5), *disappear(self.units), run_time=1.2)
            erule = at_eq(mt("E", "=", "Q", "V_L", size=SIDE), 1, vcard[1].get_y(), x=vcard[1].get_x())
            c.wait_until("so the energy")
            self.play(*edit(vcard, erule), run_time=1.5)
            box = SurroundingRectangle(erule, color=YELLOW, buff=0.15, corner_radius=0.08)
            self.play(FadeIn(box), run_time=0.6)

            # "Put that in": Q V_L slides into the E slot of a new line
            c.wait_until("put that in")
            l2 = frac_line(["Q", "V_L"], "t", ROWS[1])
            self.play(*self._slide_in(erule, l2.num),
                      *during(Transform(box, SurroundingRectangle(l2.num, color=YELLOW, buff=0.12,
                                                                  corner_radius=0.08)), 0.25, 1),
                      *during(appear(l2.lhs, l2.bar, l2.den, shift=None, lag=0), 0.4, 1),
                      run_time=min(1.6, c.until("sub2", floor=1.0)))
            self._swap_in(erule, l2)

            # {sub2}: I = Q/t, "so the charge is ..." rearranges to Q = I t, boxed
            c.wait_until("sub2")
            self.play(FadeOut(box), FlashAround(icard, run_time=1.2, time_width=1.5), run_time=1.2)
            qrule = at_eq(mt("Q", "=", "I", "t", size=SIDE), 1, icard[1].get_y(), x=icard[1].get_x())
            c.wait_until("so the charge")
            self.play(*edit(icard, qrule), run_time=1.4)
            box2 = SurroundingRectangle(qrule, color=YELLOW, buff=0.15, corner_radius=0.08)
            self.play(FadeIn(box2), run_time=0.6)

            c.wait_until("put that in too")
            l3 = frac_line(["I", "t", "V_L"], "t", ROWS[2])
            it = VGroup(l3.num[0], l3.num[1])
            self.play(*self._slide_in(qrule, it),
                      *during(Transform(box2, SurroundingRectangle(it, color=YELLOW, buff=0.12,
                                                                   corner_radius=0.08)), 0.25, 1),
                      *during(appear(l3.lhs, l3.bar, l3.den, shift=None, lag=0), 0.4, 1),
                      run_time=min(1.3, c.until("cancel", floor=1.0)))
            self.play(*appear(l3.num[2], shift=None), run_time=0.5)
            self._swap_in(qrule, l3)

            # {cancel}: the two t's
            c.wait_until("time on top")
            top_t, bot_t = l3.num[1], l3.den[0]
            self.play(FadeOut(box2), *recolor([top_t], YELLOW), FlashAround(top_t, run_time=1.0, time_width=1.5),
                      run_time=1.0)
            c.wait_until("underneath")
            self.play(*recolor([bot_t], YELLOW), FlashAround(bot_t, run_time=1.0, time_width=1.5), run_time=1.0)
            c.wait_until("they cancel")
            # a short, shallow stroke inside each t's own box (a tall one reads as a slash through the I)
            strikes = [Line(t.get_center() + [-t.width / 2 - 0.03, -0.1, 0],
                            t.get_center() + [t.width / 2 + 0.03, 0.1, 0]).set_stroke(YELLOW, 5)
                       for t in (top_t, bot_t)]
            self.play(*[Create(s) for s in strikes], run_time=0.7)
            self.play(*[restyle(t, op=0.3, fill=DIM) for t in (top_t, bot_t)],
                      *[restyle(s, op=0.3, outline=DIM) for s in strikes], run_time=0.8)

            # {result}: P_L = I V_L (W), boxed: what's left after the cancel, written below
            c.wait_until("result")
            l4 = at_eq(mt("P_L", "=", "I", "V_L"), 1, ROWS[3])
            watt = MathTex(r"(\mathrm{W})", font_size=48, color=DIM).next_to(l4, RIGHT, buff=0.4)
            watt.shift(UP * (l4[0][0].get_bottom()[1] - watt.get_bottom()[1] - 0.12))
            self.play(*appear(VGroup(l4[0], l4[1]), l4[2], l4[3], shift=0.3 * DOWN, lag=0.3), run_time=1.5)
            self.remove(*l4.get_family())
            self.add(l4)
            box4 = SurroundingRectangle(VGroup(l4, watt), color=YELLOW, buff=0.16, corner_radius=0.1)
            self.play(*appear(watt, shift=None), FadeIn(box4), run_time=1.0)
            self.l4, self.watt, self.box4 = l4, watt, box4

    # -----------------------------------------------------------------------------------------
    def clip3(self):
        l4, watt, box4, shot = self.l4, self.watt, self.box4, self.shot
        with self.say("c6.power.3") as c:
            # {any}: everything but the loop and the result clears; the result comes to the centre
            res = VGroup(l4, watt, box4)
            sweep_clear(self, res.animate.scale(1.25).move_to([0.6, 0.45, 0]),
                        keep=[shot, self.tag, l4, watt, box4], run_time=1.6)
            gen = mt("P", "=", "I", "V", size=int(FS * 1.25))
            gen.shift(l4[1].get_center() - gen[1].get_center())
            watt_t = watt.copy().next_to(gen, RIGHT, buff=0.4).align_to(watt, DOWN)
            box_g = SurroundingRectangle(VGroup(gen, watt_t), color=YELLOW, buff=0.25, corner_radius=0.1)
            self.play(*edit(l4, gen), watt.animate.move_to(watt_t), Transform(box4, box_g),
                      FadeOut(self.tag), run_time=min(1.5, c.until("the power in it", floor=0.8)))

            tag_i = T("current through it", 36, GOLD).move_to([-2.6, -1.7, 0])
            tag_v = T("voltage across it", 36, TEAL).move_to([3.7, -1.7, 0])
            ar_i = Arrow(tag_i.get_top(), gen[2].get_bottom(), buff=0.15, color=GOLD, stroke_width=4,
                         max_tip_length_to_length_ratio=0.18)
            ar_v = Arrow(tag_v.get_top(), gen[3].get_bottom(), buff=0.15, color=TEAL, stroke_width=4,
                         max_tip_length_to_length_ratio=0.18)
            c.wait_until(own_word=tag_i)
            self.play(*appear(tag_i), GrowArrow(ar_i), run_time=1.0)
            c.wait_until(own_word=tag_v)
            self.play(*appear(tag_v), GrowArrow(ar_v), run_time=1.0)

            # {familiar}
            c.wait_until("familiar")
            quote = T("“an expression that hopefully is familiar”", 32, DIM, slant=ITALIC)
            quote.move_to([0.0, -2.85, 0])
            self.play(*appear(quote), run_time=1.0)  # early: the slide's words, said from "familiar"

            # {example}: back on the loop, bigger, labels back
            c.wait_until("example")
            k = BIG / SMALL
            big = shot.copy().scale(k)
            big.move_to([-6.5 + big.width / 2, 0.0, 0])
            for m in _labels(big):
                m.set_fill(opacity=1).scale(1.5)
            big.vl.label.next_to(big.vl.arrow, RIGHT, buff=0.15)
            big.vb.label.next_to(big.vb.arrow, LEFT, buff=0.15)
            res2 = VGroup(gen, watt, box4)
            self.play(*during(disappear(tag_i, tag_v, ar_i, ar_v), 0, 0.4),
                      *during([Transform(shot, big), res2.animate.move_to([4.1, 1.5, 0])], 0.3, 1),
                      run_time=1.6)

            amps = T("0.2 A", 34, GOLD).next_to(shot.cur.arrow, DOWN, buff=0.22)
            volts = T("1.5 V", 34, TEAL).next_to(shot.vl.label, DOWN, buff=0.25)
            set_backstroke(amps)
            set_backstroke(volts)
            c.wait_until("amps")
            self.play(*appear(amps), run_time=0.8)
            c.wait_until("volts")
            self.play(*appear(volts), run_time=0.8)
            calc0 = MathTex("P", "=", r"0.2", r"\times", r"1.5", font_size=52, color=GOLD)
            calc = MathTex("P", "=", r"0.2", r"\times", r"1.5", "=", r"0.3\,\text{W}", font_size=52, color=GOLD)
            calc.move_to([4.1, -1.7, 0])
            calc0.align_to(calc, LEFT).set_y(calc.get_y())
            self.play(*appear(calc0, shift=None), run_time=0.8)
            c.wait_until("watts")
            self.play(*edit(calc0, calc), run_time=min(1.0, c.until(floor=0.6)))
        self.wait(6.6)
