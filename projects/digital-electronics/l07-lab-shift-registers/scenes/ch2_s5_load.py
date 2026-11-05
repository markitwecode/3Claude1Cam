"""Chapter 2, scene 5: preset and clear load a word in parallel; clocking shifts it out serially.
Clips c2.load.1 – c2.load.3.

Opens on ch2_s4_demo.handover_shot(); IC1a's flip-flop (shot part 10) is kept and enlarged.
Async pins: L6 ch3_s6's RED style (L8 ch2_s3's pin()). Chain: L8 ch2_s3's build_chain()/pin()/
digit_pos(), FF names dropped to make room for the PRE pins. Ends on an empty frame (s6 opens empty).
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _load_l8():
    path = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch2_s3_shiftreg.py"
    spec = importlib.util.spec_from_file_location("_l08_ch2_s3_shiftreg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8 = _load_l8()


def _p(x, y):
    return np.array([x, y, 0.0])


def wave(x0, x1, y, edges, color, start_high=False, h=0.4, slope=0.2):
    lo, hi = y - h / 2, y + h / 2
    level = hi if start_high else lo
    pts = [_p(x0, level)]
    for xc in edges:
        other = hi if level == lo else lo
        pts += [_p(xc - slope / 2, level), _p(xc + slope / 2, other)]
        level = other
    pts.append(_p(x1, level))
    m = VMobject().set_points_as_corners(pts).set_stroke(color, 4)
    m.corners = pts
    return m


def clr_pin(ff, length=0.3):
    """L8's CLR pin, shortened and its label raised so both stay well clear of the CLK bus."""
    c, hb = ff.box.get_center(), ff.box.height / 2
    a = c + 0.33 * RIGHT + hb * DOWN
    w = Line(a, a + length * DOWN).set_stroke(RED, 5)
    lab = T("CLR", 28, RED).next_to(w, RIGHT, buff=0.08)
    return w, lab


def reveal_to(m, xa, xb):
    return L8.reveal(m, xa, xb)


# ── clip 1 layout ────────────────────────────────────────────────────────────────
BIG = 2.3
BIG_AT = _p(-3.6, 0.2)
TX0, TX1 = 0.6, 5.8
ROW_Y = {"CLK": 2.0, "CLR": 1.1, "PRE": 0.2, "Q": -0.7}
CLR_E, PRE_E = 1.4, 4.4
PULSE = 0.8
SPLIT = 3.6

# ── chain layout ─────────────────────────────────────────────────────────────────
FY = 0.35
TRACE_Y = -2.0
EDGES = [-2.2, -0.2, 1.8]
SLOTS = [5.2, 5.7, 6.2]
TAG_Y = -2.85
# where each clocking step's trace reveal starts/ends, chosen so each rising edge lands at 0.3 of
# its play, when the bits start to move: xa = E - (0.3 / 0.7)(xb - E), working back from 3.2
REV = [3.2]
for _e in reversed(EDGES):
    REV.insert(0, _e - 0.3 / 0.7 * (REV[0] - _e))


