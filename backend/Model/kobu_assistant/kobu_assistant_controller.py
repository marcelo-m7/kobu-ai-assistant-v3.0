import asyncio
from Domain.Entities.enviroments import ConversationEnviroment
from backend.Model.kobu_assistant.kobu_assistant import KobuAssistant
from backend.Model.kobu_assistant.core.consts import ChatConsts as c


class Conversation(KobuAssistant):
    """
    Represents the conversation model that manages communication between users and an assistant.
    """

    def __init__(self):
        pass

    async def controller(self, cv: ConversationEnviroment) -> ConversationEnviroment: 
        """
        Manages traffic responses to messages sent and received. 
        It also executes the buffer save methods.
        """
        try:
            await asyncio.create_task(
                self.conversation_buffer(cv=cv, user_input=True))
            cv = await self.get_assistant_response(cv)
            await asyncio.create_task(
                self.conversation_buffer(cv=cv, assistant_response_message=True))

        except Exception as e:
            cv.assistant_response_message = "I'm not feeling ok... Would you mind if we talk another time?"
            print(f"Conversation: controller() Error {e}")

        finally:
            return cv

    async def get_assistant_response(self, cv: ConversationEnviroment) -> ConversationEnviroment:
        while True:
            match cv.current_conversation_stage:

                case c.WELCOME_STAGE:
                    cv = await self.welcome_stage(cv)

                    if cv.current_conversation_orientation == c.RESPONSE_READY:
                        break

                    elif cv.current_conversation_orientation == c.STAGE_FINISHED:
                        cv.current_conversation_stage = c.CHOOSE_SUBJECT_STAGE
                        continue

                case c.CHOOSE_SUBJECT_STAGE:
                    cv = await self.choose_subject_stage(cv)
                    if cv.current_conversation_orientation == c.RESPONSE_READY:
                        break

                    elif cv.current_conversation_orientation == c.STAGE_FINISHED:
                        cv.current_conversation_stage = c.DATA_COLLECTING_STAGE
                        continue

                case c.DATA_COLLECTING_STAGE:
                    cv = await self.data_colecting_stage(cv)
                    if cv.current_conversation_orientation == c.RESPONSE_READY:
                        break

                    elif cv.current_conversation_orientation == c.STAGE_FINISHED:
                        cv.current_conversation_stage = c.RESUME_VALIDATION_STAGE
                        continue

                case c.RESUME_VALIDATION_STAGE:
                    cv = await self.resume_validation_stage(cv)
                    if cv.current_conversation_orientation == c.RESPONSE_READY:
                        break

                    elif cv.current_conversation_orientation == c.STAGE_FINISHED:
                        cv.current_conversation_stage = c.SEND_VALIDATION_STAGE
                        continue

                case c.SEND_VALIDATION_STAGE:
                    cv = await self.send_validation_stage(cv)
                    
                    if cv.current_conversation_orientation == c.RESPONSE_READY:
                        break

                    elif cv.current_conversation_orientation == c.STAGE_FINISHED:
                        cv.current_conversation_stage = c.FREE_CONVERSATION_STAGE
                        continue

                case c.FREE_CONVERSATION_STAGE:   # Stop doing verifications
                    cv = await self.free_validation_stage(cv)

                    if cv.current_conversation_orientation == c.RESPONSE_READY:
                        break

                    elif cv.current_conversation_orientation == c.STAGE_FINISHED:
                        cv.current_conversation_stage = c.CHOOSE_SUBJECT_STAGE
                        continue
                
                case _:
                    cv.current_conversation_orientation = c.PROCEED
                    cv.assistant_reponse_orientation = c.PROCEED
                    continue

            return cv
