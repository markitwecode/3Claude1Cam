"""Chapter 5, scene 1: hook. ch4's end card, the title card, two clock-only machines, a serial
bit stream with a repeating pattern, and p. 123's A/B/C renamed Sync/Hunt/Sight. Clips c5.hook.1 – c5.hook.3.

Opens exactly on ch4_s8_recap's end_card() (held 0.7 s; its part line travels into the title card).
Ends on an empty frame.
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
from lib.titles import title_card  # noqa: E402

R8 = load_scene("ch4_s8_recap")       # end_card, part_chips
S3 = load_scene("ch4_s3_ring4")       # ring4
S1 = load_scene("ch1_s1_hook")        # lamp_column, STATE_LAMPS, lamp colours
S25 = load_scene("ch2_s5_ring")       # ring_cell_style, cell_bit
D5 = load_scene("ch1_s5_divide5")     # state_ring
F2 = load_scene("ch5_s2_frames")      # bit_digit, pattern_box, PATTERN, PLAIN, P
M2 = load_scene("ch1_s2_machines")    # moore_diagram
SD = load_scene("ch5_s3_diagram")     # sync_diagram

LAMP_COLS = (S1.LAMP_RED, S1.LAMP_AMBER, S1.LAMP_GREEN)


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- clip 1: the two clock-only machines ---------------------------------------------------------
OH_S = 0.55
OH_C = _p(-3.55, -0.3)
FIVE_C = _p(3.75, 0.15)
TAG_Y = -2.95
BIN = ["000", "001", "010", "011", "100"]


def onehot_machine():
    """ch4's ring4 (one-hot traffic light), small: labels dropped, own digits, a lamp column above."""
    R = S3.ring4("1000")
    for ff in R.ffs:
        ff.remove(ff.d_l, ff.q_l)
    R.remove(*R.labels, *R.heads, *R.bits)
    R.clk.remove(R.clk_label)
    paths = VGroup(*R.wire_paths)
    VGroup(R, paths).scale(OH_S, about_point=ORIGIN).shift(OH_C)
    off = 0.35 * S3.R4_S * OH_S * DOWN
    R.dpos = [c.get_center() + off for c in R.cells]
    R.digs = [S25.cell_bit(b, 32).move_to(R.dpos[i]) for i, b in enumerate("1000")]
    R.values = [1, 0, 0, 0]
    R.paths = paths
    R.clk_l = T("CLK", 30, YELLOW).next_to(R.clk_line.get_start(), DOWN, buff=0.15, aligned_edge=LEFT)
    R.lamps = S1.lamp_column(S1.STATE_LAMPS[0], scale=1.4).move_to(_p(OH_C[0], OH_C[1] + 2.15))
    return R


def five_machine():
    ring = D5.state_ring(codes=BIN, center=FIVE_C)
    clk = Arrow(FIVE_C + 2.55 * DOWN, FIVE_C + 0.35 * DOWN, buff=0, stroke_width=5, color=YELLOW,
                tip_length=0.22, max_tip_length_to_length_ratio=0.3)
    clk_l = T("CLK", 30, YELLOW).next_to(clk.get_start(), LEFT, buff=0.15)
    hl = Circle(radius=D5.NODE_R + 0.1).set_stroke(YELLOW, 5).move_to(ring.circles[0])
    return ring, clk, clk_l, hl


# ---- clip 2: the stream ---------------------------------------------------------------------------
GAP = 18
DATA = F2.PLAIN
STREAM = "".join(F2.PATTERN + DATA[(10 * k) % 36:(10 * k) % 36 + 10] for k in range(6))
NS = len(STREAM)
SY = 0.15
REC_L, REC_R = 4.85, 6.6
SPEED = 0.85
SHIFT0 = REC_L - 0.2 - F2.bx(NS - 1)      # at offset 0 the last bit sits just left of the receiver


