#!/usr/bin/env python3
"""
rebuild_captions_from_srt.py — Premiere round-trip for Social Wave captions.

WHY: Premiere can EDIT caption text + timing but cannot store/export the per-word
brand styling (blue/coral/yellow, weight ladder, size, italic). Adobe never exposed
caption tracks to scripting, so we can't read them back automatically — the editor
exports a plain SRT sidecar. This tool takes that edited SRT (the new TEXT + TIMING
truth) and re-applies the APPROVED per-word styling from a "style master" render,
then bakes a fresh transparent ProRes-4444 caption overlay that drops straight back
onto the Premiere timeline.

Editor owns TIMING + WORDING (precise, visual, one pass). Kit owns the LOOK.

  edited plain SRT  +  style master (transcript.json + director_stream.json)
        │                        │
        └── word-align (difflib) ┘
                    │  carry color/weight/size/italic onto matched words
                    ▼
   new spice_norm.json + transcript.json + director_stream.json
                    ▼   generate_spice.py --alpha
             new *_ALPHA.mov  (2160x3840 yuva, exact look, editor's timings)

Usage:
  rebuild_captions_from_srt.py \
      --edited-srt   /path/EDITED.srt \
      --master-dir   .../caption_gen_cache/505eaacefd794e6e \
      --dims-ref     .../SocialWave_captions_ALPHA.mov \
      --preset       .../presets/spice_socialwave.json \
      --out          .../SocialWave_captions_ALPHA_v2.mov \
      [--work DIR] [--dry-run]
"""
import argparse, json, re, subprocess, sys, difflib, tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent
TAGRE  = re.compile(r'</[^>]+>')
WORDRE = re.compile(r'(?:<font color="#([0-9A-Fa-f]{6})">)?((?:<[bi]>)*)([^<\s]+)')


def norm(w: str) -> str:
    """Comparison key: lowercase, strip surrounding punctuation/quotes."""
    return w.strip(' ,.:;!?"“”‘’\'').lower()


