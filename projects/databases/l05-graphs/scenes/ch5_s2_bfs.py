"""Chapter 5, scene 2: ripples from Lawrence, BFS, shortestPath / allShortestPaths. Clips c5.bfs.1 – c5.bfs.5.

Shared drawings (imported by ch5 s3, s4, s5, s8):
  ripple_rings(centre=ORIGIN, scale=1.0, seed=7) -> RippleRings   (.centre_dot .films .ring1 .ring2 .target)
  ghost_rings(rings, radii=(2.75, 3.25))          -> VGroup of DIM dashed circles round rings.centre_dot
  ripple_route(rings)                             -> VGroup(polyline YELLOW, via-film BLUE dot); .line .via
  lr_path(names=("Lawrence", None, None, None, "Radcliffe"), pitch=1.35, r=0.26, edge_color=FG, label_size=28)
                                                  -> VGroup; .nodes .edges .labels (five circles PINK BLUE PINK BLUE PINK)
  LR_NAMES                                        -> full names for lr_path(names=LR_NAMES, pitch=2.9)
  eight_fan()                                     -> ch4 s4's layered_paths() (dict parts .shapes .labels .edges),
                                                     plus lists .end_labels [L, R] and .name_labels [H, M, G]
  sp_code(fn="shortestPath", ret="RETURN path;", a="Jennifer Lawrence", b="Daniel Radcliffe", size=30) -> Code
"""
# style: 2
import random
import sys
from math import cos, log10, sin, tau
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

CH4_S4 = load_scene("ch4_s4_count8")     # layered_paths(): the eight paths
CH4_S5 = load_scene("ch4_s5_explode")    # paths_plot(): the two curves


# ---------------------------------------------------------------- shared drawings

def vertex(color, r=0.22, width=3):
    """The series' vertex: a circle, outline in its colour, a dark tint of it inside."""
    c = Circle(radius=r).set_stroke(color, width)
    c.set_fill(interpolate_color(ManimColor(BG), ManimColor(color), 0.3), 1)
    return c


class RippleRings(VGroup):
    pass


def _polar(c, r, a):
    return c + np.array([r * cos(a), r * sin(a), 0])


def ripple_rings(centre=ORIGIN, scale=1.0, seed=7):
    """Centre person (PINK), a ring of 17 BLUE film dots, ring 1 and a denser ring 2 of PINK dots.
    .target is the ring-2 dot at 30 degrees (Radcliffe in s2). Built at `centre`, then scaled."""
    rnd = random.Random(seed)
    c = np.array(ORIGIN, dtype=float)
    g = RippleRings()
    g.centre_dot = vertex(PINK, r=0.2)
    g.films = VGroup(*[Dot(_polar(c, 0.75, tau * i / 17 + 0.1), radius=0.06, color=BLUE) for i in range(17)])
    n1 = 40
    g.ring1 = VGroup(*[Dot(_polar(c, 1.3 + rnd.uniform(-0.07, 0.07), tau * (i + rnd.uniform(-0.3, 0.3)) / n1),
                           radius=0.045, color=PINK) for i in range(n1)])
    n2 = 120
    dots = []
    for i in range(n2):
        a = tau * (i + rnd.uniform(-0.4, 0.4)) / n2
        dots.append(Dot(_polar(c, rnd.uniform(1.8, 2.25), a), radius=0.038, color=PINK))
    g.target = Dot(_polar(c, 2.0, tau / 12), radius=0.05, color=PINK)
    # keep a clear spot round the target
    dots = [d for d in dots if np.linalg.norm(d.get_center() - g.target.get_center()) > 0.16]
    g.ring2 = VGroup(*dots, g.target)
    g.add(g.films, g.ring1, g.ring2, g.centre_dot)
    g.scale(scale, about_point=ORIGIN).shift(centre)
    return g


def ghost_rings(rings, radii=(2.75, 3.25)):
    s = rings.centre_dot.width / 0.4
    return VGroup(*[DashedVMobject(Circle(radius=r * s).set_stroke(DIM, 2, opacity=0.6), num_dashes=int(40 * r))
                    .move_to(rings.centre_dot) for r in radii])


