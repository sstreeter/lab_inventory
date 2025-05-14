import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/UploadPage';
const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/upload" element={<UploadPage />} />
    </Routes>
  </Router>
);
export default App;