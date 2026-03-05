import React, { useState, useEffect } from 'react';

const SimWaveforms = () => {
  const [waveform, setWaveform] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch waveform data from API
    fetch('/api/simulation/waveform')
      .then(response => response.json())
      .then(data => {
        setWaveform(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching waveform:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="waveform-viewer">
      <h1>Simulation Waveforms</h1>
      {waveform && (
        <div>
          <img src={waveform.path} alt="Waveform" />
          <p>{waveform.description}</p>
        </div>
      )}
    </div>
  );
};

export default SimWaveforms;