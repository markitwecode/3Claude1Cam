"""Chapter 5, scene 3: when a copied fact changes (Lana Wachowski's name). Clips c5.update.1 – c5.update.4.

Her former name is never shown: wherever the old value stands there is a DIM bar labelled "old name".

Exports (static, built at ORIGIN):
    recap_r2() -> VGroup, ~7.4 x 2.6: the single BLUE UPDATE row against a 3 x 3 grid of TEAL copies,
        one of them RED. Parts: .update (Mono "UPDATE" 32 BLUE bold), .row (BLUE 3.2 x 0.55 strip,
        stroke 3, fill 0.25), .left (VGroup(update, row)), .copies (VGroup of 9 TEAL cards
        1.0 x 0.7, stroke 2.5, fill 0.08), .bad (copies[5], RED stroke and fill 0.15).
    old_bar(width, height, size) -> VGroup(.rect DIM rounded bar, .label T "old name").
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
D = load_scene("ch4_s3_movie")

NEW = "Lana Wachowski"
PID = "nm0905154"

SQL = """UPDATE people
SET    name = 'Lana Wachowski'
WHERE person_id = 'nm0905154';"""

PERSON = """{
  "person_id": "nm0905154",
  "name": "Lana Wachowski",
  "birthyear": 1965,
  "directed": [/*…*/],
  "produced": [/*…*/],
  "wrote": [/*…*/]
}"""

MATRIX = """{
  "title": "The Matrix",
  "directors": [
    {"name": "Lana Wachowski", /*…*/},
    /*…*/],
  "writers": [
    {"name": "Lilly Wachowski", /*…*/},
    {"name": "Lana Wachowski", /*…*/}],
  /*…*/
}"""

CLOUD = """{
  "title": "Cloud Atlas",
  "directors": [/*…*/
    {"name": "Lana Wachowski", /*…*/},
    /*…*/],
  "writers": [/*…*/
    {"name": "Lana Wachowski", /*…*/},
    /*…*/],
  /*…*/
}"""


# ══ helpers ════════════════════════════════════════════════════════════════════

def old_bar(width, height, size=27):
    rect = (RoundedRectangle(corner_radius=min(0.08, height / 2), width=width, height=height)
            .set_fill(DIM, 0.45).set_stroke(DIM, 1.5))
    label = T("old name", size, FG).move_to(rect)
    g = VGroup(rect, label)
    g.rect, g.label = rect, label
    return g


def cut_names(code, sub='"Lana Wachowski"'):
    """Take every occurrence of sub out of code (call once the code is in place); return
    [(name_glyphs, bar)] in order. The names are standalone (not on screen); each bar sits where its name was."""
    found, n = [], 0
    while True:
        try:
            found.append(code.find(sub, nth=n))
        except ValueError:
            break
        n += 1
    out = []
    for g in found:
        name = VGroup(*g)
        code.text.remove(*g)
        bar = old_bar(max(name.width + 0.06, 1.65), 0.42, 27).move_to(name)
        out.append((name, bar))
    return out


def people_table(center):
    cols = SCH.SCHEMA["people"][0]
    row = [PID, NEW, "1965", "NULL"]
    colors = [[YELLOW, YELLOW, YELLOW, PINK]]
    t = SCH.RowTable("people", cols, [row], colors, size=27, pad=0.16, pitch=0.58)
    t.move_to(center)
    cell = t.rows[0][1]
    t.rows[0].remove(cell)
    bar = old_bar(cell.width + 0.1, 0.44, 27).move_to(cell)
    return t, cell, bar


def strip():
    return RoundedRectangle(corner_radius=0.05, width=1.0, height=0.3).set_stroke(BLUE, 2).set_fill(BLUE, 0.2)


def wall_tiles(cols=15, rows=8, px=0.5, py=0.4):
    tiles = []
    for i in range(rows):
        for j in range(cols):
            t = Rectangle(width=0.38, height=0.28).set_stroke(TEAL, 1.5).set_fill(TEAL, 0.15)
            t.move_to([j * px, -i * py, 0])
            tiles.append(t)
    w = VGroup(*tiles)
    w.cols, w.rows = cols, rows
    return w


def mini_card(center):
    return (RoundedRectangle(corner_radius=0.12, width=3.3, height=0.6)
            .set_stroke(TEAL, 2.5).set_fill(TEAL, 0.06).move_to(center))


def mini_name(center):
    return T(NEW, 28, FG).move_to(center)


def mini_bar(center):
    return old_bar(1.9, 0.44, 27).move_to(center)


def bolt(scale=1.0):
    pts = [(0.12, 0.42), (-0.2, -0.02), (0.02, -0.02), (-0.12, -0.42), (0.22, 0.06), (0.0, 0.06)]
    p = Polygon(*[np.array([x, y, 0]) * scale for x, y in pts])
    return p.set_fill(YELLOW, 1).set_stroke(RED, 2)


def recap_r2():
    upd = Mono("UPDATE", 32, BLUE, weight=BOLD)
    row = Rectangle(width=3.2, height=0.55).set_stroke(BLUE, 3).set_fill(BLUE, 0.25)
    left = VGroup(upd, row).arrange(DOWN, buff=0.3)
    cards = []
    for i in range(3):
        for j in range(3):
            c = (RoundedRectangle(corner_radius=0.12, width=1.0, height=0.7)
                 .set_stroke(TEAL, 2.5).set_fill(TEAL, 0.08).move_to([j * 1.2, -i * 0.9, 0]))
            cards.append(c)
    copies = VGroup(*cards)
    bad = copies[5]
    bad.set_stroke(RED, 2.5).set_fill(RED, 0.15)
    g = VGroup(left, copies).arrange(RIGHT, buff=1.2).move_to(ORIGIN)
    g.update, g.row, g.left, g.copies, g.bad = upd, row, left, copies, bad
    return g


# ══ scene ══════════════════════════════════════════════════════════════════════

class UpdateAnomaly(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)


    # ── 1: one row in the relational database ─────────────────────────────────
    def clip1(self):
        bar0 = old_bar(2.3, 0.62, 36)
        arr0 = Arrow(LEFT * 0.6, RIGHT * 0.6, buff=0, stroke_width=5, color=YELLOW)
        name0 = T(NEW, 48, YELLOW)
        chip = VGroup(bar0, arr0, name0).arrange(RIGHT, buff=0.35).move_to([0, 0.3, 0])
        self.chip = chip

        table, cell, cbar = people_table([0, 1.55, 0])
        code = Code(SQL, size=32)
        code.next_to(table, DOWN, buff=0.55).align_to(table, LEFT)
        one_row = T("1 row", 40, GOLD).next_to(code, RIGHT, buff=0.8)
        box1 = token_box(code.find("name = 'Lana Wachowski'"), code.line(1), height=0.56)
        box2 = token_box(code.find("person_id = 'nm0905154'"), code.line(2), height=0.56)

        hp = Mono("has_position", 28, BLUE, weight=BOLD)
        hp_note = T("person_id only", 28, DIM)
        strips = [strip() for _ in range(17)]
        for k, s in enumerate(strips):
            s.move_to([(k % 9) * 1.12, -(k // 9) * 0.42, 0])
        sg = VGroup(*strips)
        hp.next_to(code, DOWN, buff=0.6).align_to(table, LEFT)
        hp_note.next_to(hp, RIGHT, buff=0.35)
        sg.next_to(hp, DOWN, buff=0.25).align_to(table, LEFT)
        ok = T("already right", 36, GREEN)
        tick = check_mark(GREEN).scale(0.8)
        okg = VGroup(tick, ok).arrange(RIGHT, buff=0.2)
        okg.move_to(hp).align_to(table, RIGHT)

        with self.say("c5.update.1") as c:
            c.wait_until("Suppose")
            self.play(*appear(bar0, shift=None), run_time=1.0)  # early: the bar is the old value, never spoken
            c.wait_until("Lana Wachowski")
            self.play(GrowArrow(arr0), *appear(name0), run_time=1.2)
            c.wait_until("credits")
            self.play(chip.animate.scale(0.75).move_to([0, 3.3, 0]), run_time=1.5)
            c.wait_until("one_row")
            self.play(*appear(table, cbar, lag=0.0), run_time=1.0)
            c.wait_until("single update statement")
            self.play(*appear(code, shift=None), run_time=1.0)
            c.wait_until("setting the name")
            self.play(FadeIn(box1), run_time=0.6)
            c.wait_until("where the person")
            self.play(Transform(box1, box2), run_time=0.8)
            c.wait_until("done")
            self.play(*swap(cbar, cell), FadeOut(box1), run_time=1.2)
            self.play(*appear(one_row), run_time=0.8)
            c.wait_until("refs")
            self.play(*appear(hp, hp_note, shift=None), *appear(*strips, lag=0.04, shift=None), run_time=1.3)
            c.wait_until("already right")
            self.play(*[s.animate.set_stroke(GREEN).set_fill(GREEN, 0.35) for s in strips],
                      *appear(okg), run_time=1.0)

        settle(self, table, add=[cell])
        self.rel = VGroup()
        settle(self, self.rel, add=[table, code, one_row, hp, hp_note, *strips, okg])

    # ── 2: the documents ──────────────────────────────────────────────────────
    def clip2(self):
        # relational summary, left column
        s_lbl = Mono("people", 28, BLUE, weight=BOLD)
        s_row = Rectangle(width=3.4, height=0.56).set_stroke(BLUE, 2.5).set_fill(YELLOW, 0.18)
        s_name = T(NEW, 28, YELLOW).move_to(s_row)
        s_one = T("1 row", 40, GOLD)
        s_ok = VGroup(check_mark(GREEN).scale(0.7), T("credits by ID", 28, GREEN)).arrange(RIGHT, buff=0.15)
        summary = VGroup(s_lbl, VGroup(s_row, s_name), s_one, s_ok).arrange(DOWN, buff=0.35)
        summary.move_to([-4.6, 0.3, 0])
        divider = Line([-2.3, 3.2, 0], [-2.3, -3.2, 0]).set_stroke(DIM, 2)

        pcard = D.doc_card(PERSON, size=26)
        pcard.move_to([2.4, 0.3, 0])
        (pname, pbar), = cut_names(pcard.code)
        p_tile = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.62).set_stroke(TEAL, 2.5).set_fill(TEAL, 0.12)
        p_tick = check_mark(GREEN).scale(0.6).move_to(p_tile)
        p_lbl = T("her document", 28, FG)
        pdone = VGroup(VGroup(p_tile, p_tick), p_lbl).arrange(DOWN, buff=0.15)
        pdone.move_to([0.0, 2.4, 0]).align_to([-1.9, 0, 0], LEFT)

        wall = wall_tiles()
        wall.move_to([2.45, -1.3, 0])
        cols = wall.cols
        m_tile, c_tile = wall[2 * cols + 3], wall[5 * cols + 7]
        x0 = wall.get_left()[0] - 0.2
        x1 = wall[9].get_left()[0] + 0.05
        scan = Line([x0, wall.get_top()[1] + 0.15, 0], [x0, wall.get_bottom()[1] - 0.15, 0]).set_stroke(YELLOW, 4)

        idx_t1 = T("or keep an index:", 30, DIM)
        idx_t2 = VGroup(Mono("person_id", 26, DIM),
                        Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, stroke_width=3, color=DIM,
                              max_tip_length_to_length_ratio=0.35),
                        T("documents", 28, DIM)).arrange(RIGHT, buff=0.15)
        idx_txt = VGroup(idx_t1, idx_t2).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        idx_box = (RoundedRectangle(corner_radius=0.15, width=idx_txt.width + 0.4, height=idx_txt.height + 0.35)
                   .set_stroke(DIM, 2).set_fill(BG, 0))
        idx_txt.move_to(idx_box)
        idx = VGroup(idx_box, idx_txt)
        idx.move_to([4.35, 2.45, 0])

        with self.say("c5.update.2") as c:
            c.wait_until("you start")
            self.play(*during(disappear(self.rel, self.chip), 0.0, 0.45),
                      *during([GrowFromCenter(divider)], 0.2, 0.8),
                      *during(appear(summary, shift=None), 0.45, 0.8),
                      *during(appear(pcard, pbar, lag=0.0, shift=None), 0.6, 1.0), run_time=2.0)
            c.wait_until("find")
            self.play(*swap(pbar, pname), run_time=1.0)
            settle(self, pcard, add=[pname])
            c.wait_until("every movie document")
            self.play(*during(disappear(pcard), 0.0, 0.3), *during(appear(pdone, shift=None), 0.35, 0.65),
                      *during([FadeIn(wall, lag_ratio=0.01)], 0.35, 1.0), run_time=2.2)
            c.wait_until("scan")
            self.play(FadeIn(scan), run_time=0.3)
            rt = 2.4

            def lit_at(tile):
                f = (tile.get_x() - x0) / (x1 - x0)
                a = max(0.0, min(rt - 0.3, f * rt))
                return time_span(tile.animate.set_fill(YELLOW, 0.8).set_stroke(YELLOW, 2), a, a + 0.3)

            self.play(scan.animate(rate_func=linear).set_x(x1), lit_at(m_tile), lit_at(c_tile), run_time=rt)
            c.wait_until("keep an index")
            self.play(FadeOut(scan), *appear(idx), run_time=1.0)

            c.wait_until("matrix")
            band_c = np.array([-4.4, -2.85, 0])
            sweep_clear(self, wall.animate.scale(0.4).move_to(band_c),
                        idx.animate.move_to([3.6, -2.75, 0]), keep=[wall, idx], run_time=1.4)

            mcard = D.doc_card(MATRIX, size=26).move_to([0, 0.9, 0])
            ccard = D.doc_card(CLOUD, size=26).move_to([0, 0.9, 0])
            dirs_k = mcard.code.find('"directors"')
            wri_k = mcard.code.find('"writers"')
            mcuts = cut_names(mcard.code)
            ccuts = cut_names(ccard.code)
            dots = T("…", 60, DIM).next_to(wall, RIGHT, buff=0.35)

            def open_from(card, cuts, tile):
                p = tile.get_center()
                return [FadeIn(card, scale=0.1, target_position=p),
                        *[FadeIn(b, scale=0.1, target_position=p) for _, b in cuts]]

            self.play(*open_from(mcard, mcuts, m_tile), run_time=1.3)

            c.wait_until("as a director")
            self.play(*recolor(dirs_k, YELLOW), FlashAround(mcuts[0][1], color=YELLOW, run_time=1.2),
                      run_time=1.2)
            c.wait_until("as a writer")
            self.play(*recolor(wri_k, YELLOW), FlashAround(mcuts[1][1], color=YELLOW, run_time=1.2),
                      run_time=1.2)

            c.wait_until("rewrite")
            total = c.until(None) - 0.05
            r = total / 2.7
            self.play(*swap(mcuts[0][1], mcuts[0][0]), run_time=0.85 * r)
            self.play(*swap(mcuts[1][1], mcuts[1][0]), run_time=0.65 * r)
            back = [FadeOut(m, scale=0.1, target_position=m_tile.get_center())
                    for m in (mcard, mcuts[0][0], mcuts[1][0])]
            self.play(*during(back, 0.0, 0.45), *during(open_from(ccard, ccuts, c_tile), 0.45, 1.0),
                      *during(appear(dots, shift=None), 0.45, 1.0), run_time=1.2 * r)

        self.ccuts, self.idx = ccuts, idx

    # ── 3: how many, and what can go wrong ────────────────────────────────────
    def clip3(self):
        q = T("how many documents?", 40, GOLD).move_to([3.6, -2.5, 0])
        ex = T("Exercise 19, part 8", 30, DIM).next_to(q, DOWN, buff=0.25)

        xs = (-4.35, 0.0, 4.35)
        ys = (0.45, -0.35, -1.15, -1.95)
        panels, cards, slots = [], [], []
        for x in xs:
            panels.append(RoundedRectangle(corner_radius=0.2, width=3.9, height=5.0)
                          .set_stroke(RED, 3).set_fill(RED, 0.04).move_to([x, -0.5, 0]))
            cards.append([mini_card([x, y, 0]) for y in ys])
            slots.append([mini_bar([x, y, 0]) for y in ys])
        cap1 = T("missed one", 32, RED).move_to([xs[0], 1.4, 0])
        cap2 = VGroup(T("crashed halfway,", 30, RED), T("no transaction", 30, RED)).arrange(
            DOWN, buff=0.12).move_to([xs[1], 1.4, 0])
        cap3 = T("two updates at once", 28, RED).move_to([xs[2], 1.4, 0])

        def cursor(x, y, color=YELLOW):
            return Rectangle(width=3.5, height=0.76).set_stroke(color, 3).move_to([x, y, 0])

        with self.say("c5.update.3") as c:
            (n0, b0), (n1, b1) = self.ccuts
            self.play(*swap(b0, n0), run_time=0.6)
            self.play(*swap(b1, n1), run_time=0.5)
            c.wait_until(own_word=q, cue="count")
            self.play(*swap(self.idx, q), run_time=1.2)
            c.wait_until(own_word=ex, cue="exercise")
            self.play(*appear(ex), run_time=1.0)

            c.wait_until("miss")
            incoming = []
            for p, cs, ss in zip(panels, cards, slots):
                incoming += [FadeIn(p), *[FadeIn(k) for k in cs], *[FadeIn(s) for s in ss]]
            v = np.array([0, 3.0, 0]) - VGroup(q, ex).get_center()
            q2, ex2 = q.copy().shift(v), ex.copy().shift(v)
            sweep_clear(self, *incoming, FadeIn(q2), FadeIn(ex2), run_time=1.6)  # early: the bars are the old value, never spoken

            # panel 1: the application misses one copy
            c.wait_until("might miss")
            cur = cursor(xs[0], ys[0])
            self.play(*appear(cap1), FadeIn(cur), run_time=0.8)
            cur_slots = [list(s) for s in slots]
            for i in range(4):
                anims = [cur.animate.move_to([xs[0], ys[i], 0])] if i else []
                if i != 2:
                    nm = mini_name([xs[0], ys[i], 0])
                    anims += swap(cur_slots[0][i], nm)
                    cur_slots[0][i] = nm
                self.play(*anims, run_time=0.5 if i else 0.6)
            self.play(FadeOut(cur), run_time=0.4)

            # panel 2: crash halfway, no transaction
            c.wait_until("crash")
            cur = cursor(xs[1], ys[0])
            self.play(*appear(cap2), FadeIn(cur), run_time=0.8)
            for i in range(2):
                nm = mini_name([xs[1], ys[i], 0])
                anims = [cur.animate.move_to([xs[1], ys[i], 0])] if i else []
                self.play(*anims, *swap(cur_slots[1][i], nm), run_time=0.6 if i == 0 else 0.5)
                cur_slots[1][i] = nm
            bl = bolt(1.1).move_to([xs[1] + 1.33, ys[2], 0])
            self.play(cur.animate.move_to([xs[1], ys[2], 0]).set_stroke(RED), GrowFromCenter(bl),
                      run_time=0.7)

            # panel 3: two updates at once
            c.wait_until("race")
            ca = cursor(xs[2], ys[0], YELLOW)
            cb = cursor(xs[2], ys[0], PURPLE).scale(1.04)
            self.play(*appear(cap3), FadeIn(ca), run_time=0.8)
            seq = [("a", 0), ("a", 1), ("b", 1), ("a", 2), ("a", 3), ("b", 3)]
            first_b = True
            for who, i in seq:
                pos = [xs[2], ys[i], 0]
                if who == "a":
                    nm = mini_name(pos)
                    anims = [ca.animate.move_to(pos), *swap(cur_slots[2][i], nm)]
                    cur_slots[2][i] = nm
                else:
                    ob = mini_bar(pos)
                    anims = [*swap(cur_slots[2][i], ob)]
                    if first_b:
                        cb.move_to(pos)
                        anims.append(FadeIn(cb))
                        first_b = False
                    else:
                        anims.append(cb.animate.move_to(pos))
                    cur_slots[2][i] = ob
                self.play(*anims, run_time=0.5)  # early: the bar is the old value, never spoken

        self.q, self.ex = q2, ex2
        self.p3 = dict(panels=panels, cards=cards, slots=cur_slots, caps=[cap1, cap2, cap3],
                       extra=[cur, bl, ca, cb])

    # ── 4: the update anomaly ─────────────────────────────────────────────────
    def clip4(self):
        P = self.p3
        olds = [(p, i) for p in range(3) for i in range(4) if hasattr(P["slots"][p][i], "rect")]
        news = [(p, i) for p in range(3) for i in range(4) if (p, i) not in olds]
        head = T("Update anomaly", 52, YELLOW).move_to([0, 3.15, 0])
        nothing = T("nothing in the database prevents it", 36, RED).move_to([0, -3.2, 0])

        with self.say("c5.update.4") as c:
            c.wait_until("new name")
            self.play(*[FlashAround(P["slots"][p][i], color=YELLOW, run_time=1.2) for p, i in news],
                      run_time=1.2)
            c.wait_until("old one")
            self.play(*[P["cards"][p][i].animate.set_stroke(RED) for p, i in olds],
                      *[FlashAround(P["slots"][p][i], color=RED, run_time=1.2) for p, i in olds],
                      run_time=1.2)
            c.wait_until("anomaly")
            self.play(*during(disappear(self.q, self.ex), 0, 0.45), *during(appear(head), 0.45, 1),
                      run_time=1.2)

            c.wait_until("nothing")
            frames = P["panels"] + [k for cs in P["cards"] for k in cs] + P["caps"] + P["extra"]
            floor_y = nothing.get_top()[1] + 0.35      # strings stop clear of the caption
            moves, drift = [], []
            rng = np.random.default_rng(7)
            for p in range(3):
                for i in range(4):
                    s = P["slots"][p][i]
                    x, y = s.get_center()[:2]
                    dx = 0.06 * x + rng.uniform(-0.2, 0.2)
                    dy = 0.08 * (y + 0.75) + (0.12 if (i + p) % 2 else -0.12)
                    v = np.array([x + dx, y + dy + 0.6, 0])
                    d2 = 0.04 * v
                    low = s.get_bottom()[1] + dy + d2[1]
                    if low < floor_y:
                        dy += floor_y - low
                    moves.append(s.animate.shift([dx, dy, 0]))
                    drift.append((s, d2))
            self.play(*during(disappear(*frames), 0.0, 0.45), *during(moves, 0.25, 1.0),
                      *during(appear(nothing), 0.6, 1.0), run_time=1.6)
            c.wait_until("unrelated strings")
            drift = [s.animate(rate_func=linear).shift(d2) for s, d2 in drift]
            self.play(*drift, run_time=min(3.0, c.until(None, floor=0.5)))
