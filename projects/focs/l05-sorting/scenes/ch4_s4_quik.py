"""Chapter 4, scene 4: without append, the notes' quik. Clips c4.quik.1 – c4.quik.5.

Plan: ch3's `quick` small top-left (ch3_s4 handover placement), its [] line boxed → quick l's
answer (YELLOW chain) copied cell by cell into new BLUE cells, GOLD brace "copies the whole
left answer" → DIM rev_app card-pile inset on the right, label flashes YELLOW → sweep; hero
`quik` (Code 28, top-left), name column at right (quick → quik, captions), meaning column at
right below the long combine line → one box walks the clauses → code shrinks to the top at
{type}, reply + call below → test, result, the notes' quote with "reverses" struck, "sorts".
Shared (s5): `quik_code()` (hero code), `revapp_inset()` (the DIM card-pile inset).
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
from lib.style import *  # noqa: E402,F403

QUIK_SRC = """let rec quik = function
  | ([], sorted) -> sorted
  | ([x], sorted) -> x::sorted
  | a::bs, sorted ->
     let rec part = function
       | l, r, [] -> quik (l, a :: quik (r, sorted))
       | l, r, x::xs ->
           if x <= a then
             part (x::l, r, xs)
           else
             part (l, x::r, xs)
     in
     part ([], [], bs)"""
COMBINE = "| l, r, [] -> quik (l, a :: quik (r, sorted))"

SIZE = 28
LEFT_X = -6.3
TOP_Y = 3.35
BOX_H = 0.46
COL_X = 4.0          # right-hand column (beside the short lines)
SMALL_S = 0.52       # hero code scale once the replies come
RSIZE = 28


def _all(c, sub):
    out, k = [], 0
    while True:
        try:
            out.append(c.find(sub, nth=k))
        except ValueError:
            return out
        k += 1


def paint(c, yellow=("quik", "part", "quick", "rev_app"), gold=("@",)):
    for name in yellow:
        for g in _all(c, name):
            g.set_color(YELLOW)
    for name in gold:
        for g in _all(c, name):
            g.set_color(GOLD)
    return c


def ocode(src, size=SIZE, **kw):
    return paint(Code(src, size=size, **kw))


def quik_code(size=SIZE):
    """The notes' quik: `quik`, `part` YELLOW; keywords BLUE, [] and :: TEAL (highlighter)."""
    return ocode(QUIK_SRC, size, line_spacing=0.72)


def quick_code_small():
    """ch3 s4's `quick`, small, top-left (its handover placement)."""
    try:
        from lib.paths import load_scene
        m = load_scene("ch3_s4_code")
        return m.place_small(m.quick_code())
    except Exception:          # fall back to the same layout built here
        src = """let rec quick = function
  | [] -> []
  | [x] -> [x]
  | a::bs ->
      let rec part l r = function
        | [] -> (quick l) @ (a :: quick r)
        | x::xs ->
            if (x <= a) then
              part (x::l) r xs
            else
              part l (x::r) xs
      in
      part [] [] bs"""
        c = ocode(src, 28).scale(0.55)
        c.shift(np.array([-6.4, 3.45, 0]) - c.get_corner(UL))
        return c


# ── the rev_app card-pile inset (L3 ch4 s7's cards) ─────────────────────────────
CARD_W, CARD_H = 1.4, 0.8


def _card(v, s=0.7):
    box = RoundedRectangle(width=CARD_W, height=CARD_H, corner_radius=0.12, stroke_color=BLUE,
                           stroke_width=3, stroke_opacity=0.55, fill_color=BG, fill_opacity=1)
    return VGroup(box, value_label(v, color=DIM).move_to(box)).scale(s)


