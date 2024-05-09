from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DocusaurusLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from .manager_tools import ManagerTools
import pickle
import os


"""The follow classes are variations of the remain DataStore Classe. The ative DataStore classe is the 
DataStore last stable DataStore class."""


class DataStore:
    WEB = "web"
    LOCAL = "text"
    SITE_URL = "https://kobu.agency/"

    site_datas_light = 'assistant/knowledge/default/site_datas_light.txt'
    site_datas = 'assistant/knowledge/default/site_datas.txt'

    LOCAL_PATH = site_datas
    docs_pickle_path = "assistant/knowledge/default/docs.pickle"
    origin = LOCAL

    # @ManagerTools.debugger_exception_decorator
    @classmethod
    def get_vector_store(cls, oringin_preference = 'pickel')  -> FAISS:
        """Tries to load a vector_store from a pickle file. If the file doesn't exist, creates a new vector_store."""
        try:
            if oringin_preference == 'pickel':
                vector_store = cls.get_doc_from_pickel()
                print("Vector Store sucessufly loaded")

            elif oringin_preference in [cls.WEB, cls.LOCAL]:
                    vector_store = cls.create_db_critical(oringin_preference)
            else: 
                raise ValueError("Invalid origin")

        except Exception as e:
            print(f"DataStore - get_vector_store() Error: {e}")
            vector_store = cls.create_db_critical(cls.origin)

        finally:
            print("DataStore - Vector Store obtained:\n", vector_store)
            return vector_store

    @classmethod
    @ManagerTools.debugger_exception_decorator
    def get_doc_from_pickel(cls) -> FAISS:
        """Creates and returns a vector_store from a pickle file."""
        print("Checking docs_pickle_path...")

        if os.path.exists(cls.docs_pickle_path):
            with open(cls.docs_pickle_path, 'rb') as f:
                docs = pickle.load(f)
            print("Doc pickel file load from: ", cls.docs_pickle_path)
        
        else: 
            docs = cls.prepare_doc_to_be_pickeled()
            docs = cls.pickel_handler(docs)

        print("Docs After Pickel: ", docs[2])
        embedding = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(docs, embedding=embedding)

        return vector_store
   
    @classmethod
    @ManagerTools.debugger_exception_decorator
    def prepare_doc_to_be_pickeled(cls) -> list:
        if cls.origin == cls.WEB:
            loader = DocusaurusLoader(url=cls.SITE_URL)

        if cls.origin == cls.LOCAL:
            loader = TextLoader(file_path=cls.LOCAL_PATH, encoding='utf-8')

        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=30)
        splitDocs = splitter.split_documents(docs)

        print("prepare_doc_to_be_pickeled() - splitDocs:\n", splitDocs[2])
        print("prepare_doc_to_be_pickeled() - splitDocs SIZE: ", len(splitDocs))
        return splitDocs
        
    @classmethod
    @ManagerTools.debugger_exception_decorator
    def pickel_handler(cls, parameter: list) -> list:
        """Create a pickle file with the parameter if it doesn't exist, otherwise load and return the variable."""

        # Check if the pickle file exists
        if not os.path.exists(cls.docs_pickle_path):
            # If the pickle file doesn't exist, create it with the parameter
            with open(cls.docs_pickle_path, 'wb') as f:
                pickle.dump(parameter, f)
                print(f"O arquivo pickle '{cls.docs_pickle_path}' foi criado com sucesso.")
        else:
            print(f"O arquivo pickle '{cls.docs_pickle_path}' já existe.")

        # Load the pickle file and return the variable
        with open(cls.docs_pickle_path, 'rb') as f:
            loaded_variable = pickle.load(f)
            print(f"Variável carregada do arquivo pickle: '{cls.docs_pickle_path}'")
            # print(f"Variável carregada: '{loaded_variable}'")
            print(f"Variável carregada str: '{loaded_variable[2]}'")
        return loaded_variable

    @classmethod
    @ManagerTools.RETRY()
    def create_db_critical(cls, origin: str = LOCAL) -> FAISS:
        """Creates and returns a vector_store with to be search to extra context."""
        print("DataStore: create_db_critical() Starts")
        # Missing to implement the pickles to save the vector_store
        
        def get_documents_from(origin=origin):
            if origin == cls.WEB:
                loader = DocusaurusLoader(
                    url="https://kobu.agency/",
                    # filter_urls=[
                    #     "https://kobu.agency/case-studies"
                    # ],
                # parsing_function=remove_nav_and_header_elements,
                )

            if origin == cls.LOCAL:
                file_path = cls.LOCAL_PATH # site_datas_light.txt or site_datas.txt (site inteiro)
                loader = TextLoader(file_path=file_path, encoding='utf-8')

            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=550,
                chunk_overlap=30,            # separators = ['<p>', '<br>','</p>', '\n']
            )
            splitDocs = splitter.split_documents(docs)
            print("splitDocs", object)
            print("splitDocs", splitDocs[8])

            return splitDocs
        
        docs = get_documents_from()
        embedding = OpenAIEmbeddings()
        print("openaiembeddings")
        vector_store = FAISS.from_documents(docs, embedding=embedding)
        # new = OpenAI
        return vector_store


