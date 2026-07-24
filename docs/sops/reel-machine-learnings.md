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
- **Clarify audience-unfamiliar jargon INLINE for comprehension** (Joseph, 21/07 TF R01). A cold
  viewer (often muted, no context) may not know the speaker's shorthand — expand it in the caption
  so the reel reads on its own. E.g. Adrian says "techs" → caption "[technicians]". This is a
  COMPREHENSION aid (reels are watched to understand), distinct from the non-verbatim-brackets
  convention — same glyph, different reason. When generating captions, scan for trade/insider
  shorthand the target audience may not follow and clarify it.
- **Lo-fi house style:** captions + clean framing only. No motion graphics/animations.

## 5. Render economy / architecture
- **Everything editable in Premiere, only 2 renders** (1 to place, 1 final export). Reframe = editable
  keyframes; cuts = trimmable clips; captions = SRT round-trip re-baked to the styled alpha at final.
- **Round-trip:** editor edits cuts + caption text/timing → exports the SRT sidecar → Claude re-bakes
  the styled overlay from the editor's timeline (the timeline is the source of truth).

## 6. Technical gotchas
- Premiere Motion units: **Position is NORMALIZED (0.5,0.5 = center, can exceed 0..1); Scale is PERCENT.**
- **⚠ Bridge `set_clip_volume` / `adjust_audio_levels` are BROKEN — they MUTE the clip** (TF rep 3, 21/07). They write the dB number straight into the audio Volume "Level" property, but that property is a NORMALIZED gain (1.0 = unity/0 dB, 0 = silence, value = 10^(dB/20)), NOT dB. So `set_clip_volume(-6)` writes 0 (clamped) = SILENCE; even `set_clip_volume(0)` writes 0 = silence. Every call mutes. **Never use them.** Set audio gain via ExtendScript on the Volume component Level with the normalized value: `pr.setValue(Math.pow(10, dB/20), true)` — e.g. −6 dB → 0.501, −5.5 → 0.53, unity → 1.0. Iterate `seq.audioTracks[t].clips[c].components` for displayName "Volume" → property "Level". Confirm the source peak first (ffmpeg volumedetect) and target a −6 dB peak ceiling (voice in −6…−12, hard rule 10).
  CALIBRATION (Joseph, 21/07 TF R01): a −6 dB *peak* was WAY too loud on this mono Loom source. His satisfactory setting = **≈ −11.5 dB total gain** (he used Level 0.53 + clip Audio Gain −6; equivalent single Volume Level ≈ **0.266**). So for this source type, target the QUIET end of the band (~−11 to −12 dB effective, Level ~0.26), not peaks-at-−6. Also: the clip **Audio Gain** (QE `staticClipGain`, the G-key dialog) is a SEPARATE gain stage from the Volume-effect Level — they multiply; `staticClipGain` is read-only via QE assignment, so control level through the Volume Level property instead.
- **⚠ Bridge `set_clip_position` stores its x,y RAW into the normalized Position property — it does NOT convert pixels, despite the tool doc saying "pixels."** Passing `(540,960)` for a "centered" 1080x1920 clip writes Position `[540,960]` normalized = ~540 frame-widths off-screen → BLACK program monitor / "no video" (TF rep 3, 21/07/26). **Pass normalized: centered = `set_clip_position(x=0.5, y=0.5)`; Scale stays percent (`set_clip_scale(178)` = height-fill for a 1080p source in a 1080x1920 seq).** For a static webcam speaker, a static `[0.5,0.5]`+178% is a clean editable reframe (no per-frame tracking needed); verify the crop by simulating in ffmpeg (`crop=608:1080:656:0`) since bridge `export_frame`/`capture_frame` are broken on Premiere 25.4.1 (`exportFramePNG` not a function).
- **Multiple projects open:** `create_project`/`open_project` do NOT reliably bring the new project frontmost, and the bridge targets whatever project is FRONTMOST in the Premiere UI. Build a batch, then if the user later fronts another project the bridge follows it (reads/writes hit the wrong project, "sequence not found"). Confirm with `get_premiere_state.project.name` before operating; have the user front the target project if it drifted.
- `Sequence.clone()` returns a BOOLEAN and appends a "… Copy" sequence — find+rename it.
- `JSON` is undefined in the ExtendScript engine — write data into the `.jsx` or `$.evalFile`.
- **Caption tracks are invisible to scripting** — the exported SRT sidecar is the only way to read an
  editor's caption edits. When adding a styled alpha, the editor must hide the plain C1 track.
  Verified 21/07 (TF rep 3): `activeSequence.captionTracks` is UNDEFINED in both the standard and QE
  DOM. The bridge can `create_caption_track` but CANNOT enumerate, read, or delete one — so you can
  never remove or replace a caption track programmatically, only add. **Consequence: only bake a
  caption track AFTER the cut is locked.** If cuts change after baking, the captions desync (a seg-1
  trim of 1.35s made every seg-2 caption 1.35s late — the "captions lag" bug); re-baking then leaves
  an orphan track the editor must delete by hand. Generate captions from the CURRENT timeline
  boundaries (source in/out per clip via get_full_sequence_info), not from the original planned cut.
