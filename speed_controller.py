import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from datetime import datetime


# ==============================================================================
#                             用户配置区域 (USER CONFIG)
# ------------------------------------------------------------------------------
#  提示：您可以直接修改下方的变量值，来改变工具的“默认行为”。
#  修改后，直接运行脚本（不加参数）就会自动使用这些新设置。
#  (注：命令行传入的参数优先级更高，会覆盖这里的默认值)
# ==============================================================================

# --- [1. 视频时长与帧率] ---
DEFAULT_TARGET_SECONDS = 30.0   # 默认目标时长（秒）。想压成60秒？改为 60.0
DEFAULT_FPS = 60                # 默认输出帧率。25 (PAL标准), 30 (NTSC), 60 (高帧率)

# --- [2. 画质与编码 (PR级参数)] ---
DEFAULT_TARGET_BITRATE = "6000k"    # 目标码率 (6Mbps)。数值越大画质越好，体积也越大
DEFAULT_MAX_BITRATE = "24000k"      # 最大码率限制 (应对复杂画面)
DEFAULT_BUFSIZE = "48000k"          # 缓冲区大小 (建议设为 max_bitrate 的 2 倍)
DEFAULT_PROFILE = "high"            # H.264 Profile (baseline / main / high)
DEFAULT_LEVEL = "4.0"               # H.264 Level (影响设备兼容性，4.0兼容性较好)

# --- [3. 分辨率与画面适配] ---
# 分辨率可选：
#   "source" : 保持原视频分辨率 (原画)
#   "1080p"  : 1920x1080
#   "720p"   : 1280x720
#   "4k"     : 3840x2160
DEFAULT_RES = "source"

# 适配模式可选 (当原视频比例与目标分辨率不同时)：
#   "contain" : 缩放以包含在框内 (无黑边，最终尺寸可能不严格等于目标)
#   "pad"     : 缩放并加黑边填充 (严格尺寸，电影感黑边)
#   "crop"    : 缩放并裁剪多余部分 (严格尺寸，画面会被切掉一部分)
#   "stretch" : 强制拉伸铺满 (画面会变形，不推荐)
DEFAULT_FIT = "contain"

# --- [4. 批量处理设置] ---
DEFAULT_PATTERN = "*.mp4"       # 批量匹配的文件后缀，例如 "*.mov", "*.avi"
DEFAULT_RECURSE = False         # True = 批量时自动搜索所有子文件夹; False = 仅当前文件夹
DEFAULT_SKIP_EXISTING = False   # True = 如果输出文件已存在，则跳过不处理 (防重复)
DEFAULT_MERGE = False           # True = 合并模式：拼接所有视频后再加速; False = 每个视频单独处理
DEFAULT_MERGE_ONLY = False      # True = 只合并不加速：仅拼接视频，不做速度处理
DEFAULT_DURATION_ONLY = False   # True = 只输出总时长：统计所有视频时长，不做任何处理

# --- [5. 日志与杂项] ---
# 日志设置：
#   None         : 关闭日志
#   "AUTO"       : 自动生成同名 .log.txt
#   "D:\\logs\\" : 指定日志存放目录
DEFAULT_LOG = "AUTO"

DEFAULT_QUIET = False           # True = 安静模式 (运行时少说话，只报错误)

# --- [6. 自动关机设置] ---
DEFAULT_SHUTDOWN_ENABLE = False # True = 任务完成后自动关机 (仅Windows有效，慎用！)
DEFAULT_SHUTDOWN_DELAY = 60     # 自动关机倒计时 (秒)


FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


# ----------------- 工具函数 -----------------
def is_windows() -> bool:
    return os.name == "nt"


def now_perf() -> float:
    return time.perf_counter()


def format_hms(seconds: float) -> str:
    s = int(round(seconds))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}"


def run_capture(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, encoding="utf-8", errors="ignore").strip()


def probe_duration_seconds(video_path: str) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path
    ]
    out = run_capture(cmd)
    data = json.loads(out)
    dur = float(data["format"]["duration"])
    if dur <= 0:
        raise RuntimeError("无法获取视频时长（duration<=0）。")
    return dur


def parse_duration(s: str) -> float:
    """
    支持：
    - "30" / "30.5"（秒）
    - "1:30"（分:秒）
    - "01:02:03"（时:分:秒）
    """
    s = s.strip()
    if ":" not in s:
        sec = float(s)
        if sec <= 0:
            raise ValueError("目标时长必须 > 0")
        return sec

    parts = s.split(":")
    if len(parts) == 2:
        m, sec = parts
        total = int(m) * 60 + float(sec)
    elif len(parts) == 3:
        h, m, sec = parts
        total = int(h) * 3600 + int(m) * 60 + float(sec)
    else:
        raise ValueError("时长格式不支持。用 30 / 1:30 / 01:02:03 这种格式。")

    if total <= 0:
        raise ValueError("目标时长必须 > 0")
    return total


