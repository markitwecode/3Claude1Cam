"""Chapter 5, scene 4: Leibniz with a factor that runs out. Clips c5.leib.1 – c5.leib.4.

Plan: opens on ch5_s3's handover_shot() (def line, ladder_card(3), the hero line at 56 with its
circle / f / x / g marks, ch4's Leibniz card parked top-right). Work area = left of the ladder,
centred at xc (as ch5_s5's layout).
c1 {card} the marks go, the hero shrinks into s5's strip under the def line; the parked card flies
(down past the ladder heading, between strip and rungs) to the centre. {fg} "f = x, g = e^{-x^2}"
under it; x and e^{-x^2} fly into the card's lhs, now d^n/dx^n (x e^{-x^2}). {terms} the defs slide
to the bottom, the sum unrolls into two lines (line 1: m = 0, 1, ...; line 2: the last two terms);
flashes on g^(m) / f^(n-m); {ask} a YELLOW "?".
c2 {runs} defs -> chain x -> 1 -> 0 -> 0 -> ..., margin note f^(m) = 0, m > 1; {dead} line 1 struck
RED and dimmed, "= 0"; {two} "?" -> "two survive", flashes on f^(1), f^(0); {row} the dead line and
the chain go, the survivors rise to the centre; ch4's triangle rows 0-3 small at bottom-left, row 4
grows; all but 4 1 dim, labels.
c3 survivors resolve by edits: f^(1) -> 1, binom -> n; f^(0) -> x, binom -> 1; {typo} the notes'
inset with the lecturer's hand correction.
c4 {result} card and inset go, the survivors edit into s5's two-term line; {compare} ch4's three
survivors in a thumbnail + caption; they fade and the scene holds on s5's open_shot().
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2 = load_scene("ch5_s2_define")
S3 = load_scene("ch5_s3_peel")
S5 = load_scene("ch5_s5_assemble")
P4 = load_scene("ch4_s3_pattern")
F4 = load_scene("ch4_s4_formula")

HAND = "Bradley Hand"
X = ("x", BLUE)
EM = ("e^{-x^2}", PURPLE)
DN = r"\frac{d^n}{dx^n}"
LP, RP = r"\Big(", r"\Big)"
SZ = 44
CARD_Y = 0.45
ROW_SZ = 40
L1_Y, L2_Y, BOT_Y = -0.95, -2.05, -3.0


def M(parts, size=SZ):
    """MathTex with one part per entry; an entry is a tex string or (tex, colour)."""
    texs = [p if isinstance(p, str) else p[0] for p in parts]
    m = MathTex(*texs, font_size=size, color=FG)
    for i, p in enumerate(parts):
        if not isinstance(p, str):
            m[i].set_color(p[1])
    return m


def B(top, bot):
    return (rf"\binom{{{top}}}{{{bot}}}", YELLOW)


def F(k):
    return (f"f^{{({k})}}", BLUE)


def G(k):
    return (f"g^{{({k})}}", PURPLE)


def handover_shot():
    """The last frame: ch5_s5's open_shot() (def line, ladder, strip, two-term result)."""
    return S5.open_shot()


def path_fly(mob, pts, widths):
    """Move mob along the polyline pts (its centre), its width interpolated through widths."""
    pts = [np.array(p, dtype=float) for p in pts]
    lens = [np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])]
    total = sum(lens)

    def upd(m, a):
        d = a * total
        for i, ln in enumerate(lens):
            if d <= ln or i == len(lens) - 1:
                t = 0 if ln == 0 else min(1, d / ln)
                break
            d -= ln
        p = pts[i] + t * (pts[i + 1] - pts[i])
        w = widths[i] + t * (widths[i + 1] - widths[i])
        m.scale(w / m.width)
        m.move_to(p)

    return UpdateFromAlphaFunc(mob, upd)


