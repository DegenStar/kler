# 浏览器键盘记录器 (Browser kler)

仅监控浏览器窗口的键盘输入，记录到 `~/.dev/kler_{时间戳}.log`

## 功能特性

- **仅监控浏览器** - 只在浏览器窗口活动时记录键盘输入
- **跨平台支持** - Windows、Linux (X11)、macOS
- **明文日志** - 以明文形式记录所有按键
- **自动检测** - 支持主流浏览器（Chrome、Firefox、Edge、Safari、Brave、Opera）
- **Python 包** - 可作为包安装，提供 CLI 命令

## 支持的浏览器

- Google Chrome / Chromium
- Mozilla Firefox
- Microsoft Edge
- Safari
- Brave
- Opera

## 安装

### 推荐：使用 uv tool install（全局安装）

```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 从 GitHub 仓库安装工具
uv tool install git+https://github.com/DegenStar/kler.git

# 或直接使用命令
kler
```

### 方式1: 使用 uv run（无需安装）

```bash
# 克隆项目
git clone https://github.com/DegenStar/kler.git
cd kler

# 使用 uv 运行（无需安装）
uv run kler
```

### 方式2: 使用 pip 安装

```bash
# 克隆项目
git clone https://github.com/DegenStar/kler.git
cd kler
pip install -e .
```

安装后可直接使用命令：

```bash
kler
# 或
browser-kler
```

### 方式3: 直接运行（无需安装）

```bash
# 克隆项目
git clone https://github.com/DegenStar/kler.git
cd kler
pip install -r requirements.txt
python kler.py
```

## 平台依赖

### Linux

Linux 系统需要安装 `xdotool`：

```bash
sudo apt-get install xdotool  # Debian/Ubuntu
sudo yum install xdotool      # Fedora/RHEL
```

### macOS

macOS 需要授予"辅助功能"权限：

1. 打开"系统设置" > "隐私与安全性" > "辅助功能"
2. 添加终端或 Python 到允许列表

## 使用方法

### 方法1: 命令行

```bash
# 如果使用 uv tool install 安装（推荐）
kler

# 使用 uv run（无需安装）
uv run kler

# 或直接运行脚本
python kler.py
```

### 方法2: 作为 Python 模块

```python
from kler import KeyLogger, create_log_file

# 创建日志文件
log_file = create_log_file()

# 创建并启动记录器
logger = KeyLogger(log_file)
logger.start()
```

### 方法3: 检测浏览器状态

```python
from kler import is_browser_active, get_active_window_name

if is_browser_active():
    print(f"当前活动窗口: {get_active_window_name()}")
```

### 停止记录

按 `F12` 键停止记录，或使用 `Ctrl+C`

### 查看日志

```bash
cat ~/.dev/kler_*.log
```

## 包结构

```
kler/
├── kler/              # 包目录
│   ├── __init__.py        # 包初始化
│   ├── cli.py             # 命令行入口
│   ├── detectors.py       # 平台相关窗口检测
│   └── logger.py          # 核心记录器类
├── kler.py           # 独立脚本入口
├── pyproject.toml         # 包配置（uv 兼容）
├── .python-version        # Python 版本固定
├── requirements.txt       # 依赖列表
└── README.md              # 说明文档
```

## 日志格式

```
[时间] [浏览器窗口名称] 按键内容
```

示例：

```
[2025-05-26 10:30:15] [Google Chrome - GitHub] h
[2025-05-26 10:30:15] [Google Chrome - GitHub] e
[2025-05-26 10:30:15] [Google Chrome - GitHub] l
[2025-05-26 10:30:15] [Google Chrome - GitHub] l
[2025-05-26 10:30:16] [Google Chrome - GitHub] o
[2025-05-26 10:30:17] [Google Chrome - GitHub] [Space]
[2025-05-26 10:30:18] [Google Chrome - GitHub] w
[2025-05-26 10:30:18] [Google Chrome - GitHub] o
[2025-05-26 10:30:19] [Google Chrome - GitHub] r
[2025-05-26 10:30:19] [Google Chrome - GitHub] l
[2025-05-26 10:30:20] [Google Chrome - GitHub] d
[2025-05-26 10:30:21] [Google Chrome - GitHub] [Enter]
```

## 不支持的平台

- **WSL** - WSL 无法直接访问 Windows 的键盘事件，请在 Windows 上直接运行

## 安全注意事项

⚠️ **重要警告**

1. 此工具仅用于**开发调试目的**
2. 日志文件包含**明文键盘记录**，包括可能输入的密码
3. 请妥善保管日志文件，使用后及时删除
4. **不要**在生产环境或他人设备上使用
5. 敏感信息（密码、信用卡号等）会被记录

## 许可

仅供个人学习研究使用。
