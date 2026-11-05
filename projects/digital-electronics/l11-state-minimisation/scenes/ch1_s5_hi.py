"""Chapter 1, scene 5: states H and I are indistinguishable; replace I by H, delete row I. Clips c1.hi.1 – c1.hi.4.

Owns the table-left / diagram-right layout and the merge animation reused by s6 and ch3 s6.
Module-level helpers (import with load_scene("ch1_s5_hi")):
  layout_table(rows=MACHINE) -> s3's state_table, placed on the left (TABLE_TOP, TABLE_X0)
  place_diagram(d) -> s4's tree diagram scaled by DIAG_K and shifted by DIAG_SHIFT (right side),
    stripped of its arc labels, bundle label and 1/1s (strip_labels; the table carries the outputs)
    and with the state letters scaled by LETTER_K (size 28) in circles scaled by CIRCLE_K (fit_circles:
    arcs, stubs and the bundle tip are redrawn to the bigger circles' edges);
    to_screen(p) maps s4's coordinates (POS, BUS_Y, ...) to the placed diagram
  side_by_side(rows=MACHINE) -> (tbl, d), both placed (not added)
  steps_caption() -> VGroup(.step1, .step2): the pinned two-step caption, top right
  state_counter(a, b) -> GOLD MathTex "a -> b states", below the diagram
  The merge (each plays itself and keeps tbl/d consistent; settle()s afterwards):
    replace_entry(scene, tbl, r, c, letter, run_time=1.5) -> new cell Text (GOLD): the letter
      flashes GOLD and swaps into its match
    swing_arc(scene, d, src, x, dst, run_time=1.5): arc (src, x) swings onto circle dst, label follows
    dim_state(tbl, d, letter) -> anims: row and circle (and stub) go DIM
    delete_row(scene, tbl, letter, run_time=1.6): the row leaves, rows below close up
    merge_circle(scene, d, name, into, run_time=1.5): circle slides into its match and is gone
  arc_geometry(d, src, x, dst) -> (Arrow, label centre) for a swung arc
  ROWS_AFTER_HI: the 14-row table after this scene; handover_shot(): the final frame.
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

S3 = load_scene("ch1_s3_mealy")
S4 = load_scene("ch1_s4_tree")
MACHINE = S3.MACHINE

# ---------------------------------------------------------------- shared layout
TABLE_TOP = 2.2
TABLE_X0 = -5.85
TABLE_SIZE = 30
DIAG_K = 0.55
DIAG_SHIFT = np.array([3.8, 0.75, 0.0])
RIGHT_X = 0.55                      # left edge of the right-hand column's text
CAPTION_Y = (3.45, 2.95)
LETTER_K = 1.5                      # state letters: 34 * DIAG_K * 1.5 = 28
CIRCLE_K = 1.2                      # circles grow round them (radius 0.36 * 0.55 * 1.2 = 0.24)


def to_screen(p):
    return np.array(p, dtype=float) * DIAG_K + DIAG_SHIFT


def layout_table(rows=MACHINE):
    return S3.state_table(rows, size=TABLE_SIZE, top=TABLE_TOP, x0=TABLE_X0)


def strip_labels(d):
    """Take the arc labels, the bundle label and the 1/1s out of d (the table carries every output);
    returns the removed pieces. d.labels / d.ones become empty, d.bundle_label an empty VGroup."""
    gone = [*d.labels.values(), *d.ones.values()]
    if len(d.bundle_label):
        gone.append(d.bundle_label)
    d.remove(*gone)
    d.labels, d.ones, d.bundle_label = {}, {}, VGroup()
    return gone


def fit_circles(d):
    """On a placed diagram: letters x LETTER_K, circles x CIRCLE_K, and every line redrawn to the
    bigger circles' edges (call after the scale and shift)."""
    for st in d.states.values():
        st.letter.scale(LETTER_K)
        st.circle.scale(CIRCLE_K)
    r = S4.R * DIAG_K * CIRCLE_K
    for (src, x), arc in d.arcs.items():
        arc.become(arc_geometry(d, src, x, S4.NEXT[src][x], bend=0.0)[0])
    for name, stub in d.stubs.items():
        p = d.states[name].get_center()
        stub.put_start_and_end_on(p + r * DOWN, stub.get_end())
    if len(d.bundle):
        a = d.states["A"].get_center()
        tip_start = to_screen([S4.POS["A"][0] - S4.R - 0.7, S4.POS["A"][1], 0])
        d.bundle[1].become(Arrow(tip_start, a + r * LEFT, buff=0, stroke_width=4, color=FG,
                                 tip_length=0.2 * DIAG_K, max_tip_length_to_length_ratio=0.4,
                                 max_stroke_width_to_length_ratio=20))
    return d


