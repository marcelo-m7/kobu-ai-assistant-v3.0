import asyncio
from ..conversation_tools.manager_tools import *
from ..conversation_agents.agents_tools.external_tools.lead_handlers import LeadHandlers
from ..conversation_agents.agents_stages.assistant import Assistant


class Chat(Assistant, LeadHandlers):
    """
    Represents a chat interface that manages communication between users and an assistant.

    Attributes:
        extra_context (bool): Indicates whether extra context is enabled. Defaults to False.
    """

    def __init__(self, stage: str, subject: int = 0, user_id=None, subject_name=None, lead=None) -> None:
        """
        Initializes a Chat instance.

        Args:
            stage (str): The current stage of the chat.
            subject (int, optional): The subject of the chat. Defaults to 0.
            user_id (str, optional): The user ID. Defaults to None.
            subject_name (str, optional): The subject name. Defaults to None.
            lead (str, optional): The lead information in JSON format. Defaults to None.
        """

        # Initialize Chat specific attributes
        self._subject = subject
        self.stage = stage
        self.chat_history = []
        self.lead = lead
        self.current_stage
        self.next_stage
        self.orientation
        self.save_chat_mode = False
        
        # Initialize parents
        Assistant.__init__(self, stage)
        LeadHandlers.__init__(self, user_id, subject_name, lead, chat_history=[])

        print("Current subject number: ", subject)

    async def main(self, user_request) -> dict: 
        """
        Manages traffic responses to messages sent and received. 
        It also executes the buffer save methods.

        Args:
            user_request (dict): The user's request.

        Returns:
            dict: The response to the user's request.
        """
        print("Chat: main() Starts")

        try:
            self.set_user_attributes(response)
            current_conversation = self.get_conversation_atributes()
            # Buffer conversation
            self.get_assistant_response(current_conversation)

        except Exception as e:
            response = {"message": "I'm not feeling ok... Would you mind if we talk another time?",
                        'orientation': '', 'current_stage': 'error'}
            print(f"Chat: main() Error {e}")

        finally:
            return response
        
    def get_conversation_atributes(self) -> dict:
        return vars(self)

    async def get_assistant_response(self, conversation: dict = {}) -> dict:
        """
        Answers the user_input and manages conversation state changes based on data detection.
        """
        try:
            while True:
                match self.current_stage:
                    case self.WELCOME_STAGE:
                        response = await self.welcome(conversation)
                        self.set_user_attributes(response)
                        print("Welcome Response:\n", response)

                        if response['orientation'] == self.NEXT_STAGE:
                            self.next_stage = self.CHOOSE_SUBJECT_STAGE
                            # self.next_stage = self.ACCEPTANCE_OF_TERMS_STAGE # The ACCEPTANCE_OF_TERMS_STAGE case is beeing integrated.
                            break

                        else:
                            self.current_stage = self.next_stage
                            continue
                    
                    case self.CHOOSE_SUBJECT_STAGE:
                        response = await self.choose_subject(conversation)
                        self.set_user_attributes(response)
                        print("Choose Subject Response:\n", response)

                        if response['orientation'] == self.NEXT_STAGE:
                            continue

                        else:
                            self.current_stage = self.next_stage
                            break
                                
                    case self.DATA_COLLECTING_STAGE:
                        validation = await asyncio.create_task(self.data_colecting_validation(conversation))
                        # response = await asyncio.create_task(self.data_colecting_in_changing(conversation))
                        response = await asyncio.create_task(self.data_colecting(conversation))
                        self.set_user_attributes(response)
                        print("Data Collecting Response:\n", response)

                        if validation['orientation'] == self.PROCEED:

                            break
                            # del response['options']

                        elif validation['orientation'] == self.NEXT_STAGE:

                            continue

                    case self.RESUME_VALIDATION_STAGE:
                        response = await self.resume_validation(conversation)
                        print("Resume Validation Response:\n", response)
                        self.set_user_attributes(response)
                        # self.debugger_print(response)
                        # self.debugger_sleeper(2)

                        if response['orientation'] == self.VERIFY_ANSWER and response['message'] not in ['false', 'true']:

                            break
                        
                        else:   # if response['orientation'] == self.NEXT_STAGE:

                            continue

                    case self.SEND_VALIDATION_STAGE:
                        response = await self.send_validation(conversation)
                        self.set_user_attributes(response)
                        print("Send Validation Response:\n", response)

                        if response['orientation'] == self.VERIFY_ANSWER and response['message'] not in ['false', 'true']:
                            self.next_stage = self.SEND_VALIDATION_STAGE
                            break

                        else:    # if response['orientation'] == self.NEXT_STAGE:
                            continue

                    case self.FREE_CONVERSATION_STAGE:   # Stop going verifications
                        response = await self.free_conversation(conversation)
                        print("Free Conversation Response:\n", response)
                        break
                    
                    case self.CRITICAL: # To bem implemented
                        response = await self.critical(conversation)
                        print("Critial Conversation Response:\n", response)
                        break

        except Exception as e:
            print(f"Chat get_assistant_response() Error {e}")
            message = "I'm not feeling ok... Would you mind if we talk another time?"
            response = {"message": message,'orientation': self.orientation, 'current_stage': 'error'}
    
        finally:
            # self.debugger_print(response)
            self.set_user_attributes(response)
            return response
        

    @property
    def subject(self) -> int:
        """int: The subject of the chat."""
        return self._subject

    @subject.setter
    def subject(self, new_subject: int) -> None:
        self._subject = new_subject
        self.update_dependent_attributes()
