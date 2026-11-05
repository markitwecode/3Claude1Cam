"""Chapter 6, scene 2: two accumulators, the faster change (In [73]). Clips c6.accs.1 – c6.accs.5.

HAND-OFF TO s3 (ch6_s3_trace): the scene ends on the call alone, held ~1 s, then faded.
  call = Code("change [2; 1] 4 [] []", size=32).move_to([0, 3.3, 0])
  then call.find("change") -> YELLOW, call.find("[]", nth=0) and call.find("[]", nth=1) -> TEAL;
  every other glyph keeps Code's default highlighting. No labels, nothing else on screen.

IN [73] TOKEN COLOURS (s4 reuses them): Code(SRC, size=CODE_SIZE) with default highlighting
  (keywords BLUE, numbers GOLD, `[]` and `::` TEAL), then
  every `change` YELLOW · every `chg` GOLD ("coins so far (this path)", the GOLD coins) ·
  every `chgs` TEAL ("solutions so far", ch5's TEAL solution frames) · `amt < 0` (line 4) RED.
  Placed centred (it is 13.2 wide: left ~-6.6) with its top at CODE_TOP = 2.62.
  Departure: Code 28 does not fit (61-column lines are ~14.2 wide at 28), so 26, the largest that
  fits; top lowered from 3.25 to CODE_TOP so the two accumulator labels can sit above the header.

Layout: In [73] across the top (y 2.62 ... ~-0.75); the labels "coins so far (this path)"
(GOLD, up-left of `chg`) and "solutions so far" (TEAL, up-right of `chgs`) above the header, with
short arrows, for the whole scene. The band under the code changes per clip:
accs.1-2  the picture under the code: a GOLD path box (ch5's solution box) above a TEAL frame of
          finished boxes (ch5's list of solutions); the path box turns TEAL and drops into the
          frame's front (chg::chgs); a second path goes RED and leaves, the frame flashes.
accs.3    `amt < 0` RED, a DIM ghost `amt < c` ("last time") right of line 4; the frame slides
          1.5 right and the two-node strip (ch5 tree style, levels 1.4 apart) comes in at the left,
          under line 4: "1, [5; 2]" -> use 5 -> RED "-4, [5; 2]", a TEAL arrow
          hands the frame back; "caught one call later" under the RED node.
accs.4    sweep; a ch5-style fork left of centre (line 6 hangs over the right half): parent
          "amt, c::till", use child "amt - c, c::till" (left),
          skip child "amt, till" (right), YELLOW boxes on the two calls in the code; the TEAL feed
          arrow skip -> use, "chgs"; a DIM `@` under the parent is crossed out.
accs.5    code lines 1-6 fade, the header stays; OCaml's reply (Code 26, wrapped after the last
          `->`) in the lower half, the four header names fly down as labels above the argument
          types; GREEN underlines on chg's and chgs' types, a GREEN arc from chgs' type down to
          the result type on the next line; then the header leaves and the call comes in at (0, 3.3) with
          "no coins yet" / "no solutions yet".
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, select, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = (
    "let rec change till amt chg chgs =\n"
    "  match till, amt with\n"
    "  | _       , 0   -> chg::chgs\n"
    "  | []      , _   -> chgs\n"
    "  | c::till , amt -> if amt < 0 then chgs\n"
    "                     else change (c::till) (amt - c) (c::chg)\n"
    "                                 (change till amt chg chgs)"
)
# OCaml prints the first two lines as one 76-column line; wrapped after the last `->` with
# OCaml's 2-space indent (as ch3 wraps long replies) so it reads at the code's size and all four
# argument types share one line.
REPLY = ("val change : int list -> int -> int list -> int list list ->\n"
         "  int list list =\n"
         "  <fun>")
CALL = "change [2; 1] 4 [] []"

CODE_SIZE = 26
CODE_LEFT, CODE_TOP = -6.5, 2.62
LABEL = 30
REPLY_SIZE = 26
REPLY_Y = -0.8               # centre of the reply's first line

COIN_R = 0.42                # ch1's coin; boxes use it at x0.6 (ch5)
COIN_LABEL = 40              # 24 after the x0.6
PIC_LEFT = -1.8              # the solutions frame's left edge (accs.1-2; it moves 1.5 right in accs.3)
PIC_SHIFT = 1.5
NODE = 30


# ── shared looks (ch1's coin, ch5's solution box / list of solutions / tree node) ───────────
def coin(v, r=COIN_R):
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def solution(vals, color=TEAL):
    """Coins (x0.6) in a row inside a rounded box (ch5: TEAL, corner 0.1, stroke 3, pad 0.12)."""
    coins = VGroup(*[coin(v).scale(0.6) for v in vals]).arrange(RIGHT, buff=0.1)
    rect = RoundedRectangle(corner_radius=0.1, width=coins.width + 0.24,
                            height=coins.height + 0.24).set_stroke(color, 3).move_to(coins)
    return VGroup(rect, coins)


SOL_H = 2 * COIN_R * 0.6 + 0.24


def frame_for(width, y):
    """ch5's list-of-solutions frame (corner 0.15, stroke 4, pad 0.2), left edge at PIC_LEFT."""
    return RoundedRectangle(corner_radius=0.15, width=width, height=SOL_H + 0.4).set_stroke(TEAL, 4) \
        .move_to([PIC_LEFT + width / 2, y, 0])


