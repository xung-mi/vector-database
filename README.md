# Vector Database

**Vector Database** là hệ quản trị cơ sở dữ liệu được thiết kế để lưu trữ và truy vấn các vector embedding — biểu diễn số của dữ liệu như văn bản, hình ảnh, âm thanh sau khi được xử lý bằng mô hình học máy.

Dự án này minh họa cách sử dụng vector database (ví dụ: FAISS, Pinecone) để:

- Lưu trữ các vector kèm metadata
- Thực hiện tìm kiếm ngữ nghĩa (semantic search)
- Kết hợp lọc theo thuộc tính (metadata filtering)
- Triển khai nhanh bằng Python và biến môi trường `.env` để bảo mật cấu hình

**Use case phổ biến**: tìm kiếm văn bản tương đồng, gợi ý sản phẩm, chatbot theo ngữ cảnh, phân tích dữ liệu phi cấu trúc.

---

## Hướng dẫn sử dụng LLM local với Ollama

Thay vì dùng API OpenAI, bạn có thể chạy mô hình ngôn ngữ lớn (LLM) cục bộ với [Ollama](https://ollama.com).

### 1. Cài đặt Ollama (trên Windows)

1. Truy cập: https://ollama.com/download
2. Tải về bản Windows và cài đặt
3. Sau khi cài xong, mở terminal và kiểm tra:

```bash
ollama run mistral
```

### 2. Thiết lập `.env`

Tạo file `.env` tại thư mục gốc của dự án với nội dung:

```dotenv
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### 3. Build Docker image

```bash
bash docker_build.sh
```

### 4. Chạy Docker container

```bash
bash docker_run.sh
```