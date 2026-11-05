"""Chapter 4, scene 8: reduction in strength (the two causes, heavy @ -> light ::, the
multiply-by-adding history, the iter_append caveat), the chapter recap and the end card.

Clips c4.str.1 - c4.str.3, c4.recap.1 (the chapter's last scene).

STATUS: built. OCaml verified (`val iter_append : 'a list -> 'a list -> 'a list = <fun>`,
  `iter_append [1; 2; 3] [4]` -> `- : int list = [1; 2; 3; 4]`).

PLAN (as built)
- str.1 {what}: rev_app Code 34 at the top; {acc}: box `ys`, left cause "accumulator -> iterative";
  {but}: dim it; {gone}: right cause "no more append -> O(n) time", YELLOW box; {swap}: left cause
  out, code dims, heavy RED box with a GOLD `@` drops in under it ("O(n) each"); "append": code
  out, the boxed cause folds into one line at the top, "append"; "a series": arrow -> 3 light TEAL
  `::` boxes ("O(1) each"), "cons" (v1 s7_rev); {name}: the boxed cause becomes the YELLOW title
  "Reduction in strength" while heavy/light lift 0.6 to centre.
- str.2 {history}: DIM "no hardware multiply"; {products} `0 x 7` .. `3 x 7` one per spoken
  product; {adds}: RED crosses on the x; "Zero, seven, fourteen, twenty-one": GOLD answers, each
  born from the one before along a GOLD "+7" arc; {same}: flash answers, then the +7s; {again}:
  FlashUnder the title.
- str.3 {backwards}: `rev_app [1; 2; 3] []` => `[3; 2; 1]` (digits cross over), DIM "backwards";
  {iterapp}: `let iter_append xs ys =` + "?", the call; "it's short": "?" -> body, val reply;
  the demo steps down 1.25 and stays until "Reverse": box `rev xs`, row A (3 YELLOW cells from the call's digits); "then": box -> rev_app,
  row B (3 YELLOW from row A + the shared TEAL 4) + the call's reply; {double}: GOLD
  "iter_append 6 conses" vs DIM "append 3 conses"; {rule}: RED box on row A, "an extra reversal".
- recap.1: ch3_s7 recap style (title "Recap" 48, BLUE dots, T 34 / Code 32, earlier rows to 0.5);
  {next}: rows back to 1, "Next: strings and characters", `'a'` `"abc"`, "then exercises";
  end card 8 s, fade 1.3 s.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

REV_APP = "let rec rev_app xs ys =\n  match xs, ys with\n  | [], ys    -> ys\n  | x::xs, ys -> rev_app xs (x::ys)"
ITER_DEF = "let iter_append xs ys = rev_app (rev xs) ys"
ITER_VAL = "val iter_append : 'a list -> 'a list -> 'a list = <fun>"
CALL = "iter_append [1; 2; 3] [4]"
CALL_REPLY = "- : int list = [1; 2; 3; 4]"

# ── layout ──────────────────────────────────────────────────────────────────────
TOP_Y = 3.0                       # title / folded cause
CAUSE_X, CAUSE_Y = 3.4, -1.75     # the two causes, side by side under the code
HEAVY_X, LIGHT_X, HL_Y = -3.6, 3.4, -0.5    # under the code; lifted by HL_LIFT at {name}
HL_LIFT = 0.6
PX = (-4.5, -1.5, 1.5, 4.5)       # products / answers columns
PROD_Y, ANS_Y, PLUS_Y = 0.7, -0.75, -2.25
X0 = -6.4                         # left edge of the iter_append session
DEF_Y, VAL_Y, CALL_Y = 3.0, 2.4, 1.55
ROW_A_Y, ROW_B_Y, ROW_X, CH_S = 0.3, -1.25, -0.6, 0.85
COUNT_Y = -2.8


def named(src, size, *names):
    """ch3 style: every use of a function name in YELLOW; `@` in GOLD (this chapter)."""
    code = Code(src, size=size)
    for nm in names:
        for m in re.finditer(rf"(?<![\w']){re.escape(nm)}(?![\w'])", code.src):
            code._span(m.start(), m.end()).set_color(YELLOW)
    for m in re.finditer("@", code.src):
        code._span(m.start(), m.end()).set_color(GOLD)
    return code


def cost(big, word, color=GOLD, size=34):
    o = MathTex(big, font_size=size + 8, color=color)
    w = T(word, size=size, color=color)
    grp = VGroup(o, w).arrange(RIGHT, buff=0.2)
    w.align_to(o, DOWN).shift(UP * 0.06)
    return grp


def down_arrow(color=DIM):
    return Arrow(UP * 0.32, DOWN * 0.32, buff=0, stroke_width=4, color=color,
                 max_tip_length_to_length_ratio=0.35)


def cause(top, result, size=38):
    return VGroup(T(top, size), down_arrow(), result).arrange(DOWN, buff=0.2)


def heavy_box():
    box = RoundedRectangle(width=2.1, height=2.1, corner_radius=0.2, stroke_color=RED,
                           stroke_width=8, fill_color=RED, fill_opacity=0.15)
    return VGroup(box, Mono("@", 120, color=GOLD).move_to(box))


def light_box():
    box = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.12, stroke_color=TEAL,
                           stroke_width=2.5)
    return VGroup(box, Mono("::", 52, color=TEAL).move_to(box))


def build_chain(chain, label_sources, path_arc=0.0):
    """Cells fade in while their values fly in from the code (one animation per piece)."""
    anims = []
    for cell, src in zip(chain.cells, label_sources):
        anims += [FadeIn(cell.box), FadeIn(cell.ptr), FadeIn(cell.dot),
                  TransformFromCopy(src, cell.label, path_arc=path_arc)]
    anims += [GrowArrow(a) for a in chain.arrows]
    if chain.nil is not None:
        anims.append(FadeIn(chain.nil))
    return anims


def first_cue(c, *cues):
    """The first of several spellings that the clip's word list knows."""
    for q in cues:
        try:
            c.at(q)
            return q
        except KeyError:
            pass
    raise KeyError(cues)


