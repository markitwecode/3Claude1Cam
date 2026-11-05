"""Chapter 5, scene 1: hook: title, the synchroniser GAL, "field programmable", the grid of tiles, "?". Clips c5.hook.1 – c5.hook.2.
Opens exactly on open_card() (ch4 s7 ends on it); its part line travels into the title card.
Ends on handover_shot() (s2 opens on it and settles the grid into its 4 x 4 array).

Shared (load_scene("ch5_s1_hook")):
  tile_grid(cols=8, rows=6, pitch=1.1, tile=0.85, center=(0, 0.3), color=TEAL)
                           the FPGA: cols x rows square tiles (TEAL outline, stroke 2.5) at `pitch`,
                           DIM wires (stroke 1.5) along every channel between them, spanning the grid.
                           VGroup(wires, *tiles). .tiles (row-major, row 0 at the top) .tile(r, c)
                           .wires .pitch .side .cols .rows
  BIG = dict(pitch=1.1, tile=0.85, center=(0, 0.3)): s1's full-frame grid (8.65 x 6.35, x -4.33..4.33,
                           y -2.88..3.48). The GAL's tile and the ask tile is GAL_RC = (2, 3).
  open_card()              ch4 s7's last shot / this scene's first: a small grid (pitch 0.72, tile 0.55,
                           centre (-3, -0.3)), tile (2, 7) YELLOW and opened (DIM callout lines) to a big
                           TEAL tile (3.6 square at (3.9, -0.3)) holding D1's 16 bits in counting order
                           (T 48, rows 0000 0001 1101 1101; 1 GREEN, 0 DIM); "FPGA" and "lookup table"
                           (T 36) at y -2.95; part line (T 40) at y 3.2.
                           .grid .tiles .wires .src .zoom .tile .bits .fpga_tag .lut_tag .part
  handover_shot()          the {blank} shot: BIG grid all DIM, YELLOW "?" (T 200) at the grid centre,
                           "your circuit?" (T 40) at y -3.4. .grid .q .tag
"""
# style: 2
# handover: next
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


PART_LINE = "Part 5 · Inside an FPGA"
D1_BITS = ["0000", "0001", "1101", "1101"]
BIG = dict(pitch=1.1, tile=0.85, center=(0, 0.3))
GAL_RC = (2, 3)


# ---------------------------------------------------------------- the FPGA grid
def tile_grid(cols=8, rows=6, pitch=1.1, tile=0.85, center=(0, 0.3), color=TEAL):
    cx, cy = center
    tiles = []
    for r in range(rows):
        for c in range(cols):
            sq = Square(side_length=tile).set_stroke(color, 2.5).set_fill(BG, 0)
            sq.move_to(_p(cx + (c - (cols - 1) / 2) * pitch, cy + ((rows - 1) / 2 - r) * pitch))
            tiles.append(sq)
    half_w = (cols - 1) / 2 * pitch + tile / 2
    half_h = (rows - 1) / 2 * pitch + tile / 2
    wires = VGroup()
    for k in range(1, cols):
        x = cx + (k - cols / 2) * pitch
        wires.add(Line(_p(x, cy - half_h), _p(x, cy + half_h)).set_stroke(DIM, 2))
    for k in range(1, rows):
        y = cy + (rows / 2 - k) * pitch
        wires.add(Line(_p(cx - half_w, y), _p(cx + half_w, y)).set_stroke(DIM, 2))
    g = VGroup(wires, *tiles)
    g.tiles, g.wires, g.pitch, g.side, g.cols, g.rows = tiles, wires, pitch, tile, cols, rows
    g.tile = lambda r, c: tiles[r * cols + c]
    return g


def lut_bits(rows=D1_BITS, size=48, pitch=0.78):
    bits = VGroup()
    for r, row in enumerate(rows):
        for c, b in enumerate(row):
            bits.add(T(b, size, GREEN if b == "1" else DIM).move_to(_p((c - 1.5) * pitch, (1.5 - r) * pitch)))
    return bits


def open_card():
    grid = tile_grid(pitch=0.72, tile=0.55, center=(-3.0, -0.3))
    src = grid.tile(2, 7)
    src.set_stroke(YELLOW, 3)
    tile = Square(side_length=3.6).set_stroke(TEAL, 4).set_fill(BG, 0).move_to(_p(3.9, -0.3))
    bits = lut_bits().move_to(tile)
    zoom = VGroup(Line(src.get_corner(UR), tile.get_corner(UL)),
                  Line(src.get_corner(DR), tile.get_corner(DL))).set_stroke(DIM, 2)
    fpga_tag = T("FPGA", 36).move_to(_p(-3.0, -2.95))
    lut_tag = T("lookup table", 36).move_to(_p(3.9, -2.95))
    part = T(PART_LINE, 40).move_to(_p(0, 3.2))
    g = VGroup(grid, zoom, tile, bits, fpga_tag, lut_tag, part)
    g.grid, g.tiles, g.wires, g.src, g.zoom = grid, grid.tiles, grid.wires, src, zoom
    g.tile, g.bits, g.fpga_tag, g.lut_tag, g.part = tile, bits, fpga_tag, lut_tag, part
    return g


