import React from 'react';

function ChatHistory() {
    return (
        <div className="chat-history-container">
            <h3>Chat History</h3>
            {/* This can be populated dynamically based on stored history */}
            <ul>
                <li>Chat Session 1</li>
                <li>Chat Session 2</li>
                <li>Chat Session 3</li>
            </ul>
        </div>
    );
}

export default ChatHistory;
