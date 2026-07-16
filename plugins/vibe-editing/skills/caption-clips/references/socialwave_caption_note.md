# Social Wave — caption director BRAND OVERRIDE

Apply this on top of the default spice director rules when the active preset is
`spice_socialwave` (Social Wave brand clips). It changes ONE thing: how COLOR is used.

## The one change: COLOR = EMPHASIS, not voice
The default director reserves color for *voice* (white = speaker, yellow = guest) and does
emphasis with weight/size only. Social Wave instead uses **color as the emphasis axis**, matching
the brand's reference clips.

Rules for a single-speaker Social Wave clip:
- **Base words = WHITE** (`c:"speaker"`), as-spoken case, Medium/Bold weight (unchanged).
- **The one biggest PAYOFF word per caption line** (the punch word — the noun/verb/number the line
  turns on) gets:
  - a **brand accent color**, `c:"brand_blue"` or `c:"brand_coral"`,
  - **ALL-CAPS**,
  - a **size bump** (peak/strong) + heavy weight (Extrabold/Black).
- **ALTERNATE** the accent line-to-line: if the last painted punch word was blue, the next is coral,
  and so on. Two consecutive punch words should not share a color.
- Only **one** accent-colored punch word per line (occasionally the whole 1-2 word line). Never paint
  a whole sentence an accent color — that kills the contrast. White carries the line; the accent pops.
- **Numbers / money** may take an accent color (they're natural punch words) — still alternate.

## Hard rules (unchanged, restated)
- **NO EMOJIS** in caption text, ever. Strip them.
- If a clip has a REAL second speaker (Q&A guest / caller), fall back to the default voice model for
  that person's turns: their whole turn = yellow (`c:"guest"`). Brand blue/coral is for emphasis in
  the main speaker's own narration.

## Palette (from logo + reference caption screenshots)
- `brand_blue`  = `#1CB5E5` (Social Wave cyan)
- `brand_coral` = `#F58A7D` (Social Wave coral)

Reference look: white base, alternating blue/coral ALL-CAPS punch words — e.g. "it will get shown to
**MORE**," / "YouTube's **ALGORITHM** has one job" / "**EMPIRES** using **YOUTUBE**".
