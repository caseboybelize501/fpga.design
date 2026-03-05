import React, { useState, useEffect } from 'react';

const RTLMemory = () => {
  const [memoryData, setMemoryData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch memory data from API
    fetch('/api/memory/timing')
      .then(response => response.json())
      .then(data => {
        setMemoryData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching memory data:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="memory-viewer">
      <h1>RTL Memory</h1>
      {memoryData && (
        <div>
          <h2>Timing Failures</h2>
          <ul>
            {memoryData.timing_failures.map((failure, index) => (
              <li key={index}>{failure.construct} on {failure.device} at {failure.freq} MHz</li>
            ))}
          </ul>
          
          <h2>RTL Patterns</h2>
          <ul>
            {memoryData.rtl_patterns.map((pattern, index) => (
              <li key={index}>{pattern.name} meets timing on {pattern.device}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RTLMemory;