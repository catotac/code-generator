import React, { useState } from 'react';
import axios from 'axios';
import CodeBlock from './CodeBlock';
import ChatHistory from './ChatHistory';
import './ChatBox.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function ChatBox() {
    const [input, setInput] = useState('');
    const [responseParts, setResponseParts] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleGenerate = async () => {
        setLoading(true);
        try {
            const response = await axios.post(`${BACKEND_URL}/api/generate`, { input });
            setResponseParts(response.data.response);  // Expect array of text and code parts
        } catch (error) {
            console.error('Error generating code:', error);
            setResponseParts([{ type: 'text', content: 'Error generating response. Please try again.' }]);
        }
        setLoading(false);
    };

    return (
        <div className="chat-container">
            <div className="chat-history">
                <ChatHistory />
            </div>
            <div className="chat-box">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter your instructions here"
                />
                <button onClick={handleGenerate} disabled={loading}>
                    {loading ? 'Generating...' : 'Generate'}
                </button>

                <div className="response-section">
                    {responseParts.map((part, index) => (
                        <div key={index}>
                            {part.type === 'text' ? (
                                <p>{part.content}</p>
                            ) : (
                                <CodeBlock code={part.content} />
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default ChatBox;
