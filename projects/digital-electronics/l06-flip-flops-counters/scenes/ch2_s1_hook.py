"""Chapter 2, scene 1: hook -- the latch listens for a window; we want an instant. Clips c2.hook.1 – c2.hook.2."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

# ---- latch symbol (box centred at ORIGIN, then shifted) ----
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6          # D and Q pins sit 0.6 above the box centre
WIRE = 0.85          # D / Q wire length
EN_WIRE = 1.0        # EN wire length below the box
LATCH_C = np.array([-5.0, 0.2, 0])


def make_latch(center=ORIGIN):
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(box.get_bottom())
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    en_w = Line([0, -BOX_H / 2 - EN_WIRE, 0], [0, -BOX_H / 2 - 0.1, 0]).set_stroke(BLUE, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    en_l = T("EN", 30, BLUE).move_to([0, -BOX_H / 2 + 0.42, 0])
    g = VGroup(d_w, q_w, en_w, box, sq, d_l, q_l, en_l)
    g.box, g.en_wire = box, en_w
    g.shift(center)
    return g


# ---- timing diagrams ----
X0, X1 = -2.0, 6.0
H = 0.7


def X(u):
    return X0 + u * (X1 - X0)


def wave(edges, start, y0, color, h=H, width=4):
    level = start
    pts = [[X0, y0 + level * h, 0]]
    for u in edges:
        pts += [[X(u), y0 + level * h, 0], [X(u), y0 + (1 - level) * h, 0]]
        level = 1 - level
    pts.append([X1, y0 + level * h, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


EN_Y, D_Y, Q_Y = 1.3, -0.2, -1.7
BAND = (0.30, 0.68)
D_EDGES = [0.10, 0.20, 0.38, 0.48, 0.58, 0.78, 0.88]
Q_EDGES = [0.30, 0.38, 0.48, 0.58]

CLK_H = 0.8
TOP_Y, BOT_Y = 1.4, -1.5
RISES = [k * 0.25 + 0.0625 for k in range(4)]
FALLS = [k * 0.25 + 0.1875 for k in range(4)]
CLK_EDGES = sorted(RISES + FALLS)


class Hook(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------------ clip 1
        # silent lead-in: the title card is up ~3 s before the first word (music bed carries it)
        card = title_card("Part 2 · The master-slave D flip-flop")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(FadeIn(card.course), run_time=0.6)  # early: title card
        self.play(FadeIn(card.part), run_time=0.6)  # early: title card
        self.wait(2.0)
        with self.say("c2.hook.1") as c:
            c.wait_until("latch")

            latch = make_latch(LATCH_C)
            sweep_clear(self, *appear(latch, shift=None), run_time=min(1.6, c.until("enable input")))  # early: the symbol is named piece by piece

            # EN / D / Q timing diagram
            en_wave = wave([BAND[0], BAND[1]], 0, EN_Y, BLUE)
            d_wave = wave(D_EDGES, 0, D_Y, BLUE)
            q_wave = wave(Q_EDGES, 1, Q_Y, GREEN)
            row_l = VGroup(T("EN", 32, BLUE).move_to([X0 - 0.55, EN_Y + H / 2, 0]),
                           T("D", 32, BLUE).move_to([X0 - 0.55, D_Y + H / 2, 0]),
                           T("Q", 32, GREEN).move_to([X0 - 0.55, Q_Y + H / 2, 0]))
            band = Rectangle(width=X(BAND[1]) - X(BAND[0]), height=EN_Y + H + 0.2 - (Q_Y - 0.2))
            band.set_stroke(width=0).set_fill(YELLOW, 0.10).set_z_index(-1)
            band.move_to([(X(BAND[0]) + X(BAND[1])) / 2, (EN_Y + H + 0.2 + Q_Y - 0.2) / 2, 0])
            c.wait_until("an output")
            self.play(*appear(VGroup(row_l[0], en_wave), VGroup(row_l[1], d_wave),
                              VGroup(row_l[2], q_wave), shift=None, lag=0.3),  # early: diagram shown whole, then walked
                      run_time=min(1.8, c.until("follows")))
            self.play(FadeIn(band), run_time=min(0.8, c.until("follows")))
            c.wait_until("follows")

            # {follows}: band brightens, Q copies every change of D inside it
            links = VGroup(*[DashedLine([X(u), D_Y - 0.1, 0], [X(u), Q_Y + H + 0.1, 0],
                                        dash_length=0.08).set_stroke(FG, 2, opacity=0.7)
                             for u in (0.38, 0.48, 0.58)])
            self.play(band.animate.set_fill(YELLOW, 0.22), run_time=1.0)
            self.play(*appear(*links, shift=None, lag=0.4), run_time=min(1.6, c.until("holds")))
            c.wait_until("holds")

            # {holds}: outside the band, Q is flat while D still changes
            q_flat = [Line([X(0), Q_Y + H, 0], [X(BAND[0]), Q_Y + H, 0]),
                      Line([X(BAND[1]), Q_Y + H, 0], [X(1), Q_Y + H, 0])]
            self.play(band.animate.set_fill(YELLOW, 0.10), *disappear(links), run_time=1.0)
            self.play(*[VShowPassingFlash(l.set_stroke(GREEN, 10), time_width=0.6) for l in q_flat],
                      run_time=1.5)
            c.wait_until()

        # ------------------------------------------------------------------ clip 2
        with self.say("c2.hook.2") as c:
            # {clock}: a CLK wire slides into EN
            clk_wire = latch.en_wire.copy().set_stroke(YELLOW, 6).set_z_index(1)
            clk_l = T("CLK", 32, YELLOW).next_to(latch.en_wire, DOWN, buff=0.15)
            target = clk_wire.copy()
            clk_wire.shift(0.8 * DOWN).set_stroke(opacity=0)
            self.play(Transform(clk_wire, target), FadeIn(clk_l, shift=0.8 * UP), run_time=1.0)

            # the waveform clears to two stacked copies of one CLK wave
            top = wave(CLK_EDGES, 0, TOP_Y, YELLOW, h=CLK_H)
            bot = wave(CLK_EDGES, 0, BOT_Y, YELLOW, h=CLK_H)
            top_l = T("CLK", 30, YELLOW).move_to([X0 - 0.6, TOP_Y + CLK_H / 2, 0])
            bot_l = T("CLK", 30, YELLOW).move_to([X0 - 0.6, BOT_Y + CLK_H / 2, 0])
            old = [row_l, en_wave, d_wave, q_wave, band]
            self.play(*during(disappear(*old), 0, 0.45),
                      *during(appear(VGroup(top_l, top), VGroup(bot_l, bot), shift=None, lag=0.2), 0.5, 1),
                      run_time=min(1.4, c.until("window")))
            c.wait_until("window")

            # {window}: every high level of the top copy is a band
            bands = [Rectangle(width=X(f) - X(r), height=CLK_H).set_stroke(width=0)
                     .set_fill(YELLOW, 0.18).set_z_index(-1)
                     .move_to([(X(r) + X(f)) / 2, TOP_Y + CLK_H / 2, 0])
                     for r, f in zip(RISES, FALLS)]
            self.play(*appear(*bands, shift=None, lag=0.3), run_time=1.6)
            win_l = T("listens: a window", 34, YELLOW).move_to([(X0 + X1) / 2, TOP_Y - 0.5, 0])
            self.play(*appear(win_l), run_time=1.0)
            c.wait_until("instant")

            # {instant}: the bottom copy dims to a thin line
            self.play(bot.animate.set_stroke(YELLOW, 2, opacity=0.55), run_time=1.0)
            c.wait_until("edge")

            # {edge}: each rising edge gets an up-arrow and a bright dot
            arrows = [Arrow([X(r), BOT_Y - 0.05, 0], [X(r), BOT_Y + CLK_H + 0.35, 0], buff=0,
                            stroke_width=6, tip_length=0.22, max_tip_length_to_length_ratio=0.3,
                            color=YELLOW) for r in RISES]
            dots = [Dot([X(r), BOT_Y, 0], radius=0.1, color=YELLOW) for r in RISES]
            self.play(*[GrowArrow(a) for a in arrows], *[FadeIn(d, scale=0.5) for d in dots],
                      run_time=1.5)
            inst_l = T("listens: an instant", 34, YELLOW).move_to([(X0 + X1) / 2, BOT_Y - 0.55, 0])
            self.play(*appear(inst_l), run_time=1.0)
            c.wait_until("question")

            # {question}
            q_mark = T("?", 72, YELLOW).move_to([X1 + 0.55, BOT_Y + CLK_H / 2, 0])
            self.play(*appear(q_mark), run_time=1.0)
            c.wait_until("answer")

            # {answer}: two copies of the latch, side by side
            sweep_clear(self, keep=[latch], run_time=1.0)
            left_c, right_c = np.array([-2.3, -0.4, 0]), np.array([2.3, -0.4, 0])
            self.play(latch.animate.shift(left_c - latch.box.get_center()), run_time=1.0)
            second = make_latch(right_c)
            self.play(*fly(latch, second), run_time=1.4)
            ms_l = T("master-slave D flip-flop", 48, FG).move_to([0, 2.5, 0])
            c.wait_until(own_word=ms_l)
            self.play(*appear(ms_l), run_time=1.0)
            c.wait_until()

        self.wait(3.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
