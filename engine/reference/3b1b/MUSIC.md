# Music in 3Blue1Brown videos, and how we copy it

Researched 2026-10-20 from evidence: YouTube captions of Grant's own videos, his end-screen
code, the channel FAQ, the composer's liner notes and licence page, and our own measurements
of the album and of `tools/music.py`. No video or audio of his was downloaded. What we can't
know without listening is marked as such. Scripts and raw outputs live in `tools/`
(see "Reproduce" at the end).

## 1. Rules for our pipeline

| Moment | Music? | How (cue in `music/chN.json`) |
|---|---|---|
| Hook + title (first ~45 s) | **Yes, a quiet bed from frame 1, under the voice.** No music-only intro: Grant starts talking at 0.0 s. | `from: "START"`, `until: "<first line of scene 2>"`, `fade_in: 1` (or a track with a soft opening), `fade_out: 4`, so the fade ends exactly as scene 2's first line starts |
| Dense explanation (code, derivations, cost proofs) | **Mostly dry.** At most one more bed per chapter, on a visual/conceptual stretch | e.g. `from: "<last line of previous scene>:end"`, `until: "<first line of next scene>"`, `fade_in: 3`, `fade_out: 3.5` |
| Section/scene transitions | **No stings and no interludes.** 3b1b's music-only gaps mid-video are rare and 0.5–3 s long. Inside a bed, let the duck release so the music rises a little in the gap | nothing extra: the slow duck release does it |
| Recap + "next time" + end card | **Yes, under the recap, then alone over the end card** | `from: "<last line before recap>:end"`, `until: "END"`, `fade_in: 3`, `fade_out: 3` |

Levels (voice is loudnormed to -16 LUFS; `level_db` = track integrated loudness relative to the voice):

- **Beds under narration: `level_db: -12`.** Measured in a real ch1 mix: a median **23–25 dB below
  the voice while it speaks**, about 20–23 dB below in gaps.
- **Recap + end card: `level_db: -11`** (≈ 20 dB under the recap voice, interpolated between measured
  -10 → 19.3 dB and -12 → 21.3 dB; the music-only end card then sits ≈ 14 dB below speech level).
- **Never closer than 20 dB to speech while it is talking** (WCAG 2.2 SC 1.4.7's number for
  speech-over-background, the only formal standard found).
- **Duck:** a gentle, slow sidechain, put in every sheet:
  `"duck": {"threshold": 0.03, "ratio": 2, "attack": 50, "release": 2000}`. Measured: −10 dB under speech,
  −7.5 dB in the 0.55 s sentence breaths (so no pumping), −3 to −4 dB in pauses ≥ 1.2 s.
  **Do not use `tools/music.py`'s current default** (`0.02 / 6 / 20 / 600`). It ducks 19 dB under
  speech but recovers to −4.7 dB in every sentence breath, a ~14 dB pump per sentence (§4).
- Note for the brief's example format: `tools/music.py` has no per-cue `duck_db`. Ducking is one
  sheet-wide `duck` block, and with the parameters above its depth is ≈ −10 dB under speech.

Tracks (measured, not auditioned; listen before the final render):
hook bed **Clarity** (softest opening on the album), mid-chapter bed **Spirals** / **Far Away**
(least energy in the speech band, steadiest), recap + end card **Occlusion** (least speech-band
energy, 20 s natural fade ending). Avoid under speech: the solo piano pieces and other mid-heavy
tracks (§5).

## 2. Findings (with evidence strength)

1. **No music-only intro. Narration starts on the first frame.** The first caption word is at
   0.0–0.1 s in 9/9 recent videos, and 0/9 have a music-only span at the start. *Strong* (caption timing).
