# -*- coding: utf-8 -*-
"""
命令行入口模块
"""

import sys
import argparse
import platform

from .detectors import is_wsl, get_active_window_name, is_browser_active
from .logger import KeyLogger, create_log_file


def request_macos_accessibility_permission() -> bool:
    """
    请求 macOS 辅助功能权限
    如果权限未授予，会弹出系统授权窗口
    即使用户拒绝了，下次运行也会再次弹窗
    返回 True 表示有权限，False 表示无权限
    """
    if platform.system() != "Darwin":
        return True

    try:
        from Quartz import (
            AXIsProcessTrusted,
            AXIsProcessTrustedWithOptions,
            kAXTrustedCheckOptionPrompt
        )
        import CoreFoundation
        import subprocess

        # 检查是否有权限
        if AXIsProcessTrusted():
            return True

        # 每次都尝试弹窗（使用 Prompt 选项）
        options = CoreFoundation.CFDictionaryCreateMutable(None, 0, None, None)
        key = CoreFoundation.CFStringCreateWithCString(
            None, kAXTrustedCheckOptionPrompt, 0
        )
        value = CoreFoundation.kCFBooleanTrue
        CoreFoundation.CFDictionaryAddValue(options, key, value)

        AXIsProcessTrustedWithOptions(options)

        # 检查弹窗后是否获得了权限
        if AXIsProcessTrusted():
            return True

        # 仍未获得权限，打开系统设置页面
        # macOS Ventura 及更新版本
        subprocess.run([
            "open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
        ], stderr=subprocess.DEVNULL)

        return False

    except ImportError:
        # 没有 pyobjc，尝试直接打开设置
        import subprocess
        subprocess.run([
            "open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
        ], stderr=subprocess.DEVNULL)
        print("提示: 请在 系统设置 > 隐私与安全性 > 辅助功能 中允许终端访问", file=sys.stderr)
        return False
    except Exception:
        return False


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

    # macOS 权限检查（每次都会尝试，如果无权限会弹窗）
    if platform.system() == "Darwin":
        has_permission = request_macos_accessibility_permission()
        if not has_permission:
            print("\n需要授予辅助功能权限才能监控键盘输入", file=sys.stderr)
            print("请在弹出的系统窗口中允许，然后重新运行此程序\n", file=sys.stderr)
            sys.exit(1)

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
