"""Chapter 1, scene 2: three tools (names, then three retrieval questions). Clips c1.tools.1 – c1.tools.3.

Also the project's shared deep-style widgets (every scene imports them with
load_scene("ch1_s2_tools")): slot constants, legend panel, move card, think stop, tags,
pinned formula, chrome(), and the three retrieval cards (trolley, triangle, arc).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ═══════════════════════════════ shared widgets ═══════════════════════════════
# Slots (frame x ±7.1, y ±4). Every scene lays out against these.
EDGE_X, EDGE_Y = 6.6, 3.5            # outer margin of the corner slots
CARD_FILL = "#171A21"                 # move card / think box fill

TAG_SIZE = 22
TAG_TL = np.array([-EDGE_X, EDGE_Y, 0])      # "beyond the notes": its top-left corner

PIN_POS = np.array([-1.7, 3.42, 0])          # pinned formula: centre (top centre, left of the move card)
PIN_SIZE = 36

MOVE_TR = np.array([EDGE_X, EDGE_Y, 0])      # move card: its top-right corner
MOVE_TEXT_W = 5.6                            # widest move text (2 lines)

LEG_BL = np.array([-EDGE_X, -EDGE_Y, 0])     # legend panel: its bottom-left corner
LEG_SIZE, LEG_SYM = 22, 29                   # words T size, symbol MathTex font size
LEG_PITCH, LEG_PAD, LEG_GAP, LEG_COLGAP = 0.36, 0.2, 0.2, 0.45
LEG_TIGHT = 0.32                             # row pitch when it falls back to one long column
LEG_ROWS = 5                                 # rows per column; the 6th entry opens column 2
LEG_MAX_RIGHT = -0.8                         # keep the panel left of this (think box sits right of it)

RING_POS = np.array([6.25, -3.15, 0])         # think-stop ring centre
RING_R = 0.3
THINK_POS = np.array([2.6, -2.8, 0])       # think box centre (lower third, right of the legend)
THINK_MAX_W = 6.3

# Free regions: (x_min, x_max, y_min, y_max)
PICTURE = (-EDGE_X, 0.6, -1.7, 2.85)        # centre-left ~55% width, above the legend
PICTURE_CENTER = np.array([(PICTURE[0] + PICTURE[1]) / 2, (PICTURE[2] + PICTURE[3]) / 2, 0])
COL_LEFT, COL_RIGHT = 0.95, EDGE_X           # derivation column, right, under the move card
COL_TOP, COL_PITCH = 1.5, 0.7               # centre y of line 0; line pitch (6 lines to ≈ -2.0)
COL_SIZE = 34                                # MathTex size of a column line
STEP_SIZE = 22                               # DIM arrow labels


def _baseline_align(text_mob, y):
    """Put a T's baseline at y (aligns on its first glyph without a descender)."""
    s = getattr(text_mob, "_src", None)
    glyphs = text_mob.submobjects
    chars = [ch for ch in (s or "") if not ch.isspace()]
    if s and len(chars) == len(glyphs):
        for ch, g in zip(chars, glyphs):
            if ch not in "gjpqy(),;'\"·:":
                text_mob.shift((y - g.get_bottom()[1]) * UP)
                return text_mob
    text_mob.shift((y + 0.08 - text_mob.get_center()[1]) * UP)
    return text_mob


def _t(text, size, color=FG, **kw):
    m = T(text, size=size, color=color, **kw)
    m._src = text
    return m


# ── tags ─────────────────────────────────────────────────────────────────────────
def tag(text, item=None, direction=RIGHT, buff=0.2):
    """DIM 22-px tag ("reference", "(81) · notes p. 108"), beside `item` if given."""
    m = _t(text, TAG_SIZE, DIM)
    if item is not None:
        m.next_to(item, direction, buff=buff)
    return m


