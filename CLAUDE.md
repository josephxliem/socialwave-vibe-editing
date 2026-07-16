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
