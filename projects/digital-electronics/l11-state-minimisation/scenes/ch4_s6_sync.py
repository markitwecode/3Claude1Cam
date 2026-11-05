"""Chapter 4, scene 6: the synchroniser in a GAL. Clips c4.sync.1 – c4.sync.5.

Owns the GAL drawing (p. 158). Helpers other scenes import (load_scene("ch4_s6_sync")):
- `gal(left=2, right=2, gaps=None, inputs=("a", "b"), outs=("f0", "fn"), lit=True, where=LARGE,
  plane_labels=True)`: p. 158's GAL built from s3's pieces. Rails top to bottom: four GREEN
  feedback rails (outs[0], its complement, outs[1], its complement), then the inputs and their
  complements (BLUE, s3's input_bank). The left group of AND gates feeds the bottom OR gate
  (outs[1]), the right group the top one (outs[0]), by fixed lines; each OR gate drives an L6
  `make_ff` D flip-flop. Every Q and Q̄ runs right, up past the array's top, left along the top
  and down into its GREEN rail. CLK (YELLOW) enters at the bottom left. (2, 2) is the slide's
  picture with its dotted (within a group) and dashed (between groups, between the OR gates)
  gaps; (2, 3) is the synchroniser's five-gate GAL (no gaps). lit=False: every dot faint (0.3).
  Handles: .bank (input_bank: .labels .rails .invs ...) .in_labels .green .feed (Q/Q̄ wires)
  .rails (all 8 rail Lines, top to bottom) .rail_names .rail_labels (8 labels, NOT in the group)
  .ands (s3 and_row: .gates .lines[g][i] .dots[g][i]) .dots (flat) .groups {"top": [...], "bot": [...]}
  .fixed[g] (OR-plane lines) .or_lines (= fixed) .ors [top, bottom] .ffs [top, bottom]
  .out_wires .out_dots .out_labels [top, bottom] .clk (wires + dot) .clk_label .gaps (VGroup;
  empty without gaps) .dashed_or .panels [AND, OR] .plane_labels .term_pos(g) (gate-body centre).
  `where` is a Where(s, x, y) placement (LARGE, MID, SMALL here); labels are scaled up by
  where.lu (rail labels by where.rlu) about their outer edge.
- `opening_shot()`: the large p. 158 GAL, every AND-plane dot lit (s5's {figure}; s5 ends on it).
- `compiler_row(eqs, size=26, out=None)`: equations box (eqs: MathTex or tex strings, stacked)
  → "compiler" box → arrow, centred at ORIGIN. .box .eqs .arrow1 .comp (box + text) .arrow2 .out.
- `sync_gal(where=MID)`: the finished synchroniser GAL: five coloured AND gates with their terms,
  12 coloured dots, e/r and s1/s0 rail labels, output `s`, r̄ DIM, s0's output pin DIM.
  Extra handles: .terms[g] (MathTex in gate g), .unused (the r̄ rail + label).
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch4_s3_plapal")
P, poly, panel, plane_label = S3.P, S3.poly, S3.panel, S3.plane_label
LBL, RAIL_W, LINE_C, GATE_C = S3.LBL, S3.RAIL_W, S3.LINE_C, S3.GATE_C


def _load(folder, stem):
    path = Path(__file__).resolve().parents[2] / folder / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_{folder[:3]}_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L6 = _load("l06-flip-flops-counters", "ch6_s6_circuit")       # make_ff
L10D = _load("l10-state-assignment", "ch5_s3_diagram")        # sync_diagram
L10K = _load("l10-state-assignment", "ch5_s6_d1")             # kmap4, loop4, D1 map and loops

# ---------------------------------------------------------------- names and terms
TEX = {"s1": "s_1", "s1'": r"\overline{s}_1", "s0": "s_0", "s0'": r"\overline{s}_0",
       "e": "e", "e'": r"\overline{e}", "r": "r", "r'": r"\overline{r}",
       "f0": "f_0", "f0'": r"\overline{f}_0", "fn": "f_n", "fn'": r"\overline{f}_n",
       "a": "a", "a'": r"\overline{a}", "b": "b", "b'": r"\overline{b}", "s": "s"}
D1_TERMS = (r"s_1\cdot\overline{e}", r"s_1\cdot r", r"s_0\cdot e\cdot r")
D0_TERMS = (r"s_0\cdot\overline{e}", r"\overline{s}_1\cdot\overline{s}_0\cdot r")
D1_COLORS = (PINK, PURPLE, TEAL)
D0_COLORS = (PINK, PURPLE)
SYNC_RAILS = ["s1", "s1'", "s0", "s0'", "e", "e'", "r", "r'"]
# gate -> (tex, colour, rails kept); gates 0-1 feed D0 (bottom OR), 2-4 feed D1 (top OR).
# Each group's terms sit left to right as its equation reads them.
SYNC_GATES = [(D0_TERMS[0], PINK, ("s0", "e'")), (D0_TERMS[1], PURPLE, ("s1'", "s0'", "r")),
              (D1_TERMS[0], PINK, ("s1", "e'")), (D1_TERMS[1], PURPLE, ("s1", "r")),
              (D1_TERMS[2], TEAL, ("s0", "e", "r"))]
D0_MAP = (("", "1", "1", ""), ("1", "1", "", ""), ("X", "X", "X", "X"), ("", "", "", ""))
D0_LOOPS = (([(1, 0), (1, 1), (2, 0), (2, 1)], 0.08), ([(0, 1), (0, 2)], 0.08))


def tex(n, size=LBL, color=GREEN):
    return MathTex(TEX[n], font_size=size, color=color)


# ---------------------------------------------------------------- geometry (local units)
class Where:
    def __init__(self, s, x, y, lu=1.0, rlu=1.0):
        self.s, self.off, self.lu, self.rlu = s, P(x, y), lu, rlu


LARGE = Where(0.68, -4.98, 2.87, 1.15, 1.0)     # s5's figure / this scene's opening
MID = Where(0.6, -2.4, 2.94, 1.25, 1.1)         # clips 2-5: the hero, right of the left column
SMALL = Where(0.4, 0.6, 0.22, 1.75, 1.0)         # clip 1-2: lower right

PITCH = 0.45
G_YS = [0.0, -0.45, -0.9, -1.35]                # GREEN feedback rails
IN_TOP = -1.8                                   # first input rail
X_END = 11.35                                   # rails end
GTOP = -3.55                                    # AND gates' flat tops
GX4 = [2.5, 4.8, 7.4, 9.7]
GX5 = [2.5, 4.45, 6.45, 8.4, 10.35]
OR_X = 10.65                                    # OR backs
ORY = [-5.5, -7.4]                              # top OR (outs[0]), bottom OR (outs[1])
FF_S = 0.6
FF_X = 12.56
XR = [13.7, 13.88, 14.06, 14.24]                # feedback risers at the right
HT = [0.35, 0.5, 0.65, 0.8]                     # their runs over the top
XL = [1.65, 1.5, 1.35, 1.2]                     # and their drops at the left
OUT_X = 14.5
CLK_Y = -9.14
CLK_X = 11.85
RL_X = 11.5                                     # rail labels


def place(m, w):
    return m.scale(w.s, about_point=ORIGIN).shift(w.off)


def remap(m, a, b):
    return m.shift(-a.off).scale(b.s / a.s, about_point=ORIGIN).shift(b.off)


def put_label(m, w, edge, rail=False):
    """A label built in local units: placed, then scaled up by w.lu (rails: w.rlu) about `edge`."""
    place(m, w)
    k = w.rlu if rail else w.lu
    if k != 1:
        m.scale(k, about_edge=edge)
    return m


def or_inputs(n):
    return {1: [0.0], 2: [0.15, -0.15], 3: [0.22, 0.0, -0.22]}[n]


def gal(left=2, right=2, gaps=None, inputs=("a", "b"), outs=("f0", "fn"), lit=True, where=LARGE,
        plane_labels=True):
    if gaps is None:
        gaps = (left, right) == (2, 2)
    gx = GX4 if (left, right) == (2, 2) else GX5[:left] + GX5[2:2 + right]
    n = left + right
    g = VGroup()
    g.where = where
    g.labels_edges = []
    # rails
    g.rail_names = [outs[0], outs[0] + "'", outs[1], outs[1] + "'"] + \
        [x for i in inputs for x in (i, i + "'")]
    g.green = [Line(P(XL[k], y), P(X_END, y)).set_stroke(GREEN, RAIL_W) for k, y in enumerate(G_YS)]
    g.bank = S3.input_bank(inputs, x_end=X_END, top=IN_TOP)
    g.in_labels = list(g.bank.labels)
    g.rails = g.green + list(g.bank.rails)
    ys = G_YS + g.bank.rail_ys
    g.rail_ys = ys
    # AND gates
    g.ands = S3.and_row(gx, ys, GTOP)
    for st in g.ands.stubs:
        g.ands.remove(st)
    for row in g.ands.dots:
        for d in row:
            d.set_opacity(1 if lit else 0.3)
    g.dots = [d for row in g.ands.dots for d in row]
    tip = g.ands.tip_y
    g.gx = gx
    g.groups = {"bot": list(range(left)), "top": list(range(left, n))}
    # fixed OR-plane lines: the rightmost gate of a group enters its OR gate's top input
    g.fixed = [None] * n
    for key, k in (("top", 0), ("bot", 1)):
        idx = g.groups[key]
        offs = or_inputs(len(idx))
        for j, gi in enumerate(reversed(idx)):
            yi = ORY[k] + offs[j]
            g.fixed[gi] = poly([(gx[gi], tip), (gx[gi], yi), (OR_X + 0.1, yi)], LINE_C, 3)
    g.or_lines = g.fixed
    g.ors = []
    for k in range(2):
        b = S3.or_body_right().set_stroke(GATE_C, 4).set_fill(BG, 1).shift(P(OR_X, ORY[k]))
        b.set_z_index(1)
        g.ors.append(b)
    # flip-flops (L6 make_ff), D wire from each OR tip
    g.ffs = []
    for k in range(2):
        ff = L6.make_ff()
        ff.scale(FF_S, about_point=ORIGIN).shift(P(FF_X, ORY[k] - L6.PIN_Y * FF_S))
        for lab in (ff.d_l, ff.q_l, ff.qb_l):
            lab.scale(1.4)
        if k == 0:
            ff.remove(ff.clk_w)
        g.ffs.append(ff)
    # feedback: Q / Q̄ right, up, over the top, down into the GREEN rail
    q_end = FF_X + (L6.BOX_W / 2 + L6.WIRE) * FF_S
    g.feed = []
    for k in range(4):
        py = ORY[k // 2] - (0 if k % 2 == 0 else 2 * L6.PIN_Y * FF_S)
        g.feed.append(poly([(q_end, py), (XR[k], py), (XR[k], HT[k]), (XL[k], HT[k]), (XL[k], G_YS[k])],
                           GREEN, RAIL_W))
    # outputs
    g.out_wires, g.out_dots, g.out_labels = [], [], []
    for k in range(2):
        x0 = XR[2 * k]
        g.out_wires.append(Line(P(x0, ORY[k]), P(OUT_X, ORY[k])).set_stroke(GREEN, RAIL_W))
        g.out_dots.append(Dot(P(x0, ORY[k]), radius=0.08, color=GREEN))
        lab = tex(outs[k]).next_to(P(OUT_X, ORY[k]), RIGHT, buff=0.12)
        g.out_labels.append(lab)
    # clock
    hb = L6.BOX_H / 2 * FF_S
    top_tri_y = ORY[0] - L6.PIN_Y * FF_S - hb
    mid_y = (top_tri_y + ORY[1] - L6.PIN_Y * FF_S + hb) / 2
    clk_main = Line(P(0.55, CLK_Y), P(FF_X, CLK_Y)).set_stroke(YELLOW, 5)
    clk_up = poly([(CLK_X, CLK_Y), (CLK_X, mid_y), (FF_X, mid_y), (FF_X, top_tri_y)], YELLOW, 5)
    clk_dot = Dot(P(CLK_X, CLK_Y), radius=0.08, color=YELLOW)
    g.clk = VGroup(clk_main, clk_up, clk_dot)
    g.clk_label = T("CLK", 40, YELLOW).move_to(P(0.45, CLK_Y), aligned_edge=RIGHT)
    # gaps (the slide's picture)
    g.gaps = VGroup()
    g.dashed_or = VGroup()
    if gaps:
        gy = GTOP - 0.75
        hw = g.ands.w / 2
        for a, b, kind in ((0, 1, "dot"), (1, 2, "dash"), (2, 3, "dot")):
            x0, x1 = gx[a] + hw + 0.08, gx[b] - hw - 0.08
            if kind == "dot":
                g.gaps.add(VGroup(*[Dot(P(x, gy), radius=0.035, color=FG)
                                    for x in np.linspace(x0 + 0.06, x1 - 0.06, 4)]))
            else:
                g.gaps.add(DashedLine(P(x0, gy), P(x1, gy), dash_length=0.12).set_stroke(FG, 3))
        g.dashed_or.add(DashedLine(P(OR_X + 0.45, ORY[0] - 0.5), P(OR_X + 0.45, ORY[1] + 0.5),
                                   dash_length=0.12).set_stroke(FG, 3))
    # planes
    g.panels = [panel(-0.35, 11.75, 0.18, -4.85), panel(-0.35, 11.75, -4.95, -8.05)]
    g.plane_labels = VGroup(plane_label("AND", P(0.6, -4.15), 34), plane_label("OR", P(0.6, -6.5), 34))
    # rail labels (not in the group)
    g.rail_labels = [MathTex(TEX[nm], font_size=LBL, color=GREEN if k < 4 else BLUE)
                     .move_to(P(RL_X, y), aligned_edge=LEFT) for k, (nm, y) in enumerate(zip(g.rail_names, ys))]

    def term_pos(i):
        return P(gx[i], GTOP - 0.42)
    g._term_local = term_pos
    g.add(*g.panels, *g.feed, *g.green, g.bank, g.ands, *g.fixed, *g.ors, *g.ffs,
          *g.out_wires, *g.out_dots, *g.out_labels, g.clk, g.clk_label, g.gaps, g.dashed_or)
    if plane_labels:
        g.add(g.plane_labels)
    place(g, where)
    for rl in g.rail_labels:
        put_label(rl, where, LEFT, rail=True)
    for lab in g.in_labels:
        lab.scale(where.lu, about_edge=RIGHT)
    for lab in g.out_labels:
        lab.scale(where.lu, about_edge=LEFT)
    g.clk_label.scale(where.lu, about_edge=RIGHT)
    for lab in g.plane_labels:
        lab.scale(where.lu)
    return g


def gal_moved(g, b):
    """A copy of g (geometry, labels) as it would sit at placement b (for MoveToTarget)."""
    a = g.where
    t = g.copy()
    remap(t, a, b)
    k = b.lu / a.lu
    for lab in t.in_labels:
        lab.scale(k, about_edge=RIGHT)
    for lab in t.out_labels:
        lab.scale(k, about_edge=LEFT)
    t.clk_label.scale(k, about_edge=RIGHT)
    return t


def term_label(g, i, tex_s, color, where):
    m = MathTex(tex_s, font_size=40, color=color).move_to(g._term_local(i) + P(0, 0.05)).set_z_index(3)
    return place(m, where)


def local_label(tex_s, at, where, edge, color=BLUE, rail=False):
    m = MathTex(tex_s, font_size=LBL, color=color)
    m.move_to(at, aligned_edge=edge if edge is not None else ORIGIN)
    return put_label(m, where, edge if edge is not None else ORIGIN, rail=rail)


def opening_shot():
    """s5's {figure}: the large p. 158 GAL, every AND-plane dot lit."""
    return gal()


