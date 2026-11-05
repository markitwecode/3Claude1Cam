"""Chapter 4, scene 4: F19, the question and the move (hint 1, the show-that, T4.3). Clips c4.sheet.1 – c4.sheet.4.

Handover → ch4_s5_events. Exports (load_scene("ch4_s4_f19")):
  handover_shot()   the last frame: f19_plane(), gold_arrow() + gold_label() (24 − 7i), inset_spring(),
                    x_line() (X = (24 − 7i) e^{3it}) at column line 0, legend(ENTRIES_END), amp_pin(),
                    strip() (DIM "F19 · Examples Sheet I" + x = 7 + 24 cos 3t + 7 sin 3t, top-left).
  F19_O             the plane's origin (scene point); F19_U scene units per unit (per cm): 0.2.
  f19_point(z)      scene point of the complex number z on that plane.
  f19_plane()       DIM grid every 4 units (Re 0..24, Im -8..4), axes Re -2..26, Im -9..5, Re/Im labels.
  ENTRIES_END       legend entries at the end (x, k, m, ω = 3, X).
"""
# style: 2
# handover: next
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
s1 = load_scene("ch4_s1_hook")

MOVE_M8 = "Add the arrows, not the waves: flat a and downward −ib make one arrow."


def move_m8():
    try:
        ch3 = load_scene("ch3_s4_add")
        if hasattr(ch3, "move_m8"):
            return ch3.move_m8()
    except Exception:
        pass
    return kit.move_card(MOVE_M8)


# ── geometry ─────────────────────────────────────────────────────────────────────
F19_O = np.array([-5.0, 1.2, 0])
F19_U = 0.2
SPRING_POS = np.array([-2.2, 0.0, 0])     # big spring: weight centre at x = 7
INSET_POS = np.array([-6.2, -0.25, 0])
INSET_S = 0.5
RULER_X = SPRING_POS[0] - 0.95
ARROW_X = SPRING_POS[0] + 0.72            # force arrows, right of the weight

# column rows (kit column indices, fractional)
I_HINT, I_MATCH, I_X, I_EUL, I_EXP1, I_EXP2, I_RE = -0.6, 0.0, 1.25, 2.25, 3.25, 4.25, 5.25
I_RE_UP = 2.25

E_X = (r"x", BLUE, "position, from the origin")
E_K = (r"k", FG, "stiffness")
E_M = (r"m", FG, "mass")
E_W = (r"\omega = 3", FG, "turning rate")
E_XX = (r"X", GOLD, "turning arrow")
ENTRIES0 = [E_X, E_K, E_M, E_W]
ENTRIES_END = ENTRIES0 + [E_XX]


def f19_point(z):
    z = complex(z)
    return F19_O + F19_U * np.array([z.real, z.imag, 0.0])


def f19_plane():
    u = F19_U
    o = F19_O
    grid = VGroup(*[Line(o + [x * u, -8 * u, 0], o + [x * u, 4 * u, 0]) for x in range(4, 25, 4)],
                  *[Line(o + [0, y * u, 0], o + [24 * u, y * u, 0]) for y in (-8, -4, 4)])
    grid.set_stroke(DIM, 1, opacity=0.35)
    re_ax = Line(o + [-2 * u, 0, 0], o + [25.5 * u, 0, 0])
    im_ax = Line(o + [0, -9 * u, 0], o + [0, 5 * u, 0])
    axes = VGroup(re_ax, im_ax).set_stroke(DIM, 2.5)
    re = T("Re", size=26, color=DIM).next_to(re_ax.get_end(), DR, buff=0.08)
    im = T("Im", size=26, color=DIM).next_to(im_ax.get_end(), RIGHT, buff=0.15).shift(0.12 * DOWN)
    g = VGroup(grid, axes, re, im)
    g.set_z_index(-4)
    return g


def gold_arrow():
    return ak.arrow_between(F19_O, f19_point(24 - 7j), GOLD, width=6)


