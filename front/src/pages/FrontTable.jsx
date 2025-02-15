import React, { useState } from "react";
import Orders from "./Orders";
import Materials from "./Materials";
import Aircrafts from "./Aircrafts";
import Upload from "./Upload";
import "../styles/FrontTable.css"

export default function FrontTable() {
  
  const [activeTab, setActiveTab] = useState("orders");

  return (
    <div>
      {/*Header buttons*/}
      <div className="header">
        <button onClick={() => setActiveTab("orders")}>ORDERS</button>
        <button onClick={() => setActiveTab("materials")}>MATERIALS</button>
        <button onClick={() => setActiveTab("aircrafts")}>AIRCRAFTS</button>
      </div>

      {/*Table*/}
      <div className="content">
        {activeTab === "orders" && <Orders />}
        {activeTab === "materials" && <Materials />}
        {activeTab === "aircrafts" && <Aircrafts />}
      </div> 

      {/*Upload Buttons*/} 
      <Upload activeTab={activeTab}/>
    </div>

  );
}

