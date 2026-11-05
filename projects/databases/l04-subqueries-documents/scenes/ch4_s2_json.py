"""Chapter 4, scene 2: JSON in two minutes. Clips c4.json.1 – c4.json.5.

Owns the shared JSON helpers (import with `load_scene("ch4_s2_json")` or
`from scenes.ch4_s2_json import ...`):

  json_tree(value, ...)  a Python JSON value -> static JsonTree (VGroup); see its docstring
  ada_value()            slide 70's Ada Lovelace object as a Python dict (key order kept)
  ada_code(size=30)      it as Code(lang="json"), braces/brackets TEAL, null PINK
  ada_tree(**kw)         json_tree(ada_value(), **kw), fully expanded
  kid_value()            The Kid's real stored document (movies-json.duckdb, tt0012349)
  kid_tree(**kw)         The Kid: 14 top-level keys, containers collapsed to stubs,
                         one path opened: actors -> [ ] -> { } -> roles -> [ ] -> "A Tramp"
"""
# style: 2
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ══ JSON tree helper ═══════════════════════════════════════════════════════════

class _Item:
    def __init__(self, kind, path, depth, value=None, label=None, label_kind=None, n=0):
        self.kind, self.path, self.depth, self.value = kind, path, depth, value
        self.label, self.label_kind, self.n = label, label_kind, n
        self.children = []


def _leaf_mob(v, size):
    if v is None:
        s, col = "null", PINK
    elif v is True or v is False:
        s, col = ("true" if v else "false"), BLUE
    else:
        s, col = json.dumps(v, ensure_ascii=False), GOLD
    return Mono(s, size=size, color=col)


class JsonTree(VGroup):
    """A JSON value drawn as a tree growing to the RIGHT (file-tree style, elbow edges).

    Built by `json_tree(...)`; static (nothing animates by itself). Submobjects, in
    z-order: every edge, then every edge label, then every node.

    Paths: a node is named by its path from the root, a tuple of object keys (str) and
    array positions (int): `()` is the root, `("languages", 1)` is "French" in Ada.
    A merged "+n more" node's path ends in `("more", first)`, first = its first
    hidden key/position (e.g. `("actors", ("more", 1))`).

    Attributes (dicts keyed by path, plus lists in drawing order):
      .nodes[path]  the node: a container VGroup(box, text) for `{ }` / `[ ]`
                    (.box RoundedRectangle, .text Mono, TEAL), a stub VGroup(text)
                    `{…}` / `[…]` (TEAL at 0.7, no box; .box None) for a collapsed container,
                    a leaf Mono (string/number GOLD, true/false BLUE, null PINK), or a
                    "+n more" T in DIM.
      .edges[path]  the elbow line from the parent to this node (not for the root); a
                    labelled edge has two subpaths, broken around its label.
      .labels[path] the edge label, set into that line on the child's row: the key (Mono, FG) or the array
                    position(s) (Mono, DIM: "0", or "1–9" on a merged node). Merged keys
                    have no label.
      .kinds[path]  "object" | "array" | "stub" | "leaf" | "more".
      .paths        every path, depth-first (parents before children).
      .root         .nodes[()].
    Methods:
      .node(*path) .edge(*path) .label(*path)       one part (path given as arguments)
      .branch(*path) -> [edge, label?, node]        what to show to grow that child
      .children(*path) -> [child paths]
      .subtree(*path, include_self=True) -> [parts] edges/labels/nodes below (and of) it
      .depth_parts(d) -> [parts]                    branches of every node at depth d
    Animating parts one by one pulls them out of the tree (play adds them top-level);
    afterwards call `settle(scene, tree)` so a later FadeOut/move of the tree takes them all.
    """

    def node(self, *path):
        return self.nodes[tuple(path)]

    def edge(self, *path):
        return self.edges[tuple(path)]

    def label(self, *path):
        return self.labels.get(tuple(path))

    def children(self, *path):
        p = tuple(path)
        return [q for q in self.paths if len(q) == len(p) + 1 and q[:len(p)] == p]

    def branch(self, *path):
        p = tuple(path)
        out = []
        if p in self.edges:
            out.append(self.edges[p])
        if p in self.labels:
            out.append(self.labels[p])
        out.append(self.nodes[p])
        return out

    def subtree(self, *path, include_self=True):
        p = tuple(path)
        out = []
        for q in self.paths:
            if q[:len(p)] == p and (include_self or q != p):
                out += self.branch(*q) if q != p else [self.nodes[q]]
        return out

    def depth_parts(self, d):
        out = []
        for q in self.paths:
            if len(q) == d:
                out += self.branch(*q)
        return out


