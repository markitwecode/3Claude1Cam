"""Chapter 5, scene 3: a lookup table. Mux tied to constants, ROM, the 4-input LUT, D1 stored in it.
Clips c5.lut.1 – c5.lut.5.

Shared (s1, s5, s8 import these):
- `LUT_CELL` 0.8, `COUNT` ("00", "01", "10", "11"), `D1_BITS` "0000000111011101" (rows s1 s0 in
  counting order, columns e r in counting order, row-major), `GENERIC_BITS`.
- `bit_tex(ch, size=48)`: MathTex bit, "1" GREEN, "0"/"X" DIM.
- `lut_grid(bits=None, center=ORIGIN, cell=LUT_CELL, size=48, head_size=40, colored=False, axes=False)`:
  the 4 x 4 grid (BLUE lines), row headings left / column headings above (counting order;
  colored: rows GREEN, columns BLUE), axes: kmap-style corner (diagonal, `e r` BLUE, `s1 s0` GREEN).
  `.grid .row_heads .col_heads .corner .vals[r][k] (None if blank) .pos(r, k) .sq(r, k) .L .R .top .bot`.
- `lut_table(bits=None, center=ORIGIN, names=False, axes=False, out_label=False, colored=None)`:
  the hero: grid + box + "lookup table" label + 4 input wires (left) + output wire (right, low).
  `.lut (the grid) .box .label .wires .out_wire .names .out .in_bit_pos(i) .out_bit_pos()`.
- `address_bits(t, bits="0111", color=YELLOW)`: VGroup of the bits above t's input wires.
- `recap_shot(center=ORIGIN)`: D1's table, names, D1, address 0111 lit YELLOW (row 01, column 11,
  the cell and its 1).
"""
# style: 2
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


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# Shared: the lookup table
# =============================================================================================
LUT_CELL = 0.8
COUNT = ("00", "01", "10", "11")
D1_BITS = "0000" "0001" "1101" "1101"
GENERIC_BITS = "1001" "0111" "0110" "0010"
CODES = {"Hunt": "00", "Sight": "01", "Sync": "10"}


def bit_tex(ch, size=48):
    return MathTex(ch, font_size=size, color=GREEN if ch == "1" else DIM)


def lut_grid(bits=None, center=ORIGIN, cell=LUT_CELL, size=48, head_size=40, colored=False, axes=False):
    c = np.array(center, dtype=float)
    W = 4 * cell
    L, R, top, bot = c[0] - W / 2, c[0] + W / 2, c[1] + W / 2, c[1] - W / 2
    grid = VGroup(Square(side_length=W).move_to(c),
                  *[Line(_p(L + k * cell, top), _p(L + k * cell, bot)) for k in (1, 2, 3)],
                  *[Line(_p(L, top - k * cell), _p(R, top - k * cell)) for k in (1, 2, 3)]).set_stroke(BLUE, 3)
    col_heads = VGroup(*[MathTex(h, font_size=head_size, color=BLUE if colored else FG)
                         .move_to(_p(L + (k + 0.5) * cell, top + 0.32)) for k, h in enumerate(COUNT)])
    row_heads = VGroup(*[MathTex(h, font_size=head_size, color=GREEN if colored else FG)
                         .move_to(_p(L - 0.45, top - (r + 0.5) * cell)) for r, h in enumerate(COUNT)])

    def pos(r, k):
        return _p(L + (k + 0.5) * cell, top - (r + 0.5) * cell)

    def sq(r, k):
        return Square(side_length=cell).move_to(pos(r, k))

    g = VGroup(grid, col_heads, row_heads)
    corner = VGroup()
    if axes:
        diag = Line(_p(L, top), _p(L - 0.75, top + 0.75)).set_stroke(FG, 2)
        er = VGroup(MathTex("e", font_size=36, color=BLUE), MathTex("r", font_size=36, color=BLUE)).arrange(RIGHT, buff=0.1)
        er.move_to(_p(L - 0.45, top + 0.8), aligned_edge=LEFT)
        ss = VGroup(MathTex("s_1", font_size=36, color=GREEN), MathTex("s_0", font_size=36, color=GREEN)).arrange(RIGHT, buff=0.08)
        ss.move_to(_p(L - 0.98, top + 0.24))
        corner = VGroup(diag, er, ss)
        g.add(corner)
    vals = [[None] * 4 for _ in range(4)]
    vg = VGroup()
    if bits:
        for i, ch in enumerate(bits):
            if ch.strip():
                r, k = divmod(i, 4)
                v = bit_tex(ch, size).move_to(pos(r, k))
                vals[r][k] = v
                vg.add(v)
    g.add(vg)
    g.grid, g.col_heads, g.row_heads, g.corner, g.vals, g.values = grid, col_heads, row_heads, corner, vals, vg
    g.pos, g.sq, g.cell = pos, sq, cell
    g.L, g.R, g.top, g.bot, g.cx, g.cy = L, R, top, bot, c[0], c[1]
    return g


