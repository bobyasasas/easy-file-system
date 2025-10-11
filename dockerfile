# 使用 Flask 官方镜像作为基础镜像
FROM tiangolo/uwsgi-nginx-flask:python3.12

# 复制当前目录内容到容器的 /app 目录
COPY . /app

# 确保 uploads 目录存在
RUN mkdir -p uploads
