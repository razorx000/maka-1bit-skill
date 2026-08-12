# Roadmap

Maka 1bit Skill keeps image conversion and graphic-design composition as separate layers. Version 1.0 freezes the conversion core; later minor versions may add optional design effects without changing the selected dither style or palette.

## 1.0 — conversion core

- Three deterministic dither styles
- Six strict two-color palettes
- Mandatory style and palette selection gates
- Composition and identity preservation rules
- Pet-specific identity checks
- Exact two-color and pixel-grid validation

## 1.1 — frame layouts

- `none` and `frame` output modes
- Configurable inset, border width, and image alignment
- Aspect-ratio-safe placement inside a two-color frame
- Regression tests proving the embedded image is not resampled with smoothing

## 1.2 — data labels

- Optional title, index, numeric value, and compact metadata fields
- Pixel-font handling with explicit fallback rules
- Overflow, safe-area, and contrast checks
- No generated or inferred values: display only user-provided data

## 1.3 — poster systems

- Reusable grid, header, footer, and caption layouts
- Composable frame and data-label modules
- Output-size presets for screen and print
- Final whole-canvas two-color validation

## Design constraints

- Keep the original 1bit conversion available as `none` with no design layer.
- Apply design effects after the base 1bit image passes validation.
- Preserve exactly two RGB colors across the entire final canvas.
- Never change the chosen style, palette, crop, or subject identity implicitly.
- Test each new effect independently and in supported combinations.
