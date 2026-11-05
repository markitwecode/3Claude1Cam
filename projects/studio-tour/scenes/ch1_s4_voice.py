"""Chapter 1, scene 4: vk voice, a voice that costs no tokens. Clips c1.voice.1 – c1.voice.4.

Shared timeline (c1.voice.4, reused by s7): build_timeline() below. Axis Line from (-5.5, -0.5) to
(5.5, -0.5), DIM, stroke 4, scale U = 11 / 18.2 units per second. GOLD start ticks (stroke 4,
y -0.66..-0.34) at 0.0 2.2 6.5 12.0 15.4 with T 30 GOLD numbers 0.12 below; DIM end tick and T 28 DIM
"18.2 s" at x 5.5. YELLOW pins (stroke 2.5) up from the axis, heights 1.35 / 0.75 alternating
({pending} high), Mono 28 YELLOW label whose left edge sits on the pin, 0.08 above its top.
"""
import sys
import textwrap
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SENTENCES = [
    "Look at what has piled up.",
    "The one, the two and the three are each waiting to be consed on.",
    "Only now, with the first list used up, can the conses actually happen, from the inside out.",
    "Three onto four, then two, then one.",
    "One, two, three, four.",
]
STARTS = [0.0, 2.2, 6.5, 12.0, 15.4]
MARKS = ["pending", "conses", "finally", "done", "answer"]
CLIP_LEN = 18.2
GAP = 0.55
AX_L, AX_R = -5.5, 5.5
U = (AX_R - AX_L) / CLIP_LEN
LINE_Y = -1.2      # the joined waveform
AX_Y = -0.5        # the timeline axis
TOP_Y = 3.25       # tag · vk voice · note


# ---------------------------------------------------------------- shared look
def tool_box(label, w, h):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h)
    box.set_stroke(DIM, 2.5).set_fill(BLUE, 0.15)
    return VGroup(box, label.move_to(box))


def agent_box(text, w, h, size=32):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h)
    box.set_stroke(BLUE, 2.5).set_fill(BLUE, 0.15)
    return VGroup(box, T(text, size).move_to(box))


def page(w=0.6, h=0.78, fold=0.18, color=TEAL):
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - fold, 0],
                   [w / 2 - fold, h / 2, 0], [-w / 2, h / 2, 0])
    body.set_stroke(color, 3).set_fill(color, 0.15)
    crease = VMobject().set_points_as_corners([[w / 2 - fold, h / 2, 0], [w / 2 - fold, h / 2 - fold, 0],
                                               [w / 2, h / 2 - fold, 0]])
    crease.set_stroke(color, 2.5)
    return VGroup(body, crease)


def wave(seconds, seed, amp=0.35, color=BLUE):
    """Bars of a speech-like waveform, `seconds` long at the timeline scale, left edge at x = 0."""
    rng = np.random.default_rng(seed)
    w = seconds * U
    n = max(8, int(round(w / 0.075)))
    xs = np.linspace(0, w, n)
    env = 0.3 + 0.7 * np.abs(np.sin(rng.uniform(7, 9) * xs + rng.uniform(0, PI)))
    taper = np.clip(np.minimum(xs, w - xs) / 0.18, 0.25, 1.0)
    hs = np.maximum(amp * env * taper * rng.uniform(0.45, 1.0, n), 0.03)
    return VGroup(*[Line([x, -hh, 0], [x, hh, 0], stroke_width=3.2, color=color) for x, hh in zip(xs, hs)])


def span(i):
    return STARTS[i], (STARTS[i + 1] - GAP) if i < 4 else CLIP_LEN


def ear_icon(color=YELLOW):
    """Headphones: a headband arc and two filled ear cups (reads as listening)."""
    band = Arc(radius=0.38, start_angle=0, angle=PI, stroke_color=color, stroke_width=5)
    cups = VGroup(*[RoundedRectangle(corner_radius=0.07, width=0.18, height=0.36)
                    .set_stroke(color, 2).set_fill(color, 1).move_to([sx * 0.38, -0.1, 0]) for sx in (-1, 1)])
    return VGroup(band, cups).scale(1.2)


