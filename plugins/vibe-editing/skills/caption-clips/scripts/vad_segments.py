#!/usr/bin/env python3
"""
vad_segments.py — speech/silence detection via Silero VAD (offline, on-device).

Outputs the speech intervals (and the silence gaps between them) so the cut/leadfix
stage can tighten dead air and pauses precisely instead of by fixed thresholds.

    { "duration": float, "speech": [[start,end], ...], "silence": [[start,end], ...] }
Times in seconds.

Usage:
    vad_segments.py <audio_or_video> --out segments.json
        [--min-silence 0.35] [--min-speech 0.10] [--pad 0.05]
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path


def extract_wav(src: str) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", src,
                    "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True)
    return tmp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--min-silence", type=float, default=0.35, help="min silence gap to keep (s)")
    ap.add_argument("--min-speech", type=float, default=0.10, help="min speech chunk to keep (s)")
    ap.add_argument("--pad", type=float, default=0.05, help="pad around speech (s)")
    a = ap.parse_args()

    from silero_vad import load_silero_vad, get_speech_timestamps
    import wave as _wave, numpy as np, torch
    wav = extract_wav(a.source)
    try:
        model = load_silero_vad()
        SR = 16000
        # load the 16k mono PCM wav via stdlib (avoids torchaudio/torchcodec dependency)
        with _wave.open(wav, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        audio = torch.from_numpy(np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0)
        ts = get_speech_timestamps(
            audio, model, sampling_rate=SR, return_seconds=True,
            min_silence_duration_ms=int(a.min_silence * 1000),
            min_speech_duration_ms=int(a.min_speech * 1000),
            speech_pad_ms=int(a.pad * 1000))
        dur = len(audio) / SR
    finally:
        Path(wav).unlink(missing_ok=True)

    speech = [[round(t["start"], 3), round(t["end"], 3)] for t in ts]
    silence, prev = [], 0.0
    for s, e in speech:
        if s - prev > a.min_silence:
            silence.append([round(prev, 3), round(s, 3)])
        prev = e
    if dur - prev > a.min_silence:
        silence.append([round(prev, 3), round(dur, 3)])

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({"duration": round(dur, 3), "speech": speech, "silence": silence}, indent=2))
    print(f"silero-vad: {len(speech)} speech / {len(silence)} silence gaps -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
