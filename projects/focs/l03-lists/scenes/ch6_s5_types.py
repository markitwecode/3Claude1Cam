"""STATUS: done; vk check clean except the opening row's dwell (s1's row, already read there).
Departure: the 'a -> 'a ghost is `let rec loop (x : 'a) : 'a = loop x` (same name as on screen,
same verified error) rather than loop2. 2.0 s silent hold after c6.types.4 (error reading time).

Chapter 6, scene 5: exercise 3.4 solved. Why 'a -> 'a and 'a -> 'b make sense, and why
neither can cause a type error at run time. Clips c6.types.1 - c6.types.8.

Opens on s1's five-card row (ch5_s6's overview geometry); card 3.4 grows into the kit's hero
card (statement + pause tag). Then: id as a machine (the promise), id [id [id 0]] typed inside
out, id true / id 3 rejected, where loop's 'b comes from, loop never returns, loop true /
loop 3 accepted but running forever, and Milner's slogan.

Verified (ocaml 5.4.1): let id x = x -> val id : 'a -> 'a = <fun>; let rec loop x = loop x ->
val loop : 'a -> 'b = <fun>; id [id [id 0]] -> - : int list list = [[0]]; id true / id 3 ->
Error: This expression has type bool but an expression was expected of type int (underline:
id true; shown on two lines as in ch2_s6); ( / ) -> - : int -> int -> int = <fun>;
fun () -> loop true / loop 3 -> - : unit -> int = <fun>; after
let rec loop (x : 'a) : 'a = loop x, the same error under loop true.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, VShowPassingFlash, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import (  # noqa: E402  the shared exercise-card kit (read-only)
    CARD_FILL, COL_X, BigCard, HeroCard, finish, hold_for, pause_tag,
)

PINKS = ["#F6C4EE", PINK, "#C564B4"]   # outer, middle, inner id: each use its own 'a (as ch5_s7)
TOP_Y = 2.95                           # the reference line (definition + OCaml's reply)
CARD_H = 6.2
CS = 34                                # code size on the card
MY = 0.0                               # id machine
LY = 0.3                               # loop machine
CHAIN_Y = -1.9                         # loop true -> loop true -> ...
EX = -4.6                              # left edge of id [id [id 0]] in c6.types.3
SX = -5.9                              # left edge of the session rows in c6.types.4


def g(code, sub, nth=0):
    """Glyphs of a substring, as a fresh VGroup."""
    return VGroup(*code.find(sub, nth=nth))


def glyph(code, sub, nth=0, idx=0):
    return code.find(sub, nth=nth)[idx]


def assemble(scene, code, pairs=(), rest=(), run_time=1.5, extra=()):
    """Bring `code` on screen: each (source, substring) flies out of a copy of its source, the
    `rest` substrings fade in; then the glyph wrappers are swapped for the real Code."""
    anims, parts = list(extra), []
    for src, sub in pairs:
        part = g(code, sub)
        parts.append(part)
        anims.append(TransformFromCopy(src, part))
    for sub in rest:
        part = g(code, sub)
        parts.append(part)
        anims.append(FadeIn(part, shift=0.2 * UP))
    scene.play(*anims, run_time=run_time)
    scene.remove(*parts)
    scene.add(code)


def bracket(mob, y, color, tick=0.14, width=4):
    """A flat bracket under `mob` at height y, its ends ticking up."""
    l, r = mob.get_left()[0], mob.get_right()[0]
    return VMobject().set_points_as_corners(
        [[l, y + tick, 0], [l, y, 0], [r, y, 0], [r, y + tick, 0]]).set_stroke(color, width)


def type_tag(var, ty, shade=PINK, size=32):
    """`'a = int list`: the variable in its PINK, the type it stands for in GREEN."""
    v = Mono(f"{var} =", size=size, t2c={var: shade})
    t = Mono(ty, size=size, color=GREEN)
    tag = VGroup(v, t).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
    tag.var, tag.ty = v, t
    return tag


def pill(text, color=PINK):
    """A value on its way into a machine."""
    box = RoundedRectangle(corner_radius=0.3, width=text.width + 0.5, height=0.66)
    box.set_stroke(color, 3).set_fill(BG, 1).move_to(text)
    return VGroup(box, text)


def machine(name, y, out_end=5.6):
    box = RoundedRectangle(corner_radius=0.22, width=3.2, height=1.9)
    box.set_stroke(BLUE, 4).set_fill(CARD_FILL, 1).move_to([0, y, 0])
    lab = Mono(name, size=48, color=YELLOW).next_to(box, UP, buff=0.22)
    kw = dict(buff=0, stroke_width=5, color=PINK, max_tip_length_to_length_ratio=0.1)
    inp = Arrow([-5.6, y, 0], box.get_left(), **kw)
    out = Arrow(box.get_right(), [out_end, y, 0], **kw)
    return box, lab, inp, out


def error_lines(size=30):
    """OCaml's reply to a bool where an int was expected (two lines, as in ch2_s6)."""
    e1 = Mono("Error: This expression has type bool", size=size, t2c={"Error:": RED, "bool": GREEN})
    e2 = Mono("but an expression was expected of type int", size=size, t2c={"int": GREEN})
    e2.next_to(e1, DOWN, buff=0.2).align_to(select(e1, "This")[0], LEFT)
    return VGroup(e1, e2)


