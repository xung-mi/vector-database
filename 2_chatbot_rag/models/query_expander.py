from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class QueryExpander:
    def __init__(self, model_name="mistral", num_expansions=3):
        self.template = PromptTemplate(
            input_variables=["question", "n"],
            template=(
                "Hãy viết {n} phiên bản khác nhau của câu hỏi sau, với cùng ý nghĩa nhưng cách diễn đạt khác:\n\n"
                "Câu hỏi: {question}\n\n"
                "Các phiên bản:\n"
            )
        )

        self.llm = ChatOllama(model=model_name)
        self.chain = LLMChain(llm=self.llm, prompt=self.template)
        self.num_expansions = num_expansions

    def expand_query(self, question: str):
        prompt_input = {
            "question": question,
            "n": self.num_expansions
        }
        output = self.chain.run(prompt_input)
        expansions = [line.strip("-• ").strip() for line in output.split("\n") if line.strip()]
        return expansions
