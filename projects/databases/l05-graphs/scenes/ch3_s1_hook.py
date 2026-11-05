"""Chapter 3, scene 1: Hook. From ch2's co-star card to the title, a 'last time' strip, the
co-star question, and what SQL needs for it (4 tables, 3 joins). Clips c3.hook.1 – c3.hook.2.

Exports: open_card() (ch2 s7 ends on it), handover_shot() (ch3 s2 opens on it), sql_diagram().
"""
# style: 2
# handover: next
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

R = 0.95                     # vertex circle radius (ch2's look)
MAX_W = 12.6                 # widest a full-width code line may be
CARD_PATTERN = "(p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)"
SPIELBERG = "(p:Person {name: 'Steven Spielberg'})\n  -[:DIRECTED]-> (m:Movie)"
QUESTION = "Which pairs of actors have appeared together most often?"
HANDOVER_DIM = 0.35          # opacity of the handed-over SQL diagram
ROW_Y = 0.45                 # centre line of the four table boxes


# ---------------------------------------------------------------- shared drawing
def vertex(text, color, at, size=36):
    circ = Circle(radius=R, color=color, stroke_width=4).set_fill(color, 0.12).move_to(at)
    lab = T(text, size=size, slant=ITALIC).move_to(circ)
    v = VGroup(circ, lab)
    v.circ, v.lab = circ, lab
    return v


def edge(a, b, text, size=28):
    """Arrow from vertex a to vertex b, its type in caps along it (on the upper side)."""
    s, e = a.circ.get_center(), b.circ.get_center()
    arr = Arrow(s, e, buff=R + 0.06, stroke_width=4, color=FG, max_tip_length_to_length_ratio=0.12)
    d = (e - s) / np.linalg.norm(e - s)
    ang = np.arctan2(d[1], d[0])
    if ang > PI / 2:
        ang -= PI
    if ang < -PI / 2:
        ang += PI
    nrm = np.array([-d[1], d[0], 0])
    if nrm[1] < 0:
        nrm = -nrm
    lab = set_backstroke(T(text, size=size).rotate(ang))
    lab.move_to(arr.get_center() + 0.32 * nrm)
    return arr, lab


def fit(code, w=MAX_W):
    if code.width > w:
        code.scale_to_fit_width(w)
    return code


def open_card():
    """ch3's first frame = ch2's recap end card (c2.recap.2). Static, no updaters.
    Parts: .p1 .m .p2 (vertex groups with .circ .lab), .arrows, .types, .caption, .pattern, .most."""
    p1 = vertex("p1", PINK, [-4.0, 1.4, 0])
    m = vertex("m", BLUE, [0.0, -0.5, 0])
    p2 = vertex("p2", PINK, [4.0, 1.4, 0])
    a1, l1 = edge(p1, m, "ACTED_IN")
    a2, l2 = edge(p2, m, "ACTED_IN")
    caption = T("co-stars", size=44).move_to([0, 2.45, 0])
    pattern = fit(Code(CARD_PATTERN, size=28)).move_to([0, -2.3, 0]).set_color(DIM)
    most = T("most often?", size=40, color=GOLD).move_to([0, -3.25, 0])
    g = VGroup(p1, m, p2, a1, a2, l1, l2, caption, pattern, most)
    g.p1, g.m, g.p2 = p1, m, p2
    g.arrows, g.types = [a1, a2], [l1, l2]
    g.caption, g.pattern, g.most = caption, pattern, most
    return g


def table_box(name, alias):
    head = Mono(name, size=28, color=BLUE)
    body = Mono(f"AS {alias}", size=28)
    w = max(head.width, body.width) + 0.5
    hrect = Rectangle(width=w, height=0.6, stroke_color=BLUE, stroke_width=3).set_fill(BLUE, 0.18)
    brect = Rectangle(width=w, height=0.7, stroke_color=BLUE, stroke_width=3)
    brect.next_to(hrect, DOWN, buff=0)
    head.move_to(hrect)
    body.move_to(brect)
    b = VGroup(hrect, brect, head, body)
    b.hrect, b.brect, b.head, b.body = hrect, brect, head, body
    return b


