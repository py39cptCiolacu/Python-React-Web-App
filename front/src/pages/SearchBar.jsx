import React from "react";

const SearchBar = ({ onSearchChange }) => {
  const [aircraftSerialNumber, setAircraftSerialNumber] = React.useState("");
  const [materialPN, setMaterialPN] = React.useState("");
  const [status, setStatus] = React.useState("All");
  const [startDate, setStartDate] = React.useState(""); // Start date
  const [endDate, setEndDate] = React.useState(""); // End date

  const handleSearchChange = () => {
    onSearchChange(aircraftSerialNumber, materialPN, status, startDate, endDate);
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={aircraftSerialNumber}
        onChange={(e) => setAircraftSerialNumber(e.target.value)}
        placeholder="Aircraft Serial Number"
        className="search-input"
      />
      <input
        type="text"
        value={materialPN}
        onChange={(e) => setMaterialPN(e.target.value)}
        placeholder="Material PN"
        className="search-input"
      />
      <select value={status} onChange={(e) => setStatus(e.target.value)} className="search-input">
        <option value="All">All</option>
        <option value="Arrived">Arrived</option>
        <option value="Pending">Pending</option>
        <option value="Requested">Requested</option>
      </select>
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
        className="search-input"
        placeholder="Start Date"
      />
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
        className="search-input"
        placeholder="End Date"
      />
      <button onClick={handleSearchChange}>Search</button>
    </div>
  );
};

export default SearchBar;
