# Maka 1bit Skill 1.0.0

The first stable release focuses on a reproducible image-to-1bit workflow.

## Highlights

- Choose one of three dither styles: `strict-dither`, `soft-ink`, or `mono-print`.
- Choose one of six two-color palettes independently from the style.
- Pause for both choices after image upload; never assume a style or palette.
- Preserve composition, subject identity, recognizable landmarks, and tonal hierarchy.
- Apply additional identity checks to pet portraits.
- Export grid-aligned RGB PNG files containing exactly two colors.
- Validate all 18 built-in style and palette combinations.

## Requirements

- Python 3.10 or later
- Pillow 10 or later

## Scope

Version 1.0 does not include frames, numeric labels, or poster layouts. These are planned as optional post-processing layers in later minor releases so the conversion core remains stable.