def place_diagram(d):
    strip_labels(d)
    d.scale(DIAG_K, about_point=ORIGIN).shift(DIAG_SHIFT)
    return fit_circles(d)


def side_by_side(rows=MACHINE):
    return layout_table(rows), place_diagram(S4.tree_diagram())


def steps_caption():
    s1 = T("1. replace the state by its match", 28, t2c={"1.": YELLOW})
    s2 = T("2. delete the row nothing reaches", 28, t2c={"2.": YELLOW})
    s1.move_to([0, CAPTION_Y[0], 0]).align_to([RIGHT_X, 0, 0], LEFT)
    s2.move_to([0, CAPTION_Y[1], 0]).align_to([RIGHT_X, 0, 0], LEFT)
    cap = VGroup(s1, s2)
    cap.step1, cap.step2 = s1, s2
    return cap


def state_counter(a, b):
    return MathTex(rf"{a} \to {b}\ \text{{states}}", font_size=52, color=GOLD).move_to([3.6, -2.45, 0])


def _k(d):
    return d.states["A"].circle.width / (2 * S4.R)


def arc_geometry(d, src, x, dst, bend=None):
    """The arc (src, x) redrawn onto circle dst, and where its label goes. When src's other arc
    already lands on dst, the arc bends (0 arc out to the left, 1 arc to the right) so both show."""
    k = _k(d)
    a, b = d.states[src].get_center(), d.states[dst].get_center()
    u = (b - a) / np.linalg.norm(b - a)
    if bend is None:
        other = d.arcs.get((src, 1 - x))
        bend = 0.0
        if other is not None and np.linalg.norm(other.get_end() - b) < 1.6 * S4.R * k:
            bend = 0.8 if x == 0 else -0.8
    s = a + S4.R * k * rotate_vector(u, -bend / 2)
    e = b - S4.R * k * rotate_vector(u, bend / 2)
    arc = Arrow(s, e, buff=0, stroke_width=3, color=FG, tip_length=0.18 * k,
                max_tip_length_to_length_ratio=0.2, path_arc=bend)
    pos = None
    if (src, x) in d.labels:
        lbl = d.labels[(src, x)]
        side = -1 if x == 0 else 1
        n = np.array([-u[1], u[0], 0])
        if np.sign(n[0]) != side:
            n = -n
        mid = (s + e) / 2 + n * (np.linalg.norm(e - s) / 2) * np.tan(abs(bend) / 4)
        off = 0.12 * k + abs(n[0]) * lbl.width / 2 + abs(n[1]) * lbl.height / 2
        pos = mid + n * off
    return arc, pos


def _set_row_of(tbl):
    tbl.row_of = lambda letter: [rw.cells[0].text for rw in tbl.rows].index(letter)


def replace_entry(scene, tbl, r, c, letter, run_time=1.5, color=GOLD):
    """The merge, step 1 in the table: the letter flashes GOLD and turns into its match."""
    old = tbl.cell(r, c)
    new = T(letter, TABLE_SIZE, color).move_to(old)
    scene.play(FlashAround(old, color=color, time_width=1.5), *swap(old, new), run_time=run_time)
    row = tbl.rows[r]
    row.remove(old)
    row.cells[c] = new
    row.add(new)
    settle(scene, tbl)
    return new


def swing_arc(scene, d, src, x, dst, run_time=1.5):
    """The merge, step 1 on the diagram: arc (src, x) swings over onto dst; its label follows."""
    arc, pos = arc_geometry(d, src, x, dst)
    anims = [Transform(d.arcs[(src, x)], arc)]
    if pos is not None:
        anims.append(d.labels[(src, x)].animate.move_to(pos))
    scene.play(*anims, run_time=run_time)
    settle(scene, d)


