"""Chapter 4, scene 7: the five-slot recap, then the synchroniser GAL shrinks into an FPGA tile. Clips c4.recap.1 – c4.recap.3.

Grid (as ch6 s8): "Recap" T 44 at the top, five faint DIM slot frames (3 on top, 2 below), each tile its
scene's own object (load_scene, scaled down), its short line under it.
 r1 s2's moore_schematic() + two_brackets(); r2 s3's small_pla() and small_pal(), GOLD "3" / "4";
 r3 s4's gla() (chip outline dropped); r4 s6's gal() over a small compiler row; r5 s6's sync_gal()
 (terms dropped), GOLD "5 AND · 2 flip-flops".
{next}: the tiles clear, "Recap" gives way to ch5's part line, r5's GAL comes to the centre.
{fpga}: ch5's grid fades in, the GAL shrinks into the YELLOW .src tile; "FPGA". {lut}: the zoom lines,
the big tile, D1's 16 bits, "lookup table". The last frame is exactly ch5_s1_hook.open_card().
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

S2 = load_scene("ch4_s2_needs")
S3 = load_scene("ch4_s3_plapal")
S4 = load_scene("ch4_s4_gla")
S6 = load_scene("ch4_s6_sync")
C5 = load_scene("ch5_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the grid (ch6 s8's geometry, five slots) ------------------------------------------------
SLOTS = ((-4.5, 1.3), (0.0, 1.3), (4.5, 1.3), (-2.3, -1.95), (2.3, -1.95))
SW, SH = 4.2, 3.1
CAP = 30
PW, PH = 3.8, 1.95          # picture area


def slot(i):
    return SLOTS[i]


def pic_c(i, dy=0.3):
    x, y = slot(i)
    return _p(x, y + dy)


def cap_c(i):
    x, y = slot(i)
    return _p(x, y - 1.12)


def frame(i):
    x, y = slot(i)
    return RoundedRectangle(corner_radius=0.15, width=SW, height=SH).set_stroke(DIM, 2, opacity=0.5).move_to(_p(x, y))


def fit(m, w, h):
    m.scale(min(w / m.width, h / m.height))
    return m


def caption(i, text, size=CAP):
    return T(text, size, line_spacing=0.8).move_to(cap_c(i))


def _is_text(m):
    return isinstance(m, (Text, SingleStringMathTex))


def strip_text(m):
    """Drop every label (Text, MathTex, and small text+bar groups like Q-bar): thumbnails show the shapes."""
    for sub in list(m.submobjects):
        kids = sub.submobjects
        if _is_text(sub) or (kids and any(_is_text(k) for k in kids)
                             and all(_is_text(k) or (isinstance(k, Line) and k.width < 0.6) for k in kids)):
            m.remove(sub)
        else:
            strip_text(sub)
    return m


def mini_compiler_row(size=28):
    """s6's compiler_row, short: [equations] -> [compiler]."""
    et = T("equations", size)
    eb = RoundedRectangle(corner_radius=0.1, width=et.width + 0.3, height=0.55).set_stroke(FG, 2.5)
    et.move_to(eb)
    ar = Arrow(ORIGIN, RIGHT * 0.55, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.4).set_color(FG)
    ct = T("compiler", size, YELLOW)
    cb = RoundedRectangle(corner_radius=0.1, width=ct.width + 0.3, height=0.55).set_stroke(YELLOW, 2.5)
    ct.move_to(cb)
    ar = Arrow(UP * 0.4, ORIGIN, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.4).set_color(FG)
    g = VGroup(VGroup(eb, et), ar, VGroup(cb, ct)).arrange(DOWN, buff=0.08)
    return g


# ---- tiles ------------------------------------------------------------------------------------
def tile_r1():
    sch = S2.moore_schematic()
    br = S2.two_brackets(sch)
    g = strip_text(VGroup(sch, br))
    return fit(g, PW, PH + 0.1).move_to(pic_c(0, 0.3))


def tile_r2():
    pla = S3.small_pla()
    pal = S3.small_pal(programmed=True)
    strip_text(pla.core)
    strip_text(pal.core)
    fit(pla.core, 1.85, 1.45).move_to(pic_c(1, 0.62) + LEFT * 1.0)
    fit(pal.core, 1.85, 1.45).move_to(pic_c(1, 0.62) + RIGHT * 1.0)
    n3 = T("3", 34, GOLD).next_to(pla.core, DOWN, buff=0.1)
    n4 = T("4", 34, GOLD).next_to(pal.core, DOWN, buff=0.1)
    n4.align_to(n3, DOWN)
    return pla.core, pal.core, n3, n4


def tile_r3():
    g = S4.gla()
    g.remove(g.chip)
    strip_text(g)
    return fit(g, PW, PH).move_to(pic_c(2, 0.3))


