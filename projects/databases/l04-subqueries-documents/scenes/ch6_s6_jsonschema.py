"""Chapter 6, scene 6: JSON Schema. Clips c6.json.1 – c6.json.4.

Exports (import with `S = load_scene("ch6_s6_jsonschema")`; all static, no updaters):
    S.validator()      # TEAL rounded box 2.8 x 1.1 with "validator" inside (.box .label), at ORIGIN
    S.schema_card()    # slide 83's JSON Schema on ch4 s3's TEAL doc_card (size 15; .frame .code),
                       #   8.2 x 7.1, at ORIGIN
    S.recap_thumb()    # schema_card() with RED `'birth_year' was unexpected` under it; no caption
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

MOV = load_scene("ch4_s3_movie")
S4 = load_scene("ch6_s4_schema")

SCHEMA = "\n".join([
    '{',
    '  "type": "object",',
    '  "properties": {',
    '    "person_id": {"type": "string", "pattern": "^nm[0-9]+$"},',
    '    "name":      {"type": "string"},',
    '    "birthyear": {"type": "integer"},',
    '    "deathyear": {"type": "integer"},',
    '    "acted_in": {',
    '      "type": "array",',
    '      "items": {',
    '        "type": "object",',
    '        "properties": {',
    '          "movie_id": {"type": "string", "pattern": "^tt[0-9]+$"},',
    '          "title":    {"type": "string"},',
    '          "year":     {"type": "integer"},',
    '          "roles":    {"type": "array", "items": {"type": "string"}}',
    '        },',
    '        "required": ["movie_id", "title", "year", "roles"]',
    '      }',
    '    },',
    '    /* likewise "directed", "produced", "wrote", "composed_for" */',
    '  },',
    '  "required": ["person_id", "name"],',
    '  "additionalProperties": false',
    '}',
])
N_LINES = 25

CHAPLIN = '{"person_id": "nm0000122",\n "name": "Charles Chaplin"}'
BAD_UNDERSCORE = '{"person_id": "nm0000122",\n "name": "Charles Chaplin",\n "birth_year": 1889}'
BAD_QUOTED = '{"person_id": "nm0000122",\n "name": "Charles Chaplin",\n "birthyear": "1889"}'
BAD_NONAME = '{"person_id": "nm0000122"}'
MSG_UNDERSCORE = ["Additional properties are not allowed", "('birth_year' was unexpected)"]
MSG_QUOTED = ["'1889' is not of type 'integer'"]
MSG_NONAME = ["'name' is a required property"]


# ---------------------------------------------------------------- exports
def validator():
    box = RoundedRectangle(corner_radius=0.18, width=2.8, height=1.1) \
        .set_stroke(TEAL, 3).set_fill(TEAL, 0.12)
    label = T("validator", 34, TEAL).move_to(box)
    g = VGroup(box, label)
    g.box, g.label = box, label
    return g


def schema_card():
    card = MOV.doc_card(SCHEMA, size=15)
    return card.scale(7.1 / card.height)


def recap_thumb():
    card = schema_card()
    msg = Mono("'birth_year' was unexpected", 30, color=RED).next_to(card, DOWN, buff=0.3)
    return VGroup(card, msg)


# ---------------------------------------------------------------- helpers
def doc(src, size=22):
    return MOV.doc_card(src, size=size)


def message(lines, size=24, color=RED):
    return VGroup(*[Mono(s, size, color=color) for s in lines]).arrange(DOWN, buff=0.12)


def hl(card, parts, color=YELLOW, padx=0.08):
    """Highlight box behind the glyphs of (substring, line) parts of the card's code, line-high."""
    code = card.code
    top, bot = code.line(0).get_top()[1], code.line(N_LINES - 1).get_bottom()[1]
    pitch = (top - bot) / N_LINES
    gs = [code.find(s, line=ln) for s, ln in parts]
    lines = [ln for _, ln in parts]
    x0 = min(g.get_left()[0] for g in gs) - padx
    x1 = max(g.get_right()[0] for g in gs) + padx
    y1 = top - pitch * min(lines) + 0.02
    y0 = top - pitch * (max(lines) + 1) - 0.02
    r = Rectangle(width=x1 - x0, height=y1 - y0).set_stroke(color, 2).set_fill(color, 0.25)
    r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]).set_z_index(-1)
    return r


