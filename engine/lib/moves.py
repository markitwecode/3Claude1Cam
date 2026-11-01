"""The transition vocabulary: how things appear, leave, change and come out of other things, with
fixed styles, so no frame between two settled states is a jumble (glitch study 2026-10-28,
docs/glitch-study-2026-10-28.md). Re-exported by lib.kit.

Every move returns a list of animations for play(), like the kit's other helpers, and takes the
usual narration timing: the play's run_time stretches the whole move, and the move only fixes the
order, overlap and fade shape (its phases are fractions of the play):

    self.play(*swap(question, answer), run_time=min(1.2, c.until("so the answer")))

    appear(*mobs)            new things fade in whole (never letter by letter); labels drop into place
    disappear(*mobs)         things fade out whole
    swap(old, new)           one thing replaces another in place: old rises out, then new rises in
    edit(old, new)           a text is rewritten keeping what's shared; no two moving glyphs cross
    fly(src, dst)            a new thing comes out of an old one (TransformFromCopy, without the
                             doubled start or the letter salad between unlike texts)
    derive(scene, src, dst)  a trace line born from the line above (plays twice, like sweep_clear)
    during(anims, a, b)      run animations only in [a, b] of their play (fractions of run_time)

What they replace, and why (counts from the study's 187 findings): Transform / ReplacementTransform /
TransformFromCopy between different texts morph glyph outlines into each other (43); a copy that
starts opaque on its source reads as doubled text (40); TransformMatchingShapes/Strings let glyphs
cross (8); Write and lag_ratio on text show half-words (16).
"""
from difflib import SequenceMatcher

import numpy as np
from manim import DOWN, PI, UP, Animation, AnimationGroup, FadeIn, FadeOut, Transform, config
from manim.animation.animation import prepare_animation
from manim.utils.paths import path_along_arc
from manim.utils.rate_functions import smooth


__all__ = [
    "appear", "disappear", "swap", "edit", "fly", "derive", "during",
    "APPEAR_RT", "DISAPPEAR_RT", "SWAP_RT", "EDIT_RT", "FLY_RT", "DERIVE_RT", "LABEL_SHIFT", "RISE",
]

APPEAR_RT = 1.0          # default run_times (a run_time= in play() overrides them)
DISAPPEAR_RT = 0.8
SWAP_RT = 1.2
EDIT_RT = 1.5
FLY_RT = 1.5
DERIVE_RT = 2.0
LABEL_SHIFT = 0.25 * DOWN   # labels drop toward what they name
RISE = 0.2 * UP             # swap: the old thing rises out, the new one rises into place

_SWAP_OUT, _SWAP_IN = (0.0, 0.45), (0.45, 1.0)
_EDIT_OUT, _EDIT_MOVE, _EDIT_IN = (0.0, 0.35), (0.2, 0.85), (0.65, 1.0)


# ── timing within a play ────────────────────────────────────────────────────────
def _span(anim, a, b):
    """anim runs only during [a, b] of its play (fractions), holding its start state before and its
    end state after. Works inside play(run_time=...) and inside AnimationGroups. Nested spans compose;
    the effective span is kept in anim.rel_span (sweep_clear and vk check read it)."""
    if not 0 <= a < b <= 1:
        raise ValueError("need 0 <= a < b <= 1")
    anim = prepare_animation(anim)
    inner = anim.interpolate

    def spanned(alpha):
        inner(float(np.clip((alpha - a) / (b - a), 0.0, 1.0)))

    anim.interpolate = spanned   # instance attribute shadows the method (as effects.time_span)
    p = getattr(anim, "rel_span", (0.0, 1.0))
    anim.rel_span = (a + p[0] * (b - a), a + p[1] * (b - a))
    return anim


def during(anims, a, b):
    """Run one animation or a list of them only during [a, b] of their play, as fractions of its
    run_time (time_span's relative twin, so it follows c.until(...) timing). The standard handover
    in one play: what leaves (0, 0.45), moves (0.2, 0.8), what arrives (0.5, 1)."""
    return [_span(x, a, b) for x in (anims if isinstance(anims, (list, tuple)) else [anims])]


def _flat(mobs):
    out = []
    for m in mobs:
        out.extend(_flat(m) if isinstance(m, (list, tuple)) else [m])
    return out


def _lagged(anims, lag):
    """One span per animation, staggered like LaggedStart(lag_ratio=lag), without its wrapper group."""
    n = len(anims)
    if n == 1:
        return anims
    d = 1.0 / (1.0 + lag * (n - 1))
    return [_span(x, k * lag * d, min(1.0, k * lag * d + d)) for k, x in enumerate(anims)]


