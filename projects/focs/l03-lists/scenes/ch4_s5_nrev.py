"""Chapter 4, scene 5: reversing the natural way (nrev). Clips c4.nrev.1 - c4.nrev.3.

STATUS: built (all 3 clips); vk check clean (59.5 s vs 54.9 s narration; ~3.5 s end-shot tail). Trace style as ch3_s3_trace: Code size 40, lines left-aligned on a
common baseline grid, DIM \\Rightarrow column, each line born from a copy of the one above.

- nrev.1: `[1; 2; 3]` and, on a copy, `[3; 2; 1]` (the 1 and the 3 swap on arcs). The definition
  (size 44) + its reply; YELLOW box slides `[] -> []`, `x::xs`, `(nrev xs)`, `@ [x]`; `@` -> GOLD.
- nrev.2: code shrinks to the top; cells 1 | 2 3 with braces `x` / `xs`; the tail swaps
  (`xs` -> `nrev xs`), the 1 arcs to the back; GREEN on {works}; `nrev [1; 2; 3]` and its reply
  `- : int list = [3; 2; 1]` (numbers fly out of the cells).
- nrev.3: the input rises to trace line 0; lines 1-5 born from the line above; box on the peeled
  heads; {but}: every `@` -> GOLD; "adds there": one flash per step's `@`.
- End shot (s6_cost opens on it): `(([] @ [3]) @ [2]) @ [1]` alone, Code size 50, centred (0, 2.9),
  syntax colours, all three `@` GOLD.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

NREV = """let rec nrev = function
  | [] -> []
  | x::xs -> (nrev xs) @ [x]"""
NREV_REPLY = "val nrev : 'a list -> 'a list = <fun>"

TRACE = ["nrev [1; 2; 3]",
         "nrev [2; 3] @ [1]",
         "(nrev [3] @ [2]) @ [1]",
         "((nrev [] @ [3]) @ [2]) @ [1]",
         "(([] @ [3]) @ [2]) @ [1]",
         "[3; 2; 1]"]
SIZE = 40                                      # trace rows, as ch3_s3_trace
BASE = [2.75, 1.95, 1.15, 0.35, -0.45, -1.25]  # baseline of each trace row
ARROW_GAP = 0.3

S = 1.5          # cell side (clip 2)
CELL_Y = 0.45
IN_BASE, OUT_BASE = -2.1, -2.9                 # `nrev [1; 2; 3]` and its reply
END_SIZE, END_POS = 50, np.array([0.0, 2.9, 0.0])

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


# ── helpers (local to this scene) ───────────────────────────────────────────────
def baseline(code):
    """y of the text baseline of a Code."""
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def implies():
    return MathTex(r"\Rightarrow", font_size=64, color=DIM)


def hbox(glyphs, color, cy, height, pad=0.12, fill=0.2):
    """P8 highlight box: thin stroke, faint fill, behind the text, fixed height."""
    g = VGroup(*glyphs)
    r = Rectangle(width=g.width + 2 * pad, height=height, stroke_color=color, stroke_width=2.5)
    r.set_fill(color, opacity=fill).set_z_index(-1)
    return r.move_to([g.get_x(), cy, 0])


def make_cell(v, color):
    sq = Square(side_length=S, stroke_color=color, stroke_width=4).set_fill(BG, 1)
    val = value_label(v, size=60).move_to(sq)
    g = VGroup(sq, val)
    g.sq, g.val = sq, val
    return g


class NaiveReverse(NarratedScene):
    def construct(self):
        self.definition()   # c4.nrev.1
        self.example()      # c4.nrev.2
        self.trace()        # c4.nrev.3
        self.end_shot()

    # ── a Code born from pieces of other things (P11) ──────────────────────────
    def birth(self, dst, maps, run_time, extra=(), shift=0.15 * DOWN):
        """maps: (source mobject, dst substring, nth, path_arc). The mapped glyphs of dst fly out
        of copies of their sources; the rest of dst fades in. dst ends on screen as one piece."""
        used, anims, temps = set(), [], []
        for src, sub, nth, arc in maps:
            t = dst.find(sub, nth=nth)
            used.update(id(g) for g in t)
            anims.append(TransformFromCopy(src, t, path_arc=arc))
            temps.append(t)
        rest = [g for g in dst.text if id(g) not in used]
        if rest:
            r = VGroup(*rest)
            anims.append(FadeIn(r, shift=shift))
            temps.append(r)
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*temps)
        self.add(dst)

    def code_box(self, sub, line, scale=1.0):
        cy = self.code.find("[", line=line).get_y()
        return hbox(self.code.find(sub), YELLOW, cy, 0.74 * scale, pad=0.2 * scale)

    def row_box(self, k, sub, nth=0, color=YELLOW):
        row = self.rows[k]
        return hbox(row.find(sub, nth=nth), color, row.find("[").get_y(), 0.66, pad=0.17)

    # ── c4.nrev.1 ───────────────────────────────────────────────────────────────
    def definition(self):
        ex_src, ex_dst = Code("[1; 2; 3]", size=44), Code("[3; 2; 1]", size=44)
        arrow = MathTex(r"\Rightarrow", font_size=64, color=DIM)
        gap = 0.5
        total = ex_src.width + gap + arrow.width + gap + ex_dst.width
        left = -total / 2
        put(ex_src, left, 2.6)
        arrow.move_to([ex_src.get_right()[0] + gap + arrow.width / 2, 2.6 + 0.15, 0])
        put(ex_dst, arrow.get_right()[0] + gap, 2.6)
        self.example_row = [ex_src, arrow, ex_dst]

        code = self.code = Code(NREV, size=44).move_to([0, 0.15, 0])
        reply = self.def_reply = Code(NREV_REPLY, size=32).move_to([0, -2.35, 0])
        code.find("nrev", line=2).set_color(YELLOW)     # the name is YELLOW in its definition and calls
        reply.find("nrev").set_color(YELLOW)

        with self.say("c4.nrev.1") as c:
            # {task} "Now, reversing a list."  The 1 and the 3 swap places.
            self.play(FadeIn(ex_src, shift=0.2 * DOWN), run_time=0.8)
            self.birth(ex_dst, [(ex_src.find("["), "[", 0, 0),
                                (ex_src.find("1"), "1", 0, -1.1),
                                (ex_src.find(";", nth=0), ";", 0, 0),
                                (ex_src.find("2"), "2", 0, 0),
                                (ex_src.find(";", nth=1), ";", 1, 0),
                                (ex_src.find("3"), "3", 0, 1.1),
                                (ex_src.find("]"), "]", 0, 0)],
                       run_time=max(0.8, min(1.6, c.until("most natural") - 0.1)),
                       extra=[FadeIn(arrow)])
            # "Here's the most natural way, a function called en-rev."
            c.wait_until("most natural")
            self.play(FadeIn(code, shift=0.2 * UP), run_time=min(1.4, 0.9 * c.until("called")))
            c.wait_until("called")
            self.play(FlashUnder(code.find("nrev"), color=YELLOW, time_width=1.5),
                      FadeIn(reply, shift=0.2 * UP), run_time=1.1)
            # {base} "The reverse of nil is nil."
            c.wait_until("base")
            box = self.box = self.code_box("[] -> []", 1)
            self.play(FadeIn(box), run_time=0.7)
            # {step} "... with head ex and tail exes,"
            c.wait_until("step")
            self.play(Transform(box, self.code_box("x::xs", 2)), run_time=0.8)
            # {tail} "first reverse the tail,"
            c.wait_until("tail")
            self.play(Transform(box, self.code_box("(nrev xs)", 2)), run_time=0.8)
            # {end} "then put ex on the end, by appending the list holding just ex."
            c.wait_until("end")
            self.play(Transform(box, self.code_box("@ [x]", 2)), run_time=0.8)
            c.wait_until("appending")
            at = code.find("@")
            self.play(*recolor(at, GOLD), FlashAround(at, color=GOLD, time_width=1.5),
                      run_time=1.2)

    # ── c4.nrev.2 ───────────────────────────────────────────────────────────────
    def example(self):
        code = self.code
        head = make_cell(1, YELLOW).move_to([-1.9, CELL_Y, 0])
        t1 = make_cell(2, BLUE).move_to([0.4, CELL_Y, 0])
        t2 = make_cell(3, BLUE).move_to([1.9, CELL_Y, 0])
        self.cells = [head, t1, t2]
        br_x = Brace(head.sq, DOWN, buff=0.15).set_color(YELLOW)
        lb_x = Mono("x", size=40, color=YELLOW).next_to(br_x, DOWN, buff=0.15)
        br_xs = Brace(VGroup(t1.sq, t2.sq), DOWN, buff=0.15).set_color(BLUE)
        lb_xs = Mono("xs", size=40, color=BLUE).next_to(br_xs, DOWN, buff=0.15)
        lb_nxs = Mono("nrev xs", size=40, color=BLUE).next_to(br_xs, DOWN, buff=0.15)
        self.labels = [br_x, lb_x, br_xs, lb_nxs]

        x0 = self.trace_left()
        self.call = put(Code(TRACE[0], size=SIZE), x0, IN_BASE)
        self.call.find("nrev").set_color(YELLOW)
        self.out = put(Code("- : int list = [3; 2; 1]", size=SIZE), x0, OUT_BASE)

        with self.say("c4.nrev.2") as c:
            # {sense} "That makes perfect sense."  The definition moves up out of the way.
            self.play(*[FadeOut(m) for m in self.example_row], FadeOut(self.def_reply),
                      FadeOut(self.box),
                      code.animate.scale(0.7).move_to([0, 2.65, 0]),
                      run_time=min(1.2, c.until("reverse one")))
            # "To ⏸ reverse one, two, three,"
            c.wait_until("reverse one")
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in self.cells],
                                  GrowFromCenter(br_x), FadeIn(lb_x, shift=0.2 * DOWN),
                                  GrowFromCenter(br_xs), FadeIn(lb_xs, shift=0.2 * DOWN),
                                  lag_ratio=0.15),
                      run_time=min(1.6, 0.9 * c.until("you reverse")))
            # "you reverse two, three, to get three, two,"
            c.wait_until("you reverse")
            box = self.box = self.code_box("(nrev xs)", 2, scale=0.7)
            p1, p2 = t1.get_center(), t2.get_center()
            self.play(FadeIn(box),
                      t1.animate(path_arc=-PI / 2).move_to(p2),
                      t2.animate(path_arc=-PI / 2).move_to(p1),
                      TransformMatchingStrings(lb_xs, lb_nxs),
                      run_time=min(1.6, 0.9 * c.until("and then put")))
            # "and then put the one on the end."
            c.wait_until("and then put")
            d_head = RIGHT * (1.5 - head.get_x())
            d_tail = LEFT * 1.9
            self.play(Transform(box, self.code_box("@ [x]", 2, scale=0.7)),
                      *[m.animate(path_arc=-PI / 3).shift(d_head) for m in (head, br_x, lb_x)],
                      *[m.animate.shift(d_tail) for m in (t1, t2, br_xs, lb_nxs)],
                      run_time=min(1.8, 0.9 * c.until("works")))
            # {works} "And it works."
            c.wait_until("works")
            self.play(*[m.sq.animate.set_stroke(GREEN) for m in self.cells],
                      FlashAround(VGroup(*[m.sq for m in self.cells]), color=GREEN,
                                  time_width=1.5),
                      FadeOut(box), run_time=1.1)
            # {reply} "En-rev of one, two, three gives three, two, one."
            c.wait_until("reply")
            self.play(FadeIn(self.call, shift=0.2 * UP), run_time=0.8)
            c.wait_until("gives")
            vals = {1: head.val, 2: t1.val, 3: t2.val}
            self.birth(self.out, [(vals[3], "3", 0, 0.5), (vals[2], "2", 0, 0.5),
                                  (vals[1], "1", 0, 0.5)],
                       run_time=min(1.6, max(0.8, c.remaining - 0.2)))

    def trace_left(self):
        """Left edge of every trace row's code (the widest row, with its arrow, is centred)."""
        widest = Code(TRACE[3], size=SIZE).width + implies().width + ARROW_GAP
        return -widest / 2 + implies().width + ARROW_GAP

    # ── c4.nrev.3 ───────────────────────────────────────────────────────────────
    def trace(self):
        x0 = self.trace_left()
        rows = self.rows = [self.call] + [put(Code(s, size=SIZE), x0, b)
                                          for s, b in zip(TRACE[1:], BASE[1:])]
        arrows = self.arrows = [None] + [implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + 0.13)
                                         for r, b in zip(rows[1:], BASE[1:])]
        risen = put(self.call.copy(), x0, BASE[0])      # trace row 0: default colour, as s3
        risen.find("nrev").set_color(FG)
        L0, L1, L2, L3, L4, L5 = rows

        with self.say("c4.nrev.3") as c:
            # {trace} "Let's trace it."  The call rises to the top; its answer waits, dimmed.
            gone = [self.code, *self.cells, *self.labels]
            self.play(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.08),
                      Transform(self.call, risen),
                      self.out.animate.set_opacity(0.35),
                      run_time=min(1.3, c.until("t1")))
            # {t1} "Each step peels off the head, and leaves an append waiting."
            c.wait_until("t1")
            self.birth(L1, [(L0.find("nrev ["), "nrev [", 0, 0),
                            (L0.find("2; 3]"), "2; 3]", 0, 0),
                            (L0.find("1"), "1", 0, -1.2)],
                       run_time=2.0, extra=[FadeIn(arrows[1], shift=0.15 * DOWN)])
            c.wait_until("append waiting")
            self.play(FlashUnder(L1.find("@ [1]"), color=YELLOW, time_width=1.5), run_time=1.2)
            # {t2} "First the one,"
            c.wait_until("t2")
            tbox = self.row_box(1, "[1]")
            self.play(FadeIn(tbox), run_time=0.6)
            # {t3} "then the two,"
            c.wait_until("t3")
            self.birth(L2, [(L1.find("nrev ["), "nrev [", 0, 0),
                            (L1.find("3]"), "3]", 0, 0),
                            (L1.find("2"), "2", 0, -1.2),
                            (L1.find("@ [1]"), "@ [1]", 0, 0)],
                       run_time=min(1.0, 0.9 * c.until("t4")),
                       extra=[FadeIn(arrows[2], shift=0.15 * DOWN),
                              Transform(tbox, self.row_box(2, "[2]"))])
            # {t4} "then the three."
            c.wait_until("t4")
            self.birth(L3, [(L2.find("(nrev ["), "(nrev [", 0, 0),
                            (L2.find("]"), "]", 0, 0),
                            (L2.find("3"), "3", 0, -1.2),
                            (L2.find("@ [2]) @ [1]"), "@ [2]) @ [1]", 0, 0)],
                       run_time=1.0,
                       extra=[FadeIn(arrows[3], shift=0.15 * DOWN),
                              Transform(tbox, self.row_box(3, "[3]"))])
            # "When we reach nil, we're left with a chain of appends."
            c.wait_until("reach nil")
            self.play(Transform(tbox, self.row_box(3, "nrev []", color=TEAL)), run_time=0.7)
            c.wait_until("left with")
            self.birth(L4, [(L3.find("(("), "((", 0, 0),
                            (L3.find("nrev []"), "[]", 0, 0),
                            (L3.find("@ [3]) @ [2]) @ [1]"), "@ [3]) @ [2]) @ [1]", 0, 0)],
                       run_time=min(1.2, 0.9 * c.until("chain of appends")),
                       extra=[FadeIn(arrows[4], shift=0.15 * DOWN), FadeOut(tbox)])
            c.wait_until("chain of appends")
            self.play(LaggedStart(*[FlashUnder(L4.find("@", nth=k), color=YELLOW, time_width=1.5)
                                    for k in range(3)], lag_ratio=0.3), run_time=1.4)
            # {t5} "Now they all run,"
            c.wait_until("t5")
            self.birth(L5, [(L4.find("3"), "3", 0, 0.4), (L4.find("2"), "2", 0, 0.4),
                            (L4.find("1"), "1", 0, 0.4), (L4.find("["), "[", 0, 0),
                            (L4.find("]", nth=3), "]", 0, 0)],
                       run_time=min(1.5, 0.9 * c.until("result")),
                       extra=[FadeIn(arrows[5], shift=0.15 * DOWN)])
            # {result} "and out comes three, two, one."
            c.wait_until("result")
            self.play(*recolor(list(L5.text), GREEN),
                      FlashAround(L5, color=GREEN, time_width=1.5),
                      self.out.animate.set_opacity(1), run_time=1.2)
            # {but} "But the end of a list is the expensive place to add things,"
            c.wait_until("but")
            ats = [g for r in rows[1:5] for k in range(r.src.count("@")) for g in r.find("@", nth=k)]
            self.play(*recolor(ats, GOLD),
                      *[FlashAround(L4.find("@", nth=k), color=GOLD, time_width=1.5)
                        for k in range(3)],
                      *[m.animate.set_opacity(0.35) for m in (L0, L5, self.out)],
                      run_time=1.3)
            # "and this function adds there at every step."
            c.wait_until("adds there")
            self.play(LaggedStart(*[FlashUnder(r.find(f"@ [{n}]"), color=GOLD, time_width=1.5)
                                    for r, n in ((L1, 1), (L2, 2), (L3, 3))], lag_ratio=0.35),
                      run_time=max(0.8, min(1.8, c.remaining - 0.1)))

    # ── the shot s6_cost opens on ───────────────────────────────────────────────
    def end_shot(self):
        L4 = self.rows[4]
        others = [m for m in self.mobjects if m is not L4]
        self.play(*[FadeOut(m) for m in others],
                  L4.animate.scale(END_SIZE / SIZE).move_to(END_POS), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(L4), run_time=1.0)
        self.wait(0.15)
