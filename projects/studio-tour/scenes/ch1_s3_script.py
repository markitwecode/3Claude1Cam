"""Chapter 1, scene 3: A plan, then a script. Clips c1.script.1 – c1.script.4."""
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

MARKS = ["{pending}", "{conses}", "{finally}", "{done}", "{pause}", "{answer}"]
LINE_SRC = ("[c4.trace.2] {pending} Look at what has piled up. {conses} The one, the two and the three "
            "are each waiting to be consed on. {finally} Only now, with the first list used up, can the "
            "conses actually happen, from the inside out. {done} Three onto four, then two, then one. "
            "{pause} {answer} One, two, three, four.")


def agent(label, w=2.8, h=0.7):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=BLUE, stroke_width=3,
                           fill_color=BLUE, fill_opacity=0.15)
    return VGroup(box, T(label, 30)).move_to(ORIGIN)


def tool(label):
    box = RoundedRectangle(corner_radius=0.15, width=2.8, height=0.7, stroke_color=DIM, stroke_width=3,
                           fill_color=DIM, fill_opacity=0.15)
    return VGroup(box, Mono(label, 28))


def page(label):
    w, h, f = 0.6, 0.8, 0.2
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0],
                   stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.15)
    fold = VMobject(stroke_color=TEAL, stroke_width=3).set_points_as_corners(
        [[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0]])
    lab = Mono(label, 28, TEAL)
    lab.next_to(body, DOWN, buff=0.15)
    return VGroup(body, fold, lab)


def speaker():
    body = Polygon([-0.3, -0.15, 0], [-0.1, -0.15, 0], [0.2, -0.4, 0], [0.2, 0.4, 0], [-0.1, 0.15, 0],
                   [-0.3, 0.15, 0], stroke_width=0, fill_color=FG, fill_opacity=1)
    a1 = Arc(radius=0.3, start_angle=-PI / 3, angle=2 * PI / 3, arc_center=[0.25, 0, 0], stroke_color=FG, stroke_width=4)
    a2 = Arc(radius=0.55, start_angle=-PI / 3, angle=2 * PI / 3, arc_center=[0.25, 0, 0], stroke_color=FG, stroke_width=4)
    return VGroup(body, a1, a2).scale(1.3)


