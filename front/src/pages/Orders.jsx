import React, { useState, useEffect } from "react";
import "../styles/TableView.css"

const Orders = () => {
  const [orders, setOrders] = useState([]); // Inițializare ca array gol

  useEffect(() => {
    window.pywebview.api
      .order_get_all_orders()  // Înlocuiește cu apelul corect pentru comenzile tale
      .then((response) => setOrders(response)) // Salvează datele în orders
      .catch((error) => console.error("Error fetching orders data:", error));
  }, []);

  return (
    <div className="table-container">
      <h2>ORDERS</h2>
      {orders.length === 0 ? (
        <p>No orders data available</p> // Mesaj în caz că orders este gol
      ) : (
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
            {orders.map((item, index) => (
              <tr key={index}>
                <td>{item.aircraft_serial_number}</td>
                <td>{item.material_pn}</td>
                <td>{item.arrival_date}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Orders;
