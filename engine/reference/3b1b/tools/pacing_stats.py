#!/usr/bin/env python3
"""Static pacing statistics over 3Blue1Brown's ManimGL video source.

Parses (never executes) every .py file under the given year directories with
`ast` and measures, for every `self.play(...)` / `self.wait(...)` call:

  * explicit run_time values (play-level kwarg, and any run_time kwarg nested
    inside the play's animations),
  * wait() durations (bare wait() = manimlib default_wait_time = 1.0 s, see
    manimgl/manimlib/scene/scene.py:77 and default_config.yml:86),
  * lag_ratio usage and values,
  * animation classes (top-level args of play, plus every nested call whose
    name is a known animation class), and `.animate` method chains,
  * plays / waits per scene (a "scene" = a ClassDef that defines construct()),
  * the play -> wait rhythm (how many plays happen back to back before a wait),
    and "beats" (a run of plays plus the wait(s) after it, in seconds),
  * FadeIn/FadeOut shift directions, rate_func overrides, first/last call in construct,
  * a rough per-scene duration estimate for straight-line scenes (no play or
    wait inside a loop, every duration resolvable).

Usage (stdlib only):
    python3 -I reference/3b1b/tools/pacing_stats.py                 # 2023-2026
    python3 -I reference/3b1b/tools/pacing_stats.py --years 2024     # one year
    python3 -I reference/3b1b/tools/pacing_stats.py --by-project     # per project
    python3 -I reference/3b1b/tools/pacing_stats.py --json out.json  # raw numbers
    python3 -I reference/3b1b/tools/pacing_stats.py --projects _2024/transformers _2026/cross_entropy
    python3 -I reference/3b1b/tools/pacing_stats.py --exclude robot.py p6.py
    python3 -I reference/3b1b/tools/pacing_stats.py --examples FlashAround
                                                    # print file:line of uses

Python >= 3.12 is needed to parse _2026/cross_entropy/entropy.py (PEP 701 f-strings).
Under an older python3 the script re-executes itself with python3.12+ if one is on PATH
(set PACING_STATS_NO_REEXEC=1 to stop that); otherwise that file is reported and skipped. _2023/optics_puzzles/
slowing_waves_insert_embed.py is genuinely unparseable (a stray self.embed()).

Caveat: these are static counts of source code. Loops, helper methods and
variables mean the static count is not the rendered count; Grant also renders
many short scenes and edits them against narration in post, so a wait() is
often a placeholder for "hold here while I talk".
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.normpath(os.path.join(HERE, "..", "videos"))
MANIMLIB_ANIM = os.path.normpath(os.path.join(HERE, "..", "manimgl", "manimlib", "animation"))

DEFAULT_WAIT = 1.0  # manimlib/scene/scene.py:77, default_config.yml:86

# Class-level default run_times from manimlib/animation/*.py (checked by hand).
# Everything else that is an Animation defaults to DEFAULT_ANIMATION_RUN_TIME = 1.0
# (animation.py:19).
CLASS_DEFAULT_RUN_TIME = {
    "DrawBorderThenFill": 2.0,          # creation.py:78
    "Write": 1.5,                       # creation.py:173: 1 s if <15 sub-paths else 2 s
    "TransformMatchingParts": 2.0,      # transform_matching_parts.py:29
    "TransformMatchingShapes": 2.0,
    "TransformMatchingStrings": 2.0,
    "TransformMatchingTex": 2.0,
    "LaggedStartMap": 2.0,              # composition.py:172
    "FocusOn": 2.0,                     # indication.py:47
    "WiggleOutThenIn": 2.0,             # indication.py:364
    "Homotopy": 3.0,                    # movement.py:24
    "Rotating": 5.0,                    # rotation.py:25
    "Broadcast": 3.0,                   # specialized.py:25
    "ApplyPointwiseFunction": 3.0,      # transform.py:198
    "ApplyMatrix": 3.0,
}
GROUP_CLASSES = {"AnimationGroup", "LaggedStart", "Succession"}
# Pi-creature animations (custom/characters/): reported, but not something we copy.
PI_CREATURE_CALLS = {
    "change", "says", "thinks", "change_students", "debubble", "Blink", "change_mode",
    "look_at", "teacher_says", "student_says", "teacher_thinks", "student_thinks",
    "RemovePiCreatureBubble", "PiCreatureSays", "PiCreatureBubbleIntroduction", "BlinkPiCreature",
}


# Line-level idiom counts (regex per source line, comment lines skipped). Reproducible
# stand-ins for "how often does he do X" in PATTERNS.md.
IDIOMS = {
    "FlashAround(": r"\bFlashAround\(",
    "FlashUnder(": r"\bFlashUnder\(",
    "Indicate(": r"\bIndicate\(",
    "VShowPassingFlash(": r"\bVShowPassingFlash\(",
    "SurroundingRectangle(": r"\bSurroundingRectangle\(",
    ".animate.surround(": r"\.animate\.surround\(",
    "Underline(": r"\bUnderline\(",
    ".set_backstroke(": r"\.set_backstroke\(",
    ".animate.set_opacity(": r"\.animate\.set_opacity\(",
    ".animate.fade(": r"\.animate\.fade\(",
    ".save_state()": r"\.save_state\(\)",
    "Restore(": r"\bRestore\(",
    "Brace(": r"\bBrace\(",
    "brace.get_text/get_tex(": r"brace\w*\.get_te(x|xt)\(",
    "GrowFromCenter(...brace": r"GrowFromCenter\(\w*brace",
    "GrowArrow(": r"\bGrowArrow\(",
    "ShowCreation(...arrow": r"ShowCreation\(\w*arrow",
    "t2c=": r"\bt2c\s*=",
    "TransformMatchingTex(": r"\bTransformMatchingTex\(",
    "TransformMatchingStrings(": r"\bTransformMatchingStrings\(",
    "key_map=": r"\bkey_map\s*=",
    "matched_keys=": r"\bmatched_keys\s*=",
    "TransformFromCopy(": r"\bTransformFromCopy\(",
    "FadeTransform(": r"\bFadeTransform\(",
    "self.clear()": r"self\.clear\(\)",
    "LaggedStartMap(FadeOut": r"LaggedStartMap\(\s*FadeOut",
    "Group(*self.mobjects)": r"Group\(\*self\.mobjects\)",
    ".to_corner( after .animate": r"\.animate\..*\.to_corner\(",
    "frame.save_state()": r"frame\.save_state\(\)",
    "Restore(frame": r"Restore\(\s*(self\.)?frame",
    ".fix_in_frame()": r"\.fix_in_frame\(\)",
    "question marks (?, ???, q_marks)": r"(\"\?+\"|R\"\?+\"|q_marks?\b)",
    "BackgroundRectangle(": r"\bBackgroundRectangle\(",
    "ValueTracker(": r"\bValueTracker\(",
    "ChangeDecimalToValue(": r"\bChangeDecimalToValue\(",
    "CountInFrom(": r"\bCountInFrom\(",
    "make_number_changeable(": r"make_number_changeable\(",
    "ShowIncreasingSubsets(": r"\bShowIncreasingSubsets\(",
}
IDIOM_RES = {k: re.compile(v) for k, v in IDIOMS.items()}


def load_animation_class_names() -> set[str]:
    names = set()
    if os.path.isdir(MANIMLIB_ANIM):
        for fn in os.listdir(MANIMLIB_ANIM):
            if fn.endswith(".py"):
                with open(os.path.join(MANIMLIB_ANIM, fn), encoding="utf-8") as f:
                    names.update(re.findall(r"^class (\w+)\(", f.read(), flags=re.M))
    return names


ANIM_CLASSES = load_animation_class_names()


# --------------------------------------------------------------------------- helpers
def call_name(node: ast.AST) -> str | None:
    """Name of the callable: Foo(...) -> 'Foo', mod.Foo(...) -> 'Foo'."""
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Name):
            return f.id
        if isinstance(f, ast.Attribute):
            return f.attr
    return None


def is_self_method(node: ast.AST, method: str) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == method
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "self"
    )


def literal_number(node: ast.AST | None):
    if node is None:
        return None
    try:
        v = ast.literal_eval(node)
    except Exception:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def kwarg(node: ast.Call, name: str):
    for kw in node.keywords:
        if kw.arg == name:
            return kw.value
    return None


def animate_chain(node: ast.AST) -> list[str] | None:
    """For mob.animate.shift(..).scale(..) return ['shift', 'scale'], else None."""
    methods = []
    cur = node
    while isinstance(cur, ast.Call) and isinstance(cur.func, ast.Attribute):
        methods.append(cur.func.attr)
        cur = cur.func.value
    if isinstance(cur, ast.Attribute) and cur.attr == "animate":
        return list(reversed(methods))
    return None


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return float("nan")
    k = (len(sorted_vals) - 1) * p / 100.0
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def summary(vals: list[float]) -> str:
    if not vals:
        return "n=0"
    s = sorted(vals)
    mean = sum(s) / len(s)
    return (
        f"n={len(s)}  mean={mean:.2f}  p10={percentile(s, 10):.2f}  p25={percentile(s, 25):.2f}  "
        f"median={percentile(s, 50):.2f}  p75={percentile(s, 75):.2f}  p90={percentile(s, 90):.2f}  "
        f"max={s[-1]:.2f}"
    )


def top_values(vals: list[float], k: int = 12) -> str:
    c = Counter(round(v, 3) for v in vals)
    tot = sum(c.values()) or 1
    return ", ".join(f"{_fmt(v)}:{n} ({100 * n / tot:.0f}%)" for v, n in c.most_common(k))


def _fmt(v: float) -> str:
    return f"{v:g}"


# --------------------------------------------------------------------------- analysis
class Stats:
    def __init__(self):
        self.files = 0
        self.parse_errors: list[str] = []
        self.plays = 0
        self.plays_in_loops = 0
        self.play_rt_explicit: list[float] = []          # play(..., run_time=<literal>)
        self.play_rt_nonliteral = 0
        self.nested_rt_explicit: list[float] = []        # Anim(..., run_time=<literal>) inside play
        self.any_rt_by_class: dict[str, list[float]] = defaultdict(list)
        self.plays_with_any_rt = 0
        self.waits_bare = 0
        self.waits_literal: list[float] = []
        self.waits_nonliteral = 0
        self.waits_in_loops = 0
        self.waits_with_note = 0
        self.lag_in_play = 0
        self.lag_values_all: list[float] = []            # every literal lag_ratio kwarg in the files
        self.lag_values_by_class: dict[str, list[float]] = defaultdict(list)
        self.lag_nonliteral = 0
        self.lagged_start_default = 0                    # LaggedStart/Map without lag_ratio
        self.top_classes = Counter()                     # top-level play args
        self.nested_classes = Counter()                  # all animation calls inside play
        self.animate_methods = Counter()
        self.args_per_play: list[int] = []
        self.starred_plays = 0
        self.rate_funcs = Counter()
        self.scene_plays: list[int] = []
        self.scene_waits: list[int] = []
        self.scene_records: list[dict] = []
        self.run_lengths: list[int] = []                 # consecutive plays before a wait
        self.play_followed_by_wait = 0
        self.play_checked_for_wait = 0
        self.straight_durations: list[float] = []
        self.straight_wait_share: list[float] = []
        self.examples: dict[str, list[str]] = defaultdict(list)
        self.misc = Counter()
        self.effective_play: list[float] = []            # explicit or class-default duration
        self.effective_play_unresolved = 0
        self.pi_plays = 0
        self.idiom_lines = Counter()
        self.idiom_files = Counter()
        self.camera_play_durations: list[float] = []     # plays that move frame.animate
        self.camera_play_unresolved = 0
        self.scene_first_call = Counter()
        self.scene_last_call = Counter()
        self.fade_shift = Counter()                      # FadeIn/FadeOut(mob, <shift>) usage
        self.fade_shift_values = Counter()
        self.beats: list[float] = []                     # plays + following waits, seconds
        self.beat_hold_share: list[float] = []

    # ------------------------------------------------------------------ per file
    def add_file(self, path: str, rel: str):
        self.files += 1
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                src = f.read()
            tree = ast.parse(src, filename=path)
        except SyntaxError as e:
            self.parse_errors.append(f"{rel}: {e.msg} (line {e.lineno})")
            return
        self._misc_counts(src)
        self._idiom_counts(src)
        parents = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        self._parents = parents

        # every literal lag_ratio anywhere (animations are often built before play)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node) or "?"
                lr = kwarg(node, "lag_ratio")
                if lr is not None:
                    v = literal_number(lr)
                    if v is None:
                        self.lag_nonliteral += 1
                    else:
                        self.lag_values_all.append(v)
                        self.lag_values_by_class[name].append(v)
                elif name in ("LaggedStart", "LaggedStartMap"):
                    self.lagged_start_default += 1
                if name in ANIM_CLASSES or name in GROUP_CLASSES:
                    self.examples[name].append(f"{rel}:{node.lineno}")
                if name in ("FadeIn", "FadeOut"):
                    shift = node.args[1] if len(node.args) > 1 else kwarg(node, "shift")
                    if shift is None:
                        self.fade_shift[f"{name} plain"] += 1
                    else:
                        self.fade_shift[f"{name} with shift"] += 1
                        self.fade_shift_values[ast.unparse(shift)[:20]] += 1
                    if kwarg(node, "scale") is not None:
                        self.fade_shift[f"{name} with scale"] += 1
            if isinstance(node, ast.Attribute) and node.attr in (
                "set_backstroke", "fix_in_frame", "reorient", "add_ambient_rotation",
            ):
                self.examples["." + node.attr].append(f"{rel}:{node.lineno}")

        for node in ast.walk(tree):
            if is_self_method(node, "play"):
                self._add_play(node, rel)
            elif is_self_method(node, "wait"):
                self._add_wait(node)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module,
                                 ast.For, ast.While, ast.If, ast.With, ast.Try)):
                for field in ("body", "orelse", "finalbody"):
                    stmts = getattr(node, field, None)
                    if isinstance(stmts, list):
                        self._rhythm(stmts)

        for node in tree.body if isinstance(tree, ast.Module) else []:
            if isinstance(node, ast.ClassDef):
                self._add_scene(node, rel)

    def _idiom_counts(self, src: str):
        hit_files = set()
        for line in src.splitlines():
            if line.lstrip().startswith("#"):
                continue
            for k, rx in IDIOM_RES.items():
                if rx.search(line):
                    self.idiom_lines[k] += 1
                    hit_files.add(k)
        for k in hit_files:
            self.idiom_files[k] += 1

    def _misc_counts(self, src: str):
        for key, pat in {
            "files_using_self.frame": r"self\.frame\b",
            "files_using_frame.animate": r"frame\.animate",
            "files_using_PiCreature": r"\b(PiCreature|Randolph|Mortimer|TeacherStudentsScene|PiCreatureScene)\b",
            "files_using_embed": r"self\.embed\(",
            "files_using_InteractiveScene": r"\bInteractiveScene\b",
            "files_using_t2c": r"\bt2c\s*=",
            "files_using_set_backstroke": r"set_backstroke\(",
            "files_using_Brace": r"\bBrace\(",
            "files_using_SurroundingRectangle": r"SurroundingRectangle\(",
            "files_using_DecimalNumber_or_Integer": r"\b(DecimalNumber|Integer)\(",
            "files_using_ValueTracker": r"ValueTracker\(",
            "files_using_add_updater_or_f_always": r"(add_updater\(|\.f_always\.|always_redraw\()",
        }.items():
            if re.search(pat, src):
                self.misc[key] += 1

    def _in_loop(self, node) -> bool:
        cur = self._parents.get(node)
        while cur is not None:
            if isinstance(cur, (ast.For, ast.While, ast.comprehension, ast.ListComp,
                                ast.GeneratorExp)):
                return True
            if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                return False
            cur = self._parents.get(cur)
        return False

    def _anim_duration(self, node) -> float | None:
        """Best-effort duration of one animation expression, None if unknown."""
        if isinstance(node, ast.Call):
            rt = kwarg(node, "run_time")
            if rt is not None:
                return literal_number(rt)
            chain = animate_chain(node)
            if chain is not None:
                cur = node  # mob.animate.foo().set_anim_args(run_time=2)
                while isinstance(cur, ast.Call) and isinstance(cur.func, ast.Attribute):
                    if cur.func.attr == "set_anim_args" and kwarg(cur, "run_time") is not None:
                        return literal_number(kwarg(cur, "run_time"))
                    cur = cur.func.value
                return 1.0
            name = call_name(node)
            if name in GROUP_CLASSES:
                return None
            if name in CLASS_DEFAULT_RUN_TIME:
                return CLASS_DEFAULT_RUN_TIME[name]
            if name in ANIM_CLASSES:
                return 1.0
        return None

    def _add_play(self, node: ast.Call, rel: str):
        self.plays += 1
        in_loop = self._in_loop(node)
        if in_loop:
            self.plays_in_loops += 1
        rt = kwarg(node, "run_time")
        if rt is not None:
            v = literal_number(rt)
            if v is None:
                self.play_rt_nonliteral += 1
            else:
                self.play_rt_explicit.append(v)
        rf = kwarg(node, "rate_func")
        if rf is not None:
            self.rate_funcs[ast.unparse(rf)[:30]] += 1

        n_args = 0
        starred = False
        any_rt = rt is not None
        has_lag = kwarg(node, "lag_ratio") is not None
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                starred = True
                self.top_classes["*starred"] += 1
                continue
            n_args += 1
            chain = animate_chain(arg)
            if chain is not None:
                self.top_classes[".animate"] += 1
                for m in chain:
                    self.animate_methods[m] += 1
            else:
                name = call_name(arg)
                self.top_classes[name if name else "<variable>"] += 1
                if isinstance(arg, ast.Call):
                    for sub in ast.walk(arg):
                        if isinstance(sub, ast.Call):
                            if kwarg(sub, "rate_func") is not None:
                                self.rate_funcs[ast.unparse(kwarg(sub, "rate_func"))[:30]] += 1
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Call):
                    nm = call_name(sub)
                    if nm in ANIM_CLASSES or nm in GROUP_CLASSES:
                        self.nested_classes[nm] += 1
                        srt = kwarg(sub, "run_time")
                        if srt is not None:
                            any_rt = True
                            v = literal_number(srt)
                            if v is not None:
                                self.nested_rt_explicit.append(v)
                                self.any_rt_by_class[nm].append(v)
                    if kwarg(sub, "lag_ratio") is not None:
                        has_lag = True
                    if animate_chain(sub) is not None and sub is not arg:
                        pass
        if rt is not None:
            v = literal_number(rt)
            if v is not None:
                # attribute the play-level run_time to every top-level class
                for arg in node.args:
                    if isinstance(arg, ast.Starred):
                        continue
                    nm = ".animate" if animate_chain(arg) is not None else call_name(arg)
                    if nm:
                        self.any_rt_by_class[nm].append(v)
        top_names = [call_name(a) for a in node.args if not isinstance(a, ast.Starred)]
        if any(n in PI_CREATURE_CALLS for n in top_names):
            self.pi_plays += 1
        else:
            if rt is not None and literal_number(rt) is not None:
                self.effective_play.append(literal_number(rt))
            elif rt is None and not starred and node.args:
                ds = [self._anim_duration(a) for a in node.args]
                if all(d is not None for d in ds):
                    self.effective_play.append(max(ds))
                else:
                    self.effective_play_unresolved += 1
            else:
                self.effective_play_unresolved += 1
        if any(isinstance(sub, ast.Attribute) and sub.attr == "animate" and (
                (isinstance(sub.value, ast.Name) and sub.value.id == "frame")
                or (isinstance(sub.value, ast.Attribute) and sub.value.attr == "frame"))
               for a in node.args for sub in ast.walk(a)):
            d = self._play_duration(node)
            if d is None:
                self.camera_play_unresolved += 1
            else:
                self.camera_play_durations.append(d)
        if any_rt:
            self.plays_with_any_rt += 1
        if has_lag:
            self.lag_in_play += 1
        if starred:
            self.starred_plays += 1
        else:
            self.args_per_play.append(n_args)

    def _add_wait(self, node: ast.Call):
        if self._in_loop(node):
            self.waits_in_loops += 1
        if kwarg(node, "note") is not None:
            self.waits_with_note += 1
        arg = node.args[0] if node.args else kwarg(node, "duration")
        if arg is None:
            self.waits_bare += 1
        else:
            v = literal_number(arg)
            if v is None:
                self.waits_nonliteral += 1
            else:
                self.waits_literal.append(v)

    def _play_duration(self, node: ast.Call) -> float | None:
        rt = kwarg(node, "run_time")
        if rt is not None:
            return literal_number(rt)
        if not node.args or any(isinstance(a, ast.Starred) for a in node.args):
            return None
        ds = [self._anim_duration(a) for a in node.args]
        return max(ds) if all(d is not None for d in ds) else None

    @staticmethod
    def _wait_duration(node: ast.Call) -> float | None:
        arg = node.args[0] if node.args else kwarg(node, "duration")
        return DEFAULT_WAIT if arg is None else literal_number(arg)

    def _rhythm(self, stmts):
        """Run lengths of consecutive self.play statements, broken by self.wait,
        and 'beats': a run of plays plus the wait(s) after it."""
        def kind(stmt):
            if isinstance(stmt, ast.Expr):
                if is_self_method(stmt.value, "play"):
                    return "play"
                if is_self_method(stmt.value, "wait"):
                    return "wait"
            return "other"

        kinds = [kind(s) for s in stmts]
        run = 0
        beat_play = beat_wait = 0.0
        beat_ok = True
        in_wait_phase = False

        def close_beat():
            nonlocal beat_play, beat_wait, beat_ok
            if beat_ok and beat_play > 0 and beat_wait > 0:
                self.beats.append(beat_play + beat_wait)
                self.beat_hold_share.append(beat_wait / (beat_play + beat_wait))
            beat_play = beat_wait = 0.0
            beat_ok = True

        for i, k in enumerate(kinds):
            node = stmts[i].value if k != "other" else None
            if k == "play":
                if in_wait_phase:
                    close_beat()
                    in_wait_phase = False
                run += 1
                d = self._play_duration(node)
                if d is None:
                    beat_ok = False
                else:
                    beat_play += d
                # next play/wait statement in the same block (skipping other statements)
                nxt = next((kk for kk in kinds[i + 1:] if kk != "other"), None)
                if nxt is not None:
                    self.play_checked_for_wait += 1
                    if nxt == "wait":
                        self.play_followed_by_wait += 1
            elif k == "wait":
                if run:
                    self.run_lengths.append(run)
                run = 0
                d = self._wait_duration(node)
                if d is None:
                    beat_ok = False
                else:
                    beat_wait += d
                in_wait_phase = True
        if in_wait_phase:
            close_beat()
        # a trailing run of plays without a wait is not a beat (block may continue elsewhere)

    def _add_scene(self, cls: ast.ClassDef, rel: str):
        methods = {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}
        if "construct" not in methods:
            return
        plays = waits = 0
        looped = False
        total = 0.0
        wait_total = 0.0
        resolvable = True
        for m in methods.values():
            for node in ast.walk(m):
                if is_self_method(node, "play"):
                    plays += 1
                    if self._in_loop(node):
                        looped = True
                    rt = kwarg(node, "run_time")
                    if rt is not None:
                        d = literal_number(rt)
                    else:
                        ds = [self._anim_duration(a) for a in node.args]
                        d = max(ds) if ds and all(x is not None for x in ds) else None
                    if d is None:
                        resolvable = False
                    else:
                        total += d
                elif is_self_method(node, "wait"):
                    waits += 1
                    if self._in_loop(node):
                        looped = True
                    arg = node.args[0] if node.args else kwarg(node, "duration")
                    d = DEFAULT_WAIT if arg is None else literal_number(arg)
                    if d is None:
                        resolvable = False
                    else:
                        total += d
                        wait_total += d
        # first / last scene-level call in construct (top level of the method body)
        calls = []
        for stmt in methods["construct"].body:
            for node in ast.walk(stmt):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                        and isinstance(node.func.value, ast.Name) and node.func.value.id == "self" \
                        and node.func.attr in ("play", "wait", "add", "remove", "clear", "embed"):
                    calls.append((node.lineno, node.func.attr))
        if calls:
            calls.sort()
            self.scene_first_call[calls[0][1]] += 1
            self.scene_last_call[calls[-1][1]] += 1
        self.scene_plays.append(plays)
        self.scene_waits.append(waits)
        rec = dict(scene=cls.name, file=rel, line=cls.lineno, plays=plays, waits=waits,
                   looped=looped, resolvable=resolvable,
                   est_seconds=round(total, 2) if resolvable and not looped else None)
        self.scene_records.append(rec)
        if resolvable and not looped and plays >= 3:
            self.straight_durations.append(total)
            if total > 0:
                self.straight_wait_share.append(wait_total / total)

    # ------------------------------------------------------------------ report
    def report(self, title: str) -> str:
        out = []
        p = out.append
        p(f"===== {title} =====")
        p(f"files parsed: {self.files - len(self.parse_errors)} / {self.files}"
          + (f"  (syntax errors: {len(self.parse_errors)})" if self.parse_errors else ""))
        for e in self.parse_errors:
            p(f"   ! {e}")
        p(f"scenes (classes defining construct): {len(self.scene_plays)}")
        p("")
        p(f"self.play calls: {self.plays}   (inside a loop/comprehension: {self.plays_in_loops}, "
          f"{100 * self.plays_in_loops / max(self.plays, 1):.0f}%)")
        p(f"  plays with a play-level run_time kwarg: {len(self.play_rt_explicit) + self.play_rt_nonliteral} "
          f"({100 * (len(self.play_rt_explicit) + self.play_rt_nonliteral) / max(self.plays, 1):.0f}%), "
          f"literal: {len(self.play_rt_explicit)}, non-literal: {self.play_rt_nonliteral}")
        p(f"  plays with any run_time (play-level or on a nested animation): {self.plays_with_any_rt} "
          f"({100 * self.plays_with_any_rt / max(self.plays, 1):.0f}%)")
        p(f"  play-level literal run_time: {summary(self.play_rt_explicit)}")
        p(f"     most common values: {top_values(self.play_rt_explicit)}")
        p(f"  EFFECTIVE play duration (play-level run_time, else the animations' own run_time or "
          f"class default; Pi-creature plays excluded): {summary(self.effective_play)}")
        p(f"     most common values: {top_values(self.effective_play)}")
        p(f"     unresolved (variables, *starred, AnimationGroup/LaggedStart without run_time): "
          f"{self.effective_play_unresolved}; Pi-creature plays: {self.pi_plays} "
          f"({100 * self.pi_plays / max(self.plays, 1):.0f}%)")
        p(f"  nested-animation literal run_time: {summary(self.nested_rt_explicit)}")
        p(f"     most common values: {top_values(self.nested_rt_explicit)}")
        p("")
        nwait = self.waits_bare + len(self.waits_literal) + self.waits_nonliteral
        p(f"self.wait calls: {nwait}   (bare wait() = default {DEFAULT_WAIT:g}s: {self.waits_bare}, "
          f"{100 * self.waits_bare / max(nwait, 1):.0f}%; literal: {len(self.waits_literal)}; "
          f"non-literal: {self.waits_nonliteral}; in loops: {self.waits_in_loops}; with note=: {self.waits_with_note})")
        all_waits = [DEFAULT_WAIT] * self.waits_bare + self.waits_literal
        p(f"  all resolvable waits (bare counted as {DEFAULT_WAIT:g}): {summary(all_waits)}")
        p(f"  explicit literal waits only: {summary(self.waits_literal)}")
        p(f"     most common values: {top_values(self.waits_literal)}")
        p(f"  ratio waits / plays: {nwait / max(self.plays, 1):.2f}")
        p("")
        p("play -> wait rhythm (statement order within a block):")
        p(f"  a play whose next play/wait statement is a wait: {self.play_followed_by_wait} / "
          f"{self.play_checked_for_wait} ({100 * self.play_followed_by_wait / max(self.play_checked_for_wait, 1):.0f}%)")
        p(f"  consecutive plays before a wait: {summary([float(x) for x in self.run_lengths])}")
        p(f"     distribution: {top_values([float(x) for x in self.run_lengths], 8)}")
        p(f"  BEAT = consecutive plays + the wait(s) after them (resolvable only), seconds: "
          f"{summary(self.beats)}")
        p(f"     share of each beat that is holding still (wait): {summary(self.beat_hold_share)}")
        p("")
        p(f"lag_ratio: plays containing a lag_ratio anywhere: {self.lag_in_play} "
          f"({100 * self.lag_in_play / max(self.plays, 1):.0f}% of plays)")
        p(f"  every literal lag_ratio kwarg in the files: {summary(self.lag_values_all)}")
        p(f"     most common values: {top_values(self.lag_values_all, 14)}")
        p(f"  non-literal lag_ratio kwargs: {self.lag_nonliteral}; LaggedStart/Map with default "
          f"lag_ratio (0.05): {self.lagged_start_default}")
        for cname in ("LaggedStart", "LaggedStartMap", "FadeIn", "FadeOut", "Write",
                      "ShowCreation", "TransformMatchingTex", "TransformMatchingStrings",
                      "AnimationGroup"):
            vals = self.lag_values_by_class.get(cname)
            if vals:
                s = sorted(vals)
                p(f"     {cname:<26} n={len(s):<4} median={percentile(s, 50):g}  "
                  f"p25={percentile(s, 25):g}  p75={percentile(s, 75):g}")
        p("")
        p(f"animations per play (top-level args, non-starred plays): {summary([float(x) for x in self.args_per_play])}")
        p(f"     distribution: {top_values([float(x) for x in self.args_per_play], 6)}; "
          f"starred plays (*anims): {self.starred_plays}")
        p("")
        tot = sum(self.top_classes.values()) or 1
        p("top-level play arguments (what is passed to self.play):")
        for name, n in self.top_classes.most_common(40):
            rts = sorted(self.any_rt_by_class.get(name, []))
            rt_note = (f"  [explicit run_time n={len(rts)}, median {percentile(rts, 50):g}]"
                       if rts else "")
            pi = "  (Pi creature)" if name in PI_CREATURE_CALLS else ""
            p(f"  {name:<30} {n:>5}  {100 * n / tot:5.1f}%{rt_note}{pi}")
        p("")
        p("all animation-class calls nested anywhere inside play args:")
        p("  " + ", ".join(f"{k}:{v}" for k, v in self.nested_classes.most_common(45)))
        p("")
        p(f"plays that move the camera (frame.animate / self.camera.frame.animate), seconds: "
          f"{summary(self.camera_play_durations)}  (unresolved: {self.camera_play_unresolved})")
        p(f"     most common values: {top_values(self.camera_play_durations, 8)}")
        p("")
        p("FadeIn/FadeOut shift use: " + ", ".join(f"{k}:{v}" for k, v in sorted(self.fade_shift.items())))
        p("  most common shift values: " + ", ".join(f"{k}:{v}" for k, v in self.fade_shift_values.most_common(12)))
        p("")
        p(".animate methods: " + ", ".join(f"{k}:{v}" for k, v in self.animate_methods.most_common(25)))
        p("")
        p("rate_func values: " + ", ".join(f"{k}:{v}" for k, v in self.rate_funcs.most_common(15)))
        p("")
        nonzero = [float(x) for x in self.scene_plays if x > 0]
        p(f"plays per scene (all scenes): {summary([float(x) for x in self.scene_plays])}")
        p(f"plays per scene (scenes with >=1 play): {summary(nonzero)}")
        p(f"waits per scene: {summary([float(x) for x in self.scene_waits])}")
        p(f"scenes with 0 plays: {sum(1 for x in self.scene_plays if x == 0)}")
        p("first self.add/play/wait/remove/clear/embed call in construct(): "
          + ", ".join(f"{k}:{v}" for k, v in self.scene_first_call.most_common()))
        p("last such call in construct(): "
          + ", ".join(f"{k}:{v}" for k, v in self.scene_last_call.most_common()))
        p("")
        p(f"estimated duration of straight-line scenes (>=3 plays, no play/wait in loops, all "
          f"durations resolvable; seconds): {summary(self.straight_durations)}")
        p(f"  share of that time spent in wait(): {summary(self.straight_wait_share)}")
        p("")
        p("idiom line counts (non-comment source lines matching; files in brackets):")
        for k in IDIOMS:
            p(f"  {k:<36} {self.idiom_lines[k]:>5}  [{self.idiom_files[k]}]")
        p("")
        p("file-level feature use (number of files):")
        for k, v in sorted(self.misc.items()):
            p(f"  {k:<40} {v}")
        return "\n".join(out)


def iter_py(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def maybe_reexec_newer_python():
    """entropy.py needs PEP 701 f-strings (Python >= 3.12). If we are older and a newer
    interpreter is on PATH, re-run this script under it so every file parses."""
    if sys.version_info >= (3, 12) or os.environ.get("PACING_STATS_NO_REEXEC"):
        return
    import shutil
    for name in ("python3.14", "python3.13", "python3.12"):
        exe = shutil.which(name)
        if exe:
            os.environ["PACING_STATS_NO_REEXEC"] = "1"
            print(f"(re-running under {name} so PEP 701 f-strings parse)", file=sys.stderr)
            os.execv(exe, [exe, "-I", os.path.abspath(__file__), *sys.argv[1:]])


def main():
    maybe_reexec_newer_python()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--videos", default=VIDEOS, help="path to the 3b1b videos repo")
    ap.add_argument("--years", nargs="*", default=["2023", "2024", "2025", "2026"])
    ap.add_argument("--by-year", action="store_true", help="also print one report per year")
    ap.add_argument("--by-project", action="store_true", help="also print one report per project dir")
    ap.add_argument("--projects", nargs="*", help="only these project dirs, e.g. _2024/transformers")
    ap.add_argument("--exclude", nargs="*", default=[],
                    help="skip files whose repo-relative path contains any of these substrings")
    ap.add_argument("--json", help="write raw numbers to this JSON file")
    ap.add_argument("--examples", nargs="*", help="print file:line for these classes/.methods")
    ap.add_argument("--scenes", action="store_true", help="list every scene with its counts")
    args = ap.parse_args()

    total = Stats()
    per_year: dict[str, Stats] = {}
    per_project: dict[str, Stats] = {}
    for year in args.years:
        ydir = os.path.join(args.videos, f"_{year}")
        if not os.path.isdir(ydir):
            print(f"(missing {ydir})", file=sys.stderr)
            continue
        for path in iter_py(ydir):
            rel = os.path.relpath(path, args.videos)
            parts = rel.split(os.sep)
            project = os.path.join(parts[0], parts[1]) if len(parts) > 2 else parts[0]
            if args.projects and project not in args.projects:
                continue
            if any(x in rel for x in args.exclude):
                continue
            total.add_file(path, rel)
            if args.by_year:
                per_year.setdefault(year, Stats()).add_file(path, rel)
            if args.by_project:
                per_project.setdefault(project, Stats()).add_file(path, rel)

    label = ", ".join(args.years) + (f" [{', '.join(args.projects)}]" if args.projects else "")
    if args.exclude:
        label += f" excluding {', '.join(args.exclude)}"
    print(total.report(f"ALL ({label})"))
    for y, s in per_year.items():
        print()
        print(s.report(f"YEAR {y}"))
    if per_project:
        print()
        print("===== per project: plays | median play-level run_time | bare-wait share | "
              "median literal wait | lag_in_play% | median plays/scene =====")
        for proj, s in sorted(per_project.items()):
            nwait = s.waits_bare + len(s.waits_literal) + s.waits_nonliteral
            rts = sorted(s.play_rt_explicit)
            wl = sorted(s.waits_literal)
            sp = sorted(float(x) for x in s.scene_plays if x > 0)
            print(f"  {proj:<38} plays={s.plays:<5} rt_med={percentile(rts, 50) if rts else float('nan'):<5.2f} "
                  f"bare={100 * s.waits_bare / max(nwait, 1):>3.0f}%  wait_med={percentile(wl, 50) if wl else float('nan'):<5.2f} "
                  f"lag={100 * s.lag_in_play / max(s.plays, 1):>3.0f}%  plays/scene={percentile(sp, 50) if sp else float('nan'):g}")
    if args.examples:
        print()
        for name in args.examples:
            locs = total.examples.get(name, [])
            print(f"{name}: {len(locs)} uses")
            for loc in locs[:40]:
                print(f"   {loc}")
    if args.scenes:
        print()
        for r in total.scene_records:
            print(f"  {r['file']}:{r['line']}  {r['scene']}  plays={r['plays']} waits={r['waits']} "
                  f"est={r['est_seconds']}")
    if args.json:
        data = dict(
            plays=total.plays, play_rt_explicit=total.play_rt_explicit,
            nested_rt_explicit=total.nested_rt_explicit, waits_bare=total.waits_bare,
            waits_literal=total.waits_literal, waits_nonliteral=total.waits_nonliteral,
            lag_values=total.lag_values_all, top_classes=dict(total.top_classes),
            nested_classes=dict(total.nested_classes), scenes=total.scene_records,
            run_lengths=total.run_lengths,
        )
        with open(args.json, "w") as f:
            json.dump(data, f, indent=1)


if __name__ == "__main__":
    main()
