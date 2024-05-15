
    async def prompt_chooser(self, stage: str = None) -> ChatPromptTemplate:
        """
        Chooses the appropriate prompt based on the stage of the conversation.

        Args:
            stage (str): Current stage of the conversation.

        Returns:self.stage
            ChatPromptTemplate: Prompt template.
        """
        stage = self.WELCOME_STAGE if None else stage
        
        match stage:
            case ChatConsts.WELCOME_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "{basic_instructions}"),
                    self.assistant_tone_of_voice(),
                    ("system", """Greet the user, thank them for their interest in contacting Kubo, and mention that Nuno has something to share (a video will be displayed to the user just after your message. Use the tone of voice provided.)"""),
                    ("user", "{input}"),
                ])

            case ChatConsts.ACCEPTANCE_OF_TERMS_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    self.assistant_tone_of_voice(),
                    ("system", "Conversation history: {chat_history}"),
                    ("system", "Keep answering the user as the AIAssistant. Use the tone of voice provided."),
                    ("system", "Now, kindly ask the user if they agree to the terms of use, without greeting again."),
                ])


            case ChatConsts.CHOOSE_SUBJECT_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    self.assistant_tone_of_voice(),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                    ("system", "Keep answering the user as the AIAssistant. Use the tone of voice provided."),
                    ("system", "Now, simply use your tone of voice to ask the user the reason for the contact, without greeting again."),
                ])
                
            case ChatConsts.DATA_COLLECTING_STAGE:
                if self.subject_name in [ChatConsts.HIRE_US, ChatConsts.JOIN_THE_TEAM]:
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

            case ChatConsts.DATA_COLLECTING_VALIDATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Check if the user already gave the mandatory datas: {data_required}"),
                    ("system", "If the conversation resume does not contain the mandatory data, return False. If the conversation resume contains the data required for lead generation, you return True."),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                    ])
                
            case ChatConsts.SEND_VALIDATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Conversation history: {chat_history}"),
                    self.assistant_tone_of_voice(),
                    ("system", "Now, simply ask if you can send the contact solicitation to Kobu.")]) 

            case ChatConsts.RESUME_VALIDATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Conversation history: {chat_history}"),
                    self.assistant_tone_of_voice(),
                    ("system", "Now you have to resume the datas provided by the user and ask to the user if the resume is fine. Use the tone of voice provided.")
                    ])
                   
            case ChatConsts.FREE_CONVERSATION_STAGE:
                prompt = ChatPromptTemplate.from_messages([
                    self.assistant_site_context(),
                    ("system", "{basic_instructions}"),
                    self.assistant_tone_of_voice(),
                    ("system", "Keep answering the user based on the instructions provided by the system. Do not greeting again."),
                    ("system", "Conversation history: {chat_history}"),
                    ("user", "{input}"),
                ])

        """ case 'change_subject':  # To be implemented
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Conversation history: {chat_history}"),
                    ("system", "Now ask the user if that would like to change the conversation subject.")])
        """
                    
        print("Prompt returned")
        return prompt
      