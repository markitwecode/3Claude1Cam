"""Chapter 5, scene 5: assemble the recursion H_{n+1} = 2xH_n - 2nH_{n-1}. Clips c5.build.1 – c5.build.4.

Plan: opens on open_shot() (s2's def line at the top, ladder_card(3) at the right, s3's strip and
s4's two-term result under the def line; ch5_s4 lands on it). Work area = the frame left of the
ladder, centred at xc. Rows (top down): def line, F (the result line, where the boxed recursion ends),
D (a definition to match against), W (the term being worked), B (the "and so" line, later the sign
identity).
c1 {back} strip + two-term slide to the centre; {insert} the strip's derivative goes, H_{n+1} and
an empty ( ) appear; the x term, then the n term fly up into it (TransformFromCopy, part by part):
the notes' "and so" line. "In front ... stays": the prefix flashes; it stays centred to the end.
c2 {firstterm} the line drops to row B; first term copied up to W; its x hops (arc) beside the 2; {match} a copy of the def line flies
down to D, aligned factor under factor, pairs flash; {hn} the four factors collapse into H_n;
"So the first term": D goes, 2xH_n rises to row F as "= 2xH_n".
c3 second term copied up to W, its n hops beside the 2; D row: H_{n-1}'s definition; {mismatch}
the two sign powers flash YELLOW; {move} the identity (-1)^n = -(-1)^{n-1} in row B; its YELLOW -
flies to the front of the term; {minus} the factors collapse: -2nH_{n-1}.
c4 {whence} D and B go, the YELLOW - flies into F; {result} 2nH_{n-1} follows, H_{n+1} appears,
the YELLOW box grows with "n >= 1"; {holds} example42_mini() under it, GREEN tick on "claimed";
the card fades, and the scene holds on handover_shot() (def line + boxed recursion + ladder).

Exported: open_shot(), boxed_recursion() = VGroup(eq, box, caption), example42_mini() =
VGroup(border, header, claim), handover_shot().
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# --------------------------------------------------------------------------- sibling helpers
def _sib(stem, name):
    """A helper from a sibling scene file, or None while that file / helper doesn't exist yet."""
    try:
        return getattr(load_scene(stem), name, None)
    except (FileNotFoundError, OSError):
        return None


def _def_line():
    f = _sib("ch5_s2_define", "def_line")
    if f is not None:
        return f()
    m = MathTex(r"H_n(x) \equiv (-1)^n", "e^{x^2}", r"\frac{d^n}{dx^n}\left(", "e^{-x^2}", r"\right)",
                font_size=40, color=FG)
    m[1].set_color(GOLD)
    m[3].set_color(PURPLE)
    return m.to_edge(UP, buff=0.45)


def _ladder(k=3):
    f = _sib("ch5_s2_define", "ladder_card")
    if f is not None:
        return f(k)
    card = RoundedRectangle(corner_radius=0.15, width=2.1, height=5.6).set_stroke(DIM, 2)
    return VGroup(card).move_to(RIGHT * 5.75 + DOWN * 0.4)


# --------------------------------------------------------------------------- equations
X = ("x", BLUE)
EP = ("e^{x^2}", GOLD)
EM = ("e^{-x^2}", PURPLE)
DN = r"\frac{d^n}{dx^n}"
DN1 = r"\frac{d^{n-1}}{dx^{n-1}}"
LP, RP = r"\Big(", r"\Big)"


def M(parts, size=44):
    """MathTex with one part per entry; an entry is a tex string or (tex, colour)."""
    texs = [p if isinstance(p, str) else p[0] for p in parts]
    m = MathTex(*texs, font_size=size, color=FG)
    for i, p in enumerate(parts):
        if not isinstance(p, str):
            m[i].set_color(p[1])
    return m


def _layout():
    defl, lad = _def_line(), _ladder(3)
    xl, xr = -6.6, lad.get_left()[0] - 0.35
    yf = defl.get_bottom()[1] - 0.75
    yd = yf - 1.55
    yw = yd - 1.5
    yb = max(yw - 1.65, -2.85)
    return dict(xc=(xl + xr) / 2, avail=xr - xl, top=defl.get_bottom()[1],
                yf=yf, yd=yd, yw=yw, yb=yb)


def _strip():
    # 0 = | 1 2 | 2 (-1)^n | 3 e^{x^2} | 4 d^n | 5 ( | 6 x | 7 e^{-x^2} | 8 )
    return M(["=", "2", "(-1)^n", EP, DN, LP, X, EM, RP])


def _two_term():
    # 0 = | 1 n | 2 d^{n-1} | 3 e | 4 + | 5 x | 6 d^n | 7 e
    return M(["=", "n", DN1, EM, "+", X, DN, EM])


