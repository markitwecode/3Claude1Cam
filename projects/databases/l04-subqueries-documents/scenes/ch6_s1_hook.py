"""Chapter 6, scene 1: is a movie really a tree? Clips c6.hook.1 – c6.hook.2.

Exports (import with `H = load_scene("ch6_s1_hook")`; all static, no updaters):

    H.open_card() -> VGroup, ch6's first frame (= ch5 s7's end card); geometry in STATUS.md:
        .tree     The Kid's TEAL JSON tree (kid_tree_compact()) scaled TREE_S, bottom left
        .chaplin  its actors -> 0 -> name leaf "Charles Chaplin", YELLOW
        .others   VGroup of 5 OtherMovie (.node TEAL `{ }` box, .title T 28) in a column on the right
        .links    VGroup of 5 TEAL lines, each movie node -> .chaplin's right end
        .doc      small TEAL document outline (doc_card frame + 3 TEAL rule lines), top right
        .ask      YELLOW "?" (T 72) over .doc
    H.two_way_copies() -> VGroup: ch4 s5's two_way(gold=True), re-centred at ORIGIN (cards at x -3.4 / 3.4):
        .kid .chap  the two doc cards; .a1 .a2 the ID arrows, also as .arrows = [.a1, .a2] (FG)
        .name_k .name_c .title_k .title_c .year_c .roles_k (copies GOLD: name_k, title_c, year_c);
        .pid_k .mid_c the IDs; .elem_k .elem_c; .cross. Code size 20.
    H.kid_tree_stage(stage) -> JsonTree at ORIGIN, size 26: "bare" (all containers stubs),
        "trivia" (trivia_entries open, five short fragments), "full" (also actors -> 0 -> name).
    H.KID_SHOWN  the trimmed Kid value the tree draws (11 keys; trivia as short fragments).
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
from lib.titles import title_card  # noqa: E402

J = load_scene("ch4_s2_json")
D = load_scene("ch4_s3_movie")
SCH = load_scene("ch1_s2_schema")
S5 = load_scene("ch4_s5_shape")


# ══ The Kid as a tree ══════════════════════════════════════════════════════════

KEEP = ["title", "year", "genres", "rating", "rating_votes", "actors",
        "directors", "producers", "writers", "composers", "trivia_entries"]
CREW = ["directors", "producers", "writers", "composers"]
TRIVIA = ["Due to the fact that…", "The off-screen…", "This was Sir Charles…",
          "Sir Charles Chaplin…", "The production…"]


def _shown():
    v = J.kid_value()
    d = {k: v[k] for k in KEEP}
    d["trivia_entries"] = list(TRIVIA)
    return d


KID_SHOWN = _shown()
OPENS = {"bare": [], "trivia": [("trivia_entries",)],
         "full": [("trivia_entries",), ("actors", 0, "name")]}
CHAPLIN = ("actors", 0, "name")


def kid_tree_stage(stage):
    t = J.json_tree(KID_SHOWN, open=OPENS[stage], elide_keys=True, size=26, row_gap=0.40,
                    label_pad=0.28, trunk_gap=0.15)
    for k in CREW:
        t.labels[(k,)].set_color(DIM)
        t.nodes[(k,)].set_opacity(0.4)
    return t


COMPACT_OPENS = [("title",), ("rating",), ("rating_votes",), ("actors", 0, "name"), ("trivia_entries",)]


def kid_tree_compact():
    """The Kid's tree with year, genres (-> "+2 more keys") and the crew (-> "+4 more keys") folded:
    title, rating, rating_votes, actors -> 0 -> name, trivia_entries. Built under a throwaway
    wrapper object (json_tree folds keys only below the root), which is then cut off."""
    W = J.json_tree({"r": KID_SHOWN}, open=[("r",) + p for p in COMPACT_OPENS], elide_keys=True,
                    size=26, row_gap=0.40, label_pad=0.2, trunk_gap=0.1)
    W.remove(W.nodes[()], W.edges[("r",)], W.labels[("r",)])
    t = J.JsonTree()
    t.nodes = {p[1:]: m for p, m in W.nodes.items() if p}
    t.edges = {p[1:]: m for p, m in W.edges.items() if len(p) > 1}
    t.labels = {p[1:]: m for p, m in W.labels.items() if len(p) > 1}
    t.kinds = {p[1:]: k for p, k in W.kinds.items() if p}
    t.paths = [p[1:] for p in W.paths if p]
    t.add(*W.submobjects)
    t.root = t.nodes[()]
    t.move_to(ORIGIN)
    return t


# ══ the open card ══════════════════════════════════════════════════════════════

TREE_S = 0.8
TREE_LEFT, TREE_BOTTOM = -6.6, -3.5
OTHERS = [("The Gold", "Rush"), ("City", "Lights"), ("Modern", "Times"), ("The Great", "Dictator"),
          ("Chaplin", "(1992)")]
NODE_X, TITLE_X = 4.1, 4.62
SLOT_PITCH = 0.95
DOC_AT = np.array([5.85, 2.62, 0])


def _node():
    txt = Mono("{ }", size=26, color=TEAL)
    box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36,
                           height=txt.height + 0.18).set_stroke(TEAL, 2.5).set_fill(BG, 1)
    txt.move_to(box)
    g = VGroup(box, txt).scale(0.8)
    g.box, g.text = box, txt
    return g


def other_movie(lines, y):
    g = VGroup()
    g.node = _node().move_to([NODE_X, y, 0])
    g.title = VGroup(*[T(s, 28, FG) for s in lines]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    g.title.move_to([TITLE_X + g.title.width / 2, y, 0])
    g.add(g.node, g.title)
    return g


def small_doc():
    fr = D.doc_card(width=1.4, height=1.8).frame
    ob = Mono("{", size=30, color=TEAL).move_to(fr.get_corner(UL) + np.array([0.3, -0.32, 0]))
    cb = Mono("}", size=30, color=TEAL).move_to(fr.get_corner(DR) + np.array([-0.3, 0.32, 0]))
    lines = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(TEAL, 3, opacity=0.7)
                     for w in (0.75, 0.55, 0.65)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    lines.move_to(fr).shift(RIGHT * 0.12)
    g = VGroup(fr, ob, cb, lines).move_to(DOC_AT)
    g.frame, g.braces, g.lines = fr, VGroup(ob, cb), lines
    return g


def placed_tree():
    t = kid_tree_compact()
    t.nodes[CHAPLIN].set_color(YELLOW)
    t.scale(TREE_S)
    t.move_to([TREE_LEFT + t.width / 2, TREE_BOTTOM + t.height / 2, 0])
    return t


def open_card():
    g = VGroup()
    g.tree = placed_tree()
    g.chaplin = g.tree.nodes[CHAPLIN]
    ey = g.chaplin.get_y()
    g.others = VGroup(*[other_movie(n, ey + SLOT_PITCH * (2 - i)) for i, n in enumerate(OTHERS)])
    end = g.chaplin.get_right() + RIGHT * 0.1
    g.links = VGroup(*[Line(m.node.get_left(), end).set_stroke(TEAL, 3) for m in g.others])
    g.doc = small_doc()
    g.ask = set_backstroke(T("?", 72, YELLOW), width=10).move_to(g.doc)
    g.add(g.links, g.tree, g.others, g.doc, g.ask)
    return g


# ══ ch4 s5's two-way copies (composed here from ch4 s3's doc_card) ══════════════

def two_way_copies():
    """ch4 s5's two-way copies picture (S.two_way(gold=True)), centred at ORIGIN, plus `.arrows`."""
    g = S5.two_way(gold=True)
    g.move_to(ORIGIN)
    g.arrows = [g.a1, g.a2]
    return g


