import React, { useState, useEffect } from 'react';

const TimingAnalyzer = () => {
  const [timingData, setTimingData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch timing data from API
    fetch('/api/timing/report')
      .then(response => response.json())
      .then(data => {
        setTimingData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching timing data:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="timing-analyzer">
      <h1>Timing Analysis</h1>
      {timingData && (
        <div>
          <h2>Critical Paths</h2>
          <ul>
            {timingData.critical_paths.map((path, index) => (
              <li key={index}>{path.description} - WNS: {path.wns} ns</li>
            ))}
          </ul>
          
          <h2>Violations</h2>
          <ul>
            {timingData.violations.map((violation, index) => (
              <li key={index}>{violation.type}: WNS {violation.wns} ns</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default TimingAnalyzer;