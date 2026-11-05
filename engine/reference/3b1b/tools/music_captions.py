"""Measure where 3Blue1Brown videos have music-only stretches, from YouTube captions.

No video or audio is downloaded: only caption tracks (youtube-transcript-api) and
metadata (yt-dlp, skip_download) such as duration, chapters and description.

    python -I music_captions.py fetch  DATA_DIR            # captions + metadata -> DATA_DIR/<id>.json
    python -I music_captions.py stats  DATA_DIR [OUT.json] # per-video spans + aggregate stats
    python -I music_captions.py pauses DATA_DIR            # continuous bed or stretches?

Caveat built into the method: YouTube's auto-generated (ASR) captions insert "[Music]"
only where music is audible and nobody is speaking. Music *under* narration is not
marked, so these numbers measure music-only stretches (intros, swells between sections,
outros), not the full extent of the score. Manual captions are checked separately for
any music marks (they usually have none).

Needs: youtube-transcript-api>=1.2, yt-dlp (in a throwaway venv).
"""
import json
import re
import statistics as st
import sys
import time
from pathlib import Path

# Grant's own long-form explainers, newest first (guest videos, interviews, live talks,
# parodies and SoME result round-ups excluded; they follow other formats).
VIDEOS = {
    "Nbwv5wHQoj0": "The last IMO problem AI could not solve",
    "GlYgs6v2YfU": "But what is cross-entropy? | Compression is Intelligence 2",
    "l6DKRf-fAAM": "Reinventing Entropy | Compression is Intelligence 1",
    "ldxFjLJ3rVY": "How (and why) to take a logarithm of an image",
    "fsLh-NYhOoU": "The most beautiful formula not enough people understand",
    "BHdbsHFs2P0": "Why you can't comb a hairy ball",
    "FE-hM1kRK4Y": "Why Laplace transforms are so useful",
    "j0wJBEZdwLs": "But what is a Laplace Transform?",
    "-j8PzkZ70Lg": "The Physics of Euler's Formula",
    "Dlsa9EBKDGI": "Where my explanation of Grover's algorithm failed",
    "RQWpF2Gb-gU": "But what is quantum computing? (Grover)",
    "6dTyOl1fmDo": "Why colliding blocks compute pi",
    "IQqtsm-bBRU": "This open problem taught me what topology is",
    "LPZh9BOjkQs": "Large Language Models explained briefly",
    "piJkuavhV50": "Solving problems by adding a dimension",
    "EmKQsSDlaa4": "How are holograms possible?",
    "9-Jl0dxWQs8": "How might LLMs store facts | DL7",
    "eMlx5fFNoYc": "Attention in transformers | DL6",
    "wjZofJX0v4M": "Transformers, the tech behind LLMs | DL5",
    "Cz4Q4QOuoo8": "Answering viewer questions about refraction",
    "KTzGBJPuJwM": "But why would light slow down?",
    "aXRTczANuIs": "How wiggling charges give rise to light",
    "QCX62YJCmGk": "The barber pole effect",
    "d_qvLDhkg00": "Gaussian + Gaussian = Gaussian",
    "YtkIWDE36qU": "Moser's circle problem",
    "IaSGqQa5O-M": "Convolutions | Why X+Y in probability is a beautiful mess",
    "cy8r7WSuT1I": "Why pi is in the normal distribution",
    "zeJD6dqJ5lo": "But what is the Central Limit Theorem?",
    "KuXjwB4LzSA": "But what is a convolution?",
    "851U557j6HE": "Borwein integrals",
    "VYQVlVoWoPY": "How to lie using visual proofs",
    "bOXCLR3Wric": "Olympiad level counting (generating functions)",
    "v68zYyaEmEA": "Solving Wordle using information theory",
}

MUSIC_RE = re.compile(r"\[\s*music\s*\]|♪|\(\s*music\s*\)|\[\s*upbeat music\s*\]", re.I)
NONSPEECH_RE = re.compile(r"^\s*(\[[^\]]*\]|♪+|\([^)]*\))\s*$")


