from langchain_core.prompts import ChatPromptTemplate
from ...agents_tools.internal_tools.prompts import Prompts

class ChooseSubjectResponder(Prompts):

    async def choose_subject(self, user_request: dict) -> dict:
        """Sends the subjects to the user to be choosed."""
        print("ResponseHandler: choose_subject()")
        self.current_stage = self.CHOOSE_SUBJECT_STAGE

        try:
            user_input = user_request.get('user_input')
            if self.orientation == self.VERIFY_ANSWER:  # In case the user already choosed a subject
                try:
                    self.subject = self.CHOOSE_SUBJECT_STAGE_OPTIONS.index(user_input)
                    message = f"The user choosed subject: {self.subject}."
                    self.orientation = self.NEXT_STAGE
                    # print(message)
                    options = False

                except ValueError as e:
                    self.orientation = self.PROCEED
            
            if not self.orientation or self.orientation == self.PROCEED:
                prompt = await self.prompt()
                chain = prompt | self.llm_conversation
                message = self.chain_invoker(chain=chain, user_input=user_input)
                self.orientation = self.VERIFY_ANSWER
                options = True

        except Exception as e:
            print(f"ResponseHandler: choose_subject() Error {e}")
            
        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage, 'choosed_subject': self.subject}
            if options:
                response['options'] = self.CHOOSE_SUBJECT_STAGE_OPTIONS
            return response
    

    def prompt(self) -> ChatPromptTemplate:
        """
        Chooses the appropriate prompt based on the stage of the conversation.

        Args:
            stage (str): Current stage of the conversation.

        Returns:self.stage
            ChatPromptTemplate: Prompt template.
        """
        prompt = ChatPromptTemplate.from_messages([
                    self.assistant_tone_of_voice(),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                    ("system", "Keep answering the user as the AIAssistant. Use the tone of voice provided."),
                    ("system", "Now, simply use your tone of voice to ask the user the reason for the contact, without greeting again."),
                ])
             
        return prompt