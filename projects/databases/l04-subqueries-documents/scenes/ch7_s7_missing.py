"""Chapter 7, scene 7: Missing keys. Clips c7.missing.1 – c7.missing.4.

Shared pieces (`from lib.paths import load_scene; M = load_scene("ch7_s7_missing")`):
- `recap_thumb()` -> static VGroup at ORIGIN: the BLUE semijoin 1,086 card beside the TEAL
  json_exists 1,086 card, and under them `birth_year` -> PINK NULL. `.cards .typo`.
- `teal_card()`, `blue_card()` -> the two 1,086 cards (VGroup; `.frame .head .num`).
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

D = load_scene("ch4_s3_movie")

CARD_SIZE = 22
CARD_W = 3.95


def person_src(keys, blank=False):
    lines = ["{"]
    for i, k in enumerate(keys):
        comma = "," if i < len(keys) - 1 else ""
        lines.append(f'  "{k}": …{comma}')
    if blank:
        lines.append("")
    lines.append("}")
    return "\n".join(lines)


def person_card(keys, blank=False):
    code = D.json_code(person_src(keys, blank), CARD_SIZE)
    for g in chars(code, "…"):
        g.set_color(DIM)
    frame = D.fit_frame(code, size=CARD_SIZE, min_w=CARD_W)
    g = VGroup(frame, code)
    g.frame, g.code = frame, code
    return g


def _card(head, num_text, color):
    num = T(num_text, 56, GOLD)
    inner = VGroup(head, num).arrange(DOWN, buff=0.3)
    frame = (RoundedRectangle(corner_radius=0.2, width=inner.width + 0.6, height=2.0)
             .set_stroke(color, 3).set_fill(color, 0.06)).move_to(inner)
    g = VGroup(frame, head, num)
    g.frame, g.head, g.num = frame, head, num
    return g


def semijoin_tex():
    alg = MathTex(r"\text{people}", r"\ltimes_{\text{person\_id}}", r"\big(",
                  r"\sigma_{\text{position}=\text{'composer'}}(\text{has\_position})", r"\big)",
                  font_size=40, color=BLUE)
    alg.scale_to_fit_width(8.3)
    return alg


def teal_card():
    return _card(Mono("json_exists(…)", 28, TEAL), "1,086", TEAL)


def blue_card():
    return _card(semijoin_tex(), "1,086", BLUE)


def cards_row():
    return VGroup(blue_card(), teal_card()).arrange(RIGHT, buff=0.45)


def recap_thumb():
    cards = cards_row()
    key = Mono("birth_year", 36, FG)
    arr = Arrow(LEFT, RIGHT, buff=0, stroke_width=4, color=PINK).scale(0.6)
    nul = Mono("NULL", 36, PINK)
    typo = VGroup(key, arr, nul).arrange(RIGHT, buff=0.3)
    g = VGroup(cards, typo).arrange(DOWN, buff=0.7).move_to(ORIGIN)
    g.cards, g.typo = cards, typo
    return g


CHAPLIN = ["person_id", "name", "birthyear", "deathyear", "acted_in", "directed", "produced",
           "wrote", "composed_for"]
ZIMMER = ["person_id", "name", "birthyear", "composed_for"]
HITCH = ["person_id", "name", "birthyear", "deathyear", "directed"]

Q_SLIDE = ("-- People who have composed music for a movie\n"
           "SELECT COUNT(*) FROM people\n"
           "WHERE json_exists(person, '$.composed_for');\n"
           "\n"
           "-- People who have never acted\n"
           "SELECT COUNT(*) FROM people\n"
           "WHERE NOT json_exists(person, '$.acted_in');")
Q_NULL = "SELECT COUNT(*) FROM people\nWHERE (person->>'acted_in') IS NULL;"
Q_TYPO = ("SELECT person->>'name'       AS name,\n"
          "       person->>'birth_year' AS birth_year,\n"
          "       person->>'birthyear'  AS birthyear\n"
          "FROM   people\n"
          "WHERE (person->>'name') = 'Charles Chaplin';")


def fade_cards(cards, op):
    """Dim/restore cards without flooding their translucent frames: frame stroke and its faint fill
    scale with op, the rest goes through set_alpha."""
    out = []
    for cd in cards:
        out.append(cd.frame.animate.set_stroke(opacity=op).set_fill(opacity=0.06 * op))
        out += set_alpha([m for m in cd.submobjects if m is not cd.frame], op)
    return out


def dashed_slot(w, h=0.36, color=DIM):
    return DashedVMobject(Rectangle(width=w, height=h).set_stroke(color, 2), num_dashes=28)


class Missing(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c7.missing.1
    def clip1(self):
        with self.say("c7.missing.1", gap=1.8) as c:
            cards = [person_card(CHAPLIN), person_card(ZIMMER), person_card(HITCH, blank=True)]
            xs = [-4.55, 0, 4.55]
            for card, x in zip(cards, xs):
                card.move_to([x, 0, 0]).align_to([0, 2.3, 0], UP)
            names = [T(n, 30, FG).next_to(card, UP, buff=0.22)
                     for n, card in zip(["Charles Chaplin", "Hans Zimmer", "Alfred Hitchcock"], cards)]
            rt = min(2.4, c.until("cards"))
            self.play(*appear(*[VGroup(n, cd) for n, cd in zip(names, cards)], lag=0.4), run_time=rt)  # early: names caption their cards
            c.wait_until("cards")
            keys = [cards[0].code.find('"composed_for"'), cards[1].code.find('"composed_for"')]
            self.play(*[r for k in keys for r in recolor(list(k), YELLOW)],
                      *[FlashUnder(k, run_time=1.5) for k in keys], run_time=1.5)

            c.wait_until("Hitchcock's document")
            hc = cards[2].code
            slot = dashed_slot(2.7, 0.3).move_to(
                [0, (hc.line(5).get_y() + hc.line(7).get_y()) / 2, 0]).align_to(hc.line(1), LEFT)
            self.play(FadeIn(slot), *fade_cards(cards[:2], 0.5), *set_alpha(names[:2], 0.5), run_time=1.2)

            c.wait_until("ask")
            qm = T("?", 40, YELLOW).move_to(slot)
            self.play(*appear(qm), run_time=1.0)

            c.wait_until("exists")
            expr = Mono("json_exists(person, '$.composed_for')", 30, FG).move_to([0, 3.42, 0])
            self.play(*appear(expr), *fade_cards(cards[:2], 1), *set_alpha(names[:2], 1), run_time=1.0)
            res = [Mono(t, 36, col).move_to([x, -3.3, 0])
                   for t, col, x in (("true", GREEN, xs[0]), ("true", GREEN, xs[1]), ("false", RED, xs[2]))]
            self.play(*appear(*res, lag=0.35), run_time=min(1.6, c.until(None)))
            self.c1 = [*cards, *names, slot, qm, expr, *res]

    # ------------------------------------------------------------ c7.missing.2
    def clip2(self):
        with self.say("c7.missing.2", gap=1.5) as c:
            code = Code(Q_SLIDE, size=28)
            code.align_to([-6.6, 0, 0], LEFT).align_to([0, 3.55, 0], UP)
            second = [g for i in (4, 5, 6) for g in code.line(i)]
            first = [g for i in (0, 1, 2) for g in code.line(i)]
            for g in second:
                g.set_opacity(0.35)
            sweep_clear(self, *appear(code, shift=None))

            c.wait_until("one thousand")
            n1 = T("1,086", 48, GOLD).move_to([5.5, (code.line(1).get_y() + code.line(2).get_y()) / 2, 0])
            self.play(*appear(n1), run_time=1.0)

            c.wait_until("semijoin")
            row = cards_row().move_to([0, -1.75, 0])
            bc, tc = row
            self.play(FadeIn(tc.frame), *during(appear(tc.head, shift=None), 0.8, 1), *fly(n1, tc.num), run_time=1.5)
            c.wait_until("part three")
            self.play(*appear(bc, shift=None), run_time=1.5)

            c.wait_until("two")
            cap = T("one fact, two models", 36, FG).move_to([0, -3.3, 0])
            self.play(*appear(cap), *flash([tc.num, bc.num]), run_time=1.5)

            c.wait_until("acted")
            nots = code.find("NOT", line=6)
            self.play(*set_alpha(second, 1), *set_alpha(first, 0.35), run_time=1.2)
            c.wait_until("Add the word not")
            self.play(*recolor(list(nots), YELLOW), FlashUnder(nots, run_time=1.2), run_time=1.2)

            c.wait_until("seven thousand")
            n2 = T("7,706", 48, GOLD).move_to([5.5, (code.line(5).get_y() + code.line(6).get_y()) / 2, 0])
            self.play(*appear(n2), *fade_cards(row, 0.4), *set_alpha([cap], 0.4), run_time=1.0)

    # ------------------------------------------------------------ c7.missing.3
    def clip3(self):
        with self.say("c7.missing.3", gap=1.5) as c:
            sweep_clear(self)

            c.wait_until("Looking up")
            code = Code(Q_NULL, size=36).move_to([0, 2.2, 0])
            look = code.find("(person->>'acted_in')", line=1)
            look_ids = {id(g) for g in look}
            rest = [g for g in code.text.submobjects if id(g) not in look_ids]
            for g in rest:
                g.set_opacity(0.3)
            self.play(*appear(code, shift=None), run_time=1.0)
            c.wait_until("null")
            arr = Arrow(look.get_bottom() + 0.1 * DOWN, look.get_bottom() + 1.0 * DOWN, buff=0,
                        stroke_width=4, color=PINK)
            tag = Mono("NULL", 36, PINK).next_to(arr, DOWN, buff=0.15)
            self.play(GrowArrow(arr), *appear(tag), run_time=1.2)

            c.wait_until("isnull")
            isn = code.find("IS NULL", line=1)
            self.play(*set_alpha(rest, 1), FlashUnder(isn, run_time=1.5), run_time=1.5)
            c.wait_until("finds the same")
            n = T("7,706", 72, GOLD).move_to([0, -1.9, 0])
            self.play(*appear(n), run_time=1.0)

            c.wait_until("only for a key")
            col_x = [0.3, 4.8]
            row_y = [0.6, -0.9]
            h1 = Mono("json_exists(…, '$.a')", 30, FG).move_to([col_x[0], 2.0, 0])
            h2 = Mono("… ->> 'a'", 30, FG).move_to([col_x[1], 2.0, 0])
            r1 = D.json_code('{"a": null}', 34).move_to([-4.6, row_y[0], 0])
            lb, rb = Mono("{", 34, TEAL), Mono("}", 34, TEAL)
            ds = dashed_slot(1.6, 0.42)
            r2 = VGroup(lb, ds, rb).arrange(RIGHT, buff=0.15).move_to([-4.6, row_y[1], 0])
            hl = Line([-6.4, 1.45, 0], [6.4, 1.45, 0]).set_stroke(DIM, 2)
            vl = Line([-2.75, 2.4, 0], [-2.75, -1.6, 0]).set_stroke(DIM, 2)
            sweep_clear(self, *appear(h1, h2, r1, r2, lag=0.2),
                        time_span(Create(hl), 0.6, 1.4), time_span(Create(vl), 0.6, 1.4), run_time=1.6)
            c.wait_until("JSON's own null")
            nul = r1.find("null")
            self.play(FlashAround(nul, run_time=1.2, time_width=1.5, color=PINK), run_time=1.2)

            c.wait_until("says")
            cells = [[Mono("true", 40, GREEN), Mono("NULL", 40, PINK)],
                     [Mono("false", 40, RED), Mono("NULL", 40, PINK)]]
            for i, row in enumerate(cells):
                for j, m in enumerate(row):
                    m.move_to([col_x[j], row_y[i], 0])
            self.play(*appear(cells[0][0]), run_time=1.0)
            c.wait_until("double arrow gives null")
            self.play(*appear(cells[0][1]), run_time=1.0)
            c.wait_until("as if it were missing")
            self.play(*appear(cells[1][0], cells[1][1], lag=0.3), run_time=1.0)
            cap = T("can't tell them apart", 32, PINK).move_to([col_x[1] - 0.6, -2.15, 0])
            self.play(*flash([cells[0][1], cells[1][1]], color=PINK), *appear(cap),
                      run_time=min(1.2, c.until("ours")))

            c.wait_until("ours")
            note = T("no JSON null in any of our 2,935 + 23,179 documents", 30, DIM).move_to([0, -3.25, 0])
            self.play(*appear(note), run_time=1.0)

    # ------------------------------------------------------------ c7.missing.4
    def clip4(self):
        with self.say("c7.missing.4", gap=1.5) as c:
            c.wait_until("typo")
            code = Code(Q_TYPO, size=28)
            code.move_to([0, 0, 0]).align_to([0, 3.5, 0], UP)
            sweep_clear(self, *appear(code, shift=None), run_time=1.4)

            c.wait_until("birth underscore year")
            us = code.find("_", line=1)[0]
            self.play(us.animate.set_color(RED), FlashAround(us, run_time=1.2, color=RED), run_time=1.2)

            c.wait_until("nothing complains")
            heads = ["name", "birth_year", "birthyear"]
            vals = [("Charles Chaplin", FG), ("NULL", PINK), ("1889", GOLD)]
            xs = [-3.6, 0.6, 3.9]
            hs = [Mono(h, 28, DIM).move_to([x, 0.3, 0]) for h, x in zip(heads, xs)]
            rule = Line([-5.6, 0.0, 0], [5.4, 0.0, 0]).set_stroke(DIM, 2)
            vs = [(T(v, 34, col) if v == "Charles Chaplin" else Mono(v, 34, col)).move_to([x, -0.42, 0])
                  for (v, col), x in zip(vals, xs)]
            self.play(*appear(*hs, shift=None), FadeIn(rule), *appear(*vs, lag=0.2),
                      run_time=min(1.5, c.until("null")))

            c.wait_until("null")
            fact = T("0 of 23,179 people have a birth_year", 36, GOLD).move_to([0, -1.55, 0])
            self.play(FlashAround(vs[1], run_time=1.2, color=PINK), *appear(fact), run_time=1.2)

            c.wait_until("six")
            spell = Mono("birthyear  ·  birthYear  ·  birth_year", 28, DIM)
            lab = T("part 6", 28, DIM)
            inner = VGroup(lab, spell).arrange(RIGHT, buff=0.45)
            box = RoundedRectangle(corner_radius=0.12, width=inner.width + 0.5, height=0.75).set_stroke(DIM, 2)
            box.move_to(inner)
            chip_ = VGroup(box, inner).move_to([0, -2.75, 0])
            self.play(*appear(chip_), run_time=1.0)

            c.wait_until("a typo looks")
            self.play(FlashAround(us, run_time=1.2, color=RED),
                      FlashAround(vs[1], run_time=1.2, color=PINK), run_time=1.2)