# ── appear / disappear ─────────────────────────────────────────────────────────
def appear(*mobs, shift=LABEL_SHIFT, lag=0.25):
    """Each mob fades in whole, moving by `shift` (labels drop toward what they name; pass
    shift=None for none). Several mobs come in one after another (lag between mobs, never between
    the letters of one text)."""
    out = []
    for m in _flat(mobs):
        a = FadeIn(m, shift=shift) if shift is not None else FadeIn(m)
        a.run_time = APPEAR_RT
        out.append(a)
    return _lagged(out, lag)


def disappear(*mobs, lag=0.0):
    """Each mob fades out whole (lag > 0: one after another)."""
    out = []
    for m in _flat(mobs):
        a = FadeOut(m)
        a.run_time = DISAPPEAR_RT
        out.append(a)
    return _lagged(out, lag) if lag else out


# ── swap ───────────────────────────────────────────────────────────────────────
def swap(old, new, shift=RISE):
    """One thing replaces another, never a morph: old fades out rising by `shift` during the first
    45% of the play, new fades in rising into place during the rest. No frame shows both.
    The question → answer move, a value or caption update, a card replaced."""
    o = _span(FadeOut(old, shift=shift), *_SWAP_OUT)
    i = _span(FadeIn(new, shift=shift), *_SWAP_IN)
    o.run_time = i.run_time = SWAP_RT
    return [o, i]


# ── glyph identity ──────────────────────────────────────────────────────────────
GLYPH_TOL = 0.02   # same glyph at different font sizes differs by ≤ 0.001 here; different glyphs by > 0.2


def _pieces(mob):
    return mob.family_members_with_points()


def _norm_points(m):
    return (m.points - m.get_center()) / max(m.width, m.height, 1e-6)


def glyph_classes(*groups):
    """One list of class ids per group of pieces: equal ids = the same shape, whatever the size,
    colour or position (normalised outlines within GLYPH_TOL; effects._shape_key's exact rounding
    splits a glyph rendered at two font sizes)."""
    reps, out = [], []
    for g in groups:
        ids = []
        for m in g:
            q = _norm_points(m)
            k = next((i for i, r in enumerate(reps) if r.shape == q.shape and np.abs(r - q).max() <= GLYPH_TOL), None)
            if k is None:
                reps.append(q)
                k = len(reps) - 1
            ids.append(k)
        out.append(ids)
    return out


def same_glyphs(a, b):
    """True when a and b are made of the same shapes in the same order (any size/colour/place)."""
    pa, pb = _pieces(a), _pieces(b)
    if len(pa) != len(pb):
        return False
    ka, kb = glyph_classes(pa, pb)
    return ka == kb


# ── edit ───────────────────────────────────────────────────────────────────────

def _term_pairs(pairs, n_src, n_trg):
    """Maths edits: a lone matched glyph next to a changed one belongs to the changed term, so the
    term swaps whole. Otherwise the shared glyphs alone, between the fade-out and the fade-in, can read
    as a wrong formula (2026-11-01, math L11 ch3: e^{2y} → (e^y)^2 kept the e and the 2 and showed
    "e² − 2x e^y − 1 = 0" for ~0.5 s). Repeated until stable; runs of 2+ glyphs still slide."""
    pairs = list(pairs)
    while True:
        ms, mt = {i for i, _ in pairs}, {j for _, j in pairs}
        lone = set()
        for k, (i, j) in enumerate(pairs):
            run = ((k > 0 and pairs[k - 1] == (i - 1, j - 1)) or
                   (k + 1 < len(pairs) and pairs[k + 1] == (i + 1, j + 1)))
            if run:
                continue
            near_change = ((i > 0 and i - 1 not in ms) or (i + 1 < n_src and i + 1 not in ms) or
                           (j > 0 and j - 1 not in mt) or (j + 1 < n_trg and j + 1 not in mt))
            if near_change:
                lone.add(k)
        if not lone:
            return pairs
        pairs = [p for k, p in enumerate(pairs) if k not in lone]


