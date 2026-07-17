# Vibe Editing — how to run this project

This folder is **Vibe Editing**: a pipeline that turns a long video into finished, captioned,
face-tracked **vertical clips**, in the creator's own brand. It's built to be run by
**non-technical creators** — so when you help someone here, do the work yourself, never make them
run terminal commands or hand-edit files, and explain what's happening in plain English.

## Making clips (the main job)
When the user gives you a video — a YouTube/URL link or a local file — and asks for clips in ANY
plain-English way ("make clips from this", "cut this up", "shorts from this", "/edit <link>"):

1. Read **`plugins/vibe-editing/skills/edit/SKILL.md`** and follow its spine end-to-end.
2. Put source footage in the project's `00_SOURCE/`, scratch in `10_WORK/`, and finished clips in
   **`20_DELIVER/`**. Show the user the delivered clips when you're done.
3. The pipeline mines the strongest moments, hand-cuts, face-tracks to 9:16, captions, mixes music,
   renders, and runs a 6-gate self-audit — a clip that fails a gate doesn't ship.

You do **not** need the `/edit` slash command or any plugin install — run the workflow directly
from the scripts in `plugins/vibe-editing/`. (A `/edit` shortcut is available if the user wants it:
`/plugin marketplace add .` then `/plugin install vibe-editing@vibe-editing-marketplace`.)

## Horizontal "mid" videos (the highlight skill)
If the user wants HORIZONTAL 16:9 "mid" videos for SUBSCRIBER growth from a long recording —
"mine highlights", "make mids", "highlights channel", "post and schedule these" — read
`plugins/vibe-editing/skills/highlight/SKILL.md` and follow it. These are regular 16:9 videos,
NOT 9:16 shorts (shorts = the edit pipeline above). The CTA outro is user-supplied and optional
at `brand/cta/outro.mp4`. POST mode titles + schedules to the user's OWN YouTube via their own
Google sign-in — never any other account.

## First-time setup (only if it isn't set up yet)
If `plugins/vibe-editing/.venv` is missing, or `python3 plugins/vibe-editing/doctor.py` reports
missing tools, set it up first: install only what's missing yourself (ffmpeg, yt-dlp, tesseract,
rclone via Homebrew; a `.venv` with the kit's deps + faster-whisper). A free Groq key in
`plugins/vibe-editing/config/keys.env` makes transcription ~10× faster; without it, it uses free
offline transcription. Full first-run + brand interview: **`ONBOARDING.md`**.

