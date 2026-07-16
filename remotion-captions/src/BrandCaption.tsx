import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";

// Social Wave brand palette (matches spice_socialwave.json)
const COLORS = { base: "#FFFFFF", blue: "#1CB5E5", coral: "#F58A7D", guest: "#FECB00" };

const wordSchema = z.object({
  word: z.string(),
  start: z.number(),
  end: z.number(),
  hero: z.enum(["blue", "coral", "guest"]).optional(),
});

export const brandCaptionSchema = z.object({
  words: z.array(wordSchema),
});

// One-word-at-a-time caption in the Social Wave style. This is the STARTING POINT
// for building new caption-style variations per client (colours, weight, motion) —
// data comes from the kit's word-timing JSON, so styles render identically every time.
export const BrandCaption: React.FC<z.infer<typeof brandCaptionSchema>> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const active = words.find((w) => t >= w.start && t < w.end) ?? null;
  if (!active) return <AbsoluteFill style={{ backgroundColor: "transparent" }} />;

  const color = active.hero ? COLORS[active.hero] : COLORS.base;
  const isHero = Boolean(active.hero);

  return (
    <AbsoluteFill style={{ backgroundColor: "transparent", justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          position: "absolute",
          top: "58%",
          transform: "translateY(-50%)",
          fontFamily: "Montserrat, sans-serif",
          fontWeight: isHero ? 800 : 500,
          fontSize: isHero ? 104 : 88,
          color,
          textTransform: isHero ? "uppercase" : "none",
          textAlign: "center",
          // subtle brand drop shadow (down-right), not a bloom
          textShadow: "6px 8px 14px rgba(0,0,0,0.75)",
          padding: "0 60px",
        }}
      >
        {active.word}
      </div>
    </AbsoluteFill>
  );
};
