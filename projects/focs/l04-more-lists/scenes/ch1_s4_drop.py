"""Chapter 1, scene 4: drop, take's shape without the waiting cons; its flat trace. Clips c1.drop.1 – c1.drop.3.

Layout (drop.1, drop.2): take's code (Code 32, alpha TAKE_ALPHA) on top, drop's code (Code 32)
under it with the left edges aligned, so the shared clauses sit in the same columns; drop's
reply (Code 30) under that. Side by side does not fit (take's long line is 42 columns).
On {nothing} drop's `drop (i-1) xs` slides right under take's `take (i - 1) xs`, opening a
dashed slot exactly under take's YELLOW `x ::`; it slides back on {keep}.
drop.3: the flat trace in ch1_s3_trace's style (Code rows, DIM ⇒ column, rows left-aligned),
each row born from the one above; the skipped head falls out, the GOLD count morphs 2 → 1 → 0.
On {flat} it shrinks to the right and a DIM copy of s3's take trace fades in on the left at
the same scale, a dashed guide at each first row's right edge.

Hand-off constants from ch1_s3_trace live in one block below (S3_*, TRACE_*), set from s3's
report: take's code fades back in at s3's end spot, then grows into this layout.

STATUS: built; check clean apart from dwell notes on the two skipped-head ghosts (transient by
design) and the DIM take-trace copy (5.3 s of ~6, a shape reference, not text to read).
64.3 s vs 61.1 s narration (1.2 s end hold on the two traces).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── hand-off from ch1_s3_trace (one place) ─────────────────────────────────────
S3_TAKE_SIZE = 36                         # s3's last shot: Code(TAKE_SRC, 36) scaled 28/36,
S3_TAKE_SCALE = 28 / 36                   #   plain highlighting, left x -6.6, top y 3.55,
S3_TAKE_LEFT, S3_TAKE_TOP = -6.6, 3.55    #   opacity 0.35 (about 9.28 x 2.55)
S3_TAKE_ALPHA = 0.35
TRACE_SIZE = 40                           # s3's trace rows (plain names, FG elements, GOLD count)
TRACE_PITCH = 0.84
ANSWER_SIZE = 40                          # OCaml's reply under a trace (28 at FLAT_SCALE)
ANSWER_DROP = 1.0                         # baseline step from the last row to the reply
ARROW_FS = 64                             # ⇒ (MathTex, DIM)
ARROW_GAP = 0.3
ARROW_DY = 0.13
WAIT_COLOR = YELLOW                       # s3's waiting conses
UNSEEN_ALPHA = 0.3                        # s3's never-looked-at elements
TAKE_TRACE_ALPHA = 0.4                    # the {flat} copy of s3's trace

# ── this scene ─────────────────────────────────────────────────────────────────
CODE_SIZE = 32
REPLY_SIZE = 30
CODE_SPACING = 0.85
TAKE_ALPHA = S3_TAKE_ALPHA
FLAT_SCALE = 0.75         # both traces on {flat}, at most (shrunk to fit FLAT_WIDTH)
FLAT_GAP = 0.7
FLAT_WIDTH = 12.8         # the pair's width budget: 0.5 margins plus the dashed guide
BOX_H = 0.66 * CODE_SIZE / TRACE_SIZE     # L3's 0.66 box (Code 40), at this code size

TAKE_SRC = """let rec take i = function
  | [] -> []
  | x::xs ->
      if i > 0 then x :: take (i - 1) xs
      else []"""
DROP_SRC = """let rec drop i = function
  | [] -> []
  | x::xs ->
      if i > 0 then drop (i-1) xs
      else x::xs"""
DROP_REPLY = "val drop : int -> 'a list -> 'a list = <fun>"

DROP_ROWS = ["drop 2 [3; 5; 9; 4; 7]", "drop 1 [5; 9; 4; 7]", "drop 0 [9; 4; 7]", "[9; 4; 7]"]
DROP_ANSWER = "- : int list = [9; 4; 7]"
TAKE_ROWS = ["take 2 [3; 5; 9; 4; 7]", "3 :: take 1 [5; 9; 4; 7]", "3 :: 5 :: take 0 [9; 4; 7]",
             "3 :: 5 :: []", "[3; 5]"]
TAKE_ANSWER = "- : int list = [3; 5]"

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789")


def C(src, size, line_spacing=0.9):
    """A trace row or reply in s3's colours: plain names, list elements FG (count stays GOLD)."""
    code = Code(src, size=size, line_spacing=line_spacing)
    for m in re.finditer(r"\[[^\]]*\]", code.src):
        for d in re.finditer(r"\d+", m.group()):
            code._span(m.start() + d.start(), m.start() + d.end()).set_color(FG)
    return code


