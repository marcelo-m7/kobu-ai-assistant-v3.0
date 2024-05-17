import os
import json
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_community.vectorstores.faiss import VectorStore, Document, Embeddings, FAISS
from dotenv import load_dotenv

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "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"
load_dotenv()


class VectorStoreBuilder:
    """
    A class to build a vector store from a folder containing JSON documents.
    """

    def __init__(self, json_folder: str, embedding: Embeddings):
        """
        Initialize the VectorStoreBuilder.

        Parameters:
        - json_folder (str): The path to the folder containing JSON documents.
        - embedding (Embeddings): The embedding model to use for vectorization.
        """
        self.json_folder = json_folder
        self.embedding = embedding

    def load_documents(self) -> List[Document]:
        """
        Load documents from JSON files in the specified folder.

        Returns:
        - List[Document]: A list of Document objects representing the loaded documents.
        """
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
            
            # Print examples of loaded documents for verification
            print("Loaded documents[0]:\n", documents[0], documents[8], documents[15])
            print("\nLoaded documents[15]:\n", documents[15])
            return documents
        
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []

    def build_vector_store(self) -> VectorStore:
        """
        Build a vector store from loaded documents using FAISS.

        Returns:
        - VectorStore: The built vector store.
        """
        try:
            documents = self.load_documents()
            vector_store = FAISS.from_documents(documents, embedding=self.embedding)
            return vector_store
        except Exception as e:
            print(f"Error building vector store: {e}")
            return None


def get_vector_store():
    """
    Main function to get the vector store.
    """
    try:
        # Define the folder containing JSON files
        json_folder = 'assistant/knowledge/data_store_files/web_scraper_files'

        # Initialize the embedding model
        embedding = OpenAIEmbeddings()

        # Build the vector store
        builder = VectorStoreBuilder(json_folder, embedding)
        vector_store = builder.build_vector_store()

        # Check if the vector store was built successfully
        if vector_store is not None:
            print("Vector store built successfully!")
        else:
            print("Error building the vector store.")
    except Exception as e:
        print(f"Error during program execution: {e}")
    finally:
        print("Program completed.")
        return vector_store


if __name__ == "__main__":
    get_vector_store()
