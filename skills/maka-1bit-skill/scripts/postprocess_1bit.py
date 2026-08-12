#!/usr/bin/env python3
"""Convert a raster image into an exact two-color, grid-aligned PNG."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


STYLES = {
    "strict-dither": {
        "method": "bayer4",
        "contrast": 1.25,
    },
    "soft-ink": {
        "method": "atkinson",
        "contrast": 1.10,
    },
    "mono-print": {
        "method": "floyd-steinberg",
        "contrast": 1.20,
    },
}

PALETTES = {
    "olive-terminal": ("#0b0e08", "#bac3a0"),
    "soft-mint": ("#103b2b", "#dcefc8"),
    "classic-mono": ("#000000", "#ffffff"),
    "amber-screen": ("#2a1600", "#f2c14e"),
    "cobalt-ice": ("#071d3b", "#b8dbff"),
    "plum-paper": ("#2e102f", "#efcfea"),
}

BAYER4 = (
    (0, 8, 2, 10),
    (12, 4, 14, 6),
    (3, 11, 1, 9),
    (15, 7, 13, 5),
)

BAYER8 = (
    (0, 32, 8, 40, 2, 34, 10, 42),
    (48, 16, 56, 24, 50, 18, 58, 26),
    (12, 44, 4, 36, 14, 46, 6, 38),
    (60, 28, 52, 20, 62, 30, 54, 22),
    (3, 35, 11, 43, 1, 33, 9, 41),
    (51, 19, 59, 27, 49, 17, 57, 25),
    (15, 47, 7, 39, 13, 45, 5, 37),
    (63, 31, 55, 23, 61, 29, 53, 21),
)


def hex_color(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("colors must use six-digit hex, for example #0b0e08")
    try:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("colors must use six-digit hexadecimal") from exc


def luminance(color: tuple[int, int, int]) -> float:
    r, g, b = (channel / 255 for channel in color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def logical_size(width: int, height: int, long_edge: int) -> tuple[int, int]:
    ratio = long_edge / max(width, height)
    return max(1, round(width * ratio)), max(1, round(height * ratio))


def ordered_dither(gray: Image.Image, matrix: tuple[tuple[int, ...], ...]) -> Image.Image:
    width, height = gray.size
    size = len(matrix)
    levels = size * size
    source = gray.load()
    output = Image.new("1", gray.size)
    target = output.load()
    for y in range(height):
        for x in range(width):
            threshold = (matrix[y % size][x % size] + 0.5) * 255 / levels
            target[x, y] = 255 if source[x, y] >= threshold else 0
    return output


def error_diffusion(gray: Image.Image, method: str, threshold: int) -> Image.Image:
    width, height = gray.size
    values = [float(pixel) for pixel in gray.tobytes()]
    output = Image.new("1", gray.size)
    target = output.load()

    if method == "atkinson":
        diffusion = (
            (1, 0, 1 / 8),
            (2, 0, 1 / 8),
            (-1, 1, 1 / 8),
            (0, 1, 1 / 8),
            (1, 1, 1 / 8),
            (0, 2, 1 / 8),
        )
    else:
        diffusion = (
            (1, 0, 7 / 16),
            (-1, 1, 3 / 16),
            (0, 1, 5 / 16),
            (1, 1, 1 / 16),
        )

    for y in range(height):
        for x in range(width):
            index = y * width + x
            old = values[index]
            new = 255 if old >= threshold else 0
            target[x, y] = new
            error = old - new
            for dx, dy, weight in diffusion:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor = ny * width + nx
                    values[neighbor] = min(255, max(0, values[neighbor] + error * weight))
    return output


def quantize(gray: Image.Image, method: str, threshold: int) -> Image.Image:
    if method == "threshold":
        return gray.point(lambda value: 255 if value >= threshold else 0, mode="1")
    if method == "bayer4":
        return ordered_dither(gray, BAYER4)
    if method == "bayer8":
        return ordered_dither(gray, BAYER8)
    if method in {"atkinson", "floyd-steinberg"}:
        return error_diffusion(gray, method, threshold)
    raise ValueError(f"unsupported dither method: {method}")


def colorize(binary: Image.Image, dark: tuple[int, int, int], light: tuple[int, int, int]) -> Image.Image:
    palette = Image.new("RGB", binary.size)
    source = binary.load()
    target = palette.load()
    for y in range(binary.height):
        for x in range(binary.width):
            target[x, y] = light if source[x, y] else dark
    return palette


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--style", "--preset", dest="style", choices=STYLES, required=True)
    parser.add_argument("--palette", choices=PALETTES)
    parser.add_argument("--dark", type=hex_color)
    parser.add_argument("--light", type=hex_color)
    parser.add_argument(
        "--method",
        choices=("threshold", "bayer4", "bayer8", "atkinson", "floyd-steinberg"),
    )
    parser.add_argument("--threshold", type=int, default=128)
    parser.add_argument("--contrast", type=float)
    parser.add_argument("--logical-long-edge", type=int, default=512)
    parser.add_argument("--scale", type=int, default=4)
    parser.add_argument("--invert", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        raise SystemExit(f"input does not exist: {args.input}")
    if args.output.suffix.lower() != ".png":
        raise SystemExit("output must use the .png extension")
    if not 0 <= args.threshold <= 255:
        raise SystemExit("threshold must be between 0 and 255")
    if args.logical_long_edge < 16:
        raise SystemExit("logical-long-edge must be at least 16")
    if args.scale < 1 or args.scale > 32:
        raise SystemExit("scale must be between 1 and 32")

    style = STYLES[args.style]
    if args.palette and (args.dark or args.light):
        raise SystemExit("use either --palette or both --dark and --light, not both")
    if args.palette:
        palette_name = args.palette
        dark = hex_color(PALETTES[args.palette][0])
        light = hex_color(PALETTES[args.palette][1])
    elif args.dark and args.light:
        palette_name = "custom"
        dark, light = args.dark, args.light
    else:
        raise SystemExit("choose --palette or provide both --dark and --light")
    if dark == light:
        raise SystemExit("dark and light colors must differ")
    if luminance(dark) > luminance(light):
        dark, light = light, dark
    method = args.method or style["method"]
    contrast = args.contrast if args.contrast is not None else style["contrast"]
    if not math.isfinite(contrast) or contrast <= 0:
        raise SystemExit("contrast must be a positive finite number")

    with Image.open(args.input) as source:
        flattened = Image.new("RGB", source.size, light)
        if source.mode in {"RGBA", "LA"} or "transparency" in source.info:
            rgba = source.convert("RGBA")
            flattened.paste(rgba, mask=rgba.getchannel("A"))
        else:
            flattened.paste(source.convert("RGB"))

    logical = logical_size(*flattened.size, args.logical_long_edge)
    reduced = flattened.resize(logical, Image.Resampling.LANCZOS)
    gray = ImageOps.grayscale(reduced)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(contrast)
    if args.invert:
        gray = ImageOps.invert(gray)
    binary = quantize(gray, method, args.threshold)
    result = colorize(binary, dark, light)
    result = result.resize(
        (logical[0] * args.scale, logical[1] * args.scale),
        Image.Resampling.NEAREST,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output, format="PNG", optimize=True)
    print(
        f"saved={args.output} logical={logical[0]}x{logical[1]} "
        f"output={result.width}x{result.height} style={args.style} "
        f"palette_name={palette_name} method={method} "
        f"palette=#{dark[0]:02x}{dark[1]:02x}{dark[2]:02x},"
        f"#{light[0]:02x}{light[1]:02x}{light[2]:02x}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
