"""Chapter 2, scene 1: hook: L6's synchronous counter, the three design steps, strip the logic -> a chain.
Clips c2.hook.1 – c2.hook.3.

Opens on ch1_s8's end card (rebuilt from its PICS / fit / _p), then the Part 2 title card. Reuses L6's
sync_counter() / led_chain() (ch6_s6_circuit), mod_table() (ch5_s3_statetable) and L8's build_chain()
(ch2_s3_shiftreg), loaded by file path. Ends on handover_shot(): build_chain(fy=-0.5) unscaled
(FFs at x -3.6, -0.2, 3.2, y -0.5) plus a YELLOW "?" (T 120) at (-0.2, 2.15); s2 opens on it.
"""
# style: 2
# handover: next
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


def _load(lecture, stem):
    path = Path(__file__).resolve().parents[2] / lecture / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_{lecture[:3]}_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L6C = _load("l06-flip-flops-counters", "ch6_s6_circuit")
L6T = _load("l06-flip-flops-counters", "ch5_s3_statetable")
L8 = _load("l08-timing-metastability", "ch2_s3_shiftreg")
S8 = load_scene("ch1_s8_faults")


def _p(x, y):
    return np.array([x, y, 0.0])


CHAIN_FY = -0.5
Q_AT = _p(-0.2, 2.15)


def end_card():
    """ch1_s8's last frame, exactly as its end_card() draws it."""
    xs = np.linspace(-5.6, 5.6, 7)
    pics = [S8.fit(S8.PICS[k](), 1.6, 1.0).move_to(S8._p(xs[k], 2.75)) for k in range(7)]
    nxt = T("Next: shift registers", 48, t2c={"Next:": YELLOW}).move_to(S8._p(0, -2.55))
    return pics, nxt


def handover_shot():
    """The chain (L8 build_chain(fy=-0.5), as built there) and the YELLOW question mark over it."""
    C = L8.build_chain(fy=CHAIN_FY)
    q = T("?", 120, YELLOW).move_to(Q_AT)
    g = VGroup(*C.all, q)
    g.C, g.q = C, q
    return g


# ---- the 0-to-4 state table (L6 mod_table, titles dropped, scaled into the right half) ----------
TAB_S = 0.8
TAB_TOP = _p(2.65, 1.7)     # top-centre of the trimmed table


def counter_table():
    g = L6T.mod_table()
    g.skel.remove(g.titles)
    top = L6T.MT_HEAD_Y + 0.4
    for ln in g.lines[:2]:
        x = ln.get_start()[0]
        ln.put_start_and_end_on(_p(x, top), _p(x, L6T.MT_BOT))
    # row 4 goes back to 000 (a 0-to-4 counter)
    for grp, gx in ((g.nxt, L6T.MT_GX[1]), (g.inp, L6T.MT_GX[2])):
        grp.submobjects[4] = VGroup(*[MathTex("0", font_size=L6T.MT_CELL).move_to(
            _p(gx + (j - 1) * L6T.MT_DX, L6T.mt_row_y(4))) for j in range(3)])
    xs = []
    for i in range(5, 8):
        row = VGroup()
        for grp in (g.nxt, g.inp):
            for cell in grp[i]:
                row.add(MathTex("X", font_size=L6T.MT_CELL, color=YELLOW).move_to(cell))
        xs.append(row)
    body = VGroup(g.skel, g.dec, g.cur, g.nxt, g.inp, *xs)
    body.scale(TAB_S)
    body.shift(TAB_TOP - _p(body.get_center()[0], g.lines[0].get_start()[1]))
    g.xs = xs
    return g


