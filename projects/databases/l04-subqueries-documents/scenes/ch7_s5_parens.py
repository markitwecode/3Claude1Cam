"""Chapter 7, scene 5: the arrows bind loosely. Clips c7.parens.1 – c7.parens.5.

Exports (for ch7_s8, via `load_scene("ch7_s5_parens")`):
  recap_thumb()  static VGroup at ORIGIN: `(movie->>'year')::INTEGER` with YELLOW parentheses,
                 the RED conversion error crossed out behind it; .code .err
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S4 = load_scene("ch7_s4_cast")

SW_NOPAREN = S4.SW_SRC.replace("(movie->>'year')::INTEGER", "movie->>'year'::INTEGER")

KID_SRC = ("SELECT movie->>'title' AS title\n"
           "FROM   movies\n"
           "WHERE movie->>'title' = 'The Kid'\n"
           "  AND movie->>'type' = 'movie';")
KID_PARSE = ("SELECT movie->>'title' AS title\n"
             "FROM   movies\n"
             "WHERE ((movie->>'title' = 'The Kid')\n"
             "  AND movie)->>'type' = 'movie';")
KID_FIX = ("SELECT movie->>'title' AS title\n"
           "FROM   movies\n"
           "WHERE (movie->>'title') = 'The Kid'\n"
           "  AND (movie->>'type') = 'movie';")

ERR_YEAR = ["Conversion Error:",
            "Could not convert string 'year' to INT32"]
PTR_YEAR = "LINE 4:   AND movie->>'year'::INTEGER >= 2000"
ERR_KID = ["Conversion Error:",
           "Failed to cast value to numerical:",
           '{"movie_id":"tt2112124","title":"Chennai Express",...',
           "when casting from source column movie"]


def paren_glyphs(code, line):
    """Every ( and ) glyph on one line of a Code."""
    out = []
    for ch in "()":
        k = 0
        while True:
            try:
                out.append(code.find(ch, line=line, nth=k))
            except ValueError:
                break
            k += 1
    return out


def year_cast(size=44):
    c = Code("(movie->>'year')::INTEGER", size=size)
    c.find("(").set_color(YELLOW)
    c.find(")").set_color(YELLOW)
    return c


def recap_thumb():
    code = year_cast(44)
    err = Mono("Conversion Error", 32, RED).set_opacity(0.6)
    strike = Line(err.get_left() + 0.1 * LEFT, err.get_right() + 0.1 * RIGHT).set_stroke(RED, 5)
    e = VGroup(err, strike)
    g = VGroup(e, code).arrange(DOWN, buff=0.35).move_to(ORIGIN)
    e.shift(0.6 * RIGHT)
    g.code, g.err = code, e
    return g


def shake(glyphs, amp=0.08, n=4, to=RED):
    anims = []
    for g in glyphs:
        base = g.get_center().copy()
        c0 = ManimColor(g.get_color())

        def upd(m, a, base=base, c0=c0):
            m.move_to(base + amp * np.sin(a * n * TAU) * (1 - a) * RIGHT)
            m.set_color(interpolate_color(c0, ManimColor(to), min(1, 2 * a)))
        anims.append(UpdateFromAlphaFunc(g, upd))
    return anims


def doc_card():
    box = RoundedRectangle(corner_radius=0.15, width=3.8, height=1.5).set_stroke(TEAL, 3).set_fill(BG, 1)
    lines = VGroup(Mono('{"title": …,', 28, TEAL), Mono(' "year": …, …}', 28, TEAL))
    lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(box)
    return VGroup(box, lines)


class Parens(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c7.parens.1: the Star Wars query, parentheses dropped ─────────────────
    def clip1(self):
        q = S4.star_wars_query(size=28).move_to(1.95 * UP)
        self.q = q
        with self.say("c7.parens.1") as c:
            self.play(*appear(q, shift=None), run_time=1.0)
            c.wait_until("Every arrow")
            boxes = [token_box(q.spans[0], q.line(2)), token_box(q.spans[1], q.line(3))]
            self.play(*[FadeIn(b) for b in boxes], *recolor([g for p in q.parens for g in p], YELLOW),
                      run_time=min(1.5, c.until("drop")))
            c.wait_until("drop")
            q2 = Code(SW_NOPAREN, size=28)
            q2.align_to(q, LEFT).align_to(q, UP)
            self.play(*during(disappear(boxes[1]), 0, 0.45), *edit(q, q2),
                      run_time=min(1.6, c.until("cast")))
            self.q, self.box_title = q2, boxes[0]
            c.wait_until("cast")
            msg = VGroup(*[Mono(s, 28, RED) for s in ERR_YEAR]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            ptr = Mono(PTR_YEAR, 28, FG).set_opacity(0.75)
            colon = select(ptr, "::")[0][0]
            caret = Mono("^", 28, RED)
            err = VGroup(msg, ptr).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            caret.next_to(ptr, DOWN, buff=0.08).set_x(colon.get_x())
            err.add(caret)
            err.move_to(1.2 * DOWN).align_to(q2, LEFT)
            self.err = err
            self.play(*appear(msg, VGroup(ptr, caret), lag=0.4), run_time=1.4)

    # ── c7.parens.2: the cast grabs the key ───────────────────────────────────
    def clip2(self):
        q = self.q
        with self.say("c7.parens.2") as c:
            cast = q.find("::INTEGER", line=3)
            self.play(FlashAround(cast, run_time=1.5, time_width=1.5), *recolor(cast, GOLD), run_time=1.5)
            c.wait_until("group")
            src = q.find("movie->>'year'::INTEGER", line=3)
            hero = Code("movie->>'year'::INTEGER", size=48).move_to(1.3 * DOWN)
            hero.find("::INTEGER").set_color(GOLD)
            self.play(*during(disappear(self.err), 0, 0.4), FlashAround(src, run_time=1.4, time_width=1.5),
                      *during(appear(hero, shift=None), 0.4, 1), run_time=1.6)
            hero2 = Code("movie->>('year'::INTEGER)", size=48).move_to(hero)
            hero2.find("::INTEGER").set_color(GOLD)
            hero2.find("(").set_color(RED)
            hero2.find(")").set_color(RED)
            self.play(*edit(hero, hero2), run_time=min(1.5, c.until("First it casts")))
            inner = hero2.find("('year'::INTEGER)")
            brace = span_brace(inner.get_corner(DL), inner.get_corner(DR), color=RED)
            tag = T("the key, cast to a number?", 32, RED).next_to(brace, DOWN, buff=0.15)
            c.wait_until("First it casts")
            self.play(GrowFromCenter(brace), *appear(tag), run_time=1.2)
            c.wait_until("fails")
            self.play(*shake(hero2.find("'year'")), run_time=1.0)
            self.hero = VGroup(hero2, brace, tag)

    # ── c7.parens.3: The Kid, and Chennai Express ─────────────────────────────
    def clip3(self):
        with self.say("c7.parens.3") as c:
            kq = Code(KID_SRC, size=36).move_to(2.05 * UP)
            sweep_clear(self, *appear(kq, shift=None), run_time=min(1.6, c.until("Find the movie")))
            self.kq = kq
            c.wait_until("fail")
            lines = [Mono(s, 28, RED) for s in ERR_KID]
            err = VGroup(*lines).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            err.move_to(0.95 * DOWN)
            self.play(*appear(err, shift=None), run_time=1.2)
            c.wait_until("Chennai Express")
            ce = select(lines[2], "Chennai Express")[0]
            ul = underline(ce, YELLOW, buff=0.1)
            self.play(Create(ul), FlashUnder(ce, color=YELLOW, run_time=1.2), run_time=1.2)
            self.err2 = VGroup(err, ul)

    # ── c7.parens.4: AND grabs the bare document ──────────────────────────────
    def clip4(self):
        kq = self.kq
        with self.say("c7.parens.4") as c:
            andw = kq.find("AND", line=3)
            self.play(FlashAround(andw, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("grab")
            kp = Code(KID_PARSE, size=36).align_to(kq, LEFT).align_to(kq, UP)
            for g in paren_glyphs(kp, 2) + paren_glyphs(kp, 3):
                g.set_color(RED)
            self.play(*during(disappear(self.err2), 0, 0.4), *during(edit(kq, kp), 0.3, 1), run_time=1.8)
            # the hero row: left operand, AND, a slot for the bare movie
            left = Code("(movie->>'title' = 'The Kid')", size=28)
            left.find("(").set_color(RED)
            left.find(")").set_color(RED)
            and2 = Code("AND", size=28)
            card = doc_card()
            row = VGroup(left, and2, card).arrange(RIGHT, buff=0.45).move_to(1.0 * DOWN)
            mv = Code("movie", size=28).move_to(card)
            c.wait_until("comparison")
            self.play(FlashAround(kp.find("(movie->>'title' = 'The Kid')", line=2), run_time=1.5),
                      *appear(left, and2, lag=0.3), run_time=1.5)
            c.wait_until("on its right")
            self.play(*fly(kp.find("movie", line=3), mv), run_time=min(1.5, c.until("doc")))
            c.wait_until("doc")
            self.play(*swap(mv, card, shift=None), run_time=1.4)
            ltag = VGroup(T("TRUE", 30, GREEN), T("or", 30, DIM), T("FALSE", 30, RED)).arrange(RIGHT, buff=0.18)
            ltag.next_to(left, DOWN, buff=0.45)
            rtag = T("TRUE or FALSE?", 32, RED).next_to(card, DOWN, buff=0.3)
            c.wait_until(own_word=rtag, cue="true or false")
            self.play(*appear(ltag, rtag, lag=0.4), run_time=1.2)
            c.wait_until("fix")
            kf = Code(KID_FIX, size=36).align_to(kp, LEFT).align_to(kp, UP)
            for g in paren_glyphs(kf, 2) + paren_glyphs(kf, 3):
                g.set_color(YELLOW)
            self.play(*edit(kp, kf), run_time=1.5)
            res = VGroup(Mono("title", 30, DIM), Mono("The Kid", 44, GREEN)).arrange(DOWN, buff=0.25)
            res.move_to(1.1 * DOWN)
            self.play(*during(disappear(left, and2, card, ltag, rtag), 0, 0.45),
                      *during(appear(res), 0.5, 1), run_time=min(1.2, c.until(None)))
            self.kf, self.res = kf, res

    # ── c7.parens.5: the rule ─────────────────────────────────────────────────
    def clip5(self):
        with self.say("c7.parens.5") as c:
            note = T("DuckDB: arrows bind more tightly from version 2.0", 30, DIM).move_to(3.1 * DOWN)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("rule")
            l1 = T("Arrow operators have low precedence:", 44)
            l2 = T("always use parentheses!", 44, YELLOW)
            ex = year_cast(40)
            body = VGroup(l1, l2, ex).arrange(DOWN, buff=0.4)
            frame = RoundedRectangle(corner_radius=0.2, width=body.width + 1.0,
                                     height=body.height + 0.9).set_stroke(YELLOW, 3)
            card = VGroup(frame, body).move_to(0.35 * UP)
            body.move_to(frame)
            sweep_clear(self, time_span(FadeIn(card), 0.6, 1.4), keep=[note], run_time=1.4)  # early: rule card shown whole on {rule}, read out next
            tag = T("the lecturer, live, 00:43", 30, DIM).move_to(note)
            c.wait_until(own_word=tag, cue="live")
            self.play(*swap(note, tag), run_time=1.2)
        self.wait(1.5)
