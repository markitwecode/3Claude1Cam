"""Chapter 5, scene 4: Bacon numbers, the allShortestPaths query, its histogram. Clips c5.bacon.1 – c5.bacon.6.

Shared drawing (imported by ch5 s8 and ch6 s1):
  bacon_histogram(max_h=4.6, pitch=1.25, bar_w=0.9, value_size=28, tick_size=30, with_xlabel=True) -> VGroup
      eight GOLD bars (Slide 109: 107, 3,519, 8,631, 1,676, 364, 212, 62, 9), baseline on y=0, centred on x=0;
      .bars .values (GOLD counts above the bars) .ticks (DIM 1..8) .axis .xlabel ("Bacon number", or None)
  BACON_COUNTS  -> the eight counts
"""
# style: 2
import random
import sys
from math import tau
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch5_s2_bfs")
ripple_rings, vertex, sp_code = S2.ripple_rings, S2.vertex, S2.sp_code
legend_row = S2.legend_row

BACON_COUNTS = [107, 3519, 8631, 1676, 364, 212, 62, 9]


def bacon_histogram(max_h=4.6, pitch=1.25, bar_w=0.9, value_size=28, tick_size=30, with_xlabel=True):
    """Slide 109's result as a histogram: Bacon number 1..8 against people. Baseline on y=0, centred on x=0."""
    g = VGroup()
    top = max(BACON_COUNTS)
    xs = [(k - 4.5) * pitch for k in range(1, 9)]
    g.bars, g.values, g.ticks = [], [], []
    for x, v in zip(xs, BACON_COUNTS):
        h = max(0.04, max_h * v / top)
        bar = Rectangle(width=bar_w, height=h).set_stroke(width=0).set_fill(GOLD, 0.85)
        bar.move_to((x, h / 2, 0))
        lab = T(f"{v:,}", size=value_size, color=GOLD).next_to(bar, UP, buff=0.12)
        g.bars.append(bar)
        g.values.append(lab)
    for k, x in enumerate(xs, 1):
        g.ticks.append(T(str(k), size=tick_size, color=DIM).move_to((x, -0.35, 0)))
    g.axis = Line((xs[0] - 0.75 * pitch, 0, 0), (xs[-1] + 0.75 * pitch, 0, 0)).set_stroke(DIM, 2)
    g.xlabel = None
    g.add(g.axis, *g.bars, *g.values, *g.ticks)
    if with_xlabel:
        g.xlabel = T("Bacon number", size=tick_size, color=DIM).move_to((0, -0.85, 0))
        g.add(g.xlabel)
    return g


# ---------------------------------------------------------------- local drawings

def q_code(fn="shortestPath", a="a", aname="Jennifer Lawrence", b="b", bname="Daniel Radcliffe",
           where=False, ret=("RETURN path;",), size=30):
    """The query at each stage of its edit from Slide 108 into Slide 109."""
    end = f"        ({b}:Person {{name: '{bname}'}}))" if bname else f"        ({b}:Person))"
    lines = [f"MATCH path = {fn}(",
             f"        ({a}:Person {{name: '{aname}'}})",
             "        -[:ACTED_IN*]-",
             end]
    if where:
        lines.append("WHERE p.person_id <> kb.person_id")
    lines += list(ret)
    code = Code("\n".join(lines), size=size)
    code.find(fn + "(", line=0).set_color(YELLOW)
    code.find(")", line=3, nth=1).set_color(YELLOW)
    return code


def swap_tokens(old, new, pairs, line):
    """Rewrite `old` into `new` where only whole tokens on one line change: each old token fades out
    whole, the unchanged glyphs slide to their new places, then each new token fades in whole."""
    gone = {id(g) for o, _ in pairs for g in old.find(o, line=line)}
    come = {id(g) for _, n in pairs for g in new.find(n, line=line)}
    og = [g for g in old.text if id(g) not in gone]
    ng = [g for g in new.text if id(g) not in come]
    assert len(og) == len(ng), (len(og), len(ng))
    out = [FadeOut(g) for g in old.text if id(g) in gone]
    mv = [g.animate.move_to(n.get_center()) for g, n in zip(og, ng)
          if np.linalg.norm(g.get_center() - n.get_center()) > 1e-3]
    inn = [FadeIn(g) for g in new.text if id(g) in come]
    return [*during(out, 0.0, 0.4), *during(mv, 0.4, 0.7), *during(inn, 0.68, 1.0)]