def lut_table(bits=None, center=ORIGIN, names=False, axes=False, out_label=False, colored=None):
    colored = (names or axes) if colored is None else colored
    lut = lut_grid(bits, center, colored=colored, axes=axes)
    L, R, top, bot, cy = lut.L, lut.R, lut.top, lut.bot, lut.cy
    bl, br, bt, bb = L - 1.45, R + 0.35, top + 1.15, bot - 0.35
    box = Rectangle(width=br - bl, height=bt - bb).move_to(_p((bl + br) / 2, (bt + bb) / 2)).set_stroke(FG, 3)
    label = T("lookup table", 36).move_to(_p((bl + br) / 2, bt + 0.38))
    in_y = [cy + 0.9, cy + 0.3, cy - 0.3, cy - 0.9]
    wires = VGroup(*[Line(_p(bl - 1.2, y), _p(bl, y)).set_stroke(FG, 3) for y in in_y])
    out_y = bot + 0.3
    out_wire = Line(_p(br, out_y), _p(br + 1.2, out_y)).set_stroke(FG, 3)
    g = VGroup(lut, box, label, wires, out_wire)
    nm = VGroup()
    if names:
        for (tex, col), y in zip((("s_1", GREEN), ("s_0", GREEN), ("e", BLUE), ("r", BLUE)), in_y):
            nm.add(MathTex(tex, font_size=40, color=col).move_to(_p(bl - 1.5, y)))
        g.add(nm)
    out = MathTex("D_1", font_size=40, color=BLUE).move_to(_p(br + 1.58, out_y))
    if out_label:
        g.add(out)
    g.lut, g.box, g.label, g.wires, g.out_wire, g.names, g.out = lut, box, label, wires, out_wire, nm, out
    g.in_y, g.out_y, g.bl, g.br = in_y, out_y, bl, br
    g.in_bit_pos = lambda i: _p(bl - 0.6, in_y[i] + 0.25)
    g.out_bit_pos = lambda: _p(br + 0.6, out_y + 0.25)
    return g


def address_bits(t, bits="0111", color=YELLOW):
    return VGroup(*[MathTex(b, font_size=36, color=color).move_to(t.in_bit_pos(i)) for i, b in enumerate(bits)])


def hit_box(lut, r, k):
    return Square(side_length=lut.cell - 0.1).move_to(lut.pos(r, k)).set_stroke(YELLOW, 3).set_fill(YELLOW, 0.3)


def recap_shot(center=ORIGIN):
    t = lut_table(D1_BITS, center, names=True, axes=True, out_label=True)
    lut = t.lut
    hb = hit_box(lut, 1, 3)
    lut.vals[1][3].set_color(YELLOW)
    lut.row_heads[1].set_color(YELLOW)
    lut.col_heads[3].set_color(YELLOW)
    return VGroup(hb, t, address_bits(t))


