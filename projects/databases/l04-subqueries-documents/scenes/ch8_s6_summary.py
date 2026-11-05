"""Chapter 8, scene 6: the JSON toolkit on one card. Clips c8.sum.1 – c8.sum.3.

The TEAL twin of ch3 s7's BLUE toolkit card (same frame, title, DIM heads, rules, row-by-row build),
titled "JSON in DuckDB", slide 93 verbatim. Every callback value is from one DuckDB 1.5.6 run on
The Kid (movies-json.duckdb).

Exports (for ch8 s8's recap):

    mod = load_scene("ch8_s6_summary")
    card = mod.json_card()       # static VGroup, full size, about 12.2 x 6.15, frame centred near ORIGIN
    card.frame, card.title, card.heads, card.rule, card.rows (9 rows, each VGroup(syntax, meaning)
    with .syntax Mono 24 TEAL and .meaning T 25 FG), card.foot_rule, card.footer (VGroup: T 30 YELLOW prose, the two arrows Mono 28)
    thumb = mod.recap_thumb(width=4.0)   # the whole TEAL card incl. footer, scaled to `width`
                                         # (4.0 wide -> about 2.0 tall), centred at ORIGIN
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

JSON_ROWS = [
    ("j->'key', j->'$.a[0].b'", "extract a value as JSON"),
    ("j->>'key', j->>'$.a[0].b'", "extract a value as a string"),
    ("j->>'$.a[*].b'", "list of values, one per array element"),
    ("(j->>'key')::INTEGER", "extract a number"),
    ("json_exists(j, '$.key')", "does the key exist?"),
    ("json_array_length(j, '$.a')", "number of elements in an array"),
    ("list_contains(l, x)", "does list l contain x?"),
    ("list_has_all(l1, l2)", "does l1 contain all of l2?"),
    ("FROM t, unnest(l) AS u(x)", "one row per element of list l"),
]
JSON_TITLE = "JSON in DuckDB"
JSON_HEADS = ("Syntax", "Meaning")
JSON_FOOTER = "Put parentheses around -> and ->> in conditions!"

# The Kid's actors, in array order (verified: unnest(movie->>'$.actors[*].name'))
ACTORS = ["Charles Chaplin", "Edna Purviance", "Jackie Coogan", "Carl Miller", "Albert Austin",
          "Beulah Bains", "Nellie Bly Baker", "Henry Bergman", "Edward Biby", "B.F. Blinn"]

ROW0_Y, ROW_PITCH = 1.9, 0.42
SYN_SIZE, MEAN_SIZE = 24, 25
TOP, BOTTOM = 3.55, -2.6
FOOT_Y = -2.2
CB_SIZE = 22


def json_card(color=TEAL):
    built = [(Mono(s, SYN_SIZE, color), T(m, MEAN_SIZE, FG)) for s, m in JSON_ROWS]
    syn_w = max(s.width for s, _ in built)
    mean_w = max(m.width for _, m in built)
    gap = 0.45
    inner = syn_w + gap + mean_w
    left = -inner / 2
    mean_x = left + syn_w + gap
    rows = []
    for i, (s, m) in enumerate(built):
        y = ROW0_Y - ROW_PITCH * i
        s.move_to([left, y, 0], aligned_edge=LEFT)
        m.move_to([mean_x, y, 0], aligned_edge=LEFT)
        r = VGroup(s, m)
        r.syntax, r.meaning = s, m
        rows.append(r)
    width = inner + 0.7
    frame = RoundedRectangle(corner_radius=0.2, width=width, height=TOP - BOTTOM)
    frame.set_stroke(color, 3).set_fill(color, 0.04).move_to([0, (TOP + BOTTOM) / 2, 0])
    title = T(JSON_TITLE, 44, FG).move_to([0, 3.07, 0])
    h1 = T(JSON_HEADS[0], 28, DIM).move_to([left, 2.52, 0], aligned_edge=LEFT)
    h2 = T(JSON_HEADS[1], 28, DIM).move_to([mean_x, 2.52, 0], aligned_edge=LEFT)
    rule = Line([-width / 2 + 0.2, 2.25, 0], [width / 2 - 0.2, 2.25, 0]).set_stroke(DIM, 1.5)
    foot_rule = Line([-width / 2 + 0.2, -1.8, 0], [width / 2 - 0.2, -1.8, 0]).set_stroke(DIM, 1.5)
    foot = VGroup(T("Put parentheses around", 30, YELLOW), Mono("->", 28, YELLOW), T("and", 30, YELLOW),
                  Mono("->>", 28, YELLOW), T("in conditions!", 30, YELLOW))
    foot.arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
    for m in (foot[2], foot[4]):          # serif pieces on one baseline (P has no descender)
        m.align_to(foot[0][0], DOWN)
    for m in (foot[1], foot[3]):          # the arrows centred on the x-height
        m.set_y(foot[2][0].get_center()[1])
    foot.move_to([0, FOOT_Y, 0])   # JSON_FOOTER, with the arrows in Mono
    rows_g, heads = VGroup(*rows), VGroup(h1, h2)
    g = VGroup(frame, title, heads, rule, rows_g, foot_rule, foot)
    g.frame, g.title, g.heads, g.rule, g.rows = frame, title, heads, rule, rows_g
    g.foot_rule, g.footer = foot_rule, foot
    return g


def recap_thumb(width=4.0):
    """The whole TEAL card, footer included, scaled to `width`, centred at ORIGIN."""
    return json_card().scale_to_fit_width(width).move_to(ORIGIN)


def row_box(card, i):
    s = card.frame.width / json_card_width()
    y = card.rows[i].get_center()[1]
    r = Rectangle(width=card.frame.width - 0.3 * s, height=ROW_PITCH * s)
    r.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12).set_z_index(-1)
    return r.move_to([card.frame.get_center()[0], y, 0])


_W = None


def json_card_width():
    global _W
    if _W is None:
        _W = json_card().frame.width
    return _W


def callback(expr, value, vcolor):
    """DIM expression on The Kid, an arrow, the value in its type's colour."""
    e = Mono(expr, CB_SIZE, DIM)
    a = Mono("→", CB_SIZE, DIM)
    v = Mono(value, CB_SIZE, vcolor)
    g = VGroup(e, a, v).arrange(RIGHT, buff=0.18)
    g.value = v
    return g