def _fade(x):
    a = np.clip((x + 6.6) / 0.6, 0, 1)
    b = np.clip((REC_L - 0.15 - x) / 0.3, 0, 1)
    return float(min(a, b))


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c5.hook.1 ---------------------------------------------------------------------------------
    def tick(self, run_time=0.8, five=True):
        R = self.oh
        i = R.values.index(1)
        j = (i + 1) % 4
        old_i, old_j = R.digs[i], R.digs[j]
        new_i = S25.cell_bit(0, 32).move_to(R.dpos[i])
        new_j = S25.cell_bit(1, 32).move_to(R.dpos[j])
        ti, tj = R.cells[i].copy(), R.cells[j].copy()
        S25.ring_cell_style(ti, 0)
        S25.ring_cell_style(tj, 1)
        p = R.paths[i].copy().set_stroke(GOLD, 7)
        ck = R.clk_line.copy().set_stroke(YELLOW, 9)
        anims = [*during(disappear(old_j), 0, 0.3), *during(appear(new_j, shift=None), 0.3, 0.65),
                 *during(disappear(old_i), 0.5, 0.8), *during(appear(new_i, shift=None), 0.8, 1.0),
                 Transform(R.cells[i], ti), Transform(R.cells[j], tj),
                 VShowPassingFlash(p, time_width=0.6, taper_width=0.1),
                 VShowPassingFlash(ck, time_width=0.6, taper_width=0.1)]
        anims += [R.lamps.lamps[k].animate.set_fill(LAMP_COLS[k] if S1.STATE_LAMPS[j][k] else S1.LAMP_OFF, 1)
                  for k in range(3)]
        if five:
            self.k5 = (self.k5 + 1) % 5
            anims.append(self.hl.animate.move_to(self.ring5.circles[self.k5]))
            anims.append(VShowPassingFlash(Line(self.clk5.get_start(), self.clk5.get_end())
                                           .set_stroke(YELLOW, 9), time_width=0.6, taper_width=0.1))
        self.play(*anims, run_time=run_time)
        R.values[i], R.values[j] = 0, 1
        R.digs[i], R.digs[j] = new_i, new_j

    def ticks_until(self, c, cue=None, period=1.25, five=True):
        while c.until(cue, floor=0) > period:
            self.wait(period - 0.8)
            self.tick(five=five)

    def clip1(self):
        end = R8.end_card()
        self.add(end)
        with self.say("c5.hook.1") as c:
            card = title_card("Part 5 · Hunt, Sight and Sync")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            part = end.part
            self.wait(0.7)   # ch4's end card holds a moment: the cut reads as a continuation
            rest = [end.tape, end.circles, *end.chips.submobjects]   # (the chips group's .dim attr shadows Mobject.dim)
            self.play(*during(disappear(*rest), 0, 0.4),
                      *during([part.animate.scale(card.part.height / part.height).move_to(card.part)], 0.1, 0.6),
                      *during(appear(card.title, card.rule, card.course, lag=0.2), 0.55, 1),  # early: title card
                      run_time=1.6)
            self.remove(*end.get_family())
            self.add(card.part)

            # {last}: ch4's one-hot traffic light, small at the left
            c.wait_until("one-hot")
            oh = self.oh = onehot_machine()
            sweep_clear(self, FadeIn(oh), *[FadeIn(d) for d in oh.digs], FadeIn(oh.clk_l),  # early: ch4's machine
                        FadeIn(oh.lamps), run_time=1.4)
            self.ticks_until(c, "clockonly", five=False)

            # {clockonly}: ch1's divide-by-5 ring at the right, its own CLK wire
            c.wait_until("clockonly")
            ring, clk5, clk5_l, hl = five_machine()
            self.ring5, self.clk5, self.hl, self.k5 = ring, clk5, hl, 0
            self.play(*appear(ring, shift=None),  # early: ch1's machine, shown whole
                      *during([GrowArrow(clk5)], 0.4, 1), *during(appear(clk5_l, hl, shift=None), 0.5, 1),
                      run_time=1.3)
            self.ticks_until(c, "nothing")

            # "Nothing from outside": inputs: none under each
            c.wait_until("nothing")
            tags = [T("inputs: none", 30, DIM).move_to(_p(OH_C[0], TAG_Y)),
                    T("inputs: none", 30, DIM).move_to(_p(FIVE_C[0], TAG_Y))]
            self.play(*appear(*tags, lag=0.3), run_time=1.0)  # early: a tag, not a spoken word
            self.ticks_until(c)

    # -- c5.hook.2 ---------------------------------------------------------------------------------
    def clip2(self):
        with self.say("c5.hook.2") as c:
            rec_box = Rectangle(width=REC_R - REC_L, height=1.3).set_stroke(BLUE, 4).set_fill(BG, 1)
            rec_box.move_to(_p((REC_L + REC_R) / 2, SY)).set_z_index(2)
            rec_l = T("receiver", 30).move_to(rec_box).set_z_index(3)
            bits = [F2.bit_digit(ch, i, SY) for i, ch in enumerate(STREAM)]
            starts = list(range(0, NS - 7, GAP))
            boxes = [F2.pattern_box(s, SY).stretch_to_fit_width(8 * F2.P) for s in starts]
            in_pat = {s + k for s in starts for k in range(8)}   # the boxed bits turn YELLOW with their box
            base_b = [b.get_x() for b in bits]
            base_x = [b.get_x() for b in boxes]
            state = {"off": 0.0, "vis": 0.0}

            def layout(m, dt=0.0):
                state["off"] += SPEED * dt
                d = SHIFT0 + state["off"]
                for i, (b, x0) in enumerate(zip(bits, base_b)):
                    b.set_x(x0 + d)
                    if i in in_pat:
                        b.set_color(interpolate_color(ManimColor(FG), ManimColor(YELLOW), state["vis"]))
                    b.set_opacity(_fade(x0 + d))
                for bx, x0 in zip(boxes, base_x):
                    x = x0 + d
                    op = min(_fade(x - bx.width / 2 + 0.3), _fade(x + bx.width / 2 - 0.3))
                    bx.set_x(x)
                    bx.set_stroke(opacity=state["vis"] * op)
                return m

            tape = VGroup(*boxes, *bits)
            layout(tape)
            c.wait_until("receiver")
            sweep_clear(self, FadeIn(rec_box), FadeIn(rec_l), FadeIn(tape), run_time=1.4)  # early: the receiver
            tape.add_updater(layout)

            # {pattern}: the boxes come up round every copy
            c.wait_until("pattern")
            vis = ValueTracker(0)

            def show(m):
                state["vis"] = vis.get_value()
            vis.add_updater(show)
            self.add(vis)
            self.play(vis.animate.set_value(1), run_time=1.2)
            vis.clear_updaters()
            state["vis"] = 1.0

            # {ask}: where does each frame start?
            c.wait_until("ask")
            qs = [T("?", 60, YELLOW).move_to(_p(x, SY + 1.15)) for x in (-4.2, -1.3, 1.6)]
            self.play(*appear(*qs, lag=0.3), run_time=1.3)
            self.stream = (tape, layout)
            self.qs = qs

    # -- c5.hook.3 ---------------------------------------------------------------------------------
    def clip3(self):
        tape, layout = self.stream
        with self.say("c5.hook.3", gap=1.8) as c:
            title = T("Tripos question", 44)
            sub = T("(a Cambridge exam question)", 32, DIM)
            VGroup(title, sub).arrange(DOWN, buff=0.25).move_to(_p(0, 0.6))
            box = RoundedRectangle(corner_radius=0.15, width=sub.width + 0.8, height=1.45).set_stroke(DIM, 2)
            box.move_to(VGroup(title, sub))
            # the ?s leave first: they sit where the card lands
            fade_q = max(0.4, min(0.7, c.until(own_word=title, floor=0.4)))
            self.wait(max(0, c.until(own_word=title, floor=0) - fade_q))
            self.play(*disappear(*self.qs), run_time=fade_q)
            c.wait_until(own_word=title)
            sweep_clear(self, FadeIn(box), *appear(title, sub, lag=0.4, shift=None), run_time=1.6)
            tape.clear_updaters()
            self.remove(tape)

            # {lecture9}: p. 123's circles, letters only; the card goes to the corner
            c.wait_until("lecture9")
            md = M2.moore_diagram(names=("A", "B", "C"), r=0.62)
            small = title.copy().scale(32 / 44).move_to(_p(-5.0, 3.3))
            sbox = RoundedRectangle(corner_radius=0.12, width=small.width + 0.5, height=0.75).set_stroke(DIM, 2)
            sbox.move_to(small)
            low = _p(0, -2.75) - box.get_center()
            self.play(*[m.animate.shift(low) for m in (box, title, sub)],
                      *during(appear(*md.circles, lag=0.2, shift=None), 0.4, 1),  # early: p. 123's circles
                      run_time=1.8)
            c.wait_until("back then")
            self.play(*appear(*md.names, lag=0.25), run_time=1.2)  # early: the letters are read next

            # "state A, state bee and state see"
            for cue, k in (("state A", 0), ("state bee", 1), ("state see", 2)):
                c.wait_until(cue)
                self.play(S1.ring_flash(md.circles[k]),
                          run_time=min(1.2, max(0.6, c.until("names", floor=0.6))))

            # {names}: Hunt (B), Sight (C), Sync (A)
            c.wait_until("names")
            sd = SD.sync_diagram()
            new = {"Sync": sd.name["Sync"], "Hunt": sd.name["Hunt"], "Sight": sd.name["Sight"]}
            for nm, k, nxt in (("Hunt", 1, "Sight"), ("Sight", 2, "Sync"), ("Sync", 0, "job")):
                c.wait_until(nm)
                self.play(*swap(md.names[k], new[nm]), run_time=max(0.6, min(1.0, c.until(nxt, floor=0.6))))

            # {plan}: the two chips
            c.wait_until("plan")
            chips = R8.part_chips()
            lit, dimchip = chips.submobjects
            self.play(*during(disappear(box, title, sub), 0, 0.45),
                      *during(appear(sbox, small, shift=None), 0.5, 1),  # early: the card, moved
                      run_time=min(1.4, c.until("two flip-flops", floor=0.8)))
            c.wait_until("two flip-flops")
            self.play(*appear(lit), run_time=1.0)  # early: the chip names its part
            c.wait_until("one-hot")
            self.play(*appear(dimchip), run_time=1.0)
