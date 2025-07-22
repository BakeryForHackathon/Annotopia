import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import MainLayout from './layouts/MainLayout';
import OrderPage from './pages/OrderPage'; // 新しい依頼ページ
import NewRequestPage from './pages/NewRequestPage';
import ContractPage from './pages/ContractPage';   // 依頼リストページ
import TaskDetailPage from './pages/TaskDetailPage';
import TestPage from './pages/TestPage';
import TestResultPage from './pages/TestResultPage';
// import ProfilePage from './pages/ProfilePage';     // プロフィールページ

function App() {
  return (
    <Router>
      <Routes>
        {/* ログインページは独立したルート */}
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />

        {/* ★ MainLayoutを適用するページのグループ */}
        <Route element={<MainLayout />}>
          <Route path="order" element={<OrderPage />} />
          <Route path="new-request" element={<NewRequestPage />} />
          <Route path="contract" element={<ContractPage />} />
          <Route path="task/:taskId" element={<TaskDetailPage />} />
          <Route path="task/:taskId/test" element={<TestPage />} />
          <Route path="task/:taskId/result" element={<TestResultPage />} /> 
          {/* <Route path="profile" element={<ProfilePage />} /> */}
        </Route>
      </Routes>
    </Router>
  );
}

export default App;