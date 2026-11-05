"""Chapter 5, scene 8: recap in five panels, then a silhouette of Part 6 (one-hot). Clips c5.recap.1 – c5.recap.2.

Grid styled as ch4_s8_recap (ch2's slot frame / caption / veil look): "Recap" T 40 at (0, 3.4), five faint
DIM slot frames (two on top, three below, widths fitted to their pictures), each panel's line (T 28) under
its picture, earlier panels veiled.
 r1 s2's tape (bits 0..27 of FRAMED), two YELLOW pattern boxes 8 bit-spacings wide, BLUE r / e traces;
 r2 s3's diagram (sync_diagram(r=1.1), arc labels dropped, names fitted in the circles), Hunt -> Sight -> Sync lit;
 r3 s4's circles, GREEN codes [10] [00] [01], DIM [11], s = s1;
 r4 s5's sync_table (short titles, dropped), input X's boxed YELLOW, the unused row's next-state X X boxed DIM;
 r5 s6's D1 map and s7's D0 map (grid, entries, loops), the equations, the synchroniser's scoreboard row.
{next}: the tiles dim, the r3 circles fly back to the centre as s3's coded diagram, its codes fade, three
flip-flops labelled Hunt / Sight / Sync. {more}: GOLD "3 flip-flops". {easy}: a small DIM K-map, "no K-maps",
the arcs into Sync glow YELLOW.
End card (handover to ch6 s1): end_card() = that picture plus "Part 6 · One-hot, straight from the diagram"
(T 40, y 3.2); handover_shot() returns it.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

G2 = load_scene("ch2_s8_recap")          # veil
F2 = load_scene("ch5_s2_frames")         # bit_digit, pattern_box, FRAMED, COPIES, P, bx, trace_label
S3 = load_scene("ch5_s3_diagram")        # sync_diagram
S4 = load_scene("ch5_s4_twoffs")         # CODES
S5 = load_scene("ch5_s5_table")          # state_table, cell_box
S6 = load_scene("ch5_s6_d1")             # kmap4, loop4, term_eq, D1_*
S7 = load_scene("ch5_s7_d0")             # sync_board, D0_*
NL = load_scene("ch2_s6_nologic")        # make_ff
veil = G2.veil


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# the grid: (x0, x1, top, caption lines)
# =============================================================================================
SLOTS = ((-6.6, -0.2, 2.95, 1), (0.0, 6.6, 2.95, 1),
         (-6.6, -3.0, -0.4, 2), (-2.8, 1.8, -0.4, 1), (2.0, 6.6, -0.4, 1))
SLOT_H = 3.1
CAP = 28


def cap_top(i):
    x0, x1, top, n = SLOTS[i]
    return top - (2.62 if n == 1 else 2.25)


def slot_frame(i):
    x0, x1, top, _ = SLOTS[i]
    return (RoundedRectangle(corner_radius=0.15, width=x1 - x0, height=SLOT_H)
            .set_stroke(DIM, 2, opacity=0.45).move_to(_p((x0 + x1) / 2, top - SLOT_H / 2)))


def vis(i):
    """(centre, w, h) of slot i's picture area."""
    x0, x1, top, _ = SLOTS[i]
    t, b = top - 0.15, cap_top(i) + 0.12
    return _p((x0 + x1) / 2, (t + b) / 2), x1 - x0 - 0.3, t - b


def fit_slot(m, i, w=None, h=None, dy=0.0):
    c, W, H = vis(i)
    s = min((w or W) / m.width, (h or H) / m.height)
    m.scale(s).move_to(c + dy * UP)
    return s


def caption(i, lines):
    x0, x1, top, _ = SLOTS[i]
    g = VGroup(*[T(s, CAP) if isinstance(s, str) else s for s in lines]).arrange(DOWN, buff=0.1)
    return g.move_to(_p((x0 + x1) / 2, 0)).align_to(_p(0, cap_top(i)), UP)


# =============================================================================================
# panel pictures
# =============================================================================================
NB = 28                                   # r1 shows bits 0..27: copies at 1 and 19
R_Y, E_Y = -0.8, -1.45


