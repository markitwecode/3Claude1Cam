"""Chapter 1, scene 5: one director per chapter, its checklist, music, builders. Clips c1.dir.1 – c1.dir.4.

Checklist (shared with ch1_s8, must match): see CHECK_* constants and build_checklist().
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


# ---------------------------------------------------------------- shared look
def agent(w, h, label=None, size=30, mono=False, outline=BLUE, fill_op=0.15, label_color=FG):
    """BLUE rounded agent box (opaque BG backing so stacked copies hide what's behind)."""
    back = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(width=0).set_fill(BG, 1)
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(outline, 3).set_fill(BLUE, fill_op)
    g = VGroup(back, rect)
    if label:
        t = (Mono if mono else T)(label, size=size, color=label_color)
        if t.width > w - 0.2:
            t.scale_to_fit_width(w - 0.2)
        g.add(t)
    return g


def builder_box(w, h, lit=True):
    r = RoundedRectangle(corner_radius=min(0.15, h / 3), width=w, height=h)
    if lit:
        r.set_stroke(BLUE, 3).set_fill(BLUE, 0.15)
    else:
        r.set_stroke(DIM, 2).set_fill(BLUE, 0)
    return r


def page(w, h, fold=None, color=TEAL, fill_op=0.1, stroke=3):
    f = fold if fold is not None else min(w, h) * 0.28
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0])
    body.set_stroke(color, stroke).set_fill(color, fill_op)
    corner = VMobject().set_points_as_corners([[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0],
                                               [w / 2, h / 2 - f, 0]])
    corner.set_stroke(color, max(1.5, stroke - 1))
    return VGroup(body, corner)


def row_xs(cx, n, w, gap):
    pitch = w + gap
    return [cx + (i - (n - 1) / 2) * pitch for i in range(n)]


def conn(a, b, width=2):
    return Line(a.get_bottom(), b.get_top()).set_stroke(DIM, width)


# ---------------------------------------------------------------- checklist (s8 repeats it)
CHECK_NUM_X = -6.3        # centre x of the numbers
CHECK_NAME_X = -5.85      # left edge of item names and of the sub-label lines
CHECK_SIZE = 34           # T size of numbers and names
CHECK_SUB_SIZE = 28       # Mono size of the orient sub-label (DIM)
CHECK_Y = [2.74, 0.9, 0.22, -0.46, -1.14, -1.82, -2.5]   # item centres
CHECK_SUB_Y = [2.27, 1.87, 1.47]                        # sub-label line centres
CHECK_NAMES = ["orient", "narration fixes", "music", "builders", "review", "final", "record"]
CHECK_SUB = ["vk status", "PLAN.md · STATUS.md", "script, once"]


def build_checklist():
    items = []
    for i, (name, y) in enumerate(zip(CHECK_NAMES, CHECK_Y)):
        num = T(str(i + 1), size=CHECK_SIZE, color=DIM).move_to([CHECK_NUM_X, y, 0])
        nm = T(name, size=CHECK_SIZE, color=DIM)
        nm.move_to([CHECK_NAME_X + nm.width / 2, y, 0])
        nm.align_to(num, DOWN)
        items.append(VGroup(num, nm))
    sub = VGroup()
    for s, y in zip(CHECK_SUB, CHECK_SUB_Y):
        m = Mono(s, size=CHECK_SUB_SIZE, color=DIM)
        m.move_to([CHECK_NAME_X + m.width / 2, y, 0])
        sub.add(m)
    return items, sub


ROW = 26.5   # master-shot row label size (matches ch1_s2_crew)


