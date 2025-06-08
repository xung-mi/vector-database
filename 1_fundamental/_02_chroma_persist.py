import chromadb
from chromadb.utils import embedding_functions

# 1. Sử dụng PersistentClient thay vì ChromaClient
client = chromadb.PersistentClient(path="./db/chroma_persistent")

# 2. Tạo collection với embedding function mặc định
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name="my_story",
    embedding_function=default_ef
)

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

# 3. Thêm dữ liệu vào collection
for doc_key, doc_data in documents.items():\
    collection.upsert(
        documents=[doc_data["text"]],
        ids=[doc_data["id"]]
    )

# 4. Truy vấn thử
results = collection.query(
    query_texts=["How are you?"],
    n_results=1
)

print(results)