class _Edit(AnimationGroup):
    """See edit(). The end-state handling is TransformMatchingStrings': the source is put back as it
    was and taken off screen with the helper copies; the target is shown."""

    def __init__(self, old, new, min_shared=0.5, **kwargs):
        src, trg = _pieces(old), _pieces(new)
        if not src or not trg:
            raise ValueError("edit() needs two texts with glyphs (use appear/disappear for one side)")
        k1, k2 = glyph_classes(src, trg)
        blocks = SequenceMatcher(None, k1, k2, autojunk=False).get_matching_blocks()
        pairs = [(b.a + i, b.b + i) for b in blocks for i in range(b.size)]
        from manim import MathTex, Tex
        if isinstance(old, (MathTex, Tex)) or isinstance(new, (MathTex, Tex)):
            pairs = _term_pairs(pairs, len(src), len(trg))
        self.fade_in_copies, anims = [], []
        if pairs and len(pairs) >= min_shared * min(len(src), len(trg)):
            used_s, used_t = {i for i, _ in pairs}, {j for _, j in pairs}
            anims += [_span(Transform(src[i], trg[j]), *_EDIT_MOVE) for i, j in pairs]
            anims += [_span(FadeOut(m), *_EDIT_OUT) for i, m in enumerate(src) if i not in used_s]
            for j, m in enumerate(trg):
                if j not in used_t:
                    c = m.copy()
                    self.fade_in_copies.append(c)
                    anims.append(_span(FadeIn(c), *_EDIT_IN))
        else:   # little in common: a swap, glyph by glyph so the clean-up is the same
            anims += [_span(FadeOut(m, shift=RISE), *_SWAP_OUT) for m in src]
            for m in trg:
                c = m.copy()
                self.fade_in_copies.append(c)
                anims.append(_span(FadeIn(c, shift=RISE), *_SWAP_IN))
        self.source, self.target, self.shared = old, new, len(pairs)
        kwargs.setdefault("run_time", EDIT_RT)
        super().__init__(*anims, **kwargs)

    def clean_up_from_scene(self, scene):
        for anim in self.animations:
            anim.interpolate(0)
        scene.remove(self.mobject, self.source, *self.fade_in_copies)
        scene.add(self.target)


def edit(old, new):
    """Rewrite a text (Text, Code, MathTex; `old` a whole on-screen object, `new` not yet shown)
    keeping what's shared. Glyphs are paired by an order-preserving diff of their shapes (size, colour
    and position don't matter), so no two moving glyphs cross: shared glyphs slide and recolour to
    their new place (20–85% of the play), dropped glyphs fade out where they are (0–35%), new glyphs
    fade in where they land (65–100%). When under half of the shorter text is shared (or the fonts
    differ) it is a swap. `new` ends on screen as one object. For deliberate reorders (reversing a
    list) move the tokens yourself, on arcs that don't collide."""
    return [_Edit(old, new)]


# ── fly / derive ───────────────────────────────────────────────────────────────
def _clear_alpha(src, dst, cap=0.9):
    """The play fraction (rate func smooth) by which a copy moving src → dst has left src's box on
    either axis (its size interpolated on the way): it stays faint until then, so it never reads as
    doubled text. In [0.2, cap]. (2026-11-01: the old test looked at one axis only and was capped at
    0.6, so a line dropping to a close row went opaque while still on its source.)"""
    d = dst.get_center() - src.get_center()
    ws, hs, wd, hd = src.width, src.height, dst.width, dst.height
    for x in np.linspace(0.0, cap, int(round(cap * 100)) + 1):
        p = smooth(x)
        wc, hc = ws + (wd - ws) * p, hs + (hd - hs) * p
        if abs(p * d[0]) >= (ws + wc) / 2 or abs(p * d[1]) >= (hs + hc) / 2:
            return float(max(x, 0.2))
    return float(cap)


def _on_screen(m, margin=0.3):
    """Shift `m` sideways so it sits inside the frame (left edge first if it's wider than the frame)."""
    half = config.frame_width / 2 - margin
    if m.get_left()[0] < -half:
        m.shift(np.array([-half - m.get_left()[0], 0.0, 0.0]))
    elif m.get_right()[0] > half:
        m.shift(np.array([half - m.get_right()[0], 0.0, 0.0]))
    return m


def _ramp(alpha, a_clear):
    """0 for the first half of the way to clear, then up to 1 when clear."""
    return smooth(float(np.clip((alpha / a_clear - 0.5) / 0.5, 0.0, 1.0)))


def _fly_ramp(alpha, a_clear):
    """_FlyCopy's opacity: a faint ghost (at most 0.25, under vk check's 0.3 "drawn over" line) until
    the copy has left its source, then up to 1 over half the remaining way (2026-11-01: the old ramp
    reached ~0.5 while still on the source, so close rows read as doubled text)."""
    if alpha <= a_clear:
        return 0.25 * smooth(float(np.clip((alpha / a_clear - 0.6) / 0.4, 0.0, 1.0)))
    end = a_clear + 0.5 * (1.0 - a_clear)
    return 0.25 + 0.75 * smooth(float(np.clip((alpha - a_clear) / max(end - a_clear, 1e-6), 0.0, 1.0)))


def _fade_family(mob, k):
    if k >= 1.0:
        return
    for m in mob.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * k, family=False)
        m.set_stroke(opacity=m.get_stroke_opacity() * k, family=False)
        if m.get_stroke_width(background=True) > 0:
            m.set_stroke(opacity=m.get_stroke_opacity(background=True) * k, background=True, family=False)