def dim_state(tbl, d, letter, op=DIMMED):
    mobs = [tbl.rows[tbl.row_of(letter)], d.states[letter]]
    if letter in d.stubs:
        mobs.append(d.stubs[letter])
    return set_alpha(mobs, op)


def delete_row(scene, tbl, letter, run_time=1.6):
    """The merge, step 2 in the table: the row leaves, the rows below close up."""
    r = tbl.row_of(letter)
    row = tbl.rows[r]
    y = row.cells[0].get_y()
    p = tbl.pitch
    moves = [m.animate.shift(p * UP) for m in tbl.rows[r + 1:]]
    moves += [m.animate.shift(p * UP) for m in tbl.rules[1:] if m.get_y() < y - 0.01]
    for sep in tbl.seps:
        moves.append(Transform(sep, Line(sep.get_start(), sep.get_end() + p * UP).set_stroke(DIM, 2)))
    scene.play(*during(disappear(row), 0, 0.4), *during(moves, 0.45, 1.0), run_time=run_time)
    tbl.rows.remove(row)
    tbl.remove(row)
    _set_row_of(tbl)
    settle(scene, tbl)


def merge_circle(scene, d, name, into, run_time=1.5):
    """The merge, step 2 on the diagram: the circle slides into its match and is gone."""
    st = d.states[name]
    target = d.states[into].get_center()
    gone = [m for m in [d.stubs.get(name)] if m is not None]
    gone += [d.arcs[k] for k in list(d.arcs) if k[0] == name]
    gone += [d.labels[k] for k in list(d.labels) if k[0] == name]
    scene.play(*during(disappear(st.letter, *gone), 0, 0.3),
               *during([st.circle.animate.set_stroke(DIM, opacity=1).move_to(target)], 0.15, 1.0),
               run_time=0.7 * run_time)
    scene.play(FadeOut(st.circle), run_time=0.3 * run_time)
    d.remove(st, *gone)
    d.states.pop(name)
    d.stubs.pop(name, None)
    for k in [k for k in list(d.arcs) if k[0] == name]:
        d.arcs.pop(k)
    for k in [k for k in list(d.labels) if k[0] == name]:
        d.labels.pop(k)
    settle(scene, d)


ROWS_AFTER_HI = [(("D", "H", "H", "0", "0") if r[0] == "D" else r) for r in MACHINE if r[0] != "I"]


def _diagram_after_hi():
    d = place_diagram(S4.tree_diagram())
    d.remove(d.states.pop("I"), d.stubs.pop("I"))
    arc, pos = arc_geometry(d, "D", 1, "H")
    d.arcs[("D", 1)].become(arc)
    if ("D", 1) in d.labels:
        d.labels[("D", 1)].move_to(pos)
    return d


def handover_shot():
    tbl = layout_table(ROWS_AFTER_HI)
    d = _diagram_after_hi()
    g = VGroup(tbl, d, steps_caption(), state_counter(15, 14))
    return g


# ---------------------------------------------------------------- local pieces
def eye_icon(w=0.72):
    top = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=-PI / 2)
    bot = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=PI / 2)
    pupil = Circle(radius=0.1).set_stroke(width=0).set_fill(FG, 1)
    return VGroup(top, bot).set_stroke(FG, 3).add(pupil)


def quote(lines, size=28):
    g = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    g.align_to([RIGHT_X, 0, 0], LEFT).align_to([0, -3.55, 0], DOWN)
    return g


BULLET_1 = ["From the table, we see that there", "is no way of telling states H and I",
            "apart, so we can replace I with H", "when it appears in the Next State",
            "portion of the table"]
BULLET_2 = ["We also see that there is now no", "way to get to state I so we can",
            "remove row I from the table"]


