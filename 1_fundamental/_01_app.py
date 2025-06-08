import chromadb

# Tạo Chroma client
chroma_client = chromadb.Client()

# Tạo collection (sử dụng get_or_create để tránh lỗi nếu đã tồn tại)
collection_name = "test_collection"
collection = chroma_client.get_or_create_collection(name=collection_name)

# Define sample documents
documents = {
    "doc1": {
        "id": "doc1",
        "text": "Hello world"
    },
    "doc2": {
        "id": "doc2", 
        "text": "How are you today?"
    },
    "doc3": {
        "id": "doc3",
        "text": "Machine learning"
    }
}

# Dùng collection.upsert() thay vì collection.add() để tránh duplicate documents 
    # khi chạy code nhiều lần. Upsert sẽ update nếu document đã tồn tại.
print("Adding documents to collection...")
for doc_key, doc_data in documents.items():\
    collection.upsert(
        documents=[doc_data["text"]],
        ids=[doc_data["id"]]
    )

print(f"Successfully added {len(documents)} documents to collection!")

# Define query text
query_text = "Hello world"

# Thực hiện query search
# Sử dụng collection.query() với parameters query_texts (câu hỏi cần tìm) \
    # và n_results (số kết quả mong muốn) để tìm kiếm documents tương tự.
print(f"\nSearching for: '{query_text}'")
results = collection.query(
    query_texts=[query_text],
    n_results=3
)

# In kết quả
print("\n" + "="*50)
print("SEARCH RESULTS:")
print("="*50)

for i, (doc_id, distance, document) in enumerate(zip(
    results['ids'][0], 
    results['distances'][0], 
    results['documents'][0]
)):
    print(f"\nResult {i+1}:")
    print(f"Document ID: {doc_id}")
    print(f"Distance Score: {distance:.4f}")
    print(f"Content: {document}")
    print("-" * 30)

# Thêm thêm một query khác để test
print("\n" + "="*50)
query_text2 = "machine learning"
print(f"Searching for: '{query_text2}'")

results2 = collection.query(
    query_texts=[query_text2],
    n_results=2
)

print("\nSECOND SEARCH RESULTS:")
print("="*50)

for i, (doc_id, distance, document) in enumerate(zip(
    results2['ids'][0], 
    results2['distances'][0], 
    results2['documents'][0]
)):
    print(f"\nResult {i+1}:")
    print(f"Document ID: {doc_id}")
    print(f"Distance Score: {distance:.4f}")
    print(f"Content: {document}")
    print("-" * 30)

# Hiển thị thông tin collection
print(f"\nCollection info:")
print(f"Collection name: {collection.name}")
print(f"Total documents: {collection.count()}")