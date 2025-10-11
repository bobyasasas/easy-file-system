# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt（如果有的话）
COPY requirements.txt .

# 安装依赖（如果使用 requirements.txt）
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录内容到容器的 /app 目录
COPY . .

# 安装 Flask（因为项目依赖 Flask）
#RUN pip install --no-cache-dir flask

# 确保 uploads 目录存在
RUN mkdir -p uploads

# 暴露端口 5000（Flask 默认端口）
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 运行应用
CMD ["python", "app.py"]
