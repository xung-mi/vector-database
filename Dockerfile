FROM python:3.11-slim

# Tạo thư mục làm việc
WORKDIR /app

# Cài các package hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    lsof \
    git \
    git-lfs \
    wget \
    curl \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Sao chép mã nguồn vào container
COPY . /app

# Nâng cấp pip và cài Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Mở port cho Gradio / FastAPI / Flask hoặc Chroma
EXPOSE 8000

# Chạy app Python
CMD ["python", "main.py"]
