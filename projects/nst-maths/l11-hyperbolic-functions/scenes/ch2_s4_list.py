"""Chapter 2, scene 4: the whole family, each identity beside its trig parent. Clips c2.list.1 – c2.list.3.

Opens on ch2_s3_addition's handover_shot() (boxed cosh(A + B) line), which moves into row 1.
Two columns at size 34, rows spread down the frame: BLUE trig parents (=) on the left, TEAL list (95) (≡) on the right,
aligned on = / ≡; changed signs YELLOW. Rows 3-4 get a GREEN "no change" tag; a boxed
workspace below the list shows the i-cancellation, then (93) divided by cosh² / sinh²
turning into rows 5 and 6. Ends with the finished list centred, then an empty frame.

Module-level builders for reuse: parent(i), child(i) (i = 0..5), placed on row i.
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

S3 = load_scene("ch2_s3_addition")
S4 = load_scene("ch1_s4_cosix")
ctex, at_glyph = S4.ctex, S4.at_glyph

SZ = 34
PITCH = 0.95
Y = [3.15 - PITCH * i for i in range(6)]
LEFT_X = -6.62
GAP = 0.4

_TRIG = "BBBFFFFF F BBBF BBBF F BBBF BBBF"
_HYP = "TTTTFFFFF F TTTTF TTTTF F TTTTF TTTTF"
_HYP_Y = "TTTTFFFFF F TTTTF TTTTF Y TTTTF TTTTF"
PARENTS = [
    (r"\cos(A + B) = \cos A \cos B - \sin A \sin B", _TRIG, 8),
    (r"\cos(A - B) = \cos A \cos B + \sin A \sin B", _TRIG, 8),
    (r"\sin(A + B) = \sin A \cos B + \sin B \cos A", _TRIG, 8),
    (r"\sin(A - B) = \sin A \cos B - \sin B \cos A", _TRIG, 8),
    (r"1 + \tan^2 z = \sec^2 z", "F F BBBB F F BBBB F", 7),
    (r"\cot^2 z + 1 = \operatorname{cosec}^2 z", "BBBB F F F F BBBBBB F", 7),
]
CHILDREN = [
    (r"\cosh(A + B) \equiv \cosh A \cosh B + \sinh A \sinh B", _HYP_Y, 9),
    (r"\cosh(A - B) \equiv \cosh A \cosh B - \sinh A \sinh B", _HYP_Y, 9),
    (r"\sinh(A + B) \equiv \sinh A \cosh B + \sinh B \cosh A", _HYP, 9),
    (r"\sinh(A - B) \equiv \sinh A \cosh B - \sinh B \cosh A", _HYP, 9),
    (r"1 - \tanh^2 z \equiv \operatorname{sech}^2 z", "F Y TTTTT F F TTTTT F", 8),
    (r"\coth^2 z - 1 \equiv \operatorname{cosech}^2 z", "TTTTT F Y F F TTTTTTT F", 8),
]
SIGN = 20           # glyph index of the middle sign in rows 1-4 (both columns: child 20, parent 17)
SIGN_P = 17


def _columns():
    p = ctex(PARENTS[0][0], PARENTS[0][1], size=SZ)
    p.shift((LEFT_X - p.get_left()[0]) * RIGHT)
    xl = p[0][8].get_x()
    ch = ctex(CHILDREN[0][0], CHILDREN[0][1], size=SZ)
    ch.shift((p.get_right()[0] + GAP - ch.get_left()[0]) * RIGHT)
    return xl, ch[0][9].get_x(), ch.get_right()[0]


XL, XR, RIGHT_EDGE = _columns()


def parent(i):
    src, pat, k = PARENTS[i]
    return at_glyph(ctex(src, pat, size=SZ), k, XL, Y[i])


def child(i):
    src, pat, k = CHILDREN[i]
    return at_glyph(ctex(src, pat, size=SZ), k, XR, Y[i])


# ---------------------------------------------------------------- workspace (93)
FS = 40
WS = np.array([0.0, -2.55, 0.0])
WHY_Y = -1.75


def ws_layout(terms):
    st = MathTex(terms[0], "-", terms[1], r"\equiv", terms[2], font_size=FS).move_to(WS)
    return [st[i].get_center() for i in range(5)]


def piece(s, at):
    return MathTex(s, font_size=FS, color=TEAL).move_to(at)


def tag_for(rows):
    top, bot = rows[0].get_top()[1], rows[-1].get_bottom()[1]
    x = RIGHT_EDGE + 0.12
    br = Line([x, top + 0.04, 0], [x, bot - 0.04, 0], color=GREEN, stroke_width=3)
    return br


class List(NarratedScene):
    def construct(self):
        self.P = [parent(i) for i in range(6)]
        self.C = [None, child(1), child(2), child(3), child(4), child(5)]
        self.clip1()
        self.clip2()
        self.clip3()

    # ------------------------------------------------------------ c2.list.1
    def clip1(self):
        P, C = self.P, self.C
        shot = S3.handover_shot()
        line1, box = shot[0], shot[1]
        self.add(line1, box)
        with self.say("c2.list.1") as c:
            c.wait_until("list")
            self.play(*appear(P[0], shift=None), run_time=1.0)
            c.wait_until("changed signs")
            self.play(FlashAround(line1[0][SIGN], run_time=1.5, time_width=1.5))
            c.wait_until("first")
            line1.generate_target()
            line1.target.scale(SZ / 50)
            at_glyph(line1.target, 9, XR, Y[0])
            self.play(MoveToTarget(line1), *during(disappear(box), 0, 0.4), run_time=1.6)
            C[0] = line1
            c.wait_until("minusB")
            self.play(*appear(P[1], C[1], lag=0.4, shift=None), run_time=1.6)
            c.wait_until("becomes a minus")
            self.play(FlashAround(C[1][0][SIGN], run_time=1.5, time_width=1.5))
            c.wait_until("Again")
            self.play(FlashAround(P[1][0][SIGN_P], color=BLUE, run_time=1.2, time_width=1.5),
                      FlashAround(C[1][0][SIGN], run_time=1.2, time_width=1.5))

    # ------------------------------------------------------------ c2.list.2
    def clip2(self):
        P, C = self.P, self.C
        with self.say("c2.list.2") as c:
            self.play(*appear(P[2], C[2], lag=0.4, shift=None), run_time=min(1.6, c.until("same")))
            c.wait_until("same")
            self.play(FlashUnder(C[2][0][10:], run_time=2, time_width=1.5))

            c.wait_until("nochange")
            self.bracket = tag_for([C[2]])
            self.tag = T("no change", size=28, color=GREEN)
            self.tag.next_to(self.bracket, DOWN, buff=0.12).align_to(self.bracket, RIGHT)
            self.play(GrowFromCenter(self.bracket), *appear(self.tag, shift=None), run_time=1.0)

            # the door, side box
            c.wait_until("why")
            la = ctex(r"\sin(i(A + B)) = i\sinh(A + B)",
                      "BBB F P F FFF FF F P TTTT FFFFF", size=40)
            lb = ctex(r"\sin(iA + iB) = i\sinh A \cosh B + \cosh A \cdot i\sinh B",
                      "BBB F P F F P F F F P TTTT F TTTT F F TTTT F F P TTTT F", size=40)
            x_eq = -2.2
            at_glyph(la, 11, x_eq, WHY_Y + 0.45)
            at_glyph(lb, 10, x_eq, WHY_Y - 0.45)
            grp = VGroup(la, lb)
            grp.shift((0 - grp.get_center()[0]) * RIGHT)
            wbox = SurroundingRectangle(grp, color=DIM, buff=0.3, corner_radius=0.15, stroke_width=2)
            self.play(FadeIn(wbox), *appear(la, lb, lag=0.5, shift=None), run_time=2.0)

            c.wait_until("just one eye")
            self.play(*flash([lb[0][11], lb[0][29]], color=PINK), run_time=1.0)

            # same left side, so join the two right sides into one equation
            lc = ctex(r"i\sinh(A + B) = i\sinh A \cosh B + \cosh A \cdot i\sinh B",
                      "P TTTT FFFFF F P TTTT F TTTT F F TTTT F F P TTTT F", size=40)
            at_glyph(lc, 10, lb[0][10].get_x(), WHY_Y)
            wbox2 = SurroundingRectangle(lc, color=DIM, buff=0.3, corner_radius=0.15, stroke_width=2)
            self.play(*during(disappear(la), 0, 0.35), *during(edit(lb, lc), 0.3, 1.0),
                      Transform(wbox, wbox2), run_time=max(0.9, min(1.6, c.until("cancel") - 0.05)))
            self.why = [wbox, lc]

            c.wait_until("cancel")
            ivs = [lc[0][0], lc[0][11], lc[0][29]]
            strikes = [Line(g.get_corner(DL) + 0.06 * (DL), g.get_corner(UR) + 0.06 * UR,
                            color=RED, stroke_width=4) for g in ivs]
            self.play(*[Create(s) for s in strikes], *recolor(ivs, DIM), run_time=1.2)
            self.why += strikes

            c.wait_until("diff")
            br2 = tag_for([C[2], C[3]])
            tag2 = self.tag.copy().next_to(br2, DOWN, buff=0.12).align_to(br2, RIGHT)
            self.play(*appear(P[3], C[3], lag=0.4, shift=None),
                      Transform(self.bracket, br2),
                      *during(disappear(self.tag), 0, 0.35), *during(appear(tag2, shift=None), 0.6, 1.0),
                      run_time=1.6)
            self.tag = tag2

    # ------------------------------------------------------------ c2.list.3
    def derive_into(self, c, terms_seq, cues, rt):
        """Swap the workspace pieces term by term (terms_seq[k] = the line after step k)."""
        for k, cue in enumerate(cues):
            c.wait_until(cue)
            new_pos = ws_layout(terms_seq[k + 1])
            idx = [0, 2, 4][k]
            new = piece(terms_seq[k + 1][k], new_pos[idx])
            others = [j for j in range(5) if j != idx]
            moves = [self.pieces[j].animate.move_to(new_pos[j]) for j in others]
            extra = []
            if k == 0 and self.box93 is not None:
                extra = during(disappear(self.box93), 0, 0.45)
                self.box93 = None
            self.play(*swap(self.pieces[idx], new), *during(moves, 0.4, 1.0), *extra,
                      run_time=rt[k])
            self.pieces[idx] = new

    def slide_into(self, row, div, rt=1.5, swap_rt=0.9):
        P = self.P
        ws = VGroup(*self.pieces)
        settle(self, ws)
        ws.generate_target()
        ws.target.scale(SZ / FS)
        ws.target[1].set_color(YELLOW)
        ws.target.shift(np.array([XR, Y[row], 0]) - ws.target[3].get_center())
        self.play(MoveToTarget(ws), *during(disappear(div), 0, 0.4),
                  *during(appear(P[row], shift=None), 0.3, 1.0), run_time=rt)
        self.play(*swap(ws, self.C[row], shift=0.1 * UP), run_time=swap_rt)

    def clip3(self):
        with self.say("c2.list.3", gap=0.1) as c:
            # scene 2's boxed (93) returns, then is relabelled to z at once
            tx = (r"\cosh^2 x", "-", r"\sinh^2 x", r"\equiv", "1")
            t0 = (r"\cosh^2 z", "-", r"\sinh^2 z", r"\equiv", "1")
            f93x = MathTex(*tx, font_size=FS, color=TEAL).move_to(WS)
            self.box93 = SurroundingRectangle(f93x, color=YELLOW, buff=0.25)
            self.play(*during(disappear(*self.why), 0, 0.45),
                      *during(appear(f93x, self.box93, lag=0, shift=None), 0.5, 1.0),
                      run_time=1.6)
            c.wait_until("minus shine")
            f93 = MathTex(*t0, font_size=FS, color=TEAL).move_to(WS)
            self.play(*edit(f93x, f93), run_time=1.2)
            pos = ws_layout([t0[0], t0[2], t0[4]])
            self.pieces = [piece(s, p) for s, p in zip(t0, pos)]
            self.remove(*f93.get_family())
            self.add(*self.pieces)

            c.wait_until("divcosh")
            div = MathTex(r"\div\, \cosh^2 z", font_size=36, color=YELLOW).move_to(WS + 0.75 * DOWN)
            self.play(*appear(div), run_time=1.0)

            seq = [(r"\cosh^2 z", r"\sinh^2 z", "1"),
                   ("1", r"\sinh^2 z", "1"),
                   ("1", r"\tanh^2 z", "1"),
                   ("1", r"\tanh^2 z", r"\operatorname{sech}^2 z")]
            self.derive_into(c, seq, ["terms", "Shine squared over", "And one over"], [1.4, 1.2, 1.2])

            c.wait_until("res")
            self.slide_into(4, div)

            c.wait_until("divsinh")
            self.pieces = [piece(s, p) for s, p in zip(t0, pos)]
            self.box93 = None
            div2 = MathTex(r"\div\, \sinh^2 z", font_size=36, color=YELLOW).move_to(WS + 0.75 * DOWN)
            self.play(*appear(*self.pieces, lag=0, shift=None), *appear(div2, shift=None), run_time=1.0)

            seq = [(r"\cosh^2 z", r"\sinh^2 z", "1"),
                   (r"\coth^2 z", r"\sinh^2 z", "1"),
                   (r"\coth^2 z", "1", "1"),
                   (r"\coth^2 z", "1", r"\operatorname{cosech}^2 z")]
            self.derive_into(c, seq, ["cotangent", "minus one", "equals hyperbolic cosecant"],
                             [0.8, 0.7, 0.7])
            rem = c.remaining
            self.slide_into(5, div2, rt=max(0.8, min(1.2, 0.6 * rem)), swap_rt=max(0.5, min(0.8, 0.4 * rem)))

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