# =============================================================================================
# Local: the multiplexer and the ROM
# =============================================================================================
MUX_BITS = "10100011"


def mux_drawing(cx=-2.5, cy=0.5):
    W, H = 2.4, 5.0
    L, R, top, bot = cx - W / 2, cx + W / 2, cy + H / 2, cy - H / 2
    box = Rectangle(width=W, height=H).move_to(_p(cx, cy)).set_stroke(BLUE, 4)
    iy = [top - 0.4 - 0.55 * k for k in range(8)]
    ilab = VGroup(*[MathTex(f"I_{k}", font_size=34).move_to(_p(L + 0.4, y)) for k, y in enumerate(iy)])
    iw = VGroup(*[Line(_p(L - 1.0, y), _p(L, y)).set_stroke(FG, 3) for y in iy])
    sx = [L + 0.6, cx, R - 0.6]
    slab = VGroup(*[MathTex(f"S_{2 - k}", font_size=34).move_to(_p(x, bot + 0.32)) for k, x in enumerate(sx)])
    sw = VGroup(*[Line(_p(x, bot), _p(x, bot - 0.6)).set_stroke(BLUE, 3) for x in sx])
    F = MathTex("F", font_size=34).move_to(_p(R - 0.3, cy))
    ow = Line(_p(R, cy), _p(R + 1.0, cy)).set_stroke(GREEN, 3)
    f = MathTex("f", font_size=44, color=GREEN).move_to(_p(R + 1.3, cy))
    g = VGroup(box, ilab, iw, slab, sw, F, ow, f)
    g.box, g.ilab, g.iw, g.slab, g.sw, g.F, g.ow, g.f = box, ilab, iw, slab, sw, F, ow, f
    g.iy, g.sx, g.L, g.R, g.top, g.bot, g.cy = iy, sx, L, R, top, bot, cy
    g.bits = VGroup(*[bit_tex(b, 40).move_to(_p(L - 1.3, y)) for b, y in zip(MUX_BITS, iy)])
    g.names = VGroup(*[MathTex(n, font_size=40, color=BLUE).move_to(_p(x, bot - 0.92)) for n, x in zip("xyz", sx)])
    g.vals = VGroup(*[MathTex(v, font_size=34, color=YELLOW).move_to(_p(x + 0.26, bot - 0.3)) for v, x in zip("110", sx)])

    def switch(k):
        return Arrow(_p(L + 0.75, iy[k]), _p(R - 0.6, cy), buff=0, stroke_width=4, color=YELLOW,
                     max_tip_length_to_length_ratio=0.12)

    def path(k):
        return VMobject().set_points_as_corners([_p(L - 1.05, iy[k]), _p(L, iy[k]), _p(L + 0.75, iy[k]),
                                                 _p(R - 0.6, cy), _p(R + 1.0, cy)]).set_stroke(YELLOW, 7)
    g.switch, g.path = switch, path
    g.out_bit = MathTex("1", font_size=40, color=GREEN).move_to(_p(R + 0.5, cy + 0.3))
    return g