2. **Music runs under the narration, in every recent video where the captioner can hear it.**
   YouTube's newer auto-caption model (all videos from Nov 2025 on) writes `[music]` inside
   speech lines when it hears music in a short pause ("down into two bits, [music] and
   turns"). 5/5 such videos have 10–32 of these tags (3.4–6.7 per 10 min), in 34/42 of their
   sections. The older model (≤ Oct 2025) only tags music-only stretches, so it can't tell us
   either way. *Moderate*: an ASR proxy that only sees pauses.
3. **The opening section has music under it.** The first in-speech tag is at 16, 57, 85, 85 and
   190 s, inside the opening section in 4/5 videos. In the fifth, the tag comes 1 s after the cold
   open ends. Tags also appear in the final section in 4/5. *Moderate*.
4. **Beds come and go; they are not wall-to-wall.** Tags are not clustered at section boundaries
   (8–21% of tags within 20 s of a boundary vs. 9–20% of the time there). One video has 64 pauses
   with no tag from 16:25 to 32:19, its two densest math sections (complex exponential and log),
   p ≈ 0.015 if a bed were running all the way through. Two others show no significant gap
   (p ≈ 0.13 and 0.50). *Weak* for "dense explanation goes dry". The test has low power.
5. **No musical interludes between sections.** In 9 videos there are only 4 mid-video
   music-only spans, each 0.5–3 s. One falls exactly on a section boundary (18:37–18:40, as
   "Grover's Algorithm" starts); the others are 27–105 s from one. The old tagger reliably marks
   music-only stretches (it caught 3/4 end screens), so long interludes would have shown up.
   *Strong* for "none longer than ~3 s"; *weak* for "a swell marks transitions".
6. **Music carries the end screen, about 20 s after the last word.** The time from the last spoken
   word to the end of the video has median 18.4 s (IQR 17.4–22.6, n = 9). That matches Grant's
   end-screen code: `PatreonEndScreen.scroll_time = 20` and `SideScrollEndScreen.scroll_time = 21` s
   (`videos/custom/end_screen.py`). Music is tagged over it in 3/4 videos with the old tagger.
   The new tagger tagged 1/5 and emitted nothing at all for the other four tails, which tells us nothing. *Strong* for the timing,
   *moderate* for the music.
7. **Level: clearly below the voice, and nothing more precise is knowable without listening.** The ASR still
   transcribes every word while hearing music in the gaps, so the bed is audible but well under
   the speech. Manual captions never mark music (0/10 tracks). *Weak/indirect*. That's why our
   numbers come from WCAG plus our own measurements (§4).
8. **Track choice can't be determined from public sources.** Descriptions only say "Music by
   Vincent Rubinetti" with album links (32/33; the DL5 transformers video has no music line),
   and none names a track. Of the 34 liner notes, only *Zeta* names
   a video ("originally used in the Riemann zeta function video", 2016) and *Hypothesis* the
   2020 Lockdown Math streams. No signature intro/outro piece is identified. Grant himself wrote the
   piano pieces of the Essence of Linear Algebra and Calculus series (FAQ), presumably the album's
   *Grant's Etude*, *Grant's New Etude* and *Grant's Opus* (Vincent: "The songs Grant's Etude and Opus
   were named by me, not Grant"). Composition dates suggest new pieces arrive with new
   videos (*Machinery* May 2026, *Ongoing* Sep 2026); that's inference only. *Strong* (that the
   question can't be answered).

## 3. Evidence

### 3.1 YouTube captions

Method (`tools/music_captions.py`): 33 of Grant's own long-form explainers (Feb 2022 – Sep 2026;
guest videos, interviews, talks, parodies and SoME round-ups excluded) were listed with yt-dlp
(metadata only: duration, chapters, description). Captions came via `youtube-transcript-api`
1.2.4. A music-only span is a run of snippets that are nothing but a music tag; it ends where
the next spoken snippet starts. An in-speech tag's time is interpolated within its snippet
(about ±1 s).

Coverage, and why it's partial. Captions arrived for 13 videos. YouTube then answered `IpBlocked` for
the other 20 (all 2022 – Nov 2024). Five retries, 5 min apart (13:01–13:22), didn't clear it, and yt-dlp's
subtitle download failed too (an empty file on the web client, "format not available" or nothing on
tv/mweb/ios/android_vr/web_embedded). Of the 13, 3 have only manual
captions, and 1 is a recorded live lecture (applause; excluded). That leaves **9 videos with
auto captions, Mar 2025 – Sep 2026**: the recent style, which is the one we copy.

**Two caption generations.** Every track from Nov 2025 on uses lowercase `[music]` and also tags
`[applause]`, `[laughter]`, `[clears throat]`. Every older one uses `[Music]` and only tags
music-only stretches. The in-speech tags exist only in the first group, so the presence or absence of
in-speech tags is a property of the captioner, not evidence about Grant's mixing before Nov 2025.

