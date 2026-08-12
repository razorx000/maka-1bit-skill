# Maka 1bit Skill

A Codex skill for turning an existing raster image into composition-faithful 1bit-style pixel art, with optional technically verified two-color export.

It combines two layers:

1. semantic redraw with Codex ImageGen to simplify real subjects into intentional pixel-art forms while preserving composition;
2. optional deterministic local post-processing to guarantee exactly two RGB colors, a hard pixel grid, integer nearest-neighbor scaling, and a PNG export.

The default is an artistic export because real AI-generated 1bit-style references often use subtle intermediate RGB values for paper tone, glow, and atmosphere. Ask for `binary` when exactly two colors matter more than those subtleties.

## Why a dedicated skill

Existing projects cover adjacent parts of the problem, but not the complete workflow:

- [OpenAI ImageGen skill](https://github.com/openai/skills/blob/main/skills/.system/imagegen/SKILL.md) provides general raster generation and editing, but does not enforce a 1bit palette or pixel-grid QA.
- [Agent Sprite Forge](https://github.com/0x0funky/agent-sprite-forge) demonstrates a useful generation-plus-deterministic-processing architecture, but targets spritesheets and game assets rather than single-image composition-faithful conversion.
- [makew0rld/dither](https://github.com/makew0rld/dither) is a strong traditional dithering library, but it is not an agent skill and does not perform semantic redraw.

This repository is independently implemented. It delegates creative editing to the installed ImageGen skill and provides its own small Pillow-based two-color processor and validator.

## Presets

- `strict-dither` — default; bold dark contours, olive light field, ordered checker/stipple shading.
- `soft-ink` — lighter green pixel-ink contours with sparse Atkinson texture.
- `mono-print` — exact black and white with Floyd–Steinberg diffusion.

Every preset supports `artistic` and `binary` export. Binary export contains exactly two RGB colors.

## Install

Copy `skills/maka-1bit-skill` into your Codex skills directory:

```bash
cp -R skills/maka-1bit-skill ~/.codex/skills/maka-1bit-skill
```

Restart Codex, then invoke it with a local or attached input image:

```text
Use $maka-1bit-skill to convert this image with the strict-dither preset.
```

The deterministic scripts require Python 3.10+ and Pillow.

## Local verification

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/maka-1bit-skill
```

The test suite uses generated geometric fixtures. Personal reference images and generated test outputs are intentionally excluded from the public repository.

GitHub Actions repeats the pipeline tests on Python 3.10, 3.12, and 3.13.

## Repository layout

```text
skills/maka-1bit-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── qa-contract.md
│   └── style-presets.md
└── scripts/
    ├── postprocess_1bit.py
    └── validate_1bit.py
tests/
└── test_pipeline.py
```

## Release status

The skill was validated against private reference images. Those images and generated outputs are not published unless their owner explicitly approves it.

## License

MIT
