"""Chapter 3, scene 2: zip, its two clauses, the wildcard, and its type. Clips c3.zip.1 – c3.zip.3.

Layout: the four-line zip Code is the hero (size 38, centred a little above the middle) for
clips 1-2. One highlight box walks pattern -> (x, y) -> zip xs ys -> _. While the first clause is
annotated (head / tail labels, "new names"), line 3 slides down to open a gap under line 2 and
slides back at {wild}. Clip 3: the code restyles to size 32 at the top (original colours), the
reply sits under it as separate token parts (L3's substitution move: 'a -> string, 'b -> int,
re-laid out without `val zip :` / `= <fun>` so it fits), then snaps back. The last shot is the
code alone at TOP_C, size 32, which ch3_s3 fades back in.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = ("let rec zip xs ys =\n"
       "  match xs, ys with\n"
       "  | (x::xs, y::ys) -> (x, y) :: zip xs ys\n"
       "  | _ -> []")
HERO_SZ, HERO_C = 38, 0.15 * UP      # clips 1-2
TOP_SZ, TOP_C = 32, 2.3 * UP        # clip 3 and the hand-off to s3
REPLY_SZ, REPLY_BASE = 28, 0.3      # reply baseline (bottom of its first `list`)
LAB = 34
A_SLOTS, B_SLOTS = (3, 10), (6, 12)  # where 'a / 'b sit in the 17 reply parts
EXTRAS = (0, 1, 2, 15, 16)           # `val zip :` and `= <fun>`
INSET_C = 2.05 * DOWN


def make_code(size, center):
    c = Code(SRC, size=size).move_to(center)
    c.find("zip", line=2).set_color(YELLOW)      # the recursive call: function name too
    return c


def split(code, tokens):
    """Copies of the glyphs of each token, in order: separate top-level parts."""
    parts, pos = [], 0
    for tok in tokens:
        i = code.src.index(tok, pos)
        parts.append(code._span(i, i + len(tok)).copy())
        pos = i + len(tok)
    return parts


def reply_parts(a="'a", b="'b", full=True):
    """OCaml's reply to zip (or the type with a, b filled in) as 17 parts. full=False centres
    just the type (the extras are built but meant to stay off screen)."""
    toks = ["val", "zip", ":", a, "list", "->", b, "list", "->", "(", a, "*", b, ")", "list",
            "=", "<fun>"]
    c = Code(f"val zip : {a} list -> {b} list -> ({a} * {b}) list = <fun>", size=REPLY_SZ)
    p = split(c, toks)
    ref = VGroup(*[m.copy() for m in (p if full else p[3:15])])
    dx = -ref.get_x()
    dy = REPLY_BASE - p[4].get_bottom()[1]
    for m in p:
        m.shift([dx, dy, 0])
    for k in range(3, 15):
        p[k].set_color(GREEN)
    p[1].set_color(YELLOW)
    if a == "'a":
        for k in A_SLOTS:
            p[k].set_color(PINK)
    if b == "'b":
        for k in B_SLOTS:
            p[k].set_color(PURPLE)
    return p


def fst_inset():
    q = Code("fst", size=REPLY_SZ)
    q.set_color(YELLOW)
    r = Code("- : 'a * 'b -> 'a = <fun>", size=REPLY_SZ)
    r.find("'a * 'b -> 'a").set_color(GREEN)
    r.find("'a", nth=0).set_color(PINK)
    r.find("'a", nth=1).set_color(PINK)
    r.find("'b").set_color(PURPLE)
    body = VGroup(q, r).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    frame = SurroundingRectangle(body, buff=0.3, corner_radius=0.12).set_stroke(DIM, 2)
    body.set_opacity(0.7)
    return VGroup(frame, body).move_to(INSET_C)


def under(mob, label, top, buff=0.0):
    """Put `label` centred under mob's x with its top at y=top."""
    return label.move_to([mob.get_x(), top - label.height / 2 - buff, 0])


