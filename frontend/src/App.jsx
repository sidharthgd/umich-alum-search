
import React, { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [submitted, setSubmitted] = useState(false);

  const handleSearch = async () => {
    setSubmitted(true);
    const res = await fetch(`http://localhost:5000/hybrid_search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data);
  };

  return (
    <div className="min-h-screen bg-blue-50 p-8 text-center">
      <h1 className="text-4xl font-bold text-blue-900 mb-6">🎓 Michigan Alumni Search</h1>
      <div className="flex justify-center mb-6">
        <input
          type="text"
          placeholder="Type a query like 'Who worked at Meta?'"
          className="w-2/3 px-4 py-2 border border-blue-300 rounded-l-lg focus:outline-none"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="bg-maize-500 hover:bg-maize-600 text-blue-900 font-bold px-4 py-2 rounded-r-lg"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>

      {submitted && results.length === 0 && <p className="text-blue-700">No results found.</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 px-4">
        {results.map((alum, index) => (
          <div key={index} className="bg-white shadow-md rounded-lg p-4 text-left border border-blue-200">
            <h2 className="text-xl font-semibold text-blue-900">{alum.name}</h2>
            <p className="text-blue-700">🎓 {alum.major}</p>
            <p className="text-blue-700">💼 {alum.current_position} at {alum.current_company}</p>
            <p className="text-blue-600 text-sm">📜 Previously: {alum.previous_companies}</p>
            <a
              href={alum.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-800 font-medium underline mt-2 inline-block"
            >
              LinkedIn Profile
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
