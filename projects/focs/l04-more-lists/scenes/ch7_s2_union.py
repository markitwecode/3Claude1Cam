"""Chapter 7, scene 2: Exercise 4.1, set union, solved. Clips c7.union.1 - c7.union.6.

Opening (shared by ch7 s2-s7): ch6's pill strip fades in (4.1 CURRENT, the rest TODO), card 4.1
grows out of its pill (ch6's card: task rows, the GOLD "?" slot, the example, "any order"),
pause tag top right, held through the pause; then the card shrinks back into its pill (which
stays CURRENT) and the strip is the scene's header (y 3.2, x -6.5..0.3) until the final fade.

Layout after the card: ch2's member (In [63], Code 26, opacity 0.6) top right (UR at 6.6, 3.5).
  union.2  the card's example call drops out of the card to the centre and becomes
           `[4; 7; 1] @ [6; 4; 7]` (Code 48, y -0.2); its reply (Code 40) is born from it;
           the second 4 and 7 RED + RED cross.
  union.3  union's code (Code 32) + its type (30), centred; built clause by clause under a
           sliding YELLOW box.
  union.4  code + type shrink by 7/8 to the top left (line 3 at y 0.85, under member); the trace:
           xs = 4 -> 7 -> 1 -> [] (y -1.45) over ys = 6 -> 4 -> 7 -> [] (y -2.7, one slot right),
           ConsChain scale 0.8. YELLOW marker on xs, GOLD member scan on ys (GREEN + tick on a
           match), skipped cells DIM + "skip"; 1 drops to the free lower slot, its YELLOW arrow
           into ys; {result}: the call + reply replace the type line (read off the result row);
           TEAL "shared" over ys.
  union.5  GOLD box on `member x ys`; {mn}: the trace clears; GOLD 3x3 grid (rows 4 7 1 = m,
           columns 6 4 7 = n), 8 squares filled (2, 3, 3); "<= m n comparisons", "time O(m n)".
  union.6  union's `x ::` GOLD (the cost board stays); union morphs into addunion in place
           (changed parts YELLOW, the GOLD `x ::` lands in `(x::ys)`); {same}: the board gives
           way to addunion's example (left, y -0.6); union/addunion [1; 2] [3] on the right; their
           ys grows under them (scale 0.7); `union [1] [2; 2]` bottom left, the repeated 2 RED.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch2_s4_member import SRC as MEMBER_SRC  # noqa: E402   (In [63], verbatim)
from scenes.ch6_s5_hints1 import (  # noqa: E402
    CODE_DIM, CONTENT_R, CURRENT, EX41_CALL, EX41_RESULT, EX41_TAG, EX_TASKS, ROW_STEP, TODO,
    HeroCard, Slot, enter_card, finish, fit, hold_for, make_strip, pause_tag, split_line,
)

UNION_SRC = """let rec union xs ys =
  match xs with
  | [] -> ys
  | x::xs -> if member x ys then union xs ys
             else x :: union xs ys"""
UNION_REPLY = "val union : 'a list -> 'a list -> 'a list = <fun>"
ADD_SRC = """let rec addunion xs ys =
  match xs with
  | [] -> ys
  | x::xs -> if member x ys then addunion xs ys
             else addunion xs (x::ys)"""
APPEND_SRC = "[4; 7; 1] @ [6; 4; 7]"
APPEND_REPLY = "- : int list = [4; 7; 1; 6; 4; 7]"
RESULT = "union [4; 7; 1] [6; 4; 7]\n- : int list = [1; 6; 4; 7]"
ADD_RESULT = "addunion [4; 7; 1] [6; 4; 7]\n- : int list = [1; 6; 4; 7]"
SMALL_U = "union [1; 2] [3]\n- : int list = [1; 2; 3]"
SMALL_A = "addunion [1; 2] [3]\n- : int list = [2; 1; 3]"
SETS = "union [1] [2; 2]\n- : int list = [1; 2; 2]"

H41 = 0.46 + 3 * ROW_STEP + 0.46   # ch6's card 4.1
HERO_Y = -0.2                      # union.2: the append and its reply
BIG, SM = 32, 28                   # union's code: centred (union.3), then top left
REPLY_BIG = 30
CODE3_Y = -0.75                    # centre of code + reply in union.3
CODE_L = -6.6                      # left edge of the code from union.4 on
LINE3_Y = 0.85                     # code line 3 (the long one) clears member's bottom
TB_HB, TB_H = 0.57, 0.5            # clause-box heights (big / small code)

S = 0.8                            # trace chains
P = 2.3 * S                        # slot pitch
X0 = -3.1                          # slot 0 box centre (xs label .. ys's [] centred)
XS_Y, YS_Y = -1.45, -2.7

SQ = 0.75                          # cost grid
GX, GY = -2.2, -1.85
TX = 2.7

ROW1, ROW2 = -0.6, -1.85           # union.6: calls (line 0 y), left column at CODE_L ...
RCOL = 0.4                         # ... right column's left edge
D_Y = -3.1                         # the growing ys, under addunion [1; 2] [3]


def slot(k, y):
    return np.array([X0 + k * P, y, 0])


def place(code, left, y0):
    """Left edge at `left`, line 0 centred at y0."""
    code.shift([left - code.get_left()[0], y0 - VGroup(*code.line(0)).get_y(), 0])
    return code


def reveal(glyphs):
    return [FadeIn(g, shift=0.15 * DOWN) for g in glyphs]


def dim_cell(cell):
    return [cell.box.animate.set_stroke(DIM), cell.ptr.animate.set_stroke(DIM),
            cell.label.animate.set_color(DIM)]


def scan_box(m, color=GOLD):
    return SurroundingRectangle(m, color=color, buff=0.07, stroke_width=4)


class UnionSolution(NarratedScene):
    def construct(self):
        self.strip = make_strip([CURRENT] + [TODO] * 5)
        self.member = Code(MEMBER_SRC, size=26).set_opacity(CODE_DIM)
        self.member.move_to([6.6, 3.5, 0], aligned_edge=UR)
        self.clip1_card()
        self.clip2_wrong()
        self.clip3_code()
        self.clip4_trace()
        self.clip5_cost()
        self.clip6_addunion()
        hold_for(self, self.sets_born, len(SETS))
        finish(self)

    # ── glyph-level rewrites (one animation per glyph: no wrappers, no ghosts) ──────
    def retype(self, jobs, run_time, extra=()):
        """Rewrite on-screen Codes into new ones: matched glyphs move, the rest fade."""
        anims, done = [], []
        for old, new, pairs in jobs:
            used_o, used_n = set(), set()
            for og, ng in pairs:
                og, ng = list(og), list(ng)
                assert len(og) == len(ng), (old.src, new.src, len(og), len(ng))
                for a, b in zip(og, ng):
                    anims.append(Transform(a, b.copy()))
                    used_o.add(id(a))
                    used_n.add(id(b))
            anims += [g.animate.set_opacity(0) for g in old.text if id(g) not in used_o]
            fresh = [g for g in new.text if id(g) not in used_n]
            anims += [FadeIn(g, shift=0.15 * DOWN) for g in fresh]
            done.append((old, new, fresh))
        self.play(*anims, *extra, run_time=run_time)
        for old, new, fresh in done:
            self.remove(old, *fresh)
            self.add(new)

    def derive(self, pairs, new, run_time, extra=()):
        """A new Code born from copies of on-screen glyphs; its other glyphs fade in."""
        anims, used = [], set()
        for sg, ng in pairs:
            sg, ng = list(sg), list(ng)
            assert len(sg) == len(ng), (new.src, len(sg), len(ng))
            for a, b in zip(sg, ng):
                anims.append(ReplacementTransform(a.copy(), b))
                used.add(id(b))
        anims += [FadeIn(g, shift=0.15 * DOWN) for g in new.text if id(g) not in used]
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*new.text.submobjects)
        self.add(new)

    # ── union.1: the card, out of its pill; pause ───────────────────────────────────
    def clip1_card(self):
        strip = self.strip
        card = HeroCard(0, height=H41)
        t1, t2 = EX_TASKS[0].split(". ", 1)
        r1 = card.at_row(T(t1 + ".", size=34), 1)
        r2 = card.at_row(T(t2, size=34, t2c={"member": YELLOW}), 2)
        slot_ = Slot(width=3.6, height=1.25)
        slot_.move_to([CONTENT_R - slot_.width / 2, (card.row_y(1) + card.row_y(2)) / 2, 0])
        ex_in, ex_out = split_line(f"{EX41_CALL}  ⇒  {EX41_RESULT}",
                                   [EX41_CALL, f"⇒  {EX41_RESULT}"], size=34, y=card.row_y(3))
        tag = card.tag(EX41_TAG)
        card.lower(r1, r2, slot_, ex_in, ex_out)
        ptag = pause_tag()

        with self.say("c7.union.1") as c:
            # "Exercise four point one."  The strip, then the card grows out of its pill.
            self.play(FadeIn(strip, shift=0.2 * DOWN), run_time=0.9)
            self.play(*enter_card(strip, card, light=False), run_time=1.0)
            # "Store a set as a list with no repeats."
            c.wait_until("store a set")
            self.play(FadeIn(r1, shift=0.25 * DOWN), run_time=1.0)
            # "Using member, code set union."
            c.wait_until("using member")
            self.play(FadeIn(r2, shift=0.25 * DOWN), FadeIn(slot_.box), FadeIn(slot_.q, scale=0.7),
                      run_time=1.1)
            # "The union of four, seven, one, and six, four, seven should be one, six, four, seven,"
            c.wait_until("example")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("should be")
            self.play(FadeIn(ex_out, shift=0.25 * LEFT), run_time=0.9)
            # "in any order."
            c.wait_until("any order")
            self.play(FadeIn(tag, shift=0.2 * DOWN), run_time=0.8)
            # "Pause here, and try it."
            c.wait_until("stop")
            self.play(FadeIn(ptag, shift=0.2 * LEFT), run_time=0.6)
            born = self.time
        hold_for(self, born, len("pause and try it"))
        self.card, self.ex_in, self.ptag = card, ex_in, ptag
        self.card_items = [card.header, r1, r2, slot_.box, slot_.q, ex_out, tag]

    # ── union.2: the tempting shortcut, append; it repeats 4 and 7 ───────────────────
    def clip2_wrong(self):
        card, ex_in = self.card, self.ex_in
        app = Code(APPEND_SRC, size=48).move_to([0, HERO_Y, 0])
        wrong = Code(APPEND_REPLY, size=40).move_to([0, HERO_Y - 1.3, 0])
        ex_in.generate_target()
        ex_in.target.scale(48 / 34).move_to([0, HERO_Y, 0])

        with self.say("c7.union.2") as c:
            # "First, a shortcut that looks tempting."  The card goes home; its example stays.
            self.play(*[FadeOut(m) for m in self.card_items], FadeOut(self.ptag),
                      Transform(card.frame, self.strip[0].frame.copy()), MoveToTarget(ex_in),
                      run_time=1.2)
            self.remove(card.frame)
            self.play(FadeIn(self.member, shift=0.2 * DOWN), run_time=1.0)
            # "Just append the two lists."
            c.wait_until("just append")
            self.retype([(ex_in, app, [(ex_in.find("[4; 7; 1]"), app.find("[4; 7; 1]")),
                                       (ex_in.find("[6; 4; 7]"), app.find("[6; 4; 7]"))])],
                        run_time=1.5)
            # "That gives four, seven, one, six, four, seven,"
            c.wait_until("repeats")
            self.derive([(app.find("[4; 7; 1"), wrong.find("[4; 7; 1")),
                         (app.find("6; 4; 7]"), wrong.find("6; 4; 7]"))], wrong, run_time=1.5)
            # "with four and seven twice."
            c.wait_until("with four and seven")
            reds = [wrong.find("4", nth=1)[0], wrong.find("7", nth=1)[0]]
            cross = cross_mark(RED, r=0.22).next_to(wrong, RIGHT, buff=0.4)
            self.play(*recolor(reds, RED), *flash(reds, RED, buff=0.1, time_width=1.5),
                      FadeIn(cross, scale=0.6), run_time=1.2)
            # "A union must never introduce repetitions."  (still)

    # ── union.3: the code, clause by clause; its type ────────────────────────────────
    def clip3_code(self):
        code = Code(UNION_SRC, size=BIG)
        reply = Code(UNION_REPLY, size=REPLY_BIG)
        for g in reply.find("union"):
            g.set_color(YELLOW)
        reply.next_to(code, DOWN, buff=0.45, aligned_edge=LEFT)
        VGroup(code, reply).move_to([0, CODE3_Y, 0])     # layout only
        lines = [code.line(i) for i in range(5)]

        def box(sub, i):
            return token_box(code.find(sub, line=i), VGroup(*code.line(i)), height=TB_HB, pad=0.3)

        with self.say("c7.union.3") as c:
            # "Instead, walk down the first list."
            sweep_clear(self, *[time_span(a, 0.5, 1.3) for a in reveal([*lines[0], *lines[1]])],
                        keep=[self.strip, self.member], run_time=1.3)
            tb = box("match xs with", 1)
            self.play(FadeIn(tb), run_time=0.6)
            # "The union of nil with whys is just whys."
            c.wait_until("the union of nil")
            self.play(*reveal(lines[2]), Transform(tb, box("| [] -> ys", 2)), run_time=1.0)
            # "For a head, ex, if ex is already a member of whys, skip it."
            c.wait_until("skip")
            self.play(*reveal(lines[3]),
                      Transform(tb, box("| x::xs -> if member x ys then union xs ys", 3)),
                      run_time=1.1)
            c.wait_until("already a member")
            self.play(FlashAround(VGroup(*code.find("member x ys", line=3)), color=YELLOW,
                                  time_width=1.5),
                      FlashAround(VGroup(*self.member.find("member", line=0)), color=YELLOW,
                                  time_width=1.5), run_time=1.2)
            # "Otherwise, keep it, consed onto the union of the rest."
            c.wait_until("keep")
            self.play(*reveal(lines[4]), Transform(tb, box("else x :: union xs ys", 4)),
                      run_time=1.1)
            self.remove(*code.text.submobjects)
            self.add(code)
            # "The type is alpha list to alpha list to alpha list."
            c.wait_until("type")
            self.play(FadeOut(tb), FadeIn(reply, shift=0.2 * DOWN), run_time=1.0)
        self.code, self.reply = code, reply


    # ── union.4: the trace on two chains; the result shares ys ──────────────────────
    def clip4_trace(self):
        code, reply = self.code, self.reply
        about = code.get_corner(UL)
        ct = code.copy().scale(SM / BIG, about_point=about)
        rt = reply.copy().scale(SM / BIG, about_point=about)
        d = np.array([CODE_L - ct.get_left()[0], LINE3_Y - VGroup(*ct.line(3)).get_y(), 0])
        ct.shift(d)
        rt.shift(d)

        xs = ConsChain([4, 7, 1]).scale(S)
        xs.shift(slot(0, XS_Y) - xs.cells[0].box.get_center())
        ys = ConsChain([6, 4, 7]).scale(S)
        ys.shift(slot(1, YS_Y) - ys.cells[0].box.get_center())
        new = ConsCell(1).scale(S)
        new.shift(slot(0, YS_Y) - new.box.get_center())
        arr = link(new, ys.cells[0], color=YELLOW)
        xs_lbl = Mono("xs", size=32).next_to(xs.cells[0].box, LEFT, buff=0.3)
        ys_lbl = Mono("ys", size=32).next_to(ys.cells[0].box, DOWN, buff=0.15)
        mk = marker(YELLOW, 0.18).next_to(xs.cells[0].box, UP, buff=0.1)
        ticks = [check_mark(GREEN).scale(0.7).next_to(ys.cells[k].box, UP, buff=0.1) for k in (1, 2)]
        skips = [T("skip", size=30, color=DIM).next_to(xs.cells[k].box, DOWN, buff=0.1)
                 for k in (0, 1)]
        res = place(Code(RESULT, size=SM), CODE_L, VGroup(*rt.text).get_y())   # the reply slot
        shared = T("shared", size=32, color=TEAL).next_to(ys.cells[0].box, UP, buff=0.18)

        def box(sub, i):
            return token_box(code.find(sub, line=i), VGroup(*code.line(i)), height=TB_H, pad=0.3)

        with self.say("c7.union.4") as c:
            # "On our example,"  The code moves up; the two lists come in.
            self.play(Transform(code, ct), Transform(reply, rt),
                      time_span(FadeIn(xs, lag_ratio=0.1), 0.4, 1.2),
                      time_span(FadeIn(ys, lag_ratio=0.1), 0.5, 1.3),
                      time_span(FadeIn(xs_lbl), 0.4, 1.0), time_span(FadeIn(ys_lbl), 0.5, 1.1),
                      time_span(FadeIn(mk, shift=0.2 * DOWN), 0.8, 1.3), run_time=1.3)
            # "four is in six, four, seven, so it's skipped."
            c.wait_until("s1")
            tb = box("if member x ys then union xs ys", 3)
            sc = scan_box(ys.cells[0].box)
            self.play(Create(sc), FadeIn(tb), run_time=0.6)
            self.play(Transform(sc, scan_box(ys.cells[1].box, GREEN)),
                      time_span(FadeIn(ticks[0], scale=0.5), 0.4, 0.8), run_time=0.8)
            c.wait_until("skipped")
            self.play(*dim_cell(xs.cells[0]), FadeIn(skips[0], shift=0.15 * DOWN), FadeOut(sc),
                      run_time=0.8)
            # "So is seven."  (quicker)
            c.wait_until("s2")
            sc = scan_box(ys.cells[0].box)
            self.play(mk.animate.next_to(xs.cells[1].box, UP, buff=0.1),
                      Succession(FadeIn(sc, run_time=0.25),
                                 Transform(sc, scan_box(ys.cells[1].box), run_time=0.3),
                                 Transform(sc, scan_box(ys.cells[2].box, GREEN), run_time=0.3)),
                      time_span(FadeIn(ticks[1], scale=0.5), 0.8, 1.1), run_time=1.1)
            self.play(*dim_cell(xs.cells[1]), FadeIn(skips[1], shift=0.15 * DOWN), FadeOut(sc),
                      run_time=0.6)
            # "One is new, so it's kept,"  The scan runs off the end of ys.
            c.wait_until("s3")
            sc = scan_box(ys.cells[0].box)
            self.play(mk.animate.next_to(xs.cells[2].box, UP, buff=0.1),
                      Succession(FadeIn(sc, run_time=0.2),
                                 Transform(sc, scan_box(ys.cells[1].box), run_time=0.25),
                                 Transform(sc, scan_box(ys.cells[2].box), run_time=0.25),
                                 Transform(sc, scan_box(ys.nil), run_time=0.25),
                                 FadeOut(sc, run_time=0.2)), run_time=1.15)
            c.wait_until("kept")
            self.play(TransformFromCopy(xs.cells[2], new),
                      Transform(tb, box("else x :: union xs ys", 4)),
                      run_time=min(1.2, max(0.6, 0.9 * c.until("s4"))))
            # "and the union of nil with whys gives back whys itself."
            c.wait_until("s4")
            self.play(mk.animate.next_to(xs.nil, UP, buff=0.1), Transform(tb, box("| [] -> ys", 2)),
                      time_span(FlashAround(VGroup(*code.find("| [] -> ys", line=2)), color=YELLOW,
                                            time_width=1.5), 0.4, 1.4), run_time=1.4)
            c.wait_until("gives back")
            self.play(GrowArrow(arr), run_time=1.2)
            # "One, six, four, seven, exactly as the notes say."  The call's reply takes the
            # type's place, read off the result row.
            c.wait_until("result")
            gone = [reply, xs, xs_lbl, mk, tb, *ticks, *skips]
            self.derive([(new.label, res.find("1", line=1)), (ys.cells[0].label, res.find("6", line=1)),
                         (ys.cells[1].label, res.find("4", line=1)),
                         (ys.cells[2].label, res.find("7", line=1))], res,
                        run_time=1.4, extra=[FadeOut(m) for m in gone])
            # "Like the append function, it shares whys, rather than copying it."
            c.wait_until("shared")
            self.play(FadeIn(shared, shift=0.2 * DOWN),
                      FlashAround(VGroup(*ys.cells, ys.nil), color=TEAL, time_width=1.5),
                      run_time=1.3)

    # ── union.5: the cost: up to n comparisons for each of m elements ───────────────
    def clip5_cost(self):
        code = self.code
        gold_tb = token_box(code.find("member x ys", line=3), VGroup(*code.line(3)), color=GOLD,
                            height=TB_H, pad=0.3)
        grid = VGroup(*[Square(SQ).set_stroke(GOLD, 2.5).set_fill(GOLD, 0) for _ in range(9)])
        grid.arrange_in_grid(3, 3, buff=0).move_to([GX, GY, 0])
        rows = [value_label(v, size=38).move_to([grid.get_left()[0] - 0.4, grid[3 * r].get_y(), 0])
                for r, v in enumerate((4, 7, 1))]
        cols = [value_label(v, size=38).move_to([grid[k].get_x(), grid.get_top()[1] + 0.35, 0])
                for k, v in enumerate((6, 4, 7))]
        m_lbl = MathTex("m", font_size=56, color=GOLD).move_to([rows[0].get_x() - 0.65, GY, 0])
        n_lbl = MathTex("n", font_size=56, color=GOLD).next_to(grid, DOWN, buff=0.16)
        le = MathTex(r"\le m \cdot n \text{ comparisons}", font_size=50, color=GOLD)
        big = MathTex(r"\text{time } O(m \cdot n)", font_size=56, color=GOLD)
        VGroup(le, big).arrange(DOWN, buff=0.65, aligned_edge=LEFT).move_to([TX, GY, 0])
        # comparisons actually made: member 4 [6; 4; 7] stops at 4; 7 at 7; 1 runs off the end
        fills = [(0, 0.0, 0.6), (1, 0.6, 1.2),
                 (3, 1.5, 1.9), (4, 1.9, 2.3), (5, 2.3, 2.7),
                 (6, 2.9, 3.2), (7, 3.2, 3.5), (8, 3.5, 3.8)]

        with self.say("c7.union.5") as c:
            # "What does union cost?"  It is all in the member test.
            self.play(FadeIn(gold_tb), FlashAround(VGroup(*code.find("member x ys", line=3)),
                                                   color=GOLD, time_width=1.5), run_time=1.3)
            # "Say the first list is em long, and the second is en long."
            c.wait_until("mn")
            sweep_clear(self, *[time_span(FadeIn(r, shift=0.2 * RIGHT), 0.6, 1.4) for r in rows],
                        time_span(FadeIn(m_lbl, shift=0.2 * RIGHT), 0.6, 1.4),
                        keep=[self.strip, self.member, code, gold_tb], run_time=1.4)
            c.wait_until("and the second")
            self.play(*[FadeIn(k, shift=0.2 * DOWN) for k in cols], FadeIn(n_lbl, shift=0.2 * UP),
                      Create(grid, lag_ratio=0.05), run_time=1.2)
            # "Each member test may scan the whole of the second list, once per element of the first."
            c.wait_until("each member test")
            self.play(*[time_span(grid[i].animate.set_fill(GOLD, 0.75), a, b) for i, a, b in fills],
                      run_time=3.8)
            # "That's at most em times en comparisons, so big O of em times en time."
            c.wait_until("total")
            self.play(FadeIn(le, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("big o")
            self.play(FadeIn(big, shift=0.2 * DOWN), run_time=1.0)
        self.cost_board = [grid, *rows, *cols, m_lbl, n_lbl, le, big, gold_tb]

    # ── union.6: addunion, the iterative variant; order; growing ys; repeats in ys ─────
    def clip6_addunion(self):
        code = self.code
        add = Code(ADD_SRC, size=BIG).scale(SM / BIG)
        add.shift(code.line(0)[0].get_corner(UL) - add.line(0)[0].get_corner(UL))
        for g in [*add.find("addunion", line=3), *add.find("addunion xs (x::ys)", line=4)]:
            g.set_color(YELLOW)
        a = place(Code(ADD_RESULT, size=SM), CODE_L, ROW1)
        b = place(Code(SMALL_U, size=SM), RCOL, ROW1)
        cc = place(Code(SMALL_A, size=SM), RCOL, ROW2)
        e = place(Code(SETS, size=SM), CODE_L, ROW2)
        dch = ConsChain([2, 1, 3]).scale(0.7).move_to([RCOL + 0.25, D_Y, 0], aligned_edge=LEFT)
        d3 = VGroup(dch.cells[2], dch.arrows[2], dch.nil)
        d1 = VGroup(dch.cells[1], dch.arrows[1])
        d0 = VGroup(dch.cells[0], dch.arrows[0])
        waits = code.find("x ::", line=4)

        with self.say("c7.union.6") as c:
            # "Here, each kept element waits to be consed, as in append."
            self.play(*recolor(waits, GOLD), FlashAround(VGroup(*waits), color=GOLD, time_width=1.5),
                      run_time=1.3)
            # "An iterative variant, add-union, conses the new element onto whys instead."
            c.wait_until("acc")
            self.retype([
                (code, add, [(code.find("let rec", line=0), add.find("let rec", line=0)),
                             (code.find("union xs ys =", line=0), add.find("union xs ys =", line=0)),
                             (code.line(1), add.line(1)), (code.line(2), add.line(2)),
                             (code.find("| x::xs -> if member x ys then", line=3),
                              add.find("| x::xs -> if member x ys then", line=3)),
                             (code.find("union xs ys", line=3), add.find("union xs ys", line=3)),
                             (code.find("else", line=4), add.find("else", line=4)),
                             (code.find("union xs", line=4), add.find("union xs", line=4)),
                             (code.find("x ::", line=4), add.find("x::", line=4)),
                             (code.find("ys", line=4), add.find("ys)", line=4)[:2])]),
            ], run_time=1.8)
            self.code = add
            c.wait_until("conses the new")
            self.play(FlashAround(VGroup(*add.find("addunion xs (x::ys)", line=4)), color=YELLOW,
                                  time_width=1.5), run_time=1.2)
            # "It gives the same answer here,"
            c.wait_until("same")
            self.play(*[FadeOut(m) for m in self.cost_board],
                      time_span(FadeIn(a, shift=0.2 * DOWN), 0.4, 1.3), run_time=1.3)
            # "though in general the order can differ,"
            c.wait_until("though in general")
            self.play(FadeIn(b, shift=0.2 * DOWN), time_span(FadeIn(cc, shift=0.2 * DOWN), 0.3, 1.1),
                      time_span(FlashUnder(VGroup(*cc.find("[2; 1; 3]", line=1)), color=YELLOW,
                                           time_width=1.5), 1.1, 1.8),
                      run_time=min(1.8, max(1.2, c.until("grow"))))
            # "and each member test also scans the elements already added."  ys grows at the front.
            c.wait_until("grow")
            self.play(ReplacementTransform(VGroup(*cc.find("[3]", line=0)).copy(), d3),
                      time_span(FadeIn(d1, shift=0.4 * RIGHT), 0.7, 1.2), run_time=1.2)
            sc = scan_box(dch.cells[1].box)
            self.play(Succession(FadeIn(sc, run_time=0.2),
                                 Transform(sc, scan_box(dch.cells[2].box), run_time=0.35),
                                 FadeOut(sc, run_time=0.2)), run_time=0.8)
            self.play(FadeIn(d0, shift=0.4 * RIGHT), run_time=0.7)
            # "Neither version removes a repeat already inside whys, so both rely on being given sets."
            c.wait_until("sets")
            self.play(FadeIn(e, shift=0.2 * DOWN), run_time=1.0)
            self.sets_born = self.time
            c.wait_until("already inside")
            reds = [e.find("2", line=0, nth=1)[0], e.find("2", line=1, nth=1)[0]]
            self.play(*recolor(reds, RED), *flash(reds, RED, buff=0.1, time_width=1.5), run_time=1.2)