# ══ scene helpers ══════════════════════════════════════════════════════════════

def _tick(leaf):
    return check_mark().scale(0.6).next_to(leaf, RIGHT, buff=0.25)


class Ch6S1Hook(NarratedScene):
    def regrow(self, old, new, rt, extra=()):
        """Old tree -> new tree layout: shared parts move, new parts fade in, gone parts fade out.
        Ends with `new` on screen as one object."""
        leave, move, arrive = [], [], []
        for p in new.paths:
            if p in old.nodes:
                if p in new.edges:
                    move.append(Transform(old.edges[p], new.edges[p]))
                if p in new.labels:
                    move.append(Transform(old.labels[p], new.labels[p]))
                if old.kinds[p] == new.kinds[p]:
                    move.append(Transform(old.nodes[p], new.nodes[p]))
                else:
                    leave.append(old.nodes[p])
                    arrive.append(new.nodes[p])
            else:
                arrive += new.branch(*p)
        for p in old.paths:
            if p not in new.nodes:
                leave += old.branch(*p)
        self.play(*during([FadeOut(m) for m in leave], 0, 0.45),
                  *during(move + list(extra), 0.15, 0.8),
                  *during([FadeIn(m) for m in arrive], 0.55, 1), run_time=rt)
        self.remove(*old.get_family(), *[m for a in arrive for m in a.get_family()])
        self.add(new)

    def construct(self):
        self.add(open_card())
        self.wait(0.7)
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        with self.say("c6.hook.1") as c:
            tc = title_card("Part 6 · Documents or tables?")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("lasttime")

            # last time: the two-way copies and ch5's verdict
            b = two_way_copies().scale(0.8).move_to([0, 0.75, 0])
            reads = T("reads: one document", 36, GREEN)
            writes = T("writes: every copy", 36, RED)
            reads.move_to([-3.4, -2.55, 0])
            writes.move_to([3.4, -2.55, 0])
            sweep_clear(self, time_span(FadeIn(b.kid), 0.6, 1.4), time_span(FadeIn(b.chap), 0.7, 1.5),
                        time_span(GrowArrow(b.arrows[0]), 1.0, 1.6),
                        time_span(GrowArrow(b.arrows[1]), 1.0, 1.6), run_time=1.6)
            self.play(*appear(reads, writes, lag=0.5), run_time=1.2)
            c.wait_until("same information")

            # the same information, two ways
            m = SCH.schema_map()
            m.scale_to_fit_width(5.6).move_to([-3.6, -0.2, 0])
            doc = D.kid_doc(19)
            doc.scale_to_fit_height(m.height).move_to([3.7, -0.2, 0])
            eq = T("=", 72, FG).move_to([0.05, -0.2, 0])
            foot = T("apart from the trivia and the order of the cast", 30, DIM).move_to([0, -3.3, 0])
            self.play(*during([FadeOut(reads), FadeOut(writes), FadeOut(b.arrows[0]),
                               FadeOut(b.arrows[1])], 0, 0.3),
                      *during([b.kid.animate.scale(0.15).move_to(m).set_opacity(0),
                               b.chap.animate.scale(0.15).move_to(doc).set_opacity(0)], 0.1, 0.55),
                      *during([FadeIn(m), FadeIn(doc)], 0.5, 1.0), run_time=1.8)
            self.remove(*b.get_family())
            self.play(*appear(eq, shift=None), run_time=0.8)
            c.wait_until(own_word=foot)
            self.play(*appear(foot), run_time=1.0)
            c.wait_until("which")

            q = T("which is better?", 48, YELLOW).move_to([0, 2.85, 0])
            self.play(*appear(q), run_time=1.0)
            c.wait_until("depends")
            dep = T("it depends on how the data is used,", 40, FG).move_to([0, 3.1, 0])
            self.play(*swap(q, dep), run_time=1.2)
            c.wait_until("shape")
            shp = T("and on the shape of the data itself", 40, FG, t2c={"shape": YELLOW})
            shp.move_to([0, 2.45, 0])
            self.play(*appear(shp), run_time=1.0)

    def clip2(self):
        with self.say("c6.hook.2") as c:
            t0 = kid_tree_stage("bare").move_to([0, -0.1, 0])
            sweep_clear(self, time_span(FadeIn(t0), 0.6, 1.5), run_time=1.5)
            c.wait_until("trivia")

            # the five trivia entries hang off their key
            t1 = kid_tree_stage("trivia")
            t1.move_to([-0.35, -0.1, 0])
            self.regrow(t0, t1, rt=min(2.0, c.until("Each one")))
            c.wait_until("Each one")
            ticks = [_tick(t1.nodes[("trivia_entries", i)]) for i in range(5)]
            self.play(*appear(*ticks, shift=None, lag=0.2), run_time=1.3)
            c.wait_until("chaplin")

            # Chaplin, on the actors branch
            t2 = kid_tree_stage("full")
            t2.move_to([-0.35, 0, 0])
            moves = [tk.animate.move_to(_tick(t2.nodes[("trivia_entries", i)]).get_center())
                     for i, tk in enumerate(ticks)]
            leaf = t2.nodes[CHAPLIN].set_color(YELLOW)
            self.regrow(t1, t2, rt=1.5, extra=moves)
            self.play(FlashAround(leaf, time_width=1.5, color=YELLOW), run_time=1.2)
            c.wait_until("others")

            # five other movies reach for the same node
            oc = open_card()
            self.play(*[FadeOut(tk) for tk in ticks], run_time=0.4)
            self.regrow(t2, oc.tree, rt=1.4)
            self.play(*appear(*oc.others, shift=None, lag=0.15), run_time=1.0)  # early: the five titles are shown, not read
            self.play(*[Create(l) for l in oc.links], run_time=1.1)
            c.wait_until("ask")

            ask = T("a tree?", 64, YELLOW).move_to([-3.4, 2.75, 0])
            self.play(*appear(ask), run_time=1.0)
            c.wait_until("checks")

            tag = T("who checks the shape?", 34, YELLOW)
            tag.next_to(oc.doc, LEFT, buff=0.4)
            self.play(*appear(oc.doc, tag, lag=0.35), run_time=1.3)
