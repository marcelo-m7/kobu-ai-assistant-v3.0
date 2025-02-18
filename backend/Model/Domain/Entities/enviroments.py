class User:
    def __init__(self, user_id=int, request=dict):
        self.user_id = user_id
        self.request = request
        self.user_input = self.request.get('user_input')
        self.lead = None
        self.current_request = None
        self.previous_request = None

class ConversationAttributes(User):
    def __init__(self):
        self.conversation_subject = str
        self.conversation_history = list
        self.current_conversation_stage = str

        self.assistant_response_message = str
        self.assistant_reponse_orientation = str
        self.current_conversation_orientation = str

        self.conversation_options_flag = bool
        self.conversation_options = list

class ConversationEnviroment(ConversationAttributes):
    def __init__(self, user_instance: User):
        super().__init__(user_instance)


    @property
    def request(self):
        return self.request
    
    @request.setter
    def request(self, request):
        if request:
            self.previous_request = self.current_request
            self.current_request = request
            self._refresh_enviroment(request=request)
        return self.current_request
    
    def _refresh_enviroment(self, request):
        """
        Updates the class attributes based on the keys and values provided in the dictionary.

        :param request: Dictionary containing the updates for the class attributes.
        """
        if not isinstance(request, dict):
            raise ValueError("The 'request' parameter must be a dictionary.")

        for key, value in request.items():
            if hasattr(self, key):  # Checks if the attribute exists in the class
                setattr(self, key, value)  # Updates the attribute value
            else:
                print(f"Attribute '{key}' does not exist in the class and will be ignored.")
                
