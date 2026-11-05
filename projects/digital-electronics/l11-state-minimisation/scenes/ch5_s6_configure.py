"""Chapter 5, scene 6: programming an FPGA: design -> synthesis -> configuration -> SRAM; other makers.
Clips c5.config.1 – c5.config.3. Ends on an empty frame.

Shared (load_scene("ch5_s6_configure")):
  pipeline_shot()  s8's recap of this scene: document "design" -> YELLOW gear box "synthesis tool" ->
                   GOLD "configuration" arrow -> FPGA package holding the SRAM strip (GREEN/DIM bits,
                   "static RAM (SRAM)"), with a GOLD "power-up" arrow curving up into the chip from
                   below. Centred near ORIGIN, ~12.4 x 4.6. Handles .doc .gear .config .chip .sram
                   .bits .powerup (arrow + label).
  doc_icon() gear_box() lut_stack() mux_column() route_icon() sram_strip() power_switch()
                   the pieces, built at ORIGIN.
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


D1 = "0000" "0001" "1101" "1101"
D0 = "0101" "1100" "0000" "1100"
SRAM_BITS = "10110010"
ROW_Y = 1.2                       # the pipeline's row
ITEM_X = -0.85                    # synthesis outputs: icon centres
ITEM_YS = (2.75, 1.2, -0.3)
BUS_X = 2.2
CHIP_C = (5.65, ROW_Y)


def fit(m, w, h):
    m.scale(min(w / m.width, h / m.height))
    return m


def strip_text(m):
    """Remove every Text / MathTex anywhere under m (thumbnails: their labels are too small to read)."""
    for sub in list(m.submobjects):
        if isinstance(sub, (Text, MathTex, SingleStringMathTex)):
            m.remove(sub)
        else:
            strip_text(sub)
    return m


def dim_all(m):
    """Every stroke and every non-background fill DIM (a thumbnail in grey)."""
    for s in m.get_family():
        if not isinstance(s, VMobject) or not s.has_points():
            continue
        if s.get_stroke_width() > 0 and s.get_stroke_opacity() > 0:
            s.set_stroke(DIM)
        if s.get_fill_opacity() > 0 and s.get_fill_color().to_hex().upper() != BG.upper():
            s.set_fill(DIM)
    return m


# ---------------------------------------------------------------- icons
def doc_icon(w=1.2, h=1.6):
    f = 0.3
    body = Polygon(_p(-w / 2, h / 2), _p(w / 2 - f, h / 2), _p(w / 2, h / 2 - f), _p(w / 2, -h / 2),
                   _p(-w / 2, -h / 2)).set_stroke(FG, 3).set_fill(BG, 1)
    fold = VMobject().set_points_as_corners([_p(w / 2 - f, h / 2), _p(w / 2 - f, h / 2 - f),
                                             _p(w / 2, h / 2 - f)]).set_stroke(FG, 2.5)
    lines = VGroup(*[Line(_p(-w / 2 + 0.2, y), _p(w / 2 - (0.45 if k == 0 else 0.2) - (0.15 * (k % 2)), y))
                     for k, y in enumerate((0.35, 0.1, -0.15, -0.4))]).set_stroke(DIM, 3)
    g = VGroup(body, fold, lines)
    g.body = body
    return g


def gear(r=0.42, teeth=8, color=YELLOW):
    pts = []
    for k in range(teeth):
        a0 = TAU * k / teeth
        d = TAU / teeth
        for frac, rad in ((0.0, r * 0.78), (0.15, r), (0.5, r), (0.65, r * 0.78)):
            a = a0 + frac * d
            pts.append(_p(rad * np.cos(a), rad * np.sin(a)))
    g = Polygon(*pts).set_stroke(color, 3)
    hole = Circle(radius=r * 0.3).set_stroke(color, 3)
    return VGroup(g, hole)


def gear_box(w=1.8, h=1.4):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(YELLOW, 3).set_fill(BG, 1)
    g = VGroup(box, gear())
    g.box = box
    return g


def lut_stack():
    grids = VGroup()
    for k in (2, 1, 0):
        s = 0.72
        sq = Square(side_length=s).set_stroke(BLUE, 2.5).set_fill(BG, 1)
        lines = VGroup(*[Line(_p(-s / 2 + i * s / 4, s / 2), _p(-s / 2 + i * s / 4, -s / 2)) for i in (1, 2, 3)],
                       *[Line(_p(-s / 2, s / 2 - i * s / 4), _p(s / 2, s / 2 - i * s / 4)) for i in (1, 2, 3)])
        lines.set_stroke(BLUE, 1.5)
        cell = VGroup(sq, lines)
        if k == 0:
            for i, b in enumerate(D1):
                if b == "1":
                    r, c = divmod(i, 4)
                    cell.add(Square(side_length=s / 4 - 0.05).set_stroke(width=0).set_fill(GREEN, 0.9)
                             .move_to(_p(-s / 2 + (c + 0.5) * s / 4, s / 2 - (r + 0.5) * s / 4)))
        grids.add(cell.shift(_p(0.12 * k, 0.12 * k)))
    return grids.move_to(ORIGIN)


def _mux(color=FG):
    return Polygon(_p(-0.17, 0.26), _p(0.17, 0.13), _p(0.17, -0.13), _p(-0.17, -0.26)).set_stroke(color, 2.5)


def mux_column():
    g = VGroup()
    for k in range(3):
        m = _mux().move_to(_p(0, (1 - k) * 0.38))
        tick = Line(m.get_bottom() + _p(0, 0.08), m.get_bottom() + _p(0, -0.06)).set_stroke(GREEN, 3)
        g.add(VGroup(m, tick))
    return g.scale(0.95).move_to(ORIGIN)


def route_icon():
    a = Square(side_length=0.26).set_stroke(TEAL, 2.5).move_to(_p(-0.4, 0.3))
    b = Square(side_length=0.26).set_stroke(TEAL, 2.5).move_to(_p(0.4, -0.3))
    path = VMobject().set_points_as_corners([_p(-0.27, 0.3), _p(0.0, 0.3), _p(0.0, -0.3), _p(0.27, -0.3)])
    path.set_stroke(GOLD, 5)
    return VGroup(path, a, b)


def gate_thumb():
    s = 0.3
    back = VMobject().set_points_as_corners([_p(0, s), _p(-s, s), _p(-s, -s), _p(0, -s)])
    arc = ArcBetweenPoints(_p(0, s), _p(0, -s), angle=-PI)
    ins = VGroup(Line(_p(-s - 0.25, 0.15), _p(-s, 0.15)), Line(_p(-s - 0.25, -0.15), _p(-s, -0.15)))
    out = Line(_p(s, 0), _p(s + 0.25, 0))
    return VGroup(back, arc, ins, out).set_stroke(FG, 2.5)


def sram_strip(cell=0.6, bits=SRAM_BITS, size=36):
    cells, vals = VGroup(), VGroup()
    n = len(bits)
    for i, b in enumerate(bits):
        sq = Square(side_length=cell).set_stroke(BLUE, 2.5).set_fill(BG, 1).move_to(_p((i - (n - 1) / 2) * cell, 0))
        cells.add(sq)
        vals.add(T(b, size, GREEN if b == "1" else DIM).move_to(sq))
    g = VGroup(cells, vals)
    g.cells, g.vals = cells, vals
    return g


def power_switch(a=_p(4.1, 0.35), b=_p(5.3, 0.35)):
    ta = Dot(a, radius=0.08, color=FG)
    tb = Dot(b, radius=0.08, color=FG)
    lever = Line(a, b).set_stroke(FG, 5)
    g = VGroup(lever, ta, tb)
    g.lever, g.a, g.b = lever, a, b
    return g


# ---------------------------------------------------------------- borrowed drawings
def _filled_clb():
    """s5's filled CLB if it exists; otherwise s4's clb(programmed=True) with D1 in G and D0 in F."""
    try:
        return load_scene("ch5_s5_oneclb").filled_clb(), True
    except Exception:  # noqa: BLE001  (s5 not built yet)
        C = load_scene("ch5_s4_clb").clb(programmed=True)
        for tbl, bits in ((C.g, D1), (C.f, D0)):
            for cell, b in zip(tbl.grid, bits):
                old = cell[1]
                old.become(T(b, 28, GREEN if b == "1" else DIM).move_to(old))
        return C, False


def pipeline_shot():
    """s8's recap: design -> synthesis tool -> configuration -> SRAM in the chip, + power-up arrow."""
    y = 0.6
    doc = doc_icon().move_to(_p(-5.4, y))
    doc_l = T("design", 32).next_to(doc, DOWN, buff=0.25)
    a1 = Arrow(_p(-4.7, y), _p(-3.75, y), buff=0, stroke_width=4).set_color(FG)
    gb = gear_box().move_to(_p(-2.8, y))
    gb_l = T("synthesis tool", 30, YELLOW).next_to(gb, DOWN, buff=0.25)
    cfg = Arrow(_p(-1.8, y), _p(0.35, y), buff=0, stroke_width=7).set_color(GOLD)
    cfg_l = T("configuration", 30, GOLD).next_to(cfg, UP, buff=0.15)
    chip = load_scene("ch4_s1_hook").package(None, w=5.6, h=2.6, n_pins=7).move_to(_p(3.25, y))
    fp = T("FPGA", 30, DIM).move_to(chip.body.get_corner(UL) + _p(1.0, -0.38))
    sram = sram_strip(cell=0.55).move_to(_p(3.25, y + 0.15))
    sram_l = T("static RAM (SRAM)", 28).next_to(sram, DOWN, buff=0.25)
    pu = CurvedArrow(_p(0.6, -2.2), chip.body.get_bottom() + _p(-1.2, -0.3), angle=PI / 3).set_color(GOLD)
    pu.set_stroke(width=5)
    pu_l = T("power-up", 30, GOLD).move_to(_p(-0.6, -2.25))
    g = VGroup(doc, doc_l, a1, gb, gb_l, cfg, cfg_l, chip, fp, sram, sram_l, pu, pu_l)
    g.doc, g.gear, g.config, g.chip, g.sram, g.bits = VGroup(doc, doc_l), VGroup(gb, gb_l), VGroup(cfg, cfg_l), \
        VGroup(chip, fp), VGroup(sram, sram_l), sram.vals
    g.powerup = VGroup(pu, pu_l)
    return g


