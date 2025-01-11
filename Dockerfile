FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 修改权限
RUN chown -R nobody:nogroup /app/data

# 切换到非 root 用户
USER nobody

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]