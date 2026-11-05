#!/usr/bin/env python3
"""Count which manimlib (ManimGL) names Grant Sanderson's video code actually uses.

Stdlib only. It never imports or executes the code it reads: both trees are parsed
with ``ast``.

1. Index ``manimgl/manimlib``: every public top-level class, function and constant,
   every public method/property of every class (``set_backstroke``, ``fix_in_frame``,
   ``f_always``, ``reorient`` ...), and each class's kind (Animation, Mobject, Scene)
   resolved through its base classes.
2. Walk the video files for the chosen years (default 2022-2026) and count:
   - ``names``:   references to manimlib classes/functions/constants (calls and bare
                  references such as ``LaggedStartMap(FadeIn, ...)``);
   - ``methods``: ``x.method(...)`` / ``x.attr`` where the attribute is a manimlib method
                  name (receivers that are imported modules, e.g. ``np.``, are skipped;
                  names that are also builtin/numpy method names are tagged ``ambiguous``);
   - ``scene``:   ``self.X`` inside a Scene subclass (scene-ness resolved through the
                  corpus' own class hierarchy, so ``class Foo(MyBaseScene)`` counts);
   - ``frame``:   ``self.frame.X`` / ``self.camera.frame.X`` / ``frame.X``;
   - ``animate``, ``always``, ``f_always``: the method called after ``.animate`` etc.;
   - ``kwargs``:  keyword-argument names per called class/function/method;
   - ``string_selection``: ``mob["..."]`` subscripts on names bound to Tex/Text calls
                  (GL's substring selection), an approximation.
   A name that the video code itself defines is not counted in the file that defines
   it, and is flagged with the files that shadow it.

Usage:
    python3 tools/api_frequency.py                       # markdown report to stdout
    python3 tools/api_frequency.py --top 40 --years 2024-2026
    python3 tools/api_frequency.py --json counts.json    # full data
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # reference/3b1b
DEFAULT_MANIMLIB = ROOT / "manimgl" / "manimlib"
DEFAULT_VIDEOS = ROOT / "videos"

# Method names that also exist on builtin types or numpy arrays. A hit on one of these
# might not be a manimlib call, so it is tagged rather than dropped.
_BUILTIN_TYPES = (str, list, dict, set, tuple, int, float, complex, bytes, frozenset)
NUMPY_METHODS = {
    "all", "any", "argmax", "argmin", "astype", "clip", "conj", "copy", "cumsum", "dot",
    "fill", "flatten", "item", "max", "mean", "min", "prod", "ravel", "real", "imag",
    "reshape", "round", "sort", "std", "sum", "swapaxes", "T", "tolist", "transpose",
    "shape", "size", "view", "norm",
}
AMBIGUOUS = {n for t in _BUILTIN_TYPES for n in dir(t) if not n.startswith("_")} | NUMPY_METHODS

TEXT_CLASSES = {"Tex", "TexText", "Text", "OldTex", "OldTexText", "MarkupText",
                "TexMobject", "TextMobject", "StringMobject", "MTex", "MTexText"}


# ── manimlib index ───────────────────────────────────────────────────────────


class ManimlibIndex:
    def __init__(self, root: Path):
        self.root = root
        self.classes: dict[str, dict] = {}        # name -> {module, bases, methods}
        self.functions: dict[str, str] = {}       # name -> module
        self.constants: dict[str, str] = {}       # name -> module
        self.methods: dict[str, set[str]] = defaultdict(set)  # method -> classes
        for path in sorted(root.rglob("*.py")):
            self._index_file(path)
        self._kind_cache: dict[str, str] = {}

    def _module(self, path: Path) -> str:
        rel = path.relative_to(self.root.parent).with_suffix("")
        return ".".join(rel.parts)

    def _index_file(self, path: Path) -> None:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            print(f"warning: cannot parse {path}: {exc}", file=sys.stderr)
            return
        module = self._module(path)
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                methods, attrs = set(), set()
                for sub in ast.walk(node):  # ``self.frame = ...`` style instance attributes
                    if isinstance(sub, (ast.Assign, ast.AnnAssign)):
                        tgts = sub.targets if isinstance(sub, ast.Assign) else [sub.target]
                        for t in tgts:
                            if isinstance(t, ast.Attribute) and _dotted(t.value) == "self" \
                                    and not t.attr.startswith("_"):
                                attrs.add(t.attr)
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not item.name.startswith("_"):
                            methods.add(item.name)
                    elif isinstance(item, ast.Assign):  # e.g. ``pfp = point_from_proportion``
                        for t in item.targets:
                            if isinstance(t, ast.Name) and not t.id.startswith("_"):
                                if isinstance(item.value, (ast.Name, ast.Attribute)):
                                    methods.add(t.id)
                self.classes[node.name] = {
                    "module": module,
                    "bases": [_dotted(b).split(".")[-1] for b in node.bases if _dotted(b)],
                    "methods": methods,
                    "attrs": attrs,
                }
                for m in methods:
                    self.methods[m].add(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    self.functions[node.name] = module
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for t in targets:
                    for name in _target_names(t):
                        if name.startswith("_"):
                            continue
                        # ``ShowCreation = Create``-style aliases of a class count as the class
                        val = node.value
                        if isinstance(val, ast.Name) and val.id in self.classes:
                            self.classes[name] = dict(self.classes[val.id], alias_of=val.id)
                        else:
                            self.constants[name] = module

    def kind(self, cls: str, extra_bases: dict[str, list[str]] | None = None) -> str:
        """'animation' | 'mobject' | 'scene' | 'other' by walking base classes."""
        key = cls
        if extra_bases is None and key in self._kind_cache:
            return self._kind_cache[key]
        seen, stack, result = set(), [cls], "other"
        while stack:
            c = stack.pop()
            if c in seen:
                continue
            seen.add(c)
            if c == "Animation":
                result = "animation"; break
            if c == "Mobject":
                result = "mobject"; break
            if c == "Scene":
                result = "scene"; break
            bases = self.classes.get(c, {}).get("bases")
            if bases is None and extra_bases:
                bases = extra_bases.get(c)
            stack.extend(bases or [])
        if extra_bases is None:
            self._kind_cache[key] = result
        return result

    @property
    def scene_members(self) -> set[str]:
        out = set()
        for name, c in self.classes.items():
            if self.kind(c.get("alias_of", name)) == "scene":
                out |= c["methods"] | c.get("attrs", set())
        return out

    @property
    def public_names(self) -> set[str]:
        return set(self.classes) | set(self.functions) | set(self.constants)


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        inner = _dotted(node.value)
        return f"{inner}.{node.attr}" if inner else ""
    if isinstance(node, ast.Subscript):  # Generic[T]
        return _dotted(node.value)
    return ""


def _target_names(t: ast.AST):
    if isinstance(t, ast.Name):
        yield t.id
    elif isinstance(t, (ast.Tuple, ast.List)):
        for e in t.elts:
            yield from _target_names(e)


# ── corpus scan ──────────────────────────────────────────────────────────────


def video_files(videos: Path, years: range) -> list[Path]:
    files = []
    for y in years:
        d = videos / f"_{y}"
        if d.is_dir():
            files.extend(sorted(d.rglob("*.py")))
    return files


class FileInfo:
    def __init__(self, path: Path, tree: ast.Module):
        self.path = path
        self.tree = tree
        self.module_aliases: set[str] = set()
        self.defined: set[str] = set()
        self.class_bases: dict[str, list[str]] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.module_aliases.add(a.asname or a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                # ``from scipy import special`` binds a module; heuristically treat
                # lowercase single names from non-manim packages as modules.
                if node.module and not node.module.startswith(("manim", "_20", "custom")):
                    for a in node.names:
                        nm = a.asname or a.name
                        if nm != "*" and nm.islower():
                            self.module_aliases.add(nm)
            elif isinstance(node, ast.ClassDef):
                self.defined.add(node.name)
                self.class_bases[node.name] = [
                    _dotted(b).split(".")[-1] for b in node.bases if _dotted(b)]
        for node in tree.body:  # only module-level functions shadow imported names
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.defined.add(node.name)


class Counts:
    def __init__(self):
        self.names = Counter()
        self.name_calls = Counter()
        self.methods = Counter()
        self.scene = Counter()
        self.frame = Counter()
        self.animate = Counter()
        self.always = Counter()
        self.f_always = Counter()
        self.string_selection = Counter()
        self.kwargs: dict[str, Counter] = defaultdict(Counter)
        self.files: dict[str, set] = defaultdict(set)  # "section:name" -> files

    def hit(self, section: str, name: str, path: Path, n: int = 1):
        getattr(self, section)[name] += n
        self.files[f"{section}:{name}"].add(str(path))


def _is_self_frame(node: ast.AST) -> bool:
    """self.frame | self.camera.frame | frame"""
    d = _dotted(node)
    return d in ("self.frame", "self.camera.frame", "frame", "self.camera_frame")


class Scanner(ast.NodeVisitor):
    def __init__(self, idx: ManimlibIndex, info: FileInfo, counts: Counts,
                 all_bases: dict[str, list[str]]):
        self.idx, self.info, self.c, self.all_bases = idx, info, counts, all_bases
        self.class_stack: list[str] = []
        self.text_vars: set[str] = set()
        self.public = idx.public_names
        self.scene_members = idx.scene_members
        self._collect_text_vars()

    def _collect_text_vars(self):
        for node in ast.walk(self.info.tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                fn = _dotted(node.value.func).split(".")[-1]
                if fn in TEXT_CLASSES:
                    for t in node.targets:
                        d = _dotted(t)
                        if d:
                            self.text_vars.add(d)

    def in_scene(self) -> bool:
        return bool(self.class_stack) and \
            self.idx.kind(self.class_stack[-1], self.all_bases) == "scene"

    def visit_ClassDef(self, node: ast.ClassDef):
        for b in node.bases:  # base-class references count as uses
            self.visit(b)
        self.class_stack.append(node.name)
        for item in node.body:
            self.visit(item)
        self.class_stack.pop()

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load) and node.id in self.public \
                and node.id not in self.info.defined:
            self.c.hit("names", node.id, self.info.path)

    def visit_Call(self, node: ast.Call):
        f = node.func
        key = None
        if isinstance(f, ast.Name) and f.id in self.public and f.id not in self.info.defined:
            key = f.id
            self.c.name_calls[f.id] += 1
        elif isinstance(f, ast.Attribute):
            if _dotted(f.value) == "self" and self.in_scene():
                key = f"self.{f.attr}"
            elif isinstance(f.value, ast.Attribute) and f.value.attr == "animate" \
                    and _is_self_frame(f.value.value):
                key = f"frame.animate.{f.attr}"
            elif _is_self_frame(f.value):
                key = f"frame.{f.attr}"
            elif f.attr in self.idx.methods:
                key = f".{f.attr}"
        if key:
            for kw in node.keywords:
                self.c.kwargs[key]["**" if kw.arg is None else kw.arg] += 1
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        attr, val = node.attr, node.value
        root = val
        while isinstance(root, ast.Attribute):
            root = root.value
        if isinstance(root, ast.Name) and root.id in self.info.module_aliases \
                and root.id != "self":
            self.generic_visit(node)
            return
        if isinstance(val, ast.Attribute) and val.attr in ("animate", "always", "f_always"):
            self.c.hit(val.attr, attr, self.info.path)
            if val.attr == "animate" and _is_self_frame(val.value):
                self.c.hit("frame", f"animate.{attr}", self.info.path)
        if _is_self_frame(val):
            self.c.hit("frame", attr, self.info.path)
        elif _dotted(val) == "self" and self.in_scene():
            if attr in self.scene_members:  # skip the video's own scene attributes
                self.c.hit("scene", attr, self.info.path)
        elif attr in self.idx.methods:
            self.c.hit("methods", attr, self.info.path)
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        sl = node.slice
        if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
            d = _dotted(node.value)
            is_text_call = isinstance(node.value, ast.Call) and \
                _dotted(node.value.func).split(".")[-1] in TEXT_CLASSES
            if d in self.text_vars or is_text_call:
                self.c.hit("string_selection", "mob['...'] on Tex/Text", self.info.path)
        self.generic_visit(node)


def corpus_class_bases(videos: Path) -> dict[str, list[str]]:
    """Class -> base names for the whole videos tree (all years + custom/), so that a
    scene subclassing e.g. custom's TeacherStudentsScene is still recognised as a Scene."""
    bases: dict[str, list[str]] = {}
    for p in sorted(videos.rglob("*.py")):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError, ValueError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases.setdefault(node.name, [
                    _dotted(b).split(".")[-1] for b in node.bases if _dotted(b)])
    return bases


