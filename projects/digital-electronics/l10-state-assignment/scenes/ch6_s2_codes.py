"""Chapter 6, scene 2: three flip-flops, one per state; s = s2; the one-hot table (p. 141-142). Clips c6.codes.1 – c6.codes.5.

Opens on opening_shot() (s1 ends on it); ends on handover_shot() (s3 opens on it).
Shared helpers (load_scene("ch6_s2_codes")), all standalone:
- `onehot_diagram(where="native")`: ch5_s3's sync_diagram with one-hot codes ONEHOT (Sync [100],
  Hunt [001], Sight [010], GREEN Mono, the 1 GOLD). .one[name] is that GOLD glyph; all of
  sync_diagram's attributes (.circle .name .arcs .labels .code .by_state). where="native": full size
  (ch5_s3's geometry, x -4.85..4.85); "top": scale 0.55, shifted TOP_SHIFT (-3.8, 1.72): y 0.0..3.5,
  x -6.6..-1.1; "left": ch5's placement, shift LEFT_SHIFT (-3.9, 0.05): y -1.7..1.8. Placed codes are
  enlarged x1.55 (Mono 32 -> ~27 on screen), Sight's nudged left.
- `place_diagram(d, where)`: applies the "top"/"left" placement to a native diagram.
- `light_arc(d, i, on=True)` -> Transform: arc i (ch5 order: 0 Sync loop ē, 1 Sync loop e·r,
  2 Sync->Hunt, 3 Hunt loop r̄, 4 Hunt->Sight, 5 Sight loop ē, 6 Sight->Sync, 7 Sight->Hunt)
  YELLOW stroke 5 (on) / FG stroke 3 (off). `glow_state(d, name, on=True)` -> Transform: circle
  YELLOW stroke 6 / FG stroke 4. ROW_ARC[i]: the arc table row i reads.
- `ff_label()`: "FF labels" T DIM + "[s2 s1 s0]" Mono GREEN (size 30); .letters[k] = glyphs of s2, s1, s0.
- `onehot_ff(k, center, scale=0.75, out_size=44, tag_size=32)`: one D flip-flop (L6 make_ff via
  ch2_s6, no clock wire, clock triangle x1.5), k = 0, 1, 2 for s2 (Sync), s1 (Sight), s0 (Hunt);
  VGroup(ff, out, tag) with .ff (.box .d_w .q_w .d_l .q_l ...) .out (MathTex s_k GREEN right of Q)
  .tag (T YELLOW state name under the box).
- `onehot_ffs(xs=FF_XS, y=FF_Y, scale=FF_SCALE, tags=True)`: the row s2 s1 s0 at x (-4.2, 0, 4.2),
  box centres y -1.55, scale 0.75 (box 1.13 x 1.95; row x -5.4..5.9, tags at y -2.9).
  .ffs .outs .tags (lists, s2 first); .units[k] = onehot_ff group; tags in the group only if tags=True.
- `ff_bit(ff, v, size=40)`: Mono v at bit_spot(ff) (in the box, between D/Q and the clock), GOLD for "1", DIM for "0" (the hopping 1).
- `state_var(tex="s_2", tag="Sync", size=56)`: GREEN MathTex with its YELLOW T 28 name tag under it;
  .var .tag.
- `onehot_table(filled=True)`: ch5_s5's state_table with ONEHOT_ROWS / ONEHOT_HEADS, group rules
  between Hunt | Sight | Sync rows, current-state 1s GOLD, scaled 0.95 about its top centre, centred
  x 3.1: x -0.4..6.6, y 3.6..-1.4. Same attributes (.rows .cell(i,g,j) .titles .heads .lines ...);
  .row_y/.col_x are pre-scale, use the cells' positions instead.
- `pattern_chips(state="final")`: the eight 3-bit chips 000..111 in a row at y -3.0, pitch 1.3
  (x -5.05..5.05), each VGroup(rect 1.0 x 0.56, Mono 30). .chip[pattern] (.rect .txt), USED =
  001 010 100. state "plain" (FG), "lit" (used GREEN outline/0s, GOLD 1), "final" (lit + the other
  five DIM). `chip_anims(chip, pattern, state)` -> anims to restyle one chip.
- `opening_shot()`: VGroup(onehot_diagram(), ff_label() bottom-left at LABEL_CORNER).
- `handover_shot()`: VGroup(onehot_diagram("left"), onehot_table(), pattern_chips("final")).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

D3 = load_scene("ch5_s3_diagram")
S5 = load_scene("ch5_s5_table")
NL = load_scene("ch2_s6_nologic")


def _p(x, y):
    return np.array([x, y, 0.0])


def _dir(deg):
    a = np.deg2rad(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


# ---------------------------------------------------------------- shared: the one-hot diagram
STATES = D3.STATES
ONEHOT = {"Sync": "100", "Hunt": "001", "Sight": "010"}
DIAG_SCALE = 0.55
TOP_SHIFT = _p(-3.8, 1.72)
LEFT_SHIFT = _p(-3.9, 0.05)
CODE_GROW = 1.55
LABEL_GROW = 1.3
R_PLACED = 0.9                  # placed diagrams get roomier circles (native r 0.62) ...
NAME_GROW = 1.5                 # ... and names grown back to T ~26 (32 x 0.55 x 1.5)
ROW_ARC = list(S5.ROW_ARC)      # [3, 4, 5, 7, 6, 0, 2, 1]


def place_diagram(d, where="left"):
    d.scale(DIAG_SCALE, about_point=ORIGIN).shift(TOP_SHIFT if where == "top" else LEFT_SHIFT)
    for n in STATES:
        d.code[n].scale(CODE_GROW)
    d.code["Sight"].shift(0.32 * LEFT)
    for lab in d.labels:
        lab.scale(LABEL_GROW)
    return d


def onehot_diagram(where="native"):
    d = D3.sync_diagram(codes=ONEHOT)
    d.one = {}
    for n, s in ONEHOT.items():
        g = d.code[n][1 + s.index("1")]
        g.set_color(GOLD)
        d.one[n] = g
    if where != "native":
        _roomy(d, where)
    return d


def _roomy(d, where):
    """d (native, r 0.62) becomes the placed one-hot diagram: circles r R_PLACED, names ~26 pt."""
    big = D3.sync_diagram(codes=ONEHOT, r=R_PLACED)
    for a, b in zip(d.circles + d.arcs, big.circles + big.arcs):
        a.become(b)
    place_diagram(d, where)
    d.code["Sync"].shift(0.3 * RIGHT + 0.16 * UP)       # clear of the bigger loops
    d.code["Hunt"].shift(0.3 * LEFT + 0.16 * UP)
    owner = {0: "Sync", 1: "Sync", 3: "Hunt", 5: "Sight"}
    for i, n in owner.items():         # loop labels a little further out
        v = d.labels[i].get_center() - d.circle[n].get_center()
        d.labels[i].shift(0.2 * v / np.linalg.norm(v))
    for n in STATES:
        d.name[n].scale(NAME_GROW)
    return d


def light_arc(d, i, on=True):
    arc = d.arcs[i]
    col, w = (YELLOW, 5) if on else (FG, 3)
    t = arc.copy()
    t.set_stroke(col, w)
    t.get_tip().set_stroke(col, 1).set_fill(col, 1)
    return Transform(arc, t)


def glow_state(d, name, on=True):
    c = d.circle[name]
    t = c.copy().set_stroke(YELLOW if on else FG, 6 if on else 4)
    return Transform(c, t)


def _native_paths():
    """Dot paths (native coordinates): Hunt -> Sight, then round Sight and on to Sync."""
    A, B, C = (D3.CENTRES[n] for n in STATES)
    r = R_PLACED
    p4 = ArcBetweenPoints(B + r * _dir(251), C + r * _dir(21), angle=-0.5)
    piece = Arc(radius=r, start_angle=np.deg2rad(21), angle=np.deg2rad(113), arc_center=C)
    p6 = ArcBetweenPoints(C + r * _dir(134), A + r * _dir(314), angle=-0.5)
    p2 = VMobject()
    p2.append_points(piece.points)
    p2.append_points(p6.points)
    return p4, p2


# ---------------------------------------------------------------- shared: labels, flip-flops
LABEL_CORNER = _p(-4.35, -3.3)
LABEL_POS = _p(3.0, 2.75)


def ff_label():
    t = T("FF labels", 30, DIM)
    m = Mono("[s2 s1 s0]", 30, GREEN)
    g = VGroup(t, m).arrange(RIGHT, buff=0.22)
    g.letters = [m[1:3], m[3:5], m[5:7]]
    return g


FF_XS = (-4.2, 0.0, 4.2)
FF_Y = -1.55
FF_SCALE = 0.75
FF_OUTS = ("s_2", "s_1", "s_0")
FF_NAMES = ("Sync", "Sight", "Hunt")


def onehot_ff(k, center, scale=FF_SCALE, out_size=44, tag_size=32):
    f = NL.make_ff(ORIGIN, size=48)
    f.remove(f.clk_w)
    f.tri.scale(1.5, about_point=f.tri.get_bottom()).set_stroke(FG, 4)
    f.scale(scale, about_point=ORIGIN).shift(center)
    o = MathTex(FF_OUTS[k], font_size=out_size, color=GREEN).next_to(f.q_w, RIGHT, buff=0.12)
    t = T(FF_NAMES[k], tag_size, YELLOW).next_to(f.box, DOWN, buff=0.25)
    g = VGroup(f, o, t)
    g.ff, g.out, g.tag = f, o, t
    return g


def onehot_ffs(xs=FF_XS, y=FF_Y, scale=FF_SCALE, tags=True):
    units = [onehot_ff(k, _p(x, y), scale) for k, x in enumerate(xs)]
    g = VGroup()
    for u in units:
        g.add(u.ff, u.out)
        if tags:
            g.add(u.tag)
    g.units = units
    g.ffs = [u.ff for u in units]
    g.outs = [u.out for u in units]
    g.tags = [u.tag for u in units]
    return g


def hop_path(a, b, rise=1.25, angle=PI / 4):
    """The travelling 1's path from point a to point b (box centres): straight up out of the box,
    over the top (peak ~0.4 above the row's box tops), straight down into the next one (it never crosses the D/Q labels)."""
    a_up, b_up = a + rise * UP, b + rise * UP
    p = VMobject()
    p.append_points(Line(a, a_up).points)
    p.append_points(ArcBetweenPoints(a_up, b_up, angle=angle if b[0] < a[0] else -angle).points)
    p.append_points(Line(b_up, b).points)
    return p


def bit_spot(ff):
    """Where a flip-flop's held bit sits: in the box, below and between the D and Q labels."""
    k = ff.box.width / NL.BOX_W
    return ff.box.get_center() + k * _p(-0.1, -0.3)


def ff_bit(ff, v, size=40):
    return Mono(v, size, GOLD if v == "1" else DIM).move_to(bit_spot(ff))


def state_var(tex="s_2", tag="Sync", size=56):
    v = MathTex(tex, font_size=size, color=GREEN)
    t = T(tag, 28, YELLOW).next_to(v, DOWN, buff=0.12)
    g = VGroup(v, t)
    g.var, g.tag = v, t
    return g


# ---------------------------------------------------------------- shared: the one-hot table
ONEHOT_ROWS = [("001", "X0", "001"), ("001", "X1", "010"),
               ("010", "0X", "010"), ("010", "10", "001"), ("010", "11", "100"),
               ("100", "0X", "100"), ("100", "10", "001"), ("100", "11", "100")]
ONEHOT_HEADS = (("s_2", "s_1", "s_0"), ("e", "r"), ("s_2'", "s_1'", "s_0'"))
TABLE_X, TABLE_SCALE = 3.1, 0.95


def onehot_table(filled=True):
    t = S5.state_table(rows=ONEHOT_ROWS, heads=ONEHOT_HEADS, breaks=(2, 5), x=TABLE_X, filled=True)
    for i, r in enumerate(ONEHOT_ROWS):
        for j, ch in enumerate(r[0]):
            if ch == "1":
                t.cell(i, 0, j).set_color(GOLD)
    t.scale(TABLE_SCALE, about_point=_p(TABLE_X, S5.TITLE_Y + 0.3))
    if not filled:
        t.remove(t.titles, t.heads, *t.rows)
    return t


# ---------------------------------------------------------------- shared: the eight patterns
PATTERNS = [format(k, "03b") for k in range(8)]
USED = ("001", "010", "100")
CHIP_Y, CHIP_PITCH = -3.0, 1.3


def _chip_colors(p, state):
    if state == "plain":
        return FG, 2, [FG] * 3
    if p in USED:
        return GREEN, 3, [GOLD if ch == "1" else GREEN for ch in p]
    if state == "final":
        return DIM, 2, [DIM] * 3
    return FG, 2, [FG] * 3


def pattern_chips(state="final"):
    g = VGroup()
    g.chip = {}
    for k, p in enumerate(PATTERNS):
        rect = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.56)
        txt = Mono(p, 30, FG)
        chip = VGroup(rect, txt).move_to(_p((k - 3.5) * CHIP_PITCH, CHIP_Y))
        txt.move_to(rect)
        chip.rect, chip.txt = rect, txt
        oc, w, cols = _chip_colors(p, state)
        rect.set_stroke(oc, w).set_fill(BG, 0)
        for gl, cc in zip(txt, cols):
            gl.set_color(cc)
        g.add(chip)
        g.chip[p] = chip
    return g


