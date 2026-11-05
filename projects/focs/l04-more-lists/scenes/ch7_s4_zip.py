"""Chapter 7, scene 4: Exercise 4.3, a stricter zip. Clips c7.zip.1 – c7.zip.4.

PLAN
  zip.1  ch6's strip fades in (4.1, 4.2 done, 4.3 current); card 4.3 grows out of its pill with
         ch6's text (In [74], its reply under the frame, the GOLD question tag). {diff}: the card
         lifts (its reply steps out); ch3's In [64] appears under it, dimmed; its `| _ -> []`
         turns YELLOW and a copy flies into In [74]'s `| ([], [])   -> []` (YELLOW); the `_`
         flashes on "wildcard". {stop}: pause tag top right, held to the end of the clip.
  zip.2  {warn}: the card shrinks back into its pill (stays CURRENT); OCaml's reply: the warning
         (Code 23, YELLOW, location lines left out) at the top, the val line (type GREEN) in the
         lower third. The example `(x::xs, [])` is boxed and flies out big into the middle,
         labelled "non-empty list" / "nil". {type}: ch3's identical reply slides in under it.
  zip.3  {equal}: the equal call, `- : (string * int) list =` and ch3's three tuple cells built
         from the call's names and numbers; GREEN ticks "old zip" / "new zip". {unequal}: dimmed.
         {trace}: In [74] at the top right (reference), the call drops to row 0 and loses its 47;
         row 1 is born ch3-style, the two waiting pairs GOLD. {fail}: Cleo and nil flash, both
         clauses get RED boxes and crosses, the RED Match_failure. {lost}: the waiting pairs
         dissolve; aside: the other way round raises the same exception.
  zip.4  {choice}: two blocks, "Forgiving" (old zip) on top, "Strict" (new zip) below: the trace's
         call, exception and aside move into the strict block (dimmed till {strict}); the
         forgiving call and its reply, Cleo DIM. {inverse}: both calls wrapped in unzip; strict's
         lists fly into its result (GREEN tick); forgiving dimmed, its Cleo RED. {design}: GOLD
         flashes on both titles and a GOLD "?"; on "a design choice" the blocks clear, the titles
         ride onto a balance and the "?" becomes the answer; GREEN "mismatch visible" / RED "can
         hide a bug" under the pans. The strip fades with the rest.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch6_s5_hints1 import (  # noqa: E402  the shared exercise-card kit (read-only)
    COL_X, CURRENT, DONE, EX43_QUESTION, EX43_REPLY, EX43_ZIP, PHONE_EQUAL, PHONE_SHORT, ROW0,
    TODO, ZIP3_SRC, ZIP74_WARNING, HeroCard, enter_card, finish, first_cue, hold_for,
    make_strip, pause_tag)
from scenes.ch3_s4_pairs import PairChain  # noqa: E402  ch3's tuple cells (value box 2.7 x 1.0, text 30)

# ── code and replies (verbatim, from the brief) ──────────────────────────────────
ZIP3_REPLY = "val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>"      # ch3, In [64]
TYPE_SUB = "'a list -> 'b list -> ('a * 'b) list"
EXAMPLE = "(x::xs, [])"
EQ_HEAD = "- : (string * int) list ="
PAIRS = [("Amy", 21), ("Bob", 35), ("Cleo", 47)]
ROW1 = '("Amy", 21) :: ("Bob", 35) :: zip ["Cleo"] []'
WAIT = ('("Amy", 21) ::', '("Bob", 35) ::')
CLEO_CALL = 'zip ["Cleo"] []'
EXC = 'Exception: Match_failure ("//toplevel//", 2, 2).'
SURPLUS = 'zip ["Amy"; "Bob"] [21; 35; 47]'
FORGIVE_REPLY = '- : (string * int) list = [("Amy", 21); ("Bob", 35)]'
UNZIP_SHORT = 'unzip (zip ["Amy"; "Bob"; "Cleo"] [21; 35])'
UNZIP_SHORT_REPLY = '- : string list * int list = (["Amy"; "Bob"], [21; 35])'
UNZIP_EQUAL = 'unzip (zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47])'
UNZIP_TYPE = "- : string list * int list ="
UNZIP_VAL = '(["Amy"; "Bob"; "Cleo"], [21; 35; 47])'
NAMES_L = '["Amy"; "Bob"; "Cleo"]'
NUMS_L = '[21; 35; 47]'

STATES = [DONE, DONE, CURRENT, TODO, TODO, TODO]

# ── layout ────────────────────────────────────────────────────────────────────
L = -6.4                    # left edge of full-width lines (a 55-character reply at 28 is 12.8)
# zip.2
WARN_Y = 1.99               # centre of the two warning lines (Code 23)
EX_Y = 0.55                 # the example, big
VAL_Y, OLD_Y = -1.35, -1.95
# zip.3
TS = 30                     # trace rows
EQ_CALL_Y, EQ_HEAD_Y, EQ_CHAIN_Y, EQ_TICK_Y = 1.95, 1.1, -0.35, -1.95
R0_Y, R1_Y, EXC_Y, ASIDE_Y = 0.0, -0.8, -1.8, -2.8
IMP_X = -6.05               # the => column
GAP = 0.22
# zip.4
BS = 28                     # block lines
F_T, F_1, F_2 = 2.3, 1.65, 1.05
S_T, S_1, S_2, S_3 = 0.0, -0.65, -1.25, -1.85
FDIM = 0.4
# the balance
BY, BX, HOOK, RIM, RH, PB = 1.35, 3.3, 1.1, -0.5, 2.0, -2.45
SAG = 0.69                  # pan arc angle (a 0.35 dip over 4.0)
LAB_Y = -1.45


# ── helpers ───────────────────────────────────────────────────────────────────
def G(code, sub, nth=0, line=None):
    return VGroup(*code.find(sub, line=line, nth=nth))


def book(code):
    """ch3's phone book colours: names YELLOW (numbers are GOLD already)."""
    for n in ("Amy", "Bob", "Cleo"):
        q = f'"{n}"'
        for k in range(code.src.count(q)):
            code.find(q, nth=k).set_color(YELLOW)
    return code


