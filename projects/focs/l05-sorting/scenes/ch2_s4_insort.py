"""Chapter 2, scene 4: sorting by inserting, `insort`. Clips c2.insort.1 – c2.insort.5.

Plan: s2's `ins` code fades back in where s2 left it ((0, 2.65), scale 0.78) and shrinks to the
top-left corner (reference, every `ins` YELLOW) → `insort` hero (Code 40, centre) → one YELLOW box
walks [] -> [] / x::xs / insort xs / ins x (insort xs) → type reply → {trace}: insort code to the
top-right corner (the two functions side by side as the reference band), input chain 3 5 9 4 7
under it, `insort [3; 5; 9; 4; 7]` unfolds stage by stage (each `ins k` born from its cell) →
YELLOW waiting inserts under a brace, DIM inset of L3's 1 + (1 + (1 + 0)) → `ins 7 []` boxed,
the nest moves up where the input chain was → five inserts, inside out: the item is born from
its `k` in the nest beside the sorted chain, lifts 0.4 (s1's card motion), glides over the
cells it compares with (GOLD flash each), and drops into its gap while its neighbours part; the
nest collapses one level, a GOLD count lands in a row at the bottom → reply + GREEN tick →
counts gather into 0 + 1 + 2 + 2 + 1 = 6; GOLD 7 "worst input, any comparison sort", the 6
GREEN just under it → DIM caption (the notes' line) → strings example under it.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

INS_SRC = """let rec ins x = function
  | [] -> [x]
  | y::ys -> if x <= y then x :: y :: ys
             else y :: ins x ys"""
INSORT_SRC = """let rec insort = function
  | [] -> []
  | x::xs -> ins x (insort xs)"""
TYPE_SRC = "val insort : 'a list -> 'a list = <fun>"

REF_W = 6.0            # width of the top-left `ins` reference
CODE_Y = -0.1          # insort hero
TOP = 0.7              # insort scale once it joins the reference band (top-right): size 28
NSIZE = 36             # the nest expression
NEST_Y0, NEST_Y1 = -0.6, 1.3   # y of the nest's "3" glyph: during the unfold / the inserts
IN_Y = 1.0             # input chain
S = 0.85               # chain scale
PITCH = 2.3 * S
YC = -1.0              # sorted chain row
HOVER = 0.9            # where a new item is born, above the row
LIFT = 0.4             # s1's card lift
SLOT_X = [-4.4, -2.2, 0.0, 2.2, 4.4]
LAB_Y, NUM_Y = -2.35, -2.95


# ---------------------------------------------------------------- code helpers
def ocode(src, size=36):
    """s2's look: Code with every `ins` YELLOW."""
    c = Code(src, size=size)
    k = 0
    while True:
        try:
            g = c.find("ins", nth=k)
        except ValueError:
            break
        g.set_color(YELLOW)
        k += 1
    return c


def insort_code():
    c = Code(INSORT_SRC, size=40)
    for nth in (0, 1):
        c.find("insort", nth=nth).set_color(YELLOW)
    c.find("ins x")[:3].set_color(YELLOW)
    return c


def gidx(src, i):
    return i - sum(1 for ch in src[:i] if ch.isspace())


def gl(code, i, j=None):
    """Glyphs of chars [i, j) of a one-line Code (spaces have none)."""
    s = code.src
    j = i + 1 if j is None else j
    return [code.text[gidx(s, t)] for t in range(i, j) if not s[t].isspace()]


def gsub(code, sub, nth=0):
    s, i = code.src, -1
    for _ in range(nth + 1):
        i = s.index(sub, i + 1)
    return gl(code, i, i + len(sub))


def place(code, y3):
    """Centre on x = 0 with the first "3" glyph at height y3 (keeps the baseline steady)."""
    code.move_to([0, y3, 0])
    g = gl(code, code.src.index("3"))[0]
    code.shift((y3 - g.get_center()[1]) * UP)
    return code


