"""Chapter 6, scene 6: resistance, Ohm's law, the 10 ohm resistor in the loop, the I-V line, water. Clips c6.ohm.1 – c6.ohm.4.

Ends on handover_shot() (s7's first frame): the running loop with the 10 Ω resistor in its slot,
TEAL "1.5 V" arrows on battery and resistor, GOLD "0.15 A" current arrow on the top wire.
"""
# style: 2
# handover: next
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

S2 = load_scene("ch6_s2_electrons")

BEIGE = "#D8C39A"
V_OFF = 0.65      # TEAL voltage arrows sit this far outside the wire
V_LEN = 1.0       # their length


# --- the loop pieces (shared by clip 3 and the handover) ------------------------------------
def _loop():
    loop = S2.Loop()
    loop.wire.remove(loop.slot_fill)
    return loop


def _bat_arrow(loop):
    c = loop.battery_center()
    x = c[0] - V_OFF
    return S2.voltage_arrow([x, c[1] - V_LEN / 2, 0], [x, c[1] + V_LEN / 2, 0])


def _slot_arrow(loop):
    c = loop.slot_center()
    x = c[0] + V_OFF
    return S2.voltage_arrow([x, c[1] - V_LEN / 2, 0], [x, c[1] + V_LEN / 2, 0])


def _cur_arrow(loop):
    tp = loop.bounds()[3] + 0.35
    return S2.current_arrow([-0.9, tp, 0], [0.9, tp, 0])


def _bat_label(arrow, text):
    lab = text if not isinstance(text, str) else T(text, 32, TEAL)
    return lab.next_to(arrow, LEFT, buff=0.2)


def _slot_label(arrow, text):
    lab = text if not isinstance(text, str) else T(text, 32, TEAL)
    return lab.next_to(arrow, RIGHT, buff=0.2)


def _cur_label(arrow, text):
    lab = text if not isinstance(text, str) else T(text, 32, GOLD)
    return lab.next_to(arrow, UP, buff=0.18)


def _res10(loop):
    r = S2.resistor()
    loop.place(r)
    lab = T("10 Ω", 32).next_to(r.body, LEFT, buff=0.25)
    return r, lab


def handover_shot():
    """Last frame of this scene, s7's first: VGroup(loop, resistor, "10 Ω", battery arrow, its
    "1.5 V", resistor arrow, its "1.5 V", current arrow, "0.15 A")."""
    loop = _loop()
    r, rlab = _res10(loop)
    va, vr, ca = _bat_arrow(loop), _slot_arrow(loop), _cur_arrow(loop)
    return VGroup(loop, r, rlab, va, _bat_label(va, "1.5 V"), vr, _slot_label(vr, "1.5 V"),
                  ca, _cur_label(ca, "0.15 A"))


# --- clip 1: electrons bouncing through a lattice --------------------------------------------
def bouncer(els, centres, box, speed=1.6, bias=1.4, hit=0.44, seed=3, fade_edge=None):
    """Electrons random-walk with a leftward bias, bouncing off ion centres and the box's walls;
    they wrap round in x (fading at the ends)."""
    rng = np.random.default_rng(seed)
    n = len(els)
    a = rng.uniform(0, TAU, n)
    vel = np.stack([np.cos(a), np.sin(a)], 1)
    x0, x1, y0, y1 = box
    C = np.array([c[:2] for c in centres])

    def upd(m, dt):
        if dt == 0:
            return
        vel[:] += rng.normal(0, 3.0 * np.sqrt(dt), (n, 2))
        vel[:, 0] -= bias * dt
        vel[:] /= np.linalg.norm(vel, axis=1, keepdims=True)
        for i, e in enumerate(m.submobjects):
            p = e.get_center()[:2] + vel[i] * speed * dt
            d = C - p
            dist = np.linalg.norm(d, axis=1)
            k = int(np.argmin(dist))
            if dist[k] < hit:
                nrm = (p - C[k]) / max(dist[k], 1e-6)
                if vel[i] @ nrm < 0:
                    vel[i] -= 2 * (vel[i] @ nrm) * nrm
                p = C[k] + nrm * hit
            if p[1] > y1 or p[1] < y0:
                vel[i, 1] *= -1
                p[1] = np.clip(p[1], y0, y1)
            if p[0] < x0:
                p[0] += x1 - x0
            elif p[0] > x1:
                p[0] -= x1 - x0
            e.move_to([p[0], p[1], 0])
            if fade_edge is not None:
                S2._edge_fade(e, p[0], edge=fade_edge, ramp=0.5)
    return upd


