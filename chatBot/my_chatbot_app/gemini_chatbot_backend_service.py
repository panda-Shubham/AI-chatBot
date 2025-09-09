import os
# Import the OpenAI library instead of Google's
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from dotenv import load_dotenv, set_key

# --- Initial Setup ---
env_file_path = ".env"
if not os.path.exists(env_file_path):
    open(env_file_path, "w").close()

load_dotenv()

# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app)

# --- Global variable to hold PDF content ---
website_context = ""

# --- Helper Functions ---
def load_and_process_pdf(pdf_path="website_knowledge_base.pdf"):
    """Reads the provided PDF and extracts the text content."""
    global website_context
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        website_context = text
        print("Successfully loaded and processed the PDF.")
        if not text:
            print("Warning: The PDF is empty or could not be read.")
    except Exception as e:
        website_context = ""
        print(f"Error reading the PDF file: {e}")
        print("Please make sure 'website_knowledge_base.pdf' is in the same directory.")

# --- THIS ENTIRE FUNCTION IS REPLACED ---

def get_ai_response(api_key, context, question):
    """Interacts with the OpenRouter API to get an answer."""
    try:
        # Point the client to OpenRouter's API endpoint
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # The prompt structure for OpenAI-compatible APIs
        prompt_messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful and friendly AI assistant for a website. "
                    "Your role is to answer customer questions based ONLY on the information provided in the context. "
                    "If the answer is not in the context, say 'I'm sorry, I don't have that information.'"
                    " make sure to use better-looking responses (" " signs bold text, lists, etc.) and makes your chatbot answe appear more professional."
                    " don't use star * sign "
                
                )
            },
            {
                "role": "user", 
                "content": (
                    "--- Website Information Context ---\n"
                    f"{context}\n"
                    "---------------------------------\n\n"
                    f"Based on the context above, answer this question: {question}"
                )
            }
        ]

        # Make the API call - check this block carefully
        completion = client.chat.completions.create(
            model="google/gemini-pro-1.5", 
            messages=prompt_messages,    # <-- THIS LINE IS CRITICAL AND MUST BE CORRECT
            max_tokens=1024         
        )
        return completion.choices[0].message.content

    except Exception as e:
        # This will now print the specific error from OpenRouter
        print(f"An error occurred with the OpenRouter API: {e}")
        return "Sorry, I'm having trouble connecting to the AI service right now."

@app.route('/')
def index():
    return "<h1>Chatbot Backend is Running</h1><p>This is an API endpoint. Please access the chatbot through your website's main HTML file.</p>"

@app.route('/api/v1/chatbot_query', methods=['POST'])
def handle_chatbot_query():
    data = request.get_json()
    user_question = data.get('question')

    if not user_question:
        return jsonify({'error': 'No question provided.'}), 400

    # Using a more generic variable name for the API key
    api_key = os.getenv("AI_PROVIDER_API_KEY")
    if not api_key:
        return jsonify({'error': 'API key is not configured on the server.'}), 500
    
    if not website_context:
        return jsonify({'answer': "I'm sorry, my knowledge base hasn't been set up yet."})

    # Call the new, corrected function
    answer = get_ai_response(api_key, website_context, user_question)
    return jsonify({'answer': answer})

# --- Main Execution ---
if __name__ == '__main__':
    # Prompt for the OpenRouter key now
    if not os.getenv("AI_PROVIDER_API_KEY"):
        api_key_from_input = input("Please enter your OpenRouter API Key: ")
        # Save it with the new name
        set_key(env_file_path, "AI_PROVIDER_API_KEY", api_key_from_input)
        load_dotenv()
        print("OpenRouter API Key has been saved.")

    load_and_process_pdf()

    print("Backend server is running. Ready to receive requests from OpenRouter.")
    app.run(port=5001, debug=False)