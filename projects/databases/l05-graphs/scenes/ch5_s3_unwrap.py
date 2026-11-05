"""Chapter 5, scene 3: from a path to rows (nodes, WITH, range, UNWIND, coalesce). Clips c5.unwrap.1 – c5.unwrap.5.

Shared drawing (imported by ch5 s8, the recap):
  unwrap_table(merged=False, with_vertices=False, size=28) -> VGroup
      merged=False: the zigzag intermediate result, header  i | vs[i].name | vs[i].title,
                    names PINK, titles BLUE, every NULL DIM.
      merged=True:  Slide 108's reply, header  step | vertex, step numbers GOLD.
      with_vertices=True adds the vertex circle (PINK/BLUE) of each row between i and the values.
      Attributes: .heads .rule .digits .names .titles .nulls (zigzag; None where absent)
                  .values (merged) .vertices (or []). Built at this scene's coordinates
                  (x -6.45 … 6.2, y 0.45 … -2.95): scale and move_to it.
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

_s2 = load_scene("ch5_s2_bfs")
lr_path, LR_NAMES, vertex, sp_code = _s2.lr_path, _s2.LR_NAMES, _s2.vertex, _s2.sp_code

REST = ("WITH nodes(path) AS vs\n"
        "UNWIND range(0, size(vs) - 1) AS i\n"
        "RETURN i AS step,\n"
        "       coalesce(vs[i].name, vs[i].title) AS vertex\n"
        "ORDER BY step;")

ROWS = [("Jennifer Lawrence", None), (None, "Mother!"), ("Domhnall Gleeson", None),
        (None, "Harry Potter and the Deathly Hallows: Part 2"), ("Daniel Radcliffe", None)]
VCOLS = [PINK, BLUE, PINK, BLUE, PINK]

# table geometry
ROW_Y = [-0.4 - 0.6 * i for i in range(5)]
HEAD_Y = 0.3
RULE_Y = 0.0
X_I = -6.2          # digit centre
X_HEAD_I = -6.35    # left of the i / step header
X_C = -5.4          # vertex circle centre
X_NAME = -4.9       # left of the name (and merged vertex) column
X_TITLE = -1.25     # left of the title column
TOP_OFF = 0.14      # value tops sit this far above the row's y


def _cell(text, x_left, y, size, color, mono=False):
    t = (Mono if mono else T)(text, size=size, color=color)
    t.move_to((x_left + t.width / 2, 0, 0))
    t.shift((y + TOP_OFF - t.get_top()[1]) * UP)
    return t


def _digit(i, size=32):
    d = Mono(str(i), size=size, color=GOLD)
    return d.move_to((X_I, ROW_Y[i], 0))


def unwrap_table(merged=False, with_vertices=False, size=28):
    """The step table of `nodes(path)` unwound: zigzag (two columns, NULLs) or merged (step | vertex)."""
    g = VGroup()
    g.digits = [_digit(i, size + 4) for i in range(5)]
    g.vertices = [vertex(c, r=0.22).move_to((X_C, ROW_Y[i], 0)) for i, c in enumerate(VCOLS)] if with_vertices else []
    g.names, g.titles, g.nulls, g.values = [], [], [], []
    if merged:
        g.heads = [_cell("step", X_HEAD_I, HEAD_Y, size, FG, mono=True),
                   _cell("vertex", X_NAME, HEAD_Y, size, FG, mono=True)]
        for name, title in ROWS:
            g.values.append(_cell(name or title, X_NAME, 0, size, PINK if name else BLUE))
        for i, v in enumerate(g.values):
            v.shift(ROW_Y[i] * UP)
        right = max(v.get_right()[0] for v in g.values)
    else:
        g.heads = [_cell("i", X_HEAD_I + 0.05, HEAD_Y, size, FG, mono=True),
                   _cell("vs[i].name", X_NAME, HEAD_Y, size, FG, mono=True),
                   _cell("vs[i].title", X_TITLE, HEAD_Y, size, FG, mono=True)]
        for i, (name, title) in enumerate(ROWS):
            y = ROW_Y[i]
            g.names.append(_cell(name, X_NAME, y, size, PINK) if name else None)
            g.titles.append(_cell(title, X_TITLE, y, size, BLUE) if title else None)
            g.nulls.append(_cell("NULL", X_TITLE if name else X_NAME, y, size, DIM, mono=True))
        right = max(t.get_right()[0] for t in g.titles if t is not None)
    g.rule = Line((X_HEAD_I - 0.1, RULE_Y, 0), (right + 0.1, RULE_Y, 0)).set_stroke(DIM, 2)
    g.add(*g.heads, g.rule, *g.digits, *g.vertices,
          *[m for m in g.names + g.titles if m is not None], *g.nulls, *g.values)
    return g


class Unwrap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def box_to(self, glyphs, line):
        return Transform(self.box, token_box(glyphs, self.code.line(line)))

    # ---- c5.unwrap.1: a path is one value; the rest of the query makes a table
    def clip1(self):
        code = sp_code(ret=REST, size=26)
        code.move_to(ORIGIN)
        code.shift((-4.17 - code.get_left()[0]) * RIGHT)
        for i in range(4, 9):
            code.line(i).set_opacity(0)
        self.code = code
        path = lr_path().move_to((code.get_x(), -1.7, 0))
        rest = VGroup(*[code.line(i) for i in range(4, 9)])
        brace = Brace(rest, direction=LEFT, buff=0.1).set_color(DIM)
        tag = T("convenience", size=28, color=DIM).next_to(brace, LEFT, buff=0.1)
        self.brace, self.tag = brace, tag

        with self.say("c5.unwrap.1") as c:
            self.play(*appear(code, path, lag=0.4), run_time=1.6)  # early: the query and its value shown whole
            c.wait_until("rest")
            tgt = code.generate_target()
            for i in range(4):
                tgt.line(i).set_color(DIM)
            for i in range(4, 9):
                tgt.line(i).set_opacity(1)
            self.play(*during(disappear(path), 0, 0.45), *during([MoveToTarget(code)], 0.45, 1), run_time=1.6)
            c.wait_until("convenience")
            self.play(GrowFromCenter(brace), *appear(tag, shift=0.2 * LEFT), run_time=1.2)

    # ---- c5.unwrap.2: nodes(path) is the list of vertices; WITH names it vs
    def clip2(self):
        code = self.code
        tgt = code.generate_target()
        for i in range(4):
            tgt.line(i).set_opacity(0)
        line7_right = tgt.line(7).get_right()[0]
        dx = -(tgt.get_left()[0] + line7_right) / 2
        dy = 3.55 - tgt.line(4).get_top()[1]
        tgt.shift(dx * RIGHT + dy * UP)

        path = lr_path(names=LR_NAMES, pitch=2.6, r=0.3, above_films=True).move_to(ORIGIN)
        path.shift((-1.0 - path.nodes[0].get_y()) * UP)
        pitch = 1.4
        xs = [(i - 2) * pitch for i in range(5)]
        lb = Mono("[", size=72, color=TEAL).move_to((xs[0] - 0.8, -1.0, 0))
        rb = Mono("]", size=72, color=TEAL).move_to((xs[4] + 0.8, -1.0, 0))
        node_tag = T("node = vertex", size=30, color=DIM).move_to((0, -2.9, 0))
        vs = Mono("vs", size=36, color=YELLOW).next_to(lb, LEFT, buff=0.3)
        self.circles, self.lb, self.rb, self.node_tag, self.vs, self.xs = path.nodes, lb, rb, node_tag, vs, xs

        with self.say("c5.unwrap.2") as c:
            self.play(*during(disappear(self.brace, self.tag), 0, 0.4), MoveToTarget(code), run_time=1.2)
            box = token_box(code.find("nodes(path)", line=4), code.line(4))
            self.box = box
            self.play(FadeIn(box), *appear(path), run_time=1.2)
            c.wait_until("nodes", nth=1)
            self.play(*appear(node_tag), run_time=1.0)
            c.wait_until("five")
            self.play(LaggedStart(*flash(path.nodes, color=YELLOW, run_time=1.2, time_width=1.5), lag_ratio=0.25),
                      run_time=2.0)
            c.wait_until("movies")
            moves = [n.animate.move_to((xs[i], -1.0, 0)) for i, n in enumerate(path.nodes)]
            gone = [m for m in path.edges + path.labels if m is not None]
            self.play(*during(disappear(*gone), 0, 0.45), *during(moves, 0.2, 0.8),
                      *during([GrowFromCenter(lb), GrowFromCenter(rb)], 0.55, 1), run_time=1.5)
            for m in gone:
                path.remove(m)
            c.wait_until("with")
            self.play(self.box_to(code.line(4), 4), run_time=1.2)
            c.wait_until("short name")
            self.play(*appear(vs, shift=0.2 * RIGHT), run_time=1.0)

    # ---- c5.unwrap.3: range gives the positions; UNWIND makes one row each
    def clip3(self):
        code, xs = self.code, self.xs
        digits = [Mono(str(i), size=32, color=GOLD).move_to((xs[i], -0.2, 0)) for i in range(5)]
        commas = [Mono(",", size=32, color=DIM).next_to(digits[i], RIGHT, buff=0.04, aligned_edge=DOWN)
                  .shift(0.08 * DOWN) for i in range(4)]
        plb = Mono("[", size=36, color=TEAL).move_to((xs[0] - 0.8, -0.2, 0))
        prb = Mono("]", size=36, color=TEAL).move_to((xs[4] + 0.8, -0.2, 0))
        rule = Line((X_HEAD_I - 0.1, RULE_Y, 0), (X_C + 0.4, RULE_Y, 0)).set_stroke(DIM, 2)
        head_i = unwrap_table().heads[0]

        # the unnest inset
        frame = RoundedRectangle(corner_radius=0.2, width=4.4, height=3.3).set_stroke(DIM, 2).move_to((3.9, -1.25, 0))
        un_word = Mono("unnest", size=30, color=DIM).move_to((3.9, -0.1, 0))
        arr = Mono('["x", "y", "z"]', size=28, color=DIM).move_to((3.9, -0.7, 0))
        elems = [select(arr, f'"{ch}"')[0] for ch in "xyz"]
        rows = [Mono(f'"{ch}"', size=28, color=DIM).move_to((3.9, -1.3 - 0.5 * k, 0)) for k, ch in enumerate("xyz")]
        same = T("same idea", size=30, color=DIM).next_to(frame, DOWN, buff=0.2)
        self.inset = [frame, un_word, arr, *rows, same]
        self.digits, self.rule, self.head_i = digits, rule, head_i

        with self.say("c5.unwrap.3") as c:
            self.play(self.box_to(code.find("range(0, size(vs) - 1)", line=5), 5), run_time=1.2)
            c.wait_until("positions")
            self.play(*appear(plb, prb, shift=None), run_time=0.6)
            for i, word in enumerate(["zero", "one", "two", "three", "four"]):
                c.wait_until(word, nth=1 if i < 2 else 0)
                items = [digits[i]] + ([commas[i]] if i < 4 else [])
                self.play(*appear(*items, lag=0), run_time=0.5)
            c.wait_until("unwind")
            gone = [plb, prb, *commas, self.lb, self.rb, self.vs, self.node_tag]
            moves = ([d.animate.move_to((X_I, ROW_Y[i], 0)) for i, d in enumerate(digits)]
                     + [n.animate.move_to((X_C, ROW_Y[i], 0)).scale(0.22 / 0.3) for i, n in enumerate(self.circles)])
            self.play(*during([self.box_to(code.line(5), 5)], 0, 0.5), *during(disappear(*gone), 0, 0.4),
                      *during(moves, 0.35, 1), run_time=2.2)
            c.wait_until("unnest")
            self.play(FadeIn(frame), *appear(un_word, arr, lag=0.3), run_time=1.2)
            flies = []
            for e, r in zip(elems, rows):
                flies += fly(e, r)
            self.play(*flies, *during(appear(same), 0.5, 1), run_time=1.5)
            c.wait_until("rows")
            self.play(*appear(head_i), GrowFromCenter(rule), run_time=1.0)
            c.wait_until("variable")
            self.play(LaggedStart(*flash(digits, color=GOLD, run_time=1.0, time_width=1.5), lag_ratio=0.15),
                      run_time=min(1.6, c.until(None) - 0.05))

    # ---- c5.unwrap.4: look up name and title; coalesce merges the zigzag
    def clip4(self):
        code = self.code
        zz = unwrap_table()
        mg = unwrap_table(merged=True)
        self.mg = mg

        with self.say("c5.unwrap.4") as c:
            self.play(*disappear(*self.inset),
                      self.box_to(code.find("vs[i].name, vs[i].title", line=7), 7), run_time=1.2)
            self.play(*appear(zz.heads[1], zz.heads[2], lag=0.3), Transform(self.rule, zz.rule), run_time=1.2)
            c.wait_until("name")
            flies = []
            for i in (0, 2, 4):
                flies += fly(self.circles[i], zz.names[i])
            self.play(*flies, run_time=1.5)
            c.wait_until("title")
            flies = []
            for i in (1, 3):
                flies += fly(self.circles[i], zz.titles[i])
            self.play(*flies, run_time=1.5)
            c.wait_until("nulls")
            self.play(*appear(*zz.nulls, lag=0.15), run_time=1.2)
            c.wait_until("coalesce")
            self.play(self.box_to(code.find("coalesce(vs[i].name, vs[i].title)", line=7), 7), run_time=1.2)
            c.wait_until("merge")
            slides = [zz.titles[i].animate.move_to(mg.values[i]) for i in (1, 3)]
            self.play(*during(disappear(*zz.nulls, *self.circles), 0, 0.4),
                      *during(slides, 0.35, 1),
                      *during(disappear(self.head_i, zz.heads[1], zz.heads[2]), 0, 0.4),
                      *during(appear(mg.heads[0], mg.heads[1], lag=0.2), 0.5, 1),
                      *during([Transform(self.rule, mg.rule)], 0.3, 1), run_time=2.0)
            self.values = [zz.names[i] if zz.names[i] is not None else zz.titles[i] for i in range(5)]
            tag = T("no schema:\na property may be missing", size=30, color=DIM, line_spacing=0.9)
            tag.move_to((0, (ROW_Y[0] + ROW_Y[2]) / 2, 0))
            tag.shift((6.5 - tag.get_right()[0]) * RIGHT)
            self.schema = tag
            c.wait_until("schema")
            self.play(*appear(tag), run_time=1.0)

    # ---- c5.unwrap.5: the reply; or RETURN path and let Traverse draw it
    def clip5(self):
        code, digits, values = self.code, self.digits, self.values
        ret = Code("RETURN path", size=34).move_to((-4.3, 2.95, 0))
        drawn = T("Traverse draws it", size=30, color=DIM).next_to(ret, DOWN, buff=0.35)
        path = lr_path(edge_color=YELLOW).move_to((2.6, 2.75, 0))

        with self.say("c5.unwrap.5") as c:
            c.wait_until("step zero")
            self.play(FlashAround(VGroup(digits[0], values[0]), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("step four")
            self.play(FlashAround(VGroup(digits[4], values[4]), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("draw")
            items = []
            for i, n in enumerate(path.nodes):
                items.append(GrowFromCenter(n))
                if path.labels[i] is not None:
                    items.append(FadeIn(path.labels[i], shift=0.15 * DOWN))
                if i < 4:
                    items.append(Create(path.edges[i]))
            self.play(*during(disappear(code, self.box, self.schema), 0, 0.35),
                      *during(appear(ret), 0.35, 0.65),
                      *during([LaggedStart(*items, lag_ratio=0.2)], 0.4, 1), run_time=2.4)  # early: the drawn path, names read with it
            self.play(*appear(drawn), run_time=1.0)
        self.wait(1.5)
