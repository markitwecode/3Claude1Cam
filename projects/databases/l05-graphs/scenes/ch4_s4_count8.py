"""Chapter 4, scene 4: where the eight paths come from. Clips c4.eight.1 – c4.eight.4."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the query (s2's, last line changed) ───────────────────────────────────────────
Q_HEAD = ("MATCH path = (a:Person {name: 'Jennifer Lawrence'})\n"
          "             -[:ACTED_IN*4]-\n"
          "             (b:Person {name: 'Daniel Radcliffe'})\n")
Q_COUNT = Q_HEAD + "RETURN count(path);"
Q_PATH = Q_HEAD + "RETURN path;"

# ── the eight paths' vertices (cypher-shell, vertices 1-3 of each path) ───────────
MIDS = ["H", "M", "G"]
NAMES = {"L": "Lawrence", "R": "Radcliffe", "H": "Harrelson", "M": "McAvoy", "G": "Gleeson"}
LEFT_FILMS = {"H": ["Catching Fire", "Mockingjay 1", "Mockingjay 2"],
              "M": ["First Class", "Days of Future Past", "Apocalypse", "Dark Phoenix"],
              "G": ["Mother!"]}
RIGHT_FILM = {"H": "Now You See Me 2", "M": "Victor Frankenstein", "G": "Deathly Hallows 2"}

PR = 0.42            # person radius
LX, LFX, MX, RFX, RX = -6.0, -2.8, 0.3, 3.3, 6.0
END_Y = 0.2          # Lawrence and Radcliffe
FILM_PITCH, GROUP_GAP = 0.62, 0.35


def _layered_positions():
    pos = {"L": (LX, END_Y), "R": (RX, END_Y)}
    y = 3.0
    for m in MIDS:
        ys = []
        for f in LEFT_FILMS[m]:
            pos[f] = (LFX, y)
            ys.append(y)
            y -= FILM_PITCH
        y -= GROUP_GAP
        my = sum(ys) / len(ys)
        pos[m] = (MX, my)
        pos[RIGHT_FILM[m]] = (RFX, my)
    return {k: np.array([x, yy, 0.0]) for k, (x, yy) in pos.items()}


LAYERED = _layered_positions()

# a deliberately tangled Traverse-style placement (shared vertices pulled to the middle)
TANGLE = {k: np.array([x, y, 0.0]) for k, (x, y) in {
    "Days of Future Past": (-4.6, 0.8), "R": (-1.4, 0.8), "Mockingjay 2": (2.6, 0.8), "M": (4.7, 0.8),
    "H": (-5.7, -0.4), "Now You See Me 2": (-1.3, -0.4), "L": (1.5, -0.4), "Dark Phoenix": (5.4, -0.4),
    "Catching Fire": (-4.8, -1.6), "G": (-1.7, -1.6), "Deathly Hallows 2": (2.6, -1.6), "Mother!": (5.5, -1.6),
    "Apocalypse": (-5.2, -2.8), "Mockingjay 1": (-2.0, -2.8), "First Class": (1.2, -2.8),
    "Victor Frankenstein": (4.5, -2.8)}.items()}


def rim(shape, toward):
    """Point on a node's outline in the direction of `toward` (edges stop at the outline)."""
    c = shape.get_center()
    u = np.array(toward) - c
    n = np.linalg.norm(u)
    if n < 1e-6:
        return c
    u = u / n
    if isinstance(shape, Circle):
        return c + (shape.width / 2) * u
    hw, hh = shape.width / 2, shape.height / 2
    return c + u / max(abs(u[0]) / hw, abs(u[1]) / hh, 1e-6)


def edge_pts(a, b):
    return rim(a, b.get_center()), rim(b, a.get_center())


PERSON_FILL = interpolate_color(ManimColor(BG), ManimColor(PINK), 0.15)   # opaque: edges stop under it
FILM_FILL = interpolate_color(ManimColor(BG), ManimColor(BLUE), 0.2)


def person_shape(pos, r=PR):
    return Circle(radius=r).set_stroke(PINK, 4).set_fill(PERSON_FILL, 1).move_to(pos)


def film_box(width, pos, height=0.56):
    return RoundedRectangle(corner_radius=0.12, width=width, height=height) \
        .set_stroke(BLUE, 3).set_fill(FILM_FILL, 1).move_to(pos)


