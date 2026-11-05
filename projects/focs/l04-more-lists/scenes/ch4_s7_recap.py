"""Chapter 4, scene 7: the recap of making change (five lines, each with a small icon from the
chapter on its left) and the end card with ch5's teaser (the stuck trace's first call becomes the
node "6, [5; 2]", and the outline of a tree of choices grows from it). Clips c4.recap.1 – c4.recap.2
(the chapter's last scene).

Layout, sizes and the 8 s end-card hold follow ch2_s7_recap: title y 3.25, icon column centred at
x -5.05 (3.0 wide; code icons left-aligned at its left edge), text column from x -3.15 at size 34,
a said line steps back to 0.5. Icons are rebuilt small here (no imports from other scenes):
s2's till chain (its till_chain: a GOLD coin per cell, nil TEAL; shortened to
50 -> 20 -> 10 -> ... -> [] so the coins read at icon size), the clause patterns of s3's code, s4's base
case, s6's stuck trace in RED.

End card (for ch5's builder): header "Next: every way to make change" (size 40, DIM + YELLOW) at
y 3.05; root node Mono 40 "6, [5; 2]" (6 GOLD, [5; 2] TEAL) in a BLUE rounded box 3.5 x 0.85 at
(0, 1.75); GOLD "?" right of it; edges "use 5" (left) and "skip 5" (right) to empty BLUE outlines
at (±2.8, 0.05); then two more levels of DIM outline, one tip a RED dead end.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, TransformMatchingStrings, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TILL = [50, 20, 10, 5, 2, 1]
CLAUSES = ("| _, 0         ->", "| [], _        ->", "| c::till, amt ->")
TRACE = ("change [5; 2] 6", "⇒ 5 :: change [5; 2] 1", "⇒ 5 :: change [2] 1", "⇒ 5 :: change [] 1")

# ── layout (ch2_s7_recap's grid) ────────────────────────────────────────────────
TITLE_Y = 3.25
ICON_X, ICON_W = -5.05, 3.0         # icon column: centre and widest icon
ICON_L = ICON_X - ICON_W / 2        # code icons start here
TEXT_X = -3.15                      # left edge of every line's text
TEXT_SIZE, ICON_CODE, TRACE_SIZE = 34, 22, 15
R1_Y = 2.35
R2_Y = (1.55, 1.0, 0.45)            # the three clauses
R3_Y = (-0.35, -0.9)                # the constant, the coin put back
R4_Y = -1.7
R5_Y = (-2.55, -3.1)                # "greedy can get stuck", then 2 + 2 + 2 = 6
SAID = 0.5                          # a line that has been said steps back to this
END_CARD = 8.0

# ── the teaser's tree ───────────────────────────────────────────────────────────
NEXT_Y, ROOT_Y = 3.05, 1.75
LEVEL_Y = (0.05, -1.6, -3.0)
LEVEL_DX = (2.8, 1.4, 0.65)
DEAD_TIP = 1                        # the tip that turns out a dead end

COIN_R = 0.42                       # the coin disc of ch4-ch7 (scenes/ch1_s1_hook.py)
COIN_LABEL = 34
TILL_S = 0.85                       # s2's till chain scale


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def multiply_opacity(mob, k):
    """Scale every part's opacity by k in place (keeps the dims inside an icon)."""
    for leaf in mob.family_members_with_points():
        leaf.set_fill(opacity=leaf.get_fill_opacity() * k, family=False)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * k, family=False)
    return mob


def faded(mob, k):
    return multiply_opacity(mob.copy(), k)


def line_at(parts, y):
    """Parts in a row, left edge on the text column, centred on y."""
    grp = VGroup(*parts).arrange(RIGHT, buff=0.22)
    grp.move_to([TEXT_X, y, 0], aligned_edge=LEFT)
    return grp


def code_icon(src, y, size=ICON_CODE):
    return Code(src, size=size).move_to([ICON_L, y, 0], aligned_edge=LEFT)


