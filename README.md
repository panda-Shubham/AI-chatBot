# Plug-and-Play AI Chatbot for any Website

This project provides a simple yet powerful way for any website owner to add a personalized AI chatbot to their site. The chatbot's knowledge is based entirely on a PDF document you provide, ensuring it only gives answers relevant to your website's content.

The application uses OpenRouter, allowing you to easily use powerful AI models like Google's Gemini, Anthropic's Claude, and others with a single API key.



## Features

-   **Easy Integration:** Add the chatbot to any website by simply including a CSS and a JavaScript file.
-   **Custom Knowledge Base:** Just add a `website_knowledge_base.pdf` file to feed the chatbot with your specific data.
-   **Flexible AI Models:** Built to use OpenRouter, giving you access to Gemini, Claude, Llama, and more.
-   **Simple User Interface:** A clean, non-intrusive chat bubble that stays fixed at the bottom-right of the screen.
-   **No Database Needed:** The application is self-contained and requires no external database setup.

## How It Works

The application is built in two main parts:

1.  **Frontend (The Chat Widget):** This is a set of HTML, CSS (`ai_chat_widget_styles.css`), and JavaScript (`ai_chat_widget_script.js`) files. When you add these to your website, they create the chat bubble and the chat window. The JavaScript is responsible for sending user messages to the backend and displaying the AI's responses.

2.  **Backend (The Brains):** This is a Python server (`gemini_chatbot_backend_service.py`) that you run on your machine or a server. It does the heavy lifting:
    -   On startup, it reads and processes your `website_knowledge_base.pdf`.
    -   It securely prompts for and stores your OpenRouter API key.
    -   It receives questions from the frontend, combines them with the PDF content, and sends everything to the OpenRouter API to get an intelligent answer.

## Getting Started

Follow these steps to get the chatbot running on your website.

### Prerequisites

-   You need to have **Python 3.7+** installed on your system.
-   You need an **OpenRouter API Key**. You can get one for free from the [OpenRouter website](https://openrouter.ai/).

### Installation Guide

**Step 1: Get the Project Files**

Clone this repository or download the files to your computer.
git clone https://github.com/panda-Shubham/AI-chatBot.git


**Step 2: Arrange the Folder Structure**

my_awesome_website/
│
├── index.html                  <-- Your website's main page.
│
├── ai_chat_widget_styles.css   <-- The chatbot's CSS file.
├── ai_chat_widget_script.js    <-- The chatbot's JavaScript file.
│
└── my_chatbot_app/
    │
    ├── gemini_chatbot_backend_service.py   <-- The Python server.
    │
    ├── website_knowledge_base.pdf          <-- **REPLACE THIS WITH YOUR PDF**
    │
    └── requirements.txt                    <-- The list of Python packages.


**Step 3: Set Up the Backend**

This is where you'll install the necessary Python libraries.
Navigate to the backend folder in your terminal or command prompt:
"cd my_awesome_website/my_chatbot_app"


(Recommended) Create and activate a Python virtual environment. This keeps your project's dependencies separate from your system.
python3 -m venv venv
.\venv\Scripts\Activate


Install the required libraries from the requirements.txt file:
"pip install -r requirements.txt"
(If you don't have a requirements.txt file, create one and add these lines: openai, flask, PyPDF2, python-dotenv, flask-cors)

**Step 4: Integrate the Frontend**
Open your website's main index.html file and add the following two lines right before the closing </body> tag.
...
    <link rel="stylesheet" href="ai_chat_widget_styles.css">
    <script src="ai_chat_widget_script.js"></script>
</body>
</html>


###Configuration
Add Your Knowledge: Replace the placeholder website_knowledge_base.pdf file inside the my_chatbot_app folder with your own PDF containing all the information you want the chatbot to know.
API Key: The first time you run the backend server, it will prompt you to enter your OpenRouter API key in the terminal. It will be securely saved in a .env file for future use.
Running the Application
Start the Backend Server: In your terminal, make sure you are in the my_chatbot_app directory and your virtual environment is active. Then run the server:
"python gemini_chatbot_backend_service.py"
You should see a message confirming that the server is running on http://127.0.0.1:5001.
View Your Website: Open your index.html file directly in your web browser (e.g., by double-clicking it). Do not navigate to the server URL in your browser. The chatbot bubble should appear in the bottom-right corner.
###Troubleshooting
Q: The chatbot says "Sorry, I'm having trouble connecting..."
A: Look at the terminal running the Python script. It will show the exact error. This is often caused by an invalid API key or an issue with your OpenRouter account.
Q: My terminal shows a 402 Payment Required or "token" error.
A: Your PDF file might be too large for OpenRouter's free tier. The request (PDF text + your question) is exceeding the token limit. The code already includes max_tokens=1024 to help with this, but a very large PDF can still cause issues. Try using a smaller PDF or upgrading your OpenRouter plan.
Q: I see a "404 Not Found" error when I go to http://127.0.0.1:5001 in my browser.
A: This is normal! The backend is an API, not a website. You must test the chatbot by opening your actual index.html file in your browser.
