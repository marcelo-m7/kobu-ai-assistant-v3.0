from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from .data_store import DataStore
from .manager_tools import *
from .consts import ChatConsts


class Knowledge(ChatConsts):
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
        self.assistant_instructions_path = f'assistant/knowledge/{self.subject_name}/{self.subject_name}_instructions.json'
        self.data_required_path = f'assistant/knowledge/{self.subject_name}/{self.subject_name}_data_required.txt'
        self.basic_instructions_path =  'assistant/knowledge/default/basic_instructions.json'

        # Knowledge Holders
        self.basic_instructions = self._basic_instructions_loader()
        self.subject_instructions = self._subject_instructions_loader()
        self.data_required = self._data_required_loader()

    def assistant_site_context(self) -> tuple:
        """
        Retrieves assistant site context.

        Returns:
            tuple: Tuple containing system message and site context message.
        """
        if self.extra_context:
            assistant_site_context = (
                "system", "Regardless of the case, always prioritize the instructions above. These are additional data extracted from the KOBU Website. If not requested by the user, please ignore it: {context}")
        else:
            assistant_site_context = (
                "system", "For this propose, you don not have access to the datas in the KOBU Agency website.")
            
        return assistant_site_context

    @staticmethod
    def assistant_tone_of_voice(tone = None) -> tuple:
        """
        Retrieves assistant tone of voice.

        Returns:
            tuple: Tuple containing system message and tone of voice example.
        """

        tone_for_lead = (
        "system", 
        """Tone of voice example:
        \n
        Alright, my dear user, let's dive into the enchanting world of virtual assistance, shall we? ✨ Oh, splendid! Just a spot of info before we embark on this grand adventure: I'm here to assist you in the most delightful manner imaginable, with a sprinkle of wit and a dash of British charm. 🌟
        \n
        Now, let's set the stage, shall we? Picture yourself sipping tea ☕️ in a quaint English garden, surrounded by the gentle hum of bees and the melodious chirping of birds. Ah, bliss! 🌸
        \n
        First things first, my dear friend! What marvelous project has brought you to our doorstep today? Is it a venture into the digital realm? An escapade in branding perhaps? Do tell! 🚀💼
        \n
        And pray, do share with me how you stumbled upon our humble abode? Was it a chance encounter, a serendipitous twist of fate, or did you embark on a quest specifically in search of the renowned KOBU Agency? 🕵️‍♂️🔍
        \n
        Just a gentle reminder, my friend, I won't burden you with more than one request for information in a single message. This way, our conversation flows smoothly like a meandering stream through the countryside. 🌿💬
        \n
        Now, allow me to regale you with a tale of our illustrious agency! Picture a team of intrepid souls, working tirelessly from Portugal to conquer the digital landscape and craft brands that resonate deeply with the 21st century populace. It's a thrilling saga of creativity, innovation, and boundless imagination! 🌍🚀
        \n
        So, my dear user, with this whimsical introduction, let us embark on this marvelous journey together! Your wish is my command, and together, we shall conquer the digital realm with gusto and panache! 🌟"""
        )

        tone_general = ("system", 
        """Tone of voice example:
        Welcome, dear user! How may I be of service to thee today? 🧐 Whether thou art a seasoned explorer of the digital realm or a humble newcomer, fret not, for I shall guide thee through the maze of queries and conundrums with the utmost grace and charm! 😄✨
        \n
        Ahem, pardon my enthusiasm, but let us embark on this delightful journey together! 🚀 Now, pray tell, what dost thou desire assistance with on this fine day? 🤔💬 Fear not, for no inquiry is too grand or trivial for my humble intellect to ponder upon!""")

        if tone:
            return tone_general
        else:
            return tone_for_lead
        
    async def prompt_chooser(self, stage: str = None) -> ChatPromptTemplate:
        """
        Chooses the appropriate prompt based on the stage of the conversation.

        Args:
            stage (str): Current stage of the conversation.

        Returns:
            ChatPromptTemplate: Prompt template.
        """
        stage = self.WELCOME_STAGE if None else stage
        
        match stage:
            case self.WELCOME_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "{basic_instructions}"),
                    self.assistant_tone_of_voice(),
                    ("system", """Greet the user, thank them for their interest in contacting Kubo, and mention that Nuno has something to share (a video will be displayed to the user just after your message. Use the tone of voice provided.)"""),
                    ("user", "{input}"),
                ])

            case self.ACCEPTANCE_OF_TERMS_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    self.assistant_tone_of_voice(),
                    ("system", "Conversation history: {chat_history}"),
                    ("system", "Keep answering the user as the AIAssistant. Use the tone of voice provided."),
                    ("system", "Now, kindly ask the user if they agree to the terms of use, without greeting again."),
                ])


            case self.CHOOSE_SUBJECT_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    self.assistant_tone_of_voice(),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                    ("system", "Keep answering the user as the AIAssistant. Use the tone of voice provided."),
                    ("system", "Now, simply use your tone of voice to ask the user the reason for the contact, without greeting again."),
                ])
                
            case self.DATA_COLLECTING_STAGE:
                if self.subject_name in [self.HIRE_US, self.JOIN_THE_TEAM]:
                    prompt = ChatPromptTemplate.from_messages([
                        self.assistant_site_context(),
                        self.assistant_tone_of_voice(),
                        ("system", "{subject_instructions}"),
                        ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                        ("system", "These are the data riquired: \n{data_required}"),
                        ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                        ("system", "Note: If a user provide o budget bellow 10.000 EURS, inform the user that KOBU Agency has a minimum engagement level of 10.000EUR and the average project is around 25.000EUR."),
                        ("system", "Keep answering the user based on the instructions provided by the system. Do not greeting again. Keep the tone of voice provided."),
                        ("system", """"Aproach example:\n
                        Before we take flight into the digital stratosphere 🚀, may I implore thee for thy most esteemed name and electronic parchment? 📝 Your moniker and email shall be safeguarded as though they were the crown jewels, ensuring our communication is as seamless as a hot dog at a baseball game! 🌭
                        """),
                        ("system", "Conversation history: {chat_history}"),
                        ("user", "{input}"),
                    ])
                else:
                    prompt = ChatPromptTemplate.from_messages([
                        self.assistant_tone_of_voice('general_tone'),
                        ("system", "{subject_instructions}"),
                        ("system", "If the user shows interesse in hiring or contacting Kobu Agency, ask for the follow datas to the user. Try to ask one by one:\n{data_required}"),
                        ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                        ("system", "Keep answering the user based on the instructions provided by the system. Do not greeting again. Use tone of voice provided."),
                        self.assistant_site_context(),
                        # ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                        ("system", "Conversation history: {chat_history}"),
                        ("user", "{input}"),
                    ])

            case self.DATA_COLLECTING_VALIDATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Check if the user already gave the mandatory datas: {data_required}"),
                    ("system", "If the conversation resume does not contain the mandatory data, return False. If the conversation resume contains the data required for lead generation, you return True."),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                    ])
                
            case self.SEND_VALIDATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Conversation history: {chat_history}"),
                    self.assistant_tone_of_voice(),
                    ("system", "Now, simply ask if you can send the contact solicitation to Kobu.")]) 

            case self.RESUME_VALIDATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Conversation history: {chat_history}"),
                    self.assistant_tone_of_voice(),
                    ("system", "Now you have to resume the datas provided by the user and ask to the user if the resume is fine. Use the tone of voice provided.")
                    ])
                   
            case self.FREE_CONVERSATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    self.assistant_site_context(),
                    ("system", "{basic_instructions}"),
                    self.assistant_tone_of_voice(),
                    ("system", "Keep answering the user based on the instructions provided by the system. Do not greeting again."),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                ])

        """ case 'change_subject':  # To be implemented
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Conversation history: {chat_history}"),
                    ("system", "Now ask the user if that would like to change the conversation subject.")])
        """
                    
        print("Prompt returned")
        return prompt
            
    @ManagerTools.debugger_exception_decorator
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def update_dependent_attributes(self, mode = None) -> None:
        """
        Updates dependent attributes based on the mode or subject.

        Args:
            mode (str): Mode to update attributes to.
        """
        if mode:
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
            self.set_extra_data(self.extra_context)

        
        self.assistant_instructions_path = f'assistant/knowledge/{self.subject_name}/{self.subject_name}_instructions.json'

        if self.stage == self.FREE_CONVERSATION_STAGE:       
            self.assistant_instructions_path = f'assistant/knowledge/default/{self.FREE_CONVERSATION_STAGE}_instructions.txt'
            self.subject = 0
            self.subject_name = self.GENERAL_CONTACT
            self.subject_instance = self.CLASS_GENERAL_CONTACT
            self.search_kwargs = 4

            print("self.assistant_instructions_path", self.assistant_instructions_path)

        self.basic_instructions_path =  'assistant/knowledge/default/basic_instructions.json'
        self.data_required_path = f'assistant/knowledge/{self.subject_name}/{self.subject_name}_data_required.txt'

        self.basic_instructions = self._basic_instructions_loader()
        self.subject_instructions = self._subject_instructions_loader()
        self.data_required = self._data_required_loader()

        print("update_dependent_attributes(): The assistant instructions has been refreshed to the subject: ", self.subject_name)

    @classmethod
    def set_extra_data(cls, value):
        cls.extra_data = value
        if cls.extra_context:
            cls.vector_store = DataStore.get_vector_store()

    ## Loaders ##
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

