"""Audition a voice: render a sample paragraph exactly as the real pipeline would.

    vk audition engine/assets/voice/refs/ref_a.wav [more refs ...]

Writes engine/assets/voice/audition_<ref>.wav. Uses tools/voice.py's sentence pacing and
QA, so what you hear is what the video will sound like with that reference.
"""
import sys
from pathlib import Path

import soundfile as sf

import voice

SAMPLE = (
    "Now suppose we want to stick a one on the front. You might expect the computer to shuffle "
    "everything along to make room. It doesn't. It builds one new cell, holding the one, and points "
    "it at the list that was already there. {pause} That's it. One step, no matter how long the list is."
)


def main():
    from faster_whisper import WhisperModel
    from mlx_audio.tts.utils import load_model

    refs = sys.argv[1:] or [str(voice.ENGINE / voice.VOICE["ref"])]
    model = load_model(voice.VOICE["model"])
    whisper = WhisperModel("base", device="cpu", compute_type="int8")
    words, _, chunks = voice.split_line(SAMPLE)
    for ref in refs:
        voice.VOICE["ref"] = str(Path(ref).resolve().relative_to(voice.ENGINE))
        audio, sr = voice.voice_line(model, whisper, "audition", words, chunks)
        out = voice.ENGINE / "assets" / "voice" / f"audition_{Path(ref).stem}.wav"
        sf.write(out, audio, sr)
        print(f"{out.relative_to(voice.ENGINE)}  {len(words) / (len(audio) / sr) * 60:.0f} wpm")


if __name__ == "__main__":
    main()
