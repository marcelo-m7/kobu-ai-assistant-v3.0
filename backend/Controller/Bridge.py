from backend.Model.kobu_assistant.kobu_assistant_controller import User, Conversation, ConversationEnviroment
import json


model = Conversation()
actived_conversations = {}


def conversation_builder(user_id: int, user_request: json) -> ConversationEnviroment:
    user = User(user_id=user_id, user_request=user_request)
    cv = ConversationEnviroment(user_instance=user)
    return cv

def assistant_response_formater(cv: ConversationEnviroment) -> json:
    conversation = cv.__dict__
    attributes = {
        key: valor for key, valor in vars(conversation.__class__).items()
        if not callable(valor) and not key.startswith('__')
    }
    assistant_response = {**attributes, **conversation}
    return json.dumps(assistant_response, indent=4)

def interface_controller(user_request: json) -> json:
    user_id: int = user_request.get('user_id')

    if user_id in actived_conversations:
        cv = actived_conversations[user_id]
    else:
        cv = conversation_builder(user_id=user_id, user_request=user_request)

    model_response = model.controller(cv=cv)
    model_request_response = assistant_response_formater(model_response)
    return model_request_response