def scan(idx: ManimlibIndex, files: list[Path], videos: Path):
    infos, failures = [], []
    for p in files:
        try:
            infos.append(FileInfo(p, ast.parse(p.read_text(encoding="utf-8"), filename=str(p))))
        except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
            failures.append(f"{p}: {exc.__class__.__name__}")
    all_bases = corpus_class_bases(videos)
    shadowed: dict[str, set[str]] = defaultdict(set)
    for info in infos:
        all_bases.update(info.class_bases)  # a file's own definition wins
        for name in info.defined & idx.public_names:
            shadowed[name].add(str(info.path))
    counts = Counts()
    for info in infos:
        Scanner(idx, info, counts, all_bases).visit(info.tree)
    return counts, shadowed, failures, len(infos)


# ── reporting ────────────────────────────────────────────────────────────────


def describe(idx: ManimlibIndex, name: str) -> tuple[str, str]:
    if name in idx.classes:
        c = idx.classes[name]
        kind = idx.kind(c.get("alias_of", name))
        return kind if kind != "other" else "class", c["module"]
    if name in idx.functions:
        return "function", idx.functions[name]
    if name in idx.constants:
        return "constant", idx.constants[name]
    return "?", ""


def top_kwargs(counter: Counter, n=5) -> str:
    return ", ".join(f"{k}={v}" for k, v in counter.most_common(n))


