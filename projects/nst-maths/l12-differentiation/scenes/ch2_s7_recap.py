"""Chapter 2, scene 7: recap, the examples sheet, next time, end card. Clips c2.recap.1 – c2.recap.3.

As ch1 s7: a small "Recap" heading, then four panels, one per sentence, each shown big at the centre
with its line under it, then shrunk into a dim strip of four along the top as the next one arrives:
s2's table + the GOLD e^{iax} line, s3's two-bracket line (TEAL δu) over the boxed (105), s5's framed
numerator over the two-strip rectangle, s6's u × (1/v) line over the boxed (107). On {sheet} the last
panel joins the strip and sheet_card() arrives (frame, label, header); its rows come in on {h1},
{h2}, {omega}. On {next} the strip and card clear into part three's circle (ch3 s3's
circle_figure), the dashed x = 2.8, then the two YELLOW points and their GREEN tangents on {circle}.
After the last word the board clears into ch3's open_card(), held ~8 s, then fades.

Export:
    sheet_card() -> load_scene("ch3_s7_recap").question_card("H1 · H2", lines, width=12.4, colors=…,
    size=48), excerpts of Examples Sheet I:
        "Examples Sheet I · answers on p. 15"
        ["H1  (e) d/dt(at + bt^2 sin θ)", "(g) d/dy 1/(1+y)"]
        ["H2  write in exponentials:", "(a) d/dx sin x  (e) d/dx sinh x  (g) d/dx tanh x",
         "(d) d/dω sin(−iωt)"]
    t of d/dt and y of d/dy YELLOW, ω YELLOW, i PINK. Parts .frame .label .body, plus .head, .h1
    (rows), .h2 (rows), .page ("p. 15"), .t .y .theta .omega (list) .i.
"""
# style: 2
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

HERO = np.array((0.0, -0.3, 0.0))
HERO_W, HERO_H = 12.4, 4.3
CAP_Y = -3.05
STRIP = [np.array((x, 2.9, 0)) for x in (-5.1, -1.7, 1.7, 5.1)]
STRIP_W, STRIP_H = 2.9, 1.05
CARD_TOP = 2.1


def parts_by_tex(m, key):
    return [m.id_to_vgroup_dict[i] for s, i in m.matched_strings_and_ids if s == key]


def sheet_card():
    """Examples Sheet I, H1 and H2 excerpts in the series' question-card style (see docstring)."""
    qc = load_scene("ch3_s7_recap").question_card
    g = qc("H1 · H2", [
        r"Examples Sheet I $\cdot$ answers on p.\ 15",
        [r"H1\ \ (e)\ \ $\frac{d}{dt}\left(at + bt^2\sin\theta\right)$",
         r"(g)\ \ $\frac{d}{dy}\,\frac{1}{1+y }$"],
        [r"H2\ \ write in exponentials:",
         r"(a)\ \ $\frac{d}{dx}\sin x$ \quad (e)\ \ $\frac{d}{dx}\sinh x$ \quad (g)\ \ $\frac{d}{dx}\tanh x$",
         r"(d)\ \ $\frac{d}{d\omega}\sin(-{i}\omega t)$"],
    ], width=12.4, size=48, indent=0.0,
        colors={"t}": YELLOW, "y}": YELLOW, r"\omega": YELLOW, "{i}": PINK, r"\theta": FG,
                r"p.\ 15": FG})
    g.head, g.h1, g.h2 = g.body[0], g.body[1], g.body[2]
    # (g) under (e); the H2 rows under the header, indented
    e_open = g.h1[0].family_members_with_points()[2]
    g.h1[1].shift((e_open.get_left()[0] - g.h1[1].get_left()[0]) * RIGHT)
    for r in g.h2[1:]:
        r.shift(0.6 * RIGHT)
    g.page = parts_by_tex(g.head, r"p.\ 15")[0]
    g.t = parts_by_tex(g.h1[0], "t}")[0]
    g.theta = parts_by_tex(g.h1[0], r"\theta")[0]
    g.y = parts_by_tex(g.h1[1], "y}")[0]
    g.omega = parts_by_tex(g.h2[2], r"\omega")
    g.i = parts_by_tex(g.h2[2], "{i}")[0]
    # the omega after i is not isolated by the colour map: colour that glyph directly
    ix = g.i.get_right()[0]
    w2 = min((m for m in g.h2[2].family_members_with_points() if m.get_center()[0] > ix + 0.01),
             key=lambda m: m.get_center()[0]).set_color(YELLOW)
    g.omega = [g.omega[0], w2]
    return g


def fit(m, w, h, pos):
    m.scale(min(w / m.width, h / m.height)).move_to(pos)
    return m


