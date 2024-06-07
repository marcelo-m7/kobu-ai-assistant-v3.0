import { Conversation } from './conversation.js';

const ELEMENTS = {
  statusClosed: "status-closed",
  chatboxWrapper: "chatbox-wrapper",
    chatboxOpenButton: "chatbox-open-button",
    chatboxContainer: "chatbox-container",
      userInputContainer: "user-input-container",
        userInput: "user-input",
        sendIcon: "send-icon",
    chatboxCloseButton: "chatbox-close-button"
};

export class StartConversation {
  constructor() {
    this.userId = Conversation.generateUserId();
    this.conversation = new Conversation(this.userId);

    this.initInterfaceElements();
    this.initInterfaceEventListeners();
  }

  initInterfaceElements() {
    this.chatboxWrapper = document.getElementById(ELEMENTS.chatboxWrapper);
    this.chatboxOpenButton = document.getElementById(ELEMENTS.chatboxOpenButton);
    this.chatboxContainer = document.getElementById(ELEMENTS.chatboxContainer);
    this.chatboxCloseButton = document.getElementById(ELEMENTS.chatboxCloseButton);
    this.sendIcon = document.getElementById(ELEMENTS.sendIcon);
    this.userInputContainer = document.getElementById(ELEMENTS.userInputContainer);
    this.userInput = document.getElementById(ELEMENTS.userInput);
  }

  initInterfaceEventListeners() {
    this.chatboxOpenButton.addEventListener("click", this.openChat.bind(this));
    this.chatboxCloseButton.addEventListener("click", this.closeChat.bind(this));
    this.sendIcon.addEventListener('click', this.hendleSendIcon.bind(this));
    this.userInputContainer.addEventListener('keyup', this.handleKeyUpPress.bind(this));
    this.userInputContainer.addEventListener('keypress', this.handleKeyUpPress.bind(this));
  }

  async main() {
    this.conversation.showSpinner();
    const inputElement = this.userInput;
    inputElement.blur();

    switch (this.conversation.currentStage) {
      case undefined:
      case '':
      case null:
      case this.conversation.WELCOME_STAGE:
        await this.handleWelcomeStage();
        // break;
      case this.conversation.CHOOSE_SUBJECT_STAGE:
        await this.handleChooseSubjectStage();
        break;
      default:
        await this.handleDefaultStage();
    }
  }

  async handleWelcomeStage() {
    console.log("Main: starts welcomeMessage()");
    const request = this.conversation.requestData("Hi, there!");
    const response = await this.conversation.sendRequest(request);
    await this.conversation.assistantResponseHandler(response);
    if (response.current_stage === 'error') return;
    await this.conversation.setVideo();
    this.conversation.currentStage = this.conversation.CHOOSE_SUBJECT_STAGE;
    console.log("Main: finish welcomeMessage()", this.conversation.currentStage);
  }

  async handleChooseSubjectStage() {
    console.log("Main: starts chooseSubject()");
    const request = this.conversation.requestData();
    const response = await this.conversation.sendRequest(request);
    if (response.message === false) {
      this.userInput.placeholder = 'Please, choose an option.';
      return;
    }
    await this.conversation.assistantResponseHandler(response);
    this.userInput.placeholder = 'Type a message';
  }

  async handleDefaultStage() {
    this.conversation.setUserResponse();
    const request = this.conversation.requestData();
    const inputElement = this.userInput
    inputElement.value = ''
    const response = await this.conversation.sendRequest(request);
    if (response.message === false) return;
    await this.conversation.assistantResponseHandler(response);
    this.userInput.placeholder = 'Type a message';
    console.log("Main: finish default()", this.conversation.currentStage);
  }

  async openChat() {
    this.toggleChatbox(false);
    await this.conversation.openChat(this.main.bind(this));
  }

  closeChat() {
    this.toggleChatbox(true);
  }
  // Set or remove .statusClosed class to the HTML Elements
  toggleChatbox(statusClosed) {
    const action = statusClosed ? 'add' : 'remove';
    [this.chatboxCloseButton, this.chatboxContainer, this.chatboxWrapper].forEach(el => el.classList[action](ELEMENTS.statusClosed));
  }

  async hendleSendIcon(e) {
    e.preventDefault();
    const optionText = this.conversation.userInput();
    if (!optionText) return;
    await this.conversation.openChat(this.main.bind(this));
  }

  async handleKeyUpPress(e) {
    if (e.keyCode === 13 || e.which === 13) {
      const text = this.userInput.value;
      if (text.trim() === "") {
        e.preventDefault();
        return false;
      }
      e.preventDefault();
      this.userInput.blur();
      await this.main();
      return true;
    }
    return false;
  }


}
