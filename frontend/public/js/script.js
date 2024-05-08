import { Conversation } from './conversation.js';

// Consts
const userId = Conversation.generateUserId();
const userChat = new Conversation(userId);

// Listinners
document.querySelector(".profile_div").addEventListener('click', async () => {
  await userChat.openChat(main);
});
document.getElementById("closeButton").addEventListener('click', async () => {
  await userChat.closeChat();
});
document.getElementById("chat-input").addEventListener('keyup', async (e) => {
  await enterClick(e);
});
document.getElementById("chat-input").addEventListener('keypress', async (e) => {
  await enterClick(e);
});


/**
 * Main function for managing the chat interface and interaction with the AI assistant.
 * Sets up event listeners for opening and closing the chat, handling user input, and executing the conversation logic.
 * @returns {Promise<void>} - A promise that resolves once the main function completes.
 */
async function main() {
  const inputElement = document.getElementById('chat-input');

  switch (userChat.currentStage) {
    
    case undefined:
    case '':
    case null:
    case userChat.WELCOME_STAGE:
      console.log("Main: starts welcomeMessage()");
      userChat.showSpinner();
      inputElement.placeholder = '';

      userChat.currentStage = userChat.WELCOME_STAGE; // First interaction with the API
      
      var request = userChat.requestData("Hi, there!");
      var response = await userChat.sendRequest(request);
      
      await userChat.assistantResponseHandler(response);
      await userChat.setVideo();

      userChat.currentStage = userChat.CHOOSE_SUBJECT_STAGE;
      console.log("Main: finish welcomeMessage() ", userChat.currentStage);
      
      if (response.orientation !== userChat.NEXT_STAGE) {
        break
      }

      inputElement.blur()
      inputElement.placeholder = '';
      
    default:
      console.log("Main: start default()");
      userChat.showSpinner();

      const originalColor = window.getComputedStyle(inputElement).color;
      inputElement.dataset.originalColor = originalColor;
    
      inputElement.blur();
      inputElement.style.color = 'transparent'

      if (userChat.userInput() !== '') {
        await userChat.setUserResponse();
        inputElement.placeholder = '';
        userChat.scrollToBottomOfResults();
      }

      var response = await userChat.sendRequest();  //request);
      await userChat.assistantResponseHandler(response);

      inputElement.value = '';
      inputElement.style.color = inputElement.dataset.originalColor;
      inputElement.placeholder = 'Type a message';

      break;
  }
};

/**
 * Handles user responses triggered by pressing the Enter key.
 * @param {Event} e - The event object representing the keypress event.
 * @returns {Promise<boolean>} - A promise that resolves to true if the Enter key is pressed and the user input is not empty or consists only of whitespace; otherwise, resolves to false.
 */
async function enterClick(e) {
  var keyCode = e.keyCode || e.which;
  var text = document.getElementById("chat-input").value;

  if (keyCode === 13) {
    if (text == "" || text.trim() == "") {
      e.preventDefault();
      return false;
    } else {
      e.preventDefault();
      document.getElementById("chat-input").blur();
      await main();
    }
  }
};
