
import React from 'react';

const ChatInput = ({ value, onChange, onSubmit }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSubmit();
    }
  };

  return (
    <div className="chat-input-container">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="e.g., Show me alumni at Google"
        className="chat-input"
      />
      <button onClick={onSubmit} className="send-button">Search</button>
    </div>
  );
};

export default ChatInput;
