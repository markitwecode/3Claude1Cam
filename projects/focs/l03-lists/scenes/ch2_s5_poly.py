"""Chapter 2, scene 5: the types of null, hd and tl; 'a is a type variable; hd at three
element types (the 'a substitutions, P12); polymorphic; fst : 'a * 'b -> 'a; alpha, beta, gamma.
Clips c2.poly.1 – c2.poly.5.

STATUS: built; tools/check.py clean (109.1 s video vs 105.6 s narration; last clip's gap is
1.2 s so the alpha/beta/gamma row gets its screen time).

Verified replies (ocaml 5.4.1): val null : 'a list -> bool / val hd : 'a list -> 'a /
val tl : 'a list -> 'a list; hd ["cat"; "dog"] -> - : string = "cat"; hd [1; 2; 3] -> - : int = 1;
hd [[1; 2]; [3]] -> - : int list = [1; 2]; fst -> - : 'a * 'b -> 'a = <fun>;
fst (1, "one") -> - : int = 1.

Layout notes: signatures are built as one Code per line (exact baseline), then split into
top-level token parts (copies) so single tokens can be swapped ('a -> string) and the line
re-laid out with one ReplacementTransform per part. "in"/"out" braces sit ABOVE the null row as
column headers (under the hd row they would collide with the tl row).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

GAMMA = "#8FA3EF"            # third type variable ('c), next to PINK 'a and PURPLE 'b
DIM_TO = 0.3                 # spotlight on the 'a: everything else drops to this

ROW_SZ, ROW_BASES = 42, (0.72, -0.43, -1.58)          # clip 1: the three signatures
BIG_SZ, BIG_BASE = 120, -0.85                         # clip 2: one 'a, zoomed
HERO_SZ, HERO_BASE = 42, 2.4                         # clip 3-4: hd's type on top
TAB_SZ, TAB_BASES, TAB_GAP = 36, (0.9, -0.2, -1.3), 1.3
FST_SZ, FST_IN_BASE, FST_BASE = 44, 2.45, 1.45        # clip 5: fst and its type
PAIR_BASE, LAB_SZ, LAB_BASE, ANS_BASE = -0.2, 34, -1.05, -2.35

ROWS = (("val null : 'a list -> bool", ["val", "null", ":", "'a", "list", "->", "bool"]),
        ("val hd   : 'a list -> 'a", ["val", "hd", ":", "'a", "list", "->", "'a"]),
        ("val tl   : 'a list -> 'a list", ["val", "tl", ":", "'a", "list", "->", "'a", "list"]))
CALLS = ('hd ["cat"; "dog"]', "hd [1; 2; 3]", "hd [[1; 2]; [3]]")
REPLIES = ('- : string = "cat"', "- : int = 1", "- : int list = [1; 2]")
ARGS = ('["cat"; "dog"]', "[1; 2; 3]", "[[1; 2]; [3]]")
VALUES = ('"cat"', "1", "[1; 2]")
SLOTS = (3, 6)               # where 'a sits in hd's parts
FSLOTS = (2, 4, 6)           # where 'a, 'b, 'a sit in fst's parts


# ── helpers (local to this scene) ───────────────────────────────────────────────
_METRICS = {}


def metrics(size):
    """(height above the baseline, depth below it) of the tallest/deepest code glyphs."""
    if size not in _METRICS:
        up = Code("'l", size=size).height
        _METRICS[size] = (up, Code("'lg", size=size).height - up)
    return _METRICS[size]


def code_line(src, size, base, x=0.0, left=None, ref=None):
    """Code `src` centred on x (or starting at `left`), with the bottom of `ref` on y=base."""
    c = Code(src, size=size)
    if left is None:
        c.set_x(x)
    else:
        c.shift(RIGHT * (left - c.get_left()[0]))
    c.shift(UP * (base - c.find(ref or src.split()[0]).get_bottom()[1]))
    return c


def split(code, tokens):
    """Copies of the glyphs of each token, in order: separate top-level parts."""
    parts, pos = [], 0
    for tok in tokens:
        i = code.src.index(tok, pos)
        parts.append(code._span(i, i + len(tok)).copy())
        pos = i + len(tok)
    return parts


def piece(src, size, base, x=0.0, ref=None, color=None):
    """A short code token as one plain glyph group (so it transforms glyph for glyph)."""
    g = split(code_line(src, size, base, x=x, ref=ref), [src])[0]
    return g.set_color(color) if color else g


def hl_box(glyphs, base, size, color=YELLOW, pad=0.1, op=0.22):
    """The P8 box behind code glyphs, with a fixed height from the line's baseline."""
    up, down = metrics(size)
    g = VGroup(*glyphs) if isinstance(glyphs, (list, tuple)) else glyphs
    r = Rectangle(width=g.width + 2 * pad + 0.06, height=up + down + 2 * pad,
                  stroke_color=color, stroke_width=2.5).set_fill(color, opacity=op)
    return r.move_to([g.get_x(), base + (up - down) / 2, 0]).set_z_index(-1)