class LoadParallel(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(4.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.load.1
    def clip1(self):
        shot = load_scene("ch2_s4_demo").handover_shot()
        self.add(*shot)
        sim, ff = shot[1], shot[10]
        with self.say("c2.load.1", gap=0.8) as c:
            # {back}: the drawing clears to IC1a's flip-flop, enlarged
            c0 = ff.box.get_center()
            sweep_clear(self, ff.animate.scale(BIG, about_point=c0).shift(BIG_AT - c0),
                        sim.animate.to_corner(UR, buff=0.5), keep=[ff, sim], run_time=2.0)
            q = T("1", 64, GOLD).move_to(L8.digit_pos(ff))
            self.play(*appear(q, shift=None), run_time=0.8)
            c.wait_until("pins")

            # {pins}: PRE on top, CLR underneath
            bx = ff.box
            pre_w = Line(bx.get_top(), bx.get_top() + 0.6 * UP).set_stroke(RED, 6)
            pre_l = T("PRE", 36, RED).next_to(pre_w, UP, buff=0.1)
            a = bx.get_bottom() + 0.5 * RIGHT
            clr_w = Line(a, a + 0.6 * DOWN).set_stroke(RED, 6)
            clr_l = T("CLR", 36, RED).next_to(clr_w.get_end(), RIGHT, buff=0.12)
            self.play(GrowFromEdge(pre_w, DOWN), GrowFromEdge(clr_w, UP),
                      *during(appear(pre_l, clr_l, lag=0.2), 0.4, 1.0), run_time=1.5)
            asyn = T("asynchronous", 34, RED).move_to(_p(BIG_AT[0], -3.0))
            c.wait_until("pins", own_word=asyn)
            self.play(*appear(asyn), run_time=1.0)
            c.wait_until("preset and clear")

            # row labels for the timing view
            labs = {k: T(k, 32, col).next_to(_p(TX0 - 0.15, y), LEFT, buff=0)
                    for (k, y), col in zip(ROW_Y.items(), (YELLOW, RED, RED, GREEN))}
            rows = {
                "CLK": wave(TX0, TX1, ROW_Y["CLK"], [], YELLOW),
                "CLR": wave(TX0, TX1, ROW_Y["CLR"], [CLR_E, CLR_E + PULSE], RED),
                "PRE": wave(TX0, TX1, ROW_Y["PRE"], [PRE_E, PRE_E + PULSE], RED),
                "Q": wave(TX0, TX1, ROW_Y["Q"], [CLR_E, PRE_E], GREEN, start_high=True),
            }
            for m in rows.values():
                L8.cut(m, TX0 + 0.01)
            self.add(*rows.values())
            self.play(*appear(*labs.values(), lag=0.2, shift=None), run_time=1.2)
            c.wait_until("force")

            # {force}: CLR pulses, Q drops to 0 at once; the clock stays flat
            f0 = (CLR_E - TX0) / (SPLIT - TX0)
            q0 = T("0", 64, GOLD).move_to(q)
            self.play(*[reveal_to(m, TX0, SPLIT) for m in rows.values()],
                      *during(VShowPassingFlash(clr_w.copy().set_stroke(YELLOW, 10), time_width=0.6), f0 - 0.15, f0 + 0.15),
                      *during(FadeOut(q, shift=0.2 * UP), f0, f0 + 0.15),
                      *during(FadeIn(q0, shift=0.2 * UP), f0 + 0.17, f0 + 0.35),
                      run_time=max(2.0, min(2.6, c.until("and preset"))))
            c.wait_until("and preset")
            f1 = (PRE_E - SPLIT) / (TX1 - SPLIT)
            q1 = T("1", 64, GOLD).move_to(q)
            self.play(*[reveal_to(m, SPLIT, TX1) for m in rows.values()],
                      *during(VShowPassingFlash(pre_w.copy().set_stroke(YELLOW, 10), time_width=0.6), f1 - 0.15, f1 + 0.15),
                      *during(FadeOut(q0, shift=0.2 * UP), f1, f1 + 0.15),
                      *during(FadeIn(q1, shift=0.2 * UP), f1 + 0.17, f1 + 0.35),
                      run_time=max(2.0, min(2.6, c.until("at once"))))
            noclk = T("no clock edge needed", 34, YELLOW).move_to(_p((TX0 + TX1) / 2 - 0.3, -1.9))
            c.wait_until(own_word=noclk)
            self.play(*appear(noclk), *flash([rows["CLK"]], color=YELLOW), run_time=1.2)
            c.wait_until("start")

            # {start}: L6 ch3's preview: three CLR pins on one RED line
            boxes = [Rectangle(width=0.85, height=1.1).set_stroke(FG, 3).move_to(_p(x, 1.25))
                     for x in (1.6, 3.2, 4.8)]
            stubs = [Line(b.get_bottom(), _p(b.get_x(), 0.2)).set_stroke(RED, 5) for b in boxes]
            bar = Line(_p(1.0, 0.2), _p(4.8, 0.2)).set_stroke(RED, 5)
            bar_l = T("CLR", 30, RED).next_to(bar, LEFT, buff=0.15)
            mini = [*boxes, *stubs, bar, bar_l]
            old = [*rows.values(), *labs.values()]
            self.play(*during([FadeOut(m) for m in old], 0, 0.45),
                      *during(appear(*mini, shift=None, lag=0.05), 0.5, 1.0), run_time=1.1)
            zeros = [T("0", 40, GOLD).move_to(b) for b in boxes]
            self.play(VShowPassingFlash(bar.copy().set_stroke(YELLOW, 9), time_width=0.6),
                      *during(appear(*zeros, shift=None, lag=0), 0.5, 1.0), run_time=1.1)
            known = T("known start state", 34, GREEN).move_to(_p(3.2, -0.75))
            c.wait_until(own_word=known)
            self.play(*appear(known), run_time=min(1.0, c.until(floor=0.5)))

    # ------------------------------------------------------------------ c2.load.2
    def clip2(self):
        C = L8.build_chain(fy=FY)
        self.C = C
        pins, plabs = {}, {}
        for i, f in enumerate(C.ffs):
            for kind in ("PRE", "CLR"):
                w, lab = L8.pin(f, kind) if kind == "PRE" else clr_pin(f)
                pins[(i, kind)], plabs[(i, kind)] = w, lab
        self.pins, self.plabs = pins, plabs
        qy = C.qy
        self.din0 = T("0", 40, DIM).move_to(_p(C.ffs[0].d_w.get_start()[0] + 0.15, qy - 0.38))
        parts = [*C.ffs, *C.links, C.tail, *C.risers, *C.dots, *C.qls, C.din,
                 C.bus, *C.jdots, *C.clk_ws, C.clk_l, *pins.values(), *plabs.values()]
        with self.say("c2.load.2") as c:
            # {second}: the three-flip-flop chain, each box with PRE and CLR
            c.wait_until("use")
            sweep_clear(self, *appear(*parts, shift=None, lag=0.01), run_time=1.6)
            self.play(*appear(self.din0, shift=None), run_time=0.8)
            c.wait_until("load")

            # {load}: the word to load
            word = MathTex(r"D_0\,D_1\,D_2", "=", r"1\;1\;0", font_size=52).move_to(_p(-0.2, 2.85))
            word[0].set_color(BLUE)
            word[2].set_color(GOLD)
            self.word = word
            self.play(*appear(word), run_time=1.0)
            c.wait_until("clear each")
            unused = [pins[(0, "CLR")], plabs[(0, "CLR")], pins[(1, "CLR")], plabs[(1, "CLR")],
                      pins[(2, "PRE")], plabs[(2, "PRE")]]
            self.play(*set_alpha(unused, DIMMED), run_time=1.0)
            c.wait_until("same moment")

            # all at once: PRE on FF0 and FF1, CLR on FF2; the digits appear together
            used = [(0, "PRE"), (1, "PRE"), (2, "CLR")]
            digs = [L8.digit(s, f) for s, f in zip("110", C.ffs)]
            self.digs = digs
            self.play(*[VShowPassingFlash(pins[k].copy().set_stroke(YELLOW, 9), time_width=0.8) for k in used],
                      *flash([plabs[k] for k in used], color=YELLOW),
                      *during(appear(*digs, shift=None, lag=0), 0.4, 1.0), run_time=1.6)
            c.wait_until("word")

            # {word}: the three digits pulse
            self.play(*flash(digs, color=GOLD, run_time=1.5, time_width=1.5),
                      *set_alpha(unused, 1), run_time=1.5)
            c.wait_until("parallel")

            # {parallel}
            self.tag = T("parallel in", 36, YELLOW)
            self.tag.move_to(_p(-5.0 + self.tag.width / 2, TAG_Y))
            c.wait_until(own_word=self.tag)
            self.play(*appear(self.tag), run_time=1.0)

    # ------------------------------------------------------------------ c2.load.3
    def clip3(self):
        C, digs = self.C, self.digs
        pos = [L8.digit_pos(f) for f in C.ffs]
        with self.say("c2.load.3") as c:
            # {shift}: a small clock trace under the chain, a queue to the right of Q_2
            clk = wave(-3.6, 3.2, TRACE_Y, [e for x in EDGES for e in (x, x + 0.9)], YELLOW, h=0.36)
            L8.cut(clk, -3.59)
            self.add(clk)
            qbox = DashedVMobject(Rectangle(width=1.8, height=0.75).move_to(_p(5.7, pos[2][1])),
                                  num_dashes=30).set_stroke(DIM, 3)
            clk_tl = T("CLK", 30, YELLOW).next_to(_p(-3.75, TRACE_Y), LEFT, buff=0)
            self.play(reveal_to(clk, -3.6, REV[0]), FadeIn(qbox),
                      *appear(clk_tl, shift=None), run_time=1.5)
            c.wait_until("way")

            # {way}: Q_2 is the way out; it shows the 0
            out_path = VMobject().set_points_as_corners(
                [C.ffs[2].q_w.get_start(), C.tail.get_end(), C.risers[2].get_end()])
            self.play(VShowPassingFlash(out_path.set_stroke(YELLOW, 10), time_width=0.6),
                      *flash([C.qls[2]], color=YELLOW), *flash([digs[2]], color=GOLD), run_time=1.6)
            c.wait_until("e1")

            queue = []
            entering = []
            for k in range(3):
                rt = 2.0 if k == 0 else 1.2
                new0 = T("0", 40, DIM).move_to(pos[0])
                out = digs[2]
                xa, xb = REV[k], REV[k + 1]
                fe = (EDGES[k] - xa) / (xb - xa)          # the trace's rising edge: 0.3 of the play
                anims = [reveal_to(clk, xa, xb)]
                # the chain's own CLK bus flashes on the same rising edge
                anims += during([VShowPassingFlash(m.copy().set_stroke(FG, 9), time_width=0.6)
                                 for m in (C.bus, *C.clk_ws)], fe - 0.05, min(1.0, fe + 0.4))
                anims += during(out.animate.move_to(_p(SLOTS[0], pos[2][1])), 0.3, 1.0)
                anims += during([d.animate.shift(0.5 * RIGHT) for d in queue], 0.3, 0.7)
                anims += during(digs[1].animate.move_to(pos[2]), 0.3, 1.0)
                anims += during(digs[0].animate.move_to(pos[1]), 0.3, 1.0)
                anims += during(fly(self.din0, new0), 0.3, 1.0)
                self.play(*anims, run_time=rt)
                queue.insert(0, out)
                digs = [new0, digs[0], digs[1]]
                entering.append(new0)
                if k < 2:
                    c.wait_until(f"e{k + 2}")

            c.wait_until("piso")
            # {piso}: the word went in at once, came out one bit at a time
            # one small flash per digit, in the order they left, each inside the queue box
            self.play(*[during(FlashAround(d, color=GOLD, buff=0.06, time_width=1.0), i / 3, (i + 1) / 3)[0]
                        for i, d in enumerate(reversed(queue))], run_time=1.8)
            piso = T("parallel in, serial out", 36, YELLOW)
            piso.move_to(_p(-5.0 + piso.width / 2, TAG_Y))
            c.wait_until("that's parallel in")
            self.play(*edit(self.tag, piso), run_time=1.5)
            # the s4 counterpart, small and DIM, only once the main tag is written
            sipo = T("serial in, parallel out", 30, DIM)
            sipo.move_to(_p(6.4 - sipo.width / 2, TAG_Y))
            self.play(*appear(sipo, shift=None), run_time=1.0)
