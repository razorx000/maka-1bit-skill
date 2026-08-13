---
name: maka-1bit-skill
description: >-
  将现有照片、宠物肖像、插画、扫描件或生成的栅格图像转换为忠于原构图的 1bit 像素艺术；使用确定性缩放、明暗压缩、可控抖动、限定双色色板与自动质检。上传图片后，必须先让用户选择 strict-dither、soft-ink 或 mono-print，再从六种内置色板中选择一种；两项均确认后才能处理。适用于“图片转 1bit”“黑白抖动艺术”“单色像素艺术”“复古位图”“Game Boy 风格”，以及猫、狗或其他宠物的 1bit 肖像。English triggers: image to 1bit, one-bit, monochrome pixel art, black-and-white dither art, retro bitmap art, Game Boy-like art, pet portrait, cat portrait, dog portrait. 不适用于普通灰度转换、没有输入图片的通用像素画创作、矢量描摹、spritesheet 或必须保持照片真实感的编辑。
---

# Maka 1bit Skill

保留源图构图与主体身份。采用确定性的双色压缩：先缩小原图，将连续明暗概括为与风格对应的像素密度，应用所选色板，再按整数网格放大。不得用平滑的矢量剪影替代源图。

## 必选步骤

- 要求提供一张待处理图片。
- 必须取得明确的风格和色板选择，不得假设默认值。
- 图片上传后，先询问风格并暂停。必须完整展示：
  1. `strict-dither` — 规则机械的 Bayer 网格与利落明暗过渡
  2. `soft-ink` — 更轻盈、有机的 Atkinson 像素簇与开放亮部
  3. `mono-print` — 细密的 Floyd–Steinberg 印刷纹理与较完整的明暗保留
- 用户选定风格后，再询问色板并暂停。必须展示 [references/palette-presets.md](references/palette-presets.md) 中的六个选项及两种十六进制颜色。
- 如有原生交互式选择控件，优先使用；否则提供简短编号列表，请用户回复编号或名称。
- 如果初始请求已经指定其中一项，只询问另一项；如果两项都已指定，立即处理。
- 在两项选择都明确前，不得进行非安全必需的图片检查、运行处理器或生成输出。
- 默认输出严格双色 PNG。
- 可以接受可选的裁切要求、逻辑分辨率和输出缩放，不得因此增加新的必选问题。

处理前阅读 [references/style-presets.md](references/style-presets.md) 和 [references/palette-presets.md](references/palette-presets.md)。遇到宠物或动物时，另读 [references/pet-portraits.md](references/pet-portraits.md)。接受最终结果前阅读 [references/qa-contract.md](references/qa-contract.md)。

## 边界

- 除非用户要求改变，否则保留主体数量、身份、姿势、拍摄角度、空间关系、裁切和宽高比。
- 在允许缩小合并细微纹理的同时，保留辨识度和明暗层级，使细节形成连贯的抖动像素簇。
- 不得新增、删除、镜像、移动或虚构斑纹、解剖结构、道具、文字、边框、标志或水印。
- 不模仿在世艺术家，只将参考图转译为可观察的色板与抖动特征。
- 不得覆盖输入图片，另存为新的 PNG。
- 不得把平滑的黑白剪影称为 1bit 像素艺术；必须用像素密度或结构性像素簇保留内部体积。

## 流程

1. 通过第一道必选步骤取得风格选择。
2. 通过第二道必选步骤取得色板选择。
3. 检查输入图片和可选的风格参考图。
4. 记录不变量：主体身份、姿势、可见特征、裁切、前后景关系以及禁止新增的内容。处理宠物时，按 [references/pet-portraits.md](references/pet-portraits.md) 建立身份清单。
5. 直接处理原图：

   ```bash
   python3 scripts/postprocess_1bit.py \
     --input <original-image> \
     --output <final.png> \
     --style <selected-style> \
     --palette <selected-palette>
   ```

   使用 `--logical-long-edge` 控制概括程度：数值越低，细节合并越强；数值越高，保留的细小身份特征越多。`--scale` 仅用于按整数倍最近邻放大。只有当用户明确提供自定义双色时，才同时传入 `--dark` 和 `--light`，不用 `--palette`。
6. 验证输出：

   ```bash
   python3 scripts/validate_1bit.py \
     --input <final.png> \
     --source <original-image> \
     --pixel-scale 4
   ```

7. 分别以缩略图尺寸和 100% 缩放检查原图与成品。核对身份、明暗层级、像素簇及 [references/qa-contract.md](references/qa-contract.md) 中的全部规则。
8. 每次只调整一个变量。定义性特征消失时提高逻辑分辨率；无关细节过多时降低逻辑分辨率。只有在分辨率调整后，才调整对比度、阈值或抖动方法。
9. 只有当直接转换无法保留可读的主体结构时，才加载 `$imagegen`，生成一张严格锁定构图的明暗概括中间图。保留主体身份与大块明暗面。不得让 ImageGen 直接生成最终 1bit 效果，也不得直接交付 AI 中间图；必须继续执行步骤 5–8。
10. 在回复中内嵌最终 PNG，并报告文件路径、风格、色板名称与颜色、逻辑分辨率、缩放倍数、方法和验证结果。

## 执行选择

- 照片、宠物、肖像和所有身份敏感主体，优先直接进行确定性转换。
- 比较不同风格或色板时，每个组合都使用同一张原图或同一张已确认的中间图。
- 所有阶段均保持非破坏性且可复现。
- 对白色、黑色或低对比度宠物，先调整逻辑分辨率与对比度，再考虑 AI。

## 失败处理

- 验证器报告超过两种颜色或像素网格错位时，从同一源图重新执行确定性处理。
- 小特征消失时，先提高 `--logical-long-edge`，再考虑改色板或使用 AI。
- 结果过于写实时，降低 `--logical-long-edge`，加强确定性概括。
- 可选 AI 中间图偏离源图时，丢弃中间图并回到原图。
