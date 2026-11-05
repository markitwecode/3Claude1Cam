"""Chapter 7, scene 2: the circuit, plain physics, and its four laws. Clips c7.circuit.1 – c7.circuit.5.

Opens on ch7_s1_hook's handover_shot() (circuit + "V = ? · I"); the question clears as the
circuit moves to centre. Reusable helpers for the recap / later scenes:
  four_laws(size)          VGroup of the four law rows (scan p. 11), left-aligned, at ORIGIN;
                           .ohm .store .rate .loop are the four MathTex equations.
  raw_to_screen(circ, x, y) a point of s1's raw circuit geometry, on a placed circuit.
  loop_path(circ)          closed polyline round the circuit's wires (for a loop trace).
Ends on an empty frame (s3 fades in its own copy of the laws).
"""
# style: 2
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

_s1 = load_scene("ch7_s1_hook")
circuit, charge_dots, handover_shot_s1, tex = _s1.circuit, _s1.charge_dots, _s1.handover_shot, _s1.tex
_L, _RX, _TOP, _BOT, _CY, _Z0, _Z1, _GAP = (_s1._L, _s1._RX, _s1._TOP, _s1._BOT, _s1._CY,
                                            _s1._Z0, _s1._Z1, _s1._GAP)
_MID = (_L + _RX) / 2

POS1, SCALE1 = np.array([0.6, -0.1, 0.0]), 1.15      # clip 1: big, centred
POS2, SCALE2 = np.array([-3.3, 0.1, 0.0]), 0.85      # from clip 2: left third
COL_X = 3.45                                          # right column centre


# ---------------------------------------------------------------- helpers (reusable)
def four_laws(size=50):
    """The four laws (scan p. 11), one row each, left-aligned, centred at ORIGIN.
    Colours: I GOLD; R, V_R BLUE; C, Q, V_C PINK; V FG."""
    ohm_lbl = T("Ohm's law:", 36)
    ohm = tex("V_R", "(t)", "=", "R", "I", "(t)", size=size)
    ohm[0].set_color(BLUE)
    ohm[3].set_color(BLUE)
    ohm[4].set_color(GOLD)
    row1 = VGroup(ohm_lbl, ohm).arrange(RIGHT, buff=0.3)
    store = tex("Q", "(t)", "=", "C", "V_C", "(t)", size=size)
    for k in (0, 3, 4):
        store[k].set_color(PINK)
    rate = tex("I", "=", r"{dQ \over dt}", size=size)
    rate[0].set_color(GOLD)
    rate[2][1].set_color(PINK)
    loop = tex("V", "=", "V_R", "+", "V_C", size=size)
    loop[2].set_color(BLUE)
    loop[4].set_color(PINK)
    g = VGroup(row1, store, rate, loop).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
    g.move_to(ORIGIN)
    g.ohm, g.store, g.rate, g.loop = ohm, store, rate, loop
    return g


def raw_to_screen(circ, x, y):
    """s1's raw circuit coordinates -> screen, for a circuit that has been scaled/moved."""
    a, b = circ.wires[1].get_start(), circ.wires[1].get_end()
    s = np.linalg.norm(b - a) / (_Z0 - _L)
    return a + s * (np.array([x, y, 0.0]) - np.array([_L, _TOP, 0.0]))


def loop_path(circ, color=YELLOW, width=7):
    pts = [raw_to_screen(circ, x, y) for x, y in
           [(_L, _TOP), (_RX, _TOP), (_RX, _BOT), (_L, _BOT), (_L, _TOP)]]
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


# ---------------------------------------------------------------- streaming charges
_PER = 2 * (_RX - _L) + 2 * (_TOP - _BOT)
_W_TOP, _H = _RX - _L, _TOP - _BOT
# stretches of the loop parameter u (clockwise from the top-left corner) hidden behind parts
_HIDE = [(_Z0 - _L - 0.05, _Z1 - _L + 0.05),                                  # resistor
         (_W_TOP + _TOP - _CY - 0.22, _W_TOP + _TOP - _CY + 0.22),            # capacitor
         (_W_TOP + _H + _RX - _MID - 0.62, _W_TOP + _H + _RX - _MID + 0.62),  # current arrow
         (2 * _W_TOP + _H + _CY - _BOT - 0.55, 2 * _W_TOP + _H + _CY - _BOT + 0.55)]  # source


def _loop_raw(u):
    u %= _PER
    if u < _W_TOP:
        return _L + u, _TOP
    u -= _W_TOP
    if u < _H:
        return _RX, _TOP - u
    u -= _H
    if u < _W_TOP:
        return _RX - u, _BOT
    u -= _W_TOP
    return _L, _BOT + u