- Multiple projects open: `app.openDocument(path)` brings an already-open project to the front; the
  bridge targets the frontmost project.
- `generate_spice` adds quote glyphs for q-flagged words (see §4).

## 7. Rep 3 additions — TF Sales Session (Adrian Fadini, 21/07/26)
First run on a NON-Kan client (a mono Loom group sales-coaching call). New rules, generalised:

### Selection (hard rules)
- **CLEAR TAKEAWAY / behaviour change.** Educational content must let the viewer DO something differently. A perfect hook/body/closer with no actionable substance is DEAD. A big-result STORY with numbers (e.g. "15 tasks, 11 grand, we got it") is NOT a takeaway if the transferable principle is buried — it reads as a flex. Test at selection: state the one behaviour change in a sentence AND confirm the reel delivers it front-and-centre.
- **Closer must land on a FALLING pitch.** Prosody, not just wording — a closer delivered on a rising pitch sounds unfinished/awkward and the reel doesn't work. Reorder to a falling line or trim back to one (terminal f0 slope checkable acoustically).
- **Camera must hold on the speaker for the whole cut.** Active-speaker recordings (Zoom/Loom group calls) swap to whoever talks + to screenshares. Contact-sheet the span (~2s intervals) BEFORE promising a reel; a payoff line in a participant's voice/on their cam kills it.

