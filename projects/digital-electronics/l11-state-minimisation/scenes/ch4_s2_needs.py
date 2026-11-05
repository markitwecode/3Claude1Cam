"""Chapter 4, scene 2: what a state machine needs (p. 122's Moore schematic, logic + D flip-flops,
separate chips vs a programmable device, p. 156's PLA reminder). Clips c4.needs.1 – c4.needs.3.

Shared helpers (import with load_scene("ch4_s2_needs")):
- `moore_schematic()`: p. 122's Moore schematic as L10 ch1 s2 drew it (L10's coordinates, about
  13.4 x 4.5, centre near (0, 0.2)). Handles: .b1 .b1t (next-state logic box + text), .b2 .b2t
  (optional output logic), .ff (D flip-flop: .box .tri .d_l .q_l .qb_l), .clk .clk_w (YELLOW CLK
  label + line), .cs (GREEN "Current state" label), .loop_up .loop_dn (the feedback wire), .tap,
  .inp .in_w .d_w .q_w .out_w .outp (wires/labels).
  `loop_path(sch)` → a fresh polyline along Current state (Q, up, over, down into the box) for pulses;
  `wire_line(arrow)` → a fresh Line along a wire.
- `two_brackets(sch)`: the BLUE braces under it: .comb (two braces + "combinational logic" labels,
  one under each logic box) and .dff (brace + "D flip-flops" under the flip-flop).
- `handover_shot()`: the last frame, the YELLOW "PLA" at the top-centre title position.
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


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- the Moore schematic (L10 ch1 s2)
def qbar(size=32, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.06)
    return VGroup(q, bar)


def dff(center=ORIGIN, w=1.4, h=2.0, pin=0.45):
    box = Rectangle(width=w, height=h).set_stroke(FG, 4).set_fill(BG, 1)
    tri = Polygon(_p(-0.17, -h / 2), _p(0.17, -h / 2), _p(0, -h / 2 + 0.26)).set_stroke(FG, 3)
    d_l = T("D", 32, BLUE).move_to(_p(-w / 2 + 0.27, pin))
    q_l = T("Q", 32, GREEN).move_to(_p(w / 2 - 0.27, pin))
    qb_l = qbar().move_to(_p(w / 2 - 0.27, -pin + 0.05))
    g = VGroup(box, tri, d_l, q_l, qb_l)
    g.box, g.tri, g.d_l, g.q_l, g.qb_l = box, tri, d_l, q_l, qb_l
    g.shift(center)
    return g


def bus_slash(x, y, label, color):
    s = Line(_p(x - 0.12, y - 0.17), _p(x + 0.12, y + 0.17)).set_stroke(color, 3)
    t = T(label, 28, color).next_to(s, UP, buff=0.08)
    return s, t


def logic_box(text, x, w=2.6, h=2.0):
    box = Rectangle(width=w, height=h).set_stroke(FG, 4).move_to(_p(x, 0))
    t = T(text, 28, line_spacing=0.85).move_to(box)
    return box, t


def _wire(a, b, color, ratio=0.25):
    return Arrow(a, b, buff=0, stroke_width=4, max_tip_length_to_length_ratio=ratio).set_color(color)


def moore_schematic():
    inp = T("Inputs", 32, BLUE).move_to(_p(-6.15, 0))
    in_w = _wire(_p(-5.48, 0), _p(-4.7, 0), BLUE, 0.3)
    in_s, in_n = bus_slash(-5.05, 0, "n", BLUE)
    b1, b1t = logic_box("Next state\ncombinational\nlogic", -3.4)
    d_w = _wire(_p(-2.1, 0), _p(-0.7, 0), BLUE, 0.2)
    d_s, d_m = bus_slash(-1.4, 0, "m", BLUE)
    ff = dff(_p(0, -0.45))
    qb_w = Line(_p(0.7, -0.9), _p(1.0, -0.9)).set_stroke(GREEN, 3)
    q_w = _wire(_p(0.7, 0), _p(1.75, 0), GREEN)
    q_s, q_m = bus_slash(1.42, 0, "m", GREEN)
    b2, b2t = logic_box("Optional\ncombinational\nlogic", 3.05)
    out_w = _wire(_p(4.35, 0), _p(5.05, 0), GREEN, 0.3)
    outp = T("Outputs", 32, GREEN).next_to(out_w, RIGHT, buff=0.12)
    tap = Dot(_p(1.05, 0), radius=0.07, color=GREEN)
    loop_up = VMobject().set_points_as_corners([_p(1.05, 0), _p(1.05, 1.9), _p(-3.4, 1.9)])
    loop_up.set_stroke(GREEN, 4)
    loop_dn = _wire(_p(-3.4, 1.9), _p(-3.4, 1.0), GREEN, 0.3)
    cs = T("Current state", 30, GREEN).move_to(_p(-1.2, 2.3))
    clk_w = Line(_p(0, -2.05), _p(0, -1.47)).set_stroke(YELLOW, 4)
    clk = T("CLK", 30, YELLOW).next_to(clk_w.get_start(), LEFT, buff=0.12)
    parts = dict(inp=inp, in_w=in_w, in_s=in_s, in_n=in_n, b1=b1, b1t=b1t, d_w=d_w, d_s=d_s,
                 d_m=d_m, ff=ff, qb_w=qb_w, q_w=q_w, q_s=q_s, q_m=q_m, tap=tap, b2=b2, b2t=b2t,
                 out_w=out_w, outp=outp, loop_up=loop_up, loop_dn=loop_dn, cs=cs,
                 clk_w=clk_w, clk=clk)
    g = VGroup(*parts.values())
    for k, v in parts.items():
        setattr(g, k, v)
    return g


def loop_path(sch):
    """Fresh polyline along the Current-state wire: from Q's tap, up, over, down into the logic."""
    top = sch.loop_up.get_top()[1]
    return VMobject().set_points_as_corners([
        sch.tap.get_center(), _p(sch.tap.get_x(), top),
        _p(sch.loop_dn.get_x(), top), sch.loop_dn.get_end()])


