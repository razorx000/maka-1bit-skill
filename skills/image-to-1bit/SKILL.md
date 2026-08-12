---
name: image-to-1bit
description: Convert an existing photo, illustration, scan, or generated raster image into composition-faithful 1bit-style pixel art through semantic redraw, deliberate pixel clusters, limited tinted palettes, and optional strict two-color export with automated QA. Use when the user asks to turn an image into 1bit, one-bit, monochrome pixel art, Game Boy-like art, black-and-white dither art, retro bitmap art, or requests a result resembling a supplied 1bit reference. Do not use for ordinary grayscale conversion, general pixel-art creation without an input image, vector tracing, spritesheets, or edits that must remain photorealistic.
---

# Image to 1bit

Turn an input raster into intentional 1bit-style pixel art while preserving its composition. Use AI editing for semantic simplification. Run the local two-color processor only when the user requests strict binary output or the intended destination requires it.

## Required inputs

- Require one edit-target image.
- Accept an optional visual reference, palette, preset, crop request, and output size.
- Default to `strict-dither` when the user only asks for “1bit”.
- Default to `artistic` export, which preserves the AI redraw's subtle green tone variation. Use `binary` export only when the user says strict, exact two colors, hardware-ready, print-ready, or explicitly asks for binary 1bit.
- Treat `soft-ink` and `strict-dither` as observable style choices, not automatic color-depth claims.
- Ask one concise question only when a missing choice would materially change the result. Otherwise use the defaults.

Read [references/style-presets.md](references/style-presets.md) before constructing the generation prompt. Read [references/qa-contract.md](references/qa-contract.md) before accepting a final image.

## Boundaries

- Preserve the source subject count, identities, poses, spatial relationships, camera angle, and overall crop unless the user requests a change.
- Simplify texture and lighting into readable shapes; do not merely apply a threshold filter when semantic redraw is available.
- Do not add characters, props, text, borders, logos, watermarks, or narrative details.
- Do not imitate a living artist. Translate a supplied reference into observable traits such as palette, outline weight, pixel clusters, and dither pattern.
- Do not overwrite the input. Save a new PNG.
- Call the default output “1bit-style” rather than technically binary. Do not claim strict two-color compliance before the local validator passes.

## Workflow

1. Inspect the edit target with the available image-viewing tool. Inspect every supplied style reference separately.
2. Record a compact invariant list: subject count, pose, landmark positions, foreground/background relationship, crop, and forbidden additions.
3. Select `strict-dither`, `soft-ink`, or a user-defined preset from [references/style-presets.md](references/style-presets.md).
4. Load and follow the installed `$imagegen` skill. Use its built-in image editing path with the original image as the edit target. Use any style image only as a style reference.
5. Prompt for a composition-faithful semantic redraw. Include the invariant list on every iteration. Ask for hard-edged pixel clusters, a two-tone design, no antialiasing, no gradients, no text, and no added objects.
6. Inspect the generated result. Reject it before post-processing if the subject, pose, layout, crop, or major silhouettes drifted. Iterate with one targeted correction.
7. Copy the accepted generated image into the project workspace when it is project-bound.
8. For the default `artistic` export, keep the accepted AI redraw and proceed to visual QA. Do not force it through binary quantization.
9. For a requested `binary` export, run deterministic post-processing:

   ```bash
   python3 scripts/postprocess_1bit.py \
     --input <generated-image> \
     --output <final.png> \
     --preset strict-dither
   ```

   Use `--preset soft-ink` when requested. Pass `--dark` and `--light` only for a user-defined palette. Use `--logical-long-edge` to change pixel density and `--scale` to change nearest-neighbor display scale.
10. Validate a binary export:

   ```bash
   python3 scripts/validate_1bit.py \
     --input <final.png> \
     --source <original-image> \
     --pixel-scale 4
   ```

11. Inspect the final PNG at original display size and zoomed in. Apply the acceptance rules in [references/qa-contract.md](references/qa-contract.md). If it fails visual QA, change one variable at a time: AI prompt, logical resolution, contrast, dither method, or threshold.
12. Return the final PNG inline and report its saved path, style preset, export mode, and visual QA result. For `binary`, also report its two palette colors, logical resolution, scale, dither method, and validator result.

## Execution choices

- Prefer semantic redraw for photos and complex illustrations. Preserve the accepted artistic redraw unless strict binary output is required.
- Allow deterministic-only conversion when the user explicitly asks for a literal filter, when ImageGen is unavailable, or when exact geometry matters more than simplification. State that this preserves pixels but does not redraw forms.
- Generate one candidate first. Create multiple variants only when the user requests them or the first candidate reveals a real style ambiguity.
- Keep the AI generation stage non-destructive and the post-processing stage reproducible.

## Failure handling

- If ImageGen is unavailable, offer deterministic-only conversion and explain its limitation; do not silently substitute it for semantic redraw.
- If a binary export's validator reports more than two colors, rerun post-processing from the accepted generated image.
- If pixel-grid alignment fails, rerun with integer `--scale` and do not resize the final PNG afterward with a smoothing filter.
- If composition drift exceeds the source, return to the AI edit stage rather than trying to repair the drift with dithering.
- If thin features disappear, raise `--logical-long-edge` before reducing contrast.
