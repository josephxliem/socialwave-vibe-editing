# Unscripted Content (Podcasts / Interviews) — workflow (v0.1, 20/07/26)

*The workflow for SW's unscripted content — podcasts and interviews. Reconstructed from the
"Workflow for Unscripted Content Production" Loom (~11 min) + its Figma board (same 4-phase
structure as the scripted one, confirmed from frames). **Simpler than the scripted explainer
workflow** — read `scripted-youtube-explainer-workflow.md` first; this doc is the delta.*

> **Same board shape** (`#1 Pre-Production → #2 Production → #3 Post-Production → #4 Distribution`,
> colour-coded nodes + parallel branches, loops back at the end). ~1yr old, Joseph confirms still
> relevant.
> **Strategic note:** SW pushes YouTube (scripted) harder because success/conversion is more
> controllable; podcast performance rides on guest + conversation + topic quality. But podcasts
> earn their place — networking, opening doors, growing socials, and **the reels pop off**. Ties
> directly to omnipresence: **Grace Space's ad/organic source is podcasts** (see
> `tradesformation-omnipresence` context) — this workflow feeds that ad machine.

---

## #1 — PRE-PRODUCTION

- **Client books + briefs the guest** on the topic. SW advises which topics will/won't perform.
- **Project lead** (who manages the account) coordinates the **recording date with the
  videographer** — mostly filmed in the SW studio; some clients offsite (ad hoc). Regular
  podcasts (fortnightly/weekly/monthly) film in-studio.
- **Design / style frames** only if it's a brand-new client — and **far fewer formats needed**
  than scripted (podcasts use simple titles + graphics mostly for the hook; little animation
  through the body).

---

## #2 — PRODUCTION

- **Batch film** with client + guests — usually **3-4 episodes per session**.
- **Live transcript during filming via Otter** — the RØDE Podcaster mixer's USB-C out feeds a
  laptop running Otter; the transcript is saved.
- **Hook writing (after the session):** upload the Otter transcript to ChatGPT → generate strong
  hooks that hit the episode's key discussion points + build a curiosity gap (better than the
  client ad-libbing a weak hook). Matters because it's going on YouTube, not just audio.
- **Camera angles:** usually **3** — master wide (all guests) + a close-up on each guest/side.
  Sometimes **4** when there's an extra element (e.g. tabletop whiteboarding → a top-down camera
  on a C-stand).
- **Videographer wrangles + sets up + editing notes + light grade + light sound treatment**
  (same as `wrangling-and-project-setup.md`). Sound: RØDE pod mics + mixer need little treatment
  (level balancing, a general AC-hum filter). Colour: same lenses across angles = easy; shoot a
  **neutral picture profile (usually NOT log), same across all cameras**.
- **AutoPod** sometimes used to auto-cut between the camera angles.

---

## #3 — POST-PRODUCTION

- **Assembly cut** (editor). If AutoPod ran, mostly **fixing shots where it picked the wrong
  camera**; the **extra top-down angle is where AutoPod struggles**, so the editor fixes those.
- **Hook / graphics / titles** built from the style guides (consistent fonts/colours).
- **Reels — 3-5 per podcast (min 3, sometimes more).** Selection uses a *combination* of tools:
  - **Otter** = the recording transcript.
  - **ChatGPT** = find good talking points from the transcript.
  - **Opus** = good at finding hooks / high-engagement moments, **bad at knowing where the reel
    should END** (whether the main point has landed — usually it hasn't).
  - No perfect tool yet → combine them + **human judgment** so each reel works standalone without
    needing the full long-form context. Project lead gives guidance.
  - **Tool stack is person-dependent** (Joseph interview 20/07/26): Joseph himself uses
    **transcription in Claude Code** rather than Otter/Opus — which is exactly the `reel-cut`
    path. So this workflow is already migrating toward the AI system for reel selection.
- **QC (Frame.io) for long form + reels.** Long-form feedback centres on: making the **hook
  engaging**, and **removing sensitive parts** the client shouldn't have said (project lead has
  the context on what could land them in hot water). Editor applies internal revisions.
- **Thumbnail + packaging** (parallel) — project lead does packaging ideas (informed by having
  watched the hook + topic focus); designer builds thumbnails in Photoshop.
- All (long form + reels + thumbnails) → **client approval**.

---

## #4 — DISTRIBUTION

- **Post to all platforms — including the audio podcast platforms** (Spotify/Apple etc.), plus
  YouTube + socials.
- **Assess performance + reiterate.** (Less topic control than scripted — depends on the guest.)

---

## Where the AI editing system plugs in (strong fit)

| Board node | AI system asset / note |
|------------|------------------------|
| Live transcript (Otter) | our pipeline transcribes anyway (Parakeet/Groq/AssemblyAI) — could replace Otter |
| Hook writing from transcript (ChatGPT) | our reel/copy skills already do this |
| **AutoPod multicam angle-cutting** | **`rough-cut` does synced-multicam angle selection** — a transcript-driven alternative to AutoPod. Its known weakness (the top-down/extra angle) is exactly where a smarter, script/transcript-aware cutter helps. |
| Assembly cut | `rough-cut` |
| **Reels (3-5 per podcast)** | **`reel-cut` is purpose-built for this.** The "Opus doesn't know where the reel should end" problem is precisely what reel-cut's guardrails fix (payoff intact, self-contained, clean end). Best-fit automation in this whole workflow. |
| Captions | `caption-clips` |
| Sensitive-content removal | ⚠️ human/project-lead judgment — NOT automatable; keep the QC gate |

**The pitch this workflow makes for the system:** podcasts already lean on Opus/Otter/ChatGPT and
AutoPod — a fragmented stack with a known reel-ending weakness. `reel-cut` + `rough-cut` replace
most of it with one transcript-driven pipeline that already solves the ending problem. And since
Grace Space's omnipresence ads are podcast-sourced, improving this directly feeds the ad machine.

## Cross-checks for Joseph
- [ ] Board node labels reconstructed from narration (720p) — correct any missing/renamed nodes.
- [x] Reel-selection tool stack: **person-dependent**; Joseph uses Claude Code transcription
      (= `reel-cut`). Otter/Opus/ChatGPT still used by others (20/07/26 interview).
- [x] **3 angles standard (4 with whiteboard)** confirmed; **neutral profile, not log** confirmed
      (20/07/26 interview).

## Run log
- 20/07/26 — v0.1 from the Unscripted Content Production Loom + Figma board.
