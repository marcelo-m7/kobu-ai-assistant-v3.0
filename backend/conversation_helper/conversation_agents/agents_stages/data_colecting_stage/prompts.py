from langchain_core.prompts import ChatPromptTemplate
from ...agents_tools.internal_tools.prompts import Prompts


class DataColectingPrompts(Prompts):
    """
    A class representing the knowledge base for the chat application.
    """

    async def prompt_chooser(self) -> ChatPromptTemplate:
        """
        Chooses the appropriate prompt based on the stage of the conversation.

        Args:
            stage (str): Current stage of the conversation.

        Returns:self.stage
            ChatPromptTemplate: Prompt template.
        """
        if self.subject_name in [self.HIRE_US, self.JOIN_THE_TEAM]:
            prompt = ChatPromptTemplate.from_messages([
                self.assistant_site_context(),
                self.assistant_tone_of_voice(),
                ("system", "{subject_instructions}"),
                ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                ("system", "These are the data riquired: \n{data_required}"),
                ("system", "Note: If a user provide o budget bellow 10.000 EURS, inform the user that KOBU Agency has a minimum engagement level of 10.000EUR and the average project is around 25.000EUR."),
                ("system", "Keep answering the user based on the instructions provided by the system. Do not greeting again. Keep the tone of voice provided."),
                ("system", """"Aproach example:\n
                Before we take flight into the digital stratosphere 🚀, may I implore thee for thy most esteemed name and electronic parchment? 📝 Your moniker and email shall be safeguarded as though they were the crown jewels, ensuring our communication is as seamless as a hot dog at a baseball game! 🌭
                """),
                ("system", "Conversation history: {chat_history}"),
                ("user", "{input}"),
            ])
        else:
            prompt = ChatPromptTemplate.from_messages([
                self.assistant_tone_of_voice('general_tone'),
                ("system", "{subject_instructions}"),
                ("system", "If the user shows interesse in hiring or contacting Kobu Agency, ask for the follow datas to the user. Try to ask one by one:\n{data_required}"),
                ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                ("system", "Keep answering the user based on the instructions provided by the system. Do not greeting again. Use tone of voice provided."),
                self.assistant_site_context(),
                # ("system", "Please, NEVER ASK more of 2 datas in the same massage. Keep the conversation smooth. Start by asking for the name and e-mail."),
                ("system", "Conversation history: {chat_history}"),
                ("user", "{input}"),
            ])

        print("Prompt returned")
        return prompt
