# Scripted YouTube Explainer — the master workflow (v0.1, 20/07/26)

*The canonical end-to-end workflow for SW's scripted YouTube explainer videos, reconstructed from
the "Workflow for Creating Scripted YouTube Explainer Videos" Loom (~28 min) + its Figma board
("Scripted YouTube Explainer Workflow"). The board is the organising principle: **4 phases as
columns, with parallel tracks branching inside each phase**. This is the creative/content view of
the pipeline; `production-pipeline.md` is the ClickUp PM view of the same thing — read both.*

> **Board shape:** `#1 Pre-Production → #2 Production → #3 Post-Production → #4 Distribution`,
> colour-coded nodes connected by arrows, with side-branches for work that runs in parallel.
> Distribution loops back to Pre-Production (performance → next round's topics).

---

## #1 — PRE-PRODUCTION

**Main track (strategy → script):**
1. **IP extraction + strategy + topic ideation** — strategist/writer calls the client, learns
   the client's (and their audience's) pain points, researches what topics perform in the field
   on YouTube, extracts the client's unique IP so content is differentiated.
2. **Client approves topic ideation.**
3. **Research + scripting** (writer). For research-heavy videos, the writer also **compiles
   research/source links** so editors can cite them and build the visuals.
4. **Client approves scripts** (revision loop with the writer).

**Parallel track (creative direction — runs alongside scripting, Joseph heavily involved):**
- **Design the style frames / art direction.** Client sends brand guidelines/logos; if none,
  build art direction off their website. Standard frame formats (reused across most videos):
  main titles, lower thirds, one-line / two-line, title/break pages, screen lists + full-screen
  lists, text-behind-subject, text overlays, full-screen photos, screen recordings + inserts,
  icon animations + an icon library, end screen (socials). Plus **custom frames** per client
  (e.g. a suburb-countdown frame with suburb + median price). Built in Photoshop/Illustrator.
- **Joseph gives feedback → approved.**
- **Editors build the asset library** — turn the approved designs into reusable **Premiere
  templates** (so formats are reused, not rebuilt each video).
- **Editors build a general assets library** — music by mood, SFX, dot-point/pop-on effects,
  transitions, reusable MOVs, etc.

---

## #2 — PRODUCTION

- **Batch film** with the client — one day, **6-8 videos** (script 4-6+ ahead), = 2-3 months of
  content, so travelling clients film rarely.
- **Multicam: A-cam** (main angle, client reads teleprompter to camera) + **B-cam** (alt angle,
  also hides jump cuts).
- **Standardised kit for easy matching:** same bodies (Sony A7S), same lens make (Tamron ~24-70
  or 17-28), **same colour profile on both cams** — keeps colour simple, minimal grading.
- **Wrangle within 24h** of the shoot (in-studio, or wrangle from home + return cards). Sync
  files, set up Premiere projects. → detail in `wrangling-and-project-setup.md`.
- **Videographer does a light grade + light sound treatment only** — because *only they know the
  shoot conditions* (under-exposed B-cam vs A-cam, echo from an un-carpeted set) and because some
  offshore editors don't have colour-calibrated monitors. Not extensive — just enough that the
  editor doesn't have to worry about it.
- *(Videographer doing the assembly cut = aspiration, not current — time constraint on shoot days.)*

---

## #3 — POST-PRODUCTION

**Main track (edit):**
1. **Assembly cut** (editor). Easy for scripted content; the videographer leaves **editing notes
   in ClickUp** flagging improvised / off-script / added parts. They film **continuously 30-40
   min on both cams** (easy sync) and coach the client through mistakes on camera — so they
   **don't run TimeBolt** for most clients (it would strip the verbal instruction the editor uses
   to pick best takes). Bonus: the assembly cut is the editor's **first close read of the
   script** (helps offshore comprehension on technical topics — accounting, investing, etc.).
2. **Storyboarding / annotations** (editor; project lead helps for new/complex clients):
   - **Detailed storyboard** (research-heavy videos): script part · allocated visuals · **priority
     (high/med/low)** · source links · what to highlight. Priority lets a tight deadline ship the
     high-priority graphics first.
   - **Annotations** (simpler default): highlight the essential parts of the script, tag each
     against a start-frame format (title page, keyword, break page, text overlay…), plan what to
     do per important beat. Gauges how visual-dense the video is and lets the editor pace to the
     deadline. **Project lead reviews the annotations** and steers priorities *before* the first
     draft — so the first draft lands close to final.
3. **Source assets + design keyframes** — "keyframes" = anything custom (full-screen animations),
   plus specific SFX/music for the video.
4. **Apply animation, motion graphics, sound design** — assembly + grade + sound in **Premiere**;
   motion graphics in **After Effects**, **dynamic-linked** so changes update live.
5. **QC + feedback** (project lead, **Frame.io**): timestamped comments, draw-over, editor
   comments each note as a checklist (editor can't mark complete — the lead does). Aim: **≤1
   internal revision**. Feedback is prescriptive (exact wording) because of offshore language gaps.
6. **Client revisions — 2 rounds available, aim to nail it in the first.**

**Parallel tracks (run during the feedback loop):**
- **Reels** — **usually ≥2 per long-form** (longer videos produce more). The **post-production
  lead finds the reel moments** from the long-form; editor cuts. Hook cut vertical + strong
  snippets. Drives social → YouTube traffic.
- **Thumbnail** — designer designs it; project lead does packaging research (ChatGPT + YouTube
  outlier research) and pairs it with the title.
- **Copywriting** — YouTube description (links + timestamps) + reel captions for socials.
- All of it (video + captions + reel) → **client approval**.

---

## #4 — DISTRIBUTION

- **Post to all relevant platforms** — YouTube + IG, TikTok, Facebook, LinkedIn; sometimes an
  email to the client's database.
- **Assess performance** (strategist/project lead) → **feeds the next round's topic selection**
  (double down on what worked, drop what didn't). ↩ loops back to Pre-Production.

---

## Where the AI editing system plugs into THIS workflow

| Board node | AI system asset |
|------------|-----------------|
| Pre-prod: asset library / Premiere templates | the brand/caption presets + template kit in the repo |
| Production: wrangle + project setup | `wrangling-and-project-setup.md` (automation target) |
| Post: **assembly cut** | `rough-cut` skill (the core automation) |
| Post: **annotations** (script → visual plan) | AI-assistable: script + start-frame formats → draft annotation pass for the editor to refine |
| Post: **reels** (hook cut vertical + snippets) | `reel-cut` / the proven reel workflow |
| Post: captions | `caption-clips` |
| Distribution / ads branch | `ad-cut` (AC##) + organic winners (C##) |

**The through-line:** this is the same pipeline as `production-pipeline.md` (ClickUp view) and the
same engine as the organic/ads work — one machine, viewed three ways. The scripted-explainer
board is the creative spine; the assembly cut and reels are where automation already exists, and
wrangling + annotations are the next targets.

## Cross-checks for Joseph
- [ ] Board node labels reconstructed from narration (720p board text wasn't fully legible) —
      correct any step names / missing nodes.
- [ ] Is "annotations vs detailed storyboard" still the split, and is the project-lead annotation
      review still standard? (Joseph: "not sure" — leave as documented until confirmed.)
- [x] Reels: **usually ≥2 per long-form** (more for longer); **post-production lead finds the
      moments** (20/07/26 interview).

## Run log
- 20/07/26 — v0.1 from the Scripted YouTube Explainer Workflow Loom + Figma board.
