from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "maka-1bit-skill" / "scripts"
STYLES = ("strict-dither", "soft-ink", "mono-print")
PALETTES = {
    "olive-terminal": {"#0b0e08", "#bac3a0"},
    "soft-mint": {"#103b2b", "#dcefc8"},
    "classic-mono": {"#000000", "#ffffff"},
    "amber-screen": {"#2a1600", "#f2c14e"},
    "cobalt-ice": {"#071d3b", "#b8dbff"},
    "plum-paper": {"#2e102f", "#efcfea"},
}


class PipelineTest(unittest.TestCase):
    def make_fixture(self, path: Path) -> None:
        image = Image.new("RGB", (320, 240), "#e7dfc6")
        draw = ImageDraw.Draw(image)
        for x in range(image.width):
            shade = int(40 + x / image.width * 180)
            draw.line((x, 0, x, image.height), fill=(shade, shade, shade))
        draw.ellipse((80, 35, 245, 205), outline="white", width=13)
        draw.rectangle((120, 75, 205, 175), fill="#303030")
        image.save(path)

    def run_pipeline(self, style: str, palette: str) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            source = temp / "source.png"
            output = temp / "output.png"
            self.make_fixture(source)
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "postprocess_1bit.py"),
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--style",
                    style,
                    "--palette",
                    palette,
                    "--logical-long-edge",
                    "128",
                    "--scale",
                    "4",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_1bit.py"),
                    "--input",
                    str(output),
                    "--source",
                    str(source),
                    "--pixel-scale",
                    "4",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with Image.open(output) as image:
                colors = {"#%02x%02x%02x" % color for _, color in image.getcolors()}
            self.assertEqual(colors, PALETTES[palette])

    def test_all_style_palette_combinations(self) -> None:
        for style in STYLES:
            for palette in PALETTES:
                with self.subTest(style=style, palette=palette):
                    self.run_pipeline(style, palette)

    def test_style_is_required(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "postprocess_1bit.py"),
                "--input",
                "missing.png",
                "--output",
                "output.png",
                "--palette",
                "olive-terminal",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--style", result.stderr)

    def test_palette_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            source = temp / "source.png"
            output = temp / "output.png"
            self.make_fixture(source)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "postprocess_1bit.py"),
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--style",
                    "strict-dither",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("choose --palette", result.stderr)


if __name__ == "__main__":
    unittest.main()
