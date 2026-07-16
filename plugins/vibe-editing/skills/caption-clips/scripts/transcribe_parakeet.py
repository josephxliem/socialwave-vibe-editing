#!/usr/bin/env python3
"""
transcribe_parakeet.py — OFFLINE word-level transcription via Parakeet MLX (Apple Silicon).

Drop-in alternative to transcribe_lv3.py (Groq). Same output shape:
    { "clip_index": 0, "source_start": float, "source_end": float,
      "words": [ {"word": str, "start": float, "end": float, "prob": float}, ... ] }
Times are CLIP-relative (0-based), matching the Groq backend.

Runs locally on-device (no API key, offline, private). First run downloads the model
(~600MB-2.5GB) to the HF cache; subsequent runs are instant to load.

Usage:
    transcribe_parakeet.py <source> --start 0 --end 60 --out clip.json [--model <hf_id>]
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

DEFAULT_MODEL = "mlx-community/parakeet-tdt-0.6b-v2"


def extract_wav(src: str, start: float, end: float) -> str:
    """16kHz mono wav of [start,end] — what the model wants; times come back 0-based."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", src,
         "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp],
        check=True)
    return tmp


def tokens_to_words(result):
    """Aggregate subword AlignedTokens into words. A new word begins on a token whose
    text starts with whitespace or the SentencePiece boundary marker (▁)."""
    words = []
    for sent in result.sentences:
        cur = None
        for tk in sent.tokens:
            raw = tk.text
            boundary = raw.startswith(" ") or raw.startswith("▁") or cur is None
            piece = raw.replace("▁", " ").strip()
            if boundary and piece:
                if cur:
                    words.append(cur)
                cur = {"word": piece, "start": round(float(tk.start), 3),
                       "end": round(float(tk.end), 3),
                       "prob": round(float(getattr(tk, "confidence", 1.0) or 1.0), 3)}
            elif cur is not None:
                cur["word"] += piece
                cur["end"] = round(float(tk.end), 3)
        if cur:
            words.append(cur)
    return [w for w in words if w["word"]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    a = ap.parse_args()

    if a.end is None:
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", a.source], capture_output=True, text=True).stdout.strip()
        a.end = float(dur)

    from parakeet_mlx import from_pretrained
    wav = extract_wav(a.source, a.start, a.end)
    try:
        model = from_pretrained(a.model)
        result = model.transcribe(wav)
    finally:
        Path(wav).unlink(missing_ok=True)

    words = tokens_to_words(result)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({
        "clip_index": 0, "source_start": a.start, "source_end": a.end,
        "backend": "parakeet-mlx", "words": words,
    }, indent=2))
    preview = " ".join(w["word"] for w in words[:10])
    print(f"parakeet-mlx: {len(words)} words -> {a.out}  | {preview}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
