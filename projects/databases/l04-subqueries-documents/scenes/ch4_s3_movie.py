"""Chapter 4, scene 3: The Kid as one document. Clips c4.movie.1 – c4.movie.5.

Owns the shared *document card* (s1's opening card, s4, s5, s6, s7, ch5–ch8). Import with
`D = load_scene("ch4_s3_movie")`:

    D.doc_card(src=None, size=24, width=None, height=None, pad=None)
        -> DocCard (VGroup): .frame (RoundedRectangle, corner 0.2, TEAL stroke 3, TEAL fill 0.06)
           and .code (json_code(src, size), centred in the frame; None when src is None).
           With src the frame fits the code + pad (default 0.013·size) on every side;
           src=None is an empty card, width × height (default 3.6 × 2.4). Built at ORIGIN, static.
           Add/animate .frame and .code as two objects if you edit the code later.
    D.json_code(src, size=24) -> Code(src, lang="json") recoloured: { } [ ] TEAL, /* … */ DIM,
           null PINK (outside strings; keys/strings/numbers keep the lexer's colours).
    D.fit_frame(code, pad=None) -> a new card frame fitted round code (Transform the old frame
           into it when the code grows).
    D.kid_doc(size=18) -> DocCard of KID_DOC, slide 71's card (20 lines; at 18 it fills the
           frame height, ~9.5 × 7.5). D.KID_DOC is its source text; D.KID_LINES the list of its lines.
    D.comment_glyphs(card_or_code) -> [VGroup per /* … */ comment] (3 in kid_doc).
    D.coogan_note(width=6.6, size=28) -> VGroup(.box DIM RoundedRectangle, .text T): trivia
           entry 0 as plain text, wrapped.
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


# ══ document card helper ═══════════════════════════════════════════════════════

def _roles(src):
    """Role of every non-whitespace char of src: 'brace', 'comment', 'null' or None."""
    out, i, n = [], 0, len(src)
    in_str = False
    while i < n:
        ch = src[i]
        if in_str:
            if ch == "\\" and i + 1 < n:
                out += [None, None] if not src[i + 1].isspace() else [None]
                i += 2
                continue
            if ch == '"':
                in_str = False
            if not ch.isspace():
                out.append(None)
            i += 1
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out += ["comment" for c in src[i:j] if not c.isspace()]
            i = j
            continue
        if src.startswith("null", i) and not (i > 0 and src[i - 1].isalnum()):
            out += ["null"] * 4
            i += 4
            continue
        if ch == '"':
            in_str = True
        if not ch.isspace():
            out.append("brace" if ch in "{}[]" else None)
        i += 1
    return out


def json_code(src, size=24):
    code = Code(src, size=size, lang="json")
    glyphs = code.text.submobjects
    roles = _roles(code.src)
    if len(roles) == len(glyphs):
        col = {"brace": TEAL, "comment": DIM, "null": PINK}
        for g, r in zip(glyphs, roles):
            if r:
                g.set_color(col[r])
    else:   # fallback (glyph count mismatch): brackets only
        for ch in "{}[]":
            for g in chars(code, ch):
                g.set_color(TEAL)
    return code


def _frame(w, h):
    return (RoundedRectangle(corner_radius=0.2, width=w, height=h)
            .set_stroke(TEAL, 3).set_fill(TEAL, 0.06))


def fit_frame(code, pad=None, size=None, min_w=0.0, min_h=0.0):
    pad = pad if pad is not None else 0.013 * (size or 24)
    f = _frame(max(code.width + 2 * pad, min_w), max(code.height + 2 * pad, min_h))
    return f.move_to(code.get_corner(UL) + np.array([-pad, pad, 0]), aligned_edge=UL)


class DocCard(VGroup):
    def __init__(self, src=None, size=24, width=None, height=None, pad=None):
        super().__init__()
        self.size = size
        pad = pad if pad is not None else 0.013 * size
        self.code = json_code(src, size) if src else None
        if self.code is not None:
            self.frame = _frame(width or self.code.width + 2 * pad, height or self.code.height + 2 * pad)
            self.frame.move_to(self.code)
            self.add(self.frame, self.code)
        else:
            self.frame = _frame(width or 3.6, height or 2.4)
            self.add(self.frame)


def doc_card(src=None, size=24, width=None, height=None, pad=None):
    return DocCard(src, size, width, height, pad)


TT, NM = "tt0012349", "nm0000122"
L_MOVIE = ['  "movie_id": "tt0012349",', '  "title": "The Kid",', '  "year": 1921,',
           '  "type": "movie",', '  "minutes": 68,']
L_GENRES = '  "genres": ["Comedy", "Drama", "Family"],'
L_RATING = ['  "rating": 8.2,', '  "rating_votes": 142991,']
L_ACT_OPEN, L_ACT_CLOSE = '  "actors": [', '  ],'
L_OBJ_OPEN, L_OBJ_CLOSE = '    {', '    },'
L_PID, L_NAME = '      "person_id": "nm0000122",', '      "name": "Charles Chaplin",'
L_ROLES = '      "roles": ["A Tramp"]'
L_NINE = '    /* 9 more */'
L_TRIVIA = '  "trivia_entries": [/* 5 items */ ],'
L_CREW = '  /* also "directors", "producers", "writers", "composers" */'
KID_LINES = (["{"] + L_MOVIE + [L_GENRES] + L_RATING
             + [L_ACT_OPEN, L_OBJ_OPEN, L_PID, L_NAME, L_ROLES, L_OBJ_CLOSE, L_NINE, L_ACT_CLOSE,
                L_TRIVIA, L_CREW, "}"])
KID_DOC = "\n".join(KID_LINES)


def kid_doc(size=18):
    return doc_card(KID_DOC, size=size)


def comment_glyphs(card_or_code):
    code = getattr(card_or_code, "code", card_or_code)
    out, src = [], code.src
    for k, line in enumerate(src.split("\n")):
        i = line.find("/*")
        while i >= 0:
            j = line.find("*/", i) + 2
            out.append(code.find(line[i:j], line=k))
            i = line.find("/*", j)
    return out


COOGAN = ['Due to the fact that Jackie Coogan\'s', 'mother and stepfather had spent all',
          'the youngster\'s money before he', 'reached adulthood, the "Coogan Bill"',
          'was enacted to ensure that child', 'actors\' funds would never again be',
          'able to be squandered by their', 'parents or guardians.']


def coogan_note(width=6.6, size=28):
    text = T("\n".join(COOGAN), size, FG, line_spacing=1.0)
    text.scale_to_fit_width(min(text.width, width - 0.6))
    box = RoundedRectangle(corner_radius=0.15, width=text.width + 0.6, height=text.height + 0.6)
    box.set_stroke(DIM, 2.5).set_fill(BG, 1).move_to(text)
    g = VGroup(box, text)
    g.box, g.text = box, text
    return g


# ══ scene helpers ═══════════════════════════════════════════════════════════════

def one_cell(value, color, size=30):
    head = Mono("json_valid(...)", size - 2, DIM)
    val = Mono(value, size, color)
    w = max(head.width, val.width) + 0.5
    p = 0.55
    box = Rectangle(width=w, height=2 * p).set_stroke(BLUE, 2)
    hl = Line(box.get_left(), box.get_right()).set_stroke(BLUE, 2)
    head.move_to(box.get_top() + DOWN * p / 2).align_to(box, LEFT).shift(RIGHT * 0.25)
    val.move_to(box.get_bottom() + UP * p / 2).align_to(box, LEFT).shift(RIGHT * 0.25)
    g = VGroup(box, hl, head, val)
    g.val = val
    return g


SCH = load_scene("ch1_s2_schema")
CARD_TOP = 2.35     # the card's top in clips 1-2 (lines below the source row)
S2 = load_scene("ch4_s2_json")


class Ch4S3Movie(NarratedScene):
    # ---- card bookkeeping: self.frame and self.code are two top-level objects
    def anchor_to(self, code):
        code.shift(self.anchor - code.text[0].get_corner(UL))
        return code

    def stage(self, lines, hide=(), rt=0.8, extra=()):
        """Rewrite the card to `lines` (edit), frame refitted; lines in `hide` start invisible."""
        full = self.anchor_to(json_code("\n".join(lines), self.size))
        if hide:
            shown = self.anchor_to(json_code("\n".join("" if i in hide else l for i, l in enumerate(lines)),
                                             self.size))
        else:
            shown = full
        self.play(*edit(self.code, shown), Transform(self.frame, fit_frame(full, size=self.size, min_w=self.min_w, min_h=self.min_h)),
                  *extra, run_time=rt)
        self.code = shown
        self.full = full
        return full

    def land(self, items, rts=(1.4,), d=None, each=None):
        """items: (src_mob, line, value_substring, waypoints). A copy of the value travels from src
        through the waypoints into its slot (constant speed), taking the slot's size and colours,
        faint until it has left src; the rest of its line fades in as it lands. With two run
        times in `rts`, the first play takes every copy to its first waypoint together and the
        second play (staggered by d) the rest of the way. Afterwards only self.code holds it."""
        taken, last = {}, {}
        for k, (_, li, sub, _) in enumerate(items):
            taken.setdefault(li, set()).update(id(g) for g in self.full.find(sub, line=li))
            last[li] = k
        movs = []
        for src, li, sub, via in items:
            val = self.full.find(sub, line=li)
            dst = VGroup(*[g.copy().set_opacity(1) for g in val])
            start = src.copy()
            same = len(start) == len(dst)
            k1 = dst.height / start.height if same else dst[0].height / start[0].height
            cols0 = [g.get_color() for g in start]
            cols1 = [g.get_color() for g in dst] if same else [dst[0].get_color()] * len(start)
            pts = [src.get_center(), *[np.array([x, y, 0]) for x, y in via], dst.get_center()]
            movs.append(dict(mov=start.copy(), start=start, k1=k1, c0=cols0, c1=cols1, pts=pts))

        def mover(st, seg, fade, uu):
            pts = st["pts"][seg[0]:seg[1] + 1]
            L = np.cumsum([0] + [np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])])
            tot = max(L[-1], 1e-6)
            sc0 = st["k1"] if seg[0] > 0 else 1.0
            src_c, src_w, src_h = st["start"].get_center(), st["start"].width, st["start"].height

            def upd(m, a):
                s_ = smooth(a) * tot
                i = min(np.searchsorted(L, s_, side="right") - 1, len(pts) - 2)
                f = (s_ - L[i]) / max(L[i + 1] - L[i], 1e-6)
                for g, g0 in zip(m.family_members_with_points(), st["start"].family_members_with_points()):
                    g.points = g0.points.copy()   # in place: keep the glyph objects
                m.scale(interpolate(sc0, st["k1"], min(1, 2 * a)))
                m.move_to(interpolate(pts[i], pts[i + 1], f))
                u = interpolate(uu[0], uu[1], a)
                for g, c0, c1 in zip(m, st["c0"], st["c1"]):
                    g.set_color(interpolate_color(c0, c1, u))
                if fade:   # faint until its box has cleared the source's
                    off = m.get_center() - src_c
                    sep = max(abs(off[0]) - (m.width + src_w) / 2, abs(off[1]) - (m.height + src_h) / 2)
                    m.set_opacity(min(1.0, max(0.0, (sep - 0.7) / 0.3)))
                else:
                    m.set_opacity(1)
            return UpdateFromAlphaFunc(st["mov"], upd)

        n = len(items)
        if len(rts) == 2:   # together to the first waypoint, then on
            self.play(*[mover(st, (0, 1), (0.2, 0.3), (0, 0.5)) for st in movs], run_time=rts[0])
            phases = [(1, len(st["pts"]) - 1) for st in movs]
            fades, uu = [None] * n, (0.5, 1)
        else:
            phases = [(0, len(st["pts"]) - 1) for st in movs]
            fades, uu = [(0.08, 0.15)] * n, (0, 1)
        d = d if d is not None else (1.0 if n == 1 else 0.45)
        step = 0 if n == 1 else (1 - d) / (n - 1)
        anims, temps = [], []
        for k, (st, (src, li, sub, via)) in enumerate(zip(movs, items)):
            a0 = k * step
            anims += during([mover(st, phases[k], fades[k], uu)], a0, a0 + d)
            temps.append(st["mov"])
            if last[li] == k:
                line = self.full.line(li)
                rest = VGroup(*[g.copy().set_opacity(1) for g in line if id(g) not in taken[li]])
                anims += during(appear(rest, shift=None), a0 + 0.9 * d, a0 + d)
                temps.append(rest)
        if each:   # one play per item (each = its run time), in order
            groups = [[] for _ in items]
            gi = 0
            for k, st in enumerate(movs):
                groups[k].append(mover(st, phases[k], fades[k], uu))
            for k, (src, li, sub, via) in enumerate(items):
                if last[li] == k:
                    line = self.full.line(li)
                    rest = VGroup(*[g.copy().set_opacity(1) for g in line if id(g) not in taken[li]])
                    groups[k] += during(appear(rest, shift=None), 0.9, 1)
                    temps.append(rest)
            for k, g in enumerate(groups):
                self.play(*g, run_time=each[k])
        else:
            self.play(*anims, run_time=rts[-1])
        self.remove(*temps, self.code)
        self.add(self.full)
        self.code = self.full

    def construct(self):
        self.size = 22
        self.min_w, self.min_h = 5.3, 2.2
        K = kid_doc(18)
        self.final_anchor = K.code.text[0].get_corner(UL)
        top = K.frame.get_top()[1]
        pad22 = 0.013 * 22
        # phase 1: card's frame top-left corner at (1.25, CARD_TOP), sources on the left
        self.anchor = np.array([1.25 + pad22, CARD_TOP - pad22, 0])
        self.K = K

        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c4.movie.1
    def clip1(self):
        with self.say("c4.movie.1") as c:
            empty = doc_card(None, width=5.3, height=2.2)
            empty.frame.move_to([1.25 + 2.65, CARD_TOP - 1.1, 0])
            self.frame = empty.frame
            mv = SCH.place(SCH.kid_table("movies").scale(0.85), left=-6.6, top=2.6)
            self.mv = mv
            self.play(FadeIn(self.frame), *appear(mv), run_time=min(1.4, c.until("doc")))   # early: The Kid's row shown whole, then walked
            c.wait_until("doc")
            label = T("document: a JSON object stored as one unit, with a unique key", 28, DIM)
            label.move_to([0, -3.45, 0])
            self.doc_label = label
            braces = self.anchor_to(json_code("{\n}", self.size))
            self.play(*appear(label), Transform(self.frame, fit_frame(braces, size=self.size, min_w=self.min_w, min_h=self.min_h)),
                      run_time=1.0)
            self.play(*appear(braces, shift=None), run_time=0.6)
            self.code = braces
            c.wait_until("movies")
            self.stage(["{"] + L_MOVIE + ["}"], hide=range(1, 6), rt=0.6)
            vals = [TT, "The Kid", "1921", "movie", "68"]
            # the row splits: each value drops to its line's height, then slides in
            self.land([(mv.cell(0, j), j + 1, vals[j], [(mv.cell(0, j).get_x(), self.full.line(j + 1).get_y())])
                       for j in range(5)], rts=(0.8, 1.8), d=0.6)
            c.wait_until("ratings")
            rt = SCH.place(SCH.kid_table("ratings").scale(0.85), left=-6.6, top=2.6)
            self.rt = rt
            self.stage(["{"] + L_MOVIE + L_RATING + ["}"], hide=(6, 7), rt=0.9,
                       extra=[*during(disappear(mv), 0, 0.45), *during(appear(rt, shift=None), 0.5, 1)])
            left = min(1.2, max(0.6, c.until(None, floor=0.6) - 0.5))
            self.land([(rt.cell(0, j), j + 5, v, [(rt.cell(0, j).get_x(), self.full.line(j + 5).get_y())])
                       for j, v in ((1, "8.2"), (2, "142991"))], rts=(0.5, left), d=0.75)

    # ------------------------------------------------------------------ c4.movie.2
    def clip2(self):
        with self.say("c4.movie.2") as c:
            hg = SCH.place(SCH.kid_table("has_genre"), left=-6.6, top=2.6)
            gt = SCH.place(SCH.kid_table("genres"), left=-6.6, top=0.1)
            self.hg, self.gt = hg, gt
            dx = -1.9 - self.frame.get_left()[0]
            self.play(*during(disappear(self.rt), 0, 0.45),
                      *during([self.frame.animate.shift(RIGHT * dx), self.code.animate.shift(RIGHT * dx)],
                              0.3, 0.8),
                      *during(appear(hg, gt, lag=0.3), 0.55, 1),   # early: the genre rows shown whole, then walked
                      run_time=min(1.8, c.until("relationally")))
            self.anchor = self.anchor + RIGHT * dx
            c.wait_until("three rows")
            self.play(FlashAround(VGroup(*hg.rows), time_width=1.5), run_time=1.5)
            c.wait_until("plus the genres table")
            self.play(FlashAround(VGroup(*[gt.cell(i, 1) for i in range(3)]), time_width=1.5),
                      run_time=1.5)
            c.wait_until("cell")
            cellbox = SurroundingRectangle(gt.cell(0, 1), color=BLUE, buff=0.1).set_stroke(BLUE, 4)
            self.cellbox = cellbox
            self.play(FadeIn(cellbox), run_time=1.0)
            c.wait_until("array")
            lines = ["{"] + L_MOVIE + [L_GENRES] + L_RATING + ["}"]
            self.stage(lines, hide=(6,), rt=0.7)
            gy = self.full.line(6).get_y()
            gx = hg.frame.get_right()[0] + 0.2
            names = ["Comedy", "Drama", "Family"]
            self.land([(gt.cell(i, 1), 6, names[i], [(gx, gt.cell(i, 1).get_y()), (gx, gy)])
                       for i in (2, 1, 0)], each=(1.2, 0.9, 0.8))
            arr = self.code.find('["Comedy", "Drama", "Family"]', line=6)
            abox = SurroundingRectangle(arr, color=TEAL, buff=0.08).set_stroke(TEAL, 4)
            self.abox = abox
            self.play(FadeIn(abox), run_time=0.8)
            c.wait_until("nojoin")
            self.play(*set_alpha([hg], DIMMED), run_time=1.0)

    # ------------------------------------------------------------------ c4.movie.3
    def clip3(self):
        with self.say("c4.movie.3") as c:
            # shrink the card to its final size (19), keep it at the left
            s = 18 / 22
            ul = self.frame.get_corner(UR)
            v = self.K.frame.get_corner(UL) - self.frame.copy().scale(s, about_point=ul).get_corner(UL)
            self.play(*during(disappear(self.hg, self.gt, self.cellbox, self.abox, self.doc_label), 0, 0.5),
                      *during([self.frame.animate.scale(s, about_point=ul).shift(v),
                               self.code.animate.scale(s, about_point=ul).shift(v)], 0.2, 1),
                      run_time=1.5)
            self.size = 18
            self.min_w, self.min_h = 0.0, 0.0
            self.anchor = self.code.text[0].get_corner(UL)
            base = ["{"] + L_MOVIE + [L_GENRES] + L_RATING
            self.stage(base + [L_ACT_OPEN, L_ACT_CLOSE, "}"], rt=1.0)
            c.wait_until("objects")
            self.stage(base + [L_ACT_OPEN, L_OBJ_OPEN, L_OBJ_CLOSE, L_ACT_CLOSE, "}"], rt=1.2)
            c.wait_until("chaplin")
            self.stage(base + [L_ACT_OPEN, L_OBJ_OPEN, L_PID, L_NAME, L_OBJ_CLOSE, L_ACT_CLOSE, "}"],
                       rt=1.2)
            c.wait_until("roles")
            act = base + [L_ACT_OPEN, L_OBJ_OPEN, L_PID, L_NAME, L_ROLES, L_OBJ_CLOSE, L_ACT_CLOSE]
            self.stage(act + ["}"], rt=1.2)
            c.wait_until("for charles chaplin")
            tramp = self.code.find('"A Tramp"')
            self.play(FlashAround(tramp, time_width=1.5), *recolor(tramp, YELLOW), run_time=1.5)
            settle(self, self.code)
            c.wait_until("ten")
            # locator map, the three source tables lit
            m = SCH.schema_map()
            for n in ("has_position", "people", "plays_role"):
                cd = m.cards[n]
                cd.box.set_stroke(YELLOW)
                cd.title.set_color(YELLOW)
                if cd.entity:
                    cd.header.set_fill(YELLOW)
            m.scale_to_fit_width(5.3)
            m.move_to([-6.6 + 2.65, 0, 0])
            self.map = m
            obj = VGroup(*[self.code.line(i) for i in range(10, 15)])
            deck = VGroup()
            for k in range(9, 0, -1):
                r = RoundedRectangle(corner_radius=0.12, width=obj.width + 0.3, height=obj.height + 0.2)
                r.set_stroke(DIM, 2, opacity=1 - 0.06 * k).set_fill(BG, 1)
                r.move_to(obj).shift(RIGHT * 0.12 * k)
                r.set_z_index(-2)
                deck.add(r)
            dxr = 6.6 - self.frame.get_right()[0]
            deck.shift(RIGHT * dxr)
            self.play(*during([self.frame.animate.shift(RIGHT * dxr), self.code.animate.shift(RIGHT * dxr)], 0, 0.5),
                      *during(appear(m, shift=None), 0.35, 1),   # early: locator map, its tables named as it lands
                      run_time=min(1.3, c.until("crew")))
            self.anchor = self.code.text[0].get_corner(UL)
            self.play(LaggedStart(*[FadeIn(r) for r in deck], lag_ratio=0.15), run_time=0.9)
            self.wait(min(0.8, max(0.1, c.until("crew") - 1.4)))
            final = act[:-1] + [L_NINE, L_ACT_CLOSE]
            new = self.anchor_to(json_code("\n".join(final + ["}"]), self.size))
            nine = new.line(15)
            tgt = deck.copy()
            for r in tgt:
                r.stretch_to_fit_height(0.3).stretch_to_fit_width(nine.width + 0.2).move_to(nine)
                r.set_stroke(opacity=0).set_fill(opacity=0)
            self.play(*edit(self.code, new), Transform(self.frame, fit_frame(new, size=18)),
                      *during([Transform(deck, tgt)], 0, 0.9),
                      run_time=min(1.3, max(0.5, c.until("crew"))))
            self.remove(deck)
            self.code = new
            c.wait_until("crew")
            dx = self.K.frame.get_left()[0] - self.frame.get_left()[0]
            self.play(*during(disappear(m), 0, 0.5),
                      *during([self.frame.animate.shift(RIGHT * dx), self.code.animate.shift(RIGHT * dx)],
                              0.3, 1),
                      run_time=1.2)
            self.anchor = self.code.text[0].get_corner(UL)
            self.stage(final + [L_CREW, "}"], rt=1.2)

    # ------------------------------------------------------------------ c4.movie.4
    def clip4(self):
        with self.say("c4.movie.4") as c:
            self.stage(KID_LINES, rt=1.2)
            trivia = self.code.line(KID_LINES.index(L_TRIVIA))
            self.play(FlashAround(trivia, time_width=1.5), run_time=1.5)
            c.wait_until("coogan")
            # card shrinks to the left; the entry opens out of the trivia line
            s = 0.5
            home = self.frame.get_center()
            target_c = np.array([-6.6 + self.frame.width * s / 2, 0, 0])
            self.play(self.frame.animate.scale(s, about_point=home).shift(target_c - home),
                      self.code.animate.scale(s, about_point=home).shift(target_c - home),
                      run_time=1.2)
            note = coogan_note(width=7.4)
            note.move_to([(-0.9 + 6.6) / 2, 0, 0])
            self.note = note
            trivia = self.code.line(KID_LINES.index(L_TRIVIA))
            cols = [g.get_color() for g in trivia]
            self.play(*recolor(trivia, YELLOW), run_time=0.6)
            settle(self, self.code)
            tie = Line(trivia.get_right() + RIGHT * 0.12, note.get_left(), stroke_width=2.5, color=DIM)
            self.note = VGroup(tie, note)
            self.play(Create(tie), *during(appear(note, shift=None), 0.4, 1), run_time=1.5)   # early: the stored entry, the voice paraphrases it
            c.wait_until("tree")
            self.play(*disappear(tie, note), *[g.animate.set_color(cl) for g, cl in zip(trivia, cols)],
                      run_time=0.7)
            settle(self, self.code)
            self.play(self.frame.animate.scale(1 / s, about_point=target_c).shift(home - target_c),
                      self.code.animate.scale(1 / s, about_point=target_c).shift(home - target_c),
                      run_time=1.1)
            c.wait_until("branches")
            tree = S2.kid_tree()
            tree.scale_to_fit_height(min(tree.height, 7.0))
            if tree.width > 13.0:
                tree.scale_to_fit_width(13.0)
            tree.move_to(ORIGIN)
            self.tree = tree
            self.play(*during(disappear(self.frame, self.code), 0, 0.45),
                      *during(appear(tree, shift=None), 0.5, 1), run_time=1.4)
            c.wait_until("the cast")
            self.play(FlashAround(tree.node("actors"), time_width=1.5),
                      *recolor([tree.label("actors")], YELLOW), run_time=1.4)
            c.wait_until("roles one level")
            self.play(FlashAround(tree.node("actors", 0, "roles"), time_width=1.5),
                      *recolor([tree.label("actors", 0, "roles")], YELLOW), run_time=1.4)
            settle(self, tree)

    # ------------------------------------------------------------------ c4.movie.5
    def clip5(self):
        with self.say("c4.movie.5") as c:
            self.play(*during(disappear(self.tree), 0, 0.45),
                      *during(appear(self.frame, self.code, shift=None), 0.5, 1),
                      run_time=min(1.4, c.until("comments")))
            c.wait_until("comments")
            boxes = [SurroundingRectangle(g, color=RED, buff=0.07).set_stroke(RED, 3)
                     for g in comment_glyphs(self.code)]
            self.play(LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.4), run_time=1.5)
            c.wait_until("valid")
            s = 0.5
            P = self.frame.get_left()
            v = np.array([-6.6, 0, 0]) - P
            moves = [m.animate.scale(s, about_point=P).shift(v) for m in [self.frame, self.code, *boxes]]
            self.play(*moves, run_time=1.2)
            x0 = -1.1
            q1 = Code("SELECT json_valid(movie)\nFROM movies\nWHERE movie_id = 'tt0012349';", size=24)
            q2 = Code("SELECT json_valid(\n  '{\"trivia_entries\": [/* 5 items */ ]}');", size=22)
            r1 = one_cell("true", GREEN)
            r2 = one_cell("false", RED)
            col = VGroup(q1, r1, q2, r2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            col.move_to([0, 0, 0])
            for mob in (r1, r2):
                mob.shift(UP * 0.05)
            q2.shift(DOWN * 0.25)
            r2.shift(DOWN * 0.25)
            col.shift(RIGHT * (x0 - col.get_left()[0]))
            self.play(*appear(q1), run_time=1.0)   # early: the query shown, its reply on the next line
            c.wait_until("the real document")
            self.play(*appear(r1), run_time=1.0)   # early: the reply lands as the voice reads it
            c.wait_until("invalid")
            self.play(*appear(q2), run_time=0.8)   # early: the shorthand query
            self.play(*appear(r2), run_time=0.8)   # early: its reply
        self.wait(3.0)
