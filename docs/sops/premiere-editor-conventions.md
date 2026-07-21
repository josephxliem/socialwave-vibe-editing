# Premiere editor conventions — the house style (v0.1, 20/07/26)

*Extracted from the editor training Looms: "00. Assembly Cutting Basics, Visual Practices, and
Keybinds" (15 min) + "01. Premiere Audio Cleanup and Enhancement Workflow" (11 min). This is the
stage-5 conventions doc: what a hand-edited SW timeline looks like, and therefore what
machine-generated timelines must conform to. Rules marked 🤖 are enforceable by the AI pipeline.*

## 1. Cutting rhythm

- **YouTube assembly cuts:** conversational rhythm — a little dead space when a sentence/point
  ends, tight within a sentence. Not the reel jumpcut model. 🤖
- **Reels:** tight jumpcut model — no pause longer than ~0.5s (see REEL QUALITY RULES v2 in the
  repo CLAUDE.md). 🤖
- Bad takes: remove entirely; keep the better take and let the two good takes connect.
- Workflow habit: make the cut → **listen to it** → apply constant power → move on. Never leave
  a cut unheard.

## 2. Audio (from Loom 01 — do this the moment you get the project)

- **Constant power on EVERY audio cut.** Set constant power as the default audio transition
  (right-click → set as default), default duration **0.10s** (Edit → Preferences → Timeline),
  apply with Shift-D at each cut. Nudge/lengthen individual transitions where a cut still reads
  jarring. 🤖 (machine timelines/renders must ship with equal-power ~100ms crossfades baked)
- **At the EDIT stage, don't rely on Premiere's Essential Sound** for the main clean-up — the
  house loop is Adobe Podcast Enhance. (Note: the videographer already applied a *light* Denoise/
  Dereverb/Vocal Enhancer pass at wrangle — see `wrangling-and-project-setup.md` step 5. Enhance
  is the deeper second pass, not a duplicate.) The Adobe Enhance loop:
  1. After the assembly cut, export audio as **MP3 256 kbps** into an `enhanced audio` folder
     (lives next to the project; new Dropbox structure has a dedicated folder).
  2. Upload to **podcast.adobe.com/enhance**. Sliders: **Speech 30-60%, Background 10-30%**,
     judged by how rough the source is. A/B against the original before accepting.
  3. Download, rename with ` enhanced` suffix. **The folder holds exactly two files:** the
     original assembly audio and the latest enhanced version (replace, don't accumulate).
  4. Drop the enhanced file on a new audio track UNDER the original.
  5. ⚠️ **THE SYNC GOTCHA: Adobe Enhance output comes back ~1 second AHEAD of the original.**
     Zoom into the head, cut one tick (~1s) off the start, then nudge the whole file back one
     frame. Verify waveforms align before any further cutting. Skipping this poisons every cut
     you make afterwards. 🤖 (automatable: script the offset detection + correction)
  - No Adobe access? Do everything else, flag to your lead that the export still needs enhancing.
- Gain: bring the enhanced track up to sit right (reference example ran +6 dB). Judgment call,
  make it deliberately.

## 3. Visuals — base frame setting (from Loom 00)

Do this once, immediately after (or right before) the assembly cut, BEFORE detailed editing:

1. **Anchor point on the subject's face** (not the default frame centre) — punch-ins then keep
   the subject's framing automatically. 🤖 (bridge: `set_clip_anchor_point`)
2. **Base scale**: slight punch-in from 100 so there's room to move both ways.
3. **Position**: subject on the guides, centre-stage, negative space balanced.
4. **Copy the Motion effect to every clip on the timeline** (track-select, paste attributes) so
   base framing is uniform before any keyframing. 🤖

Applies doubly to reels — tight framing makes anchor-point discipline more visible, set it when
transferring a select to a reel timeline.

## 4. Keyframing house style

- **First keyframe of a move = Ease Out. Last keyframe = Ease In.** Every motion cut. (Keybinds:
  the trainer maps F3 = Ease Out / F4 = Ease In via the Effect Controls Panel section.) 🤖
- **Never stack two motion moves on one clip** — cut the clip and start the second move fresh
  (flip the boundary keyframe to Ease Out on the new clip).
- Result to aim for: no choppy punch-ins, no motion-smoothness revision rounds.

## 5. The efficiency keybinds (human editors — build the muscle memory)

| Key | Action | Use |
|-----|--------|-----|
| Q | Ripple Trim Previous Edit to playhead | kill dead space behind the playhead |
| W | Ripple Trim Next Edit to playhead | kill dead space ahead of the playhead |
| F (custom) | Ripple Delete | remove a selected bad take, joins the good takes |
| Shift-X | Add Edit | cut at playhead |
| Shift-A (custom) | Add Edit to All Tracks | cut every track at once |
| Shift-D | Apply default audio transition | constant power on the cut |
| L (tap repeatedly) | Play, faster each tap | review footage at speed |
| Shift-→ | Step 5 frames | keyframe placement |

Track targeting matters: Q/W respect which V/A tracks are enabled — check targeting before
trusting a ripple.

## Machine-conformance checklist (what the AI pipeline must guarantee) 🤖

Any timeline or render the pipeline hands to an editor:
- [ ] constant-power/equal-power ~100ms on every audio cut
- [ ] pause policy matches the deliverable (YouTube conversational vs reel ≤0.5s)
- [ ] anchor point set on subject + uniform base Motion across clips (bridge-built sequences)
- [ ] any generated keyframes follow Ease Out→Ease In, one move per clip
- [ ] enhanced-audio track synced (1s head trim applied) when the enhance loop ran

## Run log
- 20/07/26 — v0.1 extracted from the two editor training Looms (Kan's Loom account).
