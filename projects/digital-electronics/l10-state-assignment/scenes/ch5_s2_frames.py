"""Chapter 5, scene 2: frame synchronisation, and the machine's inputs r and e. Clips c5.frames.1 – c5.frames.4.

Shared helpers (load_scene("ch5_s2_frames")), for s1's {stream} and s8's recap:
  bit_tape(bits=PLAIN) -> VGroup of 46 Mono digits along y=TY (pitch P, bit i at bx(i))
  FRAMED                -> PLAIN with PATTERN inserted at COPIES (1, 19, 37)
  pattern_box(i0)       -> YELLOW box round the 8 bits starting at i0
  r_trace(extra=()), e_trace() -> BLUE traces lined up under the tape (RY, EY); trace_label(name, y)
Link: L8 ch2_s3's link_parts (boxes, Serial Data wire, CLK), parallel I/O dropped.
Inset: L8 ch4_s5's sync_circuit(), loaded from its file, recoloured DIM.
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# Shared: the bit tape, the 8-bit pattern, the r / e traces
# =============================================================================================
P = 0.27                 # bit pitch
X0 = -5.85               # x of bit 0
TY = 2.45                # tape row
N = 46
PATTERN = "01111110"
COPIES = (1, 19, 37)     # pattern starts; each copy's last bit is s + 7 (8, 26, 44)
CHANCE = 10              # s4's chance copy (bits 10..17, inside the first frame)
PLAIN = "1011001010010110100110101001011001101001010011"
RY, EY = 0.95, 0.05      # trace rows
LOW = 1.5                # clips 1-2: the tape sits this much lower (frame balance), rises in clip 3
TR_H = 0.42


def bx(i):
    return X0 + i * P


def insert(bits, starts, pat=PATTERN):
    b = list(bits)
    for s in starts:
        b[s:s + len(pat)] = pat
    return "".join(b)


FRAMED = insert(PLAIN, COPIES)


def bit_digit(ch, i, y=TY, size=28, color=FG):
    return Mono(ch, size, color).move_to(_p(bx(i), y))


def bit_tape(bits=PLAIN, y=TY, size=28):
    return VGroup(*[bit_digit(ch, i, y, size) for i, ch in enumerate(bits)])


def pattern_box(i0, y=TY, color=YELLOW, n=8):
    return Rectangle(width=n * P + 0.08, height=0.5).set_stroke(color, 3).move_to(
        _p((bx(i0) + bx(i0 + n - 1)) / 2, y))


def pulse_trace(highs, y, color=BLUE, h=TR_H, width=4):
    """Square trace from bit 0 to bit N-1; high over each inclusive bit range (a, b)."""
    lo, hi = y - h / 2, y + h / 2
    pts = [_p(bx(0) - P / 2, lo)]
    for a, b in sorted(highs):
        xa, xb = bx(a) - P / 2, bx(b) + P / 2
        pts += [_p(xa, lo), _p(xa, hi), _p(xb, hi), _p(xb, lo)]
    pts.append(_p(bx(N - 1) + P / 2, lo))
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


def r_trace(extra=()):
    return pulse_trace([(s + 7, s + 7) for s in COPIES] + list(extra), RY)


def pulse_bump(i, y=RY, color=BLUE, h=TR_H, width=4):
    """One extra square pulse at bit i, drawn over a flat trace (a BG strip hides the low line under it)."""
    lo, hi = y - h / 2, y + h / 2
    xa, xb = bx(i) - P / 2, bx(i) + P / 2
    cover = Line(_p(xa, lo), _p(xb, lo)).set_stroke(BG, width + 4)
    bump = VMobject().set_points_as_corners([_p(xa, lo), _p(xa, hi), _p(xb, hi), _p(xb, lo)]).set_stroke(color, width)
    return VGroup(cover, bump)


def e_trace():
    return pulse_trace([(s + 6, s + 8) for s in COPIES], EY)


def trace_label(name, y):
    return Mono(name, 34, BLUE).move_to(_p(-6.45, y))


def due_column(i):
    """Invisible box round both traces at bit i (for flashes)."""
    top, bot = RY + TR_H / 2 + 0.08, EY - TR_H / 2 - 0.08
    return Rectangle(width=3 * P, height=top - bot).set_stroke(width=0).move_to(_p(bx(i), (top + bot) / 2))
# =============================================================================================


def l8_sync_circuit():
    f = Path(__file__).resolve().parents[2] / "l08-timing-metastability" / "scenes" / "ch4_s5_synchroniser.py"
    spec = importlib.util.spec_from_file_location("_l8_ch4_s5", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.sync_circuit()


def link_parts(by=0.3):
    """L8 ch2_s3's serial data link, parallel I/O dropped."""
    bw, bh = 3.2, 1.5
    lx, rx = -3.6, 3.6
    parts = []
    for x, a, b in ((lx, "Parallel in,", "serial out"), (rx, "Serial in,", "parallel out")):
        parts.append(Rectangle(width=bw, height=bh).set_stroke(FG, 4).move_to(_p(x, by)))
        parts.append(VGroup(T(a, 32), T(b, 32)).arrange(DOWN, buff=0.1).move_to(_p(x, by)))
    ser = Line(_p(lx + bw / 2, by), _p(rx - bw / 2, by)).set_stroke(GREEN, 5)
    ser_l = T("Serial Data", 30, GREEN).next_to(ser, UP, buff=0.32)
    cy = by - bh / 2 - 0.7
    clk = Line(_p(lx - 2.0, cy), _p(rx, cy)).set_stroke(YELLOW, 5)
    brs = [Line(_p(x, cy), _p(x, by - bh / 2)).set_stroke(YELLOW, 5) for x in (lx, rx)]
    jd = Dot(_p(lx, cy), radius=0.07, color=YELLOW)
    clk_l = T("CLK", 32, YELLOW).next_to(clk.get_start(), LEFT, buff=0.15)
    return parts + [ser, ser_l, clk, *brs, jd, clk_l], ser


