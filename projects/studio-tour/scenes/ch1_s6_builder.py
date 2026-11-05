"""Chapter 1, scene 6: inside a scene-builder (context bar, the loop, vk check, the beats image). Clips c1.build.1 - c1.build.5.

Context bar (ch2 opens on it): GOLD, x=-6.1 (centre), width 0.8, bottom y=-3.2, segments fill GOLD 0.9,
BG separators (stroke 3); kit 1.9 tall, packet 0.45, then file .45 / check output .45 / image .9, then a
second unlabeled pass; labels T 28 left-aligned at x=-5.5; "context" GOLD under the bar.
Loop ring: built in c1.build.2 by make_ring(C=(3.9,-1.45), R=1.6); small copy in c1.build.5 at (2.6, 0.6), R=1.3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# Manim CE 0.22's Camera.display_image_mobject pastes into Image.fromarray(np.zeros((h, w)),
# mode="RGBA"), which Pillow 13 rejects ("Invalid mode for data type"), so no ImageMobject
# renders. Shim just that call (a blank RGBA canvas, which is what it meant) for this module.
def _patch_image_canvas():
    import manim.camera.camera as cam
    from PIL import Image as PILImage

    class _ImageShim:
        def __getattr__(self, name):
            return getattr(PILImage, name)

        @staticmethod
        def fromarray(arr, mode=None):
            if mode == "RGBA" and getattr(arr, "ndim", 0) == 2:
                return PILImage.new("RGBA", (arr.shape[1], arr.shape[0]), (0, 0, 0, 0))
            return PILImage.fromarray(arr, mode=mode) if mode else PILImage.fromarray(arr)

    if cam.Image is PILImage:
        cam.Image = _ImageShim()


_patch_image_canvas()

FIG = Path(__file__).resolve().parent.parent / "source" / "figures"
AGENT_FILL = interpolate_color(ManimColor(BG), ManimColor(BLUE), 0.15)
TOOL_FILL = interpolate_color(ManimColor(BG), ManimColor(DIM), 0.15)
PAGE_FILL = interpolate_color(ManimColor(BG), ManimColor(TEAL), 0.12)

BAR_X, BAR_W, BAR_BOTTOM = -6.1, 0.8, -3.2
LAB_X = -5.5


def node(label, w, kind="agent", size=28, color=None, h=0.8):
    """agent: BLUE box, T label; tool: DIM outline, Mono label."""
    if kind == "agent":
        col = color or BLUE
        r = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(col, 3)
        r.set_fill(AGENT_FILL, 1)
        t = T(label, size)
    else:
        col = DIM
        r = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(DIM, 3)
        r.set_fill(TOOL_FILL, 1)
        t = Mono(label, size)
    t.move_to(r)
    return VGroup(r, t)


def page(w, h, label=None, size=28, color=TEAL, mono=True, fold=0.28):
    f = min(fold, h / 2)
    pts = [(-w / 2, h / 2), (w / 2 - f, h / 2), (w / 2, h / 2 - f), (w / 2, -h / 2), (-w / 2, -h / 2)]
    body = Polygon(*[[x, y, 0] for x, y in pts]).set_stroke(color, 3)
    body.set_fill(interpolate_color(ManimColor(BG), ManimColor(color), 0.12), 1)
    crease = VMobject().set_points_as_corners(
        [[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0]]).set_stroke(color, 3)
    g = VGroup(body, crease)
    if label:
        t = (Mono if mono else T)(label, size, color=FG)
        t.move_to(body.get_center() + LEFT * 0.08)
        g.add(t)
    return g


def circ(C, R, deg):
    a = np.radians(deg)
    return np.array([C[0] + R * np.cos(a), C[1] + R * np.sin(a), 0])


def exit_angle(C, R, deg, hw, hh, step, pad=0.1):
    """walk from node angle along the ring (step degrees) until outside the node rectangle."""
    centre = circ(C, R, deg)
    a = deg
    for _ in range(400):
        p = circ(C, R, a)
        if abs(p[0] - centre[0]) > hw + pad or abs(p[1] - centre[1]) > hh + pad:
            return a
        a += step
    return a


def make_ring(C, R, nodes, speed=1.3):
    """nodes: three mobjects, centred on the ring at 180, 60, -60 degrees. Returns (arcs, dot)."""
    angs = [180, 60, -60, -180]
    arcs = []
    for i in range(3):
        n_a, n_b = nodes[i], nodes[(i + 1) % 3]
        s = exit_angle(C, R, angs[i], n_a.width / 2, n_a.height / 2, -1)
        e = exit_angle(C, R, angs[i + 1], n_b.width / 2, n_b.height / 2, +1, pad=0.18)
        arc = Arc(radius=R, start_angle=np.radians(s), angle=np.radians(e - s), arc_center=C)
        arc.set_stroke(FG, 3)
        arc.add_tip(tip_length=0.2, tip_width=0.2)
        arcs.append(arc)
    dot = Dot(circ(C, R, 180), radius=0.13, color=YELLOW).set_z_index(5)
    dot.ang = 180.0

    def upd(m, dt):
        m.ang -= np.degrees(speed * dt)
        m.move_to(circ(C, R, m.ang))
    dot.add_updater(upd)
    return arcs, dot


class Builder(NarratedScene):
    def construct(self):
        # ---------- shared pieces ----------
        builder = node("scene-builder\nch4_s3_trace", 3.1, "agent", 30, h=1.15)
        builder[1].set_color(FG)
        bl = builder[1]
        for tk in select(bl, "ch4_s3_trace"):
            tk.set_color(YELLOW)
        builder.move_to([-4.95, 3.0, 0])

        def seg(bottom, h):
            return (Rectangle(width=BAR_W, height=h).set_fill(GOLD, 0.9).set_stroke(BG, 3)
                    .move_to([BAR_X, bottom + h / 2, 0]))

        def lab(text, s, color=FG, size=28):
            return T(text, size, color=color).move_to([LAB_X, s.get_center()[1], 0], aligned_edge=LEFT)

        keep = [builder]

        # ================= c1.build.1 =================
        with self.say("c1.build.1") as c:
            self.play(FadeIn(builder, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("bar")
            tiny = seg(BAR_BOTTOM, 0.25)
            ctx = T("context", 28, color=GOLD).move_to([BAR_X, BAR_BOTTOM - 0.35, 0])
            self.play(GrowFromEdge(tiny, DOWN), FadeIn(ctx, shift=0.2 * UP), run_time=1.2)
            c.wait_until("kit")
            kit = seg(BAR_BOTTOM, 1.9)
            kit_top = BAR_BOTTOM + 1.9
            kit_lab = T("kit (system prompt)", 28).move_to([LAB_X, kit_top - 0.3, 0], aligned_edge=LEFT)
            self.play(ReplacementTransform(tiny, kit), FadeIn(kit_lab, shift=0.2 * RIGHT), run_time=1.5)
            c.wait_until("comes from the cache")
            cached = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=0.5).set_stroke(GREEN, 2),
                            T("cached", 28, color=GREEN))
            cached[1].move_to(cached[0])
            cached.move_to([LAB_X, kit_top - 1.0, 0], aligned_edge=LEFT)
            self.play(GrowFromCenter(cached), run_time=0.8)
            c.wait_until("packet")
            pk_bottom = kit_top
            pk = seg(pk_bottom, 0.45)
            pk_lab = lab("packet ≈1k", pk)
            icon = page(0.5, 0.65).move_to([-3.0, pk.get_center()[1], 0])
            self.play(GrowFromEdge(pk, DOWN), FadeIn(pk_lab, shift=0.2 * RIGHT), FadeIn(icon), run_time=1.0)

            rows = ["SCENE ch4_s3_trace: Tracing append",
                    "neighbours: ch4_s2_code | ch4_s4_cells",
                    "…",
                    "[c4.trace.2] 18.2 s",
                    "    0.0  {pending} Look at what has piled up.",
                    "…",
                    "   12.0  {done} Three onto four, then two, then one. ⏸",
                    "   15.4  {answer} One, two, three, four."]
            ptxt = Mono("\n".join(rows), 26, t2c={"…": DIM}, line_spacing=0.8)
            big = page(12.1, 4.0)
            big.move_to([0.6, 0.4, 0]).set_z_index(4)
            ptxt.set_z_index(5)
            ptxt.move_to(big[0].get_center() + LEFT * 0.1)
            self.play(ReplacementTransform(icon, big), pk_lab.animate.set_opacity(0), kit_lab.animate.set_opacity(0), run_time=1.3)
            self.play(FadeIn(ptxt, lag_ratio=0.1), run_time=1.0)
            c.wait_until("the brief")
            self.play(FlashAround(select(ptxt, "SCENE ch4_s3_trace: Tracing append")[0], buff=0.03), run_time=1.3)
            c.wait_until("start time")
            self.play(FlashAround(select(ptxt, "12.0")[0], buff=0.03), FlashAround(select(ptxt, "15.4")[0], buff=0.03), run_time=1.3)
            c.wait_until("neighbouring scenes")
            self.play(FlashAround(select(ptxt, "neighbours: ch4_s2_code | ch4_s4_cells")[0], buff=0.03), run_time=1.0)
        keep += [kit, kit_lab, cached, pk, pk_lab, ctx]
        bar_segs = [kit, pk]
        bar_labs = [kit_lab, cached, pk_lab, ctx]

        # ================= c1.build.2 =================
        with self.say("c1.build.2") as c:
            docs = []
            names = ["docs", "whole script", "other scenes", "engine source"]
            spots = [[1.2, 1.9], [4.4, 1.9], [1.2, 0.3], [4.4, 0.3]]
            for nm, sp in zip(names, spots):
                docs.append(page(2.7, 1.1, nm, 28, color=DIM, mono=False).move_to([sp[0], sp[1], 0]))
            self.play(FadeOut(big), FadeOut(ptxt), pk_lab.animate.set_opacity(1), kit_lab.animate.set_opacity(1),
                      LaggedStart(*[FadeIn(d, shift=0.2 * DOWN) for d in docs], lag_ratio=0.5),
                      run_time=min(3.6, c.until("told") + 3.6))
            crosses = [cross_mark(RED, r=0.3).move_to(d) for d in docs]
            for x in crosses:
                x.set_z_index(6)
            self.play(*[d.animate.shift(LEFT * 0.8) for d in docs],
                      *[x.animate.shift(LEFT * 0.8) for x in []],
                      *[GrowFromCenter(x) for x in crosses], run_time=1.0)
            for x, d in zip(crosses, docs):
                x.move_to(d)
            c.wait_until("distilled")
            tgt = np.array([BAR_X, kit.get_center()[1], 0])
            self.play(LaggedStart(*[AnimationGroup(d.animate.scale(0.15).move_to(tgt),
                                                   x.animate.scale(0.15).move_to(tgt))
                                    for d, x in zip(docs, crosses)], lag_ratio=0.25),
                      run_time=2.2)
            self.remove(*docs, *crosses)
            sig = T("complete signatures", 28, color=DIM).move_to([LAB_X, kit_top - 1.7, 0], aligned_edge=LEFT)
            c.wait_until("complete signatures")
            self.play(FadeIn(sig, shift=0.2 * RIGHT), run_time=1.0)
            bar_labs.append(sig)
            keep.append(sig)

            # ---- the loop ----
            C = np.array([3.9, -1.45, 0])
            R = 1.6
            c.wait_until("design")
            n_design = node("design once", 2.3)
            n_design.move_to([1.4, 2.9, 0])
            self.play(FadeIn(n_design, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("one visual change")
            note = T("≈ 1 change per 8 words\n· layout\n· a cue per change", 28, color=DIM, line_spacing=0.8)
            note.move_to([2.7, 2.9, 0], aligned_edge=LEFT)
            self.play(FadeIn(note, shift=0.2 * RIGHT), run_time=1.2)
            c.wait_until("write")
            n_write = node("write the whole file", 3.9).move_to([1.4, 1.3, 0])
            a1 = Arrow([1.4, 2.5, 0], [1.4, 1.7, 0], buff=0, stroke_width=3, tip_length=0.2, color=FG)
            self.play(GrowArrow(a1), FadeIn(n_write, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("check")
            n_check = node("vk check", 1.9, "tool").move_to(circ(C, R, 180))
            n_beats = page(2.9, 0.8, "beats image", 28).move_to(circ(C, R, 60))
            n_fix = node("fix, all at once", 3.2).move_to(circ(C, R, -60))
            for n_ in (n_check, n_beats, n_fix):
                n_.set_z_index(3)
            arcs, dot = make_ring(C, R, [n_check, n_beats, n_fix])
            a2 = Arrow([1.8, 0.9, 0], [1.8, -1.1, 0], buff=0, stroke_width=3, tip_length=0.2, color=FG)
            self.play(GrowArrow(a2), FadeIn(n_check, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("beats")
            self.play(Create(arcs[0]), FadeIn(n_beats, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("fix")
            self.play(Create(arcs[1]), FadeIn(n_fix, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("again")
            self.play(Create(arcs[2]), FadeIn(dot), run_time=1.0)
        loop_parts = [n_design, note, a1, n_write, a2, n_beats, n_fix, *arcs]

        # ================= c1.build.3 =================
        with self.say("c1.build.3") as c:
            dot.clear_updaters()
            p1 = node("1 · dry run (lint)", 3.7, "agent", 28).move_to([-0.65, 3.0, 0])
            p1[0].set_stroke(DIM, 3)
            p2 = node("2 · render + beats image", 4.7, "agent", 28).move_to([4.25, 3.0, 0])
            p2[0].set_stroke(DIM, 3)
            arr12 = Arrow([1.2, 3.0, 0], [1.9, 3.0, 0], buff=0, stroke_width=3, tip_length=0.2, color=FG)
            self.play(*[FadeOut(m) for m in loop_parts], FadeOut(dot), run_time=1.0)
            self.play(n_check.animate.scale(1.25).move_to([0.6, 0.6, 0]), run_time=1.0)
            self.play(ReplacementTransform(n_check.copy(), p1), TransformFromCopy(n_check, p2),
                      GrowArrow(arr12), run_time=1.6)
            self.remove(n_check)
            c.wait_until("looks")
            items = []
            texts = ["errors", "overruns", "read-twice time", "cut off · overlapping · small text"]
            cues = ["errors", "overruns", "text removed", "cut off"]
            y = 2.05
            for tx, cu in zip(texts, cues):
                it = T(tx, 30).move_to([-2.5, y, 0], aligned_edge=LEFT)
                y -= 0.55
                c.wait_until(cu)
                self.play(FadeIn(it, shift=0.2 * RIGHT), run_time=0.8)
                items.append(it)
            c.wait_until("hard")
            for tx, cu in zip(["hard-coded times", "empty last frame"], ["hard", "scene that ends"]):
                it = T(tx, 30).move_to([-2.5, y, 0], aligned_edge=LEFT)
                y -= 0.55
                c.wait_until(cu)
                self.play(FadeIn(it, shift=0.2 * RIGHT), run_time=0.8)
                items.append(it)

            c.wait_until("output")
            dw = lambda a_, b_, d_, fo: [f"  dwell: t= {a_} '{b_}' shown {d_} (needs 4.1)",
                                         f"        FadeOut during c4.trace.2 @{fo}"]
            l1 = dw("36.6", "[part of] 1::(2::(3::[4]))", "1.5s", '11.9s "…from the inside out."')
            l2 = dw("37.7", "[part of] 1::(2::[3;4])", "0.1s", '12.9s "…out. Three onto four,"')
            lines = ["ch4_s3_trace (TracingAppend): 65.0 s (narration 60.6 s, 3 clips)", *l1, *l1, *l2, *l2, "(5 s)"]
            otxt = Mono("\n".join(lines), 19, t2c={"dwell:": GOLD}, line_spacing=0.5)
            opage = page(11.6, 3.2).move_to([0.6, 0.8, 0])
            otxt.move_to(opage[0].get_center() + LEFT * 0.1)
            self.play(*[FadeOut(i) for i in items], FadeIn(opage), run_time=0.8)
            self.play(FadeIn(otxt, lag_ratio=0.05), run_time=1.2)
            c.wait_until("flags like these")
            tag = T("dwell: a note · the render goes ahead", 28, color=DIM).move_to([2.6, -1.35, 0])
            self.play(FadeIn(tag, shift=0.2 * UP), run_time=1.0)

            c.wait_until("stop")
            fixb = node("fix", 1.3).move_to([-0.65, 0.0, 0])
            a_fix = Arrow([-0.65, 2.65, 0], [-0.65, 0.4, 0], buff=0, stroke_width=3, tip_length=0.2, color=RED)
            bar = Rectangle(width=0.16, height=1.0).set_fill(RED, 1).set_stroke(RED, 0).move_to([1.55, 5.0, 0])
            bar.set_z_index(5)
            rlab = T("overrun · sync · layout:\nno render, no image", 30, color=RED, line_spacing=0.8)
            rlab.move_to([2.9, 1.5, 0])
            self.play(FadeOut(opage), FadeOut(otxt), FadeOut(tag),
                      bar.animate.move_to([1.55, 3.0, 0]), run_time=0.7)
            self.play(FadeIn(rlab, shift=0.2 * UP), GrowArrow(a_fix), FadeIn(fixb), run_time=1.4)
            c.wait_until("anyway")
            ra = Mono("--render-anyway", 30, color=YELLOW).move_to([2.9, 1.7, 0])
            ra_note = T("a flag the brief really demands", 28, color=DIM).move_to([2.9, 0.9, 0])
            self.play(bar.animate.move_to([1.55, 5.0, 0]), FadeOut(rlab), FadeOut(a_fix), FadeOut(fixb),
                      run_time=1.0)
            self.play(FadeIn(ra, shift=0.2 * UP), FadeIn(ra_note, shift=0.2 * UP), run_time=1.0)
            self.remove(bar)

        # ================= c1.build.4 =================
        with self.say("c1.build.4") as c:
            img = ImageMobject(np.array(Image.open(FIG / "ch4_s3_trace_beats.png").convert("RGBA")))
            IW = 8.0
            img.set(width=IW).move_to([2.6, -0.45, 0])
            IH = img.height

            def ip(px, py):
                return np.array([2.6 + (px / 1720 - 0.5) * IW, -0.45 + (0.5 - py / 972) * IH, 0])

            tag480 = T("480p", 32, color=GOLD).move_to([5.6, 2.25, 0])
            self.play(p1.animate.set_opacity(0.4),
                      p2[0].animate.set_stroke(GOLD, 3).set_fill(GOLD, 0.2), run_time=0.8)
            self.wait(1.2)
            cover = Rectangle(width=ip(1720, 0)[0] - ip(862, 0)[0], height=ip(0, 972)[1] - ip(0, 730)[1] if False else ip(0, 730)[1] - ip(0, 972)[1])
            cover.set_fill(BG, 1).set_stroke(BG, 0).move_to((ip(862, 730) + ip(1720, 972)) / 2).set_z_index(1)
            self.play(FadeOut(ra), FadeOut(ra_note), FadeIn(cover), FadeIn(tag480, shift=0.2 * DOWN),
                      UpdateFromAlphaFunc(img, lambda m, a: m.set_opacity(a)), run_time=1.2)
            c.wait_until("label")
            ul = Line(ip(1299, 478), ip(1468, 478), color=YELLOW, stroke_width=5)
            self.play(Create(ul), run_time=1.0)
            c.wait_until("tile")
            arr = np.array(Image.open(FIG / "ch4_s3_trace_beats.png").convert("RGB"))[244:484, 1292:1720]
            tile = ImageMobject(np.dstack([arr, np.full(arr.shape[:2], 255, dtype=np.uint8)]))
            tw = ip(1720, 0)[0] - ip(1292, 0)[0]
            tile.set(width=tw).move_to((ip(1292, 244) + ip(1720, 484)) / 2)
            frame0 = Rectangle(width=tile.width, height=tile.height).set_stroke(YELLOW, 4).move_to(tile)
            tgt_w = 5.8
            tile_c = np.array([3.5, 0.3, 0])
            frame1 = Rectangle(width=tgt_w, height=tgt_w * tile.height / tile.width).set_stroke(YELLOW, 4)
            frame1.move_to(tile_c)
            self.add(tile)
            self.play(FadeIn(frame0), run_time=0.5)
            self.play(UpdateFromAlphaFunc(img, lambda m, a: m.set_opacity(1 - 0.8 * a)), FadeOut(ul), FadeOut(tag480),
                      tile.animate.set(width=tgt_w).move_to(tile_c),
                      Transform(frame0, frame1), run_time=1.6)
            tile.set_z_index(2)
            frame0.set_z_index(3)
            c.wait_until("said")
            said_prev = T("Three onto four, then two, then one.", 28, color=DIM).move_to([3.5, -1.7, 0])
            said = T("One, two, three, four.", 38, color=YELLOW).move_to([3.5, -2.35, 0])
            said.set_z_index(10)
            said_prev.set_z_index(10)
            self.play(FadeIn(said_prev, shift=0.2 * UP), run_time=1.0)
            self.play(FadeIn(said, shift=0.2 * UP), run_time=1.0)
            c.wait_until("green")
            gx = tile_c[0] - tgt_w / 2
            gs = tgt_w / 428
            gtop = tile_c[1] + frame1.height / 2
            gbox = Rectangle(width=122 * gs, height=21 * gs).move_to(
                [gx + (65 + 61) * gs, gtop - (196 + 10.5) * gs, 0]).set_stroke(opacity=0)
            self.play(FlashAround(gbox, color=GREEN, run_time=2, time_width=1.5, buff=0.08))
            c.wait_until("judge")
            judge = T("does each tile show what is being said?", 28, color=DIM).move_to([3.3, -3.2, 0])
            self.play(FadeIn(judge, shift=0.2 * UP), run_time=1.0)

        # ================= c1.build.5 =================
        with self.say("c1.build.5") as c:
            C2 = np.array([2.6, 0.6, 0])
            R2 = 1.3
            s_check = node("", 0.7, "tool").scale(0.7).move_to(circ(C2, R2, 180))
            s_beats = page(0.8, 0.45).move_to(circ(C2, R2, 60))
            s_fix = node("", 0.8, "agent").scale(0.7).move_to(circ(C2, R2, -60))
            for n_ in (s_check, s_beats, s_fix):
                n_.set_z_index(3)
            sarcs, sdot = make_ring(C2, R2, [s_check, s_beats, s_fix])
            anchor = np.array([-0.9, -1.5, 0])
            num = Integer(0, font_size=48, color=GOLD)
            num.add_updater(lambda m: m.move_to(anchor, aligned_edge=RIGHT))
            rest = T(" turns (median) · ≈5 check runs", 32, color=GOLD).move_to(anchor + RIGHT * 0.1, aligned_edge=LEFT)
            rest.shift(DOWN * 0.0)
            sweep_clear(self, FadeIn(s_check), FadeIn(s_beats), FadeIn(s_fix),
                        *[Create(a) for a in sarcs], FadeIn(sdot), FadeIn(rest), FadeIn(num),
                        keep=keep, run_time=1.4)
            self.play(ChangeDecimalToValue(num, 25), run_time=min(3.2, c.until("grow") - 1.0), rate_func=linear)
            num.clear_updaters()
            num.move_to(anchor, aligned_edge=RIGHT)

            c.wait_until("grow")
            h = [0.45, 0.45, 0.9]
            names = ["file", "check output", "image 2–4k"]
            cues = ["the file", "the check output", "an image"]
            bottom = pk.get_top()[1]
            for hh, nm, cu in zip(h, names, cues):
                s = seg(bottom, hh)
                lb = lab(nm, s)
                c.wait_until(cu)
                self.play(GrowFromEdge(s, DOWN), FadeIn(lb, shift=0.2 * RIGHT), run_time=0.9)
                bottom += hh
                bar_segs.append(s)
                bar_labs.append(lb)
                keep += [s, lb]
            p2s = []
            for hh in (0.25, 0.25, 0.5):
                s = seg(bottom, hh)
                bottom += hh
                p2s.append(s)
            self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in p2s], lag_ratio=0.4), run_time=1.2)
            bar_segs += p2s
            keep += p2s
            c.wait_until("stays")
            allbar = VGroup(*bar_segs)
            self.play(FlashAround(allbar, color=GOLD, run_time=1.8, time_width=1.5, buff=0.15))
            c.wait_until("report")
            rep = page(3.6, 1.1, "report ≤ 12 lines", 28, mono=False).move_to([-1.5, 3.0, 0])
            self.play(FadeIn(rep, shift=0.3 * LEFT), run_time=0.6)
            self.play(rep.animate.shift(UP * 3.2), run_time=1.6, rate_func=rush_from)
            self.remove(rep)
        sdot.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
