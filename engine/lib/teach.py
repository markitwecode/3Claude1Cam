"""The teaching widgets of the auto and deep styles (docs/DEEP_STYLE.md): fixed slots on a
2560×1440 board, the reference rail (letters, definitions, key results), the move card, think
stops, tags, the pinned formula, the derivation column and derive_step. Promoted 2026-11-04 from
the pilot (projects/nst-maths/l10-deep-oscillations, scenes/ch1_s2_tools.py); the pilot keeps its
own copy. `from lib.teach import *` in any scene of a project whose project.json has a "style".

The slots (frame x ±7.11, y ±4; every scene lays out against them). Since 2026-11-04 (the user:
"use screen real estate to offload ram ... keep definitions and stuff visible") a reference rail
runs down the left edge; the legend is its top section:

    ┌ corner tag ─────────┬──── pinned formula (PIN_POS) ──┬──────── move card (MOVE_TR) ┐
    │ RAIL x −6.8..−3.4   │ PICTURE x −3.1..1.0             │ derivation column           │
    │ top 3.0, grows down │ y −3.55..2.85                   │ COL_LEFT 1.25..COL_RIGHT 6.6│
    │ to ≥ −3.72:         │ (the key picture, stays for     │ line i at y 1.5 − 0.8i      │
    │  letters            │  the scene; 4.1 × 6.4)          │ (lines 0–5: 1.5 .. −2.5;    │
    │  ── definitions     │                                 │  0–4 / 0–3 under a think box│
    │  ── key results     │                                 │ think box (THINK_POS, ≤ 4.7)│
    │ (≈ 10 entries)      │                                 │            think ring ◯     │
    └─────────────────────┴─────────────────────────────────┴─────────────────────────────┘

    x: rail −6.8..−3.4 · gap 0.3 · picture −3.1..1.0 · gap 0.25 · column 1.25..6.6 (cards to 6.8)
    y: corner tag 3.55..3.27 above the rail; move card 3.55..≈1.95 (2 lines) above column line 0
       (top ≈ 1.7); pinned formula centred at (−1.05, 3.42), ≤ 4.1 wide; think box + hint from
       y −3.62 up to ≈ −2.35 (one-line question) or ≈ −1.95 (two lines); ring (6.4, −3.15).

What changed from the first slot map (legend bottom-left, picture −6.6..0.6 × −1.7..2.85, column
0.95..6.6, think box centred (2.6, −2.8) and 6.3 wide): the legend became the rail; the picture
lost 43% of its width but gained the full height (area −20%), the column lost 0.3, the move card
is 5.5 wide (≤ ~60 characters on 2 lines), the think box moved under the column (≤ 4.7 wide).

From the pilot's copy: COL_PITCH 0.7 → 0.8 (22-px step labels sat ~0.05 from the lines);
`step_label` takes `y=`, `between=(upper, lower)`, `x=`; the column helpers take `top=`/`pitch=`;
`move_card` breaks lines evenly at 28 → 26 → 24 px before a third line; `think_box` takes a ready
Mobject; `pinned` keeps a tall formula's top at PIN_TOP; `baseline_align` works on any `T`.
"""
from collections import namedtuple
from itertools import combinations

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, TAU, UL, UP, UR, Arc, Arrow, Circle, FadeIn, FadeOut, Line, ManimColor,
    MathTex, Mobject, RoundedRectangle, Transform, UpdateFromAlphaFunc, VGroup, linear,
)
from manim.utils.rate_functions import smooth

from lib.moves import (_FlyCopy, _on_screen, appear, during, edit, edit_pairs,
                       glyph_classes)
from lib.style import DIM, FG, YELLOW, T

__all__ = [
    # slots and sizes
    "EDGE_X", "EDGE_Y", "TEXT_X", "CARD_FILL", "TAG_SIZE", "TAG_TL", "PIN_POS", "PIN_SIZE",
    "PIN_TOP", "PIN_MAX_W", "MOVE_TR", "MOVE_TEXT_W", "RAIL_LEFT", "RAIL_RIGHT", "RAIL_W",
    "RAIL_TOP", "RAIL_BOTTOM", "RAIL_SYM", "RAIL_TEX", "RAIL_WORDS", "RING_POS", "RING_R",
    "THINK_POS", "THINK_MAX_W", "PICTURE", "PICTURE_CENTER", "COL_LEFT", "COL_RIGHT", "COL_TOP",
    "COL_PITCH", "COL_SIZE", "STEP_SIZE", "EARLIER",
    # widgets
    "baseline_align", "tag", "corner_tag",
    "rail", "rail_sym", "rail_def", "rail_result", "rail_set", "rail_add", "rail_change",
    "rail_remove", "rail_row", "rail_highlight",
    "legend", "legend_set", "legend_add", "legend_change", "legend_remove", "chrome",
    "move_card", "think_box", "think_ring", "drain", "pinned", "pin_move",
    "col_point", "col_place", "step_label", "eq_line", "derive_step",
    "arrow_between", "clock", "run_clock",
]

# ═══════════════════════════════ slots ═══════════════════════════════
EDGE_X, EDGE_Y = 6.8, 3.55           # outer edge of the panels and cards (frame x ±7.11, y ±4)
TEXT_X = 6.6                         # loose text stays inside x ±6.6 (0.5 margin)
CARD_FILL = "#171A21"                # move card / think box / rail fill

TAG_SIZE = 22
TAG_TL = np.array([-6.62, EDGE_Y, 0])        # corner tag ("beyond the notes"): its top-left corner,
                                             # above the rail, on its text's left edge
