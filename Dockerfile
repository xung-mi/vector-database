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

COPY requirements.txt .

# Nâng cấp pip và cài Python packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && rm -rf ~/.cache/pip

# Sao chép mã nguồn vào container
COPY . .

EXPOSE 8000

# Chạy app Python
CMD ["python", "main.py"]
