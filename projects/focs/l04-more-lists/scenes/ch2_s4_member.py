"""Chapter 2, scene 4: member, linear search in OCaml, traced on the running chain. Clips c2.mem.1 – c2.mem.5.

Layout
  A (mem.1–2): member's code big and centred, a YELLOW box walking it; OCaml's reply under it
     with three braces.
  B (mem.3):   code small top-left; the s1 chain at ORIGIN with its GOLD marker; two flat trace
     columns below it (looking for 9 on the left, for 6 on the right).
  C (mem.4):   chain and the 6 column clear; member's column moves up, ch1's take trace (DIM)
     beside it with its waiting conses underlined; GREEN "iterative", GOLD costs under member.
  D (mem.5):   code big again with the reply under it; both 'a boxed PINK, x = y boxed YELLOW,
     a "?" between.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = """let rec member x = function
  | [] -> false
  | y::l ->
      if x = y then true
      else member x l"""
REPLY = "val member : 'a -> 'a list -> bool = <fun>"

NINE = ["member 9 [3; 5; 9; 4; 7]", "member 9 [5; 9; 4; 7]", "member 9 [9; 4; 7]", "true"]
SIX = ["member 6 [3; 5; 9; 4; 7]", "…", "member 6 []", "false"]
TAKE = ["take 2 [3; 5; 9; 4; 7]", "3 :: take 1 [5; 9; 4; 7]", "3 :: 5 :: take 0 [9; 4; 7]",
        "3 :: 5 :: []", "[3; 5]"]

TS = 28            # member's trace code size
TTS = 28           # take's trace (small, DIM)
PITCH = 0.52       # trace row pitch
XL = -6.05         # left edge of member's columns
EDGE = 6.5         # right edge for the right-hand column
CHAIN_Y = -0.4     # the s1 chain, nudged down so its marker clears the small code
Y0 = -1.4          # first trace row under the chain (phase B)
Y0C = 0.55         # first trace row in phase C
SHRINK = 0.7       # code 40 -> 28


def place(mob, x_left, y):
    return mob.move_to([x_left + mob.width / 2, y, 0])


def implies(x_left, y):
    a = MathTex(r"\Rightarrow", font_size=34, color=DIM)
    return a.move_to([x_left - 0.15 - a.width / 2, y, 0])


def trace_rows(srcs, x_left, y0, reply=None, size=TS):
    """Rows of a flat trace, left-aligned at x_left; OCaml's reply sits on the last row,
    to the right of the final value."""
    rows, arrows = [], []
    for i, s in enumerate(srcs):
        if s == "…":
            r = MathTex(r"\cdots", font_size=40, color=FG)
        else:
            r = Code(s, size=size)
        place(r, x_left, y0 - i * PITCH)
        rows.append(r)
        arrows.append(implies(x_left, y0 - i * PITCH) if i else None)
    rep = None
    if reply:
        rep = Code(reply, size=size)
        place(rep, x_left + 1.9, y0 - (len(srcs) - 1) * PITCH)
    return rows, arrows, rep


def col_width(rows, rep=None):
    return max([r.get_right()[0] for r in rows] + ([rep.get_right()[0]] if rep else [])) - rows[0].get_left()[0]


def loop_arrow(points, color=YELLOW, width=5):
    p = TipableVMobject(color=color, stroke_width=width)
    p.set_points_smoothly([np.array(q, dtype=float) for q in points])
    p.add_tip(tip_length=0.24, tip_width=0.24)
    return p


class Member(NarratedScene):
    def construct(self):
        code = Code(SRC, size=40).move_to(UP * 0.3)
        self.code = code
        self.clip1(code)
        self.clip2(code)
        self.clip3(code)
        self.clip4(code)
        self.clip5(code)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c2.mem.1: the code, x, function's unnamed list, the two clauses ──────────
    def clip1(self, code):
        m0 = code.find("member", line=0)
        xg = code.find("x", line=0)
        fn = code.find("function", line=0)
        tail_glyphs = code.find("= function", line=0)
        line0 = code.line(0)
        with self.say("c2.mem.1") as c:
            self.play(FadeIn(code, shift=0.25 * UP), run_time=1.6)
            c.wait_until("called member")
            self.play(FlashUnder(m0, color=YELLOW), run_time=1.2)

            # {x}: the item
            c.wait_until("x")
            box = token_box(xg, line0)
            top = line0.get_top()[1]
            item = T("the item", 36, YELLOW).move_to([xg.get_x() - 0.85, top + 1.0, 0])
            item_arrow = Arrow(item.get_bottom() + RIGHT * 0.4, [xg.get_x(), box.get_top()[1] + 0.02, 0],
                               buff=0.08, stroke_width=4, color=YELLOW, tip_length=0.18,
                               max_tip_length_to_length_ratio=0.4)
            self.play(FadeIn(box), run_time=0.8)
            self.play(FadeIn(item, shift=0.25 * DOWN), GrowArrow(item_arrow), run_time=1.0)

            # {function}: the list arrives as an unnamed second argument
            c.wait_until("function")
            self.play(Transform(box, token_box(fn, line0)), run_time=1.0)
            c.wait_until("supplies the list")
            S = 1.0
            self.play(*[g.animate.shift(RIGHT * S) for g in tail_glyphs],
                      box.animate.shift(RIGHT * S), run_time=1.0)
            gap_l = xg.get_right()[0]
            gap_r = tail_glyphs[0].get_left()[0]
            slot = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.72, height=box.height - 0.12),
                                  num_dashes=18).set_stroke(TEAL, 3)
            slot.move_to([(gap_l + gap_r) / 2, box.get_y(), 0])
            lst = T("the list", 36, TEAL).move_to([slot.get_x() + 0.95, item.get_y(), 0])
            lst_arrow = Arrow(lst.get_bottom() + LEFT * 0.4, slot.get_top() + UP * 0.02,
                              buff=0.08, stroke_width=4, color=TEAL, tip_length=0.18,
                              max_tip_length_to_length_ratio=0.4)
            self.play(Create(slot), FadeIn(lst, shift=0.25 * DOWN), GrowArrow(lst_arrow), run_time=1.1)

            # {nil}: the empty case
            c.wait_until("nil")
            self.play(Transform(box, token_box(code.find("| [] -> false"), code.line(1))), run_time=1.0)

            # {cons}: head y, tail l
            c.wait_until("cons")
            yg = code.find("y", line=2)
            lg = code.find("l", line=2)
            base = lg.get_bottom()[1]
            x0 = code.line(2).get_right()[0] + 1.0
            ty = yg.copy().set_color(YELLOW)
            ty.shift(RIGHT * (x0 - ty.get_left()[0]))
            head = T("head", 38, YELLOW).next_to(ty, RIGHT, buff=0.18)
            head.shift(UP * (base - head.get_bottom()[1]))
            tl = lg.copy().set_color(TEAL)
            tl.shift(RIGHT * (head.get_right()[0] + 0.75 - tl.get_left()[0]))
            tail = T("tail", 38, TEAL).next_to(tl, RIGHT, buff=0.18)
            tail.shift(UP * (base - tail.get_bottom()[1]))
            self.play(Transform(box, token_box(code.find("y::l", line=2), code.line(2))), run_time=0.9)
            c.wait_until("a head")
            self.play(TransformFromCopy(yg, ty), FadeIn(head, shift=0.2 * LEFT), run_time=0.9)
            c.wait_until("and a tail")
            self.play(TransformFromCopy(lg, tl), FadeIn(tail, shift=0.2 * LEFT), run_time=0.9)
        self.box, self.tags = box, (ty, head, tl, tail)
        self.slot_parts = (S, tail_glyphs, (slot, item, item_arrow, lst, lst_arrow))

    # ── c2.mem.2: the test, the recursive call, the reply and its three parts ─────
    def clip2(self, code):
        box = self.box
        m0 = code.find("member", line=0)
        with self.say("c2.mem.2") as c:
            # {test}; the unnamed-list slot closes up again
            S, tail_glyphs, slot_parts = self.slot_parts
            self.play(Transform(box, token_box(code.find("if x = y then true"), code.line(3))),
                      *[g.animate.shift(LEFT * S) for g in tail_glyphs],
                      FadeOut(*slot_parts), run_time=1.2)

            c.wait_until("else")
            self.play(Transform(box, token_box(code.find("else member x l"), code.line(4))),
                      FadeOut(*self.tags), run_time=1.0)
            c.wait_until("with member")
            y4 = code.line(4).get_y()
            L = code.get_left()[0]
            ytop = code.line(0).get_top()[1]
            loop = loop_arrow([
                [box.get_left()[0] - 0.08, y4, 0],
                [L - 0.45, y4 + 0.12, 0],
                [L - 0.85, (y4 + ytop) / 2, 0],
                [L - 0.4, ytop + 0.5, 0],
                [m0.get_x() - 1.0, ytop + 0.62, 0],
                [m0.get_x() - 0.15, m0.get_top()[1] + 0.12, 0],
            ])
            self.play(Create(loop), run_time=1.4)
            self.play(FlashAround(m0, color=YELLOW), run_time=1.0)

            # {reply}
            c.wait_until("reply")
            reply = self.make_reply()
            reply.move_to(DOWN * 1.55)
            self.play(FadeOut(box, loop, shift=0.45 * UP), code.animate.shift(0.45 * UP),
                      time_span(FadeIn(reply, shift=0.25 * UP), 0.5, 1.5), run_time=1.5)

            # {read}: three braces
            c.wait_until("read")
            parts = [
                (reply.find("'a", nth=0), YELLOW, ["the item"]),
                (reply.find("'a list"), TEAL, ["a list of", "the same type"]),
                (reply.find("bool"), GREEN, ["yes or no"]),
            ]
            cues = ["an item", "a list of items", "a yes or no"]
            braces = []
            for (glyphs, col, words), cue in zip(parts, cues):
                br = Brace(VGroup(*glyphs), DOWN, buff=0.12, color=col)
                lab = VGroup(*[T(w, 32, col) for w in words]).arrange(DOWN, buff=0.1)
                lab.next_to(br, DOWN, buff=0.12)
                braces += [br, lab]
                c.wait_until(cue)
                self.play(GrowFromCenter(br), FadeIn(lab, shift=0.2 * UP), run_time=0.8)
        self.reply = reply

    def make_reply(self):
        r = Code(REPLY, size=34)
        r.find("member").set_color(YELLOW)
        return r

    # ── c2.mem.3: run it, looking for 9, then for 6 ──────────────────────────────
    def clip3(self, code):
        chain = ConsChain([3, 5, 9, 4, 7]).shift(UP * CHAIN_Y)
        ptr = marker(GOLD, scale=0.24).move_to(above(chain.cells[0].box))

        def at_cell(i):
            return above(chain.cells[i].box)

        rows, arrs, rep = trace_rows(NINE, XL, Y0, reply="- : bool = true")
        rows[3].set_color(GREEN)
        probe, _, probe_rep = trace_rows(SIX, 0, Y0, reply="- : bool = false")
        xr = EDGE - col_width(probe, probe_rep)
        srows, sarrs, srep = trace_rows(SIX, xr, Y0, reply="- : bool = false")
        srows[3].set_color(RED)
        self.six = (srows, sarrs, srep, xr)

        with self.say("c2.mem.3") as c:
            # {run}: code to the corner, the chain and its marker come back
            self.play(code.animate.scale(SHRINK).to_corner(UL, buff=0.5),
                      time_span(FadeIn(chain), 0.7, 1.6),
                      time_span(FadeIn(ptr, shift=0.25 * DOWN), 1.0, 1.6), run_time=1.6)

            # {s1}: the first call; 9 is not 3
            c.wait_until("s1")
            sweep_clear(self, time_span(FadeIn(rows[0], shift=0.2 * DOWN), 0.4, 1.1),
                        keep=[code, chain, ptr], run_time=1.1)
            self.play(*recolor(rows[0].find("3"), RED), FlashAround(chain.cells[0].box, color=RED),
                      run_time=0.8)
            c.wait_until("so we search the tail")
            self.play(TransformMatchingStrings(rows[0].copy(), rows[1]), FadeIn(arrs[1]),
                      ptr.animate.move_to(at_cell(1)), run_time=1.6)

            # {s2}: 9 is not 5
            c.wait_until("s2")
            self.play(*recolor(rows[1].find("5"), RED), FlashAround(chain.cells[1].box, color=RED),
                      run_time=0.8)
            c.wait_until("so we move on")
            self.play(TransformMatchingStrings(rows[1].copy(), rows[2]), FadeIn(arrs[2]),
                      ptr.animate.move_to(at_cell(2)), run_time=1.1)

            # {s3}: 9 = 9
            c.wait_until("s3")
            self.play(*recolor(rows[2].find("9", nth=0), GREEN), *recolor(rows[2].find("9", nth=1), GREEN),
                      FlashAround(chain.cells[2].box, color=GREEN), run_time=0.9)
            c.wait_until("the answer is true")
            self.play(ReplacementTransform(rows[2].copy(), rows[3]), FadeIn(arrs[3]),
                      time_span(FadeIn(rep, shift=0.15 * LEFT), 0.6, 1.3), run_time=1.3)

            # {six}: a second, quicker column
            c.wait_until("six")
            self.play(TransformMatchingStrings(rows[0].copy(), srows[0]),
                      ptr.animate.move_to(at_cell(0)), run_time=1.0)
            c.wait_until("runs all the way")
            sweep_t = max(0.9, min(2.0, c.until("to nil")))
            nil_pt = [chain.nil.get_x(), ptr.get_y(), 0]
            self.play(ptr.animate(rate_func=linear).move_to(nil_pt),
                      FadeIn(sarrs[1]), FadeIn(srows[1], shift=0.15 * DOWN), run_time=sweep_t)
            self.play(FlashAround(chain.nil, color=TEAL), FadeIn(sarrs[2]),
                      FadeIn(srows[2], shift=0.15 * DOWN), run_time=0.8)
            c.wait_until("the answer is false")
            self.play(ReplacementTransform(srows[2].copy(), srows[3]), FadeIn(sarrs[3]),
                      time_span(FadeIn(srep, shift=0.15 * LEFT), 0.5, 1.1), run_time=1.1)

    # ── c2.mem.4: flat versus take's pile-up; iterative; the costs ───────────────
    def clip4(self, code):
        srows, sarrs, srep, xr = self.six
        mcol = [*srows, *sarrs[1:]]
        move = RIGHT * (XL - xr) + UP * (Y0C - Y0)
        # the reply drops onto its own row, so take's column fits beside
        rep_move = np.array([XL - srep.get_left()[0], Y0C - len(SIX) * PITCH - srep.get_y(), 0])
        w_mem = col_width(srows)
        probe, _, _ = trace_rows(TAKE, 0, Y0C, size=TTS)
        xt = EDGE - col_width(probe)
        trows, tarrs, _ = trace_rows(TAKE, xt, Y0C, size=TTS)
        take = VGroup(*trows, *[a for a in tarrs if a is not None]).set_color(DIM)
        waits = [trows[1].find("3 ::"), trows[2].find("3 ::"), trows[2].find("5 ::"),
                 trows[3].find("3 ::"), trows[3].find("5 ::")]
        ulines = [underline(VGroup(*w), YELLOW, buff=0.1) for w in waits]

        mid = XL + w_mem / 2
        iterative = T("iterative", 40, GREEN).move_to([mid, Y0C - len(SIX) * PITCH - 0.75, 0])
        costs = VGroup(T("O(n) time", 36, GOLD), T("O(1) space", 36, GOLD)).arrange(RIGHT, buff=0.9)
        costs.move_to([mid, iterative.get_y() - 0.65, 0])

        with self.say("c2.mem.4") as c:
            # {flat}: the chain and the 9 run clear; member's 6 run sits beside take's trace
            sweep_clear(self, *[time_span(m.animate.shift(move), 0.5, 1.7) for m in mcol],
                        time_span(srep.animate.shift(rep_move), 0.5, 1.7),
                        time_span(FadeIn(take, lag_ratio=0.1), 0.9, 1.8),
                        keep=[code, *mcol, srep], run_time=1.8)
            c.wait_until("the way the conses")
            anims = []
            for w in waits:
                anims += recolor(w, YELLOW)
            self.play(*anims, LaggedStart(*[Create(u) for u in ulines], lag_ratio=0.2), run_time=1.3)

            # {last}: the recursive call is the last thing member does
            c.wait_until("last")
            box4 = token_box(code.find("else member x l", line=4), code.line(4))
            self.play(FadeIn(box4), FlashAround(code.find("member x l", line=4), color=YELLOW),
                      run_time=1.2)

            c.wait_until("iter")
            self.play(FadeIn(iterative, shift=0.25 * UP), run_time=1.0)

            c.wait_until("cost")
            self.play(LaggedStart(*[FadeIn(m, shift=0.25 * UP) for m in costs], lag_ratio=0.5),
                      run_time=1.4)

    # ── c2.mem.5: the type again; 'a, and yet x = y ───────────────────────────────
    def clip5(self, code):
        reply = self.make_reply().move_to(DOWN * 2.3)
        with self.say("c2.mem.5") as c:
            c.wait_until("that type")
            sweep_clear(self, time_span(code.animate.scale(1 / SHRINK).move_to(UP * 1.15), 0.4, 1.8),
                        time_span(FadeIn(reply, shift=0.25 * UP), 1.0, 1.8),
                        keep=[code], run_time=1.8)

            # {alpha}: both 'a
            c.wait_until("alpha")
            a1, a2 = reply.find("'a", nth=0), reply.find("'a", nth=1)
            pb = [token_box(a1, reply, color=PINK), token_box(a2, reply, color=PINK)]
            self.play(LaggedStart(*[FadeIn(b) for b in pb], lag_ratio=0.3), run_time=1.0)
            c.wait_until("polymorphic")
            poly = T("polymorphic", 34, PINK)
            poly.move_to([(a1.get_x() + a2.get_x()) / 2, reply.get_bottom()[1] - 0.5, 0])
            self.play(FadeIn(poly, shift=0.2 * UP), run_time=0.9)

            # {yet}: x = y
            c.wait_until("yet")
            xy = code.find("x = y", line=3)
            xbox = token_box(xy, code.line(3), color=YELLOW)
            self.play(FadeIn(xbox), FlashAround(xy, color=YELLOW), run_time=1.2)

            # {how}: the question
            c.wait_until("how")
            q = T("?", 72, YELLOW)
            q_y = (code.line(4).get_bottom()[1] + reply.get_top()[1]) / 2
            q.move_to([(xy.get_x() + (a1.get_x() + a2.get_x()) / 2) / 2, q_y, 0])
            self.play(FadeIn(q, scale=0.5), run_time=1.0)
            c.wait_until()
