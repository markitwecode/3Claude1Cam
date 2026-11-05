"""Chapter 4, scene 2: from the start to the swing (A from x(0), v(0)). Clips c4.start.1 – c4.start.6.

Exports (load_scene("ch4_s2_start")):
  O, U, F      plane origin, scene units per cm (1 unit = 1 cm), scene units per cm/s (push arrows)
  MOVE_M10     the move card text; move_m10() → the card
  amp_plane()  this scene's plane (DIM 1-cm grid, axes, Re / Im). .grid .axes .re .im
  spring_at(x_cm)   ch1's spring lying on the real axis, the block's centre at x cm
  start_picture(v0, x0=3, omega=3, origin=O, unit=U, push=F, weight=False)
               the frozen arrow A = x0 − i v0/ω (GOLD), its BLUE leg x0 along Re, its PINK leg
               −v0/ω, and the weight's GREEN push arrow (length v0·push, above the block). v0 a
               number or a ValueTracker (then every piece redraws itself). weight=True adds the
               spring. .gold .blue .pink .push (.spring)
  general_box() the boxed A = x0 − i v0/ω at its place in the right column. .line .box
  handover_shot()  the last frame (s3 opens on it): plane, spring at 3 cm, GOLD 3 − 4i, boxed
               general A, move card M10, legend (7 entries), the pin.
               .plane .spring .gold .general .card .legend .pin
"""
# style: 2
# handover: next
import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
spr = load_scene("ch1_s3_spring")

# ═══════════════════════════════ geometry (shared) ═══════════════════════════════
O = np.array([-2.4, 0.6, 0.0])      # plane origin
U = 0.38                             # scene units per cm
F = 0.07                             # scene units per cm/s (push and velocity arrows)
OMEGA = 3.0
X0 = 3.0
EXT = 5                              # grid ±5 cm
PUSH_Y = O[1] + spr.BLOCK_H / 2 + 0.3
Z_PLANE, Z_GOLD, Z_LEG, Z_MARK = -4, -2, -1.9, -1.7

MOVE_M10 = "Set t = 0: the turning factor becomes 1, so the start reads off A"


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def P(z, origin=O, unit=U):
    z = complex(z)
    return np.array(origin, dtype=float) + unit * np.array([z.real, z.imag, 0.0])


def _pin():
    """The chapter's pinned x(t) = Re[A e^{iωt}] (ch4_s1_hook owns it)."""
    return load_scene("ch4_s1_hook").amp_pin()


def move_m10():
    return kit.move_card(MOVE_M10)


def amp_plane(origin=O, unit=U, ext=EXT, labels=True):
    o = np.array(origin, dtype=float)
    r = range(-ext, ext + 1)
    grid = VGroup(*[Line(o + [x * unit, -ext * unit, 0], o + [x * unit, ext * unit, 0]) for x in r],
                  *[Line(o + [-ext * unit, y * unit, 0], o + [ext * unit, y * unit, 0]) for y in r])
    grid.set_stroke(DIM, 1, opacity=0.35)
    e = (ext + 0.4) * unit
    re_ax = Line(o + [-e, 0, 0], o + [e, 0, 0])
    im_ax = Line(o + [0, -e, 0], o + [0, e, 0])
    axes = VGroup(re_ax, im_ax).set_stroke(DIM, 2.5)
    g = VGroup(grid, axes)
    g.set_z_index(Z_PLANE)
    g.grid, g.axes, g.re, g.im = grid, axes, None, None
    if labels:
        re = T("Re", size=28, color=DIM).next_to(re_ax.get_end(), RIGHT, buff=0.12)
        im = T("Im", size=28, color=DIM).next_to(im_ax.get_end(), RIGHT, buff=0.12).shift(0.18 * DOWN)
        g.add(re, im)
        g.re, g.im = re, im
    return g


def spring_at(x_cm, origin=O, unit=U):
    """ch1's spring and block on the real axis; the block's centre at x_cm (cm)."""
    y = origin[1] - spr.BLOCK_H / 2
    sp = spr.spring_drawing(unit * x_cm / spr.SPRING_UNIT, y=y, zero=False)
    sp.shift((origin[0] - spr.SPRING_REST_X) * RIGHT)
    a = sp.table.get_start()
    sp.table.put_start_and_end_on(a, np.array([origin[0] + (EXT + 0.6) * unit, a[1], 0]))
    return sp


def _empty():
    return VMobject().set_points_as_corners([ORIGIN, ORIGIN + 1e-4 * RIGHT]).set_stroke(opacity=0)


def gold_arrow(z, origin=O, unit=U, grow=1.0):
    z = complex(z) * grow
    if abs(z) * unit < 0.06:
        return _empty()
    return ak.arrow_between(origin, P(z, origin, unit), GOLD, 6, Z_GOLD)


def _leg(a, b, color, origin=O, unit=U):
    if abs(complex(b) - complex(a)) * unit < 0.03:
        return _empty()
    ln = Line(P(a, origin, unit), P(b, origin, unit)).set_stroke(color, 6)
    ln.set_z_index(Z_LEG)
    return ln


