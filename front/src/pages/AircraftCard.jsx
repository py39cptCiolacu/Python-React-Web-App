import React, { useState, useEffect } from 'react';
import "../styles/Card.css"; 

const AircraftCard = ({ aircraft, onClose }) => {
  const [aircraftDetails, setAircraftDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAircraftInfo = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/get_aircraft_info?serial_number=${aircraft.aircraft_serial_number}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch aircraft details');
        }

        const data = await response.json();
        setAircraftDetails(data); 
        setLoading(false);  
      } catch (error) {
        setError(error.message); 
        setLoading(false);
      }
    };

    fetchAircraftInfo();
  }, [aircraft.aircraft_serial_number]); 

  return (
    <div className="card">
      <button className="close-button" onClick={onClose}>X</button>
      <h3>Aircraft Details</h3>
      
      {loading && <p>Loading...</p>}
      
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {aircraftDetails && !loading && !error && (
        <>
          <p><strong>Serial Number:</strong> {aircraftDetails.serial_number}</p>
          <p><strong>Model:</strong> {aircraftDetails.model}</p>
          <p><strong>Manufacturer:</strong> {aircraftDetails.manufacturer}</p>
          <p><strong>Capacity:</strong> {aircraftDetails.capacity}</p>
          <p><strong>Configuration:</strong> {aircraftDetails.configuration}</p>
        </>
      )}
    </div>
  );
};

export default AircraftCard;
