# Maka 1bit Skill

稳定版本：**1.0.0**

将现有栅格图像转换为忠于原构图的 1bit 风格像素艺术，并可选输出经过技术验证的严格双色图片。

Convert an existing raster image into composition-faithful 1bit pixel art with verified exact two-color export.

处理宠物肖像时，会在风格转换前额外检查面部结构、独特斑纹、身体比例、爪子和尾巴，保留个体身份。

整个流程包含两层：

1. 通过确定性缩小和风格化抖动，保留源图身份、构图与明暗结构；
2. 只有当直接处理无法保持画面可读性时，才进行可控的 ImageGen 明暗概括，并继续执行相同的确定性双色导出。

最终输出是严格双色、对齐像素网格的 PNG。平滑的 AI 剪影会被明确拒绝，因为它会丢失已通过测试的内部像素密度结构。

上传图片后，Skill 会暂停两次：先选择三种抖动风格之一，再选择六种双色色板之一。两项都确认后才开始处理。

## 风格

- `strict-dither` — 规则的 Bayer 棋盘 / 点阵明暗。
- `soft-ink` — 更轻盈、有机的 Atkinson 像素簇。
- `mono-print` — 细密的 Floyd–Steinberg 印刷纹理。

## 色板

- `olive-terminal` — `#0b0e08` / `#bac3a0`
- `soft-mint` — `#103b2b` / `#dcefc8`
- `classic-mono` — `#000000` / `#ffffff`
- `amber-screen` — `#2a1600` / `#f2c14e`
- `cobalt-ice` — `#071d3b` / `#b8dbff`
- `plum-paper` — `#2e102f` / `#efcfea`

任一种风格都可以使用任一种色板，共有 18 种确定性组合。每种组合都只输出两个 RGB 颜色。

## 安装

将 `skills/maka-1bit-skill` 复制到 Codex Skills 目录：

```bash
cp -R skills/maka-1bit-skill ~/.codex/skills/maka-1bit-skill
```

重启 Codex，然后附带或指定本地图片调用：

```text
使用 $maka-1bit-skill 处理这张图片。请先让我选择风格，再选择色板，然后开始处理。
```

英文调用仍然兼容：

```text
Use $maka-1bit-skill to convert this image. Ask me to choose a style and then a palette before processing.
```

确定性脚本要求 Python 3.10+ 和 Pillow。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/maka-1bit-skill
```

测试套件使用自动生成的几何测试图。个人参考图和生成的测试结果不会放入公开仓库。

GitHub Actions 会在 Python 3.10、3.12 和 3.13 上重复执行流程测试。

## 仓库结构

```text
skills/maka-1bit-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── qa-contract.md
│   ├── palette-presets.md
│   ├── pet-portraits.md
│   └── style-presets.md
└── scripts/
    ├── postprocess_1bit.py
    └── validate_1bit.py
tests/
└── test_pipeline.py
```

## 发布状态

版本 1.0.0 固定了确定性转换核心。发布范围见 [RELEASE_NOTES.md](RELEASE_NOTES.md)，可选边框、数据标签和海报布局计划见 [ROADMAP.md](ROADMAP.md)。

Skill 已使用私有参考图片完成验证，这些图片及生成结果不会进入公开仓库。

## 许可证

MIT