class Zip(NarratedScene):
    def go(self, c, anims, cap, nxt=None, frac=0.85):
        t = cap if nxt is None else min(cap, max(0.5, frac * c.until(nxt)))
        self.play(*anims, run_time=t)

    def construct(self):
        code = self.code = make_code(HERO_SZ, HERO_C)
        L2, L3 = code.line(2), code.line(3)          # live geometry of lines 2 and 3
        m1 = code.find("match xs, ys with", line=1)
        pat = code.find("(x::xs, y::ys)", line=2)
        lx, ly = code.find("x::xs", line=2), code.find("y::ys", line=2)
        px, py = lx[0], ly[0]
        tails = [lx[3], lx[4], ly[3], ly[4]]
        rhs = code.find("(x, y)", line=2)
        rx, ry = rhs[1], rhs[3]
        call = code.find("zip xs ys", line=2)
        call_tails = list(call)[3:7]
        us = code.find("_", line=3)[0]
        nil = code.find("[]", line=3)

        # `_` <-> `p`: the p glyph from the same code with p written, aligned glyph for glyph
        alt = Code(SRC.replace("| _", "| p"), size=HERO_SZ)
        alt.shift(code.find("let")[0].get_center() - alt.find("let")[0].get_center())
        p_glyph = alt.find("p", line=3)[0].copy().set_color(FG)
        us_back = us.copy().set_color(YELLOW)

        # annotations under line 2 (in the gap line 3 opens)
        row = L2.get_bottom()[1] - 0.16
        head_x = under(px, T("head", LAB, YELLOW), row)
        head_y = under(py, T("head", LAB, YELLOW), row)
        tail_x = under(VGroup(lx[3], lx[4]), T("tail", LAB, TEAL), row)
        tail_y = under(VGroup(ly[3], ly[4]), T("tail", LAB, TEAL), row)
        tag = under(pat, T("new names", LAB, DIM), head_x.get_bottom()[1] - 0.18)
        drop = L3.get_top()[1] - (tag.get_bottom()[1] - 0.3)
        small = under(call, T("the smaller problem", LAB, YELLOW), row)
        if small.get_right()[0] > 6.5:
            small.shift(LEFT * (small.get_right()[0] - 6.5))
        pair_lab = T("a pair, as in append", LAB, t2c={"append": YELLOW}).next_to(m1, RIGHT, buff=0.9)

        # ── c3.zip.1: the code; the pair match; the first pattern ──────────────────────
        with self.say("c3.zip.1") as c:
            self.go(c, [Write(code)], 1.6, "two lists")
            c.wait_until("two lists")
            self.go(c, [FlashUnder(code.find("xs", line=0), color=YELLOW, time_width=1.5),
                        FlashUnder(code.find("ys", line=0), color=YELLOW, time_width=1.5)],
                    1.5, "match")
            c.wait_until("match")
            self.go(c, [FlashUnder(m1, color=YELLOW, time_width=1.5),
                        FadeIn(pair_lab, shift=0.3 * LEFT)], 1.5, "each pattern")
            c.wait_until("each pattern")
            self.go(c, [FlashUnder(lx, color=YELLOW, time_width=1.5),
                        FlashUnder(ly, color=YELLOW, time_width=1.5)], 1.5, "first")
            c.wait_until("first")
            box = token_box(pat, L2)
            self.go(c, [FadeOut(pair_lab), FadeIn(box),
                        *[g.animate.shift(DOWN * drop) for g in L3]], 1.2, "ex on one side")
            c.wait_until("ex on one side")
            self.go(c, [FadeIn(head_x, shift=0.25 * UP), px.animate.set_color(YELLOW)],
                    1.0, "why on the other")
            c.wait_until("why on the other")
            self.go(c, [FadeIn(head_y, shift=0.25 * UP), py.animate.set_color(YELLOW)],
                    1.0, "fresh")
            c.wait_until("exes and whys", nth=1)
            self.go(c, [*recolor(tails, TEAL), FadeIn(tail_x, shift=0.25 * UP),
                        FadeIn(tail_y, shift=0.25 * UP)], 1.2, "new names")
            c.wait_until("new names")
            self.go(c, [FadeIn(tag, shift=0.25 * UP)], 1.0)

        # ── c3.zip.2: the answer; the wildcard; _ vs a variable ─────────────────────────
        wild_lab = T("wildcard: matches anything", LAB, t2c={"wildcard": YELLOW})
        ign_lab = T("this clause ignores its argument", LAB)
        check = check_mark()
        with self.say("c3.zip.2") as c:
            self.go(c, [Transform(box, token_box(rhs, L2))], 1.0, "ex comma why")
            c.wait_until("ex comma why")
            rx.set_color(YELLOW)
            ry.set_color(YELLOW)
            self.go(c, [TransformFromCopy(px, rx, path_arc=-PI / 4),
                        TransformFromCopy(py, ry, path_arc=-PI / 4)], 1.6, "consed onto")
            c.wait_until("consed onto")
            self.go(c, [Transform(box, token_box(call, L2)), *recolor(call_tails, TEAL),
                        FadeIn(small, shift=0.25 * UP)], 1.3, "wild")
            c.wait_until("wild")
            us_box = token_box([us], L3).shift(UP * drop)
            self.go(c, [FadeOut(head_x, head_y, tail_x, tail_y, tag),
                        *[g.animate.shift(UP * drop) for g in L3],
                        Transform(box, us_box)], 1.4, "single underscore")
            c.wait_until("single underscore")
            self.go(c, [us.animate.set_color(YELLOW),
                        FlashAround(us, color=YELLOW, time_width=1.5, buff=0.16)],
                    1.3, "called the wildcard")
            c.wait_until("called the wildcard")
            wild_lab.next_to(L3, RIGHT, buff=0.9)
            ign_lab.next_to(L3, RIGHT, buff=0.9)
            check.next_to(L3, RIGHT, buff=0.9)
            self.go(c, [FadeOut(small), FadeIn(wild_lab, shift=0.3 * LEFT)], 1.0)
            c.wait_until("the answer is nil")
            self.go(c, [FlashAround(nil, color=TEAL, time_width=1.5, buff=0.14)], 1.5, "var")
            c.wait_until("var")
            self.go(c, [Transform(us, p_glyph), *set_alpha([wild_lab], 0.35)], 1.3, "just the same")
            c.wait_until("just the same")
            self.go(c, [FadeOut(wild_lab), FadeIn(check, scale=0.5)], 0.9, "ignore")
            c.wait_until("ignore")
            self.go(c, [Transform(us, us_back), FadeOut(check),
                        time_span(FadeIn(ign_lab, shift=0.3 * LEFT), 0.5, 1.4)], 1.4)

        # ── c3.zip.3: OCaml's reply; two type variables; string and int ────────────────
        parts = reply_parts()
        inset = fst_inset()
        b1 = span_brace(parts[3].get_left(), parts[7].get_right())
        b2 = span_brace(parts[9].get_left(), parts[14].get_right())
        bl1 = T("two lists", LAB).next_to(b1, DOWN, buff=0.12)
        bl2 = T("a list of pairs", LAB).next_to(b2, DOWN, buff=0.12)
        names = VGroup(T("names", 32), Mono("string", 36, GREEN)).arrange(DOWN, buff=0.2)
        nums = VGroup(T("numbers", 32), Mono("int", 36, GREEN)).arrange(DOWN, buff=0.2)
        names.move_to([-2.4, -1.25, 0])
        nums.move_to([2.4, -1.25, 0])
        nums[0].align_to(names[0], DOWN)          # labels share a baseline
        nums[1].align_to(names[1], UP)            # string / int share their top
        with self.say("c3.zip.3") as c:
            self.play(FadeOut(box), time_span(FadeOut(ign_lab), 0.2, 1.0), Transform(code, make_code(TOP_SZ, TOP_C)),
                      *[time_span(FadeIn(p, shift=0.2 * DOWN), 0.7 + 0.03 * k, 1.3 + 0.03 * k)
                        for k, p in enumerate(parts)],
                      run_time=min(1.9, max(1.0, 0.9 * c.until("args"))))
            c.wait_until("args")
            self.go(c, [GrowFromCenter(b1), FadeIn(bl1, shift=0.25 * UP)], 1.0, "out")
            c.wait_until("out")
            self.go(c, [GrowFromCenter(b2), FadeIn(bl2, shift=0.25 * UP)], 1.0, "two")
            c.wait_until("two type variables")
            self.go(c, [*flash([parts[k] for k in A_SLOTS], color=PINK, time_width=1.5),
                        *flash([parts[k] for k in B_SLOTS], color=PURPLE, time_width=1.5)],
                    1.3, "just as")
            c.wait_until("just as")
            self.go(c, [FadeIn(inset, shift=0.3 * UP)], 1.0, "different types")
            c.wait_until("different types")
            self.go(c, [FlashUnder(VGroup(parts[3], parts[4]), color=PINK, time_width=1.5),
                        FlashUnder(VGroup(parts[6], parts[7]), color=PURPLE, time_width=1.5)],
                    1.5, "fill")
            c.wait_until("fill")
            # just the type, centred: room for string and int
            core = reply_parts(full=False)
            self.go(c, [FadeOut(b1, bl1, b2, bl2, inset),
                        *[FadeOut(parts[k]) for k in EXTRAS],
                        *[ReplacementTransform(parts[k], core[k]) for k in range(3, 15)]],
                    1.2, "strings")
            cur = core
            c.wait_until("strings")
            self.go(c, [FadeIn(names, shift=0.25 * UP)], 0.8, "ints")
            c.wait_until("ints")
            self.go(c, [FadeIn(nums, shift=0.25 * UP)], 0.8, "alpha is string")
            for cue, ty, slots, nxt in (("alpha is string", ("string", "'b"), A_SLOTS, "beta is int"),
                                        ("beta is int", ("string", "int"), B_SLOTS, None)):
                c.wait_until(cue)
                new = reply_parts(*ty, full=False)
                src = names[1] if slots == A_SLOTS else nums[1]
                anims = [ReplacementTransform(cur[k], new[k]) for k in range(3, 15)
                         if k not in slots]
                anims += [FadeOut(cur[k]) for k in slots]
                anims += [TransformFromCopy(src, new[k]) for k in slots]
                self.go(c, anims, 1.2, nxt) if nxt else self.play(*anims, run_time=1.1)
                cur = new

        # the type snaps back; then the code alone (s3 opens on it), then empty
        full = reply_parts()
        self.play(*[ReplacementTransform(cur[k], full[k]) for k in range(3, 15)
                    if k not in A_SLOTS + B_SLOTS],
                  *[FadeTransform(cur[k], full[k]) for k in A_SLOTS + B_SLOTS],
                  *[FadeIn(full[k]) for k in EXTRAS],
                  FadeOut(names, nums), run_time=0.9)
        self.wait(0.25)
        self.play(*[FadeOut(p) for p in full], run_time=0.6)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.15)
