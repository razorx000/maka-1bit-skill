# Style presets

All styles preserve the same source composition and tonal structure. Style controls only the deterministic dither behavior. Choose color separately from [palette-presets.md](palette-presets.md).

## Shared abstraction contract

- Downsample before dithering so small detail merges naturally.
- Preserve identity anchors, silhouettes, facial geometry, joints, paws/hands, and essential scene relationships through tonal contrast.
- Let pixel density describe internal volume; do not flatten the subject into a logo.
- Preserve crop and aspect ratio unless reframing is requested.
- Judge subject, pose, and tonal hierarchy at thumbnail size before judging individual pixels.

## `strict-dither`

- Method: `bayer4`
- Logical long edge: `512`
- Display scale: `4`
- Character: regular mechanical Bayer grid, stable checker structures, and crisp transitions.
- Best for: graphic scenes, architecture, objects, or users who want visible ordered pixels.

## `soft-ink`

- Method: `atkinson`
- Logical long edge: `512`
- Display scale: `4`
- Character: lighter perceived exposure, organic irregular clusters, and open pale areas.
- Best for: portraits, pets, organic forms, and a softer early-Macintosh-like texture.

## `mono-print`

- Method: `floyd-steinberg`
- Logical long edge: `512`
- Display scale: `4`
- Character: fine dispersed error-diffusion clusters that retain internal volume.
- Best for: photographic tonal retention, print-like texture, or fine modeling.
- Reject: flat white subject on flat black background with only smooth contour lines; that is a silhouette illustration, not this preset.

## Custom choices

- Accept custom colors only when the user explicitly provides both six-digit hexadecimal colors; keep the darker color first.
- Use `bayer4` for an obvious ordered grid, `bayer8` for a finer ordered screen, `atkinson` for lighter organic clusters, `floyd-steinberg` for tonal retention, and `threshold` only for deliberately flat poster masses.
- Use logical long edge `256` for chunky abstraction, `512` for the default balance, and `768` for small identity marks or dense linework.
