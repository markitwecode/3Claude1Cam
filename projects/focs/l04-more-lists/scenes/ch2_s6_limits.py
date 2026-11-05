"""Chapter 2, scene 6: where polymorphic equality stops. Clips c2.lim.1 – c2.lim.5.

Plan: a big `=` opens, then waits (dim) in the question slot while `double` and `twice` are
defined above it with OCaml's replies. On {ask} the names fly into `double = twice`, a GOLD ?
beside it; the ? becomes the RED exception; the same line then turns into `double = double`,
`member double [twice; double]` and `member double []` (whose reply is a GREEN false). L3's
slogan card; on {loop} it moves up and a looping list appears: 4 BLUE cells (ConsChain style,
values 1-4) whose last pointer leaves to the right, runs back under the row and enters the first
cell from below; a YELLOW box keeps circling it. Then the two-column verdict.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

CODE_SIZE = 36
DEF_X = -4.65          # left edge of the definitions block
Q_SIZE = 44
Q_BASE = -0.38         # baseline of the question line
RING_Y = -0.6          # row of the looping list
LIFT = 0.9             # clip 1 layout sits this much lower


def place(code, anchor, base_y, x0=DEF_X):
    """Left-align a one-line Code at x0 with the baseline of `anchor` at base_y."""
    code.shift(RIGHT * (x0 - code.get_left()[0]))
    code.shift(UP * (base_y - code.find(anchor).get_bottom()[1]))
    return code


def question(src, parts):
    """Separate Mono pieces laid out exactly as in Mono(src), centred, `double` on Q_BASE.
    parts: (substring, nth occurrence, colour)."""
    ref = Mono(src, size=Q_SIZE).move_to(ORIGIN)
    ref.shift(UP * (Q_BASE - select(ref, "double")[0].get_bottom()[1]))
    return [Mono(s, size=Q_SIZE, color=col).move_to(select(ref, s)[n]) for s, n, col in parts]


def tag(text, color, mark=None):
    t = T(text, 32, color)
    if mark is None:
        return t
    return VGroup(mark, t).arrange(RIGHT, buff=0.22)


def loop_back(chain):
    """The last cell's pointer: out to the right, down, back left under the row, up into cell 0."""
    s = chain.cells[3].tail_start()
    y, r = s[1], 0.35
    x_r = chain.cells[3].get_right()[0] + 0.55
    x_l = chain.cells[0].box.get_x()
    y_b = y - 1.3
    P = lambda x, yy: np.array([x, yy, 0.0])  # noqa: E731
    pieces = [
        Line(s, P(x_r - r, y)),
        ArcBetweenPoints(P(x_r - r, y), P(x_r, y - r), angle=-PI / 2),
        Line(P(x_r, y - r), P(x_r, y_b + r)),
        ArcBetweenPoints(P(x_r, y_b + r), P(x_r - r, y_b), angle=-PI / 2),
        Line(P(x_r - r, y_b), P(x_l + r, y_b)),
        ArcBetweenPoints(P(x_l + r, y_b), P(x_l, y_b + r), angle=-PI / 2),
    ]
    curve = VMobject()
    for p in pieces:
        curve.append_points(p.points)
    curve.set_stroke(FG, 3).set_fill(opacity=0)
    head = Arrow(P(x_l, y_b + r), chain.cells[0].box.get_bottom(), buff=0, stroke_width=3,
                 color=FG, max_tip_length_to_length_ratio=0.5, tip_length=0.16)
    return curve, head


class LimitsScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c2.lim.1: two functions, same type ────────────────────────────────────
    def clip1(self):
        with self.say("c2.lim.1") as c:
            big_eq = Mono("=", size=120).move_to(UP * 0.5)
            eq_lab = T("polymorphic equality", 36, DIM).next_to(big_eq, DOWN, buff=0.7)
            self.play(FadeIn(big_eq, scale=0.8), FadeIn(eq_lab, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("two")

            self.def_d = place(Code("let double n = 2 * n", size=CODE_SIZE), "double", 2.9)
            self.rep_d = place(Code("val double : int -> int = <fun>", size=CODE_SIZE), "double", 2.25)
            self.def_t = place(Code("let twice n = n + n", size=CODE_SIZE), "twice", 1.4)
            self.rep_t = place(Code("val twice : int -> int = <fun>", size=CODE_SIZE), "twice", 0.75)
            for code, name in ((self.def_d, "double"), (self.rep_d, "double"),
                               (self.def_t, "twice"), (self.rep_t, "twice")):
                code.find(name).set_color(YELLOW)
            self.types = [self.rep_d.find("int -> int"), self.rep_t.find("int -> int")]
            for g in self.types:
                g.set_color(GREEN)

            q = question("double = twice", [("double", 0, YELLOW), ("=", 0, FG), ("twice", 0, YELLOW)])
            self.q_left, self.q_eq, self.q_right = q
            defs = [self.def_d, self.rep_d, self.def_t, self.rep_t]
            for m in defs + [self.q_eq]:
                m.shift(DOWN * LIFT)          # balanced while alone; rises on {ask}
            self.q_eq.set_opacity(0.4)
            self.play(eq_lab.animate.scale(30 / 36).next_to(self.q_eq, DOWN, buff=0.35),
                      ReplacementTransform(big_eq, self.q_eq),
                      LaggedStart(FadeIn(self.def_d, shift=0.3 * DOWN),
                                  FadeIn(self.def_t, shift=0.3 * DOWN), lag_ratio=0.4),
                      run_time=1.8)
            c.wait_until("Double of en")
            self.play(FlashUnder(self.def_d.find("2 * n"), color=YELLOW, time_width=1.5),
                      run_time=1.3)
            c.wait_until("twice of en")
            self.play(FlashUnder(self.def_t.find("n + n"), color=YELLOW, time_width=1.5),
                      run_time=1.3)

            c.wait_until("same")
            self.play(LaggedStart(FadeIn(self.rep_d, shift=0.2 * DOWN),
                                  FadeIn(self.rep_t, shift=0.2 * DOWN), lag_ratio=0.3),
                      run_time=1.2)
            self.play(*[FlashAround(g, color=GREEN, time_width=1.5) for g in self.types],
                      run_time=1.6)

            c.wait_until("ask")
            self.play(*[m.animate.shift(UP * LIFT) for m in defs],
                      self.q_eq.animate.shift(UP * LIFT).set_opacity(1), FadeOut(eq_lab),
                      TransformFromCopy(self.def_d.find("double"), self.q_left),
                      TransformFromCopy(self.def_t.find("twice"), self.q_right),
                      run_time=1.8)
            self.qmark = Mono("?", size=60, color=GOLD).next_to(self.q_right, RIGHT, buff=0.45)
            self.qmark.align_to(self.q_right, DOWN)
            self.play(FadeIn(self.qmark, scale=0.6), run_time=0.8)

    # ── c2.lim.2: it type-checks, then raises ─────────────────────────────────
    def clip2(self):
        with self.say("c2.lim.2") as c:
            self.tag_ok = tag("type-checks", GREEN, check_mark(GREEN).scale(0.8)).move_to(DOWN * 1.15)
            self.play(FadeIn(self.tag_ok, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("both sides")
            self.play(*[FlashAround(g, color=GREEN, time_width=1.5) for g in self.types],
                      run_time=1.2)

            c.wait_until("raise")
            l1 = Mono("Exception:", size=30, color=RED)
            self.exc_l2 = Mono('Invalid_argument "compare: functional value".', size=30, color=RED)
            self.exc = VGroup(l1, self.exc_l2).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
            self.exc.move_to(DOWN * 2.02)
            self.tag_bad = tag("fails at run time", RED, cross_mark(RED)).move_to(DOWN * 3.05)
            self.play(ReplacementTransform(self.qmark, self.exc), run_time=1.6)
            self.play(FadeIn(self.tag_bad, shift=0.25 * DOWN), run_time=0.9)

            c.wait_until("Invalid argument")
            self.play(FlashUnder(self.exc_l2, color=YELLOW, time_width=1.5), run_time=1.8)

            c.wait_until("nofun")
            box = token_box(select(self.exc_l2, "functional value")[0], self.exc_l2)
            self.play(FadeIn(box), FlashAround(self.q_eq, color=YELLOW, time_width=1.5),
                      run_time=1.3)

            c.wait_until("self")
            q2 = question("double = double", [("double", 0, YELLOW), ("=", 0, FG), ("double", 1, YELLOW)])
            self.q_right2 = q2[2]
            self.play(FadeOut(box), FadeOut(self.q_right),
                      self.q_left.animate.move_to(q2[0]), self.q_eq.animate.move_to(q2[1]),
                      TransformFromCopy(self.q_left, self.q_right2), run_time=1.5)
            self.play(FlashAround(self.exc, color=RED, time_width=1.5), run_time=1.1)

    # ── c2.lim.3: member inherits it; the empty list doesn't; the slogan ───────
    def clip3(self):
        with self.say("c2.lim.3") as c:
            q3 = question("member double [twice; double]",
                          [("member", 0, YELLOW), ("double", 0, YELLOW), ("[", 0, TEAL),
                           ("twice", 0, YELLOW), (";", 0, TEAL), ("double", 1, YELLOW),
                           ("]", 0, TEAL)])
            m_member, m_double, m_lb, m_twice, m_semi, m_double2, m_rb = q3
            self.play(*set_alpha([self.exc, self.tag_bad], DIMMED), run_time=1.0)

            c.wait_until("list")
            self.play(FadeOut(self.q_eq), FadeOut(self.q_right2),
                      self.q_left.animate.move_to(m_double),
                      FadeIn(m_member, shift=0.3 * RIGHT),
                      FadeIn(m_lb), FadeIn(m_semi), FadeIn(m_rb),
                      TransformFromCopy(self.def_t.find("twice"), m_twice),
                      TransformFromCopy(self.def_d.find("double"), m_double2), run_time=1.4)
            c.wait_until("and you get")
            self.play(time_span(FlashAround(self.q_left, color=YELLOW, time_width=1.5), 0, 1.1),
                      time_span(FlashAround(m_twice, color=YELLOW, time_width=1.5), 0, 1.1),
                      *[time_span(a, 0.6, 1.5) for a in set_alpha([self.exc, self.tag_bad], 1)],
                      run_time=1.5)

            c.wait_until("empty")
            q4 = question("member double []", [("member", 0, YELLOW), ("double", 0, YELLOW),
                                               ("[", 0, TEAL), ("]", 0, TEAL)])
            self.play(FadeOut(m_twice), FadeOut(m_semi), FadeOut(m_double2),
                      m_member.animate.move_to(q4[0]), self.q_left.animate.move_to(q4[1]),
                      m_lb.animate.move_to(q4[2]), m_rb.animate.move_to(q4[3]), run_time=1.5)
            c.wait_until("just false")
            reply = Mono("- : bool = false", size=36, color=GREEN).move_to(self.exc)
            self.play(ReplacementTransform(self.exc, reply), run_time=1.5)
            c.wait_until("no comparison")
            nocmp = tag("no comparison", GREEN, check_mark(GREEN).scale(0.8)).move_to(self.tag_bad)
            self.play(ReplacementTransform(self.tag_bad, nocmp), run_time=1.0)

            # the slogan card
            c.wait_until("slogan")
            c.wait_until("type-checking")   # the GREEN tag flashes as the voice says "type-checking"
            self.play(FlashAround(self.tag_ok, color=GREEN, time_width=1.5),
                      run_time=min(1.5, c.until("lecture three")))
            frame = RoundedRectangle(corner_radius=0.2, width=10.9, height=2.35)
            frame.set_stroke(DIM, 2).set_fill(opacity=0).move_to(UP * 0.55)
            header = T("Lecture 3", 32, DIM).next_to(frame, UP, buff=0.18).align_to(frame, LEFT).shift(RIGHT * 0.2)
            s1 = T("Well-typed programs cannot go wrong.", 34, disable_ligatures=True)
            s2 = T("They might run forever, or raise an exception,", 34, disable_ligatures=True)
            s3 = T("but they never mix up their types.", 34, disable_ligatures=True)
            lines = VGroup(s1, s2, s3).arrange(DOWN, buff=0.28).move_to(frame)
            c.wait_until("lecture three")   # card + "Lecture 3" header settle before "Well-typed programs"
            sweep_clear(self, time_span(FadeIn(frame), 0.5, 1.2),
                        time_span(FadeIn(header, shift=0.2 * DOWN), 0.6, 1.2), run_time=1.2)
            c.wait_until("Well-typed programs")
            self.play(FadeIn(s1, lag_ratio=0.1), run_time=1.4)
            c.wait_until("They might run forever")
            self.play(FadeIn(s2, lag_ratio=0.1), FadeIn(s3, lag_ratio=0.1), run_time=1.4)
            c.wait_until("raise an exception")
            ul_raise = underline(select(s2, "raise an exception")[0], YELLOW)
            self.play(Create(ul_raise), run_time=0.9)

            c.wait_until("later")
            later = T("functions as values: a later lecture", 32, DIM).next_to(frame, DOWN, buff=0.3)
            self.play(FadeIn(later, shift=0.2 * DOWN), run_time=1.0)
            self.card = VGroup(header, frame, lines, ul_raise, later)
            self.later = later
            self.s2 = s2

    # ── c2.lim.4: a list that loops back on itself ────────────────────────────
    def clip4(self):
        with self.say("c2.lim.4") as c:
            ul_run = underline(select(self.s2, "run forever")[0], YELLOW)
            self.play(Create(ul_run), run_time=1.0)
            self.card.add(ul_run)

            c.wait_until("loop")
            chain = ConsChain([1, 2, 3, 4], with_nil=False).shift(UP * RING_Y)
            curve, head = loop_back(chain)
            build = []
            for i, cell in enumerate(chain.cells):
                build.append(FadeIn(cell, shift=0.2 * DOWN))
                if i < 3:
                    build.append(GrowArrow(chain.arrows[i]))
            self.play(self.card.animate.scale(0.9).to_edge(UP, buff=0.4),
                      time_span(LaggedStart(*build, lag_ratio=0.3), 0.5, 2.2), run_time=2.2)
            c.wait_until("points back")
            self.play(Succession(Create(curve, run_time=1.3), GrowArrow(head, run_time=0.4)),
                      run_time=1.7)

            c.wait_until("forever")
            self.ptr = self.circling_box(chain)
            never = T("may never finish", 32, DIM).move_to(UP * (RING_Y - 2.4))
            self.play(FadeIn(self.ptr), FadeOut(self.later), FadeIn(never, shift=0.2 * DOWN),
                      run_time=1.0)
            self.start_circling(self.ptr, chain)

    def circling_box(self, chain):
        box = RoundedRectangle(corner_radius=0.12, width=CELL + PTR_W + 0.3, height=CELL + 0.3)
        return box.set_stroke(YELLOW, 4).set_fill(opacity=0).move_to(chain.cells[0])

    def start_circling(self, box, chain):
        """Hop cell to cell, then swing back under the row to the first: round and round."""
        cs = [cell.get_center() for cell in chain.cells]
        hop, back, dwell = 0.42, 0.8, 0.22
        segs = [(hop, Line(cs[0], cs[1])), (hop, Line(cs[1], cs[2])), (hop, Line(cs[2], cs[3])),
                (back, Line(cs[3], cs[0], path_arc=-1.34))]
        lap = sum(d + dwell for d, _ in segs)
        state = {"t": 0.0}

        def upd(m, dt):
            state["t"] = (state["t"] + dt) % lap
            t = state["t"]
            for d, path in segs:
                if t < dwell:
                    m.move_to(path.get_start())
                    return
                t -= dwell
                if t < d:
                    m.move_to(path.point_from_proportion(smooth(t / d)))
                    return
                t -= d
            m.move_to(cs[0])

        box.add_updater(upd)

    # ── c2.lim.5: contentious; fine for us ────────────────────────────────────
    def clip5(self):
        with self.say("c2.lim.5") as c:
            heading = T("polymorphic equality", 48).move_to(UP * 2.7)
            c.wait_until("polymorphic equality")
            self.ptr.clear_updaters()
            sweep_clear(self, time_span(FadeIn(heading, shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)

            c.wait_until("small")
            left = VGroup(T("small programs:", 40, GREEN), T("easy", 40, GREEN))
            left.arrange(DOWN, buff=0.3).move_to(LEFT * 3.0 + UP * 0.85)
            self.play(FadeIn(left, shift=0.3 * DOWN, lag_ratio=0.2), run_time=1.1)
            c.wait_until("large")
            right = VGroup(T("large systems:", 40, RED), T("dangerous", 40, RED))
            right.arrange(DOWN, buff=0.3).move_to(RIGHT * 3.0 + UP * 0.85)
            self.play(FadeIn(right, shift=0.3 * DOWN, lag_ratio=0.2), run_time=1.1)

            c.wait_until("explicit")
            expl = VGroup(T("explicit compare functions", 32),
                          T("(later, with higher-order functions)", 28, DIM))
            expl.arrange(DOWN, buff=0.2).next_to(right, DOWN, buff=0.6)
            self.play(FadeIn(expl, shift=0.25 * DOWN, lag_ratio=0.2), run_time=1.1)

            c.wait_until("fine")
            fine = tag("fine for us, for now", GREEN, check_mark(GREEN))
            fine[1].scale(42 / 32)
            fine.arrange(RIGHT, buff=0.25).move_to(DOWN * 2.75)
            self.play(FadeIn(fine, shift=0.25 * DOWN), run_time=0.8)
        self.wait(3.3)
