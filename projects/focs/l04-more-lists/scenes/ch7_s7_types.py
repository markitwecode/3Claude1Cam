"""STATUS: done; vk check clean (107.2 s for 95.0 s of narration).
Departures: the verified g examples show only their definitions beside [0] and [0; 0] (the
replies do not fit beside the fan); loop sits under both boxes, not beside them.

Chapter 7, scene 7: exercise 4.6 solved, what the types force. Clips c7.types.1 – c7.types.5.

PLAN
Opens like s2–s6: ch6's strip (4.1–4.5 done, 4.6 current) fades in, card 4.6 grows out of its
pill (the two types, size 44 as ch6_s6 draws them; `f (1, true) ⇒ ?`, `g 0 ⇒ ?`), the pause tag,
a still beat, then it shrinks back into its pill, which stays CURRENT (as ch7_s2). The strip stays
as the header until the final fade.
- c7.types.2: L3's id machine (dimmed) with `val id : 'a -> 'a = <fun>` above it; its 'a flash,
  a GOLD "?" in the box is crossed RED; a token x passes straight through. {fapp}: the id machine
  becomes f's (same place), the top line becomes f's type, `(1, true)` waits on the input with
  GREEN tags 'a = int / 'b = bool. {only}: 1 and true are alone inside the box. {answer}: they
  swap and leave as `(true, 1)`.
- c7.types.3: f shrinks to a row at the top, `(1, true) -> [f] -> (true, 1)`; below it the
  honest code and replies (the reply's `(true, 1)` comes from the row), then the cheat; its
  `bool * int` boxed RED, the required `'b * 'a` boxed GREEN.
- c7.types.4: g's machine under the f row; 0 goes in, 0 discs come out, "how many?". {any}: g
  moves left and its output fans out to [], [0], [0; 0], [0; 0; 0], …, two with the code that
  produces them, each with a GREEN check.
- c7.types.5: g joins f as a row; L3's loop (box, circular arrow, its reply) dimmed under both;
  the outputs dim (might never come), come back on {given}; {lesson}: (true, 1) GREEN,
  [0; …; 0] GREEN with a GOLD "?" for its length.

Verified (brief, ocaml 5.4.1): let f (x, y) = (y, x) -> val f : 'a * 'b -> 'b * 'a = <fun>;
f (1, true) -> - : bool * int = (true, 1); let f (x, y) = (true, 1) ->
val f : 'a * 'b -> bool * int = <fun>; let g x = [x] / [x; x] -> val g : 'a -> 'a list = <fun>,
g 0 -> - : int list = [0] / [0; 0].
"""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, VShowPassingFlash, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch6_s5_hints1 import (  # noqa: E402  the shared exercise-card kit (read-only)
    CARD_FILL, CARD_TOP, COL_X, CURRENT, DONE, EX46_CALLS, EX46_TYPES, HeroCard, enter_card,
    hold_for, make_strip, pause_tag, row_y, split_line,
)

# card 4.6 (as ch6_s6 draws it)
SIG = 44
STEP = 0.9
CALL_K = 3.4
CARD_H = CARD_TOP - (row_y(CALL_K, STEP) - 0.75)

# the solution
ID_OP = 0.5          # L3's id, recalled: dimmed
LOOP_OP = 0.45       # L3's loop, recalled: dimmed
TOP_Y = 1.95         # the reference line over the id / f machine
MY = -0.7            # the id / f machine (c7.types.2)
SLOT = 0.6           # the two value slots inside f's box, at x = -SLOT / +SLOT
FY = 2.1             # f's row (c7.types.3 - 5)
CS = 34              # the code under f's row
CX = -5.6            # its left edge
R_Y = (0.75, 0.12, -0.6, -1.55, -2.18)
GY = -0.8            # g's machine (c7.types.4)
GBX = -4.0          # g's box once its output fans out
FAN_X = -1.6         # left edge of the fan of possible results
FAN_STEP = 0.75
PILL_X = 3.7         # values on f's arrows sit at x = -PILL_X / +PILL_X
LAB_DY = 0.78        # the types above a machine's arrows
G5 = 0.45            # g's row (c7.types.5)
LY = -1.45           # loop (c7.types.5)