def handover_shot():
    grid = tile_grid(**BIG)
    for t in grid.tiles:
        t.set_stroke(DIM, 2.5)
    q = T("?", 200, YELLOW).move_to(_p(*BIG["center"]))
    set_backstroke(q, width=14)
    tag = T("your circuit?", 40).move_to(_p(0, -3.4))
    g = VGroup(grid, q, tag)
    g.grid, g.q, g.tag = grid, q, tag
    return g


# ---------------------------------------------------------------- the GAL (ch4 s6) and icons
def _strip_text(m):
    """Remove every Text / MathTex anywhere under m (from its own parent)."""
    for sub in list(m.submobjects):
        if isinstance(sub, (Text, MathTex, SingleStringMathTex)):
            m.remove(sub)
        else:
            _strip_text(sub)


def gal_and_tag():
    """ch4 s6's synchroniser GAL and its GOLD tag; a labelled placeholder until that file exists."""
    try:
        m = load_scene("ch4_s6_sync")
        gal = m.sync_gal()
        # sync_gal() leaves the stale "a"/"b" input labels inside .bank (under its e/r): drop them
        gal.bank.remove(*gal.bank.labels)
        # at hook size every label would be ~size 14: show the GAL as a picture (gates, dots, wires)
        _strip_text(gal)
        tag = getattr(gal, "tag", None)
        if tag is not None:
            gal.remove(tag)
        else:
            tag = T("5 AND · 2 OR · 2 flip-flops", 34, GOLD)
        return gal, tag
    except Exception:  # noqa: BLE001  (placeholder: ch4_s6_sync not built yet)
        gal = load_scene("ch4_s1_hook").package("GAL", w=5.0, h=2.8, n_pins=8, size=48)
        return gal, T("5 AND · 2 OR · 2 flip-flops", 34, GOLD)


def factory():
    pts = [(-0.8, -0.55), (-0.8, 0.25), (-0.4, 0.55), (-0.4, 0.25), (0.0, 0.55), (0.0, 0.25),
           (0.4, 0.55), (0.4, 0.95), (0.62, 0.95), (0.62, 0.25), (0.8, 0.25), (0.8, -0.55)]
    body = Polygon(*[_p(x, y) for x, y in pts]).set_stroke(DIM, 4).set_fill(BG, 0)
    door = Rectangle(width=0.36, height=0.5).set_stroke(DIM, 3).move_to(_p(0.0, -0.3))
    return VGroup(body, door)


