"""Chapter 1, scene 6: how big is log2(n!)? Bars, a sandwich, n log n, the floor. Clips c1.nlogn.1 – c1.nlogn.5."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

try:   # scene 4's scoreboard (read-only); a stand-in until that file exists
    from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402
except ImportError:
    make_scoreboard = None

# --- scene 5's last shot, exactly as scene 5 reports it ---
S5_SIZE = 60
S5_TOP_POS = np.array([0.0, 0.85, 0.0])     # boxed YELLOW 2^{C(n)} >= n!
S5_BOUND_POS = np.array([0.0, -0.6, 0.0])   # C(n) >= log2(n!), FG

# --- the bar chart: bar k spans [X0 + (k-1)P, X0 + kP], height log2 k * YS ---
X0, P = -6.2, 0.5
YB, YS = -2.75, 1.0
XR = X0 + 16 * P
RCOL = 4.4            # centre x of the column right of the chart
TOP_Y = 3.3           # the formula line at the top


def bar_x(k):
    return X0 + (k - 0.5) * P


def hy(h):
    return YB + h * YS


def scene5_shot():
    top = MathTex("2", "^{C(n)}", r"\ge", "n!", font_size=S5_SIZE, color=YELLOW).move_to(S5_TOP_POS)
    box = SurroundingRectangle(top, color=YELLOW, buff=0.25, stroke_width=4).move_to(S5_TOP_POS)
    bound = MathTex("C(n)", r"\ge", r"\log_2", "(", "n!", ")", font_size=S5_SIZE).move_to(S5_BOUND_POS)
    return top, box, bound


def stand_in_scoreboard():
    """Only used while scenes/ch1_s4_contest.py is missing."""
    rows = ["insertion sort", "quicksort", "merge sort"]
    row_labels = VGroup(*[T(r, size=34) for r in rows]).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    row_labels.move_to([-3.6, 0.3, 0])
    col_headers = VGroup(T("comparisons", size=30, color=DIM), T("DECstation", size=30, color=DIM))
    col_headers[0].move_to([0.9, 1.8, 0])
    col_headers[1].move_to([4.4, 1.8, 0])
    cells = [[T("?", size=40, color=GOLD).move_to([h.get_x(), r.get_y(), 0]) for h in col_headers]
             for r in row_labels]
    floor_line = DashedLine([-5.6, -1.3, 0], [5.6, -1.3, 0], color=DIM, stroke_width=3)
    floor_label = T("lower bound?", size=30, color=DIM).next_to(floor_line, DOWN, buff=0.2)
    tally_tag = T("", size=30)
    sb = VGroup(row_labels, col_headers, *[c for row in cells for c in row], floor_line, floor_label)
    sb.row_labels, sb.col_headers, sb.cells = row_labels, col_headers, cells
    sb.floor_line, sb.floor_label, sb.tally_tag = floor_line, floor_label, tally_tag
    return sb


class HowBigIsLogFactorial(NarratedScene):
    def construct(self):
        self.clip_sum()
        self.clip_bounds()
        self.clip_general()
        self.clip_numbers()
        self.clip_floor()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c1.nlogn.1
    def clip_sum(self):
        s5_top, s5_box, bound = scene5_shot()
        with self.say("c1.nlogn.1") as c:
            # {how}: scene 5's result comes back; its log2(n!) goes to the top, in question
            self.play(FadeIn(s5_top), FadeIn(s5_box), FadeIn(bound), run_time=0.6)
            bound.generate_target()
            bound.target.scale(48 / S5_SIZE).move_to(UP * TOP_Y)
            bound.target[2:].set_color(YELLOW)
            self.play(FadeOut(s5_top), FadeOut(s5_box), MoveToTarget(bound),
                      run_time=min(1.5, c.until("sum")))
            c.wait_until("sum")

            # {sum}: n! = 1 x 2 x 3 x ... x n, its n! lifted out of the bound
            prod = MathTex("n!", "=", "1", r"\times", "2", r"\times", "3", r"\times",
                           r"\cdots", r"\times", "n", font_size=52).move_to(UP * 1.9)
            self.play(TransformFromCopy(bound[4], prod[0]),
                      LaggedStart(*[FadeIn(m) for m in prod[1:]], lag_ratio=0.12),
                      run_time=1.8)
            settle(self, prod)
            c.wait_until("the log of a product")

            # ... and the log of a product is the sum of the logs
            summ = MathTex(r"\log_2(n!)", "=", r"\log_2", "1", "+", r"\log_2", "2", "+",
                           r"\log_2", "3", "+", r"\cdots", "+", r"\log_2", "n", font_size=48)
            summ.move_to(UP * 1.9)
            summ[0].set_color(YELLOW)
            # n! -> log2(n!), each factor k -> log2 k, each x -> +
            pairs = [(0, 0), (1, 1), (2, 3), (3, 4), (4, 6), (5, 7), (6, 9), (7, 10),
                     (8, 11), (9, 12), (10, 14)]
            self.play(*[ReplacementTransform(prod[i], summ[j]) for i, j in pairs],
                      *[FadeIn(summ[j], shift=0.15 * DOWN) for j in (2, 5, 8, 13)],
                      run_time=min(2.0, 0.8 * c.until("bars")))
            self.remove(*prod.get_family())
            settle(self, summ)
            c.wait_until("bars")

            # {bars}: the sum goes to the top; axes, k = 1 ... 16
            base = Line([X0 - 0.2, YB, 0], [XR + 0.3, YB, 0], color=DIM, stroke_width=3)
            yax = Line([X0, YB, 0], [X0, hy(4.45), 0], color=DIM, stroke_width=3)
            self.play(FadeOut(bound, shift=0.3 * UP), summ.animate.move_to(UP * TOP_Y),
                      Create(base), Create(yax), run_time=1.3)
            k_lbls = VGroup(*[T(str(k), size=30, color=DIM).move_to([bar_x(k), YB - 0.34, 0])
                              for k in range(1, 17)])
            c.wait_until("for each number")
            self.play(LaggedStart(*[FadeIn(m, shift=0.15 * UP) for m in k_lbls], lag_ratio=0.12),
                      run_time=1.3)
            settle(self, k_lbls)
            c.wait_until("with height")

            # bar k has height log2 k (bar 1 has height 0, so it is not drawn)
            bars = VGroup(*[
                Rectangle(width=P, height=np.log2(k) * YS)
                .set_fill(BLUE, 0.75).set_stroke(BG, 2)
                .move_to([bar_x(k), YB + np.log2(k) * YS / 2, 0])
                for k in range(2, 17)])
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12),
                      run_time=min(2.2, c.until("here are the bars")))
            settle(self, bars)
            c.wait_until("here are the bars")

            # "Here are the bars for sixteen": bars 2, 4, 8, 16 reach 1, 2, 3, 4
            h_lbls = VGroup(*[T(str(h), size=32, color=GOLD).move_to([bar_x(2 ** h), hy(h) + 0.3, 0])
                              for h in range(1, 5)])
            self.play(LaggedStart(*[FadeIn(m, shift=0.25 * DOWN) for m in h_lbls], lag_ratio=0.3),
                      run_time=1.4)
            settle(self, h_lbls)
            c.wait_until("total")

            # {total}: every bar goes into one GOLD total
            total = MathTex(r"\text{total}", r"\approx", "44.25", font_size=48, color=GOLD)
            total.move_to([RCOL, -1.1, 0])
            copies = [b.copy().set_fill(GOLD, 0.9) for b in bars]
            flys = [cp.animate.scale(0.1).move_to(total[2]).set_opacity(0) for cp in copies]
            self.play(LaggedStart(*flys, lag_ratio=0.06, run_time=1.4),
                      time_span(FadeIn(total, shift=0.2 * LEFT), 0.9, 1.9))
            self.remove(*copies)

        self.summ, self.bars, self.base, self.yax = summ, bars, base, yax
        self.k_lbls, self.h_lbls, self.total = k_lbls, h_lbls, total

    # ------------------------------------------------------------------ c1.nlogn.2
    def clip_bounds(self):
        total = self.total
        with self.say("c1.nlogn.2") as c:
            # {top}: a GOLD line at height 4 across all sixteen bars
            top_line = Line([X0, hy(4), 0], [XR, hy(4), 0], color=GOLD, stroke_width=5)
            self.play(Create(top_line), run_time=1.5)
            c.wait_until("so the total is at most")
            top_rect = Rectangle(width=16 * P, height=4 * YS).set_stroke(GOLD, 3).set_fill(GOLD, 0.08)
            top_rect.move_to([(X0 + XR) / 2, hy(2), 0]).set_z_index(-1)
            le64 = MathTex(r"\le", r"16 \times 4", "=", "64", font_size=48, color=GOLD)
            le64.next_to([XR, hy(4), 0], RIGHT, buff=0.35)
            self.play(FadeIn(top_rect), FadeIn(le64, shift=0.3 * LEFT), run_time=1.3)
            c.wait_until("half")

            # {half}: a GOLD line at height 3 under the last eight bars, an 8 x 3 block
            half_line = Line([X0 + 8 * P, hy(3), 0], [XR, hy(3), 0], color=GOLD, stroke_width=5)
            self.play(Create(half_line), run_time=1.2)
            c.wait_until("so the total is at least")
            half_rect = Rectangle(width=8 * P, height=3 * YS).set_stroke(width=0).set_fill(GOLD, 0.35)
            half_rect.move_to([X0 + 12 * P, hy(1.5), 0])
            ge24 = MathTex(r"\ge", r"8 \times 3", "=", "24", font_size=48, color=GOLD)
            ge24.next_to([XR, hy(3), 0], RIGHT, buff=0.35)
            self.add(half_line)   # keep the line above the shading
            self.play(FadeIn(half_rect), FadeIn(ge24, shift=0.3 * LEFT), run_time=1.3)
            self.bring_to_front(half_line)
            c.wait_until("exact")

            # {exact}: the total, sandwiched: 24 <= 44.25 <= 64
            exact = MathTex("24", r"\le", "44.25", r"\le", "64", font_size=52)
            exact.move_to(total)
            for i in (0, 2, 4):
                exact[i].set_color(GOLD)
            self.play(ReplacementTransform(total[2], exact[2]),
                      FadeOut(total[0]), FadeOut(total[1]),
                      TransformFromCopy(ge24[3], exact[0]), TransformFromCopy(le64[3], exact[4]),
                      FadeIn(exact[1]), FadeIn(exact[3]),
                      run_time=min(1.8, 0.8 * c.until()))
            self.remove(*total.get_family())
            settle(self, exact)

        self.top_line, self.top_rect, self.le64 = top_line, top_rect, le64
        self.half_line, self.half_rect, self.ge24, self.exact = half_line, half_rect, ge24, exact

    # ------------------------------------------------------------------ c1.nlogn.3
    def clip_general(self):
        summ, exact = self.summ, self.exact
        chart = [self.bars, self.base, self.yax, self.k_lbls, self.h_lbls,
                 self.top_line, self.le64, self.half_line, self.ge24]
        sand = MathTex(r"\tfrac{n}{2}\log_2\tfrac{n}{2}", r"\le", r"\log_2(n!)", r"\le",
                       r"n\log_2 n", font_size=56).move_to(UP * TOP_Y)
        sand[2].set_color(YELLOW)
        with self.say("c1.nlogn.3") as c:
            # {general}: the bars dim; log2(n!) takes the middle of a symbolic sandwich
            self.play(*set_alpha(chart, DIMMED),
                      self.top_rect.animate.set_stroke(opacity=DIMMED).set_fill(opacity=0.03),
                      self.half_rect.animate.set_fill(opacity=0.1),
                      ReplacementTransform(summ[0], sand[2]),
                      *[FadeOut(m) for m in summ[1:]],
                      run_time=1.5)
            self.remove(*summ.get_family())   # (ReplacementTransform put sand[2] inside summ)
            self.add(sand[2])
            c.wait_until("the low side")

            # the low side, n/2 log2 n/2, born from the 24 ...
            self.play(TransformFromCopy(exact[0], sand[0]), TransformFromCopy(exact[1], sand[1]),
                      run_time=1.6)
            c.wait_until("the high side")
            # ... the high side, n log2 n, from the 64
            self.play(TransformFromCopy(exact[4], sand[4]), TransformFromCopy(exact[3], sand[3]),
                      run_time=1.6)
            settle(self, sand)
            c.wait_until("grow")

            # {grow}: both ends grow like n log n ...
            ty = sand.get_bottom()[1] - 0.45
            tags = [MathTex(r"O(n\log n)", font_size=40, color=GOLD).move_to([sand[i].get_x(), ty, 0])
                    for i in (0, 2, 4)]
            tag_lo, tag_mid, tag_hi = tags
            self.play(LaggedStart(FadeIn(tag_lo, shift=0.25 * UP), FadeIn(tag_hi, shift=0.25 * UP),
                                  lag_ratio=0.3),
                      *set_alpha([exact], DIMMED), run_time=1.4)
            c.wait_until("so the total does too")
            # ... so the total does too
            twin = tag_mid.copy()
            self.play(TransformFromCopy(tag_lo, tag_mid), TransformFromCopy(tag_hi, twin), run_time=1.4)
            self.remove(twin)
            c.wait_until("sharp")

            # {sharp}: the notes' sharper estimate, out of the middle and the high side
            sharp = MathTex(r"\log_2(n!)", r"\approx", r"n\log_2 n", "-", r"1.44\,n",
                            font_size=60).move_to(DOWN * 0.1)
            sharp[0].set_color(YELLOW)
            foot = Tex(r"Stirling's formula; $1.44 \approx \log_2 e$", font_size=40, color=DIM)
            foot.next_to(sharp, DOWN, buff=0.7)
            sweep_clear(self,
                        time_span(TransformFromCopy(sand[2], sharp[0]), 0.5, 2.0),
                        time_span(TransformFromCopy(sand[4], sharp[2]), 0.6, 2.0),
                        time_span(FadeIn(sharp[1]), 1.0, 2.0),
                        time_span(FadeIn(sharp[3]), 1.1, 2.0),
                        time_span(FadeIn(sharp[4]), 1.2, 2.0),
                        time_span(FadeIn(foot, shift=0.2 * UP), 1.8, 2.6),
                        keep=[sand, *tags], run_time=2.6)
            settle(self, sharp)
            c.wait_until("minus one point four four")
            if c.until() > 1.5:
                self.play(FlashUnder(sharp[4], color=GOLD, run_time=1.5, time_width=1.5))

        self.sharp, self.foot = sharp, foot

    # ------------------------------------------------------------------ c1.nlogn.4
    def clip_numbers(self):
        sharp, foot = self.sharp, self.foot
        with self.say("c1.nlogn.4") as c:
            # {five}: "Let's put in numbers." The estimate goes up top for later
            sweep_clear(self, sharp.animate.scale(0.75).move_to(UP * 3.25), keep=[sharp, foot],
                        run_time=1.4)
            c.wait_until("five factorial")

            five = MathTex("5!", "=", "120", font_size=56, color=GOLD).move_to(UP * 1.95)
            self.play(FadeIn(five, shift=0.3 * DOWN), FadeOut(foot), run_time=1.2)
            c.wait_until("powers")

            # {powers}: 2^6 = 64 < 120 <= 128 = 2^7
            pw = MathTex("2^6", "=", "64", "<", "120", r"\le", "128", "=", "2^7", font_size=52)
            pw.move_to(UP * 0.8)
            pw[4].set_color(GOLD)
            self.play(LaggedStart(*[FadeIn(m) for m in pw[:4]], lag_ratio=0.2),
                      TransformFromCopy(five[2], pw[4]), run_time=1.6)
            c.wait_until("and seven give")
            self.play(LaggedStart(*[FadeIn(m) for m in pw[5:]], lag_ratio=0.2), run_time=1.3)
            settle(self, pw)
            c.wait_until("seven")

            # {seven}: some arrangement of five items needs at least 7 comparisons
            seven = T("five items: some input needs at least 7 comparisons", size=36,
                      t2c={"7": GOLD}, disable_ligatures=True).move_to(DOWN * 0.35)
            self.play(FadeIn(seven, shift=0.2 * DOWN), pw[8].animate.set_color(GOLD), run_time=1.2)
            self.play(FlashAround(select(seven, "7")[0], run_time=1.5, time_width=1.5, color=GOLD))
            c.wait_until("tenk")

            # {tenk}: log2(10000!) ~ 118,458
            tenk = MathTex(r"\log_2(10000!)", r"\approx", r"118{,}458", font_size=52).move_to(DOWN * 1.65)
            tenk[0].set_color(YELLOW)
            tenk[2].set_color(GOLD)
            self.play(FadeIn(tenk[0], shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("about a hundred and eighteen")
            self.play(FadeIn(tenk[1]), FadeIn(tenk[2], shift=0.2 * LEFT), run_time=1.0)
            settle(self, tenk)
            c.wait_until("formula")

            # {formula}: the notes' estimate at n = 10000, out of the line at the top
            fm = MathTex(r"10000\log_2 10000", "-", r"1.44 \times 10000", r"\approx", r"118{,}477",
                         font_size=48).move_to(DOWN * 2.8)
            fm[4].set_color(GOLD)
            self.play(TransformFromCopy(sharp[2], fm[0]), TransformFromCopy(sharp[3], fm[1]),
                      TransformFromCopy(sharp[4], fm[2]), FadeIn(fm[3]), FadeIn(fm[4]),
                      run_time=min(1.8, c.until(floor=0.5)))
            settle(self, fm)

        self.tenk, self.fm = tenk, fm

    # ------------------------------------------------------------------ c1.nlogn.5
    def clip_floor(self):
        tenk, fm = self.tenk, self.fm
        with self.say("c1.nlogn.5") as c:
            # {merge}: merge sort needs only O(n log n)
            merge = Tex("merge sort: ", r"$O(n\log n)$", " comparisons (Part 5)", font_size=52)
            merge[1].set_color(GOLD)
            merge.move_to(DOWN * 0.15)
            sweep_clear(self, tenk.animate.move_to(UP * 2.8), fm.animate.move_to(UP * 1.75),
                        time_span(FadeIn(merge, shift=0.3 * DOWN), 0.8, 1.8),
                        keep=[tenk, fm], run_time=1.8)
            c.wait_until("best")

            # {best}: O(n log n) is the best possible ...
            best = Tex(r"$O(n\log n)$", " is the best possible", font_size=52).move_to(DOWN * 1.45)
            best[0].set_color(GOLD)
            self.play(TransformFromCopy(merge[1], best[0]), FadeIn(best[1], shift=0.2 * LEFT),
                      run_time=1.2)
            settle(self, best)
            c.wait_until("and merge sort reaches it")
            # ... and merge sort reaches it
            tick = check_mark().next_to(merge, RIGHT, buff=0.35)
            self.play(Create(tick), run_time=0.8)
            c.wait_until("floor")

            # {floor}: scene 4's scoreboard comes back; the 118,458 parks bottom right
            sb = make_scoreboard() if make_scoreboard else stand_in_scoreboard()
            sweep_clear(self, tenk.animate.scale(0.55).move_to([4.75, -2.9, 0]),
                        time_span(FadeIn(sb), 0.7, 1.3), keep=[tenk], run_time=1.3)
            # the dashed floor line turns solid; the label becomes "lower bound ≈ 118,458"
            dashed, old_lbl = sb.floor_line, sb.floor_label
            full = T("lower bound ≈ 118,458", size=34, color=GOLD, disable_ligatures=True)
            full.move_to(old_lbl, aligned_edge=LEFT)
            words = T("lower bound ≈", size=34, color=GOLD).move_to(VGroup(*full[:11]))
            num = T("118,458", size=34, color=GOLD).move_to(VGroup(*full[11:]))
            num.shift((words.get_right()[0] + 0.2 - num.get_left()[0]) * RIGHT)
            # the longer label would run into the line: the solid line starts just after it
            solid = Line([num.get_right()[0] + 0.35, dashed.get_y(), 0], dashed.get_end())
            solid.set_stroke(GOLD, 3)
            self.play(ReplacementTransform(dashed, solid), ReplacementTransform(old_lbl, words),
                      ReplacementTransform(tenk[2], num), FadeOut(tenk[0]), FadeOut(tenk[1]),
                      run_time=1.6)
            self.remove(*tenk.get_family())   # (ReplacementTransform put num inside tenk)
            self.add(num)
            c.wait_until("no comparison sort")
            self.play(VShowPassingFlash(solid.copy().set_stroke(YELLOW, 8), time_width=0.4),
                      run_time=min(1.6, c.until()))
        self.wait(1.0)   # the floor, held before the fade