def parse_size(s: str) -> tuple[int, int]:
    s = s.strip().lower().replace("×", "x")
    if "x" not in s:
        raise ValueError("size 格式应为 1920x1080")
    w, h = s.split("x", 1)
    w, h = int(w), int(h)
    if w <= 0 or h <= 0:
        raise ValueError("size 宽高必须 > 0")
    return w, h


def resolve_target_size(res: str | None, size: str | None) -> tuple[int, int] | None:
    """
    返回 (W,H) 或 None（不缩放）
    res 优先级低于 size：若指定了 size，就用 size。
    """
    if size:
        return parse_size(size)

    if not res or res == "source":
        return None

    res = res.lower()
    if res == "1080p":
        return (1920, 1080)
    if res == "720p":
        return (1280, 720)
    if res in ("4k", "2160p"):
        return (3840, 2160)

    raise ValueError("res 只支持 source/1080p/720p/4k")


def build_scale_filter(target_wh: tuple[int, int] | None, fit: str) -> str | None:
    """
    返回 ffmpeg 滤镜片段（不含 setpts/fps）
    fit:
      - contain：保持比例缩放到“尽量放进目标框”，不加黑边（可能不是严格 H）
      - pad：保持比例缩放 + 黑边补齐到严格 WxH
      - crop：保持比例缩放到铺满目标框 + 裁掉多余部分（严格 WxH）
      - stretch：强行拉伸到 WxH（严格 WxH，可能变形）
    """
    if target_wh is None:
        return None

    W, H = target_wh
    fit = fit.lower()

    if fit == "contain":
        return f"scale={W}:-2:flags=lanczos"
    if fit == "pad":
        return (
            f"scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2"
        )
    if fit == "crop":
        return (
            f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:{H}"
        )
    if fit == "stretch":
        return f"scale={W}:{H}:flags=lanczos"

    raise ValueError("fit 只支持 contain/pad/crop/stretch")


def extract_trailing_number(filename: str) -> int | None:
    """
    提取文件名末尾的数字部分（支持多种格式）
    例如：part_10.mp4 → 10
          part10.mp4 → 10
          video_5.avi → 5
          video5.avi → 5
          random.mp4 → None
    """
    # 尝试匹配：下划线+数字（part_10.mp4）
    match = re.search(r'_(\d+)(?:\.[^.]+)?$', filename)
    if match:
        return int(match.group(1))
    
    # 尝试匹配：字母+数字（part10.mp4）
    match = re.search(r'[a-zA-Z](\d+)(?:\.[^.]+)?$', filename)
    if match:
        return int(match.group(1))
    
    return None


def smart_sort_files(files: list[Path]) -> list[Path]:
    """
    智能排序：优先按文件名末尾的 _数字 排序
    如果没有 _数字，则按文件名字母顺序排序
    """
    def sort_key(path: Path) -> tuple:
        num = extract_trailing_number(path.name)
        if num is not None:
            # 有数字：按数字排序，数字相同则按文件名排序
            return (0, num, path.name.lower())
        else:
            # 无数字：放在后面，按文件名排序
            return (1, 0, path.name.lower())
    
    return sorted(files, key=sort_key)


def interactive_reorder(files: list[Path]) -> list[Path] | None:
    """
    交互式重新排序文件
    
    Returns:
        重新排序后的文件列表，如果用户取消则返回 None
    """
    print("\n========== 自定义排序模式 ==========")
    print("可选视频列表：")
    for i, f in enumerate(files, start=1):
        print(f"  [{i}] {f.name}")
    
    print("\n提示：输入编号选择视频，输入 b 返回上一步，输入 q 取消操作\n")
    
    ordered = []
    position = 0
    used_indices = set()
    
    while position < len(files):
        prompt = f"请选择第{position + 1}个视频 [编号1-{len(files)}]: "
        try:
            user_input = input(prompt).strip().lower()
            
            # 取消操作
            if user_input in ('q', 'quit', 'exit'):
                print("[信息] 已取消操作")
                return None
            
            # 返回上一步
            if user_input in ('b', 'back', 'u', 'undo'):
                if position > 0:
                    position -= 1
                    removed = ordered.pop()
                    removed_idx = files.index(removed) + 1
                    used_indices.discard(removed_idx)
                    print(f"[信息] 已撤销，返回第{position + 1}个位置")
                else:
                    print("[警告] 已经是第一个位置，无法返回")
                continue
            
            # 尝试解析为数字
            try:
                idx = int(user_input)
            except ValueError:
                print(f"[错误] 无效输入，请输入 1-{len(files)} 之间的数字，或 b 返回，或 q 取消")
                continue
            
            # 检查范围
            if idx < 1 or idx > len(files):
                print(f"[错误] 编号超出范围，请输入 1-{len(files)} 之间的数字")
                continue
            
            # 检查是否已使用
            if idx in used_indices:
                print(f"[错误] 编号 {idx} 已被选择，请选择其他视频")
                continue
            
            # 添加到排序列表
            ordered.append(files[idx - 1])
            used_indices.add(idx)
            position += 1
            
        except (EOFError, KeyboardInterrupt):
            print("\n[信息] 已取消操作")
            return None
    
    # 显示最终顺序
    print("\n========== 最终顺序预览 ==========")
    for i, f in enumerate(ordered, start=1):
        print(f"  [{i}] {f.name}")
    
    # 最终确认
    while True:
        try:
            confirm = input("\n确认此顺序？(y=确认/n=重新排序/q=取消): ").strip().lower()
            if confirm in ('y', 'yes'):
                return ordered
            elif confirm in ('n', 'no'):
                # 递归重新排序
                return interactive_reorder(files)
            elif confirm in ('q', 'quit', 'exit'):
                print("[信息] 已取消操作")
                return None
            else:
                print("[错误] 请输入 y、n 或 q")
        except (EOFError, KeyboardInterrupt):
            print("\n[信息] 已取消操作")
            return None


