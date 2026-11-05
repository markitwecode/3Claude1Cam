"""Chapter 1, scene 8: nine products, three vanish, six pair up; the formula derived, checked,
recapped, and where it leads. Clips c1.comp.1 – c1.comp.5.

SHARED pieces:
  ijk_table()  <- s5's i/j/k table (copied from ch1_s5_rules); slides in from s5's parked pose
  hook_tuple() <- s1's tuple formula (copied from ch1_s1_hook)
  s4_inset()   <- s4's a x b = (0,0,6) shot, drawn 2D (matched to ch1_s4_define)
  CROSS_COL    <- TEAL, s4's colour for a x b
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403
from manim.utils.space_ops import rotation_about_z, rotation_matrix  # noqa: E402

from lib.effects import FlashAround, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

A_COL, B_COL, C_COL = BLUE, YELLOW, PINK
CROSS_COL = TEAL           # a x b (s4: TEAL)
FACE_COL = TEAL
PAIR_COL = {"k": GOLD, "i": PURPLE, "j": GREEN}
PAIRS = {"k": ((0, 1), (1, 0)), "i": ((1, 2), (2, 1)), "j": ((2, 0), (0, 2))}   # (positive, negative)
SLOT = {"i": 2, "j": 9, "k": 16}            # index of "(" of each component in `full`
OFF = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)]
U = "ijk"
TABLE = [["0", "k", "-j"], ["-k", "0", "i"], ["j", "-i", "0"]]   # row x column
CS = 46                                       # grid font size

COLMAP = {**{f"a_{n}": A_COL for n in "123"}, **{f"b_{n}": B_COL for n in "123"},
          **{f"c_{n}": C_COL for n in "123"},
          r"\mathbf a": A_COL, r"\mathbf b": B_COL, r"\mathbf c": C_COL}


def M(*parts, size=44, color=FG, cmap=COLMAP):
    src = " ".join(parts)
    used = {k: v for k, v in (cmap or {}).items() if k in src}
    return MathTex(*parts, font_size=size, color=color, tex_to_color_map=used)


def strut(*parts, size=CS, color=FG):
    """Parts between invisible parentheses, so every entry has the same height and baseline."""
    m = M("(", *parts, ")", size=size, color=color)
    m[0].set_opacity(0)
    m[-1].set_opacity(0)
    return m


# ── 3D: s4's camera as a plain projection ──────────────────────────────────────
PHI, THETA = 70 * DEGREES, -60 * DEGREES
_ROT = rotation_matrix(-PHI, RIGHT) @ rotation_about_z(-THETA - 90 * DEGREES)


def proj(v, s=0.6):
    q = _ROT @ np.asarray(v, dtype=float)
    return np.array([q[0] * s, q[1] * s, 0.0])


def vec_arrow(p, q, color, width=6, tip=0.24):
    return Arrow(p, q, buff=0, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)


# ── shared pieces (placeholders) ───────────────────────────────────────────────
TAB_SIZE, TAB_CW, TAB_RH = 52, 1.35, 1.05     # s5's table
TAB_PARK_SCALE = 0.6                          # s5 leaves it parked top-right at this scale
TAB_SCALE = 0.66                              # its working size here


def tab_xy(r, c):
    """s5's tab_xy, around ORIGIN: centre of cell (r, c); row/column 0 are the headers."""
    x0, y0 = -2 * TAB_CW, 2 * TAB_RH
    return np.array([x0 + TAB_CW * (c + 0.5), y0 - TAB_RH * (r + 0.5), 0])


def tab_cell(r, c, letter, minus=False, color=FG):
    """s5's cell: bold letter, the minus its own RED part."""
    parts = (["-"] if minus else []) + [rf"\mathbf {letter}"]
    m = MathTex(*parts, font_size=TAB_SIZE, color=color)
    if minus:
        m[0].set_color(RED)
    return m.move_to(tab_xy(r, c))