def revapp_inset(width=6.1):
    """DIM inset: the two piles of rev_app [1; 2; 3] [4; 5], the call ⇒ its answer, and the
    label "Lecture 3: an accumulator instead of @". Built centred on ORIGIN.
    Parts: .frame .label .piles .call .arrow .res"""
    label = T("Lecture 3:\nan accumulator instead of @", 30, color=DIM, line_spacing=0.9)
    xs = VGroup(*[_card(v) for v in (3, 2, 1)]).arrange(UP, buff=0.09)      # 1 on top
    ys = VGroup(*[_card(v) for v in (5, 4)]).arrange(UP, buff=0.09)        # 4 on top
    ys.align_to(xs, DOWN)
    piles = VGroup(xs, ys).arrange(RIGHT, buff=1.6, aligned_edge=DOWN)
    call = ocode("rev_app [1; 2; 3] [4; 5]", 28)
    res = ocode("[3; 2; 1; 4; 5]", 28)
    arrow = MathTex(r"\Rightarrow", font_size=48, color=DIM)
    out = VGroup(arrow, res).arrange(RIGHT, buff=0.3)
    body = VGroup(label, piles, call, out).arrange(DOWN, buff=0.4)
    frame = RoundedRectangle(width=width, height=body.height + 0.7, corner_radius=0.2,
                             stroke_color=DIM, stroke_width=2).move_to(body)
    g = VGroup(frame, label, piles, call, arrow, res)
    g.frame, g.label, g.piles, g.call, g.arrow, g.res = frame, label, piles, call, arrow, res
    g.shift(-frame.get_center())
    return g


def left_at(m, x, y):
    m.move_to([0, y, 0]).shift(RIGHT * (x - m.get_left()[0]))
    return m