def movie_dot(pos, r=PR):
    """An untitled Movie vertex: a BLUE circle in the person circles' look."""
    return Circle(radius=r).set_stroke(BLUE, 4).set_fill(FILM_FILL, 1).move_to(pos)


def place_person_label(key, shape, label, layered=True):
    if not layered:
        label.next_to(shape, RIGHT, buff=0.12)
    elif key in ("L", "R"):
        label.next_to(shape, DOWN, buff=0.42)    # clear of the fan's lowest edge
        if label.get_right()[0] > 6.75:
            label.shift((6.75 - label.get_right()[0]) * RIGHT)
        if label.get_left()[0] < -6.75:
            label.shift((-6.75 - label.get_left()[0]) * RIGHT)
    else:
        label.next_to(shape, UP, buff=0.14)
    return label


def layered_paths():
    """The untangled layered drawing of the 8 Lawrence-Radcliffe paths of length 4.
    VGroup(*edges, *shapes, *labels), frame-sized (about 13 x 6, centred near y=0.4).
      .shapes[k], .labels[k]: k in "L" "R" "H" "M" "G" (PINK circles, surname labels) or a film
                              title (BLUE rounded box, title inside)
      .edges[(a, b)]:         DIM Line between outlines; keys ("L", film), (film, mid), (mid, rfilm), (rfilm, "R")
      .paths:                 8 lists of 4 edge keys, Harrelson's 3, McAvoy's 4, Gleeson's 1
      .group_keys[m]:         (node keys, edge keys) belonging to middle m (not L, R); members(g, m)
                              gives the mobjects"""
    g = VGroup()
    g.shapes, g.labels, g.edges = {}, {}, {}
    for k in ("L", "R", *MIDS):
        g.shapes[k] = person_shape(LAYERED[k])
        g.labels[k] = place_person_label(k, g.shapes[k], set_backstroke(T(NAMES[k], 30)))
    for m in MIDS:
        for f in LEFT_FILMS[m] + [RIGHT_FILM[m]]:
            t = T(f, 28)
            g.shapes[f] = film_box(t.width + 0.36, LAYERED[f])
            g.labels[f] = t.move_to(g.shapes[f])
    g.paths, g.group_keys = [], {}
    for m in MIDS:
        rf = RIGHT_FILM[m]
        keys = []
        for f in LEFT_FILMS[m]:
            p = [("L", f), (f, m), (m, rf), (rf, "R")]
            g.paths.append(p)
            keys += p
        for a, b in keys:
            if (a, b) not in g.edges:
                g.edges[(a, b)] = Line(*edge_pts(g.shapes[a], g.shapes[b])).set_stroke(DIM, 3).set_z_index(-1)
        g.group_keys[m] = ([m, rf] + LEFT_FILMS[m], list(dict.fromkeys(keys)))
    g.add(*g.edges.values(), *g.shapes.values(), *g.labels.values())
    return g


def members(g, m):
    """Every shape, label and edge of middle m's part of the drawing (current objects)."""
    nodes, edges = g.group_keys[m]
    return [g.shapes[k] for k in nodes] + [g.labels[k] for k in nodes] + [g.edges[e] for e in edges]


def alpha(mobs, k):
    """Dim (k=DIMMED) or restore (k=1) parts of the drawing, keeping the nodes' faint fills."""
    out = []
    for m in mobs:
        if isinstance(m, Line):
            out.append(m.animate.set_stroke(opacity=k))
        elif isinstance(m, (Circle, RoundedRectangle)):
            out.append(m.animate.set_stroke(opacity=k))
        else:
            out.append(m.animate.set_opacity(k))
    return out