def chip_anims(chip, p, state):
    oc, w, cols = _chip_colors(p, state)
    t = chip.rect.copy().set_stroke(oc, w)
    return [Transform(chip.rect, t)] + [gl.animate.set_color(cc) for gl, cc in zip(chip.txt, cols)]


# ---------------------------------------------------------------- shared: the two joins
def opening_shot():
    lab = ff_label().move_to(LABEL_CORNER)
    return VGroup(onehot_diagram(), lab)


def handover_shot():
    return VGroup(onehot_diagram("left"), onehot_table(), pattern_chips("final"))


# ---------------------------------------------------------------- local: the Part 5 / Part 6 inset
def part5_panel():
    title = T("Part 5", 30, DIM)
    xs = (0.15, 1.25, 1.85)
    ys = (2.65, 2.2, 1.75, 1.3)
    head = [MathTex("s_1", font_size=36, color=GREEN).move_to(_p(xs[1], ys[0])),
            MathTex("s_0", font_size=36, color=GREEN).move_to(_p(xs[2], ys[0]))]
    rows = []
    for k, (n, code) in enumerate((("Hunt", "00"), ("Sight", "01"), ("Sync", "10"))):
        y = ys[k + 1]
        cells = [T(n, 28, YELLOW).move_to(_p(xs[0], y))]
        for ch, x in zip(code, xs[1:]):
            cells.append(Mono(ch, 30, GOLD if ch == "1" else FG).move_to(_p(x, y)))
        rows.append(VGroup(*cells))
    rule = Line(_p(-0.45, 2.43), _p(2.2, 2.43)).set_stroke(DIM, 2)
    table = VGroup(*head, rule, *rows)
    title.move_to(_p(0.95, 3.3))
    l1 = VGroup(MathTex("s_1", font_size=36, color=GREEN), T("= high bit,", 28)).arrange(RIGHT, buff=0.15)
    l2 = T("1 only in Sync", 28)
    tag = VGroup(l1, l2).arrange(DOWN, buff=0.14).move_to(_p(0.95, 0.6))
    col = VGroup(head[0], *[r[1] for r in rows])
    box = SurroundingRectangle(col, buff=0.1).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1)
    g = VGroup(title, table, tag)
    g.title, g.table, g.tag, g.col, g.box = title, table, tag, col, box
    return g


