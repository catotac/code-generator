from flask import Flask, request, jsonify, render_template, session
from uuid import uuid4
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

chat_histories = {}

def run_llama_cpp(prompt):
    """
    Function to call llama.cpp and generate a response based on the prompt.
    This assumes llama.cpp is set up with a command-line interface.
    """
    # Command to invoke llama.cpp (adjust paths and parameters as necessary)
    command = [
        "/path/to/llama.cpp",  # Replace with the actual llama.cpp executable path
        "--model", "/path/to/model.bin",  # Path to your LLaMA model
        "--prompt", prompt,
        "--n_predict", "512"  # Set to control the number of tokens to predict
    ]

    # Call the subprocess
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"llama.cpp failed with error: {result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"Error running llama.cpp: {e}")
        return "An error occurred while generating code."

def generate_chat_name(prompt):
    """Generates a chat name based on the user's initial input."""
    if "python" in prompt.lower() and "code" in prompt.lower():
        return "Python Code Generation"
    elif "java" in prompt.lower():
        return "Java Code Discussion"
    elif "sql" in prompt.lower():
        return "SQL Query Discussion"
    return f"Chat on {prompt[:30]}..."  # Fallback to the first few words of the input

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    user_input = data.get("input", "")
    
    if not user_input:
        return jsonify({"response": "Please provide an input"}), 400
    
    # Generate a response using llama.cpp
    generated_response = run_llama_cpp(user_input)
    
    # Store conversation history in session
    chat_id = session.get('chat_id')
    
    if not chat_id:
        chat_id = str(uuid4())  # Generate a new chat session ID
        session['chat_id'] = chat_id
        chat_histories[chat_id] = {
            "name": generate_chat_name(user_input),
            "messages": []
        }
    
    chat_histories[chat_id]["messages"].append({
        "user": user_input,
        "llama": generated_response
    })
    
    return jsonify({"response": generated_response})

@app.route('/chats', methods=['GET'])
def get_chat_history():
    """Returns the chat history of the current session."""
    chat_id = session.get('chat_id')
    if chat_id and chat_id in chat_histories:
        return jsonify(chat_histories[chat_id]["messages"])
    return jsonify([])

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear current session chat."""
    chat_id = session.get('chat_id')
    if chat_id in chat_histories:
        del chat_histories[chat_id]
    session.pop('chat_id', None)
    return jsonify({"message": "Chat cleared."})

@app.route('/all_chats', methods=['GET'])
def get_all_chats():
    """Returns all available chat sessions for displaying on the left."""
    return jsonify({"chats": [{"id": cid, "name": cdata["name"]} for cid, cdata in chat_histories.items()]})

@app.route('/load_chat/<chat_id>', methods=['GET'])
def load_chat(chat_id):
    """Load a specific chat history."""
    if chat_id in chat_histories:
        session['chat_id'] = chat_id  # Load the selected chat session
        return jsonify(chat_histories[chat_id]["messages"])
    return jsonify({"error": "Chat not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
