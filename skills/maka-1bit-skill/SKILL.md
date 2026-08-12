---
name: maka-1bit-skill
description: Convert an existing photo, pet portrait, illustration, scan, or generated raster image into composition-faithful 1bit pixel art through deterministic downsampling, tonal reduction, deliberate dithering, limited two-color palettes, and automated QA, with optional controlled AI simplification only when the source does not remain readable. Use when the user asks to turn an image into 1bit, one-bit, monochrome pixel art, Game Boy-like art, black-and-white dither art, retro bitmap art, requests a 1bit portrait of their cat, dog, or other pet, or wants a result resembling a supplied 1bit reference. Do not use for ordinary grayscale conversion, general pixel-art creation without an input image, vector tracing, spritesheets, or edits that must remain photorealistic.
---

# Maka 1bit Skill

Preserve the source composition and subject identity. Default to deterministic two-color reduction: downsample the original, compress continuous tone into preset-specific pixel density, and upscale on an integer grid. Never replace the source with a smooth vector silhouette.

## Required inputs

- Require one edit-target image.
- Accept an optional preset, two-color palette, crop request, logical resolution, and output scale.
- Default to `strict-dither` when the user only asks for “1bit”.
- Default to exact two-color PNG output.
- Ask one concise question only when a missing choice materially changes the result. Otherwise use the defaults.

Read [references/style-presets.md](references/style-presets.md) before processing. For a pet or animal, also read [references/pet-portraits.md](references/pet-portraits.md). Read [references/qa-contract.md](references/qa-contract.md) before accepting a final.

## Boundaries

- Preserve subject count, identity, pose, camera angle, spatial relationships, crop, and aspect ratio unless the user requests a change.
- Preserve recognition and tonal hierarchy while allowing downsampling to merge fine texture into coherent dither clusters.
- Do not add, remove, mirror, relocate, or invent markings, anatomy, props, text, borders, logos, or watermarks.
- Do not imitate a living artist. Translate references into observable palette and dither traits.
- Do not overwrite the input. Save a new PNG.
- Do not call a smooth black-and-white silhouette 1bit pixel art; internal volume must remain visible through pixel density or structural clusters.

## Workflow

1. Inspect the input and any style reference.
2. Record invariants: subject identity, pose, visible landmarks, crop, foreground/background relationship, and forbidden additions. For pets, build the identity ledger in [references/pet-portraits.md](references/pet-portraits.md).
3. Select `strict-dither`, `soft-ink`, `mono-print`, or a custom preset from [references/style-presets.md](references/style-presets.md).
4. Process the original image directly:

   ```bash
   python3 scripts/postprocess_1bit.py \
     --input <original-image> \
     --output <final.png> \
     --preset strict-dither
   ```

   Use `--logical-long-edge` to control abstraction: lower values merge more detail; higher values preserve small identity anchors. Use `--scale` only for integer nearest-neighbor display scaling. Pass `--dark` and `--light` only for a custom palette.
5. Validate the output:

   ```bash
   python3 scripts/validate_1bit.py \
     --input <final.png> \
     --source <original-image> \
     --pixel-scale 4
   ```

6. Inspect the original and final at thumbnail size and 100% zoom. Check identity, tonal hierarchy, pixel clusters, and every rule in [references/qa-contract.md](references/qa-contract.md).
7. Fix one variable at a time. Raise logical resolution if a defining mark disappears; lower it if irrelevant detail dominates. Adjust contrast, threshold, or dither method only after resolution.
8. Only if direct conversion cannot preserve readable subject structure, load `$imagegen` and create one composition-locked tonal simplification intermediate. Preserve identity and broad light/shadow planes. Never ask ImageGen to create the final 1bit effect, and never deliver the AI intermediate directly; run it through steps 4–7.
9. Return the final PNG inline and report its path, preset, palette, logical resolution, scale, method, and validator result.

## Execution choices

- Prefer direct deterministic conversion for photos, pets, portraits, and all identity-sensitive subjects.
- When comparing presets, process the same original or the same accepted intermediate through every preset.
- Keep all stages non-destructive and reproducible.
- For white, black, or low-contrast pets, tune logical resolution and contrast before considering AI.

## Failure handling

- If the validator reports more than two colors or grid misalignment, rerun deterministic processing from the same source.
- If a small feature disappears, raise `--logical-long-edge` before changing the palette or using AI.
- If the result is too literal, lower `--logical-long-edge` for stronger deterministic abstraction.
- If an optional AI intermediate drifts from the source, discard it and return to the original.
