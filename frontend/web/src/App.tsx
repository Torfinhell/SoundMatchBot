import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AdminPanel from './pages/AdminPanel';
import Rankings from './pages/Rankings';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Rankings />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;