def json_tree(value, *, open=None, elide_keys=False, counts=False,
              size=28, key_size=None, leaf_size=None, node_size=None,
              row_gap=None, label_pad=0.45, trunk_gap=0.25,
              edge_color=DIM, edge_width=2.5, key_color=FG, pos_color=DIM,
              node_color=TEAL):
    """Draw a Python JSON value (dict / list / str / int / float / bool / None) as a JsonTree.

    Layout: root at the left, children stacked downward in a column to its right, one
    row per leaf (row pitch `row_gap`, default 0.025·size); a container sits level with
    the middle of its children. Each child hangs off an elbow edge from its parent; the
    key (or DIM array position) is set into the edge's last horizontal stretch, on the
    child's row, so a key reads level with its value: `name ── "Ada Lovelace"`. Centred
    on ORIGIN; at size 28, Ada (ada_tree()) is ~9.2 × 4.8.

    Options:
      open        None (default): expand everything. Otherwise a list of paths (tuples
                  of keys / positions) to open: a container is expanded only if it is
                  the root or lies on one of them; every other container is drawn as a
                  stub `{…}` / `[…]`. In an expanded array, elements off the paths are
                  merged into one DIM "+n more" node per run (labelled "a–b"), unless a
                  path ends at that array (then all its elements are shown). Objects
                  show all their keys (scalars as leaves, containers as stubs).
      elide_keys  with `open`: objects below the root show only the keys on the
                  path; the others merge into "+n more keys".
      counts      stubs show their length, e.g. `[…]` then DIM "5".
      size        base font size; key_size / leaf_size / node_size override it per part.
      row_gap, label_pad (space after the widest label of a column), trunk_gap (parent
      box to its vertical trunk), edge_color, edge_width, key_color, pos_color,
      node_color: as named.
    """
    ks = key_size or size
    ls = leaf_size or size
    ns = node_size or size
    gap = row_gap or 0.025 * ls
    opens = None if open is None else [tuple(p) for p in open]

    def on_path(p):
        return opens is None or p == () or any(q[:len(p)] == p for q in opens)

    def ends_at(p):
        return opens is None or any(q == p for q in opens)

    def through(p, k):
        return opens is None or any(len(q) > len(p) and q[:len(p)] == p and q[len(p)] == k
                                    for q in opens)

    def build(v, p, depth, label, lk):
        if isinstance(v, (dict, list)):
            kind = "object" if isinstance(v, dict) else "array"
            if not on_path(p):
                return _Item("stub", p, depth, v, label, lk, n=len(v))
            it = _Item(kind, p, depth, v, label, lk)
            entries = list(v.items()) if kind == "object" else list(enumerate(v))
            if kind == "object":
                show_all = ends_at(p) or not (elide_keys and opens is not None and depth >= 1)
            else:
                show_all = ends_at(p)
            run = []

            def flush():
                if not run:
                    return
                if kind == "array":
                    a, b = run[0], run[-1]
                    lab = f"{a}" if a == b else f"{a}–{b}"
                    it.children.append(_Item("more", p + (("more", a),), depth + 1,
                                             label=lab, label_kind="pos", n=len(run)))
                else:
                    it.children.append(_Item("more", p + (("more", run[0]),), depth + 1,
                                             label=None, label_kind=None, n=len(run)))
                run.clear()

            for k, cv in entries:
                if show_all or through(p, k):
                    flush()
                    it.children.append(build(cv, p + (k,), depth + 1, str(k),
                                             "key" if kind == "object" else "pos"))
                else:
                    run.append(k)
            flush()
            return it
        return _Item("leaf", p, depth, v, label, lk)

    root = build(value, (), 0, None, None)

    # rows (depth-first) and the flat item list
    items = []
    row = [0]

    def place_rows(it):
        items.append(it)
        if it.children:
            for c in it.children:
                place_rows(c)
            it.y = (it.children[0].y + it.children[-1].y) / 2
        else:
            it.y = -row[0] * gap
            row[0] += 1

    place_rows(root)

    # mobjects
    for it in items:
        if it.kind in ("object", "array"):
            txt = Mono("{ }" if it.kind == "object" else "[ ]", size=ns, color=node_color)
            box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36,
                                   height=txt.height + 0.18).set_stroke(node_color, 2.5)
            box.set_fill(BG, 1)
            txt.move_to(box)
            m = VGroup(box, txt)
            m.box, m.text = box, txt
        elif it.kind == "stub":
            txt = Mono("{…}" if isinstance(it.value, dict) else "[…]", size=ns,
                       color=node_color).set_opacity(0.7)
            m = VGroup(txt)
            m.box, m.text = None, txt
            if counts:
                cnt = Mono(str(it.n), size=ls, color=DIM).next_to(txt, RIGHT, buff=0.15)
                m.add(cnt)
                m.count = cnt
        elif it.kind == "more":
            word = "more" if it.label_kind == "pos" else ("more key" if it.n == 1 else "more keys")
            m = T(f"+{it.n} {word}", size=ls, color=DIM)
        else:
            m = _leaf_mob(it.value, ls)
        it.mob = m
        it.lab = None
        if it.label is not None:
            it.lab = Mono(it.label, size=ks, color=key_color if it.label_kind == "key" else pos_color)

    # columns
    maxd = max(it.depth for it in items)
    col_w = [0.0] * (maxd + 1)
    lab_w = [0.0] * (maxd + 1)
    for it in items:
        if it.children:
            col_w[it.depth] = max(col_w[it.depth], it.mob.width)
            for c in it.children:
                if c.lab is not None:
                    lab_w[it.depth] = max(lab_w[it.depth], c.lab.width)
    xs = [0.0]
    for d in range(maxd):
        xs.append(xs[d] + col_w[d] + trunk_gap + 0.16 + max(lab_w[d], 0.2) + label_pad)

    for it in items:
        it.mob.move_to([xs[it.depth] + it.mob.width / 2, it.y, 0])

    tree = JsonTree()
    tree.nodes, tree.edges, tree.labels, tree.kinds = {}, {}, {}, {}
    tree.paths = [it.path for it in items]
    edges, labels = [], []
    for it in items:
        tree.nodes[it.path] = it.mob
        tree.kinds[it.path] = it.kind
        if not it.children:
            continue
        d = it.depth
        tx = xs[d] + col_w[d] + trunk_gap
        for c in it.children:
            end = np.array([xs[d + 1] - 0.08, c.y, 0])
            stop = np.array([tx + 0.1, c.y, 0]) if c.lab is not None else end
            pts = [it.mob.get_right(), np.array([tx, it.y, 0]), np.array([tx, c.y, 0]), stop]
            clean = [pts[0]]
            for q in pts[1:]:
                if np.linalg.norm(q - clean[-1]) > 1e-6:
                    clean.append(q)
            e = VMobject().set_points_as_corners(clean)
            if c.lab is not None:
                c.lab.move_to([tx + 0.16 + c.lab.width / 2, c.y, 0])
                a = np.array([c.lab.get_right()[0] + 0.12, c.y, 0])
                if end[0] - a[0] > 0.05:
                    e.start_new_path(a)
                    e.add_line_to(end)
                tree.labels[c.path] = c.lab
                labels.append(c.lab)
            e.set_stroke(edge_color, edge_width)
            tree.edges[c.path] = e
            edges.append(e)
    tree.add(*edges, *labels, *[it.mob for it in items])
    tree.root = tree.nodes[()]
    tree.move_to(ORIGIN)
    return tree


