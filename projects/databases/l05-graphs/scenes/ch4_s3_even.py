"""Chapter 4, scene 3: why the path length between two actors is always even. Clips c4.even.1 – c4.even.4.

Exports:
  banks(walk=False) -> VGroup: the bipartite picture, people (PINK) left, movies (BLUE) right.
      .rects[2] (bank RoundedRectangles: 0 people, 1 movies)  .heads[2] (T 40 "people"/"movies")
      .people[6] .movies[6] (T 30 names)  .pdots[6] .mdots[6] (Dots where edges attach)
      .lines[12] (ACTED_IN Lines)  .walk[4] (indices into .lines of the token's zigzag:
      Lawrence -> Catching Fire -> Harrelson -> Now You See Me 2 -> Radcliffe)
      walk=True: the zigzag lines YELLOW and .token (YELLOW Dot) on Radcliffe's dot.
  pill_strip(with_actors=True) -> VGroup centred on ORIGIN (pills row at y = 0).
      .pills[5] (each VGroup with .box RoundedRectangle, .star Mono "*k", .count Mono; k = 2..6,
      counts 0 0 8 0 495)  .actors (VGroup: PINK "Jennifer Lawrence", DashedLine, PINK
      "Daniel Radcliffe", 1.9 above the pills; empty when with_actors=False)
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

PEOPLE = ["Jennifer Lawrence", "Woody Harrelson", "Daniel Radcliffe",
          "Liam Hemsworth", "Emma Watson", "Jesse Eisenberg"]
MOVIES = ["Catching Fire", "Now You See Me 2", "The Hunger Games",
          "Mockingjay", "Zombieland", "Deathly Hallows"]
EDGES = [(0, 0), (1, 0), (1, 1), (2, 1),            # the walk comes first
         (0, 2), (0, 3), (1, 4), (2, 5), (3, 2), (3, 3), (4, 5), (5, 4)]
WALK = [0, 1, 2, 3]
ROW_Y = [1.9 - 0.75 * i for i in range(6)]
DOT_X = 2.3
TYPES = ["ACTED_IN", "DIRECTED", "PRODUCED", "WROTE", "COMPOSED_FOR"]
QUERY = ("MATCH path = (a:Person {name: 'Jennifer Lawrence'})\n"
         "             -[:ACTED_IN*3]- (x)\n"
         "RETURN labels(x) AS label, count(path) AS paths;")
PILLS = [("*2", "0"), ("*3", "0"), ("*4", "8"), ("*5", "0"), ("*6", "495")]
PILL_PITCH = 2.6


def banks(walk=False):
    rects, heads = [], []
    for side, (word, col) in enumerate([("people", PINK), ("movies", BLUE)]):
        sx = -1 if side == 0 else 1
        r = RoundedRectangle(corner_radius=0.3, width=4.5, height=4.9)
        r.set_stroke(DIM, 2, opacity=0.5).set_fill(col, 0).move_to([sx * 4.2, 0.05, 0])
        h = T(word, size=40, color=col).move_to([sx * 4.2, 3.05, 0])
        rects.append(r)
        heads.append(h)
    people, movies, pdots, mdots = [], [], [], []
    for i, y in enumerate(ROW_Y):
        pd = Dot([-DOT_X, y, 0], radius=0.07, color=PINK)
        md = Dot([DOT_X, y, 0], radius=0.07, color=BLUE)
        pn = T(PEOPLE[i], size=30, color=PINK)
        pn.move_to([-DOT_X - 0.3 - pn.width / 2, y, 0])
        mn = T(MOVIES[i], size=30, color=BLUE)
        mn.move_to([DOT_X + 0.3 + mn.width / 2, y, 0])
        people.append(pn)
        movies.append(mn)
        pdots.append(pd)
        mdots.append(md)
    lines = [Line(pdots[p].get_center(), mdots[m].get_center(), stroke_width=3,
                  color=FG).set_stroke(opacity=0.6) for p, m in EDGES]
    g = VGroup(*rects, *heads, *lines, *pdots, *mdots, *people, *movies)
    g.rects, g.heads, g.people, g.movies = rects, heads, people, movies
    g.pdots, g.mdots, g.lines, g.walk = pdots, mdots, lines, list(WALK)
    if walk:
        for k in WALK:
            lines[k].set_stroke(YELLOW, 5, opacity=1)
        g.token = Dot(pdots[2].get_center(), radius=0.14, color=YELLOW).set_z_index(5)
        g.add(g.token)
    return g


def pill_strip(with_actors=True):
    pills = []
    for i, (star, n) in enumerate(PILLS):
        s = Mono(star, size=36)
        k = Mono(n, size=36, color=FG)
        inner = VGroup(s, k).arrange(RIGHT, buff=0.35)
        box = RoundedRectangle(corner_radius=0.42, width=2.2, height=0.9)
        box.set_stroke(DIM, 3).set_fill(BG, 1)
        p = VGroup(box, s, k)
        inner.move_to(box)
        p.box, p.star, p.count = box, s, k
        p.move_to([PILL_PITCH * (i - 2), 0, 0])
        pills.append(p)
    actors = VGroup()
    if with_actors:
        a = T("Jennifer Lawrence", size=36, color=PINK)
        b = T("Daniel Radcliffe", size=36, color=PINK)
        a.move_to([-3.6, 1.9, 0])
        b.move_to([3.6, 1.9, 0])
        d = DashedLine(a.get_right() + 0.3 * RIGHT, b.get_left() + 0.3 * LEFT, color=DIM,
                       stroke_width=3, dash_length=0.12)
        actors = VGroup(a, d, b)
    g = VGroup(*pills, actors)
    g.pills, g.actors = pills, actors
    return g


def light(bk, side):
    """The landing side lights up in its colour; the other goes dark."""
    out = []
    for s, col in ((0, PINK), (1, BLUE)):
        r = bk.rects[s]
        if s == side:
            out.append(r.animate.set_fill(col, 0.14).set_stroke(col, 3, opacity=0.9))
        else:
            out.append(r.animate.set_fill(col, 0).set_stroke(DIM, 2, opacity=0.5))
    return out


class Even(NarratedScene):
    def construct(self):
        ch = load_scene("ch4_s2_chains").handover_shot()
        self.add(ch)
        bk = self.clip1(ch)
        self.clip2(bk)
        strip = self.clip3()
        self.clip4(ch, strip)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- clip 1
    def clip1(self, ch):
        with self.say("c4.even.1") as c:
            so_far = T("lengths so far: 2 and 4", size=40, t2c={"2": GOLD, "4": GOLD}).move_to(0.3 * DOWN)
            self.play(*appear(so_far), run_time=min(1.0, c.until("odd")))
            c.wait_until("odd")
            q = T("length 3?", size=56, color=GOLD).move_to(1.6 * DOWN)
            self.play(*appear(q), run_time=min(1.0, c.until("sides")))
            c.wait_until("sides")

            bk = banks()
            sweep_clear(self, *[FadeIn(r) for r in bk.rects], run_time=1.6)
            c.wait_until("Put all the people")
            self.play(*appear(bk.heads[0]), run_time=0.8)
            self.play(*appear(*bk.pdots, *bk.people, shift=None, lag=0.08),  # early: the bank is shown whole, walked later
                      run_time=min(1.5, c.until("all the movies")))
            c.wait_until(own_word=bk.heads[1])
            self.play(*appear(bk.heads[1]), run_time=0.8)
            self.play(*appear(*bk.mdots, *bk.movies, shift=None, lag=0.08),
                      run_time=min(1.5, c.until("cross")))
            c.wait_until("cross")
            self.play(LaggedStart(*[Create(ln) for ln in bk.lines], lag_ratio=0.15),
                      run_time=min(2.6, c.until("so it crosses")))
            c.wait_until("so it crosses")
            self.play(*[VShowPassingFlash(bk.lines[k].copy().set_stroke(YELLOW, 6, opacity=1),
                                          time_width=0.6) for k in (0, 4, 9)],
                      run_time=1.4)
            c.wait_until("five")

            items = []
            for name in TYPES:
                lab = T(name, size=28, color=FG)
                a = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, stroke_width=3, color=FG,
                          tip_length=0.16, max_tip_length_to_length_ratio=0.3)
                pd = Dot(a.get_start(), radius=0.06, color=PINK)
                a.set_color([PINK, BLUE])
                it = VGroup(lab, VGroup(a, pd).next_to(lab, DOWN, buff=0.12))
                items.append(it)
            row = VGroup(*items).arrange(RIGHT, buff=0.55).move_to(3.0 * DOWN)
            self.play(*appear(*items, lag=0.2), run_time=min(1.8, c.until("bipartite")))
            c.wait_until("bipartite")
            bip = T("bipartite", size=52, color=YELLOW).move_to(3.05 * UP)
            c.wait_until(own_word=bip)
            self.play(*appear(bip), run_time=min(1.0, c.until()))
        self.row, self.bip = row, bip
        return bk

    # ---------------------------------------------------------------- clip 2
    def clip2(self, bk):
        with self.say("c4.even.2") as c:
            tok = Dot(bk.pdots[0].get_center(), radius=0.14, color=YELLOW).set_z_index(5)
            self.play(*disappear(self.row), FadeIn(tok, scale=2.5),
                      *recolor([bk.people[0]], YELLOW), *light(bk, 0),
                      run_time=min(1.2, c.until("s1")))
            steps = T("steps", size=30, color=DIM)
            num = T("1", size=56, color=GOLD)
            VGroup(steps, num).arrange(RIGHT, buff=0.25).move_to(2.95 * DOWN)
            self.bk = bk
            c.wait_until("s1")
            path = [(0, 0), (1, 0), (1, 1), (2, 1)]   # (person, movie) of each walk edge
            cues = ["s2", "s3", "flip", "even"]
            for step, k in enumerate(WALK):
                p, m = path[step]
                to_movie = step % 2 == 0
                dest = (bk.mdots[m] if to_movie else bk.pdots[p]).get_center()
                new = T(str(step + 1), size=56, color=GOLD).move_to(num)
                rt = 1.6 if step < 3 else 1.0
                rt = min(rt, max(0.6, 0.8 * c.until(cues[step])))
                self.play(tok.animate.move_to(dest),  # early: the counter's caption "steps" is never spoken
                          bk.lines[k].animate.set_stroke(YELLOW, 5, opacity=1),
                          *light(bk, 1 if to_movie else 0),
                          *(appear(steps, num, shift=None) if step == 0 else swap(num, new)),
                          run_time=rt)
                if step:
                    num = new
                if step < 3:
                    c.wait_until(cues[step])
            self.num = num
            self.tok = tok
            c.wait_until("even")
            ev = T("people ⇔ even", size=52, color=YELLOW).move_to(3.05 * UP)
            self.play(*swap(self.bip, ev), run_time=1.2)
            self.play(FlashAround(num, color=GOLD, run_time=1.5, time_width=1.5))

    # ---------------------------------------------------------------- clip 3
    def clip3(self):
        with self.say("c4.even.3") as c:
            code = Code(QUERY, size=30)
            if code.width > 12.4:
                code.scale_to_fit_width(12.4)
            code.move_to(1.55 * UP)
            c.wait_until("query")
            sweep_clear(self, *appear(code), run_time=min(2.0, c.until("call it ex")))
            c.wait_until("call it ex")
            self.play(FlashAround(code.find("(x)", line=1), run_time=1.5, time_width=1.5))
            c.wait_until("That's a list")
            box = token_box(code.find("labels(x)"), code.line(2), height=0.62)
            self.play(FadeIn(box), run_time=1.0)

            head = Mono("label     | paths", size=34)
            rule = Line(LEFT, RIGHT, stroke_width=2, color=DIM)
            lab = Mono("['Movie']", size=34, color=BLUE)
            bar = Mono("|", size=34)
            cnt = Mono("1353", size=34, color=GOLD)
            nrow = Mono("1 row", size=30, color=DIM)
            head.move_to(1.25 * DOWN)
            hbar = head[len("label")]          # glyph of "|" (no glyphs for spaces)
            rule.set_width(head.width + 0.6).next_to(head, DOWN, buff=0.14)
            y = rule.get_y() - 0.42
            bar.move_to([hbar.get_x(), y, 0])
            lab.move_to([head.get_left()[0] + lab.width / 2, y, 0])
            cnt.move_to([bar.get_right()[0] + 0.3 + cnt.width / 2, y, 0])
            nrow.next_to(rule, DOWN, buff=1.1).align_to(head, LEFT)
            reply = VGroup(head, rule, lab, bar, cnt, nrow)
            c.wait_until("reply")
            self.play(*appear(head, rule, lab, bar, cnt, nrow, shift=None, lag=0.12),
                      run_time=min(1.5, c.until("every single one")))
            self.play(FlashAround(cnt, color=GOLD, run_time=1.5, time_width=1.5))
            c.wait_until("every single one")
            self.play(FlashAround(lab, color=BLUE, run_time=1.5, time_width=1.5))

            strip = pill_strip()
            c.wait_until("impossible")
            sweep_clear(self, *appear(strip.actors, *strip.pills, lag=0.15),
                        run_time=min(2.0, c.until("Not by chance")))
            c.wait_until("Not by chance")
            imp = []
            for i in (1, 3):
                t = T("impossible", size=32, color=RED).next_to(strip.pills[i], DOWN, buff=0.3)
                imp.append(t)
            self.play(*appear(*imp, lag=0.2),  # early: "impossible" is never spoken; lands on "Not by chance"
                      *[strip.pills[i].box.animate.set_stroke(RED, 3) for i in (1, 3)],
                      run_time=1.0)
        self.imp = imp
        return strip

    # ---------------------------------------------------------------- clip 4
    def clip4(self, ch, strip):
        with self.say("c4.even.4") as c:
            p2 = strip.pills[0]
            self.play(FlashAround(p2, run_time=1.5, time_width=1.5))
            never = VGroup(T("never shared", size=30, color=DIM),
                           T("a film", size=30, color=DIM)).arrange(DOWN, buff=0.12)
            never.next_to(p2, DOWN, buff=0.3)
            c.wait_until("never shared one")
            self.play(*appear(never), run_time=1.0)
            c.wait_until("four")
            for i, cue in ((2, "six"), (4, "half")):
                pl = strip.pills[i]
                self.play(pl.box.animate.set_stroke(GOLD, 4), *recolor([pl.star, pl.count], GOLD),
                          run_time=min(1.0, 0.8 * c.until(cue)))
                if cue == "six":
                    c.wait_until("six")
            self.play(*flash([strip.pills[2], strip.pills[4]], color=GOLD, run_time=1.2,
                             time_width=1.5))
            c.wait_until("half")
            sweep_clear(self, FadeIn(ch), run_time=1.6)
            c.wait_until("takes two edges")
            self.play(*[e.animate.set_stroke(GOLD, 6) for e in ch.edges], run_time=1.2)
            c.wait_until("the number of movies")
            self.play(*[ch.nodes[i].animate.set_fill(BLUE, 0.6).set_stroke(BLUE, 6) for i in (1, 3)],
                      *flash([ch.nodes[1], ch.nodes[3]], color=BLUE, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            res = T("4 edges = 2 movies", size=52, t2c={"4 edges": GOLD, "2 movies": BLUE})
            res.move_to(0.4 * DOWN)
            c.wait_until("half the length")
            self.play(*appear(res), run_time=1.0)
            c.wait_until("bacon")
            bac = T("distance = length ÷ 2", size=40, color=YELLOW).move_to(2.2 * DOWN)
            self.play(*appear(bac), run_time=1.0)