def fetch(data_dir: Path) -> None:
    from youtube_transcript_api import YouTubeTranscriptApi
    import yt_dlp

    data_dir.mkdir(parents=True, exist_ok=True)
    api = YouTubeTranscriptApi()
    ydl = yt_dlp.YoutubeDL({"skip_download": True, "quiet": True, "no_warnings": True})
    blocked = 0
    for vid, title in VIDEOS.items():
        out = data_dir / f"{vid}.json"
        rec = json.loads(out.read_text()) if out.exists() else {"id": vid, "title": title}
        if out.exists() and "caption_error" not in rec:
            continue  # done; records with a caption error are retried (YouTube IP blocks are temporary)
        rec.pop("caption_error", None)
        if "duration" not in rec:
            try:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
                rec["duration"] = info.get("duration")
                rec["upload_date"] = info.get("upload_date")
                rec["chapters"] = info.get("chapters") or []
                rec["description"] = info.get("description") or ""
            except Exception as e:  # metadata is optional
                rec["meta_error"] = repr(e)
        try:
            tl = api.list(vid)
            for t in tl:
                if not t.language_code.startswith("en"):
                    continue
                key = "auto" if t.is_generated else "manual"
                if key in rec:
                    continue
                rec[key] = t.fetch().to_raw_data()
        except Exception as e:
            rec["caption_error"] = repr(e)
        out.write_text(json.dumps(rec))
        print(vid, "auto" in rec, "manual" in rec, len(rec.get("chapters", [])),
              rec.get("caption_error", ""), flush=True)
        if "IpBlocked" in rec.get("caption_error", ""):
            blocked += 1
            if blocked >= 2:  # still blocked: stop hammering, try again later
                print("still IP-blocked; stopping this pass", flush=True)
                return
        time.sleep(4)


LIVE_TALKS = {"fsLh-NYhOoU"}  # recorded live lecture (applause, no end-screen format): shown, not aggregated


def eff_end(snips, i):
    """Auto-caption snippets overlap; a snippet's words end roughly where the next one starts."""
    s = snips[i]
    nxt = snips[i + 1]["start"] if i + 1 < len(snips) else None
    return nxt if (nxt is not None and nxt > s["start"]) else s["start"] + min(s["duration"], 4.0)


def is_nonspeech(text):
    return bool(NONSPEECH_RE.match(text)) or not text.strip()


def spans_from(snips, duration):
    """Music-only spans [start, end): consecutive snippets that are nothing but a music tag.
    A span ends where the next snippet containing speech starts."""
    spans, cur = [], None
    for i, s in enumerate(snips):
        if MUSIC_RE.search(s["text"]) and is_nonspeech(s["text"]):
            cur = [s["start"], eff_end(snips, i)] if cur is None else [cur[0], eff_end(snips, i)]
        elif cur is not None and not is_nonspeech(s["text"]):
            cur[1] = s["start"]
            spans.append(cur)
            cur = None
    if cur is not None:
        spans.append([cur[0], max(cur[1], duration or cur[1])])
    return [(round(a, 1), round(b, 1)) for a, b in spans]


def inline_marks(snips):
    """Times of music tags *inside* speech snippets ("two bits, [music] and turns"): the ASR
    heard music in a short pause between words, i.e. a bed running under the narration.
    Time is interpolated by character position within the snippet (about +-1 s)."""
    out = []
    for i, s in enumerate(snips):
        if is_nonspeech(s["text"]):
            continue
        for m in MUSIC_RE.finditer(s["text"]):
            frac = m.start() / max(len(s["text"]), 1)
            out.append(round(s["start"] + frac * (eff_end(snips, i) - s["start"]), 1))
    return out


def speech_bounds(snips):
    idx = [i for i, s in enumerate(snips) if not is_nonspeech(s["text"])]
    if not idx:
        return None, None
    return snips[idx[0]]["start"], eff_end(snips, idx[-1])


def chapter_of(t, chapters):
    cur = None
    for c in chapters:
        if c["start_time"] <= t:
            cur = c
    return cur


