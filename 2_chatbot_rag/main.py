import time
from models.query_expander import QueryExpander
from models.llm_loader import load_llm
from models.embedding_loader import load_embeddings
from pipeline.web_scraper import process_website
from pipeline.rag_chain import build_rag_chain
from utils.prompt_template import PROMPT

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

    expander = QueryExpander(model_name="mistral", num_expansions=3)

    print("✅ Hệ thống sẵn sàng. Hỏi gì cũng được (gõ 'exit' để thoát)")
    while True:
        query = input("🗣️ Bạn: ")
        if query.strip().lower() == "exit":
            break

        # Mở rộng truy vấn
        expanded_queries = expander.expand_query(query)
        all_queries = [query] + expanded_queries

        print("📚 Đang tìm kiếm với các phiên bản:")
        for i, q in enumerate(all_queries, 1):
            print(f"  {i}. {q}")

        # Tìm kiếm vector từ các phiên bản mở rộng
        docs_with_scores = []
        for eq in all_queries:
            docs_with_scores.extend(vectorstore.similarity_search_with_score(eq, k=2))

        # Loại trùng và lấy top 3 văn bản
        seen = set()
        dedup_docs = []
        for doc, score in sorted(docs_with_scores, key=lambda x: x[1]):
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                dedup_docs.append(doc)
            if len(dedup_docs) >= 3:
                break

        # Ghép context
        context = "\n\n".join([doc.page_content for doc in dedup_docs])
        full_prompt = PROMPT.format(context=context, question=query)

        # Đo thời gian phản hồi
        start_time = time.time()
        answer = qa_chain.llm(full_prompt)
        end_time = time.time()

        print(f"\n🤖 Bot: {answer}")
        print(f"⏱️ Thời gian phản hồi: {end_time - start_time:.2f} giây\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng chatbot. Tạm biệt!")