def part6_panel():
    title = T("Part 6", 30, DIM).move_to(_p(5.0, 3.3))
    unit = onehot_ff(1, _p(4.75, 2.25), scale=0.6, out_size=36, tag_size=28)
    line = VGroup(MathTex("s_1", font_size=36, color=GREEN), T("= Sight", 28)).arrange(RIGHT, buff=0.15)
    line.move_to(_p(5.0, 0.5))
    g = VGroup(title, unit, line)
    g.title, g.unit, g.line = title, unit, line
    return g


def output_text():
    l1 = T("An output, s should be", 32)
    l2 = T("true if in Sync state", 32)
    return VGroup(l1, l2).arrange(DOWN, buff=0.16).move_to(_p(3.0, 2.75))


def s_wire(ff):
    q_end = ff.q_w.get_right()
    x0, top = q_end[0] - 0.25, -0.25
    wire = VMobject().set_points_as_corners([_p(x0, q_end[1]), _p(x0, top), _p(-1.75, top)])
    wire.set_stroke(GREEN, 5)
    tip = Triangle().set_stroke(width=0).set_fill(GREEN, 1).scale(0.12).rotate(-PI / 2).move_to(_p(-1.7, top))
    lab = MathTex("s", font_size=44, color=GREEN).next_to(tip, RIGHT, buff=0.12)
    g = VGroup(wire, tip, lab)
    g.wire, g.tip, g.lab = wire, tip, lab
    return g