def ripple_route(rings):
    """The YELLOW route centre -> film -> ring-1 person -> film -> target (rings.target)."""
    c = rings.centre_dot.get_center()
    s = rings.centre_dot.width / 0.4
    a = tau / 12
    film = rings.films[0].get_center()
    p1 = _polar(c, 1.3 * s, a - 0.15)
    via = _polar(c, 1.62 * s, a - 0.05)
    pts = [c, film, p1, via, rings.target.get_center()]
    line = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 4)
    viadot = Dot(via, radius=0.06 * s, color=BLUE)
    g = VGroup(line, viadot)
    g.line, g.via, g.points_ = line, viadot, pts
    return g


LR_NAMES = ("Jennifer\nLawrence", "Mother!", "Domhnall\nGleeson",
            "Harry Potter and the\nDeathly Hallows: Part 2", "Daniel\nRadcliffe")


def lr_path(names=("Lawrence", None, None, None, "Radcliffe"), pitch=1.35, r=0.26, edge_color=FG,
            label_size=28, above_films=False):
    """Five circles left to right, PINK BLUE PINK BLUE PINK, joined without arrowheads, centred on ORIGIN.
    Labels (where a name is given) sit under their circle."""
    g = VGroup()
    cols = [PINK, BLUE, PINK, BLUE, PINK]
    g.nodes = [vertex(col, r=r).move_to(((i - 2) * pitch, 0, 0)) for i, col in enumerate(cols)]
    for n in g.nodes:
        n.set_z_index(1)
    g.edges = [Line(g.nodes[i].get_center(), g.nodes[i + 1].get_center(), buff=r).set_stroke(edge_color, 3)
               for i in range(4)]
    g.labels = []
    for n_i, (n, name) in enumerate(zip(g.nodes, names)):
        if name:
            lab = T(name, size=label_size, line_spacing=0.8)
            lab.next_to(n, UP if (above_films and n_i % 2) else DOWN, buff=0.18)
            g.labels.append(lab)
        else:
            g.labels.append(None)
    g.add(*g.edges, *g.nodes, *[lab for lab in g.labels if lab is not None])
    return g


FAN_FILMS = {
    "Woody Harrelson": (["The Hunger Games: Catching Fire", "The Hunger Games: Mockingjay - Part 1",
                         "The Hunger Games: Mockingjay - Part 2"], "Now You See Me 2"),
    "James McAvoy": (["X-Men: First Class", "X-Men: Days of Future Past", "X-Men: Apocalypse",
                      "X-Men: Dark Phoenix"], "Victor Frankenstein"),
    "Domhnall Gleeson": (["Mother!"], "Harry Potter and the Deathly Hallows: Part 2"),
}


def eight_fan():
    """ch4 s4's layered drawing of the 8 Lawrence-Radcliffe paths (ch4_s4_count8.layered_paths()), frame-sized
    (~13.5 x 5.7). Parts as there: .shapes[k] .labels[k] (dicts; k in "L" "R" "H" "M" "G" or a film title),
    .edges[(a, b)], .paths, .group_keys. Added: .end_labels [L, R] and .name_labels [H, M, G] (lists of labels)."""
    g = CH4_S4.layered_paths()
    g.end_labels = [g.labels["L"], g.labels["R"]]
    g.name_labels = [g.labels[k] for k in ("H", "M", "G")]
    return g


def sp_code(fn="shortestPath", ret="RETURN path;", a="Jennifer Lawrence", b="Daniel Radcliffe", size=30):
    """Slide 108's query; `fn(` and its closing bracket YELLOW."""
    src = (f"MATCH path = {fn}(\n"
           f"        (a:Person {{name: '{a}'}})\n"
           f"        -[:ACTED_IN*]-\n"
           f"        (b:Person {{name: '{b}'}}))\n"
           f"{ret}")
    code = Code(src, size=size)
    code.find(fn + "(", line=0).set_color(YELLOW)
    code.find(")", line=3, nth=1).set_color(YELLOW)
    return code


# ---------------------------------------------------------------- scene

C = np.array([-3.4, -0.1, 0])