def row_width(boxes):
    return sum(b.width for b in boxes) + 0.2 * (len(boxes) - 1) + 0.4


def place_row(boxes, y):
    x = PIC_LEFT + 0.2
    for b in boxes:
        b.move_to([x + b.width / 2, y, 0])
        x += b.width + 0.2


def node(amt, till, at, color=None):
    """ch5's tree node: Mono 30 "amount, till" (amount GOLD, till TEAL) in a BLUE rounded box."""
    txt = Mono(f"{amt}, {till}", NODE)
    n = sum(not ch.isspace() for ch in amt)
    for i, g in enumerate(txt):
        g.set_color(GOLD if i < n else FG if i == n else TEAL)
    box = RoundedRectangle(corner_radius=0.15, width=txt.width + 0.5, height=0.62).set_stroke(BLUE, 3)
    txt.move_to(box)
    if color is not None:
        txt.set_color(color)
        box.set_stroke(color)
    return VGroup(box, txt).move_to(at)


def edge(parent, child, side, color=FG, width=4, opacity=1.0):
    a = parent[0].get_bottom() + RIGHT * 0.35 * side
    return Line(a, child[0].get_top()).set_stroke(color, width, opacity=opacity)


def edge_label(e, word, v, side):
    lab = T(f"{word} {v}", LABEL)
    select(lab, str(v))[0].set_color(GOLD)
    d = e.get_end() - e.get_start()
    if abs(d[0]) > 1.5 * abs(d[1]):
        lab.next_to(e.point_from_proportion(0.65), UL if side < 0 else UR, buff=0.06)
    else:
        lab.next_to(e.point_from_proportion(0.5), LEFT if side < 0 else RIGHT, buff=0.18).shift(0.1 * UP)
    return lab


def pointer(start, end, color):
    return Arrow(start, end, buff=0, stroke_width=3, tip_length=0.14, color=color,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20)


def G(glyphs):
    return VGroup(*glyphs)


def lag_rate(a, b):
    return lambda t: smooth(min(1.0, max(0.0, (t - a) / (b - a))))


def fit(c, cue, cap, lo=0.5, frac=0.85):
    return max(lo, min(cap, frac * c.until(cue)))


