"""Chapter 2, scene 1: Hook. Clips c2.hook.1 – c2.hook.3.

Title card; ch1's scoreboard (make_scoreboard(bound="118,458") from ch1_s4_contest, scale 1, top 0.48
below the frame edge) with its solid floor "lower bound ≈ 118,458"; the DIM `rs` strip under it.
On {cards} the board shrinks into the top-left corner (4.4 wide), insertion sort row lit.

Cards (shared look with ch1_s8_recap's end card, built to its spec): RoundedRectangle
1.6 × 2.24, corner 0.14, fill #1B1F27, stroke FG 3; GOLD value T 100 centred, GOLD index
T 42 at the top-left. Fan: pivot 6.5 below the card centres, 10° apart, hand centre x -2.15,
cards' y -0.4 (the pivot stays put as the hand grows); loose 4 and 7 upright at x 1.57 / 3.47,
DIM T 30 "still to pick up" 0.42 under them.

Slide-into-place motion (s4 and s6 echo it): `card_move` below. The card lifts 0.4 (stroke
turns YELLOW), glides on a cubic Bézier whose last control point sits 0.55 above its slot,
so it drops straight in; its neighbours slide to their new fan slots in the middle of the
glide (window 0.1–0.65), opening the gap before it lands. 4: lift 0.9 s on {pick}, glide +
drop 1.8 s on {slot}; 7: lift, glide and drop in one ~2 s move.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402

# ---------------------------------------------------------------- cards (ch1 s8's spec)
CARD_W, CARD_H = 1.6, 2.24
CARD_FILL = "#1B1F27"
FAN_R = 6.5
FAN_STEP = 10 * DEGREES
HAND_X, CARD_Y = -2.15, -0.4
LOOSE_X = (1.57, 3.47)
LIFT = 0.4

ROW_Y, ROW_SCALE = -1.95, 0.68      # clip 3: the dealt row under the chain


def make_card(v):
    body = RoundedRectangle(corner_radius=0.14, width=CARD_W, height=CARD_H)
    body.set_stroke(FG, 3).set_fill(CARD_FILL, 1)
    big = T(str(v), 100, GOLD).move_to(body)
    tl = T(str(v), 42, GOLD).move_to(body.get_corner(UL) + np.array([0.29, -0.35, 0]))
    card = VGroup(body, tl, big)
    card.body, card.idx, card.num, card.v = body, tl, big, v
    card.base = card.copy()            # unrotated, at ORIGIN: every pose is computed from it
    card.pose = (np.zeros(3), 0.0, 1.0)
    return card


def fan_slots(n):
    """(centre, angle) of each card in an n-card hand, left to right (ch1 s8's fan)."""
    pivot = np.array([HAND_X, CARD_Y - FAN_R, 0])
    out = []
    for i in range(n):
        a = (n - 1) / 2 * FAN_STEP - i * FAN_STEP
        out.append((pivot + FAN_R * np.array([-np.sin(a), np.cos(a), 0]), a))
    return out


def apply_pose(card, pos, ang, scl):
    c, s = np.cos(ang), np.sin(ang)
    M = scl * np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])
    pos = np.asarray(pos, dtype=float)
    for sm, bm in zip(card.family_members_with_points(), card.base.family_members_with_points()):
        sm.set_points(bm.points @ M.T + pos)
    card.pose = (pos.copy(), ang, scl)
    return card


def glow(up=None, down=None):
    """Stroke of a moving card: FG 3 -> YELLOW 4.5 over `up`, back over `down` (alpha windows)."""
    def f(a):
        g = 1.0 if up is None else float(np.clip((a - up[0]) / (up[1] - up[0]), 0, 1))
        if down is not None:
            g *= 1 - float(np.clip((a - down[0]) / (down[1] - down[0]), 0, 1))
        return ManimColor(FG).interpolate(ManimColor(YELLOW), g), 3 + 1.5 * g
    return f


def card_move(card, pos, ang=0.0, scl=None, rise=0.0, fall=0.0, window=(0.0, 1.0),
              stroke=None, z_end=None, run_time=1.5):
    """Move a card to a pose along a cubic Bézier: `rise` lifts it on the way out, `fall`
    drops it straight into place at the end. `window`: the part of the play it moves in."""
    p0, a0, s0 = card.pose
    p1 = np.asarray(pos, dtype=float)
    s1 = s0 if scl is None else scl
    a1 = ang
    ctrl = [p0, p0 + rise * UP, p1 + fall * UP, p1]
    w0, w1 = window

    def upd(m, alpha):
        t = smooth(float(np.clip((alpha - w0) / (w1 - w0), 0, 1)))
        u = 1 - t
        p = u ** 3 * ctrl[0] + 3 * u * u * t * ctrl[1] + 3 * u * t * t * ctrl[2] + t ** 3 * ctrl[3]
        apply_pose(m, p, a0 + (a1 - a0) * t, s0 + (s1 - s0) * t)
        if stroke is not None:
            col, w = stroke(alpha)
            m.body.set_stroke(col, w)
        if z_end is not None and alpha >= 0.85:
            m.set_z_index(z_end)

    return UpdateFromAlphaFunc(card, upd, run_time=run_time, rate_func=linear)


