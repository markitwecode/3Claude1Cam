"""Chapter 2, scene 5: Inside one build. Clips c2.anat.1 – c2.anat.3.

PLAN
  c2.anat.1  ch1 s6's small GOLD context bar + "?"; title "a typical build (medians of 76 fresh
             builds)"; one outline tile "one turn" becomes a legend (bottom right); four rows of
             turn tiles, one group per sentence: ~5 vk check (2 tagged --frames), ~5 image,
             1 Write (+ DIM "Edits: ~0"), ~13 other shell calls -> 9 turn RED "~9 lookup"
             (+ breakdown), 2 tagged "~2 patch".
  c2.anat.2  the rows slide up and shrink into a strip (counts kept); the peak bar (outline,
             "peak ≈ 132k") stacks up in GOLD shades, the image / tool / write segments flying
             out of their tiles; RED "thinking ≈ 80k" fills the rest.
  c2.anat.3  flash on thinking, YELLOW "thinking ≈ 60% / of the peak"; DIM suspect tag on the
             images segment; the dollars bar beside it (RED output born from the thinking
             segment, GOLD cache writes, GREEN re-reading); both RED parts pulse; the rest
             dims; YELLOW "think less?" -> thinking segment, "look up less?" -> 9 RED tiles.

SHARED PIECES (s6 / s8 reuse them small): turn_tile / tile_row (tiles), peak_bar (stacked bar
with labels), dollar_bar. See their docstrings for sizes and colours.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── shared look ────────────────────────────────────────────────────────────────
TILE = 0.45            # one turn = one rounded square
TILE_GAP = 0.13        # pitch 0.58
TILE_OPACITY = 0.85    # coloured tiles; neutral shell tiles are DIM at 0.5
GOLD_SHADES = ("#B8824A", GOLD, "#F7C68C", "#D39552")   # startup, images, tool output, writes
PULSE_RED = "#FF9A8F"


def turn_tile(color, size=TILE, opacity=TILE_OPACITY):
    """One turn: a rounded square filled in its kind's colour (BLUE vk check, GOLD image,
    GREEN Write, DIM 0.5 other shell, RED lookup), stroke 2 in the same colour."""
    t = RoundedRectangle(corner_radius=0.13 * size, width=size, height=size)
    return t.set_fill(color, opacity).set_stroke(color, 2)


def tile_row(n, color, size=TILE, gap=TILE_GAP, opacity=TILE_OPACITY):
    """n turn tiles left to right, centred on ORIGIN (e.g. tile_row(9, RED) = the lookups)."""
    return VGroup(*[turn_tile(color, size, opacity) for _ in range(n)]).arrange(RIGHT, buff=gap)


def _stack(values, colors, x, bottom, height, width, total):
    """A bottom-anchored stacked bar: DIM outline of the full height, segments filled
    bottom-up, each with a thin dark (BG) separator stroke, as ch1 s6's context bar."""
    outline = Rectangle(width=width, height=height).set_stroke(DIM, 2).set_fill(BG, 0)
    outline.move_to([x, bottom + height / 2, 0])
    segs = VGroup()
    y = bottom
    for v, col in zip(values, colors):
        h = height * v / total
        seg = Rectangle(width=width, height=h).set_fill(col, 1).set_stroke(BG, 3)
        seg.move_to([x, y + h / 2, 0])
        segs.add(seg)
        y += h
    return outline, segs


def peak_bar(x=-2.75, bottom=-3.5, height=5.1, width=1.2, label_size=28):
    """The peak context of a typical build, 132k: segments bottom-up startup 12k, images 15k,
    tool output 11k, writes and patches 8k (GOLD_SHADES) and thinking (RED, the rest, 86 of
    132). Returns a VGroup with .outline .segs (5) .think (= segs[4]) .labels (5, the last is
    the RED "thinking ≈ 80k" at 32) .ticks (4 DIM leader lines) .header ("peak ≈ 132k", 34)."""
    outline, segs = _stack((12, 15, 11, 8, 86), (*GOLD_SHADES, RED), x, bottom, height, width, 132)
    header = T("peak ≈ 132k", 34, t2c={"132k": GOLD}).next_to(outline, UP, buff=0.32)
    texts = (("startup 12k", "12k"), ("images 15k (5 × ∼3k)", "15k"),
             ("tool output 11k", "11k"), ("writes and patches 8k", "8k"))
    lx = outline.get_right()[0] + 0.3
    labels, ticks = VGroup(), VGroup()
    prev = -10.0
    for (txt, num), seg in zip(texts, segs[:4]):
        lab = T(txt, label_size, t2c={num: GOLD})
        y = max(seg.get_y(), prev + 0.47)
        prev = y
        lab.move_to([lx, y, 0], aligned_edge=LEFT)
        ticks.add(Line([outline.get_right()[0] + 0.05, seg.get_y(), 0], [lx - 0.07, y, 0])
                  .set_stroke(DIM, 2))
        labels.add(lab)
    think = T("thinking ≈ 80k", 32, color=RED)
    think.move_to([lx, segs[4].get_y() + 0.42, 0], aligned_edge=LEFT)
    labels.add(think)
    bar = VGroup(outline, segs, ticks, labels, header)
    bar.outline, bar.segs, bar.think, bar.labels, bar.ticks, bar.header = (
        outline, segs, segs[4], labels, ticks, header)
    return bar