def compiler_row(eqs, size=26, out=None):
    """equations box -> "compiler" box -> arrow (to the AND plane), centred at ORIGIN."""
    ms = [MathTex(e, font_size=size) if isinstance(e, str) else e for e in eqs]
    col = VGroup(*ms).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.12, width=col.width + 0.5, height=col.height + 0.4)
    box.set_stroke(FG, 2.5).move_to(col)
    a1 = Arrow(box.get_right(), box.get_right() + RIGHT * 0.9, buff=0.1, stroke_width=4).set_color(FG)
    ct = T("compiler", 30, YELLOW)
    cb = RoundedRectangle(corner_radius=0.12, width=ct.width + 0.5, height=0.75).set_stroke(YELLOW, 2.5)
    comp = VGroup(cb, ct)
    comp.next_to(a1, RIGHT, buff=0.1)
    ct.move_to(cb)
    a2 = Arrow(cb.get_right(), cb.get_right() + RIGHT * 0.9, buff=0.1, stroke_width=4).set_color(FG)
    g = VGroup(box, col, a1, comp, a2)
    g.out = None
    if out:
        o = T(out, 30, FG).next_to(a2, RIGHT, buff=0.12)
        g.out = o
        g.add(o)
    g.box, g.eqs, g.arrow1, g.comp, g.arrow2 = box, col, a1, comp, a2
    g.move_to(ORIGIN)
    return g