def laptop():
    screen = RoundedRectangle(corner_radius=0.06, width=1.3, height=0.85).set_stroke(FG, 4).set_fill(BG, 0)
    base = Polygon(_p(-0.8, -0.5), _p(0.8, -0.5), _p(0.65, -0.42), _p(-0.65, -0.42)).set_stroke(FG, 4)
    screen.move_to(_p(0, 0.0))
    return VGroup(screen, base)


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(1.0)   # handover: s2 opens on this shot

    def clip1(self):
        card = title_card(PART_LINE)
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        end = open_card()
        self.add(*end)
        with self.say("c5.hook.1") as c:
            part5 = end.part
            self.wait(0.7)   # ch4's end card holds a moment: the cut reads as a continuation
            self.play(*during(disappear(end.grid, end.zoom, end.tile, end.bits, end.fpga_tag, end.lut_tag), 0, 0.4),
                      *during([part5.animate.scale(card.part.height / part5.height).move_to(card.part)], 0.1, 0.6),
                      *during(appear(card.title, card.rule, card.course, lag=0.2), 0.55, 1),  # early: title card
                      run_time=min(1.5, c.until("last", floor=1.0)))
            self.remove(part5)
            self.add(card.part)
            c.wait_until("last")

            # {last}: the synchroniser GAL, small and centred, with its GOLD tag
            gal, gtag = gal_and_tag()
            gal.scale_to_fit_width(5.6)
            if gal.height > 3.2:
                gal.scale_to_fit_height(3.2)
            gal.move_to(_p(0, -0.3))
            gtag.next_to(gal, DOWN, buff=0.35)
            sweep_clear(self, *appear(gal, shift=None), run_time=1.6)
            c.wait_until("five and gates")
            self.play(*appear(gtag), run_time=min(1.0, c.until("latest", floor=0.5)))
            c.wait_until("latest")

            # {latest}: p. 158's first bullet, verbatim, above the GAL
            cap = T("Field Programmable Gate Arrays (FPGAs) are\nthe latest type of programmable logic", 36,
                    line_spacing=0.9).move_to(_p(0, 3.0))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.2)
            c.wait_until("field")

            # {field}: "Field Programmable" YELLOW; the GAL steps aside; a factory sends out a blank chip
            gal_g = VGroup(gal, gtag)
            fac = factory().move_to(_p(1.0, -0.5))
            chip = load_scene("ch4_s1_hook").package(None, w=1.5, h=1.0, n_pins=4).move_to(_p(3.45, -0.5))
            self.play(*recolor(select(cap, "Field Programmable")[0], YELLOW),
                      gal.animate.scale(0.72).move_to(_p(-3.6, -0.3)),
                      gtag.animate.move_to(_p(-3.6, -0.3 - 0.36 * gal.height - 0.6)),
                      run_time=0.9)
            self.play(*appear(fac, shift=None),
                      time_span(FadeIn(chip, shift=1.6 * RIGHT), 0.35, 1.2), run_time=1.2)
            # a laptop beside it streams GOLD into the chip; the tag says who programs it
            lap = laptop().move_to(_p(5.75, -0.45))
            path = Line(_p(5.0, -0.45), _p(4.35, -0.45))
            dots = [Dot(path.get_start(), radius=0.07, color=GOLD).set_opacity(0) for _ in range(4)]
            arrow = Arrow(_p(5.05, -0.45), _p(4.3, -0.45), buff=0, stroke_width=4, color=GOLD,
                          max_tip_length_to_length_ratio=0.35)
            ftag = T("programmed by you,\nafter it's made", 32, line_spacing=0.9).move_to(_p(3.5, -2.1))
            self.add(*dots)
            self.play(*during(appear(lap, shift=None), 0, 0.35),
                      *during([GrowArrow(arrow)], 0.15, 0.45),
                      *[time_span(UpdateFromAlphaFunc(
                          d, lambda m, a, path=path: m.move_to(path.point_from_proportion(a)).set_opacity(
                              min(1, 4 * a, 4 * (1 - a)))), 0.7 + 0.25 * i, 1.4 + 0.25 * i)
                        for i, d in enumerate(dots)],
                      time_span(chip.body.animate.set_stroke(GOLD, 4), 1.2, 2.0),
                      time_span(FadeIn(ftag, shift=0.25 * DOWN), 1.3, 2.3),
                      run_time=min(2.3, c.until(floor=1.0)))
            self.remove(*dots)
            self.icons = [cap, fac, chip, lap, arrow, ftag]
            self.gal, self.gtag, self.gal_g = gal, gtag, gal_g

    def clip2(self):
        gal, gtag = self.gal, self.gtag
        G = tile_grid(**BIG)
        tile = G.tile(*GAL_RC)
        with self.say("c5.hook.2") as c:
            # {grid}: caption and icons fade; the GAL comes back to the centre
            c.wait_until("than a gal")
            self.play(*disappear(*self.icons), run_time=min(0.8, c.until("tiles", floor=0.5)))
            c.wait_until("tiles")

            # {tiles}: the GAL shrinks into one tile of a big grid of identical tiles
            order = sorted(G.tiles, key=lambda t: np.linalg.norm(t.get_center() - tile.get_center()))
            target = gal.copy().scale_to_fit_width(G.side * 0.8).move_to(tile)
            if target.height > G.side * 0.8:
                target.scale_to_fit_height(G.side * 0.8)
            self.play(*during(disappear(gtag), 0, 0.3),
                      gal.animate.scale(target.width / gal.width).move_to(tile),
                      *during([FadeIn(G.wires)], 0.4, 1),
                      *during(appear(*order, shift=None, lag=0.03), 0.3, 1),
                      run_time=2.2)
            c.wait_until("identical")
            self.play(restyle(tile, outline=YELLOW, width=5),
                      FlashAround(tile, run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("logic")
            self.play(*disappear(gal), restyle(tile, outline=TEAL, width=2.5), run_time=1.2)
            c.wait_until("ask")

            # {ask}: a YELLOW "?" inside one tile
            q_small = T("?", 48, YELLOW).move_to(tile)
            self.play(*appear(q_small, shift=None), run_time=1.0)
            c.wait_until("blank")

            # {blank}: every tile goes DIM and empty; one big "?" over the whole grid
            hs = handover_shot()
            self.play(*[restyle(t, outline=DIM, width=2.5) for t in G.tiles],
                      ReplacementTransform(q_small, hs.q), run_time=1.6)
            c.wait_until(own_word=hs.tag)
            self.play(*appear(hs.tag), run_time=1.0)
            # the last frame is exactly handover_shot()
            self.remove(*G.get_family())
            self.add(hs.grid)
            self.bring_to_front(hs.q)
