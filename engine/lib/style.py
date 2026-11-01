"""Shared look for every scene: palette, fonts, OCaml code blocks, cons cells.

Every scene should `from lib.style import *` and build visuals from these pieces,
so the whole video reads as one consistent piece.
"""
import re

import manimpango
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, Arrow, Dot, Line, Rectangle, Square, Text, VGroup,
    VMobject, config,
)
from pygments.lexers import get_lexer_by_name
from pygments.token import Comment, Keyword, Name, Number, Operator, String

# ── fonts ──────────────────────────────────────────────────────────────────────
_CMU = "/usr/local/texlive/2023/texmf-dist/fonts/opentype/public/cm-unicode/"
for _f in ("cmunrm", "cmunbx", "cmunti", "cmunbi"):
    manimpango.register_font(_CMU + _f + ".otf")
SERIF = "CMU Serif"  # 3b1b-style Computer Modern for prose and labels
MONO = "Menlo"       # code

# ── palette (3b1b-flavoured) ───────────────────────────────────────────────────
BG = "#0F1115"
FG = "#ECECEC"
DIM = "#7A7F87"
BLUE = "#58C4DD"     # structure: cells, keywords
TEAL = "#5CD0B3"     # nil / list syntax / "new" things
YELLOW = "#F4D345"   # attention, function names
GOLD = "#F0AC5F"     # numbers, costs
GREEN = "#83C167"    # good / types
RED = "#FC6255"      # bad / errors
PINK = "#E58BD7"     # type variables
PURPLE = "#9A72AC"

config.background_color = BG


def _tilde(s):
    return s.replace("~", "\u223c")


def T(text, size=36, color=FG, **kw):
    """Prose / label text in Computer Modern. An ASCII "~" becomes "∼" (U+223C): CMU Serif draws
    "~" as a raised accent at cap height (glitch study 2026-10-28)."""
    for k in ("t2c", "t2f", "t2g", "t2s", "t2w"):
        if isinstance(kw.get(k), dict):
            kw[k] = {_tilde(key): v for key, v in kw[k].items()}
    return Text(_tilde(text), font=SERIF, font_size=size, color=color, **kw)


def Mono(text, size=30, color=FG, **kw):
    return Text(text, font=MONO, font_size=size, color=color, **kw)


# ── OCaml code ─────────────────────────────────────────────────────────────────
try:   # the project's language (project.json "code_language"); the Code colouring is tuned for OCaml
    from lib.paths import config
    _LANG = config().get("code_language") or "ocaml"   # "" = no code on screen
except SystemExit:
    _LANG = "ocaml"
_LEXER = get_lexer_by_name(_LANG)
_LEXERS = {_LANG: _LEXER}


def _lexer(name):
    if name not in _LEXERS:
        _LEXERS[name] = get_lexer_by_name(name)
    return _LEXERS[name]


_TYPE_WORDS = {"int", "bool", "string", "char", "list", "float", "unit", "fun"}


def _token_color(ttype, value):
    if value.startswith("'") and len(value) <= 3 and value[1:].isalpha():
        return PINK                                   # 'a, 'b (type variables)
    if ttype in Comment:
        return DIM
    if ttype in Keyword.Type or value in _TYPE_WORDS:
        return GREEN
    if ttype in Keyword:
        return BLUE
    if ttype in Number:
        return GOLD
    if ttype in String:
        return GOLD
    if ttype in Name.Builtin or value in ("[]", "::"):
        return TEAL
    if ttype in Operator:
        return "#BBBBBB" if value != "::" else TEAL
    return FG


class Code(VGroup):
    """Syntax-highlighted OCaml, one Text per block so indentation is exact.

    code.line(i)            -> glyphs of line i (0-based)
    code.find("x :: xs", line=2, nth=0) -> glyphs of that substring
    """

    def __init__(self, src, size=28, line_spacing=0.9, lang=None, **kw):
        # lang: a Pygments lexer name for this block only (e.g. "sql" in a Cypher project)
        super().__init__(**kw)
        lexer = _lexer(lang) if lang else _LEXER
        self.src = src.strip("\n")
        self.text = Text(self.src, font=MONO, font_size=size, color=FG, line_spacing=line_spacing)
        self.add(self.text)
        # map every non-whitespace character in src to its glyph index
        self._glyph_of = {}
        g = 0
        for i, ch in enumerate(self.src):
            if not ch.isspace():
                self._glyph_of[i] = g
                g += 1
        # colour tokens
        pos = 0
        prev_kw = None
        for ttype, value in lexer.get_tokens(self.src):
            color = _token_color(ttype, value)
            if ttype in Name and prev_kw in ("let", "rec"):
                color = YELLOW                          # name being defined
            if value.strip():
                prev_kw = value if value in ("let", "rec") else None
            self._span(pos, pos + len(value)).set_color(color)
            pos += len(value)
        # the lexer splits these oddly; colour them directly
        for pattern, color in ((r"'[a-z]\b(?!')", PINK), (r"::", TEAL), (r"\[\]", TEAL)):
            for m in re.finditer(pattern, self.src):
                self._span(m.start(), m.end()).set_color(color)

    def _span(self, a, b):
        idx = [self._glyph_of[i] for i in range(a, b) if i in self._glyph_of]
        return VGroup(*[self.text[i] for i in idx])

    def _line_bounds(self, n):
        starts = [0] + [m.end() for m in re.finditer("\n", self.src)]
        a = starts[n]
        b = self.src.find("\n", a)
        return a, (len(self.src) if b == -1 else b)

    def line(self, n):
        return self._span(*self._line_bounds(n))

    def find(self, sub, line=None, nth=0):
        a0, b0 = self._line_bounds(line) if line is not None else (0, len(self.src))
        start = a0
        for _ in range(nth + 1):
            i = self.src.find(sub, start, b0)
            if i == -1:
                raise ValueError(f"{sub!r} not found in code")
            start = i + 1
        return self._span(i, i + len(sub))


