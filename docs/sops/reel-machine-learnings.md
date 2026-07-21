# Reel Machine — Learnings from the W01 pilot (Joseph, 2026-07-20/21)

Hard-won learnings from building 9:16 reels off the "Success Tutoring Strategy Meeting" workshop
(REEL01 vegetables, REEL02 clickbait, REEL03 true-colours). These refine the SOPs and CLAUDE.md.

## 1. Division of labour (REVISED)
- **Claude CREATES the clip; the editor trims by hand.** Claude owns: selection, hook-first structure,
  cutting at clean SENTENCE/CLAUSE boundaries, framing, first-pass captions. The editor owns: fine
  pause/filler/false-start trimming in Premiere.
- **Why the reversal from "micro-cut everything":** word-level auto pause-cutting BLEEDS adjacent
  dropped words back in — ASR word end-times overlap the next word, so `word-end + pad` re-includes
  the stumble ("Because there's", "like,") → "cuts between his words", unclear. Coarse sentence cuts
  land on real silences and stay clean.

## 2. Clip selection & structure
- **Transcript-first is a hard gate.** Every pitched reel comes with its FULL verbatim transcript so
  reel-worthiness is judged from the TEXT, not a one-line summary. Assess against the
  `kan-reel-extraction` gates first (standalone hook / body pays off / clean closer; liberation over
  correction; source not fighting the reel).
- **Hook-first, verbatim reorder.** Pull the strongest standalone line to the front; drop weak lead-ins
  ("The reason why is because…"). Everything stays verbatim so it cuts straight from the footage.
- **Source-fights-reel is real.** A clip can be unsalvageable from the footage: REEL01's hook line is
  delivered with Kan's BACK to camera (writing on the whiteboard) — no reframe fixes a face that isn't
  there. Consultation/multi-person footage fights clean solo reels; teaching/monologue sources better.

## 3. Framing / reframe (editable, no bake)
- **The reframe lives as editable Premiere Motion keyframes, not baked pixels** (Option C):
  `qa_reframe_v2.py --emit-path` dumps the tuned crop path → converted to Motion Position keyframes +
  constant Scale on a full-res clip in a 1080x1920 sequence. Achieves the 2-render goal.
- **HARD RULE: the subject's BODY stays centered** at all times, including on gestures/turns.
- **Sensitivity = heavy smoothing (`--smooth 91`) + a small deadzone (~0.03 of frame width),
  initialised on a real detection, reset per cut (`--cut-frames` + `--global-y`).** Behaviour: still
  body → HOLD (no drift); genuine side-move → follows and re-centres. A pure follow drifts on sway; a
  static Position slides off on gestures; a deadzone with a bad init (back-turned frame) parks off-subject.
- **Framing spec:** tight, eyeline ~0.38 (NOT 0.25 — a high eyeline dumped the foreground table/bottles
  into frame). On multi-person footage, constrain the ROI to the standing presenter so a seated person
  never anchors the crop.

## 4. Captions
- **Style:** keep the SW blue/coral ALL-CAPS-hero, mid-frame look. NOT the old red-italic-serif style.
- **Length:** 2-3 words per cue, never over 2 lines.
- **Quotes: ONE pair per quoted sentence** — do NOT wrap each fragment in quotes. The styler
  (`generate_spice`) adds its own open/close around q-words, so strip literal quotes from the source or
  they double. Use a colon lead-in: `I'm like: "No, it won't."`
- **Emphasis = PAYOFF/impact words** (SELFISH, IMPATIENT, IMPORTANT, PACKAGING, PRESENTATION), NOT
  adverbs/function words (anonymously). ~one accent per line, alternating blue↔coral.
- **Punctuation properly** (periods, commas, colons); curly apostrophes/quotes; clean stumbles/fillers
  from the caption TEXT even though pauses are trimmed by hand.
- **Timing: never lead the audio** — cue starts on the word or a hair after, never before it's said.
- **Knowledge-gap context:** when the speaker uses internal shorthand ("the podcast" = the client
  interview where SW extracts their IP), add a small context title near the caption
  (e.g. "podcast = client interview"). Lo-fi text only.
- **Lo-fi house style:** captions + clean framing only. No motion graphics/animations.

## 5. Render economy / architecture
- **Everything editable in Premiere, only 2 renders** (1 to place, 1 final export). Reframe = editable
  keyframes; cuts = trimmable clips; captions = SRT round-trip re-baked to the styled alpha at final.
- **Round-trip:** editor edits cuts + caption text/timing → exports the SRT sidecar → Claude re-bakes
  the styled overlay from the editor's timeline (the timeline is the source of truth).

## 6. Technical gotchas
- Premiere Motion units: **Position is NORMALIZED (0.5,0.5 = center, can exceed 0..1); Scale is PERCENT.**
- `Sequence.clone()` returns a BOOLEAN and appends a "… Copy" sequence — find+rename it.
- `JSON` is undefined in the ExtendScript engine — write data into the `.jsx` or `$.evalFile`.
- **Caption tracks are invisible to scripting** — the exported SRT sidecar is the only way to read an
  editor's caption edits. When adding a styled alpha, the editor must hide the plain C1 track.
- Multiple projects open: `app.openDocument(path)` brings an already-open project to the front; the
  bridge targets the frontmost project.
- `generate_spice` adds quote glyphs for q-flagged words (see §4).