def _result_eq(minus_color=FG):
    # 0 H_{n+1} | 1 = | 2 2 | 3 x | 4 H_n | 5 - | 6 2 | 7 n | 8 H_{n-1}
    return M(["H_{n+1}", "=", "2", X, "H_n", ("-", minus_color), "2", "n", "H_{n-1}"], 48)


def open_shot():
    """Def line at the top, ladder_card(3) at the right, s3's strip under the def line and s4's
    two-term result under it. VGroup(def_line, ladder, strip, two_term)."""
    L = _layout()
    strip = _strip()
    strip.move_to([L["xc"], L["top"] - 0.85, 0])
    two = _two_term()
    two.next_to(strip, DOWN, buff=0.5).set_x(L["xc"])
    return VGroup(_def_line(), _ladder(3), strip, two)


def boxed_recursion():
    """H_{n+1} = 2xH_n - 2nH_{n-1} (48) in a YELLOW rounded box, caption "n >= 1" right of it, at
    the top-centre of the work area under the def line. VGroup(eq, box, caption)."""
    L = _layout()
    eq = _result_eq()
    eq.move_to([L["xc"], L["yf"], 0])
    box = RoundedRectangle(corner_radius=0.15, width=eq.width + 0.7, height=eq.height + 0.6)
    box.set_stroke(YELLOW, 2.5).set_fill(opacity=0).move_to(eq)
    cap = MathTex(r"n \ge 1", font_size=36, color=FG).next_to(box, RIGHT, buff=0.3)
    return VGroup(eq, box, cap)


def example42_mini():
    """The Example 42 card, small: GREEN border, header, the claim sentence.
    VGroup(border, header, claim); claim = VGroup(line1, VGroup(math, "holds."))."""
    header = T("Example 42: Hermite polynomials", size=32, color=GREEN)
    l1 = T("Show that the recursion relation", size=30)
    math = MathTex(r"H_{n+1} = 2xH_n - 2nH_{n-1}", font_size=36, color=FG)
    holds = T("holds.", size=30)
    l2 = VGroup(math, holds).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
    claim = VGroup(l1, l2).arrange(DOWN, buff=0.22)
    body = VGroup(header, claim).arrange(DOWN, buff=0.32)
    border = RoundedRectangle(corner_radius=0.15, width=body.width + 0.7, height=body.height + 0.6)
    border.set_stroke(GREEN, 3).set_fill(BG, 1).move_to(body)
    border.set_z_index(-1)
    return VGroup(border, header, claim)


def handover_shot():
    """The last frame: def line, ladder_card(3), boxed_recursion()."""
    return VGroup(_def_line(), _ladder(3), boxed_recursion())


def _align(m, part, target_part):
    m.shift(target_part.get_center() - part.get_center())
    return m


