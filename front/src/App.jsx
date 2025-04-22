import { Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Upload from './pages/Upload';
import Products from './pages/ProductionList';
import ProductionDetail from './pages/ProductionDetail';
import MeusCertificados from './pages/MyCertificates';
import { useState } from 'react';
import LoginModal from './components/LoginModal';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [showLogin, setShowLogin] = useState(false);

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setShowLogin(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken('');
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <Navbar onLogin={() => setShowLogin(true)} onLogout={handleLogout} isAuthenticated={!!token} />
      <LoginModal open={showLogin} onClose={() => setShowLogin(false)} onLoginSuccess={handleLogin} />
      <Routes>
        <Route path="/" element={<Products />} />
        <Route path="/certificados" element={<Products />} />
        <Route path="/upload" element={token ? <Upload /> : <Navigate to="/" />} />
        <Route path="/meus-certificados" element={token ? <MeusCertificados /> : <Navigate to="/" />} />
        <Route path="/producao/:hash" element={<ProductionDetail />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  );
}
