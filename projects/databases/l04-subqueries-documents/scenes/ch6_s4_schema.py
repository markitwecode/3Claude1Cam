"""Chapter 6, scene 4: who checks the shape? Clips c6.schema.1 – c6.schema.4.

Exports (import with `S = load_scene("ch6_s4_schema")`; all static, no updaters):
    S.typed_card(color=BLUE)        # TypedCard: the ch1 s2 people card with slide 26's types
                                    #   (.box .header .divider .title .cols[c] .types[c] .underlines)
    S.json_card()                   # TEAL TypedCard: person_id TEXT / person JSON (slide 74)
    S.Gate(color, text, solid)      # the read/write gate: .bar (dashed outline, or solid fill 0.4)
                                    #   .label (T 28 inside the bar); 3.4 x 0.46, built at ORIGIN.
                                    #   s6: Gate(TEAL, "validate on write", solid=True) is the solid one.
    S.birthyear_reply()             # BLUE frame round DuckDB's RED reply, 3 lines, the
                                    #   `Did you mean: "birthyear"` line last, "birthyear" YELLOW (.frame .text)
    S.recap_thumb()                 # BLUE card + solid "schema-on-write" gate + `Did you mean`
                                    #   below it | TEAL card + solid "schema-on-read" gate above it
                                    #   + `person["name"]` reader; no caption; ~11 wide, scale it.
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

SCH = load_scene("ch1_s2_schema")

# ---------------------------------------------------------------- cards
HDR, PITCH, PAD_B, CSIZE, TSIZE, CARD_W = 0.56, 0.44, 0.14, 28, 30, 4.0
PEOPLE = [("person_id", "TEXT"), ("name", "TEXT"), ("birthyear", "INT"), ("deathyear", "INT")]
PEOPLE_JSON = [("person_id", "TEXT"), ("person", "JSON")]


class TypedCard(VGroup):
    """ch1 s2's TableCard look (header fill, divider, key underline), with a GREEN type column."""

    def __init__(self, rows, color=BLUE, title="people", keys=("person_id",), w=CARD_W):
        super().__init__()
        h = HDR + len(rows) * PITCH + PAD_B
        top = h / 2
        self.box = Rectangle(width=w, height=h).set_stroke(color, 3).set_fill(BG, 0)
        self.header = Rectangle(width=w, height=HDR).set_stroke(color, 0).set_fill(color, 0.35)
        self.header.move_to([0, top - HDR / 2, 0])
        self.divider = Line([-w / 2, top - HDR, 0], [w / 2, top - HDR, 0]).set_stroke(color, 2)
        self.title, _ = SCH._placed(title, TSIZE, FG, BOLD, top - HDR / 2, cx=0)
        tw = max(Mono(t, CSIZE).width for _, t in rows)
        self.cols, self.types, ul = {}, {}, []
        for i, (c, t) in enumerate(rows):
            y = top - HDR - PITCH * (i + 0.5) - 0.02
            ct, bot = SCH._placed(c, CSIZE, FG, NORMAL, y, left=-w / 2 + 0.24)
            tt, _ = SCH._placed(t, CSIZE, GREEN, NORMAL, y, left=w / 2 - 0.24 - tw)
            self.cols[c], self.types[c] = ct, tt
            if c in keys:
                ul.append(Line([ct.get_left()[0], bot + 0.02, 0],
                               [ct.get_right()[0], bot + 0.02, 0]).set_stroke(FG, 2.5))
        self.underlines = ul
        self.add(self.header, self.box, self.divider, self.title,
                 *self.cols.values(), *self.types.values(), *ul)


def typed_card(color=BLUE):
    return TypedCard(PEOPLE, color)


def json_card():
    return TypedCard(PEOPLE_JSON, TEAL)


# ---------------------------------------------------------------- the gate
GATE_W, GATE_H = 3.4, 0.46


class Gate(VGroup):
    def __init__(self, color=TEAL, text="write", solid=False, w=GATE_W):
        super().__init__()
        shape = RoundedRectangle(corner_radius=0.12, width=w, height=GATE_H)
        if solid:
            self.bar = shape.set_stroke(color, 3).set_fill(color, 0.4)
        else:
            self.bar = DashedVMobject(shape.set_stroke(color, 3), num_dashes=40)
        self.label = T(text, 28, FG if solid else color).move_to(self.bar)
        self.add(self.bar, self.label)


# ---------------------------------------------------------------- console (statements + replies)
CON_TOP, CON_BOT, CON_W = -0.72, -3.78, 13.4
STMT_UL = np.array([-6.3, CON_TOP - 0.22, 0])