### Per-client brand (NEW standing rule)
- Reel-cut now serves multiple clients. **Interview the client/operator on caption + title STYLE before building the first batch for any new client** — never default to SW blue/coral. Save a per-client brand card and reuse. (TF card: green #00FEA9, white bold-italic ALL-CAPS.)
- **Caption position is per-client.** TF wants captions **near-centred, JUST BELOW the face (~58-62%)**, NOT lower-third — captions sit next to the face so viewers read + see expression.
- **Caption size: BIG** (~96px on 1080-wide) with tight 2-3 word lines + a safe-zone cap so no word ever clips the frame edge.
- **Clarify audience-unfamiliar jargon inline** for comprehension (e.g. "techs" -> "[technicians]") — a cold muted viewer must follow it. Separate from the non-verbatim-brackets convention.

### Title text (per-reel, only when the hook lacks context)
- Not every reel needs it. Bake one only when the hook is unclear standalone. Use the kan-title-text method (active verbs, "you" framing, 7 words, specific-not-generic) but ANCHOR to the client's ICP — generic title text that could fit any niche fails. If the speaker states the framing out loud (e.g. "three things"), the title supplies the missing CONTEXT/purpose, not a repeat. (TF R03 example: "Tradies: This is NECESSARY to close every job.")

### Audio (see §6 for the mechanism)
- Set gain via ExtendScript Volume Level = 10^(dB/20) — NEVER the bridge volume tools (they mute). CALIBRATE to the source: a −6 dB peak was too loud on this mono Loom; satisfactory ≈ −11.5 dB effective (Level ≈ 0.266). Measure the source peak first, target the client's satisfactory band.

### Transcription
- Groq whisper-large-v3, ~17s/hr. Do NOT sort words by timestamp (scrambles neighbours). For caption TIMING, transcribe the SHORT final reel audio, not slices of the long transcript.

## 8. Rep 3 FINAL — the locked pipeline (Joseph, 2026-07-22)

Three reps on TradesFormation (a Zoom sales-coaching call) locked the system. **Division of labour:** the AI automates ~90% of the OUTPUT — caption TIMING + pause/filler TRIMMING + reel assembly in Premiere. Reel SELECTION keeps a human taste element (the operator confirms/reworks the scripts before anything is built). The two things that MUST be nailed are caption timing and pause trimming — that is where the manual hours go.

### 8a. Caption timing — THE #1 priority, nail it 100%
- **One mistimed caption cascades:** every later cue then needs re-timing by hand. Getting this right is the single biggest time-saver; getting it wrong is the single biggest time-sink.
- **Time from the SHORT reel's OWN transcription — NEVER the long session transcript.** Long-chunk Groq/Whisper word-timestamps drift ~+0.8s deep inside each 600s chunk, so mapping them onto a reel makes every caption ~0.8s late (the recurring failure across reps). Validated on Joseph's hand-tuned R04: raw onsets from transcribing the *assembled reel* land median ON the word (−0.03s), within ~2 frames.
- **Do NOT "energy-snap" or align to the on-screen waveform.** Tested — it overshoots ~0.5s early and makes timing worse. Raw reel-transcription onset is the answer.
- **Footage type changes the method — ASK "what kind of footage is this?" at intake, every time:**
  - **Zoom / online / sales-call** (most clients): the waveform you SEE in Premiere LAGS the real audio — they do not match. Time strictly from the transcription (caption flips exactly when the word is spoken), never off the visible waveform.
  - **In-person / workshop:** waveform matches the audio; either reference works.
- Rule: a caption changes exactly WHEN the word is spoken, NEVER before it is said. Target ≥90% correct so the operator's manual pass is ~15–20 min max.
- If the transcription drops a quiet/remote participant's word, hand-place JUST that one cue from cut geometry — do NOT fall back to long-transcript mapping for the rest.
- Whisper drops the first 1–4 words after a hard cut (no silence lead-in). Fix: align the clean cue text to the whole-reel transcription onsets (difflib) and evenly distribute any unmapped opening run between the cut start and the first mapped word.

### 8b. Pause / filler trimming — the "SCRIPT DEFINES THE CUT" model
The approved caption script IS the edit-decision list. Keep exactly the approved words; delete everything between them:
1. **Pure silence ≥0.4s** → razor + ripple (butt-join), keeping ~0.08s padding around each word so nothing clips.
2. **Non-script filler / stutter / tic / false-start** (um, uh, "right,", doubled words, "though she never even,") → remove, any length.
3. **Anything not in the approved script** (redundant tangents) → remove.
4. **Leave <0.4s micro-pauses** — natural rhythm is the operator's taste call.
5. **WORD-SAFETY IS ABSOLUTE:** never clip a word that is in the approved script. If a gap/filler can't be removed without risking an approved word, LEAVE it and flag it with a **timeline marker** — losing words is worse than leaving a pause.
- Cut on VAD/silence boundaries, NOT ASR word-ends (ASR word-ends overlap the next word → they bleed the stumble back in → "cuts between his words").
- This model reproduced 100% of Joseph's hand-cuts on R03 and R04 (verified by diffing his cut sequences against the source).

### 8c. Selection (human-in-the-loop) — three takeaway gates
- Transcribe AND watch the footage; a moment must work on BOTH the words and the video (drop moments where the speaker leaves frame / there's no usable shot).
- Deliver ~5 candidate scripts (hook / body / closer+takeaway) as TEXT. Operator approves / reworks / culls BEFORE any building.
- **Takeaway gates — ALL required:** (1) a takeaway EXISTS; (2) it's EXPLICITLY spoken (not demonstrated/inferred — R06 cull); (3) it has enough MEAT that spending the viewer's ~60s is a FAIR TRADE (R08 cull: a thin one-line tip padded with role-play). Thin takeaways get culled — it respects the audience and the brand.
- **Hook must NOT answer the premise** — open the loop; put the principle at the payoff, echo it in the button (R04 reorder).
- Camera must hold on the speaker for the whole cut (active-speaker Zoom/Loom recordings swap between people + screenshares).

### 8d. Assembly / output
- **Everything stays editable** — trimmable cuts + live reframe (Motion) + an editable caption track. The ONLY renders are the styled caption alpha .mov and the final MP4 export to the project's Exports folder. Never hand over a flattened clip.
- Reframe: static for a fixed webcam (height-fill scale, Position normalized to centre the subject; a second speaker on a different camera needs their own centre). Multi-cam: operator sets up the angles first + drives angle-changes while the AI learns, automate later.
- Audio gain via ExtendScript Volume Level = 10^(dB/20); NEVER the bridge volume tools (they mute). Calibrate to the source.
- Per-client BRAND INTERVIEW before the first batch (caption style, hero colour, font, logo, title-text style); save a brand card and reuse.

### 8e. Caption-track workflow + the hard bridge limit — WRITE MANUAL STEPS FOR TOTAL BEGINNERS
The operator may be anyone on the team who has never done this. Any manual step you ask for MUST be spelled out click-by-click, no insider shorthand.
- The premiere-pro bridge can ADD a caption track but CANNOT see, read, or delete one. Consequences:
  - Lay the plain editable caption track **ONCE** (nail the timing first pass). The operator edits timing/text in place (~15–20 min).
  - The operator exports the SRT sidecar — the ONLY way the AI can read the edits — then the AI re-bakes the styled alpha. Beginner steps: **File → Export → Media (⌘M) → Captions tab → "Create Sidecar File" → Format: SubRip (.srt) → Export.**
  - If a caption track ever needs REPLACING, the AI must TELL the operator BEFORE and give exact clicks: **on the timeline, right-click the caption track's header (far left) → "Delete Track"** (or click the track's caption clips and press Delete). Never assume they know this.
- **Import each SRT under a UNIQUE filename.** Re-importing the same file path makes Premiere serve its STALE cached caption data → duplicate tracks with wrong timing (burned an hour across R04/R08). New content = new filename.