def _free_spots(centres, box, n, seed=11, clear=0.6):
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = box
    out = []
    C = np.array([c[:2] for c in centres])
    while len(out) < n:
        p = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1)])
        if np.min(np.linalg.norm(C - p, axis=1)) > clear:
            out.append([p[0], p[1], 0])
    return out


def _conductor(w, h, lat, center):
    rect = RoundedRectangle(corner_radius=0.25, width=w, height=h).set_stroke(FG, 4).move_to(center)
    lat.move_to(center)
    return VGroup(rect, lat)


# --- clip 3: the drawn resistor with bands -----------------------------------------------------
def _part():
    body = RoundedRectangle(corner_radius=0.3, width=2.2, height=0.72).set_fill(BEIGE, 1).set_stroke(width=0)
    cols = ["#8B4A1C", "#202020", "#202020", GOLD]
    xs = [-0.6, -0.3, 0.0, 0.62]
    bands = VGroup(*[Rectangle(width=0.16, height=0.72).set_fill(c, 1).set_stroke(width=0).move_to([x, 0, 0])
                     for c, x in zip(cols, xs)])
    leads = VGroup(Line([-1.1, 0, 0], [-2.0, 0, 0]), Line([1.1, 0, 0], [2.0, 0, 0])).set_stroke("#B0B4BA", 5)
    return VGroup(leads, body, bands)


# --- clip 4: the water analogy ------------------------------------------------------------------
def _gauge(angle):
    dial = Circle(radius=0.5).set_stroke(FG, 3).set_fill(BG, 1)
    ticks = VGroup(*[Line(0.38 * np.array([np.cos(t), np.sin(t), 0]), 0.48 * np.array([np.cos(t), np.sin(t), 0]))
                     for t in np.linspace(PI * 1.1, -PI * 0.1, 7)]).set_stroke(DIM, 2)
    needle = Line(ORIGIN, 0.4 * np.array([np.cos(angle), np.sin(angle), 0])).set_stroke(YELLOW, 4)
    hub = Dot(radius=0.06, color=FG)
    return VGroup(dial, ticks, needle, hub)


def _tag(a, b):
    g = VGroup(T(a, 36), MathTex(r"\leftrightarrow", font_size=44, color=DIM), T(b, 36))
    return g.arrange(RIGHT, buff=0.3)


