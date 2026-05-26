# -*- coding: utf-8 -*-
"""
平台相关的窗口检测模块
"""

import subprocess
import threading
import time
from typing import Optional

import platform as pf


# 浏览器识别模式（进程名或窗口标题）
BROWSER_PATTERNS = {
    "Windows": [
        "chrome", "Google Chrome",
        "firefox", "Firefox",
        "msedge", "Microsoft Edge",
        "opera", "Opera",
        "brave", "Brave",
        "chromium"
    ],
    "Darwin": [
        "Google Chrome",
        "Firefox",
        "Safari",
        "Brave",
        "Opera",
        "Chromium",
        "Microsoft Edge"
    ],
    "Linux": [
        "chrome", "Google Chrome",
        "firefox", "Firefox",
        "msedge", "Microsoft Edge",
        "opera", "Opera",
        "brave", "Brave",
        "chromium"
    ]
}

# 浏览器扩展识别模式（扩展窗口通常不包含浏览器名，但有这些关键词）
EXTENSION_PATTERNS = [
    # 钱包扩展
    "OKX", "MetaMask", "Wallet", "Phantom", "Rainbow",
    "Coinbase", "Trust Wallet", "Binance", "Exodus",
    # 其他常见扩展
    "Extension", "Chrome Extension", "Add-on", "Plugin",
    # 浏览器相关关键词
    "Chrome Web Store", "Extension Settings"
]

# 活动窗口缓存
_active_window_cache: Optional[str] = None
_cache_lock = threading.Lock()
_cache_time = 0
CACHE_TTL = 0.1  # 缓存100ms


def get_active_window_windows() -> Optional[str]:
    """获取Windows活动窗口标题"""
    try:
        import ctypes
        from ctypes import wintypes

        # Windows API 定义
        user32 = ctypes.windll.user32
        user32.GetForegroundWindow.argtypes = []
        user32.GetForegroundWindow.restype = wintypes.HWND

        user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
        user32.GetWindowTextLengthW.restype = wintypes.INT

        user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, wintypes.INT]
        user32.GetWindowTextW.restype = wintypes.INT

        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return None

        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return None

        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        return buffer.value
    except Exception:
        return None


def get_active_window_darwin() -> Optional[str]:
    """获取macOS活动窗口应用名称"""
    try:
        from AppKit import NSWorkspace
        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        if app:
            return app.localizedName()
        return None
    except ImportError:
        return None
    except Exception:
        return None


def get_active_window_linux() -> Optional[str]:
    """获取Linux活动窗口标题（使用xdotool）"""
    try:
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            capture_output=True,
            text=True,
            timeout=0.1
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        # 尝试使用 xprop
        try:
            result = subprocess.run(
                ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                capture_output=True,
                text=True,
                timeout=0.1
            )
            if result.returncode == 0:
                # 解析窗口ID
                parts = result.stdout.split()
                if len(parts) >= 5:
                    window_id = parts[-1].strip(',', '"')
                    # 获取窗口名称
                    result = subprocess.run(
                        ["xprop", "-id", window_id, "WM_NAME"],
                        capture_output=True,
                        text=True,
                        timeout=0.1
                    )
                    if result.returncode == 0 and '=' in result.stdout:
                        name = result.stdout.split('=', 1)[1].strip().strip('"')
                        return name
            return None
        except Exception:
            return None


def get_active_window_name() -> Optional[str]:
    """获取当前活动窗口名称（带缓存）"""
    global _active_window_cache, _cache_time

    now = time.time()
    if now - _cache_time < CACHE_TTL and _active_window_cache is not None:
        return _active_window_cache

    system = pf.system()
    window_name = None

    if system == "Windows":
        window_name = get_active_window_windows()
    elif system == "Darwin":
        window_name = get_active_window_darwin()
    elif system == "Linux":
        window_name = get_active_window_linux()

    with _cache_lock:
        _active_window_cache = window_name
        _cache_time = now

    return window_name


def is_browser_active() -> bool:
    """判断当前活动窗口是否为浏览器"""
    window_name = get_active_window_name()
    if not window_name:
        return False

    window_name_lower = window_name.lower()
    system = pf.system()

    # 检查浏览器模式
    patterns = BROWSER_PATTERNS.get(system, [])
    for pattern in patterns:
        if pattern.lower() in window_name_lower:
            return True

    # 检查浏览器扩展模式
    for pattern in EXTENSION_PATTERNS:
        if pattern.lower() in window_name_lower:
            return True

    return False


def is_wsl() -> bool:
    """检测是否运行在WSL环境"""
    if pf.system() != "Linux":
        return False
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except Exception:
        return False
