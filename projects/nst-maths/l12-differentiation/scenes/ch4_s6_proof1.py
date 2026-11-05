"""Chapter 4, scene 6: proof by induction, the step splits into two sums. Clips c4.induction.1 – c4.induction.4.

Exported:
- dominoes() -> VGroup(tiles..., labels..., dots); .tiles (4 upright Rectangles), .labels (T "1".."4"),
  .dots (T "…"), .lean (the angle a tile falls to, radians). topple(dom, total, fall) -> list of
  time_span'd Rotates (play with run_time=total) that knock them down one after another.
- handover_shot() -> the last frame (see its docstring for the named parts).
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- exported helpers
def dominoes(n=4, h=1.3, w=0.28, pitch=1.0, label_size=30):
    """A row of n upright dominoes labelled 1..n, then "…", centred on ORIGIN."""
    tiles = VGroup(*[Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.35)
                     .move_to(RIGHT * pitch * i) for i in range(n)])
    labels = VGroup(*[T(str(i + 1), label_size, FG).next_to(t, DOWN, buff=0.12 + 0.06 * h)
                      for i, t in enumerate(tiles)])
    dots = T("…", label_size + 4, FG).move_to(tiles[-1].get_center() + RIGHT * pitch).align_to(labels, DOWN)
    dom = VGroup(*tiles, *labels, dots).move_to(ORIGIN)
    dom.tiles, dom.labels, dom.dots = list(tiles), list(labels), dots
    dom.lean = float(np.arcsin((pitch - w) / h))
    return dom


def topple(dom, total=3.0, fall=1.0):
    """The first tile tips and knocks the next, and so on: play(*topple(dom), run_time=total)."""
    n = len(dom.tiles)
    step = (total - fall) / max(1, n - 1)
    return [time_span(Rotate(t, angle=-dom.lean, about_point=t.get_corner(DR), rate_func=rush_into),
                      i * step, i * step + fall) for i, t in enumerate(dom.tiles)]


def _sib(stem, name):
    try:
        return getattr(load_scene(stem), name, None)
    except (FileNotFoundError, OSError):
        return None


def corner_card():
    """s2's notation card, small in the top-right corner."""
    f = _sib("ch4_s2_higher", "notation_card")
    if f is None:
        body = VGroup(MathTex(r"f^{(n)} = \frac{d^n f}{dx^n}", font_size=56))
    else:
        full = f()
        body = VGroup(full.main, full.zero)          # without the "a power" aside, too small up here
    frame = RoundedRectangle(corner_radius=0.2, width=body.width + 0.8, height=body.height + 0.8)
    frame.set_stroke(DIM, 2).set_fill(opacity=0).move_to(body)
    nc = VGroup(frame, *body).scale(0.52).to_corner(UR, buff=0.35)
    nc.frame = frame
    return nc


def mini_dominoes():
    return dominoes(h=0.65, w=0.14, pitch=0.5, label_size=28).to_corner(UL, buff=0.4)


