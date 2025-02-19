from backend.Model.kobu_assistant.core.assistant_resources.utils import Utils
from backend.Model.kobu_assistant.core.assistant_resources.assistant_prompts import Prompts
from backend.Model.kobu_assistant.core.assistant_resources.lead_extractor import LeadExtractor
from Model.Domain.Entities.enviroments import ConversationEnviroment


class BaseAssistant(Utils, Prompts):
    lead_extractor : LeadExtractor

    async def obtain_assistant_message_response(self, cv: ConversationEnviroment):
        self.update_assistant_knowledge(subject_name=cv.conversation_subject, # Need to be improoved
                                        stage=cv.current_conversation_stage)
        prompt = await self.prompt_chooser(stage=cv.current_conversation_stage)
        user_input = cv.user_input
        chain = prompt | self.llm_conversation
        return self.chain_invoker(chain=chain, user_input=user_input)
    
    async def extract_lead_from_conversation(self, cv: ConversationEnviroment):
        if self.lead_extractor.subject_name != cv.conversation_subject:
            self.lead_extractor = LeadExtractor(subject_name=cv.conversation_subject)
        return await self.lead_extractor.extract_lead(cv.conversation_history)
    