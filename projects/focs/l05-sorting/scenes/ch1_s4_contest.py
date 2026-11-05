"""Chapter 1, scene 4: the contestants, and how to score them. Clips c1.contest.1 – c1.contest.4.

Also defines `make_scoreboard()`, the chapter's scoreboard: ch1 s6–s8 and ch2–ch6 import it
(`from ch1_s4_contest import make_scoreboard`); importing this module has no side effects.
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


# ------------------------------------------------------------------ the shared scoreboard
SB_ROWS = ("insertion sort", "quicksort", "merge sort")
SB_COLS = ("comparisons on 10,000 random items", "DECstation time")
SB_TALLY = "counted by us: a tallying ≤"

SB_X_LABEL = -6.0               # left edge of the row labels and of floor_label
SB_X_COLS = (0.3, 4.65)         # x centres of the two value columns
SB_Y_HEAD = 2.75                # y centre of the two-line comparisons header
SB_Y_RULE = 1.6                 # the DIM rule under the headers
SB_Y_ROWS = (0.7, -0.5, -1.7)   # y centres of the three rows
SB_Y_FLOOR = -2.9               # the floor line / floor_label


def make_scoreboard(bound=None):
    """The chapter's scoreboard, built at its on-screen position (scale 1, fits the frame).

    Returns a VGroup (nothing is added to any scene) with these attributes:
      row_labels   VGroup of 3 YELLOW T 36: "insertion sort", "quicksort", "merge sort",
                   left edges at x = -6.0, centred on y = 0.7, -0.5, -1.7.
      col_headers  VGroup of 2: [0] "comparisons on / 10,000 random items" (a VGroup of two
                   T 30 lines, centred at x = 0.3), [1] "DECstation time" (T 30, centred at
                   x = 4.65, level with the header's second line).
      tally_tag    DIM T 28 "counted by us: a tallying ≤", just under col_headers[0].
      rule         DIM line (stroke 2) under the headers, y = 1.6, across the whole board.
      cells        cells[row][col]: GOLD T 44 "?" at (x of column, y of row). To fill a cell,
                   build the value and `.move_to(board.cells[r][c])`, then transform.
      floor_line   GOLD DashedLine (stroke 3) under the comparisons column at y = -2.9,
                   x = -2.07 .. 2.66.
      floor_label  GOLD T 34 "lower bound: ?", left edge x = -6.0, y = -2.9.
      floor_value  None.

    make_scoreboard(bound="118,458") returns the board as ch1 s6 leaves it (what ch2–ch6
    import): everything above is the same except the floor row, which becomes
      floor_label  GOLD T 34 "lower bound ≈", left edge x = -6.0, y = -2.9;
      floor_value  GOLD T 34 with the `bound` text, its left edge 0.2 right of floor_label;
      floor_line   a SOLID GOLD Line (stroke 3) at y = -2.9, from 0.35 right of floor_value
                   to the dashed line's end (x ≈ -1.25 .. 2.66 for "118,458"),
    laid out exactly as s6's {floor} beat builds it.
    """
    x1, x2 = SB_X_COLS

    row_labels = VGroup(*[T(r, size=36, color=YELLOW) for r in SB_ROWS])
    for lab, y in zip(row_labels, SB_Y_ROWS):
        lab.move_to([SB_X_LABEL, y, 0], aligned_edge=LEFT)

    head1 = VGroup(T("comparisons on", size=30), T("10,000 random items", size=30))
    head1.arrange(DOWN, buff=0.12).move_to([x1, SB_Y_HEAD, 0])
    head2 = T("DECstation time", size=30).move_to([x2, head1[1].get_y(), 0])
    col_headers = VGroup(head1, head2)

    tally_tag = T(SB_TALLY, size=28, color=DIM).next_to(head1, DOWN, buff=0.16)

    x_right = max(head2.get_right()[0], x2 + 1.4)
    rule = Line([SB_X_LABEL, SB_Y_RULE, 0], [x_right, SB_Y_RULE, 0]).set_stroke(DIM, 2)

    cells = VGroup(*[
        VGroup(*[T("?", size=44, color=GOLD).move_to([x, y, 0]) for x in SB_X_COLS])
        for y in SB_Y_ROWS
    ])

    half = tally_tag.width / 2 + 0.1
    floor_line = DashedLine([x1 - half, SB_Y_FLOOR, 0], [x1 + half, SB_Y_FLOOR, 0],
                            dash_length=0.16, dashed_ratio=0.55).set_stroke(GOLD, 3)
    floor_label = T("lower bound: ?", size=34, color=GOLD)
    floor_label.move_to([SB_X_LABEL, SB_Y_FLOOR, 0], aligned_edge=LEFT)

    floor_value = None
    if bound is not None:   # the state ch1 s6 leaves it in (same construction as s6's {floor} beat)
        full = T(f"lower bound ≈ {bound}", size=34, color=GOLD, disable_ligatures=True)
        full.move_to(floor_label, aligned_edge=LEFT)
        words = T("lower bound ≈", size=34, color=GOLD).move_to(VGroup(*full[:11]))
        floor_value = T(bound, size=34, color=GOLD).move_to(VGroup(*full[11:]))
        floor_value.shift((words.get_right()[0] + 0.2 - floor_value.get_left()[0]) * RIGHT)
        floor_line = Line([floor_value.get_right()[0] + 0.35, floor_line.get_y(), 0],
                          floor_line.get_end()).set_stroke(GOLD, 3)
        floor_label = words

    board = VGroup(rule, row_labels, col_headers, tally_tag, cells, floor_line, floor_label)
    if floor_value is not None:
        board.add(floor_value)
    board.rule = rule
    board.row_labels = row_labels
    board.col_headers = col_headers
    board.tally_tag = tally_tag
    board.cells = cells
    board.floor_line = floor_line
    board.floor_label = floor_label
    board.floor_value = floor_value
    return board


# ------------------------------------------------------------------ scene-only icons
PANEL = "#1A1D23"


def machine_icon(w, h):
    """A plain monitor (screen, stand, foot) showing the count C(n) in GOLD; `.count`."""
    screen = RoundedRectangle(corner_radius=0.1, width=w, height=h).set_stroke(FG, 3).set_fill(PANEL, 1)
    stand = Line(screen.get_bottom(), screen.get_bottom() + 0.22 * DOWN).set_stroke(FG, 3)
    foot = Line(0.4 * LEFT, 0.4 * RIGHT).move_to(stand.get_end()).set_stroke(FG, 3)
    count = MathTex("C(n)", font_size=44, color=GOLD).move_to(screen)
    g = VGroup(screen, stand, foot, count)
    g.count = count
    return g


def decstation():
    """A boxy late-80s workstation: CRT on a pizza-box base, keyboard in front."""
    body = RoundedRectangle(corner_radius=0.1, width=2.8, height=2.15).set_stroke(FG, 3).set_fill(PANEL, 1)
    screen = RoundedRectangle(corner_radius=0.22, width=2.15, height=1.5).set_stroke(DIM, 2)
    screen.set_fill("#0C1712", 1).move_to(body).shift(0.1 * UP)
    prompt = Mono("% _", size=30, color=GREEN)
    prompt.move_to(screen.get_corner(UL) + np.array([0.28, -0.28, 0]), aligned_edge=UL)
    base = RoundedRectangle(corner_radius=0.06, width=3.5, height=0.5).set_stroke(FG, 3).set_fill(PANEL, 1)
    base.next_to(body, DOWN, buff=0)
    slot = Line(0.5 * LEFT, 0.5 * RIGHT).set_stroke(DIM, 3).move_to(base).shift(0.9 * RIGHT)
    led = Dot(radius=0.05, color=GREEN).move_to(base).shift(1.4 * LEFT)
    kb = Polygon([-1.55, 0, 0], [1.55, 0, 0], [1.35, 0.3, 0], [-1.35, 0.3, 0])
    kb.set_stroke(FG, 3).set_fill(PANEL, 1).next_to(base, DOWN, buff=0.16)
    keys = DashedLine(kb.get_left() + 0.35 * RIGHT, kb.get_right() + 0.35 * LEFT,
                      dash_length=0.12, dashed_ratio=0.6).set_stroke(DIM, 4)
    return VGroup(body, screen, prompt, base, slot, led, kb, keys)


def clock_icon(r=0.5, color=GOLD):
    """A small clock face; `.minute` is the hand that sweeps, `.face` the circle."""
    face = Circle(radius=r).set_stroke(color, 3)
    ticks = VGroup(*[
        Line(UP * r * 0.74, UP * r * 0.9).rotate(k * TAU / 12, about_point=ORIGIN).set_stroke(color, 2)
        for k in range(12)
    ])
    hour = Line(ORIGIN, UP * r * 0.42).rotate(-TAU / 3, about_point=ORIGIN).set_stroke(color, 4)
    minute = Line(ORIGIN, UP * r * 0.68).set_stroke(color, 3)
    g = VGroup(face, ticks, hour, minute)
    g.face, g.minute = face, minute
    return g


NAMES = ("insertion sort", "quicksort", "merge sort", "heapsort")
PARTS = ("Part 2", "Parts 3–4", "Part 5")


class ContestScene(NarratedScene):
    def construct(self):
        self.contestants()
        self.scoring()
        self.decstation()
        self.board()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # c1.contest.1 -- four names; the first three get their parts, heapsort is only named
    def contestants(self):
        with self.say("c1.contest.1") as c:
            names = VGroup(*[T(n, size=40, color=YELLOW) for n in NAMES])
            names.arrange(RIGHT, buff=0.75).move_to(0.4 * UP)
            y_tag = names.get_y() - 0.8
            tags = VGroup(*[T(p, size=30, color=GOLD) for p in PARTS])
            for t, nm in zip(tags, names):
                t.move_to([nm.get_x(), y_tag, 0])
            named = T("named only", size=30, color=DIM).move_to([names[3].get_x(), y_tag, 0])

            cues = list(NAMES) + ["three"]
            for i, nm in enumerate(names):
                c.wait_until(cues[i])
                self.play(FadeIn(nm, shift=0.3 * DOWN), run_time=min(0.9, 0.85 * c.until(cues[i + 1])))

            c.wait_until("three")
            self.play(LaggedStart(*[FadeIn(t, shift=0.25 * DOWN) for t in tags], lag_ratio=0.25),
                      run_time=min(1.5, 0.8 * c.until("heap")))
            c.wait_until("heap")
            self.play(names[3].animate.set_color(DIM), FadeIn(named, shift=0.25 * DOWN),
                      run_time=min(1.0, 0.8 * c.until("each")))
            c.wait_until("each")

    # c1.contest.2 -- the question becomes C(n); why comparisons; same count on every machine
    def scoring(self):
        with self.say("c1.contest.2") as c:
            q = T("How do we score them?", size=52).move_to(0.5 * UP)
            sweep_clear(self, time_span(FadeIn(q, shift=0.3 * DOWN), 0.5, 1.3), run_time=1.3)

            c.wait_until("count")
            cn = MathTex("C(n)", font_size=120, color=GOLD).move_to(0.6 * UP)
            cap1 = T("comparisons needed to sort n items", size=36).next_to(cn, DOWN, buff=0.5)
            self.play(q.animate.scale(0.75).move_to(3.15 * UP),
                      TransformFromCopy(select(q, "?")[0], cn), run_time=1.8)
            c.wait_until("number of comparisons")
            self.play(FadeIn(cap1, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("why")
            row = VGroup(cn.copy().scale(0.6), cap1.copy().scale(0.9)).arrange(RIGHT, buff=0.55)
            row.move_to(3.0 * UP)
            cmp = VGroup(MathTex("42", font_size=96, color=GOLD), MathTex(r"\le\,?", font_size=96),
                         MathTex("17", font_size=96, color=GOLD)).arrange(RIGHT, buff=0.45)
            cmp.move_to(1.3 * UP)
            cap2 = T("the only way a sort learns the order", size=34).next_to(cmp, DOWN, buff=0.45)
            self.play(FadeOut(q, shift=0.3 * UP),
                      cn.animate.move_to(row[0]).scale(0.6),
                      cap1.animate.move_to(row[1]).scale(0.9),
                      time_span(FadeIn(cmp, lag_ratio=0.3), 0.6, 1.8), run_time=1.8)
            c.wait_until("the only way")
            self.play(FadeIn(cap2, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("machine")
            machines = VGroup(*[machine_icon(w, h) for w, h in ((1.6, 1.0), (2.2, 1.3), (1.8, 1.12))])
            machines.arrange(RIGHT, buff=1.3, aligned_edge=DOWN).move_to(1.45 * DOWN)
            tag = T("Lecture 2: ignore constant factors", size=30, color=DIM)
            tag.next_to(machines, DOWN, buff=0.35)
            self.play(*set_alpha([cmp, cap2], 0.4),
                      LaggedStart(*[FadeIn(m, shift=0.3 * UP) for m in machines], lag_ratio=0.25),
                      run_time=1.6)
            c.wait_until("the same on every machine")
            self.play(*flash([m.count for m in machines]), FadeIn(tag, shift=0.25 * DOWN), run_time=1.3)

    # c1.contest.3 -- the DECstation and its clock; its seconds are only relative
    def decstation(self):
        with self.say("c1.contest.3") as c:
            dec = decstation().scale(1.15).move_to(1.2 * UP)
            clock = clock_icon().next_to(dec[0], RIGHT, buff=0.75).align_to(dec[0], UP)
            lab = T("DECstation", size=44).next_to(dec, DOWN, buff=0.4)
            mips = T("MIPS chip · an early RISC design", size=32).next_to(lab, DOWN, buff=0.3)
            rel = T("times: compare them only with each other", size=36, t2c={"times": GOLD})
            rel.move_to(2.95 * DOWN)
            self._rel = rel

            sweep_clear(self, time_span(FadeIn(dec, shift=0.3 * UP), 0.5, 1.4), run_time=1.4)
            c.wait_until("Deck Station")
            self.play(FadeIn(lab, shift=0.3 * DOWN), FadeIn(clock), run_time=1.0)
            self.play(Rotating(clock.minute, angle=-TAU, about_point=clock.face.get_center(),
                               run_time=min(1.6, max(0.6, 0.9 * c.until("mips")))))
            c.wait_until("mips")
            self.play(FadeIn(mips, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("relative")
            self.play(FadeIn(rel, shift=0.3 * UP), run_time=1.2)

    # c1.contest.4 -- the scoreboard, piece by piece, then the dashed floor
    def board(self):
        with self.say("c1.contest.4") as c:
            board = make_scoreboard()
            # the 'times' caption stays through this beat (it only just landed), leaves with the rows
            sweep_clear(self, time_span(GrowFromCenter(board.rule), 0.5, 1.6), keep=[self._rel], run_time=1.6)

            c.wait_until("rows")
            self.play(FadeIn(board.row_labels, shift=0.3 * RIGHT, lag_ratio=0.3),
                      FadeOut(self._rel, shift=0.3 * DOWN), run_time=1.5)
            c.wait_until("cols")
            self.play(FadeIn(board.col_headers[0], shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("we make them ourselves")
            self.play(FadeIn(board.tally_tag, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("less than or equal")
            self.play(FlashAround(select(board.tally_tag, "≤")[0], run_time=1.4, time_width=1.5))

            c.wait_until("time")
            self.play(FadeIn(board.col_headers[1], shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("blank")
            self.play(FadeIn(board.cells, scale=0.6, lag_ratio=0.15), run_time=1.6)

            c.wait_until("floor")
            self.play(Create(board.floor_line), FadeIn(board.floor_label, shift=0.3 * RIGHT), run_time=1.6)
            c.wait_until("How low could")
            self.play(FlashAround(board.floor_label, run_time=2, time_width=1.5))
