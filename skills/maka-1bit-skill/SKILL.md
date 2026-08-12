---
name: maka-1bit-skill
description: Convert an existing photo, pet portrait, illustration, scan, or generated raster image into composition-faithful 1bit pixel art through deterministic downsampling, tonal reduction, deliberate dithering, limited two-color palettes, and automated QA. After image upload, require the user to choose one of three styles and then one of six palettes before processing. Use when the user asks to turn an image into 1bit, one-bit, monochrome pixel art, Game Boy-like art, black-and-white dither art, retro bitmap art, requests a 1bit portrait of their cat, dog, or other pet, or wants a result resembling a supplied 1bit reference. Do not use for ordinary grayscale conversion, general pixel-art creation without an input image, vector tracing, spritesheets, or edits that must remain photorealistic.
---

# Maka 1bit Skill

Preserve the source composition and subject identity. Use deterministic two-color reduction: downsample the original, compress continuous tone into style-specific pixel density, apply the selected palette, and upscale on an integer grid. Never replace the source with a smooth vector silhouette.

## Mandatory selection gates

- Require one edit-target image.
- Require an explicit style and an explicit palette. Never assume defaults.
- After an image is uploaded, ask for the style first and stop. Present exactly:
  1. `strict-dither` — regular mechanical Bayer grid and crisp transitions
  2. `soft-ink` — lighter organic Atkinson clusters and open pale areas
  3. `mono-print` — fine Floyd–Steinberg print texture and tonal retention
- After the user chooses a style, ask for the palette and stop. Present all six choices from [references/palette-presets.md](references/palette-presets.md), including both hex colors.
- Use a native interactive selection control when available. Otherwise show a concise numbered list and ask the user to reply with a number or name.
- If the initial request already specifies one choice, ask only for the other. If it specifies both, process immediately.
- Do not inspect beyond what is needed for safety, run the processor, or produce an output until both choices are known.
- Default to exact two-color PNG output.
- Accept an optional crop request, logical resolution, and output scale without adding further mandatory questions.

Read [references/style-presets.md](references/style-presets.md) and [references/palette-presets.md](references/palette-presets.md) before processing. For a pet or animal, also read [references/pet-portraits.md](references/pet-portraits.md). Read [references/qa-contract.md](references/qa-contract.md) before accepting a final.

## Boundaries

- Preserve subject count, identity, pose, camera angle, spatial relationships, crop, and aspect ratio unless the user requests a change.
- Preserve recognition and tonal hierarchy while allowing downsampling to merge fine texture into coherent dither clusters.
- Do not add, remove, mirror, relocate, or invent markings, anatomy, props, text, borders, logos, or watermarks.
- Do not imitate a living artist. Translate references into observable palette and dither traits.
- Do not overwrite the input. Save a new PNG.
- Do not call a smooth black-and-white silhouette 1bit pixel art; internal volume must remain visible through pixel density or structural clusters.

## Workflow

1. Collect the style through the first mandatory selection gate.
2. Collect the palette through the second mandatory selection gate.
3. Inspect the input and any style reference.
4. Record invariants: subject identity, pose, visible landmarks, crop, foreground/background relationship, and forbidden additions. For pets, build the identity ledger in [references/pet-portraits.md](references/pet-portraits.md).
5. Process the original image directly:

   ```bash
   python3 scripts/postprocess_1bit.py \
     --input <original-image> \
     --output <final.png> \
     --style <selected-style> \
     --palette <selected-palette>
   ```

   Use `--logical-long-edge` to control abstraction: lower values merge more detail; higher values preserve small identity anchors. Use `--scale` only for integer nearest-neighbor display scaling. Pass both `--dark` and `--light` instead of `--palette` only when the user explicitly supplies a custom pair.
6. Validate the output:

   ```bash
   python3 scripts/validate_1bit.py \
     --input <final.png> \
     --source <original-image> \
     --pixel-scale 4
   ```

7. Inspect the original and final at thumbnail size and 100% zoom. Check identity, tonal hierarchy, pixel clusters, and every rule in [references/qa-contract.md](references/qa-contract.md).
8. Fix one variable at a time. Raise logical resolution if a defining mark disappears; lower it if irrelevant detail dominates. Adjust contrast, threshold, or dither method only after resolution.
9. Only if direct conversion cannot preserve readable subject structure, load `$imagegen` and create one composition-locked tonal simplification intermediate. Preserve identity and broad light/shadow planes. Never ask ImageGen to create the final 1bit effect, and never deliver the AI intermediate directly; run it through steps 5–8.
10. Return the final PNG inline and report its path, style, palette name and colors, logical resolution, scale, method, and validator result.

## Execution choices

- Prefer direct deterministic conversion for photos, pets, portraits, and all identity-sensitive subjects.
- When comparing styles or palettes, process the same original or the same accepted intermediate through every combination.
- Keep all stages non-destructive and reproducible.
- For white, black, or low-contrast pets, tune logical resolution and contrast before considering AI.

## Failure handling

- If the validator reports more than two colors or grid misalignment, rerun deterministic processing from the same source.
- If a small feature disappears, raise `--logical-long-edge` before changing the palette or using AI.
- If the result is too literal, lower `--logical-long-edge` for stronger deterministic abstraction.
- If an optional AI intermediate drifts from the source, discard it and return to the original.