# the reference rail: letters, then definitions, then key results, down the left edge
RAIL_LEFT, RAIL_W = -EDGE_X, 3.4             # x −6.8..−3.4
RAIL_RIGHT = RAIL_LEFT + RAIL_W
RAIL_TOP, RAIL_BOTTOM = 3.0, -3.72           # it grows down from RAIL_TOP, never past RAIL_BOTTOM
RAIL_PAD = 0.18                              # box edge → text (text x −6.62..−3.58: 3.04 wide)
RAIL_SYM_GAP = 0.18                          # symbol → its words
RAIL_INDENT = 0.08                           # words under a formula
RAIL_SYM, RAIL_TEX, RAIL_WORDS = 28, 26, 22  # letter symbols, formulas (MathTex), words (T)
RAIL_PITCH = 0.38                            # baseline to baseline between one-line entries
RAIL_LINE = 0.3                              # baseline to baseline between wrapped word lines
RAIL_DEF_STEP = 0.36                         # formula baseline → its words' baseline (≥ depth + 0.3)
RAIL_ENTRY_GAP = 0.1                         # extra space after a two-line entry
RAIL_SECTION_GAP = 0.13                      # divider ↔ the text on either side
RAIL_ASCENT = 0.22                           # cap height of the first line (top padding)
RAIL_TINT = 0.22                             # rail_highlight: peak fill opacity of the row tint
RAIL_KINDS = ("sym", "def", "result")        # the sections, top to bottom

PICTURE = (-3.1, 1.0, -3.55, 2.85)           # free region (x_min, x_max, y_min, y_max)
PICTURE_CENTER = np.array([(PICTURE[0] + PICTURE[1]) / 2, (PICTURE[2] + PICTURE[3]) / 2, 0])

PIN_POS = np.array([PICTURE_CENTER[0], 3.42, 0])   # pinned formula: centre (top, over the picture)
PIN_SIZE = 36
PIN_TOP = 3.7                                # a taller pinned formula hangs from here (0.3 margin)
PIN_MAX_W = PICTURE[1] - PICTURE[0]          # 4.1: wider runs into the rail or the move card

MOVE_TR = np.array([EDGE_X, EDGE_Y, 0])      # move card: its top-right corner
MOVE_TEXT_W = 5.0                            # widest move text line (the card ≈ 5.5 wide: x ≥ 1.3)

COL_LEFT, COL_RIGHT = 1.25, TEXT_X           # derivation column, right, under the move card
COL_TOP, COL_PITCH = 1.5, 0.8                # centre y of line 0; line pitch (6 lines to -2.5;
                                             # 5 / 4 under a one- / two-line think box)
COL_SIZE = 34                                # MathTex size of a column line
STEP_SIZE = 22                               # DIM step labels
EARLIER = 0.4                                # opacity of earlier column lines (DEEP_STYLE §6)

THINK_MAX_W = 4.7
THINK_POS = np.array([3.55, -3.62, 0])      # think box + hint: bottom centre (the hint line is 5.0 wide: x 1.05..6.05),
                                             # under the column; it grows up: top ≈ −2.4 with a
                                             # one-line question (column lines 0–4 stay), ≈ −1.95
                                             # with two (lines 0–3)
RING_POS = np.array([6.4, -3.15, 0])         # think-stop ring centre (right of the think box's hint)
RING_R = 0.3


def baseline_align(text_mob, y):
    """Put a T's baseline at y (aligns on its first glyph without a descender); falls back to
    the centre (+0.08) when glyphs and characters don't pair up (ligatures)."""
    s = getattr(text_mob, "_src", None) or getattr(text_mob, "original_text", None)
    glyphs = text_mob.submobjects
    chars = [ch for ch in (s or "") if not ch.isspace()]
    if s and len(chars) == len(glyphs):
        for ch, g in zip(chars, glyphs):
            if ch not in "gjpqy(),;'\"·:":
                text_mob.shift((y - g.get_bottom()[1]) * UP)
                return text_mob
    text_mob.shift((y + 0.08 - text_mob.get_center()[1]) * UP)
    return text_mob


def _tex_on_baseline(tex, size, color):
    """MathTex part for `tex`, with ._depth = how far it reaches below its baseline (a reference
    "x" set in the same TeX run marks the baseline)."""
    m = MathTex("x", "{}" + tex, font_size=size, color=color)
    f = m[1]
    f._depth = f.get_bottom()[1] - m[0].get_bottom()[1]   # ≤ 0 when it descends
    return f


def _to_baseline(f, y):
    f.shift((y + f._depth - f.get_bottom()[1]) * UP)
    return f


# ── tags ─────────────────────────────────────────────────────────────────────────
def tag(text, item=None, direction=RIGHT, buff=0.2):
    """DIM 22-px tag ("reference", "(81) · notes p. 108"), beside `item` if given."""
    m = T(text, TAG_SIZE, DIM)
    if item is not None:
        m.next_to(item, direction, buff=buff)
    return m


def corner_tag(text="beyond the notes"):
    """The chapter's corner tag, top-left slot (above the rail)."""
    return T(text, TAG_SIZE, DIM).move_to(TAG_TL, aligned_edge=UL)


# ── the reference rail ───────────────────────────────────────────────────────────
RailEntry = namedtuple("RailEntry", "tex color words kind key")


def rail_sym(tex, color, words):
    """A letter: its symbol in its colour and what it means ("θ  angle from the vertical")."""
    return RailEntry(tex, color, words, "sym", tex)


def rail_def(tex, words, color=FG, key=None):
    """A definition: the formula and a few words ("A = a − ib", "complex amplitude").
    key: what rail_remove / rail_highlight call it (default: the TeX)."""
    return RailEntry(tex, color, words, "def", key or tex)


def rail_result(tex, words, color=FG, key=None):
    """A key result (a YELLOW bar on its left): formula and a few words."""
    return RailEntry(tex, color, words, "result", key or tex)


def _entry(e):
    if isinstance(e, RailEntry):
        return e
    if len(e) == 3:                              # a legend entry (TeX, colour, words)
        return RailEntry(e[0], e[1], e[2], "sym", e[0])
    if len(e) == 4:
        return RailEntry(*e, e[0])
    return RailEntry(*e)


def _rail_words(words, color, max_w):
    """The words as one or two lines of T (the two-line split with the shorter widest line),
    shrunk to max_w only if one word is too long for it."""
    one = T(words, RAIL_WORDS, color)
    if one.width <= max_w:
        return [one]
    ws, best = words.split(), None
    for k in range(1, len(ws)):
        a, b = T(" ".join(ws[:k]), RAIL_WORDS, color), T(" ".join(ws[k:]), RAIL_WORDS, color)
        w = max(a.width, b.width)
        if best is None or w < best[0]:
            best = (w, [a, b])
    lines = best[1] if best else [one]
    w = max(m.width for m in lines)
    if w > max_w:
        for m in lines:
            m.scale(max_w / w)
    return lines


