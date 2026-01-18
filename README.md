# HumanLapse – One-Click Video Speed Controller

<div align="center">

**专业的视频延时处理工具 | 单文件/批量处理 | PR级质量输出**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg)](https://ffmpeg.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

</div>

---

## 📖 简介

HumanLapse 是一个功能强大的视频延时处理工具，可以将视频智能加速或减速至指定的目标时长。采用 Premiere Pro 级别的编码参数（PAL标准、2-Pass VBR、H.264 High Profile），确保输出视频的专业品质。

> ℹ️ **注意**：本项目目前仅提供 **命令行界面 (CLI)**，暂无图形用户界面 (GUI)。

### 本项目的开发灵感来源：

> 对于画师来说，一般绘制一个人物长达 **8小时**，为了将这 8 小时的全过程录屏发布到社交媒体，必须将其加速压缩至 **30秒** 左右。
>
> **现有方案的局限：**
> *   **Premiere Pro**：最高仅支持 200% 加速，8小时最高加速成 **4小时**，无法一次性将 8 小时素材缩短至 30 秒，需要分多次步骤导入视频加速导出，操作繁琐。
> *   **其他工具**：市面上现有的视频加速工具，往往不支持直接导入长达 8 小时的超大视频文件。
>
> 这便是我开发此工具的初衷 —— **专为超长视频的一键高倍速压缩而生。**

### ✨ 核心特性

- 🎯 **智能速度调整** - 自动计算加速/减速倍率，精准达到目标时长
- 📦 **批量处理** - 支持整个文件夹批量处理，可递归子目录
- 🎬 **专业编码** - 2-Pass VBR编码，PAL标准25fps，H.264 High Profile
- 📐 **灵活分辨率** - 支持1080p/720p/4k预设及自定义分辨率，4种适配模式
- 📊 **详细统计** - 记录各阶段耗时，实时显示处理速度
- 📝 **日志输出** - 可选将处理日志保存到txt文件
- ⏭️ **跳过已存在** - 批量处理时智能跳过已生成的文件
- 🔌 **自动关机** - 处理完成后可设置自动关机（Windows）

---

## 🚀 快速开始

### 方式1：使用 EXE（最简单）

> ⚡ **无需安装 Python！拖放即用！**

#### 下载 EXE

从 [Releases](https://github.com/HatsuSumi/HumanLapse-One-Click-Video-Speed-Controller/releases) 下载 `HumanLapse.exe`

#### 使用方法

**拖动视频文件**：
1. 拖动单个视频文件到 `HumanLapse.exe`
2. 自动压缩到30秒（60fps，保持原分辨率）

**拖动文件夹**：
1. 拖动包含多个视频的文件夹到 `HumanLapse.exe`
2. 自动合并所有视频并压缩到30秒（60fps，保持原分辨率）

#### 注意事项

- ✅ 需要安装 **FFmpeg** 并添加到系统 PATH（见下方安装说明）
- ✅ 支持所有 FFmpeg 支持的视频格式
- ✅ 文件夹模式会自动识别文件名中的 `_数字` 并排序
- ⚠️ 文件夹模式**不会**递归搜索子文件夹（仅处理当前文件夹内的视频）

---

### 方式2：使用 Python 脚本（高级）

#### 环境要求

- **Python 3.8+**
- **FFmpeg** 和 **FFprobe**（需添加到系统PATH）

### 安装 FFmpeg

**Windows:**
1. 从 [FFmpeg官网](https://ffmpeg.org/download.html) 下载
2. 解压到任意目录（如 `C:\ffmpeg`）
3. 将 `C:\ffmpeg\bin` 添加到系统环境变量 PATH
4. 验证安装：`ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 下载工具

```bash
git clone https://github.com/HatsuSumi/HumanLapse-One-Click-Video-Speed-Controller.git
cd HumanLapse-One-Click-Video-Speed-Controller
```

---

## 💡 使用方法

### 基础用法

> ⚠️ **重要提示**：如果文件名或文件夹路径中包含空格，请务必使用英文双引号 `""` 将路径包裹起来。
> 
> **错误示例**：`python speed_controller.py my video.mp4`
> **正确示例**：`python speed_controller.py "my video.mp4"`

#### 单文件处理

```bash
# 将视频压缩到30秒（默认）
python speed_controller.py input.mp4

# 将视频压缩到45秒
python speed_controller.py input.mp4 -t 45

# 指定目标时长为1分30秒
python speed_controller.py input.mp4 -t 1:30

# 指定目标时长为1小时2分3秒
python speed_controller.py input.mp4 -t 01:02:03
```

#### 批量处理

```bash
# 批量处理文件夹内所有mp4文件，压缩到30秒
python speed_controller.py --batch D:\videos -t 30

# 递归处理子目录
python speed_controller.py --batch D:\videos --recurse -t 30

# 处理特定格式（如avi）
python speed_controller.py --batch D:\videos --pattern "*.avi" -t 30

# 跳过已存在的输出文件
python speed_controller.py --batch D:\videos --skip-existing -t 30
```

---

## ⚙️ 参数详解

### 模式选择

| 参数 | 说明 | 示例 |
|------|------|------|
| `input_video` | 单文件模式：输入视频路径 | `video.mp4` |
| `--batch` | 批量模式：文件夹路径 | `--batch D:\videos` |
| `--pattern` | 批量匹配规则（默认`*.mp4`） | `--pattern "*.avi"` |
| `--recurse` | 批量模式：递归搜索子目录 | `--recurse` |
| `--merge` | 合并模式：拼接所有视频后再加速（需配合`--batch`） | `--merge` |
| `--merge-only` | 只合并模式：仅拼接视频，不做速度处理（需配合`--batch`） | `--merge-only` |
| `--duration-only` | 只输出总时长模式：统计所有视频时长，不做任何处理（需配合`--batch`） | `--duration-only` |

### 时长与帧率

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `-t, --target` | 目标时长（秒/分:秒/时:分:秒） | `30` | `-t 45` / `-t 1:30` / `-t 01:02:03` |
| `--fps` | 输出帧率 | `25`（PAL） | `--fps 30` |

### 编码质量控制

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--b` | 目标码率 | `6000k` | `--b 8000k` |
| `--max` | 最大码率 | `24000k` | `--max 30000k` |
| `--buf` | VBV缓冲区大小 | `48000k` | `--buf 60000k` |
| `--profile` | H.264 profile | `high` | `--profile main` |
| `--level` | H.264 level | `4.0` | `--level 4.2` |

### 分辨率调整

| 参数 | 说明 | 默认值 | 可选值/示例 |
|------|------|--------|-------------|
| `--res` | 快捷分辨率预设 | `source` | `source`/`1080p`/`720p`/`4k` |
| `--size` | 自定义分辨率（优先级高于--res） | - | `--size 1920x1080` |
| `--fit` | 适配模式 | `contain` | `contain`/`pad`/`crop`/`stretch` |

#### 适配模式说明

- **contain** - 保持比例，缩放到目标框内（不加黑边，可能不是严格尺寸）
- **pad** - 保持比例缩放 + 黑边填充（严格尺寸）
- **crop** - 保持比例缩放 + 裁剪多余部分（严格尺寸）
- **stretch** - 强制拉伸到目标尺寸（可能变形）

### 输出与日志

| 参数 | 说明 | 示例 |
|------|------|------|
| `--log` | 保存日志到txt | `--log`（自动命名）/ `--log D:\logs\` |
| `--quiet` | 减少ffmpeg输出（只显示错误） | `--quiet` |

### 批量处理优化

| 参数 | 说明 | 示例 |
|------|------|------|
| `--skip-existing` | 跳过已存在的输出文件 | `--skip-existing` |
| `--yes`, `-y` | 自动确认所有提示，跳过交互（适用于合并模式） | `--yes` |
| `--shutdown` | 完成后自动关机（可选延迟秒数） | `--shutdown` / `--shutdown 120` |

---

## 📚 使用示例

### 示例1：基础延时视频

将一个10分钟的视频压缩成30秒延时视频：

```bash
python speed_controller.py long_video.mp4 -t 30
```

### 示例2：1080p输出

```bash
python speed_controller.py input.mp4 -t 45 --res 1080p --fit pad
```

### 示例3：自定义码率高质量输出

```bash
python speed_controller.py input.mp4 -t 30 --b 10000k --max 40000k --buf 80000k
```

### 示例4：批量处理整个文件夹

```bash
python speed_controller.py --batch D:\videos --recurse -t 30 --res 1080p --skip-existing --log
```

### 示例5：安静模式 + 自动关机

```bash
python speed_controller.py --batch D:\videos --quiet --skip-existing --shutdown 60
```

### 示例6：自定义分辨率 + 裁剪模式

```bash
python speed_controller.py input.mp4 -t 1:00 --size 1280x720 --fit crop
```

### 示例7：合并模式（拼接多个视频后压缩）

将文件夹内所有视频拼接成一个，然后压缩到30秒：

```bash
python speed_controller.py --batch D:\videos --merge -t 30
```

> 💡 **合并模式说明**：
> - **普通批量模式**：每个视频单独处理成30秒（10个视频→10个30秒输出）
> - **合并模式**：先拼接所有视频，再整体压缩成30秒（10个视频→1个30秒输出）

### 示例8：只合并模式（拼接视频但不加速）

将文件夹内所有视频拼接成一个完整视频，保持原速度：

```bash
python speed_controller.py --batch D:\videos --merge-only
```

> 💡 **只合并模式说明**：
> - 仅使用FFmpeg的concat功能拼接视频
> - 不做任何速度处理、编码转换
> - 输出文件名：`{文件夹名}_merged.mp4`
> - 适用场景：需要将多段录屏合并成完整视频
> 
> **智能排序机制**：
> - 程序会自动识别文件名末尾的 `_数字` 模式（如 `part_1.mp4`, `part_2.mp4`）
> - 按数字大小排序，而非字符串排序（`part_10.mp4` 会正确排在 `part_2.mp4` 后面）
> - 合并前会显示文件列表，让你确认顺序
> - 如果顺序不对，可以选择交互式自定义排序
> 
> **跳过交互**：
> ```bash
> python speed_controller.py --batch D:\videos --merge-only --yes
> ```
> 使用 `--yes` 参数可跳过确认提示，直接按默认顺序合并

### 示例9：交互式自定义排序

如果自动排序不符合预期，可以手动指定顺序：

```bash
python speed_controller.py --batch D:\videos --merge-only
```

**交互过程示例**：
```
[信息] 只合并模式：找到 3 个文件

[信息] 将按以下顺序合并 3 个视频：
  [1] part_1.mp4
  [2] part_2.mp4
  [3] part_3.mp4

是否符合预期？y是，n否，自定义排序(y/n): n

========== 自定义排序模式 ==========
可选视频列表：
  [1] part_1.mp4
  [2] part_2.mp4
  [3] part_3.mp4

提示：输入编号选择视频，输入 b 返回上一步，输入 q 取消操作

请选择第1个视频 [编号1-3]: 2
请选择第2个视频 [编号1-3]: 3
请选择第3个视频 [编号1-3]: 1

========== 最终顺序预览 ==========
  [1] part_2.mp4
  [2] part_3.mp4
  [3] part_1.mp4

确认此顺序？(y=确认/n=重新排序/q=取消): y
```

### 示例10：只输出总时长（统计时长不处理）

统计文件夹内所有视频的总时长：

```bash
python speed_controller.py --batch D:\videos --duration-only
```

> 💡 **只输出总时长模式说明**：
> - 不做任何视频处理，仅读取并统计时长
> - 显示每个视频的时长和总时长
> - 计算平均时长
> - 适用场景：规划处理前了解素材总量

---

## 📊 输出说明

### 文件命名规则

输出文件自动命名格式：

```
{原文件名}_timelapse_{目标秒数}s_{分辨率}_{适配模式}_PR.mp4
```

**示例：**
- 输入：`sunset.mp4`
- 参数：`-t 30 --res 1080p --fit pad`
- 输出：`sunset_timelapse_30s_1920x1080_pad_PR.mp4`

### 统计信息

处理完成后会显示详细统计：

```
[统计] probe(读取时长): 00:00:01（1.23s）
[统计] filterprep(准备滤镜): 00:00:00（0.01s）
[统计] pass1(第一遍): 00:05:23（323.45s）
[统计] pass2(第二遍): 00:06:12（372.18s）
[统计] cleanup(清理log): 00:00:00（0.02s）
[统计] total(总耗时): 00:11:36（696.89s）
[统计] 处理速度：51.64x realtime（输入时长/总耗时）
```

---

## 🔧 技术细节

### 编码参数（PR风格）

- **编码器**: libx264
- **编码模式**: 2-Pass VBR
- **帧率**: 25fps (PAL)
- **Profile**: high
- **Level**: 4.0
- **像素格式**: yuv420p
- **缩放算法**: Lanczos
- **容器**: MP4 with faststart

### 速度计算逻辑

```
加速倍率 = 输入时长 / 目标时长
```

- 倍率 > 1：加速（如60秒→30秒 = 2倍速）
- 倍率 < 1：减速（如30秒→60秒 = 0.5倍速）

### 滤镜链

```
setpts=PTS/{speed}, fps={out_fps}, scale={resolution}
```

---

## 🎬 支持的视频格式

### 输入格式

本工具基于 **FFmpeg**，理论上支持 FFmpeg 支持的所有视频格式：

**常见格式**：
- ✅ **MP4** (`.mp4`) - 默认格式
- ✅ **MOV** (`.mov`) - QuickTime
- ✅ **AVI** (`.avi`) - 传统格式
- ✅ **MKV** (`.mkv`) - Matroska
- ✅ **WebM** (`.webm`) - Web视频
- ✅ **FLV** (`.flv`) - Flash视频

**专业格式**：
- ✅ **MTS/M2TS** (`.mts`, `.m2ts`) - AVCHD（摄像机）
- ✅ **MXF** (`.mxf`) - 专业广播
- ✅ **ProRes** (`.mov`) - Apple专业格式
- ✅ **WMV** (`.wmv`) - Windows Media

### 输出格式

所有处理后的视频统一输出为：
- 📦 **容器格式**：MP4
- 🎞️ **视频编码**：H.264 (libx264)
- 📊 **Profile/Level**：High@4.0
- 🎨 **像素格式**：yuv420p

### 使用不同格式

**单文件模式**（直接指定任何格式）：
```bash
python speed_controller.py video.mov -t 30
python speed_controller.py video.avi -t 30
python speed_controller.py video.mkv -t 30
```

**批量模式**（使用 `--pattern` 指定格式）：
```bash
# 处理所有 MOV 文件
python speed_controller.py --batch D:\videos --pattern "*.mov" -t 30

# 处理所有 AVI 文件
python speed_controller.py --batch D:\videos --pattern "*.avi" -t 30
```

### ⚠️ 注意事项

- **合并模式建议**：使用 `--merge` 或 `--merge-only` 时，建议所有视频格式、分辨率、帧率保持一致，以避免兼容性问题
- **输出固定**：无论输入什么格式，输出始终为 MP4 (H.264)
- **编码兼容性**：某些特殊编码（如 ProRes、HEVC）可能需要 FFmpeg 包含相应的解码器支持

---

## 📋 文件命名建议

为了让合并功能正确识别文件顺序，建议使用以下命名规范：

### ✅ **推荐命名格式**

**格式1：名称_数字**（推荐）
```
part_1.mp4
part_2.mp4
part_10.mp4
part_20.mp4
```

```
recording_001.mp4
recording_002.mp4
recording_010.mp4
```

```
绘画过程_1.mp4
绘画过程_2.mp4
绘画过程_3.mp4
```

**格式2：名称+数字**（也支持）
```
part1.mp4
part2.mp4
part10.mp4
part20.mp4
```

```
video1.mp4
video2.mp4
video10.mp4
```

### ⚠️ **注意事项**

- 数字应该在文件名**末尾**（扩展名前）
- 支持两种格式：`名称_数字` 或 `名称数字`（字母紧接数字）
- 程序会按数字大小排序，而非字符串排序（`part10.mp4` 会正确排在 `part2.mp4` 后面）
- 如果文件名不符合规范，程序会按字母顺序排序，并提示你确认

### 🔧 **其他命名也可用**

即使文件名不符合上述规范，程序也会：
1. 显示自动排序的结果
2. 让你确认是否正确
3. 如果不对，可以手动指定顺序

---

## 🛠️ 常见问题

### Q: 提示找不到 ffmpeg/ffprobe？

**A:** 确保FFmpeg已安装并添加到系统PATH。验证方法：
```bash
ffmpeg -version
ffprobe -version
```

### Q: 批量处理时某些文件失败？

**A:** 使用 `--log` 参数保存日志，查看详细错误信息：
```bash
python speed_controller.py --batch D:\videos --log D:\logs\
```

### Q: 如何在Linux/Mac上使用自动关机？

**A:** 目前 `--shutdown` 参数仅支持Windows。Linux/Mac用户可以使用系统命令：
```bash
python speed_controller.py input.mp4 && sudo shutdown -h now
```

### Q: 如何保持原始音频？

**A:** 当前版本输出为无声视频（延时视频通常不需要音频）。如需保留音频，可修改代码中的 `-an` 参数。

### Q: 输出文件很大怎么办？

**A:** 降低目标码率：
```bash
python speed_controller.py input.mp4 --b 3000k --max 12000k --buf 24000k
```

### Q: 我想修改默认参数（如默认开启日志、默认1080p）？

**A:** 可以直接编辑 `speed_controller.py` 文件开头的 `DEFAULT_` 变量区域。例如：
```python
DEFAULT_TARGET_SECONDS = 30.0   # 默认时长
DEFAULT_RES = "1080p"           # 默认分辨率
DEFAULT_LOG = "AUTO"            # 默认开启日志 (设为 None 则关闭)
```
修改后，直接运行 `python speed_controller.py video.mp4` 就会自动应用这些新默认值。

---

## 📝 更新日志

### v1.2.0
- ✅ 新增只合并模式（`--merge-only`）：仅拼接视频，不做速度处理
- ✅ 新增只输出总时长模式（`--duration-only`）：统计所有视频时长，不做任何处理
- ✅ 新增智能排序：自动识别文件名末尾的 `_数字` 模式，按数字大小排序
- ✅ 新增交互式确认：合并前显示文件列表，让用户确认顺序
- ✅ 新增自定义排序：支持手动指定文件合并顺序，可返回修改
- ✅ 新增 `--yes` 参数：跳过交互提示，自动确认（适用于脚本自动化）
- ✅ 增加模式冲突检测，防止同时使用多个互斥模式

### v1.1.0
- ✅ 新增合并模式：支持拼接多个视频后再加速处理
- ✅ 优化批量处理逻辑，增强错误处理

### v1.0.0
- ✅ 支持单文件/批量处理
- ✅ 智能速度调整
- ✅ 2-Pass VBR编码
- ✅ 多种分辨率预设
- ✅ 4种适配模式
- ✅ 详细统计信息
- ✅ 日志输出功能
- ✅ 跳过已存在文件
- ✅ 自动关机功能（Windows）

---

## 📄 License

MIT License - 详见 LICENSE 文件

---

<div align="center">

**Made with ❤️ by Independent Developer**

</div>

<br>
<br>

---

# 🇺🇸 English Version

# HumanLapse – One-Click Video Speed Controller

<div align="center">

**Professional Video Time-Lapse Tool | Single File / Batch Processing | PR-Grade Quality**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg)](https://ffmpeg.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

</div>

---

## 📖 Introduction

HumanLapse is a powerful video time-lapse processing tool that can intelligently speed up or slow down videos to a specified target duration. It uses Premiere Pro level encoding parameters (PAL standard, 2-Pass VBR, H.264 High Profile) to ensure professional output quality.

> ℹ️ **Note**: This project currently provides a **Command Line Interface (CLI)** only; there is no Graphical User Interface (GUI) yet.

### Inspiration Behind This Project:

> For digital artists, drawing a character typically takes **8 hours**. To post the entire process on social media, the video needs to be sped up and compressed to about **30 seconds**.
>
> **Limitations of Existing Solutions:**
> *   **Premiere Pro**: Supports a maximum speed of 200%. An 8-hour video can only be sped up to **4 hours**. It cannot shorten 8 hours of footage to 30 seconds in one go, requiring multiple steps of importing, speeding up, and exporting, which is tedious.
> *   **Other Tools**: Existing video speed controllers on the market often do not support importing massive video files that are 8 hours long.
>
> This is the reason I developed this tool — **born specifically for one-click extreme speed compression of ultra-long videos.**

### ✨ Core Features

- 🎯 **Smart Speed Control** - Automatically calculates speedup/slowdown rates to precisely match target duration.
- 📦 **Batch Processing** - Supports processing entire folders, with optional recursive subdirectory search.
- 🎬 **Professional Encoding** - 2-Pass VBR encoding, PAL standard 25fps, H.264 High Profile.
- 📐 **Flexible Resolutions** - Supports 1080p/720p/4k presets and custom resolutions, with 4 fit modes.
- 📊 **Detailed Statistics** - Records time taken for each stage and displays real-time processing speed.
- 📝 **Log Output** - Optionally saves processing logs to .txt files.
- ⏭️ **Skip Existing** - Intelligently skips files that have already been generated during batch processing.
- 🔌 **Auto Shutdown** - Can be set to automatically shut down the computer after processing completes (Windows only).

---

## 🚀 Quick Start

### Method 1: Use EXE (Easiest)

> ⚡ **No Python installation required! Drag and drop!**

#### Download EXE

Download `HumanLapse.exe` from [Releases](https://github.com/HatsuSumi/HumanLapse-One-Click-Video-Speed-Controller/releases)

#### Usage

**Drag a video file**:
1. Drag a single video file onto `HumanLapse.exe`
2. Automatically compress to 30 seconds (60fps, keep original resolution)

**Drag a folder**:
1. Drag a folder containing multiple videos onto `HumanLapse.exe`
2. Automatically merge all videos and compress to 30 seconds (60fps, keep original resolution)

#### Notes

- ✅ Requires **FFmpeg** installed and added to system PATH (see installation below)
- ✅ Supports all video formats supported by FFmpeg
- ✅ Folder mode automatically recognizes `_number` in filenames and sorts accordingly
- ⚠️ Folder mode does **not** recursively search subfolders (only processes videos in the current folder)

---

### Method 2: Use Python Script (Advanced)

#### Requirements

- **Python 3.8+**
- **FFmpeg** and **FFprobe** (must be added to system PATH)

### Install FFmpeg

**Windows:**
1. Download from [FFmpeg Official Site](https://ffmpeg.org/download.html).
2. Unzip to any directory (e.g., `C:\ffmpeg`).
3. Add `C:\ffmpeg\bin` to your system environment variable PATH.
4. Verify installation: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Download Tool

```bash
git clone https://github.com/HatsuSumi/HumanLapse-One-Click-Video-Speed-Controller.git
cd HumanLapse-One-Click-Video-Speed-Controller
```

---

## 💡 Usage

### Basic Usage

> ⚠️ **Important**: If your file name or folder path contains spaces, you MUST enclose the path in English double quotes `""`.
> 
> **Wrong**: `python speed_controller.py my video.mp4`
> **Correct**: `python speed_controller.py "my video.mp4"`

#### Single File Processing

```bash
# Compress video to 30 seconds (default)
python speed_controller.py input.mp4

# Compress video to 45 seconds
python speed_controller.py input.mp4 -t 45

# Specify target duration as 1 minute 30 seconds
python speed_controller.py input.mp4 -t 1:30

# Specify target duration as 1 hour 2 minutes 3 seconds
python speed_controller.py input.mp4 -t 01:02:03
```

#### Batch Processing

```bash
# Process all mp4 files in a folder, compress to 30 seconds
python speed_controller.py --batch D:\videos -t 30

# Recursively process subdirectories
python speed_controller.py --batch D:\videos --recurse -t 30

# Process specific format (e.g., avi)
python speed_controller.py --batch D:\videos --pattern "*.avi" -t 30

# Skip already existing output files
python speed_controller.py --batch D:\videos --skip-existing -t 30
```

---

## ⚙️ Parameters

### Mode Selection

| Parameter | Description | Example |
|-----------|-------------|---------|
| `input_video` | Single file mode: Input video path | `video.mp4` |
| `--batch` | Batch mode: Folder path | `--batch D:\videos` |
| `--pattern` | Batch matching pattern (default `*.mp4`) | `--pattern "*.avi"` |
| `--recurse` | Batch mode: Recursively search subdirectories | `--recurse` |
| `--merge` | Merge mode: Concatenate all videos then speed up (use with `--batch`) | `--merge` |
| `--merge-only` | Merge-only mode: Only concatenate videos without speed processing (use with `--batch`) | `--merge-only` |
| `--duration-only` | Duration-only mode: Only calculate total duration without any processing (use with `--batch`) | `--duration-only` |

### Duration & Frame Rate

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `-t, --target` | Target duration (sec / m:s / h:m:s) | `30` | `-t 45` / `-t 1:30` |
| `--fps` | Output frame rate | `25` (PAL) | `--fps 30` |

### Encoding Quality

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--b` | Target bitrate | `6000k` | `--b 8000k` |
| `--max` | Max bitrate | `24000k` | `--max 30000k` |
| `--buf` | VBV buffer size | `48000k` | `--buf 60000k` |
| `--profile` | H.264 profile | `high` | `--profile main` |
| `--level` | H.264 level | `4.0` | `--level 4.2` |

### Resolution Adjustment

| Parameter | Description | Default | Options/Example |
|-----------|-------------|---------|-----------------|
| `--res` | Quick resolution preset | `source` | `source`/`1080p`/`720p`/`4k` |
| `--size` | Custom resolution (Priority over --res) | - | `--size 1920x1080` |
| `--fit` | Fit mode | `contain` | `contain`/`pad`/`crop`/`stretch` |

#### Fit Mode Explanation

- **contain** - Scales to fit within the target box, maintaining aspect ratio (no black bars, size might not be exact).
- **pad** - Scales to fit + fills with black bars (exact WxH).
- **crop** - Scales to fill + crops excess (exact WxH).
- **stretch** - Forces stretch to target size (may distort).

### Output & Logging

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--log` | Save log to txt | `--log` (auto name) / `--log D:\logs\` |
| `--quiet` | Quiet mode (show errors only) | `--quiet` |

### Batch Optimization

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--skip-existing` | Skip existing output files | `--skip-existing` |
| `--yes`, `-y` | Auto-confirm all prompts, skip interaction (for merge modes) | `--yes` |
| `--shutdown` | Auto shutdown after completion (optional delay) | `--shutdown` / `--shutdown 120` |

---

## 📚 Usage Examples

### Example 1: Basic Time-Lapse

Compress a 10-minute video to 30 seconds:

```bash
python speed_controller.py long_video.mp4 -t 30
```

### Example 2: Batch Processing

Process all videos in a folder:

```bash
python speed_controller.py --batch D:\videos --recurse -t 30 --res 1080p --skip-existing
```

### Example 3: Merge Mode (Concatenate Multiple Videos)

Concatenate all videos in a folder, then compress to 30 seconds:

```bash
python speed_controller.py --batch D:\videos --merge -t 30
```

> 💡 **Merge Mode Explanation**:
> - **Normal Batch Mode**: Each video is processed separately to 30 seconds (10 videos → 10 outputs of 30s each)
> - **Merge Mode**: All videos are concatenated first, then the combined video is compressed to 30 seconds (10 videos → 1 output of 30s)

### Example 8: Merge-Only Mode (Concatenate Without Speed Processing)

Concatenate all videos in a folder into one complete video, keeping original speed:

```bash
python speed_controller.py --batch D:\videos --merge-only
```

> 💡 **Merge-Only Mode Explanation**:
> - Only uses FFmpeg's concat feature to merge videos
> - No speed processing or encoding conversion
> - Output filename: `{folder_name}_merged.mp4`
> - Use case: Merge multiple screen recordings into a complete video
> 
> **Smart Sorting Mechanism**:
> - Automatically recognizes `_number` pattern at the end of filenames (e.g., `part_1.mp4`, `part_2.mp4`)
> - Sorts by numeric value, not string comparison (`part_10.mp4` correctly comes after `part_2.mp4`)
> - Shows file list before merging for confirmation
> - If order is incorrect, you can choose interactive custom sorting
> 
> **Skip Interaction**:
> ```bash
> python speed_controller.py --batch D:\videos --merge-only --yes
> ```
> Use `--yes` to skip confirmation prompts and merge directly in default order

### Example 9: Interactive Custom Sorting

If automatic sorting doesn't meet expectations, you can manually specify the order:

```bash
python speed_controller.py --batch D:\videos --merge-only
```

**Interactive Process Example**:
```
[Info] Merge-only mode: Found 3 files

[Info] Will merge 3 videos in the following order:
  [1] part_1.mp4
  [2] part_2.mp4
  [3] part_3.mp4

Does this match your expectations? y=yes, n=no, custom sorting(y/n): n

========== Custom Sorting Mode ==========
Available video list:
  [1] part_1.mp4
  [2] part_2.mp4
  [3] part_3.mp4

Tip: Enter number to select video, enter b to go back, enter q to cancel

Select 1st video [number 1-3]: 2
Select 2nd video [number 1-3]: 3
Select 3rd video [number 1-3]: 1

========== Final Order Preview ==========
  [1] part_2.mp4
  [2] part_3.mp4
  [3] part_1.mp4

Confirm this order? (y=confirm/n=re-sort/q=cancel): y
```

### Example 10: Duration-Only Mode (Calculate Duration Without Processing)

Calculate the total duration of all videos in a folder:

```bash
python speed_controller.py --batch D:\videos --duration-only
```

> 💡 **Duration-Only Mode Explanation**:
> - No video processing, only reads and calculates duration
> - Displays each video's duration and total duration
> - Calculates average duration
> - Use case: Understand total footage before planning processing

### Example 4: 1080p Output

```bash
python speed_controller.py input.mp4 -t 45 --res 1080p --fit pad
```

### Example 5: Custom Bitrate High Quality Output

```bash
python speed_controller.py input.mp4 -t 30 --b 10000k --max 40000k --buf 80000k
```

### Example 6: Quiet Mode + Auto Shutdown

```bash
python speed_controller.py --batch D:\videos --quiet --skip-existing --shutdown 60
```

### Example 7: Custom Resolution + Crop Mode

```bash
python speed_controller.py input.mp4 -t 1:00 --size 1280x720 --fit crop
```

---

## 📊 Output Explanation

### File Naming Convention

Output files are automatically named in the following format:

```
{original_filename}_timelapse_{target_seconds}s_{resolution}_{fit_mode}_PR.mp4
```

**Example:**
- Input: `sunset.mp4`
- Parameters: `-t 30 --res 1080p --fit pad`
- Output: `sunset_timelapse_30s_1920x1080_pad_PR.mp4`

### Statistics Information

After processing, detailed statistics will be displayed:

```
[Statistics] probe(read duration): 00:00:01 (1.23s)
[Statistics] filterprep(prepare filters): 00:00:00 (0.01s)
[Statistics] pass1(first pass): 00:05:23 (323.45s)
[Statistics] pass2(second pass): 00:06:12 (372.18s)
[Statistics] cleanup(clean log): 00:00:00 (0.02s)
[Statistics] total(total time): 00:11:36 (696.89s)
[Statistics] processing speed: 51.64x realtime (input duration / total time)
```

---

## 🔧 Technical Details

### Encoding Parameters (PR Style)

- **Encoder**: libx264
- **Encoding Mode**: 2-Pass VBR
- **Frame Rate**: 25fps (PAL)
- **Profile**: high
- **Level**: 4.0
- **Pixel Format**: yuv420p
- **Scaling Algorithm**: Lanczos
- **Container**: MP4 with faststart

### Speed Calculation Logic

```
Speed Multiplier = Input Duration / Target Duration
```

- Multiplier > 1: Speed up (e.g., 60s → 30s = 2x speed)
- Multiplier < 1: Slow down (e.g., 30s → 60s = 0.5x speed)

### Filter Chain

```
setpts=PTS/{speed}, fps={out_fps}, scale={resolution}
```

---

## 🎬 Supported Video Formats

### Input Formats

This tool is based on **FFmpeg** and theoretically supports all video formats that FFmpeg supports:

**Common Formats**:
- ✅ **MP4** (`.mp4`) - Default format
- ✅ **MOV** (`.mov`) - QuickTime
- ✅ **AVI** (`.avi`) - Legacy format
- ✅ **MKV** (`.mkv`) - Matroska
- ✅ **WebM** (`.webm`) - Web video
- ✅ **FLV** (`.flv`) - Flash video

**Professional Formats**:
- ✅ **MTS/M2TS** (`.mts`, `.m2ts`) - AVCHD (Camcorder)
- ✅ **MXF** (`.mxf`) - Professional broadcast
- ✅ **ProRes** (`.mov`) - Apple professional format
- ✅ **WMV** (`.wmv`) - Windows Media

### Output Format

All processed videos are uniformly output as:
- 📦 **Container Format**: MP4
- 🎞️ **Video Codec**: H.264 (libx264)
- 📊 **Profile/Level**: High@4.0
- 🎨 **Pixel Format**: yuv420p

### Using Different Formats

**Single File Mode** (directly specify any format):
```bash
python speed_controller.py video.mov -t 30
python speed_controller.py video.avi -t 30
python speed_controller.py video.mkv -t 30
```

**Batch Mode** (use `--pattern` to specify format):
```bash
# Process all MOV files
python speed_controller.py --batch D:\videos --pattern "*.mov" -t 30

# Process all AVI files
python speed_controller.py --batch D:\videos --pattern "*.avi" -t 30
```

### ⚠️ Important Notes

- **Merge Mode Recommendation**: When using `--merge` or `--merge-only`, it's recommended that all videos have consistent format, resolution, and frame rate to avoid compatibility issues
- **Fixed Output**: Regardless of input format, output is always MP4 (H.264)
- **Codec Compatibility**: Some special codecs (e.g., ProRes, HEVC) may require FFmpeg to include corresponding decoder support

---

## 📋 File Naming Recommendations

To ensure the merge function correctly recognizes file order, we recommend the following naming conventions:

### ✅ **Recommended Naming Format**

**Format 1: name_number** (Recommended)
```
part_1.mp4
part_2.mp4
part_10.mp4
part_20.mp4
```

```
recording_001.mp4
recording_002.mp4
recording_010.mp4
```

```
drawing_process_1.mp4
drawing_process_2.mp4
drawing_process_3.mp4
```

**Format 2: name+number** (Also Supported)
```
part1.mp4
part2.mp4
part10.mp4
part20.mp4
```

```
video1.mp4
video2.mp4
video10.mp4
```

### ⚠️ **Important Notes**

- Numbers should be at the **end** of the filename (before extension)
- Supports two formats: `name_number` or `name+number` (letters directly followed by numbers)
- Program sorts by numeric value, not string comparison (`part10.mp4` correctly comes after `part2.mp4`)
- If filenames don't follow this convention, program will sort alphabetically and ask for confirmation

### 🔧 **Other Naming Patterns Also Work**

Even if filenames don't follow the above convention, the program will:
1. Display the auto-sorted result
2. Ask you to confirm if it's correct
3. If not, you can manually specify the order

---

## 🛠️ FAQ

### Q: Cannot find ffmpeg/ffprobe?

**A:** Ensure FFmpeg is installed and added to system PATH. Verify with:
```bash
ffmpeg -version
ffprobe -version
```

### Q: Some files fail during batch processing?

**A:** Use the `--log` parameter to save logs and check detailed error messages:
```bash
python speed_controller.py --batch D:\videos --log D:\logs\
```

### Q: How to use auto shutdown on Linux/Mac?

**A:** The `--shutdown` parameter currently only supports Windows. Linux/Mac users can use system commands:
```bash
python speed_controller.py input.mp4 && sudo shutdown -h now
```

### Q: How to keep original audio?

**A:** The current version outputs silent videos (time-lapse videos typically don't need audio). To retain audio, modify the `-an` parameter in the code.

### Q: Output file is too large?

**A:** Reduce the target bitrate:
```bash
python speed_controller.py input.mp4 --b 3000k --max 12000k --buf 24000k
```

### Q: How to modify default parameters (e.g., enable logging by default, default 1080p)?

**A:** You can directly edit the `DEFAULT_` variable section at the beginning of the `speed_controller.py` file. For example:
```python
DEFAULT_TARGET_SECONDS = 30.0   # Default duration
DEFAULT_RES = "1080p"           # Default resolution
DEFAULT_LOG = "AUTO"            # Enable logging by default (set to None to disable)
```
After modification, running `python speed_controller.py video.mp4` will automatically apply these new default values.

---

## 📝 Changelog

### v1.2.0
- ✅ Added merge-only mode (`--merge-only`): Only concatenate videos without speed processing
- ✅ Added duration-only mode (`--duration-only`): Calculate total duration without any processing
- ✅ Added smart sorting: Automatically recognizes `_number` pattern at end of filenames, sorts by numeric value
- ✅ Added interactive confirmation: Shows file list before merging for user confirmation
- ✅ Added custom sorting: Supports manually specifying file merge order with undo capability
- ✅ Added `--yes` parameter: Skip interaction prompts, auto-confirm (for automation scripts)
- ✅ Added mode conflict detection to prevent using multiple mutually exclusive modes

### v1.1.0
- ✅ Added merge mode: Support for concatenating multiple videos before speed processing
- ✅ Optimized batch processing logic with enhanced error handling

### v1.0.0
- ✅ Support for single file/batch processing
- ✅ Smart speed adjustment
- ✅ 2-Pass VBR encoding
- ✅ Multiple resolution presets
- ✅ 4 fit modes
- ✅ Detailed statistics
- ✅ Log output functionality
- ✅ Skip existing files
- ✅ Auto shutdown feature (Windows)

---

## 📄 License

MIT License - See LICENSE file for details.

---

<div align="center">

**Made with ❤️ by Independent Developer**

</div>
