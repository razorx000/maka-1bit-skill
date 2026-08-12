# Style presets

The supplied tests use many RGB values—approximately 105,598 in `test01` and 49,999 in `test02`—despite reading visually as 1bit. Match their visual language through semantic redraw by default. Quantize to exactly two colors only for `binary` export.

## `strict-dither` — default

Use for a visibly strict two-tone bitmap result with bold contours and patterned shade.

- Binary palette: dark `#0b0e08`, light `#bac3a0`
- Post-process method: `bayer4`
- Logical long edge: `512`
- Display scale: `4`
- Visual traits: hard black-green contour, large flat light regions, checker/stipple clusters in midtones, squared corners, no soft gradients
- Prompt clause:

  ```text
  Rebuild the edit target as composition-faithful 1bit pixel art. Preserve every major subject, pose, landmark position, camera angle, and crop. Use bold near-black stepped contours, large pale olive tone fields, and deliberate ordered checker/stipple pixel clusters for selected midtone shading. Keep pixels hard-edged and grid-aligned. Simplify material texture into readable silhouettes and interior contour lines. Use only a two-tone visual design. No antialiasing, gradients, blur, soft brushwork, photorealistic texture, vector-smooth curves, added objects, text, frame, logo, or watermark.
  ```

## `soft-ink`

Use for the lighter green, hand-inked interpretation seen in the supplied `test01` reference.

- Binary palette: dark `#103b2b`, light `#dcefc8`
- Post-process method: `atkinson`
- Logical long edge: `512`
- Display scale: `4`
- Visual traits: selective dark-green contour, generous pale background, simplified volume, sparse clustered dither, less solid black coverage
- Prompt clause:

  ```text
  Rebuild the edit target as a composition-faithful two-tone green pixel-ink illustration. Preserve every major subject, pose, landmark position, camera angle, and crop. Use crisp stepped dark-green contours, broad pale-green fields, simplified anatomical and object planes, and sparse intentional pixel clusters only where shading is needed. Keep the result airy and readable rather than heavily black. No antialiasing, gradients, blur, photographic texture, smooth vector curves, added objects, text, frame, logo, or watermark.
  ```

## `mono-print`

Use when the user explicitly wants black and white rather than tinted two-tone art.

- Binary palette: dark `#000000`, light `#ffffff`
- Post-process method: `floyd-steinberg`
- Logical long edge: `512`
- Display scale: `4`
- Visual traits: high-contrast print, dispersed error-diffusion texture, exact black and white

## Custom choices

- Accept any two valid six-digit hexadecimal colors.
- Keep the darker color first. Compare relative luminance and swap internally if necessary.
- Prefer `bayer4` for graphic ordered dots, `atkinson` for lighter Macintosh-like texture, `floyd-steinberg` for continuous tonal retention, and `threshold` for poster-like flat masses.
- Use a logical long edge of `256` for chunkier pixels, `512` for the default balance, and `768` only for dense architecture or fine linework.