def implies():
    return MathTex(r"\Rightarrow", font_size=44, color=DIM)


def left_at(mob, x, y):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def step_bits(z, nth):
    """The tuple's ( , ) and the :: out of the step clause's `(x, y) ::` (ch3_s3's move)."""
    return [(G(z, "(", 1, line=2), "(", nth, 0.5), (G(z, ",", 1, line=2), ",", nth, 0.5),
            (G(z, ")", 1, line=2), ")", nth, 0.5), (G(z, "::", 2, line=2), "::", nth, 0.5)]


def title_pair(title, sub, y):
    t = left_at(T(title, size=40), L, y)
    s = T(sub, size=28, color=DIM).next_to(t, RIGHT, buff=0.35)
    s.shift(UP * (t[0].get_bottom()[1] - s[0].get_bottom()[1]))      # share the baseline
    return t, s


def balance():
    """A DIM balance: base, post, beam, and two pans hung on V strings. Returns (frame, pivot)."""
    parts = [Line([-1.1, PB, 0], [1.1, PB, 0]).set_stroke(DIM, 6),
             Line([0, PB, 0], [0, BY, 0]).set_stroke(DIM, 4),
             Line([-BX, BY, 0], [BX, BY, 0]).set_stroke(DIM, 5)]
    for x in (-BX, BX):
        parts += [Line([x, BY, 0], [x, HOOK, 0]).set_stroke(DIM, 4),
                  Line([x, HOOK, 0], [x - RH, RIM, 0]).set_stroke(DIM, 3),
                  Line([x, HOOK, 0], [x + RH, RIM, 0]).set_stroke(DIM, 3),
                  ArcBetweenPoints([x - RH, RIM, 0], [x + RH, RIM, 0], angle=SAG).set_stroke(DIM, 4)]
    pivot = Dot([0, BY, 0], radius=0.11, color=DIM)
    return VGroup(*parts), pivot