def inner_glyphs(code, k):
    s = code.src
    a = s.index(f"ins {k} ")
    return VGroup(*gl(code, a, s.index("]", a) + 1))


def list_glyphs(code):
    s = code.src
    a = s.index("[")
    return VGroup(*gl(code, a, s.index("]", a) + 1))


def lst(L):
    return "[" + "; ".join(map(str, L)) + "]"


def s_str(outer, rest):
    s = "insort " + lst(rest)
    for k in reversed(outer):
        s = f"ins {k} ({s})"
    return s


def n_str(ks, L):
    if not ks:
        return lst(L)
    s = f"ins {ks[-1]} {lst(L)}"
    for k in reversed(ks[:-1]):
        s = f"ins {k} ({s})"
    return s


def morph(old, new, pairs=(), gone=(), born=(), grown=()):
    """Glyph-level rewrite of one-line code `old` into `new`: pairs move, gone fade out, born
    fade in, grown = (source mobject, new char indices) born by TransformFromCopy."""
    o = old.src if old is not None else ""
    n = new.src
    anims, wrappers, used_o, used_n = [], [], set(), set()
    for a, b in pairs:
        if o[a].isspace():
            continue
        assert o[a] == n[b], (o, a, n, b)
        anims.append(ReplacementTransform(gl(old, a)[0], gl(new, b)[0]))
        used_o.add(a)
        used_n.add(b)
    for a in gone:
        anims += [FadeOut(g) for g in gl(old, a)]
        used_o.add(a)
    for b in born:
        anims += [FadeIn(g) for g in gl(new, b)]
        used_n.add(b)
    for src, idxs in grown:
        tgt = VGroup(*[g for b in idxs for g in gl(new, b)])
        anims.append(TransformFromCopy(src, tgt))
        wrappers.append(tgt)
        used_n.update(idxs)
    miss_o = [i for i, ch in enumerate(o) if not ch.isspace() and i not in used_o]
    miss_n = [i for i, ch in enumerate(n) if not ch.isspace() and i not in used_n]
    assert not miss_o and not miss_n, (o, miss_o, n, miss_n)
    return anims, wrappers


def unfold_map(o, n, k):
    """P + insort [k; rest] + Q  ->  P + ins k (insort [rest]) + Q"""
    a, b = o.index("insort ["), n.index("insort [")
    P, Q = o[:a], o[o.index("]", a) + 1:]
    pairs = [(t, t) for t in range(len(P))]
    pairs += [(a + t, b + t) for t in range(8)]
    ra = a + 8 + len(f"{k}; ")
    rlen = o.index("]", a) + 1 - ra
    pairs += [(ra + t, b + 8 + t) for t in range(rlen)]
    pairs += [(len(o) - len(Q) + t, len(n) - len(Q) + t) for t in range(len(Q))]
    gone = [a + 8, a + 9]
    born = [b - 1, len(n) - len(Q) - 1]
    grown = list(range(len(P), len(P) + 5))
    return pairs, gone, born, grown


def unfold_last(o, n):
    """P + insort [4; 7] + Q  ->  P + ins 4 (ins 7 []) + Q"""
    a = o.index("insort [")
    rb = o.index("]", a)
    P, Q = o[:a], o[rb + 1:]
    nb = n.index("[]")
    pairs = [(t, t) for t in range(len(P))]
    pairs += [(a + 7, nb), (rb, nb + 1)]
    pairs += [(len(o) - len(Q) + t, len(n) - len(Q) + t) for t in range(len(Q))]
    gone = list(range(a, a + 6)) + list(range(a + 8, rb))
    born = [len(P) + 6, len(n) - len(Q) - 1]
    g4 = list(range(len(P), len(P) + 5))
    g7 = list(range(len(P) + 7, len(P) + 12))
    return pairs, gone, born, g4, g7