# ══ Ada Lovelace (slide 70) ════════════════════════════════════════════════════

ADA_SRC = """{
  "name": "Ada Lovelace",
  "born": 1815,
  "languages": ["English", "French"],
  "address": {"city": "London", "country": "UK"},
  "programmer": true,
  "email": null
}"""


def ada_value():
    """Slide 70's object as a Python dict, key order as on the slide."""
    return json.loads(ADA_SRC)


def ada_code(size=30):
    """Slide 70's object as Code(lang="json"): `{ } [ ]` TEAL, null PINK (keys FG,
    strings and numbers GOLD, true BLUE). 8 lines; at 30 it is ~12.2 × 4.2."""
    code = Code(ADA_SRC, size=size, lang="json")
    for ch in "{}[]":
        for g in chars(code, ch):
            g.set_color(TEAL)
    code.find("null").set_color(PINK)
    return code


def ada_tree(**kw):
    """json_tree(ada_value(), **kw): fully expanded, 8 rows."""
    return json_tree(ada_value(), **kw)


# ══ The Kid (tt0012349), as stored in movies-json.duckdb ═══════════════════════

KID_JSON = r'''{"movie_id": "tt0012349", "title": "The Kid", "year": 1921, "type": "movie", "minutes": 68, "genres": ["Comedy", "Drama", "Family"], "rating": 8.2, "rating_votes": 142991, "actors": [{"person_id": "nm0000122", "name": "Charles Chaplin", "roles": ["A Tramp"]}, {"person_id": "nm0701012", "name": "Edna Purviance", "roles": ["The Woman"]}, {"person_id": "nm0001067", "name": "Jackie Coogan", "roles": ["The Child"]}, {"person_id": "nm0588033", "name": "Carl Miller", "roles": ["The Man"]}, {"person_id": "nm0042317", "name": "Albert Austin", "roles": ["Car Thief", "Man in Shelter"]}, {"person_id": "nm0047800", "name": "Beulah Bains", "roles": ["Bride"]}, {"person_id": "nm0048798", "name": "Nellie Bly Baker", "roles": ["Slum Nurse"]}, {"person_id": "nm0074788", "name": "Henry Bergman", "roles": ["Professor Guido", "Night Shelter Keeper"]}, {"person_id": "nm0080930", "name": "Edward Biby", "roles": ["Orphan Asylum Driver"]}, {"person_id": "nm0088471", "name": "B.F. Blinn", "roles": ["His Assistant"]}], "directors": [{"person_id": "nm0000122", "name": "Charles Chaplin", "job": "director"}], "producers": [{"person_id": "nm0000122", "name": "Charles Chaplin", "job": "producer"}], "writers": [{"person_id": "nm0000122", "name": "Charles Chaplin", "job": "written by"}], "composers": [{"person_id": "nm0000122", "name": "Charles Chaplin", "job": "composer"}], "trivia_entries": ["Due to the fact that Jackie Coogan's mother and stepfather had spent all the youngster's money before he reached adulthood, the \"Coogan Bill\" was enacted to ensure that child actors' funds would never again be able to be squandered by their parents or guardians.", "The off-screen chemistry between Sir Charles Chaplin and Jackie Coogan was just as strong as their onscreen relationship. Every Sunday, during the first few weeks of filming, Chaplin would take Jackie to amusement parks and pony rides and other activities. Some have seen Chaplin's relationship with Coogan as an attempt for Chaplin to reclaim his own unhappy childhood, while others have interpreted Chaplin's attention toward the boy as recasting Coogan into the child he had just lost.", "This was Sir Charles Chaplin's first feature length film he directed.", "Sir Charles Chaplin and Jackie Coogan met for the last time in 1972, during Chaplin's brief return to America for an Honorary Academy Award.", "The production company tried to cheat Sir Charles Chaplin by paying him for this six-reel film what they would ordinarily pay him for a two-reel film, which was about $500,000. Chaplin took the unassembled film out of state until the company agreed to the $1.5 million he was supposed to be paid, plus half the surplus profits on rentals, along with reversion of the film to him after five years on the rental market."]}'''

