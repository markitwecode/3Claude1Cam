"""Chapter 4, scene 3: PLAs and PALs. Clips c4.pla.1 – c4.pla.6.

Owns the chapter's programmable-array style. Helpers other scenes import:
  sig, tex_name, term_tex, formula_tex          signal / term / formula MathTex (real overbars)
  input_bank(inputs, ...)                       input labels, wires, inverters, rail pairs
  rails(names, x0, x1, ...)                     plain rails from a name list (+ labels), any colour
  rail_labels(names, ys, x)                     overbarred rail labels
  and_body_down / and_row(gate_x, rail_ys, top) AND gates hanging below rails, input lines, dots
  or_body_right / or_body_down / or_row_right   OR gates (programmable dots) ; fixed_line (PAL)
  panel(x0, x1, y_top, y_bot) / plane_label     DIM-shaded plane panels and their labels
  made_twice_tag(), count_label(n), cost_line()
  build_pla(), build_pal(), small_pal(), small_pla(), handover_shot(), opening_shot()
  handover_shot() handles: .pla .pal .pla_head .pal_head .tag .f0 .f1 .forms .c3 .c4 .counts .cost
Geometry is built in local units (top rail at y=0, input labels at x=0) and placed with
place(mob, MID / BIG / SMALL / PAL_SMALL).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- basics
def P(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=4):
    return VMobject().set_points_as_corners([P(*q) for q in pts]).set_stroke(color, width)


def tex_name(n):
    """"a" -> a, "a'" -> \\overline{a}, "f0" -> f_{0}, "q1'" -> \\overline{q_{1}}."""
    neg = n.endswith("'")
    base = n.rstrip("'")
    if len(base) == 2:
        base = "%s_{%s}" % (base[0], base[1])
    return r"\overline{%s}" % base if neg else base


def term_tex(term):
    return r"\cdot ".join(tex_name(x) for x in term)


def sig(n, size=40, color=BLUE):
    return MathTex(tex_name(n), font_size=size, color=color)


def formula_tex(out, terms, size=40, color=FG):
    """f0 = a·b̄ + b·c as MathTex parts [f, =, t0, +, t1, ...]; f GREEN."""
    parts = [tex_name(out), "="]
    for i, t in enumerate(terms):
        if i:
            parts.append("+")
        parts.append(term_tex(t))
    m = MathTex(*parts, font_size=size, color=color)
    m[0].set_color(GREEN)
    return m


# ---------------------------------------------------------------- style constants
PITCH = 0.45        # rail pitch (local units)
PIN = 0.2           # AND input-line pitch
GATE_W = 1.2
GATE_HS = 0.25      # straight sides of the AND body; tip = top - HS - W/2
DOT_R = 0.085
RAIL_W = 4
LINE_W = 2.5
GATE_C = BLUE
LINE_C = FG
LBL = 40            # local label size


class Where:
    def __init__(self, s, x, y):
        self.s, self.off = s, P(x, y)


MID = Where(1.0, -4.0, 2.3)        # s3 clips 1-2: AND plane alone, large
BIG = Where(0.8, -5.3, 2.5)        # s3 clips 3-4: whole PLA
SMALL = Where(0.54, -6.0, 2.55)    # s3 clips 5-6 and handover: PLA at the left
PAL_SMALL = Where(0.54, 1.45, 2.55)
LBL_UP = 1.39                      # input / output labels grow back to ~30 when small


def place(m, w):
    return m.scale(w.s, about_point=ORIGIN).shift(w.off)


def remap(m, a, b):
    return m.shift(-a.off).scale(b.s / a.s, about_point=ORIGIN).shift(b.off)


def tint(m, c):
    """Recolour strokes and non-background fills (gate bodies keep their BG fill)."""
    for vm in m.family_members_with_points():
        if vm.get_stroke_width() > 0:
            vm.set_stroke(c)
        if vm.get_fill_opacity() > 0 and vm.get_fill_color().to_hex().lower() != BG.lower():
            vm.set_fill(c)
    return m


def hide(m):
    return m.set_opacity(0)


def anim(pairs):
    out = []
    for m, fn in pairs:
        m.generate_target()
        fn(m.target)
        out.append(MoveToTarget(m))
    return out


def apply(pairs):
    for m, fn in pairs:
        fn(m)


# ---------------------------------------------------------------- pieces
def panel(x0, x1, y_top, y_bot, color=DIM, op=0.14):
    r = Rectangle(width=x1 - x0, height=y_top - y_bot).set_stroke(width=0).set_fill(color, op)
    r.move_to(P((x0 + x1) / 2, (y_top + y_bot) / 2)).set_z_index(-2)
    return r


def plane_label(word, at, size=LBL):
    """'AND plane' as two centred lines, DIM."""
    g = VGroup(T(word, size, DIM), T("plane", size, DIM)).arrange(DOWN, buff=0.12)
    return g.move_to(at)


def rail_labels(names, ys, x, color=BLUE, size=LBL):
    return VGroup(*[sig(n, size, color).move_to(P(x, y), aligned_edge=LEFT) for n, y in zip(names, ys)])


def rails(names, x0, x1, top=0.0, pitch=PITCH, color=BLUE, label_x=None, size=LBL):
    """Plain horizontal rails from a name list (e.g. ["q0", "q0'"]), labelled at label_x."""
    g = VGroup()
    g.ys = [top - i * pitch for i in range(len(names))]
    g.lines = [Line(P(x0, y), P(x1, y)).set_stroke(color, RAIL_W) for y in g.ys]
    g.add(*g.lines)
    g.labels = None
    if label_x is not None:
        g.labels = rail_labels(names, g.ys, label_x, color, size)
        g.add(g.labels)
    return g


def input_bank(inputs=("a", "b", "c"), x_end=7.1, color=BLUE, top=0.0, pitch=PITCH,
               size=LBL, split_x=0.9):
    """Each input: label, wire, split dot, inverter branch, and its rail pair (x, x̄)."""
    b = VGroup()
    b.labels, b.wires, b.splits, b.branches, b.invs, b.rails, b.rail_ys = [], [], [], [], [], [], []
    b.names = []
    for k, n in enumerate(inputs):
        y = top - 2 * k * pitch
        yb = y - pitch
        lab = sig(n, size, color).move_to(P(0, y))
        wire = Line(P(0.3, y), P(split_x, y)).set_stroke(color, RAIL_W)
        sd = Dot(P(split_x, y), radius=DOT_R * 0.9, color=color)
        x1 = split_x + 0.22
        br = poly([(split_x, y), (split_x, yb), (x1, yb)], color, RAIL_W)
        tri = Polygon(P(x1, yb + 0.17), P(x1, yb - 0.17), P(x1 + 0.34, yb)).set_stroke(color, 3)
        tri.set_fill(BG, 1)
        bub = Circle(radius=0.065).set_stroke(color, 3).set_fill(BG, 1).move_to(P(x1 + 0.405, yb))
        r1 = Line(P(split_x, y), P(x_end, y)).set_stroke(color, RAIL_W)
        r2 = Line(P(x1 + 0.47, yb), P(x_end, yb)).set_stroke(color, RAIL_W)
        b.labels.append(lab)
        b.wires.append(wire)
        b.splits.append(sd)
        b.branches.append(br)
        b.invs.append(VGroup(tri, bub))
        b.rails += [r1, r2]
        b.rail_ys += [y, yb]
        b.names += [n, n + "'"]
    b.add(*b.labels, *b.wires, *b.rails, *b.branches, *b.invs, *b.splits)
    return b


def and_body_down(w=GATE_W, hs=GATE_HS):
    """AND gate pointing down; flat top centred on the origin."""
    r = w / 2
    k = 0.5523 * r
    b = VMobject()
    b.start_new_path(P(-r, 0))
    b.add_line_to(P(r, 0))
    b.add_line_to(P(r, -hs))
    b.add_cubic_bezier_curve_to(P(r, -hs - k), P(k, -hs - r), P(0, -hs - r))
    b.add_cubic_bezier_curve_to(P(-k, -hs - r), P(-r, -hs - k), P(-r, -hs))
    b.add_line_to(P(-r, 0))
    return b


def and_row(gate_x, rail_ys, top_y, color=GATE_C, pin=PIN, stub=0.35):
    """AND gates below the rails; gate g has one input line per rail (line i rises to rail i)
    and a dot where it meets it. .gates .lines[g][i] .dots[g][i] .stubs[g] .tip_y .stub_y"""
    n = len(rail_ys)
    w = max(GATE_W, pin * (n - 1) + 0.4)
    row = VGroup()
    row.gates, row.lines, row.dots, row.stubs = [], [], [], []
    tip = top_y - GATE_HS - w / 2
    for gx in gate_x:
        body = and_body_down(w).set_stroke(color, 4).set_fill(BG, 1).shift(P(gx, top_y))
        body.set_z_index(1)
        ls, ds = [], []
        for i, ry in enumerate(rail_ys):
            x = gx + (i - (n - 1) / 2) * pin
            ls.append(Line(P(x, top_y), P(x, ry)).set_stroke(LINE_C, LINE_W))
            ds.append(Dot(P(x, ry), radius=DOT_R, color=FG).set_z_index(2))
        st = Line(P(gx, tip), P(gx, tip - stub)).set_stroke(LINE_C, 3)
        row.gates.append(body)
        row.lines.append(ls)
        row.dots.append(ds)
        row.stubs.append(st)
        row.add(*ls, body, *ds, st)
    row.tip_y, row.stub_y, row.w = tip, tip - stub, w
    return row


def or_body_right(L=0.95, h=0.75, d=0.14):
    """OR gate pointing right; the middle of its concave back at the origin."""
    hh = h / 2
    b = VMobject()
    b.start_new_path(P(0, hh))
    b.add_cubic_bezier_curve_to(P(L * 0.5, hh), P(L * 0.85, hh * 0.6), P(L, 0))
    b.add_cubic_bezier_curve_to(P(L * 0.85, -hh * 0.6), P(L * 0.5, -hh), P(0, -hh))
    b.add_cubic_bezier_curve_to(P(d, -hh * 0.4), P(d, hh * 0.4), P(0, hh))
    return b


def or_body_down(L=0.9, h=0.8):
    """OR gate pointing down; back at the origin, tip at (0, -L)."""
    return or_body_right(L, h).rotate(-PI / 2, about_point=ORIGIN)


def or_row_right(prod_x, ys, back_x, names, dys=(0.22, 0.0, -0.22), L=0.95, color=GATE_C):
    """Programmable OR gates stacked at the right: OR k has one input line per product line
    (prod_x[j]), a dot on each crossing. .gates .lines[k][j] .dots[k][j] .fwires .flabels"""
    row = VGroup()
    row.gates, row.lines, row.dots, row.fwires, row.flabels = [], [], [], [], []
    for k, oy in enumerate(ys):
        body = or_body_right(L).set_stroke(color, 4).set_fill(BG, 1).shift(P(back_x, oy))
        body.set_z_index(1)
        ls = [Line(P(px, oy + dy), P(back_x + 0.14, oy + dy)).set_stroke(LINE_C, LINE_W)
              for px, dy in zip(prod_x, dys)]
        ds = [Dot(P(px, oy + dy), radius=DOT_R, color=FG).set_z_index(2) for px, dy in zip(prod_x, dys)]
        fw = Line(P(back_x + L, oy), P(back_x + L + 0.4, oy)).set_stroke(GREEN, RAIL_W)
        fl = sig(names[k], LBL, GREEN).next_to(fw.get_end(), RIGHT, buff=0.12)
        row.gates.append(body)
        row.lines.append(ls)
        row.dots.append(ds)
        row.fwires.append(fw)
        row.flabels.append(fl)
        row.add(*ls, body, *ds, fw, fl)
    return row


def fixed_line(gx, tip_y, ix, top_y, bend=0.35, color=LINE_C):
    """PAL's fixed OR wiring: down from an AND tip, across, down into the OR gate's back."""
    return poly([(gx, tip_y), (gx, tip_y - bend), (ix, tip_y - bend), (ix, top_y - 0.1)], color, 3)


def made_twice_tag(size=30):
    return VGroup(T("made", size, RED), T("twice", size, RED)).arrange(DOWN, buff=0.1)


def count_label(n, size=34):
    return T(f"{n} AND gates", size, GOLD)


def cost_line():
    return T("This simplifies the structure, but at the cost of lower efficiency", 28).move_to(P(0, -3.1))


# ---------------------------------------------------------------- the PLA (p. 72)
RAILS = ["a", "a'", "b", "b'", "c", "c'"]
RI = {n: i for i, n in enumerate(RAILS)}
GX_PLA = [2.7, 4.5, 6.3]
OY = [-4.6, -5.55, -6.5]
OR_BACK = 7.5
PLA_TERMS = [("a", "b'"), ("b", "c"), ("a'", "c'")]
F_TERMS = [[0, 1], [0, 2]]                         # f0 = a·b̄ + b·c, f1 = a·b̄ + ā·c̄


def build_pla():
    p = VGroup()
    p.bank = input_bank(x_end=7.1)
    ys = p.bank.rail_ys
    gtop = ys[-1] - 0.4
    p.ands = and_row(GX_PLA, ys, gtop)
    p.prods = [Line(P(gx, p.ands.stub_y), P(gx, OY[-1] - 0.4)).set_stroke(LINE_C, 3) for gx in GX_PLA]
    p.ors = or_row_right(GX_PLA, OY, OR_BACK, ["f0", "f1", "f2"])
    p.and_panel = panel(1.7, 7.4, ys[0] + 0.3, p.ands.tip_y - 0.1)
    p.or_panel = panel(1.7, 7.4, OY[0] + 0.45, OY[-1] - 0.45)
    p.core = VGroup(p.and_panel, p.or_panel, p.bank, p.ands, *p.prods, p.ors)
    # texts (big layouts only)
    p.rail_labels = rail_labels(RAILS, ys, 7.3)
    p.and_label = plane_label("AND", P(0.8, gtop - 0.45))
    p.or_label = plane_label("OR", P(0.8, OY[1]))
    p.terms = []
    for g, t in enumerate(PLA_TERMS):
        m = MathTex(term_tex(t), font_size=LBL)
        m.next_to(p.ands.stubs[g], RIGHT, buff=0.12).align_to(p.ands.stubs[g], UP).shift(0.02 * DOWN)
        p.terms.append(m)
    p.forms, p.form_rest = [], []
    for k, idx in enumerate(F_TERMS):
        f = formula_tex(f"f{k}", [PLA_TERMS[j] for j in idx], LBL)
        f.shift(p.ors.flabels[k].get_center() - f[0].get_center())
        p.forms.append(f)
        p.form_rest.append(VGroup(*f[1:]))
    p.sop = T("sum of products", LBL - 4).next_to(p.forms[0], UP, buff=0.35).align_to(p.forms[0], LEFT)
    p.all = VGroup(p.core, p.rail_labels, p.and_label, p.or_label, *p.terms, *p.forms, p.sop)
    return p


def st_pla_gate(p, g):
    keep = [RI[n] for n in PLA_TERMS[g]]
    return [(d, hide) for i, d in enumerate(p.ands.dots[g]) if i not in keep]


def st_pla_or(p, k):
    return [(d, hide) for j, d in enumerate(p.ors.dots[k]) if j not in F_TERMS[k]]


def pla_spare_parts(p):
    o = p.ors
    return [o.gates[2], *o.lines[2], *o.dots[2], o.fwires[2], o.flabels[2]]


def st_pla_spare(p):
    return [(m, lambda m: tint(m, DIM)) for m in pla_spare_parts(p)]


def pla_route(p):
    """The shared a·b̄ gate, its product line and its two OR inputs."""
    o = p.ors
    return [p.ands.gates[0], p.ands.stubs[0], p.prods[0], o.lines[0][0], o.lines[1][0],
            o.dots[0][0], o.dots[1][0]]


def st_pla_once(p):
    return [(m, lambda m: tint(m, YELLOW)) for m in pla_route(p)]


def small_labels(p):
    return [*p.bank.labels, *p.ors.flabels]


def small_pla():
    """The programmed PLA as it sits at the left in the handover."""
    p = build_pla()
    place(p.all, SMALL)
    for g in range(3):
        apply(st_pla_gate(p, g))
    for k in range(2):
        apply(st_pla_or(p, k))
    apply(st_pla_spare(p))
    apply(st_pla_once(p))
    for m in small_labels(p):
        m.scale(LBL_UP)
    return p


# ---------------------------------------------------------------- the PAL (p. 73)
GX_PAL = [2.7, 4.3, 6.2, 7.8]
PAL_OR_X = [3.5, 7.0]                     # left OR (fn / f1) takes gates 0-1, right (f0) 2-3
PAL_TERMS = [("a", "b'"), ("a'", "c'"), ("a", "b'"), ("b", "c")]


def build_pal(out_names=("fn", "f0")):
    p = VGroup()
    p.bank = input_bank(x_end=8.6)
    ys = p.bank.rail_ys
    gtop = ys[-1] - 0.4
    p.ands = and_row(GX_PAL, ys, gtop)
    tip = p.ands.tip_y
    or_top = tip - 0.7
    p.ors, p.fixed, p.fwires, p.flabels = [], [], [], []
    for k, ox in enumerate(PAL_OR_X):
        body = or_body_down().set_stroke(GATE_C, 4).set_fill(BG, 1).shift(P(ox, or_top))
        body.set_z_index(1)
        fw = Line(P(ox, or_top - 0.9), P(ox, or_top - 1.25)).set_stroke(GREEN, RAIL_W)
        fl = sig(out_names[k], LBL, GREEN).next_to(fw.get_end(), DOWN, buff=0.1)
        p.ors.append(body)
        p.fwires.append(fw)
        p.flabels.append(fl)
    for g, gx in enumerate(GX_PAL):
        ox = PAL_OR_X[g // 2]
        p.fixed.append(fixed_line(gx, tip, ox + (-0.2 if g % 2 == 0 else 0.2), or_top))
    p.and_panel = panel(1.7, 8.75, ys[0] + 0.3, tip - 0.1)
    p.or_panel = panel(1.7, 8.75, tip - 0.2, or_top - 1.0)
    # where a would-be shared wire from gate 1 would head (toward f0's OR gate)
    p.ghost_a = VectorizedPoint(P(GX_PAL[1], tip - 0.35))
    p.ghost_b = VectorizedPoint(P(5.55, tip - 0.35))
    p.pocket = VectorizedPoint(P(0.85, gtop - 0.45))      # left of gate 0, under the inverters
    p.core = VGroup(p.and_panel, p.or_panel, p.bank, *[x for x in p.ands if x not in p.ands.stubs],
                    *p.fixed, *p.ors, *p.fwires, *p.flabels)
    p.rail_labels = rail_labels(RAILS, ys, 8.8)
    p.all = VGroup(p.core, p.rail_labels, p.ghost_a, p.ghost_b, p.pocket)
    return p


def st_pal_program(p):
    out = []
    for g, t in enumerate(PAL_TERMS):
        keep = [RI[n] for n in t]
        out += [(d, hide) for i, d in enumerate(p.ands.dots[g]) if i not in keep]
    return out


def st_pal_first(p):
    return [(m, lambda m: tint(m, YELLOW)) for m in (p.ands.gates[2], p.fixed[2])]


def st_pal_second(p):
    return [(m, lambda m: tint(m, RED)) for m in (p.ands.gates[0], p.fixed[0])]


def pal_small_labels(p):
    return [*p.bank.labels, *p.flabels]


def small_pal(programmed=True, out_names=("f1", "f0")):
    """The PAL as it sits at the right in the handover (s5 flashes it)."""
    p = build_pal(out_names)
    place(p.all, PAL_SMALL)
    for m in pal_small_labels(p):
        m.scale(LBL_UP)
    if programmed:
        apply(st_pal_program(p))
        apply(st_pal_first(p))
        apply(st_pal_second(p))
    return p


# ---------------------------------------------------------------- titles, shots
TITLE_C = P(0, 3.2)
PLA_HEAD_C = P(-3.5, 3.25)
PAL_HEAD_C = P(3.8, 3.25)


def pla_title():
    word = T("PLA", 44, YELLOW)
    rest = T(": programmable logic array", 44)
    rest.next_to(word, RIGHT, buff=0.06)
    rest.shift(UP * (word.get_bottom()[1] - rest[0].get_bottom()[1]))
    VGroup(word, rest).move_to(TITLE_C)
    return word, rest


def opening_shot():
    """s2's last frame: the YELLOW "PLA" alone, where this scene's title puts it."""
    return VGroup(pla_title()[0])


def inherited_shot():
    """s2's handover shot if it defines one (its "PLA" may sit a little off ours), else ours."""
    try:
        from lib.paths import load_scene
        return load_scene("ch4_s2_needs").handover_shot()
    except Exception:
        return opening_shot()


