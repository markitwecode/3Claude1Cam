"""Chapter 5, scene 8: recap of the FPGA chapter and the turn to electricity. Clips c5.recap.1 – c5.recap.2.

Six slots (3 x 2), each filled with a small copy of its scene's own drawing (via load_scene):
s2 spartan_array + routes[0], s3 recap_shot, s4 clb(programmed=True), s5 recap_shot, s6 pipeline_shot,
s7 cost_plot. Then the dive: r1's array to the centre, into one CLB, its G table, gates, transistors;
the battery-and-lamp loop builds into ch6_s1_hook.open_card(), which is the last frame (held ~8 s).
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

S2A = load_scene("ch5_s2_array")
S3 = load_scene("ch5_s3_lut")
S4 = load_scene("ch5_s4_clb")
S5 = load_scene("ch5_s5_oneclb")
S6 = load_scene("ch5_s6_configure")
S7 = load_scene("ch5_s7_custom")
H6 = load_scene("ch6_s1_hook")
E6 = load_scene("ch6_s2_electrons")

SLOT_W, SLOT_H = 4.35, 3.4
COLS = (-4.6, 0.0, 4.6)
ROWS = (1.78, -1.78)
TILE_W, TILE_H = 3.8, 2.0
TILE_DY = 0.52                     # thumbnail centre above the slot centre
CAP_BOTTOM = 0.28                  # caption's bottom edge above the card's bottom border

CAPTIONS = (
    ("blocks, routing,\ninput-output blocks", "blocks"),
    ("a lookup table stores\na truth table", "lookup table"),
    ("two 4-input tables, one\n3-input, two flip-flops", "flip-flops"),
    ("the synchroniser\nin one block", "synchroniser"),
    ("design → synthesis\n→ static RAM", "static RAM"),
    ("few: FPGA\nmillions: custom chip", "custom chips"),
)


def slot_center(k):
    return np.array([COLS[k % 3], ROWS[k // 3], 0.0])


def fit(m, w=TILE_W, h=TILE_H):
    m.scale(min(w / m.width, h / m.height))
    return m


def tiles():
    arr = S2A.spartan_array(center=(0, 0))
    t1 = VGroup(arr, arr.routes[0])
    t1.arr, t1.route = arr, arr.routes[0]
    out = [t1, S3.recap_shot(ORIGIN), S4.clb(programmed=True), S5.recap_shot(),
           S6.pipeline_shot(), S7.cost_plot()]
    for k, t in enumerate(out):
        S6.strip_text(t)                 # thumbnails: their labels would be too small to read
        fit(t).move_to(slot_center(k) + TILE_DY * UP)
    out[1].add(lut_bits(out[1][1].lut))
    return out


def lut_bits(lut, size=30):
    """s3's 16 bits put back, large enough to read, on the (scaled) lookup-table grid."""
    sq = lut.grid[0]
    L, top, cell = sq.get_left()[0], sq.get_top()[1], sq.width / 4
    bits = VGroup()
    for i, b in enumerate(S3.D1_BITS):
        r, k = divmod(i, 4)
        col = YELLOW if (r, k) == (1, 3) else (GREEN if b == "1" else DIM)
        bits.add(MathTex(b, font_size=size, color=col).move_to([L + (k + 0.5) * cell, top - (r + 0.5) * cell, 0]))
    return bits