class StricterZip(NarratedScene):
    def construct(self):
        self.clip_card()        # c7.zip.1
        self.clip_warning()     # c7.zip.2
        self.clip_trace()       # c7.zip.3
        self.clip_choice()      # c7.zip.4
        hold_for(self, self.last_born, len("can hide a bug"))
        finish(self)            # the strip fades with the rest: an empty frame

    # ── shared move ───────────────────────────────────────────────────────────
    def birth(self, dst, pairs, extra=(), run_time=1.5, start=0.0):
        """`dst` is born from copies (source glyphs, dst substring, nth, path_arc); every glyph
        of dst not flown in fades in. Then dst is put back on screen as one object."""
        anims, targets, covered = [], [], set()
        for src, sub, nth, arc in pairs:
            t = G(dst, sub, nth)
            anims.append(TransformFromCopy(src, t, path_arc=arc))
            targets.append(t)
            covered |= {id(g) for g in t}
        rest = VGroup(*[g for g in dst.text if id(g) not in covered])
        if len(rest):
            anims.append(FadeIn(rest, shift=0.15 * DOWN))
            targets.append(rest)
        if start > 0:
            anims = [time_span(a, start, run_time) for a in anims]
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*targets, *dst.get_family())
        self.add(dst)

    # ── c7.zip.1: the card, and how it differs from chapter 3's zip ───────────────
    def clip_card(self):
        strip = self.strip = make_strip(STATES)
        zc = Code(EX43_ZIP, size=30)                                   # ch6's card 4.3, as built there
        card = HeroCard(2, height=0.84 + zc.height + 0.34)
        zc.move_to([COL_X, ROW0 - 0.38, 0], aligned_edge=UL)
        q_tag = card.tag(EX43_QUESTION, GOLD)
        card.lower(zc)
        reply = Code(EX43_REPLY, size=28).move_to([0, card.frame.get_bottom()[1] - 0.42, 0])
        ptag = pause_tag()

        # ch3's In [64], laid out under the lifted card (recursive zip YELLOW, as ch3 drew it)
        z3 = Code(ZIP3_SRC, size=30)
        z3.find("zip", line=2).set_color(YELLOW)
        z3.move_to([COL_X, card.bottom - 0.45, 0], aligned_edge=UL)
        z3.set_opacity(0.4)
        z3_lab = T("chapter 3", size=30, color=DIM)
        left_at(z3_lab, z3.line(0).get_right()[0] + 0.7, z3.line(0).get_y())

        with self.say("c7.zip.1") as c:
            # {card} "Exercise four point three."  Then a still beat.
            self.play(FadeIn(strip, lag_ratio=0.15), run_time=0.8)
            self.play(*enter_card(strip, card, light=False),
                      time_span(FadeIn(zc, shift=0.2 * DOWN), 0.5, 1.3),
                      time_span(FadeIn(reply, shift=0.2 * UP), 0.7, 1.4), run_time=1.4)

            # "How does this version of zip differ from the one in chapter three?"
            c.wait_until("differ")
            self.play(FadeIn(q_tag, shift=0.2 * DOWN), run_time=0.9)
            card.keep(zc, q_tag)

            # {diff} "Its last clause matches a pair of empty lists, where the old one had the wildcard."
            c.wait_until("diff")
            self.play(*card.lift(), time_span(FadeOut(reply), 0, 0.6),
                      time_span(FadeIn(z3, shift=0.2 * UP), 0.6, 1.4),
                      time_span(FadeIn(z3_lab, shift=0.2 * UP), 0.8, 1.4), run_time=1.4)
            c.wait_until("empty lists")
            old3, new3 = z3.line(3), zc.line(3)
            overlay = new3.copy().set_color(YELLOW)
            self.play(*[g.animate.set_color(YELLOW).set_opacity(1) for g in old3],
                      TransformFromCopy(old3, overlay, path_arc=-0.35),
                      *[time_span(a, 0.9, 1.7) for a in recolor(new3, YELLOW)],
                      run_time=min(1.8, max(1.0, 0.9 * c.until("wildcard"))))
            self.remove(overlay)
            c.wait_until("wildcard")
            self.play(FlashAround(G(z3, "_", line=3), color=YELLOW, time_width=1.5, buff=0.12),
                      run_time=1.1)

            # {stop} "Pause, and think it through."  Still to the end of the clip.
            c.wait_until("stop")
            self.play(FadeIn(ptag, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until()
        self.card, self.ptag, self.z3, self.z3_lab = card, ptag, z3, z3_lab

    # ── c7.zip.2: OCaml's reply: the warning, its example, the same type ─────────
    def clip_warning(self):
        card = self.card
        reply = Code(EX43_REPLY, size=28)            # the card's reply, back as OCaml's answer
        G(reply, TYPE_SUB).set_color(GREEN)
        left_at(reply, L, VAL_Y)

        warn = Code(ZIP74_WARNING, size=23)          # the location lines are left out
        ex_w = warn.find(EXAMPLE, line=1)
        warn.text.set_color(YELLOW)
        for g, r in zip(ex_w, Code(EXAMPLE, size=23).text):
            g.set_color(r.get_color())               # the example keeps its code colours
        left_at(warn, L, WARN_Y)
        hero = Code(EXAMPLE, size=48).move_to([0, EX_Y, 0])
        lab_ne = T("non-empty list", size=30)
        lab_ne.move_to([G(hero, "x::xs").get_x(), hero.get_bottom()[1] - 0.42, 0])
        lab_nil = T("nil", size=30, color=TEAL).move_to([G(hero, "[]").get_x(), 0, 0])
        lab_nil.align_to(lab_ne, UP)
        old = Code(ZIP3_REPLY, size=28)
        G(old, TYPE_SUB).set_color(GREEN)
        left_at(old, L, OLD_Y).set_opacity(0.6)
        old_lab = T("chapter 3", size=28, color=DIM).next_to(old, DOWN, buff=0.16)
        old_lab.align_to(old, RIGHT)

        with self.say("c7.zip.2") as c:
            # {warn} "OCaml accepts it, with a warning."  4.3 shrinks back into its pill.
            # (as ch7_s2: the frame lands on its pill, which stays CURRENT for the whole solution)
            self.play(*[FadeOut(m) for m in (*card.shown, self.ptag, self.z3, self.z3_lab)],
                      Transform(card.frame, self.strip[2].frame.copy()), run_time=1.2)
            self.remove(card.frame)
            c.wait_until("warning")
            self.play(FadeIn(warn, shift=0.2 * DOWN), time_span(FadeIn(reply, shift=0.2 * UP), 0.3, 1.2),
                      run_time=1.2)

            # "The match is not exhaustive, and OCaml gives an example it misses,
            #  a non-empty list paired with nil."
            c.wait_until("not exhaustive")
            self.play(FlashUnder(G(warn, "not exhaustive", line=0), color=YELLOW, time_width=1.5),
                      run_time=1.1)
            c.wait_until("gives an example")
            box = token_box(ex_w, warn.line(1), color=YELLOW, pad=0.16)
            self.play(FadeIn(box), TransformFromCopy(ex_w, hero), run_time=1.6)
            c.wait_until(first_cue(c, "non-empty list", "non empty list", "a non"))
            d = c.until("nil", floor=0.0)
            self.play(FadeIn(lab_ne, shift=0.25 * UP),
                      time_span(FadeIn(lab_nil, shift=0.25 * UP), max(0.4, d), max(0.4, d) + 0.7),
                      run_time=max(0.4, d) + 0.7)

            # {type} "The type is exactly the same as before."  ch3's reply slides in under it.
            c.wait_until("type")
            self.play(FadeIn(old, shift=0.5 * UP), time_span(FadeIn(old_lab, shift=0.2 * UP), 0.5, 1.2),
                      run_time=1.2)
        self.held = [hero, lab_ne, lab_nil, reply, old, old_lab]     # cleared a beat later

    # ── c7.zip.3: same on equal lists; the uneven trace fails ─────────────────────
    def clip_trace(self):
        strip = self.strip
        chain = PairChain(PAIRS).move_to([0, EQ_CHAIN_Y, 0])
        for cell in chain.cells:
            cell.name_part.set_color(YELLOW)
            cell.num_part.set_color(GOLD)
        call = left_at(book(Code(PHONE_EQUAL, size=TS)), chain.get_left()[0], EQ_CALL_Y)
        head = left_at(Code(EQ_HEAD, size=TS), chain.get_left()[0], EQ_HEAD_Y)
        ticks = VGroup()
        for x, s in ((-2.6, "old zip"), (2.6, "new zip")):
            ticks.add(VGroup(check_mark(GREEN), T(s, size=34)).arrange(RIGHT, buff=0.3).move_to([x, EQ_TICK_Y, 0]))

        imp_w = implies().width
        x0 = IMP_X + imp_w + GAP
        tz = Code(EX43_ZIP, size=28).move_to([6.4, 2.62, 0], aligned_edge=UR)   # In [74], reference
        r0 = left_at(book(Code(PHONE_SHORT, size=TS)), x0, R0_Y)
        r1 = book(Code(ROW1, size=TS))
        for w in WAIT:
            G(r1, w).set_color(GOLD)                 # the waiting conses
        left_at(r1, x0, R1_Y)
        arr = implies().next_to(r1, LEFT, buff=GAP).set_y(r1.get_y())
        exc = Code(EXC, size=TS)
        exc.text.set_color(RED)
        left_at(exc, IMP_X, EXC_Y)
        aside = VGroup(book(Code(SURPLUS, size=28)), implies(), T("same exception", size=30, color=RED))
        aside.arrange(RIGHT, buff=0.3)
        left_at(aside, x0, ASIDE_Y)

        def call_box(row, sub, color=BLUE):
            return token_box(G(row, sub), row, color=color, pad=0.16, height=0.5)

        def clause_box(sub, line, color):
            return token_box(G(tz, sub, line=line), tz.line(line), color=color, pad=0.2, height=0.5)

        with self.say("c7.zip.3") as c:
            # {equal} "On lists of equal length, the two versions behave the same."
            sweep_clear(self, time_span(FadeIn(call, shift=0.2 * DOWN), 0.5, 1.3),
                        keep=[strip, *self.held], run_time=1.3)
            anims = [time_span(FadeOut(m), 0.06 * i, 0.5 + 0.06 * i) for i, m in enumerate(self.held)]
            anims.append(time_span(FadeIn(head, shift=0.2 * DOWN), 0.4, 1.1))
            parts = []
            for i, (cell, (n, v)) in enumerate(zip(chain.cells, PAIRS)):
                s = 0.4 + 0.25 * i
                k = len(n) + 2
                rest = VGroup(cell.label[0], cell.label[1 + k], cell.label[-1])
                anims += [time_span(FadeIn(m), s, s + 0.7) for m in (cell.box, cell.ptr, cell.dot)]
                anims += [time_span(TransformFromCopy(G(call, f'"{n}"'), cell.name_part), s + 0.1, s + 1.2),
                          time_span(TransformFromCopy(G(call, str(v)), cell.num_part), s + 0.1, s + 1.2),
                          time_span(FadeIn(rest), s + 0.5, s + 1.2),
                          time_span(GrowArrow(chain.arrows[i]), s + 0.9, s + 1.4)]
                parts += [cell.name_part, cell.num_part, rest]
            anims.append(time_span(FadeIn(chain.nil), 1.7, 2.1))
            anims.append(time_span(FadeIn(ticks, lag_ratio=0.3), 1.9, 2.5))
            self.play(*anims, run_time=2.5)
            self.remove(*parts)
            settle(self, chain)

            # {unequal} "The difference is in unequal lengths."  Then still.
            c.wait_until("unequal lengths")
            self.play(*set_alpha([head, chain, ticks], 0.35), run_time=1.0)

            # {trace} "Go back to chapter three's phone book, and zip three names with only two numbers."
            c.wait_until("trace")
            call.generate_target()
            left_at(call.target, x0, R0_Y)
            self.play(*[time_span(FadeOut(m), 0, 0.8) for m in (head, chain, ticks)],
                      time_span(MoveToTarget(call), 0.2, 1.3),
                      time_span(FadeIn(tz, shift=0.2 * DOWN), 0.5, 1.5), run_time=1.5)
            c.wait_until("three names")
            self.play(FlashUnder(G(call, NAMES_L), color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("two numbers")
            self.birth(r0, [(G(call, PHONE_SHORT[:-1]), PHONE_SHORT[:-1], 0, 0),
                            (G(call, "]", 1), "]", 1, 0)],
                       extra=[FadeOut(call)], run_time=1.0)

            # "Amy and Bob pair up as before."  Row 1 is born; the two pairs wait (GOLD).
            c.wait_until("amy and bob")
            cbox = call_box(r0, PHONE_SHORT)
            lbox = clause_box("(x::xs, y::ys)", 2, BLUE)
            self.birth(r1, [(G(r0, '"Amy"'), '"Amy"', 0, -0.8), (G(r0, "21"), "21", 0, -0.8),
                            (G(r0, '"Bob"'), '"Bob"', 0, -0.8), (G(r0, "35"), "35", 0, -0.8),
                            *step_bits(tz, 0), *step_bits(tz, 1),
                            (G(r0, "zip ["), "zip [", 0, 0), (G(r0, '"Cleo"]'), '"Cleo"]', 0, 0),
                            (G(r0, "[", 1), "[", 1, 0), (G(r0, "]", 1), "]", 1, 0)],
                       extra=[time_span(FadeIn(cbox), 0, 0.5), time_span(FadeIn(lbox), 0, 0.5),
                              time_span(FadeIn(arr, shift=0.2 * DOWN), 0.6, 1.3)],
                       start=0.3, run_time=min(2.0, max(1.2, c.until("fail") - 0.1)))

            # {fail} "Then it's left with Cleo and nil, which no clause matches, so it raises Match failure."
            c.wait_until("cleo and nil")
            self.play(Transform(cbox, call_box(r1, CLEO_CALL)),
                      FlashAround(G(r1, '["Cleo"] []'), color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("no clause matches")
            lbox2 = clause_box("([], [])", 3, RED)
            crosses = [cross_mark(RED, r=0.14).move_to([tz.get_left()[0] - 0.4, tz.line(k).get_y(), 0])
                       for k in (2, 3)]
            self.play(Transform(lbox, clause_box("(x::xs, y::ys)", 2, RED)),
                      time_span(Create(crosses[0]), 0.2, 0.7),
                      time_span(FadeIn(lbox2), 0.5, 1.0), time_span(Create(crosses[1]), 0.7, 1.2),
                      run_time=1.3)
            c.wait_until("match failure")
            self.play(FadeIn(exc, shift=0.25 * DOWN), Transform(cbox, call_box(r1, CLEO_CALL, RED)),
                      run_time=1.1)

            # {lost} "The pairs it had already built are thrown away."
            c.wait_until("lost")
            gone = [*G(r1, WAIT[0]), *G(r1, WAIT[1])]
            n = len(gone)
            self.play(*[time_span(FadeOut(g, shift=0.45 * DOWN, scale=0.4), 0.7 * i / n, 0.7 * i / n + 0.9)
                        for i, g in enumerate(gone)], run_time=1.6)
            r1.text.remove(*gone)
            self.remove(*r1.get_family())
            self.add(r1)
            # aside: the other way round fails the same way (ch6's second hint input)
            self.play(FadeIn(aside, shift=0.2 * UP), run_time=min(1.0, max(0.5, c.remaining - 0.1)))
        self.trace = dict(tz=tz, r0=r0, r1=r1, arr=arr, cbox=cbox, lbox=lbox, lbox2=lbox2,
                          crosses=crosses, exc=exc, aside=aside)

    # ── c7.zip.4: forgiving or strict; unzip; a design choice ─────────────────────
    def clip_choice(self):
        k = self.trace
        r0, exc, aside = k["r0"], k["exc"], k["aside"]
        f_title, f_sub = title_pair("Forgiving", "old zip", F_T)
        s_title, s_sub = title_pair("Strict", "new zip", S_T)
        f_call = left_at(book(Code(PHONE_SHORT, size=BS)), L, F_1)
        f_rep = left_at(book(Code(FORGIVE_REPLY, size=BS)), L, F_2)
        for m, y in ((r0, S_1), (exc, S_2)):
            m.generate_target()
            m.target.scale(BS / TS)
            left_at(m.target, L, y).set_opacity(FDIM)
        aside.generate_target()
        left_at(aside.target, L, S_3).set_opacity(FDIM)

        f_call2 = left_at(book(Code(UNZIP_SHORT, size=BS)), L, F_1).set_opacity(FDIM)
        f_rep2 = left_at(book(Code(UNZIP_SHORT_REPLY, size=BS)), L, F_2).set_opacity(FDIM)
        s_call2 = left_at(book(Code(UNZIP_EQUAL, size=BS)), L, S_1)
        s_type = left_at(Code(UNZIP_TYPE, size=BS), L, S_2)
        s_val = left_at(book(Code(UNZIP_VAL, size=BS)), L, S_3)
        tick = check_mark(GREEN).next_to(s_val, RIGHT, buff=0.5)

        frame, pivot = balance()
        f_pan = f_title.copy().scale(38 / 40)
        f_pan.move_to([-BX, RIM + 0.1 + f_pan.height / 2, 0])
        s_pan = s_title.copy().scale(38 / 40)
        s_pan.move_to([BX, RIM + 0.1 + s_pan.height / 2, 0]).align_to(f_pan, DOWN)
        s_pan.shift(UP * (f_pan[0].get_bottom()[1] - s_pan[0].get_bottom()[1]))
        q = T("?", size=72, color=GOLD).move_to([0, -2.8, 0])          # under both blocks
        choice = T("a design choice", size=40).move_to([0, 2.15, 0])
        lab_s = T("mismatch visible", size=32, color=GREEN).move_to([BX, LAB_Y, 0])
        lab_f = T("can hide a bug", size=32, color=RED).move_to([-BX, LAB_Y, 0])

        with self.say("c7.zip.4") as c:
            # {choice} "So the old zip is forgiving."  The trace's results move into the strict
            # block (dimmed for now); the forgiving block opens on the same call.
            gone = [k["tz"], k["r1"], k["arr"], k["cbox"], k["lbox"], k["lbox2"], *k["crosses"]]
            self.play(*[time_span(FadeOut(m), 0, 0.7) for m in gone],
                      time_span(MoveToTarget(r0), 0.2, 1.4), time_span(MoveToTarget(exc), 0.25, 1.45),
                      time_span(MoveToTarget(aside), 0.3, 1.5),
                      time_span(TransformFromCopy(r0, f_call), 0.4, 1.6),
                      time_span(FadeIn(f_title, shift=0.2 * DOWN), 0.5, 1.3),
                      time_span(FadeIn(f_sub, shift=0.2 * DOWN), 0.7, 1.4), run_time=1.6)

            # "It quietly drops the surplus."  The pairs form; Cleo is left behind, DIM.
            c.wait_until("quietly")
            self.birth(f_rep, [(G(f_call, '"Amy"'), '"Amy"', 0, 0.4), (G(f_call, "21"), "21", 0, 0.4),
                               (G(f_call, '"Bob"'), '"Bob"', 0, 0.4), (G(f_call, "35"), "35", 0, 0.4)],
                       extra=[time_span(a, 1.0, 1.6) for a in recolor(G(f_call, '"Cleo"'), DIM)],
                       run_time=1.6)

            # {strict} "This one is strict, and rejects lists of different lengths."
            c.wait_until("strict")
            self.play(FadeIn(s_title, shift=0.2 * DOWN), FadeIn(s_sub, shift=0.2 * DOWN),
                      *[m.animate.set_opacity(1) for m in (r0, exc, aside)], run_time=1.1)
            c.wait_until("different lengths")
            self.play(FlashAround(exc, color=RED, time_width=1.5),
                      FlashAround(aside[2], color=RED, time_width=1.5), run_time=1.2)

            # {inverse} "In return, whenever it succeeds, unzip gives back exactly the two lists
            # you started with."  Both calls go into unzip; the forgiving block dims.
            c.wait_until("inverse")
            self.birth(f_call2, [(G(f_call, PHONE_SHORT), PHONE_SHORT, 0, 0)],
                       extra=[FadeOut(f_call), FadeOut(f_rep),
                              time_span(FadeIn(f_rep2, shift=0.15 * DOWN), 0.5, 1.4),
                              *[time_span(FadeOut(m), 0, 0.6) for m in (r0, exc, aside)],
                              time_span(FadeIn(s_call2, shift=0.15 * DOWN), 0.5, 1.5)],
                       run_time=1.6)
            c.wait_until("unzip gives back")
            self.birth(s_val, [(G(s_call2, NAMES_L), NAMES_L, 0, 0.5), (G(s_call2, NUMS_L), NUMS_L, 0, 0.5)],
                       extra=[FadeIn(s_type, shift=0.15 * DOWN)],
                       run_time=min(1.8, max(1.0, 0.9 * c.until("exactly"))))
            c.wait_until("exactly")
            self.play(Create(tick), FlashAround(s_val, color=GREEN, time_width=1.5),
                      *[g.animate.set_color(RED).set_opacity(1) for g in f_call2.find('"Cleo"')],
                      run_time=1.2)

            # {design} "Which one is better?"  The two titles flash; a GOLD "?".
            c.wait_until("design")
            self.play(FlashAround(f_title, color=GOLD, time_width=1.5),
                      FlashAround(s_title, color=GOLD, time_width=1.5),
                      FadeIn(q, scale=0.7), run_time=1.2)
            # "That's a design choice."  The blocks clear; the titles ride onto a balance and
            # the "?" becomes the answer.
            c.wait_until("a design choice")
            gone = [f_call2, f_rep2, s_call2, s_type, s_val, tick, f_sub, s_sub]
            self.play(*[time_span(FadeOut(m), 0.05 * i, 0.55 + 0.05 * i) for i, m in enumerate(gone)],
                      time_span(Create(frame, lag_ratio=0.12), 0.4, 1.7),
                      time_span(FadeIn(pivot), 0.8, 1.3),
                      time_span(Transform(f_title, f_pan), 0.4, 1.6),
                      time_span(Transform(s_title, s_pan), 0.4, 1.6),
                      time_span(FadeTransform(q, choice), 0.9, 1.9), run_time=1.9)
            # "Strict code makes a mismatch visible, and forgiving code can hide a bug."
            c.wait_until("mismatch")
            self.play(FadeIn(lab_s, shift=0.25 * UP), run_time=1.0)
            c.wait_until("forgiving code")
            self.play(FadeIn(lab_f, shift=0.25 * UP), run_time=1.0)
            self.last_born = self.time
