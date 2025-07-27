import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
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
  const { userId } = useContext(UserContext);
  if (!userId) return <Navigate to="/login" replace />;
  return <MainLayout />;
};

function App() {
  const API_URL = 'https://myapp-backend-y8f2.onrender.com';
  // const API_URL = 'http://127.0.0.1:5001'
  const [userId, setUserId] = useState(() => localStorage.getItem('userId'));
  useEffect(() => {
    if (userId) localStorage.setItem('userId', userId);
    else localStorage.removeItem('userId');
  }, [userId]);

  return (
    <ApiContext.Provider value={API_URL}>
      <UserContext.Provider value={{ userId, setUserId }}>
        <Router>
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<LoginPage />} />

            <Route element={<ProtectedRoutes />}>
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
          </Routes>
        </Router>
      </UserContext.Provider>
    </ApiContext.Provider>
  );
}

export default App;