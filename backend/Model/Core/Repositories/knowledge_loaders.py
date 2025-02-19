from langchain_openai import ChatOpenAI
from Model.Domain._Utilities.data_store_from_web_scraper import get_vector_store
from Model.Domain._Utilities.manager_tools import ManagerTools
from tenacity import retry, wait_random_exponential, stop_after_attempt
from consts import Subjects, Stages
from consts import Paths as p


class KnowledgeLoaders:
    """
    A class representing the knowledge base for the chat application.

    Attributes:
        extra_context (bool): Indicates whether extra context is enabled.
        vector_store (FAISS): Vector store for extra context if enabled, otherwise None.
        llm_conversation (ChatOpenAI): Language model for conversation.
        llm_validation (ChatOpenAI): Language model for validation.
        llm_retriver (ChatOpenAI): Language model for retrieval.
    """
    
    extra_context = True
    # from .data_store import DataStore     # Old form to obtain Vector Store
    # vector_store = DataStore.get_vector_store() if extra_context else None
    vector_store = get_vector_store() if extra_context else None

    llm_conversation = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")
    llm_validation = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")
    llm_retriver = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

    def __init__(self) -> None:
        self.subject_name: Subjects
        self.stage: Stages
        self.search_kwargs: int
        # Paths
        self.assistant_instructions_path = p.ASSISTANT_INSTRUCTIONS_PATH.format(self.subject_name)
        self.data_required_path = p.DATA_REQUIRED_PATH.format(self.subject_name)
        self.basic_instructions_path = p.BASIC_INSTRUCTIONS_PATH.format(self.subject_name)

        # Knowledge Holders
        self.basic_instructions = self._basic_instructions_loader()
        self.subject_instructions = self._subject_instructions_loader()
        self.data_required = self._data_required_loader()

    @ManagerTools.debugger_exception_decorator
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def update_assistant_knowledge(self, subject_name: Subjects, stage: Stages) -> None:
        """
        Updates dependent attributes based on the mode or subject.
        """
        self.subject_name == subject_name
        self.stage = stage

        if self.subject_name == Subjects.GENERAL_CONTACT:
            self.search_kwargs = 4
        elif self.subject_name == Subjects.HIRE_US:
            self.search_kwargs = 2
        elif self.subject_name == Subjects.JOIN_THE_TEAM:
            self.search_kwargs = 2
        
        self.assistant_instructions_path = p.ASSISTANT_INSTRUCTIONS_PATH.format(self.subject_name)

        if stage == Stages.FREE_CONVERSATION_STAGE:       
            self.assistant_instructions_path = p.ASSISTANT_INSTRUCTIONS_PATH.format(Stages.FREE_CONVERSATION_STAGE)
            self.subject_name = Subjects.GENERAL_CONTACT
            self.search_kwargs = 4

        print("self.assistant_instructions_path", self.assistant_instructions_path)

        self.basic_instructions_path = p.BASIC_INSTRUCTIONS_PATH
        self.data_required_path = p.DATA_REQUIRED_PATH.format(subject_name)
        self.basic_instructions = self._basic_instructions_loader()
        self.subject_instructions = self._subject_instructions_loader()
        self.data_required = self._data_required_loader()

        print("update_assistant_knowledge(): The assistant instructions has been refreshed to the subject: ", self.subject_name)
        
    def _basic_instructions_loader(self) -> str:
        """
        Loads basic instructions.

        Returns:
            str: Basic instructions for the assistant.
        """
        with open(self.basic_instructions_path, 'r', encoding='utf-8') as file:
            basic_instructions = file.read()
        print("Basic instructions: ", self.basic_instructions_path)
        return basic_instructions
    
    def _subject_instructions_loader(self) -> str:
        """
        Loads subject-specific instructions.

        Returns:
            str: Instructions specific to the current subject.
        """
        with open(self.assistant_instructions_path, 'r', encoding='utf-8') as file:
            assistant_instructions = file.read()
        print("assistant_instructions instructions: ", self.assistant_instructions_path)
        return assistant_instructions
    
    def _data_required_loader(self) -> str:
        """
        Loads data required for the current subject.

        Returns:
            str: Data required for the current subject.
        """
        with open(self.data_required_path, 'r', encoding='utf-8') as file:
            data_required = file.read()
        # print("Data required:\n", data_required)
        print("data_required: ", self.data_required_path)
        return data_required