def _rail_build(entries, tight=False):
    """(rows, dividers, box, bottom) for the entries, top-anchored at RAIL_TOP."""
    entries = [_entry(e) for e in entries]
    keys = [e.key for e in entries]
    if len(set(keys)) != len(keys):
        raise ValueError(f"two rail entries share a key: {keys} (give rail_def/rail_result a key=)")
    k = 0.88 if tight else 1.0
    pitch, step, egap = RAIL_PITCH * k, RAIL_LINE * k, RAIL_ENTRY_GAP * k
    x0, x1 = RAIL_LEFT + RAIL_PAD, RAIL_RIGHT - RAIL_PAD
    tw = x1 - x0
    rows, divs = [], []
    prev_bottom = RAIL_TOP - RAIL_PAD
    y = prev_bottom - RAIL_ASCENT                 # the next baseline
    first = True

    def fit(row, base_y):
        """Push the row down if its top would come within 0.08 of what is above it."""
        over = row.get_top()[1] - (prev_bottom - 0.08)
        if over > 0:
            row.shift(over * DOWN)
            return base_y - over
        return base_y

    for kind in RAIL_KINDS:
        sec = [e for e in entries if e.kind == kind]
        if not sec:
            continue
        if not first:
            dy = prev_bottom - RAIL_SECTION_GAP
            d = Line([x0, dy, 0], [x1, dy, 0]).set_stroke(DIM, 1.2, opacity=0.6)
            d.key = ("divider", kind)
            divs.append(d)
            prev_bottom = dy
            y = dy - RAIL_SECTION_GAP - RAIL_ASCENT
        first = False
        if kind == "sym":
            syms = [_tex_on_baseline(e.tex, RAIL_SYM, e.color) for e in sec]
            # the symbol column fits the narrow symbols; a wide one ("a, b") pushes only its own words
            colw = max([0.32] + [s.width for s in syms if s.width <= 0.42])
            for e, s in zip(sec, syms):
                symw = max(colw, s.width)
                lines = _rail_words(e.words, FG, tw - symw - RAIL_SYM_GAP)
                _to_baseline(s, y)
                s.shift((x0 + symw - s.get_right()[0]) * RIGHT)
                for i, ln in enumerate(lines):
                    baseline_align(ln, y - i * step)
                    ln.shift((x0 + symw + RAIL_SYM_GAP - ln.get_left()[0]) * RIGHT)
                row = VGroup(s, VGroup(*lines))
                y = fit(row, y)
                y -= (len(lines) - 1) * step + pitch + (egap if len(lines) > 1 else 0)
                row.key, row.entry = e.key, e
                rows.append(row)
                prev_bottom = row.get_bottom()[1]
        else:
            for e in sec:
                f = _tex_on_baseline(e.tex, RAIL_TEX, e.color)
                if f.width > tw:
                    f.scale(tw / f.width)
                _to_baseline(f, y)
                f.shift((x0 - f.get_left()[0]) * RIGHT)
                w1 = T(e.words, RAIL_WORDS, DIM)
                if f.width + 0.22 + w1.width <= tw:         # one line: formula, then the words
                    baseline_align(w1, y)
                    w1.shift((f.get_right()[0] + 0.22 - w1.get_left()[0]) * RIGHT)
                    lines, last, two = [w1], y, False
                else:                                         # formula, words under it
                    lines = _rail_words(e.words, DIM, tw - RAIL_INDENT)
                    b = y - max(RAIL_DEF_STEP * (0.92 if tight else 1.0), -f._depth + 0.3)
                    for i, ln in enumerate(lines):
                        baseline_align(ln, b - i * step)
                        ln.shift((x0 + RAIL_INDENT - ln.get_left()[0]) * RIGHT)
                    last, two = b - (len(lines) - 1) * step, True
                row = VGroup(f, VGroup(*lines))
                shift_y = fit(row, y) - y
                last += shift_y
                if kind == "result":
                    bar = Line([RAIL_LEFT + 0.085, row.get_top()[1] + 0.02, 0],
                               [RAIL_LEFT + 0.085, row.get_bottom()[1] - 0.02, 0]).set_stroke(YELLOW, 3)
                    row.add(bar)
                y = last - pitch - (egap if two else 0)
                row.key, row.entry = e.key, e
                rows.append(row)
                prev_bottom = row.get_bottom()[1]
    bottom = prev_bottom - RAIL_PAD
    h = max(RAIL_TOP - bottom, 0.5)
    box = RoundedRectangle(corner_radius=0.1, width=RAIL_W, height=h)
    box.set_stroke(DIM, 1.5).set_fill(CARD_FILL, 0.92)
    box.move_to([RAIL_LEFT, RAIL_TOP, 0], aligned_edge=UL)
    box.set_z_index(-1)
    return rows, divs, box, RAIL_TOP - h


def rail(entries=()):
    """The reference rail down the left edge (x −6.8..−3.4, from y 3.0 down): everything a viewer
    would otherwise rewind for. Sections, top to bottom, each in the order given: letters
    (`rail_sym(tex, colour, words)`, or a legend tuple (tex, colour, words)), definitions
    (`rail_def(tex, words)`) and key results (`rail_result(tex, words)`, with a YELLOW bar), a
    thin divider between sections. Symbols 28 px, formulas 26, words 22 (DIM for definitions and
    results); words that don't fit wrap to a second line, a formula with words that don't fit
    beside it takes them on the line below. About 10 entries fit (5 letters + 5 two-line
    entries); past RAIL_BOTTOM it tightens once, then raises ValueError (rail_remove what the
    chapter no longer uses).
    Returns VGroup(box, *dividers, *rows) with .box .rows .dividers .entries; each row is
    VGroup(symbol or formula, VGroup(word lines)[, bar]) with .key and .entry. Change it on
    screen with rail_set / rail_add / rail_change / rail_remove; flag a row with rail_highlight."""
    entries = [_entry(e) for e in entries]
    rows, divs, box, bottom = _rail_build(entries)
    if bottom < RAIL_BOTTOM:
        rows, divs, box, bottom = _rail_build(entries, tight=True)
        if bottom < RAIL_BOTTOM:
            raise ValueError(f"the rail is full ({len(entries)} entries reach y {bottom:.2f}, below "
                             f"{RAIL_BOTTOM}): rail_remove entries the chapter no longer uses, or "
                             "shorten their words")
    g = VGroup(box, *divs, *rows)
    g.box, g.rows, g.dividers, g.entries = box, rows, divs, entries
    return g


