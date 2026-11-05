"""Chapter 3, scene 2: a subquery that looks outward (correlated subquery). Clips c3.corr.1 – c3.corr.3.

Owns the running visual *the outer loop* (s3, s4, s6, ch8 s2 reuse it):

    mod = load_scene("ch3_s2_correlated")
    loop = mod.outer_loop(left_title="movies", left_rows=MOVIE_ROWS, right_title="plays_role",
                          right_cols=PR_COLS, right_rows=PR_ROWS, dim_cols=(0,))
        # static VGroup, full-frame layout (left column x -6.5.., card right edge x 6.7, top y 1.75).
        # rows: tuples of cell strings, None = a DIM ⋮ row.
        # .left (.title, .rows[i] VGroup of Mono cells) .card (.box .header .divider .title .heads
        # .rows[i]) .counter (GOLD Mono) .counter_label ("rows", DIM) .cursor (YELLOW box, NOT in the
        # group: add it / FadeIn it yourself; .cursor_at(i) = a box on left row i)
    mod.move_cursor(loop, i)        # [Transform] the cursor slides to left row i
    mod.sweep(loop, run_time)       # [UpdateFromAlphaFunc] a YELLOW bar runs down the card (removes itself)
    mod.light(loop, idxs, color)    # recolor anims for card rows idxs (color=None restores built colours)
    mod.set_count(scene, loop, n, *extra, run_time=1.0)  # plays a swap of the counter to n, keeps loop whole
    # size/layout keywords (lsize rsize title_size lx ltop lpitch rx ctop hdr pitch count_y) default to
    # the original layout; this scene itself draws the larger S2_LOOP (no person_id, text >= 28).
    mod.corner_query()              # (query, arrow) at Code 20 in the top-left corner
    mod.handover_shot()             # this scene's last frame (s3 opens on it): .loop .tags .plan drawn;
                                    # .query/.arrow = corner_query(), NOT drawn (the query left at {loop})
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

QUERY = """SELECT movie_id, title
FROM   movies AS m
WHERE NOT EXISTS (
    SELECT 1 FROM plays_role AS r
    WHERE r.movie_id = m.movie_id
);"""
LIST_SUB = "(SELECT movie_id FROM plays_role)"
Q_SIZE, Q_SMALL = 30, 20

MOVIE_ROWS = [("The Kid", "1921"), ("Sherlock Jr.", "1924"), ("The Gold Rush", "1925"), None,
              ("Kaiva", "2023"), ("Flow", "2024")]
PR_COLS = ("person_id", "movie_id", "role")
TT = "tt0012349"
KID_ROLES = [("nm0000122", "A Tramp"), ("nm0047800", "Bride"), ("nm0042317", "Car Thief"),
             ("nm0088471", "His Assistant"), ("nm0042317", "Man in Shelter"),
             ("nm0074788", "Night Shelter Keeper"), ("nm0080930", "Orphan Asylum Driver"),
             ("nm0074788", "Professor Guido"), ("nm0048798", "Slum Nurse"), ("nm0001067", "The Child"),
             ("nm0588033", "The Man"), ("nm0701012", "The Woman")]
PR_ROWS = [None] + [(p, TT, r) for p, r in KID_ROLES] + [None]
KID_IDX = list(range(1, 13))

# layout of the loop (full frame)
LX, LTOP, LPITCH, LSIZE = -6.5, 0.75, 0.52, 24
RX, CTOP, HDR, PITCH, RSIZE = 6.7, 1.75, 0.45, 0.3, 20
COUNT_Y = -0.9

# this scene's own, larger loop: person_id dropped, every text >= 28
S2_COLS = ("movie_id", "role")
S2_ROWS = [None] + [(TT, r) for _, r in KID_ROLES] + [None]
S2_LOOP = dict(right_cols=S2_COLS, right_rows=S2_ROWS, dim_cols=(), lsize=28, rsize=28, title_size=30,
               lx=-6.6, ltop=0.6, lpitch=0.5, rx=6.6, ctop=3.5, hdr=0.5, pitch=0.4, count_y=-1.25,
               lgap=0.2, pad=0.17, gap=0.34, cursor_pad=0.16)
AVG_SUB = "(SELECT AVG(rating)\n FROM ratings)"       # ch1 s7's subquery, wrapped to fit at 28
LIST_SUB2 = "(SELECT movie_id\n FROM plays_role)"     # ch2 s3's, wrapped
CB_SIZE = 28


def _vdots(color=DIM, h=0.24):
    d = MathTex(r"\vdots", color=color)
    d.set_height(h)
    return d


class OuterLoop(VGroup):
    pass


def outer_loop(left_title="movies", left_rows=MOVIE_ROWS, right_title="plays_role",
               right_cols=PR_COLS, right_rows=PR_ROWS, dim_cols=(0,), lsize=LSIZE, rsize=RSIZE,
               title_size=24, lx=LX, ltop=LTOP, lpitch=LPITCH, rx=RX, ctop=CTOP, hdr=HDR, pitch=PITCH,
               count_y=COUNT_Y, lgap=0.35, pad=0.18, gap=0.28, cursor_pad=0.36):
    """The {loop} picture: left column of rows, GOLD counter, tall BLUE card on the right.
    The size/layout keywords default to the original (s4, s6 render from the defaults)."""
    LX, LTOP, LPITCH, LSIZE, RX, CTOP, HDR, PITCH, RSIZE = lx, ltop, lpitch, lsize, rx, ctop, hdr, pitch, rsize
    ks = RSIZE / 20                      # card band heights scale with the card's text size
    kl = LSIZE / 24
    loop = OuterLoop()
    loop.pitch, loop.count_y, loop.lx = PITCH, count_y, LX
    # ---- left column
    left = VGroup()
    lt = Mono(left_title, LSIZE + 2, weight=BOLD)
    lt.move_to([0, LTOP, 0]).align_to([LX, 0, 0], LEFT)
    ncol = max(len(r) for r in left_rows if r)
    widths = [max(Mono(r[j], LSIZE).width for r in left_rows if r) for j in range(ncol)]
    xs = [LX]
    for w in widths[:-1]:
        xs.append(xs[-1] + w + lgap)
    rows = []
    for i, r in enumerate(left_rows):
        y = LTOP - 0.62 * kl - i * LPITCH
        if r is None:
            g = VGroup(_vdots(h=0.3).move_to([LX + 0.25, y, 0]))
        else:
            cells = []
            for j, s in enumerate(r):
                t = Mono(s, LSIZE)
                t.move_to([0, y, 0]).align_to([xs[j], 0, 0], LEFT)
                cells.append(t)
            g = VGroup(*cells)
        rows.append(g)
    left.add(lt, *rows)
    left.title, left.rows = lt, rows
    left.width_all = xs[-1] + widths[-1] - LX
    # ---- card
    card = VGroup()
    cw = [max([Mono(c, RSIZE).width] + [Mono(r[j], RSIZE).width for r in right_rows if r])
          for j, c in enumerate(right_cols)]
    w = 2 * pad + sum(cw) + gap * (len(cw) - 1)
    h = HDR + 0.42 * ks + PITCH * len(right_rows) + 0.14
    x0 = RX - w
    cx = RX - w / 2
    box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
    box.move_to([cx, CTOP - h / 2, 0])
    header = Rectangle(width=w, height=HDR).set_stroke(BLUE, 0).set_fill(BLUE, 0)
    header.move_to([cx, CTOP - HDR / 2, 0])
    divider = Line([x0, CTOP - HDR, 0], [RX, CTOP - HDR, 0]).set_stroke(BLUE, 2)
    title = Mono(right_title, title_size, weight=BOLD).move_to([cx, CTOP - HDR / 2, 0])
    cxs = [x0 + pad]
    for ww in cw[:-1]:
        cxs.append(cxs[-1] + ww + gap)
    hy = CTOP - HDR - 0.23 * ks
    heads = VGroup(*[Mono(c, RSIZE, color=DIM).move_to([0, hy, 0]).align_to([cxs[j], 0, 0], LEFT)
                     for j, c in enumerate(right_cols)])
    crow = []
    y0 = CTOP - HDR - 0.42 * ks - PITCH / 2
    for i, r in enumerate(right_rows):
        y = y0 - i * PITCH
        if r is None:
            g = VGroup(*[_vdots(h=0.22 * ks).move_to([cxs[j] + 0.25, y, 0]) for j in range(len(right_cols))])
        else:
            cells = []
            for j, s in enumerate(r):
                t = Mono(s, RSIZE, color=DIM if j in dim_cols else FG)
                t.move_to([0, y, 0]).align_to([cxs[j], 0, 0], LEFT)
                t._base_color = DIM if j in dim_cols else FG
                cells.append(t)
            g = VGroup(*cells)
        g.row_y = y
        crow.append(g)
    card.add(header, box, divider, title, heads, *crow)
    card.box, card.header, card.divider, card.title, card.heads, card.rows = box, header, divider, title, heads, crow
    card.y_first, card.y_last = y0, y0 - (len(right_rows) - 1) * PITCH
    # ---- counter
    mid = (LX + left.width_all + x0) / 2
    counter = Mono("0", 44, color=GOLD).move_to([mid, count_y, 0])
    clabel = T("rows", 28, DIM).next_to(counter, DOWN, buff=0.2)
    loop.add(left, card, counter, clabel)
    loop.left, loop.card, loop.counter, loop.counter_label = left, card, counter, clabel
    loop.count_x = mid

    def cursor_at(i):
        row = left.rows[i]
        r = Rectangle(width=left.width_all + cursor_pad, height=0.46)
        r.set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.12).set_z_index(-1)
        r.move_to([LX + left.width_all / 2, row.get_center()[1], 0])
        return r

    loop.cursor_at = cursor_at
    loop.cursor = cursor_at(0)
    return loop


def move_cursor(loop, i):
    return [Transform(loop.cursor, loop.cursor_at(i))]


def sweep(loop, run_time=1.5):
    card = loop.card
    bar = Rectangle(width=card.box.width - 0.12, height=getattr(loop, "pitch", PITCH))
    bar.set_stroke(width=0).set_fill(YELLOW, 0.22).set_z_index(-1)
    bar.move_to([card.box.get_center()[0], card.y_first, 0])
    y0, y1 = card.y_first, card.y_last

    def upd(m, a):
        m.move_to([card.box.get_center()[0], y0 + (y1 - y0) * a, 0])
        op = 0.22 * min(1, a / 0.08, (1 - a) / 0.08)
        m.set_fill(YELLOW, max(0, op))

    return [UpdateFromAlphaFunc(bar, upd, run_time=run_time, rate_func=linear, remover=True)]


def light(loop, idxs, color=YELLOW):
    out = []
    for i in idxs:
        for cell in loop.card.rows[i]:
            out.append(cell.animate.set_color(color if color else getattr(cell, "_base_color", FG)))
    return out


def set_count(scene, loop, n, *extra, run_time=1.0):
    old = loop.counter
    new = Mono(str(n), 44, color=GOLD).move_to([loop.count_x, getattr(loop, "count_y", COUNT_Y), 0])
    scene.play(*swap(old, new), *extra, run_time=run_time)
    settle(scene, loop, add=[new], drop=[old])
    loop.counter = new


# ---------------------------------------------------------------- query and its arrow
def _query():
    q = Code(QUERY, size=Q_SIZE)
    q.move_to([0, 0.0, 0]).align_to([-6.6, 0, 0], LEFT)
    q.find("AS m", line=1)[-1].set_color(YELLOW)
    q.find("m.movie_id", line=4)[0].set_color(YELLOW)
    return q


def _arrow(q):
    """YELLOW curve from m.movie_id round the right of the subquery to `movies AS m`, tip pointing left."""
    src = q.find("m.movie_id", line=4)
    dst = q.find("AS m", line=1)[-1]
    u = q.height / 6          # one line, at whatever scale q is
    xr = max(q.line(3).get_right()[0], src.get_right()[0])
    s0 = np.array([xr + 0.55 * u, src.get_center()[1], 0])
    e0 = np.array([dst.get_right()[0] + 0.5 * u, dst.get_center()[1], 0])
    cx = xr + 1.5 * u
    curve = CubicBezier(s0, [cx, s0[1], 0], [cx, e0[1], 0], e0 + RIGHT * 0.15 * u)
    curve.set_stroke(YELLOW, 3)
    tip = Triangle().set_stroke(width=0).set_fill(YELLOW, 1)
    tip.stretch_to_fit_width(0.46 * u).stretch_to_fit_height(0.4 * u)
    tip.rotate(PI / 2)            # points left
    tip.move_to(e0 + LEFT * 0.0)
    tip.shift(LEFT * (tip.get_left()[0] - (dst.get_right()[0] + 0.12 * u)))
    return VGroup(curve, tip)


def _shrink(group):
    group.scale(Q_SMALL / Q_SIZE)
    group.align_to([-6.6, 0, 0], LEFT).align_to([0, 3.5, 0], UP)
    return group


def _tags(loop):
    # no "→": at size 28 the column, a tag and the padded card only just fit across the frame
    kid = T("12 rows", 28, DIM).next_to(loop.left.rows[0], RIGHT, buff=0.2)
    flow = T("0 rows", 28, DIM).next_to(loop.left.rows[5], RIGHT, buff=0.2)
    kid.align_to(flow, LEFT)
    return kid, flow


def _plan_lines():
    a = T("meaning: once per outer row", 28, DIM)
    b = T("plan: may be cleverer (scene 4)", 28, DIM)
    # top-left, where the callbacks were (under the loop there is no room left at text size 28)
    a.move_to([0, 3.2, 0]).align_to([S2_LOOP["lx"], 0, 0], LEFT)
    b.next_to(a, DOWN, buff=0.1, aligned_edge=LEFT)
    return a, b


def corner_query():
    """(query, arrow) shrunk to the top-left corner (Code 20): seen only in passing at {loop}."""
    q = _query()
    q.find("m.movie_id", line=4).set_color(YELLOW)
    arrow = _arrow(q)
    _shrink(VGroup(q, arrow))
    return q, arrow


def handover_shot():
    """The last frame: loop (cursor on Flow), the two tags, the two plan lines. No query on screen:
    .query/.arrow are the corner query, NOT in the group (for s3 to bring back)."""
    loop = outer_loop(**S2_LOOP)
    loop.cursor = loop.cursor_at(5)
    tags = VGroup(*_tags(loop))
    plan = VGroup(*_plan_lines())
    shot = VGroup(loop, loop.cursor, tags, plan)
    shot.query, shot.arrow = corner_query()
    shot.loop, shot.tags, shot.plan = loop, tags, plan
    return shot


class Correlated(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.0)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        with self.say("c3.corr.1") as c:
            q = _query()
            self.q = q
            self.play(*appear(q, shift=None), run_time=1.2)
            c.wait_until("where not exists")
            self.play(FlashUnder(q.find("NOT EXISTS", line=2), color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until("inner")

            sub = VGroup(q.line(3), q.line(4))
            box = SurroundingRectangle(sub, color=YELLOW, buff=0.14, corner_radius=0.08).set_stroke(width=2.5)
            self.box = box
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("m")

            mm = q.find("m.movie_id", line=4)
            self.play(*recolor(mm, YELLOW), FlashAround(mm, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("outer")

            arrow = _arrow(q)
            self.arrow = arrow
            self.play(Create(arrow.submobjects[0]), run_time=1.4)
            self.play(FadeIn(arrow.submobjects[1]), run_time=0.3)
            self.remove(*arrow.submobjects)
            self.add(arrow)
            c.wait_until("it comes from")
            self.play(FlashAround(q.find("movies AS m", line=1), run_time=1.5, time_width=1.5))
            c.wait_until("name")

            lab = T("correlated subquery", 36, YELLOW)
            sub_lab = T("refers to the outer query", 28, DIM)
            lab.next_to(box, RIGHT, buff=0.35).align_to(box, DOWN).shift(DOWN * 0.15)
            sub_lab.next_to(lab, DOWN, buff=0.18, aligned_edge=LEFT)
            self.labels = (lab, sub_lab)
            self.play(*appear(lab), run_time=1.0)  # early: the term this sentence names
            c.wait_until("refers")
            self.play(*appear(sub_lab), run_time=1.0)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        q, arrow = self.q, self.arrow
        with self.say("c3.corr.2") as c:
            c.wait_until("running")
            tq, ta = _shrink(VGroup(q.copy(), arrow.copy()))
            loop = outer_loop(**S2_LOOP)
            self.loop = loop
            # the query recedes into the corner and steps off (s3 brings it back) as the loop builds
            # (two plays: a Transform and a FadeOut of the same mobject in one play cancel the shrink)
            avail = c.until("kid")
            self.play(*during(disappear(self.box, *self.labels), 0, 0.35),
                      *during([Transform(q, tq), Transform(arrow, ta)], 0.25, 1.0),
                      run_time=max(1.0, min(1.3, 0.42 * avail)))
            self.play(*during(disappear(q, arrow), 0, 0.3),
                      *during(appear(loop.left, loop.counter, loop.counter_label, loop.card,
                                     shift=None, lag=0.3), 0.3, 1.0),
                      run_time=max(1.2, min(1.8, c.until("kid") - 0.1)))
            self.remove(*q.get_family(), *arrow.get_family())
            settle(self, loop)
            c.wait_until("kid")

            self.play(GrowFromCenter(loop.cursor), run_time=1.0)
            c.wait_until("scan")
            self.play(*sweep(loop, run_time=c.until("twelve", floor=1.0) - 0.15))
            c.wait_until("twelve")
            set_count(self, loop, 12, *light(loop, KID_IDX, YELLOW), run_time=1.2)
            c.wait_until("flow")

            self.play(*move_cursor(loop, 5), *light(loop, KID_IDX, None),
                      *set_alpha([loop.counter], DIMMED), run_time=0.9)
            self.play(*sweep(loop, run_time=max(0.8, c.until("none") - 0.1)))
            c.wait_until("none")
            set_count(self, loop, 0, run_time=1.0)
            c.wait_until("differ")

            kid, flow = _tags(loop)
            self.tags = (kid, flow)
            self.play(*appear(kid), run_time=1.0)  # early: tags summarise the two runs just shown
            self.play(*appear(flow), run_time=1.0)  # early: tags summarise the two runs just shown

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        loop = self.loop
        s7 = load_scene("ch1_s7_scalar")
        s21 = load_scene("ch2_s1_hook")
        with self.say("c3.corr.3") as c:
            avg = Code(AVG_SUB, size=CB_SIZE)
            avg.align_to([S2_LOOP["lx"], 0, 0], LEFT).align_to([0, 3.45, 0], UP)
            lst = Code(LIST_SUB2, size=CB_SIZE)
            lst.align_to([S2_LOOP["lx"], 0, 0], LEFT).align_to([0, avg.get_bottom()[1] - 0.25, 0], UP)
            self.play(*appear(avg, lst, shift=None, lag=0.4), run_time=1.4)  # early: both shown, then walked
            c.wait_until("avg")
            self.play(FlashAround(avg, run_time=1.5, time_width=1.5))
            c.wait_until("ran once")

            chip = s7.avg_chip(30).move_to(avg).align_to(avg, LEFT)
            self.play(*during([FadeOut(avg, scale=0.2, target_position=chip.get_center())], 0, 0.5),
                      *during([FadeIn(chip, scale=0.6)], 0.5, 1.0), run_time=1.6)
            once1 = T("runs once", 28, DIM).next_to(chip, RIGHT, buff=0.3)
            c.wait_until("single number")
            self.play(*appear(once1), run_time=1.0)
            c.wait_until("list")
            self.play(FlashAround(lst, run_time=1.5, time_width=1.5))
            c.wait_until("one run")

            col = s21.shape_icon("column")
            col.set_height(lst.height + 0.1).move_to(lst).align_to(chip, LEFT).shift(RIGHT * 0.2)
            self.play(*during([FadeOut(lst, scale=0.2, target_position=col.get_center())], 0, 0.5),
                      *during([FadeIn(col, scale=0.6)], 0.5, 1.0), run_time=1.6)
            once2 = T("runs once", 28, DIM).next_to(col, RIGHT, buff=0.3).align_to(once1, LEFT)
            self.play(*appear(once2), run_time=1.0)
            c.wait_until("per")

            # cursor steps down, sweep reruns at each row
            steps = [0, 1, 2, 4, 5]
            budget = c.until("plan") - 0.6
            unit = budget / (len(steps) * 1.0 + 0.7)
            self.play(*set_alpha([loop.counter], DIMMED), *move_cursor(loop, 0), run_time=unit * 0.6)
            self.play(*sweep(loop, run_time=unit * 1.0))
            for i in steps[1:]:
                self.play(*move_cursor(loop, i), run_time=unit * 0.35)
                self.play(*sweep(loop, run_time=unit * 0.65))
            self.play(*set_alpha([loop.counter], 1), run_time=0.5)
            c.wait_until("plan")

            meaning, plan = _plan_lines()
            self.play(*disappear(chip, col, once1, once2), run_time=0.8)
            self.play(*appear(plan), run_time=1.0)
            c.wait_until("meaning")
            self.play(*appear(meaning), run_time=1.0)
