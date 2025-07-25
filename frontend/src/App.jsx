import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
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
// import ProfilePage from './pages/ProfilePage';     // プロフィールページ

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />

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
      </Routes>
    </Router>
  );
}

export default App;