def to_header(m):
    return m.scale(30 / 44, about_point=TITLE_C).shift(PLA_HEAD_C - TITLE_C)


def pal_header():
    return T("PAL: programmable array logic", 30, t2c={"PAL": YELLOW}).move_to(PAL_HEAD_C)


FORM_X = -0.05                     # centred in the gap between the two drawings
FORM_YS = (-1.6, -2.3)             # f0 above f1: both drawings implement both
COUNT_Y = -1.95


def formula_row(yellow=True):
    fs = []
    for k, y in enumerate(FORM_YS):
        f = formula_tex(f"f{k}", [PLA_TERMS[j] for j in F_TERMS[k]], 40)
        f.move_to(P(FORM_X, y))
        if yellow:
            f[2].set_color(YELLOW)
        fs.append(f)
    eq_x = fs[0][1].get_center()[0]                 # line the two = signs up
    fs[1].shift((eq_x - fs[1][1].get_center()[0]) * RIGHT)
    return fs


def counts():
    return (count_label(3).move_to(P(PLA_HEAD_C[0], COUNT_Y)),
            count_label(4).move_to(P(PAL_HEAD_C[0], COUNT_Y)))


def twice_tag(pal):
    return made_twice_tag().move_to(pal.pocket.get_center())


def handover_shot():
    """Last frame: PLA (left) and PAL (right), headers, the two formulas, the counts, the cost line."""
    pla = small_pla()
    pal = small_pal()
    word, rest = pla_title()
    to_header(word)
    to_header(rest)
    f0, f1 = formula_row()
    c3, c4 = counts()
    head, tag, cost = pal_header(), twice_tag(pal), cost_line()
    shot = VGroup(pla.core, pal.core, word, rest, head, tag, f0, f1, c3, c4, cost)
    shot.pla, shot.pal, shot.pla_head, shot.pal_head = pla.core, pal.core, VGroup(word, rest), head
    shot.tag, shot.f0, shot.f1, shot.forms = tag, f0, f1, [f0, f1]
    shot.c3, shot.c4, shot.counts, shot.cost = c3, c4, [c3, c4], cost
    return shot


