# ===============================================================
# ✅ EMBEDDING PIPELINE TOÀN TRÌNH: CHUNKING + LOCAL EMBEDDING + CHROMA
# ===============================================================
# ✔️ Chunking Documents with overlap
# ✔️ Local model for embedding (e.g. SimCSE, MiniLM)
# ✔️ Embedding từng chunk → gán vào doc.embedding
# ✔️ Insert vào ChromaDB (persistent)
# ✔️ Có thể kiểm tra bằng SQLite DB viewer
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
# Đảm bảo đã tải sẵn model về local
model_path = "local_models/all-MiniLM-L6-v2"
model = SentenceTransformer(model_path)

# ===============================================================
# 2. CLASS DOCUMENT ĐỂ GÁN TEXT, ID, CHUNK & EMBEDDING
# ---------------------------------------------------------------
class DocumentChunk:
    def __init__(self, chunk_id: str, content: str, source_doc: str):
        self.id = chunk_id
        self.text = content
        self.source = source_doc
        self.embedding = None  # sẽ được gán sau

# ===============================================================
# 3. CHUNKING FUNCTION
# ---------------------------------------------------------------
def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

# ===============================================================
# 4. TẠO EMBEDDING CHO 1 CHUNK TEXT
# ---------------------------------------------------------------
def get_local_embedding(text: str) -> List[float]:
    return model.encode(text).tolist()

# ===============================================================
# 5. LOAD VÀ CHUNK TOÀN BỘ DOCUMENTS
# ---------------------------------------------------------------
def load_and_chunk_documents(folder_path: str) -> List[DocumentChunk]:
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
                chunks = split_text(raw_text, chunk_size=1000, chunk_overlap=100)
                for i, chunk in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    doc = DocumentChunk(chunk_id, chunk, filename)
                    all_chunks.append(doc)
    print(f"📄 Tổng cộng {len(all_chunks)} chunks đã được tạo từ {folder_path}")
    return all_chunks

# ===============================================================
# 6. INSERT CHUNKS VÀO CHROMA DB
# ---------------------------------------------------------------
def insert_chunks_into_chroma(chunks: List[DocumentChunk], db_dir: str = "DB"):
    chroma_client = chromadb.Client(Settings(persist_directory=db_dir))
    collection = chroma_client.get_or_create_collection(name="document_QA_collection")

    print("🧠 Đang tạo embeddings cho các chunks...")
    for chunk in chunks:
        chunk.embedding = get_local_embedding(chunk.text)

    print("💾 Đang insert vào ChromaDB...")
    collection.upsert(
        documents=[c.text for c in chunks],
        embeddings=[c.embedding for c in chunks],
        metadatas=[{"source": c.source} for c in chunks],
        ids=[c.id for c in chunks]
    )

    print(f"✅ Đã lưu {len(chunks)} chunk vào ChromaDB.")

# ===============================================================
# 7. CHẠY TOÀN BỘ PIPELINE
# ---------------------------------------------------------------
def run_pipeline():
    folder_path = "documents"
    if not os.path.exists(folder_path):
        raise FileNotFoundError("❌ Folder 'documents' không tồn tại!")

    print("🚀 Bắt đầu pipeline: Load → Chunk → Embed → Insert...")
    chunks = load_and_chunk_documents(folder_path)
    insert_chunks_into_chroma(chunks)
    print("🎉 Pipeline hoàn tất!")

# ===============================================================
# CHẠY
# ===============================================================
if __name__ == "__main__":
    run_pipeline()
