import React from "react";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

import AdminLayout from "./layouts/Admin.js";

import "./assets/plugins/nucleo/css/nucleo.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "./assets/scss/dashboard-react.scss";
//import "./App.css";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/home/*" element={<AdminLayout />} />
          <Route path="*" element={<Navigate to="/home/index" replace />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