def _shift_of(old, new, tol=2e-3):
    """The translation taking old onto new, or None if they differ in shape."""
    po, pn = old.family_members_with_points(), new.family_members_with_points()
    if len(po) != len(pn):
        return None
    d = new.get_center() - old.get_center()
    for a, b in zip(po, pn):
        if a.points.shape != b.points.shape or not np.allclose(a.points + d, b.points, atol=tol):
            return None
    return d


def _row_parts(row):
    return [row[0], *row[1].submobjects, *row.submobjects[2:]]


def _is_bar(m):
    return isinstance(m, Line)


def rail_set(scene, r, entries, *extra, run_time=1.2):
    """Animate the on-screen rail `r` to `entries` (rows matched by key): removed rows fade out
    first, kept rows slide to their new places, changed words swap in place, new rows fade in
    last, and the box grows or shrinks with them. Calls scene.play itself; `extra` animations
    play alongside. Afterwards `r` is one on-screen object again holding the new rows."""
    new = rail(entries)
    old_by = {row.key: row for row in r.rows}
    outs, moves, ins, finals, adds, word_swaps = [], [], [], [], [], []
    for nr in new.rows:
        o = old_by.pop(nr.key, None)
        if o is not None and o.entry == nr.entry:
            # same entry: each part (symbol, each word line, bar) slides to its new place (the
            # tight layout changes the spacing inside rows too)
            op, nparts = _row_parts(o), _row_parts(nr)
            ds = [_shift_of(a, b) for a, b in zip(op, nparts)] if len(op) == len(nparts) else [None]
            if all(d is not None or not a.family_members_with_points() or _is_bar(a)
                   for d, a in zip(ds, op)) and len(op) == len(nparts):
                for a, b, d in zip(op, nparts, ds):
                    if d is None:
                        moves.append(Transform(a, b))          # the result bar, another length
                    elif np.linalg.norm(d) > 1e-4:
                        moves.append(a.animate.shift(d))
                finals.append(o)
                continue
        same_sym = o is not None and o.entry[:2] == nr.entry[:2] and o.entry.kind == nr.entry.kind
        ds = _shift_of(o[0], nr[0]) if same_sym else None
        if ds is not None and len(o) == 2 and len(nr) == 2:   # same symbol, other words
            if np.linalg.norm(ds) > 1e-4:
                moves.append(o[0].animate.shift(ds))
            outs.append(FadeOut(o[1], shift=0.12 * UP))
            ins.append(FadeIn(nr[1], shift=0.12 * UP))
            word_swaps.append((o, nr[1], nr.entry))
            finals.append(o)
            continue
        if o is not None:
            outs.append(FadeOut(o))
        ins.append(FadeIn(nr, shift=0.12 * DOWN))
        adds.append(nr)
        finals.append(nr)
    for o in old_by.values():
        outs.append(FadeOut(o))
    old_divs = {d.key: d for d in r.dividers}
    final_divs = []
    for nd in new.dividers:
        od = old_divs.pop(nd.key, None)
        if od is None:
            ins.append(FadeIn(nd))
            adds.append(nd)
            final_divs.append(nd)
        else:
            dd = nd.get_center() - od.get_center()
            if np.linalg.norm(dd) > 1e-4:
                moves.append(od.animate.shift(dd))
            final_divs.append(od)
    for od in old_divs.values():
        outs.append(FadeOut(od))
    if abs(new.box.height - r.box.height) > 1e-4:
        moves.append(Transform(r.box, new.box))
    phases = [p for p in (outs, moves, ins) if p]
    anims = []
    for j, p in enumerate(phases):
        anims += during(p, j / len(phases), (j + 1) / len(phases))
    if anims or extra:
        scene.play(*anims, *extra, run_time=run_time)
    for o, nw, ent in word_swaps:
        o.submobjects[1] = nw
        o.entry = ent
    scene.remove(*r.get_family(), *[m for x in adds for m in x.get_family()],
                 *[m for _, nw, _ in word_swaps for m in nw.get_family()])
    r.submobjects = []
    r.add(r.box, *final_divs, *finals)
    r.rows, r.dividers, r.entries = finals, final_divs, new.entries
    scene.add(r)
    return r


def rail_add(scene, r, *entries, run_time=1.2, extra=()):
    """Add entries (rail_sym / rail_def / rail_result, or legend tuples) at the end of their
    sections; what is below them slides down."""
    return rail_set(scene, r, list(r.entries) + [_entry(e) for e in entries], *extra, run_time=run_time)


def rail_change(scene, r, key, words=None, tex=None, color=None, run_time=1.2, extra=()):
    """Rewrite an entry's words (and/or its TeX or colour); found by key."""
    ents = [e._replace(words=words or e.words, tex=tex or e.tex, color=color or e.color)
            if e.key == key else e for e in r.entries]
    if not any(e.key == key for e in r.entries):
        raise KeyError(f"no rail entry {key!r}: keys are {[e.key for e in r.entries]}")
    return rail_set(scene, r, ents, *extra, run_time=run_time)


def rail_remove(scene, r, *keys, run_time=1.2, extra=()):
    """Drop the entries with these keys; the rest close up."""
    return rail_set(scene, r, [e for e in r.entries if e.key not in keys], *extra, run_time=run_time)


def rail_row(r, key):
    """The on-screen row of entry `key` (e.g. to fly its formula into the column)."""
    for row in r.rows:
        if row.key == key:
            return row
    raise KeyError(f"no rail entry {key!r}: keys are {[row.key for row in r.rows]}")


