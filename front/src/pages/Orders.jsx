import React, { useState, useEffect } from "react";
import "../styles/TableView.css";

const Orders = () => {
  const [orders, setOrders] = useState([]); 
  const [currentPage, setCurrentPage] = useState(1); 
  const ordersPerPage = 10; 

  useEffect(() => {
    window.pywebview.api
      .order_get_all_orders()  
      .then((response) => setOrders(response)) 
      .catch((error) => console.error("Error fetching orders data:", error));
  }, []);

  const indexOfLastOrder = currentPage * ordersPerPage;
  const indexOfFirstOrder = indexOfLastOrder - ordersPerPage;
  const currentOrders = orders.slice(indexOfFirstOrder, indexOfLastOrder);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const totalPages = Math.ceil(orders.length / ordersPerPage);

  return (
    <div className="table-container">
      <h2>ORDERS</h2>
      {orders.length === 0 ? (
        <p>No orders data available</p> // Mesaj în caz că orders este gol
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
                  <td>{item.material_pn}</td>
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

export default Orders;