## Brand it / change it
Brand assets live in `brand/` (logos, fonts, music, caption-style, animations). When the user wants
their brand applied, or any change ("captions bigger", "use this logo", "cut tighter", "don't open
on a question"), update the right config and re-run:
- captions → `plugins/vibe-editing/skills/caption-clips/presets/spice.json`
- font → bundled `plugins/vibe-editing/skills/caption-clips/fonts/` (or their own in `brand/fonts/`)
- what makes a clip worth cutting → `plugins/vibe-editing/skills/edit/prompts/clip_select.md`
- music → `brand/music/`

## 🌊 SOCIAL WAVE — BRAND DEFAULTS (apply to every clip unless the user says otherwise)
The brand is **Social Wave**. Full details + rationale live in `brand/brand-profile.md` (source of
truth — read it when editing brand config). Defaults, encoded across the pipeline:

- **Captions:** preset **`spice_socialwave`** (`skills/caption-clips/presets/spice_socialwave.json`).
  White base; the biggest PAYOFF word per line is ALL-CAPS + size-bumped + a **brand accent color,
  ALTERNATING blue↔coral** (blue `#1CB5E5`, coral `#F58A7D`). Director brand note:
  `skills/caption-clips/references/socialwave_caption_note.md`. **Captions always ON. NO emojis.**
- **Clip length:** **30–75s, HARD FLOOR 30s** (never ship under 30s). Overrides the generic 20–45s.
- **Selection / hook:** MINDSET/principle moments over tactics; agency-owner POV. Clip must be
  **self-contained** for a cold viewer; if context is needed, add it as **on-screen TITLE TEXT**, not
  by extending the cut. **Hook = bold claim, always punchy.** End clean / on the punchline.
  (Encoded in `skills/edit/prompts/clip_select.md` → "SOCIAL WAVE — BRAND OVERRIDES".)
- **Pacing:** dynamic — relaxed during a story/point, **punchy on hard statements, hook always tight.**
- **Face-tracking:** required on every clip (already the house default — keep it).
- **Music:** **OFF by default** (captions + clean speech only). To enable later: add tracks to
  `brand/music/` (rights-cleared only) and turn the mix stage's music on.
- **Logo:** current logo = blue "SOCIAL" + coral brush "WAVE"; used on end-cards / as a small
  watermark. **File still PENDING** in `brand/logos/` — stamp it once the user supplies the file.
- **Don't cut mid-sentence** (already a hard gate — keep enforcing `ending_check.py`).

## Rules
- Only use this kit — don't pull tools or keys from anywhere else on the machine.
- Never delete the user's source footage. Re-renders overwrite the delivered clip in place.
- Be patient and plain-spoken; assume they've never used a terminal.

## 🌊 SOCIAL WAVE — THE PROVEN REEL WORKFLOW (team standard, locked 2026-07-17)

The division of labour: **the editor owns TIMING + WORDING + CUTS (in Premiere); Claude owns the LOOK (captions/render).**

1. Editor gives Claude the long-form video (+ optionally a topic). Claude scans the transcript,
   pitches 2-3 reel options (hook / arc / length), editor picks.
2. Claude cuts + renders review MP4s (face-tracked 9:16, brand captions) and QCs them
   frame-by-frame BEFORE the editor sees them (claude-video /watch skill if installed, else
   ffmpeg contact sheets: fps=1 + tile, then READ the sheets and verify every caption).
3. Editor watches the MP4s. Approve → done. Tweaks → step 4.
4. Claude builds Premiere sequences: V1 = assembly cut (trimmable), V2 = exact-look caption
   overlay (ALPHA .mov, scale 50% in a 1080x1920 seq), + an editable caption track (plain SRT).
5. Editor edits in Premiere (cuts on V1, caption text/timing on the caption track), then
   exports the caption sidecar: ⌘M → Captions tab → Create Sidecar File → SubRip (.srt).
6. Claude runs `skills/caption-clips/scripts/rebuild_captions_from_srt.py` — re-applies the
   approved per-word styling onto the editor's words/timings verbatim — re-bakes the overlay,
   and renders the final MP4 FROM THE EDITOR'S TIMELINE geometry (editors may trim cuts, not
   just captions: diff the SRT word-count/duration first; if content changed, the Premiere
   timeline is the source of truth).

### Clip rules (Kan / personal-brand mindset content)
- 30–75s, no mid-sentence cuts, end on a clean punchline.
- End the clip ~0.25s after the last spoken word — verify true speech end with Silero VAD
  (`vad_segments.py`); ASR word-ends often include trailing silence.
- Never clip the video intro / case-study rollup (it serves the video's packaging, not a feed).
- A hook must connect to the viewer's situation, not just sound bold.

### Folder conventions
- Mirror the Dropbox convention locally per video: `<NN> - <Video Title>/` with
  `Footage / Premiere / Exports / Reels Exports / Reels Working / tools`.
- Reel deliverables: `SW <NN> - <full video title> REEL<NN>_Ready.mp4` (revisions ` V2`).
  Continue the video's existing REEL numbering from Dropbox.
- **NEVER write to Dropbox** — the editor drags approved files in themselves.
- `_runs/` is disposable render cache; anything Premiere references lives in the video folder.

### Gotchas (hard-won — do not re-learn these)
- Launch `skills/render/engine.py` with the kit venv's bin PREFIXED to PATH
  (subprocess stages need cv2 etc.).
- Transcription backend order: Groq → Parakeet MLX (offline, Apple Silicon) → AssemblyAI
  (`transcribe_auto.py`). No key needed if using Parakeet.
- The soft two-layer gblur shadow is CORRECT (matches the burned MP4). If overlay captions ever
  look faded/"cut off", it's the ALPHA path (needs `alpha=1` on the text ass filter — already
  fixed), NOT the shadow. QC overlays composited over footage with /watch before delivering.
- Premiere bridge: `export_sequence` can return success with NO file if Media Encoder isn't
  running — verify the file exists; fallback = reproduce the timeline with ffmpeg from clip
  geometry. Caption tracks are invisible to scripting (the SRT sidecar export is the only way
  to read the editor's caption edits).