def rail_highlight(r, key, color=YELLOW, run_time=1.5):
    """Flag an entry while the narration uses it: a soft tint behind its row rises, holds and
    goes (it removes itself). A list for play(): self.play(*rail_highlight(rl, "A"), ...), or
    pass it as derive_step(..., extra=rail_highlight(rl, "A"))."""
    row = rail_row(r, key)
    tint = RoundedRectangle(corner_radius=0.06, width=RAIL_W - 0.12, height=row.height + 0.12)
    tint.set_stroke(width=0).set_fill(color, 0)
    tint.move_to([RAIL_LEFT + RAIL_W / 2, row.get_center()[1], 0])
    tint.set_z_index(-0.5)                       # above the rail's box (−1), under its text

    def env(a):
        return smooth(min(1.0, a / 0.25)) if a < 0.5 else smooth(min(1.0, (1 - a) / 0.3))

    def upd(m, a):
        m.set_fill(color, opacity=RAIL_TINT * env(a))

    return [UpdateFromAlphaFunc(tint, upd, run_time=run_time, introducer=True, remover=True)]


# the legend is the rail's letters section (thin wrappers: older calls keep working)
def legend(entries, max_rows=None, max_right=None):
    """The letters as a rail (entries [(TeX, colour, words), …]); max_rows/max_right are ignored."""
    return rail(entries)


def legend_set(scene, leg, entries, *extra, run_time=1.2):
    return rail_set(scene, leg, entries, *extra, run_time=run_time)


def legend_add(scene, leg, *entries, run_time=1.2, extra=()):
    return rail_add(scene, leg, *entries, run_time=run_time, extra=extra)


def legend_change(scene, leg, key, words, run_time=1.2, extra=()):
    return rail_change(scene, leg, key, words, run_time=run_time, extra=extra)


def legend_remove(scene, leg, *keys, run_time=1.2, extra=()):
    return rail_remove(scene, leg, *keys, run_time=run_time, extra=extra)


def chrome(entries, corner=True, max_rows=None):
    """Rail (+ the corner tag) as one VGroup, for joins: .rail (also .legend), .tag (None if
    corner=False). The rail's layout depends only on its entries, so the next scene rebuilds the
    exact same shot: self.add(*chrome(r.entries)) (keep the entry list in one place, e.g. the
    chapter's first scene, and import it), then rail_add(self, ch.rail, …)."""
    r = rail(entries)
    g = VGroup(r)
    g.rail, g.legend, g.tag = r, r, None
    if corner:
        g.tag = corner_tag()
        g.add(g.tag)
    return g


# ── move card ────────────────────────────────────────────────────────────────────
_PUNCT = (",", ":", ";", ".", "—", "–")
_PUNCT_BONUS = 0.4      # a break after punctuation may leave its line this much wider
_ARTICLES = {"a", "an", "the"}
_BAD_BREAK = 0.6        # (not strict) the width a bad break costs
_WIDTHS = {}


def _widths(words, size):
    """Each word's width and the space between words, at T size `size` (cached). Summed, they
    match a whole line's width to ~0.03."""
    if ("a a", size) not in _WIDTHS:
        _WIDTHS[("a a", size)] = T("a a", size=size).width - 2 * T("a", size=size).width
    for w in words:
        if (w, size) not in _WIDTHS:
            _WIDTHS[(w, size)] = T(w, size=size).width
    return [_WIDTHS[(w, size)] for w in words], _WIDTHS[("a a", size)]


def _even_lines(words, size, max_w, n, strict=True, check_width=True):
    """The best split of `words` into n lines no wider than max_w: the widest line as short as
    possible, with a bonus for breaking after punctuation. Strict: no one-word line (when there
    are words enough), no line starting on a word that ends a clause ("θ:", "swing,"), and none
    ending on "a", "an" or "the"; not strict, each of those costs _BAD_BREAK of width instead.
    None if no split fits."""
    if n > len(words):
        return None
    ww, sp = _widths(words, size)
    best = None
    for cuts in combinations(range(1, len(words)), n - 1):
        b = (0, *cuts, len(words))
        segs = [(b[k], b[k + 1]) for k in range(n)]
        bad = 0
        if n > 1:
            bad += sum(e - s < 2 for s, e in segs) if len(words) >= 2 * n else 0
            bad += sum(words[s].endswith(_PUNCT) for s, _ in segs[1:])
            bad += sum(words[e - 1].lower() in _ARTICLES for _, e in segs[:-1])
        if strict and bad:
            continue
        widths = [sum(ww[s:e]) + (e - s - 1) * sp for s, e in segs]
        if check_width and max(widths) > max_w - 0.03:
            continue
        cost = (max(widths) + _BAD_BREAK * bad
                - _PUNCT_BONUS * sum(words[e - 1].endswith(_PUNCT) for _, e in segs[:-1]))
        if best is None or cost < best[0]:
            best = (cost, segs)
    return None if best is None else [" ".join(words[s:e]) for s, e in best[1]]


def _move_lines(text, sizes, max_w, max_lines):
    """(size, lines): the largest size at which the text fits in ≤ max_lines even lines (with
    clean breaks if any size allows them), else the smallest size with as many lines as it
    takes. "\\n" in text forces the breaks."""
    if "\n" in text:
        lines = [ln.strip() for ln in text.split("\n")]
        for size in sizes:
            if max(T(ln, size=size).width for ln in lines) <= max_w:
                return size, lines
        return sizes[-1], lines
    words = text.split()
    for strict in (True, False):
        for size in sizes:
            for n in range(1, max_lines + 1):
                lines = _even_lines(words, size, max_w, n, strict)
                if lines:
                    return size, lines
    for n in range(max_lines + 1, len(words) + 1):
        lines = (_even_lines(words, sizes[-1], max_w, n)
                 or _even_lines(words, sizes[-1], max_w, n, strict=False))
        if lines:
            return sizes[-1], lines
    return sizes[-1], _even_lines(words, sizes[-1], max_w, max_lines, False, check_width=False)


