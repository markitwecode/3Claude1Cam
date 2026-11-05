"""Chapter 4, scene 5: the GAL (p. 157-158). Clips c4.gal.1 – c4.gal.4.

Opens on s4's handover (the GLA); ends on s6's opening_shot() (the large p. 158 GAL, all dots lit).
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

S3 = load_scene("ch4_s3_plapal")
S4 = load_scene("ch4_s4_gla")
S6 = load_scene("ch4_s6_sync")

W_SIDE = S6.Where(0.44, 0.0, 2.0, 1.65, 1.0)      # clip 4: GAL at the right, compiler row at the left
TERM = r"a\cdot\overline{b}"
EQS = [r"f_0 = a\cdot\overline{b} + \ldots", r"f_n = a\cdot\overline{b} + \ldots"]
KEEP = {0: (0, 6), 1: (4, 7), 2: (3, 5), 3: (4, 7)}   # the "programmed" pattern: gate -> rails kept


def handover_shot():
    """The last frame: s6's opening shot."""
    return S6.opening_shot()


def caption():
    lines = ["“A modified form of a GLA known as a Generic",
             "Array Logic (GAL) is used in the Hardware Laboratory",
             "classes to implement various FSMs.”"]
    return VGroup(*[T(s, 30, slant=ITALIC) for s in lines]).arrange(DOWN, buff=0.14).move_to(UP * 2.8)


def card(text, abbr, width):
    t = T(text, 36, t2c={abbr: BLUE})
    box = RoundedRectangle(corner_radius=0.12, width=width, height=0.72).set_stroke(DIM, 2.5)
    t.move_to(box)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def hand_icon():
    palm = RoundedRectangle(corner_radius=0.13, width=0.6, height=0.62)
    finger = RoundedRectangle(corner_radius=0.08, width=0.66, height=0.19)
    finger.move_to(palm.get_corner(UL) + RIGHT * 0.05 + DOWN * 0.13, aligned_edge=RIGHT)
    cuff = Rectangle(width=0.2, height=0.5).next_to(palm, RIGHT, buff=0)
    g = VGroup(finger, palm, cuff)
    for m in g:
        m.set_stroke(FG, 3).set_fill(BG, 1)
    g.tip = finger
    return g


def blink(dot, keep):
    def f(m, a):
        if keep:
            o = 0.15 + 0.85 * 0.5 * (1 + np.cos(a * 4 * PI))
        else:
            o = 0.15 + 0.85 * 0.5 * (1 + np.cos(a * 3 * PI)) * (1 - a) ** 0.3
        m.set_opacity(o)
    return UpdateFromAlphaFunc(dot, f)


def dim_part(m):
    """Grey a flip-flop part: outlines and coloured fills to DIM (BG fills stay BG)."""
    for sub in m.family_members_with_points():
        if sub.get_stroke_width() > 0:
            sub.set_stroke(DIM)
        if sub.get_fill_opacity() > 0 and ManimColor(sub.get_fill_color()).to_hex().upper() != BG.upper():
            sub.set_fill(DIM)
    return m


