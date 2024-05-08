# KOBU AI ASSISTANT

The project is a conversational AI chatbot designed to handle various tasks and interactions with users. It utilizes OpenAI's GPT-3.5 model to provide natural language understanding and generation capabilities.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Create a virtual environment and install the required dependencies listed in `requirements.txt`.
3. Set up the frontend files `frontend` on your preferred frontend server *(Check out point 8 of this section)*. Verify if the chat interface is being displayed on your frontend web server.

4. If your web server is in a local environment (localhost), you may need to use a proxy or ensure that your server will not block the API request. *(Check out the section **Frontend Integration: Modifications Required** below for a better understanding of how to deal with cross-origin security issues.)*.
6. Start the chatbot by running the `run.py` file inside the `/backend` folder. *(You can find more backend documentation in the README.md file in `/backend/conf/README.md` for better understanding.)*

7. If the API log shows the Flask server active, you may refresh the frontend chat interface and start the interaction with the AI Assistant through the frontend interface server.

8. To use the local node web-server for the frontend interface, run `npm run start` inside the `/frontend` folder. *(Check out the README.md frontend file in `/frontend/conf/README.md` for better understanding.)*

## Frontend Integration

This project incorporates a frontend interface for engaging with the chatbot, hosted on its own server. Here's how you can integrate the frontend with the backend project:

1. **Using the Provided Frontend Server:**
   - If you opt to utilize the provided node-server as the frontend web server, simply follow the instructions provided in the README.md file from the `frontend/conf/` directory.

2. **Manual Integration:**
   - You can manually integrate the frontend into your existing server by copying the files from the `frontend/public` directory to your frontend server. *(Check out the section **Cross-Origin Deal** in the README.md frontend file in `/frontend/conf/README.md` to adjust the default request URL according to your needs.)*

3. **Modifications Required:**
   - No changes are necessary within the API application, as the server is already configured to accommodate external traffic.
   - However, for the frontend integration, you may need to review the comments within the `Conversation.sendRequest()` method in `js/conversation.js`. This is to adjust the configuration of the frontend-backend communication, particularly regarding cross-origin resource sharing (CORS) settings, if needed. This streamlined integration process ensures seamless communication between your frontend and backend components.