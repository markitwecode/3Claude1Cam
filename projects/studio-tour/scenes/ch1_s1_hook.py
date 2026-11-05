"""Chapter 1, scene 1: Hook. Clips c1.hook.1 – c1.hook.2.

Plan: title card; the running example's finished frame (ch4_s3_trace at its 'answer' beat)
fills the screen; six small agents each wire into one part of it; it shrinks into tile 1 of
this video's eight scenes, each with its own agent behind a wall; the questions; one
narration sentence ('One, two, three, four.', the line spoken over that frame) arrows down
to the frame; the crew counted by role; a GOLD tag for part 2.
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
from lib.titles import title_card  # noqa: E402

FRAME_PNG = Path(__file__).resolve().parent.parent / "source" / "figures" / "final_ch4_s3_trace_frame.png"


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

# the big frame: 9.6 wide (1920 px -> 0.005 units/px), centred here
FW = 9.6
FC = np.array([0.0, -0.2, 0.0])
PX = FW / 1920

# this video's eight scene tiles
TILE_W, TILE_H, TILE_PITCH, TILE_Y = 1.3, 1.3 * 9 / 16, 1.56, 0.1
TILE_X = [(i - 3.5) * TILE_PITCH for i in range(8)]


def agent_box(w=0.9, h=0.6):
    """Ch1 shared look: an agent is a BLUE rounded box with a faint BLUE fill."""
    return RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)


def agent(label, size=38):
    lab = T(label, size, color=BLUE)
    box = agent_box(lab.width + 0.6, 0.8)
    lab.move_to(box)
    return VGroup(box, lab)


def px_rect(x0, x1, y0, y1, pad=0.06):
    """A thin BLUE outline round the image region x0..x1, y0..y1 (pixels of the 1920x1080 frame)."""
    left = FC[0] + (x0 - 960) * PX - pad
    right = FC[0] + (x1 - 960) * PX + pad
    top = FC[1] - (y0 - 540) * PX + pad
    bottom = FC[1] - (y1 - 540) * PX - pad
    r = RoundedRectangle(corner_radius=0.06, width=right - left, height=top - bottom)
    return r.set_stroke(BLUE, 2).set_fill(opacity=0).move_to([(left + right) / 2, (top + bottom) / 2, 0])


class Hook(NarratedScene):
    def construct(self):
        self.hook_one()
        self.hook_two()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c1.hook.1 ────────────────────────────────────────────────────────────────
    def hook_one(self):
        card = title_card("Part 1 · From a request to a finished video")
        if card.title.width > 12.6:
            card.title.scale_to_fit_width(12.6)
            card.arrange(DOWN, buff=0.45).move_to(ORIGIN)
            card.rule.shift(UP * 0.08)

        with self.say("c1.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),
                      run_time=c.until("a tour", floor=0.9))
            c.wait_until("a tour")
            self.play(FadeIn(card.course, shift=0.2 * DOWN), run_time=min(0.8, c.until("behind", floor=0.5)))
            c.wait_until("behind")
            self.play(FadeIn(card.part, shift=0.2 * DOWN), run_time=min(0.8, c.until("frame", floor=0.5)))
            c.wait_until("frame")

            # {frame}: the running example's finished frame fills the screen
            img = ImageMobject(str(FRAME_PNG))
            img.scale_to_fit_width(FW).move_to(FC)
            border = Rectangle(width=FW, height=img.height).set_stroke(DIM, 2).set_fill(opacity=0).move_to(FC)
            frame = Group(img, border)
            caption = Mono("ch4_s3_trace", 30, color=YELLOW)
            caption.next_to(border, UP, buff=0.18).align_to(border, LEFT)
            # a player's scrubber under it: the frame sits ~65% into its scene
            sy = border.get_bottom()[1] - 0.22
            sl, sr = FC[0] - FW / 2, FC[0] + FW / 2
            ph = sl + 0.65 * FW
            scrub = VGroup(Line([sl, sy, 0], [sr, sy, 0]).set_stroke(DIM, 3),
                           Line([sl, sy, 0], [ph, sy, 0]).set_stroke(FG, 3),
                           Dot([ph, sy, 0], radius=0.08, color=FG))
            sweep_clear(self, time_span(FadeIn(frame, scale=1.03), 0.4, 1.4),
                        time_span(FadeIn(scrub), 0.8, 1.4),
                        time_span(FadeIn(caption, shift=0.2 * DOWN), 1.0, 1.7), run_time=1.7)
            c.wait_until("nobody")

            # {nobody}: six small agents, each wired to one part of the frame
            lx, rx = -5.75, 5.75
            boxes = [agent_box().move_to([x, y, 0]) for x, y in
                     [(lx, 1.7), (rx, 1.7), (lx, -0.5), (rx, -0.5), (lx, -2.2), (rx, -2.4)]]
            targets = [
                px_rect(410, 1510, 85, 235),      # the code (the match lines)
                px_rect(290, 1215, 315, 392),     # a row (the first trace line)
                px_rect(290, 480, 432, 745),      # the colours (the yellow heads)
                px_rect(1065, 1745, 655, 740),    # one term of a row
                px_rect(290, 830, 885, 968),      # the result row
                Circle(radius=0.17).set_stroke(BLUE, 2).move_to([ph, sy, 0]),   # the timing
            ]
            ends = [targets[0].get_left(), targets[1].get_right(), targets[2].get_left(),
                    targets[3].get_right(), targets[4].get_left(), None]
            starts = [b.get_right() if b.get_x() < 0 else b.get_left() for b in boxes]
            d = starts[5] - targets[5].get_center()
            ends[5] = targets[5].get_center() + 0.17 * d / np.linalg.norm(d)
            wires = [Line(s, e).set_stroke(BLUE, 2) for s, e in zip(starts, ends)]
            anims = []
            for i, (b, w, t) in enumerate(zip(boxes, wires, targets)):
                t0 = 0.3 * i
                anims += [time_span(FadeIn(b, scale=0.8), t0, t0 + 0.6),
                          time_span(Create(w), t0 + 0.35, t0 + 1.0),
                          time_span(Create(t), t0 + 0.6, t0 + 1.2)]
            self.play(*anims, run_time=2.7)
            c.wait_until("same")

            # {same}: the frame becomes tile 1 of this video's eight scenes
            tiles = [Rectangle(width=TILE_W, height=TILE_H).set_stroke(DIM, 2).set_fill(DIM, 0.12)
                     .move_to([x, TILE_Y, 0]) for x in TILE_X[1:]]
            row_l = TILE_X[0] - TILE_W / 2
            row_r = TILE_X[-1] + TILE_W / 2
            mini = [agent_box(0.6, 0.4).move_to([x, TILE_Y - 0.95, 0]) for x in TILE_X]
            ties = [Line(m.get_top(), [m.get_x(), TILE_Y - TILE_H / 2, 0]).set_stroke(BLUE, 2) for m in mini]
            brace = span_brace(np.array([row_l, mini[0].get_bottom()[1], 0]),
                               np.array([row_r, mini[0].get_bottom()[1], 0]))
            label = T("this video", 32, color=DIM).next_to(brace, DOWN, buff=0.14)
            gone = boxes + wires + targets + [caption, scrub]
            self.play(*[time_span(FadeOut(m), 0, 0.7) for m in gone],
                      time_span(frame.animate.scale(TILE_W / FW).move_to([TILE_X[0], TILE_Y, 0]), 0.3, 1.8),
                      time_span(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.15), 0.8, 2.0),
                      time_span(GrowFromCenter(brace), 1.2, 2.0),
                      time_span(FadeIn(label, shift=0.2 * UP), 1.3, 2.0),
                      run_time=2.0)
            c.wait_until("built by")

            # each scene built by its own agent ...
            self.play(LaggedStart(*[FadeIn(m, shift=0.15 * UP) for m in mini], lag_ratio=0.12),
                      LaggedStart(*[Create(t) for t in ties], lag_ratio=0.12),
                      run_time=1.5)
            c.wait_until("never saw")

            # ... which never saw the others: walls between the tiles
            walls = [Line([(a + b) / 2, TILE_Y + 0.6, 0], [(a + b) / 2, mini[0].get_bottom()[1] - 0.05, 0])
                     .set_stroke(DIM, 2) for a, b in zip(TILE_X, TILE_X[1:])]
            self.play(LaggedStart(*[GrowFromCenter(w) for w in walls], lag_ratio=0.12),
                      run_time=min(1.3, c.until(floor=0.8)))

        self.frame, self.mini = frame, mini

    # ── c1.hook.2 ────────────────────────────────────────────────────────────────
    def hook_two(self):
        frame, mini = self.frame, self.mini
        q1 = T("who does what?", 44)
        q2 = T("in what order?", 44)
        VGroup(q1, q2).arrange(RIGHT, buff=1.5).move_to(UP * 2.8)

        # one sentence of the running example's narration, said over that very frame
        words = T("One, two, three, four.", 36, color=YELLOW)
        band = RoundedRectangle(corner_radius=0.12, width=words.width + 0.5, height=0.64)
        band.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.08)
        band.move_to([TILE_X[0] - TILE_W / 2 + band.width / 2, 1.55, 0])
        words.move_to(band)
        one = select(words, "One,")[0]
        tick = Line([one.get_left()[0], band.get_top()[1] - 0.12, 0],
                    [one.get_left()[0], band.get_top()[1] + 0.22, 0]).set_stroke(YELLOW, 4)
        arrow = Arrow([one.get_x(), band.get_bottom()[1], 0], [one.get_x(), TILE_Y + TILE_H / 2, 0],
                      buff=0.06, stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.35)

        # the crew, counted by role
        planner, writer, director, builder = (agent(s) for s in ("planner", "writer", "director", "builder"))
        wd = VGroup(writer, director).arrange(RIGHT, buff=0.35)
        VGroup(planner, wd, builder).arrange(RIGHT, buff=0.9).move_to(UP * 2.6)
        per_chapter = T("per chapter", 30, color=DIM).next_to(wd, DOWN, buff=0.2)
        per_scene = T("per scene", 30, color=DIM).next_to(builder, DOWN, buff=0.2)
        per_scene.align_to(per_chapter, DOWN)   # same baseline (both end in a "p" descender)

        tag_text = T("Part 2 · what it costs, where to cut", 30, color=GOLD)
        tag_box = RoundedRectangle(corner_radius=0.15, width=tag_text.width + 0.5, height=tag_text.height + 0.4)
        tag_box.set_stroke(GOLD, 2).set_fill(GOLD, 0.08)
        tag = VGroup(tag_box, tag_text.move_to(tag_box)).move_to(DOWN * 3.3)

        with self.say("c1.hook.2", gap=0.9) as c:   # a still beat on the part-2 tag before the fade
            self.play(FadeIn(q1, shift=0.3 * DOWN), run_time=min(1.0, c.until("in what order", floor=0.6)))
            c.wait_until("in what order")
            self.play(FadeIn(q2, shift=0.3 * DOWN), run_time=min(1.0, c.until("sync", floor=0.6)))
            c.wait_until("sync")

            # {sync}: a sentence, as a strip of words ...
            self.play(FadeIn(band), FadeIn(words, lag_ratio=0.15), run_time=min(1.6, c.until("an animation", floor=1.0)))
            c.wait_until("an animation")
            # ... one word ticked, and that word becomes the frame
            self.play(Create(tick), GrowArrow(arrow), run_time=1.2)
            self.play(FlashAround(frame[1], color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until("crew")

            # {crew}: the question becomes the answer
            self.play(FadeTransform(q1, planner), FadeOut(q2), run_time=1.4)
            c.wait_until("a writer")
            # the strip clears just before "per chapter" needs its corner
            self.play(*[time_span(FadeOut(m), 0, 0.6) for m in (band, words, tick, arrow)],
                      time_span(LaggedStart(FadeIn(writer, shift=0.2 * DOWN), FadeIn(director, shift=0.2 * DOWN),
                                            lag_ratio=0.3), 0.2, 1.4),
                      time_span(FadeIn(per_chapter, shift=0.2 * DOWN), 0.7, 1.5), run_time=1.5)
            c.wait_until("a builder")
            self.play(FadeIn(builder, shift=0.2 * DOWN), time_span(FadeIn(per_scene, shift=0.2 * DOWN), 0.4, 1.2),
                      time_span(LaggedStart(*flash(mini, color=BLUE, run_time=1.0), lag_ratio=0.1), 0.5, 2.0),
                      run_time=2.0)
            c.wait_until("next")

            # {next}: where part two goes
            self.play(FadeIn(tag, shift=0.2 * UP), run_time=1.0)
