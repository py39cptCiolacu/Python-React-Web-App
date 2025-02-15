import React from "react";
import "../styles/TableView.css"

const data = [
  { name: "Device A", model: "X100", manufacturer: "TechCorp", capacity: "500GB", serialNumber: "SN123456" },
  { name: "Device B", model: "Y200", manufacturer: "GigaTech", capacity: "1TB", serialNumber: "SN654321" },
  { name: "Device C", model: "Z300", manufacturer: "NanoInc", capacity: "2TB", serialNumber: "SN789123" },
  { name: "Device D", model: "W400", manufacturer: "MegaSystems", capacity: "5TB", serialNumber: "SN987654" },
];

const Materials = () => {
  return (
    <div className="table-container">
      <h2>MATERIALS</h2>
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
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.name}</td>
              <td>{item.model}</td>
              <td>{item.manufacturer}</td>
              <td>{item.capacity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Materials;
