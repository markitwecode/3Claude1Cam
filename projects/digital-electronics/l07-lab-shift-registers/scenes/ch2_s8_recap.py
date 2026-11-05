"""Chapter 2, scene 8: a flip-flop's three numbers (preview), the recap, next lecture.
Clips c2.recap.1 – c2.recap.3.

Opens on ch2_s7_timing.handover_shot(): the compressed clock wave becomes the CLK row of L8 ch1_s3's
WindowDiagram (loaded by path), labelled as slide p. 104 writes them: t_su Set-up time, t_h Hold
time, t_pc CLK-to-Q Propagation delay. Recap: six slots framed as ch1_s8's slot_frame(), each a
small copy built from its scene's own helpers (s2 L8 build_chain, s3 rows, s4 build(), s5 chain +
PRE/CLR + queue, s6 SerialLink.build(), s7 f_c + sensor_icon()), captions T 28. End card as
ch1_s8's: the six pictures in a row on top, s7's wave compressing against a "?", the question and
"Next: Lecture 8". Ends on an empty frame.
"""
# style: 2
import importlib.util
import sys
import types
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


def _load_l8():
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch1_s3_ffnumbers.py"
    spec = importlib.util.spec_from_file_location("_l08_ch1_s3_ffnumbers", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8W = _load_l8()
S2 = load_scene("ch2_s2_chain")
S3 = load_scene("ch2_s3_trace")
S4 = load_scene("ch2_s4_demo")
S5 = load_scene("ch2_s5_load")
S6 = load_scene("ch2_s6_link")
S7 = load_scene("ch2_s7_timing")
L8 = S2.L8          # L8 ch2_s3: build_chain, pin, digit_pos


def _p(x, y):
    return np.array([x, y, 0.0])


def dpos(ff):
    """Where a bit sits in a recap flip-flop: the box centre (its D/Q labels are gone), clear of the clock triangle."""
    return ff.box.get_center()


def fit(g, w, h):
    g.scale(min(w / g.width, h / g.height))
    return g


# ── recap pictures (centred on ORIGIN; final=False gives the state before the tile's own move) ──
PW, PH = 3.7, 2.05       # picture box inside a 4.2 x 2.5 slot


def pic_chain(final=True, thumb=False):
    C = L8.build_chain()
    parts = [*C.ffs, *C.links, C.tail, *C.risers, *C.dots, C.bus, *C.jdots, *C.clk_ws]
    for f in C.ffs:
        f.remove(f.d_l, f.q_l)
    g = VGroup(*parts).move_to(ORIGIN)
    fit(g, PW, PH)
    g.ffs, g.bus = C.ffs, C.bus
    if thumb:
        return g
    g.dig = T("1", 38, GOLD, weight=BOLD).move_to(dpos(C.ffs[1 if final else 0])).set_z_index(20)
    g.add(g.dig)
    return g


def pic_rows(final=True, labels=True):
    clk = S3.clk_wave()
    rows = []
    for q in range(3):
        segs = [S3.seg(q, k) for k in range(9) if S3.QV[q][k] is not None]
        row = VGroup(S3.ublock(2 + q, S3.X0, S3.XE[q]), *segs)
        row.shift(UP * S3.PITCH)
        rows.append(row)
    waves = VGroup(clk, *rows)
    waves.stretch_to_fit_width(3.1 if labels else 1.9).stretch_to_fit_height(1.95 if labels else 1.0)
    g = VGroup(waves)
    if labels:
        texs = [(r"\mathrm{CLK}", YELLOW, clk)] + [(f"Q_{q}", GREEN, r) for q, r in enumerate(rows)]
        labs = [MathTex(t, font_size=30, color=col).next_to(_p(waves.get_left()[0], m[-1].get_center()[1]),
                                                           LEFT, buff=0.12) for t, col, m in texs]
        g.add(*labs)
        rows = [VGroup(lab, r) for lab, r in zip(labs[1:], rows)]
        g.head = VGroup(clk, labs[0])
    g.move_to(ORIGIN)
    g.rows = rows
    return g


def pic_leds(final=True, thumb=False):
    R = S4.build()
    lit = 2 if final else 0
    for i, d in enumerate(R.leds):
        S4.led_state(d, 1 if i == lit else 0)
    parts = [*R.ffs, *R.links, R.tail]
    for f in R.ffs:
        f.remove(f.d_l, f.q_l)
    for i in range(4):
        parts += [R.bwires[i], R.taps[i], R.res[i], R.leds[i].glow, R.leds[i], R.gnds[i]]
    parts += [R.sw_in, R.in_w, R.sw_clk, R.bus, *R.stubs, *R.jdots]
    g = VGroup(*parts).move_to(ORIGIN)
    fit(g, PW, PH)
    g.leds = R.leds
    return g


def pic_load(final=True, thumb=False):
    C = L8.build_chain(fy=S5.FY)
    pins = []
    for f in C.ffs:
        f.remove(f.d_l, f.q_l)
        for kind in ("PRE", "CLR"):
            w, _ = L8.pin(f, kind)
            pins.append(w.set_stroke(RED, 7))
    parts = [*C.ffs, *C.links, C.tail, *C.risers, *C.dots, C.bus, *C.jdots, *C.clk_ws, *pins]
    g = VGroup(*parts).move_to(ORIGIN)
    fit(g, PW - 1.45, PH)
    # s5's queue, sized for three digits in this picture's scale: the bits leave Q_2 into it
    q2 = dpos(C.ffs[2])
    qbox = DashedVMobject(Rectangle(width=1.25, height=0.55), num_dashes=26).set_stroke(DIM, 3)
    qbox.move_to(_p(g.get_right()[0] + 0.2 + 0.625, q2[1]))
    g.add(qbox)
    g.qslots = [Dot(qbox.get_center() + (i - 1) * 0.38 * RIGHT, radius=0.01).set_opacity(0) for i in range(3)]
    g.add(*g.qslots)
    g.move_to(ORIGIN)
    g.ffs = C.ffs
    if not thumb:
        g.digs = [T(s, 36, GOLD, weight=BOLD).move_to(dpos(f)).set_z_index(20) for s, f in zip("110", C.ffs)]
        g.add(*g.digs)
    return g


def pic_link(final=True, thumb=False):
    L = types.SimpleNamespace()
    S6.SerialLink.build(L)
    TX, RX = L.TX, L.RX
    parts = [L.boxL, L.boxR, *TX.ffs, *TX.links, *L.pin_ws, *L.d_in, *L.d_out,
             *RX.ffs, *RX.links, RX.tail, *RX.dots, *RX.risers, *L.q_in, *L.q_out,
             L.serial, L.bus, *L.stubs, *L.jdots]
    g = VGroup(*parts).move_to(ORIGIN)
    fit(g, PW, PH - 0.45)
    yb = g.get_bottom()[1] - 0.26
    g.digs = [T(s, 36, GOLD, weight=BOLD).move_to(_p(f.box.get_x(), yb)) for s, f in zip("110", RX.ffs)]
    if final and not thumb:
        g.add(*g.digs)
    elif not thumb:
        g.loose = g.digs
    return g


def pic_clock(final=True, thumb=False):
    fc = MathTex("f_c", "=", "1/T_c", font_size=30 if thumb else 52)
    fc[0].set_color(YELLOW)
    sensor = S7.sensor_icon()
    plus = sensor[-1][2]
    sensor[-1].remove(plus)
    sensor.scale(0.3 if thumb else 0.75)
    g = VGroup(fc, sensor).arrange(RIGHT, buff=0.25 if thumb else 0.5)
    if not thumb:
        fit(g, PW, PH)
        g.add(T("+", 28, GOLD).move_to(sensor[-1][0]))
    return g


PICS = [pic_chain, pic_rows, pic_leds, pic_load, pic_link, pic_clock]
CAPS = [("one place per edge", "one place"),          # one line each, T 28, on its own words
        ("one clock period later", "period later"),
        ("serial in, parallel out", "serial in"),
        ("parallel in, serial out", "parallel in"),
        ("one wire, faster bits", "one data wire"),
        ("more work, more energy", "more work")]
SLOT_X = [-4.45, 0.0, 4.45]
SLOT_Y = [1.95, -1.35]


def slot_frame(k):
    return RoundedRectangle(corner_radius=0.12, width=4.2, height=2.5).move_to(_p(SLOT_X[k % 3], SLOT_Y[k // 3]))


SLOT_OP = 0.55          # earlier slots dim this far as each new one arrives


class Recap(NarratedScene):
    def construct(self):
        shot = S7.handover_shot()
        self.shot = shot
        self.add(shot.wave.wave, shot.wave.ups, shot.q, shot.ff, shot.tag)
        self.clip1()
        self.clip2()
        self.clip3()
        self.end_card()

    # ── c1: the window diagram ──
    def clip1(self):
        sh = self.shot
        g = self.g = L8W.WindowDiagram(origin=_p(0, 0.3), k=1.0, fs=1.0, words=False)
        g.sym_hold = MathTex(r"t_{\mathrm{h}}", font_size=44, color=GOLD).next_to(g.hold.arrow, RIGHT, buff=0.15)
        w_su = T("Set-up time", 32, GOLD).next_to(g.sym_su, LEFT, buff=0.25)
        w_h = T("Hold time", 32, GOLD).next_to(g.sym_hold, RIGHT, buff=0.25)
        w_pc = VGroup(T("CLK-to-Q", 32, PINK), T("Propagation delay", 32, PINK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(g.sym_pc, RIGHT, buff=0.25)
        with self.say("c2.recap.1") as c:
            # {window}: the compressed wave relaxes into the CLK row; the rows are named
            self.play(*during(disappear(sh.tag, sh.q, sh.ff) + [FadeOut(sh.wave.ups)], 0, 0.45),
                      *during([ReplacementTransform(sh.wave.wave, g.clk)], 0.25, 0.9),
                      *during(appear(g.lab_clk, g.lab_d, g.lab_q, lag=0.2), 0.5, 1.0),  # early: the rows are named as a set
                      run_time=2.0)
            self.play(GrowFromCenter(g.guide), FadeIn(g.up, shift=0.15 * UP),
                      Create(g.d, rate_func=linear), run_time=min(1.6, c.until("setup", floor=0.8)))
            # {setup}
            c.wait_until("setup")
            self.play(FadeIn(g.su.guides), GrowFromCenter(g.su.arrow), run_time=1.0)
            c.wait_until("set-up time")
            self.play(*appear(g.sym_su, w_su, lag=0.2), run_time=1.0)
            # {hold}
            c.wait_until("hold")
            self.play(FadeIn(g.hold.guides), GrowFromCenter(g.hold.arrow),
                      *during(appear(g.sym_hold, w_h, lag=0.2), 0.4, 1.0), run_time=1.5)
            # {q}
            c.wait_until("q")
            self.play(Create(g.q, rate_func=linear), run_time=1.5)
            self.play(FadeIn(g.pc.guides), GrowFromCenter(g.pc.arrow), run_time=0.8)
            c.wait_until("delay")
            self.play(*appear(g.sym_pc, w_pc, lag=0.2), run_time=1.0)
            # {bad}: the window shades, D changes inside it, Q is unknown
            c.wait_until("bad")
            self.play(FadeIn(g.band), FlashAround(g.band, color=GOLD, time_width=1.5), run_time=1.2)
            chg = g.d_change(0.45)
            c.wait_until("changes")
            self.play(FadeIn(chg), FlashAround(chg, color=RED, time_width=1.5), run_time=1.0)
            unk = g.q_unknown().next_to(_p(3.1, g.P(0, -2 + g.AMP)[1]), UP, buff=0.15)
            c.wait_until("unreliable")
            self.play(*appear(unk, shift=None), run_time=1.0)
            # {names}
            tag = T("Lecture 8", 34, YELLOW).move_to(_p(5.4, 3.35))
            c.wait_until("next lecture")
            self.play(*appear(tag), run_time=1.0)

    # ── c2: recap, slots 1-4 ──
    def slot(self, c, k, cue):
        fr = self.frames[k]
        pic = PICS[k](final=False)
        off = fr.get_center() - VGroup(pic, *getattr(pic, "loose", [])).get_center()
        pic.shift(off)
        for m in getattr(pic, "loose", []):
            m.shift(off)
        cap = T(CAPS[k][0], 28).next_to(fr, DOWN, buff=0.14)
        c.wait_until(cue)
        prev = [m for m in self.tiles]
        if k == 1:
            head = pic.head
            self.play(FadeIn(head, scale=0.9), *set_alpha(prev, SLOT_OP), run_time=0.8)  # early: a small copy of an earlier picture
        else:
            self.play(FadeIn(pic, scale=0.9), *set_alpha(prev, SLOT_OP), run_time=0.8)  # early: a small copy of an earlier picture
        return pic, cap

    def caption(self, c, cap, k):
        c.wait_until(CAPS[k][1])
        self.play(*appear(cap, shift=None), run_time=0.8)
        self.tiles.append(cap)

    def clip2(self):
        with self.say("c2.recap.2") as c:
            self.frames = [slot_frame(k).set_stroke(DIM, 2) for k in range(6)]
            self.tiles = []
            self.wait(max(0, c.until("r1") - 1.25))
            sweep_clear(self, *[FadeIn(f) for f in self.frames], run_time=min(1.2, c.until("r1", floor=0.8)))

            # {r1}: the chain, a 1 hops one box per edge
            pic, cap = self.slot(c, 0, "r1")
            c.wait_until("every bit")
            self.play(pic.dig.animate.move_to(dpos(pic.ffs[1])),
                      VShowPassingFlash(pic.bus.copy().set_stroke(YELLOW, 7), time_width=0.6), run_time=1.3)
            self.caption(c, cap, 0)
            self.tiles.insert(0, pic)

            # {r2}: the same waveform, one period later each row
            pic, cap = self.slot(c, 1, "r2")
            c.wait_until("repeats")
            self.play(*appear(*pic.rows, shift=None, lag=0.5), run_time=1.6)
            self.settle_pic(pic)
            self.caption(c, cap, 1)
            self.tiles.insert(0, pic)

            # {r3}: four LEDs, the lit one walks
            pic, cap = self.slot(c, 2, "r3")
            c.wait_until("one at a time")
            for i in (1, 2):
                self.play(*S4.led_anims(pic.leds[i - 1], 0), *S4.led_anims(pic.leds[i], 1), run_time=0.6)
            self.caption(c, cap, 2)
            self.tiles.insert(0, pic)

            # {r4}: PRE / CLR load 1 1 0, the queue waits at Q_2
            pic, cap = self.slot(c, 3, "r4")
            c.wait_until("whole word")
            self.play(*flash(pic.digs, color=GOLD, time_width=1.5), run_time=1.2)
            # {leave}: the bits leave Q_2 one after another into the queue; zeros come in behind
            c.wait_until("leave")
            zeros = [T("0", 36, DIM, weight=BOLD).move_to(dpos(f)).set_z_index(20) for f in pic.ffs]
            self.play(*during([pic.digs[2].animate.move_to(pic.qslots[2])], 0.0, 0.45),
                      *during([pic.digs[1].animate.move_to(pic.qslots[1])], 0.25, 0.7),
                      *during([pic.digs[0].animate.move_to(pic.qslots[0])], 0.5, 0.95),
                      *during(appear(*zeros, shift=None, lag=0.2), 0.6, 1.0),
                      run_time=min(2.0, c.until("parallel in", floor=1.2)))
            pic.add(*zeros)
            self.settle_pic(pic)
            self.caption(c, cap, 3)
            self.tiles.insert(0, pic)

    def settle_pic(self, pic):
        self.remove(*pic.get_family())
        self.add(pic)

    # ── c3: slots 5-6, next ──
    def clip3(self):
        with self.say("c2.recap.3") as c:
            # {r5}: the link; 1 1 0 arrives in the receiver
            pic, cap = self.slot(c, 4, "r5")
            c.wait_until("serial link")
            self.play(*appear(*pic.digs, shift=0.2 * RIGHT, lag=0.4), run_time=1.4)
            pic.add(*pic.digs)
            self.settle_pic(pic)
            self.caption(c, cap, 4)
            self.tiles.insert(0, pic)

            # {r6}: f_c = 1/T_c beside the sensor node
            pic, cap = self.slot(c, 5, "r6")
            self.caption(c, cap, 5)
            self.tiles.insert(0, pic)

            # {next}: the slots clear to the end card
            c.wait_until("asks")
            pics = [PICS[k](labels=False) if k == 1 else PICS[k](thumb=True) for k in range(6)]
            pics = [(p if k in (1, 5) else fit(p, 1.9, 1.0)).move_to(_p(-5.6 + 2.24 * k, 2.85))
                    for k, p in enumerate(pics)]
            nxt = T("Next: Lecture 8", 40, t2c={"Next:": YELLOW}).move_to(_p(0, -2.6))
            old = [*self.frames, *self.tiles]
            self.play(*during([FadeOut(m) for m in old], 0, 0.45),
                      *during([FadeIn(p) for p in pics] + appear(nxt), 0.5, 1.0), run_time=1.6)  # early: the end card
            p = ValueTracker(0.75)
            wave = always_redraw(lambda: S7.wave_shape(-0.7, 0.8, 8.0, 0.7, p.get_value()))
            qm = T("?", 80, YELLOW).move_to(_p(4.6, 0.8))
            ques = T("What sets the fastest clock speed?", 44).move_to(_p(0, -1.05))
            c.wait_until("what sets")
            self.play(FadeIn(wave), *appear(qm, ques, lag=0.3), run_time=1.2)
            self.p, self.wave = p, wave

    def end_card(self):
        self.play(self.p.animate.set_value(0.3), run_time=2.5, rate_func=linear)
        self.wave.clear_updaters()
        self.wait(5.1)   # the end card holds ~8 s after the last word; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