def G(code, sub, line=None, nth=0):
    """Glyphs of `sub` as a fresh VGroup (geometry / transform target; never added itself)."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def baseline(code):
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def implies(row, base):
    return (MathTex(r"\Rightarrow", font_size=ARROW_FS, color=DIM)
            .next_to(row, LEFT, buff=ARROW_GAP).set_y(base + ARROW_DY))


def dim_now(mob, op):
    """Instant version of set_alpha: opacity on filled parts, on the stroke of outlines."""
    for leaf in mob.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_fill(opacity=op)
        else:
            leaf.set_stroke(opacity=op)
    return mob


def build_trace(rows_src, answer_src):
    """Rows left-aligned at x=0, row 0's baseline at y=0, DIM ⇒ column, reply below."""
    rows = [C(s, TRACE_SIZE) for s in rows_src]
    arrows = []
    for i, r in enumerate(rows):
        put(r, 0, -i * TRACE_PITCH)
        if i:
            arrows.append(implies(r, -i * TRACE_PITCH))
    ans = put(C(answer_src, ANSWER_SIZE), arrows[0].get_left()[0],      # under the ⇒ column
              -(len(rows) - 1) * TRACE_PITCH - ANSWER_DROP)
    return rows, arrows, ans


class DroppingTheFirst(NarratedScene):
    def construct(self):
        self.build_codes()
        self.drop_code()
        self.nothing_waits()
        self.flat_trace()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── layout ───────────────────────────────────────────────────────────────
    def build_codes(self):
        take = Code(TAKE_SRC, size=CODE_SIZE, line_spacing=CODE_SPACING)
        take.to_edge(UP, buff=0.5).set_x(0)
        drop = Code(DROP_SRC, size=CODE_SIZE, line_spacing=CODE_SPACING)
        drop.next_to(take, DOWN, buff=0.55, aligned_edge=LEFT)
        reply = Code(DROP_REPLY, size=REPLY_SIZE).next_to(drop, DOWN, buff=0.4, aligned_edge=LEFT)
        reply.find("drop").set_color(YELLOW)
        dim_now(take, TAKE_ALPHA)
        # s3's last shot, faded back in at exactly its spot
        take0 = Code(TAKE_SRC, size=S3_TAKE_SIZE).scale(S3_TAKE_SCALE)
        take0.shift(RIGHT * (S3_TAKE_LEFT - take0.get_left()[0]) + UP * (S3_TAKE_TOP - take0.get_top()[1]))
        dim_now(take0, S3_TAKE_ALPHA)
        self.take0, self.take, self.drop, self.reply = take0, take, drop, reply

    # ── c1.drop.1: drop's code, same shape, clause by clause ─────────────────
    def drop_code(self):
        take, drop, reply = self.take, self.drop, self.reply
        with self.say("c1.drop.1") as c:
            self.play(FadeIn(self.take0), run_time=0.5)
            lines = [VGroup(*drop.line(i)) for i in range(5)]
            self.play(time_span(ReplacementTransform(self.take0, take), 0, 1.2),
                      LaggedStart(*[FadeIn(ln, shift=0.25 * UP) for ln in lines], lag_ratio=0.2),
                      run_time=1.4)
            settle(self, drop)

            c.wait_until("same")
            anims = []
            shared = [("| [] -> []", 1), ("| x::xs ->", 2), ("if i > 0 then", 3)]
            for k, (sub, ln) in enumerate(shared):
                t0 = 0.6 * k
                tg, dg = G(take, sub, line=ln), G(drop, sub, line=ln)
                anims += [time_span(restyle(g, op=1), t0, t0 + 0.8) for g in tg]
                anims += [time_span(FlashAround(tg, color=YELLOW, time_width=1.5), t0, t0 + 1.6),
                          time_span(FlashAround(dg, color=YELLOW, time_width=1.5), t0, t0 + 1.6)]
            self.play(*anims, run_time=2.8)

            c.wait_until("empty")
            box = token_box(drop.find("| [] -> []", line=1), drop.line(1), height=BOX_H)
            self.play(FadeIn(box), run_time=0.8)

            c.wait_until("skip")
            self.play(Transform(box, token_box(drop.find("if i > 0 then", line=3), drop.line(3), height=BOX_H)),
                      run_time=1.0)
            c.wait_until("drop eye minus one")
            self.play(Transform(box, token_box(drop.find("drop (i-1) xs", line=3), drop.line(3), height=BOX_H)),
                      run_time=1.0)
            c.wait_until("from the tail")
            self.play(FadeIn(reply, shift=0.2 * UP), run_time=1.0)
        self.box = box

    # ── c1.drop.2: nothing waits, so drop is iterative; the stop clause ──────
    def nothing_waits(self):
        take, drop = self.take, self.drop
        with self.say("c1.drop.2") as c:
            line3 = drop.line(3)
            tail = drop.find("drop (i-1) xs", line=3)
            dx = take.find("take (i - 1) xs", line=3)[0].get_left()[0] - tail[0].get_left()[0]
            slot_l = G(drop, "then", line=3).get_right()[0] + 0.16
            slot_r = tail[0].get_left()[0] + dx - 0.16
            slot = DashedVMobject(Rectangle(width=slot_r - slot_l, height=line3.height + 0.14,
                                            stroke_color=DIM, stroke_width=3), num_dashes=18)
            slot.move_to([(slot_l + slot_r) / 2, line3.get_y(), 0])
            self.play(time_span(FadeOut(self.box), 0, 0.6),
                      *[time_span(g.animate.shift(dx * RIGHT), 0.2, 1.5) for g in tail],
                      time_span(FadeIn(slot), 0.9, 1.6), run_time=1.6)

            c.wait_until("in take")
            xc = G(take, "x ::", line=3)
            waits = T("waits", 32, WAIT_COLOR).next_to(xc, UP, buff=0.14)
            self.play(*[restyle(g, op=1, fill=WAIT_COLOR) for g in xc],
                      FlashAround(xc.copy(), color=WAIT_COLOR, time_width=1.5),
                      time_span(FadeIn(waits, shift=0.3 * DOWN), 0.4, 1.3), run_time=1.5)

            c.wait_until("the result")
            call = G(take, "take (i - 1) xs", line=3)
            self.play(*[restyle(g, op=1) for g in call], FlashUnder(call.copy(), color=YELLOW),
                      run_time=1.5)

            c.wait_until("last")
            gbox = token_box(tail, line3, color=GREEN, height=BOX_H)
            nw = T("nothing waits", 32, GREEN).next_to(slot, UP, buff=0.12)
            self.play(FadeIn(gbox), time_span(FadeIn(nw, shift=0.3 * DOWN), 0.4, 1.3), run_time=1.3)

            c.wait_until("nothing waits for it")
            self.play(FlashAround(slot, color=GREEN, time_width=1.5), run_time=1.3)

            c.wait_until("so drop is iterative")
            it = T("iterative", 36, GREEN).next_to(drop.line(0), RIGHT, buff=0.6)
            self.play(FadeIn(it, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("keep")
            ybox = token_box(drop.find("else x::xs", line=4), drop.line(4), height=BOX_H)
            self.play(*[time_span(FadeOut(m), 0, 0.8) for m in (waits, nw, slot)],
                      *[time_span(g.animate.shift(dx * LEFT), 0.3, 1.3) for g in tail],
                      time_span(ReplacementTransform(gbox, ybox), 0.5, 1.6), run_time=1.6)
            back = T("x put back on its tail", 30, YELLOW, t2s={"x": ITALIC})
            back.next_to(ybox, RIGHT, buff=0.3)
            self.play(FadeIn(back, shift=0.3 * LEFT), run_time=0.9)

            c.wait_until("which is the list")
            self.play(FlashAround(G(drop, "x::xs", line=2), color=TEAL, time_width=1.5),
                      FlashAround(G(drop, "x::xs", line=4), color=TEAL, time_width=1.5),
                      run_time=1.6)

    # ── c1.drop.3: the flat trace, against take's growing one ────────────────
    def birth(self, src, dst, arrow, pairs, skipped=None, run_time=1.5):
        anims = [TransformFromCopy(G(src, a), G(dst, b)) for a, b in pairs]
        if skipped:
            ghost = G(src, skipped).copy()
            anims.append(time_span(FadeOut(ghost, shift=0.45 * DOWN), 0, 0.6 * run_time))
        anims.append(time_span(FadeIn(arrow, shift=0.2 * RIGHT), 0.35 * run_time, run_time))
        self.play(*anims, run_time=run_time)
        settle(self, dst)

    def flat_trace(self):
        rows, arrows, ans = build_trace(DROP_ROWS, DROP_ANSWER)
        dtrace = VGroup(*rows, *arrows, ans)
        dtrace.shift(-dtrace.get_center())                     # hero: centred

        with self.say("c1.drop.3") as c:
            sweep_clear(self, time_span(FadeIn(rows[0], shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)

            c.wait_until("d1")
            self.birth(rows[0], rows[1], arrows[0],
                       [("drop", "drop"), ("2", "1"), ("[", "["), ("5; 9; 4; 7]", "5; 9; 4; 7]")],
                       skipped="3;", run_time=1.8)

            c.wait_until("d2")
            self.birth(rows[1], rows[2], arrows[1],
                       [("drop", "drop"), ("1", "0"), ("[", "["), ("9; 4; 7]", "9; 4; 7]")],
                       skipped="5;", run_time=1.3)

            c.wait_until("d3")
            self.play(FlashAround(G(rows[2], "0"), color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("so the answer is")
            self.birth(rows[2], rows[3], arrows[2], [("[9; 4; 7]", "[9; 4; 7]")], run_time=1.2)
            self.play(TransformFromCopy(G(rows[3], "[9; 4; 7]"), G(ans, "[9; 4; 7]")),
                      FadeIn(G(ans, "- : int list ="), shift=0.2 * UP), run_time=1.2)
            settle(self, ans)

            c.wait_until("flat")
            settle(self, dtrace)
            anchor = np.array([rows[0].get_left()[0], baseline(rows[0]), 0])
            trows, tarrows, tans = build_trace(TAKE_ROWS, TAKE_ANSWER)
            wt0 = VGroup(*trows, *tarrows, tans).width
            scale = min(FLAT_SCALE, (FLAT_WIDTH - FLAT_GAP) / (wt0 + dtrace.width))
            dtrace.generate_target()
            dtrace.target.scale(scale, about_point=anchor)
            for i in (1, 2, 3):
                for sub in ("3 ::", "5 ::"):
                    if sub in TAKE_ROWS[i]:
                        trows[i].find(sub).set_color(WAIT_COLOR)
            trows[4].set_color(GREEN)                          # the built answer
            ttrace = VGroup(*trows, *tarrows, tans).scale(scale, about_point=ORIGIN)
            ttrace.shift(UP * anchor[1])                       # row 0 baselines level
            wt, wd = ttrace.width, dtrace.target.width
            left = -(wt + FLAT_GAP + wd) / 2
            ttrace.shift(RIGHT * (left - ttrace.get_left()[0]))
            dtrace.target.shift(RIGHT * (left + wt + FLAT_GAP - dtrace.target.get_left()[0]))
            top = max(ttrace.get_top()[1], dtrace.target.get_top()[1])
            bot = min(ttrace.get_bottom()[1], dtrace.target.get_bottom()[1])
            ttrace.shift(UP * -(top + bot) / 2)
            dtrace.target.shift(UP * -(top + bot) / 2)
            dim_now(ttrace, TAKE_TRACE_ALPHA)
            trows[2].find("9; 4; 7").set_fill(opacity=TAKE_TRACE_ALPHA * UNSEEN_ALPHA)

            def guide(first, last, op):
                x = first.get_right()[0] + 0.12
                return DashedLine([x, first.get_top()[1] + 0.15, 0], [x, last.get_bottom()[1] - 0.15, 0],
                                  dash_length=0.12, color=DIM, stroke_width=3).set_stroke(opacity=op)
            dt = dtrace.target
            gd = guide(dt[0], dt[len(rows) - 1], 1.0)
            gt = guide(trows[0], trows[-1], 0.6)
            self.play(MoveToTarget(dtrace), time_span(FadeIn(ttrace, shift=0.3 * RIGHT), 0.2, 1.1),
                      time_span(Create(gd), 1.4, 2.2), time_span(Create(gt), 1.4, 2.2), run_time=2.2)

            c.wait_until("each call")
            self.play(*[time_span(FlashAround(r, color=YELLOW, time_width=1.2), 0.4 * k, 0.4 * k + 1.0)
                        for k, r in enumerate(rows)], run_time=2.2)
        self.wait(1.2)                         # let the two shapes sit before the fade
