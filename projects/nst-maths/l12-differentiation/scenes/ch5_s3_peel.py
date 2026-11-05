"""Chapter 5, scene 3: peel off one derivative. Clips c5.peel.1 – c5.peel.3.

Plan: opens on ch5_s2's handover_shot() (def line at the top, ladder_card(3) at the right).
The notes' chain (p62) is built in the work area left of the ladder, one line per beat, "=" aligned:
row A  H_{n+1} = (-1)^{n+1} e^{x^2} d^{n+1}/dx^{n+1} (e^{-x^2})      (copied out of the def line)
row B  = (-1)^{n+1} e^{x^2} d^n/dx^n (d/dx e^{-x^2})                 tag "(112), part 4"
row C  = (-1)^{n+1} e^{x^2} d^n/dx^n (-2x e^{-x^2}); the -2 then lifts out in place, under the line:
       = (-1)^{n+1} (-2) e^{x^2} d^n/dx^n (x e^{-x^2})                tag "constants come out: part 1"
sign row  (-1)^{n+1}.(-2) -> 2.(-1).(-1)^{n+1} -> 2(-1)^{n+2} -> 2(-1)^n
row D  = 2(-1)^n e^{x^2} d^n/dx^n (x e^{-x^2})
{board}: the board is cleared, row D rises to row A; the lecturer's board line (45:01) in an inset,
its leading minus struck RED; an arrow to the notes' p63 line H_{n+1} = 2(-1)^n e^{x^2}( ... ).
{left}: the line becomes the hero at the centre; x e^{-x^2} circled, "f" and "g" above, a small
times sign between them flashes on {product}; on {leibniz} ch4's sum card parks top-right and pulses.

Exports: handover_shot() = VGroup(def_line, ladder_card(3), hero, circle, f, times, g, card);
hero_line() (the last line, MathTex 56; parts 0 = | 1 2 | 2 (-1)^n | 3 e^{x^2} | 4 d^n/dx^n | 5 ( |
6 x | 7 e^{-x^2} | 8 )), parked_card() (ch4's leibniz_card, small, top-right corner).
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
HAND = "Bradley Hand"           # the lecturer's handwriting (as in ch1)

X_EQ = -4.3                     # x of every line's "=" (left edge)
ROW_A, ROW_B, ROW_C, ROW_D = 1.62, 0.42, -0.78, -1.98
SIGN_Y = -3.05                  # where the sign row parks once row D arrives
SIGN_C = np.array([-2.1, -2.35, 0])   # the sign row at hero size, below the dimmed lines
SIZE = 44
HERO_SIZE = 56
HERO_C = np.array([-2.1, -0.55, 0])

X = ("x", BLUE)
EP = ("e^{x^2}", GOLD)
EM = ("e^{-x^2}", PURPLE)
DN = r"\frac{d^n}{dx^n}"
DN1 = r"\frac{d^{n+1}}{dx^{n+1}}"
LP, RP = r"\Big(", r"\Big)"


def M(parts, size=SIZE):
    """MathTex with one part per entry; an entry is a tex string or (tex, colour)."""
    texs = [p if isinstance(p, str) else p[0] for p in parts]
    m = MathTex(*texs, font_size=size, color=FG)
    for i, p in enumerate(parts):
        if not isinstance(p, str):
            m[i].set_color(p[1])
    return m


def place(m, y, eq_idx=0):
    """Put line m on row y with its "=" (part eq_idx) at X_EQ."""
    m.set_y(y)
    m.shift(RIGHT * (X_EQ - m[eq_idx].get_left()[0]))
    return m


def hero_line():
    """= 2(-1)^n e^{x^2} d^n/dx^n (x e^{-x^2}), MathTex 56 at the work-area centre, x BLUE."""
    m = M(["=", "2", "(-1)^n", EP, DN, LP, X, EM, RP], HERO_SIZE)
    return m.move_to(HERO_C)


def hero_marks(hero):
    """The lecturer's circle round x e^{-x^2}, her "f" and "g" above, a small times sign between."""
    inner = VGroup(hero[6], hero[7])
    ring = Ellipse(width=inner.width + 0.4, height=inner.height + 0.4, color=YELLOW, stroke_width=4)
    ring.move_to(inner)
    f = Text("f", font=HAND, font_size=44, color=BLUE)
    g = Text("g", font=HAND, font_size=44, color=PURPLE)
    f.next_to(ring, UP, buff=0.12).set_x(hero[6].get_x())
    g.next_to(ring, UP, buff=0.12).set_x(hero[7].get_x())
    g.align_to(f, DOWN)
    times = MathTex(r"\times", font_size=34, color=YELLOW)
    times.move_to([(f.get_right()[0] + g.get_left()[0]) / 2, f.get_center()[1], 0])
    return ring, f, times, g


