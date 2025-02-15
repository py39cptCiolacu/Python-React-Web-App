import React, { useState, useEffect } from "react";
import "../styles/TableView.css";

const Aircrafts = () => {
  const [aircrafts, setAircrafts] = useState([]); 
  const [currentPage, setCurrentPage] = useState(1); 
  const aircraftsPerPage = 10; 

  useEffect(() => {
    window.pywebview.api
      .aircraft_get_all_aircrafts() 
      .then((response) => setAircrafts(response)) 
      .catch((error) => console.error("Error fetching aircraft data:", error));
  }, []);

  const indexOfLastAircraft = currentPage * aircraftsPerPage;
  const indexOfFirstAircraft = indexOfLastAircraft - aircraftsPerPage;
  const currentAircrafts = aircrafts.slice(indexOfFirstAircraft, indexOfLastAircraft);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const totalPages = Math.ceil(aircrafts.length / aircraftsPerPage);

  return (
    <div className="table-container">
      <h2>AIRCRAFTS</h2>
      {aircrafts.length === 0 ? (
        <p>No aircraft data available</p> // Mesaj în caz că aircrafts este gol
      ) : (
        <>
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
              {currentAircrafts.map((item, index) => (
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

          {/* Butoane de paginare */}
          <div className="pagination">
            <button
              onClick={() => paginate(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => paginate(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Aircrafts;
