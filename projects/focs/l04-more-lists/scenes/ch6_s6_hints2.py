"""Chapter 6, scene 6: exercises 4.4 to 4.6, each card and its hint. Clips c6.ex.8 – c6.ex.13.

PLAN (s5's exercise-card kit, imported: HeroCard waits lowered while stated, lifts for its hint,
the hint sits beneath it; GOLD "?" for answers, never a solution; "pause and try it" top right)
Opens on s5's last shot: the strip alone, 4.1-4.3 done.
- 4.4 "Hidden assumptions": the two questions and the three change headers (greedy / every
  way / faster); on "till" the till/amt column turns YELLOW under one tall box. Hint: the
  labels flash on "each version"; four input chips (2 x 2) land one per cue, each with a GOLD
  "?"; {careful}: chip 1 turns RED, "think before you run it" beside the Hint label, above it.
- 4.5 "Counting the ways": the task revealed with the voice; under the card [5][2][2] and its
  reordering [2][5][2] "= count as one"; "Three values? Four? …". Hint: coins 5 and 2 and an
  amount n; "how many 5s?" counts 0, 1, 2 while 5-coins fly out of the 5; "the rest in 2s ?";
  {build}: [5][2] and a new [1] on the right, an arrow back to a brace round the two-coin picture.
- 4.6 "What the types force": `val f :` / `val g :` first, then each type; the calls
  `f (1, true) ⇒ ?` and `g 0 ⇒ ?`; the question. Hint (from lecture 3): id, dim; its 'a flash
  PINK, "knows nothing about 'a"; a box on the body x, a dashed arrow back to the parameter;
  {where}: f's "?" opens into "(?, ?)" and dashed arrows run from each result slot back to the
  arguments (to the pair as a whole, so no slot is matched to an argument).
Ends like s5: 4.6 shrinks into its pill (all six done), the strip holds, then fades.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch1_s1_hook import coin  # noqa: E402  ch1's GOLD coin disc
from scenes.ch6_s5_hints1 import (  # noqa: E402  the shared exercise-card kit (read-only)
    CODE_DIM, COL_X, DONE, EX44_HEADERS, EX44_LABELS, EX46_CALLS, EX46_TYPES, TODO, HeroCard,
    enter_card, exit_card, finish, fit, hint_label, hold_for, make_strip, pause_tag,
)

# 4.4 (y's are for the lifted card; lower() drops them while the card is stated)
H44 = 4.02                          # card bottom at -1.30
Q44_Y = (1.62, 1.06)                # the two questions
HDR44_Y = (0.30, -0.26, -0.82)      # the three headers
HDR_X = COL_X + 2.1                 # the headers' left edge (labels right-aligned before it)
CHIPS = ["a coin worth 0", "an amount below 0", "coins smallest first", "the same coin twice"]
CHIP_CUES = ["zero", "negative", "order", "twice"]
CHIP_W, CHIP_H = 5.7, 0.62
CHIP_ROWS = (-2.38, -3.10)
CHIP_COLS = (COL_X, COL_X + 6.1)

# 4.5
H45 = 2.75                          # card bottom at -0.03
T45_Y = (1.62, 1.02, 0.42)
EX45_Y = -2.45                      # the "count as one" example, under the lowered card
PIC_Y = (-1.12, -2.12, -3.05)       # hint rows: coins + n / how many 5s? / the rest in 2s
PIC_R, SMALL_R = 0.42, 0.34

# 4.6
H46 = 4.30                          # card bottom at -1.58
SIG_SIZE = 44
SIG_Y = (1.45, 0.65)
CALL_Y = -0.30
ASK_Y = -1.10
ID_SRC = ("let id x = x", "val id : 'a -> 'a = <fun>")
ID_Y = (-2.72, -3.24)


def t_part(text, sub):
    """A copy of the glyphs of `sub` in a T line, in place (to reveal a line piece by piece)."""
    return select(text, sub)[0].copy()


def left_at(mob, y, x=COL_X):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def code_at(src, y, x=COL_X, size=SIG_SIZE, key=None):
    """A Code line, left edge at x, with the glyphs of `key` (default: first word) centred on y,
    so lines with and without descenders share a baseline."""
    code = Code(src, size=size).move_to([x, y, 0], aligned_edge=LEFT)
    k = code.find(key or src.split()[0])
    code.shift((y - k.get_center()[1]) * UP)
    return code


def split_code(src, parts, y, x=COL_X, size=SIG_SIZE):
    """Each part of a code line as its own Code, placed exactly where it sits in the line."""
    full = code_at(src, y, x, size)
    out = []
    for p in parts:
        piece = Code(p, size=size)
        piece.move_to(VGroup(*full.find(p)))
        out.append(piece)
    return out


def gold_q(size=48):
    return T("?", size=size, color=GOLD)


def chip(text):
    box = RoundedRectangle(corner_radius=0.18, width=CHIP_W, height=CHIP_H)
    box.set_stroke(DIM, 2.5).set_fill(BG, 0.5)
    lab = T(text, size=30, t2c={"0": GOLD})
    lab.move_to(box).align_to(box, LEFT).shift(0.32 * RIGHT)
    q = gold_q(38).move_to(box).align_to(box, RIGHT).shift(0.32 * LEFT)
    return VGroup(box, lab, q)


def coin_row(values, r=SMALL_R, buff=0.14):
    return VGroup(*[coin(v, r=r) for v in values]).arrange(RIGHT, buff=buff)


def dashed_arc(start, end, angle, color=YELLOW, num_dashes=12, tip=0.2):
    """A dashed curved arrow: (dashes, tip)."""
    arc = ArcBetweenPoints(start, end, angle=angle).set_stroke(color, 3.5)
    arc.add_tip(tip_length=tip, tip_width=tip)
    head = arc.pop_tips()
    head.set_fill(color, 1).set_stroke(color, 0)
    return VGroup(DashedVMobject(arc, num_dashes=num_dashes, dashed_ratio=0.55), head)


class ExercisesFourToSix(NarratedScene):
    def construct(self):
        self.strip = make_strip([DONE] * 3 + [TODO] * 3)
        self.play(FadeIn(self.strip), run_time=0.8)        # s5's last shot
        self.wait(0.3)
        self.ex44()
        self.hint44()
        self.ex45()
        self.hint45()
        self.ex46()
        self.hint46()
        hold_for(self, self.pause_born, len("pause and try it"))
        # 4.6 shrinks back into its pill: all six done; the strip holds, then fades
        self.play(*exit_card(self.strip, self.card, [*self.hint, self.tag]), run_time=1.1)
        self.remove(self.card.frame)
        self.wait(0.9)
        finish(self)

    def pause(self, c):
        c.wait_until("try")
        tag = pause_tag()
        self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.tag, self.pause_born = tag, self.time

    def next_card(self, card):
        """The current card (and its hint) shrinks into its pill; the next grows out of its own.
        The pause tag stays a moment longer, then goes."""
        self.play(*exit_card(self.strip, self.card, self.hint), run_time=1.0)
        self.remove(self.card.frame)
        self.play(*enter_card(self.strip, card), run_time=1.0)
        self.play(FadeOut(self.tag), run_time=0.6)
        self.card = card

    # ── c6.ex.8: card 4.4, the questions and the three headers ──────────────────────
    def ex44(self):
        card = HeroCard(3, height=H44)
        q1 = left_at(T("What do the change functions assume about till and amt?", size=32,
                       t2c={"till": YELLOW, "amt": YELLOW}, t2f={"till": MONO, "amt": MONO}),
                     Q44_Y[0])
        q2 = left_at(T("What could happen if those assumptions fail?", size=32), Q44_Y[1])
        rows = []
        for lab, src, y in zip(EX44_LABELS, EX44_HEADERS, HDR44_Y):
            code = code_at(src, y, x=HDR_X, size=32, key="let")
            name = T(lab, size=30, color=DIM).next_to(code, LEFT, buff=0.35)
            name.shift((code.find("let").get_bottom()[1] - name.get_bottom()[1]) * UP)
            rows.append(VGroup(name, code).set_z_index(1))       # above the till/amt box
        cols = [VGroup(*r[1].find("till"), *r[1].find("amt")) for r in rows]
        box = SurroundingRectangle(VGroup(*cols), buff=0.13, corner_radius=0.1)
        box.set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.12)
        card.lower(q1, q2, *rows, box)

        with self.say("c6.ex.8") as c:
            # "Exercise four point four."
            self.play(*enter_card(self.strip, card), run_time=1.0)
            # "What do our making change functions assume about the till and the amount?"
            c.wait_until("task")
            self.play(FadeIn(q1, shift=0.2 * DOWN),
                      time_span(LaggedStart(*[FadeIn(r, shift=0.25 * RIGHT) for r in rows],
                                            lag_ratio=0.3), 0.6, 2.2),
                      run_time=2.2)
            c.wait_until("till")
            self.play(*[g.animate.set_color(YELLOW) for grp in cols for g in grp],
                      FadeIn(box), run_time=1.0)
            # "And what could happen if those assumptions were broken?"
            c.wait_until("happen")
            self.play(FadeIn(q2, shift=0.2 * DOWN), run_time=1.0)
        card.keep(q1, q2, *rows, box)
        self.card, self.rows = card, rows

    # ── c6.ex.9: the hint, four odd inputs ───────────────────────────────────────────
    def hint44(self):
        card = self.card
        hl = hint_label(card)
        chips = []
        for k, text in enumerate(CHIPS):
            ch = chip(text)
            ch.move_to([CHIP_COLS[k % 2], CHIP_ROWS[k // 2], 0], aligned_edge=LEFT)
            chips.append(ch)
        warn = T("think before you run it", size=30, color=RED)
        warn.next_to(hl, RIGHT, buff=0.7).align_to(hl, DOWN)

        with self.say("c6.ex.9") as c:
            # "Here's the hint."
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # "Try some odd inputs, and ask what each version does."
            c.wait_until("each version")
            self.play(*[r[0].animate.set_color(FG) for r in self.rows],
                      LaggedStart(*[FlashUnder(r[0], color=YELLOW) for r in self.rows],
                                  lag_ratio=0.25), run_time=1.2)
            # "A coin worth zero." "An amount below zero." "Coins in the wrong order, ..."
            for k, ch in enumerate(chips):
                c.wait_until(CHIP_CUES[k])
                nxt = CHIP_CUES[k + 1] if k < 3 else "careful"
                self.play(FadeIn(ch, shift=0.25 * DOWN), run_time=fit(c, nxt, lo=0.7, hi=1.0))
            # "With the coin of zero, think before you run it."
            c.wait_until("careful")
            first = chips[0]
            self.play(first[0].animate.set_stroke(RED, 4),
                      FlashAround(first, color=RED, run_time=1.5, time_width=1.5),
                      time_span(FadeIn(warn, shift=0.2 * DOWN), 0.5, 1.5), run_time=1.5)
            # "Pause, and try it."
            self.pause(c)
        self.hint = [hl, *chips, warn]

    # ── c6.ex.10: card 4.5 ───────────────────────────────────────────────────────────
    def ex45(self):
        card = HeroCard(4, height=H45)
        l1 = left_at(T("Two coin values: show there are O(n) ways", size=34, t2c={"O(n)": GOLD}),
                     T45_Y[0])
        l2 = left_at(T("to make change for n (ignoring order).", size=34), T45_Y[1])
        l3 = left_at(T("Three values?  Four?  …", size=34), T45_Y[2])
        p1, p2 = t_part(l1, "Two coin values:"), t_part(l1, "show there are O(n) ways")
        p3, p4 = t_part(l2, "to make change for n"), t_part(l2, "(ignoring order).")
        card.lower(p1, p2, p3, p4, l3)
        a, b = coin_row([5, 2, 2]), coin_row([2, 5, 2])
        eq = MathTex("=", font_size=60, color=FG)
        one = T("count as one", size=32)
        example = VGroup(a, eq, b, one).arrange(RIGHT, buff=0.5).move_to([0, EX45_Y, 0])
        one.shift(0.3 * RIGHT)

        with self.say("c6.ex.10") as c:
            # "Exercise four point five."
            self.next_card(card)
            # "Suppose there are just two coin values."
            c.wait_until("task")
            self.play(FadeIn(p1, shift=0.2 * DOWN), run_time=1.0)
            # "Show that for an amount en, the number of ways to make change is big O of en."
            c.wait_until("Show that")
            self.play(FadeIn(p2, shift=0.2 * DOWN), time_span(FadeIn(p3, shift=0.2 * DOWN), 0.5, 1.4),
                      run_time=1.4)
            # "Here, two solutions with the same coins in a different order count as one."
            c.wait_until("order")
            self.play(FadeIn(p4, shift=0.2 * DOWN),
                      LaggedStart(*[FadeIn(m, scale=0.8) for m in a], lag_ratio=0.2), run_time=1.0)
            self.play(TransformFromCopy(a[0], b[1], path_arc=-PI / 2),
                      TransformFromCopy(a[1], b[0], path_arc=-PI / 2),
                      TransformFromCopy(a[2], b[2]), run_time=1.4)
            c.wait_until("count as one")
            self.play(GrowFromCenter(eq), FadeIn(one, shift=0.2 * LEFT), run_time=0.9)
            # "Then ask the same question for three coin values, or four, or more."
            c.wait_until("more")
            self.play(FadeIn(l3, shift=0.2 * DOWN), run_time=1.0)
        card.keep(p1, p2, p3, p4, l3)
        self.example = example

    # ── c6.ex.11: the hint, fix the 5s, then the rest ─────────────────────────────────
    def hint45(self):
        card = self.card
        hl = hint_label(card)
        c5, c2 = coin(5, r=PIC_R), coin(2, r=PIC_R)
        amount = T("amount", size=36, color=DIM)
        n = T("n", size=50, color=GOLD, slant=ITALIC)
        top = VGroup(c5, c2).arrange(RIGHT, buff=0.3)
        left_at(top, PIC_Y[0])
        amount.next_to(top, RIGHT, buff=0.8)
        n.next_to(amount, RIGHT, buff=0.22).align_to(amount, DOWN)
        ask = left_at(T("how many 5s?", size=36, t2c={"5s": GOLD}), PIC_Y[1])
        cnt = T("0", size=48, color=GOLD).next_to(ask, RIGHT, buff=0.4)
        x0 = cnt.get_right()[0] + 0.6 + SMALL_R
        fives = [coin(5, r=SMALL_R).move_to([x0 + k * (2 * SMALL_R + 0.14), PIC_Y[1], 0])
                 for k in range(2)]
        dots = T("…", size=44).next_to(fives[-1], RIGHT, buff=0.25)
        rest = left_at(T("the rest in 2s", size=36, t2c={"2s": GOLD}), PIC_Y[2])
        two = coin(2, r=SMALL_R).next_to(rest, RIGHT, buff=0.4)
        q = gold_q(48).next_to(two, RIGHT, buff=0.4)
        left = VGroup(top, amount, n, ask, cnt, *fives, dots, rest, two, q)
        brace = Brace(left, direction=RIGHT, buff=0.3, color=DIM)
        n5, n2, n1 = coin(5, r=0.5), coin(2, r=0.5), coin(1, r=0.5)
        three = VGroup(n5, n2, n1).arrange(RIGHT, buff=0.3)
        three.move_to([brace.get_right()[0] + 1.5 + three.width / 2, brace.get_y(), 0])
        back = Arrow(three.get_left() + 0.1 * LEFT, brace.get_right() + 0.1 * RIGHT,
                     color=YELLOW, buff=0.1, stroke_width=5)

        with self.say("c6.ex.11") as c:
            # "Here's the hint."
            self.play(*card.lift(), *[FadeOut(m) for m in self.example],
                      time_span(FadeIn(hl, shift=0.25 * DOWN), 0.5, 1.2),
                      time_span(FadeIn(top, amount, n, shift=0.2 * DOWN), 0.8, 1.5), run_time=1.5)
            # "With two coins, first decide how many of the larger coin you'll use."
            c.wait_until("fix")
            self.play(FadeIn(ask, shift=0.2 * DOWN), FadeIn(cnt, shift=0.2 * DOWN), run_time=0.8)
            self.wait(0.3)
            for k, rt in ((1, 0.8), (2, 0.6)):
                self.play(Transform(cnt, T(str(k), size=48, color=GOLD).move_to(cnt)),
                          TransformFromCopy(c5, fives[k - 1]), run_time=rt)
                self.wait(0.15)
            self.play(FadeIn(dots, shift=0.2 * RIGHT), run_time=0.5)
            # "Once that's fixed, how many ways are left for the smaller one?"
            c.wait_until("rest")
            self.play(FadeIn(rest, shift=0.2 * DOWN), TransformFromCopy(c2, two),
                      time_span(FadeIn(q, scale=1.3), 0.8, 1.5), run_time=1.5)
            # "For more coins, build on the case you just solved."
            c.wait_until("build")
            self.play(TransformFromCopy(c5, n5), TransformFromCopy(c2, n2),
                      time_span(FadeIn(n1, shift=0.6 * LEFT), 0.6, 1.4), run_time=1.4)
            self.play(GrowFromCenter(brace), GrowArrow(back), run_time=1.0)
            # "Pause, and work it out."
            self.pause(c)
        self.hint = [hl, left, brace, three, back]

    # ── c6.ex.12: card 4.6, two types and two calls ─────────────────────────────────
    def ex46(self):
        card = HeroCard(5, height=H46)
        pf, tf = split_code(EX46_TYPES[0], ["val f :", "'a * 'b -> 'b * 'a"], SIG_Y[0])
        pg, tg = split_code(EX46_TYPES[1], ["val g :", "'a -> 'a list"], SIG_Y[1])
        ret = VGroup(*tf.find("'b * 'a"))
        fc = code_at(EX46_CALLS[0], CALL_Y, key="1")
        gc = code_at(EX46_CALLS[1], CALL_Y, x=COL_X + 8.1, key="0")
        fa = MathTex(r"\Rightarrow", font_size=52, color=DIM).next_to(fc, RIGHT, buff=0.4)
        ga = MathTex(r"\Rightarrow", font_size=52, color=DIM).next_to(gc, RIGHT, buff=0.4)
        fa.set_y(fc.find("1").get_y())
        ga.set_y(fa.get_y())
        fq = gold_q().next_to(fa, RIGHT, buff=0.4)
        gq = gold_q().next_to(ga, RIGHT, buff=0.4)
        ask = left_at(T("What will the results be, and why?", size=34), ASK_Y)
        card.lower(pf, tf, pg, tg, fc, gc, fa, ga, fq, gq, ask)

        with self.say("c6.ex.12") as c:
            # "The last exercise, four point six, is about types."
            self.next_card(card)
            # "We know nothing about two functions, eff and gee, except their types."
            c.wait_until("fg")
            self.play(FadeIn(pf, shift=0.2 * DOWN), time_span(FadeIn(pg, shift=0.2 * DOWN), 0.3, 1.2),
                      run_time=1.2)
            # "The function eff takes a pair of an alpha and a beta, and returns a pair of ..."
            c.wait_until("ftype")
            self.play(Write(tf), run_time=1.6)
            c.wait_until("returns")
            self.play(FlashUnder(ret, color=YELLOW), run_time=1.0)
            # "The function gee takes an alpha, and returns an alpha list."
            c.wait_until("gtype")
            self.play(Write(tg), run_time=1.3)
            # "Suppose we apply eff to the pair one and true, and gee to zero, and both return."
            c.wait_until("calls")
            self.play(FadeIn(fc, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("and gee")
            self.play(FadeIn(gc, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("both return")
            self.play(GrowFromCenter(fa), GrowFromCenter(ga),
                      time_span(FadeIn(fq, scale=1.3), 0.4, 1.2),
                      time_span(FadeIn(gq, scale=1.3), 0.4, 1.2), run_time=1.2)
            # "What will the results be, and why?"
            c.wait_until("ask")
            self.play(FadeIn(ask, shift=0.2 * DOWN), run_time=1.0)
        card.keep(pf, tf, pg, tg, fc, gc, fa, ga, fq, gq, ask)
        self.calls = (fc, gc, fa, fq, gq, ask)

    # ── c6.ex.13: the hint, what id can and can't do ───────────────────────────────
    def hint46(self):
        card = self.card
        fc, gc, fa, fq, gq, ask = self.calls
        hl = T("Hint · from lecture 3", size=32, color=DIM, t2c={"Hint": YELLOW})
        hl.move_to([COL_X, card.bottom - 0.4, 0], aligned_edge=LEFT)
        idl = code_at(ID_SRC[0], ID_Y[0], size=32, key="let")
        idt = code_at(ID_SRC[1], ID_Y[1], size=32, key="val")
        for m in (idl, idt):
            m.set_opacity(CODE_DIM)
        alphas = [idt.find("'a", nth=k) for k in (0, 1)]
        cap = T("knows nothing about 'a", size=32, t2c={"'a": PINK}, t2f={"'a": MONO})
        cap.next_to(idt, RIGHT, buff=0.7)
        body, param = idl.find("x", nth=1), idl.find("x", nth=0)
        box = token_box(body, idl, color=YELLOW)
        hook = dashed_arc(body.get_top() + 0.08 * UP, param.get_top() + 0.08 * UP,
                          angle=PI * 0.45, num_dashes=8, tip=0.16)

        with self.say("c6.ex.13") as c:
            # "The hint goes back to eye-dee, in lecture three."
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            self.play(FadeIn(idl, shift=0.2 * UP), time_span(FadeIn(idt, shift=0.2 * UP), 0.3, 1.2),
                      run_time=1.2)
            # "A function whose type says alpha knows nothing about alpha."
            c.wait_until("nothing")
            self.play(*[g.animate.set_opacity(1) for al in alphas for g in al],
                      *[FlashAround(al, color=PINK, run_time=1.5, time_width=1.5) for al in alphas],
                      time_span(FadeIn(cap, shift=0.2 * DOWN), 0.6, 1.5), run_time=1.5)
            # "It has no way to make up a value of that type."
            c.wait_until("invent")
            self.play(FadeIn(box), *[g.animate.set_opacity(1) for g in body], run_time=1.0)
            # "It can only use the ones you give it."
            c.wait_until("It can only use")
            self.play(Create(hook[0]), time_span(FadeIn(hook[1]), 0.8, 1.2),
                      *[g.animate.set_opacity(1) for g in param], run_time=1.2)
            # "So for each part of each result, ask where it could have come from."
            c.wait_until("where")
            lp, comma, rp = (Mono(s, size=SIG_SIZE) for s in "(,)")
            q1, q2 = gold_q(), gold_q()
            pair = VGroup(lp, q1, comma, q2, rp).arrange(RIGHT, buff=0.18)
            comma.align_to(lp, DOWN).shift(0.08 * UP)
            pair.next_to(fa, RIGHT, buff=0.4)
            self.play(ReplacementTransform(fq, q1), TransformFromCopy(fq, q2),
                      FadeIn(lp, comma, rp), FadeOut(ask), run_time=1.2)
            card.shown.remove(fq)
            card.shown.remove(ask)
            card.keep(lp, q1, comma, q2, rp)
            # both of f's slots point at the argument pair as a whole (no slot is matched to
            # an argument: that would be the answer)
            args = VGroup(*fc.find("(1, true)"))
            under = underline(args, DIM, buff=0.12)
            tgt = under.get_center() + 0.06 * DOWN
            zero = VGroup(*gc.find("0"))
            arrows = [dashed_arc(q1.get_bottom() + 0.1 * DOWN, tgt, angle=-PI * 0.4),
                      dashed_arc(q2.get_bottom() + 0.1 * DOWN, tgt, angle=-PI * 0.4),
                      dashed_arc(gq.get_bottom() + 0.1 * DOWN, zero.get_bottom() + 0.12 * DOWN,
                                 angle=-PI * 0.6, num_dashes=8)]
            self.play(Create(under), *[time_span(Create(a[0]), 0.3, 1.5) for a in arrows],
                      *[time_span(FadeIn(a[1]), 1.2, 1.6) for a in arrows], run_time=1.6)
            # "Pause, and think it through."
            self.pause(c)
        self.hint = [hl, idl, idt, cap, box, *hook, under, *[m for a in arrows for m in a]]
