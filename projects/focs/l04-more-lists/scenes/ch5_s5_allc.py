"""Chapter 5, scene 5: putting c on every answer (allc). Clips c5.allc.1 – c5.allc.4.

OPENS on s4's hand-off: In [72] = Code(SRC72, size=24), default highlighting, left x = -6.2,
top y = 3.6 (s4 docstring). It fades in, then the four allc lines lift out to hero size.

HAND-OFF TO s6 (ch5_s6_trace), the {input}/{output} pair of clip 2 (c5.allc.2), at its end:
  inp = solutions([[2], [1, 1]]).scale(1.2)       # helpers copied from s1: coin(v).scale(0.6)
  out = solutions([[2, 2], [2, 1, 1]]).scale(1.2) #   in TEAL boxes (stroke 3 / big box stroke 4)
  inp centre (0.6, 0.5), 3.23 wide x 1.37 tall; out centre (0.6, -1.75), 4.68 wide x 1.37 tall
  (at scale 1 they are 2.69 / 3.90 wide x 1.14 tall: divide by 1.2 for the ~4-wide version).
  Between them: Arrow(inp.get_bottom(), out.get_top(), buff=0.12, YELLOW, stroke_width=4) with
  Mono("allc", 32, YELLOW) next_to it RIGHT, buff 0.2. The c = 2 disc: coin(2) (r 0.42) at
  (-3.0, -0.62), Mono("c = 2", 30) LEFT of it, buff 0.3. GOLD "2 solutions -> 2 solutions" (T 34,
  MathTex arrow) centred at (0.6, -3.0). Above, the allc hero Code(HERO, 34) scaled 0.8, top y 3.55.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the coin (copied from scenes/ch1_s1_hook.py) and the chapter's solution boxes ──────────
COIN_R = 0.42
COIN_LABEL = 34


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def solution(values, s=0.6):
    """One way to make change: coins (scaled s) in a row inside a TEAL rounded box."""
    if values:
        inner = VGroup(*[coin(v).scale(s) for v in values]).arrange(RIGHT, buff=0.1)
    else:
        inner = Square(side_length=2 * COIN_R * s).set_opacity(0)
    box = RoundedRectangle(corner_radius=0.1, width=inner.width + 0.24, height=inner.height + 0.24)
    box.set_stroke(TEAL, 3).move_to(inner)
    return VGroup(box, inner)


def solutions(lists):
    """A list of solutions: solution boxes in a row inside a bigger TEAL rounded box.
    [0] is the big box, [1:] the solutions; solution[0] its box, solution[1] its coins."""
    row = VGroup(*[solution(v) for v in lists]).arrange(RIGHT, buff=0.2)
    big = RoundedRectangle(corner_radius=0.15, width=row.width + 0.4, height=row.height + 0.4)
    big.set_stroke(TEAL, 4).move_to(row)
    return VGroup(big, *row)


# ── code ──────────────────────────────────────────────────────────────────────
SRC72 = (
    "let rec change till amt =\n"
    "  match till, amt with\n"
    "  | _       , 0   -> [ [] ]\n"
    "  | []      , _   -> []\n"
    "  | c::till , amt -> if amt < c then change till amt\n"
    "                    else let rec allc = function\n"
    "                           | [] -> []\n"
    "                           | cs :: css -> (c::cs) :: allc css\n"
    "                         in\n"
    "                           allc (change (c::till) (amt - c)) @\n"
    "                                 change till amt"
)
C72_SIZE, C72_LEFT, C72_TOP = 24, -6.2, 3.6          # s4's hand-off

HERO = (
    "let rec allc = function\n"
    "  | [] -> []\n"
    "  | cs :: css -> (c::cs) :: allc css\n"
    "in"
)
HERO_SIZE, HERO_TOP = 34, 3.3

ALONE = (
    "let rec allc = function\n"
    "  | [] -> []\n"
    "  | cs :: css -> (c::cs) :: allc css;;"
)
ALONE_ERR = (
    "Line 3, characters 18-19:\n"
    "3 |   | cs :: css -> (c::cs) :: allc css;;\n"
    "                      ^\n"
    "Error: Unbound value c"
)

EDIT = (
    "let rec change till amt =\n"
    "  match till, amt with\n"
    "  | _       , 0   -> [ [] ]\n"
    "  | []      , _   -> []\n"
    "  | c::till , amt -> if amt < c then change till amt\n"
    "                    else (c :: change (c::till) (amt - c)) @\n"
    "                              change till amt"
)
EDIT_ERR = (
    "Error: This expression has type 'a list list\n"
    "       but an expression was expected of type int list\n"
    "       Type 'a list is not compatible with type int"
)
ERR_SIZE = 28

# ── layout ────────────────────────────────────────────────────────────────────
DATA = [[5], [2, 2, 1], [2, 1, 1, 1]]          # clip 1: some list of solutions
DATA_Y, DATA_SCALE = -1.0, 1.3
EX_X, INP_Y, OUT_Y, EX_SCALE = 0.6, 0.5, -1.75, 1.2   # clip 2: the example pair (s6 reuses it)
HOVER = np.array([-3.0, -0.62, 0])
SAME_Y = -3.0
HERO_SHRINK, HERO_SHRUNK_TOP = 0.8, 3.55        # clip 2: the hero steps up to make room
WRONG_Y, WRONG_SCALE = -0.95, 1.3               # clip 4: the wrong row under the edit
ERR_Y = -2.75
NAMES_Y, NAME_LABEL_Y, NAME_PIC_Y = 1.0, -0.3, -1.75
NAME_SIZE = 110


def place72(code):
    return code.shift(RIGHT * (C72_LEFT - code.get_left()[0]) + UP * (C72_TOP - code.get_top()[1]))


def make72(chapter_colours=True):
    """In [72] at s4's spot; chapter colours = recursive calls YELLOW, `@` GOLD."""
    code = place72(Code(SRC72, size=C72_SIZE))
    if chapter_colours:
        for k in (1, 2, 3):
            code.find("change", nth=k).set_color(YELLOW)
        for k in (1, 2):
            code.find("allc", nth=k).set_color(YELLOW)
        code.find("@").set_color(GOLD)
    return code