def analyse(rec):
    dur = rec.get("duration") or 0
    auto = rec.get("auto") or []
    manual = rec.get("manual") or []
    chapters = rec.get("chapters", [])
    bounds = [c["start_time"] for c in chapters[1:]]  # internal section boundaries
    first_speech, last_speech = speech_bounds(auto)
    out = {
        "id": rec["id"], "title": rec["title"], "duration": dur, "upload_date": rec.get("upload_date"),
        "live_talk": rec["id"] in LIVE_TALKS,
        "has_auto": bool(auto), "has_manual": bool(manual),
        "manual_music_marks": sum(bool(MUSIC_RE.search(s["text"])) for s in manual),
        "first_speech": first_speech, "last_speech": last_speech,
        "n_chapters": len(chapters), "spans": [], "inline": [],
    }
    for a, b in spans_from(auto, dur):
        role = "start" if a < 5 else ("end" if b >= dur - 3 else "mid")
        out["spans"].append({
            "start": a, "end": b, "len": round(b - a, 1), "pos": round(a / dur, 3) if dur else None,
            "role": role,
            "dist_to_boundary": round(min((min(abs(a - c), abs(b - c)) for c in bounds), default=1e9), 1),
        })
    for t in inline_marks(auto):
        ch = chapter_of(t, chapters)
        out["inline"].append({
            "t": t, "pos": round(t / dur, 3) if dur else None,
            "chapter": ch["title"] if ch else None,
            "dist_to_boundary": round(min((abs(t - c) for c in bounds), default=1e9), 1),
        })
    out["music_at_start"] = any(s["role"] == "start" for s in out["spans"])
    out["music_at_end"] = any(s["role"] == "end" for s in out["spans"])
    out["end_span_len"] = next((s["len"] for s in out["spans"] if s["role"] == "end"), None)
    out["tail_after_speech"] = round(dur - last_speech, 1) if (dur and last_speech) else None
    out["inline_in_first_60s"] = sum(m["t"] < 60 for m in out["inline"])
    out["chapters_with_inline"] = len({m["chapter"] for m in out["inline"]})
    return out


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def stats(data_dir: Path, out_path: Path | None) -> None:
    rows = [analyse(json.loads(p.read_text())) for p in sorted(data_dir.glob("*.json"))]
    rows.sort(key=lambda r: r.get("upload_date") or "", reverse=True)
    have = [r for r in rows if r["has_auto"] and not r["live_talk"]]

    def fmt(x, nd=1):
        return "-" if x is None else f"{x:.{nd}f}"

    print(f"{'id':12} {'date':8} {'dur':>5} {'1st sp':>6} {'st':>2} {'end':>5} {'tail':>5} {'#inl':>4} {'<60s':>4} "
          f"{'ch w/':>5}  music-only spans (start-end s, role)")
    for r in rows:
        sp = " ".join(f"{s['start']:.0f}-{s['end']:.0f}{s['role'][0]}" for s in r["spans"])
        print(f"{r['id']:12} {r.get('upload_date') or '':8} {r['duration']:>5} {fmt(r['first_speech']):>6} "
              f"{'Y' if r['music_at_start'] else '.':>2} {fmt(r['end_span_len']):>5} {fmt(r['tail_after_speech']):>5} "
              f"{len(r['inline']):>4} {r['inline_in_first_60s']:>4} "
              f"{str(r['chapters_with_inline']) + '/' + str(r['n_chapters']):>5}  {sp}"
              f"{'  [live talk]' if r['live_talk'] else ''}{'' if r['has_auto'] else '  [no auto captions]'}"
              f"{'  man-marks=' + str(r['manual_music_marks']) if r['manual_music_marks'] else ''}")

    def summ(xs):
        xs = [x for x in xs if x is not None]
        if not xs:
            return "n=0"
        q = st.quantiles(xs, n=4, method="inclusive") if len(xs) > 1 else [xs[0]] * 3
        return f"n={len(xs)} median={st.median(xs):.1f} IQR={q[0]:.1f}-{q[2]:.1f} min={min(xs):.1f} max={max(xs):.1f}"

    n = len(have)
    beds = [r for r in have if len(r["inline"]) >= 5]
    agg = {
        "videos_fetched": len(rows),
        "videos_with_auto_captions_used": n,
        "videos_with_manual_captions": sum(r["has_manual"] for r in rows),
        "manual_tracks_with_any_music_mark": sum(r["manual_music_marks"] > 0 for r in rows),
        "music_only_at_start": f"{sum(r['music_at_start'] for r in have)}/{n}",
        "music_only_at_end": f"{sum(r['music_at_end'] for r in have)}/{n}",
        "any_inline_marks": f"{sum(bool(r['inline']) for r in have)}/{n}",
        "inline_marks_>=5 (bed under narration)": f"{len(beds)}/{n}",
        "inline_in_first_60s (of bed videos)": f"{sum(r['inline_in_first_60s'] > 0 for r in beds)}/{len(beds)}",
    }
    print("\n" + json.dumps(agg, indent=1))
    print("first speech time:          ", summ([r["first_speech"] for r in have]))
    print("music-only end span length: ", summ([r["end_span_len"] for r in have]))
    print("tail after last speech:     ", summ([r["tail_after_speech"] for r in have]))
    mids = [s for r in have for s in r["spans"] if s["role"] == "mid"]
    print("mid music-only spans:       ", len(mids), [f"{s['start']:.0f}+{s['len']:.0f}s@{s['pos']:.2f}" for s in mids])
    print("inline marks / 10 min (bed videos):", summ([10 * 60 * len(r["inline"]) / r["duration"] for r in beds]))
    print("chapters with >=1 inline mark (bed videos):",
          [f"{r['chapters_with_inline']}/{r['n_chapters']}" for r in beds])
    # do marks cluster at section boundaries? compare with the share of time near a boundary
    W = 20
    for r in beds:
        rec = json.loads((data_dir / f"{r['id']}.json").read_text())
        bnd = [c["start_time"] for c in rec.get("chapters", [])[1:]]
        near_time = sum(min(W, c) + min(W, r["duration"] - c) for c in bnd) / r["duration"] if bnd else 0
        near_marks = sum(m["dist_to_boundary"] <= W for m in r["inline"]) / len(r["inline"])
        r["share_marks_within_20s_of_boundary"] = round(near_marks, 2)
        r["share_time_within_20s_of_boundary"] = round(near_time, 2)
    print(f"marks within {W}s of a chapter boundary vs share of time there:",
          [(r["id"], r["share_marks_within_20s_of_boundary"], r["share_time_within_20s_of_boundary"]) for r in beds])
    print("\nTimelines of inline music marks (mm:ss, chapter):")
    for r in beds:
        print(f" {r['id']} ({mmss(r['duration'])}):",
              "; ".join(f"{mmss(m['t'])} {(m['chapter'] or '')[:22]}" for m in r["inline"]))
    if out_path:
        out_path.write_text(json.dumps({"aggregate": agg, "videos": rows}, indent=1))