def placement_patch():
    """A small graph patch with the pattern (a)-(m)-(x)-(m)-(b) laid on it in YELLOW."""
    P = lambda x, y: np.array([x, y, 0.0])  # noqa: E731
    pat_pos = [("p", P(-2.6, -0.3)), ("f", P(-1.3, 0.8)), ("p", P(0.0, -0.2)), ("f", P(1.3, 0.9)),
               ("p", P(2.6, -0.1))]
    other_pos = {"F5": ("f", P(-1.1, -1.25)), "F6": ("f", P(1.7, -1.2)), "F7": ("f", P(-2.5, 1.5)),
                 "Q1": ("p", P(0.1, 1.6)), "Q2": ("p", P(0.3, -1.65)), "Q3": ("p", P(2.7, 1.55))}

    def node(kind, pos, hot):
        s = person_shape(pos, r=0.28) if kind == "p" else movie_dot(pos, r=0.28)
        if hot:
            s.set_stroke(YELLOW, 5)
        return s

    pat = [node(k, p, True) for k, p in pat_pos]
    oth = {n: node(k, p, False) for n, (k, p) in other_pos.items()}
    allv = {f"P{i}": s for i, s in enumerate(pat)} | oth
    other_edges = [("P0", "F5"), ("P2", "F5"), ("Q2", "F5"), ("Q2", "F6"), ("P4", "F6"), ("Q1", "P1"),
                   ("Q1", "P3"), ("F7", "P0"), ("F7", "Q1"), ("Q3", "P3"), ("P2", "F6")]
    oe = [Line(*edge_pts(allv[a], allv[b])).set_stroke(DIM, 3) for a, b in other_edges]
    pe = [Line(*edge_pts(pat[i], pat[i + 1])).set_stroke(YELLOW, 5) for i in range(4)]
    g = VGroup(*oe, *oth.values(), *pe, *pat)
    g.pattern_nodes, g.pattern_edges = pat, pe
    g.others = [*oe, *oth.values()]
    return g


