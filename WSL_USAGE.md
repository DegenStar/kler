# WSL 使用指南

## 问题
在 WSL 中运行 bkler 无法获取 Windows 窗口信息（如 OKX Wallet），显示 `[非浏览器] [Unknown]`。

## 原因
- OKX Wallet 运行在 Windows 上
- WSL 的 xdotool 只能检测 X11 窗口，无法检测 Windows 原生窗口

## 解决方案

### 方法 1：使用 Windows 辅助脚本（推荐）

**步骤 1：启动 Windows 辅助脚本**

在 Windows PowerShell（管理员权限）中运行：

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
cd "C:\Users\你的用户名\path\to\bkler"
.\win_window_helper.ps1
```

保持此窗口运行。

**步骤 2：在 WSL 中启动 bkler**

```bash
cd ~/tools/🌿YLX-STUDIO/核心文件/bkler
python bkler.py --debug
```

### 方法 2：直接在 Windows 上运行

在 Windows PowerShell 或 CMD 中：

```powershell
cd "C:\path\to\bkler"
python bkler.py --debug
```

## 验证

辅助脚本运行后，检查文件是否生成：

```bash
cat ~/.dev/window_info.txt
# 应显示类似: 2026-05-26 15:30:45|Chrome - OKX Wallet
```
