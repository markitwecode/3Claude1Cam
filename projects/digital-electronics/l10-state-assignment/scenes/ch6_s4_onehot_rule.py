"""Chapter 6, scene 4: using "exactly one is hot": not s0 = s1 + s2, so D2 = not s0 . e . r + s2 . not e (p. 142). Clips c6.rule.1 – c6.rule.4.

Opens on ch6_s3_inspect.handover_shot() (d_stack); ends on an empty frame.
Shared helpers (load_scene("ch6_s4_onehot_rule")), all standalone:
- `check_table(rows=CHECK_ROWS, size=40)`: the check table, built with its header row at y 0 and
  x -3.25..4.25 (scale/shift it yourself). Columns: state name (YELLOW T 32, or "unused" DIM T 30),
  s_2 s_1 s_0 bits (Mono 36, 1s GOLD), | \\overline{s_0} | s_1 + s_2 | mark (GREEN tick / RED cross).
  rows: (name or None, "001", "0", "0", ok) tuples; CHECK_ROWS = Hunt, Sight, Sync, then 000.
  Attrs .head (VGroup of header pieces + its rule segment) .hrule .rows[i] (VGroup) with
  .name .bits (VGroup of 3) .a .s .mark .vr (its piece of the vertical rule).
- `rule_line(size=44, words=True)`: p. 142's "so, \\overline{s_0} = s_1 + s_2, hence," as one
  MathTex; VGroup(so, eq, hence) (words=False: VGroup(eq)), .so .eq .hence (.so/.hence None
  without words); .eq is a VGroup of the five maths pieces.
- `rule_words(size=30)`: "not Hunt = Sight or Sync" (DIM, names YELLOW).
- `sum_line(size=48)`: p. 142's s_2 + s_1 + s_0 = 1 with YELLOW name tags; .tex .tags.
- `final_d2(size=56)`: eq_line of D_2 = \\overline{s_0}.e.r + s_2.\\overline{e}.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch6_s2_codes")
S3 = load_scene("ch6_s3_inspect")
C34 = load_scene("ch3_s4_check")
eq_line, put_line = S3.eq_line, S3.put_line


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- shared: the check table
CHECK_ROWS = [("Hunt", "001", "0", "0", True), ("Sight", "010", "1", "1", True),
              ("Sync", "100", "1", "1", True), (None, "000", "1", "0", False)]
NAME_X, BIT_XS, VR_X, A_X, S_X, MARK_X = -2.6, (-1.4, -0.75, -0.1), 0.45, 1.15, 2.65, 3.9
ROW0_Y, ROW_PITCH, HR_Y = -0.75, 0.62, -0.38


def _digit(v, size=36, dim=False):
    return Mono(v, size, DIM if dim else (GOLD if v == "1" else FG))


def check_table(rows=CHECK_ROWS, size=40):
    head = VGroup()
    for x, s in zip(BIT_XS, ("s_2", "s_1", "s_0")):
        head.add(MathTex(s, font_size=size, color=GREEN).move_to(_p(x, 0)))
    head.add(MathTex(r"\overline{s_0}", font_size=size, color=GREEN).move_to(_p(A_X, 0)))
    ss = MathTex("s_1", "+", "s_2", font_size=size)
    ss[0].set_color(GREEN), ss[2].set_color(GREEN)
    head.add(ss.move_to(_p(S_X, 0)))
    head.add(Line(_p(VR_X, 0.32), _p(VR_X, HR_Y)).set_stroke(DIM, 2))
    hrule = Line(_p(-3.25, HR_Y), _p(4.25, HR_Y)).set_stroke(DIM, 2)
    g = VGroup(head, hrule)
    g.head, g.hrule, g.rows = head, hrule, []
    for i, (name, bits, a, s, ok) in enumerate(rows):
        y = ROW0_Y - ROW_PITCH * i
        nm = (T(name, 32, YELLOW) if name else T("unused", 30, DIM)).move_to(_p(NAME_X, y))
        dim = name is None
        bg = VGroup(*[_digit(b, 36, dim).move_to(_p(x, y)) for b, x in zip(bits, BIT_XS)])
        av = _digit(a).move_to(_p(A_X, y))
        sv = _digit(s).move_to(_p(S_X, y))
        mk = (check_mark() if ok else cross_mark()).scale(0.8).move_to(_p(MARK_X, y))
        vr = Line(_p(VR_X, y + ROW_PITCH / 2 + (0.07 if i == 0 else 0)), _p(VR_X, y - ROW_PITCH / 2)).set_stroke(DIM, 2)
        r = VGroup(nm, bg, av, sv, mk, vr)
        r.name, r.bits, r.a, r.s, r.mark, r.vr = nm, bg, av, sv, mk, vr
        g.add(r)
        g.rows.append(r)
    return g


def rule_line(size=44, words=True):
    strs = ([r"\text{so, }"] if words else []) + [r"\overline{s_0}", "=", "s_1", "+", "s_2"] + \
        ([r"\text{, hence,}"] if words else [])
    tex = MathTex(*strs, font_size=size)
    k = 1 if words else 0
    eq = VGroup(*[tex[k + j] for j in range(5)])
    for j in (0, 2, 4):
        eq[j].set_color(GREEN)
    if words:
        g = VGroup(tex[0], eq, tex[6])
        g.so, g.hence = tex[0], tex[6]
    else:
        g = VGroup(eq)
        g.so = g.hence = None
    g.eq = eq
    return g


def rule_words(size=30):
    return T("not Hunt = Sight or Sync", size, DIM, t2c={"Hunt": YELLOW, "Sight": YELLOW, "Sync": YELLOW})


def sum_line(size=48):
    tex = MathTex("s_2", "+", "s_1", "+", "s_0", "=", "1", font_size=size)
    for j in (0, 2, 4):
        tex[j].set_color(GREEN)
    tex[6].set_color(GOLD)
    tags = VGroup(*[T(n, S3.TAG_SIZE, YELLOW).next_to(tex[j], DOWN, buff=0.12)
                    for j, n in zip((0, 2, 4), ("Sync", "Sight", "Hunt"))])
    y = min(t.get_y() for t in tags)
    for t in tags:
        t.set_y(y)
    g = VGroup(tex, tags)
    g.tex, g.tags = tex, tags
    return g


FAC = ["(", "s_1", "+", "s_2", ")", "e", "r", "+", "s_2", r"\overline{e}"]
FINAL = [r"\overline{s_0}", "e", "r", "+", "s_2", r"\overline{e}"]


def final_d2(size=56):
    return eq_line("D_2", FINAL, size=size)


# ---------------------------------------------------------------- local
STACK_K = 0.72
D2_SIZE = 56
D2_Y = 0.75
D2_Y3 = 3.05
DIAG_K = 0.84
RULE_Y = -1.55


def moves(mobs, k=1.0, about=ORIGIN, shift=ORIGIN):
    out = []
    for m in mobs:
        m.generate_target()
        m.target.scale(k, about_point=about).shift(shift)
        out.append(MoveToTarget(m))
    return out


def term_box(glyphs, tex, tag, pad=0.22):
    """token_box() style, tall enough to hold the term and its name tag (centre the tag under the term)."""
    g = VGroup(*glyphs)
    left, right = g.get_left()[0] - pad / 2, g.get_right()[0] + pad / 2
    top = tex.get_top()[1] + 0.12
    bot = tag.get_bottom()[1] - 0.12
    r = Rectangle(width=max(right - left, 0.42), height=top - bot)
    r.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.25).set_z_index(-1)
    r.move_to([(left + right) / 2, (top + bot) / 2, 0])
    return r


def dim_thumb(g):
    for m in g.family_members_with_points():
        if m.get_stroke_width() > 0:
            m.set_stroke(DIM)
        if m.get_fill_opacity() > 0 and m.get_fill_color().to_hex().upper() != BG.upper():
            m.set_fill(DIM)
    return g


class OnehotRule(NarratedScene):
    def construct(self):
        shot = S3.handover_shot()
        self.lines, self.names = list(shot.lines), list(shot.names)
        for ln in self.lines:
            self.add(ln.tex, ln.tags)
        self.add(*self.names)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c6.rule.1
    def clip1(self):
        texs = [ln.tex for ln in self.lines]
        box = VGroup(*texs)
        L, Tp = box.get_left()[0], box.get_top()[1]
        sh = _p(-5.1 - STACK_K * L, 3.6 - STACK_K * Tp)
        name_moves = []
        for nm, ln in zip(self.names, self.lines):
            d_left = STACK_K * ln.pieces[0].get_left()[0] + sh[0]
            eq_y = STACK_K * ln.eqsign.get_y() + sh[1]
            name_moves.append(nm.animate.move_to(_p(d_left - 0.3 - nm.width / 2, eq_y)))
        with self.say("c6.rule.1") as c:
            self.play(*during(disappear(*[ln.tags for ln in self.lines]), 0, 0.35),
                      *during(moves(texs, STACK_K, ORIGIN, sh) + name_moves, 0.3, 1),
                      run_time=min(2.2, 0.6 * c.until("sum")))
            c.wait_until("sum")
            cap = T("Simplification is possible since:", 28).move_to(_p(3.6, 3.25))
            self.play(*appear(cap), run_time=1.0)  # early: p. 142's sentence, read before the voice states the fact
            c.wait_until("so ess two")
            sl = sum_line(48).move_to(_p(3.6, 2.2))
            self.play(*appear(sl.tex, sl.tags, lag=0.3), run_time=1.2)  # early: the name tags belong to p. 142's equation
            self.sum_parts = [cap, sl.tex, sl.tags]

            c.wait_until("check")
            tb = check_table(CHECK_ROWS[:3])
            tb.scale(0.95, about_point=ORIGIN).shift(_p(-3.05, -0.55))
            self.tb = tb
            rows = tb.rows
            items = [tb.head, tb.hrule] + [VGroup(r.name, r.bits, r.vr) for r in rows]
            self.play(*appear(*items, lag=0.2), run_time=1.6)  # early: the table is shown whole, then walked row by row
            c.wait_until("if ess zero is zero")
            self.play(*flash([rows[1].bits[2], rows[2].bits[2]], color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until("one of the other two")
            self.play(*appear(rows[1].a, rows[1].s, rows[2].a, rows[2].s, lag=0.25), run_time=1.6)

            c.wait_until("other")
            self.play(FlashAround(rows[0].bits[2], run_time=1.2, time_width=1.5),
                      *appear(rows[0].a, rows[0].s, lag=0.3), run_time=1.4)

            c.wait_until("result")
            self.play(*appear(*[r.mark for r in rows], shift=None, lag=0.2), run_time=1.0)
            c.wait_until("is the same as")
            rl = rule_line(44).move_to(_p(3.95, -1.3))
            self.rule = rl
            self.play(*appear(rl.so, rl.eq, rl.hence, lag=0.15), run_time=1.2)
            c.wait_until("in words")
            rw = rule_words(30).next_to(rl, DOWN, buff=0.35)
            self.rw = rw
            self.play(*appear(rw), run_time=1.0)

    # ------------------------------------------------------------------ c6.rule.2
    def clip2(self):
        d2 = self.lines[0]
        tb = self.tb
        leaving = [ln.tex for ln in self.lines[1:]] + self.names + self.sum_parts + \
            [tb.head, tb.hrule] + [p for r in tb.rows for p in (r.name, r.bits, r.vr, r.a, r.s, r.mark)] + \
            [self.rule.so, self.rule.hence]
        # D2 to the centre, size 56
        k = D2_SIZE / (S3.STACK_SIZE * STACK_K)
        probe = VGroup(d2.tex.copy(), d2.tags.copy())
        probe.scale(k, about_point=ORIGIN)
        sh = _p(-probe[0].get_center()[0], D2_Y - probe[0][1].get_y())
        tags = put_line(S3.raw_line("D_2", D2_SIZE), probe[0][0].get_left()[0] + sh[0], D2_Y).tags
        # the rule to below D2, centred
        rsh = _p(0, RULE_Y) - self.rule.eq.get_center()
        with self.say("c6.rule.2") as c:
            self.play(*during(disappear(*leaving), 0, 0.4),
                      *during(moves([d2.tex], k, ORIGIN, sh), 0.42, 0.85), *during(appear(tags, shift=None), 0.8, 1),
                      *during(moves([self.rule.eq], 1.0, ORIGIN, rsh) +
                              moves([self.rw], 1.0, ORIGIN, rsh), 0.42, 1),
                      run_time=min(1.6, c.until("pair")))
            left_x = d2.pieces[0].get_left()[0]
            c.wait_until("pair")
            pair = d2.terms[0] + d2.terms[2]
            self.play(*recolor(pair, YELLOW), run_time=1.0)

            c.wait_until("factor")
            fac = put_line(eq_line("D_2", FAC, D2_SIZE), left_x, D2_Y)
            for p in fac.terms[0]:
                p.set_color(YELLOW)
            self.play(*edit(d2.tex, fac.tex), *during(disappear(tags), 0, 0.3),
                      *during(appear(fac.tags, shift=None), 0.75, 1), run_time=min(1.8, c.until("swap")))

            c.wait_until("swap")
            fin = put_line(final_d2(D2_SIZE), left_x, D2_Y)
            ref = final_d2(D2_SIZE)
            for p in fin.terms[0]:
                p.set_color(YELLOW)
            self.play(*edit(fac.tex, fin.tex), *during(disappear(fac.tags), 0, 0.3),
                      *during(appear(fin.tags, shift=None), 0.75, 1),
                      FlashAround(self.rule.eq, run_time=1.6, time_width=1.5),
                      run_time=min(1.6, c.until("final")))

            c.wait_until("final")
            self.play(*[p.animate.set_color(q.get_color()) for p, q in zip(fin.terms[0], ref.terms[0])],
                      FlashAround(fin.tex, run_time=2.0, time_width=1.5), run_time=2.0)
            self.fin = fin

    # ------------------------------------------------------------------ c6.rule.3
    def clip3(self):
        fin = self.fin
        d = S2.onehot_diagram("native")
        d.scale(DIAG_K).move_to(_p(0, -0.85))
        self.diag = d
        sh = _p(0, D2_Y3 - fin.eqsign.get_y())
        with self.say("c6.rule.3") as c:
            self.play(*during(disappear(self.rule.eq, self.rw), 0, 0.35), *during(moves([fin.tex, fin.tags], 1.0, ORIGIN, sh), 0.3, 0.7),
                      *during(FadeIn(d), 0.5, 1), run_time=min(1.6, c.until("you'll be in sync")))  # early: the diagram is shown whole, then read
            c.wait_until("past the hunting stage")
            nh = T("not Hunt", S3.TAG_SIZE, YELLOW).next_to(fin.terms[0][0], DOWN, buff=0.12)
            if len(fin.tags):
                nh.set_y(fin.tags[0].get_y())
            nh.set_x(VGroup(*fin.terms[0]).get_x())
            box = term_box(fin.terms[0], fin.tex, nh)
            t1x = VGroup(*fin.terms[1]).get_x()
            sync = min(fin.tags, key=lambda t: abs(t.get_x() - t1x)) if len(fin.tags) else nh
            self.box, self.nh = box, nh
            self.play(S2.glow_state(d, "Sight"), S2.glow_state(d, "Sync"), FadeIn(box),
                      *appear(nh), run_time=1.2)
            c.wait_until("the sequence arrives")
            self.play(S2.light_arc(d, 6), S2.light_arc(d, 1), run_time=1.2)
            c.wait_until("stay")
            self.play(S2.light_arc(d, 6, False), S2.light_arc(d, 1, False), S2.glow_state(d, "Sight", False),
                      S2.light_arc(d, 0), Transform(box, term_box(fin.terms[1], fin.tex, sync)), sync.animate.set_x(t1x),
                      run_time=1.4)

    # ------------------------------------------------------------------ c6.rule.4
    def clip4(self):
        chips = S2.pattern_chips("final")
        tb = check_table(CHECK_ROWS)
        tb.shift(_p(-1.8, 1.45))
        rows = tb.rows
        with self.say("c6.rule.4") as c:
            rl = rule_line(44, words=False).move_to(_p(0, 3.1))
            rw = rule_words(30).next_to(rl, DOWN, buff=0.3)
            sweep_clear(self, *during(appear(rl.eq, rw, *chips, lag=0.06), 0.5, 1),
                        run_time=min(1.4, c.until("this trick holds")))
            c.wait_until("this trick holds")
            items = [tb.head, tb.hrule] + [VGroup(*[p for p in r]) for r in rows[:3]]
            self.play(*appear(*items, lag=0.15), run_time=1.5)

            c.wait_until("zero")
            r3 = rows[3]
            self.play(*fly(chips.chip["000"].txt, r3.bits), *during(appear(r3.name, r3.vr), 0.6, 1),
                      run_time=1.6)
            c.wait_until("not s zero is one")
            self.play(*appear(r3.a), FlashAround(r3.a, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("s one or s two is zero")
            self.play(*appear(r3.s), run_time=1.0)
            self.play(*appear(r3.mark, shift=None), run_time=0.8)

            c.wait_until("fine")
            # the caption names the three ticked rows only (beside them, not over the chips: 011 is unused)
            used = VGroup(*[rows[i].mark for i in range(3)])
            br = Brace(used, RIGHT, buff=0.2, color=GREEN)
            cap = T("used states only", 30, GREEN).next_to(br, RIGHT, buff=0.15)
            self.play(GrowFromCenter(br), *during(appear(cap, shift=None), 0.3, 1), run_time=1.2)
            self.play(*[FlashAround(chips.chip[p], color=GREEN, run_time=1.5, time_width=1.5)
                        for p in ("001", "010", "100")], run_time=1.5)

            c.wait_until("part3")
            ring = C34.checked_ring("binary", center=ORIGIN, arrows=True)
            for m in list(ring.get_family()):
                for sub in list(m.submobjects):
                    if isinstance(sub, (Text, MarkupText, MathTex, SingleStringMathTex)):
                        m.remove(sub)
            ring = dim_thumb(ring).scale(0.42).move_to(_p(5.0, 2.6))
            tag = T("Part 3", 30, DIM).next_to(ring, DOWN, buff=0.15)
            self.play(*appear(ring, tag, lag=0.3), run_time=1.2)
