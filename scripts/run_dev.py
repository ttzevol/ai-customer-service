#!/usr/bin/env python3
"""
Development Runner - 开发模式运行脚本
"""

import os
import sys

# 确保data目录存在
os.makedirs("./data", exist_ok=True)
os.makedirs("./data/chroma", exist_ok=True)

# 启动服务
os.execve(
    sys.executable,
    [sys.executable, "-m", "uvicorn", 
     "app.main:app", 
     "--host", "0.0.0.0", 
     "--port", "8000", 
     "--reload"],
    os.environ
)
