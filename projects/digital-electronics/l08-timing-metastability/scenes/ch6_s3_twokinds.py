"""Chapter 6, scene 3: two kinds of parallelism (spatial, temporal) and the cookie picture. Clips c6.kinds.1 – c6.kinds.3."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# system_hero(): the chapter-wide system box and task squares (copied from ch6_s1_hook.py).
# box 4.4 x 1.8, r 0.25, FG stroke 4, no fill, centre (0, 0.3), "the system" FG 36 at its centre;
# task squares side 0.5, r 0.1, fill 0.85, no stroke, task 1 BLUE, 2 GREEN, 3 TEAL, 4 FG.
# =============================================================================================
SYS_C = _p(0, 0.3)
SYS_W, SYS_H = 4.4, 1.8
TASK_COLORS = [BLUE, GREEN, TEAL, FG]


def system_box():
    box = RoundedRectangle(width=SYS_W, height=SYS_H, corner_radius=0.25).set_stroke(FG, 4).set_fill(opacity=0)
    box.move_to(SYS_C)
    label = T("the system", 36, FG).move_to(SYS_C)
    return box, label


def task_square(n):
    """Task n (1-based): BLUE, GREEN, TEAL, FG, repeating."""
    s = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.1).set_stroke(width=0)
    s.set_fill(TASK_COLORS[(n - 1) % 4], 0.85)
    return s
# =============================================================================================

# s2's end shot (ch6_s2_speed.py, clip 3)
S2_BOX_C, S2_LAB_C = _p(0, -1.6), _p(0, -1.1)
S2_PAR_C = _p(0, 2.6)

# this scene's two columns
COL = (-3.55, 3.55)
HEAD_Y = 2.3
SMALL_W, SMALL_H = 3.4, 1.4          # a system box in a column
SP_Y = (1.05, -0.55)                 # spatial: the two copies
ST_Y = 0.25                          # temporal: the stage row
ST_X = (COL[1] - 0.9, COL[1] + 0.9)  # stage 1, stage 2 centres
ST_W = 1.6


def slot_shape(w, h, x, y):
    return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=0.2),
                          num_dashes=40).set_stroke(BLUE, 3).move_to(_p(x, y))


def small_box(x, y, color=FG, w=SMALL_W):
    return RoundedRectangle(width=w, height=SMALL_H, corner_radius=0.2).set_stroke(color, 4) \
        .set_fill(color, 0).move_to(_p(x, y))


# ---- cookie icons ---------------------------------------------------------------------------
def tray(color):
    base = RoundedRectangle(width=1.8, height=0.16, corner_radius=0.06).set_stroke(DIM, 3).set_fill(DIM, 0.3)
    dough = [Circle(radius=0.2).set_stroke(width=0).set_fill(color, 0.85).move_to(_p(x, 0.28))
             for x in (-0.55, 0, 0.55)]
    return VGroup(base, *dough)


def rolling_pin():
    body = RoundedRectangle(width=1.4, height=0.32, corner_radius=0.15).set_stroke(FG, 3).set_fill(GOLD, 0.35)
    hl = Line(_p(-0.7, 0), _p(-1.0, 0)).set_stroke(FG, 5)
    hr = Line(_p(0.7, 0), _p(1.0, 0)).set_stroke(FG, 5)
    return VGroup(body, hl, hr)


def oven():
    body = RoundedRectangle(width=2.4, height=1.9, corner_radius=0.15).set_stroke(FG, 4).set_fill(opacity=0)
    window = Rectangle(width=1.5, height=0.95).set_stroke(FG, 3).set_fill(BG, 0).move_to(_p(-0.25, -0.15))
    d1 = Circle(radius=0.13).set_stroke(FG, 3).move_to(_p(0.8, 0.4))
    d2 = Circle(radius=0.13).set_stroke(FG, 3).move_to(_p(0.8, -0.05))
    tick = Line(_p(0.8, 0.4), _p(0.8, 0.5)).set_stroke(FG, 3)
    g = VGroup(body, window, d1, d2, tick)
    g.window = window
    return g


PIC_S = 1.4                          # the cookie picture's scale
ST_X_ROLL, OV_X = -1.8 * PIC_S, 1.8 * PIC_S


def row_parts(row_y, tray_color, with_labels=True):
    """One baker: a rolling pin at the roll station, an oven, the arrow between (scaled by PIC_S)."""
    pin = rolling_pin().scale(PIC_S).move_to(_p(ST_X_ROLL, row_y + 0.25 * PIC_S))
    ov = oven().scale(PIC_S).move_to(_p(OV_X, row_y))
    arr = Arrow(_p(-0.65 * PIC_S, row_y), _p(0.5 * PIC_S, row_y), buff=0, stroke_width=3, color=DIM,
                max_tip_length_to_length_ratio=0.3)
    tr = baked_tray(tray_color, row_y)
    labs = None
    if with_labels:
        labs = (T("roll", 36).move_to(_p(ST_X_ROLL, row_y + 1.65)),
                T("bake", 36).move_to(_p(OV_X, row_y + 1.65)))
    return pin, ov, arr, tr, labs


def baked_tray(color, row_y):
    return tray(color).scale(PIC_S).move_to(_p(ST_X_ROLL, row_y - 0.22 * PIC_S))


def in_window(tr, ov):
    return tr.copy().scale(0.72).move_to(ov.window.get_center() + 0.12 * PIC_S * DOWN)


class TwoKinds(NarratedScene):
    def construct(self):
        # ---- s2's end shot fades back in
        box = RoundedRectangle(width=SYS_W, height=SYS_H, corner_radius=0.25).set_stroke(FG, 4) \
            .set_fill(opacity=0).move_to(S2_BOX_C)
        lab = T("the system", 36, FG).move_to(S2_LAB_C)
        par = T("parallelism", 48, color=BLUE).move_to(S2_PAR_C)
        slots, nums, legs = [], [], []
        for k, x in enumerate((-2.3, 2.3)):
            s = slot_shape(3.6, 1.4, x, 0.9)
            slots.append(s)
            nums.append(T(str(k + 1), 36, color=DIM).move_to(s))
            legs.append(Line(par.get_bottom() + 0.12 * DOWN + 0.4 * x / 2.3 * RIGHT,
                             s.get_top() + 0.08 * UP).set_stroke(DIM, 3))
        self.play(*[FadeIn(m) for m in (box, lab, par, *slots, *nums, *legs)], run_time=1.0)  # early: s2's end shot fades back in

        # ---------------------------------------------------------------- clip 1: spatial
        with self.say("c6.kinds.1") as c:
            par_t = par.copy().scale(44 / 48).move_to(_p(0, 3.25))
            heads = [slot_shape(4.2, 0.9, x, HEAD_Y) for x in COL]
            new_legs = [Line(par_t.get_bottom() + 0.1 * DOWN + 0.5 * np.sign(x) * RIGHT,
                             h.get_top() + 0.06 * UP).set_stroke(DIM, 3) for x, h in zip(COL, heads)]
            box_a = small_box(COL[0], SP_Y[0])
            lab_pos = _p(COL[0] - 0.4, SP_Y[0])
            self.play(Transform(par, par_t),
                      *[Transform(s, h) for s, h in zip(slots, heads)],
                      *[Transform(l, nl) for l, nl in zip(legs, new_legs)],
                      *[n.animate.move_to(h) for n, h in zip(nums, heads)],
                      Transform(box, box_a), lab.animate.scale(30 / 36).move_to(lab_pos),
                      run_time=1.4)
            sp_title = T("spatial", 40).move_to(slots[0])
            self.play(*swap(nums[0], sp_title), run_time=1.0)

            # "Provide multiple copies": a second box comes out underneath
            box_b = small_box(COL[0], SP_Y[1])
            lab_b = lab.copy().move_to(_p(COL[0] - 0.4, SP_Y[1]))
            c.wait_until("multiple copies")
            self.play(TransformFromCopy(box, box_b), time_span(FadeIn(lab_b), 0.9, 1.5), run_time=1.5)

            # "multiple tasks": one square in each
            sq = [task_square(1).move_to(_p(COL[0] + 1.15, SP_Y[0])),
                  task_square(2).move_to(_p(COL[0] + 1.15, SP_Y[1]))]
            c.wait_until("multiple tasks")
            self.play(*[FadeIn(s, scale=0.6) for s in sq], run_time=1.0)

            # {copies}: both exit together; the rate and the cost
            rate = T("2 tasks every 10 ns", 34, GOLD).move_to(_p(COL[0], -1.85))
            cost = T("× 2 hardware", 34, GOLD).move_to(_p(COL[0], -2.75))
            cost_fr = SurroundingRectangle(cost, buff=0.16, corner_radius=0.1).set_stroke(GOLD, 2)
            c.wait_until("copies")
            self.play(*[s.animate.shift(1.4 * RIGHT).set_opacity(0) for s in sq], run_time=1.2)
            self.remove(*sq)
            c.wait_until(own_word=rate)
            self.play(*appear(rate), run_time=1.0)
            c.wait_until("you pay")
            self.play(*appear(cost), GrowFromCenter(cost_fr), run_time=1.0)  # early: the cost tag lands on "you pay"

        # ---------------------------------------------------------------- clip 2: temporal
        with self.say("c6.kinds.2") as c:
            tp_title = T("temporal", 40).move_to(slots[1])
            whole = small_box(COL[1], ST_Y)
            self.play(*swap(nums[1], tp_title), time_span(Create(whole), 0.3, 1.3), run_time=1.3)

            # "sequential stages": a cut down the middle, two half boxes
            cut = DashedLine(_p(COL[1], ST_Y + 0.9), _p(COL[1], ST_Y - 0.9), dash_length=0.12).set_stroke(YELLOW, 3)
            st = [small_box(x, ST_Y, BLUE, w=ST_W) for x in ST_X]
            st_lab = [T(f"stage {k + 1}", 30).move_to(_p(x, ST_Y + 0.35)) for k, x in enumerate(ST_X)]
            c.wait_until("Break each task")
            self.play(Create(cut), run_time=1.0)
            c.wait_until("sequential stages")
            self.play(ReplacementTransform(whole, st[0]), ReplacementTransform(whole.copy(), st[1]),
                      FadeOut(cut), run_time=1.3)
            self.play(*appear(*st_lab, lag=0.3), run_time=1.0)  # early: both stage names land on "stages"

            # {spread}: task 1 moves on to stage 2 as task 2 enters stage 1
            sq_y = ST_Y - 0.25
            t1 = task_square(1).move_to(_p(ST_X[0] - 1.45, sq_y))
            t2 = task_square(2).move_to(_p(ST_X[0] - 1.45, sq_y))
            c.wait_until("spread")
            self.play(FadeIn(t1), run_time=0.4)
            self.play(t1.animate.move_to(_p(ST_X[0], sq_y)), run_time=1.0)
            self.play(t1.animate.move_to(_p(ST_X[1], sq_y)), time_span(FadeIn(t2), 0, 0.4),
                      t2.animate.move_to(_p(ST_X[0], sq_y)), run_time=1.5)

            # {through}: task 1's route, stage 1 then stage 2
            route = Arrow(_p(ST_X[0] - 0.8, ST_Y - 1.0), _p(ST_X[1] + 0.8, ST_Y - 1.0), buff=0,
                          stroke_width=3, color=BLUE, max_tip_length_to_length_ratio=0.08)
            c.wait_until("through")
            self.play(GrowArrow(route), run_time=2.0, rate_func=linear)

            # {overlap}: both stages lit at once, each with its own colour
            c.wait_until("overlap")
            self.play(st[0].animate.set_fill(GREEN, 0.22), st[1].animate.set_fill(BLUE, 0.22),
                      *flash(st, color=YELLOW), run_time=1.5)

            # {pipelining}
            pl_a = T("temporal parallelism", 32).move_to(_p(COL[1], -1.4))
            pl_b = T("= pipelining", 40, YELLOW).move_to(_p(COL[1], -1.95))
            c.wait_until("pipelining")
            self.play(*appear(pl_a, pl_b, lag=0.4), run_time=1.3)

            # {attractive}
            good = T("more throughput, same hardware", 32, GREEN).move_to(_p(COL[1], cost.get_y()))
            c.wait_until("attractive")
            self.play(*appear(good), run_time=1.2)  # early: the gain, spelled out as "attractive" is said
            c.wait_until("busy")
            self.play(*flash(st, color=YELLOW), run_time=min(1.5, c.until(None)))

        # ---------------------------------------------------------------- clip 3: cookies
        with self.say("c6.kinds.3") as c:
            # {bake}: the board clears; the two slots shrink to the top, dimmed
            heads_top = [(slots[0], sp_title, -4.6), (slots[1], tp_title, 4.6)]
            content = [m for m in self.mobjects
                       if m not in (slots[0], slots[1], sp_title, tp_title)]
            moves = []
            for s, t, x in heads_top:
                moves += [s.animate.scale(0.75).move_to(_p(x, 3.15)).set_stroke(opacity=0.4),
                          t.animate.scale(0.75).move_to(_p(x, 3.15)).set_opacity(0.4)]
            self.play(*during(disappear(*content), 0, 0.45), *during(moves, 0.3, 1), run_time=1.5)

            row0 = -0.35
            pin1, ov1, arr1, tr1, (l_roll, l_bake) = row_parts(row0, BLUE)
            c.wait_until("trays of cookies")
            self.play(FadeIn(tr1, shift=0.2 * DOWN), FadeIn(ov1), run_time=1.2)

            # "roll out a tray": the pin rolls it
            c.wait_until("roll out")
            self.play(FadeIn(pin1, shift=0.2 * DOWN), *appear(l_roll), run_time=1.0)
            self.play(pin1.animate(rate_func=there_and_back).shift(0.45 * PIC_S * RIGHT), run_time=1.0)

            # "in the oven": the tray goes in, and bakes (BLUE glow)
            c.wait_until("in the oven")
            self.play(Transform(tr1, in_window(tr1, ov1), path_arc=-0.6), GrowArrow(arr1),
                      ov1.window.animate.set_fill(BLUE, 0.3), *appear(l_bake), run_time=1.3)  # early: "bake" names the oven step as it is said

            # {oven}: a second baker and a second oven, alongside
            up = 1.2 * UP                        # row 1 to y 0.85, row 2 at -2.05
            row1 = [pin1, ov1, arr1, tr1, l_roll, l_bake]
            pin2, ov2, arr2, tr2, _ = row_parts(row0 - 1.7, GREEN, with_labels=False)
            tr2_in = in_window(tr2, ov2)
            ov2.window.set_fill(GREEN, 0.3)
            c.wait_until("a friend")
            self.play(*[m.animate.shift(up) for m in row1], run_time=1.2)
            c.wait_until("second oven")
            self.play(*appear(pin2, ov2, arr2, tr2_in, lag=0.15, shift=None), run_time=1.3)
            sp_tag = T("spatial", 36, BLUE).move_to(_p(-5.5, row0 - 0.1))
            c.wait_until("alongside")
            self.play(*fly(sp_title, sp_tag), slots[0].animate.set_stroke(opacity=1),
                      sp_title.animate.set_opacity(1), run_time=1.5)

            # {tray}: back to one oven; tray 2 rolled while tray 1 bakes
            row2 = [pin2, ov2, arr2, tr2_in]
            c.wait_until("tray")
            self.play(*during(disappear(*row2, sp_tag), 0, 0.45),
                      *during([m.animate.shift(-up) for m in row1]
                              + [slots[0].animate.set_stroke(opacity=0.4), sp_title.animate.set_opacity(0.4)],
                              0.35, 1), run_time=1.5)
            tr3 = baked_tray(GREEN, row0)
            self.play(FadeIn(tr3, shift=0.2 * DOWN), run_time=0.6)
            self.play(pin1.animate(rate_func=there_and_back).shift(0.45 * PIC_S * RIGHT),
                      ov1.window.animate.set_fill(BLUE, 0.45), run_time=1.0)
            # centred under the whole roll -> bake picture: both steps busy at once
            tp_tag = T("temporal", 36, BLUE).move_to(_p(0, ov1.get_bottom()[1] - 0.6))
            c.wait_until("temporal")
            # the header stays dim and small, so only the tag reads as "temporal"
            self.play(*fly(tp_title, tp_tag, arc=PI / 6), run_time=1.5)

            # "Both steps are busy at once"
            c.wait_until("both steps")
            self.play(FlashAround(VGroup(pin1, tr3), color=YELLOW, run_time=1.5, time_width=1.5),
                      FlashAround(ov1, color=YELLOW, run_time=1.5, time_width=1.5), run_time=1.5)

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