def short_owner(idx: ManimlibIndex, method: str) -> str:
    owners = sorted(idx.methods.get(method, ()))
    pref = [o for o in ("Mobject", "VMobject", "Scene", "InteractiveScene", "CameraFrame")
            if o in owners]
    shown = pref or owners[:3]
    more = len(owners) - len(shown)
    return ", ".join(shown) + (f" +{more}" if more > 0 else "")


def build_report(idx, counts, shadowed, failures, n_files, args) -> str:
    out = []
    w = out.append
    w(f"# manimlib usage in 3b1b/videos {args.years} ({n_files} files parsed"
      f"{', %d failed' % len(failures) if failures else ''})\n")
    w(f"manimlib index: {len(idx.classes)} classes, {len(idx.functions)} functions, "
      f"{len(idx.constants)} constants, {len(idx.methods)} method names\n")

    # names grouped by kind
    groups = defaultdict(list)
    for name, n in counts.names.most_common():
        kind, module = describe(idx, name)
        groups[kind].append((name, n, module))
    order = ["animation", "mobject", "scene", "class", "function", "constant"]
    for kind in order:
        rows = groups.get(kind, [])[: args.top]
        if not rows:
            continue
        w(f"\n## {kind} names\n")
        w("| rank | name | uses | calls | files | module | top kwargs | shadowed |")
        w("|---|---|---|---|---|---|---|---|")
        for i, (name, n, module) in enumerate(rows, 1):
            nf = len(counts.files[f"names:{name}"])
            sh = len(shadowed.get(name, ()))
            w(f"| {i} | {name} | {n} | {counts.name_calls[name]} | {nf} | {module} | "
              f"{top_kwargs(counts.kwargs.get(name, Counter()))} | {sh or ''} |")

    def section(title, counter, sect, kwprefix=None, owners=True, ambiguous=False):
        rows = counter.most_common(args.top)
        if not rows:
            return
        w(f"\n## {title}\n")
        w("| rank | name | uses | files | defined on | top kwargs |" +
          (" ambiguous |" if ambiguous else ""))
        w("|---|---|---|---|---|---|" + ("---|" if ambiguous else ""))
        for i, (name, n) in enumerate(rows, 1):
            nf = len(counts.files[f"{sect}:{name}"])
            kw = counts.kwargs.get(f"{kwprefix}{name}", Counter()) if kwprefix else Counter()
            own = short_owner(idx, name) if owners else ""
            amb = (" yes |" if name in AMBIGUOUS else " |") if ambiguous else ""
            w(f"| {i} | {name} | {n} | {nf} | {own} | {top_kwargs(kw)} |{amb}")

    section("mobject/other methods (x.method)", counts.methods, "methods", ".", ambiguous=True)
    section("scene calls (self.X in a Scene subclass)", counts.scene, "scene", "self.")
    section("frame calls (self.frame.X / frame.X)", counts.frame, "frame", "frame.")
    section("methods used via .animate", counts.animate, "animate")
    section("methods used via .always (updater builder)", counts.always, "always")
    section("methods used via .f_always", counts.f_always, "f_always")
    if counts.string_selection:
        w("\n## string selection (approximate)\n")
        for k, v in counts.string_selection.items():
            w(f"- {k}: {v} uses in {len(counts.files['string_selection:' + k])} files")
    if failures:
        w("\n## files that failed to parse\n")
        for f in failures:
            w(f"- {f}")
    return "\n".join(out) + "\n"


