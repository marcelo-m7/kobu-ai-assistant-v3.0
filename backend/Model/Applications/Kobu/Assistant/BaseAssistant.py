from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from Utils.Prompts import Prompts, ChatPromptTemplate
from Utils.LeadExtractor import LeadExtractor
from Core.Entities.Attributes import ConversationAttributes


class BaseAssistant(Prompts):
    lead_extractor: LeadExtractor

    async def obtain_assistant_message_response(self, cv: ConversationAttributes):
        prompt = self.prompt_chooser(stage=cv.current_conversation_stage)

        if cv.extra_context_flag:
            chain = create_stuff_documents_chain(
                llm=self.llm_conversation,
                prompt=prompt
            )
            retriever = vector_store.as_retriever(search_kwargs={"k": self.search_kwargs})
            retriever_prompt = ChatPromptTemplate.from_messages([
                ("human", """Given the above conversation, generate a search query to look up 
                in order to get information relevant to the conversation"""),
                ("system", "Messages History: {conversation_history}"),
                ("human", "{user_input}")
            ])
            history_aware_retriever = create_history_aware_retriever(
                llm=self.llm_retriver,
                retriever=retriever,
                prompt=retriever_prompt
            )
            retrieval_chain = create_retrieval_chain(
                retriever,
                history_aware_retriever,
                chain
            )
            response_chain = retrieval_chain

        user_input = cv.user_input
        response_chain = prompt | self.llm_conversation
        return self.chain_invoker(chain=response_chain, user_input=user_input)
    
    async def extract_lead_from_conversation(self, cv: ConversationAttributes):
        if self.lead_extractor.subject_name != cv.conversation_subject:
            self.lead_extractor = LeadExtractor(subject_name=cv.conversation_subject)
        return await self.lead_extractor.extract_lead(cv.conversation_history)


   