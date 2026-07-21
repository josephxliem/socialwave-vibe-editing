# Reel Quality Bar — the standard for machine + human reels (v0.1, 20/07/26)

*The consolidated quality standard for short-form reels: what makes one good, how it's selected,
cut, captioned, and reviewed. This is the JUDGMENT LAYER the AI reel pipeline must hit. Sources:
Joseph's Personal Guides notes (Long form → Reels, Editing Long form Video, Caption Reels, Edit
Reviews) + the repo's REEL QUALITY RULES v2 (CLAUDE.md) + reel-cut guardrails. Every rule tagged
🤖 is machine-enforceable and should live in `reel-cut`'s guardrails / clip-select prompt.*

> **Context matters — two reel specs:**
> - **Client reels** (webinar/podcast repurpose, e.g. Palise): **45-60s sweet spot, 90s max**.
> - **Kan / SW personal brand:** **30-75s, hard floor 30s** (repo brand default).
> Pick by client; the brand interview sets it per account.
>
> **Count:** scripted explainers yield **usually ≥2 reels per long-form** (more for longer
> videos); podcasts **3-5**. The **post-production lead finds the moments** from the long-form.

> **Deeper reasoning lives in `editorial-principles.md`** (the editor onboarding guide): the
> Comprehension Decay / Misalignment / Sacred Timeline principles, the 3-component hook, the 7
> Lego Bricks, the 2-dopamine-hit rule, and the eyes-closed / 2x-speed pre-submission tests. This
> doc is the checklist; that doc is the why.

## 1. The reel arc (the spine — every reel follows it) 🤖
**HOOK (open a loop) → Context → Main Point → Explanation → Close the loop.**
- The reel must deliver a **clear, simple point** the viewer takes away. If it opens a loop it
  can't close inside the clip, it's the wrong moment — don't use it.
- **Hook = the attention-grabber pulled to the FRONT** (verbatim reordering allowed — a reel that
  merely starts where the topic started is weak). Strong hook material: **contrarian / unpopular
  opinion** (then explained), an **analogy**, an **AMS** (attention-grabbing statement) tied to
  the topic, or a **Q&A question**.

## 2. Selection (finding the moments) 🤖-assist
- **Watch intentionally against the transcript**; bold the moment when found; drop a **Marker
  (M)** on the timeline to return to it. Finding good moments is a skill, not a lookup.
- **AI is a VALIDATION tool, not the discovery tool.** ChatGPT/Opus/Otter confirm or surface
  candidates, but they miss context and (Opus especially) don't know where a reel should END.
  Human/judgment picks the real boundaries. *(This is exactly what `reel-cut`'s guardrails fix —
  payoff intact, self-contained, clean end — so the pipeline should lead selection, not defer to
  Opus-style tools.)*
- **Context / audience fit:** a great line isn't automatically a great reel. Don't pick a moment
  that excludes part of the audience unless the source topic is deliberately audience-specific.

## 3. The no-audio test (non-negotiable) 🤖
Most reels are watched **muted** — the reel must be fully understandable from captions + visuals
alone. If it doesn't read without sound, it fails.

## 4. Cutting 🤖
- **Every second counts.** Cut micro-pauses, filler words, and anything that doesn't earn its
  place (a 1:23 → 1:07 trim is normal). Use **waveforms** to spot pauses fast (flat = pause).
- Reorder freely to serve the arc (§1). Captions contain **only what's spoken in the final cut**
  — no filler tokens.
- Kill the **tick after a cut** with a default audio transition (constant power / short cross
  dissolve on audio only). Overlaps `premiere-editor-conventions.md`.

## 5. Captions 🤖
- Position: **near the middle, next to the speaker's face** (so viewers read + see expression).
- **Min 2 words per line**, especially the bottom line — make it easy and satisfying to read.
- **Grammatical goblin:** punctuation/casing matters; small fixes compound into viewer
  satisfaction. Caption wording may be lightly edited for flow even if the speaker said it
  slightly differently (meaning preserved).
- Pace: readable, not too fast — allow >2 lines to buy on-screen time when needed.

## 6. Audio levels 🤖
- **Voice: −6 to −12 dB** · **Music: −25 to −30 dB** · **SFX: between** (higher pitch → lower dB).
- Music from the **per-client YouTube Music Library** asset folder (mood folders); rights-cleared
  only.

## 7. Framing / angles 🤖
- Tight, follow the subject (repo v2 rule 5). Zoom in to remove distracting hands/gestures.
- Switch angles by **enable/disable, never delete** (toggle the top video layer only) — deletion
  is unrecoverable.

## 8. The social first-frame (thumbnail) 🤖
The reel's **first frame is its preview image** on IG/TikTok. Put a **short, clean cut of the
speaker's face in a good position at the very front** (extend the hook caption over it) so the
feed preview looks intentional, not a mid-blink freeze.

## 9. Export
- **Reels: bitrate 10.** Send to **Media Encoder**. Name the file properly (not "Reel 1").
  (Long-form podcasts/webinars: bitrate 3; Zoom recordings: bitrate 1.)

## 10. The review bar (how a lead QCs a reel — from Edit Reviews) 🤖-audit
- **Frame.io**: exact timings + draw-on-screen; notes must be **impossible to misinterpret**
  (re-exporting graphic-heavy videos is slow — ambiguity is expensive).
- Reference the **client style frames** (fonts/graphics allowed) + the **script with editor
  comments** (word-by-word).