def _trace(highs, y, h=F2.TR_H):
    P, bx = F2.P, F2.bx
    lo, hi = y - h / 2, y + h / 2
    pts = [_p(bx(0) - P / 2, lo)]
    for a, b in highs:
        xa, xb = bx(a) - P / 2, bx(b) + P / 2
        pts += [_p(xa, lo), _p(xa, hi), _p(xb, hi), _p(xb, lo)]
    pts.append(_p(bx(NB - 1) + P / 2, lo))
    return VMobject().set_points_as_corners(pts).set_stroke(BLUE, 4)


def tape_panel():
    bits = VGroup(*[F2.bit_digit(ch, i, y=0.0) for i, ch in enumerate(F2.FRAMED[:NB])])
    starts = [s for s in F2.COPIES if s + 8 <= NB]
    boxes = VGroup(*[F2.pattern_box(s, y=0.0).stretch_to_fit_width(8 * F2.P) for s in starts])
    rt = _trace([(s + 7, s + 7) for s in starts], R_Y)
    et = _trace([(s + 6, s + 8) for s in starts], E_Y)
    rl, el = F2.trace_label("r", R_Y), F2.trace_label("e", E_Y)
    g = VGroup(bits, boxes, rt, et, rl, el)
    g.bits, g.boxes, g.rt, g.et, g.rl, g.el = bits, boxes, rt, et, rl, el
    return g


DIAG_R = 1.15


def diagram_panel():
    d = S3.sync_diagram(r=DIAG_R)
    d.remove(*d.labels)
    return d


def fit_names(d, k, texts):
    """After fitting: grow each text toward 26 pt, but keep it inside its circle."""
    for t, circ in texts:
        s = min(27.5 / (32 * k), 1.66 * (circ.width / 2) / t.width)
        if s > 1:
            t.scale(s)


TRI = {"Sync": _p(-1.0, 0.63), "Hunt": _p(1.0, 0.63), "Sight": _p(0.0, -0.42)}
UNUSED_C = _p(1.55, -0.8)
TRI_R = 0.47


def codes_panel():
    circ, codes = {}, {}
    for n in S3.STATES:
        circ[n] = Circle(radius=TRI_R).set_stroke(FG, 4).move_to(TRI[n])
        codes[n] = Mono(f"[{S4.CODES[n]}]", 32, GREEN).move_to(TRI[n])
    uc = Circle(radius=TRI_R).set_stroke(DIM, 4).move_to(UNUSED_C)
    ut = Mono("[11]", 32, DIM).move_to(UNUSED_C)
    for t in (*codes.values(), ut):
        t.scale_to_fit_width(1.6 * TRI_R)
    g = VGroup(*circ.values(), *codes.values(), uc, ut)
    g.circle, g.code, g.ucirc, g.ucode = circ, codes, uc, ut
    return g


def table_panel():
    t = S5.state_table(titles=("s", "in", "next"), dim_rows=(8,))
    t.remove(t.titles)
    return t


def maps_panel():
    s = 0.4
    m1 = S6.kmap4(S6.D1_MAP, center=_p(-1.2, 0), scale=s)
    d0 = (("", "1", "1", ""), ("1", "1", "", ""), ("X", "X", "X", "X"), ("", "", "", ""))
    m0 = S6.kmap4(d0, center=_p(1.2, 0), scale=s)
    for m in (m1, m0):
        m.remove(m.col_heads, m.row_heads, m.corner, m.bars)
    for (r, k), col in zip(S6.D1_ESSENTIAL, S6.D1_COLORS):
        m1.ent[r][k].set_color(col)
    l1 = [S6.loop4(m1, cells, col, inset) for (cells, inset), col in zip(S6.D1_LOOPS, S6.D1_COLORS)]
    l0 = [S6.loop4(m0, S7.PINK_CELLS, PINK, 0.08), S6.loop4(m0, S7.PURPLE_CELLS, PURPLE, 0.08)]
    e1 = S6.term_eq("D_1", S6.D1_TERMS, S6.D1_COLORS, 0.0, 0.0, xs=(-2.05, 0.3, 2.8))
    e0 = S6.term_eq("D_0", S7.D0_TERMS, S7.D0_COLORS, 0.0, 0.0, xs=(-0.9, 1.75))
    row = S7.sync_board().sync_row.copy()
    row.arrange(RIGHT, buff=0.5)
    g = VGroup(m1, m0, *l1, *l0, e1, e0, row)
    g.m1, g.m0, g.l1, g.l0, g.e1, g.e0, g.row = m1, m0, l1, l0, e1, e0, row
    return g


