"""
HumanLapse - 拖放式入口
支持拖动视频文件或文件夹到此程序，自动处理

默认设置：
- 单文件：压缩到30秒
- 文件夹：合并所有视频并压缩到30秒
- 帧率：60fps
- 分辨率：保持原分辨率
- 适配模式：contain
"""

import sys
import os
from pathlib import Path

# 导入主程序
from speed_controller import main as speed_main


def show_usage():
    """显示使用说明"""
    print("=" * 70)
    print(" " * 20 + "HumanLapse - 拖放式视频加速工具")
    print("=" * 70)
    print("\n📖 使用方法：")
    print("  1. 拖动单个视频文件到此程序 → 压缩到30秒")
    print("  2. 拖动文件夹到此程序 → 合并所有视频并压缩到30秒")
    print("\n⚙️  默认设置：")
    print("  - 目标时长：30秒")
    print("  - 帧率：60fps")
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
    # 没有参数：显示使用说明
    if len(sys.argv) < 2:
        show_usage()
        return
    
    # 获取拖放的路径
    target_path = Path(sys.argv[1])
    
    # 检查路径是否存在
    if not target_path.exists():
        print("=" * 70)
        print(f"❌ 错误：路径不存在")
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
        print("  - 目标时长：30秒")
        print("  - 帧率：60fps")
        print("  - 分辨率：保持原分辨率")
        print("  - 适配模式：contain")
        print("\n开始处理...\n")
        print("=" * 70 + "\n")
        
        # 设置参数
        sys.argv = [
            "speed_controller.py",
            str(target_path),
            "-t", "30",
            "--fps", "60",
            "--res", "source",
            "--fit", "contain"
        ]
        
    elif target_path.is_dir():
        # ========== 文件夹模式 ==========
        print("=" * 70)
        print("📁 检测到：文件夹")
        print(f"路径：{target_path}")
        print("=" * 70)
        print("\n⚙️  处理设置：")
        print("  - 模式：合并所有视频后压缩")
        print("  - 目标时长：30秒")
        print("  - 帧率：60fps")
        print("  - 分辨率：保持原分辨率")
        print("  - 适配模式：contain")
        print("  - 自动确认：是（跳过交互）")
        print("\n开始处理...\n")
        print("=" * 70 + "\n")
        
        # 设置参数
        sys.argv = [
            "speed_controller.py",
            "--batch", str(target_path),
            "--merge",
            "-t", "30",
            "--fps", "60",
            "--res", "source",
            "--fit", "contain",
            "--yes"  # 自动确认，跳过交互
        ]
    else:
        print("=" * 70)
        print(f"❌ 错误：不支持的路径类型")
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

