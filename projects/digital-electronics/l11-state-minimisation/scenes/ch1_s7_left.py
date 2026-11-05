"""Chapter 1, scene 7: what's left. 7 states fit 3 flip-flops (one code spare, one function fewer,
one input fewer); the 7-state diagram read: after two bits it remembers same/different; the two
words 0101 and 1001; p. 147's first bullet names row matching. Clips c1.left.1 – c1.left.4.

Shared (s8 recap, ch3 s7: load_scene("ch1_s7_left")):
  seven_diagram() -> SevenDiagram (VGroup), s4's circle style with the merges done
    .states[name]          StateCircle (.circle, .letter) for A B C D E H J
    .arcs[(name, x)]       Arrow out of name on input x, for A..E
    .labels[(name, x)]     s4 MealyLabel on that arc (.inp BLUE, .slash, .out GREEN)
    .returns[name]         VGroup(path, tip): H's / J's bundled arrow down, left, up the left side, into A
    .ret_labels[name]      VGroup(0/0, ",", 1/0 or 1/1) on that return; .l0 .l1
    .one                   J's 1/1 label (= ret_labels["J"].l1)
  SEVEN_NEXT[name] = (next on 0, next on 1); SEVEN_POS[name] = centre
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

S2 = load_scene("ch1_s2_why")
S3 = load_scene("ch1_s3_mealy")
S4 = load_scene("ch1_s4_tree")


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- the 7-state machine (checked)
SEVEN_NEXT = {"A": ("B", "C"), "B": ("D", "E"), "C": ("E", "D"), "D": ("H", "H"), "E": ("J", "H"),
              "H": ("A", "A"), "J": ("A", "A")}
SR = 0.42
SEVEN_POS = {"A": _p(0.5, 3.0), "B": _p(-2.5, 1.6), "C": _p(3.5, 1.6), "D": _p(-1.1, 0.15),
             "E": _p(2.1, 0.15), "H": _p(-1.1, -1.45), "J": _p(2.1, -1.45)}
RET = {"H": dict(bus_y=-2.3, side_x=-4.9, top_dy=-0.15), "J": dict(bus_y=-2.9, side_x=-5.5, top_dy=0.15)}


def _on(name, ang):
    return SEVEN_POS[name] + SR * np.array([np.cos(ang), np.sin(ang), 0])


def _edge(a, b):
    pa, pb = SEVEN_POS[a], SEVEN_POS[b]
    d = (pb - pa) / np.linalg.norm(pb - pa)
    return pa + d * SR, pb - d * SR


def _arrow(s, e, **kw):
    return Arrow(s, e, buff=0, stroke_width=3.5, color=FG, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.25, **kw)


def _lbl_at(lbl, s, e, frac, normal, off):
    n = np.array([*normal, 0], dtype=float)
    n /= np.linalg.norm(n)
    lbl.move_to(s + (e - s) * frac + n * off)
    return lbl


class SevenDiagram(VGroup):
    def __init__(self, size=30):
        super().__init__()
        self.states, self.arcs, self.labels, self.returns, self.ret_labels = {}, {}, {}, {}, {}
        for n, p in SEVEN_POS.items():
            self.states[n] = S4.StateCircle(n, radius=SR, size=38).move_to(p)
        ml = lambda x, o: S4.mealy_label(x, o, size)  # noqa: E731
        # A's two arcs
        for x, side in ((0, -1), (1, 1)):
            s, e = _edge("A", SEVEN_NEXT["A"][x])
            self.arcs[("A", x)] = _arrow(s, e)
            self.labels[("A", x)] = S4.place_on_arc(ml(x, 0), s, e, side)
        # B -> D (0, outer left), B -> E (1, above, near B); mirrored for C
        s, e = _edge("B", "D")
        self.arcs[("B", 0)] = _arrow(s, e)
        self.labels[("B", 0)] = S4.place_on_arc(ml(0, 0), s, e, -1)
        s, e = _edge("B", "E")
        self.arcs[("B", 1)] = _arrow(s, e)
        self.labels[("B", 1)] = _lbl_at(ml(1, 0), s, e, 0.3, (0.3, 1), 0.3)
        s, e = _edge("C", "E")
        self.arcs[("C", 0)] = _arrow(s, e)
        self.labels[("C", 0)] = S4.place_on_arc(ml(0, 0), s, e, 1)
        s, e = _edge("C", "D")
        self.arcs[("C", 1)] = _arrow(s, e)
        self.labels[("C", 1)] = _lbl_at(ml(1, 0), s, e, 0.3, (-0.3, 1), 0.3)
        # D -> H on both inputs: two curved arcs
        for x, ang, arc in ((0, -2.2, 1.0), (1, -0.94, -1.0)):
            s = _on("D", ang)
            e = _on("H", -ang)
            self.arcs[("D", x)] = _arrow(s, e, path_arc=arc)
            dx = -1 if x == 0 else 1
            self.labels[("D", x)] = ml(x, 0).move_to((s + e) / 2 + _p(dx * 0.62, 0))
        # E -> J (0, right side), E -> H (1, below)
        s, e = _edge("E", "J")
        self.arcs[("E", 0)] = _arrow(s, e)
        self.labels[("E", 0)] = S4.place_on_arc(ml(0, 0), s, e, 1)
        s, e = _edge("E", "H")
        self.arcs[("E", 1)] = _arrow(s, e)
        self.labels[("E", 1)] = _lbl_at(ml(1, 0), s, e, 0.45, (0.4, -1), 0.3)
        self.add(*self.states.values(), *self.arcs.values(), *self.labels.values())
        # returns to A: two bundled arrows up the left side
        a = SEVEN_POS["A"]
        for n in ("H", "J"):
            r = RET[n]
            p = SEVEN_POS[n]
            ty = a[1] + r["top_dy"]
            ex = a[0] - np.sqrt(SR ** 2 - r["top_dy"] ** 2)
            tip_start = _p(ex - 0.6, ty)
            path = VMobject().set_points_as_corners([
                p + SR * DOWN, _p(p[0], r["bus_y"]), _p(r["side_x"], r["bus_y"]),
                _p(r["side_x"], ty), tip_start]).set_stroke(FG, 3.5)
            tip = Arrow(tip_start, _p(ex, ty), buff=0, stroke_width=3.5, color=FG, tip_length=0.2,
                        max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)
            self.returns[n] = VGroup(path, tip)
            l0, l1 = ml(0, 0), ml(1, 1 if n == "J" else 0)
            comma = T(",", size)
            g = VGroup(l0, comma, l1).arrange(RIGHT, buff=0.08)
            l1.shift(0.12 * RIGHT)
            comma.align_to(l0, DOWN).shift(0.06 * DOWN)
            g.l0, g.l1 = l0, l1
            if n == "H":
                g.move_to(_p(-3.0, r["bus_y"] + 0.32))
            else:
                g.move_to(_p(0.4, r["bus_y"] + 0.32))
            self.ret_labels[n] = g
        self.one = self.ret_labels["J"].l1
        self.add(*self.returns.values(), *self.ret_labels.values())

    def path(self, steps):
        """Arcs for a walk: steps = [(state, input), ...]; a step from H or J is its return."""
        out = []
        for n, x in steps:
            out.append(self.returns[n] if n in ("H", "J") else self.arcs[(n, x)])
        return out


def seven_diagram(size=30):
    return SevenDiagram(size)


# ---------------------------------------------------------------- scene-local drawings
def fn_line(n, size=52):
    toks, cols = [], []
    for i in range(n - 1, -1, -1):
        toks.append(f"D_{i}")
        cols.append(BLUE)
        if i:
            toks.append(",")
            cols.append(FG)
    toks += ["=", "f("]
    cols += [FG, FG]
    for i in range(n - 1, -1, -1):
        toks += [f"s_{i}", ","]
        cols += [GREEN, FG]
    toks += ["X", ")"]
    cols += [BLUE, FG]
    m = MathTex(*toks, font_size=size)
    for part, col in zip(m, cols):
        part.set_color(col)
    m.eq = m[toks.index("=")]
    return m


def light(arcs, color=YELLOW, start=0.0, end=1.0):
    """Recolour arcs one after another inside [start, end] of the play."""
    n = len(arcs)
    span = (end - start) / n
    out = []
    for i, a in enumerate(arcs):
        out += during([a.animate.set_color(color)], start + i * span, start + (i + 1) * span)
    return out


def word_block(bits, outs, center):
    """X row (BLUE bits) over Y row (GREEN outputs), columns at pitch 0.62."""
    pitch = 0.62
    xs = [center[0] + (i - 1.5) * pitch for i in range(4)]
    xb = [Mono(b, 44, BLUE).move_to(_p(x, center[1] + 0.33)) for b, x in zip(bits, xs)]
    yb = [Mono(o, 44, GREEN).move_to(_p(x, center[1] - 0.33)) for o, x in zip(outs, xs)]
    hx = T("X", 30, BLUE).move_to(_p(xs[0] - 0.75, center[1] + 0.33))
    hy = T("Y", 30, GREEN).move_to(_p(xs[0] - 0.75, center[1] - 0.33))
    g = VGroup(hx, hy, *xb, *yb)
    g.xb, g.yb, g.hx, g.hy, g.xs = xb, yb, hx, hy, xs
    return g


def col_brace(block, i0, i1, text):
    y = block.yb[0].get_bottom()[1] - 0.08
    br = Brace(Line(_p(block.xs[i0] - 0.24, y), _p(block.xs[i1] + 0.24, y)), DOWN, buff=0.06, color=DIM)
    lab = T(text, 30, YELLOW).next_to(br, DOWN, buff=0.1)
    return br, lab


class Left(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- the ladder: 7 states, 3 flip-flops -----------------------------------------------------
    def clip1(self):
        with self.say("c1.left.1") as c:
            lad = S2.ladder()
            lad.align_to(_p(-6.6, 0), LEFT)
            lad.shift(UP * (3.4 - lad.get_top()[1]))
            b15 = S2.ladder_bracket(lad, 3, 15)
            self.play(FadeIn(lad), FadeIn(b15), run_time=min(1.2, c.until("three")))   # early: the ladder returns whole, as in s2

            c.wait_until("three")
            b7 = S2.ladder_bracket(lad, 2, 7, x=b15.brace.get_left()[0])
            self.play(GrowFromCenter(b7.brace), *during(appear(b7.tag, b7.formula, lag=0.3), 0.25, 1),
                      *set_alpha([lad.rows[0], lad.rows[1]], 0.4), run_time=1.5)
            chips = S2.code_chips(unused=("111",), crossed=False).scale(0.8).move_to(_p(-3.4, -2.25))
            self.play(*appear(*chips.chips, shift=None, lag=0.08), run_time=1.2)
            spare = T("1 code to spare", 36, GOLD).next_to(chips, RIGHT, buff=0.7).shift(0.4 * UP)
            c.wait_until(own_word=spare)
            self.play(FlashAround(chips.chips[7], color=GOLD, run_time=1.2), *appear(spare), run_time=1.2)

            ffs = T("4 → 3 flip-flops", 40, GOLD).next_to(spare, DOWN, buff=0.4, aligned_edge=LEFT)
            c.wait_until("saved")
            self.play(*appear(ffs), FlashAround(b7.formula, color=GOLD, run_time=1.4), run_time=1.4)

            c.wait_until("functions")
            old = fn_line(4).move_to(_p(0, 1.2))
            new = fn_line(3)
            new.shift(_p(old.eq.get_x() - new.eq.get_x(), -0.1))
            sweep_clear(self, *appear(old), keep=[ffs], run_time=min(1.6, c.until("design")))
            c.wait_until("design")
            self.play(*appear(new), run_time=1.2)
            c.wait_until("fewer state bit")
            strike = Line(old.get_left() + 0.15 * LEFT, old.get_right() + 0.15 * RIGHT).set_stroke(DIM, 4)
            self.play(Create(strike), old.animate.set_color(DIM), run_time=1.2)
            self.fns = VGroup(old, new, strike)

    # -- the 7-state diagram: same or different after two bits ----------------------------------
    def clip2(self):
        with self.say("c1.left.2") as c:
            d = seven_diagram()
            self.d = d
            sweep_clear(self, FadeIn(d), run_time=min(2.2, c.until("two")))   # early: the whole shape first
            c.wait_until("two")

            paths = [("00", [("A", 0), ("B", 0)], "D"), ("11", [("A", 1), ("C", 1)], "D"),
                     ("01", [("A", 0), ("B", 1)], "E"), ("10", [("A", 1), ("C", 0)], "E")]
            slots = {"D": [_p(-3.95, 0.45), _p(-3.25, 0.45)], "E": [_p(4.25, 0.45), _p(4.95, 0.45)]}
            cues = ["two", "remembers", "whether", "or different"]
            prev, tags = [], {"D": [], "E": []}
            for k, ((bits, steps, dst), cue) in enumerate(zip(paths, cues)):
                c.wait_until(cue)
                arcs = d.path(steps)
                tag = Mono(bits, 36, BLUE).move_to(slots[dst][len(tags[dst])])
                tags[dst].append(tag)
                restore = during([a.animate.set_color(FG) for a in prev], 0, 0.3) if prev else []
                rt = 1.8 if k == 0 else 1.3
                self.play(*restore, *light(arcs, start=0.1, end=0.75),
                          *during(appear(tag, shift=None), 0.7, 1), run_time=min(rt, c.until(floor=0.8)))
                prev = arcs
            self.tags = tags

            c.wait_until("same")
            same = T("same", 34, YELLOW).move_to(_p(-3.6, -0.1))
            self.play(*[a.animate.set_color(FG) for a in prev], *appear(same),
                      FlashAround(d.states["D"].circle, color=YELLOW, run_time=1.4), run_time=1.4)
            c.wait_until("diff")
            diff = T("different", 34, YELLOW).move_to(_p(4.6, -0.1))
            self.play(*appear(diff), FlashAround(d.states["E"].circle, color=YELLOW, run_time=1.4),
                      run_time=min(1.4, c.until(floor=0.8)))
            self.same, self.diff = same, diff

    # -- reading each state ---------------------------------------------------------------------
    def clip3(self):
        d = self.d
        with self.say("c1.left.3") as c:
            dead = [d.arcs[("D", 0)], d.arcs[("D", 1)], d.returns["H"]]
            self.play(*light(dead), run_time=1.6)
            c.wait_until("output stays")
            zeros = [d.labels[("D", 0)].out, d.labels[("D", 1)].out, d.ret_labels["H"].l0.out, d.ret_labels["H"].l1.out]
            stays = T("output\nstays 0", 30, GREEN, line_spacing=0.8).move_to(_p(0.3, -1.68))   # beside H, clear of the tags
            self.play(*flash(zeros, color=GREEN, run_time=1.3), *appear(stays), run_time=1.3)
            c.wait_until("end of the word")
            self.play(*[a.animate.set_color(FG) for a in dead],
                      *set_alpha([d.states["D"], d.states["H"]], 0.5), run_time=1.0)

            c.wait_until("zero")
            self.play(*light([d.arcs[("E", 0)]]), FlashAround(d.labels[("E", 0)].inp, color=BLUE, run_time=1.2),
                      run_time=1.2)
            c.wait_until("one")
            self.play(*light([d.returns["J"]]), FlashAround(d.one, color=GREEN, run_time=1.5), run_time=1.5)
            c.wait_until("other")
            self.play(*light([d.arcs[("E", 0)], d.returns["J"]], color=FG, start=0, end=0.4),
                      *light([d.arcs[("E", 1)]], start=0.3, end=0.8),
                      FlashAround(d.labels[("E", 1)].out, color=GREEN, run_time=1.4), run_time=1.4)
            self.stays = stays
            self.play(d.arcs[("E", 1)].animate.set_color(FG), *set_alpha([d.states["D"], d.states["H"]], 1),
                      run_time=min(1.0, c.until(floor=0.5)))

    # -- the two words, the pattern, the name ---------------------------------------------------
    def clip4(self):
        d = self.d
        with self.say("c1.left.4") as c:
            gone = [*self.tags["D"], *self.tags["E"], self.same, self.diff]
            d.generate_target()
            d.target.shift(1.0 * LEFT)
            self.play(*during(disappear(*gone, self.stays), 0, 0.45), *during([MoveToTarget(d)], 0.3, 1),
                      run_time=min(1.6, c.until("zero one zero one")))

            w1 = word_block("0101", "0001", _p(5.35, 2.3))
            w2 = word_block("1001", "0001", _p(5.35, -0.6))
            walks = [d.path([("A", 0), ("B", 1), ("E", 0), ("J", 1)]),
                     d.path([("A", 1), ("C", 0), ("E", 0), ("J", 1)])]
            prev = []
            for w, walk, cue in ((w1, walks[0], "zero one zero one"), (w2, walks[1], "one zero zero one")):
                c.wait_until(cue)
                restore = during([a.animate.set_color(FG) for a in prev if a not in walk], 0, 0.3) if prev else []
                cols = [w.hx, w.hy, *[m for pair in zip(w.xb, w.yb) for m in pair]]
                self.play(*restore, *appear(*cols, shift=None, lag=0.12), *light(walk, start=0.1, end=1),
                          run_time=min(1.6, c.until("pattern") if w is w2 else c.until("one zero zero one")))
                prev = walk

            for (i0, i1, text, cue) in ((0, 1, "differ", "differ"), (2, 2, "0", "third"), (3, 3, "1", "fourth")):
                c.wait_until(cue)
                parts = []
                for w in (w1, w2):
                    br, lab = col_brace(w, i0, i1, text)
                    parts += [br, lab]
                done = [a.animate.set_color(FG) for a in prev] if text == "differ" else []
                self.play(*done, *[GrowFromCenter(p) for p in parts[0::2]],
                          *during(appear(*parts[1::2], lag=0.1), 0.3, 1), run_time=1.0)

            c.wait_until("procedure")
            bullet = T("The procedure employed to find equivalent states\nin this example is known as row matching.",
                       36, line_spacing=1.0, disable_ligatures=True).move_to(_p(0, 1.4))
            # the whole board leaves together (a lagged sweep faded the word blocks glyph by glyph)
            self.play(*during(disappear(*self.mobjects), 0, 0.45), *during(appear(bullet), 0.5, 1),
                      run_time=min(1.8, c.until("called")))
            c.wait_until("called")
            rm = select(bullet, "row matching")[0]
            self.play(*recolor(rm, YELLOW), FlashUnder(rm, color=YELLOW, run_time=1.4, time_width=1.5), run_time=1.4)

            c.wait_until("merges")
            ident = T("identical next states, identical outputs", 36, YELLOW).move_to(_p(0, -0.4))
            rows = [("D", "H", "H", "0", "0"), ("G", "H", "H", "0", "0")]
            tbl = S3.state_table(rows=rows, size=36, pitch=0.6, top=0.0, rules_after=())
            icon = VGroup(*tbl.rows)
            boxes = VGroup(*[tbl.row_box(r, color=GOLD) for r in range(2)])
            pair = VGroup(boxes, icon).move_to(_p(0, -1.9))
            c.wait_until(own_word=ident)
            self.play(*appear(ident), run_time=1.0)
            self.play(*appear(icon, shift=None), *during([FadeIn(boxes)], 0.3, 1), run_time=1.2)
        self.wait(1.5)
