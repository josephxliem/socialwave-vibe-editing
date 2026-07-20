#!/usr/bin/env python3
"""
title_overlay.py — burn Social Wave reel TITLE TEXT onto a vertical clip (or emit an alpha overlay).

Per SW Reel Quality Rules v2 (2026-07-20): every reel carries on-screen title text at the top —
a scroll-stopper that gives the premise/context and complements (never duplicates) the hook line.

Style: Montserrat ExtraBold, ALL-CAPS as-written, white, centred at ~13% from top, auto-wrapped
(max 2 lines, ~86% safe width), with the brand two-layer soft shadow. Words wrapped in
*asterisks* render in brand blue (#1CB5E5); words in ~tildes~ in brand coral (#F58A7D).

Usage:
  title_overlay.py <in.mp4> --title "STOP MAKING *HOW-TO* CONTENT" --out <out.mp4>
  title_overlay.py <in.mp4> --title "..." --out <out.mov> --alpha       # transparent overlay
  [--y-pct 13] [--font-px 0 (auto ~7.4% of height)] [--end <sec> (default: full duration)]
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
FONTS = SKILL / "fonts" / "free_font"
BLUE, CORAL, WHITE = "1CB5E5", "F58A7D", "FFFFFF"


def ass_color(hex_rgb):
    h = hex_rgb.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}&"


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-show_entries", "format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    d = json.loads(out)
    st = d["streams"][0]
    return int(st["width"]), int(st["height"]), float(d["format"]["duration"])


def wrap(words, max_chars):
    lines, cur = [], []
    for w in words:
        plain = w.strip("*~")
        if cur and len(" ".join([x.strip('*~') for x in cur]) + " " + plain) > max_chars:
            lines.append(cur); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(cur)
    return lines


def parse_spans(title):
    """'A *B C* D' -> [('A',None),('B C',BLUE),('D',None)] — spans may cover multiple words."""
    out=[]
    for m in re.finditer(r"\*([^*]+)\*|~([^~]+)~|([^*~]+)", title):
        if m.group(1): out.append((m.group(1).strip(), BLUE))
        elif m.group(2): out.append((m.group(2).strip(), CORAL))
        elif m.group(3) and m.group(3).strip(): out.append((m.group(3).strip(), None))
    return out


def span_words(title):
    """flatten to [(word, color)]"""
    words=[]
    for text,color in parse_spans(title):
        for w in text.split(): words.append((w,color))
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--y-pct", type=float, default=13.0)
    ap.add_argument("--font-px", type=int, default=0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--alpha", action="store_true")
    a = ap.parse_args()

    W, H, dur = probe(a.inp)
    end = a.end or dur
    fs = a.font_px or int(H * 0.05)
    pairs = span_words(a.title)
    def wrap_pairs(fs_):
        max_chars = max(10, int((W * 0.86) / (fs_ * 0.62)))
        lines, cur, cl = [], [], 0
        for w, c in pairs:
            if cur and cl + 1 + len(w) > max_chars:
                lines.append(cur); cur, cl = [], 0
            cur.append((w, c)); cl += (1 if cl else 0) + len(w)
        if cur: lines.append(cur)
        return lines
    lines = wrap_pairs(fs)
    while len(lines) > 2 and fs > int(H * 0.035):
        fs = int(fs * 0.92); lines = wrap_pairs(fs)
    y = int(H * a.y_pct / 100)
    def line_txt(ln, colored=True):
        parts=[]
        for w,c in ln:
            if colored and c: parts.append(f"{{\\1c{ass_color(c)}}}{w}{{\\1c{ass_color(WHITE)}}}")
            else: parts.append(w)
        return " ".join(parts)
    text = "\\N".join(line_txt(ln) for ln in lines)
    plain = "\\N".join(line_txt(ln, colored=False) for ln in lines)

    def tc(t):
        h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    hdr = f"""[Script Info]
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Montserrat ExtraBold,{fs},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,0,8,40,40,0,1
Style: TitleShadow,Montserrat ExtraBold,{fs},&H00000000,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,0,8,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{tc(0)},{tc(end)},TitleShadow,,0,0,0,,{{\\an8\\pos({W//2+int(fs*0.06)},{y+int(fs*0.10)})\\blur14\\1a&H50&}}{plain}
Dialogue: 1,{tc(0)},{tc(end)},Title,,0,0,0,,{{\\an8\\pos({W//2},{y})}}{text}
"""
    tmp = tempfile.NamedTemporaryFile(suffix=".ass", delete=False, mode="w")
    tmp.write(hdr); tmp.close()
    sub = Path(tmp.name).as_posix().replace(":", r"\:")
    fdir = FONTS.resolve().as_posix().replace(":", r"\:")

    if a.alpha:
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-f", "lavfi", "-i", f"color=c=black@0.0:s={W}x{H}:r=25:d={end:.3f},format=yuva444p",
               "-vf", f"ass='{sub}':fontsdir='{fdir}':alpha=1",
               "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", a.out]
    else:
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", a.inp,
               "-vf", f"ass='{sub}':fontsdir='{fdir}'",
               "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
               "-c:a", "copy", "-movflags", "+faststart", a.out]
    r = subprocess.run(cmd)
    Path(tmp.name).unlink(missing_ok=True)
    print(("alpha title overlay" if a.alpha else "title burned") + f" -> {a.out}")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
