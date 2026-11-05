"""Chapter 4, scene 6: was it worth it? quik's comparisons, copies, and time on the board. Clips c4.speed.1 – c4.speed.3.

- c4.speed.1: "Was it worth it?"; `quick rs` / `quik (rs, [])` side by side, 158,058 comparisons under
  each; {copies} cells copied by @: 76,447 vs 0.
- c4.speed.2: the scoreboard returns; quicksort's 0.74 s slides down small/DIM ("quick"), 0.53 s takes
  its place; DIM reading tag; GREEN "same for quik" under 158,058.
- c4.speed.3: tags and 0.74 fade, board shrinks up; Pascal-array bar vs quik-chain bar, "only slightly
  faster"; chain cells light with "new memory"; {real} "comparisons dominate" over a balance;
  {strings} two long names compared letter by letter, "one comparison".
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402


def filled_board():
    """The scoreboard as ch3 leaves it."""
    sb = make_scoreboard(bound="118,458")
    for r, vals in enumerate((("25,146,194", "174 s"), ("158,058", "0.74 s"))):
        for col, val in enumerate(vals):
            sb.cells[r].submobjects[col] = T(val, 44, GOLD).move_to(sb.cells[r][col])
    return sb


def array_icon(n=5, s=0.5):
    boxes = VGroup(*[Square(s).set_stroke(BLUE, 3).set_fill(BG, 1) for _ in range(n)])
    boxes.arrange(RIGHT, buff=0)
    return boxes


def chain_icon(n=3, pitch=2.0):
    """n small cons cells [box|•] with arrows; returns VGroup(cells..., arrows...) with .cells, .boxes."""
    cells, boxes, arrows = [], [], []
    for i in range(n):
        box = Square(0.55).set_stroke(BLUE, 3).set_fill(BG, 1)
        ptr = Rectangle(width=0.3, height=0.55).set_stroke(BLUE, 3).set_fill(BG, 1)
        ptr.next_to(box, RIGHT, buff=0)
        dot = Dot(ptr.get_center(), radius=0.06, color=FG)
        cell = VGroup(box, ptr, dot).move_to([i * pitch, 0, 0])
        cells.append(cell)
        boxes.append(box)
    for a, b in zip(cells, cells[1:]):
        arrows.append(Arrow(a[2].get_center(), b[0].get_left(), buff=0.05, stroke_width=3,
                            max_tip_length_to_length_ratio=0.3).set_color(FG))
    g = VGroup(*cells, *arrows)
    g.cells, g.boxes = cells, boxes
    return g


class Speed(NarratedScene):
    def construct(self):
        self.calls()
        self.board()
        self.surprise()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c4.speed.1
    def calls(self):
        with self.say("c4.speed.1", gap=1.4) as c:
            q = T("Was it worth it?", 52, YELLOW).move_to(UP * 2.6)
            self.play(*appear(q), run_time=1.0)   # early: the question is the line itself
            c.wait_until("same")

            left = Code("quick rs", size=48).move_to([-3.5, 0.9, 0])
            right = Code("quik (rs, [])", size=48).move_to([3.5, 0.9, 0])
            self.play(*appear(left, right, lag=0.4), run_time=1.5)
            c.wait_until("both make")

            n1 = T("158,058 comparisons", 36, GOLD).move_to([-3.5, -0.3, 0])
            n2 = T("158,058 comparisons", 36, GOLD).move_to([3.5, -0.3, 0])
            self.play(*appear(n1, n2, lag=0.4), run_time=1.4)
            c.wait_until("copies")

            self.play(*set_alpha([n1, n2], 0.4), run_time=1.0)
            c.wait_until("copying")

            k1 = T("cells copied by @: 76,447", 36, t2c={"76,447": GOLD}).move_to([-3.5, -1.8, 0])
            self.play(*appear(k1), run_time=1.2)  # early: the copy count lands on "the copying"; the number follows
            c.wait_until("quick with accumulator", nth=1)

            k2 = T("cells copied by @: 0", 36, t2c={"0": GREEN})
            k2.move_to([3.5, -1.8, 0]).align_to(k1, DOWN)
            self.play(*appear(k2), run_time=1.0)
            self.play(FlashAround(k2[-1], color=GREEN, time_width=1.5), run_time=min(1.2, c.until(floor=0.4)))

    # ------------------------------------------------------------ c4.speed.2
    def board(self):
        with self.say("c4.speed.2") as c:
            sb = filled_board()
            self.sb = sb
            c.wait_until("speedup")
            sweep_clear(self, time_span(FadeIn(sb, shift=0.2 * UP), 0.6, 1.5))  # early: the scoreboard returns whole
            c.wait_until("secs")

            old = sb.cells[1][1]
            cell_pos = old.get_center()
            quick = Mono("quick", 28, color=DIM)
            target = old.copy().scale(28 / 44).set_color(DIM)
            row = VGroup(quick, target).arrange(RIGHT, buff=0.2)
            row.move_to([old.get_x(), old.get_y() - 0.52, 0])
            quick.align_to(target, DOWN)
            self.play(old.animate.scale(28 / 44).set_color(DIM).move_to(target), run_time=1.5)
            self.play(*appear(quick, shift=None), run_time=0.8)
            c.wait_until("five three")

            new = T("0.53 s", 44, GOLD).move_to(cell_pos)
            self.play(*appear(new), run_time=1.2)
            c.wait_until("quarter")
            self.play(FlashAround(new, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("reading")

            tag = VGroup(T("the notes' summary;", 28, color=DIM),
                         T("our reading: quik", 28, color=DIM, t2c={"quik": YELLOW}))
            tag.arrange(DOWN, buff=0.12).move_to([4.65, -2.95, 0])
            self.play(*appear(tag), run_time=1.2)
            c.wait_until("cell")

            self.play(FlashAround(VGroup(sb.row_labels[1], *sb.cells[1][:1], new), color=YELLOW,
                                  time_width=1.5), run_time=1.5)
            same = T("same for quik", 28, GREEN).move_to([sb.cells[1][0].get_x(), quick.get_y(), 0])
            c.wait_until("scoreboard")
            self.play(*appear(same), run_time=1.0)  # early: the tag sits on the cell the line names; "same" follows
            self.old, self.new, self.tags = old, new, [quick, tag, same]

    # ------------------------------------------------------------ c4.speed.3
    def surprise(self):
        sb, old, new = self.sb, self.old, self.new
        with self.say("c4.speed.3", gap=1.6) as c:
            c.wait_until("Pascal")
            sb.cells[1].remove(old)
            self.play(*disappear(old, *self.tags), run_time=0.7)
            self.play(FadeOut(sb, new, shift=0.6 * UP, scale=0.6), run_time=0.9)

            x0 = -0.7
            arr = array_icon().move_to([-3.7, 0.7, 0])
            plab = T("Pascal quicksort on arrays (Sedgewick)", 30).move_to([x0, 1.3, 0], aligned_edge=LEFT)
            pbar = Rectangle(width=6.5, height=0.42).set_stroke(width=0).set_fill(BLUE, 0.8)
            pbar.move_to([x0, 0.7, 0], aligned_edge=LEFT)
            self.play(*appear(arr, plab, lag=0.3), run_time=1.2)
            self.play(GrowFromEdge(pbar, LEFT), run_time=1.5)
            c.wait_until("slightly faster")

            cap = T("only slightly faster", 36, YELLOW).move_to([3.0, -2.7, 0])
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("quick with accumulator")

            chain = chain_icon().move_to([-3.7, -0.9, 0])
            qlab = Mono("quik", 30, color=YELLOW).move_to([x0, -0.3, 0], aligned_edge=LEFT)
            qbar = Rectangle(width=7.2, height=0.42).set_stroke(width=0).set_fill(TEAL, 0.8)
            qbar.move_to([x0, -0.9, 0], aligned_edge=LEFT)
            self.play(*appear(chain, qlab, lag=0.3), run_time=1.0)
            self.play(GrowFromEdge(qbar, LEFT), run_time=1.3)
            c.wait_until("lists cost")

            self.play(FlashAround(chain, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("than arrays")

            tags = [T("new memory", 28, color=DIM).next_to(cell, UP if i == 1 else DOWN, buff=0.3)
                    for i, cell in enumerate(chain.cells)]
            anims = []
            for i, (box, tg) in enumerate(zip(chain.boxes, tags)):
                o = i * 0.6
                anims.append(time_span(box.animate.set_fill(YELLOW, 0.7), o, o + 0.6))
                anims.append(time_span(FadeIn(tg, shift=0.2 * DOWN), o, o + 0.8))
            self.play(*anims, run_time=2.0)  # early: the cells light as lists are said to cost; "new memory" follows
            c.wait_until("dominant")

            title = T("comparisons dominate", 48, GOLD).move_to(UP * 3.2)
            bal = self.balance()
            sweep_clear(self, time_span(FadeIn(title, shift=0.2 * DOWN), 0.6, 1.4),
                        time_span(FadeIn(bal), 0.8, 1.6), run_time=1.6)
            c.wait_until("strings")

            n1 = Mono("Smithson-Whitworth, Alexandra", 40, color=YELLOW)
            n2 = Mono("Smithson-Whitworth, Alexander", 40, color=YELLOW)
            n1.move_to([0, -1.45, 0])
            n2.move_to([0, -2.25, 0]).align_to(n1, LEFT)
            self.play(*appear(n1, n2, lag=0.3), run_time=1.0)

            box = Rectangle(width=0.4, height=1.45).set_stroke(BLUE, 3).set_fill(BLUE, 0.2)
            box.set_z_index(-1).move_to([n1[0].get_x(), -1.85, 0])
            one = T("one comparison", 32, color=DIM).move_to([0, -3.25, 0])
            self.play(FadeIn(box), *appear(one, shift=None), run_time=0.6)

            N = 27
            def step(m, a):
                k = min(int(a * N), N - 1)
                m.set_x(n1[k].get_x())
            self.play(UpdateFromAlphaFunc(box, step), run_time=max(1.5, c.until(floor=0.5) - 0.8),
                      rate_func=linear)
            self.play(*recolor([n1[26], n2[26]], GOLD), restyle(box, outline=GOLD),
                      run_time=min(0.7, c.until(floor=0.3)))

    def balance(self):
        P = np.array([0, 1.6, 0])
        th, L = 0.2, 2.8
        le = P + L * np.array([-np.cos(th), -np.sin(th), 0])
        re = P + L * np.array([np.cos(th), np.sin(th), 0])
        beam = Line(le, re).set_stroke(FG, 5)
        fulc = Polygon(P, P + [-0.45, -1.3, 0], P + [0.45, -1.3, 0]).set_stroke(DIM, 3).set_fill(DIM, 0.3)
        heavy = Square(1.0).set_stroke(GOLD, 3).set_fill(GOLD, 0.7).move_to(le + 0.8 * DOWN)
        light = Square(0.45).set_stroke(DIM, 3).set_fill(DIM, 0.5).move_to(re + 0.525 * DOWN)
        s1 = Line(le, heavy.get_top()).set_stroke(FG, 2)
        s2 = Line(re, light.get_top()).set_stroke(FG, 2)
        hl = T("comparisons", 30, GOLD).next_to(heavy, DOWN, buff=0.2)
        ll = T("list overheads", 30, DIM).next_to(light, DOWN, buff=0.2)
        return VGroup(fulc, beam, s1, s2, heavy, light, hl, ll)
