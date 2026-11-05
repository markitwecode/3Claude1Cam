"""Chapter 8, scene 5: Searching text (EXISTS over unnested trivia, ILIKE's limits, search engines).
Clips c8.text.1 – c8.text.4.

Shared pieces (`from lib.paths import load_scene; M = load_scene("ch8_s5_text")`):
- `recap_thumb()` -> static VGroup at ORIGIN: the word "Thacker" (T 72, FG) with its letters
  "hacker" RED, about 3.3 wide x 0.75 tall. `.word`, `.hacker` (the six RED glyphs).
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
from lib.style import *  # noqa: E402,F403

Q_SRC = """SELECT movie->>'title' AS title, movie->>'year' AS year
FROM    movies
WHERE EXISTS (
     SELECT 1
     FROM   unnest(movie->>'$.trivia_entries[*]') AS t(e)
     WHERE e ILIKE '%hacker%'
)
ORDER BY title;"""
Q_SIZE = 27

KID_FREE = [
    "Due to the fact that Jackie Coogan's mother and stepfather…",
    "The off-screen chemistry between Sir Charles Chaplin and…",
    "This was Sir Charles Chaplin's first feature length film…",
    "Sir Charles Chaplin and Jackie Coogan met for the last time…",
    "The production company tried to cheat Sir Charles Chaplin…",
]
KID_LOOP = [
    "Due to the fact that Jackie Coogan's mother and…",
    "The off-screen chemistry between Sir Charles…",
    "This was Sir Charles Chaplin's first feature length…",
    "Sir Charles Chaplin and Jackie Coogan met for the…",
    "The production company tried to cheat Sir Charles…",
]
HACK_LOOP = [
    "Jonny Lee Miller and Angelina Jolie were married…",
    "The \"hacking\"-sequences - the scenes where you…",
    "Eugene Belford uses the pseudonym Babbage at the…",
    "The high school scenes were filmed at Stuyvesant…",
    "The bearded London hacker is David A. Stewart of Eurythmics.",
]
RESULT = [("Hackers", "1995"), ("Mission: Impossible", "1996"), ("Notting Hill", "1999"),
          ("Upgrade", "2018"), ("Who Am I", "2014")]
THACKER = ["(at around 1h 28 mins) The long shot where William Thacker walks",
           "through Notting Hill during summer, fall, winter, and spring was",
           "actually four different shots, all filmed the same day."]
SNOWDEN = ["To make sure the screenplay was not hacked or leaked, Oliver Stone",
           "wrote the script on a single computer with no Internet connection."]
HACK28 = ["Army of Thieves", "Death Wish", "Dolores Claiborne", "Dragged Across Concrete",
          "Enemy of the State", "Equilibrium", "Hackers", "Icarus", "Infinity Pool",
          "Mission: Impossible", "Notting Hill", "Parker", "Peter Rabbit", "RKO 281",
          "Resident Evil: Extinction", "Runaway Jury", "Snowden", "The Huntsman: Winter's War",
          "The Lost Battalion", "The Lost City of Z", "The Royal Tenenbaums",
          "The Shawshank Redemption", "The Signal", "The World's Fastest Indian",
          "Top Gun: Maverick", "Unforgiven", "Upgrade", "Who Am I"]
HACKMAN = {"Enemy of the State", "RKO 281", "Runaway Jury", "The Royal Tenenbaums",
           "The Shawshank Redemption", "Unforgiven"}
UNFORGIVEN = ["The script floated", "around Hollywood", "for almost 20 years.",
              "Gene Hackman read", "and rejected it, …"]
# illustrative relevance scores (search engines rank; these are not computed)
RELEVANCE = {"Hackers": 1.0, "Who Am I": 0.8, "Upgrade": 0.62, "Mission: Impossible": 0.45,
             "Notting Hill": 0.12}


def recap_thumb():
    word = T("Thacker", 72)
    hk = select(word, "hacker")[0]
    hk.set_color(RED)
    g = VGroup(word)
    g.word, g.hacker = word, hk
    return g.move_to(ORIGIN)


def query():
    return Code(Q_SRC, size=Q_SIZE)


def pattern(word, size=36):
    p = Code(f"WHERE e ILIKE '%{word}%'", size=size)
    p.find("ILIKE").set_color(YELLOW)
    for k in range(2):
        p.find("%", nth=k).set_color(GOLD)
    return p


def strip(text, w, size=30, color=DIM, stroke=TEAL):
    t = T(text, size, color)
    r = RoundedRectangle(corner_radius=0.1, width=w, height=0.6).set_stroke(stroke, 2)
    t.move_to(r).align_to(r.get_left() + 0.25 * RIGHT, LEFT)
    g = VGroup(r, t)
    g.text = t
    return g


def tile(word, size=32, color=FG, stroke=BLUE):
    t = Mono(word, size, color)
    r = RoundedRectangle(corner_radius=0.1, width=t.width + 0.4, height=0.62).set_stroke(stroke, 2)
    r.move_to(t)
    g = VGroup(r, t)
    g.text, g.frame = t, r
    return g


def entry_block(lines, size=30, color=FG, t2c=None):
    g = VGroup(*[T(s, size, color, t2c=t2c or {}) for s in lines]).arrange(DOWN, buff=0.18)
    return g


def result_table(size=32, pitch=0.55):
    h_t, h_y = Mono("title", size), Mono("year", size)
    titles = [Mono(t, size, color=BLUE) for t, _ in RESULT]
    years = [Mono(y, size, color=BLUE) for _, y in RESULT]
    x_year = max(t.width for t in titles) + 0.8
    for i, (t, y) in enumerate(zip(titles, years)):
        yy = -(i + 1) * pitch - 0.12
        t.move_to([t.width / 2, yy, 0])
        y.move_to([x_year + y.width / 2, yy, 0])
    h_t.move_to([h_t.width / 2, 0, 0])
    h_y.move_to([x_year + h_y.width / 2, 0, 0])
    right = years[0].get_right()[0]
    rule = Line([-0.1, -0.3, 0], [right + 0.1, -0.3, 0]).set_stroke(DIM, 2)
    rows = [VGroup(t, y) for t, y in zip(titles, years)]
    g = VGroup(h_t, h_y, rule, *rows)
    g.rows = rows
    return g


def bar_rows(scores, title_x, bar_x, max_len, y_top, pitch, size=30, color=GOLD):
    rows = []
    for i, (name, s) in enumerate(scores):
        y = y_top - i * pitch
        t = T(name, size, BLUE).move_to([0, y, 0]).align_to([title_x, 0, 0], RIGHT)
        b = Rectangle(width=max_len * s, height=0.4).set_stroke(width=0).set_fill(color, 0.85)
        b.move_to([bar_x + max_len * s / 2, y, 0])
        g = VGroup(t, b)
        g.name, g.title, g.bar = name, t, b
        rows.append(g)
    return rows


# ---------------------------------------------------------------- the semijoin loop (ch3 s6's look)
LX = -6.6
CARD_X0, CARD_X1 = -4.75, 6.6
CARD_TOP = 1.95
HDR = 0.6
SPITCH = 0.7
LPITCH = 0.8
SSIZE = 28


def loop_left():
    title = Mono("movies", 28, weight=BOLD)
    title.move_to([0, CARD_TOP - HDR / 2, 0]).align_to([LX, 0, 0], LEFT)
    rows = []
    for i, name in enumerate(["The Kid", "Hackers"]):
        y = CARD_TOP - HDR - 0.45 - i * LPITCH
        rows.append(Mono(name, 28, BLUE).move_to([0, y, 0]).align_to([LX, 0, 0], LEFT))
    return title, rows


def loop_card():
    w = CARD_X1 - CARD_X0
    h = HDR + 5 * SPITCH + 0.25
    cx = (CARD_X0 + CARD_X1) / 2
    box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
    box.move_to([cx, CARD_TOP - h / 2, 0])
    div = Line([CARD_X0, CARD_TOP - HDR, 0], [CARD_X1, CARD_TOP - HDR, 0]).set_stroke(BLUE, 2)
    title = Mono("t(e)", 28, weight=BOLD).move_to([cx, CARD_TOP - HDR / 2, 0])
    return VGroup(box, div, title)


def strip_y(i):
    return CARD_TOP - HDR - 0.12 - SPITCH / 2 - i * SPITCH


def loop_strips(texts, color=DIM):
    return [T(s, SSIZE, color).move_to([0, strip_y(i), 0]).align_to([CARD_X0 + 0.22, 0, 0], LEFT)
            for i, s in enumerate(texts)]


def loop_mark(i, ok):
    m = (check_mark() if ok else cross_mark()).scale(0.6)
    return m.move_to([CARD_X1 - 0.32, strip_y(i), 0])


def cursor_at(row):
    r = Rectangle(width=1.95, height=0.5).set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.12).set_z_index(-1)
    return r.move_to([LX + 0.9, row.get_y(), 0])


class SearchText(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ the question, the query, the loop
    def scan(self, bar, n, ok_last, run_time):
        bx = (CARD_X0 + CARD_X1) / 2

        def upd(m, a):
            k = min(int(a * n), n - 1)
            m.move_to([bx, strip_y(k), 0])

        marks = [loop_mark(k, False) for k in range(n - 1 if ok_last else n)]
        anims = [UpdateFromAlphaFunc(bar, upd, rate_func=linear)]
        for k in range(len(marks)):
            anims.append(time_span(FadeIn(marks[k]), (k + 0.5) * run_time / n, (k + 0.9) * run_time / n))
        self.play(*anims, run_time=run_time)
        return marks

    def clip1(self):
        with self.say("c8.text.1") as c:
            head = VGroup(Mono("The Kid", 34, BLUE), Mono("trivia_entries", 30, TEAL)).arrange(RIGHT, buff=0.5)
            strips = [strip(s, 12.0) for s in KID_FREE]
            col = VGroup(*strips).arrange(DOWN, buff=0.18)
            board = VGroup(head, col).arrange(DOWN, buff=0.35).move_to([0, -0.45, 0])
            head.align_to(col, LEFT)
            self.play(*appear(head, shift=None), run_time=0.8)  # early: the document's name, read as the strips arrive
            self.play(*appear(*strips, lag=0.3), run_time=min(1.8, c.until("ask")))  # early: the five entries, shown whole
            c.wait_until("ask")
            ask = T("Which movies have trivia mentioning hackers?", 40, YELLOW).move_to([0, 3.3, 0])
            self.play(*appear(ask), run_time=1.0)
            c.wait_until("query")
            code = query().move_to([0, -0.35, 0])
            self.play(*during(disappear(head, *strips), 0, 0.45), *during(appear(code, shift=None), 0.5, 1),
                      run_time=1.6)
            c.wait_until("un-nest")
            box = token_box(code.find("unnest(movie->>'$.trivia_entries[*]') AS t(e)"), code.line(4))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("match a pattern")
            self.play(Transform(box, token_box(code.find("e ILIKE '%hacker%'"), code.line(5))), run_time=1.0)
            c.wait_until("exists")
            # the query shrinks to the top; the loop comes in under it
            ltitle, lrows = loop_left()
            card = loop_card()
            kid = loop_strips(KID_LOOP)
            cur = cursor_at(lrows[0])
            hdr = Code("WHERE EXISTS ( … )", size=36)
            hdr.move_to([0, 3.2, 0]).align_to([-6.4, 0, 0], LEFT)
            self.play(*during([FadeOut(box), FadeOut(ask)], 0, 0.35),  # early: the loop's shape shown whole, then walked
                      *during(edit(code, hdr), 0.1, 0.6),
                      *during(appear(ltitle, *lrows, card, *kid, shift=None, lag=0.1), 0.55, 1),
                      run_time=1.6)
            self.play(FadeIn(cur), FlashAround(hdr.find("EXISTS"), run_time=1.0), run_time=1.0)
            bar = Rectangle(width=CARD_X1 - CARD_X0 - 0.12, height=SPITCH - 0.04)
            bar.set_stroke(width=0).set_fill(YELLOW, 0.2).set_z_index(-1).move_to([0, strip_y(0), 0])
            marks = self.scan(bar, 5, False, run_time=1.6)
            self.play(lrows[0].animate.set_color(RED), FadeOut(bar), run_time=0.6)
            c.wait_until("semijoin")
            hack = loop_strips(HACK_LOOP)
            lab = VGroup(MathTex(r"\ltimes", font_size=52, color=YELLOW),
                         T("inside one document", 34, YELLOW)).arrange(RIGHT, buff=0.2)
            lab.move_to([0, 3.2, 0]).align_to([6.4, 0, 0], RIGHT)
            self.play(Transform(cur, cursor_at(lrows[1])),
                      *during(disappear(*kid, *marks), 0, 0.45), *during(appear(*hack, shift=None), 0.5, 1),
                      *appear(lab), run_time=1.3)
            bar.move_to([0, strip_y(0), 0])
            bar.set_fill(YELLOW, 0.2)
            marks2 = self.scan(bar, 5, True, run_time=min(1.5, max(1.0, c.until() - 1.0)))
            hk = select(hack[4], "hacker")[0]
            self.play(lrows[1].animate.set_color(GREEN),
                      *[g.animate.set_color(GREEN if any(g is h for h in hk) else FG) for g in hack[4]],
                      run_time=min(0.7, max(0.3, c.until())))
            self.hdr = hdr
            self.loop_parts = [ltitle, *lrows, card, *hack, *marks2, bar, cur, lab]

    # ------------------------------------------------------------ ILIKE, %, five results, Thacker
    def clip2(self):
        with self.say("c8.text.2") as c:
            code = query().move_to([0, 1.35, 0])
            self.play(*during(disappear(*self.loop_parts), 0, 0.45),
                      *during(edit(self.hdr, code), 0.3, 1), run_time=1.6)
            il = code.find("ILIKE")
            leg1 = VGroup(Mono("ILIKE", 32, YELLOW), T("LIKE, ignoring case", 34)).arrange(RIGHT, buff=0.4)
            leg2 = VGroup(Mono("%", 32, GOLD), T("any run of characters", 34)).arrange(RIGHT, buff=0.4)
            leg1.move_to([0, -1.75, 0])
            leg2.move_to([0, -2.65, 0])
            leg2[0].move_to([leg1[0].get_center()[0], leg2.get_y(), 0])
            leg2[1].align_to(leg1[1], LEFT)
            c.wait_until("version of like")
            self.play(*recolor(il, YELLOW), FlashAround(il, run_time=1.2), *appear(leg1), run_time=1.2)
            c.wait_until("percent")
            pcts = [code.find("%", nth=k) for k in range(2)]
            self.play(*recolor(pcts[0], GOLD), *recolor(pcts[1], GOLD),
                      *flash(pcts, color=GOLD, run_time=1.2), *appear(leg2), run_time=1.2)
            c.wait_until("result")
            pat = pattern("hacker").move_to([0, 3.25, 0]).align_to([-6.4, 0, 0], LEFT)
            count = VGroup(T("5", 56, GOLD), T("movies", 34, DIM)).arrange(RIGHT, buff=0.25)
            count.move_to([0, 3.25, 0]).align_to([6.4, 0, 0], RIGHT)
            tab = result_table().move_to([0, 0.75, 0])
            sweep_clear(self, *appear(pat, count, tab, shift=None, lag=0.2), run_time=1.6)  # early: the result, shown whole then named
            c.wait_until("notting")
            row = tab.rows[2]
            q = T("?", 52, GOLD).next_to(row, RIGHT, buff=0.45)
            self.play(*[m.animate.set_color(YELLOW) for m in row], *appear(q), run_time=1.0)
            c.wait_until("thacker")
            ent = entry_block(THACKER).move_to([0, -2.35, 0])
            self.play(*appear(ent, shift=None), run_time=1.0)
            c.wait_until("six letters")
            hk = select(ent[0], "hacker")[0]
            self.play(*recolor(hk, RED), FlashAround(select(ent[0], "Thacker")[0], color=RED, run_time=1.4),
                      run_time=1.4)
            self.pat, self.count, self.tab, self.q, self.ent = pat, count, tab, q, ent

    # ------------------------------------------------------------ too much, too little; %hack%; no rank
    def clip3(self):
        with self.say("c8.text.3") as c:
            much = T("too much", 34, RED).next_to(self.tab.rows[2], RIGHT, buff=0.45)
            self.play(*swap(self.q, much), run_time=1.2)
            c.wait_until("hacked")
            sn_head = Mono("Snowden", 30, BLUE)
            sn = entry_block(SNOWDEN)
            sn_g = VGroup(sn_head, sn).arrange(DOWN, buff=0.22).move_to([0, -2.35, 0])
            sn_head.align_to(sn, LEFT)
            self.play(*swap(self.ent, sn_g), run_time=1.3)
            c.wait_until("hacked", nth=1)
            missed = T("missed", 32, RED).next_to(sn_head, RIGHT, buff=0.4)
            hd = select(sn[0], "hacked")[0]
            self.play(*recolor(hd, GREEN), FlashAround(hd, color=GREEN, run_time=1.2), *appear(missed),
                      run_time=1.2)
            c.wait_until("hack")
            pat2 = pattern("hack").align_to(self.pat, LEFT).align_to(self.pat, UP)
            n28 = T("28", 56, GOLD).move_to(self.count[0]).align_to(self.count[0], RIGHT)
            # 28 titles, three columns
            names = [T(s, 28, BLUE) for s in HACK28]
            cols = [names[0:14], names[14:28]]
            colw = [max(t.width for t in cl) for cl in cols]
            x = -6.5
            for cl, w in zip(cols, colw):
                for i, t in enumerate(cl):
                    t.move_to([0, 2.55 - i * 0.4, 0]).align_to([x, 0, 0], LEFT)
                x += w + 0.35
            gone = [self.tab, much, sn_g, missed]
            self.play(*during(edit(self.pat, pat2), 0, 0.6), *during(swap(self.count[0], n28), 0, 0.6),
                      *during(disappear(*gone), 0, 0.4), *during(appear(*names, shift=None, lag=0.02), 0.45, 1),
                      run_time=2.0)
            c.wait_until("hackman")
            red = [t for t, s in zip(names, HACK28) if s in HACKMAN]
            unf = entry_block(UNFORGIVEN, size=28, t2c={"Gene Hackman": RED})
            unf_head = Mono("Unforgiven", 28, RED)
            for ln in unf:
                ln.align_to(unf, LEFT)
            unf_g = VGroup(unf_head, unf).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            unf_g.move_to([0, -0.4, 0]).align_to([6.6, 0, 0], RIGHT)
            self.play(*[t.animate.set_color(RED) for t in red], *during(appear(unf_g), 0.35, 1), run_time=1.5)
            c.wait_until("ranked")
            scores = [(t, 1.0) for t, _ in RESULT]
            rows = bar_rows(scores, -0.4, -0.1, 5.6, 1.6, 0.8, size=34)
            sweep_clear(self, *appear(*rows, shift=None, lag=0.15), run_time=1.4)  # early: the five results as bars
            c.wait_until("counts as much")
            pick = [rows[0], rows[2]]
            self.play(*[r.title.animate.set_color(YELLOW) for r in pick],
                      *flash([r.bar for r in pick], color=YELLOW, run_time=1.4), run_time=1.4)
            self.rank_rows = rows

    # ------------------------------------------------------------ full-text search engines
    def clip4(self):
        with self.say("c8.text.4") as c:
            W, H = 5.2, 3.0
            frame = RoundedRectangle(corner_radius=0.2, width=W, height=H).set_stroke(PURPLE, 3)
            frame.set_fill(PURPLE, 0.06)
            title = VGroup(T("full-text", 34), T("search engine", 34)).arrange(DOWN, buff=0.12)
            title.move_to([-1.0, 0.8, 0])
            n1 = T("Elasticsearch", 32, YELLOW).move_to([-1.0, -0.3, 0])
            n2 = T("OpenSearch", 32, YELLOW).move_to([-1.0, -0.95, 0])
            slot = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=1.6, height=1.25), num_dashes=24)
            slot.set_stroke(TEAL, 2).move_to([1.55, 0.55, 0])
            eng = VGroup(frame, title, n1, n2, slot)
            # final place (left), and a big centred start
            ENG_C = np.array([-3.85, 0.55, 0])
            eng.move_to(ORIGIN).scale(1.25)
            sweep_clear(self, *appear(frame, title, slot, shift=None, lag=0.2), run_time=1.6)  # early: the diagram's heading, its subject
            c.wait_until(own_word=n1)
            self.play(*appear(n1), run_time=0.8)
            c.wait_until(own_word=n2)
            self.play(*appear(n2), run_time=0.8)
            c.wait_until("words")
            shown = VGroup(frame, title, n1, n2, slot)
            tgt = VGroup(frame.copy(), title.copy(), n1.copy(), n2.copy(), slot.copy())
            tgt.scale(1 / 1.25).move_to(ENG_C)
            words = "the screenplay was not hacked or leaked".split()
            sent = VGroup(*[T(w, 36) for w in words]).arrange(RIGHT, buff=0.17, aligned_edge=DOWN)
            sent.move_to([2.7, 1.9, 0])
            self.play(*[m.animate.move_to(t).scale(1 / 1.25) for m, t in zip(shown, tgt)],
                      *during(appear(sent, shift=None), 0.35, 0.8), run_time=1.3)
            c.wait_until("stems")
            tiles = [tile(w, 32, FG, DIM) for w in words]
            r1 = VGroup(*tiles[:4]).arrange(RIGHT, buff=0.18)
            r2 = VGroup(*tiles[4:]).arrange(RIGHT, buff=0.18)
            VGroup(r1, r2).arrange(DOWN, buff=0.3).move_to([2.7, 1.55, 0])
            self.play(*during(disappear(sent), 0, 0.45), *during(appear(*tiles, shift=None, lag=0.06), 0.4, 1),
                      run_time=1.3)
            c.wait_until("so hacker")
            # stems: four forms funnel to "hack"; Hackman stays its own word
            forms = ["hacker", "hackers", "hacking", "hacked"]
            ftiles = [tile(f, 32, FG, BLUE) for f in forms]
            for i, t in enumerate(ftiles):
                t.move_to([0.6, 2.6 - i * 0.8, 0])
            hacked_old = tiles[4]
            others = [t for k, t in enumerate(tiles) if k != 4]
            self.play(*during(disappear(*others), 0, 0.4),
                      *during([hacked_old.animate.move_to(ftiles[3]).set_stroke(BLUE, 2)], 0.25, 0.75),
                      *during(appear(*ftiles[:3], shift=None, lag=0.2), 0.5, 1), run_time=1.6)
            self.remove(hacked_old)
            self.add(ftiles[3])
            stem = tile("hack", 40, GREEN, GREEN).move_to([4.9, 1.4, 0])
            arrows = [Arrow(t.get_right(), stem.get_left(), buff=0.12, stroke_width=3, color=GREEN)
                      for t in ftiles]
            c.wait_until("all match hack")
            self.play(*[GrowArrow(a) for a in arrows], *during(appear(stem, shift=None), 0.4, 1), run_time=1.6)
            hm = tile("Hackman", 32, DIM, DIM).move_to([0.6, -1.0, 0])
            hm2 = tile("hackman", 32, DIM, DIM).move_to([4.9, -1.0, 0])
            hm_a = Arrow(hm.get_right(), hm2.get_left(), buff=0.12, stroke_width=3, color=DIM)
            c.wait_until("while")
            self.play(*appear(hm, shift=None), GrowArrow(hm_a), *during(appear(hm2, shift=None), 0.4, 1),
                      run_time=1.5)
            c.wait_until("typos")
            typo = Mono("hakcer", 40, RED).move_to([ENG_C[0], -1.65, 0])
            self.play(*appear(typo), run_time=0.8)
            c.wait_until("relevance")
            fixed = Mono("hacker", 40, GREEN).move_to(typo)
            self.play(*edit(typo, fixed), run_time=1.1)
            # relevance: the five results, reordered by a GOLD bar
            scores = [(t, RELEVANCE[t]) for t, _ in RESULT]
            rows = bar_rows(scores, 2.6, 2.9, 3.6, 2.5, 0.75, size=30)
            stems = [*ftiles, stem, *arrows, hm, hm2, hm_a]
            self.play(*during(disappear(*stems), 0, 0.45), *during(appear(*rows, shift=None, lag=0.1), 0.5, 1),
                      run_time=1.4)
            ranked = bar_rows(sorted(scores, key=lambda p: -p[1]), 2.6, 2.9, 3.6, 2.5, 0.75, size=30)
            self.play(*swap(VGroup(*rows), VGroup(*ranked)), run_time=1.4)
            c.wait_until("json")
            card = VGroup(RoundedRectangle(corner_radius=0.1, width=1.45, height=1.0).set_stroke(TEAL, 3)
                          .set_fill(TEAL, 0.1), Mono("{ … }", 32, TEAL))
            card[1].move_to(card[0])
            card.move_to([slot.get_x(), 3.25, 0])
            self.play(*appear(card, shift=None), run_time=0.8)
            self.play(card.animate.move_to(slot), run_time=1.4)
            c.wait_until("duck")
            tag = VGroup(Mono("DuckDB", 30, BLUE), T("full-text search extension", 30))
            tag.arrange(RIGHT, buff=0.3)
            tframe = RoundedRectangle(corner_radius=0.12, width=tag.width + 0.5, height=0.7).set_stroke(BLUE, 2)
            tframe.move_to(tag)
            duck = VGroup(tframe, tag).move_to([2.7, -1.75, 0])
            self.play(*appear(duck), run_time=1.0)
