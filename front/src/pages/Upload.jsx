import React from "react";
import "../styles/Upload.css";

export default function Upload({ activeTab }) {
  const handleUpload = () => {
    alert(`Uploading file for: ${activeTab}`);
    // Aici ai putea trimite la API, folosind activeTab ca identificator
  };

  return (
    <div className="upload-container">
      <button className="upload-btn" onClick={handleUpload}>
        Upload {activeTab.toUpperCase()} File
      </button>
    </div>
  );
}