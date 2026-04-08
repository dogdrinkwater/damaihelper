@echo off
REM Step 1: 创建 venv 虚拟环境，命名为 joker（使用 Python 3.12）
py -3.12 -m venv joker

REM Step 2: 激活虚拟环境
call joker\Scripts\activate

REM Step 3: 安装依赖包
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

REM Step 4: 运行 gui.py
python gui.py

REM Step 5: 保持命令行窗口打开，直到用户关闭
pause