def gold_label():
    mid = (F19_O + f19_point(24 - 7j)) / 2
    n = np.array([-7.0, -24.0, 0]) / 25
    lab = MathTex(r"24 - 7i", font_size=34, color=GOLD)
    lab.move_to(mid + 0.42 * n)
    return lab


def inset_spring():
    return s1.hanging_spring(7, pos=INSET_POS, scale=INSET_S)


def x_line():
    m = MathTex("X", "=", "(", "24", "-", "7i", ")", r"\,e^{3it}", font_size=kit.COL_SIZE)
    m[0].set_color(GOLD)
    m[3].set_color(BLUE)
    m[5].set_color(PINK)
    m[7].set_color(GOLD)
    return m


def strip_formula(size=26):
    m = MathTex("x", "=", "7", "+", "24", r"\cos 3t", "+", "7", r"\sin 3t", font_size=size)
    m[0].set_color(BLUE)
    m[2].set_color(YELLOW)
    m[4].set_color(BLUE)
    m[7].set_color(BLUE)
    return m


def strip_tag():
    return kit.tag("F19 · Examples Sheet I").move_to(kit.TAG_TL + 0.12 * UP, aligned_edge=UL)


def strip():
    tg = strip_tag()
    f = strip_formula().next_to(tg, DOWN, buff=0.14, aligned_edge=LEFT)
    return VGroup(tg, f)


def handover_shot():
    x = x_line()
    col(x, 0)
    return VGroup(f19_plane(), gold_arrow(), gold_label(), inset_spring(), x,
                  kit.legend(ENTRIES_END), s1.amp_pin(), strip())


# ── the question card ────────────────────────────────────────────────────────────
QUESTION = (
    "Show that the displacement from the centre of motion (at $x = 7$) in the simple harmonic "
    "motion $x = 7 + 24\\cos 3t + 7\\sin 3t$ is given by the real part of the complex quantity "
    "$X = (24 - 7i)e^{3it}$ and hence obtain the [amplitude] of the motion. By writing $X$ in the "
    "form $Ae^{i\\phi}$, where $A$ and $\\phi$ are real, find the time of the [first two passages "
    "through the centre] after $t = 0$ and the [distances of the stationary points] of the motion "
    "[from the origin].")


def _tokens(s):
    toks, buf, b_sp, b_g = [], "", False, None
    pend, grp, gc, i = False, None, 0, 0

    def flush():
        nonlocal buf
        if buf:
            toks.append(("t", buf, b_sp, b_g))
            buf = ""

    while i < len(s):
        ch = s[i]
        if ch == " ":
            flush()
            pend = True
        elif ch == "[":
            flush()
            grp, gc = gc, gc + 1
        elif ch == "]":
            flush()
            grp = None
        elif ch == "$":
            flush()
            j = s.index("$", i + 1)
            toks.append(("m", s[i + 1:j], pend, grp))
            pend = False
            i = j
        else:
            if not buf:
                b_sp, b_g, pend = pend, grp, False
            buf += ch
        i += 1
    flush()
    return toks