def confirm_file_order(files: list[Path], auto_yes: bool = False) -> list[Path] | None:
    """
    显示文件顺序并让用户确认
    
    Args:
        files: 已排序的文件列表
        auto_yes: 是否自动确认（跳过交互）
    
    Returns:
        确认后的文件列表，如果用户取消则返回 None
    """
    print(f"\n[信息] 将按以下顺序合并 {len(files)} 个视频：")
    for i, f in enumerate(files, start=1):
        print(f"  [{i}] {f.name}")
    
    if auto_yes:
        print("\n[信息] 自动确认模式，跳过交互")
        return files
    
    while True:
        try:
            response = input("\n是否符合预期？y是，n否，自定义排序(y/n): ").strip().lower()
            
            if response in ('y', 'yes'):
                return files
            elif response in ('n', 'no'):
                # 进入交互式排序
                reordered = interactive_reorder(files)
                if reordered is None:
                    return None
                return reordered
            else:
                print("[错误] 请输入 y 或 n")
        except (EOFError, KeyboardInterrupt):
            print("\n[信息] 已取消操作")
            return None


def shutdown_windows(delay_seconds: int = 60):
    if os.name != "nt":
        return
    print(f"[信息] 将在 {delay_seconds} 秒后关机。如需取消：运行 shutdown /a")
    subprocess.check_call(["shutdown", "/s", "/t", str(delay_seconds)])


def make_logger(log_path: Path | None):
    """
    返回 log(msg) 和 close()
    log 同时输出到控制台与 txt
    """
    if log_path is None:
        def _log(msg: str):
            print(msg)
        def _close():
            return
        return _log, _close

    log_path.parent.mkdir(parents=True, exist_ok=True)
    f = open(log_path, "w", encoding="utf-8", newline="\n")

    def _log(msg: str):
        print(msg)
        f.write(msg + "\n")
        f.flush()

    def _close():
        try:
            f.flush()
        finally:
            f.close()

    return _log, _close


def compute_output_path(
    input_path: Path,
    target_seconds: float,
    target_wh: tuple[int, int] | None,
    fit: str
) -> Path:
    out_tag = f"{target_seconds:g}s".replace(".", "p")
    res_tag = "src" if target_wh is None else f"{target_wh[0]}x{target_wh[1]}_{fit}"
    return input_path.with_name(f"{input_path.stem}_timelapse_{out_tag}_{res_tag}_PR.mp4")


def derive_log_path(log_spec: str | None, output_path: Path) -> Path | None:
    """
    log_spec:
      None     -> 不写日志
      "AUTO"   -> 输出同名 .log.txt
      其它路径 -> 单文件模式：写到该路径
                 批量模式：若传的是目录则写入该目录；若传的是文件则写到该文件所在目录并按输出名生成
    """
    if log_spec is None:
        return None
    if log_spec == "AUTO":
        return output_path.with_suffix(".log.txt")

    p = Path(log_spec)
    # 目录：每个输出一个日志
    if p.exists() and p.is_dir():
        return p / (output_path.stem + ".log.txt")
    # 以分隔符结尾也认为是目录
    s = str(log_spec)
    if s.endswith("\\") or s.endswith("/"):
        return Path(s) / (output_path.stem + ".log.txt")
    # 否则当作“文件路径”传入：批量时也不要所有视频写同一个文件，改成同目录分文件
    return p.parent / (output_path.stem + ".log.txt")


