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

    // User Options element creation
    createSuggestionAssistantElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");
      
      div.classList.add("content-block");
      p.classList.add("assistantSuggestion");
      p.innerHTML = content;
      div.appendChild(p);
      
      return div;
    };
    
    // Assistant message element creation
    createMessageAssistantElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");
      
      div.classList.add("content-block");
      p.classList.add("assistantResult");
      p.innerHTML = content;
      div.appendChild(p);
      
      return div;
    };
    
    // User message element creation
    createMessageUserElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");
      
      div.classList.add("content-block");
      p.classList.add("userEnteredText");
      p.innerHTML = content;
      div.appendChild(p);
      
      return div;
    };
  
    // Scroll to the bottom of the results div
    scrollToBottomOfResults() {
      var terminalResultsDiv = document.getElementById("result_div");
      terminalResultsDiv.scrollTo({
        top: terminalResultsDiv.scrollHeight,
        behavior: 'smooth'
      });
    };
  
    // Ascii Spinner
    showSpinner() {
      document.querySelector(".spinner").style.display = "block";
      document.getElementById("chat-input").disabled = true;
      document.getElementById("chat-input").blur();
    };
    hideSpinner() {
      document.querySelector(".spinner").style.display = "none";
      document.getElementById("chat-input").disabled = false;
    };

  }