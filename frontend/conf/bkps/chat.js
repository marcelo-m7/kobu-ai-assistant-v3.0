import { Utils } from "./utils.js";

var userInput = () => document.getElementById('chat-input').value;

export class Chat extends Utils {
  constructor(userId) {
    super();
    this.userId = userId;
    this.options = null;
    this.choosedSubject = null;
    this.currentStage = this.WELCOME_STAGE;
    this.nextStage = ''
    this.subject = null
    this.orientation = 'proceed'
    this.message = null
  }

  // Set the assistant answer, save the assistant messagem, refresh haldle variables and display the user inputs options (if any)
  async assistantResponseHandler(response) {
    this.message = response.message;
    this.options = response.options;
    this.choosedSubject = response.choosed_subject;
    this.currentStage = response.current_stage;
    this.nextStage = response.next_stage
    this.subject = response.subject
    this.orientation = response.orientation
    await this.setAssistantResponse(this.message)

    if (this.options ) {
      var inputElement = document.getElementById('chat-input');
      inputElement.blur();
      inputElement.placeholder = '';
      await this.setAssistantSuggestion(this.options);
      document.getElementById("chat-input").blur();
      await this.addOptionListinner();
    }
    console.log("assistantResponseHandler after await")
    this.chatHistoryBuffer(null, this.message);
    
  };

  async addOptionListinner() {
        // Seleciona o elemento de entrada pelo ID
    var inputElement = document.getElementById('chat-input');
    inputElement.placeholder = 'Please, select an option';
    
    return new Promise((resolve, reject) => {
      document.addEventListener("click", async (e) => {
        if (e.target.classList.contains("assistantSuggestion")) {
          inputElement.placeholder = '';
          var optionText = e.target.textContent;
          e.stopImmediatePropagation();
          await this.optionListinner(optionText);
          // Define o novo valor do placeholder
          inputElement.placeholder = 'Type a message';
          resolve();
        }
      });
    });
  }

  async optionListinner(optionText) {
    await this.setUserResponse(optionText);
    var request = this.requestData(optionText);
  
    var response = await this.sendRequest(request);
    console.log(response);
    await this.assistantResponseHandler(response);
  };

  requestData (
      input = userInput(), 
      currentStage = this.currentStage,
      nextStage = this.nextStage,
      choosedSubject = this.choosedSubject,
      subject = this.subject,
      orientation = this.orientation,
  ) { 
    return {
      "user_id": this.userId,
      "user_input": input,
      "current_stage": currentStage,
      "next_Stage": nextStage,
      "choosed_subject": choosedSubject,
      "subject": subject,
      "orientation": orientation
    }
  };
  
/**
 * Sends a request to the specified URL (default local proxy) with the provided data.
 * @param {object} data - The data to be sent with the request.
 * @returns {Promise<object>} - A promise resolving to the response data from the server.
 */
async sendRequest(data = this.requestData()) {
  try {
    // Specify the URL for the request (default local proxy)
    const url = 'http://localhost:3000/proxy'; // Default local proxy (no need to add any URL)

    // Uncomment the following lines to use a different proxy or no proxy at all
    // const url = 'https://assistant.kobudev.com/kobu-assistant'; // Use this URL if you don't want to use any proxy
    // const proxyUrl = 'https://cors-anywhere.herokuapp.com/';  // Set the external proxy URL if desired
    // const response = await fetch(proxyUrl + url, { // Use an external proxy (uncomment this line if using an external proxy)

    // Send the request to the specified URL
    const response = await fetch(url, { // Use the default local proxy (comment this line if using an external proxy)
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(data)
    });

    // Check if the response is successful
    if (!response.ok) {
      throw new Error('Network Error');
    } else {
      // Parse the response data and return it
      const responseData = await response.json();
      console.log(responseData);
      return responseData;
    }
  } catch (error) {
    // Handle any errors that occur during the request
    console.error(error);
    // Return a default error message if the request fails
    return { "message": "Sorry, but I'm unable to assist you at the moment. Please contact <a href='https://kobu.agency/contact'>Kobu.agency/Contact</a> for further assistance." };
  }
}


  // ------ Axios Framework (To test):
  // import axios from 'axios';

  // async sendRequest(data = this.requestData()) {
  //   const url = 'https://assistant.kobudev.com/kobu-assistant';

