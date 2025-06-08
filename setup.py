from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2 (tiếng Anh, nhẹ, phổ biến)
model_en = SentenceTransformer('all-MiniLM-L6-v2')
model_en.save('local_models/all-MiniLM-L6-v2')

# VoVanPhuc/sup-SimCSE-VietNamese-phobert-base (tiếng Việt)
model_vi = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
model_vi.save('local_models/SimCSE-VietNamese-phobert')