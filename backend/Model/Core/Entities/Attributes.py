from User import User
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class ConversationAttributes:
    def __init__(self, user: User):
        self.user_input: str = user.user_input
        self.id: int = user.user_id

        self.lead: any
        self.conversation_history: list
        self.conversation_subject: str
        self.extra_context_flag: bool = True

        self.current_conversation_stage: str
        self.assistant_response_message: str
        self.assistant_reponse_orientation: str
        self.current_conversation_orientation: str

        self.conversation_options_flag: bool
        self.conversation_options: list

class ContextLoaderAttributes():
    llm_conversation: ChatOpenAI = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")
    llm_validation: ChatOpenAI = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")
    llm_retriver: ChatOpenAI = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

    def __init__(self, extra_context_flag: bool = True):
        self.extra_context_flag: bool = extra_context_flag
        self.vector_store: any

class PromptsAttributes(ConversationAttributes, ChatPromptTemplate):
    def __init__(self,
                 basic_instructions,
                 data_required,
                 extra_context_flag,
                 conversation_subject,
                 conversation_current_stage):
        
        self.extra_context_flag=extra_context_flag
        self.basic_instructions = basic_instructions
        self.data_required = data_required
        self.conversation_subject = conversation_subject
        self.conversation_current_stage = conversation_current_stage