  //   try {
  //     const response = await axios.post(url, data, {
  //       headers: {
  //         'Content-Type': 'application/json',
  //         'Accept': 'application/json',
  //       }
  //     });

  //     if (response.status !== 200) {
  //       throw new Error('Erro de rede');
  //     } else {
  //       const responseData = response.data;
  //       console.log(responseData);
  //       return responseData;
  //     }
  //   } catch (error) {
  //     console.error(error);
  //     return { "message": "Sorry my dear, but I don't think I'm working properly to help you today. You may send a message to <a href='https://kobu.agency/contact'>Kobu.agency/Contact</a>, please." };
  //   }
  // }
  // ------ END Axios


  // async sendRequest(data = this.requestData()) {
  //   const url = 'https://assistant.kobudev.com/kobu-assistant';
  //   const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
  
  //   try {
  //     // const response = await fetch(url, {
  //     const response = await fetch(proxyUrl + url, {
  //       method: 'POST',
  //       mode: 'cors',
  //       headers: {
  //         'Content-Type': 'application/json',
  //         'Accept': 'application/json',
  //       },
  //       body: JSON.stringify(data)
  //     });
  
  //     if (!response.ok) {
  //       throw new Error('Erro de rede');
  //     }
  //     else {
  //     const responseData = await response.json();
  //     console.log(responseData);
  //     return responseData;
  //     }
  //   } catch (error) {
  //     console.error(error);
  //     return { "message": "Sorry my dear, but I don't think I'm working properly to help you today. You may send a message to <a href='https://kobu.agency/contact'>Kobu.agency/Contact</a>, please." };
  //   }
  // }


  
  // Saves chatHistory array in LocalStorage
  chatHistoryBuffer(userInput, assistantMessage) {
    let chatHistory = localStorage.getItem('chat_history');
    if (!chatHistory) {
      chatHistory = [];
    } else {
      chatHistory = JSON.parse(chatHistory);
    }
    if (userInput){chatHistory.push({ user: userInput })};
    if (assistantMessage){chatHistory.push({ assistant: assistantMessage, system: Date.now().toString() })};
    localStorage.setItem('chat_history', JSON.stringify(chatHistory));
  };

  // Set user response in result_div
  async setUserResponse(user_input = userInput()) {
    document.getElementById("chat-input").blur();
    
    const userResponseElement = this.createMessageUserElement(user_input);
    
    // Hide the element initially
    userResponseElement.style.opacity = 0;
    userResponseElement.style.display = "block";
  
    // Append the element to the result_div
    document.getElementById("result_div").appendChild(userResponseElement);
    
    // Apply fadeIn effect
    await this.fadeIn(userResponseElement);
  
    this.scrollToBottomOfResults();
    this.showSpinner();
  };

  // Set assisant response in result_div
  async setAssistantResponse(message) {
    var text = this.formatAssistantMessage(message);
  
    const assistantResponseElement = this.createMessageAssistantElement(text);
    assistantResponseElement.style.opacity = 0; 
    document.getElementById("result_div").appendChild(assistantResponseElement);
  
    await this.fadeIn(assistantResponseElement);
  
    this.scrollToBottomOfResults();
    this.hideSpinner();
    document.getElementById("chat-input").focus();
  };
  
  // Set assisant response in result_div
  async setVideo() {
    var text = "[THE VIDEO WILL BE EXIB HERE]";

    const assistantResponseElement = this.createMessageAssistantElement(text);
    assistantResponseElement.style.opacity = 0;
    document.getElementById("result_div").appendChild(assistantResponseElement);

    await this.fadeIn(assistantResponseElement);

    this.scrollToBottomOfResults();
    this.hideSpinner();
    document.getElementById("chat-input").focus();
  };

  async setAssistantSuggestion(options) {
    document.getElementById("chat-input").blur();
  
    for (let i = 0; i < options.length; i++) {
      let option = this.formatAssistantMessage(options[i]);
      const assistantResponseElement = this.createSuggestionAssistantElement(option);
      assistantResponseElement.style.opacity = 0; 
      document.getElementById("result_div").appendChild(assistantResponseElement);
  
      await this.fadeIn(assistantResponseElement);
  
      assistantResponseElement.style.display = "block";
    }
  
    this.scrollToBottomOfResults();
    this.hideSpinner();
    document.getElementById("chat-input").disabled = true;
  };

};