class Leibniz(NarratedScene):
    def construct(self):
        shot = S3.handover_shot()
        self.dl, self.lad, self.hero, ring, fm, times, gm, self.card = shot
        self.marks = [ring, fm, times, gm]
        self.add(*shot)
        final = S5.open_shot()
        self.strip_t, self.two_t = final[2], final[3]
        xl, xr = -6.6, self.lad.get_left()[0] - 0.35
        self.xc = (xl + xr) / 2
        self.xr = xr
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)          # handover: hold on ch5_s5's open_shot()

    # ------------------------------------------------------------------ c1
    def clip1(self):
        xc = self.xc
        card = self.card
        # where the card lands: rest (= sum binom f g) placed so the card with its new lhs is centred
        tgt = F4.leibniz_card(56).scale(48 / 56)
        new_lhs = M([DN, LP, X, EM, RP], 48)
        gap = tgt.eq.get_left()[0] - tgt.lhs.get_right()[0]
        rest = VGroup(tgt.eq, tgt.sum, tgt.binom, tgt.fpart, tgt.gpart)
        total = new_lhs.width + gap + rest.width
        if total > 8.4:
            k = 8.4 / total
            tgt.scale(k)
            new_lhs.scale(k)
            gap *= k
            total = 8.4
        tgt.set_y(CARD_Y)
        tgt.shift(RIGHT * (xc - total / 2 + new_lhs.width + gap - rest.get_left()[0]))
        new_lhs.next_to(tgt.eq, LEFT, buff=gap)
        new_lhs.shift(UP * (tgt.eq.get_y() - new_lhs[2].get_y()))

        # the squeeze path: down above the ladder heading, left, down between strip and rungs, left
        h_ratio = card.height / card.width
        lb = self.strip_t.get_right()[0]
        rb = self.lad.rungs[4].label.get_left()[0]
        wsq = min(1.8, rb - lb - 0.3)
        cx = (lb + rb) / 2
        w_b = 2.6
        y_b = self.lad.heading.get_top()[1] + 0.12 + w_b * h_ratio / 2
        y_c = min(y_b, self.dl.get_bottom()[1] - 0.08 - wsq * h_ratio / 2)
        pts = [card.get_center(), [card.get_x(), y_b, 0], [cx, y_c, 0], [cx, tgt.get_y(), 0],
               tgt.get_center()]
        widths = [card.width, w_b, wsq, wsq, tgt.width]

        with self.say("c5.leib.1") as c:
            self.play(*during(disappear(*self.marks), 0, 0.3),
                      *during([ReplacementTransform(self.hero, self.strip_t)], 0.05, 0.5),
                      *during([path_fly(card, pts, widths)], 0.4, 1.0),
                      run_time=max(2.0, min(3.2, c.until("fg") - 0.2)))
            self.remove(*card.get_family())
            self.add(card)

            # {fg}: f = x, g = e^{-x^2}
            defs = M([("f", BLUE), "=", X, r",\qquad", ("g", PURPLE), "=", EM])
            defs.move_to([max(new_lhs.get_x(), -6.3 + defs.width / 2), -0.95, 0])
            c.wait_until("fg")
            self.play(*appear(VGroup(*defs[0:3])), run_time=1.0)
            c.wait_until("the Gaussian")
            self.play(*appear(VGroup(*defs[3:7])), run_time=1.0)
            settle(self, defs)
            # x and e^{-x^2} drop into the f and g slots of the lhs
            old_lhs = card.lhs
            card.remove(old_lhs)
            self.add(old_lhs)
            self.play(*during(disappear(old_lhs), 0, 0.4),
                      *during(fly(defs[2], new_lhs[2]), 0.3, 1.0),
                      *during(fly(defs[6], new_lhs[3]), 0.3, 1.0),
                      *during(appear(new_lhs[0], new_lhs[1], new_lhs[4], shift=None), 0.55, 1.0),
                      run_time=max(1.2, min(1.8, c.until("terms") - 0.1)))
            settle(self, new_lhs)
            settle(self, card, add=[new_lhs])
            card.lhs = new_lhs

            # {terms}: the sum unrolls
            l1 = M([B("n", 0), F("n"), G(0), "+", B("n", 1), F("n-1"), G(1), "+", r"\cdots", "+"], ROW_SZ)
            l2 = M([B("n", "n-1"), F(1), G("n-1"), "+", B("n", "n"), F(0), G("n")], ROW_SZ)
            zero = MathTex("=", "0", font_size=ROW_SZ, color=RED)
            k = min(1.0, 8.4 / (l1.width + 0.3 + zero.width))
            l1.scale(k)
            l2.scale(k)
            zero.scale(k)
            block_w = l1.width + 0.3 + zero.width
            left = xc - block_w / 2
            l1.move_to([left + l1.width / 2, L1_Y, 0])
            l2.move_to([left + l2.width / 2, L2_Y, 0])
            zero.next_to(l1, RIGHT, buff=0.3)
            self.l1, self.l2, self.zero, self.defs, self.k = l1, l2, zero, defs, k
            terms = [VGroup(*l1[0:3]), VGroup(*l1[3:4]), VGroup(*l1[4:7]), VGroup(*l1[7:10]),
                     VGroup(*l2[0:3]), VGroup(*l2[3:4]), VGroup(*l2[4:7])]
            c.wait_until("sum has")
            self.play(*during([defs.animate.set_y(BOT_Y)], 0, 0.35),
                      *during(appear(*terms, shift=None, lag=0.35), 0.35, 1.0),
                      run_time=max(1.5, min(3.0, c.until("The term labelled") - 0.3)))
            settle(self, l1)
            settle(self, l2)

            c.wait_until("Gaussian M times")
            self.play(FlashAround(card.gpart, time_width=1.5, color=PURPLE), run_time=1.3)
            c.wait_until("the other")
            self.play(FlashAround(card.fpart, time_width=1.5, color=BLUE), run_time=1.3)

            # {ask}
            q = MathTex("?", font_size=90, color=YELLOW)
            q.next_to(l2, RIGHT, buff=1.0)
            q.set_x(min(q.get_x(), self.xr - 0.2 - q.width / 2))
            self.q = q
            c.wait_until("ask")
            self.play(*appear(q), run_time=1.0)

    # ------------------------------------------------------------------ c2
    def clip2(self):
        xc = self.xc
        l1, l2, zero, defs = self.l1, self.l2, self.zero, self.defs
        chain = M([X, r"\to", ("1", BLUE), r"\to", ("0", BLUE), r"\to", ("0", BLUE), r"\to", r"\cdots"], 38)
        for i in (1, 3, 5, 7, 8):
            chain[i].set_color(DIM)
        note = M([(r"f^{(m)}", BLUE), r"= 0,\ \ m > 1"], 36)
        chain.next_to([l1.get_left()[0], BOT_Y, 0], RIGHT, buff=0)
        note.next_to([zero.get_right()[0], BOT_Y, 0], LEFT, buff=0)
        with self.say("c5.leib.2") as c:
            # {runs}: the defs give way to x's derivative chain
            self.play(*swap(defs, VGroup(*chain[0:3])), run_time=1.4)
            c.wait_until("every derivative")
            self.play(*appear(VGroup(*chain[3:9]), shift=None), run_time=1.2)
            settle(self, chain)
            c.wait_until("zero")
            self.play(*appear(note), run_time=1.0)

            # {dead}
            groups = [VGroup(*l1[0:3]), VGroup(*l1[4:7]), l1[8]]
            strikes = [Line(g.get_left() + LEFT * 0.08, g.get_right() + RIGHT * 0.08,
                            color=RED, stroke_width=5) for g in groups]
            c.wait_until("dead")
            self.play(restyle(l1, op=0.4),
                      LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.35),
                      run_time=1.8)
            c.wait_until("zero", nth=1)
            self.play(*appear(zero), run_time=1.0)

            # {two}
            ans = T("two\nsurvive", size=32, color=YELLOW)
            ans.next_to(l2, RIGHT, buff=0.4)
            ans.set_x(min(ans.get_x(), self.xr - 0.15 - ans.width / 2))
            c.wait_until("two")
            self.play(*swap(self.q, ans), FlashAround(l2, time_width=1.5, buff=0.15), run_time=1.3)
            c.wait_until("differentiated once")
            self.play(FlashAround(l2[1], time_width=1.5), run_time=0.9)
            c.wait_until("left alone")
            self.play(FlashAround(l2[5], time_width=1.5), run_time=0.9)

            # {row}: the dead line goes, the survivors rise; ch4's triangle at bottom-left
            # the card shrinks toward its top so the survivors and the triangle get room
            card_t = self.card.copy().scale(0.82, about_point=self.card.get_top())
            surv_y = card_t.get_bottom()[1] - 0.3 - l2.height / 2
            self.surv_y = surv_y
            tri = P4.pascal_triangle(n_max=3, start=0, size=64)   # big digits, rows still at PASCAL_DY
            r4 = P4.pascal_row(4, like=tri)
            whole = VGroup(tri, r4)
            top = surv_y - l2.height / 2 - 0.3
            whole.scale((top + 3.4) / whole.height)
            whole.move_to([-6.5 + whole.width / 2, top - whole.height / 2, 0])
            labs = VGroup(MathTex(r"\text{row } n = 4", font_size=36, color=DIM),
                          MathTex(r"\binom{4}{3} = 4", font_size=40, color=YELLOW),
                          MathTex(r"\binom{4}{4} = 1", font_size=40, color=YELLOW))
            labs[2].next_to(labs[1], RIGHT, buff=0.5)
            labs[0].next_to(VGroup(labs[1], labs[2]), UP, buff=0.3, aligned_edge=LEFT)
            labs.next_to(whole, RIGHT, buff=0.8)
            labs.align_to(r4, DOWN)
            self.tri, self.r4, self.labs = tri, r4, labs
            c.wait_until("row")
            self.play(*during(disappear(l1, zero, *strikes, chain, note, ans), 0, 0.4),
                      *during([Transform(self.card, card_t), l2.animate.move_to([xc, surv_y, 0])], 0.4, 0.8),
                      *during(appear(tri), 0.6, 1.0),  # early: the triangle as in part four
                      run_time=1.5)
            c.wait_until("only the last two")
            self.play(*appear(r4, shift=0.15 * DOWN), run_time=0.8)
            c.wait_until("are used")
            self.play(restyle(tri, op=0.3), *set_alpha([r4[0], r4[1], r4[2]], 0.3),
                      *during(appear(*labs, lag=0.3), 0.3, 1.0),  # early: the n = 4 labels name "N and one"
                      run_time=min(1.4, c.until(floor=0.8)))

    # ------------------------------------------------------------------ c3
    def clip3(self):
        xc = self.xc
        l2 = self.l2

        def at(m):
            return m.scale(self.k).move_to([xc, self.surv_y, 0])

        v1 = at(M([B("n", "n-1"), r"\cdot", ("1", BLUE), r"\cdot", G("n-1"), "+", B("n", "n"), F(0), G("n")]))
        v2 = at(M([("n", YELLOW), G("n-1"), "+", B("n", "n"), F(0), G("n")]))
        v3 = at(M([("n", YELLOW), G("n-1"), "+", B("n", "n"), X, G("n")]))
        v4 = at(M([("n", YELLOW), G("n-1"), "+", X, G("n")]))
        with self.say("c5.leib.3") as c:
            # {coef}: the first survivor
            self.play(FlashAround(VGroup(*l2[0:3]), time_width=1.5, buff=0.15), run_time=1.4)
            c.wait_until("to give one")
            self.play(*edit(l2, v1), run_time=1.5)
            c.wait_until("Its coefficient is")
            self.play(FlashAround(v1[0], time_width=1.5), FlashAround(self.labs[1], time_width=1.5),
                      run_time=min(1.4, c.until(floor=0.8)))
            c.wait_until("which is N")
            self.play(*edit(v1, v2), run_time=1.5)

            # {second}
            c.wait_until("second")
            self.play(FlashAround(VGroup(*v2[3:6]), time_width=1.5, buff=0.15), run_time=1.4)
            c.wait_until("as it is")
            self.play(*edit(v2, v3), run_time=1.5)
            c.wait_until("which is one")
            self.play(*edit(v3, v4), FlashAround(self.labs[2], time_width=1.5), run_time=1.5)
            self.surv = v4

            # {typo}: the notes' printed n choose 0, the lecturer's correction
            printed = MathTex(r"\binom{n}{0}", r"f^{(0)}", r"g^{(n)}", font_size=48, color=FG)
            box = RoundedRectangle(corner_radius=0.15, width=printed.width + 1.6, height=printed.height + 1.3)
            box.set_stroke(DIM, 2)
            box.move_to([xc + 0.6, -2.6, 0])
            printed.move_to(box.get_center() + DOWN * 0.25)
            tag = T("the notes", size=30, color=DIM).next_to(box, LEFT, buff=0.3)
            bparts = printed[0]
            small = [g for g in bparts if g.height < 0.6 * bparts.height]
            zero_g = min(small, key=lambda g: g.get_y())
            hand_n = Text("n", font=HAND, font_size=32, color=RED).move_to(zero_g).shift(RIGHT * 0.03 + DOWN * 0.04)
            hand_eq = Text("= 1", font=HAND, font_size=40, color=RED)
            hand_eq.next_to(bparts, UP, buff=0.12).shift(RIGHT * 0.25)
            self.inset = [box, printed, tag, hand_n, hand_eq]
            c.wait_until("typo")
            self.play(*during(disappear(self.tri, self.r4, self.labs), 0, 0.45),
                      *during([FadeIn(box)] + appear(printed, tag, shift=None, lag=0.3), 0.5, 1.0),
                      run_time=1.6)
            c.wait_until("corrected")
            self.play(*during([FadeOut(zero_g)], 0, 0.45), *during(appear(hand_n, shift=None), 0.4, 1.0),
                      run_time=1.2)
            c.wait_until("both equal one")
            self.play(*appear(hand_eq, shift=None), run_time=1.0)

    # ------------------------------------------------------------------ c4
    def clip4(self):
        xc = self.xc
        two = self.two_t
        with self.say("c5.leib.4") as c:
            # {result}
            self.play(*disappear(self.card), run_time=0.9)
            self.play(*edit(self.surv, two), run_time=1.8)
            c.wait_until("N times the Gaussian")
            self.play(FlashAround(VGroup(*two[1:4]), time_width=1.5, buff=0.15), run_time=1.4)
            c.wait_until("plus ex")
            self.play(FlashAround(VGroup(*two[5:8]), time_width=1.5, buff=0.15), run_time=1.4)

            # {compare}: part four's three survivors
            head = VGroup(T("Part 4:", size=30, color=DIM),
                          M([r"\big(", ("x^2", BLUE), ("e^{-x}", PURPLE), r"\big)^{(n)}"], 36))
            head.arrange(RIGHT, buff=0.2)
            row3 = M([B("n", "n-2"), ("f''", BLUE), G("n-2"), "+", B("n", "n-1"), ("f'", BLUE), G("n-1"),
                      "+", B("n", "n"), ("f", BLUE), G("n")], 36)
            body = VGroup(head, row3).arrange(DOWN, buff=0.3)
            frame = RoundedRectangle(corner_radius=0.15, width=body.width + 0.6, height=body.height + 0.5)
            frame.set_stroke(DIM, 2)
            thumb = VGroup(frame, body)
            thumb.move_to([xc, -1.65, 0])
            cap = M([("x^2", BLUE), r"\text{: three terms}", r"\quad\cdot\quad", X, r"\text{: two terms}"], 38)
            cap.move_to([xc, -3.1, 0])
            c.wait_until("compare")
            box, printed, tag, hand_n, hand_eq = self.inset
            self.play(*during([FadeOut(hand_n), FadeOut(hand_eq)], 0, 0.2),
                      *during([FadeOut(m) for m in (box, printed, tag)], 0.2, 0.4),
                      *during(appear(thumb, cap, lag=0.5), 0.4, 1.0), run_time=2.0)
            c.wait_until("three terms were left")
            self.play(*flash([VGroup(*row3[0:3]), VGroup(*row3[4:7]), VGroup(*row3[8:11])]), run_time=1.4)
            c.wait_until("Ex survives one")
            self.play(*flash([VGroup(*two[1:4]), VGroup(*two[5:8])]), run_time=1.4)
        self.wait(2.5)
        self.play(*disappear(thumb, cap), run_time=1.0)