class DataStore_propose2:
    WEB = "web"
    LOCAL = "text"
    SITE_URL = "https://kobu.agency/"
    LOCAL_PATH = 'assistant/knowledge/default/site_datas.txt' #_light.txt'
    DOCS_PICKLE_PATH = "assistant/knowledge/default/docs.pickle"

    origin = LOCAL

    # @ManagerTools.debugger_exception_decorator
    @classmethod
    def get_vector_store(cls, origin = origin) -> FAISS:
        """Tries to load a vector_store from a pickle file. If the file doesn't exist, creates a new vector_store."""
        try:
            vector_store = cls.get_doc_from_pickel()
            print("Vector Store successfully loaded: ", vector_store)
        except Exception as e:
            print(f"DataStore - get_vector_store() Error: {e}")
            vector_store = cls.create_db_critical(origin)
        finally:
            return vector_store

    @classmethod
    @ManagerTools.debugger_exception_decorator
    def get_doc_from_pickel(cls) -> FAISS:
        """Creates and returns a vector_store from a pickle file."""
        if os.path.exists(cls.DOCS_PICKLE_PATH):
            with open(cls.DOCS_PICKLE_PATH, 'rb') as f:
                docs = pickle.load(f)
            print("Doc pickle file loaded from: ", cls.DOCS_PICKLE_PATH)
            print("Pickel picked from pickel file:\n", docs[2])
        else:
            docs = cls.prepare_doc_with_splitter()
            cls.pickel_handler(docs)
            print("Pickel picked from prepare doc:\n", docs[2])
        embedding = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(docs, embedding=embedding)
        return vector_store

    @classmethod
    @ManagerTools.debugger_exception_decorator
    def prepare_doc_with_splitter(cls) -> RecursiveCharacterTextSplitter:
        """Returns a RecursiveCharacterTextSplitter object (that is a list) with the datas loaded."""
        if cls.origin == cls.WEB:
            loader = DocusaurusLoader(url=cls.SITE_URL)
        elif cls.origin == cls.LOCAL:
            loader = TextLoader(file_path=cls.LOCAL_PATH, encoding='utf-8')
        else:
            raise ValueError("Invalid origin")
        
        print("Origin: ", cls.origin)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=550, chunk_overlap=30)
        split_docs = splitter.split_documents(docs)
        print("split_docs:\n", split_docs[2])
        print("prepare_doc_with_splitter() - splitDocs SIZE: ", len(split_docs))
        return split_docs

    @classmethod
    @ManagerTools.debugger_exception_decorator
    def pickel_handler(cls, parameter: list) -> None:
        """Create a pickle file with the parameter if it doesn't exist, otherwise load and return the variable."""
        if not os.path.exists(cls.DOCS_PICKLE_PATH):
            with open(cls.DOCS_PICKLE_PATH, 'wb') as f:
                pickle.dump(parameter, f)
                print(f"Pickle file '{cls.DOCS_PICKLE_PATH}' created successfully.")
        else:
            print(f"Pickle file '{cls.DOCS_PICKLE_PATH}' already exists.")

    @classmethod
    @ManagerTools.RETRY()
    def create_db_critical(cls, origin) -> FAISS:
        """Creates and returns a vector_store with to be search to extra context."""
        cls.origin = origin
        print("DataStore: create_db_critical() Starts")
        docs = cls.prepare_doc_with_splitter()
        embedding = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(docs, embedding=embedding)
        return vector_store


