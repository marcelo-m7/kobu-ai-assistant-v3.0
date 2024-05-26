/**
 * Represents elements for the conversation interface of a user and the AI assistant.
 */
export class InterfaceElements {
  constructor() {
      // Possible orientations values
      this.NEXT_STAGE = 'next_stage';
      this.VERIFY_ANSWER = 'verify_answer';
      this.PROCEED = 'proceed';

      // Possible stages values
      this.WELCOME_STAGE = 'welcome';
      this.CHOOSE_SUBJECT_STAGE = 'choose_subject';
      this.DATA_COLLECTING_STAGE = 'data_collecting';
      this.RESUME_VALIDATION_STAGE = 'resume_validation';
      this.SEND_VALIDATION_STAGE = 'send_validation';
      this.FREE_CONVERSATION_STAGE = 'free_conversation';
  }

  // Assistant message element creation
  createMessageAssistantElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");

      div.classList.add("assistant-message");
    //   p.classList.add("message assistant-message");
      p.innerHTML = content;
      div.appendChild(p);

      return div;
  };

  // User Options element creation
  createSuggestionAssistantElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");

      div.classList.add("assistant-message");
      div.classList.add("conversation-option");
      p.innerHTML = content;
      div.appendChild(p);

      return div;
  };

  // User message element creation
  createMessageUserElement(content) {
      const div = document.createElement("div");
      const p = document.createElement("p");

      div.classList.add("user-message");
    //   p.classList.add("message user-message");
      p.innerHTML = content;
      div.appendChild(p);

      return div;
  };

  // Scroll to the bottom of the results div
  scrollToBottomOfResults() {
      var terminalResultsDiv = document.getElementById("messages-container");
      terminalResultsDiv.scrollTo({
          top: terminalResultsDiv.scrollHeight,
          behavior: 'smooth'
      });
  };

  // Ascii Spinner
  showSpinner() {
    this.scrollToBottomOfResults();
    document.querySelector(".spinner").style.display = "block";
    this.scrollToBottomOfResults();
    document.getElementById("user-input").disabled = true;
    document.getElementById("user-input").blur();
  };
  hideSpinner() {
      document.querySelector(".spinner").style.display = "none";
      document.getElementById("user-input").disabled = false;
      document.getElementById("user-input").focus();
  };
}
