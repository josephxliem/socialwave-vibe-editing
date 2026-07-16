#!/usr/bin/env python3
"""
transcribe_assemblyai.py — cloud word-level transcription via AssemblyAI.

Drop-in alternative to transcribe_lv3.py (Groq). Same output shape:
    { "clip_index": 0, "source_start": float, "source_end": float,
      "words": [ {"word": str, "start": float, "end": float, "prob": float}, ... ] }
Times are CLIP-relative (0-based).

Needs ASSEMBLYAI_API_KEY (in config/keys.env or the environment). Get one at
https://www.assemblyai.com — then add `ASSEMBLYAI_API_KEY=...` to keys.env.

Usage:
    transcribe_assemblyai.py <source> --start 0 --end 60 --out clip.json
"""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

KEYS_ENV = Path(__file__).resolve().parents[3] / "config" / "keys.env"


def load_key() -> str | None:
    if os.environ.get("ASSEMBLYAI_API_KEY"):
        return os.environ["ASSEMBLYAI_API_KEY"]
    if KEYS_ENV.exists():
        for ln in KEYS_ENV.read_text().splitlines():
            ln = ln.strip()
            if ln.startswith("ASSEMBLYAI_API_KEY=") and "=" in ln:
                return ln.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def extract_wav(src: str, start: float, end: float) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", src,
                    "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True)
    return tmp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    key = load_key()
    if not key:
        print("ERROR: ASSEMBLYAI_API_KEY not set (config/keys.env or env). "
              "Add it to use this backend.", file=sys.stderr)
        return 2

    if a.end is None:
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", a.source], capture_output=True, text=True).stdout.strip()
        a.end = float(dur)

    import assemblyai as aai
    aai.settings.api_key = key
    wav = extract_wav(a.source, a.start, a.end)
    try:
        cfg = aai.TranscriptionConfig(punctuate=True, format_text=True)
        tr = aai.Transcriber().transcribe(wav, cfg)
    finally:
        Path(wav).unlink(missing_ok=True)

    if tr.status == aai.TranscriptStatus.error:
        print(f"ERROR: AssemblyAI: {tr.error}", file=sys.stderr)
        return 1

    words = [{"word": w.text, "start": round(w.start / 1000.0, 3),
              "end": round(w.end / 1000.0, 3),
              "prob": round(getattr(w, "confidence", 1.0) or 1.0, 3)}
             for w in (tr.words or [])]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({
        "clip_index": 0, "source_start": a.start, "source_end": a.end,
        "backend": "assemblyai", "words": words,
    }, indent=2))
    print(f"assemblyai: {len(words)} words -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