def dollar_bar(x=2.75, bottom=-3.5, height=5.1, width=1.1):
    """A builder's dollars: RED output (mostly thinking) ½, GOLD cache writes 30%, GREEN
    re-reading 15%, bottom-up in a full-height DIM outline (top 5% left empty). Returns a
    VGroup with .outline .segs (3) .labels (3, size 30/28, in the segment colours) .header."""
    outline, segs = _stack((50, 30, 15), (RED, GOLD, GREEN), x, bottom, height, width, 100)
    header = T("a builder's dollars", 34).next_to(outline, UP, buff=0.32)
    lx = outline.get_right()[0] + 0.25
    l_out = VGroup(T("output ≈ ½", 30, color=RED), T("(mostly thinking)", 28, color=RED))
    l_wr = VGroup(T("cache writes", 30, color=GOLD), T("≈ 30%", 30, color=GOLD))
    for lab in (l_out, l_wr):
        lab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    l_rd = T("re-reading ≈ 15%", 30, color=GREEN)
    labels = VGroup(l_out, l_wr, l_rd)
    for lab, seg in zip(labels, segs):
        lab.move_to([lx, seg.get_y(), 0], aligned_edge=LEFT)
    bar = VGroup(outline, segs, labels, header)
    bar.outline, bar.segs, bar.labels, bar.header = outline, segs, labels, header
    return bar


def mini_context_bar(height=2.3, width=0.7):
    """ch1 s6's context bar, small: GOLD segments, thin dark separators, bottom-anchored."""
    _, segs = _stack((0.95, 0.22, 0.45, 0.58), GOLD_SHADES, 0, -height / 2, height, width, 2.2)
    return segs


# ── layout of the clip-1 board ─────────────────────────────────────────────────
ROW_Y = (2.05, 0.95, -0.15, -1.25)     # vk check, image, Write, shell
TILE_X0 = -1.25                         # left edge of each row's first tile
COUNT_RX = -5.45                        # counts right-aligned here (size 44)
NAME_LX = -5.15                         # kind names left-aligned here
STRIP_Y = 2.95                          # clips 2-3: the shrunk tile strip
STRIP_X = (-6.35, 5.9)
STRIP_S = 28 / 44                       # counts shrink 44 -> 28, tiles with them