def build_ladder():
    data = [("project", "focs/l03-lists", None),
            ("chapter", "ch4", "8–11 min · ≈ 1300–1800 words"),
            ("scene", "ch4_s3_trace", "45–150 s · one Manim file"),
            ("clip", "[c4.trace.2]", "15–40 s · one narration line ·\nthe unit of voicing and syncing"),
            ("mark", "{pending}", "a cue word")]
    heads = []
    for name, tag, gold in data:
        row = VGroup(T(name, 30, BLUE), Mono(tag, 28, YELLOW)).arrange(RIGHT, buff=0.3)
        parts = [row]
        if gold:
            parts.append(T(gold, 28, GOLD, line_spacing=0.8))
        heads.append(VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
    cx, W, top = 1.6, 9.6, 3.5
    tops, y = [], top
    for i, h in enumerate(heads):
        tops.append(y)
        y = y - 0.12 - h.height - 0.15
    bottoms = [0] * 5
    bottoms[4] = y
    for i in (3, 2, 1, 0):
        bottoms[i] = bottoms[i + 1] - 0.15
    boxes = []
    for i, h in enumerate(heads):
        w = W - 0.6 * i
        r = RoundedRectangle(corner_radius=0.15, width=w, height=tops[i] - bottoms[i], stroke_color=BLUE,
                             stroke_width=3, fill_color=BLUE, fill_opacity=0.05)
        r.move_to([cx, (tops[i] + bottoms[i]) / 2, 0])
        h.move_to([0, 0, 0]).align_to(r, LEFT).shift(RIGHT * 0.25)
        h.align_to([0, tops[i] - 0.12, 0], UP)
        boxes.append(r)
    allm = VGroup(*boxes, *heads)
    allm.shift(DOWN * (allm.get_center()[1]))
    return boxes, heads


class ScriptScene(NarratedScene):
    def construct(self):
        # ---------------- clip 1
        planner = agent("series-planner").move_to([-5.1, 1.0, 0])
        boxes, heads = build_ladder()
        ladder = VGroup(*boxes, *heads)
        with self.say("c1.script.1") as c:
            self.play(FadeIn(planner, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("planner")
            self.wait(1.2)
            self.play(planner.animate.move_to([-5.1, 3.1, 0]), run_time=1.6)
            c.wait_until("ladder")
            self.play(Create(boxes[0]), run_time=1.5)
            c.wait_until("project")
            self.play(FadeIn(heads[0], shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("chapter")
            self.play(FadeIn(boxes[1]), FadeIn(heads[1], shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("scene")
            self.play(FadeIn(boxes[2]), FadeIn(heads[2], shift=0.2 * DOWN), run_time=1.2)
        # ---------------- clip 2
        with self.say("c1.script.2") as c:
            self.play(FadeIn(boxes[3]), FadeIn(heads[3], shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("mark")
            self.play(FadeIn(boxes[4]), FadeIn(heads[4], shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("approve")
            self.remove(*boxes, *heads)
            self.add(ladder)
            plan = page("PLAN.md").move_to([-5.6, -2.1, 0])
            plan_body = plan[0:2]
            plan.shift(UP * 0)  # label sits below the page
            self.play(ladder.animate.scale(0.28).move_to([-5.1, 0.1, 0]), FadeIn(plan, shift=0.3 * UP),
                      run_time=1.5)
            tick = check_mark(YELLOW).move_to([-4.5, -1.95, 0])
            you = T("you", 30, YELLOW).next_to(tick, RIGHT, buff=0.15)
            self.play(Create(tick), FadeIn(you, shift=0.2 * RIGHT), run_time=0.8)
            c.wait_until("writers")
            writers = [agent("script-writer").move_to([x, 2.0, 0]) for x in (-1.6, 1.6, 4.8)]
            pages = [page(f"ch{i + 1}_….md").move_to([x, 0.0, 0]) for i, x in enumerate((-1.6, 1.6, 4.8))]
            self.play(*[FadeIn(w, shift=0.3 * DOWN) for w in writers], run_time=1.0)
            self.play(*[FadeIn(p, shift=0.6 * DOWN) for p in pages], run_time=1.2)
            c.wait_until("line")
            line_text = Mono(textwrap.fill(LINE_SRC, 52), 28, FG, line_spacing=0.6, t2c={m: YELLOW for m in MARKS})
            rect = SurroundingRectangle(line_text, color=TEAL, buff=0.25, corner_radius=0.15)
            mid = pages[1]
            others = [m for m in self.mobjects if m is not mid]
            self.play(*[FadeOut(m) for m in others], ReplacementTransform(mid, rect), run_time=1.2)
            self.play(Write(line_text), run_time=c.until("marks", floor=1.0) - 0.2)
            c.wait_until("marks")
            script = VGroup(rect, line_text)
            self.remove(rect, line_text)
            self.add(script)
            self.play(LaggedStart(*[FlashAround(select(line_text, m)[0], color=YELLOW, buff=0.06)
                                    for m in MARKS], lag_ratio=0.25), run_time=2.4)
            c.wait_until("brief")
            e1 = Mono('The waiting `1 ::`, `2 ::`, `3 ::` turn YELLOW and\nstay; a brace under them, "waiting" (on {pending}). …',
                      28, DIM, line_spacing=0.6, t2c={"{pending}": YELLOW})
            e2 = Mono("On {done} the conses fire inside out: `3 :: [4]`,\nthen `2 ::`, then `1 ::`, collapsing into GREEN\n`[1; 2; 3; 4]`.",
                      28, DIM, line_spacing=0.6, t2c={"{done}": YELLOW})
            blocks = VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            g1 = Mono(">", 28, TEAL).next_to(e1.get_corner(UL), RIGHT, buff=0).shift(LEFT * 0.35 + DOWN * 0.22)
            g2 = Mono(">", 28, TEAL).next_to(e2.get_corner(UL), RIGHT, buff=0).shift(LEFT * 0.35 + DOWN * 0.22)
            brief = VGroup(blocks, g1, g2)
            script.generate_target()
            script.target.to_edge(DOWN, buff=0.65)
            brief.next_to(script.target, UP, buff=0.25)
            brief.set_x(0)
            self.play(MoveToTarget(script), FadeIn(brief, shift=0.3 * DOWN), run_time=1.5)
            joins = []
            for key, src in (("{pending}", e1), ("{done}", e2)):
                a = select(src, key)[0]
                b = select(line_text, key)[0]
                joins.append(Line(a.get_bottom() + DOWN * 0.05, b.get_top() + UP * 0.05, color=YELLOW,
                                  stroke_width=2).set_opacity(0.6))
            self.play(*[Create(j) for j in joins], run_time=1.2)
            self.wait(0.2)
        # ---------------- clip 3
        with self.say("c1.script.3") as c:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
            c.wait_until("before")
            before = T("exactly en conses", 52)
            before.move_to([0, 2.4, 0])
            strike = Line(before.get_left() + LEFT * 0.1, before.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
            strike_full = strike.copy()
            strike.become(Line(strike_full.get_start(), strike_full.get_start() + RIGHT * 0.001, color=RED, stroke_width=6))
            before_g = VGroup(before, strike)
            self.play(FadeIn(before_g, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("heard")
            spk = speaker().move_to([-3.3, 0.5, 0])
            red = T("exactly unconscious", 52, RED).move_to([1.3, 0.5, 0])
            self.play(FadeIn(spk), run_time=0.6)
            self.play(FadeIn(red, shift=1.2 * RIGHT), run_time=1.4)
            self.play(Transform(strike, strike_full), run_time=0.7)
            c.wait_until("after")
            after = T("one cons per element", 52, GREEN).move_to([0, -1.6, 0])
            self.play(TransformFromCopy(before, after), run_time=1.8)
            c.wait_until("verify")
            self.play(FadeOut(spk), FadeOut(red), before_g.animate.scale(0.7).move_to([0, 3.0, 0]),
                      after.animate.scale(0.7).move_to([0, 2.15, 0]), run_time=1.0)
            code1 = Mono("append [1; 2; 3] [4]", 34, FG)
            code2 = Mono("- : int list = [1; 2; 3; 4]", 34, FG, t2c={"int list": GREEN})
            code = VGroup(code1, code2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            card = SurroundingRectangle(code, color=DIM, buff=0.35, corner_radius=0.15)
            lang = T("OCaml", 28, DIM).next_to(card, UP, buff=0.12).align_to(card, LEFT)
            cardg = VGroup(card, code, lang).move_to([0, 0.0, 0])
            ok = VGroup(check_mark(GREEN), T("run, reply pasted exactly", 36, GREEN)).arrange(RIGHT, buff=0.25)
            ok.move_to([0, -2.1, 0])
            self.play(FadeIn(cardg, shift=0.2 * UP), run_time=1.0)
            self.play(Create(ok[0]), FadeIn(ok[1], shift=0.2 * RIGHT), run_time=1.0)
        # ---------------- clip 4
        with self.say("c1.script.4") as c:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
            planner2 = agent("series-planner").move_to([-5.1, 1.0, 0])
            pgs = VGroup(*[page(f"ch{i + 1}_….md") for i in range(3)])
            for p, x in zip(pgs, (-2.0, 0.0, 2.0)):
                p.move_to([x, 1.0, 0])
            self.play(FadeIn(planner2, shift=0.3 * RIGHT), LaggedStart(*[FadeIn(p, shift=0.3 * DOWN) for p in pgs],
                      lag_ratio=0.3), run_time=1.5)
            c.wait_until("it checks for")
            rows = [T(s, 32, FG) for s in ("same terms", "last time → next time", "lengths")]
            rv = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            rv.move_to([-0.6, -1.7, 0])
            checks = [check_mark(GREEN).scale(0.8).next_to(r, LEFT, buff=0.3) for r in rows]
            sweep = SurroundingRectangle(pgs, color=YELLOW, buff=0.2)
            sweep.set_stroke(YELLOW, 6)
            c.wait_until("same terms")
            self.play(VShowPassingFlash(sweep, time_width=0.5), time_span(FadeIn(rows[0]), 0, 0.5),
                      time_span(Create(checks[0]), 0.5, 1.0), run_time=1.1)
            c.wait_until("last time")
            self.play(FadeIn(rows[1]), run_time=0.4)
            self.play(Create(checks[1]), run_time=0.4)
            c.wait_until("right lengths")
            self.play(FadeIn(rows[2]), run_time=0.4)
            self.play(Create(checks[2]), run_time=0.4)
            c.wait_until("voiced")
            voice = tool("vk voice").move_to([5.3, 1.0, 0])
            arrow = Arrow([3.0, 1.0, 0], [3.9, 1.0, 0], buff=0, color=DIM, stroke_width=4)
            self.play(FadeIn(voice, shift=0.3 * LEFT), GrowArrow(arrow), run_time=0.9)
            self.play(arrow.animate.set_color(TEAL), run_time=0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
