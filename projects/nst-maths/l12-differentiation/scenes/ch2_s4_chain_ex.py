"""Chapter 2, scene 4: Example 37 (sin x², ln cos x) and a look ahead to the two-route tree. Clips c2.chex.1 – c2.chex.3."""
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

LX = -5.6                      # left edge of the worked rows
ROW_A, ROW_D, ROW_V, ROW_R = 1.9, 0.6, -0.9, -2.5
FS = 54


def M(*s, size=FS, color=FG):
    return MathTex(*s, font_size=size, color=color)


def row_at(mob, y, x=LX):
    mob.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    return mob


def answer_box(m):
    return SurroundingRectangle(m, color=YELLOW, buff=0.2, stroke_width=3)


class ChainExample(NarratedScene):
    def construct(self):
        chain = load_scene("ch2_s3_chain").handover_shot()
        self.add(chain)
        self.chain = chain
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- (a) sin x^2
    def clip1(self):
        with self.say("c2.chex.1") as c:
            title = T("Example 37: Chain rule", 44, t2c={"Example 37": YELLOW})
            title.to_edge(UP, buff=0.5).align_to([-6.4, 0, 0], LEFT)
            tag = T("(a)", 36, DIM)
            line = M("y", "=", r"\sin", "x^2", "=", "f", r"\big(", "g", "(x)", r"\big)", size=56)
            row_at(line, ROW_A)
            tag.next_to(line, LEFT, buff=0.35)
            self.title = title
            self.play(*appear(title), run_time=0.9)  # early: card heading
            self.play(*appear(tag, line, lag=0.2), run_time=1.2)
            c.wait_until("outer")

            defF = M(r"f(g) = \sin g", size=50, color=BLUE)
            defG = M("g(x)", "=", "x^2", size=50, color=PURPLE)
            row_at(defF, ROW_D)
            defG.next_to(defF, RIGHT, buff=1.2)
            defG.align_to(defF, DOWN)
            self.play(*appear(defF), *recolor([line[2], line[5]], BLUE), run_time=1.2)
            c.wait_until("inner function")
            self.play(*appear(defG), *recolor([line[3], line[7], line[8]], PURPLE), run_time=1.2)
            c.wait_until("cos")

            d1 = M(r"\frac{dy}{dx}", "=", r"\frac{df}{dg}", r"\frac{dg}{dx}", "=")
            d1[2].set_color(BLUE)
            d1[3].set_color(PURPLE)
            row_at(d1, ROW_V)
            cosg = M(r"(\cos g)", color=BLUE).next_to(d1, RIGHT, buff=0.2)
            twox = M("(2x)", color=PURPLE).next_to(cosg, RIGHT, buff=0.1)
            self.play(*appear(d1), run_time=1.1)
            self.play(*appear(cosg), run_time=1.0)
            c.wait_until("two ex")
            self.play(*appear(twox), run_time=1.0)
            c.wait_until("back")

            eq = M("=").move_to([d1[4].get_x(), ROW_R, 0])
            ans = M("2x", r"\cos", "x^2")
            ans[0].set_color(PURPLE)
            ans[1].set_color(BLUE)
            ans[2].set_color(PURPLE)
            ans.next_to(eq, RIGHT, buff=0.25)
            self.play(*appear(eq, ans[0], ans[1], shift=None, lag=0.15),
                      FlashAround(cosg[0][4], color=PURPLE, run_time=1.6, time_width=1.5),
                      *fly(defG[2], ans[2], arc=3.0), run_time=1.6)
            box = answer_box(ans)
            c.wait_until("the answer")
            self.play(FadeIn(box), run_time=0.8)
            grpA = VGroup(ans, box)
            settle(self, grpA)
            self.grpA = grpA
            self.workA = [tag, line, defF, defG, d1, cosg, twox, eq]

    # ---------------------------------------------------------------- (b) ln cos x
    def clip2(self):
        with self.say("c2.chex.2") as c:
            tag = T("(b)", 36, DIM)
            line = M("z", "=", r"\ln", r"(\cos x)", "=", "u", r"\big(", "v", "(x)", r"\big)", size=56)
            row_at(line, ROW_A)
            tag.next_to(line, LEFT, buff=0.35)
            self.play(*during(disappear(*self.workA), 0, 0.5),
                      *during([self.grpA.animate.scale(0.6).move_to([5.6, -3.2, 0])], 0.3, 1.0),
                      run_time=1.3)
            self.play(*appear(tag, line, lag=0.2), run_time=1.2)
            c.wait_until("outerlog")

            defU = M(r"u = \ln v", size=50, color=BLUE)
            defV = M(r"v = \cos x", size=50, color=PURPLE)
            row_at(defU, ROW_D)
            defV.next_to(defU, RIGHT, buff=1.2).align_to(defU, DOWN)
            self.play(*appear(defU), *recolor([line[2], line[5]], BLUE),
                      *recolor([line[3], line[7], line[8]], PURPLE), run_time=1.2)
            c.wait_until("its derivative")
            d1 = M(r"\frac{dz}{dx}", "=", r"\frac{du}{dv}", r"\frac{dv}{dx}", "=")
            d1[2].set_color(BLUE)
            d1[3].set_color(PURPLE)
            row_at(d1, ROW_V)
            inv = M(r"\left(\frac{1}{v}\right)", color=BLUE).next_to(d1, RIGHT, buff=0.2)
            msin = M(r"(-\sin x)", color=PURPLE).next_to(inv, RIGHT, buff=0.1)
            self.play(*appear(d1, inv, lag=0.35), run_time=1.4)
            c.wait_until("innercos")
            self.play(*appear(defV), run_time=1.0)
            c.wait_until("minus sine of")
            self.play(*appear(msin), run_time=1.0)
            c.wait_until("tan")

            eq = M("=").move_to([d1[4].get_x(), ROW_R, 0])
            ans = M(r"-\frac{\sin x}{\cos x}", "=", r"-\tan x")
            ans.next_to(eq, RIGHT, buff=0.25)
            self.play(*appear(eq, ans[0], shift=None, lag=0.15), run_time=1.2)
            c.wait_until("minus the tangent")
            self.play(*appear(ans[1], ans[2], shift=None, lag=0.2), run_time=1.2)
            box = answer_box(ans)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("caveat")

            # graph of cos x on the right
            ax = Axes(x_range=[-2 * PI, 2 * PI, PI], y_range=[-1.2, 1.2, 1], x_length=4.8, y_length=1.8,
                      tips=False, axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
            ax.move_to([4.4, 0.15, 0])
            curve = ax.plot(np.cos, x_range=[-2 * PI, 2 * PI], color=FG, stroke_width=3)
            clab = M(r"\cos x", size=34, color=DIM).next_to(ax.c2p(0, 1), UP, buff=0.15)
            goods = [(-2 * PI, -1.5 * PI), (-0.5 * PI, 0.5 * PI), (1.5 * PI, 2 * PI)]
            bads = [(-1.5 * PI, -0.5 * PI), (0.5 * PI, 1.5 * PI)]
            seg = lambda a, b, col: Line(ax.c2p(a, 0), ax.c2p(b, 0), color=col, stroke_width=8)
            green = [seg(a, b, GREEN) for a, b in goods]
            red = [seg(a, b, RED) for a, b in bads]
            undef = T("ln undefined", 30, RED).next_to(ax.c2p(PI, 0), DOWN, buff=1.0)
            cpos = M(r"\cos x > 0", size=40, color=GREEN).next_to(box, RIGHT, buff=0.35)
            self.play(Create(ax), Create(curve), *appear(clab), run_time=1.4)
            c.wait_until("positive")
            self.play(*[Create(s) for s in green], *appear(cpos), run_time=1.2)
            c.wait_until("undefined")
            self.play(*[Create(s) for s in red], *appear(undef), run_time=1.1)

            grpB = VGroup(ans, box, cpos)
            settle(self, grpB)
            self.grpB = grpB
            self.workB = [self.title, tag, line, defU, defV, d1, inv, msin, eq, ax, curve, clab,
                          *green, *red, undef]

    # ---------------------------------------------------------------- the tree, a look ahead
    def clip3(self):
        with self.say("c2.chex.3") as c:
            c.wait_until("again")
            self.play(*during(disappear(*self.workB), 0, 0.5),
                      *during([self.grpA.animate.scale(1.25).move_to([-4.8, 3.05, 0])], 0.62, 1.0),
                      *during([self.grpB.animate.scale(0.75).move_to([-0.1, 3.05, 0])], 0.3, 0.65),
                      run_time=2.2)
            c.wait_until("grow")
            self.play(*disappear(self.grpA, self.grpB), run_time=1.0)
            self.play(FlashAround(self.chain[0].rect, run_time=1.6, time_width=1.5))
            c.wait_until("tree")

            P = {"h": (-3.6, 2.5), "u": (-5.6, 0.2), "v": (-1.6, 0.2), "x": (-5.6, -2.2), "y": (-1.6, -2.2)}
            cols = {"h": BLUE, "u": PURPLE, "v": PURPLE, "x": FG, "y": FG}
            nodes = {k: M(k, size=56, color=cols[k]).move_to([*P[k], 0]) for k in P}

            def edge(a, b):
                pa, pb = np.array([*P[a], 0]), np.array([*P[b], 0])
                d = (pb - pa) / np.linalg.norm(pb - pa)
                return Line(pa + 0.38 * d, pb - 0.38 * d, color=DIM, stroke_width=3)

            def plabel(top, bot, pos):
                return M(r"\frac{\partial %s}{\partial %s}" % (top, bot), size=36).move_to([*pos, 0])

            E = {k: edge(k[0], k[1]) for k in ("hu", "hv", "ux", "uy", "vx", "vy")}
            L = {"hu": plabel("h", "u", (-5.15, 1.5)), "hv": plabel("h", "v", (-2.05, 1.5)),
                 "ux": plabel("u", "x", (-6.2, -1.0)), "vy": plabel("v", "y", (-1.0, -1.0)),
                 "uy": plabel("u", "y", (-4.37, -0.01)), "vx": plabel("v", "x", (-2.83, -0.01))}
            self.play(Succession(
                FadeIn(nodes["h"], run_time=0.5),
                AnimationGroup(Create(E["hu"]), Create(E["hv"]), run_time=0.6),
                AnimationGroup(FadeIn(nodes["u"]), FadeIn(nodes["v"]), FadeIn(L["hu"]), FadeIn(L["hv"]),
                               run_time=0.6),
                AnimationGroup(*[Create(E[k]) for k in ("ux", "uy", "vx", "vy")], run_time=0.8),
                AnimationGroup(FadeIn(nodes["x"]), FadeIn(nodes["y"]),
                               *[FadeIn(L[k]) for k in ("ux", "uy", "vx", "vy")], run_time=0.7)),
                run_time=3.2)
            c.wait_until("routes")

            def route_path(mid):
                return VMobject().set_points_as_corners(
                    [np.array([*P["x"], 0]), np.array([*P[mid], 0]), np.array([*P["h"], 0])]
                ).set_stroke(YELLOW, 7)

            def light(mid, col):
                ks = (mid + "x" if mid == "u" else "vx", "h" + mid)
                return [*recolor([E[k] for k in ks], col), *recolor([L[k] for k in ks], col if col != DIM else FG)]

            self.play(VShowPassingFlash(route_path("u"), time_width=0.6), *light("u", YELLOW), run_time=1.6)
            c.wait_until("through each")
            self.play(VShowPassingFlash(route_path("v"), time_width=0.6), *light("v", YELLOW),
                      *light("u", DIM), run_time=1.6)
            c.wait_until("terms")

            f = M(r"\frac{\partial h}{\partial x}", "=", r"\frac{\partial h}{\partial u}",
                  r"\frac{\partial u}{\partial x}", "+", r"\frac{\partial h}{\partial v}",
                  r"\frac{\partial v}{\partial x}", size=56)
            f.move_to([3.2, 0.0, 0])
            note = T("Chapter 7 of the notes · next term", 30, DIM).next_to(f, DOWN, buff=0.6)
            self.play(*appear(f[0], f[1], f[2], f[3], lag=0.15), *light("u", YELLOW), *light("v", DIM),
                      run_time=1.4)
            c.wait_until("two terms add")
            self.play(*appear(f[4], f[5], f[6], lag=0.15), *light("v", YELLOW), run_time=1.2)
            self.play(*appear(note), run_time=0.8)
            c.wait_until("curly")
            parts = [f[i] for i in (0, 2, 3, 5, 6)]
            ds = [p[j] for p in parts for j in (0, 3)]
            self.play(LaggedStart(*[FlashAround(d, run_time=1.2, time_width=1.5, buff=0.06) for d in ds],
                                  lag_ratio=0.12), run_time=2.0)