def hero_parts(t):
    """`val hd : t list -> t` as parts, centred, on the hero baseline."""
    c = code_line(f"val hd : {t} list -> {t}", HERO_SZ, HERO_BASE, ref="val")
    p = split(c, ["val", "hd", ":", t, "list", "->", t])
    p[1].set_color(YELLOW)
    return p


def fst_parts(a="'a", b="'b"):
    """OCaml's reply to `fst` (or the same with a, b filled in) as parts."""
    c = code_line(f"- : {a} * {b} -> {a} = <fun>", FST_SZ, FST_BASE, ref=":")
    p = split(c, ["-", ":", a, "*", b, "->", a, "=", "<fun>"])
    if b == "'b":
        p[4].set_color(PURPLE)
    return p


def born_anims(code, flights, shift=0.15 * DOWN):
    """Bring `code` on screen: each (source, substring) flies out of a copy of its source
    while the other glyphs fade in. Returns (anims, done); call done(scene) after the play
    to swap the pieces for the real Code."""
    pieces = [code.find(sub) for _, sub in flights]
    used = {id(g) for p in pieces for g in p}
    others = VGroup(*[g for g in code.text if id(g) not in used])
    anims = [TransformFromCopy(s, p) for (s, _), p in zip(flights, pieces)]
    if len(others):
        anims.append(FadeIn(others, shift=shift))

    def done(scene):
        scene.remove(*pieces, others)
        scene.add(code)
    return anims, done


def cover(center, side=0.84):
    """A closed lid over a cell's value: hd never looks inside, it's just an 'a."""
    sq = RoundedRectangle(corner_radius=0.08, width=side, height=side)
    sq.set_fill("#2A2E36", opacity=1).set_stroke(PINK, 3)
    a = piece("'a", 34, 0, ref="a", color=PINK).move_to(sq)
    return VGroup(sq, a).move_to(center)


