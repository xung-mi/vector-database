from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
api_key = os.getenv("PINECONE_KEY")  # Sửa tên biến từ PINECORN_KEY

# Khởi tạo Pinecone client
pc = Pinecone(api_key)

# Tên index
index_name = "developer-quickstart-py"

# Tạo index nếu chưa tồn tại (tùy chọn)
# if not pc.list_indexes().get(index_name):
#     pc.create_index(
#         name=index_name,
#         dimension=16,  # số chiều của vector
#         metric="dotproduct",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )

# Truy cập index
index = pc.Index(index_name)

# Upsert sparse vectors vào namespace
index.upsert(
    namespace="example-namespace",
    vectors=[ ... ]  # Giữ nguyên danh sách vectors như bạn đã có
)

# ✅ Truy vấn vector (vì bạn dùng sparse_values nên phải dùng sparse_vector)
query_sparse_vector = {
    "indices": [8661920, 350356213, 391213188, 554637446, 1024951234, 1640781426, 1780689102, 1799010313,
                2194093370, 2632344667, 2641553256, 2779594451, 3517203014, 3543799498, 3837503950, 4283091697],
    "values": [2.6875, 4.2929688, 3.609375, 3.0722656, 2.1152344, 5.78125, 3.7460938, 3.7363281,
               1.2695312, 3.4824219, 0.7207031, 0.0826416, 4.671875, 3.7011719, 2.796875, 0.61621094]
}

# Gọi truy vấn
results = index.query(
    namespace="example-namespace",
    sparse_vector=query_sparse_vector,
    top_k=2,
    include_metadata=True
)

# Hiển thị kết quả
for match in results["matches"]:
    print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")
