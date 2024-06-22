import logging
import asyncio
from .assistant import Assistant
from .tools.lead_handlers import LeadHandlers


class StageHandlers(Assistant, LeadHandlers):

    async def get_assistant_response(self, user_request: dict = {}) -> dict:
        """
        Answers the user_input and manages conversation state changes based on data detection for lead generation.

        Args:
            user_request (dict, optional): The user's request.

        Returns:
            dict: The response to the user's request.
        """
        response = {}
        try:
            logging.info(f"Current stage: {self.current_stage}")
            self.initialize_stage()

            while True:
                response = await self.process_stage(user_request)
                if response.get('orientation') == self.NEXT_STAGE:
                    self.current_stage = self.next_stage
                    continue
                elif response.get('orientation') == self.PROCEED:
                    break

        except Exception as e:
            logging.error(f"Chat get_assistant_response() Error: {e}")
            response = self.handle_error()

        finally:
            self.set_user_attributes(response)
            return response

    def initialize_stage(self):
        if not self.current_stage:
            self.current_stage = self.WELCOME_STAGE
            logging.info(f"Current stage initialized to: {self.current_stage}")

        if self.orientation == self.NEXT_STAGE:
            self.current_stage = self.next_stage
            self.orientation = self.PROCEED
            logging.info(f"Stage and orientation set to: {self.current_stage}, {self.orientation}")

    async def process_stage(self, user_request: dict) -> dict:
        match self.current_stage:
            case self.WELCOME_STAGE:
                return await self.handle_welcome_stage(user_request)

            case self.CHOOSE_SUBJECT_STAGE:
                return await self.handle_choose_subject_stage(user_request)

            case self.DATA_COLLECTING_STAGE:
                return await self.handle_data_collecting_stage(user_request)

            case self.RESUME_VALIDATION_STAGE:
                return await self.handle_resume_validation_stage(user_request)

            case self.SEND_VALIDATION_STAGE:
                return await self.handle_send_validation_stage(user_request)

            case self.FREE_CONVERSATION_STAGE:
                return await self.handle_free_conversation_stage(user_request)

            case self.CRITICAL:
                return await self.handle_critical_stage(user_request)

    async def handle_welcome_stage(self, user_request):
        response = await self.welcome(user_request)
        self.set_user_attributes(response)
        if response.get('orientation') == self.NEXT_STAGE:
            self.next_stage = self.CHOOSE_SUBJECT_STAGE
        else:
            self.next_stage = self.current_stage
        return response

    async def handle_choose_subject_stage(self, user_request):
        response = await self.choose_subject(user_request)
        self.set_user_attributes(response)
        if response.get('orientation') == self.NEXT_STAGE:
            self.next_stage = self.DATA_COLLECTING_STAGE
            self.subject = response.get('choosed_subject')
            logging.info(f"Subject chosen: {self.subject}")
        else:
            self.next_stage = self.current_stage
        return response

    async def handle_data_collecting_stage(self, user_request):
        validation = await self.data_colecting_validation(user_request)
        response = await self.data_colecting(user_request)
        self.set_user_attributes(response)
        if validation.get('orientation') == self.PROCEED:
            self.next_stage = self.DATA_COLLECTING_STAGE
            self.orientation = self.VERIFY_ANSWER
        elif validation.get('orientation') == self.NEXT_STAGE:
            self.next_stage = self.RESUME_VALIDATION_STAGE
            self.orientation = self.PROCEED
            await self.chat_buffer(system_message=f"Datas detected: {self.lead}")
        return response

    async def handle_resume_validation_stage(self, user_request):
        response = await self.resume_validation(user_request)
        self.set_user_attributes(response)
        if response.get('orientation') == self.VERIFY_ANSWER and response.get('message') not in ['false', 'true']:
            self.next_stage = self.RESUME_VALIDATION_STAGE
        else:
            if response.get('message') == 'true':
                self.next_stage = self.SEND_VALIDATION_STAGE
                self.orientation = self.PROCEED
            else:
                self.next_stage = self.DATA_COLLECTING_STAGE
                self.orientation = self.VERIFY_ANSWER
        return response

    async def handle_send_validation_stage(self, user_request):
        response = await self.send_validation(user_request)
        self.set_user_attributes(response)
        if response.get('orientation') == self.VERIFY_ANSWER and response.get('message') not in ['false', 'true']:
            self.next_stage = self.SEND_VALIDATION_STAGE
        else:
            if response.get('message') == 'true':
                self.lead = self.subject_instance.get_leads_info(self.chat_history)
                await self.send_leads_info()
                self.subject = 0
                self.next_stage = self.FREE_CONVERSATION_STAGE
                self.orientation = self.PROCEED
            else:
                self.next_stage = self.RESUME_VALIDATION_STAGE
                self.orientation = self.VERIFY_ANSWER
        return response

    async def handle_free_conversation_stage(self, user_request):
        return await self.free_conversation(user_request)

    async def handle_critical_stage(self, user_request):
        response = await self.critical(user_request)
        logging.info(f"Critical Conversation Response:\n{response}")
        return response

    def handle_error(self):
        message = "I'm not feeling ok... Would you mind if we talk another time?"
        response = {"message": message, 'orientation': self.orientation, 'current_stage': 'error'}
        return response
