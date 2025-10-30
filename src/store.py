from langchain_postgres import PGVector
from settings import settings

class Store:
    store: PGVector
    
    def __init__(self, embeddings):
        self.store = PGVector(
            embeddings=embeddings,
            collection_name=settings.pg_vector_collection_name,
            connection=settings.database_url,
            use_jsonb=True,
        )
    
    def add_documents(self, documents, ids):
        self.store.add_documents(documents=documents, ids=ids)
        
    def search(self, query: str)-> list:
        return self.store.similarity_search_by_vector(query, k=10)

