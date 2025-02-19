class Conversation(User):
    def __init__(self):
        self.user_input = self.request.get('user_input')
        self.lead = None
        self.conversation_subject = str
        self.conversation_history = list
        self.current_conversation_stage = str
        self.extra_context : bool = True

        self.assistant_response_message = str
        self.assistant_reponse_orientation = str
        self.current_conversation_orientation = str

        self.conversation_options_flag = bool
        self.conversation_options = list
