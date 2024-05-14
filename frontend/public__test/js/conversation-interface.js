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

    userInput = () => document.getElementById('user_input').value;

    /**
     * Closes the chatbox by hiding its content.
     * @returns {Promise<void>} - A promise that resolves after the chatbox is closed.
     */
    async closeChat() {
        const chatContent = document.querySelector(".chatCont.open_chatbox_container");
        if (chatContent) {
            chatContent.style.display = 'none';
            await this.fadeIn(chatContent);
            console.log("Chat closed.");

        } else {
            console.log("Chat element has not been found.");
        }
    }

    /**
     * Opens the chatbox by displaying its content and optionally executing a main function.
     * @param {Function} main - The main function to execute after opening the chatbox.
     * @returns {Promise<void>} - A promise that resolves after the chatbox is opened.
     */
    async openChat(main) {
        const chat = document.querySelectorAll(".assistant_chatbox.open_chatbox_container");
        chat.forEach(async function(element) {
            element.style.display = 'block';
        });
        console.log("Chat opened.");

        if (this.count === 0) {
            console.log("First access to the chat.");
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
        if (message == "") {
          return false
        }
    
        message = message.replace(/\*/g, '<strong>'); 
        message = message.replace(/\*\//g, '</strong>'); 
        message = message.replace(/_([^_]+)_/g, '<em>$1</em>'); 
        message = message.replace(/~([^~]+)~/g, '<del>$1</del>'); 
        message = message.replace(/\[([^[]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>'); 
        message = message.replace(/#([^#\s]+)/g, '<span class="hashtag assistant_message">#$1</span>'); 
        message = message.replace(/@([^@\s]+)/g, '<span class="mention assistant_message">@$1</span>'); 
        message = message.replace(new RegExp("\r?\n", "g"), "<br />");
    
        return message;
    };

    // Set user response in messages_container
    async setUserResponse(user_input = this.userInput()) {
        document.getElementById("user_input").blur();
        const userResponseElement = this.createMessageUserElement(user_input);

        // Hide the element initially
        userResponseElement.style.opacity = 0;
        userResponseElement.style.display = "block";
        // Append the element to the messages_container
        document.getElementById("messages_container").appendChild(userResponseElement);
        // Apply fadeIn effect

        this.scrollToBottomOfResults();
        await this.fadeIn(userResponseElement);

        this.showSpinner();
    };

    // Set assistant response in messages_container
    async setAssistantResponse(message) {
        var text = this.formatAssistantMessage(message);

        const assistantResponseElement = this.createMessageAssistantElement(text);
        assistantResponseElement.style.opacity = 0; 
        document.getElementById("messages_container").appendChild(assistantResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(assistantResponseElement);

        this.hideSpinner();
        document.getElementById("user_input_container").focus();
    };

    // Set assistant response in messages_container
    async setVideo() {
        var text = "[THE VIDEO WILL BE EXIB HERE]";

        const assistantResponseElement = this.createMessageAssistantElement(
        `<div class="assistant_message">
            <video src="/js/video/hire_us_1920x1080.webm" id="assistant_welcome_video">
            </video>
        </div>`
        );
        assistantResponseElement.style.opacity = 0;
        document.getElementById("messages_container").appendChild(assistantResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(assistantResponseElement);

        this.hideSpinner();
        document.getElementById("user_input").focus();
    };

    async setAssistantSuggestion(options) {
        document.getElementById("user_input").blur();

        for (let i = 0; i < options.length; i++) {
            let option = this.formatAssistantMessage(options[i]);
            const assistantResponseElement = this.createSuggestionAssistantElement(option);
            assistantResponseElement.style.opacity = 0; 
            document.getElementById("messages_container").appendChild(assistantResponseElement);

            this.scrollToBottomOfResults();
            await this.fadeIn(assistantResponseElement);

            assistantResponseElement.style.display = "block";
        }

        this.scrollToBottomOfResults();
        this.hideSpinner();
        document.getElementById("user_input").disabled = true;
    };

};
