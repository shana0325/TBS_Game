# Unit Sprite Generator Guide

本文件说明：

- `generate_unit_sprites.py` 当前如何生成像素占位小人
- 如何批量生成或只生成部分单位
- 如何通过修改 `unit_sprite_presets.json` 扩展新单位
- 以后如果要新增新的 `feature`，应该修改哪些代码

---

## 1. 文件位置

相关文件：

- [generate_unit_sprites.py](/D:/PycharmProjects/TBS_Game/tools/generate_unit_sprites.py)
- [unit_sprite_presets.json](/D:/PycharmProjects/TBS_Game/tools/unit_sprite_presets.json)
- 输出目录：[assets/units](/D:/PycharmProjects/TBS_Game/assets/units)

职责划分：

- `generate_unit_sprites.py`
  - 负责读取预设
  - 负责绘制像素角色
  - 负责输出 PNG 文件

- `unit_sprite_presets.json`
  - 负责描述每个单位的外观配置
  - 后续新增单位通常只需要改这里

---

## 2. 当前生成逻辑

当前生成器使用的是：

```text
固定画布尺寸
+ 基础体型模板
+ 调色板
+ 可选部件 feature 叠加
```

生成流程如下：

1. 读取 `unit_sprite_presets.json`
2. 对每个单位预设创建一个透明背景 `pygame.Surface`
3. 根据 `base` 选择基础体型绘制函数
4. 按 `features` 列表顺序叠加额外部件
5. 保存到 `assets/units/<unit_id>.png`

这意味着：

- 风格统一主要来自相同的基础模板与有限的调色板结构
- 单位差异主要来自 `features`
- 后续新增单位不需要手动画完整像素图，可以通过“模板 + 配置”批量生成

---

## 3. 当前支持的基础模板（base）

当前脚本中支持的 `base`：

- `human`
  - 标准人形体型
  - 适合 Hero、Knight、Archer、Mage 等单位

- `goblin`
  - 更矮更宽的怪物体型
  - 适合 Goblin、Imp 等单位

- `orc`
  - 更厚重的体型，强调肩宽
  - 适合 Orc、Brute 等单位

这些模板在脚本中的对应函数为：

- `_draw_human_base(...)`
- `_draw_goblin_base(...)`
- `_draw_orc_base(...)`

如果以后要新增新的基础体型，例如：

- `skeleton`
- `slime`
- `beast`

则需要：

1. 新增一个 `_draw_xxx_base(...)` 函数
2. 将它注册到 `BASE_DRAWERS`
3. 在 JSON 中使用新的 `base` 名称

---

## 4. 当前支持的 feature

当前脚本中支持的 `feature` 如下：

- `cape`
- `headband`
- `sword`
- `helmet`
- `shield`
- `spear`
- `ears`
- `dagger`
- `tusks`
- `axe`
- `shoulders`

这些 feature 在脚本中的对应函数为：

- `_draw_cape(...)`
- `_draw_headband(...)`
- `_draw_sword(...)`
- `_draw_helmet(...)`
- `_draw_shield(...)`
- `_draw_spear(...)`
- `_draw_ears(...)`
- `_draw_dagger(...)`
- `_draw_tusks(...)`
- `_draw_axe(...)`
- `_draw_shoulders(...)`

并统一注册在：

```python
FEATURE_DRAWERS = {
    ...
}
```

### feature 的作用

feature 用来定义单位之间的识别性差异，例如：

- Hero：披风、头带、剑
- Knight：头盔、盾牌、长枪
- Goblin：尖耳朵、匕首
- Orc：獠牙、巨斧、肩甲

注意：

- feature 是在基础体型上叠加的
- `features` 列表顺序会影响覆盖关系
- 如果两个 feature 画在相同位置，后画的会覆盖先画的

---

## 5. 调色板（palette）说明

每个单位预设都带有一组调色板：

- `outline`
  - 外轮廓/描边色
  - 控制整体像素形状边缘

- `skin`
  - 皮肤色
  - 用于头部、手部等位置

- `primary`
  - 主服装色
  - 决定角色整体最显眼的颜色

- `secondary`
  - 副服装色 / 金属色 / 腿部颜色

- `accent`
  - 点缀色
  - 常用于饰带、武器头、徽记等

建议：

- 为了保持同风格，尽量继续沿用这五类颜色结构
- 不建议一开始扩展太多颜色槽位
- 每个单位总颜色数尽量控制在低数量范围内，避免风格变杂

---

## 6. 预设文件结构

`unit_sprite_presets.json` 中每个单位的结构如下：

```json
"hero": {
  "size": 32,
  "palette": {
    "outline": [26, 34, 44],
    "skin": [238, 205, 170],
    "primary": [74, 128, 222],
    "secondary": [226, 196, 88],
    "accent": [164, 73, 60]
  },
  "base": "human",
  "features": ["cape", "headband", "sword"]
}
```

字段说明：

- `size`
  - 画布尺寸
  - 当前建议固定为 `32`

- `palette`
  - 颜色定义

- `base`
  - 使用的基础体型模板

- `features`
  - 要叠加的部件列表

---

## 7. 如何批量生成

在项目根目录执行：

```powershell
D:\Anaconda\envs\TBS_Game\python.exe tools\generate_unit_sprites.py
```

效果：

- 读取 `unit_sprite_presets.json` 中所有单位
- 逐个生成对应 PNG
- 输出到 `assets/units/`

输出示例：

```text
generated: D:\PycharmProjects\TBS_Game\assets\units\hero.png
generated: D:\PycharmProjects\TBS_Game\assets\units\knight.png
```

适用场景：

- 刚修改完一批预设
- 想整体刷新所有占位图
- 新增多个单位后统一生成

---

## 8. 如何只生成部分单位

