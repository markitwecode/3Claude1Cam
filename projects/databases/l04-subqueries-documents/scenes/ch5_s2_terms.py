"""Chapter 5, scene 2: normalised and denormalised. Clips c5.terms.1 – c5.terms.4.

Opens on ch5 s1's handover_shot() (the dimmed split, "Bug or feature?"), clears the question and
re-lays the split (Chaplin's own card goes, the movie grid moves up) to free a top band for the
redundancy heading and a bottom band per side for the two terms. Clip 2 zooms on the people row,
clip 3 shows denormalised reads/writes beside the six movie cards, clip 4 flips both ways
(plays_role + title column; a movie document holding only person_ids) and ends on the loose rule.
Data verified on movies.duckdb / movies-json.duckdb: John Morris nm0606657 (1926-2018),
nm0606658 (1984-NULL), nm1898234 (NULL-NULL); The Kid's actors[1] = Edna Purviance nm0701012
"The Woman"; The Kid has 10 actors.
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

H = load_scene("ch5_s1_hook")
SCH = load_scene("ch1_s2_schema")
F = load_scene("ch5_s5_forms")

LX = H.LX
TT, NM = "tt0012349", "nm0000122"
MORRIS = [["nm0606657", "John Morris", "1926", "2018"],
          ["nm0606658", "John Morris", "1984", "NULL"],
          ["nm1898234", "John Morris", "NULL", "NULL"]]
KID_IDS_SRC = "\n".join([
    '{', '  "title": "The Kid",', '  "actors": [',
    '    {', '      "person_id": "nm0000122",', '      "name": "Charles Chaplin",',
    '      "roles": ["A Tramp"]', '    },',
    '    {', '      "person_id": "nm0701012",', '      "name": "Edna Purviance",',
    '      "roles": ["The Woman"]', '    },',
    '    /* 8 more */', '  ]', '}'])
NAME_LINES = (5, 10)
PID_LINES = (4, 9)


def person_src(pid, name):
    return "\n".join(['{', f'  "person_id": "{pid}",', f'  "name": "{name}",', '  /* … */', '}'])


def _base_all(mob):
    for p in mob.get_family():
        if not hasattr(p, "_base"):
            p._base = (p.get_fill_opacity(), p.get_stroke_opacity())
    return mob


def refit(m, a=1.0, scale=1.0, about=None, shift=ORIGIN):
    """One Transform: opacity a x built opacity, then scale about a point and shift."""
    tgt = m.copy()
    for src, dst in zip(m.get_family(), tgt.get_family()):
        bf, bs = getattr(src, "_base", (src.get_fill_opacity(), src.get_stroke_opacity()))
        dst.set_fill(opacity=bf * a, family=False)
        dst.set_stroke(opacity=bs * a, family=False)
    if scale != 1.0:
        tgt.scale(scale, about_point=about)
    tgt.shift(shift)
    return Transform(m, tgt)


def lab(text, size, color, x, y):
    t = T(text, size, color).move_to([x, y, 0])
    SCH._remember(t)
    return t


def rt(c, cue, want, frac=0.85):
    return max(0.4, min(want, frac * c.until(cue)))


class Terms(NarratedScene):
    def construct(self):
        shot = H.handover_shot()
        self.add(shot)
        sp, ps, ds, q = shot.split, shot.left, shot.right, shot.q
        self.remove(shot)
        self.add(sp.divider, sp.rel, sp.doc, ps.card, ps.one, *ps.strips, ps.arrows, ps.label,
                 ds.own, *ds.cards, ds.counter, q)
        for m in [sp, ps, ds]:
            _base_all(m)
        self.sp, self.ps, self.ds, self.q = sp, ps, ds, q
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── clip 1: redundancy, normalised, denormalised ──────────────────────────
    def clip1(self):
        sp, ps, ds, q = self.sp, self.ps, self.ds, self.q
        with self.say("c5.terms.1", gap=1.0) as c:
            left = [ps.card, ps.one, *ps.strips, ps.arrows]
            about = np.array([LX, 2.85, 0])
            new_div = Line([H.DIV_X, 2.45, 0], [H.DIV_X, -3.75, 0]).set_stroke(DIM, 2)
            new_div._base = (new_div.get_fill_opacity(), new_div.get_stroke_opacity())
            self.play(*during(disappear(q, ds.own, ps.label), 0, 0.45),  # early: s1's counter, restored from dim, not new
                      *during([refit(m, 1, 0.88, about, DOWN * 0.45) for m in left]
                              + [refit(cd, 1, shift=UP * 1.3) for cd in ds.cards]
                              + [refit(ds.counter, 1, shift=UP * 1.2),
                                 refit(sp.rel), refit(sp.doc), Transform(sp.divider, new_div)],
                              0.2, 1.0), run_time=1.8)
            c.wait_until("several places")
            self.play(*[FlashAround(cd.tags, color=GOLD, time_width=1.5) for cd in ds.cards],
                      run_time=1.5)
            head = T("Redundancy: the same fact stored in several places", 32, YELLOW).move_to([0, 2.9, 0])
            c.wait_until(own_word=head)
            self.play(*appear(head), run_time=1.0)
            self.head = head

            # normalised (spotlight left)
            c.wait_until("normalised")
            self.play(*[H.dim(cd, 0.35) for cd in ds.cards], H.dim(ds.counter, 0.35),
                      FlashAround(ps.card.values["name"], color=GOLD, time_width=1.5),
                      run_time=rt(c, "every fact", 1.5))
            n1 = lab("Normalised:", 34, BLUE, LX + 0.25, -2.5)
            n2 = lab("every fact in exactly one place", 28, BLUE, LX + 0.25, -2.98)
            n3 = lab("refers to it by its key", 28, DIM, LX + 0.25, -3.42)
            c.wait_until(own_word=n2)
            self.play(*appear(n2), run_time=1.0)
            c.wait_until("is called normalised")
            self.play(*appear(n1), run_time=1.0)
            c.wait_until("refer")
            flashes = [VShowPassingFlash(Line(a.get_start(), a.get_end()).set_stroke(YELLOW, 4),
                                         time_width=0.6) for a in ps.arrows]
            self.play(*flashes, run_time=1.4)
            c.wait_until(own_word=n3)
            self.play(*appear(n3), run_time=1.0)

            # denormalised (spotlight right)
            c.wait_until("denorm")
            self.play(*[H.dim(cd, 1) for cd in ds.cards], H.dim(ds.counter, 1),
                      *[H.dim(m, 0.35) for m in left + [n1, n2, n3]], run_time=1.4)
            d1 = lab("Denormalised:", 34, TEAL, 3.45, -2.5)
            d2 = lab("copies stored where reads need them", 28, TEAL, 3.45, -2.98)
            c.wait_until(own_word=d2)
            self.play(*swap(ds.counter, d2), run_time=1.2)
            c.wait_until("is called denormalised")
            self.play(*appear(d1), run_time=1.0)

            # ours
            c.wait_until("ours")
            our_rel = lab("our relational schema", 36, BLUE, -3.4, 3.5)
            our_doc = lab("our documents", 36, TEAL, 3.45, 3.5)
            self.play(*[H.dim(m, 1) for m in left + [n1, n2, n3]], run_time=0.8)
            c.wait_until(own_word=our_rel)
            self.play(*swap(sp.rel, our_rel), run_time=rt(c, "our documents", 1.2))
            c.wait_until(own_word=our_doc)
            self.play(*swap(sp.doc, our_doc), run_time=1.2)
            c.wait_until()

    # ── clip 2: why an ID ─────────────────────────────────────────────────────
    def clip2(self):
        ps = self.ps
        card = ps.card
        vals = card.values
        with self.say("c5.terms.2", gap=1.4) as c:
            sweep_clear(self, card.animate.scale(1.6).move_to([0, 0.2, 0]), keep=[card],
                        run_time=1.8)
            ul = underline(vals["person_id"], YELLOW, buff=0.05)
            c.wait_until("by an ID")
            self.play(GrowFromEdge(ul, LEFT), *recolor(vals["person_id"], YELLOW), run_time=1.0)
            settle(self, card, add=[ul])

            c.wait_until("change")
            name = vals["name"]
            new = T("new name?", 32, DIM, slant=ITALIC)
            new.move_to(name).align_to(name, LEFT)
            self.play(*during([name.animate.set_opacity(0)], 0, 0.45),
                      *during(appear(new, shift=None), 0.5, 1.0), run_time=1.2)
            c.wait_until("never needs")
            self.play(*during(disappear(new), 0, 0.45),
                      *during([name.animate.set_opacity(1)], 0.5, 1.0),
                      FlashAround(vals["person_id"], color=YELLOW, time_width=1.5), run_time=1.5)
            ptr = label_pointer("just letters and digits", vals["person_id"], direction=UP,
                                color=DIM, size=30, length=0.5)
            c.wait_until(own_word=ptr[0])
            self.play(*appear(ptr), run_time=1.0)

            # two people can share a name
            cols = SCH.SCHEMA["people"][0]
            colors = [[SCH._kid_color(cl, v) for cl, v in zip(cols, r)] for r in MORRIS]
            tab = SCH.RowTable("people", cols, MORRIS, colors, size=28, pitch=0.58)
            tab.move_to([0, -1.0, 0])
            c.wait_until("shared")
            self.play(*during(disappear(ptr), 0, 0.3),
                      during([card.animate.scale(0.6).move_to([0, 2.55, 0])], 0.25, 0.7)[0],
                      *during(appear(tab.label, tab.frame, tab.head, shift=None, lag=0.1), 0.65, 1.0),
                      run_time=2.2)
            c.wait_until("three different")
            self.play(*appear(*tab.rows, lag=0.5), run_time=1.6)
            c.wait_until("John Morris")
            self.play(*[FlashAround(tab.cell(i, 0), color=GOLD, time_width=1.5) for i in range(3)],
                      *[recolor(tab.cell(i, 0), GOLD)[0] for i in range(3)], run_time=1.4)

            # the price: joins
            c.wait_until("join")
            strip = SCH.RowTable("has_position", ["movie_id", "person_id", "position"],
                                 [[TT, NM, "actor"]], [[DIM, DIM, YELLOW]], size=34, pitch=0.7)
            strip.move_to(ORIGIN)
            SCH.place(strip, top=3.45)
            # the join stacks vertically: has_position on top, ⋈, the people card below (1.5x)
            k = 1.5
            card_h = card.height * k
            card_to = np.array([0, strip.get_bottom()[1] - 1.05 - card_h / 2, 0])
            self.play(*during(disappear(tab.label, tab.frame, tab.head, *tab.rows), 0, 0.45),
                      during([card.animate.scale(k).move_to(card_to)], 0.35, 0.85)[0],
                      *during(appear(strip, shift=None), 0.5, 1.0), run_time=1.8)
            mid = (strip.get_bottom()[1] + card.get_top()[1]) / 2
            bow = MathTex(r"\bowtie", font_size=80, color=YELLOW).move_to([0, mid, 0])
            cap = T("to show a name: a join", 36, YELLOW).move_to([0, card.get_bottom()[1] - 0.65, 0])
            c.wait_until(own_word=cap)
            self.play(GrowFromCenter(bow), *appear(cap), run_time=1.0)
            c.wait_until("look up")
            sid = strip.cell(0, 1)
            self.play(*recolor(sid, YELLOW), FlashAround(sid, color=YELLOW, time_width=1.5),
                      FlashAround(vals["person_id"], color=YELLOW, time_width=1.5),
                      run_time=rt(c, None, 1.4, 1.0))
            c.wait_until()

    # ── clip 3: denormalised turns it around ──────────────────────────────────
    def clip3(self):
        with self.say("c5.terms.3", gap=1.4) as c:
            head = T("Denormalised", 48, TEAL).move_to([0, 3.2, 0])
            cards = [H.movie_card(t, n).move_to([x, y, 0]) for (t, n), (x, y) in zip(H.MOVIES, H.GRID)]
            grid = VGroup(*cards).scale(0.8).move_to([-3.95, -0.4, 0])
            sweep_clear(self, *appear(head, *cards, lag=0.06), run_time=2.0)
            x0 = -0.9
            r1 = T("Reads: faster and simpler", 34, GREEN)
            r2 = T("fewer joins", 30, DIM)
            w1 = T("Writes: slower and more complex", 34, RED)
            w2 = T("every copy updated", 30, DIM)
            x1 = T("copies may disagree", 34, RED)
            for m, y in [(r1, 1.6), (r2, 1.1), (w1, 0.0), (w2, -0.5), (x1, -1.6)]:
                m.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
            c.wait_until(own_word=r1)
            self.play(*appear(r1), run_time=1.0)
            c.wait_until(own_word=r2)
            self.play(*appear(r2), run_time=1.0)
            c.wait_until(own_word=w1)
            self.play(*appear(w1), run_time=1.0)
            c.wait_until(own_word=w2)
            self.play(*appear(w2), *[FlashAround(cd.tags, color=GOLD, time_width=1.5) for cd in cards],
                      run_time=1.5)
            c.wait_until("one copy")
            bad = cards[2].tags[2]
            self.play(*recolor(bad, RED), FlashAround(bad, color=RED, time_width=1.5), run_time=1.2)
            c.wait_until(own_word=x1)
            self.play(*appear(x1), run_time=1.0)
            c.wait_until()

    # ── clip 4: both can go either way ────────────────────────────────────────
    def clip4(self):
        with self.say("c5.terms.4", gap=3.0) as c:
            card = F.title_card(size=20, pitch=0.4)
            card.move_to([0, 0.3, 0])
            base, col = card.base, card.title_col
            sweep_clear(self, *appear(base, shift=None), run_time=2.2)
            c.wait_until("title column")
            self.play(GrowFromEdge(col.frame, LEFT), *appear(col.head), run_time=1.2)
            c.wait_until("twelve")
            self.play(*appear(*col.cells, shift=None, lag=0.1), run_time=1.8)
            tag1 = T("denormalised, relational", 34, FG,
                     t2c={"denormalised": TEAL, "relational": BLUE}).move_to([0, -3.35, 0])
            c.wait_until(own_word=tag1)
            self.play(*appear(tag1), run_time=1.0)

            # the other way: documents holding only IDs
            c.wait_until("ids_only")
            doc = H._card(KID_IDS_SRC, 20, [-3.4, 0.25, 0])
            sweep_clear(self, *appear(doc.frame, doc.code, shift=None), run_time=1.8)
            code = doc.code
            c.wait_until("only their")
            strikes = []
            for i in NAME_LINES:
                ln = code.line(i)
                strikes.append(Line(ln.get_left() + LEFT * 0.08, ln.get_right() + RIGHT * 0.08)
                               .set_stroke(RED, 3))
            dims = [g.animate.set_opacity(0.35) for i in NAME_LINES for g in code.line(i)]
            self.play(*dims, *[GrowFromEdge(s, LEFT) for s in strikes],
                      *[FlashAround(code.find(f'"{p}"'), color=YELLOW, time_width=1.5)
                        for p in (NM, "nm0701012")], run_time=1.6)
            p1 = H._card(person_src(NM, "Charles Chaplin"), 20, [0, 0, 0], yellow=['"Charles Chaplin"'])
            p2 = H._card(person_src("nm0701012", "Edna Purviance"), 20, [0, 0, 0],
                         yellow=['"Edna Purviance"'])
            for p, y in [(p1, 1.75), (p2, -1.35)]:
                p.move_to([6.5 - p.width / 2, y, 0])
            arrows = []
            for i, p in zip(PID_LINES, (p1, p2)):
                y0 = code.line(i).get_y()
                arrows.append(Arrow([doc.frame.get_right()[0] + 0.05, y0, 0],
                                    [p.frame.get_left()[0], p.code.line(1).get_y(), 0],
                                    buff=0.04, stroke_width=3, color=FG, tip_length=0.18))
            c.wait_until("each name")
            self.play(*appear(p1, p2, shift=None, lag=0.3), *[GrowArrow(a) for a in arrows],
                      run_time=1.6)
            tag2 = T("normalised, documents", 34, FG,
                     t2c={"normalised": BLUE, "documents": TEAL}).move_to([0, -3.4, 0])
            c.wait_until(own_word=tag2)
            self.play(*appear(tag2), run_time=1.0)
            mid = (doc.frame.get_right()[0] + p1.frame.get_left()[0]) / 2
            bow = MathTex(r"\bowtie", font_size=72, color=YELLOW).move_to([mid, 0.45, 0])
            c.wait_until("you need a join")
            self.play(GrowFromCenter(bow), run_time=1.0)

            # the loose rule
            c.wait_until("rule")
            l1 = T("Relational DBs: often normalised, can be denormalised", 34, BLUE).move_to([0, 0.55, 0])
            l2 = T("Document DBs: often denormalised, can be normalised", 34, TEAL).move_to([0, -0.55, 0])
            sweep_clear(self, run_time=1.2)
            c.wait_until(own_word=l1)
            self.play(*appear(l1), run_time=1.0)
            c.wait_until(own_word=l2)
            self.play(*appear(l2), run_time=1.0)
            c.wait_until()
