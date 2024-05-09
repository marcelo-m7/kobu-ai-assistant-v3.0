import json
from abc import ABC, abstractmethod
from openai import OpenAI
from datetime import datetime
from .manager_tools import *
from dotenv import load_dotenv
import os

os.environ["OPENAI_API_KEY"] = "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"
load_dotenv()


class LeadExtractor(ABC):
    """Abstract class for extracting lead data from conversation."""
    CLIENT = OpenAI()
    TEMPERATURE = 0.6
    MODEL = "gpt-3.5-turbo"

    def __init__(self, subject_name):
        self.function_description_path = f'assistant/knowledge/{subject_name}/{subject_name}_function_description.json'
        with open(self.function_description_path, 'r', encoding='utf-8') as json_file:
            self.function_description = json.load(json_file)
        
    @abstractmethod
    def get_leads_info(self, chat_history):
        """Abstract method to extract and return lead data."""
        pass
    
    def extract_data(self, chat_history, tool_choice='auto'):
        """Extracts data from chat history using GPT-3."""
        functions_descriptions = self.function_description
        print("Lead Extractor - extract_datas(): Extracting data to generate lead...")

        try:
            completion = self.CLIENT.chat.completions.create(model=self.MODEL, # This model is better for extractions
            response_format={"type": "json_object"},
            temperature=self.TEMPERATURE,
            messages=[
                {'role': 'system', 'content': 'You check whether the conversation contains all the mandatory data for Lead Generation'},
                {'role': 'system', 'content': 'If the conversation contains all the required data for Lead Generation, you extract the data into json from the entire conversation'},
                {'role': 'system', 'content': 'The resume of the user needs you may store in the project_description arguments, if project_description exists.'},
                {'role': 'system', 'content': 'If there is more relevant data, store in the other_data arguments'},
                {"role": "user", "content": f'{chat_history}'}],
            tools=functions_descriptions,
            tool_choice=tool_choice)

            print("Lead Extractor - extract_datas(): Enough data to generate lead")

            output = completion.choices[0].message
            tool_calls = output.tool_calls
            tool_call_arguments = tool_calls[0].function.arguments
            function_arguments = json.loads(tool_call_arguments)

            return function_arguments

        except Exception as e:
            print(f"Error extracting data: {e}")
            return {}
        

class HireUs(LeadExtractor):
    """Extract the datas for lead generation for HIRE_US subject."""
    def __init__(self, subject_name):
        super().__init__(subject_name)

    # @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def get_leads_info(self, chat_history = []) -> json:
        """Extracts and returns the conversation data for Lead Generation."""

        print("HireUS get_leads_info() - Extracting datas to generate lead.")

        try:
            function_arguments = self.extract_data(chat_history)

            person_name = function_arguments['person_name']
            email_address = function_arguments['email_address']
            role_of_person = function_arguments['role_of_person']
            type_of_industry = function_arguments['type_of_industry']
            brand = function_arguments['brand']
            type_of_project = function_arguments['type_of_project']
            available_budget = function_arguments['available_budget']
            how_found_us = function_arguments['how_found_us']
            # timeframe_for_project = function_arguments['timeframe_for_project']

            if 'timeframe_for_project' in function_arguments:
                timeframe_for_project = function_arguments['timeframe_for_project']

            else:
                other_data = ''
            if 'other_data' in function_arguments:
                other_data = function_arguments['other_data']
            else:
                other_data = ''

            if 'project_description' in function_arguments:
                project_description = function_arguments['project_description']
            else:
                project_description = ''

            leads_info = {
                "person_name": person_name,
                "email_address": email_address,
                "role_of_person": role_of_person,
                "type_of_industry": type_of_industry,
                "brand": brand,
                "type_of_project": type_of_project,
                "available_budget": available_budget,
                "timeframe_for_project": timeframe_for_project,
                "how_found_us": how_found_us,
                "project_description": project_description, 
                "other_data": other_data,
                "finish_datetime": str(datetime.now())
            }
            print("Data string for Lead Generation loaded successfully.")

            # print(leads_info)
            lead = json.dumps(leads_info)
            return lead

        except Exception as e:
            print(f"get_leads_info Error {e}")
            return Exception


class GeneralContact(LeadExtractor):
    """Extract the datas for lead generation for self.GENERAL_CONTACT subject."""
    def __init__(self, subject_name):
        super().__init__(subject_name)
    
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def get_leads_info(self, chat_history) -> dict:
        """Extract and return the conversation data for Lead Generation."""
        print("GeneralContact get_leads_info() - Extracting data to generate lead.")

        try:
            function_arguments = self.extract_data(chat_history)
            print(function_arguments)

            # Define default values
            default_values = {
                'other_data': '',
                'how_found_us': '',
                'project_description': '',
                'timeframe_for_project': ''
            }

            # Update default values with extracted data
            for key in default_values:
                if key in function_arguments:
                    default_values[key] = function_arguments[key]

            leads_info = {
                "person_name": function_arguments.get('person_name', ''),
                "email_address": function_arguments.get('email_address', ''),
                "role_of_person": function_arguments.get('role_of_person', ''),
                "brand": function_arguments.get('brand', ''),
                "contact_reason": function_arguments.get('contact_reason', ''),
                "contact_description": function_arguments.get('contact_description', ''),
                "timeframe_for_project": default_values['timeframe_for_project'],
                "how_found_us": default_values['how_found_us'],
                "project_description": default_values['project_description'],
                "other_data": default_values['other_data'],
                "finish_datetime": str(datetime.now())
            }
            print("Data string for Lead Generation loaded successfully.")

            # print(leads_info)
            return json.dumps(leads_info)

        except Exception as e:
            print(f"get_leads_info Error {e}")
            return False


class JoinTheTeam(LeadExtractor):
    """Extract the datas for lead generation for self.JOIN_THE_TEAM subject."""
    def __init__(self, subject_name):
        super().__init__(subject_name)
        
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def get_leads_info(self, chat_history) -> json:
        """Extracts and returns the conversation data for Lead Generation."""
        print("JoinTheTeam get_leads_info() - Extracting datas to generate lead.")

        try:
            function_arguments = self.extract_data(chat_history)

            person_name = function_arguments['person_name']
            email_address = function_arguments['email_address']
            video_url = function_arguments['video_url']
            how_found_us = function_arguments['how_found_us']

            if 'other_data' in function_arguments:
                other_data = function_arguments['other_data']
            else:
                other_data = ''

            leads_info = {
                "person_name": person_name,
                "email_address": email_address,
                "video_url": video_url,
                "how_found_us": how_found_us,
                "other_data": other_data,
                "finish_datetime": str(datetime.now())
            }

            print("Data string for Lead Generation loaded successfully.")

            lead = json.dumps(leads_info)
            return lead

        except Exception as e:
            print(f"get_leads_info Error {e}")
            return ''
        