def pauses(data_dir: Path, min_pause=0.5, tol=1.5) -> None:
    """Is the bed continuous or in stretches? Pauses come from the manual captions (gaps
    between cues >= min_pause s); a pause is a 'hit' if the new ASR tagged music within
    tol s of it. Under a continuous bed hits would be spread evenly, so a long run of
    pauses without a hit (p = (1 - rate)^run) points at a stretch without music."""
    for p in sorted(data_dir.glob("*.json")):
        rec = json.loads(p.read_text())
        auto, man = rec.get("auto") or [], rec.get("manual") or []
        marks = inline_marks(auto)
        if not man or len(marks) < 5:
            continue
        chapters = rec.get("chapters", [])
        ps = [man[i]["start"] + man[i]["duration"] for i in range(len(man) - 1)
              if man[i + 1]["start"] - (man[i]["start"] + man[i]["duration"]) >= min_pause]
        hits = [any(abs(m - t) <= tol for m in marks) for t in ps]
        rate = sum(hits) / len(hits)
        print(f"\n{rec['id']} {rec['title'][:50]}: {len(ps)} pauses >= {min_pause}s, "
              f"{sum(hits)} with a music tag nearby (rate {rate:.2f})")
        for i, c in enumerate(chapters):
            a = c["start_time"]
            b = chapters[i + 1]["start_time"] if i + 1 < len(chapters) else rec["duration"]
            sel = [h for t, h in zip(ps, hits) if a <= t < b]
            print(f"   {mmss(a):>6}-{mmss(b):<6} {c['title'][:34]:34} pauses {len(sel):3}  hits {sum(sel):2}")
        run, best, best_at = 0, 0, None
        for t, h in zip(ps, hits):
            run = 0 if h else run + 1
            if run > best:
                best, best_at = run, t
        start = ps[ps.index(best_at) - best + 1] if best_at is not None else None
        print(f"   longest run without a tag: {best} pauses ({mmss(start)}-{mmss(best_at)}), "
              f"p under a uniform bed = {(1 - rate) ** best:.4f}")


if __name__ == "__main__":
    cmd, d = sys.argv[1], Path(sys.argv[2])
    if cmd == "fetch":
        fetch(d)
    elif cmd == "pauses":
        pauses(d)
    else:
        stats(d, Path(sys.argv[3]) if len(sys.argv) > 3 else None)
