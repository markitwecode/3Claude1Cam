"""Chapter 7, scene 7: recap, the lecture in one line, and next (Lecture 9). Clips c7.recap.1 – c7.recap.4.

Six slots (two rows of three, ch6_s7's grid and T 28 captions), each a small copy of its scene:
r1 ch7_s2 circuit() with c7.circuit.4's critical path, CB2 dim; r2 ch7_s3's 12 ns budget bar and
YELLOW T_c arrow; r3 ch7_s4's stage bars (names inside, as ch7_s5), period marker at 6.5, idle box;
r4 ch7_s5's comparison numbers, GREEN "× 1.85"; r5 ch7_s5's three bars, CB4 outlined YELLOW;
r6 ch7_s6's stalled staircase. Then the slots shrink to a row along the top and three chips
(icons: ch1_s3 WindowDiagram, ch4_s5 sync_circuit, ch6_s6 pipe_diagram) light in turn.
End card: "Next: Lecture 9" over p. 120's title text, L6's counter (hook_counter) counting, two
blank machine outlines with "?"; held 8 s.
The source scenes' builders are loaded from their files (importlib), so the tiles stay identical.
"""
# style: 2
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
from lib.style import *  # noqa: E402,F403


def _load(stem):
    p = Path(__file__).resolve().parent / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_recap7_{stem}", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


S2 = _load("ch7_s2_circuit")         # circuit(), budget_bar(), CRIT_W, OFF
S6 = _load("ch7_s6_limits")          # dep_wire(), staircase geometry
W13 = _load("ch1_s3_ffnumbers")      # WindowDiagram
SY45 = _load("ch4_s5_synchroniser")  # sync_circuit()
P66 = _load("ch6_s6_registers")      # pipe_diagram()
H11 = _load("ch1_s1_hook")           # hook_counter(), set_led()


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- grid (ch6_s7's slots, three per row) ----------------------------------------------------
COLS = (-4.45, 0.0, 4.45)
TOP_Y, BOT_Y = 2.45, -0.75
CAP_T = (1.1, 0.7)
CAP_B = (-2.3, -2.7, -3.1)
ROW_Y = 3.15                         # clip 3: the six slots in one row along the top
ROW_X = [-5.55 + 2.22 * i for i in range(6)]


def caption(text, x, y):
    return T(text, 28).move_to(_p(x, y))


def fit(g, w, h, center):
    g.scale(min(w / g.width, h / g.height)).move_to(center)
    return g


def thin(g, f):
    for m in g.family_members_with_points():
        m.set_stroke(width=m.get_stroke_width() * f)
    return g


def dim_state(g, op=DIMMED):
    for m in g.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * op)
        m.set_stroke(opacity=m.get_stroke_opacity() * op)
    return g


