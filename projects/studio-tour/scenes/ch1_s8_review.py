"""Chapter 1, scene 8: review, the final cut, and the recap. Clips c1.review.1 – c1.review.4, c1.recap.1.

Shared pieces copied (never imported) from earlier ch1 scenes:
  checklist  CHECK_* + build_checklist() from ch1_s5_director (items only; the orient sub-label is
             left out, it would run into the workspace)
  lint page  s6's dwell output page (page6 + the same Mono 18 lines), shown small
  recap      s3 ladder + PLAN.md tick, s3 struck line, s4 timeline + vk voice, s5 checklist,
             s6 loop ring + s7 cue pin/block, own holds crop + film strip, s2 conveyor of pages
End shot: s2's master shot (current version: row labels T 26.5, separate DIM "×N" tags) with a GOLD
token mark (ch2_s1_hook token_mark) on every BLUE box, plus "Next: …" T 34 at y=-2.5.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# Manim CE 0.22's Camera.display_image_mobject pastes into Image.fromarray(np.zeros((h, w)),
# mode="RGBA"), which Pillow 13 rejects ("Invalid mode for data type"), so no ImageMobject
# renders. Shim just that call (a blank RGBA canvas, which is what it meant) for this module.
def _patch_image_canvas():
    import manim.camera.camera as cam
    from PIL import Image as PILImage

    class _ImageShim:
        def __getattr__(self, name):
            return getattr(PILImage, name)

        @staticmethod
        def fromarray(arr, mode=None):
            if mode == "RGBA" and getattr(arr, "ndim", 0) == 2:
                return PILImage.new("RGBA", (arr.shape[1], arr.shape[0]), (0, 0, 0, 0))
            return PILImage.fromarray(arr, mode=mode) if mode else PILImage.fromarray(arr)

    if cam.Image is PILImage:
        cam.Image = _ImageShim()


_patch_image_canvas()

HOLDS = Path(__file__).resolve().parent.parent / "source" / "figures" / "ch4_holds.png"
HOLDS_W, HOLDS_H = 1720, 1948
CROP_Y0, CROP_Y1 = 244, 729          # rows 2 and 3 of the 8 (c4.code.3 … c4.cells.2)
CROP_PH = CROP_Y1 - CROP_Y0
TRACE_TILES = [(3, 0), (0, 1), (1, 1)]   # (col, row in crop): c4.trace.1, .2, .3
CELLS1 = (2, 1)


def crop_image():
    arr = np.asarray(Image.open(HOLDS).convert("RGBA").crop((0, CROP_Y0, HOLDS_W, CROP_Y1)))
    return ImageMobject(arr)


def tile_rect(img, col, row, color=YELLOW, width=4):
    """Frame round one tile of the crop image `img` (any size/position)."""
    u = img.width / HOLDS_W
    x0 = img.get_left()[0] + col * 431 * u
    y0 = img.get_top()[1] - row * 244 * u
    r = Rectangle(width=427 * u, height=240 * u).set_stroke(color, width).set_fill(opacity=0)
    return r.move_to([x0 + 427 * u / 2, y0 - 240 * u / 2, 0])


# ---------------------------------------------------------------- s2 shared look (master shot)
ROW = 26.5


def agent(w, h, label=None, size=30, mono=False, outline=BLUE, fill_op=0.15, label_color=FG):
    back = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(width=0).set_fill(BG, 1)
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(outline, 3).set_fill(BLUE, fill_op)
    g = VGroup(back, rect)
    if label:
        t = (Mono if mono else T)(label, size=size, color=label_color)
        if t.width > w - 0.3:
            t.scale_to_fit_width(w - 0.3)
        g.add(t)
    return g


def builder_box(w, h):
    return RoundedRectangle(corner_radius=min(0.15, h / 3), width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)


def page(w, h, color=TEAL, fill_op=0.1, stroke=3):
    f = min(w, h) * 0.28
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0])
    body.set_stroke(color, stroke).set_fill(color, fill_op)
    corner = VMobject().set_points_as_corners([[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0],
                                               [w / 2, h / 2 - f, 0]])
    corner.set_stroke(color, max(1.5, stroke - 1))
    return VGroup(body, corner)


def page_pair(w=0.6, h=0.75, two=True):
    if not two:
        return VGroup(page(w, h))
    back = page(w, h).shift(0.12 * UP + 0.12 * RIGHT)
    front = page(w, h)
    front.add_to_back(page(w, h)[0].set_stroke(width=0).set_fill(BG, 1))
    return VGroup(back, front)


def row_xs(cx, n, w, gap):
    pitch = w + gap
    return [cx + (i - (n - 1) / 2) * pitch for i in range(n)]


def conn(a, b, width=2):
    return Line(a.get_bottom(), b.get_top()).set_stroke(DIM, width).set_z_index(-1)


def master_shot():
    you = T("you", size=36, color=YELLOW).move_to([0, 3.4, 0])
    producer = agent(3.2, 0.8, "producer", 32).move_to([0, 2.45, 0])
    planner = agent(2.8, 0.7, "series-planner", ROW).move_to([-5.1, 1.0, 0])
    writers = VGroup(*[agent(2.8, 0.7, "script-writer" if k == 0 else None, ROW)
                       .move_to([-1.7 + 0.1 * k, 1.0 + 0.1 * k, 0]) for k in (2, 1, 0)])
    voice = agent(2.8, 0.7, "vk voice", ROW, mono=True, outline=DIM, label_color=DIM).move_to([1.7, 1.0, 0])
    dir_back = VGroup(*[agent(2.8, 0.7, None, 28, outline=DIM, fill_op=0.06)
                        .move_to([5.1 + 0.08 * k, 1.0 + 0.08 * k, 0]) for k in (2, 1)])
    dir_front = agent(2.8, 0.7, "chapter-director", ROW).move_to([5.1, 1.0, 0])
    builders = [builder_box(0.75, 0.45).move_to([x, -0.5, 0]) for x in row_xs(3.0, 8, 0.75, 0.15)]
    brow = VGroup(*builders)
    blabel = T("scene-builder × 6–8", size=28, color=DIM).move_to([3.0, -1.05, 0])
    top_conns = VGroup(Line(you.get_bottom() + 0.05 * DOWN, producer.get_top()).set_stroke(DIM, 2).set_z_index(-1),
                       *[conn(producer, b) for b in (planner, writers[-1], voice, dir_front)])
    bconn = VGroup(*[conn(dir_front, b) for b in builders])
    wfront = writers[-1]
    w_n = T("×N", size=ROW, color=DIM)
    w_n.move_to([wfront.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
    d_n = T("×N", size=ROW, color=DIM)
    d_n.move_to([dir_front.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
    tree = VGroup(top_conns, bconn, you, producer, planner, writers, voice, dir_back, dir_front, brow, blabel, w_n, d_n)
    blue = [producer[1], planner[1], *[w[1] for w in writers], dir_front[1]]
    return tree, blue, builders


def token_mark(box_rect, scale=1.0):
    d = VGroup(Circle(radius=0.15, color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=2),
               Circle(radius=0.07, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0))
    d.scale(scale).move_to(box_rect.get_corner(UR))
    d.set_z_index(3)
    return d


# ---------------------------------------------------------------- s5 checklist
CHECK_NUM_X = -6.3
CHECK_NAME_X = -5.85
CHECK_SIZE = 34
CHECK_Y = [2.74, 0.9, 0.22, -0.46, -1.14, -1.82, -2.5]
CHECK_NAMES = ["orient", "narration fixes", "music", "builders", "review", "final", "record"]
CHECK_SUB_SIZE = 28
CHECK_SUB_Y = [2.27, 1.87, 1.47]
CHECK_SUB = ["vk status", "PLAN.md · STATUS.md", "script, once"]


def build_sub():
    sub = VGroup()
    for s_, y in zip(CHECK_SUB, CHECK_SUB_Y):
        m = Mono(s_, size=CHECK_SUB_SIZE, color=DIM)
        m.move_to([CHECK_NAME_X + m.width / 2, y, 0])
        sub.add(m)
    return sub


def build_checklist():
    items = []
    for i, (name, y) in enumerate(zip(CHECK_NAMES, CHECK_Y)):
        num = T(str(i + 1), size=CHECK_SIZE, color=DIM).move_to([CHECK_NUM_X, y, 0])
        nm = T(name, size=CHECK_SIZE, color=DIM)
        nm.move_to([CHECK_NAME_X + nm.width / 2, y, 0])
        nm.align_to(num, DOWN)
        items.append(VGroup(num, nm))
    return items


# ---------------------------------------------------------------- s6 pieces
AGENT_FILL = interpolate_color(ManimColor(BG), ManimColor(BLUE), 0.15)
TOOL_FILL = interpolate_color(ManimColor(BG), ManimColor(DIM), 0.15)


def node6(label, w, kind="agent", size=28):
    if kind == "agent":
        r = RoundedRectangle(corner_radius=0.15, width=w, height=0.8).set_stroke(BLUE, 3).set_fill(AGENT_FILL, 1)
        t = T(label, size)
    else:
        r = RoundedRectangle(corner_radius=0.15, width=w, height=0.8).set_stroke(DIM, 3).set_fill(TOOL_FILL, 1)
        t = Mono(label, size)
    t.move_to(r)
    return VGroup(r, t)


def page6(w, h, color=TEAL, fold=0.28):
    f = min(fold, h / 2)
    pts = [(-w / 2, h / 2), (w / 2 - f, h / 2), (w / 2, h / 2 - f), (w / 2, -h / 2), (-w / 2, -h / 2)]
    body = Polygon(*[[x, y, 0] for x, y in pts]).set_stroke(color, 3)
    body.set_fill(interpolate_color(ManimColor(BG), ManimColor(color), 0.12), 1)
    crease = VMobject().set_points_as_corners(
        [[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0]]).set_stroke(color, 3)
    return VGroup(body, crease)


def lint_page():
    dw = lambda a, b, d: [f"  dwell: t= {a} '{b}' shown {d} (needs 4.1)",  # noqa: E731
                          "        FadeOut during c4.trace.2 @" + (
                              '11.9s "…from the inside out."' if a == "36.6"
                              else '12.9s "…out. Three onto four,"')]
    l1 = dw("36.6", "[part of] 1::(2::(3::[4]))", "1.5s")
    l2 = dw("37.7", "[part of] 1::(2::[3;4])", "0.1s")
    lines = ["ch4_s3_trace (TracingAppend): 65.0 s (narration 60.6 s, 3 clips)", *l1, *l1, *l2, *l2, "(5 s)"]
    otxt = Mono("\n".join(lines), 18, t2c={"dwell:": GOLD}, line_spacing=0.75)
    opage = page6(11.6, 3.2)
    otxt.move_to(opage[0].get_center() + LEFT * 0.1)
    return VGroup(opage, otxt)


def circ(C, R, deg):
    a = np.radians(deg)
    return np.array([C[0] + R * np.cos(a), C[1] + R * np.sin(a), 0])


def exit_angle(C, R, deg, hw, hh, step, pad=0.1):
    centre = circ(C, R, deg)
    a = deg
    for _ in range(400):
        p = circ(C, R, a)
        if abs(p[0] - centre[0]) > hw + pad or abs(p[1] - centre[1]) > hh + pad:
            return a
        a += step
    return a


def make_ring(C, R, nodes):
    angs = [180, 60, -60, -180]
    arcs = []
    for i in range(3):
        n_a, n_b = nodes[i], nodes[(i + 1) % 3]
        s = exit_angle(C, R, angs[i], n_a.width / 2, n_a.height / 2, -1)
        e = exit_angle(C, R, angs[i + 1], n_b.width / 2, n_b.height / 2, +1, pad=0.18)
        arc = Arc(radius=R, start_angle=np.radians(s), angle=np.radians(e - s), arc_center=C)
        arc.set_stroke(FG, 3)
        arc.add_tip(tip_length=0.2, tip_width=0.2)
        arcs.append(arc)
    dot = Dot(circ(C, R, 150), radius=0.11, color=YELLOW).set_z_index(5)
    return arcs, dot


# ---------------------------------------------------------------- s3 pieces
def build_ladder():
    data = [("project", "focs/l03-lists", None),
            ("chapter", "ch4", "8–11 min · ~1300–1800 words"),
            ("scene", "ch4_s3_trace", "45–150 s · one Manim file"),
            ("clip", "[c4.trace.2]", "15–40 s · one narration line ·\nthe unit of voicing and syncing"),
            ("mark", "{pending}", "a cue word")]
    heads = []
    for name, tag, gold in data:
        row = VGroup(T(name, 30, BLUE), Mono(tag, 28, YELLOW)).arrange(RIGHT, buff=0.3)
        parts = [row]
        if gold:
            parts.append(T(gold, 28, GOLD, line_spacing=0.8))
        heads.append(VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
    cx, W, top = 1.6, 9.6, 3.5
    tops, y = [], top
    for h in heads:
        tops.append(y)
        y = y - 0.12 - h.height - 0.15
    bottoms = [0] * 5
    bottoms[4] = y
    for i in (3, 2, 1, 0):
        bottoms[i] = bottoms[i + 1] - 0.15
    boxes = []
    for i, h in enumerate(heads):
        w = W - 0.6 * i
        r = RoundedRectangle(corner_radius=0.15, width=w, height=tops[i] - bottoms[i], stroke_color=BLUE,
                             stroke_width=3, fill_color=BLUE, fill_opacity=0.05)
        r.move_to([cx, (tops[i] + bottoms[i]) / 2, 0])
        h.move_to([0, 0, 0]).align_to(r, LEFT).shift(RIGHT * 0.25)
        h.align_to([0, tops[i] - 0.12, 0], UP)
        boxes.append(r)
    return VGroup(*boxes, *heads)


def page3():
    w, h, f = 0.6, 0.8, 0.2
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0],
                   stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.15)
    fold = VMobject(stroke_color=TEAL, stroke_width=3).set_points_as_corners(
        [[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0]])
    return VGroup(body, fold)


# ---------------------------------------------------------------- s4 timeline (mini)
V_STARTS = [0.0, 2.2, 6.5, 12.0, 15.4]
V_LEN = 18.2
V_L, V_R, V_Y = -5.5, 5.5, -0.5
V_U = (V_R - V_L) / V_LEN


def build_timeline():
    axis = Line([V_L, V_Y, 0], [V_R, V_Y, 0], color=DIM, stroke_width=4)
    ticks, pins = [], []
    for k, s in enumerate(V_STARTS):
        x = V_L + V_U * s
        ticks.append(Line([x, V_Y - 0.16, 0], [x, V_Y + 0.16, 0], color=GOLD, stroke_width=4))
        h = 1.35 if k % 2 == 0 else 0.75
        pins.append(Line([x, V_Y, 0], [x, V_Y + h, 0], color=YELLOW, stroke_width=2.5))
    end_tick = Line([V_R, V_Y - 0.16, 0], [V_R, V_Y + 0.16, 0], color=DIM, stroke_width=4)
    return axis, ticks, end_tick, pins


def tool_box(label, w, h):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h)
    box.set_stroke(DIM, 2.5).set_fill(BLUE, 0.15)
    return VGroup(box, label.move_to(box))


# ---------------------------------------------------------------- own pieces
def bin_shape(cx, w, bottom, top, color):
    return VMobject().set_points_as_corners([[cx - w / 2, top, 0], [cx - w / 2, bottom, 0],
                                             [cx + w / 2, bottom, 0], [cx + w / 2, top, 0]]).set_stroke(color, 4)


def film_band(n, fw, fh, cx, cy):
    """Film strip band: DIM outline, sprocket holes top and bottom; frames go inside."""
    W = n * fw + 0.2
    H = fh + 0.4
    band = Rectangle(width=W, height=H).set_stroke(DIM, 2).set_fill(BG, 1).move_to([cx, cy, 0])
    holes = VGroup()
    k = int(W / 0.22)
    for i in range(k):
        x = cx - W / 2 + 0.11 + i * (W - 0.22) / (k - 1)
        for dy in (H / 2 - 0.1, -H / 2 + 0.1):
            holes.add(Square(0.08).set_stroke(width=0).set_fill(DIM, 0.8).move_to([x, cy + dy, 0]))
    return VGroup(band, holes).set_z_index(-1)


def music_bar(xl, xr, y, h=0.36):
    return RoundedRectangle(corner_radius=0.12, width=xr - xl, height=h) \
        .set_stroke(PURPLE, 2).set_fill(PURPLE, 0.55).move_to([(xl + xr) / 2, y, 0])


def mini_film(n, fw, cx, cy):
    fh = fw * 9 / 16
    band = film_band(n, fw, fh, cx, cy)
    frames = VGroup(*[Rectangle(width=fw, height=fh).set_stroke(DIM, 1.5).set_fill(BLUE, 0.35)
                      .move_to([cx + (i - (n - 1) / 2) * fw, cy, 0]) for i in range(n)])
    return VGroup(band, frames)


# ---------------------------------------------------------------- recap vignettes
def text_to_bars(group):
    """Miniature: each line of every Text becomes a bar in its colour (shape kept, no tiny glyphs)."""
    out = VGroup()
    for m in group.get_family():
        if isinstance(m, Text):
            col = m[0].get_fill_color() if len(m) else FG
            lines = m.text.split("\n") if hasattr(m, "text") else [""]
            n = max(1, len(lines))
            lh = m.height / n
            for j in range(n):
                frac = len(lines[j]) / max(len(l) for l in lines) if lines[j] else 0.5
                w = max(0.05, m.width * frac)
                bar = Rectangle(width=w, height=lh * 0.55).set_stroke(width=0).set_fill(col, 0.85)
                bar.move_to([m.get_left()[0] + w / 2, m.get_top()[1] - lh * (j + 0.5), 0])
                out.add(bar)
    return out


def vig_plan():
    lad = build_ladder()
    boxes = VGroup(*lad[:5])
    lad = VGroup(boxes, text_to_bars(VGroup(*lad[5:])))
    lad.scale_to_fit_width(2.1).move_to([0, 0.45, 0])
    pg = page3().scale(0.8).move_to([-0.95, -0.62, 0])
    lab = Mono("PLAN.md", 28, TEAL).next_to(pg, RIGHT, buff=0.15)
    tick = check_mark(YELLOW).scale(0.8).next_to(lab, RIGHT, buff=0.2)
    return VGroup(lad, pg, lab, tick)


def vig_script():
    before = T("exactly en conses", 28).move_to([0, 0.4, 0])
    strike = Line(before.get_left() + LEFT * 0.08, before.get_right() + RIGHT * 0.08, color=RED, stroke_width=5)
    after = T("one cons per element", 28, GREEN).move_to([0, -0.45, 0])
    return VGroup(before, strike, after)


def vig_voice():
    vk = tool_box(Mono("vk voice", 28), 2.3, 0.6).move_to([0, 0.75, 0])
    axis, ticks, end_tick, pins = build_timeline()
    tl = VGroup(axis, *ticks, end_tick, *pins)
    tl.stretch(3.0 / 11.0, 0).stretch(0.45, 1)
    tl.move_to([0, -0.05, 0]).align_to([0, -0.3, 0], DOWN)
    note = T("no tokens", 28, GREEN).move_to([0, -0.75, 0])
    return VGroup(vk, tl, note)


def vig_checklist():
    items = build_checklist()
    items[4].set_color(YELLOW)
    g = text_to_bars(VGroup(*items))
    g.scale_to_fit_height(2.1).move_to(ORIGIN)
    return g


def vig_loop():
    C, R = np.array([-0.95, 0.0, 0]), 0.8
    s_check = node6("", 0.7, "tool").scale(0.6).move_to(circ(C, R, 180))
    s_beats = page6(0.7, 0.4, fold=0.14).move_to(circ(C, R, 60))
    s_fix = node6("", 0.8, "agent").scale(0.6).move_to(circ(C, R, -60))
    for n_ in (s_check, s_beats, s_fix):
        n_.set_z_index(3)
    arcs, dot = make_ring(C, R, [s_check, s_beats, s_fix])
    A = -0.55
    axis = Line([0.4, A, 0], [1.9, A, 0]).set_stroke(DIM, 3)
    px = 0.65
    pin = Line([px, A, 0], [px, A + 0.95, 0]).set_stroke(YELLOW, 2).set_z_index(1)
    plab = Mono("{done}", 28, YELLOW).move_to([px - 0.04, A + 1.05, 0], aligned_edge=DL)
    blk = Rectangle(width=0.85, height=0.3).set_stroke(BLUE, 2).set_fill(BLUE, 0.45)
    blk.move_to([px, A + 0.08, 0], aligned_edge=DL)
    return VGroup(*arcs, s_check, s_beats, s_fix, dot, axis, blk, pin, plab)


def vig_review():
    img = crop_image().scale_to_fit_width(2.8).move_to([0, 0.45, 0])
    frames = [tile_rect(img, c, r, width=2.5) for c, r in TRACE_TILES]
    film = mini_film(8, 0.33, 0, -0.5)
    mus = music_bar(-1.32, 1.32, -0.98, h=0.2)
    return Group(img, *frames, film, mus)


def vig_files():
    pairs = [page_pair(w=0.42, h=0.54, two=(i % 2 == 0)).move_to([(i - 1.5) * 0.95, 0, 0]) for i in range(4)]
    arrows = [Arrow([a.get_right()[0], 0, 0], [b.get_left()[0], 0, 0], buff=0.08, stroke_width=3,
                    tip_length=0.14, color=DIM) for a, b in zip(pairs[:-1], pairs[1:])]
    return VGroup(*pairs, *arrows), pairs


class Review(NarratedScene):
    def construct(self):
        items = build_checklist()
        items[4].set_color(YELLOW)
        sub = build_sub()
        WX = 2.2   # workspace centre beside the checklist
        WX4 = 2.6  # review.4 film work sits right of the orient sub-labels

        # ================================================= c1.review.1
        with self.say("c1.review.1") as c:
            self.play(LaggedStart(*[FadeIn(it, shift=0.2 * RIGHT) for it in items], lag_ratio=0.12),
                      FadeIn(sub, lag_ratio=0.3), run_time=min(1.5, 0.9 * c.until("lint")))
            c.wait_until("lint")
            cmd = Mono("vk check --chapter 4 --no-render", 30).move_to([WX, 3.1, 0])
            self.play(FadeIn(cmd, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("every")
            b_fix = bin_shape(0.0, 2.4, 0.55, 2.0, GREEN)
            b_acc = bin_shape(4.15, 4.6, 0.55, 2.0, GOLD)
            l_fix = T("fixed", 32, GREEN).move_to([0.0, 0.15, 0])
            l_acc = T("accepted, for a reason", 32, GOLD).move_to([4.15, 0.15, 0])
            self.play(Create(b_fix), Create(b_acc), LaggedStart(FadeIn(l_fix, shift=0.2 * DOWN),
                                                                FadeIn(l_acc, shift=0.2 * DOWN), lag_ratio=0.3),
                      run_time=1.4)
            ticks = [check_mark(GREEN).scale(0.6).move_to([x, 0.95, 0]) for x in (-0.7, 0.0, 0.7)]
            self.play(LaggedStart(*[FadeIn(t, shift=0.6 * DOWN) for t in ticks], lag_ratio=0.25), run_time=1.0)
            c.wait_until("accept")
            lp = lint_page().scale_to_fit_width(4.2).move_to([4.15, 1.25, 0])
            self.play(FadeIn(lp, shift=1.2 * DOWN), run_time=1.4)
            note = T("the collapse shows passing states\nwhile the voice says: three onto four,\nthen two, then one",
                     30, DIM, line_spacing=0.85).move_to([WX, -1.15, 0])
            self.play(Write(note), run_time=min(3.0, 0.8 * c.until("recorded")))
            c.wait_until("recorded")
            rec = VGroup(check_mark(GREEN), T("recorded", 32, GREEN)).arrange(RIGHT, buff=0.25).move_to([WX, -2.65, 0])
            self.play(Create(rec[0]), FadeIn(rec[1], shift=0.2 * RIGHT), run_time=min(0.9, c.until(floor=0.4)))

        # ================================================= c1.review.2
        with self.say("c1.review.2") as c:
            hcmd = Mono("vk holds 4", 34).move_to([0, 3.4, 0])
            whole = ImageMobject(str(HOLDS)).set_height(4.6).move_to([0, -0.75, 0])
            sweep_clear(self, FadeIn(hcmd, shift=0.2 * DOWN), time_span(FadeIn(whole), 0.5, 1.4), run_time=1.4)
            s = whole.height / HOLDS_H
            C = whole.get_center()
            P = C + np.array([0, (HOLDS_H / 2 - (CROP_Y0 + CROP_Y1) / 2) * s, 0])
            crop = crop_image().scale_to_fit_width(HOLDS_W * s).move_to(P)
            Tc = np.array([0, 1.55, 0])
            k = 9.6 / (HOLDS_W * s)
            self.wait(0.5)
            self.add(crop)
            self.play(FadeOut(whole, scale=k, shift=Tc + k * (C - P) - C),
                      crop.animate.scale(k).move_to(Tc), run_time=min(1.6, max(0.8, c.until("taken") - 0.9)))
            frames = [tile_rect(crop, cc, rr) for cc, rr in TRACE_TILES]
            self.play(*[Create(f) for f in frames], run_time=min(0.8, c.until("taken", floor=0.4)))
            c.wait_until("taken")
            A = -0.3
            xl, xr = crop.get_left()[0], crop.get_left()[0] + 858 * crop.width / HOLDS_W
            axis = Line([xl, A, 0], [xr, A, 0]).set_stroke(DIM, 2)
            pins = VGroup(*[VGroup(Line([x, A, 0], [x, A + 0.32, 0]).set_stroke(GOLD, 3),
                                   Dot([x, A + 0.32, 0], radius=0.06, color=GOLD))
                            for x in (xl + 0.2, xl + 1.75, xl + 3.3)])
            log = T("from the render's own log", 30, GOLD)
            log.move_to([0.4 + log.width / 2, A + 0.1, 0])
            self.play(Create(axis), LaggedStart(*[GrowFromEdge(p, DOWN) for p in pins], lag_ratio=0.3), run_time=1.3)
            self.play(FadeIn(log, shift=0.2 * LEFT), run_time=0.9)
            c.wait_until("reads")
            once = T("once per round", 30, DIM)
            once.move_to([-6.3 + once.width / 2, -1.3, 0])
            self.play(FadeIn(once, shift=0.2 * RIGHT), run_time=0.9)
            checks = []
            for txt, cue, y in zip(["matches the narration", "consistent across scenes", "exact code",
                                    "nothing cramped, cut off or half-empty"],
                                   ["match", "consistent", "code", "cramped"], (-1.3, -1.85, -2.4, -2.95)):
                c.wait_until(cue)
                m = T(txt, 32).move_to([-1.8, y, 0], aligned_edge=LEFT)
                self.play(FadeIn(m, shift=0.2 * RIGHT), run_time=0.8)
                checks.append(m)

        # ================================================= c1.review.3
        with self.say("c1.review.3") as c:
            self.play(FadeOut(hcmd, axis, pins, log, once, *checks, *frames), run_time=1.0)
            cx, cy = tile_rect(crop, *CELLS1).get_center()[:2]
            q = set_backstroke(T("?", 80, YELLOW)).move_to([cx, cy, 0])
            self.play(FadeIn(q, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("left")
            tile = RoundedRectangle(corner_radius=0.08, width=3.6, height=2.025).set_stroke(DIM, 3).set_fill(BG, 1)
            tile.move_to([-3.3, 2.0, 0])
            tl, tr = tile.get_left()[0] + 0.25, tile.get_right()[0] - 0.25
            ty0, ty1 = 1.55, 2.7
            table = VGroup(*[Line([tl, y, 0], [tr, y, 0]) for y in np.linspace(ty0, ty1, 4)],
                           *[Line([x, ty0, 0], [x, ty1, 0]) for x in np.linspace(tl, tr, 5)])
            table.set_stroke(FG, 2, opacity=0.7)
            sweep_clear(self, time_span(FadeIn(tile), 0.6, 1.2), time_span(Create(table), 0.6, 1.4), run_time=1.4)
            lh = T("left-heavy?", 36, RED)
            lh.move_to([-0.9 + lh.width / 2, 2.0, 0])
            self.play(FadeIn(lh, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("spanned")
            my = 1.25
            ruler = VGroup(Line([tl, my, 0], [tr, my, 0]),
                           Line([tl, my - 0.1, 0], [tl, my + 0.1, 0]),
                           Line([tr, my - 0.1, 0], [tr, my + 0.1, 0])).set_stroke(GOLD, 4)
            self.play(Create(ruler[1]), Create(ruler[0], rate_func=linear), run_time=1.2)
            sp = T("spans the frame", 36, GREEN)
            sp.move_to([-0.9 + sp.width / 2, 2.0, 0])
            self.play(Create(ruler[2]), ReplacementTransform(lh, sp), run_time=1.0)
            c.wait_until("notes")
            note = Mono("acc.3 > give: the reply overlaps the chain;\nmove the chain down ~0.5", 30,
                        t2c={"acc.3 > give": YELLOW}, line_spacing=0.8).move_to([0, 0.0, 0])
            self.play(FadeIn(note, shift=0.2 * UP), run_time=1.0)
            self.play(FlashUnder(select(note, "acc.3 > give")[0], run_time=1.2, time_width=1.5))
            c.wait_until("send")
            b1 = agent(2.8, 0.7, "scene-builder", 28).move_to([-3.6, -2.3, 0])
            a1 = Arrow([-3.6, -0.6, 0], [-3.6, -1.9, 0], buff=0, stroke_width=3, tip_length=0.2, color=DIM)
            sm = Mono("send message", 28, DIM)
            sm.move_to([-3.35 + sm.width / 2, -1.25, 0])
            self.play(GrowArrow(a1), FadeIn(sm), FadeIn(b1, shift=0.2 * DOWN), run_time=1.0)
            fly = note.copy()
            self.play(fly.animate.scale(0.12).move_to(b1).set_opacity(0),
                      time_span(FlashAround(b1, color=BLUE, time_width=1.5), 0.6, 1.4), run_time=1.4)
            self.remove(fly)
            hour = T("< 1 h", 32, GOLD)
            hour.move_to([b1.get_right()[0] + 0.3 + hour.width / 2, -2.3, 0])
            self.play(FadeIn(hour, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("fresh")
            b2 = agent(3.4, 0.7, "fresh scene-builder", 28).move_to([3.6, -2.3, 0])
            a2 = Arrow([3.6, -0.6, 0], [3.6, -1.9, 0], buff=0, stroke_width=3, tip_length=0.2, color=DIM)
            fly2 = note.copy()
            self.play(GrowArrow(a2), FadeIn(b2, shift=0.2 * DOWN), run_time=0.9)
            self.play(fly2.animate.scale(0.12).move_to(b2).set_opacity(0),
                      time_span(FlashAround(b2, color=BLUE, time_width=1.5), 0.5, 1.2),
                      run_time=min(1.2, c.until("At most two rounds", floor=0.6)))
            self.remove(fly2)
            c.wait_until("At most two rounds")
            rounds = T("≤ 2 rounds", 34, GOLD).move_to([0, -3.2, 0])
            self.play(FadeIn(rounds, shift=0.2 * DOWN), run_time=0.8)

        # ================================================= c1.review.4
        with self.say("c1.review.4") as c:
            for i, it in enumerate(items):
                it.set_color(YELLOW if i == 5 else DIM)
            fcmd = Mono("vk final 4", 34).move_to([WX4, 3.2, 0])
            sweep_clear(self, LaggedStart(*[FadeIn(it) for it in items], FadeIn(sub), lag_ratio=0.08),
                        time_span(FadeIn(fcmd, shift=0.2 * DOWN), 0.5, 1.4), run_time=1.4)
            c.wait_until("renders every scene")
            fw, fh = 0.8, 0.8 * 9 / 16
            sx = row_xs(WX4, 8, fw, 0.12)
            outl = [Rectangle(width=fw, height=fh).set_stroke(DIM, 2).set_fill(FG, 0.08).move_to([x, 2.25, 0])
                    for x in sx]
            fills = [Rectangle(width=fw, height=fh).set_stroke(width=0).set_fill(BLUE, 0.45).move_to([x, 2.25, 0])
                     for x in sx]
            self.play(LaggedStart(*[FadeIn(o, shift=0.15 * DOWN) for o in outl], lag_ratio=0.1),
                      run_time=min(1.0, 0.8 * c.until("in parallel")))
            c.wait_until("in parallel")
            self.play(*[GrowFromEdge(f, LEFT) for f in fills], rate_func=linear,
                      run_time=min(1.8, 0.9 * c.until("stitches")))
            c.wait_until("stitches")
            fx = row_xs(WX4, 8, fw, 0)
            band = film_band(8, fw, fh, WX4, 1.85)
            mus = music_bar(fx[0] - fw / 2, fx[-1] + fw / 2, 1.05)
            self.play(*[o.animate.move_to([x, 1.85, 0]) for o, x in zip(outl, fx)],
                      *[f.animate.move_to([x, 1.85, 0]) for f, x in zip(fills, fx)],
                      FadeIn(band), time_span(GrowFromEdge(mus, LEFT), 0.8, 1.8), run_time=1.8)
            c.wait_until("two or three minutes")
            spec = T("1080p60 · 2–3 min", 32, GOLD).move_to([WX4, 0.35, 0])
            self.play(FadeIn(spec, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("probe")
            probe = VGroup(Mono("ffprobe", 30), T("1920×1080 · 60 fps", 30, GREEN)).arrange(RIGHT, buff=0.45)
            probe.move_to([WX4, -0.45, 0])
            self.play(FadeIn(probe[0], shift=0.2 * RIGHT), time_span(FadeIn(probe[1], shift=0.2 * RIGHT), 0.5, 1.2),
                      run_time=1.2)
            c.wait_until("status")
            st_pg = page(0.5, 0.64).move_to([-1.3, -2.0, 0])
            st_lab = Mono("STATUS.md", 28, TEAL).next_to(st_pg, DOWN, buff=0.15)
            st_tick = check_mark(GREEN).move_to([-0.55, -2.0, 0])
            producer = agent(3.0, 0.75, "producer", 32).move_to([3.4, -1.45, 0])
            self.play(items[5].animate.set_color(DIM), items[6].animate.set_color(YELLOW),
                      FadeIn(st_pg), FadeIn(st_lab), FadeIn(producer), run_time=0.9)
            rep = page(0.5, 0.64).move_to([1.1, -1.45, 0])
            rep_lab = Mono("report", 28, TEAL).next_to(rep, DOWN, buff=0.15)
            self.play(Create(st_tick), TransformFromCopy(st_pg, rep), FadeIn(rep_lab, shift=0.4 * UP),
                      run_time=min(1.3, c.until("relay", floor=0.5)))
            c.wait_until("relay")
            you = T("you", 36, YELLOW).move_to([3.4, -2.85, 0])
            ar = Arrow(producer.get_bottom(), you.get_top(), buff=0.08, stroke_width=3, tip_length=0.18, color=DIM)
            five = T("≤ 5 lines", 30, GOLD)
            five.move_to([3.65 + five.width / 2, -2.2, 0])
            self.play(GrowArrow(ar), FadeIn(you, shift=0.2 * DOWN), FadeIn(five, target_position=producer),
                      run_time=1.2)
            c.wait_until("lines to check by ear")
            ear = T("lines to check by ear", 28).move_to([3.4, -3.3, 0])
            self.play(FadeIn(ear, shift=0.2 * DOWN), run_time=min(0.8, c.until(floor=0.4)))

        # ================================================= c1.recap.1
        with self.say("c1.recap.1") as c:
            spots = [(-5.15, 2.15), (-1.75, 2.15), (1.75, 2.15), (5.2, 2.15), (-3.6, -1.15), (0.0, -1.15), (3.6, -1.15)]
            texts = ["the plan,\nyou approve", "scripted\nfor the ear", "audio and\nword times",
                     "a director\nper chapter", "write, check, look, fix,\ncued on words",
                     "review and\nthe final cut", "every hand-off\nis a file"]
            files, file_pages = vig_files()
            vigs = [vig_plan(), vig_script(), vig_voice(), vig_checklist(), vig_loop(), vig_review(), files]
            for v, (x, y) in zip(vigs, spots):
                v.move_to([x, y, 0])
            labels = []
            for t, v, (x, y) in zip(texts, vigs, spots):
                lab = T(t, 28, line_spacing=0.8)
                lab.move_to([x, (0.45 if y > 0 else -2.85), 0])
                labels.append(lab)

            self.play(*[FadeOut(m) for m in self.mobjects], run_time=min(1.0, 0.8 * c.until("r1")))
            cues = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "next"]
            prev = None
            for i in range(7):
                c.wait_until(cues[i])
                v, lab = vigs[i], labels[i]
                lab.set_color(YELLOW)
                rt = min(1.3, 0.75 * c.until(cues[i + 1]))
                anims = [FadeIn(lab, shift=0.2 * DOWN)]
                if prev is not None:
                    anims.append(labels[prev].animate.set_color(FG))
                if i == 0:
                    anims += [FadeIn(v[0], shift=0.2 * DOWN), FadeIn(v[1]), FadeIn(v[2]),
                              time_span(Create(v[3]), 0.5 * rt, rt)]
                elif i == 1:
                    anims += [FadeIn(v[0]), time_span(Create(v[1]), 0.2 * rt, 0.6 * rt),
                              time_span(TransformFromCopy(v[0], v[2]), 0.4 * rt, rt)]
                elif i == 6:
                    anims += [FadeIn(v, lag_ratio=0.15)]
                else:
                    anims += [FadeIn(v, shift=0.2 * DOWN)]
                self.play(*anims, run_time=rt)
                prev = i
            # r7: pages flash along the conveyor
            self.play(LaggedStart(*[FlashAround(p, color=TEAL, time_width=1.5) for p in file_pages], lag_ratio=0.3),
                      run_time=min(2.0, 0.8 * c.until("next")))

            # the grid holds through the pause and "Every turn of every agent"; the crew returns on "costs tokens"
            c.wait_until("costs tokens")
            tree, blue, builders = master_shot()
            sweep_clear(self, time_span(FadeIn(tree), 0.5, 1.4), run_time=1.4)
            marks = [token_mark(b) for b in blue] + [token_mark(b, 0.75) for b in builders]
            self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.08),
                      run_time=min(1.6, c.until("next time", floor=1.0)))
            c.wait_until("next time")
            nxt = T("Next: where the tokens go, and where we can cut", 34, t2c={"Next:": DIM}).move_to([0, -2.5, 0])
            self.play(FadeIn(nxt, shift=0.2 * UP), run_time=1.0)

        self.wait(7.5)   # end card: music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
