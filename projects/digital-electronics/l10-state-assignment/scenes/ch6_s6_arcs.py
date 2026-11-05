"""Chapter 6, scene 6: one-hot equations straight from the diagram, one term per incoming arc (p. 143). Clips c6.arcs.1 – c6.arcs.4.

Opens from empty; ends on an empty frame.
Shared helpers (load_scene("ch6_s6_arcs")):
- `arcs_diagram()`: ch6_s2's onehot_diagram("left"), x1.1 about (-3.8, 0.05), shifted (0.25, 0.6):
  x -6.6..-0.5, y -1.3..2.6. `place_more(m)` applies that to anything placed like "left".
- `sync_arcs_shot()`: arcs_diagram() with the three arcs into Sync (6 Sight->Sync, 0 and 1 Sync's
  loops) lit YELLOW (stroke 5), as in this scene's {d2} beat (s8's recap).
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

S2 = load_scene("ch6_s2_codes")
S3 = load_scene("ch6_s3_inspect")
S5 = load_scene("ch5_s5_table")
D3 = load_scene("ch5_s3_diagram")


def _p(x, y):
    return np.array([x, y, 0.0])


DIAG_GROW = 1.1
NAME_GROW = 1.35
R_BIG = 0.78
GROW_ABOUT = np.array([-3.8, 0.05, 0.0])
DIAG_NUDGE = np.array([0.4, 0.6, 0.0])
STATES = ("Sync", "Hunt", "Sight")
INTO = {"Sync": [6, 0, 1], "Sight": [4, 5], "Hunt": [3, 7, 2]}
ARC_FROM = {0: "Sync", 1: "Sync", 2: "Sync", 3: "Hunt", 4: "Hunt", 5: "Sight", 6: "Sight", 7: "Sight"}
EQ_X = 0.0
EQ_SIZE = 40
ROW_Y = (2.4, 0.9, -0.6, -2.1)
DIMMED_OP = 0.3


def _style_arc(arc, col, w, op=1.0):
    arc.set_stroke(col, w, opacity=op)
    arc.get_tip().set_stroke(col, 1, opacity=op).set_fill(col, op)
    return arc


def big_diagram(codes, r=R_BIG):
    """ch5_s3's sync_diagram with roomier circles (r R_BIG), in ch6_s2's "left" placement, then place_more."""
    d = D3.sync_diagram(codes=codes, r=r)
    S2.place_diagram(d, "left")
    d.code["Sync"].shift(0.3 * RIGHT)      # clear of the bigger loops
    d.code["Hunt"].shift(0.3 * LEFT)
    owner = {0: "Sync", 1: "Sync", 3: "Hunt", 5: "Sight"}
    for i, n in owner.items():         # loop labels a little further out, clear of the bigger loops
        v = d.labels[i].get_center() - d.circle[n].get_center()
        d.labels[i].shift(0.12 * v / np.linalg.norm(v))
    place_more(d)
    return d


def arcs_diagram():
    d = big_diagram(S2.ONEHOT)
    d.one = {}
    for n, code in S2.ONEHOT.items():
        g = d.code[n][1 + code.index("1")]
        g.set_color(GOLD)
        d.one[n] = g
    for n in STATES:
        d.name[n].scale(NAME_GROW)
    return d


def place_more(m):
    """From ch6_s2's "left" placement to this scene's: x1.1 about its centre, nudged right and up."""
    m.scale(DIAG_GROW, about_point=GROW_ABOUT)
    m.shift(DIAG_NUDGE)
    return m


def sync_arcs_shot():
    d = arcs_diagram()
    d.circle["Sync"].set_stroke(YELLOW, 6)
    for i in INTO["Sync"]:
        _style_arc(d.arcs[i], YELLOW, 5)
    return d


def look(d, focus=None, lit=(), keep=()):
    """Every diagram part to its look: focus circle glows, `lit` arcs YELLOW, everything else
    (except the names in `keep`) dimmed; focus=None restores the plain diagram."""
    anims = []
    for n in STATES:
        on = focus is None or n == focus
        c = d.circle[n]
        t = c.copy().set_stroke(YELLOW if n == focus else FG, 6 if n == focus else 4,
                                opacity=1 if on else DIMMED_OP)
        anims.append(Transform(c, t))
        anims.append(restyle(d.name[n], 1 if (on or n in keep) else DIMMED_OP))
        anims.append(restyle(d.code[n], 1 if on else DIMMED_OP))
    for i, arc in enumerate(d.arcs):
        on = focus is None or i in lit
        col, w = (YELLOW, 5) if i in lit else (FG, 3)
        anims.append(Transform(arc, _style_arc(arc.copy(), col, w, 1 if on else DIMMED_OP)))
        anims.append(restyle(d.labels[i], 1 if on else DIMMED_OP))
    return anims


def slide_text():
    p1 = ["“Note that it is not strictly",
          "necessary to write down the state",
          "table, since the next state",
          "equations can be obtained from",
          "the state diagram”"]
    p2 = ["“It can be seen that for each state",
          "variable, the required equation is",
          "given by terms representing the",
          "incoming arcs on the graph”"]
    g1 = VGroup(*[T(s, 28) for s in p1]).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
    g2 = VGroup(*[T(s, 28) for s in p2]).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
    g = VGroup(g1, g2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    g.move_to(_p(3.2, 1.35))
    g.p1, g.p2 = g1, g2
    g.key = select(g2[3], "incoming arcs")[0]
    return g


def arc_template():
    a = VGroup(*[T(s, 28, GREEN) for s in ("flip-flop of", "the state", "the arc leaves")]).arrange(DOWN, buff=0.1)
    b = VGroup(*[T(s, 28, BLUE) for s in ("condition", "on the arc")]).arrange(DOWN, buff=0.1)
    ra = SurroundingRectangle(a, buff=0.3, corner_radius=0.1).set_stroke(GREEN, 2)
    rb = SurroundingRectangle(b, buff=0.3, corner_radius=0.1).set_stroke(BLUE, 2)
    rb.stretch_to_fit_height(ra.height)
    ga, gb = VGroup(ra, a), VGroup(rb, b)
    dot = MathTex(r"\cdot", font_size=60)
    g = VGroup(ga, dot, gb).arrange(RIGHT, buff=0.3)
    g.a, g.dot, g.b = ga, dot, gb
    return g


def built_line(lhs, y):
    return S3.put_line(S3.raw_line(lhs, EQ_SIZE), EQ_X, y)


def _quick(anims, rate=rush_from):
    """Flies that leave their source briskly (so the copy is off it early)."""
    for a in anims:
        a.rate_func = rate
    return anims


class LineBuild:
    """Copies of a line's pieces, put on screen term by term; settle() swaps them for the line."""

    def __init__(self, line):
        self.L = line
        self.shown = []

    def term(self, k):
        pieces = self.L.terms[k]
        tags = self.L.term_tags[k]
        var = pieces[0].copy()
        tag = tags[0].copy() if tags else None
        joint = pieces[1].copy()
        inp = VGroup(*[p.copy() for p in pieces[2:]])
        self.shown += [m for m in (var, tag, joint) if m is not None] + [inp]
        return var, tag, joint, inp

    def rest(self):
        g = VGroup(*[p.copy() for p in (*self.L.lhs, *self.L.plus)])
        self.shown.append(g)
        return g

    def settle(self, scene):
        for m in self.shown:
            scene.remove(*m.get_family())
        scene.add(self.L)
        return self.L


