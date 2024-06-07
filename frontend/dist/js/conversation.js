import { Interface } from './conversation-interface.js';

const LOCAL_PROXY_URL = 'http://localhost:3000/proxy';
const CONTACT_URL = "https://kobu.agency/contact";
const CHAT_HISTORY_KEY = 'chat_history';
const USER_ID_KEY = 'userId';
const ERROR_RESPONSE = {
  "message": `Sorry, but I'm unable to assist you at the moment. Please contact <a href='${CONTACT_URL}'>Kobu.agency/Contact</a> for further assistance.`,
  "current_stage": "error"
};

/**
 * Represents a conversation between a user and an AI assistant.
 * Extends Interface class to handle conversation interface.
 * @param {string} userId - The unique ID of the user.
 */
export class Conversation extends Interface {
  constructor(userId) {
    super();
    this.userId = userId;
    this.options = null;
    this.choosedSubject = null;
    this.currentStage = this.WELCOME_STAGE;
    this.nextStage = '';
    this.subject = null;
    this.orientation = 'proceed';
    this.message = null;

    (this.setupSuggestionListener.bind(this))();
  }

  setupSuggestionListener() {
    const elements = document.getElementsByClassName('input-suggestion');
    Array.from(elements).forEach(element => {
      element.addEventListener('click', async (e) => {
        e.stopImmediatePropagation();
        const optionText = e.target.textContent.trim();
        console.log(e, optionText);
        this.currentStage = this.nextStage;
        await this.optionListener(optionText);
      });
    });
  }

  /**
   * Sends a request to the specified URL (default local proxy) with the provided data.
   * @param {object} data - The data to be sent with the request.
   * @returns {Promise<object>} - A promise resolving to the response data from the server.
   */
  async sendRequest(data = this.requestData()) {
    try {
      const response = await fetch(LOCAL_PROXY_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) throw new Error(`Network Error: ${response.statusText}`);

      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('Fetch error:', error);
      return ERROR_RESPONSE;
    }
  }

  /**
   * Generates a unique user ID using the current timestamp and a random number.
   * If a user ID is not already stored in the local storage, generates a new one and stores it.
   * @returns {string} - The generated or retrieved unique user ID.
   */
  static generateUserId() {
    if (!localStorage.getItem(USER_ID_KEY)) {
      const userId = Date.now().toString() + Math.floor(Math.random() * 1000);
      localStorage.setItem(USER_ID_KEY, userId);
    }
    return localStorage.getItem(USER_ID_KEY);
  }

  /**
   * Handles the response from the assistant, updating the conversation state and UI accordingly.
   * @param {object} response - The response from the assistant.
   */
  async assistantResponseHandler(response) {
    const {
      message,
      options,
      choosed_subject: choosedSubject,
      current_stage: currentStage,
      next_stage: nextStage,
      subject,
      orientation
    } = response;

    Object.assign(this, {
      message,
      options,
      choosedSubject,
      currentStage,
      nextStage,
      subject,
      orientation
    });

    this.scrollToBottomOfResults();
    await this.setAssistantResponse(this.message);
    this.scrollToBottomOfResults();

    const inputElement = document.getElementById('user-input');
    inputElement.value = '';
    inputElement.placeholder = '';

    if (this.options) {
      inputElement.blur();
      this.scrollToBottomOfResults();
      await this.setAssistantSuggestion(this.options);
      await this.addOptionListener();
    }

    console.log("assistantResponseHandler after await");
    this.chatHistoryBuffer(null, this.message);
  }

  async addOptionListener() {
    this.scrollToBottomOfResults();
    const inputElement = document.getElementById('user-input');
    inputElement.blur();
    inputElement.placeholder = 'Please, select an option';

    return new Promise((resolve) => {
      document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('conversation-option')) {
          const optionText = e.target.textContent;
          e.stopImmediatePropagation();
          inputElement.placeholder = '';
          this.scrollToBottomOfResults();
          await this.optionListener(optionText);
          inputElement.placeholder = 'Type a message';
          resolve();
        }
      });
    });
  }

  async optionListener(optionText) {
    this.scrollToBottomOfResults();
    await this.setUserResponse(optionText);
    this.scrollToBottomOfResults();

    const request = this.requestData(optionText);
    const response = await this.sendRequest(request);
    await this.assistantResponseHandler(response);
  }

  requestData(
    input = this.userInput(),
    currentStage = this.currentStage,
    nextStage = this.nextStage,
    choosedSubject = this.choosedSubject,
    subject = this.subject,
    orientation = this.orientation
  ) {
    return {
      "user_id": this.userId,
      "user_input": input,
      "current_stage": currentStage,
      "next_stage": nextStage,
      "choosed_subject": choosedSubject,
      "subject": subject,
      "orientation": orientation
    };
  }

  /**
   * Saves chat history array in LocalStorage.
   * @param {string} userInput - The user's input.
   * @param {string} assistantMessage - The assistant's message.
   */
  chatHistoryBuffer(userInput, assistantMessage) {
    let chatHistory = localStorage.getItem(CHAT_HISTORY_KEY);
    chatHistory = chatHistory ? JSON.parse(chatHistory) : [];

    if (userInput) chatHistory.push({ user: userInput });
    if (assistantMessage) chatHistory.push({ assistant: assistantMessage, system: Date.now().toString() });

    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(chatHistory));
  }
}
