import { Composition } from "remotion";
import { BrandCaption, brandCaptionSchema } from "./BrandCaption";

// Sample word-timing data — same shape the kit's transcript.json produces
// ({word,start,end}). Swap defaultProps.words for a real clip's words to render.
const SAMPLE = [
  { word: "YouTube's", start: 0.0, end: 0.55 },
  { word: "ALGORITHM", start: 0.55, end: 0.95, hero: "blue" as const },
  { word: "has", start: 0.95, end: 1.15 },
  { word: "one", start: 1.15, end: 1.35 },
  { word: "job:", start: 1.35, end: 1.8 },
  { word: "SATISFY", start: 1.8, end: 2.4, hero: "coral" as const },
  { word: "its", start: 2.4, end: 2.6 },
  { word: "viewers.", start: 2.6, end: 3.2 },
];

export const RemotionRoot: React.FC = () => {
  const fps = 30;
  const durationInFrames = Math.ceil(3.4 * fps);
  return (
    <Composition
      id="BrandCaption"
      component={BrandCaption}
      durationInFrames={durationInFrames}
      fps={fps}
      width={1080}
      height={1920}
      schema={brandCaptionSchema}
      defaultProps={{ words: SAMPLE }}
    />
  );
};