class ReductionInStrength(NarratedScene):
    def construct(self):
        self.causes()
        self.history()
        self.caveat()
        self.recap()
        # End card: the finished recap and the teaser hold under the music.
        self.wait(8.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.3)
        self.wait(0.15)

    # ── str.1: two causes; the real one is that append is gone ──────────────────
    def causes(self):
        code = named(REV_APP, 34, "rev_app").move_to([0, 2.05, 0])
        ys_box = token_box(code.find("ys", line=0), code.line(0))
        left = cause("accumulator", T("iterative", 38, color=GREEN)).move_to([-CAUSE_X, CAUSE_Y, 0])
        right = cause("no more append", cost(r"O(n)", "time", size=38)).move_to([CAUSE_X, CAUSE_Y, 0])
        rbox = SurroundingRectangle(right, color=YELLOW, buff=0.25)
        rc = VGroup(right)

        flat = VGroup(T("no more append", 34),
                      Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, stroke_width=4, color=DIM,
                            max_tip_length_to_length_ratio=0.35),
                      cost(r"O(n)", "time", size=34)).arrange(RIGHT, buff=0.25)
        rc_top = VGroup(flat, SurroundingRectangle(flat, color=YELLOW, buff=0.2)).move_to([0, TOP_Y, 0])
        title = T("Reduction in strength", 52, color=YELLOW).move_to([0, TOP_Y, 0])

        heavy = heavy_box().move_to([HEAVY_X, HL_Y, 0])
        h_name = T("append", 38)
        h_cost = MathTex(r"O(n)\text{ each}", font_size=42, color=GOLD)
        VGroup(h_name, h_cost).arrange(DOWN, buff=0.25).next_to(heavy, DOWN, buff=0.4)
        lights = VGroup(*[light_box() for _ in range(3)]).arrange(RIGHT, buff=0.3)
        lights.move_to([LIGHT_X, HL_Y, 0])
        l_name = T("cons", 38).move_to([LIGHT_X, h_name.get_y(), 0])
        l_cost = MathTex(r"O(1)\text{ each}", font_size=42, color=GOLD).move_to([LIGHT_X, h_cost.get_y(), 0])
        swap = Arrow(heavy.get_right() + RIGHT * 0.3, lights.get_left() + LEFT * 0.3, buff=0,
                     color=FG, stroke_width=5)

        with self.say("c4.str.1") as c:
            # "So what made rev-app fast?"
            self.play(FadeIn(code, shift=0.2 * DOWN), run_time=min(0.9, 0.7 * c.until("acc")))
            # "Its accumulator, whys, makes it iterative."
            c.wait_until("acc")
            self.play(FadeIn(ys_box), run_time=0.8)
            c.wait_until("makes it iterative")
            self.play(FadeIn(left, shift=0.3 * DOWN), run_time=1.0)
            # "But that's not where the speed comes from."
            c.wait_until("but")
            self.play(left.animate.set_opacity(0.4), FadeOut(ys_box), run_time=1.0)
            # "The real gain is that append is gone."
            c.wait_until("gone")
            self.play(FadeIn(right, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("is gone")
            self.play(Create(rbox), run_time=0.8)
            settle(self, rc, add=[rbox])
            # "We replaced an expensive operation, append, with a series of cheap ones, single conses."
            # the heavy @ drops in under the (dimmed) code; the dim cause makes way
            c.wait_until("swap")
            self.play(time_span(FadeOut(left), 0, 0.5), code.animate.set_opacity(0.4),
                      time_span(FadeIn(heavy, shift=0.6 * DOWN, rate_func=rush_into), 0.3, 1.0),
                      time_span(FadeIn(h_cost, shift=0.2 * UP), 0.6, 1.2), run_time=1.2)
            c.wait_until("append", nth=1)
            self.play(FadeOut(code), ReplacementTransform(rc, rc_top), FadeIn(h_name, shift=0.2 * UP),
                      run_time=min(1.1, c.until("with a series")))
            c.wait_until("with a series")
            self.play(GrowArrow(swap),
                      LaggedStart(*[FadeIn(lt, shift=0.4 * UP) for lt in lights], lag_ratio=0.3),
                      time_span(FadeIn(l_cost, shift=0.2 * UP), 0.5, 1.3),
                      run_time=min(1.3, c.until("single conses")))
            c.wait_until("single conses")
            self.play(FadeIn(l_name, shift=0.2 * UP), run_time=0.8)
            hl = VGroup()
            settle(self, hl, add=[heavy, h_name, h_cost, swap, *lights, l_name, l_cost])
            # "This is called reduction in strength, and it's a common technique in computer science."
            c.wait_until("name")
            self.play(FadeTransform(rc_top, title), hl.animate.shift(UP * HL_LIFT), run_time=1.5)
        self.title = title

    # ── str.2: no hardware multiply; adding sevens instead ───────────────────────
    def history(self):
        title = self.title
        nohw = T("no hardware multiply", 36, color=DIM).move_to([0, 2.1, 0])
        prods = [MathTex(str(k), r"\times", "7", font_size=66).move_to([x, PROD_Y, 0])
                 for k, x in enumerate(PX)]
        ans = [MathTex(str(7 * k), font_size=66, color=GOLD).move_to([x, ANS_Y, 0])
               for k, x in enumerate(PX)]
        arcs, plus = [], []
        for a, b in zip(ans, ans[1:]):
            y = ANS_Y - 0.5
            arcs.append(CurvedArrow(np.array([a.get_x() + 0.3, y, 0]), np.array([b.get_x() - 0.3, y, 0]),
                                    angle=PI / 2, color=GOLD, stroke_width=4, tip_length=0.18))
            plus.append(MathTex("+7", font_size=46, color=GOLD).move_to([(a.get_x() + b.get_x()) / 2, PLUS_Y, 0]))
        crosses = [Cross(p[1], stroke_color=RED, stroke_width=6, scale_factor=1.7) for p in prods]

        with self.say("c4.str.2") as c:
            # "The idea dates from when many computers had no hardware multiply instruction."
            sweep_clear(self, time_span(FadeIn(nohw, shift=0.3 * DOWN), 0.6, 1.4), keep=[title], run_time=1.4)
            # "Suppose you needed zero times seven, then one times seven, then two times seven, and so on."
            for i, cue in enumerate(("zero times seven", "one times seven", "two times seven", "and so on")):
                c.wait_until(cue)
                self.play(FadeIn(prods[i], shift=0.3 * DOWN), run_time=0.9 if i == 0 else 0.6)
            # "Instead of multiplying, you could just keep adding seven."
            c.wait_until("adds")
            self.play(LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.25),
                      *[p.animate.set_opacity(0.5) for p in prods], run_time=1.4)
            # "Zero, seven, fourteen, twenty-one."
            c.wait_until("zero", nth=1)
            self.play(FadeIn(ans[0], shift=0.3 * DOWN), run_time=0.6)
            steps = (("seven", 4), ("fourteen", 0), (first_cue(c, "twenty-one", "twenty"), 0))
            for i, (cue, nth) in enumerate(steps):
                c.wait_until(cue, nth=nth)
                nxt = c.until(steps[i + 1][0], nth=steps[i + 1][1]) if i < 2 else 1.0
                self.play(Create(arcs[i]), FadeIn(plus[i], shift=0.2 * UP),
                          TransformFromCopy(ans[i], ans[i + 1], path_arc=PI / 2),
                          run_time=min(0.9, 0.9 * nxt))
            # "The same answers, from cheap additions."
            c.wait_until("same")
            self.play(FlashAround(VGroup(*ans), color=GOLD, time_width=1.5, buff=0.25), run_time=1.5)
            c.wait_until("cheap additions")
            self.play(LaggedStart(*flash(plus, YELLOW, time_width=1.5), lag_ratio=0.2), run_time=1.3)
            # "You'll see this trick many times in this course, very often to get rid of an append."
            c.wait_until("again")
            self.play(FlashUnder(title, color=YELLOW), run_time=1.5)

    # ── str.3: the caveat: an accumulator builds backwards; iter_append ─────────
    def caveat(self):
        inp = named("rev_app [1; 2; 3] []", 44, "rev_app").move_to([0, 1.0, 0])
        res = Code("[3; 2; 1]", 44)
        lst = VGroup(*inp.find("[1; 2; 3]"))
        res.move_to([lst.get_x(), -0.35, 0])
        imp = MathTex(r"\Rightarrow", font_size=60, color=DIM).next_to(res, LEFT, buff=0.4)
        bk = T("backwards", 34, color=DIM).next_to(res, DOWN, buff=0.45)
        digit = {d: res.find(d)[0] for d in "123"}
        others = [g for g in res.text if all(g is not v for v in digit.values())]

        idef = named(ITER_DEF, 32, "rev_app", "rev").move_to([X0, DEF_Y, 0], aligned_edge=LEFT)
        hdr = VGroup(*[g.copy() for g in idef.find("let iter_append xs ys =")])
        body = VGroup(*[g.copy() for g in idef.find("rev_app (rev xs) ys")])
        q = T("?", 56, color=YELLOW).next_to(hdr, RIGHT, buff=0.35)
        ival = Code(ITER_VAL, 28).move_to([X0, VAL_Y, 0], aligned_edge=LEFT)
        call = named(CALL, 28, "iter_append").move_to([X0, CALL_Y, 0], aligned_edge=LEFT)
        creply = Code(CALL_REPLY, 28).next_to(call, RIGHT, buff=0.7)
        tbox = token_box(idef.find("rev xs"), idef)

        row_b = ConsChain([1, 2, 3, 4], color=YELLOW).scale(CH_S).move_to([ROW_X, ROW_B_Y, 0])
        for part in (row_b.cells[3].box, row_b.cells[3].ptr):
            part.set_stroke(TEAL)
        row_a = ConsChain([3, 2, 1], color=YELLOW).scale(CH_S)
        row_a.move_to([row_b.get_left()[0], ROW_A_Y, 0], aligned_edge=LEFT)
        lc = VGroup(Code("iter_append", 30).set_color(YELLOW), T("6 conses", 38, color=GOLD))
        lc.arrange(RIGHT, buff=0.3).move_to([-3.2, COUNT_Y, 0])
        rcnt = VGroup(Code("append", 30).set_color(DIM), T("3 conses", 38, color=DIM))
        rcnt.arrange(RIGHT, buff=0.3).move_to([3.2, COUNT_Y, 0])
        extra = SurroundingRectangle(row_a, color=RED, buff=0.15)
        rext = T("an extra reversal", 36, color=RED).next_to(extra, RIGHT, buff=0.4)

        with self.say("c4.str.3") as c:
            # "One warning, though."
            sweep_clear(self, run_time=min(1.2, c.until("backwards")))
            # "Consing onto an accumulator builds the result backwards, just as rev-app did."
            c.wait_until("backwards")
            self.play(FadeIn(inp, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("the result backwards")
            arcs = {"1": PI / 2, "2": 0, "3": PI / 2}
            self.play(FadeIn(imp), *[FadeIn(g) for g in others],
                      *[TransformFromCopy(inp.find(d)[0], digit[d], path_arc=arcs[d]) for d in "123"],
                      run_time=1.6)
            c.wait_until("just as")
            self.play(FadeIn(bk, shift=0.2 * DOWN), run_time=0.8)
            demo = VGroup()
            settle(self, demo, add=[inp, imp, *others, *digit.values(), bk])
            # "Remember the iterative append we decided not to write?"  (the demo steps down)
            c.wait_until("iterapp")
            self.play(demo.animate.shift(DOWN * 1.25), time_span(FadeIn(hdr, shift=0.2 * DOWN), 0.4, 1.2),
                      time_span(FadeIn(q, scale=1.4), 0.8, 1.5), run_time=1.5)
            c.wait_until("decided not")
            self.play(FadeIn(call, shift=0.2 * DOWN), run_time=0.9)
            # "With rev-app, it's short."
            c.wait_until("short")
            self.play(ReplacementTransform(q, body), time_span(FadeIn(ival, shift=0.2 * DOWN), 0.8, 1.6),
                      run_time=1.6)
            self.remove(hdr, body)
            self.add(idef)
            # "Reverse the first list, then rev-app it onto the second."
            c.wait_until("reverse the first")
            self.play(time_span(FadeOut(demo), 0, 0.6), time_span(FadeIn(tbox), 0, 0.5),
                      *build_chain(row_a, [call.find(str(v))[0] for v in (3, 2, 1)], path_arc=PI / 3),
                      run_time=1.5)
            settle(self, row_a)
            c.wait_until("then")
            self.play(Transform(tbox, token_box(idef.find("rev_app"), idef)),
                      *[TransformFromCopy(row_a.cells[2 - j], row_b.cells[j], path_arc=PI / 4) for j in range(3)],
                      TransformFromCopy(VGroup(*call.find("[4]")), row_b.cells[3]),
                      *[GrowArrow(a) for a in row_b.arrows], FadeIn(row_b.nil),
                      time_span(FadeIn(creply, shift=0.2 * LEFT), 0.9, 1.6),
                      run_time=min(1.6, c.until("double", floor=1.0)))
            settle(self, row_b)
            # "It's iterative, but it makes twice as many conses as plain append."
            c.wait_until("double")
            self.play(FadeIn(lc, shift=0.2 * UP),
                      LaggedStart(*flash([*row_a.cells, *row_b.cells[:3]], GOLD, time_width=1.5), lag_ratio=0.12),
                      run_time=1.5)
            c.wait_until("plain append")
            self.play(FadeIn(rcnt, shift=0.2 * UP), run_time=0.9)
            # "So if an accumulator forces an extra reversal, the iterative version can be much
            # slower than the recursive one."
            c.wait_until("rule")
            self.play(FadeIn(rext, shift=0.2 * LEFT), Create(extra), FadeOut(tbox), run_time=1.0)
            c.wait_until("much slower")
            self.play(FlashAround(lc, color=RED, time_width=1.5), run_time=1.4)

    # ── recap.1: four lines, each on its cue; then the teaser ────────────────────
    def recap(self):
        title = T("Recap", size=48).move_to([0, 3.25, 0])
        app = Code("xs @ ys", size=32)
        app.find("@")[0].set_color(GOLD)
        ys = Code("ys", size=32).set_color(TEAL)
        lines = [
            [app, T("copies", size=34), Code("xs", size=32), T("and", size=34),
             T("shares", size=34, color=TEAL), ys],
            [T("Adding at the end copies, so", size=34), Code("nrev", size=32).set_color(YELLOW),
             T("is", size=34), *cost(r"O(n^2)", "time", color=RED)],
            [Code("rev_app", size=32).set_color(YELLOW), T("makes one cons per element:", size=34),
             *cost(r"O(n)", "time")],
            [T("Reduction in strength:", size=34, color=YELLOW), T("one expensive", size=34, color=RED),
             MathTex(r"\rightarrow", font_size=40), T("many cheap", size=34, color=TEAL)],
        ]
        rows = []
        for ln in lines:
            body = VGroup(*ln).arrange(RIGHT, buff=0.22)
            rows.append(VGroup(Dot(radius=0.07, color=BLUE), *body))
            rows[-1][0].next_to(body, LEFT, buff=0.3)
        rows = VGroup(*rows)
        for row in rows[1:3]:                       # a cost's word sits a touch low beside its O(..)
            for i, m in enumerate(row):
                if isinstance(m, MathTex) and i + 1 < len(row):
                    row[i + 1].align_to(m, DOWN).shift(UP * 0.06)
        left = -max(r.width for r in rows) / 2
        for i, r in enumerate(rows):
            r.move_to([left, 2.4 - 0.65 * i, 0], aligned_edge=LEFT)

        nxt = VGroup(T("Next:", size=40, color=DIM), T("strings and characters", size=40, color=YELLOW))
        nxt.arrange(RIGHT, buff=0.25).move_to([0, -0.95, 0])
        ch = Code("'a'", size=48).move_to([-1.7, -2.05, 0])
        st = Code('"abc"', size=48).move_to([1.7, -2.05, 0])
        ex = VGroup(T("then", size=36, color=DIM), T("exercises", size=36, color=YELLOW))
        ex.arrange(RIGHT, buff=0.2).move_to([0, -3.1, 0])

        def part(row, a, b, run_time, *extra):
            self.play(*[FadeIn(m, shift=0.25 * UP) for m in row[a:b]], *extra, run_time=run_time)

        with self.say("c4.recap.1") as c:
            # "Let's recap."
            sweep_clear(self, time_span(FadeIn(title, shift=0.3 * DOWN), 0.4, 1.0),
                        run_time=min(1.2, c.until("r1")))
            # "Append copies its first list and shares its second, so its cost depends only on the
            # first list."
            c.wait_until("r1")
            self.play(FadeIn(rows[0], shift=0.25 * UP, lag_ratio=0.02), run_time=1.5)
            c.wait_until("so its cost")
            self.play(*recolor(rows[0][3].text, GOLD), FlashUnder(rows[0][3], color=GOLD), run_time=1.2)
            # "Adding to the end means copying, and doing that at every step made en-rev quadratic."
            c.wait_until("r2")
            part(rows[1], 0, 4, 1.5, rows[0].animate.set_opacity(0.5))
            c.wait_until("quadratic")
            part(rows[1], 4, 6, 1.0)
            settle(self, rows[1])
            # "Rev-app moves elements one at a time onto an accumulator, and reverses a list with
            # exactly one cons per element."
            c.wait_until("r3")
            part(rows[2], 0, 3, 1.5, rows[1].animate.set_opacity(0.5))
            c.wait_until("exactly one cons")
            part(rows[2], 3, 5, 1.0)
            settle(self, rows[2])
            # "And replacing an expensive operation with a series of cheap ones is reduction in strength."
            c.wait_until("r4")
            self.play(FadeIn(rows[3], shift=0.25 * UP, lag_ratio=0.02),
                      rows[2].animate.set_opacity(0.5), run_time=1.5)
            c.wait_until("reduction in strength")
            self.play(FlashUnder(rows[3][1], color=YELLOW), run_time=1.2)
            # "Next time, strings and characters, and then some exercises to try yourself."
            c.wait_until("next")
            self.play(*[r.animate.set_opacity(1) for r in rows[:3]], FadeIn(nxt, shift=0.25 * UP),
                      run_time=1.2)
            c.wait_until("characters")
            self.play(FadeIn(ch, shift=0.25 * DOWN), FadeIn(st, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("exercises")
            self.play(FadeIn(ex, shift=0.25 * UP), run_time=0.9)
