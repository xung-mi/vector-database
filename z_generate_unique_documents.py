import os
import random

# Tạo thư mục chứa các file nếu chưa có
folder_path = "documents"
os.makedirs(folder_path, exist_ok=True)

# Tập hợp các câu ngẫu nhiên (đủ đa dạng)
sentences = [
    "Trí tuệ nhân tạo đang cách mạng hóa nhiều ngành công nghiệp.",
    "Học máy giúp máy tính học từ dữ liệu mà không cần lập trình rõ ràng.",
    "Việc áp dụng AI trong y tế giúp chẩn đoán chính xác hơn.",
    "Xe tự lái sử dụng cảm biến và thuật toán để di chuyển an toàn.",
    "Ngôn ngữ tự nhiên là cầu nối giữa con người và máy móc.",
    "Các mô hình ngôn ngữ lớn có thể viết văn bản giống con người.",
    "Bảo mật dữ liệu là thách thức lớn khi dùng AI.",
    "Chatbot đang thay thế một phần chăm sóc khách hàng truyền thống.",
    "AI có thể giúp cá nhân hóa giáo dục cho từng học sinh.",
    "Tuy mạnh mẽ, AI cũng tiềm ẩn rủi ro nếu không được kiểm soát.",
    "Phát hiện gian lận tài chính là ứng dụng phổ biến của học sâu.",
    "AI đang được tích hợp vào thiết bị IoT để làm nhà thông minh.",
    "Phân tích cảm xúc giúp doanh nghiệp hiểu khách hàng tốt hơn.",
    "Mô hình nhận diện hình ảnh đã vượt qua năng lực con người ở một số tác vụ.",
    "Kỹ thuật học tăng cường đang mở ra kỷ nguyên robot tự hành.",
    "AI không thể thay thế con người, nhưng có thể hỗ trợ rất tốt.",
    "Việc quản lý AI cần sự tham gia của cả luật pháp và xã hội.",
    "Người dùng cần hiểu giới hạn của mô hình AI để dùng đúng cách.",
    "AI tạo ảnh đang làm mờ ranh giới giữa thực và ảo.",
    "Mỗi bước tiến trong AI đều đi kèm câu hỏi đạo đức.",
    "Giải thích quyết định của AI là yêu cầu quan trọng trong nhiều lĩnh vực."
]

# Tạo 21 file với nội dung ngẫu nhiên
for i in range(21):
    file_name = f"article_{i+1:02}.txt"
    file_path = os.path.join(folder_path, file_name)
    
    # Chọn ngẫu nhiên 2–3 câu không trùng nhau
    selected = random.sample(sentences, k=random.randint(2, 3))
    content = f"Bài viết số {i+1}\n" + "\n".join(selected)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Đã tạo 21 file .txt khác nhau trong thư mục '{folder_path}'")