def push_arrow(x_cm, v, origin=O, unit=U, push=F, op=1.0):
    y = origin[1] + spr.BLOCK_H / 2 + 0.3
    x = P(x_cm, origin, unit)[0]
    if abs(v) * push < 0.06 or op < 0.01:
        return _empty()
    a = ak.arrow_between([x, y, 0], [x + push * v, y, 0], GREEN, 5, 0)
    a.set_opacity(op)
    return a


def start_picture(v0, x0=X0, omega=OMEGA, origin=O, unit=U, push=F, weight=False):
    """The frozen arrow A = x0 − i v0/ω with its legs and the weight's push arrow (see docstring)."""
    live = hasattr(v0, "get_value")

    def dyn(build):
        return always_redraw(build) if live else build()

    def amp():
        return complex(x0, -_v(v0) / omega)
    gold = dyn(lambda: gold_arrow(amp(), origin, unit))
    blue = _leg(0, x0, BLUE, origin, unit)
    pink = dyn(lambda: _leg(x0, amp(), PINK, origin, unit))
    pa = dyn(lambda: push_arrow(x0, _v(v0), origin, unit, push))
    g = VGroup(blue, pink, gold, pa)
    g.gold, g.blue, g.pink, g.push, g.spring = gold, blue, pink, pa, None
    if weight:
        sp = spring_at(x0, origin, unit)
        g.add_to_back(sp)
        g.spring = sp
    return g


# ── the right column ────────────────────────────────────────────────────────────
COLX, ROW0, PITCH, COL_W = kit.COL_LEFT, 1.36, 0.72, kit.EDGE_X - kit.COL_LEFT
ROWS = [ROW0 - PITCH * i for i in range(7)]
SZ = 34


def _row(spec, i, size=SZ, x=COLX):
    m = MathTex(*[p for p, _ in spec], font_size=size)
    for k, (_, col) in enumerate(spec):
        m[k].set_color(col)
    if x + m.width > kit.EDGE_X:
        m.scale_to_fit_width(kit.EDGE_X - x)
    m.move_to([x, ROWS[i], 0], aligned_edge=LEFT)
    return m


def _lab(spec):
    """A DIM step label: "t:text", "m:tex", or ("text", "tex") mixed."""
    if isinstance(spec, tuple):
        a = kit.tag(spec[0])
        b = MathTex(spec[1], font_size=26, color=DIM)
        b.next_to(a, RIGHT, buff=0.1).align_to(a, DOWN).shift(0.02 * DOWN)
        m = VGroup(a, b)
    elif spec.startswith("m:"):
        m = MathTex(spec[2:], font_size=26, color=DIM)
    else:
        m = kit.tag(spec)
    m.key = spec
    return m


def _place(labs, row, idxs):
    """Each label centred over its '=' (glyph part idxs[k] of row), bottom 0.24 above the row's
    centre; pushed right so labels on one row never touch."""
    last = None
    for lab, k in zip(labs, idxs):
        lab.move_to([row[k].get_center()[0], 0, 0])
        lab.shift((row.get_center()[1] + 0.24 - lab.get_bottom()[1]) * UP)
        if last is not None and lab.get_left()[0] < last.get_right()[0] + 0.15:
            lab.shift((last.get_right()[0] + 0.15 - lab.get_left()[0]) * RIGHT)
        if lab.get_right()[0] > kit.EDGE_X:
            lab.shift((kit.EDGE_X - lab.get_right()[0]) * RIGHT)
        last = lab
    return labs


# Numbers (the start's 3 BLUE, ω's 3 FG, 12 GREEN, i and β PINK, A and e^{…} GOLD)
N0 = [("x", BLUE), ("(0)", FG), ("=", FG), (r"\mathrm{Re}\,", FG), ("A", GOLD), ("=", FG), ("3", BLUE)]
N1 = [(r"\dot x", GREEN), ("(t)", FG), ("=", FG), (r"\mathrm{Re}\,[", FG), ("3", FG), ("i", PINK),
      ("A", GOLD), (r"\,e^{3it}", GOLD), ("]", FG)]
N2 = [(r"\dot x", GREEN), ("(0)", FG), ("=", FG), (r"\mathrm{Re}\,(", FG), ("3", FG), ("i", PINK),
      ("A", GOLD), (")", FG), ("=", FG), ("12", GREEN)]
N3 = [("A", GOLD), ("=", FG), ("3", BLUE), ("+", FG), ("i", PINK), (r"\beta", PINK)]
N4 = [("3", FG), ("i", PINK), ("A", GOLD), ("=", FG), ("3", FG), ("i", PINK), ("(", FG), ("3", BLUE),
      ("+", FG), ("i", PINK), (r"\beta", PINK), (")", FG), ("=", FG), ("9", FG), ("i", PINK), ("+", FG),
      ("3", FG), ("i^2", PINK), (r"\beta", PINK), ("=", FG), ("9", FG), ("i", PINK), ("-", FG),
      ("3", FG), (r"\beta", PINK)]