def move_card(text=None, small=False, max_lines=2, max_w=None, body=None):
    """The move card: rounded, YELLOW stroke 2, fill CARD_FILL, "The move" YELLOW 24, the move
    in FG at 28 px, down to 26 / 24 to stay on ≤ max_lines lines, broken into even lines. Placed
    in the top-right slot (MOVE_TR, ≈ 5.5 wide). Keep a move ≤ ~60 characters: past that it
    takes a third line and the card reaches y ≈ 1.55, onto the column's line 0.
    "\\n" in `text` sets the breaks yourself. `body`: a ready-made Mobject instead of text (e.g.
    a VGroup of lines mixing T and coloured MathTex), used as it is.
    small=True: the recap version (label 20, text 22 → 20, ≤ 4.3 wide), built at ORIGIN;
    a recap row of small cards may pass max_lines=3 and a narrower max_w.
    .box .label .body (VGroup of lines, or `body`)."""
    if small:
        sizes, width, lab_size, pad = (22, 20), 4.3, 20, 0.16
    else:
        sizes, width, lab_size, pad = (28, 26, 24), MOVE_TEXT_W, 24, 0.24
    if body is None:
        size, lines = _move_lines(text, sizes, max_w or width, max_lines)
        body = VGroup(*[T(ln, size, FG) for ln in lines]).arrange(DOWN, buff=0.13 * size / 30,
                                                                 aligned_edge=LEFT)
    else:
        size = sizes[0]
    label = T("The move", lab_size, YELLOW)
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
    """Think-stop question box (FG stroke 2, fill CARD_FILL) with DIM "pause the video if you
    want longer" (24) under it, its bottom at THINK_POS (under the column, left of the ring),
    ≤ 4.7 wide: break the question into lines of ≤ ~24 characters with "\\n" (a wider question
    is scaled down to fit). It grows upward: a one-line question tops out at y ≈ −2.4 (column
    lines 0–4 stay up), two lines at ≈ −1.95 (lines 0–3). `pos`: centre it there instead.
    `question`: text, or a ready-made Mobject. .box .question .hint"""
    q = T(question, size, FG, line_spacing=0.9) if isinstance(question, str) else question
    if q.width > THINK_MAX_W - 0.5:
        q.scale_to_fit_width(THINK_MAX_W - 0.5)
    box = RoundedRectangle(corner_radius=0.12, width=q.width + 0.5, height=q.height + 0.42)
    box.set_stroke(FG, 2).set_fill(CARD_FILL, 1)
    q.move_to(box)
    hint = T("pause the video if you want longer", 24, DIM).next_to(box, DOWN, buff=0.14)
    g = VGroup(box, q, hint)
    if pos is not None:
        g.move_to(pos)
    else:
        g.move_to(THINK_POS, aligned_edge=DOWN)
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
    """A formula pinned at top centre (PIN_POS, over the picture; ≤ 4.1 wide with its label) for
    a chapter, with an optional DIM 22 label on its left ("the rule"). `tex` a TeX string or list
    (MathTex args); kw go to MathTex (tex_to_color_map, substrings_to_isolate). .formula .label"""
    f = MathTex(*(tex if isinstance(tex, (list, tuple)) else [tex]), font_size=size, **kw)
    f.move_to(PIN_POS)
    if f.get_top()[1] > PIN_TOP:            # a tall formula (limits, a fraction) hangs from 3.7
        f.shift((PIN_TOP - f.get_top()[1]) * UP)
    g = VGroup(f)
    g.formula, g.label = f, None
    if label:
        lab = T(label, TAG_SIZE, DIM).next_to(f, LEFT, buff=0.25)
        g.add(lab)
        g.label = lab
        g.shift((PIN_POS[0] - g.get_center()[0]) * RIGHT)   # the pair centred over the picture
    return g


def pin_move(mob, height=None):
    """mob.animate into the pinned slot (scaled to `height`, default unchanged)."""
    a = mob.animate
    if height is not None:
        a = a.scale_to_fit_height(height)
    return a.move_to(PIN_POS)


# ── derivation column ────────────────────────────────────────────────────────────
def col_point(i, top=None, pitch=None):
    """Left-centre point of column line i (0 = top, under the move card; fractions allowed)."""
    top = COL_TOP if top is None else top
    pitch = COL_PITCH if pitch is None else pitch
    return np.array([COL_LEFT, top - i * pitch, 0])


def col_place(mob, i, top=None, pitch=None):
    """Put mob's left edge on the column, at line i."""
    return mob.move_to(col_point(i, top, pitch), aligned_edge=LEFT)


def step_label(text, i=None, y=None, between=None, top=None, pitch=None, x=None):
    """DIM arrow (0.26 tall) + 22-px label in the gap above column line i: the justification
    for line i (≤ 5 words). Or at height `y`, or centred in the real gap between two placed
    lines, `between=(upper, lower)` (use it when a line is tall: fractions, roots). `x`: the
    arrow's x (default COL_LEFT + 0.18)."""
    if between is not None:
        upper, lower = between
        y = (upper.get_bottom()[1] + lower.get_top()[1]) / 2
    elif y is None:
        y = col_point(i - 0.5, top, pitch)[1]
    arr = Arrow(UP * 0.13, DOWN * 0.13, buff=0, stroke_width=2.5, tip_length=0.1,
                max_tip_length_to_length_ratio=0.4, color=DIM)
    arr.move_to([COL_LEFT + 0.18 if x is None else x, y, 0])
    lab = T(text, STEP_SIZE, DIM)
    lab.next_to(arr, RIGHT, buff=0.15)
    return VGroup(arr, lab)


# ── derivations that keep the original (DEEP_STYLE §14) ──────────────────────────
DERIVE_HL_RT, DERIVE_DROP_RT, DERIVE_EDIT_RT = 0.8, 1.0, 1.5


def _tex_row(parts, anchor):
    """Place MathTex `parts` side by side exactly as TeX sets them in one formula (same
    baseline, TeX's spacing round relations), keeping parts[anchor] where it is. Falls back to
    next_to when a part has no TeX string."""
    strs = [getattr(p, "tex_string", None) for p in parts]
    if all(strs):
        try:
            ref = MathTex(*strs, font_size=getattr(parts[anchor], "font_size", None) or COL_SIZE)
        except Exception:
            ref = None
        if ref is not None and len(ref) == len(parts) and ref[anchor].width > 1e-6:
            k = parts[anchor].width / ref[anchor].width
            c0 = parts[anchor].get_center()
            for j, p in enumerate(parts):
                if j != anchor:
                    p.move_to(c0 + k * (ref[j].get_center() - ref[anchor].get_center()))
            return parts
    for j in range(anchor + 1, len(parts)):
        parts[j].next_to(parts[j - 1], RIGHT, buff=0.18)
    for j in range(anchor - 1, -1, -1):
        parts[j].next_to(parts[j + 1], LEFT, buff=0.18)
    return parts


