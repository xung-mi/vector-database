from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

# cho phép lưu trữ chuỗi các tin nhắn giữa người dùng và chatbot để tăng tính liên kết trong các phản hồi.
from langchain.memory import ConversationBufferMemory
from utils.prompt_template import PROMPT

def build_rag_chain(llm, texts, embedding_model):
    vectorstore = FAISS.from_documents(texts, embedding_model)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    retriever = vectorstore.as_retriever()
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        memory=memory,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain, vectorstore