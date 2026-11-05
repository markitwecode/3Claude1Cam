"""Chapter 1, scene 2: taking the first i (the general picture, take's code, its type). Clips c1.take.1 – c1.take.4.

Opens on scene 1's hand-off shot (S1_* constants below, as reported by the s1 builder).
Ends on take's code block with OCaml's reply under it, alone (END_* constants; see report).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── scene 1's last shot (keep in sync with ch1_s1_hook) ─────────────────────────
S1_VALUES = [3, 5, 9, 4, 7]
S1_CUT = ([-1.774, 1.05, 0], [-1.774, -1.05, 0])
S1_LABEL_SIZE = 48
S1_TAKE_AT = [-4.074, 1.95, 0]
S1_DROP_AT = [2.3, 1.95, 0]

# ── layout ──────────────────────────────────────────────────────────────────────
CH_SCALE, CH_Y = 0.72, 1.85       # the chain, shrunk to the top on {general} (values stay >= 30)
CH_LBL_DY = 0.95                   # its labels' height above the shrunk chain
LBL_SCALE = 0.75                   # its take/drop labels (48 -> 36)
FORM_SIZE, FORM_Y = 64, -0.6      # the notes' diagram xs = [x_0, ..., x_{n-1}]
DIAG_SCALE, DIAG_TOP = 0.7, 3.45   # the diagram, dimmed at the top while the code is up
DIAG_OP = 0.4
CODE_SIZE = 36
CODE_TOP_2 = 1.1                   # code top while the diagram sits above it (clips 2-3)
CODE_TOP_4 = 2.6                   # code top once the reply is under it (clip 4)
REPLY_SIZE = 32
REPLY_GAP = 0.5
LINE_H = 0.58                      # height of the sliding highlight box

TAKE_SRC = """let rec take i = function
  | [] -> []
  | x::xs ->
      if i > 0 then x :: take (i - 1) xs
      else []"""
REPLY_SRC = "val take : int -> 'a list -> 'a list = <fun>"
DROP_SRC = "val drop : int -> 'a list -> 'a list = <fun>"
ADDLEN_SRC = "let rec addlen n = function"


def scene1_last_shot():
    chain = ConsChain(S1_VALUES)
    cut = DashedLine(*S1_CUT, dash_length=0.12, color=GOLD, stroke_width=5)
    take = Mono("take", size=S1_LABEL_SIZE, color=YELLOW).move_to(S1_TAKE_AT)
    drop = Mono("drop", size=S1_LABEL_SIZE, color=YELLOW).move_to(S1_DROP_AT)
    return chain, cut, take, drop


def call_label(name):
    """`take i xs` / `drop i xs` as two pieces: the name (born from the chain's label) and `i xs`."""
    head = Mono(name, size=40, color=YELLOW)
    rest = Mono("i xs", size=40, t2c={"i": GOLD})
    VGroup(head, rest).arrange(RIGHT, buff=0.33, aligned_edge=DOWN)
    return head, rest


def dim_move(mob, op, scale, about, shift):
    """One Transform that scales (about a common point), moves and dims `mob`."""
    t = mob.copy().scale(scale, about_point=about).shift(shift)
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_fill(opacity=op)
        leaf.set_stroke(opacity=op if leaf.get_stroke_width() > 0 else 0)
    return Transform(mob, t)


def hl(glyphs, line):
    return token_box(glyphs, line, height=LINE_H)


class TakeScene(NarratedScene):
    def construct(self):
        chain, cut, take_lbl, drop_lbl = scene1_last_shot()
        self.play(FadeIn(chain, cut, take_lbl, drop_lbl), run_time=0.8)
        self.chain, self.cut, self.take_lbl, self.drop_lbl = chain, cut, take_lbl, drop_lbl

        self.general_picture()
        self.code_args()
        self.code_clauses()
        self.code_type()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c1.take.1: the general picture ─────────────────────────────────────────
    def general_picture(self):
        chain, cut, take_lbl, drop_lbl = self.chain, self.cut, self.take_lbl, self.drop_lbl
        up = UP * CH_Y

        def lbl_target(m):
            return m.copy().scale(LBL_SCALE).move_to([m.get_x() * CH_SCALE, CH_Y + CH_LBL_DY, 0])

        parts = [r"xs", "=", "[", "x_0", ",", r"\ldots", ",", "x_{i-1}", r",\;\;\;",
                 "x_i", ",", r"\ldots", ",", "x_{n-1}", "]"]
        form = MathTex(*parts, font_size=FORM_SIZE).move_to(UP * FORM_Y)
        lo = min(form[k].get_bottom()[1] for k in range(3, 14))
        cut_x = (form[8].get_right()[0] + form[9].get_left()[0]) / 2
        fcut = DashedLine([cut_x, form.get_top()[1] + 0.35, 0], [cut_x, lo - 0.3, 0],
                          dash_length=0.12, color=GOLD, stroke_width=5)
        b_take = span_brace(np.array([form[3].get_left()[0], lo, 0]),
                            np.array([form[7].get_right()[0], lo, 0]), color=FG)
        b_drop = span_brace(np.array([form[9].get_left()[0], lo, 0]),
                            np.array([form[13].get_right()[0], lo, 0]), color=FG)
        t_head, t_rest = call_label("take")
        VGroup(t_head, t_rest).next_to(b_take, DOWN, buff=0.18)
        d_head, d_rest = call_label("drop")
        VGroup(d_head, d_rest).next_to(b_drop, DOWN, buff=0.18)
        pos = T("position i", size=34, t2c={"[9:10]": GOLD}, t2s={"[9:10]": ITALIC})
        pos.next_to(fcut, UP, buff=0.15)

        with self.say("c1.take.1") as c:
            # "Here's the general picture."  The example shrinks to the top.
            self.play(chain.animate.scale(CH_SCALE, about_point=ORIGIN).shift(up),
                      cut.animate.scale(CH_SCALE, about_point=ORIGIN).shift(up),
                      Transform(take_lbl, lbl_target(take_lbl)),
                      Transform(drop_lbl, lbl_target(drop_lbl)),
                      run_time=min(1.6, 0.8 * c.until("elems")))
            c.wait_until("elems")

            # "A list, exes, holds elements ex zero, ex one, ... up to ex en minus one."
            self.play(time_span(Write(form), 0.0, 3.6),
                      time_span(TransformFromCopy(cut, fcut), 3.2, 4.6),
                      run_time=4.6)
            c.wait_until("front")

            # "Take i of xs returns the front of the list ..."
            self.play(GrowFromCenter(b_take),
                      TransformFromCopy(take_lbl, t_head),
                      time_span(FadeIn(t_rest, shift=0.2 * UP), 0.5, 1.5),
                      run_time=1.5)
            c.wait_until("rest")

            # "Drop i of xs returns the rest, from x_i onwards."
            self.play(GrowFromCenter(b_drop),
                      TransformFromCopy(drop_lbl, d_head),
                      time_span(FadeIn(d_rest, shift=0.2 * UP), 0.4, 1.3),
                      run_time=1.3)
            c.wait_until("cutpos")

            # "Together, they cut the list at position i."
            path = Line(fcut.get_top(), fcut.get_bottom()).set_stroke(GOLD, 9)
            self.play(VShowPassingFlash(path, time_width=0.6),
                      FadeIn(pos, shift=0.25 * DOWN), run_time=1.3)

        self.form, self.fcut, self.pos = form, fcut, pos
        self.diagram = [form, fcut, b_take, b_drop, t_head, t_rest, d_head, d_rest]

    # ── c1.take.2: take's code; its two arguments ──────────────────────────────
    def code_args(self):
        code = Code(TAKE_SRC, size=CODE_SIZE)
        code.move_to(ORIGIN).shift(UP * (CODE_TOP_2 - code.get_top()[1]))
        self.code = code

        geo = VGroup(*self.diagram)
        about = geo.get_center()
        top_after = about[1] + DIAG_SCALE * (geo.get_top()[1] - about[1])
        lift = UP * (DIAG_TOP - top_after)

        i0 = code.find("i", line=0)
        fn = code.find("function", line=0)
        rest0 = code.find("= function", line=0)
        line0 = code.line(0)

        with self.say("c1.take.2") as c:
            # "Let's write take first."  The diagram goes up and dims; the code comes in.
            self.play(time_span(FadeOut(self.chain, self.cut, self.take_lbl, self.drop_lbl), 0.0, 0.8),
                      time_span(FadeOut(self.pos), 0.8, 1.6),
                      *[time_span(dim_move(m, DIAG_OP, DIAG_SCALE, about, lift), 0.2, 1.4)
                        for m in self.diagram],
                      time_span(FadeIn(code, shift=0.3 * UP), 0.6, 1.8),
                      run_time=1.8)
            c.wait_until("function")

            # "It names one argument, i, the count."
            box = hl(i0, line0)
            count = T("the count", size=32, color=YELLOW).next_to(box, UP, buff=0.12)
            self.play(FadeIn(box), FadeIn(count, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("list")

            # "Remember that the word function introduces an argument of its own ..."
            self.play(Transform(box, hl(fn, line0)), run_time=1.0)
            c.wait_until("of its own")

            # "... with no name": a slot opens after i (L3's addlen gesture).
            name = T("unnamed list", size=30, color=TEAL, slant=ITALIC)
            slot_w = name.width + 0.4
            gap = slot_w + 0.4
            self.play(*[g.animate.shift(RIGHT * gap) for g in rest0],
                      box.animate.shift(RIGHT * gap), run_time=1.0)
            eq = code.find("=", line=0)
            slot_c = np.array([(i0.get_right()[0] + eq.get_left()[0]) / 2, line0.get_y(), 0])
            frame = DashedVMobject(RoundedRectangle(width=slot_w, height=0.62, corner_radius=0.1),
                                   num_dashes=22).set_stroke(TEAL, 3).move_to(slot_c)
            name.move_to(frame)
            arc = CurvedArrow(fn.get_top() + UP * 0.1, frame.get_top() + UP * 0.08, angle=TAU / 5,
                              color=BLUE, stroke_width=3, tip_length=0.18)
            self.play(Create(frame), FadeIn(name, scale=0.8), Create(arc), run_time=1.0)
            c.wait_until("just as it did")

            # "... just as it did for addlen, last lecture."
            inset = Code(ADDLEN_SRC, size=30)
            inset.next_to(code, DOWN, buff=0.7).set_x(0)
            inset.set_opacity(0.6)
            self.play(FadeIn(inset, shift=0.25 * UP), run_time=1.0)
            c.wait_until("that argument is the list")

            # "Here, that argument is the list."
            self.play(FlashAround(frame, color=TEAL, time_width=1.5), run_time=1.5)
            c.wait_until("empty")

            # "If the list is empty, there's nothing to take, so take gives nil."
            line1 = code.line(1)
            self.play(FadeOut(frame, name, arc, count),
                      *[g.animate.shift(LEFT * gap) for g in rest0],
                      Transform(box, hl(line1, line1)), run_time=1.3)
            c.wait_until("gives nil")
            self.play(FlashUnder(code.find("[]", line=1, nth=1), color=TEAL),
                      run_time=max(0.5, min(1.0, c.remaining - 0.1)))

        self.box, self.inset = box, inset

    # ── c1.take.3: the cons clause ─────────────────────────────────────────────
    def code_clauses(self):
        code, box = self.code, self.box
        line2, line3, line4 = code.line(2), code.line(3), code.line(4)
        xcons = code.find("x ::", line=3)
        call = code.find("take (i - 1) xs", line=3)
        orig = [g.get_color() for g in xcons]

        with self.say("c1.take.3") as c:
            # "Otherwise, the list has a head, x, and a tail, xs."
            self.play(Transform(box, hl(line2, line2)), FadeOut(self.inset), run_time=1.2)
            c.wait_until("keep")

            # "If i is greater than zero, we still need more elements."
            self.play(Transform(box, hl(line3, line3)), run_time=1.2)
            c.wait_until("so we keep")

            # "So we keep x, and cons it onto take i minus one, of the tail."
            self.play(*recolor(xcons, YELLOW), FlashUnder(xcons, color=YELLOW), run_time=1.2)
            c.wait_until("onto take")
            sub = SurroundingRectangle(call, color=PURPLE, buff=0.1, corner_radius=0.08, stroke_width=3)
            sub_lbl = T("the smaller problem", size=32, color=PURPLE).next_to(sub, DOWN, buff=0.14)
            self.play(Create(sub), FadeIn(sub_lbl, shift=0.25 * UP), run_time=1.3)
            c.wait_until("stop")

            # "Once i reaches zero, we've taken enough, and the answer is nil."
            self.play(Transform(box, hl(line4, line4)),
                      *[g.animate.set_color(col) for g, col in zip(xcons, orig)], run_time=1.2)

        self.sub, self.sub_lbl = sub, sub_lbl

    # ── c1.take.4: OCaml's reply, the type ─────────────────────────────────────
    def code_type(self):
        code, box = self.code, self.box
        lift = UP * (CODE_TOP_4 - code.get_top()[1])
        reply = Code(REPLY_SRC, size=REPLY_SIZE)
        reply.next_to(code.copy().shift(lift), DOWN, buff=REPLY_GAP, aligned_edge=LEFT)

        g_int = reply.find("int")
        g_in = reply.find("'a list", nth=0)
        g_out = reply.find("'a list", nth=1)
        lab_y = reply.get_bottom()[1] - 0.42
        l_int = T("count", size=30).move_to([VGroup(*g_int).get_x(), lab_y, 0])
        l_in = T("list in", size=30).move_to([VGroup(*g_in).get_x(), lab_y, 0])
        l_out = T("list out, same 'a", size=30, t2c={"'a": PINK})
        l_out.move_to([VGroup(*g_out).get_x(), lab_y, 0])
        for lab in (l_int, l_in, l_out):
            lab.align_to(l_in, UP)

        drop = Code(DROP_SRC, size=REPLY_SIZE).set_opacity(0.45)
        drop.next_to(l_in, DOWN, buff=0.5).align_to(reply, LEFT)

        with self.say("c1.take.4") as c:
            # "OCaml's reply gives the type."
            self.play(time_span(FadeOut(*self.diagram, self.sub, self.sub_lbl), 0.0, 0.8),
                      time_span(code.animate.shift(lift), 0.2, 1.4),
                      time_span(box.animate.shift(lift), 0.2, 1.4),
                      time_span(FadeIn(reply, shift=0.25 * DOWN), 1.0, 2.0),
                      run_time=2.0)
            c.wait_until("int")

            # "First comes an integer, the count."
            self.play(Transform(box, hl(g_int, reply)), FadeIn(l_int, shift=0.25 * UP), run_time=1.2)
            c.wait_until("inlist")

            # "Then an alpha list, a list of any type."
            self.play(Transform(box, hl(g_in, reply)), FadeIn(l_in, shift=0.25 * UP), run_time=1.0)
            c.wait_until("out")

            # "And out comes an alpha list, with the same alpha, ..."
            self.play(Transform(box, hl(g_out, reply)), FadeIn(l_out, shift=0.25 * UP), run_time=1.0)
            c.wait_until("with the same alpha")
            self.play(FlashAround(reply.find("'a", nth=0), color=PINK, time_width=1.5),
                      FlashAround(reply.find("'a", nth=1), color=PINK, time_width=1.5),
                      run_time=1.5)
            c.wait_until("droptype")

            # "Drop has exactly the same type."  A dim preview slides out under it.
            self.play(TransformFromCopy(reply, drop), run_time=1.3)

        self.wait(1.5)
        # Hand-off: take's code and its reply alone, centred, for scene 3.
        both = VGroup(code, reply)
        centre = DOWN * both.get_center()[1]
        self.play(FadeOut(box, l_int, l_in, l_out, drop),
                  code.animate.shift(centre), reply.animate.shift(centre), run_time=1.2)
        self.wait(1.0)
