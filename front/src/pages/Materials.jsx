import React, { useState, useEffect } from "react";
import "../styles/TableView.css";

const Materials = () => {
  const [materials, setMaterials] = useState([]); // Inițializare ca array gol

  useEffect(() => {
    window.pywebview.api
      .material_get_all_materials() // Apelează funcția API care aduce datele
      .then((response) => setMaterials(response)) // Salvează datele în state-ul materials
      .catch((error) => console.error("Error fetching materials data:", error));
  }, []);

  return (
    <div className="table-container">
      <h2>MATERIALS</h2>
      {materials.length === 0 ? (
        <p>No materials data available</p> // Mesaj în caz că materials este gol
      ) : (
        <table>
          <thead>
            <tr>
              <th>Product Number</th>
              <th>Name</th>
              <th>Type</th>
              <th>Weight</th>
            </tr>
          </thead>
          <tbody>
            {materials.map((item, index) => (
              <tr key={index}>
                <td>{item.part_number}</td>
                <td>{item.name}</td>
                <td>{item.type}</td>
                <td>{item.weight}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Materials;
