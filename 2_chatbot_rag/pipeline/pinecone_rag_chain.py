import os
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from utils.prompt_template import PROMPT

def build_rag_chain(llm, texts, embedding_model):
    # Khởi tạo Pinecone client
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    index_name = os.environ["PINECONE_INDEX_NAME"]
    environment = os.environ["PINECONE_ENVIRONMENT"]

    # Tạo index nếu chưa tồn tại
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=embedding_model.embed_query("test").__len__(),
            metric="cosine",
            spec=ServerlessSpec(cloud="gcp", region=environment)
        )

    # Gửi documents lên Pinecone
    vectorstore = PineconeVectorStore.from_documents(
        documents=texts,
        embedding=embedding_model,
        index_name=index_name
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa_chain, vectorstore
