"""Chapter 5, scene 2: merging two sorted lists (the zipper). Clips c5.merge.1 – c5.merge.4.

Reusable (s3, s7, ch7): `Zipper` (two input chains stacked left, output slots right) with
`.take(which)` (smaller head steps out of its row and drops into the next output slot; its
chain closes up) and `.rest(which)` (the leftover chain slides across whole); `instant=True`
applies a move without animating. `final_zipper()` / `handover_shot()` draw the finished frame.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- the zipper
ZS = 0.6              # zipper scale
ZIP_LEFT = -6.3       # left edge of the input chains
ROW_DY = 0.65         # input rows sit at cy ± ROW_DY; the output row at cy
LANE_DY = 1.3         # heads travel above (top) / below (bottom) at cy ± LANE_DY
ZIP_Y = 0.4           # zipper centre while it is the hero (clip 1)
ZIP_Y_TRACE = 2.25    # zipper centre while the trace runs under it


class Zipper:
    """Two sorted input chains stacked on the left, an empty output row (DIM dashed slots) right.

    Zipper(top=(3, 5), bot=(4, 7, 9), cy=ZIP_Y, left=ZIP_LEFT, scale=ZS)
      .top .bot      ConsChains (top-level mobjects to add)
      .slots         VGroup of DIM dashed slot outlines (z -1)
      .slot(i)       centre of output slot i
      .heads()       the current head cells (top, bot), None for an empty side
      .take(which, instant=False) -> anims: head of "top"/"bot" leaves its row (up / down),
                     runs along the lane and drops into the next slot; its out-arrow fades; the
                     chain closes up; a link grows from the previous output cell.
      .rest(which, instant=False) -> anims: the leftover chain (incl. its []) slides across
                     whole into the next slots, and the link to it grows.
      .links         VGroup of the output links made so far
    """

    def __init__(self, top=(3, 5), bot=(4, 7, 9), cy=ZIP_Y, left=ZIP_LEFT, scale=ZS):
        self.vals = (tuple(top), tuple(bot))
        self.s, self.cy = scale, cy
        self.pitch = (CELL + PTR_W + LINK) * scale
        self.cw = (CELL + PTR_W) * scale
        self.top = ConsChain(list(top)).scale(scale)
        self.bot = ConsChain(list(bot)).scale(scale)
        k = max(1.0, 31 / (42 * scale))           # keep values readable (≥ size 30) when scaled down
        for ch in (self.top, self.bot):
            for m in [cl.label for cl in ch.cells] + [ch.nil.label]:
                m.scale(k)
        for ch, dy in ((self.top, ROW_DY), (self.bot, -ROW_DY)):
            c0 = ch.cells[0].get_center()
            ch.shift(RIGHT * (left - ch.get_left()[0]) + UP * (cy + dy - c0[1]))
        self.out_left = max(self.top.get_right()[0], self.bot.get_right()[0]) + 0.9
        n = len(top) + len(bot)
        self.slots = VGroup(*[
            DashedVMobject(Rectangle(width=self.cw, height=CELL * scale), num_dashes=16)
            .set_stroke(DIM, 2).move_to(self.slot(i)) for i in range(n)])
        self.slots.set_z_index(-1)
        self.rem = {"top": list(self.top.cells), "bot": list(self.bot.cells)}
        self.arr = {"top": list(self.top.arrows), "bot": list(self.bot.arrows)}
        self.nil = {"top": self.top.nil, "bot": self.bot.nil}
        self.chain = {"top": self.top, "bot": self.bot}
        self.out = []
        self.links = VGroup()

    def slot(self, i):
        return np.array([self.out_left + self.cw / 2 + i * self.pitch, self.cy, 0])

    def heads(self):
        return tuple(self.rem[w][0] if self.rem[w] else None for w in ("top", "bot"))

    def _link(self, a_tail, b_entry):
        return Arrow(a_tail, b_entry, buff=0, stroke_width=3, color=FG,
                     max_tip_length_to_length_ratio=0.3, tip_length=0.16 * self.s)

    def _path(self, which, start, end):
        lane = self.cy + (LANE_DY if which == "top" else -LANE_DY)
        return VMobject().set_points_as_corners(
            [start, [start[0], lane, 0], [end[0], lane, 0], end])

    def take(self, which, instant=False):
        head = self.rem[which].pop(0)
        arr = self.arr[which].pop(0)
        i = len(self.out)
        end = self.slot(i)
        new = None
        if self.out:
            entry = head.entry() + (end - head.get_center())
            new = self._link(self.out[-1].tail_start(), entry)
        self.out.append(head)
        closers = self.rem[which] + self.arr[which] + [self.nil[which]]
        if instant:
            head.move_to(end)
            self.chain[which].remove(arr)
            for m in closers:
                m.shift(LEFT * self.pitch)
            if new is not None:
                self.links.add(new)
            return []
        anims = [MoveAlongPath(head, self._path(which, head.get_center(), end)), FadeOut(arr)]
        anims += during([m.animate.shift(LEFT * self.pitch) for m in closers], 0.4, 1.0)
        if new is not None:
            self.links.add(new)
            anims += during([GrowArrow(new)], 0.75, 1.0)
        return anims

    def rest(self, which, instant=False):
        parts = self.rem[which] + self.arr[which] + [self.nil[which]]
        first = self.rem[which][0]
        d = self.slot(len(self.out)) - first.get_center()
        entry = first.entry() + d
        new = self._link(self.out[-1].tail_start(), entry)
        self.links.add(new)
        self.out += self.rem[which]
        self.rem[which] = []
        if instant:
            for m in parts:
                m.shift(d)
            return []
        anims = [MoveAlongPath(m, self._path(which, m.get_center(), m.get_center() + d)) for m in parts]
        return anims + during([GrowArrow(new)], 0.8, 1.0)


def final_zipper(cy=ZIP_Y_TRACE):
    """The finished zipper: top row just [], output 3 → 4 → 5 → 7 → 9 → [] (VGroup)."""
    z = Zipper(cy=cy)
    for w in ("top", "bot", "top"):
        z.take(w, instant=True)
    z.rest("bot", instant=True)
    return z


def done_tick(z):
    return check_mark(GREEN).move_to(z.nil["bot"].get_center() + UP * 0.85)


# ---------------------------------------------------------------- code + trace
MERGE_SRC = """let rec merge = function
  | [], ys -> ys
  | xs, [] -> xs
  | x::xs, y::ys ->
      if x <= y then
        x :: merge (xs, y::ys)
      else
        y :: merge (x::xs, ys)"""
TYPE_SRC = "val merge : 'a list * 'a list -> 'a list = <fun>"

TSIZE = 30                      # trace rows
L = -5.6                        # left edge of the trace code column
ROW_Y = [0.25, -0.4, -1.05, -1.7, -2.35]
REPLY_Y = -3.1
QX = 3.5                        # left edge of the comparison notes
ROWS = ["merge ([3; 5], [4; 7; 9])",
        "3 :: merge ([5], [4; 7; 9])",
        "3 :: 4 :: merge ([5], [7; 9])",
        "3 :: 4 :: 5 :: merge ([], [7; 9])",
        "3 :: 4 :: 5 :: [7; 9]"]
QS = [(r"3 \le 4\,?", "yes"), (r"5 \le 4\,?", "no"), (r"5 \le 7\,?", "yes")]


def ycode(src, size):
    """Code with every `merge` YELLOW."""
    c = Code(src, size=size)
    k = 0
    while True:
        try:
            g = c.find("merge", nth=k)
        except ValueError:
            break
        g.set_color(YELLOW)
        k += 1
    return c


def trace_row(i):
    code = ycode(ROWS[i], TSIZE)
    code.move_to([0, ROW_Y[i], 0]).shift(RIGHT * (L - code.get_left()[0]))
    return code


def trace_arrow(i):
    a = MathTex(r"\Rightarrow", font_size=48, color=DIM)
    return a.move_to([L - 0.45, ROW_Y[i], 0])


def question(i):
    q = MathTex(QS[i][0], font_size=44, color=GOLD)
    return q.move_to([0, ROW_Y[i + 1], 0]).shift(RIGHT * (QX - q.get_left()[0]))


def answer(i, q):
    a = T(QS[i][1], size=34, color=GOLD).next_to(q, RIGHT, buff=0.25)
    a.shift(UP * (q.get_bottom()[1] - a[-1].get_bottom()[1]))
    return a


def free_note():
    f = T("free", size=34, color=GREEN)
    return f.move_to([0, ROW_Y[4], 0]).shift(RIGHT * (QX - f.get_left()[0]))


def reply():
    r = Code("- : int list = [3; 4; 5; 7; 9]", size=TSIZE)
    return r.move_to([0, REPLY_Y, 0]).shift(RIGHT * (L - r.get_left()[0]))


def counter():
    t = T("comparisons: 3", size=34, color=GOLD)
    return t.move_to([0, REPLY_Y, 0]).shift(RIGHT * (6.3 - t.get_right()[0]))


def handover_shot():
    """Last frame: finished zipper + tick, the trace with its notes, the reply, the counter."""
    z = final_zipper()
    parts = [z.top, z.bot, z.links, done_tick(z)]
    parts += [trace_row(i) for i in range(5)] + [trace_arrow(i) for i in range(1, 5)]
    for i in range(3):
        q = question(i)
        parts += [q, answer(i, q)]
    parts += [free_note(), reply(), counter()]
    return VGroup(*parts)


# ---------------------------------------------------------------- the scene
class MergeTwo(NarratedScene):
    def construct(self):
        self.zip_intro()
        self.code_walk()
        self.type_reply()
        self.trace()

    # c5.merge.1 --------------------------------------------------------------
    def zip_intro(self):
        z = self.z = Zipper()
        with self.say("c5.merge.1") as c:
            self.play(*appear(z.top, z.bot, lag=0.4, shift=None), run_time=1.6)
            c.wait_until("Three, five")
            self.play(FlashAround(z.top, run_time=1.2, time_width=1.5))
            c.wait_until("four, seven")
            self.play(FlashAround(z.bot, run_time=1.2, time_width=1.5))

            c.wait_until("how")
            self.q = T("?", size=64, color=YELLOW).move_to(
                (z.slot(0) + z.slot(4)) / 2 + UP * 0.95)
            self.play(FadeIn(z.slots), *appear(self.q), run_time=1.2)

            c.wait_until("heads")
            h1, h2 = z.heads()
            others = [m for m in (*z.top.cells[1:], *z.bot.cells[1:], *z.top.arrows, *z.bot.arrows,
                                  z.top.nil, z.bot.nil)]
            self.le = MathTex(r"\le\,?", font_size=40, color=YELLOW).move_to(
                [h1.get_x(), z.cy, 0])
            self.others = others
            self.play(*self.head_style(YELLOW, YELLOW), *set_alpha(others, 0.5),
                      run_time=1.5)
            self.play(*appear(self.le), run_time=0.8)
            c.wait_until("compare the two front")
            self.play(*flash([h1, h2]), run_time=1.5)

            c.wait_until("zip")
            self.cap = T("compare the heads, take the smaller, repeat", size=34)
            self.cap.move_to([0, -1.7, 0])
            self.play(*appear(self.cap), run_time=1.2)

    def head_style(self, outline, label):
        anims = []
        for h in self.z.heads():
            anims += [restyle(h.box, outline=outline), restyle(h.ptr, outline=outline)]
            anims += recolor(h.label, label)
        return anims

    # c5.merge.2 --------------------------------------------------------------
    def code_walk(self):
        z = self.z
        with self.say("c5.merge.2") as c:
            self.play(*disappear(self.q, self.le), FadeOut(z.slots),
                      *self.head_style(BLUE, FG), *set_alpha(self.others, 1),
                      self.cap.animate.move_to([0, -3.3, 0]), run_time=1.0)
            for ch in (z.top, z.bot):
                ch.generate_target()
                ch.target.shift(UP * 0.55)
            code = self.code = ycode(MERGE_SRC, 30)
            code.move_to([0, 0.95, 0]).shift(RIGHT * (6.4 - code.get_right()[0]))
            self.play(*during([MoveToTarget(z.top), MoveToTarget(z.bot)], 0, 0.6),
                      *during(appear(code, shift=None), 0.45, 1.0), run_time=1.6)

            c.wait_until("nil1")
            box = self.box = token_box(code.find("[], ys -> ys", line=1), code.line(1))
            self.play(FadeIn(box), run_time=1.0)
            inset_lab = T("as in append", size=28, color=DIM)
            inset = Code("| [], ys    -> ys", size=28).set_color(DIM)
            inset.move_to([0, -1.1, 0]).shift(RIGHT * (ZIP_LEFT - inset.get_left()[0]))
            inset_lab.next_to(inset, UP, buff=0.22, aligned_edge=LEFT)
            self.inset = VGroup(inset_lab, inset)
            c.wait_until(own_word=inset_lab)
            self.play(*appear(inset_lab, inset, lag=0.3), run_time=1.2)

            steps = [("nil2", "xs, [] -> xs", 2), ("cons", "x::xs, y::ys", 3),
                     ("test", "x <= y", 4), ("left", "x :: merge (xs, y::ys)", 5),
                     ("right", "y :: merge (x::xs, ys)", 7)]
            for cue, sub, ln in steps:
                c.wait_until(cue)
                self.play(Transform(box, token_box(code.find(sub, line=ln), code.line(ln))),
                          run_time=1.0)
                if cue == "cons":
                    c.wait_until("Call them")
                    self.play(*flash([code.find("x", line=3), code.find("y", line=3)]), run_time=1.5)

    # c5.merge.3 --------------------------------------------------------------
    def type_reply(self):
        code = self.code
        with self.say("c5.merge.3") as c:
            rep = self.rep = Code(TYPE_SRC, size=28).move_to([0, -2.3, 0])
            self.play(*during(disappear(self.cap, self.inset, self.box), 0, 0.45),
                      *during(appear(rep), 0.45, 1.0), run_time=min(1.4, c.until("pair")))
            c.wait_until("pair")
            g = rep.find("'a list * 'a list")
            self.brace = span_brace(g.get_corner(DL), g.get_corner(DR), DOWN, color=GREEN)
            self.blab = T("a pair of lists", size=30).next_to(self.brace, DOWN, buff=0.12)
            self.play(GrowFromCenter(self.brace), *appear(self.blab), run_time=1.2)
            c.wait_until("poly")
            le = code.find("<=")
            self.play(FlashAround(le, run_time=2, time_width=1.5), *recolor(le, YELLOW))

    # c5.merge.4 --------------------------------------------------------------
    def trace(self):
        z = self.z
        with self.say("c5.merge.4") as c:
            ref = Zipper(cy=ZIP_Y_TRACE)
            z.top.target, z.bot.target = ref.top, ref.bot
            z.cy, z.out_left = ref.cy, ref.out_left
            z.slots = ref.slots
            rows = [trace_row(i) for i in range(5)]
            sweep_clear(self, MoveToTarget(z.top), MoveToTarget(z.bot), FadeIn(z.slots),
                        *appear(rows[0], shift=None), keep=[z.top, z.bot],
                        run_time=min(2.2, c.until("s1")))

            nexts = ["s2", "s3", "empty"]
            word = ["Yes", "No", "Yes"]
            sides = ["top", "bot", "top"]
            self.qa = []
            for i in range(3):
                c.wait_until(f"s{i + 1}")
                q = question(i)
                self.play(*appear(q), *flash(list(z.heads())), run_time=1.0)
                c.wait_until(word[i], nth=0)
                a = answer(i, q)
                self.qa += [q, a]
                derive(self, rows[i], rows[i + 1], *z.take(sides[i]), *appear(trace_arrow(i + 1), shift=None),
                       *appear(a), run_time=max(1.8, min(2.6, c.until(nexts[i]))), split=0.55)

            c.wait_until("empty")
            self.play(FlashAround(z.top.nil, color=TEAL, run_time=1.2, time_width=1.5),
                      FlashAround(rows[3].find("[]"), color=TEAL, run_time=1.2, time_width=1.5))

            c.wait_until("rest")
            free = free_note()
            derive(self, rows[3], rows[4], *z.rest("bot"), *appear(trace_arrow(4), shift=None),
                   *appear(free), run_time=min(2.8, c.until("done")), split=0.6)

            c.wait_until("done")
            tick = done_tick(z)
            rep = reply()
            self.play(FadeOut(z.slots), GrowFromCenter(tick), *appear(rep), run_time=1.2)
            c.wait_until("three")
            qs = [m for k, m in enumerate(self.qa) if k % 2 == 0]
            self.play(*appear(counter()), *flash(qs, color=GOLD), run_time=1.4)

        # handover: the frame becomes handover_shot() exactly (same geometry, no animation)
        self.clear()
        self.add(handover_shot())
        self.wait(1.0)