如果只想生成指定单位：

```powershell
D:\Anaconda\envs\TBS_Game\python.exe tools\generate_unit_sprites.py hero knight
```

效果：

- 只生成 `hero.png`
- 只生成 `knight.png`

适用场景：

- 只改了少数单位的预设
- 想快速迭代某个单位外观

---

## 9. 如何新增一个新单位

例如要新增 `archer`：

### 第一步：在 JSON 中新增预设

```json
"archer": {
  "size": 32,
  "palette": {
    "outline": [30, 34, 28],
    "skin": [228, 198, 164],
    "primary": [78, 120, 76],
    "secondary": [122, 88, 58],
    "accent": [214, 182, 92]
  },
  "base": "human",
  "features": ["headband"]
}
```

### 第二步：运行生成命令

```powershell
D:\Anaconda\envs\TBS_Game\python.exe tools\generate_unit_sprites.py archer
```

### 第三步：确认输出

查看：

- [assets/units/archer.png](/D:/PycharmProjects/TBS_Game/assets/units/archer.png)

如果以后战斗渲染逻辑按单位名称或显式 sprite 字段读取，这个文件就可以直接使用。

---

## 10. 如何新增一个新的 feature

如果已有 feature 不够用，例如你想新增：

- `bow`
- `staff`
- `horns`
- `robe`

则需要改 Python 脚本，而不只是改 JSON。

### 步骤 1：新增绘制函数

例如新增 `bow`：

```python
def _draw_bow(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    accent = palette["accent"]
    pygame.draw.rect(surface, outline, (23, 12, 2, 10))
    pygame.draw.rect(surface, accent, (24, 13, 1, 8))
```

### 步骤 2：注册到 `FEATURE_DRAWERS`

```python
FEATURE_DRAWERS = {
    ...
    "bow": _draw_bow,
}
```

### 步骤 3：在 JSON 中使用它

```json
"archer": {
  "size": 32,
  "palette": {...},
  "base": "human",
  "features": ["headband", "bow"]
}
```

### 步骤 4：重新生成

```powershell
D:\Anaconda\envs\TBS_Game\python.exe tools\generate_unit_sprites.py archer
```

---

## 11. 如何新增一个新的 base

如果你不只是加部件，而是要增加新的基础体型，例如：

- `skeleton`
- `slime`
- `wolf`

则流程是：

### 步骤 1：新增基础体型函数

例如：

```python
def _draw_skeleton_base(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    ...
```

### 步骤 2：注册到 `BASE_DRAWERS`

```python
BASE_DRAWERS = {
    "human": _draw_human_base,
    "goblin": _draw_goblin_base,
    "orc": _draw_orc_base,
    "skeleton": _draw_skeleton_base,
}
```

### 步骤 3：在 JSON 中使用新的 base

```json
"skeleton": {
  "size": 32,
  "palette": {...},
  "base": "skeleton",
  "features": ["sword"]
}
```

### 步骤 4：重新生成

---

## 12. 风格统一建议

为了保持同风格，建议遵守以下约束：

1. 尺寸固定为 `32x32`
2. 继续使用透明背景
3. 调色板尽量继续保持 `outline / skin / primary / secondary / accent`
4. 优先通过 `base + features` 组合差异，而不是每个单位单独写一套完整绘制逻辑
5. 每次只增加少量新 feature，避免生成器过快失控

这套工具的定位是：

- 占位资源生成器
- 快速批量生成同风格小人
- 在正式美术资源到位前提供稳定可用的角色表现

它不是：

- 精修像素美术工具
- 动画工具
- 多朝向精细角色编辑器

---

## 13. 当前脚本的限制

当前版本有以下限制：

1. 只生成静态单帧角色图
2. 没有朝向区分
3. 没有攻击/受击/待机动画
4. 没有职业专属高级绘制逻辑
5. 某些 feature 之间可能会有覆盖冲突
6. `features` 只是简单按顺序叠加，不带复杂层级系统

因此如果后续要继续扩展，建议优先顺序是：

1. 补更多 feature
2. 补更多 base
3. 再考虑是否要引入更复杂的图层系统

---

## 14. 推荐维护方式

推荐的维护顺序：

### 日常新增单位

优先只改：

- `unit_sprite_presets.json`

### 需要新的外观部件时

改：

- `generate_unit_sprites.py`
  - 新增 `_draw_xxx(...)`
  - 注册到 `FEATURE_DRAWERS`

### 需要新的种族/体型时

改：

- `generate_unit_sprites.py`
  - 新增 `_draw_xxx_base(...)`
  - 注册到 `BASE_DRAWERS`

---

## 15. 建议的后续扩展方向

如果之后继续演进，建议按以下顺序扩展：

1. 增加更多预设
   - `archer`
   - `mage`
   - `skeleton`
   - `priest`
   - `wolf`

2. 增加更多 feature
   - `bow`
   - `staff`
   - `robe`
   - `horns`
   - `crown`

3. 让 `units.json` 使用显式 `sprite` 字段
   - 避免未来继续依赖单位名称自动推断 PNG 文件名

4. 如果将来真的需要，再扩展多朝向或多帧动画

---

## 16. 总结

这套工具的核心思想是：

```text
用少量基础模板 + 少量 feature + 调色板
批量生成统一风格的角色占位图
```

对当前项目阶段来说，这样做的优点是：

- 成本低
- 易批量生成
- 风格统一
- 易扩展
- 可直接接入当前战斗渲染

如果只想继续加新角色，优先改：

- [unit_sprite_presets.json](/D:/PycharmProjects/TBS_Game/tools/unit_sprite_presets.json)

如果要扩展新部件或新体型，再改：

- [generate_unit_sprites.py](/D:/PycharmProjects/TBS_Game/tools/generate_unit_sprites.py)