def arrow(p, q, color=TEAL):
    return Arrow(p, q, buff=0, stroke_width=4, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.4, color=color)


# ---------------------------------------------------------------- layout
ROW1 = -0.3                     # clip 1 diagram row
VX, VY = -2.6, 0.3              # validator, from {absent} on
DOC_BOT = 1.7                   # documents sit with their bottom here, above the validator
OUT_TOP = -1.5                 # validator's reply, top here
SMALL = 0.66                    # schema card scale beside the validator


def put_doc(d):
    d.move_to([VX, 0, 0]).shift(UP * (DOC_BOT - d.get_bottom()[1]))
    return d


def put_out(m):
    m.move_to([VX, 0, 0]).shift(UP * (OUT_TOP - m.get_top()[1]))
    return m


class Ch6S6JsonSchema(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c6.json.1: what it is
    def clip1(self):
        title = T("JSON Schema", 60, TEAL).move_to([0, 0.4, 0])
        mini = MOV.doc_card('{"type": "object"}', size=26).move_to([0, ROW1, 0])
        val = validator().move_to([0.3, ROW1, 0])
        chap = doc(CHAPLIN, 20)
        chap.move_to([-6.6 + chap.width / 2, ROW1, 0])
        with self.say("c6.json.1") as c:
            self.play(*appear(title), run_time=1.0)   # early: scene title
            c.wait_until("itself")
            self.play(*during([title.animate.scale(0.8).move_to([0, 3.15, 0])], 0, 0.6),
                      *during(appear(mini), 0.4, 1), run_time=min(1.6, c.until("validator")))
            c.wait_until("validator")
            self.play(*during([mini.animate.move_to([6.6 - mini.width / 2, ROW1, 0])], 0, 0.6),
                      *during(appear(val, shift=None), 0.4, 1), run_time=1.5)
            lab_doc = T("document", 30, DIM).next_to(chap, UP, buff=0.3)
            a_doc = arrow(chap.get_right() + RIGHT * 0.1, val.get_left() + LEFT * 0.08)
            lab_sch = T("schema", 30, DIM).next_to(mini, UP, buff=0.3).match_y(lab_doc)
            a_sch = arrow(mini.get_left() + LEFT * 0.1, val.get_right() + RIGHT * 0.08)
            a_out = arrow(val.get_bottom() + DOWN * 0.08, [val.get_x(), -1.95, 0], FG)
            out = VGroup(T("valid", 34, GREEN), T("or", 30, DIM), T("what's wrong", 34, RED)) \
                .arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([val.get_x(), -2.45, 0])
            c.wait_until("checks a document")
            self.play(*appear(chap, lab_doc, lab_sch, lag=0.3), GrowArrow(a_doc), GrowArrow(a_sch),
                      run_time=1.0)
            self.play(GrowArrow(a_out), *appear(*out, lag=0.3), run_time=1.0)
            c.wait_until("people")
            card = schema_card()
            card.move_to([6.6 - card.width / 2, 0, 0])
            self.play(*during(disappear(title, mini, chap, lab_doc, lab_sch, a_doc, a_sch, a_out, *out), 0, 0.45),
                      *during([val.animate.move_to([-4.6, 0, 0])], 0.2, 0.8),
                      *during(appear(card, shift=None), 0.5, 1), run_time=min(2.0, c.until()))
        self.val, self.card = val, card

    # ------------------------------------------------------------ c6.json.2: walk the schema
    def clip2(self):
        card, val = self.card, self.val
        steps = [
            ("props", [('"properties"', 2)]),
            ("pattern", [('"pattern": "^nm[0-9]+$"', 3)]),
            ("year", [('"birthyear": {"type": "integer"}', 5)]),
            ("array", [('"type": "array"', 8), ('"items"', 9)]),
            ("required", [('"required": ["person_id", "name"]', 22)]),
            ("extra", [('"additionalProperties": false', 23)]),
        ]
        with self.say("c6.json.2") as c:
            box = hl(card, [('"type": "object"', 1)])
            self.play(FadeIn(box), run_time=1.0)
            for cue, parts in steps:
                c.wait_until(cue)
                self.play(Transform(box, hl(card, parts)), run_time=1.0)
                if cue == "pattern":
                    c.wait_until("two fixed letters")
                    self.play(FlashUnder(card.code.find("nm", line=3), color=YELLOW, time_width=1.5,
                                         buff=0.05), run_time=1.0)
                    c.wait_until("digits")
                    self.play(FlashUnder(card.code.find("[0-9]+", line=3), color=YELLOW, time_width=1.5,
                                         buff=0.05), run_time=1.0)

            # {absent}: the card steps aside, the validator takes the middle
            c.wait_until("absent")
            w, h = card.width * SMALL, card.height * SMALL
            self.play(*during(disappear(box), 0, 0.35),
                      *during([card.animate.scale(SMALL).move_to([6.6 - w / 2, 3.5 - h / 2, 0]),
                               val.animate.move_to([VX, VY, 0])], 0.15, 1), run_time=1.5)
            self.remove(box)
            chap = put_doc(doc(CHAPLIN))
            a_doc = arrow([VX, DOC_BOT - 0.1, 0], [VX, VY + 0.63, 0])
            a_sch = arrow([card.get_left()[0] - 0.1, VY, 0], [VX + 1.48, VY, 0])
            self.play(*appear(chap), GrowArrow(a_doc), GrowArrow(a_sch), run_time=1.2)
            a_out = arrow([VX, VY - 0.63, 0], [VX, OUT_TOP + 0.12, 0], FG)
            valid = put_out(T("valid", 44, GREEN))
            self.play(GrowArrow(a_out), *appear(valid), FlashAround(val.box, color=GREEN, time_width=1.5),
                      run_time=1.2)
            c.wait_until("but if it's there")
            box2 = hl(card, [('"birthyear": {"type": "integer"}', 5)])
            self.play(FadeIn(box2), run_time=min(1.0, c.until()))
        self.box, self.doc, self.out = box2, chap, valid
        self.arrows = [a_doc, a_sch, a_out]

    # ------------------------------------------------------------ c6.json.3: the mistakes
    def clip3(self):
        card, val = self.card, self.val
        with self.say("c6.json.3") as c:
            self.play(*disappear(self.box), run_time=0.8)
            self.remove(self.box)
            rounds = [
                ("underscore", BAD_UNDERSCORE, MSG_UNDERSCORE, "extra key", '"birth_year"',
                 ('"additionalProperties": false', 23), 1.2),
                ("quoted", BAD_QUOTED, MSG_QUOTED, "is a string", '"1889"',
                 ('"birthyear": {"type": "integer"}', 5), 1.0),
                ("noname", BAD_NONAME, MSG_NONAME, None, None,
                 ('"required": ["person_id", "name"]', 22), 0.9),
            ]
            cur, msgs, top = self.doc, [], OUT_TOP
            for k, (cue, src, msg, hit, key, rule, rt) in enumerate(rounds):
                c.wait_until(cue)
                d = put_doc(doc(src))
                anims = swap(cur, d)
                if k == 0:
                    anims += during(disappear(self.out), 0, 0.45)
                else:
                    anims += set_alpha([msgs[-1]], 0.4)
                self.play(*anims, run_time=rt)
                cur = d
                if hit:
                    c.wait_until(hit)
                out = message(msg)
                out.move_to([VX, 0, 0]).shift(UP * (top - out.get_top()[1]))
                top = out.get_bottom()[1] - 0.16
                msgs.append(out)
                g = d.code.find(key) if key else d.frame
                self.play(*appear(out, shift=None), FlashAround(g, color=RED, time_width=1.5),
                          FlashAround(card.code.find(rule[0], line=rule[1]), color=RED, time_width=1.5),
                          run_time=1.0)

            c.wait_until("real")
            stack = VGroup(*[MOV.doc_card(width=3.4, height=1.1) for _ in range(3)])
            for i, f in enumerate(stack):
                f.shift(np.array([0.22, 0.18, 0]) * (i - 1))
            put_doc(stack)
            count = put_out(T("23,179 of 23,179 valid", 44, GOLD))
            # the nameless doc's RED reply holds ~1.5 s into {real}, then the count takes its place
            self.play(*swap(cur, stack), run_time=1.5)
            self.play(*during(disappear(*msgs), 0, 0.45),
                      *during(appear(count, shift=0.2 * UP), 0.5, 1), run_time=1.4)
            self.play(FlashAround(count, color=GOLD, time_width=1.5), run_time=1.2)
        self.doc, self.out = stack, count

    # ------------------------------------------------------------ c6.json.4: where it's used
    def clip4(self):
        card, val = self.card, self.val
        lx = -3.0
        api = VGroup(T("OpenAPI:", 36, YELLOW), T("descriptions of web services", 34)) \
            .arrange(DOWN, buff=0.18).move_to([lx, 2.7, 0])
        chips = VGroup(*[self.chip(s) for s in ("documentation", "code", "input forms")]) \
            .arrange(RIGHT, buff=0.25).move_to([lx - 0.2, 1.05, 0])
        with self.say("c6.json.4") as c:
            c.wait_until("widely used")
            self.play(*during(disappear(self.doc, self.out, *self.arrows), 0, 0.5),
                      *during([val.animate.move_to([lx, -2.2, 0])], 0.3, 1), run_time=1.5)
            c.wait_until("open a p i")
            self.play(*appear(api[0]), run_time=1.0)
            c.wait_until("web services")
            self.play(*appear(api[1]), run_time=1.0)
            c.wait_until("generate")
            for cue, ch in zip(("documentation", "code", "input forms"), chips):
                c.wait_until(cue)
                self.play(FadeIn(ch, shift=0.4 * LEFT), run_time=0.7)

            c.wait_until("onwrite")
            jc = S4.json_card()
            jc.move_to([lx, 0, 0]).shift(UP * (1.1 - jc.get_bottom()[1]))
            gate = S4.Gate(TEAL).move_to([lx, 0.45, 0])
            c.wait_until("some databases")
            self.play(*during(disappear(*api, *chips), 0, 0.45),  # early: s4's write gate
                      *during(appear(jc, gate, lag=0.3), 0.45, 1), run_time=1.8)
            c.wait_until("on every write")
            self.play(*during([FadeOut(gate.label)], 0, 0.35),
                      *during([val.animate.move_to(gate)], 0, 1), run_time=1.5)
            solid = S4.Gate(TEAL, "validate on write", solid=True).move_to(gate)
            self.play(*during(disappear(val, gate.bar), 0, 0.45),
                      *during(appear(solid, shift=None), 0.45, 1), run_time=1.2)  # early: "write" is the word
            self.remove(gate)

            c.wait_until("details")
            cap = T("know that it exists", 52).move_to([0, 2.55, 0])
            self.play(*during(disappear(jc, solid), 0, 0.4),
                      *during([card.animate.scale(0.9).move_to([0, -0.9, 0])], 0.15, 1), run_time=1.4)
            self.play(*set_alpha([card], DIMMED), *appear(cap), run_time=1.0)

    def chip(self, s):
        t = T(s, 30, FG)
        r = RoundedRectangle(corner_radius=0.15, width=t.width + 0.44, height=0.62) \
            .set_stroke(TEAL, 2.5).set_fill(TEAL, 0.12).move_to(t)
        return VGroup(r, t)
