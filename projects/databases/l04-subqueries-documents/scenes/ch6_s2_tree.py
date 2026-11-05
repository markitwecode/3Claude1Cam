"""Chapter 6, scene 2: what fits in a tree. Clips c6.tree.1 – c6.tree.3.

Exports `recap_thumb()`: The Kid's trimmed tree (title, rating, rating_votes, the five
trivia entries) with the GREEN one-parent ticks on every leaf edge, no caption (s7's {r1}).
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
S = load_scene("ch1_s2_schema")

TT = "tt0012349"
# opening words of The Kid's five stored trivia entries (verbatim prefixes)
TRIVIA = [
    "Due to the fact that Jackie…",
    "The off-screen chemistry…",
    "This was Sir Charles Chaplin's…",
    "Sir Charles Chaplin and Jackie…",
    "The production company tried…",
]
_KID = J.kid_value()
TRIM = {"title": _KID["title"], "rating": _KID["rating"], "rating_votes": _KID["rating_votes"],
        "trivia_entries": TRIVIA}
LEAVES = [("rating",), ("rating_votes",)] + [("trivia_entries", i) for i in range(5)]
COMMON = [("title",), ("rating",), ("rating_votes",), ("trivia_entries",)]
OPEN_SCALE = 0.84
RIGHT_X = 3.85


def tree_closed():
    """The trimmed tree, trivia_entries collapsed to a stub, default size, left half."""
    t = J.json_tree(TRIM, open=[])
    t.move_to([0, -0.35, 0]).align_to([-6.5, 0, 0], LEFT)
    return t


def tree_open():
    """The trimmed tree with trivia_entries opened, centred (scaled to fit the width)."""
    t = J.json_tree(TRIM, open=[("trivia_entries",)], label_pad=0.8)
    t.scale(OPEN_SCALE).move_to([0, -0.1, 0])
    return t


def ticks(tree):
    """One small GREEN tick on the single edge above each leaf."""
    out = []
    for p in LEAVES:
        end = tree.edge(*p).get_all_points()[-1]
        a = tree.label(*p).get_right()[0] + 0.08
        tk = check_mark(GREEN).scale(0.55).set_stroke(width=5)
        tk.move_to([(a + end[0]) / 2, end[1] + 0.04, 0])
        out.append(tk)
    return out


def recap_thumb():
    t = tree_open()
    return VGroup(t, *ticks(t))


def join_formula(right_name):
    a = Mono("movies", 30, BLUE)
    bt = MathTex(r"\bowtie", font_size=52, color=FG)
    sub = Mono("movie_id", 24, DIM)
    b = Mono(right_name, 30, BLUE)
    bt.next_to(a, RIGHT, buff=0.18)
    sub.next_to(bt, RIGHT, buff=0.04).align_to(bt, DOWN).shift(DOWN * 0.16)
    b.next_to(sub, RIGHT, buff=0.18).align_to(a, DOWN)
    return VGroup(a, bt, sub, b)


def strip_item(label, pair, x):
    lab = T(label, 30, DIM)
    pr = T(pair, 28, DIM)
    g = VGroup(lab, pr).arrange(DOWN, buff=0.12).move_to([x, 3.15, 0])
    g.lab, g.pair = lab, pr
    return g


def light(item, on=True):
    return [item.lab.animate.set_color(YELLOW if on else DIM),
            item.pair.animate.set_color(FG if on else DIM)]


def copies(*mobs):
    return VGroup(*[m.copy() for m in mobs])


class WhatFitsInATree(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── one-to-one ──────────────────────────────────────────────────────────
    def clip1(self):
        with self.say("c6.tree.1") as c:
            self.strip = [strip_item("one-to-one", "movie — rating", -4.6),
                          strip_item("one-to-many", "movie — trivia entries", 0),
                          strip_item("many-to-many", "movies — people", 4.6)]
            self.play(*appear(*self.strip, lag=0.5), run_time=2.0)  # early: the three shapes shown whole, then walked
            c.wait_until("one")
            self.play(*light(self.strip[0]), run_time=1.0)
            c.wait_until("a movie has one rating")
            self.t1 = tree_closed()
            self.rcard = S.TableCard("ratings", RIGHT_X, 2.45)
            self.mcard = S.TableCard("movies", RIGHT_X, -0.7)
            self.play(*appear(self.t1, self.rcard, self.mcard, shift=None, lag=0.4),  # early: tree and cards are the board the clip walks
                      run_time=2.0)
            c.wait_until("keys")
            self.play(FlashAround(copies(self.t1), run_time=1.6, time_width=1.5))
            c.wait_until("the rating and its")
            t = self.t1
            self.play(*[FlashAround(copies(t.label(*p), t.node(*p)), run_time=1.6, time_width=1.5)
                        for p in [("rating",), ("rating_votes",)]],
                      *recolor([t.label("rating"), t.label("rating_votes")], YELLOW), run_time=1.6)
            c.wait_until("next to the title")
            self.play(FlashUnder(t.label("title").copy(), run_time=1.2, time_width=1.5, color=FG))
            c.wait_until("table")
            rt = S.kid_table("ratings")
            S.place(rt, top=2.45)
            rt.set_x(RIGHT_X)
            h = rt.head[0]
            ul = Line(h.get_corner(DL) + DOWN * 0.07, h.get_corner(DR) + DOWN * 0.07).set_stroke(FG, 2.5)
            self.rrow = VGroup(rt, ul)
            self.play(*swap(self.rcard, self.rrow), run_time=1.4)
            c.wait_until("movie id")
            self.play(FlashUnder(h.copy(), run_time=1.4, time_width=1.5))
            c.wait_until("join")
            self.j1 = join_formula("ratings").move_to([RIGHT_X, 0.2, 0])
            self.play(*appear(self.j1), run_time=0.8)

    # ── one-to-many ─────────────────────────────────────────────────────────
    def clip2(self):
        with self.say("c6.tree.2") as c:
            t1, t2 = self.t1, tree_open()
            stub = ("trivia_entries",)
            moves = []
            for p in COMMON:
                if p != stub:
                    moves.append(Transform(t1.node(*p), t2.node(*p).copy()))
                moves.append(Transform(t1.label(*p), t2.label(*p).copy()))
                moves.append(Transform(t1.edge(*p), t2.edge(*p).copy()))
            moves.append(Transform(t1.root, t2.root.copy()))
            self.play(*light(self.strip[0], False), *light(self.strip[1]), run_time=1.0)
            c.wait_until("many trivia")
            self.play(*during(disappear(self.rrow, self.j1, self.mcard), 0, 0.45),
                      *during([FadeOut(t1.node(*stub))], 0, 0.4),
                      *during(moves, 0.2, 1),
                      *during([FadeIn(t2.node(*stub))], 0.55, 1),
                      run_time=2.0)
            self.remove(*t1.get_family())
            kids = []
            for i in range(5):
                kids += t2.branch("trivia_entries", i)
            self.add(*[m for m in t2.submobjects if m not in kids])
            self.play(*appear(*kids, shift=None, lag=0.12), run_time=1.8)
            settle(self, t2)
            self.t2 = t2
            c.wait_until("nest")
            self.play(FlashAround(copies(*t2.subtree("trivia_entries")), run_time=2.0, time_width=1.5),
                      *recolor([t2.label("trivia_entries")], YELLOW), run_time=2.0)
            c.wait_until("read the movie")
            self.play(FlashAround(copies(t2), run_time=2.0, time_width=1.5))
            c.wait_until("rel")
            mv = S.TableCard("movies", -4.6, 1.5)
            sweep_clear(self, *appear(mv, shift=None), keep=self.strip)
            c.wait_until("if there were")
            rows = [[TT, s] for s in TRIVIA]
            tv = S.RowTable("trivia", ["movie_id", "entry"], rows,
                            [[DIM, FG] for _ in rows], size=22)
            box, hline = tv.frame[0], tv.frame[1]
            target_top = mv.row_y("movie_id") + 1.5 * 0.46
            tv.shift(UP * (target_top - box.get_top()[1]) + RIGHT * (-1.6 - box.get_left()[0]))
            dbox = DashedVMobject(box, num_dashes=80).set_stroke(BLUE, 2)
            dh = DashedVMobject(hline, num_dashes=24).set_stroke(BLUE, 2)
            tv.frame.remove(box, hline)
            tv.frame.add(dbox, dh)
            self.play(*appear(tv.label, tv.frame, tv.head, shift=None, lag=0.2), run_time=1.4)
            self.play(*appear(*tv.rows, shift=None, lag=0.25), run_time=1.6)
            c.wait_until("pointing back")
            y = mv.row_y("movie_id")
            fk = S._fk([(box.get_left()[0], y, 0), (mv.box.get_right()[0], y, 0)])
            self.play(GrowArrow(fk[-1]), *recolor([r[0] for r in tv.rows], TEAL),
                      *recolor([mv.rows["movie_id"]], TEAL), run_time=1.5)
            c.wait_until("join2")
            j2 = join_formula("trivia").move_to([0, -2.75, 0])
            self.play(*appear(j2), run_time=1.0)

    # ── why a tree ──────────────────────────────────────────────────────────
    def clip3(self):
        with self.say("c6.tree.3") as c:
            t = tree_open()
            c.wait_until("parent")
            sweep_clear(self, *appear(t, shift=None), *light(self.strip[0]), keep=self.strip)
            tks = ticks(t)
            self.play(*appear(*tks, shift=0.15 * DOWN, lag=0.15), run_time=2.4)
            c.wait_until("owner")
            self.play(*[VShowPassingFlash(t.edge(*p).copy().set_stroke(YELLOW, 6), time_width=0.6)
                        for p in LEAVES[:2]], run_time=1.4)
            c.wait_until("so does every trivia entry")
            self.play(*[VShowPassingFlash(t.edge(*p).copy().set_stroke(YELLOW, 6), time_width=0.6)
                        for p in LEAVES[2:]], run_time=1.4)
            c.wait_until("rule")
            cap = VGroup(T("one owner", 44, YELLOW), MathTex(r"\rightarrow", font_size=52, color=YELLOW),
                         T("nest it inside", 44, YELLOW)).arrange(RIGHT, buff=0.25).move_to([0, -3.2, 0])
            self.play(*appear(cap), run_time=1.2)  # early: the test is put on screen as it is announced ("here's the test")
            st = [check_mark(GREEN).scale(0.7).next_to(it.lab, RIGHT, buff=0.18) for it in self.strip[:2]]
            self.play(*appear(*st, lag=0.3), run_time=1.0)