def _auto_arc(src, dst, arc):
    """Straight by default; an upward bulge only for a move along the same row, where a straight
    path would slide the copy through that row's other text. (A curved approach into a formula
    from another row grazes the neighbours of the slot it lands in.)"""
    if arc is not None:
        return arc
    d = dst.get_center() - src.get_center()
    if abs(d[1]) > 0.5 * max(src.height, dst.height, 0.2):
        return 0.0
    return PI / 3 if d[0] > 0 else -PI / 3


class _FlyCopy(Transform):
    """TransformFromCopy(src, dst) whose copy stays faint until it has left its source."""

    def __init__(self, src, dst, path_arc=0.0, **kwargs):
        self.a_clear = _clear_alpha(src, dst)
        kwargs.setdefault("run_time", FLY_RT)
        super().__init__(dst, src.copy(), path_arc=path_arc, **kwargs)

    def interpolate(self, alpha):
        super().interpolate(1 - alpha)
        _fade_family(self.mobject, _fly_ramp(alpha, self.a_clear))


class _Carry(Animation):
    """A copy of src, unchanged in shape, travels to dst (scaling to its height) and fades away just
    before dst fades in there: no morph between unlike glyphs, no frame with both."""

    def __init__(self, src, dst, path_arc=0.0, out=(0.55, 0.8), **kwargs):
        self.start_copy = src.copy()
        self.p0, self.p1 = src.get_center(), dst.get_center()
        sh, dh = max(src.height, 1e-6), max(dst.height, 1e-6)
        self.s1 = dh / sh if src.height > 0.05 and dst.height > 0.05 else 1.0
        self.path = path_along_arc(path_arc)
        self.a_clear, self.out = _clear_alpha(src, dst, cap=0.6), out   # visible before its fade-out
        kwargs.setdefault("run_time", FLY_RT)
        super().__init__(src.copy(), remover=True, introducer=True, **kwargs)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        m = self.mobject.become(self.start_copy)
        c = self.path(np.array([self.p0]), np.array([self.p1]), a)[0]
        m.scale(1 + (self.s1 - 1) * a).move_to(c)
        k_out = 1 - smooth(float(np.clip((alpha - self.out[0]) / (self.out[1] - self.out[0]), 0, 1)))
        _fade_family(m, _ramp(alpha, self.a_clear) * k_out)


def fly(src, dst, arc=None):
    """A new thing comes out of an old one: a copy of `src` travels to `dst` (which ends on screen;
    `src` stays). Same glyphs (same text and font, any size or colour): the copy becomes dst, faint
    until it has left src, so it never sits doubled on its source. Different glyphs or shapes: the
    copy flies unchanged, scaled to dst's height, and fades out just before dst fades in at its place
    (80–100%). `arc`: path angle; default straight, bulging upward only along the same row."""
    arc = _auto_arc(src, dst, arc)
    if same_glyphs(src, dst):
        return [_FlyCopy(src, dst, path_arc=arc)]
    i = _span(FadeIn(dst), 0.78, 1.0)
    i.run_time = FLY_RT
    return [_Carry(src, dst, path_arc=arc), i]


def derive(scene, src, dst, *extra, run_time=DERIVE_RT, split=0.45):
    """A trace line born from the line above, in two plays (like sweep_clear, it calls scene.play):
    a whole copy of `src` drops rigidly to `dst`'s row, aligned on their longest shared run of glyphs
    (first `split` of run_time), then edit()s into `dst` in place. Pieces never cross. `extra`
    animations (the ⇒ arrow, a highlight box) run with the first play. `src` stays; `dst` ends on
    screen as one object. run_time follows narration timing: derive(self, a, b, run_time=c.until(…))."""
    sp, dp = _pieces(src), _pieces(dst)
    k1, k2 = glyph_classes(sp, dp)
    m = SequenceMatcher(None, k1, k2, autojunk=False).find_longest_match(0, len(k1), 0, len(k2))
    if m.size:
        delta = dp[m.b].get_center() - sp[m.a].get_center()   # that run lands exactly in place
    else:
        delta = np.array([dst.get_left()[0] - src.get_left()[0], dst.get_y() - src.get_y(), 0.0])
    moved = _on_screen(src.copy().shift(delta))   # the run alignment can push it past an edge
    scene.play(_FlyCopy(src, moved, path_arc=0.0), *extra, run_time=run_time * split)
    step = edit(moved, dst)
    for a in step:
        a.dwell_exempt = True   # the copy's glyphs were on screen all along, on src: not a reading-time loss
    scene.play(*step, run_time=run_time * (1 - split))
