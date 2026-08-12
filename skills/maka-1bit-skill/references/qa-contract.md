# QA contract

Accept a final only after both semantic and technical checks pass.

## Semantic checks

- Preserve the source subject count and identities.
- Preserve the dominant pose, silhouette, gaze/direction, camera angle, spatial relationships, and recognizable landmarks.
- Preserve the intended crop unless the user requested reframing.
- Add no objects, anatomy, text, border, signature, logo, or watermark.
- Keep important thin features legible at the final logical resolution.

Perform these checks visually before and after deterministic post-processing. Automated metrics do not replace visual comparison.

For pet portraits, additionally apply every rejection rule in [pet-portraits.md](pet-portraits.md). Treat a missing or moved identity mark, changed eye/ear geometry, altered body proportion, or changed paw/tail placement as a semantic failure even when the overall style is strong.

## Style checks

- Make individual pixels or pixel clusters visibly intentional at 100% zoom.
- Use hard edges with no resampling blur.
- Prefer coherent clusters over isolated salt-and-pepper noise.
- Reserve solid dark masses for structural shadow and outline while retaining internal volume through dither density.
- Avoid pseudo-pixel artifacts: smooth diagonal antialiasing, soft gradients, JPEG halos, and subpixel-looking strokes.
- Require thumbnail readability before texture readability.
- Require dither density to follow the source tonal hierarchy instead of acting as arbitrary decoration.
- Reject smooth vector-like silhouettes that remove internal form, even if they technically contain two colors.

## Technical checks for `binary` export

Require all of the following:

- PNG output
- RGB color model
- exactly two unique RGB colors
- positive dimensions divisible by the declared integer display scale
- uniform blocks aligned to that scale
- source-to-output aspect-ratio drift no greater than 15% unless reframing was requested

Run `scripts/validate_1bit.py`; require exit status 0 and `"passed": true`.

## Iteration order

Fix the earliest failing layer first:

1. missing identity detail: raise logical resolution
2. excessive irrelevant detail: lower logical resolution
3. muddy tonal separation: adjust contrast or threshold
4. unwanted texture character: select the correct preset method
5. technical palette/grid failure: rerun deterministic post-processing
6. unreadable structure after deterministic tuning: create one controlled AI intermediate
