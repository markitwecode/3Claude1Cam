"""Chapter 1, scene 1: the hook. Algebra bricks stack; a SQL query is a form. Clips c1.hook.1 – c1.hook.3.

Shared pieces (later scenes: `from lib.paths import load_scene; m = load_scene("ch1_s1_hook")`):
- `table_card(name="movies")` -> small BLUE table card; `.label` is the name (Mono 38).
- `table_icon(color=BLUE, scale=1)` -> tiny table glyph (0.36 x 0.26 at scale 1), the relation handed up.
- `brick(tex, caption=None, width=BRICK_W)` -> VGroup(box, op): BLUE rounded rectangle with the
  operator in MathTex; `.box .op`, `.caption` (DIM T 36, NOT a submobject; place it with
  `place_caption(b)`).
- `BRICKS` = [(tex, caption)] for the three bricks; `group_brick()`, `keep_brick()`,
  `count_brick()` build each one on its own (count_brick is the third, "count those years").
- `tower()` -> VGroup(base, icon0, b1, icon1, b2, icon2, b3), base centred at ORIGIN-ish, built
  bottom-up at pitch BRICK_H + GAP; `.base .bricks (list of 3) .icons (list of 3)
  .captions (VGroup, not a submobject, already placed right of the bricks)`.
- `ghost_bricks(top)` -> VGroup of two DIM ghost bricks (with icons) stacked above `top`.
- `select_form()` -> VGroup of seven rows in writing order (SELECT FROM WHERE GROUP BY HAVING
  ORDER BY LIMIT); `.slots[name]` -> row with `.kw` (Mono 30 BLUE) and `.box` (slot rectangle).
  `slot_content(form, name, sql)` -> Code 28 left-aligned inside that slot (form must be placed
  first); `slot_tick(form, name)` -> small GREEN check at the slot's right end.
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

BRICK_W = 5.4
BRICK_H = 0.9
GAP = 0.36
PITCH = BRICK_H + GAP

BRICKS = [
    (r"\gamma_{\text{year};\ \text{count}(*)\to \text{n\_movies}}", "group by year, count"),
    (r"\sigma_{\text{n\_movies} > 140}", "keep years over 140"),
    (r"\gamma_{\text{count}(*)\to \text{n\_years}}", "count those years"),
]

FORM_SLOTS = ["SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]
KW_W = 2.0
SLOT_W = 4.4
SLOT_H = 0.56
ROW_PITCH = 0.72


def table_icon(color=BLUE, scale=1.0):
    w, h = 0.36, 0.26
    frame = Rectangle(width=w, height=h).set_stroke(color, 2).set_fill(color, 0.15)
    head = Line([-w / 2, h / 2 - 0.08, 0], [w / 2, h / 2 - 0.08, 0]).set_stroke(color, 2)
    col = Line([0, h / 2 - 0.08, 0], [0, -h / 2, 0]).set_stroke(color, 1.5)
    g = VGroup(frame, head, col)
    g.scale(scale)
    return g


def table_card(name="movies"):
    box = RoundedRectangle(corner_radius=0.12, width=2.6, height=1.1)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.12)
    label = Mono(name, 38, FG).move_to(box.get_top() + 0.28 * DOWN)
    rule = Line(box.get_left() + 0.05 * DOWN, box.get_right() + 0.05 * DOWN).set_stroke(BLUE, 2)
    rows = VGroup(*[Line(LEFT * 0.85, RIGHT * 0.85).set_stroke(DIM, 2).shift(y * UP)
                    for y in (-0.22, -0.38)])
    g = VGroup(box, rule, rows, label)
    g.box, g.label = box, label
    return g


def brick(tex, caption=None, width=BRICK_W):
    box = RoundedRectangle(corner_radius=0.14, width=width, height=BRICK_H)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.15)
    op = MathTex(tex, font_size=66, color=FG)
    if op.width > width - 0.4:
        op.scale_to_fit_width(width - 0.4)
    op.move_to(box)
    g = VGroup(box, op)
    g.box, g.op = box, op
    g.caption = T(caption, 36, DIM) if caption else None
    return g


def place_caption(b, buff=0.4):
    if b.caption is not None:
        b.caption.next_to(b.box, RIGHT, buff=buff)
    return b.caption


def group_brick():
    return brick(*BRICKS[0])


def keep_brick():
    return brick(*BRICKS[1])


def count_brick():
    return brick(*BRICKS[2])


def tower():
    base = table_card("movies")
    bricks = [group_brick(), keep_brick(), count_brick()]
    icons = []
    y = base.box.get_top()[1]
    parts = [base]
    for b in bricks:
        icon = table_icon().move_to([0, y + GAP / 2, 0])
        b.move_to([0, y + GAP + BRICK_H / 2, 0])
        y = b.box.get_top()[1]
        icons.append(icon)
        parts += [icon, b]
    g = VGroup(*parts)
    g.base, g.bricks, g.icons = base, bricks, icons
    g.captions = VGroup(*[place_caption(b) for b in bricks])
    return g


def ghost_bricks(top, height=0.6):
    out = []
    y = top.get_top()[1]
    x = top.get_center()[0]
    for k in range(2):
        icon = table_icon(DIM).move_to([x, y + GAP / 2, 0]).set_opacity(0.6)
        box = RoundedRectangle(corner_radius=0.14, width=top.width, height=height)
        box.set_stroke(DIM, 2.5, opacity=0.7 - 0.25 * k).set_fill(DIM, 0.06)
        box.move_to([x, y + GAP + height / 2, 0])
        y = box.get_top()[1]
        out += [icon, box]
    return VGroup(*out)


def select_form():
    rows = []
    slots = {}
    for i, name in enumerate(FORM_SLOTS):
        kw = Mono(name, 30, BLUE)
        box = Rectangle(width=SLOT_W, height=SLOT_H).set_stroke(DIM, 2).set_fill(BG, 0)
        y = -i * ROW_PITCH
        kw.move_to([KW_W / 2, y, 0]).align_to([0, 0, 0], LEFT)
        box.move_to([KW_W + 0.25 + SLOT_W / 2, y, 0])
        row = VGroup(kw, box)
        row.kw, row.box = kw, box
        rows.append(row)
        slots[name] = row
    g = VGroup(*rows)
    g.move_to(ORIGIN)
    g.slots = slots
    return g


def slot_content(form, name, sql, size=28):
    box = form.slots[name].box
    code = Code(sql, size=size)
    code.move_to(box).align_to(box.get_left() + 0.2 * RIGHT, LEFT)
    return code


def slot_tick(form, name):
    box = form.slots[name].box
    return check_mark(GREEN).scale(0.6).move_to(box.get_right() + 0.3 * LEFT)


def carry(scene, src, dst, via=(), lane_x=None):
    """Like fly() for different glyphs: a copy of src (put on screen exactly over it first, so
    nothing visibly changes) (faint at first, so it never reads as doubled) travels through the waypoints `via` (or, with `lane_x`, first
    sideways to x = lane_x at src's height) to dst, shrinking to fit dst, and fades out as dst
    fades in (80-100%). Returns a list for play()."""
    a0, a1 = src.get_center(), dst.get_center()
    pts = [a0]
    if lane_x is not None:
        pts.append(np.array([lane_x, a0[1], 0.0]))
    pts += [np.array(p, dtype=float) for p in via] + [a1]
    seg = [np.linalg.norm(q - p) for p, q in zip(pts, pts[1:])]
    cum = np.concatenate([[0], np.cumsum(seg)]) / sum(seg)
    k = min(1.0, dst.height / src.height, dst.width / src.width)

    def path(a):
        i = min(int(np.searchsorted(cum, a, side="right")) - 1, len(seg) - 1)
        f = (a - cum[i]) / max(cum[i + 1] - cum[i], 1e-9)
        return interpolate(pts[i], pts[i + 1], f)

    tmpl = src.copy()
    cp = src.copy().set_opacity(0.3)
    scene.add(cp)

    def upd(m, a):
        m.become(tmpl)
        m.scale(interpolate(1, k, a)).move_to(path(a))
        m.set_opacity((0.3 + 0.7 * min(1, a / 0.3)) * (1 - max(0, (a - 0.8) / 0.2)))

    return [UpdateFromAlphaFunc(cp, upd, remover=True), *during([FadeIn(dst)], 0.8, 1.0)]


class Hook(NarratedScene):
    def construct(self):
        # ---- c1.hook.1: title card
        with self.say("c1.hook.1", gap=1.0) as c:
            card = title_card("Part 1 · Queries inside queries")
            if card.title.width > 12:
                card.title.scale_to_fit_width(12)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            c.wait_until("Databases")
            self.play(FadeIn(card.course, shift=0.2 * DOWN), run_time=0.9)  # early: title card
            c.wait_until("We begin")
            self.play(FadeIn(card.part, shift=0.2 * DOWN), run_time=0.9)  # early: title card

        # ---- c1.hook.2: operators take and return relations; the tower
        with self.say("c1.hook.2") as c:
            icon_in = table_icon(scale=2.6).move_to(2.6 * DOWN)
            op1 = brick(r"\text{operator}").move_to(1.3 * DOWN)
            icon_mid = table_icon(scale=2.6).move_to(ORIGIN)
            op2 = brick(r"\text{operator}").move_to(1.3 * UP)
            icon_out = table_icon(scale=2.6).move_to(2.6 * UP)

            sweep_clear(self, time_span(FadeIn(icon_in), 0.6, 1.4),
                        time_span(FadeIn(op1, shift=0.3 * UP), 0.8, 1.6), run_time=1.6)
            c.wait_until("returns a relation")
            self.play(*fly(icon_in, icon_mid), run_time=1.5)
            c.wait_until("stack")
            self.play(FadeIn(op2, target_position=op1.get_center(), scale=0.9), run_time=1.5)
            c.wait_until("hands a table up")
            self.play(*fly(icon_mid, icon_out), run_time=1.5)

            # the real tower, centred with its captions
            tw = tower()
            tw.shift(-tw.base.get_center() + np.array([-2.45, -2.85, 0]))
            for b in tw.bricks:
                place_caption(b)

            c.wait_until("movies")
            sweep_clear(self, time_span(FadeIn(tw.base, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)

            below = tw.base
            for k, cue in enumerate(["group", "keep", "count"]):
                b, icon = tw.bricks[k], tw.icons[k]
                c.wait_until(cue)
                rt = 1.5 if k == 0 else 1.2
                self.play(FadeIn(icon, target_position=below.get_top() + 0.15 * DOWN, scale=0.8),
                          FadeIn(b, shift=0.3 * UP),
                          time_span(FadeIn(b.caption, shift=0.25 * DOWN), 0.4 * rt, rt),
                          run_time=rt)
                below = b

            ghosts = ghost_bricks(tw.bricks[2].box)
            c.wait_until("more")
            self.play(*appear(*ghosts, shift=0.25 * DOWN, lag=0.3), run_time=1.6)

        # ---- c1.hook.3: the form; two bricks fit, the third is stuck; the question
        with self.say("c1.hook.3", gap=2.6) as c:
            form = select_form()
            form.move_to([-6.6 + form.width / 2, 2.75 - 3 * ROW_PITCH, 0])

            tw.generate_target()
            tw.target.scale(0.75)
            tw.target.shift(np.array([4.55, -2.3, 0]) - tw.target[0].get_center())
            self.play(*during(disappear(*ghosts, *tw.captions), 0, 0.35),
                      *during([MoveToTarget(tw)], 0.3, 1.0),
                      run_time=2.0)
            c.wait_until("fixed boxes")
            self.play(*appear(*[r.box for r in form], *[r.kw for r in form], shift=None, lag=0.12),  # early: the form is shown whole, then filled
                      run_time=1.8)
            c.wait_until("fixed order")
            self.play(*[time_span(FlashUnder(r.kw, color=BLUE, time_width=1.5), 0.15 * i, 0.15 * i + 0.8)
                        for i, r in enumerate(form)], run_time=0.15 * 6 + 0.8)

            c_from = slot_content(form, "FROM", "movies")
            c_sel = slot_content(form, "SELECT", "year, count(*)")
            c_gb = slot_content(form, "GROUP BY", "year")
            c_hav = slot_content(form, "HAVING", "count(*) > 140")
            ticks = [slot_tick(form, n) for n in ("SELECT", "FROM", "GROUP BY", "HAVING")]
            b1, b2, b3 = tw.bricks

            c.wait_until("fit")
            lane = 1.25
            sel_box = form.slots["SELECT"].box
            self.play(*carry(self, tw.base.label, c_from, lane_x=lane), run_time=1.2)
            self.play(*during(carry(self, b1.op, c_gb, lane_x=lane), 0.0, 0.55),
                      *during(carry(self, b1.op, c_sel, lane_x=lane,
                                    via=[(lane, sel_box.get_y(), 0), sel_box.get_right() + 0.4 * RIGHT]), 0.25, 0.85),
                      *during(carry(self, b2.op, c_hav, lane_x=lane), 0.45, 1.0),
                      *during([FadeIn(t, scale=0.6) for t in ticks]
                              + [r.box.animate.set_stroke(GREEN, 2.5) for r in
                                 (form.slots[n] for n in ("SELECT", "FROM", "GROUP BY", "HAVING"))],
                              0.85, 1.0),
                      run_time=2.4)

            c.wait_until("stuck")
            gb_box = form.slots["GROUP BY"].box
            hover = np.array([gb_box.get_right()[0] + 0.3 + b3.width / 2, gb_box.get_y(), 0])
            self.play(b3.animate.move_to(hover), run_time=1.5)
            start = b3.get_center()

            def shake(m, a):
                m.move_to(start + RIGHT * 0.16 * np.sin(a * 6 * PI) * (1 - a))

            self.play(UpdateFromAlphaFunc(b3, shake),
                      FlashAround(form.slots["SELECT"].box, color=GREEN, time_width=1.5),
                      FlashAround(gb_box, color=GREEN, time_width=1.5),
                      run_time=1.2)
            self.play(b3.box.animate.set_stroke(RED, 4), run_time=0.8)

            q = T("How do you make SQL stack?", 44, YELLOW).move_to(3.25 * DOWN)
            c.wait_until(own_word=q)
            self.play(*appear(q), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
