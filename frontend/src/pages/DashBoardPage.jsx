import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from './DashboardPage.module.css';
import { useAuth } from '../hooks/useAuth';
import { RequestIcon, ListIcon, ProfileIcon } from '../components/Icons';

const DashboardPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth(); 
  const user = location.state?.user;

  useEffect(() => {
    if (!user) {
      navigate('/');
    }
  }, [user, navigate]);

  const handleNavigation = (path) => {
    navigate(path, { state: { user } });
  };

  if (!user) return null;

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

      <div className={styles.container}>
        <aside className={styles.sidebar}>
          <nav>
            <ul className={styles.menuList}>
              <li className={styles.menuItem} onClick={() => handleNavigation('/createrequest')}>
                <RequestIcon />
                <span>依頼する</span>
              </li>
              <li className={styles.menuItem} onClick={() => handleNavigation('/requestlist')}>
                <ListIcon />
                <span>依頼リスト</span>
              </li>
              <li className={styles.menuItem} onClick={() => handleNavigation('/profile')}>
                <ProfileIcon />
                <span>プロフィール</span>
              </li>
            </ul>
          </nav>
        </aside>

        <main className={styles.main}>
          <h1 className={styles.heading}>ダッシュボード</h1>
          <p className={styles.subheading}>ここから各機能へアクセスできます。</p>
          <section className={styles.cardSection}>
            <div className={styles.card} onClick={() => handleNavigation('/createrequest')}>
              <h2 className={styles.cardTitle}>新しい依頼</h2>
              <p className={styles.cardText}>アノテーション作業を新規に依頼します。</p>
            </div>
            <div className={styles.card} onClick={() => handleNavigation('/requestlist')}>
              <h2 className={styles.cardTitle}>発注済み依頼リスト</h2>
              <p className={styles.cardText}>進行中および完了した依頼を確認します。</p>
            </div>
          </section>
        </main>
      </div>
    </div>
    </div>
  );
};

export default DashboardPage;