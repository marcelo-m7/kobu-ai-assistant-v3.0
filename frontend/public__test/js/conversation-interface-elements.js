/**
 * Represents elements for the convesation interface of a user and the AI assistant.
 */
export class InterfaceElements {
    constructor() {
        // # Possibles orientations values
        this.NEXT_STAGE = 'next_stage';
        this.VERIFY_ANSWER = 'verify_answer';
        this.PROCEED = 'proceed';

        // # Possible stages values
        this.WELCOME_STAGE = 'welcome';
        this.CHOOSE_SUBJECT_STAGE = 'choose_subject';
        this.DATA_COLLECTING_STAGE = 'data_colecting';
        this.RESUME_VALIDATION_STAGE = 'resume_validation';
        this.SEND_VALIDATION_STAGE = 'send_validation';
        this.FREE_CONVERSATION_STAGE = 'free_conversation';
        
    }
    
    // Assistant message element creation
    createMessageAssistantElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");
      
      div.classList.add("assistant_message", "messages_container");
      p.classList.add("assistant_message");
      p.innerHTML = content;
      div.appendChild(p);
      
      return div;
    };
    
    // User Options element creation
    createSuggestionAssistantElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");
      
      div.classList.add("assistant_message, assistant_suggestions_mandatory_true_container");
      p.classList.add("assistant_suggestion_mandatory_true");
      p.innerHTML = content;
      div.appendChild(p);
      
      return div;
    };

    // User message element creation
    createMessageUserElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");
      
      div.classList.add("user_message, messages_container");
      p.classList.add("user_message");
      p.innerHTML = content;
      div.appendChild(p);
      
      return div;
    };
  
    // Scroll to the bottom of the results div
    scrollToBottomOfResults() {
      var terminalResultsDiv = document.getElementById("messages_container");
      terminalResultsDiv.scrollTo({
        top: terminalResultsDiv.scrollHeight,
        behavior: 'smooth'
      });
    };
  
    // Ascii Spinner
    showSpinner() {
      document.querySelector(".spinner").style.display = "block";
      document.getElementById("user_input_container").disabled = true;
      document.getElementById("user_input_container").blur();
    };
    hideSpinner() {
      document.querySelector(".spinner").style.display = "none";
      document.getElementById("user_input_container").disabled = false;
    };

  }