def caption(k):
    """Two centred lines, the block's bottom CAP_BOTTOM above the card's bottom border (same in all six)."""
    lines = VGroup(*[T(s, 28) for s in CAPTIONS[k][0].split("\n")]).arrange(DOWN, buff=0.12)
    bottom = slot_center(k)[1] - SLOT_H / 2 + CAP_BOTTOM
    return lines.move_to([slot_center(k)[0], bottom + lines.height / 2, 0])


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()

    # -- c5.recap.1: six slots, one per sentence --------------------------------------------------
    def clip1(self):
        with self.say("c5.recap.1") as c:
            self.slots = [RoundedRectangle(corner_radius=0.18, width=SLOT_W, height=SLOT_H)
                          .set_stroke(DIM, 2).set_fill(BG, 0).move_to(slot_center(k)) for k in range(6)]
            self.play(LaggedStart(*[FadeIn(s) for s in self.slots], lag_ratio=0.15),
                      run_time=min(1.4, c.until("r1")))
            self.tiles = tiles()
            self.caps = [caption(k) for k in range(6)]
            for k in range(6):
                c.wait_until(f"r{k + 1}")
                nxt = f"r{k + 2}" if k < 5 else None
                self.play(FadeIn(self.tiles[k], scale=0.9), run_time=min(1.4, 0.4 * c.until(nxt)))
                c.wait_until(CAPTIONS[k][1])
                self.play(*appear(self.caps[k]), run_time=min(1.0, max(0.5, 0.5 * c.until(nxt))))

    # -- c5.recap.2: next time: gates, transistors, electricity -----------------------------------
    def clip2(self):
        t1 = self.tiles[0]
        others = self.tiles[1:] + self.caps[1:] + self.slots[1:]
        with self.say("c5.recap.2") as c:
            # {next}: the slots dim, r1's array comes to the centre
            self.play(*set_alpha(others, DIMMED), *disappear(self.caps[0], self.slots[0]), run_time=0.7)
            self.remove(self.caps[0], self.slots[0])
            self.play(*during([FadeOut(m) for m in others], 0, 0.4),
                      *during([t1.animate.scale(6.0 / t1.height).move_to(0.1 * DOWN)], 0.25, 1.0),
                      run_time=1.0)

            # dive into CLB(1, 0): it grows into the frame, the rest flies past and fades
            arr = t1.arr
            ch = arr.clb(1, 0)
            arr.remove(ch)
            self.add(ch)
            cpt = ch.get_center()
            big = Rectangle(width=8.4, height=5.4).set_stroke(TEAL, 4).set_fill(BG, 0).move_to(0.1 * DOWN)
            g_name = T("G", 44, YELLOW).move_to(big.get_corner(UL) + np.array([0.5, -0.45, 0]))
            grid = S3.lut_grid(S3.D1_BITS, center=(0.25, -0.45, 0), cell=0.95, size=44, head_size=36)
            self.play(*during([t1.animate.scale(5, about_point=cpt).set_opacity(0)], 0, 0.7),
                      *during([ReplacementTransform(ch.box, big)], 0, 0.7),
                      *during([FadeIn(grid), FadeIn(g_name)], 0.6, 1.0),
                      run_time=1.2)
            self.remove(t1, ch)
            self.add(big)

            # {gates}: the table opens into a handful of gates
            c.wait_until("gates")
            self.wait(0.5)                   # hold: the table fills the frame
            a1 = H6._at(H6.and_gate(), [-1.7, 1.0, 0])
            a2 = H6._at(H6.and_gate(), [-1.7, -1.2, 0])
            og = H6._at(H6.or_gate(1.8, 1.4), [1.4, -0.1, 0])
            L, R = big.get_left()[0], big.get_right()[0]
            ins = VGroup(*[H6.wire([L, p[1], 0], p) for g in (a1, a2) for p in g.ins])
            mid = VGroup(H6.wire(a1.out, [0.0, a1.out[1], 0], [0.0, og.ins[0][1], 0], og.ins[0]),
                         H6.wire(a2.out, [0.0, a2.out[1], 0], [0.0, og.ins[1][1], 0], og.ins[1]))
            outw = H6.wire(og.out, [R, og.out[1], 0])
            self.play(*during(disappear(grid, g_name), 0, 0.45),
                      *during([FadeIn(VGroup(a1, a2, og)), FadeIn(VGroup(ins, mid, outw))], 0.5, 1.0),
                      run_time=1.2)

            # {transistors}: one gate goes translucent, transistors inside
            trs = VGroup(*[H6.transistor().scale(0.8).move_to(og.get_center() + np.array([dx, dy, 0]))
                           for dx in (-0.38, 0.0) for dy in (0.19, -0.19)])
            tag = T("transistors", 32, FG).move_to([1.4, -1.45, 0])
            c.wait_until("transistors")      # its first mention (own_word could skip to the second)
            self.play(*set_alpha([a1, a2, ins, mid, outw, big], DIMMED),
                      og.animate.set_stroke(opacity=0.35), FadeIn(trs), *appear(tag),
                      run_time=min(1.4, max(0.6, c.until("electricity") - 0.2)))

            # {electricity}: the gates slide away, the battery-and-lamp loop writes on
            c.wait_until("electricity")
            card = H6.open_card()
            loop, els, lmp, part = card.loop, card.els, card.lamp, card.part
            board = [big, a1, a2, og, ins, mid, outw, trs, tag]
            self.play(*during([m.animate.shift(15 * LEFT) for m in board], 0, 0.5),
                      *during([Create(w) for w in loop.wire], 0.4, 1.0),
                      *during([FadeIn(loop.battery)], 0.5, 1.0),
                      run_time=2.0)
            self.remove(*board)
            self.remove(*loop.wire, loop.battery)
            self.add(loop)
            els.start()
            # ch6_s2's own motion: drift E6.DRIFT anticlockwise (from the - terminal round to +), jitter 1
            self.play(FadeIn(lmp), FadeIn(els), *els.motion(drift=E6.DRIFT, jitter=1.0), run_time=1.2)

        # end card: the part line while they keep drifting, then they park (forward, never back); held
        self.play(*appear(part), run_time=1.0)  # early: end card
        self.wait(1.5)
        self.play(*els.motion(drift=0.0, jitter=0.0), run_time=1.0)
        step = loop.perimeter() / els.n
        self.play(els.pos.animate.set_value(np.ceil(els.pos.get_value() / step) * step), run_time=0.8)
        els.stop()
        self.wait(6.0)
