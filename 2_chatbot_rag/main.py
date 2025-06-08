import time
from models.llm_loader import load_llm
from models.embedding_loader import load_embeddings
from pipeline.web_scraper import process_website
from pipeline.rag_chain import build_rag_chain

def main():
    print("🌐 Nhập URL website cần xử lý:")
    url = input("→ URL: ")
    print("🔄 Đang phân tích website...")
    docs = process_website(url)
    
    print("📥 Đang tải LLM và Embedding...")
    llm = load_llm()
    embeddings = load_embeddings()

    print("🧠 Xây dựng RAG pipeline...")
    qa_chain, vectorstore = build_rag_chain(llm, docs, embeddings)

    print("✅ Hệ thống sẵn sàng. Hỏi gì cũng được (gõ 'exit' để thoát)")
    while True:
        query = input("🗣️ Bạn: ")
        if query.strip().lower() == "exit":
            break
        
        
        start_time = time.time()
        result = qa_chain.invoke({"query": query})
        answer = result['result']
        end_time = time.time()

        elapsed = end_time - start_time
        print(f"🤖 Bot: {answer}")
        print(f"⏱️ Thời gian phản hồi: {elapsed:.2f} giây\n")
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng chatbot. Tạm biệt!")