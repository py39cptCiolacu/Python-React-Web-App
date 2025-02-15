import React, { useState } from "react";
import "../styles/Upload.css";

export default function Upload({ activeTab }) {
  const [filePath, setFilePath] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFilePath(file); 
    }
  };

  const handleUpload = async () => {
    if (!filePath) {
      alert("No file selected!");
      return;
    }

    // ------------------------ MUST CHANGE------------
    try {
      if (activeTab == "aircrafts"){
        var formData = {"file": "C:\\Users\\dciol\\OneDrive\\Desktop\\aircraft.xlsx"};
        const response = await window.pywebview.api.aircraft_add_aircrafts_from_file(formData); 
      }
      else if (activeTab == "orders"){
        var formData = {"file": "C:\\Users\\dciol\\OneDrive\\Desktop\\order.xlsx"};
        const response = await window.pywebview.api.order_add_orders_from_file(formData); 
      }
      else if (activeTab == "materials"){
        var formData = {"file": "C:\\Users\\dciol\\OneDrive\\Desktop\\material.xlsx"};
        const response = await window.pywebview.api.material_add_materials_from_file(formData); 
      }
    // ------------------------------------
      console.log("File uploaded successfully:", response);
      alert("File uploaded successfully!");
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file.");
    }
  };

  return (
    <div className="upload-container">
      <input
        type="file"
        onChange={handleFileChange}
        className="file-input"
      />
      <button className="upload-btn" onClick={handleUpload}>
        Upload {activeTab.toUpperCase()} File
      </button>
    </div>
  );
}
