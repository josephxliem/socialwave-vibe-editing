# SW Client Assembly Cut — living SOP (v1, 08/07/26)

*Goal: automate the assembly cut of a client YouTube video (full run footage → complete end-to-end cut in words, no animations/screenshares yet). Engine: Peter Phan's rough-cut kit (`SW-APPS/rough-cut/`) + premiere-pro-mcp. Baseline today: 2-3 editor-hours per 12-18 min video. Target: ~20 min human attention + background compute.*
*This is a LIVING doc (Hunter's rule): update after every run with what worked/broke.*

## The SW footage reality (design inputs, per Joseph 08/07)
- 2 cameras: **A-cam** = teleprompter front-on, MAIN audio (studio mic) → the reference angle. **B-cam** = side angle, backup audio (lav backup; sometimes shotgun on cam).
- One exported file per angle, audio attached ✓ (Peter's hard requirement met).
- 30-45 min raw per video → 12-18 min final. 2-4 videos per session, but the videographer pre-splits footage per video in Dropbox, so input is already per-video ✓.
- Take markers: verbal countdown AND/OR audible clap. Between-take chatter = videographer directions + client script questions. Flubs = full-sentence restarts (teleprompter).
- **The script exists and is client-approved BEFORE the shoot** → available as ground truth.
- Dropbox/Premiere convention: bins `Assets / Exports / Footage / Premiere` (mirror these, not Peter's names).
- Editors: mixed Mac/Windows (offshore mostly Windows) → **the pipeline runs on a central Mac, not editor machines** (see Rollout).

## The workflow (per video)
**Human step 0 (~5 min):** copy the video's Dropbox footage folder local (never work in Dropbox) + drop the approved script (txt/doc) into the project folder.
**Human step 1 (~5 min):** in Premiere, sync A+B into one sequence (multicam merge or manual sync), NO cuts. Start the MCP bridge panel (Window → Extensions → MCP Bridge).
**Agent steps (background, ~30-60 min for 30-45 min footage):** Claude Code session, say "rough cut":
1. Transcribe A-cam audio in full (word timestamps, cached).
2. Deterministic defect detection: countdowns, duplicate/stumbled phrases (restarts), pauses >1s. Clap markers via audio analysis if verbal countdown absent.
3. Semantic review (run 2x, union): keeper-take choice, videographer/client chatter boundaries. **SW upgrade over Peter's default: feed the approved SCRIPT into this step, keeper = the take matching the script; deviations get flagged, not guessed.**
4. Build word-anchored EDL (+0.5s tails) → verify-loop until clean → cut A-cam → verify → propagate to B-cam (sync offset independently verified).
**Human step 2 (~15 min):** editor opens the cut, reviews flagged judgment calls, chooses angles (A/B switches), confirms pacing. Assembly done → proceed to normal edit (animations, screenshares, B-roll).

## Per-client speaker profiles
One `speaker_profile.json` per client talent (countdown style, on-set direction phrases, restart style). Build on first video, reuse forever. Profiles live in this repo: `documentation/speaker-profiles/<client>.json`. First: Davie Mach (Box Advisory).

## Rollout model (solves Mac/Windows)
- Pipeline runs on ONE Mac (Joseph's for the pilot; a dedicated Mac later if it earns it).
- Editors receive the CUT OUTPUT via Dropbox: the Premiere project (or exported XML) + the verified cut. Premiere projects open cross-platform; media relinks against the same folder structure.
- Editors never need Claude Code, Macs, or new tools. The machine is a service step between "footage wrangled" and "editor starts".

## Pilot: Davie Mach (Box Advisory)
1. Prereqs: Peter's Premiere-bridge patches in hand · premiere-pro-mcp installed + bridged · whisper model predownloaded (`rough-cut/tools/download_model.py`, ~3GB) · one recent Davie video's footage + script.
2. Build Davie's speaker profile (from the videographer's knowledge of the shoot habits + first transcript).
3. Run the workflow end-to-end. Record: human-minutes, compute-minutes, missed defects, false cuts.
4. Editor (Jen/assigned) reviews the output against what they'd have done manually. Their verdict = the pilot result.
5. Update this SOP with everything learned; then present numbers to Kan (baseline 2-3 hrs → measured result).
- NOTE: Kan workshop recordings ≠ assembly-cut material (unscripted, no takes). They pilot vibe-editing's clipping instead.

## Why this doc doubles as course IP
This is the editing-workflow SOP SW doesn't have ("all in Noel's head" class). Once proven, it feeds THE EXPANSION's production/editing unit + the agency SOP folder (Edwin's vlog workflow doc = the sister SOP for vlog-style edits).

## Run log
- (append per run: date · video · human-min · compute-min · defects missed · fixes made)
- 10/07/26 · **reel-cut pilot** (not assembly) · Kan video 22 FINAL EDIT → 13 candidates, 6 approved by Joseph, EDLs verified, bridge down → per-reel FCP7 XML + audio previews in project 002 `exports/` · ~10 human-min, ~6 compute-min · fixes: discover_session s24le WAV bug (pre-extract s16le), adaptive tail buffer (fixed 0.5s clips next-word onset on edited sources) · full detail: `CUT-PROJECTS/002_…/RUN-REPORT.md` + new guardrails hard rule 0 (no YT-intro material).
