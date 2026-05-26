# -*- coding: utf-8 -*-
"""
命令行入口模块
"""

import sys
import argparse

from .detectors import is_wsl, get_active_window_name, is_browser_active
from .logger import KeyLogger, create_log_file


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="浏览器键盘记录器 - 监控浏览器窗口的键盘输入",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  bkler              # 正常模式，仅记录浏览器输入
  bkler --debug       # 调试模式，记录所有输入并显示实时窗口信息
  bkler --test        # 测试窗口检测
        """
    )

    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="调试模式：记录所有按键（不仅限于浏览器），显示实时窗口信息"
    )

    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="测试模式：仅测试窗口检测，不记录键盘"
    )

    args = parser.parse_args()

    # 检查是否在WSL环境
    if is_wsl():
        print("错误: 检测到 WSL 环境", file=sys.stderr)
        print("WSL 不支持键盘监控，请在 Windows 上直接运行此脚本", file=sys.stderr)
        sys.exit(1)

    # 测试模式
    if args.test:
        print("窗口检测测试模式")
        print("=" * 50)
        print(f"当前窗口: {get_active_window_name()}")
        print(f"是否为浏览器: {is_browser_active()}")
        print("=" * 50)
        return 0

    # 创建日志文件
    log_file = create_log_file()

    # 启动键盘记录器
    logger = KeyLogger(log_file, debug_mode=args.debug)

    try:
        logger.start()
    except KeyboardInterrupt:
        print("\n已停止记录")
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n日志已保存到: {log_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