def build_timeline():
    """The c4.trace.2 timeline (shared with s7). Returns axis, ticks, nums, end tick, end label, pins, labels."""
    axis = Line([AX_L, AX_Y, 0], [AX_R, AX_Y, 0], color=DIM, stroke_width=4)
    ticks, nums, pins, labs = [], [], [], []
    for k, (s, m) in enumerate(zip(STARTS, MARKS)):
        x = AX_L + U * s
        tk = Line([x, AX_Y - 0.16, 0], [x, AX_Y + 0.16, 0], color=GOLD, stroke_width=4)
        ticks.append(tk)
        nums.append(T(f"{s:.1f}", 30, GOLD).next_to(tk, DOWN, buff=0.12))
        h = 1.35 if k % 2 == 0 else 0.75
        pin = Line([x, AX_Y, 0], [x, AX_Y + h, 0], color=YELLOW, stroke_width=2.5)
        pins.append(pin)
        labs.append(Mono("{" + m + "}", 28, YELLOW).next_to(pin.get_end(), UP, buff=0.08, aligned_edge=LEFT))
    end_tick = Line([AX_R, AX_Y - 0.16, 0], [AX_R, AX_Y + 0.16, 0], color=DIM, stroke_width=4)
    end_lab = T("18.2 s", 28, DIM).next_to(end_tick, DOWN, buff=0.12)
    return axis, ticks, nums, end_tick, end_lab, pins, labs


