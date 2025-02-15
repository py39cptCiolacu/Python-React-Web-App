import React, { useState } from "react";
import "../styles/Upload.css";

export default function Upload({ activeTab, onUploadSuccess }) {
  const [filePath, setFilePath] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

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

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", filePath);

      let url = `http://localhost:5000/upload/${activeTab}`;
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        console.log("File uploaded successfully:", result);
        alert("File uploaded successfully!");
        onUploadSuccess();
      } else {
        // Afișează mesajul exact de eroare din backend
        console.error("Error uploading file:", result.error);
        alert(`Error: ${result.error || "Unknown error"}`);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert(`Error uploading file: ${error.message || "Unknown error"}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload {activeTab.toUpperCase()} File</h2>
      <input
        type="file"
        onChange={handleFileChange}
        className="file-input"
        disabled={isUploading}
      />
      <button
        className="upload-btn"
        onClick={handleUpload}
        disabled={isUploading}
      >
        {isUploading ? "Uploading..." : "Upload File"}
      </button>
    </div>
  );
}
