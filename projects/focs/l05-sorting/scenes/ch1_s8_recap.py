"""Chapter 1, scene 8: Recap, and the end card (ch2's hand of cards). Clips c1.recap.1 – c1.recap.2.

Layout: "Recap" title at the top (T 52, y 3.3); six rows below it (pitch 1.05 from y 2.2),
each a small icon (≤ 2.0 × 0.82) at the left and its line (T 34 / MathTex) left-aligned
beside it. On {next} the rows dim and the title becomes "Next: insertion sort". On {cards}
the rows sweep out and the end card comes in: five playing cards, the 3 5 9 fanned in the
hand, the 4 and 7 face up to the right ("still to pick up"); the 4 lifts and slots in
between the 3 and the 5. End card held ~8 s, then fades.

Card design (shared look with ch2_s1_hook): RoundedRectangle 1.6 × 2.24, corner 0.14,
fill #1B1F27, stroke FG 3; GOLD value T 100 in the centre, GOLD corner index T 42 at the top-left
(no turned bottom-right index: an upside-down 9 reads as 6). Fan: pivot 6.5 below the card centres, cards 10° apart
(3 cards: +10, 0, -10; 4 cards: +15, +5, -5, -15), each card above its left neighbour;
hand centre x -2.15, cards' y -0.4; loose 4 and 7 upright at x 1.57 / 3.47; DIM T 30
"still to pick up" centred under them, 0.42 below the cards.
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

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402  the shared scoreboard (read-only)
from scenes.ch1_s2_why import (icon_dups, icon_graphics, icon_merge, icon_search,  # noqa: E402
                               icon_table)  # s2's use icons (read-only)


ICON_W, ICON_H = 2.0, 0.82
ROW_Y0, ROW_PITCH = 2.2, 1.05
TEXT_GAP = 0.45
TITLE_Y = 3.3

CARD_W, CARD_H = 1.6, 2.24
CARD_FILL = "#1B1F27"
FAN_R = 6.5
HAND_X, CARD_Y = -2.15, -0.4
LOOSE_X = (1.57, 3.47)


# ── recap icons ─────────────────────────────────────────────────────────────────
def fit(m, w=ICON_W, h=ICON_H):
    if m.width / w > m.height / h:
        m.scale_to_fit_width(w, scale_stroke=True)
    else:
        m.scale_to_fit_height(h, scale_stroke=True)
    return m


def uses_icon():
    """s2's five uses (its own icons), in a row: search, merging, duplicates, tables, graphics."""
    row = VGroup(icon_search(), icon_merge(), icon_dups(), icon_table(), icon_graphics())
    return fit(row.arrange(RIGHT, buff=0.22))


def pill(left, right, y, h, color):
    w = max(right - left, h)
    return (RoundedRectangle(corner_radius=h / 2, width=w, height=h).set_stroke(width=0)
            .set_fill(color, 1).move_to([(left + right) / 2, y, 0]))


def schematic(mob, k=0.5):
    """A thumbnail of `mob`: every Text in it becomes a pill of its colour (k × its height)."""
    for parent in mob.get_family():
        for i, sub in enumerate(parent.submobjects):
            if isinstance(sub, Text):
                parent.submobjects[i] = pill(sub.get_left()[0], sub.get_right()[0], sub.get_y(),
                                             k * sub.height, sub[0].get_fill_color())
    return mob


def code_thumb(code):
    """A thumbnail of a Code: each run of same-coloured glyphs on a line becomes a pill."""
    pitch = code.height / max(1, len(code.src.split("\n")))
    bars = VGroup()
    for i in range(len(code.src.split("\n"))):
        glyphs = list(code.line(i))
        y = VGroup(*[g.copy() for g in glyphs]).get_y()
        runs = []
        for g in glyphs:
            col = g.get_fill_color().to_hex()
            if runs and runs[-1][0] == col and g.get_left()[0] - runs[-1][2] < 0.06:
                runs[-1][2] = g.get_right()[0]
            else:
                runs.append([col, g.get_left()[0], g.get_right()[0]])
        for col, l, r in runs:
            bars.add(pill(l, r, y, 0.42 * pitch, col))
    return bars


def primes_icon():
    """s3's 16-box prime row, first probe YELLOW, the thrown-away half dim, a GOLD halving brace."""
    boxes = VGroup(*[Square(0.46).set_stroke(BLUE, 6).set_fill(BG, 1) for _ in range(16)])
    boxes.arrange(RIGHT, buff=0)
    dots = VGroup(*[Dot(b.get_center(), radius=0.08, color=GOLD) for b in boxes])
    boxes[7].set_stroke(YELLOW, 8)
    for i in range(7):
        boxes[i].set_stroke(opacity=0.35)
        dots[i].set_opacity(0.35)
    brace = Brace(VGroup(*boxes[8:]), DOWN, buff=0.12, color=GOLD)
    return fit(VGroup(boxes, dots, brace))


