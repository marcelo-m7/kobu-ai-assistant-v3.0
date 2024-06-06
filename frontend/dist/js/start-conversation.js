import { Conversation } from './conversation.js';


export class StartConversation {
  constructor() {
    this.userId = Conversation.generateUserId();
    this.conversation = new Conversation(this.userId);

    // Interface HTML Elements
    const chatboxWrapper = document.getElementById("chatbox-wrapper");
      const chatboxOpenButton = document.getElementById("chatbox-open-button");
      const chatboxContainer = document.getElementById("chatbox-container");
      const chatboxCloseButton = document.getElementById("chatbox-close-button");

    // When clicking on the open chat button
    chatboxOpenButton.addEventListener("click", async () => {
      chatboxCloseButton.classList.remove("status-closed")
      chatboxContainer.classList.remove("status-closed")
      chatboxWrapper.classList.remove("status-closed")
      await this.conversation.openChat(this.main.bind(this));
    });
    // When clicking on the close chat button
    chatboxCloseButton.addEventListener("click", async () => {
      chatboxCloseButton.classList.add("status-closed")
      chatboxContainer.classList.add("status-closed")
      chatboxWrapper.classList.add("status-closed")
    });
    // When clicking on the send chat icon
    document.getElementById("send-icon").addEventListener('click', async (e) => {
      e.preventDefault();
      var optionText = this.conversation.userInput() 
      if (!optionText) {
          return false;
      }
        await this.conversation.openChat(this.main());
    });
    // When presssing 'Enter' key
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
    switch (this.conversation.currentStage) {

      case undefined:
      case '':
      case null:
      case this.conversation.WELCOME_STAGE:
        console.log("Main: starts welcomeMessage()");
        this.conversation.showSpinner();
        inputElement.placeholder = '';
        this.conversation.currentStage = this.conversation.WELCOME_STAGE; // First interaction with the API

        var request = this.conversation.requestData("Hi, there!");
        var response = await this.conversation.sendRequest(request);
        await this.conversation.assistantResponseHandler(response);
        if (response.current_stage === 'error') {
          break;
        }
        await this.conversation.setVideo();
        this.conversation.currentStage = this.conversation.CHOOSE_SUBJECT_STAGE;
        console.log("Main: finish welcomeMessage() ", this.conversation.currentStage);
        if (response.orientation === false) {
          break;
        }

      case this.conversation.CHOOSE_SUBJECT_STAGE:
        console.log("Main: starts chooseSubject()");
        inputElement.placeholder = '';
        this.conversation.showSpinner();
        this.conversation.currentStage = this.conversation.CHOOSE_SUBJECT_STAGE; // Ask for the subejects list
        
        var request = this.conversation.requestData() // input="Choose subject stage")
        inputElement.value = '';
        inputElement.placeholder = '';
        var response = await this.conversation.sendRequest(request);

        if (response.message === false) {
          inputElement.placeholder = 'Please, choose a option.'
          
          break;
        }
        await this.conversation.assistantResponseHandler(response); 
        inputElement.placeholder = 'Type a message'

        break;
      
      // It is missing to add a case to send the history or div state to the API, to send the conversation settings and history by client side
      default:
        this.conversation.showSpinner();
        this.conversation.setUserResponse()
        var request = this.conversation.requestData()
        inputElement.value = '';
        inputElement.placeholder = '';
        
        var response = await this.conversation.sendRequest(request);

        if (response.message === false) {
          break;
        }
        await this.conversation.assistantResponseHandler(response);
        inputElement.placeholder = 'Type a message';
        console.log("Main: finish default() ", this.conversation.currentStage); 

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