def collapse_map(o, n, k):
    """... (ins k [L]) ...  ->  ... [L'] ...  (k slides into the list)."""
    s = o.index(f"ins {k} ")
    lb = s + 6
    rb = o.index("]", lb)
    paren = s > 0
    P = o[:s - 1] if paren else ""
    Q = o[rb + 2:] if paren else ""
    nlb = len(P)
    nrb = n.index("]", nlb)
    pairs = [(t, t) for t in range(len(P))]
    pairs += [(lb, nlb), (rb, nrb), (s + 4, n.index(str(k), nlb))]
    for t in range(lb + 1, rb):
        if o[t].isdigit():
            pairs.append((t, n.index(o[t], nlb)))
    used = set()
    for t in range(lb, rb):
        if o[t] == ";":
            u = n.index(o[t - 1] + ";", nlb) + 1
            pairs.append((t, u))
            used.add(u)
    born = [t for t in range(nlb, nrb) if n[t] == ";" and t not in used]
    gone = [s, s + 1, s + 2] + ([s - 1, rb + 1] if paren else [])
    pairs += [(len(o) - len(Q) + t, len(n) - len(Q) + t) for t in range(len(Q))]
    return pairs, gone, born


def glide_drop(start, end, alpha):
    """Path for a lifted item: across first, then straight down into its slot."""
    ax = smooth(min(1.0, alpha / 0.75))
    ay = smooth(max(0.0, (alpha - 0.45) / 0.55))
    out = start.copy()
    out[:, 0] = start[:, 0] + (end[:, 0] - start[:, 0]) * ax
    out[:, 1] = start[:, 1] + (end[:, 1] - start[:, 1]) * ay
    out[:, 2] = start[:, 2] + (end[:, 2] - start[:, 2]) * alpha
    return out


def inv_smooth(f):
    xs = np.linspace(0, 1, 401)
    return float(xs[np.argmin(np.abs(np.array([smooth(x) for x in xs]) - f))])