def console(color):
    return RoundedRectangle(corner_radius=0.16, width=CON_W, height=CON_TOP - CON_BOT) \
        .set_stroke(color, 2.5).set_fill(BG, 0).move_to([0, (CON_TOP + CON_BOT) / 2, 0])


def stmt(src):
    c = Code(src, size=30)
    c.move_to(STMT_UL, aligned_edge=UL)
    return c


def reply(*lines, size=28):
    """lines: str (RED) or (str, color[, t2c])."""
    out = []
    for ln in lines:
        s, col, t2c = (ln, RED, {}) if isinstance(ln, str) else (tuple(ln) + ({},))[:3]
        out.append(Mono(s, size, color=col, t2c=t2c))
    return VGroup(*out).arrange(DOWN, buff=0.12, aligned_edge=LEFT)


def dym_line(size=28):
    return Mono('Did you mean: "birthyear"', size, color=RED, t2c={'"birthyear"': YELLOW})


BIRTH_REPLY = ['Binder Error: Table "people" does not have a column', 'with name "birth_year"']


def _birth_reply_text(size=28):
    g = reply(*BIRTH_REPLY, size=size)
    d = dym_line(size)
    return VGroup(*g, d).arrange(DOWN, buff=0.12, aligned_edge=LEFT)


def birthyear_reply():
    text = _birth_reply_text()
    frame = SurroundingRectangle(text, buff=0.3, corner_radius=0.16).set_stroke(BLUE, 2.5).set_fill(BG, 0)
    g = VGroup(frame, text)
    g.frame, g.text = frame, text
    return g


def reader_card():
    code = Mono('person["name"]', 30, t2c={'"name"': GOLD})
    frame = SurroundingRectangle(code, buff=0.18, corner_radius=0.12).set_stroke(DIM, 2.5)
    g = VGroup(frame, code)
    g.frame, g.code = frame, code
    return g


def recap_thumb():
    lc = typed_card()
    lg = Gate(BLUE, "schema-on-write", solid=True).next_to(lc, DOWN, buff=0.35)
    ld = dym_line().next_to(lg, DOWN, buff=0.35)
    left = VGroup(lc, lg, ld)
    rc = json_card()
    rg = Gate(TEAL, "schema-on-read", solid=True).next_to(rc, UP, buff=0.3)
    rr = reader_card().next_to(rg, UP, buff=0.3)
    right = VGroup(rc, rg, rr)
    right.next_to(left, RIGHT, buff=1.2).align_to(left, DOWN).shift(UP * (ld.height + 0.35))
    g = VGroup(left, right).move_to(ORIGIN)
    return g


# ---------------------------------------------------------------- layout
CARD_BOT, GATE_Y, READER_BOT = 0.6, -0.04, 2.9
SX = 3.5                       # side centres once split


def put_card(card, x, bot=CARD_BOT):
    card.move_to([x, 0, 0]).shift(UP * (bot - card.get_bottom()[1]))
    return card


def up_arrow(x, y0, y1, color):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, stroke_width=4, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.5, color=color)


# terminal panels (clip 4)
PAN_W, PAN_TOP, PS = 6.8, 2.85, 21
OCAML = ('let next_year y = y + 1\n'
         'let () = print_endline "running"\n'
         'let () = print_int (next_year "1889")')
PYTHON = ('def next_year(y):\n'
          '    return y + 1\n'
          '\n'
          'print("running")\n'
          'print(next_year("1889"))')


def tline(s, color=FG, **kw):
    return Mono(s, PS, color=color, **kw)


