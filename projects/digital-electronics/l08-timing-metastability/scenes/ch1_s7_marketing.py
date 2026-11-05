"""Chapter 1, scene 7: who sets the clock? Marketing fixes T_c, the logic gets what's left.
Clips c1.market.1 – c1.market.4."""
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


# ============================================================================
# THE lecture's budget bar (owned by ch1_s6; ch1_s7, ch1_s8, ch3, ch4, ch7 copy this block)
# ============================================================================
BAR_H = 0.5          # segment / outline height
BAR_FILL = 0.85      # segment fill opacity (no stroke)
BAR_OUT_W = 3        # YELLOW outline stroke


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
    """One clock period as a budget. `segs` = [(tex, colour, length), ...] laid flush left to right
    from x0 (they may run past the outline: a broken budget). `total` = the outline's length (one T_c).
    Returns VGroup(*segs, outline, *syms, tc, *nums) with
      .segs    Rectangles BAR_H tall, filled in their colour at BAR_FILL, no stroke (z 0)
      .outline YELLOW Rectangle, stroke BAR_OUT_W, no fill, x0 .. x0 + total (z 1, over the segments)
      .syms    MathTex(tex, sym_size) in the segment's colour, 0.15 above each segment ([] if not syms)
      .tc      MathTex(tc_tex, 44) YELLOW, 0.25 left of the outline
      .nums    GOLD T(text, num_size) 0.2 under each segment whose `nums` entry is not None"""
    g = VGroup()
    g.segs, g.syms, g.nums = [], [], []
    x = x0
    for tex, col, w in segs:
        r = Rectangle(width=w, height=BAR_H).set_stroke(width=0).set_fill(col, BAR_FILL)
        r.move_to([x + w / 2, y, 0])
        g.segs.append(r)
        x += w
    g.outline = Rectangle(width=total, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    g.outline.move_to([x0 + total / 2, y, 0]).set_z_index(1)
    if syms:
        for (tex, col, _), r in zip(segs, g.segs):
            g.syms.append(MathTex(tex, font_size=sym_size, color=col).next_to(r, UP, buff=0.15))
    g.tc = MathTex(tc_tex, font_size=44, color=YELLOW).next_to(g.outline, LEFT, buff=0.25)
    for txt, r in zip(nums or [], g.segs):
        if txt is not None:
            g.nums.append(T(txt, num_size, GOLD).next_to(r, DOWN, buff=0.2))
    g.add(*g.segs, g.outline, *g.syms, g.tc, *g.nums)
    return g
# ============================================================================


SEG_COLORS = (PINK, PURPLE, GOLD)
SEG_TEX = ("t_{pc}", "t_{pd}", "t_{su}")
SEG_OP = BAR_FILL


def padlock(scale=1.0):
    """Small dark padlock (body + shackle), drawn on top of a coloured segment."""
    body = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.2)
    body.set_fill(BG, 1).set_stroke(width=0)
    shackle = Arc(radius=0.085, start_angle=0, angle=PI).set_stroke(BG, 3.5)
    shackle.move_to(body.get_top() + 0.075 * UP)
    lock = VGroup(shackle, body)
    lock.scale(scale)
    return lock


def pcs_bar(pc, pd, su, tc, unit=1.0, x0=-3.3, y=0.8, tc_tex="T_c", syms=True, nums=None,
            locks=False, lock_scale=1.0, sym_size=40, num_size=34):
    """budget_bar with the three standard segments (durations times `unit`) and optional
    padlocks on t_pc and t_su (.locks, z 2)."""
    segs = [(t, col, w * unit) for t, col, w in zip(SEG_TEX, SEG_COLORS, (pc, pd, su))]
    g = budget_bar(segs, tc * unit, x0, y, tc_tex, syms=syms, nums=nums,
                   sym_size=sym_size, num_size=num_size)
    g.locks = []
    if locks:
        for r in (g.segs[0], g.segs[2]):
            g.locks.append(padlock(lock_scale).move_to(r).set_z_index(2))
        g.add(*g.locks)
    return g


