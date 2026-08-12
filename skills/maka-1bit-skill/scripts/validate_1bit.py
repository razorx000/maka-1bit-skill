#!/usr/bin/env python3
"""Validate exact palette, pixel-grid alignment, and source aspect ratio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--pixel-scale", type=int, default=4)
    parser.add_argument("--aspect-tolerance", type=float, default=0.15)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        raise SystemExit(f"input does not exist: {args.input}")
    if args.pixel_scale < 1:
        raise SystemExit("pixel-scale must be at least 1")
    if args.aspect_tolerance < 0:
        raise SystemExit("aspect-tolerance must be non-negative")

    with Image.open(args.input) as opened:
        image_format = opened.format
        original_mode = opened.mode
        image = opened.convert("RGB")

    colors = image.getcolors(maxcolors=image.width * image.height)
    unique = sorted(color for _, color in colors) if colors is not None else []
    divisible = image.width % args.pixel_scale == 0 and image.height % args.pixel_scale == 0
    grid_aligned = False
    if divisible:
        logical_size = (image.width // args.pixel_scale, image.height // args.pixel_scale)
        reduced = image.resize(logical_size, Image.Resampling.BOX)
        reconstructed = reduced.resize(image.size, Image.Resampling.NEAREST)
        grid_aligned = ImageChops.difference(image, reconstructed).getbbox() is None

    aspect_drift = None
    aspect_passed = True
    if args.source:
        if not args.source.is_file():
            raise SystemExit(f"source does not exist: {args.source}")
        with Image.open(args.source) as source:
            source_aspect = source.width / source.height
        output_aspect = image.width / image.height
        aspect_drift = abs(output_aspect / source_aspect - 1)
        aspect_passed = aspect_drift <= args.aspect_tolerance

    checks = {
        "png": image_format == "PNG",
        "rgb": original_mode == "RGB",
        "exactly_two_colors": len(unique) == 2,
        "dimensions_divisible_by_scale": divisible,
        "pixel_grid_aligned": grid_aligned,
        "aspect_ratio_within_tolerance": aspect_passed,
    }
    report = {
        "passed": all(checks.values()),
        "input": str(args.input),
        "size": [image.width, image.height],
        "pixel_scale": args.pixel_scale,
        "unique_colors": ["#%02x%02x%02x" % color for color in unique],
        "aspect_drift": round(aspect_drift, 6) if aspect_drift is not None else None,
        "checks": checks,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