# ── cons cells ─────────────────────────────────────────────────────────────────
CELL = 1.0      # value-box side
PTR_W = 0.5     # pointer-box width
LINK = 0.8      # arrow length between cells


def value_label(v, size=42, color=FG):
    s = str(v)
    slant = "ITALIC" if s.isalpha() and len(s) == 1 else "NORMAL"
    return Text(s, font=SERIF, font_size=size, color=color, slant=slant)


class ConsCell(VGroup):
    """[ value | • ]  — the dot is where the tail pointer starts."""

    def __init__(self, value, color=BLUE, fill=BG, **kw):
        super().__init__(**kw)
        self.value = value
        self.box = Square(CELL, stroke_color=color, stroke_width=3, fill_color=fill, fill_opacity=1)
        self.ptr = Rectangle(width=PTR_W, height=CELL, stroke_color=color, stroke_width=3,
                             fill_color=fill, fill_opacity=1).next_to(self.box, RIGHT, buff=0)
        self.dot = Dot(self.ptr.get_center(), radius=0.07, color=FG)
        self.label = value_label(value).move_to(self.box)
        self.add(self.box, self.ptr, self.dot, self.label)

    def tail_start(self):
        return self.dot.get_center()

    def entry(self):
        """Where an incoming arrow should land."""
        return self.box.get_left()


class Nil(VGroup):
    """The empty list, drawn as [] in the list-syntax colour."""

    def __init__(self, size=42, **kw):
        super().__init__(**kw)
        self.label = Text("[]", font=MONO, font_size=size, color=TEAL)
        self.add(self.label)

    def entry(self):
        return self.label.get_left() + LEFT * 0.05


def link(src_cell, dst, color=FG, follow=False):
    """Pointer arrow from a cell's dot to another cell/nil.

    follow=True re-draws it every frame so it tracks cells moved independently
    (it then ignores colour animations — recolour by rebuilding instead).
    """

    def build():
        start = src_cell.tail_start()
        end = dst.entry()
        return Arrow(start, end, buff=0, stroke_width=3, color=color,
                     max_tip_length_to_length_ratio=0.3, tip_length=0.16)

    arrow = build()
    if follow:
        arrow.add_updater(lambda a: a.become(build()))
    return arrow


class ConsChain(VGroup):
    """A whole linked list: cells left→right, arrows between them, nil at the end.

    chain.cells[i], chain.arrows[i] (arrow out of cell i), chain.nil
    """

    def __init__(self, values, color=BLUE, with_nil=True, follow=False, **kw):
        super().__init__(**kw)
        self.cells = [ConsCell(v, color=color) for v in values]
        x = 0.0
        for c in self.cells:
            c.move_to(RIGHT * x, aligned_edge=LEFT)
            x += CELL + PTR_W + LINK
        self.nil = Nil() if with_nil else None
        if self.nil is not None:
            self.nil.move_to(RIGHT * (x + 0.25))
        targets = self.cells[1:] + ([self.nil] if self.nil is not None else [])
        self.arrows = [link(c, t, follow=follow) for c, t in zip(self.cells, targets)]
        self.add(*self.cells, *self.arrows)
        if self.nil is not None:
            self.add(self.nil)
        self.move_to(ORIGIN)


def label_pointer(text, target, direction=UP, color=YELLOW, size=30, length=0.6):
    """A name (like `x`) with a short arrow pointing at a cell."""
    lab = T(text, size=size, color=color)
    tip = target.get_edge_center(direction)
    lab.move_to(tip + direction * (length + 0.3))
    arr = Arrow(lab.get_edge_center(-direction), tip, buff=0.06, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.35, tip_length=0.15)
    return VGroup(lab, arr)
