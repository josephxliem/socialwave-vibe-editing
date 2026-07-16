#!/usr/bin/env python3
"""
transcribe_auto.py — transcription backend selector for the caption pipeline.

Order (first available wins), so behaviour is UNCHANGED while Groq works and it
auto-falls-back the day the Groq key expires:
    1. Groq (transcribe_lv3.py)      — needs GROQ_API_KEY        [primary]
    2. Parakeet MLX (transcribe_parakeet.py) — offline, on-device [no key]
    3. AssemblyAI (transcribe_assemblyai.py) — needs ASSEMBLYAI_API_KEY

Override with --backend groq|parakeet|assemblyai or env VIBE_STT_BACKEND.
Same CLI + output shape as transcribe_lv3.py single-clip mode:
    transcribe_auto.py <source> --start S --end E --out clip.json
"""
import argparse, os, sys, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEYS_ENV = HERE.parents[2] / "config" / "keys.env"


def _key(name: str) -> bool:
    if os.environ.get(name):
        return True
    if KEYS_ENV.exists():
        for ln in KEYS_ENV.read_text().splitlines():
            if ln.strip().startswith(f"{name}=") and ln.strip() != f"{name}=":
                return True
    return False


def _parakeet_ok() -> bool:
    try:
        import parakeet_mlx  # noqa: F401
        return True
    except Exception:
        return False


def pick_backend() -> str:
    forced = os.environ.get("VIBE_STT_BACKEND")
    if forced:
        return forced.lower()
    if _key("GROQ_API_KEY"):
        return "groq"
    if _parakeet_ok():
        return "parakeet"
    if _key("ASSEMBLYAI_API_KEY"):
        return "assemblyai"
    return "groq"  # will error clearly on missing key


SCRIPTS = {
    "groq": "transcribe_lv3.py",
    "parakeet": "transcribe_parakeet.py",
    "assemblyai": "transcribe_assemblyai.py",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--backend", default=None, help="force groq|parakeet|assemblyai")
    a, extra = ap.parse_known_args()

    backend = (a.backend or pick_backend()).lower()
    script = SCRIPTS.get(backend)
    if not script:
        print(f"unknown backend '{backend}'", file=sys.stderr); return 2

    cmd = [sys.executable, str(HERE / script), a.source, "--out", str(a.out),
           "--start", str(a.start)]
    if a.end is not None:
        cmd += ["--end", str(a.end)]
    cmd += extra
    print(f"[transcribe_auto] backend={backend}")
    r = subprocess.run(cmd)
    # graceful fallback: if the primary failed and it was groq, try parakeet offline
    if r.returncode != 0 and backend == "groq" and _parakeet_ok():
        print("[transcribe_auto] groq failed → falling back to parakeet (offline)")
        cmd[1] = str(HERE / SCRIPTS["parakeet"])
        r = subprocess.run(cmd)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
