"""Chapter 1, scene 3: tuples vs lists, the [1, 2] trap, arrays vs lists, @ and List.rev."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, TransformMatchingStrings, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TUP = YELLOW   # tuple syntax: round brackets and commas
LST = TEAL     # list syntax: square brackets and semicolons
DIMMED = 0.25  # spotlight: everything else drops to this opacity (PATTERNS P9)
SLOT = 1.0     # array slot side
CELL_L = 1.2   # list-chain box side


# ── helpers (local to this scene) ──────────────────────────────────────────────
# Everything that animates part of a Code works on its glyphs one by one: wrapping them
# in a VGroup/AnimationGroup makes manim pull them out of the Code (LESSONS.md).
def chars(code, ch):
    """Every glyph of `code` that is the character `ch`, as a list of glyphs."""
    return [g for k in range(code.src.count(ch)) for g in code.find(ch, nth=k)]


def recolor(glyphs, color):
    return [g.animate.set_color(color) for g in glyphs]


def flash(mobs, color, **kw):
    """3b1b's FlashAround on each item; it removes itself (P6)."""
    return [FlashAround(m, color=color, **kw) for m in mobs]


def token_box(glyphs, code, color):
    """The sliding highlight (P8): thin stroke, faint fill, behind the text, as tall as the line."""
    g = VGroup(*glyphs)
    r = Rectangle(width=max(g.width + 0.22, 0.42), height=code.height + 0.24,
                  stroke_color=color, stroke_width=2).set_fill(color, opacity=0.25)
    return r.move_to([g.get_x(), code.get_y(), 0]).set_z_index(-1)


def restyle(mob, op=None, outline=None, width=None, fill=None, shift=None):
    """One Transform that dims/restores (P9), recolours and moves `mob` together, so no two
    animations fight over the same object. Opacity goes on the fill of filled parts (text,
    arrow tips) and on the stroke of outlines, which stay unfilled; `outline`/`width`
    restyle the outlines, `fill` recolours the filled parts."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            if fill is not None:
                leaf.set_color(fill)
            if op is not None:
                leaf.set_opacity(op)
        else:
            if outline is not None or width is not None:
                leaf.set_stroke(color=outline, width=width)
            if op is not None:
                leaf.set_stroke(opacity=op)
    if shift is not None:
        t.shift(shift)
    return Transform(mob, t)


def set_alpha(mobs, op):
    return [restyle(m, op) for m in mobs]


def underline(mob, color, buff=0.14):
    return Line(mob.get_corner(DL), mob.get_corner(DR), color=color, stroke_width=5).shift(DOWN * buff)


def box(content, width=1.0, height=1.0, color=BLUE):
    """An element box with something inside."""
    frame = Rectangle(width=width, height=height, stroke_color=color, stroke_width=3)
    return VGroup(frame, content.move_to(frame))


def marker(color=YELLOW, scale=0.24):
    """A downward-pointing triangle that sits above a slot or a box."""
    return Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(scale).rotate(PI)


def above(mob, buff=0.2):
    """Where a marker's centre goes when it sits just above `mob`."""
    return mob.get_top() + UP * (buff + 0.18)


