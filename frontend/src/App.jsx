import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import MainLayout from './pages/MainLayout';
import NewRequestPage from './pages/NewRequestPage';

function App() {
  return (
    <Router>
      <Routes>
        {/* ログインページは独立したルート */}
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />

        {/* ★ MainLayoutを適用するページのグループ */}
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/new-request" element={<NewRequestPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;