def rom_drawing(cx=0.8, cy=0.0):
    W, H = 2.4, 5.2
    L, R, top, bot = cx - W / 2, cx + W / 2, cy + H / 2, cy - H / 2
    box = Rectangle(width=W, height=H).move_to(_p(cx, cy)).set_stroke(BLUE, 4)
    label = T("ROM", 40).move_to(_p(cx, top + 0.4))
    pitch = 0.28
    slots = VGroup(*[Rectangle(width=1.5, height=pitch).move_to(_p(cx, cy + 7.5 * pitch - i * pitch))
                     .set_stroke(BLUE, 2) for i in range(16)])
    ly = [cy + 0.9, cy + 0.3, cy - 0.3, cy - 0.9]
    aw = VGroup(*[Line(_p(L - 1.4, y), _p(L, y)).set_stroke(BLUE, 3) for y in ly])
    al = VGroup(*[MathTex(f"A_{3 - i}", font_size=36, color=BLUE).move_to(_p(L - 1.75, y)) for i, y in enumerate(ly)])
    dw = VGroup(*[Line(_p(R, y), _p(R + 1.4, y)).set_stroke(GREEN, 3) for y in ly])
    dl = VGroup(*[MathTex(f"D_{3 - i}", font_size=36, color=GREEN).move_to(_p(R + 1.75, y)) for i, y in enumerate(ly)])
    g = VGroup(box, label, slots, aw, al, dw, dl)
    g.box, g.label, g.slots, g.aw, g.al, g.dw, g.dl = box, label, slots, aw, al, dw, dl
    g.addr = VGroup(*[MathTex(b, font_size=36, color=YELLOW).move_to(_p(L - 0.7, y + 0.24)) for b, y in zip("0101", ly)])
    g.word = VGroup(*[MathTex(b, font_size=36, color=YELLOW).move_to(_p(R + 0.7, y + 0.24)) for b, y in zip("0110", ly)])
    g.lit = slots[5].copy().set_stroke(YELLOW, 3).set_fill(YELLOW, 0.45)
    g.bot = bot
    return g


# =============================================================================================
# The scene
# =============================================================================================
GY = -0.3
C3 = _p(0.5, GY)      # the table's grid centre in clip 3
C4 = _p(-1.4, GY)     # and from clip 4 on
KMAP_C = _p(4.6, 0.8)
CNT = {0: 0, 1: 1, 2: 3, 3: 2}     # Gray index -> counting index


def _caption(lines):
    return VGroup(*[T(s, 32) for s in lines]).arrange(DOWN, buff=0.16).move_to(_p(4.2, 2.2))


