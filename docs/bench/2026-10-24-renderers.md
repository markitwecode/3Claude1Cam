# ManimCE renderer / encoder benchmark — 2026-10-24

Machine: Apple M1 Max (8P+2E), 32 GB. ManimCE 0.22.0, PyAV 18.1, moderngl 5.13, ffmpeg 7.1.1.
Command replicated from `engine/tools/render.py`: `engine/.venv/bin/manim -qh --media_dir <run>/media
--config_file <per-run cfg: text_dir/tex_dir> --disable_caching scenes/<stem>.py <Class>`, env from
`lib.paths.subprocess_env()` with `VK_PROJECT` = a scratch mirror (`bench/proj`: copied project.json + scenes,
`audio/` symlinked read-only), so the project and engine were never written. Each run starts from a copy of
a warm per-scene text cache (production has one from earlier previews). Times are `/usr/bin/time -l`;
"best of 2" unless noted. Nothing else rendering.

Scenes: `ch4_s3_trace` (TracingAppend, 65.15 s, 3909 frames) and `ch4_s6_cost` (CountingTheCost, 114.5 s,
6872 frames). Baseline encoder = libx264 crf 23 (preset medium), yuv420p, 456 kb/s on trace. Baseline
output matches the project's own 1080p60 render (same bitrate, same frame count).

## 1. Single-process results

SSIM/PSNR: ffmpeg `ssim`/`psnr`, mean over all frames. "vs lossless" = against a libx264 crf=0 render of the
same scene (same source frames), which separates encoder loss from the baseline's own loss. SSIM saturates on
this content (dark flat background + text), so PSNR and worst-frame SSIM are what discriminate.

### ch4_s3_trace

| Variant | wall s | CPU s | speedup | size MB | SSIM vs base | vs lossless: SSIM / worst-frame Y / PSNR |
|---|---|---|---|---|---|---|
| **Cairo + libx264 (baseline)** | **33.6** (34.8) | 79.5 | 1.00 | 4.63 | — | 0.99905 / 0.9985 / 50.1 dB |
| Cairo + x264, `--max-inflight-encoders 4` | **25.9** (26.6) | 81.3 | **1.30** | 4.63 | bit-identical | same as baseline |
| Cairo + VT q65 (`flags=+qscale global_quality=7670`) | 38.2 (41.2) | 41.2 | 0.88 | 14.6 | 0.99900 | 0.99907 / 0.9966 / 50.5 dB |
| Cairo + VT q65 + inflight 4 | 36.4 (36.4) | 44.7 | 0.92 | 15.1 | — | — |
| Cairo + VT default (no rate opts), 1 run | 37.4 | 40.8 | 0.90 | 30.2 | 0.99911 | 0.99972 / 0.9988 / 56.1 dB |
| Cairo + VT `b=1M`, 1 run | 36.6 | 39.4 | 0.92 | 11.5 | 0.99760 | 0.99755 / **0.9744** / 43.5 dB |
| Cairo + VT `b=2M`, 1 run | — | — | — | 18.3 | 0.99861 | 0.99879 / **0.9775** / 47.7 dB |
| Cairo + VT q50 / q62 / q72, 1 run each | ~35–36 | ~40 | — | 9.4 / 13.7 / 18.4 | — | PSNR 44.9 / 49.8 / 54.4 dB |
| Cairo + x264 `preset=veryfast` | 31.5 (32.5) | 68.9 | 1.06 | 4.20 | 0.99843 | 0.99835 / 0.9976 / 47.3 dB (worse) |
| Cairo + x264 `threads=2`, 1 run | 47.9 | 74.1 | 0.70 | 4.02 | — | — |
| **OpenGL + libx264** (3 shims, see §3) | 62.7 (63.2) | 99.6 | **0.54** | 4.68 | 0.982 (timing drift + text weight) | — |
| OpenGL + VT q65 | 63.7 (68.3) | 58.0 | 0.53 | 15.0 | — | — |

### ch4_s6_cost

| Variant | wall s | CPU s | speedup | size MB | SSIM vs base | vs lossless: SSIM / PSNR |
|---|---|---|---|---|---|---|
| Cairo + libx264 (baseline) | 56.0 (65.5) | 133.8 | 1.00 | 7.12 | — | 0.99926 / 52.1 dB |
| Cairo + x264, inflight 4 | **38.0** (38.4) | 133.0 | **1.47** | 7.12 | bit-identical | same |
| Cairo + VT q65 | 66.7 (67.0) | 68.1 | 0.84 | 14.3 | 0.99908 | 0.99929 / 51.8 dB |

