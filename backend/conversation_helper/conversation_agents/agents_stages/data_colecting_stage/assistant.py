import json
from .prompts import DataColectingPrompts


class DataColectingResponder(DataColectingPrompts):


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