class FrameSync(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c5.frames.1
    def clip1(self):
        with self.say("c5.frames.1") as c:
            link, ser = link_parts()
            self.play(*appear(*link, lag=0.08, shift=None), run_time=min(2.0, c.until("wire")))
            c.wait_until("wire")

            # bits leave the left box one at a time and run along the wire
            bits = "1011001010010110"
            x_l, x_r, y = ser.get_start()[0], ser.get_end()[0], ser.get_y()
            stream = VGroup(*[set_backstroke(Mono(ch, 34, FG)) for ch in bits])
            span = (x_r - x_l) + 0.5 * (len(bits) - 1) + 0.4

            def place(g, a):
                for k, d in enumerate(g):
                    x = x_l - 0.2 - 0.5 * k + a * span
                    d.move_to(_p(float(np.clip(x, x_l, x_r)), y))
                    op = float(np.clip(min(x - x_l, x_r - x) / 0.3, 0, 1))
                    d.set_opacity(op)
            place(stream, 0)
            self.add(stream)
            self.play(UpdateFromAlphaFunc(stream, place), run_time=c.until("plain", floor=1.0) - 0.15,
                      rate_func=linear)
            self.remove(stream)
            c.wait_until("plain")

            # zoom on the wire: the bits become the long, unmarked tape
            tape = list(bit_tape(PLAIN, y=TY - LOW))
            zc = ser.get_center()
            self.play(*during([m.animate.scale(2.2, about_point=zc).set_opacity(0) for m in link], 0, 0.45),
                      *during(appear(*tape, lag=0.02, shift=None), 0.45, 1), run_time=1.8)
            self.remove(*link)
            self.tape = tape
            c.wait_until("On its own")
            self.q = T("?", 72, YELLOW).move_to(_p(0, TY - LOW + 0.75))
            self.play(*appear(self.q), run_time=1.0)  # early: the question mark has no word

    # ------------------------------------------------------------------ c5.frames.2
    def clip2(self):
        with self.say("c5.frames.2") as c:
            self.play(*disappear(self.q), run_time=0.8)
            old, new, self.boxes = [], [], []
            for s in COPIES:
                old += self.tape[s:s + 8]
                nd = [bit_digit(PATTERN[k], s + k, y=TY - LOW) for k in range(8)]
                new += nd
                self.tape[s:s + 8] = nd
                self.boxes.append(pattern_box(s, y=TY - LOW))
            self.play(*swap(VGroup(*old), VGroup(*new)), run_time=1.4)
            self.play(*[GrowFromCenter(b) for b in self.boxes], run_time=1.0)
            c.wait_until("eight")
            tag = T("8 or 16 bits", 32, GOLD).next_to(self.boxes[1], UP, buff=0.25)
            self.play(*appear(tag), run_time=1.0)  # early: tag is the spoken "eight or sixteen"
            c.wait_until("frames")

            # frames: braces between consecutive copies
            self.braces, self.frame_ls = [], []
            for s in COPIES[:2]:
                a, b = s + 8, s + 17
                br = span_brace(_p(bx(a) - P / 2, TY - LOW - 0.22), _p(bx(b) + P / 2, TY - LOW - 0.22), DOWN,
                                color=DIM)
                lb = T("frame", 32).next_to(br, DOWN, buff=0.1)
                self.braces.append(br)
                self.frame_ls.append(lb)
            self.play(*[GrowFromCenter(b) for b in self.braces], run_time=1.2)
            self.play(*appear(*self.frame_ls, lag=0.3), run_time=1.0)
            c.wait_until("sync")

            # the receiver finds each copy as it arrives
            self.ticks = [check_mark().move_to(_p(b.get_x(), TY - LOW + 0.62)) for b in self.boxes]
            for k, (b, t) in enumerate(zip(self.boxes, self.ticks)):
                self.play(FlashAround(b, color=GREEN, run_time=0.9, time_width=1.5),
                          FadeIn(t, scale=0.6), *(disappear(tag) if k == 0 else []), run_time=0.9)
                self.wait(0.5)
            c.wait_until("That's frame")
            self.cap = T("frame synchronisation", 40, YELLOW).move_to(_p(0, -1.2))
            self.play(*appear(self.cap), run_time=1.0)
            c.wait_until("notL8")

            # not Lecture 8's synchroniser
            inset = l8_sync_circuit()
            inset.remove(*[m for m in inset.submobjects if isinstance(m, (Text, MathTex))])
            for f in (inset.ff0, inset.ff1):
                f.remove(f.d_l, f.q_l)
            for m in inset.get_family():
                if isinstance(m, Dot):
                    m.set_color(DIM)
                elif m.get_stroke_width() > 0:
                    m.set_stroke(DIM)
            inset.scale_to_fit_width(4.2).move_to(_p(3.7, -1.25))
            itag = T("Lecture 8: metastability", 30, DIM).next_to(inset, DOWN, buff=0.3)
            neq = MathTex(r"\neq", font_size=72, color=FG).move_to(_p(0.55, -1.2))
            self.play(*during([self.cap.animate.move_to(_p(-3.4, -1.2))], 0, 0.5),
                      *during(appear(neq, inset, itag, shift=None, lag=0.3), 0.5, 1), run_time=2.0)
            c.wait_until("Same word")
            self.wait(0.6)
            self.play(*during(disappear(inset, itag, neq), 0, 0.45),
                      *during([self.cap.animate.move_to(_p(0, -1.2))], 0.35, 1),
                      run_time=max(0.8, min(1.4, c.until())))

    # ------------------------------------------------------------------ c5.frames.3
    def clip3(self):
        with self.say("c5.frames.3") as c:
            BY = -2.75
            rec = Rectangle(width=2.4, height=1.0).set_stroke(FG, 4).move_to(_p(-4.4, BY))
            rec_l = T("receiver", 32).move_to(rec)
            sm = Rectangle(width=3.2, height=1.2).set_stroke(YELLOW, 4).move_to(_p(1.2, BY))
            sm_l = T("state machine", 32, YELLOW).move_to(sm)
            up = [m for m in (*self.tape, *self.boxes, *self.braces, *self.frame_ls)]
            self.play(*disappear(*self.ticks), *set_alpha([self.cap], 0.4), run_time=0.8)
            self.play(*[m.animate.shift(LOW * UP) for m in up], run_time=1.2)
            c.wait_until(own_word=rec_l)
            self.play(*appear(rec, rec_l, shift=None, lag=0.2), run_time=1.0)
            c.wait_until("machine")
            self.play(*appear(sm, sm_l, shift=None, lag=0.2), run_time=1.0)
            c.wait_until("r")

            # r: high for one bit as each copy's last bit arrives
            def wire(y, color=BLUE):
                return Line(_p(rec.get_right()[0], y), _p(sm.get_left()[0], y)).set_stroke(color, 5)
            r_w, e_w = wire(BY + 0.25), wire(BY - 0.25)
            r_wl = Mono("r", 32, BLUE).next_to(r_w, UP, buff=0.12)
            e_wl = Mono("e", 32, BLUE).next_to(e_w, DOWN, buff=0.12)
            self.r_tr, self.e_tr = r_trace(), e_trace()
            self.r_l, self.e_l = trace_label("r", RY), trace_label("e", EY)
            self.play(GrowFromEdge(r_w, LEFT), *appear(r_wl, self.r_l, shift=None), run_time=1.0)  # early: r is spoken as "ar"
            self.play(Create(self.r_tr), run_time=2.2, rate_func=linear)
            self.play(*flash([self.boxes[0], self.boxes[1], self.boxes[2]], color=BLUE, run_time=1.0))
            c.wait_until("e")

            # e: high in a short window at each due time
            self.play(GrowFromEdge(e_w, LEFT), *appear(e_wl, self.e_l, shift=None), run_time=1.0)  # early: e is spoken as "ee"
            self.play(Create(self.e_tr), run_time=2.2, rate_func=linear)
            c.wait_until("spacing")
            self.guides = [DashedLine(_p(bx(s + 7), TY - 0.3), _p(bx(s + 7), EY - TR_H / 2 - 0.12),
                                      dash_length=0.08).set_stroke(DIM, 2) for s in COPIES]
            self.play(*[Create(g) for g in self.guides], run_time=1.2)
            c.wait_until("s")

            # s: the machine's output
            s_w = Line(sm.get_right(), _p(4.9, BY)).set_stroke(GREEN, 5)
            s_l = Mono("s", 34, GREEN).next_to(s_w, RIGHT, buff=0.15)
            self.play(GrowFromEdge(s_w, LEFT), *appear(s_l, shift=None), run_time=1.0)  # early: s is spoken as "ess"
            self.play(VShowPassingFlash(s_w.copy().set_stroke(GREEN, 12), time_width=0.6),
                      s_w.animate.set_stroke(width=8), run_time=1.2)

    # ------------------------------------------------------------------ c5.frames.4
    def clip4(self):
        with self.say("c5.frames.4", gap=2.8) as c:
            self.play(*flash([self.e_l], color=BLUE, run_time=1.2))
            c.wait_until("chance")

            # a copy of the pattern turns up inside the data
            idx = [CHANCE + k for k in range(8) if PATTERN[k] != self.tape[CHANCE + k].text]
            old = [self.tape[i] for i in idx]
            new = [bit_digit(PATTERN[i - CHANCE], i) for i in idx]
            for i, d in zip(idx, new):
                self.tape[i] = d
            self.play(*swap(VGroup(*old), VGroup(*new), shift=None), run_time=1.3)
            rbox = pattern_box(CHANCE, color=RED)
            self.bump = pulse_bump(CHANCE + 7)
            self.play(GrowFromCenter(rbox), FadeIn(self.bump), run_time=1.2)
            c.wait_until("by chance")
            rtag = T("by chance", 30, RED).next_to(rbox, UP, buff=0.22)
            self.play(*appear(rtag), FlashAround(due_column(CHANCE + 7), color=RED, run_time=1.2,
                                                 time_width=1.5), run_time=1.2)
            c.wait_until("lock")

            # believing it would lock on to the wrong place
            a, b = CHANCE + 8, CHANCE + 17
            ghost = span_brace(_p(bx(a) - P / 2, TY + 0.22), _p(bx(b) + P / 2, TY + 0.22), UP, color=RED)
            ghost.set_opacity(0.6)
            wl = T("wrong frame", 30, RED).next_to(ghost, UP, buff=0.1)
            self.play(GrowFromEdge(ghost, LEFT), *appear(wl), run_time=1.3)
            c.wait_until("guard")

            # one sighting proves nothing: wait for the next copy, on time
            t1 = check_mark().move_to(_p(self.boxes[0].get_x(), TY + 0.62))
            self.play(FadeIn(t1, scale=0.6), FlashAround(self.boxes[0], color=GREEN, run_time=1.0,
                                                         time_width=1.5), run_time=1.0)
            c.wait_until("waits")
            t2 = check_mark().move_to(_p(self.boxes[1].get_x(), TY + 0.62))
            cap2 = T("seen, then seen again on time", 40, GREEN).move_to(self.cap)
            back = [bit_digit(PLAIN[i], i) for i in idx]
            for i, d in zip(idx, back):
                self.tape[i] = d
            self.play(*during(disappear(rbox, rtag, ghost, wl), 0, 0.5), *swap(VGroup(*new), VGroup(*back), shift=None),
                      *during([FadeOut(self.bump)], 0, 0.6), *swap(self.cap, cap2), run_time=1.4)
            c.wait_until("exactly")
            self.play(FadeIn(t2, scale=0.6), FlashAround(due_column(COPIES[1] + 7), color=GREEN, run_time=1.2,
                                                       time_width=1.5),
                      FlashAround(self.boxes[1], color=GREEN, run_time=1.2, time_width=1.5), run_time=1.2)