KID_PATH = ("actors", 0, "roles", 0)


def kid_value():
    """The Kid's stored document (14 top-level keys, 10 actors, 5 trivia entries)."""
    return json.loads(KID_JSON)


def kid_tree(**kw):
    """The Kid with only actors -> [0] -> roles -> [0] ("A Tramp") opened: 14 top-level
    keys (scalars as leaves, genres/directors/.../trivia_entries as stubs), actors 1–9
    merged into "+9 more"; Chaplin's person_id and name shown (elide_keys=True folds
    them into "+2 more keys"). Defaults elide_keys=True, size=26, row_gap=0.42: 16 rows, ~11.7 × 6.95
    (elide_keys=False: 17 rows); at size 26 it needs most of the frame.
    Any json_tree option can be passed."""
    opts = dict(open=[KID_PATH], elide_keys=True, size=26, row_gap=0.42,
                label_pad=0.32, trunk_gap=0.15)
    opts.update(kw)
    return json_tree(kid_value(), **opts)


# ══ the scene ══════════════════════════════════════════════════════════════════

XML_SRC = """<person>
  <name>Ada Lovelace</name>
  <born>1815</born>
</person>"""

ADA_KEYS = ['"name"', '"born"', '"languages"', '"address"', '"programmer"', '"email"']