# ---------------------------------------------------------------- the scene
class StatesHI(NarratedScene):
    def construct(self):
        self.d = S4.handover_shot()
        self.add(self.d)
        self.tbl = layout_table()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)          # handover: s6 opens on this shot

    # ------------------------------------------------------------ c1: the two rows are identical
    def clip1(self):
        tbl, d = self.tbl, self.d
        rh, ri = tbl.row_of("H"), tbl.row_of("I")
        with self.say("c1.hi.1") as c:
            labs = strip_labels(d)
            self.add(*labs)
            d.generate_target()
            d.target.scale(DIAG_K, about_point=ORIGIN).shift(DIAG_SHIFT)
            fit_circles(d.target)
            self.play(*during(disappear(*labs), 0, 0.3), *during([MoveToTarget(d)], 0.25, 0.75),  # early: s3's table returns whole
                      *during(appear(tbl, shift=None), 0.5, 1.0), run_time=min(2.4, c.until("look at")))
            self.remove(*labs)
            c.wait_until("look at")
            self.boxes = [tbl.row_box(rh), tbl.row_box(ri)]
            self.play(*[FadeIn(b) for b in self.boxes], run_time=1.0)
            c.wait_until("next")
            nxt = [tbl.cell(r, k) for r in (rh, ri) for k in (1, 2)]
            self.play(*recolor(nxt, YELLOW), run_time=1.0)
            c.wait_until("outs")
            outs = [tbl.cell(r, k) for r in (rh, ri) for k in (3, 4)]
            self.play(*recolor(nxt, FG), *recolor(outs, YELLOW), run_time=1.0)
            c.wait_until("same")
            gold = [tbl.row_box(rh, GOLD), tbl.row_box(ri, GOLD)]
            self.play(*recolor(outs, FG), *[Transform(b, g) for b, g in zip(self.boxes, gold)],
                      restyle(d.states["H"], outline=GOLD), restyle(d.states["I"], outline=GOLD),
                      *flash([d.states["H"], d.states["I"]], color=GOLD, time_width=1.5), run_time=1.5)
            settle(self, d)
            settle(self, tbl)

    # ------------------------------------------------------------ c2: no way of telling them apart
    def clip2(self):
        d = self.d
        with self.say("c1.hi.2") as c:
            self.bullet = quote(BULLET_1)
            self.play(*appear(*self.bullet, lag=0.15), run_time=1.6)  # early: the slide's bullet, read whole
            c.wait_until("start")
            k = DIAG_K
            ph, pi_ = d.states["H"].get_center(), d.states["I"].get_center()
            r = d.states["H"].circle.width / 2
            dots = [Dot(p + r * DOWN, radius=0.1, color=YELLOW).set_z_index(2) for p in (ph, pi_)]
            eye = eye_icon().move_to([RIGHT_X + 0.4, 3.2, 0])
            olab = T("outputs only", 28, DIM).next_to(eye, RIGHT, buff=0.25)
            self.play(*[FadeIn(x, scale=0.5) for x in dots], run_time=0.8)
            self.play(*appear(eye, olab, shift=None, lag=0.3), run_time=1.0)  # early: the eye is "all you can watch"
            c.wait_until("nothing")
            inl = T("input", 28, DIM).move_to([5.3, 3.2, 0])
            ind = T("1", 36, BLUE).next_to(inl, RIGHT, buff=0.2)
            self.play(*appear(inl, ind, shift=0.15 * DOWN, lag=0.2), run_time=0.9)
            by, bx, a = to_screen([0, S4.BUS_Y, 0])[1], to_screen([S4.BUS_X, 0, 0])[0], d.states["A"].get_center()
            paths = [VMobject().set_points_as_corners([p + r * DOWN, [p[0], by, 0], [bx, by, 0], [bx, a[1], 0],
                                                      a + r * LEFT])
                     for p in (ph, pi_)]
            zeros = [T("0", 30, GREEN).move_to(p + np.array([0.22, -0.62, 0])) for p in (ph, pi_)]
            self.play(*during(appear(*zeros, shift=None), 0, 0.3),
                      *during([MoveAlongPath(x, pth, rate_func=smooth) for x, pth in zip(dots, paths)], 0.15, 1.0),
                      run_time=min(3.0, c.until("forever") - 0.2))
            c.wait_until("forever")
            self.play(FadeOut(dots[1]), dots[0].animate.scale(1.3), FlashAround(d.states["A"], color=YELLOW),
                      run_time=1.0)
            ac = d.arcs[("A", 1)]
            self.play(MoveAlongPath(dots[0], VMobject().set_points_as_corners(
                [a + r * LEFT, ac.get_start(), ac.get_end()])), run_time=1.3)
            self.wait(0.4)
            self.play(FadeOut(dots[0], scale=0.4), *disappear(*zeros, eye, olab, inl, ind),
                      run_time=min(1.0, c.until(floor=0.5)))

    # ------------------------------------------------------------ c3: replace I by H
    def clip3(self):
        tbl, d = self.tbl, self.d
        with self.say("c1.hi.3") as c:
            phrase = list(select(self.bullet[2], "replace I with H")[0])
            self.play(*recolor(phrase, YELLOW), run_time=1.0)
            c.wait_until("find")
            p = tbl.pitch
            xa = tbl.cell(0, 1).get_x() - 0.45
            xb = tbl.cell(0, 2).get_x() + 0.45
            band = (Rectangle(width=xb - xa, height=p * 0.98).move_to([(xa + xb) / 2, tbl.cell(0, 1).get_y(), 0])
                    .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1))
            self.play(*[FadeOut(b) for b in self.boxes], FadeIn(band), run_time=0.6)
            self.play(band.animate.shift((len(tbl.rows) - 1) * p * DOWN), rate_func=linear,
                      run_time=min(2.0, c.until("only")))
            c.wait_until("only")
            rd = tbl.row_of("D")
            cell = tbl.cell(rd, 2)
            cbox = (Rectangle(width=0.62, height=p * 0.98).move_to(cell)
                    .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.18).set_z_index(-1))
            self.play(*during([FadeOut(band)], 0, 0.4), *during([FadeIn(cbox)], 0.4, 0.8),
                      *during(recolor([cell], YELLOW), 0.4, 0.8), FlashAround(cell, time_width=1.5), run_time=1.5)
            band = cbox
            c.wait_until("becomes")
            self.newH = replace_entry(self, tbl, rd, 2, "H")
            c.wait_until("arc")
            self.play(FadeOut(band), run_time=0.6)
            swing_arc(self, d, "D", 1, "H", run_time=1.6)
            self.play(VShowPassingFlash(d.arcs[("D", 1)].copy().set_stroke(GOLD, 6), time_width=0.6),
                      run_time=min(1.0, c.until(floor=0.3)))

    # ------------------------------------------------------------ c4: I is unreachable; delete it
    def clip4(self):
        tbl, d = self.tbl, self.d
        with self.say("c1.hi.4") as c:
            b2 = quote(BULLET_2)
            self.play(*swap(self.bullet, b2), *recolor([self.newH], FG), run_time=1.4)  # early: the slide's bullet
            c.wait_until("nolead")
            ci = d.states["I"]
            tag = T("no arrows in", 28, RED).move_to([ci.get_x(), -1.5, 0])
            self.play(*dim_state(tbl, d, "I"), FlashAround(ci, color=RED), run_time=1.2)
            self.play(*appear(tag), run_time=0.9)  # early: names what "nothing leads to it" means
            c.wait_until("delete")
            delete_row(self, tbl, "I", run_time=1.6)
            c.wait_until("merge")
            ci = d.states["I"]
            self.play(*disappear(tag), ci.circle.animate.set_stroke(GOLD, opacity=1), run_time=0.7)
            self.play(*during(disappear(ci.letter, d.stubs["I"]), 0, 0.25),
                      *during([ci.circle.animate.move_to(d.states["H"].get_center())], 0.15, 1.0), run_time=1.6)
            self.play(FadeOut(ci.circle), FlashAround(d.states["H"], color=GOLD), run_time=0.6)
            self.remove(ci.circle)
            d.remove(ci, d.stubs.pop("I"))
            d.states.pop("I")
            settle(self, d)
            c.wait_until("count")
            cnt = state_counter(15, 14)
            self.play(*swap(b2, cnt), restyle(d.states["H"], outline=FG), run_time=1.4)
            settle(self, d)
            c.wait_until("step1")
            cap = steps_caption()
            self.play(*appear(cap.step1), run_time=1.0)
            c.wait_until("step2")
            self.play(*appear(cap.step2), run_time=1.0)
