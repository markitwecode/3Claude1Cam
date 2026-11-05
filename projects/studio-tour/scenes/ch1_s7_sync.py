"""Chapter 1, scene 7: cued on words, never on seconds. Clips c1.sync.1 – c1.sync.3.

Top: the real say block of c4.trace.2 (excerpt of focs/l03-lists/scenes/ch4_s3_trace.py,
lines 228, 257, 259, 290), walked with one sliding token box. Bottom: the clip's timeline in
s4's style (DIM axis, GOLD sentence ticks, YELLOW cue pins with Mono labels, BLUE blocks for
the cued animations hanging off their pins). c1.sync.3 moves the timeline to the centre,
re-voices the line (longer), slides pins and blocks, leaves the RED seconds-timed block
behind, and shows an overrun shoving the next clip.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = '''with self.say("c4.trace.2") as c:
    ...
    c.wait_until("inside out")
    self.play(FadeIn(ubox),
              run_time=min(0.8, 0.9 * c.until("done")))
    ...
    c.wait_until("answer")'''

# c4.trace.2 as voiced (word times from its manifest), and a longer re-voicing for c1.sync.3
TIMES1 = dict(end=18.2, ticks=(0.0, 2.2, 6.5, 12.0, 15.4),
              pins=dict(each=4.2, inside=10.56, done=12.0, answer=15.4))
TIMES2 = dict(end=20.6, ticks=(0.0, 3.4, 8.2, 14.0, 17.6),
              pins=dict(each=5.75, inside=12.6, done=14.0, answer=17.6))
H_TALL, H_SHORT = 1.45, 0.85
PINS = dict(each=(H_TALL, "each"), inside=(H_TALL, "inside out"),
            done=(H_SHORT, "{done}"), answer=(H_SHORT, "{answer}"))
BLOCKS = dict(b1=("inside", 0.8, BLUE), b2=("answer", 1.5, BLUE), red=(None, 1.0, RED))
RED_T = 4.2                                   # the RED block is timed in seconds: never moves
HARD = "c.start {} 4.2".format("+")           # the builder kit's example of what never to write
LANE, BLK_H = 0.08, 0.36
L1 = dict(s=11 / 18.2, x0=-5.5, A=-2.3)       # under the code, s4's 11-unit axis
L2 = dict(s=0.47, x0=-6.2, A=-0.1)            # c1.sync.3: centred, room for the stretch


def timeline(times, s, x0, A):
    X = lambda t: x0 + s * t  # noqa: E731
    p = {}
    p["axis"] = Line([X(0), A, 0], [X(times["end"]), A, 0]).set_stroke(DIM, 3)
    p["end"] = Line([X(times["end"]), A - 0.2, 0], [X(times["end"]), A + 0.2, 0]).set_stroke(DIM, 3)
    for i, t in enumerate(times["ticks"]):
        p[f"tick{i}"] = Line([X(t), A - 0.13, 0], [X(t), A + 0.13, 0]).set_stroke(GOLD, 3)
        p[f"num{i}"] = T(f"{t:.1f}", 28, GOLD).move_to([X(t), A - 0.42, 0])
    for k, (h, text) in PINS.items():
        x = X(times["pins"][k])
        p[f"pin_{k}"] = Line([x, A, 0], [x, A + h, 0]).set_stroke(YELLOW, 2).set_z_index(1)
        p[f"lab_{k}"] = Mono(text, 28, YELLOW).move_to([x - 0.04, A + h + 0.1, 0], aligned_edge=DL)
    for k, (pin, dur, col) in BLOCKS.items():
        t0 = RED_T if pin is None else times["pins"][pin]
        r = Rectangle(width=dur * s, height=BLK_H).set_stroke(col, 2).set_fill(col, 0.45)
        p[k] = r.move_to([X(t0), A + LANE, 0], aligned_edge=DL)
    p["red_lab"] = Mono(HARD, 28, RED).move_to([p["red"].get_x(), A - 1.0, 0])
    return p


def page(color=TEAL, w=0.42, h=0.54, f=0.14):
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0]).set_stroke(color, 2).set_fill(color, 0.15)
    fold = Polygon([w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0],
                   [w / 2, h / 2 - f, 0]).set_stroke(color, 2).set_fill(color, 0.4)
    return VGroup(body, fold)


class Ch1S7Sync(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c1.sync.1: the say block, walked term by term ─────────────────────────────────
    def clip1(self):
        code = Code(SRC, size=28)
        code.to_edge(UP, buff=0.4).set_x(0)
        self.code = code
        pitch = (code.line(2).get_y() - code.line(6).get_y()) / 4
        y_row5 = code.line(4).get_y() - pitch
        y_row7 = code.line(6).get_y() - pitch
        self.y_row5 = y_row5
        tl = timeline(TIMES1, **L1)
        self.tl = tl
        X1 = lambda t: L1["x0"] + L1["s"] * t  # noqa: E731
        A1 = L1["A"]

        g_say = code.find('self.say("c4.trace.2")')
        g_until = code.find('c.until("done")')
        g_wait = code.find('c.wait_until("inside out")')
        BH = 0.52
        box = token_box(g_say, code.line(0), height=BH)
        leave_box = (Rectangle(width=0.55, height=BH).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.25)
                     .move_to([code.get_left()[0] + 0.2, y_row7, 0]).set_z_index(-1))

        lab_say = T("audio starts now", 28, DIM).next_to(code.line(0), RIGHT, buff=0.5)
        lab_until = T("seconds to the cue → run_time", 28, DIM)
        lab_until.move_to([0, y_row5, 0]).align_to(g_until, RIGHT)
        lab_wait = T("idle until the cue", 28, DIM).next_to(code.line(2), RIGHT, buff=0.5)
        lab_leave = T("wait out the clip + 0.35 s", 28, DIM).next_to(leave_box, RIGHT, buff=0.3)
        self.walk = [box, lab_say, lab_until, lab_wait, lab_leave]

        with self.say("c1.sync.1") as c:
            # {code} the excerpt appears
            self.play(*[time_span(FadeIn(code.line(i), shift=0.15 * DOWN), 0.15 * i, 0.9 + 0.15 * i)
                        for i in range(7)])
            # "Here's part of the real code for trace two": its timeline, whole shape first
            c.wait_until("here's part")
            anims = [time_span(Create(tl["axis"]), 0, 1.0), time_span(FadeIn(tl["end"]), 0.7, 1.1)]
            for i in range(5):
                anims += [time_span(FadeIn(tl[f"tick{i}"]), 0.2 + 0.15 * i, 0.7 + 0.15 * i),
                          time_span(FadeIn(tl[f"num{i}"], shift=0.15 * UP), 0.3 + 0.15 * i, 0.9 + 0.15 * i)]
            for j, k in enumerate(("inside", "done", "answer")):
                anims += [time_span(GrowFromEdge(tl[f"pin_{k}"], DOWN), 1.0 + 0.2 * j, 1.6 + 0.2 * j),
                          time_span(FadeIn(tl[f"lab_{k}"], shift=0.2 * DOWN), 1.2 + 0.2 * j, 1.8 + 0.2 * j)]
            anims += [time_span(GrowFromEdge(tl["b1"], LEFT), 1.6, 2.2),
                      time_span(GrowFromEdge(tl["b2"], LEFT), 1.8, 2.4)]
            self.play(*anims)

            # {say} audio starts now
            c.wait_until("say")
            sweep = tl["axis"].copy().set_stroke(YELLOW, 6)
            self.play(FadeIn(box), FadeIn(lab_say, shift=0.2 * LEFT),
                      time_span(VShowPassingFlash(sweep, time_width=0.4), 0.6, 2.6))

            # {until} seconds from now to the cue, used as a run_time
            c.wait_until("until")
            self.play(Transform(box, token_box(g_until, code.line(4), height=BH)),
                      FadeIn(lab_until, shift=0.2 * UP), run_time=1.2)
            c.wait_until("seconds")
            yb = A1 + 0.65
            xl, xr = X1(TIMES1["pins"]["inside"]), X1(TIMES1["pins"]["done"])
            bracket = VGroup(Line([xl, yb, 0], [xr, yb, 0]),
                             Line([xl, yb - 0.1, 0], [xl, yb + 0.1, 0]),
                             Line([xr, yb - 0.1, 0], [xr, yb + 0.1, 0])).set_stroke(GOLD, 3)
            self.bracket = bracket
            self.play(GrowFromEdge(bracket, LEFT), run_time=1.0)
            c.wait_until("run time")
            self.play(FlashAround(tl["b1"], color=GOLD, time_width=1.5),
                      run_time=min(1.2, c.until(floor=0.6)))

            # {wait} idles until the cue
            c.wait_until("wait")
            self.play(Transform(box, token_box(g_wait, code.line(2), height=BH)),
                      FadeIn(lab_wait, shift=0.2 * LEFT),
                      time_span(FlashAround(VGroup(tl["pin_inside"], tl["lab_inside"]),
                                            time_width=1.5), 0.4, 1.6))

            # {leave} the dedent: wait out the clip + 0.35 s
            c.wait_until("leave")
            x_from, x_to = X1(15.4 + 1.5), X1(TIMES1["end"] + 0.35)
            dashed = DashedLine([x_from, A1 + LANE + BLK_H / 2, 0], [x_to, A1 + LANE + BLK_H / 2, 0],
                                dash_length=0.08).set_stroke(DIM, 3)
            self.dashed = dashed
            self.play(Transform(box, leave_box), FadeIn(lab_leave, shift=0.2 * LEFT),
                      time_span(Create(dashed, rate_func=linear), 0.5, 1.7))

    # ── c1.sync.2: what a cue is; why bother ─────────────────────────────────────────
    def clip2(self):
        code, tl = self.code, self.tl
        box = self.walk[0]
        cue_g = [code.find('"inside out"'), code.find('"done"'), code.find('"answer"')]
        cue_ids = {id(g) for grp in cue_g for g in grp}
        others = [g for g in code.text if id(g) not in cue_ids]

        man = VGroup(page(), Mono("manifest.json", 28, FG))
        man[1].next_to(man[0], RIGHT, buff=0.2)
        wt = T("word times", 28, DIM).next_to(man[1], DOWN, buff=0.12, aligned_edge=LEFT)
        man.add(wt)
        man.move_to([0, -1.05, 0]).to_edge(LEFT, buff=0.7)
        man_arrow = Arrow([man.get_right()[0] + 0.15, -1.05, 0],
                          [tl["pin_inside"].get_x() - 0.12, -1.05, 0],
                          buff=0, stroke_width=3).set_color(TEAL)

        tag_phrase = T("a phrase", 30, FG).next_to(code.line(2), RIGHT, buff=0.5)
        tag_done = T("a mark", 30, FG).move_to([cue_g[1].get_x(), self.y_row5, 0])
        tag_answer = T("a mark", 30, FG).next_to(code.line(6), RIGHT, buff=0.5)

        with self.say("c1.sync.2") as c:
            # {cue} the cue strings light up and fly to their pins
            self.play(FadeOut(box), *recolor([g for grp in cue_g for g in grp], YELLOW),
                      *set_alpha(others, 0.4), run_time=1.0)
            flies, anims = [], []
            for j, (grp, k) in enumerate(zip(cue_g, ("inside", "done", "answer"))):
                fly = VGroup(*[g.copy() for g in grp])
                flies.append(fly)
                anims.append(time_span(Transform(fly, tl[f"lab_{k}"].copy()), 0.3 * j, 1.3 + 0.3 * j))
            self.play(*anims)
            self.remove(*flies)
            c.wait_until("looked up")
            self.play(*[FadeOut(m) for m in self.walk[1:]], FadeOut(self.bracket), FadeOut(self.dashed),
                      FadeIn(man, shift=0.2 * DOWN), time_span(GrowArrow(man_arrow), 0.5, 1.3))

            # {here} a phrase; marks
            c.wait_until("inside out")
            self.play(FadeIn(tag_phrase, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("and done")
            self.play(FadeIn(tag_done, shift=0.2 * UP), FadeIn(tag_answer, shift=0.2 * LEFT), run_time=0.8)

            # {why} the code goes; a question, held through the pause
            c.wait_until("why")
            q = T("?", 144, YELLOW).move_to([0, 1.7, 0])
            sweep_clear(self, time_span(FadeIn(q, scale=0.8), 0.5, 1.3),
                        keep=[tl[k] for k in self.on_screen()], run_time=1.3)

            # {v1} 157 hard-coded times
            c.wait_until("v1")
            n157 = T("157", 120, GOLD).move_to([0, 2.2, 0])
            v1 = T("hard-coded times · v1", 40, RED).move_to([0, 1.0, 0])
            self.play(ReplacementTransform(q, n157), time_span(FadeIn(v1, shift=0.2 * DOWN), 0.6, 1.5),
                      run_time=1.5)
            # "every line voiced again ...": one hard-coded time, on its word for now
            c.wait_until("every line")
            self.play(GrowFromEdge(tl["pin_each"], DOWN), FadeIn(tl["lab_each"], shift=0.2 * DOWN),
                      GrowFromEdge(tl["red"], LEFT), FadeIn(tl["red_lab"], shift=0.2 * UP), run_time=1.2)
            self.has_red = True

    def on_screen(self):
        keys = ["axis", "end"] + [f"tick{i}" for i in range(5)] + [f"num{i}" for i in range(5)]
        keys += [f"pin_{k}" for k in ("inside", "done", "answer")]
        keys += [f"lab_{k}" for k in ("inside", "done", "answer")] + ["b1", "b2"]
        if getattr(self, "has_red", False):
            keys += ["pin_each", "lab_each", "red", "red_lab"]
        return keys

    # ── c1.sync.3: re-voiced; pins and cued blocks slide, the seconds block doesn't ───
    def clip3(self):
        tl = self.tl
        A2 = L2["A"]
        X2 = lambda t: L2["x0"] + L2["s"] * t  # noqa: E731
        mid = timeline(TIMES1, **L2)        # same times, centred layout
        new = timeline(TIMES2, **L2)        # the re-voiced line
        keys = self.on_screen()
        clip_lab = Mono("c4.trace.2", 28, YELLOW).move_to([L2["x0"], A2 + 2.3, 0], aligned_edge=LEFT)

        cross = cross_mark(RED).scale(0.85).move_to([mid["red"].get_x(), A2 + 0.8, 0])

        vk_lab = Mono("vk check", 28, FG)
        vk_box = (RoundedRectangle(corner_radius=0.15, width=vk_lab.width + 0.5, height=0.62)
                  .set_stroke(DIM, 2).set_fill(BLUE, 0.15).move_to(vk_lab))
        vk = VGroup(vk_box, vk_lab)
        vk.move_to([mid["red_lab"].get_left()[0], A2 - 1.75, 0], aligned_edge=LEFT)
        hc = T("hard-coded time", 28, RED).next_to(vk, RIGHT, buff=0.25)

        gap = 0.35
        x_strip = X2(TIMES2["end"] + gap)
        strip = (RoundedRectangle(corner_radius=0.08, width=2.2, height=0.4)
                 .set_stroke(DIM, 2).set_fill(DIM, 0.2).move_to([x_strip, A2, 0], aligned_edge=LEFT))
        strip_lab = Mono("c4.trace.3", 28, DIM).move_to([x_strip, A2 + 0.65, 0], aligned_edge=LEFT)
        over_end = TIMES2["end"] + 1.0
        b2_long = (Rectangle(width=(over_end - TIMES2["pins"]["answer"]) * L2["s"], height=BLK_H)
                   .set_stroke(RED, 2).set_fill(RED, 0.45)
                   .move_to([X2(TIMES2["pins"]["answer"]), A2 + LANE, 0], aligned_edge=DL))
        shove = (X2(over_end + gap) - x_strip) * RIGHT
        overrun = T("overrun", 30, RED).move_to([(X2(TIMES2["end"]) + X2(over_end)) / 2, A2 - 0.62, 0])

        with self.say("c1.sync.3") as c:
            # {revoice} the timeline takes the stage, then the line is voiced again, longer
            sweep_clear(self, *[Transform(tl[k], mid[k]) for k in keys],
                        time_span(FadeIn(clip_lab, shift=0.2 * DOWN), 0.5, 1.3),
                        keep=[tl[k] for k in keys], run_time=1.3)
            stretch = ["axis", "end"] + [f"tick{i}" for i in range(5)] + [f"num{i}" for i in range(5)]
            self.play(*[Transform(tl[k], new[k]) for k in stretch],
                      run_time=min(2.0, max(1.0, c.until("slide") - 0.3)))

            # {slide} pins slide with their words, the cued blocks with them
            c.wait_until("slide")
            pins = [f"pin_{k}" for k in PINS] + [f"lab_{k}" for k in PINS]
            self.play(*[Transform(tl[k], new[k]) for k in pins], run_time=1.5)
            c.wait_until("the animations cued")
            self.play(Transform(tl["b1"], new["b1"]), Transform(tl["b2"], new["b2"]), run_time=1.2)

            # {stuck} the block timed in seconds stays put, off its word
            c.wait_until("stuck")
            self.play(Create(cross), FlashAround(tl["red"], color=RED, time_width=1.5), run_time=1.2)

            # {flags} vk check flags it
            c.wait_until("flags")
            self.play(FadeIn(vk, shift=0.2 * UP), time_span(FadeIn(hc, shift=0.2 * LEFT), 0.3, 1.1),
                      time_span(FlashAround(tl["red_lab"], color=RED, time_width=1.5), 0.4, 1.4))

            # {overrun} a block outlasts its clip and shoves the next one late
            c.wait_until("overrun")
            self.play(FadeIn(strip), FadeIn(strip_lab, shift=0.2 * DOWN), run_time=0.8)
            self.play(Transform(tl["b2"], b2_long), strip.animate.shift(shove),
                      strip_lab.animate.shift(shove),
                      time_span(FadeIn(overrun, shift=0.2 * UP), 0.6, 1.4), run_time=1.5)
