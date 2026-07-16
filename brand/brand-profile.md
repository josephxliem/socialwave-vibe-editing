# Social Wave — Brand Profile

This file records the brand answers from the setup interview. Claude uses it to wire the
Vibe Editing pipeline (captions, logo, music, clip open/close, editing preferences).

## 1. Brand name
Social Wave

## 2. Logo
- **Primary / current logo (use on end-cards):** blue "SOCIAL" block + coral brush-script "WAVE".
- **Alternate (newer, on merch):** blue→coral gradient wave mark with "SOCIALWAVE" wordmark.
- **File status:** PENDING — user to drop the real image file into `brand/logos/`. Seen as pasted
  images only; not yet saved to disk. Add anytime, then re-run to stamp end-card.

## 3. Caption font + look  (from 4 reference screenshots — "use these")
- **Font:** heavy sans, ALL-CAPS on emphasis words. Montserrat Black/Extrabold (kit default) is a match.
- **Base words:** WHITE, as-spoken case, Medium/Bold weight.
- **Emphasis word (one punch word per line):** BIG + ALL-CAPS + brand color, alternating:
  - **Social Wave BLUE (cyan):** ~`#1CB5E5` — e.g. MORE, ALGORITHM, EMPIRES
  - **Social Wave CORAL:** ~`#F58A7D` — e.g. RESULTS, YOUTUBE
- **Alternation:** consecutive punch words alternate blue ↔ coral for contrast.
- **Shadow:** subtle drop shadow (kit's locked premiere shadow is a match).
- **Position:** mid-frame (kit default ~50%).
- **Watermark:** brush "Social Wave" logo shown small on-frame (needs logo file — see §2, pending).
- **Wiring plan:** in caption preset, set emphasis/payoff color palette to {blue,coral} alternating,
  uppercase emphasis words, keep base white. (default guest-yellow replaced by brand blue/coral.)

## 4. Music
- **None for now** (captions + clean speech only). Subject to change.
- Wiring plan: music OFF by default. To enable later: drop royalty-free tracks in `brand/music/`
  and re-run — user must own/clear rights (no copyrighted songs).

## 5. Topics + how a clip should OPEN and END
- **Topics (flexible for now):** currently editing for **Kan's personal brand** — YouTube +
  business strategy from an **agency-owner** POV. Lean toward **MINDSET / principles**, NOT
  tactical how-to. (Will broaden later.)
- **OPEN / hook = BOLD CLAIM.** Hard rules:
  - Clip must be **self-contained** — works with **no prior context**.
  - If context IS needed, add it as **on-screen TITLE TEXT** (top of frame), not by extending the cut.
  - Must **grab instantly**: within the first beat the viewer knows *what* they're watching and
    *why it's worth it* (clear value signal up front).
- **END:** editor's judgment, but **default = end clean / on a punchline** (the payoff). Avoid
  trailing chatter. CTA endings allowed occasionally if it fits.
- Wiring plan: encode into `skills/edit/prompts/clip_select.md` (selection = bold self-contained
  mindset claims) and ensure title-text step is available for context. Refine later.

## 6. Editing preferences
- **Pacing = content-dependent (dynamic):**
  - **Relaxed** during a point / story (let it breathe).
  - **Punchy** on hard statements.
  - **Hook is ALWAYS punchy** (non-negotiable).
- **Clip length: 30–75 seconds. HARD FLOOR: never under 30s.**
- **Captions: always ON.**
- **Face-tracking: required** (9:16 face-tracked framing).
- **Avoid:** NO emojis in captions. NEVER cut mid-sentence.
- Wiring plan: set min-duration gate = 30s, target 30–75s; enforce sentence-boundary cuts;
  captions + face-track always on; strip emojis from caption text; pacing guidance in clip_select.
