import json
from .tools.utils import Utils
import asyncio
from .knowledge.prompts import Prompts


class Assistant(Utils, Prompts):

    async def welcome(self, user_request: dict) -> dict: 
        """Sends a welcome message to the user."""
        print("ResponseHandler: welcome()")
        self.current_stage = self.WELCOME_STAGE

        try:
            # user_input = 'Hi, there!'    # user_request.get('user_input')
            user_input = user_request.get('user_input')
            prompt = await self.prompt_chooser(stage=self.current_stage)
            chain = prompt | self.llm_conversation
            message = self.chain_invoker(chain=chain, user_input=user_input)
            self.orientation = self.NEXT_STAGE

            # print("Messase in welcome(): ", message)

        except Exception as e:
            print(f"ResponseHandler: welcome() Error {e}")

        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage}
            return response

    async def acceptance_of_terms(self, user_request: dict) -> dict:
        """[TO BE IMPLEMENTED] Sends the subjects to the user to be choosed."""
        print("ResponseHandler: acceptance_of_terms()")
        self.current_stage = self.ACCEPTANCE_OF_TERMS_STAGE

        try:
            user_input = user_request.get('user_input')
            if self.orientation == self.VERIFY_ANSWER:  # In case the user already choosed a subject
                try:
                    option_choosed = self.ACCEPTANCE_OF_TERMS_STAGE_OPTIONS.index(user_input)
                    if option_choosed == 0:
                        message = 'true'
                    elif option_choosed == 1:
                        message = 'false'

                    print(f"User answer for terms acc: {option_choosed}.")
                    self.orientation = self.NEXT_STAGE
                    options = False

                except ValueError as e:
                    self.orientation = self.PROCEED
            
            if not self.orientation or self.orientation == self.PROCEED:
                prompt = await self.prompt_chooser(stage=self.current_stage)
                chain = prompt | self.llm_conversation
                message = self.chain_invoker(chain=chain, user_input=user_input)
                self.orientation = self.VERIFY_ANSWER
                options = True

        except Exception as e:
            print(f"ResponseHandler: choose_subject() Error {e}")
            
        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage, 'choosed_subject': self.subject}
            if options:
                response['options'] = self.ACCEPTANCE_OF_TERMS_STAGE_OPTIONS
            return response
        
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
                prompt = await self.prompt_chooser(stage=self.current_stage)
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

    async def data_colecting_validation(self, user_request: dict) -> dict:
        """Check if all the datas has been provided by the user"""
        print("ResponseHandler: data_colecting_validation()")
        self.current_stage = self.DATA_COLLECTING_STAGE 

        while True:        
            try:
                user_input = user_request.get('user_input')
                status = 'false'

                # 1str: Check whether the necessary data for Lead Generation has been provided during the conversation
                prompt = await self.prompt_chooser(stage=self.DATA_COLLECTING_VALIDATION_STAGE)
                chain = prompt | self.llm_validation

                status = str(self.chain_invoker(chain=chain, user_input=user_input).lower().strip(" "))

                print("data_colecting_validation() status recibed: ", status)

                # If has been provided (True), try to extract the datas.
                if 'true' in status:
                    print("data_colecting_validation() TRUE")
                    self.lead = self.subject_instance.get_leads_info(self.chat_history)
                    lead = json.loads(self.lead)
                    print("Lead sucessfull extracted") # :\n", lead)

                    # 2nd: Check ff the datas has been sucessfull extracted and has no empty value
                    try:
                        lead.pop("other_data", None)
                        lead.pop("project_description", None)
                    finally:
                        print("other_data and project_description pop()")
                        lead = str(str(lead).strip('{').strip('}').strip(']').strip(']')).lower()
                        print("strip ok")
                        # print("lead string", lead)
                        
                        if 'not provided' in lead or 'not specified' in lead:
                            message = 'The lead are not compleated.'
                            status = 'false'
                            self.orientation = self.PROCEED
                        
                        else:
                            # If necessary, second checker if there is any data that was not provided.
                            # If the leads are ok, set 'true' message to the response
                            message = 'Lead well compleated.'
                            status = 'true'
                            self.orientation = self.NEXT_STAGE

                else:    # if status == 'false':
                    # If the leads are not ok, set 'false' message to the response
                    message = 'The lead are not compleated.'
                    self.orientation = self.PROCEED


            except Exception as e:
                print(f"ResponseHandler: data_colecting_validation() Error {e}")

            finally:
                response = {"message": message, "current_stage": self.current_stage, 'orientation': self.orientation}
                # print(message)
                return response
        
    async def data_colecting(self, user_request: dict) -> dict:
        """Send a welcome message to the user"""
        print("ResponseHandler: data_colecting()")
        self.current_stage = self.DATA_COLLECTING_STAGE 

        try:
            user_input = user_request.get('user_input')
            chain = await self.chain_builder(self.DATA_COLLECTING_STAGE)
            message = self.chain_invoker(chain=chain, user_input=user_input)
            self.orientation = self.PROCEED

        except Exception as e:
            print(f"ResponseHandler: data_colecting() Error {e}")

        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.DATA_COLLECTING_STAGE}
            return response
       
    async def data_colecting_in_changing(self, user_request: dict) -> dict:
        """[Methodol beeing refactorated] Send a welcome message to the user"""
        print("ResponseHandler:  data_colecting_in_changing()")
        self.current_stage = self.DATA_COLLECTING_STAGE 

        try:
            retriver_chain = await asyncio.create_task(self.retriver_chain_extra_context())

            user_input = user_request.get('user_input')

            retriver_extra_context = await asyncio.create_task(self.retriever_chain_invoker(
                retriver_chain, 
                {'input': user_input, 
                 'chat_history': self.chat_history}))
            
            print("retriver_extra_context: \n", retriver_extra_context)

            prompt = self.prompt_chooser(self.DATA_COLLECTING_STAGE)
            chain = prompt | self.llm_conversation
            message = await self.chain_invoker(chain=chain, user_input=user_input, extra_context=retriver_extra_context)
            self.orientation = self.PROCEED

            print("message agter retriver_extra_context: \n", message)


        except Exception as e:
            print(f"ResponseHandler: data_colecting() Error {e}")

        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.DATA_COLLECTING_STAGE}
            return response

    async def resume_validation(self, user_request: dict) -> dict:
        """Ask the user if the contact resume are ok"""
        self.current_stage = self.RESUME_VALIDATION_STAGE
        print("ResponseHandler: resume_validation()")

        try:
            user_input = user_request.get('user_input')

            if self.orientation == self.VERIFY_ANSWER: # It may be improved
                try:
                    message = self.RESUME_VALIDATION_STAGE_OPTIONS.index(user_input)
                    if message == 0:
                        message = 'true'
                        self.orientation = self.NEXT_STAGE
                    else:
                        message = 'false'
                        self.orientation = self.VERIFY_ANSWER
                except ValueError:
                    self.orientation = self.PROCEED
                
            if self.orientation == '' or self.orientation == self.PROCEED:
                prompt = await self.prompt_chooser(stage=self.current_stage)
                chain = prompt | self.llm_conversation
                message = self.chain_invoker(chain=chain)
                self.orientation = self.VERIFY_ANSWER
                # options = True

        except Exception as e:
            print(f"ResponseHandler: resume_validation() Error {e}")

        finally:
            # print(message)
            response = {"message": message, 'options': self.RESUME_VALIDATION_STAGE_OPTIONS, 'orientation': self.orientation, "current_stage": self.current_stage}
            return response

    async def send_validation(self, user_request: dict) -> dict:
        """Ask the user if the assistant can send the contact solicitation"""
        self.current_stage = self.SEND_VALIDATION_STAGE
        print("ResponseHandler: send_validation()")
        # options  = None

        try:
            user_input = user_request.get('user_input')
            if self.orientation == self.VERIFY_ANSWER: # It may be improved
                try:                
                    message = self.SEND_VALIDATION_STAGE_OPTIONS.index(user_input)
                    if message == 0:
                        message = 'true'
                        self.orientation = self.NEXT_STAGE
                    else:
                        message = 'false'
                        self.orientation = self.VERIFY_ANSWER
                    # options = False
                        
                except ValueError:
                    self.orientation = self.PROCEED

            if self.orientation == '' or self.orientation == self.PROCEED:
                prompt = await self.prompt_chooser(stage=self.current_stage)
                chain = prompt | self.llm_conversation
                message = self.chain_invoker(chain=chain)
                self.orientation = self.VERIFY_ANSWER
                # options = True

        except Exception as e:
            print(f"ResponseHandler: send_validation() Error {e}")

        finally:
            response = {"message": message, 'options': self.SEND_VALIDATION_STAGE_OPTIONS, 'orientation': self.orientation, "current_stage": self.current_stage}
            # if options:
            return response

    async def free_conversation(self, user_request: dict) -> dict:
        self.current_stage = self.FREE_CONVERSATION_STAGE
        print("ResponseHandler: free_conversation()")

        try:
            user_input = user_request.get('user_input')
            if self.orientation == '' or self.orientation == self.PROCEED or self.orientation == self.NEXT_STAGE:
                chain = await self.chain_builder(stage=self.current_stage)
                message = self.chain_invoker(chain=chain, user_input=user_input)
                self.orientation = self.PROCEED

            else:   # To be implementing: subject changer
                options = ["No, it is fine.", "Actually, I do."]

                if user_input not in options:
                    prompt = await self.prompt_chooser(stage='change_subject')
                    chain = prompt | self.llm_conversation
                    message = self.chain_invoker(chain=chain, user_input=user_input)
                    self.orientation = self.VERIFY_ANSWER

                else: # if self.orientation == 'verify':
                        message = options.index(user_input)
                        if message == 0:
                            message = 'false'
                        else:
                            message = 'true'
                        self.orientation = self.PROCEED  
        except Exception as e:
            print(f"ResponseHandler: free_conversation() Error {e}")

        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage}
            return response
    
    # To be implemented
    async def critical(self, user_request: dict) -> dict: 
        """[METHODOL IN TESTE] Response with the basic prompt message to the user."""
        print("ResponseHandler: welcome()")
        self.current_stage = self.CRITICAL

        try:
            user_input = user_request.get('user_input')
            prompt = await self.prompt_chooser(stage=self.current_stage)
            chain = prompt | self.llm_conversation
            message = self.chain_invoker(chain=chain, user_input=user_input)
            self.orientation = self.NEXT_STAGE

        except Exception as e:
            print(f"ResponseHandler: welcome() Error {e}")

        finally:
            response = {"message": message, 'orientation': self.orientation, 'current_stage': self.current_stage}
            return response
