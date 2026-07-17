# Social Wave — AI Reel Editing Setup (Vibe Editing kit)

Welcome! This guide sets up the Social Wave AI editing workflow on your Mac. **You don't do any
of this by hand** — Claude (reading this right now) does the installing, checking, and testing
for you. Budget ~20–30 minutes, mostly waiting on downloads.

## What you're getting

A proven pipeline where you give Claude a long-form client video and get back finished
9:16 reels: face-tracked crop, brand-styled captions (the per-word colour "spice" look),
delivered as MP4s for review and as editable Premiere sequences for fine-tuning. The
caption round-trip means you edit text/timing in Premiere and Claude re-bakes the exact
styled look on your edits.

## Instructions for Claude

You are setting up a NON-TECHNICAL video editor. Do everything for them — never make them run
terminal commands or edit files. Explain in plain English, keep a visible to-do list, and ask
ONE question at a time when you need input.

### Step 1 — Prerequisites check
- Confirm this is an Apple Silicon Mac (`uname -m` → arm64). The offline transcriber needs it.
- Confirm Adobe Premiere Pro is installed (they're an editor — it should be).
- Install Homebrew if missing, then: `ffmpeg`, `yt-dlp`, `uv`, `gh` (optional).

### Step 2 — Get the kit
- The user needs access to the private repo `josephxliem/socialwave-vibe-editing`.
  If `git clone https://github.com/josephxliem/socialwave-vibe-editing.git ~/Documents/vibe-editing`
  fails with auth/404, have them ask Joseph to add their GitHub account as a collaborator
  (repo → Settings → Collaborators), then authenticate with `gh auth login --web` (they approve
  in their browser — never handle their password yourself).

### Step 3 — Python environment
- In `~/Documents/vibe-editing/plugins/vibe-editing/`: create the venv with
  `uv venv --python 3.12 .venv` (Homebrew Python 3.14 has a broken pyexpat — use uv's 3.12).
- Install deps: `uv pip install --python .venv/bin/python -r <repo root>/requirements.txt`
  (on Apple Silicon, also add `parakeet-mlx` for offline transcription — it's commented in the
  file because the install fails on Windows/Linux).
- Run the kit's doctor script if present and fix anything it flags until READY.
- Smoke-test: reframe a few seconds of any 16:9 video via
  `skills/horizontal-to-vertical/scripts/qa_reframe_v2.py` (run with the venv's bin prefixed to
  PATH), and transcribe 5s with `skills/caption-clips/scripts/transcribe_parakeet.py`
  (first run downloads ~600MB model — that's normal).

### Step 4 — Transcription key (optional but recommended)
- Groq is the fastest transcriber. Have the user create their OWN free key at
  https://console.groq.com (never share keys between team members). Save it to
  `plugins/vibe-editing/config/keys.env` as `GROQ_API_KEY=...`, `chmod 600` it, and verify
  it's gitignored. No key? Fine — the pipeline auto-falls-back to Parakeet MLX (offline).

### Step 5 — Premiere Pro MCP bridge
- Install from https://github.com/leancoderkavy/premiere-pro-mcp (follow its README: the CEP
  plugin + MCP server). Add it to Claude Code's MCP config. Verify with the `ping` tool —
  it should report the Premiere version with Premiere open.

### Step 5b — QC skill (claude-video /watch)
- Clone `https://github.com/bradautomates/claude-video` next to the kit (e.g. `~/Documents/claude-video`).
  Its `/watch` skill extracts frames from renders so you can QC captions/cuts frame-by-frame.
  If it's unavailable, QC with ffmpeg contact sheets instead: extract 1 frame/sec and tile them
  (`ffmpeg -i reel.mp4 -vf "fps=1,scale=270:480,tile=8x8" sheet.jpg`), then READ the sheets and
  verify every caption is correct and fully visible BEFORE showing the user anything.

### Step 6 — Read the playbook
- Read `~/Documents/vibe-editing/CLAUDE.md` fully — especially
  "THE PROVEN REEL WORKFLOW", the clip rules, folder conventions, and the Gotchas section.
  These are hard-won; follow them exactly. Key rules to internalize:
  - The editor owns timing/wording/cuts (in Premiere); Claude owns the look (captions/render).
  - QC every render frame-by-frame BEFORE the editor sees it.
  - NEVER write to the team Dropbox — editors drag approved files in themselves.
  - Reel naming: `SW <NN> - <full video title> REEL<NN>_Ready.mp4`.

### Step 7 — Test reel
- Ask the user for any client long-form video (or a YouTube link — yt-dlp can fetch it).
- Run the full workflow once: pitch 2–3 reel options → they pick one → cut, reframe, caption,
  QC with contact sheets → deliver the MP4 to their Downloads.
- Then build the Premiere sequences (V1 cut + V2 exact-look overlay + editable caption track)
  and walk them through one caption-edit round-trip (edit → ⌘M sidecar SRT export → rebuild).

### Step 8 — Client brand setup (when working on a non-Kan client)
- The Social Wave / Kan caption preset is `presets/spice_socialwave.json`. For a NEW client,
  run the brand interview (one question at a time): brand name, logo, caption font + look
  (ask for reference screenshots), music yes/no, topics, hook/ending style, editing
  preferences. Create a new `spice_<client>.json` preset from the socialwave one and iterate
  on a test clip until they love it.

## 🪟 Windows differences (read this if the user is on Windows)

The kit has been patched for Windows (subprocess calls use `sys.executable`, ffmpeg filter
paths use forward slashes, temp dirs are platform-aware) but has NOT yet been battle-tested
there — expect to fix a quirk or two on the first reel, and **commit those fixes back as a PR**
so Windows becomes proven for the whole team.

- **Step 1**: skip the Apple Silicon check. Install with `winget install Gyan.FFmpeg yt-dlp.yt-dlp astral-sh.uv Git.Git GitHub.cli` (or choco equivalents). A machine with an NVIDIA GPU is nice but not required — the kit falls back to software x264 encoding automatically (renders are slower; fine).
- **Step 3**: the venv's python lives at `.venv\Scripts\python.exe` (not `.venv/bin/python`).
  **Do NOT install `parakeet-mlx`** — it's Apple-Silicon-only and the pip install will fail.
  Install the rest: `faster-whisper silero-vad mediapipe assemblyai "numba>=0.61" "llvmlite>=0.44" "numpy<2.3"`.
- **Step 4 is REQUIRED, not optional**: without Parakeet, a **Groq API key is the primary
  transcriber** (free at console.groq.com). `faster-whisper` remains the offline fallback.
- **Step 5**: Premiere Pro and the CEP-based MCP bridge both run on Windows, but the bridge
  is unverified there — test `ping` early, and if it misbehaves report exactly what happened.
- Long-path issues: if git clone or renders fail with path errors, enable Windows long paths
  (`git config --global core.longpaths true` and the LongPathsEnabled registry setting).

## When something breaks
Check the Gotchas section of CLAUDE.md first — the answer is probably there. Still stuck?
Ask Joseph. Improvements welcome: commit fixes on a branch and open a PR on the repo so the
whole team benefits.
