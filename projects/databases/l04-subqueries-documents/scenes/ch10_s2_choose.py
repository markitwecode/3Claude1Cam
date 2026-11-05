"""Chapter 10, scene 2: Exercise 17, tables or documents? Clips c10.choose.1 – c10.choose.6.

Opens on ch9 s9's next_card() row (no header), card 17 bright, 18/19 at 0.3; card 17 grows into ch6 s7's
exercise_card(17), hint DIM under it, ch9 s1's pause_icon(); held through the pause. On {tests} the card
shrinks to the top left; the three test icons enter large, then park as column heads along the top. Each
application gets a row (name, three answers, verdict chip) under them, with its sketch large below.
Ends on an empty frame.

EXPORTS (static, no updaters; `load_scene("ch10_s2_choose").<name>()`):
- recap_r1(): the three test icons (tree/tangle, copies ≠, three shapes) in a row above the five verdict
  chips (documents, tables, documents, hybrid, documents) in a column; centred at ORIGIN, ~5.6 x 4.4.
- shape_icon(), writes_icon(), kinds_icon(): the icons alone, natural size (~1.5 tall), at ORIGIN.
- verdict_chip(kind): kind in "documents" | "tables" | "hybrid"; 2.1 x 0.42.
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
G3 = load_scene("ch6_s3_graph")
T5 = load_scene("ch6_s5_tradeoff")
EX7 = load_scene("ch6_s7_recap")
S1 = load_scene("ch9_s1_intro")
R9 = load_scene("ch9_s9_recap")

# ---------------------------------------------------------------- layout
COL_X = (-3.1, -0.1, 2.8)       # the three test columns
CHIP_X = 5.55
NAME_L = -6.6
HEAD_Y = 3.13
ICON_H = 0.62
ROW_Y0, ROW_P = 2.42, 0.5
MINI_H = 0.6
HINT = "tree or tangle?  ·  what is updated, how often?  ·  one structure or many?"

APPS = [
    ("blog", [("tree", TEAL), ("rare edits", TEAL), ("one shape", BLUE)], "documents"),
    ("bank", [("tangle", BLUE), ("constant, critical", BLUE), ("one shape", BLUE)], "tables"),
    ("event log", [("flat", TEAL), ("written once", TEAL), ("many shapes", TEAL)], "documents"),
    ("shop", [("tree", TEAL), ("some", FG), ("many shapes", TEAL)], "hybrid"),
    ("settings", [("tree", TEAL), ("rare", TEAL), ("versions differ", TEAL)], "documents"),
]


def row_y(i):
    return ROW_Y0 - i * ROW_P


def area_top(i):
    return row_y(i) - 0.45


# ---------------------------------------------------------------- icons
def shape_icon():
    p = {"r": (0, 0.55), "a": (-0.5, 0), "b": (0.5, 0), "c": (-0.75, -0.55), "d": (-0.25, -0.55),
         "e": (0.25, -0.55), "f": (0.75, -0.55)}
    p = {k: np.array([x, y, 0]) for k, (x, y) in p.items()}
    edges = [("r", "a"), ("r", "b"), ("a", "c"), ("a", "d"), ("b", "e"), ("b", "f")]
    tree = VGroup(*[Line(p[a], p[b]).set_stroke(TEAL, 4) for a, b in edges],
                  *[Dot(v, radius=0.1, color=TEAL) for v in p.values()])
    q = {k: np.array([v[0] * 0.23, v[1] * 0.4, 0]) for k, v in G3.TANGLE_POS.items()}
    pairs = [("coogan", "kid"), ("chaplin", "kid"), ("chaplin", "gold"), ("coogan", "gold")]
    tg = VGroup(*[Line(q[a], q[b]).set_stroke(FG, 4) for a, b in pairs],
                *[Dot(v, radius=0.12, color=DIM) for v in q.values()])
    return VGroup(tree, tg).arrange(RIGHT, buff=0.55)


def writes_icon():
    b1 = Square(0.8).set_stroke(FG, 3)
    b2 = Square(0.8).set_stroke(FG, 3)
    neq = VGroup(Line(LEFT * 0.22, RIGHT * 0.22).shift(UP * 0.09), Line(LEFT * 0.22, RIGHT * 0.22).shift(DOWN * 0.09),
                 Line(DL * 0.2, UR * 0.2)).set_stroke(RED, 5)
    VGroup(b1, neq, b2).arrange(RIGHT, buff=0.25)
    v1 = Rectangle(width=0.4, height=0.36).set_stroke(width=0).set_fill(GOLD, 1)
    v1.move_to(b1).align_to(b1, DOWN).shift(0.12 * UP)
    v2 = Rectangle(width=0.4, height=0.58).set_stroke(width=0).set_fill(GOLD, 1)
    v2.move_to(b2).align_to(b2, DOWN).shift(0.12 * UP)
    body = Rectangle(width=0.2, height=0.75).set_stroke(width=0).set_fill(YELLOW, 1)
    tip = Polygon([-0.1, -0.375, 0], [0.1, -0.375, 0], [0, -0.6, 0]).set_stroke(width=0).set_fill(GOLD, 1)
    cap = Rectangle(width=0.2, height=0.14).set_stroke(width=0).set_fill(DIM, 1).move_to([0, 0.445, 0])
    pencil = VGroup(body, tip, cap).rotate(-0.6)
    pencil.shift(b2.get_corner(UR) + np.array([-0.05, -0.05, 0]) - tip.get_vertices()[2])
    return VGroup(b1, v1, neq, b2, v2, pencil)


def kinds_icon():
    out = VGroup()
    for w, h, (x, y) in ((0.8, 1.1, (-0.45, 0.12)), (1.2, 0.72, (0.05, -0.12)), (0.66, 0.92, (0.55, 0.2))):
        f = RoundedRectangle(corner_radius=0.1, width=w, height=h).set_stroke(TEAL, 3).set_fill(BG, 1)
        f.move_to([x, y, 0])
        n = 3 if h > 0.8 else 2
        ls = VGroup(*[Line(LEFT * (w / 2 - 0.15), RIGHT * (w / 2 - 0.15 - 0.12 * (k % 2)))
                      .set_stroke(TEAL, 2, opacity=0.6) for k in range(n)]).arrange(DOWN, buff=0.16)
        ls.move_to(f)
        out.add(VGroup(f, ls))
    return out


ICONS = (shape_icon, writes_icon, kinds_icon)


def verdict_chip(kind):
    w, h = 2.1, 0.42
    if kind == "hybrid":
        lf = Rectangle(width=w / 2, height=h).set_stroke(width=0).set_fill(TEAL, 0.3).shift(LEFT * w / 4)
        rt = Rectangle(width=w / 2, height=h).set_stroke(width=0).set_fill(BLUE, 0.3).shift(RIGHT * w / 4)
        ol = VGroup(Line([-w / 2, h / 2, 0], [0, h / 2, 0]), Line([-w / 2, -h / 2, 0], [0, -h / 2, 0]),
                    Line([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0])).set_stroke(TEAL, 2)
        orr = VGroup(Line([0, h / 2, 0], [w / 2, h / 2, 0]), Line([0, -h / 2, 0], [w / 2, -h / 2, 0]),
                     Line([w / 2, h / 2, 0], [w / 2, -h / 2, 0])).set_stroke(BLUE, 2)
        box = VGroup(lf, rt, ol, orr)
        lab = T("hybrid", 28, FG)
    else:
        col = TEAL if kind == "documents" else BLUE
        box = Rectangle(width=w, height=h).set_stroke(col, 2).set_fill(col, 0.15)
        lab = T(kind, 28, col)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def recap_r1():
    icons = VGroup(*[f().scale_to_fit_height(0.9) for f in ICONS]).arrange(RIGHT, buff=0.7)
    chips = VGroup(*[verdict_chip(a[2]) for a in APPS]).arrange(DOWN, buff=0.14)
    chips.next_to(icons, DOWN, buff=0.5)
    g = VGroup(icons, chips).move_to(ORIGIN)
    g.icons, g.chips = icons, chips
    return g


# ---------------------------------------------------------------- rows
def name_t(i):
    t = T(APPS[i][0], 30)
    return t.move_to([NAME_L + t.width / 2, row_y(i), 0])


def mark_t(i, k):
    s, col = APPS[i][1][k]
    return T(s, 28, col).move_to([COL_X[k], row_y(i), 0])


def chip_at(i):
    return verdict_chip(APPS[i][2]).move_to([CHIP_X, row_y(i), 0])


# ---------------------------------------------------------------- blog
BLOG = ('{\n  "title": "Making databases cool again",\n  "body": "...",\n  "tags": ["databases", "json"],\n'
        '  "comments": [\n    {"user_id": "u42", "name": "Ada", "text": "Nice!"}\n  ]\n}')
POSTS = ['{"title": "Making databases...",\n "comments": [{"user_id": "u42",\n   "name": "Ada", "text": "Nice!"}]}',
         '{"title": "JSON in practice",\n "comments": [{"user_id": "u7",\n   "name": "Grace", "text": "Yes!"}]}',
         '{"title": "Why indexes?",\n "comments": [{"user_id": "u42",\n   "name": "Ada", "text": "Agreed"}]}']
POST_USERS = ["u42", "u7", "u42"]
USERS = [("u42", "Ada"), ("u7", "Grace")]
GENRES = '"genres": ["Comedy", "Drama", "Family"]'

# ---------------------------------------------------------------- bank
BANK_CARDS = [("customers", ["customer_id", "name"], 3.0, -4.8),
              ("accounts", ["account_id", "customer_id", "balance"], 3.2, -0.6),
              ("transfers", ["transfer_id", "from_account", "to_account", "amount"], 3.5, 4.3)]
ACC1 = '{"account_id": "a1",\n "transfers": [\n   {"to": "a2",\n    "amount": 50}]}'
ACC2 = '{"account_id": "a2",\n "transfers": [\n   {"from": "a1",\n    "amount": 50}]}'
DOTS = {"a1": (-4.6, -1.45), "a2": (-1.7, -3.3), "a3": (1.0, -1.4), "a4": (4.5, -3.15), "a5": (-0.4, -2.45),
        "a6": (2.6, -2.2)}
TRANSFERS = [("a1", "a4"), ("a2", "a3"), ("a1", "a5"), ("a5", "a4"), ("a3", "a4"), ("a2", "a6"), ("a6", "a3"),
             ("a5", "a6")]

# ---------------------------------------------------------------- log
EV1 = '{"time": "2026-10-27T10:04:12Z",\n "function": "send_email",\n "args": {"to": "ada@example.com"}}'
EV2 = ('{"time": "2026-10-27T10:04:13Z",\n "function": "resize_image",\n'
       ' "args": {"width": 640, "height": 480}}')
ARGS = ['{"to": "ada@example.com"}', '{"width": 640, "height": 480}']

# ---------------------------------------------------------------- shop
P_COLS = ["product_id", "name", "price", "attributes"]
P_ROWS = [["1", "My Autobiography", "9", '{"author":\n "Charles Chaplin"}'],
          ["2", "Walking boot", "79", '{"size": 42}'],
          ["3", "Cinema 55", "499", '{"resolution":\n "3840x2160"}']]
SHOP_KEYS = ['"author"', '"size"', '"resolution"']

# ---------------------------------------------------------------- settings
SET1 = '{"user_id": "u42",\n "language": "en-GB",\n "notifications":\n   {"email": false,\n    "push": true}}'
SET2 = ('{"user_id": "u7",\n "language": "fr-FR",\n "notifications":\n   {"email": true,\n    "push": true},\n'
        ' "theme": "dark"}')


def padlock():
    body = RoundedRectangle(corner_radius=0.06, width=0.5, height=0.4).set_stroke(FG, 3).set_fill(FG, 0.15)
    shackle = Arc(radius=0.15, start_angle=0, angle=PI).set_stroke(FG, 4)
    shackle.next_to(body, UP, buff=0)
    hole = Dot(body.get_center(), radius=0.05, color=FG)
    return VGroup(body, shackle, hole)


def coin():
    c = Circle(radius=0.32).set_stroke(GOLD, 4).set_fill(GOLD, 0.3)
    ci = Circle(radius=0.21).set_stroke(GOLD, 2)
    lab = T("+30", 32, GOLD).next_to(c, RIGHT, buff=0.18)
    return VGroup(c, ci, lab)


class PTable(VGroup):
    """products(product_id, name, price, attributes): BLUE row table, attributes as TEAL JSON chips."""

    def __init__(self, size=27, pad=0.14, hdr=0.5, pitch=0.52):
        super().__init__()
        cw = []
        for j, c in enumerate(P_COLS):
            vals = [(D.json_code(r[j], 27).width + 0.24) if j == 3 else Mono(r[j], size).width for r in P_ROWS]
            cw.append(max([Mono(c, size).width] + vals) + 2 * pad)
        w = sum(cw)
        rh = [max(pitch, D.json_code(r[3], 27).height + 0.14) for r in P_ROWS]
        h = hdr + sum(rh)
        top, left = h / 2, -w / 2
        xs = [left + sum(cw[:j]) for j in range(4)]
        self.box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.band = Rectangle(width=w, height=hdr).set_stroke(width=0).set_fill(BLUE, 0.35)
        self.band.move_to([0, top - hdr / 2, 0])
        lines = [Line([left, top - hdr, 0], [-left, top - hdr, 0]).set_stroke(BLUE, 2)]
        lines += [Line([x, top, 0], [x, -top, 0]).set_stroke(DIM, 1.5) for x in xs[1:]]
        lines += [Line([left, top - hdr - sum(rh[:k]), 0], [-left, top - hdr - sum(rh[:k]), 0]).set_stroke(DIM, 1)
                  for k in (1, 2)]
        self.heads, self.cells, self.chips = [], [], []
        for j, c in enumerate(P_COLS):
            t = Mono(c, size, weight=BOLD).move_to([xs[j] + cw[j] / 2, top - hdr / 2, 0])
            self.heads.append(t)
        ul = Line(self.heads[0].get_corner(DL) + 0.07 * DOWN, self.heads[0].get_corner(DR) + 0.07 * DOWN)
        ul.set_stroke(FG, 2.5)
        for i, r in enumerate(P_ROWS):
            y = top - hdr - sum(rh[:i]) - rh[i] / 2
            row = []
            for j, v in enumerate(r):
                if j < 3:
                    t = Mono(v, size, GOLD if j == 2 else FG)
                    t.move_to([xs[j] + pad + t.width / 2, y, 0])
                    row.append(t)
                else:
                    code = D.json_code(v, 27)
                    fr = RoundedRectangle(corner_radius=0.1, width=code.width + 0.24, height=code.height + 0.08)
                    fr.set_stroke(TEAL, 2).set_fill(TEAL, 0.08)
                    chip = VGroup(fr, code.move_to(fr))
                    chip.move_to([xs[j] + pad + chip.width / 2, y, 0])
                    self.chips.append(chip)
                    row.append(chip)
            self.cells.append(row)
        self.add(self.band, self.box, *lines, *self.heads, ul, *[m for r in self.cells for m in r])


# ---------------------------------------------------------------- scene
class Ch10S2Choose(NarratedScene):
    def construct(self):
        self.clip1()
        self.blog()
        self.bank()
        self.log()
        self.shop()
        self.settings()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ helpers
    def mark(self, c, i, k, cue, nxt=None):
        c.wait_until(cue)
        m = mark_t(i, k)
        self.play(*appear(m), run_time=min(1.0, max(0.5, 0.8 * c.until(nxt))))
        return m

    def open_row(self, c, i, old, *incoming, rt=1.6):
        """Clear the last sketch, write the new row's name, bring in the first piece of the new sketch."""
        name = name_t(i)
        anims = during(disappear(*old), 0, 0.45) + during(appear(name, shift=None), 0.3, 0.7)
        anims += during(list(incoming), 0.5, 1) if incoming else []
        self.play(*anims, run_time=rt)

    # ------------------------------------------------------------ c10.choose.1
    def clip1(self):
        nc = R9.next_card()
        cards = nc.cards
        for n in (18, 19):
            cards[n].box.set_stroke(opacity=0.3)
            for part in cards[n][1:]:
                part.set_opacity(0.3)
        c17 = cards[17]
        self.add(c17.box, c17.head, c17.title, c17.lines, cards[18], cards[19])

        big = EX7.exercise_card(17, max_w=13.0, max_h=6.45)
        big.move_to([0, 3.6 - big.height / 2, 0])
        hint = T(HINT, 28, DIM)
        pause = S1.pause_icon(0.6)
        VGroup(hint, pause).arrange(RIGHT, buff=0.45).next_to(big, DOWN, buff=0.3)
        with self.say("c10.choose.1") as c:
            self.play(ReplacementTransform(c17.box, big.box),
                      *during(disappear(c17.head, c17.title, c17.lines, cards[18], cards[19]), 0, 0.4),
                      *during(appear(big.text, shift=None), 0.55, 1),
                      run_time=1.8)  # early: the exercise card, read whole
            c.wait_until("justify")
            self.play(*appear(hint, shift=None), run_time=1.0)  # early: the hint, shown with its exercise
            c.wait_until("stop")
            self.play(FadeIn(pause, scale=0.8), run_time=1.0)
            c.wait_until("tests")
            mini = RoundedRectangle(corner_radius=0.12, width=2.3, height=MINI_H).set_stroke(DIM, 2)
            mini.move_to([NAME_L + 1.15, HEAD_Y, 0])
            mlab = T("Exercise 17", 28, YELLOW).move_to(mini)
            self.play(ReplacementTransform(big.box, mini), *during(disappear(big.text, hint, pause), 0, 0.4),
                      *during(appear(mlab, shift=None), 0.6, 1), run_time=1.5)
            big = VGroup(mini, mlab)

            xs = (-4.5, 0.0, 4.5)
            icons = [f().scale_to_fit_height(1.7).move_to([x, 0.5, 0]) for f, x in zip(ICONS, xs)]
            caps = [T(s, 32).move_to([x, -0.9, 0])
                    for s, x in zip(("tree or tangle?", "copies disagree?", "one structure?"), xs)]
            c.wait_until("shape")
            self.play(*appear(icons[0], caps[0], lag=0.3, shift=None), run_time=1.2)
            c.wait_until("writes")
            self.play(*appear(icons[1], shift=None), run_time=1.0)
            c.wait_until(own_word=caps[1], cue="disagree")
            self.play(*appear(caps[1]), run_time=0.8)
            c.wait_until("kinds")
            self.play(*appear(icons[2], shift=None), run_time=1.0)
            c.wait_until(own_word=caps[2], cue="one structure")
            self.play(*appear(caps[2]), run_time=0.8)
            noans = T("no official answers: the justification counts", 30, DIM).move_to([0, -2.5, 0])
            c.wait_until(own_word=noans, cue="noanswer")
            self.play(*appear(noans), run_time=1.0)
        self.mini, self.icons, self.caps, self.noans = big, icons, caps, noans

    # ------------------------------------------------------------ c10.choose.2  blog
    def blog(self):
        with self.say("c10.choose.2") as c:
            name = name_t(0)
            moves = [ic.animate.scale_to_fit_height(ICON_H).move_to([COL_X[k], HEAD_Y, 0])
                     for k, ic in enumerate(self.icons)]
            self.play(*during(disappear(*self.caps), 0, 0.4), *during(moves, 0.15, 0.85),
                      *during(appear(name, shift=None), 0.6, 1), run_time=1.8)

            post = D.doc_card(BLOG, size=26, pad=0.2)
            post.move_to([0, area_top(0) - 0.1 - post.height / 2, 0])
            c.wait_until("post")
            self.play(*during(disappear(self.noans), 0, 0.45), *during(appear(post, shift=None), 0.4, 1),
                      run_time=1.4)
            self.mark(c, 0, 0, "is a tree", "so one document")
            c.wait_until("one document per post")
            chip = chip_at(0)
            self.play(*appear(mark_t(0, 2), chip, lag=0.4), run_time=1.2)
            self.chips = [chip]

            c.wait_until("genres")
            tags = post.code.find('"tags": ["databases", "json"]')
            ghost = D.json_code(GENRES, 27).set_color(DIM)
            kid = T("The Kid", 28, DIM)
            gg = VGroup(kid, ghost).arrange(RIGHT, buff=0.4)
            gg.next_to(post, DOWN, buff=0.3).align_to(post.code, LEFT)
            self.play(FlashAround(tags, time_width=1.5), *recolor(tags, YELLOW),
                      *during(appear(gg, shift=None), 0.4, 1), run_time=1.5)  # early: the genres ghost, named in this sentence

            # {authors}: three posts, compact; two readers; arrows by ID: a small tangle
            c.wait_until("authors")
            posts = [D.doc_card(src, size=26, pad=0.2) for src in POSTS]
            for p in posts[1:]:
                p.code.set_opacity(0.5)
                p.frame.set_stroke(opacity=0.5)
            col = VGroup(*posts).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            col.move_to([NAME_L + col.width / 2, (area_top(0) - 3.7) / 2, 0])
            self.play(*during(disappear(post, gg), 0, 0.45),
                      *during(appear(*posts, lag=0.25, shift=None), 0.5, 1), run_time=1.6)
            users = {}
            for (uid, nm), p in zip(USERS, (posts[0], posts[2])):
                u = D.doc_card(f'{{"user_id": "{uid}",\n "name": "{nm}"}}', size=26, pad=0.2)
                u.move_to([6.6 - u.width / 2, (p.get_y() + posts[1].get_y()) / 2, 0])
                users[uid] = u
            arrows = []
            for p, uid in zip(posts, POST_USERS):
                p0 = np.array([p.frame.get_right()[0] + 0.06, p.code.line(1).get_y(), 0])
                dst = users[uid].get_left() + 0.08 * LEFT
                arrows.append(Arrow(p0, dst, buff=0, stroke_width=3, tip_length=0.18, color=FG))
            self.play(*appear(*users.values(), lag=0.2, shift=None),
                      *[time_span(GrowArrow(a), 0.4 + 0.15 * k, 1.2 + 0.15 * k) for k, a in enumerate(arrows)],
                      run_time=1.8)
            c.wait_until("copied name")
            gold = []
            for p, uid in zip(posts, POST_USERS):
                gold += list(p.code.find(f'"name": "{dict(USERS)[uid]}"'))
            self.play(*recolor(gold, GOLD), *flash([p.code.find('"name"') for p in posts], color=GOLD),
                      run_time=1.2)
            self.mark(c, 0, 1, "update if they rename")
            post, p2, p3 = posts
            users = list(users.values())
            self.sketch = [post, p2, p3, *users, *arrows]

    # ------------------------------------------------------------ c10.choose.3  bank
    def bank(self):
        with self.say("c10.choose.3") as c:
            top = area_top(1) - 0.05
            cards = {}
            for nm, cols, w, x in BANK_CARDS:
                cd = T5.ProdCard(nm, cols, w=w)
                cd.move_to([x, top - cd.height / 2, 0])
                cards[nm] = cd
            cu, ac, tr = cards["customers"], cards["accounts"], cards["transfers"]
            fks = [Arrow([tr.box.get_left()[0], tr.rows[1].get_y(), 0],
                         [ac.box.get_right()[0], ac.rows[0].get_y() + 0.07, 0], buff=0, stroke_width=3,
                         tip_length=0.16, color=FG),
                   Arrow([tr.box.get_left()[0], tr.rows[2].get_y(), 0],
                         [ac.box.get_right()[0], ac.rows[0].get_y() - 0.07, 0], buff=0, stroke_width=3,
                         tip_length=0.16, color=FG),
                   Arrow([ac.box.get_left()[0], ac.rows[1].get_y(), 0],
                         [cu.box.get_right()[0], cu.rows[0].get_y(), 0], buff=0, stroke_width=3,
                         tip_length=0.16, color=FG)]
            self.open_row(c, 1, self.sketch, *appear(cu, ac, tr, lag=0.2, shift=None), rt=1.7)
            self.play(*[GrowArrow(a) for a in fks], run_time=0.8)

            # {transfers}: the accounts as dots, transfers as crossing lines
            dots, lines = {}, []
            for k, (x, y) in DOTS.items():
                circ = Circle(radius=0.34).set_stroke(BLUE, 3).set_fill(BLUE, 0.15).move_to([x, y, 0])
                lab = Mono(k, 26).move_to(circ)
                dots[k] = VGroup(circ, lab)
            for a, b in TRANSFERS:
                lines.append(Line(dots[a].get_center(), dots[b].get_center(), buff=0.36).set_stroke(FG, 3))
            c.wait_until("transfers")
            self.play(FlashAround(ac.box, time_width=1.5), *appear(*dots.values(), lag=0.1, shift=None),
                      *[time_span(Create(l), 0.7, 1.6) for l in lines], run_time=1.6)
            self.mark(c, 1, 0, "so this is a tangle", "copies")
            tangle = [*lines, *dots.values()]

            # {copies}: the tempting document version
            c.wait_until("copies")
            d1 = D.doc_card(ACC1, size=26, pad=0.2)
            d2 = D.doc_card(ACC2, size=26, pad=0.2)
            VGroup(d1, d2).arrange(RIGHT, buff=1.4).move_to([-0.6, (tr.get_bottom()[1] - 3.7) / 2, 0])
            self.play(*during(disappear(*tangle), 0, 0.45), *set_alpha([cu, ac, tr, *fks], DIMMED),
                      *during(appear(d1, d2, lag=0.3, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("can disagree")
            old = d2.code.find("50")
            new = Mono("80", 27, GOLD).move_to(old)
            self.play(*during([o.animate.set_opacity(0).shift(0.2 * UP) for o in old], 0, 0.45),
                      *during([FadeIn(new, shift=0.2 * UP)], 0.5, 1), run_time=1.2)
            neq = T("≠", 60, RED).move_to(VGroup(d1, d2).get_center())
            self.play(FadeIn(neq, scale=0.7), FlashAround(new, color=RED), run_time=1.0)
            cn = coin().next_to(d2, RIGHT, buff=0.5)
            c.wait_until("money appears")
            self.play(FadeIn(cn, scale=0.3), run_time=0.8)

            # {tables}: back to the cards; one transfers row, one fact
            c.wait_until("tables")
            vals = ["t1", "a1", "a2", "50"]
            cells = VGroup(*[Rectangle(width=0.95, height=0.55).set_stroke(GREEN, 2) for _ in vals])
            cells.arrange(RIGHT, buff=0)
            txt = [Mono(v, 28, GOLD if v == "50" else FG).move_to(cl) for v, cl in zip(vals, cells)]
            glow = Rectangle(width=cells.width + 0.12, height=0.67).set_stroke(GREEN, 4).set_fill(GREEN, 0.15)
            strip = VGroup(glow, cells, *txt).move_to([tr.get_x(), tr.get_bottom()[1] - 0.75, 0])
            fact = T("one fact, one place", 32, GREEN).next_to(strip, DOWN, buff=0.3)
            self.play(*during(disappear(d1, d2, new, neq, cn), 0, 0.45), *set_alpha([cu, ac, tr, *fks], 1),
                      *during(appear(strip, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until(own_word=fact, cue="one fact")
            self.play(*appear(fact), FlashAround(strip, color=GREEN, time_width=1.5), run_time=1.2)
            self.mark(c, 1, 1, "balances change constantly", "same structure")
            self.mark(c, 1, 2, "same structure", "database checks")
            c.wait_until("tables win")
            chip = chip_at(1)
            self.play(*appear(chip), run_time=1.0)
            self.chips.append(chip)
            self.sketch = [cu, ac, tr, *fks, strip, fact]

    # ------------------------------------------------------------ c10.choose.4  event log
    def log(self):
        with self.say("c10.choose.4") as c:
            e1 = D.doc_card(EV1, size=26, pad=0.2)
            e2 = D.doc_card(EV2, size=26, pad=0.2)
            col = VGroup(e1, e2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            col.move_to([-1.7, (area_top(2) - 3.7) / 2, 0])
            self.open_row(c, 2, self.sketch, FadeIn(e1, shift=2.5 * LEFT), rt=1.4)
            self.play(FadeIn(e2, shift=2.5 * LEFT), run_time=1.0)
            c.wait_until("writeonce")
            locks = [padlock().move_to([col.get_right()[0] + 0.6, e.get_y(), 0]) for e in (e1, e2)]
            once = T("written once", 32).move_to([locks[0].get_x() + 0.5 + 1.15, col.get_y(), 0])
            self.play(*appear(*locks, lag=0.25, shift=None), *during(appear(once, shift=None), 0.4, 1),
                      run_time=1.3)
            self.mark(c, 2, 1, "never changed", "args")
            c.wait_until("args")
            boxes = []
            for e, a in zip((e1, e2), ARGS):
                boxes.append(token_box(e.code.find(a), e.code.line(2)))
            self.play(*[FadeIn(b) for b in boxes], run_time=1.0)
            self.mark(c, 2, 2, "many shapes", "documents fit")
            c.wait_until("documents fit perfectly")
            chip = chip_at(2)
            self.play(*appear(mark_t(2, 0), chip, lag=0.4), run_time=1.2)
            self.chips.append(chip)
            c.wait_until("object of its arguments")
            self.play(*flash(boxes, time_width=1.5), run_time=1.5)
            self.sketch = [e1, e2, *locks, once, *boxes]

    # ------------------------------------------------------------ c10.choose.5  shop
    def shop(self):
        with self.say("c10.choose.5") as c:
            self.open_row(c, 3, self.sketch, rt=1.4)
            docs = [D.doc_card(s, size=26, pad=0.2) for s in (T5.BOOK, T5.SHOE, T5.TV)]
            r1 = VGroup(docs[0], docs[1]).arrange(RIGHT, buff=0.5)
            grid = VGroup(r1, docs[2]).arrange(DOWN, buff=0.3)
            grid.move_to([0, (area_top(3) - 3.7) / 2, 0])
            c.wait_until("attrs")
            self.play(*appear(*docs, lag=0.3, shift=None), run_time=1.5)
            c.wait_until("different attributes")
            boxes = [token_box(d.code.find(k), d.code.line(2)) for d, k in zip(docs, SHOP_KEYS)]
            self.play(*[FadeIn(b) for b in boxes], run_time=1.0)
            self.mark(c, 3, 2, "handles well", "one document per product")
            self.mark(c, 3, 0, "one document per product", "hybrid")

            c.wait_until("hybrid")
            pt = PTable()
            orders = T5.ProdCard("orders", [], w=2.6)
            stock = T5.ProdCard("stock", [], w=2.6)
            pt.move_to([0, area_top(3) + 0.1 - pt.height / 2, 0])
            orders.move_to([-3.2, -3.75 + orders.height / 2, 0])
            stock.move_to([3.2, -3.75 + stock.height / 2, 0])
            arrs = [Arrow([cd.get_x(), cd.get_top()[1], 0], [cd.get_x(), pt.get_bottom()[1], 0], buff=0.05,
                          stroke_width=3, tip_length=0.18, color=FG) for cd in (orders, stock)]
            self.play(*during(disappear(*docs, *boxes), 0, 0.45),
                      *during(appear(orders, stock, pt, lag=0.2, shift=None), 0.5, 1), run_time=1.6)
            self.play(*[GrowArrow(a) for a in arrs], run_time=0.8)
            self.mark(c, 3, 1, "suit tables", "a hybrid")
            c.wait_until("a hybrid")
            chip = chip_at(3)
            self.play(*appear(chip), run_time=1.0)
            self.chips.append(chip)
            c.wait_until("name and price")
            self.play(*flash([pt.heads[1], pt.heads[2]], time_width=1.5), run_time=1.3)
            c.wait_until("json column")
            self.play(FlashAround(VGroup(*pt.chips), color=TEAL, time_width=1.5), run_time=1.5)
            self.sketch = [pt, orders, stock, *arrs]

    # ------------------------------------------------------------ c10.choose.6  settings
    def settings(self):
        with self.say("c10.choose.6", gap=2.5) as c:
            self.open_row(c, 4, self.sketch, rt=1.4)
            s1 = D.doc_card(SET1, size=26, pad=0.2)
            s2 = D.doc_card(SET2, size=26, pad=0.2)
            for g in s2.code.find('"theme"'):
                g.set_color(GREEN)
            mid = (area_top(4) - 3.7) / 2
            s1.move_to([-4.2, area_top(4) - 0.05 - s1.height / 2, 0])
            s2.move_to([1.3, area_top(4) - 0.05 - s2.height / 2, 0])
            v2 = T("version 2", 30, GREEN).next_to(s2, RIGHT, buff=0.3).align_to(s2, UP).shift(0.1 * DOWN)
            c.wait_until("onedoc")
            self.play(*appear(s1, shift=None), run_time=1.2)
            self.mark(c, 4, 0, "read in one go", "referred to")
            self.mark(c, 4, 1, "referred to by nothing else", "versions")
            c.wait_until("versions")
            self.play(*appear(s2, shift=None), run_time=1.3)
            c.wait_until(own_word=v2, cue="new version")
            self.play(*appear(v2), run_time=1.0)
            self.mark(c, 4, 2, "old and new documents mix", "fills in")
            dflt = D.json_code('"theme": "light"', 26).set_color(DIM)
            dflt.next_to(s1, DOWN, buff=0.2).align_to(s1.code, LEFT).shift(0.22 * RIGHT)
            c.wait_until("fills in a default")
            self.play(*appear(dflt, shift=None), run_time=1.0)
            c.wait_until("verdict")
            chip = chip_at(4)
            self.play(*appear(chip), run_time=0.8)
            self.chips.append(chip)
            self.play(*set_alpha([s1.code, s2.code, v2, dflt], DIMMED),
                      *[f.animate.set_stroke(opacity=0.3) for f in (s1.frame, s2.frame)],
                      *[time_span(FlashAround(ch, time_width=1.5), 0.1 * k, 1.0 + 0.1 * k)
                        for k, ch in enumerate(self.chips)], run_time=1.4)
