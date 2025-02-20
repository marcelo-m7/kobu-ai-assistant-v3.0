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
    # SUBJECTS POSSIBLES
    GENERAL_CONTACT = 'general_contact'
    HIRE_US = 'hire_us'
    JOIN_THE_TEAM = 'join_the_team'
              
class Paths:
    # ASSISTANT BUFFER PATHS
    BUFFER_SAVER_FILE_PATH = 'kobu-assistant/.buffer/buffer.json'
    EXPOERTED_LEAD_DATAS = 'kobu-assistant/.buffer/lead_datas.json'
    # KNWOLEDGE PATHS
    EXTRA_CONTEXT_FLAG: bool = True
    BASIC_INSTRUCTIONS_PATH =  'kobu-assistant/core/knowledge/basic_instructions.json'
    DATA_REQUIRED_PATH: str = 'kobu-assistant/core/knowledge/{subject_name}/{subject_name}_data_required.txt'
    ASSISTANT_INSTRUCTIONS_PATH: str = 'kobu-assistant/core/knowledge/{subject_name}/{self.subject_name}_instructions.json'
    FUNCTION_DESCRIPTION_PATH ='kobu-assistant/core/knowledge/{subject_name}/{subject_name}_function_description.json'

class ChatConsts(Stages, FlowOrientations, Subjects, Paths):
    pass
