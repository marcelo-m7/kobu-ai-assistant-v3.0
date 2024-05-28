import { Conversation } from './conversation.js';

export class StartConversation {
  constructor() {
    // Constants
    this.userId = Conversation.generateUserId();
    this.userChat = new Conversation(this.userId);
    const chatboxOpenButton = document.getElementById("chatbox-open-button");
    const chatboxCloseButton = document.getElementById("chatbox-close-button");
    const chatboxContainer = document.getElementById("chatbox-container");

    // Listeners
    chatboxOpenButton.addEventListener("click", async () => {
      chatboxContainer.style.opacity = 1;
      chatboxCloseButton.style.opacity = 1;
      chatboxOpenButton.style.opacity = 1;
      await this.userChat.openChat(this.main.bind(this));
    });
    chatboxCloseButton.addEventListener("click", async () => {
      chatboxContainer.style.opacity = 0;
      chatboxCloseButton.style.opacity = 0;
      chatboxOpenButton.style.opacity = 1;
    });
    document.getElementById("send-icon").addEventListener('click', async (e) => {
      e.preventDefault();
      var optionText = this.userChat.userInput() 
      if (!optionText) { // Verifica se a string está vazia após o trim
          return false;
      }
        await this.userChat.openChat(this.main());
    });
    document.getElementById("user-input-container").addEventListener('keyup', async (e) => {
      await this.enterClick(e);
    });
    document.getElementById("user-input-container").addEventListener('keypress', async (e) => {
      await this.enterClick(e);
    });
  }

  /**
   * Main function for managing the chat interface and interaction with the AI assistant.
   * Sets up event listeners for opening and closing the chat, handling user input, and executing the conversation logic.
   * @returns {Promise<void>} - A promise that resolves once the main function completes.
   */
  async main() {
    const inputElement = document.getElementById('user-input');
    const userChatActive = this.userChat; // Fixing the scope issue

    switch (userChatActive.currentStage) {

      case undefined:
      case '':
      case null:
      case userChatActive.WELCOME_STAGE:
        console.log("Main: starts welcomeMessage()");
        userChatActive.showSpinner();
        inputElement.placeholder = '';
        userChatActive.currentStage = userChatActive.WELCOME_STAGE; // First interaction with the API

        var request = userChatActive.requestData("Hi, there!");
        var response = await userChatActive.sendRequest(request);
        await userChatActive.assistantResponseHandler(response);
        if (response.current_stage === 'error') {
          break;
        }
        await userChatActive.setVideo();
        userChatActive.currentStage = userChatActive.CHOOSE_SUBJECT_STAGE;
        console.log("Main: finish welcomeMessage() ", userChatActive.currentStage);
        if (response.orientation === false) {
          break;
        }

      case userChatActive.CHOOSE_SUBJECT_STAGE:
        console.log("Main: starts chooseSubject()");
        inputElement.placeholder = '';
        userChatActive.showSpinner();
        userChatActive.currentStage = userChatActive.CHOOSE_SUBJECT_STAGE; // Ask for the subejects list
        
        var request = userChatActive.requestData() // input="Choose subject stage")
        inputElement.value = '';
        inputElement.placeholder = '';
        var response = await userChatActive.sendRequest(request);

        if (response.message === false) {
          inputElement.placeholder = 'Please, choose a option.'
          
          break;
        }
        await userChatActive.assistantResponseHandler(response); 
        inputElement.placeholder = 'Type a message'

        break;
        
      default:
        userChatActive.showSpinner();
        userChatActive.setUserResponse()

        var request = userChatActive.requestData()
        inputElement.value = '';
        inputElement.placeholder = '';
        
        var response = await userChatActive.sendRequest(request);

        if (response.message === false) {
          break;
        }
        
        await userChatActive.assistantResponseHandler(response);
        inputElement.placeholder = 'Type a message';
        console.log("Main: finish default() ", userChatActive.currentStage); 

        break;

    }
  }

  /**
   * Handles user responses triggered by pressing the Enter key.
   * @param {Event} e - The event object representing the keypress event.
   * @returns {Promise<boolean>} - A promise that resolves to true if the Enter key is pressed and the user input is not empty or consists only of whitespace; otherwise, resolves to false.
   */
  async enterClick(e) {
    var keyCode = e.keyCode || e.which;
    var text = document.getElementById("user-input").value;

    if (keyCode === 13) {
      if (text == "" || text.trim() == "") {
        e.preventDefault();
        return false;
      } else {
        e.preventDefault();
        document.getElementById("user-input").blur();
        await this.main();
      }
    }
  }
}
