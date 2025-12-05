FROM python:3.12-slim

# 环境变量：不生成 .pyc、立即输出日志
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    TZ=Asia/Shanghai

# 如果你在国内，可以换成国内源（可选）
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存
COPY requirements.txt .

# 安装依赖
# rapidfuzz/pandas/numpy 都有 wheel，一般不需要额外系统库
RUN pip install --no-cache-dir -r requirements.txt

# 再复制项目代码
COPY . .

# 对外暴露 Streamlit 端口
EXPOSE 8501

# 以非 root 用户运行（安全一些，可选）
RUN useradd -m appuser \
    && chown -R appuser /app
USER appuser

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]