"""Chapter 2, scene 3: the chain rule from the definition. Clips c2.chain.1 – c2.chain.4.

Exports: chain_box() (105) boxed like ch1's definition_box() plus `.tag`; bracket_line() the
two-bracket line with the TEAL δu; small_diff_box() ch1's differentiability box as shown on {cont}
(DIFF_K, bottom-right, `.a` YELLOW, rest dimmed) for s5; handover_shot() (105) top-right for s4.
"""
# style: 2
# handover: next
import re
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

# ── maths builder: f BLUE, u PURPLE, δx/δu/δf TEAL, per-segment overrides and keys ──────────
_TOK = re.compile(r"(\\delta [xuf]|f|u)")
_CMAP = {"f": BLUE, "u": PURPLE, r"\delta x": TEAL, r"\delta u": TEAL, r"\delta f": TEAL}


def mt(segs, size=44):
    """MathTex from segments: str, or (tex, colour or None, key or None). Every f / u / δ? is its own
    piece, coloured by _CMAP unless the segment's colour overrides. `m.keys[key]` → piece indices.
    (No TeX command may contain f or u: write fractions as {a \\over b}, brackets \\Bigg.)"""
    pieces, cols, keys = [], [], {}
    for s in segs:
        tex, col, key = (s, None, None) if isinstance(s, str) else (tuple(s) + (None, None))[:3]
        assert not re.search(r"\\(?!delta)[a-zA-Z]*[fu]", tex), tex
        for t in _TOK.split(tex):
            if not t.strip():
                continue
            if key:
                keys.setdefault(key, []).append(len(pieces))
            pieces.append(t)
            cols.append(col or _CMAP.get(t))
    m = MathTex(*pieces, font_size=size)
    for i, c in enumerate(cols):
        if c:
            m[i].set_color(c)
    m.keys = keys
    return m


def grp(m, *keys):
    return VGroup(*[m[i] for k in keys for i in m.keys[k]])


CHANGE_U = r"u(x+\delta x) - u(x)"
CHANGE_F = r"f(u(x+\delta x)) - f(u(x))"


def quotient(size=52):
    return mt(["{", (CHANGE_F, None, "num"), r"\over", (r"\delta x", None, "den"), "}"], size)


def line_one(size=44):
    return mt(["=", (r"\Bigg[", None, "b1"), ("{", None, "b1"), (CHANGE_F, None, "b1"), (r"\over", None, "b1"),
               (CHANGE_U, TEAL, "c1"), ("}", None, "b1"), (r"\Bigg]", None, "b1"),
               (r"\Bigg[", None, "b2"), ("{", None, "b2"), (CHANGE_U, TEAL, "c2"), (r"\over", None, "b2"),
               (r"\delta x", None, "b2"), ("}", None, "b2"), (r"\Bigg]", None, "b2")], size)


def bracket_line(size=44):
    """The regrouped line, TEAL δu: `.eq .br1 .br2 .du` (δu, bracket 1's denominator) `.c2`."""
    m = mt(["=", (r"\Bigg[", None, "b1"), ("{", None, "b1"), (r"f(u + \delta u) - f(u)", None, "b1"),
            (r"\over", None, "b1"), (r"\delta u", None, "du"), ("}", None, "b1"), (r"\Bigg]", None, "b1"),
            (r"\Bigg[", None, "b2"), ("{", None, "b2"), (CHANGE_U, TEAL, "c2"), (r"\over", None, "b2"),
            (r"\delta x", None, "b2"), ("}", None, "b2"), (r"\Bigg]", None, "b2")], size)
    m.eq = m[0]
    m.br1, m.br2 = grp(m, "b1", "du"), grp(m, "b2", "c2")
    m.du, m.c2 = grp(m, "du"), grp(m, "c2")
    return m


def frac_d(top, bot, size=58, color=GREEN):
    """{d top \\over d bot}, one colour; keys 'top', 'bot' (the d with its letter)."""
    return mt([("{d", color, "top"), (top, color, "top"), (r"\over", color), ("d", color, "bot"),
               (bot, color, "bot"), ("}", color)], size)


def chain_formula(size=58):
    g = GREEN
    m = mt([(r"{d \over dx}", None, "lhs"), ("f", None, "lhs"), (r"\big(", None, "lhs"), ("u", None, "lhs"),
            ("(x)", None, "lhs"), (r"\big)", None, "lhs"), ("=", None, "lhs"),
            ("{d", g, "dfdu"), ("f", g, "dfdu"), (r"\over", g, "dfdu"), ("d", g, "du1"), ("u", g, "du1"),
            ("}", g, "dfdu"), (r"\,", None, "dfdu"),
            ("{d", g, "du2"), ("u", g, "du2"), (r"\over", g, "dudx"), ("dx", g, "dudx"), ("}", g, "dudx")], size)
    return m


