import os
from langchain_ollama import OllamaLLM

def load_llm():
    """
    Load LLM từ Ollama server đang chạy ngoài container (host).
    Có thể tùy chỉnh model và base_url qua biến môi trường:
      - OLLAMA_MODEL (mặc định: mistral)
      - OLLAMA_BASE_URL (mặc định: http://host.docker.internal:11434)
    """
    model_name = os.getenv("OLLAMA_MODEL", "mistral")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

    try:
        llm = OllamaLLM(
            model=model_name,
            base_url=base_url,
            temperature=0.7
        )
        # Test thử gọi 1 câu ngắn
        _ = llm.invoke("Xin chào!")
        return llm
    except Exception as e:
        raise RuntimeError(f"❌ Không thể kết nối đến Ollama tại {base_url}. Chi tiết: {e}")
