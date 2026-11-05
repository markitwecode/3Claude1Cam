"""Chapter 6, scene 4: faster, still slow, and stepwise refinement. Clips c6.refine.1 – c6.refine.4.

refine.1  In [72] (ch5's end-card look: Code default, the line-9 `allc` call and `@` GOLD) Code 18,
          top-right (right x 6.45, top y 3.6), dimmed to 0.3 except the GOLD tokens and their GOLD
          token_boxes. In [73] (s2's colours: every `change` YELLOW, default highlighting otherwise)
          Code 24, bottom-left (left x -6.6, bottom y -3.6), `c::chg` (line 5) and the passed-along
          `chgs` (line 6) GREEN-boxed. Side by side does not fit (62 + 61 columns), so the old code
          sits above, the new one below. {cons}: GOLD "many allc conses" beside the allc box;
          {one}: GREEN arrow to GREEN "one c::chg" above its box; {append}: GREEN "chgs instead"
          under the @, chgs box flashes; "no append": RED cross over the @.
refine.2  {faster}: the notes' words "several times faster" (italic) y 3.1; GOLD bars "all ways"
          (9.0 long) and "faster" (3.6) from x -3.4, grown linearly in proportion to their length.
          {measured}: copies of the short bar tile the long one (2 + a half), GOLD "≈ 2.5×", DIM
          "measured in the OCaml 5.4.1 toplevel". {still}: RED "still extremely slow".
          {count}: the call (Code 30) and its reply, 4366 GOLD. {every}: rows of tiny TEAL
          solution boxes pour in from the bottom and fill the frame around the call.
refine.3  {three}: three step cards; {simple}/{all}/{fast} fill them, with the greedy and every-way
          replies (Code 26) under the row, each with its number badge; {name}: header.
refine.4  recipe lines under the row (left x -1.6), each flashing its card; {discard}: card 1 dims to
          0.35 and slides down to (-4.6, -1.45); {learned}: YELLOW tag under it.

STEP CARDS (s7's recap reuses them, small):
  three DIM-outlined RoundedRectangles (corner 0.18, 3.7 x 2.3, stroke 2.5) centred at x -4.6, 0,
  4.6, y 1.3; inside each, from the top: a GOLD number ring (Circle r 0.3, stroke 2.5) with a GOLD
  T 32 digit at y +0.68, the title T 40 FG at y 0, a tag T 30 at y -0.65: 1 "greedy" + RED "can
  fail"; 2 "every way" (no tag); 3 "faster" + GREEN "two accumulators". DIM arrows (stroke 4,
  buff 0.1) between the cards turn YELLOW at {name}. Header "stepwise refinement" T 52 YELLOW at
  y 3.2. Recipe (T 36 FG, left-aligned, left x -1.6, y -0.55 / -1.45 / -2.35): "start very
  simple", "add requirements one at a time", "efficiency last of all".

Note: In [72] is ch5's string (27 spaces before `| [] -> []`); the script's quote has 28.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── code and replies, verbatim (In [72] as ch5 shows it; In [73] from the brief) ───
IN72 = """let rec change till amt =
  match till, amt with
  | _       , 0   -> [ [] ]
  | []      , _   -> []
  | c::till , amt -> if amt < c then change till amt
                    else let rec allc = function
                           | [] -> []
                           | cs :: css -> (c::cs) :: allc css
                         in
                           allc (change (c::till) (amt - c)) @
                                 change till amt"""
CALL_LINE = 9                       # "allc (change (c::till) (amt - c)) @"
IN73 = """let rec change till amt chg chgs =
  match till, amt with
  | _       , 0   -> chg::chgs
  | []      , _   -> chgs
  | c::till , amt -> if amt < 0 then chgs
                     else change (c::till) (amt - c) (c::chg)
                                 (change till amt chg chgs)"""
R1 = "val change : int list -> int -> int list = <fun>"
R2 = "val change : int list -> int -> int list list = <fun>"
CALL = "List.length (change [50; 20; 10; 5; 2; 1] 99 [] [])"
REPLY = "- : int = 4366"

# ── layout ─────────────────────────────────────────────────────────────────────
OLD_SIZE, NEW_SIZE = 18, 24
OLD_OP = 0.3

CAP_Y = 3.1
BAR_L, LONG, BAR_H = -3.4, 9.0, 0.55
SHORT = LONG / 2.5
BAR1_Y, BAR2_Y = 2.05, 1.1
MEAS_Y = 0.25
CALL_Y, REPLY_GAP = -1.05, 0.8

CARD_W, CARD_H, CARD_Y = 3.7, 2.3, 1.3
CARD_X = (-4.6, 0.0, 4.6)
HEAD_Y = 3.2
REPLY_ROWS = (-0.55, -1.35)
REPLY_LEFT = -5.9
RECIPE_LEFT, RECIPE_Y = -1.6, (-0.55, -1.45, -2.35)
ASIDE = np.array([0.0, -1.45 - CARD_Y, 0.0])     # card 1's slide


def put_left(mob, x, y):
    return mob.shift(RIGHT * (x - mob.get_left()[0]) + UP * (y - mob.get_y()))


def badge(n, r=0.3, size=32):
    ring = Circle(radius=r).set_stroke(GOLD, 2.5)
    num = T(str(n), size, GOLD).move_to(ring)
    return ring, num


def dim_move(mob, op, scale=1.0, about=None, shift=ORIGIN):
    """restyle's opacity rule (fill on filled parts, stroke on outlines) plus a scale and shift."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_fill(opacity=op)
        else:
            leaf.set_stroke(opacity=op)
    t.scale(scale, about_point=about if about is not None else mob.get_center()).shift(shift)
    return Transform(mob, t)