| video (upload) | length | tagger | 1st word | music-only spans | end tail after last word | inline `[music]` tags | sections with a tag |
|---|---|---|---|---|---|---|---|
| [The last IMO problem AI could not solv](https://www.youtube.com/watch?v=Nbwv5wHQoj0) (2026-09) | 51:55 | new `[music]` | 0.1 s | 21:59–21:59 (mid), 25:27–25:28 (mid) | 24 s | 32 | 8/9 |
| [But what is cross-entropy? – Compressi](https://www.youtube.com/watch?v=GlYgs6v2YfU) (2026-07) | 33:51 | new `[music]` | 0.1 s | 33:33–33:51 (end) | 18 s | 12 | 7/10 |
| [How (and why) to take a logarithm of a](https://www.youtube.com/watch?v=ldxFjLJ3rVY) (2026-03) | 44:52 | new `[music]` | 0.1 s | none | 25 s | 30 | 7/7 |
| [The most beautiful formula not enough ](https://www.youtube.com/watch?v=fsLh-NYhOoU) (2026-02) (live lecture, excluded) | 60:23 | new `[music]` | 7.8 s | 60:13–60:21 (end) | -1 s | 1 | 1/13 |
| [Why you can't comb a hairy ball](https://www.youtube.com/watch?v=BHdbsHFs2P0) (2026-01) | 29:39 | new `[music]` | 0.0 s | none | 23 s | 10 | 5/8 |
| [Why Laplace transforms are so useful](https://www.youtube.com/watch?v=FE-hM1kRK4Y) (2025-11) | 23:05 | new `[music]` | 0.0 s | 3:00–3:01 (mid) | 17 s | 14 | 7/8 |
| [But what is a Laplace Transform?](https://www.youtube.com/watch?v=j0wJBEZdwLs) (2025-10) | 34:40 | old `[Music]` | 0.1 s | 34:21–34:40 (end) | 18 s | 0 | 0/8 |
| [Where my explanation of Grover's algor](https://www.youtube.com/watch?v=Dlsa9EBKDGI) (2025-05) | 16:23 | old `[Music]` | 0.1 s | 16:06–16:23 (end) | 17 s | 0 | 0/4 |
| [But what is quantum computing? (Grover](https://www.youtube.com/watch?v=RQWpF2Gb-gU) (2025-04) | 36:54 | old `[Music]` | 0.0 s | 18:37–18:40 (mid), 36:48–36:54 (end) | 6 s | 0 | 0/10 |
| [Why colliding blocks compute pi](https://www.youtube.com/watch?v=6dTyOl1fmDo) (2025-03) | 26:07 | old `[Music]` | 0.0 s | none | 20 s | 0 | 0/6 |

Aggregates (9 videos, live lecture excluded):

| statistic | value |
|---|---|
| first spoken word | median 0.1 s (range 0.0–0.1) |
| music-only span at the start | 0/9 |
| music-only span over the end screen | 4/9 (old tagger 3/4, new tagger 1/5) |
| time after the last word | median 18.4 s, IQR 17.4–22.6, range 5.8–25.0 |
| mid-video music-only spans | 4 in 9 videos, 0.5–2.9 s each, at 13%, 42%, 49%, 51% of the video |
| videos with in-speech `[music]` tags | 5/5 new-tagger videos (0/4 old: can't tag) |
| in-speech tags per 10 min | median 6.1 (range 3.4–6.7) |
| sections with ≥ 1 tag | 8/9, 7/10, 7/7, 5/8, 7/8 |
| tags within 20 s of a section boundary vs. share of time there | 12% vs 10%, 8% vs 18%, 10% vs 9%, 20% vs 16%, 21% vs 20% |
| manual caption tracks with any music mark | 0/10 |

Per-video timelines of in-speech tags (mm:ss, section) are printed by
`music_captions.py stats`. The full per-video data is in `tools/caption_stats.json`.

**Continuous or in stretches?** (`music_captions.py pauses`) Pauses are gaps ≥ 0.5 s between
manual caption cues. A pause counts as a hit if an in-speech tag lies within 1.5 s. A bed that
never stops would give hits spread evenly, so a long run without hits is unlikely under it:

| video | pauses | hits | longest run without a tag | p if the bed never stopped |
|---|---|---|---|---|
| Log of an image (ldxFjLJ3rVY) | 174 | 11 | 64 pauses, 16:25–32:19 (complex exp. + complex log) | 0.015 |
| Cross-entropy (GlYgs6v2YfU) | 113 | 4 | 56 pauses, 7:58–26:11 | 0.13 |
| Laplace, useful (FE-hM1kRK4Y) | 79 | 1 | 54 pauses, 6:33–22:39 | 0.50 |

The hit rates are low (1–6%), so this is suggestive at best.

### 3.2 Grant's own code

`reference/3b1b/videos/custom/end_screen.py`: `PatreonEndScreen.scroll_time = 20` and
`SideScrollEndScreen.scroll_time = 21` (the patron-name scroll). Used by the end screens of his
2023–2025 videos (`grep -rn "EndScreen(" videos/_202*`). The music isn't in the code: it's added
in the edit.

### 3.3 Official statements

- 3b1b FAQ, <https://www.3blue1brown.com/faq/>: "Almost all of it was written by Vincent Rubinetti. The
  piano pieces used in the Linear Algebra and Calculus series were written by me." It links the album
  on Bandcamp/Spotify/Apple Music and, for usage, the composer's form.
- Album page, <https://vincerubinetti.bandcamp.com/album/the-music-of-3blue1brown>: released
  2018-02-22, 34 tracks in Volumes I (1–15), II (16–23), III (24–31), IV (32–), "all rights
  reserved"; "You don't need a Bandcamp account to download this music for free"; "Direct
  download: vincentrubinetti.com/audio/3blue1brown/".
- Liner notes (all 34 track pages, scraped from their JSON-LD): dates per track (Zeta 2016-11 …
  Ongoing 2026-09). Video links only for Zeta (Riemann zeta video), One, Two, Zeta (the Minute
  Physics × 3b1b Bell's theorem collaboration), and Hypothesis (Lockdown Math). The 3Blue1Brown
  Experience: "An April fools joke".
- Descriptions of the 33 sample videos: 32 say "Music by Vincent Rubinetti" (or "The music is by …")
  with album links; DL5 (wjZofJX0v4M) has no music line. None names a track.
- No interview, podcast or blog post by Grant or Vincent on *how* the music is placed was found
  (searched: 3b1b podcast, FAQ, About page, Vincent's site, Patreon posts).

### 3.4 Level references

- WCAG 2.2 SC 1.4.7 (AAA), <https://www.w3.org/WAI/WCAG22/Understanding/low-or-no-background-audio.html>:
  for speech-led audio, background sounds should be "at least 20 decibels lower than the foreground
  speech content, with the exception of occasional sounds that last for only one or two seconds".
- Production guides commonly duck music 15–20 dB under speech (e.g.
  <https://sounddesign.irpr.agency/guides/how-to-mix-audio-for-youtube/>). That's practice, not 3b1b data.

## 4. Our measurements: ducking and levels

`tools/duck_test.py`: hook lines (and, separately, ht.3/ht.4/recap) are joined with 1.5 s holds and
loudnormed to -16 LUFS like the stitch step. Music sits at `level_db -14`, and ffmpeg
`sidechaincompress` runs with each parameter set. Values are median gain reduction in dB. Breath = silent
runs of 0.3–0.9 s; pause = runs ≥ 1.2 s, second half.

| duck params (threshold, ratio, attack ms, release ms) | speech | breath | pause |
|---|---|---|---|
| **current default** 0.02, 6, 20, 600 | −19.0 / −18.7 | **−4.7 / −4.8** (pumps ~14 dB per sentence) | 0.0 |
| 0.02, 3, 20, 1500 | −16.5 / −16.1 | −12.0 / −11.6 | −2.4 / −5.5 |
| 0.05, 4, 50, 1500 | −11.6 / −11.2 | −6.5 / −6.1 | 0.0 / −0.5 |
| **recommended** 0.03, 2, 50, 2000 | **−10.2 / −9.9** | **−7.7 / −7.4** | **−2.6 / −3.9** |
| 0.03, 2, 50, 3000 | − / −10.2 | − / −8.6 | − / −6.1 |
| 0.015, 10, 20, 2000 | −25.0 / −24.4 | −20.4 / −19.9 | −10.6 / −13.5 |

(Two voice passages, separated by "/". Same numbers with Occlusion and Wading: the duck depends on the voice, not the track.)

Full-chapter check: the cue sheet in §6 was run through the real `tools/music.py` `build()` (in a
scratch mirror of the project, without creating `music/ch1.json`) on the 480p15 ch1 render. Exact
music and voice stems were rendered from that graph and compared in 400 ms frames:

| cue | `level_db` | music vs. voice while speaking (median, IQR) | in gaps vs. speech |
|---|---|---|---|
| hook, Clarity | −14 | −26.9 dB (−32.1 … −23.0) | — |
| hook, Clarity | **−12** | **−24.9 dB** (−30.1 … −21.0) | −23.0 dB |
| scene 5 bed, Spirals @ 214 s | −16 | −26.8 dB (−29.2 … −23.1) | — |
| scene 5 bed, Spirals @ 214 s | **−12** | **−22.8 dB** (−25.2 … −19.1) | −19.8 dB |
| recap, Occlusion | −12 | −21.3 dB (−25.2 … −19.9) | — |
| recap, Occlusion | −10 | −19.3 dB (−23.2 … −17.9) | −16.8 dB |
| end card (music only), Occlusion | −10 | — | −13.4 dB |

So **under-speech level ≈ `level_db` − 10 to − 13 dB** with the recommended duck. Clarity reads
quieter because its opening builds slowly.

## 5. The album

**Downloaded:** all 34 tracks, from the composer's official direct link
<https://vincentrubinetti.com/audio/3blue1brown/> (linked from the Bandcamp page; no account, email
or payment), into `music/album/` with original filenames
(`Vincent Rubinetti - The Music of 3Blue1Brown - NN Name.ogg`, plus `cover.png` and
`... - background.png`). 211 MB. The format is **Ogg Vorbis, 44.1 kHz stereo, ~192 kbps**, the only format
that link serves. ffmpeg (and so `tools/music.py`) reads it directly. For MP3/FLAC instead:
Bandcamp album page → "Buy Digital Album" → enter 0 (name your price) → download → pick the format.
Bandcamp may ask for an email for a free download.

**Licence, important before publishing.** The composer's usage page
(<https://vincerubinetti.github.io/using-the-music-of-3blue1brown/>, text read from its source)
says buying or downloading the music gives "the right to listen to it for personal enjoyment;
you don't get to use it in any kind of public production". The free download is "for the
benefit of students … and for people who just want to listen to it casually". Using it in
videos/projects goes through that form, and some uses carry a licence fee. Private renders for study
are fine. **Before these lectures are shared or uploaded with this music, fill in the form.**

Measurements (`tools/measure_album.py` → `tools/album_measurements.json`). I/LRA/TP are EBU R128 from
ffmpeg `ebur128`. "Speech-band share" is the fraction of energy in 300–3400 Hz, the band that
masks a voice (lower = safer under narration). Onsets/s is busyness. Centroid is brightness. "First 15 s" is the
level of 3–15 s vs. the track's median short-term loudness (negative = soft opening).
"Build-up" is when it first reaches median − 3 dB. "Fade tail" is how long the ending takes to
die away. librosa tempo estimates were octave-unreliable and are left out (they're in the JSON).

| # | track | length | I (LUFS) | LRA (LU) | TP (dBFS) | speech-band share | onsets/s | centroid (Hz) | first 15 s vs median (dB) | build-up (s) | natural fade tail (s) | steadiest minute starts at (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Zeta | 4:48 | -14.3 | 4.0 | -0.8 | 0.41 | 4.1 | 557 | -3.8 | 5.1 | 3.9 | 165 |
| 2 | Heartbeat | 5:40 | -15.6 | 5.2 | -0.8 | 0.42 | 3.7 | 679 | -1.0 | 3.0 | 7.5 | 39 |
| 3 | Sixes | 5:30 | -14.9 | 3.7 | -0.8 | 0.38 | 3.9 | 557 | -2.5 | 3.0 | 8.5 | 233 |
| 4 | Euler's Clock | 4:28 | -14.7 | 5.4 | -0.7 | 0.35 | 3.4 | 591 | -2.3 | 3.2 | 6.9 | 52 |
| 5 | One, Two, Zeta | 6:57 | -13.3 | 3.9 | -0.5 | 0.26 | 3.7 | 742 | -3.1 | 4.7 | 4.2 | 187 |
| 6 | Grant's Etude | 1:21 | -15.2 | 4.2 | -0.9 | 0.65 | 1.3 | 541 | -0.3 | 3.0 | 5.7 | 13 |
| 7 | Grant's New Etude | 3:27 | -15.1 | 4.9 | -0.9 | 0.56 | 2.4 | 516 | -1.7 | 3.0 | 5.7 | 69 |
| 8 | Grant's Opus | 2:33 | -15.7 | 2.8 | -1.0 | 0.54 | 1.7 | 529 | -0.3 | 3.0 | 9.3 | 60 |
| 9 | The Wallis Ballade | 4:35 | -16.5 | 4.8 | -0.7 | 0.35 | 2.0 | 631 | -0.9 | 3.0 | 11.3 | 26 |
| 10 | Stepwise | 5:31 | -15.7 | 6.4 | -0.8 | 0.47 | 2.9 | 671 | -1.7 | 3.2 | 7.6 | 71 |
| 11 | Quaternions | 4:52 | -14.9 | 6.4 | -0.6 | 0.46 | 3.6 | 485 | 0.5 | 3.0 | 4.0 | 45 |
| 12 | Reflections | 5:41 | -16.1 | 7.6 | -0.7 | 0.39 | 3.1 | 482 | -5.3 | 19.0 | 7.6 | 95 |
| 13 | Resonance | 6:18 | -16.2 | 4.4 | -0.7 | 0.52 | 3.5 | 475 | -0.7 | 3.0 | 6.1 | 134 |
| 14 | Serendipity | 4:42 | -15.2 | 8.5 | -0.6 | 0.28 | 2.0 | 450 | -5.7 | 7.4 | 9.0 | 23 |
| 15 | Trinkets | 2:00 | -14.8 | 4.3 | -0.8 | 0.68 | 4.0 | 426 | -0.7 | 3.0 | 12.8 | 7 |
| 16 | Hypothesis | 1:36 | -15.1 | 3.8 | 0.1 | 0.41 | 3.0 | 483 | -0.0 | 3.0 | 9.9 | 22 |
| 17 | Wading | 5:09 | -16.8 | 8.2 | -0.1 | 0.61 | 2.0 | 479 | 0.9 | 5.5 | 13.4 | 51 |
| 18 | Centroid | 5:47 | -14.6 | 6.9 | 0.0 | 0.39 | 2.8 | 485 | -2.8 | 3.5 | 15.7 | 172 |
| 19 | Spirals | 6:02 | -17.1 | 4.8 | -1.7 | 0.21 | 3.7 | 420 | -0.1 | 3.0 | 9.3 | 214 |
| 20 | Endpoint | 5:31 | -16.2 | 6.3 | -0.0 | 0.49 | 2.7 | 517 | -1.5 | 6.9 | 10.6 | 190 |
| 21 | Fractals | 5:21 | -14.2 | 4.9 | 0.1 | 0.37 | 4.2 | 379 | -1.1 | 3.0 | 9.0 | 110 |
| 22 | Occlusion | 6:05 | -16.0 | 4.6 | 0.1 | 0.17 | 3.7 | 390 | -2.5 | 4.2 | 20.1 | 165 |
| 23 | Fives | 8:53 | -16.6 | 5.5 | -0.0 | 0.37 | 3.2 | 396 | -4.8 | 6.8 | 18.4 | 215 |
| 24 | Transformation | 5:16 | -15.5 | 4.8 | 0.0 | 0.39 | 4.7 | 617 | -2.6 | 3.0 | 6.4 | 42 |
| 25 | Clarity | 5:28 | -16.0 | 8.6 | -0.2 | 0.32 | 3.5 | 698 | -6.1 | 21.9 | 6.0 | 185 |
| 26 | Focal Point | 5:26 | -15.9 | 9.2 | 0.2 | 0.41 | 4.8 | 589 | -4.0 | 10.0 | 16.7 | 237 |
| 27 | Fragments | 6:30 | -15.5 | 8.9 | 0.1 | 0.28 | 4.2 | 563 | -0.0 | 3.0 | 18.6 | 225 |
| 28 | Gnomon | 5:41 | -15.9 | 8.4 | -0.0 | 0.30 | 2.8 | 754 | -0.8 | 3.0 | 6.0 | 204 |
| 29 | Orbit | 5:13 | -15.2 | 8.3 | 0.1 | 0.28 | 3.3 | 620 | -2.7 | 3.0 | 12.4 | 199 |
| 30 | Far Away | 5:45 | -16.1 | 3.5 | -1.7 | 0.20 | 2.5 | 335 | -0.2 | 3.0 | 10.3 | 173 |
| 31 | Quantum Blue | 5:17 | -14.4 | 7.3 | 0.2 | 0.31 | 3.9 | 671 | -3.4 | 3.0 | 14.3 | 163 |
| 32 | Machinery | 6:00 | -16.0 | 7.4 | 0.1 | 0.29 | 5.3 | 650 | -3.9 | 16.2 | 16.7 | 278 |
| 33 | Ongoing | 4:56 | -14.6 | 6.8 | -0.6 | 0.40 | 3.8 | 540 | 1.5 | 3.0 | 17.3 | 27 |
| 34 | The 3Blue1Brown Experience | 2:22 | -9.6 | 3.0 | 0.8 | 0.22 | 2.6 | 2409 | -1.0 | 3.0 | 9.0 | 5 |

The album is evenly mastered (I −14 to −17 LUFS, LRA 3–9 LU; true peaks reach +0.8 dBFS, which is
harmless at −12 dB). `tools/music.py` gains each track to its own integrated loudness anyway.

Suggested tracks per role (from the numbers; **audition before committing**):

| role | first choice | alternatives | why |
|---|---|---|---|
| calm bed over the hook/title (`track_start: 0`) | **25 Clarity** | 14 Serendipity, 32 Machinery, 12 Reflections | softest openings (first 15 s 4–6 dB under their median, 7–22 s build-ups), so they fade in by themselves |
| bed under explanation (start at the steadiest minute) | **19 Spirals** (@214 s), **30 Far Away** (@173 s) | 22 Occlusion (@165 s), 28 Gnomon, 29 Orbit | 17–30% of energy in the speech band (album median 0.38), steady (LRA 3.5–4.8 for the first three) |
| transition swell/sting (use sparingly, 3b1b mostly doesn't) | **33 Ongoing** | 11 Quaternions, 27 Fragments | start at full level (first 15 s ≥ 0 dB vs median); take 4–6 s from `track_start: 0` with a 2–3 s fade, in a gap only |
| recap + end card | **22 Occlusion** | 27 Fragments, 32 Machinery | least speech-band energy (0.17) for the recap; long natural endings (17–20 s) |
| avoid under speech | 6–8 Grant's Etude/New Etude/Opus, 15 Trinkets, 17 Wading, 13 Resonance | — | 52–68% of their energy in the speech band (solo piano/mid-heavy). Fine music-only, e.g. an end card |
| avoid entirely | 34 The 3Blue1Brown Experience; 5 One, Two, Zeta | — | an April-fools joke (−9.6 LUFS, very bright); a mashup with Minute Physics's theme |

Rotate tracks between chapters so each chapter has its own colour, as each 3b1b video does.

## 6. Cue sheet for ch1 (`tools/music.py` format)

Line ids are from `script/ch1_lists.md`. Copy to `music/ch1.json` to switch music on.
The same file is kept as `tools/ch1_cues.example.json`.

```json
{
 "cues": [
  {"track": "music/album/Vincent Rubinetti - The Music of 3Blue1Brown - 25 Clarity.ogg",
   "from": "START", "until": "c1.what.1",
   "track_start": 0, "fade_in": 1, "fade_out": 4, "level_db": -12},
  {"track": "music/album/Vincent Rubinetti - The Music of 3Blue1Brown - 19 Spirals.ogg",
   "from": "c1.build.5:end", "until": "c1.ht.1",
   "track_start": 214, "fade_in": 3, "fade_out": 3.5, "level_db": -12},
  {"track": "music/album/Vincent Rubinetti - The Music of 3Blue1Brown - 22 Occlusion.ogg",
   "from": "c1.ht.4:end", "until": "END",
   "track_start": 0, "fade_in": 3, "fade_out": 3, "level_db": -11}
 ],
 "duck": {"threshold": 0.03, "ratio": 2, "attack": 50, "release": 2000}
}
```

What each cue does, and where it lands in the current 480p15 render (`tools/cue_check.py`, which
uses `music.py`'s own `line_times`/`resolve`):

```
chapter 1 (480p15): 8:31.8 total, last line ends 8:26.0 -> end-card hold 5.8 s
25 Clarity:   0:00.0 -> 0:47.2 (47.2 s)  lines under it: c1.hook.1, c1.hook.2, c1.hook.3
19 Spirals:   5:25.0 -> 6:47.8 (82.7 s)  lines under it: c1.cells.1 … c1.cells.4
22 Occlusion: 8:00.6 -> 8:31.8 (31.2 s)  lines under it: c1.recap.1
```

- **Hook:** starts with the title card. The narration starts at once, as Grant's does. The fade
  ends exactly when `c1.what.1` (scene 2) starts. Scenes 2–4 (syntax, types, tuples vs. arrays,
  cons notation) are code-reading heavy and stay dry.
- **Scene 5 "Inside the computer":** the box-and-pointer reveal and sharing, the chapter's visual
  "aha", gets one bed. It starts in the gap before `c1.cells.1` and has faded out when `c1.ht.1` begins.
- **Recap + end card:** enters in the gap before the recap and carries the 5.8 s end card alone.
  The duck releases there, so the music rises about 6 dB.

Rules that make cues robust (and why):

- Anchor cues to line ids, never seconds (LESSONS.md). Start a bed at `"<previous line>:end"`. End it
  at `"<next section's first line>"` so the fade-out finishes as the next section starts. Our scene
  gaps are only 1.15–1.46 s and line gaps ~0.3 s, so fixed `until_offset`s ran into the next line.
- Fades: `fade_in` 1 s when a track opens softly, 3 s otherwise; `fade_out` 3–4 s. Fades overlap
  the voice, which is fine because the music is ducked under it.
- Our end card is 5.8 s against 3b1b's ~18–20 s (which includes patron credits). If the music should
  "land", hold the end card ~8–10 s. That's a scene decision, not a music one.

Optional `tools/music.py` improvements, if wanted (not made here): change `DUCK_DEFAULT` to the
recommended duck (the current one pumps); add `"end_align": true` (choose `track_start` so the track's
natural ending lands on the cue's end, which Occlusion's 20 s fade tail would suit); allow a per-cue
duck override.

## 7. What we still don't know

- The actual level and fades in Grant's mix. They can only be known by listening. A quick ear
  check of 2–3 recent videos would settle "how loud is the bed" and "does it fade or cut".
- Whether 2022–2024 videos follow the same pattern. Their captions were IP-blocked. Re-run
  `music_captions.py fetch` later (it retries only the missing ones). Their old-style tags would
  still answer the intro, end-screen and interlude questions.
- Which piece plays where. No public mapping exists. Shazam-style identification would need the audio.

## Reproduce

```sh
# throwaway venvs in the scratchpad (not the project's .venv)
uv venv $TMP/ytvenv && uv pip install --python $TMP/ytvenv/bin/python youtube-transcript-api yt-dlp
uv venv -p 3.12 $TMP/audiovenv && uv pip install --python $TMP/audiovenv/bin/python librosa numpy  # 3.13: numba segfault
$TMP/ytvenv/bin/python -I reference/3b1b/tools/music_captions.py fetch  $TMP/captions
$TMP/ytvenv/bin/python -I reference/3b1b/tools/music_captions.py stats  $TMP/captions reference/3b1b/tools/caption_stats.json
$TMP/ytvenv/bin/python -I reference/3b1b/tools/music_captions.py pauses $TMP/captions
$TMP/audiovenv/bin/python -I reference/3b1b/tools/measure_album.py music/album reference/3b1b/tools/album_measurements.json
$TMP/audiovenv/bin/python -I reference/3b1b/tools/duck_test.py "music/album/…22 Occlusion.ogg" $TMP/duck [line ids…]
.venv/bin/python -I reference/3b1b/tools/cue_check.py reference/3b1b/tools/ch1_cues.example.json 1 480p15
```
