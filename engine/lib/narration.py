"""Sync manim animations to the narration clips made by tools/voice.py.

    class MyScene(NarratedScene):
        def construct(self):
            with self.say("cons.3") as c:          # starts the audio clip now
                self.play(FadeIn(x), run_time=c.until("shuffle"))
                c.wait_until("nope")               # idle until the word after {nope}
                self.play(Create(y))
                c.wait_until("the list that was")  # ...or until any spoken phrase
            # leaving the block waits out the rest of the clip (plus a short gap)

A cue is either a {mark} name from script.md or a phrase spoken in that clip
(case and punctuation ignored; `nth=1` for its second occurrence). Phrase cues
come from Whisper word timings, so they stay in sync when a clip is re-voiced:
never hard-code seconds.

`c.until(cue)` is the time from *now* until the cue, so it can be used directly
as a run_time; it never returns less than `floor`, so an animation that is
running late still gets a sane duration.
"""
import inspect
import json
import re
from contextlib import contextmanager
from pathlib import Path

from manim import Scene, config

from lib.paths import project


def _patch_pillow13_image_canvas():
    """Manim CE 0.22's Camera.display_image_mobject pastes into Image.fromarray(np.zeros((h, w)),
    mode="RGBA"), which Pillow 13 rejects ("Invalid mode for data type"), so no ImageMobject
    renders. Shim just that call with the blank RGBA canvas it meant (studio-tour ch1, 2026-10-28)."""
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


_patch_pillow13_image_canvas()

ROOT = project()   # the project folder: audio/manifest.json, audio/*.wav, media/cues/
_MANIFEST = None


def manifest():
    global _MANIFEST
    if _MANIFEST is None:
        _MANIFEST = json.loads((ROOT / "audio" / "manifest.json").read_text())
    return _MANIFEST


def _norm(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


_STOP = set("this that with from have what when then them they their there here into onto only each "
            "over your just than also more most less very does done will would been were where which "
            "while about after before again every other these those being still".split())


def label_text(label):
    """The string a label shows: a Text's text, a MathTex/Tex's source, a Code's src, or str()."""
    for attr in ("original_text", "src", "tex_string"):
        v = getattr(label, attr, None)
        if isinstance(v, str):
            return v
    return str(label)


def label_words(label):
    """A label's distinctive words, normalised like the manifest's: alphabetic, 4+ letters, not a
    stop word. "≈ 300 images" -> ["images"]. Shared by Clip.own_word_time and vk check's early rule."""
    out = []
    for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", label_text(label)):
        n = _norm(w)
        if len(n) >= 4 and n.isalpha() and n not in _STOP:
            out.append(n)
    return out


class Clip:
    def __init__(self, scene, cid, info, start):
        self.scene, self.id, self.info, self.start = scene, cid, info, start
        self.duration = info["duration"]
        self.end = start + self.duration
        self._words = [(_norm(w), t) for w, t in info.get("words", [])]

    def at(self, cue=None, nth=0, own_word=None):
        """Absolute scene time of a {mark} or of the first word of a spoken phrase.
        own_word=<a Text label>: instead, when that label's own word is said: the first of its
        distinctive words (4+ letters) spoken from now on, so `c.wait_until(own_word=label)` lands
        the label on its word. With `cue` too, the cue is the fallback when none of its words are
        spoken in this clip (KeyError otherwise)."""
        if own_word is not None:
            t = self.own_word_time(own_word)
            if t is not None:
                return t
            # the word began a hair ago: an entrance ran just past it, and frame rounding decides which
            # side (15 fps preview fine, 60 fps final raised: DB L5 ch1 s1, 2026-11-01). Land it now.
            now = self.scene.time
            words = set(label_words(own_word))
            if any(w in words and now - 0.5 <= self.start + t < now for w, t in self._words):
                return now
            if cue is None:
                raise KeyError(f"{self.id}: none of the words of {label_text(own_word)!r} are spoken "
                               f"from here on; pass a cue. Text: {self.info['text']!r}")
        if cue is None:
            raise TypeError("at() needs a cue or own_word=")
        if cue in self.info["marks"]:
            return self.start + self.info["marks"][cue]
        toks = [_norm(w) for w in cue.split() if _norm(w)]
        norms = [w for w, _ in self._words]
        hits = [i for i in range(len(norms) - len(toks) + 1) if toks and norms[i:i + len(toks)] == toks]
        if len(hits) <= nth:
            raise KeyError(f"{self.id}: no mark or phrase {cue!r} (nth={nth}). "
                           f"Marks: {list(self.info['marks'])}. Text: {self.info['text']!r}")
        # same small lead as the {marks} get, so visuals land just before the word
        return self.start + max(0.0, self._words[hits[nth]][1] - 0.05)

    def own_word_time(self, label, after=None):
        """When `label`'s first distinctive word (4+ letters, see label_words) is next spoken in this
        clip, at or after `after` (default: now), or None."""
        words = set(label_words(label))
        after = self.scene.time if after is None else after
        for w, t in self._words:
            if w in words and self.start + t >= after - 0.05:
                return self.start + max(0.0, t - 0.05)
        return None

    def until(self, cue=None, floor=0.3, nth=0, own_word=None):
        """Seconds from now until `cue` (or the end of the clip), at least `floor`."""
        target = self.end if cue is None and own_word is None else self.at(cue, nth, own_word)
        return max(floor, target - self.scene.time)

    def wait_until(self, cue=None, nth=0, own_word=None):
        """Idle until `cue` (or the end of the clip); no-op if already past it."""
        target = self.end if cue is None and own_word is None else self.at(cue, nth, own_word)
        gap = target - self.scene.time
        if gap > 1 / 30:
            self.scene.wait(gap)

    @property
    def remaining(self):
        return max(0.0, self.end - self.scene.time)


class NarratedScene(Scene):
    gap = 0.35  # breathing room after each clip

    @contextmanager
    def say(self, cid, gap=None):
        info = manifest()[cid]
        # A play() served from manim's cache leaves the renderer in "skipping" mode
        # until the next play(), and manim silently drops sounds added while skipping.
        # Restore the real status first (exactly what play() itself does on entry).
        r = self.renderer
        r.skip_animations = r._original_skipping_status
        r.update_skipping_status()
        self.add_sound(str(ROOT / info["file"]))
        # exact start of every clip, for music cues placed relative to narration lines
        self.__dict__.setdefault("_cue_log", []).append({"id": cid, "start": round(self.time, 4)})
        clip = Clip(self, cid, info, self.time)
        yield clip
        clip.wait_until()
        # an explicit gap= wins, then a scene's own class gap, then the line's varied gap
        # from `vk regap` (manifest "gap_after"), then the default
        if gap is not None:
            g = gap
        elif self.gap != NarratedScene.gap:
            g = self.gap
        else:
            g = info.get("gap_after", self.gap)
        if g > 0:
            self.wait(g)

    def tear_down(self):
        """Write media/cues/<scene file>_<res>.json: when each clip starts in the rendered video.

        Only real renders write it: a dry run's clock skips the per-play rounding to whole
        frames, so its times drift slightly from the actual video."""
        super().tear_down()
        if config.dry_run:
            return
        stem = Path(inspect.getfile(type(self))).stem
        res = f"{config.pixel_height}p{round(config.frame_rate)}"
        out = ROOT / "media" / "cues" / f"{stem}_{res}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"scene": type(self).__name__, "duration": round(self.time, 4),
                                   "clips": self.__dict__.get("_cue_log", [])}, indent=1))
