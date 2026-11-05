"""Chapter 2, scene 3: what a match is (the stencil slid over the graph). Clips c2.match.1 – c2.match.4.

Exports, for ch3 s3, ch6 s2/s4 and ch2's recap (all static, no updaters, self-contained):
- movie_patch() -> MoviePatch: the placement picture. Five BLUE Movie circles in a column at x = 0.8
  (The Kid, The Gold Rush, Jaws, Hook, The Matrix; titles to their right) and five PINK Person
  circles in a column at x = -4.5 (Jackie Coogan, Charles Chaplin, Roy Scheider, Steven Spielberg,
  Keanu Reeves; two-line names to their left), with DIM arrows person -> movie (real edges of
  movies.tvdb: ACTED_IN / DIRECTED). Spans about x -6.5 .. 4.1, y -3.4 .. 3.3 at scale 1.
  Parts: .movies / .persons (lists of Vertex: .circle, .name, .title), .arrows (list),
  .vertex(title) -> that Vertex, .people() -> persons + arrows (to dim them together).
- stencil(label="Movie", name="m") -> Stencil: the YELLOW stroke-only hole (radius 0.52) with the
  Mono tags "m" (upper-left rim) and "Movie" (above, a little right). .ring .name_tag .label_tag;
  .centre() is the ring's centre; .at(point) returns the stencil moved so the ring sits on point.
  Sized to sit on a movie_patch() circle (radius 0.4) whose neighbours are >= 1.4 apart.
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

V_R = 0.40          # vertex circle radius
HOLE_R = 0.52       # stencil hole radius
MOVIE_X, PERSON_X = 0.65, -4.5
MOVIES = [("The Kid", 2.55), ("The Gold Rush", 1.12), ("Jaws", -0.31), ("Hook", -1.74),
          ("The Matrix", -3.17)]
PERSONS = [("Jackie Coogan", 2.9), ("Charles Chaplin", 1.3), ("Roy Scheider", 0.0),
           ("Steven Spielberg", -1.45), ("Keanu Reeves", -3.0)]
EDGES = [("Jackie Coogan", "The Kid"), ("Charles Chaplin", "The Kid"),
         ("Charles Chaplin", "The Gold Rush"), ("Roy Scheider", "Jaws"),
         ("Steven Spielberg", "Jaws"), ("Steven Spielberg", "Hook"), ("Keanu Reeves", "The Matrix")]


class Vertex(VGroup):
    """A graph vertex: a tinted circle in its label's colour plus its name (28, FG)."""

    def __init__(self, title, color, point, name_side):
        super().__init__()
        self.title = title
        self.circle = Circle(radius=V_R).set_stroke(color, 4).set_fill(
            interpolate_color(ManimColor(BG), ManimColor(color), 0.22), 1).move_to(point)
        if name_side is RIGHT:
            self.name = T(title, 28)
            self.name.next_to(self.circle, RIGHT, buff=0.57)
        else:
            self.name = T(title.replace(" ", "\n"), 28, line_spacing=0.8)
            self.name.next_to(self.circle, LEFT, buff=0.15)
        self.add(self.circle, self.name)


class MoviePatch(VGroup):
    """The placement picture (see module docstring)."""

    def __init__(self):
        super().__init__()
        self.movies = [Vertex(t, BLUE, [MOVIE_X, y, 0], RIGHT) for t, y in MOVIES]
        self.persons = [Vertex(n, PINK, [PERSON_X, y, 0], LEFT) for n, y in PERSONS]
        self.arrows = []
        for p, m in EDGES:
            a, b = self.vertex(p).circle.get_center(), self.vertex(m).circle.get_center()
            d = (b - a) / np.linalg.norm(b - a)
            self.arrows.append(Arrow(a + d * V_R, b - d * V_R, buff=0, stroke_width=3, color=DIM,
                                     tip_length=0.18, max_tip_length_to_length_ratio=0.1))
        self.add(*self.arrows, *self.persons, *self.movies)

    def vertex(self, title):
        return next(v for v in self.movies + self.persons if v.title == title)

    def people(self):
        return self.persons + self.arrows


def movie_patch():
    return MoviePatch()


class Stencil(VGroup):
    """The pattern stencil (see module docstring)."""

    def __init__(self, label="Movie", name="m"):
        super().__init__()
        self.ring = Circle(radius=HOLE_R).set_stroke(YELLOW, 5).set_fill(opacity=0)
        self.name_tag = set_backstroke(Mono(name, 30, YELLOW)).move_to([-0.66, 0.5, 0])
        self.add(self.ring, self.name_tag)
        self.label_tag = None
        if label:
            self.label_tag = set_backstroke(Mono(label, 30, YELLOW))
            self.label_tag.move_to([0.27, 0.74, 0])
            self.add(self.label_tag)

    def centre(self):
        return self.ring.get_center()

    def at(self, point):
        return self.shift(np.array(point) - self.centre())


