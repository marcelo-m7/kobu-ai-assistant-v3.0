from backend.Model.kobu_assistant.core.assistant_resources.assistant_utils import Utils
from backend.Model.kobu_assistant.core.assistant_resources.assistant_prompts import Prompts
from Model.Domain.Entities.enviroments import ConversationEnviroment
from consts import Subjects as s


class BaseAssistant(Utils, Prompts):

    async def obtain_assistant_message_response(self, cv: ConversationEnviroment):
        self.update_assistant_knowledge(subject_name=cv.conversation_subject, 
                                        stage=cv.current_conversation_stage)
        prompt = await self.prompt_chooser(stage=cv.current_conversation_stage)
        user_input = cv.user_input
        chain = prompt | self.llm_conversation
        return self.chain_invoker(chain=chain, user_input=user_input)
    
    async def extract_lead_from_conversation(self, cv: ConversationEnviroment):
        subject_instance: s.LeadExtractor = s.subject_instance(cv.conversation_subject)
        lead = await subject_instance.get_leads_info(cv.conversation_history)
        return lead
    