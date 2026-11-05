"""Chapter 4, scene 4: add flip-flops, feed them back: the GLA. Clips c4.gla.1 – c4.gla.4.

Shared helpers (import with load_scene("ch4_s4_gla")):
- `gla()`: the finished GLA (p. 157, both Q and Q-bar fed back) at its full-frame place, built from
  s3's helpers and L6's make_ff. Handles:
    .bank (input_bank, no labels: .wires .rails .branches .invs .splits .rail_ys), .in_stubs
    .ands (and_row over 10 rails: .gates .lines[g][i] .dots[g][i] .stubs; rails i = 0..3 are the
          state rails q0, q0', q1, q1', i = 4..9 the input rails a, a', b, b', c, c')
    .prods, .ors (.gates .lines[k][j] .dots[k][j]), .orw (OR output wires), .dpath (BLUE, to D)
    .ffs[k] (.box .tri .d_l .q_l .qb_l .d_w .q_w .qb_w), .fb[k] (GREEN feedback, k: Q0, Q0', Q1, Q1'),
    .clk (VGroup: .clk_a .clk_b .jdot), .clk_label, .and_panel, .or_panel,
    .chip (L8's chip(): .body .pins .lab, the "GLA" label in the bottom-left corner)
  The returned VGroup holds every piece. Feedback style (shared with s6): GREEN from Q right, up past
  the top, left, down into a horizontal rail above the input rails; CLK YELLOW from below.
- `final_tag()`: "two programmable planes" in the right column.
- `handover_shot()`: the last frame: gla() + final_tag().
"""
# style: 2
# handover: next
import importlib.util
import sys
from pathlib import Path

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


S3 = load_scene("ch4_s3_plapal")
S2 = load_scene("ch4_s2_needs")
L6 = _load_other("l06-flip-flops-counters", "ch2_s7_recap")
L8 = _load_other("l08-timing-metastability", "ch1_s1_hook")

P = S3.P
poly = S3.poly

# ---------------------------------------------------------------- geometry (s3's local units)
S = 0.62
FULL = S3.Where(S, -5.5, 0.65)
SY = [1.95, 1.5, 1.05, 0.6]          # state rails q0, q0', q1, q1' (above the input rails)
PIN_G = 0.18
GX = [3.2, 5.7]
X_END = 6.95
OY = [-4.75, -5.7]
OR_BACK, OR_L = 7.0, 0.95
OR_TIP = OR_BACK + OR_L
XB = [8.25, 8.55]
FFS = 0.8
X_FF = 10.13
YC = [-1.93, -4.76]
PIN_FF = L6.PIN_Y * FFS
HALF_FF = (L6.BOX_W / 2 + L6.WIRE) * FFS
X_D, X_Q = X_FF - HALF_FF, X_FF + HALF_FF
FF_BOT = [y - L6.BOX_H / 2 * FFS for y in YC]
XR = [11.7, 12.0, 12.3, 12.6]
YT = [2.4, 2.7, 3.0, 3.3]
XL = [1.2, 0.9, 0.6, 0.3]
X_CLK, Y_BR0, Y_BR1, Y_CLK0 = 9.25, -3.35, -6.12, -6.75
FF_LBL = 1.6                          # FF pin labels grow back to ~29 after the shrink
COL_X = 4.75                          # right column for tags


def G(x, y):
    """A local point in frame coordinates (FULL placement)."""
    return P(x * S + FULL.off[0], y * S + FULL.off[1])


