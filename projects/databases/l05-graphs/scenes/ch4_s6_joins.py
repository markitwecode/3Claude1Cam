"""Chapter 4, scene 6: *4 and *6 as SQL joins; the bounce that SQL counts; UNION ALL; shortest. Clips c4.joins.1 – c4.joins.4.

Exports (for the recap):
  sql_block() -> VGroup(code, reply): the six-join DuckDB query (Code size 22, lang="sql") with its
      wrong reply. Parts: .code (Code, 13 lines), .reply (VGroup head, rule, val),
      .head (T "paths" DIM 30), .rule (Line), .val (T "1085" RED 44). Code top-left at
      (CODE_X, CODE_TOP), reply column centred at x = REPLY_X; the whole is ~12.4 wide.
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

CS = 22                 # code size (13 lines of up to 56 characters)
CODE_X = -5.9           # code left edge
CODE_TOP = 2.65
REPLY_X = 5.5
CHAIN_Y = 3.0
CHAIN_SCALE = 0.6
EDGE_COLS = [YELLOW, GOLD, GREEN, PURPLE]
NODE_R = 0.4

HEAD = ("SELECT count(*) AS paths\n"
        "FROM   people AS a\n"
        "JOIN   has_position AS h1 ON h1.person_id = a.person_id\n"
        "JOIN   has_position AS h2 ON h2.movie_id  = h1.movie_id\n"
        "JOIN   has_position AS h3 ON h3.person_id = h2.person_id\n"
        "JOIN   has_position AS h4 ON h4.movie_id  = h3.movie_id\n")
NAMES_W = ("WHERE  a.name = 'Jennifer Lawrence'\n"
           "  AND  b.name = 'Daniel Radcliffe'\n"
           "  AND  h1.position = 'actor' AND h2.position = 'actor'\n")
SQL4 = (HEAD
        + "JOIN   people AS b        ON b.person_id  = h4.person_id\n"
        + NAMES_W
        + "  AND  h3.position = 'actor' AND h4.position = 'actor';")
SQL6 = (HEAD
        + "JOIN   has_position AS h5 ON h5.person_id = h4.person_id\n"
        + "JOIN   has_position AS h6 ON h6.movie_id  = h5.movie_id\n"
        + "JOIN   people AS b        ON b.person_id  = h6.person_id\n"
        + NAMES_W
        + "  AND  h3.position = 'actor' AND h4.position = 'actor'\n"
        + "  AND  h5.position = 'actor' AND h6.position = 'actor';")


def place(code):
    code.move_to(ORIGIN)
    code.shift((CODE_X - code.get_left()[0]) * RIGHT + (CODE_TOP - code.get_top()[1]) * UP)
    return code


def sql_code(src):
    return place(Code(src, size=CS, lang="sql"))


def reply(value, color, center_y):
    head = T("paths", size=30, color=DIM)
    val = T(value, size=44, color=color)
    rule = Line(LEFT * 0.8, RIGHT * 0.8, stroke_width=2, color=DIM)
    g = VGroup(head, rule, val).arrange(DOWN, buff=0.16).move_to([REPLY_X, center_y, 0])
    g.head, g.rule, g.val = head, rule, val
    return g


def sql_block():
    code = sql_code(SQL6)
    rep = reply("1085", RED, code.get_center()[1] + 0.3)
    g = VGroup(code, rep)
    g.code, g.reply, g.head, g.rule, g.val = code, rep, rep.head, rep.rule, rep.val
    return g


def tick(code, i, color):
    ln = code.line(i)
    y = ln.get_center()[1]
    return Line([CODE_X - 0.22, y - 0.16, 0], [CODE_X - 0.22, y + 0.16, 0], stroke_width=7, color=color)


def vertex(name, col, at, side=DOWN, size=30):
    c = Circle(radius=NODE_R, color=col, stroke_width=4).set_fill(col, 0.15).move_to(at)
    n = T(name, size=size, color=col, line_spacing=0.8).next_to(c, side, buff=0.18)
    return c, n


def edge_between(c1, c2, color=DIM, width=4):
    d = c2.get_center() - c1.get_center()
    u = d / np.linalg.norm(d)
    return Line(c1.get_center() + u * (NODE_R + 0.08), c2.get_center() - u * (NODE_R + 0.08),
                stroke_width=width, color=color)


class Joins(NarratedScene):
    def construct(self):
        code, rep8 = self.clip1()
        rep, cy = self.clip2(code, rep8)
        self.clip3(rep, cy)
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- clip 1
    def clip1(self):
        with self.say("c4.joins.1") as c:
            code = sql_code(SQL4)
            self.play(*appear(code, shift=None), run_time=1.0)  # early: the query shown whole, then walked
            c.wait_until("edge")

            ch = load_scene("ch4_s2_chains").chain_example(arrows=False)
            nodes, edges = ch.nodes, ch.edges
            small = VGroup(*nodes, *edges).scale(CHAIN_SCALE, about_point=ORIGIN).shift(CHAIN_Y * UP)
            self.play(*appear(small, shift=None), run_time=min(1.0, c.until("a join")))
            c.wait_until("a join")
            self.play(*flash([code.line(i) for i in range(2, 6)], run_time=1.5, time_width=1.5))
            c.wait_until("four")

            labs = [Mono(f"h{i + 1}", size=28, color=EDGE_COLS[i]).move_to(e.get_center() + 0.36 * UP)
                    for i, e in enumerate(edges)]
            ticks = [tick(code, i + 2, EDGE_COLS[i]) for i in range(4)]
            self.play(*[e.animate.set_color(EDGE_COLS[i]) for i, e in enumerate(edges)],
                      *appear(*ticks, shift=None, lag=0.2), *appear(*labs, lag=0.2),
                      run_time=min(2.0, c.until("restricted")))
            c.wait_until("restricted")
            self.play(*[FlashUnder(code.line(i), color=GREEN, run_time=1.5, time_width=1.5)
                        for i in (9, 10)])
            c.wait_until("people table")

            la = Mono("a", size=28, color=PINK).next_to(nodes[0], LEFT, buff=0.18)
            lb = Mono("b", size=28, color=PINK).next_to(nodes[4], RIGHT, buff=0.18)
            pticks = [tick(code, i, PINK) for i in (1, 6)]
            self.play(*appear(*pticks, shift=None), *appear(la, lb, shift=None),
                      *flash([nodes[0], nodes[4]], color=PINK), run_time=min(1.5, c.until("two names")))
            c.wait_until("two names")
            self.play(*[FlashUnder(code.line(i), color=PINK, run_time=1.2, time_width=1.5) for i in (7, 8)])
            c.wait_until("eight")

            rep = reply("8", FG, code.get_center()[1] + 0.3)
            self.play(*appear(rep.head, rep.rule, rep.val, lag=0.2), run_time=min(1.0, c.until("six")))
            c.wait_until("six")

            code6 = sql_code(SQL6)
            gone = [small, *labs, *ticks, *pticks, la, lb]
            qm = T("?", size=44, color=DIM).move_to(rep.val)
            self.play(*during(disappear(*gone), 0, 0.3), *during(swap(rep.val, qm), 0, 0.4),
                      *during(edit(code, code6), 0.25, 1.0),
                      run_time=min(2.4, c.until("painful")))
            rep.remove(rep.val)
            rep.add(qm)
            rep.val = qm
        return code6, rep

    # ---------------------------------------------------------------- clip 2
    def clip2(self, code, rep):
        with self.say("c4.joins.2") as c:
            c.wait_until("wrong")
            v = T("1085", size=44, color=RED).move_to(rep.val)
            self.play(*swap(rep.val, v), run_time=1.2)
            rep.remove(rep.val)
            rep.add(v)
            rep.val = v
            cy = T("Cypher: 495", size=28, color=GOLD).next_to(rep, DOWN, buff=0.45)
            c.wait_until("not four hundred")
            self.play(*appear(cy), run_time=1.0)  # early: Cypher's count, said in this sentence
            c.wait_until("why")
            self.play(*flash([rep.val], color=RED, run_time=1.5, time_width=1.5))
            c.wait_until("bounce")

            # the walk: Lawrence, Mother!, Gleeson, (back, forth), Harry Potter 8 Part 2, Radcliffe
            Y = -0.6
            specs = [("Jennifer\nLawrence", PINK), ("Mother!", BLUE), ("Domhnall\nGleeson", PINK),
                     ("Harry Potter and\nthe Deathly Hallows:\nPart 2", BLUE), ("Daniel\nRadcliffe", PINK)]
            vs = [vertex(n, col, [2.9 * (i - 2), Y, 0], UP if col == BLUE else DOWN)
                  for i, (n, col) in enumerate(specs)]
            circles = [v[0] for v in vs]
            names = [v[1] for v in vs]
            base = [edge_between(circles[i], circles[i + 1]) for i in range(4)]
            top = VGroup(rep, cy)
            sweep_clear(self, time_span(top.animate.shift((3.4 - top.get_top()[1]) * UP + 0.25 * RIGHT), 0.6, 1.2),  # early: the walk's shape first, then walked
                        *[time_span(FadeIn(m), 1.2, 1.9) for m in (*circles, *base, *names)],
                        keep=[rep, cy], run_time=1.9)
            c.wait_until("the film mother")

            def step_num(k, e, frac=0.5):
                p = e.point_from_proportion(frac)
                return T(str(k), size=34, color=GOLD).move_to(p + 0.42 * DOWN)

            walk = [Line(b.get_start(), b.get_end(), stroke_width=7, color=YELLOW) for b in base]
            nums = []
            n1 = step_num(1, base[0])
            self.play(Create(walk[0]), *appear(n1), run_time=1.0)
            nums.append(n1)
            c.wait_until("gleeson")
            n2 = step_num(2, base[1], 0.2)
            self.play(Create(walk[1]), *appear(n2), run_time=1.0)
            nums.append(n2)
            c.wait_until("back and forth")

            dot = Dot(walk[1].get_end(), radius=0.13, color=RED).set_z_index(3)
            n3, n4 = step_num(3, base[1], 0.45), step_num(4, base[1], 0.7)
            tag = T("same edge again", size=30, color=RED).move_to(base[1].get_center() + 1.4 * UP)
            self.play(FadeIn(dot), walk[1].animate.set_color(RED), run_time=0.5)
            back = Line(walk[1].get_end(), walk[1].get_start())
            self.play(MoveAlongPath(dot, back), *appear(n3), run_time=1.1)
            self.play(MoveAlongPath(dot, walk[1].copy()), *appear(n4), *appear(tag), run_time=1.1)
            nums += [n3, n4]
            c.wait_until("harry potter")
            n5 = step_num(5, base[2])
            self.play(Create(walk[2]), *appear(n5), FadeOut(dot), run_time=1.0)
            c.wait_until("radcliffe")
            n6 = step_num(6, base[3])
            self.play(Create(walk[3]), *appear(n6), run_time=1.0)
            nums += [n5, n6]
            c.wait_until("six2")
            self.play(*flash(nums, color=GOLD, run_time=1.5, time_width=1.5))
            c.wait_until("rule")
            self.play(*flash([cy], color=GOLD, run_time=1.5, time_width=1.5),
                      *flash([tag], color=RED, run_time=1.5, time_width=1.5))
        return rep, cy

    # ---------------------------------------------------------------- clip 3
    def clip3(self, rep, cy):
        with self.say("c4.joins.3") as c:
            C = np.array([0.0, -0.45, 0])
            R = 2.2
            pos = [C + R * LEFT, C + R * UP, C + R * RIGHT, C + R * DOWN]
            specs = [("Jennifer\nLawrence", PINK, LEFT), ("Silver Linings\nPlaybook", BLUE, RIGHT),
                     ("Bradley\nCooper", PINK, RIGHT), ("American\nHustle", BLUE, RIGHT)]
            vs = [vertex(n, col, p, side) for (n, col, side), p in zip(specs, pos)]
            circles = [v[0] for v in vs]
            names = [v[1] for v in vs]
            sweep_clear(self, *[time_span(FadeIn(m), 0.7, 1.4) for m in (circles[0], names[0])],
                        run_time=1.4)
            c.wait_until("loop")
            head = T("112 paths of length 4, from Lawrence back to Lawrence", size=32, color=GOLD)
            head.move_to([0, 3.25, 0])
            self.play(*appear(head), run_time=1.0)
            loop = [edge_between(circles[i], circles[(i + 1) % 4], color=GREEN, width=6) for i in range(4)]
            nums = []
            for i, e in enumerate(loop):
                mid = e.get_center()
                out = (mid - C) / np.linalg.norm(mid - C)
                nums.append(T(str(i + 1), size=34, color=GOLD).move_to(mid + 0.42 * out))
            for k, cue in ((1, "silver"), (2, "bradley"), (3, "american")):
                c.wait_until(cue)
                self.play(Create(loop[k - 1]), FadeIn(nums[k - 1]), FadeIn(circles[k]), *appear(names[k]),
                          run_time=1.0)
            self.play(Create(loop[3]), FadeIn(nums[3]), run_time=0.9)
            c.wait_until("distinct")
            ok = check_mark().scale(1.3).move_to(C)
            self.play(GrowFromCenter(ok), *flash(nums, color=GOLD, run_time=1.2), run_time=1.2)
            c.wait_until("sqlfix")

            blk = sql_block().shift(0.4 * UP)    # no chain above it now
            code6 = blk.code
            r6 = blk.reply
            cy2 = T("Cypher: 495", size=28, color=GOLD).next_to(r6, DOWN, buff=0.45)
            cap = T("+ conditions: no has_position row used twice", size=28, color=DIM)
            cap.next_to(code6, DOWN, buff=0.2).align_to(code6, LEFT)
            sweep_clear(self, *[time_span(FadeIn(m), 0.8, 1.6) for m in (code6, r6, cy2)],  # early: the block comes back whole
                        time_span(FadeIn(cap, shift=0.25 * DOWN), 1.6, 2.4), run_time=2.4)
            c.wait_until("fourok")

            code4 = sql_code(SQL4).shift(0.4 * UP)
            v8 = T("8", size=44, color=GREEN).move_to(r6.val)
            tag = T("a step back would need both in one film", size=30, color=GREEN)
            tag.next_to(code4, DOWN, buff=0.4).align_to(code4, LEFT)
            self.play(*during(disappear(cy2, cap), 0, 0.3), *during(edit(code6, code4), 0.2, 0.8),
                      *swap(r6.val, v8), run_time=2.0)
            self.play(*appear(tag), *flash([v8], color=GREEN, run_time=1.2),
                      run_time=1.2)  # early: the reason, read with the rest of the sentence

    # ---------------------------------------------------------------- clip 4
    def clip4(self):
        with self.say("c4.joins.4") as c:
            c.wait_until("star two")
            pat = Code("-[:ACTED_IN*2..6]-", size=36).move_to([-1.0, 2.9, 0])
            sweep_clear(self, time_span(FadeIn(pat), 0.6, 1.2), run_time=1.2)  # early: the range, read next
            c.wait_until("one such query")

            blocks, unions = [], []
            ys = [1.55, -0.45, -2.45]
            for k, y in zip((2, 4, 6), ys):
                box = RoundedRectangle(corner_radius=0.15, width=6.4, height=1.0, color=BLUE,
                                       stroke_width=3).move_to([-1.0, y, 0])
                q = Code("SELECT count(*) …", size=28, lang="sql").move_to(box).align_to(box, LEFT).shift(0.3 * RIGHT)
                n = T(f"{k} joins", size=30, color=GOLD).move_to(box).align_to(box, RIGHT).shift(0.3 * LEFT)
                blocks.append(VGroup(box, q, n))
            for y in (0.55, -1.45):
                unions.append(Code("UNION ALL", size=28, lang="sql").move_to([-1.0, y, 0]))
            for b, (cue, nth) in zip(blocks, (("two", 1), ("four", 0), ("and six", 0))):
                c.wait_until(cue, nth=nth)
                self.play(*appear(b), run_time=0.9)
            c.wait_until("union all")
            self.play(*appear(*unions, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("question")

            q = T("shortest chain, however long?", size=44, color=YELLOW).move_to([0, 2.9, 0])
            self.play(*swap(pat, q), *set_alpha(blocks + unions, DIMMED), run_time=1.5)
            c.wait_until("joins")
            qj = T("? joins", size=48, color=GOLD).move_to([4.6, -0.45, 0])
            self.play(*appear(qj), run_time=1.0)
            c.wait_until("cypher")

            t1 = T("Cypher: next part", size=30, color=BLUE)
            t2 = T("SQL: recursive queries, next lecture", size=30, color=DIM)
            VGroup(t1, t2).arrange(RIGHT, buff=1.0).move_to([0, -3.45, 0])
            self.play(*appear(t1), run_time=1.0)
            c.wait_until(own_word=t2)
            self.play(*appear(t2), run_time=1.0)
        self.wait(2.5)
