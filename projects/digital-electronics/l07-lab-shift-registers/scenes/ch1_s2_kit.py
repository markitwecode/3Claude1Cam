"""Chapter 1, scene 2: four kinds of chip, four workshops, one prototyping box. Clips c1.kit.1 – c1.kit.4.

Reusable: `prototyping_box()` draws the flat prototyping box (full screen, centred on ORIGIN);
ch1_s8's recap shows it small. `box_callouts(box)` builds this scene's callout labels for it.
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

CHIP_FILL = "#2A2F38"
PIN_OFF = "#5A5F68"
PIN_ON = "#C8CCD4"
BOARD_GREEN = "#1F5A35"
STRIP_GREEN = "#184A2B"
WHITE_BB = "#E6E6E0"
HOLE = "#A9A9A2"
LED_OFF = "#3A3530"
LED_ON = GOLD

HEX_SEGS = ["abcdef", "bc", "abdeg", "abcdg", "bcfg", "acdfg", "acdefg", "abc",
            "abcdefg", "abcdfg", "abcefg", "cdefg", "adef", "bcdeg", "adefg", "aefg"]
HEART = [".......", ".......", ".XX.XX.", "XXXXXXX", "XXXXXXX",
         ".XXXXX.", "..XXX..", "...X...", ".......", "......."]
BAR_PATTERN = "10110010"


# ---------------------------------------------------------------- small icons
def chip_icon(pins_per_side, pitch=0.22, h=0.8):
    """A DIP chip seen from above, pins top and bottom, notch on the left."""
    w = pins_per_side * pitch + 0.24
    body = Rectangle(width=w, height=h).set_fill(CHIP_FILL, 1).set_stroke(DIM, 3)
    pins = VGroup()
    for i in range(pins_per_side):
        x = -w / 2 + 0.12 + pitch * (i + 0.5)
        for s in (1, -1):
            pins.add(Rectangle(width=0.1, height=0.16).set_fill(PIN_OFF, 1).set_stroke(width=0)
                     .move_to([x, s * (h / 2 + 0.08), 0]))
    notch = Arc(radius=0.12, start_angle=-PI / 2, angle=PI).set_stroke(DIM, 2).move_to(body.get_left() + 0.06 * RIGHT)
    g = VGroup(pins, body, notch)
    g.body, g.pins, g.notch = body, pins, notch
    return g


def laptop_icon(scale=1.0):
    lid = RoundedRectangle(corner_radius=0.08, width=1.5, height=1.0).set_fill("#1A1E25", 1).set_stroke(FG, 2.5)
    lines = VGroup(*[Line(LEFT * 0.45, RIGHT * (0.45 - 0.25 * (i % 2)), stroke_width=3, color=DIM)
                     for i in range(3)]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(lid)
    base = Polygon([-0.9, 0, 0], [0.9, 0, 0], [0.75, 0.14, 0], [-0.75, 0.14, 0]) \
        .set_fill("#3A3F48", 1).set_stroke(FG, 2.5)
    base.next_to(lid, DOWN, buff=0.02)
    g = VGroup(lid, lines, base).scale(scale)
    g.lid, g.screen = lid, lines
    return g


def programmer_icon():
    box = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.9).set_fill(CHIP_FILL, 1).set_stroke(GOLD, 2.5)
    zif = Rectangle(width=0.9, height=0.34).set_fill("#1A1E25", 1).set_stroke(DIM, 2).move_to(box).shift(0.08 * UP)
    lever = Line(zif.get_right() + 0.08 * RIGHT, zif.get_right() + 0.08 * RIGHT + 0.3 * DOWN, stroke_width=4,
                 color=DIM)
    led = Dot(box.get_corner(DR) + 0.18 * UL, radius=0.05, color=GREEN)
    return VGroup(box, zif, lever, led)


def packet_icon():
    card = RoundedRectangle(corner_radius=0.05, width=0.55, height=0.4).set_fill(BG, 1).set_stroke(YELLOW, 2.5)
    lines = VGroup(*[Line(LEFT * 0.17, RIGHT * 0.17, stroke_width=2.5, color=YELLOW) for _ in range(3)]) \
        .arrange(DOWN, buff=0.08).move_to(card)
    return VGroup(card, lines).set_z_index(5)


def reprogram_arrow(radius=0.42):
    arc = Arc(radius=radius, start_angle=PI / 2 + 0.3, angle=TAU - 0.9).set_stroke(YELLOW, 5)
    arc.add_tip(tip_length=0.2)
    arc.get_tip().set_fill(YELLOW, 1).set_stroke(YELLOW, 1)
    return arc


def tip(*rows, stroke=DIM):
    """A callout: rows of text on a dark rounded card, so it reads over the board."""
    g = VGroup(*rows).arrange(DOWN, buff=0.1)
    box = RoundedRectangle(corner_radius=0.1, width=g.width + 0.3, height=g.height + 0.24) \
        .set_fill(BG, 0.9).set_stroke(stroke, 1.5).move_to(g)
    t = VGroup(box, g)
    t.box, t.rows = box, g
    return t


# ---------------------------------------------------------------- the prototyping box
def seg_digit(w=0.42, h=0.78, t=0.08):
    """Seven segments a..g (VGroup in that order), all unlit."""
    def hseg(y):
        return Rectangle(width=w - 0.06, height=t).move_to([0, y, 0])

    def vseg(x, y):
        return Rectangle(width=t, height=h / 2 - 0.06).move_to([x, y, 0])
    segs = VGroup(hseg(h / 2), vseg(w / 2, h / 4), vseg(w / 2, -h / 4), hseg(-h / 2),
                  vseg(-w / 2, -h / 4), vseg(-w / 2, h / 4), hseg(0))
    segs.set_fill(LED_OFF, 1).set_stroke(width=0)
    return segs


def show_hex(digit, n):
    on = HEX_SEGS[n % 16]
    for seg, name in zip(digit, "abcdefg"):
        seg.set_fill(LED_ON if name in on else LED_OFF, 1)


def breadboard(width=6.8, height=1.4):
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height).set_fill(WHITE_BB, 1).set_stroke(
        "#BDBDB5", 1.5)
    groove = Rectangle(width=width - 0.2, height=0.36).set_fill("#CFCFC8", 1).set_stroke(width=0)
    holes = VGroup()
    for dy in (0.3, 0.44, -0.3, -0.44):
        holes.add(DashedLine(LEFT * (width / 2 - 0.25), RIGHT * (width / 2 - 0.25), dash_length=0.05,
                             dashed_ratio=0.45, stroke_width=3, color=HOLE).shift(dy * UP))
    rail_top = Line(LEFT * (width / 2 - 0.25), RIGHT * (width / 2 - 0.25), stroke_width=2, color=RED) \
        .shift((height / 2 - 0.12) * UP)
    rail_bot = Line(LEFT * (width / 2 - 0.25), RIGHT * (width / 2 - 0.25), stroke_width=2, color=BLUE) \
        .shift((height / 2 - 0.12) * DOWN)
    g = VGroup(body, groove, holes, rail_top, rail_bot)
    g.body, g.groove, g.rail_top = body, groove, rail_top
    return g


def prototyping_box():
    """The lab's prototyping box, drawn flat, 12.4 x 7.0, centred on ORIGIN.

    Parts (attributes): board, top_strip, socket, pot, clock (.rate), push (3 buttons; [2] debounced),
    seg_housing, segs (2 digits of 7 segments a..g), bar_housing, bar (8 LEDs), matrix_housing,
    matrix (70 dots, 10 rows x 7, row-major from the top), strip (power strip), boards (3 breadboards),
    header (8 pins), switches (8, each VGroup(slot, lever), levers start right).
    Scale the whole VGroup for a recap: `prototyping_box().scale(0.4).to_corner(UL)`.
    """
    g = VGroup()
    board = RoundedRectangle(corner_radius=0.15, width=12.4, height=7.0).set_fill(BOARD_GREEN, 1) \
        .set_stroke("#2E7D4A", 3)
    top_strip = Rectangle(width=12.1, height=1.05).set_fill(STRIP_GREEN, 1).set_stroke(width=0).move_to([0, 2.9, 0])
    socket = VGroup(Circle(radius=0.2).set_fill("#111111", 1).set_stroke(GOLD, 2.5),
                    Dot(radius=0.06, color=GOLD)).move_to([-5.75, 2.9, 0])
    knob = Circle(radius=0.28).set_fill("#2A2F38", 1).set_stroke(FG, 2.5)
    pot = VGroup(knob, Line(ORIGIN, 0.24 * UP + 0.08 * RIGHT, stroke_width=4, color=FG)).move_to([-4.35, 2.9, 0])
    pot[1].move_to(knob.get_center() + 0.12 * UP + 0.04 * RIGHT)
    cbox = RoundedRectangle(corner_radius=0.06, width=1.7, height=0.75).set_fill(CHIP_FILL, 1).set_stroke(DIM, 2.5) \
        .move_to([-2.2, 2.9, 0])
    slot = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.22).set_fill("#111111", 1).set_stroke(DIM, 1.5) \
        .move_to(cbox.get_left() + 0.45 * RIGHT)
    slide = Rectangle(width=0.18, height=0.22).set_fill(FG, 1).set_stroke(width=0).move_to(slot.get_left() + 0.12 * RIGHT)
    rate = VGroup(slot, slide)
    led = Dot(cbox.get_right() + 0.3 * LEFT, radius=0.08, color=YELLOW)
    clock = VGroup(cbox, rate, led)
    clock.body, clock.rate, clock.led = cbox, rate, led
    push = VGroup(*[VGroup(Circle(radius=0.24).set_fill("#2A2F38", 1).set_stroke(FG, 2.5),
                           Circle(radius=0.13).set_fill(RED if i == 2 else BLUE, 1).set_stroke(width=0))
                    .move_to([3.9 + 0.8 * i, 2.9, 0]) for i in range(3)])

    seg_housing = RoundedRectangle(corner_radius=0.06, width=1.4, height=1.1).set_fill("#141414", 1) \
        .set_stroke(DIM, 2).move_to([-5.2, 1.25, 0])
    segs = VGroup(seg_digit().move_to([-5.51, 1.25, 0]), seg_digit().move_to([-4.89, 1.25, 0]))
    bar_housing = RoundedRectangle(corner_radius=0.05, width=1.5, height=0.36).set_fill("#141414", 1) \
        .set_stroke(DIM, 2).move_to([-5.2, 0.15, 0])
    bar = VGroup(*[Rectangle(width=0.11, height=0.22).set_fill(LED_OFF, 1).set_stroke(width=0)
                   for _ in range(8)]).arrange(RIGHT, buff=0.06).move_to(bar_housing)
    matrix_housing = RoundedRectangle(corner_radius=0.06, width=1.25, height=1.75).set_fill("#141414", 1) \
        .set_stroke(DIM, 2).move_to([-5.2, -1.6, 0])
    matrix = VGroup(*[Dot(radius=0.055, color=LED_OFF).move_to([-5.2 + 0.16 * (c - 3), -1.6 + 0.16 * (4.5 - r), 0])
                      for r in range(10) for c in range(7)])

    strip = RoundedRectangle(corner_radius=0.05, width=0.32, height=4.6).set_fill(WHITE_BB, 1) \
        .set_stroke("#BDBDB5", 1.5).move_to([-3.9, -0.5, 0])
    strip_holes = VGroup(DashedLine(UP * 2.15, DOWN * 2.15, dash_length=0.05, dashed_ratio=0.45, stroke_width=3,
                                    color=RED).shift(0.07 * LEFT),
                         DashedLine(UP * 2.15, DOWN * 2.15, dash_length=0.05, dashed_ratio=0.45, stroke_width=3,
                                    color=BLUE).shift(0.07 * RIGHT)).move_to(strip)
    strip_g = VGroup(strip, strip_holes)
    boards = VGroup(*[breadboard().move_to([0, y, 0]) for y in (1.1, -0.5, -2.1)])

    ys = [1.1 - 0.55 * i for i in range(8)]
    header = VGroup(*[Square(0.16).set_fill(PIN_OFF, 1).set_stroke(width=0).move_to([4.05, y, 0]) for y in ys])
    switches = VGroup()
    for y in ys:
        s = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.3).set_fill("#141414", 1).set_stroke(DIM, 2) \
            .move_to([5.2, y, 0])
        lv = Square(0.26).set_fill(FG, 1).set_stroke(width=0).move_to(s.get_right() + 0.17 * LEFT)
        switches.add(VGroup(s, lv))

    g.add(board, top_strip, socket, pot, clock, push, seg_housing, segs, bar_housing, bar,
          matrix_housing, matrix, strip_g, boards, header, switches)
    g.board, g.top_strip, g.socket, g.pot, g.clock, g.push = board, top_strip, socket, pot, clock, push
    g.seg_housing, g.segs, g.bar_housing, g.bar = seg_housing, segs, bar_housing, bar
    g.matrix_housing, g.matrix, g.strip, g.boards = matrix_housing, matrix, strip_g, boards
    g.header, g.switches = header, switches
    return g


def square_wave(width=1.3, height=0.26, periods=3, color=YELLOW):
    pts, p = [], width / periods
    for i in range(periods):
        x0 = -width / 2 + i * p
        pts += [[x0, -height / 2, 0], [x0, height / 2, 0], [x0 + p / 2, height / 2, 0],
                [x0 + p / 2, -height / 2, 0]]
    pts.append([width / 2, -height / 2, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, 3)


# ---------------------------------------------------------------- the scene
class KitScene(NarratedScene):
    def construct(self):
        self.kinds()
        self.workshops()
        self.box_tour()
        self.box_io()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c1.kit.1 ---------------------------------------------------------------
    def kinds(self):
        chips = [chip_icon(7), chip_icon(8), chip_icon(12), chip_icon(10)]
        xs = [-5.5, -2.8, 0.45, 4.55]
        for ch, x in zip(chips, xs):
            ch.scale(1.25).move_to([x, 0.9, 0])
        labels = [
            VGroup(T("Logic gates", 30), T("(SSI)", 30, color=DIM)),
            VGroup(T("counter chips", 30), T("(MSI)", 30, color=DIM)),
            VGroup(T("Memory devices", 30), T("(VLSI)", 30, color=DIM)),
            VGroup(T("Programmable array logic", 28), T("(PAL) type devices –", 28),
                   T("specifically Generic", 28), T("array logic (GAL)", 28)),
        ]
        for lb, ch in zip(labels, chips):
            lb.arrange(DOWN, buff=0.1).next_to(ch, DOWN, buff=0.45)
        gal = chips[3]

        with self.say("c1.kit.1", gap=1.4) as c:
            self.play(LaggedStart(*[FadeIn(ch, shift=0.2 * DOWN) for ch in chips], lag_ratio=0.25),
                      run_time=min(1.6, c.until("gates")))
            for ch, lb, cue in zip(chips, labels, ["gates", "counters", "memory", "gal"]):
                c.wait_until(cue)
                self.play(ch.body.animate.set_stroke(BLUE, 4), ch.pins.animate.set_fill(PIN_ON),  # early: the slide's wording, shown whole on its name
                          *appear(lb, lag=0.15), run_time=min(1.2, c.until(None)))
            c.wait_until("equations")

            # the GAL grows; its card appears with a laptop
            card_txt = VGroup(T("next-state logic", 34), T("as Boolean equations", 34)).arrange(DOWN, buff=0.12)
            card = VGroup(RoundedRectangle(corner_radius=0.12, width=card_txt.width + 0.6,
                                           height=card_txt.height + 0.5).set_fill(BG, 1).set_stroke(YELLOW, 2.5),
                          card_txt).move_to([3.4, 2.45, 0])
            lap = laptop_icon().move_to([3.4, 0.55, 0])
            others = chips[:3] + labels
            self.play(*during([FadeOut(m) for m in others], 0, 0.45),  # early: the card is read as the sentence runs
                      *during([gal.animate.scale(1.2).move_to([-4.0, 0.6, 0])], 0.2, 0.8),
                      *during([FadeIn(card, shift=0.2 * DOWN), FadeIn(lap)], 0.5, 1.0),
                      run_time=min(2.0, 0.8 * c.until("program")))
            c.wait_until("program")

            # programmer writes the equations into the chip
            prog = programmer_icon().move_to([0.0, 0.55, 0])
            prog_lbl = T("programmer", 28, color=DIM).next_to(prog, DOWN, buff=0.22)
            a1 = Arrow(lap.get_left(), prog.get_right(), buff=0.15, stroke_width=4, color=YELLOW)
            a2 = Arrow(prog.get_left(), gal.get_right(), buff=0.15, stroke_width=4, color=YELLOW)
            pk = packet_icon().move_to(lap.lid)
            path = VMobject().set_points_as_corners([lap.lid.get_center(), prog.get_center(), gal.get_center()])
            rt = max(1.6, min(2.6, c.until("wrong") - 0.1))
            self.play(time_span(FadeIn(prog), 0, 0.5), time_span(FadeIn(prog_lbl), 0.1, 0.6),
                      time_span(GrowArrow(a1), 0.4, 1.0), time_span(GrowArrow(a2), 0.9, 1.5),
                      time_span(FadeIn(pk), 0.3, 0.6),
                      time_span(MoveAlongPath(pk, path, rate_func=linear), 0.6, rt - 0.3),
                      time_span(FadeOut(pk), rt - 0.3, rt),
                      run_time=rt)
            self.remove(pk)

            c.wait_until("wrong")
            cross = cross_mark().scale(2.0).move_to(gal)
            self.play(GrowFromCenter(cross), run_time=0.7)
            rep_lbl = T("reprogram", 32, color=YELLOW)
            c.wait_until(own_word=rep_lbl)
            rep = reprogram_arrow().move_to([-4.0, -1.35, 0])
            rep_lbl.next_to(rep, RIGHT, buff=0.25)
            self.play(Create(rep), *appear(rep_lbl), run_time=1.0)
            tick = check_mark().scale(2.0).move_to(gal)
            c.wait_until("which is why")
            self.play(*swap(cross, tick), run_time=1.0)

            c.wait_until("stations")
            laps = VGroup(*[laptop_icon(0.62) for _ in range(3)]).arrange(RIGHT, buff=0.5).move_to([2.6, -1.9, 0])
            st_lbl = T("3 programming stations · Workshops 2 and 3", 30).next_to(laps, DOWN, buff=0.35)
            st_lbl.set_x(1.6)
            self.play(LaggedStart(*[FadeIn(lp, shift=0.2 * DOWN) for lp in laps], lag_ratio=0.25),
                      *appear(st_lbl), run_time=min(1.2, c.until(None)))

    # c1.kit.2 ---------------------------------------------------------------
    def workshops(self):
        data = [(1, "Electronic Die", ["gates", "counter"]),
                (2, "Shaft Position Encoder", ["GAL", "counter"]),
                (3, "Debouncing a Switch", ["gates", "counter", "GAL"]),
                (4, "Framestore for an LED Array", ["memory", "gates", "counter", "flip-flops"])]
        cards, heads, tags = [], [], []
        for (n, name, kinds), y in zip(data, [2.85, 1.65, 0.45, -0.75]):
            head = T(f"Workshop {n} – {name}", 30)
            tg = T(" · ".join(kinds), 28, color=DIM)
            VGroup(head, tg).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.1, width=8.4, height=1.05).set_stroke(BLUE, 2).set_fill(BG, 0)
            box.move_to([-2.4, y, 0])
            VGroup(head, tg).move_to(box).align_to(box, LEFT).shift(0.3 * RIGHT)
            cards.append(box)
            heads.append(head)
            tags.append(tg)
        for m in cards + heads:
            m.set_opacity(0.3)

        with self.say("c1.kit.2", gap=1.4) as c:
            sweep_clear(self, *[FadeIn(m) for m in cards + heads], run_time=min(1.6, c.until("w1")))  # early: the list shown whole, then walked
            for i, cue in enumerate(["w1", "w2", "w3", "w4"]):
                c.wait_until(cue)
                self.play(cards[i].animate.set_stroke(opacity=1), heads[i].animate.set_opacity(1),
                          *appear(tags[i]), run_time=min(1.0, c.until(None)))  # early: chip-kind tags go with their card

            prep = VGroup(T("no preparation ·", 28, color=GREEN), T("questions at the end", 28, color=GREEN)) \
                .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            prep.move_to(cards[0]).align_to(cards[0], LEFT).shift(8.6 * RIGHT)
            c.wait_until("prep")
            self.play(*appear(prep), FlashAround(cards[0], color=GREEN), run_time=1.2)

            brace = Brace(VGroup(*cards[1:]), direction=RIGHT, color=YELLOW, buff=0.15)
            before = VGroup(T("design work", 30, color=YELLOW), T("before the session", 30, color=YELLOW)) \
                .arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(brace, RIGHT, buff=0.25)
            c.wait_until("before")
            self.play(GrowFromCenter(brace), run_time=0.8)
            c.wait_until("design work")
            self.play(*appear(before), run_time=1.0)

            # the lab session bar, squeezed by design work
            c.wait_until("without")
            sess = T("lab session", 30, color=DIM).move_to([-5.75, -2.6, 0])
            bar = Rectangle(width=10.9, height=0.8).set_fill(GREEN, 0.22).set_stroke(GREEN, 2.5)
            bar.move_to([0.85, -2.6, 0])
            bt = T("build and test", 32, color=GREEN).move_to(bar)
            self.play(*appear(sess, bar, bt, lag=0.2), run_time=1.2)
            c.wait_until("designing")
            red = Rectangle(width=7.4, height=0.8).set_fill(RED, 0.25).set_stroke(RED, 2.5)
            red.align_to(bar, LEFT).set_y(bar.get_y())
            green2 = Rectangle(width=10.9 - 7.4, height=0.8).set_fill(GREEN, 0.22).set_stroke(GREEN, 2.5)
            green2.align_to(bar, RIGHT).set_y(bar.get_y())
            rt = T("design", 32, color=RED).move_to(red)
            self.play(*during([GrowFromEdge(red, LEFT), Transform(bar, green2)], 0, 0.8),
                      *during([bt.animate.move_to(green2)], 0, 0.55),
                      *during([FadeIn(rt)], 0.6, 1.0),
                      run_time=min(1.8, max(0.8, c.until(None) - 0.2)))

    # c1.kit.3 ---------------------------------------------------------------
    def box_tour(self):
        box = prototyping_box()
        self.box = box
        with self.say("c1.kit.3") as c:
            sweep_clear(self, FadeIn(box), run_time=min(1.8, c.until("psu")))

            c.wait_until("psu")
            plug = VGroup(Line([-6.6, 2.9, 0], [-6.15, 2.9, 0], stroke_width=8, color=DIM),
                          Rectangle(width=0.4, height=0.3).set_fill(GOLD, 1).set_stroke(width=0)
                          .move_to([-6.15, 2.9, 0])).shift(0.45 * LEFT)
            psu = T("PSU", 30)
            volts = T("5 V", 30, color=GOLD)
            VGroup(psu, volts).arrange(RIGHT, buff=0.3).move_to([-5.25, 2.05, 0])
            self.play(plug.animate.shift(0.45 * RIGHT + 0.0 * UP), *appear(psu, volts, lag=0.3),
                      run_time=min(1.5, c.until("boards")))
            self.plug = plug

            c.wait_until("boards")
            bls = [T("Breadboard", 30, color=BG).move_to(b.groove) for b in box.boards]
            self.play(*appear(*bls, lag=0.2), run_time=1.2)  # early: one label per board, all named at once

            c.wait_until("strip")
            sl = T("Power strip", 30).move_to([-2.2, -3.2, 0])
            sa = Arrow(sl.get_left(), box.strip.get_bottom() + 0.05 * UP, buff=0.1, stroke_width=3, color=FG)
            self.play(*appear(sl), GrowArrow(sa), FlashAround(box.strip, color=FG), run_time=1.2)

            c.wait_until("clock")
            ck = T("Clock", 30, color=YELLOW)
            ck.move_to([-0.9, 3.1, 0]).align_to([-0.95, 0, 0], LEFT)
            wave = square_wave().next_to(ck, RIGHT, buff=0.3)
            self.play(*appear(ck), Create(wave), box.clock.body.animate.set_stroke(YELLOW, 3), run_time=1.2)
            mf = T("manual / free-running", 28).move_to([0, 2.62, 0]).align_to(ck, LEFT)
            c.wait_until("You can set its rate")
            self.play(FlashAround(box.clock.rate, color=YELLOW), run_time=1.0)
            c.wait_until("step it by hand")
            self.play(*appear(mf), run_time=1.0)

            c.wait_until("push")
            pt = tip(T("Push switches", 30), T("2 plain + 1 debounced", 28)).move_to([4.55, 1.85, 0])
            self.play(*appear(pt), run_time=1.0)  # early: one callout, read with the sentence

    # c1.kit.4 ---------------------------------------------------------------
    def box_io(self):
        box = self.box
        sw0 = box.switches[0]
        with self.say("c1.kit.4") as c:
            lg = tip(T("8 Logic switches", 30, color=BLUE), stroke=BLUE).move_to([4.9, -3.2, 0])
            self.play(*appear(lg), *[s[0].animate.set_stroke(BLUE, 2.5) for s in box.switches],
                      run_time=min(1.2, c.until("left")))

            c.wait_until("left")
            v0 = tip(T("0 V = 0", 30)).move_to([2.55, 1.1, 0])
            self.play(sw0[1].animate.shift(0.46 * LEFT), box.header[0].animate.set_fill(DIM), run_time=0.8)
            self.play(*appear(v0), run_time=0.8)
            c.wait_until("right")
            v1 = tip(T("5 V = 1", 30, color=GOLD), stroke=GOLD).move_to(v0)
            self.play(sw0[1].animate.shift(0.46 * RIGHT), box.header[0].animate.set_fill(GOLD), run_time=0.8)
            self.play(*swap(v0, v1), run_time=1.0)

            c.wait_until("header")
            ic = chip_icon(4, pitch=0.26, h=0.5).move_to([1.95, -0.5, 0])
            ic.body.set_stroke(BLUE, 3)
            ic.pins.set_fill(PIN_ON)
            pin_top = ic.pins[6]   # top pin, rightmost
            hp = box.header[2].get_center()
            blue_w = VMobject().set_points_as_corners([hp, [pin_top.get_x(), hp[1], 0], pin_top.get_top()]) \
                .set_stroke(BLUE, 5)
            self.play(FadeIn(ic), run_time=0.7)
            self.play(Create(blue_w), run_time=1.0)
            tick = check_mark().move_to([3.25, 0.35, 0])
            self.play(GrowFromCenter(tick), run_time=0.6)
            c.wait_until("never")
            hp5 = box.header[5].get_center()
            rail_pt = [2.6, box.boards[2].rail_top.get_y(), 0]
            red_w = VMobject().set_points_as_corners([hp5, [2.6, hp5[1], 0], rail_pt]).set_stroke(RED, 5)
            cross = cross_mark().move_to([3.3, -1.25, 0])
            self.play(Create(red_w), run_time=0.9)
            self.play(GrowFromCenter(cross), run_time=0.6)

            c.wait_until("outputs")
            self.play(*disappear(ic, blue_w, tick, red_w, cross, v1), run_time=0.8)
            led = tip(T("LED Displays", 30, color=GREEN), stroke=GREEN).move_to([-5.42, -3.05, 0])
            self.play(*appear(led), box.seg_housing.animate.set_stroke(GREEN, 3),  # early: names the outputs the voice calls out
                      box.bar_housing.animate.set_stroke(GREEN, 3),
                      box.matrix_housing.animate.set_stroke(GREEN, 3), run_time=min(1.2, c.until("seven")))

            # the displays step 0..F; the bar shows a pattern; the matrix a small shape
            c.wait_until("seven")
            total = c.until("pot", floor=1.5)
            tb = c.until("bar", floor=0.1)
            tm = max(tb + 0.3, c.until("matrix", floor=0.1))
            lit_bar = [i for i, b in enumerate(BAR_PATTERN) if b == "1"]
            lit_mx = [r * 7 + col for r, row in enumerate(HEART) for col, ch in enumerate(row) if ch == "X"]
            lit_rows = sorted({i // 7 for i in lit_mx})

            def step(_, alpha):
                t = alpha * total
                n = min(15, int(alpha * 16))
                for d in box.segs:
                    show_hex(d, n)
                k = 0 if t < tb else min(len(lit_bar), int((t - tb) / 0.12) + 1)
                for j, b in enumerate(box.bar):
                    b.set_fill(LED_ON if j in lit_bar[:k] else LED_OFF, 1)
                rows = 0 if t < tm else min(len(lit_rows), int((t - tm) / 0.12) + 1)
                shown = set(lit_rows[:rows])
                for idx, dot in enumerate(box.matrix):
                    dot.set_fill(LED_ON if (idx in lit_mx and idx // 7 in shown) else LED_OFF, 1)
            self.play(UpdateFromAlphaFunc(box.segs, step), UpdateFromAlphaFunc(box.bar, lambda m, a: None),
                      UpdateFromAlphaFunc(box.matrix, lambda m, a: None), rate_func=linear, run_time=total)

            c.wait_until("pot")
            pl = tip(T("Potentiometer", 30)).move_to([-2.45, 2.08, 0])
            knob = box.pot[0]
            lead = Line(knob.get_center() + 0.3 * DOWN + 0.05 * RIGHT, pl.box.get_left() + 0.05 * UP,
                        stroke_width=2.5, color=FG)
            self.play(*appear(pl), Create(lead), FlashAround(box.pot, color=FG), run_time=1.0)
        self.wait(2.6)
