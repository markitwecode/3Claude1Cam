"""Chapter 3, scene 7: the whole toolkit on one card. Clips c3.kit.1 – c3.kit.3.

Owns *the toolkit card* (reused by ch3 s8's end card, ch4 s1's callback, ch8 s6's TEAL JSON twin):

    mod = load_scene("ch3_s7_toolkit")
    card = mod.toolkit_card()   # static VGroup, full size, centred at ORIGIN (about 10.1 x 6.95)
    card.frame                  # BLUE rounded border (stroke 3, faint fill)
    card.title                  # T 44 "Relational algebra summary"
    card.heads                  # VGroup of the two DIM T 28 column heads ("SQL", "Relational algebra")
    card.rule, card.foot_rule   # DIM lines under the heads / above the footer
    card.rows                   # VGroup of 12 rows (slide 68's order); each row is VGroup(sql, glyph, name)
                                #   with .sql (Mono 28, keywords in `color`), .glyph (STIX Two Math 38, `color`),
                                #   .name (T 28 FG)
    card.footer                 # T 30 "Relational algebra works on sets, SQL on multisets."
    card.body                   # VGroup of everything but the footer and its rule

    toolkit_card(rows=TOOLKIT_ROWS, title=..., heads=..., footer=..., color=BLUE, plain=None)
    builds a twin in the same layout: rows = [(sql_text, glyph, name)], `plain` = {substring: colour}
    for parts of the sql text that are not keywords (default: "..." DIM, "a, b" FG).
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

TOOLKIT_ROWS = [
    ("WHERE ...", "σ", "selection: rows"),
    ("SELECT a, b", "π", "projection: columns"),
    ("AS", "ρ", "renaming"),
    ("GROUP BY", "γ", "grouping & aggregation"),
    ("FROM a, b", "×", "cartesian product"),
    ("JOIN ... ON", "⋈", "inner join"),
    ("LEFT JOIN", "⟕", "left outer join"),
    ("WHERE EXISTS ...", "⋉", "semijoin"),
    ("WHERE NOT EXISTS ...", "⊳", "antijoin"),   # ⊳: slide 68 ▷ at operator size
    ("UNION", "∪", "union"),
    ("INTERSECT", "∩", "intersection"),
    ("EXCEPT", "−", "difference"),
]
TOOLKIT_TITLE = "Relational algebra summary"
TOOLKIT_HEADS = ("SQL", "Relational algebra")
TOOLKIT_FOOTER = "Relational algebra works on sets, SQL on multisets."
GLYPH_FONT = "STIX Two Math"

ROW0_Y, ROW_PITCH = 1.88, 0.4
SQL_SIZE, GLYPH_SIZE, NAME_SIZE = 28, 38, 28


def toolkit_card(rows=TOOLKIT_ROWS, title=TOOLKIT_TITLE, heads=TOOLKIT_HEADS, footer=TOOLKIT_FOOTER,
                 color=BLUE, plain=None):
    plain = {"...": DIM, "a, b": FG} if plain is None else plain
    built = []
    for sql, glyph, name in rows:
        s = Mono(sql, SQL_SIZE, color, t2c={k: v for k, v in plain.items() if k in sql})
        g = Text(glyph, font=GLYPH_FONT, font_size=GLYPH_SIZE, color=color)
        n = T(name, NAME_SIZE, FG)
        built.append((s, g, n))
    sql_w = max(s.width for s, _, _ in built)
    name_w = max(n.width for _, _, n in built)
    glyph_w = 0.5
    inner = sql_w + 0.35 + glyph_w + 0.3 + name_w
    left = -inner / 2
    glyph_x = left + sql_w + 0.35 + glyph_w / 2
    name_x = glyph_x + glyph_w / 2 + 0.3
    row_mobs = []
    for i, (s, g, n) in enumerate(built):
        y = ROW0_Y - ROW_PITCH * i
        s.move_to([left, y, 0], aligned_edge=LEFT)
        g.move_to([glyph_x, y, 0])
        n.move_to([name_x, y, 0], aligned_edge=LEFT)
        r = VGroup(s, g, n)
        r.sql, r.glyph, r.name = s, g, n
        row_mobs.append(r)
    width = max(inner, 0) + 0.7
    top, bottom = 3.5, -3.45
    frame = RoundedRectangle(corner_radius=0.2, width=width, height=top - bottom)
    frame.set_stroke(color, 3).set_fill(color, 0.04).move_to([0, (top + bottom) / 2, 0])
    title_t = T(title, 44, FG).move_to([0, 3.02, 0])
    h1 = T(heads[0], 28, DIM).move_to([left, 2.47, 0], aligned_edge=LEFT)
    h2 = T(heads[1], 28, DIM).move_to([glyph_x - glyph_w / 2, 2.47, 0], aligned_edge=LEFT)
    rule = Line([-width / 2 + 0.2, 2.2, 0], [width / 2 - 0.2, 2.2, 0]).set_stroke(DIM, 1.5)
    foot_rule = Line([-width / 2 + 0.2, -2.82, 0], [width / 2 - 0.2, -2.82, 0]).set_stroke(DIM, 1.5)
    foot = T(footer, 30, FG).move_to([0, -3.12, 0])
    rows_g = VGroup(*row_mobs)
    head_g = VGroup(h1, h2)
    g = VGroup(frame, title_t, head_g, rule, rows_g, foot_rule, foot)
    g.frame, g.title, g.heads, g.rule, g.rows = frame, title_t, head_g, rule, rows_g
    g.foot_rule, g.footer = foot_rule, foot
    g.body = VGroup(frame, title_t, head_g, rule, rows_g)
    return g


def row_box(card, i, n=1):
    """Highlight bar behind rows i .. i+n-1 of the card."""
    pitch = ROW_PITCH * card.frame.height / 6.95
    top = card.rows[i].get_center()[1] + pitch / 2
    bot = card.rows[i + n - 1].get_center()[1] - pitch / 2
    w = card.frame.width - 0.3
    r = Rectangle(width=w, height=top - bot)
    r.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12).set_z_index(-1)
    r.move_to([card.frame.get_center()[0], (top + bot) / 2, 0])
    return r


def slot(card, i):
    w = card.frame.width - 0.3
    r = DashedVMobject(Rectangle(width=w, height=ROW_PITCH - 0.06), num_dashes=60)
    r.set_stroke(DIM, 2)
    return r.move_to([card.frame.get_center()[0], card.rows[i].get_center()[1], 0])


def minimap(src, hot, char_w=0.042, pitch=0.11):
    """A thumbnail of a code block: one bar per line (indent and length as in the source),
    hot lines YELLOW, the rest DIM, in a thin frame. No text, so it never reads as tiny code."""
    bars = []
    lines = src.splitlines()
    for i, ln in enumerate(lines):
        body = ln.split("#")[0].rstrip() if "#" in ln else ln.rstrip()
        ind = len(body) - len(body.lstrip())
        n = max(len(body) - ind, 2)
        col = YELLOW if hot(ln) else DIM
        bar = RoundedRectangle(corner_radius=0.025, width=n * char_w, height=0.055)
        bar.set_stroke(width=0).set_fill(col, 0.9 if col == YELLOW else 0.6)
        bar.move_to([ind * char_w, -i * pitch, 0], aligned_edge=LEFT)
        bars.append(bar)
    g = VGroup(*bars)
    fr = RoundedRectangle(corner_radius=0.08, width=g.width + 0.3, height=g.height + 0.24)
    fr.set_stroke(DIM, 1.5).set_fill(BG, 0).move_to(g)
    return VGroup(fr, g)


class ToolkitCard(NarratedScene):
    def construct(self):
        self.card = toolkit_card()
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------ the classic rows
    def clip1(self):
        card = self.card
        with self.say("c3.kit.1") as c:
            self.play(GrowFromCenter(card.frame), *appear(card.title), run_time=1.3)  # early: card title
            self.play(*appear(*card.heads, lag=0.3), GrowFromCenter(card.rule), run_time=1.0)  # early: column heads frame the rows
            c.wait_until("where")
            self.box = row_box(card, 0)
            cues = ["where", "select", "as", "group", "from", "join", "left"]
            for i, cue in enumerate(cues):
                c.wait_until(cue)
                row = card.rows[i]
                nxt = c.until(cues[i + 1]) if i + 1 < len(cues) else c.until()
                rt = min(1.3, 0.6 * nxt)
                box_anim = FadeIn(self.box) if i == 0 else Transform(self.box, row_box(card, i))
                self.play(*appear(row, shift=0.3 * LEFT), box_anim, run_time=rt)
        self.shown = VGroup(card.frame, card.title, card.heads, card.rule, *card.rows[:7])
        settle(self, self.shown)

    # ------------------------------------------------------------ today's rows and the sets
    def clip2(self):
        card = self.card
        loops = load_scene("ch3_s6_loops")
        dx = -1.45
        with self.say("c3.kit.2") as c:
            # the card makes room on the right; two empty slots open
            card.shift(dx * RIGHT)  # moves the not-yet-shown rows too (shown ones animate below)
            self.shown.shift(-dx * RIGHT)
            slots = [slot(card, 7), slot(card, 8)]
            self.play(self.shown.animate.shift(dx * RIGHT), self.box.animate.shift(dx * RIGHT),
                      run_time=min(1.2, 0.5 * c.until("exists")))
            self.play(*appear(*slots, shift=None, lag=0.3), run_time=min(0.8, 0.8 * c.until("exists")))
            c.wait_until("exists")
            right = card.frame.get_right()[0]
            mid = (card.rows[7].get_center()[1] + card.rows[8].get_center()[1]) / 2
            semi = minimap(loops.SEMI_SRC, lambda ln: "append" in ln or "break" in ln)
            semi.move_to([right + 0.35 + semi.width / 2, mid + 0.06 + semi.height / 2, 0])
            anti = minimap(loops.ANTI_SRC, lambda ln: "matched" in ln or "break" in ln)
            anti.move_to([right + 0.35 + anti.width / 2, mid - 0.06 - anti.height / 2, 0])
            self.thumbs = [semi, anti]
            for k, (cue, nxt) in enumerate([("exists", "notexists"), ("notexists", "sets")]):
                c.wait_until(cue)
                i = 7 + k
                row = card.rows[i]
                span = c.until(nxt)
                self.play(*appear(row, shift=0.6 * LEFT), *disappear(slots[k]),
                          Transform(self.box, row_box(card, i)), run_time=min(1.0, 0.45 * span))
                self.play(FlashAround(row, color=YELLOW, time_width=1.5), *appear(self.thumbs[k], shift=None),
                          run_time=min(1.0, 0.35 * span))
            c.wait_until("sets")
            self.play(*appear(*card.rows[9:], shift=0.4 * LEFT, lag=0.2),  # early: the brief brings the three set rows in together
                      Transform(self.box, row_box(card, 9, 3)), run_time=1.5)
            c.wait_until("intersection")
            self.play(*disappear(self.box), run_time=0.8)
        self.remove(self.box)
        settle(self, card.body)
        self.remove(*slots)

    # ------------------------------------------------------------ stacking, and sets vs multisets
    def clip3(self):
        card = self.card
        s1 = load_scene("ch1_s1_hook")
        s4 = load_scene("ch1_s4_setops")
        s5 = load_scene("ch1_s5_derived")
        s35 = load_scene("ch3_s5_semijoin")
        with self.say("c3.kit.3") as c:
            # each operator takes relations and returns one: the glyph column lights
            for m in (card.footer, card.foot_rule):
                m.set_x(0)
            self.play(*disappear(*self.thumbs), card.body.animate.set_x(0), run_time=1.2)
            self.play(FlashAround(VGroup(*[r.glyph for r in card.rows]), color=YELLOW, time_width=1.5),
                      run_time=1.6)
            c.wait_until("that's why")
            # part one's tower of bricks takes the card's place
            tw = s1.tower().scale(0.82)
            tw.move_to([0, 3.45 - tw.height / 2, 0])
            self.play(*during(disappear(card.body), 0, 0.4),
                      *during(appear(*tw, shift=0.15 * DOWN, lag=0.25), 0.4, 1.0),
                      run_time=min(3.0, 0.7 * c.until("sql")))
            c.wait_until("sql")
            code = s5.derived_code(size=27)
            code.move_to([0, tw.get_bottom()[1] - 0.3 - code.height / 2, 0])
            self.play(*appear(code, shift=0.25 * UP), run_time=min(1.5, 0.6 * c.until("multi")))
            c.wait_until("multi")
            # one difference remains: the card comes back, the footer lands
            self.play(*during(disappear(tw, code), 0, 0.45), *during(appear(card.body, shift=None), 0.5, 1.0),
                      run_time=min(1.8, 0.9 * c.until("relational algebra works")))
            c.wait_until("relational algebra works")
            self.play(*appear(card.footer, shift=0.2 * UP), GrowFromCenter(card.foot_rule), run_time=1.0)
            c.wait_until("multisets")
            self.play(*recolor(select(card.footer, "multisets")[0], GOLD), run_time=0.8)
            c.wait_until("union")
            # the claim moves up; below it, the evidence
            v = s4.venn().scale(0.87).move_to([-3.4, -1.3, 0])
            self.play(*during(disappear(card.body, card.foot_rule), 0, 0.4),
                      during([card.footer.animate.scale(1.2).move_to([0, 3.0, 0])], 0.2, 0.8)[0],
                      *during(appear(v, shift=None), 0.5, 1.0), run_time=1.5)
            eq = T("UNION ALL: 2,312 = 621 + 1,691", 30, GOLD).move_to([3.25, -0.3, 0])
            self.play(*appear(eq), run_time=0.9)
            self.play(*s4.fill(v, ["both"]), FlashAround(v.counts["both"], color=GOLD, time_width=1.5),
                      run_time=min(1.0, max(0.4, c.until("zimmer"))))
            c.wait_until("zimmer")
            tag = s35.zimmer_tag(40).move_to([3.25, -1.6, 0])
            self.play(*appear(tag), run_time=1.0)
        self.wait(2.2)
