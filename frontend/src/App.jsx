
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Results from './pages/Results';

const App = () => (
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/results" element={<Results />} />
  </Routes>
);

export default App;
