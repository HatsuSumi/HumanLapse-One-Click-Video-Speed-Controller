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

### 环境要求

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

### Requirements

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