N5A = [("-", FG), ("3", FG), (r"\beta", PINK), ("=", FG), ("12", GREEN)]
N5B = [(r"\Rightarrow", FG), (r"\beta", PINK), ("=", FG), ("-4", PINK)]
N6 = [("A", GOLD), ("=", FG), ("3", BLUE), ("-", PINK), ("4", PINK), ("i", PINK)]
# Letters
L0 = N0[:6] + [("x_0", BLUE)]
L1 = N1[:4] + [("i", PINK), (r"\omega", FG), ("A", GOLD), (r"\,e^{i\omega t}", GOLD), ("]", FG)]
L2 = N2[:4] + [("i", PINK), (r"\omega", FG), ("A", GOLD), (")", FG), ("=", FG), ("v_0", GREEN)]
L3 = [("A", GOLD), ("=", FG), ("x_0", BLUE), ("+", FG), ("i", PINK), (r"\beta", PINK)]
L4 = [("i", PINK), (r"\omega", FG), ("A", GOLD), ("=", FG), ("i", PINK), (r"\omega", FG), ("x_0", BLUE),
      ("+", FG), ("i^2", PINK), (r"\omega", FG), (r"\beta", PINK), ("=", FG), ("i", PINK), (r"\omega", FG),
      ("x_0", BLUE), ("-", FG), (r"\omega", FG), (r"\beta", PINK)]
L5A = [("-", FG), (r"\omega", FG), (r"\beta", PINK), ("=", FG), ("v_0", GREEN)]
L5B = [(r"\Rightarrow", FG), (r"\beta", PINK), ("=", FG), ("-", FG), ("v_0", GREEN), ("/", FG),
       (r"\omega", FG)]
GEN = [("A", GOLD), ("=", FG), ("x_0", BLUE), ("-", FG), ("i", PINK), (r"\,\dfrac{v_0}{\omega}", FG)]

NUM_LABS = [["m:e^0 = 1", "starts at 3"], ["differentiate: × iω"], ["m:e^0 = 1", "moving out at 12"],
            ["real part is 3"], ["substitute", "multiply out", "m:i^2 = -1"], ["real parts match"],
            ["divide by −3"]]
LET_LABS = [["m:e^0 = 1", ("starts at", "x_0")], ["differentiate: × iω"],
            ["m:e^0 = 1", ("moving out at", "v_0")], [("real part is", "x_0")],
            ["multiply out", "m:i^2 = -1"], ["real parts match"], ["divide by −ω"]]
NUM_EQ = [[2, 5], [2], [2, 8], [1], [3, 12, 19], [3], [0]]
LET_EQ = [[2, 5], [2], [2, 8], [1], [3, 11], [3], [0]]


def _r5b(spec, r5a, left_lab, lab_spec):
    """Row 5's second half (⇒ β = …) and its label, placed right of r5a so the two labels don't touch."""
    m = MathTex(*[p for p, _ in spec], font_size=SZ)
    for k, (_, col) in enumerate(spec):
        m[k].set_color(col)
    m.next_to(r5a, RIGHT, buff=0.6)
    m.shift((r5a[3].get_center()[1] - m[2].get_center()[1]) * UP)
    labs = _place([_lab(lab_spec)], m, [0])
    gap = left_lab.get_right()[0] + 0.2 - labs[0].get_left()[0]
    if gap > 0:
        m.shift(gap * RIGHT)
        labs[0].shift(gap * RIGHT)
    return m, labs


def general_line():
    m = _row(GEN, 6)
    frac = m[5]
    frac[0:2].set_color(GREEN)   # v_0 (then the bar and ω stay FG)
    m.shift(0.08 * DOWN)
    return m


def general_box():
    line = general_line()
    box = SurroundingRectangle(line, color=YELLOW, buff=0.14).set_stroke(YELLOW, 3)
    g = VGroup(line, box)
    g.line, g.box = line, box
    return g


# Legend
E_X = (r"x", BLUE, "displacement, cm")
E_XD = (r"\dot x", GREEN, "velocity")
E_W3 = (r"\omega = 3", FG, "per second")
E_A = (r"A", GOLD, "complex amplitude")
E_B = (r"\beta", PINK, "A's vertical part")
E_X0 = (r"x_0", BLUE, "starting position")
E_V0 = (r"v_0", GREEN, "starting velocity")
ENTRIES0 = [E_X, E_XD, E_W3, E_A]
ENTRIES = ENTRIES0 + [E_B, E_X0, E_V0]


def handover_shot():
    pl = amp_plane()
    sp = spring_at(X0)
    gold = gold_arrow(complex(3, -4))
    gen = general_box()
    card = move_m10()
    leg = kit.legend(ENTRIES)
    pin = _pin()
    g = VGroup(pl, sp, gold, gen, card, leg, pin)
    g.plane, g.spring, g.gold, g.general, g.card, g.legend, g.pin = pl, sp, gold, gen, card, leg, pin
    return g


