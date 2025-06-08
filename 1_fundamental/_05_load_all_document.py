# ===============================================================
# ✅ XÂY DỰNG VECTOR STORE VỚI LOCAL EMBEDDING + CHROMADB PERSISTENT
# ---------------------------------------------------------------
# 1. Đọc nhiều file .txt từ thư mục
# 2. Tách chunk có overlap
# 3. Dùng mô hình LOCAL embedding (sentence-transformers)
# 4. Lưu vào ChromaDB persistent
# ===============================================================

import os
import uuid
from typing import List
from chromadb.config import Settings
import chromadb
from sentence_transformers import SentenceTransformer

# ===============================================================
# 1. CẤU HÌNH MODEL EMBEDDING LOCAL
# ---------------------------------------------------------------
# Bạn cần đảm bảo đã tải trước model về local (ví dụ: local_models/...)

# Tiếng Anh (nhẹ): all-MiniLM-L6-v2
# model_path = "local_models/all-MiniLM-L6-v2"

# Hoặc dùng tiếng Việt mạnh hơn:
model_path = "local_models/SimCSE-VietNamese-phobert"

print(f"🔄 Đang tải mô hình từ local: {model_path}")
embedding_model = SentenceTransformer(model_path)

# ===============================================================
# 2. LOAD TẤT CẢ FILE .txt TRONG THƯ MỤC
# ---------------------------------------------------------------
def load_documents_from_directory(folder_path: str) -> List[dict]:
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append({
                    "id": filename,
                    "text": text
                })
    print(f"📄 Đã load {len(documents)} documents từ thư mục {folder_path}")
    return documents

# ===============================================================
# 3. CHUNK TEXT VỚI OVERLAP
# ---------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 20) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# ===============================================================
# 4. TẠO EMBEDDINGS VỚI MÔ HÌNH LOCAL
# ---------------------------------------------------------------
def get_embeddings(texts: List[str]) -> List[List[float]]:
    return embedding_model.encode(texts).tolist()

# ===============================================================
# 5. KHỞI TẠO CHROMA VỚI PERSISTENT FOLDER
# ---------------------------------------------------------------
db_dir = "DB"  # Folder lưu trữ dữ liệu
client_chroma = chromadb.Client(Settings(persist_directory=db_dir))
collection = client_chroma.get_or_create_collection(name="document_QA_collection")

# ===============================================================
# 6. QUY TRÌNH XỬ LÝ HOÀN CHỈNH
# ---------------------------------------------------------------
folder_path = "documents"  # Thư mục chứa các file .txt

all_docs = load_documents_from_directory(folder_path)
all_chunks = []
chunk_metadatas = []

print("🔧 Đang chunk văn bản với overlap...")

for doc in all_docs:
    chunks = chunk_text(doc["text"], chunk_size=1000, overlap=20)
    for i, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        chunk_metadatas.append({
            "source_doc": doc["id"],
            "chunk_id": i
        })

print(f"🧩 Đã tạo tổng cộng {len(all_chunks)} chunks từ {len(all_docs)} documents.")

# ===============================================================
# 7. TẠO EMBEDDINGS & LƯU VÀO CHROMADB
# ---------------------------------------------------------------
print("🧠 Đang tạo vector embedding với mô hình local...")
embeddings = get_embeddings(all_chunks)

chunk_ids = [str(uuid.uuid4()) for _ in all_chunks]

print("💾 Đang lưu dữ liệu vào ChromaDB (persistent)...")
collection.add(
    documents=all_chunks,
    ids=chunk_ids,
    embeddings=embeddings,
    metadatas=chunk_metadatas
)

print("✅ Đã lưu vector vào collection 'document_QA_collection' trong folder DB.")

# ===============================================================
# 8. VALIDATION
# ---------------------------------------------------------------
print("\n📊 Validation:")
print(f"Số lượng documents gốc: {len(all_docs)} (expect: 21)")
print(f"Số chunks đã xử lý: {len(all_chunks)}")

print("\n📌 Ví dụ chunk đầu:")
print("Nguồn:", chunk_metadatas[0])
print("Văn bản:", all_chunks[0][:200], "...")