def _vis(u):
    u %= _PER
    d = min(min(abs(u - a), abs(u - b)) if not (a <= u <= b) else 0.0 for a, b in _HIDE)
    return float(np.clip(d / 0.18, 0, 1))


def flow_system(circ, n=24, speed=0.5, period=2.4):
    """Dots streaming clockwise round circ. st['mode']: 'stream' -> 'ac' (dots slosh, the
    current arrow shrinks/flips/regrows, the source's ~ wobbles) -> 'off'."""
    dots = VGroup(*[Dot(radius=0.06, color=FG, fill_opacity=0.75) for _ in range(n)])
    w = TAU / period
    st = {"mode": "stream", "u": 0.0, "t": 0.0, "u0": 0.0, "ang": 0.0,
          "arrow0": circ.current.copy(), "sim0": circ.source[1].copy()}
    amp = speed / w
    mid = raw_to_screen(circ, _MID, _BOT)

    def upd(g, dt):
        if st["mode"] == "stream":
            st["u"] += speed * dt
        elif st["mode"] == "ac":
            st["t"] += dt
            ph = w * st["t"]
            st["u"] = st["u0"] + amp * np.sin(ph)
            f = np.cos(ph)
            a = st["arrow0"].copy().scale(max(abs(f), 0.03), scale_tips=True, about_point=mid)
            if f < 0:
                a.rotate(PI, about_point=mid)
            a.set_opacity(min(1.0, abs(f) / 0.15))
            circ.current.become(a)
            st["ang"] = 0.4 * np.sin(ph)
            circ.source[1].become(st["sim0"].copy().rotate(st["ang"]))
        for k, d in enumerate(g):
            u = st["u"] + k * _PER / n
            d.move_to(raw_to_screen(circ, *_loop_raw(u)))
            d.set_opacity(0.75 * _vis(u))
        return g

    dots.add_updater(upd)
    upd(dots, 0)
    return dots, st


def _arrive(dot, a, b):
    def f(m, al):
        m.move_to(a + (b - a) * al)
        m.set_opacity(float(np.clip(min(4 * al, 4 * (1 - al)), 0, 1)))
    return UpdateFromAlphaFunc(dot, f)