def _bs(m):
    return set_backstroke(m, BG, 5)


class Start(NarratedScene):
    def construct(self):
        # trackers
        self.t = ValueTracker(0.0)        # time (s)
        self.v0 = ValueTracker(12.0)      # starting velocity (cm/s)
        self.xw = ValueTracker(0.0)       # the weight's start (cm), before the arrow is known
        self.push_op = ValueTracker(0.0)
        self.grow = ValueTracker(0.0)     # GOLD arrow 0 → 1
        self.drop_op = ValueTracker(0.0)
        self.rows, self.labs = [None] * 7, [[] for _ in range(7)]
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.finish()

    # ── live pieces ──
    def amp(self):
        return complex(X0, -self.v0.get_value() / OMEGA)

    def z(self):
        return self.amp() * cmath.exp(1j * OMEGA * self.t.get_value())

    def weight_x(self):
        return self.xw.get_value() + self.z().real - X0

    def build_live(self):
        self.spring = always_redraw(lambda: spring_at(self.weight_x()))
        self.gold = always_redraw(lambda: gold_arrow(self.z(), grow=self.grow.get_value()))
        self.push = always_redraw(lambda: push_arrow(self.weight_x(), self.v0.get_value(),
                                                     op=self.push_op.get_value()))

        def drop():
            tip, foot = P(self.z()), P(self.z().real)
            op = self.drop_op.get_value()
            if op < 0.01 or np.linalg.norm(tip - foot) < 0.06:
                return _empty()
            return DashedLine(tip, foot, dash_length=0.08).set_stroke(DIM, 2, opacity=op)
        self.drop = always_redraw(drop)

    # ── clip 1: the example's start ──
    def clip1(self):
        self.build_live()
        self.plane = amp_plane()
        self.pin = _pin()
        self.leg = kit.legend(ENTRIES0)
        self.corner = kit.corner_tag()
        self.faint = MathTex(r"x = 3\cos 3t + 4\sin 3t", font_size=30, color=DIM).move_to([-1.1, -2.65, 0])
        self.two = kit.tag("part two's swing").next_to(self.faint, DOWN, buff=0.16)
        x3 = P(X0)[0]
        self.tick = Line([x3, O[1] - spr.BLOCK_H / 2, 0], [x3, O[1] - spr.BLOCK_H / 2 - 0.16, 0]).set_stroke(BLUE, 4)
        self.cm3 = T("3 cm", size=28, color=BLUE)
        self.cm3.move_to([x3 + 0.18, O[1] - spr.BLOCK_H / 2 - 0.2, 0], aligned_edge=UL)
        self.lab12 = T("12 cm/s", size=28, color=GREEN)

        def stick(m):
            m.move_to([P(self.weight_x())[0] + 0.1, PUSH_Y + 0.3, 0], aligned_edge=LEFT)
        stick(self.lab12)
        self.lab12.add_updater(stick)
        self.aq = _bs(MathTex(r"A = ?", font_size=36, color=YELLOW).move_to(O + 0.62 * UP + 0.5 * LEFT))
        self.why_lab = kit.tag("start → A").next_to(self.aq, LEFT, buff=0.3)
        self.add(self.drop, self.gold, self.push)

        with self.say("c4.start.1") as c:
            self.play(FadeIn(self.plane), FadeIn(self.spring), FadeIn(self.pin), FadeIn(self.leg),  # early: legend and chapter tag shown with the board
                      FadeIn(self.corner), run_time=1.5)
            c.wait_until(own_word=self.two)
            self.play(*appear(self.faint, self.two, lag=0.3), run_time=1.2)
            c.wait_until("start")
            self.play(self.xw.animate.set_value(X0), FlashAround(self.leg.rows[2], color=FG, time_width=1.5),
                      run_time=min(1.6, c.until("starts three")))
            c.wait_until("starts three")
            self.play(*appear(self.tick, self.cm3, lag=0.2), run_time=min(1.0, c.until("push")))
            c.wait_until("push")
            self.play(self.push_op.animate.set_value(1.0), *appear(self.lab12), run_time=1.2)
            c.wait_until("ask")
            self.play(*appear(self.aq), run_time=1.0)
            c.wait_until(own_word=self.why_lab, cue="why")
            self.why1 = Line(self.lab12.get_left() + 0.05 * LEFT, self.aq.get_right() + 0.08 * RIGHT).set_stroke(DIM, 2)
            self.why2 = Line(self.cm3.get_left() + 0.05 * LEFT, self.aq.get_bottom() + 0.08 * DOWN).set_stroke(DIM, 2)
            self.play(Create(self.why1), Create(self.why2), *appear(self.why_lab), run_time=1.5)

    # ── clip 2: the move, t = 0 ──
    def clip2(self):
        self.card = move_m10()
        self.small = MathTex(r"e^{i\omega\cdot 0}", "=", r"e^{0}", "=", "1", font_size=30)
        self.small[0].set_color(GOLD)
        self.small[2].set_color(GOLD)
        self.small.move_to([kit.PIN_POS[0], 2.92, 0])
        self.tf = kit.tag("the turning factor", self.small, LEFT, buff=0.3)
        self.snap = _bs(kit.tag("t = 0: a snapshot").move_to([O[0] - EXT * U + 0.12, O[1] + EXT * U - 0.55, 0],
                                                             aligned_edge=LEFT))
        frame = Rectangle(width=2 * EXT * U + 0.3, height=2 * EXT * U + 0.3).move_to(O)
        with self.say("c4.start.2") as c:
            self.play(*appear(self.card, shift=None), run_time=1.2)
            c.wait_until("one")
            self.play(*disappear(self.why1, self.why2, self.why_lab), run_time=0.6)
            self.play(*appear(self.small, self.tf, lag=0.5), run_time=1.5)
            c.wait_until(own_word=self.snap)
            self.play(FlashAround(frame, color=DIM, stroke_width=6, time_width=1.5), *appear(self.snap),
                      run_time=1.2)
            c.wait_until("xzero")
            self.show_row(0, N0, NUM_LABS[0], NUM_EQ[0], c.until("line"))
            c.wait_until("line")
            x3 = P(X0)[0]
            self.vline = DashedLine([x3, O[1] + EXT * U, 0], [x3, O[1] - EXT * U, 0],
                                    dash_length=0.1).set_stroke(DIM, 2.5).set_z_index(Z_MARK)
            self.tipline = _bs(kit.tag("A's tip is on this line"))
            self.tipline.move_to([x3 - 0.15, O[1] - 1.75, 0], aligned_edge=RIGHT)
            self.play(Create(self.vline), *disappear(self.snap, self.tf), *appear(self.tipline),
                      run_time=min(1.5, c.until()))

    def show_row(self, i, spec, labs, eqs, budget, x=COLX, part=None):
        row = _row(spec, i, x=x) if part is None else part
        ls = _place([_lab(s) for s in labs], row, eqs)
        self.play(*appear(row, shift=None), *appear(*ls, shift=None, lag=0.35),
                  run_time=min(1.6, max(0.6, 0.7 * budget)))
        if part is None:
            self.rows[i] = row
            self.labs[i] = ls
        return row, ls

    def dim_row(self, i, op=0.4):
        mobs = [self.rows[i], *self.labs[i]]
        if i == 1:
            mobs.append(self.tag83)
        return set_alpha(mobs, op)

    # ── clip 3: the velocity ──
    def clip3(self):
        with self.say("c4.start.3") as c:
            row = _row(N1, 1)
            ls = _place([_lab(s) for s in NUM_LABS[1]], row, NUM_EQ[1])
            self.tag83 = kit.tag("(83) · notes p. 109", row, RIGHT, buff=0.3)
            self.play(*appear(row, *ls, self.tag83, shift=None, lag=0.4), run_time=1.6)
            self.rows[1], self.labs[1] = row, ls
            c.wait_until("vzero")
            self.show_row(2, N2, NUM_LABS[2], NUM_EQ[2], c.until("two_threes"))
            c.wait_until("one is omega")
            self.tag_w = kit.tag("this 3 is ω", self.rows[2], RIGHT, buff=0.35)
            self.play(FlashAround(self.rows[2][4], color=FG, time_width=1.5), *appear(self.tag_w), run_time=1.2)
            c.wait_until("where the weight starts")
            self.tag_s = kit.tag("where it starts", self.rows[0], RIGHT, buff=0.35)
            self.play(FlashAround(self.rows[0][6], color=BLUE, time_width=1.5), *appear(self.tag_s),
                      run_time=1.2)

    # ── clip 4: solve for β ──
    def clip4(self):
        with self.say("c4.start.4") as c:
            kit.legend_add(self, self.leg, E_B, run_time=1.2)  # early: the legend lists β as it enters
            self.rows[3] = _row(N3, 3)
            self.labs[3] = _place([_lab(s) for s in NUM_LABS[3]], self.rows[3], NUM_EQ[3])
            self.play(*appear(self.rows[3], *self.labs[3], shift=None, lag=0.35), *self.dim_row(0), run_time=1.4)
            c.wait_until("mult")
            self.rows[4] = _row(N4, 4)
            self.labs[4] = _place([_lab(s) for s in NUM_LABS[4]], self.rows[4], NUM_EQ[4])
            self.play(*appear(self.rows[4]), *self.dim_row(1), *disappear(self.tag_w, self.tag_s), run_time=1.2)
            self.play(*appear(*self.labs[4], shift=None, lag=0.6), run_time=min(2.4, c.until("match") - 0.2))
            c.wait_until("match")
            self.rows[5] = _row(N5A, 5)
            self.labs[5] = _place([_lab(s) for s in NUM_LABS[5]], self.rows[5], NUM_EQ[5])
            self.play(*appear(self.rows[5], *self.labs[5], shift=None, lag=0.35), *self.dim_row(2),
                      run_time=min(1.4, c.until("beta")))
            c.wait_until("beta")
            self.r5b, self.labs5b = _r5b(N5B, self.rows[5], self.labs[5][0], NUM_LABS[6][0])
            self.play(*appear(self.r5b, *self.labs5b, shift=None, lag=0.35), run_time=min(1.4, c.until("result")))
            c.wait_until("result")
            self.rows[6] = _row(N6, 6)
            self.box = SurroundingRectangle(self.rows[6], color=YELLOW, buff=0.14).set_stroke(YELLOW, 3)
            self.play(*appear(self.rows[6]), FadeIn(self.box), *self.dim_row(3), run_time=1.4)

    # ── clip 5: draw it, polar form, let it turn ──
    def clip5(self):
        A = complex(3, -4)
        self.blue = _leg(0, 3, BLUE)
        self.pink = _leg(3, A, PINK)
        self.alab = _bs(MathTex(r"A = 3 - 4i", font_size=30, color=GOLD))
        self.alab.move_to([-1.85, O[1] - EXT * U - 0.32, 0])          # below the grid, under the tip
        self.circle = Circle(radius=5 * U).move_to(O).set_stroke(DIM, 2.5).set_z_index(Z_PLANE)
        self.absA = _bs(MathTex(r"|A| = 5", font_size=30, color=GOLD))
        self.absA.move_to([O[0] - EXT * U - 0.2, -0.62, 0], aligned_edge=RIGHT)   # outside the circle, under arg A
        self.arc = Arc(radius=0.6, start_angle=0, angle=-math.atan2(4, 3), arc_center=O).set_stroke(YELLOW, 4)
        self.arc.set_z_index(Z_MARK)
        self.argl = _bs(MathTex(r"\arg A \approx -0.93\ \text{rad}\ (-53^\circ)", font_size=28, color=YELLOW))
        self.argl.move_to([-2.15, -0.08, 0], aligned_edge=RIGHT)
        self.cap = MathTex("x", r"\approx", "5", r"\cos(", "3", "t", "-", "0.93", ")", font_size=34)
        self.cap[0].set_color(BLUE)
        self.cap[2].set_color(GOLD)
        self.cap[7].set_color(YELLOW)
        self.cap.move_to([-1.1, -2.18, 0])
        self.tread = ak.t_readout(self.t)
        self.tread.move_to([O[0] - EXT * U - 0.2, O[1] + 1.5, 0], aligned_edge=RIGHT)   # left of the circle, above the wall
        self.whyq = _bs(T("why below?", size=28, color=YELLOW))
        self.whyq.move_to(P(A) + np.array([0.16, -0.15, 0]), aligned_edge=LEFT)
        with self.say("c4.start.5") as c:
            rt = min(3.0, c.until("polar") - 0.1)
            self.play(*disappear(self.aq, self.vline, self.tipline),
                      time_span(Create(self.blue), 0.3 * rt, 0.55 * rt),
                      time_span(Create(self.pink), 0.55 * rt, 0.78 * rt),
                      time_span(self.grow.animate.set_value(1.0), 0.72 * rt, rt),
                      run_time=rt)
            c.wait_until("polar")
            self.play(Create(self.circle), *appear(self.absA, self.alab, lag=0.4), run_time=1.5)
            c.wait_until("minus")
            self.play(Create(self.arc), *appear(self.argl), run_time=1.5)
            c.wait_until("swings")
            self.play(*appear(self.cap), FlashAround(self.faint, color=DIM, time_width=1.5), run_time=1.5)
            c.wait_until("run")
            turn = TAU / OMEGA
            self.play(self.t.animate.set_value(turn), self.drop_op.animate.set_value(1.0),
                      *during(self.push_op.animate.set_value(0.0), 0, 0.15),
                      *during(disappear(self.lab12), 0, 0.15), *during(appear(self.tread, shift=None), 0, 0.2),
                      run_time=min(turn, c.until("below")), rate_func=linear)
            self.t.set_value(0.0)
            c.wait_until("below")
            self.play(self.drop_op.animate.set_value(0.0), self.push_op.animate.set_value(1.0),
                      *appear(self.lab12), run_time=0.8)
            c.wait_until(own_word=self.whyq)
            self.play(*appear(self.whyq), run_time=1.0)
            c.wait_until("answer")
            self.play(self.drop_op.animate.set_value(1.0), run_time=0.6)
            self.play(self.t.animate.set_value(0.15), run_time=2.2)
            self.wait(0.8)
            self.play(self.t.animate.set_value(0.0), self.drop_op.animate.set_value(0.0), run_time=1.2)
            c.wait_until("its velocity arrow")
            vel = 3j * A                                   # 12 + 9i
            tip = P(A)
            vend = tip + F * np.array([vel.real, vel.imag, 0])
            self.green = ak.arrow_between(tip, vend, GREEN, 6, Z_GOLD)
            d = -np.array([A.real, A.imag, 0]) / abs(A)
            v = np.array([vel.real, vel.imag, 0]) / abs(vel)
            s = 0.17
            self.rang = VMobject().set_points_as_corners([tip + s * d, tip + s * (d + v), tip + s * v])
            self.rang.set_stroke(FG, 2.5).set_z_index(Z_MARK)
            self.vdrop = DashedLine(vend, [vend[0], PUSH_Y, 0], dash_length=0.08).set_stroke(DIM, 2)
            self.glab = _bs(MathTex(r"3iA = 12 + 9i", font_size=28, color=GREEN))
            self.glab.move_to([tip[0] + 0.18, O[1] - 4.5 * U, 0], aligned_edge=LEFT)   # in the grid cell row under the tip
            self.play(*during(disappear(self.whyq, self.cm3), 0, 0.4), *during([GrowArrow(self.green), FadeIn(self.rang)], 0.3, 1),
                      *during(appear(self.glab), 0.5, 1), run_time=1.6)
            self.play(Create(self.vdrop), FlashAround(self.lab12, color=GREEN, time_width=1.5),
                      run_time=min(1.4, c.until()))

    # ── clip 6: letters, the general form, the sweep ──
    def clip6(self):
        with self.say("c4.start.6") as c:
            kit.legend_add(self, self.leg, E_X0, E_V0, run_time=1.2,  # early: the legend lists x0, v0 as they enter
                           extra=disappear(self.circle, self.absA, self.argl, self.arc, self.cap, self.faint,
                                           self.two))
            # numbers → letters, row by row
            anims = []
            specs = [L0, L1, L2, L3, L4, L5A]
            for i, spec in enumerate(specs):
                new = _row(spec, i)
                nl = _place([_lab(s) for s in LET_LABS[i]], new, LET_EQ[i])
                a0, a1 = (0.11 * i, 0.11 * i + 0.35) if i < 5 else (0.8, 1.0)
                anims += during(edit(self.rows[i], new), a0, a1)
                anims += during(self.relabel(self.labs[i], nl), a0, a1)
                if i == 1:
                    anims += during(self.tag83.animate.next_to(new, RIGHT, buff=0.3), a0, a1)
                self.rows[i], self.labs[i] = new, nl
            new5b, nl5b = _r5b(L5B, self.rows[5], self.labs[5][0], LET_LABS[6][0])
            anims += during(edit(self.r5b, new5b), 0.8, 1.0)
            anims += during(disappear(*self.labs5b), 0, 0.2)
            anims += during(appear(*nl5b, shift=None), 0.85, 1.0)
            self.r5b, self.labs5b = new5b, nl5b
            self.play(*anims, run_time=min(3.4, c.until("general") - 0.1))  # early: step labels rewritten with their lines
            c.wait_until("general")
            self.gen = general_box()
            self.play(*edit(self.rows[6], self.gen.line), Transform(self.box, self.gen.box),
                      *disappear(self.green, self.rang, self.vdrop, self.glab, self.tread),
                      *[a for i in range(4) for a in self.dim_row(i)], run_time=1.6)
            self.remove(self.box)
            self.add(self.gen)
            c.wait_until("its real part")
            self.bl_words = kit.tag("where it starts")
            self.bl_sym = MathTex("x_0", font_size=32, color=BLUE)
            self.bl = VGroup(self.bl_sym, self.bl_words).arrange(RIGHT, buff=0.18)
            self.bl_words.align_to(self.bl_sym, DOWN)
            self.bl.move_to([P(0)[0] - 0.15, O[1] + 0.62, 0], aligned_edge=RIGHT)
            _bs(self.bl)
            c.wait_until(own_word=self.bl_words)
            self.play(*appear(self.bl),
                      FlashAround(self.gen.line[2], color=BLUE, time_width=1.5), run_time=1.3)
            self.pk_words = VGroup(kit.tag("how fast,"), kit.tag("÷ (−ω)")).arrange(DOWN, buff=0.08,
                                                                                   aligned_edge=LEFT)
            self.pk_sym = MathTex(r"-v_0/\omega", font_size=30, color=PINK)
            self.pk = VGroup(self.pk_sym, self.pk_words).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            _bs(self.pk)

            def follow(m):
                m.move_to([P(X0)[0] + 0.15, O[1] + U * self.amp().imag / 2 - 0.25, 0], aligned_edge=LEFT)
            follow(self.pk)
            c.wait_until(own_word=self.pk_words[0])
            self.play(*appear(self.pk), FlashAround(self.gen.line[5], color=PINK, time_width=1.5), run_time=1.3)
            # the knob
            c.wait_until("sweep")
            self.knob = self.build_knob()
            pink_live = always_redraw(lambda: _leg(X0, self.amp(), PINK))
            self.remove(self.pink)
            self.add(pink_live)
            self.pink = pink_live
            self.play(*disappear(self.lab12, self.alab), *during(appear(self.knob, shift=None), 0.3, 1),
                      run_time=1.0)
            self.play(self.v0.animate.set_value(24.0), run_time=min(3.0, c.until("push inward") - 0.1))
            c.wait_until("push inward")
            self.play(*disappear(self.pk), run_time=0.5)
            self.play(self.v0.animate.set_value(-12.0), run_time=min(3.3, c.until("beyond") - 0.1))
            c.wait_until("beyond")
            self.btag = kit.tag("beyond the notes", self.gen, RIGHT, buff=0.3)
            self.play(*appear(self.btag), FlashAround(self.gen, color=DIM, time_width=1.5), run_time=1.0)
            self.play(self.v0.animate.set_value(12.0), run_time=min(1.6, max(0.6, c.until() - 0.1)))

    def relabel(self, old, new):
        anims = []
        drops = len(old) > len([n for n in new if n.key in {o.key for o in old}])
        mv = (0.4, 1) if drops else (0, 1)
        olds = {o.key: o for o in old}
        used = set()
        for k, n in enumerate(new):
            o = olds.get(n.key)
            if o is not None and n.key not in used:
                used.add(n.key)
                anims += during(o.animate.move_to(n), *mv)
                new[k] = o
            else:
                cand = [x for x in old if x.key not in used and x.key not in {m.key for m in new}]
                if cand:
                    used.add(cand[0].key)
                    anims += during(disappear(cand[0]), 0, 0.45)
                    anims += during(appear(n, shift=None), 0.55, 1)
                else:
                    anims += appear(n, shift=None)
        for o in old:
            if o.key not in used:
                anims += during(disappear(o), 0, 0.4)
        return anims

    def build_knob(self):
        y1, y2 = -2.78, -3.25
        x_l = -2.55
        v_sym = MathTex("v_0", "=", font_size=32, color=GREEN)
        v_num = DecimalNumber(12.0, num_decimal_places=1, font_size=32, color=GREEN)
        v_unit = T("cm/s", size=26, color=GREEN)
        vr = VGroup(v_sym, v_num, v_unit)
        v_sym.move_to([x_l, y1, 0], aligned_edge=LEFT)

        def upd_v(m):
            m[1].set_value(self.v0.get_value())
            m[1].next_to(m[0], RIGHT, buff=0.12).align_to(m[0], DOWN)
            m[2].next_to(m[1], RIGHT, buff=0.12).align_to(m[0], DOWN)
        upd_v(vr)
        vr.add_updater(upd_v)
        # slider
        tx0, tx1 = -0.45, 0.75
        track = Line([tx0, y2, 0], [tx1, y2, 0]).set_stroke(DIM, 3)

        def sx(v):
            return tx0 + (v + 12) / 36 * (tx1 - tx0)
        ticks = VGroup(*[Line([sx(v), y2 - 0.08, 0], [sx(v), y2 + 0.08, 0]).set_stroke(DIM, 2) for v in (-12, 0, 12, 24)])
        dot = always_redraw(lambda: Dot([sx(self.v0.get_value()), y2, 0], radius=0.08, color=GREEN))
        # A readout
        a_sym = MathTex("A", "=", "3", font_size=32)
        a_sym[0].set_color(GOLD)
        a_sym[2].set_color(BLUE)
        a_sym.move_to([x_l, y2, 0], aligned_edge=LEFT)
        minus = MathTex("-", font_size=32, color=PINK)
        plus = MathTex("+", font_size=32, color=PINK)
        num = DecimalNumber(4.0, num_decimal_places=1, font_size=32, color=PINK)
        ii = MathTex("i", font_size=32, color=PINK)
        ar = VGroup(a_sym, minus, plus, num, ii)

        def upd_a(m):
            b = -self.v0.get_value() / OMEGA
            m[3].set_value(abs(b))
            m[1].next_to(m[0], RIGHT, buff=0.14)
            m[1].move_to([m[1].get_center()[0], m[0][1].get_center()[1], 0])
            m[2].move_to(m[1])
            m[1].set_opacity(1.0 if b < 0 else 0.0)
            m[2].set_opacity(0.0 if b < 0 else 1.0)
            m[3].next_to(m[1], RIGHT, buff=0.14).align_to(m[0][2], DOWN)
            m[4].next_to(m[3], RIGHT, buff=0.06).align_to(m[0][2], DOWN)
        upd_a(ar)
        ar.add_updater(upd_a)
        g = VGroup(vr, track, ticks, dot, ar)
        return g

    def finish(self):
        leave = [m for i in range(6) for m in [self.rows[i], *self.labs[i]]]
        self.wait(2.4)
        leave += [self.r5b, *self.labs5b, self.tag83, self.knob, self.blue, self.pink, self.bl, self.tick,
                  self.corner, self.small, self.btag]
        self.play(*disappear(*leave), self.push_op.animate.set_value(0.0), run_time=1.2)
        shot = handover_shot()
        self.clear()
        self.add(*shot)
        self.wait(1.2)
