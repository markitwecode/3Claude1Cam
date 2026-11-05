"""Chapter 4, scene 1: hook: from the product rule once to the tenth derivative. Clips c4.hook.1 – c4.hook.4."""
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
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

PART = "Part 4 · Leibniz's formula"


# ====================== exported helpers (siblings load these) ======================
def open_card():
    """The chapter's title card, bare and static, centred at ORIGIN (ch3 s7 ends on exactly this)."""
    return title_card(PART)


def question(size=64):
    """d^10/dx^10 (x^2 e^{-x}) = ?   Parts: [0] operator, [1] '(', [2] x^2 BLUE, [3] e^{-x} PURPLE,
    [4] ')', [5] '=', [6] '?' YELLOW."""
    q = MathTex(r"\frac{d^{10}}{dx^{10}}", r"\Big(", r"x^2", r"e^{-x}", r"\Big)", r"=\;", r"?",
                font_size=size)
    q[2].set_color(BLUE)
    q[3].set_color(PURPLE)
    q[6].set_color(YELLOW)
    return q


def product_rule(size=72):
    """(fg)' = f'g + fg'.  Parts: [0] '(', [1] f, [2] g, [3] ")'", [4] '=', [5] f', [6] g, [7] '+', [8] f, [9] g'."""
    r = MathTex("(", "f", "g", ")'", "=", "f'", "g", "+", "f", "g'", font_size=size)
    for i in (1, 5, 8):
        r[i].set_color(BLUE)
    for i in (2, 6, 9):
        r[i].set_color(PURPLE)
    return r


def _term(nf, ng, size):
    t = MathTex("f" + "'" * nf, "g" + "'" * ng, font_size=size)
    t[0].set_color(BLUE)
    t[1].set_color(PURPLE)
    return t


TREE_W = 9.6        # horizontal span of level k is TREE_W, node pitch TREE_W / 2**k
TREE_PITCH = 1.35   # vertical pitch between levels
TREE_SIZES = {0: 52, 1: 44, 2: 36}   # levels >= 3 are dots


