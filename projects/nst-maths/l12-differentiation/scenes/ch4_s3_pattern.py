"""Chapter 4, scene 3: the pattern on the board, Pascal's triangle. Clips c4.pattern.1 – c4.pattern.4."""
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


# ======================= exported helpers (s4, s5, s7, recap, ch5, ch7) =======================

PASCAL_SIZE = 44     # default font size of the entries
PASCAL_PITCH = 0.8   # horizontal distance between neighbouring entries of a row (unscaled)
PASCAL_DY = 0.7      # vertical distance between rows (unscaled)


def _binom_row(n):
    row = [1]
    for m in range(n):
        row.append(row[-1] * (n - m) // (m + 1))
    return row


def _pitch_for(n, size):
    """PASCAL_PITCH, widened only if row n's widest entry would not fit (row 10 and beyond)."""
    widest = max(len(str(v)) for v in _binom_row(n))
    return max(PASCAL_PITCH, widest * 0.0125 * size + 0.3)


def pascal_row(n, size=PASCAL_SIZE, pitch=None, like=None):
    """Row n of Pascal's triangle: VGroup of YELLOW MathTex entries, `[m]` is place m.
    Unscaled placement: apex (row 0) at ORIGIN, row n's entries at y = -n*PASCAL_DY,
    x = (m - n/2) * pitch (pitch defaults to PASCAL_PITCH, widened only for rows with 3-digit entries).
    `like=tri` (a pascal_triangle, possibly moved/scaled): the row is built in that triangle's frame
    (same size, pitch, position, scale), ready to add as row n, e.g. s4's row 0 or ch5 s4's row 4."""
    if like is not None:
        ref_k = next(k for k, r in enumerate(like.rows) if r is not None and len(r) >= 2)
        ref = like.rows[ref_k]
        s = (ref[1].get_x() - ref[0].get_x()) / like.pitch
        row = pascal_row(n, size=like.size, pitch=like.pitch)
        row.scale(s, about_point=ORIGIN)
        apex = np.array([(ref[0].get_x() + ref[-1].get_x()) / 2, ref[0].get_y() + ref_k * PASCAL_DY * s, 0])
        row.shift(apex)
        return row
    if pitch is None:
        pitch = _pitch_for(n, size)
    row = VGroup()
    for m, v in enumerate(_binom_row(n)):
        e = MathTex(str(v), font_size=size, color=YELLOW)
        e.move_to([(m - n / 2) * pitch, -n * PASCAL_DY, 0])
        row.add(e)
    return row


def pascal_triangle(n_max=3, start=0, size=PASCAL_SIZE):
    """Rows start..n_max of Pascal's triangle, YELLOW MathTex at one fixed pitch.
    `.rows[k][m]`: row k, place m (`.rows[k]` is None for k < start). `.pitch`, `.size`: unscaled.
    Built with the apex (row 0's place, even if row 0 is not drawn) at ORIGIN, so the group's
    centre depends on start/n_max; position it by a row (e.g. `tri.rows[1]`) or move the whole group.
    Add a row later with `pascal_row(k, like=tri)` and `tri.rows[k] = row; tri.add(row)`."""
    pitch = _pitch_for(n_max, size)
    tri = VGroup()
    tri.rows = [None] * (n_max + 1)
    for k in range(start, n_max + 1):
        r = pascal_row(k, size=size, pitch=pitch)
        tri.rows[k] = r
        tri.add(r)
    tri.pitch = pitch
    tri.size = size
    return tri


BOARD_SIZE = 44
BOARD_LINE_GAP = 0.85   # gap between lines in board_lines()


def _board_line(lhs, terms, size=BOARD_SIZE):
    """terms: list of (coef or None, nf, ng)."""
    parts, idx = [lhs, "="], []
    for i, (c, nf, ng) in enumerate(terms):
        if i:
            parts.append("+")
        start = len(parts)
        if c is not None:
            parts.append(str(c))
        parts += ["f" + "'" * nf, "g" + "'" * ng]
        idx.append((start, c is not None))
    line = MathTex(*parts, font_size=size, color=FG)
    line.lhs = line[0]
    line.eq = line[1]
    line.terms, line.coefs, line.plus = [], [], []
    for start, has_c in idx:
        if has_c:
            co, f, g = line[start], line[start + 1], line[start + 2]
            co.set_color(YELLOW)
            line.terms.append(VGroup(co, f, g))
            line.coefs.append(co)
        else:
            f, g = line[start], line[start + 1]
            line.terms.append(VGroup(f, g))
            line.coefs.append(None)
        f.set_color(BLUE)
        g.set_color(PURPLE)
    line.plus = [p for p in line if p.get_tex_string() == "+"]
    return line


def y1_line(size=BOARD_SIZE):
    return _board_line("y'", [(None, 1, 0), (None, 0, 1)], size)


def y2_line(size=BOARD_SIZE):
    return _board_line("y''", [(None, 2, 0), (2, 1, 1), (None, 0, 2)], size)


def y3_line(size=BOARD_SIZE):
    return _board_line("y'''", [(None, 3, 0), (3, 2, 1), (3, 1, 2), (None, 0, 3)], size)


def board_lines(size=BOARD_SIZE, gap=BOARD_LINE_GAP):
    """Her board's three lines, stacked with their '=' signs aligned, centred at ORIGIN:
      y' = f'g + fg'     y'' = f''g + 2f'g' + fg''     y''' = f'''g + 3f''g' + 3f'g'' + fg'''
    f-parts BLUE, g-parts PURPLE, coefficients YELLOW, y, =, + FG.
    `.lines[i]` (i = 0, 1, 2 for y', y'', y''') is a MathTex with `.lhs`, `.eq`, `.terms` (one VGroup per
    term: (coef, f, g) or (f, g)), `.coefs` (the YELLOW coefficient per term, None where it is 1), `.plus`."""
    lines = [y1_line(size), y2_line(size), y3_line(size)]
    g = VGroup(*lines).arrange(DOWN, buff=gap)
    for ln in lines[1:]:
        ln.shift((lines[0].eq.get_x() - ln.eq.get_x()) * RIGHT)
    g.move_to(ORIGIN)
    g.lines = lines
    return g


# ============================== scene ==============================

EQ_X = -5.3          # x of the '=' in the board lines
LINE_Y = (2.0, 0.3, -1.1)
TRI_X = 2.0          # triangle's centre line
TRI_Y1 = 1.75        # y of the triangle's row 1


def _term(nf, ng, size=BOARD_SIZE, coef=None):
    parts = ([str(coef)] if coef else []) + ["f" + "'" * nf, "g" + "'" * ng]
    t = MathTex(*parts, font_size=size)
    if coef:
        t[0].set_color(YELLOW)
    t[-2].set_color(BLUE)
    t[-1].set_color(PURPLE)
    return t


def _branch(parent, child, color):
    """ch4_s1_hook's doubling_tree edge: stroke 4, parent bottom to child top."""
    return Line(parent.get_bottom() + DOWN * 0.08, child.get_top() + UP * 0.08, color=color, stroke_width=4)


def _ones_over(line):
    """Small YELLOW coefficient (1 where none is written) over each term of a line."""
    ones = []
    for t, c in zip(line.terms, line.coefs):
        o = MathTex(c.get_tex_string() if c is not None else "1", font_size=30, color=YELLOW)
        o.next_to(t, UP, buff=0.22)
        ones.append(o)
    return ones


def _row_sources(line, ones):
    return ones


class PatternScene(NarratedScene):
    def construct(self):
        self.build()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def build(self):
        self.header = MathTex(r"\text{If }", "y(x)", "=", "f(x)", r"\,g(x)", r"\text{, find }",
                              r"\frac{d^n y}{dx^n}", font_size=40, color=FG)
        self.header[3].set_color(BLUE)
        self.header[4].set_color(PURPLE)
        self.header.move_to([0, 3.05, 0])
        self.lines = [y1_line(), y2_line(), y3_line()]
        for ln, y in zip(self.lines, LINE_Y):
            ln.shift([EQ_X - ln.eq.get_x(), y - ln.eq.get_y(), 0])
        self.tri = pascal_triangle(3, start=1)
        self.tri.shift([TRI_X, TRI_Y1 + PASCAL_DY, 0])

    def fly_row(self, c, line, ones, k, arc=None, cue=None):
        """The small coefficients over the line travel (rightmost first) into the triangle's row k."""
        pairs = list(zip(ones, self.tri.rows[k]))[::-1]
        n = len(pairs)
        anims = []
        for i, (src, dst) in enumerate(pairs):
            a0 = 0.5 * i / max(n - 1, 1)
            anims += during([ReplacementTransform(src, dst, path_arc=arc or 0.0)], a0, a0 + 0.5)
        self.play(*anims, run_time=min(2.0, c.until(cue)))
        ones.clear()

    # ---------------------------------------------------------------- clip 1
    def clip1(self):
        with self.say("c4.pattern.1") as c:
            self.play(*appear(self.header), run_time=1.5)   # early: the board's heading, read as it lands
            c.wait_until("Call the product")
            self.play(FlashUnder(VGroup(*self.header[1:5]), run_time=2, time_width=1.5))
            c.wait_until("first")
            y1 = self.lines[0]
            self.play(*appear(y1, shift=None), run_time=1.5)
            c.wait_until("F prime times G")
            self.play(*flash([y1.terms[0], y1.terms[1]]), run_time=2.0)
            c.wait_until("ones")
            self.ones1 = _ones_over(y1)
            self.play(*appear(*[o for o in self.ones1 if o], lag=0.3), run_time=0.9)
            self.fly_row(c, y1, self.ones1, 1, arc=0.4)

    # ---------------------------------------------------------------- clip 2
    def clip2(self):
        y1, y2 = self.lines[0], self.lines[1]
        with self.say("c4.pattern.2") as c:
            c.wait_until("Each piece")
            self.play(*flash([y1.terms[0], y1.terms[1]]), run_time=2.0)
            # leaves of the one-level tree, on y'' 's row
            cx = (y1.terms[0].get_x() + y1.terms[1].get_x()) / 2 + 0.3
            ly = LINE_Y[1]
            leaves = [_term(2, 0), _term(1, 1), _term(1, 1), _term(0, 2)]
            for t, dx in zip(leaves, (-2.5, -0.85, 0.85, 2.5)):
                t.move_to([cx + dx, ly, 0])
            br = [_branch(y1.terms[0], leaves[0], BLUE), _branch(y1.terms[0], leaves[1], PURPLE),
                  _branch(y1.terms[1], leaves[2], BLUE), _branch(y1.terms[1], leaves[3], PURPLE)]

            c.wait_until("split")
            self.play(*during([Create(br[0]), Create(br[1])], 0, 0.55),
                      *during(appear(leaves[0], leaves[1], shift=None, lag=0.3), 0.45, 1), run_time=1.8)
            c.wait_until("split2")
            self.play(*during([Create(br[2]), Create(br[3])], 0, 0.55),
                      *during(appear(leaves[2], leaves[3], shift=None, lag=0.3), 0.45, 1), run_time=1.8)

            c.wait_until("merge")
            mid = _term(1, 1, coef=2).move_to([cx, ly, 0])
            self.play(*during([leaves[1].animate.shift(0.3 * RIGHT).set_opacity(0),
                               leaves[2].animate.shift(0.3 * LEFT).set_opacity(0)], 0, 0.5),
                      *during(appear(mid, shift=None), 0.5, 1), run_time=1.6)
            self.remove(leaves[1], leaves[2])

            c.wait_until("twos")
            # settle: the three leaves glide into the y'' line, its = and + signs arrive
            outs = [leaves[0], mid, leaves[3]]
            rest = [y2.lhs, y2.eq, *y2.plus]
            self.ones2 = _ones_over(y2)
            moves = [m.animate.move_to(t) for m, t in zip(outs, y2.terms)]
            self.play(*during([FadeOut(b) for b in br], 0, 0.4),
                      *during(moves, 0.2, 0.75),
                      *during(appear(*rest, shift=None), 0.7, 1),
                      run_time=1.4)
            self.remove(*outs)
            self.add(y2)
            self.play(*appear(*[o for o in self.ones2 if o], shift=None, lag=0.2), run_time=0.6)
            self.fly_row(c, y2, self.ones2, 2, arc=-0.8)

    # ---------------------------------------------------------------- clip 3
    def clip3(self):
        y3 = self.lines[2]
        with self.say("c4.pattern.3") as c:
            self.ones3 = _ones_over(y3)
            self.play(*appear(y3, shift=None), run_time=1.5)
            self.play(*appear(*[o for o in self.ones3 if o], shift=None, lag=0.2), run_time=0.6)
            self.fly_row(c, y3, self.ones3, 3, arc=-0.5, cue="what")
            c.wait_until("what")
            q = MathTex("?", font_size=52, color=YELLOW).next_to(self.tri, UP, buff=0.15)
            self.play(*appear(q, shift=None), run_time=1.0)
            c.wait_until("pascal")
            self.frame = SurroundingRectangle(self.tri, color=YELLOW, buff=0.3, stroke_width=4)
            self.play(*during(disappear(q), 0, 0.4), *during([GrowFromCenter(self.frame)], 0.3, 1), run_time=1.6)
            self.plabel = T("Pascal's triangle", size=34, color=YELLOW).next_to(self.frame, DOWN, buff=0.22)
            c.wait_until(own_word=self.plabel)
            self.play(*appear(self.plabel), run_time=1.0)
            c.wait_until("binom")
            self.binoms = self._binoms()
            self.play(*appear(*self.binoms, lag=0.5), run_time=2.2)

    def _binoms(self):
        rows = [
            ["(a+b)^1", "=", "a", "+", "b"],
            ["(a+b)^2", "=", "a^2", "+", "2", "ab", "+", "b^2"],
            ["(a+b)^3", "=", "a^3", "+", "3", "a^2b", "+", "3", "ab^2", "+", "b^3"],
        ]
        ms = []
        for r in rows:
            m = MathTex(*r, font_size=40, color=FG)
            for part in m:
                if part.get_tex_string() in ("2", "3"):
                    part.set_color(YELLOW)
            ms.append(m)
        g = VGroup(*ms).arrange(DOWN, buff=0.3)
        for m in ms[1:]:
            m.shift((ms[0][1].get_x() - m[1].get_x()) * RIGHT)
        g.move_to([3.6, -2.55, 0])
        return ms

    # ---------------------------------------------------------------- clip 4
    def clip4(self):
        with self.say("c4.pattern.4", gap=3.5) as c:
            board = [self.header, *self.lines, *[o for o in self.ones1 + self.ones2 + self.ones3 if o]]
            self.play(*set_alpha(board, DIMMED), run_time=1.2)

            # left splitting: f'g -> f''g, f'g'
            ly0, ly1 = -2.0, -3.3
            root_l = _term(1, 0).move_to([-3.4, ly0, 0])
            lA, lB = _term(2, 0).move_to([-4.7, ly1, 0]), _term(1, 1).move_to([-2.1, ly1, 0])
            aL1 = Arrow(root_l.get_bottom(), lA.get_top(), buff=0.1, color=BLUE, stroke_width=4)
            aL2 = Arrow(root_l.get_bottom(), lB.get_top(), buff=0.1, color=PURPLE, stroke_width=4)
            c.wait_until("Each time you differentiate")
            self.play(*appear(root_l, shift=None), run_time=0.8)
            self.play(*during([GrowArrow(aL1), GrowArrow(aL2)], 0, 0.55),
                      *during(appear(lA, lB, shift=None, lag=0.3), 0.45, 1), run_time=1.8)

            # right splitting: ab (a+b) -> a^2b, ab^2
            root_r = MathTex("ab", r"\cdot", "(a+b)", font_size=BOARD_SIZE, color=FG).move_to([2.9, ly0, 0])
            rA = MathTex("a^2b", font_size=BOARD_SIZE, color=FG).move_to([root_r.get_x() - 1.3, ly1, 0])
            rB = MathTex("ab^2", font_size=BOARD_SIZE, color=FG).move_to([root_r.get_x() + 1.3, ly1, 0])
            aR1 = Arrow(root_r.get_bottom(), rA.get_top(), buff=0.1, color=BLUE, stroke_width=4)
            aR2 = Arrow(root_r.get_bottom(), rB.get_top(), buff=0.1, color=PURPLE, stroke_width=4)
            c.wait_until("binom2")
            self.play(*during(disappear(*self.binoms), 0, 0.45),
                      *during(appear(root_r, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("Each term splits")
            self.play(*during([GrowArrow(aR1), GrowArrow(aR2)], 0, 0.55),
                      *during(appear(rA, rB, shift=None, lag=0.3), 0.45, 1), run_time=1.8)

            c.wait_until("count")
            left = VGroup(root_l, aL1, aL2, lA, lB)
            right = VGroup(root_r, aR1, aR2, rA, rB)
            self.play(FlashAround(left, run_time=2, time_width=1.5, buff=0.25),
                      FlashAround(right, run_time=2, time_width=1.5, buff=0.25))

            c.wait_until("total")
            sums = []
            for k, txt in ((1, "1+1=2"), (2, "1+2+1=4"), (3, "1+3+3+1=8")):
                s = MathTex(txt, font_size=36, color=GOLD)
                s.move_to(self.tri.rows[k]).align_to(self.frame.get_right() + 0.35 * RIGHT, LEFT)
                sums.append(s)
            self.play(*appear(*sums, shift=None, lag=0.6), run_time=2.4)

            c.wait_until("ten")
            vals = _binom_row(10)
            row10 = MathTex(*[str(v) + (r",\;" if i < 10 else "") for i, v in enumerate(vals)],
                            font_size=38, color=YELLOW)
            tot = MathTex("=", "1024", font_size=44)
            tot[0].set_color(FG)
            tot[1].set_color(GOLD)
            grp = VGroup(row10, tot).arrange(RIGHT, buff=0.35).move_to([-0.2, -2.65, 0])
            tot.align_to(row10, UP)
            self.play(*during(disappear(left, right), 0, 0.45),
                      *during(appear(row10, shift=None), 0.5, 1), run_time=1.6)
            self.play(*appear(tot, shift=None), run_time=min(1.0, c.until(floor=0.5)))