def sql_diagram():
    """What SQL needs for co-stars: people AS p1, has_position AS h1, has_position AS h2,
    people AS p2 in a row; three join conditions; the actor filters; the GOLD tally.
    Parts: .p1 .h1 .h2 .p2 (boxes: .hrect .brect .head .body), .boxes, .links (3 TEAL Lines),
    .leaders (3 VGroups: dot + DIM line), .link_labels (3 sql Code), .same_tag, .notes (2 Code),
    .tally."""
    p1, h1 = table_box("people", "p1"), table_box("has_position", "h1")
    h2, p2 = table_box("has_position", "h2"), table_box("people", "p2")
    boxes = [p1, h1, h2, p2]
    x = 0.0
    for b, gap in zip(boxes, (0.42, 1.8, 0.42, 0.0)):
        b.move_to([x + b.width / 2, ROW_Y, 0])
        x += b.width + gap
    row = VGroup(*boxes)
    row.shift(-row.get_center()[0] * RIGHT)
    links = [Line(boxes[i].get_right(), boxes[i + 1].get_left(), color=TEAL, stroke_width=4)
             for i in range(3)]
    srcs = ["h1.person_id = p1.person_id", "h2.movie_id = h1.movie_id", "h2.person_id = p2.person_id"]
    labels = [Code(s, size=28, lang="sql") for s in srcs]
    labels[0].move_to([0, 2.4, 0]).align_to(row, LEFT)
    labels[2].move_to([0, 1.8, 0]).align_to(row, RIGHT)
    notes = [Code("position = 'actor'", size=28, lang="sql").next_to(b, DOWN, buff=0.22) for b in (h1, h2)]
    labels[1].move_to([0, -1.55, 0])
    same = T("same movie", size=30, color=YELLOW).next_to(labels[1], RIGHT, buff=0.35)
    leaders = []
    for lk, lab in zip(links, labels):
        mid = lk.get_center()
        end = lab.get_bottom() + 0.1 * DOWN if lab.get_y() > ROW_Y else lab.get_top() + 0.1 * UP
        end = np.array([mid[0], end[1], 0])
        leaders.append(VGroup(Dot(mid, radius=0.06, color=TEAL),
                              Line(mid, end, color=DIM, stroke_width=2)))
    tally = T("4 tables · 3 joins", size=36, color=GOLD).move_to([-3.3, -2.85, 0])
    g = VGroup(*boxes, *links, *leaders, *labels, same, *notes, tally)
    g.p1, g.h1, g.h2, g.p2, g.boxes = p1, h1, h2, p2, boxes
    g.links, g.leaders, g.link_labels, g.same_tag, g.notes, g.tally = links, leaders, labels, same, notes, tally
    return g


def dim(mob, f=HANDOVER_DIM):
    """Static dim: every part's fill and stroke opacity times f."""
    for sm in mob.get_family():
        if sm.has_points():
            sm.set_fill(opacity=sm.get_fill_opacity() * f)
            sm.set_stroke(opacity=sm.get_stroke_opacity() * f)
    return mob


def handover_shot():
    """ch3 s2's first frame: the SQL diagram dimmed to 0.35, nothing else on screen."""
    return dim(sql_diagram())


def sketch_v():
    """A faint pencil V, stopped half-way: p1, a stroke toward m, half of m."""
    a, m = np.array([1.9, -2.45, 0]), np.array([3.5, -3.3, 0])
    c1 = Circle(radius=0.32).move_to(a)
    d = (m - a) / np.linalg.norm(m - a)
    ln = Line(a + 0.32 * d, m - 0.32 * d)
    arc = Arc(radius=0.32, start_angle=PI * 0.85, angle=-PI * 1.1, arc_center=m)
    g = VGroup(c1, ln, arc).set_stroke(FG, 2.5, opacity=0.55)
    return g


