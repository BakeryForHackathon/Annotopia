import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { createContext, useState, useContext, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import MainLayout from './layouts/MainLayout';
import OrderPage from './pages/OrderPage';
import NewRequestPage from './pages/NewRequestPage';
import ContractPage from './pages/ContractPage';
import TaskDetailPage from './pages/TaskDetailPage';
import TestPage from './pages/TestPage';
import TestResultPage from './pages/TestResultPage';
import CreateTestPage from './pages/CreateTestPage';
import CreateMasterTestPage from './pages/CreateMasterTestPage';
import AnnotationPage from './pages/AnnotationPage';

export const ApiContext = createContext(null);
export const UserContext = createContext(null);

const ProtectedRoutes = () => {
  const { usernameHash } = useContext(UserContext);
  if (!usernameHash) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};

function App() {
  const API_URL = 'https://myapp-backend-q7z0.onrender.com';
  const [usernameHash, setUsernameHash] = useState(() => localStorage.getItem('usernameHash') || '');

  useEffect(() => {
    if (usernameHash) localStorage.setItem('usernameHash', usernameHash);
    else localStorage.removeItem('usernameHash');
  }, [usernameHash]);

  return (
    <ApiContext.Provider value={API_URL}>
      <UserContext.Provider value={{ usernameHash, setUsernameHash }}>
        <Router>
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<LoginPage />} />

            <Route element={<ProtectedRoutes />}>
              <Route element={<MainLayout />}>
                <Route path="order" element={<OrderPage />} />
                <Route path="new-request" element={<NewRequestPage />} />
                <Route path="new-request/create-test" element={<CreateTestPage />} />
                <Route path="contract" element={<ContractPage />} />
                <Route path="task/:taskId" element={<TaskDetailPage />} />
                <Route path="task/:taskId/test" element={<TestPage />} />
                <Route path="task/:taskId/result" element={<TestResultPage />} />
                <Route path="task/:taskId/create-master-test" element={<CreateMasterTestPage />} />
                <Route path="task/:taskId/annotate" element={<AnnotationPage />} />
              </Route>
            </Route>
          </Routes>
        </Router>
      </UserContext.Provider>
    </ApiContext.Provider>
  );
}

export default App;