def one_ns_bar(unit=7.5, left=-3.3, y=0.8, numbers=True):
    """The 1 ns budget: 0.2 + 0.7 + 0.1 ns, padlocks on t_pc and t_su, 'T_c = 1 ns' left.
    At 4+ units/ns: symbols above and GOLD '0.2', '0.7 ns', '0.1' under the segments; at smaller
    scales only '0.7 ns' under the slot (no symbols, no 0.2/0.1: they would crowd).
    Default: 7.5 units per ns, x -3.3 .. 4.2."""
    big = unit >= 4
    nums = None
    if numbers:
        nums = ["0.2", "0.7 ns", "0.1"] if big else [None, "0.7 ns", None]
    return pcs_bar(0.2, 0.7, 0.1, 1.0, unit=unit, x0=left, y=y, tc_tex=r"T_c = 1\,\text{ns}",
                   syms=big, nums=nums, locks=True, lock_scale=1.3 if big else 0.85,
                   sym_size=48 if big else 40, num_size=40 if big else 34)


def billboard(text):
    board = RoundedRectangle(corner_radius=0.12, width=3.9, height=1.4)
    board.set_stroke(FG, 3).set_fill(BG, 1)
    txt = T(text, 60, YELLOW, weight=BOLD).move_to(board)
    legs = VGroup(*[Line(board.get_bottom() + dx * RIGHT, board.get_bottom() + dx * RIGHT + 0.9 * DOWN)
                    for dx in (-1.0, 1.0)]).set_stroke(DIM, 6)
    g = VGroup(legs, board, txt)
    g.legs, g.board, g.txt = legs, board, txt
    return g


def colored_tex(parts, colors):
    m = MathTex(*parts, font_size=60)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