# ----------------- 单文件处理（含细分统计+可写日志） -----------------
def timelapse_one(
    input_path: Path,
    target_seconds: float,
    out_fps: int,
    target_bitrate: str,
    max_bitrate: str,
    bufsize: str,
    profile: str,
    level: str,
    res: str,
    size: str | None,
    fit: str,
    quiet: bool,
    log_spec: str | None,
    skip_existing: bool,
) -> tuple[Path, dict]:
    """
    返回 (output_path, stats)
    stats: probe/filterprep/pass1/pass2/cleanup/total/realtime/speed/dur
    """
    if not input_path.exists():
        raise FileNotFoundError(f"找不到文件：{input_path}")

    t_total0 = now_perf()

    # probe 阶段
    t0 = now_perf()
    dur = probe_duration_seconds(str(input_path))
    t_probe = now_perf() - t0

    speed = dur / target_seconds  # 自动加速/减速

    # 分辨率滤镜准备阶段
    t0 = now_perf()
    target_wh = resolve_target_size(res=res, size=size)
    scale_part = build_scale_filter(target_wh, fit)  # 可能为 None
    t_filterprep = now_perf() - t0

    output_path = compute_output_path(input_path, target_seconds, target_wh, fit)

    if skip_existing and output_path.exists():
        # 仍返回 stats，标记 skip
        return output_path, {
            "skipped": True,
            "reason": "output exists",
            "dur": dur,
            "speed": speed,
            "total": 0.0,
            "realtime": 0.0,
        }

    log_path = derive_log_path(log_spec, output_path)
    log, log_close = make_logger(log_path)

    try:
        log(f"[信息] 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if log_path:
            log(f"[信息] 日志文件：{log_path}")

        # 组滤镜链：setpts + fps + (可选 scale/pad/crop)
        vf_parts = [f"setpts=PTS/{speed}", f"fps={out_fps}"]
        if scale_part:
            vf_parts.append(scale_part)
        vf = ",".join(vf_parts)

        passlog = str(output_path.with_suffix("")) + "_passlog"
        null_sink = "NUL" if is_windows() else "/dev/null"

        log(f"[信息] 输入：{input_path}")
        log(f"[信息] 输入时长：{dur:.2f}s")
        log(f"[信息] 目标：{target_seconds:.2f}s | 加速倍率：{speed:.2f}x（>1加速，<1减速）")
        if target_wh is None:
            log(f"[信息] 分辨率：保持源分辨率")
        else:
            log(f"[信息] 分辨率：{target_wh[0]}x{target_wh[1]} | 适配：{fit} | 缩放：lanczos")
        log(f"[信息] 导出：{out_fps}fps | VBR 2次 | 目标 {target_bitrate} / 最大 {max_bitrate} | {profile}@{level}")
        log(f"[信息] 输出：{output_path}")

        ffmpeg_prefix = [FFMPEG, "-hide_banner"]
        if quiet:
            ffmpeg_prefix += ["-loglevel", "error"]

        common = [
            "-vf", vf,
            "-an",
            "-map_metadata", "-1",
            "-map_chapters", "-1",
            "-c:v", "libx264",
            "-profile:v", profile,
            "-level:v", level,
            "-pix_fmt", "yuv420p",
            "-b:v", target_bitrate,
            "-maxrate", max_bitrate,
            "-bufsize", bufsize,
            "-passlogfile", passlog
        ]

        # Pass 1
        t0 = now_perf()
        log("[信息] Pass 1 开始…")
        cmd1 = ffmpeg_prefix + ["-y", "-i", str(input_path)] + common + [
            "-pass", "1",
            "-f", "null", null_sink
        ]
        subprocess.check_call(cmd1)
        t_pass1 = now_perf() - t0
        log("[信息] Pass 1 完成。")

        # Pass 2
        t0 = now_perf()
        log("[信息] Pass 2 开始…")
        cmd2 = ffmpeg_prefix + ["-y", "-i", str(input_path)] + common + [
            "-pass", "2",
            "-movflags", "+faststart",
            str(output_path)
        ]
        subprocess.check_call(cmd2)
        t_pass2 = now_perf() - t0
        log("[信息] Pass 2 完成。")

        # cleanup
        t0 = now_perf()
        for suffix in ["", ".mbtree"]:
            p = Path(passlog + suffix)
            if p.exists():
                try:
                    p.unlink()
                except Exception:
                    pass
        t_cleanup = now_perf() - t0

        t_total = now_perf() - t_total0
        realtime = dur / t_total if t_total > 0 else 0.0

        log(f"[统计] probe(读取时长): {format_hms(t_probe)}（{t_probe:.2f}s）")
        log(f"[统计] filterprep(准备滤镜): {format_hms(t_filterprep)}（{t_filterprep:.2f}s）")
        log(f"[统计] pass1(第一遍): {format_hms(t_pass1)}（{t_pass1:.2f}s）")
        log(f"[统计] pass2(第二遍): {format_hms(t_pass2)}（{t_pass2:.2f}s）")
        log(f"[统计] cleanup(清理log): {format_hms(t_cleanup)}（{t_cleanup:.2f}s）")
        log(f"[统计] total(总耗时): {format_hms(t_total)}（{t_total:.2f}s）")
        log(f"[统计] 处理速度：{realtime:.2f}x realtime（输入时长/总耗时）")

        log(f"[完成] 输出：{output_path}")

        return output_path, {
            "skipped": False,
            "dur": dur,
            "speed": speed,
            "probe": t_probe,
            "filterprep": t_filterprep,
            "pass1": t_pass1,
            "pass2": t_pass2,
            "cleanup": t_cleanup,
            "total": t_total,
            "realtime": realtime,
        }

    finally:
        log_close()


# ----------------- 合并模式 -----------------
def merge_videos(files: list[Path], output_path: Path, quiet: bool, is_temp: bool = True) -> Path:
    """
    使用 FFmpeg concat 将多个视频拼接成一个文件
    
    Args:
        files: 要合并的视频文件列表
        output_path: 输出路径（用于确定输出目录和命名）
        quiet: 是否安静模式
        is_temp: True=创建临时文件; False=创建最终输出文件
    
    Returns:
        合并后的文件路径
    """
    if not files:
        raise ValueError("没有文件可供合并")
    
    # 创建 concat 列表文件
    concat_list = output_path.parent / f"_concat_list_{int(time.time())}.txt"
    try:
        with open(concat_list, "w", encoding="utf-8") as f:
            for video in files:
                # FFmpeg concat 格式：file 'path'
                # 路径中的单引号需要转义
                safe_path = str(video.absolute()).replace("'", "'\\''")
                f.write(f"file '{safe_path}'\n")
        
        # 根据 is_temp 决定输出文件名
        if is_temp:
            merged_file = output_path.parent / f"_temp_merged_{int(time.time())}.mp4"
        else:
            merged_file = output_path
        
        print(f"[信息] 正在合并 {len(files)} 个视频...")
        
        cmd = [FFMPEG, "-f", "concat", "-safe", "0", "-i", str(concat_list)]
        if quiet:
            cmd += ["-loglevel", "error"]
        cmd += ["-c", "copy", "-y", str(merged_file)]
        
        subprocess.check_call(cmd)
        
        print(f"[信息] 合并完成：{merged_file}")
        return merged_file
        
    finally:
        # 清理 concat 列表文件
        if concat_list.exists():
            try:
                concat_list.unlink()
            except Exception:
                pass


def merge_only(
    folder: Path,
    pattern: str,
    recurse: bool,
    quiet: bool,
    auto_yes: bool = False,
) -> Path | None:
    """
    只合并模式：收集所有视频 -> 拼接成一个文件（不做速度处理）
    
    Returns:
        输出文件路径，如果用户取消则返回 None
    """
    files = collect_files(folder, pattern, recurse)
    if not files:
        raise RuntimeError(f"[错误] 没找到匹配文件：{folder} / {pattern}（recurse={recurse}）")
    
    print(f"[信息] 只合并模式：找到 {len(files)} 个文件")
    
    # 确认文件顺序
    confirmed_files = confirm_file_order(files, auto_yes)
    if confirmed_files is None:
        return None
    
    # 输出文件名
    output_name = f"{folder.name}_merged.mp4"
    output_path = folder / output_name
    
    # 合并所有视频（直接输出最终文件）
    t0 = now_perf()
    final_output = merge_videos(confirmed_files, output_path, quiet, is_temp=False)
    t_total = now_perf() - t0
    
    print(f"\n[统计] 合并耗时：{format_hms(t_total)}（{t_total:.2f}s）")
    print(f"[完成] 只合并模式输出：{final_output}")
    
    return final_output


def duration_only(
    folder: Path,
    pattern: str,
    recurse: bool,
) -> tuple[float, int]:
    """
    只输出总时长模式：统计所有视频的总时长（不做任何处理）
    
    Returns:
        (总时长秒数, 文件数量)
    """
    files = collect_files(folder, pattern, recurse)
    if not files:
        print(f"[信息] 没找到匹配文件：{folder} / {pattern}（recurse={recurse}）")
        return 0.0, 0
    
    print(f"[信息] 只输出总时长模式：找到 {len(files)} 个文件")
    print(f"[信息] 正在读取视频时长...\n")
    
    total_duration = 0.0
    success_count = 0
    fail_count = 0
    
    for i, f in enumerate(files, start=1):
        try:
            dur = probe_duration_seconds(str(f))
            total_duration += dur
            success_count += 1
            print(f"  [{i}/{len(files)}] {f.name}")
            print(f"           时长: {format_hms(dur)} ({dur:.2f}s)")
        except Exception as e:
            fail_count += 1
            print(f"  [{i}/{len(files)}] {f.name}")
            print(f"           [失败] {e}")
    
    print(f"\n========== 统计结果 ==========")
    print(f"[统计] 成功读取：{success_count} 个")
    if fail_count > 0:
        print(f"[统计] 失败：{fail_count} 个")
    print(f"[统计] 总时长：{format_hms(total_duration)} ({total_duration:.2f}s)")
    
    # 计算平均时长
    if success_count > 0:
        avg_duration = total_duration / success_count
        print(f"[统计] 平均时长：{format_hms(avg_duration)} ({avg_duration:.2f}s)")
    
    return total_duration, success_count


def merge_and_process(
    folder: Path,
    pattern: str,
    recurse: bool,
    target_seconds: float,
    out_fps: int,
    target_bitrate: str,
    max_bitrate: str,
    bufsize: str,
    profile: str,
    level: str,
    res: str,
    size: str | None,
    fit: str,
    quiet: bool,
    log_spec: str | None,
    auto_yes: bool = False,
) -> Path | None:
    """
    合并模式：收集所有视频 -> 拼接成一个 -> 加速处理
    
    Returns:
        输出文件路径，如果用户取消则返回 None
    """
    files = collect_files(folder, pattern, recurse)
    if not files:
        raise RuntimeError(f"[错误] 没找到匹配文件：{folder} / {pattern}（recurse={recurse}）")
    
    print(f"[信息] 合并模式：找到 {len(files)} 个文件")
    
    # 确认文件顺序
    confirmed_files = confirm_file_order(files, auto_yes)
    if confirmed_files is None:
        return None
    
    # 输出文件名
    time_str = f"{target_seconds:g}s".replace(".", "p")
    output_name = f"{folder.name}_merged_timelapse_{time_str}.mp4"
    output_path = folder / output_name
    
    # 1. 合并所有视频
    temp_merged = None
    try:
        temp_merged = merge_videos(confirmed_files, output_path, quiet, is_temp=True)
        
        # 2. 对合并后的视频进行加速处理
        print(f"\n[信息] 开始处理合并后的视频...")
        final_output, stats = timelapse_one(
            input_path=temp_merged,
            target_seconds=target_seconds,
            out_fps=out_fps,
            target_bitrate=target_bitrate,
            max_bitrate=max_bitrate,
            bufsize=bufsize,
            profile=profile,
            level=level,
            res=res,
            size=size,
            fit=fit,
            quiet=quiet,
            log_spec=log_spec,
            skip_existing=False,
        )
        
        # 重命名输出文件（因为 timelapse_one 会自动生成名字）
        if final_output != output_path:
            final_output.rename(output_path)
            
            # 同时重命名日志文件（如果存在）
            if log_spec is not None:
                temp_log = final_output.with_suffix(".log.txt")
                if temp_log.exists():
                    final_log = output_path.with_suffix(".log.txt")
                    try:
                        temp_log.rename(final_log)
                        print(f"[信息] 日志文件已重命名：{final_log.name}")
                    except Exception as e:
                        print(f"[警告] 重命名日志文件失败：{e}")
        
        print(f"\n[完成] 合并模式输出：{output_path}")
        return output_path
        
    finally:
        # 清理临时合并文件及相关文件
        if temp_merged:
            # 清理临时视频文件
            if temp_merged.exists():
                try:
                    temp_merged.unlink()
                    print(f"[信息] 已清理临时文件：{temp_merged}")
                except Exception as e:
                    print(f"[警告] 清理临时视频文件失败：{e}")
            
            # 清理 passlog 文件（但保留日志文件）
            temp_stem = temp_merged.stem  # 不含扩展名的文件名
            temp_parent = temp_merged.parent
            
            # 只清理 passlog 文件，不清理 .log.txt
            for temp_file in temp_parent.glob(f"{temp_stem}*_passlog*"):
                try:
                    temp_file.unlink()
                    print(f"[信息] 已清理临时文件：{temp_file.name}")
                except Exception as e:
                    print(f"[警告] 清理临时文件失败：{temp_file.name} - {e}")


# ----------------- 批量模式 -----------------
def collect_files(folder: Path, pattern: str, recurse: bool) -> list[Path]:
    if recurse:
        files = list(folder.rglob(pattern))
    else:
        files = list(folder.glob(pattern))
    # 只要文件
    files = [p for p in files if p.is_file()]
    
    # 过滤掉临时文件和输出文件
    filtered_files = []
    for f in files:
        name = f.name
        # 排除临时文件
        if name.startswith('_temp_merged_'):
            continue
        if name.startswith('_concat_list_'):
            continue
        # 排除已处理的输出文件
        if '_timelapse_' in name and name.endswith('_PR.mp4'):
            continue
        if name.endswith('_merged.mp4'):
            continue
        # 保留
        filtered_files.append(f)
    
    # 智能排序：优先识别文件名末尾的数字
    files = smart_sort_files(filtered_files)
    return files


def batch_process(
    folder: Path,
    pattern: str,
    recurse: bool,
    target_seconds: float,
    out_fps: int,
    target_bitrate: str,
    max_bitrate: str,
    bufsize: str,
    profile: str,
    level: str,
    res: str,
    size: str | None,
    fit: str,
    quiet: bool,
    log_spec: str | None,
    skip_existing: bool,
) -> tuple[list[Path], list[tuple[Path, str]]]:
    files = collect_files(folder, pattern, recurse)
    if not files:
        print(f"[信息] 没找到匹配文件：{folder} / {pattern}（recurse={recurse}）")
        return [], []

    ok: list[Path] = []
    fail: list[tuple[Path, str]] = []
    skipped = 0

    t_batch0 = now_perf()
    print(f"[信息] 批量开始：{folder}")
    print(f"[信息] 匹配：{pattern} | recurse={recurse} | 共 {len(files)} 个")
    print(f"[信息] 参数：target={target_seconds}s fps={out_fps} res={res} size={size or '-'} fit={fit} VBR2 target={target_bitrate} max={max_bitrate}")

    for i, inp in enumerate(files, start=1):
        print(f"\n===== [{i}/{len(files)}] {inp} =====")
        try:
            outp, stats = timelapse_one(
                input_path=inp,
                target_seconds=target_seconds,
                out_fps=out_fps,
                target_bitrate=target_bitrate,
                max_bitrate=max_bitrate,
                bufsize=bufsize,
                profile=profile,
                level=level,
                res=res,
                size=size,
                fit=fit,
                quiet=quiet,
                log_spec=log_spec,
                skip_existing=skip_existing,
            )
            if stats.get("skipped"):
                skipped += 1
                print(f"[跳过] 已存在输出：{outp}")
            else:
                ok.append(outp)
        except Exception as e:
            msg = str(e)
            fail.append((inp, msg))
            print(f"[失败] {inp}\n       {msg}")

    t_batch = now_perf() - t_batch0
    print("\n========== 批量总结 ==========")
    print(f"[统计] 总耗时：{format_hms(t_batch)}（{t_batch:.2f}s）")
    print(f"[统计] 成功：{len(ok)} | 跳过：{skipped} | 失败：{len(fail)}")

    if fail:
        print("\n[失败列表]")
        for p, msg in fail[:20]:
            print(f"- {p}\n  {msg}")
        if len(fail) > 20:
            print(f"... 还有 {len(fail) - 20} 条失败未展开")

    return ok, fail


# ----------------- CLI -----------------
def main():
    parser = argparse.ArgumentParser(
        description="timelapse.py：单文件/批量 timelapse（PR风格：PAL/2-pass/VBR），支持自定义时长、分辨率、细分统计、可写日志txt"
    )

    # 单文件：可选
    parser.add_argument("input_video", nargs="?", help="输入视频路径（单文件模式）")

    # 批量
    parser.add_argument("--batch", help="批量处理文件夹路径（启用批量模式）")
    parser.add_argument("--pattern", default=DEFAULT_PATTERN, help='批量匹配规则（默认 "*.mp4"）')
    parser.add_argument("--recurse", action="store_true", default=DEFAULT_RECURSE, help="批量模式：递归子目录")
    parser.add_argument("--merge", action="store_true", default=DEFAULT_MERGE, help="合并模式：拼接所有视频后再加速（需配合 --batch 使用）")
    parser.add_argument("--merge-only", action="store_true", default=DEFAULT_MERGE_ONLY, help="只合并模式：仅拼接视频，不做速度处理（需配合 --batch 使用）")
    parser.add_argument("--duration-only", action="store_true", default=DEFAULT_DURATION_ONLY, help="只输出总时长模式：统计所有视频时长，不做任何处理（需配合 --batch 使用）")

    # 通用参数
    parser.add_argument("-t", "--target", default=str(DEFAULT_TARGET_SECONDS),
                        help="目标时长：秒(30) / 分:秒(1:30) / 时:分:秒(01:02:03)。默认 30")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="输出帧率，默认 25（PAL）")

    parser.add_argument("--b", dest="target_bitrate", default=DEFAULT_TARGET_BITRATE, help="目标码率，如 6000k")
    parser.add_argument("--max", dest="max_bitrate", default=DEFAULT_MAX_BITRATE, help="最大码率，如 24000k")
    parser.add_argument("--buf", dest="bufsize", default=DEFAULT_BUFSIZE, help="VBV bufsize，如 48000k")
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="H.264 profile，默认 high")
    parser.add_argument("--level", default=DEFAULT_LEVEL, help="H.264 level，默认 4.0")

    # 分辨率选项
    parser.add_argument("--res", default=DEFAULT_RES, help="快捷分辨率：source/1080p/720p/4k。默认 source")
    parser.add_argument("--size", default=None, help="自定义分辨率：例如 1920x1080（优先级高于 --res）")
    parser.add_argument("--fit", default=DEFAULT_FIT, help="适配模式：contain/pad/crop/stretch。默认 contain")

    # 日志输出
    parser.add_argument("--log", nargs="?", const="AUTO", default=DEFAULT_LOG,
                        help="将脚本输出同步写入txt。用法：--log（自动命名）或 --log D:\\logs\\（输出到目录）或 --log D:\\x.txt（批量时按目录分文件）")

    # 安静模式
    parser.add_argument("--quiet", action="store_true", default=DEFAULT_QUIET, help="减少 ffmpeg 输出（只显示 error）")

    # 批量：跳过已存在
    parser.add_argument("--skip-existing", action="store_true", default=DEFAULT_SKIP_EXISTING, help="若输出文件已存在则跳过（批量很实用）")
    
    # 自动确认（跳过交互）
    parser.add_argument("--yes", "-y", action="store_true", help="自动确认所有提示，跳过交互（适用于合并模式）")

    # 自动关机：单文件模式=本文件完成后关机；批量模式=全部完成后关机
    # default 根据 DEFAULT_SHUTDOWN_ENABLE 决定是 None 还是 延迟秒数
    _shutdown_default = str(DEFAULT_SHUTDOWN_DELAY) if DEFAULT_SHUTDOWN_ENABLE else None
    parser.add_argument("--shutdown", nargs="?", const=str(DEFAULT_SHUTDOWN_DELAY), default=_shutdown_default,
                        help=f"导出成功后自动关机，可选延迟秒数（默认{DEFAULT_SHUTDOWN_DELAY}）。批量模式：全部完成后关机。例：--shutdown 或 --shutdown 120")

    args = parser.parse_args()

    # 解析 target
    try:
        target_seconds = parse_duration(args.target)
    except Exception as e:
        raise SystemExit(f"[错误] target 参数不合法：{e}")

    # 解析 shutdown
    shutdown_delay = None
    if args.shutdown is not None:
        try:
            shutdown_delay = int(args.shutdown)
            if shutdown_delay < 0:
                raise ValueError
        except Exception:
            raise SystemExit("[错误] --shutdown 需要是非负整数秒数，比如 --shutdown 或 --shutdown 120")

    # 批量模式
    if args.batch:
        folder = Path(args.batch)
        if not folder.exists() or not folder.is_dir():
            raise SystemExit(f"[错误] batch 路径不是有效文件夹：{folder}")

        # 检查模式冲突
        mode_count = sum([args.merge, args.merge_only, args.duration_only])
        if mode_count > 1:
            raise SystemExit("[错误] --merge、--merge-only、--duration-only 只能选择一个")

        # 只输出总时长模式：统计所有视频时长
        if args.duration_only:
            try:
                duration_only(
                    folder=folder,
                    pattern=args.pattern,
                    recurse=args.recurse,
                )
            except Exception as e:
                raise SystemExit(f"[错误] 只输出总时长模式失败：{e}")
        # 只合并模式：拼接视频但不加速
        elif args.merge_only:
            try:
                result = merge_only(
                    folder=folder,
                    pattern=args.pattern,
                    recurse=args.recurse,
                    quiet=args.quiet,
                    auto_yes=args.yes,
                )
                if result is None:
                    print("[信息] 操作已取消")
                    return
            except Exception as e:
                raise SystemExit(f"[错误] 只合并模式失败：{e}")
        # 合并模式：拼接所有视频后再加速
        elif args.merge:
            try:
                result = merge_and_process(
                    folder=folder,
                    pattern=args.pattern,
                    recurse=args.recurse,
                    target_seconds=target_seconds,
                    out_fps=args.fps,
                    target_bitrate=args.target_bitrate,
                    max_bitrate=args.max_bitrate,
                    bufsize=args.bufsize,
                    profile=args.profile,
                    level=args.level,
                    res=args.res,
                    size=args.size,
                    fit=args.fit,
                    quiet=args.quiet,
                    log_spec=args.log,
                    auto_yes=args.yes,
                )
                if result is None:
                    print("[信息] 操作已取消")
                    return
            except Exception as e:
                raise SystemExit(f"[错误] 合并模式失败：{e}")
        else:
            # 普通批量模式：每个视频单独处理
            _, _ = batch_process(
                folder=folder,
                pattern=args.pattern,
                recurse=args.recurse,
                target_seconds=target_seconds,
                out_fps=args.fps,
                target_bitrate=args.target_bitrate,
                max_bitrate=args.max_bitrate,
                bufsize=args.bufsize,
                profile=args.profile,
                level=args.level,
                res=args.res,
                size=args.size,
                fit=args.fit,
                quiet=args.quiet,
                log_spec=args.log,
                skip_existing=args.skip_existing,
            )

        if shutdown_delay is not None:
            shutdown_windows(delay_seconds=shutdown_delay)
        return

    # 单文件模式
    if not args.input_video:
        raise SystemExit("[错误] 请输入 input_video（单文件模式）或使用 --batch（批量模式）")

    inp = Path(args.input_video)
    try:
        outp, stats = timelapse_one(
            input_path=inp,
            target_seconds=target_seconds,
            out_fps=args.fps,
            target_bitrate=args.target_bitrate,
            max_bitrate=args.max_bitrate,
            bufsize=args.bufsize,
            profile=args.profile,
            level=args.level,
            res=args.res,
            size=args.size,
            fit=args.fit,
            quiet=args.quiet,
            log_spec=args.log,
            skip_existing=args.skip_existing,
        )
        if stats.get("skipped"):
            print(f"[跳过] 已存在输出：{outp}")
        if shutdown_delay is not None:
            shutdown_windows(delay_seconds=shutdown_delay)
    except FileNotFoundError as e:
        raise SystemExit(f"[错误] {e}")
    except OSError as e:
        raise SystemExit(f"[错误] 系统找不到 ffmpeg/ffprobe。请确认已加入 PATH。详细：{e}")
    except ValueError as e:
        raise SystemExit(f"[错误] 参数错误：{e}")
    except subprocess.CalledProcessError as e:
        error_msg = f"[错误] ffmpeg 执行失败，返回码 {e.returncode}"
        if e.returncode == -28:
            error_msg += "\n[提示] 磁盘空间不足！请清理磁盘空间或更换输出位置。"
        raise SystemExit(error_msg)


if __name__ == "__main__":
    main()
