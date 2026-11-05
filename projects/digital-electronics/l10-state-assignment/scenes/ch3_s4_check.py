"""Chapter 3, scene 4: do our counters self-start? Feed every unused state into each design's logic. Clips c3.check.1 – c3.check.4.

Shared (for s8):
  checked_ring(kind, center=..., arrows=False)
      kind "binary" (ch1: 000 001 010 011 100) or "sliding" (ch2: 000 001 011 110 100): ch2_s1's
      five_ring (radius 1.35, .code_at) with the three unused states as DIM circles outside it (binary ones tagged 5, 6, 7),
      DIM codes beside them. .ring .unused {code: node (.circ .code .num)} .esc [YELLOW escape arrows,
      in narrated order] (added to the group only with arrows=True).
  check_rings(arrows=True) -> VGroup(binary at C_L, sliding at C_R): the end-of-clip-3 layout.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

H2 = load_scene("ch2_s1_hook")
K7 = load_scene("ch1_s7_kmaps")
P3 = load_scene("ch3_s3_powerup")
five_ring, NODE_R = H2.five_ring, H2.NODE_R
RING_R = 1.35
kmap3, kmap_eq = K7.kmap3, K7.kmap_eq


def selfstart_tag(ring):
    """P3's GREEN pill under a ring, kept a little clearer of the bottom code (101 / 111)."""
    return P3.selfstart_tag(ring).shift(0.04 * DOWN)


def _p(x, y):
    return np.array([x, y, 0.0])


def _slot(deg, r=2.5):
    a = np.radians(deg)
    return _p(r * np.cos(a), r * np.sin(a))


# ---- shared: the two rings with their unused states -------------------------------------------------
U_R = 0.42
C_L, C_R = _p(-3.6, 0.4), _p(3.9, 0.4)
RING_CODES = {"binary": ["000", "001", "010", "011", "100"],
              "sliding": ["000", "001", "011", "110", "100"]}
# code: (offset from ring centre, number tag or None, label side)
UNUSED = {
    "binary": [("101", _slot(-90, 2.45), "5", DOWN), ("110", _slot(-18), "6", DOWN),
               ("111", _slot(198), "7", DOWN)],
    "sliding": [("010", _slot(198), None, LEFT), ("101", _p(-2.38, -2.3), None, LEFT),
                ("111", _slot(-90, 2.45), None, DOWN)],
}
# escape arrows in narrated order: (from unused code, to ring node index or unused code)
ESCAPES = {"binary": [("111", 4), ("101", 2), ("110", 2)],
           "sliding": [("010", 4), ("111", 3), ("101", "010")]}


def unused_node(pos, code, num=None, side=DOWN):
    circ = Circle(radius=U_R).set_stroke(DIM, 3).set_fill(BG, 1).move_to(pos)
    lab = Mono(code, size=28, color=DIM).next_to(circ, side, buff=0.12)
    parts = [circ, lab]
    n = None
    if num is not None:
        n = T(num, 34, DIM).move_to(pos)
        parts.append(n)
    g = VGroup(*parts)
    g.circ, g.code, g.num = circ, lab, n
    return g


def esc_arrow(p, q, r0, r1, color=YELLOW):
    u = (q - p) / np.linalg.norm(q - p)
    return Arrow(p + (r0 + 0.04) * u, q - (r1 + 0.04) * u, buff=0, color=color, stroke_width=3,
                 tip_length=0.18, max_tip_length_to_length_ratio=0.4)


def checked_ring(kind, center=None, arrows=False):
    center = np.array(C_L if center is None and kind == "binary" else C_R if center is None else center,
                      dtype=float)
    ring = five_ring(RING_CODES[kind], radius=RING_R).shift(center)
    ring.center = center
    unused = {}
    for code, off, num, side in UNUSED[kind]:
        unused[code] = unused_node(center + off, code, num, side)
    esc = []
    for src, dst in ESCAPES[kind]:
        p = unused[src].circ.get_center()
        if isinstance(dst, int):
            q, r1 = ring.circles[dst].get_center(), NODE_R
        else:
            q, r1 = unused[dst].circ.get_center(), U_R
        esc.append(esc_arrow(p, q, U_R, r1))
    g = VGroup(ring, *unused.values())
    g.ring, g.unused, g.esc = ring, unused, esc
    if arrows:
        g.add(*esc)
    return g


def check_rings(arrows=True):
    return VGroup(checked_ring("binary", C_L, arrows), checked_ring("sliding", C_R, arrows))