class ThreeFlipFlops(NarratedScene):
    def construct(self):
        shot = opening_shot()
        d, lab = shot[0], shot[1]
        self.add(d, lab)
        self.d, self.lab = d, lab
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(1.0)      # handover: hold the final shot

    # ------------------------------------------------------------ c6.codes.1
    def clip1(self):
        d, lab = self.d, self.lab
        with self.say("c6.codes.1") as c:
            d.generate_target()
            _roomy(d.target, "top")
            self.play(*during([MoveToTarget(d)], 0, 0.65),
                      *during([lab.animate.scale(1.2).move_to(LABEL_POS)], 0.45, 1.0),
                      run_time=min(2.2, c.until("ess two", floor=1.2)))
            c.wait_until("ess two")
            t1 = c.at("ess one") - c.at("ess two")
            t2 = c.at("ess zero") - c.at("ess two")
            anims = []
            for k, start in enumerate((0.0, t1, t2)):
                for gl in lab.letters[k]:
                    anims.append(time_span(gl.animate(rate_func=there_and_back).set_color(YELLOW),
                                           start, start + 1.0))
            self.play(*anims, run_time=t2 + 1.0)

            for n, cue in (("Hunt", "hunt"), ("Sight", "sight"), ("Sync", "sync")):
                c.wait_until(cue)
                self.play(FlashAround(d.code[n], color=GOLD, time_width=1.5),
                          d.one[n].animate(rate_func=there_and_back).scale(1.7).set_color(YELLOW),
                          d.circle[n].animate(rate_func=there_and_back).set_stroke(YELLOW, 6),
                          run_time=1.4)

            c.wait_until("hot")
            ffs = onehot_ffs(tags=False)
            self.ffs = ffs
            items = []
            for u in ffs.units:
                items += [u.ff, u.out]
            self.play(*appear(*items, lag=0.15), run_time=1.6)
            bits = [ff_bit(f, v) for f, v in zip(ffs.ffs, "001")]
            self.play(*appear(*bits, shift=None), glow_state(d, "Hunt"), run_time=1.0)
            self.play(FlashAround(bits[2], color=GOLD, time_width=1.5), run_time=1.0)

            c.wait_until("hop")
            p4, p2 = _native_paths()
            for p in (p4, p2):
                p.scale(DIAG_SCALE, about_point=ORIGIN).shift(TOP_SHIFT)
            dot = Dot(p4.get_start(), radius=0.1, color=YELLOW)
            self.play(FadeIn(dot, scale=0.5), run_time=0.4)
            self.dot = dot
            one = bits[2]
            for path, src, dst, frm, to in ((p4, 2, 1, "Hunt", "Sight"), (p2, 1, 0, "Sight", "Sync")):
                new0 = ff_bit(ffs.ffs[src], "0")
                self.play(MoveAlongPath(dot, path),
                          *during([glow_state(d, frm, False), glow_state(d, to)], 0.5, 1.0),
                          *during(disappear(bits[dst]), 0, 0.3),
                          *during([MoveAlongPath(one, hop_path(one.get_center(), bit_spot(ffs.ffs[dst])))], 0.2, 0.85),
                          *during(appear(new0, shift=None), 0.7, 1.0),
                          run_time=2.0)
                bits[src] = new0
                bits[dst] = one
                self.wait(0.2)
            self.bits = bits

    # ------------------------------------------------------------ c6.codes.2
    def clip2(self):
        d, lab, ffs = self.d, self.lab, self.ffs
        with self.say("c6.codes.2") as c:
            self.play(FadeOut(self.dot), glow_state(d, "Sync", False), run_time=1.0)
            for k in (2, 1, 0):      # Hunt, Sight, Sync: the order they are named
                tag = ffs.tags[k]
                c.wait_until(own_word=tag)
                self.play(*appear(tag), FlashAround(ffs.ffs[k].box, color=YELLOW, time_width=1.5), run_time=1.1)

            c.wait_until("careful")
            a = part5_panel()
            self.play(*during(disappear(lab), 0, 0.45),
                      *during(appear(a.title, a.table, lag=0.2), 0.5, 1.0), run_time=1.5)
            c.wait_until("In Part five")
            self.play(FadeIn(a.box), FlashAround(a.col, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until(own_word=a.tag[0][1])
            self.play(*appear(a.tag, lag=0.4), run_time=1.2)

            c.wait_until("now")
            b = part6_panel()
            self.play(FlashAround(ffs.ffs[1].box, color=YELLOW, time_width=1.5),
                      *appear(b.unit, b.title, b.line, lag=0.3), run_time=1.8)
            c.wait_until("Same name")
            neq = MathTex(r"\neq", font_size=72, color=YELLOW).move_to(_p(2.95, 1.95))
            self.play(GrowFromCenter(neq), FlashAround(a.col, color=YELLOW, time_width=1.5),
                      FlashAround(b.unit.out, color=YELLOW, time_width=1.5), run_time=1.4)
            self.inset = [a.title, a.table, a.tag, a.box, b.title, b.unit, b.line, neq]

    # ------------------------------------------------------------ c6.codes.3
    def clip3(self):
        d, ffs = self.d, self.ffs
        with self.say("c6.codes.3") as c:
            out = output_text()
            self.play(*during(disappear(*self.inset), 0, 0.45),
                      *during(appear(out), 0.5, 1.0), run_time=1.6)
            self.out = out

            c.wait_until("inspect")
            self.play(FlashAround(ffs.ffs[0].box, color=YELLOW, time_width=1.5),
                      FlashAround(self.bits[0], color=GOLD, time_width=1.5), run_time=1.3)
            w = s_wire(ffs.ffs[0])
            self.play(Create(w.wire), *during([FadeIn(w.tip)], 0.7, 1.0),
                      *during(appear(w.lab, shift=None), 0.75, 1.0), run_time=1.5)
            self.wire = w

            c.wait_until("So by inspection")
            frm = T("From inspection,", 30).move_to(_p(1.75, 1.35))
            sv = state_var("s_2", "Sync", 56)
            eq_l = MathTex("s", "=", font_size=56, color=GREEN)
            eq_l.next_to(frm, RIGHT, buff=0.35)
            sv.next_to(eq_l, RIGHT, buff=0.2)
            sv.shift((eq_l.get_center()[1] - sv.var.get_center()[1]) * UP)
            self.play(*appear(frm, eq_l, sv, lag=0.3), run_time=1.6)
            self.eq = VGroup(frm, eq_l, sv)
            c.wait_until("once again")
            self.play(VShowPassingFlash(w.wire.copy().set_stroke(YELLOW, 8), time_width=0.4), run_time=1.5)

    # ------------------------------------------------------------ c6.codes.4
    def clip4(self):
        d = self.d
        tab = onehot_table()
        self.tab = tab
        with self.say("c6.codes.4", gap=0.8) as c:
            sweep_clear(self, *during([d.animate.shift(LEFT_SHIFT - TOP_SHIFT)], 0.5, 1.0),
                        *during([Create(tab.lines)], 0.55, 1.0), keep=[d], run_time=2.0)
            self.play(*appear(tab.titles, tab.heads, lag=0.4), run_time=1.6)   # early: the table's header, shown whole before it is read

            c.wait_until("row1")
            self.play(glow_state(d, "Hunt"), run_time=1.0)
            r0 = tab.rows[0]
            c.wait_until("In Hunt")
            self.play(*appear(r0[0], shift=None), FlashAround(d.code["Hunt"], color=GOLD, time_width=1.5),
                      run_time=1.2)
            c.wait_until("if ar is zero")
            self.play(*appear(r0[1], shift=None), light_arc(d, ROW_ARC[0]), run_time=1.2)
            c.wait_until("we stay in Hunt")
            self.play(*appear(r0[2], shift=None), run_time=1.2)

            c.wait_until("row2")
            self.play(light_arc(d, ROW_ARC[0], False), light_arc(d, ROW_ARC[1]),
                      *appear(tab.rows[1], shift=None), run_time=1.5)

            c.wait_until("rest")
            total = c.until(None, floor=2.5) - 0.15
            step = (total - 0.9) / 5
            anims = [time_span(light_arc(d, ROW_ARC[1], False), 0, 0.4)]
            for i in range(2, 8):
                t = step * (i - 2)
                arc = light_arc(d, ROW_ARC[i])
                arc.rate_func = there_and_back_with_pause
                anims.append(time_span(arc, t, t + 0.9))
                anims += during(appear(tab.rows[i], shift=None), t / total, min(1.0, (t + 0.6) / total))
            # the state being read glows: Hunt off, Sight for rows 2-4, Sync for rows 5-7
            anims.append(time_span(glow_state(d, "Hunt", False), 0, 0.4))
            for name, a, b in (("Sight", 0.0, 3 * step), ("Sync", 3 * step, total)):
                g = glow_state(d, name)
                g.rate_func = there_and_back_with_pause
                anims.append(time_span(g, a, b))
            self.play(*anims, run_time=total)

    # ------------------------------------------------------------ c6.codes.5
    def clip5(self):
        d, tab = self.d, self.tab
        with self.say("c6.codes.5") as c:
            chips = pattern_chips("plain")
            self.play(*appear(*chips, lag=0.12), run_time=1.6)
            c.wait_until("we use only three")
            anims = []
            for p in USED:
                anims += chip_anims(chips.chip[p], p, "lit")
            self.play(*anims, run_time=1.2)

            c.wait_until("five")
            anims = []
            for p in PATTERNS:
                if p not in USED:
                    anims += chip_anims(chips.chip[p], p, "final")
            self.play(*anims, run_time=1.2)

            c.wait_until("notlisted")
            gy = tab.rows[7][0][0].get_center()[1] - 0.6
            ghost = VGroup(*[MathTex(r"\ ".join(s), font_size=36, color=DIM).move_to(
                _p(np.mean([m.get_center()[0] for m in tab.rows[0][g]]), gy))
                for g, s in enumerate(("11", "XX", "XX"))])
            note = T("Part 5:", 28, DIM).next_to(ghost, LEFT, buff=0.45)
            self.play(*appear(note, ghost, lag=0.3), run_time=1.2)

            c.wait_until("why")
            self.play(*disappear(note, ghost), run_time=0.9)
            self.play(*[FlashAround(chips.chip[p], color=GREEN, time_width=1.5) for p in USED],
                      *[FlashAround(d.code[n], color=GOLD, time_width=1.5) for n in STATES], run_time=1.6)
