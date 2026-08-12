# Style presets

All presets preserve the same source composition and tonal structure. Their difference comes from palette and deterministic dither behavior, not from three independent AI redraws.

## Shared abstraction contract

- Downsample before dithering so small detail merges naturally.
- Preserve identity anchors, silhouettes, facial geometry, joints, paws/hands, and essential scene relationships through tonal contrast.
- Let pixel density describe internal volume; do not flatten the subject into a logo.
- Preserve crop and aspect ratio unless reframing is requested.
- Judge subject, pose, and tonal hierarchy at thumbnail size before judging individual pixels.

## `strict-dither` — default

- Palette: dark `#0b0e08`, light `#bac3a0`
- Method: `bayer4`
- Logical long edge: `512`
- Display scale: `4`
- Character: regular mechanical Bayer grid, stable checker structures, crisp transitions, olive/near-black palette.
- Best for: graphic scenes, architecture, objects, or users who want visible ordered pixels.

## `soft-ink`

- Palette: dark `#103b2b`, light `#dcefc8`
- Method: `atkinson`
- Logical long edge: `512`
- Display scale: `4`
- Character: lighter perceived exposure, organic irregular clusters, open pale areas, dark-green/pale-green palette.
- Best for: portraits, pets, organic forms, and a softer early-Macintosh-like texture.

## `mono-print`

- Palette: dark `#000000`, light `#ffffff`
- Method: `floyd-steinberg`
- Logical long edge: `512`
- Display scale: `4`
- Character: exact black and white, strongest luminance contrast, fine dispersed error-diffusion clusters that retain internal volume.
- Best for: monochrome print, e-paper, laser output, or strict black-and-white requests.
- Reject: flat white subject on flat black background with only smooth contour lines; that is a silhouette illustration, not this preset.

## Custom choices

- Accept any two six-digit hexadecimal colors and keep the darker color first.
- Use `bayer4` for an obvious ordered grid, `bayer8` for a finer ordered screen, `atkinson` for lighter organic clusters, `floyd-steinberg` for tonal retention, and `threshold` only for deliberately flat poster masses.
- Use logical long edge `256` for chunky abstraction, `512` for the default balance, and `768` for small identity marks or dense linework.
