"""Chapter 4, scene 7: proof by induction, the two sums add by Pascal's rule. Clips c4.pascal.1 – c4.pascal.5.

Exported (the recap loads it):
  linked_rows(labels=False, heads=True, y3=True): the proof in miniature, in this scene's frame position.
      Parts: .heads (4 product MathTex f'''g, f''g', f'g'', fg''' over the 4 columns, or None),
      .top (VGroup of 3 YELLOW MathTex 1 2 1, columns 0-2), .bottom (VGroup 1 2 1, columns 1-3: the
      shifted copy), .bar (the DIM adding line), .sum (VGroup 1 3 3 1, YELLOW), .y3 (s3's y''' board line
      under it, or None), .cols (the 4 column x's), .labels (VGroup or None) with .lab_sums
      (VGroup(brace, "the two sums")), .lab_shift (VGroup(arrow, "the relabelling")),
      .lab_outer (VGroup(underline, underline, "the outer terms")); labels TEAL.
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


# ---------------------------------------------------------------- exported helper (first: the recap loads it)
LR_Y = dict(heads=2.1, top=1.1, bottom=0.15, bar=-0.4, sum=-1.0, y3=-2.35)


def _prod(nf, ng, size=40):
    t = MathTex("f" + "'" * nf, "g" + "'" * ng, font_size=size)
    t[0].set_color(BLUE)
    t[1].set_color(PURPLE)
    return t


def linked_rows(labels=False, heads=True, y3=True):
    """Two copies of 1 2 1, the second shifted one column right, adding to 1 3 3 1 (see module docstring)."""
    s3 = load_scene("ch4_s3_pattern")
    line = s3.y3_line(size=44)
    line.move_to([-0.6, LR_Y["y3"], 0])
    cols = [t.get_center()[0] for t in line.terms]

    def num_row(vals, start, y):
        return VGroup(*[MathTex(str(v), font_size=50, color=YELLOW).move_to([cols[start + i], y, 0])
                        for i, v in enumerate(vals)])

    g = VGroup()
    g.cols = cols
    g.heads = None
    if heads:
        g.heads = VGroup(*[_prod(3 - k, k).move_to([cols[k], LR_Y["heads"], 0]) for k in range(4)])
        g.add(g.heads)
    g.top = num_row([1, 2, 1], 0, LR_Y["top"])
    g.bottom = num_row([1, 2, 1], 1, LR_Y["bottom"])
    g.bar = Line([cols[0] - 0.55, LR_Y["bar"], 0], [cols[3] + 0.55, LR_Y["bar"], 0]).set_stroke(DIM, 3)
    g.sum = num_row([1, 3, 3, 1], 0, LR_Y["sum"])
    g.add(g.top, g.bottom, g.bar, g.sum)
    g.y3 = None
    if y3:
        g.y3 = line
        g.add(line)
    g.labels = None
    if labels:
        br = Brace(VGroup(g.top, g.bottom), RIGHT, buff=0.3, color=TEAL)
        ls = T("the two sums", 30, TEAL).next_to(br, RIGHT, buff=0.15)
        yb = LR_Y["bottom"]
        arr = Arrow([cols[0] - 0.25, yb, 0], [cols[1] - 0.3, yb, 0], buff=0, stroke_width=3,
                    max_tip_length_to_length_ratio=0.2, color=TEAL)
        lsh = T("the relabelling", 30, TEAL).next_to(arr, LEFT, buff=0.2)
        u0, u3 = underline(g.sum[0], TEAL, buff=0.12), underline(g.sum[3], TEAL, buff=0.12)
        lo = T("the outer terms", 30, TEAL).next_to(g.sum[3], RIGHT, buff=0.55)
        lab = VGroup(VGroup(br, ls), VGroup(arr, lsh), VGroup(u0, u3, lo))
        lab.lab_sums, lab.lab_shift, lab.lab_outer = lab[0], lab[1], lab[2]
        g.labels = lab
        g.add(lab)
    return g


# ---------------------------------------------------------------- scene pieces
S6 = load_scene("ch4_s6_proof1")
mt, place, limits = S6.mt, S6.place, S6.limits
XEQ, S1_Y = S6.XEQ, S6.S1_Y
LINE_Y = 2.0          # the merged working line
LS = 37            # the working line's font size
LEFT_C = -3.8         # centre of the left work area (triangle, slots)


def lhs_part(m):
    """Colour (fg)^{(...)}: f BLUE, g PURPLE."""
    m[1].set_color(BLUE)
    m[2].set_color(PURPLE)


def sum1_split():
    s = mt("=", r"f^{(n+1)}g", "+", r"\sum_{m=1}^{n}", r"\binom{n}{m}", r"f^{(n-m", "+1", ")}", r"g^{(m)}")
    s[4].set_color(YELLOW)
    s[6].set_color(BLUE)
    return place(s, s[2], XEQ, S1_Y)


def merged_line(bracket=True):
    mid = (r"\left[\binom{n}{m} + \binom{n}{m-1}\right]" if bracket else r"\binom{n+1}{m}")
    s = mt(r"(fg)^{(n+1)}", "=", r"f^{(n+1)}", r"g^{(0)}", "+", r"\sum_{m=1}^{n}", mid,
           r"f^{(n-m+1)}", r"g^{(m)}", "+", r"f^{(0)}", r"g^{(n+1)}", size=LS)
    lhs_part(s[0])
    s[6].set_color(YELLOW)
    for i in (2, 7, 10):
        s[i].set_color(BLUE)
    for i in (3, 8, 11):
        s[i].set_color(PURPLE)
    return s.move_to([0, LINE_Y, 0])


def final_line():
    s = mt(r"(fg)^{(n+1)}", "=", r"\sum_{m=0}^{n+1}", r"\binom{n+1}{m}", r"f^{(n-m+1)}", r"g^{(m)}", size=LS)
    lhs_part(s[0])
    s[3].set_color(YELLOW)
    s[4].set_color(BLUE)
    s[5].set_color(PURPLE)
    up, lo = limits(s[2])
    for gl in up + lo:
        gl.set_color(YELLOW)
    return s.move_to([0, LINE_Y, 0])


def vee(a, b, target):
    return [Arrow(m.get_bottom() + 0.14 * DOWN, target.get_top() + 0.12 * UP, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.35, color=GOLD) for m in (a, b)]


class ProofTwo(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c1: separate m = 0, add
    def clip1(self):
        shot = S6.handover_shot()
        self.add(*shot.submobjects)
        first = shot.row1[0]
        with self.say("c4.pascal.1") as c:
            self.play(FlashAround(first, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("out on its own")
            new1 = sum1_split()
            rt = min(2.0, c.until("its coefficient"))
            self.play(first.animate.shift(UP * (S6.BOX2_Y - S6.BOX1_Y)), *edit(shot.sum1, new1), run_time=rt)
            s1 = new1

            f = mt(r"\binom{n}{0}", r"f^{(n+1)} g^{(0)}", "=", r"f^{(n+1)} g", size=36)
            f[0].set_color(YELLOW)
            tag = mt("m = 0", size=34, color=DIM)
            note = VGroup(tag, f).arrange(RIGHT, buff=0.4)
            note.move_to([0, shot.note.get_y(), 0]).align_to(LEFT * 6.6, LEFT)
            c.wait_until("its coefficient")
            self.play(*appear(tag, f[0], f[1], lag=0.3), run_time=1.4)
            c.wait_until("so it's")
            self.play(*appear(f[2], f[3], shift=None), run_time=1.0)

            c.wait_until("both")
            up, lo = limits(s1[3])
            self.play(*recolor(up + lo, YELLOW), *recolor(limits(shot.sum2[1])[1], YELLOW),
                      FlashAround(s1[3], run_time=1.6, time_width=1.5),
                      FlashAround(shot.sum2[1], run_time=1.6, time_width=1.5), run_time=1.6)

            c.wait_until("add")
            self.merged = merged_line().move_to(ORIGIN)       # centred while it is alone; rises on {pascal}
            self.play(*during(disappear(*self.mobjects), 0, 0.45),
                      *during(appear(self.merged, shift=None), 0.5, 1), run_time=2.0)
            c.wait_until("each product")
            self.play(FlashAround(self.merged[6], run_time=1.8, time_width=1.5), run_time=1.8)

    # ------------------------------------------------------------------ c2: Pascal's triangle, the rule
    def clip2(self):
        s3 = load_scene("ch4_s3_pattern")
        tri = s3.pascal_triangle(n_max=3)
        tri.scale(1.8).move_to([LEFT_C, -1.15, 0])
        r2, r3 = tri.rows[2], tri.rows[3]
        with self.say("c4.pascal.2") as c:
            self.play(*during([self.merged.animate.move_to([0, LINE_Y, 0])], 0, 0.55),
                      *during(appear(tri, shift=None), 0.45, 1), run_time=2.0)
            c.wait_until("each number")
            v1 = vee(r2[0], r2[1], r3[1])
            self.play(*[GrowArrow(a) for a in v1], FlashAround(r3[1], color=GOLD, run_time=1.5), run_time=1.5)
            c.wait_until("two above it")
            v2 = vee(r2[1], r2[2], r3[2])
            self.play(*[GrowArrow(a) for a in v2], FlashAround(r3[2], color=GOLD, run_time=1.1), run_time=1.1)

            rule = mt(r"\binom{n}{m}", "+", r"\binom{n}{m-1}", "=", r"\binom{n+1}{m}", size=48)
            for i in (0, 2, 4):
                rule[i].set_color(YELLOW)
            rule.move_to([2.9, -0.7, 0])
            box = SurroundingRectangle(rule, color=YELLOW, buff=0.3, corner_radius=0.15).set_stroke(YELLOW, 2.5)
            tag = T("Pascal's rule · notes §8.4.2", 30, DIM).next_to(box, DOWN, buff=0.3)
            c.wait_until("rule")
            self.play(*appear(rule, shift=None), FadeIn(box), run_time=1.5)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
        self.tri, self.vees = tri, v1 + v2
        self.rule, self.rbox, self.rtag = rule, box, tag

    # ------------------------------------------------------------------ c3: why the rule holds
    def clip3(self):
        s4 = load_scene("ch4_s4_formula")
        slots = s4.prime_slots(4, side=0.9, pitch=1.15).move_to([LEFT_C, -0.3, 0])
        nm = mt(r"n+1 = 4,", r"\ m = 2", size=36, color=DIM).next_to(slots, UP, buff=0.35)
        lab_g = T("to g: pick m − 1 from the rest", 30, PURPLE).move_to([LEFT_C, -1.35, 0])
        lab_g.move_to([LEFT_C, -1.25, 0])
        lab_f = T("to f: pick m from the rest", 30, BLUE).next_to(lab_g, DOWN, buff=0.3)
        cnt = mt("3", "+", "3", "=", "6", "=", r"\binom{4}{2}", size=48, color=GOLD).move_to([LEFT_C, -2.65, 0])
        k1, k2, k3 = cnt[0], VGroup(*cnt[1:3]), VGroup(*cnt[3:])
        last = [slots.boxes[3], slots.primes[3]]
        with self.say("c4.pascal.3") as c:
            self.play(*during(disappear(self.tri, *self.vees), 0, 0.45),
                      *during(appear(*slots.slots, lag=0.15, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("send m")
            self.play(*appear(nm), run_time=1.0)
            c.wait_until("the last one")
            self.play(*recolor(last, PURPLE), FlashAround(slots.slots[3], color=PURPLE, run_time=1.2),
                      run_time=1.2)
            c.wait_until(own_word=lab_g)
            self.play(*appear(lab_g), *appear(k1, shift=None), run_time=1.0)
            c.wait_until("or it goes")
            self.play(*recolor(last, BLUE), FlashAround(slots.slots[3], color=BLUE, run_time=1.2),
                      *set_alpha([lab_g], 0.4), *appear(lab_f), run_time=1.2)
            c.wait_until("pick all")
            self.play(*appear(*cnt[1:], lag=0.15, shift=None), run_time=min(1.4, c.until()))
        self.c3 = [slots, nm, lab_g, lab_f, *cnt]

    # ------------------------------------------------------------------ c4: fold in the outer terms
    def clip4(self):
        s4 = load_scene("ch4_s4_formula")
        m1 = self.merged
        m2 = merged_line(bracket=False)
        fin = final_line()
        with self.say("c4.pascal.4") as c:
            self.play(*edit(m1, m2), FlashAround(self.rule[4], run_time=1.6, time_width=1.5),
                      run_time=min(1.6, c.until("ends")))
            c.wait_until("ends")
            self.play(*disappear(*self.c3, self.rule, self.rbox, self.rtag), run_time=1.0)
            self.play(FlashAround(VGroup(m2[2], m2[3]), run_time=1.4, time_width=1.5),
                      FlashAround(VGroup(m2[10], m2[11]), run_time=1.4, time_width=1.5), run_time=1.4)

            l0 = mt(r"\binom{n+1}{0} = 1", size=34, color=YELLOW).next_to(VGroup(m2[2], m2[3]), UP, buff=0.35)
            ln = mt(r"\binom{n+1}{n+1} = 1", size=34, color=YELLOW).next_to(VGroup(m2[10], m2[11]), UP, buff=0.35)
            c.wait_until("n plus one choose zero")
            self.play(*appear(l0), run_time=1.0)
            c.wait_until("and so is")
            self.play(*appear(ln), run_time=1.0)

            c.wait_until("so the outer terms")
            self.play(*edit(m2, fin), run_time=2.0)
            c.wait_until("the sum now runs")
            self.play(*disappear(l0, ln), FlashAround(fin[2], run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("done")
            big = 54
            card = s4.leibniz_card(size=big)
            tgt = fin.copy().scale(big / LS).move_to([0, 1.15, 0])
            card.move_to([0, -0.95, 0]).shift(RIGHT * (tgt[1].get_x() - card.eq.get_x()))
            dx = -(min(tgt.get_left()[0], card.get_left()[0]) + max(tgt.get_right()[0], card.get_right()[0])) / 2
            tgt.shift(RIGHT * dx)
            card.shift(RIGHT * dx)
            self.play(fin.animate.scale(big / LS).move_to(tgt), run_time=1.4)
            box = SurroundingRectangle(fin, color=YELLOW, buff=0.25, corner_radius=0.15).set_stroke(YELLOW, 2.5)
            self.play(FadeIn(box), *appear(card, shift=None), run_time=1.3)
            tick = check_mark().next_to(card, RIGHT, buff=0.5)
            c.wait_until("in place of")
            self.play(*appear(tick, shift=None), FlashAround(fin[3], color=GREEN, run_time=1.2),
                      FlashAround(card.binom, color=GREEN, run_time=1.2), run_time=1.2)

            c.wait_until("every")
            dom = S6.dominoes(h=0.65, w=0.14, pitch=0.5, label_size=28).move_to([0, -2.85, 0])
            self.play(*appear(dom, shift=None), run_time=0.8)
            tot = max(1.6, min(3.0, c.until() - 0.1))
            self.play(*S6.topple(dom, total=tot, fall=min(1.0, tot / 2.2)), run_time=tot)

    # ------------------------------------------------------------------ c5: the proof in miniature
    def clip5(self):
        g = linked_rows(labels=True)
        with self.say("c4.pascal.5", gap=3.5) as c:   # hold the picture: the labels land on the last words
            sweep_clear(self, run_time=1.4)
            c.wait_until("the whole proof")
            self.play(*appear(*g.heads, lag=0.2, shift=None), run_time=1.4)
            c.wait_until("take the row")
            self.play(*appear(*g.top, lag=0.25), run_time=1.2)
            c.wait_until("write it twice")
            anims = []
            for a, b in zip(g.top, g.bottom):
                anims += fly(a, b)
            self.play(*anims, run_time=1.8)

            c.wait_until("addrows")
            cols = []
            for k in range(4):
                parts = [m for m in ((g.top[k] if k < 3 else None), (g.bottom[k - 1] if k > 0 else None)) if m]
                cols.append(VGroup(*parts, g.sum[k]))
            flashes = [time_span(FlashAround(col, run_time=1.0, time_width=1.5), 0.4 + 0.45 * k, 1.4 + 0.45 * k)
                       for k, col in enumerate(cols)]
            self.play(time_span(GrowFromCenter(g.bar), 0, 0.6),
                      *[time_span(FadeIn(s, shift=0.2 * DOWN), 0.4 + 0.45 * k, 1.2 + 0.45 * k)
                        for k, s in enumerate(g.sum)], *flashes, run_time=2.75)

            c.wait_until("second derivative")
            self.play(*appear(g.y3), run_time=1.2)

            lab = g.labels
            c.wait_until(own_word=lab.lab_sums[1])
            self.play(GrowFromCenter(lab.lab_sums[0]), *appear(lab.lab_sums[1]), run_time=1.0)
            c.wait_until(own_word=lab.lab_shift[1])
            self.play(GrowArrow(lab.lab_shift[0]), *appear(lab.lab_shift[1]), run_time=1.0)
            c.wait_until(own_word=lab.lab_outer[2])
            self.play(*[GrowFromCenter(u) for u in lab.lab_outer[:2]], *appear(lab.lab_outer[2]),
                      run_time=min(1.0, c.until()))