def corner_tag(text="beyond the notes"):
    """The chapter's corner tag, top-left slot."""
    m = _t(text, TAG_SIZE, DIM)
    m.move_to(TAG_TL, aligned_edge=UL)
    return m


# ── legend ───────────────────────────────────────────────────────────────────────
def _leg_row(entry):
    tex, col, words = entry
    sym = MathTex(tex, font_size=LEG_SYM, color=col)
    w = _t(words, LEG_SIZE, FG)
    row = VGroup(sym, w)
    row.key = tex
    row.words_str = words
    return row


def _leg_layout(rows, max_rows, pitch=LEG_PITCH):
    """Place rows (column-major, bottom-anchored at LEG_BL) and return the panel box."""
    n = len(rows)
    nrows = max(1, min(n, max_rows))
    ncols = max(1, -(-n // max_rows))
    x0 = LEG_BL[0] + LEG_PAD
    right = x0
    for c in range(ncols):
        col = rows[c * max_rows:(c + 1) * max_rows]
        symw = max([0.32] + [r[0].width for r in col])
        wordw = max([0.0] + [r[1].width for r in col])
        for i, r in enumerate(col):
            base = LEG_BL[1] + LEG_PAD + 0.07 + (nrows - 1 - i) * pitch
            sym, w = r
            sym.shift((base - sym.get_bottom()[1]) * UP + (x0 + symw - sym.get_right()[0]) * RIGHT)
            _baseline_align(w, base)
            w.shift((x0 + symw + LEG_GAP - w.get_left()[0]) * RIGHT)
        right = x0 + symw + LEG_GAP + wordw
        x0 = right + LEG_COLGAP
    top = LEG_BL[1] + LEG_PAD + 0.07 + (nrows - 1) * pitch + 0.3 + LEG_PAD - 0.04
    w = right + LEG_PAD - LEG_BL[0]
    h = top - LEG_BL[1]
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h)
    box.set_stroke(DIM, 1.5).set_fill(CARD_FILL, 0.92)
    box.move_to(LEG_BL, aligned_edge=DL)
    box.set_z_index(-1)
    return box


def legend(entries, max_rows=LEG_ROWS):
    """The legend panel, bottom-left. entries: [(symbol TeX, colour, words), …].
    Returns a VGroup(box, *rows) with .box, .rows (VGroup(sym, words) each, .key = TeX),
    .entries, .max_rows. Change it on screen with legend_set / legend_add / legend_change /
    legend_remove (they keep the bottom-left corner fixed: the panel grows upward, then a
    second column opens after max_rows entries)."""
    entries = list(entries)
    rows = [_leg_row(e) for e in entries]
    box = _leg_layout(rows, max_rows)
    if len(rows) > max_rows and box.get_right()[0] > LEG_MAX_RIGHT:
        # two columns would run into the think-box / column area: one tighter column instead
        rows = [_leg_row(e) for e in entries]
        box = _leg_layout(rows, len(rows), LEG_TIGHT)
    g = VGroup(box, *rows)
    g.box, g.rows, g.entries, g.max_rows = box, rows, entries, max_rows
    return g


def legend_set(scene, leg, entries, *extra, run_time=1.2):
    """Animate the on-screen legend `leg` to `entries` (matched by symbol TeX): removed rows
    fade out first, kept rows slide to their new places, changed words swap in place, new rows
    fade in last. Calls scene.play itself; `extra` animations play alongside. Afterwards
    `leg` is one on-screen object again holding the new rows."""
    entries = list(entries)
    new = legend(entries, leg.max_rows)
    old_by = {r.key: r for r in leg.rows}
    outs, moves, ins, finals, adds, word_swaps = [], [], [], [], [], []
    for nr in new.rows:
        o = old_by.pop(nr.key, None)
        if o is None:
            ins.append(FadeIn(nr, shift=0.12 * UP))
            adds.append(nr)
            finals.append(nr)
            continue
        d = nr[0].get_center() - o[0].get_center()
        if o.words_str != nr.words_str:
            if np.linalg.norm(d) > 1e-4:
                moves.append(o[0].animate.shift(d))
            outs.append(FadeOut(o[1], shift=0.15 * UP))
            ins.append(FadeIn(nr[1], shift=0.15 * UP))
            word_swaps.append((o, nr[1], nr.words_str))
        elif np.linalg.norm(d) > 1e-4:
            moves.append(o.animate.shift(d))
        finals.append(o)
    for o in old_by.values():
        outs.append(FadeOut(o))
    if abs(new.box.width - leg.box.width) > 1e-4 or abs(new.box.height - leg.box.height) > 1e-4:
        moves.append(Transform(leg.box, new.box))
    phases = [p for p in (outs, moves, ins) if p]
    k = len(phases)
    anims = []
    for j, p in enumerate(phases):
        anims += during(p, j / k, (j + 1) / k)
    scene.play(*anims, *extra, run_time=run_time)
    for o, nw, s in word_swaps:
        o.remove(o[1])
        o.add(nw)
        o.words_str = s
    scene.remove(*leg.get_family(), *[m for r in adds for m in r.get_family()],
                 *[m for _, nw, _ in word_swaps for m in nw.get_family()])
    leg.submobjects = []
    leg.add(leg.box, *finals)
    leg.rows, leg.entries = finals, entries
    scene.add(leg)
    return leg


def legend_add(scene, leg, *entries, run_time=1.2, extra=()):
    """Append entries (each (TeX, colour, words)) at the bottom; the panel grows upward."""
    return legend_set(scene, leg, list(leg.entries) + list(entries), *extra, run_time=run_time)


def legend_change(scene, leg, key, words, run_time=1.2, extra=()):
    """Rewrite the words of the entry whose symbol TeX is `key`."""
    ents = [(t, c, words if t == key else w) for t, c, w in leg.entries]
    return legend_set(scene, leg, ents, *extra, run_time=run_time)


def legend_remove(scene, leg, *keys, run_time=1.2, extra=()):
    """Drop the entries with these symbol TeX keys; the rest close up."""
    return legend_set(scene, leg, [e for e in leg.entries if e[0] not in keys], *extra,
                      run_time=run_time)


# ── move card ────────────────────────────────────────────────────────────────────
def _wrap(text, size, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        cand = (cur + " " + wd).strip()
        if cur and T(cand, size=size).width > max_w:
            lines.append(cur)
            cur = wd
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def move_card(text, small=False):
    """The move card (PLAN's look): rounded, YELLOW stroke 2, fill #171A21, "The move" YELLOW 24,
    the move FG ~30 (down to 26 to stay ≤ 2 lines). Placed in the top-right slot (MOVE_TR).
    small=True: the recap version (label 20, text 22, ≤ 4.3 wide), built at ORIGIN.
    .box .label .body (VGroup of lines)."""
    if small:
        sizes, max_w, lab_size, pad = (22, 20), 4.3, 20, 0.16
    else:
        sizes, max_w, lab_size, pad = (28, 26), MOVE_TEXT_W, 24, 0.24
    for size in sizes:
        lines = _wrap(text, size, max_w)
        if len(lines) <= 2:
            break
    body = VGroup(*[_t(ln, size, FG) for ln in lines]).arrange(DOWN, buff=0.13 * size / 30,
                                                              aligned_edge=LEFT)
    label = _t("The move", lab_size, YELLOW)
    inner = VGroup(label, body).arrange(DOWN, buff=0.14 * size / 30, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.12, width=inner.width + 2 * pad,
                           height=inner.height + 2 * pad)
    box.set_stroke(YELLOW, 2).set_fill(CARD_FILL, 1).move_to(inner)
    card = VGroup(box, label, body)
    card.box, card.label, card.body = box, label, body
    if not small:
        card.move_to(MOVE_TR, aligned_edge=UR)
    return card


# ── think stop ───────────────────────────────────────────────────────────────────
def think_box(question, size=32, pos=None):
    """Think-stop question box (FG stroke 2, fill #171A21) with DIM "pause the video if you want
    longer" under it, centred at THINK_POS (lower third, right of the legend). `question` may hold
    "\\n" line breaks. .box .question .hint"""
    q = _t(question, size, FG, line_spacing=0.9)
    if q.width > THINK_MAX_W - 0.5:
        q.scale_to_fit_width(THINK_MAX_W - 0.5)
    box = RoundedRectangle(corner_radius=0.12, width=q.width + 0.5, height=q.height + 0.42)
    box.set_stroke(FG, 2).set_fill(CARD_FILL, 1)
    q.move_to(box)
    hint = _t("pause the video if you want longer", 24, DIM).next_to(box, DOWN, buff=0.14)
    g = VGroup(box, q, hint)
    g.move_to(pos if pos is not None else THINK_POS)
    g.box, g.question, g.hint = box, q, hint
    return g


def think_ring(pos=None):
    """The DIM ring (r 0.3) for a think stop, bottom-right slot. .track .arc; drain(ring, t)."""
    p = RING_POS if pos is None else pos
    track = Circle(radius=RING_R).set_stroke(DIM, 2, opacity=0.35).move_to(p)
    arc = Arc(radius=RING_R, start_angle=PI / 2, angle=-TAU, arc_center=p).set_stroke(DIM, 5)
    g = VGroup(track, arc)
    g.track, g.arc = track, arc
    return g


def drain(ring, run_time=8.0):
    """The ring's arc empties clockwise over run_time (linear). Use the hold's length:
    self.play(drain(ring, c.until("answer cue")))."""
    full = ring.arc.copy()

    def upd(m, a):
        m.pointwise_become_partial(full, min(a, 0.995), 1)

    return UpdateFromAlphaFunc(ring.arc, upd, run_time=run_time, rate_func=linear)


# ── pinned formula ───────────────────────────────────────────────────────────────
def pinned(tex, label=None, size=PIN_SIZE, **kw):
    """A formula pinned at top centre (PIN_POS) for a chapter, with an optional DIM 22 label on
    its left ("the rule"). `tex` a TeX string or list (MathTex args); kw go to MathTex
    (tex_to_color_map, substrings_to_isolate). .formula .label"""
    f = MathTex(*(tex if isinstance(tex, (list, tuple)) else [tex]), font_size=size, **kw)
    f.move_to(PIN_POS)
    g = VGroup(f)
    g.formula, g.label = f, None
    if label:
        lab = _t(label, TAG_SIZE, DIM).next_to(f, LEFT, buff=0.25)
        g.add(lab)
        g.label = lab
    return g


def pin_move(mob, height=None):
    """mob.animate into the pinned slot (scaled to `height`, default a 36-px formula's)."""
    a = mob.animate
    if height is not None:
        a = a.scale_to_fit_height(height)
    return a.move_to(PIN_POS)


# ── derivation column ────────────────────────────────────────────────────────────
def col_point(i):
    """Left-centre point of column line i (0 = top, under the move card)."""
    return np.array([COL_LEFT, COL_TOP - i * COL_PITCH, 0])


def col_place(mob, i):
    """Put mob's left edge on the column, at line i."""
    return mob.move_to(col_point(i), aligned_edge=LEFT)


def step_label(text, i):
    """DIM arrow + 22-px label in the gap above column line i (the justification for line i)."""
    y = COL_TOP - (i - 0.5) * COL_PITCH
    arr = Arrow(UP * 0.16, DOWN * 0.16, buff=0, stroke_width=2.5, tip_length=0.1,
                max_tip_length_to_length_ratio=0.4, color=DIM).move_to([COL_LEFT + 0.18, y, 0])
    lab = _t(text, STEP_SIZE, DIM)
    lab.next_to(arr, RIGHT, buff=0.15)
    return VGroup(arr, lab)


# ── chrome (scene joins) ─────────────────────────────────────────────────────────
def chrome(entries, corner=True):
    """Legend (+ the corner tag) as one VGroup, for joins: .legend, .tag (None if corner=False).
    In the next scene: ch = chrome(...); self.add(*ch); then legend_add(self, ch.legend, …)."""
    leg = legend(entries)
    g = VGroup(leg)
    g.legend, g.tag = leg, None
    if corner:
        g.tag = corner_tag()
        g.add(g.tag)
    return g


# The project's standing entries (colours from PLAN.md)
E_X = (r"x", BLUE, "displacement from the middle (signed)")
E_XD = (r"\dot{x}", GREEN, "velocity")
E_XDD = (r"\ddot{x}", RED, "acceleration")


def handover_shot():
    """Scene 2's last frame = scene 3's first: the legend (x, ẋ, ẍ) and the corner tag."""
    return chrome([E_X, E_XD, E_XDD])


# ── retrieval cards ──────────────────────────────────────────────────────────────
def _trolley_picture():
    ground = Line(LEFT * 1.9, RIGHT * 1.9).set_stroke(DIM, 2)
    body = RoundedRectangle(corner_radius=0.06, width=1.7, height=0.85)
    body.set_stroke(FG, 3).set_fill(CARD_FILL, 1)
    body.next_to(ground, UP, buff=0.3).shift(RIGHT * 0.6)
    wheels = VGroup(*[Circle(radius=0.15).set_stroke(FG, 3).set_fill(BG, 1)
                      .move_to(body.get_corner(DOWN + s * RIGHT) + RIGHT * (-s) * 0.38 + DOWN * 0.15)
                      for s in (-1, 1)])
    mass = _t("2 kg", 30).move_to(body)
    push = Arrow(body.get_left() + LEFT * 1.45, body.get_left(), buff=0.04, stroke_width=5,
                 color=FG, max_tip_length_to_length_ratio=0.22)
    force = _t("10 N", 30).next_to(push, UP, buff=0.12)
    g = VGroup(ground, body, wheels, mass, push, force)
    g.ground, g.body, g.mass, g.push, g.force = ground, body, mass, push, force
    return g


def _triangle_picture(scale=1.0):
    L = 2.7 * scale
    th = 30 * DEGREES
    A = np.array([0.0, 0.0, 0])
    B = np.array([L * np.cos(th), 0.0, 0])
    C = np.array([L * np.cos(th), L * np.sin(th), 0])
    tri = Polygon(A, B, C).set_stroke(FG, 3)
    s = 0.2 * scale
    corner = VMobject().set_points_as_corners([B + LEFT * s, B + LEFT * s + UP * s, B + UP * s])
    corner.set_stroke(FG, 2)
    ang = Arc(radius=0.55 * scale, start_angle=0, angle=th, arc_center=A).set_stroke(YELLOW, 4)
    ang_lab = MathTex(r"30^\circ", font_size=30 * scale ** 0.5, color=YELLOW)
    ang_lab.move_to(A + 0.95 * scale * np.array([np.cos(th / 2.6), np.sin(th / 2.6), 0]))
    hyp_lab = MathTex("10", font_size=32 * scale ** 0.5)
    mid = (A + C) / 2
    hyp_lab.move_to(mid + 0.3 * np.array([-np.sin(th), np.cos(th), 0]))
    q = MathTex("?", font_size=36 * scale ** 0.5).next_to(Line(B, C), RIGHT, buff=0.15)
    g = VGroup(tri, corner, ang, ang_lab, hyp_lab, q)
    g.tri, g.ang, g.ang_lab, g.hyp_lab, g.q = tri, ang, ang_lab, hyp_lab, q
    g.opp = Line(B, C)
    return g


def _arc_picture(scale=1.0):
    R = 1.85 * scale
    half = 0.25
    O = np.array([0.0, 0.0, 0])
    a0, a1 = PI / 2 - half, PI / 2 + half
    r0 = Line(O, O + R * np.array([np.cos(a0), np.sin(a0), 0])).set_stroke(FG, 3)
    r1 = Line(O, O + R * np.array([np.cos(a1), np.sin(a1), 0])).set_stroke(FG, 3)
    arc = Arc(radius=R, start_angle=a0, angle=2 * half, arc_center=O).set_stroke(BLUE, 6)
    ang = Arc(radius=0.55 * scale, start_angle=a0, angle=2 * half, arc_center=O).set_stroke(YELLOW, 4)
    ang_lab = MathTex(r"0.5\ \mathrm{rad}", font_size=30 * scale ** 0.5, color=YELLOW)
    ang_lab.next_to(ang.get_right(), RIGHT, buff=0.12).shift(DOWN * 0.08 * scale)
    rad_lab = MathTex("2", font_size=32 * scale ** 0.5).next_to(r1.get_center(), LEFT, buff=0.15)
    q = MathTex("?", font_size=36 * scale ** 0.5, color=BLUE).next_to(arc, UP, buff=0.12)
    g = VGroup(r0, r1, arc, ang, ang_lab, rad_lab, q)
    g.arc, g.ang, g.ang_lab, g.rad_lab, g.q = arc, ang, ang_lab, rad_lab, q
    return g


def _card(picture, lines, buff=0.35):
    g = VGroup(picture, *lines)
    picture.move_to(ORIGIN)
    prev = picture
    for ln in lines:
        ln.next_to(prev, DOWN, buff=buff if prev is picture else 0.22)
        prev = ln
    return g


def trolley_card(small=False):
    """Retrieval card 1: a 2 kg trolley pushed by 10 N. Full: .picture .question ("a = ?")
    .answer (a = F/m = 10/2 = 5 m/s², edit()-able from .question) .law (F = ma) .law_x
    (F = mẍ, not in the group: edit .law into it). Small (for s3): picture + F = mẍ, ~2.3 wide."""
    pic = _trolley_picture()
    law_x = MathTex("F", "=", "m", r"\ddot{x}", font_size=40)
    law_x[3].set_color(RED)
    if small:
        law_x.scale(30 / 40)
        g = VGroup(pic.scale(0.6), law_x)
        law_x.next_to(pic, DOWN, buff=0.22)
        g.picture, g.law_x = pic, law_x
        return g
    q = MathTex("a", "=", "?", font_size=36)
    ans = MathTex("a", "=", "F/m", "=", "10/2", "=", r"5\ \mathrm{m/s^2}", font_size=34)
    law = MathTex("F", "=", "m", "a", font_size=40)
    g = _card(pic, [ans, law])
    q.move_to(ans, aligned_edge=LEFT)
    law_x.move_to(law)
    g.picture, g.question, g.answer, g.law, g.law_x = pic, q, ans, law, law_x
    return g


def triangle_card(small=False):
    """Retrieval card 2: hypotenuse 10, YELLOW 30°, the opposite side "?". Full: .picture (with
    .q, the "?"), .five (the 5 that replaces it), .answer (2 lines). Small (for s5): picture +
    "opposite = hypotenuse × sin(angle)"."""
    pic = _triangle_picture(0.62 if small else 1.0)
    if small:
        f = MathTex(r"\text{opposite} = \text{hypotenuse}\times\sin(\text{angle})", font_size=26)
        f.next_to(pic, DOWN, buff=0.22)
        g = VGroup(pic, f)
        g.picture, g.formula = pic, f
        return g
    a1 = MathTex(r"\text{opposite} = \text{hypotenuse}\times\sin 30^\circ", font_size=28)
    a2 = MathTex(r"= 10\times\tfrac{1}{2} = 5", font_size=32)
    g = _card(pic, [a1, a2])
    a2.align_to(a1, LEFT).shift(RIGHT * 1.6)
    five = MathTex("5", font_size=36).move_to(pic.q, aligned_edge=LEFT)
    g.picture, g.answer, g.five = pic, VGroup(a1, a2), five
    return g


def arc_card(small=False):
    """Retrieval card 3: a sector of radius 2, YELLOW 0.5 rad, BLUE arc "?". Full: .picture (.q),
    .one (the 1 that replaces "?"), .answer (2 lines), .note (DIM "(angle in radians)").
    Small (for s6): picture + "arc = radius × angle"."""
    pic = _arc_picture(0.62 if small else 1.0)
    if small:
        f = MathTex(r"\text{arc} = \text{radius}\times\text{angle}", font_size=26)
        f.next_to(pic, DOWN, buff=0.22)
        g = VGroup(pic, f)
        g.picture, g.formula = pic, f
        return g
    a1 = MathTex(r"\text{arc} = \text{radius}\times\text{angle}", font_size=32)
    a2 = MathTex(r"= 2\times 0.5 = 1", font_size=32)
    note = _t("(angle in radians)", 28, DIM)
    g = _card(pic, [a1, a2, note])
    a2.align_to(a1, LEFT).shift(RIGHT * 0.75)
    one = MathTex("1", font_size=36, color=BLUE).move_to(pic.q)
    g.picture, g.answer, g.note, g.one = pic, VGroup(a1, a2), note, one
    return g


# ═══════════════════════════════════ scene ═══════════════════════════════════
class Tools(NarratedScene):
    def construct(self):
        self.add(corner_tag())                       # s1 ends on it: no FadeIn
        leg = self.names()
        trolley = self.quiz_trolley()
        self.quiz_shapes(trolley)
        # ends on handover_shot(): legend (x, ẋ, ẍ) + corner tag

    # ── c1.tools.1: the names ──────────────────────────────────────────────────
    def names(self):
        Y = 0.35
        line = Line([-4.2, Y, 0], [4.2, Y, 0]).set_stroke(FG, 3)
        tick = Line([0, Y - 0.15, 0], [0, Y + 0.15, 0]).set_stroke(DIM, 3)
        zero = MathTex("0", font_size=36, color=DIM).next_to(tick, DOWN, buff=0.15)
        xv = ValueTracker(0.0)

        def mk_arrow():
            v = xv.get_value()
            if abs(v) < 0.08:
                return Line([0, Y + 0.45, 0], [0.01, Y + 0.45, 0]).set_stroke(BLUE, 0, opacity=0)
            return Arrow([0, Y + 0.45, 0], [v, Y + 0.45, 0], buff=0, color=BLUE, stroke_width=6,
                         max_tip_length_to_length_ratio=0.2)

        arrow = always_redraw(mk_arrow)
        dot = Dot(radius=0.13, color=BLUE).move_to([0, Y, 0])
        dot.add_updater(lambda m: m.move_to([xv.get_value(), Y, 0]))
        xlab = MathTex("x", font_size=48, color=BLUE)
        xlab.add_updater(lambda m: m.move_to([xv.get_value() / 2, Y + 0.95, 0]))
        neg = MathTex("x", "<", "0", font_size=40, color=BLUE).move_to([-2.6, Y - 0.6, 0])
        cap = T("one dot: rate of change in time  ·  two dots: twice", 30, DIM).move_to([0, Y - 1.55, 0])

        with self.say("c1.tools.1") as c:
            leg = legend([E_X])
            self.play(*appear(leg, shift=None), run_time=1.0)  # early: the legend opens on "the names"; x is defined in the next sentence
            c.wait_until("Whatever swings")
            self.play(*appear(line, tick, zero, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("how far")
            self.add(arrow)
            self.play(FadeIn(dot), FadeIn(xlab), xv.animate.set_value(2.6),
                      run_time=min(1.8, c.until("signed")))
            c.wait_until("signed")
            self.play(xv.animate.set_value(-2.6), run_time=min(2.2, c.until("negative")))
            c.wait_until("negative")
            self.play(*appear(neg), run_time=1.0)
            c.wait_until(own_word=cap)
            self.play(*appear(cap, shift=None), run_time=1.0)
            c.wait_until(own_word=T("velocity"))
            legend_add(self, leg, E_XD, run_time=1.2)
            c.wait_until("that's the acceleration")
            legend_add(self, leg, E_XDD, run_time=min(1.2, c.until()))
        for m in (dot, xlab, arrow):
            m.clear_updaters()
        self.number_line = [line, tick, zero, arrow, dot, xlab, neg, cap]
        return leg

    # ── c1.tools.2: the trolley ────────────────────────────────────────────────
    def quiz_trolley(self):
        card = trolley_card()
        d = np.array([-4.65, 2.45, 0]) - card.get_top()
        for m in (card, card.question, card.law_x):
            m.shift(d)
        with self.say("c1.tools.2") as c:
            c.wait_until("quick questions")
            self.play(*disappear(*self.number_line), run_time=min(1.0, c.until("trolley")))
            c.wait_until("trolley")
            self.play(*appear(card.picture, shift=None), run_time=1.2)
            c.wait_until("What's its acceleration")
            self.play(*appear(card.question), run_time=1.0)
            c.wait_until("five")
            self.play(*edit(card.question, card.answer), run_time=min(1.5, c.until("Force equals")))
            c.wait_until("Force equals")
            self.play(*appear(card.law), run_time=1.0)
            c.wait_until("From here on")
            self.play(*edit(card.law, card.law_x), run_time=1.5)
            self.play(FlashAround(card.law_x[3], color=RED, time_width=1.5),
                      run_time=min(1.5, c.until()))
        return [[card.picture, card.answer, card.law_x]]

    # ── c1.tools.3: the triangle and the arc ────────────────────────────────────
    def quiz_shapes(self, trolley):
        tri = triangle_card()
        tri.move_to([0.1, 2.45, 0], aligned_edge=UP)
        tri.five.move_to(tri.picture.q, aligned_edge=LEFT)
        arc = arc_card()
        arc.move_to([4.75, 2.45, 0], aligned_edge=UP)
        arc.one.move_to(arc.picture.q)
        tq, aq = tri.picture.q, arc.picture.q
        tri.picture.remove(tq)
        arc.picture.remove(aq)
        with self.say("c1.tools.3", gap=1.2) as c:
            self.play(*appear(tri.picture, shift=None), run_time=1.2)
            c.wait_until("How long is the side")
            self.play(*appear(tq), run_time=1.0)
            c.wait_until("opposite")
            self.play(*swap(tq, tri.five), *appear(*tri.answer, lag=0.5),
                      run_time=min(1.8, c.until("arc")))
            c.wait_until("arc")
            self.play(*appear(arc.picture, shift=None), run_time=1.2)
            c.wait_until("How long is it")
            self.play(*appear(aq), run_time=1.0)
            c.wait_until("arc_answer")
            self.play(*swap(aq, arc.one), *appear(*arc.answer, lag=0.5),
                      run_time=min(1.5, c.until("Arc length")))
            c.wait_until("with the angle")
            self.play(*appear(arc.note), run_time=min(1.0, c.until("tools")))
            c.wait_until("tools")
        # the cards hold through "next few minutes" and leave once the line is over
        cards = [trolley, [tri.picture, tri.five, *tri.answer],
                 [arc.picture, arc.one, *arc.answer, arc.note]]
        leaves = [FadeOut(VGroup(*cd), scale=0.5) for cd in cards]
        self.play(*[a for k, x in enumerate(leaves) for a in during(x, 0.2 * k, 0.6 + 0.2 * k)],
                  run_time=1.8)