def sync_labels(g, where):
    """The synchroniser's names on a gal(): input labels, rail labels, flip-flop outputs."""
    ins = []
    for nm, y in (("e", IN_TOP), ("r", IN_TOP - 2 * PITCH)):
        m = place(MathTex(nm, font_size=LBL, color=BLUE).move_to(P(0, y)), where)
        ins.append(m.scale(where.lu, about_edge=RIGHT))
    rails = [local_label(TEX[nm], P(RL_X, y), where, LEFT, GREEN if k < 4 else BLUE, rail=True)
             for k, (nm, y) in enumerate(zip(SYNC_RAILS, g.rail_ys))]
    outs = [local_label("s_1", P(OUT_X + 0.12, ORY[0]), where, LEFT, GREEN),
            local_label("s_0", P(OUT_X + 0.12, ORY[1]), where, LEFT, GREEN)]
    return ins, rails, outs


def sync_gal(where=MID):
    g = gal(2, 3, inputs=("a", "b"), outs=("f0", "fn"), lit=False, where=where, plane_labels=False)
    ins, rails, outs = sync_labels(g, where)
    g.bank.remove(*g.in_labels)
    g.remove(*g.in_labels, *g.out_labels)
    s_lab = local_label("s", P(OUT_X + 0.12, ORY[0]), where, LEFT, GREEN)
    g.in_labels, g.rail_labels = ins, rails
    g.out_labels = [s_lab, outs[1]]
    g.terms = []
    for i, (t, col, keep) in enumerate(SYNC_GATES):
        g.ands.gates[i].set_stroke(col)
        g.fixed[i].set_stroke(col)
        for j, d in enumerate(g.ands.dots[i]):
            if SYNC_RAILS[j] in keep:
                d.set_fill(col, 1).scale(1.35)
            else:
                d.set_opacity(0)
        tm = term_label(g, i, t, col, where)
        g.terms.append(tm)
    g.unused = VGroup(g.rails[7], rails[7])
    g.rails[7].set_stroke(DIM)
    rails[7].set_color(DIM)
    for m in (g.out_wires[1], g.out_dots[1], outs[1]):
        m.set_color(DIM)
    g.add(*ins, *rails, *g.out_labels, *g.terms)
    return g