# --------------------------------------------------------------------------- scene
class Ch5S5Assemble(NarratedScene):
    def construct(self):
        L = _layout()
        self.L = L
        xc = L["xc"]
        shot = open_shot()
        self.defl, self.lad, strip, two = shot
        self.add(self.defl, self.lad, strip, two)
        self.clip1(strip, two)
        self.clip2()
        self.clip3()
        self.clip4()

    # ----------------------------------------------------------------- c1: the "and so" line
    def clip1(self, S, R):
        L = self.L
        xc = L["xc"]
        with self.say("c5.build.1") as c:
            self.play(S.animate.move_to([xc, 1.0, 0]), R.animate.move_to([xc, -1.5, 0]),
                      run_time=min(1.6, c.until("insert")))
            c.wait_until("insert")
            # 0 H | 1 = | 2 2 | 3 (-1)^n | 4 e^{x^2} | 5 ( | 6 x | 7 d^n | 8 e | 9 + | 10 n | 11 d^{n-1} | 12 e | 13 )
            L1 = M(["H_{n+1}", "=", "2", "(-1)^n", EP, LP, X, DN, EM, "+", "n", DN1, EM, RP], 48)
            if L1.width > L["avail"] - 0.4:
                L1.scale_to_fit_width(L["avail"] - 0.4)
            L1.move_to([xc, 1.0, 0])
            self.play(*during(disappear(*S[4:]), 0, 0.45),
                      *during([Transform(S[i], L1[i + 1]) for i in range(4)], 0.2, 0.8),
                      *during(appear(L1[0], L1[5], L1[13], shift=None, lag=0), 0.5, 1),
                      run_time=1.5)
            self.remove(*S.get_family())
            self.add(*[L1[i] for i in (1, 2, 3, 4)])
            c.wait_until("two surviving")
            self.play(*[a for k, j in ((5, 6), (6, 7), (7, 8)) for a in fly(R[k], L1[j], arc=PI / 5)],
                      *during(disappear(R[0], *R[4:]), 0.75, 1), run_time=1.6)
            c.wait_until("first")
            self.play(*[Transform(R[k], L1[j]) for k, j in ((1, 10), (2, 11), (3, 12))],
                      *during(appear(L1[9], shift=None), 0.85, 1), run_time=1.5)
            self.remove(*L1.get_family(), *R.get_family())
            self.add(L1)
            self.L1 = L1
            c.wait_until("in front")
            self.play(FlashAround(VGroup(L1[2], L1[3], L1[4]), run_time=2, time_width=1.5))
            c.wait_until("stays")

    # ----------------------------------------------------------------- c2: the first term
    def clip2(self):
        L, L1 = self.L, self.L1
        xc = L["xc"]
        with self.say("c5.build.2") as c:
            T1a = M(["2", "(-1)^n", EP, X, DN, EM]).move_to([xc, L["yw"], 0])
            # {firstterm}: the "and so" line leaves the centre for row B, its second term dims
            self.play(L1.animate.scale(40 / 48).move_to([xc, L["yb"], 0]), run_time=1.0)
            self.play(*set_alpha([L1[i] for i in (9, 10, 11, 12)], DIMMED),
                      *[x for a, b in zip((2, 3, 4, 6, 7, 8), range(6)) for x in fly(L1[a], T1a[b])],
                      run_time=1.3)
            c.wait_until("bring")
            T1 = M(["2", X, r"\cdot", "(-1)^n", EP, DN, EM])
            _align(T1, T1[0], T1a[0])
            self.play(Transform(T1a[3], T1[1], path_arc=0.7 * PI),
                      *[Transform(T1a[a], T1[b]) for a, b in ((1, 3), (2, 4), (4, 5), (5, 6))],
                      *during(appear(T1[2], shift=None), 0.6, 1), run_time=1.6)
            self.remove(*T1a.get_family(), T1[2])
            self.add(T1)
            c.wait_until("match")
            D = M(["H_n(x)", r"\equiv", "(-1)^n", EP, DN, LP, EM, RP])
            D.move_to([0, L["yd"], 0])
            D.shift((T1[3].get_x() - D[2].get_x()) * RIGHT)
            self.play(*fly(self.defl, D), run_time=1.5)
            c.wait_until("minus one to the power")
            self.play(*flash([T1[3], D[2]], run_time=1.2))
            c.wait_until("squared")
            self.play(*flash([T1[4], D[3]], run_time=1.2))
            c.wait_until("nth derivative")
            self.play(*flash([VGroup(T1[5], T1[6]), VGroup(*D[4:8])], run_time=1.2))
            c.wait_until("hn")
            R1 = M(["2", X, "H_n"])
            _align(R1, R1[0], T1[0])
            Hn = R1[2]
            self.play(*during(disappear(*T1[2:]), 0, 0.45),
                      *during(appear(Hn, shift=None), 0.5, 1),
                      *during(flash([D[0]]), 0.5, 1), run_time=1.5)
            c.wait_until("so the first term")
            F = _result_eq(minus_color=YELLOW).move_to([xc, L["yf"], 0])
            self.F = F
            self.play(*during(disappear(D), 0, 0.45),
                      *during([Transform(T1[0], F[2]), Transform(T1[1], F[3]), Transform(Hn, F[4])], 0.3, 1),
                      *during(appear(F[1], shift=None), 0.6, 1), run_time=min(1.6, c.until(floor=1.0)))
            self.remove(*T1.get_family(), Hn)
            self.add(F[1], F[2], F[3], F[4])

    # ----------------------------------------------------------------- c3: the second term
    def clip3(self):
        L, L1, F = self.L, self.L1, self.F
        xc = L["xc"]
        with self.say("c5.build.3") as c:
            T2a = M(["2", "(-1)^n", EP, "n", DN1, EM]).move_to([xc + 0.6, L["yw"], 0])
            self.play(*set_alpha([L1[i] for i in (6, 7, 8)], DIMMED),
                      *set_alpha([L1[i] for i in (9, 10, 11, 12)], 1),
                      *[x for a, b in zip((2, 3, 4, 10, 11, 12), range(6)) for x in fly(L1[a], T2a[b])],
                      run_time=1.5)
            c.wait_until("differentiated")
            T2 = M(["2", "n", r"\cdot", "(-1)^n", EP, DN1, EM])
            _align(T2, T2[0], T2a[0])
            self.play(Transform(T2a[3], T2[1], path_arc=0.7 * PI),
                      *[Transform(T2a[a], T2[b]) for a, b in ((1, 3), (2, 4), (4, 5), (5, 6))],
                      *during(appear(T2[2], shift=None), 0.6, 1), run_time=1.4)
            self.remove(*T2a.get_family(), T2[2])
            self.add(T2)
            c.wait_until("should give")
            Dn1 = M(["H_{n-1}", "=", "(-1)^{n-1}", EP, DN1, LP, EM, RP])
            Dn1.move_to([0, L["yd"], 0])
            Dn1.shift((T2[3].get_x() - Dn1[2].get_x()) * RIGHT)
            self.play(*appear(Dn1), *disappear(L1), run_time=1.2)
            c.wait_until("carries")
            self.play(*flash([Dn1[2]], run_time=1.2), *recolor(Dn1[2], YELLOW), run_time=1.2)
            c.wait_until("here we have")
            self.play(*flash([T2[3]], run_time=1.2), *recolor(T2[3], YELLOW), run_time=1.2)
            c.wait_until("move")
            T2b = M([("-", YELLOW), "2", "n", r"\cdot", ("(-1)^{n-1}", YELLOW), EP, DN1, EM])
            _align(T2b, T2b[1], T2[0])
            I = M(["(-1)^n", "=", ("-", YELLOW), "(-1)^{n-1}"]).move_to([0, L["yb"], 0])
            I.shift((T2b[0].get_x() - I[2].get_x()) * RIGHT)   # its minus right under the term's front
            self.play(*appear(I), run_time=1.2)
            c.wait_until("take it out front")
            self.play(*fly(I[2], T2b[0]),
                      *during(disappear(T2[3]), 0, 0.45),
                      *during([Transform(T2[a], T2b[b]) for a, b in ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7))],
                              0, 0.5),
                      *during(appear(T2b[4], shift=None), 0.55, 1),
                      run_time=min(1.5, c.until("minus", floor=1.0)))
            self.remove(*T2.get_family(), T2b[0], T2b[4])
            self.add(T2b)
            c.wait_until("minus")
            R2 = M([("-", YELLOW), "2", "n", "H_{n-1}"])
            _align(R2, R2[0], T2b[0])
            Hn1 = R2[3]
            self.play(*during(disappear(*T2b[3:]), 0, 0.45),
                      *during(appear(Hn1, shift=None), 0.5, 1),
                      *during(flash([Dn1[0]]), 0.5, 1), run_time=1.5)
            self.T2b, self.Hn1, self.Dn1, self.I = T2b, Hn1, Dn1, I

    # ----------------------------------------------------------------- c4: the result
    def clip4(self):
        L, F, T2b, Hn1 = self.L, self.F, self.T2b, self.Hn1
        with self.say("c5.build.4", gap=0.2) as c:
            self.play(*during(disappear(self.Dn1, self.I), 0, 0.45),
                      *during([Transform(T2b[0], F[5], path_arc=-PI / 4)], 0.3, 1), run_time=1.6)
            self.play(FlashAround(F[5], run_time=1.2))
            c.wait_until("result")
            self.play(*[Transform(m, F[k], path_arc=-PI / 4) for m, k in ((T2b[1], 6), (T2b[2], 7), (Hn1, 8))],
                      run_time=1.5)
            self.remove(*T2b.get_family(), Hn1)
            self.add(*F[1:])
            c.wait_until("two ex times")
            self.play(*appear(F[0], shift=None), run_time=1.0)
            self.remove(*F.get_family())
            self.add(F)
            c.wait_until("times h n minus one")
            br = boxed_recursion()
            eq, box, cap = br
            self.play(GrowFromCenter(box), *recolor(F[5], FG),
                      *during(appear(cap, shift=None), 0.4, 1), run_time=1.3)
            c.wait_until("holds")
            card = example42_mini().move_to([L["xc"], (box.get_bottom()[1] - 3.75) / 2, 0])
            self.play(*appear(card, shift=0.2 * DOWN), run_time=1.0)  # early: the card is read whole; its claim is what "holds"
            tick = check_mark(GREEN).next_to(card[2][1], RIGHT, buff=0.3)
            c.wait_until("example claimed")
            self.play(Create(tick), FlashAround(card[2], color=GREEN, run_time=1.2), run_time=1.2)
        self.wait(0.8)
        self.play(*disappear(card, tick), run_time=0.8)
        # land exactly on handover_shot()
        self.remove(*[m for m in self.mobjects])
        hs = handover_shot()
        self.add(*hs)
        self.wait(1.0)
