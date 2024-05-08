import { Chat } from './chat.js';

// Consts
const userId = Chat.generateUserId();
const userChat = new Chat(userId);

// Listinners
document.querySelector(".profile_div").addEventListener('click', async () => {
  await userChat.openChat(main);
});
document.getElementById("closeButton").addEventListener('click', async () => {
  await userChat.closeChat()
});
document.getElementById("chat-input").addEventListener('keyup', async (e) => {
  await enterClick(e)
});
document.getElementById("chat-input").addEventListener('keypress', async (e) => {
  await enterClick(e)
});

async function main() {
  switch (userChat.currentStage) {
    
    case undefined:
    case '':
    case null:
    case userChat.WELCOME_STAGE:
      console.log("Main: starts welcomeMessage()");
      await FLOW_TEMPLATES.welcomeStageTemplate();
      userChat.currentStage = userChat.CHOOSE_SUBJECT_STAGE;
      console.log("Main: finish welcomeMessage() ", userChat.currentStage);
      
      case userChat.CHOOSE_SUBJECT_STAGE:
        console.log("Main: starts chooseSubject()");
      await FLOW_TEMPLATES.chooseSubjectStageTemplate();
      userChat.currentStage = userChat.DATA_COLLECTING_STAGE;
      console.log("Main: finish chooseSubject() ", userChat.currentStage);
      break;
      
      default:
        console.log("Main: start default()");
        await FLOW_TEMPLATES.defaultTemplate();
        userChat.assistantResponseHandler(response);
        console.log("Main: finish default() ", userChat.currentStage);
        break;
      }
}

// Chat flow templates for different stages
var FLOW_TEMPLATES = {
  
  welcomeStageTemplate: async function() {
    userChat.showSpinner();
    var inputElement = document.getElementById('chat-input');
    inputElement.placeholder = '';

    userChat.currentStage = userChat.WELCOME_STAGE; // First interaction with the API
    
    let request = userChat.requestData("Hi, there!");
    var response = await userChat.sendRequest(request);
    
    await userChat.assistantResponseHandler(response);
    await userChat.setVideo();
    // Wait until the video ends
  },
  
  chooseSubjectStageTemplate: async function() {
    var inputElement = document.getElementById('chat-input');
    inputElement.placeholder = '';

    userChat.showSpinner();
    userChat.currentStage = userChat.CHOOSE_SUBJECT_STAGE; // Ask for the subejects list
    let request = userChat.requestData() // input="Choose subject stage")
    var response = await userChat.sendRequest(request);

    await userChat.assistantResponseHandler(response); // "Please, choose a option bellow: "
    inputElement.placeholder = 'Type a message'
  },
    
  defaultTemplate: async function() {
    var inputElement = document.getElementById('chat-input');
    inputElement.placeholder = '';
    userChat.showSpinner();
    userChat.setUserResponse()
    var response = await userChat.sendRequest();
    await userChat.assistantResponseHandler(response);
    inputElement.placeholder = 'Type a message'

  }
};

// Treat the user responses send by clicking Enter key
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
