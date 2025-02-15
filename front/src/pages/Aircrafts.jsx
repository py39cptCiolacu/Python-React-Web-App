import React, { useState, useEffect } from "react";
import "../styles/TableView.css"

const Aircrafts = () => {
  const [aircrafts, setAircrafts] = useState([]); // Inițializare ca array gol

  useEffect(() => {
    window.pywebview.api
      .aircraft_get_all_aircrafts()
      .then((response) => setAircrafts(response)) // Salvează datele în aircrafts
      .catch((error) => console.error("Error fetching aircraft data:", error));
  }, []);

  return (
    <div className="table-container">
      <h2>AIRCRAFTS</h2>
      {aircrafts.length === 0 ? (
        <p>No aircraft data available</p> // Mesaj în caz că aircrafts este gol
      ) : (
        <table>
          <thead>
            <tr>
              <th>Serial Number</th>
              <th>Model</th>
              <th>Manufacturer</th>
              <th>Capacity</th>
              <th>Configuration</th>
            </tr>
          </thead>
          <tbody>
            {aircrafts.map((item, index) => (
              <tr key={index}>
                <td>{item.serial_number}</td>
                <td>{item.model}</td>
                <td>{item.manufacturer}</td>
                <td>{item.capacity}</td>
                <td>{item.configuration}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Aircrafts;
