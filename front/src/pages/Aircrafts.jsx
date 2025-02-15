import React from "react";
import "../styles/TableView.css"

const data = [
  { configuration: "Device A", model: "aa", manufacturer: "TechCorp", capacity: "500GB", serialNumber: "SN123456" },
  { configuration: "Device B", model: "Y200", manufacturer: "GigaTech", capacity: "1TB", serialNumber: "SN654321" },
  { configuration: "Device C", model: "Z300", manufacturer: "NanoInc", capacity: "2TB", serialNumber: "SN789123" },
  { configuration: "Device D", model: "W400", manufacturer: "MegaSystems", capacity: "5TB", serialNumber: "SN987654" },
];

const Aircrafts= () => {
  return (
    <div className="table-container">
      <h2>AIRCRAFTS</h2>
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
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.serialNumber}</td>
              <td>{item.model}</td>
              <td>{item.manufacturer}</td>
              <td>{item.capacity}</td>
              <td>{item.configuration}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Aircrafts;