def srt_time(t: str) -> float:
    t = t.strip().replace('.', ',')
    h, m, rest = t.split(':')
    s, ms = rest.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt_words(path: Path):
    """Edited SRT -> flat list of {word, start, end, cue, cue_start, cue_end}. Tags
    stripped. Cue span is distributed across its words proportionally to word length
    (+1) so multi-word cues get sane per-word timings; single-word cues keep the cue
    span exactly. cue_start/cue_end are carried so unchanged cues can be snapped back
    to the master's exact per-word timings later (identical round-trip)."""
    raw = path.read_text(encoding='utf-8')
    words, cue = [], 0
    for block in re.split(r'\n\s*\n', raw.strip()):
        L = [x for x in block.splitlines() if x.strip() != '']
        if len(L) < 2 or '-->' not in L[1]:
            continue
        s_str, e_str = L[1].split('-->')
        s, e = srt_time(s_str), srt_time(e_str)
        text = TAGRE.sub('', ' '.join(L[2:]))
        toks = [m.group(3) for m in WORDRE.finditer(text)]
        if not toks:
            continue
        weights = [len(t) + 1 for t in toks]
        tot = sum(weights)
        acc = s
        for tok, wt in zip(toks, weights):
            dur = (e - s) * (wt / tot)
            words.append({'word': tok, 'start': round(acc, 3), 'end': round(acc + dur, 3),
                          'cue': cue, 'cue_start': round(s, 3), 'cue_end': round(e, 3)})
            acc += dur
        words[-1]['end'] = round(e, 3)  # snap last word to cue end
        cue += 1
    return words


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--edited-srt', type=Path, required=True)
    ap.add_argument('--master-dir', type=Path, required=True,
                    help='caption_gen_cache dir with the APPROVED transcript.json + director_stream.json')
    ap.add_argument('--dims-ref', type=Path, required=True,
                    help='video whose W/H/duration to match (the approved ALPHA.mov)')
    ap.add_argument('--preset', type=Path,
                    default=SCRIPT.parent / 'presets' / 'spice_socialwave.json')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--work', type=Path, default=None)
    ap.add_argument('--dry-run', action='store_true',
                    help='write the JSON inputs + report alignment, skip the render')
    a = ap.parse_args()

    # Align in the DIRECTOR'S index space: director_stream keys index spice_norm.json,
    # which can be SHORTER than transcript.json (numeric merges like "million dollars" ->
    # "$1M"). Aligning against transcript.json shifted every style after the merge point
    # by one word. spice_norm carries the same timings, so use it when present.
    _norm_p = a.master_dir / 'spice_norm.json'
    _tx_p   = a.master_dir / 'transcript.json'
    master_tx = json.loads((_norm_p if _norm_p.exists() else _tx_p).read_text())['words']
    director  = json.loads((a.master_dir / 'director_stream.json').read_text())
    d_words   = director.get('words', {})

    edited = parse_srt_words(a.edited_srt)
    if not edited:
        print('ERROR: no words parsed from edited SRT', file=sys.stderr); return 1

    m_keys = [norm(w['word']) for w in master_tx]
    e_keys = [norm(w['word']) for w in edited]

    # Word-level alignment: carry master per-word styling + (on unchanged runs) exact
    # master timings onto the edited stream.
    sm = difflib.SequenceMatcher(a=m_keys, b=e_keys, autojunk=False)
    e2m = {}            # edited index -> master index (for 'equal' blocks)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for off in range(i2 - i1):
                e2m[j1 + off] = i1 + off

    EPS = 0.035
    # Cue-level snap: a cue whose words all map to a CONTIGUOUS master run and whose
    # start/end match that run's master boundaries (within EPS) is UNCHANGED -> copy
    # the master's exact per-word timings so it round-trips identically. Any other cue
    # is treated as edited and keeps the editor's (redistributed) timings.
    from collections import defaultdict
    cue_words = defaultdict(list)
    for j, ew in enumerate(edited):
        cue_words[ew['cue']].append(j)
    snap = {}  # edited index -> master index whose timing to copy verbatim
    for cid, idxs in cue_words.items():
        ms = [e2m.get(j) for j in idxs]
        if any(m is None for m in ms):
            continue
        if ms != list(range(ms[0], ms[0] + len(ms))):   # not contiguous run
            continue
        cs, ce = edited[idxs[0]]['cue_start'], edited[idxs[0]]['cue_end']
        if abs(master_tx[ms[0]]['start'] - cs) < EPS and abs(master_tx[ms[-1]]['end'] - ce) < EPS:
            for j, m in zip(idxs, ms):
                snap[j] = m

    # Carry the master's per-word styling through UNCHANGED. Size/weight uniformity
    # within a cue is owned downstream by generate_spice's per-cue size logic (which
    # reproduces the approved look), so we do NOT second-guess it here.
    new_tx, new_norm, new_dir = [], [], {}
    changed_words, retimed = 0, 0
    for j, ew in enumerate(edited):
        m = e2m.get(j)
        start, end, word = ew['start'], ew['end'], ew['word']
        if j in snap:
            mt = master_tx[snap[j]]
            start, end = round(mt['start'], 3), round(mt['end'], 3)
        elif m is not None:
            retimed += 1
        if m is not None:
            if str(m) in d_words:
                new_dir[str(j)] = d_words[str(m)]
        else:
            changed_words += 1  # inserted / respelled -> base white (flag for review)
        new_tx.append({'word': word, 'start': start, 'end': end, 'prob': 1.0})
        new_norm.append({'word': word.lower(), 'start': start, 'end': end})

    # DE-DUPLICATE QUOTES: the renderer auto-adds " around words the director flags as
    # quoted (q). If the edited SRT ALSO carries literal double-quotes on those same words
    # (they were baked into the exported text), they'd stack ("" ""). Strip literal double
    # quotes ONLY from q-flagged words; leave editor-added quotes on non-q words as typed.
    _DQ = '"“”'  # straight + curly double quotes (NOT apostrophes)
    dequoted = 0
    for j in range(len(new_tx)):
        if new_dir.get(str(j), {}).get('q'):
            w0 = new_tx[j]['word']
            w = w0.lstrip(_DQ).rstrip(_DQ)
            if w != w0:
                new_tx[j]['word'] = w
                new_norm[j]['word'] = w.lower()
                dequoted += 1
    print(f'quote de-dupe       : {dequoted} words (literal quote stripped; renderer re-adds)')

    # Cue groupings verbatim from the edited SRT (honor the editor's exact boundaries).
    cues, cur_cid, cur = [], None, []
    for j, ew in enumerate(edited):
        if ew['cue'] != cur_cid:
            if cur:
                cues.append(cur)
            cur, cur_cid = [], ew['cue']
        cur.append(j)
    if cur:
        cues.append(cur)

    work = a.work or Path(tempfile.mkdtemp(prefix='caprebuild_'))
    work.mkdir(parents=True, exist_ok=True)
    (work / 'transcript.json').write_text(json.dumps({'words': new_tx}, indent=1))
    (work / 'spice_norm.json').write_text(json.dumps({'words': new_norm}, indent=1))
    (work / 'director_stream.json').write_text(
        json.dumps({'words': new_dir, 'voice_spans': director.get('voice_spans', [])}, indent=1))
    (work / 'cues.json').write_text(json.dumps(cues))
    print(f'cues (verbatim)     : {len(cues)}')

    print(f'edited words        : {len(edited)}')
    print(f'master words        : {len(master_tx)}')
    print(f'carried styling on  : {len(new_dir)} words')
    print(f're-timed (moved)    : {retimed} words')
    print(f'changed/new (WHITE) : {changed_words} words  <-- review if > 0')
    print(f'work dir            : {work}')

    if a.dry_run:
        print('DRY RUN — inputs written, render skipped.')
        return 0

    cmd = [sys.executable, str(SCRIPT / 'generate_spice.py'),
           str(work / 'spice_norm.json'),
           '--preset', str(a.preset),
           '--style',  str(work / 'director_stream.json'),
           '--cues',   str(work / 'cues.json'),
           '--no-onset-correct',
           '--out',    str(work / 'subs.ass'),
           '--burn',   str(a.dims_ref),
           '--burn-out', str(a.out),
           '--alpha']
    print('\n$ ' + ' '.join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print('generate_spice FAILED', file=sys.stderr); return r.returncode
    print(f'\nOK -> {a.out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