Run-to-run noise: up to ~15% on a single run (baseline cost runs 56.0 vs 65.5 s); trace runs within ~4%.

VT notes: ABR (`b=`) starves each segment's opening frames (worst-frame SSIM 0.974–0.978), so use constant
quality (`--encoder-option flags=+qscale --encoder-option global_quality=<q*118>`). q65 matches baseline quality
on both scenes at 2–3x the file size. The default VT bitrate is not too low here: it's ~3.7 Mb/s, 6.5x baseline.
Segment joins decode cleanly (0 ffmpeg errors).

## 2. Where baseline time goes (instrumented run, ch4_s3_trace)

Inclusive wall/CPU timers on renderer, camera, file-writer and encoder methods (`bin/prof_manim.py`).
Instrumented wall 36.9 s vs 33.6 s clean; the ~3 s overhead lands mostly in the Cairo inner calls.

**Wall-clock critical path (main thread):**
| Bucket | wall s | share |
|---|---|---|
| Cairo drawing: `capture_mobjects` 12.8 (path building in Python/numpy 5.8, fill raster 4.3, stroke 0.8) + background reset 2.9 + frame copy 1.5 | ~17 (≈14 without instrumentation) | ~45% |
| **Main thread idle, waiting for the segment encoder to finish** (`_PartialMovieEncodeJob.join` at each of 58 animation ends) | **13.5** | ~37% |
| Python scene work: interpolation and updaters (`update_to_time`) 1.5, `begin_animations` 0.7, static-frame prep 0.3, construct glue ~0.6 | ~3 | ~9% |
| Final concat + audio mux 1.4, imports and startup ~1.3 | ~2.7 | ~8% |

**CPU (83 s total):** main thread 19.4 s (Cairo + Python); encoder Python thread 15.3 s (RGBA to yuv420p
swscale + frame copies + encode calls, one per output frame, static waits included); **libx264 worker threads
≈ 48 s**. So **~76% of CPU is encoding**. Static `wait()`s are encoded frame by frame (repeat=N), so a 65 s scene
always costs 3909 frames of conversion and encoding.

**Ceilings.** (A) A free renderer removes only the Cairo bucket. Single-process, the encoder thread (busy
~25 s) then becomes the limit: ≤ ~1.35x. It's also only ~15% of CPU, so a CPU-bound parallel batch gains
≤ ~1.2x. (B) The encoder is the big CPU consumer and the main
source of idle wait. Hiding the wait (inflight encoders) is worth 1.3–1.5x single-process. Cutting encoder CPU
only helps batches if the replacement isn't itself a bottleneck. VT is (§4).

## 3. OpenGL renderer

Fails out of the box on this scene. Three breakages, each shimmed at launch in `bin/gl_manim.py` (no scene
edits; about 15 min):
1. `set_z_index` doesn't exist on OpenGL mobjects (`AttributeError` in the scene's `hbox`; also used in
   `engine/lib/kit.py`, and in **21 of 42 scenes** with 29 calls). The OpenGL renderer has no z-index at all; it
   draws `scene.mobjects` in list order. Shim: store `z_index` and sort top-level mobjects in `update_frame`
   (nested z-index is still ignored).
2. `engine/lib/effects.py` (`FlashAround` tapered path) and **22 scenes** construct plain `VMobject()`, which
   is the Cairo class and can't be mixed with OpenGL mobjects (`TypeError: Expected a VMobject`). Shim:
   `manim.VMobject = OpenGLVMobject`.
3. `set_cap_style` doesn't exist on `OpenGLVMobject` (effects.py). Shim: no-op (the GL stroke shader has fixed caps).

With the shims it renders, but **1.9x slower** (62.7 s vs 33.6 s) and with more CPU (99.6 s). Why (cProfile):
~29k synchronous draw calls at ~0.54 ms each (15.7 s, Apple's deprecated GL-over-Metal driver), framebuffer
readback 2.4 ms/frame (5 s), ~10 s of per-frame Python shader-data prep, ~8 s deepcopy in setup, and it still
waits ~12 s on the encoder. The GPU doesn't buy anything on macOS through moderngl/OpenGL.

**Visual differences** (sheets in `sheets/`; `contact_trace.png` = same timestamps,
`contact_trace_aligned.png` = OpenGL frames shifted by the measured lag; crops `crop_*.png`):
- **Timing drift / A-V sync:** OpenGL writes 3902 frames vs 3909. Its events land progressively earlier: 0–1
  frames at the start, 3 by ~25 s, 7 frames (0.12 s) by 60 s. Audio is placed by scene time, so the picture
  runs ahead of the narration. This is the same class of bug as LESSONS.md's cache drift (0.33 s/scene was
  noticeable).
