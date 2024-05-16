from langchain_openai import ChatOpenAI
from .data_store import DataStore
from ..tools.manager_tools import *
from ..consts import ChatConsts


class KnowledgeLoaders(ChatConsts):
    """
    A class representing the knowledge base for the chat application.

    Attributes:
        extra_context (bool): Indicates whether extra context is enabled.
        vector_store (FAISS): Vector store for extra context if enabled, otherwise None.
        llm_conversation (ChatOpenAI): Language model for conversation.
        llm_validation (ChatOpenAI): Language model for validation.
        llm_retriver (ChatOpenAI): Language model for retrieval.
        stage (str): Current stage of the conversation.
        subject_name (str): Name of the current subject.
        subject_instance (object): Instance of the current subject class.
        search_kwargs (int): Number of search arguments.
        assistant_instructions_path (str): Path to assistant instructions.
        data_required_path (str): Path to data required file.
        basic_instructions_path (str): Path to basic instructions file.
        basic_instructions (str): Basic instructions for the assistant.
        subject_instructions (str): Instructions specific to the current subject.
        data_required (str): Data required for the current subject.
    """
    
    extra_context = True
    vector_store = DataStore.get_vector_store() if extra_context else None

    llm_conversation = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")
    llm_validation = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")
    llm_retriver = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

    def __init__(self, stage: str = None) -> None:
        """
        Initializes a Knowledge instance.

        Args:
            stage (str): Current stage of the conversation.
        """
        # Essential chat parameters (default configuration)
        self.stage = stage if stage is not None else self.WELCOME_STAGE
        self.subject_name = self.GENERAL_CONTACT
        self.subject_instance = self.CLASS_GENERAL_CONTACT
        self.search_kwargs = 3
        
        # Paths
        self.assistant_instructions_path = f'assistant/knowledge/data_store_files/{self.subject_name}/{self.subject_name}_instructions.json'
        self.data_required_path = f'assistant/knowledge/data_store_files/{self.subject_name}/{self.subject_name}_data_required.txt'
        self.basic_instructions_path =  'assistant/knowledge/data_store_files/default/basic_instructions.json'

        # Knowledge Holders
        self.basic_instructions = self._basic_instructions_loader()
        self.subject_instructions = self._subject_instructions_loader()
        self.data_required = self._data_required_loader()

    @ManagerTools.debugger_exception_decorator
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def update_dependent_attributes(self, mode = False) -> None:
        """
        Updates dependent attributes based on the mode or subject.

        Args:
            mode (str): Mode to update attributes to.
        """
        if mode != False:
            if mode == self.CRITICAL:
                print("[MODE IN TEST] ", mode)
                self.subject_name = self.GENERAL_CONTACT
                self.subject_instance = self.CLASS_GENERAL_CONTACT
                self.extra_context = False
                self.subject = 0
            print("The parameters has been refreshed to mode: ", mode)

        else:
            print("No updade mode provided")
            if self.subject == 0:
                self.subject_name = self.GENERAL_CONTACT
                self.subject_instance = self.CLASS_GENERAL_CONTACT
                self.search_kwargs = 4
                
            elif self.subject == 1:
                self.subject_name = self.HIRE_US
                self.subject_instance = self.CLASS_HIRE_US
                self.search_kwargs = 2

            elif self.subject == 2:
                self.subject_name = self.JOIN_THE_TEAM
                self.subject_instance = self.CLASS_JOIN_THE_TEAM
                self.search_kwargs = 2
            
            self.extra_context = True
        
        self.assistant_instructions_path = f'assistant/knowledge/data_store_files/{self.subject_name}/{self.subject_name}_instructions.json'

        if self.stage == self.FREE_CONVERSATION_STAGE:       
            self.assistant_instructions_path = f'assistant/knowledge/data_store_files/default/{self.FREE_CONVERSATION_STAGE}_instructions.txt'
            self.subject = 0
            self.subject_name = self.GENERAL_CONTACT
            self.subject_instance = self.CLASS_GENERAL_CONTACT
            self.search_kwargs = 4

            print("self.assistant_instructions_path", self.assistant_instructions_path)

        self.basic_instructions_path =  'assistant/knowledge/data_store_files/default/basic_instructions.json'
        self.data_required_path = f'assistant/knowledge/data_store_files/{self.subject_name}/{self.subject_name}_data_required.txt'

        self.basic_instructions = self._basic_instructions_loader()
        self.subject_instructions = self._subject_instructions_loader()
        self.data_required = self._data_required_loader()

        print("update_dependent_attributes(): The assistant instructions has been refreshed to the subject: ", self.subject_name)

        
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

