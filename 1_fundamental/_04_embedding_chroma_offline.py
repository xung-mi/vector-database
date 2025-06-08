# ===============================================================
# ✅ TẠO VÀ TRUY VẤN EMBEDDING HOÀN TOÀN OFFLINE VỚI CHROMA & SENTENCE-TRANSFORMERS
# ---------------------------------------------------------------
# - Không cần kết nối internet
# - Hỗ trợ cả tiếng Việt và tiếng Anh
# - Sử dụng ChromaDB để lưu trữ và truy vấn vector
# ===============================================================

import chromadb
import uuid
from sentence_transformers import SentenceTransformer

# ===============================================================
# 🔧 CẤU HÌNH: Chọn mô hình tiếng Việt hoặc tiếng Anh
# ---------------------------------------------------------------
# Bạn cần tải trước model từ HuggingFace rồi lưu ở local
# Nếu chưa có, dùng model.save("local_models/...") để lưu trước

# Tiếng Anh: all-MiniLM-L6-v2
# model_path = "local_models/all-MiniLM-L6-v2"

# Tiếng Việt: VoVanPhuc/sup-SimCSE-VietNamese-phobert-base
model_path = "local_models/SimCSE-VietNamese-phobert"

# Tải model từ ổ đĩa local
print("🔄 Đang tải mô hình từ local:", model_path)
model = SentenceTransformer(model_path)

# ===============================================================
# 🗃️ KHỞI TẠO CHROMA DB (in-memory hoặc persistent)
# ---------------------------------------------------------------
# Nếu bạn muốn lưu DB vào ổ đĩa → dùng: persist_directory="chroma_store"

client = chromadb.PersistentClient(path="./db/chroma_persistent")
collection = client.get_or_create_collection(name="my_documents")

# ===============================================================
# 📥 NHÚNG DỮ LIỆU VÀ THÊM VÀO VECTOR DATABASE
# ---------------------------------------------------------------

texts = [
    "Tôi yêu học máy", 
    "Vector database rất hữu ích", 
    "Chào bạn, bạn khỏe không?",
    "Trí tuệ nhân tạo đang thay đổi thế giới"
]

# Sinh ID ngẫu nhiên cho mỗi văn bản
ids = [str(uuid.uuid4()) for _ in texts]

# Tạo vector embedding từ văn bản
print("🧠 Đang tạo vector embedding...")
embeddings = model.encode(texts).tolist()

# Thêm văn bản và vector vào ChromaDB
collection.add(documents=texts, embeddings=embeddings, ids=ids)
print("✅ Đã thêm dữ liệu vào ChromaDB.")

# ===============================================================
# 🔍 TRUY VẤN VĂN BẢN GẦN NHẤT VỚI CÂU HỎI
# ---------------------------------------------------------------
query_text = "Học về vector rất thú vị"
query_vector = model.encode([query_text]).tolist()

# Truy vấn top 2 văn bản tương tự
results = collection.query(query_embeddings=query_vector, n_results=2)

print("\n🔎 Kết quả gần giống nhất với truy vấn:")
for doc, dist in zip(results['documents'][0], results['distances'][0]):
    print(f"• {doc} (≈ khoảng cách: {dist:.4f})")

# ===============================================================
# ✅ KẾT THÚC
# ---------------------------------------------------------------
# Bạn có thể mở rộng thêm:
# - Tạo giao diện search
# - Lưu DB vào ổ đĩa
# - Trích xuất vector từ file PDF, TXT, ...
# ===============================================================
