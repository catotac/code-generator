import React, { useEffect } from 'react';
import Prism from 'prismjs';
import 'prismjs/themes/prism-okaidia.css';  // You can choose any theme you prefer
import './CodeBlock.css';

function CodeBlock({ code }) {
    useEffect(() => {
        Prism.highlightAll();  // Highlight code after rendering
    }, [code]);

    const handleCopy = () => {
        navigator.clipboard.writeText(code);
        alert("Code copied to clipboard!");
    };

    const handleDownload = () => {
        const element = document.createElement("a");
        const file = new Blob([code], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = "generated_code.py";  // Default file name
        document.body.appendChild(element);  // Required for Firefox
        element.click();
    };

    return (
        <div className="code-block-container">
            <div className="code-block-header">
                <button onClick={handleCopy} className="copy-button">Copy</button>
            </div>
            <pre className="code-block">
                <code className="language-python">{code}</code>  {/* Specify language for PrismJS */}
            </pre>
        </div>
    );
}

export default CodeBlock;
