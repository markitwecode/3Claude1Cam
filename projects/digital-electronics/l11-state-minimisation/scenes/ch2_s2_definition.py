"""Chapter 2, scene 2: same outputs, for ever: p. 148's definition of state equivalence. Clips c2.def.1 - c2.def.3.

Opens on ch2_s5_layout's `p150_table()` at its home (s1's last frame); {slide} shrinks it DIM to the
left edge, where it stays.

Shared drawings (import with load_scene("ch2_s2_definition")), returned at their home positions:
- `dim_table()`: p. 150's table, shrunk (x0.55) and DIM at the left edge.
- `definition_card(colored=True, shrunk=False)`: p. 148's definition, verbatim, in a DIM rounded
  frame. p, q YELLOW; "same output sequence" GREEN; "any input bit sequence" BLUE (colored=True).
  `.lines` (5 Texts), `.frame`, `.names` (glyph groups of p, q, p, q), `.same`, `.anyinput`
  (glyph groups), `.any` (glyphs of "any"), `.sym` (glyphs of "p ≡ q"). Home: right of the table,
  centred at (CARD_X, CARD_Y); shrunk=True: x0.7, at the top (this scene's last position).
- `machine_boxes()`: two machine copies stacked right of the table: `.boxes` [top, bottom]
  (BLUE RoundedRectangles), `.labels` ["start in p", "start in q"], `.inp` (BLUE Mono
  "0 1 1 0 1 0 …"), `.trunk` + `.forks` (BLUE arrows into both boxes), `.paths` (the two input
  routes, for VShowPassingFlash), `.out_arrows` [2], `.outs` [[5 GREEN bits], [5 GREEN bits]],
  `.eq` (GOLD "="). The VGroup holds everything.
- `handover_shot()`: dim_table() + definition_card(shrunk=True) (s3 opens on it).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S5 = load_scene("ch2_s5_layout")
HI = load_scene("ch1_s5_hi")
MEALY = load_scene("ch1_s3_mealy")


def _p(x, y):
    return np.array([x, y, 0.0])


CARD_X, CARD_Y = 1.65, 1.1          # centre of the free area right of the dim table
TABLE_K = 0.55
CARD_K = 0.7
LEFT_X = -2.7                       # left edge of text in the free area


# ------------------------------------------------------------------ shared drawings
def dim_table():
    t = S5.p150_table()
    t.scale(TABLE_K).to_edge(LEFT, buff=0.5).set_color(DIM)
    return t


DEF_LINES = [
    "Two states, say p and q, can be considered",
    "equivalent, i.e., p ≡ q, if from each of these",
    "states, a finite state machine generates the",
    "same output sequence in response to any",
    "input bit sequence.",
]


def _glyphs(line, s, sub, nth=0):
    """Glyphs of the nth occurrence of sub in line (built from string s with ligatures off,
    which keeps one (empty) submobject per space, so string index = submobject index)."""
    i = -1
    for _ in range(nth + 1):
        i = s.index(sub, i + 1)
    return VGroup(*[g for g in line.submobjects[i:i + len(sub)] if g.has_points()])


def definition_card(colored=True, shrunk=False, size=32):
    lines = VGroup(*[T(s, size, disable_ligatures=True) for s in DEF_LINES])
    lines.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    frame = RoundedRectangle(corner_radius=0.2, width=lines.width + 0.7, height=lines.height + 0.6)
    frame.set_stroke(DIM, 2).move_to(lines)
    card = VGroup(frame, lines).move_to(_p(CARD_X, CARD_Y))
    l0, l1, l3, l4 = lines[0], lines[1], lines[3], lines[4]
    sym = _glyphs(l1, DEF_LINES[1], "p ≡ q")
    card.names = [_glyphs(l0, DEF_LINES[0], "p"), _glyphs(l0, DEF_LINES[0], "q"),
                  VGroup(sym[0]), VGroup(sym[2])]
    card.same = _glyphs(l3, DEF_LINES[3], "same output sequence")
    card.any = _glyphs(l3, DEF_LINES[3], "any")
    card.anyinput = VGroup(*card.any, *_glyphs(l4, DEF_LINES[4], "input bit sequence"))
    card.sym = sym
    card.lines, card.frame = lines, frame
    if colored:
        for g in card.names:
            g.set_color(YELLOW)
        card.same.set_color(GREEN)
        card.anyinput.set_color(BLUE)
    if shrunk:
        card.scale(CARD_K).to_edge(UP, buff=0.3).set_x(CARD_X)
    return card


BOX_X, BOX_W, BOX_H = 2.0, 2.6, 1.1
BOX_Y = (0.75, -1.55)
MID_Y = (BOX_Y[0] + BOX_Y[1]) / 2
OUT_BITS = "00101"
OUT_X0, OUT_PITCH = 4.15, 0.46


def machine_boxes():
    boxes = [RoundedRectangle(corner_radius=0.2, width=BOX_W, height=BOX_H).set_stroke(BLUE, 3)
             .move_to(_p(BOX_X, y)) for y in BOX_Y]
    labels = [T(f"start in {n}", 34, t2c={n: YELLOW}).move_to(b) for n, b in zip("pq", boxes)]
    inp = Mono("0 1 1 0 1 0 …", 28, BLUE)
    inp.move_to(_p(0, MID_Y)).align_to(_p(-0.25, 0), RIGHT)
    fork = _p(0.3, MID_Y)
    trunk = Line(_p(-0.1, MID_Y), fork).set_stroke(BLUE, 3)
    forks = [Arrow(fork, b.get_left(), buff=0.05, stroke_width=3, color=BLUE,
                   max_tip_length_to_length_ratio=0.2) for b in boxes]
    paths = [VMobject().set_points_as_corners([_p(-0.1, MID_Y), fork, b.get_left()]) for b in boxes]
    out_arrows = [Arrow(b.get_right(), b.get_right() + 0.6 * RIGHT, buff=0, stroke_width=3, color=GREEN,
                        max_tip_length_to_length_ratio=0.35) for b in boxes]
    outs = [[Mono(v, 30, GREEN).move_to(_p(OUT_X0 + i * OUT_PITCH, b.get_y())) for i, v in enumerate(OUT_BITS)]
            for b in boxes]
    eq = MathTex("=", font_size=72, color=GOLD).move_to(_p(OUT_X0 + 2 * OUT_PITCH, MID_Y))
    g = VGroup(*boxes, *labels, inp, trunk, *forks, *out_arrows, *outs[0], *outs[1], eq)
    g.boxes, g.labels, g.inp, g.trunk, g.forks, g.paths = boxes, labels, inp, trunk, forks, paths
    g.out_arrows, g.outs, g.eq = out_arrows, outs, eq
    return g


def handover_shot():
    return VGroup(dim_table(), definition_card(colored=True, shrunk=True))


# ------------------------------------------------------------------ local pieces
def quote_card(lines, size=28):
    body = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    who = T("— the lecturer", size, DIM).next_to(body, DOWN, buff=0.18, aligned_edge=RIGHT)
    g = VGroup(body, who)
    g.move_to(_p(CARD_X, 0)).align_to(_p(0, -3.5), DOWN)
    return g


def bullet(lines, size=30):
    body = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    dot = T("•", size).next_to(body[0], LEFT, buff=0.25)
    g = VGroup(dot, body)
    g.align_to(_p(LEFT_X, 0), LEFT)
    return g


ROOT_Y, TREE_DY, TREE_W, COUNT_X = 1.25, 0.95, 7.2, 5.75
TREE_X = 1.3


def even_clear(scene, incoming, keep=(), run_time=1.2):
    """Fade every top-level object not kept in one even fade (no lag), then bring incoming in."""
    gone = [m for m in scene.mobjects if m not in keep]
    scene.play(*during([FadeOut(m) for m in gone], 0, 0.45), *during(list(incoming), 0.5, 1.0),
               run_time=run_time)


def tree_level(k):
    """Edges, dots and the GOLD count for depth k (k = 5 runs off the bottom of the screen)."""
    def xy(level, i):
        n = 2 ** level
        x = TREE_X + (i + 0.5 - n / 2) * (TREE_W / n) if level else TREE_X
        y = ROOT_Y - level * TREE_DY if level <= 4 else -3.95
        return _p(x, y)
    w = 2.5 if k <= 3 else (2 if k == 4 else 1.5)
    edges = [Line(xy(k - 1, i // 2), xy(k, i)).set_stroke(BLUE, w) for i in range(2 ** k)]
    dots = [Dot(xy(k, i), radius=0.06 if k < 4 else 0.05, color=FG) for i in range(2 ** k)] if k <= 4 else []
    count = T(str(2 ** k), 36, GOLD).move_to(_p(COUNT_X, ROOT_Y - k * TREE_DY)) if k <= 4 else None
    return edges, dots, count


# ------------------------------------------------------------------ the scene
class Definition(NarratedScene):
    def construct(self):
        self.tbl = S5.p150_table()
        self.add(self.tbl)
        self.clip1()
        self.clip2()
        self.clip3()

    # ---------------------------------------------------------------- c1: the slide and the definition
    def clip1(self):
        tbl = self.tbl
        with self.say("c2.def.1") as c:
            self.play(tbl.animate.scale(TABLE_K).to_edge(LEFT, buff=0.5).set_color(DIM), run_time=1.2)
            title = VGroup(T("Elimination of Redundant States –", 40), T("State Equivalence", 40))
            title.arrange(DOWN, buff=0.14, aligned_edge=LEFT).align_to(_p(LEFT_X, 0), LEFT).to_edge(UP, buff=0.45)
            self.play(*appear(title, lag=0.2), run_time=1.0)  # early: the slide's title, shown whole
            b1 = bullet(["The previous row matching approach only", "works in certain cases."])
            b1.align_to(_p(0, 1.85), UP)
            b2 = bullet(["We will now consider a more general approach",
                         "that identifies state equivalence to help",
                         "eliminate states"])
            b2.next_to(b1, DOWN, buff=0.45).align_to(_p(LEFT_X, 0), LEFT)
            c.wait_until("row matching")
            self.play(*appear(b1), run_time=1.0)  # early: the slide's bullet, read whole
            c.wait_until("general approach")
            self.play(*appear(b2), run_time=1.0)  # early: the slide's bullet, read whole
            c.wait_until("powerful")
            q = quote_card(["“a more powerful way of trying to", "identify equivalent states”"])
            q.align_to(_p(0, -3.45), DOWN)
            self.play(*appear(q), run_time=1.0)  # early: a quote card, read whole
            c.wait_until("quote")
            card = definition_card(colored=False)
            self.card = card
            self.quote1 = q
            sweep_clear(self, time_span(FadeIn(card, shift=0.2 * DOWN), 0.6, 1.4), keep=[tbl, q], run_time=1.4)  # early: the definition, read whole
            c.wait_until("pee and cue")
            self.play(*[a for g in card.names for a in recolor(g, YELLOW)],
                      run_time=1.2)
            c.wait_until("same output")
            self.play(*recolor(card.same, GREEN), FlashUnder(card.same, color=GREEN, time_width=1.5),
                      run_time=1.2)
            c.wait_until("any input")
            self.play(*recolor(card.anyinput, BLUE), run_time=1.0)
            c.wait_until("symbol")
            big = MathTex("p", r"\equiv", "q", font_size=120)
            big[0].set_color(YELLOW)
            big[2].set_color(YELLOW)
            big[1].set_color(GOLD)
            big.move_to(_p(CARD_X, -2.25))
            self.big = big
            self.play(FlashAround(card.sym, color=GOLD, time_width=1.5), *during(disappear(q), 0, 0.4),
                      *during(appear(big), 0.45, 1.0), run_time=min(1.8, c.until()))

    # ---------------------------------------------------------------- c2: two copies, same inputs
    def clip2(self):
        card, big = self.card, self.big
        m = machine_boxes()
        with self.say("c2.def.2") as c:
            card.generate_target()
            card.target.scale(CARD_K).to_edge(UP, buff=0.3).set_x(CARD_X)
            self.play(*during(disappear(big), 0, 0.5), MoveToTarget(card), run_time=1.4)
            self.play(*[FadeIn(b) for b in m.boxes], run_time=0.8)
            c.wait_until("state pee")
            self.play(*appear(m.labels[0]), run_time=0.8)
            c.wait_until("state cue")
            self.play(*appear(m.labels[1]), run_time=0.8)
            c.wait_until("feed")
            self.play(*appear(m.inp, shift=None), Create(m.trunk), *[GrowArrow(f) for f in m.forks],
                      run_time=min(1.1, c.until("watch")))
            c.wait_until("watch")
            flashes = [VShowPassingFlash(p.copy().set_stroke(YELLOW, 6), time_width=0.5) for p in m.paths]
            self.play(*flashes, *[GrowArrow(a) for a in m.out_arrows], run_time=0.8)
            outs = [a for i in range(5)
                    for a in during(appear(m.outs[0][i], m.outs[1][i], shift=0.15 * RIGHT, lag=0),
                                    i * 0.17, i * 0.17 + 0.32)]
            self.play(*outs, run_time=min(2.2, c.until("agree")))
            c.wait_until("agree")
            self.play(*appear(m.eq, shift=None),
                      *flash([VGroup(*m.outs[0]), VGroup(*m.outs[1])], color=GOLD, time_width=1.5),
                      run_time=1.5)
            c.wait_until("merge")
            top, bot = m.boxes
            dy = BOX_Y[0] - MID_Y
            gone = [*m.labels, *m.forks, m.trunk, m.out_arrows[1], *m.outs[1], m.eq]
            keep_out = m.outs[0]
            moves = [top.animate.shift(dy * DOWN), bot.animate.shift(dy * UP),
                     m.out_arrows[0].animate.shift(dy * DOWN), *[b.animate.shift(dy * DOWN) for b in keep_out]]
            self.play(*during(disappear(*gone), 0, 0.4), *during(moves, 0.35, 1.0), run_time=1.6)
            self.remove(bot)
            lab = MathTex("p", r"\equiv", "q", font_size=60)
            lab[0].set_color(YELLOW)
            lab[2].set_color(YELLOW)
            lab[1].set_color(GOLD)
            lab.move_to(top)
            arrow_in = Arrow(_p(-0.1, MID_Y), top.get_left(), buff=0.05, stroke_width=3, color=BLUE,
                             max_tip_length_to_length_ratio=0.2)
            self.play(restyle(top, outline=GOLD), *appear(lab, shift=None), GrowArrow(arrow_in), run_time=1.2)
            c.wait_until("move")
            small = MEALY.state_table(rows=[("p", "q", "p", "0", "1"), ("q", "q", "p", "0", "1")],
                                      size=30, pitch=0.5, top=-2.5, x0=CARD_X - 2.475, rules_after=())
            self.play(*appear(small, shift=None), run_time=1.0)
            c.wait_until("replace")
            HI.replace_entry(self, small, 0, 1, "p", run_time=1.4)
            self.play(*set_alpha([small.rows[1]], DIMMED), run_time=0.6)
            c.wait_until("delete")
            HI.delete_row(self, small, "q", run_time=max(0.8, min(1.4, c.until() - 0.1)))

    # ---------------------------------------------------------------- c3: any input, of every length
    def clip3(self):
        card, tbl = self.card, self.tbl
        with self.say("c2.def.3") as c:
            box = SurroundingRectangle(card.any, color=YELLOW, buff=0.06).set_stroke(YELLOW, 3)
            even_clear(self, [FadeIn(box)], keep=[tbl, card], run_time=1.2)
            c.wait_until("grow")
            root = Dot(_p(TREE_X, ROOT_Y), radius=0.08, color=FG)
            tree = [root]
            counts = []
            cues = [None, "four", "eight", "doubling"]
            for k in range(1, 5):
                if cues[k - 1]:
                    c.wait_until(cues[k - 1])
                edges, dots, count = tree_level(k)
                anims = [Create(e) for e in edges] + [FadeIn(d) for d in dots]
                anims += appear(count, shift=None)
                if k == 1:
                    lab0 = T("0", 30, BLUE).next_to(edges[0].get_center(), LEFT, buff=0.2)
                    lab1 = T("1", 30, BLUE).next_to(edges[1].get_center(), RIGHT, buff=0.2)
                    anims = [FadeIn(root)] + anims + [FadeIn(lab0), FadeIn(lab1)]
                    tree += [lab0, lab1]
                self.play(*anims, run_time=1.2 if k < 4 else 1.0)
                tree += edges + dots
                counts.append(count)
            edges5, _, _ = tree_level(5)
            dots_more = T("…", 36, GOLD).move_to(_p(COUNT_X, ROOT_Y - 5 * TREE_DY + 0.2))
            self.play(*[Create(e) for e in edges5], *appear(dots_more, shift=None), run_time=1.2)
            tree += edges5
            c.wait_until("infinite")
            inf = MathTex(r"\infty", font_size=60, color=GOLD).next_to(dots_more, RIGHT, buff=0.2)
            self.play(*appear(inf, shift=None), FlashAround(inf, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("hide")
            rows = []
            labels = [T(f"from {n}", 36, t2c={n: YELLOW}) for n in "pq"]
            bits = ["1001", "1000"]
            ys = (0.45, -0.85)
            for lab, y in zip(labels, ys):
                lab.move_to(_p(0, y)).align_to(_p(0.2, 0), RIGHT)
            cells = [[Mono(v, 56, GREEN).move_to(_p(1.2 + i * 0.95, y)) for i, v in enumerate(b)]
                     for b, y in zip(bits, ys)]
            even_clear(self, appear(*labels, shift=None, lag=0.3), keep=[tbl, card, box], run_time=1.4)
            c.wait_until("agree")
            cols = [VGroup(cells[0][i], cells[1][i]) for i in range(3)]
            self.play(*appear(*cols, shift=0.15 * RIGHT, lag=0.4), run_time=1.6)
            c.wait_until("differ")
            last = [cells[0][3], cells[1][3]]
            self.play(*appear(VGroup(*last), shift=0.15 * RIGHT), run_time=0.8)
            self.play(*recolor(last, RED), *flash(last, color=RED, time_width=1.5), run_time=1.2)
            c.wait_until("lecturer")
            q = quote_card(["“we don’t really want to be applying", "an infinitely long sequence to check”"])
            self.play(*appear(q), run_time=1.0)  # early: a quote card, read whole
            self.rest = [*labels, *cols, VGroup(*last), q, box]
        self.wait(1.0)   # the lecturer's quote reads to its end
        self.play(*disappear(*self.rest), run_time=0.9)
        self.wait(1.0)
