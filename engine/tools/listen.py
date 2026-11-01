"""Ear check of a chapter's voiced narration by Gemini (audio only): every word or letter not
pronounced as the script writes it.

    vk listen 4 [--only c4.cost.2 c4.cost.4] [--model M]

Chapter N's clips (audio/<id>.wav, script order, or just --only) are joined with 1 s of silence
into one mp3 (~32 Gemini tokens per second of audio, so a whole chapter is one request; agy's file
viewer attaches mp3 but not m4a). Gemini gets every clip's id, its start in the audio and its
exact text (manifest "raw", marks stripped), and reports words heard differently from the text:
single letters ("en", "ex", "ell"), identifiers and numbers above all; accent and prosody don't
count. Each finding is snapped to the script word it names in that clip, which gives its sentence
number (as `vk qa` counts them: voice.split_line); "+qa" marks one the Whisper consensus QA also
flagged, "≈" one whose expected words weren't found in the clip's text.

Output: media/review/chN_listen.{json,md} (chN_listen_partial.* with --only); the .md is printed:
    c4.cost.3:6 "en wide" → "on wide"  (high, conf high)  @ 18.2 s
Writes nothing outside media/review/.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
import wave
from datetime import datetime
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(ENGINE / "tools"))
from lib.paths import project, rel  # noqa: E402
from gemini import DEFAULT_MODEL, fmt_usage, mss, parse_time, watch  # noqa: E402
from review import snap  # noqa: E402
from voice import TOKEN_RE, parse_scripts, split_line  # noqa: E402
from voiceqa import reported  # noqa: E402

ROOT = project()
GAP = 1.0            # s of silence between clips
LEVELS = ["high", "medium", "low"]

PROMPT = """Open the audio and listen to all of it. It is the text-to-speech narration of chapter {n} of an explainer video, {k} clips joined with one second of silence. Here is exactly what each clip should say, with the time it starts in the audio (mm:ss.s):

{clips}

How the text is meant to be read: letters and code names are spelled the way they should sound. "en" is the letter n, "ex" is x, "exes" is xs, "whys" is ys (it sounds like "wise"), "ell" is l, "kay" is k; a hyphenated name like "en-rev" or "rev-app" is said as its parts ("en rev", "rev app"). Numbers are said as written.

Report every word or letter that is not pronounced as written: a different or garbled word, a wrong vowel or consonant that makes it a different word or letter (e.g. "en" said as "on" or "an"), a skipped, repeated or added word, a misread number or identifier. Check single letters, identifiers and numbers with special care. Do not report accent, intonation, emphasis, pace or pauses. Report each occurrence separately. If every word is right, report nothing; don't invent problems."""


def schema(ids):
    return {
        "type": "object",
        "properties": {"findings": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "clip": {"type": "string", "enum": ids},
                "time": {"type": "string", "description": "mm:ss.s from the start of the audio, when the word is said"},
                "expected": {"type": "string", "description": "the exact word(s) from the clip's text"},
                "heard": {"type": "string", "description": "what it sounds like instead, plain spelling, no IPA"},
                "severity": {"type": "string", "enum": LEVELS},
                "confidence": {"type": "string", "enum": LEVELS},
            },
            "required": ["clip", "time", "expected", "heard", "severity", "confidence"],
        }}},
        "required": ["findings"],
    }


def join(ids, manifest, out_wav):
    """Concatenate the clips' wavs with GAP s of silence -> {id: start s}."""
    starts, t, params = {}, 0.0, None
    with wave.open(str(out_wav), "wb") as dst:
        for k, cid in enumerate(ids):
            with wave.open(str(ROOT / manifest[cid]["file"]), "rb") as src:
                if params is None:
                    params = src.getparams()
                    dst.setparams(params)
                elif src.getparams()[:3] != params[:3]:
                    sys.exit(f"{cid}: audio format differs from the other clips")
                if k:
                    silence = int(GAP * params.framerate)
                    dst.writeframes(b"\0" * silence * params.sampwidth * params.nchannels)
                    t += GAP
                starts[cid] = t
                frames = src.readframes(src.getnframes())
                dst.writeframes(frames)
                t += src.getnframes() / params.framerate
    return starts