# ---- scene-local pieces ------------------------------------------------------------------------------
EQ_BIN = [K7.EQ_A, K7.EQ_B, K7.EQ_C]
EQ_SLIDE = [["D_a", "=", r"\overline{b}\cdot\overline{c}"], ["D_b", "=", "a"], ["D_c", "=", "b"]]
BIG = 48
EQ_X, EQ_YS = 1.4, (1.3, 0.1, -1.1)          # the "=" signs of the big binary logic (clips 1-2)
INP_Y, RES_Y = 2.6, -2.5
RES_XS = (6.1, 5.6, 5.1)    # D_a, D_b, D_c result digits: a staircase, so each drops straight to c' b' a'
COL_XS = (4.5, 5.9)


def logic_block(parts_list, size, eq_x, ys):
    eqs = []
    for parts, y in zip(parts_list, ys):
        e = kmap_eq(parts, size)
        e.shift(_p(eq_x - e[1].get_x(), y - e[1].get_y()))
        eqs.append(e)
    return eqs


def small_logic(parts_list, corner):
    eqs = logic_block(parts_list, 34, 0.0, (0.0, -0.62, -1.24))
    g = VGroup(*eqs)
    g.move_to(corner, aligned_edge=UL if corner[0] < 0 else UR)
    return eqs


def on_row(m, eq, x=None, left=None):
    """m sitting on eq's baseline (its right-hand side), at centre x or with its left edge at left."""
    if left is not None:
        m.next_to(_p(left, 0), RIGHT, buff=0)
    else:
        m.set_x(x)
    m.align_to(eq[-1], DOWN)
    return m