class Hook(NarratedScene):
    def construct(self):
        card = open_card()
        self.add(card)
        self.wait(0.7)
        self.clip1(card)
        self.clip2()
        self.play(*disappear(self.header, self.qmark), run_time=1.0)
        self.wait(1.0)

    # ------------------------------------------------------------------ clip 1
    def clip1(self, card):
        tc = title_card("Part 3 · Co-stars: bigger patterns and counting")
        with self.say("c3.hook.1") as c:
            self.play(*during(FadeOut(card), 0, 0.35),
                      *during([FadeIn(tc.title, shift=0.3 * DOWN), GrowFromCenter(tc.rule)], 0.35, 1),
                      run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.2)  # early: title card
            c.wait_until("last")

            last = T("Last time", size=32, color=DIM).move_to(3.1 * UP)
            sweep_clear(self, *appear(last), run_time=1.6)
            c.wait_until("round brackets")
            circ = Circle(radius=0.45, color=BLUE, stroke_width=4).set_fill(BLUE, 0.12)
            mm = Code("(m:Movie)", size=40)
            vrow = VGroup(circ, mm).arrange(RIGHT, buff=0.5).move_to(1.75 * UP)
            self.play(*appear(circ, mm, lag=0.3), run_time=1.3)
            c.wait_until("an arrow")
            pat = Code(SPIELBERG, size=34).move_to(0.1 * UP)
            self.play(*appear(pat), run_time=1.2)
            arrow_g = pat.find("-[:DIRECTED]->")
            box = token_box(arrow_g, pat.line(1), height=0.62)
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("each edge")
            jb = [VGroup(RoundedRectangle(corner_radius=0.1, width=Mono(n, size=28).width + 0.4, height=0.65,
                                          stroke_color=FG, stroke_width=2.5), Mono(n, size=28))
                  for n in ("people", "has_position")]
            for b in jb:
                b[1].move_to(b[0])
            jrow = VGroup(*jb).arrange(RIGHT, buff=1.0).move_to(1.75 * DOWN)
            jline = Line(jb[0].get_right(), jb[1].get_left(), color=TEAL, stroke_width=4)
            tie = DashedLine(box.get_bottom(), jrow.get_top() + 0.08 * UP, color=YELLOW, stroke_width=2.5)
            self.play(Create(tie), *appear(jb[0], jb[1], lag=0.3), run_time=1.4)
            self.play(Create(jline), run_time=0.8)
            note = T("an edge ≈ a join with has_position", size=30, color=DIM).move_to(2.95 * DOWN)
            c.wait_until(own_word=note, cue="join")
            self.play(*appear(note), run_time=1.0)

            q = T("Which pairs of actors have appeared\ntogether most often?", size=44, color=YELLOW,
                  line_spacing=1.1).move_to(0.2 * UP)
            c.wait_until(own_word=q)
            sweep_clear(self, *appear(q), run_time=1.8)
        self.q = q

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        q = self.q
        header = T(QUESTION, size=30, color=YELLOW).move_to(3.45 * UP)
        d = sql_diagram()
        with self.say("c3.hook.2") as c:
            c.wait_until("hp")
            self.play(*during(FadeOut(q), 0, 0.4), *during(FadeIn(header, shift=0.2 * UP), 0.45, 1),
                      *during(appear(d.h1), 0.45, 1), run_time=1.8)
            c.wait_until("two of those rows")
            self.play(*appear(d.h2, *d.notes, lag=0.35), run_time=1.6)
            c.wait_until("same")
            self.play(GrowFromCenter(d.links[1]), FadeIn(d.leaders[1]), run_time=1.0)
            self.play(*appear(d.link_labels[1], d.same_tag, lag=0.4), run_time=1.4)
            c.wait_until("people")
            self.play(*appear(d.p1, d.p2, lag=0.3), run_time=1.4)
            c.wait_until("two names")
            self.play(*[GrowFromCenter(d.links[i]) for i in (0, 2)],
                      *[FadeIn(d.leaders[i]) for i in (0, 2)], run_time=1.0)
            self.play(*appear(d.link_labels[0], d.link_labels[2], lag=0.4), run_time=1.4)
            settle(self, d, drop=[d.tally])
            c.wait_until("four")
            self.play(*appear(d.tally), *flash(d.boxes, color=GOLD, run_time=1.6, time_width=1.5),
                      run_time=1.6)
            self.play(*flash(d.links, color=TEAL, run_time=1.4, time_width=1.5), run_time=1.4)
            settle(self, d, add=[d.tally])
            c.wait_until("draw")
            sk = sketch_v()
            self.play(Create(sk, lag_ratio=1.0), run_time=min(3.0, c.until("shape") - 0.3), rate_func=linear)
            c.wait_until("shape")
            qmark = T("?", size=80, color=YELLOW).move_to(sk)
            d.generate_target()
            dim(d.target)
            self.play(*swap(sk, qmark), MoveToTarget(d), run_time=1.6)
        self.header, self.qmark = header, qmark
