"""Chapter 1, scene 3: the pull grows with the stretch (Hooke, Newton, the rule ẍ = −ω²x). Clips c1.spring.1 – c1.spring.5.

Also the project's spring drawing, reused in every chapter (load_scene("ch1_s3_spring")):
  spring_drawing(x=0, y=SPRING_Y, zero=True)  wall, FG coil, BLUE block, DIM table, DIM tick "0"
                                               (x = displacement in cm, + to the right)
  block_center(x, y)                           centre of the block at displacement x
  stretch_arrow(x, y)                          BLUE arrow from the 0 tick to the block (under the table)
  pull_arrow(x, y, per_cm=PULL_PER_CM)         RED pull on the block, back toward 0 (above the block)
  rule_boxed()                                 the boxed rule ẍ = −ω²x (ẍ RED, x BLUE, YELLOW box)
  handover_shot()                              this scene's last frame (spring at rest, rule, legend, tag)
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

# ═══════════════════════════════ the spring (shared) ═══════════════════════════════
SPRING_Y = 0.4            # table line y
SPRING_WALL_X = -6.3      # wall face
SPRING_REST_X = -3.2      # block centre at rest (the "0" tick)
SPRING_UNIT = 0.5         # scene units per cm of displacement
SPRING_TABLE_R = 0.4      # right end of the table
BLOCK_W, BLOCK_H = 0.9, 0.8
WALL_H = 1.2
PULL_PER_CM = 0.4         # pull arrow length per cm of stretch
ARROW_DY = 0.22           # stretch arrow: this far under the table
PULL_DY = 0.3             # pull arrow: this far above the block

E_K = (r"k", FG, "stiffness")
E_M = (r"m", FG, "mass")
E_W = (r"\omega", FG, "pull back per unit stretch, per kg")
ENTRIES = [kit.E_X, kit.E_XD, kit.E_XDD, E_K, E_M, E_W]
RULE_POS = np.array([(kit.COL_LEFT + kit.EDGE_X) / 2, SPRING_Y + BLOCK_H / 2, 0])


def block_center(x=0.0, y=SPRING_Y):
    return np.array([SPRING_REST_X + SPRING_UNIT * x, y + BLOCK_H / 2, 0])


def _coil(x0, x1, y, turns=8, amp=0.2, lead=0.22):
    pts = [[x0, y, 0], [x0 + lead, y, 0]]
    n = 2 * turns
    span = max(x1 - x0 - 2 * lead, 0.05)
    for i in range(n):
        t = (i + 0.5) / n
        pts.append([x0 + lead + t * span, y + (amp if i % 2 == 0 else -amp), 0])
    pts += [[x1 - lead, y, 0], [x1, y, 0]]
    return VMobject().set_points_as_corners(pts).set_stroke(FG, 3)


def spring_drawing(x=0.0, y=SPRING_Y, zero=True):
    """The spring: wall (left), FG coil, BLUE block on a DIM table, DIM tick (+ "0") under the
    rest position. x = displacement in cm (+ right). .table .wall .hatch .coil .block .tick .zero"""
    c = block_center(x, y)
    table = Line([SPRING_WALL_X - 0.25, y, 0], [SPRING_TABLE_R, y, 0]).set_stroke(DIM, 3)
    wall = Line([SPRING_WALL_X, y, 0], [SPRING_WALL_X, y + WALL_H, 0]).set_stroke(FG, 4)
    hatch = VGroup(*[Line([SPRING_WALL_X, y + 0.2 + 0.25 * i, 0],
                          [SPRING_WALL_X - 0.2, y + 0.0 + 0.25 * i, 0]) for i in range(5)])
    hatch.set_stroke(DIM, 2)
    block = Rectangle(width=BLOCK_W, height=BLOCK_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.3)
    block.move_to(c)
    coil = _coil(SPRING_WALL_X, c[0] - BLOCK_W / 2, c[1])
    tick = Line([SPRING_REST_X, y - 0.14, 0], [SPRING_REST_X, y, 0]).set_stroke(DIM, 3)
    g = VGroup(table, hatch, wall, coil, block, tick)
    g.table, g.wall, g.hatch, g.coil, g.block, g.tick, g.zero = table, wall, hatch, coil, block, tick, None
    if zero:
        z = T("0", size=28, color=DIM).move_to([SPRING_REST_X, y - 0.52, 0])
        g.add(z)
        g.zero = z
    return g


def _harrow(x0, x1, y, color):
    if abs(x1 - x0) < 0.06:
        return Arrow([x0, y, 0], [x0 + 0.06, y, 0], buff=0, stroke_width=5, tip_length=0.03,
                     color=color).set_opacity(0)
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, stroke_width=5, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=30,
                 color=color)


def stretch_arrow(x=0.0, y=SPRING_Y):
    """BLUE displacement arrow, from the 0 tick to the block's centre, just under the table."""
    return _harrow(SPRING_REST_X, block_center(x, y)[0], y - ARROW_DY, BLUE)