class LookupTable(NarratedScene):
    def construct(self):
        L10D1 = _load_other("l10-state-assignment", "ch5_s6_d1")
        L10DG = _load_other("l10-state-assignment", "ch5_s3_diagram")

        # ------------------------------------------------------------------ c5.lut.1: the mux
        mux = mux_drawing()
        arrow = mux.switch(0)
        with self.say("c5.lut.1") as c:
            self.play(*appear(mux.box, VGroup(mux.ilab, mux.iw), VGroup(mux.slab, mux.sw),  # early: the multiplexer drawn whole
                              VGroup(mux.F, mux.ow, mux.f), lag=0.2, shift=None), run_time=1.6)
            self.play(GrowArrow(arrow), run_time=0.8)
            c.wait_until("Its select inputs")
            a3 = mux.switch(3)
            self.play(Transform(arrow, a3), run_time=1.2)
            self.play(VShowPassingFlash(mux.path(3), time_width=0.5), run_time=1.2)
            c.wait_until("tie")
            self.play(*appear(*mux.bits, lag=0.15, shift=None), run_time=1.6)
            c.wait_until("select")
            self.play(*appear(*mux.names, lag=0.2), *during(appear(*mux.vals, lag=0.2), 0.3, 1), run_time=1.2)
            self.play(Transform(arrow, mux.switch(6)), mux.bits[6].animate.set_color(YELLOW), run_time=1.2)
            self.play(VShowPassingFlash(mux.path(6), time_width=0.5),
                      *during(appear(mux.out_bit), 0.6, 1), run_time=1.3)
            c.wait_until("name")
            cap1 = _caption(["“The Mux is sometimes", "called a hardware", "look-up table.”"])
            self.play(*appear(cap1, shift=None), run_time=1.0)  # early: the slide's line, quoted whole

        mux_all = VGroup(mux, mux.bits, mux.names, mux.vals, mux.out_bit, arrow)
        self.remove(*mux.bits, *mux.names, *mux.vals, mux.out_bit, arrow, mux)
        self.add(mux_all)

        # ------------------------------------------------------------------ c5.lut.2: the ROM
        rom = rom_drawing()
        with self.say("c5.lut.2") as c:
            mux_all.generate_target()
            mux_all.target.scale(0.5).to_corner(UL, buff=0.45)
            self.play(*during(MoveToTarget(mux_all), 0, 0.6),
                      *during(appear(rom.box, rom.slots, rom.label, VGroup(rom.aw, rom.al), VGroup(rom.dw, rom.dl),
                                     lag=0.15, shift=None), 0.45, 1), run_time=2.0)
            c.wait_until("essentially")
            cap2 = _caption(["“Essentially is a", "look-up table”"])
            self.play(*swap(cap1, cap2), run_time=1.2)
            c.wait_until("address")
            self.play(*appear(*rom.addr, lag=0.2), run_time=1.1)
            self.play(FadeIn(rom.lit), run_time=0.7)
            self.play(*[VShowPassingFlash(w.copy().set_stroke(YELLOW, 7), time_width=0.6) for w in rom.dw],
                      *during(appear(*rom.word, lag=0.1, shift=None), 0.4, 1), run_time=1.3)
            c.wait_until("nosimp")
            tag = T("No logic simplification required", 32, GREEN).move_to(_p(0.8, rom.bot - 0.55))
            self.play(*appear(tag), run_time=1.0)

        # ------------------------------------------------------------------ c5.lut.3: the LUT
        t3 = lut_table(None, C3)
        lut = t3.lut
        rom_all = VGroup(rom, rom.lit)
        self.remove(rom.lit, rom)
        self.add(rom_all)
        with self.say("c5.lut.3") as c:
            mux_all.generate_target()
            mux_all.target.scale(0.6).to_corner(UL, buff=0.35)
            for m in mux_all.target.family_members_with_points():
                m.set_stroke(opacity=0.35 * m.get_stroke_opacity())
                m.set_fill(opacity=0.35 * m.get_fill_opacity())
            rom_all.generate_target()
            rom_all.target.scale(0.3).to_corner(UR, buff=0.35)
            for m in rom_all.target.family_members_with_points():
                m.set_stroke(opacity=0.35 * m.get_stroke_opacity())
                m.set_fill(opacity=0.35 * m.get_fill_opacity())
            self.play(*during(disappear(cap2, rom.addr, rom.word), 0, 0.4),
                      *during([MoveToTarget(mux_all), MoveToTarget(rom_all)], 0.25, 1), run_time=1.5)
            self.play(*appear(t3.box, t3.label, t3.wires, t3.out_wire, lag=0.2, shift=None), run_time=1.3)
            c.wait_until("cells")
            self.play(FadeIn(lut.grid), FadeOut(tag), run_time=0.8)
            self.play(*appear(*lut.row_heads, *lut.col_heads, lag=0.08, shift=None), run_time=1.2)  # early: headings, not words
            c.wait_until("one for each combination")
            self.play(LaggedStart(*[FlashAround(lut.sq(r, k), color=YELLOW, stroke_width=4, buff=-0.06)
                                    for r in range(4) for k in range(4)], lag_ratio=0.18), run_time=3.2)

            c.wait_until("any")
            col = VGroup(*[bit_tex(b, 30).move_to(_p(4.6, 1.45 - 0.27 * i)) for i, b in enumerate(GENERIC_BITS)])
            self.play(*appear(*col, lag=0.04, shift=None), run_time=0.8)
            gen = [bit_tex(b).move_to(lut.pos(*divmod(i, 4))) for i, b in enumerate(GENERIC_BITS)]
            moves = []
            for r in range(4):
                moves += during([Transform(col[4 * r + k], gen[4 * r + k]) for k in range(4)], 0.17 * r, 0.17 * r + 0.49)
            self.play(*moves, run_time=min(2.0, c.until("count") - 1.2))
            self.play(VShowPassingFlash(t3.out_wire.copy().set_stroke(YELLOW, 9), time_width=0.7), run_time=1.0)

            c.wait_until("count")
            count = VGroup(MathTex(r"2^{16} = 65{,}536", font_size=44, color=GOLD),
                           T("functions, 16 bits each", 36, GOLD)).arrange(RIGHT, buff=0.25)
            count.move_to(_p(0, -3.05))
            self.play(*appear(count), run_time=1.0)
            self.play(FlashAround(count, color=GOLD, time_width=1.5), run_time=1.6)

        # ------------------------------------------------------------------ c5.lut.4: D1 in it
        t4 = lut_table(None, C4, names=True, axes=True, out_label=True)
        P = t4.lut     # geometry at C4 (t3 was built at C3 and shifted)
        with self.say("c5.lut.4") as c:
            sweep_clear(self, t3.animate.shift(C4 - C3), keep=[t3], run_time=1.6)
            c.wait_until("dee one")
            self.play(*appear(t4.out), run_time=0.8)
            for i, cue in enumerate(("S one", "S zero", "ee", "ar")):
                c.wait_until(cue)
                self.play(*appear(t4.names[i]), run_time=0.6)
            c.wait_until("form the address")
            self.play(*recolor(lut.row_heads, GREEN), *recolor(lut.col_heads, BLUE),
                      *during(appear(t4.lut.corner, shift=None), 0.3, 1), run_time=1.3)

            c.wait_until("kmap")
            vals = [[v or "0" for v in row] for row in L10D1.D1_MAP]
            km = L10D1.kmap4(vals, center=KMAP_C, scale=0.7)
            km.remove(km.bars)
            for part in (km.grid, km.col_heads, km.row_heads, km.corner):
                for m in part.family_members_with_points():
                    m.set_stroke(opacity=0.55 * m.get_stroke_opacity())
                    m.set_fill(opacity=0.55 * m.get_fill_opacity())
            self.play(FadeIn(km), run_time=1.0)
            # columns 11 / 10 swap into counting order
            ch2, ch3 = km.col_heads[2].copy().move_to(km.col_heads[3]), km.col_heads[3].copy().move_to(km.col_heads[2])
            self.play(*[km.ent[r][a].animate(path_arc=1.85).move_to(km.pos(r, b))
                        for r in range(4) for a, b in ((2, 3), (3, 2))],
                      *swap(km.col_heads[2], ch2), *swap(km.col_heads[3], ch3), run_time=1.3)
            # then rows 11 / 10
            rh2, rh3 = km.row_heads[2].copy().move_to(km.row_heads[3]), km.row_heads[3].copy().move_to(km.row_heads[2])
            self.play(*[km.ent[a][k].animate(path_arc=1.85).move_to(km.pos(b, CNT[k]))
                        for k in range(4) for a, b in ((2, 3), (3, 2))],
                      *swap(km.row_heads[2], rh2), *swap(km.row_heads[3], rh3), run_time=1.3)

            c.wait_until("rows")
            tv = [[None] * 4 for _ in range(4)]
            moves = []
            for r in range(4):
                for k in range(4):
                    ch = vals[r][k]
                    v = bit_tex(ch).move_to(P.pos(CNT[r], CNT[k]))
                    if ch == "1":
                        v.set_color(FG)
                    tv[CNT[r]][CNT[k]] = v
                    moves.append(Transform(km.ent[r][k], v))
            self.play(*during(disappear(km.col_heads[0], km.col_heads[1], ch2, ch3, km.row_heads[0], km.row_heads[1],
                                        rh2, rh3, km.corner), 0, 0.3),
                      *during(moves, 0.25, 1), *during(FadeOut(km.grid), 0.4, 1), run_time=1.8)
            self.remove(*km.get_family(), ch2, ch3, rh2, rh3)
            self.add(*[v for row in tv for v in row])

            def row_box(r):
                return Rectangle(width=4 * P.cell + 0.12, height=P.cell - 0.1).move_to(
                    _p(P.cx, P.pos(r, 0)[1])).set_stroke(YELLOW, 3).set_fill(YELLOW, 0.15)

            rb = row_box(0)
            c.wait_until("all four bits")
            self.play(FadeIn(rb), run_time=0.7)
            for r, cue in ((1, "At zero one"), (2, "At one zero")):
                c.wait_until(cue)
                ones = [tv[r][k] for k in range(4) if vals_of(tv, r, k) == "1"]
                self.play(Transform(rb, row_box(r)), *during(recolor(ones, GREEN), 0.4, 1), run_time=1.2)

            c.wait_until("unused")
            self.play(Transform(rb, row_box(3)), run_time=1.0)
            eq = L10D1.term_eq("D_1", L10D1.D1_TERMS, L10D1.D1_COLORS, cx=-1.4, y=-3.0)
            self.play(*appear(eq, shift=None), run_time=1.0)
            self.play(FlashAround(eq, color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("But every location")
            new3 = [bit_tex(ch).move_to(P.pos(3, k)) for k, ch in enumerate(D1_BITS[12:])]
            sw = []
            for k in range(4):
                sw += swap(tv[3][k], new3[k])
            self.play(*sw, run_time=1.2)
            tv[3] = new3
            tag4 = VGroup(T("every location", 34), T("holds a bit", 34)).arrange(DOWN, buff=0.14).move_to(_p(4.6, -2.0))
            self.play(*appear(tag4), FadeOut(rb), run_time=1.0)  # early: the line's "hold a bit" 

        # ------------------------------------------------------------------ c5.lut.5: look one up
        dg = L10DG.sync_diagram(codes=CODES)
        dg.scale_to_fit_width(3.9).move_to(_p(4.6, 0.6))
        addr = address_bits(t4)
        with self.say("c5.lut.5") as c:
            self.play(FadeIn(dg), *set_alpha([eq], 0.4), run_time=1.2)  # early: the diagram drawn whole
            c.wait_until("Sight is")
            self.play(dg.circle["Sight"].animate.set_stroke(YELLOW, 6), run_time=0.8)
            c.wait_until("zero one")
            self.play(*appear(addr[0], addr[1], lag=0.2), lut.row_heads[1].animate.set_color(YELLOW), run_time=1.0)
            c.wait_until("both one")
            self.play(*appear(addr[2], addr[3], lag=0.2), lut.col_heads[3].animate.set_color(YELLOW), run_time=1.0)

            c.wait_until("hit")
            hb = hit_box(P, 1, 3)
            self.play(FadeIn(hb), tv[1][3].animate.set_color(YELLOW), run_time=0.8)
            p = P.pos(1, 3)
            xr = t4.br - 0.18
            path = VMobject().set_points_as_corners([p + 0.3 * RIGHT, _p(xr, p[1]), _p(xr, t4.out_y),
                                                     _p(t4.br + 1.2, t4.out_y)]).set_stroke(YELLOW, 7)
            ob = MathTex("1", font_size=36, color=YELLOW).move_to(t4.out_bit_pos())
            self.play(VShowPassingFlash(path, time_width=0.5), *during(appear(ob), 0.55, 1), run_time=1.4)

            c.wait_until("The machine moves")
            arc, al = dg.arcs[6], dg.labels[6]
            self.play(arc.animate.set_color(YELLOW), al.animate.set_color(YELLOW),
                      VShowPassingFlash(arc.copy().set_stroke(YELLOW, 8), time_width=0.6), run_time=1.2)
            self.play(dg.circle["Sight"].animate.set_stroke(FG, 4), dg.circle["Sync"].animate.set_stroke(YELLOW, 6),
                      run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)


def vals_of(tv, r, k):
    return tv[r][k].tex_string
