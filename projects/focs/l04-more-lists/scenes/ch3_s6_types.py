"""Chapter 3, scene 6: zip's and unzip's types are mirror images; unzip undoes zip, not always the
other way round. Clips c3.types.1 – c3.types.3.

Plan
  c3.types.1  `zip;;` / `unzip;;` and OCaml's replies stacked, left-aligned on the colon; braces
              "two lists" -> "a list of pairs" under zip's type, "a list of pairs" -> "a pair of lists"
              under unzip's; {mirror}: braces go, YELLOW boxes on both ('a * 'b) list and a curved
              arrow between them; zip's first -> flashes ("one after the other"), unzip's result *
              flashes ("together").
  c3.types.2  {undo}: the four lines shrink to the top, dimmed; {cut}: the unzip (zip ...) call,
              "Cleo" boxed RED; reply: type line, then the four surviving values fly down from the
              call; {gone}: a RED ghost "Cleo" flies to beside the reply and fades, "gone for good".
  c3.types.3  {other}: types go, the cut example rises and dims; `let xs, ys = unzip book in zip xs ys`
              below; YELLOW box on `unzip book`, slides to `zip xs ys` as the reply arrives; GREEN tick
              "back where you started"; {equal}: equal braces under xs and ys, GOLD 3 and 3. Clear.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


ZIP_REPLY = "- : 'a list -> 'b list -> ('a * 'b) list = <fun>"
UNZIP_REPLY = "- : ('a * 'b) list -> 'a list * 'b list = <fun>"
CUT_SRC = 'unzip (zip ["Amy"; "Bob"; "Cleo"] [21; 35])'
CUT_TYPE = "- : string list * int list ="
CUT_VAL = '(["Amy"; "Bob"], [21; 35])'
BACK_SRC = "let xs, ys = unzip book in zip xs ys"
BACK_TYPE = "- : (string * int) list ="
BACK_VAL = '[("Amy", 21); ("Bob", 35); ("Cleo", 47)]'

TYPE_SIZE = 32       # the two replies (clip 1)
EXPR_SIZE = 34       # the calls
REPLY_SIZE = 32      # their replies
LABEL_SIZE = 32

# clip 1
Y_ZREP, Y_UREP = 1.4, -1.15
# clip 2
Y_CUT, Y_CUT_T, Y_CUT_V = 0.0, -1.0, -1.58
# clip 3
CUT_RISE = 3.25      # the cut call's y once it has risen
Y_BACK, Y_BACK_T, Y_BACK_V = 0.25, -1.3, -1.88


def tint_vars(code):
    """'a PINK, 'b PURPLE."""
    for k in range(code.src.count("'a")):
        code.find("'a", nth=k).set_color(PINK)
    for k in range(code.src.count("'b")):
        code.find("'b", nth=k).set_color(PURPLE)
    return code


def names_yellow(code, *names):
    """Function names YELLOW; each entry is (name, nth)."""
    for name, nth in names:
        code.find(name, nth=nth).set_color(YELLOW)
    return code


def under_brace(glyphs, y, color=DIM):
    """A brace under `glyphs`, its top at a shared y (so braces on one line sit level)."""
    line = Line([glyphs.get_left()[0], y, 0], [glyphs.get_right()[0], y, 0])
    return Brace(line, DOWN, buff=0.1).set_color(color)


def brace_label(glyphs, y, text):
    b = under_brace(glyphs, y)
    lab = T(text, size=LABEL_SIZE).next_to(b, DOWN, buff=0.12)
    return b, lab


def leaves(mob):
    return mob.family_members_with_points()


class MirrorTypes(NarratedScene):
    def construct(self):
        self.types_clip()
        self.cut_clip()
        self.back_clip()
        self.wait(0.8)                                                   # let the last result land
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c3.types.1: the two types side by side ────────────────────────────────
    def types_clip(self):
        zrep = tint_vars(Code(ZIP_REPLY, size=TYPE_SIZE))
        urep = tint_vars(Code(UNZIP_REPLY, size=TYPE_SIZE))
        x0 = -max(zrep.width, urep.width) / 2
        zrep.move_to([x0, Y_ZREP, 0], aligned_edge=LEFT)
        urep.move_to([x0, Y_UREP, 0], aligned_edge=LEFT)
        zin = names_yellow(Code("zip;;", size=TYPE_SIZE), ("zip", 0))
        uin = names_yellow(Code("unzip;;", size=TYPE_SIZE), ("unzip", 0))
        zin.next_to(zrep, UP, buff=0.22, aligned_edge=LEFT)
        uin.next_to(urep, UP, buff=0.22, aligned_edge=LEFT)
        self.types = [zin, zrep, uin, urep]

        zy, uy = zrep.get_bottom()[1], urep.get_bottom()[1]
        zb1, zl1 = brace_label(zrep.find("'a list -> 'b list"), zy, "two lists")
        zb2, zl2 = brace_label(zrep.find("('a * 'b) list"), zy, "a list of pairs")
        ub1, ul1 = brace_label(urep.find("('a * 'b) list"), uy, "a list of pairs")
        ub2, ul2 = brace_label(urep.find("'a list * 'b list"), uy, "a pair of lists")

        with self.say("c3.types.1") as c:
            self.play(LaggedStart(*[FadeIn(m, shift=0.3 * DOWN) for m in self.types], lag_ratio=0.3),
                      run_time=min(2.2, 0.85 * c.until("zip")))
            c.wait_until("zip")
            self.play(GrowFromCenter(zb1), FadeIn(zl1, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("gives a list of pairs")
            self.play(GrowFromCenter(zb2), FadeIn(zl2, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("unzip")
            self.play(GrowFromCenter(ub1), FadeIn(ul1, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("gives a pair of lists")
            self.play(GrowFromCenter(ub2), FadeIn(ul2, shift=0.25 * DOWN), run_time=1.0)

            # {mirror}: the shared ('a * 'b) list, one on each side; the braces stay
            c.wait_until("mirror")
            up = urep.find("('a * 'b) list")
            arrow = CurvedArrow(zl2.get_bottom() + 0.2 * DOWN, up.get_top() + 0.14 * UP,
                                angle=PI / 8, color=YELLOW, stroke_width=5)
            self.marks = [zb1, zl1, zb2, zl2, ub1, ul1, ub2, ul2, arrow]
            self.play(*[m.animate.set_color(YELLOW) for m in (zb2, zl2, ub1, ul1)],
                      time_span(Create(arrow), 0.5, 1.8), run_time=1.8)

            c.wait_until("one after the other")
            arr = zrep.find("->", nth=0)
            self.play(FlashAround(arr, color=YELLOW, time_width=1.5), *recolor(arr, YELLOW), run_time=1.5)
            c.wait_until("together")
            star = urep.find("*", nth=1)
            self.play(FlashAround(star, color=YELLOW, time_width=1.5), *recolor(star, YELLOW), run_time=1.5)

    # ── c3.types.2: unzip undoes zip, with one catch ──────────────────────────
    def cut_clip(self):
        expr = names_yellow(Code(CUT_SRC, size=EXPR_SIZE), ("unzip", 0), ("zip", 1))
        expr.move_to([0, Y_CUT, 0])
        xl = expr.get_left()[0]
        rtype = Code(CUT_TYPE, size=REPLY_SIZE).move_to([xl, Y_CUT_T, 0], aligned_edge=LEFT)
        rval = Code(CUT_VAL, size=REPLY_SIZE).move_to([xl, Y_CUT_V, 0], aligned_edge=LEFT)
        cleo = expr.find('"Cleo"')
        cbox = SurroundingRectangle(cleo, color=RED, buff=0.1, corner_radius=0.06, stroke_width=4)
        ghost = Code('"Cleo"', size=REPLY_SIZE).find('"Cleo"').set_color(RED)   # bare glyphs, like cleo
        ghost.next_to(rval, RIGHT, buff=0.5).align_to(rval.find('"Bob"'), DOWN)
        glabel = T("gone for good", size=LABEL_SIZE, color=RED).next_to(ghost, RIGHT, buff=0.4)
        self.cut = dict(expr=expr, cbox=cbox, rtype=rtype, rval=rval, ghost=ghost, glabel=glabel)

        with self.say("c3.types.2") as c:
            # {undo}: the types move up out of the way, small and dim
            tgt = [m.copy() for m in self.types]
            col = VGroup(*tgt).scale(0.875).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            col.move_to(ORIGIN).to_edge(UP, buff=0.45)
            for t in tgt:
                t.set_opacity(0.5)
            self.play(*[FadeOut(m) for m in self.marks],
                      *[Transform(m, t) for m, t in zip(self.types, tgt)], run_time=1.5)

            c.wait_until("cut")
            self.play(FadeIn(expr, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("Cleo is dropped")
            self.play(Create(cbox), run_time=0.9)

            c.wait_until("Unzip that")
            self.play(FadeIn(rtype, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("you get Amy")
            moved = [(expr.find('"Amy"; "Bob"'), rval.find('"Amy"; "Bob"')),
                     (expr.find("21; 35"), rval.find("21; 35"))]
            taken = {id(m) for _, dst in moved for m in leaves(dst)}
            skel = VGroup(*[m for m in leaves(rval) if id(m) not in taken])
            self.play(*[TransformFromCopy(src, dst) for src, dst in moved], FadeIn(skel), run_time=1.8)
            self.remove(*[dst for _, dst in moved], skel)
            self.add(rval)

            c.wait_until("gone")
            self.play(TransformFromCopy(cleo, ghost), run_time=1.2)
            self.play(ghost.animate.set_opacity(0.3), FadeIn(glabel, shift=0.25 * LEFT), run_time=1.0)

    # ── c3.types.3: the other way round always works ──────────────────────────
    def back_clip(self):
        k = self.cut
        dy = CUT_RISE - k["expr"].get_y()
        expr3 = names_yellow(Code(BACK_SRC, size=EXPR_SIZE), ("unzip", 0), ("zip", 1))
        rtype3 = Code(BACK_TYPE, size=REPLY_SIZE)
        rval3 = Code(BACK_VAL, size=REPLY_SIZE)
        xl = -max(expr3.width, rval3.width) / 2
        expr3.move_to([xl, Y_BACK, 0], aligned_edge=LEFT)
        rtype3.move_to([xl, Y_BACK_T, 0], aligned_edge=LEFT)
        rval3.move_to([xl, Y_BACK_V, 0], aligned_edge=LEFT)
        tick = check_mark(color=GREEN)
        blabel = T("back where you started", size=LABEL_SIZE, color=GREEN)
        VGroup(tick, blabel).arrange(RIGHT, buff=0.25).next_to(rval3, DOWN, buff=0.4)
        xs, ys = expr3.find("xs", nth=1), expr3.find("ys", nth=1)
        by = expr3.get_bottom()[1]
        bx, byy = under_brace(xs, by, color=GOLD), under_brace(ys, by, color=GOLD)
        n1 = T("3", size=44, color=GOLD).next_to(bx, DOWN, buff=0.12)
        n2 = T("3", size=44, color=GOLD).next_to(byy, DOWN, buff=0.12)

        with self.say("c3.types.3") as c:
            # {other}: types go, the cut example rises and dims, the new call arrives below
            self.play(*[time_span(FadeOut(m), 0, 0.8) for m in self.types],
                      k["expr"].animate.shift(dy * UP).set_opacity(0.45),
                      k["cbox"].animate.shift(dy * UP).set_stroke(opacity=0.45),
                      k["rtype"].animate.shift(dy * UP).set_opacity(0.45),
                      k["rval"].animate.shift(dy * UP).set_opacity(0.45),
                      k["ghost"].animate.shift(dy * UP).set_opacity(0.2),
                      k["glabel"].animate.shift(dy * UP).set_opacity(0.45),
                      time_span(FadeIn(expr3, shift=0.3 * DOWN), 0.7, 1.6), run_time=1.6)

            c.wait_until("Unzip a list of pairs")
            box = token_box(expr3.find("unzip book"), expr3, color=YELLOW)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("zip the two halves")
            self.play(Transform(box, token_box(expr3.find("zip xs ys"), expr3, color=YELLOW)),
                      time_span(FadeIn(rtype3, shift=0.25 * DOWN), 0.0, 1.0),
                      time_span(FadeIn(rval3, shift=0.25 * DOWN), 0.2, 1.2), run_time=1.3)
            c.wait_until("back where you started")
            self.play(FadeIn(tick, scale=0.6), FadeIn(blabel, shift=0.25 * LEFT), run_time=0.9)

            c.wait_until("equal")
            self.play(FadeOut(box), GrowFromCenter(bx), GrowFromCenter(byy),
                      time_span(FadeIn(n1, shift=0.25 * UP), 0.3, 1.0),
                      time_span(FadeIn(n2, shift=0.25 * UP), 0.3, 1.0), run_time=1.0)
