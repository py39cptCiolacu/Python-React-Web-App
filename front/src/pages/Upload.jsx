import React, { useState } from "react";
import "../styles/Upload.css";

export default function Upload({ activeTab, onUploadSuccess }) {
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

    try {
      let response;
      // const formData = new FormData();
      // formData.append("file", filePath);

      if (activeTab === "aircrafts") {
        const formData = { file: "C:\\Users\\dciol\\OneDrive\\Desktop\\aircraft.xlsx" };
        response = await window.pywebview.api.aircraft_add_aircrafts_from_file(formData);
      } else if (activeTab === "orders") {
        const formData = { file: "C:\\Users\\dciol\\OneDrive\\Desktop\\order.xlsx" };
        response = await window.pywebview.api.order_add_orders_from_file(formData);
      } else if (activeTab === "materials") {
        const formData = { file: "C:\\Users\\dciol\\OneDrive\\Desktop\\material.xlsx" };
        response = await window.pywebview.api.material_add_materials_from_file(formData);
      }

      if (response.success) {
        console.log("File uploaded successfully:", response);
        alert("File uploaded successfully!");
        onUploadSuccess();
      } else {
        // Afișează mesajul exact de eroare din backend
        console.error("Error uploading file:", response.error);
        alert(`Error: ${response.error || "Unknown error"}`);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert(`Error uploading file: ${error.message || "Unknown error"}`);
    }
  };

  return (
    <div className="upload-container">
      <input type="file" onChange={handleFileChange} className="file-input" />
      <button className="upload-btn" onClick={handleUpload}>
        Upload {activeTab.toUpperCase()} File
      </button>
    </div>
  );
}
