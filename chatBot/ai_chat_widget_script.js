document.addEventListener('DOMContentLoaded', () => {

    const BACKEND_URL = 'http://127.0.0.1:5001/api/v1/chatbot_query';

    function initializeChatWidget() {
        // Inject CSS
        const head = document.head || document.getElementsByTagName('head')[0];
        const styleLink = document.createElement('link');
        styleLink.rel = 'stylesheet';
        styleLink.type = 'text/css';
        styleLink.href = 'ai_chat_widget_styles.css';
        head.appendChild(styleLink);

        const widgetContainer = document.createElement('div');
        widgetContainer.id = 'ai_chat_widget_container';
        
        const chatBubbleHTML = `
            <div id="ai_chat_bubble">
                <span>&#129302;</span>
            </div>
        `;

        const chatWindowHTML = `
            <div id="ai_chat_window">
                <div id="ai_chat_header">AI Assistant</div>
                <div id="ai_chat_messages"></div>
                <div id="ai_chat_input_area">
                    <input type="text" id="ai_chat_input" placeholder="Ask a question...">
                    <button id="ai_chat_send_button">&#10148;</button>
                </div>
            </div>
        `;

        widgetContainer.innerHTML = chatBubbleHTML + chatWindowHTML;
        document.body.appendChild(widgetContainer);
    }

    initializeChatWidget();

    const chatBubble = document.getElementById('ai_chat_bubble');
    const chatWindow = document.getElementById('ai_chat_window');
    const messagesContainer = document.getElementById('ai_chat_messages');
    const chatInput = document.getElementById('ai_chat_input');
    const sendButton = document.getElementById('ai_chat_send_button');

    chatBubble.addEventListener('click', () => {
        chatWindow.style.display = (chatWindow.style.display === 'none' || chatWindow.style.display === '') ? 'flex' : 'none';
    });

    const sendMessage = async () => {
        const userMessage = chatInput.value.trim();
        if (userMessage === '') return;

        addMessageToUI(userMessage, 'user');
        chatInput.value = '';

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: userMessage })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            addMessageToUI(data.answer, 'bot');

        } catch (error) {
            console.error('Error fetching chatbot response:', error);
            addMessageToUI('Sorry, something went wrong. Please try again.', 'bot');
        }
    };

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function addMessageToUI(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.className = `ai_chat_message ai_chat_${sender}`;
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});