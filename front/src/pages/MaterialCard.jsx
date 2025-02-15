import React, { useState, useEffect } from 'react';

const MaterialCard = ({ materialPN, onClose }) => {
  const [materialDetails, setMaterialDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMaterialInfo = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/get_material_info?material_part_number=${materialPN}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch material details');
        }

        const data = await response.json();
        setMaterialDetails(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchMaterialInfo();
  }, [materialPN]);

  return (
    <div className="card">
      <button className="close-button" onClick={onClose}>X</button>
      <h3>Material Details</h3>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {materialDetails && !loading && !error && (
        <>
          <p><strong>Material PN:</strong> {materialDetails.part_number}</p>
          <p><strong>Description:</strong> {materialDetails.name}</p>
          <p><strong>Quantity Available:</strong> {materialDetails.type}</p>
          <p><strong>Status:</strong> {materialDetails.weight}</p>
        </>
      )}
    </div>
  );
};

export default MaterialCard;
