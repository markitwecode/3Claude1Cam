# ManimGL → Manim CE 0.22: verified translation guide

How to port an idea from Grant's video code (`videos/`, ManimGL / `manimlib`) into our
**Manim CE 0.22.0** scenes without inventing APIs. Ground truth is the installed CE source,
`.venv/lib/python3.11/site-packages/manim/`. Every row below was checked against it.

**Which names are here.** `tools/api_frequency.py` parsed his 2022–2026 videos (131 files;
2 skipped because they don't parse: one is a fragment, one uses Python 3.12 f-string syntax)
and counted references to names defined in `manimgl/manimlib`. The numbers in brackets are
use counts. Re-run with `python3 reference/3b1b/tools/api_frequency.py --top 60`.

**"Verified" column**

| tag | meaning |
|---|---|
| `src: path` | definition read in the installed CE source at `manim/path`; signature checked with `inspect` |
| `P##` | behaviour probe in `tools/gl_to_ce_probes.py` (46/46 pass: `.venv/bin/python reference/3b1b/tools/gl_to_ce_probes.py`) |
| `V##` | tiny scene in `tools/gl_to_ce_snippets.py`, rendered with `-ql -s`; the last frame was checked by eye |
| `port` | `ce_ports.py`: self-test passes and `PortsDemo` rendered (video frames checked) |

GL source paths below are relative to `manimgl/manimlib/`, CE paths to `manim/`.

## Read this first: the traps that cost the most

1. **GL `Tex` is CE `MathTex`; GL `TexText` is CE `Tex`.** CE rejects `t2c=` and `isolate=`
   with a TypeError. Use `tex_to_color_map=` and `substrings_to_isolate=` (P11).
2. **No `mob["x"]`.** GL's string selection (~1140 uses) is a TypeError in CE (P15). Use
   `ce_ports.select(mob, "x")`, or `get_part_by_tex` (first occurrence only, P13).
3. **CE silently accepts many GL `get_*`/`set_*` calls.** `Mobject.__getattr__` turns an
   unknown `set_foo(v)` into an attribute write and `get_foo()` into an attribute read
   (`src: mobject/mobject.py`). So `mob.set_backstroke(BLACK)`, `mob.set_max_width(3)` and
   `mob.set_flat_stroke(False)` **do nothing and raise no error**, while the same calls with
   two arguments or any keyword raise a TypeError (P18, P19, P20).
4. **Positional arguments differ.** GL `Rectangle(4, 2)` means (width, height): CE crashes,
   because its first positional is `color`. GL `Arc(0, PI)` means (start_angle, angle): CE
   silently builds an arc of radius 0. Always pass keywords (P28; 92 + 71 such calls).
5. **`FadeIn(scale=)` is inverted.** GL `scale=2` grows into place from half size. In CE,
   `scale=2` *shrinks* into place from double size. GL `scale=s` is CE `scale=1/s` (P01).
6. **Updaters.** CE animations freeze the animated mobject's own updaters by default
   (`suspend_mobject_updating=True`; GL's default is False, P06). CE `add_updater` doesn't
   call the updater once straight away, as GL does: pass `call_updater=True` (P23).
7. **No `time_span=`** (555 uses). It's a TypeError in CE (P05). Use `ce_ports.time_span`.
8. **No `self.frame`.** Use `MovingCameraScene` and `self.camera.frame` for 2D moves, and
   `ThreeDScene` camera methods for 3D (see Camera, below).
9. **CE's `arrange_in_grid` silently ignores GL keywords** (`n_rows`, `n_cols`, `h_buff`,
   `v_buff`, `fill_rows_first`). Use `rows, cols, buff=(h, v), flow_order` (P26).
10. **Strokes are one width per mobject in Cairo.** GL tapered strokes (`Underline`, `Cross`,
    `VShowPassingFlash`, `set_stroke(width=[0, 3, 0])`) come out flat or need a port.

## Translation table

Columns: GL name [uses] | CE 0.22 equivalent | differences / gotchas | verified.

### Scene, play, timing

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `InteractiveScene` [1328], `Scene` [52] | `Scene`; `MovingCameraScene` to move the frame; `ThreeDScene` for 3D | InteractiveScene's extras (selection, `embed`, mouse) are interactive-only. | `src: scene/scene.py`, `scene/moving_camera_scene.py`, `scene/three_d_scene.py` |
| `self.play(..., run_time=, rate_func=, lag_ratio=)` [10243] | same | Both set each kwarg on every animation passed in. In CE, `lag_ratio` there re-times `FadeIn(group)`/`Create(group)`, but **not** an `AnimationGroup`/`LaggedStart`, whose timings are fixed when it's built. Give those their `lag_ratio` in the constructor. | `src: scene/scene.py` (`compile_animations`), P07, V06 |
| `self.wait(t, note=)` [6742; note=52] | `self.wait(t)` | No `note=` (GL presenter-mode label). `stop_condition=` exists in both. | `src: scene/scene.py` |
| `self.add / remove / bring_to_front` [2987 / 564 / 46] | same | If you add or animate a piece of a mobject that's already on screen (e.g. a `select()`/`get_part_by_tex` group), CE splits the parent in `self.mobjects`. After that, `self.remove(parent)` **leaves the pieces on screen**: use `self.remove(*parent.get_family())`. `FadeOut(parent)` still clears everything. | `src: scene/scene.py` (`restructure_mobjects`), P46 |
| `time_span=(a, b)` kwarg [555, on any animation] | `ce_ports.time_span(anim, a, b)`, or `Succession(Wait(a), anim)` with `run_time=b-a` on `anim` | TypeError in CE. The port keeps GL semantics: absolute seconds inside the `play()`, holds the end state, works with `play(run_time=)`. | P05, port |
| `lag_ratio` placement [2297 kwarg uses] | same places | `LaggedStart(*anims, lag_ratio=)`: default 0.05 in both. `LaggedStartMap(AnimClass, group, lag_ratio=, **anim_kwargs)`: run_time 2 in both, and other kwargs (`shift=`...) go to each animation. `AnimationGroup(lag_ratio=0)`. `FadeIn(group, lag_ratio=)` lags over submobjects. | `src: animation/composition.py`, P09, V06 |
| `suspend_mobject_updating=` [144] | same kwarg | Default GL False, **CE True**: a mobject with an updater freezes while it is itself being animated. | `src: animation/animation.py`, P06 |

### Creation and fading

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `FadeIn` [3285; shift 204, scale 85, lag_ratio 438] | `FadeIn` | `shift=v` is the same (it starts at −v). **`scale` is inverted** (GL `s` = CE `1/s`). CE also takes several mobjects, and has `target_position=`. | P01, P02, V01 |
| `FadeOut` [2785] | `FadeOut` | `shift`/`scale` mean the same. Removes the mobject, then restores it to its pre-fade state, as GL does. | P03, V01 |
| `FadeInFromPoint` / `FadeOutToPoint` [69 / 23] | `FadeIn(m, target_position=p, scale=0)` / `FadeOut(m, target_position=p, scale=0)` | Not in CE. `scale=0` is safe (no NaNs). | P04, V01 |
| `VFadeIn` / `VFadeOut` / `VFadeInThenOut` [170 / 52 / 38] | `ce_ports.VFadeIn` / `VFadeOut` / `VFadeInThenOut` | Not in CE. They fade opacity only and keep updaters running (GL behaviour). Plain `FadeIn` is fine for static mobjects. | P37, port |
| `Write` [1506; run_time 158, lag_ratio 85, stroke_color 78] | `Write` | Works on `Text` and `MathTex`. CE defaults: run_time 1 below 15 glyph paths, else 2; lag_ratio `min(4/n, 0.2)`. Keep his explicit `run_time`. `stroke_color=`/`stroke_width=` are accepted. | `src: animation/creation.py`, P08, V02 |
| `ShowCreation` [1204] | `Create` | Renamed. lag_ratio 1.0 in both. | `src: animation/creation.py`, V02 |
| `ShowIncreasingSubsets` [87] | same | `int_func` default: GL `np.round`, CE `np.floor`. | `src: animation/creation.py`, P37 |
| `GrowArrow` / `GrowFromCenter` / `GrowFromPoint` / `GrowFromEdge` [354 / 229 / 35 / 37] | same | Same signatures (CE adds `point_color`). | `src: animation/growing.py`, V15 |
| `ShowCreationThenFadeOut` [26] | `Succession(Create(m), FadeOut(m))` | Not in CE. | `src: animation/composition.py`, P37 |

### Transforms

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `TransformFromCopy` [907], `MoveToTarget` + `generate_target` [500 / 473], `FadeTransform` [409], `ReplacementTransform` [373], `Transform` [335], `Restore` + `save_state` [265 / 422], `FadeTransformPieces` [71] | same names | Same arguments (`path_arc`, `path_arc_axis`, `path_func`, `remover`; `stretch`/`dim_to_match` on the Fade ones). `Restore` also works on `self.camera.frame`. | `src: animation/transform.py`, V05, V12 |
| `TransformMatchingTex` [186; key_map 34, matched_keys 24] | for GL behaviour: `ce_ports.TransformMatchingStrings`. CE's own: `TransformMatchingTex(a, b, key_map=)` | **Same name, different algorithm.** GL's is an alias of TransformMatchingStrings: it matches glyph runs automatically. CE's matches whole *parts* by exact `tex_string`: separate args or `{{...}}` groups. Unsplit strings match nothing, so everything just fades (P17). `substrings_to_isolate` does not create parts in 0.22 (P12). There is no `matched_keys` (TypeError). `key_map` keys are part strings, spaces included. Asserts on `Text`. | P12, P17, V04, port |
| `TransformMatchingStrings` [64] | `ce_ports.TransformMatchingStrings` | Not in CE. The port also takes `matched_keys=`/`key_map=` (resolved with `select`). GL default `run_time=2` kept. | P37, port |
| `TransformMatchingShapes` [139] | same name | CE puts **all** glyphs of one shape into a single group: repeated letters move as a unit and can fly across lines (see LESSONS.md). GL pairs pieces one-to-one. Works on `Text`. | `src: animation/transform_matching_parts.py`, V04 |
| `Rotate` [203; about_point 144, axis 64] | `Rotate(m, angle, axis=, about_point=)` | Default pivot is the centre in both. In CE it is a Transform with `path_arc`, and a full `TAU` turn still animates. | P10, V15 |
| `UpdateFromFunc` / `UpdateFromAlphaFunc` [102 / 76] | same | Both default to `suspend_mobject_updating=False` here. | `src: animation/updaters/update.py`, V11 |
| `ChangeDecimalToValue` [54] / `CountInFrom` [34] | `ChangeDecimalToValue` / `n.set_value(0)`, then `ChangeDecimalToValue(n, final)` | `CountInFrom` isn't in CE. | P37, V10 |

### Highlighting

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `FlashAround` [162; run_time 85, time_width 83] | `ce_ports.FlashAround(m, run_time=2, time_width=1.5)`; CE-native fallback `Circumscribe(m, time_width=0.5)` or `ShowPassingFlash(SurroundingRectangle(m), time_width=0.5)` | GL's flash is a tapered Gaussian bump of stroke width. CE's `ShowPassingFlash` shows a constant-width segment. `Circumscribe` defaults: time_width 0.3, buff 0.1. | V07, port |
| `VShowPassingFlash` [64] | `ce_ports.VShowPassingFlash(path.copy(), time_width=)` | Not in CE. CE `ShowPassingFlashWithThinningStrokeWidth` is a cruder stack of flashes. | P37, port |
| `FlashUnder` [26] | `ce_ports.FlashUnder` | Not in CE. | port |
| `Indicate` [21; scale_factor 13] | same | Same defaults (1.2, YELLOW). It floods opaque-filled boxes (LESSONS.md). | P43, V07 |
| `Flash` [11] | same | `flash_radius` default: GL 0.3, **CE 0.1**. | P43, V07 |

### Text and numbers

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `Tex` [2617; font_size 956, t2c 381, tex_to_color_map 88, isolate 28] | `MathTex` | Both use math mode (`align*`). `t2c=` → `tex_to_color_map=`, which colours **every** occurrence. `isolate=` → `substrings_to_isolate=`. Several string args become parts in both. `font_size` is the same. | `src: mobject/text/tex_mobject.py`, P11, V03 |
| `TexText` [381] | `Tex` | Text mode. Same kwarg caveats as above. | V03 |
| `OldTex` / `OldTexText` [278 / 112] | `MathTex` / `Tex` | GL legacy classes. | P37 |
| `Text` [1768; font_size 645, alignment 67, t2s 16, t2c 13] | `Text` | `t2c`, `t2f`, `t2s`, `t2w`, `font=` all exist. No `alignment=` (TypeError): use `Paragraph(*lines, alignment="left")` or `VGroup(...).arrange(DOWN, aligned_edge=LEFT)`. At equal `font_size`, CE `Text` is about 1.3× taller than `MathTex`. | P16, P39, V03 |
| `mob["x"]` substring selection [~1140, approximate count] | `ce_ports.select(mob, "x")` (all occurrences); CE `get_part_by_tex("x")` (first only) | TypeError in CE. In MathTex the key must be isolated (`substrings_to_isolate` / `tex_to_color_map`) or be a whole part. Glyph indexes in `Text` skip spaces unless `disable_ligatures=True`. | P13, P15, port |
| `set_color_by_tex` / `get_part_by_tex` [10 / 18] | same names | Exact match on a part's `tex_string` or on an isolated substring. `{{ b }}` keeps its spaces (part `" b "`), so `set_color_by_tex("b")` silently does nothing; write `{{b}}`. | P13, P14, V03 |
| `tex.make_number_changeable("0.00")` [128] | no equivalent: `VGroup(MathTex("p ="), DecimalNumber(...))` with an updater `m.set_value(...).next_to(label, RIGHT)` | GL swaps glyphs inside the Tex for a live number. In CE, build the label and the number separately. | V10 |
| `Integer` [212] / `DecimalNumber` [141; num_decimal_places 45, unit 17, include_sign 11] | same | `num_decimal_places`, `include_sign`, `unit`, `edge_to_fix`, `font_size` and `group_with_commas` (True in both: "1,000") all exist. No `min_total_width` (TypeError). GL `text_config` ≈ CE `mob_class`. `set_value` keeps the left edge fixed. | P31, V10 |
| `Brace` [254; buff 60] | `Brace(m, direction, buff=)` | No `tex_string=` (TypeError). | P30, V09 |
| `brace.get_tex(...)` / `brace.get_text(...)` [87 / 62; font_size 42] | same names, no style kwargs | CE passes kwargs to `put_at_tip`, so `font_size=` is a TypeError. CE `get_text` returns LaTeX `Tex` (GL: Pango `Text`). For a styled label, build it and call `brace.put_at_tip(label, buff=)`, or use `BraceLabel(m, "x", font_size=)`. | P30, V09 |

### Mobjects

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `VGroup` / `Group` [4924 / 665] | same | CE `VGroup` accepts generators and lists. Use `Group` to mix in `ImageMobject`. | P40 |
| `SurroundingRectangle` [704; buff 312] | same | Same defaults (buff 0.1, YELLOW). CE takes several mobjects and adds `corner_radius=`. | `src: mobject/geometry/shape_matchers.py`, V15 |
| `BackgroundRectangle` [45] | same | Same defaults (fill_opacity 0.75, buff 0, background colour). | V15 |
| `Arrow` [456; buff 195, thickness 124, path_arc 106] | `Arrow(start, end, buff=, stroke_width=, max_tip_length_to_length_ratio=)` | GL draws a filled shape whose size is set by `thickness`. CE draws a stroked line plus a tip. `thickness=` is a TypeError; use `stroke_width` (default 6). Buff 0.25 in both; `path_arc` works; tip styles are in `tips.py` (`StealthTip`...). | P27, V15 |
| `Vector` [325; thickness 111] | `Vector(direction)` | Same as Arrow; buff 0. | V15 |
| `DashedLine` [84; dash_length 24] | same | GL `positive_space_ratio` → CE `dashed_ratio`. | V15 |
| `Rectangle` [186; 92 positional] | `Rectangle(width=, height=)` | **Positional order differs** (CE: color, height, width); `Rectangle(4, 2)` raises. | P28, V15 |
| `Arc` [82; 71 positional] | `Arc(radius=, start_angle=, angle=, arc_center=)` | **Positional order differs**; `Arc(0, PI)` silently gives radius 0. | P28, V15 |
| `Circle` / `Dot` / `Square` [166 / 117 / 128] | same | CE `Circle`'s first positional is `radius` (GL: `start_angle`), so pass keywords. `Dot` radius is 0.08 in both. | `src: mobject/geometry/arc.py`, V15 |
| `Underline` [78; buff 35, stretch_factor 13] | `Underline(m, buff=)` | No `stretch_factor` (TypeError): use `.stretch(1.2, 0)`. GL's tapered stroke can't be drawn: CE's is flat. | P29, V15 |
| `Cross` [33] | `Cross(m, stroke_width=)` | Flat stroke (GL tapers). | V15 |
| `ValueTracker` [322] + `get_value` / `set_value` / `increment_value` [753 / 1218 / 75] | same | `tracker.animate.set_value(x)` works. | V11 |
| `ImageMobject` [192] | `ImageMobject(path).set(height=h)` | No `height=` kwarg (TypeError). The default size comes from `scale_to_resolution=1080`. | P34 |
| `SVGMobject` [94] | same | Default `height=2` in both. GL's `svg_string=` has no CE counterpart (CE adds `use_svg_cache`). | `src: mobject/svg/svg_mobject.py` |
| `FullScreenRectangle` / `ScreenRectangle` [106 / 48] | same | `ScreenRectangle(height=)`. | `src: mobject/frame.py` |
| `Point` / `VectorizedPoint` [70 / 51] | `VectorizedPoint` | CE `Point` is a point-cloud `PMobject`. Use `VectorizedPoint` as an invisible anchor. | P41 |
| `GlowDot` [219] / `TrueDot` [84] / `DotCloud` [54] | `ce_ports.GlowDot` / `Dot` / a `VGroup` of `Dot`s | CE's `TrueDot`/`DotCloud` exist only in `manim.mobject.opengl` (OpenGL renderer). | P38, port |
| `TracingTail` [32] / `TracedPath` [16] | `TracedPath(mob.get_center, dissipating_time=, stroke_color=, stroke_width=)` | GL `time_traced` ≈ CE `dissipating_time`. | `src: animation/changing.py`, V11 |
| `Axes` [145; width 106, height 109] | `Axes(x_range=, y_range=, x_length=, y_length=, tips=)` | `width`/`height` are TypeErrors. | P32, V14 |
| `axes.get_graph(f, x_range=)` [191] | `axes.plot(f, x_range=, color=)` | `get_graph` raises a TypeError (it hits the auto-getter). | P32, V14 |
| `axes.add_coordinate_labels()` [81] | `axes.add_coordinates()` | AttributeError in CE. | P32, V14 |
| `c2p` / `n2p` / `p2n` / `i2gp` [493 / 479 / 74 / 28] | same | `get_graph_label`, `get_area`, `get_riemann_rectangles` exist too. | V14 |
| `NumberLine` [59; width 38, tick_size 20, big_tick_spacing 14] | `NumberLine(x_range=, length=, tick_size=, numbers_with_elongated_ticks=, include_numbers=)` | `width=` and `big_tick_spacing=` are TypeErrors. `add_numbers(font_size=, num_decimal_places=)` works. | P33, V14 |
| `NumberPlane` / `ComplexPlane` [79 / 88] | same | Defaults differ: GL `faded_line_ratio=4`, CE 1. Pass `background_line_style` / `faded_line_ratio` explicitly. | `src: mobject/graphing/coordinate_systems.py`, V08 |
| `ThreeDAxes` [84] | `ThreeDAxes(x_range=, ..., x_length=, y_length=, z_length=)` | Lengths, not width/height. | V13 |
| `ParametricCurve` [37] | `ParametricFunction(f, t_range=)` | Renamed. | P37 |
| `ParametricSurface` / `Sphere` / `SurfaceMesh` [39 / 56 / 51] | `Surface(f, u_range=, v_range=, resolution=)` / `Sphere(radius=, resolution=)` / none | CE `Surface` already draws a checkerboard plus a stroke mesh. GL's GPU shading has no CE counterpart. | V13 |

### Mobject methods

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `.animate` [3947; run_time 81, path_arc 15] | same | `mob.animate(run_time=, path_arc=).method()` works. | P42 |
| `set_stroke` [3000; width 645, opacity 461, behind 60] | `set_stroke(color, width, opacity, background=)` | No `behind=` or `flat=` (TypeError). Lists of widths (tapers) aren't possible in Cairo. | P22 |
| `set_fill` [1378; opacity 411, border_width 97] | `set_fill(color, opacity)` | No `border_width=` (TypeError); drop it. | P22 |
| `set_color(c, opacity)` [1882; 70 with 2 positionals] | `set_color(c)` then `.set_opacity(o)` | CE's 2nd positional is `alpha` and does **not** set opacity. | P21 |
| `set_backstroke(color=BLACK, width=3)` [293] | `set_stroke(BLACK, w, background=True)` or `ce_ports.set_backstroke(mob, ...)` | Calling `mob.set_backstroke` in CE: no args → TypeError; 1 arg → **silent no-op**; 2 args → TypeError. In our renders, widths of 6–8 gave a clear halo. | P18, V08 |
| `set_height` / `set_width` [1109 / 529; stretch 115, about_edge 89] | `scale_to_fit_height(h, about_edge=)` / `stretch_to_fit_height(h)`, or `mob.set(height=h)` | A bare `set_height(h)` happens to work through the deprecated auto-setter, but any kwarg is a TypeError. Don't rely on it. | P19, V16 |
| `set_max_width` / `set_max_height` [77 / 21] | `if m.width > w: m.scale_to_fit_width(w)` | **Silent no-op** in CE (auto-setter). | P20, V16 |
| `get_width` / `get_height` / `get_points` [415 / 311 / 126] | `m.width` / `m.height` / `m.points` | The get_ forms only work through the deprecated auto-getter. | P19 |
| `arrange_in_grid` [67] | `arrange_in_grid(rows, cols, buff=(h, v), flow_order="rd")` | GL kwarg names (`n_rows`, `n_cols`, `h_buff`, `v_buff`, `fill_rows_first`) are **silently ignored**. `fill_rows_first=False` → `flow_order="dr"`. | P26, V16 |
| `get_grid` / `replicate` [135 / 259] | `ce_ports.get_grid` / `ce_ports.replicate`, or `VGroup(*(m.copy() for _ in range(n)))` | `get_grid` is a TypeError, `replicate` an AttributeError. | P25, port |
| `pfp` [191] | `point_from_proportion` | AttributeError in CE. | P25 |
| `add_updater` [1014] | `add_updater(f, call_updater=True)` | GL calls the updater immediately; CE doesn't unless `call_updater=True`. `(m)` and `(m, dt)` signatures work in both. | P23, V11 |
| `.always.method(...)` [109] | same (`mob.always.next_to(a, UP)`) | Exists in CE and runs once immediately. Each chained call becomes its own updater. | P24, P45, V11 |
| `.f_always.method(func)` [139] | `f_always(mob.method, func)` | No `.f_always` attribute in CE (AttributeError); use the function form. | P24, V11 |
| `always_redraw(func, *args)` [110] | `always_redraw(lambda: ...)` | CE's takes a zero-arg function only. | P24, V11 |
| `become(m, match_updaters=)` [161] | `become(m)` | No `match_updaters` (TypeError). | P35 |
| `set_z_index` [172] | same | Parameter is named `z_index_value`. | `src: mobject/mobject.py` |
| `fix_in_frame` [222] | ThreeDScene: `self.add_fixed_in_frame_mobjects(m)`; MovingCameraScene: `ce_ports.fix_in_frame(m, self.camera.frame)` | AttributeError on CE mobjects. | P25, V13, port |
| `set_submobject_colors_by_gradient` [72] | same | No `interp_by_hsl` (also missing from `color_gradient` and `interpolate_color`). | P36 |

### Functions and constants

| GL name [uses] | CE 0.22 | Differences / gotchas | Verified |
|---|---|---|---|
| `DEG` [776] | `DEGREES` | `DEG` doesn't exist in CE. | P36 |
| `FRAME_WIDTH` / `FRAME_HEIGHT` [321 / 182], `FRAME_X_RADIUS`, `RIGHT_SIDE`, `TOP`... | `config.frame_width` / `config.frame_height` (14.22 × 8, the same as GL's defaults); `config.frame_x_radius`, `config.right_side`, `config.left_side`, `config.top`, `config.bottom` | None of the GL constants exist in CE. | P36, `src: _config/utils.py` |
| `get_norm` [103] / `cross` [63] | `np.linalg.norm` / `np.cross` | Not in CE. | P36 |

## Same in both (present in CE 0.22 with the same core signature)

Checked by name and by a parameter diff (GL `ast` against CE `inspect`). Only the
noted differences were found.

- **Layout**: `arrange` (buff 0.25 in both), `next_to`, `move_to`, `shift`, `scale(about_point=, about_edge=)`, `rotate`,
  `to_edge`, `to_corner` (buff 0.5 in both), `align_to`, `match_x/y/width/height/color/style`,
  `set_x/y`, `get_x/y`, `get_center/top/bottom/left/right/corner/start/end`, `stretch`,
  `flip`, `surround`, `center`, `put_start_and_end_on`, `space_out_submobjects`,
  `shift_onto_screen`, `add_to_back`, `shuffle`, `sort`, `copy`, `fade`, `set_opacity`,
  `insert_n_curves`, `set_points_as_corners`, `family_members_with_points`.
- **Updater state**: `clear_updaters`, `suspend_updating`, `resume_updating`, `save_state`, `restore`, `generate_target`.
- **Mobjects**: `Line` (`buff`, `path_arc`), `Polygon`, `Triangle`, `RoundedRectangle` (no width/height positionals), `Elbow`, `ArcBetweenPoints`,
  `CurvedArrow`, `CubicBezier` (argument names differ), `Annulus`, `Sector`, `BulletedList`, `Code` (a different API: check `code_mobject.py`).
- **Animations**: `Rotating(m, angle=, axis=, about_point=)` (run_time 5, linear in both), `Uncreate`, `DrawBorderThenFill`, `Succession`, `MoveAlongPath`, `ShowSubmobjectsOneByOne`,
  `Homotopy`, `Swap`, `CyclicReplace`, `MaintainPositionRelativeTo`, `ApplyMethod`.
- **Functions**: `interpolate`, `inverse_interpolate`, `normalize`, `rotate_vector`, `midpoint`, `clip`,
  `choose`, `angle_of_vector`, `angle_between_vectors`, `compass_directions`, `bezier`, `color_gradient`,
  `interpolate_color`, `random_bright_color` (CE takes no range kwargs), `turn_animation_into_updater`, `cycle_animation`, `always_shift`, `always_rotate`,
  `index_labels`, `always` (the function form).
- **Rate functions**: `linear`, `smooth`, `there_and_back`, `there_and_back_with_pause`, `wiggle`,
  `rush_into`, `rush_from`, `squish_rate_func`, `running_start`.
- **Constants and colours**: `UP DOWN LEFT RIGHT UL UR DL DR OUT IN ORIGIN`, `PI TAU DEGREES`,
  `SMALL_BUFF MED_SMALL_BUFF MED_LARGE_BUFF LARGE_BUFF` (same values), `ITALIC`, and every GL
  colour name he uses (`GREY_A`…`GREY_E`, `BLUE_E`, `TEAL`, `PINK`, `LIGHT_PINK`, `PURE_GREEN`…)
  except `GREEN_SCREEN`. The only GL constants he uses that CE lacks are `DEG`, `GREEN_SCREEN` and the
  frame constants (`FRAME_*`, `RIGHT_SIDE`, `LEFT_SIDE`, `TOP`, `BOTTOM`).

## Camera

| GL (`self.frame` = CameraFrame) | CE | Verified |
|---|---|---|
| 2D pans and zooms: `self.frame.animate.set_height(h).move_to(p)` [92 + 42], `.scale` [35], `.shift` [20], `.set_x/.match_x` [24 / 14] | `class S(MovingCameraScene)`, `frame = self.camera.frame` (a `ScreenRectangle`). Then `self.play(frame.animate.set(height=h).move_to(p))`; `.scale`, `.shift`, `.set_x`, `.match_x` work unchanged. | V12 |
| `frame.save_state()` + `Restore(frame)`; `frame.animate.to_default_state()` [57] | `frame.save_state()` at the start, `Restore(frame)` later; or `frame.animate.set(height=config.frame_height).move_to(ORIGIN)`. Extra in CE: `self.camera.auto_zoom(mobs, margin=)`. | V12 |
| `mob.fix_in_frame()` while the frame moves [222] | `ce_ports.fix_in_frame(mob, self.camera.frame)` (an updater). Don't animate `mob` itself in the same `play()`: CE suspends its updater. | port |
| 3D orientation: `frame.reorient(θ, φ, γ, center, height)` [205; animated 801] | `class S(ThreeDScene)`; `self.set_camera_orientation(theta=(θ-90)*DEGREES, phi=φ*DEGREES, gamma=-γ*DEGREES, frame_center=center, zoom=8/height)`. The rotation matrices match exactly, e.g. GL `reorient(-30, 70)` = CE `theta=-120°, phi=70°`. | P44, V13 |
| `self.play(frame.animate.reorient(...))` | `self.move_camera(theta=, phi=, gamma=, zoom=, frame_center=, run_time=, added_anims=[...])` | V13 |
| `frame.add_ambient_rotation(ω)` [56] | `self.begin_ambient_camera_rotation(rate=ω)` (rad/s, same direction), `self.stop_ambient_camera_rotation()` | V13 |
| `title.fix_in_frame()` in 3D | `self.add_fixed_in_frame_mobjects(title)` | V13 |
| `frame.set_field_of_view(fov)` [36] | `self.set_camera_orientation(focal_distance=0.5 * h / tan(fov/2))`, where h is the frame height. GL's default 45° gives ≈ 9.66 at h = 8. CE's default is 20 (flatter perspective). | `src: camera/three_d_camera.py`; GL `camera/camera_frame.py` |
| `self.set_floor_plane("xz")` [38] | none: model the scene with z up instead | — |

## No reasonable CE equivalent

- **Shader effects**: `set_shading` [95], `set_flat_stroke` [67], `set_anti_alias_width` [20],
  `apply_depth_test` [70], `set_clip_plane` [63], `always_sort_to_camera` [45],
  `set_scale_stroke_with_zoom` [14], `TexturedSurface` [33], true GPU lighting on `Sphere`/`Surface`.
  CE's Cairo renderer has nothing similar. (`set_flat_stroke(x)` is a silent no-op; `set_shading(a, b, c)` is a TypeError.)
- **Variable-width strokes**: tapered `Underline`, `Cross`, `set_stroke(width=[...])`. Only the
  flash family is ported (by cutting the path into segments).
- **`make_number_changeable`**: use a separate `DecimalNumber` next to the label (V10).
- **`set_floor_plane`**, **`self.embed()`**, **`InteractiveScene` tooling**, **`wait(note=)`** (presenter mode).
- **custom/ characters**: `Randolph`, `PiCreature`, `TeacherStudentsScene`, `look_at=`, `added_anims=`
  come from `videos/custom/`, not manimlib. Not counted here and not available in CE.
- **SVG drawings** (`Checkmark` [31], `Exmark` [23], `SpeechBubble` [20], `ThoughtBubble` [17]):
  use `Tex(r"\checkmark")` or `Text("✓")`, `Text("✗")`, or draw your own shape.

## Ports (`ce_ports.py`)

`time_span`, `select`, `TransformMatchingStrings`, `set_backstroke`, `VShowPassingFlash`,
`FlashAround`, `FlashUnder`, `VFadeIn`, `VFadeOut`, `VFadeInThenOut`, `replicate`, `get_grid`,
`fix_in_frame`, `GlowDot`. Each docstring cites the GL source it follows. Self-test:
`.venv/bin/python reference/3b1b/ce_ports.py`. Demo:
`.venv/bin/manim -ql -s --media_dir reference/3b1b/_scratch_media reference/3b1b/ce_ports.py PortsDemo`.
