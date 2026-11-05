"""Chapter 7, scene 3: Exercise 5.2's solution, selection sort in OCaml (select, selsort, a trace,
the tests, and the remove-every-copy pitfall). Clips c7.selcode.1 - c7.selcode.6.

Exports for ch7's recap: select_code() (the select block as styled here) and dups_reply() (the
`- : int list = [1; 3; 3; 5; 5]` reply, its list GREEN). Every reply checked with OCaml 5.4.1.
"""
# style: 2
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

K = load_scene("ch6_s4_hints1")          # the exercise-card kit
RUNNING = [3, 5, 9, 4, 7]
LEFT_X = -6.3                            # left edge of code blocks

SELECT_SRC = ("let rec select m rest = function\n"
              "  | [] -> (m, rest)\n"
              "  | x::xs -> if x <= m then select x (m::rest) xs\n"
              "             else select m (x::rest) xs")
SELSORT_SRC = ("let rec selsort = function\n"
               "  | [] -> []\n"
               "  | x::xs -> let (m, rest) = select x [] xs in\n"
               "             m :: selsort rest")
MINIMUM_SRC = ("let rec minimum m = function\n"
               "  | [] -> m\n"
               "  | x::xs -> if x <= m then minimum x xs\n"
               "             else minimum m xs")
REMOVE_SRC = ("let rec remove m = function\n"
              "  | [] -> []\n"
              "  | x::xs -> if x = m then remove m xs\n"
              "             else x :: remove m xs")
REMOVE_FIX = ("let rec remove m = function\n"
              "  | [] -> []\n"
              "  | x::xs -> if x = m then xs\n"
              "             else x :: remove m xs")
SELSORT2_SRC = ("let rec selsort2 = function\n"
                "  | [] -> []\n"
                "  | x::xs -> let m = minimum x xs in\n"
                "             m :: selsort2 (remove m (x::xs))")


def ocode(src, size=28):
    return Code(src, size=size)


def select_code(size=28):
    """The select block, keywords BLUE, every `select` YELLOW, [] and :: TEAL."""
    code = Code(SELECT_SRC, size=size)
    for k in range(3):
        code.find("select", nth=k).set_color(YELLOW)
    return code


def dups_reply(size=30):
    """`- : int list = [1; 3; 3; 5; 5]`, its list GREEN."""
    code = Code("- : int list = [1; 3; 3; 5; 5]", size=size)
    code.find("[1; 3; 3; 5; 5]").set_color(GREEN)
    return code


def left_at(mob, y, x=LEFT_X):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def top_at(mob, top, x=LEFT_X):
    mob.move_to([x, 0, 0], aligned_edge=LEFT)
    return mob.shift(UP * (top - mob.get_top()[1]))


def fit(c, cue=None, frac=0.7, lo=0.6, hi=1.5, nth=0):
    return min(hi, max(lo, frac * c.until(cue, floor=0.0, nth=nth)))


def helper_box():
    """ch6 s4's hint: "one job, two results" over (?, ?) with "smallest" and "rest" beneath."""
    box_t = T("one job, two results", size=30)
    box = RoundedRectangle(corner_radius=0.18, width=box_t.width + 0.5, height=0.75)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.1)
    box_t.move_to(box)
    arr = Arrow(UP * 0.22, DOWN * 0.22, buff=0, stroke_width=3, color=FG,
                max_tip_length_to_length_ratio=0.35, tip_length=0.18)
    lp, q1, cm, q2, rp = (T("(", size=50), T("?", size=50, color=GOLD), T(",", size=50),
                          T("?", size=50, color=GOLD), T(")", size=50))
    pair = VGroup(lp, q1, cm, q2, rp).arrange(RIGHT, buff=0.2)
    cm.next_to(q1, RIGHT, buff=0.6)
    q2.next_to(cm, RIGHT, buff=0.6).set_y(q1.get_y())
    rp.next_to(q2, RIGHT, buff=0.2).set_y(lp.get_y())
    cm.align_to(q1, DOWN).shift(DOWN * 0.1)
    VGroup(VGroup(box, box_t), arr, pair).arrange(DOWN, buff=0.15)
    l1 = T("smallest", size=30, color=DIM).next_to(q1, DOWN, buff=0.18)
    l2 = T("rest", size=30, color=DIM).next_to(q2, DOWN, buff=0.18).align_to(l1, UP)
    g = VGroup(box, box_t, arr, lp, q1, cm, q2, rp, l1, l2)
    (g.box, g.box_t, g.arr, g.lp, g.q1, g.cm, g.q2, g.rp, g.l1, g.l2) = g.submobjects
    return g