def main():
    import gemini as _g
    if _g.off_reason():   # Gemini's quota is out: say so plainly, exit 3 (agents treat it as "skipped")
        print(f"vk listen: skipped, Gemini is off ({_g.off_reason()}). Use vk qa / vk check / vk holds / "
              "builder frames instead (chapter-director.md, \"When Gemini is off\").", flush=True)
        sys.exit(3)
    ap = argparse.ArgumentParser(description="Gemini listens to a chapter's narration for mispronunciations.")
    ap.add_argument("chapter", type=int)
    ap.add_argument("--only", nargs="+", metavar="ID", help="just these clips")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()
    n = args.chapter
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    script = parse_scripts(n)
    if not script:
        sys.exit(f"no script/ch{n}_*.md")
    ids = [cid for cid in script if cid in manifest]
    if args.only:
        bad = [c for c in args.only if c not in manifest]
        if bad:
            sys.exit(f"not voiced: {', '.join(bad)}")
        ids = [c for c in ids if c in args.only] + [c for c in args.only if c not in script]
    unvoiced = [c for c in script if c not in manifest and (not args.only or c in args.only)]
    stale = [c for c in ids if c in script and manifest[c].get("raw") != script[c]]
    warnings = ([f"not voiced, skipped: {', '.join(unvoiced)}"] if unvoiced else []) + \
               ([f"changed since voicing (the audio says the old text): {', '.join(stale)}"] if stale else [])
    texts = {c: " ".join(TOKEN_RE.sub(" ", manifest[c]["raw"]).split()) for c in ids}

    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="vk-listen-") as tmp:
        starts = join(ids, manifest, Path(tmp) / "all.wav")
        mp3 = Path(tmp) / f"ch{n}_narration.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(Path(tmp) / "all.wav"), "-c:a", "libmp3lame",
                        "-b:a", "96k", str(mp3)], check=True)
        total = max(starts.values()) + manifest[ids[-1]]["duration"] if ids else 0
        print(f"listening to {len(ids)} clip(s) of chapter {n} ({mss(total)}) with {args.model}", flush=True)
        prompt = PROMPT.format(n=n, k=len(ids), clips="\n".join(f"[{mss(starts[c])}] {c}: {texts[c]}" for c in ids))
        r = watch(mp3, prompt, schema(ids), model=args.model)
    seconds = time.time() - t0

    clips = {c: {"id": c, "start": starts[c], "end": starts[c] + manifest[c]["duration"],
                 "words": [(w, starts[c] + wt) for w, wt in manifest[c].get("words", [])]} for c in ids}
    order = {c: k for k, c in enumerate(ids)}
    findings = []
    for f in r.data.get("findings", []):
        t = parse_time(f.get("time", ""))
        cid = f.get("clip") if f.get("clip") in clips else None
        if cid is None and t is not None:
            cid = next((c for c in reversed(ids) if starts[c] <= t), ids[0])
        if cid is None:
            warnings.append(f"finding without clip or time: {f}")
            continue
        c = clips[cid]
        t = t if t is not None and c["start"] - 2 <= t <= c["end"] + 2 else (c["start"] + c["end"]) / 2
        hit = snap([c], t, f.get("expected", ""), within=c["end"] - c["start"] + 4)
        item = {"clip": cid, **{k: str(f.get(k, "")).strip() for k in ("expected", "heard", "severity", "confidence")},
                "audio_time": round(t, 2), "snapped": bool(hit), "sentence": None, "clip_time": None, "qa": False}
        if hit:
            wt, _, i = hit
            words, _, chunks = split_line(manifest[cid]["raw"])
            if len(words) == len(c["words"]):
                item["sentence"] = next((k + 1 for k, (a, b, _) in enumerate(chunks) if a <= i < b), None)
            item["clip_time"] = round(wt - c["start"], 2)
        else:
            item["clip_time"] = round(max(0.0, t - c["start"]), 2)
        flagged = {fl["s"] for fl in reported(manifest[cid].get("qa")) if fl["why"] == "consensus"}
        item["qa"] = item["sentence"] in flagged
        findings.append(item)
    findings.sort(key=lambda x: (order[x["clip"]], x["clip_time"] or 0))

    def line(x):
        where = f"{x['clip']}:{x['sentence']}" if x["sentence"] else x["clip"]
        return (f"{where} \"{x['expected']}\" → \"{x['heard']}\"  ({x['severity']}, conf {x['confidence']})"
                f"{'' if x['snapped'] else ' ≈'}{' +qa' if x['qa'] else ''}  @ {x['clip_time']:.1f} s")
    base = ROOT / "media" / "review" / (f"ch{n}_listen_partial" if args.only else f"ch{n}_listen")
    base.parent.mkdir(parents=True, exist_ok=True)
    base.with_suffix(".json").write_text(json.dumps({
        "chapter": n, "clips": ids, "duration": round(total, 2), "model": args.model,
        "generated": datetime.now().isoformat(timespec="seconds"), "seconds": round(seconds, 1),
        "attempts": r.attempts, "usage": r.usage, "warnings": warnings, "raw": r.data, "findings": findings},
        indent=1, ensure_ascii=False) + "\n")
    lines = {c: sum(x["clip"] == c for x in findings) for c in ids}
    md = [f"# Chapter {n} listen ({args.model})",
          f"{len(ids)} clip(s), {mss(total)} of narration; {seconds:.0f} s, {fmt_usage(r.usage)}. "
          f"{len(findings)} finding(s) in {sum(1 for v in lines.values() if v)} clip(s). Line: clip:sentence "
          "\"script\" → \"heard\" (severity, confidence) @ clip time; ≈ not found in the text, +qa also "
          "flagged by the Whisper QA. Claims: listen before re-voicing.", "",
          *(line(x) for x in findings),
          *([""] + [f"warning: {w}" for w in warnings] if warnings else [])]
    base.with_suffix(".md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
