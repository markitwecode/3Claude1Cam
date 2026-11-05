"""Chapter 1, scene 4: the 15-state table drawn as a four-layer diagram. Clips c1.tree.1 – c1.tree.3.

Owns the 15-state diagram reused by s1, s5–s6 and s7/s8. Module-level helpers:
  tree_diagram(labelled=True, zeros_dim=True, bundle=True, ones=True) -> TreeDiagram (VGroup)
    .states[name]          StateCircle (VGroup: .circle, .letter), by letter "A".."P" (no O)
    .arcs[(name, x)]       Arrow for state name on input x (0 left, 1 right), A..G only
    .labels[(name, x)]     MealyLabel on that arc
    .stubs[name]           short Line down from each bottom state (H..P) into the bundle
    .bundle                VGroup(path, tip): the bundled arrow along the bottom, up the left, into A
    .bundle_label          VGroup(MealyLabel 0/0, comma, MealyLabel 1/0), under the bundle
    .ones[name]            MealyLabel 1/1 just left of J's and L's own stubs
    .layers                [[A], [B, C], [D..G], [H..P]] state names by layer
  mealy_label(inp, out, size=28, out_color=None) -> MealyLabel (.inp BLUE, .slash FG, .out GREEN;
    a 0 output DIM when out_color=DIM); place_on_arc(label, start, end, side)
  NEXT[name] = (next on 0, next on 1); OUT[(name, x)] = output; POS[name] = centre
  handover_shot() = tree_diagram(): the final {later} frame (zeros DIM, 1/1 labels, bundle).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- the machine (p. 145, checked)
NEXT = {
    "A": ("B", "C"), "B": ("D", "E"), "C": ("F", "G"),
    "D": ("H", "I"), "E": ("J", "K"), "F": ("L", "M"), "G": ("N", "P"),
}
for _s in "HIJKLMNP":
    NEXT[_s] = ("A", "A")
OUT = {(s, x): 0 for s in NEXT for x in (0, 1)}
OUT[("J", 1)] = 1
OUT[("L", 1)] = 1

LAYERS = [["A"], ["B", "C"], ["D", "E", "F", "G"], list("HIJKLMNP")]
LAYER_Y = [2.9, 1.45, 0.0, -1.45]
PITCH = 1.35                      # bottom-row pitch
R = 0.36                          # circle radius
BUS_Y = -2.7                      # the bundle's bottom run
BUS_X = -6.0                      # the bundle's left side


def _positions():
    pos = {}
    xs = [(i - 3.5) * PITCH for i in range(8)]
    for name, x in zip(LAYERS[3], xs):
        pos[name] = np.array([x, LAYER_Y[3], 0])
    for k in (2, 1, 0):
        for name in LAYERS[k]:
            a, b = NEXT[name]
            pos[name] = np.array([(pos[a][0] + pos[b][0]) / 2, LAYER_Y[k], 0])
    return pos


POS = _positions()


class StateCircle(VGroup):
    def __init__(self, name, radius=R, size=34):
        self.circle = Circle(radius=radius).set_stroke(FG, 3).set_fill(BG, 0)
        self.letter = T(name, size)
        self.name = name
        super().__init__(self.circle, self.letter)


class MealyLabel(VGroup):
    def __init__(self, inp, out, size=28, out_color=None):
        self.inp = T(str(inp), size, BLUE)
        self.slash = T("/", size, FG)
        if out_color is None:
            out_color = GREEN
        self.out = T(str(out), size, out_color)
        super().__init__(self.inp, self.slash, self.out)
        self.arrange(RIGHT, buff=0.04)
        self.slash.align_to(self.inp, DOWN)


def mealy_label(inp, out, size=28, out_color=None):
    return MealyLabel(inp, out, size, out_color)


def place_on_arc(label, start, end, side):
    """Put label beside the arc start→end, on the outer side (side -1: left arc, +1: right arc)."""
    d = end - start
    d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0], 0])
    if np.sign(n[0]) != side:
        n = -n
    off = 0.12 + abs(n[0]) * label.width / 2 + abs(n[1]) * label.height / 2
    label.move_to((start + end) / 2 + n * off)
    return label


def _edge(a, b, r=R):
    d = b - a
    return a + d / np.linalg.norm(d) * r


class TreeDiagram(VGroup):
    def __init__(self, labelled=True, zeros_dim=True, bundle=True, ones=True):
        super().__init__()
        self.layers = LAYERS
        self.states, self.arcs, self.labels, self.stubs, self.ones = {}, {}, {}, {}, {}
        zc = DIM if zeros_dim else GREEN
        for name, p in POS.items():
            self.states[name] = StateCircle(name).move_to(p)
        for name in "ABCDEFG":
            for x in (0, 1):
                tgt = NEXT[name][x]
                s, e = _edge(POS[name], POS[tgt]), _edge(POS[tgt], POS[name])
                arc = Arrow(s, e, buff=0, stroke_width=3, color=FG, tip_length=0.18,
                            max_tip_length_to_length_ratio=0.2)
                self.arcs[(name, x)] = arc
                if labelled:
                    o = OUT[(name, x)]
                    lbl = place_on_arc(mealy_label(x, o, out_color=GREEN if o else zc), s, e, -1 if x == 0 else 1)
                    self.labels[(name, x)] = lbl
        self.add(*self.states.values(), *self.arcs.values(), *self.labels.values())
        self.bundle = VGroup()
        self.bundle_label = VGroup()
        if bundle:
            for name in LAYERS[3]:
                p = POS[name]
                self.stubs[name] = Line(p + R * DOWN, [p[0], BUS_Y, 0]).set_stroke(FG, 3)
            a = POS["A"]
            tip_start = np.array([a[0] - R - 0.7, a[1], 0])
            path = VMobject().set_points_as_corners([
                [POS["P"][0], BUS_Y, 0], [BUS_X, BUS_Y, 0], [BUS_X, a[1], 0], tip_start,
            ]).set_stroke(FG, 4)
            tip = Arrow(tip_start, a + R * LEFT, buff=0, stroke_width=4, color=FG, tip_length=0.2,
                        max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)
            self.bundle = VGroup(path, tip)
            if labelled:
                l0, l1 = mealy_label(0, 0, 30, zc), mealy_label(1, 0, 30, zc)
                comma = T(",", 30)
                self.bundle_label = VGroup(l0, comma, l1).arrange(RIGHT, buff=0.08)
                l1.shift(0.12 * RIGHT)
                comma.align_to(l0, DOWN).shift(0.06 * DOWN)
                self.bundle_label.move_to([-3.7, BUS_Y - 0.42, 0])
            self.add(*self.stubs.values(), self.bundle, self.bundle_label)
            if ones and labelled:
                for name in "JL":
                    lbl = mealy_label(1, 1)
                    lbl.next_to(self.stubs[name], LEFT, buff=0.1)   # its own stub's left: reads as J's / L's
                    self.ones[name] = lbl
                self.add(*self.ones.values())

    def all_outputs(self):
        outs = [l.out for l in self.labels.values()]
        if len(self.bundle_label):
            outs += [self.bundle_label[0].out, self.bundle_label[2].out]
        return outs


def tree_diagram(labelled=True, zeros_dim=True, bundle=True, ones=True):
    return TreeDiagram(labelled, zeros_dim, bundle, ones)


def handover_shot():
    return tree_diagram()


# ---------------------------------------------------------------- the scene
class TableAsDiagram(NarratedScene):
    def construct(self):
        d = tree_diagram(zeros_dim=False)
        self.d = d
        self.clip1(d)
        self.clip2(d)
        self.clip3(d)
        self.wait(1.0)          # handover: hold the full diagram; s5 slides it right

    def _light(self, names):
        return [restyle(self.d.states[n], op=1) for n in names]

    def clip1(self, d):
        S, A_, L = d.states, d.arcs, d.labels
        with self.say("c1.tree.1") as c:
            # {draw}: the whole shape first, A bright, the rest faint
            for n, s in S.items():
                if n != "A":
                    s.circle.set_stroke(opacity=DIMMED)
                    s.letter.set_fill(opacity=DIMMED)
            self.play(FadeIn(S["A"], scale=0.8), run_time=1.0)
            rest = [S[n] for lay in LAYERS[1:] for n in lay]
            self.play(LaggedStart(*[FadeIn(s) for s in rest], lag_ratio=0.12),
                      run_time=min(2.2, c.until("a")))
            c.wait_until("a")

            # {a}: A's two arcs, B and C light as they arrive
            def grow(names, rt):
                arcs = [A_[(n, x)] for n in names for x in (0, 1)]
                lbls = [L[(n, x)] for n in names for x in (0, 1)]
                tg = [NEXT[n][x] for n in names for x in (0, 1)]
                self.play(*[GrowArrow(a) for a in arcs],
                          *during(self._light(tg), 0.5, 1.0),
                          *during(appear(*lbls, shift=None, lag=0), 0.55, 1.0),
                          run_time=rt)
            grow(["A"], min(1.8, c.until("layer2")))
            c.wait_until("layer2")
            grow(["B", "C"], min(1.8, c.until("layer3")))
            c.wait_until("layer3")
            grow(["D", "E", "F", "G"], min(2.0, c.until("layers")))
            c.wait_until("layers")

            # {layers}: 1, 2, 4, 8 = 15
            counts = [T(str(k), 36, GOLD).move_to([6.15, y, 0]) for k, y in zip((1, 2, 4, 8), LAYER_Y)]
            for cnt, (cue, nth) in zip(counts, [("one", 0), ("two", 1), ("four", 3), ("eight", 1)]):
                c.wait_until(cue, nth=nth)
                self.play(*appear(cnt, shift=0.15 * DOWN), run_time=0.6)
            rule = Line([5.75, -1.9, 0], [6.55, -1.9, 0]).set_stroke(GOLD, 2)
            total = T("15", 40, GOLD).move_to([6.15, -2.35, 0])
            self.play(GrowFromCenter(rule), *during(appear(total, shift=0.15 * DOWN), 0.3, 1.0), run_time=0.9)
            self.counts = VGroup(*counts, rule, total)
            c.wait_until("left")

            # {left}: left arcs pulse BLUE, "input 0"; then the right arcs, "input 1"
            tag0 = T("input 0", 30, BLUE).move_to([-4.7, 2.45, 0])
            tag1 = T("input 1", 30, BLUE).move_to([4.6, 2.45, 0])
            for x, tag in ((0, tag0), (1, tag1)):
                c.wait_until(own_word=tag)
                lines = [Line(A_[(n, x)].get_start(), A_[(n, x)].get_end()).set_stroke(BLUE, 8)
                         for n in "ABCDEFG"]
                self.play(*[VShowPassingFlash(ln, time_width=0.8) for ln in lines],
                          *flash([L[(n, x)].inp for n in "ABCDEFG"], color=BLUE),
                          *appear(tag, shift=None), run_time=1.4)
            self.tags = [tag0, tag1]

    def clip2(self, d):
        S = d.states
        with self.say("c1.tree.2") as c:
            # {back}: each bottom state grows a stub down
            self.play(LaggedStart(*[Create(d.stubs[n]) for n in LAYERS[3]], lag_ratio=0.1),
                      run_time=min(1.6, c.until("bundle")))
            c.wait_until("bundle")
            # {bundle}: one bundled arrow back to A
            path, tip = d.bundle
            self.play(*during(Create(path), 0, 0.85), *during(GrowArrow(tip), 0.82, 1.0),
                      *disappear(*self.tags), run_time=min(2.4, c.until("outputs")))
            ring = S["A"].circle.copy().set_stroke(YELLOW, 6)
            self.play(*appear(d.bundle_label, shift=0.15 * DOWN), VShowPassingFlash(ring, time_width=0.6),
                      run_time=1.0)
            c.wait_until("outputs")
            # {outputs}: every output digit pulses
            outs = d.all_outputs()
            self.play(*flash(outs, color=GREEN, run_time=1.4, time_width=1.5), run_time=1.5)
            c.wait_until("zeros")
            self.play(*recolor(outs, DIM), run_time=1.2)
            c.wait_until("ones")
            # {ones}: J's and L's own 1/1 labels
            self.play(*appear(d.ones["J"], d.ones["L"], shift=0.15 * DOWN, lag=0.3), run_time=1.2)
            self.play(*flash([d.ones["J"].out, d.ones["L"].out], color=GREEN), run_time=1.0)
            for n, cue in (("J", "jay"), ("L", "state L")):
                c.wait_until(cue)
                rt = min(0.9, c.until(floor=0.4))
                self.play(FlashAround(S[n], color=YELLOW, run_time=rt), run_time=rt)

    def clip3(self, d):
        S = d.states
        with self.say("c1.tree.3") as c:
            # {four}: the layer counts make way for a bit counter
            xs = [4.4 + 0.6 * i for i in range(4)]
            bits = [T(str(i + 1), 34, GOLD).move_to([x, 3.35, 0]) for i, x in enumerate(xs)]
            rowlab = [T(w, 28, DIM).move_to([3.55, y, 0]) for w, y in (("bit", 3.35), ("in", 2.8), ("out", 2.25))]
            self.play(*disappear(self.counts), run_time=0.8)
            self.play(*appear(*rowlab, *bits, shift=0.15 * DOWN, lag=0.08), run_time=1.4)
            c.wait_until("walk")
            # {walk}: 1, 1, 0, 0 : A -> C -> G -> N -> A
            dot = Dot(POS["A"], radius=0.24, color=YELLOW).set_fill(opacity=0.55).set_z_index(-1)
            self.play(FadeIn(dot, scale=0.5), run_time=0.5)
            seq = [1, 1, 0, 0]
            cur = "A"
            ins, outs = [], []
            cues = [("one", 0), ("one", 1), ("zero", 0), ("zero", 1)]
            for i, (x, (cue, nth)) in enumerate(zip(seq, cues)):
                nxt = NEXT[cur][x]
                if nxt == "A":
                    p = POS[cur]
                    path = VMobject().set_points_as_corners([
                        p, [p[0], BUS_Y, 0], [BUS_X, BUS_Y, 0], [BUS_X, POS["A"][1], 0], POS["A"]])
                    rt = 2.0
                else:
                    path = Line(POS[cur], POS[nxt])
                    rt = 1.2 if i == 0 else 0.9
                din = T(str(x), 34, BLUE).move_to([xs[i], 2.8, 0])
                dout = T(str(OUT[(cur, x)]), 34, GREEN).move_to([xs[i], 2.25, 0])
                c.wait_until(cue, nth=nth)
                self.play(*during(appear(din, shift=None), 0, 0.35),
                          *during(MoveAlongPath(dot, path, rate_func=smooth), 0.1, 0.85),
                          *during(appear(dout, shift=None), 0.75, 1.0), run_time=rt)
                ins.append(din)
                outs.append(dout)
                cur = nxt
            # {restart}: back on A; the counter resets
            c.wait_until("what")
            self.play(*disappear(*ins, *outs), FlashAround(bits[0], color=GOLD, run_time=1.0),
                      FlashAround(S["A"], color=YELLOW, run_time=1.0), run_time=1.0)
            # {what}: the two 1/1 labels pulse; a "?"
            q = T("?", 56, YELLOW).move_to([-0.45, BUS_Y - 0.5, 0])
            self.play(*flash([d.ones["J"], d.ones["L"]], color=GREEN, run_time=1.5, time_width=1.5),
                      FadeOut(dot), *during(appear(q, shift=0.2 * DOWN), 0.4, 1.0), run_time=1.5)
            c.wait_until("later")
            # {later}: back to the full diagram
            self.play(*disappear(q, *bits, *rowlab), run_time=1.0)
