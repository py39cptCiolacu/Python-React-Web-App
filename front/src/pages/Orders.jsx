import React, { useState, useEffect } from "react";
import "../styles/TableView.css";
import SearchBar from "./SearchBar"; // Importăm SearchBar

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const ordersPerPage = 10;

  useEffect(() => {
    window.pywebview.api
      .order_get_all_orders()
      .then((response) => {
        setOrders(response);
        setFilteredOrders(response); // Set initial filtered orders
      })
      .catch((error) => console.error("Error fetching orders data:", error));
  }, []);

  const handleSearchChange = (aircraftSerialNumber, materialPN, status, startDate, endDate) => {
    let filtered = orders;

    if (aircraftSerialNumber) {
      filtered = filtered.filter((order) =>
        order.aircraft_serial_number.toLowerCase().includes(aircraftSerialNumber.toLowerCase())
      );
    }

    if (materialPN) {
      filtered = filtered.filter((order) =>
        order.material_part_number.toLowerCase().includes(materialPN.toLowerCase())
      );
    }

    if (status !== "All") {
      filtered = filtered.filter((order) => order.status === status);
    }

    // Filtrarea pe baza datei
    if (startDate) {
      filtered = filtered.filter((order) => new Date(order.arrival_date) >= new Date(startDate));
    }
    if (endDate) {
      filtered = filtered.filter((order) => new Date(order.arrival_date) <= new Date(endDate));
    }

    setFilteredOrders(filtered);
    setCurrentPage(1); // Reset page to 1 after filtering
  };

  const indexOfLastOrder = currentPage * ordersPerPage;
  const indexOfFirstOrder = indexOfLastOrder - ordersPerPage;
  const currentOrders = filteredOrders.slice(indexOfFirstOrder, indexOfLastOrder);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const totalPages = Math.ceil(filteredOrders.length / ordersPerPage);

  return (
    <div className="table-container">
      <h2>ORDERS</h2>
      
      {/* Componente de căutare */}
      <SearchBar onSearchChange={handleSearchChange} />

      {filteredOrders.length === 0 ? (
        <p>No orders data available</p> // Mesaj în caz că filteredOrders este gol
      ) : (
        <>
          <table>
            <thead>
              <tr>
                <th>Aircraft Serial Number</th>
                <th>Material PN</th>
                <th>Arrival Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {currentOrders.map((item, index) => (
                <tr key={index}>
                  <td>{item.aircraft_serial_number}</td>
                  <td>{item.material_part_number}</td>
                  <td>{item.arrival_date}</td>
                  <td>{item.status}</td>
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
            <span>
              Page {currentPage} of {totalPages}
            </span>
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

export default Orders;