def wire_line(arrow):
    return Line(arrow.get_start(), arrow.get_end())


def two_brackets(sch):
    y = sch.clk_w.get_start()[1] - 0.3
    comb, labs = [], []
    for box in (sch.b1, sch.b2):
        b = span_brace(_p(box.get_left()[0], y), _p(box.get_right()[0], y), color=BLUE)
        lab = T("combinational\nlogic", 30, BLUE, line_spacing=0.8).next_to(b, DOWN, buff=0.14)
        comb += [b, lab]
        labs.append(lab)
    fb = span_brace(_p(sch.ff.box.get_left()[0], y), _p(sch.ff.box.get_right()[0], y), color=BLUE)
    fl = T("D flip-flops", 30, BLUE).next_to(fb, DOWN, buff=0.14).align_to(labs[0], UP)
    g = VGroup(*comb, fb, fl)
    g.comb = VGroup(*comb)
    g.comb_braces, g.comb_labels = [comb[0], comb[2]], labs
    g.dff = VGroup(fb, fl)
    g.ff_brace, g.ff_label = fb, fl
    return g


# ---------------------------------------------------------------- chip packages: s1's helpers
def face_grid(pkg, cols=6, rows=4, color=BLUE):
    """A small programmable grid on a package's face: rails, columns, and a dot at each crossing."""
    b = pkg.body
    w, h = b.width * 0.62, b.height * 0.6
    c = b.get_center()
    xs = [c[0] - w / 2 + i * w / (cols - 1) for i in range(cols)]
    ys = [c[1] - h / 2 + j * h / (rows - 1) for j in range(rows)]
    lines = [Line(_p(xs[0], y), _p(xs[-1], y)).set_stroke(color, 2) for y in ys]
    lines += [Line(_p(x, ys[0]), _p(x, ys[-1])).set_stroke(color, 2) for x in xs]
    dots = [Dot(_p(x, y), radius=0.045, color=color) for x in xs for y in ys]
    return VGroup(*lines, *dots)


# ---------------------------------------------------------------- handover
PLA_POS = _p(0, 3.3)


def handover_shot():
    return VGroup(T("PLA", 48, YELLOW).move_to(PLA_POS))