def glyphs_of(code, n):
    return [g for i in range(n) for g in code.line(i)]


def to_op(glyphs, op):
    """One opacity animation per glyph (glyphs stay inside their Code)."""
    return [g.animate.set_opacity(op) for g in glyphs]


def pointer(color=YELLOW):
    return Triangle().rotate(PI).scale(0.17).set_fill(color, 1).set_stroke(width=0)


class Allc(NarratedScene):
    def construct(self):
        self.code72 = make72(chapter_colours=False)
        self.play(FadeIn(self.code72), run_time=0.8)        # s4's last shot comes back
        self.wait(0.4)
        self.what_it_does()
        self.example()
        self.why_local()
        self.tempting_edit()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c5.allc.1: the four lines, walk, base case, step ─────────────────────────
    def what_it_does(self):
        code72 = self.code72
        hero = Code(HERO, size=HERO_SIZE)
        hero.find("allc", nth=1).set_color(YELLOW)
        hero.move_to(UP * (HERO_TOP - hero.height / 2))
        self.hero = hero
        srcs = [code72.find("let rec allc = function"), code72.line(6), code72.line(7), code72.line(8)]
        parts = [hero.line(i) for i in range(4)]

        data = solutions(DATA).scale(DATA_SCALE).move_to(UP * DATA_Y)
        sols = list(data[1:])

        with self.say("c5.allc.1") as c:
            c.wait_until("what")
            self.play(*[TransformFromCopy(s, p) for s, p in zip(srcs, parts)],
                      time_span(FadeOut(code72), 0.2, 1.4), run_time=2.0)
            self.remove(*parts)
            self.add(hero)
            self.play(FadeIn(data, lag_ratio=0.2), run_time=1.2)

            # {walk}: a pointer steps down the list
            c.wait_until("walk")
            ptr = pointer().next_to(sols[0], UP, buff=0.42)
            self.play(FadeIn(ptr, shift=0.2 * DOWN), run_time=0.6)
            self.wait(0.3)
            for s in sols[1:]:
                self.play(ptr.animate.next_to(s, UP, buff=0.42), run_time=0.7)
                self.wait(0.3)

            # {base}: no solutions in, no solutions out
            c.wait_until("base")
            box = token_box(hero.line(1), hero.line(1))
            self.play(FadeOut(ptr), FadeIn(box), run_time=0.8)

            # {step}: cs and css
            c.wait_until("step")
            self.play(Transform(box, token_box(hero.find("cs :: css"), hero.line(2))), run_time=1.0)
            bottom = data[0].get_bottom()[1]
            labels = []
            for key, text, group, cue in (("cs", "one solution", sols[:1], "a first solution"),
                                          ("css", "the rest", sols[1:], "the rest")):
                left, right = group[0].get_left()[0], group[-1].get_right()[0]
                br = span_brace(np.array([left, bottom, 0]), np.array([right, bottom, 0]), color=DIM)
                tok = Mono(key, size=HERO_SIZE).next_to(br, DOWN, buff=0.14)
                lab = T(text, size=30).next_to(tok, DOWN, buff=0.14)
                c.wait_until(cue)
                src = hero.find("cs" if key == "cs" else "css", line=2)
                self.play(GrowFromCenter(br), TransformFromCopy(src, tok),
                          time_span(FadeIn(lab, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
                labels += [br, tok, lab]

            # {cons}: (c::cs), then the same to the rest
            c.wait_until("cons")
            ccs = hero.find("(c::cs)")
            self.play(Transform(box, token_box(ccs, hero.line(2))), *recolor(ccs, YELLOW), run_time=1.0)
            c.wait_until("does the same")
            self.play(Transform(box, token_box(hero.find("allc css"), hero.line(2))), run_time=1.0)
        self.data, self.box, self.labels = data, box, labels

    # ── c5.allc.2: c = 2 on [[2]; [1; 1]] ─────────────────────────────────────────
    def example(self):
        hover = coin(2).move_to(HOVER)
        c_lab = Mono("c = 2", size=30).next_to(hover, LEFT, buff=0.3)
        inp = solutions([[2], [1, 1]]).scale(EX_SCALE).move_to([EX_X, INP_Y, 0])
        out = solutions([[2, 2], [2, 1, 1]]).scale(EX_SCALE).move_to([EX_X, OUT_Y, 0])
        arrow = Arrow(inp.get_bottom(), out.get_top(), buff=0.12, color=YELLOW, stroke_width=4)
        a_lab = Mono("allc", size=32, color=YELLOW).next_to(arrow, RIGHT, buff=0.2)
        same = VGroup(T("2 solutions", size=34, color=GOLD), MathTex(r"\to", color=GOLD),
                      T("2 solutions", size=34, color=GOLD)).arrange(RIGHT, buff=0.25)
        same.move_to([EX_X, SAME_Y, 0])
        fronts = [out[1][1][0], out[2][1][0]]
        skeleton = [(inp[0], out[0]), (inp[1][0], out[1][0]), (inp[1][1][0], out[1][1][1]),
                    (inp[2][0], out[2][0]), (inp[2][1][0], out[2][1][1]), (inp[2][1][1], out[2][1][2])]

        with self.say("c5.allc.2") as c:
            # {example}: the coin two
            hero = self.hero
            hero.generate_target()
            hero.target.scale(HERO_SHRINK)
            hero.target.shift(UP * (HERO_SHRUNK_TOP - hero.target.get_top()[1]))
            self.play(FadeOut(self.data), FadeOut(self.box), *[FadeOut(m) for m in self.labels],
                      MoveToTarget(hero),
                      time_span(FadeIn(hover, scale=0.8), 0.5, 1.5),
                      time_span(FadeIn(c_lab, shift=0.2 * DOWN), 0.7, 1.5), run_time=1.5)

            # {input}: two solutions
            c.wait_until("input")
            self.play(FadeIn(inp, lag_ratio=0.3), run_time=1.4)
            c.wait_until("a single two")
            self.play(FlashAround(inp[1], color=YELLOW, run_time=1.2))
            c.wait_until("one plus one")
            self.play(FlashAround(inp[2], color=YELLOW, run_time=1.2))

            # {output}: the 2 goes onto the front of each
            c.wait_until("output")
            self.play(GrowArrow(arrow), FadeIn(a_lab, shift=0.2 * DOWN),
                      *[time_span(TransformFromCopy(s, t), 0.3, 1.5) for s, t in skeleton],
                      run_time=1.5)
            self.play(TransformFromCopy(hover, fronts[0]), run_time=1.0)
            c.wait_until("and two")
            self.play(TransformFromCopy(hover, fronts[1]), run_time=0.9)
            settle(self, out)

            # {same}: as many solutions, each one longer
            c.wait_until("same")
            self.play(FadeIn(same, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("each one coin longer")
            self.play(*[FlashAround(f, color=YELLOW, run_time=1.4) for f in fronts])
        self.example_mobs = [hover, c_lab, inp, out, arrow, a_lab]
        self.same = same

    # ── c5.allc.3: why allc lives inside change ──────────────────────────────────
    def why_local(self):
        hero = self.hero
        code = make72()
        homes = [code.find("let rec allc = function"), code.line(6), code.line(7), code.line(8)]
        targets = [VGroup(*[g.copy() for g in h]) for h in homes]
        for h in homes:
            for g in h:
                g.set_opacity(0)
        everything = glyphs_of(code, 11)

        alone = Code(ALONE, size=HERO_SIZE)
        alone.find("allc", nth=1).set_color(YELLOW)
        err = Code(ALONE_ERR, size=ERR_SIZE).set_color(RED)
        VGroup(alone, err).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(ORIGIN)

        with self.say("c5.allc.3") as c:
            # {local}: back into In [72]
            self.play(*[ReplacementTransform(hero.line(i), targets[i]) for i in range(4)],
                      *[time_span(FadeOut(m), 0, 1.0) for m in self.example_mobs],
                      time_span(FadeOut(self.same), 1.0, 2.0),
                      time_span(FadeIn(code), 0.5, 2.0), run_time=2.0)
            self.remove(hero, *targets)
            for h in homes:
                for g in h:
                    g.set_opacity(1)

            # {needs}: the c of (c::cs) is the c of c::till
            c.wait_until("needs")
            c_use = code.find("(c::cs)")[1]
            c_home = code.find("c::till")[0]
            keep = {id(c_use), id(c_home)}
            self.play(*to_op([g for g in everything if id(g) not in keep], DIMMED),
                      *recolor([c_use, c_home], YELLOW), run_time=1.2)
            arrow = CurvedArrow(c_use.get_bottom() + 0.08 * DOWN, c_home.get_bottom() + 0.08 * DOWN,
                                angle=-PI / 3, color=YELLOW, stroke_width=4)
            self.play(Create(arrow), FlashAround(c_home, color=YELLOW, run_time=1.4), run_time=1.4)
            c.wait_until("third clause")
            clause = [g for i in range(4, 11) for g in code.line(i) if id(g) not in keep]
            self.play(*to_op(clause, 1), run_time=1.0)

            # {outside}: allc alone at top level, and OCaml's error
            c.wait_until("outside")
            pairs = [(code.find("let rec allc = function"), alone.line(0)), (code.line(6), alone.line(1)),
                     (code.line(7), alone.find("| cs :: css -> (c::cs) :: allc css"))]
            semis = alone.find(";;")
            self.play(*[TransformFromCopy(s, t) for s, t in pairs],
                      time_span(FadeIn(semis), 0.9, 1.4),
                      time_span(FadeOut(code), 0, 1.0), time_span(FadeOut(arrow), 0, 0.8),
                      time_span(FadeIn(err, shift=0.2 * DOWN, lag_ratio=0.1), 1.2, 2.0), run_time=2.0)
            self.remove(*[t for _, t in pairs], semis)
            self.add(alone)

            c.wait_until("unbound there")
            c_bad = alone.find("(c::cs)")[1]
            self.play(*recolor([c_bad], RED), FlashAround(c_bad, color=RED, run_time=1.4), run_time=1.4)

            # {letin}: a let ... in, local, as in unzip
            c.wait_until("letin")
            code2 = make72()
            region = [g for g in code2.find("let rec allc = function")] + \
                     [g for i in (6, 7, 8) for g in code2.line(i)]
            region_ids = {id(g) for g in region}
            rest = [g for g in glyphs_of(code2, 11) if id(g) not in region_ids]
            top = code2.line(5).get_top()[1] + 0.04
            bot = code2.line(8).get_bottom()[1] - 0.04
            x = code2.find("else")[0].get_left()[0] - 0.3
            brace = Brace(Line([x, top, 0], [x, bot, 0]), LEFT, buff=0.08, color=YELLOW)
            lab = T("local, as in unzip", size=30, color=YELLOW).next_to(brace, LEFT, buff=0.15)
            for g in rest:
                g.set_opacity(DIMMED)
            self.play(FadeOut(alone), FadeOut(err), time_span(FadeIn(code2), 0.4, 1.4),
                      time_span(GrowFromCenter(brace), 1.0, 1.8),
                      time_span(FadeIn(lab, shift=0.2 * LEFT), 1.2, 2.0), run_time=2.0)
            c.wait_until("recursive function")
            self.play(FlashAround(code2.find("rec", line=5), color=YELLOW, run_time=1.4))
        self.code2, self.brace, self.brace_lab = code2, brace, lab

    # ── c5.allc.4: the tempting edit, its type error, and the names ─────────────
    def tempting_edit(self):
        old = self.code2
        edit = Code(EDIT, size=C72_SIZE)
        for k in (1, 2, 3):
            edit.find("change", nth=k).set_color(YELLOW)
        edit.find("@").set_color(GOLD)
        edit.shift(RIGHT * (C72_LEFT - edit.get_left()[0]) + UP * (C72_TOP - edit.get_top()[1]))

        moves = [(old.line(i), edit.line(i)) for i in range(5)]
        moves += [(old.find("else"), edit.find("else")),
                  (VGroup(old.find("(change", line=9)[0]), VGroup(edit.find("(c ::", line=5)[0])),
                  (old.find("change (c::till) (amt - c)) @", line=9),
                   edit.find("change (c::till) (amt - c)) @", line=5)),
                  (old.line(10), edit.line(6))]
        gone = [old.find("let rec allc = function"), old.line(6), old.line(7), old.line(8),
                old.find("allc", line=9)]
        new = VGroup(*edit.find("(c ::", line=5)[1:])

        k = WRONG_SCALE
        wrong = solutions([[2], [1, 1]]).scale(k)
        lone = coin(2).scale(0.6 * k)
        wide = RoundedRectangle(corner_radius=0.15 * k, width=wrong[0].width + lone.width + 0.2 * k,
                                height=wrong[0].height).set_stroke(TEAL, 4)
        wide.move_to([0, WRONG_Y, 0])
        wrong.align_to(wide, RIGHT).set_y(WRONG_Y)
        lone_home = np.array([wide.get_left()[0] + 0.2 * k + lone.width / 2, WRONG_Y, 0])
        lone.move_to(lone_home + LEFT * 1.8)
        qmark = T("?", size=64, color=RED).next_to(wide, LEFT, buff=0.4)

        err = Code(EDIT_ERR, size=ERR_SIZE).set_color(RED)
        err.shift(RIGHT * (C72_LEFT - err.get_left()[0])).set_y(ERR_Y)
        bad = edit.find("change (c::till) (amt - c)", line=5)
        ul = underline(VGroup(*bad), RED, buff=0.05).set_stroke(width=4)

        with self.say("c5.allc.4") as c:
            # {tempt}: skip allc, cons c straight on
            self.play(*[time_span(ReplacementTransform(s, t), 0.4, 2.0) for s, t in moves],
                      *[time_span(FadeOut(g), 0, 0.8) for g in gone], time_span(FadeIn(new), 1.2, 2.0),
                      time_span(FadeOut(self.brace), 0, 0.6), time_span(FadeOut(self.brace_lab), 0, 0.6),
                      run_time=2.0)
            self.remove(old, *[t for _, t in moves], new)
            self.add(edit)
            c.wait_until("straight onto")
            self.play(FlashUnder(edit.find("(c :: change (c::till) (amt - c))", line=5),
                                 color=YELLOW, run_time=1.5))

            # {wrong}: the coin joins as one more solution
            c.wait_until("wrong")
            self.play(FadeIn(wrong, lag_ratio=0.2), FadeIn(lone, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("one more solution")
            self.play(lone.animate.move_to(lone_home), ReplacementTransform(wrong[0], wide), run_time=1.5)
            self.play(FadeIn(qmark, shift=0.2 * DOWN), run_time=0.8)

            # {error}: OCaml rejects it
            c.wait_until("error")
            self.play(Create(ul), FadeIn(err, shift=0.2 * DOWN, lag_ratio=0.1), run_time=1.2)
            c.wait_until("a list of coins")
            self.play(FlashAround(err.find("int list"), color=YELLOW, run_time=1.5))
            c.wait_until("a list of lists")
            self.play(FlashAround(err.find("'a list list"), color=YELLOW, run_time=1.5))

            # {names}: cs, css, and L3's xs
            c.wait_until("names")
            xs = Mono("xs", size=90, color=DIM)
            cs = Mono("cs", size=NAME_SIZE)
            css = Mono("css", size=NAME_SIZE)
            xs.move_to([-4.9, NAMES_Y, 0])
            cs.move_to([-1.25, NAMES_Y, 0])
            css.move_to([3.4, NAMES_Y, 0])
            for m in (xs, cs, css):
                m.align_to(cs, DOWN)
            sweep_clear(self, time_span(FadeIn(VGroup(xs, cs, css), lag_ratio=0.25), 0.6, 1.6),
                        run_time=1.6)

            c.wait_until("cs")
            cs_lab = T("a list of coins", size=34).move_to([cs.get_x(), NAME_LABEL_Y, 0])
            cs_pic = solution([2, 1, 1], s=0.75).move_to([cs.get_x(), NAME_PIC_Y, 0])
            self.play(FadeIn(cs_lab, shift=0.2 * DOWN), time_span(FadeIn(cs_pic), 0.4, 1.2), run_time=1.2)
            c.wait_until("css")
            css_lab = T("a list of such lists", size=34).move_to([css.get_x(), NAME_LABEL_Y, 0])
            css_pic = solutions([[2, 2], [2, 1, 1]]).scale(1.25).move_to([css.get_x(), NAME_PIC_Y, 0])
            self.play(FadeIn(css_lab, shift=0.2 * DOWN), time_span(FadeIn(css_pic), 0.4, 1.2),
                      run_time=1.2)

            # {plural}: every trailing s
            c.wait_until("plural")
            s_cs, s_css = cs[-1], css[-1]
            self.play(*recolor([s_cs, s_css], YELLOW),
                      FlashAround(s_cs, color=YELLOW, run_time=1.5),
                      FlashAround(s_css, color=YELLOW, run_time=1.5), run_time=1.5)
            c.wait_until("just as exes")
            self.play(xs[0].animate.set_color(FG), xs[1].animate.set_color(YELLOW),
                      FlashAround(xs[1], color=YELLOW, run_time=1.5), run_time=1.5)
            c.wait_until()
