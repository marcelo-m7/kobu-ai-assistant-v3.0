import { Interface } from './conversation-interface.js';

/**
 * Represents a conversation between a user and an AI assistant.
 * Extends Interface class to handle conversation interface.
 * @param {string} userId - The unique ID of the user.
 */
export class Conversation extends Interface{
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
    };
    
    /**
     * Generates a unique user ID using the current timestamp and a random number.
     * If a user ID is not already stored in the local storage, generates a new one and stores it.
     * @returns {string} - The generated or retrieved unique user ID.
     */
    static generateUserId() {
        if (!localStorage.getItem('userId')) {
            var userId = Date.now().toString() + Math.floor(Math.random() * 1000);
            localStorage.setItem('userId', userId);
        }
        return localStorage.getItem('userId');
    };

    // Set the assistant answer, save the assistant messagem, refresh haldle variables and display the user inputs options (if any)
    async assistantResponseHandler(response) {
        this.message = response.message;
        this.options = response.options;
        this.choosedSubject = response.choosed_subject;
        this.currentStage = response.current_stage;
        this.nextStage = response.next_stage
        this.subject = response.subject
        this.orientation = response.orientation

        await this.setAssistantResponse(this.message);
        this.scrollToBottomOfResults();

        var inputElement = document.getElementById('chat-input');
        if (this.options ) {
            inputElement.blur();
            inputElement.placeholder = '';
            await this.setAssistantSuggestion(this.options);
            this.scrollToBottomOfResults();
            document.getElementById("chat-input").blur();
            await this.addOptionListinner();
        }

        inputElement.value = '';
        console.log("assistantResponseHandler after await");
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
        input = this.userInput(), 
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

}