def scoreboard_icon():
    return fit(schematic(make_scoreboard()))


def tree_icon():
    """s5's decision tree for three items: question boxes, six GREEN leaves."""
    def node(x, y):
        return RoundedRectangle(corner_radius=0.04, width=0.3, height=0.16).set_stroke(YELLOW, 2) \
            .set_fill(BG, 1).move_to([x, y, 0])

    def leaf(x, y):
        return Dot([x, y, 0], radius=0.055, color=GREEN)

    root = node(0, 0.32)
    a, b = node(-0.5, 0.04), node(0.5, 0.04)
    a2, b2 = node(-0.25, -0.24), node(0.75, -0.24)
    leaves = [leaf(-0.75, -0.24), leaf(0.25, -0.24),
              leaf(-0.4, -0.5), leaf(-0.1, -0.5), leaf(0.6, -0.5), leaf(0.9, -0.5)]
    pairs = [(root, a), (root, b), (a, leaves[0]), (a, a2), (b, leaves[1]), (b, b2),
             (a2, leaves[2]), (a2, leaves[3]), (b2, leaves[4]), (b2, leaves[5])]
    edges = VGroup(*[Line(p.get_bottom(), q.get_center() if isinstance(q, Dot) else q.get_top())
                     .set_stroke(DIM, 2) for p, q in pairs])
    return fit(VGroup(edges, root, a, b, a2, b2, *leaves))


def bars_icon():
    """s6's sixteen bars, bar k of height log2 k, under the GOLD n log n ceiling."""
    unit, pitch, w = 0.2, 0.112, 0.075
    base_y = -0.4
    bars = VGroup()
    for k in range(2, 17):
        h = unit * np.log2(k)
        bars.add(Rectangle(width=w, height=h).set_stroke(width=0).set_fill(BLUE, 1)
                 .move_to([(k - 1) * pitch, base_y + h / 2, 0]))
    x0, x1 = -w / 2 - 0.04, 15 * pitch + w / 2 + 0.04
    base = Line([x0, base_y, 0], [x1, base_y, 0]).set_stroke(DIM, 2)
    ceil = Line([x0, base_y + 4 * unit, 0], [x1, base_y + 4 * unit, 0]).set_stroke(GOLD, 2)
    return fit(VGroup(base, bars, ceil))


def rs_icon():
    """s7's printout, its left-hand columns (each line a prefix of the real one)."""
    code = Code("val rs : float list =\n  [1484786315.; 925166085.;\n   789328014.; 570809709.;", size=32)
    return fit(code_thumb(code))


# ── the end card ────────────────────────────────────────────────────────────────
def make_card(v):
    body = RoundedRectangle(corner_radius=0.14, width=CARD_W, height=CARD_H)
    body.set_stroke(FG, 3).set_fill(CARD_FILL, 1)
    big = T(str(v), 100, GOLD).move_to(body)
    tl = T(str(v), 42, GOLD).move_to(body.get_corner(UL) + np.array([0.29, -0.35, 0]))
    card = VGroup(body, tl, big)
    card.angle = 0.0
    return card


def fan_slots(n):
    step = 10 * DEGREES
    pivot = np.array([HAND_X, CARD_Y - FAN_R, 0])
    out = []
    for i in range(n):
        a = (n - 1) / 2 * step - i * step
        out.append((a, pivot + FAN_R * np.array([-np.sin(a), np.cos(a), 0])))
    return out


def place(card, angle, center):
    card.rotate(angle - card.angle)
    card.angle = angle
    card.move_to(center)
    return card


