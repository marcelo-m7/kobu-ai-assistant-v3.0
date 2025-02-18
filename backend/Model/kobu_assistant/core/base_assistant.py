from backend.Model.kobu_assistant.core.assistant_resources.assistant_utils import Utils
from backend.Model.kobu_assistant.core.assistant_resources.assistant_prompts import Prompts
from Model.Domain.Entities.enviroments import ConversationEnviroment


class BaseAssistant(Utils, Prompts):

    async def obtain_assistant_message_response(self, cv: ConversationEnviroment):
        prompt = await self.prompt_chooser(stage=cv.current_conversation_stage)
        user_input = cv.user_input
        chain = prompt | self.llm_conversation
        return self.chain_invoker(chain=chain, user_input=user_input)
    