def tile_bar(specs, x0, y, u, h=0.42, outline=None):
    """specs = [(colour, ns, name or None)]: budget-bar segments (fill 0.85, no stroke), T 28 names
    inside, thin BG dividers between adjacent PURPLE segments; outline colour -> a stroke-2 box."""
    g = VGroup()
    g.segs, g.names, g.divs = [], [], []
    x = x0
    for col, ns, name in specs:
        r = Rectangle(width=ns * u, height=h).set_stroke(width=0).set_fill(col, 0.85).move_to(_p(x + ns * u / 2, y))
        g.segs.append(r)
        if name:
            g.names.append(T(name, 28).move_to(r))
        x += ns * u
    for (ca, _, _), (cb, _, _), r in zip(specs, specs[1:], g.segs):
        if ca == PURPLE and cb == PURPLE:
            g.divs.append(Line(r.get_corner(UR), r.get_corner(DR)).set_stroke(BG, 3).set_z_index(0.5))
    g.add(*g.segs, *g.divs, *g.names)
    g.outline = None
    if outline is not None:
        g.outline = Rectangle(width=x - x0, height=h).set_stroke(outline, 2).set_fill(opacity=0)
        g.outline.move_to(_p((x0 + x) / 2, y)).set_z_index(1)
        g.add(g.outline)
    return g


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(8.0)                                                     # end card; music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ r1, r2, r3
    def clip1(self):
        self.tiles, self.caps = [], []
        with self.say("c7.recap.1") as c:
            # ---- r1: s2's circuit, critical path bright, CB2 dim
            C = S2.circuit()
            crit = [C.w_q, C.w_up, C.w_1, C.w_34, C.w_out]
            for w in crit:
                w.set_stroke(opacity=1, width=S2.CRIT_W)
            for i in (0, 2, 3):
                C.cb[i].set_stroke(BLUE, S2.CRIT_W)
            for m in (C.w_dn, C.w_2, C.cb[1]):
                m.set_stroke(opacity=S2.OFF)
            for f in (C.ff_in, C.ff_out):
                f.remove(f.d_l, f.q_l, f.qb_l)
            t1 = VGroup(C.w_q, C.w_up, C.w_dn, C.w_1, C.w_2, C.w_34, C.w_out, C.fork, C.clk_bus, C.clk_dot,
                        C.br_in, C.br_out, C.ff_in, C.ff_out, *C.cb)
            fit(t1, 4.1, 2.0, _p(COLS[0], TOP_Y))
            thin(t1, 0.6)
            cap1 = [caption("the slowest route", COLS[0], CAP_T[0]), caption("sets the period", COLS[0], CAP_T[1])]

            c.wait_until("r1")
            self.play(FadeIn(t1), run_time=1.3)
            c.wait_until(own_word=cap1[0])
            self.play(*appear(cap1[0], shift=None), run_time=1.0)
            flashes = [time_span(VShowPassingFlash(w.copy().set_stroke(YELLOW, 6, opacity=1), time_width=0.6),
                                 0.25 * i, 0.25 * i + 0.6) for i, w in enumerate(crit)]
            c.wait_until(own_word=cap1[1])
            self.play(*flashes, *during(appear(cap1[1], shift=None), 0.3, 1.0), run_time=1.6)
            self.tiles.append(t1)
            self.caps += cap1

            # ---- r2: s3's 12 ns budget bar with its YELLOW T_c arrow
            cx, cy = COLS[1], TOP_Y
            u = 0.3
            x0 = cx - 6 * u
            segs = [("t_{pc}", PINK, 0.2 * u)] + [("t_{pd}", PURPLE, d * u) for d in (3.2, 3, 5.5)] + \
                [("t_{su}", GOLD, 0.1 * u)]
            bar = S2.budget_bar(segs, 12 * u, x0=x0, y=cy + 0.4, syms=False)
            bar.remove(bar.tc)
            arr = DoubleArrow(_p(x0, cy - 0.15), _p(x0 + 12 * u, cy - 0.15), buff=0, color=YELLOW,
                              stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.1)
            tcl = MathTex(r"T_c = 12\text{ ns}", font_size=36, color=YELLOW).move_to(_p(cx, cy - 0.6))
            cap2 = [caption("12 ns, 83.3 MHz", cx, CAP_T[0])]

            c.wait_until("r2")
            self.play(GrowFromEdge(bar.outline, LEFT),
                      *[time_span(FadeIn(s), 0.2 + 0.15 * i, 0.8 + 0.15 * i) for i, s in enumerate(bar.segs)],
                      run_time=1.5)
            c.wait_until("twelve nanoseconds")
            self.play(GrowFromCenter(arr), *during(appear(tcl, shift=None), 0.4, 1.0), run_time=1.2)
            c.wait_until("eighty-three")
            self.play(*appear(cap2[0], shift=None), run_time=1.0)
            t2 = VGroup(*bar.segs, bar.outline, arr, tcl)
            settle(self, t2)
            self.tiles.append(t2)
            self.caps += cap2

            # ---- r3: s4's two stage bars, the period marker at 6.5 and the idle box
            cx = COLS[2]
            u = 0.5
            x0 = cx - 1.9
            b1 = tile_bar([(PINK, 0.2, None), (PURPLE, 3.2, "CB1"), (PURPLE, 3, "CB3"), (GOLD, 0.1, None)],
                          x0, cy + 0.2, u, h=0.55)
            b2 = tile_bar([(PINK, 0.2, None), (PURPLE, 5.5, "CB4"), (GOLD, 0.1, None)], x0, cy - 0.6, u, h=0.55)
            xm = x0 + 6.5 * u
            mk = Line(_p(xm, cy + 0.65), _p(xm, cy - 1.05)).set_stroke(YELLOW, 4).set_z_index(2)
            v65 = T("6.5 ns", 28, GOLD).next_to(mk, UP, buff=0.1)
            idle = DashedVMobject(Rectangle(width=0.7 * u, height=0.55), num_dashes=10).set_stroke(DIM, 2)
            idle.move_to(_p(x0 + 6.15 * u, cy - 0.6))
            idle_l = T("idle", 28, DIM).next_to(idle, RIGHT, buff=0.15)
            cap3 = [caption("the slowest stage", cx, CAP_T[0]), caption("decides", cx, CAP_T[1])]
            self.b1, self.b2, self.idle = b1, b2, idle

            c.wait_until("r3")
            self.play(*appear(b1, b2, shift=None, lag=0.3), run_time=1.4)
            c.wait_until("six point five")
            self.play(FadeIn(mk, shift=0.2 * DOWN), *appear(v65, shift=None), run_time=1.0)
            c.wait_until("set the period")
            self.play(FadeIn(idle), *appear(idle_l, shift=None), run_time=1.0)
            self.play(*appear(*cap3, shift=None, lag=0.4), run_time=min(1.2, c.until(floor=0.5)))
            t3 = VGroup(b1, b2, mk, v65, idle, idle_l)
            settle(self, t3)
            self.tiles.append(t3)
            self.caps += cap3

    # ------------------------------------------------------------------ r4, short, r5, r6
    def clip2(self):
        with self.say("c7.recap.2", gap=2.0) as c:
            # ---- r4: s5's comparison, GREEN "× 1.85"
            cx, cy = COLS[0], BOT_Y
            la = T("12 ns → 13 ns", 32, GOLD)
            lp = T("+ 1 ns", 28, DIM)
            ra = VGroup(la, lp).arrange(RIGHT, buff=0.3).move_to(_p(cx, cy + 0.7))
            lb = T("83.3 → 153.85 MHz", 32, GOLD).move_to(_p(cx, cy))
            lt = T("× 1.85", 40, GREEN).next_to(lb, DOWN, buff=0.3).align_to(lb, RIGHT)
            cap4 = [caption("throughput × 1.85,", cx, CAP_B[0]), caption("latency + 1 ns", cx, CAP_B[1])]

            self.play(*appear(lb, lt, cap4[0], shift=None, lag=0.3), run_time=1.4)
            c.wait_until("latency")
            self.play(*appear(la, lp, cap4[1], shift=None, lag=0.3), run_time=1.2)
            t4 = VGroup(la, lp, lb, lt)
            self.tiles.append(t4)
            self.caps += cap4

            # ---- short: back in slot 3, the idle box and the new register's PINK and GOLD flash
            cap4c = caption("unequal stages, + 0.3 ns", cx, CAP_B[2])
            c.wait_until("unequal")
            self.play(FlashAround(self.idle, color=FG, time_width=1.5, buff=0.08), run_time=1.3)
            c.wait_until("costs time")
            self.play(FlashAround(self.b1.segs[-1], color=GOLD, time_width=1.5, buff=0.08),
                      FlashAround(self.b2.segs[0], color=PINK, time_width=1.5, buff=0.08),
                      *during(appear(cap4c, shift=None), 0.3, 1.0), run_time=1.4)
            self.caps.append(cap4c)

            # ---- r5: s5's three bars, CB4's outlined YELLOW
            cx = COLS[1]
            u = 0.5
            x0 = cx - 1.45
            ys = (cy + 0.5, cy - 0.15, cy - 0.8)
            bars = [tile_bar([(PINK, 0.2, None), (PURPLE, a, n), (GOLD, 0.1, None)], x0, y, u, h=0.5, outline=DIM)
                    for (a, n), y in zip(((3.2, "CB1"), (3, "CB3"), (5.5, "CB4")), ys)]
            xm = x0 + 5.8 * u
            mk = Line(_p(xm, cy + 0.85), _p(xm, cy - 1.15)).set_stroke(YELLOW, 4).set_z_index(2)
            v58 = T("5.8 ns", 28, GOLD).next_to(mk, UP, buff=0.1)
            cap5 = [caption("cutting again", cx, CAP_B[0]), caption("helps less", cx, CAP_B[1])]

            c.wait_until("r5")
            self.play(*appear(*bars, shift=None, lag=0.25), *during(appear(cap5[0], shift=None), 0.5, 1.0),
                      run_time=1.4)
            c.wait_until("helped less")
            self.play(*appear(cap5[1], shift=None), run_time=1.0)
            c.wait_until("block four")
            self.play(FadeIn(mk, shift=0.2 * DOWN), *appear(v58, shift=None),
                      restyle(bars[2].outline, outline=YELLOW, width=4), run_time=1.0)
            t5 = VGroup(*bars, mk, v58)
            settle(self, t5)
            self.tiles.append(t5)
            self.caps += cap5

            # ---- r6: s6's staircase, stalled, with its dashed RED stall
            cx = COLS[2]
            W, H, PIT = S6.STAGE_W, S6.STAGE_H, S6.STAIR_PITCH
            rows = []
            for r in range(S6.STAIR_N):
                col0 = r + (1 if r >= 1 else 0)
                tc = S6.TASK_COLORS[r + 1]
                rows.append([Rectangle(width=W, height=H).set_stroke(tc, 3).set_fill(tc, 0.18)
                             .move_to(_p((col0 + k) * W + W / 2, -r * PIT)) for k in (0, 1)])
            stall = DashedVMobject(Rectangle(width=W, height=H), num_dashes=24).set_stroke(RED, 3)
            stall.move_to(_p(1.5 * W, -PIT))
            a1, b0 = rows[1][0], rows[0][1]
            wire = S6.dep_wire(b0.get_right()[0], b0.get_y(), a1.get_left()[0], a1.get_y())
            st = VGroup(*[m for r in rows for m in r], stall, wire)
            s = 0.4
            st.scale(s, about_point=ORIGIN)
            for m in [*[m for r in rows for m in r], stall]:
                m.set_stroke(width=2)
            wire[0].set_stroke(width=3)
            st.move_to(_p(cx + 0.25, cy - 0.1))
            stall_l = T("stall", 28, RED).next_to(stall, LEFT, buff=0.08)
            cap6 = [caption("dependencies", cx, CAP_B[0]), caption("stall the pipeline", cx, CAP_B[1])]

            c.wait_until("r6")
            self.play(*[time_span(FadeIn(m), 0.25 * r, 0.25 * r + 0.7) for r, row in enumerate(rows) for m in row],
                      run_time=1.45)
            c.wait_until("needs the result")
            self.play(Create(wire[0]), *during([FadeIn(wire[1])], 0.8, 1.0),
                      *during(appear(*cap6, shift=None, lag=0.3), 0.3, 1.0), run_time=1.4)
            c.wait_until("the one before")
            self.play(FadeIn(stall), *appear(stall_l, shift=None),
                      run_time=min(1.2, c.until(floor=0.5)))
            t6 = VGroup(st, stall_l)
            settle(self, t6)
            self.tiles.append(t6)
            self.caps += cap6

    # ------------------------------------------------------------------ the lecture in one line
    def clip3(self):
        # icons, each from its chapter, no text
        Wd = W13.WindowDiagram(origin=ORIGIN, k=0.26, fs=0.6, words=False)
        ic1 = VGroup(Wd.guide, Wd.band, Wd.clk, Wd.d, Wd.up)
        Sc = SY45.sync_circuit()
        for f in (Sc.ff0, Sc.ff1):
            f.remove(f.d_l, f.q_l)
        ic2 = VGroup(Sc.btn, Sc.d0_w, Sc.link, Sc.bus, Sc.jdot, *Sc.clk_ws, Sc.ff0, Sc.ff1)
        D = P66.pipe_diagram()
        for f in D.ffs:
            f.remove(f.d_l, f.q_l, f.qb_l)
        ic3 = VGroup(*[g for gh in D.ghs for g in gh], D.b1, D.b2, D.bus, *D.dots, *D.brs, *D.ffs)
        ys = (1.3, -0.5, -2.3)
        icons = []
        for ic, y in zip((ic1, ic2, ic3), ys):
            fit(ic, 2.3, 1.1, _p(-5.0, y))
            icons.append(ic)
        thin(ic2, 0.6)
        thin(ic3, 0.6)
        txts = [T("flip-flops need time: set-up, hold, skew", 36),
                T("outside inputs need synchronisers", 36),
                T("registers between stages buy throughput", 36)]
        for t, y in zip(txts, ys):
            t.align_to(_p(-3.5, 0), LEFT).set_y(y)
        txts[1].shift(0.25 * UP)
        years = T("3.04 ns → 1.05 years", 30, GOLD).next_to(txts[1], DOWN, buff=0.18).align_to(txts[1], LEFT)
        rects = [RoundedRectangle(width=12.8, height=1.5, corner_radius=0.18).set_stroke(DIM, 2)
                 .set_fill(opacity=0).move_to(_p(0, y)) for y in ys]
        contents = [VGroup(icons[0], txts[0]), VGroup(icons[1], txts[1]), VGroup(icons[2], txts[2])]
        fulls = [g.copy() for g in contents]
        for g in contents:
            dim_state(g)

        with self.say("c7.recap.3") as c:
            # {lecture}: captions go, the slots shrink to a row along the top, the chips arrive dimmed
            # the tiles' small text fades (it would shrink below size 28); r4 keeps its GREEN x 1.85
            keep = self.tiles[3][3]
            texts = []
            for t in self.tiles:
                for m in [m for m in t.get_family() if isinstance(m, (Text, MathTex)) and m is not keep]:
                    for parent in t.get_family():
                        if m in parent.submobjects:
                            parent.remove(m)
                    texts.append(m)
            self.tiles[3].remove(keep)
            self.add(*texts)
            # staggered so no slot crosses another: the top row settles left first, then the bottom row rises
            top, bottom = [], []
            for i, (t, x) in enumerate(zip(self.tiles, ROW_X)):
                if t is self.tiles[3]:
                    continue
                t.generate_target()
                t.target.scale(min(1.95 / t.width, 0.95 / t.height)).move_to(_p(x, ROW_Y))
                (top if i < 3 else bottom).append(MoveToTarget(t))
            bottom.insert(0, keep.animate.scale(0.8).move_to(_p(ROW_X[3], ROW_Y)))
            self.remove(self.tiles[3])
            self.tiles[3] = VGroup(keep)
            self.play(*during(disappear(*self.caps, *texts), 0, 0.3), *during(top, 0.28, 0.58),
                      *during(bottom, 0.58, 0.86),
                      *during([FadeIn(r) for r in rects] + [FadeIn(g) for g in contents], 0.84, 1.0),  # early: the lecture's three lines shown whole, dimmed, then lit in turn
                      run_time=min(2.6, c.until("time", floor=0.5) - 0.05))

            def light(i):
                anims = [Transform(contents[i], fulls[i]), restyle(rects[i], outline=YELLOW, width=3)]
                if i > 0:
                    anims.append(restyle(rects[i - 1], outline=DIM, width=2))
                return anims

            c.wait_until("time")
            self.play(*light(0), run_time=1.2)
            c.wait_until("set-up time")
            self.play(FlashAround(Wd.band, color=GOLD, time_width=1.5, buff=0.06), run_time=1.2)
            c.wait_until("sync")
            self.play(*light(1), run_time=1.2)
            c.wait_until(own_word=years)
            self.play(*appear(years), run_time=1.0)
            c.wait_until("stages")
            self.play(*light(2), run_time=1.2)
            c.wait_until("independent")
            self.play(restyle(rects[2], outline=DIM, width=2), run_time=min(1.0, c.until(floor=0.4)))

    # ------------------------------------------------------------------ next: Lecture 9
    def clip4(self):
        head = T("Next: Lecture 9", 44).move_to(_p(0, 3.2))
        sub = T("Digital Electronics: Sequential Logic", 30, DIM).move_to(_p(0, 2.35))
        title = T("Synchronous State Machines 1", 48, YELLOW).move_to(_p(0, 1.65))

        S, chains, src, _M = H11.hook_counter()
        for f in S.ffs:
            f.remove(f.d_l, f.q_l, f.qb_l)
        leds = [ch.led for ch in chains]
        for l in leds:
            l.on = False
            l.set_stroke(DIM, 3).set_fill(BG, 0)
        ctr = VGroup(*S.ffs, S.bus, *S.jdots, *S.risers, S.loop, S.xor, *S.xor_stubs, S.block, S.block_out,
                     *S.block_stubs, *[m for ch in chains for m in (ch.res, ch.link, ch.led)], src)
        fit(ctr, 5.4, 2.9, _p(-3.4, -0.75))
        thin(ctr, 0.7)
        subset = T("(of which counters are a subset)", 30, DIM).next_to(ctr, DOWN, buff=0.3)
        machines = [RoundedRectangle(width=2.4, height=2.0, corner_radius=0.2).set_stroke(BLUE, 3)
                    .move_to(_p(x, -0.75)) for x in (2.0, 5.0)]
        qs = [T("?", 56, GOLD).move_to(m) for m in machines]

        with self.say("c7.recap.4") as c:
            c.wait_until("next")
            sweep_clear(self, *during(appear(head, sub, title, shift=None, lag=0.3), 0.5, 1.0), run_time=1.8)

            c.wait_until("counters")
            self.play(FadeIn(ctr), *during(appear(subset, shift=None), 0.4, 1.0), run_time=1.2)  # early: the slide's aside, said as "one special case"
            self.n = 0

            def step():
                self.n = (self.n + 1) % 8
                return [H11.set_led(l, bool(self.n >> i & 1)) for i, l in enumerate(leds)]

            while c.until("types", floor=0.0) > 1.0:
                self.play(*step(), run_time=0.4)
                self.wait(0.45)
            c.wait_until("types")
            self.play(*[FadeIn(m) for m in machines], *during(step(), 0.6, 1.0), run_time=1.0)
            c.wait_until("two popular kinds")
            self.play(*appear(*qs, shift=None, lag=0.4), *during(step(), 0.6, 1.0), run_time=1.0)
            while c.until(floor=0.0) > 0.9:
                self.wait(0.45)
                self.play(*step(), run_time=0.4)
