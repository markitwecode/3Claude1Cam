"""Chapter 4, scene 4: n choose m, then Leibniz's formula and its n = 2 check. Clips c4.formula.1 – c4.formula.4.

Exported helpers (siblings, the recap, ch5 and ch7 load them):
  leibniz_card(size=56): one VGroup, centred at ORIGIN,
      (fg)^{(n)} = \\sum_{m=0}^{n} \\binom{n}{m} f^{(n-m)} g^{(m)}
      parts .lhs (f BLUE, g PURPLE), .eq, .sum (sign with limits, FG), .binom (YELLOW),
      .fpart (BLUE), .gpart (PURPLE); also .tex (the MathTex; .tex[i] are the parts in that order).
  prime_slots(n, m=None, picks=None, side=0.8, pitch=1.0): a row of n square slots, centred at ORIGIN,
      each holding one prime; picks (default: the last m) PURPLE (sent to g), the rest BLUE (sent to
      f); m=None leaves every slot FG. .slots[i] = VGroup(box, prime), .boxes, .primes.
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


# ---------------------------------------------------------------- exported helpers
CARD_PARTS = [r"(fg)^{(n)}", "=", r"\sum_{m=0}^{n}", r"\binom{n}{m}", r"f^{(n-m)}", r"g^{(m)}"]


def _colour_fg(part, f_idx, g_idx):
    for i in f_idx:
        if i < len(part):
            part[i].set_color(BLUE)
    for i in g_idx:
        if i < len(part):
            part[i].set_color(PURPLE)


def leibniz_card(size=56):
    tex = MathTex(*CARD_PARTS, font_size=size, color=FG)
    lhs, eq, sm, binom, fpart, gpart = tex
    _colour_fg(lhs, [1], [2])                 # ( f g ) ( n )
    binom.set_color(YELLOW)
    fpart.set_color(BLUE)
    gpart.set_color(PURPLE)
    card = VGroup(*tex)
    card.move_to(ORIGIN)
    card.tex = tex
    card.lhs, card.eq, card.sum, card.binom, card.fpart, card.gpart = lhs, eq, sm, binom, fpart, gpart
    return card


def prime_slots(n, m=None, picks=None, side=0.8, pitch=1.0):
    if picks is None and m is not None:
        picks = list(range(n - m, n))
    slots, boxes, primes = [], [], []
    for i in range(n):
        if m is None and picks is None:
            col = FG
        else:
            col = PURPLE if i in picks else BLUE
        box = RoundedRectangle(corner_radius=0.08, width=side, height=side)
        box.set_stroke(col, 3).set_fill(opacity=0)
        pr = MathTex(r"\prime", font_size=56 * side / 0.8, color=col)
        box.move_to(RIGHT * i * pitch)
        pr.move_to(box).shift(UP * 0.06 * side / 0.8)
        slots.append(VGroup(box, pr))
        boxes.append(box)
        primes.append(pr)
    g = VGroup(*slots).move_to(ORIGIN)
    g.slots, g.boxes, g.primes = slots, boxes, primes
    return g


# ---------------------------------------------------------------- scene pieces
def _hero(size=56):
    """Her board's form: d^n(fg)/dx^n = sum binom f^{(n-m)}(x) g^{(m)}(x)."""
    parts = [r"\frac{d^n (fg)}{dx^n}", "=", r"\sum_{m=0}^{n}", r"\binom{n}{m}", r"f^{(n-m)}", "(x)",
             r"g^{(m)}", "(x)"]
    h = MathTex(*parts, font_size=size, color=FG)
    _colour_fg(h[0], [3], [4])                # d n ( f g ) — d x n
    h[3].set_color(YELLOW)
    h[4].set_color(BLUE)
    h[6].set_color(PURPLE)
    return h


def _frac_groups(frac):
    """Split a \\frac{n!}{m!(n-m)!} into (numerator, first denominator factorial, second)."""
    glyphs = list(frac)
    bar = max(glyphs, key=lambda g: g.width / max(g.height, 1e-3))
    num = [g for g in glyphs if g is not bar and g.get_y() > bar.get_y()]
    den = sorted([g for g in glyphs if g is not bar and g.get_y() < bar.get_y()], key=lambda g: g.get_x())
    return VGroup(*num), VGroup(*den[:2]), VGroup(*den[2:])


