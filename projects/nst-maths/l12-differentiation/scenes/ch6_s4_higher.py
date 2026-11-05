"""Chapter 6, scene 4: when the second derivative is zero (Figure 30, higher derivatives). Clips c6.higher.1 – c6.higher.4.

Exports (static, no updaters):
- figure30(): VGroup(.cube, .quart), the two panels as clip 1 shows them; each panel has
  .axes .xlab .ylab .curve .tan .dot .lab (y = x^3 / y = x^4, BLUE).
- chain_cards(): VGroup(.cube, .quart), the two derivative-chain cards with their values at 0 and
  the YELLOW rings, as clip 2 shows them under the panels; each card has .frame .expr .vals .ring.
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
from lib.style import *  # noqa: E402,F403

AXIS_CFG = {"color": DIM, "stroke_width": 2, "tip_width": 0.2, "tip_height": 0.2, "include_ticks": False}

# panel layouts: (scale, x of the two centres, y)
LAY_A = (1.0, 3.5, 1.15)     # clip 1: Figure 30 full size
LAY_B = (0.7, 3.55, 1.95)    # clip 2: room for the cards
LAY_C = (0.52, 4.1, 2.45)    # clip 3: room for the rule

KINDS = {
    "cube": (lambda x: x ** 3, (-8.8, 8.8), "y = x^3", (-1.15, 5.0)),
    "quart": (lambda x: x ** 4, (-1.0, 17.0), "y = x^4", (1.0, 11.0)),
    "nquart": (lambda x: -x ** 4, (-17.0, 1.0), "y = -x^4", (-3.1, -11.0)),
}


def build_panel(kind, lay=LAY_A):
    s, cx, cy = lay
    f, yr, tex, anchor = KINDS[kind]
    c = np.array([-cx if kind == "cube" else cx, cy, 0])
    ax = Axes(x_range=[-2.3, 2.3, 1], y_range=[yr[0], yr[1], 1], x_length=5.2 * s, y_length=4.4 * s,
              tips=True, axis_config=AXIS_CFG)
    ax.shift(c - ax.get_center())
    g = VGroup()
    g.axes = ax
    lab_fs = max(28, 36 * s)
    g.xlab = MathTex("x", font_size=lab_fs, color=DIM).next_to(ax.x_axis.get_right(), DOWN, buff=0.12)
    g.ylab = MathTex("y", font_size=lab_fs, color=DIM).next_to(ax.y_axis.get_top(), LEFT, buff=0.12)
    g.curve = ax.plot(f, x_range=[-2, 2], color=BLUE, stroke_width=5 if s > 0.8 else 4)
    g.tan = Line(ax.c2p(-0.75, 0), ax.c2p(0.75, 0), color=GREEN, stroke_width=5)
    g.dot = Dot(ax.c2p(0, 0), radius=0.1 if s > 0.8 else 0.08, color=YELLOW).set_z_index(2)
    g.lab = MathTex(tex, font_size=max(30, 40 * s), color=BLUE).move_to(ax.c2p(*anchor))
    g.add(ax, g.xlab, g.ylab, g.curve, g.tan, g.dot, g.lab)
    return g


def figure30():
    fig = VGroup(build_panel("cube"), build_panel("quart"))
    fig.cube, fig.quart = fig[0], fig[1]
    return fig


CHAINS = {
    "cube": (["x^3", r"\to", "3x^2", r"\to", "6x", r"\to", "6", r"\to", "0"], ["0", "0", "0", "6"]),
    "quart": (["x^4", r"\to", "4x^3", r"\to", "12x^2", r"\to", "24x", r"\to", "24"],
              ["0", "0", "0", "0", "24"]),
}
NEG_QUART = ["-x^4", r"\to", "-4x^3", r"\to", "-12x^2", r"\to", "-24x", r"\to", "-24"]
CARD_FS = 40
CARD_Y = -0.35


def chain_expr(parts, fs=CARD_FS):
    e = MathTex(*parts, font_size=fs, color=FG)
    e[0].set_color(BLUE)
    for i in range(2, len(parts), 2):
        e[i].set_color(GREEN)
    return e


def build_card(kind):
    parts, values = CHAINS[kind]
    expr = chain_expr(parts)
    x = -LAY_B[1] if kind == "cube" else LAY_B[1]
    expr.move_to([x, CARD_Y, 0])
    frame = RoundedRectangle(corner_radius=0.15, width=expr.width + 0.6, height=expr.height + 0.6)
    frame.set_stroke(YELLOW, 2.5).set_fill(opacity=0).move_to(expr)
    vals = VGroup(*[MathTex(v, font_size=CARD_FS, color=FG).move_to(
        [expr[2 * i].get_x(), frame.get_bottom()[1] - 0.45, 0]) for i, v in enumerate(values)])
    last = vals[-1]
    ring = Circle(radius=max(last.width, last.height) / 2 + 0.17, color=YELLOW, stroke_width=4).move_to(last)
    card = VGroup(frame, expr, vals, ring)
    card.frame, card.expr, card.vals, card.ring = frame, expr, vals, ring
    return card


def chain_cards():
    g = VGroup(build_card("cube"), build_card("quart"))
    g.cube, g.quart = g[0], g[1]
    return g


def s3_rule_card():
    lines = VGroup(
        MathTex(r"\dfrac{d^2y}{dx^2} > 0 \Rightarrow \text{local minimum}", font_size=30),
        MathTex(r"\dfrac{d^2y}{dx^2} < 0 \Rightarrow \text{local maximum}", font_size=30),
    ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    frame = RoundedRectangle(corner_radius=0.15, width=lines.width + 0.5, height=lines.height + 0.45)
    frame.set_stroke(DIM, 2).set_fill(opacity=0).move_to(lines)
    return VGroup(frame, lines)


def general_rule():
    head = MathTex(r"\text{first non-zero derivative } \dfrac{d^ny}{dx^n} \text{ at the stationary point:}",
                   font_size=34)
    rows = [MathTex(r"n \text{ odd}", r"\;\to\;", r"\text{point of inflection}", font_size=34),
            MathTex(r"n \text{ even and positive}", r"\;\to\;", r"\text{local minimum}", font_size=34),
            MathTex(r"n \text{ even and negative}", r"\;\to\;", r"\text{local maximum}", font_size=34)]
    for r in rows:
        r[1].set_color(DIM)
    note = MathTex(r"n = 2:\ \text{the second-derivative test}", font_size=32, color=DIM)
    body = VGroup(*rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    g = VGroup(head, body, note).arrange(DOWN, buff=0.26)
    note.align_to(body, LEFT)
    g.move_to([0, -1.95, 0])
    g.head, g.rows, g.note = head, rows, note
    return g


def tilted_tangent(ax, x0, half=0.42):
    p = ax.c2p(x0, x0 ** 3)
    q = ax.c2p(x0 + 0.1, x0 ** 3 + 3 * x0 ** 2 * 0.1)
    d = (q - p) / np.linalg.norm(q - p)
    return Line(p - half * d, p + half * d, color=GREEN, stroke_width=5).set_z_index(1)


def panel_moves(p, q):
    """Move on-screen panel p into the layout of the built panel q (shapes; same-string labels)."""
    return [Transform(getattr(p, k), getattr(q, k)) for k in ("axes", "xlab", "ylab", "curve", "tan", "dot", "lab")]


class Higher(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c6.higher.1: Figure 30, and the second-derivative test is silent ──
    def clip1(self):
        fig = figure30()
        self.cube, self.quart = fig.cube, fig.quart
        cu, qu = self.cube, self.quart
        with self.say("c6.higher.1") as c:
            self.play(*appear(cu.axes, cu.xlab, cu.ylab, qu.axes, qu.xlab, qu.ylab, shift=None, lag=0.1),
                      run_time=min(1.2, c.until("cube")))
            c.wait_until("cube")
            self.play(Create(cu.curve), *appear(cu.lab), run_time=min(1.8, c.until("quart")))
            c.wait_until("quart")
            self.play(Create(qu.curve), *appear(qu.lab), run_time=min(1.8, c.until("both")))
            c.wait_until("both")
            self.play(GrowFromCenter(cu.dot), GrowFromCenter(qu.dot), GrowFromCenter(cu.tan),
                      GrowFromCenter(qu.tan), run_time=1.0)
            both = MathTex(r"\dfrac{dy}{dx} = \dfrac{d^2y}{dx^2} = 0 \quad \text{at } x = 0", font_size=40)
            both.move_to([0, -2.45, 0])
            self.play(*appear(both), run_time=1.0)
            c.wait_until("nothing")
            card = s3_rule_card().move_to([3.3, -2.45, 0])
            q = T("?", size=72, color=YELLOW).next_to(card, RIGHT, buff=0.3)
            self.play(both.animate.move_to([-3.4, -2.45, 0]), run_time=1.0)
            self.play(*appear(card, q, lag=0.5), run_time=1.4)   # early: the "?" is the card's verdict
            c.wait_until("shapes")
            self.play(VShowPassingFlash(cu.curve.copy().set_stroke(YELLOW, 9), time_width=0.6),
                      run_time=2.2)
            c.wait_until("minimum")
            bottom = qu.axes.plot(lambda x: x ** 4, x_range=[-0.9, 0.9]).set_stroke(YELLOW, 9)
            self.play(VShowPassingFlash(bottom, time_width=1.0), FlashAround(qu.dot, color=YELLOW),
                      run_time=1.6)
        self.both, self.s3card, self.q1 = both, card, q

    # ── c6.higher.2: keep differentiating, the two chains ──
    def clip2(self):
        cu, qu = self.cube, self.quart
        cards = chain_cards()
        cc, qc = cards.cube, cards.quart
        with self.say("c6.higher.2") as c:
            self.play(*during(disappear(self.both, self.s3card, self.q1), 0, 0.45),
                      *during(panel_moves(cu, build_panel("cube", LAY_B)) +
                              panel_moves(qu, build_panel("quart", LAY_B)), 0.3, 1),
                      run_time=min(1.8, c.until("card")))
            c.wait_until("card")
            self.play(FadeIn(cc.frame), *appear(cc.expr[0]), run_time=1.2)
            for k, cue, nth in ((1, "three", 0), (3, "six", 0), (5, "six", 1), (7, "zero", 0)):
                c.wait_until(cue, nth=nth)
                self.play(*appear(cc.expr[k], cc.expr[k + 1], lag=0.15, shift=None),
                          run_time=0.9 if k == 1 else 0.7)
            c.wait_until("atzero")
            self.play(*appear(*cc.vals, lag=0.2, shift=0.25 * UP), run_time=1.2)
            c.wait_until("six", nth=2)
            n3 = MathTex(r"\dfrac{d^3}{dx^3}\left(x^3\right) = 6 \neq 0", font_size=34)
            n3.move_to([cc.get_x(), -2.35, 0])
            self.play(GrowFromCenter(cc.ring), *appear(n3), run_time=1.2)
            c.wait_until("quartchain")
            self.play(FadeIn(qc.frame), *appear(qc.expr[0]), run_time=1.2)
            for k, cue, nth in ((1, "four", 1), (3, "twelve", 0), (5, "twenty-four ex", 0), (7, "twenty-four", 1)):
                c.wait_until(cue, nth=nth)
                self.play(*appear(qc.expr[k], qc.expr[k + 1], lag=0.15, shift=None),
                          run_time=0.9 if k == 1 else 0.7)
            c.wait_until("fourth")
            n4a = MathTex(r"\dfrac{d^3}{dx^3}\left(x^4\right) = 0", font_size=34)
            n4b = MathTex(r"\dfrac{d^4}{dx^4}\left(x^4\right) = 24 > 0", font_size=34)
            VGroup(n4a, n4b).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([qc.get_x(), -2.75, 0])
            self.play(*appear(*qc.vals, lag=0.2, shift=0.25 * UP), run_time=1.2)
            self.play(*appear(n4a), run_time=1.0)
            c.wait_until("twenty-four", nth=2)
            self.play(GrowFromCenter(qc.ring), *appear(n4b), run_time=1.2)
        settle(self, cc)
        settle(self, qc)
        self.cc, self.qc, self.notes = cc, qc, [n3, n4a, n4b]

    # ── c6.higher.3: the general rule ──
    def clip3(self):
        cu, qu, cc, qc = self.cube, self.quart, self.cc, self.qc
        rule = general_rule()
        cu_c, qu_c = build_panel("cube", LAY_C), build_panel("quart", LAY_C)
        keys = ("axes", "xlab", "ylab", "curve", "tan", "dot")
        with self.say("c6.higher.3") as c:
            self.play(*panel_moves(cu, cu_c), *panel_moves(qu, qu_c),
                      cc.animate.scale(0.72).move_to([-LAY_C[1], 0.3, 0]),
                      qc.animate.scale(0.72).move_to([LAY_C[1] - 0.3, 0.3, 0]),
                      run_time=min(2.0, c.until("find the first")))
            c.wait_until("find the first")
            self.play(*appear(rule.head), run_time=1.2)
            c.wait_until("odd")
            dim_q = [qu, qc]
            self.play(*during(disappear(*self.notes), 0, 0.45), *during(appear(rule.rows[0]), 0.5, 1),
                      *set_alpha(dim_q, 0.3), run_time=1.6)
            c.wait_until("gradient")
            tl, tr = tilted_tangent(cu_c.axes, -0.95), tilted_tangent(cu_c.axes, 0.95)
            self.play(GrowFromCenter(tl), GrowFromCenter(tr), run_time=1.0)
            grad = MathTex(r"\dfrac{dy}{dx} = 3x^2 > 0", r"\\ \text{for } x \neq 0", font_size=34)
            grad.move_to([0, 2.55, 0])
            self.play(*appear(grad), run_time=1.0)
            c.wait_until("even")
            self.play(*appear(rule.rows[1]), *set_alpha(dim_q, 1), *set_alpha([cu, cc, tl, tr, grad], 0.3),
                      run_time=1.2)
            c.wait_until("neg")
            self.play(*appear(rule.rows[2]), *disappear(grad), run_time=1.2)
            c.wait_until("flip")
            nq = build_panel("nquart", LAY_C)
            lmax = T("local maximum", size=30, color=YELLOW).move_to([1.15, 3.0, 0])
            arr = Arrow(lmax.get_right(), nq.dot.get_center(), buff=0.22, stroke_width=3, color=YELLOW, max_tip_length_to_length_ratio=0.12)
            old_expr, old_val = qc.expr, qc.vals[-1]
            neg_expr = chain_expr(NEG_QUART, CARD_FS * 0.72).move_to(old_expr)
            neg_val = MathTex("-24", font_size=CARD_FS * 0.72).move_to(old_val)
            ring2 = Circle(radius=max(neg_val.width, neg_val.height) / 2 + 0.13, color=YELLOW,
                           stroke_width=4).move_to(neg_val)
            frame2 = qc.frame.copy().stretch_to_fit_width(max(qc.frame.width, neg_expr.width + 0.45))
            # the name leaves before the curve flips and the new one lands once it has settled
            self.play(*during(disappear(qu.lab), 0, 0.22),
                      *during([Transform(getattr(qu, k), getattr(nq, k)) for k in keys], 0.2, 0.75),
                      *during(appear(nq.lab), 0.78, 1),
                      *edit(old_expr, neg_expr), *edit(old_val, neg_val), Transform(qc.ring, ring2),
                      Transform(qc.frame, frame2), *during(appear(lmax) + [GrowArrow(arr)], 0.6, 1),
                      run_time=2.2)
            c.wait_until("two")
            back = build_panel("quart", LAY_C)
            back.lab.move_to(back.axes.c2p(-3.1, 11.0))   # clear of the curve, mirroring y = -x^4's spot
            back_expr = chain_expr(CHAINS["quart"][0], CARD_FS * 0.72).move_to(neg_expr)
            back_val = MathTex("24", font_size=CARD_FS * 0.72).move_to(neg_val)
            ring3 = Circle(radius=max(back_val.width, back_val.height) / 2 + 0.13, color=YELLOW,
                           stroke_width=4).move_to(back_val)
            frame3 = qc.frame.copy().stretch_to_fit_width(back_expr.width + 0.45)
            self.play(*during(disappear(nq.lab), 0, 0.22),
                      *during([Transform(getattr(qu, k), getattr(back, k)) for k in keys], 0.2, 0.75),
                      *during(appear(back.lab), 0.78, 1),
                      *edit(neg_expr, back_expr), *edit(neg_val, back_val),
                      Transform(qc.ring, ring3), Transform(qc.frame, frame3), *disappear(lmax, arr),
                      *set_alpha([cu, cc, tl, tr], 1), run_time=1.6)
            self.play(*appear(rule.note), run_time=1.0)
        settle(self, rule)
        self.rule = rule

    # ── c6.higher.4: e^{-1/x^2}, where the rule is silent ──
    def clip4(self):
        rule = self.rule
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 1.15, 1], x_length=9.0, y_length=2.8, tips=True,
                  axis_config=AXIS_CFG)
        ax.shift(np.array([0, -0.55, 0]) - ax.c2p(0, 0))
        xl = MathTex("x", font_size=36, color=DIM).next_to(ax.x_axis.get_right(), DOWN, buff=0.12)
        yl = MathTex("y", font_size=36, color=DIM).next_to(ax.y_axis.get_top(), LEFT, buff=0.12)

        def f(x):
            return np.exp(-1 / x ** 2) if abs(x) > 1e-3 else 0.0

        curve = ax.plot(f, x_range=[-3, 3, 0.01], color=BLUE, stroke_width=5)
        with self.say("c6.higher.4") as c:
            c.wait_until("every derivative")
            sweep_clear(self, rule.animate.scale(0.86).move_to([-0.3, -2.3, 0]), keep=[rule], run_time=1.6)
            self.play(*appear(ax, xl, yl, shift=None, lag=0.1), run_time=1.0)
            self.play(Create(curve), run_time=min(2.0, c.until("aside")))
            c.wait_until("minus one")
            f1 = MathTex(r"y = e^{-1/x^2}", font_size=44, color=BLUE)
            f2 = MathTex(r"y(0) = 0", font_size=44)
            VGroup(f1, f2).arrange(RIGHT, buff=0.6).to_corner(UL, buff=0.5)
            self.play(*appear(f1), run_time=1.0)
            c.wait_until("value")
            self.play(*appear(f2), run_time=1.0)
            c.wait_until("flatflat")
            flat = MathTex(r"y^{(n)}(0) = 0 \text{ for every } n", font_size=40).to_corner(UR, buff=0.5)
            self.play(*appear(flat), run_time=1.0)
            c.wait_until("silent")
            q = T("?", size=72, color=YELLOW).next_to(rule, RIGHT, buff=0.4)
            self.play(*appear(q), run_time=1.0)
            c.wait_until("minimum")
            dot = Dot(ax.c2p(0, 0), radius=0.1, color=YELLOW).set_z_index(2)
            mlab = T("minimum", size=32, color=YELLOW).next_to(dot, UP, buff=0.55)
            self.play(GrowFromCenter(dot), *appear(mlab), run_time=1.0)
            c.wait_until("since")
            pos = MathTex(r"y > 0 \text{ for } x \neq 0", font_size=40).next_to(flat, DOWN, buff=0.35)
            pos.align_to(flat, RIGHT)
            self.play(*appear(pos), run_time=1.0)
        self.wait(1.8)
