"""Chapter 10, scene 3: Exercise 18, what a JSON Schema can see. Clips c10.schema.1 – c10.schema.5.

Clip 1: ch9 s9's next_card() row (no header), card 18 bright; its box grows into ch6 s7's full
exercise_card(18), the five properties light one by one, hint chip (DIM) and the pause icon.
Clip 2: ch6 s6's schema card on the left, Chaplin's document on the right; the validator window
(a TEAL frame around exactly one document) checks three values against their rules. On {zones}
the three columns appear as a band across the top; the schema and window move below.
Clips 3-4: properties 1 and 2 under the window (rule row above it, reply under it).
Clip 5: 3-5 reach beyond one document: two docs with one person_id, the people table's key,
the movie_id pattern vs a missing movie, ch4 s5's two-way copies. Ends on the band: ✓ | ✗ | ✗ ✗ ✗.

EXPORTS (static): recap_r2() -> VGroup(.window (frame + label + Chaplin's doc), .band (three columns,
one mark each: ✓ | ✗ | ✗)), stacked, centred at ORIGIN (~13.4 wide).
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

R9 = load_scene("ch9_s9_recap")
R7 = load_scene("ch6_s7_recap")
I9 = load_scene("ch9_s1_intro")
S6 = load_scene("ch6_s6_jsonschema")
MOV = load_scene("ch4_s3_movie")
TW = load_scene("ch4_s5_shape")
ST = load_scene("ch4_s6_store")

# ---------------------------------------------------------------- documents and replies
CH = '{"person_id": "nm0000122",\n "name": "Charles Chaplin",\n "birthyear": 1889}'
NONAME = S6.BAD_NONAME
EMPTY = '{"person_id": "nm0000122",\n "name": ""}'
DEATH = '{"person_id": "nm0000122",\n "name": "Charles Chaplin",\n "birthyear": 1889,\n "deathyear": 1800}'
P1 = '{"person_id": "nm0000122",\n "name": "Charles Chaplin"}'
P2 = '{"person_id": "nm0000122",\n "name": "Charlie Chaplin"}'
M1 = '{"movie_id": "The Kid"}'
M2 = '{"movie_id": "tt9999999"}'
MSG_NONAME = "'name' is a required property"
MSG_EMPTY = "'' should be non-empty"
MSG_TT = "'The Kid' does not match '^tt[0-9]+$'"

# a readable excerpt of ch6 s6's schema (slide 83): the lines this scene points at, "…" for the rest
EXC_LINES = [
    '{"properties": {',
    ' "person_id": {"type": "string",',
    '   "pattern": "^nm[0-9]+$"},',
    ' "name": {"type": "string"},',
    ' "birthyear": {"type": "integer"},',
    ' "deathyear": {"type": "integer"},',
    ' "acted_in": {"items": {"properties": {',
    '   "movie_id": {"type": "string",',
    '     "pattern": "^tt[0-9]+$"},',
    '   "title": {"type": "string"},…}}},…},',
    ' "required": ["person_id", "name"], …}',
]
L_PID, L_NAME, L_BIRTH, L_DEATH, L_REQ = 1, 3, 4, 5, 10


def _insert(lines, i, new_i, extra):
    return lines[:i] + [new_i, extra] + lines[i + 1:]


EXC_MINLEN = _insert(EXC_LINES, L_NAME, ' "name": {"type": "string",', '   "minLength": 1},')
EXC_MIN = _insert(EXC_MINLEN, L_DEATH + 1, ' "deathyear": {"type": "integer",', '   "minimum": 1800},')
SCH_SIZE = 20
R_REQ = '"required": ["person_id", "name"]'
R_TT = '"movie_id": {"type": "string", "pattern": "^tt[0-9]+$"}'

KID2 = TW.KID_SRC.replace('"title": "The Kid"', '"title": "The Kid (1921)"')

# ---------------------------------------------------------------- layout
DOC_SIZE = 22
SCH_LEFT, SCH_TOP_A, SCH_TOP_B = -6.6, 2.4, 1.95   # schema card left edge; top in clip 2 / from {zones}
RX, DOC_TOP = 3.55, 0.9                        # right working area: doc top-centre
RULE_Y, REPLY_Y, TAG_Y = 1.4, -2.3, -3.1

BAND_TOP, BAND_H = 3.65, 1.45
COLS = [("one value", 3.0, -5.2), ("two values, one document", 5.2, -0.9), ("many documents", 4.8, 4.3)]
ENTRY_Y = BAND_TOP - 1.05
SLOT = {1: (0, 0.0), 2: (1, 0.0), 3: (2, -1.55), 4: (2, 0.0), 5: (2, 1.55)}


def doc(src, size=DOC_SIZE):
    return MOV.doc_card(src, size=size)


def put_right(d):
    d.move_to([RX, 0, 0]).shift(UP * (DOC_TOP - d.get_top()[1]))
    return d


def win_frame(d, pad=0.15):
    f = RoundedRectangle(corner_radius=0.25, width=d.width + 2 * pad, height=d.height + 2 * pad)
    return f.set_stroke(TEAL, 6).set_fill(BG, 0).move_to(d)


def win_label(frame, side=UP):
    return set_backstroke(T("validator", 28, TEAL), width=10).move_to(frame.get_edge_center(side))


def column(i):
    name, w, x = COLS[i]
    box = RoundedRectangle(corner_radius=0.18, width=w, height=BAND_H).set_stroke(DIM, 2).set_fill(BG, 0)
    box.move_to([x, BAND_TOP - BAND_H / 2, 0])
    head = T(name, 30).move_to([x, BAND_TOP - 0.4, 0])
    g = VGroup(box, head)
    g.box, g.head = box, head
    return g


def slot_x(k):
    col, off = SLOT[k]
    return COLS[col][2] + off


def badge(k):
    c = Circle(radius=0.28).set_stroke(FG, 2.5)
    n = T(str(k), 30).move_to(c)
    return VGroup(c, n).move_to([slot_x(k) - 0.33, ENTRY_Y, 0])


def mark(k, ok):
    m = check_mark(GREEN) if ok else cross_mark(RED)
    return m.move_to([slot_x(k) + 0.4, ENTRY_Y, 0])


def rule(src, y=RULE_Y, x=RX, size=27):
    return MOV.json_code(src, size).move_to([x, y, 0])


def reply(s, color=RED, y=REPLY_Y, x=RX):
    return Mono(s, 26, color=color).move_to([x, y, 0])


def valid(x=RX, y=REPLY_Y):
    return T("valid", 32, GREEN).move_to([x, y, 0])


def hl(code, *parts, color=YELLOW, padx=0.08, pady=0.07):
    """Highlight box behind the glyphs of (substring, line) parts of a schema excerpt."""
    gs = VGroup(*[code.find(sub, line=ln) for sub, ln in parts])
    r = Rectangle(width=gs.width + 2 * padx, height=gs.height + 2 * pady).set_stroke(color, 2)
    return r.set_fill(color, 0.25).move_to(gs).set_z_index(-1)


def excerpt(lines):
    return MOV.doc_card("\n".join(lines), size=SCH_SIZE)


def place_excerpt(card, top):
    return card.move_to([0, 0, 0]).shift([SCH_LEFT - card.get_left()[0], top - card.get_top()[1], 0])


def recap_r2():
    d = doc(CH)
    f = win_frame(d)
    win = VGroup(f, d, win_label(f))
    cols = [column(i) for i in range(3)]
    marks = [(check_mark(GREEN) if i == 0 else cross_mark(RED)).move_to([COLS[i][2], ENTRY_Y, 0])
             for i in range(3)]
    band = VGroup(*cols, *marks)
    g = VGroup(win, band).arrange(DOWN, buff=0.6).move_to(ORIGIN)
    g.window, g.band = win, band
    return g


# ---------------------------------------------------------------- scene
class Ch10S3Schema(NarratedScene):
    def construct(self):
        self.band = []
        self.lab_side = UP
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # helpers ---------------------------------------------------------
    def move_window(self, new_doc, keep_label=False):
        """Frame slides to fit new_doc; the label fades out and back in (it never slides over text)."""
        nf = win_frame(new_doc)
        nl = win_label(nf, self.lab_side)
        anims = [ReplacementTransform(self.wf, nf)]
        if keep_label:
            anims.append(Transform(self.wl, nl))
            self.wf = nf
            return anims
        anims += during(FadeOut(self.wl), 0, 0.3) + during(FadeIn(nl), 0.7, 1)
        self.wf, self.wl = nf, nl
        return anims

    def insert_line(self, new, line, keep_boxes=()):
        """Rewrite schema line `line` as two lines (new card `new`, not on screen): the old line's
        closing '},' fades, everything below slides down one line and the frame grows, then the
        new ',' and the inserted line fade in. No glyph passes over another."""
        old = self.sc
        tail = old.find("},", line=line)
        below = [g for i in range(line + 1, len(old.src.split("\n"))) for g in old.line(i)]
        dy = new.code.line(line + 2).get_y() - old.line(line + 1).get_y()
        self.tmp = VGroup(new.code.line(line)[-1], *new.code.line(line + 1)).copy()
        anims = during([FadeOut(g) for g in tail], 0, 0.3)
        anims += during([g.animate.shift(dy * UP) for g in below], 0.25, 0.7)
        anims += during(Transform(self.sf, new.frame), 0.25, 0.7)
        anims += during(FadeIn(self.tmp), 0.7, 1)
        for b in keep_boxes:
            anims += during(b.animate.shift(dy * UP), 0.25, 0.7)
        return anims

    def swap_in(self, new):
        """No visible change: the edited excerpt replaces the old code and the temporary glyphs."""
        self.remove(*self.sc.get_family(), *self.tmp.get_family())
        self.add(new.code)
        self.sc = new.code

    # clip 1 ----------------------------------------------------------
    def clip1(self):
        nc = R9.next_card()
        cards = nc.cards
        for n in (17, 19):
            cards[n].set_color(DIM)
        c18 = cards[18]
        self.add(cards[17], cards[19], c18.box, c18.head, c18.title, c18.lines)
        big = R7.exercise_card(18)
        big.move_to([0, 3.55 - big.height / 2, 0])
        paras = big.text
        for p in paras[1:]:
            p.set_opacity(0.3)
        hint = R7.hint_chip().set_color(DIM)
        hint.next_to(big, DOWN, buff=0.45)
        pause = I9.pause_icon(1.0).next_to(hint, DOWN, buff=0.45)
        dy = -VGroup(big, hint, pause).get_center()[1]
        for m in (big, hint, pause):
            m.shift(dy * UP)
        self.big, self.hint, self.pause = big, hint, pause

        with self.say("c10.schema.1") as c:
            self.play(*during([FadeOut(m) for m in (cards[17], cards[19], c18.head, c18.title, c18.lines)],
                              0, 0.45),
                      *during(ReplacementTransform(c18.box, big.box), 0.2, 0.8),
                      *during(FadeIn(big.text), 0.55, 1),
                      run_time=min(2.0, c.until("Which of these")))
            for k in range(1, 6):
                c.wait_until(f"p{k}")
                self.play(*set_alpha([paras[k]], 1), FlashUnder(paras[k], color=YELLOW, time_width=1.5),
                          run_time=min(1.2, c.until(f"p{k + 1}" if k < 5 else "stop")))
            self.play(*appear(hint), run_time=1.0)  # early: the hint is shown with the exercise
            c.wait_until("stop")
            self.play(*appear(pause, shift=None), run_time=0.8)

    # clip 2 ----------------------------------------------------------
    def clip2(self):
        sch = place_excerpt(excerpt(EXC_LINES), SCH_TOP_A)
        self.sf, self.sc = sch.frame, sch.code
        d = doc(CH).move_to([RX, sch.get_y(), 0])
        self.doc = d

        with self.say("c10.schema.2") as c:
            sweep_clear(self, *appear(self.sf, self.sc, d, lag=0.3, shift=None),
                        run_time=min(2.0, c.until("one")))
            c.wait_until("one")
            self.wf = win_frame(d)
            self.wl = win_label(self.wf)
            self.play(FadeIn(self.wf, scale=1.15), *during(FadeIn(self.wl), 0.4, 1),
                      run_time=min(1.2, c.until("checks each value")))
            steps = [("this key must be there", '"name"', 1, [(R_REQ, L_REQ)]),
                     ("this value must be an integer", "1889", 2, [('{"type": "integer"}', L_BIRTH)]),
                     ("this string must match a pattern", '"nm0000122"', 0,
                      [('{"type": "string",', L_PID), ('"pattern": "^nm[0-9]+$"}', L_PID + 1)])]
            vbox = rbox = arr = None
            for i, (cue, vsub, vline, rparts) in enumerate(steps):
                c.wait_until(cue)
                g = d.code.find(vsub, line=vline)
                nv = token_box(g, d.code.line(vline))
                nr = hl(self.sc, *rparts)
                p = np.array([self.wf.get_left()[0] - 0.05, g.get_y(), 0])
                q = np.array([nr.get_right()[0] + 0.05, nr.get_y(), 0])
                na = Arrow(p, q, buff=0, stroke_width=4, tip_length=0.2,
                           max_tip_length_to_length_ratio=0.3, color=YELLOW)
                nxt = steps[i + 1][0] if i < 2 else "zones"
                if vbox is None:
                    self.play(FadeIn(nv), FadeIn(nr), GrowArrow(na), run_time=min(1.5, c.until(nxt)))
                    vbox, rbox, arr = nv, nr, na
                else:
                    self.play(Transform(vbox, nv), Transform(rbox, nr), ReplacementTransform(arr, na),
                              run_time=min(1.2, c.until(nxt)))
                    arr = na
            c.wait_until("zones")
            # schema and window move down; the band takes the top
            self.sf.generate_target()
            self.sc.generate_target()
            VGroup(self.sf.target, self.sc.target).shift((SCH_TOP_B - SCH_TOP_A) * UP)
            nd = doc(CH)
            put_right(nd)
            shift = nd.get_center() - d.get_center()
            self.wf.generate_target()
            self.wf.target.shift(shift)
            d.generate_target()
            d.target.shift(shift)
            self.lab_side = DOWN
            nl = win_label(self.wf.target, DOWN)
            self.play(*during([FadeOut(vbox), FadeOut(rbox), FadeOut(arr), FadeOut(self.wl)], 0, 0.3),
                      *during([MoveToTarget(self.sf), MoveToTarget(self.sc), MoveToTarget(self.wf),
                               MoveToTarget(d)], 0.2, 0.85),
                      *during(FadeIn(nl), 0.8, 1), run_time=min(1.5, c.until("one value")))
            self.wl = nl
            self.cols = [column(i) for i in range(3)]
            for i, cue in enumerate(["one value", "two values", "other documents"]):
                c.wait_until(cue)
                nxt = ["two values", "other documents", None][i]
                self.play(FadeIn(self.cols[i].box), *appear(self.cols[i].head),
                          run_time=min(0.9, c.until(nxt)))
                self.band.append(self.cols[i])

    # clip 3 ----------------------------------------------------------
    def clip3(self):
        d = self.doc
        with self.say("c10.schema.3") as c:
            b1 = badge(1)
            self.play(*appear(b1), run_time=min(1.0, c.until("required")))
            self.band.append(b1)
            c.wait_until("required")
            self.rbox = hl(self.sc, (R_REQ, L_REQ))
            self.play(FadeIn(self.rbox), FlashAround(self.sc.find(R_REQ, line=L_REQ), time_width=1.5),
                      run_time=min(1.5, c.until("a document without one")))
            c.wait_until("a document without one")
            nd = put_right(doc(NONAME))
            self.play(*swap(d, nd), *self.move_window(nd, keep_label=True),
                      run_time=min(1.2, c.until("name is a required")))
            d = nd
            c.wait_until("name is a required")
            self.msg = reply(MSG_NONAME)
            self.play(*appear(self.msg), run_time=min(1.0, c.until("So the first")))
            c.wait_until("So the first")
            m1 = mark(1, True)
            self.play(Create(m1), run_time=min(0.8, c.until("empty")))
            self.band.append(m1)
            c.wait_until("empty")
            new = place_excerpt(excerpt(EXC_MINLEN), SCH_TOP_B)
            self.play(*self.insert_line(new, L_NAME), FadeOut(self.rbox),
                      run_time=min(1.6, 0.5 * c.until(None)))
            self.swap_in(new)
            self.rbox = hl(self.sc, ('{"type": "string",', L_NAME), ('"minLength": 1}', L_NAME + 1))
            nd = put_right(doc(EMPTY))
            nm = reply(MSG_EMPTY)
            self.play(FadeIn(self.rbox), *swap(d, nd), *self.move_window(nd, keep_label=True),
                      *swap(self.msg, nm), run_time=min(1.2, c.until(None)))
            self.doc, self.msg = nd, nm

    # clip 4 ----------------------------------------------------------
    def clip4(self):
        d = self.doc
        with self.say("c10.schema.4") as c:
            b2 = badge(2)
            self.play(*appear(b2), *disappear(self.msg), FadeOut(self.rbox),
                      run_time=min(1.0, 0.45 * c.until("fixed")))
            self.band.append(b2)
            nd = put_right(doc(DEATH))
            self.play(*swap(d, nd), *self.move_window(nd, keep_label=True),
                      run_time=min(1.2, c.until("fixed")))
            d = self.doc = nd
            c.wait_until("fixed")
            new = place_excerpt(excerpt(EXC_MIN), SCH_TOP_B)
            ld = L_DEATH + 1
            self.play(*self.insert_line(new, ld), run_time=min(1.5, 0.45 * c.until("never another")))
            self.swap_in(new)
            self.rbox = hl(self.sc, ('{"type": "integer",', ld), ('"minimum": 1800}', ld + 1))
            self.play(FadeIn(self.rbox), run_time=0.5)
            n1800 = self.sc.find("1800", line=ld + 1)
            self.play(FlashAround(n1800, color=GOLD, time_width=1.5), run_time=min(1.0, c.until("never another")))
            c.wait_until("never another")
            mn = self.sc.find("1800},", line=ld + 1)
            yr = d.code.find("1889")
            p = np.array([self.rbox.get_right()[0] + 0.05, self.rbox.get_y(), 0])
            q = np.array([self.wf.get_left()[0] - 0.05, yr.get_y(), 0])
            self.try_arr = Arrow(p, q, buff=0, stroke_width=4, tip_length=0.2, color=YELLOW,
                                 max_tip_length_to_length_ratio=0.3)
            xm = (self.sf.get_right()[0] + self.wf.get_left()[0]) / 2
            self.try_x = cross_mark(RED).move_to(p + (q - p) * (xm - p[0]) / (q[0] - p[0]))
            self.try_box = token_box(yr, d.code.line(2))
            self.play(GrowArrow(self.try_arr), *during(FadeIn(self.try_box), 0.5, 0.8),
                      *during(Create(self.try_x), 0.65, 1),
                      run_time=min(1.4, c.until("So a death year")))
            c.wait_until("So a death year")
            self.ok = valid()
            self.play(*appear(self.ok), run_time=min(1.0, c.until("nostd")))
            c.wait_until("nostd")
            m2 = mark(2, False)
            self.tag = T("Ajv's $data: an extension,\nnot standard", 28, DIM).move_to([RX, TAG_Y, 0])
            self.play(Create(m2), *appear(self.tag), run_time=min(1.0, c.until("Some validators")))
            self.band.append(m2)

    # clip 5 ----------------------------------------------------------
    def clip5(self):
        with self.say("c10.schema.5") as c:
            self.lab_side = UP
            bs = [badge(k) for k in (3, 4, 5)]
            sweep_clear(self, *appear(*bs, lag=0.4), keep=self.band, run_time=min(2.2, c.until("only ever")))
            self.band += bs
            c.wait_until("unique")
            # 3: two documents, one person_id
            d1 = doc(P1, 27).move_to([-3.15, 0.75, 0])
            d2 = doc(P2, 27).move_to([-3.15, -1.75, 0])
            self.wf = win_frame(d1)
            self.wl = win_label(self.wf)
            self.play(*appear(d1, d2, lag=0.3, shift=None), *during([FadeIn(self.wf), FadeIn(self.wl)], 0.6, 1),
                      run_time=min(1.3, 0.4 * c.until("key")))
            ok1 = T("valid", 30, GREEN).next_to(d1, RIGHT, buff=0.4)
            self.play(*appear(ok1), run_time=min(0.6, 0.25 * c.until("key")))
            ok2 = T("valid", 30, GREEN).next_to(d2, RIGHT, buff=0.4)
            self.play(*self.move_window(d2), *during(FadeIn(ok2, shift=0.2 * DOWN), 0.6, 1),
                      run_time=min(1.0, 0.6 * c.until("key")))
            m3 = mark(3, False)
            self.play(Create(m3), run_time=min(0.6, c.until("key")))
            self.band.append(m3)
            c.wait_until("key")
            tab = ST.TableCard("people", ["person_id", "person"], [["nm0000002", "doc"], ["nm0000122", "doc"]],
                               [2.75, 1.65]).move_to([4.2, 0.1, 0])
            self.play(*appear(tab, shift=None), run_time=min(1.0, c.until("primary key")))
            c.wait_until("primary key")
            self.play(tab.pks.animate.set_stroke(YELLOW, 4), FlashUnder(tab.heads[0], color=YELLOW, time_width=1.5),
                      run_time=min(1.0, c.until("does that job")))
            dup = Mono("nm0000122", 28, RED)
            dup.move_to(tab.cells[1]).align_to(tab.cells[1], LEFT).shift(0.62 * DOWN)
            dx = cross_mark(RED).next_to(dup, RIGHT, buff=0.3)
            self.play(FlashAround(d2.code.find("nm0000122"), color=RED, time_width=1.5),
                      *during(FadeIn(dup, shift=0.2 * DOWN), 0.3, 0.8), *during(Create(dx), 0.75, 1),
                      run_time=min(1.5, c.until("pattern")))
            c.wait_until("pattern")
            # 4: a pattern is not a foreign key
            rr = rule(R_TT, y=1.45, x=0)
            e1 = doc(M1, 26).move_to([-3.6, 0.25, 0])
            e2 = doc(M2, 26).move_to([-3.6, -2.0, 0])
            self.wf = win_frame(e1)
            self.wl = win_label(self.wf)
            sweep_clear(self, *appear(rr, e1, lag=0.3, shift=None), *during([FadeIn(self.wf), FadeIn(self.wl)], 0.8, 1),
                        keep=self.band, run_time=min(1.6, c.until("not that")))
            bad = Mono(MSG_TT, 26, RED)
            bad.next_to(e1, DOWN, buff=0.28).align_to(e1, LEFT)
            self.play(*appear(bad), run_time=min(1.0, c.until("not that")))
            c.wait_until("not that")
            ok = T("valid", 30, GREEN).next_to(e2, DOWN, buff=0.18)
            self.play(*appear(e2, shift=None), *during(self.move_window(e2), 0.3, 1),
                      *during(FadeIn(ok, shift=0.2 * DOWN), 0.75, 1), run_time=min(1.5, c.until("foreign")))
            c.wait_until("foreign")
            slot = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.6, height=e2.height)
                                  .set_stroke(TEAL, 3), num_dashes=36).move_to([3.9, e2.get_y(), 0])
            qm = T("?", 48, DIM).move_to(slot)
            da = DashedLine(self.wf.get_right() + 0.1 * RIGHT, slot.get_left() + 0.1 * LEFT,
                            dash_length=0.15).set_stroke(FG, 3)
            da.add_tip(tip_length=0.22)
            self.play(Create(da), *during([FadeIn(slot), FadeIn(qm)], 0.5, 1),
                      run_time=min(1.2, 0.6 * c.until("titles")))
            m4 = mark(4, False)
            self.play(Create(m4), run_time=min(0.8, c.until("titles")))
            self.band.append(m4)
            c.wait_until("titles")
            # 5: copies drift
            tw = TW.two_way()
            c0 = tw.get_center()
            tw.move_to([0, -0.95, 0])
            tw.title_k.set_color(GOLD)
            k, ch = tw.kid, tw.chap
            k2 = TW._card(KID2, -TW.TW_X)
            k2.shift(tw.get_center() - c0)
            k2.code.find('"The Kid (1921)"').set_color(GOLD)
            parts = [k.frame, k.code, ch.frame, ch.code, tw.a1, tw.a2]
            sweep_clear(self, *appear(*parts, lag=0.1, shift=None), keep=self.band,
                        run_time=min(1.6, c.until("drifting")))
            c.wait_until("drifting")
            tk = k2.code.find('"The Kid (1921)"')
            ne = MathTex(r"\neq", font_size=72, color=RED)
            ne.move_to([(k.get_right()[0] + ch.get_left()[0]) / 2, tw.title_c.get_y(), 0])
            set_backstroke(ne, width=8)
            self.play(*edit(k.code, k2.code), *during(FadeIn(ne), 0.7, 1),
                      run_time=min(1.5, 0.5 * c.until("No schema")))
            self.wf = win_frame(k)
            self.wl = win_label(self.wf)
            ck = check_mark(GREEN).move_to(k.get_corner(UR) + np.array([-0.45, -0.4, 0]))
            self.play(FadeIn(self.wf), FadeIn(self.wl), *during(Create(ck), 0.6, 1),
                      run_time=min(0.9, 0.5 * c.until("No schema")))
            cc = check_mark(GREEN).move_to(ch.get_corner(UR) + np.array([-0.45, -0.4, 0]))
            self.play(*self.move_window(ch), *during(Create(cc), 0.6, 1),
                      run_time=min(1.0, c.until("No schema")))
            c.wait_until("No schema")
            m5 = mark(5, False)
            self.play(Create(m5), run_time=min(0.8, c.until(None)))
            self.band.append(m5)
            others = [m for m in self.mobjects if not any(m is b for b in self.band)]
            self.play(*[FadeOut(m) for m in others], run_time=min(1.0, c.until(None)))
            self.play(*[m.animate.shift((BAND_TOP - BAND_H / 2) * DOWN) for m in self.band], run_time=min(1.2, c.until(None)))
        self.wait(1.2)