def parked_card():
    card = load_scene("ch4_s4_formula").leibniz_card()
    card.scale_to_fit_width(3.4)
    card.move_to([4.85, 2.7, 0])
    return card


def handover_shot():
    hero = hero_line()
    return VGroup(S2.def_line(), S2.ladder_card(3), hero, *hero_marks(hero), parked_card())


class Peel(NarratedScene):
    def construct(self):
        self.dl = S2.def_line()
        self.lad = S2.ladder_card(3)
        self.add(self.dl, self.lad)
        self.goal_and_write()
        self.chain_and_out()
        self.merge_and_board()
        self.wait(1.0)          # handover: hold on handover_shot(); ch5_s4 opens on it

    # ------------------------------------------------------------ c5.peel.1
    def goal_and_write(self):
        dl, lad = self.dl, self.lad
        r3 = lad.rungs[3]
        with self.say("c5.peel.1") as c:
            # {goal}: the target, and the empty rung above H_2 lights faintly
            goal = MathTex("H_{n+1}", font_size=64, color=YELLOW).move_to(HERO_C)
            c.wait_until("We want")
            self.play(*appear(goal, shift=None), r3.label.animate.set_opacity(0.8),
                      r3.slot.animate.set_color(YELLOW), run_time=1.2)
            c.wait_until("in place of")
            self.play(*flash([dl.sign, dl.dn]), run_time=1.5)

            # {write}: the definition with n+1 in place of n
            L1 = place(M([("H_{n+1}", YELLOW), "=", "(-1)^{n+1}", EP, DN1, LP, EM, RP]), ROW_A, eq_idx=1)
            self.L1, self.goal = L1, VGroup()
            c.wait_until("write")
            derive(self, dl, L1, *during(FadeOut(goal), 0, 0.6), run_time=min(2.4, c.until("differentiated")))
            c.wait_until("differentiated")
            self.play(*flash([L1[2], L1[4]]), *recolor([L1[2], L1[4]], YELLOW), run_time=1.5)

            # {split}: d^{n+1} = d^n of d/dx
            L2 = place(M(["=", "(-1)^{n+1}", EP, DN, LP, r"\frac{d}{dx}", EM, RP]), ROW_B)
            self.L2 = L2
            c.wait_until("split")
            self.play(*recolor([L1[2], L1[4]], FG), run_time=0.6)
            derive(self, L1, L2, run_time=min(2.0, c.until("That changes")))
            self.play(*flash([L2[3], L2[5]]), run_time=1.2)
            self.tag1 = T("(112),\npart 4", size=28, color=DIM).next_to(L2, LEFT, buff=0.3)
            c.wait_until("That changes")
            self.play(*appear(self.tag1), run_time=1.0)  # early: names the rule behind the split

    # ------------------------------------------------------------ c5.peel.2
    def chain_and_out(self):
        L2, lad = self.L2, self.lad
        with self.say("c5.peel.2") as c:
            # {chain}: the first derivative is already known (ladder row n = 1)
            inner = VGroup(L2[5], L2[6])
            box = token_box(inner, L2, height=L2.height + 0.15)
            self.play(FadeIn(box), FlashAround(lad.rungs[1], run_time=1.5, time_width=1.5),
                      run_time=1.5)
            L3 = place(M(["=", "(-1)^{n+1}", EP, DN, LP, "-2", "x", EM, RP]), ROW_C)
            c.wait_until("minus two ex")
            derive(self, L2, L3, FadeOut(box), run_time=min(2.0, c.until("inside")))

            # {inside}: the bracket outlined
            c.wait_until("inside")
            brk = VGroup(*L3[4:9])
            outline = SurroundingRectangle(brk, color=YELLOW, buff=0.08, corner_radius=0.1)
            self.play(GrowFromCenter(outline), run_time=1.0)

            # {out}: the -2 lifts out of the bracket to the front, passing under the line
            L4 = place(M(["=", "(-1)^{n+1}", "(", "-2", ")", EP, DN, LP, "x", EM, RP]), ROW_C)
            c.wait_until("out")
            mapping = {0: 0, 1: 1, 2: 5, 3: 6, 4: 7, 6: 8, 7: 9, 8: 10}
            moves = [L3[i].animate.move_to(L4[j]) for i, j in mapping.items()]
            lift = L3[5].animate(path_arc=-0.95 * PI).move_to(L4[3])
            self.play(*during(FadeOut(outline), 0, 0.3), *during(moves, 0.2, 0.8),
                      *during(lift, 0.1, 0.85), run_time=min(1.8, c.until("signs")))
            self.remove(*L3.get_family())
            self.add(*[L4[j] for j in mapping.values()], L4[3])
            self.play(FadeIn(L4[2]), FadeIn(L4[4]), run_time=0.5)
            settle(self, L4)
            self.L4 = L4
            tag2 = T("constants\ncome out:\npart 1", size=28, color=DIM)
            tag2.next_to(L4, LEFT, buff=0.3)
            self.tag2 = tag2
            self.play(*appear(tag2), run_time=0.8)  # early: names the rule behind the lift

            # {signs}: the two sign factors on their own
            c.wait_until("signs")
            S1 = M([("(-1)^{n+1}", YELLOW), ("(", YELLOW), ("-2", YELLOW), (")", YELLOW)], HERO_SIZE)
            S1.move_to(SIGN_C)
            rest = [self.L1, L2, self.tag1, tag2, *[L4[i] for i in (0, 5, 6, 7, 8, 9, 10)]]
            self.play(*set_alpha(rest, DIMMED), *fly(VGroup(*L4[1:5]), S1),
                      run_time=min(1.6, c.until()))
            self.S1, self.rest = S1, rest

    # ------------------------------------------------------------ c5.peel.3
    def merge_and_board(self):
        dl, lad, L4, S1 = self.dl, self.lad, self.L4, self.S1
        with self.say("c5.peel.3") as c:
            # {merge}: -2 = 2 . (-1), the minus ones combine
            S2_ = M(["2", r"\cdot", ("(-1)", YELLOW), r"\cdot", ("(-1)^{n+1}", YELLOW)], HERO_SIZE)
            S2_.move_to(S1)
            self.play(*swap(S1, S2_), run_time=1.3)
            S3 = M(["2", ("(-1)^{n+2}", YELLOW)], HERO_SIZE).move_to(S1)
            c.wait_until("The minus ones")
            self.play(*swap(S2_, S3), run_time=1.3)
            S4 = M(["2", ("(-1)^{n+2}", YELLOW), "=", "2", ("(-1)^n", YELLOW)], HERO_SIZE).move_to(S1)
            S3.generate_target().move_to(VGroup(*S4[0:2]))
            c.wait_until("which is")
            self.play(MoveToTarget(S3), *during(appear(*S4[2:5], shift=None), 0.4, 1.0), run_time=1.5)
            self.remove(*S3.get_family())
            settle(self, S4)

            # {front}: the new line
            L5 = place(M(["=", "2", "(-1)^n", EP, DN, LP, "x", EM, RP]), ROW_D)
            c.wait_until("front")
            self.play(*set_alpha([self.L1, self.L2, self.tag1, self.tag2], 0.45),
                      *set_alpha([L4[i] for i in (0, 5, 6, 7, 8, 9, 10)], 1),
                      S4.animate.scale(SIZE / HERO_SIZE).move_to([S4.get_x(), SIGN_Y, 0]), run_time=1.2)
            derive(self, L4, L5, run_time=min(2.0, c.until("board")))
            self.play(*flash([VGroup(*L5[1:3]), VGroup(*S4[3:5])]), run_time=1.5)

            # {board}: the lecturer's slip, struck through; the printed p63 line has +2
            c.wait_until("board")
            r3 = lad.rungs[3]
            sweep_clear(self, L5.animate.set_y(ROW_A),
                        r3.label.animate.set_opacity(0.4), r3.slot.animate.set_color(DIM),
                        keep=[dl, lad, L5], run_time=1.6)
            bl = M(["=", "-", "2", "(-1)^n", EP, DN, LP, "x", EM, RP])
            head = Text("board, 45:01", font=HAND, font_size=32, color=DIM)
            body = VGroup(head, bl).arrange(DOWN, buff=0.25)
            frame = RoundedRectangle(corner_radius=0.15, width=body.width + 0.7, height=body.height + 0.5)
            frame.set_stroke(DIM, 2).move_to(body)
            inset = VGroup(frame, head, bl).move_to([-2.1, -0.15, 0])
            self.play(*appear(inset, shift=None), run_time=1.0)
            strike = Line(bl[1].get_corner(DL) + 0.12 * (DL), bl[1].get_corner(UR) + 0.12 * UR,
                          color=RED, stroke_width=6)
            c.wait_until("slip")
            self.play(Create(strike), run_time=0.8)
            p63 = M(["H_{n+1}", "=", ("2", GREEN), "(-1)^n", EP, LP, r"\;\dots\;", RP])
            p63.move_to([-2.6, -2.75, 0])
            ptag = T("notes, p63", size=28, color=DIM).next_to(p63, RIGHT, buff=0.45)
            arrow = Arrow(frame.get_bottom() + 0.05 * DOWN, p63.get_top() + 0.05 * UP, buff=0.08,
                          color=GREEN, stroke_width=4)
            c.wait_until("printed line")
            self.play(GrowArrow(arrow), *during(appear(p63, ptag, shift=None), 0.3, 1.0), run_time=1.4)
            c.wait_until("plus two")
            self.play(FlashAround(p63[2], color=GREEN, run_time=1.5, time_width=1.5))

            # {left}: x e^{-x^2}, the product left to differentiate
            hero = hero_line()
            ring, f, times, g = hero_marks(hero)
            c.wait_until("left")
            self.play(*during(disappear(inset, strike, arrow), 0, 0.45),
                      *during(Transform(L5, hero), 0.3, 1.0), run_time=1.8)
            self.remove(*L5.get_family())
            self.add(hero)
            self.play(Create(ring), *recolor([hero[6]], BLUE), run_time=1.2)
            c.wait_until("ex")
            self.play(*appear(f), run_time=0.8)
            c.wait_until("Gaussian")
            self.play(*appear(g), run_time=0.8)

            # {product}
            c.wait_until("product")
            self.play(*appear(times, shift=None), run_time=0.6)
            self.play(FlashAround(times, run_time=1.2, time_width=1.5))

            # {leibniz}: ch4's sum card parks in the corner and pulses
            card = parked_card()
            c.wait_until("leibniz")
            self.play(*during(disappear(p63, ptag), 0, 0.45), *during(appear(card, shift=None), 0.4, 1.0),
                      run_time=1.2)  # early: ch4's card, named by "Leibniz's formula"
            self.play(FlashAround(card, run_time=2, time_width=1.5),
                      card.animate(rate_func=there_and_back).scale(1.08), run_time=2)
