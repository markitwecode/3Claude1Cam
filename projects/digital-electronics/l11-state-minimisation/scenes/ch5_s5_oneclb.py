"""Chapter 5, scene 5: what one block can do; the synchroniser fits in one CLB. Clips c5.oneclb.1 – c5.oneclb.4.

Opens on ch5_s4_clb.handover_shot() (= clb(programmed=True)); ends on an empty frame.
Everything new is built in s4's own (unscaled) coordinates and mapped onto the screen with a view
(k, centre-of-outline): V1 (clip 1, room for tags on the right), V2 (clip 2, L10's diagram and
equations on the left), V3 (clip 3, routing round the block), V4 (clip 4, small at the right).

Shared (s8 imports these):
- `D0_BITS` "0101110000001100" (same order as ch5_s3_lut.D1_BITS).
- `filled_clb(view=V3)`: the programmed block as this scene leaves it after clip 3: D1 / D0 bits in
  G / F (s3's lut_grid look), D1 / D0 output labels, YQ fed by G and XQ by F (other mux inputs DIM),
  s1 / s0 at YQ / XQ, the unused parts dimmed, and the GOLD routes, PURPLE switch matrix, DIM IOBs,
  BLUE e / r, GREEN output s. VGroup(clb, routes); `.clb` (s4's clb handles + .d_grid {G, F},
  .d_label {G, F}, .s_label {G, F}), `.routes` (.s_wires .e_r .out .sm).
- `recap_shot()` = filled_clb(V3).
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

S4 = load_scene("ch5_s4_clb")
S3 = load_scene("ch5_s3_lut")
_p, wire, jdot = S4._p, S4.wire, S4.jdot

D1_BITS = S3.D1_BITS
D0_BITS = "0101" "1100" "0000" "1100"

O = _p(0.15, 0.25)                    # centre of s4's TEAL outline
V0 = (1.0, (0.15, -0.1))
V1 = (0.72, (-1.0, 0.65))
V2 = (0.72, (1.8, 0.1))
V3 = (0.72, (0.1, 0.5))
V4 = (0.38, (2.96, 0.67))
K = 0.72                              # font sizes of new pieces are divided by this


def to_view(mob, view):
    k, c = view
    return mob.scale(k, about_point=O).shift(np.array([c[0], c[1], 0.0]) - O)


def view_anim(mob, a, b):
    """mob drawn in view a -> view b (one .animate)."""
    (ka, ca), (kb, cb) = a, b
    ca, cb = np.array([*ca, 0.0]), np.array([*cb, 0.0])
    return mob.animate.scale(kb / ka, about_point=ca).shift(cb - ca)


def S(px):                            # an orig-coords font size that reads as px on screen
    return px / K


# ---------------------------------------------------------------- pieces (s4 coordinates)
G_Y = dict(S4.G_PINS)
F_Y = dict(S4.F_PINS)


def d_grid(which):
    bits, y = (D1_BITS, S4.G_OUT) if which == "G" else (D0_BITS, S4.F_OUT)
    g = S3.lut_grid(bits, _p(-4.45, y), cell=0.38, size=S(28))
    g.remove(g.col_heads, g.row_heads)
    g.grid.set_stroke(BLUE, 2.5)
    return g


def d_label(which):
    tex, y = ("D_1", 2.5) if which == "G" else ("D_0", -1.2)
    return MathTex(tex, font_size=S(32), color=BLUE).move_to(_p(-2.75, y))


def s_label(which):
    if which == "G":
        return MathTex("s_1", font_size=S(32), color=GREEN).move_to(_p(6.3, S4.FF1_CY + 0.43 + 0.5))
    return MathTex("s_0", font_size=S(32), color=GREEN).move_to(_p(6.3, -0.15 - 0.5))


def sel_paths(color=FG, width=S4.WW):
    """The two mux inputs chosen: G -> YQ, F -> XQ."""
    gy = wire([(S4.BUS["G"], S4.G_OUT), (S4.BUS["G"], 2.75), (S4.B_X0, 2.75)], color, width)
    fx = wire([(S4.BUS["F"], S4.F_OUT), (S4.BUS["F"], -0.6), (S4.B_X0, -0.6)], color, width)
    return gy, fx


UNSEL = ("h_q", "f_q", "din_q", "g_xq", "h_xq", "din_xq")


def spare_parts(C):
    h, a, b = C.h, C.a, C.b
    W, D = C.w, C.dots
    out = [h.box, h.name, h.grid, h.out_label, *h.in_labels.values(),
           a.box, a.label, a.mux_g, a.mux_f, a.mux_g.tick, a.mux_f.tick,
           b.mux_y, b.mux_x, b.mux_y.tick, b.mux_x.tick]
    out += [W[k] for k in ("g_a", "a_h_g", "f_a", "a_h_f", "h_run", "g_y", "h_y", "f_x", "h_x")]
    for n in ("Y", "X", "H1", "DIN"):
        w, lab = C.pins[n]
        out += [w, lab]
    out += [D[k] for k in ("din", "bus_h", "bus_h_y", "bus_g_y", "bus_h_xq", "bus_din_xq")]
    return out


def dimmed(m, op=0.3):
    for sm in m.family_members_with_points():
        if sm.get_stroke_width() > 0:
            sm.set_stroke(opacity=op * sm.get_stroke_opacity())
        if sm.get_fill_opacity() > 0 and sm.get_fill_color().to_hex().upper() != BG.upper():
            sm.set_fill(opacity=op * sm.get_fill_opacity())
    return m


def iob(x, y):
    box = Rectangle(width=0.95, height=0.55).set_stroke(DIM, 2.5).set_fill(BG, 1).move_to(_p(x, y))
    lab = T("IOB", S(28), DIM).move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def routes(C):
    """GOLD routing outside the block (C in s4 coordinates)."""
    xe = min(C.pins[n][1].get_left()[0] for n in list(G_Y) + list(F_Y) + ["DIN"]) - 0.1
    xq = max(C.pins[n][1].get_right()[0] for n in ("YQ", "XQ")) + 0.1
    yq, xqy = C.b.mux_yq.out_y, C.b.mux_xq.out_y
    gw = 5
    s1 = wire([(xq, yq), (7.5, yq), (7.5, -4.15), (-6.95, -4.15), (-6.95, G_Y["G2"]), (xe, G_Y["G2"])], GOLD, gw)
    s1b = wire([(-6.95, F_Y["F2"]), (xe, F_Y["F2"])], GOLD, gw)
    s0 = wire([(xq, xqy), (7.15, xqy), (7.15, -3.8), (-6.6, -3.8), (-6.6, G_Y["G1"]), (xe, G_Y["G1"])], GOLD, gw)
    s0b = wire([(-6.6, F_Y["F1"]), (xe, F_Y["F1"])], GOLD, gw)
    sdots = VGroup(jdot(-6.95, F_Y["F2"], GOLD), jdot(-6.6, F_Y["F1"], GOLD))
    smb = Square(0.85).set_stroke(PURPLE, 3).set_fill(BG, 1).move_to(_p(0.4, -3.975)).set_z_index(2)
    sml = T("SM", S(28), PURPLE).move_to(smb).set_z_index(2)
    sm = VGroup(smb, sml)
    lab1 = MathTex("s_1", font_size=S(32), color=GREEN).move_to(_p(-5.0, -4.5))
    lab0 = MathTex("s_0", font_size=S(32), color=GREEN).move_to(_p(-5.0, -3.47))
    s_wires = VGroup(s1, s1b, s0, s0b, sdots)

    io_r, io_e = iob(-8.6, 3.5), iob(-8.6, 2.75)
    xr, xe_bus = -7.3, -7.65
    rw = wire([(-8.125, 3.5), (xr, 3.5), (xr, F_Y["F4"]), (xe, F_Y["F4"])], BLUE, 4)
    rg = wire([(xr, G_Y["G4"]), (xe, G_Y["G4"])], BLUE, 4)
    ew = wire([(-8.125, 2.75), (xe_bus, 2.75), (xe_bus, F_Y["F3"]), (xe, F_Y["F3"])], BLUE, 4)
    eg = wire([(xe_bus, G_Y["G3"]), (xe, G_Y["G3"])], BLUE, 4)
    rdots = VGroup(jdot(xr, G_Y["G4"], BLUE), jdot(xe_bus, G_Y["G3"], BLUE))
    r_l = MathTex("r", font_size=S(32), color=BLUE).move_to(_p(-7.72, 3.78))
    e_l = MathTex("e", font_size=S(32), color=BLUE).move_to(_p(-7.9, 2.45))
    e_r = VGroup(io_r, io_e, rw, rg, ew, eg, rdots, r_l, e_l)
    e_r.iobs, e_r.wires, e_r.labels = VGroup(io_r, io_e), VGroup(rw, rg, ew, eg, rdots), VGroup(r_l, e_l)

    ow = wire([(7.5, yq), (8.075, yq)], GOLD, gw)
    odot = jdot(7.5, yq, GOLD)
    io_o = iob(8.55, yq)
    s_l = MathTex("s", font_size=S(34), color=GREEN).move_to(_p(7.8, yq + 0.36))
    out = VGroup(ow, odot, io_o, s_l)
    out.wire, out.dot, out.iob, out.label = ow, odot, io_o, s_l

    R = VGroup(s_wires, sm, lab1, lab0, e_r, out)
    R.s_wires, R.sm, R.s_labels, R.e_r, R.out = s_wires, sm, VGroup(lab1, lab0), e_r, out
    return R


def program(C):
    """Static: s4's block -> this scene's programmed block (in place)."""
    C.d_grid, C.d_label, C.s_label = {}, {}, {}
    for which, t in (("G", C.g), ("F", C.f)):
        C.remove(t.grid)
        grid = d_grid(which)
        t.grid = grid
        C.d_grid[which] = grid
        C.d_label[which] = d_label(which)
        C.s_label[which] = s_label(which)
        C.add(grid, C.d_label[which], C.s_label[which])
    for k in UNSEL:
        C.w[k].set_stroke(DIM)
    C.sel = sel_paths()
    C.add(*C.sel)
    for m in spare_parts(C):
        dimmed(m)
    return C


def filled_clb(view=V3):
    C = program(S4.clb(programmed=True))
    R = routes(C)
    g = VGroup(C, R)
    g.clb, g.routes = C, R
    if view is not None:
        to_view(g, view)
    return g


def recap_shot():
    return filled_clb(V3)


def overlay(w, width=6):
    o = w.copy().set_stroke(YELLOW, width)
    if hasattr(o, "set_fill"):
        o.set_fill(opacity=0)
    return o.set_z_index(4)


def glide(mob, pts, end_width, fade_from=0.6):
    """mob slides along a corner path (screen points), shrinking, and dissolves at the end."""
    start = mob.copy()
    path = VMobject().set_points_as_corners(pts)
    w0 = mob.width

    def upd(m, a):
        s = smooth(a)
        m.become(start)
        m.scale(interpolate(1, end_width / w0, s))
        m.move_to(path.point_from_proportion(s))
        if a > fade_from:
            m.set_opacity(max(0.0, 1 - (a - fade_from) / (1 - fade_from)))

    return UpdateFromAlphaFunc(mob, upd, rate_func=linear, remover=True)


def P(x, y):
    return np.array([x, y, 0.0])


class Ch5S5Oneclb(NarratedScene):
    def construct(self):
        C = S4.handover_shot()
        self.add(C)
        self.C = C
        self.lit, self.lit_labels = [], []
        self.clip1(C)
        self.clip2(C)
        self.clip3(C)
        self.clip4(C)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- lighting helpers
    def light(self, wires=(), labels=()):
        ovs = [overlay(w) for w in wires]
        self.lit += ovs
        anims = [Create(o) for o in ovs]
        for lab in labels:
            self.lit_labels.append((lab, lab.copy()))
            anims.append(lab.animate.set_color(YELLOW))
        return anims

    def unlight(self):
        anims = [FadeOut(o) for o in self.lit]
        anims += [Transform(lab, saved) for lab, saved in self.lit_labels]
        self.lit, self.lit_labels = [], []
        return anims

    @staticmethod
    def row_box(grid, r):
        cell = grid.grid[0].width / 4          # on-screen cell (the grid has been scaled into the view)
        a, b = grid.vals[r][0].get_center(), grid.vals[r][3].get_center()
        return (Rectangle(width=b[0] - a[0] + cell + 0.08, height=cell + 0.06).move_to((a + b) / 2)
                .set_stroke(YELLOW, 3).set_fill(YELLOW, 0.15).set_z_index(3))

    def mk(self, mob, view):
        return to_view(mob, view)

    # ---------------------------------------------------------------- clip 1: what it can do
    def clip1(self, C):
        b = C.b
        cap = VGroup(T("Thus each CLB can perform up to 2 combinational", 32),
                     T("and/or 2 registered functions", 32)).arrange(DOWN, buff=0.14).move_to(P(-1.0, -2.75))
        with self.say("c5.oneclb.1") as c:
            self.play(view_anim(C, V0, V1), *during(appear(cap, shift=None), 0.5, 1),  # early: slide p. 161, read over the line
                      run_time=min(1.6, c.until("combinational")))
            settle(self, C)

            yw, yl = C.pins["Y"]
            xw, xl = C.pins["X"]
            tag_c = T("combinational", 32, YELLOW).next_to(xl, RIGHT, buff=0.3)
            c.wait_until("combinational")
            self.play(*self.light([yw, xw], [yl, xl]), *during(appear(tag_c), 0.3, 1), run_time=1.0)
            settle(self, C)

            yql, xql = C.pins["YQ"][1], C.pins["XQ"][1]
            tag_r = T("registered", 32, YELLOW).next_to(yql, RIGHT, buff=0.3)
            c.wait_until("registered")
            self.play(*self.light([C.ff_y.q_w, C.ff_x.q_w], [yql, xql]), *during(appear(tag_r), 0.3, 1),
                      run_time=1.0)
            settle(self, C)

            # {four}: G1-G4 -> G -> Y
            c.wait_until("four")
            self.play(*self.unlight(), run_time=0.8)
            settle(self, C)
            gpins = [C.pins[n][0] for n in G_Y]
            g_to_y = self.mk(wire([(S4.TAB_X1, S4.G_OUT), (S4.BUS["G"], S4.G_OUT), (S4.BUS["G"], 1.1),
                                   (S4.B_X0, 1.1)]), V1)
            self.play(*self.light(gpins + [C.g.box]), run_time=0.9)
            self.play(*self.light([g_to_y, b.mux_y, yw], [yl]), run_time=1.0)
            settle(self, C)
            four = VGroup(T("at least", 34, YELLOW), T("4 inputs", 34, YELLOW)).arrange(DOWN, buff=0.12)
            four.next_to(yl, RIGHT, buff=0.45)
            c.wait_until("four inputs", own_word=four[0])
            self.play(*appear(four), run_time=0.8)

            # {nine}: both tables through A into H, with H1, then H -> Y
            c.wait_until("nine")
            gy_ov = self.lit.pop(len(gpins) + 1)          # the G -> Y run goes dark
            fpins = [C.pins[n][0] for n in F_Y]
            W = C.w
            self.play(FadeOut(gy_ov), *disappear(tag_c, tag_r),
                      *self.light(fpins + [C.f.box, W["g_a"], W["f_a"], C.a.mux_g, C.a.mux_f, W["a_h_g"], W["a_h_f"],
                                  C.pins["H1"][0], C.h.box, W["h_run"], W["h_y"]],
                                  [C.pins["H1"][1]]),
                      run_time=min(2.0, c.until("as many as nine")))
            settle(self, C)
            total = MathTex("4", "+", "4", "+", "1", "=", "9", font_size=48, color=GOLD)
            total.move_to(four).align_to(four, LEFT)
            c.wait_until("as many as nine")
            self.play(*swap(four, total), run_time=1.2)
            c.wait_until("four plus four")
            self.play(*flash([total[0], total[2], total[4]], color=GOLD), run_time=1.6)

            # {levels}
            lv1 = T("level 1", 34, YELLOW).move_to(P(-1.0 + (-4.3 - 0.15) * K, -2.4))
            lv2 = T("level 2", 34, YELLOW).move_to(P(-1.0 + (-0.05 - 0.15) * K, -2.4))
            c.wait_until("levels")
            self.play(*disappear(cap), run_time=0.7)
            self.play(*appear(lv1), run_time=0.8)
            c.wait_until("feeding a third")
            self.play(*appear(lv2), run_time=0.8)
        self.c1_extra = [total]
        self.levels = [lv1, lv2]

    # ---------------------------------------------------------------- clip 2: the synchroniser fits
    def clip2(self, C):
        L10DG = S3._load_other("l10-state-assignment", "ch5_s3_diagram")
        S6 = load_scene("ch4_s6_sync")
        dg = L10DG.sync_diagram()
        dg.scale_to_fit_width(3.6).move_to(P(-4.8, 0.25))
        eq1 = S6.eq_tex(1, 38).move_to(P(-4.0, 3.3))
        eq0 = S6.eq_tex(0, 38).move_to(P(-4.0, -3.05))
        with self.say("c5.oneclb.2") as c:
            self.play(*self.unlight(), *disappear(*self.c1_extra, *self.levels), run_time=0.7)
            settle(self, C)
            self.play(view_anim(C, V1, V2), run_time=1.3)
            settle(self, C)
            self.play(*appear(eq1, dg, shift=None, lag=0.2), run_time=1.4)  # early: L10's picture shown whole

            # {d1}: D1 -> G
            g_grid = self.mk(d_grid("G"), V2)
            g_lab = self.mk(d_label("G"), V2)
            gc = C.g.box.get_center()
            c.wait_until("d1")
            self.play(*appear(eq0, shift=None), run_time=1.0)  # early: L10's second equation, read a moment later
            c.wait_until("goes in the gee table")
            self.play(glide(eq1, [eq1.get_center(), P(gc[0], 3.3), P(gc[0], 2.85)], 1.2),
                      *during([FadeOut(C.g.grid)], 0.35, 0.6),
                      *during([FadeIn(g_grid)], 0.65, 1), run_time=2.0)
            old = C.g.grid
            C.g.grid = g_grid
            settle(self, C, add=[g_grid], drop=[old])
            c.wait_until("sixteen bits")
            self.play(*appear(g_lab), FlashAround(g_grid, color=YELLOW, time_width=1.5), run_time=1.4)
            settle(self, C, add=[g_lab])

            # {d0}: D0 -> F, rows as they are read
            f_grid = self.mk(d_grid("F"), V2)
            f_lab = self.mk(d_label("F"), V2)
            fc = C.f.box.get_center()
            c.wait_until("d0")
            self.play(glide(eq0, [eq0.get_center(), P(fc[0], -3.05), P(fc[0], -1.85)], 1.1),
                      *during([FadeOut(C.f.grid)], 0.35, 0.6),
                      *during([FadeIn(f_grid), *appear(f_lab)], 0.65, 1), run_time=2.0)
            old = C.f.grid
            C.f.grid = f_grid
            settle(self, C, add=[f_grid, f_lab], drop=[old])
            row_box = None
            for r, (cue, nth) in enumerate((("zero one zero one", 0), ("one one zero zero", 0),
                                            ("four zeros", 0), ("one one zero zero", 1))):
                box = self.row_box(f_grid, r)
                c.wait_until(cue, nth=nth)
                if row_box is None:
                    row_box = box
                    self.play(FadeIn(row_box), run_time=0.8)
                else:
                    self.play(Transform(row_box, box), run_time=0.8)

            # {ffs}: the flip-flop muxes choose G and F
            gy, fx = (self.mk(w, V2) for w in sel_paths(YELLOW, 6))
            gy.set_z_index(4)
            fx.set_z_index(4)
            c.wait_until("ffs")
            self.play(Create(gy), FadeOut(row_box), *[C.w[k].animate.set_stroke(DIM) for k in UNSEL[:3]],
                      run_time=1.2)
            settle(self, C)
            s1 = self.mk(s_label("G"), V2)
            c.wait_until("holds S one")
            self.play(*appear(s1), run_time=0.9)
            c.wait_until("after the eff table")
            self.play(Create(fx), *[C.w[k].animate.set_stroke(DIM) for k in UNSEL[3:]], run_time=1.2)
            settle(self, C)
            s0 = self.mk(s_label("F"), V2)
            c.wait_until("holds S zero")
            self.play(*appear(s0), run_time=0.9)
            settle(self, C, add=[s1, s0])
        self.dg, self.sel = dg, (gy, fx)

    # ---------------------------------------------------------------- clip 3: routing
    def clip3(self, C):
        gy, fx = self.sel
        R0 = S4.clb(programmed=True)
        R = to_view(routes(R0), V3)
        self.R = R
        with self.say("c5.oneclb.3") as c:
            self.play(*during(disappear(self.dg), 0, 0.4),
                      *during([view_anim(C, V2, V3), view_anim(gy, V2, V3), view_anim(fx, V2, V3)], 0.3, 1),
                      run_time=1.5)
            self.play(gy.animate.set_stroke(FG, S4.WW), fx.animate.set_stroke(FG, S4.WW), run_time=0.8)
            gy.set_z_index(0)
            fx.set_z_index(0)
            settle(self, C, add=[gy, fx])
            C.sel = (gy, fx)

            c.wait_until("out of the block")
            sw = R.s_wires
            self.play(*[Create(w) for w in sw[:4]], FadeIn(R.sm), FadeIn(sw[4]),
                      run_time=min(2.0, c.until("back into both")))
            c.wait_until("back into both")
            self.play(*appear(*R.s_labels, lag=0.3), run_time=1.0)
            c.wait_until("beside the inputs")
            er = R.e_r
            self.play(FadeIn(er.iobs), *[Create(w) for w in er.wires], *during(appear(*er.labels), 0.5, 1),
                      run_time=min(1.5, c.until("out")))

            # {out}
            o = R.out
            c.wait_until("out")
            self.play(FadeIn(o.dot), Create(o.wire), *during([FadeIn(o.iob)], 0.4, 1), run_time=1.2)
            c.wait_until("ess")
            self.play(*appear(o.label), FlashAround(C.pins["YQ"][1], color=GREEN, time_width=1.5), run_time=1.2)
            self.remove(*R.get_family())
            self.add(R)

            # {spare}
            c.wait_until("spare")
            parts = spare_parts(C)
            self.play(*[Transform(m, dimmed(m.copy())) for m in parts], run_time=1.5)
            settle(self, C)

    # ---------------------------------------------------------------- clip 4: compare, then the grid
    def clip4(self, C):
        R = self.R
        gal, gtag = load_scene("ch5_s1_hook").gal_and_tag()
        gal.scale_to_fit_width(4.6).move_to(P(-3.85, 0.45))
        gtag.scale(30 / 34).move_to(P(-3.85, -1.95))
        ctag = T("2 × 16 bits · 2 flip-flops", 30, GOLD).move_to(P(2.9, -1.95))
        nosimp = T("no simplifying", 32, GREEN).move_to(P(2.9, -2.7))
        with self.say("c5.oneclb.4") as c:
            self.play(view_anim(C, V3, V4), view_anim(R, V3, V4), *during([FadeIn(gal)], 0.45, 1), run_time=1.8)
            c.wait_until("five and gates")
            self.play(*appear(gtag), run_time=1.0)  # early: the GAL's count, read across the line

            c.wait_until("bits")
            gates = list(getattr(getattr(gal, "ands", None), "gates", [])) or [gal]
            self.play(*flash(gates, color=YELLOW, time_width=1.5), run_time=1.2)
            self.play(*appear(ctag), *flash([C.g.grid, C.f.grid], color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("nothing to simplify")
            self.play(*appear(nosimp), run_time=1.0)

            # {grid}: back into the array
            arr = load_scene("ch5_s2_array").spartan_array(center=(0, 0.1))
            tile = arr.clb(1, 0)
            tc = tile.get_center()
            Vt = (0.8 / 11.6, (tc[0], tc[1]))
            c.wait_until("grid")
            self.play(FlashAround(C.outline, color=TEAL, time_width=1.5), run_time=1.4)
            c.wait_until("the chip has")
            self.play(*during(disappear(gal, gtag, ctag, nosimp, R), 0, 0.4),
                      *during([view_anim(C, V4, Vt)], 0.3, 1), run_time=1.8)
            rest = [m for m in arr.submobjects if m is not tile]
            self.play(*during([FadeOut(C)], 0, 0.45), *during([FadeIn(tile)], 0.45, 1),
                      *during([FadeIn(VGroup(*rest))], 0.3, 1), run_time=1.4)
            self.remove(*arr.get_family())
            self.add(arr)
            self.play(tile.box.animate.set_fill(TEAL, 0.35).set_stroke(YELLOW, 5),
                      FlashAround(tile, color=YELLOW, time_width=1.5), run_time=1.2)

            c.wait_until("Wired together")
            self.play(*[Create(r) for r in arr.routes], run_time=min(2.0, c.until("even several")))