def ghost_cell(v, side=0.6):
    sq = DashedVMobject(Square(side), num_dashes=16).set_stroke(RED, 2.5)
    lab = T(str(v), size=32, color=RED).move_to(sq)
    g = VGroup(sq, lab).set_opacity(0.75)
    return g


class SelectionCode(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        K.hold_for(self, self.label_born, len("nothing removed by value"))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # 1: the four cards; 5.2 grows from its card: task, slot, tests; pause
    def clip1(self):
        row = K.four_cards()
        card = K.card_5_2()
        tag = K.pause_tag()
        self.card, self.tag = card, tag
        with self.say("c7.selcode.1") as c:
            self.play(*appear(row.cards, row.note, lag=0.2), run_time=0.8)  # early: the overview, recalled
            src = row.cards[1].frame
            others = [m for m in (*row.cards, row.note) if m is not row.cards[1]]
            self.play(*during([TransformFromCopy(src, card.frame)], 0, 0.6),
                      *during([FadeOut(m) for m in (*others, row.cards[1])], 0, 0.45),
                      *during(appear(card.header), 0.5, 1), run_time=1.4)
            c.wait_until(own_word=card.task, cue="implement")
            self.play(*appear(card.task, card.name, lag=0.3),
                      *during([FadeIn(card.slot, shift=0.2 * DOWN)], 0.4, 1), run_time=1.4)
            c.wait_until("test it")
            self.play(*appear(card.tests[0]), run_time=1.0)
            c.wait_until("three five three")
            self.play(*appear(card.tests[1]), run_time=1.0)
            c.wait_until("repeats")
            self.play(*appear(card.rep, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("stop")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.7)
            self.play(FlashAround(tag[0], color=YELLOW, time_width=1.5, buff=0.12), run_time=1.2)

    # 2: the helper's pair, unzip, then select, walked
    def clip2(self):
        card, tag = self.card, self.tag
        head = VGroup(card.name, card.slot)
        head_t = head.copy().scale(0.8).move_to([LEFT_X, 3.42, 0], aligned_edge=LEFT)
        hb = helper_box().move_to([-3.95, 1.5, 0])
        uz = ocode("let xs, ys = unzip pairs in", 30)
        uz.move_to([6.5, 2.45, 0], aligned_edge=RIGHT).set_opacity(0.6)
        uz.find("xs, ys").set_color(YELLOW).set_opacity(1)
        uz_tag = T("Lecture 4", size=30, color=DIM).next_to(uz, DOWN, buff=0.25).align_to(uz, RIGHT)
        code = top_at(select_code(28), -0.15)
        m_new = Mono("m", size=46, color=YELLOW).move_to(hb.q1)
        r_new = Mono("rest", size=46, color=YELLOW)
        r_new.move_to(hb.q2.get_left(), aligned_edge=LEFT).set_y(hb.q2.get_y())
        dx = r_new.width - hb.q2.width
        self.hb, self.uz, self.uz_tag, self.code, self.head = hb, uz, uz_tag, code, head
        self.m_new, self.r_new = m_new, r_new
        with self.say("c7.selcode.2") as c:
            # "The key step returns two things at once, the smallest item and the rest."
            gone = [card.frame, card.header, card.task, *card.tests, card.rep]
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during([Transform(head, head_t)], 0.2, 0.8),
                      *during(appear(hb.box, hb.box_t), 0.55, 1), run_time=1.5)  # early: the helper's caption, recalled from ch6
            self.play(GrowArrow(hb.arr), *appear(hb.lp, hb.q1, hb.cm, hb.q2, hb.rp, lag=0.05),
                      run_time=1.0)
            c.wait_until(own_word=hb.l1, cue="smallest")
            self.play(*appear(hb.l1), run_time=0.7)
            c.wait_until(own_word=hb.l2, cue="the rest")
            self.play(*appear(hb.l2), run_time=0.7)
            # "So it returns a pair, like unzip last lecture."
            c.wait_until("pair")
            self.play(*during([FadeOut(tag)], 0, 0.4), *during(appear(uz, shift=0.25 * LEFT), 0.3, 1), run_time=1.2)
            c.wait_until("unzip")
            self.play(*appear(uz_tag), FlashAround(uz.find("xs, ys"), color=YELLOW, time_width=1.5),
                      run_time=1.2)
            # "We'll call it select."
            c.wait_until("select")
            self.play(*appear(code, shift=0.25 * UP), run_time=1.2)  # early: the code shown whole, then walked
            # "It carries two values along."
            c.wait_until("carry")
            box = token_box(code.find("m rest", line=0), code.line(0))
            self.play(FadeIn(box), run_time=0.8)
            # "Em is the smallest so far, and rest holds the items set aside."
            c.wait_until("em is")
            self.play(*swap(hb.q1, m_new), run_time=1.0)
            c.wait_until("rest holds")
            self.play(*swap(hb.q2, r_new), hb.rp.animate.shift(RIGHT * dx),
                      hb.l2.animate.set_x(r_new.get_x()), run_time=1.0)
            # "When the list runs out, it returns the pair."
            c.wait_until("done")
            self.play(Transform(box, token_box(code.find("[] -> (m, rest)"), code.line(1))),
                      run_time=fit(c, "returns the pair", hi=1.2))
            # "Otherwise, it compares the next item, ex, with em."
            c.wait_until("step")
            self.play(Transform(box, token_box(code.find("x <= m"), code.line(2))), run_time=1.0)
            # "The smaller becomes the new em, and the other is set aside."
            c.wait_until("new em")
            self.play(Transform(box, token_box(code.find("select x (m::rest) xs"), code.line(2))),
                      run_time=0.8)
            c.wait_until("set aside", nth=1)
            box2 = token_box(code.find("(x::rest)"), code.line(3))
            self.play(Transform(box, token_box(code.find("(m::rest)"), code.line(2))), FadeIn(box2),
                      run_time=max(0.4, min(0.8, c.until())))
        self.box, self.box2 = box, box2

    # 3: select's type; selsort, walked; its type fills ch6's slot
    def clip3(self):
        code, hb = self.code, self.hb
        ty = ocode("val select :\n  'a -> 'a list -> 'a list -> 'a * 'a list = <fun>", 28)
        top_at(ty, code.get_bottom()[1] - 0.3)
        ss = top_at(ocode(SELSORT_SRC, 28), -0.35)
        ss.find("selsort", nth=1).set_color(YELLOW)
        ss.find("select").set_color(YELLOW)
        sty = left_at(ocode("val selsort : 'a list -> 'a list = <fun>", 28), ss.get_bottom()[1] - 0.5)
        dy = 3.05 - code.get_top()[1]
        slot = self.head[1]
        tick = check_mark().scale(0.8).move_to(slot.q)
        self.ty, self.ss, self.sty = ty, ss, sty
        with self.say("c7.selcode.3", gap=1.2) as c:
            # "Select returns an alpha, paired with an alpha list."
            self.play(*disappear(self.box, self.box2), *appear(ty), run_time=1.0)
            c.wait_until("paired")
            self.play(FlashUnder(ty.find("'a * 'a list"), color=YELLOW, time_width=1.5),
                      FlashAround(VGroup(hb.lp, hb.rp), color=YELLOW, time_width=1.5), run_time=1.5)
            # "The sort itself, sel-sort, is short."
            c.wait_until("sort")
            leaving = [m for m in hb if m not in (hb.q1, hb.q2)] + [self.uz, self.uz_tag, self.m_new, self.r_new]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.4),
                      *during([code.animate.shift(UP * dy), ty.animate.shift(UP * dy)], 0.2, 0.7),
                      *during(appear(ss, shift=0.25 * UP), 0.7, 1), run_time=2.0)  # early: the code shown whole, then walked
            # "The empty list is already sorted."
            c.wait_until("nil")
            box = token_box(ss.find("[] -> []"), ss.line(1))
            self.play(FadeIn(box), run_time=0.8)
            # "Otherwise, start select with the head as the smallest so far, and nothing set aside, ..."
            c.wait_until("start")
            self.play(Transform(box, token_box(ss.find("select x [] xs"), ss.line(2))), run_time=1.0)
            c.wait_until("take its pair apart")
            self.play(Transform(box, token_box(ss.find("let (m, rest) ="), ss.line(2))), run_time=1.0)
            # "Then cons the smallest onto the sorted rest."
            c.wait_until("cons")
            self.play(Transform(box, token_box(ss.find("m :: selsort rest"), ss.line(3))), run_time=1.0)
            # "Sel-sort takes an alpha list to an alpha list."
            c.wait_until("stype")
            self.play(*disappear(box), *appear(sty), run_time=1.0)
            self.play(*swap(slot.q, tick), slot.box.animate.set_stroke(GREEN),
                      FlashAround(slot, color=GREEN, time_width=1.5), run_time=1.2)
        self.tick0 = tick

    # 4: a trace of select, the backwards rest, then the two tests
    def clip4(self):
        code = self.code
        inp = left_at(ocode("select 3 [] [5; 9; 4; 7];;", 32), 1.0)
        y = -0.15
        m_lbl = left_at(T("m =", size=36, color=DIM), y)
        m_sq = Square(0.8).set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12)
        m_sq.next_to(m_lbl, RIGHT, buff=0.25)
        m_val = value_label(3, color=YELLOW).move_to(m_sq)
        r_lbl = T("rest =", size=36, color=DIM).move_to([-3.75, y, 0], aligned_edge=LEFT)
        vals = [7, 4, 9, 5]
        cells = [ConsCell(v).scale(0.7).move_to([-1.75 + 1.61 * k, y, 0]) for k, v in enumerate(vals)]
        for cl in cells:
            cl.label.scale(1.15)
        nil = Nil().scale(0.85).move_to([cells[-1].get_right()[0] + 0.95, y, 0])
        links = [link(cells[k], cells[k + 1] if k < 3 else nil) for k in range(4)]
        reply = left_at(ocode("- : int * int list = (3, [7; 4; 9; 5])", 32), -1.3)
        H3 = load_scene("ch3_s6_trace")
        tree = H3.call_tree(RUNNING, size=28, pitch=0.8, gap=0.8, badges=False, pivot_color=None,
                            max_depth=1)
        tree.set_color(DIM)
        tree.place(1.0, [1.8, -2.25, 0])
        rnode = tree.node([7, 4, 9, 5]).body
        bb = T("built backwards", size=28, color=YELLOW).next_to(rnode, RIGHT, buff=0.3)
        p3 = K.Tag("Part 3: sorted next, so harmless", DIM).move_to([LEFT_X, -2.25, 0], aligned_edge=LEFT)
        p3.set_y(-2.25)

        t1 = left_at(ocode("selsort [3; 5; 9; 4; 7];;", 34), 0.95)
        r1 = left_at(ocode("- : int list = [3; 4; 5; 7; 9]", 34), 0.3)
        k1 = check_mark().next_to(r1, RIGHT, buff=0.45)
        t2 = left_at(ocode("selsort [3; 5; 3; 1; 5];;", 34), -0.95)
        rep = K.Tag("repeats", PURPLE).next_to(t2, RIGHT, buff=0.45)
        r2 = left_at(ocode("- : int list = [1; 3; 3; 5; 5]", 34), -1.6)
        k2 = check_mark().next_to(rep, RIGHT, buff=0.3)
        lst2 = r2.find("[1; 3; 3; 5; 5]")
        with self.say("c7.selcode.4", gap=0.8) as c:
            # "On our list, select keeps three as the smallest, ..."
            leaving = [self.ss, self.sty, self.ty, *self.head, self.tick0]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.4),
                      *during([code.animate.shift(UP * (3.55 - code.get_top()[1]))], 0.2, 0.8),
                      *during(appear(inp), 0.6, 1), run_time=1.6)
            c.wait_until("keeps three")
            self.play(*appear(m_lbl, m_sq, m_val, lag=0.15), run_time=1.0)
            c.wait_until("sets the others aside")
            self.play(*appear(r_lbl, nil, lag=0.2), run_time=0.8)
            for i, k in enumerate((3, 2, 1, 0)):
                g = inp.find(str(vals[k]))
                rt = 1.0 if i == 0 else 0.6
                self.play(*recolor(g, DIM), FadeIn(cells[k], shift=0.2 * DOWN), GrowArrow(links[k]),
                          run_time=rt)
            self.play(*appear(reply), run_time=min(1.0, max(0.5, c.until("backwards", floor=0.0))))
            # "That's backwards, like quicksort's partition in part three, ..."
            c.wait_until("backwards")
            self.play(*recolor(reply.find("[7; 4; 9; 5]"), YELLOW),
                      *appear(tree, shift=None), run_time=1.2)
            self.play(rnode.animate.set_color(YELLOW), *appear(bb, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("part three")
            self.play(*appear(p3, shift=0.2 * RIGHT), run_time=0.9)  # early: the inset's caption
            # "Selecting four, five, seven and nine in turn sorts the list."
            c.wait_until("in turn")
            sweep_clear(self, *appear(t1, r1, lag=0.4), keep=[code], run_time=1.6)
            self.play(Create(k1), run_time=0.8)
            # "With repeats, three, five, three, one, five becomes one, three, three, five, five."
            c.wait_until("dups")
            self.play(*appear(t2), *during(appear(rep, shift=0.2 * LEFT), 0.4, 1), run_time=1.1)
            c.wait_until("becomes")
            self.play(*appear(r2), run_time=1.0)
            c.wait_until("one three three")
            twins = [*r2.find("3", nth=0), *r2.find("3", nth=1), *r2.find("5", nth=0), *r2.find("5", nth=1)]
            self.play(*recolor(twins, YELLOW), *flash(twins, color=YELLOW, time_width=1.5),
                      run_time=1.4)
            # "Every copy survives."
            c.wait_until("every copy")
            self.play(*recolor(lst2, GREEN), rep.box.animate.set_stroke(GREEN).set_fill(GREEN, 0.12),
                      rep.label.animate.set_color(GREEN), Create(k2),
                      run_time=max(0.5, min(1.2, c.until())))

    # 5: the pitfall: minimum, remove (deletes every copy), selsort2 loses items
    def clip5(self):
        mn = top_at(ocode(MINIMUM_SRC, 28), 3.6)
        mn_v = left_at(ocode("val minimum : 'a -> 'a list -> 'a = <fun>", 28), mn.get_bottom()[1] - 0.45)
        rm = top_at(ocode(REMOVE_SRC, 30), 0.45)
        rm_v = left_at(ocode("val remove : 'a -> 'a list -> 'a list = <fun>", 28), rm.get_bottom()[1] - 0.5)
        bad = rm.find("then remove m xs")
        rm_t = rm.copy().scale(28 / 30)
        top_at(rm_t, 3.6)
        s2 = top_at(ocode(SELSORT2_SRC, 28), rm_t.get_bottom()[1] - 0.3)
        s2_v = left_at(ocode("val selsort2 : 'a list -> 'a list = <fun>", 28), s2.get_bottom()[1] - 0.36)
        u1 = left_at(ocode("selsort2 [3; 5; 9; 4; 7];;", 28), s2_v.get_y() - 0.52)
        v1 = left_at(ocode("- : int list = [3; 4; 5; 7; 9]", 28), u1.get_y() - 0.42)
        k1 = check_mark().scale(0.85).next_to(v1, RIGHT, buff=0.4)
        u2 = left_at(ocode("selsort2 [3; 5; 3; 1; 5];;", 28), v1.get_y() - 0.46)
        v2 = left_at(ocode("- : int list = [1; 3; 5]", 28), u2.get_y() - 0.42)
        x2 = cross_mark().next_to(v2, RIGHT, buff=0.45)
        ghosts = VGroup(ghost_cell(3), ghost_cell(5)).arrange(RIGHT, buff=0.25)
        ghosts.next_to(x2, RIGHT, buff=0.5)
        with self.say("c7.selcode.5") as c:
            # "Here's a tempting alternative."
            self.play(*[FadeOut(m, shift=0.4 * RIGHT) for m in self.mobjects], run_time=1.0)
            # "Find the smallest item first, then remove it from the list."
            c.wait_until("smallest")
            self.play(*appear(mn, mn_v, lag=0.4), run_time=1.2)
            c.wait_until("remove it")
            self.play(*appear(rm, rm_v, lag=0.4), run_time=1.2)
            # "But this remove keeps going after it finds a match, so it deletes every copy."
            c.wait_until("keeps going")
            self.play(*recolor(bad, RED), FlashUnder(bad, color=RED, time_width=1.5), run_time=1.4)
            # "On our list, with no repeats, it works."
            c.wait_until("chainok")
            self.play(*during([FadeOut(m) for m in (mn, mn_v, rm_v)], 0, 0.4),
                      *during([Transform(rm, rm_t)], 0.35, 1), run_time=1.2)
            self.play(*appear(s2, s2_v, lag=0.3), run_time=1.1)
            c.wait_until("it works")
            self.play(*appear(u1, v1, lag=0.3), run_time=1.0)
            self.play(Create(k1), run_time=0.6)
            # "On three, five, three, one, five, it returns just one, three, five."
            c.wait_until("lost")
            self.play(*appear(u2), run_time=0.9)
            c.wait_until("just one")
            self.play(*appear(v2), Create(x2), run_time=1.0)
            # "Two items have vanished."
            c.wait_until("vanished")
            self.play(*appear(*ghosts, shift=0.2 * UP, lag=0.3), run_time=1.0)
        self.rm, self.s2, self.v2, self.x2, self.ghosts = rm, s2, v2, x2, ghosts
        self.pit = [rm, s2, s2_v, u1, v1, k1, u2]

    # 6: the fix; enter selsort2 again; select never removes by value
    def clip6(self):
        rm, s2, v2, x2 = self.rm, self.s2, self.v2, self.x2
        new = ocode(REMOVE_FIX, 28)
        top_at(new, rm.get_top()[1])
        good = new.find("xs", line=2, nth=1)
        v2n = left_at(ocode("- : int list = [1; 3; 3; 5; 5]", 28), v2.get_y())
        k2 = check_mark().scale(0.85).next_to(v2n, RIGHT, buff=0.4)
        sel = select_code(30).move_to(UP * 0.5)
        lab = T("nothing removed by value", size=36, color=GREEN).next_to(sel, DOWN, buff=0.8)
        conses = [sel.find("(m::rest)"), sel.find("(x::rest)")]
        with self.say("c7.selcode.6") as c:
            # "Remove should stop at the first copy, and return the rest of the list unchanged."
            self.play(*edit(rm, new), run_time=1.5)
            self.play(*recolor(good, GREEN), FlashAround(good, color=GREEN, time_width=1.5), run_time=1.2)
            # "In the toplevel, enter the sort again too, or it keeps the old remove."
            c.wait_until("again")
            self.play(FlashAround(s2, color=YELLOW, time_width=1.5, buff=0.12), run_time=1.1)
            self.play(*swap(v2, v2n, shift=None), *swap(x2, k2, shift=None),
                      *during(disappear(*self.ghosts), 0, 0.45), run_time=1.2)
            # "Select avoids all this, because it never removes anything by value."
            c.wait_until("aside")
            sweep_clear(self, *appear(sel, shift=0.25 * UP), run_time=1.2)  # early: select recalled whole
            self.play(*[a for g in conses for a in recolor(g, GREEN)],
                      *flash(conses, color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until(own_word=lab, cue="by value")
            self.play(*appear(lab), run_time=0.9)
            self.label_born = self.time
