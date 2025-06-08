from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_PATH

def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_PATH,
        encode_kwargs={'normalize_embeddings': True}
    )
