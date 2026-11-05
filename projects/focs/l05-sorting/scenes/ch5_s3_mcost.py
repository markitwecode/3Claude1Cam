"""Chapter 5, scene 3: what merging costs. Clips c5.mcost.1 – c5.mcost.4.

Opens on ch5_s2_merge.handover_shot() (finished zipper + trace). Every merge uses s2's Zipper
(scale 0.5 here so six items plus [] fit). ins code is ch2_s2_ins.ocode(INS_SRC).
"""
# style: 2
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

S2 = load_scene("ch5_s2_merge")
S2INS = load_scene("ch2_s2_ins")

ZY = 0.9          # zipper centre for the example merges
ZL = -6.0         # left edge of the input chains
ZSC = 0.5         # zipper scale (6 items + [] fit the frame)
CMD_Y = 3.3
REPLY_Y = -1.45
COUNT_Y = -2.35
TRACE_DY = 2.95   # clip 4: s2's trace rows shifted up


def zipper(top, bot):
    return S2.Zipper(top=top, bot=bot, cy=ZY, left=ZL, scale=ZSC)


def command(src):
    return S2.ycode(src, 36).move_to([0, CMD_Y, 0])


def reply_line(src):
    return Code(src, size=32).move_to([0, REPLY_Y, 0])


def count_label(txt):
    return T(txt, size=36, color=GOLD).move_to([0, COUNT_Y, 0])


def tick_at(z, i):
    return check_mark(GOLD).scale(0.6).move_to(z.slot(i) + UP * 0.62)


def free_over(z, i0, i1, side=UP):
    f = T("free", size=30, color=GREEN)
    return f.move_to((z.slot(i0) + z.slot(i1)) / 2 + side * 0.62)


