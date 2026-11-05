"""Chapter 3, scene 7: unzip without the let, via conspair. Clips c3.cons.1 – c3.cons.3.

Layout: c3.cons.1 asks with s5's let line (boxed, then small and dim on top), then conspair (wrapped
after `=`, size 40) with nested braces above its argument; the body is built from the pattern.
c3.cons.2 moves the definition to the top; the reply (wrapped after `->`, size 30: 76 chars
cannot fit one line at a legal size) gets "in" above / "out" below, then a spotlight with lines
from type parts to pattern parts; then the Cleo example and a DIM two-rung inset of s5's ladder.
c3.cons.3 morphs s5's unzip into the let-free one, checks the type against s5's reply, runs
`unzip book` (reply wrapped after `=`), and brings the let line back in YELLOW.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

OLD = """let rec unzip = function
  | [] -> ([], [])
  | (x, y)::pairs ->
      let xs, ys = unzip pairs in
      (x::xs, y::ys)"""
NEW = """let rec unzip = function
  | [] -> ([], [])
  | xy :: pairs -> conspair (xy, unzip pairs)"""
CONS = """let conspair ((x, y), (xs, ys)) =
  (x::xs, y::ys)"""
CONS_TYPE = """val conspair : ('a * 'b) * ('a list * 'b list) ->
  'a list * 'b list = <fun>"""
EX = 'conspair (("Cleo", 47), ([], []))'
EX_REPLY = '- : string list * int list = (["Cleo"], [47])'
UNZIP_TYPE = "val unzip : ('a * 'b) list -> 'a list * 'b list = <fun>"
BOOK_REPLY = """- : string list * int list =
  (["Amy"; "Bob"; "Cleo"], [21; 35; 47])"""
LET_LINE = "let xs, ys = unzip pairs in"


def purple_b(code):
    """'b is PURPLE in this series (Code colours every type variable PINK)."""
    for k in range(code.src.count("'b")):
        code.find("'b", nth=k).set_color(PURPLE)
    return code


def unzip_reply():
    r = purple_b(Code(UNZIP_TYPE, size=28))
    r.find("unzip").set_color(YELLOW)
    return r


def land(scene, group, *wrappers):
    """Drop the animation wrappers, put `group` back on screen as one object."""
    for w in wrappers:
        scene.remove(w)
    settle(scene, group)