class Resistance(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        shot = handover_shot()
        sweep_clear(self, FadeIn(shot), run_time=1.6)
        self.wait(1.2)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        title = T("Circuit Theory", 60)
        ctr = np.array([0, -0.5, 0])
        lat = S2.lattice(7, 3, (1.4, 1.1), 0.3)
        cond = _conductor(10.4, 3.4, lat, ctr)
        box = (-5.0, 5.0, ctr[1] - 1.5, ctr[1] + 1.5)
        centres = [m.get_center() for m in lat]
        els = VGroup(*[S2.electron().move_to(p) for p in _free_spots(centres, box, 16)])
        upd = bouncer(els, centres, box, fade_edge=5.0)
        rlab = T("resistance (R)", 42, YELLOW).move_to([0, -2.95, 0])

        with self.say("c6.ohm.1") as c:
            self.play(*appear(title, shift=None), run_time=1.0)  # early: heading, read as the line opens
            c.wait_until("oppose")
            self.play(title.animate.scale(0.75).move_to([0, 3.3, 0]), FadeIn(cond), run_time=1.5)
            els.add_updater(upd)
            self.play(FadeIn(els), run_time=1.0)
            c.wait_until(own_word=rlab)
            self.play(*appear(rlab), run_time=1.0)
            c.wait_until("bigger")
            # two conductors side by side, the same current through each
            xs = (-3.4, 3.4)
            y = 1.85
            sparse = _conductor(4.4, 1.5, S2.lattice(4, 2, (1.0, 0.7), 0.2), [xs[0], y, 0])
            dense = _conductor(4.4, 1.5, S2.lattice(8, 3, (0.5, 0.42), 0.13), [xs[1], y, 0])
            curs = [S2.current_arrow([x - 1.0, y + 1.15, 0], [x + 1.0, y + 1.15, 0]) for x in xs]
            vs = [S2.voltage_arrow([xs[0] + 0.7, y - 1.05, 0], [xs[0] - 0.7, y - 1.05, 0]),
                  S2.voltage_arrow([xs[1] + 2.0, y - 1.05, 0], [xs[1] - 2.0, y - 1.05, 0])]
            tag = T("bigger R, bigger V, for a given current", 38).move_to([0, -0.25, 0])
            sweep_clear(self, FadeIn(sparse), FadeIn(dense), *[GrowArrow(a.arrow) for a in curs],
                        keep=[rlab], run_time=1.6)
            els.clear_updaters()
            c.wait_until("the bigger the voltage")
            self.play(*[GrowArrow(v.arrow) for v in vs], *during(appear(tag), 0.45, 1), run_time=1.6)
        self.c1 = (rlab, sparse, dense, curs, vs, tag)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        rlab, sparse, dense, curs, vs, tag = self.c1
        eq = MathTex("R", "=", r"{V", r"\over", r"I}", font_size=80)
        eq[2].set_color(TEAL)
        eq[4].set_color(GOLD)
        eq.move_to([-1.6, -2.15, 0])
        t_v = T("pd across it", 34, TEAL).next_to(eq, RIGHT, buff=0.6).match_y(eq[2])
        t_i = T("current through it", 34, GOLD).next_to(eq, RIGHT, buff=0.6).match_y(eq[4])
        ohm = MathTex("V", "=", "I", "R", font_size=110)
        ohm[0].set_color(TEAL)
        ohm[2].set_color(GOLD)
        ohm.move_to([0, -0.9, 0])
        law = T("Ohm's law", 46, YELLOW).next_to(ohm, DOWN, buff=0.55)
        unit = T("ohms (Ω)", 40).next_to(ohm, RIGHT, buff=0.8)

        with self.say("c6.ohm.2") as c:
            self.play(*during(FadeOut(rlab), 0, 0.45), *during(FadeIn(eq), 0.5, 1), run_time=1.4)
            c.wait_until("across", own_word=t_v)
            self.play(*appear(t_v), run_time=1.0)
            c.wait_until("current through", own_word=t_i)
            self.play(*appear(t_i), run_time=1.0)
            c.wait_until("the current times")
            up = UP * 3.65
            sweep_clear(self, *[time_span(m.animate.shift(up), 0.7, 1.4) for m in (eq, t_v, t_i)],
                        keep=[eq, t_v, t_i], run_time=1.4)
            # V = IR fades in whole below the settled R = V/I (a fly copy overlapped it)
            self.play(*appear(ohm, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("ohm's law")
            self.play(*appear(law), run_time=1.0)
            c.wait_until("measured in ohms")
            self.play(*appear(unit, shift=None), run_time=1.0)
            c.wait_until("omega")
            rt = min(1.5, c.until())
            self.play(FlashAround(select(unit, "Ω")[0], run_time=rt, time_width=1.5), run_time=rt)
        self.c2 = (eq, t_v, t_i, ohm, law, unit)

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        sym = S2.resistor(vertical=False, span=3.0).scale(1.5).move_to([-2.9, -0.3, 0])
        sym_lab = MathTex(r"R\,\Omega", font_size=60).next_to(sym.body, UP, buff=0.35)
        part = _part().move_to([3.3, -0.3, 0])

        loop = _loop()
        lamp = S2.lamp(lit=True)
        loop.place(lamp)
        va, vr, ca = _bat_arrow(loop), _slot_arrow(loop), _cur_arrow(loop)
        vb_lab, vl_lab = _bat_label(va, "1.5 V"), _slot_label(vr, "1.5 V")
        i_lab = _cur_label(ca, MathTex("I", font_size=40, color=GOLD))
        res, res_lab = _res10(loop)

        eq = MathTex("I", "=", "1.5", r"\div", "10", "=", r"0.15\,\text{A}", font_size=50)
        eq[0].set_color(GOLD)
        eq[2].set_color(TEAL)
        eq[6].set_color(GOLD)
        eq.move_to([0.1, -1.65, 0])

        with self.say("c6.ohm.3", gap=3.4) as c:
            c.wait_until("called a resistor")
            sweep_clear(self, FadeIn(sym), *appear(sym_lab), run_time=1.6)
            c.wait_until("small rectangle")
            self.play(FlashAround(sym.body, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("labelled")
            self.play(FlashAround(sym_lab, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("coloured bands")
            self.play(FadeIn(part, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("swap")
            # symbol and part leave whole; the 10 ohm resistor waits beside the new loop
            res.move_to([5.6, -3.0, 0])
            sweep_clear(self, FadeIn(loop), FadeIn(lamp), GrowArrow(va.arrow), GrowArrow(vr.arrow),
                        GrowArrow(ca.arrow), FadeIn(vb_lab), FadeIn(vl_lab), FadeIn(i_lab), FadeIn(res),
                        run_time=1.4)
            self.play(lamp.animate.scale(0.02), *during(FadeOut(lamp), 0.5, 0.6),
                      *during(res.animate.move_to(loop.slot_center()), 0.2, 0.9),
                      *during(FadeIn(res_lab), 0.75, 1), run_time=1.5)
            res.move_to(loop.slot_center())
            c.wait_until("one and a half volts")
            self.play(*flash([vb_lab, vl_lab], run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("the current is")
            self.play(*appear(*eq[:5], lag=0.15, shift=None), run_time=1.4)
            c.wait_until("which is")
            self.play(*appear(*eq[5:], shift=None), run_time=1.0)
            settle(self, eq)
            n_i = _cur_label(ca, "0.15 A")
            c.wait_until("zero point one five")
            self.play(*swap(i_lab, n_i), FlashAround(eq[6], run_time=1.2, time_width=1.5), run_time=1.2)

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        ax = Axes(x_range=[0, 4.4, 1], y_range=[0, 0.44, 0.1], x_length=8.8, y_length=5.5, tips=True,
                  axis_config={"color": DIM, "stroke_width": 3})
        ax.shift(np.array([-4.6, -2.7, 0]) - ax.c2p(0, 0))
        nums = VGroup(*[T(str(v), 30, DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.2) for v in (1, 2, 3, 4)],
                      *[T(f"0.{k}", 30, DIM).next_to(ax.c2p(0, k / 10), LEFT, buff=0.2) for k in (1, 2, 3, 4)])
        xl = T("V (volts)", 34, TEAL).next_to(ax.x_axis.get_right(), RIGHT, buff=0.2)
        yl = T("I (amps)", 34, GOLD).next_to(ax.y_axis.get_top(), RIGHT, buff=0.3)
        line1 = Line(ax.c2p(0, 0), ax.c2p(4, 0.4)).set_stroke(FG, 5)
        line2 = Line(ax.c2p(0, 0), ax.c2p(4, 0.2)).set_stroke(DIM, 5)
        dot = Dot(ax.c2p(1.5, 0.15), radius=0.12, color=GOLD).set_z_index(2)

        def pt_lab(v, i):
            lab = T(f"{v} V, {i} A", 32, t2c={f"{v} V": TEAL, f"{i} A": GOLD})
            return lab.next_to(ax.c2p(v, i), UP, buff=0.35).shift(LEFT * 1.25)
        lab1 = pt_lab(1.5, 0.15)
        lab2 = pt_lab(3, 0.3)
        o_dot = Dot(ax.c2p(0, 0), radius=0.12, color=YELLOW).set_z_index(2)
        l10 = T("10 Ω", 34).next_to(line1.get_end(), RIGHT, buff=0.2)
        l20 = T("20 Ω", 34, DIM).next_to(line2.get_end(), RIGHT, buff=0.2)

        with self.say("c6.ohm.4", gap=3.0) as c:
            sweep_clear(self, Create(ax), *appear(nums, xl, yl, lag=0.05, shift=None), run_time=2.0)
            c.wait_until("line")
            self.play(Create(line1), run_time=1.5)
            self.play(FadeIn(dot, scale=0.5), *appear(lab1, l10, shift=None), run_time=1.0)
            c.wait_until("double")
            ghost = dot.copy().set_opacity(0.4)
            self.add(ghost)
            self.play(dot.animate.move_to(ax.c2p(3, 0.3)), lab1.animate.set_opacity(0.5),
                      *during(appear(lab2, shift=None), 0.5, 1), run_time=1.5)
            c.wait_until("no voltage")
            self.play(FadeIn(o_dot, scale=0.5), FlashAround(o_dot, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("flatter")
            self.play(Create(line2), *during(appear(l20, shift=None), 0.55, 1), run_time=1.4)
            c.wait_until("charge flowing")
            # clear the plot completely before the pipe comes in
            self.play(*disappear(*self.mobjects), run_time=0.9)
            # the water analogy
            py = 0.55
            walls = VGroup(Line([-4.6, py + 0.5, 0], [4.6, py + 0.5, 0]),
                           Line([-4.6, py - 0.5, 0], [4.6, py - 0.5, 0])).set_stroke(FG, 5)
            water = Rectangle(width=9.2, height=1.0).move_to([0, py, 0]).set_fill(BLUE, 0.22).set_stroke(width=0)
            rng = np.random.default_rng(5)
            flow = VGroup(*[Line(LEFT * 0.22, RIGHT * 0.22).set_stroke(BLUE, 4).move_to(
                [rng.uniform(-4.4, 4.4), py + rng.uniform(-0.32, 0.32), 0]) for _ in range(14)])

            def run_water(m, dt):
                for d in m:
                    x = d.get_x() + 1.1 * dt
                    if x > 4.35:
                        x -= 8.7
                    d.set_x(x)
            g_hi, g_lo = _gauge(PI * 0.05), _gauge(PI * 0.8)
            stems = VGroup()
            for g, x in ((g_hi, -3.3), (g_lo, 3.3)):
                g.move_to([x, py + 1.55, 0])
                stems.add(Line([x, py + 0.5, 0], [x, py + 1.05, 0]).set_stroke(FG, 4))
            hi_t = T("high", 30, DIM).next_to(g_hi, RIGHT, buff=0.25)
            lo_t = T("low", 30, DIM).next_to(g_lo, LEFT, buff=0.25)
            tags = [_tag("water", "charges"), _tag("pipe", "conductor"), _tag("pressure difference", "voltage")]
            for k, tg in enumerate(tags):
                tg.move_to([0, py - 1.45 - 0.8 * k, 0])
            self.play(FadeIn(walls), FadeIn(water), FadeIn(flow), FadeIn(stems), FadeIn(g_hi),
                      FadeIn(g_lo), run_time=1.2)
            flow.add_updater(run_water)
            self.play(*appear(hi_t, lo_t, shift=None), run_time=1.0)
            for tg, word in zip(tags, ("water flowing", "pipe", "pressure")):
                c.wait_until(word)
                self.play(*appear(tg), run_time=1.0)
        self.wait(1.5)
        flow.clear_updaters()