class TuplesAndArrays(NarratedScene):
    def construct(self):
        self.tuple_vs_list()
        self.the_trap()
        self.arrays_vs_lists()
        self.free_tools()
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.1)  # a truly empty last frame (FadeOut's final frame is not quite alpha 0)

    def sweep_clear(self, *incoming, run_time=1.2):
        """Clear the board in a lagged sweep (P18), in the same play as whatever needs the
        space (pass it time_span'd so it arrives as the old content leaves)."""
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.1),
                  *incoming, run_time=run_time)

    # cmp.1: tuple (1, "one") as the hero, then beside the list [3; 5; 9]
    def tuple_vs_list(self):
        S = 0.711                 # the tuple column shrinks by this when the list arrives
        LX, RX, DIV_X = -3.6, 3.25, -0.45   # the list column is wider: it grows to 5 elements

        # final layout first (P4): the tuple centred and big ...
        tup_head = T("Tuple", size=58).move_to(UP * 2.5)
        tup = Code('(1, "one")', size=72).move_to(UP * 1.15)
        # int * string, int under the 1 and string under "one" (one Text, so the
        # baselines agree; the pieces are then slid sideways)
        ref = Mono("int * string", size=46, color=GREEN).move_to(UP * 0.05)
        t_int, t_star, t_str = VGroup(*ref[0:3]), ref[3], VGroup(*ref[4:10])
        t_star.set_color("#BBBBBB")
        t_int.set_x(tup.find("1").get_x())
        t_str.set_x(tup.find('"one"').get_x())
        t_star.set_x((t_int.get_right()[0] + t_str.get_left()[0]) / 2)
        cap_fixed = T("fixed size", size=48).move_to(DOWN * 1.45)
        cap_mixed = T("different types", size=48).move_to(DOWN * 2.45)
        tcol = VGroup(tup_head, tup, t_int, t_star, t_str, cap_fixed, cap_mixed)

        # ... and where it goes (this copy only gives positions; the real target is built
        # at play time, after recolouring), with the list column matched to it row for row
        tcol_end = tcol.copy().scale(S).move_to([LX, tcol.get_y(), 0])
        e_head, e_code, e_int, _, _, e_fixed, e_mixed = tcol_end
        divider = Line(UP * 2.95, DOWN * 2.75, color=DIM, stroke_width=2).set_x(DIV_X)
        lst_head = T("List", size=58).scale(S).move_to([RX, e_head.get_y(), 0])
        lists = [Code(s, size=72 * S) for s in ("[3; 5; 9]", "[3; 5; 9; 2; 10]")]
        for code in lists:
            code.move_to([RX, e_code.get_y(), 0])
        lst = lists[0]
        lst_type = Mono("int list", size=46, color=GREEN).scale(S).move_to([RX, 0, 0])
        lst_type.align_to(e_int, DOWN)
        cap_any = T("any length", size=48).scale(S).move_to([RX, e_fixed.get_y(), 0])
        cap_same = T("same type", size=48).scale(S).move_to([RX, e_mixed.get_y(), 0])

        with self.say("c1.cmp.1") as c:
            c.wait_until("tuples")
            self.play(FadeIn(tup_head, shift=0.3 * DOWN), FadeIn(tup, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("round brackets")
            parens = chars(tup, "(") + chars(tup, ")")
            self.play(*flash(parens, TUP), *recolor(parens, TUP), run_time=1.0)
            c.wait_until("commas")
            comma = chars(tup, ",")
            self.play(*flash(comma, TUP), *recolor(comma, TUP), run_time=1.0)

            c.wait_until("fixed")
            self.play(FadeIn(cap_fixed, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("different types")
            self.play(FadeIn(cap_mixed, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("integer")
            self.play(FadeIn(t_int, shift=0.3 * UP), run_time=0.8)
            c.wait_until("string")
            self.play(FadeIn(t_str, shift=0.3 * UP), FadeIn(t_star), run_time=0.9)

            c.wait_until("list")  # {list}: the tuple steps aside for the list
            self.play(tcol.animate.scale(S).move_to(tcol_end), Create(divider),
                      FadeIn(VGroup(lst_head, lst), shift=0.3 * DOWN), run_time=1.5)

            c.wait_until("semicolons")
            semis = chars(lst, ";")
            self.play(*flash(semis, LST), *recolor(semis, LST), run_time=1.0)
            for g in chars(lists[1], ";"):
                g.set_color(LST)

            c.wait_until("any length")
            self.play(*self.grow(lists[0], lists[1]), FadeIn(cap_any, shift=0.3 * DOWN), run_time=1.2)
            self.swap(lists[0], lists[1])
            lst = lists[1]

            c.wait_until("every element")
            self.play(FadeIn(lst_type, shift=0.3 * UP), FadeIn(cap_same, shift=0.3 * DOWN), run_time=0.9)

        self.tup, self.lst = tup, lst

    def grow(self, old, new):
        """Slide the old list's glyphs onto their places in the longer list; the new tail
        fades in. Old and new share a prefix and the closing bracket."""
        n_old, n_new = len(old.text), len(new.text)
        anims = [old.text[i].animate.move_to(new.text[i]) for i in range(n_old - 1)]
        anims.append(old.text[-1].animate.move_to(new.text[-1]))
        anims += [FadeIn(new.text[i], shift=LEFT * 0.15) for i in range(n_old - 1, n_new - 1)]
        return anims

    def swap(self, old, new):
        """After grow(): replace the moved glyphs and faded-in tail by the real new Code."""
        self.remove(*old.get_family(), *new.get_family())
        self.add(new)

    # cmp.2: [1, 2] is a list of ONE pair
    def the_trap(self):
        inp = Code("[1, 2]", size=72).move_to(UP * 2.55)
        reply = Code("- : (int * int) list = [(1, 2)]", size=42).move_to(UP * 1.3)
        for g in chars(reply, "(") + chars(reply, ")") + chars(reply, ","):
            g.set_color(TUP)
        fixed = Code("[1; 2]", size=72).move_to(inp)
        fixed_reply = Code("- : int list = [1; 2]", size=42).move_to(reply)
        for code in (fixed, fixed_reply):
            for g in chars(code, ";"):
                g.set_color(LST)
        for g in chars(fixed, "[") + chars(fixed, "]"):
            g.set_color(LST)

        DIAG_Y, BOX = -1.05, 1.25

        def brackets_around(inner):
            lb = Mono("[", size=110, color=LST).next_to(inner, LEFT, buff=0.28)
            rb = Mono("]", size=110, color=LST).next_to(inner, RIGHT, buff=0.28)
            return VGroup(lb, rb)

        def at_diag(*parts):
            VGroup(*parts).move_to(UP * DIAG_Y)

        two = VGroup(box(Code("1", size=52), BOX, BOX, color=DIM),
                     box(Code("2", size=52), BOX, BOX, color=DIM)).arrange(RIGHT, buff=0.35)
        br = brackets_around(two)
        at_diag(br, two)
        cross = Cross(two, stroke_color=RED, stroke_width=7, scale_factor=1.05)

        pair = Code("(1, 2)", size=52)
        for g in chars(pair, "(") + chars(pair, ")") + chars(pair, ","):
            g.set_color(TUP)
        one = box(pair, pair.width + 0.7, BOX)
        br_one = brackets_around(one)
        at_diag(br_one, one)
        one_lab = T("one element", size=40).next_to(VGroup(br_one, one), DOWN, buff=0.35)

        good = VGroup(box(Code("1", size=52), BOX, BOX), box(Code("2", size=52), BOX, BOX))
        good.arrange(RIGHT, buff=0.35)
        br_good = brackets_around(good)
        at_diag(br_good, good)
        VGroup(br_good, good).shift(RIGHT * 3.3)
        good_lab = T("two elements", size=40, color=GREEN).next_to(VGroup(br_good, good), DOWN, buff=0.35)

        with self.say("c1.cmp.2") as c:
            # one highlight box slides from the tuple's comma to the list's semicolon (P8)
            c.wait_until("comma")
            hb = token_box(chars(self.tup, ","), self.tup, TUP)
            self.play(FadeIn(hb), run_time=0.6)
            c.wait_until("semicolon")
            self.play(hb.animate.become(token_box(chars(self.lst, ";")[:1], self.lst, LST)), run_time=0.8)
            # the comparison stays up until [1, 2] needs the space
            c.wait_until("trap")  # {trap}
            self.sweep_clear(time_span(FadeIn(inp, shift=0.3 * DOWN), 0.5, 1.3), run_time=1.3)
            c.wait_until("square brackets")
            brs = chars(inp, "[") + chars(inp, "]")
            self.play(*flash(brs, LST), *recolor(brs, LST), run_time=1.0)
            c.wait_until("comma", nth=1)
            cm = chars(inp, ",")
            hb = token_box(cm, inp, TUP)
            self.play(FadeIn(hb), *flash(cm, TUP), *recolor(cm, TUP), run_time=1.0)

            # {reveal}: OCaml's reply is born from the input (P5)
            c.wait_until("reveal")
            body = VGroup(*reply.find("[(1, 2)]"))
            prefix = VGroup(*reply.find("- : (int * int) list ="))
            self.play(TransformFromCopy(VGroup(*inp.text), body), FadeIn(prefix, shift=0.3 * DOWN),
                      run_time=1.0)
            self.remove(body, prefix)
            self.add(reply)

            c.wait_until("two numbers")
            self.play(FadeIn(br), FadeIn(two), time_span(Create(cross), 0.8, 1.4), run_time=1.4)

            c.wait_until("it sees")
            self.play(FadeOut(cross), FadeTransform(two, one), Transform(br, br_one),
                      time_span(FadeIn(one_lab, shift=0.3 * UP), 0.9, 1.5), run_time=1.5)

            c.wait_until("the pair")
            self.play(hb.animate.become(token_box(reply.find("(int * int)"), reply, TUP)),
                      FlashAround(pair, color=TUP, time_width=1.5), run_time=1.2)

            # {lesson}: back to the comma; it becomes a semicolon, the box riding along
            # (P12), and OCaml's reply changes with it
            c.wait_until("lesson")
            self.play(hb.animate.become(token_box(chars(inp, ","), inp, TUP)), run_time=0.6)
            c.wait_until("a list", nth=2)
            self.play(FadeTransform(inp, fixed), hb.animate.become(token_box(fixed.find(";"), fixed, LST)),
                      TransformMatchingStrings(reply, fixed_reply), run_time=1.0)
            # the one-element picture steps aside (dimmed), the right one arrives beside it
            self.play(restyle(VGroup(br, one, one_lab), 0.4, shift=LEFT * 3.3),
                      FadeIn(VGroup(br_good, good, good_lab), shift=0.3 * LEFT), run_time=0.9)

    # cmp.3: arrays jump to a slot; lists are walked from the front
    def arrays_vs_lists(self):
        ARR_A, ARR_B, LIST_Y = 0.45, 2.25, -1.6      # array row: alone, then above the list
        arr_lab = T("array", size=44)
        lab_w = arr_lab.width
        span = lab_w + 0.4 + 8 * SLOT + 2.4          # label, 8 slots, gap and slot 12
        X0 = -span / 2 + lab_w + 0.4                 # left edge of the array (and the chain)

        slots = VGroup()
        for v in (3, 5, 9, 2, 10, 4, 7, 1):
            sq = Square(SLOT, stroke_color=BLUE, stroke_width=3)
            slots.add(VGroup(sq, value_label(v, size=44).move_to(sq)))
        slots.arrange(RIGHT, buff=0).move_to([X0, ARR_A, 0], aligned_edge=LEFT)
        idx = VGroup(*[T(str(i), size=34, color=DIM).next_to(s, DOWN, buff=0.18)
                       for i, s in enumerate(slots)])
        arr_lab.next_to(slots, LEFT, buff=0.4)
        array = VGroup(arr_lab, slots, idx)

        # slot 12 of an 8-slot array: past the end (the gap is drawn as dots, not to scale)
        ghost_sq = DashedVMobject(Square(SLOT, stroke_color=RED, stroke_width=3), num_dashes=16)
        ghost_sq.move_to([slots.get_right()[0] + 1.9, ARR_A, 0])
        dots = VGroup(*[Dot(radius=0.055, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.17)
        dots.move_to([(slots.get_right()[0] + ghost_sq.get_left()[0]) / 2, ARR_A, 0])
        ghost_idx = T("12", size=34, color=RED).next_to(ghost_sq, DOWN, buff=0.18)
        ghost_idx.align_to(idx[0], DOWN)
        ghost_q = T("?", size=48, color=RED).move_to(ghost_sq)
        oob = T("out of bounds!", size=40, color=RED).next_to(ghost_idx, DOWN, buff=0.4)
        oob.set_x(min(ghost_sq.get_x(), 6.5 - oob.width / 2))
        ghost = VGroup(dots, ghost_sq, ghost_idx)

        chain = VGroup(*[box(value_label(v, size=48), CELL_L, CELL_L) for v in (3, 5, 9, 2, 10)])
        chain.arrange(RIGHT, buff=0.8).move_to([X0, LIST_Y, 0], aligned_edge=LEFT)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, stroke_width=4, color=FG,
                                max_tip_length_to_length_ratio=0.35, tip_length=0.2)
                          for a, b in zip(chain[:-1], chain[1:])])
        list_lab = T("list", size=44).next_to(chain, LEFT, buff=0.4)
        list_lab.align_to(arr_lab, RIGHT)

        with self.say("c1.cmp.3") as c:
            # the [1; 2] fix stays up until the array needs the space
            c.wait_until("jump straight")
            self.sweep_clear(time_span(FadeIn(arr_lab, shift=0.3 * DOWN), 0.5, 1.5),
                             time_span(LaggedStart(*[FadeIn(VGroup(s, i), shift=0.3 * DOWN)
                                                     for s, i in zip(slots, idx)], lag_ratio=0.1), 0.5, 1.5),
                             run_time=1.5)

            m = marker().move_to(above(slots[0]))
            self.play(FadeIn(m, shift=0.3 * DOWN), run_time=c.until("give me", floor=0.4) * 0.8)

            # "give me element number five": one hop, then a spotlight on slot 5 (P6, P9)
            c.wait_until("give me")
            self.play(MoveAlongPath(m, ArcBetweenPoints(m.get_center(), above(slots[5]), angle=-PI / 2.5)),
                      run_time=1.0)
            others = [s for i, s in enumerate(slots) if i != 5] + [g for i, g in enumerate(idx) if i != 5]
            self.play(FlashAround(slots[5], color=YELLOW, buff=0.06),
                      slots[5][0].animate.set_stroke(YELLOW, width=6), idx[5].animate.set_color(YELLOW),
                      *set_alpha(others, DIMMED), run_time=1.0)

            # a slot that doesn't exist
            c.wait_until("ask for")
            self.play(MoveAlongPath(m, ArcBetweenPoints(m.get_center(), above(ghost_sq), angle=-PI / 2.5)),
                      slots[5][0].animate.set_stroke(BLUE, width=3), idx[5].animate.set_color(DIM),
                      *set_alpha(others, 1), time_span(FadeIn(ghost), 0.5, 1.5), run_time=1.5)

            c.wait_until("things go wrong")
            self.play(m.animate.set_color(RED), FlashAround(ghost_sq, color=RED, buff=0.06),
                      FadeIn(VGroup(ghost_q, oob), shift=0.3 * DOWN), run_time=1.0)

            # {walk}: the array steps back (dimmed, above) and the list arrives
            c.wait_until("walk")
            self.play(FadeOut(m),
                      restyle(VGroup(array, ghost, ghost_q, oob), 0.3, shift=UP * (ARR_B - ARR_A)),
                      FadeIn(VGroup(list_lab, chain, arrows), shift=0.3 * UP), run_time=1.5)

            c.wait_until("don't jump")
            nope = DashedVMobject(ArcBetweenPoints(above(chain[0]), above(chain[2]), angle=-PI / 2,
                                                   color=DIM, stroke_width=3), num_dashes=16)
            x = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(RED, 7).scale(0.2).move_to(above(chain[2]))
            self.play(Create(nope), time_span(FadeIn(x, scale=1.4), 0.8, 1.2), run_time=1.2)

            # walk it: a cursor on the current box, the others faded (PATTERNS §3)
            c.wait_until("start at the front")
            w = marker().move_to(above(chain[0]))
            self.play(FadeOut(VGroup(nope, x)), FadeIn(w, shift=0.3 * DOWN),
                      restyle(chain[0], outline=YELLOW, width=6),
                      *set_alpha([*chain[1:], *arrows], DIMMED), run_time=1.0)

            c.wait_until("work your way")
            step = lambda t: smooth(min(1.0, t / 0.7))  # noqa: E731  move, then rest
            for i in range(1, len(chain)):  # each step costs the same screen time
                self.play(w.animate(rate_func=step).move_to(above(chain[i])),
                          restyle(chain[i - 1], DIMMED, outline=BLUE, width=3),
                          restyle(arrows[i - 1], 1, outline=YELLOW, fill=YELLOW),
                          restyle(chain[i], 1, outline=YELLOW, width=6), run_time=1.0, rate_func=step)

            c.wait_until("recursion")
            self.play(*set_alpha(chain[:-1], 1), run_time=1.0)

    # cmp.4: @ and List.rev come for free
    def free_tools(self):
        X0 = -4.6
        app = Code("[3; 5; 9] @ [2; 10]", size=52).move_to([X0, 2.45, 0], aligned_edge=LEFT)
        app.find("@").set_color(YELLOW)
        app_res = Code("[3; 5; 9; 2; 10]", size=52).move_to([X0, 1.1, 0], aligned_edge=LEFT)
        arrow1 = Mono("⇒", size=80).next_to(app_res, LEFT, buff=0.35)
        u1 = underline(app.find("[3; 5; 9]"), BLUE)
        u2 = underline(app.find("[2; 10]"), PURPLE)
        r1 = underline(app_res.find("3; 5; 9"), BLUE)
        r2 = underline(app_res.find("2; 10"), PURPLE)

        rev = Code("List.rev [3; 5; 9]", size=52).move_to([X0, -0.85, 0], aligned_edge=LEFT)
        rev.find("List.rev").set_color(YELLOW)
        rev_res = Code("[9; 5; 3]", size=52)
        rev_res.move_to(rev.find("[3; 5; 9]")).shift(DOWN * 1.35)
        arrow2 = Mono("⇒", size=80).next_to(rev_res, LEFT, buff=0.35)

        def dashed_box(mob):
            return DashedVMobject(SurroundingRectangle(mob, color=YELLOW, buff=0.14, stroke_width=3),
                                  num_dashes=28)

        with self.say("c1.cmp.4", gap=0.6) as c:  # a little extra hold on the final picture
            c.wait_until("append")
            self.sweep_clear(time_span(FadeIn(app, shift=0.3 * DOWN), 0.5, 1.3), run_time=1.3)
            self.play(FlashAround(app.find("@"), color=YELLOW, time_width=1.5), run_time=1.0)

            c.wait_until("three five nine")
            self.play(Create(u1), run_time=0.8)
            c.wait_until("two and ten")
            self.play(Create(u2), run_time=0.8)

            # "gives": the result is born from copies of the two lists (P5)
            c.wait_until("gives")
            part1 = [VGroup(*app.find("3; 5; 9"), u1), VGroup(*app_res.find("3; 5; 9"), r1)]
            part2 = [VGroup(*app.find("2; 10"), u2), VGroup(*app_res.find("2; 10"), r2)]
            rest = VGroup(arrow1, app_res.find("["), app_res.find("]"), app_res.find(";", nth=2))
            self.play(TransformFromCopy(*part1), TransformFromCopy(*part2), FadeIn(rest), run_time=1.8)
            self.remove(part1[1], part2[1], rest)
            self.add(arrow1, app_res, r1, r2)

            # {rev}: the append lines step back (P9) for the new one
            c.wait_until("rev")
            done = [app, app_res, arrow1, u1, u2, r1, r2]
            self.play(*set_alpha(done, 0.35), FadeIn(rev, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("reverses")
            # copies of 3, 5, 9 drop straight down, then 3 and 9 trade ends (9 over the
            # top, 3 underneath); the brackets only arrive with the swap, so no frame
            # ever reads as "=> [3; 5; 9]"
            spots = [rev_res.find(d)[0].get_center() for d in "953"]
            drops = [rev.find(d)[0].copy() for d in "359"]
            frame = VGroup(arrow2, rev_res.find("["), rev_res.find("]"),
                           *[g for k in range(2) for g in rev_res.find(";", nth=k)])
            self.play(*[d.animate.move_to(p) for d, p in zip(drops, spots)], run_time=0.8)
            self.play(drops[0].animate(path_arc=PI / 2).move_to(spots[2]),
                      drops[2].animate(path_arc=PI / 2).move_to(spots[0]), FadeIn(frame), run_time=1.0)
            self.remove(*drops, frame)
            self.add(arrow2, rev_res)

            # {later}: "we'll build both ... and find out how much they really cost":
            # both back in full with their cost in question, then boxed as blueprints
            c.wait_until("later")
            costs = VGroup(T("cost?", size=44, color=GOLD).next_to(app, RIGHT, buff=0.7),
                           T("cost?", size=44, color=GOLD).next_to(rev, RIGHT, buff=0.7))
            costs[1].align_to(costs[0], LEFT)
            self.play(*set_alpha(done, 1), FadeIn(costs, shift=0.3 * LEFT), run_time=0.6)
            c.wait_until("build both")
            self.play(Create(dashed_box(app.find("@"))), Create(dashed_box(rev.find("List.rev"))),
                      run_time=1.2)