class Circuit(NarratedScene):
    def construct(self):
        hs = handover_shot_s1()
        circ, q, qbox, qtag = hs
        self.add(circ, q, qbox, qtag)

        # ============================================================ clip 1
        with self.say("c7.circuit.1") as c:
            self.play(*during(disappear(q, qbox, qtag), 0, 0.45),
                      *during([circ.animate.scale(SCALE1 / 1.1).move_to(POS1)], 0.3, 1.0),
                      run_time=2.0)

            c.wait_until("source")
            vt = tex("V(t)", size=40).move_to(circ.V, aligned_edge=RIGHT)
            v_words = T("applied voltage", 30).next_to(vt, UP, buff=0.18).align_to(vt, RIGHT)
            self.play(FlashAround(circ.source, run_time=1.5, time_width=1.5), *swap(circ.V, VGroup(v_words, vt)), run_time=1.5)  # early: the lecturer's label for the source

            c.wait_until("resistor")
            r_words = T("resistance", 30, BLUE).next_to(circ.R, LEFT, buff=0.2)
            self.play(FlashAround(circ.resistor, color=BLUE, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until(own_word=r_words)
            self.play(*appear(r_words), run_time=1.0)

            c.wait_until("capacitor")
            c_words = T("capacitance", 30, PINK).next_to(circ.C, UP, buff=0.15, aligned_edge=LEFT)
            self.play(FlashAround(circ.capacitor, color=PINK, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until(own_word=c_words)
            self.play(*appear(c_words), run_time=1.0)

            c.wait_until("current")
            it = tex("I(t)", size=40, color=GOLD).move_to(circ.I)
            i_words = T("current", 30, GOLD).next_to(it, LEFT, buff=0.2)
            self.play(FlashAround(circ.current, color=GOLD, run_time=1.5, time_width=1.5),
                      *swap(circ.I, VGroup(i_words, it)), run_time=1.5)
        settle(self, circ, add=[vt, it], drop=[circ.V, circ.I])
        circ.V, circ.I = vt, it

        # ============================================================ clip 2
        with self.say("c7.circuit.2") as c:
            c.wait_until("plain words")
            self.play(*during(disappear(v_words, r_words, c_words, i_words), 0, 0.45),
                      *during([circ.animate.scale(SCALE2 / SCALE1).move_to(POS2)], 0.3, 1.0),
                      run_time=2.0)

            c.wait_until("push")
            push = T("voltage: the push", 36).move_to([COL_X, 2.5, 0])
            self.play(FlashAround(circ.source, run_time=1.4, time_width=1.5),
                      *appear(push), run_time=1.4)

            c.wait_until("flow")
            dots, st = flow_system(circ)
            g0 = raw_to_screen(circ, -1.0, _BOT + 0.38)
            g1 = raw_to_screen(circ, -1.0, _BOT - 0.38)
            gate = DashedLine(g0, g1, dash_length=0.08, color=DIM, stroke_width=3)
            flow = T("current: charge per second", 36).move_to([COL_X, 1.55, 0])
            self.play(FadeIn(dots), Create(gate), *during(appear(flow), 0.3, 1.0), run_time=1.6)

            c.wait_until("water")
            pc = np.array([COL_X, -1.2, 0])
            tube = VGroup(Line(pc + [-2.4, 0.3, 0], pc + [2.4, 0.3, 0]),
                          Line(pc + [-2.4, -0.3, 0], pc + [2.4, -0.3, 0])).set_stroke(FG, 3)
            water = Rectangle(width=4.8, height=0.6, stroke_width=0, fill_color=TEAL,
                              fill_opacity=0.18).move_to(pc)
            gc = pc + [-1.3, 0.95, 0]
            dial = Circle(radius=0.32, color=FG, stroke_width=3).move_to(gc)
            stem = Line(gc + 0.32 * DOWN, pc + 0.3 * UP, color=FG, stroke_width=3)
            needle = Line(gc, gc + 0.24 * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]),
                          color=FG, stroke_width=3)
            gauge = VGroup(dial, stem, needle)
            p_lbl = T("push", 30).next_to(dial, RIGHT, buff=0.25)
            flows = [Arrow(pc + [x - 0.35, 0, 0], pc + [x + 0.35, 0, 0], buff=0, color=GOLD,
                           stroke_width=4, tip_length=0.2) for x in (-1.2, 0.0, 1.2)]
            f_lbl = T("current", 30, GOLD).next_to(tube, DOWN, buff=0.22)
            self.play(FadeIn(water), Create(tube), FadeIn(gauge), run_time=1.2)
            self.play(*appear(p_lbl, shift=None), *[GrowArrow(a) for a in flows],  # early: the pipe sketch is labelled whole
                      *during(appear(f_lbl), 0.3, 1.0), run_time=1.2)

            c.wait_until("pressure")
            self.play(Rotate(needle, angle=-PI / 2, about_point=gc),
                      FlashAround(p_lbl, run_time=1.2, time_width=1.5), run_time=1.2)

            c.wait_until("and current is the flow")
            self.play(*flash(flows, color=GOLD, run_time=1.3, time_width=1.5), run_time=1.3)

            c.wait_until("ac")
            pipe = [water, tube, gauge, p_lbl, *flows, f_lbl]
            st["u0"] = st["u"]
            st["mode"] = "ac"
            om = VGroup(tex(r"\omega", size=52),
                        T("angular frequency\nof the source", 32, line_spacing=0.9))
            om.arrange(RIGHT, buff=0.35).move_to([COL_X, -1.1, 0])
            c.wait_until("angular frequency")
            self.play(*during(disappear(*pipe), 0, 0.45),
                      *during(appear(om, shift=None), 0.5, 1.0), run_time=1.6)

        # ============================================================ clip 3
        with self.say("c7.circuit.3") as c:
            st["mode"] = "off"
            self.play(FadeOut(dots), FadeOut(gate),
                      Transform(circ.current, st["arrow0"]), Rotate(circ.source[1], angle=-st["ang"]),
                      run_time=1.4)
            dots.clear_updaters()
            self.remove(dots)

            c.wait_until("each one")
            self.play(*disappear(push, flow, om), run_time=1.0)

            laws = four_laws().move_to([COL_X, 0.1, 0])
            laws.align_to([0.4, 0, 0], LEFT)
            rows = list(laws)

            c.wait_until("ohm")
            self.play(*appear(rows[0]), restyle(circ.resistor, width=8), run_time=1.4)

            c.wait_until("times the current")
            self.play(FlashAround(VGroup(laws.ohm[3], laws.ohm[4]), run_time=1.5, time_width=1.5),
                      FlashAround(circ.current, color=GOLD, run_time=1.5, time_width=1.5),
                      run_time=1.5)

            c.wait_until("store")
            p1, p2 = circ.capacitor
            c1, c2 = p1.get_center(), p2.get_center()

            def signs(dx):
                out = []
                for x in dx:
                    out.append(tex("+", size=30, color=PINK).move_to(c1 + [x, 0.2, 0]))
                    out.append(tex("-", size=30, color=PINK).move_to(c2 + [x, -0.2, 0]))
                return out
            ch1 = signs([-0.2, 0.2])
            self.play(*appear(rows[1]), restyle(circ.resistor, width=3),
                      restyle(circ.capacitor, width=7), run_time=1.4)
            self.play(*appear(*ch1, shift=None, lag=0.15), run_time=1.2)

            c.wait_until("bigger")
            ch2 = signs([-0.56, 0.56])
            self.play(FlashAround(laws.store[3], color=PINK, run_time=1.5, time_width=1.5),
                      *appear(*ch2, shift=None, lag=0.15), run_time=1.5)

        # ============================================================ clip 4
        with self.say("c7.circuit.4") as c:
            self.play(*appear(rows[2]), run_time=1.3)
            a = raw_to_screen(circ, _RX, _TOP)
            b = raw_to_screen(circ, _RX, _CY + _GAP + 0.08)
            arr = [Dot(a, radius=0.06, color=FG).set_opacity(0) for _ in range(4)]
            self.add(*arr)
            self.play(LaggedStart(*[_arrive(d, a, b) for d in arr], lag_ratio=0.3), run_time=2.2)
            self.remove(*arr)

            c.wait_until("derivative")
            self.play(FlashAround(laws.rate[2], run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("loop")
            self.play(*appear(rows[3]), restyle(circ.capacitor, width=4), run_time=1.3)
            self.play(VShowPassingFlash(loop_path(circ), time_width=0.35), run_time=2.4)

            c.wait_until("shared")
            self.play(FlashAround(laws.loop[0], run_time=1.4, time_width=1.5),
                      FlashAround(circ.source, run_time=1.4, time_width=1.5), run_time=1.4)
            self.play(FlashAround(laws.loop[2], color=BLUE, run_time=1.4, time_width=1.5),
                      FlashAround(laws.loop[4], color=PINK, run_time=1.4, time_width=1.5),
                      run_time=1.4)

        # ============================================================ clip 5
        with self.say("c7.circuit.5") as c:
            gone = [circ, *ch1, *ch2]
            self.play(*during(disappear(*gone), 0, 0.6), *set_alpha([laws], DIMMED), run_time=1.4)

            cx = -3.2
            big_i = tex("I", size=120).move_to([cx - 1.75, 0.9, 0])
            small_i = tex("i", size=120).move_to([cx + 1.75, 0.9, 0]).align_to(big_i, DOWN)
            i_cap = T("the current", 32, DIM).next_to(big_i, DOWN, buff=0.45)
            root = tex(r"\sqrt{-1}", size=40, color=DIM)
            root.move_to([small_i.get_x(), i_cap.get_y(), 0])
            c.wait_until("capital eye")
            self.play(*appear(big_i, shift=None), *during(appear(i_cap), 0.3, 1.0), run_time=1.2)
            c.wait_until("small eye")
            self.play(*appear(small_i, shift=None), *during(appear(root), 0.3, 1.0), run_time=1.2)

            c.wait_until("out loud")
            xs = np.linspace(-0.6, 0.6, 60)
            wave = VMobject().set_points_smoothly(
                [[cx + x, 0.95 + 0.16 * np.sin(14 * x) * np.cos(2.6 * x), 0] for x in xs])
            wave.set_stroke(RED, 3)
            same = T("same sound", 28, RED).next_to(wave, UP, buff=0.55)
            self.play(Create(wave), *during(appear(same), 0.3, 1.0), run_time=1.3)

            c.wait_until("j")
            j_line = VGroup(T("engineers write", 32), tex(r"j = \sqrt{-1}", size=44))
            j_line.arrange(RIGHT, buff=0.3).move_to([cx, -1.7, 0])
            self.play(*appear(j_line), run_time=1.2)

            c.wait_until("colours")
            self.play(big_i.animate.set_color(GOLD), FlashAround(big_i, color=GOLD, run_time=1.6,
                                                                 time_width=1.5), run_time=1.6)
            self.play(small_i.animate.set_color(PINK), FlashAround(small_i, color=PINK,
                                                                   run_time=1.6, time_width=1.5),
                      run_time=1.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