def chain_box(size=58, right_pad=0.95):
    """(105) boxed as ch1's definition_box(): `.rect` YELLOW, `.formula`, `.num` "(105)" DIM 28,
    `.tag` "chain rule" under it; rect centred at ORIGIN. Formula parts: `.lhs .dfdu .dudx` (the two
    GREEN fractions), `.du1` (du under df), `.du2` (du over dx)."""
    f = chain_formula(size)
    f.lhs, f.du1, f.du2 = grp(f, "lhs"), grp(f, "du1"), grp(f, "du2")
    f.dfdu, f.dudx = grp(f, "dfdu", "du1"), grp(f, "du2", "dudx")
    pad = 0.35
    rect = Rectangle(width=f.width + pad + right_pad, height=f.height + 2 * pad, color=YELLOW, stroke_width=3)
    rect.move_to(f.get_center() + (right_pad - pad) / 2 * RIGHT)
    num = T("(105)", 28, DIM).next_to(rect.get_corner(UR), UP, buff=0.1).align_to(rect, RIGHT)
    tag = T("chain rule", 32, YELLOW).next_to(rect, DOWN, buff=0.22)
    g = VGroup(rect, f, num, tag)
    g.rect, g.formula, g.num, g.tag = rect, f, num, tag
    g.shift(-rect.get_center())
    return g


BOX_POS = np.array([0.0, 0.55, 0])
HAND_K = 0.5


def handover_shot():
    """s3's last frame / s4's first: (105) alone, scale HAND_K, top-right corner (buff 0.5)."""
    b = chain_box().scale(HAND_K)
    b.to_corner(UR, buff=0.5)
    return VGroup(b)


DIFF_K = 0.45


def small_diff_box(lit=True):
    """ch1's diff_box() at DIFF_K, bottom-right (buff 0.4); lit: `.a` YELLOW, the rest at DIMMED."""
    b = load_scene("ch1_s6_differentiable").diff_box().scale(DIFF_K).to_corner(DR, buff=0.4)
    if lit:
        b.a.set_color(YELLOW)
        for m in (b.head, b.b, b.then, b.eq):
            m.set_opacity(DIMMED)
    return b


def schematic():
    """x → [u] → u(x) → [f] → f(u(x)); `.x .ub .ux .fb .fux .arrows`; captions built apart."""
    x = MathTex("x", font_size=48)

    def fbox(letter, col):
        sq = Square(1.0).set_stroke(col, 3)
        return VGroup(sq, MathTex(letter, font_size=52, color=col).move_to(sq))
    ub, fb = fbox("u", PURPLE), fbox("f", BLUE)
    ux = MathTex("u", "(x)", font_size=48)
    ux[0].set_color(PURPLE)
    fux = MathTex("f", "(", "u", "(x))", font_size=48)
    fux[0].set_color(BLUE)
    fux[2].set_color(PURPLE)
    items = VGroup(x, ub, ux, fb, fux).arrange(RIGHT, buff=1.0)
    arrows = [Arrow(a.get_right(), b.get_left(), buff=0.14, stroke_width=3, color=DIM,
                    max_tip_length_to_length_ratio=0.3) for a, b in zip(items[:-1], items[1:])]
    g = VGroup(*items, *arrows)
    g.x, g.ub, g.ux, g.fb, g.fux, g.arrows = x, ub, ux, fb, fux, arrows
    return g


SCH_K = 0.65
Q_UP = np.array([0, 1.45, 0])
L_Y = -0.45