# =============================================================================================
# Part 6 silhouette and the end card (ch6 s1 opens on end_card())
# =============================================================================================
NEXT_S = 0.68
NEXT_SHIFT = _p(-3.3, 0.15)
FF_XS = (1.95, 3.85, 5.75)
FF_Y = 0.95
FF_S = 0.52
GLOW = (6, 0, 1)                    # the arcs into Sync: Sight -> Sync and Sync's two loops


def next_diagram(codes=False, glow=False):
    d = S3.sync_diagram(codes=S4.CODES if codes else None)
    d.scale(NEXT_S, about_point=ORIGIN).shift(NEXT_SHIFT)
    for t in d.names:
        t.scale(min(27 / (32 * NEXT_S), 0.84 * d.circles[0].width / t.width))
    if glow:
        for i in GLOW:
            d.arcs[i].set_color(YELLOW)
    return d


def next_ffs():
    ffs, names = [], []
    for x, n in zip(FF_XS, ("Hunt", "Sight", "Sync")):
        f = NL.make_ff(ORIGIN, size=52)
        f.remove(f.clk_w, f.qb_w, f.qb_l)
        f.tri.scale(1.8, about_point=f.tri.get_bottom()).set_stroke(FG, 4)
        f.scale(FF_S, about_point=ORIGIN).shift(_p(x, FF_Y))
        ffs.append(f)
        names.append(T(n, 32, YELLOW).next_to(f.box, DOWN, buff=0.2))
    g = VGroup(*ffs, *names)
    g.ffs, g.names = ffs, names
    return g


def ff_tag():
    return T("3 flip-flops", 40, GOLD).move_to(_p(FF_XS[1], -1.0))


def no_kmap():
    m = S6.kmap4(None, center=_p(2.75, -2.55), scale=0.32)
    m.remove(m.col_heads, m.row_heads, m.corner, m.bars)
    m.set_stroke(DIM, 2)
    tag = T("no K-maps", 32, GREEN).next_to(m.grid, RIGHT, buff=0.4)
    return m, tag


def part6_line():
    return T("Part 6 · One-hot, straight from the diagram", 40).move_to(_p(0, 3.2))


def end_card():
    d = next_diagram(glow=True)
    ff = next_ffs()
    tag = ff_tag()
    m, mt = no_kmap()
    part = part6_line()
    g = VGroup(d, ff, tag, m, mt, part)
    g.diagram, g.ffs, g.tag, g.kmap, g.kmap_tag, g.part = d, ff, tag, m, mt, part
    return g


def handover_shot():
    return end_card()


