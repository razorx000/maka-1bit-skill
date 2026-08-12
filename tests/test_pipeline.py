from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "image-to-1bit" / "scripts"


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

    def run_pipeline(self, preset: str) -> None:
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
                    "--preset",
                    preset,
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

    def test_strict_dither(self) -> None:
        self.run_pipeline("strict-dither")

    def test_soft_ink(self) -> None:
        self.run_pipeline("soft-ink")

    def test_mono_print(self) -> None:
        self.run_pipeline("mono-print")


if __name__ == "__main__":
    unittest.main()
