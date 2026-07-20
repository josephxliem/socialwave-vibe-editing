---
name: ad-cut
description: >
  THE paid-ads variant machine. Turns footage + ad scripts into a named MATRIX of finished
  Meta ad variants (hook × body × CTA × aspect ratio) instead of one-off organic clips.
  Two footage modes picked at the start. MODE A — SCRIPTED SHOOT — talent read hooks/bodies/CTAs
  to camera (messy takes fine); each script component is forced-aligned and cut via script-cut,
  then assembled combinatorially. MODE B — MINE — mine an existing long-form source (webinar,
  VSL, podcast, testimonial call) for ad-shaped verbatim moments that can serve as hooks/bodies/
  CTAs, then assemble the same way. This skill ORCHESTRATES — it owns the variant matrix,
  component cutting order, naming, and the ad-specific audit gate, then POINTS TO the standalone
  skills for each capability: source-intel (footage analysis), script-cut (precision component
  cutting), horizontal-to-vertical (reframing), caption-clips (captions), render (manifest build),
  plus the standard audit agents at delivery. Scripts come from the meta-ads-copywriter /
  lo-fi-ad-builder skills or are user-supplied. Trigger keywords: ad cut, /ad-cut, make ads from
  this footage, cut ads, ad variants, hook variants, build the ad matrix, turn this shoot into ads,
  make Meta ads from this, ad machine, cut the hooks, assemble ad variants.
---

# ad-cut — footage + scripts → a matrix of finished ad variants

> **STATUS: v0 DRAFT (2026-07-20).** Pipeline skeleton is real (every referenced skill exists and
> is the single source of truth for its capability). Sections marked **⏳ SOP-PENDING** get
> fleshed out from Joseph's ads SOPs as they land. Do not treat SOP-PENDING defaults as canon —
> ask when one matters to the current run.

> **📦 PLUGIN PATHS.** Ships inside the **`vibe-editing`** plugin. `${CLAUDE_PLUGIN_ROOT}` = the
> plugin install dir, same convention as `edit`. This skill never duplicates another skill's
> instructions — it sequences them.

## What this makes (and how it differs from /edit)

`/edit` and `reel-cut` answer: *"what are the best moments in this footage?"* → organic clips.
`/ad-cut` answers: *"make this footage say these scripts, in every combination we want to test"*
→ paid creative. The unit of output is not a clip, it's a **variant**:

```
variant = HOOK(h) + BODY(b) + CTA(c), rendered at RATIO(r), captioned, audited, named
```

> **Omnipresence context (TradesFormation build plan + briefing, 20/07/26).** SW ad campaigns
> run two creative pools. **C## content clips** = organic winners reused as Awareness/Traffic
> ads (look like normal reels, minimal graphics, no hard CTA) — those come from the ORGANIC
> pipeline (`reel-cut`/`edit`), not this skill; organic performance decides the winners, Tony
> loads them. **AC## ad/sales creatives** = dedicated Leads-campaign creative (VSL cuts,
> testimonials, case studies, offers) — THAT is what ad-cut manufactures. Guardrail from the
> plan: **never reuse organic C## clips as Leads creatives** (cannibalises Campaigns 1-2).
> Weekly rhythm: kill losers, top up winners, retest minus past winners.

Deliverable = every requested combination, plus a `variant-manifest.csv` that maps each export
back to its components, so ad performance data can be traced to the exact hook/body/CTA that
produced it.

## 🔒 NON-NEGOTIABLES — verify before EVERY delivery, never silently skip

1. **Verbatim guardrail.** Every cut word was actually spoken in the source footage. Forced
   alignment (script-cut) is the mechanism; never splice syllables or reorder words inside a
   sentence to fabricate a line the speaker didn't say. If a requested script line has no
   spoken match, it goes in the run report as UNCUTTABLE — it does not get faked.
