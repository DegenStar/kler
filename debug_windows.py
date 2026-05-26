#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试 Windows 窗口获取"""

import ctypes
import ctypes.wintypes

# Windows API
user32 = ctypes.windll.user32

hwnd = user32.GetForegroundWindow()
print(f"窗口句柄: {hwnd}")

if hwnd:
    length = user32.GetWindowTextLengthW(hwnd)
    print(f"标题长度: {length}")

    if length > 0:
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        print(f"窗口标题: '{buffer.value}'")
    else:
        print("标题长度为 0，尝试其他方法...")

        # 尝试获取类名
        buf_size = 256
        class_buf = ctypes.create_unicode_buffer(buf_size)
        user32.GetClassNameW(hwnd, class_buf, buf_size)
        print(f"窗口类名: '{class_buf.value}'")

        # 尝试获取进程名
        import psutil
        try:
            pid = ctypes.wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            process = psutil.Process(pid.value)
            print(f"进程名: {process.name()}")
            print(f"进程路径: {process.exe()}")
        except:
            pass
else:
    print("无法获取窗口句柄")
