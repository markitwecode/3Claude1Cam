"""Chapter 1, scene 3: x³ from first principles. Clips c1.cube.1 – c1.cube.5.

Opens from an empty frame; s2's corner tag "y = x^3, at x = 1" (MathTex 34, FG) fades in top-right.
Recipe labels across the top, the derivation column on the left-centre, side calculations under the
corner tag, the limit line, the power rule, the notes' condition, then the boxed 3x² shrinks into the
x³ derivative-chain card, top-left, and the scene ends on that card alone (handover to s4).

Exports
- cube_card() -> VGroup(frame, expr), exactly as it sits in the last frame:
  expr = MathTex("x^3", r"\\to", "3x^2", font_size=44), expr[2] GREEN, the rest FG;
  frame = RoundedRectangle (corner 0.15, YELLOW stroke 2.5, no fill) round expr, 0.3 padding;
  the whole card moved to_corner(UL, buff=0.5). Attributes .frame, .expr. The rest of the top row is
  empty: ch4 s2 extends the chain to x^3 -> 3x^2 -> 6x -> 6 -> 0 (rebuild expr with more parts and
  stretch the frame to the right, keeping its left edge), ch6 s4 sets x^4's card beside it.
- handover_shot() -> cube_card() (s4 opens on it).
- derivation() -> VGroup(labels, column) for the recap: the five DIM-free step labels
  "substitute · expand · subtract · divide · limit" over the column y(x+dx) = (x+dx)^3, the expansion,
  the subtraction, the division, and the limit line ending in the boxed GREEN 3x^2. dx TEAL.
  Centred at ORIGIN, scaled to fit 13 x 7.2; the caller rescales.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

D = r"\delta x"
SIZE = 46
EQX = -1.4                     # x of the column's "=" signs
ROWS = (1.8, 0.8, -0.2, -1.85)
LABEL_Y = 2.95
STEP_WORDS = ("substitute", "expand", "subtract", "divide", "limit")


def _tex(parts, size=SIZE, color=FG):
    m = MathTex(*parts, font_size=size, color=color)
    for i, p in enumerate(parts):
        if p == D:
            m[i].set_color(TEAL)
    return m


def mline(segs, size=SIZE, eq=None, y=0.0):
    """One typeset line built as standalone MathTex segments laid exactly where the whole line's
    glyphs sit (so each segment can fly, fade or move on its own). eq=(seg, part): put that part's
    centre at x = EQX."""
    parts = [p for s in segs for p in s]
    tmpl = _tex(parts, size)
    out = VGroup()
    k = 0
    for s in segs:
        m = _tex(s, size)
        m.move_to(VGroup(*tmpl[k:k + len(s)]))
        for j in range(len(s)):            # part by part: keeps the whole line's spacing exactly
            if len(m[j].get_all_points()) and len(tmpl[k + j].get_all_points()):
                m[j].move_to(tmpl[k + j])
        k += len(s)
        out.add(m)
    out.shift(UP * (y - tmpl.get_y()))
    if eq is not None:
        out.shift(RIGHT * (EQX - out[eq[0]][eq[1]].get_x()))
    return out


def make_tag():
    return MathTex(r"y = x^3,\ \text{at } x = 1", font_size=34, color=FG).to_corner(UR, buff=0.5)


def make_labels():
    words = [T(w, 30) for w in STEP_WORDS]
    seps = [T("·", 30, DIM) for _ in range(4)]
    row = VGroup(words[0])
    for s, w in zip(seps, words[1:]):
        row.add(s, w)
    row.arrange(RIGHT, buff=0.3).move_to([-1.5, LABEL_Y, 0])
    return row, words, seps


def make_l1():
    return mline([["y(x+", D, ")", "=", "(x+", D, ")^3"]], eq=(0, 3), y=ROWS[0])


def make_l2():
    return mline([["=", "x^3"], ["+", r"3x^2\,", D], ["+", r"3x\,(", D, ")^2"], ["+", "(", D, ")^3"]],
                 eq=(0, 0), y=ROWS[1])


def make_l3():
    return mline([["y(x+", D, ") - y(x)", "="],
                  [r"3x^2\,", D, "+", r"3x\,(", D, ")^2", "+", "(", D, ")^3"]], eq=(0, 3), y=ROWS[2])


def make_l4():
    """VGroup(lhs fraction without its denominator, den, rhs). rhs parts: 0 '=', 1 3x^2, 2 +,
    3 3x, 4 dx, 5 +, 6 (, 7 dx, 8 )^2."""
    full = [r"\frac{y(x+", D, r") - y(x)}{", D, "}"]
    rhs_p = ["=", "3x^2", "+", r"3x\,", D, "+", "(", D, ")^2"]
    tmpl = _tex(full + rhs_p)
    lhs = _tex([r"\frac{y(x+", D, r") - y(x)}{\phantom{\delta x}}"])
    lhs.align_to(tmpl, UP).align_to(tmpl, LEFT)
    den = _tex([D]).move_to(tmpl[3])
    rhs = _tex(rhs_p).move_to(VGroup(*tmpl[5:]))
    for j in range(len(rhs_p)):
        rhs[j].move_to(tmpl[5 + j])
    out = VGroup(lhs, den, rhs)
    out.shift(UP * (ROWS[3] - tmpl.get_y()) + RIGHT * (EQX - rhs[0].get_x()))
    return out


def make_l5():
    """VGroup(lhs, res) for dy/dx = lim ... = 3x^2, res GREEN."""
    line = mline([[r"\frac{dy}{dx} \equiv \lim_{", D, r" \to 0} \frac{y(x+", D, r") - y(x)}{", D, "} ="],
                  [r"\;3x^2"]])
    line[1].set_color(GREEN)
    return line


def result_box(res):
    return SurroundingRectangle(res, color=YELLOW, buff=0.12, stroke_width=3)


def cube_card():
    expr = MathTex("x^3", r"\to", "3x^2", font_size=44, color=FG)
    expr[2].set_color(GREEN)
    frame = RoundedRectangle(corner_radius=0.15, width=expr.width + 0.6, height=expr.height + 0.6)
    frame.set_stroke(YELLOW, 2.5).set_fill(opacity=0).move_to(expr)
    card = VGroup(frame, expr)
    card.to_corner(UL, buff=0.5)
    card.frame, card.expr = frame, expr
    return card


def handover_shot():
    return cube_card()


def derivation():
    labels, _, _ = make_labels()
    l1, l2, l3, l4 = make_l1(), make_l2(), make_l3(), make_l4()
    l5 = make_l5()
    box = result_box(l5[1])
    res_row = VGroup(l5, box)
    res_row.next_to(l4, DOWN, buff=0.45)
    res_row.shift(RIGHT * (l4.get_center()[0] - res_row.get_center()[0]))
    column = VGroup(l1, l2, l3, l4, res_row)
    labels.next_to(column, UP, buff=0.5)
    whole = VGroup(labels, column)
    s = min(13 / whole.width, 7.2 / whole.height, 1.0)
    whole.scale(s).move_to(ORIGIN)
    return whole


def converge(src, dst, angle, a0, a1):
    """A copy of src travels along an arc to dst's place and fades out as it arrives (it's absorbed
    into dst, which fades in separately); active only in [a0, a1] of the play."""
    c = src.copy()
    path = ArcBetweenPoints(c.get_center(), dst.get_center(), angle=angle)

    def upd(m, a):
        t = min(max((a - a0) / (a1 - a0), 0), 1)
        m.move_to(path.point_from_proportion(smooth(t)))
        m.set_opacity(min(max((t - 0.22) / 0.13, 0.0), 1.0) if t < 0.7 else max(0.0, (1 - t) / 0.3))

    return UpdateFromAlphaFunc(c, upd, remover=True)


class Cube(NarratedScene):
    def construct(self):
        tag = make_tag()
        labels, words, seps = make_labels()
        self.words = words

        # ---------------- c1: why, recipe, substitute
        with self.say("c1.cube.1") as c:
            q = MathTex(r"\text{chord slopes} \;\to\; 3", r"\;?", font_size=60)
            q[1].set_color(YELLOW)
            self.play(*appear(tag, q, lag=0.4), run_time=min(1.4, c.until("work it out")))
            for i, w in enumerate(words):
                c.wait_until(own_word=w)
                items = [w] if i == 0 else [seps[i - 1], w]
                gone = disappear(q) if i == 0 else []
                self.play(*gone, *appear(*items, lag=0.15), run_time=min(0.8, c.until("sub")))
            c.wait_until("sub")
            l1 = make_l1()
            self.play(*self.light(0), *appear(l1, shift=None), run_time=min(1.4, c.until()))

        # ---------------- c2: expand, subtract, what's left
        with self.say("c1.cube.2") as c:
            l2 = make_l2()
            self.play(*self.light(1), run_time=0.8)
            c.wait_until("ex cubed")
            self.play(*appear(l2[0], shift=None), run_time=1.0)
            for seg, cue in ((l2[1], "three ex squared"), (l2[2], "three ex times"),
                             (l2[3], "plus delta ex cubed")):
                c.wait_until(cue)
                self.play(*appear(seg, shift=None), run_time=min(1.0, c.until("subtract")))
            c.wait_until("subtract")
            l3 = make_l3()
            self.play(*self.light(2), *appear(l3[0], shift=None), run_time=min(1.4, c.until("it cancels")))
            c.wait_until("it cancels")
            x3 = l2[0][1]
            strike = Line(x3.get_corner(DL) + 0.06 * LEFT, x3.get_corner(UR) + 0.06 * RIGHT,
                          color=RED, stroke_width=5)
            self.play(*recolor(x3, RED), Create(strike), run_time=1.0)
            src = VGroup(*l2[1][1:], *l2[2], *l2[3])
            self.play(*fly(src, l3[1]), run_time=min(1.6, c.until("left")))
            c.wait_until("left")
            dxs = [l3[1][1], l3[1][4], l3[1][8]]
            self.play(*[FlashAround(d, color=TEAL, time_width=1.5) for d in dxs], run_time=1.6)

        # ---------------- c3: divide, the δx=0.5 check
        with self.say("c1.cube.3") as c:
            l4 = make_l4()
            lhs, den, rhs = l4
            self.play(*self.light(3), *appear(lhs, shift=None), run_time=min(1.4, c.until("each term")))
            c.wait_until("each term")
            rt = min(2.2, c.until("you get"))
            ghosts = [den.copy() for _ in dxs[1:]]
            flies = []
            for k, (d, g) in enumerate(zip(dxs, [den, *ghosts])):
                flies += during(fly(d, g, arc=1.2), 0.2 * k, 0.6 + 0.2 * k)
            self.play(*flies, run_time=rt)
            self.remove(*ghosts)
            c.wait_until("you get")
            self.play(*appear(rhs, shift=None), run_time=min(1.4, c.until("check")))
            c.wait_until("check")
            s1 = MathTex(r"3 + 3\,", D, r" + (", D, r")^2", font_size=36)
            s1[1].set_color(TEAL)
            s1[3].set_color(TEAL)
            s1.next_to(tag, DOWN, buff=0.4).align_to(tag, RIGHT)
            self.play(*appear(s1), run_time=1.0)
            c.wait_until("four point seven five")
            s2 = MathTex(D, r" = 0.5:\;\; ", "4.75", font_size=36)
            s2[0].set_color(TEAL)
            s2[2].set_color(TEAL)
            s2.next_to(s1, DOWN, buff=0.3).align_to(tag, RIGHT)
            self.play(*appear(s2), run_time=1.0)
            c.wait_until("first chord slope")
            self.play(FlashAround(s2[2], color=TEAL, time_width=1.5), run_time=1.5)

        # ---------------- c4: limit, result, power rule, slope 3
        with self.say("c1.cube.4") as c:
            lift = UP * (1.45 - l4.get_y())
            sweep_clear(self, *[m.animate.shift(lift) for m in l4],
                        *self.light(4),
                        keep=[tag, *words, *seps, s1, s2, *l4], run_time=min(1.8, c.until("last two")))
            c.wait_until("last two")
            t1 = [rhs[3], rhs[4]]
            t2 = [rhs[6], rhs[7], rhs[8]]
            self.play(*[FlashAround(VGroup(*t).copy(), time_width=1.5) for t in (t1, t2)], run_time=1.5)
            c.wait_until("go to zero", nth=1)
            anims = []
            for t in (t1, t2):
                ctr = VGroup(*t).get_center()
                for p in t:
                    anims.append(p.animate.scale(0.75, about_point=ctr).set_opacity(0.4))
            anims += [rhs[2].animate.set_opacity(0.4), rhs[5].animate.set_opacity(0.4)]
            self.play(*anims, run_time=min(1.6, c.until("result")))
            c.wait_until("result")
            l5 = make_l5().move_to([-1.0, -0.1, 0])
            res = l5[1]
            box = result_box(res)
            self.play(*during(fly(rhs[1], res), 0.0, 0.55), *during(appear(l5[0], shift=None), 0.5, 1.0),
                      run_time=min(2.0, c.until("rule")))
            self.play(GrowFromCenter(box), run_time=0.8)
            c.wait_until("rule")
            rule = MathTex("y = x^{", "a", r"} \;\Rightarrow\; \frac{dy}{dx} = ", "a", r"\,x^{", "a-1", "}",
                           font_size=42).move_to([-1.0, -1.8, 0])
            self.play(*appear(rule, shift=None), run_time=1.2)
            c.wait_until("comes down")
            self.play(FlashAround(rule[3], time_width=1.5), *recolor(rule[3], YELLOW), run_time=1.2)
            c.wait_until("one less")
            self.play(FlashAround(rule[5], time_width=1.5), *recolor(rule[5], YELLOW), run_time=1.2)
            a3 = MathTex("a = 3", font_size=36).next_to(rule, DOWN, buff=0.35)
            self.play(*appear(a3), run_time=min(1.0, c.until("three")))
            c.wait_until("three")
            three = MathTex(r"x = 1:\;\; 3x^2 = 3", font_size=36, color=GREEN)
            three.next_to(tag, DOWN, buff=0.4).align_to(tag, RIGHT)
            self.play(*swap(VGroup(s1, s2), three), run_time=min(1.2, c.until()))

        # ---------------- c5: the notes' condition, not needed, the card
        with self.say("c1.cube.5") as c:
            notes = MathTex(r"\text{Provided } |\delta x| < 1 \text{ then } "
                            r"1 > |\delta x| > |\delta x|^2 > |\delta x|^3 > \cdots",
                            font_size=34, color=DIM).move_to([-0.7, -3.35, 0])
            self.play(*appear(notes, shift=None), run_time=1.2)
            c.wait_until("needed")
            nn = T("not needed", 30, YELLOW).next_to(l4, RIGHT, buff=0.9)
            self.play(*appear(nn), run_time=1.0)
            c.wait_until("every leftover term")
            d1, d2 = rhs[4], rhs[7]
            circs = [Circle(radius=max(d.width, d.height) / 2 + 0.05, color=YELLOW, stroke_width=3).move_to(d)
                     for d in (d1, d2)]
            ar2 = Arrow(nn.get_left(), circs[1].get_right(), buff=0.12, color=YELLOW, stroke_width=3)
            ar1 = CurvedArrow(nn.get_corner(UL) + 0.1 * RIGHT, circs[0].get_top() + 0.08 * UP,
                              angle=0.9, color=YELLOW, stroke_width=3)
            self.play(*[GrowFromCenter(ci) for ci in circs], d1.animate.set_opacity(1),
                      d2.animate.set_opacity(1), GrowArrow(ar2), Create(ar1),
                      run_time=min(1.6, c.until("card")))
            c.wait_until("card")
            sweep_clear(self, keep=[res, box], run_time=1.2)
            card = cube_card()
            k = card.expr[2].height / res.height
            self.play(res.animate.scale(k).move_to(card.expr[2]),
                      Transform(box, card.frame.copy()), run_time=1.6)
            x3c, arc = card.expr[0].copy(), card.expr[1].copy()
            self.play(*appear(x3c, arc, lag=0.3), run_time=1.0)
            self.remove(res, box, x3c, arc)
            self.add(handover_shot())
            self.wait(1.0)

    def light(self, i):
        """Step label i lights YELLOW; the one before goes DIM (done)."""
        out = recolor(self.words[i], YELLOW)
        if i > 0:
            out += recolor(self.words[i - 1], DIM)
        return out