# =============================================================================================
class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.end()

    def dim_previous(self):
        out = []
        for t in self.panels:
            if not getattr(t, "veiled", False):
                t.veiled = True
                v = veil(t)
                self.veils.append(v)
                out.append(FadeIn(v))
        return out

    def light(self, d, name, prev=None):
        anims = [restyle(d.circle[name], outline=YELLOW, width=6)]
        if prev:
            anims.append(restyle(d.circle[prev], outline=FG, width=4))
        return anims

    # -- c5.recap.1 -----------------------------------------------------------------------------
    def clip1(self):
        self.veils = []
        with self.say("c5.recap.1") as c:
            head = self.head = T("Recap", 40).move_to(_p(0, 3.4))
            frames = self.frames = [slot_frame(i) for i in range(5)]
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames],  # early: the scene's heading
                      run_time=min(1.2, c.until("r1")))

            # r1: the tape, the two boxed copies, then the traces
            c.wait_until("r1")
            tp = tape_panel()
            k = fit_slot(tp, 0)
            for t in (tp.rl, tp.el):
                t.scale(max(1.0, 28 / (34 * k)))
            cap1 = caption(0, ["known sequence, known spacing"])
            self.play(FadeIn(tp.bits), *[FadeIn(b) for b in tp.boxes], *appear(cap1, shift=None),  # early: panel shown whole
                      run_time=1.0)
            c.wait_until("known sequence")
            self.play(*flash(list(tp.boxes), time_width=1.5), run_time=min(1.5, c.until("known spacing")))
            c.wait_until("known spacing")
            self.play(Create(tp.rt), Create(tp.et), *appear(tp.rl, tp.el, shift=None),
                      run_time=min(1.5, c.until("r2", floor=0.8)))
            self.panels.append(VGroup(tp, cap1))

            # r2: the diagram; Hunt -> Sight -> Sync light in turn
            c.wait_until("r2")
            d = self.d2 = diagram_panel()
            k = fit_slot(d, 1)
            fit_names(d, k, [(d.name[n], d.circle[n]) for n in S3.STATES])
            cap2 = caption(1, ["seen once, then on time"])
            self.play(*self.dim_previous(), FadeIn(d), *appear(cap2, shift=None), run_time=1.0)  # early: panel shown whole
            c.wait_until("hunts")
            self.play(*self.light(d, "Hunt"), run_time=min(0.9, c.until("sights")))
            c.wait_until("sights")
            self.play(*self.light(d, "Sight", "Hunt"),
                      VShowPassingFlash(d.arcs[4].copy().set_stroke(YELLOW, 6), time_width=0.6),
                      run_time=min(1.0, c.until("moves to sync")))
            c.wait_until("moves to sync")
            self.play(*self.light(d, "Sync", "Sight"),
                      VShowPassingFlash(d.arcs[6].copy().set_stroke(YELLOW, 6), time_width=0.6),
                      run_time=min(1.0, c.until("on time")))
            c.wait_until("on time")
            self.play(*recolor([d.arcs[6]], YELLOW), run_time=min(0.9, c.until("r3", floor=0.5)))
            self.panels.append(VGroup(d, cap2))

            # r3: circles with their codes, the unused [11], s = s1
            c.wait_until("r3")
            cp = self.cp = codes_panel()
            fit_slot(cp, 2)
            cap3 = caption(2, ["two flip-flops,", MathTex("s", "=", "s_1", font_size=40, color=GREEN)])
            self.play(*self.dim_previous(), *[FadeIn(m) for m in (*cp.circle.values(), cp.ucirc)],  # early: panel shown whole
                      *appear(*cp.code.values(), cp.ucode, shift=None, lag=0.1), *appear(cap3[0], shift=None),
                      run_time=1.0)
            c.wait_until("two flip-flops")
            self.play(*flash(list(cp.code.values()), color=GREEN, time_width=1.5),
                      run_time=min(1.4, c.until("one zero")))
            c.wait_until("one zero")
            self.play(FlashAround(cp.code["Sync"], time_width=1.5), run_time=min(1.2, c.until("ess one")))
            c.wait_until("ess one")
            self.play(*appear(cap3[1]), run_time=min(1.0, c.until("r4", floor=0.5)))
            self.panels.append(VGroup(cp, cap3))

            # r4: the table; the input X's, then the unused row's next-state X X
            c.wait_until("r4")
            tb = table_panel()
            fit_slot(tb, 3)
            cap4 = caption(3, ["shorthand X, don't-care X"])
            self.play(*self.dim_previous(), FadeIn(tb), *appear(cap4, shift=None), run_time=1.0)  # early: panel shown whole
            c.wait_until("under the inputs")
            ins = [tb.cell(0, 1, 0), tb.cell(1, 1, 0), tb.cell(2, 1, 1), tb.cell(5, 1, 1)]
            boxes = [S5.cell_box([m], buff=0.05) for m in ins]
            self.play(*[FadeIn(b) for b in boxes], run_time=min(1.0, c.until("next state")))
            c.wait_until("next state")
            xbox = S5.cell_box([tb.rows[8][2]], color=DIM, buff=0.05)
            self.play(FadeIn(xbox), FlashAround(tb.rows[8][2], color=FG, time_width=1.5),
                      run_time=min(1.3, c.until("r5", floor=0.5)))
            self.panels.append(VGroup(tb, *boxes, xbox, cap4))

            # r5: the two maps, their loops and equations, the scoreboard row
            c.wait_until("r5")
            mp = maps_panel()
            c5, W5, H5 = vis(4)
            maps = VGroup(mp.m1, mp.m0)
            eqs = VGroup(mp.e1, mp.e0)
            eqs.scale(min(W5 / mp.e1.width, 0.6))
            mp.e0.align_to(mp.e1, LEFT)
            mp.row.scale(min(1.0, W5 / mp.row.width))
            top5, bot5 = c5[1] + H5 / 2, c5[1] - H5 / 2
            mp.row.move_to(_p(c5[0], bot5 + 0.14 + mp.row.height / 2))   # clear of the caption
            mp.e0.next_to(mp.row, UP, buff=0.14).set_x(c5[0] + (mp.e0.get_x() - eqs.get_x()))
            mp.e1.next_to(mp.e0, UP, buff=0.1).align_to(mp.e0, LEFT)
            eqs.set_x(c5[0])
            grp = VGroup(maps, *mp.l1, *mp.l0)
            room = top5 - mp.e1.get_top()[1] - 0.12
            grp.scale(room / maps.height).move_to(_p(c5[0], top5 - room / 2))
            cap5 = caption(4, ["D1, D0: seven gates"])
            self.play(*self.dim_previous(), FadeIn(mp.m1), FadeIn(mp.m0), *appear(cap5, shift=None),  # early: panel shown whole
                      run_time=1.0)
            c.wait_until("unused row")
            xr = [VGroup(m.sq(2, 0), m.sq(2, 3)) for m in (mp.m1, mp.m0)]
            self.play(*[FlashAround(x, color=YELLOW, time_width=1.5) for x in xr],
                      run_time=min(1.3, c.until("dee one")))
            c.wait_until("dee one")
            self.play(*[Create(lp) for lp in mp.l1], *appear(mp.e1, shift=None),
                      run_time=min(1.4, c.until("dee zero")))
            c.wait_until("dee zero")
            self.play(*[Create(lp) for lp in mp.l0], *appear(mp.e0, shift=None),
                      run_time=min(1.4, c.until("seven gates")))
            c.wait_until("seven gates")
            self.play(*appear(mp.row, shift=None), run_time=min(1.0, c.until(floor=0.5)))
            if c.remaining > 1.0:
                self.play(FlashAround(mp.row[2], time_width=1.5), run_time=min(1.2, c.remaining))
            self.panels.append(VGroup(mp, cap5))

    # -- c5.recap.2: one-hot next time -----------------------------------------------------------------
    def clip2(self):
        cp = self.cp
        src = VGroup(*cp.circle.values(), *cp.code.values())
        rest = [m for m in self.mobjects if m is not cp]
        dst = next_diagram(codes=True)
        ff = self.ff = next_ffs()
        with self.say("c5.recap.2") as c:
            self.play(*set_alpha(rest, DIMMED), run_time=min(0.8, c.until("same machine")))
            c.wait_until("same machine")
            self.play(*during(disappear(*rest, cp.ucirc, cp.ucode), 0, 0.35),
                      *during(fly(src, dst), 0.3, 1.0), run_time=min(1.6, c.until("more", floor=1.0)))
            self.remove(*cp.get_family())
            c.wait_until("more")
            self.play(*disappear(*[dst.code[n] for n in S3.STATES]),
                      *during(appear(*ff.ffs, shift=None, lag=0.15), 0.3, 1.0),
                      *during(appear(*ff.names, lag=0.15), 0.45, 1.0),
                      run_time=min(1.3, c.until("third flip-flop", floor=0.8)))
            for n in S3.STATES:
                dst.remove(dst.code[n])
            self.dg = dst
            c.wait_until("third flip-flop")
            tag = self.tag = ff_tag()
            self.play(*appear(tag), FlashAround(ff.ffs[2].box, color=GOLD, time_width=1.5),
                      run_time=min(1.3, c.until("easy", floor=0.8)))
            c.wait_until("easy")
            m, mt = self.km, self.kt = no_kmap()
            self.play(FadeIn(m), run_time=min(1.0, c.until("straight from the diagram")))
            c.wait_until("straight from the diagram")
            self.play(*recolor([dst.arcs[i] for i in GLOW], YELLOW),
                      *[VShowPassingFlash(dst.arcs[i].copy().set_stroke(YELLOW, 7), time_width=0.6) for i in GLOW],
                      run_time=min(1.4, c.until("no K-maps")))
            c.wait_until("no K-maps")
            self.play(*appear(mt), run_time=min(1.0, c.until(floor=0.6)))

    # -- end card: the part line, held while the music carries it --------------------------------------
    def end(self):
        part = part6_line()
        self.play(*appear(part, shift=None), run_time=1.2)   # fades in place: no faint moving glyphs
        self.remove(*self.mobjects)
        self.add(handover_shot())             # the same picture, as one object (ch6 s1 opens on it)
        self.wait(7.0)
