"""Chapter 7, scene 3: JSON path, a route through the tree. Clips c7.paths.1 – c7.paths.5.

Shared pieces (`from lib.paths import load_scene; P = load_scene("ch7_s3_paths")`):

  list_box(items, size=28, item_color=BLUE, bracket_color=BLUE, quoted=False,
           per_line=None, serif=False, frame=True)
      DuckDB's list as a BLUE box, e.g. list_box(["Comedy", "Drama", "Family"]) ->
      `[Comedy, Drama, Family]`. Every item is its own text (.items[i]); brackets and
      commas are .punct; .frame the RoundedRectangle (None with frame=False).
      quoted=True + item_color=TEAL: `["Comedy", "Drama", "Family"]` (json[] elements).
      per_line=(3, 4, 3): wrap into lines of that many items. serif=True: CMU Serif.
  walk_tree(lit=(), keys=WALK_KEYS, open=(), size=26, **kw)
      A static subset of The Kid (ch4 s2's json_tree(kid_value())), only `keys` at the
      top level; genres fully open, actors open at [0] (person_id, name, roles) with
      [1–9] merged, plus every path in `lit` / `open` opened. Every path in `lit` is
      lit TEAL from the root down (edges, labels, nodes). Paths are tuples of keys and
      positions; the merged "+9 more" node is ("actors", ("more", 1)).
      e.g. walk_tree([("actors", 0, "name")]);  the [*] fork across genres:
      walk_tree([("genres", 0), ("genres", 1), ("genres", 2)]);  s6:
      walk_tree([("directors", 0, "name")], keys=("movie_id", "genres", "actors", "directors")).
  light_step(tree, path, on=True)  animations lighting (or unlighting) the last step of
      a path: its edge, label and node (path () = the root).
  light(tree, paths)  the same, static, for every step of every path.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

J = load_scene("ch4_s2_json")

# ══ shared helpers ═════════════════════════════════════════════════════════════

WALK_KEYS = ("movie_id", "genres", "actors")
LIT_FILL = interpolate_color(ManimColor(BG), ManimColor(TEAL), 0.28)


def list_box(items, size=28, item_color=BLUE, bracket_color=BLUE, quoted=False,
             per_line=None, serif=False, frame=True):
    """A DuckDB list `[a, b, c]` as separate texts (items, brackets, commas) in a BLUE box."""
    make = T if serif else Mono
    strs = [f'"{s}"' if quoted else str(s) for s in items]
    counts = list(per_line) if per_line else [len(strs)]
    groups, i = [], 0
    for n in counts:
        groups.append(list(range(i, i + n)))
        i += n
    item_mobs = [None] * len(strs)
    punct, lines = [], []
    for li, idx in enumerate(groups):
        toks = []                       # (text, kind, item index)
        if li == 0:
            toks.append(("[", "b", None))
        for j, k in enumerate(idx):
            toks.append((strs[k], "i", k))
            last = (li == len(groups) - 1 and j == len(idx) - 1)
            toks.append(("]" if last else ",", "b" if last else "c", None))
        line_str = ""
        spans = []
        for text, kind, k in toks:
            if kind == "i" and line_str and not line_str.endswith("["):
                line_str += " "
            a = len(line_str.replace(" ", ""))
            line_str += text
            spans.append((text, kind, k, a, len(line_str.replace(" ", ""))))
        ref = make(line_str, size=size)
        parts = VGroup()
        for text, kind, k, a, b in spans:
            col = item_color if kind == "i" else (bracket_color if kind == "b" else DIM)
            m = make(text, size=size, color=col)
            m.move_to(VGroup(*ref[a:b]).get_center())
            parts.add(m)
            if kind == "i":
                item_mobs[k] = m
            else:
                punct.append(m)
        lines.append(parts)
    body = VGroup(*lines).arrange(DOWN, buff=0.16 * size / 28, aligned_edge=LEFT)
    if len(lines) > 1:
        dx = lines[0][1].get_left()[0] - lines[1].get_left()[0]
        for ln in lines[1:]:
            ln.shift(dx * RIGHT)
    box = VGroup()
    fr = None
    if frame:
        fr = RoundedRectangle(corner_radius=0.12, width=body.width + 0.44,
                              height=body.height + 0.32)
        fr.set_stroke(BLUE, 2.5).set_fill(BLUE, 0.08).move_to(body)
        box.add(fr)
    box.add(*punct, *item_mobs)
    box.frame, box.items, box.punct, box.lines = fr, item_mobs, punct, lines
    return box


def _concrete(p):
    return all(isinstance(k, (str, int)) for k in p)


def walk_tree(lit=(), keys=WALK_KEYS, open=(), size=26, **kw):
    """The Kid, top-level `keys` only, with `lit` paths lit TEAL (see module docstring)."""
    kid = J.kid_value()
    value = {k: kid[k] for k in keys}
    opens = []
    if "genres" in keys:
        opens.append(("genres",))
    if "actors" in keys:
        opens.append(("actors", 0))
    opens += [tuple(p) for p in open]
    opens += [tuple(p) for p in lit if _concrete(p)]
    opts = dict(open=opens, size=size, row_gap=0.42, label_pad=0.32, trunk_gap=0.15)
    opts.update(kw)
    tree = J.json_tree(value, **opts)
    tree.orig = {}
    for p in tree.paths:
        if tree.kinds[p] in ("leaf", "more"):
            tree.orig[p] = tree.nodes[p].get_color()
        if p in tree.labels:
            tree.orig[("label",) + p] = tree.labels[p].get_color()
    light(tree, lit)
    return tree


def _box_style(node, on):
    node.box.set_fill(LIT_FILL if on else BG, 1).set_stroke(TEAL, 4 if on else 2.5)


def light(tree, paths):
    """Static: light every step of every path (root included)."""
    for path in paths:
        p = tuple(path)
        for n in range(len(p) + 1):
            q = p[:n]
            if q in tree.edges:
                tree.edges[q].set_stroke(TEAL, 5)
            if q in tree.labels:
                tree.labels[q].set_color(TEAL)
            node, kind = tree.nodes[q], tree.kinds[q]
            if kind in ("object", "array"):
                _box_style(node, True)
            elif kind == "stub":
                node.set_opacity(1)
            else:
                node.set_color(TEAL)
    return tree


def light_step(tree, path, on=True, flash=True):
    """Animations lighting (on) or unlighting the last step of `path`."""
    p = tuple(path)
    anims = []
    if p in tree.edges:
        e = tree.edges[p]
        anims.append(e.animate.set_stroke(TEAL if on else DIM, 5 if on else 2.5))
        if on and flash:
            anims.append(VShowPassingFlash(e.copy().set_stroke(FG, 7), time_width=0.7))
    if p in tree.labels:
        lab = tree.labels[p]
        anims.append(lab.animate.set_color(TEAL if on else tree.orig[("label",) + p]))
    node, kind = tree.nodes[p], tree.kinds[p]
    if kind in ("object", "array"):
        tgt = node.copy()
        _box_style(tgt, on)
        anims.append(Transform(node, tgt))
    elif kind == "stub":
        anims.append(node.animate.set_opacity(1 if on else 0.7))
    else:
        anims.append(node.animate.set_color(TEAL if on else tree.orig[p]))
    return anims


# ══ this scene's pieces ════════════════════════════════════════════════════════

CHAIN = "movie->'actors'->0->>'name'"
PATH1 = "movie->>'$.actors[0].name'"

Q1 = """SELECT movie->>'$.actors[0].name' AS first_actor,
       movie->>'$.genres[1]'      AS second_genre,
       movie->>'$.genres[*]'      AS all_genres
