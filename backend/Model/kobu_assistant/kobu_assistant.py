from .core.base_assistant import *
from backend.Model.kobu_assistant.core.consts import ChatConsts as c
import json


class KobuAssistant(BaseAssistant):

    async def welcome_stage(self, cv: ConversationEnviroment) -> ConversationEnviroment: 
        """Assistant that sends a welcome message to the user."""
        print("Assistant: welcome()")
        
        if cv.assistant_reponse_orientation == c.STAGE_FINISHED:
            cv.current_conversation_orientation = c.STAGE_FINISHED
        else:
            cv.assistant_response_message = self.obtain_assistant_message_response(cv=cv)
            cv.current_conversation_orientation = c.RESPONSE_READY
            cv.assistant_reponse_orientation = c.STAGE_FINISHED
        
        return cv

    async def choose_subject_stage(self, cv: ConversationEnviroment) -> ConversationEnviroment: 
        """Assistant that sends the subjects to the user to be choosed."""
        print("Assistant: choose_subject()")

        if cv.assistant_reponse_orientation == c.STAGE_FINISHED:
            cv.current_conversation_orientation = c.STAGE_FINISHED
            cv.assistant_reponse_orientation = c.PROCEED

        elif cv.assistant_reponse_orientation == c.VERIFY_ANSWER:
            cv.conversation_subject = c.CHOOSE_SUBJECT_STAGE_OPTIONS.index(cv.user_input)
            cv.conversation_options_flag = False
            cv.current_conversation_orientation = c.STAGE_FINISHED
            cv.assistant_reponse_orientation = c.PROCEED

        else:   # elif cv.assistant_reponse_orientation == c.PROCEED:
            cv.assistant_response_message = self.obtain_assistant_message_response(cv=cv)
            cv.conversation_options = c.CHOOSE_SUBJECT_STAGE_OPTIONS
            cv.conversation_options_flag = True

            cv.current_conversation_orientation = c.RESPONSE_READY
            cv.assistant_reponse_orientation = c.VERIFY_ANSWER
        
        return cv
    
    async def data_colecting_stage(self, cv: ConversationEnviroment) -> ConversationEnviroment:
        """Send a welcome message to the user"""
        print("Assistant: data_colecting()")

        flag = self._data_colecting_stage_validator(cv=cv)
        
        if flag:
            cv.current_conversation_orientation = c.STAGE_FINISHED
            cv.assistant_reponse_orientation = c.PROCEED

        else:
            cv.assistant_response_message = self.obtain_assistant_message_response(cv=cv)
            cv.assistant_reponse_orientation = c.PROCEED
            cv.current_conversation_orientation == c.RESPONSE_READY

        return cv

    async def _data_colecting_stage_validator(self, cv: ConversationEnviroment) -> ConversationEnviroment: 
        """Assistant that verifys if all the datas has been provided by the user. It does not answers the user_input."""
        print("Assistant: data_colecting_validation()")

        while True:        
            # 1str: Check whether the necessary data for Lead Generation has been provided during the conversation
            status = self.obtain_assistant_message_response(cv=cv)
            # print("data_colecting_validation() status recibed: ", status)

            # If has been provided (True), try to extract the datas.
            if 'true' in status:
                lead = c.subject_instance.get_leads_info(c)
                lead_json = lead = json.loads(lead)
                print("Lead sucessfull extracted") # :\n", lead)

                # 2nd: Check if the datas has been sucessfull extracted and has no empty value
                try:
                    lead.pop("other_data", None)
                    lead.pop("project_description", None)
                finally:
                    lead = str(str(lead).strip('{').strip('}').strip(']').strip(']')).lower()
                    
                    if 'not provided' in lead or 'not specified' in lead:
                        message = 'The lead are not compleated.'
                        status = 'false'
                        self.orientation = self.PROCEED

                    else:
                        # 3nd: Check if any datas is empty
                        try:
                            def is_lead_valid(lead: dict) -> bool:
                                exceptions = {"other_data", "project_description"}
                                
                                for key, value in lead.items():
                                    if key not in exceptions and value == "":
                                        return False
                                return True
                            
                            status = is_lead_valid(lead_json)

                            if status == True:
                                status = 'true'
                            else:
                                status = 'false'
                            # print("is_lead_valid status: ", status)

                        except Exception as e:
                            print(f"data_colecting_validation() is_lead_valid(): Error {e}")
                    
                    if status != 'true':
                        return False

                    else:
                        # If necessary, second checker if there is any data that was not provided.
                        # If the leads are ok, set 'true' message to the response
                        cv.lead = lead_json
                        return True


    # async def resume_validation(self, user_request: dict) -> dict:
    #     """Assistant that asks the user if the contact resume provided is ok."""
    #     self.current_stage = self.RESUME_VALIDATION_STAGE
    #     print("Assistant: resume_validation()")

    #     try:
    #         user_input = user_request.get('user_input')

    #         if self.orientation == self.VERIFY_ANSWER: # It may be improved
    #             try:
    #                 message = self.RESUME_VALIDATION_STAGE_OPTIONS.index(user_input)
    #                 if message == 0:
    #                     message = 'true'
    #                     self.orientation = self.NEXT_STAGE
    #                 else:
    #                     message = 'false'
    #                     self.orientation = self.VERIFY_ANSWER
    #             except ValueError:
    #                 self.orientation = self.PROCEED
                
    #         if self.orientation == '' or self.orientation == self.PROCEED:
    #             prompt = await self.prompt_chooser(stage=self.current_stage)
    #             chain = prompt | self.llm_conversation
    #             message = self.chain_invoker(chain=chain)
    #             self.orientation = self.VERIFY_ANSWER
    #             # options = True

    #     except Exception as e:
    #         print(f"Assistant: resume_validation() Error {e}")

    #     finally:
    #         # print(message)
    #         response = {"message": message, 'options': self.RESUME_VALIDATION_STAGE_OPTIONS, 'orientation': self.orientation, "current_stage": self.current_stage}
    #         return response

    # async def send_validation(self, user_request: dict) -> dict:
    #     """Assistant that asks the user if the assistant can send the contact solicitation"""
    #     self.current_stage = self.SEND_VALIDATION_STAGE
    #     print("Assistant: send_validation()")
    #     # options  = None

    #     try:
    #         user_input = user_request.get('user_input')
    #         if self.orientation == self.VERIFY_ANSWER: # It may be improved
    #             try:                
    #                 message = self.SEND_VALIDATION_STAGE_OPTIONS.index(user_input)
    #                 if message == 0:
    #                     message = 'true'
    #                     self.orientation = self.NEXT_STAGE
    #                 else:
    #                     message = 'false'
    #                     self.orientation = self.VERIFY_ANSWER
    #                 # options = False
                        
    #             except ValueError:
    #                 self.orientation = self.PROCEED

    #         if self.orientation == '' or self.orientation == self.PROCEED:
    #             prompt = await self.prompt_chooser(stage=self.current_stage)
    #             chain = prompt | self.llm_conversation
    #             message = self.chain_invoker(chain=chain)
    #             self.orientation = self.VERIFY_ANSWER
    #             # options = True

    #     except Exception as e:
    #         print(f"Assistant: send_validation() Error {e}")

    #     finally:
    #         response = {"message": message, 'options': self.SEND_VALIDATION_STAGE_OPTIONS, 'orientation': self.orientation, "current_stage": self.current_stage}
    #         # if options:
    #         return response

    # async def free_conversation(self, user_request: dict) -> dict:
    #     """Assistant that keeps the conversation after lead genereted."""
    #     self.current_stage = self.FREE_CONVERSATION_STAGE
    #     print("Assistant: free_conversation()")

    #     try:
    #         user_input = user_request.get('user_input')
    #         if self.orientation == '' or self.orientation == self.PROCEED or self.orientation == self.NEXT_STAGE:
    #             chain = await self.chain_builder(stage=self.current_stage)
    #             message = self.chain_invoker(chain=chain, user_input=user_input)
    #             self.orientation = self.PROCEED

    #         else:   # To be implementing: subject changer
    #             options = ["No, it is fine.", "Actually, I do."]

    #             if user_input not in options:
    #                 prompt = await self.prompt_chooser(stage='change_subject')
    #                 chain = prompt | self.llm_conversation
    #                 message = self.chain_invoker(chain=chain, user_input=user_input)
    #                 self.orientation = self.VERIFY_ANSWER

    #             else: # if self.orientation == 'verify':
    #                     message = options.index(user_input)
    #                     if message == 0:
    #                         message = 'false'
    #                     else:
    #                         message = 'true'
    #                     self.orientation = self.PROCEED  
    #     except Exception as e:
    #         print(f"Assistant: free_conversation() Error {e}")

    #     finally:
    #         response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage}
    #         return response
    
    # # To be implemented
    # async def critical(self, user_request: dict) -> dict: 
    #     """[METHODOL IN TESTE] Response with the basic prompt message to the user."""
    #     print("Assistant: welcome()")
    #     self.current_stage = self.CRITICAL

    #     try:
    #         user_input = user_request.get('user_input')
    #         prompt = await self.prompt_chooser(stage=self.current_stage)
    #         chain = prompt | self.llm_conversation
    #         message = self.chain_invoker(chain=chain, user_input=user_input)
    #         self.orientation = self.NEXT_STAGE

    #     except Exception as e:
    #         print(f"Assistant: welcome() Error {e}")

    #     finally:
    #         response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage}
    #         return response
