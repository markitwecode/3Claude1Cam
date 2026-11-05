"""Chapter 1, scene 2: what a list is. Syntax, order and repetition, one type.

Clips c1.what.1 – c1.what.4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def underline(glyphs, color, buff=0.12, width=4):
    return Line(LEFT, RIGHT, color=color, stroke_width=width).set_width(glyphs.width + 0.12) \
        .next_to(glyphs, DOWN, buff=buff)


def hl_box(glyphs, line, color=YELLOW):
    """P8 highlight box: faint fill behind the text, one height for the whole code line."""
    box = Rectangle(width=glyphs.width + 0.12, height=line.height + 0.3)
    box.move_to([glyphs.get_x(), line.get_y(), 0])
    box.set_stroke(color, 3).set_fill(color, 0.2)
    box.set_z_index(-1)
    return box


class WhatIsAList(NarratedScene):
    def construct(self):
        typed = self.syntax()
        ref = self.ordered(typed)
        row = self.one_type(ref)
        self.general_rule(row)

    # what.1: [3; 5; 9], its punctuation, and OCaml's reply
    def syntax(self):
        big = Code("[3; 5; 9]", size=96)
        digits = [big.find(d) for d in "359"]
        brackets = VGroup(big.find("["), big.find("]")).set_color(TEAL)
        semis = VGroup(big.find(";"), big.find(";", nth=1)).set_color(TEAL)

        top = Code("# [3; 5; 9];;\n- : int list = [3; 5; 9]", size=52, line_spacing=1.1)
        prompt, ends = top.find("#"), top.find(";;")
        VGroup(prompt, ends).set_color(DIM)
        typed = top.find("[3; 5; 9]", line=0)
        head = top.find("- : int list =", line=1)
        echo = top.find("[3; 5; 9]", line=1)
        int_list = top.find("int list", line=1)

        with self.say("c1.what.1") as c:
            # "Three, five, and nine." Each value appears as it is said
            for digit, word in zip(digits, ("three", "five", "nine")):
                c.wait_until(word)
                self.play(FadeIn(digit, shift=0.3 * DOWN), run_time=0.8)

            # "It's written in square brackets, with semicolons between the elements."
            c.wait_until("brackets")
            self.play(FadeIn(brackets, scale=1.3), run_time=1.0)
            c.wait_until("semicolons")
            self.play(FadeIn(semis, shift=0.3 * DOWN), run_time=1.0)

            # "When you type it into OCaml, it replies with the type: int list."
            c.wait_until("when you type")
            self.play(*[ReplacementTransform(a, b) for a, b in zip(big.text, typed)],
                      FadeIn(VGroup(prompt, ends)), run_time=1.8)
            c.wait_until("type")
            self.play(TransformFromCopy(typed, echo), FadeIn(head, shift=0.3 * DOWN),
                      run_time=1.5)
            # "A list of integers." Flash under the type and leave the underline
            c.wait_until("a list of integers")
            u = underline(int_list, GREEN)
            self.play(FlashUnder(int_list, color=GREEN, run_time=1.5), Create(u, run_time=1.0))
        self.toplevel = VGroup(VGroup(prompt, ends), typed, head, echo, u)
        return typed

    # what.2: order matters, repetition matters; a sequence, not a set
    def ordered(self, typed):
        size, g, nw = 52, 0.8, 0.55
        y1, y2 = 1.35, -0.2
        w3 = Code("[3; 5; 9]", size=size).width
        w4 = Code("[3; 3; 5; 9]", size=size).width
        x0 = -(w3 + 2 * g + nw + w4) / 2
        neq_x = x0 + w3 + g + nw / 2
        cmp_left = neq_x + nw / 2 + g

        ref = Code("[3; 5; 9]", size=size).move_to([x0 + w3 / 2, y1, 0])
        cmp1 = Code("[3; 5; 9]", size=size)
        cmp1.move_to([cmp_left + cmp1.width / 2, y1, 0])
        neq1 = MathTex(r"\neq", font_size=72).move_to([neq_x, y1, 0])

        ref2 = ref.copy().set_y(y2)
        tmp = Code("[3; 5; 9]", size=size)
        tmp.move_to([cmp_left + tmp.width / 2, y2, 0])
        cmp2 = Code("[3; 3; 5; 9]", size=size)
        cmp2.move_to([cmp_left + cmp2.width / 2, y2, 0])
        VGroup(cmp2.find("3"), cmp2.find("3", nth=1)).set_color(YELLOW)
        neq2 = MathTex(r"\neq", font_size=72).move_to([neq_x, y2, 0])

        sets = MathTex(r"\{3, 5, 9\} = \{5, 3, 9\} = \{3, 3, 5, 9\}", font_size=56)
        sets_lab = T("sets in maths:", size=34, color=DIM)
        set_line = VGroup(sets_lab, sets).arrange(RIGHT, buff=0.4).move_to(DOWN * 2.15)
        sets_lab.align_to(sets[0][1], DOWN)  # baseline of the "3", not the brace

        with self.say("c1.what.2") as c:
            # OCaml's exchange moves up out of the way (still readable); the list is copied out
            self.play(self.toplevel.animate.scale(0.65).to_edge(UP, buff=0.4),
                      TransformFromCopy(typed, ref.text), run_time=1.5)

            # "First, order matters. Five, three, nine is a different list..."
            c.wait_until("order")
            self.play(TransformFromCopy(ref, cmp1), run_time=1.5)
            c.wait_until("five three nine")
            three, five = cmp1.find("3"), cmp1.find("5")
            p3, p5 = three.get_center(), five.get_center()
            self.play(three.animate(path_arc=-0.8 * PI).move_to(p5).set_color(YELLOW),
                      five.animate(path_arc=-0.8 * PI).move_to(p3).set_color(YELLOW),
                      run_time=1.2)
            c.wait_until("a different")
            self.play(Write(neq1), run_time=1.0)

            # "Second, repetition matters." Spotlight the new row.
            c.wait_until("repeat")
            row1 = VGroup(ref, cmp1, neq1)
            self.play(row1.animate.set_opacity(0.25), TransformFromCopy(ref, ref2),
                      TransformFromCopy(ref, tmp), run_time=1.5)
            # "Three, three, five, nine": "5; 9]" slides right, a second "3;" drops into the gap
            c.wait_until("three three five nine")
            keep = [(0, 0), (1, 1), (2, 2), (3, 5), (4, 6), (5, 7), (6, 8)]
            extra = VGroup(cmp2.text[3], cmp2.text[4])
            self.play(*[tmp.text[i].animate.move_to(cmp2.text[j]).set_color(cmp2.text[j].get_color())
                        for i, j in keep],
                      FadeIn(extra, shift=0.4 * DOWN), run_time=1.5)
            self.remove(tmp, extra)
            self.add(cmp2)
            c.wait_until("different again")
            self.play(Write(neq2), run_time=1.0)

            # "So a list is not like a set from maths."
            c.wait_until("set")
            self.play(row1.animate.set_opacity(1), FadeIn(set_line, shift=0.3 * UP), run_time=1.5)
        self.order_stuff = (cmp1, neq1, ref2, cmp2, neq2, set_line)
        return ref

    # what.3: every element has the same type
    def one_type(self, ref):
        header = T("Every element has the same type", size=44,
                   t2c={"same type": GREEN}).move_to(UP * 2.55)
        rows = []
        for val, typ in (("[3; 5; 9]", "int list"),
                         ('[(1, "one"); (2, "two")]', "(int * string) list"),
                         ("[[3]; [5; 9]]", "int list list")):
            code = Code(f"{val} : {typ}", size=34)
            code.find(typ).set_color(GREEN)
            rows.append((code, code.find(val), code.find(":"), code.find(f": {typ}")))

        # colons in one column, the block centred
        ys = [1.05, -0.3, -1.65]
        left = max(colon.get_x() - code.get_left()[0] for code, _, colon, _ in rows)
        right = max(code.get_right()[0] - colon.get_x() for code, _, colon, _ in rows)
        col = (left - right) / 2
        for (code, _, colon, _), y in zip(rows, ys):
            code.shift([col - colon.get_x(), y - colon.get_y(), 0])

        cues = [("ints", "int list"), ("pairs", "int times string"), ("lists", "this one has type")]

        with self.say("c1.what.3") as c:
            # "There is one strict rule. Every element of a list must have the same type."
            # The header needs the top: OCaml's exchange goes, the comparisons step back.
            c.wait_until("rule")
            self.play(time_span(FadeOut(self.toplevel), 0, 0.7),
                      time_span(FadeIn(header, shift=0.3 * DOWN), 0.4, 1.4),
                      VGroup(*self.order_stuff).animate.set_opacity(0.4), run_time=1.4)
            c.wait_until("same type")
            same = select(header, "same type")[0]
            self.play(FlashUnder(same, color=GREEN, run_time=1.2))

            for i, ((code, val, _, typ), (mark, type_cue)) in enumerate(zip(rows, cues)):
                c.wait_until(mark)
                if i == 0:
                    # the table starts: clear the comparisons, the reference list joins it
                    self.play(LaggedStart(*[FadeOut(m) for m in self.order_stuff], lag_ratio=0.1),
                              *[ReplacementTransform(a, b) for a, b in zip(ref.text, val)],
                              run_time=1.1)
                else:
                    self.play(FadeIn(val, shift=0.3 * UP), run_time=1.0)
                c.wait_until(type_cue)
                self.play(FadeIn(typ, shift=0.3 * LEFT), run_time=1.0)
        self.header = header
        self.rows = [r[0] for r in rows]
        return self.rows[0]

    # what.4: the general rule, born from the first example; the list OCaml rejects
    def general_rule(self, example):
        header = self.header
        ex_x = example.copy().scale(40 / 34).move_to(UP * 1.3)

        rule = MathTex(r"x_1, \ldots, x_n", r":", r"\tau", r"\quad\Longrightarrow\quad",
                       r"[", r"x_1", r";\,", r"\ldots", r";\,", r"x_n", r"]",
                       r":", r"\tau", r"\ \mathtt{list}", font_size=56)
        rule.move_to(DOWN * 0.15)
        for i in (2, 12, 13):
            rule[i].set_color(GREEN)
        premise, tau, concl = rule[0], rule[2], rule[4:11]

        bad = Code('[3; "five"]', size=48)
        bad.move_to(DOWN * 1.75).align_to(rule, LEFT)
        box = hl_box(bad.find("3"), bad)
        box_five = hl_box(bad.find('"five"'), bad)
        note = T("Type error: rejected before the program runs", size=30, color=RED)
        note.next_to(bad, DOWN, buff=0.4).align_to(bad, LEFT)

        pick = MathTex(r"x_i", r":", r"\tau", font_size=56)
        pick[2].set_color(GREEN)
        pick.next_to(concl, DOWN, buff=1.3)
        pick.shift(RIGHT * (concl.get_x() - pick[0].get_x()))
        down = Arrow(concl.get_bottom(), pick[0].get_top(), buff=0.2, color=DIM,
                     stroke_width=4, max_tip_length_to_length_ratio=0.25, tip_length=0.2)

        with self.say("c1.what.4") as c:
            # the first example steps up to become the source of the general rule
            self.play(Transform(example, ex_x), run_time=1.2)

            # "If every element has the same type, call it tau, then the list has type tau list."
            # The rule needs the middle: the other two examples go now.
            c.wait_until("if every element")
            self.play(LaggedStart(FadeOut(self.rows[2]), FadeOut(self.rows[1]), lag_ratio=0.25),
                      time_span(TransformFromCopy(
                          VGroup(*[g for d in "359" for g in example.find(d)]), premise), 0.5, 1.6),
                      run_time=1.6)
            c.wait_until("call it")
            self.play(TransformFromCopy(example.find("int"), tau), FadeIn(rule[1]), run_time=0.9)
            c.wait_until("then the list")
            self.play(Write(rule[3]), TransformFromCopy(premise, concl),
                      TransformFromCopy(rule[1:3], rule[11:13]), FadeIn(rule[13], shift=0.2 * LEFT),
                      run_time=1.5)

            # "So what about a list that mixes an integer with a string?"
            c.wait_until("bad")
            self.play(VGroup(header, example).animate.set_opacity(0.4),
                      FadeIn(bad, shift=0.3 * UP), run_time=1.0)
            c.wait_until("integer")
            self.play(FadeIn(box), run_time=0.7)
            c.wait_until("string")
            self.play(box.animate.become(box_five), run_time=0.8)

            # "OCaml rejects it, before the program even runs."
            c.wait_until("reject")
            self.play(bad.animate.set_color(RED), box.animate.set_stroke(RED).set_fill(RED, 0.15),
                      run_time=1.0)
            c.wait_until("before the program")
            self.play(FadeIn(note, shift=0.3 * UP), run_time=1.0)

            # "That might feel strict, but it's a gift. Whenever you take an element out of a
            #  list, you know exactly what type it is." The rejected list stays, dimmed.
            c.wait_until("gift")
            self.play(AnimationGroup(GrowArrow(down), TransformFromCopy(rule[5], pick[0]),
                                     TransformFromCopy(rule[11:13], pick[1:])),
                      VGroup(bad, note).animate.set_opacity(0.4),
                      box.animate.set_stroke(opacity=0.4).set_fill(opacity=0.06), run_time=1.5)
            c.wait_until("a gift")
            self.play(VGroup(header, example).animate.set_opacity(1), run_time=1.0)
            c.wait_until("whenever")
            self.play(FlashAround(pick, color=GREEN, run_time=1.5, time_width=1.5))

        self.play(LaggedStart(*[FadeOut(m) for m in (header, example, rule, down, pick,
                                                     bad, box, note)],
                              lag_ratio=0.06), run_time=1.0)