def doubling_tree(levels=3):
    """The product-rule doubling tree, root `fg` at the top, `levels` rounds below it.
    `.nodes[k]`: VGroup of level k's 2**k nodes, left to right (MathTex f^(a) g^(b) for k <= 2, f BLUE
    g PURPLE; Dots for k >= 3, coloured like their branch). `.edges[k]`: VGroup of the 2**k lines into
    level k (`.edges[0]` empty); left child (prime lands on f) BLUE, right child (on g) PURPLE.
    The whole tree is centred at ORIGIN; level pitches do not depend on `levels`."""
    top = levels * TREE_PITCH / 2
    nodes, edges = [], [VGroup()]
    counts = [(0, 0)]
    for k in range(levels + 1):
        y = top - k * TREE_PITCH
        dx = TREE_W / 2 ** k
        if k > 0:
            counts = [c for (a, b) in counts for c in ((a + 1, b), (a, b + 1))]
        row = VGroup()
        for i, (a, b) in enumerate(counts):
            x = (i - (2 ** k - 1) / 2) * dx
            if k in TREE_SIZES:
                n = _term(a, b, TREE_SIZES[k])
            else:
                n = Dot(radius=0.09, color=BLUE if i % 2 == 0 else PURPLE)
            n.move_to([x, y, 0])
            row.add(n)
        nodes.append(row)
        if k > 0:
            lines = VGroup()
            for i, child in enumerate(row):
                parent = nodes[k - 1][i // 2]
                lines.add(Line(parent.get_bottom() + DOWN * 0.08, child.get_top() + UP * 0.08,
                               color=BLUE if i % 2 == 0 else PURPLE, stroke_width=4))
            edges.append(lines)
    tree = VGroup(*[m for k in range(levels + 1) for m in (edges[k], nodes[k])])
    tree.nodes = nodes
    tree.edges = edges
    return tree


def _count_num(n, size=96):
    return MathTex(str(n), font_size=size, color=GOLD)


def _counter(n):
    num = _count_num(n)
    lab = T("terms", size=30, color=DIM).next_to(num, DOWN, buff=0.25)
    g = VGroup(num, lab)
    g.num = num
    g.label = lab
    return g


def counter_1024():
    """The GOLD term counter as it lands: `.num` (MathTex "1024", GOLD, font 96) over `.label`
    (T "terms", 30, DIM). VGroup at ORIGIN."""
    return _counter(1024).move_to(ORIGIN)


# ---------- part three stand-ins (ch3 not built yet)
def _circle_thumb(u=0.5):
    ax = Axes(x_range=[-3, 5, 1], y_range=[-3.5, 3.5, 1], x_length=8 * u, y_length=7 * u, tips=False,
              axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
    circ = Circle(radius=3 * u, color=BLUE, stroke_width=4).move_to(ax.c2p(1, 0))
    centre = Dot(ax.c2p(1, 0), radius=0.05, color=BLUE)
    dash = DashedLine(ax.c2p(2.8, -3.3), ax.c2p(2.8, 3.3), color=DIM, stroke_width=2, dash_length=0.08)
    tans, dots = VGroup(), VGroup()
    for y0, m in ((2.4, -0.75), (-2.4, 0.75)):
        h = 1.3
        tans.add(Line(ax.c2p(2.8 - h, y0 - m * h), ax.c2p(2.8 + h, y0 + m * h), color=GREEN, stroke_width=4))
        dots.add(Dot(ax.c2p(2.8, y0), radius=0.07, color=YELLOW))
    g = VGroup(ax, circ, centre, dash, tans, dots)
    g.axes, g.circle, g.dash, g.tangents, g.dots = ax, circ, dash, tans, dots
    return g


def _recip_thumb(u=1.6):
    ax = Axes(x_range=[0, 2.2, 1], y_range=[0, 2.2, 1], x_length=2.2 * u, y_length=2.2 * u, tips=False,
              axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
    mirror = DashedLine(ax.c2p(0, 0), ax.c2p(2.2, 2.2), color=DIM, stroke_width=2, dash_length=0.08)
    cube = ax.plot(lambda x: x ** 3, x_range=[0, 2.2 ** (1 / 3)], color=BLUE, stroke_width=3)
    cube.set_stroke(opacity=0.4)
    root = ax.plot(lambda x: np.cbrt(x), x_range=[0, 2.2], color=BLUE, stroke_width=4)
    t3 = Line(ax.c2p(0.75, 0.25), ax.c2p(1.25, 1.75), color=GREEN, stroke_width=3).set_stroke(opacity=0.5)
    t13 = Line(ax.c2p(0.25, 0.75), ax.c2p(1.75, 1.25), color=GREEN, stroke_width=4)
    pt = Dot(ax.c2p(1, 1), radius=0.07, color=YELLOW)
    tri = VGroup(  # TEAL slope triangles, as ch3 s6 plans: run 0.2 / rise 0.6 on x^3, mirrored on the root
        VMobject(color=TEAL, stroke_width=3).set_points_as_corners(
            [ax.c2p(1, 1), ax.c2p(1.2, 1), ax.c2p(1.2, 1.6)]).set_stroke(opacity=0.5),
        VMobject(color=TEAL, stroke_width=3).set_points_as_corners(
            [ax.c2p(1, 1), ax.c2p(1.6, 1), ax.c2p(1.6, 1.2)]))
    s3 = MathTex(r"\text{slope }", "3", font_size=34)
    s3[1].set_color(GOLD)
    s3.move_to(ax.c2p(0.42, 1.95))
    s13 = MathTex(r"\text{slope }", r"\tfrac13", font_size=34)
    s13[1].set_color(GOLD)
    s13.move_to(ax.c2p(1.62, 0.55))
    g = VGroup(ax, mirror, cube, t3, root, t13, tri, pt, s3, s13)
    g.axes, g.mirror, g.cube, g.root, g.readouts = ax, mirror, cube, root, VGroup(s3, s13)
    return g


def _from_ch3(stem, helper, **kw):
    """ch3's own figure once its scene file defines the helper; None (use the stand-in) until then."""
    try:
        from lib.paths import load_scene
        mod = load_scene(stem)
        if hasattr(mod, helper):
            return getattr(mod, helper)(**kw)
    except Exception:
        pass
    return None


def _trim_pair(g):
    """ch3's swapped_pair() as a thumbnail: curves, dashed y = x, GREEN tangents, the point (1, 1);
    the delta legs/braces/labels go, and the slope readouts sit beside their tangents (in ch3 they
    stand at fixed screen spots far right, which would push the pair off-centre)."""
    for pic in (g.orig, g.mirror):
        for k in ("run_leg", "rise_leg", "right_angle", "run_brace", "run_lab", "rise_brace", "rise_lab",
                  "q_dot"):
            m = getattr(pic, k, None)
            if m is not None:
                pic.remove(m)
    g.r3.next_to(g.orig.tangent.get_end(), LEFT, buff=0.75).shift(0.5 * DOWN)
    g.r13.next_to(g.mirror.tangent.get_end(), UP, buff=0.3).shift(0.6 * LEFT)
    return g


def last_time_thumbs():
    """Part three's callback: ch3's circle_figure() / swapped_pair() once those files define them,
    else these STAND-INS: `.circle` (ch3 s3's circle, centre (1, 0),
    radius 3, BLUE, dashed x = 2.8, GREEN tangent lines at (2.8, +-2.4)) and `.recip` (ch3 s6's swapped
    Figure 29: faint y = x^3, dashed y = x, BLUE cube root, GREEN tangents slope 3 / 1/3 at (1, 1), GOLD
    readouts), side by side, centred at ORIGIN, both 4.2 tall."""
    c = _from_ch3("ch3_s3_circle", "circle_figure", dashed=True, points=True, tangents=True) or _circle_thumb()
    r = _from_ch3("ch3_s6_reciprocal", "swapped_pair")
    r = _trim_pair(r) if r is not None else _recip_thumb()
    c.scale_to_fit_height(4.2)
    r.scale_to_fit_height(4.2)
    g = VGroup(c, r).arrange(RIGHT, buff=1.6, aligned_edge=DOWN).move_to(ORIGIN)
    g.circle, g.recip = c, r
    return g


# ---------- stick-figure room
def _person(raised):
    head = Circle(radius=0.16, color=FG, stroke_width=3).move_to(UP * 0.62)
    body = Line(UP * 0.46, DOWN * 0.15, color=FG, stroke_width=3)
    sh = UP * 0.34
    left = Line(sh, sh + np.array([-0.25, -0.35, 0]), color=FG, stroke_width=3)
    if raised:
        right = Line(sh, sh + np.array([0.4, 0.52, 0]), color=YELLOW, stroke_width=3)
    else:
        right = Line(sh, sh + np.array([0.25, -0.35, 0]), color=FG, stroke_width=3)
    p = VGroup(head, body, left, right)
    if not raised:
        p.set_stroke(opacity=0.5)
    return p


def _room():
    pattern = [0, 1, 0, 0, 1, 1, 0, 1, 0]
    return VGroup(*[_person(r) for r in pattern]).arrange(RIGHT, buff=0.55, aligned_edge=DOWN)


class HookScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c4.hook.1: title card, last time
    def clip1(self):
        with self.say("c4.hook.1") as c:
            card = open_card()
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.6),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 0.6),
                      time_span(FadeIn(card.course), 0.15, 0.75),
                      time_span(FadeIn(card.part), 0.3, 0.9), run_time=0.9)
            c.wait_until("last")

            thumbs = last_time_thumbs().shift(UP * 0.35)
            cap_c = T("an equation as it stands", size=30, color=DIM).next_to(thumbs.circle, DOWN, buff=0.35)
            cap_r = T("the reciprocal rule", size=30, color=DIM).next_to(thumbs.recip, DOWN, buff=0.35)
            cap_r.align_to(cap_c, UP)
            self.play(*during([FadeOut(card)], 0, 0.4),
                      *during([FadeIn(thumbs.circle, shift=0.2 * DOWN)], 0.45, 0.85),
                      *during([FadeIn(thumbs.recip, shift=0.2 * DOWN)], 0.6, 1), run_time=2.0)
            c.wait_until(own_word=cap_c)
            self.play(*appear(cap_c), run_time=1.0)
            c.wait_until(own_word=cap_r)
            self.play(*appear(cap_r), run_time=1.0)
            self.thumbs = VGroup(thumbs.circle, thumbs.recip, cap_c, cap_r)

    # ---- c4.hook.2: product rule once, then ten times
    def clip2(self):
        with self.say("c4.hook.2") as c:
            rule = product_rule(80).move_to(UP * 1.5)
            self.play(*during([FadeOut(self.thumbs)], 0, 0.45),
                      *during([FadeIn(rule, shift=0.2 * DOWN)], 0.5, 1), run_time=1.6)
            c.wait_until("once is easy")
            self.play(FlashAround(rule, run_time=1.5, time_width=1.5, buff=0.2))
            lab = T("the product rule, part two", size=30, color=DIM).next_to(rule, DOWN, buff=0.45)
            c.wait_until("product rule", own_word=lab)
            self.play(*appear(lab), run_time=1.0)
            c.wait_until("ten")
            q = question().move_to(DOWN * 1.4)
            self.play(*appear(q), run_time=1.2)
            c.wait_until("squared")
            self.play(FlashUnder(q[2], run_time=1.2, time_width=1.5, color=BLUE))
            c.wait_until("minus")
            self.play(FlashUnder(q[3], run_time=1.2, time_width=1.5, color=PURPLE))
            self.rule, self.rule_lab, self.q = rule, lab, q

    # ---- c4.hook.3: the doubling tree
    def clip3(self):
        with self.say("c4.hook.3") as c:
            rule = self.rule
            self.play(*disappear(self.q, self.rule_lab), run_time=0.8)
            self.play(rule.animate.scale(0.7).move_to(UP * 3.3), run_time=1.2)

            tree = doubling_tree(3).move_to(LEFT * 1.1 + DOWN * 0.2)
            self.play(*fly(VGroup(rule[1], rule[2]), tree.nodes[0][0]), run_time=1.3)
            c.wait_until("splits")
            self.play(*[Create(e) for e in tree.edges[1]],
                      *during(appear(*tree.nodes[1], lag=0.3), 0.35, 1), run_time=1.6)

            ctr = _counter(2).move_to(RIGHT * 5.3 + DOWN * 0.2)
            c.wait_until("two terms")
            self.play(*appear(ctr.num, ctr.label, lag=0.3), run_time=1.0)
            c.wait_until("four")
            self.play(*[Create(e) for e in tree.edges[2]],
                      *during(appear(*tree.nodes[2], lag=0.15), 0.35, 1),
                      *swap(ctr.num, n4 := _count_num(4).move_to(ctr.num)), run_time=1.4)
            ctr.num = n4
            c.wait_until("eight")
            self.play(*[Create(e) for e in tree.edges[3]],
                      *during([GrowFromCenter(d) for d in tree.nodes[3]], 0.35, 1),
                      *swap(ctr.num, n8 := _count_num(8).move_to(ctr.num)), run_time=1.3)
            ctr.num = n8
            settle(self, tree)

            more = MathTex(r"\vdots", font_size=60, color=DIM).next_to(tree, DOWN, buff=0.15)
            c.wait_until("thousand")
            num = ctr.num
            centre = num.get_center()

            def tick(m, a):
                k = 3 + min(7, int(a * 7.999))
                m.become(_count_num(2 ** k).move_to(centre))

            self.play(*appear(more), UpdateFromAlphaFunc(num, tick), run_time=2.2, rate_func=linear)
            self.play(FlashAround(num, run_time=1.2, time_width=1.5, color=GOLD))
            self.tree = VGroup(tree, more)
            self.ctr = VGroup(num, ctr.label)
            self.add(self.ctr)

    # ---- c4.hook.4: the question; the room
    def clip4(self):
        with self.say("c4.hook.4", gap=2.2) as c:
            grp = VGroup(self.tree, self.ctr)
            grp.generate_target()
            more = self.tree[1]
            grp.target.shift(UP * (3.45 - self.tree[0].get_top()[1])).set_opacity(DIMMED)
            grp.target[0][1].set_opacity(0)
            self.play(*disappear(self.rule, more), MoveToTarget(grp), run_time=1.5)
            self.remove(more)

            ask = VGroup(T("a formula for the nth derivative", size=46, color=YELLOW),
                         T("of a product?", size=46, color=YELLOW)).arrange(DOWN, buff=0.22)
            ask.move_to(DOWN * 2.35)
            c.wait_until("formula", own_word=ask[0])
            self.play(*appear(ask), run_time=1.2)

            c.wait_until("hands")
            room = _room().scale(1.35).move_to(DOWN * 0.05)
            quote = T("“at least I’ll tell you something new today”", size=40, slant=ITALIC)
            quote.move_to(DOWN * 2.1)
            who = T("— the lecturer", size=28, color=DIM).next_to(quote, DOWN, buff=0.2).align_to(quote, RIGHT)
            self.play(*during(disappear(grp), 0, 0.45),
                      *during([ask.animate.move_to(UP * 2.55)], 0.2, 1), run_time=1.6)
            self.play(*appear(*room, lag=0.12), run_time=1.4)
            self.play(*appear(quote, who, lag=0.4), run_time=1.3)  # early: her line stays up while it is said