def card_proxy(card):
    """Off-screen stand-in shaped like a ConsCell's parts (box, ptr, dot, label) for
    TransformFromCopy(card -> cell)."""
    b = card.body.copy()
    dot = Dot(card.num.get_center(), radius=0.02, color=FG)
    return VGroup(b, b.copy(), dot, card.num.copy())


def tag(text, color):
    t = T(text, 36, color)
    box = SurroundingRectangle(t, buff=0.2, corner_radius=0.14)
    box.set_stroke(color, 2).set_fill(color, 0.1)
    return VGroup(box, t)


class Hook(NarratedScene):
    def construct(self):
        self.clip_title()
        self.clip_cards()
        self.clip_chain()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c2.hook.1 ──────────────────────────────────────────────────────────────
    def clip_title(self):
        card = title_card("Part 2 · Insertion sort")
        board = make_scoreboard(bound="118,458")   # as ch1 s6 leaves it: solid GOLD floor
        board.to_edge(UP, buff=0.48)
        strip = Mono("rs = [1484786315.; 925166085.; 1614852353.; …]", size=28, color=DIM)
        strip.next_to(board, DOWN, buff=0.3).set_x(0)
        self.board, self.strip = board, strip

        with self.say("c2.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),
                      time_span(FadeIn(card.course, shift=0.2 * DOWN), 0.6, 1.4), run_time=1.4)
            self.play(FadeIn(card.part, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("last")
            sweep_clear(self, time_span(FadeIn(board, shift=0.2 * UP), 0.6, 1.6), run_time=1.6)
            c.wait_until("N log N")
            line = board.floor_line
            self.play(VShowPassingFlash(line.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      FlashAround(VGroup(board.floor_label, board.floor_value), color=GOLD,
                                  time_width=1.5),
                      run_time=min(2.0, c.until("random")))
            c.wait_until("random")
            self.play(FlashAround(board.col_headers[0], time_width=1.5),
                      time_span(FadeIn(strip, shift=0.6 * RIGHT), 0.5, 1.6), run_time=2.0)

    # ── c2.hook.2 ──────────────────────────────────────────────────────────────
    def clip_cards(self):
        board, strip = self.board, self.strip

        # the board's corner pose: shrunk, insertion sort lit, the other rows dimmed
        target = board.copy()
        fam = {id(m): i for i, m in enumerate(board.get_family())}
        tfam = target.get_family()
        for part in (board.row_labels[1], board.row_labels[2], board.cells[1], board.cells[2]):
            for sm in part.get_family():
                tm = tfam[fam[id(sm)]]
                tm.set_fill(opacity=tm.get_fill_opacity() * 0.3)
                tm.set_stroke(opacity=tm.get_stroke_opacity() * 0.3)
        target.scale(4.4 / board.width).to_corner(UL, buff=0.4)
        lit = VGroup(tfam[fam[id(board.row_labels[0])]], tfam[fam[id(board.cells[0])]])
        hl = SurroundingRectangle(lit, buff=0.1, corner_radius=0.06)
        hl.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12).set_z_index(-1)
        board.target = target

        cards = {v: make_card(v) for v in (3, 5, 9, 4, 7)}
        for v, (ctr, a) in zip((3, 5, 9), fan_slots(3)):
            apply_pose(cards[v], ctr, a, 1.0)
        for v, x in zip((4, 7), LOOSE_X):
            apply_pose(cards[v], [x, CARD_Y, 0], 0.0, 1.0)
        for v, z in ((3, 10), (5, 11), (9, 12), (4, 13), (7, 14)):
            cards[v].set_z_index(z)
        still = T("still to pick up", 30, DIM)
        still.move_to([sum(LOOSE_X) / 2, CARD_Y - CARD_H / 2 - 0.42, 0])
        self.cards = cards

        with self.say("c2.hook.2") as c:
            self.play(MoveToTarget(board), time_span(FadeIn(hl), 1.1, 1.7), run_time=1.7)
            self.hl = hl
            c.wait_until("It sorts")
            deal = [time_span(FadeIn(cards[v], shift=0.3 * UP), 0.15 * k, 0.9 + 0.15 * k)
                    for k, v in enumerate((3, 5, 9, 4, 7))]
            self.play(*deal, time_span(FadeIn(still, shift=0.2 * DOWN), 1.3, 2.1), run_time=2.1)

            # {pick}: the 4 lifts
            c.wait_until("pick")
            c4 = cards[4]
            c4.set_z_index(30)
            self.play(card_move(c4, c4.pose[0] + LIFT * UP, 0.0, stroke=glow(up=(0, 1))),
                      FadeOut(strip, shift=0.3 * DOWN), run_time=0.9)

            # {slot}: it glides over and drops in between the 3 and the 5, which part
            c.wait_until("slot")
            s4 = fan_slots(4)
            cards[5].set_z_index(12)
            cards[9].set_z_index(13)
            self.play(card_move(c4, *s4[1], fall=0.55, stroke=glow(down=(0.8, 1.0)), z_end=11),
                      *[card_move(cards[v], *s4[i], window=(0.1, 0.65))
                        for i, v in ((0, 3), (2, 5), (3, 9))],
                      still.animate.move_to([LOOSE_X[1], still.get_y(), 0]),
                      run_time=1.8)

            # then the 7, the same way, in one move, between the 5 and the 9
            self.wait(0.25)
            s5 = fan_slots(5)
            c7 = cards[7]
            c7.set_z_index(30)
            cards[9].set_z_index(14)
            rt = max(1.3, min(2.0, c.until("order") - 0.1))
            self.play(card_move(c7, *s5[3], rise=0.6, fall=0.55,
                                stroke=glow(up=(0, 0.2), down=(0.8, 1.0)), z_end=13),
                      *[card_move(cards[v], *s5[i], window=(0.25, 0.75))
                        for i, v in ((0, 3), (1, 4), (2, 5), (4, 9))],
                      FadeOut(still, run_time=0.6), run_time=rt)

            # {order}: the hand reads 3 4 5 7 9
            c.wait_until("order")
            tick = check_mark(GREEN)
            words = T("always in order", 36, GREEN)
            ok = VGroup(tick, words).arrange(RIGHT, buff=0.25)
            hand_right = max(cards[v].get_right()[0] for v in (3, 4, 5, 7, 9))
            ok.move_to([hand_right + 0.7, CARD_Y, 0], aligned_edge=LEFT)
            self.play(Create(tick), FadeIn(words, shift=0.3 * LEFT), run_time=1.0)
            self.ok = ok

    # ── c2.hook.3 ──────────────────────────────────────────────────────────────
    def clip_chain(self):
        cards, board = self.cards, self.board
        dealt = [cards[v] for v in (3, 5, 9, 4, 7)]
        chain = ConsChain([3, 5, 9, 4, 7])
        xs = [cell.box.get_x() for cell in chain.cells]

        with self.say("c2.hook.3", gap=2.0) as c:
            # {chain}: back to the dealt order, laid out in a row under where the chain goes
            for k, cd in enumerate(dealt):
                cd.set_z_index(30 if cd.v in (4, 7) else 20 + k)
            moves = [card_move(cd, [x, ROW_Y, 0], 0.0, ROW_SCALE,
                               rise=0.5 if cd.v in (4, 7) else 0.0, window=(0.15, 1.0))
                     for cd, x in zip(dealt, xs)]
            self.play(time_span(FadeOut(self.ok), 1.0, 1.7), *moves, run_time=1.7)
            for k, cd in enumerate(dealt):
                cd.set_z_index(20 + k)

            # each card becomes a cell as its number is said
            offs = [c.until(w, floor=0.0) for w in ("three", "five", "nine", "four", "seven")]
            offs = [max(0.0, o - 0.25) for o in offs]
            for i in range(1, 5):
                offs[i] = max(offs[i], offs[i - 1] + 0.35)
            anims = []
            for i, (cd, o) in enumerate(zip(dealt, offs)):
                anims.append(time_span(TransformFromCopy(card_proxy(cd), chain.cells[i]), o, o + 1.1))
                anims.append(time_span(GrowArrow(chain.arrows[i]), o + 0.8, o + 1.3))
            end = offs[-1] + 1.3
            anims.append(time_span(FadeIn(chain.nil, shift=0.2 * LEFT), end - 0.3, end + 0.4))
            self.play(*anims, run_time=end + 0.4)
            settle(self, chain)

            # {ask}: two questions under the chain
            c.wait_until("ask")
            q1 = tag("in OCaml?", BLUE)
            q2 = tag("how many comparisons?", GOLD)
            VGroup(q1, q2).arrange(RIGHT, buff=1.0).move_to([0, ROW_Y + 0.1, 0])
            self.play(*[FadeOut(cd, shift=0.3 * DOWN) for cd in dealt],
                      time_span(FadeIn(q1, shift=0.3 * DOWN), 0.4, 1.2),
                      time_span(FadeIn(q2, shift=0.3 * DOWN), 0.8, 1.6), run_time=1.6)
            c.wait_until("how many")
            self.play(FlashAround(board.cells[0][0], color=GOLD, time_width=1.5),
                      FlashAround(q2, color=GOLD, time_width=1.5),
                      run_time=min(1.8, c.until()))
