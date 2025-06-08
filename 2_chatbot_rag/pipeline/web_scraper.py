import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import BSHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
import tempfile, os
from config import CHUNK_SIZE, CHUNK_OVERLAP

def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def process_website(url):
    html_content = fetch_html(url)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp:
        temp.write(html_content)
        path = temp.name

    loader = BSHTMLLoader(path)
    documents = loader.load()
    os.remove(path)

    splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)

    print(f"\n🔍 Số đoạn văn bản sau khi chia: {len(chunks)}")
    print("📝 Nội dung mẫu đã load (tối đa 5 đoạn đầu):\n")
    for i, doc in enumerate(chunks[:5]):
        print(f"[{i+1}] {doc.page_content[:500]}...\n")  # Giới hạn 500 ký tự

    return chunks
