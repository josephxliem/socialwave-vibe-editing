# Course Video Editing Workflow — SOP (v0.1, 20/07/26)

*Editing workflow for **course/educational module videos** (distinct content type). Source:
Harvey's SOP doc, written on a Moore Finance Group course build. ~3 hours per pillar video
(excluding revisions). Green = lead tasks, Blue = editor tasks in the original. Introduces a new
tool — **Hera** (AI graphics generation).*

> **How it differs from the other content types:** scripted explainers + unscripted are for
> YouTube/social; **course videos are course modules** — heavier on structured graphics (chapter
> pages, lower thirds, half-screen lists), minimalist/subtle animation, "high-end professional,
> minimum effort." Same engine underneath (assembly cut, audio levels, transcript-driven).

## Phase 1 — Assembly & rough cut  (~20-30 min per 10-min video) 🤖
- Arrange all footage + directories into a logical sequence; folder hierarchy set before editing.
- **Back up the sequence before any cutting.**
- **Silence/pause removal via Premiere's native pause-detection tool**; remove pauses + bad takes;
  refine pacing. (= our micro-cut stage.)
- **Normalise voice to -6 to -12 dB** (same house level as reels/long-form).
- Frame to pillar-format standards.

## Phase 2 — Scripting & AI assistance  (~30 min per 10-min video) 🤖
- **Text refinement:** Claude/ChatGPT to restructure + compress wording for narrative flow.
- **Transcription:** export video → MP3 → transcribe via **Otter.ai** → upload the Google Doc to Drive.
- **Visual planning:** annotate the script with graphic-type specs in Google Docs comment bubbles;
  verify the AI's interpretation before proceeding. (= the annotation layer, course version.)

## Phase 3 — Graphics generation (Hera)  (~5-10 min per prompt; ~90 min total once standardised)
- **New tool: Hera** = AI graphics generation. Prep: upload the style guide (colour palette,
  typefaces, reference screenshots). Engineer Hera prompts to the client's visual standards
  (Moore Finance Group here).
- Watch the assembled cut and inventory every graphic needed.
- **Graphic types + specs:**
  - **Chapter pages:** min **3s** per page, played at **197.36%** speed. Built in a separate
    dedicated project.
  - **Half-screen lists:** standalone dedicated project.
  - **Text overlays + lower thirds:** one consolidated project (each built in its own sequence
    first, then integrated).
- **Export/integration:** transparent backgrounds for drag-and-drop; reposition/mask in Premiere;
  add drop shadows in Premiere where contrast/readability needs it.

## Phase 4 — Export  (~10 min per 5-min edited video)
- Codec **H.264**, profile **"Match Source – High bitrate"**, **1920×1080**, **10-bit**.

## Phase 5 — Revisions  (~1 hour per video)

## Aesthetic & efficiency standards
- **Minimalist/subtle animations + graphics only** — no over-animating or over-embellishing.
- High-end, professional output for minimum production effort.
- Do's: consistent folder structures · back up before editing · hit -6 to -12 dB exactly ·
  transparent-background graphics · drop shadows for readability when needed.
- Don'ts: skip the backup · deviate from audio levels · export graphics on non-transparent
  backgrounds · over-animate.

## Where the AI editing system fits
- Assembly + pause removal (Phase 1) = `rough-cut` / the micro-cut stage.
- Transcript + script refinement (Phase 2) = our transcription + LLM edit stages (could replace
  the MP3→Otter→Drive loop with in-pipeline transcription).
- **Hera graphics (Phase 3) = NOT in our pipeline** — a separate AI-graphics tool. Roadmap
  question: do we integrate Hera-style graphics generation, or keep it a manual lead/editor step?
  Note it alongside the reel visual-insert gap in `reel-quality-bar.md`.
- Export preset (Phase 4) is a fixed render profile — trivial to encode.

## Cross-checks for Joseph / Harvey
- [ ] Is this workflow Moore-Finance-specific or the general course-video standard?
- [ ] What is **Hera** exactly (which product), and is it a keeper in the stack or being trialled?
- [ ] Chapter-page 197.36% speed — is that a real house value or a one-off from this build?

## Run log
- 20/07/26 — v0.1 from Harvey's course-video editing SOP (Moore Finance Group build).