class ChainRule(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        box = self.box
        hs = handover_shot()[0]
        sweep_clear(self, box.animate.scale(HAND_K).move_to(hs.rect.get_center()), keep=[box], run_time=1.6)
        self.remove(*box.get_family())
        self.add(handover_shot())            # the exact shot s4 opens on
        self.wait(1.0)

    # ---------------- c2.chain.1: a function of a function; sin(x²); the definition
    def clip1(self):
        sch = schematic().move_to(0.5 * UP)
        self.sch = sch
        inner = T("inner", 36, PURPLE).next_to(sch.ub, DOWN, buff=0.2)
        outer = T("outer", 36, BLUE).next_to(sch.fb, DOWN, buff=0.2)
        ex = MathTex(r"\sin", "(", "x^2", ")", font_size=60).move_to(1.6 * DOWN)
        ex[0].set_color(BLUE)
        ex[2].set_color(PURPLE)
        self.ex = ex
        with self.say("c2.chain.1") as c:
            self.play(*appear(sch.x, sch.arrows[0], sch.ub, sch.arrows[1], sch.ux, shift=None, lag=0.3),
                      run_time=min(2.0, 0.8 * c.until("function of a function")))
            c.wait_until("function of a function")
            self.play(*appear(sch.arrows[2], sch.fb, sch.arrows[3], sch.fux, shift=None, lag=0.3), run_time=1.8)
            c.wait_until(own_word=outer)
            self.play(*appear(outer), run_time=1.0)
            c.wait_until(own_word=inner)
            self.play(*appear(inner), run_time=1.0)
            c.wait_until("example")
            self.play(*appear(ex), run_time=1.2)
            c.wait_until("sine is the outer function")
            self.play(FlashAround(ex[0], color=BLUE), FlashAround(sch.fb, color=BLUE), run_time=1.5)
            c.wait_until("ex squared the inner")
            self.play(FlashAround(ex[2], color=PURPLE), FlashAround(sch.ub, color=PURPLE), run_time=1.5)

            c.wait_until("def")
            sch.generate_target()
            sch.target.scale(SCH_K).to_corner(UL, buff=0.45)
            ex.generate_target()
            ex.target.scale(SCH_K).next_to(sch.target, RIGHT, buff=0.7)
            q = quotient().move_to(0.2 * DOWN)
            self.q = q
            self.play(*during(disappear(inner, outer), 0, 0.3),
                      *during([MoveToTarget(sch), MoveToTarget(ex)], 0.1, 0.65),
                      *during(appear(q, shift=None), 0.6, 1), run_time=min(2.4, c.until("That's the change")))
            c.wait_until("the change in F")
            self.play(FlashUnder(grp(q, "num"), color=BLUE), run_time=1.5)
            c.wait_until("divided by delta ex")
            self.play(FlashAround(grp(q, "den"), color=TEAL), run_time=min(1.5, c.until()))

    # ---------------- c2.chain.2: multiply and divide; ×1; regroup with δu
    def clip2(self):
        q = self.q
        l1 = line_one().move_to(L_Y * UP)
        c1, c2 = grp(l1, "c1"), grp(l1, "c2")
        b1, b2 = grp(l1, "b1", "c1"), grp(l1, "b2", "c2")
        times1 = MathTex(r"\times 1", font_size=40, color=YELLOW)
        times1.move_to([(b1.get_right()[0] + b2.get_left()[0]) / 2, l1.get_bottom()[1] - 0.4, 0])
        dl = mt([(r"\delta u", None, "lhs"), ("=", TEAL, "lhs"), (CHANGE_U, TEAL, "rhs")], 42)
        dlhs, drhs = grp(dl, "lhs"), grp(dl, "rhs")
        dl.shift([c1.get_center()[0] - drhs.get_center()[0], -2.15 - dl.get_center()[1], 0])
        cap = T("change in the inner function", 32, TEAL).next_to(dl, RIGHT, buff=0.6)
        l2 = bracket_line().move_to(L_Y * UP)
        l2.shift((l1[0].get_center() - l2[0].get_center()) * RIGHT)
        self.l2, self.dlhs, self.drhs, self.cap = l2, dlhs, drhs, cap
        with self.say("c2.chain.2") as c:
            self.play(q.animate.move_to(Q_UP), run_time=1.3)
            c.wait_until("mult")
            derive(self, q, l1, run_time=2.0)
            c.wait_until("the change in the inner function")
            self.play(*flash([c1, c2], color=TEAL), run_time=1.6)
            c.wait_until("one")
            self.play(*appear(times1), run_time=1.0)
            c.wait_until("regroup")
            rt = c.until("first")
            self.play(*during(disappear(times1), 0, 0.3), *fly(c1, drhs),
                      *during(appear(dlhs, shift=None), 0.55, 1), run_time=min(1.6, 0.45 * rt))
            self.play(*edit(l1, l2), *during(appear(cap), 0.5, 1), run_time=1.5)  # early: names δu as it is born; the voice says "change in the inner function" on {first}
            self.remove(l2)
            self.add(l2.eq, l2.br1, l2.br2)
            c.wait_until("first")
            self.play(*set_alpha([l2.br2], DIMMED), FlashAround(l2.br1, color=YELLOW), run_time=1.5)
            c.wait_until("second")
            self.play(*set_alpha([l2.br1], DIMMED), *set_alpha([l2.br2], 1), FlashAround(l2.br2, color=YELLOW),
                      run_time=1.5)

    # ---------------- c2.chain.3: the limit; continuity; df/du, du/dx; (105)
    def clip3(self):
        l2 = self.l2
        limx = mt([(r"\delta x \to 0", TEAL)], 42)
        limx.next_to(self.dlhs, DOWN, buff=0.55).align_to(self.dlhs, LEFT)
        limu = mt([(r"\delta u \to 0", TEAL)], 42).next_to(limx, RIGHT, buff=0.9)
        dbox = small_diff_box(lit=False)
        dfdu = frac_d("f", "u").move_to(l2.br1)
        dudx = frac_d("u", "x").move_to(l2.br2)
        box = chain_box().move_to(BOX_POS)
        self.box = box
        f = box.formula
        with self.say("c2.chain.3") as c:
            self.play(*set_alpha([l2.br1], 1), *during(disappear(self.cap), 0, 0.4),
                      *during(appear(limx), 0.45, 1), run_time=1.5)
            c.wait_until("part one's box")
            self.play(*appear(dbox, shift=None), run_time=1.0)  # early: the box is shown whole, then line (a) is read
            c.wait_until("continuous")
            self.play(dbox.a.animate.set_color(YELLOW), *set_alpha([dbox.head, dbox.b, dbox.then, dbox.eq], DIMMED),
                      run_time=1.2)
            c.wait_until("goes to zero too")
            self.play(*appear(limu), run_time=1.0)
            c.wait_until("df")
            self.play(*swap(l2.br1, dfdu), run_time=1.5)
            c.wait_until("du")
            self.play(*swap(l2.br2, dudx), run_time=1.5)

            c.wait_until("rule")
            sweep_clear(self, keep=[self.sch, self.ex, dfdu, dudx], run_time=1.2)
            lhs = [f[i] for i in f.keys["lhs"]]
            self.play(*during([dfdu.animate.move_to(f.dfdu), dudx.animate.move_to(f.dudx)], 0, 0.6),
                      *during(appear(*lhs, shift=None, lag=0), 0.5, 1),
                      *during(appear(box.rect, box.num, box.tag, shift=None, lag=0.2), 0.6, 1), run_time=1.8)
            self.remove(dfdu, dudx, *lhs, box.rect, box.num, box.tag)
            self.add(box)
            c.wait_until("Differentiate the outer function")
            self.play(FlashAround(f.dfdu, color=GREEN), run_time=1.5)
            c.wait_until("derivative of the inner one")
            self.play(FlashAround(f.dudx, color=GREEN), run_time=1.5)

    # ---------------- c2.chain.4: function of a function; fractions cancelling; δu ≠ 0
    def clip4(self):
        box, f = self.box, self.box.formula
        sub = T("differentiation of a function of a function", 32, FG, slant=ITALIC)
        sub.next_to(box.tag, DOWN, buff=0.3)
        fin = mt([("{", None, "a"), (r"\delta f", TEAL), (r"\over", TEAL), (r"\delta u", TEAL, "den"), ("}", None),
                  (r"\cdot", TEAL), ("{", None), (r"\delta u", TEAL, "nu"), (r"\over", TEAL), (r"\delta x", TEAL),
                  ("}", None)], 46)
        fin.next_to(sub, DOWN, buff=0.45)
        foot = mt([(r"\delta u \neq 0\,?", RED)], 38).next_to(fin, RIGHT, buff=0.9)
        tick = check_mark().next_to(box.rect, RIGHT, buff=0.35)
        cancel = Line(f.du1.get_corner(DL) + 0.08 * DL, f.du2.get_corner(UR) + 0.08 * UR).set_stroke(FG, 3, opacity=0.55)
        with self.say("c2.chain.4") as c:
            c.wait_until(own_word=sub)
            self.play(*appear(sub), run_time=1.2)
            c.wait_until("two fractions cancelling")
            self.play(*flash([f.du1, f.du2], color=YELLOW), run_time=1.3)
            self.play(Create(cancel), run_time=0.8)
            self.play(FadeOut(cancel), run_time=0.8)
            c.wait_until("they really were fractions")
            self.play(*appear(fin), run_time=1.3)
            c.wait_until("catch")
            self.play(*appear(foot), run_time=1.0)
            c.wait_until("divided by the change")
            self.play(FlashAround(grp(fin, "den"), color=RED), run_time=1.5)
            c.wait_until("patch")
            self.play(GrowFromCenter(tick), *set_alpha([foot], 0.35), run_time=1.2)