def pull_arrow(x=0.0, y=SPRING_Y, per_cm=PULL_PER_CM):
    """RED pull on the block, from its centre back toward 0, just above the block."""
    cx = block_center(x, y)[0]
    return _harrow(cx, cx - per_cm * x, y + BLOCK_H + PULL_DY, RED)


def rule_line():
    m = MathTex(r"\ddot{x}", "=", r"-\omega^2", "x", font_size=kit.COL_SIZE)
    m[0].set_color(RED)
    m[3].set_color(BLUE)
    return m


def rule_boxed():
    """The boxed rule ẍ = −ω²x. .line .box"""
    line = rule_line()
    box = SurroundingRectangle(line, color=YELLOW, buff=0.16).set_stroke(YELLOW, 3)
    g = VGroup(line, box)
    g.line, g.box = line, box
    return g


def handover_shot():
    """Last frame of s3 = first of s4: spring at rest, the boxed rule (right, at block height),
    the six-entry legend and the corner tag. .spring .rule .legend .tag"""
    sp = spring_drawing(0.0)
    rule = rule_boxed().move_to(RULE_POS)
    ch = kit.chrome(ENTRIES)
    g = VGroup(sp, rule, ch.legend, ch.tag)
    g.spring, g.rule, g.legend, g.tag = sp, rule, ch.legend, ch.tag
    return g


# ═══════════════════════════════ scene helpers ═══════════════════════════════
def _readout(label_tex, color, unit_tex, fn, size=32):
    """Live 'label = value unit': the number right-aligned before the unit, on its baseline."""
    tmpl = MathTex(label_tex, "=", r"-0.0", unit_tex, font_size=size)
    tmpl[0].set_color(color)
    lab, eq, slot, unit = tmpl
    unit.shift(0.08 * RIGHT)
    dec = DecimalNumber(fn(), num_decimal_places=1, font_size=size, color=color)

    def upd(d):
        d.set_value(fn())
        d.shift([unit.get_left()[0] - 0.12 - d.get_right()[0], unit.get_bottom()[1] - d.get_bottom()[1], 0])

    upd(dec)
    dec.add_updater(upd)
    g = VGroup(lab, eq, dec, unit)
    return g


def _static_readout(label_tex, color, value_tex, size=30):
    m = MathTex(label_tex, "=", value_tex, font_size=size)
    m[0].set_color(color)
    m[2].set_color(color)
    return m


def _top_at(mob, top):
    mob.shift((top - mob.get_top()[1]) * UP + (kit.COL_LEFT - mob.get_left()[0]) * RIGHT)
    return mob


def _step(text, y):
    lab = kit.step_label(text, 0)
    lab.shift((y - lab[0].get_center()[1]) * UP)
    return lab


GAP = 0.5