class ConsPair(NarratedScene):
    def construct(self):
        code, braces = self.clip1()
        self.clip2(code, braces)
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c3.cons.1: the helper and its pattern argument ─────────────────────────────
    def clip1(self):
        with self.say("c3.cons.1") as c:
            letq = Code(LET_LINE, size=44).move_to(UP * 0.3)
            letq.find("unzip").set_color(YELLOW)   # the recursive call, as in s2/s3/s5
            box = token_box(letq, letq)
            self.play(FadeIn(letq, shift=0.2 * DOWN), run_time=1.0)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("helper")

            # the question stays up, small and dim, while the helper is built
            code = Code(CONS, size=40).move_to(DOWN * 0.8)
            l0 = code.line(0)
            self.play(FadeOut(box), letq.animate.scale(0.75).move_to(UP * 3.1).set_opacity(0.4),
                      time_span(FadeIn(l0, lag_ratio=0.04), 0.5, 1.7), run_time=1.7)

            arg = code.find("((x, y), (xs, ys))", line=0)
            p1 = code.find("(x, y)", line=0)
            p2 = code.find("(xs, ys)", line=0)
            b1 = Brace(p1, UP, buff=0.12).set_color(DIM)
            b2 = Brace(p2, UP, buff=0.12).set_color(DIM)
            t1 = T("a pair", 30).next_to(b1, UP, buff=0.1)
            t2 = T("a pair of lists", 30).next_to(b2, UP, buff=0.1)
            t1.align_to(t2, DOWN)
            y = max(t1.get_top()[1], t2.get_top()[1]) + 0.14
            bo = Brace(Line([arg.get_left()[0], y, 0], [arg.get_right()[0], y, 0]), UP,
                       buff=0.0).set_color(DIM)
            to = T("one argument: a pair of pairs", 30).next_to(bo, UP, buff=0.1)

            c.wait_until("Its argument is a pattern")
            self.play(FlashAround(arg, time_width=1.5), GrowFromCenter(bo),
                      FadeIn(to, shift=0.3 * DOWN), run_time=1.3)
            c.wait_until("outer")
            self.play(GrowFromCenter(b1), FadeIn(t1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("inner")
            self.play(GrowFromCenter(b2), FadeIn(t2, shift=0.3 * DOWN), run_time=1.0)

            # the body is built from the pattern: x onto xs, y onto ys
            c.wait_until("body")
            x0, xs0 = code.find("x", line=0), code.find("xs", line=0)
            y0, ys0 = code.find("y", line=0), code.find("ys", line=0)
            x1, xs1 = code.find("x", line=1), code.find("xs", line=1)
            y1, ys1 = code.find("y", line=1), code.find("ys", line=1)
            k1, k2 = code.find("::", line=1), code.find("::", line=1, nth=1)
            punct = VGroup(*code.find("(", line=1), *code.find(",", line=1),
                           *code.find(")", line=1))
            self.play(FadeIn(punct), TransformFromCopy(x0, x1), TransformFromCopy(xs0, xs1),
                      time_span(FadeIn(k1, scale=1.4), 0.8, 1.4), run_time=1.4)
            c.wait_until("why onto whys")
            self.play(TransformFromCopy(y0, y1), TransformFromCopy(ys0, ys1),
                      time_span(FadeIn(k2, scale=1.4), 0.7, 1.2), run_time=1.2)
            land(self, code, l0, punct, x1, xs1, k1, y1, ys1, k2)
        return code, [letq, to, bo, t1, b1, t2, b2]

    # ── c3.cons.2: its type, part by part; the Cleo example ────────────────────────
    def clip2(self, code, braces):
        with self.say("c3.cons.2") as c:
            reply = purple_b(Code(CONS_TYPE, size=30))
            reply.find("conspair").set_color(YELLOW)
            reply.move_to(DOWN * 0.6)
            self.play(LaggedStart(*[FadeOut(b) for b in braces], lag_ratio=0.1),
                      code.animate.move_to(UP * 2.3), run_time=1.2)
            self.play(FadeIn(reply, shift=0.2 * DOWN), run_time=1.0)

            inp = reply.find("('a * 'b) * ('a list * 'b list)", line=0)
            outp = reply.find("'a list * 'b list", line=1)
            b_in = Brace(inp, UP, buff=0.1).set_color(DIM)
            t_in = T("in", 32).next_to(b_in, UP, buff=0.08)
            b_out = Brace(outp, DOWN, buff=0.1).set_color(DIM)
            t_out = T("out", 32).next_to(b_out, DOWN, buff=0.08)
            c.wait_until("in")
            self.play(GrowFromCenter(b_in), FadeIn(t_in, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("out")
            self.play(GrowFromCenter(b_out), FadeIn(t_out, shift=0.3 * UP), run_time=1.0)

            # spotlight: each type part lines up with a pattern part
            c.wait_until("lineup")
            p1 = code.find("(x, y)", line=0)
            p2 = code.find("(xs, ys)", line=0)
            q1 = reply.find("('a * 'b)", line=0)
            q2 = reply.find("('a list * 'b list)", line=0)
            lit = {id(g) for grp in (p1, p2, q1, q2) for g in grp}
            rest = [g for g in [*code.text, *reply.text] if id(g) not in lit]
            ln1 = Line(p1.get_bottom() + DOWN * 0.12, q1.get_top() + UP * 0.12,
                       stroke_width=2.5, color=YELLOW)
            ln2 = Line(p2.get_bottom() + DOWN * 0.12, q2.get_top() + UP * 0.12,
                       stroke_width=2.5, color=YELLOW)
            self.play(FadeOut(b_in), FadeOut(t_in), *set_alpha(rest + [b_out, t_out], DIMMED),
                      run_time=1.0)
            self.play(Create(ln1), Create(ln2), run_time=1.3)

            # the example, with a recall of s5's ladder
            c.wait_until("last")
            ex = Code(EX, size=34)
            ex.find("conspair").set_color(YELLOW)
            exr = Code(EX_REPLY, size=30)
            VGroup(ex, exr).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.5)
            inset, up, r0, r1, cp = self.make_inset()
            self.play(LaggedStart(FadeOut(ln1), FadeOut(ln2), FadeOut(reply), FadeOut(b_out),
                                  FadeOut(t_out), lag_ratio=0.1),
                      *set_alpha(list(code.text), 1),
                      time_span(FadeIn(ex, shift=0.2 * DOWN), 0.6, 1.4), run_time=1.4)
            self.play(FadeIn(inset, lag_ratio=0.1), run_time=1.0)
            c.wait_until("you get")
            self.play(FadeIn(exr, shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("That's the first step")
            val = exr.find('(["Cleo"], [47])')
            self.play(restyle(up, op=1, outline=YELLOW, fill=YELLOW), restyle(r0, op=1),
                      restyle(r1, op=1), restyle(cp, op=1),
                      FlashAround(val, color=YELLOW, time_width=1.5), run_time=1.4)

    def make_inset(self):
        """Bottom two rungs of s5's down-and-up ladder, DIM."""
        y0, y1 = -1.55, -2.65
        c0 = Code('unzip [("Cleo", 47)]', size=28).move_to([0, y0, 0]).align_to([-0.4, 0, 0], RIGHT)
        c1 = Code("unzip []", size=28).move_to([0, y1, 0]).align_to([-0.4, 0, 0], RIGHT)
        r0 = Code('(["Cleo"], [47])', size=28).move_to([0, y0, 0]).align_to([0.8, 0, 0], LEFT)
        r0.find('"Cleo"').set_color(YELLOW)
        r1 = Code("([], [])", size=28).move_to([0, y1, 0]).align_to([0.8, 0, 0], LEFT)
        r1.set_color(TEAL)
        kw = dict(buff=0.12, stroke_width=3, tip_length=0.16, color=DIM)
        a0 = Arrow(c0.get_right(), r0.get_left(), **kw)
        a1 = Arrow(c1.get_right(), r1.get_left(), **kw)
        xd, xu = c1.get_x(), r1.get_x()
        down = Arrow([xd, c0.get_bottom()[1], 0], [xd, c1.get_top()[1], 0], **kw)
        up = Arrow([xu, r1.get_top()[1], 0], [xu, r0.get_bottom()[1], 0], **kw)
        cp = Mono("conspair", 28, color=YELLOW).next_to(up, RIGHT, buff=0.2)
        parts = VGroup(c0, c1, a0, a1, down, r1, up, r0, cp)
        parts.set_opacity(0.5)
        frame = SurroundingRectangle(parts, buff=0.3, corner_radius=0.15, color=DIM,
                                     stroke_width=2)
        return VGroup(frame, parts), up, r0, r1, cp

    # ── c3.cons.3: unzip without the let ───────────────────────────────────────────
    def clip3(self):
        with self.say("c3.cons.3") as c:
            new = Code(NEW, size=32)
            new.find("conspair").set_color(YELLOW)
            new.find("unzip", line=2).set_color(YELLOW)   # the recursive call
            new.move_to(ORIGIN).align_to(UP * 3.25, UP)
            old = Code(OLD, size=32).align_to(new, UP).align_to(new, LEFT)
            old.find("unzip", line=3).set_color(YELLOW)
            old.set_opacity(0.4)
            oldr = unzip_reply().next_to(old, DOWN, buff=0.45).set_x(0).set_opacity(0.4)
            sweep_clear(self, time_span(FadeIn(old, shift=0.2 * RIGHT), 0.4, 1.0),
                        time_span(FadeIn(oldr), 0.5, 1.0), run_time=1.0)

            # the three let lines morph into the one new clause
            anims, wraps = [], []
            for a, la, b in (("|", 2, "|"), ("x", 2, "x"), ("y", 2, "y"), ("::", 2, "::"),
                             ("pairs", 2, "pairs"), ("->", 2, "->"),
                             ("unzip pairs", 3, "unzip pairs")):
                src, dst = old.find(a, line=la), new.find(b, line=2)
                anims.append(ReplacementTransform(src, dst))
                wraps += [src, dst]
            gone = [old.find("(", line=2), old.find(",", line=2), old.find(")", line=2),
                    old.find("let xs, ys =", line=3), old.find("in", line=3)]
            anims += [FadeOut(g) for g in gone]
            l4, cpn = old.line(4), new.find("conspair", line=2)
            anims.append(FadeTransform(l4, cpn))
            born = [new.find("(xy,", line=2), new.find(")", line=2)]
            anims += [FadeIn(g) for g in born]
            top_old = VGroup(*old.line(0), *old.line(1))
            top_new = VGroup(*new.line(0), *new.line(1))
            anims += [FadeOut(top_old), FadeIn(top_new)]
            wraps += [*gone, l4, cpn, *born, top_old, top_new]
            self.play(*anims, run_time=1.4)
            self.remove(*old.get_family())
            land(self, new, *wraps)

            # "On nil" lands as the morph ends: hold the finished clause, box on the result
            c.wait_until("two empty lists")
            box = token_box(new.find("[] -> ([], [])", line=1), new.line(1))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("step")
            xy = new.find("xy", line=2)
            xy_box = token_box(xy, new.line(2))
            tag = T("not taken apart", 30, color=YELLOW).next_to(xy_box, DOWN, buff=0.2)
            self.play(Transform(box, xy_box), FadeIn(tag, shift=0.3 * UP), run_time=1.1)
            c.wait_until("call")
            call = new.find("conspair (xy, unzip pairs)", line=2)
            self.play(Transform(box, token_box(call, new.line(2))), run_time=1.3)

            # same type as s5's
            c.wait_until("same")
            newr = unzip_reply().move_to(UP * 0.85)
            self.play(FadeOut(box), FadeOut(tag), time_span(FadeIn(newr, shift=0.2 * DOWN), 0.3, 1.1),
                      run_time=1.1)
            self.play(FlashAround(newr, color=GREEN, time_width=1.5),
                      FlashAround(oldr, color=GREEN, time_width=1.5), restyle(oldr, op=1),
                      run_time=1.5)

            c.wait_until("It's the same computation")
            book = Code("unzip book", size=32)
            bookr = Code(BOOK_REPLY, size=28)
            VGroup(book, bookr).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 1.0)
            self.play(FadeOut(oldr, target_position=newr.get_center()),
                      time_span(FadeIn(book, shift=0.2 * DOWN), 0.4, 1.2),
                      time_span(FadeIn(bookr, shift=0.2 * DOWN), 0.9, 1.8), run_time=1.8)

            # but let with a pattern is worth knowing
            c.wait_until("but")
            letl = Code(LET_LINE, size=34).set_color(YELLOW)
            lbl = T("worth knowing", 32)
            VGroup(letl, lbl).arrange(RIGHT, buff=0.6).move_to(DOWN * 2.75)
            self.play(FadeIn(letl, shift=0.3 * UP),
                      time_span(FadeIn(lbl, shift=0.3 * LEFT), 0.4, 1.0), run_time=1.0)
            c.wait_until("well worth knowing")
            self.play(FlashUnder(letl, color=YELLOW), run_time=1.2)
        self.wait(1.0)   # let the last lines be read before the clear