class CountEight(NarratedScene):
    def construct(self):
        self.G = layered_paths()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── helpers ────────────────────────────────────────────────────────────────
    def light(self, idxs, lit, run_time=1.0, extra=()):
        """Light whole paths YELLOW: a pulse runs along each, its edges stay YELLOW."""
        G = self.G
        anims = list(extra)
        for i in idxs:
            es = [G.edges[k] for k in G.paths[i]]
            pts = []
            for e in es:
                pts += [e.get_start(), e.get_end()]
            pl = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 8)
            anims.append(VShowPassingFlash(pl, time_width=0.6))
            for k in G.paths[i]:
                if k not in lit:
                    lit.add(k)
                    anims.append(G.edges[k].animate.set_stroke(YELLOW, 5))
        self.play(*anims, run_time=run_time)

    def product(self, m, text):
        p = MathTex(text, font_size=44, color=GOLD)
        p.next_to(self.G.shapes[m], DOWN, buff=0.16)
        return p

    # ── clip 1: the tangle, untangled ──────────────────────────────────────────
    def clip1(self):
        G = self.G
        with self.say("c4.eight.1") as c:
            code0 = Code(Q_COUNT, size=28).to_edge(UP, buff=0.45)
            self.play(*appear(code0, shift=None), run_time=0.8)
            c.wait_until("instead")
            code1 = Code(Q_PATH, size=28)
            code1.align_to(code0, UL)
            self.play(*edit(code0, code1), run_time=min(1.4, c.until("traverse")))
            # the tangle: the same objects, scrambled
            lay_labels = {k: l.copy() for k, l in G.labels.items()}
            for k, s in G.shapes.items():
                s.move_to(TANGLE[k])
                if k in NAMES:
                    place_person_label(k, s, G.labels[k], layered=False)
                else:
                    G.labels[k].move_to(s)
            for (a, b), e in G.edges.items():
                e.put_start_and_end_on(*edge_pts(G.shapes[a], G.shapes[b]))
            c.wait_until("traverse")
            nodes = []
            for k in G.shapes:
                nodes += [G.shapes[k], G.labels[k]]
            self.play(*appear(*nodes, shift=None, lag=0.04), run_time=1.4)  # early: Traverse draws the whole tangle at once
            self.play(*appear(*G.edges.values(), shift=None, lag=0.03), run_time=1.2)
            c.wait_until("same people")
            self.play(*flash([G.shapes[k] for k in ("L", "R", "H", "M", "G")], run_time=1.5,
                             time_width=1.5))
            c.wait_until("untangle")
            # untangle: labels step out, vertices move to their layers, labels step back in
            for (a, b), e in G.edges.items():
                e.add_updater(lambda l, a=a, b=b: l.put_start_and_end_on(*edge_pts(G.shapes[a], G.shapes[b])))
            old = list(G.labels.values())
            self.play(*during(disappear(code1, *old), 0, 0.25),  # early: the same labels, back in their layers
                      *during([s.animate.move_to(LAYERED[k]) for k, s in G.shapes.items()], 0.2, 0.82),
                      *during(appear(*lay_labels.values(), shift=None), 0.8, 1.0),
                      run_time=2.6)
            for e in G.edges.values():
                e.clear_updaters()
            G.labels = lay_labels
            G.remove(*old)
            settle(self, G, add=list(lay_labels.values()))
            # every path has a middle
            c.wait_until("mid")
            col = RoundedRectangle(corner_radius=0.2, width=2.3, height=6.0).set_stroke(YELLOW, 2) \
                .set_fill(YELLOW, 0.06).move_to([MX, (G.labels["H"].get_top()[1] + G.shapes["G"].get_bottom()[1]) / 2, 0])
            col.stretch_to_fit_height(G.labels["H"].get_top()[1] - G.shapes["G"].get_bottom()[1] + 0.4)
            col.set_z_index(-2)
            self.play(FadeIn(col), run_time=1.0)
            self.col = col
            c.wait_until("lawrence")
            self.play(*flash([G.shapes["L"]], run_time=1.2, time_width=1.5))
            c.wait_until("radcliffe")
            self.play(*flash([G.shapes["R"]], run_time=1.2, time_width=1.5))
            for cue, m in (("woody", "H"), ("mcavoy", "M"), ("gleeson", "G")):
                c.wait_until(cue)
                self.play(*flash([VGroup(G.shapes[m], G.labels[m])], run_time=1.0, time_width=1.5),
                          G.labels[m].animate.set_color(PINK), run_time=1.0)

    # ── clip 2: Harrelson ───────────────────────────────────────────────────────
    def clip2(self):
        G = self.G
        self.lit = set()
        with self.say("c4.eight.2") as c:
            self.play(FadeOut(self.col), *alpha(members(G, "M") + members(G, "G"), DIMMED),
                      run_time=1.0)
            c.wait_until("catching fire")
            self.play(*flash([G.shapes["Catching Fire"]], run_time=1.2, time_width=1.5))
            c.wait_until("mockingjay")
            self.play(*flash([G.shapes["Mockingjay 1"], G.shapes["Mockingjay 2"]], run_time=1.4,
                             time_width=1.5))
            # the first film is missing from the stored cast
            c.wait_until("first")
            box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.1, height=0.95),
                                 num_dashes=28).set_stroke(BLUE, 3, opacity=0.55)
            hg = T("The Hunger\nGames", 28, color=DIM)
            ghost = VGroup(box, hg.move_to(box)).move_to([-5.45, 2.9, 0])
            self.play(*appear(ghost, shift=None), run_time=1.0)
            c.wait_until("at most ten")
            cap = T("stored cast: 10 actors, Harrelson not among them", 30, t2c={"10": GOLD})
            cap.move_to([0, -3.4, 0])
            self.play(*appear(cap), run_time=1.0)  # early: caption sums up the spoken clause
            c.wait_until("nysm")
            self.play(*flash([G.shapes["Now You See Me 2"]], run_time=1.4, time_width=1.5))
            c.wait_until("mult")
            self.light([0], self.lit, run_time=1.2)
            c.wait_until("one of three")
            self.light([1], self.lit, run_time=1.0, extra=disappear(ghost, cap))
            self.light([2], self.lit, run_time=1.0)
            c.wait_until("three times one")
            self.p1 = self.product("H", r"3 \times 1")
            self.play(*appear(self.p1), run_time=1.0)

    # ── clip 3: McAvoy, Gleeson, the sum ────────────────────────────────────────
    def clip3(self):
        G = self.G
        with self.say("c4.eight.3") as c:
            self.play(*alpha(members(G, "H"), DIMMED), *alpha(members(G, "M"), 1), run_time=1.0)
            self.play(*flash([G.shapes[f] for f in LEFT_FILMS["M"]], run_time=1.4, time_width=1.5))
            c.wait_until("vf")
            self.play(*flash([G.shapes["Victor Frankenstein"]], run_time=1.2, time_width=1.5))
            c.wait_until("four times one")
            self.light([3, 4, 5, 6], self.lit, run_time=1.2)
            self.p2 = self.product("M", r"4 \times 1")
            self.play(*appear(self.p2), run_time=0.9)
            c.wait_until("domhnall")
            self.play(*alpha(members(G, "M"), DIMMED), *alpha(members(G, "G"), 1), run_time=1.0)
            c.wait_until("mother")
            self.play(*flash([G.shapes["Mother!"]], run_time=1.2, time_width=1.5))
            c.wait_until("harry potter")
            self.play(*flash([G.shapes["Deathly Hallows 2"]], run_time=1.2, time_width=1.5))
            c.wait_until("one path")
            self.p3 = self.product("G", r"1 \times 1")
            self.light([7], self.lit, run_time=1.1, extra=during(appear(self.p3), 0.4, 1.0))
            # the products slide together
            c.wait_until("sum")
            tmpl = MathTex(r"3 \times 1", "+", r"4 \times 1", "+", r"1 \times 1", "=", "8",
                           font_size=44).move_to([0, -3.4, 0])
            tmpl[6].set_color(GOLD)
            for p, i in ((self.p1, 0), (self.p2, 2), (self.p3, 4)):
                p.generate_target()
                p.target.move_to(tmpl[i])
            # the middles' names step aside so the products can slide down through their column
            names = [G.labels[m] for m in MIDS]
            G.remove(*names)
            self.add(*names)
            restore = [m for m in members(G, "H") + members(G, "M") if m not in names]
            self.play(*alpha(restore, 1), *during(disappear(*names), 0, 0.22),
                      *during([MoveToTarget(p) for p in (self.p1, self.p2, self.p3)], 0.2, 0.8),
                      *during(appear(tmpl[1], tmpl[3], shift=None), 0.75, 1.0), run_time=2.2)
            for m in MIDS:
                del G.labels[m]
            c.wait_until("eight")
            self.play(*appear(tmpl[5], tmpl[6], shift=None, lag=0.3), run_time=0.8)
            self.play(FlashAround(tmpl[6], color=GOLD, run_time=1.0, time_width=1.5))
            self.sum = VGroup(self.p1, tmpl[1], self.p2, tmpl[3], self.p3, tmpl[5], tmpl[6])
            settle(self, self.sum)

    # ── clip 4: the rule, and one path = one placement ──────────────────────────
    def clip4(self):
        G = self.G
        with self.say("c4.eight.4") as c:
            # the drawing shrinks to a thumbnail: its labels step out first (too small to read)
            labs = list(G.labels.values())
            G.remove(*labs)
            self.add(*labs)
            self.play(*during(disappear(*labs), 0, 0.3),
                      *during([G.animate.scale(0.5).move_to([-3.3, 1.0, 0]),
                               self.sum.animate.scale(0.9).move_to([-3.3, -1.7, 0])], 0.25, 1.0),
                      run_time=1.6)
            r1 = T("along a path: multiply", 36, color=YELLOW).move_to([3.6, 0.9, 0])
            r2 = T("different middles: add", 36, color=YELLOW).move_to([3.6, -0.1, 0])
            c.wait_until("times")
            self.play(*appear(r1), *flash([self.p1[0][1], self.p2[0][1], self.p3[0][1]],
                                          color=GOLD, run_time=1.4), run_time=1.4)
            c.wait_until("plus")
            self.play(*appear(r2), *flash([self.sum[1], self.sum[3]], color=GOLD, run_time=1.4),
                      run_time=1.4)
            # one path lifts out and is laid on the pattern's placement
            c.wait_until("placement")
            keys = ["L", "Catching Fire", "H", "Now You See Me 2", "R"]
            nodes = [G.shapes[k].copy() for k in keys]
            edges = [G.edges[k].copy() for k in G.paths[0]]
            for m in nodes:
                m.set_stroke(YELLOW, 4)
            for e in edges:
                e.set_stroke(YELLOW, 4)
            self.play(*[FadeIn(m, shift=0.3 * UP) for m in nodes + edges], run_time=0.9)
            patch = placement_patch()
            patch.scale(1.1).move_to([-3.3, 0.6, 0])
            sweep_clear(self, *[FadeIn(m) for m in patch.others], keep=[r1, r2, *nodes, *edges],
                        run_time=1.2)
            self.play(*[ReplacementTransform(a, b) for a, b in
                        zip(nodes + edges, patch.pattern_nodes + patch.pattern_edges)], run_time=1.5)
            tag = T("1 path = 1 placement = 1 row", 36).move_to([-3.3, -2.3, 0])
            c.wait_until("one row")
            self.play(*appear(tag), run_time=1.0)  # early: the tag is the sentence's summary
            c.wait_until("why")
            self.play(FlashUnder(r1, color=YELLOW, run_time=2.0, time_width=1.5))
