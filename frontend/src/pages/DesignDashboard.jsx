import React, { useState, useEffect } from 'react';

const DesignDashboard = () => {
  const [designs, setDesigns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch designs from API
    fetch('/api/designs')
      .then(response => response.json())
      .then(data => {
        setDesigns(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching designs:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>FPGA Design Dashboard</h1>
      <div className="design-list">
        {designs.map(design => (
          <div key={design.id} className="design-card">
            <h2>{design.name}</h2>
            <p>Status: {design.status}</p>
            <p>Created: {design.created_at}</p>
            <button onClick={() => window.location.href = `/design/${design.id}`}>
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DesignDashboard;