class Configure(NarratedScene):
    def construct(self):
        self.pkg = load_scene("ch4_s1_hook").package
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ 1: design -> synthesis -> FPGA
    def clip1(self):
        with self.say("c5.config.1") as c:
            C, self.s5_clb = _filled_clb()
            C.scale(0.45 * 11.6 / C.width if C.width > 0 else 1).move_to(_p(-3.55, 0.1))
            arr = load_scene("ch5_s2_array").spartan_array(with_routes=True)
            arr.scale(0.58).move_to(_p(3.6, 0.1))
            strip_text(arr)
            if hasattr(C, "g"):     # bits as coloured cells: at this size the digits can't be read
                for tbl, bits in ((C.g, D1), (C.f, D0)):
                    for cell, b in zip(tbl.grid, bits):
                        cell[0].set_fill(GREEN if b == "1" else BG, 0.85 if b == "1" else 1)
            strip_text(C)
            self.play(*appear(C, arr, lag=0.3, shift=None), run_time=min(1.0, c.until("hdl")))
            bit = C.g.grid[7][0] if hasattr(C, "g") else C
            cursor = Polygon(_p(0, 0), _p(0, -0.55), _p(0.14, -0.42), _p(0.25, -0.65), _p(0.34, -0.6),
                             _p(0.23, -0.38), _p(0.4, -0.38)).set_fill(FG, 1).set_stroke(BG, 2)
            cursor.shift(_p(-1.6, 1.8) - cursor.get_vertices()[0]).set_z_index(5)
            self.add(cursor)
            tip = bit.get_center() + _p(0.05, -0.05)
            self.play(cursor.animate.shift(tip - cursor.get_vertices()[0]), run_time=min(0.8, c.until("hdl")))
            cross = cross_mark().scale(0.9).move_to(bit).set_z_index(6)
            self.play(*appear(cross, shift=None), run_time=min(0.6, c.until("hdl")))
            c.wait_until("hdl")

            # {hdl}
            doc = doc_icon().move_to(_p(-5.9, ROW_Y))
            doc_l = T("design", 32).next_to(doc, DOWN, buff=0.22)
            sweep_clear(self, *appear(doc, doc_l, lag=0.2), run_time=1.4)
            tag1 = T("hardware description language,\ne.g. Verilog", 30, t2c={"Verilog": BLUE})
            tag1.to_edge(LEFT, buff=0.55).set_y(-1.35)
            c.wait_until(own_word=tag1)
            self.play(*appear(tag1), run_time=1.0)
            tag2 = T("or a schematic", 30)
            gt = gate_thumb()
            VGroup(tag2, gt).arrange(RIGHT, buff=0.45).to_edge(LEFT, buff=0.55).set_y(-2.55)
            c.wait_until(own_word=tag2)
            self.play(*appear(tag2, gt, lag=0.3), run_time=1.0)

            # {synth}
            c.wait_until("synth")
            gb = gear_box().move_to(_p(-3.35, ROW_Y))
            gb_l = T("synthesis tool", 30, YELLOW).next_to(gb, DOWN, buff=0.22)
            a1 = Arrow(doc.get_right(), gb.get_left(), buff=0.12, stroke_width=4).set_color(FG)
            self.play(GrowArrow(a1), *appear(gb, gb_l, lag=0.3), run_time=1.5)
            self.play(Rotate(gb[1], angle=PI / 4), run_time=1.0)
            icons = [lut_stack(), mux_column(), route_icon()]
            texts = [("lookup table\ncontents", BLUE), ("multiplexer\nsettings", FG), ("routing", GOLD)]
            items, fans = [], []
            for ic, (txt, col), y in zip(icons, texts, ITEM_YS):
                ic.move_to(_p(ITEM_X, y))
                lab = T(txt, 28, col, line_spacing=0.8)
                lab.next_to(ic, RIGHT, buff=0.3).align_to(_p(-0.2, 0), LEFT)
                fan = Arrow(gb.get_right(), ic.get_left() + _p(-0.05, 0), buff=0.12, stroke_width=3,
                            max_tip_length_to_length_ratio=0.12).set_color(DIM)
                items.append((ic, lab))
                fans.append(fan)
            for (ic, lab), fan in zip(items, fans):
                c.wait_until(own_word=lab)
                self.play(GrowArrow(fan), *appear(ic, lab, lag=0.3), run_time=min(1.2, c.until("download")))

            # {download}
            c.wait_until("download")
            chip = self.pkg(None, w=1.8, h=1.3, n_pins=7).move_to(_p(*CHIP_C))
            fp = T("FPGA", 30).move_to(chip.body)
            stubs = []
            for ic, lab in items:
                y = ic.get_y()
                stubs.append(Line(_p(lab.get_right()[0] + 0.15, y), _p(BUS_X, y)).set_stroke(GOLD, 5))
            bus = Line(_p(BUS_X, ITEM_YS[0] + 0.025), _p(BUS_X, ITEM_YS[2] - 0.025)).set_stroke(GOLD, 5)
            stream = Arrow(_p(BUS_X - 0.03, ROW_Y), chip.body.get_left(), buff=0.08, stroke_width=7,
                           max_tip_length_to_length_ratio=0.12).set_color(GOLD)
            cfg = T("configuration", 28, GOLD).next_to(stream, UP, buff=0.12).set_x(
                (BUS_X + chip.body.get_left()[0]) / 2 + 0.05)
            self.play(*[Create(s) for s in stubs], Create(bus), *appear(cfg), run_time=1.3)
            c.wait_until("downloaded")
            self.play(GrowArrow(stream), *appear(chip, fp, shift=None, lag=0.2), run_time=1.3)
            self.play(VShowPassingFlash(stream.copy().set_stroke(YELLOW, 9), time_width=0.6),
                      FlashAround(chip.body, color=GOLD, run_time=1.2), run_time=1.2)
            self.chip, self.fp = chip, fp

            # {lab}
            c.wait_until("lab")
            row = load_scene("ch4_s6_sync").compiler_row(
                [Line(LEFT * 0.4, RIGHT * 0.4).set_stroke(FG, 3) for _ in range(3)])
            docbox = VGroup(row.box, row.eqs)
            comp = row.comp
            gal, _ = load_scene("ch5_s1_hook").gal_and_tag()
            fit(gal, 1.9, 1.3)
            ar1 = Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.3)
            ar2 = ar1.copy()
            lab_row = VGroup(docbox, ar1, comp, ar2, gal).arrange(RIGHT, buff=0.12)
            lab_row.move_to(_p(0, -2.35)).to_edge(RIGHT, buff=0.6)
            gal_l = T("GAL", 28).next_to(gal, DOWN, buff=0.15)
            lab_g = dim_all(VGroup(lab_row, gal_l))
            self.play(*appear(lab_g, shift=None), run_time=1.2)
            self.play(FlashAround(comp, color=DIM, run_time=1.2), FlashAround(gb.box, color=YELLOW, run_time=1.2),
                      run_time=1.2)

    # ------------------------------------------------------------ 2: static RAM, power, reload
    def clip2(self):
        with self.say("c5.config.2") as c:
            chip, fp = self.chip, self.fp
            big = self.pkg(None, w=5.6, h=2.8, n_pins=7).move_to(_p(0, 0.35))
            fp_t = fp.copy().move_to(big.body.get_corner(UL) + _p(1.0, -0.38)).set_color(DIM)
            sweep_clear(self, ReplacementTransform(chip, big), fp.animate.move_to(fp_t).set_color(DIM),
                        keep=[chip, fp], run_time=1.8)
            strip = sram_strip().move_to(_p(0, 0.5))
            self.play(*appear(*strip.cells, lag=0.08, shift=None), run_time=1.0)
            self.play(*appear(*strip.vals, lag=0.1, shift=None), run_time=1.0)
            sram_l = T("static RAM (SRAM)", 30).next_to(strip, DOWN, buff=0.3)
            c.wait_until(own_word=sram_l)
            self.play(*appear(sram_l), run_time=1.0)
            cap1 = T("Xilinx devices store their configuration information\n"
                     "in static RAM (SRAM) so can be easily reprogrammed", 30, line_spacing=0.85)
            cap1.move_to(_p(0, 3.2))
            self.play(*appear(cap1), run_time=min(1.0, c.until("volatile")))

            # {volatile}
            c.wait_until("volatile")
            sw = power_switch(a=big.body.get_right() + _p(1.3, 0), b=big.body.get_right() + _p(2.5, 0))
            w1 = Line(big.body.get_right(), sw.a).set_stroke(DIM, 3)
            w2 = Line(sw.b, sw.b + _p(0.8, 0)).set_stroke(DIM, 3)
            pw = T("power", 30, DIM).move_to((sw.a + sw.b) / 2 + _p(0, 0.75))
            sw.lever.set_color(GREEN)
            self.play(*appear(w1, w2, sw, pw, lag=0.15, shift=None), run_time=1.0)
            c.wait_until("power")
            self.play(Rotate(sw.lever, angle=PI / 5, about_point=sw.a), sw.lever.animate.set_color(RED),
                      run_time=0.8)
            self.play(*[v.animate.set_color(DIM).set_opacity(0.2) for v in strip.vals], run_time=1.5)
            lost = T("lost once power\nis removed", 30, RED, line_spacing=0.85)
            lost.move_to((sw.a + sw.b) / 2 + _p(0.2, -1.05))
            self.play(*appear(lost), run_time=min(1.0, c.until("powerup")))

            # {powerup}
            c.wait_until("powerup")
            self.play(Rotate(sw.lever, angle=-PI / 5, about_point=sw.a), sw.lever.animate.set_color(GREEN),
                      lost.animate.set_opacity(0.4), run_time=0.8)
            lap = load_scene("ch5_s1_hook").laptop().move_to(_p(-5.0, 1.2))
            lap_l = T("computer", 30).next_to(lap, DOWN, buff=0.2)
            ee = self.pkg("EEPROM", w=2.0, h=0.85, n_pins=4, size=28).move_to(_p(-5.0, -1.05))
            self.play(*appear(lap, lap_l, ee, lag=0.3), run_time=1.3)  # early: both sources up at power-up; their streams fire on their words
            cap2 = T("…downloaded either from a computer or from an EEPROM\n"
                     "device when the system is powered-up", 30, line_spacing=0.85)
            cap2.move_to(_p(0, -2.9))
            self.play(*appear(cap2), run_time=1.0)  # early: the slide's caption, quoted whole
            c.wait_until(own_word=lap_l)
            s1 = Arrow(lap.get_right() + _p(0.05, -0.1), big.body.get_left() + _p(0, 0.6), buff=0.1,
                       stroke_width=6, max_tip_length_to_length_ratio=0.15).set_color(GOLD)
            self.play(GrowArrow(s1), *[v.animate.set_color(GREEN if b == "1" else DIM).set_opacity(1)
                                       for v, b in zip(strip.vals, SRAM_BITS)], run_time=1.3)
            c.wait_until("memory chip")
            s2 = Arrow(ee.body.get_right(), big.body.get_left() + _p(0, -0.5), buff=0.1,
                       stroke_width=6, max_tip_length_to_length_ratio=0.15).set_color(GOLD)
            self.play(GrowArrow(s2), FlashAround(ee.body, color=GOLD), run_time=min(1.3, c.until()))

    # ------------------------------------------------------------ 3: other makers, old and modern
    def clip3(self):
        tg = load_scene("ch5_s1_hook").tile_grid
        with self.say("c5.config.3") as c:
            def frame(cx, w):
                return RoundedRectangle(corner_radius=0.15, width=w, height=3.85).set_stroke(DIM, 3) \
                    .set_fill(BG, 1).move_to(_p(cx, 0.9)).set_z_index(-1)   # always under its grid and ROM

            xf = frame(-4.6, 2.65)
            xg = tg(4, 4, pitch=0.6, tile=0.45, center=(-4.6, 1.5))
            af = frame(4.35, 3.85)
            ag = tg(4, 4, pitch=0.6, tile=0.45, center=(4.35, 0.9))
            xn = T("Xilinx", 40).move_to(_p(-4.6, 3.45))
            an = T("Altera", 40).move_to(_p(4.35, 3.45))
            sweep_clear(self, *appear(xf, xg, xn, lag=0.2, shift=None), run_time=1.6)
            c.wait_until(own_word=an)
            self.play(*appear(af, ag, an, lag=0.2, shift=None), run_time=1.0)

            def plates(f):
                ps = VGroup()
                for k in (2, 1):
                    ps.add(f.copy().set_stroke(DIM, 2).shift(_p(0.13 * k, 0.13 * k)).set_z_index(-2 + 0 * k))
                return ps

            xp, ap = plates(xf), plates(af)
            items_x = -2.6
            many = T("many product lines", 28, DIM)
            many.move_to(_p(0, 2.3)).align_to(_p(items_x, 0), LEFT)
            c.wait_until(own_word=many)
            self.play(*appear(xp, ap, shift=None, lag=0.3), *appear(many), run_time=1.2)
            # plates and frames first in draw order: later plays treat everything after their first
            # animated mobject as moving and draw it on top, so opaque plates would hide the grids
            self.bring_to_back(xp, ap, xf, af)

            def item(txt, k, col=FG):
                return T(txt, 28, col).move_to(_p(0, 2.3 - 0.72 * k)).align_to(_p(items_x, 0), LEFT)

            # {diff}
            c.wait_until("diff")
            n_clb = item("no. of CLBs", 1)
            ag6 = tg(6, 6, pitch=0.6, tile=0.45, center=(4.35, 0.9))
            self.play(*during(disappear(ag), 0, 0.45), *during(appear(ag6, shift=None), 0.5, 1),
                      *appear(n_clb), run_time=1.6)
            struct = item("structure of the CLBs", 2)
            c.wait_until("built")
            t = ag6.tile(5, 4)
            inset = Rectangle(width=1.7, height=1.4).set_stroke(YELLOW, 2.5).set_fill(BG, 1).move_to(_p(5.35, -2.45))
            co = VGroup(Line(t.get_corner(DL), inset.get_corner(UL)),
                        Line(t.get_corner(DR), inset.get_corner(UR))).set_stroke(DIM, 2)
            lutA = Square(0.4).set_stroke(BLUE, 2.5).move_to(inset.get_center() + _p(-0.45, 0.28))
            lutB = Square(0.4).set_stroke(BLUE, 2.5).move_to(inset.get_center() + _p(-0.45, -0.28))
            mx = _mux(PURPLE).move_to(inset.get_center() + _p(0.15, 0))
            ff = Rectangle(width=0.32, height=0.5).set_stroke(FG, 2.5).move_to(inset.get_center() + _p(0.6, 0))
            ws = VGroup(Line(lutA.get_right(), mx.get_left() + _p(0, 0.12)),
                        Line(lutB.get_right(), mx.get_left() + _p(0, -0.12)),
                        Line(mx.get_right(), ff.get_left())).set_stroke(DIM, 2)
            interior = VGroup(lutA, lutB, mx, ff, ws)
            self.play(t.animate.set_stroke(YELLOW), *appear(co, inset, shift=None), *appear(struct),
                      run_time=1.5)
            self.play(*appear(interior, shift=None), run_time=1.0)

            # internal / external ROM
            rom_i = item("internal or external ROM", 3, PURPLE)
            c.wait_until("read-only")
            self.play(*appear(rom_i), run_time=1.0)

            def rom(w, h, at):
                b = Rectangle(width=w, height=h).set_stroke(PURPLE, 3).set_fill(BG, 1).move_to(at)
                return VGroup(b, T("ROM", 28, PURPLE).move_to(b))

            xrom = rom(1.6, 0.65, _p(-4.6, -0.35))
            c.wait_until("inside")
            self.play(*appear(xrom, shift=None), run_time=1.0)
            arom = rom(1.1, 0.6, _p(3.2, -2.15))
            conn = Line(_p(3.2, af.get_bottom()[1]), arom[0].get_top()).set_stroke(DIM, 3)
            c.wait_until("outside")
            self.play(*appear(conn, arom, lag=0.3, shift=None), run_time=1.0)

            ar_i = item("arithmetic", 4, GOLD)
            ram_i = item("user RAM", 5, BLUE)
            c.wait_until("arithmetic")
            self.play(*[ag6.tile(r, 1).animate.set_stroke(GOLD).set_fill(GOLD, 0.55) for r in range(1, 5)],
                      *appear(ar_i), run_time=1.2)
            c.wait_until("memory for")
            self.play(*[ag6.tile(r, 3).animate.set_stroke(BLUE).set_fill(BLUE, 0.55) for r in range(1, 5)],
                      *appear(ram_i), run_time=1.2)

            # {old}
            c.wait_until("Spartan")
            sp = load_scene("ch5_s2_array").spartan_array()
            dim_all(strip_text(sp).scale(0.68).move_to(_p(-3.6, 0.35)))
            self.play(*during(disappear(*self.mobjects), 0, 0.45), *during(appear(sp, shift=None), 0.5, 1),
                      run_time=1.6)
            old_t = T("quite an old FPGA architecture", 30).move_to(_p(-3.6, -2.65))
            c.wait_until("old design")
            self.play(*appear(old_t), run_time=1.0)

            # {modern}
            c.wait_until("modern")
            mg = tg(8, 6, pitch=0.58, tile=0.44, center=(3.6, 0.35))
            mod_t = T("modern FPGA", 30).move_to(_p(3.6, -2.65))
            self.play(*appear(mg, shift=None), *appear(mod_t), run_time=1.5)
            under = [mg.tile(r, k) for r in range(2, 5) for k in range(2, 6)]
            blk_bg = Rectangle(width=3 * 0.58 + 0.44, height=2 * 0.58 + 0.44).set_stroke(width=0).set_fill(BG, 1)
            blk = Rectangle(width=blk_bg.width, height=blk_bg.height).set_stroke(PURPLE, 3).set_fill(PURPLE, 0.3)
            arm = T("Arm core", 34)
            proc = T("processor", 28, DIM)
            VGroup(arm, proc).arrange(DOWN, buff=0.12)
            block = VGroup(blk_bg, blk, arm, proc).move_to(_p(3.6, 0.35 - 0.5 * 0.58)).set_z_index(3)
            c.wait_until("processor")
            self.play(*during(disappear(*under), 0, 0.4), *during(appear(block, shift=0.6 * DOWN), 0.35, 1),
                      run_time=1.8)

            # {flex}
            c.wait_until("flex")   # {flex}: hold
