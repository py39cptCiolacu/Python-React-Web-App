import React, { useState, useEffect } from "react";
import "../styles/TableView.css";

const Materials = () => {
  const [materials, setMaterials] = useState([]); 
  const [currentPage, setCurrentPage] = useState(1); 
  const materialsPerPage = 10; 
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    fetch(`${API_BASE_URL}/get_all_materials`)
      .then((response) => response.json())
      .then((data) => setMaterials(data))
      .catch((error) => console.error("Error fetching materials data:", error));
  }, []);
  

  const indexOfLastMaterial = currentPage * materialsPerPage;
  const indexOfFirstMaterial = indexOfLastMaterial - materialsPerPage;
  const currentMaterials = materials.slice(indexOfFirstMaterial, indexOfLastMaterial);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const totalPages = Math.ceil(materials.length / materialsPerPage);

  return (
    <div className="table-container">
      <h2>MATERIALS</h2>
      {materials.length === 0 ? (
        <p>No materials data available</p> // Mesaj în caz că materials este gol
      ) : (
        <>
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
              {currentMaterials.map((item, index) => (
                <tr key={index}>
                  <td>{item.part_number}</td>
                  <td>{item.name}</td>
                  <td>{item.type}</td>
                  <td>{item.weight}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Butoane de paginare */}
          <div className="pagination">
            <button
              onClick={() => paginate(currentPage - 1)}
              disabled={currentPage === 1}
              aria-label="Previous page"
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => paginate(currentPage + 1)}
              disabled={currentPage === totalPages}
              aria-label="Next page"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Materials;