RET_FINAL = ("RETURN length(path) / 2 AS bacon_number,",
             "       count(DISTINCT p.person_id) AS people",
             "ORDER BY bacon_number;")


def paper_icon(w=0.13, h=0.17, color=BLUE):
    sheet = Rectangle(width=w, height=h).set_stroke(color, 1.5).set_fill(BG, 1)
    lines = VGroup(*[Line(LEFT * w * 0.3, RIGHT * w * 0.3).set_stroke(color, 1).shift(UP * h * (0.2 - 0.2 * i))
                     for i in range(3)])
    return VGroup(sheet, lines.move_to(sheet))


def clock_icon(r=0.36):
    face = Circle(radius=r).set_stroke(FG, 3)
    hour = Line(ORIGIN, UP * r * 0.5).set_stroke(FG, 3)
    minute = Line(ORIGIN, RIGHT * r * 0.75).set_stroke(YELLOW, 3)
    g = VGroup(face, hour, minute)
    g.minute = minute
    return g


def parity_icon():
    """ch4 s3's side flip, small: person, movie, person, movie... zig-zagging between two rows."""
    top_y, bot_y = 0.35, -0.35
    xs = [i * 0.55 for i in range(6)]
    pts = [np.array([x, top_y if i % 2 == 0 else bot_y, 0]) for i, x in enumerate(xs)]
    zig = VMobject().set_points_as_corners(pts).set_stroke(FG, 2.5)
    nodes = VGroup(*[vertex(PINK if i % 2 == 0 else BLUE, r=0.12).move_to(p) for i, p in enumerate(pts)])
    lp = T("person", size=28, color=PINK).next_to(nodes[0], LEFT, buff=0.25)
    lm = T("movie", size=28, color=BLUE).move_to((0, bot_y, 0)).align_to(lp, RIGHT)
    g = VGroup(zig, nodes, lp, lm)
    return g


def converging_paths(kb_pt, target_pt, n_paths=8, seed=5):
    """Kevin Bacon -> film -> person -> film -> person -> film -> one ring-3 person, many YELLOW routes."""
    rnd = random.Random(seed)
    cols = 5
    xs = [kb_pt[0] + (target_pt[0] - kb_pt[0]) * (i + 1) / (cols + 1) for i in range(cols)]
    ys = [kb_pt[1] + 0.62, kb_pt[1], kb_pt[1] - 0.62]
    nodes = [[np.array([x, y, 0]) for y in ys] for x in xs]
    routes = set()
    while len(routes) < n_paths:
        routes.add(tuple(rnd.randrange(3) for _ in range(cols)))
    paths = VGroup()
    for r in sorted(routes):
        pts = [kb_pt] + [nodes[i][j] for i, j in enumerate(r)] + [target_pt]
        paths.add(VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 2.5, opacity=0.8))
    dots = VGroup(*[Dot(p, radius=0.07, color=BLUE if i % 2 == 0 else PINK).set_z_index(1)
                    for i, col in enumerate(nodes) for p in col])
    kb = vertex(PINK, r=0.2).move_to(kb_pt).set_z_index(2)
    tgt = Dot(target_pt, radius=0.13, color=PINK).set_z_index(2)
    g = VGroup(paths, dots, kb, tgt)
    g.paths, g.dots, g.kb, g.tgt = paths, dots, kb, tgt
    return g


def join_box(size=28):
    t = Mono("has_position", size=size, color=FG)
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.35, height=t.height + 0.4).set_stroke(BLUE, 2.5)
    return VGroup(box, t.move_to(box))


# ---------------------------------------------------------------- scene

RC = np.array([-1.6, -0.35, 0])           # the big rings' centre
RS = 1.25                                 # their scale
CORNER = np.array([5.75, 2.85, 0])        # where they shrink to
CS = 0.38                                 # corner scale (absolute)
HIST_SHIFT = np.array([0.4, -2.4, 0])     # the histogram's baseline centre


