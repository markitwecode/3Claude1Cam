"""Helpers that every scene kept re-implementing, promoted here (Oct 2026) so scene agents
import them instead of copying them out of other scenes. Each one is taken verbatim from a
finished, rendered scene (source noted). `from lib.kit import *`.

Rule they all follow (LESSONS.md): to animate *parts* of an on-screen object (glyphs of a
Code, cells of a chain), pass one animation per part to play(); never wrap the parts in a
VGroup/AnimationGroup (manim pulls them out of their parent → ghosts, wrong layering).
"""
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, Brace, CapStyleType, FadeOut, LaggedStart, Line, Rectangle,
    Transform, Triangle, VGroup, VMobject,
)
from manim.animation.animation import prepare_animation

from lib.effects import FlashAround, VShowPassingFlash
from lib.moves import *  # noqa: F401,F403  (the transition vocabulary: appear, swap, edit, fly, …)
from lib.moves import __all__ as _moves_all
from lib.moves import _span
from lib.style import DIM, GREEN, RED, YELLOW

__all__ = [
    "chars", "recolor", "flash", "token_box", "restyle", "set_alpha", "underline", "marker",
    "above", "check_mark", "cross_mark", "span_brace", "flash_along", "sweep_clear", "settle",
    "DIMMED", *_moves_all,
]

DIMMED = 0.25  # spotlight opacity for everything that isn't the focus (PATTERNS P9)


# ── code glyphs (ch1_s3_compare) ────────────────────────────────────────────────
def chars(code, ch):
    """Every glyph of `code` (a lib.style.Code) that is the character `ch`, as a list."""
    return [g for k in range(code.src.count(ch)) for g in code.find(ch, nth=k)]


def recolor(glyphs, color):
    """One colour change per glyph: self.play(*recolor(code.find("xs"), TEAL))."""
    return [g.animate.set_color(color) for g in glyphs]


def flash(mobs, color=YELLOW, **kw):
    """3b1b's FlashAround on each item; it removes itself (P6)."""
    return [FlashAround(m, color=color, **kw) for m in mobs]


def token_box(glyphs, code, color=YELLOW, pad=0.22, height=None):
    """The sliding highlight box (P8): thin stroke, faint fill, behind the text, as tall as
    the line. Slide it with box.animate.become(token_box(other, code)) or Transform.
    `code` sets the height (pass one line, e.g. code.line(2), for multi-line code)."""
    g = VGroup(*glyphs)
    r = Rectangle(width=max(g.width + pad, 0.42), height=height or (code.height + 0.24),
                  stroke_color=color, stroke_width=2).set_fill(color, opacity=0.25)
    return r.move_to([g.get_x(), code.get_y(), 0]).set_z_index(-1)


# ── dim / restore / move in one Transform (ch1_s3_compare) ──────────────────────
def restyle(mob, op=None, outline=None, width=None, fill=None, shift=None):
    """One Transform that dims/restores (P9), recolours and moves `mob` together, so no two
    animations fight over the same object. Opacity goes on the fill of filled parts (text,
    arrow tips) and on the stroke of outlines, which stay unfilled; `outline`/`width`
    restyle the outlines, `fill` recolours the filled parts."""
    from manim.mobject.svg.svg_mobject import VMobjectFromSVGPath
    t = mob.copy()
    for leaf in t.family_members_with_points():
        # a text glyph is a filled part even when faded to 0 (so op=1 brings it back; 2026-11-01:
        # it used to count as an outline and only its stroke, which glyphs don't have, was restored)
        if leaf.get_fill_opacity() > 0 or isinstance(leaf, VMobjectFromSVGPath):
            if fill is not None:
                leaf.set_color(fill)
            if op is not None:
                leaf.set_opacity(op)
        else:
            if outline is not None or width is not None:
                leaf.set_stroke(color=outline, width=width)
            if op is not None:
                leaf.set_stroke(opacity=op)
    if shift is not None:
        t.shift(shift)
    return Transform(mob, t)


def set_alpha(mobs, op):
    """Dim (op=DIMMED) or restore (op=1) several objects: self.play(*set_alpha([a, b], 0.25))."""
    return [restyle(m, op) for m in mobs]


# ── small marks (ch1_s3_compare, ch2_s2_null, ch1_s5_cells) ─────────────────────
def underline(mob, color, buff=0.14):
    return Line(mob.get_corner(LEFT + DOWN), mob.get_corner(RIGHT + DOWN), color=color,
                stroke_width=5).shift(DOWN * buff)


def marker(color=YELLOW, scale=0.24):
    """A downward-pointing triangle that sits above a slot or a box (put it at above(box))."""
    return Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(scale).rotate(PI)


def above(mob, buff=0.2):
    """Where a marker's centre goes when it sits just above `mob`."""
    return mob.get_top() + UP * (buff + 0.18)


def check_mark(color=GREEN):
    m = VMobject().set_points_as_corners([[-0.24, 0.0, 0], [-0.07, -0.19, 0], [0.26, 0.23, 0]])
    return m.set_stroke(color, 8).set_cap_style(CapStyleType.ROUND)


def cross_mark(color=RED, r=0.19):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_stroke(color, 8)


def span_brace(left_pt, right_pt, direction=DOWN, color=DIM, inset=0.06, buff=0.18):
    """A brace under (or over) the horizontal span left_pt..right_pt (e.g. a chain's tail)."""
    line = Line(left_pt + RIGHT * inset, right_pt + LEFT * inset)
    return Brace(line, direction, buff=buff, color=color)


def flash_along(src, dst, color=YELLOW, run_time=1.0):
    """A bright pulse travelling along one pointer arrow, src cell -> dst cell/Nil (P6)."""
    path = Line(src.tail_start(), dst.entry()).set_stroke(color, 8)
    return VShowPassingFlash(path, time_width=0.6, run_time=run_time)


# ── board management (ch1_s3_compare, ch3_s2_nlength) ───────────────────────────
def sweep_clear(scene, *incoming, keep=(), run_time=1.2):
    """Clear the board in a lagged sweep (P18), in the same play as whatever needs the
    space: sweep_clear(self, time_span(FadeIn(new), 0.6, 1.2)). `keep` survives.
    The sweep finishes in the first half of the play and incoming animations without their own
    time_span/during start at half time, so old and new never overlap (glitch study 2026-10-28:
    the sweep used to run to the end, ghosting under the new content)."""
    keep_ids = {id(m) for k in keep for m in k.get_family()}
    gone = [m for m in list(scene.mobjects) if id(m) not in keep_ids]
    anims = [_span(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.1), 0.0, 0.5)] if gone else []
    for a in incoming:
        a = prepare_animation(a)
        timed = getattr(a, "rel_span", None) or getattr(a, "abs_span", None)
        anims.append(a if timed else _span(a, 0.5, 1.0))
    scene.play(*anims, run_time=run_time)


def settle(scene, group, add=(), drop=()):
    """After animating pieces into place one by one: make them part of `group` (and drop
    replaced ones), then put the whole group back on screen as one object, so later
    FadeOut(group)/restyle(group) catch every piece (no ghosts)."""
    group.remove(*drop)
    scene.remove(*group.get_family(), *add)
    group.add(*add)
    scene.add(group)