def mt(*parts, size=38, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def place(m, anchor, x, y):
    m.shift(np.array([x, y, 0]) - anchor.get_center())
    return m


def limits(part):
    """(upper-limit glyphs, lower-limit glyphs) of a \\sum_{..}^{..} part."""
    sigma = max(part, key=lambda g: g.height)
    up = [g for g in part if g.get_y() > sigma.get_top()[1] - 0.02]
    lo = [g for g in part if g.get_y() < sigma.get_bottom()[1] + 0.02]
    return up, lo


XEQ = -2.6                       # x of the "=" every working line hangs from
S1_Y, S2_Y = 3.1, 1.68           # the two sums, final rows
PITCH, X0 = 2.0, -5.6             # box columns
BOX1_Y, BOX2_Y = -0.2, -2.0
E_X = 5.0                         # the detached term


def sum1():
    s = mt("=", r"\sum_{m=0}^{n}", r"\binom{n}{m}", r"f^{(n-m", "+1", ")}", r"g^{(m)}")
    s[2].set_color(YELLOW)
    s[4].set_color(BLUE)
    return place(s, s[0], XEQ, S1_Y)


def sum2a(y=S2_Y):
    s = mt("+", r"\sum_{m=0}^{n}", r"\binom{n}{m}", r"f^{(n-m)}", r"g^{(m", "+1", ")}")
    s[2].set_color(YELLOW)
    s[5].set_color(PURPLE)
    return place(s, s[0], XEQ, y)


def sum2b():
    s = mt("+", r"\sum_{m=0}^{n-1}", r"\binom{n}{m}", r"f^{(n-m)}", r"g^{(m", "+1", ")}",
           r"+\,f^{(0)} g^{(n+1)}")
    s[2].set_color(YELLOW)
    s[5].set_color(PURPLE)
    for g in limits(s[1])[0]:
        g.set_color(YELLOW)
    return place(s, s[0], XEQ, S2_Y)


def sum2c():
    s = mt("+", r"\sum_{m=1}^{n}", r"\binom{n}{", "m-1", "}", "f^{(", "n-m+1", ")}", "g^{(", "m", ")}",
           r"+\,f^{(0)} g^{(n+1)}")
    s[2].set_color(YELLOW)
    s[4].set_color(YELLOW)
    up, lo = limits(s[1])
    for g in up + [max(lo, key=lambda g: g.get_x())]:           # the new limits: n, and the 1 of m = 1
        g.set_color(YELLOW)
    s[3].set_color(YELLOW)            # m-1 (the changed coefficient), YELLOW like the rest of the binom
    for i in (6, 9):
        s[i].set_color(YELLOW)
    return place(s, s[0], XEQ, S2_Y)


R1 = [("f^{(n+1)}g", r"\binom{n}{0}"), ("f^{(n)}g'", r"\binom{n}{1}"), ("f^{(n-1)}g''", r"\binom{n}{2}"),
      None, ("f'g^{(n)}", r"\binom{n}{n}")]
R2 = [("f^{(n)}g'", r"\binom{n}{0}"), ("f^{(n-1)}g''", r"\binom{n}{1}"), None,
      ("f'g^{(n)}", r"\binom{n}{n-1}"), ("fg^{(n+1)}", r"\binom{n}{n}")]
MATCHED1, MATCHED2 = (1, 2, 4), (0, 1, 3)    # the columns that line up after the slide


def slot(spec, x, y, stroke=BLUE):
    if spec is None:
        prod = mt(r"\cdots", size=40).move_to([x, y, 0])
        s = VGroup(prod)
        s.box, s.prod, s.coef = None, prod, None
        return s
    prod = mt(spec[0], size=36).move_to([x, y, 0])
    box = RoundedRectangle(corner_radius=0.12, width=1.7, height=0.8).set_stroke(stroke, 2.5)
    box.set_fill(opacity=0).move_to([x, y, 0])
    coef = mt(spec[1], size=32, color=YELLOW).next_to(box, UP, buff=0.1)
    s = VGroup(box, prod, coef)
    s.box, s.prod, s.coef = box, prod, coef
    return s


def last_note():
    f = mt(r"\binom{n}{n}", r"f^{(0)} g^{(n+1)}", "=", r"f\,g^{(n+1)}", size=36)
    f[0].set_color(YELLOW)
    f.move_to([0, -3.1, 0]).align_to(RIGHT * 6.6, RIGHT)
    tag = mt("m = n", size=34, color=DIM).next_to(f, LEFT, buff=0.4)
    g = VGroup(tag, f)
    g.tag, g.formula = tag, f
    return g


def handover_shot():
    """The last frame. Parts: .card (s2's notation card, top-right), .dominoes (upright, top-left),
    .sum1 (= Σ_{0}^{n} C(n,m) f^{(n-m+1)} g^{(m)}), .sum2 (+ Σ_{1}^{n} C(n,m-1) f^{(n-m+1)} g^{(m)}
    + f^{(0)}g^{(n+1)}, changed parts YELLOW), .row1 / .row2 (lists of 5 slots; each slot a VGroup with
    .box .prod .coef, the "…" slot has box = coef = None; row2 = its first four slots, already slid one
    column right), .detached (row2's last slot, f g^{(n+1)}, on the right), .note (VGroup(.tag "m = n",
    .formula C(n,n) f^{(0)} g^{(n+1)} = f g^{(n+1)}) under it). Matched boxes have GREEN strokes."""
    card = corner_card()
    dom = mini_dominoes()
    s1, s2 = sum1(), sum2c()
    row1 = [slot(sp, X0 + PITCH * k, BOX1_Y, GREEN if k in MATCHED1 else BLUE) for k, sp in enumerate(R1)]
    row2 = [slot(sp, X0 + PITCH * (k + 1), BOX2_Y, GREEN if k in MATCHED2 else BLUE)
            for k, sp in enumerate(R2[:4])]
    det = slot(R2[4], E_X, BOX2_Y)
    note = last_note()
    shot = VGroup(card, dom, s1, s2, *row1, *row2, det, note)
    shot.card, shot.dominoes, shot.sum1, shot.sum2 = card, dom, s1, s2
    shot.row1, shot.row2, shot.detached, shot.note = row1, row2, det, note
    return shot


def badge(d):
    c = Circle(radius=0.28).set_stroke(FG, 2.5)
    return VGroup(c, T(d, 30, FG).move_to(c))


def leibniz():
    f = _sib("ch4_s4_formula", "leibniz_card")
    card = f(size=40) if f else VGroup(mt(r"(fg)^{(n)} = \sum_{m=0}^{n}\binom{n}{m} f^{(n-m)} g^{(m)}", size=40))
    frame = SurroundingRectangle(card, color=YELLOW, buff=0.25, corner_radius=0.15).set_stroke(YELLOW, 2.5)
    g = VGroup(frame, card).move_to([0.5, 2.75, 0])
    return card, frame


class ProofOne(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        # the final picture is exactly handover_shot(): swap in the canonical objects (an invisible cut)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)

    # ------------------------------------------------------------------ c1: the two steps
    def clip1(self):
        with self.say("c4.induction.1") as c:
            self.nc = corner_card()
            head = T("Proof by induction:", 48).move_to([-6.1, 3.15, 0], aligned_edge=LEFT)
            st1 = VGroup(badge("1"), mt("n = 1", size=44)).arrange(RIGHT, buff=0.35)
            st1.move_to([-5.6, 2.0, 0], aligned_edge=LEFT)
            st2 = VGroup(badge("2"), mt(r"\text{true for } n \;\Rightarrow\; \text{true for } n+1", size=44))
            st2.arrange(RIGHT, buff=0.35).move_to([-5.6, -0.5, 0], aligned_edge=LEFT)
            self.play(*appear(head, st1, st2, self.nc, lag=0.3), run_time=1.6)  # early: the proof's outline, walked next
            c.wait_until("base")
            base = mt(r"\binom{1}{0}", "f'g", "+", r"\binom{1}{1}", "fg'", size=48)
            base[0].set_color(YELLOW)
            base[3].set_color(YELLOW)
            base.move_to([-4.9, 0.75, 0], aligned_edge=LEFT)
            self.play(*flash([st1[0]]), *appear(base), run_time=1.5)
            c.wait_until("there")
            rhs = mt("=", "f'g + fg'", size=48).next_to(base, RIGHT, buff=0.25)
            rhs.shift(UP * (base[1].get_y() - rhs[1].get_y()))
            self.play(*appear(rhs), run_time=1.2)
            tick = check_mark().next_to(rhs, RIGHT, buff=0.4)
            lab = T("product rule", 30, GREEN).next_to(tick, RIGHT, buff=0.25)
            c.wait_until(own_word=lab)
            self.play(*appear(tick, lab, lag=0.3), run_time=1.2)
            c.wait_until("step")
            self.play(*recolor(list(st2[0]) + list(st2[1]), YELLOW), FlashAround(st2, color=YELLOW),
                      run_time=1.5)
            c.wait_until("domino")
            dom = dominoes().move_to([0, -2.55, 0])
            self.play(*appear(dom, shift=None), run_time=0.8)
            tot = max(1.6, min(3.0, c.until() - 0.1))
            self.play(*topple(dom, total=tot, fall=min(1.0, tot / 2.2)), run_time=tot)
            self.dom = dom

    # ------------------------------------------------------------------ c2: differentiate once more
    def clip2(self):
        with self.say("c4.induction.2") as c:
            mini = mini_dominoes()
            sweep_clear(self, Transform(self.dom, mini), keep=[self.nc, self.dom], run_time=1.4)
            card, frame = leibniz()
            tag = T("assume, for this n", 30, YELLOW).next_to(frame, LEFT, buff=0.3).align_to(frame, DOWN)
            self.play(*appear(card, frame, tag, lag=0.3), run_time=1.3)
            self.card, self.frame, self.tag = card, frame, tag

            c.wait_until("diff")
            L1 = mt(r"(fg)^{(n+1)}", "=", r"\frac{d}{dx}", r"\sum_{m=0}^{n}", r"\binom{n}{m}",
                    r"f^{(n-m)}", r"g^{(m)}")
            L1[4].set_color(YELLOW)
            place(L1, L1[1], XEQ, 0.95)
            self.play(*appear(L1), run_time=1.3)

            c.wait_until("inside")
            L1b = mt(r"(fg)^{(n+1)}", "=", r"\sum_{m=0}^{n}", r"\binom{n}{m}", r"\frac{d}{dx}", r"\Big[",
                     r"f^{(n-m)}", r"g^{(m)}", r"\Big]")
            L1b[3].set_color(YELLOW)
            place(L1b, L1b[1], XEQ, 0.95)
            pairs = [(0, 0), (1, 1), (3, 2), (4, 3), (5, 6), (6, 7)]
            self.play(*[Transform(L1[i], L1b[j]) for i, j in pairs],
                      Transform(L1[2], L1b[4], path_arc=1.4 * PI),
                      *during([FadeIn(L1b[5]), FadeIn(L1b[8])], 0.6, 1),
                      run_time=min(2.0, 0.8 * c.until("rule")))
            self.remove(*L1.get_family(), L1b[5], L1b[8])
            self.add(L1b)
            self.L1 = L1b

            c.wait_until("rule")
            L2 = mt("=", r"\sum_{m=0}^{n}", r"\binom{n}{m}", r"\Big[", r"f^{(n-m", "+1", ")}", r"g^{(m)}", "+",
                    r"f^{(n-m)}", r"g^{(m", "+1", r")}", r"\Big]")
            L2[2].set_color(YELLOW)
            place(L2, L2[0], XEQ, -0.45)
            n114 = T("(114)", 30, DIM).next_to(L2, RIGHT, buff=0.35)
            self.play(*appear(L2, n114, lag=0.3), run_time=1.3)
            c.wait_until("on f")
            self.play(*recolor(L2[5], BLUE), FlashAround(L2[5], color=BLUE), run_time=1.2)
            c.wait_until("on g")
            self.play(*recolor(L2[11], PURPLE), FlashAround(L2[11], color=PURPLE), run_time=1.2)
            self.L2, self.n114 = L2, n114

            c.wait_until("two")
            s1 = sum1()
            self.S1 = place(s1, s1[0], XEQ, -1.75)
            self.S2 = sum2a(-2.95)
            self.play(*appear(self.S1, self.S2, lag=0.35), run_time=min(1.6, c.until()))

    # ------------------------------------------------------------------ c3: the rows of terms
    def clip3(self):
        with self.say("c4.induction.3") as c:
            gone = [self.card, self.frame, self.tag, self.L1, self.L2, self.n114]
            self.play(*during(disappear(*gone), 0, 0.45),
                      *during([self.S1.animate.shift(UP * (S1_Y + 1.75)),
                               self.S2.animate.shift(UP * (S2_Y + 2.95))], 0.45, 1),
                      run_time=2.0)
            r1 = [slot(sp, X0 + PITCH * k, BOX1_Y) for k, sp in enumerate(R1)]
            r2 = [slot(sp, X0 + PITCH * k, BOX2_Y) for k, sp in enumerate(R2)]
            self.r1, self.r2 = r1, r2
            self.play(*appear(*r1, shift=None, lag=0.2), run_time=1.6)
            c.wait_until("second")
            self.play(*appear(*r2, shift=None, lag=0.2), run_time=1.6)

            c.wait_until("matching")
            self.play(FlashAround(r1[1].box, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("out of step")
            self.play(FlashAround(r2[0].box, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("last")
            e = r2[4]
            self.play(e.animate.shift(RIGHT * (E_X - e.box.get_x())), run_time=1.5)
            note = last_note()
            c.wait_until("where m equals n")
            self.play(*appear(note.tag), run_time=1.0)
            c.wait_until("its coefficient")
            self.play(*appear(note.formula), run_time=1.3)
            self.note = note

            c.wait_until("rest")
            new = sum2b()
            self.play(*edit(self.S2, new), run_time=min(1.5, c.until()))
            self.S2 = new

    # ------------------------------------------------------------------ c4: relabel and slide
    def clip4(self):
        with self.say("c4.induction.4") as c:
            rel = mt(r"m \to m-1", size=36, color=YELLOW).move_to([-5.0, S2_Y, 0])
            c.wait_until("replace")
            self.play(*appear(rel), run_time=1.0)
            new = sum2c()
            self.play(*edit(self.S2, new), run_time=min(1.6, c.until("the new m")))
            self.S2 = new

            c.wait_until("the new m")
            self.play(FlashAround(new[1], run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("the coefficient")
            self.play(FlashAround(VGroup(*new[2:5]), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("and the product")
            self.play(FlashAround(VGroup(*new[5:11]), run_time=1.8, time_width=1.5), run_time=1.8)

            c.wait_until("slide")
            self.play(*during(disappear(rel), 0, 0.4),
                      *[s.animate.shift(RIGHT * PITCH) for s in self.r2[:4]], run_time=2.0)

            c.wait_until("match")
            cols = list(zip(MATCHED1, MATCHED2))
            anims = []
            for k, (i, j) in enumerate(cols):
                for b in (self.r1[i].box, self.r2[j].box):
                    anims.append(time_span(FlashAround(b, color=GREEN, time_width=1.5), 0.3 * k, 0.3 * k + 1.2))
                    anims.append(time_span(b.animate.set_stroke(GREEN), 0.3 * k, 0.3 * k + 1.2))
            self.play(*anims, run_time=1.8)
            c.wait_until("coefficients")
            coefs = [self.r1[i].coef for i, _ in cols] + [self.r2[j].coef for _, j in cols]
            self.play(*flash(coefs), run_time=1.5)
