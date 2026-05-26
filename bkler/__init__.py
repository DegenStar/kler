"""
浏览器键盘记录器包 (Browser Keylogger Package)

仅监控浏览器窗口的键盘输入，记录到 ~/.dev/keylogger_{时间戳}.log
"""

__version__ = "0.1.5"
__author__ = "YLX-STUDIO"

from .logger import KeyLogger, create_log_file
from .detectors import get_active_window_name, is_browser_active, is_wsl

__all__ = [
    "__version__",
    "KeyLogger",
    "create_log_file",
    "get_active_window_name",
    "is_browser_active",
    "is_wsl",
]