class AlphaPolymorphism(NarratedScene):
    def construct(self):
        self.three_types()
        self.what_is_alpha()
        self.use_head()
        self.polymorphic()
        self.two_variables()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # poly.1: the three signatures, in -> out
    def three_types(self):
        left = -Code(ROWS[2][0], size=ROW_SZ).width / 2
        self.rows = []
        for (src, toks), base in zip(ROWS, ROW_BASES):
            parts = split(code_line(src, ROW_SZ, base, left=left, ref="val"), toks)
            parts[1].set_color(YELLOW)
            self.rows.append(parts)
        r0, r1, r2 = self.rows
        top = max(p.get_top()[1] for p in r0)
        b_in = span_brace(np.array([r0[3].get_left()[0], top, 0]),
                          np.array([r0[4].get_right()[0], top, 0]), direction=UP, color=DIM)
        b_out = span_brace(np.array([r2[6].get_left()[0], top, 0]),
                           np.array([r2[7].get_right()[0], top, 0]), direction=UP, color=DIM)
        l_in = T("in", size=40).next_to(b_in, UP, buff=0.12)
        l_out = T("out", size=40).next_to(b_out, UP, buff=0.12)
        self.headers = [b_in, l_in, b_out, l_out]

        with self.say("c2.poly.1") as c:
            anims = []
            for i, row in enumerate(self.rows):
                anims += [time_span(FadeIn(p, shift=0.2 * DOWN), 0.4 * i, 0.4 * i + 1.2) for p in row]
            self.play(*anims, run_time=2.0)

            # one box slides along the voice: what goes in, what comes out, row by row
            c.wait_until("null")
            box = hl_box([r0[3], r0[4]], ROW_BASES[0], ROW_SZ)
            self.play(FadeIn(box), run_time=0.7)
            steps = [("boolean", 0, [r0[6]], 0), ("hd", 0, [r1[3], r1[4]], 1),
                     ("gives", 1, [r1[6]], 1), ("tl", 0, [r2[3], r2[4]], 2),
                     ("another", 0, [r2[6], r2[7]], 2)]
            for cue, nth, glyphs, k in steps:
                c.wait_until(cue, nth=nth)
                self.play(Transform(box, hl_box(glyphs, ROW_BASES[k], ROW_SZ)), run_time=0.8)

            c.wait_until("arrow")
            self.play(FadeOut(box), run_time=0.6)
            c.wait_until("arrow separates")
            t_in = c.at("goes in") - self.time
            t_out = c.at("comes out") - self.time
            self.play(*[time_span(r[5].animate.set_color(YELLOW), 0, 0.8) for r in self.rows],
                      *[time_span(FlashAround(r[5], time_width=1.5), 0, 1.0) for r in self.rows],
                      time_span(GrowFromCenter(b_in), t_in, t_in + 0.7),
                      time_span(FadeIn(l_in, shift=0.2 * DOWN), t_in + 0.1, t_in + 0.7),
                      time_span(GrowFromCenter(b_out), t_out, t_out + 0.7),
                      time_span(FadeIn(l_out, shift=0.2 * DOWN), t_out + 0.1, t_out + 0.7),
                      run_time=t_out + 0.7)

    # poly.2: what is alpha? a type variable = any type
    def what_is_alpha(self):
        r0, r1, r2 = self.rows
        everything = [p for r in self.rows for p in r] + self.headers
        tvars = {id(m) for m in (r0[3], r1[3], r1[6], r2[3], r2[6])}
        P = VGroup(*everything).get_top()
        dy = 3.55 - P[1]

        big = piece("'a", BIG_SZ, BIG_BASE, x=-1.05, ref="a")
        apos = big[0]
        alpha = MathTex(r"\alpha", color=PINK).scale_to_fit_height(big[1].height * 1.05)
        alpha.move_to([1.15, big[1].get_y(), 0])
        line = T("type variable = any type", size=48)
        tv, anyt = VGroup(*line[:12]).set_color(PINK), VGroup(*line[12:])
        line.move_to(DOWN * 2.65)
        q = T("?", size=84, color=GOLD).move_to([tv.get_x(), line.get_y(), 0])
        self.big = [big, alpha, tv, anyt]

        with self.say("c2.poly.2") as c:
            moves = [m.animate.scale(0.8, about_point=P).shift(UP * dy)
                     .set_opacity(1 if id(m) in tvars else DIM_TO) for m in everything]
            self.play(*moves, time_span(TransformFromCopy(r1[3], big), 0.3, 1.6),
                      time_span(FadeIn(q, shift=0.2 * DOWN), 0.9, 1.7), run_time=1.7)
            c.wait_until("tick")
            self.play(FadeIn(alpha, shift=0.3 * LEFT), run_time=0.8)
            c.wait_until("apostrophe")
            self.play(FlashAround(apos, buff=0.14, time_width=1.5), run_time=1.3)
            c.wait_until("apostrophe", nth=1)
            self.play(FlashAround(apos, buff=0.14, time_width=1.5),
                      time_span(FadeTransform(q, tv), 0.3, 1.5), run_time=1.5)
            c.wait_until("stands")
            self.play(FadeIn(anyt, shift=0.3 * DOWN), run_time=1.0)

    def sub_hero(self, t, run_time, extra=()):
        """Fill hd's 'a slots with t (or put 'a back): the line re-lays itself out."""
        new = hero_parts(t)
        anims = [FadeTransform(a, b) if i in SLOTS else ReplacementTransform(a, b)
                 for i, (a, b) in enumerate(zip(self.hero, new))]
        anims += [Transform(box, hl_box(new[i], HERO_BASE, HERO_SZ, color=PINK))
                  for box, i in zip(self.boxes, SLOTS)]
        self.play(*anims, *extra, run_time=run_time)
        self.hero = new

    # poly.3: hd at three element types (P12)
    def use_head(self):
        r0, r1, r2 = self.rows
        big, alpha, tv, anyt = self.big
        self.hero = hero = hero_parts("'a")
        cw = max(Code(s, size=TAB_SZ).width for s in CALLS)
        rw = max(Code(s, size=TAB_SZ).width for s in REPLIES)
        call_left = -(cw + TAB_GAP + rw) / 2
        calls = [code_line(s, TAB_SZ, b, left=call_left, ref="hd") for s, b in zip(CALLS, TAB_BASES)]
        replies = [code_line(s, TAB_SZ, b, left=call_left + cw + TAB_GAP, ref=":")
                   for s, b in zip(REPLIES, TAB_BASES)]
        self.table = calls, replies

        with self.say("c2.poly.3") as c:
            self.play(*[ReplacementTransform(a, b) for a, b in zip(r1, hero)],
                      *[FadeOut(m) for m in r0 + r2 + self.headers], run_time=1.5)
            c.wait_until("strings")
            self.play(*[FadeOut(m) for m in self.big],
                      time_span(FadeIn(calls[0], shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)

            c.wait_until("fill")
            self.boxes = [hl_box(hero[i], HERO_BASE, HERO_SZ, color=PINK) for i in SLOTS]
            self.play(*[GrowFromCenter(b) for b in self.boxes], run_time=0.8)
            c.wait_until("be string")
            self.sub_hero("string", run_time=1.4)

            c.wait_until("takes")
            self.play(FlashUnder(VGroup(self.hero[3], self.hero[4]), time_width=1.5), run_time=1.2)
            c.wait_until("gives")
            self.play(FlashUnder(self.hero[6], time_width=1.5), run_time=1.0)
            c.wait_until("the answer")
            anims, done = born_anims(replies[0], [(self.hero[6], "string"),
                                                  (calls[0].find(VALUES[0]), VALUES[0])])
            self.play(*anims, run_time=1.5)
            done(self)

            # faster: ints, then lists
            for k, t, cue in ((1, "int", "ints"), (2, "int list", "lists")):
                c.wait_until(cue)
                self.play(calls[k - 1].animate.set_opacity(0.45),
                          replies[k - 1].animate.set_opacity(0.45),
                          FadeIn(calls[k], shift=0.2 * DOWN), run_time=0.8)
                c.wait_until("alpha becomes", nth=k - 1)
                new_slot = hero_parts(t)[6]
                flights = [(new_slot, t), (calls[k].find(VALUES[k]), VALUES[k])]
                if k == 1:
                    anims, done = born_anims(replies[k], flights)
                    self.sub_hero(t, run_time=1.4, extra=[time_span(a, 0.5, 1.4) for a in anims])
                    done(self)
                else:
                    self.sub_hero(t, run_time=1.2)
                    c.wait_until("the answer", nth=1)
                    anims, done = born_anims(replies[k], flights)
                    self.play(*anims, run_time=1.5)
                    done(self)

    # poly.4: polymorphic; why hd's type can't care
    def polymorphic(self):
        calls, replies = self.table
        poly = T("polymorphic", size=56, color=YELLOW).move_to(DOWN * 2.35)
        shapes = T("= many shapes", size=38).next_to(poly, DOWN, buff=0.25)

        with self.say("c2.poly.4") as c:
            c.wait_until("polymorphic")
            self.play(FadeIn(poly, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("many shapes")
            self.play(FadeIn(shapes, shift=0.3 * DOWN), run_time=0.9)

            # snap back: still the one function; every kind of list flows into it
            c.wait_until("single")
            self.sub_hero("'a", run_time=1.1,
                          extra=[m.animate.set_opacity(1) for m in calls[:2] + replies[:2]])
            c.wait_until("works on lists")
            slot = VGroup(self.hero[3], self.hero[4])
            flows = [calls[k].find(ARGS[k]).copy() for k in range(3)]
            self.play(*[time_span(f.animate.move_to(slot).scale(0.35).set_opacity(0),
                                  0.35 * k, 0.35 * k + 1.2) for k, f in enumerate(flows)],
                      time_span(FlashAround(slot, color=PINK, time_width=1.5), 1.2, 2.3),
                      run_time=2.3)
            self.remove(*flows)

            # what hd does: hands back the first value, never looks at it
            c.wait_until("think about")
            chain = ConsChain([1, 2, 3]).scale(1.1).move_to(DOWN * 0.55)
            sweep_clear(self, time_span(FadeIn(chain), 0.5, 1.5), keep=self.hero, run_time=1.5)
            c.wait_until("hands back")
            cell0 = chain.cells[0]
            lifted = cell0.label.copy().move_to([self.hero[6].get_x(), 1.3, 0])
            self.play(time_span(FlashAround(cell0.box, time_width=1.5), 0, 1.0),
                      time_span(TransformFromCopy(cell0.label, lifted), 0.4, 1.7), run_time=1.7)
            c.wait_until("without ever")
            lids = [cover(m.label.get_center()) for m in chain.cells] + [cover(lifted.get_center())]
            vals = [m.label for m in chain.cells] + [lifted]
            self.play(*[time_span(FadeIn(lid, scale=0.7), 0.15 * k, 0.15 * k + 0.8)
                        for k, lid in enumerate(lids)],
                      *[time_span(v.animate.set_opacity(0), 0.15 * k + 0.4, 0.15 * k + 0.8)
                        for k, v in enumerate(vals)], run_time=1.25)
            c.wait_until("elements")
            self.play(*flash(lids, color=PINK, time_width=1.5), run_time=1.1)
            c.wait_until("its type")
            self.play(*flash([self.hero[3], self.hero[6]], color=PINK, time_width=1.5), run_time=1.1)

    # poly.5: fst : 'a * 'b -> 'a; Greek letters
    def two_variables(self):
        big_a = piece("'a", 110, -0.4, x=-1.1, ref="a")
        big_b = piece("'b", 110, -0.4, x=1.1, ref="b", color=PURPLE)

        with self.say("c2.poly.5", gap=1.2) as c:
            t_b = c.at("more than") - self.time
            sweep_clear(self, ReplacementTransform(self.hero[6], big_a),
                        time_span(FadeIn(big_b, shift=0.3 * LEFT), t_b, t_b + 0.9),
                        keep=[self.hero[6]], run_time=t_b + 0.9)

            c.wait_until("OCaml's")
            fst_in = code_line("fst", FST_SZ, FST_IN_BASE)
            fst_in.text.set_color(YELLOW)
            parts = fst_parts()
            rest = [p for i, p in enumerate(parts) if i not in FSLOTS]
            self.play(time_span(FadeIn(fst_in, shift=0.2 * DOWN), 0, 0.8),
                      ReplacementTransform(big_a, parts[2]), TransformFromCopy(big_a, parts[6]),
                      ReplacementTransform(big_b, parts[4]),
                      *[time_span(FadeIn(p), 0.6, 1.6) for p in rest], run_time=1.6)
            c.wait_until("takes")
            box = hl_box(parts[2:5], FST_BASE, FST_SZ)
            self.play(FadeIn(box), run_time=0.7)
            c.wait_until("gives back")
            self.play(Transform(box, hl_box([parts[6]], FST_BASE, FST_SZ)), run_time=0.8)

            # the ch1 pair: two parts, two types
            c.wait_until("parts")
            pair = code_line('fst (1, "one")', FST_SZ, PAIR_BASE)
            for ch in "(,)":
                pair.find(ch).set_color(YELLOW)
            self.play(FadeOut(box), FadeIn(pair, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("different types")
            t_int = piece("int", LAB_SZ, LAB_BASE, x=pair.find("1").get_x())
            t_str = piece("string", LAB_SZ, LAB_BASE, x=pair.find('"one"').get_x(), ref="str")
            self.play(FadeIn(t_int, shift=0.25 * DOWN), FadeIn(t_str, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("different variables")
            self.play(FlashAround(parts[2], color=PINK, time_width=1.5),
                      FlashAround(parts[4], color=PURPLE, time_width=1.5), run_time=1.2)
            c.wait_until("alpha and beta")
            filled = fst_parts("int", "string")
            self.play(*[ReplacementTransform(parts[i], filled[i]) for i in range(9) if i not in FSLOTS],
                      *[FadeOut(parts[i], shift=0.25 * UP) for i in FSLOTS],
                      TransformFromCopy(t_int, filled[2]), TransformFromCopy(t_str, filled[4]),
                      TransformFromCopy(t_int, filled[6]), run_time=1.2)
            parts = filled

            c.wait_until("same")
            answer = code_line("- : int = 1", FST_SZ, ANS_BASE, ref=":")
            anims, done = born_anims(answer, [(parts[6], "int"), (pair.find("1"), "1")])
            self.play(*anims, run_time=1.3)
            done(self)
            c.wait_until("first part", nth=1)
            self.play(*flash([parts[2], parts[6], answer.find("int")], color=GREEN, time_width=1.5),
                      run_time=1.2)

            # 'a 'b 'c ... read alpha, beta, gamma; the worked pair stays below, dimmed
            c.wait_until("general")
            xs = (-2.7, 0.0, 2.7)
            row = [piece(f"'{l}", 100, 1.55, x=x, ref=l, color=col)
                   for l, x, col in zip("abc", xs, (PINK, PURPLE, GAMMA))]
            dots = MathTex(r"\cdots", color=DIM, font_size=90).move_to([4.6, row[0][1].get_y(), 0])
            greek = MathTex(r"\alpha", r"\beta", r"\gamma", arg_separator=r"\quad ", font_size=120)
            greek.move_to(DOWN * 0.15)
            for g, x, col in zip(greek, xs, (PINK, PURPLE, GAMMA)):
                g.set_x(x).set_color(col)
            pw = pair.width
            left = -(pw + 1.3 + answer.width) / 2
            low = -2.75
            self.play(*[FadeOut(m) for m in [fst_in, t_int, t_str] + parts],
                      pair.animate.shift([left - pair.get_left()[0], low - PAIR_BASE, 0]).set_opacity(0.4),
                      answer.animate.shift([left + pw + 1.3 - answer.get_left()[0], low - ANS_BASE, 0])
                      .set_opacity(0.4),
                      *[time_span(FadeIn(m, shift=0.3 * DOWN), 0.3 + 0.15 * k, 0.9 + 0.15 * k)
                        for k, m in enumerate(row + [dots])], run_time=1.4)
            c.wait_until("these variables")
            self.play(*[time_span(FadeIn(g, shift=0.3 * DOWN), 0.15 * k, 0.15 * k + 0.7)
                        for k, g in enumerate(greek)], run_time=1.0)
            c.wait_until("letters")
            spans = [max(0.0, c.at(w, nth=n) - self.time) for w, n in (("alpha", 3), ("beta", 2), ("gamma", 0))]
            self.play(*[time_span(FlashAround(g, color=col, time_width=1.5, buff=0.15), s, s + 0.9)
                        for g, s, col in zip(greek, spans, (PINK, PURPLE, GAMMA))],
                      run_time=spans[-1] + 0.9)