class Recap(NarratedScene):
    def construct(self):
        self.build_recap()
        self.clip_recap()
        self.clip_next()
        self.wait(7.6)                                     # the end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── layout ──────────────────────────────────────────────────────────────────
    def build_recap(self):
        self.title = T("Recap", 52).move_to(UP * TITLE_Y)
        icons = [uses_icon(), primes_icon(), scoreboard_icon(), tree_icon(), bars_icon(), rs_icon()]
        r5 = VGroup(MathTex(r"C(n) \ge \log_2(n!) \approx n\log_2 n", font_size=44),
                    T("≈ 118,458 for 10,000 items", 34, GOLD)).arrange(RIGHT, buff=0.55)
        texts = [
            T("sorting serves search, merging, duplicates, tables", 34),
            T("binary search: O(log n), needs arrays or trees", 34, t2c={"O(log n)": GOLD}),
            T("we count comparisons", 34, t2c={"comparisons": GOLD}),
            MathTex(r"2^{C(n)} \ge n!", font_size=50, color=YELLOW),
            r5,
            T("10,000 random numbers to race on", 34, t2c={"10,000": GOLD}),
        ]
        x_text = ICON_W / 2 + TEXT_GAP
        for i, (icon, text) in enumerate(zip(icons, texts)):
            y = ROW_Y0 - i * ROW_PITCH
            icon.move_to([0, y, 0])
            text.move_to([0, y, 0])
            text.shift((x_text - text.get_left()[0]) * RIGHT)
        block = VGroup(*icons, *texts)
        if block.width > 13.0:
            block.scale_to_fit_width(13.0)
        block.shift(-block.get_center()[0] * RIGHT)
        self.icons, self.texts = icons, texts
        self.r5_formula, self.r5_note = r5[0], r5[1]

    def row_in(self, i, lag=0.35):
        self.play(FadeIn(self.icons[i], scale=0.8, run_time=1.0),
                  time_span(FadeIn(self.texts[i], shift=0.2 * DOWN), lag, lag + 1.0))

    # ── c1.recap.1 ──────────────────────────────────────────────────────────────
    def clip_recap(self):
        with self.say("c1.recap.1") as c:
            self.play(FadeIn(self.title, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("r1")
            self.play(FadeIn(self.icons[0], lag_ratio=0.12, run_time=1.8),
                      time_span(FadeIn(self.texts[0], shift=0.2 * DOWN), 0.4, 1.6))
            c.wait_until("r2")
            self.row_in(1)
            c.wait_until("r3")
            self.row_in(2)
            c.wait_until("r4")
            self.play(FadeIn(self.icons[3], scale=0.8), run_time=1.0)
            c.wait_until("so two")
            self.play(Write(self.texts[3]), run_time=min(1.6, 0.7 * c.until("r5")))
            c.wait_until("r5")
            self.play(FadeIn(self.icons[4], scale=0.8, run_time=1.0),
                      time_span(FadeIn(self.r5_formula, shift=0.2 * DOWN), 0.35, 1.4))
            c.wait_until("unavoidable")
            self.play(FadeIn(self.r5_note, shift=0.3 * LEFT), run_time=1.0)
            c.wait_until("r6")
            self.row_in(5, lag=0.0)

    # ── c1.recap.2 ──────────────────────────────────────────────────────────────
    def clip_next(self):
        nxt = T("Next: insertion sort", 52, t2c={"insertion sort": YELLOW}).move_to(UP * TITLE_Y)
        recap_parts = [*self.icons, *self.texts[:4], self.r5_formula, self.r5_note, self.texts[5]]

        cards = {v: make_card(v) for v in (3, 5, 9, 4, 7)}
        for card, (a, ctr) in zip((cards[3], cards[5], cards[9]), fan_slots(3)):
            place(card, a, ctr)
        for v, x in zip((4, 7), LOOSE_X):
            place(cards[v], 0.0, [x, CARD_Y, 0])
        for v, z in ((3, 1), (4, 2), (5, 3), (9, 4), (7, 1)):
            cards[v].set_z_index(z)
        tag = T("still to pick up", 30, DIM).move_to([sum(LOOSE_X) / 2, CARD_Y - CARD_H / 2 - 0.42, 0])

        with self.say("c1.recap.2") as c:
            self.play(*set_alpha(recap_parts, DIMMED), FadeTransform(self.title, nxt), run_time=1.2)
            c.wait_until("cards")
            deal = [time_span(FadeIn(cards[v], shift=0.3 * UP), 0.4 + 0.15 * k, 1.3 + 0.15 * k)
                    for k, v in enumerate((3, 5, 9, 4, 7))]
            sweep_clear(self, *deal, time_span(FadeIn(tag, shift=0.2 * DOWN), 1.4, 2.2),
                        keep=[nxt], run_time=2.2)
            c.wait_until("picking up")
            self.play(cards[4].animate.shift(0.45 * UP), run_time=0.8)
            c.wait_until("slotting")
            for card, (a, ctr) in zip((cards[3], cards[4], cards[5], cards[9]), fan_slots(4)):
                card.generate_target()
                place(card.target, a, ctr)
            self.play(*[MoveToTarget(cards[v]) for v in (3, 4, 5, 9)],
                      tag.animate.move_to([LOOSE_X[1], tag.get_y(), 0]),
                      run_time=max(1.2, min(1.8, c.until())))
            for v in (3, 4, 5, 9):
                cards[v].angle = cards[v].target.angle