class Spring(NarratedScene):
    def construct(self):
        ch = kit.handover_shot()
        self.add(*ch)
        self.leg, self.ctag = ch.legend, ch.tag
        self.xt = ValueTracker(0.0)
        self.ty = ValueTracker(SPRING_Y)
        self.c1_spring()
        self.c2_sign()
        self.c3_newton()
        self.c4_rule()
        self.c5_stop()

    # ── c1.spring.1 ───────────────────────────────────────────────────────────────
    def c1_spring(self):
        xt, ty = self.xt, self.ty
        with self.say("c1.spring.1") as c:
            sp0 = spring_drawing(0.0)
            self.play(*appear(sp0, shift=None), run_time=1.5)
            self.remove(*sp0.get_family())
            self.live = always_redraw(lambda: spring_drawing(xt.get_value(), ty.get_value()))
            self.xarr = always_redraw(lambda: stretch_arrow(xt.get_value(), ty.get_value()))
            self.parr = always_redraw(lambda: pull_arrow(xt.get_value(), ty.get_value()))
            self.add(self.live, self.xarr, self.parr)

            self.nofric = kit.tag("no friction")
            self.nofric.move_to([SPRING_WALL_X, SPRING_Y - 0.45, 0], aligned_edge=LEFT)
            c.wait_until("smooth table")
            self.play(*appear(self.nofric), run_time=1.0)

            self.xread = _readout("x", BLUE, r"\mathrm{cm}", lambda: xt.get_value(), size=34)
            self.pread = _readout(r"\text{pull}", RED, r"\mathrm{N}",
                                  lambda: abs(0.5 * xt.get_value()), size=34)
            self.xread.move_to([1.3, 1.3, 0], aligned_edge=LEFT)
            self.pread.move_to([1.3, 0.6, 0], aligned_edge=LEFT)
            self.pread.shift((self.xread[1].get_left()[0] - self.pread[1].get_left()[0]) * RIGHT)
            c.wait_until("pull")
            self.play(*appear(self.xread, self.pread, shift=None, lag=0.2), run_time=0.9)
            t = c.until("twice")
            self.play(xt.animate.set_value(3.5), run_time=0.6 * t)
            self.play(xt.animate.set_value(2.0), run_time=max(0.3, c.until("twice") - 0.3))
            c.wait_until("twice")

            ghost = pull_arrow(2.0)
            self.add(ghost)
            self.play(ghost.animate.shift(0.38 * UP).set_opacity(0.45), run_time=0.9)
            self.play(xt.animate.set_value(4.0), ghost.animate.shift(2 * SPRING_UNIT * RIGHT),
                      run_time=2.0)
            self.ghost = ghost
            self.twice = T("twice the stretch, twice the pull", size=26)
            self.twice.next_to(ghost, UP, buff=0.3).align_to(ghost, RIGHT).shift(0.5 * RIGHT)
            self.play(*appear(self.twice), run_time=1.0)

            self.hooke = kit.tag("Hooke's law (GCSE)")
            self.hooke.move_to([SPRING_TABLE_R, SPRING_Y - 0.5, 0], aligned_edge=RIGHT)
            c.wait_until("hooke's law")
            self.play(*appear(self.hooke), run_time=1.0)

    # ── c1.spring.2 ───────────────────────────────────────────────────────────────
    def c2_sign(self):
        xt = self.xt
        with self.say("c1.spring.2") as c:
            c.wait_until("ex to the right")
            self.play(*disappear(self.ghost, self.twice), FlashAround(self.xread, color=BLUE, time_width=1.5),
                      run_time=1.3)
            c.wait_until("pull points left")
            self.play(FlashAround(self.parr, color=RED, time_width=1.5), run_time=1.3)
            c.wait_until("push the weight")
            self.play(xt.animate.set_value(-2.5), run_time=min(2.6, c.until("hooke") - 0.2))
            c.wait_until("hooke")

            cap = MathTex("F", "=", "-", "k", "x", font_size=52)
            cap[0].set_color(RED)
            cap[4].set_color(BLUE)
            cap.move_to([-6.1, -0.72, 0], aligned_edge=LEFT)
            self.cap = cap
            self.play(*appear(cap), run_time=1.2)
            c.wait_until("stiffness says")
            kit.legend_add(self, self.leg, E_K)

            c.wait_until("minus")
            self.play(FlashAround(cap[2], color=YELLOW, time_width=1.5), cap[2].animate.set_color(YELLOW),
                      xt.animate.set_value(2.0), run_time=2.2)
            self.back = kit.tag("back toward the middle")
            self.back.next_to(cap, RIGHT, buff=0.4)
            self.back.shift((cap[0].get_bottom()[1] - self.back.get_bottom()[1]) * UP)
            c.wait_until(own_word=self.back)
            self.play(*appear(self.back), run_time=0.9)

    # ── c1.spring.3 ───────────────────────────────────────────────────────────────
    def c3_newton(self):
        with self.say("c1.spring.3") as c:
            self.play(*disappear(self.xread, self.pread), run_time=1.0)
            for m in (self.xread, self.pread):
                for s in m:
                    s.clear_updaters()

            card = kit.trolley_card(small=True)
            card.scale(1.25).move_to([5.0, 0.1, 0])
            self.trolley = card
            c.wait_until("newton ties")
            self.play(*appear(card, shift=None), run_time=1.2)
            row = next(r for r in self.leg.rows if r.key == r"\ddot{x}")
            c.wait_until("differentiated twice")
            self.play(FlashAround(row, color=RED, time_width=1.5), run_time=1.4)

            self.move = kit.move_card("Name the pull, then let Newton turn it into an acceleration.")
            c.wait_until("move")
            self.play(*appear(self.move, shift=None), run_time=1.2)

            # the column, stacked from under the move card
            top0 = min(1.75, self.move.get_bottom()[1] - 0.5)
            L0 = MathTex("F", "=", "m", r"\ddot{x}", font_size=kit.COL_SIZE)
            L0[0].set_color(RED)
            L0[3].set_color(RED)
            _top_at(L0, top0)
            lab0 = _step("Newton", L0.get_top()[1] + 0.27)
            L1 = MathTex("m", r"\ddot{x}", "=", "-k", "x", font_size=kit.COL_SIZE)
            L1[1].set_color(RED)
            L1[4].set_color(BLUE)
            _top_at(L1, L0.get_bottom()[1] - GAP)
            lab1 = _step("the force is the pull", L0.get_bottom()[1] - GAP / 2)
            L2 = MathTex(r"\ddot{x}", "=", r"-\frac{k}{m}", r"\,x", font_size=kit.COL_SIZE)
            L2[0].set_color(RED)
            L2[3].set_color(BLUE)
            _top_at(L2, L1.get_bottom()[1] - GAP)
            lab2 = _step("divide by m", L1.get_bottom()[1] - GAP / 2)
            self.L, self.labs = [L0, L1, L2], [lab0, lab1, lab2]

            c.wait_until("newton")
            self.play(*fly(card.law_x, L0), *during(appear(lab0, shift=None), 0.6, 1), run_time=1.6)
            kit.legend_add(self, self.leg, E_M)

            c.wait_until("sub")
            derive(self, L0, L1, FlashAround(self.cap, color=RED, time_width=1.5), run_time=2.2)
            self.play(*appear(lab1, shift=None), *disappear(card), run_time=1.0)

            c.wait_until("divide")
            derive(self, L1, L2, run_time=2.2)
            self.play(*appear(lab2, shift=None), run_time=0.8)

    # ── c1.spring.4 ───────────────────────────────────────────────────────────────
    def c4_rule(self):
        xt = self.xt
        L0, L1, L2 = self.L
        lab0, lab1, lab2 = self.labs
        with self.say("c1.spring.4") as c:
            self.play(FlashAround(L2[2], color=YELLOW, time_width=1.5), run_time=1.5)

            L3 = MathTex(r"\omega^2", "=", r"\frac{k}{m}", font_size=kit.COL_SIZE)
            _top_at(L3, L2.get_bottom()[1] - GAP)
            lab3 = _step("a name", L2.get_bottom()[1] - GAP / 2)
            c.wait_until("call it omega")
            derive(self, L2, L3, *set_alpha([L0, lab0], 0.4), run_time=2.0)
            kit.legend_add(self, self.leg, E_W, extra=appear(lab3, shift=None))

            R = rule_boxed()
            _top_at(R, L3.get_bottom()[1] - GAP)
            lab4 = _step("put in the name", L3.get_bottom()[1] - GAP / 2)
            c.wait_until("rule")
            derive(self, L3, R.line, *set_alpha([L1, lab1], 0.4), run_time=2.0)
            self.play(GrowFromCenter(R.box), *appear(lab4, shift=None), run_time=1.0)
            settle(self, R, add=[R.line, R.box])
            self.R = R
            self.L += [L3]
            self.labs += [lab3, lab4]

            c.wait_until("points back")
            self.play(FlashAround(R.line[2][0], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("grows with")
            t = c.until()
            self.play(xt.animate.set_value(4.0), run_time=min(2.2, 0.45 * t))
            self.play(xt.animate.set_value(2.0), run_time=min(2.2, max(0.4, c.until() - 0.1)))

    # ── c1.spring.5 ───────────────────────────────────────────────────────────────
    def c5_stop(self):
        xt, ty = self.xt, self.ty
        L0, L1, L2, L3 = self.L
        lab0, lab1, lab2, lab3, lab4 = self.labs
        R = self.R
        with self.say("c1.spring.5") as c:
            # the finished derivation: the oldest lines leave, the rest close up
            d = (L0.get_top()[1] - L3.get_top()[1]) * UP
            self.play(*during(disappear(L0, L1, L2, lab0, lab1, lab2, lab3, self.back), 0, 0.45),
                      *during([m.animate.shift(d) for m in (L3, lab4, R)], 0.35, 1),
                      run_time=1.5)

            q = ("Same spring, twice the mass.\nIs the acceleration back toward\n"
                 "the middle bigger or smaller,\nand by how much?")
            box = kit.think_box(q, size=30)
            box.shift((R.get_bottom()[1] - 0.3 - box.box.get_top()[1]) * UP)
            ring = kit.think_ring()
            c.wait_until("same spring")
            self.play(*appear(box, shift=None), FadeIn(ring), *set_alpha([self.move], 0.6),
                      run_time=1.2)
            self.play(kit.drain(ring, run_time=max(1.0, c.until("same_pull") - 0.2)))
            c.wait_until("same_pull")

            # the second spring, same stretch, twice the mass
            T1, T2 = 1.3, -0.7
            self.play(*during(disappear(box, ring, self.cap, self.hooke, self.nofric), 0, 0.45),
                      *during([restyle(self.move, 1)], 0, 0.5),
                      *during([ty.animate.set_value(T1)], 0.35, 1), run_time=1.6)
            sp2 = VGroup(spring_drawing(2.0, T2, zero=False), stretch_arrow(2.0, T2), pull_arrow(2.0, T2))
            m1 = MathTex("m", font_size=32).move_to(block_center(2.0, T1))
            m2 = MathTex("2m", font_size=32).move_to(block_center(2.0, T2))
            self.play(*appear(sp2, shift=None), *appear(m1, m2, shift=None), run_time=1.4)
            p1 = _static_readout(r"\text{pull}", RED, r"1.0\ \mathrm{N}")
            p2 = _static_readout(r"\text{pull}", RED, r"1.0\ \mathrm{N}")
            p1.move_to([SPRING_WALL_X + 0.3, T1 + BLOCK_H + PULL_DY, 0], aligned_edge=LEFT)
            p2.move_to([SPRING_WALL_X + 0.3, T2 + BLOCK_H + PULL_DY, 0], aligned_edge=LEFT)
            c.wait_until("same as before")
            self.play(*appear(p1, p2, shift=None, lag=0.2), *flash([self.parr, sp2[2]], color=RED),
                      run_time=1.4)
            c.wait_until("twice the mass")
            self.play(FlashAround(m2, color=YELLOW, time_width=1.5), run_time=1.3)

            a1 = _static_readout(r"\ddot{x}", RED, r"-2.0\ \mathrm{m/s^2}")
            a2 = _static_readout(r"\ddot{x}", RED, r"-1.0\ \mathrm{m/s^2}")
            a1.next_to(p1, UP, buff=0.22, aligned_edge=LEFT)
            a2.next_to(p2, UP, buff=0.22, aligned_edge=LEFT)
            L5 = MathTex(r"\ddot{x}", "=", r"-\frac{k}{2m}", r"\,x", font_size=kit.COL_SIZE)
            L5[0].set_color(RED)
            L5[3].set_color(BLUE)
            _top_at(L5, R.get_bottom()[1] - GAP)
            lab5 = _step("twice the mass", R.get_bottom()[1] - GAP / 2)
            half = T("half", size=32, color=YELLOW).next_to(L5, RIGHT, buff=0.45)
            c.wait_until("half")
            self.play(*appear(a1, a2, shift=None, lag=0.3), run_time=1.0)
            self.play(*appear(lab5, L5, shift=None, lag=0.3), run_time=1.4)
            self.play(*appear(half), FlashAround(L5[2], color=YELLOW, time_width=1.5), run_time=1.2)

            # the second spring leaves; the board closes on the spring at rest and the rule
            c.wait_until("swings more slowly")
            self.play(*disappear(sp2, m2, p2, a2, m1, p1, a1), run_time=1.0)
        self.play(*during(disappear(L3, L5, lab4, lab5, half, self.move), 0, 0.45),
                      *during([ty.animate.set_value(SPRING_Y), xt.animate.set_value(0.0),
                               R.animate.move_to(RULE_POS)], 0.3, 1),
                      run_time=1.8)

        final = handover_shot()
        self.remove(self.live, self.xarr, self.parr)
        self.add(final.spring)
        self.wait(1.0)
