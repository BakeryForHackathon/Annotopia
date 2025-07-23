import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth'; 
import styles from './ProfilePage.module.css';

const ProfilePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const user = location.state?.user;

  const [username, setUsername] = useState(user?.username || '');
  const [email, setEmail] = useState(user?.email || '');

  useEffect(() => {
    if (!user) {
      navigate('/');
    }
  }, [user, navigate]);

  const handleSave = (e) => {
    e.preventDefault();
    // console.log('Saving profile:', { username, email });
    alert('プロフィールが更新されました。（実際には保存されません）');
  };

  const navigateToDashboard = () => {
    navigate('/dashboard', { state: { user } });
  }

  if (!user) return null;

  return (
    <div className={styles.background}>
    <div className={styles.pageContainer}>
        <header className={styles.header}>
            <div className={styles.logoContainer} onClick={navigateToDashboard}>
              <img src="/logo.png" alt="ANNOTOPIA Logo" className={styles.logo} />
              <span className={styles.logoText}>ANNOTOPIA</span>
            </div>
            <div className={styles.userMenu}>
              <span className={styles.username}>こんにちは、{user.username}さん</span>
              <button onClick={logout} className={styles.logoutButton}>
                ログアウト
              </button>
            </div>
        </header>
        <main className={styles.main}>
            <div className={styles.headingContainer}>
                <h1 className={styles.heading}>プロフィール設定</h1>
                <button onClick={navigateToDashboard} className={styles.dashboardButton}>ダッシュボードに戻る</button>
            </div>

            <div className={styles.profileCard}>
            <div className={styles.profileHeader}>
                <div className={styles.avatar}>
                {username.charAt(0).toUpperCase()}
                </div>
                <div className={styles.userInfo}>
                <h2>{user.username}</h2>
                <p>{user.email}</p>
                </div>
            </div>

            <form onSubmit={handleSave}>
                <div className={styles.formGroup}>
                <label htmlFor="username" className={styles.label}>ユーザー名</label>
                <input
                    type="text"
                    id="username"
                    className={styles.input}
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                </div>

                <div className={styles.formGroup}>
                <label htmlFor="email" className={styles.label}>メールアドレス</label>
                <input
                    type="email"
                    id="email"
                    className={styles.input}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                </div>
                
                <div className={styles.formGroup}>
                <label htmlFor="role" className={styles.label}>役割</label>
                <input
                    type="text"
                    id="role"
                    className={styles.input}
                    value={user.role}
                    disabled
                />
                </div>

                <div className={styles.buttonGroup}>
                <button type="submit" className={styles.saveButton}>
                    変更を保存
                </button>
                </div>
            </form>
            </div>
        </main>
    </div>
    </div>
  );
};

export default ProfilePage;
