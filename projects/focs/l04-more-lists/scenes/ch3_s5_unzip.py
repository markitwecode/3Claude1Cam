"""Chapter 3, scene 5: unzip, two results at once. Clips c3.unzip.1 – c3.unzip.5.

Layout notes for neighbours
- {split} replays s1's zip backwards with s1's own layout (S1_* constants, from ch3_s1_hook.py):
  pairs Code 34 at y -2.65, names Code 44 at y 0.9, numbers Code 44 at y -0.6 in the names' columns,
  DIM column lines between; names YELLOW, numbers GOLD; names detour round the numbers row.
- s7 rebuilds: unzip = unzip_code(40) (recursive unzip YELLOW, let-line xs FG); the ladder is plain Code(…, 28): calls left edge -6.6,
  results (OCaml's two-line pair layout) right edge 6.6, rows at y LADDER_YS.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, select, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── s1 hook layout (copied from ch3_s1_hook.py's constants) ──────────────
S1_LIST_SIZE = 44       # Code size of the two stacked lists
S1_NAMES_Y = 0.9        # centre y of ["Amy"; "Bob"; "Cleo"]
S1_NUMS_Y = -0.6        # centre y of [21; 35; 47], numbers under the names' columns
S1_PAIRS_SIZE = 34
S1_PAIRS_Y = -2.65
S1_NAMES = ['"Amy"', '"Bob"', '"Cleo"']
S1_NUMS = ["21", "35", "47"]
S1_NAME_DETOUR = [-1.4, -0.95, -1.55]   # names pass the numbers row round/through its gaps
PAIRS_SRC = '[("Amy", 21); ("Bob", 35); ("Cleo", 47)]'
NAMES_SRC = '["Amy"; "Bob"; "Cleo"]'
NUMS_SRC = "[21; 35; 47]"

UNZIP_SRC = """let rec unzip = function
  | [] -> ([], [])
  | (x, y)::pairs ->
      let xs, ys = unzip pairs in
      (x::xs, y::ys)"""
UNZIP_REPLY = "val unzip : ('a * 'b) list -> 'a list * 'b list = <fun>"

LADDER_SIZE = 28
LADDER_YS = [0.5, -0.7, -1.9, -3.1]
CALLS = ["unzip book", 'unzip [("Bob", 35); ("Cleo", 47)]', 'unzip [("Cleo", 47)]', "unzip []"]
R3_SRC = '(["Cleo"],\n [47])'
R2_SRC = '(["Bob"; "Cleo"],\n [35; 47])'
R1_SRC = '(["Amy"; "Bob"; "Cleo"],\n [21; 35; 47])'
FINAL_REPLY = '- : string list * int list =\n  (["Amy"; "Bob"; "Cleo"], [21; 35; 47])'


# ── glyph helpers (one animation per glyph: never wrap on-screen parts) ──
def G(code):
    return list(code.text.submobjects)


def fly(src, dst):
    src, dst = list(src), list(dst)
    assert len(src) == len(dst), (len(src), len(dst))
    return [TransformFromCopy(a, b) for a, b in zip(src, dst)]


def fade_each(group, **kw):
    return [FadeIn(g, **kw) for g in group]


def rest_of(code, *groups):
    used = {id(g) for grp in groups for g in grp}
    return [g for g in G(code) if id(g) not in used]


def faded_copy(code, keep_lines=(), op=DIMMED):
    keep = {id(g) for i in keep_lines for g in code.line(i)}
    t = code.copy()
    for g, tg in zip(G(code), G(t)):
        tg.set_opacity(1 if id(g) in keep else op)
    return t


def dim_lines(code, lines, op=DIMMED):
    return [g.animate.set_opacity(op) for i in lines for g in code.line(i)]


def left_at(mob, x, y):
    mob.shift([x - mob.get_left()[0], y - mob.get_center()[1], 0])
    return mob


def right_at(mob, x, y):
    mob.shift([x - mob.get_right()[0], y - mob.get_center()[1], 0])
    return mob


def bump_path(offset):
    """Straight from start to end plus a sideways bump (full `offset` halfway); as in s1."""
    def path(start, end, alpha):
        return start + alpha * (end - start) + 4 * alpha * (1 - alpha) * offset
    return path


def unzip_code(size):
    """The unzip definition, chapter colours: the recursive call YELLOW, the let's xs plain like ys."""
    code = Code(UNZIP_SRC, size=size)
    code.find("unzip", line=3).set_color(YELLOW)
    code.find("xs", line=3).set_color(FG)
    return code