class Ch6S4Schema(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c6.schema.1: schema-on-write
    def clip1(self):
        card = put_card(typed_card(), 0)
        gate = Gate(BLUE).move_to([0, GATE_Y, 0])
        frame = console(BLUE)
        s1 = stmt("INSERT INTO people (person_id, name, birth_year)\n"
                  "VALUES ('nm9999999', 'Ann Example', 1990);")
        r1 = _birth_reply_text().next_to(s1, DOWN, buff=0.24, aligned_edge=LEFT)
        r1a, r1b = VGroup(*r1[:2]), r1[2]
        arr = up_arrow(-1.2, CON_TOP, GATE_Y - GATE_H / 2, BLUE)
        cross = cross_mark().move_to([GATE_W / 2 + 0.45, GATE_Y, 0])
        with self.say("c6.schema.1") as c:
            self.play(*appear(card), run_time=1.0)  # early: the scene's opening shot
            c.wait_until(own_word=gate.label)
            self.play(*appear(gate), run_time=min(1.0, c.until("column")))
            c.wait_until("column")
            self.play(FadeIn(frame), *appear(s1, shift=0.2 * UP), run_time=1.2)
            c.wait_until("refuses")
            self.play(GrowArrow(arr), FlashAround(gate.bar, color=RED, time_width=1.5), run_time=1.0)
            self.play(*appear(cross, shift=None), *appear(r1a, lag=0.3), run_time=1.0)
            c.wait_until("suggests")
            self.play(*appear(r1b, shift=None), run_time=1.0)
            self.play(FlashAround(r1b[-11:], color=YELLOW, time_width=1.5), run_time=1.0)

            # {type}: the right name, the wrong kind of value
            c.wait_until("type")
            s2 = stmt("INSERT INTO people (person_id, name, birthyear)\n"
                      "VALUES ('nm9999999', 'Ann Example', 'unknown');")
            r2 = reply("Conversion Error: Could not convert string 'unknown'", "to INT32") \
                .next_to(s2, DOWN, buff=0.24, aligned_edge=LEFT)
            self.play(*edit(s1, s2), run_time=1.5)
            c.wait_until("refuses that too")
            self.play(FlashAround(gate.bar, color=RED, time_width=1.5), FlashAround(cross, color=RED),
                      *during(disappear(r1a, r1b), 0, 0.45), *during(appear(r2, lag=0.3), 0.5, 1),
                      run_time=1.4)

            # {name}: the gate is the schema
            c.wait_until("name")
            g2 = Gate(BLUE, "schema-on-write", solid=True).move_to(gate)
            self.play(*disappear(arr, cross), run_time=0.8)
            c.wait_until(own_word=g2.label)
            self.play(FadeOut(gate.bar), FadeIn(g2.bar), *swap(gate.label, g2.label), run_time=1.2)
            settle(self, g2)
            self.blue_card, self.blue_gate = card, g2

            # {query}: reads are checked too
            c.wait_until("known type")
            self.play(FlashAround(VGroup(*card.types.values()), color=GREEN, time_width=1.5), run_time=1.2)
            chk = VGroup(T("checked", 30, GREEN), T("before it runs", 30, GREEN)) \
                .arrange(DOWN, buff=0.12).move_to([4.6, 1.9, 0])
            q = stmt("SELECT name + 1 FROM people WHERE false;")
            c.wait_until(own_word=chk[0])
            self.play(*appear(chk, lag=0.2), *during(disappear(s2, r2), 0, 0.45),
                      *during(appear(q, shift=0.2 * UP), 0.5, 1), run_time=1.4)
            c.wait_until("adding one")
            self.play(FlashAround(q.find("name + 1"), color=YELLOW, time_width=1.5), run_time=1.0)
            r3 = reply("Binder Error: No function matches the given name",
                       "and argument types '+(VARCHAR, INTEGER_LITERAL)'.",
                       "You might need to add explicit type casts.", ("…", DIM)) \
                .next_to(q, DOWN, buff=0.24, aligned_edge=LEFT)
            c.wait_until("rejected")
            self.play(*appear(r3, lag=0.2), run_time=1.2)
            box = token_box(q.find("WHERE false"), q, color=YELLOW)
            c.wait_until("where false")
            self.play(FadeIn(box), run_time=0.8)
            rows = T("reads no rows", 30, YELLOW).next_to(q, RIGHT, buff=0.45)
            c.wait_until(own_word=rows)
            self.play(*appear(rows), run_time=1.0)
        self.chk = chk
        self.c1_console = [frame, q, r3, box, rows]

    # ------------------------------------------------------------ c6.schema.2: documents
    def clip2(self):
        card, gate = self.blue_card, self.blue_gate
        tcard = put_card(json_card(), SX, CARD_BOT - 0.14)
        tgate = Gate(TEAL).move_to([SX, GATE_Y, 0])
        frame = console(TEAL)
        s3 = stmt("INSERT INTO people\n"
                  "VALUES ('nm9999999', '{\"nmae\": 42}');")
        ax = SX - 1.2
        thru = up_arrow(ax, CON_TOP, tcard.get_bottom()[1], GREEN)
        tick = check_mark().move_to([SX + GATE_W / 2 + 0.45, GATE_Y, 0])
        with self.say("c6.schema.2") as c:
            self.play(*during(disappear(self.chk), 0, 0.4),
                      *during([card.animate.shift(LEFT * SX), gate.animate.shift(LEFT * SX)], 0.15, 0.75),
                      *during(appear(tcard, tgate, lag=0.3), 0.5, 1), run_time=2.0)
            c.wait_until("nmae")
            self.play(*during(disappear(*self.c1_console), 0, 0.45),
                      *during([FadeIn(frame)] + appear(s3, shift=0.2 * UP), 0.5, 1), run_time=1.6)
            self.play(FlashAround(s3.find('"nmae"'), color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("stores it")
            self.play(GrowArrow(thru), run_time=1.0)
            self.play(*appear(tick, shift=None), FlashAround(tcard, color=GREEN, time_width=1.5), run_time=1.0)

            c.wait_until("malformed")
            self.play(FlashAround(tcard.types["person"], color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until("leave the quotes")
            s4 = stmt("INSERT INTO people\n"
                      "VALUES ('nm9999998', '{name: 42}');")
            self.play(*during(disappear(thru, tick), 0, 0.4), *during(edit(s3, s4), 0.2, 1), run_time=1.0)
            stop = up_arrow(ax, CON_TOP, GATE_Y - GATE_H / 2, TEAL)
            cross = cross_mark().move_to(tick)
            r4 = reply("Conversion Error: Malformed JSON at byte 1 of input:",
                       'unexpected character.  Input: "{name: 42}"') \
                .next_to(s4, DOWN, buff=0.24, aligned_edge=LEFT)
            c.wait_until("and that's refused")
            self.play(GrowArrow(stop), FlashAround(tgate.bar, color=RED, time_width=1.5),
                      *appear(cross, *r4, shift=None, lag=0.2), run_time=min(1.2, c.until()))
        self.tcard, self.tgate = tcard, tgate
        self.c2_console = [frame, s4, r4, stop, cross]

    # ------------------------------------------------------------ c6.schema.3: schema-on-read
    def clip3(self):
        tcard, tgate = self.tcard, self.tgate
        word = T('"schemaless"', 40, TEAL).move_to([SX, 3.2, 0])
        strike = Line(word.get_left() + LEFT * 0.1, word.get_right() + RIGHT * 0.1).set_stroke(RED, 6)
        rd = reader_card()
        rd.move_to([6.55 - rd.width / 2, 0, 0]).shift(UP * (READER_BOT - rd.get_bottom()[1]))
        tag = T("expects: a string", 30, YELLOW).next_to(rd, LEFT, buff=0.35)
        read_y = (tcard.get_top()[1] + rd.get_bottom()[1]) / 2
        with self.say("c6.schema.3") as c:
            c.wait_until(own_word=word)
            self.play(*appear(word), run_time=1.0)
            c.wait_until("misleading")
            self.play(GrowFromEdge(strike, LEFT), word.animate.set_opacity(0.6), run_time=0.9)
            c.wait_until("reader")
            self.play(*during(disappear(word, strike), 0, 0.45), *during(appear(rd), 0.5, 1), run_time=1.4)
            rarr = up_arrow(SX + 1.45, tcard.get_top()[1], rd.get_bottom()[1], TEAL)
            c.wait_until("name key")
            self.play(GrowArrow(rarr), FlashAround(tcard.types["person"], color=YELLOW, time_width=1.5),
                      run_time=1.0)
            c.wait_until(own_word=tag, cue="string")
            self.play(*appear(tag), run_time=1.0)

            # {implicit}: the schema lives in the reader, checked at read time
            c.wait_until("implicit")
            mov = [self.blue_card, self.blue_gate, tcard, tgate, rd, tag, rarr]
            self.play(*during(disappear(*self.c2_console), 0, 0.45),
                      *during([m.animate.shift(DOWN * 1.5) for m in mov], 0.35, 1), run_time=1.8)
            read_y = (tcard.get_top()[1] + rd.get_bottom()[1]) / 2
            c.wait_until("it's implicit")
            self.play(*disappear(tgate.label), run_time=0.6)
            self.play(tgate.bar.animate.move_to([SX, read_y, 0]), run_time=1.8)
            lab = T("read", 28, TEAL).move_to([SX, read_y, 0])
            c.wait_until(own_word=lab)
            self.play(*appear(lab, shift=None), run_time=0.8)
            g2 = Gate(TEAL, "schema-on-read", solid=True).move_to([SX, read_y, 0])
            c.wait_until("sor")
            c.wait_until(own_word=g2.label)
            self.play(FadeOut(tgate.bar), FadeIn(g2.bar), *swap(lab, g2.label), run_time=1.2)
            settle(self, g2)
        self.teal_gate = g2
        self.right_rest = [tcard, rd, tag, rarr]

    # ------------------------------------------------------------ c6.schema.4: static vs dynamic types
    def clip4(self):
        po = Code(OCAML, size=PS, lang="ocaml")
        pp = Code(PYTHON, size=PS, lang="python")
        inner = PAN_W - 0.34
        for p in (po, pp):
            if p.width > inner:
                p.scale_to_fit_width(inner)
        lx, rx = -3.55, 3.55
        po.move_to([lx - PAN_W / 2 + 0.17, PAN_TOP - 0.22, 0], aligned_edge=UL)
        pp.move_to([rx - PAN_W / 2 + 0.17, PAN_TOP - 0.22, 0], aligned_edge=UL)
        sep_y = min(po.get_bottom()[1], pp.get_bottom()[1]) - 0.18
        seps = [Line([x - PAN_W / 2 + 0.17, sep_y, 0], [x + PAN_W / 2 - 0.17, sep_y, 0]).set_stroke(DIM, 1.5)
                for x in (lx, rx)]
        oc_out = VGroup(tline("$ ocamlc nextyear.ml", t2c={"$": DIM}),
                        tline('File "nextyear.ml", line 3,', DIM), tline("characters 30-36:", DIM),
                        tline("…", DIM),
                        tline("Error: This constant has type", RED),
                        tline("string but an expression was", RED),
                        tline("expected of type int", RED)).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
        py_out = VGroup(tline("$ python3 nextyear.py", t2c={"$": DIM}),
                        tline("running"),
                        tline("Traceback (most recent call last):"),
                        tline("…", DIM),
                        tline("TypeError: can only concatenate str", RED),
                        tline('(not "int") to str', RED)).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
        oc_out.move_to([lx - PAN_W / 2 + 0.17, sep_y - 0.18, 0], aligned_edge=UL)
        py_out.move_to([rx - PAN_W / 2 + 0.17, sep_y - 0.18, 0], aligned_edge=UL)
        bot = min(oc_out.get_bottom()[1], py_out.get_bottom()[1]) - 0.18
        frames = [RoundedRectangle(corner_radius=0.16, width=PAN_W, height=PAN_TOP - bot)
                  .set_stroke(col, 2.5).set_fill(BG, 0).move_to([x, (PAN_TOP + bot) / 2, 0])
                  for x, col in ((lx, BLUE), (rx, TEAL))]
        map_l = T("static types ≈ schema-on-write", 30, BLUE).move_to([lx, bot - 0.36, 0])
        map_r = T("dynamic types ≈ schema-on-read", 30, TEAL).move_to([rx, bot - 0.36, 0])
        gy = PAN_TOP + 0.2 + GATE_H / 2

        with self.say("c6.schema.4", gap=3.0) as c:
            self.play(*during(disappear(self.blue_card, *self.right_rest), 0, 0.45),
                      *during([self.blue_gate.animate.move_to([lx, gy, 0]),
                               self.teal_gate.animate.move_to([rx, gy, 0])], 0.35, 1), run_time=1.8)
            c.wait_until("ocaml")
            self.play(*appear(frames[0], po, seps[0], shift=None, lag=0.15),
                      *during(appear(frames[1], pp, seps[1], shift=None, lag=0.15), 0.3, 1), run_time=1.8)
            c.wait_until("a function")
            names = [po.find("next_year", nth=k) for k in (0, 1)] + [pp.find("next_year", nth=k) for k in (0, 1)]
            self.play(*[a for g in names for a in recolor(g, YELLOW)], run_time=1.0)
            boxes = [token_box(po.find('"1889"'), po.line(2), color=YELLOW),
                     token_box(pp.find('"1889"'), pp.line(4), color=YELLOW)]
            c.wait_until("as a string")
            self.play(*[FadeIn(b) for b in boxes], run_time=1.0)

            c.wait_until("compile")
            self.play(*appear(oc_out[0], shift=None), run_time=0.8)
            c.wait_until("rejects")
            self.play(*appear(*oc_out[1:], shift=None, lag=0.15), run_time=1.4)
            c.wait_until("python")
            self.play(*appear(py_out[0], shift=None), run_time=0.8)
            c.wait_until("prints")
            self.play(*appear(py_out[1], shift=None), run_time=0.8)
            c.wait_until("crashes")
            self.play(*appear(*py_out[2:], shift=None, lag=0.2), run_time=1.4)

            c.wait_until(own_word=map_l)
            self.play(*appear(map_l), run_time=1.0)
            c.wait_until(own_word=map_r)
            self.play(*appear(map_r), run_time=1.0)