# ---------------------------------------------------------------- left-side pieces
def eq_tex(which, size):
    if which == 1:
        m = MathTex("D_1", "=", D1_TERMS[0], "+", D1_TERMS[1], "+", D1_TERMS[2], font_size=size)
        cols = {2: D1_COLORS[0], 4: D1_COLORS[1], 6: D1_COLORS[2]}
    else:
        m = MathTex("D_0", "=", D0_TERMS[0], "+", D0_TERMS[1], font_size=size)
        cols = {2: D0_COLORS[0], 4: D0_COLORS[1]}
    m[0].set_color(BLUE)
    for k, c in cols.items():
        m[k].set_color(c)
    return m


def chip(name):
    t = MathTex(name, font_size=44, color=BLUE)
    b = RoundedRectangle(corner_radius=0.12, width=0.7, height=0.7).set_stroke(BLUE, 3).move_to(t)
    return VGroup(b, t)


def ghost_map(values, loops, center, title):
    m = L10K.kmap4(values, center=center, scale=0.45)
    body = VGroup(m.grid, m.entries)
    for leaf in body.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_opacity(0.45)
        else:
            leaf.set_stroke(opacity=0.45)
    lps = [L10K.loop4(m, cells, col, inset) for (cells, inset), col in zip(loops, (PINK, PURPLE, TEAL))]
    tt = MathTex(title, font_size=30, color=BLUE).next_to(m.grid, UP, buff=0.1)
    g = VGroup(body, *lps, tt)
    g.loops = lps
    return g


