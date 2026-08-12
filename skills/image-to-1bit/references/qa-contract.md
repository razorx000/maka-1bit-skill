# QA contract

Accept a final only after both semantic and technical checks pass.

## Semantic checks

- Preserve the source subject count and identities.
- Preserve the dominant pose, silhouette, gaze/direction, camera angle, spatial relationships, and recognizable landmarks.
- Preserve the intended crop unless the user requested reframing.
- Add no objects, anatomy, text, border, signature, logo, or watermark.
- Keep important thin features legible at the final logical resolution.

Perform these checks visually before and after deterministic post-processing. Automated metrics do not replace visual comparison.

## Style checks

- Make individual pixels or pixel clusters visibly intentional at 100% zoom.
- Use hard edges with no resampling blur.
- Prefer coherent clusters over isolated salt-and-pepper noise.
- Reserve solid dark masses for structural shadow and outline.
- Avoid pseudo-pixel artifacts: smooth diagonal antialiasing, soft gradients, JPEG halos, and subpixel-looking strokes.

## Technical checks for `binary` export

Require all of the following:

- PNG output
- RGB color model
- exactly two unique RGB colors
- positive dimensions divisible by the declared integer display scale
- uniform blocks aligned to that scale
- source-to-output aspect-ratio drift no greater than 15% unless reframing was requested

Run `scripts/validate_1bit.py`; require exit status 0 and `"passed": true`. Do not apply these exact-two-color requirements to the default `artistic` export.

## Iteration order

Fix the earliest failing layer first:

1. semantic drift: revise the ImageGen prompt
2. missing thin detail: raise logical resolution
3. muddy tonal separation: raise contrast or change method
4. excessive noise: use `atkinson` or `bayer4` and lower contrast
5. weak 1bit character: use `threshold` or `bayer4` and strengthen prompt contours
6. technical palette/grid failure: rerun deterministic post-processing