class BaconNumbers(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c5.bacon.1: the game, rings round Kevin Bacon, Erdős
    def clip1(self):
        rings = ripple_rings(RC, scale=RS)
        self.rings = rings
        # legend bottom-left, clear of the rings (as s2 does for Lawrence)
        icon0, name0 = legend_row(vertex(PINK, 0.12), "Kevin Bacon", -3.3, x=-6.35)
        name = VGroup(icon0, name0)

        def num(k, r):
            a = tau * 0.36
            p = RC + RS * r * np.array([np.cos(a), np.sin(a), 0])
            return set_backstroke(T(str(k), size=42, color=GOLD).move_to(p))

        n0, n1, n2 = num(0, 0.47), num(1, 1.56), num(2, 2.55)

        # Erdős inset
        ic = np.array([4.75, -0.3, 0])
        frame = RoundedRectangle(corner_radius=0.2, width=3.6, height=4.1).set_stroke(DIM, 2).move_to(ic)
        title = T("Erdős number", size=32, color=DIM).move_to(ic + UP * 1.62)
        erings = ripple_rings(ic + DOWN * 0.05, scale=0.52, seed=3)
        erings.remove(erings.films)
        papers = VGroup(*[paper_icon().move_to(ic + DOWN * 0.05 + 0.39 * np.array([np.cos(tau * i / 10 + 0.3),
                                                                                    np.sin(tau * i / 10 + 0.3), 0]))
                          for i in range(10)])
        erings.add(papers)
        erings.set_opacity(0.7)
        cap = T("papers, not films", size=28, color=DIM).move_to(ic + DOWN * 1.62)
        question = T("How many actors have each Bacon number?", size=40).move_to((0, 3.35, 0))

        with self.say("c5.bacon.1") as c:
            self.play(GrowFromCenter(rings.centre_dot), *appear(name), run_time=1.2)
            c.wait_until("zero")
            self.play(*appear(n0), run_time=1.0)
            c.wait_until("one")
            self.play(FadeIn(rings.films, lag_ratio=0.05),
                      FadeIn(rings.ring1, lag_ratio=0.03), *appear(n1), run_time=1.8)
            c.wait_until("two")
            self.play(FadeIn(rings.ring2, lag_ratio=0.01), *appear(n2), run_time=2.0)
            settle(self, rings)
            c.wait_until("erdos")
            self.play(FadeIn(frame), *appear(title), run_time=1.0)
            self.play(FadeIn(erings, lag_ratio=0.01), run_time=1.6)
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("ask")
            self.play(*appear(question), run_time=1.0)
        self.big = VGroup(name, n0, n1, n2)

    # ---- c5.bacon.2: build the query from shortestPath
    def clip2(self):
        rings = self.rings
        code = sp_code(size=30)
        code.to_corner(UL, buff=0.6).shift(RIGHT * 0.05)
        ul = code.get_corner(UL)

        def place(m):
            return m.move_to(ul, aligned_edge=UL)

        s1 = place(q_code(a="kb", aname="Kevin Bacon"))
        s2 = place(q_code(a="kb", aname="Kevin Bacon", b="p", bname=None))
        s3 = place(q_code("allShortestPaths", a="kb", aname="Kevin Bacon", b="p", bname=None))
        s4 = place(q_code("allShortestPaths", a="kb", aname="Kevin Bacon", b="p", bname=None, where=True))
        note = T("same table without it (Traverse)", size=28, color=DIM)
        note.next_to(s4.line(3), RIGHT, buff=0.7).align_to(s4.line(3), DOWN)
        f = CS / RS

        with self.say("c5.bacon.2") as c:
            sweep_clear(self, *during([rings.animate.scale(f, about_point=RC).shift(CORNER - RC)], 0.0, 0.6),
                        *during(appear(code, shift=None), 0.55, 1.0),
                        keep=[rings], run_time=min(2.2, c.until("kevin")))
            c.wait_until("kevin")
            self.play(*swap_tokens(code, s1, [("a", "kb"), ("Jennifer Lawrence", "Kevin Bacon")], line=1),
                      run_time=1.5)
            self.remove(*code.get_family(), *s1.get_family())
            self.add(s1)
            c.wait_until("any")
            self.play(*edit(s1, s2), run_time=1.5)
            c.wait_until("allsp")
            self.play(*edit(s2, s3), run_time=1.5)
            c.wait_until("where")
            self.play(*edit(s3, s4), run_time=1.5)
            c.wait_until("without")
            self.play(*appear(note), run_time=1.0)
        self.code, self.note, self.ul = s4, note, ul

    # ---- c5.bacon.3: length(path) / 2
    def clip3(self):
        code = self.code
        s5 = q_code("allShortestPaths", a="kb", aname="Kevin Bacon", b="p", bname=None, where=True,
                    ret=RET_FINAL[:1]).move_to(self.ul, aligned_edge=UL)

        # mini chain
        cy = -1.85
        pts = [np.array([-5.0 + 2.3 * i, cy, 0]) for i in range(3)]
        nodes = [vertex(col, r=0.24).move_to(p).set_z_index(1) for col, p in zip((PINK, BLUE, PINK), pts)]
        edges = [Line(pts[i], pts[i + 1], buff=0.24).set_stroke(FG, 3) for i in range(2)]
        labs = [T(s, size=28, color=col).next_to(n, UP, buff=0.18)
                for s, col, n in zip(("Kevin Bacon", "movie", "co-star"), (PINK, BLUE, PINK), nodes)]
        brace = span_brace(pts[0], pts[2], DOWN, color=GOLD, buff=0.38)
        btxt = T("2 edges = 1 film", size=32, color=GOLD).next_to(brace, DOWN, buff=0.12)
        par = parity_icon().move_to((3.3, -2.15, 0))

        with self.say("c5.bacon.3") as c:
            self.play(*edit(code, s5), run_time=1.5)
            box = token_box(s5.find("length(path) / 2"), s5.line(5))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("half")
            self.play(GrowFromCenter(nodes[0]), *appear(labs[0]), Create(edges[0]), GrowFromCenter(nodes[1]),
                      Create(edges[1]), GrowFromCenter(nodes[2]), *appear(labs[2]), run_time=1.6)
            c.wait_until(own_word=labs[1])
            self.play(*appear(labs[1]), run_time=0.8)
            self.play(GrowFromCenter(brace), *appear(btxt), run_time=1.0)
            c.wait_until("parity")
            self.play(Create(par[0]), FadeIn(par[1], lag_ratio=0.2), *appear(par[2], par[3], shift=None),
                      run_time=1.6)
            c.wait_until("So the Bacon number")
            self.play(FlashAround(s5.find("length(path) / 2"), run_time=1.5, time_width=1.5), run_time=1.5)
        self.code, self.box = s5, box
        self.chain = VGroup(*edges, *nodes, *labs, brace, btxt)
        self.par = par

    # ---- c5.bacon.4: count(DISTINCT p.person_id)
    def clip4(self):
        code, box = self.code, self.box
        s6 = q_code("allShortestPaths", a="kb", aname="Kevin Bacon", b="p", bname=None, where=True,
                    ret=RET_FINAL).move_to(self.ul, aligned_edge=UL)
        cnt = s6.find("count(DISTINCT p.person_id)")
        why = T("why not just count rows?", size=34, color=YELLOW)

        conv = converging_paths(np.array([-5.15, -2.3, 0]), np.array([-1.2, -2.3, 0]))
        kbl = T("Kevin\nBacon", size=28, color=PINK, line_spacing=0.8).next_to(conv.kb, LEFT, buff=0.2)
        r3 = T("ring 3", size=28, color=PINK).next_to(conv.tgt, RIGHT, buff=0.2)
        people = T("8,631 people", size=34, color=GOLD)
        paths = T("111,342 shortest paths", size=34, color=GOLD)
        people.move_to((1.9, -1.95, 0), aligned_edge=LEFT)
        paths.move_to((1.9, -2.95, 0), aligned_edge=LEFT)
        why.move_to((0.6, -2.45, 0), aligned_edge=LEFT)

        def row(src, txt, col, y, ref):
            m = Mono(src, size=28)
            t = T(txt, size=32, color=col).next_to(m, RIGHT, buff=0.2)
            g = VGroup(m, t)
            g.move_to((1.4, y, 0), aligned_edge=RIGHT)
            t.align_to(ref, DOWN)
            m.match_y(t)
            return g

        rp = row("count(DISTINCT p.person_id)", "= people", GREEN, -1.95, people)
        rr = row("count(*)", "= paths", RED, -2.95, paths)

        bn = s6.find("bacon_number", line=5)
        gbox = token_box(bn, s6.line(5), color=GREEN)
        glab = T("grouping key", size=30, color=GREEN).next_to(s6.line(5), RIGHT, buff=0.45)

        with self.say("c5.bacon.4") as c:
            self.play(*disappear(self.chain, self.par, self.note), FadeOut(box), run_time=0.7)
            self.play(*edit(code, s6), run_time=1.4)
            box = token_box(cnt, s6.line(6))
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("why")
            self.play(*appear(why), run_time=1.0)
            c.wait_until("every")
            self.play(Create(conv.paths, lag_ratio=0.15), FadeIn(conv.dots), GrowFromCenter(conv.kb),
                      GrowFromCenter(conv.tgt), *appear(kbl, r3, shift=None), run_time=2.0)
            c.wait_until("three")
            self.play(*swap(why, people), FlashAround(conv.tgt, color=PINK), run_time=1.2)
            c.wait_until("hundred and eleven thousand")
            self.play(*appear(paths), *[VShowPassingFlash(p.copy().set_stroke(YELLOW, 6), time_width=0.4)
                                        for p in conv.paths], run_time=1.5)
            c.wait_until("rows")
            self.play(*disappear(conv, kbl, r3), run_time=0.7)
            self.play(*appear(rr, rp, lag=0.4, shift=None), run_time=1.4)
            c.wait_until("group")
            self.play(FadeOut(box), FadeIn(gbox), *appear(glab, shift=None), run_time=1.2)

    # ---- c5.bacon.5: run it; the histogram
    def clip5(self):
        rings = self.rings
        hist = bacon_histogram().shift(HIST_SHIFT)
        self.hist = hist
        clock = clock_icon().move_to((-5.8, 3.05, 0))
        ctxt = T("≈ 1 minute", size=32).next_to(clock, RIGHT, buff=0.3)
        self.clock = VGroup(clock, ctxt)

        def bar(k, rt=1.0):
            b = hist.bars[k]
            return [GrowFromEdge(b, DOWN), *during(appear(hist.values[k], shift=None), 0.5, 1.0)]

        with self.say("c5.bacon.5") as c:
            c.wait_until("minute")
            sweep_clear(self, *appear(clock, ctxt, lag=0.3, shift=None), keep=[rings],
                        run_time=min(1.4, c.until("table")))
            c.wait_until("table")
            self.play(Create(hist.axis), *appear(*hist.ticks, hist.xlabel, lag=0.05, shift=None),
                      Rotate(clock.minute, angle=-tau, about_point=clock[0].get_center(), rate_func=linear),
                      run_time=1.0)
            c.wait_until("low")
            self.play(*bar(0), run_time=1.2)
            c.wait_until("three thousand")
            self.play(*bar(1), run_time=1.4)
            c.wait_until("peak")
            self.play(*bar(2), run_time=1.8)
            c.wait_until("tail")
            self.play(LaggedStart(*[AnimationGroup(*bar(k)) for k in range(3, 8)], lag_ratio=0.3), run_time=2.4)
            settle(self, hist)
            c.wait_until("ripples")
            centre = rings.centre_dot.get_center()
            srcs = [rings.ring1, rings.ring2] + [
                Circle(radius=rings.ring2.width / 2 * (1 + 0.1 * (k - 1))).set_stroke(PINK, 2, opacity=0.6)
                .move_to(centre)
                for k in range(2, 8)]
            T_all = min(2.8, c.until() - 0.2)
            fly_d, flash_d = 0.9, 0.8
            step = max(0.05, (T_all - fly_d - flash_d) / 7)
            anims, copies = [], []
            for k, s in enumerate(srcs):
                cp = s.copy()
                b = hist.bars[k]
                dst = b.get_top()
                t0 = k * step
                anims.append(time_span(cp.animate(rate_func=smooth).scale(0.12).move_to(dst).set_opacity(0),
                                       t0, t0 + fly_d))
                anims.append(time_span(FlashAround(VGroup(b, hist.values[k]), color=YELLOW, time_width=1.5), t0 + fly_d - 0.1,
                                       t0 + fly_d - 0.1 + flash_d))
                copies.append(cp)
            self.add(*copies[:2])   # copies of the on-screen rings; the outer ones are new outlines
            self.play(*anims, run_time=7 * step + fly_d - 0.1 + flash_d)
            self.remove(*copies)
            self.play(*[FlashAround(b, color=YELLOW, run_time=1.0) for b in hist.bars[:3]], run_time=1.0)

    # ---- c5.bacon.6: six degrees, the missing, two names, SQL
    def clip6(self):
        rings, hist = self.rings, self.hist
        x6 = (hist.bars[5].get_right()[0] + hist.bars[6].get_left()[0]) / 2
        base = hist.axis.get_y()
        divider = DashedLine((x6, base, 0), (x6, base + 1.9, 0), dash_length=0.12).set_stroke(YELLOW, 3)
        top78 = max(hist.values[6].get_top()[1], hist.values[7].get_top()[1])
        br = span_brace(hist.bars[6].get_left() * RIGHT + top78 * UP, hist.bars[7].get_right() * RIGHT + top78 * UP,
                        UP, color=GOLD, buff=0.12)
        n71 = T("71", size=36, color=GOLD).next_to(br, UP, buff=0.1)

        rnd = random.Random(11)
        cc = np.array([3.0, 1.15, 0])
        cl_dots = VGroup(*[Dot(cc + np.array([rnd.uniform(-0.55, 0.55), rnd.uniform(-0.35, 0.35), 0]),
                               radius=0.05, color=PINK).set_opacity(0.6) for _ in range(26)])
        cl_ring = DashedVMobject(Ellipse(width=1.6, height=1.05).set_stroke(DIM, 2).move_to(cc), num_dashes=24)
        cl_txt = T("892 actors: no chain", size=32, color=GOLD).next_to(cl_ring, DOWN, buff=0.15)

        def tag(a, b):
            g = VGroup(T(a, size=28), T(b, size=28, color=DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            return g

        tag1 = tag("Jennifer Lawrence", "X-Men: First Class")
        tag1.move_to((-6.55, hist.values[0].get_top()[1] + 0.25, 0), aligned_edge=DL)
        tag2 = tag("Daniel Radcliffe", "via Brad Pitt")
        tag2.move_to((-6.55, hist.values[1].get_top()[1] + 0.55, 0), aligned_edge=DL)
        lead2 = Line(tag2.get_right() + RIGHT * 0.1 + DOWN * 0.15, hist.values[1].get_top() + UP * 0.08 + LEFT * 0.15
                     ).set_stroke(DIM, 2)

        jb = [join_box() for _ in range(3)]
        joins = [MathTex(r"\bowtie", font_size=56, color=GOLD) for _ in range(3)]
        dots = T("…", size=40)
        chain = VGroup(jb[0], joins[0], jb[1], joins[1], jb[2], joins[2], dots).arrange(RIGHT, buff=0.25)
        chain.move_to((0, -0.35, 0))
        howmany = T("how many joins?", size=40, color=GOLD).next_to(chain, DOWN, buff=0.6)
        nxt = T("recursive queries: next lecture", size=32, color=DIM).move_to((0, -2.9, 0))

        with self.say("c5.bacon.6") as c:
            self.play(Create(divider), run_time=1.2)
            c.wait_until("seventy-one")
            self.play(GrowFromCenter(br), *appear(n71), run_time=1.2)
            c.wait_until("missing")
            self.play(*disappear(self.clock), run_time=0.6)
            self.play(FadeIn(cl_ring), FadeIn(cl_dots, lag_ratio=0.05), *appear(cl_txt), run_time=1.5)
            c.wait_until("Jennifer Lawrence")
            self.play(*appear(tag1[0], shift=None), run_time=0.8)
            c.wait_until(own_word=tag1[1])
            self.play(*appear(tag1[1], shift=None), run_time=0.8)
            c.wait_until("Daniel Radcliffe")
            self.play(Create(lead2), *appear(tag2[0], shift=None), run_time=0.8)
            c.wait_until("has two")
            self.play(*appear(tag2[1], shift=None), run_time=0.8)
            c.wait_until("sql")
            small = VGroup(hist.axis, *hist.bars, divider)
            self.play(*disappear(br, n71, lead2, *hist.values, *hist.ticks, hist.xlabel),
                      *during([small.animate.scale(0.5).move_to((-4.2, 2.6, 0))], 0.3, 1.0), run_time=1.6)
            self.play(*disappear(tag1, tag2, cl_ring, cl_dots, cl_txt), run_time=0.8)
            self.play(*appear(*chain, lag=0.45, shift=None), run_time=3.0)
            self.play(*appear(howmany), run_time=1.0)
            c.wait_until("next")
            self.play(*appear(nxt), run_time=1.0)