class SortingByInserting(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(1.2)   # let the strings reply sit before the scene ends
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def finish(self, old, new, wrappers=()):
        if old is not None:
            self.remove(*old.get_family())
        for w in wrappers:
            self.remove(w)
        self.remove(*new.get_family())
        self.add(new)

    # ------------------------------------------------------------ c2.insort.1
    def clip1(self):
        with self.say("c2.insort.1") as c:
            ins = self.ins = ocode(INS_SRC).scale(0.78).move_to([0, 2.65, 0])
            self.play(FadeIn(ins, shift=0.2 * DOWN), run_time=0.8)

            c.wait_until("the sort itself")
            code = self.code = insort_code().move_to([0, CODE_Y, 0])
            self.play(ins.animate.scale_to_fit_width(REF_W).to_corner(UL, buff=0.4),
                      time_span(FadeIn(code, shift=0.2 * UP), 0.5, 1.6), run_time=1.6)

            c.wait_until("call it")
            self.play(FlashUnder(code.find("insort", line=0), time_width=1.5), run_time=1.2)

            c.wait_until("nil")
            box = token_box(code.find("[] -> []"), code.line(1))
            self.play(FadeIn(box), run_time=0.7)

            c.wait_until("cons")
            self.play(Transform(box, token_box(code.find("x::xs"), code.line(2))), run_time=0.9)

            c.wait_until("sorttail")
            self.play(Transform(box, token_box(code.find("insort xs"), code.line(2))),
                      run_time=min(0.9, 0.8 * c.until("insert")))

            c.wait_until("insert")
            self.play(Transform(box, token_box(code.find("ins x (insort xs)"), code.line(2))),
                      FlashAround(ins.find("ins", line=0), time_width=1.5), run_time=1.2)

            c.wait_until("type")
            reply = self.reply = Code(TYPE_SRC, size=32).next_to(code, DOWN, buff=0.85)
            reply.find("insort").set_color(YELLOW)
            self.play(FadeOut(box), FadeIn(reply, shift=0.2 * UP), run_time=1.0)

            c.wait_until("takes an alpha list")
            self.play(FlashUnder(reply.find("'a list"), time_width=1.5), run_time=1.0)
            c.wait_until("returns an alpha list")
            self.play(FlashUnder(reply.find("'a list", nth=1), time_width=1.5), run_time=1.0)

    # ------------------------------------------------------------ c2.insort.2
    def clip2(self):
        with self.say("c2.insort.2") as c:
            code = self.code
            self.play(code.animate.scale(TOP).to_corner(UR, buff=0.4), run_time=1.2)

            chain = ConsChain([3, 5, 9, 4, 7]).scale(S).move_to([0, IN_Y, 0])
            cell_of = {v: chain.cells[i] for i, v in enumerate([3, 5, 9, 4, 7])}
            stages = [s_str([], [3, 5, 9, 4, 7]), s_str([3], [5, 9, 4, 7]),
                      s_str([3, 5], [9, 4, 7]), s_str([3, 5, 9], [4, 7]),
                      n_str([3, 5, 9, 4, 7], [])]
            codes = [place(Code(s, size=NSIZE), NEST_Y0) for s in stages]
            for cd in codes:
                if "insort" in cd.src:
                    VGroup(*gsub(cd, "insort")).set_color(YELLOW)

            c.wait_until("three")
            self.play(FadeIn(chain, lag_ratio=0.1),
                      time_span(FadeIn(codes[0], shift=0.2 * DOWN), 1.0, 1.8), run_time=1.8)

            # {unfold}: each insort [k; rest] becomes ins k (insort [rest])
            nest = codes[0]
            plan = [("unfold", "for the five", 2.0), ("for the five", "the nine", 1.1),
                    ("the nine", "the four", 0.9)]
            for i, (cue, nxt, rt) in enumerate(plan):
                c.wait_until(cue)
                k = [3, 5, 9][i]
                new = codes[i + 1]
                pairs, gone, born, grown = unfold_map(nest.src, new.src, k)
                anims, wr = morph(nest, new, pairs, gone, born, [(cell_of[k].label, grown)])
                if i == 0:
                    anims.append(FadeOut(self.reply))
                self.play(*anims, run_time=min(rt, max(0.5, 0.85 * c.until(nxt))))
                self.finish(nest, new, wr)
                nest = new

            c.wait_until("the four")
            new = codes[4]
            pairs, gone, born, g4, g7 = unfold_last(nest.src, new.src)
            anims, wr = morph(nest, new, pairs, gone, born,
                              [(cell_of[4].label, g4), (cell_of[7].label, g7)])
            self.play(*anims, run_time=min(1.2, max(0.8, c.until("nlength") - 1.3)))
            self.finish(nest, new, wr)
            nest = self.nest = new

            # {wait}: the four waiting inserts
            c.wait_until("wait")
            waiting = [g for k in (3, 5, 9, 4) for g in gsub(nest, f"ins {k}")]
            yb = nest.get_bottom()[1]
            brace = span_brace([gsub(nest, "ins 3")[0].get_left()[0], yb, 0],
                               [gsub(nest, "ins 4")[-1].get_right()[0], yb, 0], DOWN)
            wlab = T("waiting", size=32, color=YELLOW).next_to(brace, DOWN, buff=0.15)
            self.play(*recolor(waiting, YELLOW), GrowFromCenter(brace),
                      time_span(FadeIn(wlab, shift=0.2 * UP), 0.4, 1.2), run_time=1.2)

            # {nlength}: L3's length, waiting the same way
            c.wait_until("nlength")
            tag = T("length, Lecture 3", size=28, color=DIM)
            ones = Mono("1 + (1 + (1 + 0))", size=30, color=DIM)
            body = VGroup(tag, ones).arrange(DOWN, buff=0.2)
            frame = RoundedRectangle(corner_radius=0.15, width=body.width + 0.6,
                                     height=body.height + 0.45).set_stroke(DIM, 2)
            inset = VGroup(frame, body).move_to([3.7, -2.5, 0])
            self.play(FadeIn(inset, shift=0.2 * UP), run_time=1.0)

            # {first}: the innermost insert runs first
            c.wait_until("first")
            box = self.box = token_box(VGroup(*gsub(nest, "ins 7 []")), nest)
            self.play(FadeIn(box), run_time=1.0)

            c.wait_until("last item")
            self.play(FlashAround(chain.cells[4], time_width=1.5), run_time=1.3)

            c.wait_until("goes in first")
            d = (NEST_Y1 - NEST_Y0) * UP
            self.play(FadeOut(chain), FadeOut(brace), FadeOut(wlab), FadeOut(inset),
                      nest.animate.shift(d), box.animate.shift(d),
                      run_time=min(1.3, max(0.6, c.until() - 0.05)))

    # ------------------------------------------------------------ c2.insort.3
    def clip3(self):
        steps = [   # k, new list, slot j, indices of the cells it is compared with
            (7, [7], 0, []),
            (4, [4, 7], 0, [0]),
            (9, [4, 7, 9], 2, [0, 1]),
            (5, [4, 5, 7, 9], 1, [0, 1]),
            (3, [3, 4, 5, 7, 9], 0, [0]),
        ]
        outer_after = [[3, 5, 9, 4], [3, 5, 9], [3, 5], [3], []]
        counts = [0, 1, 2, 2, 1]
        cues = ["r1", "r2", "r3", "r4", "r5", "result"]
        nest, box = self.nest, self.box
        nil = Nil().scale(S).move_to([0, YC, 0])
        cells, arrows = [], []
        self.nums, self.labs = [], []

        with self.say("c2.insort.3") as c:
            for i, (k, Lnew, j, cmp) in enumerate(steps):
                c.wait_until(cues[i])
                W = c.until(cues[i + 1])
                tb, tg, td = min(0.9, 0.2 * W), min(0.5 + 0.35 * len(cmp), 0.2 * W), min(1.3, 0.28 * W)

                # born from its k in the nest, beside the chain
                first = cells[0] if cells else nil
                pb = np.array([first.get_x() - PITCH, YC + HOVER, 0])
                X = ConsCell(k, color=YELLOW).scale(S).move_to(pb)
                kg = gsub(nest, f"ins {k}")[-1]
                birth = [TransformFromCopy(kg, X)]
                if i == 0:
                    birth.append(TransformFromCopy(VGroup(*gsub(nest, "[]")), nil))
                else:
                    birth.append(Transform(box, token_box(inner_glyphs(nest, k), nest)))
                self.play(*birth, run_time=tb)
                self.wait(0.15)

                # lifts 0.4 and glides over the cells it is compared with
                p1 = pb + LIFT * UP
                pts = [pb, p1]
                if cmp:
                    pts.append(np.array([cells[cmp[-1]].get_x(), p1[1], 0]))
                path = VMobject().set_points_as_corners(pts)
                total = LIFT + (pts[-1][0] - pb[0])
                glide = [time_span(MoveAlongPath(X, path), 0, tg)]
                ends = [tg]
                for t in cmp:
                    frac = (LIFT + cells[t].get_x() - pb[0]) / total
                    st = max(0.0, inv_smooth(frac) * tg - 0.35)
                    en = min(st + 0.7, tg + 0.25)
                    glide.append(time_span(FlashAround(cells[t], color=GOLD, time_width=1.5), st, en))
                    ends.append(en)
                self.play(*glide, run_time=max(ends))

                # neighbours part, it drops in; the nest loses a level; the count lands
                tmp = ConsChain(Lnew).scale(S).move_to([0, YC, 0])
                part = lambda a: time_span(a, 0.1 * td, 0.65 * td)   # noqa: E731
                late = lambda a: time_span(a, 0.35 * td, td)         # noqa: E731
                drop = []
                for t, cell in enumerate(cells):
                    ti = t if t < j else t + 1
                    drop.append(part(cell.animate.move_to(tmp.cells[ti].get_center())))
                drop.append(part(nil.animate.move_to(tmp.nil.get_center())))
                new_arrows = [None] * len(Lnew)
                for t, ar in enumerate(arrows):
                    if j >= 1 and t == j - 1:
                        drop.append(time_span(FadeOut(ar), 0, 0.25 * td))
                        continue
                    ti = t if t < j - 1 else t + 1
                    drop.append(part(Transform(ar, tmp.arrows[ti].copy())))
                    new_arrows[ti] = ar
                for ti in ([j - 1] if j >= 1 else []) + [j]:
                    a = tmp.arrows[ti].copy()
                    new_arrows[ti] = a
                    drop.append(time_span(GrowArrow(a), 0.72 * td, td))
                landed = ConsCell(k).scale(S).move_to(tmp.cells[j].get_center())
                drop.append(Transform(X, landed, path_func=glide_drop, rate_func=linear))

                N = Code(n_str(outer_after[i], Lnew), size=NSIZE)
                place(N, NEST_Y1)
                for kk in outer_after[i]:
                    VGroup(*gsub(N, f"ins {kk}")).set_color(YELLOW)
                pairs, gone, born = collapse_map(nest.src, N.src, k)
                anims, wr = morph(nest, N, pairs, gone, born)
                drop += [late(a) for a in anims]
                drop.append(late(Transform(box, token_box(list_glyphs(N), N))))

                lab = Mono(f"ins {k}", size=28, color=DIM).move_to([SLOT_X[i], LAB_Y, 0])
                num = T(str(counts[i]), size=44, color=GOLD).move_to([SLOT_X[i], NUM_Y, 0])
                drop.append(time_span(FadeIn(lab, shift=0.2 * DOWN), 0.5 * td, td))
                drop.append(time_span(FadeIn(num, shift=0.2 * DOWN), 0.6 * td, td))
                self.play(*drop, run_time=td)
                self.finish(nest, N, wr)
                nest = N
                cells.insert(j, X)
                arrows = new_arrows
                self.nums.append(num)
                self.labs.append(lab)

            # {result}: the reply, and the lecture's tick
            c.wait_until("result")
            reply = place(Code("- : int list = [3; 4; 5; 7; 9]", size=NSIZE), NEST_Y1)
            off = reply.src.index("[")
            anims, wr = morph(nest, reply, [(t, off + t) for t in range(len(nest.src))],
                              born=range(off))
            tick = check_mark(GREEN).scale(0.75).next_to(nil, RIGHT, buff=0.25)
            self.play(FadeOut(box), *anims, time_span(Create(tick), 0.5, 1.4), run_time=1.4)
            self.finish(nest, reply, wr)
            self.result = reply

    # ------------------------------------------------------------ c2.insort.4
    def clip4(self):
        with self.say("c2.insort.4") as c:
            sweep_clear(self, keep=[self.ins, self.code, self.result, *self.nums], run_time=1.0)

            c.wait_until("zero")
            digits = [T(str(v), size=64, color=GOLD) for v in (0, 1, 2, 2, 1)]
            plus = [T("+", size=64) for _ in range(4)]
            eqs, six = T("=", size=64), T("6", size=64, color=GOLD)
            row = VGroup(digits[0], plus[0], digits[1], plus[1], digits[2], plus[2],
                         digits[3], plus[3], digits[4], eqs, six)
            row.arrange(RIGHT, buff=0.32).move_to([0, 0.0, 0])
            gather = [time_span(ReplacementTransform(n, d), 0.15 * t, 1.1 + 0.15 * t)
                      for t, (n, d) in enumerate(zip(self.nums, digits))]
            gather += [time_span(FadeIn(p), 0.6 + 0.15 * t, 1.4 + 0.15 * t) for t, p in enumerate(plus)]
            self.play(*gather, run_time=2.0)

            c.wait_until("make six")
            self.play(FadeIn(eqs), TransformFromCopy(VGroup(*digits), six), run_time=1.3)

            c.wait_until("floor")
            seven = T("7", size=64, color=GOLD).move_to([-3.65, -1.45, 0])
            lab7 = T("worst input, any comparison sort", size=32, color=DIM)
            lab7.next_to(seven, RIGHT, buff=0.5)
            self.play(FadeIn(seven, shift=0.3 * DOWN),
                      time_span(FadeIn(lab7, shift=0.2 * LEFT), 0.4, 1.3), run_time=1.3)

            c.wait_until("easy")
            six2 = T("6", size=64, color=GREEN).next_to(seven, DOWN, buff=0.4)
            lab6 = T("this input", size=32, color=GREEN).next_to(six2, RIGHT, buff=0.5)
            lab6.align_to(lab7, LEFT)
            self.play(TransformFromCopy(six, six2),
                      time_span(FadeIn(lab6, shift=0.2 * LEFT), 0.8, 1.6), run_time=1.6)

            c.wait_until("happens to be easy")
            self.play(FlashAround(VGroup(six2, lab6), color=GREEN, time_width=1.5), run_time=1.3)

    # ------------------------------------------------------------ c2.insort.5
    def clip5(self):
        with self.say("c2.insort.5") as c:
            sweep_clear(self, keep=[self.ins, self.code], run_time=1.2)

            lines = [T(s, size=34, color=DIM) for s in (
                "Items from the input are copied",
                "one at a time to the output.",
                "Each new item is inserted into the right place",
                "so that the output is always in order.")]
            cap = VGroup(*lines).arrange(DOWN, buff=0.22).move_to([0, -0.25, 0])

            c.wait_until("Items from the input")
            self.play(FadeIn(lines[0], shift=0.2 * UP),
                      time_span(FadeIn(lines[1], shift=0.2 * UP), 0.5, 1.5), run_time=1.5)

            c.wait_until("each into its right place")
            self.play(FadeIn(lines[2], shift=0.2 * UP),
                      time_span(FadeIn(lines[3], shift=0.2 * UP), 0.5, 1.5), run_time=1.5)

            c.wait_until("always in order")
            good = select(lines[3], "always in order")[0]
            self.play(*recolor(good, GREEN), FlashUnder(good, color=GREEN, time_width=1.5), run_time=1.2)

            # {strings}: the same code sorts strings
            c.wait_until("strings")
            inp = Code('insort ["dog"; "cat"; "emu"]', size=NSIZE).move_to([0, -1.2, 0])
            inp.find("insort").set_color(YELLOW)
            for w in ('"dog"', '"cat"', '"emu"'):
                inp.find(w).set_color(YELLOW)
            self.play(cap.animate.scale(0.85).move_to([0, 0.8, 0]),
                      time_span(FadeIn(inp, shift=0.2 * UP), 0.6, 1.5), run_time=1.5)

            c.wait_until("dog")
            self.play(FlashUnder(inp.find('["dog"; "cat"; "emu"]'), time_width=1.5), run_time=1.0)

            c.wait_until("becomes")
            rep = Code('- : string list = ["cat"; "dog"; "emu"]', size=NSIZE).move_to([0, -2.4, 0])
            rep.find("string list").set_color(GREEN)
            grown, used = [], set()
            for w in ('"cat"', '"dog"', '"emu"'):
                rep.find(w).set_color(YELLOW)
                a = rep.src.index(w)
                grown.append((VGroup(*gsub(inp, w)), list(range(a, a + len(w)))))
                used.update(range(a, a + len(w)))
            born = [t for t in range(len(rep.src)) if t not in used]
            anims, wr = morph(None, rep, born=born, grown=grown)
            self.play(*anims, run_time=min(1.4, max(0.8, c.until() - 0.4)))
            self.finish(None, rep, wr)