2. **Hook lands immediately.** The hook's first spoken word starts within the first
   0.5s of the variant; the hook must be fully delivered inside the first 3 seconds
   (⏳ SOP-PENDING: exact threshold from Joseph's ads SOP; 3s is the working default).
3. **Safe zones per placement.** Captions and any burned-in text stay inside Meta's safe areas
   for the target ratio (9:16 Reels/Stories leave top ~14% and bottom ~20% clear;
   ⏳ SOP-PENDING: confirm against the SOP's template).
4. **AU compliance flags.** Before export, scan all on-screen/spoken claims for the compliance
   categories flagged in the copy skills (income claims, guarantees, before/after, finance/health
   claims). Flag, never self-approve — compliance calls are Joseph's.
5. **No silent matrix pruning.** If a requested combination can't be built (component uncuttable,
   audio unusable), it's listed in the run report with the reason. The delivered set is never
   quietly smaller than the requested set.
6. **Naming is law.** Every export follows the variant naming convention (below) exactly —
   Meta upload and reporting depend on it.

## Inputs (gather at kickoff — ask ONE question at a time if missing)

1. **Footage** — local file(s) or fetch via `footage-fetch`. Declare MODE A (scripted shoot)
   or MODE B (mine) — infer from the footage if obvious, confirm if not.
2. **Ad scripts** — the component sheet: hooks (H1..Hn), bodies (B1..Bn), CTAs (C1..Cn).
   Accepted sources: output of `meta-ads-copywriter`, a user-pasted doc, or (MODE B) "mine the
   components from the footage" with an angle brief.
3. **Matrix spec** — which combinations and ratios. Default: all hooks × 1 body × all CTAs at
   9:16, i.e. hooks are the primary test variable (⏳ SOP-PENDING: Joseph's testing doctrine —
   confirm whether hook-first testing is canon).
4. **Client/brand profile** — caption style, fonts, colours, logo, safe-zone template:
   `brand/<client>/` (same convention as caption-clips; ⏳ SOP-PENDING: per-client ad templates,
   end-cards, logo stings).

## The run (agent steps)

### 0. Project scaffold
Create the project folder using the standard numbered structure (mirrors bins if a Premiere
round-trip is requested):
```
ads/active/<client>-<concept>-<yyyymmdd>/
  01_footage/  02_audio/  03_components/  04_variants/  05_exports/  06_scripts/  07_notes/
```

### 1. Ingest + transcribe
`long-form-ingest` / `footage-fetch` conventions: normalize footage, produce
`transcript_ts.txt` + `transcript_words.json` (word-level timestamps are required — script-cut
depends on them).

### 2. Component acquisition — the mode fork
- **MODE A (scripted shoot):** for each script component (H1, H2, B1, C1, …) run `script-cut`
  with the component's exact words against the take(s). Best take per component: cleanest
  alignment score, no clipped words, energy consistent with neighbours
  (⏳ SOP-PENDING: take-selection criteria from the SOP; alignment-cleanliness is the default).
- **MODE B (mine):** read the transcript and mine for ad-shaped verbatim spans per the angle
  brief — hook-worthy openers, proof/story bodies, natural CTA lines. Same mining discipline as
  `edit`/reel-cut (self-contained, no dangling references, payoff intact), but selected for the
  hook/body/CTA role, not for standalone virality. Then cut each selected span via `script-cut`.
Each cut component is rendered as a standalone segment into `03_components/` and named
`H1.mp4`, `B2.mp4`, `C1.mp4` etc., with a `components.json` recording source timecodes.

### 3. Component gate (before any assembly)
Play-test every component: clean in/out, no clipped first/last word, loudness within −1 dB of
siblings (components from different takes WILL mismatch — level them now, not after assembly).
A component that fails here fails every variant that uses it — fix or recut before proceeding.

### 4. Assemble the matrix
For each requested (h, b, c): concatenate components (hard cuts by default;
⏳ SOP-PENDING: transition/j-cut policy) into `04_variants/<variant-id>.mp4` (16:9 master).
Manifest-driven via `render` where the manifest fits; otherwise ffmpeg concat with re-encode
gate (`encode_gate.py` conventions from `lib/_shared`).

### 5. Reframe per ratio
`horizontal-to-vertical` for 9:16 (face-tracked). **9:16 is the confirmed SW default — no
square/1:1 mix** (Kan, briefing 20/07/26: "9:16 as usual"). Only produce other ratios if the
brief explicitly orders them; the tracking data supports 1:1/4:5 crops when it does.

### 6. Captions
`caption-clips` with the client's ad caption style. Ad-specific overrides: captions ON by
default (sound-off viewing), hook text may double as an on-screen title card
(⏳ SOP-PENDING: lo-fi vs branded caption treatment per client).

### 7. Ad audit gate
Run the standard audit agents (`sf-audit`, `audit-visual`, `audit-audio`, `audit-captions`)
PLUS the ad checks: non-negotiables 1–4 above, per variant. Any FAIL → fix and re-audit;
anything unfixable → run report, not export.

### 8. Export + manifest
Creative IDs follow the ad-account convention (TradesFormation plan §5): **AC##**, sequential,
matching the numbering already in the client's ad account — campaign/audience suffixes like
`AC03-C3-BR` (= ad creative 03 · Campaign 3 · Broad) are added at ad-name level by the media
buyer, not baked into the file. Filenames carry the component recipe so performance traces back:
```
{AC##}_{client}_{H#-B#-C#}_{ratio}_v##.mp4
e.g. AC07_TRADES_H2-B1-C1_9x16_v01.mp4
```
Export finals into `05_exports/`. Write `variant-manifest.csv`: AC##, hook text (first 60
chars), body id, CTA text, ratio, duration, source timecodes, audit status, compliance flags.
The manifest is the hand-off to the media buyer (Tony) — it must let him name ads
`AC##-C#-{RT|BR}` without opening a single file.
(⏳ SOP-PENDING: confirm the next free AC number per client account before each run.)