class Check(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c3.check.1: the binary counter, 111 fed in ---------------------------------------------------
    def clip1(self):
        L = self.L = checked_ring("binary", C_L)
        with self.say("c3.check.1") as c:
            self.play(*appear(L.ring), run_time=1.5)
            c.wait_until("binary count")
            eqs = self.eqs = logic_block(EQ_BIN, BIG, EQ_X, EQ_YS)
            self.play(*appear(*eqs, lag=0.3), run_time=min(1.4, c.until("unused")))
            c.wait_until("five")
            us = [L.unused[k] for k in ("101", "110", "111")]
            self.play(*appear(*us, lag=0.35, shift=None), run_time=min(1.6, c.until("feed")))
            c.wait_until("feed")

            u7 = L.unused["111"]
            inp_l = MathTex("cba", "=", font_size=BIG)
            inp_r = MathTex("111", font_size=BIG, color=GOLD)
            inp_l.shift(_p(EQ_X - inp_l[1].get_x(), INP_Y - inp_l[1].get_y()))
            inp_r.next_to(inp_l, RIGHT, buff=0.2).align_to(inp_l[0], DOWN)
            self.inp = [inp_l, inp_r]
            self.play(FlashAround(VGroup(u7.circ, u7.code), time_width=1.5), *appear(inp_l, inp_r, shift=None),
                      run_time=min(1.5, c.until("the input")))
            c.wait_until("the input")

            subs_tex = [r"\overline{1}\cdot\overline{1}", r"1\oplus 1", r"1\cdot 1"]
            vals = ["0", "0", "1"]
            cues = [("not see", "which is zero"), ("exclusive-or", "also zero"), ("bee and a", "which is one")]
            self.subs, self.res = [], []
            for e, st, v, (c1, c2), rx in zip(eqs, subs_tex, vals, cues, RES_XS):
                s = MathTex("=", st, font_size=BIG)
                if r"\oplus" in st:
                    s[1][1].set_color(YELLOW)
                s.next_to(e, RIGHT, buff=0.22).align_to(e[-1], DOWN)
                req = MathTex("=", font_size=BIG).align_to(s[0], DOWN)
                req.set_x(max(rx - 0.5, s.get_right()[0] + 0.25 + req.width / 2))
                rv = MathTex(v, font_size=BIG, color=GOLD).set_x(rx).align_to(e[-1], DOWN)
                r = VGroup(req, rv)
                c.wait_until(c1)
                self.play(*appear(s, shift=None), run_time=min(1.0, c.until(c2)))
                c.wait_until(c2)
                self.play(*appear(req, rv, lag=0, shift=None), run_time=0.8)
                self.subs.append(s)
                self.res += [req, rv]
            c.wait_until("lands")

            # c' b' a' = 1 0 0, assembled from D_c, D_b, D_a
            rl = MathTex("c'b'a'", "=", font_size=BIG)
            rl.shift(_p(RES_XS[2] - 0.55 - rl[1].get_x(), RES_Y - rl[1].get_y()))
            digs = [MathTex(d, font_size=BIG, color=GOLD).move_to(_p(x, 0)).align_to(rl[0], DOWN)
                    for x, d in zip(RES_XS[::-1], "100")]
            self.resrow = [rl, *digs]
            flies = [*fly(self.res[5], digs[0], arc=0), *fly(self.res[3], digs[1], arc=0),
                     *fly(self.res[1], digs[2], arc=0)]
            for f in flies:
                f.rate_func = linear     # straight drops leave their source quickly: never doubled
            self.play(*appear(rl, shift=None), *flies,
                      run_time=min(1.8, c.until("that's four")))
            self.play(GrowArrow(L.esc[0]), run_time=1.0)
            c.wait_until("four")
            self.play(FlashAround(L.ring.circles[4], time_width=1.5, color=GREEN),
                      L.ring.circles[4].animate.set_stroke(GREEN), run_time=1.2)

    # -- c3.check.2: 101 and 110 -> 010; every unused state rejoins -----------------------------------
    def clip2(self):
        L, eqs = self.L, self.eqs
        with self.say("c3.check.2") as c:
            hdr_l = MathTex("cba", font_size=BIG)
            hdr_l.move_to(self.inp[0][0]).align_to(self.inp[0][0], LEFT)
            hdrs = [MathTex(s, font_size=BIG, color=GOLD).move_to(_p(x, INP_Y)).align_to(hdr_l, DOWN)
                    for s, x in zip(("101", "110"), COL_XS)]
            cols = [[], []]
            for j, (cba) in enumerate(("101", "110")):
                cc, bb, aa = (int(ch) for ch in cba)
                outs = [int((not aa) and (not cc)), aa ^ bb, aa & bb]
                for e, v in zip(eqs, outs):
                    cols[j].append(on_row(MathTex(str(v), font_size=BIG, color=GOLD if v else DIM), e, x=COL_XS[j]))
            rl2 = MathTex("c'b'a'", font_size=BIG).move_to(self.resrow[0][0]).align_to(hdr_l, LEFT)
            rres = [MathTex("010", font_size=BIG, color=GOLD).move_to(_p(x, 0)).align_to(rl2, DOWN)
                    .set_y(rl2.get_y()) for x in COL_XS]
            old = [*self.inp, *self.subs, *self.res, *self.resrow]
            new = [hdr_l, *hdrs, *cols[0], *cols[1], rl2, *rres]
            self.play(*during(disappear(*old), 0, 0.45), *during(appear(*new, lag=0.05, shift=None), 0.5, 1.0),
                      run_time=1.6)
            self.play(GrowArrow(L.esc[1]), GrowArrow(L.esc[2]), run_time=min(1.2, c.until("in both")))
            self.play(L.ring.circles[2].animate.set_stroke(GREEN), run_time=0.6)
            c.wait_until("in both")
            ones = [cols[0][1], cols[1][1]]
            self.play(*flash(ones, time_width=1.5), *recolor(ones, YELLOW),
                      eqs[1][0].animate.set_color(YELLOW), run_time=1.5)
            c.wait_until("next")
            pulses = [Line(a.get_start(), a.get_end()).set_stroke(YELLOW, 8) for a in L.esc]
            self.play(*[VShowPassingFlash(p, time_width=0.6) for p in pulses], run_time=1.6)
            c.wait_until("selfstart")
            tag = self.tagL = selfstart_tag(L)
            self.play(*appear(tag, shift=0.25 * UP), run_time=1.0)   # rises from below: never crosses 101
            self.board = [hdr_l, *hdrs, *cols[0], *cols[1], rl2, *rres]

    # -- c3.check.3: the sliding counter; 101 passes through 010 ---------------------------------------
    def clip3(self):
        L = self.L
        R = self.R = checked_ring("sliding", C_R)
        with self.say("c3.check.3") as c:
            small = small_logic(EQ_BIN, _p(-6.6, 3.6))
            self.play(*during(disappear(*self.board, *self.eqs), 0, 0.45),
                      *during(appear(*small, lag=0.15, shift=None), 0.5, 1.0), run_time=1.4)
            self.eqs = small
            self.eqsR = small_logic(EQ_SLIDE, _p(6.6, 3.6))
            self.play(*appear(R.ring), *appear(*self.eqsR, lag=0.2, shift=None),
                      run_time=min(1.3, c.until("its unused")))
            for code, cue in (("010", "zero one zero"), ("101", "one zero one"), ("111", "all ones")):
                c.wait_until(cue)
                self.play(*appear(R.unused[code], shift=None), run_time=0.9)
            c.wait_until("quick")
            self.play(GrowArrow(R.esc[0]), run_time=1.2)
            c.wait_until("all-ones state")
            self.play(GrowArrow(R.esc[1]), run_time=1.2)
            c.wait_until("both are used")
            used = [R.ring.circles[4], R.ring.circles[3]]
            self.play(*flash(used, color=GREEN, time_width=1.5), *[u.animate.set_stroke(GREEN) for u in used],
                      run_time=1.3)
            c.wait_until("through")
            self.play(GrowArrow(R.esc[2]), run_time=1.5)
            c.wait_until("unused too")
            self.play(FlashAround(R.unused["010"].circ, time_width=1.5, color=DIM), run_time=1.2)
            c.wait_until("one more edge")
            a0, a2 = R.esc[0], R.esc[2]
            path = VMobject().set_points_as_corners([R.unused["101"].circ.get_center(),
                                                    R.unused["010"].circ.get_center(), a0.get_end()])
            dot = Dot(path.get_start(), radius=0.11, color=YELLOW)
            self.play(FadeIn(dot), run_time=0.3)
            self.play(MoveAlongPath(dot, path), run_time=2.2, rate_func=linear)
            self.play(FadeOut(dot), FlashAround(R.ring.circles[4], color=GREEN, time_width=1.5), run_time=0.8)
            c.wait_until("eventually")
            card = self.card = P3.remedy_cards().cards[0]
            card.scale(0.55).move_to(_p(0.15, 2.75))
            word = card.word("eventually")
            self.play(*appear(card), run_time=1.0)  # early: card 1 shown whole, its word lit next
            c.wait_until("eventually reaches")
            self.play(*recolor(word, YELLOW), FlashUnder(word, time_width=1.5), run_time=1.5)

    # -- c3.check.4: both self-start, by luck: the K-map's X's ------------------------------------------
    def clip4(self):
        L, R = self.L, self.R
        with self.say("c3.check.4") as c:
            tagR = selfstart_tag(R)
            c.wait_until(own_word=tagR.text)
            self.play(*appear(tagR, shift=0.25 * UP), run_time=1.0)   # rises from below: never crosses 111
            c.wait_until("nobody planned")
            settle(self, L, add=L.esc)
            settle(self, R, add=R.esc)
            moves = []
            for g, tag, x in ((L, self.tagL, -4.75), (R, tagR, 4.75)):
                both = VGroup(g, tag)
                pc = both.get_center()
                top = pc[1] + 0.6 * (both.get_top()[1] - pc[1])
                sh = _p(x - pc[0], 3.55 - top)
                moves += [g.animate.scale(0.6, about_point=pc).shift(sh),
                          tag.animate.scale(0.6, about_point=pc).shift(sh)]
            self.play(*during(disappear(self.card, *self.eqs, *self.eqsR), 0, 0.4),
                      *during(moves, 0.4, 1.0), run_time=min(2.0, c.until("xs")))
            c.wait_until("xs")
            km = kmap3(K7.MAP_C, center=_p(-0.05, -0.35), scale=0.85, loops=K7.LOOPS_C, eq=K7.EQ_C, eq_size=42)
            xs = [km.ent[1][k] for k in (1, 2, 3)]
            km.entries.remove(*xs)
            self.play(*appear(km, *xs, shift=None), run_time=1.2)
            c.wait_until("became a one")
            one = km.value(1, 2, 1)
            self.play(*swap(xs[1], one), run_time=1.2)
            c.wait_until("became a zero")
            zeros = [km.value(1, k, 0) for k in (1, 3)]
            self.play(*swap(xs[0], zeros[0]), *swap(xs[2], zeros[1]), run_time=1.2)
            c.wait_until("we chose")
            cap = T("each X became whatever the loops made it", 32, FG).move_to(_p(0, -3.35))
            self.play(*appear(cap), run_time=1.0)  # early: caption sums up the sentence just said
            c.wait_until("lucky")
            lucks = [T("(by luck)", 30, DIM).next_to(t, DOWN, buff=0.15) for t in (self.tagL, tagR)]
            self.play(*appear(*lucks), run_time=1.0)