class Needs(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.8)   # handover: end on the YELLOW "PLA" at s3's title position

    # ------------------------------------------------------------ c1: the Moore schematic, walked
    def clip1(self):
        with self.say("c4.needs.1") as c:
            sch = moore_schematic().shift(0.4 * UP)
            self.sch = sch
            self.play(*appear(*sch, shift=None, lag=0.04),  # early: whole schematic first, then walked
                      run_time=min(2.0, c.until("logic")))
            settle(self, sch)
            c.wait_until("logic")

            self.play(VShowPassingFlash(wire_line(sch.in_w).set_stroke(YELLOW, 9), time_width=0.6),
                      VShowPassingFlash(loop_path(sch).set_stroke(YELLOW, 9), time_width=0.6),
                      FlashAround(sch.b1, run_time=1.8, time_width=1.5),
                      run_time=1.8)
            c.wait_until("ffs")

            self.play(VShowPassingFlash(wire_line(sch.d_w).set_stroke(YELLOW, 9), time_width=0.6),
                      FlashAround(sch.ff.box, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("one clock signal")

            self.play(VShowPassingFlash(sch.clk_w.copy().set_stroke(YELLOW, 10), time_width=0.8),
                      FlashAround(sch.clk, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("loop")

            self.play(VShowPassingFlash(loop_path(sch).set_stroke(GREEN, 11), time_width=0.5,
                                        rate_func=linear),
                      time_span(FlashAround(sch.cs, time_width=1.5, color=GREEN), 0.6, 2.2),
                      run_time=2.2)
            c.wait_until("outlogic")

            self.play(FlashAround(sch.b2, run_time=1.5, time_width=1.5), run_time=1.5)
            self.play(VShowPassingFlash(wire_line(sch.out_w).set_stroke(YELLOW, 9), time_width=0.8),
                      FlashAround(sch.outp, run_time=1.2, time_width=1.5),
                      run_time=max(0.5, min(1.2, c.remaining)))

    # ------------------------------------------------------------ c2: two kinds of thing; labs
    def clip2(self):
        sch = self.sch
        with self.say("c4.needs.2") as c:
            br = two_brackets(sch)
            c.wait_until("comb")
            self.play(*[GrowFromCenter(b) for b in br.comb_braces],
                      *appear(*br.comb_labels, lag=0.15),
                      run_time=max(0.6, min(0.9, c.until("dtype"))))
            c.wait_until("dtype")
            self.play(GrowFromCenter(br.ff_brace), *appear(br.ff_label), run_time=1.0)
            settle(self, br)
            c.wait_until("discrete")

            # the schematic (and its brackets) shrinks to the top
            thumb = VGroup(sch, br)
            self.thumb = thumb
            labs = T("in the labs", 30, DIM).move_to(_p(0.075, -2.75))   # centred under both tags
            self.labs = labs
            self.play(thumb.animate.scale(0.5).move_to(_p(0, 1.9)), *appear(labs), run_time=1.5)

            # three separate chips, wired gate by gate
            S1 = load_scene("ch4_s1_hook")
            A = S1.three_wired()
            A.scale(0.55).move_to(_p(-3.45, -0.75))
            pkgs, wires = A.pkgs, list(A.wires)
            for pk in pkgs:                      # part numbers back at a readable size after the shrink
                lab = T(pk.lab.text, 24, DIM).move_to(pk.body)
                pk.remove(pk.lab)
                pk.add(lab)
                pk.lab = lab
            self.play(*appear(*pkgs, shift=None, lag=0.25), run_time=1.2)
            sep = T("separate chips", 32).move_to(_p(-3.45, -2.15))
            c.wait_until(own_word=sep)
            self.play(*appear(sep), run_time=0.9)
            c.wait_until("wired up")
            self.play(*[Create(w) for w in wires], run_time=1.4)
            self.left_side = [*pkgs, sep, *wires]
            c.wait_until("prog")

            # one programmable device
            M = S1.merged_package()
            M.scale(0.45).shift(_p(3.6, -0.75) - M.chip.body.get_center())
            big, q = M.chip, M.q
            self.play(*appear(big, q, shift=None, lag=0.2), run_time=0.8)
            prog = T("programmable device", 32).move_to(_p(3.6, -2.15))
            c.wait_until(own_word=prog)
            self.play(*appear(prog), run_time=0.8)
            c.wait_until("whose logic")
            grid = face_grid(big)
            self.play(*swap(q, grid), run_time=max(0.6, min(1.2, c.remaining - 0.1)))
            self.right_side = [big, grid, prog, self.labs]

    # ------------------------------------------------------------ c3: p. 156's slide, PLA
    def clip3(self):
        thumb = self.thumb
        with self.say("c4.needs.3") as c:
            title = T("Implementation of FSMs", 48).move_to(_p(0, 3.2))
            gone = self.left_side + self.right_side
            c.wait_until("earlier")
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during([thumb.animate.move_to(_p(0, -2.0))], 0.4, 0.85),
                      *during(appear(title), 0.6, 1.0),  # early: the slide's title, read as the voice names it
                      run_time=1.6)
            tag = T("pp. 71–73: an earlier lecture, not in our series", 30, DIM).move_to(_p(0, 2.5))
            c.wait_until("outside")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("quote")

            quote = T("We saw previously that programmable logic\n"
                      "can be used to implement combinational\n"
                      "logic circuits, i.e., using PLA devices", 34, line_spacing=0.95,
                      t2c={"PLA": YELLOW})
            quote.move_to(_p(-1.6, 1.0))
            dot = T("•", 34).next_to(quote, LEFT, buff=0.25).align_to(quote, UP).shift(0.05 * DOWN)
            self.play(*appear(dot, quote, shift=None, lag=0.1),  # early: the bullet is quoted whole
                      run_time=1.2)
            pla = select(quote, "PLA")[0]
            c.wait_until("P-L-A chips")
            self.play(FlashUnder(pla, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("add")

            plus = T("+", 56, YELLOW).move_to(_p(3.6, 1.0))
            ff_big = dff(w=1.4, h=2.0).scale(0.7).move_to(_p(5.0, 1.0))
            # the thumbnail's flip-flop is ringed while the full one (D, Q, Q-bar on) drops in beside
            # the +; a fly would cross the quote or the thumbnail's text on any path
            self.play(FlashAround(self.sch.ff, run_time=1.5, time_width=1.5),
                      *appear(plus, ff_big, shift=None, lag=0.3), run_time=1.5)
            c.wait_until("state machine")
            self.play(FlashAround(thumb, run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("remind")

            final = handover_shot()
            target = final[0]
            rest = [m for m in self.mobjects]
            self.play(*during(disappear(*rest), 0, 0.4),
                      *during(fly(pla, target), 0.3, 1.0),
                      run_time=min(2.0, c.until(None)))
            self.remove(*[m for m in self.mobjects if m is not target])
            self.add(target)
