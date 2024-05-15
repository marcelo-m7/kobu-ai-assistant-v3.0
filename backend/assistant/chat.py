import asyncio
from .tools.manager_tools import *
from .tools.lead_handlers import LeadHandlers
from .assistant import Assistant


class Chat(Assistant, LeadHandlers):
    """
    Represents a chat interface that manages communication between users and an assistant.

    Attributes:
        extra_context (bool): Indicates whether extra context is enabled. Defaults to False.
    """
    def __init__(self, stage: str, subject: int = 0) -> None:
        """
        Initializes a Chat instance.

        Args:
            stage (str): The current stage of the chat.
            subject (int, optional): The subject of the chat. Defaults to 0.
        """
        super().__init__(stage) #, subject)
        self._subject = subject
        self.stage = stage
        self.chat_history = []
        self.lead = None
        self.save_chat_mode = False
        self.lead_generation = True # Default
        print("Current subject number: ", subject)
    
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    @ManagerTools.debugger_exception_decorator
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
            await asyncio.create_task(self.refresh_stages())
            user_input = user_request.get("user_input")
            await asyncio.create_task(self.chat_buffer(user_input=user_input))
            response = await self.get_assistant_response(user_request)
            await asyncio.create_task(self.chat_buffer(response=response['message']))

            if self.save_chat_mode:
                await asyncio.create_task(self.chat_buffer_saver(user_input=user_input, response=response.get('message')))

        except Exception as e:
            response = {"message": "I'm not feeling ok... Would you mind if we talk another time?",
                        'orientation': '', 'current_stage': 'error'}
            print(f"Chat: main() Error {e}")

        finally:
            return response

    async def get_assistant_response(self, user_request: dict = {}) -> dict:
        """
        Answers the user_input and manages conversation state changes based on data detection.
        """
        try:
            while True:
                match self.current_stage:
                    case self.WELCOME_STAGE:
                        response = await self.welcome(user_request)
                        self.set_user_attributes(response)
                        print("Welcome Response:\n", response)

                        if response['orientation'] == self.NEXT_STAGE:
                            self.next_stage = self.CHOOSE_SUBJECT_STAGE
                            # self.next_stage = self.ACCEPTANCE_OF_TERMS_STAGE # The ACCEPTANCE_OF_TERMS_STAGE case is beeing integrated.
                            break

                        else:
                            self.current_stage = self.next_stage
                            continue
                    
                    # The ACCEPTANCE_OF_TERMS_STAGE case is beeing integrated.
                    case self.ACCEPTANCE_OF_TERMS_STAGE:
                        response = await self.acceptance_of_terms(user_request)
                        self.set_user_attributes(response)
                        print("ACCEPTANCE_OF_TERMS Response:\n", response)

                        if response['orientation'] == self.VERIFY_ANSWER and response['message'] not in ['false', 'true']:
                            print("Inside of if response['orientation'] == self.VERIFY_ANSWER")
                            self.next_stage = self.ACCEPTANCE_OF_TERMS_STAGE
                            break
                        
                        else:
                            if response['message'] == 'true':
                                self.current_stage = self.next_stage = self.CHOOSE_SUBJECT_STAGE
                                self.orientation = self.PROCEED
                                print("Inside of if response['message'] == 'true': ")
                                

                            else:
                                response['current_stage'] = self.next_stage = self.current_stage = self.WELCOME_STAGE # Missing to configurate a stage for decline terms
                                response['orientation'] = self.orientation = self.VERIFY_ANSWER
                                print("New current_stage after message 'false': ", self.current_stage)
                                print("Current Stage After False: ", self.current_stage, self.orientation)
        
                            del response['options']
                            continue

                    case self.CHOOSE_SUBJECT_STAGE:
                        response = await self.choose_subject(user_request)
                        self.set_user_attributes(response)
                        print("Choose Subject Response:\n", response)

                        if response['orientation'] == self.NEXT_STAGE:
                            self.next_stage = self.current_stage = self.DATA_COLLECTING_STAGE
                            self.orientation = self.PROCEED
                            self.subject = response['choosed_subject']
                            print("Subject choosed: ", self.subject_name)
                            print("subject_instance: ", self.subject_instance)
                            continue

                        else:
                            self.current_stage = self.next_stage
                            break
                                
                    case self.DATA_COLLECTING_STAGE:
                        validation = await asyncio.create_task(self.data_colecting_validation(user_request))
                        # response = await asyncio.create_task(self.data_colecting_in_changing(user_request))
                        response = await asyncio.create_task(self.data_colecting(user_request))
                        self.set_user_attributes(response)
                        print("Data Collecting Response:\n", response)

                        if validation['orientation'] == self.PROCEED:
                            self.next_stage = self.DATA_COLLECTING_STAGE
                            self.orientation = self.VERIFY_ANSWER
                            break
                            # del response['options']

                        elif validation['orientation'] == self.NEXT_STAGE:
                            # response = await self.data_colecting(user_request)
                            self.current_stage = self.next_stage = self.RESUME_VALIDATION_STAGE
                            self.orientation = self.PROCEED

                            # self.lead = self.subject_instance.get_leads_info(self.chat_history)
                            await asyncio.create_task(self.chat_buffer(system_message=f"Datas detected: {self.lead}"))

                            continue

                    case self.RESUME_VALIDATION_STAGE:
                        response = await self.resume_validation(user_request)
                        print("Resume Validation Response:\n", response)
                        self.set_user_attributes(response)
                        # self.debugger_print(response)
                        # self.debugger_sleeper(2)

                        if response['orientation'] == self.VERIFY_ANSWER and response['message'] not in ['false', 'true']:
                            print("Inside of if response['orientation'] == self.VERIFY_ANSWER")
                            self.next_stage = self.RESUME_VALIDATION_STAGE
                            break
                        
                        else:   # if response['orientation'] == self.NEXT_STAGE:
                            if response['message'] == 'true':
                                self.current_stage = self.next_stage = self.SEND_VALIDATION_STAGE
                                self.orientation = self.PROCEED
                                print("Inside of if response['message'] == 'true': ")

                            else:    # elif response['message'] == 'false':  # IT IS NOT WORKIG AS IT SHOULD
                                response['current_stage'] = self.next_stage = self.current_stage = self.DATA_COLLECTING_STAGE
                                response['orientation'] = self.orientation = self.VERIFY_ANSWER
                                print("New current_stage after message 'false': ", self.current_stage)
                                print("Current Stage After False: ", self.current_stage, self.orientation)
        
                            del response['options']
                            continue

                    case self.SEND_VALIDATION_STAGE:
                        response = await self.send_validation(user_request)
                        self.set_user_attributes(response)
                        print("Send Validation Response:\n", response)

                        if response['orientation'] == self.VERIFY_ANSWER and response['message'] not in ['false', 'true']:
                            self.next_stage = self.SEND_VALIDATION_STAGE
                            break

                        else:    # if response['orientation'] == self.NEXT_STAGE:
                            if response['message'] == 'true':

                                self.lead = self.subject_instance.get_leads_info(self.chat_history)
                                await asyncio.create_task(self.send_leads_info())
                                self.subject = 0
                                self.current_stage = self.next_stage = self.FREE_CONVERSATION_STAGE
                                self.orientation = self.PROCEED
                                del response['options']

                            else:   # elif response['message'] == 'false':
                                response['current_stage'] =  self.current_stage = self.next_stage = self.RESUME_VALIDATION_STAGE
                                response['orientation'] = self.orientation = self.VERIFY_ANSWER

                            # del response['options']
                            continue

                    case self.FREE_CONVERSATION_STAGE:   # Stop going verifications
                        response = await self.free_conversation(user_request)
                        print("Free Conversation Response:\n", response)
                        break
                    
                    case self.CRITICAL: # To bem implemented
                        response = await self.critical(user_request)
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
        
    @ManagerTools.debugger_exception_decorator
    async def refresh_stages(self) -> None:
        """
        Updates the status of the conversation, based on the orientation setted.
        """
        print("Current stage: ", self.current_stage)
        if not self.current_stage:
            self.current_stage = self.WELCOME_STAGE
            print("Current stage changed from '' to: ", self.current_stage)

        if self.orientation == self.NEXT_STAGE:
            self.current_stage = self.next_stage
            self.orientation = self.PROCEED
            print("Current stage changed to: ", self.current_stage)
            print("Orientation changed to: ", self.orientation)

    @property
    def subject(self) -> int:
        """int: The subject of the chat."""
        return self._subject

    @subject.setter
    def subject(self, new_subject: int) -> None:
        self._subject = new_subject
        self.update_dependent_attributes()

    # The follow methodol is not completed integrated.
    @ManagerTools.debugger_exception_decorator
    async def main_critical(self, user_request) -> dict: 
        """
        [METHOD IN TESTING] Manages traffic responses to messages in case of Critical Mode. 
        It also executes the buffer save methods.

        Args:
            user_request (dict): The user's request.

        Returns:
            dict: The response to the user's request.
        """
        print("main_critical() Starts")

        try:
            self.debugger_sleeper(2)
            await self.chat_buffer(system_message="""A error has been indentify. You will not be able to answer datas from KOBU Agency Website,
                            but still can generate and send a lead to Kobu to be analysed.""")
            
            self.current_stage = self.CRITICAL
            
            if not isinstance(user_request, dict):
                user_request = {'user_input': user_request}

            response = await self.get_assistant_response(user_request)
            self.update_dependent_attributes(code = self.CRITICAL)
            await self.chat_buffer(response=response['message'])

        except Exception as e:
            response = {"message": "I'm not feeling ok... Would you mind if we talk another time?",
                        'orientation': '', 'current_stage': 'error'}
            
            print(f"main_critical() Error {e}")

        finally:
            return response