class TwoAccumulators(NarratedScene):
    def construct(self):
        code = Code(SRC, size=CODE_SIZE)
        left = CODE_LEFT if code.width <= 13.1 else -code.width / 2
        code.shift(RIGHT * (left - code.get_left()[0]) + UP * (CODE_TOP - code.get_top()[1]))
        for i in (0, 5, 6):
            for g in code.find("change", line=i):
                g.set_color(YELLOW)
        self.code = code
        self.cb = code.get_bottom()[1]
        f = code.find
        h = f("till amt chg chgs", 0)
        self.h_names = [h[0:4], h[4:7], h[7:10], h[10:14]]
        c2 = f("chg::chgs", 2)
        l6 = f("chg chgs", 6)
        self.chg_occ = [h[7:10], c2[0:3], f("(c::chg)", 5)[4:7], l6[0:3]]
        self.chgs_occ = [h[10:14], c2[5:9], f("chgs", 3), f("chgs", 4), l6[3:7]]
        self.zero = f("0", 2)
        self.lt0 = f("amt < 0", 4)
        self.use_call = f("change (c::till) (amt - c) (c::chg)", 5)
        self.skip_call = f("(change till amt chg chgs)", 6)

        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

        # end on the call alone (s3 fades it back in), then an empty frame
        self.wait(2.3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.call], run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(self.call), run_time=1.0)
        self.wait(0.15)

    # ── c6.accs.1: the code, two new arguments, the two labels and the picture ─────────────
    def clip1(self):
        code = self.code
        chg_h, chgs_h = G(self.h_names[2]), G(self.h_names[3])

        lab1 = T("coins so far (this path)", LABEL, GOLD)
        lab1.move_to([chg_h.get_center()[0] - 0.3 - lab1.width / 2, CODE_TOP + 0.62, 0])
        arr1 = pointer([lab1.get_right()[0] - 0.2, lab1.get_bottom()[1] - 0.04, 0],
                       chg_h.get_top() + 0.07 * UP, GOLD)
        lab2 = T("solutions so far", LABEL, TEAL)
        lab2.move_to([chgs_h.get_center()[0] + 0.3 + lab2.width / 2, CODE_TOP + 0.62, 0])
        arr2 = pointer([lab2.get_left()[0] + 0.2, lab2.get_bottom()[1] - 0.04, 0],
                       chgs_h.get_top() + 0.07 * UP, TEAL)
        self.labels = [lab1, arr1, lab2, arr2]

        # the picture: the current path above the frame of finished solutions
        path_y, frame_y = self.cb - 0.6, self.cb - 1.95
        self.path_y, self.frame_y = path_y, frame_y
        boxes = [solution([1, 1, 2]), solution([1, 1, 1, 1])]
        place_row(boxes, frame_y)
        frame = frame_for(row_width(boxes), frame_y)
        self.stack = VGroup(frame, *boxes)
        self.frame, self.boxes = frame, boxes
        path = solution([2, 2], color=GOLD)
        path.move_to([PIC_LEFT + 0.2 + path.width / 2, path_y, 0])
        self.path = path

        with self.say("c6.accs.1") as c:
            # revealed clause by clause: header, match, clause 1, clause 2, clause 3
            groups = [code.line(0), code.line(1), code.line(2), code.line(3),
                      [*code.line(4), *code.line(5), *code.line(6)]]
            for grp in groups:
                for g in grp:
                    g.set_opacity(0)
            self.add(code)
            anims = []
            for k, grp in enumerate(groups):
                a = k * 0.16
                anims += [g.animate(rate_func=lag_rate(a, a + 0.36)).set_opacity(1) for g in grp]
            self.play(*anims, run_time=min(2.8, 0.95 * c.until("args")))

            c.wait_until("args")
            self.play(FlashUnder(G([*self.h_names[0], *self.h_names[1]]), color=FG),
                      run_time=fit(c, "it takes two new arguments", 1.5))
            c.wait_until("it takes two new arguments")
            self.play(FlashAround(G([*self.h_names[2], *self.h_names[3]]), color=YELLOW,
                                  time_width=1.5), run_time=1.6)

            c.wait_until("chg")
            self.play(*[a for g in self.chg_occ for a in recolor(g, GOLD)],
                      FadeIn(lab1, shift=0.3 * DOWN), GrowArrow(arr1), run_time=1.4)
            c.wait_until("It holds the coins")
            self.play(FadeIn(path, target_position=chg_h.get_center(), scale=0.3), run_time=1.6)

            c.wait_until("chgs")
            self.play(*[a for g in self.chgs_occ for a in recolor(g, TEAL)],
                      FadeIn(lab2, shift=0.3 * DOWN), GrowArrow(arr2), run_time=1.4)
            c.wait_until("holds the solutions found")
            self.play(FadeIn(self.stack, target_position=chgs_h.get_center(), scale=0.3),
                      run_time=min(1.6, max(0.8, c.remaining - 0.2)))

    # ── c6.accs.2: clause 1 records the path, clause 2 adds nothing ────────────────────────
    def clip2(self):
        code, path, frame = self.code, self.path, self.frame
        with self.say("c6.accs.2") as c:
            self.box = token_box(code.line(2), code.line(2))
            self.play(FadeIn(self.box), run_time=1.0)

            c.wait_until("When the amount reaches zero")
            self.play(FlashAround(G(self.zero), color=GOLD, time_width=1.5), run_time=1.4)
            c.wait_until("so they make a solution")
            self.play(path[0].animate.set_stroke(TEAL), FlashAround(path, color=TEAL, time_width=1.5),
                      run_time=1.3)

            c.wait_until("record")
            boxes = self.boxes
            dx = path.width + 0.2
            new_frame = frame_for(row_width([path, *boxes]), self.frame_y)
            slot = [PIC_LEFT + 0.2 + path.width / 2, self.frame_y, 0]
            self.play(FlashUnder(G(code.find("chg::chgs", 2)), color=YELLOW, time_width=1.5),
                      path.animate.move_to(slot),
                      *[b.animate.shift(RIGHT * dx) for b in boxes], Transform(frame, new_frame),
                      run_time=2.0)
            settle(self, self.stack, add=[path])
            self.boxes = [path, *boxes]
            c.wait_until("and returns the lot")
            self.play(FlashAround(frame, color=TEAL, time_width=1.5, buff=0.08), run_time=1.4)

            dead = solution([1, 2], color=GOLD)
            dead.move_to([PIC_LEFT + 0.2 + dead.width / 2, self.path_y, 0])
            c.wait_until("empty")
            self.play(Transform(self.box, token_box(code.line(3), code.line(3))),
                      FadeIn(dead, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("so this path has failed")
            self.play(dead[0].animate.set_stroke(RED), restyle(dead[1], op=0.4), run_time=1.0)

            c.wait_until("nothing")
            self.play(FadeOut(dead, shift=0.3 * UP),
                      FlashUnder(G(code.find("chgs", 3)), color=TEAL, time_width=1.5),
                      FlashAround(frame, color=TEAL, time_width=1.5, buff=0.08),
                      run_time=min(1.5, max(0.8, c.remaining - 0.2)))

    # ── c6.accs.3: amt < 0, the overshoot caught one call later ─────────────────────────────
    def clip3(self):
        code = self.code
        lt0 = G(self.lt0)
        line4 = code.line(4)
        ghost = Mono("amt < c", CODE_SIZE, DIM).set_opacity(0.6)
        ghost.next_to(line4, RIGHT, buff=0.7).align_to(line4, DOWN)
        was = T("last time", 28, DIM).next_to(ghost, UP, buff=0.18)
        self.ghost = VGroup(ghost, was)

        x = -4.2                      # under line 4's left end (lines 5-6 start further right)
        n1 = node("1", "[5; 2]", [x, self.cb - 0.1, 0])
        n2 = node("-4", "[5; 2]", [x, self.cb - 0.1 - 1.4, 0], color=RED)
        e = edge(n1, n2, -1)
        e_lab = edge_label(e, "use", 5, -1)
        back = Arrow(n2.get_right(), self.frame.get_left() + PIC_SHIFT * RIGHT, buff=0.15,
                     stroke_width=5, color=TEAL)
        caught = T("caught one call later", LABEL, RED).next_to(n2, DOWN, buff=0.2)

        with self.say("c6.accs.3") as c:
            self.play(Transform(self.box, token_box(line4, line4)), run_time=1.2)

            c.wait_until("It asks whether")
            self.play(*recolor(self.lt0, RED), FlashAround(lt0, color=RED, time_width=1.5),
                      run_time=1.4)
            c.wait_until("not whether")
            self.play(FadeIn(ghost, shift=0.2 * LEFT), FadeIn(was, shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("overshoot")
            self.play(FlashUnder(G(code.find("(amt - c)", 5)), color=YELLOW, time_width=1.5),
                      run_time=1.5)

            c.wait_until("late")
            self.play(FadeIn(n1, shift=0.3 * DOWN), self.stack.animate.shift(PIC_SHIFT * RIGHT), run_time=1.2)
            c.wait_until("It uses the five anyway")
            self.play(Create(e), FadeIn(e_lab, shift=0.2 * RIGHT), run_time=fit(c, "so the next call sees", 1.2))
            c.wait_until("so the next call sees")
            self.play(TransformFromCopy(n1, n2), run_time=fit(c, "and just returns", 1.5))
            c.wait_until("and just returns")
            self.play(GrowArrow(back), run_time=1.0)
            self.play(FlashAround(self.frame, color=TEAL, time_width=1.5, buff=0.08), run_time=1.3)

            c.wait_until("caught")
            self.play(FadeIn(caught, shift=0.3 * UP), FlashAround(lt0, color=RED, time_width=1.5),
                      run_time=1.3)

    # ── c6.accs.4: the two choices; skip's solutions feed the use call ──────────────────────
    def clip4(self):
        code = self.code
        y_p = self.cb - 0.6
        y_c = y_p - 1.4
        px = -1.35                    # left of centre: line 6 hangs over the right half
        par = node("amt", "c::till", [px, y_p, 0])
        uch = node("amt - c", "c::till", [px - 2.75, y_c, 0])
        sch = node("amt", "till", [px + 3.2, y_c, 0])
        u_e, s_e = edge(par, uch, -1), edge(par, sch, 1)
        u_dim, s_dim = (edge(par, uch, -1, DIM, 2.5, 0.6), edge(par, sch, 1, DIM, 2.5, 0.6))
        u_lab, s_lab = edge_label(u_e, "use", "c", -1), edge_label(s_e, "skip", "c", 1)
        u_box = uch[0].copy().set_stroke(DIM, 2.5, opacity=0.6)
        s_box = sch[0].copy().set_stroke(DIM, 2.5, opacity=0.6)
        u_rect = SurroundingRectangle(G(self.use_call), buff=0.07, corner_radius=0.06).set_stroke(YELLOW, 3)
        s_rect = SurroundingRectangle(G(self.skip_call), buff=0.07, corner_radius=0.06).set_stroke(YELLOW, 3)
        feed = Arrow(sch.get_left(), uch.get_right(), buff=0.12, stroke_width=5, color=TEAL)
        feed_lab = Mono("chgs", LABEL, TEAL).next_to(feed, DOWN, buff=0.15)
        at = Mono("@", 48, DIM).move_to([px, y_p - 0.72, 0])
        cross = Cross(at, stroke_color=RED, stroke_width=5, scale_factor=1.1)

        with self.say("c6.accs.4") as c:
            c.wait_until("it makes the same")
            sweep_clear(self, time_span(FadeIn(par, shift=0.2 * DOWN), 0.5, 1.3),
                        time_span(FadeIn(u_dim, s_dim, u_box, s_box), 0.8, 1.6),
                        keep=[code, *self.labels], run_time=1.6)

            c.wait_until("Use the coin")
            self.play(Create(u_rect), Transform(u_dim, u_e), FadeIn(u_lab, shift=0.2 * DOWN),
                      run_time=fit(c, "by taking it off", 1.3))
            c.wait_until("by taking it off")
            self.play(Transform(u_box, uch[0]), FadeIn(uch[1], shift=0.2 * DOWN),
                      FlashUnder(G(code.find("(amt - c)", 5)), color=GOLD, time_width=1.5),
                      run_time=fit(c, "consing it onto", 1.4))
            c.wait_until("consing it onto")
            self.play(FlashUnder(G(code.find("(c::chg)", 5)), color=GOLD, time_width=1.5), run_time=1.3)

            c.wait_until("skip")
            self.play(Create(s_rect), Transform(s_dim, s_e), FadeIn(s_lab, shift=0.2 * DOWN),
                      run_time=fit(c, "which is the call", 1.3))
            c.wait_until("which is the call")
            self.play(Transform(s_box, sch[0]), FadeIn(sch[1], shift=0.2 * DOWN), run_time=1.2)

            c.wait_until("feed")
            self.play(FadeIn(at, scale=0.8), run_time=1.0)
            c.wait_until("Whatever the skip call finds")
            self.play(GrowArrow(feed), run_time=fit(c, "is passed in", 1.6))
            c.wait_until("is passed in")
            self.play(FadeIn(feed_lab, shift=0.2 * UP), FlashAround(uch, color=TEAL, time_width=1.5),
                      run_time=1.4)

            c.wait_until("nojoin")
            self.play(Create(cross), FlashAround(at, color=RED, time_width=1.5),
                      run_time=min(1.2, max(0.8, c.remaining - 0.1)))

    # ── c6.accs.5: the reply's four arguments, then the first call ──────────────────────────
    def clip5(self):
        code = self.code
        reply = Code(REPLY, size=REPLY_SIZE)
        reply.move_to([0, 0, 0]).shift(UP * (REPLY_Y - G(reply.line(0)).get_center()[1]))
        rf = reply.find
        types = [rf("int list", 0, nth=0), rf("int", 0, nth=1), rf("int list", 0, nth=1),
                 rf("int list list", 0, nth=0)]
        result = rf("int list list", 1)
        names = ["till", "amt", "chg", "chgs"]
        cols = [DIM, DIM, GOLD, TEAL]
        ty = G(reply.line(0)).get_top()[1] + 0.34          # labels above the argument types
        tlabs = [Mono(n, LABEL, col).move_to([G(t).get_center()[0], ty, 0]) for n, t, col in zip(names, types, cols)]
        ul3 = underline(G(types[2]), GREEN, buff=0.08).set_stroke(width=3)
        ul4 = underline(G(types[3]), GREEN, buff=0.08).set_stroke(width=3)
        ulr = underline(G(result), GREEN, buff=0.08).set_stroke(width=3)
        res = G(result)
        arc = ArcBetweenPoints(G(types[3]).get_bottom() + 0.2 * DOWN,
                               [res.get_right()[0] - 0.35, res.get_bottom()[1] - 0.15, 0],
                               angle=-PI / 3).set_stroke(GREEN, 4)

        call = Code(CALL, size=32).move_to([0, 3.3, 0])
        for g in call.find("change"):
            g.set_color(YELLOW)
        nil1, nil2 = G(call.find("[]", nth=0)), G(call.find("[]", nth=1))
        for g in [*nil1, *nil2]:
            g.set_color(TEAL)
        self.call = call
        la = T("no coins yet", LABEL, GOLD)
        la.move_to([nil1.get_center()[0] - 0.35 - la.width / 2, call.get_bottom()[1] - 0.6, 0])
        pa = pointer([la.get_right()[0] - 0.15, la.get_top()[1] + 0.04, 0], nil1.get_bottom() + 0.07 * DOWN, GOLD)
        lb = T("no solutions yet", LABEL, TEAL)
        lb.move_to([nil2.get_center()[0] + 0.35 + lb.width / 2, call.get_bottom()[1] - 0.6, 0])
        pb = pointer([lb.get_left()[0] + 0.15, lb.get_top()[1] + 0.04, 0], nil2.get_bottom() + 0.07 * DOWN, TEAL)

        body = [g for i in range(1, 7) for g in code.line(i)]
        with self.say("c6.accs.5") as c:
            sweep_clear(self, *[g.animate.set_opacity(0) for g in body],
                        time_span(FadeIn(reply, shift=0.2 * UP), 0.6, 1.5),
                        keep=[code, *self.labels], run_time=1.5)

            c.wait_until("now lists four arguments")
            self.play(LaggedStart(*[TransformFromCopy(G(n), t) for n, t in zip(self.h_names, tlabs)],
                                  lag_ratio=0.2), run_time=fit(c, "types", 1.8, frac=0.95))

            c.wait_until("types")
            self.play(FlashAround(G(types[2]), color=GREEN, time_width=1.5), Create(ul3), run_time=1.3)
            c.wait_until("and the solutions so far are")
            self.play(FlashAround(G(types[3]), color=GREEN, time_width=1.5), Create(ul4), run_time=1.3)
            c.wait_until("the same type as the answer")
            self.play(Create(arc), Create(ulr), FlashAround(G(result), color=GREEN, time_width=1.5),
                      run_time=1.5)

            c.wait_until("call")
            self.play(*[FadeOut(m) for m in [code, *self.labels]],
                      time_span(FadeIn(call, shift=0.3 * DOWN), 0.5, 1.4), run_time=1.4)
            c.wait_until("No coins chosen yet")
            self.play(FadeIn(la, shift=0.25 * UP), GrowArrow(pa),
                      time_span(FadeIn(lb, shift=0.25 * UP), 0.7, 1.7), time_span(GrowArrow(pb), 0.7, 1.7),
                      run_time=1.7)