class Director(NarratedScene):
    # ------------------------------------------------------------ helpers
    def master_shot(self):
        you = T("you", size=36, color=YELLOW).move_to([0, 3.4, 0])
        producer = agent(3.2, 0.8, "producer", 32).move_to([0, 2.45, 0])
        planner = agent(2.8, 0.7, "series-planner", ROW).move_to([-5.1, 1.0, 0])
        writers = VGroup(*[agent(2.8, 0.7, "script-writer" if k == 0 else None, ROW)
                           .move_to([-1.7 + 0.1 * k, 1.0 + 0.1 * k, 0]) for k in (2, 1, 0)])
        voice = agent(2.8, 0.7, "vk voice", ROW, mono=True, outline=DIM, label_color=DIM).move_to([1.7, 1.0, 0])
        dir_back = VGroup(*[agent(2.8, 0.7, None, 28, outline=DIM, fill_op=0.06)
                            .move_to([5.1 + 0.08 * k, 1.0 + 0.08 * k, 0]) for k in (2, 1)])
        dir_front = agent(2.8, 0.7, "chapter-director", ROW).move_to([5.1, 1.0, 0])
        builders = [builder_box(0.75, 0.45).move_to([x, -0.5, 0]) for x in row_xs(3.0, 8, 0.75, 0.15)]
        blabel = T("scene-builder × 6–8", size=28, color=DIM).move_to([3.0, -1.05, 0])
        top_conns = VGroup(Line(you.get_bottom() + 0.05 * DOWN, producer.get_top()).set_stroke(DIM, 2).set_z_index(-1),
                           *[conn(producer, b) for b in (planner, writers[-1], voice, dir_front)])
        dconns = [conn(dir_front, b) for b in builders]
        # "×N" count tags (as s2): T 26.5 DIM, right edge 0.1 inside the front box, centre y = 0.42
        w_n = T("×N", size=ROW, color=DIM)
        w_n.move_to([writers[-1].get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
        d_n = T("×N", size=ROW, color=DIM)
        d_n.move_to([dir_front.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
        rest = VGroup(you, producer, planner, writers, voice, dir_back, top_conns, w_n, d_n)
        return rest, dir_front, builders, blabel, dconns

    def unit(self, cx, dy, by, bw, bh, gap, lit=True, label=True):
        d = agent(3.6, 0.9, "chapter-director", 32,
                  outline=BLUE if lit else DIM, fill_op=0.15 if lit else 0,
                  label_color=FG if lit else DIM).move_to([cx, dy, 0])
        bs = [builder_box(bw, bh).move_to([x, by, 0]) for x in row_xs(cx, 8, bw, gap)]
        cs = [conn(d, b) for b in bs]
        return d, bs, cs

    def hl(self, c, items, prev, cur, nxt):
        anims = [items[cur].animate.set_color(YELLOW)]
        if prev is not None:
            anims.append(items[prev].animate.set_color(DIM))
        self.play(*anims, run_time=min(0.6, 0.6 * c.until(nxt)))
        c.wait_until(nxt)

    # ------------------------------------------------------------ scene
    def construct(self):
        rest, dfront, mbuilders, mblabel, mconns = self.master_shot()
        self.play(FadeIn(rest, *mconns, dfront, *mbuilders, mblabel), run_time=1.0)
        self.wait(0.8)

        items, sub = build_checklist()

        # ---------------- c1.dir.1: zoom, checklist
        with self.say("c1.dir.1") as c:
            d, bs, cs = self.unit(3.1, 1.6, -0.4, 0.72, 0.6, 0.14)
            blabel = T("scene-builder × 6–8", size=30, color=DIM).move_to([3.1, -1.1, 0])
            self.play(FadeOut(rest, scale=1.3),
                      ReplacementTransform(dfront, d),
                      *[ReplacementTransform(a, b) for a, b in zip(mbuilders, bs)],
                      *[ReplacementTransform(a, b) for a, b in zip(mconns, cs)],
                      ReplacementTransform(mblabel, blabel),
                      run_time=min(2.0, 0.9 * c.until("steps")))
            c.wait_until("steps")
            self.play(LaggedStart(*[FadeIn(it, shift=0.2 * RIGHT) for it in items], lag_ratio=0.15),
                      run_time=min(2.0, 0.9 * c.until("orient")))
            c.wait_until("orient")
            self.play(items[0].animate.set_color(YELLOW),
                      LaggedStart(*[FadeIn(s, shift=0.2 * DOWN) for s in sub], lag_ratio=0.3),
                      run_time=1.5)
            c.wait_until("narration")
            self.hl(c, items, 0, 1, "music")
            self.hl(c, items, 1, 2, "builders")
            self.hl(c, items, 2, 3, "review")
            self.hl(c, items, 3, 4, "final")
            self.hl(c, items, 4, 5, "record")
            self.play(items[6].animate.set_color(YELLOW), items[5].animate.set_color(DIM), run_time=0.6)

        # ---------------- c1.dir.2: one at a time, or two for speed
        with self.say("c1.dir.2") as c:
            dA, bA, cA = self.unit(-3.4, 2.2, 0.8, 0.66, 0.55, 0.12)
            dB = agent(3.6, 0.9, "chapter-director", 32, outline=DIM, fill_op=0,
                       label_color=DIM).move_to([3.4, 2.2, 0])
            self.play(FadeOut(*items, sub, blabel),
                      ReplacementTransform(d, dA),
                      *[ReplacementTransform(a, b) for a, b in zip(bs, bA)],
                      *[ReplacementTransform(a, b) for a, b in zip(cs, cA)],
                      run_time=min(1.6, 0.6 * c.until("spike")))
            axis = VMobject().set_points_as_corners([[-6.2, -0.9, 0], [-6.2, -3.1, 0], [1.2, -3.1, 0]])
            axis.set_stroke(DIM, 2)
            usage = T("usage", size=30, color=DIM)
            usage.move_to([-5.95 + usage.width / 2, -0.95, 0])
            flat = VMobject().set_points_as_corners([[-6.2, -2.7, 0], [-2.6, -2.7, 0]]).set_stroke(GOLD, 5)
            self.play(FadeIn(dB, shift=0.2 * DOWN), Create(axis), FadeIn(usage),
                      run_time=min(1.0, 0.8 * c.until("spike")))
            self.play(Create(flat), run_time=min(1.0, 0.9 * c.until("spike")))
            c.wait_until("spike")

            dB_lit, bB, cB = self.unit(3.4, 2.2, 0.8, 0.66, 0.55, 0.12)
            self.play(ReplacementTransform(dB, dB_lit),
                      *[TransformFromCopy(a, b) for a, b in zip(bA, bB)],
                      *[ReplacementTransform(a.copy(), b) for a, b in zip(cA, cB)],
                      run_time=1.6)
            icons = [Triangle().set_fill(GOLD, 1).set_stroke(width=0).scale(0.11).rotate(-PI / 2)
                     .move_to(b) for b in bA + bB]
            spike = VMobject().set_points_as_corners([[-2.6, -2.7, 0], [-2.2, -1.3, 0], [1.2, -1.3, 0]])
            spike.set_stroke(GOLD, 5)
            self.play(LaggedStart(*[GrowFromCenter(i) for i in icons], lag_ratio=0.08),
                      Create(spike, rate_func=linear), run_time=1.8)
            c.wait_until("twelve to sixteen")
            renders = T("12–16 renders", size=40, color=GOLD).move_to([4.3, -1.3, 0])
            self.play(FadeIn(renders, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("speed")
            half = T("≈ ½ the wall time", size=40, color=GOLD).move_to([4.3, -2.2, 0])
            ask = T("if you ask for speed", size=30, color=YELLOW).move_to([4.3, -2.9, 0])
            self.play(FadeIn(half, shift=0.3 * DOWN), time_span(FadeIn(ask, shift=0.2 * DOWN), 0.6, 1.4),
                      run_time=1.4)

        # ---------------- c1.dir.3: music cue sheet
        with self.say("c1.dir.3") as c:
            # the second director goes first, then the rest of the board
            self.play(FadeOut(dB_lit, *bB, *cB, *icons[8:]), run_time=0.7)
            for it in items:
                it.set_color(DIM)
            items[2].set_color(YELLOW)
            sweep_clear(self, LaggedStart(*[FadeIn(it) for it in items], FadeIn(sub), lag_ratio=0.08),
                        run_time=1.2)

            pg = page(6.4, 1.6, fold=0.35).move_to([3.25, 1.9, 0])
            fname = Mono("music/ch4.json", size=28, color=TEAL)
            fname.move_to([pg.get_left()[0] + 0.3 + fname.width / 2, 2.35, 0])
            line = Mono('"from": "c4.nrev.3:end",', size=28)
            line.move_to([pg.get_center()[0], 1.6, 0])
            self.play(FadeIn(pg, shift=0.3 * DOWN), FadeIn(fname, shift=0.3 * DOWN),
                      run_time=min(1.2, 0.5 * c.until("from")))
            self.play(Write(line), run_time=min(1.5, 0.8 * c.until("from")))
            c.wait_until("from")
            key = select(line, "c4.nrev.3:end")[0]
            self.play(*recolor(key, YELLOW), FlashUnder(key, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("shape")

            # narration strip: 13 line boxes + end card
            n, bw, gap, sy = 13, 0.38, 0.08, -0.7
            x0 = -0.05
            lines = [Rectangle(width=bw, height=0.6).set_stroke(DIM, 2).set_fill(FG, 0.08)
                     .move_to([x0 + bw / 2 + i * (bw + gap), sy, 0]) for i in range(n)]
            endc = Rectangle(width=0.6, height=0.6).set_stroke(DIM, 2).set_fill(DIM, 0.25)
            endc.move_to([lines[-1].get_right()[0] + 0.12 + 0.3, sy, 0])
            endlab = T("end card", size=28, color=DIM)
            endlab.move_to([endc.get_right()[0] - endlab.width / 2, sy + 0.62, 0])
            self.play(LaggedStart(*[FadeIn(r) for r in lines + [endc]], lag_ratio=0.1),
                      FadeIn(endlab), run_time=1.2)

            def bar(xl, xr):
                return RoundedRectangle(corner_radius=0.12, width=xr - xl, height=0.36) \
                    .set_stroke(PURPLE, 2).set_fill(PURPLE, 0.55).move_to([(xl + xr) / 2, sy - 0.8, 0])
            b1 = bar(lines[0].get_left()[0], lines[1].get_right()[0])
            b2 = bar(lines[5].get_right()[0], lines[8].get_right()[0])
            b3 = bar(lines[11].get_left()[0], endc.get_right()[0])
            labs = [T(s, size=28, color=DIM).move_to([b.get_center()[0], sy - 1.4, 0])
                    for s, b in zip(["hook", "visual stretch", "recap"], (b1, b2, b3))]
            tie = DashedLine(line.get_bottom() + 0.1 * DOWN + (key.get_center()[0] - line.get_center()[0]) * RIGHT,
                             lines[5].get_corner(UR), dash_length=0.08).set_stroke(YELLOW, 2)
            self.play(Create(tie), lines[5].animate.set_stroke(YELLOW, 3), run_time=1.0)
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in (b1, b2, b3)], lag_ratio=0.35),
                      LaggedStart(*[FadeIn(lb, shift=0.2 * DOWN) for lb in labs], lag_ratio=0.35),
                      run_time=min(2.4, 0.9 * c.until("dry")))
            c.wait_until("dry")
            dry = [T("dry", size=30, color=DIM).move_to([(lines[a].get_left()[0] + lines[b].get_right()[0]) / 2,
                                                         sy - 0.8, 0]) for a, b in ((2, 5), (9, 10))]
            self.play(*[FadeIn(x, scale=0.8) for x in dry], run_time=0.8)

        # ---------------- c1.dir.4: builders
        with self.say("c1.dir.4") as c:
            d4, _, cs4 = self.unit(3.1, 2.1, 0.5, 0.72, 0.6, 0.14)
            bxs = row_xs(3.1, 8, 0.72, 0.14)
            b4 = [builder_box(0.72, 0.6, lit=False).move_to([x, 0.5, 0]) for x in bxs]
            sweep_clear(self, time_span(items[2].animate.set_color(DIM), 0.3, 1.2),
                        time_span(items[3].animate.set_color(YELLOW), 0.3, 1.2),
                        time_span(FadeIn(d4, *b4, *cs4), 0.5, 1.4),
                        keep=[*items, sub], run_time=1.4)
            c.wait_until("in one message")
            msg = T("one message, in the background", size=28, color=DIM).move_to([3.1, -0.45, 0])
            self.play(*[b.animate.set_stroke(BLUE, 3).set_fill(BLUE, 0.15) for b in b4],
                      FadeIn(msg, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("gets")

            legend = []
            for k, (s, y) in enumerate(zip(["project folder", "scene name", "≤ 3 lines of continuity"],
                                           [-1.4, -2.0, -2.6])):
                ic = page(0.28, 0.36, fold=0.1, stroke=2).move_to([0.75, y, 0])
                tx = T(s, size=30, color=TEAL)
                tx.move_to([1.1 + tx.width / 2, y, 0])
                legend.append(VGroup(ic, tx))
            self.play(LaggedStart(*[FadeIn(g, shift=0.2 * RIGHT) for g in legend], lag_ratio=0.3),
                      run_time=min(1.5, 0.4 * c.until("flow")))
            tags = []
            moves = []
            for b in b4:
                for k in range(3):
                    tg = page(0.13, 0.18, fold=0.05, stroke=1.5, fill_op=0.3)
                    tg.move_to(b.get_center() + (k - 1) * 0.2 * RIGHT)
                    tags.append(tg)
                    moves.append(TransformFromCopy(legend[k][0], tg))
            self.play(LaggedStart(*moves, lag_ratio=0.04), run_time=min(2.0, 0.8 * c.until("flow")))
            c.wait_until("flow")

            src, dst = b4[3], b4[4]
            card_t = T("position · size · colours", size=28, color=YELLOW)
            card_r = RoundedRectangle(corner_radius=0.1, width=card_t.width + 0.4, height=card_t.height + 0.35)
            card_r.set_stroke(YELLOW, 2).set_fill(BG, 1)
            card = VGroup(card_r, card_t).move_to([3.1, -0.7, 0])
            arc = CurvedArrow(src.get_bottom() + 0.05 * DOWN, dst.get_bottom() + 0.05 * DOWN, angle=PI / 2,
                              tip_length=0.15).set_stroke(YELLOW, 3)
            arc.get_tip().set_fill(YELLOW).set_stroke(YELLOW)
            self.play(FadeOut(msg), src.animate.set_stroke(YELLOW, 4), run_time=1.0)
            self.play(GrowFromPoint(card, src.get_bottom()), run_time=1.2)
            c.wait_until("reports")
            self.play(Create(arc), FadeOut(*legend), run_time=1.0)
            c.wait_until("to the next")
            self.play(card.animate.scale(0.1).move_to(dst.get_center()).set_opacity(0),
                      FlashAround(dst, run_time=1.2), run_time=1.2)
            self.remove(card)
            self.play(src.animate.set_stroke(BLUE, 3), FadeOut(arc), run_time=0.6)
            c.wait_until("share")

            walls = [Line([(a + b) / 2, 0.0, 0], [(a + b) / 2, 1.0, 0]).set_stroke(DIM, 2)
                     for a, b in zip(bxs[:-1], bxs[1:])]
            self.play(LaggedStart(*[GrowFromCenter(w) for w in walls], lag_ratio=0.1), run_time=1.2)
            c.wait_until("why")

            q = T("?", size=56, color=YELLOW).move_to([3.1, 3.12, 0])
            self.play(FadeIn(q, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("judgment")

            cen, R = np.array([3.1, -1.95, 0]), 1.3
            loop = VGroup()
            angs = [90, -30, 210]
            for a, s in zip(angs, ["review", "judge", "fix"]):
                loop.add(T(s, size=32, color=YELLOW if s == "review" else FG)
                         .move_to(cen + R * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0])))
            g = 36
            for a in angs:
                arcm = Arc(radius=R, start_angle=(a - g) * DEGREES, angle=-(120 - 2 * g) * DEGREES,
                           arc_center=cen).set_stroke(YELLOW, 3)
                arcm.add_tip(tip_length=0.16)
                arcm.get_tip().set_fill(YELLOW).set_stroke(YELLOW)
                loop.add(arcm)
            self.play(ReplacementTransform(q, loop),
                      items[3].animate.set_color(DIM), items[4].animate.set_color(YELLOW),
                      run_time=min(1.8, 0.8 * c.remaining))

        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
