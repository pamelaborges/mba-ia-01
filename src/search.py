from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from prompts import PROMPT_TEMPLATE
from settings import settings
from store import Store
class BaseSearchChain():

    def __init__(self):
        self.embeddings = self._create_embeddings()
        self.llm = self._create_llm()
        self.prompt = self._build_prompt()
        self.store = Store(self.embeddings)
        self.chain = self._build_chain()

    def _build_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            input_variables=["context", "question"],
            template=PROMPT_TEMPLATE,
        )

    def _build_chain(self):
        @chain
        def search_database(question: str) -> dict:
            question_vector = self.embeddings.embed_query(question)
            database_results = self.store.search(question_vector)
            content = "\n\n".join(
                doc.page_content.strip() for doc in database_results if doc.page_content
            )
            return {"context": content, "question": question}

        return search_database | self.prompt | self.llm | StrOutputParser()

    def invoke(self, question: str) -> str:
        return self.chain.invoke(question)


class OpenAISearchChain(BaseSearchChain):

    def _create_embeddings(self):
        return OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            api_key=settings.openai_api_key,
        )

    def _create_llm(self):
        return ChatOpenAI(
            model=settings.openai_model,
            temperature="0.5",
            api_key=settings.openai_api_key,
        )


class GeminiSearchChain(BaseSearchChain):

    def _create_embeddings(self):
        return GoogleGenerativeAIEmbeddings(
            model=settings.google_embedding_model,
            google_api_key=settings.google_api_key,
        )

    def _create_llm(self):
        return ChatGoogleGenerativeAI(
            model=settings.google_model,
            temperature="0.5",
            google_api_key=settings.google_api_key,
        )


class SearchFactory:
    @classmethod
    def get_instance(cls, provider: str) -> BaseSearchChain:
        
      search_provider = OpenAISearchChain
      if provider == '2':
          search_provider = GeminiSearchChain
    
      return search_provider()



def get_search(provider: str) -> BaseSearchChain:
    return SearchFactory.get_instance(provider)


def search_prompt(question: str, provider: str) -> str:
    return get_search(provider).invoke(question)
