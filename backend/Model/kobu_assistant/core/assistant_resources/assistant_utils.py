import json
import asyncio
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from Domain.Entities.enviroments import ConversationEnviroment


class Utils():
    """
    Utility functions for handling chat history, saving lead data, and invoking chat chains.
    """
    buffer_saver_file_path = 'assistant/buffer/buffer.json'
    exported_lead_datas = 'assistant/buffer/lead_datas.json'

    async def conversation_buffer(self, cv: ConversationEnviroment,
                                  user_input: bool = False, 
                                  assistant_response_message: bool = False, 
                                  system_message: str = None) -> None:
        try: 
            
            if user_input:
                cv.conversation_history.append(HumanMessage(content=cv.user_input))

            if assistant_response_message:
                cv.conversation_history.append(AIMessage(content=cv.assistant_response_message))
                cv.conversation_history.append(SystemMessage(content=f"Awnswered at: {datetime.now()}"))

            if system_message:
                cv.conversation_history.append(SystemMessage(content=f"{system_message}\nSystem Message set at: {datetime.now()}"))
                
            print("Buffer saved in cv.conversation_history list")

        except Exception as e:
            print(f"chat_buffer Error {e}")
    
    async def conversation_buffer_local(self, user_input: str, response: str) -> None:
        """
        Save the chat history in a JSON file.
        
        Args:
            user_input (str): User input message.
            response (str): Assistant response message.
        """

        messages_history = []
        messages_history.append({'role': 'user', 'content': user_input})
        messages_history.append({'role': 'assistant', 'content': response})
        messages_history.append({'role': 'system', 'content': datetime.now()})
        try:
            try:
                with open(self.buffer_saver_file_path, 'r', encoding='utf-8') as existing_json_file:
                    existing_data = json.load(existing_json_file)
            except FileNotFoundError:
                existing_data = []

            existing_data.extend(messages_history)
            with open(self.buffer_saver_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

            print(f'cv.conversation_history saved in {self.buffer_saver_file_path}')
        except Exception as e:
            print(f"chat_buffer_saver Error {e}")

    def chain_invoker(self, cv: ConversationEnviroment, chain) -> str:
        """
        Invoke the main chain and return the assistant response.
        """
        try:
            response = chain.invoke({
                "user_input": cv.user_input, 
                "conversation_history": cv.conversation_history, 
                "lead_string": str(cv.lead).strip('{').strip('}').strip(']').strip(']'),

                "subject_instructions": self.subject_instructions,
                "basic_instructions": self.basic_instructions, 
                "data_required": self.data_required})
            
            print("chain_invoker(): The chain has been invoked.")

            if type(response) == dict:
                message = response['answer']
            else:
                message = response.content

        except AttributeError as e:
            if "'list' object has no attribute 'content'" in str(e):
                print(f"chain_invoker Error: {e}")
                message = response
        except Exception as e:
            print(f"chain_invoker Error {e}")
            message = "I'm not feeling ok... Would you mind if we talk another time?"
            
        finally:
            cv.assistant_response_message = message
            return cv

    async def chain_builder(self, stage: str = '') -> object:
        """
        Build the main chain that will answer the user_input.
        
        Args:
            stage (str): Stage of the conversation.
        
        Returns:
            object: Main chat chain.
        """
        print("chain_builder starts")

        try:
            # prompt = await asyncio.create_task(self.prompt_chooser(stage=stage))
            prompt = await asyncio.create_task(self.prompt_chooser(stage=stage))

            if self.extra_context == False:
                chain = prompt | self.llm_conversation
                return chain
        
            elif self.extra_context == True:          # Add a retriever to the chain with the extra context obtained
                print("self.extra_context == True")
                
                chain = create_stuff_documents_chain(
                    llm=self.llm_retriver,
                    prompt=prompt
                )

                retriever = self.vector_store.as_retriever(search_kwargs={"k": self.search_kwargs})
                    
                retriever_prompt = ChatPromptTemplate.from_messages([
                    # MessagesPlaceholder(variable_name="chat_history"),
                    ("human", """Given the above conversation, generate a search query to look up 
                     in order to get information relevant to the conversation"""),
                    ("system", "Messages History: {chat_history}"),
                    ("human", "{input}")
                ])

                history_aware_retriever = create_history_aware_retriever(
                    llm=self.llm_retriver,
                    retriever=retriever,
                    prompt=retriever_prompt
                )

                # history_aware_retriever_response = self.chain_invoker(history_aware_retriever) # Verify context added
                # print("History_aware_retriever:\n", history_aware_retriever_response)

                retrieval_chain = create_retrieval_chain(
                    # retriever,
                    history_aware_retriever,
                    chain
                )

                return retrieval_chain

        except Exception as e:
            print(f"chain_builder Error {e}")
            return False
