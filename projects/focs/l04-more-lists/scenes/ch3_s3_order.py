"""Chapter 3, scene 3: tracing zip, uneven lists, and why clause order matters.
Clips c3.order.1 - c3.order.4.

s2's last shot (the four-line zip Code alone, hero size, centred) fades back in and shrinks to the
top-right corner, where it stays as the reference. The trace is a stack of Code 28 rows in L3
ch4's style (DIM => column, rows left-aligned, BLUE call box riding down, one box sliding over the
corner clauses), each row born from copies of the row above; the tuple's (, ) and :: fly out of
the clause's `(x, y) ::`, the final [] out of `_ -> []`. The waiting conses turn YELLOW, fire into
the list, and the list becomes three tuple cells plus OCaml's reply. Then the uneven cases, the
code back in the centre with GOLD 1st / 2nd tags, the swap, warning 11 and the rule.

STATUS: built; c3.order.4 re-synced to its re-voice; check clean apart from dwell notes on transient states (trace row 4 and its =>,
cleared on {answer} when the rows give way to the cells; reply A, cleared on "So how does";
"at least one list is empty", which turns false at the swap). 99.3 s vs 91.8 s narration
(1.1 s lead-in fading s2's shot back, 4.1 s end hold for the rule).
Departures: the answer stays up through "different lengths?" and dims, cleared on "Amy and Bob"
(not on {uneven}); the surplus example sits below the short one (no room beside it).
Shared with s4: the answer's PairChain is ch3_s4_pairs' class, copied (value box 2.7 x 1.0, pointer
0.5, tuple text CMU Serif 30 FG, links 0.6, Nil 42; 11.9 wide), centred at y = ANS_Y.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── s2's last shot, as s2 reported it (Code 32 centred at (0, 2.3), recursive zip YELLOW) ──
S2_SIZE = 32
S2_CENTER = 2.3 * UP

ZIP_SRC = ("let rec zip xs ys =\n"
           "  match xs, ys with\n"
           "  | (x::xs, y::ys) -> (x, y) :: zip xs ys\n"
           "  | _ -> []")
CORNER = 28              # the reference copy in the top-right corner
MID = 32                 # the code back in the centre (clips 3-4)

TS = 28                  # trace rows
PITCH = 0.76
BASE = [0.95 - PITCH * k for k in range(6)]
GAP = 0.22               # between the => column and the rows

ROWS = ['zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]',
        '("Amy", 21) :: zip ["Bob"; "Cleo"] [35; 47]',
        '("Amy", 21) :: ("Bob", 35) :: zip ["Cleo"] [47]',
        '("Amy", 21) :: ("Bob", 35) :: ("Cleo", 47) :: zip [] []',
        '("Amy", 21) :: ("Bob", 35) :: ("Cleo", 47) :: []',
        '[("Amy", 21); ("Bob", 35); ("Cleo", 47)]']
CALLS = ['zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]', 'zip ["Bob"; "Cleo"] [35; 47]',
         'zip ["Cleo"] [47]', 'zip [] []', '[]']
WAIT = ['("Amy", 21) ::', '("Amy", 21) :: ("Bob", 35) ::',
        '("Amy", 21) :: ("Bob", 35) :: ("Cleo", 47) ::',
        '("Amy", 21) :: ("Bob", 35) :: ("Cleo", 47) ::']
REPLY_HEAD = "- : (string * int) list ="
PAIRS = [("Amy", 21), ("Bob", 35), ("Cleo", 47)]

SHORT = ['zip ["Amy"; "Bob"; "Cleo"] [21; 35]',
         '("Amy", 21) :: ("Bob", 35) :: zip ["Cleo"] []']
REPLY2 = '- : (string * int) list = [("Amy", 21); ("Bob", 35)]'
SURPLUS = 'zip ["Amy"; "Bob"] [21; 35; 47]'
S_BASE = [0.95, 0.19, None, -1.12, -2.0, -2.76]   # A0, A1, (label), reply A, B0, reply B

W_SRC = "Warning 11 [redundant-case]:\nthis match case is unused."
VAL_SRC = "val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>"
NIL_CALL = 'zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]'
NIL_REPLY = "- : (string * int) list = []"

PAIR_W = 2.7             # tuple cells: ch3_s4_pairs' spec (value box width, cell height CELL)
PAIR_SIZE = 30           # tuple text in the cell: CMU Serif, FG
PAIR_LINK = 0.6          # arrow length between tuple cells
ANS_Y = -0.45

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


# ── helpers ────────────────────────────────────────────────────────────────────
def baseline(code):
    """y of the text baseline of a Code (first glyph that sits on it)."""
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def G(code, sub, nth=0, line=None):
    return VGroup(*code.find(sub, line=line, nth=nth))


def implies():
    return MathTex(r"\Rightarrow", font_size=44, color=DIM)


def ocaml_reply(src, base_color=None):
    c = Code(src, size=TS)
    if base_color is not None:
        c.text.set_color(base_color)
    return c


class PairCell(VGroup):
    """[ ("Amy", 21) | • ]: one cons cell whose value is a pair (ch3_s4_pairs' class, copied)."""

    def __init__(self, name, num, color=BLUE, **kw):
        super().__init__(**kw)
        self.box = Rectangle(width=PAIR_W, height=CELL, stroke_color=color, stroke_width=3,
                             fill_color=BG, fill_opacity=1)
        self.ptr = Rectangle(width=PTR_W, height=CELL, stroke_color=color, stroke_width=3,
                             fill_color=BG, fill_opacity=1).next_to(self.box, RIGHT, buff=0)
        self.dot = Dot(self.ptr.get_center(), radius=0.07, color=FG)
        self.label = T(f'("{name}", {num})', size=PAIR_SIZE).move_to(self.box)
        self.label.set_z_index(2)          # above a highlight box (z 1) above the cell (z 0)
        k = len(name) + 2                  # glyphs: ( "name" , num )   (no glyph for spaces)
        self.name_part = self.label[1:1 + k]
        self.num_part = self.label[2 + k:2 + k + len(str(num))]
        self.add(self.box, self.ptr, self.dot, self.label)

    def tail_start(self):
        return self.dot.get_center()

    def entry(self):
        return self.box.get_left()


class PairChain(VGroup):
    """ConsChain's layout with tuple cells: .cells[i], .arrows[i] (out of cell i), .nil."""

    def __init__(self, pairs, **kw):
        super().__init__(**kw)
        self.cells = [PairCell(n, v) for n, v in pairs]
        x = 0.0
        for c in self.cells:
            c.move_to(RIGHT * x, aligned_edge=LEFT)
            x += PAIR_W + PTR_W + PAIR_LINK
        self.nil = Nil().move_to(RIGHT * (x + 0.25))
        targets = self.cells[1:] + [self.nil]
        self.arrows = [link(c, t) for c, t in zip(self.cells, targets)]
        self.add(*self.cells, *self.arrows, self.nil)
        self.move_to(ORIGIN)


class UnevenAndOrder(NarratedScene):
    def construct(self):
        self.zip = Code(ZIP_SRC, size=S2_SIZE).move_to(S2_CENTER)
        G(self.zip, "zip", line=2).set_color(YELLOW)      # s2 colours the recursive call too
        self.play(FadeIn(self.zip), run_time=0.8)
        self.wait(0.3)
        self.trace()        # c3.order.1
        self.uneven()       # c3.order.2
        self.order()        # c3.order.3
        self.swap()         # c3.order.4
        self.wait(4.1)      # the rule gets its reading time
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── shared moves ───────────────────────────────────────────────────────────
    def birth(self, dst, pairs, fades=(), arrow=None, extra=(), run_time=1.5, start=0.0):
        """`dst` is born from copies: (source glyphs, dst substring, nth, path_arc), during
        [start, run_time] of the play."""
        anims, targets = [], []
        for src, sub, nth, arc in pairs:
            t = G(dst, sub, nth)
            anims.append(TransformFromCopy(src, t, path_arc=arc))
            targets.append(t)
        for sub, nth in fades:
            t = G(dst, sub, nth)
            anims.append(FadeIn(t, shift=0.2 * DOWN))
            targets.append(t)
        if arrow is not None:
            anims.append(FadeIn(arrow, shift=0.2 * DOWN))
        if start > 0:
            anims = [time_span(a, start, run_time) for a in anims]
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*targets)
        self.add(dst)

    def step_bits(self, dst, nth):
        """The tuple's ( , ) and the :: out of the step clause's `(x, y) ::`."""
        z = self.zip
        return [(G(z, "(", 1, line=2), "(", nth, 0.5), (G(z, ",", 1, line=2), ",", nth, 0.5),
                (G(z, ")", 1, line=2), ")", nth, 0.5), (G(z, "::", 2, line=2), "::", nth, 0.5)]

    def clause_box(self, sub, line, color):
        glyphs = self.zip.find(sub, line=line)
        return token_box(glyphs, self.zip.line(line), color=color, pad=0.2, height=0.5)

    # ── order.1: the trace of the phone book ──────────────────────────────────
    def trace(self):
        z = self.zip
        rows = [Code(s, size=TS) for s in ROWS]
        imp_w = implies().width
        left = -(rows[3].width + imp_w + GAP) / 2
        x0 = left + imp_w + GAP
        for r, b in zip(rows, BASE):
            put(r, x0, b)
        arrows = [None] + [implies().next_to(r, LEFT, buff=GAP).set_y(b + 0.1)
                           for r, b in zip(rows[1:], BASE[1:])]
        self.rows, self.arrows = rows, arrows

        def call_box(k):
            return token_box(G(rows[k], CALLS[k]), rows[k], color=BLUE, pad=0.16, height=0.5)

        with self.say("c3.order.1") as c:
            # "Let's zip our phone book."  The definition steps into the corner; the call arrives.
            self.play(z.animate.scale(CORNER / S2_SIZE).to_corner(UR, buff=0.5),
                      time_span(FadeIn(rows[0], shift=0.3 * DOWN), 0.5, 1.4),
                      run_time=min(1.5, max(0.8, c.until("s1") - 0.2)))

            # "Both lists have a head, so Amy pairs with twenty-one, and we zip the rest."
            c.wait_until("s1")
            cbox = call_box(0)
            lbox = self.clause_box(z.src.splitlines()[2].strip(), 2, BLUE)
            self.play(FadeIn(cbox), FadeIn(lbox), run_time=0.8)
            c.wait_until("have a head")
            self.play(FlashAround(G(rows[0], '"Amy"'), color=YELLOW, time_width=1.5),
                      FlashAround(G(rows[0], "21"), color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("so amy pairs")
            r0 = rows[0]
            self.birth(rows[1], [(G(r0, '"Amy"'), '"Amy"', 0, -0.8), (G(r0, "21"), "21", 0, -0.8),
                                 *self.step_bits(rows[1], 0),
                                 (G(r0, "zip ["), "zip [", 0, 0),
                                 (G(r0, '"Bob"; "Cleo"]'), '"Bob"; "Cleo"]', 0, 0),
                                 (G(r0, "[", 1), "[", 1, 0), (G(r0, "35; 47]"), "35; 47]", 0, 0)],
                       arrow=arrows[1], run_time=min(2.0, 0.9 * c.until("zip the rest")))
            c.wait_until("zip the rest")
            self.play(Transform(cbox, call_box(1)), run_time=min(1.0, 0.8 * c.until("s2")))

            # "Then Bob with thirty-five,"
            c.wait_until("s2")
            r1 = rows[1]
            self.birth(rows[2], [(G(r1, '("Amy", 21) ::'), '("Amy", 21) ::', 0, 0),
                                 (G(r1, '"Bob"'), '"Bob"', 0, -0.8), (G(r1, "35"), "35", 0, -0.8),
                                 *self.step_bits(rows[2], 1),
                                 (G(r1, "zip ["), "zip [", 0, 0), (G(r1, '"Cleo"]'), '"Cleo"]', 0, 0),
                                 (G(r1, "[", 1), "[", 1, 0), (G(r1, "47]"), "47]", 0, 0)],
                       arrow=arrows[2], extra=[Transform(cbox, call_box(2))],
                       run_time=min(1.3, 0.9 * c.until("s3")))

            # "and Cleo with forty-seven."
            c.wait_until("s3")
            r2 = rows[2]
            self.birth(rows[3], [(G(r2, WAIT[1]), WAIT[1], 0, 0),
                                 (G(r2, '"Cleo"'), '"Cleo"', 0, -0.8), (G(r2, "47"), "47", 0, -0.8),
                                 *self.step_bits(rows[3], 2),
                                 (G(r2, "zip ["), "zip [", 0, 0), (G(r2, "]", 0), "]", 0, 0),
                                 (G(r2, "[", 1), "[", 1, 0), (G(r2, "]", 1), "]", 1, 0)],
                       arrow=arrows[3], extra=[Transform(cbox, call_box(3))],
                       run_time=min(1.2, 0.9 * c.until("s4")))

            # "Now both lists are empty."
            c.wait_until("s4")
            self.play(FlashAround(G(rows[3], "[] []"), color=TEAL, time_width=1.5), run_time=1.2)

            # "The first pattern fails, so the wildcard takes over, and gives nil."
            c.wait_until("first pattern fails")
            self.play(Transform(lbox, self.clause_box("(x::xs, y::ys)", 2, RED)), run_time=0.9)
            c.wait_until("wildcard takes over")
            self.play(Transform(lbox, self.clause_box("_ -> []", 3, YELLOW)), run_time=1.0)
            c.wait_until("gives nil")
            self.birth(rows[4], [(G(rows[3], WAIT[2]), WAIT[2], 0, 0),
                                 (G(z, "[]", line=3), "[]", 0, 0.6)],
                       arrow=arrows[4], extra=[Transform(cbox, call_box(4))],
                       run_time=min(1.3, 0.9 * c.until("done")))

            # "As in append, the conses were waiting, and now they all happen."
            c.wait_until("done")
            anims = [FadeOut(cbox), FadeOut(lbox)]
            for k in range(1, 5):
                for a in recolor(G(rows[k], WAIT[k - 1]), YELLOW):
                    anims.append(time_span(a, 0.25 * (k - 1), 0.25 * (k - 1) + 0.8))
            self.play(*anims, run_time=1.55)
            c.wait_until("now they all happen")
            r4, r5 = rows[4], rows[5]
            fire = [time_span(FlashAround(G(r4, f"{t} ::"), color=YELLOW, time_width=1.5),
                              0.2 * j, 0.2 * j + 0.8)
                    for j, t in enumerate(['("Cleo", 47)', '("Bob", 35)', '("Amy", 21)'])]
            self.birth(r5, [*[(G(r4, f'("{n}", {v})'), f'("{n}", {v})', 0, 0) for n, v in PAIRS],
                            (G(r4, "::", 0), ";", 0, 0), (G(r4, "::", 1), ";", 1, 0),
                            (G(r4, ":: []"), "]", 0, 0)],
                       fades=[("[", 0)], arrow=arrows[5], extra=fire,
                       run_time=min(1.6, 0.9 * c.until("answer")))

            # "Three pairs, in order."  The trace makes way: the list becomes cells, and the
            # last row becomes OCaml's reply, under a head born where the row above it was.
            c.wait_until("answer")
            chain = PairChain(PAIRS).move_to(UP * ANS_Y)
            head = put(Code(REPLY_HEAD, size=TS), x0, BASE[4])
            frames = [m for cell in chain.cells for m in (cell.box, cell.ptr, cell.dot)]
            gone = [*rows[1:5], *arrows[1:5]]
            anims = [time_span(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.1), 0, 0.8)]
            anims += [time_span(FadeIn(m), 0.3, 1.0) for m in frames]
            anims += [time_span(ReplacementTransform(G(r5, f'("{n}", {v})').copy().set_z_index(2),
                                                     cell.label), 0.3, 1.4)
                      for (n, v), cell in zip(PAIRS, chain.cells)]
            anims += [time_span(GrowArrow(a), 0.9, 1.5) for a in chain.arrows]
            anims += [time_span(FadeIn(chain.nil), 1.1, 1.6),
                      time_span(ReplacementTransform(arrows[5], head), 0.6, 1.6)]
            self.play(*anims, run_time=1.6)
            settle(self, chain)
        self.x0 = x0
        self.answer = [chain, head, r5]

    # ── order.2: three names, two numbers; then the surplus on the other side ─────
    def uneven(self):
        z = self.zip
        a0, a1 = [Code(s, size=TS) for s in SHORT]
        rep_a, b0, rep_b = Code(REPLY2, size=TS), Code(SURPLUS, size=TS), Code(REPLY2, size=TS)
        x0 = self.x0                     # same column as the trace: the call is edited in place
        for m, b in zip([a0, a1, None, rep_a, b0, rep_b], S_BASE):
            if m is not None:
                put(m, x0, b)
        arr = implies().next_to(a1, LEFT, buff=GAP).set_y(S_BASE[1] + 0.1)
        for t in ['("Amy", 21) ::', '("Bob", 35) ::']:
            G(a1, t).set_color(YELLOW)
        cleo = G(a1, '"Cleo"')
        dropped = T("dropped", size=30, color=RED).next_to(cleo, DOWN, buff=0.22)
        b47 = G(b0, "47")
        dropped2 = T("dropped", size=30, color=RED).next_to(b0, RIGHT, buff=0.45)
        pattern = G(z, "(x::xs, y::ys)", line=2)
        cross = Cross(Rectangle(width=pattern.width + 0.1, height=0.42).move_to(pattern),
                      stroke_color=RED, stroke_width=5)
        lbox = self.clause_box("_ -> []", 3, YELLOW)

        with self.say("c3.order.2") as c:
            # "But what if the lists have different lengths?"  The answer stays up.
            # "Suppose Cleo has no number yet, so we zip three names with only two numbers."
            # The call loses its 47 in place; the old answer steps back.
            c.wait_until("short")
            r0 = self.rows[0]
            self.birth(a0, [(G(r0, 'zip ["Amy"; "Bob"; "Cleo"] [21; 35'),
                             'zip ["Amy"; "Bob"; "Cleo"] [21; 35', 0, 0),
                            (G(r0, "]", 1), "]", 1, 0)],
                       extra=[FadeOut(r0), *set_alpha(self.answer, 0.35)], run_time=1.3)
            c.wait_until("three names")
            self.play(FlashUnder(G(a0, '["Amy"; "Bob"; "Cleo"]'), color=YELLOW, time_width=1.5),
                      run_time=1.0)
            c.wait_until("two numbers")
            self.play(FlashUnder(G(a0, "[21; 35]"), color=GOLD, time_width=1.5), run_time=1.0)

            # "Amy and Bob pair up as before."
            c.wait_until("amy and bob")
            old = [time_span(FadeOut(m), 0, 0.6) for m in self.answer]
            self.birth(a1, [(G(a0, '"Amy"'), '"Amy"', 0, -0.8), (G(a0, "21"), "21", 0, -0.8),
                            (G(a0, '"Bob"'), '"Bob"', 0, -0.8), (G(a0, "35"), "35", 0, -0.8),
                            *self.step_bits(a1, 0), *self.step_bits(a1, 1),
                            (G(a0, "zip ["), "zip [", 0, 0), (G(a0, '"Cleo"]'), '"Cleo"]', 0, 0),
                            (G(a0, "[", 1), "[", 1, 0), (G(a0, "]", 1), "]", 1, 0)],
                       arrow=arr, extra=old, start=0.3, run_time=min(1.7, 0.9 * c.until("catch")))

            # "That leaves the list holding Cleo, and nil."
            c.wait_until("holding cleo")
            self.play(FlashAround(G(a1, '["Cleo"]'), color=YELLOW, time_width=1.5), run_time=0.9)
            c.wait_until("and nil")
            self.play(FlashAround(G(a1, "[]"), color=TEAL, time_width=1.5), run_time=0.9)

            # "The first pattern needs two heads, so the wildcard returns nil."
            c.wait_until("needs two heads")
            self.play(Create(cross), run_time=0.9)
            c.wait_until("wildcard returns nil")
            self.play(FadeIn(lbox), FlashAround(G(z, "[]", line=3), color=TEAL, time_width=1.5),
                      run_time=1.0)

            # "Cleo is simply dropped."
            c.wait_until("drop")
            self.play(*recolor(cleo, RED), FadeIn(dropped, shift=0.25 * UP), run_time=0.9)
            self.wait(0.2)
            self.play(*[g.animate.set_opacity(0.4) for g in cleo], FadeIn(rep_a, shift=0.2 * DOWN),
                      run_time=min(1.0, max(0.5, c.until("surplus") - 0.1)))

            # "Zip discards any surplus at the end of the longer list, whichever list that is."
            c.wait_until("surplus")
            self.play(FadeIn(b0, shift=0.2 * DOWN), time_span(FadeIn(rep_b, shift=0.2 * DOWN), 0.5, 1.3),
                      run_time=1.3)
            c.wait_until("whichever list")
            self.play(*recolor(b47, RED),
                      FadeIn(dropped2, shift=0.25 * LEFT), run_time=min(0.9, c.remaining))
        self.lbox = lbox

    # ── order.3: the code back in the centre; the clauses are tried in order ──────
    def order(self):
        z = self.zip
        k = MID / CORNER
        tgt = z.copy().scale(k)
        tag_w = T("2nd", size=30).width
        arw = 0.75
        total = arw + 0.12 + tag_w + 0.28 + tgt.width
        code_left = -total / 2 + arw + 0.12 + tag_w + 0.28
        tgt.shift(RIGHT * (code_left - tgt.get_left()[0]) + UP * (0.75 - tgt.get_y()))
        bar2, bar3 = G(tgt, "|", line=2), G(tgt, "|", line=3)
        tag_x = code_left - 0.28
        tag1 = T("1st", size=30, color=GOLD)
        tag1.move_to([tag_x - tag1.width / 2, bar2.get_y(), 0])
        tag2 = T("2nd", size=30, color=GOLD)
        tag2.move_to([tag_x - tag2.width / 2, bar3.get_y(), 0])
        q = T("?", size=48, color=YELLOW).move_to([tag_x - tag_w / 2, bar2.get_y(), 0])
        ax = tag_x - tag_w - 0.12
        arrow = Arrow([ax - arw, bar2.get_y(), 0], [ax, bar2.get_y(), 0], buff=0, color=YELLOW,
                      stroke_width=5, max_tip_length_to_length_ratio=0.35)
        dy = bar2.get_y() - bar3.get_y()
        self.pitch = dy
        wild = G(tgt, "_", line=3)
        sees = T("at least one list is empty", size=30, color=TEAL)
        sees.next_to(wild, DOWN, buff=0.75).align_to(wild, LEFT).shift(LEFT * 0.3)
        sees_arrow = Arrow([wild.get_x(), sees.get_top()[1] + 0.08, 0],
                           [wild.get_x(), wild.get_bottom()[1] - 0.1, 0], buff=0, color=TEAL,
                           stroke_width=4, max_tip_length_to_length_ratio=0.3)

        with self.say("c3.order.3") as c:
            # "Now, the wildcard matches every argument, not just empty lists."  The box in the
            # corner narrows to the _ itself; the uneven examples stay up for this sentence.
            c.wait_until("every argument")
            self.play(Transform(self.lbox, self.clause_box("_", 3, YELLOW)),
                      FlashAround(G(z, "_", line=3), color=YELLOW, time_width=1.5), run_time=1.0)

            # "So how does the first clause ever get a turn?"  The code comes back to the
            # centre; the question is asked on screen, by the clause.
            c.wait_until("so how does")
            sweep_clear(self, z.animate.scale(k).move_to(tgt.get_center()), keep=[z], run_time=1.5)
            box = token_box(z.find("(x::xs, y::ys)", line=2), z.line(2), color=YELLOW, pad=0.24,
                            height=0.56)
            c.wait_until("first clause")
            self.play(FadeIn(box), FadeIn(q, shift=0.2 * DOWN), run_time=1.0)

            # "Because OCaml tries the clauses in order."  The question becomes the answer.
            c.wait_until("tried")
            self.play(ReplacementTransform(q, tag1), time_span(FadeIn(tag2, shift=0.2 * DOWN), 0.4, 1.2),
                      FadeOut(box), run_time=1.2)

            # "The first pattern is tried first, and the wildcard only when that fails."
            c.wait_until("first pattern is tried")
            self.play(GrowArrow(arrow), run_time=0.8)
            c.wait_until("only when that fails")
            self.play(arrow.animate.shift(DOWN * dy), run_time=1.0)

            # "So the wildcard only ever sees arguments where at least one list is empty."
            c.wait_until("sees")
            self.play(FadeIn(sees, shift=0.25 * UP), GrowArrow(sees_arrow), run_time=1.0)
        self.tags = [tag1, tag2]
        self.gone3 = [arrow, sees, sees_arrow]

    # ── order.4: wildcard first; warning 11; the rule ───────────────────────────
    def swap(self):
        z = self.zip
        tag1, tag2 = self.tags
        lift = 3.45 - z.get_top()[1]
        step, wild_line = z.line(2), z.line(3)
        dy = self.pitch
        wtext = Code(W_SRC, size=TS)
        wtext.text.set_color(FG)
        G(wtext, "Warning 11 [redundant-case]:").set_color(YELLOW)
        wtext.move_to(UP * 0.12)
        wbox = SurroundingRectangle(wtext, buff=0.2, color=YELLOW, stroke_width=3, corner_radius=0.08)
        val = Code(VAL_SRC, size=TS).move_to(UP * -1.1)
        for j in range(2):
            G(val, "'b", j).set_color(PURPLE)
        call = Code(NIL_CALL, size=TS)
        reply = Code(NIL_REPLY, size=TS)
        reply.text.set_color(RED)
        VGroup(call, reply).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(UP * -0.85)
        rule = T("specific patterns first, catch-all last", size=40, color=YELLOW).move_to(UP * -2.55)

        with self.say("c3.order.4") as c:
            # "That makes the order matter."  The code goes up to make room.
            self.play(*[m.animate.shift(UP * lift) for m in (z, tag1, tag2, *self.gone3)],
                      run_time=1.2)

            # "Put the wildcard first,"  The two clauses trade places; the tags stay put, and
            # the _ that now comes first turns RED.
            c.wait_until("put the wildcard first")
            wild = G(z, "_", line=3)[0]
            anims = [FadeOut(m) for m in self.gone3]
            anims += [g.animate(path_arc=-PI / 2).shift(DOWN * dy) for g in step]
            anims += [g.animate(path_arc=-PI / 2).shift(UP * dy) for g in wild_line if g is not wild]
            anims.append(wild.animate(path_arc=-PI / 2).shift(UP * dy).set_color(RED))
            self.play(*anims, run_time=1.6)

            # "and OCaml warns you, with warning eleven."
            c.wait_until("warn")
            self.play(time_span(Create(wbox), 0, 1.0), time_span(FadeIn(wtext, shift=0.2 * DOWN), 0.3, 1.2),
                      time_span(FadeIn(val, shift=0.2 * DOWN), 0.9, 1.7), run_time=1.7)
            c.wait_until("warning eleven")
            self.play(FlashUnder(G(wtext, "Warning 11"), color=YELLOW, time_width=1.5), run_time=1.0)

            # "This match case is unused."  It points at the step clause's pattern.
            c.wait_until("this match case")
            self.play(FlashUnder(VGroup(*wtext.line(1)), color=YELLOW, time_width=1.5),
                      FlashAround(G(z, "(x::xs, y::ys)", line=2), color=RED, time_width=1.5),
                      run_time=1.3)

            # "The wildcard now catches every call, so the second clause can never run."
            c.wait_until("never")
            self.play(FlashAround(G(z, "_ -> []", line=3), color=RED, time_width=1.5), run_time=1.0)
            c.wait_until("second clause")
            self.play(*[g.animate.set_opacity(0.3) for g in step], tag2.animate.set_opacity(0.3),
                      run_time=1.0)

            # "Zip still has the same type, but it returns nil for everything."
            c.wait_until("nil")
            self.play(FadeOut(wbox), FadeOut(wtext), val.animate.move_to(UP * 0.55), run_time=1.0)
            c.wait_until("returns nil")
            self.play(FadeIn(call, shift=0.2 * DOWN), time_span(FadeIn(reply, shift=0.2 * DOWN), 0.4, 1.2),
                      run_time=min(1.2, 0.9 * c.until("rule")))

            # "So put the specific patterns first, and the catch-all pattern at the end."
            c.wait_until("rule")
            self.play(FadeIn(rule, shift=0.25 * UP), run_time=1.0)