def stencil(label="Movie", name="m"):
    return Stencil(label, name)


def ring_to(st, point):
    return st.animate.shift(np.array(point) - st.centre())


# right column (results)
COL_X, COL_L = 5.45, 4.55
ROW_Y = [1.95, 1.4, 0.85]


def row_text(title, i):
    return T(title, 28).move_to([0, ROW_Y[i], 0]).align_to([COL_L, 0, 0], LEFT)


def count_text(s):
    return T(s, 56, GOLD).move_to([COL_X, -1.0, 0])


def cell(v, color=FG, w=0.85):
    box = Rectangle(width=w, height=0.62).set_stroke(DIM, 2)
    return VGroup(box, Mono(v, 30, color).move_to(box))


def table(rows, x, y0=1.0):
    out = VGroup()
    for i, r in enumerate(rows):
        row = VGroup(*[cell(v, GOLD if j == 0 else FG) for j, v in enumerate(r)]).arrange(RIGHT, buff=0)
        row.move_to([x, y0 - 0.62 * i, 0])
        out.add(row)
    return out


class Match(NarratedScene):
    def construct(self):
        patch = movie_patch()
        kid = patch.vertex("The Kid")

        # ---------------- c2.match.1 ----------------
        with self.say("c2.match.1") as c:
            code = Code("(m:Movie)", size=56).move_to(UP * 1.7)
            self.play(*appear(code), run_time=1.0)
            c.wait_until("stencil")
            st = stencil().scale(1.6)
            st.at([0, -1.3, 0])
            # the code itself lifts down and becomes the stencil
            self.play(*during([code.animate.shift(st.centre() - code.get_center()).set_opacity(0)], 0, 0.55),
                      *during([FadeIn(st, scale=0.8)], 0.5, 1.0),
                      run_time=min(1.6, c.until("named holes")))
            self.remove(code)
            c.wait_until("named holes")
            self.play(*flash([st.name_tag, st.label_tag]), run_time=min(1.0, c.until("place")))
            st.generate_target()
            st.target.scale(1 / 1.6)
            st.target.shift(np.array([-2.0, 0.6, 0]) - st.target.ring.get_center())
            self.play(*during([MoveToTarget(st)], 0, 0.6),
                      *during(appear(patch, shift=None), 0.45, 1.0),  # early: the graph is shown whole
                      run_time=1.6)
            pts = [[-2.0, 0.6], [-2.7, 2.3], [-1.3, 1.4], [-2.6, -0.6], [-1.4, -2.5], [-2.5, -1.6],
                   [-1.5, 1.6]]
            off = st.get_center() - st.centre()
            path = VMobject().set_points_smoothly([np.array([x, y, 0]) + off for x, y in pts])
            self.play(MoveAlongPath(st, path), rate_func=linear,
                      run_time=max(1.0, c.until("fits") - 0.2))
            c.wait_until("fits")
            self.play(ring_to(st, kid.circle.get_center()), run_time=min(1.2, c.until("labels agree")))
            c.wait_until("labels agree")
            self.play(*flash([st.label_tag, kid.circle]), run_time=1.2)

        # ---------------- c2.match.2 ----------------
        with self.say("c2.match.2") as c:
            header = Mono("m.title", 30, t2c={"m": YELLOW}).move_to([COL_X, 2.7, 0])
            rule = Line([COL_L - 0.1, 2.42, 0], [6.6, 2.42, 0]).set_stroke(DIM, 2)
            divider = Line([4.38, 3.2, 0], [4.38, -3.2, 0]).set_stroke(DIM, 2, opacity=0.5)
            rows_lbl = T("rows", 30, DIM).move_to([COL_X, -1.75, 0])
            cnt = count_text("1")
            r1 = row_text("The Kid", 0)
            self.play(*appear(header, rule, divider, shift=None),
                      *during(fly(kid.name, r1), 0.3, 1.0), run_time=1.6)
            self.play(*appear(cnt, rows_lbl, shift=None), run_time=1.0)  # early: counter beside its first row
            c.wait_until("becomes one row")
            gr = patch.vertex("Jaws")
            r2 = row_text("Jaws", 1)
            c2 = count_text("2")
            self.play(*during([ring_to(st, gr.circle.get_center())], 0, 0.45),
                      *during(fly(gr.name, r2), 0.45, 1.0),
                      *during(swap(cnt, c2), 0.5, 1.0), run_time=min(1.6, c.until("bind")))
            cnt = c2
            c.wait_until("bind")
            bind = Arrow([COL_L - 0.15, ROW_Y[0], 0],
                         kid.circle.get_center() + 0.42 * (RIGHT * 0.8 + DOWN * 0.6),
                         buff=0, stroke_width=4, color=YELLOW, tip_length=0.22,
                         max_tip_length_to_length_ratio=0.1)
            self.play(GrowArrow(bind), *recolor([r1], YELLOW), run_time=1.5)
            c.wait_until("em dot title")
            self.play(*flash([header, kid.name]), run_time=1.2)
            c.wait_until("count")
            jaws = patch.vertex("Hook")
            r3 = row_text("Hook", 2)
            c3 = count_text("3")
            self.play(FadeOut(bind), r1.animate.set_color(FG),
                      *during([ring_to(st, jaws.circle.get_center())], 0, 0.45),
                      *during(fly(jaws.name, r3), 0.45, 1.0), run_time=1.2)
            self.play(*swap(cnt, c3), run_time=0.6)
            cnt = c3
            dots = T("⋮", 36, DIM).move_to([COL_X, 0.35, 0])
            hook, matrix = patch.vertex("The Gold Rush"), patch.vertex("The Matrix")
            self.play(Succession(ring_to(st, matrix.circle.get_center()),
                                 ring_to(st, hook.circle.get_center())),
                      *during(appear(dots, shift=None), 0.5, 1.0), run_time=1.2)
            big = count_text("2,935")
            c.wait_until("nine hundred")
            self.play(*swap(cnt, big), run_time=min(1.2, c.until("once per movie")))
            cnt = big
            self.play(*flash([cnt], color=GOLD), run_time=1.2)
            c.wait_until("person")
            spiel = patch.vertex("Steven Spielberg")
            self.play(ring_to(st, spiel.circle.get_center()), run_time=1.2)
            ptag = set_backstroke(Mono("Person", 30, PINK)).move_to(
                spiel.circle.get_center() + np.array([0.95, -0.55, 0]))
            x1 = cross_mark(RED, r=0.15).move_to(spiel.circle)
            c.wait_until("label is wrong")
            self.play(*appear(ptag, shift=None), st.label_tag.animate.set_color(RED), run_time=0.8)
            self.play(*appear(x1, shift=None), run_time=0.6)
            self.play(ring_to(st, [-2.1, -2.3, 0]), run_time=min(1.0, c.until()))

        # ---------------- c2.match.3 ----------------
        with self.say("c2.match.3") as c:
            zero = count_text("0")
            self.play(*disappear(r1, r2, r3, dots), *swap(cnt, zero), run_time=1.0)
            self.play(*disappear(ptag, x1), st.label_tag.animate.set_color(YELLOW),
                      *set_alpha(patch.people(), 0.35), ring_to(st, matrix.circle.get_center()),
                      run_time=1.0)
            cnt = zero
            card = Code("{title: 'The Kid',\n year: 1921}", size=28)
            card_bg = BackgroundRectangle(card, color=BG, fill_opacity=0.9, buff=0.1)
            cardg = VGroup(card_bg, card)
            cardg.next_to(st.centre(), LEFT, buff=0.82)
            cardg.set_y(st.centre()[1])
            c.wait_until("curly braces")
            self.play(*appear(cardg, shift=None), run_time=1.0)  # early: the card is read out whole
            settle(self, st, add=[cardg])
            c.wait_until("one")
            marks = [cross_mark(RED, r=0.15).move_to(matrix.circle)]
            self.play(*appear(marks[0], shift=None), run_time=0.6)
            for name in ["Hook", "Jaws", "The Gold Rush"]:
                v = patch.vertex(name)
                xm = cross_mark(RED, r=0.15).move_to(v.circle)
                self.play(*during([ring_to(st, v.circle.get_center())], 0, 0.65),
                          *during(appear(xm, shift=None), 0.65, 1.0), run_time=0.75)
                marks.append(xm)
            ok = check_mark(GREEN).scale(0.75).move_to(kid.circle)
            self.play(*during([ring_to(st, kid.circle.get_center())], 0, 0.6),
                      *during(appear(ok, shift=None), 0.6, 1.0), run_time=1.0)
            c.wait_until("one placement")
            r1 = row_text("The Kid", 0)
            one = count_text("1")
            self.play(*fly(kid.name, r1), *during(swap(cnt, one), 0.5, 1.0), run_time=1.5)
            cnt = one
            c.wait_until("bare")
            lab = st.label_tag
            st.remove(lab)
            st.remove(cardg)
            self.add(lab, cardg)
            self.play(FadeOut(lab, shift=1.0 * DOWN),
                      *disappear(cardg, *marks, ok), run_time=1.2)
            bare = Code("(m)", size=40).move_to([COL_X, 2.2, 0])
            c.wait_until("fits every vertex")
            others = [v for v in patch.movies + patch.persons if v is not kid]
            rings = [Circle(radius=HOLE_R).set_stroke(YELLOW, 4).move_to(v.circle) for v in others]
            self.play(*during(disappear(header, rule, r1, divider), 0, 0.45),
                      *during(appear(bare, shift=None), 0.5, 1.0),
                      *set_alpha(patch.people(), 1), run_time=1.0)
            self.play(*appear(*rings, shift=None, lag=0.12), run_time=2.0)
            c.wait_until("twenty-six thousand")
            total = count_text("26,114")
            sum_t = T("2,935 + 23,179", 28, GOLD).move_to([COL_X, -2.45, 0])
            sum_t.shift(min(0, 6.55 - sum_t.get_right()[0]) * RIGHT)
            self.play(*swap(cnt, total), *during(appear(sum_t), 0.5, 1.0), run_time=1.4)
            cnt = total

        # ---------------- c2.match.4 ----------------
        with self.say("c2.match.4") as c:
            self.play(*set_alpha([patch, st, *rings], DIMMED), run_time=1.0)
            c.wait_until("rows")
            A = table([("1", "a"), ("2", "b"), ("3", "c")], -4.6)
            B = table([("2", "x"), ("3", "y"), ("3", "z")], -0.9)
            R = table([("2", "b", "x"), ("3", "c", "y"), ("3", "c", "z")], 4.3)
            tA = T("A", 34, DIM).next_to(A, UP, buff=0.3)
            tB = T("B", 34, DIM).next_to(B, UP, buff=0.3)
            tR = T("result", 34, DIM).next_to(R, UP, buff=0.3)
            sweep_clear(self, *appear(A, B, tA, tB, shift=None, lag=0.15))  # early: the two tables shown whole
            pairs = [(1, 0), (2, 1), (2, 2)]
            links = [Line(A[i].get_right(), B[j].get_left()).set_stroke(YELLOW, 3) for i, j in pairs]
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.4), run_time=1.4)
            arr = Arrow([0.4, 0.38, 0], [2.6, 0.38, 0], buff=0, stroke_width=4, color=DIM)
            self.play(GrowArrow(arr), *appear(tR, shift=None), run_time=0.8)  # early: result column header
            self.play(*appear(*R, shift=None, lag=0.4),
                      *[VShowPassingFlash(l.copy().set_stroke(GOLD, 6), time_width=0.6) for l in links],
                      run_time=1.6)
            cap = T("one placement = one row", 40).move_to(DOWN * 2.3)
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("later")
            v = Circle(radius=0.8).set_stroke(BLUE, 5).set_fill(
                interpolate_color(ManimColor(BG), ManimColor(BLUE), 0.22), 1).move_to(UP * 0.6)
            vt = T("The Kid", 36).next_to(v, DOWN, buff=0.3)
            ringL = Circle(radius=1.0).set_stroke(YELLOW, 5).move_to([-3.6, 0.6, 0])
            ringR = Circle(radius=1.15).set_stroke(YELLOW, 5).move_to([3.6, 0.6, 0])
            mL = set_backstroke(Mono("m", 34, YELLOW)).move_to(ringL.get_center() + [-1.0, 1.0, 0])
            mR = set_backstroke(Mono("m", 34, YELLOW)).move_to(ringR.get_center() + [1.1, 1.15, 0])
            conn = DashedLine(ringL.get_right(), ringR.get_left(), dash_length=0.15).set_stroke(YELLOW, 3)
            gL, gR = VGroup(ringL, mL), VGroup(ringR, mR)
            sweep_clear(self, *appear(v, vt, gL, gR, conn, shift=None, lag=0.1), keep=[cap])  # early: the two-hole stencil shown whole
            self.play(*during([FadeOut(conn)], 0, 0.35),
                      gL.animate.shift(v.get_center() - ringL.get_center()),
                      gR.animate.shift(v.get_center() - ringR.get_center()),
                      run_time=1.8)
            cap2 = T("same name = same vertex", 40).move_to(DOWN * 2.3)
            self.play(*swap(cap, cap2), *flash([v], color=YELLOW), run_time=1.2)
            c.wait_until("next part")
            ch3 = T("part 3", 30, DIM).move_to(DOWN * 3.05)
            self.play(*appear(ch3), run_time=0.8)  # early: a tag for "the next part"

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