# ── icons ───────────────────────────────────────────────────────────────────────
def till_chain(values, scale=TILL_S):
    """The till: ConsChain(values) scaled `scale`; each cell's label is coin(v, r=COIN_R*scale)
    (the value stays size 34). Nil TEAL as in ConsChain. Centred on ORIGIN. (From ch4_s2_idea.)"""
    chain = ConsChain(values).scale(scale)
    for cell in chain.cells:
        cell.remove(cell.label)
        cell.label = coin(cell.value, r=COIN_R * scale).move_to(cell.box)
        cell.add(cell.label)
    return chain


def till_icon():
    """s2's till, shortened to read at icon size: 50 -> 20 -> 10 -> ... -> []."""
    ch = till_chain(TILL[:3])
    last, nil = ch.cells[-1], ch.nil
    ch.remove(ch.arrows[-1])
    y = last.box.get_y()
    hop = LINK * TILL_S * 0.7                   # each half of the elided link
    x0 = last.ptr.get_right()[0]
    dots = T("…", size=42, color=FG).scale(TILL_S).move_to([x0 + hop + 0.12, y, 0], aligned_edge=LEFT)
    nil.move_to([dots.get_right()[0] + 0.12 + hop, y, 0], aligned_edge=LEFT)

    def arrow(p, q):
        return Arrow(p, q, buff=0, stroke_width=3, color=FG, max_tip_length_to_length_ratio=0.3,
                     tip_length=0.16 * TILL_S)

    a1 = arrow(last.tail_start(), [x0 + hop, y, 0])
    a2 = arrow([dots.get_right()[0] + 0.12, y, 0], nil.entry())
    ch.add(a1, dots, a2)
    ch.scale(ICON_W / ch.width).move_to([ICON_X, R1_Y, 0])
    return ch


def trace_icon():
    """s6's stuck trace, in RED, four rows left-aligned."""
    rows = VGroup(*[Mono(s, size=TRACE_SIZE, color=RED) for s in TRACE])
    rows.arrange(DOWN, buff=0.13, aligned_edge=LEFT)
    rows.move_to([ICON_L, (R5_Y[0] + R5_Y[1]) / 2, 0], aligned_edge=LEFT)
    return rows


# ── the teaser's tree ───────────────────────────────────────────────────────────
def outline(w, h, op):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(BLUE, 3, opacity=op)


def edge(a, b, color=DIM, width=3):
    return Line(a, b, buff=0).set_stroke(color, width)