class Anatomy(NarratedScene):
    def construct(self):
        self.build_board()
        self.turns()
        self.stack_peak()
        self.cost()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── objects ────────────────────────────────────────────────────────────────
    def build_board(self):
        t1 = T("a typical build", 48)
        t2 = T("(medians of 76 fresh builds)", 32, color=DIM)
        self.title = VGroup(t1, t2).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to(UP * 3.35)

        def row(n, color, y, count, name, opacity=TILE_OPACITY):
            tiles = tile_row(n, color, opacity=opacity).move_to([TILE_X0, y, 0], aligned_edge=LEFT)
            cnt = T(count, 44, color=color if color != DIM else FG)
            cnt.move_to([COUNT_RX, y, 0], aligned_edge=RIGHT)
            name.move_to([NAME_LX, y, 0], aligned_edge=LEFT)
            return tiles, cnt, name

        self.checks, self.cnt_chk, self.name_chk = row(5, BLUE, ROW_Y[0], "∼5", Mono("vk check", 30, BLUE))
        self.images, self.cnt_img, self.name_img = row(5, GOLD, ROW_Y[1], "∼5", T("image", 32, color=GOLD))
        self.write, self.cnt_wr, self.name_wr = row(1, GREEN, ROW_Y[2], "1", Mono("Write", 30, GREEN))
        self.shell, self.cnt_sh, self.name_sh = row(13, DIM, ROW_Y[3], "∼13",
                                                    T("other shell calls", 32), opacity=0.5)

        self.frames_box = SurroundingRectangle(self.checks[3], self.checks[4], buff=0.07,
                                               corner_radius=0.08, color=DIM).set_stroke(width=2)
        self.frames_txt = Mono("--frames", 28, DIM).next_to(self.frames_box, RIGHT, buff=0.2)
        self.edits = T("Edits: ∼0", 30, color=DIM).next_to(self.write, RIGHT, buff=0.45)

        sh = self.shell
        self.l_brace = span_brace(sh[0].get_corner(DL), sh[8].get_corner(DR), DOWN, color=RED, buff=0.15)
        self.l_label = T("∼9 lookup", 30, color=RED).next_to(self.l_brace, DOWN, buff=0.1)
        # the lookup breakdown: four items (separate texts) in two lines, "·" between
        items = [T(name + " " + num, 28, color=DIM, t2c={num: GOLD}) for name, num in
                 (("engine library", "2.7"), ("Manim source", "1.2"), ("other scenes", "1.1"), ("misc", "3.8"))]
        dots = [T("·", 28, color=DIM) for _ in range(2)]
        lines = VGroup(VGroup(items[0], dots[0], items[1]).arrange(RIGHT, buff=0.18),
                       VGroup(items[2], dots[1], items[3]).arrange(RIGHT, buff=0.18))
        lines.arrange(DOWN, buff=0.16).next_to(self.l_label, DOWN, buff=0.28)
        self.bd = [items[0], dots[0], items[1], items[2], dots[1], items[3]]
        self.p_brace = Line(sh[9].get_corner(DL) + 0.06 * RIGHT, sh[10].get_corner(DR) + 0.06 * LEFT)
        self.p_brace.set_stroke(GREEN, 4).shift(0.2 * DOWN)
        self.p_label = T("∼2 patch", 28, color=GREEN).next_to(self.p_brace, DOWN, buff=0.1)
        self.p_label.match_y(self.l_label)

        # the "one turn" tile, big at first, then a legend at the bottom right
        self.intro = RoundedRectangle(corner_radius=0.12, width=0.9, height=0.9).set_stroke(FG, 3)
        self.intro.move_to(UP * 0.2)
        self.one_turn = T("one turn", 36, color=DIM).next_to(self.intro, DOWN, buff=0.3)

        self.pk = peak_bar()
        self.db = dollar_bar()

    # ── c2.anat.1 ──────────────────────────────────────────────────────────────
    def enter_row(self, c, tiles, cnt, name, nxt, lag=0.2, extra=()):
        rt = min(1.5, 0.7 * c.until(nxt))
        self.play(FadeIn(tiles, lag_ratio=lag), FadeIn(cnt, shift=0.2 * RIGHT),
                  FadeIn(name, shift=0.2 * RIGHT), *extra, run_time=rt)
        c.wait_until(nxt)

    def turns(self):
        with self.say("c2.anat.1") as c:
            mini = mini_context_bar().move_to(LEFT * 0.4)
            q = T("?", 84, color=YELLOW).next_to(mini, RIGHT, buff=0.45)
            self.play(FadeIn(mini, shift=0.3 * UP), FadeIn(q, shift=0.3 * DOWN),
                      run_time=min(0.7, 0.6 * c.until("a typical build")))
            c.wait_until("a typical build")
            self.play(FadeIn(self.title, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("tiles")
            self.play(FadeOut(mini, scale=1.6), FadeOut(q, scale=1.6),
                      time_span(FadeIn(self.intro, scale=0.5), 0.3, 1.0),
                      time_span(FadeIn(self.one_turn, shift=0.3 * DOWN), 0.4, 1.0), run_time=1.0)
            c.wait_until("in typical counts")
            # the single tile becomes a legend in the bottom-right corner
            self.one_turn.generate_target()
            self.one_turn.target.scale(28 / 36).move_to([6.5, -3.3, 0], aligned_edge=RIGHT)
            self.intro.generate_target()
            self.intro.target.scale(0.32 / 0.9).next_to(self.one_turn.target, LEFT, buff=0.18)
            self.play(MoveToTarget(self.intro), MoveToTarget(self.one_turn),
                      run_time=min(1.4, 0.7 * c.until("checks")))
            c.wait_until("checks")

            self.enter_row(c, self.checks, self.cnt_chk, self.name_chk, "images",
                           extra=(time_span(Create(self.frames_box), 1.0, 1.6),
                                  time_span(FadeIn(self.frames_txt, shift=0.2 * LEFT), 1.0, 1.6)))
            self.enter_row(c, self.images, self.cnt_img, self.name_img, "write")
            self.enter_row(c, self.write, self.cnt_wr, self.name_wr, "median number")
            self.play(FadeIn(self.edits, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("shell")
            self.enter_row(c, self.shell, self.cnt_sh, self.name_sh, "lookups", lag=0.12)

            # nine of the shell calls are lookups
            reds = [time_span(t.animate.set_fill(RED, TILE_OPACITY).set_stroke(RED), 0.1 * i, 0.1 * i + 0.6)
                    for i, t in enumerate(self.shell[:9])]
            self.play(*reds, time_span(GrowFromCenter(self.l_brace), 0.8, 1.5),
                      time_span(FadeIn(self.l_label, shift=0.2 * DOWN), 0.9, 1.6), run_time=1.6)
            self.play(*[time_span(FadeIn(m, shift=0.2 * DOWN), 0.12 * i, 0.12 * i + 0.6)
                        for i, m in enumerate(self.bd)], run_time=1.2)
            c.wait_until("patches")
            self.play(*[t.animate.set_stroke(GREEN, 3) for t in self.shell[9:11]],
                      Create(self.p_brace), FadeIn(self.p_label, shift=0.2 * DOWN), run_time=1.0)

    # ── c2.anat.2 ──────────────────────────────────────────────────────────────
    def strip_targets(self):
        groups = (self.shell, self.checks, self.images, self.write)
        counts = (self.cnt_sh, self.cnt_chk, self.cnt_img, self.cnt_wr)
        widths = [g.width * STRIP_S for g in groups]
        gap = (STRIP_X[1] - STRIP_X[0] - sum(widths)) / 3
        x = STRIP_X[0]
        for g, cnt, w in zip(groups, counts, widths):
            g.generate_target()
            g.target.scale(STRIP_S).move_to([x, STRIP_Y, 0], aligned_edge=LEFT)
            cnt.generate_target()
            cnt.target.scale(STRIP_S).next_to(g.target, UP, buff=0.14, aligned_edge=LEFT)
            x += w + gap
        st = self.shell.target
        self.p_label.generate_target()
        self.p_label.target.move_to([(st[9].get_x() + st[10].get_x()) / 2, self.cnt_sh.target.get_y(), 0])
        return [*groups, *counts, self.p_label]

    def stack_peak(self):
        pk = self.pk
        with self.say("c2.anat.2") as c:
            movers = self.strip_targets()
            fades = [self.title, self.name_chk, self.name_img, self.name_wr, self.name_sh,
                     self.frames_box, self.frames_txt, self.edits, self.l_brace, self.l_label,
                     *self.bd, self.p_brace, self.intro, self.one_turn]
            self.play(*[time_span(FadeOut(m), 0.0, 0.6) for m in fades],   # names gone before counts cross rows
                      *[MoveToTarget(m) for m in movers], run_time=1.8)
            c.wait_until("about a hundred")
            self.play(Create(pk.outline), FadeIn(pk.header, shift=0.2 * DOWN),
                      run_time=min(1.0, 0.8 * c.until("startup")))
            c.wait_until("startup")

            def segment(intro, i, nxt, rt):
                intro = intro if isinstance(intro, (list, tuple)) else [intro]
                self.play(*intro, time_span(Create(pk.ticks[i]), rt - 0.6, rt),
                          time_span(FadeIn(pk.labels[i], shift=0.2 * LEFT), rt - 0.6, rt),
                          run_time=rt)
                c.wait_until(nxt)

            sh = self.shell
            segment(GrowFromEdge(pk.segs[0], DOWN), 0, "imgs", 1.0)
            segment(TransformFromCopy(self.images.copy(), pk.segs[1]), 1, "tool", 1.5)
            segment(TransformFromCopy(VGroup(self.checks.copy(), sh.copy()), pk.segs[2]), 2, "files", 1.5)
            # the sources flash in place (a Write copy flying ~9 units read as a stray tile)
            segment([GrowFromEdge(pk.segs[3], DOWN),
                     *flash([self.write[0], sh[9], sh[10]], color=GREEN, time_width=1.5)],
                    3, "think", 1.3)
            self.play(GrowFromEdge(pk.think, DOWN), run_time=min(1.8, 0.9 * c.until("is thinking")))
            c.wait_until("is thinking")
            self.play(FadeIn(pk.labels[4], shift=0.2 * LEFT), run_time=0.8)

    # ── c2.anat.3 ──────────────────────────────────────────────────────────────
    def cost(self):
        pk, db, sh = self.pk, self.db, self.shell
        y60 = VGroup(T("thinking ≈ 60%", 30, color=YELLOW), T("of the peak", 30, color=YELLOW))
        y60.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(pk.labels[4], DOWN, aligned_edge=LEFT, buff=0.25)
        suspect = VGroup(T("the old suspect:", 28, color=DIM), T("≈ 10%", 28, color=DIM))
        suspect.arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        suspect.move_to([pk.outline.get_left()[0] - 0.25, pk.segs[1].get_y(), 0], aligned_edge=RIGHT)

        q1 = T("think less?", 32, color=YELLOW)
        q1.move_to([pk.outline.get_left()[0] - 0.75, pk.think.get_y() + 0.3, 0], aligned_edge=RIGHT)
        a1 = Arrow(q1.get_right() + 0.08 * RIGHT, [pk.outline.get_left()[0] - 0.04, q1.get_y(), 0],
                   buff=0, stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.4)
        look_x = (sh[0].get_left()[0] + sh[8].get_right()[0]) / 2
        look_bottom = sh[0].get_bottom()[1]
        q2 = T("look up less?", 32, color=YELLOW).move_to([look_x - 0.25, 1.3, 0])
        a2 = Arrow(q2.get_top() + 0.08 * UP, [look_x, look_bottom - 0.08, 0],
                   buff=0, stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.3)

        with self.say("c2.anat.3", gap=3.6) as c:
            self.play(FlashAround(pk.think, time_width=1.5), run_time=1.6)
            c.wait_until("Thinking is about sixty percent")
            self.play(FadeIn(y60, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("suspect")
            self.play(FadeIn(suspect, shift=0.3 * RIGHT),
                      FlashAround(pk.segs[1], color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("dollars")
            self.play(Create(db.outline), FadeIn(db.header, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("Output, mostly thinking")
            self.play(TransformFromCopy(pk.think.copy(), db.segs[0]),
                      time_span(FadeIn(db.labels[0], shift=0.2 * LEFT), 1.0, 1.7), run_time=1.7)
            c.wait_until("writes")
            self.play(GrowFromEdge(db.segs[1], DOWN),
                      time_span(FadeIn(db.labels[1], shift=0.2 * LEFT), 0.4, 1.0), run_time=1.0)
            c.wait_until("reads")
            self.play(GrowFromEdge(db.segs[2], DOWN),
                      time_span(FadeIn(db.labels[2], shift=0.2 * LEFT), 0.4, 1.0), run_time=1.0)
            c.wait_until("biggest")
            self.play(FlashAround(pk.think, time_width=1.5), FlashAround(db.segs[0], time_width=1.5),
                      pk.think.animate(rate_func=there_and_back).set_fill(PULSE_RED),
                      db.segs[0].animate(rate_func=there_and_back).set_fill(PULSE_RED), run_time=1.6)
            c.wait_until("two")
            dim = [pk.header, *pk.segs[:4], *pk.ticks, *pk.labels[:4], y60, suspect,
                   db.header, db.segs[1], db.segs[2], db.labels[1], db.labels[2],
                   self.checks, self.images, self.write, *sh[9:],
                   self.cnt_sh, self.cnt_chk, self.cnt_img, self.cnt_wr, self.p_label]
            self.play(*set_alpha(dim, 0.3), run_time=1.0)
            c.wait_until("Can it think less")
            self.play(FadeIn(q1, shift=0.2 * RIGHT), GrowArrow(a1), run_time=1.0)
            c.wait_until("look")
            self.play(FadeIn(q2, shift=0.2 * UP), GrowArrow(a2), run_time=0.9)
            self.play(FlashAround(VGroup(*[t.copy() for t in sh[:9]]), time_width=1.5), run_time=1.2)
