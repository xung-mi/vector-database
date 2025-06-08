from sentence_transformers import SentenceTransformer

# Tải model nhẹ phổ biến (tiếng Anh)
# model = SentenceTransformer('local_models/all-MiniLM-L6-v2')
model = SentenceTransformer('local_models/SimCSE-VietNamese-phobert')


# Hoặc nếu bạn muốn dùng model hỗ trợ tiếng Việt tốt hơn:
# model = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')

# Câu bạn muốn nhúng thành vector
sentence = "Tôi đang học về vector database"

# Tạo embedding
embedding = model.encode(sentence)

print("Kích thước vector:", len(embedding))
print("Vector đầu tiên:", embedding[:5])  # In thử vài giá trị đầu