def CH5_PLOT():
    """ch4 s5's two curves (same axes and colours), without its ceiling line, scaled into the right half
    (x -3.9..5.4, y -3.2..2.85). "path length" sits at the x axis' right end to save height."""
    plot = CH4_S5.paths_plot()
    plot.remove(plot.ceiling, plot.ceiling_label)
    plot.x_label.next_to(plot.axes.x_axis.get_right(), RIGHT, buff=0.25)
    plot.scale(0.95)
    plot.shift((-3.9 - plot.get_left()[0]) * RIGHT + (2.85 - plot.get_top()[1]) * UP)
    return plot


def legend_row(icon, text, y, x=2.35, size=32, color=FG):
    icon.move_to((x, y, 0))
    t = T(text, size=size, color=color)
    t.next_to(icon, RIGHT, buff=0.25)
    return icon, t


class Ripples(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c5.bfs.1: the rings
    def clip1(self):
        rings = ripple_rings(C)
        self.rings = rings
        icon0, name0 = legend_row(vertex(PINK, 0.12), "Jennifer Lawrence", 2.8)
        icon1, films_t = legend_row(Dot(radius=0.07, color=BLUE), "17 films", 2.15)
        icon2, ring1_t = legend_row(Dot(radius=0.06, color=PINK), "ring 1", 1.5)
        icon3, ring2_t = legend_row(Dot(radius=0.06, color=PINK), "ring 2", 0.85)
        n1 = T("117", size=32, color=GOLD).move_to((5.15, 1.5, 0), aligned_edge=LEFT)
        n1.align_to(ring1_t, DOWN)
        n2 = T("+3,895", size=32, color=GOLD).move_to((5.15, 0.85, 0), aligned_edge=LEFT)
        n2.align_to(ring2_t, DOWN)
        n1.align_to(n2, LEFT)
        self.legend = VGroup(icon0, name0, icon1, films_t, icon2, ring1_t, icon3, ring2_t, n1, n2)

        with self.say("c5.bfs.1") as c:
            self.play(GrowFromCenter(rings.centre_dot), *appear(icon0, name0), run_time=1.2)
            c.wait_until("spread outwards")
            ripples = [Circle(radius=0.2).set_stroke(BLUE, 3).move_to(C) for _ in range(3)]

            def grow(m, a, base=None):
                m.become(Circle(radius=0.2 + 2.3 * a).set_stroke(BLUE, 3, opacity=1 - a).move_to(C))
            self.play(LaggedStart(*[UpdateFromAlphaFunc(r, grow) for r in ripples], lag_ratio=0.35),
                      run_time=min(3.5, c.until("ring1") - 0.2))
            self.remove(*ripples)
            c.wait_until("ring1")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in rings.films], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in rings.ring1], lag_ratio=0.03),
                      *appear(icon2, ring1_t), run_time=1.8)
            c.wait_until("one hundred")
            self.play(*appear(n1), run_time=1.0)
            c.wait_until(own_word=films_t)
            self.play(*appear(icon1, films_t), run_time=1.0)
            c.wait_until("ring2")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in rings.ring2], lag_ratio=0.012),
                      *appear(icon3, ring2_t), run_time=2.0)
            c.wait_until("three thousand")
            self.play(*appear(n2), run_time=1.0)
            c.wait_until("found")
            rad = set_backstroke(T("Daniel Radcliffe", size=30, color=YELLOW))
            rad.next_to(rings.target, RIGHT, buff=0.2)
            self.rad = rad
            self.play(rings.target.animate.set_color(YELLOW).scale(2.2), *appear(rad, shift=0.15 * LEFT),
                      run_time=1.0)
            route = ripple_route(rings)
            route.via.set_z_index(2)
            self.route = route
            self.play(Create(route.line), FadeIn(route.via), run_time=1.2)

    # ---- c5.bfs.2: four edges, stop early, join once
    def clip2(self):
        rings, route = self.rings, self.route
        path = lr_path(edge_color=YELLOW).move_to((3.0, -1.35, 0))
        straight = VMobject().set_points_as_corners([n.get_center() for n in path.nodes]).set_stroke(YELLOW, 4)
        edges_t = T("4 edges", size=34, color=GOLD).move_to((3.0, -0.55, 0))
        ghosts = ghost_rings(rings)
        seen = T("≤ 4,013 people seen", size=34, color=GOLD).move_to((3.0, -2.9, 0))

        with self.say("c5.bfs.2") as c:
            self.play(ReplacementTransform(route.line.copy(), straight), run_time=1.6)
            self.play(*[GrowFromCenter(n) for n in path.nodes], *appear(*[l for l in path.labels if l]),
                      run_time=1.0)
            self.remove(straight)
            self.add(*path.edges)
            c.wait_until("four edges")
            self.play(*appear(edges_t), *[VShowPassingFlash(e.copy().set_stroke(GOLD, 8), time_width=0.6)
                                          for e in path.edges], run_time=1.0)
            c.wait_until("stop")
            self.play(*[Create(g) for g in ghosts], *disappear(self.rad), run_time=1.5)
            c.wait_until("by then")
            self.play(*appear(seen), run_time=1.0)

            # zoom on one ring-2 dot
            c.wait_until("cheap")
            mag_dot = rings.ring2[0]
            for d in rings.ring2:
                if abs(d.get_y() - C[1]) < 0.12 and d.get_x() > C[0]:
                    mag_dot = d
            mag = Circle(radius=0.22).set_stroke(FG, 2).move_to(mag_dot)
            panel = RoundedRectangle(corner_radius=0.15, width=6.1, height=5.6).set_stroke(DIM, 2)
            panel.move_to((3.5, -0.1, 0))
            lines = VGroup(Line(mag.get_top(), panel.get_corner(UL) + 0.15 * RIGHT),
                           Line(mag.get_bottom(), panel.get_corner(DL) + 0.15 * RIGHT)).set_stroke(DIM, 1.5)
            ys = [-1.6, 0.0, 1.6]
            arcs = [ArcBetweenPoints((1.9, y, 0), (6.2, y, 0), angle=-0.3).set_stroke(PINK, 2, opacity=0.5)
                    for y in ys]
            ring_labels = [T(f"ring {i + 1}", size=28, color=DIM).next_to(a, LEFT, buff=0.2)
                           for i, a in enumerate(arcs)]
            arc_dots = []
            for a in arcs:
                for p in (0.08, 0.3, 0.55, 0.78, 0.95):
                    arc_dots.append(Dot(a.point_from_proportion(p), radius=0.07, color=PINK))
            target = vertex(PINK, 0.16).move_to(arcs[1].point_from_proportion(0.42)).set_z_index(1)
            src1 = arcs[0].point_from_proportion(0.18)
            src3 = arcs[2].point_from_proportion(0.68)
            arc_dots += [Dot(src1, radius=0.07, color=PINK), Dot(src3, radius=0.07, color=PINK)]
            c.wait_until("full search")
            self.play(*disappear(path, edges_t, seen, self.legend), run_time=0.9)
            self.play(Create(mag), *[Create(l) for l in lines], FadeIn(panel), run_time=1.0)
            self.play(*[Create(a) for a in arcs], *appear(*ring_labels, lag=0.1),
                      LaggedStart(*[FadeIn(d) for d in arc_dots], lag_ratio=0.03), run_time=1.2)  # early: the zoom's ring scale, read with the arrows

            c.wait_until("once")
            self.play(GrowFromCenter(target), run_time=0.8)
            a1 = Arrow(src1, target.get_center(), buff=0.2, stroke_width=5, color=GREEN)
            kept = T("first: kept", size=30, color=GREEN).move_to((4.9, -0.85, 0))
            self.play(GrowArrow(a1), run_time=1.2)
            self.play(*appear(kept), target.animate.set_stroke(GREEN), run_time=1.0)

            c.wait_until("later")
            a2 = Arrow(src3, target.get_center(), buff=0.2, stroke_width=5, color=FG)
            ign = T("longer: ignored", size=30, color=DIM).move_to((2.8, 0.85, 0))
            self.play(GrowArrow(a2), run_time=1.2)
            x = cross_mark().scale(0.8).move_to(a2.point_from_proportion(0.5))
            self.play(a2.animate.set_color(DIM).set_opacity(0.5), GrowFromCenter(x), *appear(ign), run_time=1.2)
            self.zoom = VGroup(mag, lines, panel, *arcs, *ring_labels, *arc_dots, target, a1, a2, x, kept, ign)
            self.ghosts = ghosts

    # ---- c5.bfs.3: the two curves (ch4 s5's plot), BFS
    def clip3(self):
        rings, route = self.rings, self.route
        plot = CH5_PLOT()
        frame_parts = [plot.axes, plot.yticks, plot.xticks, plot.log_label, plot.x_label]
        pval = T("≈ 39.6 million", size=30, color=GOLD).next_to(plot.gold_label, DOWN, buff=0.18, aligned_edge=LEFT)
        qval = T("14,072", size=30, color=PINK).next_to(plot.pink_dots[-1], RIGHT, buff=0.22)
        title = T("breadth-first search", size=48, color=YELLOW).move_to((-1.0, 3.4, 0))
        tag = T("Algorithms course", size=28, color=DIM).next_to(title, RIGHT, buff=0.6).align_to(title, DOWN)

        with self.say("c5.bfs.3") as c:
            dst = np.array([-5.3, 0.2, 0])
            sweep_clear(self, rings.animate.scale(0.5, about_point=C).shift(dst - C),  # early: the axes' labels frame both curves
                        route.animate.scale(0.5, about_point=C).shift(dst - C),
                        Create(plot.axes), *appear(plot.yticks, plot.xticks, plot.log_label, plot.x_label, lag=0.1),
                        keep=[rings, route], run_time=min(2.0, c.until("paths")))
            c.wait_until("paths")
            self.play(Create(plot.gold_curve), LaggedStart(*[FadeIn(d) for d in plot.gold_dots], lag_ratio=0.3),
                      run_time=2.0)
            self.play(*appear(plot.gold_label), run_time=0.8)
            c.wait_until("forty million")
            self.play(*appear(pval), run_time=1.0)
            c.wait_until("people")
            self.play(Create(plot.pink_curve), LaggedStart(*[FadeIn(d) for d in plot.pink_dots], lag_ratio=0.3),
                      *appear(plot.pink_label), run_time=2.0)
            c.wait_until("fifteen thousand")
            self.play(*appear(qval), run_time=1.0)
            c.wait_until("ripples")
            mk = Dot(plot.pink_dots[0].get_center(), radius=0.13, color=YELLOW).set_z_index(3)
            self.play(FadeIn(mk, scale=0.5), FlashAround(rings, color=YELLOW, run_time=1.0), run_time=0.8)
            self.play(MoveAlongPath(mk, plot.pink_curve.copy()), run_time=min(3.5, c.until("work") - 0.3),
                      rate_func=linear)
            c.wait_until("work")
            self.play(*set_alpha([plot.gold_curve, plot.gold_dots, plot.gold_label, pval], DIMMED), run_time=1.0)
            self.play(FlashUnder(plot.pink_curve, color=PINK, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("name")
            self.play(*appear(title), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)

    # ---- c5.bfs.4: shortestPath in Cypher
    def clip4(self):
        code = sp_code()
        code.to_edge(UP, buff=0.55)
        self.code = code
        star = code.find("*", line=2)
        anylen = T("any length", size=30, color=YELLOW).next_to(code.line(2), RIGHT, buff=0.5)
        path = lr_path(names=LR_NAMES, pitch=2.9, r=0.3, above_films=True)
        path.shift((-1.8 - path.nodes[0].get_y()) * UP - path.nodes[2].get_x() * RIGHT)
        self.path, self.anylen = path, anylen

        with self.say("c5.bfs.4") as c:
            sweep_clear(self, *appear(code), run_time=min(1.8, c.until("function") - 0.1))
            c.wait_until("shortest path")
            self.play(FlashAround(code.find("shortestPath(", line=0), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("star")
            self.play(FlashAround(star, run_time=1.5, time_width=1.5), *appear(anylen, shift=0.2 * LEFT), run_time=1.5)
            c.wait_until("one")
            items = []
            for i, n in enumerate(path.nodes):
                items.append(GrowFromCenter(n))
                if path.labels[i] is not None:
                    items.append(FadeIn(path.labels[i], shift=0.15 * DOWN))
                if i < 4:
                    items.append(Create(path.edges[i]))
            self.play(LaggedStart(*items, lag_ratio=0.25), run_time=1.8)  # early: the path shown whole, then walked name by name
            cues = ["route", "Mother", "Gleeson", "Harry Potter", "Daniel Radcliffe"]
            for i, cue in enumerate(cues):
                c.wait_until(cue)
                anims = [path.nodes[i].animate.set_stroke(YELLOW, 5)]
                if i > 0:
                    anims.append(path.edges[i - 1].animate.set_stroke(YELLOW, 5))
                self.play(*anims, run_time=0.7)

    # ---- c5.bfs.5: allShortestPaths, the eight (ch4 s4's picture)
    def clip5(self):
        code, path = self.code, self.path
        new = sp_code(fn="allShortestPaths", ret="RETURN length(path), count(*);")
        new.find("*", line=2).set_color(YELLOW)
        new.align_to(code, LEFT).align_to(code, UP)
        h1, h2 = Mono("length(path)", size=30, color=DIM), Mono("count(*)", size=30, color=DIM)
        v1, v2 = Mono("4", size=34, color=GOLD), Mono("8", size=34, color=GOLD)
        h2.next_to(h1, RIGHT, buff=0.9)
        v1.next_to(h1, DOWN, buff=0.35)
        v2.next_to(h2, DOWN, buff=0.35).align_to(v1, DOWN)
        rule = Line(h1.get_corner(DL) + 0.18 * DOWN + 0.2 * LEFT, h2.get_corner(DR) + 0.18 * DOWN + 0.2 * RIGHT)
        rule.set_stroke(DIM, 2)
        table = VGroup(h1, h2, rule, v1, v2).move_to((0, -1.4, 0))
        fan = eight_fan().scale(0.95)
        fan.shift((3.5 - fan.get_top()[1]) * UP - fan.get_center()[0] * RIGHT)
        table_dst = np.array([-3.4, -2.6, 0])
        none = T("495 of length 6", size=34, color=DIM).move_to((3.4, table_dst[1], 0))
        strike = Line(none.get_left() + 0.1 * LEFT, none.get_right() + 0.1 * RIGHT).set_stroke(RED, 4)
        films = [k for k in fan.shapes if k not in ("L", "R", "H", "M", "G")]

        with self.say("c5.bfs.5") as c:
            self.play(FlashAround(code.find("shortestPath(", line=0), run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("allsp")
            self.play(*disappear(path, self.anylen), run_time=0.8)
            self.play(*edit(code, new), run_time=1.5)
            c.wait_until("eight paths")
            self.play(*appear(h1, h2, rule, lag=0.1), run_time=0.8)  # early: the table header, read with its row
            self.play(*appear(v1, v2, lag=0.3), run_time=1.0)
            settle(self, table)
            c.wait_until("same")
            # the code is gone completely before the fan arrives in its place
            sweep_clear(self, *during([table.animate.move_to(table_dst)], 0, 1), keep=[table], run_time=0.9)
            self.play(LaggedStart(*[Create(e) for e in fan.edges.values()], lag_ratio=0.02),  # early: the returning eight-path picture, shown whole
                      *[GrowFromCenter(s) for s in fan.shapes.values()],
                      *appear(*[fan.labels[k] for k in films], shift=None, lag=0.03),
                      *appear(*fan.end_labels, *fan.name_labels, lag=0.05),
                      run_time=1.4)
            for k, name in zip(("H", "M", "G"), ["Woody", "McAvoy", "Gleeson"]):
                c.wait_until(name)
                self.play(FlashAround(VGroup(fan.shapes[k], fan.labels[k]), run_time=1.0, time_width=1.5),
                          fan.shapes[k].animate.set_stroke(YELLOW), run_time=1.0)
            c.wait_until("none")
            self.play(*appear(none), run_time=0.8)
            self.play(Create(strike), run_time=0.6)
        self.wait(2.5)
