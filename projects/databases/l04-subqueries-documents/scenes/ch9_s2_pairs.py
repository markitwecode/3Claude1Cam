"""Chapter 9, scene 2: Exercise 13, pairs one and two. Clips c9.pairs.1 – c9.pairs.5.

Opens on s1's ex_row(); card 13 grows out of it (s1's big_card(13)), shrinks to a strip on {pairs}
while the four pairs are listed; pair 1 is the hero (right column) next to *the growing database*
(left column); pair 2 is worked on a full-width ON / WHERE table (the db leaves for it). Ends empty.

EXPORTS (static, no updaters; `load_scene("ch9_s2_pairs").<name>()`):
- db(r_rows, s_rows, r_slots=None, s_slots=None): VGroup `.r` `.s`, two DbCards at their fixed place
  (r centred x -5.35, s x -2.75, tops y 2.5, 2.4 wide, 3.0 tall, room for 3 rows each: the cards never
  move). Rows are tuples, None = PINK NULL; `r_slots` lists the slot (0..2) of each row (default 0, 1, ..).
  DbCard: `.box .header .divider .title` (Mono 34 bold) `.tag` (T 28 DIM "first"/"second", under the
  name, inside the header) `.cols[j]` (DIM Mono 28) `.rows[slot]` (VGroup of value Texts, Mono 30)
  `.cell(slot, j)` `.slot_y(slot)` `.col_x(j)` `.make_row(slot, values)` (a new row, not added)
  `.key_line(j)` (an FG underline for column j's name, not added).
- insert_code(src): Code 28 left-aligned at x -6.55, top 3.45 (above the cards); this scene uses
  "INSERT INTO r VALUES\\n  (1, 10);" and "INSERT INTO s VALUES\\n  (10, 99), (10, 5);".
- pair_code(i), i = 1..4: VGroup `.a` `.b` (Code 34, wrapped as SQL usually is; PAIR_SRC), left edge
  x -1.0, `.a` top 2.85, `.b` 0.95 under it (room for an algebra line). strip(i): the collapsed card,
  "Exercise 13 · pair i", centred (2.8, 3.3) over the queries.
- result_card(values, slots=None): DIM header `x`, Mono 30 values, 1.2 wide, its box top at ORIGIN
  (place with `place_top(card, x, top)`); `.box .head .vals .slot_pos(k)`.
- join_card(): the JOIN result card (1, 1) at its place (x -3.6, top -1.25) with YELLOW "JOIN" under it.
- recap_r1(): r and s (real rows), the two YELLOW match lines, IN card `1` and JOIN card `1`, `1`,
  the RED ≠ between them: the left column of clip 3's end.
- recap_r2(): pair 2's ON / WHERE verdict table (headers, the 99 pair kept GREEN, the 5 pair dropped).
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

SCH = load_scene("ch1_s2_schema")
R8 = load_scene("ch3_s8_recap")
S1 = load_scene("ch9_s1_intro")

PAIRS = R8.PAIRS
PAIR_SRC = {
    1: ("SELECT r.x FROM r\nWHERE r.y IN\n  (SELECT s.y FROM s);",
        "SELECT r.x FROM r\nJOIN s ON r.y = s.y;"),
    2: ("SELECT r.x FROM r\nJOIN s ON r.y = s.y\n  AND s.z = 99;",
        "SELECT r.x FROM r\nJOIN s ON r.y = s.y\nWHERE s.z = 99;"),
    3: ("SELECT r.x FROM r\nLEFT JOIN s ON r.y = s.y\n  AND s.z = 99;",
        "SELECT r.x FROM r\nLEFT JOIN s ON r.y = s.y\nWHERE s.z = 99;"),
    4: ("SELECT r.x FROM r\nLEFT JOIN s ON r.y = s.y\nWHERE s.y IS NULL;",
        "SELECT r.x FROM r\nWHERE r.y NOT IN\n  (SELECT s.y FROM s);"),
}
INS_R = "INSERT INTO r VALUES\n  (1, 10);"
INS_S = "INSERT INTO s VALUES\n  (10, 99), (10, 5);"

# ---------------------------------------------------------------- the growing database
DB_X = {"r": -5.35, "s": -2.75}
DB_TOP = 2.5
CARD_W = 2.4
HEAD_H, COLH_H, SLOT_H, PAD = 0.95, 0.45, 0.5, 0.1
COL_DX = 0.6
COLS = {"r": ("x", "y"), "s": ("y", "z")}
TAGS = {"r": "first", "s": "second"}
Q_LEFT, Q_TOP, Q_GAP = -1.0, 2.85, 0.95
STRIP_POS = np.array([2.8, 3.3, 0])
IN_X, JOIN_X, RES_TOP = -5.95, -3.6, -1.25
REL_POS = np.array([-4.78, RES_TOP - COLH_H - SLOT_H / 2, 0])
LAB_Y = -3.15


def value_text(v, size=30):
    return Mono("NULL", size, PINK) if v is None else Mono(str(v), size)


class DbCard(VGroup):
    def __init__(self, name, rows=(), slots=None):
        super().__init__()
        x, top = DB_X[name], DB_TOP
        self.x, self.top = x, top
        h = HEAD_H + COLH_H + 3 * SLOT_H + PAD
        self.box = Rectangle(width=CARD_W, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.box.move_to([x, top - h / 2, 0])
        self.header = Rectangle(width=CARD_W, height=HEAD_H).set_stroke(BLUE, 0).set_fill(BLUE, 0.2)
        self.header.move_to([x, top - HEAD_H / 2, 0])
        self.divider = Line([x - CARD_W / 2, top - HEAD_H, 0], [x + CARD_W / 2, top - HEAD_H, 0]).set_stroke(BLUE, 2)
        yh = top - HEAD_H - COLH_H
        self.hdiv = Line([x - CARD_W / 2, yh, 0], [x + CARD_W / 2, yh, 0]).set_stroke(DIM, 1.5)
        self.vdiv = Line([x, top - HEAD_H, 0], [x, top - h, 0]).set_stroke(DIM, 1.5)
        self.title = Mono(name, 34, weight=BOLD).move_to([x, top - 0.33, 0])
        self.tag = T(TAGS[name], 28, DIM).move_to([x, top - 0.72, 0])
        self.cols, self._bots = [], []
        for j, c in enumerate(COLS[name]):
            t, bot = SCH._placed(c, 28, DIM, NORMAL, top - HEAD_H - COLH_H / 2 - 0.02, cx=self.col_x(j))
            self.cols.append(t)
            self._bots.append(bot)
        self.add(self.header, self.box, self.divider, self.hdiv, self.vdiv, self.title, self.tag, *self.cols)
        self.rows = {}
        slots = slots if slots is not None else list(range(len(rows)))
        for k, vals in zip(slots, rows):
            row = self.make_row(k, vals)
            self.rows[k] = row
            self.add(row)

    def col_x(self, j):
        return self.x + (j - 0.5) * 2 * COL_DX

    def slot_y(self, k):
        return self.top - HEAD_H - COLH_H - SLOT_H * (k + 0.5)

    def make_row(self, k, vals):
        return VGroup(*[value_text(v).move_to([self.col_x(j), self.slot_y(k), 0]) for j, v in enumerate(vals)])

    def cell(self, k, j):
        return self.rows[k][j]

    def key_line(self, j):
        t = self.cols[j]
        y = self._bots[j] + 0.02
        return Line([t.get_left()[0] - 0.05, y, 0], [t.get_right()[0] + 0.05, y, 0]).set_stroke(FG, 2.5)


def db(r_rows=(), s_rows=(), r_slots=None, s_slots=None):
    r = DbCard("r", r_rows, r_slots)
    s = DbCard("s", s_rows, s_slots)
    g = VGroup(r, s)
    g.r, g.s = r, s
    return g


def insert_code(src):
    code = Code(src, size=28)
    code.move_to([0, 0, 0])
    code.shift(np.array([-6.55 - code.get_left()[0], 3.45 - code.get_top()[1], 0]))
    return code


# ---------------------------------------------------------------- queries
def pair_code(i, size=34):
    a = Code(PAIR_SRC[i][0], size=size)
    b = Code(PAIR_SRC[i][1], size=size)
    a.shift(np.array([Q_LEFT - a.get_left()[0], Q_TOP - a.get_top()[1], 0]))
    b.next_to(a, DOWN, buff=Q_GAP, aligned_edge=LEFT)
    g = VGroup(a, b)
    g.a, g.b = a, b
    return g


def strip(i=None):
    lab = VGroup(T("Exercise 13", 30, YELLOW))
    if i is not None:
        lab.add(T(f"· pair {i}", 30))
    lab.arrange(RIGHT, buff=0.18)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.6, height=0.5).set_stroke(DIM, 2)
    lab.move_to(box)
    g = VGroup(box, lab).move_to(STRIP_POS)
    g.box, g.label = box, lab
    return g


# ---------------------------------------------------------------- results
def result_card(values, slots=None):
    n = slots or max(1, len(values))
    h = COLH_H + n * SLOT_H + PAD
    box = Rectangle(width=1.2, height=h).set_stroke(BLUE, 2.5).set_fill(BG, 0)
    box.move_to([0, -h / 2, 0])
    head, _ = SCH._placed("x", 28, DIM, NORMAL, -COLH_H / 2 - 0.02, cx=0)
    div = Line([-0.6, -COLH_H, 0], [0.6, -COLH_H, 0]).set_stroke(DIM, 1.5)
    g = VGroup(box, div, head)
    g.box, g.head = box, head
    g.slot_pos = lambda k: box.get_top() + np.array([0, -COLH_H - SLOT_H * (k + 0.5), 0])
    vals = VGroup(*[value_text(v).move_to(g.slot_pos(k)) for k, v in enumerate(values)])
    g.vals = vals
    g.add(vals)
    return g


def place_top(card, x, top):
    card.shift(np.array([x - card.box.get_x(), top - card.box.get_top()[1], 0]))
    return card


def res_label(text, card):
    return Mono(text, 30, YELLOW).move_to([card.box.get_x(), LAB_Y, 0])


def join_card():
    c = place_top(result_card([1, 1]), JOIN_X, RES_TOP)
    lab = res_label("JOIN", c)
    g = VGroup(c, lab)
    g.card, g.label = c, lab
    return g


def match_lines(d, color=YELLOW):
    r, s = d.r, d.s
    src = r.cell(0, 1).get_right() + 0.1 * RIGHT
    return [Line(src, s.cell(k, 0).get_left() + 0.1 * LEFT).set_stroke(color, 4) for k in (0, 1)]


def recap_r1():
    d = db([(1, 10)], [(10, 99), (10, 5)])
    for m in (d.r.cell(0, 1), d.s.cell(0, 0), d.s.cell(1, 0)):
        m.set_color(YELLOW)
    lines = match_lines(d)
    inc = place_top(result_card([1]), IN_X, RES_TOP)
    jc = join_card()
    rel = MathTex(r"\neq", font_size=60, color=RED).move_to(REL_POS)
    return VGroup(d, *lines, inc, res_label("IN", inc), jc, rel)


# ---------------------------------------------------------------- pair 2's table
ON_X, WH_X = -4.1, 4.1
HEAD_Y, ROW_Y, RES2_TOP = 0.95, (0.2, -0.6, -1.4), -2.05
LABEL_DX = (-1.4, -0.8, 0.1, 0.7)


def pill(text, color=BLUE):
    lab = Mono(text, 28)
    box = RoundedRectangle(corner_radius=0.12, width=lab.width + 0.26, height=0.56).set_stroke(color, 2.5)
    box.set_fill(color, 0)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.lab = box, lab
    return g


def pills(x, y, second="s.z = 99"):
    g = VGroup(pill("r.y = s.y"), pill(second)).arrange(RIGHT, buff=0.12).move_to([x, y, 0])
    return g


def pair_label(vals, y):
    cells = VGroup(*[value_text(v, 28).move_to([dx, y, 0]) for dx, v in zip(LABEL_DX, vals)])
    cells[3].align_to([0.48, 0, 0], LEFT)
    bar = Line([-0.4, y - 0.24, 0], [-0.4, y + 0.24, 0]).set_stroke(DIM, 1.5)
    g = VGroup(cells, bar)
    g.cells = cells
    return g


def paint(p, color, fill=0.15):
    p.box.set_stroke(color).set_fill(color, fill)
    p.lab.set_color(color)
    return p


def judge(p, color):
    return [p.box.animate.set_stroke(color).set_fill(color, 0.15), p.lab.animate.set_color(color)]


def strike(mob):
    return Line(mob.get_left() + 0.15 * LEFT, mob.get_right() + 0.15 * RIGHT).set_stroke(RED, 4)


def recap_r2():
    on_h = Mono("ON", 30, BLUE).move_to([ON_X, HEAD_Y, 0])
    wh_h = Mono("WHERE", 30, BLUE).move_to([WH_X, HEAD_Y, 0])
    g = VGroup(on_h, wh_h)
    for k, z in enumerate((99, 5)):
        lab = pair_label((1, 10, 10, z), ROW_Y[k])
        for x in (ON_X, WH_X):
            ps = pills(x, ROW_Y[k])
            paint(ps[0], GREEN)
            paint(ps[1], GREEN if z == 99 else RED)
            g.add(ps)
        if z == 99:
            lab.cells.set_color(GREEN)
            g.add(lab)
        else:
            lab.set_opacity(0.4)
            g.add(lab, strike(lab))
    return g


class Ch9S2Pairs(NarratedScene):
    def construct(self):
        self.card()
        self.pair1()
        self.test_db()
        self.sets_bags()
        self.pair2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c9.pairs.1
    def card(self):
        with self.say("c9.pairs.1", gap=1.0) as c:
            row = S1.ex_row()
            self.add(row)
            big = S1.big_card(13)
            self.play(ReplacementTransform(row.cards[13].box.copy(), big.box),
                      *during(disappear(row), 0, 0.45),
                      *during(appear(big.text, shift=None), 0.5, 1),  # early: the exercise card, read whole
                      run_time=min(1.5, c.until("the first table")))
            c.wait_until("the first table")
            lines = big.text
            r_ph = select(lines[1], "r with columns x and y")[0]
            self.play(*recolor(r_ph, BLUE), FlashUnder(r_ph, color=BLUE, run_time=1.2),
                      run_time=min(1.2, c.until("the second table")))
            c.wait_until("the second table")
            s_ph = [select(lines[1], "s with columns")[0], select(lines[2], "y and z")[0]]
            self.play(*recolor(s_ph[0], BLUE), *recolor(s_ph[1], BLUE),
                      run_time=min(1.2, c.until("pairs")))
            c.wait_until("pairs")
            st = strip().move_to([0, 3.3, 0])
            self.st = st
            self.play(*during([big.animate.scale(0.25).move_to(st).set_opacity(0)], 0, 0.5),
                      *during(appear(st, shift=None), 0.5, 1),
                      run_time=1.2)
            pairs = VGroup(*[R8.pair_block(i + 1, a, b) for i, (a, b) in enumerate(PAIRS)])
            pairs.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
            R8.fit(pairs, 12.6, 5.2, [0, 0.25, 0])
            self.pairs = pairs
            self.play(*appear(*pairs, lag=0.35), run_time=min(2.0, c.until("if not")))  # early: the four pairs, shown whole then walked
            self.remove(*big.get_family())
            c.wait_until("if not")
            pause = big.pause.scale(0.8).move_to([0, -3.1, 0])
            self.pause = pause
            self.play(*appear(pause, shift=None), run_time=1.0)

    # ------------------------------------------------------------ c9.pairs.2
    def pair1(self):
        with self.say("c9.pairs.2") as c:
            pairs = self.pairs
            st1 = strip(1).move_to([0, 3.3, 0])
            self.play(*disappear(pairs[1], pairs[2], pairs[3], self.pause, pairs[0].num),
                      *during(swap(self.st, st1), 0.2, 1), run_time=1.1)
            self.st = st1
            hero = pair_code(1)
            self.home = hero.get_center()
            hero.scale(1.2).move_to([-0.6, 0.05, 0])
            self.hero = hero
            self.play(*fly(pairs[0].code, hero), *during(disappear(pairs[0].code), 0.4, 0.8),
                      run_time=min(1.6, c.until("the first query")))
            c.wait_until("the first query")
            kw_in = hero.a.find("IN")
            self.play(*recolor(kw_in, YELLOW), FlashAround(kw_in, run_time=1.2, time_width=1.5),
                      run_time=1.2)
            c.wait_until("appears in the second")
            sub = hero.a.line(2)
            self.play(FlashUnder(sub, color=YELLOW, run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("join")
            kw_j = hero.b.find("JOIN")
            self.play(*recolor(kw_j, YELLOW), FlashAround(kw_j, run_time=1.2, time_width=1.5),
                      run_time=min(1.2, c.until("matching on why")))
            c.wait_until("matching on why")
            on = hero.b.find("r.y = s.y")
            self.play(FlashUnder(on, color=YELLOW, run_time=1.2, time_width=1.5), run_time=1.2)
            same = T("same?", 44, YELLOW)
            same.move_to([4.9, (hero.a.get_bottom()[1] + hero.b.get_top()[1]) / 2, 0])
            self.same = same
            c.wait_until(own_word=same)
            self.play(*appear(same), run_time=min(1.0, c.until()))

    # ------------------------------------------------------------ c9.pairs.3
    def test_db(self):
        with self.say("c9.pairs.3") as c:
            hero = self.hero
            d = db()
            self.d = d
            self.play(*during(disappear(self.same), 0, 0.4),
                      *during([hero.animate.scale(1 / 1.2).move_to(self.home),
                               self.st.animate.move_to(STRIP_POS)], 0.1, 0.8),
                      *during(appear(d.r, d.s, lag=0.3, shift=None), 0.5, 1),
                      run_time=min(1.8, c.until("the first table holds")))
            c.wait_until("the first table holds")
            ins = insert_code(INS_R)
            self.play(*appear(ins, shift=None), run_time=0.8)
            row = d.r.make_row(0, (1, 10))
            self.play(*flash([ins.find("1"), ins.find("10")]),
                      *during(appear(row, shift=0.3 * DOWN), 0.3, 1),
                      run_time=min(1.4, c.until("the second holds")))
            settle(self, d.r, add=[row])
            d.r.rows[0] = row
            c.wait_until("the second holds")
            ins2 = insert_code(INS_S)
            self.play(*swap(ins, ins2), run_time=1.0)
            for k, (a, b) in enumerate(((0, 0), (1, 1))):
                row = d.s.make_row(k, (10, 99) if k == 0 else (10, 5))
                self.play(*flash([ins2.find("10", nth=k), ins2.find("99" if k == 0 else "5")]),
                          *during(appear(row, shift=0.3 * DOWN), 0.3, 1), run_time=1.1)
                settle(self, d.s, add=[row])
                d.s.rows[k] = row
            # -- {two}: a join outputs one row per match
            c.wait_until("two")
            lines = match_lines(d)
            self.lines = lines
            jc = join_card()
            jframe = place_top(result_card([], slots=2), JOIN_X, RES_TOP)
            self.play(*during(disappear(ins2), 0, 0.4),
                      *[Create(l) for l in lines],
                      *recolor(d.r.cell(0, 1), YELLOW), *recolor(d.s.cell(0, 0), YELLOW),
                      *recolor(d.s.cell(1, 0), YELLOW), run_time=1.2)
            jlab = res_label("JOIN", jframe)
            self.play(*appear(jframe, jlab, lag=0.2, shift=None), run_time=0.8)
            c.wait_until("so the one comes out twice")
            ones = []
            for k in (0, 1):
                one = value_text(1).move_to(jframe.slot_pos(k))
                self.play(VShowPassingFlash(lines[k].copy().set_stroke(YELLOW, 8), time_width=0.5),
                          *fly(d.r.cell(0, 0), one, arc=-0.9 * PI), run_time=1.1 if k == 0 else 0.9)
                ones.append(one)
            settle(self, jframe, add=ones)
            jframe.vals = VGroup(*ones)
            self.jframe, self.jlab = jframe, jlab
            # -- {once}: IN only asks whether a match exists
            c.wait_until("once")
            ok = VGroup(check_mark(), T("a match exists", 30, GREEN)).arrange(RIGHT, buff=0.25)
            ok.move_to([0, 3.1, 0]).align_to([-6.55, 0, 0], LEFT)
            self.ok = ok
            self.play(*appear(ok), run_time=0.9)
            c.wait_until("so the one comes out once")
            inc = place_top(result_card([], slots=1), IN_X, RES_TOP)
            inlab = res_label("IN", inc)
            self.play(*appear(inc, inlab, lag=0.2, shift=None), run_time=0.7)
            one = value_text(1).move_to(inc.slot_pos(0))
            self.play(*fly(d.r.cell(0, 0), one, arc=-PI), run_time=1.2)
            settle(self, inc, add=[one])
            inc.vals = VGroup(one)
            self.inc, self.inlab = inc, inlab
            # -- that's a semijoin
            c.wait_until("semijoin")
            mid_a = (hero.a.get_bottom()[1] + hero.b.get_top()[1]) / 2
            alg_a = MathTex(r"\pi_x(r \ltimes_y s)", font_size=44, color=BLUE)
            alg_a.move_to([0, mid_a, 0]).align_to([Q_LEFT, 0, 0], LEFT)
            alg_b = MathTex(r"\pi_x(r \bowtie_y s)", font_size=44, color=BLUE)
            alg_b.next_to(hero.b, DOWN, buff=0.3, aligned_edge=LEFT)
            semi = T("semijoin", 30, DIM).next_to(alg_a, RIGHT, buff=0.45)
            self.algs = [alg_a, alg_b, semi]
            self.play(*appear(alg_a, alg_b, semi, lag=0.25), run_time=min(1.4, c.until("differ")))
            c.wait_until("differ")
            rel = MathTex(r"\neq", font_size=60, color=RED).move_to(REL_POS)
            rows3 = T("3 rows", 30, GOLD).move_to([-2.6, -0.9, 0])
            self.rel, self.rows3 = rel, rows3
            self.play(*appear(rel, rows3, lag=0.3), run_time=1.0)

    # ------------------------------------------------------------ c9.pairs.4
    def sets_bags(self):
        d, inc, jf = self.d, self.inc, self.jframe
        with self.say("c9.pairs.4", gap=0.0) as c:
            # {sets}: { 1 } = { 1 }
            braces = []
            for card in (inc, jf):
                p = card.slot_pos(0)
                braces += [MathTex(r"\{", font_size=48, color=GREEN).move_to(p + 0.38 * LEFT),
                           MathTex(r"\}", font_size=48, color=GREEN).move_to(p + 0.38 * RIGHT)]
            eq = MathTex("=", font_size=60, color=GREEN).move_to(REL_POS)
            self.play(*set_alpha([jf.vals[1]], DIMMED), *appear(*braces, shift=None),
                      *during(swap(self.rel, eq), 0.3, 1), run_time=min(1.5, c.until("bags")))
            c.wait_until("bags")
            # {bags}: the second copy counts
            neq = MathTex(r"\neq", font_size=60, color=RED).move_to(REL_POS)
            x2 = MathTex(r"\times 2", font_size=44, color=GOLD)
            x2.move_to([jf.box.get_right()[0] + 0.5, jf.box.get_y() - COLH_H / 2 + 0.05, 0])
            self.play(*[FadeOut(b, shift=0.4 * DOWN) for b in braces], *set_alpha([jf.vals[1]], 1),
                      run_time=1.0)
            self.play(*recolor(jf.vals[0], GOLD), *recolor(jf.vals[1], GOLD),
                      FlashAround(jf.vals, color=GOLD, run_time=1.2, time_width=1.5),
                      *during(appear(x2, shift=None), 0.4, 1), *during(swap(eq, neq), 0.3, 1),
                      run_time=1.4)
            c.wait_until("key")
            # {key}: y is a key of s
            key = d.s.key_line(0)
            self.play(GrowFromCenter(key), run_time=1.0)
            c.wait_until("at most one match")
            self.play(*set_alpha([d.s.cell(1, 0), self.lines[1]], DIMMED), run_time=1.0)
            eq2 = MathTex("=", font_size=60, color=GREEN).move_to(REL_POS)
            self.play(*set_alpha([jf.vals[1]], DIMMED), *recolor(jf.vals[0], FG), *recolor(jf.vals[1], FG),
                      *during(disappear(x2), 0, 0.5), *during(swap(neq, eq2), 0.3, 1),
                      run_time=1.3)
            c.wait_until()
        # back to the real tables
        neq2 = MathTex(r"\neq", font_size=60, color=RED).move_to(REL_POS)
        self.play(*disappear(key), *set_alpha([d.s.cell(1, 0), self.lines[1], jf.vals[1]], 1),
                  *during(swap(eq2, neq2), 0.3, 1), run_time=1.0)
        self.wait(0.6)

    # ------------------------------------------------------------ c9.pairs.5
    def pair2(self):
        with self.say("c9.pairs.5") as c:
            a = Code(PAIR_SRC[2][0], size=30)
            b = Code(PAIR_SRC[2][1], size=30)
            a.shift(np.array([ON_X - a.get_x(), 2.85 - a.get_top()[1], 0]))
            b.shift(np.array([WH_X - b.get_x(), 2.85 - b.get_top()[1], 0]))
            st2 = strip(2).move_to([0, 3.3, 0])
            sweep_clear(self, *appear(a, b, lag=0.3), keep=[self.st], run_time=1.6)
            self.play(*swap(self.st, st2), run_time=1.0)
            c.wait_until("on clause")
            g_on = [a.find("ON"), a.find("AND s.z = 99")]
            self.play(*recolor(g_on[0], YELLOW), *recolor(g_on[1], YELLOW),
                      FlashUnder(g_on[1], run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("where clause")
            g_wh = b.find("WHERE s.z = 99")
            self.play(*recolor(g_wh, YELLOW), FlashUnder(g_wh, run_time=1.2, time_width=1.5),
                      run_time=min(1.2, c.until("ask2")))
            c.wait_until("ask2")
            mid = a.get_y()
            q = T("?", 60, YELLOW).move_to([0, mid, 0])
            self.play(*appear(q), run_time=0.9)
            c.wait_until("same")
            eq = MathTex("=", font_size=80, color=GREEN).move_to([0, mid, 0])
            self.play(*swap(q, eq), run_time=1.0)
            # {why}: the pairs of rows from r × s, each with its two tests
            c.wait_until("why")
            on_h = Mono("ON", 30, BLUE).move_to([ON_X, HEAD_Y, 0])
            wh_h = Mono("WHERE", 30, BLUE).move_to([WH_X, HEAD_Y, 0])
            labs = [pair_label((1, 10, 10, z), ROW_Y[k]) for k, z in enumerate((99, 5))]
            on_p = [pills(ON_X, ROW_Y[k]) for k in (0, 1)]
            wh_p = [pills(WH_X, ROW_Y[k]) for k in (0, 1)]
            self.play(*appear(on_h, wh_h, *labs, lag=0.2), run_time=1.2)
            self.play(*appear(on_p[0], wh_p[0], on_p[1], wh_p[1], lag=0.2, shift=None), run_time=1.2)
            c.wait_until("tested together")
            self.play(*judge(on_p[0][0], GREEN), *judge(on_p[0][1], GREEN),
                      *judge(on_p[1][0], GREEN), *judge(on_p[1][1], RED), run_time=1.0)
            c.wait_until("one after the other")
            self.play(*judge(wh_p[0][0], GREEN), *judge(wh_p[1][0], GREEN), run_time=0.8)
            self.play(*judge(wh_p[0][1], GREEN), *judge(wh_p[1][1], RED), run_time=0.8)
            c.wait_until("a pair survives")
            cut = strike(labs[1])
            self.play(*recolor(labs[0].cells, GREEN), Create(cut),
                      *set_alpha([labs[1]], 0.4), run_time=1.0)
            r_on = place_top(result_card([1]), ON_X, RES2_TOP)
            r_wh = place_top(result_card([1]), WH_X, RES2_TOP)
            eq_r = MathTex("=", font_size=60, color=GREEN).move_to([0, r_on.slot_pos(0)[1], 0])
            self.play(*appear(r_on, r_wh, eq_r, lag=0.25, shift=None), run_time=min(1.2, c.until("null")))
            # {null}: a ghost third pair
            c.wait_until("null")
            ghost = pair_label((1, 10, 10, None), ROW_Y[2])
            g_on = pills(ON_X, ROW_Y[2], "NULL = 99")
            g_wh = pills(WH_X, ROW_Y[2], "NULL = 99")
            for ps in (g_on, g_wh):
                paint(ps[0], GREEN)
                paint(ps[1], PINK)
            gg = VGroup(ghost, g_on, g_wh).set_opacity(0.75)
            for ps in (g_on, g_wh):
                ps[0].box.set_fill(opacity=0.12)
                ps[1].box.set_fill(opacity=0.12)
            self.play(*appear(gg, shift=None), run_time=1.2)
            c.wait_until("dropped either way")
            cut2 = strike(ghost)
            self.play(Create(cut2), *set_alpha([ghost], 0.4), run_time=0.9)
