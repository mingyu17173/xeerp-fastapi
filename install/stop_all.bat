@echo off
chcp 65001
echo 关闭所有 Python 服务...
taskkill /f /im python.exe
echo 已关闭！
pause