class VoiceScene(NarratedScene):
    def construct(self):
        self.top()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------ fixed header
    def top(self):
        self.tag = Mono("[c4.trace.2]", 28, YELLOW).move_to([-4.6, TOP_Y, 0])
        self.vk = tool_box(Mono("vk voice", 32), 2.8, 0.7).move_to([0, TOP_Y, 0])
        self.note = T("local GPU · no tokens", 30, GREEN).next_to(self.vk, RIGHT, buff=0.4)
        # the joined waveform, one segment per sentence, on the timeline's scale
        self.segs = []
        for i in range(5):
            a, b = span(i)
            self.segs.append(wave(b - a, seed=10 + i).shift([AX_L + U * a, LINE_Y, 0]))

    def header(self):
        return [self.tag, self.vk, self.note]

    # ------------------------------------------------------------ c1.voice.1
    def clip1(self):
        para = Mono("\n".join(textwrap.wrap(" ".join(SENTENCES), 46)), 28).move_to([0, -0.1, 0])
        texts = [Mono("\n".join(textwrap.wrap(s, 48)), 28) for s in SENTENCES]
        strips = []
        for t in texts:
            r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.4, height=t.height + 0.3)
            r.set_stroke(DIM, 1.5).set_fill(FG, 0.05)
            t.move_to(r)
            strips.append(VGroup(r, t))
        VGroup(*strips).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0, -0.15, 0])

        # conveyor layout: strip column | Chatterbox Turbo | waveform rows
        col = VGroup(*[s.copy() for s in strips]).scale(0.4)
        col.move_to([0, -0.4, 0]).align_to(np.array([-6.5, 0, 0]), LEFT)
        chat = tool_box(VGroup(Mono("Chatterbox", 28), Mono("Turbo", 28)).arrange(DOWN, buff=0.12), 2.8, 1.25)
        chat.move_to([col.get_right()[0] + 0.5 + 1.4, -0.4, 0])
        ref = page().move_to([chat.get_x(), 1.6, 0])
        ref_lab = Mono("ref_c.wav", 28).next_to(ref, RIGHT, buff=0.2)
        ref_note = T("one reference recording", 28, DIM).next_to(ref, LEFT, buff=0.3)
        ref_arrow = Arrow(ref.get_bottom(), chat.get_top(), buff=0.08, stroke_width=3, color=TEAL,
                          max_tip_length_to_length_ratio=0.3)
        rt = T("2.5–3.5× real time", 32, GOLD).next_to(chat, DOWN, buff=0.55)
        x0 = chat.get_right()[0] + 0.55
        rows = []
        for i, s in enumerate(self.segs):
            r = s.copy().stretch(0.65, 1)
            rows.append(r.move_to([x0 + r.width / 2, 0.7 - 0.48 * i, 0]))

        # join: gap pointers and the speaking rate
        gaps = []
        for i in range(4):
            gx = AX_L + U * (STARTS[i + 1] - GAP / 2)
            ln = Line([gx, LINE_Y + 0.2, 0], [gx, LINE_Y - 0.5, 0], color=DIM, stroke_width=2)
            gaps.append(VGroup(ln, T("0.55 s", 28, DIM).next_to(ln, DOWN, buff=0.1)))
        wpm = T("≈ 160 words a minute", 40, GOLD).move_to([3.2, 0.45, 0])
        self.gaps, self.wpm, self.rt = gaps, wpm, rt

        def pass_anims(i, o, d):
            return [time_span(strips[i].animate.scale(0.2).move_to(chat).set_opacity(0), o, o + 0.55 * d),
                    time_span(GrowFromPoint(rows[i], chat.get_right()), o + 0.4 * d, o + d)]

        with self.say("c1.voice.1") as c:
            self.play(FadeIn(self.vk, shift=0.3 * DOWN), FadeIn(self.tag, shift=0.3 * DOWN), run_time=1.0)
            self.play(FadeIn(para, shift=0.2 * UP), FadeIn(self.note, shift=0.2 * LEFT),
                      run_time=min(1.0, max(0.5, 0.8 * c.until("split"))))
            c.wait_until("split")

            # the line splits into its five sentences: every glyph flies to its strip
            src = list(para)
            dst = [g for t in texts for g in t]
            self.play(*[ReplacementTransform(a, b) for a, b in zip(src, dst)],
                      *[time_span(FadeIn(s[0]), 0.9, 1.6) for s in strips], run_time=1.6)
            self.remove(*para.get_family(), *dst)
            self.add(*strips)
            c.wait_until("voice")

            self.play(*[Transform(s, t) for s, t in zip(strips, col)],
                      time_span(FadeIn(chat), 0.5, 1.4), run_time=1.4)
            self.play(*pass_anims(0, 0, 1.5))
            self.remove(strips[0])
            c.wait_until("cloned from")
            self.play(FadeIn(ref, shift=0.2 * DOWN), FadeIn(ref_lab), FadeIn(ref_note), GrowArrow(ref_arrow),
                      run_time=min(1.0, max(0.5, 0.8 * c.until("the Mac's GPU"))))
            c.wait_until("the Mac's GPU")
            self.play(*pass_anims(1, 0, 1.0))
            c.wait_until("about three times")
            self.play(*pass_anims(2, 0, 0.9), *pass_anims(3, 0.35, 0.9), *pass_anims(4, 0.7, 0.9),
                      time_span(FadeIn(rt, shift=0.2 * UP), 0.8, 1.6))
            self.remove(*strips[1:])
            self.add(*rows)
            c.wait_until("join")

            # joined end to end with half-second breaths
            sweep_clear(self, *[ReplacementTransform(r, s) for r, s in zip(rows, self.segs)],
                        rt.animate.scale(1.25).move_to([-3.4, 0.45, 0]),
                        time_span(LaggedStart(*[FadeIn(g, shift=0.2 * DOWN) for g in gaps], lag_ratio=0.2), 1.2, 2.0),
                        keep=[*self.header(), *rows, rt], run_time=2.0)
            self.add(*self.segs, *gaps)
            c.wait_until("a hundred and sixty")
            self.play(FadeIn(wpm, shift=0.2 * DOWN), run_time=min(1.0, max(0.5, 0.8 * c.until())))

    # ------------------------------------------------------------ c1.voice.2
    def clip2(self):
        segs = self.segs
        whisper = []
        for (sz, w, h), x in zip([(28, 1.9, 0.6), (30, 2.3, 0.74), (32, 2.7, 0.88)], [-4.0, 0.0, 4.0]):
            whisper.append(tool_box(Mono("Whisper", sz), w, h).move_to([x, 1.55, 0]))
        rows = []
        for s in segs:
            row = VGroup(*[check_mark().scale(0.45).set_stroke(width=4) for _ in range(3)])
            rows.append(row.arrange(RIGHT, buff=0.08).move_to([s.get_x(), LINE_Y + 0.62, 0]))
        ticks = [t for row in rows for t in row]
        q = T("?", 80, YELLOW).move_to([0, 0.35, 0])
        hl = SurroundingRectangle(segs[2], color=YELLOW, buff=0.12, corner_radius=0.08)
        gtick = check_mark(GREEN).next_to(whisper[0], RIGHT, buff=0.3)
        crosses = [cross_mark(RED).next_to(whisper[k], RIGHT, buff=0.3) for k in (1, 2)]

        def pair(a, b):
            g = VGroup(Mono(a, 32), Arrow(ORIGIN, 0.8 * RIGHT, buff=0, stroke_width=3, color=RED,
                                          max_tip_length_to_length_ratio=0.3), Mono(b, 32, RED))
            return g.arrange(RIGHT, buff=0.25)
        pairs = VGroup(pair("nil", "no"), pair("type error", "tie bearer")).arrange(RIGHT, buff=1.4)
        pairs.move_to([0, -2.75, 0])
        self.pairs = list(pairs)

        with self.say("c1.voice.2") as c:
            self.play(LaggedStart(*[FadeIn(w, shift=0.3 * DOWN) for w in whisper], lag_ratio=0.25), run_time=1.4)
            self.add(*whisper)
            c.wait_until("They must agree")
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(t, scale=0.5) for t in row], lag_ratio=0.35)
                                    for row in rows], lag_ratio=0.45),
                      run_time=min(3.2, 0.9 * c.until("why")))
            self.add(*ticks)
            c.wait_until("why")
            self.play(FadeIn(q, scale=0.6), *[FadeOut(m) for m in [*self.gaps, self.wpm, self.rt]],
                      *set_alpha(ticks, DIMMED), run_time=1.0)
            c.wait_until("small")
            self.play(ReplacementTransform(q, gtick), Create(hl), *[FadeOut(t) for t in ticks], run_time=1.5)
            c.wait_until("passed real mishearings")
            self.play(*[FadeIn(x, scale=0.6) for x in crosses], run_time=0.8)
            c.wait_until("was heard")
            self.play(LaggedStart(*[FadeIn(p, shift=0.3 * DOWN) for p in pairs], lag_ratio=0.4), run_time=1.4)
            self.add(*pairs)

    # ------------------------------------------------------------ c1.voice.3
    def clip3(self):
        segs = self.segs
        keep = lambda: [*self.header(), *segs]   # noqa: E731
        # {fail}: re-voiced takes over sentence 3
        d3 = span(2)[1] - span(2)[0]
        take2 = wave(d3, seed=31).move_to([segs[2].get_x(), LINE_Y + 1.0, 0])
        take3 = wave(d3, seed=32).move_to([segs[2].get_x(), LINE_Y + 1.95, 0])
        l2 = T("seed 2", 30).next_to(take2, RIGHT, buff=0.35)
        l3 = T("seed 3", 30).next_to(take3, RIGHT, buff=0.35)
        # {text}: sentence 1 fails on every seed; a word of its text changes
        d1 = span(0)[1] - span(0)[0]
        t1a = wave(d1, seed=41, color=RED).move_to([segs[0].get_x(), LINE_Y + 1.0, 0])
        t1b = wave(d1, seed=42, color=RED).move_to([segs[0].get_x(), LINE_Y + 1.95, 0])
        m2 = T("seed 2", 30).next_to(t1a, RIGHT, buff=0.35)
        m3 = T("seed 3", 30).next_to(t1b, RIGHT, buff=0.35)
        full = Mono(SENTENCES[0], 32)
        full.move_to([0, 1.85, 0]).align_to(np.array([AX_L, 0, 0]), LEFT)
        base = Mono("Look at what has       up.", 32)
        base.shift(full[0].get_center() - base[0].get_center())
        w_old = Mono("piled", 32)
        w_old.shift(full[13].get_center() - w_old[0].get_center())
        w_new = Mono("built", 32, YELLOW).move_to(w_old)
        w_new.shift(UP * (w_old[2].get_center()[1] - w_new[3].get_center()[1]))
        # {stored}: a still-flagged sentence becomes a record for the director
        head = T("flagged lines", 32)
        rule = Line(ORIGIN, 3.2 * RIGHT, color=DIM, stroke_width=2)
        rec = VGroup(Mono("c4.trace.2, sentence 2", 28, DIM), Mono('heard: "…to be conned on"', 28, TEAL))
        rec.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lst = VGroup(head, rule, rec).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lst.move_to([0, 1.25, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
        director = agent_box("director", 2.5, 0.8).move_to([3.9, 1.2, 0])
        arr = Arrow(rec.get_right() + 0.25 * RIGHT, director.get_left(), buff=0.15, stroke_width=4, color=YELLOW)
        manual = T("manual check", 32, DIM).move_to([3.9, 0.05, 0])
        strike = Line(manual.get_left() + 0.12 * LEFT, manual.get_right() + 0.12 * RIGHT, color=RED, stroke_width=5)

        with self.say("c1.voice.3") as c:
            sweep_clear(self, segs[2].animate.set_color(RED), keep=[*keep(), *self.pairs], run_time=1.0)
            c.wait_until("voiced again")
            self.play(LaggedStart(TransformFromCopy(segs[2], take2), TransformFromCopy(segs[2], take3), lag_ratio=0.35),
                      LaggedStart(FadeIn(l2), FadeIn(l3), lag_ratio=0.35), run_time=1.3)
            self.add(take2, take3, l2, l3)
            c.wait_until("the best take")
            self.play(take2.animate.set_color(RED), take3.animate.set_color(GREEN), run_time=0.7)
            self.play(take3.animate.move_to(segs[2]), FadeOut(segs[2]), FadeOut(l3), run_time=0.9)
            segs[2] = take3
            c.wait_until("text")

            self.play(segs[0].animate.set_color(RED),
                      LaggedStart(TransformFromCopy(segs[0], t1a), TransformFromCopy(segs[0], t1b), lag_ratio=0.3),
                      LaggedStart(FadeIn(m2), FadeIn(m3), lag_ratio=0.3),
                      FadeIn(base), FadeIn(w_old),
                      *[time_span(FadeOut(m), 0, 0.6) for m in [take2, l2, *self.pairs]], run_time=1.3)
            self.add(t1a, t1b, m2, m3)
            c.wait_until("the text changes")
            self.play(FadeOut(w_old, shift=0.3 * UP), FadeIn(w_new, shift=0.3 * UP),
                      segs[0].animate.set_color(GREEN), run_time=1.3)
            c.wait_until("stored")

            self.play(segs[1].animate.set_color(RED), run_time=0.8)
            c.wait_until("with what was heard")
            sweep_clear(self, time_span(FadeIn(head, shift=0.2 * DOWN), 0.5, 1.6), time_span(Create(rule), 0.5, 1.6),
                        time_span(TransformFromCopy(segs[1], rec), 0.4, 1.6), keep=keep(), run_time=1.6)
            self.add(rec)
            c.wait_until("for the director")
            self.play(FadeIn(director, shift=0.2 * LEFT), GrowArrow(arr), run_time=1.2)
            c.wait_until("nobody")
            self.play(FadeIn(manual, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("manual check")
            self.play(Create(strike), run_time=min(0.8, max(0.4, 0.9 * c.until())))

    # ------------------------------------------------------------ c1.voice.4
    def clip4(self):
        segs = self.segs
        axis, ticks, nums, end_tick, end_lab, pins, labs = build_timeline()
        tl = VGroup(axis, *ticks, *nums, end_tick, end_lab, *pins, *labs)
        man = page(0.9, 1.15, 0.26).move_to([-4.3, 0.75, 0])
        man_lab = Mono("manifest.json", 28).next_to(man, DOWN, buff=0.25)
        hour = VGroup(T("1 hour of narration", 40, GOLD),
                      Arrow(ORIGIN, 0.9 * RIGHT, buff=0, stroke_width=4, color=GOLD, max_tip_length_to_length_ratio=0.3),
                      T("20–30 min", 40, GOLD)).arrange(RIGHT, buff=0.25).move_to([1.8, 0.75, 0])
        you = VGroup(ear_icon(), T("you", 48, YELLOW)).arrange(RIGHT, buff=0.25).move_to([-4.3, -2.1, 0])
        lst = VGroup(T("check by ear", 32), Mono('c4.trace.2  "consed on"', 28), Mono('c1.voice.1  "vee-kay"', 28))
        lst.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([1.8, -2.1, 0])
        arr = Arrow(lst.get_left() + 0.2 * LEFT, you.get_right() + 0.2 * RIGHT, buff=0.1, stroke_width=4, color=YELLOW)

        with self.say("c1.voice.4") as c:
            # the joined waveform becomes the clip's timeline
            self.play(ReplacementTransform(VGroup(*segs), axis), run_time=1.6)
            self.add(axis)
            c.wait_until("sentence starts")
            sweep_clear(self, LaggedStart(*[AnimationGroup(Create(t), FadeIn(n, shift=0.15 * DOWN))
                                            for t, n in zip([*ticks, end_tick], [*nums, end_lab])], lag_ratio=0.2),
                        keep=[*self.header(), axis], run_time=1.3)
            c.wait_until("marks land")
            self.play(LaggedStart(*[AnimationGroup(Create(p), FadeIn(lb, shift=0.15 * DOWN))
                                    for p, lb in zip(pins, labs)], lag_ratio=0.25),
                      run_time=min(1.5, max(0.6, 0.9 * c.until("manifest"))))
            c.wait_until("into the manifest")
            settle(self, tl)
            self.play(tl.animate.scale(0.08).move_to(man).set_opacity(0),
                      time_span(FadeIn(man, scale=0.7), 0.6, 1.5), time_span(FadeIn(man_lab, shift=0.2 * DOWN), 0.9, 1.5))
            self.remove(*tl.get_family())
            c.wait_until("hour")
            self.play(FadeIn(hour, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("ear")
            self.play(FadeIn(you, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("you still get")
            self.play(LaggedStart(*[FadeIn(x, shift=0.2 * DOWN) for x in lst], lag_ratio=0.3), GrowArrow(arr),
                      run_time=min(1.3, max(0.6, 0.9 * c.until())))
            self.add(*lst)
        self.wait(2.0)   # let the list be read before the scene clears
