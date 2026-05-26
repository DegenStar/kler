# Windows 窗口信息辅助脚本
# 运行在 Windows PowerShell 中，将窗口信息写入共享文件

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern int GetWindowTextLength(IntPtr hWnd);

    public static string GetActiveWindowTitle() {
        IntPtr hWnd = GetForegroundWindow();
        if (hWnd == IntPtr.Zero) return null;

        int length = GetWindowTextLength(hWnd);
        if (length == 0) return null;

        StringBuilder sb = new StringBuilder(length + 1);
        GetWindowText(hWnd, sb, sb.Capacity);
        return sb.ToString();
    }
}
"@

# WSL 可访问的路径
$outputFile = "\\wsl.localhost\Ubuntu\home\star\.dev\window_info.txt"

# 确保目录存在
$outputDir = Split-Path $outputFile -Parent
if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

Write-Host "窗口信息辅助服务已启动"
Write-Host "输出文件: $outputFile"
Write-Host "按 Ctrl+C 停止`n"

while ($true) {
    try {
        $title = [Win32]::GetActiveWindowTitle()
        if ($title) {
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            "$timestamp|$title" | Out-File -FilePath $outputFile -Encoding UTF8 -Force
        }
    } catch {
        # 忽略错误
    }
    Start-Sleep -Milliseconds 100
}