def make_clock(center, r=0.42):
    face = Circle(radius=r).set_stroke(FG, 3).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.1) * np.array([np.cos(a), np.sin(a), 0]),
                          center + (r - 0.02) * np.array([np.cos(a), np.sin(a), 0]))
                     for a in np.arange(0, TAU, TAU / 4)]).set_stroke(DIM, 2)
    hand = Line(center, center + UP * (r - 0.1)).set_stroke(GOLD, 4)
    hub = Dot(center, radius=0.05, color=GOLD)
    return VGroup(face, ticks, hand, hub)


def start_ticking(hand, center, period=0.5):
    state = {"t": 0.0, "k": 0}

    def upd(m, dt):
        state["t"] += dt
        k = int(state["t"] / period)
        if k != state["k"]:
            m.rotate(-(k - state["k"]) * TAU / 12, about_point=center)
            state["k"] = k
    hand.add_updater(upd)


def start_blink(cur, period=1.0):
    state = {"t": 0.0}

    def upd(m, dt):
        state["t"] += dt
        m.set_fill(opacity=1.0 if (state["t"] % period) < period * 0.55 else 0.0)
    cur.add_updater(upd)


class TwoStrangeTypes(NarratedScene):
    def construct(self):
        self.statement()
        self.id_promise()
        self.nested()
        self.contrast()
        self.beta()
        self.never()
        self.division()
        self.guarantee()
        hold_for(self, self.last_born, self.last_len)
        finish(self)

    # c6.types.1: the five cards; 3.4 grows into the hero card; the statement; pause
    def statement(self):
        bigs = VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * 0.7)
        card = HeroCard(3, height=CARD_H)
        id_def = Code("let id x = x", size=CS).move_to([COL_X, 1.48, 0], aligned_edge=LEFT)
        id_val = Code("val id : 'a -> 'a = <fun>", size=CS).move_to([COL_X, 0.92, 0], aligned_edge=LEFT)
        lp_def = Code("let rec loop x = loop x", size=CS).move_to([COL_X, 0.18, 0], aligned_edge=LEFT)
        lp_val = Code("val loop : 'a -> 'b = <fun>", size=CS).move_to([COL_X, -0.38, 0], aligned_edge=LEFT)
        q1 = T("Why do these types make logical sense,", size=34).move_to([COL_X, -1.14, 0], aligned_edge=LEFT)
        q2 = T("and prevent run-time type errors?", size=34).move_to([COL_X, -1.66, 0], aligned_edge=LEFT)
        e_id = Code("id [id [id 0]]", size=38).move_to([COL_X, -2.42, 0], aligned_edge=LEFT)
        e_lp = Code("loop true / loop 3", size=38).move_to([0.3, -2.42, 0], aligned_edge=LEFT)
        note = T("/ is integer division", size=28, color=DIM).move_to([e_lp.get_x(), -3.0, 0])
        tag = pause_tag()

        # s1's row, as it left it
        self.play(LaggedStart(*[FadeIn(b) for b in bigs], lag_ratio=0.1), run_time=0.8)
        self.wait(0.9)
        with self.say("c6.types.1") as c:
            # "Exercise three point four."  3.4 lights up, then grows into the hero card.
            big = bigs[3]
            others = [b for b in bigs if b is not big]
            self.play(big.frame.animate.set_stroke(YELLOW, 3), big.num.animate.set_color(YELLOW),
                      LaggedStart(*[FadeOut(b) for b in others], lag_ratio=0.1), run_time=0.8)
            self.play(TransformFromCopy(big.frame, card.frame), FadeTransform(big.num.copy(), card.header),
                      FadeOut(big.name), run_time=1.4)
            self.remove(big)
            # "The identity function, eye-dee, returns its argument, and has type alpha to alpha."
            c.wait_until("id")
            self.play(FadeIn(id_def, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("alpha to alpha")
            self.play(FadeIn(id_val, shift=0.25 * DOWN), run_time=1.0)
            # "Loop calls itself forever, and has type alpha to beta."
            c.wait_until("loop")
            self.play(FadeIn(lp_def, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("alpha to beta")
            self.play(FadeIn(lp_val, shift=0.25 * DOWN), run_time=1.0)
            # "Why do these types make sense?"
            c.wait_until("question")
            self.play(FadeIn(q1, shift=0.25 * DOWN), run_time=1.0)
            # "And why can't they cause type errors at run time, even in strange expressions like these?"
            c.wait_until("and why")
            self.play(FadeIn(q2, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("even in strange")
            self.play(LaggedStart(FadeIn(e_id, shift=0.25 * DOWN), FadeIn(e_lp, shift=0.25 * DOWN),
                                  FadeIn(note, shift=0.2 * UP), lag_ratio=0.3), run_time=1.3)
            # "Pause, and think it through."
            c.wait_until("stop")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.8)
        self.id_def, self.id_val, self.tag = id_def, id_val, tag

    # c6.types.2: 'a -> 'a as a promise: id as a machine
    def id_promise(self):
        top = Code("let id x = x" + " " * 4 + "val id : 'a -> 'a = <fun>", size=CS).move_to([0, TOP_Y, 0])
        box, name, inp, out = machine("id", MY)
        la = Mono("'a", size=44, color=PINK).move_to([inp.get_x(), MY + 0.68, 0])
        lb = Mono("'a", size=44, color=PINK).move_to([out.get_x(), MY + 0.68, 0])
        cap_t = T("for every type", size=34)
        cap_a = Mono("'a", size=38, color=PINK).next_to(cap_t, RIGHT, buff=0.22)
        cap_a.align_to(cap_t[0], DOWN)
        cap = VGroup(cap_t, cap_a).move_to([0, MY - 1.6, 0])
        token = pill(Mono("x", size=40)).move_to([-4.7, MY, 0])
        q = T("?", size=84, color=GOLD).move_to(box)
        cross = cross_mark(RED, r=0.42).move_to(q)
        spin = Arc(radius=0.5, start_angle=PI * 0.62, angle=-TAU * 0.82, arc_center=box.get_center())
        spin.set_stroke(DIM, 3).add_tip(tip_length=0.16, tip_width=0.16)
        never = T("or never return", size=30, color=DIM).move_to([3.6, MY - 0.62, 0])

        with self.say("c6.types.2") as c:
            # "Read alpha to alpha as a promise."  The card clears; id's line goes to the top.
            p1, p2 = g(top, "let id x = x"), g(top, "val id : 'a -> 'a = <fun>")
            sweep_clear(self, ReplacementTransform(self.id_def, p1), ReplacementTransform(self.id_val, p2),
                        time_span(AnimationGroup(FadeIn(box), FadeIn(name, shift=0.2 * DOWN),
                                                 GrowArrow(inp), GrowArrow(out)), 0.7, 1.6),
                        keep=[self.id_def, self.id_val, self.tag], run_time=1.6)
            self.remove(p1, p2)
            self.add(top)
            # "Whatever alpha is, give the function an alpha, and you get an alpha back."
            c.wait_until("whatever alpha is")
            self.play(TransformFromCopy(g(top, "'a", 0), la), TransformFromCopy(g(top, "'a", 1), lb),
                      FadeIn(cap, shift=0.2 * UP), FadeOut(self.tag), run_time=1.5)
            c.wait_until("give the function")
            self.play(FadeIn(token, shift=0.4 * RIGHT), run_time=0.6)
            self.play(token.animate.move_to(box), run_time=1.0)
            c.wait_until("you get an alpha back")
            self.play(token.animate.move_to([4.5, MY, 0]), run_time=1.2)
            # "But it knows nothing about alpha, so it can't make up a new alpha."
            c.wait_until("only")
            self.play(FadeIn(q, scale=0.6), run_time=0.9)
            c.wait_until("make up a new")
            self.play(Create(cross), q.animate.set_opacity(0.45), run_time=0.9)
            # "All it can hand back is the value you gave it."  (the x in is the x out)
            c.wait_until("all it can hand back")
            xs = [glyph(top, "x", 0), glyph(top, "x", 1)]
            path = Line([-5.6, MY, 0], [5.6, MY, 0]).set_stroke(YELLOW, 8)
            self.play(VShowPassingFlash(path, time_width=0.5),
                      *[FlashAround(x, color=YELLOW, buff=0.06) for x in xs], *recolor(xs, YELLOW),
                      token[1].animate.set_color(YELLOW), run_time=1.5)
            # "Or it could never return at all."  "Hold that thought."
            c.wait_until("except")
            self.play(FadeOut(q), FadeOut(cross), time_span(Create(spin), 0.3, 1.2),
                      FadeIn(never, shift=0.2 * DOWN), run_time=1.2)
        self.top, self.id_held = top, [box, spin, never]

    # c6.types.3: id [id [id 0]], inside out; each id gets its own 'a
    def nested(self):
        top = self.top
        e = Code("id [id [id 0]]", size=52).move_to([EX, 1.55, 0], aligned_edge=LEFT)
        subs = ["id 0", "id [id 0]", "id [id [id 0]]"]      # inner, middle, outer
        tys = ["int", "int list", "int list list"]
        shades = [PINKS[2], PINKS[1], PINKS[0]]
        ys = [0.72, 0.05, -0.62]
        spans, tags = [], []
        for sub, ty, sh, y in zip(subs, tys, shades, ys):
            sp = bracket(g(e, sub), y, sh)
            tg = type_tag("'a", ty, sh)
            tg.move_to([sp.get_right()[0] + 0.3, y + 0.07, 0], aligned_edge=LEFT)
            spans.append(sp)
            tags.append(tg)
        reply = Code("- : int list list = [[0]]", size=44).move_to([EX, -2.0, 0], aligned_edge=LEFT)
        brackets = VGroup(glyph(e, "[", 0), glyph(e, "[", 1), glyph(e, "0"), glyph(e, "]", 0), glyph(e, "]", 1))

        with self.say("c6.types.3") as c:
            # "Now take eye-dee of a list, of eye-dee of a list, of eye-dee of zero."
            sweep_clear(self, time_span(FadeIn(e, shift=0.25 * DOWN), 0.5, 1.5), keep=[top, *self.id_held],
                        run_time=1.5)
            # "Work from the inside out."
            c.wait_until("work from the inside out")
            box = token_box(e.find("id 0"), e)
            self.play(*[FadeOut(m) for m in self.id_held], FadeIn(box),
                      FlashAround(glyph(e, "0"), color=YELLOW, buff=0.06), run_time=1.0)
            # "The innermost eye-dee is given an int."  "The next, an int list."  "And the outer one ..."
            for k, cue in enumerate(["inner", "middle", "outer"]):
                c.wait_until(cue)
                anims = [Create(spans[k]), FadeIn(tags[k], shift=0.2 * LEFT)]
                if k:
                    anims.append(Transform(box, token_box(e.find(subs[k]), e)))
                self.play(*anims, run_time=1.3 if k == 0 else 1.1)
            # "The same function, at three different types, because each use gets its own fresh alpha."
            c.wait_until("three")
            self.play(FadeOut(box), *[FlashAround(g(e, "id", n), color=YELLOW, buff=0.06) for n in range(3)],
                      run_time=1.3)
            c.wait_until("its own fresh")
            self.play(*[FlashAround(t.var, color=sh, buff=0.06) for t, sh in zip(tags, shades)], run_time=1.2)
            # "Every promise is kept, and the result is a list of lists holding zero."
            c.wait_until("every promise")
            assemble(self, reply, pairs=[(tags[2].ty, "int list list"), (brackets, "[[0]]")],
                     rest=["- :", "="], run_time=1.5,
                     extra=[FlashAround(g(top, "'a -> 'a"), color=GREEN, buff=0.08)])
        self.e, self.reply = e, reply

    # c6.types.4: id true / id 3 is rejected before it runs
    def contrast(self):
        top, e, reply = self.top, self.e, self.reply
        e.generate_target()
        e.target.scale(CS / 52).move_to([SX, 1.6, 0], aligned_edge=LEFT)
        reply.generate_target()
        reply.target.scale(CS / 44).next_to(e.target, RIGHT, buff=0.9).align_to(e.target, DOWN)
        bad = Code("id true / id 3", size=44).move_to([SX, 0.05, 0], aligned_edge=LEFT)
        ul = underline(g(bad, "id true"), RED)
        err = error_lines().move_to([SX, -1.45, 0], aligned_edge=LEFT)
        xm = cross_mark(RED, r=0.24).next_to(bad, RIGHT, buff=0.55)

        with self.say("c6.types.4") as c:
            # "Compare eye-dee of true, divided by eye-dee of three."
            sweep_clear(self, MoveToTarget(e), MoveToTarget(reply),
                        time_span(FadeIn(bad, shift=0.25 * DOWN), 0.6, 1.5), keep=[top, e, reply], run_time=1.5)
            # "That's rejected before it runs, because eye-dee of true is a bool, and you can't divide a bool."
            c.wait_until("bad")
            self.play(Create(ul), GrowFromCenter(xm), FadeIn(err, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("is a bool")
            self.play(FlashAround(select(err[0], "bool")[0], color=GREEN, buff=0.06),
                      FlashAround(g(bad, "id true"), color=RED, buff=0.08), run_time=1.0)
            c.wait_until("divide a bool")
            self.play(FlashAround(glyph(bad, "/"), color=RED, buff=0.08), run_time=0.9)
        self.wait(2.0)      # the end of the id half: let OCaml's error be read before loop

    # c6.types.5: where does 'b come from? Nothing in the definition pins it down.
    def beta(self):
        rv = Code("val loop : 'a -> 'b = <fun>", size=44).move_to([0, 2.55, 0])
        d = Code("let rec loop x = loop x", size=52).move_to([0, 0.55, 0])
        b = g(rv, "'b")
        q = T("?", size=60, color=GOLD).move_to([b.get_x(), 1.62, 0])
        free = T("free", size=40, color=PINK).move_to(q)
        lhs, body = g(d, "loop x", 0), g(d, "loop x", 1)
        u1, u2 = underline(lhs, YELLOW), underline(body, YELLOW)
        l1 = Mono("'b", size=44, color=PINK).next_to(u1, DOWN, buff=0.25)
        l2 = Mono("'b", size=44, color=PINK).next_to(u2, DOWN, buff=0.25)

        with self.say("c6.types.5") as c:
            # "Now, alpha to beta."
            sweep_clear(self, time_span(FadeIn(rv, shift=0.25 * DOWN), 0.4, 1.4),
                        time_span(FadeIn(d, shift=0.25 * DOWN), 0.7, 1.6), run_time=1.6)
            # "Where does the beta come from?"
            c.wait_until("where")
            self.play(FadeIn(q, scale=0.6), FlashAround(b, color=PINK, buff=0.06), run_time=1.0)
            # "The definition says loop of ex is loop of ex, so the result is whatever loop returns, ..."
            c.wait_until("infer")
            self.play(Create(u1), Create(u2), run_time=1.2)
            c.wait_until("whatever loop returns")
            self.play(TransformFromCopy(b, l1), TransformFromCopy(b, l2), run_time=1.5)
            # "So the result type stays free."  "That's beta."
            c.wait_until("nothing pins")
            self.play(ReplacementTransform(q, free), run_time=1.1)
            c.wait_until("free")
            self.play(FlashAround(b, color=PINK, buff=0.06), FlashAround(l1, color=PINK, buff=0.06),
                      FlashAround(l2, color=PINK, buff=0.06), run_time=1.4)
        self.rv = rv

    # c6.types.6: as a promise it sounds absurd; it's safe because loop never returns
    def never(self):
        rv = self.rv
        box, name, inp, out = machine("loop", LY, out_end=4.5)
        la = Mono("'a", size=44, color=PINK).move_to([inp.get_x(), LY + 0.72, 0])
        lb = Mono("'b", size=44, color=PINK).move_to([out.get_x(), LY + 0.72, 0])
        token = pill(Code("true", size=36)).move_to([-4.6, LY, 0])
        types = VGroup(*[Mono(t, size=32, color=GREEN) for t in ("int", "string", "bool")])
        types.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.85, LY, 0], aligned_edge=LEFT)
        q = T("?", size=64, color=GOLD).move_to([types.get_x(), LY + 1.5, 0])
        items = [Code("loop true", size=36) for _ in range(3)]
        arrows = [Arrow(LEFT * 0.38, RIGHT * 0.38, buff=0, stroke_width=4, color=YELLOW,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.18) for _ in range(3)]
        dots = T("…", size=44)
        chain = VGroup(items[0], arrows[0], items[1], arrows[1], items[2], arrows[2], dots)
        chain.arrange(RIGHT, buff=0.18).move_to([0, CHAIN_Y, 0])
        back = CurvedArrow(dots.get_bottom() + DOWN * 0.15, items[0].get_bottom() + DOWN * 0.15,
                           angle=-0.55, color=YELLOW, stroke_width=4, tip_length=0.18)
        back_path = ArcBetweenPoints(dots.get_bottom() + DOWN * 0.15, items[0].get_bottom() + DOWN * 0.15,
                                     angle=-0.55).set_stroke(YELLOW, 8)
        stops = [items[0], items[1], items[2], dots]
        hh = items[0].height + 0.3

        def hop_rect(m):
            r = RoundedRectangle(corner_radius=0.1, width=m.width + 0.3, height=hh)
            return r.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.08).move_to([m.get_x(), CHAIN_Y, 0])

        never_lab = T("never arrives", size=30, color=DIM).move_to([out.get_x(), LY - 0.6, 0])

        with self.say("c6.types.6") as c:
            # "As a promise, it sounds absurd."  loop's reply goes up; loop as a machine.
            sweep_clear(self, rv.animate.scale(40 / 44).move_to([0, TOP_Y, 0]),
                        time_span(AnimationGroup(FadeIn(box), FadeIn(name, shift=0.2 * DOWN),
                                                 GrowArrow(inp), GrowArrow(out)), 0.6, 1.5),
                        keep=[rv], run_time=1.5)
            # "Give loop anything, and it returns any type you like."
            c.wait_until("give loop anything")
            self.play(TransformFromCopy(g(rv, "'a"), la), TransformFromCopy(g(rv, "'b"), lb),
                      FadeIn(token, shift=0.4 * RIGHT), run_time=1.3)
            c.wait_until("any type you like")
            self.play(token.animate.move_to(box),
                      LaggedStart(*[FadeIn(t, shift=0.3 * RIGHT) for t in types], lag_ratio=0.3), run_time=1.5)
            # "How can that be safe?"
            c.wait_until("question")
            self.play(FadeIn(q, scale=0.6), run_time=0.8)
            # "Because loop never returns."  loop true calls loop true calls loop true ...
            c.wait_until("never")
            self.play(LaggedStart(TransformFromCopy(token, items[0]), GrowArrow(arrows[0]),
                                  FadeIn(items[1], shift=0.2 * RIGHT), GrowArrow(arrows[1]),
                                  FadeIn(items[2], shift=0.2 * RIGHT), GrowArrow(arrows[2]),
                                  FadeIn(dots), lag_ratio=0.22),
                      FadeIn(never_lab, shift=0.2 * DOWN), run_time=2.0)
            hop = hop_rect(items[0])
            self.play(Create(back), FadeIn(hop), run_time=0.9)
            # "A promise about the result can't be broken if the result never arrives."
            c.wait_until("vacuous")
            self.play(*set_alpha([out, lb, types], DIMMED), FadeOut(q), Transform(hop, hop_rect(items[1])),
                      run_time=1.2)
            self.hops, k = 0, 1

            def lap(k):
                k = (k + 1) % len(stops)
                anims = [Transform(hop, hop_rect(stops[k]))]
                if k == 0:
                    anims.append(VShowPassingFlash(back_path.copy(), time_width=0.6))
                self.play(*anims, run_time=0.7)
                self.wait(0.2)
                return k
            while c.remaining > 1.1:          # round and round, until the line ends
                k = lap(k)
        k = lap(k)                            # ... and on, a beat past it
        self.first_call = items[0]

    # c6.types.7: loop true / loop 3 type-checks, runs forever, never goes wrong; 'a -> 'a would be rejected
    def division(self):
        h = Code("loop true / loop 3", size=52).move_to([0, 1.5, 0])
        slash = glyph(h, "/")
        div_t = Code("( / ) : int -> int -> int", size=CS)
        div_t.move_to([0, 2.75, 0])
        div_t.shift(RIGHT * min(slash.get_x() - glyph(div_t, "/").get_x(), 6.1 - div_t.get_right()[0]))
        sp1 = bracket(g(h, "loop true"), 0.9, GREEN)
        sp2 = bracket(g(h, "loop 3"), 0.9, GREEN)
        t1 = type_tag("'b", "int").next_to(sp1, DOWN, buff=0.16)
        t2 = type_tag("'b", "int").next_to(sp2, DOWN, buff=0.16)
        fun_row = Code("fun () -> loop true / loop 3", size=32)
        fx = -fun_row.width / 2
        fun_row.move_to([fx, -0.45, 0], aligned_edge=LEFT)
        fun_val = Code("- : unit -> int = <fun>", size=32).move_to([fx, -1.0, 0], aligned_edge=LEFT)
        ok = check_mark(GREEN).next_to(fun_val, RIGHT, buff=0.45)
        prompt = VGroup(Mono("#", size=36, color=DIM), Code("loop true / loop 3;;", size=36))
        prompt.arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([fx, -2.25, 0], aligned_edge=LEFT)
        cursor = Rectangle(width=0.2, height=0.42).set_stroke(width=0).set_fill(FG, 1)
        cursor.move_to([fx + 0.1, -2.9, 0])
        clock_c = np.array([prompt.get_right()[0] + 1.0, -2.55, 0])
        clock = make_clock(clock_c)
        ghost = Code("let rec loop (x : 'a) : 'a = loop x", size=32).set_opacity(0.6).move_to([0, 2.75, 0])
        ghost_box = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=ghost.width + 0.5,
                                                    height=ghost.height + 0.36), num_dashes=60)
        ghost_box.set_stroke(DIM, 2).move_to(ghost)
        ul = underline(g(h, "loop true"), RED)
        err = error_lines().move_to([-6.1, -0.7, 0], aligned_edge=LEFT)

        with self.say("c6.types.7") as c:
            # "So look at loop of true, divided by loop of three."
            p1, p2 = g(h, "loop true"), g(h, "/ loop 3")
            sweep_clear(self, time_span(TransformFromCopy(self.first_call, p1), 0.3, 1.5),
                        time_span(FadeIn(p2, shift=0.2 * LEFT), 0.7, 1.5), run_time=1.5)
            self.remove(p1, p2)
            self.add(h)
            # "Division needs integers, and loop can promise integers, so OCaml accepts it."
            c.wait_until("checks")
            self.play(FadeIn(div_t, shift=0.2 * DOWN), FlashAround(slash, color=YELLOW, buff=0.08), run_time=1.1)
            c.wait_until("loop can promise")
            self.play(Create(sp1), Create(sp2), FadeIn(t1, shift=0.2 * DOWN), FadeIn(t2, shift=0.2 * DOWN),
                      run_time=1.2)
            c.wait_until("accepts it")
            self.play(FadeIn(fun_row, shift=0.2 * DOWN), FadeIn(fun_val, shift=0.2 * DOWN), Create(ok),
                      run_time=1.0)
            # "But whichever loop starts first never finishes, so the division never happens."
            c.wait_until("run")
            self.play(FadeIn(prompt, shift=0.2 * DOWN), FadeIn(cursor), FadeIn(clock), run_time=1.0)
            start_ticking(clock[2], clock_c)
            start_blink(cursor)
            c.wait_until("division never happens")
            self.play(restyle(slash, op=0.3), run_time=1.0)
            # "No bool ever turns up where an integer was expected."  "It runs forever, but it never goes wrong."
            c.wait_until("safe")
            self.play(FlashAround(g(h, "true"), color=GREEN, buff=0.08),
                      FlashAround(g(div_t, "int", 0), color=GREEN, buff=0.06), run_time=1.2)
            c.wait_until("never goes wrong")
            self.play(FlashAround(ok, color=GREEN), run_time=1.0)
            # "Give loop the type alpha to alpha, and this would be rejected."
            c.wait_until("contrast2")
            self.play(FadeOut(div_t), FadeOut(fun_row), FadeOut(fun_val), FadeOut(ok),
                      FadeIn(ghost), Create(ghost_box), run_time=1.0)
            c.wait_until("would be rejected")
            self.play(FadeOut(sp1), FadeOut(t1), Create(ul), FadeIn(err, shift=0.2 * DOWN), run_time=1.0)
        self.h, self.err, self.ticking = h, err, (clock[2], cursor)

    # c6.types.8: the guarantee, and Milner's slogan
    def guarantee(self):
        h, err = self.h, self.err
        card = RoundedRectangle(corner_radius=0.25, width=12.2, height=3.5)
        card.set_stroke(DIM, 2).set_fill(CARD_FILL, 1).move_to([0, 0.6, 0])
        mark = T("“", size=110, color=GOLD).move_to(card.get_corner(UL) + np.array([0.55, -0.55, 0]))
        quote = T("Well-typed programs cannot go wrong.", size=48, slant=ITALIC).move_to([0, 1.15, 0])
        who = T("Robin Milner, 1978", size=34).move_to([5.6, 0.05, 0], aligned_edge=RIGHT)
        src = T("A Theory of Type Polymorphism in Programming", size=28, color=DIM, slant=ITALIC)
        src.move_to([5.6, -0.5, 0], aligned_edge=RIGHT)
        cav1 = T("They might run forever, or raise an exception,", size=32, color=DIM).move_to([0, -1.75, 0])
        cav2 = T("but they never mix up their types.", size=36, color=GREEN).move_to([0, -2.45, 0])

        with self.say("c6.types.8") as c:
            # "That's the guarantee."  "Types are checked before the program runs, ..."
            c.wait_until("types are checked")
            self.play(FlashAround(err, color=RED, buff=0.12), run_time=1.4)
            # "... so no value can ever turn up with the wrong type."
            c.wait_until("no value")
            self.play(FlashAround(g(h, "true"), color=GREEN, buff=0.08), run_time=1.2)
            # "Robin Milner, who created ML, OCaml's ancestor, put it as a slogan."
            c.wait_until("quote")
            for m in self.ticking:
                m.clear_updaters()
            sweep_clear(self, time_span(AnimationGroup(FadeIn(card), FadeIn(mark, scale=0.7)), 0.4, 1.3),
                        time_span(FadeIn(who, shift=0.2 * LEFT), 0.8, 1.6),
                        time_span(FadeIn(src, shift=0.2 * LEFT), 0.9, 1.7), run_time=1.7)
            # "Well-typed programs cannot go wrong."
            c.wait_until("cannot go wrong")
            self.play(Write(quote), run_time=1.6)
            # "They might run forever, or raise an exception, but they never mix up their types."
            c.wait_until("caveat")
            self.play(FadeIn(cav1, shift=0.2 * UP), run_time=1.0)
            c.wait_until("never mix up")
            self.play(FadeIn(cav2, shift=0.2 * UP), run_time=1.0)
            self.last_born, self.last_len = self.time, len("They might run forever, or raise an exception,")