- **"People watch videos so they don't need to read"** — show relationships/equations, not blocks
  of text. Grammatical goblin applies to on-screen graphics too.
- Give feedback **+ the WHY**, and categorise: **required edit / personal preference / creative
  choice** (the last two give the editor freedom). Aim ≤1 internal revision round.

## Machine-conformance checklist (what `reel-cut` output must satisfy) 🤖
- [ ] follows the HOOK→Context→Point→Explanation→Close arc; hook is the strongest line, front-loaded
- [ ] self-contained + closes its loop; passes the no-audio (muted) test
- [ ] micro-cut: no filler tokens, no dead pauses; captions = spoken words only
- [ ] captions mid-frame near face, ≥2 words/line, grammatically clean, readable pace
- [ ] levels: voice −6…−12, music −25…−30; audio transitions kill cut-ticks
- [ ] clean speaker-face first frame for the social preview
- [ ] length within the client's spec (45-60s client / 30-75s Kan)
- [ ] exported at bitrate 10, named properly
- [ ] captions verbatim-to-script: exact wording, punctuation, quotes opened+closed, correct
      casing, numbers in full; non-verbatim words in [square brackets]; one accent colour per point
- [ ] captions synced to the spoken word (not early); repositioned off any on-screen graphic
- [ ] evergreen: no dated references (year mentions) cut; no redundant/fluff repeats
- [ ] visual inserts only where they SERVE the message (cut b-roll that pulls focus)

## Worked examples — real reel reviews (Frame.io, ~28 notes across 3 reels, 20/07/26)

Analysed to calibrate the bar against actual project-lead → editor rejections (the Maddox loop):
**Reel 03 "Megaphone vs Dog Whistle"** (8 notes), **Reel 02 "Production Quality Doesn't Matter"**
(10 notes), **Reel 03_V1** (10 notes incl. praise). (A 4th, Reel 02_V1, sat behind a guest
name/email gate — not opened.)

**Overwhelming pattern: captions are ~2/3 of ALL notes.** Whatever else the pipeline nails,
captions are where reels get sent back. And notes cluster on the **hook (first few seconds)**.

### Caption rules (the dominant category) 🤖
- **Exact wording** to the approved script ("replace with 'YouTubers'", "level of brand").
- **Punctuation:** add/remove full stops on command; **open AND close quotation marks**; follow
  the script's quotes exactly.
- **Casing:** capitalise sentence starts; **lowercase mid-sentence words** ("right?" not "Right?").
- **Numbers written in full:** "4000 to 7000", not "4 to 7000".
- **Bold the key figure** ("$400,000 a year") for visibility, especially over a busy background.
- **Colour discipline:** **one accent highlight per point** — don't over-colour (keep "Chinese"
  white when "knockoffs" is already the red highlight). Refines the spice_socialwave payoff-word rule.
- **Timing/sync:** caption appears **when the word is actually said**, not early.
- **Grouping:** group a short fragment with its adjacent line ("…about the quality, right?").
- **Positioning:** reposition captions when an on-screen graphic/screen cuts them off.
- **Square brackets for non-verbatim words** ("[he]") when the speaker didn't say it verbatim.
- **Catch skimmed/rushed words** and caption them correctly.
- **Spelling checked every time** ("super important").

### Cut / content rules
- Remove **grammar-breaking stray words** ("is", "actually") even when tightly spaced.
- Remove **redundancy / fluff** (a point repeated with examples).
- **Cut dated references** ("2025") → keep creative **evergreen** (matters doubly for ads).
- **Don't over-tighten past the Context beat** — a lost "I was like:" lead-in kills conversational flow.

### Visual inserts — CONDITIONAL (the nuance) 🤖-gap
- Some reels: **add** script-referenced images/b-roll *below the captions* (proof photo, the
  screen content, highlight a follower count when mentioned).
- Other reels: **remove** b-roll when it **pulls focus from the message** — keep the audience on
  the speaker + captions.
- Rule: **inserts serve the message; cut them when they distract.** `reel-cut` does talking-head +
  captions only today — script-keyed visual inserts are a real **roadmap gap** for client reels.

### Pacing nuance
- **A deliberate micro-pause at a transition can improve flow** ("add a bit of a pause after
  'best'"). Nuances the cut-all-pauses rule — beats at transitions are good; dead air isn't.

### What gets PRAISED (positive patterns to keep)
- **Front-loaded brand/hook treatment** ("the 'brand' stuck out front and separate — amazing").
- **Bold contrast colour imagery** (red for negative brands / knockoffs).
- Reviewers actively **encourage experimentation** — the bar rewards initiative, not just compliance.

### Verbatim / script fidelity (repeated, emphatic)
"Follow the Google Docs script" appears again and again. The script is ground truth for wording,
punctuation, and where visuals go. Square-bracket anything not said verbatim.

## What would sharpen this further (resources to get)
1. **Real Frame.io revision threads on reels** — the actual reject→reason→fix comments. The
   deltas between draft and approved ARE the bar in action; each becomes a guardrail rule.
2. **3-5 approved reels paired with their source long-form** — shows selection + cut + caption
   choices concretely.
3. **A "bangers" set + a "rejected/weak" set with reasons** — the contrast teaches the boundary
   better than either alone.
4. The **Caption Reels Google-Doc SOP** (linked in the note) — a distinct native-IG-text format.

## Run log
- 20/07/26 — v0.1 consolidated from Joseph's Personal Guides notes + repo v2 rules + reel-cut guardrails.
