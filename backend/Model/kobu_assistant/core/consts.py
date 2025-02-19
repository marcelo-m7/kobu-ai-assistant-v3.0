class Stages:
    # STAGES POSSIBLES
    WELCOME_STAGE = 'welcome'  # Welcome stage
    ACCEPTANCE_OF_TERMS_STAGE = 'acceptance_of_terms'
    CHOOSE_SUBJECT_STAGE = 'choose_subject'  # Stage to choose a subject
    DATA_COLLECTING_STAGE = 'data_colecting'  # Data collecting stage
    DATA_COLLECTING_VALIDATION_STAGE = 'data_colecting_validation'  # Data collecting validation stage
    RESUME_VALIDATION_STAGE = 'resume_validation'  # Resume validation stage
    SEND_VALIDATION_STAGE = 'send_validation'  # Send validation stage
    FREE_CONVERSATION_STAGE = 'free_conversation'  # Free conversation stage
    # OPTIONS POSSIBLES BY STAGES
    ACCEPTANCE_OF_TERMS_STAGE_OPTIONS = [
        "I agree to the terms and conditions.",
        "I do not agree to the terms and conditions."
    ]  # Options for the acceptance of terms stage
    CHOOSE_SUBJECT_STAGE_OPTIONS = [
        "I'd like to know more about KOBU Agency.",
        "I'd like to hire KOBU.",
        "I'd like to join KOBU team.",
        # "I'd like to talk to somebody in KOBU Agency."
    ]  # Options for the choose subject stage
    RESUME_VALIDATION_STAGE_OPTIONS = [
        "It looks fine!",
        "Actually I'd like to change something, if you don't mind."
    ]  # Options for the resume validation stage
    SEND_VALIDATION_STAGE_OPTIONS = [
        "Yes, you may send!",
        "Wait. Do not send it yet, please."
    ]  # Options for the send validation stage


class FlowOrientations:
    # CONVERSATION POSSIVLES ORIENTATIONS
    RESPONSE_READY = 'response_ready'
    STAGE_FINISHED = 'stage_finished'
    NEXT_STAGE = 'next_stage'  # Proceed to the next stage
    # ASSISTANT NEXT ORIENTATIONS POSSIBLES
    PROCEED = 'proceed'  # Proceed with the current stage
    VERIFY_ANSWER = 'verify_answer'  # Verify the answer


class Subjects:
    """
    Utility class containing constant values used throughout the chat application.
    """
    from assistant_resources.subjects_lead_extractor import HireUs, GeneralContact, JoinTheTeam, LeadExtractor
    
    # SUBJECTS POSSIBLES
    GENERAL_CONTACT = 'general_contact'
    HIRE_US = 'hire_us'
    JOIN_THE_TEAM = 'join_the_team'
    # Initialize instances of subjects
    CLASS_GENERAL_CONTACT = GeneralContact(GENERAL_CONTACT)
    CLASS_HIRE_US = HireUs(HIRE_US)
    CLASS_JOIN_THE_TEAM = JoinTheTeam(JOIN_THE_TEAM)
    
    def subject_instance(self, subject) -> LeadExtractor:
        match subject:
            case self.GENERAL_CONTACT:
                return self.CLASS_GENERAL_CONTACT
            case self.HIRE_US:
                return self.CLASS_HIRE_US
            case self.JOIN_THE_TEAM:
                return self.CLASS_JOIN_THE_TEAM
              
class Paths:
    BUFFER_SAVER_FILE_PATH = 'kobu-assistant/.buffer/buffer.json'
    EXPOERTED_LEAD_DATAS = 'kobu-assistant/.buffer/lead_datas.json'

class KnowledgeDatas:
    EXTRA_CONTEXT_FLAG: bool = True
    BASIC_INSTRUCTIONS_PATH =  'kobu-assistant/core/knowledge/default/basic_instructions.json'

    def __init__(self):
        super().__init__()
        self.assistant_instructions_path: str = 'kobu-assistant/core/knowledge/{subject_name}/{self.subject_name}_instructions.json'
        self.data_required_path: str = 'kobu-assistant/core/knowledge/{subject_name}/{subject_name}_data_required.txt'
        self.basic_instructions_path: str = 'kobu-assistant/core/knowledge/default/basic_instructions.json'

    @property
    def assistant_instructions_path(self, subject_name):
        return self.assistant_instructions_path.format(subject_name=subject_name)
    
    @property
    def data_required_path(self, subject_name):
        return self.data_required_path.format(subject_name=subject_name)

         

class ChatConsts(Stages, FlowOrientations, Subjects, Paths):
    pass