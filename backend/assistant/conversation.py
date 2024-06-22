import asyncio
from .tools.manager_tools import *
from .stage_handlers import StageHandlers
import logging


class Conversation(StageHandlers):
# import asyncio
# from .tools.manager_tools import ManagerTools, retry, wait_random_exponential, stop_after_attempt
# from .tools.lead_handlers import LeadHandlers
# from .assistant import Assistant

# class Conversation(Assistant, LeadHandlers):
    """
    Represents a chat interface that manages communication between users and an assistant.

    Attributes:
        extra_context (bool): Indicates whether extra context is enabled. Defaults to False.
    """
    extra_context = False # Stay always True if subject is General (init config)

    def __init__(self, stage: str, subject: int = 0) -> None:
        """
        Initializes a Chat instance.

        Args:
            stage (str): The current stage of the chat.
            subject (int, optional): The subject of the chat. Defaults to 0.
        """
        super().__init__(stage)
        self._subject = subject
        self.stage = stage
        self.chat_history = []
        self.lead = None
        self.save_chat_mode = False
        self.lead_generation = True # Default
        print("Current subject number: ", subject)
        logging.basicConfig(level=logging.INFO)

    # @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    # @ManagerTools.debugger_exception_decorator # It is seted in this function for to test proposes 
    async def main(self, user_request) -> dict: 
        """
        Manages traffic responses to messages sent and received. 
        It also executes the buffer save methods.

        Args:
            user_request (dict): The user's request.

        Returns:
            dict: The response to the user's request.
        """
        print("Conversation: main() Starts")

        try:
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

    # The follow methodol is not completed integrated.
    # @ManagerTools.debugger_exception_decorator
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
        
    @property
    def subject(self) -> int:
        """int: The subject of the chat."""
        return self._subject

    @subject.setter
    def subject(self, new_subject: int) -> None:
        self._subject = new_subject
        self.update_dependent_attributes()