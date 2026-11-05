"""Chapter 5, scene 2: the definition z^w := e^{w ln z}, and why it has many values. Clips c5.def.1 – c5.def.4.

Shared helpers (import with load_scene("ch5_s2_define")):
  definition_box(size=120, note=True)  the YELLOW-boxed definition z^w := e^{w ln z} with its YELLOW
                                       "Definition" label above the box's top-left and (note=True) the
                                       DIM note "z ≠ 0" right of the box. VGroup with .tex .box .label
                                       .note (None if note=False), .e (the e glyph), .w (exponent's w),
                                       .lnz (the "ln z" glyphs). Built at ORIGIN (tex centred).
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

S5 = load_scene("ch5_s5_count")


# ---------------------------------------------------------------- shared helper
def definition_box(size=120, note=True):
    """The boxed definition z^w := e^{w ln z} (see module docstring)."""
    tex = MathTex(r"z^{w}", r":=", r"e^{w\ln z}", font_size=size, color=FG)
    box = SurroundingRectangle(tex, color=YELLOW, buff=0.35, stroke_width=4)
    label = T("Definition", size=44, color=YELLOW)
    label.next_to(box, UP, buff=0.15).align_to(box, LEFT)
    g = VGroup(box, tex, label)
    g.tex, g.box, g.label = tex, box, label
    g.e, g.w, g.lnz = tex[2][0], tex[2][1], tex[2][2:5]
    g.note = None
    if note:
        g.note = MathTex(r"z \neq 0", font_size=52, color=DIM).next_to(box, RIGHT, buff=0.35)
        g.add(g.note)
    return g


class Define(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c5.def.1
    def clip1(self):
        with self.say("c5.def.1") as c:
            a = MathTex(r"2^{3}", r"=", r"8", font_size=80).move_to(UP * 2.3)
            b = MathTex(r"2^{3}", r"=", r"e^{3\ln 2}", font_size=80).move_to(UP * 2.3)
            ch = MathTex(r"e^{3\ln 2}", r"=", r"\left(e^{\ln 2}\right)^{3}", r"=", r"2^{3}", r"=", r"8",
                         font_size=80).move_to(DOWN * 0.9)
            # the chain's first term sits straight under b's right side: the fly drops vertically
            ch.shift(RIGHT * (b[2].get_x() - ch[0].get_x()))
            dx = -(ch.get_right()[0] + b.get_left()[0]) / 2
            for m in (a, b, ch):
                m.shift(RIGHT * dx)
            a.align_to(b, LEFT)
            c.wait_until("cube")
            self.play(*appear(a), run_time=1.0)
            c.wait_until("three log two")
            self.play(*edit(a, b), run_time=min(1.6, c.until("why")))
            c.wait_until("why")
            self.play(*fly(b[2], ch[0]), run_time=1.4)
            self.play(*appear(*ch[1:], lag=0.3), run_time=1.6)
            settle(self, ch)
            inner = ch[2][1:5]
            ul = underline(inner, YELLOW)
            note = MathTex(r"e^{\ln 2} = 2", font_size=56, color=YELLOW).next_to(ul, DOWN, buff=0.35)
            self.play(GrowFromCenter(ul), *appear(note), run_time=1.0)
            c.wait_until("general")
            rule = MathTex(r"a^{b}", r"=", r"e^{b\ln a}", r"\quad (a>0)", font_size=110, color=BLUE)
            rule[3].set_color(DIM).scale(0.6, about_edge=LEFT)
            rule.move_to(DOWN * 0.9)
            self.chain = VGroup(ch, ul, note)
            self.play(*disappear(b), run_time=0.7)
            self.play(self.chain.animate.scale(0.6).set_opacity(0.6).to_edge(UP, buff=0.45), run_time=1.0)
            self.play(*appear(rule), run_time=1.0)
            self.rule = rule
            # pointer tags: "log of the base" is said first, then "exponent"
            b_g, ln_g = rule[2][1], rule[2][2:5]
            exp_t = T("exponent", size=38, color=BLUE).move_to(b_g.get_center() + np.array([-2.0, 1.4, 0]))
            base_t = T("log of the base", size=38, color=BLUE).move_to(ln_g.get_center() + np.array([2.0, 1.4, 0]))
            exp_a = Arrow(exp_t.get_bottom(), b_g.get_top(), buff=0.12, stroke_width=3, color=BLUE,
                          max_tip_length_to_length_ratio=0.15)
            base_a = Arrow(base_t.get_bottom(), ln_g.get_top(), buff=0.12, stroke_width=3, color=BLUE,
                           max_tip_length_to_length_ratio=0.15)
            c.wait_until(own_word=base_t)
            self.play(*appear(base_t), GrowArrow(base_a), run_time=1.0)
            c.wait_until("exponent", nth=1)
            self.play(*appear(exp_t), GrowArrow(exp_a), run_time=min(0.8, c.until()))
            self.tags1 = [exp_t, base_t, exp_a, base_a]

    # ------------------------------------------------------------ c5.def.2
    def clip2(self):
        with self.say("c5.def.2") as c:
            d = definition_box()
            d.move_to(DOWN * 0.6)
            self.defn = d
            c.wait_until("box")
            self.play(*disappear(*self.tags1, self.chain), run_time=0.8)
            self.play(*edit(self.rule, d.tex), run_time=1.6)
            self.play(GrowFromCenter(d.box), *appear(d.label), run_time=1.2)
            c.wait_until("except zero")
            self.play(*appear(d.note), run_time=1.0)
            settle(self, d)
            # the two parts
            ex_t = T("exponential", size=38, color=FG)
            ex_t.move_to([d.e.get_x() - 1.0, d.box.get_bottom()[1] - 0.95, 0])
            ln_t = T("logarithm (Part 4)", size=38, color=FG)
            ln_t.move_to([d.lnz.get_x() + 1.4, d.box.get_bottom()[1] - 0.95, 0])
            ex_a = Arrow(ex_t.get_top(), d.e.get_bottom(), buff=0.12, stroke_width=3, color=FG,
                         max_tip_length_to_length_ratio=0.12)
            ln_a = Arrow(ln_t.get_top(), d.lnz.get_bottom(), buff=0.12, stroke_width=3, color=FG,
                         max_tip_length_to_length_ratio=0.12)
            c.wait_until("exp2")
            self.play(*appear(ex_t), GrowArrow(ex_a), *recolor(d.e, YELLOW), run_time=1.0)
            c.wait_until("ln")
            self.play(*appear(ln_t), GrowArrow(ln_a), *recolor(d.lnz, TEAL), run_time=1.0)
            c.wait_until("theme")
            self.play(FlashAround(d.box, run_time=2, time_width=1.5))
            self.tags2 = [ex_t, ln_t, ex_a, ln_a]

    # ------------------------------------------------------------ c5.def.3
    def clip3(self):
        with self.say("c5.def.3") as c:
            d = self.defn
            self.play(*disappear(*self.tags2), run_time=0.8)
            self.play(d.animate.scale(0.7).to_edge(UP, buff=0.45), run_time=min(1.4, c.until("ladder")))
            c.wait_until("ladder")
            ns = (-1, 0, 1, 2)
            lad = S5.ladder(ns=ns, x=-5.0, y0=-1.6, pitch=1.0, ext=0.4)
            self.play(FlashAround(d.lnz, color=TEAL, run_time=1.2, time_width=1.5))
            # a TEAL streak runs from ln z down to the ladder's place; the ladder fades in there, whole
            # (no shrunken copy on top of the text)
            path = Line([d.lnz.get_x(), d.box.get_bottom()[1] - 0.12, 0], lad.get_top() + UP * 0.1, color=TEAL, stroke_width=5)
            self.play(VShowPassingFlash(path, time_width=0.6, run_time=0.9),
                      time_span(FadeIn(lad, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)
            c.wait_until("spread")
            dots, arrows, labels = {}, {}, {}
            for n in ns:
                col = GREEN if n == 0 else TEAL
                y = lad.y(n)
                dots[n] = Dot([0.6, y, 0], radius=0.12 if n == 0 else 0.1, color=col)
                arrows[n] = Arrow(lad.rungs[n].get_center(), dots[n].get_center(), buff=0.18,
                                  stroke_width=3, color=col, max_tip_length_to_length_ratio=0.04)
                labels[n] = MathTex(r"z^{w}", font_size=60, color=col).next_to(dots[n], RIGHT, buff=0.15)
            order = (0, 1, 2, -1)
            # first rung slow, the rest quicker
            self.play(GrowArrow(arrows[0]), run_time=1.4)
            self.play(FadeIn(dots[0], scale=0.5), *appear(labels[0]), run_time=0.8)
            self.play(*[GrowArrow(arrows[n]) for n in order[1:]],
                      *[FadeIn(dots[n], scale=0.5) for n in order[1:]],
                      *appear(*[labels[n] for n in order[1:]], lag=0.15), run_time=1.6)
            c.wait_until("many")
            col_grp = VGroup(*labels.values())
            br = Brace(col_grp, direction=RIGHT, buff=0.25, color=TEAL)
            many = T("many values", size=42, color=TEAL).next_to(br, RIGHT, buff=0.2)
            self.play(GrowFromCenter(br), *appear(many, shift=None), run_time=1.2)
            self.lad, self.dots, self.arrows, self.labels = lad, dots, arrows, labels
            self.many = [br, many]

    # ------------------------------------------------------------ c5.def.4
    def clip4(self):
        with self.say("c5.def.4") as c:
            lad, dots, arrows, labels = self.lad, self.dots, self.arrows, self.labels
            rest = [self.defn, lad.line, lad.brace, lad.brace_label]
            rest += [lad.rungs[n] for n in lad.rungs if n != 0]
            rest += [m[n] for m in (dots, arrows, labels) for n in m if n != 0]
            self.play(*disappear(*self.many), *set_alpha(rest, DIMMED), run_time=1.2)
            pv = T("principal value", size=40, color=GREEN).next_to(labels[0], RIGHT, buff=0.45)
            c.wait_until(own_word=pv)
            self.play(*appear(pv), run_time=1.0)
            c.wait_until("green")
            # colour pulse on the GREEN z^w and its dot: brighten to YELLOW, back to GREEN
            self.play(*recolor([dots[0], labels[0]], YELLOW), run_time=0.6)
            self.play(*recolor([dots[0], labels[0]], GREEN), run_time=0.8)
            c.wait_until("only")
            only = T("only one of the values", size=34, color=FG).next_to(pv, DOWN, buff=0.35).align_to(pv, LEFT)
            self.play(*set_alpha(rest, 1), *appear(only), run_time=1.4)
        self.wait(0.8)
