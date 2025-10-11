# 使用 Flask 官方镜像作为基础镜像
FROM flask:latest

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器的 /app 目录
COPY . .

# 确保 uploads 目录存在
RUN mkdir -p uploads

# 暴露端口 5000（Flask 默认端口）
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 运行应用
CMD ["python", "app.py"]
