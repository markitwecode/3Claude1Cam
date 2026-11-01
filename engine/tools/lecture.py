"""Source material from a lecture recording: an exact local transcript plus Gemini's digest of
what was shown and said.

    vk lecture <video> [--model gemini-3.8-flash-medium] [--chunk 600] [--until 20:00] [--name l05-rec]

Writes, next to the other material (the course's source/ for a course lecture, the project's
source/ for a one-off, as `vk new --source` does), and records in project.json "sources":
- <stem>.transcript.md: Whisper medium on the GPU (MLX, the same model and decoder as the voice
  QA in tools/voiceqa.py), one "[hh:mm:ss] text" line per segment. Free and exact.
- <stem>.digest.md: Gemini watches ~10-minute pieces at 720p (~150k tokens each, at most 2 at a
  time) and returns per topic segment: the board/slide/screen content verbatim (code, commands,
  queries, output, formulas), diagrams described to redraw, examples, emphasis, student questions
  and answers, demos. Times are absolute (the piece's offset added). Not a transcript.
- <stem>.captions.md: the file's own subtitle track, if it has one (e.g. Panopto auto-captions),
  in the transcript's format, as a free cross-check.
The video itself stays where it is (it's read in place, never copied). Each piece's Gemini answer
is cached in media/lecture/<stem>/, so a re-run after a failure only redoes the missing pieces
(--redo ignores the cache). --until limits everything to the start of the recording (testing).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(ENGINE / "tools"))
from lib.paths import STUDIO, config, project, rel  # noqa: E402
from gemini import (DEFAULT_MODEL, GeminiError, add_usage, cut, ffprobe_duration,  # noqa: E402
                    fmt_usage, hms, parse_time, watch)

ROOT = project()
PROJECTS = STUDIO / "projects"
SR = 16000
WHISPER = "medium"           # a key of voiceqa.QA_MODELS
BATCH = 8                    # Whisper windows decoded together
GATE = 0.05                  # 10 ms frames this far under the loud speech (p99) are a pause (-26 dB)
DIGEST_VERSION = 1           # bump when the prompt or schema changes (invalidates cached pieces)

_LIST = {"type": "array", "items": {"type": "string"}}
SCHEMA = {
    "type": "object",
    "properties": {"segments": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "start": {"type": "string", "description": "mm:ss from the start of this clip"},
            "end": {"type": "string", "description": "mm:ss from the start of this clip"},
            "topic": {"type": "string"},
            "screen": {"type": "string", "description": "board/slide/screen content verbatim, line breaks kept"},
            "points": _LIST,
            "diagrams": _LIST,
            "examples": _LIST,
            "emphasis": _LIST,
            "questions": {"type": "array", "items": {
                "type": "object",
                "properties": {"question": {"type": "string"}, "answer": {"type": "string"}},
                "required": ["question", "answer"]}},
            "demos": _LIST,
        },
        "required": ["start", "end", "topic", "screen", "points", "diagrams", "examples", "emphasis",
                     "questions", "demos"],
    }}},
    "required": ["segments"],
}

PROMPT = """This is part {i} of {k} of a recorded university lecture{course}. The clip runs from {a} to {b} of the full recording. Give every time as mm:ss from the start of THIS clip.

