"""Chapter 5, scene 4: the Spartan's logic block (slide p. 160), built piece by piece.
Clips c5.clb.1 – c5.clb.4.

Owns the chapter's CLB drawing: `clb(programmed=True)` returns the whole block as a VGroup with named
parts (see its docstring); `handover_shot()` = clb() as this scene ends (grids in the tables, select
ticks on the muxes, F's output labelled F). s5 opens on it, s8 recaps it.
{open}: s2's spartan_array(with_routes=True) returns; CLB(1, 0) zooms up into the empty outline.
Flip-flops: L6's make_ff (ch6_s7_carry, loaded by path), pins D/CK/EC on the left, SR on top.
"""
# style: 2
# handover: next
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

import lib.paths as _paths  # noqa: E402
from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

_LECTURES = Path(__file__).resolve().parents[2]


def _load_other(folder, stem):
    """A scene file of another lecture; its own load_scene() calls resolve inside that lecture."""
    proj = _LECTURES / folder
    orig = _paths.project
    _paths.project = lambda: proj
    try:
        spec = importlib.util.spec_from_file_location(f"_{folder[:3]}_{stem}", proj / "scenes" / f"{stem}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        _paths.project = orig
    return mod


L6 = _load_other("l06-flip-flops-counters", "ch6_s7_carry")

# ---- geometry (slide p. 160 layout; y values before the global DY shift) ------------------------
DY = -0.35
WW = 3                      # wire stroke
OUT_L, OUT_R, OUT_T, OUT_B = -5.65, 5.95, 3.65, -3.15
TAB_X0, TAB_X1 = -5.3, -3.3
G_PINS = (("G4", 2.75), ("G3", 2.33), ("G2", 1.91), ("G1", 1.49))
F_PINS = (("F4", -0.19), ("F3", -0.61), ("F2", -1.03), ("F1", -1.45))
Y_SR, Y_H1, Y_DIN, Y_K, Y_EC = 1.07, 0.65, 0.23, -2.4, -2.95
G_OUT, F_OUT, H_OUT = 2.12, -0.82, 0.65
H_X0, H_X1, H_Y0, H_Y1 = -1.3, 1.2, -0.15, 1.45
H_IN = {"G": 1.15, "H1": 0.65, "F": 0.15}
J_GF, J_SD = -3.15, -2.85            # junction columns: G/F outputs, SR/DIN pins
A_X0, MUX_W = -2.31, 0.42
B_X0 = 2.64
BUS = {"DIN": 1.55, "G": 1.8, "H": 2.05, "F": 2.3}
SR_BUS, CK_BUS, EC_BUS, SR_TOP, SR_X_Y = 3.35, 3.6, 3.85, 3.5, 0.55
FF_CX, FF_K = 5.075, 0.7
FF1_CY, FF2_CY = 2.18, -0.57
Y_Y, Y_X = 0.95, -1.8
K_DROP, K_RUN = -3.45, -2.7


def _p(x, y):
    return np.array([x, y + DY, 0.0])


def wire(pts, color=FG, width=WW):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


def jdot(x, y, color=FG):
    return Dot(_p(x, y), radius=0.065, color=color)


def mux(x0, ys, w=MUX_W, pad=0.15, slant=0.12):
    """A trapezoid multiplexer (inputs on the tall left side). .ins (points), .out, .tick (select)."""
    top, bot = max(ys) + pad, min(ys) - pad
    m = Polygon(_p(x0, top), _p(x0 + w, top - slant), _p(x0 + w, bot + slant), _p(x0, bot))
    m.set_stroke(FG, 3).set_fill(BG, 1).set_z_index(1)
    m.ins = [_p(x0, y) for y in ys]
    m.out_y = (top + bot) / 2
    m.out = _p(x0 + w, m.out_y)
    xm = x0 + w / 2
    m.tick = Line(_p(xm, bot + slant / 2), _p(xm, bot + slant / 2 - 0.17)).set_stroke(YELLOW, 4)
    return m


def bit_grid(rows, cols, center, cell=0.36, seed=0):
    """DIM placeholder grid of bits: VGroup of cells, each VGroup(square, bit); row-major."""
    rng = np.random.default_rng(seed)
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(cell).set_stroke(DIM, 2)
            b = T(str(int(rng.integers(0, 2))), 28, DIM)
            cells.add(VGroup(sq, b.move_to(sq)).move_to(
                center + np.array([(c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0])))
    return cells


def _lines(*ls, size=28):
    return VGroup(*[T(s, size) for s in ls]).arrange(DOWN, buff=0.1)


def _table(key, x0, x1, y0, y1, out_y, text_lines, rows, cols, name_side, seed):
    t = SimpleNamespace()
    t.box = Rectangle(width=x1 - x0, height=y1 - y0).set_stroke(FG, 4).move_to(_p((x0 + x1) / 2, (y0 + y1) / 2))
    t.name = T(f"{key}-LUT", 36, YELLOW)
    if name_side is UP:
        t.name.next_to(t.box, UP, buff=0.12)
    else:
        t.name.next_to(t.box, DOWN, buff=0.12)
    t.out_label = T(key if key != "H" else "H", 30).move_to(_p(x1 - 0.2, out_y))
    c = _p((x0 + x1) / 2 - 0.15, (y0 + y1) / 2) if key != "H" else _p(0.05, (y0 + y1) / 2)
    t.text = _lines(*text_lines).move_to(c)
    t.grid = bit_grid(rows, cols, c, seed=seed)
    t.out = _p(x1, out_y)
    return t


def _ff(cy):
    f = L6.make_ff(ORIGIN, ins=(("D", 0.6), ("CK", 0.0), ("EC", -0.6)), q_len=0.5)
    f.remove(f.qb_w, f.clk_w, f.tri, *f.labels)
    f.scale(FF_K, about_point=ORIGIN).shift(_p(FF_CX, cy))
    d_w, ck_w, ec_w = f.in_w
    d_w.set_stroke(FG, WW)
    ck_w.set_stroke(YELLOW, WW)
    ec_w.set_stroke(DIM, WW)
    f.q_w.set_stroke(GREEN, WW)
    box = f.box
    labs = []
    for s, w, col in (("D", d_w, BLUE), ("CK", ck_w, YELLOW), ("EC", ec_w, DIM)):
        lab = T(s, 28, col).move_to(w.get_end())
        lab.align_to(box, LEFT).shift(0.08 * RIGHT)
        labs.append(lab)
    q = T("Q", 28, GREEN).move_to(f.q_w.get_start()).align_to(box, RIGHT).shift(0.08 * LEFT)
    sr = T("SR", 28, DIM).next_to(box.get_top(), UP, buff=0.04).shift(0.3 * RIGHT)
    f.add(*labs, q, sr)
    f.d_l, f.ck_l, f.ec_l = labs
    f.q_l, f.sr_l = q, sr
    f.d_w, f.ck_w, f.ec_w = d_w, ck_w, ec_w
    return f


def clb(programmed=True):
    """The Spartan CLB of p. 160. VGroup with named parts:
    .outline (TEAL); .g .f .h tables: .box .name .text .grid (DIM placeholder cells, row-major, each
    VGroup(square, bit); G/F 4x4, H 4 rows x 2) .out_label .out (point); .h.in_labels {G, H1, F};
    .pins {name: (wire, label)} for G4..G1 F4..F1 SR H1 DIN K EC (left) and YQ Y XQ X (right);
    .a (dashed box A): .box .label .mux_g .mux_f; .b (dashed box B): .box .label .mux_yq .mux_y
    .mux_xq .mux_x (each mux: .ins .out .tick); .ff_y .ff_x (make_ff: .box .d_w .ck_w .ec_w .q_w
    .d_l .ck_l .ec_l .q_l .sr_l); .w {wire name: VMobject}; .dots {name: Dot}; .legend; .muxes.
    programmed=True: grids in the tables and select ticks on every mux (this scene's end state);
    False: the slide's "Logic Function of ..." text instead, no ticks (grids/ticks still built)."""
    C = VGroup()
    C.outline = Rectangle(width=OUT_R - OUT_L, height=OUT_T - OUT_B).set_stroke(TEAL, 4)
    C.outline.move_to(_p((OUT_L + OUT_R) / 2, (OUT_T + OUT_B) / 2))
    C.g = _table("G", TAB_X0, TAB_X1, 1.29, 2.95, G_OUT, ("Logic", "Function", "of G1-G4"), 4, 4, UP, 1)
    C.f = _table("F", TAB_X0, TAB_X1, -1.65, 0.01, F_OUT, ("Logic", "Function", "of F1-F4"), 4, 4, DOWN, 2)
    C.h = _table("H", H_X0, H_X1, H_Y0, H_Y1, H_OUT, ("Logic", "Function", "of F-G-H1"), 4, 2, UP, 3)
    C.h.in_labels = {k: T(k, 28).move_to(_p(H_X0, y)).align_to(C.h.box, LEFT).shift(0.08 * RIGHT)
                     for k, y in H_IN.items()}

    # pins
    C.pins = {}
    left = [(n, y, BLUE) for n, y in G_PINS + F_PINS] + [("SR", Y_SR, DIM), ("H1", Y_H1, BLUE),
                                                         ("DIN", Y_DIN, BLUE), ("K", Y_K, YELLOW),
                                                         ("EC", Y_EC, DIM)]
    a_g = mux(A_X0, [1.48, Y_SR])
    a_f = mux(A_X0, [Y_DIN, -0.17])
    ends = {"SR": A_X0, "H1": H_X0, "DIN": A_X0}
    for n, y, col in left:
        lab = T(n, 30, col).next_to(_p(OUT_L, y), LEFT, buff=0.12)
        if n == "K":
            w = wire([(OUT_L, y), (K_DROP, y), (K_DROP, K_RUN), (CK_BUS, K_RUN), (CK_BUS, FF1_CY),
                      (FF_CX - 0.525 - 0.6, FF1_CY)], YELLOW)
        elif n == "EC":
            w = wire([(OUT_L, y), (EC_BUS, y), (EC_BUS, FF1_CY - 0.42), (FF_CX - 0.525 - 0.6, FF1_CY - 0.42)],
                     DIM)
        else:
            w = wire([(OUT_L, y), (ends.get(n, TAB_X0), y)], col)
        C.pins[n] = (w, lab)

    # box A
    C.a = SimpleNamespace(mux_g=a_g, mux_f=a_f)
    C.a.box = DashedVMobject(Rectangle(width=1.0, height=2.28).set_stroke(DIM, 2), num_dashes=28)
    C.a.box.move_to(_p(-2.1, 0.66))
    C.a.label = T("A", 30, DIM).move_to(_p(-1.45, -0.38))

    # box B
    m_yq = mux(B_X0, [3.05, 2.75, 2.45, 2.15])
    m_y = mux(B_X0, [1.1, 0.8])
    m_xq = mux(B_X0, [0.3, 0.0, -0.3, -0.6])
    m_x = mux(B_X0, [-1.65, -1.95])
    C.b = SimpleNamespace(mux_yq=m_yq, mux_y=m_y, mux_xq=m_xq, mux_x=m_x)
    C.b.box = DashedVMobject(Rectangle(width=1.9, height=5.65).set_stroke(DIM, 2), num_dashes=60)
    C.b.box.move_to(_p(2.3, 0.475))
    C.b.label = T("B", 30, DIM).move_to(_p(1.15, 3.15))

    # flip-flops
    C.ff_y = _ff(FF1_CY)
    C.ff_x = _ff(FF2_CY)
    xm = B_X0 + MUX_W
    d_in = FF_CX - 0.525 - 0.6
    for n, y in (("YQ", m_yq.out_y), ("Y", Y_Y), ("XQ", m_xq.out_y), ("X", Y_X)):
        lab = T(n, 30, GREEN).next_to(_p(OUT_R, y), RIGHT, buff=0.12)
        w = wire([(xm, y), (OUT_R, y)], GREEN) if n in ("Y", "X") else None
        C.pins[n] = (w, lab)

    W = {
        "g_a": wire([(TAB_X1, G_OUT), (J_GF, G_OUT), (J_GF, 1.48), (A_X0, 1.48)]),
        "a_h_g": wire([(A_X0 + MUX_W, a_g.out_y), (-1.48, a_g.out_y), (-1.48, H_IN["G"]), (H_X0, H_IN["G"])]),
        "f_a": wire([(TAB_X1, F_OUT), (J_GF, F_OUT), (J_GF, -0.17), (A_X0, -0.17)]),
        "a_h_f": wire([(A_X0 + MUX_W, a_f.out_y), (-1.48, a_f.out_y), (-1.48, H_IN["F"]), (H_X0, H_IN["F"])]),
        "g_run": wire([(J_GF, G_OUT), (BUS["G"], G_OUT)]),
        "h_run": wire([(H_X1, H_OUT), (BUS["H"], H_OUT)]),
        "f_run": wire([(J_GF, F_OUT), (BUS["F"], F_OUT)]),
        "g_y": wire([(BUS["G"], G_OUT), (BUS["G"], 1.1), (B_X0, 1.1)]),
        "h_y": wire([(BUS["H"], H_OUT), (BUS["H"], 0.8), (B_X0, 0.8)]),
        "f_x": wire([(BUS["F"], F_OUT), (BUS["F"], -1.65), (B_X0, -1.65)]),
        "h_x": wire([(BUS["H"], H_OUT), (BUS["H"], -1.95), (B_X0, -1.95)]),
        "g_q": wire([(BUS["G"], G_OUT), (BUS["G"], 2.75), (B_X0, 2.75)]),
        "h_q": wire([(BUS["H"], 0.8), (BUS["H"], 2.45), (B_X0, 2.45)]),
        "f_q": wire([(BUS["F"], F_OUT), (BUS["F"], 2.15), (B_X0, 2.15)]),
        "din_q": wire([(J_SD, Y_DIN), (J_SD, -0.6), (BUS["DIN"], -0.6), (BUS["DIN"], 3.05), (B_X0, 3.05)]),
        "g_xq": wire([(BUS["G"], 1.1), (BUS["G"], 0.0), (B_X0, 0.0)]),
        "h_xq": wire([(BUS["H"], -0.3), (B_X0, -0.3)]),
        "f_xq": wire([(BUS["F"], -0.6), (B_X0, -0.6)]),
        "din_xq": wire([(BUS["DIN"], 0.3), (B_X0, 0.3)]),
        "q_y": wire([(xm, m_yq.out_y), (d_in, m_yq.out_y)]),
        "q_x": wire([(xm, m_xq.out_y), (d_in, m_xq.out_y)]),
        "k_x": wire([(CK_BUS, FF2_CY), (d_in, FF2_CY)], YELLOW),
        "ec_x": wire([(EC_BUS, FF2_CY - 0.42), (d_in, FF2_CY - 0.42)], DIM),
        "sr_y": wire([(J_SD, Y_SR), (J_SD, SR_TOP), (FF_CX, SR_TOP), (FF_CX, FF1_CY + 0.91)], DIM),
        "sr_x": wire([(SR_BUS, SR_TOP), (SR_BUS, SR_X_Y), (FF_CX, SR_X_Y), (FF_CX, FF2_CY + 0.91)], DIM),
    }
    C.w = W
    C.dots = {
        "g": jdot(J_GF, G_OUT), "f": jdot(J_GF, F_OUT), "din": jdot(J_SD, Y_DIN), "sr": jdot(J_SD, Y_SR, DIM),
        "bus_g": jdot(BUS["G"], G_OUT), "bus_g_y": jdot(BUS["G"], 1.1),
        "bus_h": jdot(BUS["H"], H_OUT), "bus_h_y": jdot(BUS["H"], 0.8), "bus_h_xq": jdot(BUS["H"], -0.3),
        "bus_f": jdot(BUS["F"], F_OUT), "bus_f_xq": jdot(BUS["F"], -0.6), "bus_din_xq": jdot(BUS["DIN"], 0.3),
        "k_x": jdot(CK_BUS, FF2_CY, YELLOW), "ec_x": jdot(EC_BUS, FF2_CY - 0.42, DIM),
        "sr_top": jdot(SR_BUS, SR_TOP, DIM),
    }

    # legend
    icon = Polygon(_p(-3.05, -1.7), _p(-2.8, -1.8), _p(-2.8, -2.2), _p(-3.05, -2.3)).set_stroke(FG, 3)
    stubs = VGroup(*[Line(_p(-3.2, y), _p(-3.05, y)).set_stroke(FG, 3) for y in (-1.85, -2.15)])
    txt = VGroup(*[T(s, 28) for s in ("Multiplexer", "Controlled by", "Configuration Program")]).arrange(
        DOWN, buff=0.08, aligned_edge=LEFT)
    txt.next_to(icon, RIGHT, buff=0.2)
    C.legend = VGroup(stubs, icon, txt).shift(0.15 * LEFT)

    C.muxes = [a_g, a_f, m_yq, m_y, m_xq, m_x]

    # assemble (drawing order: wires under boxes, labels on top)
    C.add(C.outline)
    C.add(*W.values())
    C.add(*[w for w, _ in C.pins.values() if w is not None])
    C.add(*C.dots.values())
    for t in (C.g, C.f, C.h):
        C.add(t.box, t.name, t.out_label, t.grid if programmed else t.text)
    C.add(*C.h.in_labels.values())
    C.add(C.a.box, C.a.label, C.b.box, C.b.label, *C.muxes)
    if programmed:
        C.add(*[m.tick for m in C.muxes])
    C.add(C.ff_y, C.ff_x)
    C.add(*[lab for _, lab in C.pins.values()])
    C.add(C.legend)
    return C


def handover_shot():
    return clb(programmed=True)


def _flash(w, color=YELLOW, rt=1.2):
    return VShowPassingFlash(w.copy().set_stroke(color, 7), time_width=0.6, run_time=rt)


class Ch5S4Clb(NarratedScene):
    def construct(self):
        C = clb(programmed=True)
        self.C = C
        self.clip1(C)
        self.clip2(C)
        self.clip3(C)
        self.clip4(C)
        # the finished block, exactly as handover_shot() draws it
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)

    # -------------------------------------------------------------------------------------------
    def clip1(self, C):
        g, f = C.g, C.f
        with self.say("c5.clb.1") as c:
            S2 = load_scene("ch5_s2_array")
            arr = S2.spartan_array(with_routes=True)       # s2's own placement (ARRAY_C), GOLD routes
            self.play(FadeIn(arr), run_time=0.8)
            self.wait(0.4)
            cell = arr.clb(*S2.INSET_CLB)
            tile, tlab = cell.box, cell.label
            cell.remove(tile, tlab)                        # the zooming CLB leaves the array's group
            self.add(tile, tlab)
            zoom_to = C.outline.copy().set_fill(BG, 0)   # fill stays dark while it fades
            self.play(*during(FadeOut(tlab), 0, 0.25), *during(FadeOut(arr), 0, 0.6),
                      ReplacementTransform(tile, zoom_to), run_time=min(1.9, c.until("It has just")))
            self.remove(zoom_to)
            self.add(C.outline)

            logic_w = T("logic", 44, DIM).move_to(_p(-3.4, 0.4))
            ffs_w = T("flip-flops", 44, DIM).move_to(_p(4.0, 0.4))
            c.wait_until("logic to work out", own_word=logic_w)
            self.play(*appear(logic_w))
            c.wait_until("flip-flops to hold", own_word=ffs_w)
            self.play(*appear(ffs_w))

            c.wait_until("g")
            self.play(                      *during([FadeIn(g.box), *appear(g.name, g.out_label)], 0.35, 1),
                      run_time=min(2.0, c.until("The gee table")))
            c.wait_until("inputs")
            gp = [C.pins[n] for n, _ in G_PINS]
            self.play(*[Create(w) for w, _ in gp], *appear(*[lab for _, lab in gp], lag=0.15),
                      run_time=min(1.6, c.until("f")))

            c.wait_until("f")
            fp = [C.pins[n] for n, _ in F_PINS]
            self.play(*during(disappear(logic_w, ffs_w), 0, 0.4),
                      *during([FadeIn(f.box), *appear(f.name, f.out_label)], 0.35, 1), run_time=1.2)
            self.play(*[Create(w) for w, _ in fp], *appear(*[lab for _, lab in fp], lag=0.15),
                      run_time=min(1.3, c.until("each")))

            c.wait_until("each")
            self.play(FadeIn(g.grid), FadeIn(f.grid), run_time=1.0)

    # -------------------------------------------------------------------------------------------
    def clip2(self, C):
        g, f, h = C.g, C.f, C.h
        with self.say("c5.clb.2") as c:
            self.play(*during([FadeIn(h.box), *appear(h.name, *h.in_labels.values(), h.out_label,
                                                      lag=0.1)], 0, 0.6),
                      *during(swap(g.grid, g.text) + swap(f.grid, f.text) + appear(h.text), 0.55, 1),
                      run_time=min(2.6, c.until("hin")))

            c.wait_until("hin")
            direct_g = wire([(TAB_X1, G_OUT), (J_GF, G_OUT), (J_GF, H_IN["G"]), (H_X0, H_IN["G"])])
            direct_f = wire([(TAB_X1, F_OUT), (J_GF, F_OUT), (J_GF, H_IN["F"]), (H_X0, H_IN["F"])])
            self.play(Create(direct_g), Create(direct_f), run_time=1.5)
            c.wait_until("aitch one")
            h1w, h1l = C.pins["H1"]
            self.play(Create(h1w), *appear(h1l), run_time=min(1.2, c.until("amux")))

            c.wait_until("amux")
            a = C.a
            srw, srl = C.pins["SR"]
            dinw, dinl = C.pins["DIN"]
            self.play(FadeIn(a.box), FadeIn(a.mux_g), FadeIn(a.mux_f), FadeIn(a.label),
                      ReplacementTransform(direct_g, VGroup(C.w["g_a"], C.w["a_h_g"])),
                      ReplacementTransform(direct_f, VGroup(C.w["f_a"], C.w["a_h_f"])),
                      run_time=1.6)
            self.play(Create(srw), Create(dinw), *appear(srl, dinl), run_time=1.0)

            c.wait_until("Each passes")
            self.play(_flash(C.w["g_a"]), _flash(C.w["f_a"]), run_time=1.2)
            c.wait_until("or a signal")
            self.play(_flash(srw), _flash(dinw), run_time=1.2)

    # -------------------------------------------------------------------------------------------
    def clip3(self, C):
        b, W, D = C.b, C.w, C.dots
        with self.say("c5.clb.3") as c:
            self.play(FadeIn(b.box), *appear(b.label), run_time=1.0)

            c.wait_until("Output why")
            yw, yl = C.pins["Y"]
            self.play(Create(W["g_run"]), Create(W["g_y"]), Create(W["h_run"]), Create(W["h_y"]),
                      FadeIn(D["g"]), FadeIn(b.mux_y), run_time=1.5)
            self.play(Create(yw), *appear(yl), run_time=1.0)

            c.wait_until("x")
            xw, xl = C.pins["X"]
            self.play(Create(W["f_run"]), Create(W["f_x"]), Create(W["h_x"]), FadeIn(D["f"]), FadeIn(D["bus_h"]),
                      FadeIn(b.mux_x), run_time=1.5)
            self.play(Create(xw), *appear(xl), run_time=1.0)

            c.wait_until("reg")
            self.play(FadeIn(C.ff_y), FadeIn(C.ff_x), run_time=1.5)
            c.wait_until("why-cue")
            self.play(*appear(C.pins["YQ"][1]), run_time=0.8)
            c.wait_until("ex-cue")
            self.play(*appear(C.pins["XQ"][1]), run_time=0.8)

            c.wait_until("din")
            new_w = [W[k] for k in ("g_q", "h_q", "f_q", "din_q", "g_xq", "h_xq", "f_xq", "din_xq",
                                    "q_y", "q_x")]
            new_d = [D[k] for k in ("din", "bus_g", "bus_g_y", "bus_h_y", "bus_h_xq", "bus_f",
                                    "bus_f_xq", "bus_din_xq")]
            self.play(FadeIn(b.mux_yq), FadeIn(b.mux_xq), *[Create(w) for w in new_w],
                      *[FadeIn(d) for d in new_d], run_time=1.6)
            c.wait_until("any of the three")
            self.play(LaggedStart(*[AnimationGroup(_flash(W[a]), _flash(W[bb]))
                                    for a, bb in (("f_q", "f_xq"), ("g_q", "g_xq"), ("h_q", "h_xq"))],
                                  lag_ratio=0.45), run_time=min(1.6, c.until("dee in")))
            c.wait_until("dee in")
            self.play(_flash(W["din_q"]), _flash(W["din_xq"]), run_time=min(1.0, c.until(floor=0.6)))

    # -------------------------------------------------------------------------------------------
    def clip4(self, C):
        W, D = C.w, C.dots
        g, f, h = C.g, C.f, C.h
        with self.say("c5.clb.4") as c:
            kw, kl = C.pins["K"]
            self.play(Create(kw), Create(W["k_x"]), FadeIn(D["k_x"]), *appear(kl), run_time=1.6)

            c.wait_until("Their other")
            ecw, ecl = C.pins["EC"]
            unused = T("not used here", 30, DIM).move_to(_p(-1.05, 3.05))   # under the SR run, clear of H-LUT and B
            self.play(Create(W["sr_y"]), Create(W["sr_x"]), Create(ecw), Create(W["ec_x"]),
                      FadeIn(D["sr"]), FadeIn(D["sr_top"]), FadeIn(D["ec_x"]), *appear(ecl), run_time=1.6)
            self.play(*appear(unused), run_time=1.0)

            c.wait_until("muxes")
            self.play(LaggedStart(*flash(C.muxes), lag_ratio=0.12), run_time=2.0)
            c.wait_until("controlled by")
            self.play(*appear(C.legend), run_time=1.0)  # early: the slide's legend, read as it lands

            c.wait_until("all")
            self.play(*swap(g.text, g.grid), *swap(f.text, f.grid), *swap(h.text, h.grid), run_time=1.5)
            prog = T("all programmable", 30, YELLOW).move_to(_p(-1.15, 3.05))
            c.wait_until("and the choice")
            self.play(*[GrowFromEdge(m.tick, UP) for m in C.muxes], *swap(unused, prog), run_time=1.5)

            c.wait_until("slip")
            self.play(FlashAround(f.out_label, run_time=1.5, time_width=1.5))
            c.wait_until("On the slide")
            wrong = T("G", 30, RED).move_to(f.out_label)
            tag = T("slide p. 160", 28, DIM).move_to(_p(-1.9, -1.1))
            self.play(*swap(f.out_label, wrong), *during(appear(tag), 0.4, 1), run_time=1.4)

            c.wait_until("It should say")
            right = f.out_label.copy()
            tick = check_mark(GREEN).scale(0.7).move_to(_p(-2.75, -1.12))
            self.play(*swap(wrong, right), *swap(tag, tick), run_time=1.4)
        self.play(*disappear(prog, tick), run_time=0.8)