def eq_line(lhs, rhs, rel="=", font_size=COL_SIZE, color=FG, **tex_kw):
    """The first line of a derivation, "lhs = rhs", as derive_step's lines are built: a VGroup
    (lhs, rel, body) with .lhs .rel .body, so the next derive_step copies only the body and puts
    its "=" under this one. tex_kw (tex_to_color_map, substrings_to_isolate) go to the body.
    Built at ORIGIN: col_place(line, 0), then self.play(*appear(line))."""
    a = MathTex(lhs, font_size=font_size, color=color)
    r = MathTex(rel, font_size=font_size, color=color)
    b = MathTex(rhs, font_size=font_size, color=color, **tex_kw)
    _tex_row([a, r, b], 0)
    line = VGroup(a, r, b)
    line.lhs, line.rel, line.body = a, r, b
    return line.move_to(np.zeros(3))


def _box(m):
    return np.array([m.get_left()[0], m.get_bottom()[1], m.get_right()[0], m.get_top()[1]])


def _clear_from(start, moved, other, a0=0.6, pad=0.06):
    """The earliest fraction of the drop play from which the copy (a straight, smooth move from
    `start` to `moved`) no longer touches `other`'s box, if ≤ 0.85; else None."""
    sb, mb, ob = _box(start), _box(moved), _box(other)
    for a in (a0, 0.7, 0.8, 0.85):
        ok = True
        for x in np.linspace(a, 1.0, 9):
            p = smooth(x)
            b = sb + p * (mb - sb)
            if (b[0] < ob[2] + pad and b[2] > ob[0] - pad and b[1] < ob[3] + pad and b[3] > ob[1] - pad):
                ok = False
                break
        if ok:
            return a
    return None


def _ghost_until(start, moved, others, cap=0.92, pad=0.02):
    """The fraction of the slide at which the copy (straight, smooth, start → moved) has left
    every box in `others`: _FlyCopy keeps it a faint ghost (≤ 0.25) until then."""
    sb, mb = _box(start), _box(moved)
    obs = [_box(o) for o in others]
    for x in np.linspace(0.0, cap, 93):
        b = sb + smooth(x) * (mb - sb)
        if not any(b[0] < o[2] + pad and b[2] > o[0] - pad and b[1] < o[3] + pad and b[3] > o[1] - pad
                   for o in obs):
            return float(max(x, 0.2))
    return cap