Write study notes that let someone who never saw the lecture rebuild its content as teaching material. Split the clip into segments, one per topic or step (usually 1-5 minutes each), in order, covering the whole clip. For each segment:
- topic: a short title.
- screen: what is on the board, slides or screen, VERBATIM where legible: code, terminal commands with their prompts, queries, program output and result tables, formulas, slide text. Keep line breaks and indentation; write [illegible] for parts you can't read. If it is a screen recording with a small picture-in-picture of the lecturer, read the screen itself (the inset only matters for gestures or a physical board). Include every command or query typed and its output, in the order they appear, and the final version of anything edited.
- points: what the lecturer explains, as precise statements (definitions, rules, reasoning, caveats), in order.
- diagrams: each diagram drawn or shown, described well enough to redraw it (elements, labels, arrows, layout).
- examples: the examples used (data, values, inputs and results).
- emphasis: anything flagged as important ("this is the key idea", "this will be on the exam", repeated warnings), quoted where possible.
- questions: student questions and the lecturer's answers.
- demos: live demos: what was run and what happened, including errors and how they were fixed.
Do not write a verbatim transcript of the speech: a separate transcript exists. Leave a field empty when there is nothing for it."""


# ── where the material goes ────────────────────────────────────────────────────
def material_dir():
    """(folder for material, path prefix as project.json records it): the course's source/ for a
    course lecture (projects/<course>/<lecture>/, or any project whose parent has a COURSE.md),
    else the project's own source/ (tools/new_project.py's rule)."""
    parent = ROOT.parent
    course = parent != PROJECTS and (PROJECTS in ROOT.parents or (parent / "COURSE.md").exists())
    return (parent / "source", Path("..", "source")) if course else (ROOT / "source", Path("source"))


def record_sources(entries):
    """Add or replace project.json "sources" entries (matched by path)."""
    path = ROOT / "project.json"
    cfg = json.loads(path.read_text())
    sources = [s for s in cfg.get("sources", []) if s.get("path") not in {e["path"] for e in entries}]
    cfg["sources"] = sources + entries
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


# ── transcript: Whisper medium on the GPU, via voiceqa's model and decoder ─────
def load_audio(video, until):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", f"{until:.3f}", "-i", str(video), "-vn", "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32)


def _segments(tokens, tok, limit):
    """[(start s, text)] from a timestamped decode (the timestamp-aware twin of
    voiceqa._speech_words): empty segments and any starting at/after `limit` are dropped."""
    out, start, text = [], 0.0, []
    for t in list(tokens) + [None]:
        if t is None or t >= tok.timestamp_begin:
            at = None if t is None else (t - tok.timestamp_begin) * 0.02
            if text and start < limit and at != start:
                s = tok.decode(text).strip()
                if s:
                    out.append((start, s))
            text = []
            if at is not None:
                start = at
        elif t < tok.eot:
            text.append(t)
    return out


def transcribe(x, log=print, debug=False):
    """[(absolute start s, text)] for 16 kHz mono audio, with voiceqa's model and decoder: windows
    of <= 29.5 s (voiceqa.windows), each decoded once, greedily, stopped at its end of speech, with
    the loop guard; so none of mlx-audio's own generate() failures (invented sentences, gibberish).
    Lecture audio has no exact silence for voiceqa.windows to cut in, so it is given a copy with
    the pauses (10 ms frames GATE under the loud speech) zeroed: it then cuts in the middle of a
    pause, never inside a word. A window Whisper itself judges speechless (no-speech probability
    > 0.6 with a low average log-probability, openai-whisper's rule) is dropped: over room noise
    Whisper writes "Thank you." again and again."""
    import mlx.core as mx
    import numpy as np
    from mlx_audio.stt.models.whisper.audio import N_FRAMES, N_SAMPLES, log_mel_spectrogram, pad_or_trim
    from mlx_audio.stt.models.whisper.decoding import DecodingOptions, DecodingTask
    import voiceqa

    import slots
    _gpu = slots.gpu("vk lecture transcript", gb=3.0)  # noqa: F841  held until this process exits
    os.nice(10)        # nobody's loop waits on a lecture transcript: low CPU priority (2026-11-01)
    model, tok = voiceqa.Voters([WHISPER])._model(WHISPER)
    n = len(x) // 160 * 160
    rms = np.sqrt(np.mean(x[:n].reshape(-1, 160) ** 2, axis=1))       # 10 ms frames
    loud = float(np.percentile(rms, 99)) if len(rms) else 0.0
    gate = max(1e-3, GATE * loud)
    gated = x.copy()
    gated[:n].reshape(-1, 160)[rms < gate] = 0.0
    spans = voiceqa.windows(gated, SR)
    jobs = []
    for a, b in spans:
        voiced = np.flatnonzero(rms[a // 160:b // 160] >= gate)
        if len(voiced) < 30:            # under 0.3 s above the gate: nothing to transcribe
            continue
        # start at the first sound: Whisper stamps its first segment at the window's start
        a2 = a + max(0, voiced[0] - 20) * 160
        jobs.append((a2, b, (voiced[-1] + 1) / 100 - (a2 - a) / SR))
    out, t0, dropped = [], time.time(), 0
    for i in range(0, len(jobs), BATCH):
        batch = jobs[i:i + BATCH]
        mels = []
        for a, b, end in batch:         # as voiceqa.Voters.hear: content frames, zero-padded
            stop = min(b, a + int((end + 0.25) * SR))
            mel = log_mel_spectrogram(mx.array(x[a:stop]), n_mels=model.dims.n_mels, padding=N_SAMPLES)
            mels.append(pad_or_trim(mel[:mel.shape[-2] - N_FRAMES], N_FRAMES, axis=-2).astype(model.dtype))
        task = DecodingTask(model, DecodingOptions(language="en", task="transcribe", temperature=0.0,
                                                   without_timestamps=False))
        limits = [max(0.3, end - 0.2) for _, _, end in batch]
        task.logit_filters += [voiceqa._NoLoops(task.sample_begin),
                               voiceqa._StopAtSpeechEnd(tok, task.sample_begin, limits)]
        for r, (a, b, _), limit in zip(task.run(mx.stack(mels)), batch, limits):
            segs = [(t, text) for t, text in _segments(r.tokens, tok, limit) if re.search(r"\w", text)]
            texts = {re.sub(r"\W", "", text.lower()) for _, text in segs}
            silent = (r.no_speech_prob > 0.6 and r.avg_logprob < -1.0) or not segs \
                or (r.avg_logprob < -1.0 and (len(texts) == 1 and len(segs) > 1     # "Thank you." ×5
                                              or sum(len(t.split()) for _, t in segs) <= 4))
            if debug:
                log(f"    [{hms(a / SR)}–{hms(b / SR)}] no_speech {r.no_speech_prob:.2f} "
                    f"logprob {r.avg_logprob:.2f}{' DROPPED' if silent else ''}: {r.text[:90]!r}")
            if silent:
                dropped += 1
                continue
            out += [(a / SR + s, text) for s, text in segs]
        log(f"  transcript: {hms(batch[-1][1] / SR)} of {hms(len(x) / SR)} ({time.time() - t0:.0f}s)", flush=True)
    if dropped:
        log(f"  transcript: {dropped} window(s) without speech dropped")
    return out


def sentences(segments, longest=20.0):
    """Whisper's 2-5 s segments joined into sentence lines (at most `longest` s each)."""
    out = []
    for t, text in segments:
        if out and not re.search(r"[.?!]['\")]?$", out[-1][1]) and t - out[-1][0] < longest:
            out[-1] = (out[-1][0], f"{out[-1][1]} {text}")
        else:
            out.append((t, text))
    return out


def write_lines(path, title, note, segments):
    body = "\n".join(f"[{hms(t)}] {text}" for t, text in segments)
    path.write_text(f"# {title}\n\n{note}\n\n{body}\n")


# ── captions: the file's own subtitle track ────────────────────────────────────
def captions(video, until):
    """[(start s, text)] from the first subtitle stream, or None if there is none."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "s", "-show_entries",
                            "stream=index:stream_tags=handler_name,language", "-of", "json", str(video)],
                           capture_output=True, text=True)
    streams = json.loads(probe.stdout or "{}").get("streams", [])
    if not streams:
        return None, ""
    tags = streams[0].get("tags", {})
    srt = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-map", "0:s:0", "-f", "srt", "-"],
                         capture_output=True, text=True).stdout
    out = []
    for block in re.split(r"\n\s*\n", srt.replace("\r", "")):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->", block)
        if not m:
            continue
        t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 1000
        text = " ".join(re.sub(r"<[^>]+>", "", l).strip() for l in block.split("\n")[block.count("\n", 0, m.end()) + 1:])
        if t < until and text.strip():
            out.append((t, text.strip()))
    return out, " ".join(v for v in (tags.get("handler_name"), tags.get("language")) if v)


# ── digest: Gemini watches ~10-minute pieces ───────────────────────────────────
def pieces(span, chunk):
    out, s = [], 0.0
    while s < span - 1e-6:
        d = min(chunk, span - s)
        if out and d < 60:              # a short tail joins the piece before it
            out[-1] = (out[-1][0], out[-1][1] + d)
            break
        out.append((s, d))
        s += d
    return out


def digest_piece(video, i, parts, model, cache_dir, redo, tmp):
    start, dur = parts[i]
    key = cache_dir / f"piece_{int(start)}_{int(round(dur))}_{model}_v{DIGEST_VERSION}.json"
    if key.exists() and not redo:
        got = json.loads(key.read_text())
        print(f"  digest piece {i + 1}/{len(parts)}: cached ({len(got['data']['segments'])} segments)", flush=True)
        return {**got, "cached": True}
    clip = cut(video, Path(tmp) / f"piece{i + 1}.mp4", start, dur)
    course = config().get("course_line", "")
    prompt = PROMPT.format(i=i + 1, k=len(parts), a=hms(start), b=hms(start + dur),
                           course=f" ({course})" if course else "")
    r = watch(clip, prompt, SCHEMA, model=model)
    got = {"start": start, "duration": dur, "model": model, "seconds": round(r.seconds, 1),
           "attempts": r.attempts, "usage": r.usage, "data": r.data}
    key.write_text(json.dumps(got, indent=1, ensure_ascii=False))
    print(f"  digest piece {i + 1}/{len(parts)} [{hms(start)}–{hms(start + dur)}]: "
          f"{len(r.data.get('segments', []))} segments, {r.seconds:.0f}s, {fmt_usage(r.usage)}"
          + (f", {r.attempts} attempts" if r.attempts > 1 else ""), flush=True)
    return got


def _fence(text):
    ticks = "````" if "```" in text else "```"
    return f"{ticks}\n{text.rstrip()}\n{ticks}"


def digest_md(video, model, parts, results, chunk):
    lines = [f"# Digest: {video.name}", "",
             f"Gemini ({model}) watched {video}, {hms(0)}–{hms(parts[-1][0] + parts[-1][1])}, in "
             f"{len(parts)} piece(s) of ≤ {chunk:.0f} s (a topic that crosses a piece boundary shows as two "
             "segments). Times are hh:mm:ss from the start of the recording. These are a model's notes: "
             "check code, output and numbers against the transcript or the video.", ""]
    for (start, dur), got in zip(parts, results):
        if isinstance(got, Exception):
            lines += [f"## [{hms(start)}–{hms(start + dur)}] MISSING: {got}", ""]
            continue
        for seg in got["data"].get("segments", []):
            a, b = parse_time(seg.get("start", "")), parse_time(seg.get("end", ""))
            a = start + (a if a is not None else 0.0)
            b = start + (b if b is not None else dur)
            lines += [f"## [{hms(a)}–{hms(min(b, start + dur))}] {seg.get('topic', '').strip()}", ""]
            if seg.get("screen", "").strip():
                lines += ["**Screen**", _fence(seg["screen"]), ""]
            for key, label in (("points", "Points"), ("diagrams", "Diagrams"), ("examples", "Examples"),
                               ("emphasis", "Emphasis"), ("demos", "Demos")):
                items = [x.strip() for x in seg.get(key, []) if x.strip()]
                if items:
                    lines += [f"**{label}**", *(f"- {x}" for x in items), ""]
            qs = [q for q in seg.get("questions", []) if q.get("question", "").strip()]
            if qs:
                lines += ["**Questions**", *(f"- Q: {q['question'].strip()}\n  A: {q.get('answer', '').strip()}"
                                             for q in qs), ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Transcript + digest of a lecture recording, as source material.")
    ap.add_argument("video")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--chunk", type=float, default=600, help="seconds of video per Gemini call (default 600)")
    ap.add_argument("--until", help="only the first part of the recording: seconds or hh:mm:ss (testing)")
    ap.add_argument("--name", help="file stem for the outputs (default: the video's)")
    ap.add_argument("--no-transcript", action="store_true")
    ap.add_argument("--no-digest", action="store_true")
    ap.add_argument("--redo", action="store_true", help="ignore cached digest pieces")
    args = ap.parse_args()

    video = Path(os.environ.get("VK_CALLER_PWD") or os.getcwd(), args.video).expanduser().resolve()
    if not video.exists():
        sys.exit(f"no such file: {video}")
    full = ffprobe_duration(video)
    until = parse_time(args.until) if args.until else None
    if args.until and until is None:
        sys.exit(f"--until: can't read {args.until!r}")
    span = min(full, until or full)
    stem = args.name or video.stem
    dest, prefix = material_dir()
    dest.mkdir(parents=True, exist_ok=True)
    cache_dir = ROOT / "media" / "lecture" / stem
    cache_dir.mkdir(parents=True, exist_ok=True)
    part_note = f", first {hms(span)} of {hms(full)}" if span < full - 1 else ""
    print(f"lecture {video.name} ({hms(full)}{part_note}) -> {rel(dest)}/{stem}.*")

    t0 = time.time()
    entries, usage, failed = [], {}, 0
    with tempfile.TemporaryDirectory(prefix="vk-lecture-") as tmp, ThreadPoolExecutor(max_workers=2) as pool:
        parts = pieces(span, args.chunk)
        futures = [] if args.no_digest else [
            pool.submit(digest_piece, video, i, parts, args.model, cache_dir, args.redo, tmp)
            for i in range(len(parts))]

        caps, track = captions(video, span)
        if caps:
            path = dest / f"{stem}.captions.md"
            write_lines(path, f"Captions: {video.name}",
                        f"The recording's own subtitle track ({track}), {hms(0)}–{hms(span)}. A cross-check "
                        f"for {stem}.transcript.md (Whisper).", caps)
            entries.append({"path": str(prefix / path.name), "pages": "",
                            "note": f"embedded captions ({track}) of {video.name}{part_note}; cross-check only"})
            print(f"captions: {len(caps)} lines -> {rel(path)}")

        if not args.no_transcript:
            t1 = time.time()
            segs = sentences(transcribe(load_audio(video, span)))
            path = dest / f"{stem}.transcript.md"
            write_lines(path, f"Transcript: {video.name}",
                        f"Whisper {WHISPER} (MLX, local, greedy) of {video}, {hms(0)}–{hms(span)}. "
                        "Each line: [hh:mm:ss] from the start of the recording.", segs)
            entries.append({"path": str(prefix / path.name), "pages": "",
                            "note": f"Whisper {WHISPER} transcript of {video}{part_note}"})
            print(f"transcript: {len(segs)} segments, {sum(len(t.split()) for _, t in segs)} words, "
                  f"{time.time() - t1:.0f}s -> {rel(path)}")

        if futures:
            results = []
            for f in futures:
                try:
                    results.append(f.result())
                except (GeminiError, subprocess.CalledProcessError) as e:
                    results.append(e)
                    failed += 1
                    print(f"  digest piece failed: {e}", flush=True)
            for got in results:
                if not isinstance(got, Exception) and not got.get("cached"):
                    add_usage(usage, got["usage"])
            path = dest / f"{stem}.digest.md"
            path.write_text(digest_md(video, args.model, parts, results, args.chunk))
            entries.append({"path": str(prefix / path.name), "pages": "",
                            "note": f"Gemini ({args.model}) digest of {video.name}{part_note}: screen content, "
                                    "diagrams, examples, emphasis, Q&A, demos"
                                    + (f"; {failed} piece(s) MISSING, re-run vk lecture" if failed else "")})
            n_seg = sum(len(g["data"].get("segments", [])) for g in results if not isinstance(g, Exception))
            print(f"digest: {n_seg} segments from {len(parts)} piece(s)"
                  + (f", {failed} failed" if failed else "") + f"; Gemini {fmt_usage(usage)} -> {rel(path)}")

    if entries:
        record_sources(entries)
        print(f"recorded {len(entries)} source(s) in {rel(ROOT / 'project.json')}")
    print(f"done in {time.time() - t0:.0f}s ({date.today().isoformat()})")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