def question_card(size=28, max_w=12.3, pitch=0.5):
    """The sheet's question, verbatim, wrapped. .box .lines .maths (math tokens in order)
    .groups {id: [tokens]} for the underlined phrases, .base {token: baseline y}."""
    toks = _tokens(QUESTION)
    space, glue = 0.0047 * size, 0.03
    mobs = []
    for kind, s, sp, g in toks:
        if kind == "t":
            m = T(s, size=size)
            m._src = s
            kit._baseline_align(m, 0)
            ref_y = 0.0
        else:
            mt = MathTex(r"\mathrm{x}", s, font_size=size * 1.05)
            mt.shift(-mt[0].get_bottom()[1] * UP)
            m = mt[1]
        mobs.append((m, sp, g, kind))
    lines, cur, x = [], [], 0.0
    for m, sp, g, kind in mobs:
        gap = (space if sp else glue) if cur else 0.0
        if cur and x + gap + m.width > max_w:
            lines.append(cur)
            cur, x, gap = [], 0.0, 0.0
        m.shift((x + gap - m.get_left()[0]) * RIGHT)
        x = m.get_right()[0]
        cur.append((m, g, kind))
    lines.append(cur)
    base = {}
    rows = VGroup()
    for li, ln in enumerate(lines):
        y = -li * pitch
        row = VGroup()
        for m, g, kind in ln:
            m.shift(y * UP)
            base[id(m)] = y
            row.add(m)
        rows.add(row)
    pad = 0.3
    box = RoundedRectangle(corner_radius=0.12, width=rows.width + 2 * pad, height=rows.height + 2 * pad)
    box.set_stroke(DIM, 1.5).set_fill(kit.CARD_FILL, 1).move_to(rows)
    card = VGroup(box, rows)
    card.move_to([-kit.EDGE_X, 3.3, 0], aligned_edge=UL)
    card.box, card.lines = box, rows
    card.maths = [m for ln in lines for (m, g, k) in ln if k == "m"]
    groups = {}
    for li, ln in enumerate(lines):
        for m, g, k in ln:
            if g is not None:
                groups.setdefault(g, {}).setdefault(li, []).append(m)
    card.groups = groups
    return card


def underlines(card, gid):
    out = []
    for li, ms in card.groups[gid].items():
        left = ms[0].get_left()[0]
        right = ms[-1].get_right()[0]
        y = min(m.get_bottom()[1] for m in ms) - 0.07
        out.append(Line([left, y, 0], [right, y, 0]).set_stroke(YELLOW, 4))
    return out


# ── column helpers ───────────────────────────────────────────────────────────────
def step_tex(tex, i):
    sl = kit.step_label("x", i + COL_OFF)
    arr = sl[0]
    lab = MathTex(tex, font_size=30, color=DIM).next_to(arr, RIGHT, buff=0.15)
    return VGroup(arr, lab)


COL_OFF = 0.3     # the column starts 0.21 lower than kit's: M8's card runs to three lines


def col(mob, i):
    return kit.col_place(mob, i + COL_OFF)


def cpt(i):
    return kit.col_point(i + COL_OFF)


def step(text, i):
    return kit.step_label(text, i + COL_OFF)


def tri(a, b, unit, corner):
    """Small right triangle: BLUE leg a along, PINK leg b down, GOLD hypotenuse (lines)."""
    p0 = np.array(corner, dtype=float)
    p1 = p0 + unit * a * RIGHT
    p2 = p1 + unit * b * DOWN
    g = VGroup(Line(p0, p1).set_stroke(BLUE, 4), Line(p1, p2).set_stroke(PINK, 4),
               Line(p0, p2).set_stroke(GOLD, 5))
    return g