def paint_reply(reply):
    for grp in select(reply.text, "'b"):
        for g in grp:
            g.set_color(PURPLE)
    return reply


class UnzipScene(NarratedScene):
    def construct(self):
        self.clip_split()
        self.clip_code()
        self.clip_let()
        self.clip_pattern()
        self.clip_trace()
        self.wait(1.0)   # let the final reply sit
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── 1: the other direction; two results at once ──────────────────────
    def clip_split(self):
        # s1's picture, exactly (see its constants), so its zip can run backwards
        names = Code(NAMES_SRC, size=S1_LIST_SIZE).move_to(UP * S1_NAMES_Y)
        name_g = [names.find(n) for n in S1_NAMES]
        for g in name_g:
            g.set_color(YELLOW)
        cols = [g.get_center()[0] for g in name_g]
        nums = Code(NUMS_SRC, size=S1_LIST_SIZE).move_to(UP * S1_NUMS_Y)
        num_g = [nums.find(n) for n in S1_NUMS]
        semis = [nums.find(";", nth=i) for i in range(2)]
        for i, g in enumerate(num_g):
            dx = cols[i] - g.get_center()[0]
            g.shift(dx * RIGHT)
            if i < 2:
                semis[i].shift(dx * RIGHT)
        nums.find("[").set_x(names.find("[").get_x())
        nums.find("]").set_x(names.find("]").get_x())
        top = names.line(0).get_bottom()[1] - 0.15
        bot = nums.line(0).get_top()[1] + 0.15
        col_lines = [Line([x, top, 0], [x, bot, 0], stroke_width=2.5, color=DIM) for x in cols]
        pairs = Code(PAIRS_SRC, size=S1_PAIRS_SIZE).move_to(UP * S1_PAIRS_Y)
        p_name = [pairs.find(n) for n in S1_NAMES]
        for g in p_name:
            g.set_color(YELLOW)
        p_num = [pairs.find(n) for n in S1_NUMS]

        with self.say("c3.unzip.1") as c:
            # "Now the other direction."
            self.play(FadeIn(pairs, shift=0.2 * UP), run_time=1.0)
            c.wait_until("splits it")
            # "... and splits it into two lists, the first parts and the second parts."
            # s1's zip run backwards: pair by pair, each name (round the numbers row) and its number fly up
            rt = min(2.4, 0.9 * c.until("the second parts"))
            u = rt / 3.0
            anims = [time_span(FadeIn(g), 0, 0.8 * u) for g in rest_of(names, *name_g)]
            anims += [time_span(FadeIn(g), 0, 0.8 * u) for g in rest_of(nums, *num_g)]
            for i in range(3):
                s0 = i * 0.7 * u
                e0 = s0 + 1.6 * u
                anims += [time_span(TransformFromCopy(a, b, path_func=bump_path(S1_NAME_DETOUR[i] * RIGHT)),
                                    s0, e0) for a, b in zip(p_name[i], name_g[i])]
                anims += [time_span(TransformFromCopy(a, b), s0, e0) for a, b in zip(p_num[i], num_g[i])]
            self.play(*anims, run_time=rt)
            self.add(names, nums)
            self.play(*[Create(ln) for ln in col_lines], run_time=0.8)
            c.wait_until("two")
            # "So it has to build two results at once ..."
            self.play(pairs.animate.set_opacity(0.4),
                      FlashAround(names, color=YELLOW, time_width=1.5, run_time=1.6),
                      FlashAround(nums, color=YELLOW, time_width=1.5, run_time=1.6),
                      run_time=1.6)
            c.wait_until("problem")

            # "The recursive call hands back a pair of lists ..."
            lbl = Mono("unzip pairs", size=44, t2c={"unzip": YELLOW})
            box = RoundedRectangle(corner_radius=0.15, width=lbl.width + 0.9, height=lbl.height + 0.8,
                                   color=BLUE, stroke_width=4).move_to(lbl)
            call = VGroup(box, lbl)
            q = Mono("(?, ?)", size=56, t2c={"?": GOLD})
            VGroup(call, q).arrange(RIGHT, buff=2.2).move_to([0, 0.2, 0])
            arrow = Arrow(box.get_right(), q.get_left(), buff=0.25, color=FG, stroke_width=5)
            # the call comes in, then ("hands back") its result slides out of it
            sweep_clear(self, time_span(FadeIn(call, shift=0.2 * DOWN), 0.2, 0.9),
                        time_span(GrowArrow(arrow), 0.8, 1.5),
                        time_span(FadeIn(q, shift=0.6 * RIGHT), 0.8, 1.6), run_time=1.6)
            c.wait_until("both of them")
            qs = select(q, "?")
            self.play(*[FlashAround(g, color=GOLD, time_width=1.5, run_time=1.2) for g in qs],
                      run_time=1.2)
        self.diagram = VGroup(call, arrow, q)

    # ── 2: the definition, walked line by line ───────────────────────────
    def clip_code(self):
        code = unzip_code(40).move_to([-0.45, 0.5, 0])   # room for the tag on the right
        reply = paint_reply(Code(UNZIP_REPLY, size=28)).move_to([0, -2.45, 0])
        self.code, self.reply = code, reply

        def tb(sub, line):
            return token_box(code.find(sub, line=line), code.line(line))

        with self.say("c3.unzip.2") as c:
            # "Here's the definition."
            sweep_clear(self,
                        time_span(FadeIn(code, shift=0.2 * DOWN, lag_ratio=0.02), 0.4, 1.5),
                        time_span(FadeIn(reply, shift=0.2 * DOWN), 1.1, 1.8),
                        run_time=min(1.8, c.until("base")))
            c.wait_until("base")
            # "Unzip of nil is a pair of empty lists."
            box = tb("[] -> ([], [])", 1)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("step")
            # "For a list whose head is the pair, ex comma why,"
            self.play(Transform(box, tb("(x, y)::pairs", 2)), run_time=1.0)
            c.wait_until("let")
            # "let exes comma whys equal the unzip of the rest."
            self.play(Transform(box, tb("let xs, ys = unzip pairs in", 3)), run_time=1.0)
            c.wait_until("cons")
            # "Then ex is consed onto exes,"
            self.play(Transform(box, tb("(x::xs, y::ys)", 4)), run_time=0.7)
            c.wait_until("ex is consed")
            self.play(*fly(code.find("x", line=2), code.find("x", line=4)),
                      *fly(code.find("xs", line=3), code.find("xs", line=4)),
                      run_time=min(1.3, 0.9 * c.until("why onto whys")))
            c.wait_until("why onto whys")
            # "and why onto whys, and we return the two lists as a pair."
            self.play(*fly(code.find("y", line=2), code.find("y", line=4)),
                      *fly(code.find("ys", line=3), code.find("ys", line=4)),
                      run_time=1.3)
            c.wait_until("func")
            # "As with take, the word function supplies the list as an argument with no name."
            fn = code.find("function", line=0)
            tag = VGroup(*[T(s, size=30, color=DIM) for s in ("the list:", "an unnamed argument",
                                                              "(as in take)")])
            tag.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            left_at(tag, fn.get_right()[0] + 0.45, fn.get_center()[1] - 0.2)
            self.play(Transform(box, tb("function", 0)), FadeIn(tag, shift=0.3 * LEFT), run_time=1.1)
            c.wait_until("the word function")
            self.play(FlashAround(fn, time_width=1.5, run_time=1.3), run_time=1.3)
        self.box, self.tag = box, tag

    # ── 3: let, refreshed: an expression with a value ────────────────────
    def clip_let(self):
        code = self.code
        row2 = Code("1 + (let half = 21 in half + half)", size=40).move_to([0, -1.8, 0])
        inner = row2.find("let half = 21 in half + half")
        row1 = Code("let half = 21 in half + half", size=40)
        row1.move_to([0, 0.3, 0]).shift((inner.get_left()[0] - row1.get_left()[0]) * RIGHT)
        reply1 = left_at(Code("- : int = 42", size=36), row1.get_left()[0], row1.get_y() - 0.85)
        reply2 = left_at(Code("- : int = 43", size=36), row2.get_left()[0], row2.get_y() - 0.85)
        self.row1 = row1

        def tb(sub):
            return token_box(row1.find(sub), row1.line(0))

        with self.say("c3.unzip.3") as c:
            # "That let deserves a closer look."  (spotlight in place, then slide it aside)
            self.play(Transform(self.box, token_box(code.find("let xs, ys = unzip pairs in", line=3),
                                                    code.line(3))),
                      *dim_lines(code, (0, 1, 2, 4)), run_time=1.2)
            c.wait_until("you met let")
            # "You met let in lecture two."
            tgt = faded_copy(code, keep_lines=(3,))
            tgt.scale(0.7)
            tgt.shift([-6.6 - tgt.get_left()[0], 3.6 - tgt.get_top()[1], 0])
            code.target = tgt
            self.play(MoveToTarget(code), FadeOut(self.box), FadeOut(self.tag), FadeOut(self.reply),
                      run_time=min(1.5, 0.9 * c.until("half")))
            c.wait_until("let half equal")
            # "For example, let half equal twenty-one,"
            self.play(*fade_each(row1.find("let half = 21"), shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("in the expression")
            # "in the expression half plus half."
            self.play(*fade_each(row1.find("in half + half"), shift=0.2 * DOWN), run_time=1.0)
            settle(self, row1)
            c.wait_until("value")
            # "It computes twenty-one,"
            box = tb("21")
            self.play(FadeIn(box), run_time=0.7)
            c.wait_until("calls it half")
            # "calls it half inside the second part,"
            self.play(Transform(box, tb("half + half")), run_time=1.0)
            c.wait_until("gives forty-two")
            # "and gives forty-two."
            self.play(FadeIn(reply1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("expr")
            # "The whole let is an expression, so it can go wherever an expression goes,"
            self.play(Transform(box, token_box(row1.line(0), row1.line(0))), run_time=1.1)
            c.wait_until("brackets")
            # "wrapped in brackets if needed."
            brk = [row2.find("(")[0], row2.find(")")[0]]
            brk_cols = [b.get_color() for b in brk]
            for b in brk:
                b.set_color(YELLOW)
            self.play(FadeOut(box), *fly(G(row1), inner),
                      *[FadeIn(b, scale=1.6) for b in brk], run_time=1.4)
            c.wait_until("add one to it")
            # "Add one to it,"
            self.play(*fade_each(row2.find("1 +"), shift=0.3 * RIGHT),
                      *[b.animate.set_color(col) for b, col in zip(brk, brk_cols)],
                      run_time=0.8)
            self.add(row2)
            # "and you get forty-three."
            self.play(FadeIn(reply2, shift=0.3 * DOWN), run_time=min(0.9, max(0.4, c.remaining)))

    # ── 4: the left-hand side is a pattern ───────────────────────────────
    def clip_pattern(self):
        code, row1 = self.code, self.row1
        lpe = Code("let P = E", size=56).move_to([0, 2.4, 0])
        lpe.find("P")[0].set_color(YELLOW)
        lpe.find("E")[0].set_color(BLUE)
        lab_a = T("match P against E's value,", size=34, t2c={"P": YELLOW, "E": BLUE}).move_to([0, 1.35, 0])
        lab_b = T("bind every variable in P", size=34, t2c={"P": YELLOW}).move_to([0, 0.78, 0])
        demo = Code('let name, number = ("Amy", 21);;', size=40).move_to([0, -0.7, 0])
        for w in ("name", "number"):
            demo.find(w).set_color(YELLOW)
        dreply = Code('val name : string = "Amy"\nval number : int = 21', size=36)
        left_at(dreply, demo.get_left()[0], -2.45)

        with self.say("c3.unzip.4") as c:
            # "What's new is the left-hand side."
            b_half = token_box(row1.find("half"), row1.line(0))
            b_xy = token_box(code.find("xs, ys", line=3), code.line(3), pad=0.12)
            self.play(FadeIn(b_half), run_time=0.7)
            self.play(ReplacementTransform(b_half.copy(), b_xy), run_time=1.2)
            c.wait_until("you write let")
            # "In general, when you write let, a pattern, equals, an expression,"
            sweep_clear(self, *[time_span(FadeIn(g, shift=0.25 * DOWN), 0.5, 1.0) for g in lpe.find("let")],
                        run_time=1.0)
            for cue, sub in (("a pattern", "P"), ("equals", "="), ("an expression", "E")):
                c.wait_until(cue)
                self.play(*fade_each(lpe.find(sub), shift=0.25 * DOWN), run_time=0.6)
            self.add(lpe)
            c.wait_until("OCaml matches")
            # "OCaml matches the pattern against the expression's value,"
            self.play(FadeIn(lab_a, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("and binds every")
            # "and binds every variable in the pattern."
            self.play(FadeIn(lab_b, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("demo")
            # "Let name comma number equal Amy comma twenty-one,"
            anims = fly(lpe.find("let"), demo.find("let")) + fly(lpe.find("="), demo.find("="))
            anims += [TransformFromCopy(lpe.find("P")[0], g) for g in demo.find("name, number")]
            anims += [TransformFromCopy(lpe.find("E")[0], g) for g in demo.find('("Amy", 21)')]
            anims += fade_each(demo.find(";;"))
            self.play(*anims, run_time=1.5)
            self.add(demo)
            self.play(FadeIn(dreply, shift=0.3 * DOWN), run_time=min(1.0, 0.9 * c.until("both")))
            c.wait_until("both")
            # "and OCaml binds both at once."
            nm, amy = demo.find("name"), demo.find('"Amy"')
            nb, n21 = demo.find("number"), demo.find("21")
            a1 = CurvedArrow(nm.get_top() + 0.1 * UP, amy.get_top() + 0.1 * UP, angle=-PI / 4,
                             color=YELLOW, stroke_width=4)
            a2 = CurvedArrow(nb.get_bottom() + 0.1 * DOWN, n21.get_bottom() + 0.1 * DOWN, angle=PI / 4,
                             color=YELLOW, stroke_width=4)
            self.play(Create(a1), Create(a2), run_time=1.3)
            c.wait_until("here")
            # "In unzip, one let catches both results of the recursive call, as exes and whys."
            # the code returns above the example, which stays (same shape: a pattern catching a pair)
            code2 = unzip_code(32)
            code2.shift([-code2.get_center()[0], 3.55 - code2.get_top()[1], 0])
            self.code2 = code2
            sweep_clear(self, time_span(FadeIn(code2, shift=0.2 * DOWN, lag_ratio=0.02), 0.4, 1.4),
                        keep=[demo, dreply, a1, a2], run_time=1.4)
            c.wait_until("one let catches")
            self.play(*dim_lines(code2, (0, 1, 2, 4)),
                      FlashAround(code2.line(3), time_width=1.5, run_time=1.4), run_time=1.4)
            c.wait_until("the recursive call")
            b_e = token_box(code2.find("unzip pairs", line=3), code2.line(3), color=BLUE)
            self.play(FadeIn(b_e), run_time=0.8)
            c.wait_until("as exes")
            b_p = token_box(code2.find("xs, ys", line=3), code2.line(3), color=YELLOW)
            self.play(FadeIn(b_p), run_time=0.8)
        self.leftovers = [demo, dreply, a1, a2, b_e, b_p]

    # ── 5: the down-and-up ladder ────────────────────────────────────────
    def clip_trace(self):
        code2 = self.code2
        calls = [left_at(Code(s, size=LADDER_SIZE), -6.6, y) for s, y in zip(CALLS, LADDER_YS)]
        waits = [right_at(T("waiting", size=30, color=DIM), 6.6, y) for y in LADDER_YS[:3]]
        base = right_at(Code("([], [])", size=LADDER_SIZE), 6.6, LADDER_YS[3]).set_color(TEAL)
        rs = {}
        for key, src, y, nm in ((3, R3_SRC, LADDER_YS[2], ["Cleo"]),
                                (2, R2_SRC, LADDER_YS[1], ["Bob", "Cleo"]),
                                (1, R1_SRC, LADDER_YS[0], ["Amy", "Bob", "Cleo"])):
            r = right_at(Code(src, size=LADDER_SIZE), 6.6, y)
            for n in nm:
                r.find(f'"{n}"').set_color(YELLOW)
            rs[key] = r
        r1, r2, r3 = rs[1], rs[2], rs[3]
        reply = Code(FINAL_REPLY, size=32).move_to([0, 2.95, 0])
        book = calls[0].find("book")

        with self.say("c3.unzip.5") as c:
            # "Let's unzip our phone book."
            tgt = faded_copy(code2, keep_lines=range(5))
            tgt.scale(LADDER_SIZE / 32)
            tgt.shift([-6.6 - tgt.get_left()[0], 3.6 - tgt.get_top()[1], 0])
            code2.target = tgt
            self.play(MoveToTarget(code2), *[FadeOut(m) for m in self.leftovers],
                      time_span(FadeIn(calls[0], shift=0.2 * DOWN), 1.0, 1.8),
                      run_time=min(1.8, c.until("down")))
            c.wait_until("down")
            # "Each call takes off one pair, and leaves work waiting."
            row2_new = rest_of(calls[1], calls[1].find("unzip"))
            self.play(*fly(calls[0].find("unzip"), calls[1].find("unzip")),
                      *[TransformFromCopy(book, g) for g in row2_new],
                      FadeIn(waits[0], shift=0.2 * DOWN), run_time=1.0)
            self.add(calls[1])
            self.play(*fly(calls[1].find("unzip ["), calls[2].find("unzip [")),
                      *fly(calls[1].find('("Cleo", 47)]'), calls[2].find('("Cleo", 47)]')),
                      FadeIn(waits[1], shift=0.2 * DOWN), run_time=0.8)
            self.add(calls[2])
            self.play(*fly(calls[2].find("unzip ["), calls[3].find("unzip [")),
                      *fly(calls[2].find("]"), calls[3].find("]")),
                      FadeIn(waits[2], shift=0.2 * DOWN), run_time=0.7)
            self.add(calls[3])
            c.wait_until("nil")
            # "At the bottom, unzip of nil gives two empty lists."
            self.play(*fly(code2.find("([], [])", line=1), G(base)), run_time=1.5)
            self.add(base)
            c.wait_until("up1")
            # "On the way back, Cleo goes onto the names,"
            self.play(FadeOut(waits[2]),
                      *fly(base.find("(["), r3.find("([", line=0)),
                      *fly(base.find("],"), r3.find("],", line=0)),
                      *fly(calls[2].find('"Cleo"'), r3.find('"Cleo"', line=0)),
                      run_time=1.5)
            c.wait_until("forty-seven onto")
            # "and forty-seven onto the numbers."
            self.play(*fly(base.find("[", nth=1), r3.find("[", line=1)),
                      *fly(calls[2].find("47"), r3.find("47", line=1)),
                      *fly(base.find("])"), r3.find("])", line=1)),
                      run_time=min(1.3, 0.9 * c.until("up2")))
            self.add(r3)
            c.wait_until("up2")
            # "Then Bob and thirty-five,"
            self.play(FadeOut(waits[1]),
                      *fly(r3.find("([", line=0), r2.find("([", line=0)),
                      *fly(r3.find('"Cleo"],', line=0), r2.find('"Cleo"],', line=0)),
                      *fly(calls[1].find('"Bob"'), r2.find('"Bob"', line=0)),
                      *fade_each(r2.find(";", line=0)),
                      *fly(r3.find("[", line=1), r2.find("[", line=1)),
                      *fly(r3.find("47])", line=1), r2.find("47])", line=1)),
                      *fly(calls[1].find("35"), r2.find("35", line=1)),
                      *fade_each(r2.find(";", line=1)),
                      run_time=min(1.2, 0.9 * c.until("up3")))
            self.add(r2)
            c.wait_until("up3")
            # "then Amy and twenty-one."
            self.play(FadeOut(waits[0]),
                      *fly(r2.find("([", line=0), r1.find("([", line=0)),
                      *fly(r2.find('"Bob"; "Cleo"],', line=0), r1.find('"Bob"; "Cleo"],', line=0)),
                      *[TransformFromCopy(book, g) for g in r1.find('"Amy"', line=0)],
                      *fade_each(r1.find(";", line=0)),
                      *fly(r2.find("[", line=1), r1.find("[", line=1)),
                      *fly(r2.find("35; 47])", line=1), r1.find("35; 47])", line=1)),
                      *[TransformFromCopy(book, g) for g in r1.find("21", line=1)],
                      *fade_each(r1.find(";", line=1)),
                      run_time=min(1.0, max(0.5, 0.95 * c.until("result"))))
            self.add(r1)
            c.wait_until("result")
            # "Out come the names, Amy, Bob, Cleo, and the numbers, ..."
            self.play(FadeOut(code2), *fly(G(r1), reply.line(1)), *fade_each(reply.line(0)),
                      run_time=1.3)
            self.add(reply)
            c.wait_until("out come the names")
            box = token_box(reply.find('["Amy"; "Bob"; "Cleo"]', line=1), reply.line(1))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("and the numbers")
            self.play(Transform(box, token_box(reply.find("[21; 35; 47]", line=1), reply.line(1))),
                      run_time=1.0)