def json_icon(scale=1.0):
    """The TEAL `{ }` badge used in the last clip."""
    txt = Mono("{ }", size=64, color=TEAL)
    box = RoundedRectangle(corner_radius=0.2, width=txt.width + 0.9, height=1.3).set_stroke(TEAL, 4)
    txt.move_to(box)
    return VGroup(box, txt).scale(scale)


def chip(text):
    lab = T(text, 32)
    box = RoundedRectangle(corner_radius=0.18, width=lab.width + 0.7, height=0.8).set_stroke(TEAL, 3)
    lab.move_to(box)
    return VGroup(box, lab)


class JsonInTwoMinutes(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── what JSON is; Ada's object; keys ─────────────────────────────────────
    def clip1(self):
        with self.say("c4.json.1") as c:
            title = T("JSON", 96).move_to(UP * 1.3)
            full = T("JavaScript Object Notation", 44).next_to(title, DOWN, buff=0.45)
            for i in (0, 10, 16):
                full[i].set_color(YELLOW)
            self.play(*appear(title, shift=None), run_time=1.0)  # early: the title is the topic word itself
            c.wait_until("JavaScript Object Notation")
            self.play(*appear(full), run_time=1.0)

            c.wait_until("origin")
            js_box = RoundedRectangle(corner_radius=0.2, width=5.4, height=2.6).set_stroke(BLUE, 3)
            js_box.move_to([-3.4, -1.4, 0])
            js_lab = T("JavaScript", 34, BLUE).next_to(js_box.get_corner(UL), DR, buff=0.25)
            inner = VGroup(RoundedRectangle(corner_radius=0.15, width=3.2, height=0.9).set_stroke(TEAL, 3),
                           T("data values", 32, TEAL))
            inner[1].move_to(inner[0])
            inner.move_to(js_box).shift(DOWN * 0.35)
            self.play(*during([VGroup(title, full).animate.shift(UP * 1.4)], 0, 0.6),
                      *during(appear(js_box, js_lab, lag=0.2), 0.4, 1), run_time=1.6)
            c.wait_until(own_word=inner[1])
            self.play(*appear(inner), run_time=0.9)

            c.wait_until("is now")
            jbox = RoundedRectangle(corner_radius=0.2, width=3.6, height=1.5).set_stroke(TEAL, 4)
            jlab = T("JSON", 48, TEAL).move_to(jbox)
            jgrp = VGroup(jbox, jlab).move_to([3.5, -1.4, 0])
            self.play(*fly(inner, jgrp), run_time=min(1.5, c.until("ada")))

            c.wait_until("a record about")
            code = ada_code(30)
            code.to_edge(LEFT, buff=0.5).set_y(-0.25)
            self.code = code
            sweep_clear(self, *appear(code, shift=None), run_time=min(2.0, c.until("braces")))

            c.wait_until("braces")
            ob = code.find("{")
            cb = code.find("}", line=7)
            self.play(FlashAround(ob, color=TEAL, run_time=1.4, time_width=1.5),
                      FlashAround(cb, color=TEAL, run_time=1.4, time_width=1.5))
            obj = T("object: key-value pairs", 32, TEAL).next_to(code, UP, buff=0.45).align_to(code, LEFT)
            self.obj_lab = obj
            c.wait_until(own_word=obj)
            self.play(*appear(obj), run_time=1.0)

            c.wait_until("keys")
            uls = [underline(code.find(k), YELLOW, buff=0.07) for k in ADA_KEYS]
            self.uls = uls
            self.play(LaggedStart(*[Create(u) for u in uls], lag_ratio=0.3),
                      run_time=min(2.6, c.until(None)))

    # ── the kinds of value ───────────────────────────────────────────────────
    def clip2(self):
        code = self.code
        with self.say("c4.json.2") as c:
            self.play(*disappear(*self.uls), run_time=min(0.9, c.until("string")))

            def tag(text, color, line):
                return T(text, 30, color).next_to(code.line(line), RIGHT, buff=0.5)

            beats = [("string", '"Ada Lovelace"', GOLD, 1, "number"),
                     ("number", "1815", GOLD, 2, "bools"),
                     ("bools", "true", BLUE, 5, "null"),
                     ("null", "null", PINK, 6, "array")]
            tags = []
            for cue, sub, col, line, nxt in beats:
                c.wait_until(cue)
                t = tag({"bools": "boolean"}.get(cue, cue), col, line)
                tags.append(t)
                self.play(FlashAround(code.find(sub), color=col, time_width=1.5),
                          *appear(t), run_time=min(1.2, c.until(nxt)))

            c.wait_until("array")
            arr = T("array: ordered list", 30, TEAL).next_to(code.line(3), RIGHT, buff=0.4)
            tags.append(arr)
            self.play(FlashAround(code.find('["English", "French"]'), color=TEAL, time_width=1.5),
                      *appear(arr), run_time=1.4)

            c.wait_until("nested")
            box = SurroundingRectangle(code.find('{"city": "London", "country": "UK"}'), color=TEAL,
                                       buff=0.08, corner_radius=0.08).set_stroke(TEAL, 3)
            self.play(FadeIn(box), run_time=1.0)
            self.tags, self.box = tags, box

    # ── a JSON value is a tree ───────────────────────────────────────────────
    def clip3(self):
        code = self.code
        tree = ada_tree(size=30).move_to([0, -0.2, 0])
        self.tree = tree
        with self.say("c4.json.3") as c:
            self.play(*during(disappear(*self.tags, self.obj_lab, self.box), 0, 0.45),
                      *during(disappear(code), 0.3, 1), run_time=2.0)

            c.wait_until("root")
            self.play(*appear(tree.root, shift=None), FlashAround(tree.root, color=TEAL, time_width=1.5),
                      run_time=1.4)

            c.wait_until("edges")
            d1 = tree.children()
            self.play(LaggedStart(*[Create(tree.edge(*p)) for p in d1], lag_ratio=0.15),
                      *appear(*[tree.label(*p) for p in d1], lag=0.15),  # early: the keys were read in clip 1
                      run_time=min(1.6, c.until("leaves")))

            c.wait_until("leaves")
            self.play(*appear(*[tree.node(*p) for p in d1], lag=0.12, shift=None), run_time=1.2)
            sub = tree.children("address")
            self.play(LaggedStart(*[Create(tree.edge(*p)) for p in sub], lag_ratio=0.3),
                      *appear(*[tree.label(*p) for p in sub], *[tree.node(*p) for p in sub],
                              lag=0.15, shift=None),
                      run_time=1.2)

            c.wait_until("inorder")
            for i, p in enumerate(tree.children("languages")):
                self.play(Create(tree.edge(*p)), *appear(tree.label(*p), tree.node(*p), lag=0.3, shift=None),
                          run_time=1.4 if i == 0 else 1.0)
            settle(self, tree)

            c.wait_until("Keep this tree")
            for p in [("address",), ("address", "city")]:
                self.play(VShowPassingFlash(tree.edge(*p).copy().set_stroke(YELLOW, 6), time_width=0.6),
                          run_time=1.1)

    # ── few types: one number, no dates ──────────────────────────────────────
    def clip4(self):
        tree = self.tree
        with self.say("c4.json.4", gap=0.7) as c:
            self.play(*disappear(tree), run_time=1.2)

            c.wait_until("numbers")
            n1 = Mono("1815", 60, GOLD).move_to([-1.8, 1.0, 0])
            n2 = Mono("8.2", 60, GOLD).move_to([1.8, 1.0, 0])
            self.play(*appear(n1, n2, lag=0.3), run_time=1.2)

            c.wait_until("In OCaml")
            ly = -0.05
            oc = T("OCaml:", 32, DIM).move_to([-3.9, ly, 0])
            self.play(*appear(oc), run_time=0.9)
            c.wait_until("int and float")
            li = Mono("int", 34, DIM).next_to(n1, DOWN, buff=0.45).set_y(ly)
            lf = Mono("float", 34, DIM).next_to(n2, DOWN, buff=0.45).set_y(ly)
            self.play(*appear(li, lf, lag=0.3), run_time=1.0)

            c.wait_until("both are simply numbers")
            js = T("JSON:", 32, DIM).move_to(oc)
            num = T("number", 36, GOLD).move_to([0, ly, 0])
            self.play(*swap(oc, js),
                      *during([li.animate.shift(RIGHT * 0.6).set_opacity(0),
                               lf.animate.shift(LEFT * 0.6).set_opacity(0)], 0, 0.45),
                      *during(appear(num, shift=None), 0.5, 1),
                      FlashAround(VGroup(n1, n2), color=GOLD, time_width=1.5),
                      run_time=1.6)
            self.remove(li, lf)

            c.wait_until("dates")
            date = Code('"date": "2026-10-27"', size=44, lang="json").move_to([0, -1.75, 0])
            d1 = T("a string,", 32, GOLD)
            d2 = T("not a date", 32, RED)
            VGroup(d1, d2).arrange(RIGHT, buff=0.2).next_to(date, DOWN, buff=0.45)
            self.play(*appear(date), run_time=1.0)
            self.play(*appear(d1, d2, lag=0.3), run_time=1.0)  # early: the caption states the point of the sentence
            c.wait_until("written as")
            self.play(FlashAround(date.find('"2026-10-27"'), color=GOLD, time_width=1.5), run_time=1.2)

    # ── everywhere: web, config, logs; Python; XML; one format end to end ─────
    def clip5(self):
        with self.say("c4.json.5", gap=2.6) as c:
            icon = json_icon().move_to([0, 2.55, 0])
            sweep_clear(self, *appear(icon, shift=None), run_time=1.6)

            c.wait_until("web")
            chips = [chip("web APIs"), chip("configuration files"), chip("logs")]
            VGroup(*chips).arrange(RIGHT, buff=0.6).move_to([0, 0.75, 0])
            self.play(*appear(chips[0]), run_time=1.0)
            c.wait_until(own_word=chips[1][1])
            self.play(*appear(chips[1]), run_time=1.0)
            c.wait_until(own_word=chips[2][1])
            self.play(*appear(chips[2]), run_time=1.0)

            c.wait_until("python")
            self.play(FlashAround(icon, color=TEAL, time_width=1.5), run_time=1.4)

            py = T("Python:", 32, YELLOW)
            m1 = T("object → dict", 34, t2c={"object": TEAL, "→": DIM})
            m2 = T("array → list", 34, t2c={"array": TEAL, "→": DIM})
            VGroup(py, m1, m2).arrange(RIGHT, buff=0.7).move_to([0, -0.85, 0])
            c.wait_until("In Python")
            self.play(*appear(py, m1, lag=0.4), run_time=1.2)
            c.wait_until(own_word=m2)
            self.play(*appear(m2), run_time=1.0)

            c.wait_until("xml")
            xml = Code(XML_SRC, size=28, lang="xml").set_color(DIM).move_to([0, -2.5, 0])
            self.play(*appear(xml, shift=None), run_time=1.0)
            c.wait_until("fallen out of favour")
            self.play(xml.animate.set_opacity(0.35), run_time=1.2)

            c.wait_until("same")
            xs = [-4.6, 0, 4.6]
            stops = [json_icon(0.6).move_to([x, 0.05, 0]) for x in xs]
            names = [T(n, 34).next_to(s, DOWN, buff=0.35) for n, s in zip(["database", "server", "browser"], stops)]
            arrows = [Arrow(stops[i].get_right(), stops[i + 1].get_left(), buff=0.3, color=TEAL, stroke_width=4)
                      for i in range(2)]
            flies = []
            for s in stops:
                flies += fly(icon, s)
            sweep_clear(self, *flies, keep=[icon, xml], run_time=2.0)
            self.play(*appear(*names, lag=0.25), *[GrowArrow(a) for a in arrows],
                      run_time=min(1.2, c.until(None)))