# ---------------------------------------------------------------- the scene
class PlaPal(NarratedScene):
    def construct(self):
        self.pla = build_pla()
        place(self.pla.all, MID)
        self.word, self.rest = pla_title()
        self.inherited = inherited_shot()
        self.add(self.inherited)                 # s2's last frame: the YELLOW "PLA"
        self.parts = []                          # every PLA piece on screen (top level)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.remove(*self.mobjects)              # invisible cut to the canonical handover shot
        self.add(handover_shot())
        self.wait(1.0)

    def show(self, *mobs):
        self.parts += list(mobs)
        return mobs

    # -- c4.pla.1: build the AND plane
    def clip1(self):
        p = self.pla
        b = p.bank
        with self.say("c4.pla.1") as c:
            self.play(*during(ReplacementTransform(self.inherited[0], self.word), 0, 0.5),
                      *during(appear(self.rest, shift=None), 0.55, 1.0),
                      run_time=min(1.8, c.until("inputs")))  # early: title
            for k, cue in enumerate(("input a", "input bee", "input see")):
                c.wait_until(cue)
                self.show(b.labels[k], b.wires[k])
                self.play(*appear(b.labels[k], shift=0.2 * RIGHT), Create(b.wires[k]),
                          run_time=0.8)
            c.wait_until("inverters")
            anims = []
            for k in range(3):
                self.show(b.branches[k], b.invs[k], b.splits[k])
                anims.append(AnimationGroup(FadeIn(b.splits[k]), Create(b.branches[k]),
                                            FadeIn(b.invs[k]), lag_ratio=0.3))
            self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=min(2.0, c.until("itself")))
            c.wait_until("plane")
            self.show(*b.rails)
            self.play(*[Create(r) for r in b.rails], run_time=min(1.6, 0.6 * c.until("called the")))
            c.wait_until("called the")
            self.show(p.and_panel, p.and_label, *p.rail_labels)
            self.play(FadeIn(p.and_panel), *appear(p.and_label, shift=None),
                      *appear(*p.rail_labels, shift=None, lag=0.08), run_time=1.0)
            c.wait_until("gates")
            a = p.ands
            gate_anims = []
            for g in range(3):
                self.show(a.gates[g], *a.lines[g], a.stubs[g])
                gate_anims.append(AnimationGroup(*[Create(l) for l in a.lines[g]],
                                                 FadeIn(a.gates[g], shift=0.15 * DOWN), Create(a.stubs[g])))
            self.play(LaggedStart(*gate_anims, lag_ratio=0.3), run_time=min(1.8, c.until("full")))
            c.wait_until("full")
            dots = [d for g in range(3) for d in a.dots[g]]
            self.show(*dots)
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.06), run_time=1.6)
            self.play(*[d.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.5) for d in dots],
                      run_time=1.0)

    # -- c4.pla.2: programming the AND plane
    def clip2(self):
        p = self.pla
        a = p.ands
        cap = VGroup(T("Programmed by selectively removing connections", 30),
                     T("in the AND and OR planes – controlled by", 30),
                     T("fuses or memory bits", 30)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        cap.move_to(P(-0.4, -2.5))
        self.cap = cap
        with self.say("c4.pla.2") as c:
            self.play(*appear(*cap, lag=0.4), run_time=min(1.8, c.until("fuses")))  # early: slide caption, read whole
            c.wait_until("fuses")
            self.play(*recolor(list(cap[2]), YELLOW), run_time=1.0)
            c.wait_until("term")
            self.play(*anim(st_pla_gate(p, 0)), run_time=1.2)
            c.wait_until("that gate makes")
            self.show(p.terms[0])
            self.play(*appear(p.terms[0]), run_time=1.0)
            c.wait_until("one")
            one = MathTex("1", font_size=40, color=GREEN).next_to(a.stubs[0], LEFT, buff=0.14)
            one.align_to(a.stubs[0], UP)
            self.play(*appear(one), run_time=0.8)
            chips = []
            for k, (n, v) in enumerate((("a", "1"), ("b", "0"))):
                t = MathTex(f"{n} = {v}", font_size=36, color=BLUE)
                box = SurroundingRectangle(t, buff=0.1, corner_radius=0.08).set_stroke(BLUE, 2)
                chip = VGroup(box, t).next_to(p.bank.labels[k], LEFT, buff=0.3)
                chips.append(chip)
            c.wait_until("input a is one")
            self.play(*appear(chips[0], shift=0.2 * RIGHT), run_time=0.8)
            c.wait_until("input bee is zero")
            self.play(*appear(chips[1], shift=0.2 * RIGHT), run_time=0.8)
            c.wait_until("each")
            self.play(*flash(a.gates, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("others")
            self.play(*disappear(*chips, one), *anim(st_pla_gate(p, 1) + st_pla_gate(p, 2)), run_time=1.2)
            c.wait_until("bee and see")
            self.show(p.terms[1])
            self.play(*appear(p.terms[1]), run_time=0.9)
            c.wait_until("not a and not see")
            self.show(p.terms[2])
            self.play(*appear(p.terms[2]), run_time=0.9)

    # -- c4.pla.3: the OR plane
    def clip3(self):
        p = self.pla
        o = p.ors
        # parts not yet shown move to the BIG layout at once
        shown = set(id(m) for m in self.parts)
        for m in [p.or_panel, p.or_label, *p.prods, o, *p.forms, p.sop]:
            remap(m, MID, BIG)
        moves = []
        for m in self.parts:
            m.generate_target()
            remap(m.target, MID, BIG)
            moves.append(MoveToTarget(m))
        with self.say("c4.pla.3") as c:
            self.play(*during(disappear(*self.cap), 0, 0.4), *during(moves, 0.25, 1.0),
                      run_time=min(1.6, c.until("or plane") + 0.6))
            self.show(p.or_panel, p.or_label)
            self.play(FadeIn(p.or_panel), *appear(p.or_label, shift=None), run_time=0.8)
            c.wait_until("sums")
            or_parts = []
            for k in range(3):
                self.show(o.gates[k], *o.lines[k], o.fwires[k], o.flabels[k])
                or_parts.append(AnimationGroup(*[Create(l) for l in o.lines[k]],
                                               FadeIn(o.gates[k], shift=0.15 * RIGHT), Create(o.fwires[k]),
                                               FadeIn(o.flabels[k])))
            self.show(*p.prods)
            self.play(*[Create(l) for l in p.prods], LaggedStart(*or_parts, lag_ratio=0.3), run_time=1.8)
            dots = [d for k in range(3) for d in o.dots[k]]
            self.show(*dots)
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.08), run_time=1.0)
            c.wait_until("again by keeping")
            self.play(*[d.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.6) for d in dots],
                      run_time=1.2)
            c.wait_until("f0")
            self.play(*anim(st_pla_or(p, 0)), run_time=1.0)
            self.show(p.form_rest[0])
            self.play(*appear(p.form_rest[0], shift=None), run_time=1.0)
            c.wait_until("f1")
            self.play(*anim(st_pla_or(p, 1)), run_time=1.0)
            self.show(p.form_rest[1])
            self.play(*appear(p.form_rest[1], shift=None), run_time=1.0)
            route = [p.prods[0], o.lines[0][0], o.lines[1][0]]
            self.play(*[VShowPassingFlash(m.copy().set_stroke(YELLOW, 7), time_width=0.6) for m in route],
                      run_time=1.2)
            c.wait_until("spare")
            self.play(*anim(st_pla_spare(p)), run_time=1.0)
            c.wait_until("sop")
            self.show(p.sop)
            self.play(*appear(p.sop), run_time=1.0)

    # -- c4.pla.4: minterm vs product term
    def clip4(self):
        x0 = 2.0
        title = T("“minterm”", 36)
        r1 = T("minterm: every input,", 30)
        e1t = T("e.g.", 30)
        e1m = MathTex(r"a\cdot\overline{b}\cdot c", font_size=40)
        r3 = T("product term: any AND", 30)
        r4t = T("of inputs, e.g.", 30)
        r4m = MathTex(r"a\cdot\overline{b}\cdot", font_size=40)
        gap = DashedVMobject(Square(0.34), num_dashes=12).set_stroke(DIM, 2)
        title.move_to(P(x0, 2.55), aligned_edge=LEFT)
        r1.move_to(P(x0, 1.85), aligned_edge=LEFT)
        e1t.move_to(P(x0 + 0.4, 1.35), aligned_edge=LEFT)
        e1m.next_to(e1t, RIGHT, buff=0.15).align_to(e1t[0], DOWN)
        r3.move_to(P(x0, 0.7), aligned_edge=LEFT)
        r4t.move_to(P(x0 + 0.4, 0.2), aligned_edge=LEFT)
        r4m.next_to(r4t, RIGHT, buff=0.15).align_to(r4t[0], DOWN)
        gap.next_to(r4m, RIGHT, buff=0.1).align_to(r4m, DOWN)
        rows = VGroup(title, r1, e1t, e1m, r3, r4t, r4m, gap)
        card = SurroundingRectangle(rows, buff=0.25, corner_radius=0.12).set_stroke(DIM, 2)
        self.card = VGroup(card, rows)
        with self.say("c4.pla.4") as c:
            self.play(FadeIn(card), run_time=0.8)
            c.wait_until("the slides call")
            self.play(*appear(title), run_time=1.0)  # early: heading; the slides' word "minterms" is said now
            c.wait_until("strict")
            self.play(*appear(r1), run_time=1.0)
            c.wait_until("like a and not bee")
            self.play(*appear(e1t, e1m, shift=None), run_time=1.0)
            c.wait_until("loose")
            self.play(*appear(r3), run_time=1.0)
            self.play(*appear(r4t, r4m, shift=None), FadeIn(gap), run_time=1.0)
            c.wait_until("product")
            self.play(*recolor(list(r3[:11]), YELLOW), *flash([VGroup(*r3[:11]).copy()], run_time=1.5),
                      run_time=1.5)

    # -- c4.pla.5: the PAL
    def clip5(self):
        p = self.pla
        texts = [p.rail_labels, p.and_label, p.or_label, *p.terms, *p.form_rest, p.sop, self.card]
        tid = set(id(m) for m in texts)
        core_parts = [m for m in self.parts if id(m) not in tid]
        lab_ids = set(id(m) for m in small_labels(p))
        moves = []
        for m in core_parts:
            m.generate_target()
            remap(m.target, BIG, SMALL)
            if id(m) in lab_ids:
                m.target.scale(LBL_UP)
            moves.append(MoveToTarget(m))
        for m in (self.word, self.rest):
            m.generate_target()
            to_header(m.target)
            moves.append(MoveToTarget(m))
        pal = build_pal()
        place(pal.all, PAL_SMALL)
        for m in pal_small_labels(pal):
            m.scale(LBL_UP)
        self.pal = pal
        head = pal_header()
        self.pal_head = head
        b, a = pal.bank, pal.ands
        with self.say("c4.pla.5") as c:
            self.play(*during(disappear(*texts), 0, 0.4), *during(moves, 0.3, 1.0), run_time=2.0)
            and_part = [pal.and_panel, *b.labels, *b.wires, *b.splits, *b.branches, *b.invs, *b.rails,
                        *a.gates, *[l for g in a.lines for l in g], *[d for g in a.dots for d in g]]
            self.play(*appear(head), *[FadeIn(m) for m in and_part], run_time=min(1.5, c.until("fixed")))
            c.wait_until("fixed")
            self.play(FadeIn(pal.or_panel), *[Create(f) for f in pal.fixed], *[FadeIn(m) for m in pal.ors],
                      *[Create(w) for w in pal.fwires], *appear(*pal.flabels, shift=None), run_time=1.5)
            c.wait_until("each or gate")
            self.play(*[VShowPassingFlash(f.copy().set_stroke(YELLOW, 7), time_width=0.6) for f in pal.fixed],
                      run_time=1.5)
            c.wait_until("only")
            dots = [d for g in a.dots for d in g]
            self.play(*[d.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.7) for d in dots],
                      run_time=1.2)
            c.wait_until("cost")
            self.cost = cost_line()
            self.play(*appear(self.cost), run_time=1.2)  # early: the slide's line, said in paraphrase
            c.wait_until("share")
            ghost = DashedLine(pal.ghost_a.get_center(), pal.ghost_b.get_center(),
                               dash_length=0.08).set_stroke(RED, 3)
            x = cross_mark(RED, r=0.12).move_to(pal.ghost_b.get_center() + 0.2 * RIGHT)
            self.ghost = VGroup(ghost, x)
            self.play(Create(ghost), run_time=1.2, rate_func=linear)
            self.play(FadeIn(x, scale=1.4), run_time=0.6)

    # -- c4.pla.6: the same two functions in both
    def clip6(self):
        p, pal = self.pla, self.pal
        f0, f1 = formula_row(yellow=False)
        ref = build_pal(("f1", "f0"))
        place(ref.all, PAL_SMALL)
        for m in pal_small_labels(ref):
            m.scale(LBL_UP)
        new_f1 = ref.flabels[0]
        tag = twice_tag(pal)
        c3, c4 = counts()
        with self.say("c4.pla.6") as c:
            # the two outputs flash in the PLA, and their formulas come up between the drawings
            self.play(*disappear(self.ghost), *flash(p.ors.flabels[:2], run_time=1.2, time_width=1.5),
                      *during(appear(f0, f1, lag=0.3), 0.35, 1.0), run_time=1.8)
            c.wait_until("eff one")
            self.play(*swap(pal.flabels[0], new_f1), *anim(st_pal_program(pal)), run_time=1.2)
            c.wait_until("the term")
            self.play(*recolor([f0[2], f1[2]], YELLOW), *flash([f0[2], f1[2]], run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("once")
            self.play(*anim(st_pla_once(p)), run_time=1.2)
            route = [p.prods[0], p.ors.lines[0][0], p.ors.lines[1][0]]
            self.play(*[VShowPassingFlash(m.copy().set_stroke(YELLOW, 7), time_width=0.6) for m in route],
                      run_time=1.2)
            c.wait_until("twice")
            self.play(*anim(st_pal_first(pal)), run_time=1.0)
            self.play(*anim(st_pal_second(pal)), *appear(tag), run_time=1.2)
            c.wait_until("count")
            self.play(*appear(c3), run_time=0.9)
            c.wait_until("the pal needs")
            self.play(*appear(c4), run_time=0.9)
            c.wait_until("lower")
            self.play(FlashAround(self.cost, run_time=2, time_width=1.5), run_time=2)
