"""Chapter 5, scene 2: blocks, wires and switches: the Spartan array. Clips c5.array.1 – c5.array.4.
Opens on ch5_s1_hook.handover_shot() (8 x 6 DIM tile grid, "?", "your circuit?"); the grid settles
into the 4 x 4 CLB array. Ends on an empty frame.

Shared (load_scene("ch5_s2_array")):
  ARRAY_C = (1.8, -0.33)    where this scene draws the array (left zone x < -1.9 holds the insets).
  spartan_array(center=ARRAY_C, with_routes=False)
                           p. 159's simplified schematic: 4 x 4 CLBs (TEAL square 0.8, stroke 3, BG fill,
                           "CLB" T 28) at pitch 1.3; DIM routing channels (3 parallel lines each) between
                           the rows and columns; 3 x 3 PURPLE switch matrices (0.48 square, "SM" T 28) at
                           the crossings; 16 IOBs (DIM 0.75 x 0.4 rectangles, "IOB" T 28 DIM, rotated on
                           the left/right sides) round the edge with FG pin stubs outward.
                           Whole drawing 6.34 x 6.34 (x -1.37..4.97, y -3.50..2.84 at ARRAY_C).
                           .clbs (row-major, row 0 top; each .box .label) .clb(r, c)
                           .sms (each .box .label) .sm(r, c)  (SM(r, c) sits below-right of CLB(r, c))
                           .iobs (top L->R, right T->B, bottom L->R, left T->B; each .box .label .stub .side)
                           .iob(side, k) with side in "top right bottom left"
                           .channels (VGroup) .hchan[k] .vchan[k] (k = 0..2, each a VGroup of 3 Lines)
                           .routes: VGroup of the two GOLD routes (stroke 5): routes[0] CLB(1,0) -> SM(1,0)
                           -> CLB(1,2); routes[1] CLB(0,1) -> SM(0,2) -> CLB(3,2). Only part of the
                           returned group when with_routes=True. z: channels 0, routes 1, SM/CLB 2.
  INSET_CLB = (1, 0)       the CLB this scene opens into an inset (a good one for s4's zoom).
  switch_inset(center, side=2.1)  the "Programmable Switch Matrix" inset: PURPLE box, 4 x 4 DIM wire mesh,
                           a circle at every crossing (ON ones GOLD-filled). .box .wires .circles .on .off
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


ARRAY_C = (1.8, -0.33)
PITCH = 1.3
CLB_S = 0.8
SM_S = 0.48
IOB_L, IOB_T, IOB_GAP, STUB = 0.75, 0.4, 0.22, 0.18
INSET_CLB = (1, 0)
ON = {(0, 1), (1, 3), (2, 0), (3, 2)}
LEFT_X = -4.275   # centre of the left zone


# ---------------------------------------------------------------- the Spartan array

def spartan_array(center=ARRAY_C, with_routes=False):
    cx, cy = center
    half = 1.5 * PITCH + CLB_S / 2
    ext = half + IOB_GAP

    def cxy(r, c):
        return _p(cx + (c - 1.5) * PITCH, cy + (1.5 - r) * PITCH)

    clbs = []
    for r in range(4):
        for c in range(4):
            box = Square(side_length=CLB_S).set_stroke(TEAL, 3).set_fill(BG, 1).move_to(cxy(r, c))
            lab = T("CLB", 28).move_to(box)
            g = VGroup(box, lab)
            g.box, g.label = box, lab
            g.set_z_index(2)
            clbs.append(g)

    hchan, vchan = [], []
    for k in range(3):
        y = cy + (1 - k) * PITCH
        hchan.append(VGroup(*[Line(_p(cx - ext, y + d), _p(cx + ext, y + d)).set_stroke(DIM, 1.5)
                              for d in (-0.12, 0, 0.12)]))
        x = cx + (k - 1) * PITCH
        vchan.append(VGroup(*[Line(_p(x + d, cy + ext), _p(x + d, cy - ext)).set_stroke(DIM, 1.5)
                              for d in (-0.12, 0, 0.12)]))
    channels = VGroup(*hchan, *vchan)
    channels.hchan, channels.vchan = hchan, vchan

    sms = []
    for r in range(3):
        for c in range(3):
            box = Square(side_length=SM_S).set_stroke(PURPLE, 3).set_fill(BG, 1)
            box.move_to(_p(cx + (c - 1) * PITCH, cy + (1 - r) * PITCH))
            lab = T("SM", 28, PURPLE).move_to(box)
            g = VGroup(box, lab)
            g.box, g.label = box, lab
            g.set_z_index(2)
            sms.append(g)

    iobs = []
    mid = ext + IOB_T / 2
    for side in ("top", "right", "bottom", "left"):
        for k in range(4):
            off = (k - 1.5) * PITCH
            if side in ("top", "bottom"):
                sgn = 1 if side == "top" else -1
                pos = _p(cx + off, cy + sgn * mid)
                box = Rectangle(width=IOB_L, height=IOB_T)
                lab = T("IOB", 28, DIM)
                a = pos + sgn * _p(0, IOB_T / 2)
                b = a + sgn * _p(0, STUB)
            else:
                sgn = 1 if side == "right" else -1
                pos = _p(cx + sgn * mid, cy - off)
                box = Rectangle(width=IOB_T, height=IOB_L)
                lab = T("IOB", 28, DIM).rotate(-sgn * PI / 2)
                a = pos + sgn * _p(IOB_T / 2, 0)
                b = a + sgn * _p(STUB, 0)
            box.set_stroke(DIM, 2.5).set_fill(BG, 0).move_to(pos)
            lab.move_to(pos)
            stub = Line(a, b).set_stroke(FG, 3)
            g = VGroup(stub, box, lab)
            g.box, g.label, g.stub, g.side = box, lab, stub, side
            iobs.append(g)

    def route(pts):
        return VMobject().set_points_as_corners([_p(cx + x, cy + y) for x, y in pts]).set_stroke(GOLD, 5)

    h = CLB_S / 2
    # CLB(1,0) right edge -> down the first vertical channel -> SM(1,0) -> along the middle channel -> CLB(1,2)
    r1 = route([(-1.5 * PITCH + h, 0.5 * PITCH), (-PITCH, 0.5 * PITCH), (-PITCH, 0),
                (0.5 * PITCH, 0), (0.5 * PITCH, 0.5 * PITCH - h)])
    # CLB(0,1) bottom -> top channel -> SM(0,2) -> down the last vertical channel -> CLB(3,2)
    r2 = route([(-0.5 * PITCH, 1.5 * PITCH - h), (-0.5 * PITCH, PITCH), (PITCH, PITCH),
                (PITCH, -1.5 * PITCH), (0.5 * PITCH + h, -1.5 * PITCH)])
    routes = VGroup(r1, r2).set_z_index(1)

    g = VGroup(channels, *sms, *clbs, *iobs)
    if with_routes:
        g.add(routes)
    g.clbs, g.sms, g.iobs, g.channels, g.routes = clbs, sms, iobs, channels, routes
    g.clb = lambda r, c: clbs[r * 4 + c]
    g.sm = lambda r, c: sms[r * 3 + c]
    sides = ("top", "right", "bottom", "left")
    g.iob = lambda side, k: iobs[sides.index(side) * 4 + k]
    return g


def switch_inset(center=(LEFT_X, 1.95), side=2.1):
    c = _p(*center)
    box = Square(side_length=side).set_stroke(PURPLE, 3).set_fill(BG, 1).move_to(c)
    offs = [-0.75, -0.25, 0.25, 0.75]
    s = side / 2.1
    wires = VGroup()
    for o in offs:
        wires.add(Line(c + _p(-side / 2, o * s), c + _p(side / 2, o * s)).set_stroke(DIM, 2))
        wires.add(Line(c + _p(o * s, -side / 2), c + _p(o * s, side / 2)).set_stroke(DIM, 2))
    circles, on, off = {}, [], []
    for i, oy in enumerate(reversed(offs)):
        for j, ox in enumerate(offs):
            dot = Circle(radius=0.1 * s).set_stroke(FG, 2.5).set_fill(BG, 1).move_to(c + _p(ox * s, oy * s))
            if (i, j) in ON:
                dot.set_fill(GOLD, 1).set_stroke(GOLD, 2.5)
                on.append(dot)
            else:
                off.append(dot)
            circles[(i, j)] = dot
    g = VGroup(box, wires, *circles.values())
    g.box, g.wires, g.circles, g.on, g.off = box, wires, circles, on, off
    return g


# ---------------------------------------------------------------- icons

def lut_icon():
    bits = ["0110", "1000"]
    g = VGroup()
    for r, row in enumerate(bits):
        for c, b in enumerate(row):
            pos = _p((c - 1.5) * 0.32, (0.5 - r) * 0.32)
            g.add(Square(side_length=0.32).set_stroke(DIM, 1.5).move_to(pos))
            g.add(T(b, 28, GREEN if b == "1" else DIM).move_to(pos))
    return g


def mux_icon():
    body = Polygon(_p(-0.3, 0.5), _p(0.3, 0.25), _p(0.3, -0.25), _p(-0.3, -0.5)).set_stroke(FG, 3)
    ins = VGroup(*[Line(_p(-0.6, y), _p(-0.3, y)) for y in (0.25, -0.25)])
    out = Line(_p(0.3, 0), _p(0.6, 0))
    sel = Line(_p(0, -0.38), _p(0, -0.62))
    VGroup(ins, out).set_stroke(FG, 3)
    sel.set_stroke(YELLOW, 3)
    return VGroup(ins, out, sel, body)


def ff_icon():
    try:
        ff = load_scene("ch4_s4_gla").L6.make_ff()
        ff.remove(ff.d_l, ff.q_l, ff.qb_l)
    except Exception:  # noqa: BLE001  (fallback: a plain clocked box)
        box = Rectangle(width=1.5, height=2.6).set_stroke(FG, 4)
        tri = Polygon(_p(-0.17, -1.3), _p(0.17, -1.3), _p(0, -1.04)).set_stroke(FG, 3)
        ff = VGroup(box, tri)
    return ff.scale_to_fit_height(1.1)


def lamp(center):
    c = _p(*center)
    glow = Circle(radius=0.55).set_stroke(width=0).set_fill(YELLOW, 0.22).move_to(c)
    bulb = Circle(radius=0.3).set_stroke(FG, 3).set_fill(BG, 1).move_to(c)
    fil = VMobject().set_points_as_corners([c + _p(x, y) for x, y in
                                            [(-0.15, -0.05), (-0.08, 0.1), (0, -0.05), (0.08, 0.1), (0.15, -0.05)]])
    fil.set_stroke(FG, 2.5)
    g = VGroup(bulb, fil)
    g.bulb, g.fil, g.glow = bulb, fil, glow
    return g


# ---------------------------------------------------------------- the scene

class Array(NarratedScene):
    def construct(self):
        shot = load_scene("ch5_s1_hook").handover_shot()
        self.add(shot.grid.wires, *shot.grid.tiles, shot.q, shot.tag)
        self.shot = shot
        self.arr = spartan_array()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c5.array.1: the CLB array
    def clip1(self):
        shot, arr = self.shot, self.arr
        grid = shot.grid
        boxes = [cl.box for cl in arr.clbs]
        for b in boxes:
            b.set_stroke(DIM, 2.5)
        moved, gone = [], []
        for r in range(grid.rows):
            for col in range(grid.cols):
                t = grid.tile(r, col)
                if 1 <= r <= 4 and 2 <= col <= 5:
                    moved.append(ReplacementTransform(t, arr.clb(r - 1, col - 2).box))
                else:
                    gone.append(FadeOut(t))
        heading = T("FPGA – Xilinx Spartan", 44).move_to(_p(ARRAY_C[0], 3.22))
        self.heading = heading
        with self.say("c5.array.1") as c:
            self.play(*during(disappear(shot.q, shot.tag), 0, 0.4),
                      *during(gone + [FadeOut(grid.wires)], 0.1, 0.55),
                      *during(moved, 0.25, 0.85),
                      *during(appear(heading), 0.6, 1.0),
                      run_time=min(2.4, c.until("clbs")))  # early: the heading is a title
            c.wait_until("clbs")
            anims = []
            for i, cl in enumerate(arr.clbs):
                s = i * 0.09
                anims.append(time_span(cl.box.animate.set_stroke(TEAL, 3), s, s + 0.6))
                anims.append(time_span(FadeIn(cl.label, shift=0.1 * DOWN), s + 0.1, s + 0.7))
            self.play(*anims, run_time=2.05)
            tag = T("all identical,\nall programmable", 34).move_to(_p(LEFT_X, 2.4))
            c.wait_until(own_word=tag)
            self.play(*flash(boxes, color=TEAL), *appear(tag), run_time=1.5)

            c.wait_until("inside")
            src = arr.clb(*INSET_CLB).box
            ibox = Rectangle(width=4.65, height=4.5).set_stroke(TEAL, 3).set_fill(BG, 1).move_to(_p(LEFT_X, -0.95))
            call = VGroup(Line(src.get_corner(UL), ibox.get_corner(UR)),
                          Line(src.get_corner(DL), ibox.get_corner(DR))).set_stroke(DIM, 2)
            self.play(src.animate.set_stroke(YELLOW, 3), ReplacementTransform(src.copy(), ibox),
                      *during([Create(call)], 0.3, 1.0), run_time=min(1.2, c.until("lookup tables")))
            rows = []
            for k, (icon, name) in enumerate([(lut_icon(), "lookup tables"), (mux_icon(), "multiplexers"),
                                               (ff_icon(), "D flip-flops")]):
                y = 0.55 - 1.5 * k
                icon.move_to(_p(-5.75, y))
                lab = T(name, 30).move_to(_p(-4.85, y), aligned_edge=LEFT)
                lab.align_to(_p(-4.85, 0), LEFT)
                rows.append((icon, lab))
            cues = ["lookup tables", "multiplexers", "flip-flops", "the parts"]
            for k, (icon, lab) in enumerate(rows):
                c.wait_until(cues[k])
                self.play(*appear(icon, lab, lag=0.2), run_time=min(1.0, 0.85 * c.until(cues[k + 1])))
        self.fold = (src, ibox, call, tag, [m for row in rows for m in row])

    # ---- c5.array.2: channels, switch matrices, routes
    def clip2(self):
        arr = self.arr
        lines = [ln for ch in arr.channels for ln in ch]
        # until the IOBs arrive (clip3) the channels stop at the outer blocks' edges: no stubs sticking out
        self.full_lines = [ln.copy() for ln in lines]
        half = 1.5 * PITCH + CLB_S / 2
        cx, cy = ARRAY_C
        for ln in arr.channels.hchan:
            for l in ln:
                l.put_start_and_end_on(_p(cx - half, l.get_y()), _p(cx + half, l.get_y()))
        for ln in arr.channels.vchan:
            for l in ln:
                l.put_start_and_end_on(_p(l.get_x(), cy + half), _p(l.get_x(), cy - half))
        ych = arr.channels.hchan[2][1].get_y()
        rlab = T("routing channels", 32).move_to(_p(LEFT_X - 0.3, ych))
        rarrow = Arrow(rlab.get_right() + 0.1 * RIGHT, _p(cx - half + 0.3, ych), buff=0, stroke_width=3,
                       max_tip_length_to_length_ratio=0.12).set_color(DIM)
        with self.say("c5.array.2") as c:
            src, ibox, call, tag, parts = self.fold
            back = src.copy().set_stroke(TEAL, 3)
            self.play(*during(disappear(*parts, call, tag), 0, 0.3),
                      *during([ReplacementTransform(ibox, back), src.animate.set_stroke(TEAL, 3)], 0.2, 0.55),
                      *[time_span(Create(ln), 1.0 + i * 0.06, 1.8 + i * 0.06) for i, ln in enumerate(lines)],
                      run_time=1.8 + 0.06 * 17)
            self.remove(back)
            c.wait_until(own_word=rlab)
            self.play(*appear(rlab), GrowArrow(rarrow), run_time=1.0)

            c.wait_until("sm")
            self.play(*appear(*arr.sms, lag=0.1, shift=None), run_time=1.5)

            c.wait_until("inset")
            sm = arr.sm(1, 0)
            ins = switch_inset()
            self.ins = ins
            on_fill = [d for d in ins.on]
            for d in on_fill:
                d.set_fill(BG, 1).set_stroke(FG, 2.5)
            self.play(sm.box.animate.set_stroke(YELLOW, 3), ReplacementTransform(sm.box.copy(), ins.box),
                      *during([FadeIn(ins.wires), *[FadeIn(d) for d in ins.circles.values()]], 0.55, 1.0),
                      run_time=1.6)
            c.wait_until("join")
            self.play(*[d.animate.set_fill(GOLD, 1).set_stroke(GOLD, 2.5) for d in on_fill], run_time=1.0)
            slab = T("Programmable\nSwitch Matrix", 30).move_to(_p(LEFT_X, 0.4))
            self.slab = slab
            c.wait_until(own_word=slab)
            self.play(*appear(slab), run_time=1.0)

            c.wait_until("route")
            r1, r2 = arr.routes
            self.play(Create(r1, rate_func=linear),
                      time_span(FlashAround(sm.box, color=GOLD, time_width=1.5, buff=0.15), 0.5, 1.5),
                      time_span(FlashAround(ins.circles[(2, 0)], color=GOLD, time_width=1.5), 0.5, 1.5),
                      run_time=min(2.0, c.until("reach")))
            c.wait_until("reach")
            self.play(Create(r2, rate_func=linear),
                      time_span(FlashAround(arr.sm(0, 2).box, color=GOLD, time_width=1.5, buff=0.15), 0.4, 1.2),
                      run_time=min(1.5, c.until("programmable blocks")))
            c.wait_until("programmable blocks")
            self.play(*flash([cl.box for cl in arr.clbs], color=TEAL), run_time=1.2)
            c.wait_until("programmable switches")
            self.play(*flash([s.box for s in arr.sms], color=PURPLE, buff=0.15), run_time=1.2)
        self.rlab, self.rarrow = rlab, rarrow

    # ---- c5.array.3: the IOBs
    def clip3(self):
        arr = self.arr
        iob = arr.iob("left", 2)
        ibox = Rectangle(width=2.8, height=1.7).set_stroke(YELLOW, 3).set_fill(BG, 1).move_to(_p(-4.0, -1.85))
        call = VGroup(Line(iob.box.get_corner(UL), ibox.get_corner(UR)),
                      Line(iob.box.get_corner(DL), ibox.get_corner(DR))).set_stroke(DIM, 2)
        cy = -1.85
        tri = Polygon(_p(-3.35, cy + 0.6), _p(-3.35, cy - 0.6), _p(-4.65, cy)).set_stroke(FG, 4).set_fill(BG, 1)
        w_in = Line(_p(-2.6, cy), _p(-3.35, cy)).set_stroke(FG, 3)
        w_out = Line(_p(-4.65, cy), _p(-5.75, cy)).set_stroke(FG, 3)
        lmp = lamp((-6.05, cy))
        big = T("big transistors", 34, YELLOW).move_to(_p(-4.0, -3.2))
        logic = T("the logic is\nin the blocks", 36, TEAL).move_to(_p(LEFT_X, -1.9))
        self.logic = logic
        with self.say("c5.array.3") as c:
            self.play(*during(disappear(self.rlab, self.rarrow), 0, 0.4),
                      *during([Transform(ln, full) for ln, full in
                               zip([ln for ch in arr.channels for ln in ch], self.full_lines)], 0.1, 0.5),
                      *during(appear(*arr.iobs, lag=0.06, shift=None), 0.2, 1.0), run_time=2.2)
            c.wait_until("big")
            self.play(restyle(iob.box, outline=YELLOW), ReplacementTransform(iob.box.copy(), ibox),
                      *during([Create(call)], 0.2, 0.7),
                      *during([FadeIn(tri), FadeIn(w_in), FadeIn(w_out), FadeIn(lmp)], 0.55, 1.0),
                      run_time=1.6)
            c.wait_until(own_word=big)
            self.play(*appear(big), run_time=1.0)
            c.wait_until("drive")
            self.play(w_out.animate.set_stroke(YELLOW, 4), w_in.animate.set_stroke(YELLOW, 4),
                      lmp.bulb.animate.set_fill(YELLOW, 1), lmp.fil.animate.set_stroke(BG, 2.5),
                      FadeIn(lmp.glow), run_time=1.0)
            c.wait_until("nologic")
            others = [m for m in arr.iobs if m is not iob]
            self.play(*disappear(ibox, call, tri, w_in, w_out, lmp.bulb, lmp.fil, lmp.glow),
                      *set_alpha(others, 0.4), restyle(iob.box, outline=DIM, op=0.4),
                      restyle(iob.label, op=0.4), restyle(iob.stub, op=0.4), run_time=1.2)
            c.wait_until("all the logic")
            self.play(*[cl.box.animate.set_stroke(TEAL, 5) for cl in arr.clbs],
                      *flash([cl.box for cl in arr.clbs], color=TEAL), *during(disappear(big), 0, 0.4),
                      *during(appear(logic), 0.45, 1.0), run_time=1.8)

    # ---- c5.array.4: configuration
    def clip4(self):
        ins = self.ins
        texts = ["The FPGA is configured", "by specifying the", "contents of the LUTs",
                 "and select signals", "for the MUXs"]
        lines = VGroup(*[T(s, 30) for s in texts]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        lines.move_to(_p(LEFT_X, -2.0))
        luts = select(lines[2], "LUTs")[0]
        muxs = select(lines[4], "MUXs")[0]
        with self.say("c5.array.4") as c:
            c.wait_until("slide")
            self.play(*swap(self.logic, lines), run_time=1.2)  # early: the slide's bullet, quoted whole
            c.wait_until("lookup tables")
            self.play(*recolor(luts, YELLOW), run_time=0.8)
            c.wait_until("multiplexers")
            self.play(*recolor(muxs, YELLOW), run_time=0.8)
            c.wait_until("switches")
            on, off = ins.on, ins.off
            self.play(*[d.animate.set_fill(BG, 1).set_stroke(FG, 2.5) for d in on],
                      *[d.animate.set_fill(GOLD, 1).set_stroke(GOLD, 2.5) for d in off], run_time=0.6)
            self.play(*[d.animate.set_fill(GOLD, 1).set_stroke(GOLD, 2.5) for d in on],
                      *[d.animate.set_fill(BG, 1).set_stroke(FG, 2.5) for d in off], run_time=0.6)
            c.wait_until("first")
            keep = set(id(g) for g in luts)
            self.play(*[g.animate.set_opacity(0) for ln in lines for g in ln if id(g) not in keep],
                      run_time=1.0)
