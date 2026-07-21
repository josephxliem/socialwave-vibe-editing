# Wrangling + Premiere project setup — stage 3 SOP (v0.3, 20/07/26)

*The videographer/wrangler's job between filming and editor handoff. **Primary source = Joseph's
own wrangling notes** (Apple Notes → Personal Guides → Wrangling) + his interview answers
(20/07/26); secondary = the ~2yr-old "Video Editing Workflow" Loom (Premiere mechanics only).
Where they differ, Joseph's answers win.*

> **WHO:** MUST be done by the videographer or someone who was in-studio for the shoot.
> **BEFORE ANYTHING:** if the script changed during the shoot, update the script document so the
> editor has the real version; add any important editor notes to the ClickUp video project.

## Audio treatment: two passes, not a conflict (resolved 20/07/26)

- **Wrangle (this stage):** apply **minor** audio treatment — **Denoise, Dereverb, Vocal
  Enhancer**. Method is **videographer preference**: the Effects panel or Essential Sound, either
  is fine. Keep it light (recipes in step 5).
- **Edit (`premiere-editor-conventions.md`):** the deeper **Adobe Podcast Enhance** round-trip
  still runs at the edit stage. The two are complementary — wrangle cleans, edit enhances.

## The sequence (merged, notes-primary)

### 1. Drives + folders
- Two drives: **Z Drive** (office server, downstairs) and **Dropbox** (cloud). Insert the video
  SD card at the desktop, open from the SW drive.
- On the **Z Drive**: client folder → **`SW Raw`** → new shoot-day folder, format
  **`01_SHOOTDAY_DATE`** (copy the format of previous folders). This is the raw ingest location.
- Create **Cam A**, **Cam B**, and **Premiere** entries. Copy footage from the SD cards into
  Cam A / Cam B.
- **Camera roles:** **A Cam = the main angle (serves as the master)**; **B Cam = the side
  angle**. There is no separate "master" file kept — A Cam is it.

### 2. Rename footage 🤖
- **Bulk Rename Utility** (Windows) to rename generic camera names in bulk; Mac has native
  multi-select character-replace in Finder.
- **Replace the leading `C` with the client unique identifier**, e.g. `13SP_30_A(RNG number)` —
  keep the camera's own number so the file stays unique + traceable back to the card.

### 3. Create the Premiere project early (Senthan's efficiency tip) 🤖
- Make a **Premiere** folder in the shoot day, create the Premiere project inside it.
- **Do this ASAP** so you can drop footage in and let Premiere generate audio waveforms in the
  background — makes syncing easier and means you're not idle waiting on syncs.
- Import all of Cam A + Cam B into a bin called **Footage** in Premiere.

### 4. Multicam + per-video sequences
- Create the **multi-cam sequence** from Cam A + Cam B (all recordings must be in the one Footage
  bin for this to work). Sync by audio.
