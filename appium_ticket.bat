@echo off
chcp 65001 >nul
REM ============================================================
REM Appium + Android Emulator 抢票启动脚本
REM 前置条件:
REM   1. Android Studio 已安装并启动 AVD (emulator-5554)
REM   2. Node.js 已安装
REM   3. 大麦 App 已安装到模拟器并已登录账号
REM ============================================================

REM Step 1: 激活 venv
call joker\Scripts\activate

REM Step 2: 安装/检查 Appium (全局)
set APPIUM=%APPDATA%\npm\appium.cmd
where appium >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    IF NOT EXIST "%APPIUM%" (
        echo [INFO] 未检测到 Appium，正在安装...
        npm config set strict-ssl false
        npm install -g appium
        "%APPIUM%" driver install uiautomator2
    )
) ELSE (
    set APPIUM=appium
)
echo [INFO] Appium 已就绪

REM Step 3: 后台启动 Appium 服务
echo [INFO] 启动 Appium 服务 (端口 4723)...
start "Appium Server" cmd /c "%APPIUM% --port 4723 --log appium.log"
timeout /t 4 /nobreak >nul

REM Step 4: 运行 Appium 抢票脚本
python scripts\appium_simulator.py

REM Step 5: 保持窗口
pause
