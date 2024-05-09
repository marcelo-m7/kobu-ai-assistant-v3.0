export class Utils {
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

    this.count = 0;
  }

  // Generate a unic User ID
  static generateUserId() {
    if (!localStorage.getItem('userId')) {
      var userId = Date.now().toString() + Math.floor(Math.random() * 1000);
      localStorage.setItem('userId', userId);
    }
    return localStorage.getItem('userId');
  };

  // Close chatbox
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

  // Open chatbox
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
  };
ZZ
  // FadeIn efect
  async fadeIn(element) {
    return new Promise((resolve) => {
      var opacity = 0;
      var interval = setInterval(function() {
        if (opacity < 1) {
          opacity += 0.2; // você pode ajustar a velocidade ajustando esse valor
          element.style.opacity = opacity;
        } else {
          clearInterval(interval);
          resolve(); // Resolva a Promise quando a animação for concluída
        }
      }, 50); // você pode ajustar a velocidade ajustando esse valor
    });
  }

  // Invokes the chatbox
  invokeChatBox() {
    var assistant =
    `
    <div class="chatCont" id="chatCont">
    
    <div class="assistant_profile">
      <div class="close" id="closeButton">
        <i class="fa fa-times" aria-hidden="true"></i>
      </div>
    </div><!--assistant_profile end-->
    
    <div id="result_div" class="resultDiv">
    <!-- messages -->
    </div>
    
    <div class="chatForm" id="chat-div">
        <div class="spinner">
            <div class="bounce1"></div>
            <div class="bounce2"></div>
            <div class="bounce3"></div>
        </div>
    
      <input type="text" id="chat-input" autocomplete="off" placeholder="Type a message" class="form-control assistant-txt  "/>
    
    </div>
    </div><!--chatCont end-->
    
    
    <div class="profile_div">
    <div class="row">
        <div class="col-hgt">
            <img src="../static/img/kobu-chatbox-icon.svg" class="img-circle img-profile">
        </div><!--col-hgt end-->
    </div><!--row end-->
    </div><!--profile_div end-->
    `;
    return assistant;
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

  formatAssistantMessage(message) {
    if (message.trim() == "") {
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