def ijk_table():
    """SHARED with s5 (ch1_s5_rules build_table / cell / tab_xy), full size around ORIGIN.
    Entries row x column; `.ents[r][c]` has `.unit` and `.sign` (None if positive)."""
    x0, x1, y0, y1 = -2 * TAB_CW, 2 * TAB_CW, 2 * TAB_RH, -2 * TAB_RH
    corner = MathTex(r"\times", font_size=TAB_SIZE, color=DIM).move_to(tab_xy(0, 0))
    cols = [MathTex(rf"\mathbf {n}", font_size=TAB_SIZE, color=FG).move_to(tab_xy(0, c + 1))
            for c, n in enumerate(U)]
    rows = [MathTex(rf"\mathbf {n}", font_size=TAB_SIZE, color=FG).move_to(tab_xy(r + 1, 0))
            for r, n in enumerate(U)]
    hline = Line([x0 + 0.15, y0 - TAB_RH, 0], [x1, y0 - TAB_RH, 0]).set_stroke(DIM, 2)
    vline = Line([x0 + TAB_CW, y0 - 0.12, 0], [x0 + TAB_CW, y1, 0]).set_stroke(DIM, 2)
    ents = [[None] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            e = TABLE[r][c]
            if e == "0":
                m = tab_cell(r + 1, c + 1, "0", color=DIM)
            else:
                m = tab_cell(r + 1, c + 1, e[-1], minus=e.startswith("-"))
            m.sign, m.unit = (m[0], m[1]) if e.startswith("-") else (None, m[0])
            ents[r][c] = m
    g = VGroup(corner, *cols, *rows, hline, vline, *[e for row in ents for e in row])
    g.ents = ents
    return g


HOOK_PARTS = [r"\mathbf a", r"\times", r"\mathbf b", "=", "(",
              "a_2", "b_3", "-", "a_3", "b_2", r",\ ",
              "a_3", "b_1", "-", "a_1", "b_3", r",\ ",
              "a_1", "b_2", "-", "a_2", "b_1", ")"]


def hook_tuple(size=40):
    """SHARED with s1 (ch1_s1_hook make_formula): same parts and colouring.
    Entries are parts 5-9, 11-15, 17-21."""
    f = MathTex(*HOOK_PARTS, font_size=size)
    for part, g in zip(HOOK_PARTS, f):
        if part == r"\mathbf a" or part.startswith("a_"):
            g.set_color(A_COL)
        elif part == r"\mathbf b" or part.startswith("b_"):
            g.set_color(B_COL)
    return f


def coord_label(name, coords, color, size=34):
    """s4's coordinate label: coloured name, FG brackets, GOLD digits."""
    parts = [name, "=", "("]
    for i, v in enumerate(coords):
        parts += [str(v)] + ([","] if i < len(coords) - 1 else [])
    parts.append(")")
    lab = MathTex(*parts, font_size=size, color=FG)
    lab[0].set_color(color)
    for i, p in enumerate(parts):
        if p.isdigit():
            lab[i].set_color(GOLD)
    return lab


def s4_inset(max_w=5.3):
    """SHARED with s4 (ch1_s4_define): a still 2D drawing of its a x b = (0,0,6) shot. Same camera
    (phi 70, theta -60), 0.6 units per step, FG axes with ticks, faint floor grid, TEAL
    parallelogram (fill 0.45), a BLUE, b YELLOW, a x b TEAL (thicker), coordinate labels."""
    a, b, ab = (3, 0, 0), (1, 2, 0), (0, 0, 6)
    o = ORIGIN

    def P(v):
        return proj(v, 0.6)

    xr, yr, zr = (-1.5, 4.5), (-1, 3), (-1, 7)
    axes = VGroup(Line(P((xr[0], 0, 0)), P((xr[1], 0, 0))), Line(P((0, yr[0], 0)), P((0, yr[1], 0))),
                  Line(P((0, 0, zr[0])), P((0, 0, zr[1])))).set_stroke(FG, 2)
    ticks = VGroup()
    for k in range(-1, 5):
        if k:
            ticks.add(Line(P((k, 0, 0)) + 0.05 * UP, P((k, 0, 0)) + 0.05 * DOWN))
    for k in range(-1, 4):
        if k:
            ticks.add(Line(P((0, k, 0)) + 0.05 * UP, P((0, k, 0)) + 0.05 * DOWN))
    for k in range(-1, 8):
        if k:
            ticks.add(Line(P((0, 0, k)) + 0.05 * LEFT, P((0, 0, k)) + 0.05 * RIGHT))
    ticks.set_stroke(FG, 2)
    grid = VGroup(*[Line(P((x, yr[0], 0)), P((x, yr[1], 0))) for x in range(-1, 5) if x],
                  *[Line(P((xr[0], y, 0)), P((xr[1], y, 0))) for y in range(-1, 4) if y])
    grid.set_stroke(FG, 1.5, opacity=0.16)
    para = Polygon(P(o), P(a), P((4, 2, 0)), P(b)).set_fill(FACE_COL, 0.45).set_stroke(FACE_COL, 2)
    va = vec_arrow(P(o), P(a), A_COL, 5, 0.22)
    vb = vec_arrow(P(o), P(b), B_COL, 5, 0.22)
    vab = vec_arrow(P(o), P(ab), CROSS_COL, 7, 0.26)
    la = coord_label(r"\mathbf a", a, A_COL).next_to(va.get_end(), DOWN, buff=0.22)
    lb = coord_label(r"\mathbf b", b, B_COL).next_to(vb.get_end(), RIGHT, buff=0.3).shift(0.15 * UP)
    lab = coord_label(r"\mathbf a\times\mathbf b", ab, CROSS_COL).next_to(vab.get_end(), RIGHT, buff=0.2)
    for lbl in (la, lb, lab):
        set_backstroke(lbl)
    pic = VGroup(grid, axes, ticks, para, va, vb, vab, la, lb, lab)
    frame = RoundedRectangle(corner_radius=0.2, width=pic.width + 0.6, height=pic.height + 0.6)
    frame.set_stroke(DIM, 2).move_to(pic)
    g = VGroup(frame, pic)
    if g.width > max_w:
        g.scale(max_w / g.width)
    return g


# ── small pictures ─────────────────────────────────────────────────────────────
def hl_box(m, color=YELLOW):
    return SurroundingRectangle(m, color=color, buff=0.05, corner_radius=0.06,
                                stroke_width=2).set_fill(color, 0.15).set_z_index(-1)


def make_wheel(R=0.95, size=48):
    ang = {1: PI / 2, 2: PI / 2 - TAU / 3, 3: PI / 2 - 2 * TAU / 3}
    nodes = {n: M(str(n), size=size).move_to(R * np.array([np.cos(t), np.sin(t), 0]))
             for n, t in ang.items()}
    arcs = {}
    d = 0.42
    for p, q in ((1, 2), (2, 3), (3, 1)):
        arc = Arc(radius=R, start_angle=ang[p] - d, angle=-(TAU / 3 - 2 * d)).set_stroke(DIM, 4)
        arc.add_tip(tip_length=0.18, tip_width=0.18)
        arc.set_color(DIM)
        arcs[(p, q)] = arc
    return VGroup(*arcs.values(), *nodes.values()), nodes, arcs


def icon_split():
    l_box = RoundedRectangle(corner_radius=0.06, width=0.34, height=0.34).set_stroke(BLUE, 3)
    r_box = l_box.copy()
    VGroup(l_box, r_box).arrange(RIGHT, buff=0.14)
    return VGroup(l_box, r_box, M(r"\cdot", size=44).move_to(l_box), M(r"\times", size=30).move_to(r_box))


def icon_wrench():
    handle = Line([-0.3, -0.3, 0], [0.07, 0.07, 0]).set_stroke(FG, 7)
    head = Arc(radius=0.15, start_angle=PI / 4 + 0.85, angle=TAU - 1.7,
               arc_center=[0.18, 0.18, 0]).set_stroke(FG, 6)
    return VGroup(handle, head)


def icon_para():
    return Polygon([-0.38, -0.2, 0], [0.16, -0.2, 0], [0.38, 0.2, 0], [-0.16, 0.2, 0]).set_fill(
        FACE_COL, 0.45).set_stroke(FACE_COL, 3)


def icon_flip():
    kw = dict(buff=0, color=CROSS_COL, stroke_width=5, tip_length=0.15, max_tip_length_to_length_ratio=0.5)
    return VGroup(Arrow(DOWN * 0.28, UP * 0.28, **kw), Arrow(UP * 0.28, DOWN * 0.28, **kw)).arrange(RIGHT, buff=0.22)


def icon_strip():
    sq = VGroup(*[Square(0.2).set_stroke(FG, 2) for _ in range(3)]).arrange(RIGHT, buff=0.1)
    for s, col in zip(sq, (BLUE, TEAL, GREEN)):
        s.set_fill(col, 0.5)
    return sq


def icon_grid():
    g = VGroup(*[Square(0.16).set_stroke(FG, 1.5) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.04)
    for k in (0, 4, 8):
        g[k].set_fill(DIM, 0.8)
    return g


def build_recap():
    rows = [
        (icon_split(), T("Hamilton's product, split in two", 36)),
        (icon_wrench(), T("Torque, angular momentum, force", 36)),
        (icon_para(), M(r"|\mathbf a\times\mathbf b|=\text{area},\ \text{right-hand rule}", size=44)),
        (icon_flip(), M(r"\mathbf b\times\mathbf a=-\,\mathbf a\times\mathbf b,\qquad"
                        r"\mathbf a\times\mathbf a=\mathbf 0", size=44)),
        (icon_strip(), M(r"\mathbf a\times(\mathbf b+\mathbf c)=\mathbf a\times\mathbf b+"
                         r"\mathbf a\times\mathbf c", size=44)),
        (icon_grid(), T("Multiply out: the components", 36)),
    ]
    lines = VGroup()
    for k, (ic, tx) in enumerate(rows):
        y = 2.0 - k * 1.0
        ic.move_to([0, y, 0])
        tx.move_to([0, y, 0]).align_to(np.array([0.66, 0, 0]), LEFT)
        lines.add(VGroup(ic, tx))
    title = T("Recap", 48).next_to(lines, UP, buff=0.45).align_to(lines, LEFT)
    return VGroup(title, lines), title, lines


class BoxPic:
    """The slanted box of a=(3,0,0), b=(1,2,0), c=(1,1,2) in s4's camera."""

    def __init__(self, s=1.0, center=(-3.55, -0.2)):
        a, b, c = (np.array(v, dtype=float) for v in ((3, 0, 0), (1, 2, 0), (1, 1, 2)))
        o = np.zeros(3)

        def P(v):
            return proj(v, s)

        def face(*vs, op=0.12, w=2):
            return Polygon(*[P(v) for v in vs]).set_fill(FACE_COL, op).set_stroke(
                FACE_COL, w, opacity=0.85).set_z_index(-2)

        self.faces = [face(o, a, a + b, b), face(c, a + c, a + b + c, b + c), face(o, a, a + c, c),
                      face(b, a + b, a + b + c, b + c), face(a, a + b, a + b + c, a + c)]
        self.base = face(o, b, b + c, c, op=0.35, w=3)
        self.va = vec_arrow(P(o), P(a), A_COL)
        self.vb = vec_arrow(P(o), P(b), B_COL)
        self.vc = vec_arrow(P(o), P(c), C_COL)
        m = (b + c) / 2
        self.bxc = vec_arrow(P(m), P(m + np.cross(b, c)), CROSS_COL, width=7, tip=0.28)
        self.dot = Dot(P(o), radius=0.06, color=FG)
        self.la = M(r"\mathbf a", size=42).next_to(self.va.get_end(), DOWN, buff=0.12)
        self.lb = M(r"\mathbf b", size=42).next_to(self.vb.get_end(), RIGHT, buff=0.1).shift(0.12 * DOWN)
        self.lc = M(r"\mathbf c", size=42).next_to(self.vc.get_end(), LEFT, buff=0.12)
        self.lbxc = M(r"\mathbf b\times\mathbf c", size=40, color=CROSS_COL, cmap=None)
        self.lbxc.next_to(self.bxc.get_end(), RIGHT, buff=0.12)
        for lbl in (self.la, self.lb, self.lc, self.lbxc):
            set_backstroke(lbl)
        self.pic = VGroup(*self.faces, self.base, self.va, self.vb, self.vc, self.bxc, self.dot)
        self.labels = [self.la, self.lb, self.lc, self.lbxc]
        everything = VGroup(self.pic, *self.labels)
        everything.shift(np.array([*center, 0]) - everything.get_center())


class Components(NarratedScene):
    def construct(self):
        self.clip_expand()
        self.clip_pairs()
        self.clip_result()
        self.clip_recap()
        self.clip_next()
        self.end_card()

    # ── c1.comp.1: write a and b, multiply out, the 3x3 grid, the table ─────────
    def build_grid(self):
        old = [[M(f"a_{r + 1}b_{c + 1}", rf"\,(\mathbf {U[r]}\times\mathbf {U[c]})", size=CS)
                for c in range(3)] for r in range(3)]
        rh = [M(rf"a_{r + 1}\mathbf {U[r]}", size=CS) for r in range(3)]
        ch = [M(rf"b_{c + 1}\mathbf {U[c]}", size=CS) for c in range(3)]
        corner = M(r"\times", size=CS, color=DIM)
        cw = max(m.width for row in old for m in row)
        hw = max(m.width for m in rh)
        px, py = cw + 0.4, 1.1
        x0 = hw / 2 + 0.55 + cw / 2
        for k in range(3):
            rh[k].move_to([0, -(k + 1) * py, 0])
            ch[k].move_to([x0 + k * px, 0, 0])
            for c in range(3):
                old[k][c].move_to([x0 + c * px, -(k + 1) * py, 0])
        vx = hw / 2 + 0.3
        self.vline = Line([vx, 0.5, 0], [vx, -3 * py - 0.5, 0]).set_stroke(DIM, 2)
        self.hline = Line([-hw / 2 - 0.2, -py / 2, 0], [x0 + 2 * px + cw / 2 + 0.2, -py / 2, 0]).set_stroke(DIM, 2)
        self.old, self.rh, self.ch, self.corner = old, rh, ch, corner
        self.G = VGroup(corner, *rh, *ch, self.vline, self.hline, *[old[r][c] for r in range(3) for c in range(3)])
        self.G.move_to(UP * 0.3)

    def clip_expand(self):
        with self.say("c1.comp.1") as c:
            eqA = M(r"\mathbf a", "=", r"a_1\mathbf i", "+", r"a_2\mathbf j", "+", r"a_3\mathbf k", size=56)
            eqB = M(r"\mathbf b", "=", r"b_1\mathbf i", "+", r"b_2\mathbf j", "+", r"b_3\mathbf k", size=56)
            VGroup(eqA, eqB).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to(UP * 0.3)
            c.wait_until("Write ay as")
            self.play(Write(eqA), run_time=min(3.0, 0.75 * c.until("b")))
            c.wait_until("b")
            self.play(Write(eqB), run_time=min(1.4, 0.6 * c.until("expand")))

            # {expand}: both brackets into one product, order kept
            c.wait_until("expand")
            prod = M(r"\mathbf a\times\mathbf b", "=", "(", r"a_1\mathbf i", "+", r"a_2\mathbf j", "+",
                     r"a_3\mathbf k", ")", r"\times", "(", r"b_1\mathbf i", "+", r"b_2\mathbf j", "+",
                     r"b_3\mathbf k", ")", size=48)
            prod.scale_to_fit_width(min(prod.width, 12.6)).move_to(UP * 0.3)
            anims = []
            for k in range(5):
                anims += [ReplacementTransform(eqA[2 + k], prod[3 + k]),
                          ReplacementTransform(eqB[2 + k], prod[11 + k])]
            dup = [prod[0].copy(), prod[1].copy()]
            anims += [ReplacementTransform(eqA[0], prod[0]), ReplacementTransform(eqA[1], prod[1]),
                      ReplacementTransform(eqB[0], dup[0]), ReplacementTransform(eqB[1], dup[1])]
            anims += [FadeIn(prod[i]) for i in (2, 8, 9, 10, 16)]
            self.play(*anims, run_time=min(2.0, 0.7 * c.until("grid")))
            self.remove(*dup)
            settle(self, prod)
            self.prod = prod

            # {grid}: a's terms down the left, b's across the top, then the nine products
            c.wait_until("grid")
            self.build_grid()
            prod.generate_target()
            prod.target.scale(0.82).move_to(UP * 3.25)
            anims = [MoveToTarget(prod)]
            anims += [TransformFromCopy(prod[3 + 2 * k], self.rh[k]) for k in range(3)]
            anims += [TransformFromCopy(prod[11 + 2 * k], self.ch[k]) for k in range(3)]
            anims += [Create(self.vline), Create(self.hline), FadeIn(self.corner)]
            self.play(*anims, run_time=1.7)
            c.wait_until("giving nine products")
            cells = [self.old[r][k] for r in range(3) for k in range(3)]
            lag = 0.14
            self.play(*[time_span(FadeIn(m, shift=0.15 * DOWN), lag * k, lag * k + 0.8)
                        for k, m in enumerate(cells)], run_time=lag * 8 + 0.8)
            settle(self, self.G)

            # {table}: each is numbers times a unit cross product; the table slides in
            c.wait_until("table")
            self.play(*[time_span(FlashAround(m[1], time_width=1.5, stroke_width=3), 0.07 * k, 0.07 * k + 1.2)
                        for k, m in enumerate(cells)], run_time=0.07 * 8 + 1.2)
            c.wait_until("we already have the table")
            T_ = ijk_table()
            G = self.G
            gap = 0.7
            tw = T_.width * TAB_SCALE
            s = min(1.0, (13.1 - gap - tw) / G.width)
            total = s * G.width + gap + tw
            gy = G.get_y()
            gx, tx = -total / 2 + s * G.width / 2, -total / 2 + s * G.width + gap + tw / 2
            T_.scale(TAB_PARK_SCALE).to_edge(RIGHT, buff=0.5).to_edge(UP, buff=0.5)   # s5's parked pose
            # grid and product make room on the left while the table reappears where s5 parked it
            rt = min(1.0, max(0.6, 0.45 * (c.remaining - 0.2)))
            self.play(G.animate.scale(s).move_to([gx, gy, 0]),
                      self.prod.animate.to_edge(LEFT, buff=0.5), FadeIn(T_), run_time=rt)
            T_.generate_target()
            T_.target.scale(TAB_SCALE / TAB_PARK_SCALE).move_to([tx, gy, 0])
            self.play(MoveToTarget(T_), run_time=min(1.2, max(0.6, c.remaining - 0.2)))
            self.gs, self.T = s, T_

    # ── c1.comp.2: diagonal vanishes, six pair up, the components ───────────────
    def substitute(self, r, cc, t0=0.0, dur=None):
        old = self.old[r][cc]
        ent = self.T.ents[r][cc]
        s = TABLE[r][cc]
        neg = s.startswith("-")
        coef, unit = f"a_{r + 1}b_{cc + 1}", rf"\,\mathbf {s[-1]}"
        new = (M("-", coef, unit, size=CS) if neg else M(coef, unit, size=CS)).scale(self.gs)
        if neg:
            new[0].set_color(RED)          # the table's red minus carries over
        ci, ui = (1, 2) if neg else (0, 1)
        new.move_to(old)
        new.shift(UP * (old[0].get_y() - new[ci].get_y()))
        self.new[(r, cc)] = new
        anims = [ReplacementTransform(old[0], new[ci]), FadeOut(old[1], scale=0.6),
                 TransformFromCopy(ent.unit, new[ui])]
        if neg:
            anims.append(TransformFromCopy(ent.sign, new[0]))
        if dur:
            anims = [time_span(a, t0, t0 + dur) for a in anims]
        return anims

    def merge(self, key, t0=0.0, dur=None):
        """The pair `key` flies into its component slot of `full`; returns (anims, extras)."""
        full, b = self.full, SLOT[key]
        (pr, pc), (nr, nc) = PAIRS[key]
        P, N = self.new[(pr, pc)], self.new[(nr, nc)]
        extra = full[b + 5].copy()
        anims = [TransformFromCopy(P[1], full[b + 5]), TransformFromCopy(N[2], extra),
                 FadeIn(full[b]), FadeIn(full[b + 4]), TransformFromCopy(P[0], full[b + 1]),
                 TransformFromCopy(N[0], full[b + 2]), TransformFromCopy(N[1], full[b + 3])]
        if dur:
            anims = [time_span(a, t0, t0 + dur) for a in anims]
        return anims, [extra]

    def clip_pairs(self):
        old, T_, G, gs = self.old, self.T, self.G, self.gs
        self.new = {}
        full = M(r"\mathbf a\times\mathbf b", "=",
                 "(", "a_2b_3", "-", "a_3b_2", ")", r"\,\mathbf i", "+",
                 "(", "a_3b_1", "-", "a_1b_3", ")", r"\,\mathbf j", "+",
                 "(", "a_1b_2", "-", "a_2b_1", ")", r"\,\mathbf k", size=CS)
        full.scale_to_fit_width(min(full.width, 12.8)).move_to(DOWN * 2.8)
        self.full = full
        with self.say("c1.comp.2") as c:
            # {diag}: a unit arrow crossed with itself: the table's zeros fly in
            diag = [old[i][i] for i in range(3)]
            self.play(*[FlashAround(d, time_width=1.5) for d in diag], run_time=1.4)
            c.wait_until("so they vanish")
            zeros = [strut(r"\mathbf 0", size=CS, color=DIM).scale(gs).move_to(d) for d in diag]
            anims = []
            for i, d in enumerate(diag):
                anims += [FadeOut(d, scale=0.6), TransformFromCopy(T_.ents[i][i].unit, zeros[i][1])]
            self.play(*anims, run_time=1.4)
            settle(self, G, add=zeros, drop=diag)

            # {pair}: mirror cells pair up (one colour per pair)
            c.wait_until("pair")
            bw = max(old[r][k].width for r, k in OFF) + 0.24
            bh = max(old[r][k].height for r, k in OFF) + 0.24
            boxes, anims = {}, []
            for p, key in enumerate("kij"):
                for rc in PAIRS[key]:
                    box = RoundedRectangle(corner_radius=0.1, width=bw, height=bh).set_stroke(PAIR_COL[key], 3)
                    box.move_to(old[rc[0]][rc[1]])
                    boxes[rc] = box
                    anims.append(time_span(Create(box), 0.45 * p, 0.45 * p + 1.0))
            self.play(*anims, run_time=1.9)
            self.boxes = boxes

            # {k}: spotlight the k pair; i x j = k from the table
            c.wait_until("k")
            ij = [(1, 2), (2, 1), (2, 0), (0, 2)]
            self.play(*set_alpha([old[r][k] for r, k in ij] + [boxes[rc] for rc in ij], DIMMED), run_time=1.0)
            c.wait_until("with eye cross jay")
            self.play(FlashAround(old[0][1][1], time_width=1.5), FlashAround(T_.ents[0][1], time_width=1.5),
                      run_time=1.4)
            c.wait_until("gives plus kay")
            self.play(*self.substitute(0, 1), run_time=1.5)

            # {kminus}: j x i = -k
            c.wait_until("with jay cross eye")
            self.play(FlashAround(old[1][0][1], time_width=1.5), FlashAround(T_.ents[1][0], time_width=1.5),
                      run_time=1.4)
            c.wait_until("gives minus kay")
            self.play(*self.substitute(1, 0), run_time=1.5)

            # {kcomp}: the pair merges into the k component
            c.wait_until("kcomp")
            P, N = self.new[(0, 1)], self.new[(1, 0)]
            b = SLOT["k"]
            extra = full[b + 5].copy()
            self.play(TransformFromCopy(P[1], full[b + 5]), TransformFromCopy(N[2], extra),
                      FadeIn(full[b]), FadeIn(full[b + 4]), TransformFromCopy(P[0], full[b + 1]),
                      run_time=1.6)
            self.remove(extra)
            c.wait_until("minus ay two")
            self.play(TransformFromCopy(N[0], full[b + 2]), TransformFromCopy(N[1], full[b + 3]), run_time=1.4)

            # {others}: the other two pairs, the same way, faster
            c.wait_until("others")
            anims = set_alpha([boxes[rc] for rc in ij], 1)
            for k, (r, cc) in enumerate(ij):
                anims += self.substitute(r, cc, t0=0.15 * k, dur=1.0)
            self.play(*anims, run_time=0.15 * 3 + 1.0)
            a_i, x_i = self.merge("i", 0.0, 1.3)
            a_j, x_j = self.merge("j", 0.3, 1.3)
            self.play(*a_i, *a_j, time_span(FadeIn(full[8]), 0.6, 1.6), time_span(FadeIn(full[15]), 0.6, 1.6),
                      run_time=1.6)
            self.remove(*x_i, *x_j)
            full[0].set_opacity(0)
            full[1].set_opacity(0)
            settle(self, full)
            settle(self, G, add=list(self.new.values()), drop=[old[r][k] for r, k in OFF])

    # ── c1.comp.3: the formula, the cyclic pattern, two checks ──────────────────
    def clip_result(self):
        full = self.full
        with self.say("c1.comp.3") as c:
            # {result}: prefix appears, the line takes the centre; the hook's tuple returns
            full.generate_target()
            full.target[0].set_opacity(1)
            full.target[1].set_opacity(1)
            full.target.scale_to_fit_width(min(12.6, full.width * 1.05)).move_to(UP * 2.0)
            tup = hook_tuple().move_to(UP * 0.5)
            sweep_clear(self, MoveToTarget(full), time_span(FadeIn(tup, shift=0.25 * UP), 0.9, 1.9),
                        keep=[full], run_time=1.9)
            c.wait_until("now derived")
            comps = [full[2:8], full[9:15], full[16:22]]
            ents = [tup[5:10], tup[11:16], tup[17:22]]
            ticks = [check_mark(GREEN).scale(0.8).next_to(e, DOWN, buff=0.3) for e in ents]
            anims = []
            for k in range(3):
                t0 = 0.25 * k
                anims += [time_span(FlashAround(comps[k], color=GREEN, time_width=1.5), t0, t0 + 1.0),
                          time_span(FlashAround(ents[k], color=GREEN, time_width=1.5), t0, t0 + 1.0),
                          time_span(Create(ticks[k]), t0 + 0.2, t0 + 0.9)]
            self.play(*anims, run_time=1.5)

            # {pattern}: the wheel 1 -> 2 -> 3; index pairs (2,3), (3,1), (1,2) light in turn
            c.wait_until("pattern")
            wheel, nodes, arcs = make_wheel()
            wheel.move_to(DOWN * 2.0)
            self.play(FadeIn(wheel, shift=0.2 * UP), run_time=1.0)
            box = hl_box(full[3])
            dt = max(0.5, min(0.8, (c.until("six") - 0.1) / 3))
            prev = None
            for (p, q), term in (((2, 3), full[3]), ((3, 1), full[10]), ((1, 2), full[17])):
                anims = [arcs[(p, q)].animate.set_color(YELLOW), nodes[p].animate.set_color(YELLOW),
                         nodes[q].animate.set_color(YELLOW)]
                if prev is None:
                    anims.append(FadeIn(box))
                else:
                    anims += [Transform(box, hl_box(term)), arcs[prev].animate.set_color(DIM)]
                    anims += [nodes[n].animate.set_color(FG) for n in prev if n not in (p, q)]
                self.play(*anims, run_time=dt)
                prev = (p, q)

            # {six}: the formula moves up; (3,0,0) x (1,2,0) = (0,0,6), with s4's picture
            c.wait_until("six")
            full.generate_target()
            full.target.scale_to_fit_width(min(full.width, 10.6)).move_to(UP * 3.25)
            self.play(MoveToTarget(full), FadeOut(tup), *[FadeOut(t) for t in ticks], FadeOut(box), run_time=1.2)
            c.wait_until("Three, zero, zero")
            ex1 = M("(3,0,0)", r"\times", "(1,2,0)", "=", "(0,0,6)", size=48)
            ex1[0].set_color(A_COL)
            ex1[2].set_color(B_COL)
            ex1[4].set_color(CROSS_COL)
            ex1.move_to(UP * 1.5).to_edge(LEFT, buff=0.9)
            self.play(time_span(Write(ex1[0]), 0, 0.8), time_span(FadeIn(ex1[1]), 0.5, 1.0),
                      time_span(Write(ex1[2]), 0.8, 1.6), FadeOut(wheel), run_time=1.6)
            c.wait_until("gives zero, zero, six")
            self.play(FadeIn(ex1[3]), FadeIn(ex1[4], shift=0.3 * LEFT), run_time=1.0)
            settle(self, ex1)
            c.wait_until("just as the picture said")
            inset = s4_inset().move_to([3.95, -0.1, 0])
            self.play(FadeIn(inset, shift=0.3 * LEFT), run_time=1.2)

            # {test}: (1,2,3) x (4,5,6) = (-3,6,-3)
            c.wait_until("test")
            ex2 = M("(1,2,3)", r"\times", "(4,5,6)", "=", "(-3,6,-3)", size=48)
            ex2[0].set_color(A_COL)
            ex2[2].set_color(B_COL)
            ex2[4].set_color(CROSS_COL)
            ex2.next_to(ex1, DOWN, buff=0.75, aligned_edge=LEFT)
            self.play(time_span(Write(ex2[0]), 0, 0.8), time_span(FadeIn(ex2[1]), 0.5, 1.0),
                      time_span(Write(ex2[2]), 0.8, 1.6), run_time=1.6)
            c.wait_until("gives minus three")
            self.play(FadeIn(ex2[3]), FadeIn(ex2[4], shift=0.3 * LEFT), run_time=1.0)
            settle(self, ex2)

            # {perp}: both dot products vanish
            c.wait_until("perp")
            d1 = M("(-3,6,-3)", r"\cdot", "(1,2,3)", "=", "0", size=44)
            d2 = M("(-3,6,-3)", r"\cdot", "(4,5,6)", "=", "0", size=44)
            for d, col in ((d1, A_COL), (d2, B_COL)):
                d[0].set_color(CROSS_COL)
                d[2].set_color(col)
                d[4].set_color(GREEN)
            d1.next_to(ex2, DOWN, buff=0.8, aligned_edge=LEFT)
            d2.next_to(d1, DOWN, buff=0.45, aligned_edge=LEFT)
            anims = []
            for k, (d, src) in enumerate(((d1, ex2[0]), (d2, ex2[2]))):
                t0 = 0.5 * k
                anims += [time_span(TransformFromCopy(ex2[4], d[0]), t0, t0 + 1.3),
                          time_span(FadeIn(d[1]), t0 + 0.4, t0 + 1.0),
                          time_span(TransformFromCopy(src, d[2]), t0, t0 + 1.3),
                          time_span(FadeIn(d[3]), t0 + 1.1, t0 + 1.6),
                          time_span(FadeIn(d[4], shift=0.2 * LEFT), t0 + 1.1, t0 + 1.6)]
            self.play(*anims, run_time=2.1)
            c.wait_until("is zero")
            self.play(FlashAround(d1[4], color=GREEN, time_width=1.5),
                      FlashAround(d2[4], color=GREEN, time_width=1.5), run_time=1.2)
            settle(self, d1)
            settle(self, d2)

    # ── c1.comp.4: recap ───────────────────────────────────────────────────────
    def clip_recap(self):
        R, title, lines = build_recap()
        R.to_edge(LEFT, buff=0.55)
        self.recap_home = R.get_center().copy()
        R.move_to([0, R.get_y(), 0])
        with self.say("c1.comp.4") as c:
            sweep_clear(self, time_span(FadeIn(title, shift=0.3 * DOWN), 0.7, 1.5), run_time=1.5)
            for k, cue in enumerate(("r1", "r2", "r3", "r4", "r5", "r6")):
                c.wait_until(cue)
                icon, text = lines[k]
                self.play(FadeIn(icon, scale=0.5), FadeIn(text, shift=0.25 * LEFT),
                          run_time=min(1.0, max(0.5, c.until() - 0.1)))
            settle(self, R)
        self.R = R

    # ── c1.comp.5: a third vector, the box, the determinant ────────────────────
    def clip_next(self):
        B = BoxPic()
        self.B = B
        trip = M(r"\mathbf a\cdot(\mathbf b\times\mathbf c)", size=56)
        vol = T("= volume (up to sign)", 36)
        det = M(r"=\det\begin{pmatrix}a_1&a_2&a_3\\b_1&b_2&b_3\\c_1&c_2&c_3\end{pmatrix}", size=44)
        trip.move_to([0, 1.75, 0]).align_to(np.array([0.7, 0, 0]), LEFT)
        vol.next_to(trip, DOWN, buff=0.5).align_to(trip, LEFT).shift(0.45 * RIGHT)
        det.next_to(vol, DOWN, buff=0.5).align_to(vol, LEFT)
        self.trip, self.vol, self.det = trip, vol, det
        with self.say("c1.comp.5") as c:
            # {next} the recap holds; {triple}: a and b again, in 3D, then c
            c.wait_until("triple")
            sweep_clear(self, time_span(FadeIn(B.dot), 0.5, 1.0), time_span(GrowArrow(B.va), 0.5, 1.5),
                        time_span(GrowArrow(B.vb), 0.7, 1.7), time_span(FadeIn(B.la), 1.0, 1.8),
                        time_span(FadeIn(B.lb), 1.0, 1.8), run_time=1.8)
            c.wait_until("vector see")
            self.play(GrowArrow(B.vc), FadeIn(B.lc, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("and dot ay")
            self.play(Write(trip), time_span(FadeIn(B.base), 0.6, 1.6), time_span(GrowArrow(B.bxc), 0.8, 2.0),
                      time_span(FadeIn(B.lbxc), 1.4, 2.0), run_time=2.0)
            # {box}: the slanted box; = volume (up to sign)
            c.wait_until("box")
            self.play(*[FadeIn(f) for f in B.faces], run_time=1.5)
            c.wait_until("the three of them span")
            self.play(FadeIn(vol, shift=0.2 * DOWN), run_time=1.0)
            # {det}: = det(...)
            c.wait_until("det")
            self.play(FadeIn(det, shift=0.2 * DOWN), run_time=1.6)
            settle(self, B.pic)

    # ── end card: the finished recap + Next ────────────────────────────────────
    def end_card(self):
        B, R, trip, vol, det = self.B, self.R, self.trip, self.vol, self.det
        R.move_to(self.recap_home)
        rx = (R.get_right()[0] + 6.6) / 2
        head = T("Next: the triple product", 32, color=YELLOW).move_to([rx, R[0].get_y(), 0])
        B.pic.generate_target()
        B.pic.target.scale(0.5).next_to(head, DOWN, buff=0.45)
        right = VGroup(trip.copy(), vol.copy(), det.copy()).scale(0.8)
        right.next_to(B.pic.target, DOWN, buff=0.4).set_x(rx)
        for m, t in zip((trip, vol, det), right):
            m.generate_target()
            m.target.become(t)
        self.play(*[FadeOut(lbl) for lbl in B.labels], MoveToTarget(B.pic),
                  *[MoveToTarget(m) for m in (trip, vol, det)], run_time=1.5)
        self.play(FadeIn(R, lag_ratio=0.05), FadeIn(head, shift=0.3 * DOWN), run_time=1.2)
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