class F19Question(NarratedScene):
    def construct(self):
        self.clip_card()
        self.clip_spring()
        self.clip_hint()
        self.clip_amp()

    # ── c4.sheet.1: the question ────────────────────────────────────────────────
    def clip_card(self):
        card = question_card()
        tg = strip_tag()
        fcard = card.maths[1]           # x = 7 + 24 cos 3t + 7 sin 3t, glyphs
        big = strip_formula(54).move_to([-0.4, -2.0, 0])
        self.card, self.tg, self.big = card, tg, big
        with self.say("c4.sheet.1") as c:
            self.play(*appear(tg, card, lag=0.3), run_time=1.5)   # early: the sheet's question, shown whole, then read
            c.wait_until("motion")
            # glyphs: x = 7 + 2 4 c o s 3 t + 7 s i n 3 t
            cols = {0: BLUE, 2: YELLOW, 4: BLUE, 5: BLUE, 12: BLUE}
            self.play(*[fcard[i].animate.set_color(col_) for i, col_ in cols.items()],
                      FlashAround(fcard, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("ex equals")
            self.play(*appear(big, shift=None), FlashAround(big, run_time=1.5, time_width=1.5),
                      run_time=min(1.5, c.until("plus twenty-four")))
            c.wait_until("asks")
            self.ul = []
            for gids, cue in (((0,), "amplitude"), ((1,), "first two times"), ((2, 3), "how far")):
                c.wait_until(cue)
                lines = [ln for g in gids for ln in underlines(card, g)]
                self.play(*[GrowFromEdge(ln, LEFT) for ln in lines], run_time=0.9)
                self.ul += lines
            c.wait_until("try")
            self.try_ = kit.tag("pause to try it").scale(1.2).next_to(big, DOWN, buff=0.55)
            self.play(*appear(self.try_), run_time=1.0)

    # ── c4.sheet.2: where the 7 comes from ──────────────────────────────────────
    def clip_spring(self):
        card, big = self.card, self.big
        target = strip()[1]
        with self.say("c4.sheet.2") as c:
            self.play(*during(disappear(card, *self.ul, self.try_), 0, 0.45),
                      *during([big.animate.scale(target.width / big.width).move_to(target)], 0.45, 1.0),
                      run_time=1.8)
            self.strip_f = big
            c.wait_until("seven")
            self.play(FlashAround(big[2], run_time=1.2, time_width=1.5, color=YELLOW))

            # the spring and its ruler
            c.wait_until("spring")
            xt = ValueTracker(7.0)
            self.xt = xt
            spring = s1.hanging_spring(7, pos=SPRING_POS)
            y0 = s1.weight_center(0, SPRING_POS)[1]
            y7 = SPRING_POS[1]
            ruler = Line([RULER_X, y0 - 0.45, 0], [RULER_X, y7 + 1.1, 0]).set_stroke(DIM, 2)
            t0 = Line([RULER_X - 0.12, y0, 0], [RULER_X + 0.12, y0, 0]).set_stroke(DIM, 3)
            t7 = Line([RULER_X - 0.12, y7, 0], [RULER_X + 0.12, y7, 0]).set_stroke(YELLOW, 4)
            n0 = T("0", size=26, color=DIM).next_to(t0, LEFT, buff=0.12)
            w0 = T("origin", size=26, color=DIM).next_to(n0, LEFT, buff=0.18)
            n7 = T("7", size=28, color=YELLOW).next_to(t7, LEFT, buff=0.12)
            w7 = T("centre", size=26, color=YELLOW).next_to(n7, LEFT, buff=0.18)
            beyond = kit.tag("beyond the notes").next_to(spring.ceiling, RIGHT, buff=0.3)
            self.play(FadeIn(spring), run_time=1.2)
            self.play(Create(ruler), FadeIn(t0), FadeIn(t7), *appear(n0, w0, n7, w7, beyond, lag=0.2),
                      run_time=1.6)
            leg = kit.legend(ENTRIES0)
            self.leg = leg
            c.wait_until("like the one")
            self.play(FadeIn(leg, shift=0.15 * UP), run_time=1.0)

            # balance
            c.wait_until("balance")
            wc = s1.weight_center(7, SPRING_POS)
            top = wc[1] + s1.BLOCK_H / 2
            bot = wc[1] - s1.BLOCK_H / 2
            down = ak.arrow_between([ARROW_X, wc[1] - 0.05, 0], [ARROW_X, wc[1] - 0.95, 0], FG, width=5)
            up = ak.arrow_between([ARROW_X, wc[1] + 0.05, 0], [ARROW_X, wc[1] + 0.95, 0], FG, width=5)
            mg = MathTex("mg", font_size=32).next_to(down.get_end(), RIGHT, buff=0.15).shift(0.25 * UP)
            pull = T("spring's pull", size=26).next_to(up.get_end(), RIGHT, buff=0.15).shift(0.25 * DOWN)
            c.wait_until("gravity pulls")
            self.play(GrowArrow(down), *appear(mg), run_time=1.2)
            c.wait_until("the spring stretches")
            self.play(GrowArrow(up), *appear(pull), run_time=1.2)   # early: names the spring's force, said as "its force" 
            bal = kit.tag("balanced").next_to(mg, DOWN, buff=0.25, aligned_edge=LEFT)
            l0 = MathTex(r"\text{at } x = 7:\ \ \text{spring's pull} = mg", font_size=kit.COL_SIZE)
            col(l0, 0)
            c.wait_until("balances gravity")
            self.play(*appear(bal, l0, lag=0.3), run_time=1.3)

            # the extra pull, live
            c.wait_until("extra")
            self.remove(spring)
            live = always_redraw(lambda: s1.hanging_spring(xt.get_value(), pos=SPRING_POS))
            self.add(live)

            def net():
                x = xt.get_value()
                d = x - 7
                yc = s1.weight_center(x, SPRING_POS)[1]
                if abs(d) < 0.4:
                    return VGroup()
                return ak.arrow_between([ARROW_X, yc, 0], [ARROW_X, yc - 0.13 * d, 0], RED, width=5)

            net_arr = always_redraw(net)
            net_lab = T("net pull", size=26, color=RED)

            def place_lab(m):
                x = xt.get_value()
                yc = s1.weight_center(x, SPRING_POS)[1]
                m.move_to([ARROW_X + 0.2, yc - 0.065 * (x - 7), 0], aligned_edge=LEFT)
                m.set_opacity(min(1.0, abs(x - 7) / 3.0))

            net_lab.add_updater(place_lab)
            place_lab(net_lab)
            self.add(net_arr, net_lab)
            self.play(*disappear(down, up, mg, pull, bal), run_time=0.8)
            self.play(xt.animate.set_value(13), run_time=1.6)   # early: the net pull is shown growing as "the extra pull" is said
            c.wait_until("pointing back")
            self.play(xt.animate.set_value(1), run_time=2.0)
            l1 = MathTex(r"\text{net pull}", "=", r"-k\,(x - 7)", font_size=kit.COL_SIZE)
            l1[0].set_color(RED)
            col(l1, 1)
            self.play(*appear(l1), run_time=1.0)

            # the same rule
            c.wait_until("same")
            self.play(xt.animate.set_value(7), run_time=1.2)
            net_lab.clear_updaters()
            self.remove(live, net_arr, net_lab)
            spring = s1.hanging_spring(7, pos=SPRING_POS)
            self.add(spring)
            l2 = MathTex(r"\ddot x", "=", r"-\omega^2\,(x - 7)", font_size=kit.COL_SIZE)
            l2[0].set_color(RED)
            col(l2, 2)
            s2 = step("Newton, then divide by m", 2)
            rule_tag = kit.tag("the rule, measured from 7").next_to(l2, DOWN, buff=0.22, aligned_edge=LEFT)
            self.play(*appear(s2, l2, lag=0.3, shift=None), run_time=1.4)
            self.play(*appear(rule_tag), run_time=0.9)
            c.wait_until("it's the centre")
            w7b = T("centre of motion", size=26, color=YELLOW).next_to(n7, LEFT, buff=0.18)
            self.play(*swap(w7, w7b), FlashAround(VGroup(n7, t7), run_time=1.2, time_width=1.5),
                      run_time=1.2)
            c.wait_until("ex minus seven")
            self.play(FlashUnder(l2[2], run_time=1.2, time_width=1.5))
        self.spring = spring
        self.ruler = VGroup(ruler, t0, t7, n0, w0, n7, w7b)
        self.beyond = beyond
        self.col2 = [l0, l1, l2, s2, rule_tag]

    # ── c4.sheet.3: hint 1 and the show-that ────────────────────────────────────
    def clip_hint(self):
        with self.say("c4.sheet.3") as c:
            hint = T("Hint 1", size=32, color=YELLOW)
            card = move_m8()
            hint.next_to(card, LEFT, buff=0.3).align_to(card, DOWN)
            self.play(*disappear(*self.col2, self.beyond), run_time=0.9)
            self.play(*appear(hint, card, lag=0.4), run_time=min(1.4, c.until("add")))
            c.wait_until("add")
            self.play(FlashAround(card.body, run_time=1.5, time_width=1.5))
            # spring to the inset, plane in
            pin = s1.amp_pin()
            plane = f19_plane()
            self.play(*disappear(self.ruler),
                      Transform(self.spring, inset_spring()), run_time=1.5)
            self.play(FadeIn(plane), *appear(pin), run_time=min(1.3, max(0.5, c.until("match") - 0.1)))
            self.plane, self.pin, self.card_m8, self.hint = plane, pin, card, hint

            # match
            c.wait_until("match")
            l1 = MathTex("x - 7", "=", "24", r"\cos 3t", "+", "7", r"\sin 3t", font_size=kit.COL_SIZE)
            l1[0].set_color(BLUE)
            l1[2].set_color(BLUE)
            l1[5].set_color(BLUE)
            col(l1, I_MATCH)
            self.play(*appear(l1, shift=None), run_time=1.0)
            ta = MathTex("a", font_size=28, color=BLUE).next_to(l1[2], DOWN, buff=0.12)
            tb = MathTex("b", font_size=28, color=BLUE).next_to(l1[5], DOWN, buff=0.12)
            tw = MathTex(r"\omega", font_size=28, color=FG).next_to(l1[3][3], DOWN, buff=0.12)
            tb.align_to(ta, DOWN)
            tw.align_to(ta, DOWN)
            blue = ak.arrow_between(F19_O, f19_point(24), BLUE, width=6, z=-1.8)
            pink = ak.arrow_between(f19_point(24), f19_point(24 - 7j), PINK, width=6, z=-1.8)
            lab24 = MathTex("24", font_size=32, color=BLUE).next_to(blue, UP, buff=0.12)
            lab7 = MathTex("-7i", font_size=32, color=PINK).next_to(pink, RIGHT, buff=0.12)
            c.wait_until("twenty-four")
            self.play(*appear(ta, shift=None), GrowArrow(blue), *appear(lab24), run_time=1.3)
            c.wait_until("sine coefficient")
            self.play(*appear(tb, shift=None), GrowArrow(pink), *appear(lab7), run_time=1.3)
            c.wait_until("omega is")
            self.play(*appear(tw, shift=None), run_time=0.9)

            # the one arrow
            c.wait_until("arrow")
            gold = gold_arrow()
            glab = gold_label()
            c.wait_until("twenty-four minus")
            self.play(GrowArrow(gold), *appear(glab), run_time=1.4)
            xl = x_line()
            col(xl, I_X)
            c.wait_until("times e")
            self.play(*appear(xl, shift=None), run_time=1.1)
            kit.legend_add(self, self.leg, E_XX, run_time=1.0)

            # the show-that
            c.wait_until("show")
            eul = MathTex("X", "=", "(", "24", "-", "7i", ")", r"(\cos 3t + i\sin 3t)",
                          font_size=kit.COL_SIZE)
            eul[0].set_color(GOLD)
            eul[3].set_color(BLUE)
            eul[5].set_color(PINK)
            col(eul, I_EUL)
            s_eul = step_tex(r"e^{i\theta} = \cos\theta + i\sin\theta", I_EUL)
            derive(self, xl, eul, run_time=2.0)
            self.play(*appear(s_eul, shift=None), run_time=0.8)
            e1 = MathTex("=", r"24\cos 3t", "+", r"24i\sin 3t", font_size=kit.COL_SIZE)
            e1[1].set_color(BLUE)
            e1[3].set_color(PINK)
            col(e1, I_EXP1)
            e2 = MathTex("-", r"7i\cos 3t", "-", r"7i^2\sin 3t", font_size=kit.COL_SIZE)
            e2[1].set_color(PINK)
            e2[3].set_color(PINK)
            e2.move_to(cpt(I_EXP2), aligned_edge=LEFT)
            e2.shift((e1[1].get_left()[0] - e2.get_left()[0] + 0.0) * RIGHT)
            s_mul = step("multiply out", I_EXP1)
            c.wait_until("multiply out")
            self.play(*appear(s_mul, e1, e2, lag=0.35, shift=None), run_time=min(1.8, c.until("flip")))

            # the flip
            c.wait_until("flip")
            self.play(FlashAround(e2[2:], run_time=1.4, time_width=1.5))
            s_i2 = MathTex(r"i^2 = -1", font_size=26, color=DIM).next_to(e2[3], RIGHT, buff=0.3)
            self.play(*appear(s_i2), run_time=0.9)
            e2b = MathTex("-", r"7i\cos 3t", "+", r"7\sin 3t", font_size=kit.COL_SIZE)
            e2b[1].set_color(PINK)
            e2b[3].set_color(BLUE)
            e2b.move_to(e2, aligned_edge=LEFT)
            c.wait_until("becomes")
            self.play(*edit(e2, e2b), run_time=1.5)
            s_i2.generate_target()
            s_i2.target.next_to(e2b, RIGHT, buff=0.3)
            self.play(MoveToTarget(s_i2), run_time=0.6)

            # the real part
            c.wait_until("real")
            re = MathTex(r"\mathrm{Re}\,X", "=", r"24\cos 3t", "+", r"7\sin 3t", font_size=kit.COL_SIZE)
            re[0][2].set_color(GOLD)
            re[2].set_color(BLUE)
            re[4].set_color(BLUE)
            col(re, I_RE)
            s_re = step("keep the real part", I_RE)
            self.play(*set_alpha([e1[2], e1[3], e2b[0], e2b[1]], 0.25),
                      *appear(s_re, re, lag=0.3, shift=None), run_time=min(1.4, max(0.6, c.until() - 0.9)))
            tick = check_mark(YELLOW).scale(0.8).next_to(re, RIGHT, buff=0.3)
            eqx = MathTex("= x - 7", font_size=30, color=YELLOW).next_to(tick, RIGHT, buff=0.15)
            self.play(*appear(tick, eqx, lag=0.2), run_time=max(0.5, min(0.9, c.until() + 0.2)))
        self.l1, self.tags = l1, [ta, tb, tw]
        self.blue, self.pink, self.lab24, self.lab7 = blue, pink, lab24, lab7
        self.gold, self.glab, self.xl = gold, glab, xl
        self.work = [eul, s_eul, s_mul, e1, e2b, s_i2]
        self.re = [s_re, re, tick, eqx]

    # ── c4.sheet.4: T4.3 and the amplitude ──────────────────────────────────────
    def clip_amp(self):
        with self.say("c4.sheet.4", gap=3.4) as c:
            # finished working leaves; the result moves up
            dy = (cpt(I_RE_UP) - cpt(I_RE))[1]
            self.play(*during(disappear(*self.work), 0, 0.45),
                      *during([m.animate.shift(dy * UP) for m in self.re], 0.4, 1.0), run_time=1.4)
            # think stop T4.3
            q = VGroup(
                T("The displacement from the centre", size=28),
                VGroup(T("is the shadow of", size=28),
                       MathTex(r"(24 - 7i)\,e^{3it}", font_size=30, color=GOLD)).arrange(RIGHT, buff=0.15),
                T("How big is the swing?", size=28)).arrange(DOWN, buff=0.16)
            q[1][1].align_to(q[1][0], DOWN).shift(0.02 * DOWN)
            box = RoundedRectangle(corner_radius=0.12, width=q.width + 0.5, height=q.height + 0.42)
            box.set_stroke(FG, 2).set_fill(kit.CARD_FILL, 1)
            q.move_to(box)
            hint = T("pause the video if you want longer", size=24, color=DIM).next_to(box, DOWN, buff=0.14)
            think = VGroup(box, q, hint).move_to([3.4, -2.25, 0])
            ring = kit.think_ring()
            self.play(FadeIn(box), *appear(*q, lag=0.3), FadeIn(ring), run_time=1.4)   # early: the think stop's question, read at once
            c.wait_until("pause the video")
            self.play(*appear(hint), run_time=0.8)
            self.play(kit.drain(ring, c.until("amp")))

            # the length of the arrow
            c.wait_until("amp")
            self.play(*disappear(think, ring), run_time=0.8)
            self.play(*during(disappear(self.hint, self.l1, *self.tags, *self.re), 0, 0.45),
                      *during([self.xl.animate.move_to(cpt(0), aligned_edge=LEFT)], 0.4, 1.0),
                      run_time=1.4)
            lab7b = MathTex("7", font_size=32, color=PINK).move_to(self.lab7, aligned_edge=LEFT)
            self.play(*swap(self.lab7, lab7b), VShowPassingFlash(self.gold.copy().set_stroke(YELLOW, 8),
                                                                  time_width=0.5), run_time=1.2)

            # Pythagoras, atomic
            r1 = MathTex(r"|24 - 7i|", "=", r"\sqrt{", "24^2", "+", "7^2", "}", font_size=kit.COL_SIZE)
            r1[0].set_color(GOLD)
            r1[3].set_color(BLUE)
            r1[5].set_color(PINK)
            col(r1, 1)
            eq_x = r1[1].get_left()[0]

            def row(parts, i, colors):
                m = MathTex(*parts, font_size=kit.COL_SIZE)
                for k, cl in colors.items():
                    m[k].set_color(cl)
                m.move_to(cpt(i), aligned_edge=LEFT)
                m.shift((eq_x - m[0].get_left()[0]) * RIGHT)
                return m

            r2 = row(["=", r"\sqrt{", "576", "+", "49", "}"], 2, {2: BLUE, 4: PINK})
            r3 = row(["=", r"\sqrt{625}"], 3, {})
            r4 = row(["=", "25"], 4, {1: GOLD})
            steps = [step("Pythagoras", 1), step("square each", 2),
                     step("add", 3), step("square root", 4)]
            c.wait_until("pythagoras")
            self.play(*appear(steps[0], r1, lag=0.3, shift=None), run_time=1.3)
            c.wait_until("twenty-four squared")
            self.play(*appear(steps[1], r2, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("make six")
            self.play(*appear(steps[2], r3, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("twenty-five squared")
            self.play(*appear(steps[3], r4, lag=0.3, shift=None), run_time=1.2)

            # amplitude 25, and its small cousin
            c.wait_until("sibling")
            amp = T("amplitude 25", size=32, color=YELLOW)
            amp_box = SurroundingRectangle(amp, color=YELLOW, buff=0.16, corner_radius=0.08).set_stroke(width=2.5)
            ampg = VGroup(amp_box, amp).next_to(r4, RIGHT, buff=0.7)
            self.play(GrowFromCenter(amp_box), *appear(amp), run_time=1.2)
            big_tri = tri(24, 7, 0.1, [1.0, -2.3, 0])
            cap1 = T("7, 24, 25", size=28).next_to(big_tri, DOWN, buff=0.25)
            small = tri(3, 4, 0.25, [3.95, -2.0, 0])
            small.align_to(big_tri, DOWN)
            cap2 = T("3, 4, 5", size=28).next_to(small, DOWN, buff=0.25).align_to(cap1, DOWN)
            third = kit.tag("third weight").next_to(small, RIGHT, buff=0.3)
            c.wait_until("its triangle")
            srcs = [self.blue.copy(), self.pink.copy(), self.gold.copy()]
            self.play(*[ReplacementTransform(s_, d_) for s_, d_ in zip(srcs, big_tri)], *appear(cap1),
                      run_time=1.5)
            c.wait_until("cousin")
            self.play(*[Create(m) for m in small], *appear(cap2, third, lag=0.3), run_time=1.4)

        # the rest leaves; the handover shot stays
        keep = handover_shot()
        self.play(*disappear(self.blue, self.pink, self.lab24, lab7b, self.card_m8, r1, r2, r3, r4,
                             *steps, ampg, big_tri, small, cap1, cap2, third), run_time=1.0)
        # make the frame exactly the handover shot
        self.remove(*self.mobjects)
        self.add(*keep)
        self.wait(1.0)