class ChangeRecap(NarratedScene):
    def construct(self):
        self.recap()
        self.teaser()
        # End card: the tree and its header hold, fully visible, under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.3)
        self.wait(0.15)

    # ── recap.1: five lines, one per mark ──────────────────────────────────────────
    def recap(self):
        self.title = title = T("Recap", size=48).move_to([0, TITLE_Y, 0])

        i1 = till_icon()
        l1 = line_at([T("Descending till: largest coin at the head", size=TEXT_SIZE,
                        t2c={"head": YELLOW})], R1_Y)
        row1 = VGroup(i1, *l1)

        pats = [code_icon(s, y) for s, y in zip(CLAUSES, R2_Y)]
        tag_ok = line_at([T("success", size=TEXT_SIZE, color=GREEN)], R2_Y[0])
        tag_fail = line_at([T("failure", size=TEXT_SIZE, color=RED)], R2_Y[1])
        tag_use = line_at([T("use it if it fits,", size=TEXT_SIZE), T("else skip", size=TEXT_SIZE)],
                          R2_Y[2])
        row2 = VGroup(*pats, *tag_ok, *tag_fail, *tag_use)

        i3a = code_icon("| _, 0", R3_Y[0])
        i3b = code_icon("change (c::till)", R3_Y[1])
        VGroup(*i3b.find("change")).set_color(FG)
        VGroup(*i3b.find("(c::till)")).set_color(YELLOW)
        l3a = line_at([T("A constant matches only that value", size=TEXT_SIZE)], R3_Y[0])
        l3b = line_at([T("Putting the coin back lets it be reused", size=TEXT_SIZE)], R3_Y[1])
        row3 = VGroup(i3a, i3b, *l3a, *l3b)

        i4 = code_icon("| _, 0 -> []", R4_Y)
        l4 = line_at([T("Base case does nothing:", size=TEXT_SIZE), T("keeps it simple", size=TEXT_SIZE)],
                     R4_Y)
        row4 = VGroup(i4, *l4)

        self.trace = i5 = trace_icon()
        l5a = line_at([T("Greedy, largest first, can get stuck", size=TEXT_SIZE)], R5_Y[0])
        l5b = line_at([Mono("2 + 2 + 2 = 6", size=TEXT_SIZE, color=GREEN),
                       T("even when change exists", size=TEXT_SIZE)], R5_Y[1])
        row5 = VGroup(i5, *l5a, *l5b)
        self.rows = [row1, row2, row3, row4, row5]

        up = 0.25 * UP
        side = 0.3 * LEFT                       # tags drop toward their clause
        with self.say("c4.recap.1") as c:
            # "Let's recap."
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=min(1.0, c.until("r1")))

            # "The till is a list in descending order, so the largest coin is its head."
            c.wait_until("r1")
            self.play(FadeIn(i1, shift=up), FadeIn(l1[0], shift=up), run_time=1.2)
            c.wait_until("largest coin")
            head = i1.cells[0]
            self.play(head.box.animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.35),
                      FlashAround(head.box, color=YELLOW, time_width=1.5, buff=0.06), run_time=1.2)
            settle(self, row1)

            # "Change has three clauses, success at zero, an exception when the till runs out,
            # and for the first coin, use it if it fits, or skip it if it's too large."
            c.wait_until("r2")
            self.play(Transform(row1, faded(row1, SAID)),
                      LaggedStart(*[FadeIn(p, shift=up) for p in pats], lag_ratio=0.25), run_time=1.4)
            c.wait_until("success")
            self.play(FadeIn(tag_ok[0], shift=side), run_time=0.9)
            c.wait_until("an exception")
            self.play(FadeIn(tag_fail[0], shift=side), run_time=0.9)
            c.wait_until("use it if it fits")
            self.play(FadeIn(tag_use[0], shift=side), run_time=0.9)
            c.wait_until("or skip it")
            self.play(FadeIn(tag_use[1], shift=side), run_time=0.9)
            settle(self, row2)

            # "A constant in a pattern matches only that value, and putting the coin back lets it
            # be used again."
            c.wait_until("r3")
            self.play(Transform(row2, faded(row2, SAID)), FadeIn(i3a, shift=up), FadeIn(l3a[0], shift=up),
                      run_time=1.3)
            c.wait_until("only that value")
            self.play(FlashAround(VGroup(*i3a.find("0")), color=GOLD, time_width=1.5), run_time=1.1)
            c.wait_until("putting the coin back")
            self.play(FadeIn(i3b, shift=up), FadeIn(l3b[0], shift=up), run_time=1.2)
            settle(self, row3)

            # "The base case does nothing, which keeps the program simple."
            c.wait_until("r4")
            self.play(Transform(row3, faded(row3, SAID)), FadeIn(i4, shift=up), FadeIn(l4[0], shift=up),
                      run_time=1.2)
            c.wait_until("keeps the program simple")
            self.play(FadeIn(l4[1], shift=up), run_time=0.9)
            settle(self, row4)

            # "And greedy, largest first, can get stuck even when change exists."
            c.wait_until("r5")
            self.play(Transform(row4, faded(row4, SAID)), FadeIn(l5a[0], shift=up),
                      LaggedStart(*[FadeIn(r, shift=up) for r in i5], lag_ratio=0.3), run_time=1.5)
            c.wait_until("even when")
            self.play(FadeIn(l5b[0], shift=up), FadeIn(l5b[1], shift=up), run_time=1.0)
            settle(self, row5)

    # ── recap.2: the teaser, ch5's tree of choices ─────────────────────────────────
    def teaser(self):
        header = VGroup(T("Next:", size=40, color=DIM), T("every way to make change", size=40, color=YELLOW))
        header.arrange(RIGHT, buff=0.25)
        header[0].align_to(header[1], UP)
        header.move_to([0, NEXT_Y, 0])

        label = Mono("6, [5; 2]", size=40, t2c={"6": GOLD, "[5; 2]": TEAL})
        box = RoundedRectangle(corner_radius=0.15, width=3.5, height=0.85).set_stroke(BLUE, 3)
        box.move_to([0, ROOT_Y, 0])
        label.move_to(box)
        q = T("?", size=56, color=GOLD).next_to(box, RIGHT, buff=0.4)

        # level 1: "use 5" to the left, "skip 5" to the right, each to an empty node outline
        kids, e1, tags = [], [], []
        for sgn, word in ((-1, "use 5"), (1, "skip 5")):
            kid = outline(1.6, 0.6, 0.7).move_to([sgn * LEVEL_DX[0], LEVEL_Y[0], 0])
            e = edge(box.get_bottom() + RIGHT * sgn * 0.9, kid.get_top(), color=FG, width=4)
            tag = T(word, size=32, t2c={"5": GOLD})
            tag.next_to(e.point_from_proportion(0.6), RIGHT if sgn > 0 else LEFT, buff=0.4).shift(0.12 * UP)
            kids.append(kid)
            e1.append(e)
            tags.append(tag)

        # levels 2 and 3: the outline fans out
        grand, e2, tips, e3 = [], [], [], []
        for kid in kids:
            for sgn in (-1, 1):
                g = outline(1.1, 0.45, 0.5).move_to([kid.get_x() + sgn * LEVEL_DX[1], LEVEL_Y[1], 0])
                e2.append(edge(kid.get_bottom(), g.get_top()))
                grand.append(g)
        for g in grand:
            for sgn in (-1, 1):
                tip = Dot([g.get_x() + sgn * LEVEL_DX[2], LEVEL_Y[2], 0], radius=0.09, color=DIM)
                e3.append(edge(g.get_bottom(), tip.get_center()))
                tips.append(tip)
        dead = cross_mark(RED).move_to(tips[DEAD_TIP])

        recap, row5 = [self.title, *self.rows[:4]], self.rows[4]
        src = self.trace[0]
        self.trace.remove(src)                  # the stuck call leaves its trace (and row 5) ...
        self.add(src)
        with self.say("c4.recap.2") as c:
            # "Next time, instead of one answer, ..." The recap sweeps away, all but greedy's
            # line; then its stuck call becomes the first node of next time's tree.
            self.play(LaggedStart(*[FadeOut(m) for m in recap], lag_ratio=0.1),
                      time_span(FadeIn(header[0], shift=0.3 * DOWN), 0.3, 1.0), run_time=1.0)
            self.play(TransformMatchingStrings(src, label, matched_keys=("[5; 2]", "6")),
                      time_span(Create(box), 0.6, 1.4), time_span(FadeIn(q, scale=0.6), 1.2, 1.7),
                      run_time=1.7)

            # "... we'll find every way to make change."
            c.wait_until("every way")
            t = max(1.2, min(1.6, c.until("paths") - 0.2))
            self.play(time_span(FadeIn(header[1], shift=0.3 * DOWN), 0, 0.6 * t),
                      *[time_span(Create(e), 0.15 * t, 0.65 * t) for e in e1],
                      *[time_span(FadeIn(k), 0.5 * t, 0.85 * t) for k in kids],
                      *[time_span(FadeIn(g, shift=0.2 * DOWN), 0.6 * t, t) for g in tags], run_time=t)

            # "Then a dead end is just one path among many."
            c.wait_until("paths")
            # Greedy's stuck line clears as the tree fans out into its space.
            t = max(1.2, min(1.8, c.until("one path") - 0.1))
            self.play(time_span(FadeOut(row5), 0, 0.4 * t),
                      *[time_span(Create(e), 0.15 * t, 0.55 * t) for e in e2],
                      *[time_span(FadeIn(g), 0.35 * t, 0.65 * t) for g in grand],
                      *[time_span(Create(e), 0.55 * t, 0.9 * t) for e in e3],
                      *[time_span(FadeIn(d), 0.75 * t, t) for d in tips], run_time=t)
            c.wait_until("one path")
            self.play(e3[DEAD_TIP].animate.set_stroke(RED), ReplacementTransform(tips[DEAD_TIP], dead),
                      run_time=1.0)