FF_XS = (-5.4, -2.75, -0.2)
FF_Y = -2.3


def small_ffs():
    units = [S2.onehot_ff(k, _p(x, FF_Y), scale=0.62, out_size=38, tag_size=28) for k, x in enumerate(FF_XS)]
    for u in units:
        u.ff.remove(u.ff.d_w)
        u.tag.next_to(u.ff.box, DOWN, buff=0.08)
    return units


def centred_hop(src_ff, dst_ff):
    """The 1's hop between two boxes, rising and landing through the middle of the box (clear of D and Q)."""
    a, b = S2.bit_spot(src_ff), S2.bit_spot(dst_ff)
    ac, bc = _p(src_ff.box.get_x(), a[1]), _p(dst_ff.box.get_x(), b[1])
    rise = src_ff.box.get_top()[1] - a[1] + 0.3
    p = VMobject()
    p.append_points(Line(a, ac).points)
    p.append_points(S2.hop_path(ac, bc, rise=rise).points)
    p.append_points(Line(bc, b).points)
    return p


class StraightFromDiagram(NarratedScene):
    def construct(self):
        self.d = arcs_diagram()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)      # let the one-hot term sit before the board clears
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ helpers
    def fly_term(self, b, k, src_state, arc_i, run_time, arcs=(0.8, 0.6), extra=()):
        """Term k of the line: the source's name flies down to the tag (or the term appears in
        place when src_state is None), the arc label flies to the inputs (or appears)."""
        var, tag, joint, inp = b.term(k)
        anims = []
        if src_state is not None:
            anims += during(_quick(fly(self.d.name[src_state], tag, arc=arcs[0]), linear), 0.35, 1.0)
            anims += during(appear(var, shift=None), 0.85, 1.0)
        else:
            anims += appear(var, tag, shift=None)
        if arc_i is not None:
            lab = self.d.labels[arc_i]
            same = MathTex(lab.tex_string, font_size=EQ_SIZE, color=BLUE).move_to(inp)
            b.shown[-1] = same
            anims += during(_quick(fly(lab, same, arc=arcs[1]), linear), 0, 0.65 if src_state else 1.0)
        else:
            anims += appear(inp, shift=None)
        anims += during(appear(joint, shift=None), 0.8, 1.0)
        anims += list(extra)
        self.play(*anims, run_time=run_time)

    def join(self, b, c, extra=(), run_time=1.2):
        rest = b.rest()
        self.play(*appear(rest, shift=None), *extra, run_time=run_time)
        return b.settle(self)

    # ------------------------------------------------------------ c6.arcs.1
    def clip1(self):
        d = self.d
        with self.say("c6.arcs.1") as c:
            ghost = S2.onehot_table()
            ghost.set_opacity(0.3)
            self.play(*appear(d, shift=None), *appear(ghost, shift=None),  # early: the diagram and table ghost shown whole
                      run_time=min(1.4, c.until("the table is optional")))
            c.wait_until("the table is optional")
            slide = slide_text()
            self.slide = slide
            self.play(*during(disappear(ghost), 0, 0.45), *during(appear(slide.p1, shift=None), 0.5, 1.0),  # early: the slide's text, quoted
                      run_time=1.6)
            c.wait_until("rule")
            self.play(*appear(slide.p2, shift=None), run_time=1.0)  # early: the slide's text, quoted
            c.wait_until("coming into")
            self.play(*recolor(slide.key, YELLOW), FlashUnder(slide.key, color=YELLOW, time_width=1.5), run_time=1.4)
            tpl = arc_template().move_to(_p(3.2, -2.55))
            self.tpl = tpl
            c.wait_until("of the state")
            self.play(*appear(tpl.a), run_time=1.0)
            c.wait_until("the condition")
            self.play(*appear(tpl.dot, tpl.b, lag=0.2), run_time=1.0)

    # ------------------------------------------------------------ c6.arcs.2
    def clip2(self):
        d, tpl = self.d, self.tpl
        with self.say("c6.arcs.2") as c:
            self.play(*during(disappear(self.slide), 0, 0.45),
                      *during([tpl.animate.move_to(_p(d.get_x(), -2.65))], 0.3, 0.9),
                      *during(look(d, "Sync", (), keep=("Sight",)), 0.4, 1.0),
                      run_time=min(2.0, c.until("three arcs")))
            c.wait_until("three arcs")
            b = LineBuild(built_line("D_2", ROW_Y[0]))
            self.play(*look(d, "Sync", INTO["Sync"], keep=("Sight",)), run_time=1.0)
            c.wait_until("a1")
            self.play(FlashAround(d.labels[6], time_width=1.5), run_time=1.0)
            c.wait_until("which gives")
            self.fly_term(b, 0, "Sight", 6, run_time=min(1.6, c.until("a2")), arcs=(0.8, 0.01))
            c.wait_until("a2")
            self.play(FlashAround(d.labels[0], time_width=1.5), run_time=1.0)
            c.wait_until("which gives", nth=1)
            self.fly_term(b, 1, None, None, run_time=min(1.5, c.until("a3")))
            c.wait_until("a3")
            self.play(FlashAround(d.labels[1], time_width=1.5), run_time=1.0)
            c.wait_until("gives ess two", nth=1)
            self.fly_term(b, 2, None, None, run_time=min(1.4, c.until("d2")))
            c.wait_until("d2")
            cap = T("For example, for FF 2:", 30).next_to(b.L, UP, buff=0.3).align_to(b.L, LEFT)
            self.cap = cap
            L2 = self.join(b, c, extra=during(appear(cap), 0.3, 1.0))
            s3 = built_line("D_2", ROW_Y[1])
            tick = check_mark().next_to(s3.tex, RIGHT, buff=0.3)
            self.play(*appear(s3, shift=0.6 * LEFT), run_time=1.0)
            self.play(*appear(tick, shift=None), run_time=0.6)
            self.L, self.s3, self.ticks = [L2], s3, [tick]

    # ------------------------------------------------------------ c6.arcs.3
    def clip3(self):
        d = self.d
        with self.say("c6.arcs.3") as c:
            tick = self.ticks[0]
            pulses = [VShowPassingFlash(d.arcs[i].copy().set_stroke(GOLD, 8), time_width=0.5) for i in (0, 1)]
            self.play(*pulses, *flash([d.labels[0], d.labels[1]], color=GOLD), run_time=1.6)
            c.wait_until("has an arc")
            self.play(*during(disappear(self.cap, self.s3), 0, 0.45),
                      *during([tick.animate.next_to(self.L[0].tex, RIGHT, buff=0.3)], 0.3, 1.0),
                      run_time=1.2)

            c.wait_until("sight")
            b = LineBuild(built_line("D_1", ROW_Y[1]))
            self.play(*look(d, "Sight", INTO["Sight"], keep=("Hunt",)), run_time=1.2)
            c.wait_until("from hunt")
            self.fly_term(b, 0, "Hunt", 4, run_time=min(1.5, c.until("sights own loop")), arcs=(0.01, 0.4))
            c.wait_until("sights own loop")
            self.fly_term(b, 1, None, None, run_time=min(1.4, c.until("d1")), extra=[FlashAround(d.labels[5], time_width=1.5)])
            c.wait_until("d1")
            s3 = built_line("D_1", ROW_Y[2])
            tick = check_mark().next_to(s3.tex, RIGHT, buff=0.3)
            L1 = self.join(b, c, extra=during(appear(s3, shift=0.6 * LEFT), 0.4, 1.0), run_time=1.4)
            self.play(*appear(tick, shift=None), run_time=0.6)
            self.L.append(L1)
            self.ticks.append(tick)

            c.wait_until("hunt")
            b = LineBuild(built_line("D_0", ROW_Y[2]))
            self.play(*look(d, "Hunt", INTO["Hunt"], keep=("Sight", "Sync")), run_time=1.0)
            c.wait_until("its own loop")
            self.play(*during(disappear(s3), 0, 0.45),
                      *during([tick.animate.next_to(L1.tex, RIGHT, buff=0.3)], 0.3, 1.0),
                      run_time=0.9)
            self.fly_term(b, 0, None, None, run_time=min(1.4, c.until("from sight")))
            c.wait_until("from sight")
            self.fly_term(b, 1, "Sight", 7, run_time=min(1.1, c.until("from sync")), arcs=(-1.0, -0.3))
            c.wait_until("from sync")
            self.fly_term(b, 2, None, None, run_time=min(1.2, c.until("d0")))
            c.wait_until("d0")
            s3 = built_line("D_0", ROW_Y[3])
            tick = check_mark().next_to(s3.tex, RIGHT, buff=0.3)
            L0 = self.join(b, c, extra=during(appear(s3, shift=0.6 * LEFT), 0.4, 1.0), run_time=1.3)
            self.play(*appear(tick, shift=None), run_time=0.6)
            self.L.append(L0)
            self.ticks.append(tick)
            self.s3 = s3

    # ------------------------------------------------------------ c6.arcs.4
    def clip4(self):
        d = self.d
        L2, L1, L0 = self.L
        with self.say("c6.arcs.4") as c:
            tick = self.ticks[2]
            self.play(*during(disappear(self.s3, self.tpl), 0, 0.45),
                      *during([tick.animate.next_to(L0.tex, RIGHT, buff=0.3)], 0.3, 1.0),
                      *during(look(d), 0.3, 1.0),
                      run_time=1.4)
            c.wait_until("the hot")
            units = small_ffs()
            items = []
            for u in units:
                items += [u.ff, u.out, u.tag]
            self.play(*appear(*items, lag=0.1), run_time=1.4)
            bits = [S2.ff_bit(u.ff, v, size=30) for u, v in zip(units, "001")]
            A, B, C = (D3.CENTRES[n] for n in STATES)
            p4 = ArcBetweenPoints(B + R_BIG * S2._dir(251), C + R_BIG * S2._dir(21), angle=-0.5)
            place_more(p4.scale(S2.DIAG_SCALE, about_point=ORIGIN).shift(S2.LEFT_SHIFT))
            dot = Dot(p4.get_start(), radius=0.1, color=YELLOW)
            self.play(*appear(*bits, shift=None), FadeIn(dot, scale=0.5), *look(d, "Hunt", [4]), run_time=1.0)
            c.wait_until("the arcs condition")
            self.play(FlashAround(d.labels[4], time_width=1.5), run_time=1.2)

            c.wait_until("lands")
            one = bits[2]
            term_box = SurroundingRectangle(VGroup(*[p.copy() for p in L1.terms[0]]), buff=0.1)
            new0 = S2.ff_bit(units[2].ff, "0", size=30)
            self.play(MoveAlongPath(dot, p4),
                      *during(look(d, "Sight", [4]), 0.5, 1.0),
                      *during(disappear(bits[1]), 0, 0.3),
                      *during([MoveAlongPath(one, centred_hop(units[2].ff, units[1].ff))], 0.2, 0.85),
                      *during(appear(new0, shift=None), 0.7, 1.0),
                      FlashAround(term_box, time_width=1.5, color=YELLOW),
                      run_time=2.0)
            self.wait(0.3)

            c.wait_until("seq")
            inset = big_diagram(S5.SYNC_CODES)
            for n in STATES:
                inset.name[n].scale(NAME_GROW)
            inset.scale(1.1).move_to(_p(3.4, 0.95))
            head = T("Part 5", 30, DIM).next_to(inset, UP, buff=0.2)
            stack = [*self.L, *self.ticks]
            self.play(*during(disappear(*stack), 0, 0.45),
                      *during(appear(head, inset, shift=None), 0.5, 1.0),  # early: the Part 5 inset shown whole
                      run_time=1.6)
            c.wait_until("hunt is zero")
            binary = S3.eq_line(None, [r"\overline{s_1}", r"\overline{s_0}"], size=60, tags=False).tex
            binary.move_to(_p(3.3, FF_Y))
            self.play(FlashAround(inset.code["Hunt"], color=GOLD, time_width=1.5), run_time=1.0)
            self.play(*appear(binary), run_time=1.0)
            c.wait_until("spell out")
            full = S3.eq_line(None, [r"\overline{s_1}", r"\overline{s_0}", "r"], size=60, tags=False).tex
            full.move_to(_p(3.3, FF_Y))
            self.play(*edit(binary, full), run_time=min(1.5, c.until("onehot")))

            c.wait_until("onehot")
            lines = []
            for n, u in zip(("Sync", "Sight", "Hunt"), units):
                top = u.ff.box.get_top()
                cc = d.circle[n].get_center()
                r = d.circle[n].width / 2
                v = top - cc
                start = cc + r * v / np.linalg.norm(v)
                if n == "Sight":
                    a = np.deg2rad(330)
                    start = cc + r * np.array([np.cos(a), np.sin(a), 0])
                lines.append(Line(start, top).set_stroke(GREEN, 3))
            self.play(*during(disappear(head, inset), 0, 0.45),
                      *during([Create(ln) for ln in lines], 0.3, 1.0),
                      run_time=1.6)
            c.wait_until("arcs turn")
            one_hot = S3.eq_line(None, ["s_0", "r"], size=60, tags=False).tex
            one_hot.move_to(_p(3.3, FF_Y))
            self.play(*edit(full, one_hot), run_time=min(1.5, c.until(floor=0.8)))


def S2_glow(d, name):
    return [S2.glow_state(d, name)]
