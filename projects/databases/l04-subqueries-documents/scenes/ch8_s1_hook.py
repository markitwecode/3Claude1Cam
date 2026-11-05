"""Chapter 8, scene 1: ten actors squeezed into one row. Clips c8.hook.1 – c8.hook.3.

Exports (import with `H = load_scene("ch8_s1_hook")`; all static, no updaters):

    H.open_card(lifted=True) -> VGroup(.table .tag .cell .link .doc .chips .slots), ch8's first frame
        (ch7 s8 lands on exactly this). lifted=False: chips inside .doc, .slots empty (not on screen).
    H.handover_shot() -> open_card(lifted=True), this scene's last frame (ch8 s2 opens on it).
    H.CAST (the ten names, array order), H.chip(name, w) (one TEAL name chip), H.CHIP_W.

Exact geometry (scene units; frame x ±7.1, y ±4):
    .table  ch7 s1 movies_card() scaled 0.38, top-left corner (-6.3, 3.5): 3.59 x 2.04, centre (-4.5, 2.48), The Kid's row
            (YELLOW id + cell) centred at y ≈ 2.77 (KID_Y; computed from the card).
    .cell   TEAL box (stroke 2.5) round The Kid's `movie` cell (ch7 s1 cell_box()).
    .tag    GOLD "1 row": T 26 GOLD in a GOLD rounded box (stroke 2, fill 0.12), 1.13 x 0.46, centre (-1.74, 2.77),
            left edge at table right + 0.4, centred on KID_Y.
    .link   TEAL elbow (stroke 3): table right edge at KID_Y -> 0.2 right -> straight down to the
            doc's top edge.
    .doc    ch4 s3 document-card look: frame (RoundedRectangle corner 0.2, TEAL stroke 3, fill 0.06),
            left edge -6.3, top 0.28 under the table (1.19), 5.02 x 4.62, centre (-3.79, -1.12); inside, json_code size 22:
            `"actors": [` on chip 0's line (left 0.2 inside), `]` on its own line under chip 9, same left.
            .doc = VGroup(frame, key, close); .doc.frame .doc.key .doc.close.
    .chips  ten chips, CAST order: RoundedRectangle (corner 0.1, TEAL stroke 2, fill 0.12),
            CHIP_W (= widest name + 0.3, ≈ 2.5) x 0.34, name T 22 TEAL (baseline-aligned);
            unlifted: one column, left edge 0.18 right of `[`, chip 0 centre y = doc top - 0.32,
            pitch 0.40 down: x -2.72, y 0.86 … -2.74. lifted=True: each chip exactly half way (midpoint) between its unlifted
            centre and its slot centre: x 1.09, y 1.78 … -2.72, pitch 0.50.
    .slots  ten faint BLUE row slots (Rectangle CHIP_W + 0.3 x 0.46, BLUE stroke 2 at 0.5, fill 0.08),
            one column centred x = 4.9, slot i centre y = 2.7 - 0.6 i (2.7 … -2.7).
    `print_geometry()` prints every centre/size (run it to verify the numbers above).

Plan: open on open_card(lifted=True) 0.7 s, sweep to the title card on {title}; {cell} rebuild
open_card(lifted=False) (table, cell, link, doc; chips on "ten"; tag on "single row"); three question
cards on {sort}/{genres}/{ages} (right half), ORDER BY / GROUP BY / JOIN under them, DIM "these work on
rows" with an arrow to the "1 row" tag; {ask} cards clear, slots fade in, chips lift half way; hold.
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
from lib.titles import title_card  # noqa: E402

H7 = load_scene("ch7_s1_hook")
D = load_scene("ch4_s3_movie")

CAST = ["Charles Chaplin", "Edna Purviance", "Jackie Coogan", "Carl Miller", "Albert Austin",
        "Beulah Bains", "Nellie Bly Baker", "Henry Bergman", "Edward Biby", "B.F. Blinn"]

TABLE_S = 0.38
TABLE_LEFT, TABLE_TOP = -6.3, 3.5
CODE_S = 22
CHIP_S, CHIP_H, CHIP_PITCH = 22, 0.34, 0.40
CHIP_W = max(T(n, CHIP_S).width for n in CAST) + 0.3
SLOT_X, SLOT_TOP, SLOT_PITCH, SLOT_H = 4.9, 2.7, 0.6, 0.46
DOC_PAD = 0.2


def chip(name, w=CHIP_W):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=CHIP_H)
    box.set_stroke(TEAL, 2).set_fill(TEAL, 0.12)
    txt = T(name, CHIP_S, TEAL)
    txt.move_to(box)
    base = box.get_center()[1] - 0.0095 * CHIP_S / 2     # every name on one baseline
    txt.shift(UP * (base - txt[0].get_bottom()[1]))
    g = VGroup(box, txt)
    g.box, g.text = box, txt
    return g


def _tag():
    txt = T("1 row", 26, GOLD)
    box = RoundedRectangle(corner_radius=0.12, width=txt.width + 0.3, height=0.46)
    box.set_stroke(GOLD, 2).set_fill(GOLD, 0.12)
    txt.move_to(box)
    g = VGroup(box, txt)
    g.box, g.text = box, txt
    return g


def open_card(lifted=True):
    table = H7.movies_card().scale(TABLE_S)
    table.shift(RIGHT * (TABLE_LEFT - table.get_left()[0]) + UP * (TABLE_TOP - table.get_top()[1]))
    kid_y = table.rows[0].get_center()[1]
    t_right = table.box.get_right()[0]
    cell = H7.cell_box(table)

    tag = _tag()
    tag.move_to([t_right + 0.4 + tag.width / 2, kid_y, 0])

    doc_top = table.get_bottom()[1] - 0.28
    key = D.json_code('"actors": [', CODE_S)
    close = D.json_code("]", CODE_S)
    chips = VGroup(*[chip(n) for n in CAST])
    y0 = doc_top - 0.32
    x_chip = TABLE_LEFT + DOC_PAD + key.width + 0.18 + CHIP_W / 2
    for i, ch in enumerate(chips):
        ch.move_to([x_chip, y0 - i * CHIP_PITCH, 0])
    key.move_to([TABLE_LEFT + DOC_PAD + key.width / 2, y0, 0])
    close.move_to([TABLE_LEFT + DOC_PAD + close.width / 2, y0 - 10 * CHIP_PITCH, 0])
    w = x_chip + CHIP_W / 2 + DOC_PAD - TABLE_LEFT
    h = doc_top - (close.get_bottom()[1] - 0.16)
    frame = D._frame(w, h)
    frame.move_to([TABLE_LEFT + w / 2, doc_top - h / 2, 0])
    doc = VGroup(frame, key, close)
    doc.frame, doc.key, doc.close = frame, key, close

    lx = t_right + 0.2
    link = VMobject().set_points_as_corners([[t_right, kid_y, 0], [lx, kid_y, 0], [lx, doc_top, 0]])
    link.set_stroke(TEAL, 3)

    slots = VGroup()
    if lifted:
        for i in range(len(CAST)):
            s = Rectangle(width=CHIP_W + 0.3, height=SLOT_H)
            s.set_stroke(BLUE, 2, opacity=0.5).set_fill(BLUE, 0.08)
            s.move_to([SLOT_X, SLOT_TOP - i * SLOT_PITCH, 0])
            slots.add(s)
        for ch, s in zip(chips, slots):
            ch.move_to((ch.get_center() + s.get_center()) / 2)

    g = VGroup(table, cell, tag, link, doc, chips, slots)
    g.table, g.cell, g.tag, g.link, g.doc, g.chips, g.slots = table, cell, tag, link, doc, chips, slots
    g.kid_y = kid_y
    return g


def handover_shot():
    return open_card(lifted=True)


def print_geometry():
    for lifted in (False, True):
        g = open_card(lifted)
        print("lifted", lifted)
        for k in ("table", "cell", "tag", "link", "doc"):
            m = getattr(g, k)
            print(f"  {k}: centre {np.round(m.get_center()[:2], 2)}, {m.width:.2f} x {m.height:.2f}")
        print(f"  kid_y {g.kid_y:.2f}, CHIP_W {CHIP_W:.2f}")
        for n, ch in zip(CAST, g.chips):
            print(f"  chip {n}: {np.round(ch.get_center()[:2], 2)}")
        for i, s in enumerate(g.slots):
            print(f"  slot {i}: {np.round(s.get_center()[:2], 2)}")


# ══ question cards and tools ═══════════════════════════════════════════════════

QUESTIONS = ["Sort the cast by name", "How many movies in each genre?", "How old was each actor?"]
TOOLS = ["ORDER BY", "GROUP BY", "JOIN"]
Q_X, Q_TOP, Q_PITCH, Q_H = 0.25, 2.1, 1.0, 0.74


def q_cards():
    txts = [T(q, 28) for q in QUESTIONS]
    w = max(t.width for t in txts) + 1.15
    out = []
    for i, t in enumerate(txts):
        box = RoundedRectangle(corner_radius=0.15, width=w, height=Q_H).set_stroke(DIM, 2).set_fill(BG, 0)
        box.move_to([Q_X + w / 2, Q_TOP - i * Q_PITCH, 0])
        mark = T("?", 40, GOLD, weight=BOLD).move_to([box.get_left()[0] + 0.4, box.get_y(), 0])
        t.move_to([mark.get_right()[0] + 0.25 + t.width / 2, box.get_y(), 0])
        g = VGroup(box, mark, t)
        g.box, g.mark, g.text = box, mark, t
        out.append(g)
    return out


def tool_row(cards):
    tools = VGroup(*[Mono(s, 32, BLUE) for s in TOOLS]).arrange(RIGHT, buff=0.55)
    left, right = cards[0].get_left()[0], max(c.get_right()[0] for c in cards)
    tools.move_to([(left + right) / 2, cards[-1].get_y() - 1.05, 0])
    return list(tools)


# ══ the scene ══════════════════════════════════════════════════════════════════

class Ch8S1Hook(NarratedScene):
    def construct(self):
        self.add(open_card(lifted=True))   # ch7's recap ends on this
        self.wait(0.7)
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.0)   # handover: ch8 s2 opens on handover_shot()

    def clip1(self):
        with self.say("c8.hook.1") as c:
            tc = title_card("Part 8 · Arrays into rows")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("cell")

            oc = open_card(lifted=False)
            self.oc = oc
            sweep_clear(self, time_span(FadeIn(oc.table), 0.75, 1.6),
                        time_span(FadeIn(oc.cell), 1.0, 1.6),
                        time_span(Create(oc.link), 1.1, 1.6),
                        time_span(FadeIn(oc.doc), 1.1, 1.6), run_time=1.6)
            c.wait_until("ten")
            self.play(*appear(*oc.chips, shift=0.15 * DOWN, lag=0.12),
                      run_time=min(1.8, c.until("single")))
            c.wait_until("single")
            self.play(*appear(oc.tag, shift=None),
                      FlashAround(oc.table.rows[0], run_time=1.5, time_width=1.5), run_time=1.5)

    def clip2(self):
        oc = self.oc
        with self.say("c8.hook.2") as c:
            cards = q_cards()
            self.cards = cards
            for cue, card in zip(("sort", "genres", "ages"), cards):
                c.wait_until(cue)
                self.play(*appear(card), run_time=1.0)
            tools = tool_row(cards)
            self.tools = tools
            for cue, t in zip(("order by", "group by", "joins"), tools):
                c.wait_until(cue)
                self.play(*appear(t, shift=0.2 * DOWN), run_time=0.8)

            c.wait_until("work on rows")
            label = T("these work on rows", 30, DIM)
            label.move_to([cards[0].get_left()[0] + label.width / 2, tools[0].get_y() - 0.95, 0])
            start = label.get_left() + 0.05 * LEFT + 0.12 * UP
            end = oc.tag.get_corner(DR) + 0.05 * DOWN
            arrow = Arrow(start, end, buff=0.08, stroke_width=3, color=DIM,
                          max_tip_length_to_length_ratio=0.06)
            self.label, self.arrow = label, arrow
            self.play(*appear(label, shift=None), GrowArrow(arrow), run_time=1.2)
            c.wait_until("squeezed")
            self.play(FlashAround(VGroup(*oc.chips), run_time=1.8, time_width=1.5, color=YELLOW),
                      run_time=min(1.8, c.until()))

    def clip3(self):
        oc = self.oc
        tgt = open_card(lifted=True)
        with self.say("c8.hook.3") as c:
            self.play(*disappear(*self.cards, *self.tools, self.label, self.arrow), run_time=0.8)
            self.play(*during(appear(*tgt.slots, shift=None, lag=0.06), 0, 0.6),
                      *during([ch.animate.move_to(t.get_center()) for ch, t in zip(oc.chips, tgt.chips)],
                              0.15, 1),
                      run_time=2.4)