class ShiftHook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.hook.1
    def clip1(self):
        pics, nxt = end_card()
        self.add(*pics, nxt)
        card = title_card("Part 2 · Shift registers and serial links")
        if card.title.width > 12.6:
            card.title.scale_to_fit_width(12.6)
        with self.say("c2.hook.1") as c:
            self.wait(0.7)   # ch1's end card holds a moment: the cut reads as a continuation
            self.play(*during(disappear(*pics, nxt), 0, 0.45),  # early: title card
                      *during(appear(card.title, card.rule, card.course, card.part, lag=0.2), 0.5, 1),  # early: title card
                      run_time=1.6)
            c.wait_until("counter")

            # {counter}: L6's synchronous counter, LEDs and readout
            S = L6C.sync_counter()
            self.S = S
            self.chains = [L6C.led_chain(i) for i in range(3)]
            for r in S.risers:
                r.set_stroke(opacity=L6C.LOW)
            self.r_lab = MathTex(r"Q_2\,Q_1\,Q_0", font_size=40, color=GREEN)
            self.r_eq1 = MathTex("=", font_size=40)
            self.r_bits = Mono("000", 44, GREEN)
            self.r_eq2 = MathTex("=", font_size=40)
            self.r_dec = T("0", 48, GOLD)
            VGroup(self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec).arrange(RIGHT, buff=0.25).move_to(
                _p(0.3, 3.35))
            parts = [*S.all, *[m for ch in self.chains for m in ch]]
            readout = [self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec]
            sweep_clear(self, *[FadeIn(m) for m in parts],  # early: the counter's block label, a drawing part
                        *during(appear(*readout, shift=None, lag=0.1), 0.6, 1.0), run_time=1.8)
            c.wait_until("together")

            # {together}: one pulse along CLK; the three triangles flash at once
            bus_p, clk_p = S.clk_paths()
            self.play(*during([VShowPassingFlash(p, time_width=0.6) for p in bus_p], 0, 0.55),
                      *during([VShowPassingFlash(p, time_width=0.8) for p in clk_p], 0.5, 0.8),
                      *during([FlashAround(f.tri, color=YELLOW, time_width=1.5, buff=0.08) for f in S.ffs], 0.55, 1.0),
                      run_time=1.8)
            # counts 0 .. 7, then wraps
            rt = max(0.3, (c.until(floor=0) - 0.5) / 8)
            for n in [*range(1, 8), 0]:
                self.step_to(n, run_time=rt)

    def step_to(self, n, run_time):
        """As in L6: bits, decimal, LEDs and Q risers switch in one frame; a pulse then runs along CLK."""
        S = self.S
        b = [(n >> i) & 1 for i in range(3)]
        nb = Mono(f"{n:03b}", 44, GREEN).move_to(self.r_bits)
        nd = T(str(n), 48, GOLD).move_to(self.r_dec)
        self.remove(self.r_bits, self.r_dec)
        self.add(nb, nd)
        for ch, v in zip(self.chains, b):
            ch.led.on = bool(v)
            if v:
                ch.led.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
            else:
                ch.led.set_stroke(DIM, 3).set_fill(BG, 0)
        for r, v in zip(S.risers, b):
            r.set_stroke(opacity=1 if v else L6C.LOW)
        self.r_bits, self.r_dec = nb, nd
        bus_p, _ = S.clk_paths()
        self.play(VShowPassingFlash(bus_p[0], time_width=0.8), run_time=run_time)

    # ------------------------------------------------------------------ c2.hook.2
    def clip2(self):
        S = self.S
        self.cmobs = [*S.all, *[m for ch in self.chains for m in ch],
                      self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec]
        for m in self.cmobs:
            m.save_state()
        whole = VGroup(*[m.copy() for m in self.cmobs])
        sc, to = 0.43, _p(-3.9, 0.3)
        pivot = whole.get_center()
        for m in self.cmobs:
            m.generate_target()
            m.target.scale(sc, about_point=pivot).shift(to - pivot)
        # the thumbnail keeps only drawing: its labels would be unreadably small
        self.gone_text = [*S.q_labels, *S.xor_labels, S.block_l, *S.block_labels,
                          self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec]
        for m in [*self.gone_text, *S.names, S.clk_l]:
            m.target.set_opacity(0)
        for f in S.ffs:
            for idx, sub in enumerate(f.submobjects):
                if any(sub is x for x in (f.d_l, f.q_l, f.qb_l)):
                    f.target[idx].set_opacity(0)

        rows = [("1 ·", "state transition table"), ("2 ·", "FF excitation (easy for D-types)"),
                ("3 ·", "combinational logic")]
        self.steps = []
        for k, (a, b) in enumerate(rows):
            num = T(a, 32, DIM)
            body = T(b, 32, DIM)
            VGroup(num, body).arrange(RIGHT, buff=0.18)
            num.shift(_p(-0.8, 3.3 - 0.58 * k) - num.get_left())
            body.align_to(num, DOWN).shift(_p(num.get_right()[0] + 0.18 - body.get_left()[0], 0))
            # common baseline: old-style 2/3 have other bboxes than 1, so pin the body's first
            # letter to the row baseline and each "·" at the same height above it
            if k == 0:
                base0 = num[0].get_bottom()[1]
                dot_h = num[1].get_center()[1] - base0
            base = base0 - 0.58 * k
            body.shift((base - body[0].get_bottom()[1]) * UP)
            num.shift((base + dot_h - num[1].get_center()[1]) * UP)
            self.steps.append((num, body))

        with self.say("c2.hook.2") as c:
            # {steps}: the counter shrinks to the left
            self.play(*[MoveToTarget(m) for m in self.cmobs], run_time=1.6)
            c.wait_until("three steps")
            flat = [m for pair in self.steps for m in pair]
            self.play(*appear(*flat, shift=None, lag=0.15), run_time=1.2)  # early: the list shown whole, then walked
            prev = None
            for (num, body), cue in zip(self.steps, ("state transition", "excitation", "and the logic")):
                c.wait_until(cue)
                off = [] if prev is None else [prev[0].animate.set_color(DIM), prev[1].animate.set_color(DIM)]
                self.play(num.animate.set_color(YELLOW), body.animate.set_color(FG), *off, run_time=0.8)
                prev = (num, body)

            # {example}: the 0-to-4 table under the steps
            c.wait_until("example")
            tab = counter_table()
            self.tab = tab
            first = [tab.skel]
            for i in range(5):
                first += [tab.dec[i], tab.cur[i], tab.nxt[i], tab.inp[i]]
            self.play(FadeIn(tab.skel), *[a for k, m in enumerate(first[1:])
                                           for a in during([FadeIn(m)], 0.2 + 0.1 * (k // 4), 0.6 + 0.1 * (k // 4))],
                      run_time=min(1.8, c.until("never", floor=1.0)))

            # {unused}: rows 5, 6, 7 never visited: DIM, their outputs "X"
            c.wait_until("never")
            for i in range(5, 8):
                tab.dec[i].set_opacity(0.4)
                tab.cur[i].set_opacity(0.4)
            self.play(*appear(*[tab.dec[i] for i in range(5, 8)], *[tab.cur[i] for i in range(5, 8)],
                              shift=None, lag=0.05), run_time=1.0)
            self.tag = T("don't care", 34, YELLOW).move_to(_p(tab.lines[1].get_start()[0], -3.35))
            c.wait_until(own_word=self.tag)
            self.play(*appear(*tab.xs, lag=0.2), *during(appear(self.tag), 0.4, 1.0), run_time=1.4)

            # {simpler}: the logic block in the small counter shrinks a little
            c.wait_until("simpler")
            blk = [S.block, S.block_l, *S.block_stubs, *S.block_labels]
            ctr = S.block.get_center()
            self.play(*[m.animate.scale(0.75, about_point=ctr) for m in blk],
                      FlashAround(S.block, color=YELLOW, time_width=1.5, buff=0.1),
                      run_time=min(1.5, c.until(floor=0.8)))

    # ------------------------------------------------------------------ c2.hook.3
    def clip3(self):
        S = self.S
        tab = self.tab
        shot = handover_shot()
        C = shot.C
        with self.say("c2.hook.3") as c:
            # {strip}: table and steps clear, counter back to full size, its gates and readout fade
            out = [m for pair in self.steps for m in pair] + [tab.skel, *tab.dec, *tab.cur, *tab.nxt[:5], *tab.inp[:5],
                                                              *tab.xs, self.tag]
            self.remove(*self.gone_text)
            back = [m for m in self.cmobs if not any(m is g for g in self.gone_text)]
            self.play(*during(disappear(*out), 0, 0.35),
                      *during([Restore(m) for m in back], 0.4, 1.0), run_time=1.4)
            gates = [*S.risers, S.loop, S.xor, *S.xor_stubs, S.block, S.block_out,
                     *S.block_stubs, *[m for ch in self.chains for m in ch],
                     *[m for f in S.ffs for m in (f.qb_w, f.qb_l)], S.ffs[0].d_w]
            self.play(*disappear(*gates), run_time=min(0.9, c.until("chain", floor=0.5)))
            c.wait_until("chain")

            # {chain}: the flip-flops line up into L8's chain
            anims = []
            for a, b in zip(S.ffs, C.ffs):
                pairs = [(a.box, b.box), (a.tri, b.tri), (a.q_w, b.q_w), (a.d_l, b.d_l), (a.q_l, b.q_l),
                         (a.clk_w, b.clk_w)]
                if a is not S.ffs[0]:
                    pairs.append((a.d_w, b.d_w))
                anims += [ReplacementTransform(x, y) for x, y in pairs]
            anims += [ReplacementTransform(x, y) for x, y in zip(S.names, C.names)]
            anims += [ReplacementTransform(S.bus, C.bus), ReplacementTransform(S.clk_l, C.clk_l)]
            anims += [ReplacementTransform(x, y) for x, y in zip(S.jdots, C.jdots)]
            self.play(*anims, run_time=2.0)
            self.remove(*self.mobjects)
            din_w = C.ffs[0].d_w
            din_w.set_stroke(opacity=0)
            self.add(*C.ffs, *C.names, C.bus, *C.jdots, *C.clk_ws, C.clk_l)

            # each output straight into the next one's input
            c.wait_until("wire each")
            self.play(*[Create(m) for m in (*C.links, C.tail)],
                      *during([Create(r) for r in C.risers], 0.4, 1.0),
                      *during([FadeIn(d) for d in C.dots], 0.5, 1.0), run_time=1.5)
            self.play(*appear(*C.qls, shift=None, lag=0.15), run_time=1.0)
            # a new D_in wire into FF0
            c.wait_until("input")
            new_w = din_w.copy().set_stroke(BLUE, 5, opacity=1)
            self.play(Create(new_w), *during(appear(C.din, shift=None), 0.4, 1.0), run_time=1.0)
            self.remove(new_w)
            din_w.set_stroke(BLUE, 5, opacity=1)

            # {question}
            c.wait_until("question")
            self.play(*appear(shot.q), run_time=1.0)
            # hold on handover_shot() through the clip's end
        self.remove(*self.mobjects)
        self.add(*C.all, shot.q)
