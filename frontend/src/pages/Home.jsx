
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatInput from '../components/ChatInput';

const Home = () => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (query.trim()) {
      navigate('/results');
    }
  };

  return (
    <div className="container">
      <h1 className="title">Michigan Alumni Finder</h1>
      <p className="subtitle">Search for alumni using natural language.</p>
      <ChatInput value={query} onChange={setQuery} onSubmit={handleSubmit} />
    </div>
  );
};

export default Home;
