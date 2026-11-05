"""Chapter 4, scene 7: recap in five panels, then ch5's opening card. Clips c4.recap.1 – c4.recap.2.

Layout: five DIM frames (3 on top, 2 below) appear on {recap}; each fills on its sentence with a
shrunken copy of the visual that taught it (helpers loaded from s2-s6), its line underneath.
{next}: the panels sweep out while ch5's open_card() is built piece by piece; the last ~8 s hold
exactly load_scene("ch5_s1_hook").open_card() (reversed join; chapter end, no handover mark).
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

# ── grid: three frames on top, two below ──────────────────────────────────────────
TOP_C, TOP_W, TOP_H = [np.array([x, 2.3, 0]) for x in (-4.45, 0.0, 4.45)], 4.2, 2.4
BOT_C, BOT_W, BOT_H = [np.array([x, -1.3, 0]) for x in (-3.15, 3.15)], 5.8, 2.2
CENTRES = TOP_C + BOT_C
SIZES = [(TOP_W, TOP_H)] * 3 + [(BOT_W, BOT_H)] * 2
LINES = ["no arrowheads,\nstar four", "every step\nflips the side", "multiply along,\nadd across",
         "paths explode,\npeople level off", "one join per edge,\nno edge twice"]
CAP = 30


def frame(i):
    w, h = SIZES[i]
    return RoundedRectangle(corner_radius=0.2, width=w, height=h).set_stroke(DIM, 2, opacity=0.6) \
        .move_to(CENTRES[i])


def caption(i, fr):
    t2c = {"paths": GOLD, "people": PINK} if i == 3 else {}
    return T(LINES[i], CAP, FG, line_spacing=0.8, t2c=t2c).next_to(fr, DOWN, buff=0.15)


def fit(mob, w, h, centre):
    s = min(w / mob.width, h / mob.height)
    mob.scale(s).move_to(centre)
    return s


class Recap(NarratedScene):
    def construct(self):
        s2 = load_scene("ch4_s2_chains")
        s3 = load_scene("ch4_s3_even")
        s4 = load_scene("ch4_s4_count8")
        s5 = load_scene("ch4_s5_explode")
        s6 = load_scene("ch4_s6_joins")
        frames = [frame(i) for i in range(5)]
        caps = [caption(i, f) for i, f in enumerate(frames)]

        with self.say("c4.recap.1") as c:
            # {recap}: the whole shape first, five empty frames
            self.play(*appear(*frames, shift=None, lag=0.15), run_time=min(1.2, c.until("r1")))
            c.wait_until("r1")

            # {r1}: the chain, its arrowheads fade, *4 under it
            full = s2.chain_example(arrows=True)
            plain = s2.chain_example(arrows=False)
            chain = VGroup(*full.nodes, *full.edges)
            sc = min(3.8 / chain.width, 1.0)
            shift = CENTRES[0] + 0.4 * UP
            for g in (VGroup(*full.nodes, *full.edges), VGroup(*plain.edges)):
                g.scale(sc, about_point=ORIGIN).shift(shift)
            for e in plain.edges:
                e.set_stroke(width=3)
            for e in full.edges:
                e.set_stroke(width=3)
            self.play(*appear(*full.nodes, *full.edges, shift=None, lag=0.05),
                      run_time=min(1.2, c.until("drop the arrowheads")))
            c.wait_until("drop the arrowheads")
            self.play(*[FadeOut(a) for a in full.edges], *[FadeIn(l) for l in plain.edges],
                      run_time=min(1.5, c.until("star four")))
            c.wait_until("star four")
            star = Mono("-[:ACTED_IN*4]-", 28, FG, t2c={"*4": YELLOW}).move_to(CENTRES[0] + 0.55 * DOWN)
            self.play(*appear(star), run_time=min(1.0, c.until("in a row")))
            c.wait_until("four edges")
            self.play(*appear(caps[0]), run_time=min(1.0, c.until("r2")))
            c.wait_until("r2")

            # {r2}: two banks, the token's zigzag
            bk = s3.banks(walk=True)
            ymid = (s3.ROW_Y[0] + s3.ROW_Y[-1]) / 2
            rects = [RoundedRectangle(corner_radius=0.3, width=1.2, height=4.6).set_stroke(col, 3)
                     .set_fill(col, 0.12).move_to([x, ymid, 0])
                     for x, col in ((-s3.DOT_X, PINK), (s3.DOT_X, BLUE))]
            bk.token.move_to(bk.pdots[0])
            banks = VGroup(*rects, *bk.lines, *bk.pdots, *bk.mdots, bk.token)
            fit(banks, 3.8, 2.15, CENTRES[1])
            walk_pts = [bk.pdots[0], bk.mdots[0], bk.pdots[1], bk.mdots[1], bk.pdots[2]]
            self.play(*appear(*rects, *bk.lines, *bk.pdots, *bk.mdots, bk.token, shift=None, lag=0.02),
                      run_time=min(1.2, c.until("so paths")))
            c.wait_until("so paths")
            path = VMobject().set_points_as_corners([d.get_center() for d in walk_pts])
            self.play(MoveAlongPath(bk.token, path), rate_func=linear,
                      run_time=min(2.0, c.until("even length")))
            c.wait_until("even length")
            self.play(*appear(caps[1]), run_time=min(1.0, c.until("r3")))
            c.wait_until("r3")

            # {r3}: the layered drawing, 3 x 1 + 4 x 1 + 1 x 1 = 8
            lp = s4.layered_paths()
            draw = VGroup(*lp.edges.values(), *lp.shapes.values())
            fit(draw, 3.8, 1.6, CENTRES[2] + 0.3 * UP)
            for e in lp.edges.values():
                e.set_stroke(width=2)
            for k, sh in lp.shapes.items():
                sh.set_stroke(width=2)
            self.play(*appear(*draw, shift=None, lag=0.0), run_time=min(1.0, c.until("multiply")))
            c.wait_until(own_word=caps[2])
            self.play(*appear(caps[2]), run_time=min(1.0, c.until("three")))
            eq = MathTex(r"3 \times 1", r"+ 4 \times 1", r"+ 1 \times 1", r"= 8", font_size=32, color=GOLD)
            eq.move_to(CENTRES[2] + 0.82 * DOWN)
            for piece, cue, m in zip(eq, ["three", "plus four", "plus one", "makes eight"], ["H", "M", "G", None]):
                c.wait_until(cue)
                anims = appear(piece, shift=None)
                if m is not None:
                    anims += recolor([lp.edges[k] for k in lp.group_keys[m][1]], GOLD)
                self.play(*anims, run_time=min(0.8, c.until("r4") if m is None else 0.8))
            settle(self, eq)
            c.wait_until("r4")

            # {r4}: the log plot, GOLD paths rising, PINK people flat under the ceiling
            pp = s5.paths_plot()
            gl = T("paths", 30, GOLD)
            pl = T("people", 30, PINK)
            plot = VGroup(pp.axes, pp.ceiling, pp.gold_curve, pp.gold_dots, pp.pink_curve, pp.pink_dots)
            sp = fit(plot, 5.4, 1.9, ORIGIN)
            for e in (pp.gold_curve, pp.pink_curve):
                e.set_stroke(width=3)
            for d in [*pp.gold_dots, *pp.pink_dots]:
                d.scale(1.6)
            gl.next_to(pp.gold_dots[-1], RIGHT, buff=0.15)
            pl.next_to(pp.pink_dots[-1], RIGHT, buff=0.15).shift(0.1 * DOWN)
            VGroup(plot, gl, pl).move_to(CENTRES[3])
            self.play(*appear(pp.axes, pp.ceiling, shift=None, lag=0.1), run_time=min(0.8, c.until("explode")))
            c.wait_until("explode")
            self.play(Create(pp.gold_curve), *appear(*pp.gold_dots, gl, shift=None, lag=0.1),
                      run_time=min(1.2, c.until("people")))
            c.wait_until("people")
            self.play(Create(pp.pink_curve), *appear(*pp.pink_dots, pl, caps[3], shift=None, lag=0.1),
                      run_time=min(1.2, 0.9 * c.until("r5")))
            c.wait_until("r5")

            # {r5}: the SQL block, a JOIN per edge, the RED 1085
            sb = s6.sql_block()     # s6's reply (RED 1085); the code is a readable excerpt of its JOINs
            code = Code("JOIN has_position AS h1\n⋮\nJOIN has_position AS h6", size=20, lang="sql")
            rep = sb.reply
            rep.rule.stretch_to_fit_width(1.1)
            rep.next_to(code, RIGHT, buff=0.4)
            VGroup(code, rep).move_to(CENTRES[4])
            self.play(*appear(code, rep, shift=None, lag=0.2), run_time=min(1.2, c.until("join")))
            c.wait_until("join")
            joins = [g for k in range(2) for g in code.find("JOIN", nth=k)]
            self.play(*recolor(joins, YELLOW), *appear(caps[4]), run_time=min(1.2, c.until("rule out")))
            c.wait_until("twice")
            self.play(FlashAround(sb.val, color=RED, time_width=1.5), run_time=min(1.5, c.until()))

        with self.say("c4.recap.2") as c:
            card = load_scene("ch5_s1_hook").open_card()
            tangle, law, rad, yellow, q, total = card
            # {next}: the panels sweep out, ch4 s5's 503 arrives on "five hundred"
            sweep_clear(self, time_span(FadeIn(total, shift=0.2 * DOWN), 0.6, 1.2), run_time=1.2)
            c.wait_until("between lawrence")
            self.play(FadeIn(tangle), *appear(law, rad, lag=0.3), run_time=min(1.5, c.until("we usually")))
            c.wait_until("just one")
            pick = tangle[0][0].copy()
            self.play(ReplacementTransform(pick, yellow), run_time=min(1.5, c.until("the shortest") + 0.6))
            c.wait_until("without listing")
            self.play(*appear(q), run_time=min(1.0, c.until()))

        # end card: exactly ch5's opening card, held ~8 s while the music carries it
        self.remove(*self.mobjects)
        self.add(card)
        self.wait(8.0)