def parse_years(s: str) -> range:
    if "-" in s:
        a, b = s.split("-")
        return range(int(a), int(b) + 1)
    return range(int(s), int(s) + 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manimlib", type=Path, default=DEFAULT_MANIMLIB)
    ap.add_argument("--videos", type=Path, default=DEFAULT_VIDEOS)
    ap.add_argument("--years", default="2022-2026")
    ap.add_argument("--top", type=int, default=50, help="rows per section")
    ap.add_argument("--json", type=Path, help="also dump all counts as JSON here")
    args = ap.parse_args(argv)

    idx = ManimlibIndex(args.manimlib)
    files = video_files(args.videos, parse_years(args.years))
    counts, shadowed, failures, n = scan(idx, files, args.videos)
    sys.stdout.write(build_report(idx, counts, shadowed, failures, n, args))

    if args.json:
        data = {
            "years": args.years, "files_parsed": n, "parse_failures": failures,
            "names": {k: {"uses": v, "calls": counts.name_calls[k],
                          "files": len(counts.files[f"names:{k}"]),
                          "kind": describe(idx, k)[0], "module": describe(idx, k)[1],
                          "shadowed_in": sorted(shadowed.get(k, ()))}
                      for k, v in counts.names.most_common()},
        }
        for sect in ("methods", "scene", "frame", "animate", "always", "f_always",
                     "string_selection"):
            data[sect] = {k: {"uses": v, "files": len(counts.files[f"{sect}:{k}"])}
                          for k, v in getattr(counts, sect).most_common()}
        for k in data["methods"]:
            data["methods"][k]["defined_on"] = sorted(idx.methods.get(k, ()))
            data["methods"][k]["ambiguous"] = k in AMBIGUOUS
        data["kwargs"] = {k: dict(v.most_common()) for k, v in counts.kwargs.items()}
        args.json.write_text(json.dumps(data, indent=1))
        print(f"wrote {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()
