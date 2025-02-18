# KOBU AI ASSISTANT


The project is a conversational AI chatbot designed to handle various tasks and interactions with users. It utilizes OpenAI's GPT-3.5 model to provide natural language understanding and generation capabilities.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Create a virtual environment and install the required dependencies listed in `requirements.txt`.
3. If the API is hosted on an online server, uncomment the indicated line in `backend\run_api-ai-assistant.py` before running the API. If the host is not set to '0.0.0.0', the API will not listen to external traffic. 

    ```python
    if __name__ == '__main__':
        app.run(debug=True)
        # app.run(debug=False, host='0.0.0.0') # To run on an online server
    ```

4. Create a `.env` file in the root directory of the project and add the following content:

    ```
    OPENAI_API_KEY=your_api_key_here
    ```

    Replace `your_api_key_here` with your actual OpenAI API key.

5. Ensure that the `python-dotenv` package is installed in your virtual environment.
6. The function from the `dotenv` module is setted on the script to automatically load environment variables from the `.env` file.

    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```

7. Start the chatbot by running the file `run_api-ai-assistant.py` inside the `/backend` folder.
8. If the API log shows the Flask server as active, you can refresh the frontend chat interface and start interacting with the AI Assistant through the frontend interface server.
9. To use the local Node web-server for the frontend interface, run `npm run start` inside the `/frontend` folder. *(Refer to the README file in `/frontend/conf/README.md` for a better understanding.)*

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

Flow to handle the user request: **`app.py` -> `request_handler.py` -> `conversation.py` -> `assistant.py`** [-> `utils.py` -> `knowledge.py` -> `utils.py` -> `assistant.py`]

Flow to return a response: **`assistant.py` -> `conversation.py` -> `request_handler.py` -> `app.py`**.

1. **User Request**: The user sends a request to the Flask server through an API call. This request contains information about the user, such as their ID and the message they sent.

2. **Request Handler**: The Flask server receives the request and passes it to the `RequestHandler`. This is the entry point for processing the user request.

3. **User Validation**: The `RequestHandler` checks if the user who made the request is already active or if they are a new user. If it's a new user, a new instance of the `User` class is created and added to the active users dictionary.

4. **Forwarding to Chat**: After user validation, the request is forwarded to the `Conversation ` instance associated with the user. Here, the Conversation  processing logic is triggered.

5. **Conversation .main() Method Logic**: The `main()` method of the `Conversation ` object is invoked, where the user's message is processed. In `main()`, the user's message is saved and forwarded to be answered by `get_assistant_response()`.

6. **Assistant Response Retrieval**: Once the user's message is processed, the `get_assistant_response()` function is called. This function may include steps such as determining the current stage of the conversation and validating user data. Additionally, it invokes the corresponding assistant for each based on the conversation stage, user input, and conversation context. This may involve generating text, querying external data sources, or executing specific business logic.

7. **Response from get_assistant_response to main()**: After determining the response, `get_assistant_response()` updates user attributes, returns the response as a dictionary to `main()`, which returns the response to the `RequestHandler`.

8. **Response Forwarded to Client**: The `RequestHandler` receives the response from the `Conversation ` and sends it back to the client as a JSON response.