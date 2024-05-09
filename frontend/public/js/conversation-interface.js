import { InterfaceElements } from './conversation-interface-elements.js';

/**
 * Represents an interface for managing conversation between the user and the AI assistant.
 * This class inherits elements from the InterfaceElements class and provides methods for interface manipulation.
 */
export class Interface extends InterfaceElements {
    constructor() {
        super();
        this.count = 0;
    }

    userInput = () => document.getElementById('chat-input').value;

    /**
     * Closes the chatbox by hiding its content.
     * @returns {Promise<void>} - A promise that resolves after the chatbox is closed.
     */
    async closeChat() {
        const chatContent = document.querySelector(".chatCont");
        if (chatContent) {
            chatContent.style.display = 'none';
            await this.fadeIn(chatContent)
            console.log("Chat closed.");

        } else {
            console.log("Chat element has not been fond on.");
        }
    }

    /**
     * Opens the chatbox by displaying its content and optionally executing a main function.
     * @param {Function} main - The main function to execute after opening the chatbox.
     * @returns {Promise<void>} - A promise that resolves after the chatbox is opened.
     */
    async openChat(main) {
        const chat = document.querySelectorAll(".profile_div, .chatCont, .assistant_profile, .chatForm");
        chat.forEach(async function(element) {
            element.style.display = 'block';
        });
        console.log("Chat opened.");

        if (this.count === 0) {
            console.log("First acess to the chat.");
            this.count += 1;
            await main();
        }
    }

    /**
     * Animates the fadeIn effect for an HTML element by gradually increasing its opacity.
     * @param {HTMLElement} element - The HTML element to apply the fadeIn effect to.
     * @returns {Promise<void>} - A promise that resolves after the fadeIn effect is complete.
     */
    async fadeIn(element) {
        return new Promise((resolve) => {
            var opacity = 0;
            var interval = setInterval(function() {
                if (opacity < 1) {
                    opacity += 0.2;
                    element.style.opacity = opacity;

                } else {
                    clearInterval(interval);
                    resolve();
                }
            }, 50);
        });
    }

    formatAssistantMessage(message) {
        // if (message.trim() == "") {
        if (message == "") {
          message = "I couldn't get that. Let's try something else!";
        }
    
        // Replace characters with HTML format. There is an option to put the modifications on the backend side (using or not AI to format)
        message = message.replace(/\*/g, '<strong>'); // Replace * with <strong>
        message = message.replace(/\*\//g, '</strong>'); // Add closing tag </strong> after each <strong>
        message = message.replace(/_([^_]+)_/g, '<em>$1</em>'); // Replace _text_ with <em>text</em>
        message = message.replace(/~([^~]+)~/g, '<del>$1</del>'); // Replace ~text~ with <del>text</del>
        message = message.replace(/\[([^[]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>'); // Replace [link](URL) with <a href="URL">link</a>
        message = message.replace(/#([^#\s]+)/g, '<span class="hashtag">#$1</span>'); // Replace #hashtag with <span class="hashtag">hashtag</span>
        message = message.replace(/@([^@\s]+)/g, '<span class="mention">@$1</span>'); // Replace @mention with <span class="mention">@mention</span>
        message = message.replace(new RegExp("\r?\n", "g"), "<br />");
    
        return message;
    };

    // Set user response in result_div
    async setUserResponse(user_input = this.userInput()) {
        document.getElementById("chat-input").blur();
        const userResponseElement = this.createMessageUserElement(user_input);

        // Hide the element initially
        userResponseElement.style.opacity = 0;
        userResponseElement.style.display = "block";
        // Append the element to the result_div
        document.getElementById("result_div").appendChild(userResponseElement);
        // Apply fadeIn effect

        this.scrollToBottomOfResults();
        await this.fadeIn(userResponseElement);

        this.showSpinner();
    };

    // Set assisant response in result_div
    async setAssistantResponse(message) {
        var text = this.formatAssistantMessage(message);

        const assistantResponseElement = this.createMessageAssistantElement(text);
        assistantResponseElement.style.opacity = 0; 
        document.getElementById("result_div").appendChild(assistantResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(assistantResponseElement);

        this.hideSpinner();
        document.getElementById("chat-input").focus();
    };

    // Set assisant response in result_div
    async setVideo() {
        var text = "[THE VIDEO WILL BE EXIB HERE]";

        const assistantResponseElement = this.createMessageAssistantElement(text);
        assistantResponseElement.style.opacity = 0;
        document.getElementById("result_div").appendChild(assistantResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(assistantResponseElement);

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

            this.scrollToBottomOfResults();
            await this.fadeIn(assistantResponseElement);

            assistantResponseElement.style.display = "block";
        }

        this.scrollToBottomOfResults();
        this.hideSpinner();
        document.getElementById("chat-input").disabled = true;
    };

};