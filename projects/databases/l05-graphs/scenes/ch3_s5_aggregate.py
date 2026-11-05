"""Chapter 3, scene 5: counting without GROUP BY. Clips c3.count.1 – c3.count.5.

Recap helpers (module level):
  potter_collapse() -> VGroup(.header, .rule, .rows, .result, .yc)
      .rows[i]: VGroup with .icon (PINK-BLUE-PINK placement), .p1, .p2, .title, .year
      .result:  VGroup(.p1, .p2, .count)  "Daniel Radcliffe | Emma Watson | 8" (8 GOLD)
      .yc:      y the rows collapse to (the result row's y)
  return_rule() -> VGroup(.la, .lb, .keys, .keys_label, .agg, .agg_label)
      .la "RETURN p1.name AS name1, p2.name AS name2,"  .lb "count(*) AS movies"
      .keys: two YELLOW braces (grouping keys), .agg: GOLD brace under count(*)
  top5_table() -> the Slide 106 result table in cypher-shell style (.rows, .hdr, .rule, .seps)
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
from lib.style import *  # noqa: E402,F403

PAT1 = "MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)"
WHERE = "WHERE p1.person_id < p2.person_id"
Q0 = f"{PAT1}\n{WHERE}\nRETURN p1.name, p2.name, m.title"
RET2 = "RETURN p1.name AS name1, p2.name AS name2,\n       count(*) AS movies"
Q1 = f"{PAT1}\n{WHERE}\nRETURN p1.name, p2.name,\n       count(*) AS movies"
ORDER = "ORDER BY movies DESC, name1, name2\nLIMIT 5;"
Q2 = f"{PAT1}\n{WHERE}\n{RET2}\n{ORDER}"
Q3 = ("MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie)\n"
      "      <-[:ACTED_IN]- (p2:Person)\n"
      f"{WHERE}\n{RET2}\n{ORDER}")

TOP5 = [("Daniel Radcliffe", "Emma Watson", "8"),
        ("Rupert Grint", "Daniel Radcliffe", "8"),
        ("Rupert Grint", "Emma Watson", "8"),
        ("Johnny Depp", "Helena Bonham Carter", "7"),
        ("Robert Downey Jr.", "Scarlett Johansson", "7")]
ROW6 = ("Tom Cruise", "Ving Rhames", "7")

HP = [("Harry Potter and the Sorcerer's Stone", "2001"),
      ("… and the Chamber of Secrets", "2002"),
      ("… and the Prisoner of Azkaban", "2004"),
      ("… and the Goblet of Fire", "2005"),
      ("… and the Order of the Phoenix", "2007"),
      ("… and the Half-Blood Prince", "2009"),
      ("… and the Deathly Hallows: Part 1", "2010"),
      ("… and the Deathly Hallows: Part 2", "2011")]

SCREAM = [("David Arquette", "Courteney Cox", "Scream", "2"),
          ("Neve Campbell", "Courteney Cox", "Scream", "2"),
          ("Neve Campbell", "David Arquette", "Scream", "2"),
          ("Tia Carrere", "Chris Sanders", "Lilo & Stitch", "2"),
          ("'Poo' Ram", "Aparna Balamurali", "Soorarai Pottru", "1")]


def paint(q):
    for s in ("AS name1", "AS name2"):
        try:
            q.find(s).set_color(YELLOW)
        except ValueError:
            pass
    try:
        q.find("count(*) AS movies").set_color(GOLD)
    except ValueError:
        pass
    return q


def grid(header, rows, size=30, hsize=28, pitch=0.85, gap=0.7, x=0.0, top=2.6, first=0.75):
    """Left-aligned table, last column numeric (GOLD, centred under its header)."""
    n = len(header)
    hdr = [Mono(h, size=hsize, color=DIM) for h in header]
    cells = [[T(v, size=size, color=GOLD if j == n - 1 else FG) for j, v in enumerate(r)] for r in rows]
    widths = [max([hdr[j].width] + [c[j].width for c in cells]) for j in range(n)]
    xs, acc = [], 0.0
    for w in widths:
        xs.append(acc)
        acc += w + gap
    total = acc - gap
    for j, h in enumerate(hdr):
        if j == n - 1:
            h.move_to([xs[j] + widths[j] / 2, 0, 0]).align_to([0, top, 0], UP)
        else:
            h.move_to([xs[j] + h.width / 2, 0, 0]).align_to([0, top, 0], UP)
    rule = Line([-0.1, top - 0.45, 0], [total + 0.1, top - 0.45, 0], color=DIM, stroke_width=2)
    row_groups = []
    for i, r in enumerate(cells):
        ytop = top - first - pitch * i
        for j, c in enumerate(r):
            cx = xs[j] + widths[j] / 2 if j == n - 1 else xs[j] + c.width / 2
            c.move_to([cx, 0, 0]).align_to([0, ytop, 0], UP)
        g = VGroup(*r)
        g.cells = r
        row_groups.append(g)
    hdr_g = VGroup(*hdr)
    tab = VGroup(hdr_g, rule, *row_groups)
    tab.shift((x - total / 2) * RIGHT)
    tab.hdr, tab.rule, tab.rows, tab.xs = hdr_g, rule, row_groups, [v + x - total / 2 for v in xs]
    tab.pitch = pitch
    return tab


def shell_grid(header, rows, size=28, pitch=0.85, gap=0.5, left=-6.55, top=2.6, first=0.75,
               max_w=13.0):
    """cypher-shell output as in scene 3: Mono cells, DIM header, a rule under it, DIM column
    lines; last column numeric (GOLD, centred under its header). Left edge at `left` (centred
    if None). Parts .hdr .rule .seps .rows[i] (.cells) .xs .pitch."""
    n = len(header)
    hdr = [Mono(h, size=size, color=DIM) for h in header]
    cells = [[Mono(v, size=size, color=GOLD if j == n - 1 else FG) for j, v in enumerate(r)]
             for r in rows]
    widths = [max([hdr[j].width] + [c[j].width for c in cells]) for j in range(n)]
    xs, acc = [], 0.0
    for w in widths:
        xs.append(acc)
        acc += w + gap
    total = acc - gap
    for j, h in enumerate(hdr):
        cx = xs[j] + widths[j] / 2 if j == n - 1 else xs[j] + h.width / 2
        h.move_to([cx, 0, 0]).align_to([0, top, 0], UP)
    rule = Line([-0.15, top - 0.45, 0], [total + 0.15, top - 0.45, 0], color=DIM, stroke_width=2)
    row_groups = []
    for i, r in enumerate(cells):
        ytop = top - first - pitch * i
        for j, c in enumerate(r):
            cx = xs[j] + widths[j] / 2 if j == n - 1 else xs[j] + c.width / 2
            c.move_to([cx, 0, 0]).align_to([0, ytop, 0], UP)
        g = VGroup(*r)
        g.cells = r
        row_groups.append(g)
    bottom = top - first - pitch * (len(rows) - 1) - 0.42
    seps = [Line([xs[j] - gap / 2, top + 0.12, 0], [xs[j] - gap / 2, bottom, 0], color=DIM,
                 stroke_width=2) for j in range(1, n)]
    hdr_g = VGroup(*hdr)
    tab = VGroup(hdr_g, rule, *seps, *row_groups)
    k = min(1.0, max_w / tab.width)
    if k < 1.0:
        tab.scale(k, about_point=[0, top, 0])
    dx = (left - tab.get_left()[0]) if left is not None else -tab.get_x()
    tab.shift(dx * RIGHT)
    tab.hdr, tab.rule, tab.seps, tab.rows = hdr_g, rule, seps, row_groups
    tab.xs = [rule.get_left()[0] + 0.15 * k + v * k for v in xs]
    tab.pitch = pitch
    return tab


def top5_table(pitch=0.85, top=2.7, rows=TOP5, gap=0.5):
    return shell_grid(["name1", "name2", "movies"], rows, pitch=pitch, top=top, gap=gap)


def placement_icon():
    pts = [LEFT * 0.4, ORIGIN, RIGHT * 0.4]
    dots = [Circle(radius=0.12, color=c, stroke_width=3).set_fill(c, 0.35).move_to(p)
            for c, p in zip((PINK, BLUE, PINK), pts)]
    lines = [Line(pts[0] + RIGHT * 0.12, pts[1] + LEFT * 0.12, stroke_width=2, color=FG),
             Line(pts[2] + LEFT * 0.12, pts[1] + RIGHT * 0.12, stroke_width=2, color=FG)]
    return VGroup(*lines, *dots)


def potter_collapse():
    rows = [("Daniel Radcliffe", "Emma Watson", t, y) for t, y in HP]
    tab = grid(["p1.name", "p2.name", "m.title", "m.year"], rows, size=28, pitch=0.62, gap=0.4,
               x=0.6, top=3.0, first=0.68)
    # last column (year) is GOLD by grid's rule; years are values, keep them FG
    for r in tab.rows:
        r.cells[3].set_color(FG)
    out_rows = []
    for r in tab.rows:
        icon = placement_icon().next_to(r.cells[0], LEFT, buff=0.35)
        icon.set_y(r.cells[0].get_y())
        row = VGroup(icon, *r.cells)
        row.icon, row.p1, row.p2, row.title, row.year = icon, *r.cells
        out_rows.append(row)
    whole = VGroup(tab.hdr, tab.rule, *out_rows)
    if whole.width > 13.0:
        whole.scale(13.0 / whole.width)
    whole.set_x(0)
    yc = (out_rows[0].p1.get_y() + out_rows[-1].p1.get_y()) / 2
    r0 = out_rows[0]
    rp1 = T("Daniel Radcliffe", size=34)
    rp2 = T("Emma Watson", size=34)
    cnt = T("8", size=44, color=GOLD)
    result = VGroup(rp1, rp2, cnt).arrange(RIGHT, buff=0.7).move_to([0, yc, 0])
    cnt.align_to(rp1, DOWN)
    result.p1, result.p2, result.count = rp1, rp2, cnt
    g = VGroup(tab.hdr, tab.rule, *out_rows)
    g.header, g.rule, g.rows, g.result, g.yc = tab.hdr, tab.rule, out_rows, result, yc
    return g


def return_rule(y=2.0, size=32):
    la = paint(Code("RETURN p1.name AS name1, p2.name AS name2,", size=size))
    la.move_to([0, y, 0])
    lb = paint(Code("count(*) AS movies", size=size))
    lb.move_to([0, y - 1.75, 0]).align_to(la.find("p1.name"), LEFT)
    k1 = la.find("p1.name AS name1")
    k2 = la.find("p2.name AS name2")
    keys = VGroup(*[span_brace(k.get_left(), k.get_right(), DOWN, color=YELLOW, buff=0.15)
                    for k in (k1, k2)])
    for b in keys:
        b.align_to(la, DOWN).shift(DOWN * 0.15 + DOWN * b.height)
    keys_label = T("grouping keys", size=30, color=YELLOW).next_to(keys, DOWN, buff=0.12)
    keys_label.set_x(keys.get_x())
    agg = brace_under(lb.find("count(*)"), lb, GOLD)
    agg_label = T("aggregate", size=30, color=GOLD).next_to(agg, DOWN, buff=0.12)
    g = VGroup(la, lb, keys, keys_label, agg, agg_label)
    g.la, g.lb, g.keys, g.keys_label, g.agg, g.agg_label = la, lb, keys, keys_label, agg, agg_label
    return g


def brace_under(glyphs, line, color):
    b = span_brace(glyphs.get_left(), glyphs.get_right(), DOWN, color=color, buff=0.15)
    b.move_to([b.get_x(), line.get_bottom()[1] - 0.15 - b.height / 2, 0])
    return b


def vertex(lines, color, r=0.62, size=28):
    circ = Circle(radius=r, color=color, stroke_width=4).set_fill(color, 0.12)
    lab = VGroup(*[T(t, size=size) for t in lines.split("\n")]).arrange(DOWN, buff=0.1).move_to(circ)
    v = VGroup(circ, lab)
    v.circ, v.lab = circ, lab
    return v


class Aggregate(NarratedScene):
    def construct(self):
        q3 = self.clip1()
        top = self.clip2(q3)
        res = self.clip3(top)
        rule = self.clip4(res)
        self.clip5(rule)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        q0 = Code(Q0, size=22.8).move_to(ORIGIN)
        q1 = paint(Code(Q1, size=22.8)).move_to(ORIGIN)
        q2 = paint(Code(Q2, size=22.8)).move_to(ORIGIN)
        q3 = paint(Code(Q3, size=30)).move_to(ORIGIN)
        with self.say("c3.count.1") as c:
            self.play(*appear(q0, shift=None), run_time=1.2)  # early: the query the scene starts from
            c.wait_until("replace")
            self.play(*edit(q0, q1), run_time=min(2.0, 0.8 * c.until("sort")))
            c.wait_until("sort")
            self.play(*edit(q1, q2), run_time=min(1.8, 0.8 * c.until("slide")))
            c.wait_until("slide")
            self.play(*swap(q2, q3, shift=None), run_time=min(1.4, 0.5 * c.until()))
        return q3

    # ------------------------------------------------------------------ clip 2
    def clip2(self, q3):
        tab = top5_table()
        with self.say("c3.count.2") as c:
            sweep_clear(self, *appear(tab.hdr, tab.rule, *tab.seps, *tab.rows[:3], lag=0.2, shift=None),  # early: result table shown whole, then read
                        run_time=min(2.0, c.until("trio")))
            c.wait_until("trio")
            hp = VGroup(*tab.rows[:3])
            br = Brace(hp, RIGHT, color=YELLOW, buff=0.25)
            br.set_x(tab.get_right()[0] + 0.45).match_y(hp)
            lab = T("Harry\nPotter", size=30, color=YELLOW).next_to(br, RIGHT, buff=0.2)
            c.wait_until("harry potter")
            self.play(GrowFromCenter(br), *appear(lab), run_time=1.0)
            c.wait_until("seven")
            self.play(*appear(*tab.rows[3:], lag=0.4, shift=None), run_time=1.4)  # early: rows read after
            c.wait_until("prominent")
            foot = T("only the most prominent cast is stored", size=28, color=DIM)
            foot.move_to([tab.get_x(), -2.95, 0])
            self.play(*appear(foot), run_time=1.0)
        tab.br, tab.lab, tab.foot = br, lab, foot
        return tab

    # ------------------------------------------------------------------ clip 3
    def clip3(self, tab):
        pot = potter_collapse()
        with self.say("c3.count.3") as c:
            c.wait_until("group by")
            sql = Code("GROUP BY name1, name2", size=32, lang="sql")
            sqll = T("SQL:", size=30, color=DIM)
            grp = VGroup(sqll, sql).arrange(RIGHT, buff=0.3).move_to(tab.foot)
            self.play(*swap(tab.foot, grp), run_time=1.2)
            c.wait_until("cypher has none")
            x = Cross(sql, stroke_width=6, scale_factor=0.9)
            self.play(Create(x), run_time=0.8)
            c.wait_until("how")
            qn = T("How does it know what to count?", size=40, color=YELLOW).move_to([tab.get_x(), 0.4, 0])
            self.play(*disappear(tab.hdr, tab.rule, *tab.seps, *tab.rows, tab.br, tab.lab), run_time=0.8)
            self.play(*appear(qn), run_time=0.9)
            c.wait_until("before")
            sweep_clear(self, *appear(pot.header, pot.rule, *pot.rows, lag=0.1, shift=None),  # early: the rows shown whole, then read
                        run_time=min(2.4, c.until("radcliffe and watson")))
            c.wait_until("placement")
            self.play(LaggedStart(*flash([r.icon for r in pot.rows]), lag_ratio=0.12), run_time=1.6)
            c.wait_until("sensible")
            self.play(*set_alpha([m for r in pot.rows for m in (r.icon, r.title, r.year)], DIMMED),
                      FadeOut(pot.header[2:]), run_time=1.0)
            c.wait_until("share both names")
            self.play(*recolor([m for r in pot.rows for m in (r.p1, r.p2)], YELLOW), run_time=1.0)
            c.wait_until("collapse")
            rt = c.until()
            anims = []
            for i, r in enumerate(pot.rows):
                for m in (r.p1, r.p2):
                    anims.append(m.animate.set_y(pot.yc - (i - 3.5) * 0.34))
                anims += [FadeOut(r.icon), FadeOut(r.title), FadeOut(r.year)]
            self.play(*anims, run_time=min(1.4, 0.45 * rt))
            self.play(*during(disappear(*pot.rows), 0, 0.45),
                      *during(appear(pot.result, shift=None), 0.5, 1), run_time=min(1.0, 0.35 * rt))
        return pot

    # ------------------------------------------------------------------ clip 4
    def clip4(self, pot):
        rule = return_rule()
        with self.say("c3.count.4") as c:
            res0 = pot.result
            k = 28 / 34
            sweep_clear(self, res0.animate.scale(k).move_to([0, -3.05, 0]),
                        *appear(rule.la, rule.lb, lag=0.3, shift=None), keep=[res0], run_time=1.6)
            c.wait_until("aggregates")
            self.play(GrowFromCenter(rule.agg), *appear(rule.agg_label), run_time=1.0)
            c.wait_until("grouping key")
            self.play(*[GrowFromCenter(b) for b in rule.keys], *appear(rule.keys_label), run_time=1.0)
            c.wait_until("twice")
            ghost = Code("GROUP BY p1.name, p2.name", size=32, lang="sql")
            ghost.set_opacity(0.6).align_to(rule.la, LEFT).set_y(-1.85)
            gl = T("SQL: keys twice", size=30, color=DIM).next_to(ghost, RIGHT, buff=0.6)
            self.play(*appear(ghost, shift=None), run_time=1.0)
            self.play(*flash([rule.la.find("p1.name"), rule.la.find("p2.name"),
                              ghost.find("p1.name"), ghost.find("p2.name")]),
                      *appear(gl), run_time=1.5)
            c.wait_until("reads")
            imp = T("implied", size=30, color=DIM, slant=ITALIC).move_to(gl).align_to(gl, LEFT)
            self.play(*swap(gl, imp), *set_alpha([ghost], 0.3), run_time=1.2)
            c.wait_until("test")
            self.play(*disappear(imp, ghost), run_time=0.7)
            lb2 = paint(Code("m.title, count(*) AS movies", size=32)).move_to(rule.lb).align_to(rule.lb, LEFT)
            agg2 = brace_under(lb2.find("count(*)"), lb2, GOLD)
            self.play(*edit(rule.lb, lb2), Transform(rule.agg, agg2),
                      rule.agg_label.animate.next_to(agg2, DOWN, buff=0.12),
                      run_time=min(1.6, 0.6 * c.until("split")))
            kt = brace_under(lb2.find("m.title"), lb2, YELLOW)
            self.play(GrowFromCenter(kt), run_time=0.8)
            c.wait_until("split")
            self.play(*disappear(rule.keys_label, rule.agg_label, res0), run_time=0.7)
            P = np.array([0, 3.4, 0])
            d = P - np.array([0, rule.la.get_top()[1], 0])
            movers = [rule.la, lb2, rule.agg, kt, *rule.keys]
            self.play(*[m.animate.shift(d).scale(0.875, about_point=P) for m in movers], run_time=1.2)
            res = shell_grid(["name1", "name2", "m.title", "movies"], SCREAM, pitch=0.48, gap=0.45, max_w=13.2,
                             left=None, top=lb2.get_bottom()[1] - 0.72, first=0.55)
            self.play(*appear(res.hdr, res.rule, *res.seps, *res.rows, lag=0.15, shift=None),  # early: table, then read
                      run_time=min(1.8, max(0.6, c.until() - 0.2)))
        rule.lb2, rule.kt, rule.res = lb2, kt, res
        return rule

    # ------------------------------------------------------------------ clip 5
    def clip5(self, rule):
        res = rule.res
        with self.say("c3.count.5") as c:
            twos = [r.cells[3] for r in res.rows[:4]]
            self.play(*flash(twos, color=GOLD), run_time=1.5)
            self.play(*set_alpha([res.rows[4]], 0.4), run_time=0.8)
            y = -2.78
            s1 = vertex("Scream\n1996", BLUE, r=0.68).move_to([-0.6, y, 0])
            s2 = vertex("Scream\n2022", BLUE, r=0.68).move_to([4.6, y, 0])
            c.wait_until("nineteen ninety-six")
            self.play(*appear(s1, shift=None), run_time=0.8)
            c.wait_until("twenty twenty-two")
            self.play(*appear(s2, shift=None), run_time=0.8)
            c.wait_until("value")
            box = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.55, color=YELLOW,
                                   stroke_width=3).move_to([3.0, y, 0])
            lab = T("the key is the value", size=32, color=YELLOW).next_to(box, LEFT, buff=0.5)
            self.play(s1.animate.move_to([2.22, y, 0]), s2.animate.move_to([3.78, y, 0]),
                      time_span(FadeIn(box), 0.6, 1.4), *during(appear(lab), 0.5, 1), run_time=1.6)
            c.wait_until("grint")
            tab = top5_table(pitch=1.0, top=3.4, gap=0.4)
            sweep_clear(self, *appear(tab.hdr, tab.rule, *tab.seps, *tab.rows, lag=0.1, shift=None),
                        run_time=min(1.6, c.until("smaller one")))
            ids = []
            for i, (k1, k2) in ((1, ("nm0342488", "nm0705356")), (2, ("nm0342488", "nm0914612"))):
                r = tab.rows[i]
                ids.append(Mono(k1, size=28, color=YELLOW).next_to(r.cells[0], DOWN, buff=0.08)
                           .align_to(r.cells[0], LEFT))
                ids.append(Mono(k2, size=28, color=DIM).next_to(r.cells[1], DOWN, buff=0.08)
                           .align_to(r.cells[1], LEFT))
            c.wait_until("his id")
            self.play(*appear(*ids, lag=0.2, shift=None), run_time=1.2)
            note = T("smaller ID,\nso p1", size=28, color=YELLOW)
            note.next_to(tab, RIGHT, buff=0.3).match_y(VGroup(tab.rows[1], tab.rows[2]))
            self.play(*appear(note), run_time=min(1.0, max(0.4, c.until("tie") - 0.1)))
            c.wait_until("tie")
            r6 = top5_table(pitch=1.0, top=3.4, rows=TOP5 + [ROW6], gap=0.4).rows[5]
            r6.shift(DOWN * 0.1).set_color(DIM)
            cut = DashedLine([tab.get_left()[0] - 0.1, 0, 0], [tab.get_right()[0] + 0.1, 0, 0],
                             color=RED, stroke_width=3, dash_length=0.12)
            cut.set_y((tab.rows[4].get_bottom()[1] + r6.get_top()[1]) / 2)
            lim = Mono("LIMIT 5", size=28, color=RED).next_to(cut, RIGHT, buff=0.3)
            self.play(*appear(r6, shift=None), Create(cut), *appear(lim, shift=None), run_time=1.2)
            c.wait_until("break the tie")
            sevens = [tab.rows[3].cells[2], tab.rows[4].cells[2], r6.cells[2]]
            initials = [tab.rows[3].cells[0][0], tab.rows[4].cells[0][0], r6.cells[0][0]]
            self.play(*flash(sevens, color=GOLD), run_time=1.2)
            self.play(LaggedStart(*flash(initials), lag_ratio=0.4), run_time=1.6)
            c.wait_until("limit five")
            self.play(*flash([lim], color=RED), run_time=1.0)