def gold_q(size=48):
    return T("?", size=size, color=GOLD, weight=BOLD)


def piece(code, sub, nth=0):
    """Copies of a substring's glyphs, in place: an independent top-level mobject."""
    return VGroup(*[g.copy() for g in code.find(sub, nth=nth)])


def pill(text, color=PINK):
    """A value on its way into a machine (L3's look)."""
    box = RoundedRectangle(corner_radius=0.3, width=text.width + 0.5, height=0.66)
    return box.set_stroke(color, 3).set_fill(BG, 1).move_to(text)


def pink_arrow(a, b, width=5, ratio=0.1):
    return Arrow(a, b, buff=0, stroke_width=width, color=PINK, max_tip_length_to_length_ratio=ratio)


def hero_machine(name, y, in_src, out_src=None, cx=0.0, w=3.2, h=1.9, x_in=-5.6, x_out=5.6):
    """L3's machine (ch6_s5): a BLUE box, its name YELLOW above it, PINK arrows in and out,
    the types they carry above them."""
    box = RoundedRectangle(corner_radius=0.22, width=w, height=h)
    box.set_stroke(BLUE, 4).set_fill(CARD_FILL, 1).move_to([cx, y, 0])
    lab = Mono(name, size=48, color=YELLOW).next_to(box, UP, buff=0.22)
    inp = pink_arrow([x_in, y, 0], box.get_left())
    la = Code(in_src, size=40).move_to([inp.get_x(), y + LAB_DY, 0])
    m = SimpleNamespace(box=box, name=lab, inp=inp, la=la, parts=[box, lab, inp, la])
    if out_src is not None:
        m.out = pink_arrow(box.get_right(), [x_out, y, 0])
        m.lb = Code(out_src, size=40).move_to([m.out.get_x(), y + LAB_DY, 0])
        m.parts += [m.out, m.lb]
    return m


def row_machine(name, y, in_src, out_src, cx=0.0):
    """The same machine as one row: value -> [name] -> value."""
    box = RoundedRectangle(corner_radius=0.18, width=1.8, height=1.0)
    box.set_stroke(BLUE, 4).set_fill(CARD_FILL, 1).move_to([cx, y, 0])
    lab = Mono(name, size=40, color=YELLOW).move_to(box)
    inp = pink_arrow(box.get_left() + LEFT * 1.0, box.get_left(), width=4, ratio=0.3)
    out = pink_arrow(box.get_right(), box.get_right() + RIGHT * 1.0, width=4, ratio=0.3)
    vin = Code(in_src, size=CS).next_to(inp, LEFT, buff=0.18)
    vout = Code(out_src, size=CS).next_to(out, RIGHT, buff=0.18)
    return SimpleNamespace(box=box, name=lab, inp=inp, out=out, vin=vin, vout=vout,
                           parts=[box, lab, inp, out, vin, vout])


def type_tag(var, ty, size=32):
    """`'a = int`: the variable PINK, the type it stands for GREEN (as L3)."""
    v = Mono(f"{var} =", size=size, t2c={var: PINK})
    t = Mono(ty, size=size, color=GREEN)
    return VGroup(v, t).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)


def zero_disc(r=0.32):
    c = Circle(radius=r).set_stroke(GOLD, 3).set_fill(CARD_FILL, 1)
    return VGroup(c, Mono("0", size=34, color=GOLD).move_to(c))


def fades_in(mobs, start, end, **kw):
    return [time_span(FadeIn(m, **kw), start, end) for m in mobs]


def fades_out(mobs, **kw):
    return [FadeOut(m, **kw) for m in mobs]


