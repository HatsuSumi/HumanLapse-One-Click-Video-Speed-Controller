"""
HumanLapse - 拖放式入口
支持拖动视频文件或文件夹到此程序，自动处理

默认设置：
- 单文件：压缩到 exe 文件名指定的秒数（默认30秒）
- 文件夹：合并所有视频并压缩到 exe 文件名指定的秒数（默认30秒）
- 帧率：60fps
- 分辨率：保持原分辨率
- 适配模式：contain
"""

import re
import sys
from pathlib import Path

# 导入主程序
from speed_controller import main as speed_main


DEFAULT_TARGET_SECONDS = 30
DEFAULT_FPS = 60
DEFAULT_RES = "source"
DEFAULT_FIT = "contain"


def detect_target_seconds() -> int:
    """从当前可执行文件/脚本名中提取目标秒数，默认 30 秒。"""
    exe_name = Path(sys.argv[0]).stem
    match = re.search(r'_(\d+)s$', exe_name, re.IGNORECASE)
    if not match:
        return DEFAULT_TARGET_SECONDS

    seconds = int(match.group(1))
    return seconds if seconds > 0 else DEFAULT_TARGET_SECONDS


def show_usage(target_seconds: int):
    """显示使用说明"""
    print("=" * 70)
    print(" " * 20 + "HumanLapse - 拖放式视频加速工具")
    print("=" * 70)
    print("\n📖 使用方法：")
    print(f"  1. 拖动单个视频文件到此程序 → 压缩到{target_seconds}秒")
    print(f"  2. 拖动文件夹到此程序 → 合并所有视频并压缩到{target_seconds}秒")
    print("\n⚙️  默认设置：")
    print(f"  - 目标时长：{target_seconds}秒")
    print(f"  - 帧率：{DEFAULT_FPS}fps")
    print("  - 分辨率：保持原分辨率")
    print("  - 适配模式：contain（保持比例）")
    print("\n💡 提示：")
    print("  - 输出文件会保存在原文件/文件夹的同一位置")
    print("  - 文件夹模式会自动识别文件名中的 _数字 并排序")
    print("  - 处理过程中会显示详细进度信息")
    print("\n" + "=" * 70)
    print("\n按任意键退出...")
    input()


def drag_entry():
    """
    拖放入口：处理拖放的文件/文件夹
    """
    target_seconds = detect_target_seconds()

    # 没有参数：显示使用说明
    if len(sys.argv) < 2:
        show_usage(target_seconds)
        return

    # 获取拖放的路径
    target_path = Path(sys.argv[1])

    # 检查路径是否存在
    if not target_path.exists():
        print("=" * 70)
        print("❌ 错误：路径不存在")
        print(f"路径：{target_path}")
        print("=" * 70)
        input("\n按任意键退出...")
        return

    # 判断是文件还是文件夹
    if target_path.is_file():
        # ========== 单文件模式 ==========
        print("=" * 70)
        print("📹 检测到：单个视频文件")
        print(f"文件名：{target_path.name}")
        print(f"位置：{target_path.parent}")
        print("=" * 70)
        print("\n⚙️  处理设置：")
        print(f"  - 目标时长：{target_seconds}秒")
        print(f"  - 帧率：{DEFAULT_FPS}fps")
        print("  - 分辨率：保持原分辨率")
        print(f"  - 适配模式：{DEFAULT_FIT}")
        print("\n开始处理...\n")
        print("=" * 70 + "\n")

        # 设置参数
        sys.argv = [
            "speed_controller.py",
            str(target_path),
            "-t", str(target_seconds),
            "--fps", str(DEFAULT_FPS),
            "--res", DEFAULT_RES,
            "--fit", DEFAULT_FIT
        ]

    elif target_path.is_dir():
        # ========== 文件夹模式 ==========
        print("=" * 70)
        print("📁 检测到：文件夹")
        print(f"路径：{target_path}")
        print("=" * 70)
        print("\n⚙️  处理设置：")
        print("  - 模式：合并所有视频后压缩")
        print(f"  - 目标时长：{target_seconds}秒")
        print(f"  - 帧率：{DEFAULT_FPS}fps")
        print("  - 分辨率：保持原分辨率")
        print(f"  - 适配模式：{DEFAULT_FIT}")
        print("  - 自动确认：是（跳过交互）")
        print("\n开始处理...\n")
        print("=" * 70 + "\n")

        # 设置参数
        sys.argv = [
            "speed_controller.py",
            "--batch", str(target_path),
            "--merge",
            "-t", str(target_seconds),
            "--fps", str(DEFAULT_FPS),
            "--res", DEFAULT_RES,
            "--fit", DEFAULT_FIT,
            "--yes"
        ]
    else:
        print("=" * 70)
        print("❌ 错误：不支持的路径类型")
        print(f"路径：{target_path}")
        print("=" * 70)
        input("\n按任意键退出...")
        return

    # 调用主程序
    try:
        speed_main()
        print("\n" + "=" * 70)
        print("✅ 处理完成！")
        print("=" * 70)
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("⚠️  用户中断操作")
        print("=" * 70)
    except SystemExit as e:
        # 捕获 SystemExit（主程序的错误退出）
        print("\n" + "=" * 70)
        print(f"❌ 处理失败（错误码：{e.code}）")
        print("=" * 70)
        print("\n💡 可能的原因：")
        print("  - 磁盘空间不足")
        print("  - FFmpeg 未安装或未添加到 PATH")
        print("  - 视频文件损坏")
        print("  - 文件路径包含特殊字符")
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ 处理失败：{e}")
        print("=" * 70)

    input("\n按任意键退出...")


if __name__ == "__main__":
    drag_entry()