### 9. Hand-off + SOP update (never skip)
- `RUN-REPORT.md` in `07_notes/`: what was requested, what was delivered, UNCUTTABLE lines,
  pruned combinations + reasons, compliance flags for Joseph's review.
- Update `documentation/ads-workflow-SOP.md`: what worked, what needed manual correction, what
  should change next run. This is what makes the machine self-evolving — a run that doesn't
  update the SOP is an edit, not a system.

## What this skill does NOT do

- ❌ Write ad copy or scripts (→ `meta-ads-copywriter`, `lo-fi-ad-builder` for statics)
- ❌ Upload to Meta or name campaigns (→ ads upload workflow; manifest is the hand-off)
- ❌ Organic clips/reels (→ `edit`, `reel-cut`, `listicle-short`)
- ❌ Motion-graphics/branded promo videos (→ `promo`)
- ❌ Approve compliance-flagged claims (→ Joseph, always)

## ⏳ SOP-PENDING master list (fill as Joseph's SOPs land)

- [ ] Hook timing threshold + hook checklist from the ads SOP
- [ ] Testing doctrine: which matrix dimensions get tested first (hooks vs CTAs vs formats)
- [ ] Per-client brand ad templates (end-cards, logo stings, caption styles, safe-zone overlays)
- [x] ~~Ratio/placement order sheet~~ → RESOLVED 20/07/26: 9:16 only, SW-wide default (briefing)
- [ ] Take-selection criteria on scripted shoots
- [ ] Transition/j-cut policy between components
- [x] ~~Creative naming alignment~~ → RESOLVED 20/07/26: C##/AC## account convention (step 8)
- [ ] B-roll / overlay policy (does v1 support B-roll slots, or talking-head only?)
- [ ] Throughput target: briefing benchmark = ~20-30 min human time per clip (vs 1.5-2h manual),
      ~10 live creatives per campaign sourced from 2-3 different recordings — validate on run 1