class WhatTheTypesForce(NarratedScene):
    def construct(self):
        self.strip = make_strip([DONE] * 5 + [CURRENT])
        self.play(FadeIn(self.strip), run_time=0.8)
        self.card_beat()
        self.id_to_f()
        self.code_beat()
        self.g_beat()
        self.caveat()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c7.types.1: card 4.6 ───────────────────────────────────────────────────────
    def card_beat(self):
        card = HeroCard(5, CARD_H, step=STEP)
        f_val, f_ty = split_line(EX46_TYPES[0], ["val f :", "'a * 'b -> 'b * 'a"], size=SIG, k=1, step=STEP)
        g_val, g_ty = split_line(EX46_TYPES[1], ["val g :", "'a -> 'a list"], size=SIG, k=2, step=STEP)
        want = VGroup(*f_val.find("val")).get_bottom()[1] - STEP
        dy = want - VGroup(*g_val.find("val")).get_bottom()[1]
        g_val.shift(dy * UP)
        g_ty.shift(dy * UP)

        fc = Code(EX46_CALLS[0], size=SIG).move_to([COL_X, row_y(CALL_K, STEP), 0], aligned_edge=LEFT)
        gc = Code(EX46_CALLS[1], size=SIG).move_to([COL_X + 8.1, 0, 0], aligned_edge=LEFT)
        gc.shift((VGroup(*fc.find("1")).get_bottom()[1] - VGroup(*gc.find("0")).get_bottom()[1]) * UP)
        fa = MathTex(r"\Rightarrow", font_size=52, color=DIM).next_to(fc, RIGHT, buff=0.4)
        ga = MathTex(r"\Rightarrow", font_size=52, color=DIM).next_to(gc, RIGHT, buff=0.4)
        fq = gold_q().next_to(fa, RIGHT, buff=0.4)
        gq = gold_q().next_to(ga, RIGHT, buff=0.4)
        items = [f_val, f_ty, g_val, g_ty, fc, gc, fa, ga, fq, gq]
        card.lower(*items)
        card.keep(*items)
        tag = pause_tag()

        with self.say("c7.types.1") as c:
            # "Exercise four point six."  The card grows out of its pill.
            self.play(*enter_card(self.strip, card, light=False), run_time=1.3)
            # "All we know about two functions, eff and gee, is their types."
            c.wait_until("eff and gee")
            self.play(LaggedStart(FadeIn(f_val, shift=0.2 * DOWN), FadeIn(g_val, shift=0.2 * DOWN),
                                  lag_ratio=0.3), run_time=1.2)
            # "The first, eff, takes an alpha times beta to a beta times alpha."
            c.wait_until("f")
            self.play(Write(f_ty), run_time=1.6)
            # "The second, gee, takes an alpha to an alpha list."
            c.wait_until("g")
            self.play(Write(g_ty), run_time=1.3)
            # "Suppose eff of one, true, and gee of zero both return."
            c.wait_until("ask")
            self.play(FadeIn(fc, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("and gee of zero")
            self.play(FadeIn(gc, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("both return")
            self.play(GrowFromCenter(fa), GrowFromCenter(ga),
                      time_span(FadeIn(fq, scale=1.3), 0.4, 1.2),
                      time_span(FadeIn(gq, scale=1.3), 0.4, 1.2), run_time=1.2)
            # "What are the results?"
            c.wait_until("What are the results")
            self.play(FlashAround(fq, color=GOLD, time_width=1.5), FlashAround(gq, color=GOLD, time_width=1.5),
                      run_time=1.3)
            # "Pause, and reason it out."
            c.wait_until("stop")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.8)
            born = self.time
        hold_for(self, born, len("pause and try it"))
        self.card, self.pause = card, tag

    # ── c7.types.2: id can only hand back what it was given; so f must swap ──────────
    def id_to_f(self):
        id_line = Code("val id : 'a -> 'a = <fun>", size=36)
        l3 = T("Lecture 3", size=28, color=DIM)
        VGroup(id_line, l3).arrange(RIGHT, buff=0.6).move_to([0, TOP_Y, 0])
        id_line.set_opacity(0.6)
        idm = hero_machine("id", MY, "'a", "'a")
        for m in idm.parts:
            m.set_opacity(ID_OP)
        q = T("?", size=84, color=GOLD).move_to(idm.box)
        cross = cross_mark(RED, r=0.42).move_to(q)
        token_pill = RoundedRectangle(corner_radius=0.25, width=0.8, height=0.5)
        token_pill.set_stroke(PINK, 3).set_fill(PINK, 0.35).move_to([-4.6, MY, 0])

        f_line = Code(EX46_TYPES[0], size=40).move_to([0, TOP_Y, 0])
        fm = hero_machine("f", MY, "'a * 'b", "'b * 'a")
        in_code = Code("(1, true)", size=36).move_to([-PILL_X, MY, 0])
        in_box = pill(in_code)
        one, tru = piece(in_code, "1"), piece(in_code, "true")
        tag_a = type_tag("'a", "int").move_to([-4.7, MY - 0.8, 0], aligned_edge=LEFT)
        tag_b = type_tag("'b", "bool").move_to([-4.7, MY - 1.35, 0], aligned_edge=LEFT)
        out_code = Code("(true, 1)", size=36).move_to([PILL_X, MY, 0])
        out_box = pill(out_code)

        with self.say("c7.types.2") as c:
            # "Remember eye-dee, from lecture three."  The card goes home; L3's id, dimmed.
            # (as ch7_s2: the frame lands on the pill as it is, so 4.6 stays CURRENT until the end)
            self.play(*[FadeOut(m) for m in (*self.card.shown, self.pause)],
                      Transform(self.card.frame, self.strip[5].frame.copy()),
                      *fades_in([id_line, l3, *idm.parts], 0.5, 1.5), run_time=1.5)
            self.remove(self.card.frame)
            # "A function that knows nothing about alpha has no way to invent one."
            c.wait_until("knows nothing")
            self.play(idm.la.animate.set_opacity(1), idm.lb.animate.set_opacity(1),
                      FlashAround(idm.la, color=PINK, time_width=1.5),
                      FlashAround(idm.lb, color=PINK, time_width=1.5),
                      time_span(FadeIn(q, scale=0.6), 0.5, 1.3), run_time=1.3)
            c.wait_until("invent")
            self.play(Create(cross), q.animate.set_opacity(0.45), run_time=0.9)
            # "It can only hand back what it was given."  x in, the same x out.
            c.wait_until("only hand back")
            self.play(FadeIn(token_pill, shift=0.4 * RIGHT), run_time=0.5)
            path = Line([-5.6, MY, 0], [5.6, MY, 0]).set_stroke(YELLOW, 8)
            self.play(token_pill.animate.move_to([4.6, MY, 0]), VShowPassingFlash(path, time_width=0.5),
                      run_time=1.8)

            # "For eff of one, true, alpha is int, and beta is bool."  id's machine becomes f's.
            c.wait_until("fapp")
            self.play(FadeOut(q), FadeOut(cross), FadeOut(token_pill), FadeOut(l3),
                      *[ReplacementTransform(getattr(idm, k), getattr(fm, k))
                        for k in ("box", "name", "inp", "out", "la", "lb")],
                      FadeTransform(id_line, f_line),
                      *fades_in([in_box, in_code], 1.0, 1.6, shift=0.4 * RIGHT),
                      run_time=1.6)
            c.wait_until("alpha is int")
            self.play(FadeIn(tag_a, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("beta is bool")
            self.play(FadeIn(tag_b, shift=0.3 * DOWN), run_time=0.8)

            # "The only int that eff has is one, and the only bool is true."  Alone in the box.
            c.wait_until("only")
            self.add(one, tru)
            self.play(one.animate.set_x(-SLOT), tru.animate.set_x(SLOT), run_time=1.4)
            c.wait_until("eff has is one")
            self.play(FlashAround(one, color=GOLD, time_width=1.5), FlashAround(tag_a, color=GREEN, time_width=1.5),
                      run_time=1.1)
            c.wait_until("only bool is true")
            self.play(FlashAround(tru, color=GOLD, time_width=1.5), FlashAround(tag_b, color=GREEN, time_width=1.5),
                      run_time=1.1)

            # "So it must swap them, giving true, one."
            c.wait_until("answer")
            self.play(one.animate(path_arc=PI * 0.9).set_x(SLOT), tru.animate(path_arc=PI * 0.9).set_x(-SLOT),
                      run_time=1.3)
            c.wait_until("giving")
            parts = [piece(out_code, s) for s in ("(", ",", ")")]
            o_true, o_one = piece(out_code, "true"), piece(out_code, "1")
            self.play(ReplacementTransform(tru, o_true), ReplacementTransform(one, o_one),
                      *fades_in([out_box, *parts], 0.6, 1.4), run_time=1.4)
            self.remove(o_true, o_one, *parts)
            self.add(out_code)
        self.fm, self.f_line, self.f_out, self.f_in = fm, f_line, (out_box, out_code), (in_box, in_code)
        self.f_tags = (tag_a, tag_b)

    # ── c7.types.3: the obvious code has exactly this type; a cheat does not ──────────
    def code_beat(self):
        fm, (out_box, out_code) = self.fm, self.f_out
        fr = row_machine("f", FY, "(1, true)", "(true, 1)")
        r1 = Code("let f (x, y) = (y, x)", size=CS)
        r2 = Code("val f : 'a * 'b -> 'b * 'a = <fun>", size=CS)
        r3a = Code("f (1, true)", size=CS)
        r3b = Code("- : bool * int = (true, 1)", size=CS)
        r4 = Code("let f (x, y) = (true, 1)", size=CS)
        r5 = Code("val f : 'a * 'b -> bool * int = <fun>", size=CS)
        for r, y in zip((r1, r2, r3a, r4, r5), R_Y):
            r.move_to([CX, y, 0], aligned_edge=LEFT)
        r3b.next_to(r3a, RIGHT, buff=0.85)
        r3b.shift((VGroup(*r3a.find("(")).get_bottom()[1] - VGroup(*r3b.find("(")).get_bottom()[1]) * UP)
        b_req = token_box(r2.find("'b * 'a"), r2, color=GREEN)
        b_bad = token_box(r5.find("bool * int"), r5, color=RED)
        ok = check_mark(GREEN).next_to(r2, RIGHT, buff=0.4)
        bad = cross_mark(RED, r=0.17).next_to(r5, RIGHT, buff=0.45)

        with self.say("c7.types.3") as c:
            # "The obvious code, eff of ex, why, equals why, ex, has exactly this type."
            self.play(*[ReplacementTransform(getattr(fm, k), getattr(fr, k)) for k in ("box", "name", "inp", "out")],
                      ReplacementTransform(out_code, fr.vout), FadeOut(out_box),
                      ReplacementTransform(self.f_in[1], fr.vin), FadeOut(self.f_in[0]),
                      *fades_out([fm.la, fm.lb, *self.f_tags, self.f_line]), run_time=1.3)
            self.play(Write(r1), run_time=min(2.0, max(0.8, 0.8 * c.until("has exactly"))))
            c.wait_until("has exactly")
            pa, pb = piece(r3b, "- : bool * int ="), piece(r3b, "(true, 1)")
            self.play(FadeIn(r2, shift=0.2 * DOWN),
                      time_span(FadeIn(r3a, shift=0.2 * DOWN), 0.5, 1.2),
                      time_span(FadeIn(pa, shift=0.2 * DOWN), 0.6, 1.3),
                      time_span(TransformFromCopy(fr.vout, pb), 0.5, 1.5), run_time=1.5)
            self.remove(pa, pb)
            self.add(r3b)
            # "Cheat by always returning true, one, and the result type becomes bool times int, ..."
            c.wait_until("cheat")
            self.play(FadeIn(r4, shift=0.2 * DOWN), time_span(FadeIn(r5, shift=0.2 * DOWN), 0.5, 1.3),
                      run_time=1.3)
            c.wait_until("bool times int")
            self.play(FadeIn(b_bad), FlashAround(VGroup(*r5.find("bool * int")), color=RED, time_width=1.5),
                      run_time=1.1)
            # "... which no longer matches beta times alpha."
            c.wait_until("beta times alpha")
            self.play(FadeIn(b_req), Create(ok), Create(bad), run_time=1.0)
        self.wait(1.3)      # the mismatch, read
        self.fr = fr
        self.code_rows = [r1, r2, r3a, r3b, r4, r5, b_req, b_bad, ok, bad]

    # ── c7.types.4: g 0 is a list of zeros; how many? any number ──────────────────
    def g_beat(self):
        gm = hero_machine("g", GY, "'a", "'a list")
        disc = zero_disc().move_to([gm.inp.get_x(), GY, 0])
        tag = type_tag("'a", "int").move_to([gm.inp.get_x(), GY - 0.85, 0])
        outs = [zero_disc().move_to([2.6 + 1.1 * k, GY, 0]) for k in range(3)]
        hm = T("how many?", size=40, color=GOLD).move_to([3.6, GY - 0.95, 0])

        gb = hero_machine("g", GY, "'a", cx=GBX, w=2.2, h=1.4, x_in=-6.5)
        gb.la.move_to([gb.inp.get_x(), GY + 0.55, 0])
        srcs = ["[]", "[0]", "[0; 0]", "[0; 0; 0]"]
        entries = [Code(s, size=40) for s in srcs] + [T("…", size=48)]
        ys = [GY + FAN_STEP * (2 - k) for k in range(5)]
        for e, y in zip(entries, ys):
            e.move_to([FAN_X, y, 0], aligned_edge=LEFT)
        fan = [Arrow(gb.box.get_right(), [FAN_X - 0.15, y, 0], buff=0.08, stroke_width=3, color=PINK,
                     max_tip_length_to_length_ratio=0.2, tip_length=0.16) for y in ys]
        checks = [check_mark(GREEN).move_to([FAN_X + 3.45, y, 0]) for y in ys[:4]]
        ex = [Code("let g x = [x]", size=30), Code("let g x = [x; x]", size=30)]
        for e, y in zip(ex, ys[1:3]):
            e.move_to([FAN_X + 3.95, y, 0], aligned_edge=LEFT).set_opacity(0.75)

        with self.say("c7.types.4") as c:
            # "Now gee of zero."  The code clears; g's machine under f's row; 0 goes in.
            self.play(LaggedStart(*fades_out(self.code_rows, shift=0.2 * DOWN), lag_ratio=0.08),
                      *fades_in(gm.parts, 0.6, 1.4), time_span(FadeIn(disc, shift=0.4 * RIGHT), 0.9, 1.4),
                      run_time=1.4)
            self.play(disc.animate.move_to(gm.box), run_time=0.9)
            # "It must return a list of alphas, and the only alpha it has is zero."
            c.wait_until("It must return")
            self.play(FlashAround(gm.lb, color=PINK, time_width=1.5), run_time=1.2)
            c.wait_until("the only alpha")
            self.play(FadeIn(tag, shift=0.3 * DOWN), FlashAround(disc, color=GOLD, time_width=1.5), run_time=1.2)
            # "So the answer is a list of zeros."
            c.wait_until("zeros")
            self.play(LaggedStart(*[TransformFromCopy(disc, o) for o in outs], lag_ratio=0.3), run_time=1.8)
            # "But how many?"
            c.wait_until("howmany")
            self.play(FadeIn(hm, shift=0.2 * DOWN), run_time=0.9)

            # "It could be the empty list, a single zero, two zeros, or more."
            c.wait_until("any")
            e3 = entries[3]
            zs = [piece(e3, "0", nth=k) for k in range(3)]
            rest3 = [piece(e3, "["), piece(e3, ";", 0), piece(e3, ";", 1), piece(e3, "]")]
            self.play(*[ReplacementTransform(getattr(gm, k), getattr(gb, k)) for k in ("box", "name", "inp", "la")],
                      disc.animate.move_to(gb.box), tag.animate.move_to([GBX, GY - 1.2, 0]),
                      hm.animate.move_to([FAN_X + 2.0, GY - 2.3, 0]), *fades_out([gm.out, gm.lb]),
                      *[ReplacementTransform(o, z) for o, z in zip(outs, zs)], *fades_in(rest3, 0.7, 1.3),
                      time_span(GrowArrow(fan[3]), 0.6, 1.2), time_span(GrowArrow(fan[0]), 0.8, 1.4),
                      time_span(FadeIn(entries[0], shift=0.2 * RIGHT), 0.9, 1.5), run_time=1.5)
            self.remove(*zs, *rest3)
            self.add(e3)
            for k, cue in ((1, "single zero"), (2, "two zeros")):
                c.wait_until(cue)
                self.play(GrowArrow(fan[k]), time_span(FadeIn(entries[k], shift=0.2 * RIGHT), 0.2, 0.8),
                          time_span(FadeIn(ex[k - 1], shift=0.2 * LEFT), 0.25, 0.8), run_time=1.0)
            c.wait_until("or more")
            self.play(GrowArrow(fan[4]), time_span(FadeIn(entries[4], shift=0.2 * RIGHT), 0.3, 1.0), run_time=1.0)
            # "Each fits the type, so the type alone leaves the length open."
            c.wait_until("Each fits")
            self.play(LaggedStart(*[Create(m) for m in checks], lag_ratio=0.25), run_time=1.2)
        self.wait(0.2)      # the second example, read
        self.g = SimpleNamespace(m=gb, disc=disc, tag=tag, entries=entries, fan=fan, checks=checks, ex=ex, hm=hm)

    # ── c7.types.5: they might never return; when they do, the type decides ───────────
    def caveat(self):
        g, fr = self.g, self.fr
        gr = row_machine("g", G5, "0", "[0; …; 0]")
        lbox = RoundedRectangle(corner_radius=0.18, width=1.8, height=1.0)
        lbox.set_stroke(BLUE, 4).set_fill(CARD_FILL, 1).move_to([0, LY, 0])
        lname = Mono("loop", size=36, color=YELLOW).move_to(lbox)
        again = CurvedArrow(lbox.get_right() + DOWN * 0.2 + RIGHT * 0.04, lbox.get_left() + DOWN * 0.2 + LEFT * 0.04,
                            angle=-PI * 0.85, color=YELLOW, stroke_width=4, tip_length=0.2)
        lreply = Code("val loop : 'a -> 'b = <fun>", size=30).move_to([0, LY - 1.5, 0])
        for m in (lbox, lname, lreply):
            m.set_opacity(LOOP_OP)
        again.set_stroke(opacity=LOOP_OP)
        again.tip.set_fill(opacity=LOOP_OP).set_stroke(opacity=LOOP_OP)
        outs = [fr.out, fr.vout, gr.out, gr.vout]
        brace = Brace(gr.vout, DOWN, buff=0.12, color=DIM)
        length_q = gold_q(48).next_to(brace, DOWN, buff=0.12)
        hm_to = g.hm.copy().move_to([gr.vout.get_x(), G5 - 0.62, 0])

        with self.say("c7.types.5") as c:
            # "One caveat."  g's answers fold into one row under f's.
            mid = g.entries[3]
            self.play(*[ReplacementTransform(getattr(g.m, k), getattr(gr, k)) for k in ("box", "name", "inp")],
                      FadeTransform(g.disc, gr.vin), ReplacementTransform(g.fan[2], gr.out),
                      ReplacementTransform(mid, gr.vout),
                      *fades_out([g.m.la, g.tag, *g.checks, *[f for i, f in enumerate(g.fan) if i != 2],
                                  *[e for e in g.entries if e is not mid]]),
                      *[time_span(FadeOut(e), 0.3, 1.2) for e in g.ex],
                      time_span(Transform(g.hm, hm_to), 0.3, 1.4), run_time=1.4)
            # "Like loop in lecture three, either function could run forever, or raise an exception."
            c.wait_until("Like loop")
            self.play(*[FadeIn(m) for m in (lbox, lname, lreply)], time_span(Create(again), 0.3, 1.3), run_time=1.3)
            c.wait_until("run forever")
            self.play(*set_alpha(outs, DIMMED), run_time=1.0)
            # "That's why the exercise says they return."
            c.wait_until("given")
            paths = [Line(r.box.get_right(), r.vout.get_right()).set_stroke(YELLOW, 8) for r in (fr, gr)]
            self.play(*set_alpha(outs, 1), *[VShowPassingFlash(p, time_width=0.6) for p in paths], run_time=1.3)
            # "When they do, the type decides eff's answer completely, ..."
            c.wait_until("decides")
            self.play(fr.vout.animate.set_color(GREEN), FlashAround(fr.vout, color=GREEN, time_width=1.5),
                      run_time=1.2)
            # "... and gee's answer up to its length."
            c.wait_until("up to its length")
            self.play(gr.vout.animate.set_color(GREEN), GrowFromCenter(brace), FadeOut(g.hm),
                      TransformFromCopy(g.hm[-1], length_q), run_time=1.3)
            born = self.time
        hold_for(self, born, 8)
