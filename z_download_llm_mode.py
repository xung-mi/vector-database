from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "NlpHUST/gpt2-vietnamese"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.save_pretrained("./models/gpt2_vi")
model.save_pretrained("./models/gpt2_vi")

print("✅ Đã tải và lưu mô hình vào ./models/gpt2_vi")