class Marketing(NarratedScene):
    def construct(self):
        FORM_Y = -2.4

        # ---------------------------------------------------------------- clip 1
        with self.say("c1.market.1") as c:
            quote = T("“Note that the clock period of a system\n"
                      "(i.e., the clock speed) is often set\n"
                      "by the marketing dept!”", 34, line_spacing=1.1)
            card = RoundedRectangle(corner_radius=0.15, width=quote.width + 0.8,
                                    height=quote.height + 0.8).set_stroke(DIM, 2)
            qcard = VGroup(card, quote).move_to([-2.05, 0, 0])
            bb = billboard("1 GHz!").scale(0.9).move_to([4.75, 0, 0])

            self.play(FadeIn(card), *appear(quote, shift=None), run_time=1.2)  # early: quote card shown whole
            c.wait_until("marketing department")
            mk = select(quote, "marketing dept!")[0]
            self.play(*recolor(mk, YELLOW), FlashUnder(mk, color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("billboard")
            self.play(*appear(bb), run_time=1.2)
            c.wait_until("gigahertz")
            self.play(FlashAround(bb.txt, run_time=1.5, time_width=1.5))

        # ---------------------------------------------------------------- clip 2
        with self.say("c1.market.2") as c:
            gen = pcs_bar(1.6, 5.0, 1.2, 7.8, unit=1.0, x0=-3.6, y=0.8, sym_size=48)
            sweep_clear(self, *[time_span(FadeIn(m), 0.6, 1.6) for m in [*gen.segs, gen.outline]],
                        *[time_span(FadeIn(m), 0.9, 1.8) for m in [*gen.syms, gen.tc]],
                        run_time=1.8)
            words = VGroup(
                Tex(r"``worst case values of ", r"$t_{pc}$", r" (i.e., max) and ", r"$t_{su}$",
                    r" (i.e., min)", font_size=40),
                Tex(r"are specified by the chip manufacturer''", font_size=40),
            ).arrange(DOWN, buff=0.18).move_to([0, 3.0, 0])
            words[0][1].set_color(PINK)
            words[0][3].set_color(GOLD)
            self.play(*appear(words, shift=None), run_time=1.0)  # early: the slide's words shown whole

            c.wait_until("maximum")
            lk_pc = padlock(1.3).move_to(gen.segs[0]).set_z_index(2)
            tag_max = T("max", 32, PINK).next_to(gen.segs[0], DOWN, buff=0.2)
            self.play(FadeIn(lk_pc, scale=1.4), *appear(tag_max), run_time=1.2)

            c.wait_until("minimum")
            lk_su = padlock(1.3).move_to(gen.segs[2]).set_z_index(2)
            tag_min = T("min", 32, GOLD).next_to(gen.segs[2], DOWN, buff=0.2)
            self.play(FadeIn(lk_su, scale=1.4), *appear(tag_min), run_time=1.2)

            c.wait_until("free")
            self.play(FlashAround(gen.segs[1], color=PURPLE, stroke_width=6, run_time=2, time_width=1.5),
                      *set_alpha([gen.segs[0], gen.segs[2]], 0.45), run_time=2)
            tag_des = T("the designer’s", 32, PURPLE).next_to(gen.segs[1], DOWN, buff=0.2)
            c.wait_until("designer")
            self.play(*appear(tag_des), run_time=1.0)

            c.wait_until("rearrange")
            rule = colored_tex(["T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}"],
                               {0: YELLOW, 2: PINK, 4: PURPLE, 6: GOLD}).move_to([0, FORM_Y, 0])
            self.play(*appear(rule), *set_alpha([gen.segs[0], gen.segs[2]], 1), run_time=1.2)
            c.wait_until("minus")
            rearr = colored_tex(["t_{pd}", r"\le", "T_c", "-", "(", "t_{pc}", "+", "t_{su}", ")"],
                                {0: PURPLE, 2: YELLOW, 5: PINK, 7: GOLD}).move_to([0, FORM_Y, 0])
            self.play(*edit(rule, rearr), run_time=2.0)

        # ---------------------------------------------------------------- clip 3
        with self.say("c1.market.3") as c:
            bb2 = billboard("1 GHz!").scale(0.62).move_to([5.3, 2.75, 0])
            sweep_clear(self, time_span(FadeIn(bb2, shift=0.25 * DOWN), 0.6, 1.4),
                        keep=[*gen.segs, gen.outline, *gen.syms, gen.tc, lk_pc, lk_su, rearr],
                        run_time=1.4)
            c.wait_until("one nanosecond")
            b1 = one_ns_bar(numbers=True)
            moves = [Transform(gen.segs[i], b1.segs[i]) for i in range(3)]
            moves += [Transform(gen.syms[i], b1.syms[i]) for i in range(3)]
            moves += [Transform(gen.outline, b1.outline), Transform(lk_pc, b1.locks[0]),
                      Transform(lk_su, b1.locks[1])]
            self.play(*moves, *during(swap(gen.tc, b1.tc), 0.4, 1), run_time=2.0)
            # from here on the bar's pieces are gen.* (now shaped like b1) plus b1.tc
            bar_segs, bar_syms, bar_out, bar_tc = gen.segs, gen.syms, gen.outline, b1.tc
            locks = [lk_pc, lk_su]

            c.wait_until("budget")
            n02, n07, n01 = b1.nums
            self.play(*appear(n02, n01, lag=0.2), *flash(locks, color=YELLOW), run_time=1.2)
            numeric = colored_tex(["t_{pd}", r"\le", "1", "-", "(", "0.2", "+", "0.1", ")",
                                   "=", r"0.7\,\text{ns}"],
                                  {0: PURPLE, 2: YELLOW, 5: PINK, 7: GOLD, 10: PURPLE}).move_to([0, FORM_Y, 0])
            self.play(*edit(rearr, numeric), run_time=1.6)
            c.wait_until("zero point seven")
            self.play(*appear(n07), FlashAround(bar_segs[1], color=PURPLE, run_time=1.5, time_width=1.5),
                      run_time=1.5)

            c.wait_until("compare")
            b2 = one_ns_bar(unit=2.0, left=-3.5)
            # at 2 units/ns only "0.7 ns" stays (symbols and 0.2 / 0.1 would crowd)
            moves = [Transform(bar_segs[i], b2.segs[i]) for i in range(3)]
            moves += [Transform(n07, b2.nums[0])]
            moves += [Transform(bar_out, b2.outline), Transform(lk_pc, b2.locks[0]),
                      Transform(lk_su, b2.locks[1]), Transform(bar_tc, b2.tc)]
            self.play(*during(disappear(*bar_syms, n02, n01), 0, 0.4), *moves, run_time=1.5)

            x0 = b2.segs[1].get_left()[0]
            cy = -0.45
            cmp_ok = Rectangle(width=0.7 * 2.0, height=BAR_H).set_fill(PURPLE, SEG_OP).set_stroke(width=0)
            cmp_ok.move_to([x0 + 0.7, cy, 0])
            cmp_bad = Rectangle(width=4.0 * 2.0, height=BAR_H).set_fill(RED, SEG_OP).set_stroke(width=0)
            cmp_bad.move_to([x0 + 1.4 + 4.0, cy, 0]).set_z_index(-1)   # under cmp_ok, t_su and the locks
            lab47 = MathTex(r"4.7\,\text{ns}", font_size=48, color=GOLD).next_to(cmp_ok, LEFT, buff=0.35)
            c.wait_until("four point seven")
            self.play(GrowFromEdge(cmp_ok, LEFT), *appear(lab47, shift=None), run_time=0.8)
            self.play(GrowFromEdge(cmp_bad, LEFT), run_time=2.0, rate_func=linear)
            tag67 = MathTex(r"\approx 6.7\,\times", font_size=56, color=YELLOW).next_to(cmp_bad, DOWN, buff=0.3)
            c.wait_until("seven times")
            self.play(*appear(tag67), FlashAround(cmp_bad, color=RED, run_time=1.5, time_width=1.5),
                      run_time=1.5)

        # ---------------------------------------------------------------- clip 4
        with self.say("c1.market.4", gap=5.5) as c:
            br1 = T("redesign the logic", 34, PURPLE).move_to([-3.2, FORM_Y, 0])
            self.play(*during(disappear(numeric), 0, 0.45), *during(appear(br1), 0.5, 1),
                      run_time=1.2)
            squeezed = cmp_bad.copy().stretch_to_fit_width(1.6 * 2.0, about_edge=LEFT)
            full_bad = cmp_bad.copy()
            self.play(Transform(cmp_bad, squeezed), *set_alpha([lab47, tag67], DIMMED), run_time=2.0)

            c.wait_until("can't get there")
            xm = cross_mark().next_to(br1, RIGHT, buff=0.3)
            self.play(Transform(cmp_bad, full_bad), *set_alpha([lab47, tag67], 1), run_time=1.5)
            self.play(FadeIn(xm, scale=1.3), *set_alpha([br1], 0.4), *disappear(tag67), run_time=1.0)

            c.wait_until("grow")
            br2 = Tex(r"increase $T_c$", font_size=40, color=YELLOW).move_to([3.2, FORM_Y, 0])
            self.play(*appear(br2), run_time=1.0)
            b5 = pcs_bar(0.2, 4.7, 0.1, 5.0, unit=2.0, x0=-3.5, y=0.8,
                         tc_tex=r"T_c = 5.0\,\text{ns}", syms=False,
                         nums=[None, "4.7 ns", None], locks=True, lock_scale=0.85, num_size=40)
            self.play(Transform(bar_out, b5.outline), Transform(bar_segs[2], b5.segs[2]),
                      Transform(lk_su, b5.locks[1]),
                      FadeOut(bar_segs[1]), *during(disappear(n07, lab47), 0, 0.22),
                      *during([Transform(cmp_ok, b5.segs[1]),
                               cmp_bad.animate.move_to([x0 + 1.4 + 4.0, 0.8, 0]).set_fill(PURPLE, 0)],
                              0.25, 1),
                      run_time=2.0)
            self.remove(cmp_bad)   # cmp_ok is now the one 4.7 ns segment: no seam
            n47 = b5.nums[0]
            self.play(*edit(bar_tc, b5.tc), *appear(n47, shift=None), run_time=1.5)
            new_txt = T("200 MHz", 60, YELLOW, weight=BOLD)
            new_txt.scale_to_fit_width(bb2.board.width - 0.35).move_to(bb2.board)
            self.play(*swap(bb2.txt, new_txt), run_time=1.2)

            c.wait_until("upset")
            hinge = bb2.legs[0].get_start()
            upset = T("“the clock period has to be increased\nto ensure correct operation”",
                      34, line_spacing=1.1).move_to([0, -2.6, 0])
            self.play(*during(disappear(br1, xm, br2), 0, 0.45), *during(appear(upset, shift=None), 0.5, 1),
                      Rotate(bb2.board, angle=-0.2, about_point=hinge),
                      Rotate(new_txt, angle=-0.2, about_point=hinge),
                      run_time=1.8)
            self.play(new_txt.animate.set_color(DIM), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