- **Text/code glyphs heavier and brighter:** +24% integrated "ink" on the same word (all Code/Text/MathTex
  look semi-bold next to Cairo).
- **Stroke widths:** identical (measured edge profiles of the gold box match pixel for pixel). Antialiasing on
  boxes and glyph edges looks equivalent at 1080p.
- **Layering:** correct here only because of the top-level z sort. Nested `set_z_index` and the
  fill-then-stroke batching of OpenGL families can reorder overlapping parts in other scenes (not seen in
  this scene).
- **Colours, layout, positions:** match. The rounded-corner inset box and the dimmed (opacity) code render
  the same apart from the text weight.
- **Dashed lines:** none in this scene, not assessed.
- Mean SSIM vs baseline is 0.982 (PSNR 29.5), dominated by the drift and the text weight.

## 4. Parallel batches (real finals run 7–8 scenes at once)

| Batch | batch wall s | Σ CPU s | Σ RSS GB | vs baseline |
|---|---|---|---|---|
| 4x trace, baseline | **58.4** | 388 | 4.1 | 1.00 |
| 4x trace, x264 inflight 4 | 60.8 | 401 | 6.6 | 0.96 |
| 4x trace, VT q65 | 62.1 | 200 | 2.4 | 0.94 |
| 4x trace, VT q65 + inflight 4 | **111.3** | 210 | 3.2 | **0.52** |
| 8x mixed (4 trace + 4 cost), baseline | **147.7** | 1075 | 9.1 | 1.00 |
| 8x mixed, VT q65 | **177.4** | 552 | 5.4 | **0.83** |
| 8x mixed, hybrid: 4 on x264 + 4 on VT | 137.3 | 854 | 6.8 | 1.08 (within noise) |

(Single run per batch. Inflight-4 was skipped at 8x: no gain at 4x, and ~21 GB RSS with 12 GB swap already in use.)

**Why VT loses in parallel:** the M1 Max media engine is one shared resource. Raw ffmpeg test: 1 session
≈ 366 fps 1080p, 4 concurrent sessions ≈ 397 fps total. Through manim's pipeline (yuv420p frames copied
into CVPixelBuffers one at a time), the batch tops out at ~245–250 fps. Baseline x264 on the CPU reached
~290 fps over the same 8-scene batch. VT halves CPU (frees the machine for other work), but caps throughput,
and many concurrent VT sessions (VT + inflight) thrash it.

**Why inflight encoders don't help in parallel:** they only hide per-process idle time; with 4+ processes
the cores are already busy filling it.

## Recommendation

- **Don't adopt videotoolbox for finals:** quality-matched (q65) it's 12–16% slower single-scene and 17%
  slower on a real 8-scene batch, with 2–3x larger files. Its one win is halving CPU. Use it only if keeping the
  machine responsive matters more than finish time.
- **Don't pursue OpenGL:** 1.9x slower here, 3 API breakages touching `engine/lib` and half the scenes, an
  A/V drift bug, and heavier text. Even a free renderer caps at ~1.2x for parallel batches.
- **Cheap, safe win for single-scene renders** (fix passes: `vk render --only`, single-scene finals):
  `--max-inflight-encoders 4` gives a bit-identical video 1.3–1.5x faster, at ~2x RSS (~2.6 GB/scene). Don't add
  it to the 7–8-way chapter final (no gain, memory risk). Example: pass it in `render.py` only when one or
  two scenes are queued.

## Files
- `bin/run.py`: one timed render (render.py replica); `bin/batch.sh`: concurrent batch; `bin/prof_manim.py`: instrumented
  timers; `bin/gl_manim.py`: OpenGL shims; `bin/ssim.sh`, `bin/cmp.sh`: SSIM/PSNR.
- `results.jsonl` (every single run), `batches.jsonl`, `prof_base_trace.json`, `prof_vt_trace.json`, `cprof_gl.prof`.
- `runs/<variant>/media/videos/...`: outputs (partial movie files deleted); `sheets/`: contact sheets and crops.