EQ_X = -6.65            # left column's left edge
COL_X = -4.75           # left column's centre


class SyncGal(NarratedScene):
    def construct(self):
        self.G = G = opening_shot()
        self.add(G)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        G = self.G
        with self.say("c4.sync.1") as c:
            G.target = gal_moved(G, SMALL)
            self.play(MoveToTarget(G), *during(disappear(G.plane_labels), 0, 0.4),
                      run_time=min(1.6, c.until("frame synchroniser")))
            settle(self, G, drop=[G.plane_labels])
            G.where = SMALL
            d = L10D.sync_diagram(codes={"Hunt": "00", "Sight": "01", "Sync": "10"}, r=0.75)
            d.scale(0.6)
            for nm in d.names:
                nm.scale(1.45)
            for cd in d.code.values():
                cd.scale(1.45)
            d.code["Sight"].shift(0.3 * LEFT)
            d.code["Sync"].shift(0.08 * UP)
            d.code["Hunt"].shift(0.08 * UP)
            for lb in d.labels:
                lb.scale(1.25)
            d.move_to(P(-3.75, 1.62))
            self.diag = d
            self.play(*appear(d, shift=None), run_time=1.0)  # early: the diagram is the machine being named
            c.wait_until("states")
            for w in ("Hunt", "Sight", "Sync"):
                c.wait_until(w)
                self.play(d.circle[w].animate.set_stroke(YELLOW, 5), run_time=0.5)
            c.wait_until("inputs")
            self.chips = [chip("e").move_to(P(0.1, 2.85)), chip("r").move_to(P(0.1, 1.95))]
            self.play(*appear(*self.chips, lag=0.4),
                      *[d.circle[w].animate.set_stroke(FG, 4) for w in ("Hunt", "Sight")],
                      run_time=1.2)
            c.wait_until("called ess")
            tag = MathTex("s = 1", font_size=34, color=GREEN)
            tag.move_to(d.code["Sync"]).shift(RIGHT * 1.0)
            self.s_tag = tag
            self.play(*appear(tag), run_time=0.9)
            c.wait_until("ffs")
            ffs = []
            for k, (x, nm) in enumerate(((2.45, "s_1"), (5.05, "s_0"))):
                ff = L6.make_ff()
                ff.scale(0.55).move_to(P(x, 2.2))
                for lab in (ff.d_l, ff.q_l, ff.qb_l):
                    lab.scale(1.2)
                ol = MathTex(nm, font_size=34, color=GREEN).next_to(ff.q_w, RIGHT, buff=0.1)
                ffs.append(VGroup(ff, ol))
            self.ffs = ffs
            self.play(*appear(*ffs, lag=0.4), run_time=1.4)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        G = self.G
        with self.say("c4.sync.2") as c:
            d1, d0 = eq_tex(1, 36), eq_tex(0, 36)
            d1.move_to(P(0, -0.9)).align_to(P(EQ_X + 0.05, 0), LEFT)
            d0.move_to(P(0, -2.2)).align_to(P(EQ_X + 0.05, 0), LEFT)
            self.d1, self.d0 = d1, d0
            self.play(*appear(d1, d0, lag=0.5), run_time=min(1.6, c.until("products")))
            c.wait_until("products")
            p3 = T("3 products", 30, GOLD).next_to(d1, DOWN, buff=0.22).align_to(d1, LEFT)
            p2 = T("2 products", 30, GOLD).next_to(d0, DOWN, buff=0.22).align_to(d0, LEFT)
            self.play(*appear(p3), run_time=0.9)
            c.wait_until("two for dee zero")
            self.play(*appear(p2), run_time=0.9)
            c.wait_until("rails")
            # the GAL becomes the hero; the equations move to the left column
            G.target = gal_moved(G, MID)
            movers = []
            for m, p, y in ((d1, p3, 1.0), (d0, p2, -1.6)):
                m.generate_target()
                m.target.scale(30 / 36).move_to(P(0, y)).align_to(P(EQ_X, 0), LEFT)
                p.generate_target()
                p.target.next_to(m.target, DOWN, buff=0.2).align_to(m.target, LEFT)
                movers += [MoveToTarget(m), MoveToTarget(p)]
            self.prods = [p3, p2]
            gone = [self.diag, *self.chips, self.s_tag, *self.ffs]
            self.play(*during(disappear(*gone), 0, 0.4), *during(MoveToTarget(G), 0.3, 1),
                      *during(movers, 0.4, 0.95), run_time=min(2.0, c.until("become ee")))
            G.where = MID
            c.wait_until("become ee")
            ins, rails, outs = sync_labels(G, MID)
            self.rl = rails
            self.play(*swap(G.in_labels[0], ins[0]), *swap(G.in_labels[1], ins[1]),
                      *during(appear(*rails[4:], lag=0.2, shift=None), 0.45, 1), run_time=1.6)
            G.bank.remove(*G.in_labels)
            settle(self, G, add=[*ins, *rails[4:]], drop=G.in_labels)
            G.in_labels = ins
            c.wait_until("fed")
            self.play(*appear(*rails[:4], lag=0.2, shift=None), run_time=1.2)
            self.play(*swap(G.out_labels[0], outs[0]), *swap(G.out_labels[1], outs[1]),
                      run_time=min(1.2, c.until("eight")))
            settle(self, G, add=[*rails[:4], *outs], drop=G.out_labels)
            G.out_labels = outs
            c.wait_until("eight")
            self.eight = T("8 rails", 34, GOLD).move_to(P(COL_X, 2.6))
            flashes = [VShowPassingFlash(r.copy().set_stroke(YELLOW, 7), time_width=0.5) for r in G.rails]
            self.play(*appear(self.eight), *flashes, run_time=1.6)

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        G = self.G
        with self.say("c4.sync.3") as c:
            N = gal(2, 3, lit=False, where=MID, plane_labels=False)
            old = [G.ands, *G.fixed, G.gaps, G.dashed_or]
            self.play(*during(disappear(*old, *self.prods), 0, 0.45),
                      *during(appear(N.ands, *N.fixed, shift=None, lag=0), 0.5, 1), run_time=1.6)
            settle(self, G, add=[N.ands, *N.fixed], drop=old)
            G.ands, G.fixed, G.dots, G.gx = N.ands, N.fixed, N.dots, N.gx
            G._term_local = N._term_local
            gates, fixed = G.ands.gates, G.fixed
            self.play(*[m.animate.set_stroke(YELLOW) for i in (2, 3, 4) for m in (gates[i], fixed[i])],
                      run_time=1.0)
            self.terms = [None] * 5
            # one term at a time, each on an arc over the terms already placed
            beats = [(2, self.d1[2], "pink", 1.5, -2 * PI / 3), (3, self.d1[4], "purple", 1.0, -PI / 2),
                     (4, self.d1[6], "teal", 1.2, -PI / 2),
                     (0, self.d0[2], "pink0", 1.2, PI / 5), (1, self.d0[4], "purple0", 1.3, PI / 4)]
            for i, src, cue, rt, arc in beats:
                if i == 0:
                    c.wait_until("d0gates")
                    self.play(*[m.animate.set_stroke(YELLOW) for j in (0, 1) for m in (gates[j], fixed[j])],
                              run_time=1.0)
                c.wait_until(cue)
                t, col, _ = SYNC_GATES[i]
                dst = term_label(G, i, t, col, MID)
                self.terms[i] = dst
                self.play(*fly(src, dst, arc=arc), gates[i].animate.set_stroke(col),
                          fixed[i].animate.set_stroke(col), run_time=rt)
            settle(self, G, add=self.terms)
            c.wait_until("loops")
            k1 = ghost_map(L10K.D1_MAP, L10K.D1_LOOPS, P(-5.75, -0.4), "D_1")
            k0 = ghost_map(D0_MAP, D0_LOOPS, P(-3.85, -0.4), "D_0")
            self.ghosts = [k1, k0]
            self.play(*appear(k1, k0, lag=0.3, shift=None), run_time=1.2)
            pairs = [(k1.loops[0], 2, PINK), (k1.loops[1], 3, PURPLE), (k1.loops[2], 4, TEAL),
                     (k0.loops[0], 0, PINK), (k0.loops[1], 1, PURPLE)]
            anims = []
            for n, (lp, gi, col) in enumerate(pairs):
                a, b = 0.55 * n, 0.55 * n + 1.1
                anims += [time_span(FlashAround(lp, color=col, time_width=1.0), a, b),
                          time_span(FlashAround(gates[gi], color=col, time_width=1.0), a, b)]
            self.play(*anims, run_time=0.55 * 4 + 1.1)

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        G = self.G
        with self.say("c4.sync.4") as c:
            anims = [time_span(a, 0, 0.8) for a in disappear(*self.ghosts)]
            for i, (_, col, keep) in enumerate(SYNC_GATES):
                a, b = 0.4 + 0.35 * i, 1.4 + 0.35 * i
                for j, dt in enumerate(G.ands.dots[i]):
                    if SYNC_RAILS[j] in keep:
                        anims.append(time_span(dt.animate.set_fill(col, 1).scale(1.35), a, b))
                    else:
                        anims.append(time_span(dt.animate.set_opacity(0), a, b))
            self.play(*anims, run_time=1.4 + 0.35 * 4)
            c.wait_until("kept")
            kept = T("12 kept of 40", 34, GOLD).move_to(self.eight)
            self.play(*swap(self.eight, kept), run_time=1.2)
            self.kept = kept
            c.wait_until("unused")
            # the tag sits in the left column, between "12 kept of 40" and D1
            un_w = T("unused", 32, DIM)
            un = VGroup(MathTex(r"\overline{r}", font_size=40, color=DIM), un_w).arrange(RIGHT, buff=0.2)
            un.move_to(P(COL_X, 1.85))
            self.unused = un
            self.play(G.rails[7].animate.set_stroke(DIM), self.rl[7].animate.set_color(DIM),
                      FlashAround(self.rl[7], color=DIM, time_width=1.0), run_time=0.9)
            c.wait_until(own_word=un_w)
            self.play(*appear(un), run_time=0.9)
            c.wait_until("state")
            self.play(*[FlashAround(ff.box, color=GREEN, time_width=1.0) for ff in G.ffs],
                      *flash(G.out_labels, color=GREEN), run_time=1.4)
            c.wait_until("out")
            s_lab = local_label("s", P(OUT_X + 0.12, ORY[0]), MID, LEFT, GREEN)
            st = MathTex("s = s_1", font_size=36, color=GREEN).move_to(P(COL_X, -2.55))
            self.s_tag = st
            self.play(*swap(G.out_labels[0], s_lab),
                      *[m.animate.set_color(DIM) for m in (G.out_wires[1], G.out_dots[1], G.out_labels[1])],
                      run_time=1.2)
            settle(self, G, add=[s_lab], drop=[G.out_labels[0]])
            G.out_labels = [s_lab, G.out_labels[1]]
            self.play(*appear(st), run_time=0.9)

    # ------------------------------------------------------------------ clip 5
    def clip5(self):
        G = self.G
        with self.say("c4.sync.5") as c:
            spot = place(VectorizedPoint(P(7.6, -6.4)), MID).get_center()
            q = T("?", 60, YELLOW).move_to(spot)
            self.play(*appear(q), run_time=1.0)
            c.wait_until("none")
            ok = set_backstroke(T("nothing shared", 30, GREEN).move_to(spot)).set_z_index(3)
            self.play(*swap(q, ok), run_time=1.2)
            c.wait_until("No product term")
            ghost = S3.made_twice_tag().move_to(place(VectorizedPoint(P(1.0, -6.4)), MID).get_center())
            ghost.set_opacity(0.6)
            self.play(*appear(ghost, shift=None), run_time=0.8)  # early: a ghost of s3's tag, read with "made twice"
            c.wait_until("made twice")
            self.play(*disappear(ghost), run_time=min(1.0, c.until("five")))
            c.wait_until("five")
            corner = P(6.6, 3.45)
            moving = [G]
            counts = T("5 AND · 2 OR · 2 flip-flops", 32, GOLD).move_to(P(2.8, -1.8))
            self.play(*[m.animate.scale(0.8, about_point=corner) for m in moving],
                      *[m.animate.move_to(corner + 0.8 * (m.get_center() - corner)) for m in (ok,)],
                      *during(disappear(self.s_tag), 0, 0.4),
                      *during(appear(counts), 0.55, 1), run_time=2.0)  # early: the totals, read as said
            c.wait_until("compiler")
            row = compiler_row([eq_tex(1, 28), eq_tex(0, 28)], out="connections")
            row.move_to(P(0, -2.85)).align_to(P(EQ_X, 0), LEFT)
            for m, ph in ((self.d1, row.eqs[0]), (self.d0, row.eqs[1])):
                m.generate_target()
                m.target.scale(28 / 30).move_to(ph)
            self.play(*during(MoveToTarget(self.d0), 0, 0.5), *during(MoveToTarget(self.d1), 0.4, 0.9),
                      *during(appear(row.box, shift=None), 0.75, 1), run_time=1.6)
            c.wait_until("connections")
            self.play(*appear(row.arrow1, row.comp, row.arrow2, row.out, lag=0.3, shift=None), run_time=1.3)
        self.wait(1.5)
