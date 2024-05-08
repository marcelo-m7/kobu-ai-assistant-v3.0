# KOBU AI ASSISTANT

**Documentation Update:**

**Please be advised that the repository documentation is currently being updated to provide more accurate and helpful information. We apologize for any inconvenience this may cause and appreciate your patience. If you have any questions or need further assistance, please don't hesitate to reach out. Thank you for your understanding.**

------------------------------------------------------
The project is a conversational AI chatbot designed to handle various tasks and interactions with users. It utilizes OpenAI's GPT-3.5 model to provide natural language understanding and generation capabilities.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Create a virtual environment and install the required dependencies listed in `requirements.txt`.
3. Start the chatbot by running the `run.py` file inside the `/backend` folder.
4. If the API log shows the Flask server active, you may refresh the frontend chat interface and start the interaction with the AI Assistant through the frontend interface server.
5. To use the local node web-server for the frontend interface, run `npm run start` inside the `/frontend` folder. *(Check out README frontend file in `/frontend/conf/README.md` for better understanding.)*

## Usage

The chatbot is designed to handle various tasks and interactions based on different stages of conversation. Here are some key points to keep in mind:

- **Lead Generation:** If the conversation involves lead generation, the assistant may prompt the user to confirm if all necessary information has been provided. Once it is in a beta version, if the assistant does not provide a resume with the data provided, the users may need to send a message like "it is all" to indicate to the AI that it was completion.
- **Creating New Stages:** To add a new stage to the conversation flow, follow these steps:
  - Define the stage constants in the `ChatConsts` class.
  - Set the stage prompt in the `Knowledge.prompt_chooser()` method.
  - Implement the stage method in the `Assistant` class. If the stage requires data validation, consider creating a validation stage for it.
  - If the stage requires validation of static options, use an index validation.
  - Define the next stage and actions in the `Chat.get_assistant_response()` method.

## Basic Flow of a User Request Until Response

Flow to handle the user request: **`app.py` -> `request_handler.py` -> `chat.py` -> `assistant.py`** [-> `utils.py` -> `knowledge.py` -> `utils.py` -> `assistant.py`]

Flow to return a response: **`assistant.py` -> `chat.py` -> `request_handler.py` -> `app.py`**.

1. **User Request**: The user sends a request to the Flask server through an API call. This request contains information about the user, such as their ID and the message they sent.

2. **RequestHandler**: The Flask server receives the request and passes it to the `RequestHandler`. This is the entry point for processing the user request.

3. **User Validation**: The `RequestHandler` checks if the user who made the request is already active or if they are a new user. If it's a new user, a new instance of the `User` class is created and added to the active users dictionary.

4. **Forwarding to Chat**: After user validation, the request is forwarded to the `Chat` instance associated with the user. Here, the chat processing logic is triggered.

5. **Chat.main() Method Logic**: The `main()` method of the `Chat` object is invoked, where the user's message is processed. In `main()`, the user's message is saved and forwarded to be answered by `get_assistant_response()`.

6. **Assistant Response Retrieval**: Once the user's message is processed, the `get_assistant_response()` function is called. This function may include steps such as determining the current stage of the conversation and validating user data. Additionally, it invokes the corresponding assistant for each based on the conversation stage, user input, and conversation context. This may involve generating text, querying external data sources, or executing specific business logic.

7. **Response from get_assistant_response to main()**: After determining the response, `get_assistant_response()` updates user attributes, returns the response as a dictionary to `main()`, which returns the response to the `RequestHandler`.

8. **Response Forwarded to Client**: The `RequestHandler` receives the response from the `Chat` and sends it back to the client as a JSON response.