def tile_r4():
    g = strip_text(S6.gal())
    fit(g, 2.1, 1.8).move_to(pic_c(3, 0.4) + LEFT * 0.95)
    row = mini_compiler_row().move_to(pic_c(3, 0.4) + RIGHT * 1.05)
    return g, row


def tile_r5():
    g = S6.sync_gal()
    g.remove(*g.terms)
    strip_text(g)
    fit(g, 1.75, 1.8).move_to(pic_c(4, 0.4) + LEFT * 1.12)
    n = VGroup(T("5 AND", 30, GOLD), T("2 flip-flops", 30, GOLD)).arrange(DOWN, buff=0.22)
    n.move_to(pic_c(4, 0.4) + RIGHT * 0.98)
    return g, n


# ---- end card (ch5's opening card) -------------------------------------------------------------
def handover_shot():
    return C5.open_card()


HERO_C = _p(0, -0.25)


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)          # end card, the music carries it; ch5 s1 opens on this frame

    # -- c4.recap.1 -----------------------------------------------------------------------------
    def clip1(self):
        head = T("Recap", 44).move_to(_p(0, 3.2))
        frames = [frame(i) for i in range(5)]
        self.head = head
        v1 = tile_r1()
        cap1 = caption(0, "logic + D flip-flops")
        pla, pal, n3, n4 = tile_r2()
        cap2 = caption(1, "PLA shares,\nPAL makes it twice", 28)
        with self.say("c4.recap.1") as c:
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames],  # early: the heading
                      run_time=min(1.2, c.until("r1")))
            c.wait_until("r1")
            self.play(FadeIn(v1), run_time=1.3)
            c.wait_until("combinational logic")
            self.play(*appear(cap1), run_time=1.0)  # early: the tile's line sums up the sentence
            c.wait_until("r2")
            self.play(FadeIn(pla), *appear(n3, shift=None), run_time=1.3)
            c.wait_until("A PAL fixes")
            self.play(FadeIn(pal), *appear(n4, shift=None), run_time=1.3)
            c.wait_until("each product term")
            self.play(*appear(cap2), run_time=1.0)  # early: the line sums up both sentences

    # -- c4.recap.2 -----------------------------------------------------------------------------
    def clip2(self):
        v3 = tile_r3()
        cap3 = caption(2, "flip-flops, fed back")
        g4, row = tile_r4()
        cap4 = caption(3, "fixed OR plane")
        g5, n5 = tile_r5()
        cap5 = caption(4, "the synchroniser")
        self.g5 = g5
        with self.say("c4.recap.2", gap=1.5) as c:
            self.play(FadeIn(v3), run_time=1.3)
            c.wait_until("feeds the state back")
            self.play(*appear(cap3), run_time=1.0)
            c.wait_until("r4")
            self.play(FadeIn(g4), run_time=1.3)
            c.wait_until("a compiler")
            self.play(*appear(row, shift=None), *appear(cap4), run_time=1.2)  # early: the tile's line
            c.wait_until("r5")
            self.play(FadeIn(g5), *appear(cap5), run_time=1.3)
            c.wait_until("five and gates")
            self.play(*appear(n5, shift=None), run_time=1.0)

    # -- c4.recap.3: next time ------------------------------------------------------------------
    def clip3(self):
        card = C5.open_card()
        g5 = self.g5
        with self.say("c4.recap.3") as c:
            others = [m for m in self.mobjects if m is not g5 and m is not self.head]
            g5.generate_target()
            fit(g5.target, 8.6, 5.4).move_to(HERO_C)
            self.play(*during(disappear(*others), 0, 0.45),  # early: the next part's heading
                      *swap(self.head, card.part),
                      *during([MoveToTarget(g5)], 0.35, 1), run_time=min(2.2, c.until("fpga")))
            c.wait_until("fpga")
            src = card.src
            g5.generate_target()
            g5.target.scale(src.width * 0.9 / g5.width).move_to(src)
            others5 = [m for m in card.grid if m is not src]
            self.play(*during([FadeIn(m) for m in others5], 0, 0.5),
                      *during([MoveToTarget(g5)], 0.15, 0.85),
                      *during([FadeIn(src)], 0.7, 1), run_time=2.2)
            settle(self, card.grid)
            self.play(FadeOut(g5), run_time=0.6)
            c.wait_until("field programmable")
            self.play(*appear(card.fpga_tag), run_time=1.0)  # early: "FPGA" was just spelled out
            c.wait_until("whole grid")
            self.play(FlashAround(card.grid, run_time=2, time_width=1.5, color=TEAL))
            c.wait_until("lut")
            self.play(*[Create(z) for z in card.zoom], FadeIn(card.tile), run_time=1.2)
            self.play(*appear(*card.bits, shift=None, lag=0.06),
                      *during(appear(card.lut_tag), 0.5, 1), run_time=min(1.6, c.until(floor=0.8)))
        self.remove(*self.mobjects)
        self.add(handover_shot())