class Gal(NarratedScene):
    def construct(self):
        self.h = S4.handover_shot()
        self.add(self.h)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.remove(*self.mobjects)                  # invisible cut to the canonical handover shot
        self.add(handover_shot())
        self.wait(1.0)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        gla, tag = self.h[0], self.h[1]
        cap = caption()
        w = 6.3
        c1 = card("GLA: generic logic array", "GLA", w).move_to(RIGHT * 2.3 + UP * 1.5)
        c2 = card("GAL: generic array logic", "GAL", w).move_to(RIGHT * 2.3 + UP * 0.2)
        pal = S3.small_pal(programmed=True)
        core = pal.core
        core.scale(0.78).move_to(RIGHT * 3.4 + DOWN * 1.7)
        ptag = T("fixed OR plane, like a PAL", 30, BLUE).next_to(core, DOWN, buff=0.22)
        with self.say("c4.gal.1", gap=1.2) as c:
            gla.generate_target()
            gla.target.scale(0.63).move_to(LEFT * 4.05 + DOWN * 1.05)
            self.play(MoveToTarget(gla), *during(disappear(tag), 0, 0.4),
                      *during(appear(cap, shift=None), 0.5, 1),  # early: p. 157's line, shown as it's paraphrased
                      run_time=min(2.0, c.until("names")))
            c.wait_until("names")
            self.play(*appear(c1, c2, lag=0.5), run_time=1.2)  # early: both names shown, then walked
            c.wait_until("gla")
            self.play(c1.box.animate.set_stroke(YELLOW, 4), FlashAround(c1, color=YELLOW, time_width=1.5),
                      run_time=1.2)
            c.wait_until("galname")
            self.play(c1.box.animate.set_stroke(DIM, 2.5), c2.box.animate.set_stroke(YELLOW, 4),
                      FlashAround(c2, color=YELLOW, time_width=1.5), run_time=1.0)
            arcs = []
            for word, ang in (("logic", -0.5), ("array", 0.5)):
                a = select(c1.text, word)[0]
                b = select(c2.text, word)[0]
                arcs.append(CurvedArrow(a.get_bottom() + DOWN * 0.08, b.get_top() + UP * 0.08, angle=ang)
                            .set_color(YELLOW).set_stroke(width=3))
            words = [select(m.text, wd)[0] for m in (c1, c2) for wd in ("logic", "array")]
            self.play(*[Create(a) for a in arcs], *recolor([g for w in words for g in w], YELLOW),
                      run_time=min(1.4, c.until("fixed")))
            c.wait_until("fixed")
            self.play(*appear(core, shift=None), run_time=1.2)
            c.wait_until(own_word=ptag)
            self.play(*appear(ptag), *[VShowPassingFlash(f.copy().set_stroke(YELLOW, 8), time_width=0.7) for f in pal.fixed],
                      FlashAround(pal.or_panel, color=YELLOW, time_width=1.5), run_time=1.4)
        self.c1_items = [gla, cap, c1, c2, *arcs, core, ptag]

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        self.G = G = S6.gal()
        later = [*G.out_labels, G.clk, G.clk_label]
        G.remove(*later)
        # the flip-flops sit DIM from {figure} (so the feedback wires never end in mid-air), light at {ffs}
        ff_parts = [m for ff in G.ffs for m in ff.submobjects if m is not ff.clk_w]
        for m in ff_parts:
            m.save_state()
            dim_part(m)
        clk_w = G.ffs[1].clk_w
        clk_w.save_state()
        clk_w.set_stroke(opacity=0)
        with self.say("c4.gal.2") as c:
            sweep_clear(self, *appear(G, shift=None), run_time=min(2.0, c.until("rails")))
            c.wait_until("rails")
            self.play(*[VShowPassingFlash(r.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for r in G.bank.rails], *flash(G.in_labels, run_time=1.4), run_time=1.4)
            c.wait_until("state")
            self.play(*[VShowPassingFlash(f.copy().set_stroke(YELLOW, 8), time_width=0.5)
                        for f in G.feed + G.green], run_time=1.6)
            c.wait_until("groups")
            self.tinted = []
            anims = []
            for key, col, k in (("top", TEAL, 0), ("bot", PINK, 1)):
                for gi in G.groups[key]:
                    anims += [G.ands.gates[gi].animate.set_stroke(col, 6),
                              G.fixed[gi].animate.set_stroke(col, 5)]
                    self.tinted += [(G.ands.gates[gi], GATE_STROKE), (G.fixed[gi], FIXED_STROKE)]
                anims.append(G.ors[k].animate.set_stroke(col, 6))
                self.tinted.append((G.ors[k], GATE_STROKE))
            self.play(*anims, run_time=1.5)
            c.wait_until("gaps")
            pulse = [m.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.25)
                     for m in G.gaps]
            self.play(*pulse, run_time=1.6)
            c.wait_until("more outputs")
            self.play(G.dashed_or[0].animate(rate_func=there_and_back).set_color(YELLOW).scale(1.15),
                      run_time=1.2)
            c.wait_until("ffs")
            self.play(*[Restore(m) for m in ff_parts], *flash([ff.box for ff in G.ffs], color=GREEN),
                      run_time=1.2)
            c.wait_until("eff zero")
            self.play(*appear(G.out_labels[0]), run_time=0.8)
            c.wait_until("eff N")
            self.play(*appear(G.out_labels[1]), run_time=0.8)
            c.wait_until("clk")
            self.play(*[Create(m) for m in G.clk[:2]], FadeIn(G.clk[2]), Restore(clk_w), *appear(G.clk_label, shift=None),
                      run_time=min(1.5, c.until(None)))
        settle(self, G, add=later)

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        G = self.G
        t_top = MathTex(TERM, font_size=40, color=YELLOW).move_to(G.ands.gates[3]).shift(DOWN * 0.02)
        t_bot = MathTex(TERM, font_size=40, color=RED).move_to(G.ands.gates[1]).shift(DOWN * 0.02)
        for t in (t_top, t_bot):
            t.set_z_index(3)
        twice = S3.made_twice_tag().move_to(np.array([-2.5, -1.27, 0]))
        q = T("?", 48, YELLOW).move_to(np.array([-0.82, -1.45, 0]))
        simp = T("simpler", 30, GREEN).move_to(np.array([1.0, -1.32, 0]))
        fast = T("faster", 30, GREEN).move_to(np.array([1.0, -1.78, 0]))
        with self.say("c4.gal.3") as c:
            restore = [m.animate.set_stroke(FG if s == FIXED_STROKE else BLUE, s) for m, s in self.tinted]
            self.play(*restore, *during(appear(t_top), 0.4, 1), run_time=1.4)
            c.wait_until("Each product term")
            self.play(VShowPassingFlash(G.fixed[3].copy().set_stroke(YELLOW, 8), time_width=0.6),
                      FlashAround(G.ors[0], color=YELLOW), run_time=1.4)
            c.wait_until("same")
            self.play(*appear(t_bot), run_time=1.2)
            c.wait_until("own copy")
            self.play(*appear(twice), run_time=1.0)
            self.play(*flash([t_top, t_bot], run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("gain")
            self.play(*[VShowPassingFlash(f.copy().set_stroke(GREEN, 8), time_width=0.6) for f in G.fixed],
                      run_time=1.6)
            c.wait_until(own_word=simp)
            self.play(*appear(simp, fast, lag=0.5), run_time=1.2)
            c.wait_until("depends")
            self.play(*appear(q), run_time=1.0)
        self.c3_items = [t_top, t_bot, twice, q, simp, fast]

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        G = self.G
        dot = G.ands.dots[3][4]                      # gate 3's dot on the `a` rail, inside the AND plane
        hand = hand_icon()
        hand.shift(dot.get_center() + RIGHT * 0.03 - hand.tip.get_left())
        cross = cross_mark(RED).scale(1.5).move_to(hand[1])
        with self.say("c4.gal.4") as c:
            self.play(*appear(hand, shift=0.8 * LEFT), run_time=1.2)
            self.play(FlashAround(dot, color=YELLOW, time_width=1.5), run_time=0.8)
            c.wait_until("by hand")
            self.play(GrowFromCenter(cross), hand.animate.set_stroke(DIM), run_time=0.8)
            c.wait_until("type")
            G.target = S6.gal_moved(G, W_SIDE)
            for lab in G.target.plane_labels:
                lab.scale(PL_K)
            self.play(*during(disappear(hand, cross, *self.c3_items), 0, 0.4),
                      *during([MoveToTarget(G)], 0.25, 1), run_time=1.6)
            G.where = W_SIDE
            y = (G.green[1].get_y() + G.green[2].get_y()) / 2
            row = S6.compiler_row(EQS, size=32)
            row.shift(np.array([-6.75 - row.get_left()[0], y - row.box.get_y(), 0]))
            arrow2 = Arrow(row.comp.get_right(), np.array([G.panels[0].get_left()[0] + 0.32, y, 0]),
                           buff=0.1, stroke_width=4).set_color(FG)
            self.play(Create(row.box), *appear(*row.eqs, lag=0.5), run_time=1.6)
            c.wait_until("compiler")
            self.play(GrowArrow(row.arrow1), *appear(row.comp, shift=None), run_time=1.2)
            c.wait_until("works out")
            self.play(GrowArrow(arrow2), run_time=0.8)
            c.wait_until("which connections")
            kept = [G.ands.dots[g][i] for g, ii in KEEP.items() for i in ii]
            self.play(*[blink(d, d in kept) for d in G.dots], run_time=min(2.4, c.until("programmed")))
            c.wait_until("programmed")
            self.play(*[d.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.8) for d in kept],
                      run_time=min(1.2, c.until(None)))
        # back to the large GAL, every dot lit: s6's opening shot
        G.target = S6.gal_moved(G, S6.LARGE)
        for lab in G.target.plane_labels:
            lab.scale(1 / PL_K)
        for d in G.target.dots:
            d.set_opacity(1)
        self.play(*disappear(row.box, *row.eqs, row.arrow1, row.comp, arrow2), run_time=0.8)
        self.wait(0.6)                               # the programmed pattern holds a beat
        self.play(MoveToTarget(G), run_time=2.0)     # the removed dots fade back as the GAL grows


GATE_STROKE = 4
PL_K = W_SIDE.lu / S6.LARGE.lu
FIXED_STROKE = 3