- Create **one new sequence per video recorded** (7 videos in the session = 7 named sequences).
- **Applying sound + colour once (optional method — varies by wrangler):** one approach (Edwin's)
  is a sequence called **`EVERYTHING`** holding all recordings — treat audio + grade there, then
  **Cmd/Ctrl+X** into each per-video sequence. This is *a* wrangler's habit, **not the standard**;
  others grade per sequence directly. Either is fine as long as A/B match and each video's
  sequence is correct.

### 5. Audio treatment (minor — light pass only)
Applied in `EVERYTHING` (per notes). **Method is videographer preference: Effects panel OR
Essential Sound.** Keep it light — the deeper Adobe Enhance pass happens at the edit stage.
Two recorded recipes:
- **Generic:** Denoise ~10% (removes AC hum etc.) · Dereverb ~20% (if floor isn't carpeted) ·
  Vocal Enhancer (low tone = male, high tone = female) · check Essential Sound for the enhancer.
- **Senthan's SW-studio guide:** Dereverb 20% · Denoise 5% · Vocal Enhancer low male / high female.
- (Editor-side echo rule still applies downstream: fully mute whoever isn't talking during long
  passages — lives in `premiere-editor-conventions.md`.)

### 6. Colour grade (basic Lumetri — the goal is A/B match, NOT a look)
- **No base LUT / per-client preset.** The grade is simply **matching each camera angle to the
  other** so cuts don't jar. Footage is shot on a neutral profile (same across cams) to make this
  easy — see the content workflows.
- Basic Lumetri panel: **contrast**, **shadows** if needed, **colour temp** (cool/warm white),
  **saturation** ~10-20 for face colour, **highlights + exposure** to brighten. Midtone **colour
  wheel** for neutralising.
- **Curves ONLY in very extreme circumstances** (e.g. skin matches but the wall won't) — not the
  default. Comparison View helps A/B the angles.

### 7. Reframe / straighten (done at the wrangle stage) 🤖
- Straighten wide-angle barrel distortion to a known vertical (roof/door/pole); rotation is
  sensitive (~0.1-0.3°); don't reveal black edges when punching/rotating; copy across same-lens
  episodes.

### 8. ⭐ Relink footage from Z Drive → Dropbox (CRITICAL — missing from the Loom) 🤖
Once all the per-video Premiere projects are made, **relink the footage to the Dropbox folder
instead of the Z Drive**, so the offshore team can access it (they can't reach the office Z Drive):
1. Right-click the Footage bin → **Make Offline** → *Media files remain on disk*.
2. Right-click the Footage bin again → **Link Media** → point it at the **Dropbox** copy.
- **The Dropbox footage is organised by the VIDEO the footage is for, not the shoot date** — the
  shoot-date grouping means nothing to the editor. (Z Drive = raw ingest by shoot day; Dropbox =
  per-video access for the offshore editor.)

### 9. Handoff
- Keep the project tidy — everything in bins (Deliverables / Reel Assets / etc.), nothing loose.
- Update **ClickUp** (status + editor notes). Post file paths for project + footage.
- Brief the editor on any footage/file quirks, on call AND written in ClickUp so they have a
  reference.

## Where the AI pipeline can take over (the prize)

Mechanical + bridge-addressable: rename (2), create project + import + waveform preload (3),
build multicam + per-video sequences (4), reframe preset (7), and the **Z→Dropbox relink** (8,
scriptable via the bridge's `make offline` / `relink`). Grade (6) is A/B cam-matching with no base
LUT — harder to fully preset, but the machine can propose a match and the wrangler verifies. Audio
(5) is a light, preference-driven pass — low-value to automate. A machine that ingests the renamed
shoot-day folder and outputs clean, matched, relinked, per-video projects (organised by video) with
ClickUp paths collapses most of stage 3 — and sits upstream of `rough-cut`, so savings compound.

## All cross-checks RESOLVED (Joseph interview, 20/07/26)
- [x] Audio: both passes — light Denoise/Dereverb/Vocal Enhancer at wrangle (Effects or Essential
      Sound, wrangler's choice); Adobe Enhance at edit.
- [x] Storage: Z Drive `SW Raw` / `01_SHOOTDAY_DATE` for raw ingest; ClickUp statuses are
      **Wrangling Footage → Footage Ready**. Dropbox relink is organised **by video, not shoot date**.
- [x] Reframe/straighten: **wrangle stage**.
- [x] Cameras: **A Cam = main/master, B Cam = side angle** — no separate master file.
- [x] "EVERYTHING sequence" = one wrangler's habit, **not standard** — varies by wrangler.
- [x] Base LUT: **none** — grade is just A/B cam-matching, basic Lumetri, Curves only in extremes.

## Run log
- 20/07/26 — v0.1 from the ~2yr-old Video Editing Workflow Loom.
- 20/07/26 — v0.2 reconciled against Joseph's own Wrangling notes.
- 20/07/26 — v0.3 all cross-checks resolved via Joseph interview (cameras, reframe, EVERYTHING,
  LUT, ClickUp statuses, Dropbox-relink-by-video).