def q_y(k):
    """Output k (Q0, Q0', Q1, Q1') height."""
    return YC[k // 2] + (PIN_FF if k % 2 == 0 else -PIN_FF)


def make_ff_gla(k):
    ff = L6.make_ff()
    d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l = ff.submobjects
    ff.remove(clk_w)
    ff.box, ff.tri, ff.d_l, ff.q_l, ff.qb_l = box, tri, d_l, q_l, qb_l
    ff.d_w, ff.q_w, ff.qb_w = d_w, q_w, qb_w
    ff.scale(FFS, about_point=ORIGIN)
    ff.shift(P(X_FF, YC[k]) - box.get_center())
    return ff


def gla():
    g = VGroup()
    g.bank = S3.input_bank(x_end=X_END)
    g.bank.remove(*g.bank.labels)
    iy = g.bank.rail_ys
    g.in_stubs = [Line(P(-0.6, y), P(0.3, y)).set_stroke(BLUE, S3.RAIL_W) for y in iy[::2]]
    gtop = iy[-1] - 0.4
    g.ands = S3.and_row(GX, SY + iy, gtop, pin=PIN_G)
    g.prods = [Line(P(gx, g.ands.stub_y), P(gx, OY[-1] - 0.4)).set_stroke(S3.LINE_C, 3) for gx in GX]
    ors = VGroup()
    ors.gates, ors.lines, ors.dots = [], [], []
    for oy in OY:
        body = S3.or_body_right(OR_L).set_stroke(S3.GATE_C, 4).set_fill(BG, 1).shift(P(OR_BACK, oy))
        body.set_z_index(1)
        ls = [Line(P(px, oy + dy), P(OR_BACK + 0.14, oy + dy)).set_stroke(S3.LINE_C, S3.LINE_W)
              for px, dy in zip(GX, (0.15, -0.15))]
        ds = [Dot(P(px, oy + dy), radius=S3.DOT_R, color=FG).set_z_index(2)
              for px, dy in zip(GX, (0.15, -0.15))]
        ors.gates.append(body)
        ors.lines.append(ls)
        ors.dots.append(ds)
        ors.add(*ls, body, *ds)
    g.ors = ors
    g.orw = [Line(P(OR_TIP, oy), P(xb, oy)).set_stroke(FG, 4) for oy, xb in zip(OY, XB)]
    g.dpath = [poly([(xb, oy), (xb, YC[k] + PIN_FF), (X_D, YC[k] + PIN_FF)], BLUE, 4)
               for k, (oy, xb) in enumerate(zip(OY, XB))]
    g.ffs = [make_ff_gla(k) for k in range(2)]
    g.fb = [poly([(X_Q, q_y(k)), (XR[k], q_y(k)), (XR[k], YT[k]), (XL[k], YT[k]), (XL[k], SY[k]),
                  (X_END, SY[k])], GREEN, S3.RAIL_W) for k in range(4)]
    clk_a = poly([(X_CLK, Y_CLK0), (X_CLK, Y_BR0), (X_FF, Y_BR0), (X_FF, FF_BOT[0])], YELLOW, 4)
    clk_b = poly([(X_CLK, Y_BR1), (X_FF, Y_BR1), (X_FF, FF_BOT[1])], YELLOW, 4)
    jdot = Dot(P(X_CLK, Y_BR1), radius=0.08, color=YELLOW)
    g.clk = VGroup(clk_a, clk_b, jdot)
    g.clk.clk_a, g.clk.clk_b, g.clk.jdot = clk_a, clk_b, jdot
    g.and_panel = S3.panel(1.7, 7.2, 2.25, g.ands.tip_y - 0.1)
    g.or_panel = S3.panel(1.7, 8.15, OY[0] + 0.45, OY[-1] - 0.45)
    g.add(g.and_panel, g.or_panel, *g.in_stubs, g.bank, g.ands, *g.prods, g.ors, *g.orw, *g.dpath,
          *g.ffs, *g.fb, g.clk)
    S3.place(g, FULL)
    for ff in g.ffs:
        for lab in (ff.d_l, ff.q_l, ff.qb_l):
            lab.scale(FF_LBL)
    g.clk_label = T("CLK", 30, YELLOW).next_to(clk_a.get_start(), RIGHT, buff=0.15)
    lo, hi = G(-0.15, -6.33), G(12.85, 3.55)
    chip = L8.chip("GLA", w=hi[0] - lo[0], h=hi[1] - lo[1], n_pins=4)
    chip.shift((lo + hi) / 2 - chip.body.get_center())
    chip.lab.move_to(G(0.8, -5.0))
    g.chip = chip
    g.add(g.clk_label, chip)
    return g


def final_tag():
    return T("two programmable\nplanes", 30, BLUE, line_spacing=0.9).move_to(P(COL_X, 0.4))


def handover_shot():
    return VGroup(gla(), final_tag())


# ---------------------------------------------------------------- the scene
class Gla(NarratedScene):
    def construct(self):
        self.g = gla()
        self.G = VGroup()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.remove(*self.mobjects)                  # invisible cut to the canonical handover shot
        self.add(handover_shot())
        self.wait(1.0)

    def keep(self, *mobs):
        settle(self, self.G, add=list(mobs))

    def all_dots(self, state=False):
        a, o = self.g.ands, self.g.ors
        rng = range(10) if state else range(4, 10)
        return [a.dots[gi][i] for gi in range(2) for i in rng] + [d for k in range(2) for d in o.dots[k]]

    # -- c4.gla.1: back to state machines, flip-flops, one clock
    def clip1(self):
        g = self.g
        shot = S3.handover_shot()
        core = shot[0]
        o_and, o_or, ob, oa = core[0], core[1], core[2], core[3]
        oprods, oo = list(core[4:7]), core[7]
        pieces = [o_and, o_or, *ob.submobjects, *oa.submobjects, *oprods, *oo.submobjects, *shot[1:]]
        self.add(*pieces)                            # s3's last frame, flattened

        pairs = [(o_and, g.and_panel), (o_or, g.or_panel)]
        b = g.bank
        for k in range(3):
            pairs += [(ob.wires[k], b.wires[k]), (ob.branches[k], b.branches[k]), (ob.invs[k], b.invs[k]),
                      (ob.splits[k], b.splits[k])]
        pairs += [(ob.rails[i], b.rails[i]) for i in range(6)]
        for gi in range(2):
            pairs.append((oa.gates[gi], g.ands.gates[gi]))
            pairs.append((oa.stubs[gi], g.ands.stubs[gi]))
            pairs.append((oprods[gi], g.prods[gi]))
            for i in range(6):
                pairs.append((oa.lines[gi][i], g.ands.lines[gi][4 + i]))
                pairs.append((oa.dots[gi][i], g.ands.dots[gi][4 + i]))
        for k in range(2):
            pairs.append((oo.gates[k], g.ors.gates[k]))
            pairs.append((oo.fwires[k], g.orw[k]))
            for j in range(2):
                pairs.append((oo.lines[k][j], g.ors.lines[k][j]))
                pairs.append((oo.dots[k][j], g.ors.dots[k][j]))
        moved = set(id(a) for a, _ in pairs)
        fades = [m for m in pieces if id(m) not in moved]
        new = [bnew for _, bnew in pairs] + list(g.in_stubs)

        title = T("GLA: generic logic array", 44, t2c={"GLA": YELLOW}).move_to(P(0, 3.4))
        like = T("like a PLA:\nboth planes\nprogrammable", 30, line_spacing=0.9).move_to(P(COL_X, 1.3))
        cap = T("“one following\neach OR gate”", 30, slant=ITALIC, line_spacing=0.9).move_to(P(COL_X, -0.8))
        self.title, self.like, self.cap = title, like, cap
        ffs = g.ffs
        for ff in ffs:
            ff.shift(0.9 * S * RIGHT)

        with self.say("c4.gla.1") as c:
            self.play(*during(disappear(*fades), 0, 0.45),
                      *during([ReplacementTransform(a, bn) for a, bn in pairs], 0.3, 1.0),
                      *during([FadeIn(m) for m in g.in_stubs], 0.6, 1.0),
                      run_time=min(2.2, c.until("modify")))
            self.keep(*new)
            c.wait_until("modify")
            self.play(*appear(*ffs, shift=0.6 * LEFT, lag=0.3), run_time=1.5)
            c.wait_until("called a")
            self.play(*appear(title), run_time=1.0)  # early: title, said as G-L-A then spelled out
            c.wait_until("like")
            self.play(*appear(like), run_time=1.0)
            self.play(*[d.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.7)
                        for d in self.all_dots()], run_time=1.2)
            c.wait_until("ffs")
            self.play(*[ff.animate.shift(0.9 * S * LEFT) for ff in ffs],
                      *during(recolor(g.orw, BLUE), 0.3, 0.7),
                      *during([Create(p) for p in g.dpath], 0.4, 1.0), run_time=1.8)
            self.play(*appear(cap), run_time=1.0)  # early: p. 156's own words; the voice says "followed by"
            self.keep(*ffs, *g.dpath)
            c.wait_until("clk")
            self.play(Create(g.clk.clk_a), Create(g.clk.clk_b), FadeIn(g.clk.jdot),
                      *during(appear(g.clk_label), 0.4, 1.0), run_time=1.6)
            self.keep(g.clk, g.clk_label)
            c.wait_until("edge")
            vals = []
            for k, v in enumerate("10"):
                vd = T(v, 34, GOLD).move_to(G(X_D - 0.12, YC[k] + PIN_FF + 0.3))
                vals.append((vd, G(X_Q + 0.25, YC[k] + PIN_FF)))
            self.vals = [vd for vd, _ in vals]
            self.play(*appear(vals[0][0], vals[1][0], lag=0.3), run_time=1.0)
            c.wait_until("stores")
            pulses = [VShowPassingFlash(p.copy().set_stroke(YELLOW, 9), time_width=0.5)
                      for p in (g.clk.clk_a, g.clk.clk_b)]
            self.play(*during(pulses, 0, 0.5),
                      *during([vd.animate(path_arc=-PI / 3).move_to(q) for vd, q in vals], 0.35, 1.0),
                      run_time=min(2.2, c.until(floor=1.5)))

    # -- c4.gla.2: not enough; feed the state back
    def clip2(self):
        g = self.g
        outs = [Arrow(G(X_Q, q_y(k)), G(X_Q + 1.4, q_y(k)), buff=0, stroke_width=5,
                     max_tip_length_to_length_ratio=0.3).set_color(GREEN) for k in (0, 2)]
        qm = T("?", 80, YELLOW).move_to(G(4.45, 1.3))
        tag = T("next state = f(inputs, current state)", 36,
                t2c={"inputs": BLUE, "current state": GREEN}).move_to(P(0, 3.35))
        quote = T("“Consequently it becomes possible to build\nprogrammable sequential logic circuits”",
                  28, slant=ITALIC, line_spacing=0.8).move_to(P(0, 3.15))
        self.quote = quote
        a = g.ands
        st = [(gi, i) for gi in range(2) for i in (0, 2)]
        with self.say("c4.gla.2") as c:
            self.play(*during(disappear(self.title, self.like, self.cap, *self.vals), 0, 0.45),
                      *during([GrowArrow(x) for x in outs], 0.35, 0.8),
                      *during(appear(qm, shift=None), 0.7, 1.0), run_time=min(2.0, c.until("state")))
            c.wait_until("the next state")
            self.play(*swap(qm, tag), run_time=1.2)  # early: the tag is read out in the next sentence
            c.wait_until("current state")
            self.play(*flash([VGroup(*tag[-13:-1])], color=GREEN, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("feedback")
            self.play(*during(disappear(*outs), 0, 0.3),
                      *during([Create(g.fb[0]), Create(g.fb[2])], 0.15, 1.0), run_time=2.2)
            self.play(*[Create(a.lines[gi][i]) for gi, i in st],
                      *during([FadeIn(a.dots[gi][i], scale=0.4) for gi, i in st], 0.5, 1.0), run_time=1.2)
            self.keep(g.fb[0], g.fb[2], *[a.lines[gi][i] for gi, i in st], *[a.dots[gi][i] for gi, i in st])
            c.wait_until("sees")
            hi = [a.lines[0][0], a.lines[0][4]]
            hd = [a.dots[0][0], a.dots[0][4]]
            self.play(*recolor(hi, YELLOW),
                      *[d.animate(rate_func=there_and_back).scale(2.0).set_color(YELLOW) for d in hd],
                      run_time=1.4)
            c.wait_until("quote")
            self.play(*swap(tag, quote), *recolor(hi, S3.LINE_C), run_time=1.4)  # early: slide quote

    # -- c4.gla.3: it is the Moore machine
    def clip3(self):
        g = self.g
        sch = S2.moore_schematic().scale(0.6)
        sch.move_to(P(0, 0)).align_to(P(0, 0.85), DOWN)
        pivot = P(-1.7, -3.65)
        self.G.save_state()
        chip = g.chip
        loops = [g.fb[0], g.fb[2]]
        with self.say("c4.gla.3") as c:
            self.play(*during(disappear(self.quote), 0, 0.4),
                      *during([self.G.animate.scale(0.66, about_point=pivot)], 0.2, 0.8),
                      *during(appear(sch, shift=None), 0.6, 1.0), run_time=min(2.4, c.until("logic")))
            c.wait_until("logic")
            panels = [g.and_panel, g.or_panel]
            self.play(sch.b1.animate.set_stroke(BLUE, 7), *[p.animate.set_fill(BLUE, 0.3) for p in panels],
                      FlashAround(sch.b1, color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("ffs2")
            boxes = [ff.box for ff in g.ffs]
            self.play(sch.b1.animate.set_stroke(FG, 4), *[p.animate.set_fill(DIM, 0.14) for p in panels],
                      sch.ff.box.animate.set_stroke(YELLOW, 6), *[b.animate.set_stroke(YELLOW, 6) for b in boxes],
                      run_time=1.2)
            c.wait_until("loop")
            self.play(sch.ff.box.animate.set_stroke(FG, 4), *[b.animate.set_stroke(FG, 4) for b in boxes],
                      VShowPassingFlash(S2.loop_path(sch).set_stroke(YELLOW, 7), time_width=0.6),
                      *[VShowPassingFlash(m.copy().set_stroke(YELLOW, 8), time_width=0.6) for m in loops],
                      run_time=1.8)
            c.wait_until("onechip")
            self.play(*during(disappear(sch), 0, 0.4),
                      *during([Restore(self.G)], 0.15, 0.6),
                      *during([Create(chip.body)], 0.55, 1.0),
                      *during([FadeIn(p) for p in chip.pins] + [FadeIn(chip.notch)], 0.7, 1.0),
                      *during(appear(chip.lab, shift=None), 0.75, 1.0),
                      run_time=min(2.4, c.until(floor=1.5)))
            self.keep(chip)

    # -- c4.gla.4: the slide's picture is simplified; Q-bar too
    def clip4(self):
        g = self.g
        a = g.ands
        fig = T("p. 157:\nvery simplified", 30, line_spacing=0.9)
        fig.move_to(P(COL_X, 2.3))
        counts = [T(s, 32, GOLD) for s in ("3 inputs", "2 AND", "2 OR", "2 flip-flops")]
        for i, m in enumerate(counts):
            m.move_to(P(COL_X - 1.2, 1.25 - 0.55 * i), aligned_edge=LEFT)
        cues = ["three inputs", "pair of and gates", "pair of or gates", "two flip-flops"]
        marks = [
            lambda: [VShowPassingFlash(s.copy().set_stroke(YELLOW, 8), time_width=0.8) for s in g.in_stubs],
            lambda: flash(a.gates, run_time=1.2),
            lambda: flash(g.ors.gates, run_time=1.2),
            lambda: flash([ff.box for ff in g.ffs], run_time=1.2),
        ]
        ghosts = [DashedVMobject(g.fb[k].copy(), num_dashes=70).set_stroke(GREEN, 3, opacity=0.45) for k in (1, 3)]
        st = [(gi, i) for gi in range(2) for i in (1, 3)]
        tag = final_tag()
        with self.say("c4.gla.4") as c:
            c.wait_until(own_word=fig)
            self.play(*appear(fig), run_time=1.0)
            for m, cue, mk in zip(counts, cues, marks):
                c.wait_until(cue)
                self.play(*appear(m), *mk(), run_time=1.0)
            c.wait_until("notq")
            self.play(*[VShowPassingFlash(g.fb[k].copy().set_stroke(YELLOW, 9), time_width=0.6) for k in (0, 2)],
                      *[ff.q_l.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.4) for ff in g.ffs],
                      run_time=1.6)
            c.wait_until("not cue is fed back")
            qb = [ff.qb_l for ff in g.ffs]
            self.play(*[q.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.4) for q in qb],
                      *[ff.qb_w.animate(rate_func=there_and_back).set_stroke(YELLOW, 9) for ff in g.ffs],
                      run_time=1.4)
            self.play(*[Create(gh) for gh in ghosts], run_time=1.6)
            c.wait_until("both")
            self.play(*during([FadeOut(gh) for gh in ghosts], 0, 0.3),
                      *during([Create(g.fb[1]), Create(g.fb[3])], 0.1, 1.0), run_time=1.4)
            self.play(*[Create(a.lines[gi][i]) for gi, i in st],
                      *during([FadeIn(a.dots[gi][i], scale=0.4) for gi, i in st], 0.5, 1.0),
                      run_time=min(0.9, c.until("complex")))
            self.keep(g.fb[1], g.fb[3], *[a.lines[gi][i] for gi, i in st], *[a.dots[gi][i] for gi, i in st])
            c.wait_until("complex")
            panels = [g.and_panel, g.or_panel]
            self.play(*[p.animate(rate_func=there_and_back).set_fill(BLUE, 0.35) for p in panels],
                      *during(disappear(fig, *counts), 0, 0.45),
                      *during(appear(tag), 0.5, 1.0), run_time=1.6)
            c.wait_until()
