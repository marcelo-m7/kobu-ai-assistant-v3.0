from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
from Consts import Paths as p
load_dotenv()


class Lead:
    """Classe representando um lead extraído."""
    def __init__(self, **kwargs):
        self.data = kwargs
        self.data["finish_datetime"] = str(datetime.now())

    def to_dict(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data)


class LeadExtractor:
    """Classe genérica para extração de leads."""
    CLIENT = OpenAI()
    TEMPERATURE = 0.6
    MODEL = "gpt-3.5-turbo"

    def __init__(self, subject_name):
        self.subject_name = subject_name
        self.function_description_path = p.FUNCTION_DESCRIPTION_PATH.format(subject_name=self.subject_name)
        with open(self.function_description_path, 'r', encoding='utf-8') as json_file:
            self.function_description = json.load(json_file)

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def extract_lead(self, conversation_history, tool_choice='auto') -> Lead:
        """Extrai dados da conversa e retorna uma instância de Lead."""
        try:
            completion = self.CLIENT.chat.completions.create(
                model=self.MODEL,
                response_format={"type": "json_object"},
                temperature=self.TEMPERATURE,
                messages=[
                    {'role': 'system', 'content': 'Extract lead data from the conversation.'},
                    {"role": "user", "content": conversation_history}
                ],
                tools=self.function_description,
                tool_choice=tool_choice
            )
            
            output = completion.choices[0].message
            tool_call_arguments = output.tool_calls[0].function.arguments
            extracted_data = json.loads(tool_call_arguments)
            
            return Lead(**extracted_data)
        except Exception as e:
            print(f"Erro na extração de dados: {e}")
            return Lead()
