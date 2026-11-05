"""Chapter 5, scene 7: the recap of every way to make change (the notes' "challenges" quote card,
a small case traced by hand, four recap lines with icons) and the end card with ch6's teaser
(In [72] small, `allc` and `@` GOLD as "copies", YELLOW "accumulators?"). Clips c5.recap.1 –
c5.recap.2 (the chapter's last scene).

Layout follows ch4_s7_recap: title y 3.25, icon column centred at x -5.05 (3.0 wide), text column
from x -3.15 at size 34, a said line steps back to 0.5, 8 s end card under the music. Icons are
rebuilt small from the chapter looks (coin = ch1's coin; solution = coins x0.6 in a TEAL box; list
of solutions = solution boxes in a bigger TEAL box): s2's box of boxes with `int list list`, s2's
`[[]]` beside `[]`, s3's use / skip fork from "6, [5; 2]", s5's 2 disc onto each of [2], [1; 1].

End card: header "Next:" (DIM) "faster, and exercises" (YELLOW) size 40 at y 3.2; In [72] as Code
size 22, centred at x 0 with its top at y 2.6; the `allc` call and the `@` of its 10th line GOLD,
each with a GOLD "copies" (size 32) under it; YELLOW "accumulators?" (size 44) at (2.6, -3.25).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the notes' words (p. 35) and In [72] (p. 34), verbatim ───────────────────────
QUOTE = ("“This complicated program, and the even",
         "trickier one in the next section, are",
         "included as challenges.”")
LATER = "making change returns, with exceptions, in a later lecture"
IN72 = """let rec change till amt =
  match till, amt with
  | _       , 0   -> [ [] ]
  | []      , _   -> []
  | c::till , amt -> if amt < c then change till amt
                    else let rec allc = function
                           | [] -> []
                           | cs :: css -> (c::cs) :: allc css
                         in
                           allc (change (c::till) (amt - c)) @
                                 change till amt"""
CALL_LINE = 9                       # "allc (change (c::till) (amt - c)) @"

# ── layout (ch4_s7_recap's grid) ────────────────────────────────────────────────
TITLE_Y = 3.25
ICON_X, ICON_W = -5.05, 3.0
TEXT_X = -3.15
TEXT_SIZE = 34
SAID = 0.5
END_CARD = 8.0

R1_Y, R1_ICON_Y, R1_TYPE_Y = 2.05, 2.22, 1.5
R2_Y, R2_ICON_Y = (0.8, 0.2), 0.5
R3_Y, R3_ROOT_Y, R3_TIP_Y = (-0.72, -1.32), -0.56, -1.38
R4_Y, R4_BOX_Y, R4_DISC_Y = (-2.38, -2.98), -2.88, -2.06
ICON_K = 0.77                       # solution-box icons (rows 1 and 4)
EMPTY_K = 0.5                       # row 2's [[]] and []
ICON_TEXT = 26                      # Mono labels inside icons

# clip 1
QUOTE_SIZE, QUOTE_Y = 40, 0.25
QUOTE_UP_Y, QUOTE_UP_K = 2.3, 0.85
TREE_ROOT_Y, TREE_KID_Y, TREE_DX = 0.3, -1.35, 2.7
LATER_Y = -2.85

# end card
NEXT_Y, CODE_TOP, CODE_SIZE = 3.2, 2.6, 22
COPIES_Y = -2.45
ACC_POS = (2.6, -3.25)

COIN_R = 0.42                       # the coin disc of ch4-ch7 (scenes/ch1_s1_hook.py)
COIN_LABEL = 34
SOL_COIN = 0.6                      # a coin inside a solution box


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


class Sol(VGroup):
    """One solution: coins x0.6 in a row (buff 0.1) in a TEAL box (corner 0.1, stroke 3,
    padding 0.12); empty = that box as a coin-height square."""

    def __init__(self, values):
        coins = [coin(v).scale(SOL_COIN) for v in values]
        side = 2 * COIN_R * SOL_COIN + 2 * 0.12
        row = VGroup(*coins).arrange(RIGHT, buff=0.1) if coins else None
        w = row.width + 2 * 0.12 if coins else side
        box = RoundedRectangle(corner_radius=0.1, width=w, height=side).set_stroke(TEAL, 3)
        if coins:
            row.move_to(box)
        super().__init__(box, *coins)
        self.box, self.coins = box, coins


class Sols(VGroup):
    """A list of solutions: solution boxes in a row (buff 0.2) in a bigger TEAL box (corner
    0.15, stroke 4, padding 0.2); [] = the big box empty."""

    def __init__(self, sols):
        items = [Sol(s) for s in sols]
        if items:
            row = VGroup(*items).arrange(RIGHT, buff=0.2)
            w, h = row.width + 0.4, row.height + 0.4
        else:
            h = Sol([]).height + 0.4
            w = h
        big = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(TEAL, 4)
        if items:
            row.move_to(big)
        super().__init__(big, *items)
        self.big, self.sols = big, items


def node(amount, till, size=32, pad=(0.5, 0.36)):
    """A tree node: Mono "amount, till" (amount GOLD, till TEAL) in a BLUE rounded box."""
    lab = Mono(f"{amount}, {till}", size=size)
    n = len(str(amount))
    lab[:n].set_color(GOLD)
    lab[n + 1:].set_color(TEAL)
    box = RoundedRectangle(corner_radius=0.15, width=lab.width + pad[0],
                           height=lab.height + pad[1]).set_stroke(BLUE, 3)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.lab = box, lab
    return g


def edge(a, b, width=4):
    return Line(a, b, buff=0).set_stroke(FG, width)


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


def sols_icon(sols, y):
    return Sols(sols).scale(ICON_K).move_to([ICON_X, y, 0])


class AllWaysRecap(NarratedScene):
    def construct(self):
        self.challenge()
        self.recap()
        # End card: In [72], its copies and the question hold, fully visible, under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.3)
        self.wait(0.15)

    # ── recap.1: the quote card, a small case by hand, the later lecture ─────────────
    def challenge(self):
        lines = VGroup(*[T(s, size=QUOTE_SIZE, slant=ITALIC, t2c={"challenges": YELLOW}) for s in QUOTE])
        lines.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        bar = Line(lines.get_corner(UL) + 0.4 * LEFT + 0.05 * UP, lines.get_corner(DL) + 0.4 * LEFT
                   + 0.05 * DOWN).set_stroke(DIM, 4)
        src = T("FoCS notes, p. 35", size=36, color=DIM)
        src.next_to(lines, DOWN, buff=0.4).align_to(lines, RIGHT)
        quote = VGroup(bar, lines, src).move_to([0, QUOTE_Y, 0])
        challenges = select(lines[2], "challenges")[0]
        trickier = select(lines[1], "trickier one in the next section")[0]

        root = node(4, "[2; 1]").move_to([0, TREE_ROOT_Y, 0])
        kids, edges, tags = [], [], []
        for sgn, (amt, till), word in ((-1, (2, "[2; 1]"), "use 2"), (1, (4, "[1]"), "skip 2")):
            kid = node(amt, till).move_to([sgn * TREE_DX, TREE_KID_Y, 0])
            e = edge(root.box.get_bottom() + RIGHT * sgn * 0.8, kid.box.get_top())
            tag = T(word, size=30, t2c={"2": GOLD})
            tag.next_to(e.get_center(), RIGHT if sgn > 0 else LEFT, buff=0.35).shift(0.1 * UP)
            kids.append(kid)
            edges.append(e)
            tags.append(tag)
        self.later = later = T(LATER, size=32, color=DIM).move_to([0, LATER_Y, 0])

        up = 0.25 * UP
        with self.say("c5.recap.1") as c:
            # "The notes call this program a challenge, ..."
            self.play(GrowFromCenter(bar),
                      LaggedStart(*[FadeIn(ln, shift=up) for ln in lines], lag_ratio=0.25),
                      time_span(FadeIn(src), 0.9, 1.5), run_time=1.5)
            c.wait_until("a challenge")
            self.play(FlashUnder(challenges, color=YELLOW), run_time=1.2)
            # "... and they promise an even trickier one next."
            c.wait_until("trickier")
            self.play(FlashUnder(trickier, color=YELLOW), run_time=1.3)

            # "If it took you a couple of passes, that's normal."
            c.wait_until("normal")
            self.play(quote.animate.scale(QUOTE_UP_K).move_to([0, QUOTE_UP_Y, 0]), run_time=1.3)

            # "Trace a small case by hand, and it gets much clearer."
            c.wait_until("Trace a small case")
            self.play(FadeIn(root, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("by hand")
            self.play(*[Create(e) for e in edges],
                      *[time_span(FadeIn(k, shift=0.2 * DOWN), 0.5, 1.6) for k in kids],
                      *[time_span(FadeIn(t, shift=0.2 * DOWN), 0.6, 1.6) for t in tags], run_time=1.6)

            # "We'll come back to making change in a later lecture, when we study exceptions."
            c.wait_until("later")
            self.play(FadeIn(later, shift=0.2 * UP), run_time=1.0)

    # ── recap.2: four lines, one per mark ──────────────────────────────────────────
    def recap(self):
        self.title = title = T("Recap", size=48).move_to([0, TITLE_Y, 0])

        # r1: a list of solutions, each an int list
        i1 = sols_icon([[2], [1, 1]], R1_ICON_Y)
        ty1 = Mono("int list list", size=ICON_TEXT, color=GREEN).move_to([ICON_X, R1_TYPE_Y, 0])
        l1 = line_at([T("A list of solutions,", size=TEXT_SIZE),
                      T("each an int list", size=TEXT_SIZE, t2c={"int list": GREEN})], R1_Y)
        row1 = VGroup(i1, ty1, *l1)

        # r2: [[]] beside []
        i2a = Sols([[]]).scale(EMPTY_K)
        m2a = Mono("[[]]", size=ICON_TEXT, color=TEAL).next_to(i2a, RIGHT, buff=0.16)
        i2b = Sols([]).scale(EMPTY_K).next_to(m2a, RIGHT, buff=0.36)
        m2b = Mono("[]", size=ICON_TEXT, color=TEAL).next_to(i2b, RIGHT, buff=0.16)
        VGroup(i2a, m2a, i2b, m2b).move_to([ICON_X, R2_ICON_Y, 0])
        l2a = line_at([T("Zero: exactly one solution, no coins", size=TEXT_SIZE,
                         t2c={"Zero": GOLD, "one solution": GREEN})], R2_Y[0])
        l2b = line_at([T("Empty till, money owed: none", size=TEXT_SIZE, t2c={"none": RED})], R2_Y[1])
        row2 = VGroup(i2a, m2a, i2b, m2b, *l2a, *l2b)

        # r3: the use / skip fork, joined by @
        root = node(6, "[5; 2]", size=ICON_TEXT - 2, pad=(0.3, 0.22)).move_to([ICON_X, R3_ROOT_Y, 0])
        forks, tips = [], []
        for sgn, word in ((-1, "use 5"), (1, "skip 5")):
            end = np.array([ICON_X + sgn * 1.0, R3_TIP_Y + 0.22, 0])
            forks.append(edge(root.box.get_bottom() + RIGHT * sgn * 0.45, end, width=3))
            tips.append(T(word, size=26, t2c={"5": GOLD}).move_to([end[0], R3_TIP_Y, 0]))
        at = Mono("@", size=30, color=GOLD).move_to([ICON_X, R3_TIP_Y, 0])
        l3a = line_at([T("Two sources: use the coin, or skip it", size=TEXT_SIZE)], R3_Y[0])
        l3b = line_at([Mono("@", size=TEXT_SIZE, color=GOLD), T("joins them", size=TEXT_SIZE)], R3_Y[1])
        row3 = VGroup(root, *forks, *tips, at, *l3a, *l3b)

        # r4: the 2 disc onto the front of each box
        before = sols_icon([[2], [1, 1]], R4_BOX_Y)
        mid = sols_icon([[2, 2], [1, 1]], R4_BOX_Y)
        after = sols_icon([[2, 2], [2, 1, 1]], R4_BOX_Y)
        disc = coin(2).scale(SOL_COIN * ICON_K).move_to([ICON_X, R4_DISC_Y, 0])
        l4a = line_at([T("Local", size=TEXT_SIZE), Mono("allc", size=TEXT_SIZE, color=YELLOW),
                       T("puts the coin on the front", size=TEXT_SIZE)], R4_Y[0])
        l4b = line_at([T("of every use-branch solution", size=TEXT_SIZE)], R4_Y[1])

        up = 0.25 * UP
        with self.say("c5.recap.2") as c:
            # "Let's recap."  The quote and the tree sweep away; the later-lecture note stays a while.
            sweep_clear(self, time_span(FadeIn(title, shift=0.3 * DOWN), 0.4, 1.2), keep=[self.later],
                        run_time=min(1.2, c.until("r1")))

            # "We return every way as a list of solutions, ..."
            c.wait_until("r1")
            self.play(FadeIn(i1, shift=up), FadeIn(ty1, shift=up), FadeIn(l1[0], shift=up), run_time=1.2)
            # "... where each solution is an int list."
            c.wait_until("each solution")
            self.play(*[FlashAround(s.box, color=TEAL, time_width=1.5, buff=0.05) for s in i1.sols],
                      FadeIn(l1[1], shift=up), run_time=1.2)
            settle(self, row1)

            # "Change for zero has exactly one solution, using no coins, ..."
            c.wait_until("r2")
            self.play(Transform(row1, faded(row1, SAID)), FadeOut(self.later),
                      FadeIn(i2a, shift=up), FadeIn(m2a, shift=up), FadeIn(l2a[0], shift=up), run_time=1.3)
            # "... and an empty till, with money still owed, has none."
            c.wait_until("an empty till")
            self.play(FadeIn(i2b, shift=up), FadeIn(m2b, shift=up), FadeIn(l2b[0], shift=up), run_time=1.2)
            settle(self, row2)

            # "At each coin, there are two sources of answers, using it or skipping it, ..."
            c.wait_until("r3")
            self.play(Transform(row2, faded(row2, SAID)), FadeIn(root, shift=up), FadeIn(l3a[0], shift=up),
                      run_time=1.2)
            c.wait_until("using it")
            self.play(*[Create(e) for e in forks],
                      *[time_span(FadeIn(t, shift=0.15 * DOWN), 0.4, 1.2) for t in tips], run_time=1.2)
            # "... and the append joins them."
            c.wait_until("the append")
            self.play(FadeIn(at, scale=0.6), FadeIn(l3b[0], shift=up), FadeIn(l3b[1], shift=up), run_time=1.0)
            settle(self, row3)

            # "And the local function all-see puts the coin on the front of every solution
            # from the use branch."
            c.wait_until("r4")
            self.play(Transform(row3, faded(row3, SAID)), FadeIn(before, shift=up), FadeIn(disc, shift=up),
                      *[FadeIn(p, shift=up) for p in (*l4a, *l4b)], run_time=1.0)
            c.wait_until("puts the coin")
            self.onto_front(before, mid, disc, 0, run_time=1.3)
            self.onto_front(mid, after, disc, 1, run_time=1.0)
            self.row4 = [after, disc, *l4a, *l4b]

            # ⏸ then "Next time, we'll notice how much copying all-see and the append do, ..."
            c.wait_until("next")
            self.teaser(c)

    def onto_front(self, cur, nxt, disc, i, run_time, extra=()):
        """A copy of the disc slides onto the front of solution i; the boxes widen to fit."""
        anims = [ReplacementTransform(cur.big, nxt.big)]
        for s, (a, b) in enumerate(zip(cur.sols, nxt.sols)):
            anims.append(ReplacementTransform(a.box, b.box))
            off = 1 if s == i else 0
            anims += [ReplacementTransform(cn, b.coins[j + off]) for j, cn in enumerate(a.coins)]
        anims.append(TransformFromCopy(disc, nxt.sols[i].coins[0]))
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*nxt.get_family())
        self.add(nxt)

    # ── recap.2, {next}: In [72] small, its copies, accumulators? ─────────────────────
    def teaser(self, c):
        header = VGroup(T("Next:", size=40, color=DIM), T("faster, and exercises", size=40, color=YELLOW))
        header.arrange(RIGHT, buff=0.25)
        header[0].align_to(header[1], UP)
        header.move_to([0, NEXT_Y, 0])

        code = Code(IN72, size=CODE_SIZE)
        code.move_to([0, CODE_TOP - code.height / 2, 0])
        allc = code.find("allc", line=CALL_LINE)
        app = code.find("@", line=CALL_LINE)
        labels, arrows = [], []
        for glyphs in (allc, app):
            g = VGroup(*glyphs)
            lab = T("copies", size=32, color=GOLD).move_to([g.get_x(), COPIES_Y, 0])
            if lab.get_right()[0] > 6.6:
                lab.shift((6.6 - lab.get_right()[0]) * RIGHT)
            arr = Arrow(lab.get_top() + 0.05 * UP, [g.get_x(), g.get_bottom()[1] - 0.06, 0], buff=0,
                        stroke_width=4, color=GOLD, max_tip_length_to_length_ratio=0.3, tip_length=0.18)
            labels.append(lab)
            arrows.append(arr)
        acc = T("accumulators?", size=44, color=YELLOW).move_to([*ACC_POS, 0])

        # The recap sweeps away (all but allc's line, which In [72] doesn't need yet); In [72]
        # comes back, small, under the next part's header.
        sweep_clear(self, time_span(FadeIn(header, shift=0.3 * DOWN), 0.3, 1.0),
                    time_span(FadeIn(code, shift=0.2 * UP), 0.5, 1.5), keep=self.row4, run_time=1.5)
        c.wait_until("copying")
        self.play(*[time_span(FadeOut(m), 0, 0.6) for m in self.row4],
                  *recolor(allc, GOLD), FlashAround(VGroup(*allc), color=GOLD, time_width=1.5),
                  time_span(GrowArrow(arrows[0]), 0.4, 1.2), time_span(FadeIn(labels[0], shift=0.2 * UP), 0.4, 1.2),
                  run_time=1.2)
        c.wait_until("append do")
        self.play(*recolor(app, GOLD), FlashAround(VGroup(*app), color=GOLD, time_width=1.5),
                  GrowArrow(arrows[1]), FadeIn(labels[1], shift=0.2 * UP), run_time=1.2)
        # "... and ask whether accumulators can help, as they did for reverse."
        c.wait_until("accumulators")
        self.play(FadeIn(acc, shift=0.3 * DOWN), run_time=1.0)