class Quik(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def bx(self, sub, line, nth=0):
        return token_box(self.code.find(sub, line=line, nth=nth), self.code.line(line), height=BOX_H)

    def slide(self, sub, line, rt, nth=0):
        self.play(Transform(self.box, self.bx(sub, line, nth)), run_time=rt)

    # ── c4.quik.1: append copies; rev_app's accumulator ──────────────────────
    def clip1(self):
        q = quick_code_small()
        qbox = token_box(q.find("| [] -> (quick l) @ (a :: quick r)", line=5), q.line(5), height=0.3)

        s = 0.68
        top = ConsChain([1, 2, 3], color=YELLOW).scale(s)
        top.shift(RIGHT * (-6.3 - top.get_left()[0]) + UP * (-0.95 - top.get_y()))
        copies = [ConsCell(v, color=BLUE).scale(s).move_to(top.cells[i]).shift(DOWN * 1.25)
                  for i, v in enumerate((1, 2, 3))]
        acell = ConsCell("a", color=TEAL).scale(s).next_to(copies[2], RIGHT, buff=LINK * s)
        dots = Mono("…", 30, color=DIM).next_to(acell, RIGHT, buff=LINK * s)
        arrows = [link(copies[i], copies[i + 1]) for i in range(2)] + [link(copies[2], acell)]
        a_out = Arrow(acell.tail_start(), dots.get_left() + LEFT * 0.05, buff=0, stroke_width=3,
                      color=FG, max_tip_length_to_length_ratio=0.35)
        brace = span_brace(copies[0].get_corner(DL), copies[2].get_corner(DR), DOWN, color=GOLD)
        blab = T("copies the whole left answer", 30, color=GOLD).next_to(brace, DOWN, buff=0.12)
        blab.align_to(copies[0], LEFT)

        inset = revapp_inset(width=6.0).move_to([3.75, 0.35, 0])

        with self.say("c4.quik.1") as c:
            self.play(FadeIn(q), run_time=1.0)
            c.wait_until("last step")
            self.play(FadeIn(qbox), run_time=0.8)

            c.wait_until("copies")
            self.play(FadeIn(top, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("the whole sorted")
            anims = []
            for i in range(3):
                anims += during(fly(top.cells[i], copies[i]), 0.15 * i, 0.15 * i + 0.45)
            anims += during([GrowArrow(a) for a in arrows] + [FadeIn(acell), FadeIn(dots), GrowArrow(a_out)],
                            0.5, 0.75)
            anims += during([GrowFromCenter(brace), FadeIn(blab, shift=0.2 * DOWN)], 0.7, 1.0)
            self.play(*anims, run_time=min(2.2, c.until("revapp") - 0.2))

            c.wait_until("revapp")
            self.play(FadeIn(inset.frame), *appear(inset.label, inset.piles, lag=0.3), run_time=1.3)
            c.wait_until("an extra argument")
            self.play(*appear(inset.call, VGroup(inset.arrow, inset.res), lag=0.5), run_time=1.4)

            c.wait_until("same")
            self.play(FlashAround(inset.label, color=YELLOW, time_width=1.5),
                      inset.label.animate.set_color(YELLOW), run_time=1.5)

    # ── c4.quik.2: the code, its name, what it means, [] and [x] ─────────────
    def clip2(self):
        code = self.code = quik_code()
        code.shift(np.array([LEFT_X, TOP_Y, 0]) - code.get_corner(UL))

        quick = Mono("quick", 48, color=YELLOW).move_to([COL_X, 2.8, 0])
        quik = Mono("quik", 48, color=YELLOW).move_to(quick)
        cap = T("the notes' name", 30, color=DIM).move_to([COL_X, 2.15, 0])
        said = T("said: quick with accumulator", 28, color=DIM).move_to([COL_X, 1.6, 0])
        self.names = [quick, cap, said]

        m1 = ocode("quik (xs, sorted)")
        m2 = T("means", 32, color=GREEN)
        m3 = ocode("quick xs @ sorted")
        m4 = T("but with no @", 30, color=DIM)
        mean = VGroup(m1, m2, m3, m4).arrange(DOWN, buff=0.26)
        mean.move_to([COL_X, 0, 0]).align_to(np.array([0, -0.55, 0]), UP)
        self.mean = mean

        with self.say("c4.quik.2") as c:
            sweep_clear(self, time_span(FadeIn(code), 0.6, 1.2), run_time=1.4)
            c.wait_until("name")
            self.play(*appear(quick), run_time=1.0)  # early: the voice spells it next
            c.wait_until("which is quick without")
            self.play(*edit(quick, quik), FadeIn(cap, shift=0.2 * DOWN), run_time=1.5)
            self.names[0] = quik
            c.wait_until("quick with accumulator")
            self.play(*appear(said), run_time=1.0)

            c.wait_until("pair")
            self.box = self.bx("([], sorted)", 1)
            self.play(FadeIn(self.box), run_time=0.8)
            c.wait_until("is called sorted")
            self.slide("sorted", 1, 0.9)

            c.wait_until("meaning")
            self.play(*appear(m1, m2, m3, lag=0.4), run_time=1.8)
            c.wait_until("never appends")
            self.play(*appear(m4), run_time=0.9)

            c.wait_until("nil")
            self.slide("| ([], sorted) -> sorted", 1, 1.0)
            c.wait_until("one")
            self.slide("| ([x], sorted) -> x::sorted", 2, 1.0)

    # ── c4.quik.3: a::bs, the local part, its split, its start ───────────────
    def clip3(self):
        code = self.code
        with self.say("c4.quik.3") as c:
            self.slide("| a::bs, sorted ->", 3, 1.0)
            c.wait_until("part")
            self.slide("let rec part = function", 4, 1.0)
            c.wait_until("one triple")
            u1 = underline(code.find("l, r, []", line=5), YELLOW, buff=0.1)
            u2 = underline(code.find("l, r, x::xs", line=6), YELLOW, buff=0.1)
            self.play(GrowFromCenter(u1), GrowFromCenter(u2), run_time=1.0)

            c.wait_until("split")
            self.play(Transform(self.box, self.bx("part (x::l, r, xs)", 8)), *disappear(u1, u2),
                      run_time=1.0)
            c.wait_until("the others onto")
            self.slide("part (l, x::r, xs)", 10, 0.9)
            c.wait_until("start")
            self.slide("part ([], [], bs)", 12, 1.0)

    # ── c4.quik.4: the combine line, no @, the type, the call ────────────────
    def clip4(self):
        code = self.code
        no_at = T("no @", 36, color=GREEN).move_to([5.0, -0.15, 0])
        reply = ocode("val quik : 'a list * 'a list -> 'a list = <fun>", RSIZE)
        reply.move_to([0, -0.55, 0])
        call = left_at(ocode("quik (rs, [])", RSIZE), reply.get_left()[0], -1.35)
        self.reply, self.call = reply, call

        with self.say("c4.quik.4") as c:
            self.slide(COMBINE, 5, 1.0)
            c.wait_until("one call sorts")
            self.slide("quik (r, sorted)", 5, 0.8)
            c.wait_until("the pivot is consed")
            self.slide("a ::", 5, 0.8)
            c.wait_until("a second call")
            self.slide("quik (l, a :: quik (r, sorted))", 5, 0.9)

            c.wait_until("noapp")
            an = code.find("a ::", line=5)
            self.play(*recolor(an, TEAL), FlashAround(an, color=TEAL, time_width=1.5),
                      *appear(no_at, shift=None), run_time=1.2)

            c.wait_until("type")
            olds = [*self.names, self.mean, self.box]
            code.generate_target()
            code.target.scale(SMALL_S).move_to([0, 0, 0]).align_to(np.array([0, 3.6, 0]), UP)
            # the point stays: "no @" shrinks with the code and sits beside the combine line
            no_at.generate_target()
            no_at.target.scale(30 / 36).next_to(code.target.line(5), RIGHT, buff=0.4)
            self.play(*during(disappear(*olds), 0, 0.4),
                      *during([MoveToTarget(code), MoveToTarget(no_at)], 0.45, 1.0),
                      run_time=1.8)
            self.no_at = no_at
            self.play(*appear(reply, shift=None), run_time=1.0)
            c.wait_until("call")
            self.play(*appear(call), run_time=1.0)

    # ── c4.quik.5: a test, and the notes' slip ───────────────────────────────
    def clip5(self):
        test = ocode("quik ([3; 5; 9; 4; 7], [100; 200]);;", RSIZE)
        res = ocode("- : int list = [3; 4; 5; 7; 9; 100; 200]", RSIZE)
        x0 = -res.width / 2
        left_at(test, x0, -0.6)
        left_at(res, x0, -1.4)
        for g in res.find("3; 4; 5; 7; 9"):
            g.set_color(GREEN)
        for g in res.find("100; 200"):
            g.set_color(DIM)

        q1 = T("“Calling quik(xs, sorted) reverses the elements of xs", 30, color=DIM)
        q2 = T("and prepends them to the list sorted.”", 30, color=DIM)
        quote = VGroup(q1, q2).arrange(DOWN, buff=0.18).move_to([0, -2.95, 0])
        rev = select(q1, "reverses")[0]
        strike = Line(rev.get_left() + LEFT * 0.05, rev.get_right() + RIGHT * 0.05,
                      color=RED, stroke_width=4).move_to(rev)
        sorts = T("sorts", 32, color=GREEN).next_to(rev, UP, buff=0.12)

        with self.say("c4.quik.5") as c:
            self.play(*swap(VGroup(self.reply, self.call), test), *disappear(self.no_at),
                      run_time=1.3)
            c.wait_until("we sort three")
            self.play(FlashUnder(test.find("[3; 5; 9; 4; 7]"), color=YELLOW, time_width=1.5),
                      run_time=1.5)
            c.wait_until("result")
            self.play(*appear(res, shift=None), run_time=1.0)

            c.wait_until("slip")
            self.play(*appear(q1, q2, lag=0.4), run_time=1.6)  # early: a quote read whole
            c.wait_until("sorts")
            self.play(Create(strike), run_time=0.8)
            self.play(*appear(sorts), run_time=0.9)
