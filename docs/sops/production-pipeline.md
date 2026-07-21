# Social Wave production pipeline — the stage map (v0.1, 20/07/26)

*How work flows from idea to published content, who owns each stage, and where the AI editing
system slots in. Compiled from Joseph's overview + the ClickUp Videographer Workflow Loom
(20/07/26). This is the umbrella doc — each stage gets its own SOP as they're written.
Primary output = YouTube long-form; the same chain feeds ads; organic socials are repurposed
from the long-form.*

> **Two views of the same pipeline:** this doc = the **ClickUp PM view** (statuses, gates,
> ownership). `scripted-youtube-explainer-workflow.md` = the **creative view** (the 4-phase Figma
> board with parallel tracks). Same stages, different lens — keep them in sync.

## The stages

| # | Stage | Owner | Output / hand-off | SOP |
|---|-------|-------|-------------------|-----|
| 1 | **Pre-production** | Cass or Tayla | Locked script + videographer brief + editor brief (TN Sketch process) | exists as skills (tn-sketch-process, youtube-production-brief) |
| 2 | **Production** | Videographer | Raw footage, filmed to the brief on the scheduled date | videographer brief per project |
| 3 | **Wrangling + editor prep** | **Videographer** (not a separate post role) | Footage on SW server/Dropbox · Premiere project built with footage imported + linked · base colour grade · basic audio treatment | ⏳ technical SOP pending (folder naming, grade process, audio prep detail) |
| 4 | **QC gate** | Noel, Ahmed or Harvey (project lead) | Reviews the Premiere project, "converts" it, passes to editor with briefs + script consolidated | — |
| 5 | **Edit** | Editor | Assembly cut → full edit | `premiere-editor-conventions.md` (from the editor training Looms) |
| 6 | **Distribution** | — (unassigned for now) | YouTube publish · organic reels repurposed from the long-form · winners feed ads (C##) · dedicated ad creatives (AC##) | reel workflow (repo CLAUDE.md) · ad-cut skill |

## The ClickUp layer (PM spine)

### Task anatomy (set by the pre-production lead, read by everyone)

- A video = one **pillar task** duplicated from Templates and renamed
  `<client code> <video ##>` (e.g. `230 LM 01`); **reel subtasks duplicate with it**.
- Stage fields on the task: **ClientStage** · **ContentType** (LongForm/ShortForm) ·
  **ProductionStage** (pre-prod lead's field) · **FilmingStage** (videographer) ·
  **DesignStage** (designer) · **06 Edit Stage** (editor).
- Link fields that must ALL be populated before pass-off: **Ideas and Briefs link** (the TN
  sketch Google Doc — videographer + editor briefs live as tabs in it, written AFTER the client
  approves the sketch) · **Script link** · **Internal thumbnail link** (Dropbox) · **Frame.io
  thumbnail link** (uploaded by the pre-prod lead once approved) · **Distribution date** (set
  early; treat as locked once the task moves down the pipeline).
- ClickUp comments are the guidance system: every stage change posts the instructions for the
  next step. Client review loops (idea, script, package) all follow the same closed loop:
  send up → `Client Revisions` if needed → revise → resend or bypass.

### Pre-production lead side — **ProductionStage** field (Cass/Tayla)

`Ideation` → `Client Idea Review` ⇄ `Client Revisions` → `Research and Writing` →
`Client Script Review` ⇄ `Client Revisions` → `Delegate Film and Design` → `Final Checks` →
`Handoff`

- Due dates: first set = client script-approval target; reset after idea approval to reflect
  the filming cut-off.
- `Delegate Film and Design`: assign the designer, and assign the videographer **only once the
  filming session is scheduled and entered in the Filming Date field**. Good moment to populate
  the distribution package fields (titles, description, captions, reel captions from the script
  doc) so everything lives in ClickUp.
- Design runs on its own DesignStage loop (internal review → client review → closed, Frame.io
  link embedded before closing). The videographer stage can be bypassed straight to Final
  Checks if the lead has the footage/project already.
- **`Final Checks` = the handoff QC**: confirm the Social Wave Dropbox folder path, every link
  field populated, distribution date set, reel subtasks complete (reel briefs/scripts/thumbnails
  where they exist). Set reel subtasks to handoff first (→ "passed to editor"), then the pillar
  task → status `Passed Editors`, ProductionStage closed, and the task appears on the
  post-production list for the pod assignee to pick up.
- Reference cadence: promo reel distributes ~2 working days after the pillar video.

### Videographer side — **04 Filming Stage** field

`Assigned` → *(film on the Filming Date)* → `Wrangling Footage` → `Footage Ready`
(outliers: `Footage Error`, `Upload Error`)

- On assignment: inbox notification → read the task comment; **checking the Videographer Brief
  (Ideas and Briefs link, left tab) is mandatory.**
- `Wrangling Footage` = footage in hand; covers upload/sync, Premiere project setup, colour
  grading. An ETA comment is expected when this status is set.
- `Footage Ready` = Premiere project ready for the project lead; the **folder path is posted in
  the task comments** at this point.

### Editor side — **06 Edit Stage** field (+ **06.1 Internal Video Link**)

Two task types: **pillar edits** (the YouTube video) and **reels** (subtasks; same structure,
different automation prompts). Flow for both:

`Assigned` → `Editing` → *(drop Dropbox link in 06.1)* → `Internal Video Review`

- On assignment the task comment links the **Script Link** (from the pre-production lead) and
  the **Ideas and Briefs link** → the TN sketch, with the **editor brief** on its left-hand side
  (not yet templatized). No brief present → confirm video INTENTION + STYLE with the production
  lead before cutting anything.
- **The "did you read the brief" checkbox is a hard gate.** Ticking it is required BEFORE
  setting the stage to `Editing`; skipping it trips an automation that resets the stage to
  `Assigned` and notifies the leads. Reels may not have a brief (often just a thumbnail + end
  CTA) — check anyway, then tick the box.
- Set `Editing` only when actually starting. Due date + **time estimate** are set by the
  production lead (scaled to editor skill + video intensity; reference: ~2h for a reel).
  If V1 runs over the estimate, reply to the thread with the extra time taken.
- `Internal Video Review` requires the Dropbox link in **06.1 Internal Video Link** first —
  moving stage without a link trips a reminder and the lead won't review.
- **Revision loop (internal and client revisions, identical):** notified → estimate the time →
  review the linked feedback → revise → re-drop the new link in 06.1 (it's emptied each round)
  → set `Internal Video Review` again.
- From review, the project lead disposition is one of: needs internal revision · approved but
  reels pending · approved + reels approved (ready for client) · client-seen, links updated.
  Editor hand-off point = `Internal Video Review`; then move to reels or the next task.

## Where the AI editing system slots in

- **Stage 3/4 (prep):** highly automatable via the Premiere MCP bridge (import, bins per the SW
  convention, base grade/LUT, the audio-enhance round-trip). Goal: videographer wrangles files,
  machine builds the project.
- **Stage 5 (edit):** `rough-cut` automates the assembly cut; the editor starts from a verified
  assembly instead of raw footage (the 1.5-2h → 20-30min claim lives here). Machine output must
  conform to `premiere-editor-conventions.md` so editors receive timelines that look hand-prepped.
- **Stage 6 (distribution):** `reel-cut`/the proven reel workflow for organic; `ad-cut` for AC##
  ad variants; organic winners graduate to paid (see TradesFormation omnipresence plan).
- **Automation hook (future):** ClickUp `Footage Ready` + folder path comment = a machine-readable
  trigger to kick off the assembly pipeline. Claude has ClickUp MCP access — worth piloting once
  the manual flow is stable.

## Open gaps (fill as SOPs/trainings land)

- [x] ~~Stage 3 technical SOP~~ → DRAFTED 20/07/26: `wrangling-and-project-setup.md` (from the
      ~2yr-old Video Editing Workflow Loom; folder naming, multicam sync, grade, reframe, split,
      handoff). Cross-checks still open in that doc (folder names, ClickUp status reconciliation,
      grade ownership, 25fps, per-client LUT).
- [ ] Stage 4: what the project lead's "convert" step checks
- [x] ~~Stage 1/2 SOP pointers~~ → RESOLVED 20/07/26: briefs are tabs in the TN sketch Google
      Doc, linked via Ideas and Briefs on the task (pre-production LEADER workflow Loom)
- [ ] Ads branch: how ad projects enter this pipeline (same ClickUp flow? separate list?)
- [ ] Editor brief templatization (flagged as in-progress in the editor workflow Loom)

## Run log
- 20/07/26 — v0.1 drafted from Joseph's overview + 3 Looms (editor training 00/01, videographer PM workflow 02).
- 20/07/26 — v0.2: owners corrected (Cass/Tayla pre-prod; Noel/Ahmed/Harvey QC gate); editor-side
  ClickUp flow added from Loom "04. ClickUp PM Editor Workflow" (06 Edit Stage, 06.1 link gate,
  brief checkbox gate, revision loop, pillar vs reels subtasks).
- 20/07/26 — v0.3: pre-production LEADER workflow added from Loom 01 (task anatomy, ProductionStage
  flow, Final Checks handoff, client review loops); stage-1 owner detail confirmed.