FROM   movies
WHERE movie_id = 'tt0012349';"""

Q2 = """SELECT movie->>'$.genres[0]'      AS json_first,
       (movie->>'$.genres[*]')[1] AS list_first,
       (movie->>'$.genres[*]')[0] AS list_zero
FROM   movies
WHERE movie_id = 'tt0012349';"""

GENRES = ["Comedy", "Drama", "Family"]
NAMES = ["Charles Chaplin", "Edna Purviance", "Jackie Coogan", "Carl Miller", "Albert Austin",
         "Beulah Bains", "Nellie Bly Baker", "Henry Bergman", "Edward Biby", "B.F. Blinn"]

LEGEND = [("$", "the whole document"),
          (".actors", "value of the key actors"),
          ("[0]", "first element of an array (counting from 0)"),
          ("[*]", "every element of an array ⇒ result is a list")]


def step_chips(code, line, steps, color=TEAL):
    """One rounded chip behind each step of the path on `line` of `code`."""
    ln = code.line(line)
    out = []
    for s in steps:
        g = code.find(s, line=line)
        r = RoundedRectangle(corner_radius=0.07, width=g.width + 0.05, height=0.5)
        r.set_stroke(color, 2).set_fill(color, 0.2).move_to([g.get_center()[0], ln.get_center()[1], 0])
        r.set_z_index(-1)
        out.append(r)
    return out


def drop_copy(src, dst, via, color):
    """A copy of src (same glyphs as dst) goes src -> via -> dst, fading up as it leaves src and
    turning `color`; returns (animation, copy). Afterwards remove the copy and add dst."""
    c0 = src.copy()
    cp = src.copy()
    p0, p2 = src.get_center(), dst.get_center()
    s1 = dst.height / max(src.height, 1e-6)
    col0 = src[0].get_color()

    def upd(m, a):
        m.become(c0)
        if a < 0.3:
            t = smooth(a / 0.3)
            pos, op = p0 + (via - p0) * t, 0.1 + 0.9 * float(np.clip((t - 0.45) / 0.55, 0, 1))
        else:
            t = smooth((a - 0.3) / 0.7)
            pos, op = via + (p2 - via) * t, 1.0
        m.scale(1 + (s1 - 1) * a).move_to(pos)
        m.set_color(interpolate_color(ManimColor(col0), ManimColor(color), a)).set_opacity(op)
    return UpdateFromAlphaFunc(cp, upd), cp


def result_cell(header, value, x, y):
    h = Mono(header, size=28, color=DIM).move_to([x, y, 0])
    value.move_to([x, y - 0.55, 0])
    return h, value


class JsonPaths(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c7.paths.1: from a chain of arrows to one path ─────────────────────────
    def clip1(self):
        with self.say("c7.paths.1") as c:
            chain = Code(CHAIN, size=48).move_to(0.4 * UP)
            self.play(*appear(chain), run_time=1.0)
            arrows = [chain.find("->", nth=0), chain.find("->", nth=1), chain.find("->>")]
            self.play(*[time_span(FlashAround(a, color=YELLOW), 0.35 * i, 0.35 * i + 1.0)
                        for i, a in enumerate(arrows)], run_time=1.7)
            c.wait_until("route")

            path = Code(PATH1, size=48).move_to(chain)
            self.play(*edit(chain, path), run_time=min(1.6, c.until("one string")))
            self.path = path
            c.wait_until("one string")
            strpart = path.find("'$.actors[0].name'")
            self.play(FlashUnder(strpart, color=TEAL, run_time=1.4, time_width=1.5))
            c.wait_until("name")

            brace = Brace(strpart, DOWN, buff=0.2).set_color(TEAL)
            jp = T("JSON path", size=44, color=TEAL).next_to(brace, DOWN, buff=0.2)
            c.wait_until(own_word=jp)
            self.play(GrowFromCenter(brace), *appear(jp), run_time=1.0)
            c.wait_until("example")

            # the path settles into slide 85's query; the tree comes in below
            q = Code(Q1, size=26)
            q.to_corner(UL, buff=0.5).shift(0.15 * UP)
            self.q = q
            sub = q.find(PATH1, line=0)
            s = sub.width / path.width
            jp_to = jp.copy().scale(30 / 44).next_to(q.line(0), RIGHT, buff=0.45)
            self.play(*during(disappear(brace), 0, 0.4),
                      *during([jp.animate.scale(30 / 44).move_to(jp_to)], 0.35, 1),
                      *during([path.animate.scale(s).move_to(sub.get_center())], 0, 0.8), run_time=1.3)
            self.jp = jp
            subset = set(id(g) for g in sub)
            rest = [g for g in q.text if id(g) not in subset]
            for g in rest:
                g.set_opacity(0)
            self.remove(path)
            self.add(q)

            tree = walk_tree()
            tree.next_to(q, DOWN, buff=0.45).set_x(0)
            self.tree = tree

            def show_rest(m, a):
                for g in rest:
                    g.set_opacity(a)
            self.play(UpdateFromAlphaFunc(q, show_rest), FadeIn(tree), run_time=1.0)
            q.set_opacity(1)
            # dim lines 2 and 3 until their turn
            for i in (1, 2):
                q.line(i).set_opacity(DIMMED)
            c.wait_until("Dollar")

            self.chips1 = step_chips(q, 0, ["$", ".actors", "[0]", ".name"])
            self.play(*appear(*self.chips1, shift=None, lag=0.55), run_time=min(2.4, c.until()))

    # ── c7.paths.2: walk $.actors[0].name, then $.genres[1] ───────────────────
    def clip2(self):
        q, tree, ch = self.q, self.tree, self.chips1
        with self.say("c7.paths.2") as c:
            steps = [((), "dollar"), (("actors",), "key"), (("actors", 0), "index"),
                     (("actors", 0, "name"), "leaf")]
            for i, (p, cue) in enumerate(steps):
                c.wait_until(cue)
                self.play(*light_step(tree, p), FlashAround(ch[i], color=TEAL, time_width=1.5),
                          run_time=1.4)
            settle(self, tree)

            ybase = tree.get_bottom()[1] - 0.4
            leaf = tree.node("actors", 0, "name")
            inner = VGroup(*leaf[1:-1])
            v1 = Mono("Charles Chaplin", size=28, color=BLUE)
            x1 = min(leaf.get_x() + 0.5, 6.6 - v1.width / 2)
            xs = [-4.4, x1]
            self.xs, self.ybase = xs, ybase
            h1, v1 = result_cell("first_actor", v1, xs[1], ybase)
            stub = tree.node("actors", 0, "roles")
            w = max(inner.width, v1.width)
            via = np.array([stub.get_right()[0] + 0.2 + w / 2, stub.get_y(), 0])
            anim, cp = drop_copy(inner, v1, via, BLUE)
            self.play(anim, *during(appear(h1, shift=None), 0.8, 1), run_time=1.6)
            self.remove(cp)
            self.add(v1)
            self.h1, self.v1 = h1, v1
            c.wait_until("genre")

            # line 2: $.genres[1]
            chips2 = step_chips(q, 1, ["$", ".genres", "[1]"])
            self.chips2 = chips2
            self.play(*[g.animate.set_opacity(1) for g in q.line(1)],
                      *[a for p in [("actors",), ("actors", 0), ("actors", 0, "name")]
                        for a in light_step(tree, p, on=False)],
                      *appear(*chips2, shift=None, lag=0.2), run_time=1.0)
            self.play(*light_step(tree, ("genres",)), *light_step(tree, ("genres", 1)),
                      FlashAround(chips2[2], color=TEAL, time_width=1.5), run_time=1.3)
            settle(self, tree)
            settle(self, q)
            h2, v2 = result_cell("second_genre", Mono("Drama", size=28, color=BLUE), xs[0], ybase)
            self.play(*appear(h2, v2, shift=None, lag=0.3), FlashAround(tree.node("genres", 1), color=TEAL),
                      run_time=min(1.4, c.until(floor=0.8)))
            self.h2, self.v2 = h2, v2

    # ── c7.paths.3: the star, lists, ->> vs ->, all ten names ─────────────────
    def clip3(self):
        q, tree = self.q, self.tree
        xs, ybase = self.xs, self.ybase
        with self.say("c7.paths.3") as c:
            chips3 = step_chips(q, 2, ["$", ".genres"]) + step_chips(q, 2, ["[*]"], color=YELLOW)
            self.play(*[g.animate.set_opacity(1) for g in q.line(2)], *appear(*chips3, shift=None, lag=0.2),
                      *light_step(tree, ("genres", 1), on=False), run_time=1.4)
            c.wait_until("The star means")
            settle(self, q)
            settle(self, tree)
            self.play(FlashAround(chips3[2], color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("fan")

            self.play(*[a for k in range(3) for a in light_step(tree, ("genres", k))], run_time=1.6)
            settle(self, tree)
            c.wait_until("list")

            box = list_box(GENRES, size=26)
            g1 = tree.node("genres", 1)
            box.move_to([0, g1.get_y(), 0]).align_to([6.55, 0, 0], RIGHT)
            h3 = Mono("all_genres", size=28, color=DIM).next_to(box, UP, buff=0.14)
            flies = [a for k in range(3)
                     for a in fly(VGroup(*tree.node("genres", k)[1:-1]), box.items[k])]
            self.play(*during([FadeIn(box.frame), *[FadeIn(m) for m in box.punct]], 0.82, 1),
                      *appear(h3, shift=None), *flies, run_time=1.6)
            settle(self, box)
            c.wait_until("kinds")

            # ->> gives varchar[], -> gives json[]
            r1 = Code("movie->>'$.genres[*]'", size=28)
            r2 = Code("movie->'$.genres[*]'", size=28)
            b1 = list_box(GENRES, size=28)
            b2 = list_box(GENRES, size=28, item_color=TEAL, quoted=True)
            r1.move_to([0, 3.35, 0]).to_edge(LEFT, buff=0.6)
            r2.move_to([0, 2.15, 0]).align_to(r1, LEFT)
            bx = r1.get_right()[0] + 0.5
            b1.move_to(r1).align_to([bx, 0, 0], LEFT)
            b2.move_to(r2).align_to([bx, 0, 0], LEFT)
            t1 = Mono("varchar[]", size=26, color=GREEN).next_to(b1, DOWN, buff=0.12).align_to(b1, RIGHT)
            t2 = Mono("json[]", size=26, color=GREEN).next_to(b2, DOWN, buff=0.12).align_to(b2, RIGHT)
            chips = self.chips1 + self.chips2 + chips3
            self.play(*disappear(q, *chips, h3, self.jp), run_time=0.6)
            self.play(*appear(r1, shift=None), box.animate.move_to(b1), run_time=1.0)
            self.remove(box)
            self.add(b1)
            self.play(*appear(t1, r2, b2, t2, shift=None, lag=0.15), run_time=1.2)
            c.wait_until("names")

            # $.actors[*].name: the walk forks over all ten actors
            r3 = Code("movie->>'$.actors[*].name'", size=28).move_to([0, 3.4, 0])
            chip3 = step_chips(r3, 0, ["[*]"], color=YELLOW)[0]
            names = list_box(NAMES, size=28, serif=True, per_line=(3, 4, 3))
            names.next_to(r3, DOWN, buff=0.25)
            off = [a for k in range(3) for a in light_step(tree, ("genres", k), on=False)]
            off += light_step(tree, ("genres",), on=False)
            self.play(*disappear(r1, r2, b1, b2, t1, t2), *off, run_time=0.8)
            fork = [("actors",), ("actors", 0), ("actors", 0, "name"), ("actors", ("more", 1))]
            self.play(*appear(r3, chip3, shift=None), run_time=0.8)
            self.play(*[a for p in fork for a in light_step(tree, p)],
                      *during(appear(names, shift=None), 0.35, 1), run_time=1.5)
            settle(self, tree)

    # ── c7.paths.4: JSON counts from 0, DuckDB lists from 1 ───────────────────
    def clip4(self):
        with self.say("c7.paths.4") as c:
            arr = list_box(GENRES, size=32, item_color=TEAL, bracket_color=TEAL, quoted=True,
                           frame=False)
            arr.move_to([0.9, 2.7, 0])
            la = T("JSON array", size=32, color=TEAL).next_to(arr, LEFT, buff=0.6)
            sweep_clear(self, *during(appear(la, arr, shift=None, lag=0.3), 0.55, 1))
            tag = Mono("[1]", size=30, color=YELLOW).next_to(arr.items[1], UP, buff=0.22)
            self.play(*appear(tag), FlashAround(arr.items[1], color=YELLOW, time_width=1.5),
                      run_time=1.2)
            c.wait_until("zero")

            idx = [Mono(str(k), size=30, color=TEAL).next_to(arr.items[k], UP, buff=0.22)
                   for k in range(3)]
            for m in idx:
                m.set_y(tag.get_y())
            self.play(*swap(tag, idx[1]), *during(appear(idx[0], idx[2], shift=None), 0.4, 1),
                      run_time=1.4)
            c.wait_until("one")

            lst = list_box(GENRES, size=32)
            lst.move_to([0.9, 1.45, 0]).align_to(arr, LEFT).shift(0.22 * LEFT)
            ll = T("DuckDB list", size=32, color=BLUE).next_to(lst, LEFT, buff=0.6).align_to(la, RIGHT)
            self.play(*appear(ll, lst, shift=None, lag=0.3), run_time=1.2)
            pos = [Mono(str(k + 1), size=30, color=BLUE).next_to(lst.items[k], DOWN, buff=0.3)
                   for k in range(3)]
            for m in pos:
                m.set_y(lst.get_bottom()[1] - 0.3)
            self.play(*appear(*pos, shift=None, lag=0.35), run_time=1.4)
            c.wait_until("both")

            q2 = Code(Q2, size=26).next_to(VGroup(*pos), DOWN, buff=0.4)
            q2.set_x(0)
            self.play(*appear(q2, shift=None), run_time=1.0)
            yb = q2.get_bottom()[1] - 0.4
            xs = [-4.2, -0.2, 3.8]
            h1, v1 = result_cell("json_first", Mono("Comedy", size=28, color=BLUE), xs[0], yb)
            h2, v2 = result_cell("list_first", Mono("Comedy", size=28, color=BLUE), xs[1], yb)
            self.play(*appear(h1, v1, h2, v2, shift=None, lag=0.25),
                      FlashAround(arr.items[0], color=TEAL, time_width=1.5),
                      FlashAround(lst.items[0], color=BLUE, time_width=1.5), run_time=1.6)
            c.wait_until("null")

            h3, v3 = result_cell("list_zero", Mono("NULL", size=28, color=FG), xs[2], yb)
            self.play(*appear(h3, v3, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("quietly")
            self.play(v3.animate.set_color(PINK), FlashAround(v3, color=PINK, time_width=1.5),
                      run_time=1.2)

    # ── c7.paths.5: a path is a little query language ──────────────────────────
    def clip5(self):
        with self.say("c7.paths.5") as c:
            rows = []
            for code, desc in LEGEND:
                rows.append((Mono(code, size=34, color=TEAL), T(desc, size=32)))
            cw = max(a.width for a, _ in rows)
            grid = VGroup()
            for i, (a, b) in enumerate(rows):
                y = -i * 0.72
                a.move_to([cw / 2, y, 0])
                b.next_to([cw + 0.5, y, 0], RIGHT, buff=0).set_y(y)
                grid.add(a, b)
            card = RoundedRectangle(corner_radius=0.2, width=grid.width + 0.9,
                                    height=grid.height + 0.8).set_stroke(TEAL, 3)
            card.set_fill(TEAL, 0.06)
            grid.move_to(ORIGIN)
            card.move_to(grid)
            legend = VGroup(card, grid).move_to(0.5 * UP)
            sweep_clear(self, *during([FadeIn(card), *appear(*grid, shift=None, lag=0.12)], 0.55, 1))  # early: the legend is shown whole and read as a summary
            c.wait_until("decl")
            cap = T("a small declarative query language", size=40, color=YELLOW)
            cap.next_to(legend, DOWN, buff=0.55)
            self.play(*appear(cap), run_time=1.0)
