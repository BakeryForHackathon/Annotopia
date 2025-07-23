import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from './RequestListPage.module.css';
import { useAuth } from '../hooks/useAuth'; 
import api from '../api/axiosConfig';

const mockRequests = [
  { id: 1, title: '猫の画像のセグメンテーション', date: '2024-07-20', status: 'Completed' },
  { id: 2, title: '道路標識のバウンディングボックス作成', date: '2024-07-21', status: 'In Progress' },
  { id: 3, title: '医療画像の異常検知', date: '2024-07-22', status: 'In Progress' },
  { id: 4, title: '領収書のテキストOCR', date: '2024-07-15', status: 'Completed' },
  { id: 5, title: '自動運転用の歩行者検出', date: '2024-07-23', status: 'Pending' },
];

const RequestListPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const user = location.state?.user;

  useEffect(() => {
    if (!user) {
      navigate('/');
    }
  }, [user, navigate]);

  const getStatusClass = (status) => {
    const statusClassMap = {
      'In Progress': styles.statusInProgress,
      'Completed': styles.statusCompleted,
      'Pending': styles.statusPending,
    };
    return statusClassMap[status] || '';
  };

  const navigateToDashboard = () => {
    navigate('/dashboard', { state: { user } });
  };

  // if (!user) return null;

  return (
    <div className={styles.background}>
      <div className={styles.pageContainer}>
        <header className={styles.header}>
          <div className={styles.logoContainer}>
            <img src="/logo.png" alt="ANNOTOPIA Logo" className={styles.logo} />
            <span className={styles.logoText}>ANNOTOPIA</span>
          </div>
          <div className={styles.userMenu}>
            <span className={styles.username}>こんにちは、{user.username}さん</span>
            <button onClick={logout} className={styles.logoutButton}>ログアウト</button>
          </div>
        </header>

        <main className={styles.main}>
          <div className={styles.headingContainer}>
            <h1 className={styles.heading}>発注済み依頼リスト</h1>
            <button onClick={navigateToDashboard} className={styles.dashboardButton}>ダッシュボードに戻る</button>
          </div>

          <div className={styles.requestList}>
            {mockRequests.map(({ id, title, date, status }) => (
              <div key={id} className={styles.requestItem}>
                <div className={styles.requestDetails}>
                  <h2 className={styles.requestTitle}>{title}</h2>
                  <p className={styles.requestDate}>依頼日: {date}</p>
                </div>
                <div className={`${styles.requestStatus} ${getStatusClass(status)}`}>{status}</div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
};

export default RequestListPage;