class MergeCost(NarratedScene):
    def construct(self):
        self.bound_clip()
        self.extremes_clip()
        self.lopsided_clip()
        self.deep_clip()
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # helpers ---------------------------------------------------------------
    def takes(self, z, sides, rt, flash_top=False):
        ticks = []
        for k, w in enumerate(sides):
            tick = tick_at(z, len(z.out))
            extra = []
            if flash_top and z.rem["top"]:
                extra = [FlashAround(z.rem["top"][0], color=GOLD, time_width=1.5)]
            self.play(*z.take(w), *during(appear(tick, shift=None), 0.7, 1.0), *extra,
                      run_time=rt * (1.3 if k == 0 else 1.0))
            ticks.append(tick)
        return ticks

    # c5.mcost.1 --------------------------------------------------------------
    def bound_clip(self):
        shot = S2.handover_shot()
        parts = list(shot.submobjects)
        self.add(*parts)
        top, bot, links, tick = parts[0:4]
        rows = parts[4:9]
        qs = [parts[13], parts[15], parts[17]]
        cnt = parts[21]
        out = [top.cells[0], bot.cells[0], top.cells[1], bot.cells[1], bot.cells[2]]

        with self.say("c5.mcost.1") as c:
            self.play(*flash(qs, color=GOLD), FlashAround(cnt, color=GOLD, time_width=1.5),
                      run_time=1.5)
            prev = None
            for i, cue in enumerate(["Look at", "Every comparison", "exactly one item"]):
                c.wait_until(cue)
                q = qs[i]
                arr = Arrow(q.get_left() + LEFT * 0.08, out[i].get_bottom(), buff=0.12,
                            stroke_width=4, color=GOLD, max_tip_length_to_length_ratio=0.1,
                            tip_length=0.22)
                anims = [GrowArrow(arr), restyle(out[i].box, outline=GOLD),
                         restyle(out[i].ptr, outline=GOLD)]
                if prev is not None:
                    anims += during(disappear(prev), 0, 0.4)
                self.play(*anims, run_time=1.2)
                prev = arr

            c.wait_until("free")
            note = T("no comparisons", size=30, color=GREEN)
            note.move_to((out[3].get_center() + out[4].get_center()) / 2 + DOWN * 0.8)
            self.play(*disappear(prev),
                      *[restyle(m, outline=GREEN) for cl in out[3:] for m in (cl.box, cl.ptr)],
                      run_time=1.2)
            self.play(*appear(note), run_time=1.0)

            c.wait_until("very last")
            self.play(FlashAround(out[4], color=GREEN, time_width=1.5), run_time=1.5)

            c.wait_until("bound")
            row0 = rows[0]
            others = [m for m in self.mobjects if m not in (top, bot, links, row0)]
            self.play(*during(disappear(*others), 0, 0.5),
                      *during([row0.animate.move_to([0, 0.45, 0])], 0.4, 1.0), run_time=1.6)

            c.wait_until("lengths")
            braces, labs = [], []
            for sub, txt in (("[3; 5]", "m = 2"), ("[4; 7; 9]", "n = 3")):
                g = row0.find(sub)
                b = span_brace(g.get_corner(DL), g.get_corner(DR), DOWN, color=GOLD)
                lab = MathTex(txt, font_size=42, color=GOLD).next_to(b, DOWN, buff=0.12)
                braces.append(b)
                labs.append(lab)
            self.play(*[GrowFromCenter(b) for b in braces], *appear(*labs, lag=0.3),
                      run_time=1.4)

            c.wait_until("at most")
            form = MathTex(r"\text{comparisons} \le m + n - 1", font_size=54, color=GOLD)
            form.move_to([0, -1.75, 0])
            box = SurroundingRectangle(form, color=GOLD, buff=0.25)
            self.fgroup = VGroup(form, box)
            self.play(*appear(self.fgroup, shift=None), run_time=1.4)

            foot = T("the notes also say: at most m + n", size=30, color=DIM)
            foot.move_to([0, -2.95, 0])
            c.wait_until(own_word=foot)
            self.play(*appear(foot), run_time=1.0)

    # c5.mcost.2 --------------------------------------------------------------
    def extremes_clip(self):
        fg = self.fgroup
        with self.say("c5.mcost.2") as c:
            z = zipper((1, 2, 3), (4, 5, 6))
            cmd = command("merge ([1; 2; 3], [4; 5; 6])")
            c.wait_until("interleave")
            sweep_clear(self, *appear(cmd, z.top, z.bot, lag=0.3, shift=None), FadeIn(z.slots),
                        fg.animate.scale(0.7).move_to([0, -3.35, 0]), keep=[fg],
                        run_time=1.8)

            c.wait_until("Merge one")
            rt = max(0.7, min(1.0, c.until("runs out") / 3.5))
            self.takes(z, ["top"] * 3, rt)

            c.wait_until("runs out")
            free = free_over(z, 3, 5)
            self.play(*z.rest("bot"), run_time=1.3)

            c.wait_until("three comparisons")
            cnt = count_label("3 comparisons")
            rep = reply_line("- : int list = [1; 2; 3; 4; 5; 6]")
            self.play(FadeOut(z.slots), *appear(rep, cnt, lag=0.4), run_time=1.3)
            c.wait_until(own_word=free)
            self.play(*appear(free, shift=None), run_time=0.8)

            c.wait_until("with two")
            z2 = zipper((1, 3, 5), (2, 4, 6))
            cmd2 = command("merge ([1; 3; 5], [2; 4; 6])")
            sweep_clear(self, *appear(z2.top, z2.bot, cmd2, lag=0.2, shift=None),
                        FadeIn(z2.slots), keep=[fg], run_time=min(2.0, c.until("alternate")))

            c.wait_until("alternate")
            rt = max(0.6, min(1.0, c.until("five comparisons") / 6.3))
            self.takes(z2, ["top", "bot", "top", "bot", "top"], rt)
            free2 = free_over(z2, 5, 5)
            self.play(*z2.rest("bot"), *during(appear(free2, shift=None), 0.5, 1.0),
                      run_time=rt)

            c.wait_until("five comparisons")
            rep2 = reply_line("- : int list = [1; 2; 3; 4; 5; 6]")
            cnt2 = count_label("5 comparisons = 3 + 3 − 1")
            self.play(FadeOut(z2.slots), *appear(rep2, cnt2, lag=0.4), run_time=1.4)

            c.wait_until("most possible")
            self.play(FlashAround(cnt2, color=GOLD, time_width=1.5), run_time=1.5)

    # c5.mcost.3 --------------------------------------------------------------
    def lopsided_clip(self):
        fg = self.fgroup
        with self.say("c5.mcost.3", gap=2.0) as c:
            z = zipper((5,), (1, 2, 3, 4))
            cmd = command("merge ([5], [1; 2; 3; 4])")
            c.wait_until("of the list")
            sweep_clear(self, *appear(cmd, z.top, z.bot, lag=0.2, shift=None),
                        FadeIn(z.slots), keep=[fg], run_time=min(1.8, c.until("The five")))

            c.wait_until("The five")
            self.takes(z, ["bot"] * 4, 0.7, flash_top=True)

            free = free_over(z, 4, 4, side=DOWN)
            rep = reply_line("- : int list = [1; 2; 3; 4; 5]")
            cnt = count_label("4 comparisons")
            self.play(*during(z.rest("top"), 0, 0.6), FadeOut(z.slots),
                      *during(appear(free, rep, cnt, lag=0.3, shift=None), 0.45, 1.0),
                      run_time=1.8)

            # {ins}: ins beside merge
            c.wait_until("what ins")
            ins = S2INS.ocode(S2INS.INS_SRC, 30)
            ins.move_to([0, 2.45, 0]).shift(RIGHT * (-5.9 - ins.get_left()[0]))
            mrg = S2.ycode(S2.MERGE_SRC, 28)
            mrg.move_to([0, -1.1, 0]).shift(RIGHT * (-5.9 - mrg.get_left()[0]))
            sweep_clear(self, *appear(ins, mrg, lag=0.3, shift=None),
                        run_time=min(2.0, c.until("generalises")))

            cap = T("Generalises insert\nto two lists", size=34, line_spacing=1.1)
            cap.move_to([4.15, 0.35, 0])
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)

            c.wait_until("two lists")
            il2, il3 = ins.line(2), ins.line(3)
            b_ins = token_box(ins.find("if x <= y then x :: y :: ys", line=2), il2)
            b_m1 = token_box(mrg.find("if x <= y then", line=4), mrg.line(4))
            b_m2 = token_box(mrg.find("x :: merge (xs, y::ys)", line=5), mrg.line(5))
            self.play(FadeIn(b_ins), FadeIn(b_m1), FadeIn(b_m2), run_time=1.2)

            c.wait_until("single item")
            self.play(Transform(b_ins, token_box(ins.find("else y :: ins x ys", line=3), il3)),
                      Transform(b_m1, token_box(mrg.find("else", line=6), mrg.line(6))),
                      Transform(b_m2, token_box(mrg.find("y :: merge (x::xs, ys)", line=7),
                                                mrg.line(7))),
                      run_time=1.5)

            c.wait_until("little")
            bad = T("4 comparisons\nto place 1 item", size=34, color=RED, line_spacing=1.1)
            bad.move_to([4.15, -1.35, 0])
            self.play(*appear(bad), run_time=1.0)

            c.wait_until("equal")
            good = T("lengths about equal:\nfast", size=34, color=GREEN, line_spacing=1.1)
            good.move_to([4.15, -2.95, 0])
            self.play(*appear(good), run_time=1.0)

    # c5.mcost.4 --------------------------------------------------------------
    def deep_clip(self):
        with self.say("c5.mcost.4") as c:
            rows = [S2.trace_row(i).shift(UP * TRACE_DY) for i in range(5)]
            arrs = [S2.trace_arrow(i).shift(UP * TRACE_DY) for i in range(1, 5)]
            sweep_clear(self, *appear(*rows, lag=0.15, shift=None),
                        *appear(*arrs, lag=0.15, shift=None),
                        run_time=min(2.0, c.until("wait")))

            c.wait_until("wait")
            waits = [rows[1].find("3 ::"), rows[2].find("3 :: 4 ::"),
                     rows[3].find("3 :: 4 :: 5 ::"), rows[4].find("3 :: 4 :: 5 ::")]
            g = waits[-1]
            br = span_brace(g.get_corner(DL), g.get_corner(DR), DOWN, color=YELLOW)
            wl = T("waiting", size=30, color=YELLOW).next_to(br, DOWN, buff=0.1)
            self.play(*[a for w in waits for a in recolor(w, YELLOW)], GrowFromCenter(br),
                      *during(appear(wl), 0.4, 1.0), run_time=1.5)

            ilab = T("lecture 3's append", size=28, color=DIM)
            iarr = MathTex(r"\Rightarrow", font_size=40, color=DIM)
            icode = Code("1 :: (2 :: (3 :: append [] [4]))", size=28).set_color(DIM)
            iarr.move_to([0, -1.55, 0]).shift(RIGHT * (-5.6 - iarr.get_left()[0]))
            icode.next_to(iarr, RIGHT, buff=0.2)
            ilab.next_to(iarr, UP, buff=0.25, aligned_edge=LEFT)
            c.wait_until(own_word=ilab)
            self.play(*appear(ilab, VGroup(iarr, icode), lag=0.3), run_time=1.2)

            ni = T("not iterative", size=36, color=RED).move_to([4.9, 1.9, 0])
            c.wait_until("not iterative")
            self.play(*appear(ni), run_time=1.0)

            c.wait_until("acc")
            b1t = T("still builds every cell", size=30, color=DIM)
            b2t = T("builds them backwards", size=30, color=DIM)
            VGroup(b1t, b2t).arrange(RIGHT, buff=1.0).move_to([0, -2.45, 0])
            b1 = VGroup(SurroundingRectangle(b1t, color=DIM, buff=0.2), b1t)
            b2 = VGroup(SurroundingRectangle(b2t, color=DIM, buff=0.2), b2t)
            c.wait_until(own_word=b1t)
            self.play(*appear(b1), run_time=1.0)
            c.wait_until("backwards")
            self.play(*appear(b2), run_time=1.0)

            c.wait_until("habit")
            maxim = T("Never add an accumulator merely out of habit.", size=34, color=DIM,
                      slant=ITALIC).move_to([0, -3.28, 0])
            self.play(*appear(maxim), run_time=1.2)  # early: the maxim the sentence leads into, read in full