def _a_line():
    parts = [r"\binom{2}{0}", "f''g", "+", r"\binom{2}{1}", "f'g'", "+", r"\binom{2}{2}", "fg''"]
    a = MathTex(*parts, font_size=46, color=FG)
    for i in (0, 3, 6):
        a[i].set_color(YELLOW)
    _colour_fg(a[1], [0, 1, 2], [3])
    _colour_fg(a[4], [0, 1], [2, 3])
    _colour_fg(a[7], [0], [1, 2, 3])
    return a


def _b_line():
    b = MathTex("f''g", "+", "2", "f'g'", "+", "fg''", font_size=46, color=FG)
    _colour_fg(b[0], [0, 1, 2], [3])
    b[2].set_color(YELLOW)
    _colour_fg(b[3], [0, 1], [2, 3])
    _colour_fg(b[5], [0], [1, 2, 3])
    return b


def _ypp_line():
    """s3's y'' = f''g + 2f'g' + fg'' line, as on her board."""
    return load_scene("ch4_s3_pattern").board_lines(size=46).lines[1]


class Formula(NarratedScene):
    def construct(self):
        s3 = load_scene("ch4_s3_pattern")
        self.s3 = s3
        self.clip1(s3)
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ n choose m
    def clip1(self, s3):
        tri = s3.pascal_triangle(n_max=3, start=0)
        tri.scale_to_fit_width(4.4).move_to(LEFT * 3.6 + DOWN * 0.1)
        self.tri = tri
        rows = tri.rows

        formula = MathTex(r"\binom{n}{m}", "=", r"\frac{n!}{m!\,(n-m)!}", font_size=72, color=YELLOW)
        formula.move_to(RIGHT * 3.0 + UP * 1.75)
        self.formula = formula
        binom_big = MathTex(r"\binom{n}{m}", font_size=72, color=YELLOW).move_to(formula[0])
        name = T("n choose m", 36, color=YELLOW).next_to(formula[0], UP, buff=0.3)

        with self.say("c4.formula.1") as c:
            low = VGroup(*[r for k, r in enumerate(rows) if k >= 1])
            self.play(FadeIn(low, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("name")
            self.play(*appear(binom_big), run_time=1.0)
            c.wait_until("place")
            self.play(*appear(rows[0]), run_time=1.0)
            self.remove(low, *rows[0].get_family())
            self.add(tri)
            # row numbers, then places along row 3
            col_x = tri.get_left()[0] - 0.45
            rnums = VGroup(*[T(str(k), 28, color=DIM).move_to([col_x, rows[k].get_y(), 0]) for k in range(4)])
            pnums = VGroup(*[T(str(m), 28, color=DIM).move_to(
                [rows[3][m].get_x(), rows[3].get_bottom()[1] - 0.38, 0]) for m in range(4)])
            c.wait_until("rows")
            self.play(*appear(*rnums, lag=0.2), run_time=1.0)
            c.wait_until("places")
            self.play(*appear(*pnums, lag=0.2), run_time=1.0)
            settle(self, rnums)
            settle(self, pnums)
            self.rnums, self.pnums = rnums, pnums
            c.wait_until("row n place m")
            ring = Circle(radius=0.38, color=YELLOW).set_stroke(YELLOW, 3).move_to(rows[3][1])
            self.ring = ring
            self.play(GrowFromCenter(ring), FlashAround(pnums[1], run_time=1.2), run_time=1.2)
            c.wait_until("called")
            self.play(*appear(name), run_time=1.0)
            self.name = name
            # the factorial formula
            c.wait_until("fact")
            self.remove(binom_big)
            self.add(formula[0])
            self.play(*appear(formula[1], formula[2], shift=None, lag=0.3), run_time=1.2)
            settle(self, formula)
            num, den1, den2 = _frac_groups(formula[2])
            for cue, grp, nth in (("n factorial", num, 0), ("m factorial", den1, 0), ("factorial of n minus m", den2, 0)):
                c.wait_until(cue, nth=nth)
                rt = min(1.0, max(0.5, c.until("example") - 0.1)) if cue.startswith("factorial") else 1.0
                self.play(FlashAround(grp, run_time=rt), *recolor(list(grp), GOLD), run_time=rt)
            # example
            ex = MathTex(r"\binom{3}{1}", "=", r"\frac{3!}{1!\,2!}", "=", r"\frac{6}{2}", "=", "3",
                         font_size=54, color=GOLD)
            for i in (1, 3, 5):
                ex[i].set_color(FG)
            ex.next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
            self.ex = ex
            c.wait_until("example")
            self.play(*appear(ex[0], ex[1], ex[2], lag=0.3), run_time=1.2)
            c.wait_until("six")
            self.play(*appear(ex[3], ex[4], lag=0.2), run_time=0.9)
            c.wait_until("which is three")
            rt = max(1.0, min(1.6, c.until() - 0.05))
            self.play(*appear(ex[5], ex[6], lag=0.2), time_span(FlashAround(rows[3][1], run_time=1.0), rt - 1.0, rt),
                      run_time=rt)
            settle(self, ex)

    # ------------------------------------------------------------ C_n^m
    def clip2(self):
        f = self.formula
        cline = MathTex("C_n^m", "=", r"\binom{n}{m}", font_size=52, color=YELLOW)
        cline[1].set_color(FG)
        cline.next_to(self.ex, DOWN, buff=0.45).align_to(self.ex, LEFT)
        poll_a = T("Russia · Ukraine · Kazakhstan · China", 28, color=DIM)
        poll_b = T(" · France", 28, color=DIM)
        VGroup(poll_a, poll_b).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        VGroup(poll_a, poll_b).next_to(cline, DOWN, buff=0.4).set_x(cline.get_x() + 0.6)
        poll_b.next_to(poll_a, RIGHT, buff=0.1, aligned_edge=DOWN)
        self.cline, self.poll = cline, VGroup(poll_a, poll_b)
        with self.say("c4.formula.2", gap=1.2) as c:
            self.play(*appear(cline[2], cline[1], cline[0], shift=None, lag=0.4), run_time=1.5)
            settle(self, cline)
            c.wait_until(own_word=poll_a)
            self.play(*appear(poll_a), run_time=1.0)
            c.wait_until("france")
            self.play(*appear(poll_b), run_time=0.8)
            settle(self, self.poll)

    # ------------------------------------------------------------ Leibniz's formula
    def clip3(self):
        tri = self.s3.pascal_triangle(n_max=3, start=0)
        tri.scale_to_fit_width(2.4).move_to(RIGHT * 4.5 + DOWN * 2.35)
        title = T("Leibniz's formula", 40, color=FG).move_to(UP * 3.35)
        hero = _hero(68).move_to(UP * 1.0)
        card = leibniz_card(size=68).move_to(UP * 1.0)
        self.card = card
        with self.say("c4.formula.3") as c:
            sweep_clear(self, *appear(title, shift=None), FadeIn(hero, shift=0.2 * UP), run_time=2.2)
            self.title = title
            c.wait_until("nth derivative")
            self.play(FlashAround(hero[0], run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("sum over m")
            self.play(FlashAround(hero[2], run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("zero to n")
            rt = max(1.2, min(2.0, c.until("term") + 0.6))
            moves = [hero[i].animate.move_to(card.tex[j]) for i, j in ((1, 1), (2, 2), (3, 3), (4, 4), (6, 5))]
            self.play(*during([FadeOut(hero[0]), FadeOut(hero[5]), FadeOut(hero[7])], 0, 0.4),
                      *during(moves, 0.25, 0.8),
                      *during([FadeIn(card.lhs)], 0.55, 1), run_time=rt)
            self.remove(*hero.get_family(), *card.lhs.get_family())
            self.add(card)
            # underlines, one per piece of the summand
            base_y = min(card.binom.get_bottom()[1], card.fpart.get_bottom()[1], card.gpart.get_bottom()[1]) - 0.14

            def uline(mob, col):
                return Line([mob.get_left()[0], base_y, 0], [mob.get_right()[0], base_y, 0]).set_stroke(col, 5)

            ub, uf, ug = uline(card.binom, YELLOW), uline(card.fpart, BLUE), uline(card.gpart, PURPLE)
            for cue, ln in (("n choose m", ub), ("f differentiated", uf), ("g differentiated", ug)):
                c.wait_until(cue)
                self.play(GrowFromEdge(ln, LEFT), run_time=0.9)
            self.ub = ub
            # braces: m on g, the rest on f
            bf = span_brace(uf.get_left(), uf.get_right(), color=BLUE, buff=0.1)
            bg = span_brace(ug.get_left(), ug.get_right(), color=PURPLE, buff=0.1)
            lf = MathTex(r"n-m \text{ on } f", font_size=42, color=BLUE)
            lg = MathTex(r"m \text{ on } g", font_size=42, color=PURPLE)
            lf.next_to(bf, DOWN, buff=0.15).align_to(bf, RIGHT).shift(LEFT * 0.1)
            lg.next_to(bg, DOWN, buff=0.15).align_to(bg, LEFT).shift(RIGHT * 0.1)
            lg.align_to(lf, UP)
            c.wait_until("land on g")
            self.play(*during([FadeOut(ug)], 0, 0.4), *during([GrowFromCenter(bg)], 0.3, 0.8),
                      *during(appear(lg), 0.5, 1), run_time=1.2)
            c.wait_until("rest land on f")
            self.play(*during([FadeOut(uf)], 0, 0.4), *during([GrowFromCenter(bf)], 0.3, 0.8),
                      *during(appear(lf), 0.5, 1), run_time=1.2)
            self.braces = [bf, bg, lf, lg]
            # n choose m counts the ways
            slots = prime_slots(3).move_to(LEFT * 3.0 + DOWN * 2.4)
            tag = MathTex("n = 3,", r"\ m = 1", font_size=36, color=DIM).next_to(slots, UP, buff=0.35)
            c.wait_until("choose")
            self.play(*appear(*slots.slots, lag=0.2), *appear(tag, tri, shift=None), run_time=1.0)
            count_x = slots.get_right()[0] + 1.0
            counts = [MathTex(str(k), font_size=60, color=GOLD).move_to([count_x, slots.get_y(), 0]) for k in (1, 2, 3)]

            def way(k):
                anims = []
                for i in range(3):
                    col = PURPLE if i == k else BLUE
                    anims += recolor([slots.boxes[i], slots.primes[i]], col)
                return anims

            c.wait_until("pick")
            self.play(*way(0), *appear(counts[0], shift=None), FlashAround(slots.slots[0], run_time=0.9),
                      run_time=0.9)
            for k, cue in ((1, "derivatives"), (2, "go to g")):
                c.wait_until(cue)
                self.play(*way(k), *swap(counts[k - 1], counts[k]), FlashAround(slots.slots[k], run_time=0.7),
                          run_time=0.75)
            c.wait_until("that's where")
            ring = Circle(radius=0.24).set_stroke(GOLD, 3).move_to(tri.rows[3][1])
            arr = CurvedArrow(counts[2].get_bottom() + 0.1 * DOWN, ring.get_bottom() + 0.05 * DOWN,
                              angle=PI / 4, color=GOLD).set_stroke(width=3)
            rt = max(1.0, min(1.6, c.until() - 0.05))
            self.play(Create(arr), time_span(GrowFromCenter(ring), rt * 0.5, rt), run_time=rt)
            self.extra = [slots, tag, counts[2], ring, tri, arr]

    # ------------------------------------------------------------ n = 2 check
    def clip4(self):
        card = self.card
        a = _a_line().move_to(DOWN * 0.4)
        b = _b_line().move_to(DOWN * 1.75)
        n2 = MathTex("n = 2", font_size=40, color=GOLD).next_to(a, LEFT, buff=0.6)
        grp = VGroup(n2, a)
        dx = -grp.get_center()[0]
        n2.shift(RIGHT * dx)
        a.shift(RIGHT * dx)
        b.set_x(a.get_x())
        with self.say("c4.formula.4", gap=1.5) as c:
            self.play(*disappear(self.ub, *self.braces, *self.extra), card.animate.move_to(UP * 1.55), run_time=1.0)
            self.play(*appear(n2, shift=None), run_time=0.8)
            terms = [(("m equals zero", 0), [a[0], a[1]], [b[0]]),
                     (("m equals one", 0), [a[2], a[3], a[4]], [b[1], b[2], b[3]]),
                     (("m equals two", 0), [a[5], a[6], a[7]], [b[4], b[5]])]
            for (cue, nth), apart, bpart in terms:
                c.wait_until(cue, nth=nth)
                self.play(*appear(*apart, shift=None, lag=0.15), run_time=1.0)
                c.wait_until("gives" if cue == "m equals zero" else cue, nth=nth)
                self.play(*appear(*bpart, shift=0.2 * DOWN, lag=0.15), run_time=1.0)
            # the board's y'' line slides in under it
            ypp = _ypp_line()
            c.wait_until("match")
            self._place_ypp(ypp, b)
            self.play(FadeIn(ypp, shift=0.4 * UP), run_time=1.2)
            tick = check_mark(GREEN).next_to(VGroup(b, ypp), RIGHT, buff=0.5)
            bterms = [b[0], VGroup(b[2], b[3]), b[5]]
            for k in range(3):
                self.play(FlashAround(bterms[k], run_time=0.7), FlashAround(ypp.terms[k], run_time=0.7),
                          run_time=0.7)
            self.play(*appear(tick, shift=None), run_time=0.8)

    def _place_ypp(self, ypp, b):
        ypp.move_to(DOWN * 3.0)
        ypp.shift(RIGHT * (b[0].get_left()[0] - ypp.terms[0].get_left()[0]))
