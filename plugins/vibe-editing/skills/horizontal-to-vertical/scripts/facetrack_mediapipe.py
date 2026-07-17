#!/usr/bin/env python3
"""
facetrack_mediapipe.py — face tracking via Google MediaPipe (alternative to YuNet).

Outputs per-sampled-frame face center + box (normalized 0..1), the same signal the
reframe uses to keep the subject in frame. Available as a fallback/alternative to
qa_reframe_v2's YuNet detector when YuNet mis-tracks.

    { "fps": float, "sample_fps": float, "width": int, "height": int,
      "track": [ {"t": float, "x": float, "y": float, "w": float, "h": float, "score": float}, ... ] }
(x,y = box center as a fraction of frame; missing frames omitted.)

Usage:
    facetrack_mediapipe.py <video> --out track.json [--sample-fps 5] [--score 0.5]
"""
import argparse, json, sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sample-fps", type=float, default=5.0)
    ap.add_argument("--score", type=float, default=0.5)
    a = ap.parse_args()

    import cv2, mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision

    model_path = Path(__file__).with_name("blaze_face_short_range.tflite")
    if not model_path.exists():
        print(f"ERROR: missing model {model_path.name} — download it next to this script:\n"
              f"  curl -L -o {model_path} https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite",
              file=sys.stderr); return 1

    cap = cv2.VideoCapture(a.source)
    if not cap.isOpened():
        print(f"ERROR: cannot open {a.source}", file=sys.stderr); return 1
    W = int(cap.get(3)); H = int(cap.get(4)); fps = cap.get(5) or 30.0
    step = max(1, int(round(fps / a.sample_fps)))

    opts = mp_vision.FaceDetectorOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(model_path)),
        min_detection_confidence=a.score)
    detector = mp_vision.FaceDetector.create_from_options(opts)

    track, idx = [], 0
    try:
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            if idx % step == 0:
                rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
                mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                res = detector.detect(mp_img)
                if res.detections:
                    d = max(res.detections, key=lambda x: x.categories[0].score)
                    bb = d.bounding_box  # pixel coords
                    track.append({
                        "t": round(idx / fps, 3),
                        "x": round((bb.origin_x + bb.width / 2) / W, 4),
                        "y": round((bb.origin_y + bb.height / 2) / H, 4),
                        "w": round(bb.width / W, 4), "h": round(bb.height / H, 4),
                        "score": round(float(d.categories[0].score), 3),
                    })
            idx += 1
    finally:
        cap.release(); detector.close()

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({
        "fps": round(fps, 3), "sample_fps": a.sample_fps, "width": W, "height": H, "track": track,
    }, indent=2))
    hit = len(track)
    print(f"mediapipe: {hit} face samples -> {a.out}"
          + (f"  | x {min(t['x'] for t in track):.2f}-{max(t['x'] for t in track):.2f}" if hit else " (no faces)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