class DataStore_propose3:
    vector_store_pickle_path = "assistant/knowledge/default/vector_store.pickle"
    text_file_path = 'assistant/knowledge/default/site_datas_light.txt'
    
    @classmethod
    @ManagerTools.RETRY()
    def create_db(cls, origin: str) -> FAISS:
        """Creates and returns a vector_store with to be search to extra context."""
        print("Trying to create a vector_store...")

        def get_documents_from(origin=origin):
            if origin == 'site':
                print("Site data origin for extra_context choosed.")
                loader = DocusaurusLoader(
                    url="https://kobu.agency/",
                    # filter_urls=[
                    #     "https://kobu.agency/case-studies"
                    # ],
                # parsing_function=remove_nav_and_header_elements,
                )
            if origin == 'text':
                print("Local data origin for extra_context choosed.")
                loader = TextLoader(file_path=cls.text_file_path, encoding='utf-8')
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=550,
                chunk_overlap=30,            # separators = ['<p>', '<br>','</p>', '\n']
            )
            splitDocs = splitter.split_documents(docs)
            return splitDocs
        
        docs = get_documents_from(origin)
        embedding = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(docs, embedding=embedding)
        return vector_store

    @classmethod
    @ManagerTools.RETRY()
    def vector_store_to_pickle(cls, vector_store):
        """Converts the given vector_store to a pickle file."""
        serialized_data = {}
        serialized_data['index'] = vector_store.index

        with open(cls.vector_store_pickle_path, 'wb') as file:
            pickle.dump(serialized_data, file)

    @classmethod
    def get_vector_store(cls, origin: str = 'site')  -> FAISS:
        """Tries to load a vector_store from a pickle file. If the file doesn't exist, creates a new vector_store."""
        try:
            if os.path.exists(cls.vector_store_pickle_path):
                print("Trying to open pickle file...")
                with open(cls.vector_store_pickle_path, 'rb') as file:
                    serialized_data = pickle.load(file)  # Use pickle.load instead of json.load
                # Deserialize basic attributes
                index = serialized_data['index']
                embedding = OpenAIEmbeddings()  # Initialize the Embeddings object
                docstore = None  # Set docstore to None or provide the appropriate docstore
                index_to_docstore_id = None  # Set index_to_docstore_id to None or provide the appropriate index_to_docstore_id
                # Check if the index is an instance of IndexFlatL2
                if isinstance(index, FAISS.IndexFlatL2):
                    # If it is, create a new FAISS object with the provided index
                    vector_store = FAISS(index, embedding, docstore, index_to_docstore_id)
                else:
                    # Otherwise, create a new FAISS object with the default index type
                    vector_store = FAISS.from_documents([], embedding=embedding)
            else:
                vector_store = cls.create_db(origin)
                cls.vector_store_to_pickle(vector_store)

        except Exception as e:
            print(f"DataStore - get_vector_store() Error: {e}")
            vector_store = cls.create_db_critical(origin)

        finally:
            return vector_store

    @classmethod
    @ManagerTools.RETRY()
    def create_db_critical(cls, origin: str = 'text') -> FAISS:
        """Creates and returns a vector_store with to be search to extra context."""
        print("DataStore: create_db_critical() Starts")
        # Missing to implement the pickles to save the vector_store
        def get_documents_from(origin=origin):

            if origin == 'site':
                loader = DocusaurusLoader(
                    url="https://kobu.agency/",
                    # filter_urls=[
                    #     "https://kobu.agency/case-studies"
                    # ],
                # parsing_function=remove_nav_and_header_elements,
                )

            if origin == 'text':
                file_path = 'assistant/knowledge/default/site_datas_light.txt' # site_datas_light.txt or site_datas.txt (site inteiro)
                loader = TextLoader(file_path=file_path, encoding='utf-8')

            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=550,
                chunk_overlap=30,            # separators = ['<p>', '<br>','</p>', '\n']
            )
            splitDocs = splitter.split_documents(docs)
            print("splitDocs", object)
            print("splitDocs", splitDocs[8])

            return splitDocs
        
        docs = get_documents_from(origin)
        embedding = OpenAIEmbeddings()
        print("openaiembeddings")
        vector_store = FAISS.from_documents(docs, embedding=embedding)
        # new = OpenAI
        return vector_store