def derive_step(scene, src, new, rel="=", where="below", i=None, top=None, pitch=None,
                label=None, highlight=None, hl_color=YELLOW, new_color=None, keep_colors=True,
                dim=True, run_time=None, hold=0.4, extra=(), indent=0.0, **tex_kw):
    """One step of a derivation that keeps the original on screen (DEEP_STYLE §14; never
    transform an expression in place). It calls scene.play itself (2 plays, 3 with highlight):
      1. (highlight) the parts of `src` that will change take `hl_color` (a colour that stays:
         it shows where the change came from), then `hold` s of stillness;
      2. a copy of src's expression drops to the new line's place and the relation ("=") fades
         in as soon as the copy is clear of its spot (beside: the "=" fades in first and the
         copy slides past it as a faint ghost, brightening once clear);
      3. the copy is edit()ed into the new expression: shared glyphs slide, changed ones fade
         out where they are and the new ones fade in where they land (no glyph crosses another),
         the step label drops into the gap, and src dims to EARLIER (0.4) as the new line lands.
    src itself never moves or changes shape. Returns the new line, VGroup(rel, body) with .rel
    .body .label (the step label, not part of the line; None without one): pass it as `src` of
    the next step, which copies only its body and puts its "=" under this one.
      src       the line on screen: an eq_line, a line from derive_step, or a plain MathTex
      new       TeX string, list of TeX strings (MathTex args), or a ready MathTex (not on screen)
      rel       TeX of the relation ("=", r"\\Rightarrow", r"\\approx"); None for none
      where     "below": the next line (column line `i` if given, else one COL_PITCH below src,
                more if the lines are tall); "beside": a short rewrite on src's own line,
                "src = new" (keep it short: it must fit before x 6.6)
      label     step label (≤ 5 words), DIM in the gap above the new line ("below" only)
      highlight True: the glyphs that will change (the same diff edit() uses); or a list of
                src parts (sub-mobjects, or TeX keys isolated in src with substrings_to_isolate)
      hl_color  YELLOW; a substitution passes the substituted thing's colour (its rail entry's)
      new_color True: the new glyphs take hl_color too (the substituted-in part); or a colour
      keep_colors  shared glyphs keep their colour from src (a coloured term stays coloured),
                unless `new` colours them itself (tex_to_color_map)
      dim       dim src to EARLIER as the new line lands (an earlier line, DEEP_STYLE §6)
      run_time  the whole move (highlight 0.8 + drop 1.0 + edit 1.5 by default), split in
                those proportions: run_time=c.until("next cue") follows the narration
      extra     animations to play with the first play (rail_highlight(rl, key), a flash)
      indent    when src has no relation of its own: the new relation's x offset from src's left
      tex_kw    MathTex options for `new` (tex_to_color_map, substrings_to_isolate)"""
    if where not in ("below", "beside"):
        raise ValueError("where must be 'below' or 'beside'")
    s_body = src.body if getattr(src, "body", None) is not None else src
    s_rel = getattr(src, "rel", None)
    fs = getattr(s_body, "font_size", None) or COL_SIZE   # (a MathTex part has no font_size)
    if isinstance(new, Mobject):
        body = new
    else:
        body = MathTex(*([new] if isinstance(new, str) else list(new)), font_size=fs, **tex_kw)
    rel_m = MathTex(rel, font_size=fs) if rel else None

    # ── where the new line goes ──
    if where == "beside":
        _tex_row([s_body, rel_m, body] if rel_m else [s_body, body], 0)
    else:
        if rel_m is not None:
            if s_rel is not None:
                rel_m.shift((s_rel.get_center()[0] - rel_m.get_center()[0]) * RIGHT)
            else:
                rel_m.shift((s_body.get_left()[0] + indent - rel_m.get_left()[0]) * RIGHT)
            _tex_row([rel_m, body], 0)
        else:
            body.shift((s_body.get_left()[0] + indent - body.get_left()[0]) * RIGHT)
        grp = VGroup(rel_m, body) if rel_m is not None else VGroup(body)
        if i is not None:
            y = col_point(i, top, pitch)[1]
        else:
            y = s_body.get_center()[1] - (COL_PITCH if pitch is None else pitch)
        grp.shift((y - body.get_center()[1]) * UP)
        gap = 0.42 if label else 0.25            # room for the step label between the lines
        over = grp.get_top()[1] - (src.get_bottom()[1] - gap)
        if i is None and over > 0:
            grp.shift(over * DOWN)
    line = VGroup(rel_m, body) if rel_m is not None else VGroup(body)

    # ── what changes (edit()'s own diff) ──
    sp, tp, pairs = edit_pairs(s_body, body)
    if len(pairs) < 0.5 * min(len(sp), len(tp)):   # edit() swaps outright
        pairs = []
    used_s, used_t = {a for a, _ in pairs}, {b for _, b in pairs}
    if keep_colors:          # a coloured term keeps its colour in the new line (unless new colours it)
        hexes = [m.get_fill_color().to_hex().upper() for m in tp]
        default = max(set(hexes), key=hexes.count)
        fg = ManimColor(FG).to_hex().upper()
        for a, b in pairs:
            c = sp[a].get_fill_color()
            if c.to_hex().upper() != fg and hexes[b] == default:
                tp[b].set_color(c)
    if new_color:
        nc = hl_color if new_color is True else new_color
        for j, m in enumerate(tp):
            if j not in used_t:
                m.set_color(nc)

    w = (DERIVE_HL_RT if highlight else 0.0, DERIVE_DROP_RT, DERIVE_EDIT_RT)
    k = 1.0 if run_time is None else run_time / sum(w)
    t_hl, t_drop, t_edit = (x * k for x in w)
    extra = list(extra)

    # 1. highlight what will change
    if highlight:
        if highlight is True:
            marks = [m for a, m in enumerate(sp) if a not in used_s]
        else:
            marks = []
            for h in highlight:
                if isinstance(h, str):
                    from lib.effects import select
                    try:
                        groups = select(s_body, h)
                    except KeyError as e:
                        raise KeyError(f"derive_step highlight {h!r}: {e}") from None
                    marks += [m for g in groups for m in g.family_members_with_points()]
                else:
                    marks += list(h.family_members_with_points())
        if marks:
            scene.play(*[m.animate.set_color(hl_color) for m in marks], *extra, run_time=t_hl)
            extra = []
            if hold > 0:
                scene.wait(hold)

    # 2. a copy of the expression drops (or slides) to the new line, aligned on the longest
    #    shared run of glyphs, never left of the body (the relation sits there)
    kp, kt = glyph_classes(sp, tp)
    from difflib import SequenceMatcher
    run = SequenceMatcher(None, kp, kt, autojunk=False).find_longest_match(0, len(kp), 0, len(kt))
    if run.size >= 2:
        delta = tp[run.b].get_center() - sp[run.a].get_center()
    else:
        delta = np.array([body.get_left()[0] - s_body.get_left()[0],
                          body.get_center()[1] - s_body.get_center()[1], 0.0])
    moved = s_body.copy().shift(delta)
    for m in moved.family_members_with_points():          # the new line is the bright one
        if m.get_fill_opacity() > 0:
            m.set_fill(opacity=1)
    if moved.get_left()[0] < body.get_left()[0]:
        moved.shift((body.get_left()[0] - moved.get_left()[0]) * RIGHT)
    _on_screen(moved, margin=7.11 - TEXT_X)
    fly_copy = _FlyCopy(s_body, moved, path_arc=0.0)
    drop = [fly_copy]
    rel_in = None
    if rel_m is not None and where == "beside":
        # "=" first; the copy slides past it as a faint ghost and brightens once clear of both
        fly_copy.a_clear = _ghost_until(s_body, moved, [s_body, rel_m])
        drop += during(FadeIn(rel_m), 0.0, 0.3)
    elif rel_m is not None:
        a0 = _clear_from(s_body, moved, rel_m)
        if a0 is not None:
            drop += during(FadeIn(rel_m), a0, 1.0)
        else:
            rel_in = during(FadeIn(rel_m), 0.0, 0.3)
    scene.play(*drop, *extra, run_time=t_drop)

    # 3. rewrite the copy; label in; src dims as the new line lands
    step = edit(moved, body)
    for a in step:
        a.dwell_exempt = True    # its glyphs were on screen all along, on src
    more = list(rel_in or [])
    lab = None
    if label and where == "below":
        lab = step_label(label, between=(src, VGroup(line.copy(), moved.copy())),
                         x=min(src.get_left()[0], line.get_left()[0]) + 0.18)
        more += during(appear(lab, shift=0.08 * DOWN), 0.0, 0.45)
    elif label:
        raise ValueError("derive_step: a step label goes with where='below' only")
    if dim:
        from lib.kit import restyle
        more += during(restyle(src, EARLIER), 0.7, 1.0)
    scene.play(*step, *more, run_time=t_edit)
    scene.remove(*line.get_family())
    scene.add(line)              # one on-screen object (a later FadeOut(line) takes it all)
    line.rel, line.body, line.label = rel_m, body, lab
    return line


# ── board helpers (from the pilot's arrow kit, ch2_s3_velocity) ─────────────────
def arrow_between(start, end, color, width=6, z=-2):
    """The house arrow (stroke 6, tip 0.24, no buff), for still arrows on the board. z −2 puts
    it under the panels (rail −1, cards), so a long arrow passes behind them."""
    a = Arrow(start, end, buff=0, stroke_width=width, tip_length=0.24,
              max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=40, color=color)
    a.set_z_index(z)
    return a


def clock(t):
    """Make ValueTracker t advance in real time while it runs (it starts stopped); add t to the
    scene. run_clock(t) / run_clock(t, False) start and stop it. For a deterministic freeze,
    stop it, then play t.animate.set_value(exact)."""
    t.running = False

    def tick(m, dt):
        if m.running:
            m.increment_value(dt)
    t.add_updater(tick)
    return t


def run_clock(t, on=True):
    t.running = on