def name_chip(name):
    t = T(name, 22, TEAL)
    box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=0.34)
    box.set_stroke(TEAL, 1.5).set_fill(TEAL, 0.1).move_to(t)
    return VGroup(box, t)


def hook_chips():
    """s1's ten TEAL name chips if s1 offers them, else our own (same names, T 22)."""
    try:
        chips = load_scene("ch8_s1_hook").open_card(lifted=False).chips
        return [c.copy() for c in chips], True
    except Exception:
        return [name_chip(n) for n in ACTORS], False


def toward(mobs, p, s):
    return [m.animate.scale(s, about_point=p) for m in mobs]


class JsonSummary(NarratedScene):
    def construct(self):
        self.card = json_card()
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def land(self, i, rt, extra=()):
        row = self.card.rows[i]
        box_anim = FadeIn(self.box) if self.box is None else None
        if self.box is None:
            self.box = row_box(self.card, i)
            box_anim = FadeIn(self.box)
        else:
            box_anim = Transform(self.box, row_box(self.card, i))
        self.play(*appear(row, shift=0.3 * LEFT), box_anim, *extra, run_time=rt)  # early: a card row lands on its cue
        self.shown.append(row)

    # ------------------------------------------------------------ extract, paths, cast
    def clip1(self):
        card = self.card
        self.box = None
        self.shown = [card.frame, card.title, *card.heads, card.rule]
        with self.say("c8.sum.1") as c:
            self.play(GrowFromCenter(card.frame), *appear(card.title), run_time=1.3)  # early: card title
            self.play(*appear(*card.heads, lag=0.3), GrowFromCenter(card.rule), run_time=1.0)  # early: column heads frame the rows
            c.wait_until("arrows")
            a = callback("movie->'title'", '"The Kid"', TEAL)
            b = callback("movie->>'title'", "The Kid", BLUE)
            VGroup(a, b).arrange(RIGHT, buff=0.8).move_to([0, FOOT_Y, 0])
            self.land(0, min(1.3, 0.6 * c.until("double arrow")), appear(a, shift=0.15 * UP))
            c.wait_until("double arrow")
            self.land(1, min(1.3, 0.6 * c.until("paths")), appear(b, shift=0.15 * UP))
            c.wait_until("paths")
            p = callback("movie->>'$.directors[*].name'", "[Charles Chaplin]", BLUE).move_to([0, FOOT_Y, 0])
            self.land(2, min(1.5, 0.5 * c.until("with a star")),
                      during(disappear(a, b), 0, 0.45) + during(appear(p, shift=0.15 * UP), 0.5, 1))
            c.wait_until("with a star")
            star = select(card.rows[2].syntax, "[*]")[0]
            star_p = select(p[0], "[*]")[0]
            self.play(FlashAround(star, color=YELLOW, time_width=1.5),
                      FlashAround(star_p, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("cast")
            q = callback("(movie->>'year')::INTEGER", "1921", BLUE).move_to([0, FOOT_Y, 0])
            self.land(3, min(1.5, 0.6 * c.until()),
                      [*swap(p, q, shift=0.15 * UP)])
            self.cb = q

    # ------------------------------------------------------------ exists, length, lists, unnest
    def clip2(self):
        card = self.card
        with self.say("c8.sum.2") as c:
            e = callback("json_exists(movie, '$.composers')", "true", BLUE).move_to([0, FOOT_Y, 0])
            self.land(4, min(1.3, 0.6 * c.until("length")), swap(self.cb, e, shift=0.15 * UP))
            c.wait_until("length")
            n = callback("json_array_length(movie, '$.actors')", "10", GOLD).move_to([0, FOOT_Y, 0])
            self.land(5, min(1.3, 0.5 * c.until("counts")), swap(e, n, shift=0.15 * UP))
            self.play(FlashAround(card.rows[5], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("counts")
            # the card shrinks to the left; The Kid's ten actor chips line up at the right
            S = 0.8
            P = np.array([-9.0, 0.1, 0.0])
            on = self.shown + [self.box, n]
            chips, _ = hook_chips()
            self.from_s1 = _
            lane_x, top_y, pitch = 3.95, 3.3, 0.31
            for k, ch in enumerate(chips):        # s1's chips at their own size (0.34 tall, T 22)
                ch.move_to([lane_x, 3.15 - 0.36 * k, 0], aligned_edge=LEFT)
            self.play(*toward(on, P, S), run_time=min(1.4, 0.4 * c.until("actors array")))
            for part in [*card.rows[6:], card.foot_rule, card.footer]:
                part.scale(S, about_point=P)
            self.P, self.S = P, S
            self.play(*appear(*chips, shift=0.2 * LEFT, lag=0.08), run_time=min(1.5, 0.9 * c.until("actors array")))
            c.wait_until("actors array")
            nums = [T(str(k + 1), 24, GOLD).next_to(ch, LEFT, buff=0.15) for k, ch in enumerate(chips)]
            self.play(*appear(*nums, shift=None, lag=0.2), run_time=1.8)  # early: counting off the chips
            self.play(FlashAround(n.value, color=GOLD, time_width=1.5), FlashAround(nums[-1], color=GOLD),
                      run_time=1.0)
            c.wait_until("lists")
            t1 = Mono("true", 24, BLUE)
            t2 = Mono("true", 24, BLUE)
            right = card.frame.get_right()[0] + 0.3
            t1.move_to([right, card.rows[6].get_center()[1], 0], aligned_edge=LEFT)
            t2.move_to([right, card.rows[7].get_center()[1], 0], aligned_edge=LEFT)
            self.land(6, min(1.2, 0.6 * c.until("list has all")), appear(t1, shift=0.2 * LEFT))  # early: result of the row
            c.wait_until("list has all")
            self.land(7, min(1.2, 0.6 * c.until("unnest")), appear(t2, shift=0.2 * LEFT))  # early: result of the row
            c.wait_until("unnest")
            # one row per element: the chips give way to ten BLUE rows, in array order
            head = Mono("x", 22, DIM).move_to([lane_x, top_y, 0], aligned_edge=LEFT)
            hrule = Line([lane_x - 0.05, top_y - 0.16, 0], [lane_x + 2.4, top_y - 0.16, 0]).set_stroke(DIM, 1.5)
            rows = [T(nm, 22, BLUE).move_to([lane_x, top_y - pitch * (k + 1), 0], aligned_edge=LEFT)
                    for k, nm in enumerate(ACTORS)]
            self.land(8, min(1.2, 0.5 * c.until("gives you")))
            c.wait_until("gives you")
            self.play(*during(disappear(*chips, *nums), 0, 0.45),
                      *during(appear(head, hrule, *rows, shift=None, lag=0.06), 0.45, 1),
                      run_time=min(2.0, 0.85 * c.until()))
            self.lane = [head, hrule, *rows, t1, t2, n]

    # ------------------------------------------------------------ the warning, the docs, two cards
    def clip3(self):
        card = self.card
        with self.say("c8.sum.3") as c:
            c.wait_until("warning")
            self.play(*during(disappear(*self.lane, self.box), 0, 0.4),
                      *during(toward(self.shown, self.P, 1 / self.S), 0.35, 1),
                      run_time=min(1.6, 0.4 * c.until("parentheses")))
            for part in [card.foot_rule, card.footer]:
                part.scale(1 / self.S, about_point=self.P)
            c.wait_until("parentheses")
            self.play(*appear(card.footer, shift=0.2 * UP), GrowFromCenter(card.foot_rule), run_time=1.2)
            self.shown += [card.foot_rule, card.footer]
            c.wait_until("docs")
            note = T("full details: DuckDB's JSON functions documentation", 28, DIM).move_to([0, -3.15, 0])
            self.play(*appear(note, shift=0.15 * UP), run_time=1.0)  # early: the footnote is what she reads out
            c.wait_until("two toolkits")
            # ch3's BLUE card comes back small at the left, the TEAL card beside it, the same width
            W = 6.3
            S2 = W / card.frame.width
            src = card.frame.get_center()
            dst = np.array([3.4, 0.35, 0.0])
            P2 = (dst - S2 * src) / (1 - S2)
            blue = load_scene("ch3_s7_toolkit").toolkit_card()
            blue.scale_to_fit_width(W).move_to([-3.4, 0.35, 0])
            self.play(*during(disappear(note), 0, 0.3),
                      *during(toward(self.shown, P2, S2), 0.15, 0.75),
                      *during(appear(blue, shift=1.2 * RIGHT), 0.45, 1),
                      run_time=min(2.2, 0.6 * c.until("tables")))
            lab_y = -2.35
            lt = T("tables", 32, BLUE).move_to([-3.4, lab_y, 0])
            ld = T("documents", 32, TEAL).move_to([3.4, lab_y, 0])
            c.wait_until(own_word=lt)
            self.play(*appear(lt), run_time=0.9)
            c.wait_until(own_word=ld)
            self.play(*appear(ld), run_time=0.9)
            c.wait_until()
        self.wait(1.5)   # hold the two cards before the fade