def caption(*pieces):
    g = VGroup(*[T(p, 32) if isinstance(p, str) else p for p in pieces]).arrange(RIGHT, buff=0.16)
    return g.move_to([0, CAP_Y, 0])


def shrink(m, i, op=0.5):
    t = restyle(m, op).target_mobject
    fit(t, STRIP_W, STRIP_H, STRIP[i])
    return Transform(m, t)


def handoff(old, old_cap, i, new, new_cap):
    """Old caption out, old panel into strip slot i, the new panel and caption in."""
    return [*during(disappear(*old_cap), 0, 0.35), *during([shrink(old, i)], 0.05, 0.5),
            *during(appear(new, new_cap, lag=0.2), 0.55, 1.0)]


class Recap(NarratedScene):
    def handoff2(self, c, old, old_cap, i, new, new_cap, cue):
        """Two steps, so the big panel never sweeps over the strip: shrink in place (caption out),
        then glide into slot i while the new panel and caption arrive."""
        small = restyle(old, 0.5).target_mobject
        fit(small, STRIP_W, STRIP_H, old.get_center())
        self.play(*during(disappear(*old_cap), 0, 0.5), Transform(old, small), run_time=0.8)
        self.play(*during([old.animate.move_to(STRIP[i])], 0, 0.45),
                  *during(appear(new, new_cap, lag=0.2), 0.45, 1.0), run_time=min(1.6, c.until(cue)))

    def construct(self):
        s2 = load_scene("ch2_s2_table")
        s3 = load_scene("ch2_s3_chain")
        s5 = load_scene("ch2_s5_product")
        s6 = load_scene("ch2_s6_quotient")

        head = T("Recap", 44).move_to([0, 3.0, 0])

        # panel 1: the table, the e^{iax} line beside it
        table = fit(s2.table_card(), 6.4, 4.7, [-3.1, -0.3, 0])
        euler = s2.euler_line()
        euler.scale_to_fit_width(5.6).move_to([3.6, -0.3, 0])
        cap1 = caption("basic derivatives; the rest from", MathTex("e^{ax}", font_size=40, color=GOLD))

        # panel 2: the two-bracket line over the boxed (105)
        bl = s3.bracket_line()
        cb = s3.chain_box()
        p2 = fit(VGroup(bl, cb).arrange(DOWN, buff=0.55), HERO_W, HERO_H, HERO)
        cap2 = caption("chain rule:  × and ÷ by", MathTex(r"\delta u", font_size=40, color=TEAL))

        # panel 3: the framed numerator over the two-strip rectangle
        num = s5.framed_numerator()
        pic = s5.strips_picture()
        num.scale_to_fit_width(HERO_W)
        pic.scale_to_fit_height(HERO_H + 0.3 - num.height - 0.4)
        p3 = VGroup(num, pic).arrange(DOWN, buff=0.4).move_to(HERO + 0.15 * UP)
        frame3 = num[1]
        strips = [pic[12], pic[13]]
        cap3 = caption("product rule: subtract, add back")

        # panel 4: u × (1/v) over the boxed (107)
        sl = s6.split_line()
        qb = s6.quotient_box()
        p4 = fit(VGroup(sl, qb).arrange(DOWN, buff=0.55), HERO_W, HERO_H, HERO)
        uv = MathTex("u", r"\times", "1/v", font_size=40)
        uv[0].set_color(BLUE)
        uv[2][1].set_color(PURPLE)
        cap4 = caption("quotient rule:", uv)

        # ---------------- c1: the four rules
        with self.say("c2.recap.1") as c:
            self.play(*appear(head), run_time=1.0)
            c.wait_until("r1")
            self.play(*appear(table, cap1, lag=0.4), run_time=min(1.5, c.until("exponential")))  # early: the table thumbnail shown whole
            c.wait_until("exponential")
            self.play(*appear(euler), FlashAround(euler[0], color=GOLD, time_width=1.5),
                      run_time=min(1.5, c.until("r2")))
            p1 = VGroup(table, euler)
            self.remove(table, euler)
            self.add(p1)
            c.wait_until("r2")
            self.play(*during(disappear(head), 0, 0.4), *handoff(p1, [cap1], 0, p2, cap2),
                      run_time=min(2.0, c.until("multiply")))
            c.wait_until("multiply")
            self.play(FlashAround(bl.du, color=TEAL, time_width=1.5),
                      FlashAround(bl.c2, color=TEAL, time_width=1.5), run_time=1.5)
            c.wait_until("inner function")
            self.play(FlashAround(cb.rect, color=YELLOW, time_width=1.5), run_time=min(1.5, c.until("r3")))
            c.wait_until("r3")
            self.handoff2(c, p2, [cap2], 1, p3, cap3, "subtract")
            c.wait_until("subtract")
            self.play(FlashAround(frame3, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("add it back")
            self.play(*[FlashAround(s, color=TEAL, time_width=1.5) for s in strips],
                      run_time=min(1.5, c.until("r4")))
            c.wait_until("r4")
            self.handoff2(c, p3, [cap3], 2, p4, cap4, "write the top")
            c.wait_until("one over")
            self.play(FlashAround(sl.parts[4], color=YELLOW, time_width=1.5),
                      run_time=min(1.5, c.until(floor=0.8)))

        # ---------------- c2: the examples sheet
        card = sheet_card()
        card.move_to([0, CARD_TOP - card.height / 2, 0])
        theta_tag = T("constant", 30, YELLOW)
        theta_tag.next_to(card.h1[0], RIGHT, buff=0.7).shift(0.45 * DOWN)
        theta_arrow = CurvedArrow(theta_tag.get_left() + 0.1 * LEFT, card.theta.get_bottom() + 0.08 * DOWN,
                                  angle=-PI / 3, color=YELLOW, stroke_width=3, tip_length=0.18)
        with self.say("c2.recap.2") as c:
            # shrink in place first, then into the slot, so the big panel never sweeps over slot 2
            small = restyle(p4, 0.5).target_mobject
            fit(small, STRIP_W, STRIP_H, p4.get_center())
            self.play(*during(disappear(cap4), 0, 0.5), Transform(p4, small), run_time=0.8)
            self.play(p4.animate.move_to(STRIP[3]),
                      *during(appear(card.frame, card.label, card.head, lag=0.2), 0.4, 1.0),
                      run_time=min(1.4, c.until("answers")))
            c.wait_until("last page")
            self.play(FlashUnder(card.page, color=YELLOW, time_width=1.5), run_time=min(1.5, c.until("h1")))
            c.wait_until("h1")
            self.play(*appear(*card.h1, lag=0.4), run_time=min(1.4, c.until("tee")))
            c.wait_until("tee")
            self.play(FlashAround(card.t, color=YELLOW, time_width=1.5), run_time=0.9)
            c.wait_until("or why")
            self.play(FlashAround(card.y, color=YELLOW, time_width=1.5), run_time=0.9)
            c.wait_until("constants")
            self.play(Create(theta_arrow),
                      *during(appear(theta_tag, shift=None), 0.4, 1.0), run_time=min(1.2, c.until("h2")))
            c.wait_until("h2")
            self.play(*appear(card.h2[0], card.h2[1], lag=0.4), run_time=min(1.5, c.until("omega")))
            c.wait_until("omega")
            self.play(*appear(card.h2[2]), run_time=1.0)
            self.play(*[FlashAround(o, color=YELLOW, time_width=1.5) for o in card.omega],
                      run_time=min(1.5, c.until(floor=0.8)))

        # ---------------- c3: next time, the circle
        cs = load_scene("ch3_s3_circle")
        fig = cs.circle_figure(ticks=False, dashed=True, points=True, tangents=True)
        extras = [fig.dashed, fig.p_top, fig.p_bot, fig.t_top, fig.t_bot]
        fig.remove(*extras)
        eq = MathTex("y^2 = 9 - (x - 1)^2", font_size=52, color=FG).move_to([3.6, 0.6, 0])
        nxt = T("Next time", 44).move_to([3.6, 2.2, 0])
        with self.say("c2.recap.3") as c:
            sweep_clear(self, time_span(FadeIn(nxt, shift=0.25 * DOWN), 0.7, 1.4),
                        time_span(FadeIn(fig), 0.8, 1.6), run_time=1.6)
            c.wait_until("equations")
            self.play(*appear(eq), run_time=1.0)
            c.wait_until("formula in ex")
            self.play(Create(fig.dashed), run_time=min(1.2, c.until("circle")))
            c.wait_until("two values")
            self.play(*[GrowFromCenter(p) for p in (fig.p_top, fig.p_bot)],
                      FlashAround(fig.p_top, color=YELLOW, buff=0.12), FlashAround(fig.p_bot, color=YELLOW, buff=0.12),
                      run_time=1.0)
            c.wait_until("two tangent")
            self.play(Create(fig.t_top), Create(fig.t_bot), run_time=min(1.5, c.until(floor=1.0)))

        card3 = load_scene("ch3_s1_hook").open_card()
        sweep_clear(self, time_span(FadeIn(card3), 0.6, 1.4), run_time=1.4)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
