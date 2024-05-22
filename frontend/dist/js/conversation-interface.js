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

    userInput = () => document.getElementById('user-input').value;

    
    /**
     * Opens the chatbox by displaying its content and optionally executing a main function.
     * @param {Function} main - The main function to execute after opening the chatbox.
     * @returns {Promise<void>} - A promise that resolves after the chatbox is opened.
     */
    async openChat(main) {
        const chat = document.querySelectorAll(".chatbox-container");
        chat.forEach(element => {
            element.style.opacity = 0
            element.style.display = 'block';
            element.style.opacity = 1
        });
        console.log("Chat opened.");
    
        // Call animation function
        await this.animateChatItems(main, chat);
    }

    async animateChatItems(main, chat) {
        // const chat = document.querySelectorAll(".chatbox-container");

        for (let i = 0; i < chat.length; i++) {
            const item = chat[i];
            item.style.opacity = 0;
            item.display = "block"
            item.style.transform = "translateY(20px)";
            item.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    
            // Delay each item by 500 milliseconds
            await new Promise(resolve => setTimeout(resolve, 1));
    
            item.style.opacity = 1;
            item.style.transform = "translateY(0)";
        }
    
        console.log("Chat animation completed.");
    
        // Check if it's the first access to the chat
        if (this.count === 0) {
            console.log("First access to the chat.");
            this.count += 1;
            await main();
        }
    }
    async animateChat(chat) {
        // const chat = document.querySelectorAll(".chatbox-container");

        for (let i = 0; i < chat.length; i++) {
            const item = chat[i];
            item.style.opacity = 0;
            item.display = "block"
            item.style.transform = "translateY(20px)";
            item.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    
            // Delay each item by 500 milliseconds
            await new Promise(resolve => setTimeout(resolve, 1));
    
            item.style.opacity = 1;
            item.style.transform = "translateY(0)";
        }
    
        console.log("Chat animation completed.");
    
    }


    async openChat_old(main) {
        const chat = document.querySelectorAll(".chatbox-container");
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
                    element.style.display = 'block';
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
        message = message.replace(/\*/g, "<strong>");
        message = message.replace(/\*\//g, '</strong>');
        message = message.replace(/_([^_]+)_/g, '<em class="assistant_message">$1</em>');
        message = message.replace(/~([^~]+)~/g, '<del class="assistant_message">$1</del>');
        message = message.replace(/\[([^[]+)\]\(([^)]+)\)/g, '<a class="assistant_message" href="$2">$1</a>');
        message = message.replace(/#([^#\s]+)/g, '<span class="hashtag">#$1</span>');
        message = message.replace(/@([^@\s]+)/g, '<span class="mention">@$1</span>');
        message = message.replace(new RegExp("\r?\n", "g"), "<br />");
        return message;
    };
     
    // Set user response in messages-container
    async setUserResponse(user_input = this.userInput()) {
        document.getElementById("user-input").blur();
        const userResponseElement = this.createMessageUserElement(user_input);

        // Hide the element initially
        userResponseElement.style.opacity = 0;
        userResponseElement.style.display = "block";
        // Append the element to the messages-container
        document.getElementById("messages-container").appendChild(userResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(userResponseElement);
        this.showSpinner();
    };

    // Set assistant response in messages-container
    async setAssistantResponse(message) {
        var text = this.formatAssistantMessage(message);

        const assistantResponseElement = this.createMessageAssistantElement(text);
        assistantResponseElement.style.opacity = 0; 
        document.getElementById("messages-container").appendChild(assistantResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(assistantResponseElement);

        this.hideSpinner();
        document.getElementById("user-input-container").focus();
    };

    // Set assistant response in messages-container
    async setVideo() {
        var text = "[THE VIDEO WILL BE EXIB HERE]";

        const assistantResponseElement = this.createMessageAssistantElement(
        `
        <video src="../video/hire_us_1920x1080.webm" controls aria-label="Assistant Welcome Video" id="assistant-welcome-video">
        </video>
        `
        );
        assistantResponseElement.style.opacity = 0;
        document.getElementById("messages-container").appendChild(assistantResponseElement);

        this.scrollToBottomOfResults();
        await this.fadeIn(assistantResponseElement);

        this.hideSpinner();
        document.getElementById("user-input").focus();
    };

    async setAssistantSuggestion(options) {
        document.getElementById("user-input").blur();

        for (let i = 0; i < options.length; i++) {
            let option = this.formatAssistantMessage(options[i]);
            const assistantResponseElement = this.createSuggestionAssistantElement(option);
            assistantResponseElement.style.opacity = 0; 
            document.getElementById("messages-container").appendChild(assistantResponseElement);

            this.scrollToBottomOfResults();
            await this.fadeIn(assistantResponseElement);

            assistantResponseElement.style.display = "block";
        }
        this.scrollToBottomOfResults();
        this.hideSpinner();
        document.getElementById("user-input").disabled = true;
    };

};
