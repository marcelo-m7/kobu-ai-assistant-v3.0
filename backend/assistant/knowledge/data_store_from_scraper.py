import os
import json
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_community.vectorstores.faiss import VectorStore, Document, Embeddings, FAISS
from dotenv import load_dotenv
os.environ["OPENAI_API_KEY"] = "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"
load_dotenv()



class VectorStoreBuilder:
    def __init__(self, json_folder: str, embedding: Embeddings):
        self.json_folder = json_folder
        self.embedding = embedding

    def load_documents(self) -> List[Document]:
        try:
            documents = []
            for filename in os.listdir(self.json_folder):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.json_folder, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        title = data.get('title', '')
                        content = data.get('content', '')
                        metadata = data.get('metadata', {})
                        documents.append(Document(title=title, page_content=content, metadata=metadata))
            
            print("Docs loadeds:\n", documents[0], documents[8], documents[15])
            return documents
        except Exception as e:
            print(f"Erro ao carregar documentos: {e}")
            return []

    def build_vector_store(self) -> VectorStore:
        try:
            documents = self.load_documents()
            vector_store = FAISS.from_documents(documents, embedding=self.embedding)
            return vector_store
        except Exception as e:
            print(f"Erro ao construir o vetor de armazenamento: {e}")
            return None


class GetVectorStore:
    @staticmethod
    def main():
        try:
            # Definindo a pasta contendo os arquivos JSON
            # json_folder = 'assistant/tools/web_scraper_files__test'
            json_folder = 'assistant/tools/web_scraper_files__test'

            # Inicializando a classe de embeddings
            embedding = OpenAIEmbeddings()

            # Construindo o vetor de armazenamento
            builder = VectorStoreBuilder(json_folder, embedding)
            vector_store = builder.build_vector_store()

            # Verificando se o vetor de armazenamento foi construído corretamente
            if vector_store is not None:
                print("Vector store construído com sucesso!")
            else:
                print("Erro ao construir o vector store.")
        except Exception as e:
            print(f"Erro durante a execução do programa: {e}")
        finally:
            print("Programa concluído.")
            return vector_store


if __name__ == "__main__":
    GetVectorStore.main()