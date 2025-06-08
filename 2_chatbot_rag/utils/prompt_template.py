from langchain.prompts import PromptTemplate

template = """Context: {context}

Question: {question}

Answer the question concisely based only on the given context. If the context doesn't contain relevant information, say "Tôi không có đủ thông tin để trả lời câu hỏi này."

Nếu câu hỏi là kiến thức chung, hãy trả lời như bình thường."""

PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
