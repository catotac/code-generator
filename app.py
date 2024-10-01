import os
from flask import Flask, request, jsonify, session, send_file, render_template
from uuid import uuid4
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Paths for the generated code
GENERATED_CODE_DIR = 'models/generated_code'  # Directory to store generated code files

# Chat histories and code storage
chat_histories = {}
code_storage = {}

# Load the Hugging Face model and tokenizer
MODEL_NAME = "distilgpt2"  # You can choose other models like "gpt2", "EleutherAI/gpt-neo-125M"
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

@app.route('/')
def home():
    return render_template('index.html')

def generate_chat_name(prompt):
    """Generates a chat name based on the user's initial input."""
    return "Chat_" + "_".join(prompt.split()[:3])  # Example: First three words of the prompt

def generate_code(prompt):
    """Generates a static code block for testing."""
    # Static code to simulate code generation
    generated_code = f"""
    this is a test code...
    
    ```python
    def greet(name):
        return f"Hello, {prompt}!"
    
    print(greet("World"))
    ```
    """
    return generated_code

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({"response": "Please provide an input"}), 400

    # Generate the hardcoded response (simulating code generation)
    generated_response = generate_code(user_input)

    # Store conversation history in session
    chat_id = session.get('chat_id')

    # Initialize a new chat session if it doesn't exist
    if not chat_id or chat_id not in chat_histories:
        chat_id = str(uuid4())  # Generate a new chat session ID
        session['chat_id'] = chat_id
        chat_histories[chat_id] = {
            "name": generate_chat_name(user_input),
            "messages": []
        }
        code_storage[chat_id] = []  # Initialize code storage for this session

    # Extract code if present
    code_block = extract_code(generated_response)

    # Append user input and generated response to the chat history
    chat_histories[chat_id]["messages"].append({
        "user": user_input,
        "response": generated_response,
        "code": code_block if code_block else None  # Save code separately if found
    })

    # If code is detected, store it
    if code_block:
        code_storage[chat_id].append(code_block)

    # Create a combined response with both text and code (if applicable)
    response = {
        "text": generated_response.replace(code_block, '').strip() if code_block else generated_response,
        "code": code_block
    }

    return jsonify(response)


def extract_code(response_text):
    """Extract code block from generated text (between ``` markers)."""
    code_start = response_text.find("```")
    code_end = response_text.rfind("```")
    if code_start != -1 and code_end != -1:
        # Remove the ``` markers and return the code inside
        return response_text[code_start + 3:code_end].strip()  # Extract code between the ``` markers
    return response_text.strip()  # If no code markers, return the full response

@app.route('/download_code', methods=['GET'])
def download_code():
    """Combine generated code blocks and return a single code file."""
    chat_id = session.get('chat_id')
    
    if not chat_id or chat_id not in code_storage or len(code_storage[chat_id]) == 0:
        return jsonify({"error": "No code to download."}), 400
    
    # Combine all code blocks into a single file
    file_name = f"generated_code_{chat_id}.txt"
    file_path = os.path.join(GENERATED_CODE_DIR, file_name)
    
    with open(file_path, 'w') as code_file:
        for code_block in code_storage[chat_id]:
            code_file.write(code_block + "\n\n")
    
    # Return the generated file for download
    return send_file(file_path, as_attachment=True)

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear current session chat and code storage."""
    chat_id = session.get('chat_id')
    if chat_id in chat_histories:
        del chat_histories[chat_id]
    if chat_id in code_storage:
        del code_storage[chat_id]
    session.pop('chat_id', None)
    return jsonify({"message": "Chat and code cleared."})

if __name__ == '__main__':
    if not os.path.exists(GENERATED_CODE_DIR):
        os.makedirs(GENERATED_CODE_DIR)
    app.run(debug=True)