class RefineScene(NarratedScene):
    def construct(self):
        self.compare()
        self.speed()
        self.steps()
        self.recipe()
        self.wait(2.4)                       # the last tag stays readable before the end
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── refine.1: what the accumulators bought ───────────────────────────────────
    def compare(self):
        old = Code(IN72, size=OLD_SIZE)
        old.shift(RIGHT * (6.45 - old.get_right()[0]) + UP * (3.6 - old.get_top()[1]))
        allc = old.find("allc", line=CALL_LINE)
        app = old.find("@", line=CALL_LINE)
        bright = {id(g) for g in [*allc, *app]}
        for i in range(len(IN72.splitlines())):
            for g in old.line(i):
                if id(g) not in bright:
                    g.set_opacity(OLD_OP)
        for g in [*allc, *app]:
            g.set_color(GOLD)
        allc_box = token_box(allc, old.line(CALL_LINE), color=GOLD)
        app_box = token_box(app, old.line(CALL_LINE), color=GOLD)

        new = Code(IN73, size=NEW_SIZE)
        new.shift(RIGHT * (-6.6 - new.get_left()[0]) + UP * (-3.6 - new.get_bottom()[1]))
        for ln in (0, 5, 6):
            for g in new.find("change", line=ln):
                g.set_color(YELLOW)
        chg_box = token_box(new.find("c::chg", line=5), new.line(5), color=GREEN)
        chgs_box = token_box(new.find("chgs", line=6), new.line(6), color=GREEN)

        many = T("many allc conses", 30, GOLD, t2f={"allc": MONO})
        many.next_to(allc_box, LEFT, buff=0.2)
        one = T("one c::chg", 30, GREEN, t2f={"c::chg": MONO})
        one.next_to(chg_box, UP, buff=0.3)
        arrow = Arrow(allc_box.get_bottom() + 0.05 * DOWN, one.get_left() + 0.12 * LEFT, buff=0,
                      stroke_width=5, color=GREEN, max_tip_length_to_length_ratio=0.12, tip_length=0.22)
        instead = T("chgs instead", 30, GREEN, t2f={"chgs": MONO})
        instead.next_to(app_box, DOWN, buff=0.3)
        if instead.get_right()[0] > 6.6:
            instead.shift((6.6 - instead.get_right()[0]) * RIGHT)
        cross = Cross(app_box, stroke_color=RED, stroke_width=6, scale_factor=1.15)

        with self.say("c6.refine.1") as c:
            # {compare} "So what did the two accumulators buy us?"
            self.play(time_span(FadeIn(old), 0, 1.0), time_span(FadeIn(allc_box), 0, 1.0),
                      time_span(FadeIn(app_box), 0, 1.0),
                      time_span(FadeIn(new, shift=0.2 * UP), 0.5, 1.6), time_span(FadeIn(chg_box), 0.5, 1.6),
                      time_span(FadeIn(chgs_box), 0.5, 1.6), run_time=1.6)
            # {cons} "... all-see consed it onto every solution that came back."
            c.wait_until("cons")
            self.play(FlashAround(allc_box, color=GOLD, time_width=1.5),
                      FadeIn(many, shift=0.3 * RIGHT), run_time=1.5)
            # {one} "Here, a single cons onto the coins so far replaces many of those."
            c.wait_until("one")
            self.play(GrowArrow(arrow), time_span(FadeIn(one, shift=0.3 * DOWN), 0.6, 1.6),
                      time_span(FlashAround(chg_box, color=GREEN, time_width=1.5), 0.8, 1.8), run_time=1.8)
            # {append} "And since the solutions so far are passed along, ..."
            c.wait_until("append")
            self.play(FlashAround(chgs_box, color=GREEN, time_width=1.5),
                      FadeIn(instead, shift=0.3 * UP), run_time=1.5)
            # "... there's no append at all."
            c.wait_until("no append")
            self.play(Create(cross), run_time=1.0)

    # ── refine.2: 2.5x faster, still slow ────────────────────────────────────────
    def speed(self):
        cap = VGroup(T("the notes:", 30, DIM), T("“several times faster”", 40, slant=ITALIC))
        cap.arrange(RIGHT, buff=0.3)
        cap[0].align_to(cap[1], DOWN).shift(0.04 * UP)
        cap.move_to([0, CAP_Y, 0])

        def bar(w, y):
            return Rectangle(width=w, height=BAR_H).set_fill(GOLD, 1).set_stroke(width=0).move_to(
                [BAR_L + w / 2, y, 0])
        bar1, bar2 = bar(LONG, BAR1_Y), bar(SHORT, BAR2_Y)
        lab1 = T("all ways", 34)
        lab2 = T("faster", 34)
        for lab, b in ((lab1, bar1), (lab2, bar2)):
            lab.shift(RIGHT * (BAR_L - 0.3 - lab.get_right()[0]) + UP * (b.get_y() - lab.get_y()))

        def slot(k, w):
            return Rectangle(width=w, height=BAR_H).set_fill(opacity=0).set_stroke(FG, 3).move_to(
                [BAR_L + k * SHORT + w / 2, BAR1_Y, 0])
        slots = [slot(0, SHORT), slot(1, SHORT), slot(2, SHORT / 2)]
        ratio = MathTex(r"\approx 2.5\times", font_size=48, color=GOLD)
        ratio.next_to(bar2, RIGHT, buff=0.3)
        meas = T("measured in the OCaml 5.4.1 toplevel", 28, DIM)
        put_left(meas, lab1.get_left()[0], MEAS_Y)
        slow = T("still extremely slow", 32, RED)
        slow.next_to(ratio, RIGHT, buff=0.45)
        bars = [cap, bar1, bar2, lab1, lab2, *slots, ratio, meas, slow]

        call = Code(CALL, size=30)
        call.move_to([0, CALL_Y, 0])
        reply = Code(REPLY, size=30)
        put_left(reply, call.get_left()[0], CALL_Y - REPLY_GAP)
        n4366 = reply.find("4366")
        for g in n4366:
            g.set_color(GOLD)

        with self.say("c6.refine.2") as c:
            # {faster} "The notes say this version runs several times faster."
            c.wait_until("this version")          # In [72] / In [73] and their tags stay a beat longer
            sweep_clear(self, time_span(FadeIn(cap, shift=0.3 * DOWN), 0.3, 1.2), run_time=1.2)
            # the bars grow at one speed, so the long one takes 2.5 times as long
            self.play(GrowFromEdge(bar1, LEFT, rate_func=linear),
                      time_span(GrowFromEdge(bar2, LEFT, rate_func=linear), 0, 2.2 / 2.5),
                      time_span(FadeIn(lab1), 0, 0.8), time_span(FadeIn(lab2), 0, 0.8), run_time=2.2)
            # {measured} "... about two and a half times faster."
            c.wait_until("measured")
            self.play(LaggedStart(*[TransformFromCopy(bar2, s) for s in slots], lag_ratio=0.35),
                      run_time=1.8)
            self.play(FadeIn(ratio, shift=0.2 * LEFT), FadeIn(meas, shift=0.2 * UP), run_time=1.0)
            # {still} "But it's still extremely slow, for a simple reason."
            c.wait_until("still")
            self.play(FadeIn(slow, shift=0.2 * LEFT), FlashAround(bar2, color=RED, time_width=1.5),
                      run_time=1.3)
            # "The number of solutions grows rapidly with the amount."
            c.wait_until("number of solutions")
            self.play(*[restyle(m, op=0.4) for m in bars], run_time=1.0)
            # {count} "With coins of fifty, twenty, ten, five, two and one pence, ..."
            c.wait_until("count")
            self.play(FadeIn(call, shift=0.2 * UP), run_time=1.2)
            c.wait_until("four thousand")
            self.play(FadeIn(reply, shift=0.2 * DOWN),
                      time_span(FlashAround(VGroup(*n4366).copy(), color=GOLD, time_width=1.5), 0.5, 2.0),
                      run_time=2.0)
            # {every} "And every one of them has to be built."
            c.wait_until("every")
            rows = self.solution_rows(VGroup(call, reply))
            self.play(*[time_span(FadeOut(m), 0, 0.8) for m in bars],
                      LaggedStart(*[FadeIn(r, shift=0.5 * DOWN) for r in rows], lag_ratio=0.08),
                      run_time=min(2.4, max(1.0, c.remaining - 0.1)))

    def solution_rows(self, hole):
        """Rows of tiny TEAL solution boxes covering the frame, bottom row first, around `hole`."""
        w, h, px, py = 0.26, 0.15, 0.34, 0.24
        x0, x1 = hole.get_left()[0] - 0.3, hole.get_right()[0] + 0.3
        y0, y1 = hole.get_bottom()[1] - 0.25, hole.get_top()[1] + 0.25
        rows = []
        y = -4.0 + py / 2
        k = 0
        while y < 4.0:
            row = VGroup()
            x = -7.1 + px / 2 + (px / 2 if k % 2 else 0)
            while x < 7.1:
                if not (x0 < x < x1 and y0 < y < y1):
                    row.add(Rectangle(width=w, height=h).set_stroke(TEAL, 1.2, opacity=0.55)
                            .set_fill(TEAL, opacity=0.14).move_to([x, y, 0]))
                x += px
            if len(row):
                rows.append(row)
            y += py
            k += 1
        return rows

    # ── refine.3: three change functions ─────────────────────────────────────────
    def steps(self):
        self.frames, self.rings, self.nums = [], [], []
        for i, x in enumerate(CARD_X):
            f = RoundedRectangle(corner_radius=0.18, width=CARD_W, height=CARD_H).set_stroke(DIM, 2.5)
            f.move_to([x, CARD_Y, 0])
            ring, num = badge(i + 1)
            VGroup(ring, num).move_to([x, CARD_Y + 0.68, 0])
            self.frames.append(f)
            self.rings.append(ring)
            self.nums.append(num)
        self.arrows = [Arrow(self.frames[i].get_right(), self.frames[i + 1].get_left(), buff=0.1,
                             stroke_width=4, color=DIM, max_tip_length_to_length_ratio=0.4)
                       for i in range(2)]
        names = ("greedy", "every way", "faster")
        self.titles = [T(n, 40).move_to([x, CARD_Y, 0]) for n, x in zip(names, CARD_X)]
        self.fail = T("can fail", 30, RED).move_to([CARD_X[0], CARD_Y - 0.65, 0])
        accs = T("two accumulators", 30, GREEN).move_to([CARD_X[2], CARD_Y - 0.65, 0])
        head = T("stepwise refinement", 52, YELLOW).move_to([0, HEAD_Y, 0])

        self.replies = []
        for k, (src, y) in enumerate(zip((R1, R2), REPLY_ROWS)):
            r = put_left(Code(src, size=26), REPLY_LEFT, y)
            ring, num = badge(k + 1, r=0.24, size=28)
            VGroup(ring, num).move_to([REPLY_LEFT - 0.5, y, 0])
            self.replies.append((r, ring, num))

        cards = [VGroup(f, r, n) for f, r, n in zip(self.frames, self.rings, self.nums)]
        with self.say("c6.refine.3") as c:
            # {three} "Now step back, and look at our three change functions."
            sweep_clear(self, time_span(LaggedStart(*[FadeIn(cd, shift=0.3 * UP) for cd in cards],
                                                    *[GrowArrow(a) for a in self.arrows], lag_ratio=0.25),
                                        0.5, 2.4), run_time=2.4)
            for cd in cards:                      # the cards' parts stand alone from here on
                self.remove(cd)
                self.add(*cd)
            # {simple} "First, a greedy one."
            c.wait_until("simple")
            r1, g1, n1 = self.replies[0]
            self.play(FadeIn(self.titles[0], shift=0.3 * DOWN), FadeIn(r1, shift=0.2 * DOWN),
                      FadeIn(g1), FadeIn(n1), run_time=1.2)
            # "It was simple, but it could fail."
            c.wait_until("could fail")
            self.play(FadeIn(self.fail, shift=0.3 * DOWN), run_time=1.0)
            # {all} "Then one that finds every way."
            c.wait_until("all")
            r2, g2, n2 = self.replies[1]
            self.play(FadeIn(self.titles[1], shift=0.3 * DOWN), TransformFromCopy(r1, r2),
                      TransformFromCopy(g1, g2), TransformFromCopy(n1, n2), run_time=1.6)
            # {fast} "Then the same thing, faster."
            c.wait_until("fast")
            self.play(FadeIn(self.titles[2], shift=0.3 * DOWN), FadeIn(accs, shift=0.3 * DOWN), run_time=1.2)
            # {name} "Improving simple code, step by step like this, ..."
            c.wait_until("name")
            self.play(LaggedStart(*[FlashAround(f, color=YELLOW, time_width=1.5) for f in self.frames],
                                  lag_ratio=0.3),
                      *[a.animate.set_color(YELLOW) for a in self.arrows], run_time=2.0)
            # "... is called stepwise refinement."
            c.wait_until("stepwise refinement")
            self.play(FadeIn(head, shift=0.3 * DOWN), run_time=1.0)

    # ── refine.4: the recipe ─────────────────────────────────────────────────────
    def recipe(self):
        lines = [T(s, 36) for s in ("start very simple", "add requirements one at a time",
                                    "efficiency last of all")]
        for ln, y in zip(lines, RECIPE_Y):
            put_left(ln, RECIPE_LEFT, y)
        card1 = [self.frames[0], self.rings[0], self.nums[0], self.titles[0], self.fail]
        centre = self.frames[0].get_center()
        taught = T("it taught us the task", 30, YELLOW)
        taught.move_to(centre + ASIDE + (CARD_H / 2 + 0.4) * DOWN)

        with self.say("c6.refine.4") as c:
            # {recipe} "The recipe is short."
            self.play(*[FadeOut(m) for r in self.replies for m in r], run_time=1.0)
            for cue, ln, f in zip(("begin", "add", "last"), lines, self.frames):
                c.wait_until(cue)
                self.play(FadeIn(ln, shift=0.3 * DOWN), FlashAround(f, color=YELLOW, time_width=1.5),
                          run_time=1.3)
            # {discard} "Sometimes the simple version has to be thrown away."
            c.wait_until("discard")
            self.play(*[dim_move(m, 0.35, 1.0, centre, ASIDE) for m in card1],
                      FadeOut(self.arrows[0]), run_time=1.6)
            # {learned} "Even then, writing it taught you about the task."
            c.wait_until("learned")
            self.play(FadeIn(taught, shift=0.3 * UP), *[dim_move(m, 0.7) for m in card1], run_time=1.2)
