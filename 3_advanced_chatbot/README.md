Cách hoạt động:
- Người dùng đặt câu hỏi bằng ngôn ngữ tự nhiên.
- LLM tạo truy vấn SQL tương ứng.
- Truy vấn được gửi đến database thực tế
- Kết quả trả về được LLM xử lý và chuyển thành câu trả lời thân thiện với người dùng

Kỹ thuật sử dụng
- Toolkit từ LangChain giúp gắn kết LLM với database
- SQL Agent được tạo từ create_sql_agent trong LangChain, kết hợp:
    - Mô hình ngôn ngữ (GPT-4 mini)
    - Toolkits cho SQL
    - System message hướng dẫn cách trả lời
    - Cấu hình truy vết (verbose)