// Wait for the DOM to load before attaching the event listener
document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.getElementById('send-button');
    
    // Attach the event listener to the "Send" button
    sendButton.addEventListener('click', function() {
        console.log("Button clicked!"); // This should log when the button is clicked
        sendMessage();
    });
});

function sendMessage() {
    const inputBox = document.getElementById('user-input');
    const chatArea = document.getElementById('chat-area');
    const userInput = inputBox.value;

    // Avoid sending empty messages
    if (userInput.trim() === "") {
        console.log("Empty message, ignoring.");
        return;
    }

    // Append the user's message to the chat area
    const userMessage = document.createElement('div');
    userMessage.textContent = `You: ${userInput}`;
    userMessage.classList.add('message', 'user');
    chatArea.appendChild(userMessage);

    // Clear the input box after the message is sent
    inputBox.value = '';

    // Log before sending to the server
    console.log("Sending message to server:", userInput);

    // Send the message to the Flask server
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display the response from the server in the chat area
        const llamaResponse = document.createElement('div');
        llamaResponse.textContent = `LLaMA: ${data.response}`;
        llamaResponse.classList.add('message', 'llama');
        chatArea.appendChild(llamaResponse);

        // Auto-scroll to the bottom of the chat area
        chatArea.scrollTop = chatArea.scrollHeight;
        console.log("Response from server:", data.response);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
